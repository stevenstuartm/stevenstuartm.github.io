---
title: "IaC Testing Strategies"
layout: guide
category: Infrastructure & Cloud
subcategory: Infrastructure as Code
description: "Static analysis, unit testing, integration testing, and compliance testing strategies for infrastructure code."
---

## Table of Contents
1. [Why Test Infrastructure](#why-test-infrastructure)
2. [Testing Levels](#testing-levels)
3. [Static Analysis](#static-analysis)
4. [Unit Testing](#unit-testing)
5. [Integration Testing](#integration-testing)
6. [Compliance Testing](#compliance-testing)
7. [Testing Strategy](#testing-strategy)

---

## Why Test Infrastructure

**Catch errors early:**
- Syntax errors before deployment
- Logic errors before production
- Security misconfigurations before breaches
- Policy violations before non-compliance

**Confidence in changes:**
- Safe refactoring
- Prevent regressions
- Validate assumptions
- Speed up deployments

**Documentation:**
- Tests document expected behavior
- Serve as examples
- Capture business requirements

---

## Testing Levels

```
        /\
       /E2E\          ← Few, slow, expensive
      /─────\
     / Integ \        ← More, faster, cheaper
    /────────\
   /  Unit   \       ← Many, fast, inexpensive
  /───────────\
 / Static Ana \      ← Most, instant, free
/─────────────\
```

**Static Analysis (70%):**
- Syntax validation
- Linting
- Security scanning
- Policy checking
- Run on every commit

**Unit Tests (20%):**
- Test individual modules
- Mock dependencies
- Fast execution
- Run on every commit

**Integration Tests (9%):**
- Test full stacks
- Real cloud resources
- Slower execution
- Run before merge

**End-to-End Tests (1%):**
- Complete workflows
- Production-like environment
- Very slow
- Run before production

---

## Static Analysis

**What it is:** Analyze code without executing it.

### Tools

**Terraform:**
```bash
# Validate syntax
terraform validate

# Lint code
tflint

# Security scanning
checkov -d .
tfsec .
terrascan scan

# Format check
terraform fmt -check -recursive
```

**CloudFormation:**
```bash
# Validate template
aws cloudformation validate-template --template-body file://template.yaml

# Lint
cfn-lint template.yaml

# Security scanning
cfn_nag_scan --input-path template.yaml
```

### What Static Analysis Catches

- Syntax errors
- Deprecated syntax
- Security issues (open security groups, unencrypted storage)
- Best practice violations
- Policy compliance issues
- Resource naming violations

### CI/CD Integration

```yaml
# GitHub Actions
name: Static Analysis
on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Validate
        run: |
          terraform init -backend=false
          terraform validate

      - name: TFLint
        uses: terraform-linters/setup-tflint@v3
        with:
          tflint_version: latest

      - name: Run TFLint
        run: tflint --recursive

      - name: Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform
          soft_fail: false

      - name: tfsec
        uses: aquasecurity/tfsec-action@v1.0.0
```

---

## Unit Testing

**What it is:** Test individual modules in isolation.

### Tools

**Terratest (Go):**
```go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCModule(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../modules/vpc",
        Vars: map[string]interface{}{
            "cidr_block":  "10.0.0.0/16",
            "environment": "test",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcId := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcId)

    cidr := terraform.Output(t, terraformOptions, "vpc_cidr")
    assert.Equal(t, "10.0.0.0/16", cidr)
}
```

**Pytest (Python + boto3):**
```python
import pytest
import boto3
import subprocess

@pytest.fixture
def deployed_vpc():
    # Deploy with Terraform
    subprocess.run(["terraform", "init"], check=True)
    subprocess.run(["terraform", "apply", "-auto-approve"], check=True)

    yield

    # Cleanup
    subprocess.run(["terraform", "destroy", "-auto-approve"], check=True)

def test_vpc_exists(deployed_vpc):
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs(
        Filters=[{'Name': 'tag:Name', 'Values': ['test-vpc']}]
    )
    assert len(vpcs['Vpcs']) == 1

def test_vpc_cidr(deployed_vpc):
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs(
        Filters=[{'Name': 'tag:Name', 'Values': ['test-vpc']}]
    )
    assert vpcs['Vpcs'][0]['CidrBlock'] == '10.0.0.0/16'
```

### What Unit Tests Validate

- Module inputs/outputs
- Resource creation
- Resource configuration
- Dependencies
- Error handling

---

## Integration Testing

**What it is:** Test complete infrastructure stacks in isolated environments.

### Approach

1. Deploy infrastructure to test environment
2. Validate resources created correctly
3. Test connectivity and functionality
4. Destroy test infrastructure

### Example Integration Test

```bash
#!/bin/bash
set -e

# Deploy to test environment
terraform workspace select test
terraform apply -auto-approve

# Get outputs
VPC_ID=$(terraform output -raw vpc_id)
ALB_DNS=$(terraform output -raw alb_dns)

# Test 1: VPC exists
aws ec2 describe-vpcs --vpc-ids $VPC_ID

# Test 2: Load balancer healthy
HEALTH=$(aws elbv2 describe-target-health \
  --target-group-arn $(terraform output -raw target_group_arn) \
  --query 'TargetHealthDescriptions[0].TargetHealth.State' \
  --output text)

if [ "$HEALTH" != "healthy" ]; then
  echo "Load balancer unhealthy"
  exit 1
fi

# Test 3: Application responds
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://$ALB_DNS)
if [ "$HTTP_CODE" != "200" ]; then
  echo "Application not responding"
  exit 1
fi

echo "All integration tests passed"

# Cleanup
terraform destroy -auto-approve
```

### Tools

**Kitchen-Terraform:**
```yaml
# .kitchen.yml
---
driver:
  name: terraform

provisioner:
  name: terraform

platforms:
  - name: aws

suites:
  - name: default
    driver:
      variables:
        environment: test
    verifier:
      name: terraform
      systems:
        - name: default
          backend: aws
          controls:
            - operating_system
```

---

## Compliance Testing

**What it is:** Validate infrastructure against organizational policies and regulatory requirements.

### Tools

**Open Policy Agent (OPA):**
```rego
package terraform.analysis

import input as tfplan

deny[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_s3_bucket"
    not resource.change.after.server_side_encryption_configuration
    msg := sprintf(
        "S3 bucket %s must have encryption enabled",
        [resource.address]
    )
}

deny[msg] {
    resource := tfplan.resource_changes[_]
    resource.type == "aws_security_group"
    rule := resource.change.after.ingress[_]
    rule.cidr_blocks[_] == "0.0.0.0/0"
    rule.from_port == 22
    msg := sprintf(
        "Security group %s allows SSH from anywhere",
        [resource.address]
    )
}
```

**HashiCorp Sentinel:**
```hcl
import "tfplan"

main = rule {
  all tfplan.resources.aws_s3_bucket as _, buckets {
    all buckets as _, b {
      b.applied.server_side_encryption_configuration is not null
    }
  }
}
```

**Cloud Custodian:**
```yaml
policies:
  - name: s3-encryption-required
    resource: s3
    filters:
      - type: value
        key: ServerSideEncryptionConfiguration
        value: absent
    actions:
      - type: notify
        violation_desc: "S3 bucket must have encryption enabled"
```

### What Compliance Tests Validate

- Security policies
- Compliance requirements (HIPAA, PCI-DSS, etc.)
- Naming conventions
- Tagging standards
- Cost controls
- Resource limits

---

## Testing Strategy

### Pre-Commit

```bash
# Run locally before committing
terraform fmt -recursive
terraform validate
tflint
```

**Git Hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

terraform fmt -check -recursive
terraform validate
tflint
```

### Pull Request

```yaml
# CI/CD pipeline
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Static Analysis
        run: |
          terraform fmt -check
          terraform validate
          tflint
          checkov -d .

      - name: Unit Tests
        run: |
          cd tests
          go test -v ./...

      - name: Plan
        run: terraform plan

      - name: Compliance
        run: conftest test --policy policies/ terraform/
```

### Pre-Merge

```yaml
integration-test:
  runs-on: ubuntu-latest
  if: github.event.pull_request.merged == true
  steps:
    - name: Deploy to test environment
      run: terraform apply -auto-approve

    - name: Run integration tests
      run: ./integration-tests.sh

    - name: Cleanup
      run: terraform destroy -auto-approve
```

### Pre-Production

- Deployment to staging environment
- Smoke tests
- Performance validation
- Security validation
- Manual review

### Production

- Gradual rollout
- Monitoring and alerting
- Automated rollback on failure

---

