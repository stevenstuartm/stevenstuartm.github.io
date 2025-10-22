---
title: "AWS CloudFormation: Migrating Existing Resources"
layout: guide
category: Infrastructure & Cloud
subcategory: AWS
description: "Step-by-step guide for bringing existing manually-created AWS resources under CloudFormation management."
---

## Table of Contents
1. [Overview](#overview)
2. [Step 1: Discover Resources](#step-1-discover-resources)
3. [Step 2: Tag Resources](#step-2-tag-resources)
4. [Step 3: Choose Migration Strategy](#step-3-choose-migration-strategy)
5. [Step 4: Generate Templates](#step-4-generate-templates)
6. [Step 5: Import Resources](#step-5-import-resources)
7. [Step 6: Verify and Validate](#step-6-verify-and-validate)
8. [Step 7: Clean Up](#step-7-clean-up)
9. [Common Challenges](#common-challenges)

---

## Overview

**Goal:** Bring manually-created AWS resources under CloudFormation management.

**Why migrate:**
- Version control for infrastructure
- Drift detection
- Automated deployments
- Rollback capabilities
- Documented architecture

**Migration process:**
1. Discover what resources exist
2. Tag resources for organization
3. Choose import vs recreate strategy
4. Generate CloudFormation templates
5. Import resources into stacks
6. Verify with drift detection
7. Clean up temporary tags

---

## Step 1: Discover Resources

Find all existing resources in your AWS account before migrating them.

### Use AWS Tag Editor

**Access:** AWS Console → Resource Groups & Tag Editor → Tag Editor

**Steps:**
1. Select regions (all or specific)
2. Select resource types (all or specific)
3. Add tag filters (optional, if resources already tagged)
4. Click "Search resources"
5. Export results to CSV for planning

**What you learn:**
- What resources exist across regions
- Current tags on resources
- Resource types and IDs
- Dependencies between resources

---

## Step 2: Tag Resources

Apply organizational tags to resources for migration planning and long-term management.

### Required Tags

Apply these three tags to all resources:

```yaml
environment: prod | dev | staging
layer: foundation | platform | devops | application
domain: platform | devops | <business-domain-name>
```

**Tagging rules:**
- **environment**: The deployment environment (prod, dev, staging)
- **layer**: Infrastructure layer based on ownership and change frequency
  - `foundation`: VPCs, networking, DNS (platform team, rarely changes)
  - `platform`: Shared services like databases, queues (platform team, occasional changes)
  - `devops`: CI/CD, repos, pipelines (DevOps team, occasional changes)
  - `application`: App-specific resources (app teams, frequent changes)
- **domain**: Ownership hint
  - Use `platform` for foundation and platform layers
  - Use `devops` for devops layer
  - Use business domain name for application layer (e.g., `payments`, `identity`, `orders`)

### Optional Migration Tags (Temporary)

Add these during migration, remove after:

```yaml
MigrationStatus: Pending | InProgress | Completed | Excluded
MigrationBatch: 1 | 2 | 3
```

**Why use migration tags:**
- Track which resources are migrated vs manual
- Query for "Pending" resources to plan batches
- Filter "Excluded" resources (intentionally left manual)
- Create groups by migration status
- **Remove after migration completes**

### Apply Tags

**Single resource:**

```bash
aws resourcegroupstaggingapi tag-resources \
  --resource-arn-list arn:aws:ec2:us-east-1:123456789012:vpc/vpc-abc123 \
  --tags environment=prod,layer=foundation,domain=platform,MigrationStatus=Pending,MigrationBatch=1
```

**Multiple resources:**

```bash
aws resourcegroupstaggingapi tag-resources \
  --resource-arn-list \
    arn:aws:s3:::bucket-1 \
    arn:aws:s3:::bucket-2 \
    arn:aws:rds:us-east-1:123456789012:db:db-1 \
  --tags environment=prod,layer=platform,domain=platform,MigrationStatus=Pending
```

**Query by migration status:**

```bash
# Find all pending resources
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=MigrationStatus,Values=Pending

# Find batch 1 resources
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=MigrationBatch,Values=1
```

### Resource Groups (Optional)

**What they are:** Named, saved queries that filter resources by tags. Think of them as bookmarks for specific sets of resources.

**Why they're useful during migration:**

1. **IaC Generator filtering** (Step 4): When generating templates, IaC Generator lets you filter by resource group. Instead of manually selecting resources each time, you select the group and get all matching resources automatically.

2. **Bulk operations**: Query a group once, get all matching resource ARNs for batch tagging or validation.

3. **Team coordination**: Share named groups across team members ("everyone use the `migration-batch-1` group for this sprint").

4. **Console visibility**: View all resources in a group through the Resource Groups console.

**When you can skip them:**

- Small migrations (fewer than 20 resources)
- One-time operations where writing the tag query directly is faster
- You're comfortable with CLI tag filters

**When to create them:**

- Large migrations with multiple batches over weeks/months
- Repeatedly generating templates for the same resource sets
- Multiple team members working on the migration
- You want visual tracking in the AWS Console

**How to create groups:**

```bash
# Production foundation layer
aws resource-groups create-group \
  --name prod-foundation \
  --resource-query '{
    "Type": "TAG_FILTERS_1_0",
    "Query": "{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"environment\",\"Values\":[\"prod\"]},{\"Key\":\"layer\",\"Values\":[\"foundation\"]}]}"
  }'

# Migration batch 1
aws resource-groups create-group \
  --name migration-batch-1 \
  --resource-query '{
    "Type": "TAG_FILTERS_1_0",
    "Query": "{\"ResourceTypeFilters\":[\"AWS::AllSupported\"],\"TagFilters\":[{\"Key\":\"MigrationBatch\",\"Values\":[\"1\"]}]}"
  }'
```

**Using groups in later steps:**

In Step 4 (Generate Templates), IaC Generator Console allows you to filter by resource group when selecting which resources to include in the generated template. This saves time versus manually selecting resources or writing tag filter queries.

---

## Step 3: Choose Migration Strategy

Decide whether to import resources as-is or recreate them from scratch.

### Option A: Import (No Downtime)

**What it does:** Brings existing resources under CloudFormation without recreating them.

**When to use:**
- Production resources that can't tolerate downtime
- Stateful resources (databases, S3 buckets with data)
- Resources with complex configurations
- Resources already correctly configured

**Advantages:**
- Zero downtime
- No resource recreation
- Immediate CloudFormation management
- Resources keep same IDs and configurations

**Disadvantages:**
- Template must match exact current configuration
- Inherits any technical debt
- More complex for resources with many dependencies

**Recommended for:**
- Foundation layer (VPCs, networking)
- Platform layer (shared databases, queues, registries)
- Any stateful resources with data

### Option B: Recreate (Clean Start)

**What it does:** Create new resources via CloudFormation, migrate data, delete old resources.

**When to use:**
- Non-critical resources
- Easily replaceable resources
- Want to redesign or apply best practices
- Can tolerate downtime or migration window

**Advantages:**
- Clean slate (no configuration baggage)
- Apply best practices from scratch
- Simpler templates
- Forces documentation

**Disadvantages:**
- Requires downtime or migration window
- Data migration complexity
- Higher risk
- Resources get new IDs

**Recommended for:**
- DevOps layer (pipelines, repos - can recreate)
- Application layer compute (EC2, Lambda - can recreate)
- Non-critical resources

### Option C: Hybrid (Phased Approach)

**What it does:** Import critical resources, recreate others, migrate gradually.

**When to use:**
- Large, complex environments
- Want to minimize risk
- Different teams own different resources

**Approach:**
- Import foundation and platform layers
- Recreate DevOps and application layers
- Migrate workloads gradually
- Decommission old resources over time

---

## Step 4: Generate Templates

Create CloudFormation templates that describe your existing resources.

### Option A: Use IaC Generator

**What it is:** AWS service that scans your account and generates CloudFormation templates.

**How to use:**

**1. Scan your account:**

```bash
# Create a resource scan
aws cloudformation create-resource-scan

# List scans
aws cloudformation list-resource-scans

# Get scan details
aws cloudformation describe-resource-scan \
  --resource-scan-id <scan-id>
```

**2. List resources found:**

```bash
aws cloudformation list-resource-scan-resources \
  --resource-scan-id <scan-id>
```

**3. Generate template:**

In AWS Console:
1. CloudFormation → IaC Generator
2. Review scanned resources
3. Select resources to include (use tags or resource groups to filter)
4. Generate template
5. Download YAML template

**4. Review and customize:**

```yaml
# Generated template will look like:
AWSTemplateFormatVersion: '2010-09-09'
Description: Generated from existing resources

Parameters:
  BucketName:
    Type: String
    Default: my-existing-bucket

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      VersioningConfiguration:
        Status: Enabled
```

**Limitations:**
- Over 600 resource types supported, but not all
- May not capture all configuration details
- Check [supported resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/resource-import-supported-resources.html){:target="_blank" rel="noopener noreferrer"}

### Option B: Write Templates Manually

**When to use:**
- IaC Generator doesn't support the resource type
- You want full control over template structure
- Simple resources where manual is faster

**How to do it:**

1. Use AWS Console or CLI to view current resource configuration
2. Look up CloudFormation resource documentation
3. Write template matching current configuration
4. Validate template syntax

```bash
# Validate template
aws cloudformation validate-template \
  --template-body file://template.yaml

# Use cfn-lint for better validation
pip install cfn-lint
cfn-lint template.yaml
```

---

## Step 5: Import Resources

Bring existing resources under CloudFormation management using the import operation.

### Prepare Import File

Create a JSON file specifying which resources to import:

```json
[
  {
    "ResourceType": "AWS::S3::Bucket",
    "LogicalResourceId": "MyBucket",
    "ResourceIdentifier": {
      "BucketName": "my-actual-bucket-name"
    }
  },
  {
    "ResourceType": "AWS::EC2::VPC",
    "LogicalResourceId": "MainVPC",
    "ResourceIdentifier": {
      "VpcId": "vpc-abc123"
    }
  }
]
```

**Resource identifier by type:**

| Resource Type | Identifier Property |
|--------------|---------------------|
| AWS::S3::Bucket | BucketName |
| AWS::EC2::Instance | InstanceId |
| AWS::EC2::VPC | VpcId |
| AWS::RDS::DBInstance | DBInstanceIdentifier |
| AWS::Lambda::Function | FunctionName |
| AWS::DynamoDB::Table | TableName |
| AWS::IAM::Role | RoleName |

### Import into New Stack

```bash
aws cloudformation create-stack \
  --stack-name prod-foundation \
  --template-body file://template.yaml \
  --resources-to-import file://resources-to-import.json
```

### Import into Existing Stack

```bash
# 1. Create change set with import
aws cloudformation create-change-set \
  --stack-name existing-stack \
  --change-set-name import-more-resources \
  --change-set-type IMPORT \
  --template-body file://updated-template.yaml \
  --resources-to-import file://resources-to-import.json

# 2. Review change set
aws cloudformation describe-change-set \
  --stack-name existing-stack \
  --change-set-name import-more-resources

# 3. Execute import
aws cloudformation execute-change-set \
  --stack-name existing-stack \
  --change-set-name import-more-resources
```

### Requirements for Successful Import

**Template requirements:**
- Resource properties must match existing resource exactly
- Must include all required properties
- Use correct resource identifier property

**Common import failures:**
- Template property doesn't match actual resource
- Missing required properties
- Resource already managed by another stack
- Resource doesn't exist

---

## Step 6: Verify and Validate

After importing, verify the template accurately represents the actual resource configuration.

### Detect Drift

```bash
# Start drift detection
aws cloudformation detect-stack-drift \
  --stack-name prod-foundation

# Get drift detection status
aws cloudformation describe-stack-drift-detection-status \
  --stack-drift-detection-id <detection-id>

# View drift details
aws cloudformation describe-stack-resource-drifts \
  --stack-name prod-foundation
```

### Interpret Drift Results

**IN_SYNC:** Template matches actual resource - good!

**MODIFIED:** Actual resource differs from template:
- Someone changed the resource manually after import
- Template doesn't capture all properties
- **Action:** Update template to match reality or fix the resource

**DELETED:** Resource no longer exists:
- Resource was deleted outside CloudFormation
- **Action:** Recreate or remove from template

**NOT_CHECKED:** Resource type doesn't support drift detection

### Fix Drift

If drift detected, you have two options:

**Option 1: Update template to match reality**

```bash
# 1. Update template with actual configuration
# 2. Update stack
aws cloudformation update-stack \
  --stack-name prod-foundation \
  --template-body file://updated-template.yaml
```

**Option 2: Fix resource to match template**

Manually change the resource back to match the template, or use CloudFormation to update it.

---

## Step 7: Clean Up

After migration completes, remove temporary migration tags.

### Remove Migration Tags

```bash
# Single resource
aws resourcegroupstaggingapi untag-resources \
  --resource-arn-list arn:aws:ec2:us-east-1:123456789012:vpc/vpc-abc123 \
  --tag-keys MigrationStatus MigrationBatch

# Multiple resources
aws resourcegroupstaggingapi untag-resources \
  --resource-arn-list \
    arn:aws:s3:::bucket-1 \
    arn:aws:s3:::bucket-2 \
  --tag-keys MigrationStatus MigrationBatch
```

### Keep Organizational Tags

**Keep these tags permanently:**
- `environment`
- `layer`
- `domain`

These tags align with your IaC organization and help with ongoing management.

### Delete Temporary Resource Groups

```bash
# Delete migration-specific groups
aws resource-groups delete-group \
  --group-name migration-batch-1
```

Keep permanent groups for layer/environment organization.

---

## Common Challenges

### Challenge 1: Resources Without CloudFormation Support

**Problem:** Not all AWS resources support CloudFormation or import.

**Solutions:**
- Use AWS CDK custom resources
- Use CloudFormation custom resources with Lambda
- Manage separately with Terraform or scripts
- Check AWS roadmap for future support

### Challenge 2: Template Doesn't Match Resource

**Problem:** Import fails because template properties don't match actual resource.

**Solutions:**
- Use IaC Generator to get accurate configuration
- Use AWS Console to view actual resource properties
- Compare template with actual configuration carefully
- Start with minimal required properties, add more later

### Challenge 3: Complex Dependencies

**Problem:** Resources have circular dependencies or unclear relationships.

**Solutions:**
- Use Tag Editor to map resource relationships
- Review AWS Config for dependency graph
- Use `DependsOn` attribute explicitly in template
- Break into multiple stacks if needed

### Challenge 4: Drift After Import

**Problem:** Template shows drift immediately after import.

**Solutions:**
- IaC Generator may not capture all properties
- Some properties are computed/output-only (don't include in template)
- Update template to match actual configuration
- Check CloudFormation documentation for resource-specific notes

### Challenge 5: Missing Resource Identifiers

**Problem:** Don't know resource identifier needed for import.

**Solutions:**

```bash
# Find S3 buckets
aws s3 ls

# Find EC2 instance IDs
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0]]'

# Find RDS instances
aws rds describe-db-instances \
  --query 'DBInstances[].[DBInstanceIdentifier,Engine]'

# Find VPC IDs
aws ec2 describe-vpcs \
  --query 'Vpcs[].[VpcId,Tags[?Key==`Name`].Value|[0]]'
```

### Challenge 6: Large Number of Resources

**Problem:** Too many resources to migrate at once.

**Solutions:**
- Use migration batches (tag with `MigrationBatch`)
- Migrate one layer at a time (foundation → platform → devops → application)
- Use Resource Groups to organize batches
- Automate with scripts for repetitive tasks

### Challenge 7: Resources Created by Other Tools

**Problem:** Resources were created by Terraform, CDK, or other tools.

**Solutions:**
- Check if resource is already managed by another tool (avoid conflicts)
- Use `terraform state rm` to remove from Terraform state before importing to CloudFormation
- For CDK: CDK uses CloudFormation under the hood, resources already in stacks
- Document which tool manages what to avoid confusion

---
