---
title: "CI/CD: Continuous Integration and Continuous Delivery"
layout: guide
category: Software Development Lifecycle
subcategory: SDLC & Modeling
description: "CI/CD fundamentals, pipeline design, automation strategies, security gates, testing approaches, and deployment workflows for modern software delivery."
---

## Table of Contents
1. [What is CI/CD](#what-is-cicd)
2. [Continuous Integration (CI)](#continuous-integration-ci)
3. [Continuous Delivery and Deployment](#continuous-delivery-and-deployment)
4. [Pipeline Architecture](#pipeline-architecture)
5. [Automated Testing in Pipelines](#automated-testing-in-pipelines)
6. [Security Gates and Scanning](#security-gates-and-scanning)
7. [Secrets and Credential Management](#secrets-and-credential-management)
8. [Pipeline Hardening](#pipeline-hardening)
9. [Continuous Compliance](#continuous-compliance)
10. [CI/CD Platforms and Tools](#cicd-platforms-and-tools)

---

## What is CI/CD

**CI/CD** is a set of practices that automate the integration, testing, and delivery of software changes, enabling teams to ship code faster, more reliably, and with higher quality.

### Core Components

**Continuous Integration (CI):**
The practice of frequently merging code changes into a shared repository, with automated builds and tests to catch integration issues early.

**Continuous Delivery (CD):**
The practice of automatically preparing code for release to production, ensuring it's always in a deployable state.

**Continuous Deployment:**
An extension of continuous delivery where every change that passes automated tests is automatically deployed to production.

### Why CI/CD Matters

**Speed and Frequency:**
- Deploy multiple times per day instead of monthly or quarterly
- Reduce time from code commit to production from weeks to hours
- Enable faster feedback loops and iteration

**Quality and Reliability:**
- Catch bugs earlier through automated testing
- Reduce manual errors through automation
- Ensure consistent build and deployment processes
- Enable quick rollbacks when issues occur

**Developer Productivity:**
- Eliminate repetitive manual tasks
- Reduce context switching and deployment friction
- Provide fast feedback on code quality
- Allow developers to focus on building features

**Business Value:**
- Faster time to market for features
- Reduced risk of large, complex releases
- Better responsiveness to market changes
- Lower operational costs through automation

---

## Continuous Integration (CI)

**Continuous Integration** is the practice of automatically building and testing code every time a team member commits changes to version control.

### Core CI Principles

**1. Maintain a Single Source Repository**
- All code lives in version control (Git, etc.)
- Include build scripts, tests, and configuration
- Never rely on code that exists only on developer machines

**2. Automate the Build**
- Build should run with a single command
- No manual steps required
- Reproducible on any machine

**3. Make Your Build Self-Testing**
- Automated tests run as part of the build
- Build fails if tests fail
- Tests must be fast enough to run frequently

**4. Everyone Commits to Mainline Every Day**
- Small, frequent commits reduce integration risk
- Keeps branches short-lived (feature flags for incomplete work)
- Reduces merge conflicts and integration hell

**5. Every Commit Triggers a Build**
- Automated build and test on every commit
- Fast feedback to developers (< 10 minutes ideal)
- Clear pass/fail status

**6. Keep the Build Fast**
- Optimize test suite for speed
- Use test parallelization
- Consider splitting into fast and slow test suites

**7. Test in a Clone of Production**
- Build and test in environment matching production
- Use containers or infrastructure-as-code for consistency
- Avoid "works on my machine" problems

**8. Make it Easy to Get Latest Deliverables**
- Latest build artifacts readily available
- Clear versioning and tagging
- Artifact repository for binaries

**9. Everyone Can See Results**
- Build status visible to entire team
- Radiator/dashboard showing build health
- Notifications for failures

**10. Automate Deployment**
- Push-button or automated deployment
- Same deployment process for all environments
- Deployment is part of the CI process

### CI Workflow

```
Developer commits code
       ↓
Trigger CI pipeline
       ↓
Checkout code
       ↓
Install dependencies
       ↓
Build application
       ↓
Run automated tests
       ├─ Unit tests
       ├─ Integration tests
       └─ Linting/static analysis
       ↓
Generate build artifacts
       ↓
Report results to team
```

### Benefits of CI

**Early Bug Detection:**
- Find integration issues within hours, not weeks
- Easier to debug (fewer changes to investigate)
- Cheaper to fix (developer context still fresh)

**Reduced Integration Risk:**
- Small, frequent integrations are less risky than big bang merges
- Merge conflicts caught and resolved quickly
- Always have a working build

**Higher Code Quality:**
- Automated testing enforces quality gates
- Code review integrated into workflow
- Static analysis catches issues automatically

**Better Collaboration:**
- Shared responsibility for build health
- Transparency around code quality
- Faster feedback cycles

---

## Continuous Delivery and Deployment

### Continuous Delivery

**Continuous Delivery** ensures code is always in a deployable state, with automated testing and deployment to staging environments. Deployment to production requires manual approval.

**Key characteristics:**
- Every change passes automated tests
- Code can be deployed to production at any time
- Deployment is a business decision, not a technical constraint
- Manual approval gate before production

**Workflow:**
```
Code commit → CI build → Deploy to staging → Automated tests → Ready for production
                                                                          ↓
                                                                  Manual approval
                                                                          ↓
                                                                Deploy to production
```

### Continuous Deployment

**Continuous Deployment** takes continuous delivery one step further: every change that passes automated tests is automatically deployed to production without manual intervention.

**Key characteristics:**
- Fully automated pipeline from commit to production
- No manual approval gates
- Requires high confidence in automated testing
- Fast feedback from real users

**Workflow:**
```
Code commit → CI build → Automated tests → Deploy to staging → More tests → Auto-deploy to production
```

### CD vs. Continuous Deployment

| Aspect | Continuous Delivery | Continuous Deployment |
|--------|--------------------|-----------------------|
| Production deployment | Manual approval required | Fully automated |
| Release frequency | As needed (on-demand) | Every successful build |
| Risk tolerance | Lower (manual gate provides control) | Higher (requires robust automation) |
| Feedback speed | Moderate | Very fast |
| Required maturity | Moderate | High |

### Prerequisites for CD/Continuous Deployment

**Robust Automated Testing:**
- Comprehensive test suite covering critical paths
- High confidence in test accuracy (low false positives/negatives)
- Fast test execution

**Deployment Automation:**
- Infrastructure as Code (IaC)
- Automated provisioning and configuration
- Consistent deployment across environments

**Monitoring and Observability:**
- Real-time monitoring of application health
- Automated alerting on anomalies
- Fast rollback capabilities

**Feature Flags:**
- Decouple deployment from release
- Gradual rollouts and A/B testing
- Quick feature toggles for issues

**Culture of Quality:**
- Shared responsibility for production
- Blameless post-mortems
- Investment in testing and automation

---

## Pipeline Architecture

### Pipeline Stages

A typical CI/CD pipeline consists of multiple stages that code must pass through before reaching production.

**Stage 1: Source**
- Triggered by code commit or pull request
- Fetch code from version control
- Determine what changed

**Stage 2: Build**
- Compile code
- Resolve dependencies
- Create build artifacts
- Run fast validation checks

**Stage 3: Test**
- Unit tests
- Integration tests
- Static analysis and linting
- Code coverage analysis

**Stage 4: Security Scan**
- SAST (Static Application Security Testing)
- Dependency scanning (SCA)
- Secret detection
- License compliance checks

**Stage 5: Package**
- Create deployable artifacts
- Build container images
- Version and tag artifacts
- Push to artifact repository

**Stage 6: Deploy to Staging**
- Deploy to staging environment
- Run smoke tests
- Dynamic security testing (DAST)
- Performance testing

**Stage 7: Deploy to Production**
- Manual approval (Continuous Delivery) or automatic (Continuous Deployment)
- Deployment strategy (blue-green, canary, rolling)
- Production smoke tests
- Monitor for issues

**Stage 8: Post-Deployment**
- Verify deployment success
- Monitor application health
- Collect metrics
- Alert on anomalies

### Pipeline Design Principles

**1. Pipeline as Code**
- Store pipeline definitions in version control
- Use declarative configuration (YAML, JSON)
- Enable code review of pipeline changes
- Version and track pipeline evolution

**2. Fast Feedback**
- Run fastest tests first
- Fail fast on critical issues
- Provide clear error messages
- Notify developers immediately

**3. Idempotent and Reproducible**
- Same inputs produce same outputs
- No manual steps required
- Isolated from external state
- Use fixed versions for dependencies

**4. Environment Parity**
- Consistent environments across pipeline
- Use containers or IaC for reproducibility
- Minimize dev/prod differences

**5. Automated Rollback**
- Quick rollback mechanism
- Tested rollback procedures
- Preserve previous versions
- Automated health checks trigger rollback

**6. Security by Default**
- Security scanning integrated, not optional
- Fail builds on critical vulnerabilities
- Least privilege for pipeline permissions
- Audit all pipeline activities

### Pipeline Patterns

**Sequential Pipeline:**
```
Build → Test → Package → Deploy → Verify
```
- Simple and predictable
- Stages run one after another
- Easy to understand and debug

**Parallel Pipeline:**
```
        ├─ Unit Tests
Build ──├─ Integration Tests
        ├─ Security Scan
        └─ Linting
           ↓
        Package → Deploy
```
- Faster execution
- Independent stages run concurrently
- Requires more resources

**Fan-Out/Fan-In Pipeline:**
```
              ├─ Deploy to Region A
Package  ────├─ Deploy to Region B ───→ Aggregate Results → Verify
              └─ Deploy to Region C
```
- Deploy to multiple targets simultaneously
- Collect and aggregate results
- Useful for multi-region deployments

**Branch-Based Pipeline:**
```
Feature Branch → PR Pipeline (build, test, security scan)
       ↓
Main Branch → Full Pipeline (build, test, scan, deploy to staging)
       ↓
Release Tag → Production Pipeline (deploy to prod)
```
- Different pipeline behavior per branch
- More thorough validation on main branch
- Production deployments from release tags

---

## Automated Testing in Pipelines

### Testing Pyramid

```
        /\
       /UI\          ← Few, slow, expensive
      /─────\
     / API  \        ← More, faster, cheaper
    /────────\
   /  Unit   \       ← Many, fast, inexpensive
  /───────────\
```

**Unit Tests (70%):**
- Test individual functions/methods in isolation
- Very fast (milliseconds)
- Run on every commit
- High code coverage (80%+ goal)

**Integration Tests (20%):**
- Test multiple components together
- Moderate speed (seconds)
- Test API endpoints, database interactions
- Run on every commit

**End-to-End/UI Tests (10%):**
- Test complete user workflows
- Slow (minutes)
- Brittle and expensive to maintain
- Run on main branch or before deployment

### Test Types in CI/CD

**Unit Tests:**
- Run first in pipeline (fast feedback)
- Should complete in < 5 minutes
- High test coverage (80%+ is common)
- Mock external dependencies

**Integration Tests:**
- Test API contracts
- Database interactions
- Third-party service integrations (with mocking)
- Should complete in < 15 minutes

**Contract Tests:**
- Verify API contracts between services
- Producer and consumer tests
- Tools: Pact, Spring Cloud Contract
- Prevent breaking changes

**Smoke Tests:**
- Quick validation after deployment
- Test critical user paths
- Verify app is running and accessible
- Run in < 5 minutes

**Performance Tests:**
- Load testing
- Stress testing
- Benchmark comparisons
- Run on staging before production

**Security Tests:**
- Static analysis (SAST)
- Dynamic analysis (DAST)
- Dependency scanning (SCA)
- Penetration testing (periodic)

### Test Strategies

**Shift-Left Testing:**
- Run tests as early as possible
- Developers run tests locally before commit
- Fast feedback reduces context switching
- Catch issues before they reach CI

**Parallel Test Execution:**
- Split tests across multiple workers
- Dramatically reduce test execution time
- Tools: Pytest-xdist, Jest parallel, TestNG parallel

**Flaky Test Management:**
- Identify and quarantine flaky tests
- Track flaky test trends
- Fix or remove consistently flaky tests
- Don't let flaky tests erode confidence

**Test Data Management:**
- Use factories/fixtures for test data
- Database seeding for integration tests
- Isolate test data (separate DB per test run)
- Clean up after tests

---

## Security Gates and Scanning

### Types of Security Scanning

**1. Static Application Security Testing (SAST)**

**What it is:** Analyzes source code, bytecode, or binaries without executing the program to identify security vulnerabilities.

**When to run:**
- On every commit (fast scans)
- On pull requests (comprehensive scans)
- Scheduled deep scans (nightly)

**What SAST catches:**
- SQL injection vulnerabilities
- Cross-site scripting (XSS)
- Buffer overflows
- Insecure cryptography usage
- Code quality issues affecting security
- CWE (Common Weakness Enumeration) violations

**Popular tools:**
- SonarQube / SonarCloud
- Checkmarx
- Veracode
- Semgrep
- CodeQL (GitHub Advanced Security)

**Pipeline integration:**
```yaml
sast:
  stage: security
  script:
    - sonar-scanner -Dsonar.projectKey=myproject
  allow_failure: false
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event'
```

**2. Dynamic Application Security Testing (DAST)**

**What it is:** Tests running applications by sending requests and analyzing responses, simulating real attacks.

**When to run:**
- Against staging environments
- Before production deployment
- Scheduled scans (weekly/monthly)

**What DAST catches:**
- Authentication and session management flaws
- Configuration issues
- Server vulnerabilities
- Runtime issues not visible in code
- OWASP Top 10 vulnerabilities

**Popular tools:**
- OWASP ZAP
- Burp Suite
- Acunetix
- AppScan
- Nikto

**Pipeline integration:**
```yaml
dast:
  stage: security
  script:
    - docker run -t owasp/zap2docker-stable zap-baseline.py -t https://staging.example.com
  only:
    - main
```

**3. Software Composition Analysis (SCA)**

**What it is:** Analyzes third-party dependencies and open-source components for known vulnerabilities and license compliance issues.

**When to run:**
- On every build
- When dependencies change
- Scheduled audits (daily)

**What SCA catches:**
- Known vulnerabilities (CVEs) in dependencies
- Outdated dependencies with available patches
- License compliance issues
- Supply chain risks
- Transitive dependency vulnerabilities

**Popular tools:**
- Snyk
- Dependabot (GitHub)
- WhiteSource / Mend
- Black Duck
- npm audit / pip-audit / cargo audit

**Pipeline integration:**
```yaml
dependency_scan:
  stage: security
  script:
    - npm audit --audit-level=high
    - snyk test --severity-threshold=high
  allow_failure: false
```

**4. Secret Detection**

**What it is:** Scans code, commits, and configuration files for accidentally committed secrets like API keys, passwords, and tokens.

**When to run:**
- Pre-commit hooks (prevent commits)
- On every commit (catch what hooks missed)
- Periodic repository scans
- Pull request validation

**What secret detection catches:**
- API keys and tokens
- Database credentials
- Private keys and certificates
- OAuth tokens
- Cloud provider credentials
- Hardcoded passwords

**Popular tools:**
- GitGuardian
- TruffleHog
- git-secrets
- detect-secrets
- GitHub Secret Scanning

**Pipeline integration:**
```yaml
secret_scan:
  stage: security
  script:
    - trufflehog filesystem . --json
  allow_failure: false
```

**5. Container Image Scanning**

**What it is:** Scans container images for vulnerabilities in base images, installed packages, and application code.

**When to run:**
- After building images
- Before pushing to registry
- Periodic rescans of registry images

**What it catches:**
- Vulnerabilities in base images
- Outdated OS packages
- Known CVEs in image layers
- Misconfigurations
- Exposed secrets in images

**Popular tools:**
- Trivy
- Snyk Container
- Aqua Security
- Clair
- Docker Scan

**Pipeline integration:**
```yaml
container_scan:
  stage: security
  script:
    - docker build -t myapp:latest .
    - trivy image --severity HIGH,CRITICAL myapp:latest
  allow_failure: false
```

**6. Infrastructure as Code (IaC) Scanning**

**What it is:** Scans infrastructure configuration (Terraform, CloudFormation, Kubernetes manifests) for security misconfigurations.

**When to run:**
- On IaC file changes
- Before applying infrastructure changes
- Pull request validation

**What it catches:**
- Open security groups
- Unencrypted storage
- Overly permissive IAM policies
- Missing logging/monitoring
- Non-compliant configurations

**Popular tools:**
- Checkov
- tfsec
- Terrascan
- Bridgecrew
- Snyk IaC

**Pipeline integration:**
```yaml
iac_scan:
  stage: security
  script:
    - checkov -d terraform/ --framework terraform
  allow_failure: false
```

### Security Gate Strategy

**Pre-Commit Gates:**
- Secret detection hooks
- Linting and formatting
- Fast local security checks

**Pull Request Gates:**
- SAST scanning
- Dependency scanning (SCA)
- Code review (including security review)
- Unit and integration tests

**Main Branch Gates:**
- DAST scanning (staging environment)
- Container image scanning
- IaC security scanning
- Comprehensive integration tests
- Performance and load tests

**Pre-Production Gates:**
- Final security validation
- Compliance checks
- Manual security review (for high-risk changes)
- Deployment smoke tests

**Post-Deployment:**
- Production smoke tests
- Runtime security monitoring
- Anomaly detection
- Continuous vulnerability scanning

### Managing False Positives

**Tune scanners:**
- Configure tools for your tech stack
- Adjust severity thresholds
- Exclude test code from some scans

**Triage and track:**
- Review and categorize findings
- Document false positives
- Track technical debt for accepted risks

**Continuous improvement:**
- Regularly review scanner configuration
- Update rules and policies
- Share knowledge across teams

---

## Secrets and Credential Management

### What Are Secrets?

**Secrets** are sensitive pieces of information that grant access to systems, services, or data:
- API keys and tokens
- Database passwords
- Private keys and certificates
- OAuth client secrets
- Encryption keys
- Service account credentials

### The Secrets Problem

**Why secrets are challenging in CI/CD:**
- Need to be available to pipelines but not exposed in code
- Different secrets for different environments
- Must be rotated regularly
- Need to be auditable
- Can't be committed to version control

### Secrets Management Best Practices

**1. Never Commit Secrets to Version Control**
- Use `.gitignore` to exclude config files with secrets
- Use environment variables or secret management tools
- Run secret detection tools to catch accidents
- Rotate immediately if a secret is exposed

**2. Use Dedicated Secrets Management Tools**

**Cloud Provider Solutions:**
- AWS Secrets Manager
- Azure Key Vault
- Google Cloud Secret Manager
- Alibaba Cloud KMS

**Third-Party Solutions:**
- HashiCorp Vault
- 1Password Secrets Automation
- CyberArk Conjur
- Doppler

**CI/CD Platform Built-In:**
- GitHub Secrets
- GitLab CI/CD Variables
- CircleCI Contexts
- Jenkins Credentials

**3. Rotate Secrets Regularly**
- Automate rotation where possible
- Have a rotation schedule for all secrets
- Rotate immediately if exposure suspected
- Test rotation process regularly

**4. Use Short-Lived Credentials**
- Prefer temporary tokens over long-lived credentials
- Use IAM roles and service accounts where possible
- Implement just-in-time access
- Token TTL < 24 hours when possible

**5. Apply Least Privilege**
- Grant minimum necessary permissions
- Use separate credentials for different environments
- Regularly audit and revoke unused credentials
- Scope secrets to specific pipelines or stages

**6. Encrypt Secrets at Rest and in Transit**
- Use TLS for all network communication
- Encrypt secrets in configuration files
- Use encrypted storage for secrets
- Never log secrets in build output

### Secrets in CI/CD Pipelines

**Using CI/CD Platform Secrets:**

GitHub Actions:
```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
        run: ./deploy.sh
```

GitLab CI/CD:
```yaml
deploy:
  script:
    - ./deploy.sh
  variables:
    API_KEY: $CI_API_KEY
    DB_PASSWORD: $DB_PASSWORD
```

**Using External Secrets Manager:**

Vault example:
```yaml
deploy:
  script:
    - export VAULT_TOKEN=$(vault login -token-only)
    - vault kv get -field=password secret/db > db_password.txt
    - ./deploy.sh
  variables:
    VAULT_ADDR: "https://vault.example.com"
```

**Injecting Secrets at Runtime:**
- Fetch secrets at deployment time, not build time
- Use environment variables
- Mount secrets as files in containers
- Use cloud provider instance roles when possible

**Example: Kubernetes Secrets:**
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-credentials
          key: password
```

### Secrets in Different Environments

**Development:**
- Use local environment variables or `.env` files (not committed)
- Use mock credentials where possible
- Limited access to production secrets
- Developers should never need production secrets locally

**CI/CD:**
- Use CI/CD platform secret management
- Inject secrets as environment variables at runtime
- Never log secrets in build output
- Mask secrets in logs automatically

**Staging:**
- Use separate secrets from production
- Rotate regularly
- Similar access controls to production
- Can be less restrictive for debugging

**Production:**
- Use cloud provider secret management services
- Inject secrets at runtime, not build time
- Strict access controls
- Monitor and audit secret access
- Automatic rotation where possible

### Secret Rotation Strategy

**Automated Rotation:**
- Cloud provider native rotation (AWS Secrets Manager, etc.)
- Custom scripts for unsupported services
- Schedule rotation (30-90 days)
- Test rotation process in staging first

**Manual Rotation:**
- Document rotation procedure
- Rotate on schedule
- Rotate on team member departure
- Rotate after suspected exposure

**Zero-Downtime Rotation:**
- Support multiple active secrets during rotation
- Gradual rollout of new secrets
- Verify new secret works before revoking old

---

## Pipeline Hardening

### Securing the Pipeline Infrastructure

**1. Keep CI/CD Tools Updated**
- Regular security patches
- Monitor CVE feeds for CI/CD tools
- Test updates in non-production first
- Automate update notifications

**2. Access Control**
- Use multi-factor authentication (MFA)
- Role-based access control (RBAC)
- Principle of least privilege
- Regular access audits
- Remove access for departed team members

**3. Audit Logging**
- Log all pipeline activities
- Log authentication and authorization events
- Log configuration changes
- Centralized log collection
- Retain logs per compliance requirements
- Alert on suspicious activities

**4. Harden Build Agents/Runners**
- Use minimal base images
- Regularly patch and update
- Isolate runners (containers, VMs)
- No persistent state between builds
- Network segmentation
- Monitor for anomalies

**5. Restrict Pipeline Modifications**
- Require code review for pipeline changes
- Separate pipeline configuration from application code (when appropriate)
- Use signed commits
- Protected branches for pipeline config
- Audit trail for all changes

### Preventing Pipeline Manipulation

**1. Validate Inputs**
- Sanitize all external inputs to pipelines
- Validate webhooks and triggers
- Check parameter values
- Prevent command injection

**2. Use Pipeline as Code**
- Version control pipeline definitions
- Code review for pipeline changes
- Automated validation of pipeline config
- Treat pipelines like application code

**3. Least Privilege for Pipelines**
- Minimal permissions for service accounts
- Scope permissions to specific resources
- Different credentials for different stages
- No admin credentials in pipelines

**4. Isolated Execution**
- Run builds in isolated containers/VMs
- No network access unless required
- Clean workspace between builds
- Prevent cross-contamination between builds

**5. Dependency Pinning**
- Pin versions of build tools
- Pin versions of CI/CD plugins/actions
- Use checksums to verify integrity
- Review updates before adopting

### Pipeline Security Checklist

**Authentication & Authorization:**
- [ ] MFA enabled for all users
- [ ] RBAC configured with least privilege
- [ ] Service accounts use minimal permissions
- [ ] Regular access reviews conducted

**Secrets Management:**
- [ ] No secrets in code or pipeline definitions
- [ ] Secrets stored in dedicated secrets manager
- [ ] Secrets rotated regularly
- [ ] Secrets masked in logs

**Build Security:**
- [ ] Build agents/runners hardened
- [ ] Isolated build environments
- [ ] Dependency versions pinned
- [ ] Build artifacts signed

**Monitoring & Auditing:**
- [ ] All pipeline activities logged
- [ ] Centralized log collection
- [ ] Alerting on suspicious activities
- [ ] Regular security audits

**Compliance:**
- [ ] Pipeline meets regulatory requirements
- [ ] Audit trails maintained
- [ ] Access controls documented
- [ ] Incident response plan in place

---

## Continuous Compliance

### Policy as Code

**What it is:** Defining security and compliance policies as code that can be automatically enforced, versioned, and tested.

**Benefits:**
- Automated compliance checking
- Consistent policy enforcement
- Audit trails through version control
- Faster policy updates
- Self-service compliance validation
- Documentation as code

**Tools:**
- Open Policy Agent (OPA)
- HashiCorp Sentinel
- Cloud Custodian
- Chef InSpec
- AWS Config Rules

**What to codify:**
- Infrastructure security policies
- Access control policies
- Data retention policies
- Encryption requirements
- Network security rules
- Deployment approval requirements

**Example OPA Policy:**
```rego
package deployment.approval

# Require security team approval for production deployments
deny[msg] {
    input.environment == "production"
    not has_security_approval(input)
    msg := "Production deployments require security team approval"
}

has_security_approval(deployment) {
    some i
    deployment.approvals[i].team == "security"
}
```

### Automated Compliance Checking

**In CI/CD Pipeline:**
- Validate infrastructure changes against policies
- Block non-compliant deployments
- Generate compliance reports automatically
- Fail builds on policy violations

**Example GitLab CI:**
```yaml
compliance_check:
  stage: validate
  script:
    - opa test policies/
    - conftest test -p policies/ kubernetes/*.yaml
  allow_failure: false
```

**Continuous Monitoring:**
- Real-time security posture assessment
- Drift detection from compliance baselines
- Automated remediation of violations
- Alerting on policy violations

**Tools for Continuous Compliance:**
- AWS Config
- Azure Policy
- Google Cloud Security Command Center
- Prisma Cloud
- Lacework

### Audit Trails and Documentation

**What to Log:**
- All code changes (git history)
- Pipeline executions and results
- Security scan findings
- Deployment activities
- Configuration changes
- Access and authentication events
- Approval and sign-off records

**Log Retention:**
- Follow regulatory requirements (GDPR, HIPAA, SOC 2, etc.)
- Typically 1-7 years depending on compliance framework
- Immutable logs (prevent tampering)
- Encrypted at rest and in transit

**Compliance Documentation:**
- Security architecture decisions
- Threat models
- Security controls implementation
- Vulnerability assessment results
- Incident response activities
- Policy documents
- Audit reports

**Automated Evidence Collection:**
- Screenshots of deployments
- Test result artifacts
- Security scan reports
- Deployment logs
- Change approval records

---

## CI/CD Platforms and Tools

### Major CI/CD Platforms

**GitHub Actions**

**What it is:** GitHub's native CI/CD platform integrated directly into GitHub repositories.

**Key features:**
- Deep GitHub integration
- Marketplace with thousands of pre-built actions
- Matrix builds for testing multiple configurations
- Self-hosted runners
- Built-in secrets management

**Best for:** Projects already on GitHub, open source projects, teams wanting GitHub ecosystem integration

**Example workflow:**
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
```

**Resources:**
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

**GitLab CI/CD**

**What it is:** GitLab's built-in CI/CD system integrated with GitLab repositories.

**Key features:**
- Integrated with GitLab ecosystem
- Auto DevOps for automatic pipeline creation
- Built-in container registry
- Review apps for feature branches
- Kubernetes integration

**Best for:** Teams using GitLab, organizations wanting all-in-one DevOps platform

**Example pipeline:**
```yaml
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - npm install
    - npm run build

test:
  stage: test
  script:
    - npm test

deploy:
  stage: deploy
  script:
    - ./deploy.sh
  only:
    - main
```

**Resources:**
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)

**Jenkins**

**What it is:** Open-source automation server, one of the oldest and most widely used CI/CD tools.

**Key features:**
- Highly extensible (1800+ plugins)
- Self-hosted (full control)
- Pipeline as code (Jenkinsfile)
- Distributed builds
- Strong community

**Best for:** Organizations needing full control, complex custom workflows, legacy systems integration

**Example Jenkinsfile:**
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'npm install'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

**Resources:**
- [Jenkins Documentation](https://www.jenkins.io/doc/)

**CircleCI**

**What it is:** Cloud-based CI/CD platform with strong Docker support.

**Key features:**
- Fast builds with intelligent caching
- Docker-first approach
- SSH debugging
- Orbs (reusable configuration packages)
- Generous free tier

**Best for:** Teams wanting fast, reliable cloud CI/CD with Docker support

**Example config:**
```yaml
version: 2.1
jobs:
  build:
    docker:
      - image: circleci/node:18
    steps:
      - checkout
      - run: npm install
      - run: npm test
workflows:
  build-and-test:
    jobs:
      - build
```

**Resources:**
- [CircleCI Documentation](https://circleci.com/docs/)

**Azure DevOps**

**What it is:** Microsoft's comprehensive DevOps platform (formerly VSTS).

**Key features:**
- Integrated with Azure ecosystem
- Azure Repos, Boards, Artifacts
- Strong Windows/.NET support
- Hybrid cloud support
- Enterprise features

**Best for:** Microsoft shops, Azure users, enterprises needing comprehensive DevOps suite

**Example pipeline:**
```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '18.x'
  - script: npm install
  - script: npm test
```

**Resources:**
- [Azure DevOps Documentation](https://learn.microsoft.com/en-us/azure/devops/)

**AWS CodePipeline**

**What it is:** AWS's native CI/CD service integrated with AWS services.

**Key features:**
- Deep AWS integration
- Integrates with CodeBuild, CodeDeploy
- Managed service (no infrastructure)
- Pay-per-use pricing
- Visual pipeline editor

**Best for:** Teams heavily invested in AWS, serverless applications

**Resources:**
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)

### Specialized CI/CD Tools

**For Containers:**
- Docker Hub Automated Builds
- Google Cloud Build
- Red Hat OpenShift Pipelines

**For Kubernetes:**
- Argo CD
- Flux CD
- Tekton

**For Serverless:**
- Serverless Framework CI/CD
- AWS SAM CLI
- Vercel
- Netlify

### Choosing a CI/CD Platform

**Considerations:**

| Factor | Questions to Ask |
|--------|------------------|
| Hosting | Cloud-hosted or self-hosted? |
| Integration | Does it integrate with your VCS (GitHub, GitLab, Bitbucket)? |
| Scale | Can it handle your build volume? |
| Cost | Pricing model (per-minute, per-user, flat fee)? |
| Ecosystem | Does it support your tech stack? |
| Security | Does it meet your security and compliance requirements? |
| Team Skills | How steep is the learning curve? |
| Support | What level of support is available? |

**Decision matrix:**
- **Small team, GitHub-based:** GitHub Actions
- **GitLab users:** GitLab CI/CD
- **Enterprise, need control:** Jenkins
- **Fast Docker builds:** CircleCI
- **Microsoft stack:** Azure DevOps
- **AWS-centric:** AWS CodePipeline
- **Multi-cloud, complex:** Jenkins or self-hosted GitLab

---

## Resources

### Documentation and Standards
- [Continuous Delivery Book](https://continuousdelivery.com/) by Jez Humble and David Farley
- [The Phoenix Project](https://itrevolution.com/product/the-phoenix-project/) - DevOps novel
- [Accelerate](https://itrevolution.com/product/accelerate/) - Research-based DevOps metrics

### CI/CD Platforms
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitLab CI/CD](https://docs.gitlab.com/ee/ci/)
- [Jenkins](https://www.jenkins.io/doc/)
- [CircleCI](https://circleci.com/docs/)
- [Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/)

### Security Tools
- [OWASP ZAP](https://www.zaproxy.org/) - Free DAST scanner
- [Snyk](https://snyk.io/) - Developer security platform
- [SonarQube](https://www.sonarqube.org/) - Code quality and security
- [Trivy](https://trivy.dev/) - Container vulnerability scanner

### Secrets Management
- [HashiCorp Vault](https://www.vaultproject.io/)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault/)
- [Google Secret Manager](https://cloud.google.com/secret-manager)

### Compliance and Policy
- [Open Policy Agent](https://www.openpolicyagent.org/)
- [Conftest](https://www.conftest.dev/) - Test structured configuration
- [Cloud Custodian](https://cloudcustodian.io/) - Cloud resource management

### Testing Tools
- [Selenium](https://www.selenium.dev/) - Browser automation
- [JMeter](https://jmeter.apache.org/) - Performance testing
- [k6](https://k6.io/) - Modern load testing
- [Pact](https://pact.io/) - Contract testing
