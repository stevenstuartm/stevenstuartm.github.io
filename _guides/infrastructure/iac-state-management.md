---
title: "IaC State Management"
layout: guide
category: Infrastructure & Cloud
subcategory: Infrastructure as Code
description: "Understanding infrastructure state, remote backends, state locking, and best practices for managing IaC state across teams."
---

## Table of Contents
1. [What is State](#what-is-state)
2. [Do You Need State Management?](#do-you-need-state-management)
3. [Local vs. Remote State](#local-vs-remote-state)
4. [State Locking](#state-locking)
5. [State Management Best Practices](#state-management-best-practices)
6. [Common State Operations](#common-state-operations)

---

## What is State

**State** is the record of infrastructure resources currently deployed, tracked by IaC tools to:
- Map configuration to real resources
- Track resource metadata
- Determine what changes are needed
- Manage dependencies between resources

### Why State Matters

**Without state, IaC tools cannot:**
- Know what infrastructure currently exists
- Determine what needs to be created, updated, or deleted
- Track resource relationships
- Detect configuration drift

**State contains:**
- Resource IDs
- Resource attributes
- Dependencies between resources
- Provider configurations
- Sensitive data (passwords, private keys)

---

## Do You Need State Management?

**Cloud-native IaC tools handle state automatically** - you don't need to manage state yourself.

### Tools That Manage State for You

**AWS CloudFormation:**
- AWS manages all state internally
- No state files to secure or back up
- No risk of state corruption
- No locking concerns
- Built-in drift detection

**Azure Resource Manager (ARM Templates / Bicep):**
- Azure manages deployment state
- Integrated with Azure portal
- Deployment history tracked automatically

**Google Cloud Deployment Manager:**
- GCP tracks deployment state
- Managed through GCP console

### When State Management Is Your Responsibility

**Terraform and Pulumi** require you to manage state explicitly:
- You must configure remote backends
- You must implement locking mechanisms
- You must secure sensitive data in state
- You must handle backup and recovery
- You must prevent state corruption

### Should You Accept This Complexity?

**Only add user-managed state when you can articulate specific reasons:**

**Valid reasons:**
- Multi-cloud requirements (managing AWS + Azure + GCP together)
- Need for Terraform/Pulumi-specific features not available in cloud-native tools
- Existing infrastructure already managed by Terraform/Pulumi
- Organizational standard requires specific tooling

**Not valid reasons:**
- "Terraform is popular"
- "We know Terraform already" (unless you have multi-cloud needs)
- "Terraform is industry standard" (CloudFormation is the standard for AWS-only)

**The cost of user-managed state:**
- Risk of state corruption causing infrastructure issues
- Complexity of securing state files containing sensitive data
- Operational overhead of managing remote backends and locking
- Recovery procedures when state issues occur
- Additional infrastructure to support state management

**If you're deploying only to AWS, CloudFormation eliminates all of these risks.**

---

## Local vs. Remote State

### Local State

**What it is:** State stored on local filesystem.

```
terraform.tfstate
```

**Advantages:**
- Simple to get started
- No additional setup required
- Fast access

**Disadvantages:**
- ❌ Not suitable for teams (no sharing)
- ❌ No locking (concurrent changes dangerous)
- ❌ Risk of loss/corruption
- ❌ No backup/versioning
- ❌ Contains sensitive data locally

**When to use:**
- Learning and experimentation only
- Single developer, non-critical infrastructure
- Never for production

### Remote State

**What it is:** State stored in a remote backend (S3, Azure Blob, GCS, Terraform Cloud).

**Terraform S3 Backend:**
```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Advantages:**
- ✅ Shared access for teams
- ✅ State locking (prevents conflicts)
- ✅ Encryption at rest
- ✅ Versioning and backup
- ✅ Audit logging
- ✅ Centralized management

**Disadvantages:**
- Requires setup
- Depends on external service
- Potential costs

**When to use:**
- All team environments
- Production infrastructure
- Any collaborative work

### Popular Remote Backends

**AWS S3 + DynamoDB:**
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "path/to/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # For locking
    encrypt        = true
    kms_key_id     = "arn:aws:kms:..."  # Optional KMS encryption
  }
}
```

**Azure Blob Storage:**
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}
```

**Google Cloud Storage:**
```hcl
terraform {
  backend "gcs" {
    bucket = "terraform-state"
    prefix = "prod"
  }
}
```

**Terraform Cloud:**
```hcl
terraform {
  cloud {
    organization = "my-org"
    workspaces {
      name = "production"
    }
  }
}
```

---

## State Locking

**What it is:** Preventing simultaneous state modifications that could corrupt state.

### How Locking Works

1. Process acquires lock before modifying state
2. Lock prevents other processes from modifying state
3. Lock released after operation completes or fails

### Implementations

**DynamoDB (AWS + S3 backend):**
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"  # Locking table
  }
}
```

**DynamoDB table structure:**
```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

**Consul:**
```hcl
terraform {
  backend "consul" {
    address = "consul.example.com"
    path    = "terraform/prod"
    lock    = true
  }
}
```

### Force Unlock (Use Carefully)

```bash
# Only use if lock is stuck
terraform force-unlock <lock-id>
```

**When to force unlock:**
- Process crashed and left lock
- Lock is stale
- You're certain no one else is running operations

**Never force unlock if:**
- Someone else might be running operations
- Uncertain about lock state

---

## State Management Best Practices

### 1. Always Use Remote State for Teams

**Never rely on local state files for production or team environments.**

```hcl
# ❌ BAD: No backend configured
terraform {
  # Uses local state
}

# ✅ GOOD: Remote backend
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-locks"
  }
}
```

### 2. Secure State Files

**State contains sensitive data!**

**Enable encryption:**
```hcl
terraform {
  backend "s3" {
    bucket  = "terraform-state"
    key     = "terraform.tfstate"
    encrypt = true  # Enable encryption at rest
    kms_key_id = "arn:aws:kms:..."  # Use KMS for extra security
  }
}
```

**Restrict access:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::terraform-state/prod/*",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/TerraformRole"
      }
    }
  ]
}
```

**Never commit state to Git:**
```
# .gitignore
*.tfstate
*.tfstate.*
```

### 3. Backup State

**Enable versioning:**
```hcl
resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

**Regular backups:**
- S3 versioning (automatic)
- Cross-region replication
- Periodic manual backups
- Test restore procedures

### 4. Separate State by Environment

**Don't share state across environments:**

```
s3://terraform-state/
├── dev/terraform.tfstate
├── staging/terraform.tfstate
└── production/terraform.tfstate
```

**Or use separate buckets:**
```
s3://terraform-state-dev/terraform.tfstate
s3://terraform-state-staging/terraform.tfstate
s3://terraform-state-prod/terraform.tfstate
```

### 5. Review Plans Before Applying

```bash
# Always plan first
terraform plan -out=tfplan

# Review carefully
# Then apply
terraform apply tfplan
```

### 6. State File Security Checklist

- [ ] Remote backend configured
- [ ] Encryption at rest enabled
- [ ] State locking enabled
- [ ] Versioning enabled
- [ ] Access restricted via IAM
- [ ] State files not in Git
- [ ] Regular backups tested
- [ ] Separate state per environment

---

## Common State Operations

### Viewing State

```bash
# List all resources in state
terraform state list

# Show details of specific resource
terraform state show aws_instance.web

# Get output values
terraform output
```

### Modifying State

**Move resource:**
```bash
# Rename resource in state
terraform state mv aws_instance.web aws_instance.web_server

# Move to different module
terraform state mv aws_instance.web module.compute.aws_instance.web
```

**Remove resource:**
```bash
# Remove from state (doesn't delete actual resource)
terraform state rm aws_instance.old

# Now you can delete or import elsewhere
```

**Import existing resource:**
```bash
# Import existing AWS instance into state
terraform import aws_instance.existing i-1234567890abcdef0
```

### Recovering from State Issues

**Pull remote state:**
```bash
# Download current remote state
terraform state pull > backup.tfstate
```

**Push state:**
```bash
# Upload state (use with caution!)
terraform state push backup.tfstate
```

**Replace corrupted state:**
```bash
# 1. Download backup from S3
aws s3 cp s3://terraform-state/prod/terraform.tfstate backup.tfstate

# 2. Push backup
terraform state push backup.tfstate
```

### Migrating State

**Change backend:**
```hcl
# Old backend
terraform {
  backend "local" {}
}

# New backend
terraform {
  backend "s3" {
    bucket = "terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
```

```bash
# Migrate state
terraform init -migrate-state
```

---

