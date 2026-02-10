# Azure Study Guides Plan

## Purpose and Intent

Create a comprehensive set of Azure study guides mirroring the depth and structure of the existing AWS guides (50 guides across 16 subcategories). These guides target **software developers and system architects** who need practical, job-relevant Azure knowledge. The guides follow the same conceptual format as the AWS guides: explaining what services are, what problems they solve, when to use them, architecture patterns, decision frameworks, and practical considerations.

All guides use `layout: guide`, `category: Azure`, and follow the study guide content philosophy in CLAUDE.md: conceptual over code syntax, explain before prescribing, inline links, and actionable knowledge over reference material.

## File Location

All Azure guides live in: `_guides/infrastructure/azure/`

Each guide must also be registered in `assets/data/study_guides_config.json` under a new "Azure" category.

## Status Legend

- [ ] Not started
- [~] In progress
- [x] Completed

---

## Subcategory 1: Architecture Principles (1 guide)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 1 | `azure-well-architected-framework.md` | Azure Well-Architected Framework | WAF pillars, Azure Advisor, WAF Assessment | [x] |

**Notes**: Covers the five pillars (Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency) plus the newer Sustainability considerations. Maps to AWS WAF guide.

---

## Subcategory 2: Subscription & Resource Organization (3 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 2 | `azure-subscription-architecture.md` | Azure Subscription & Tenant Architecture | Entra ID tenants, Management Groups, Subscriptions, Resource Groups, subscription design patterns (single vs multi-subscription, workload isolation, environment separation) | [x] |
| 3 | `azure-resource-organization.md` | Azure Resource Organization & Tagging | Resource Group strategies, naming conventions, tagging policies, resource locks, move operations, cross-subscription resource access | [x] |
| 4 | `azure-billing-enrollment.md` | Azure Billing & Enterprise Enrollment | Enterprise Agreement vs CSP vs PAYG vs MCA, billing accounts, billing profiles, invoice sections, cost allocation, spending limits, subscription quotas | [x] |

**Notes**: This subcategory has no AWS equivalent because Azure's organizational hierarchy is fundamentally different and much more layered. AWS uses a flat account model with Organizations layered on top; Azure's hierarchy (Tenant → Management Groups → Subscriptions → Resource Groups → Resources) is baked into the platform from the start. Every architect needs to understand this before provisioning anything.

Key topics that make this Azure-specific:
- **Tenant architecture**: Single vs multi-tenant Entra ID, B2B guest access across tenants
- **Subscription design**: Subscriptions as billing boundaries AND security/policy boundaries; how to split workloads across subscriptions
- **Resource Group patterns**: Lifecycle-based vs team-based vs environment-based grouping; the fact that resource groups are a deployment scope (not just a folder)
- **Billing models**: EA enrollment hierarchies (departments, accounts, subscriptions), CSP partner relationships, MCA billing profiles and invoice sections
- **Cross-subscription concerns**: VNet peering across subscriptions, shared services subscriptions, Azure Lighthouse for cross-tenant management

---

## Subcategory 3: Identity & Access Management (2 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 5 | `azure-entra-id.md` | Azure Entra ID (Azure AD) for System Architects | Entra ID, Conditional Access, MFA, B2B/B2C, App Registrations | [x] |
| 6 | `azure-rbac-managed-identities.md` | Azure RBAC & Managed Identities | RBAC, Built-in/Custom Roles, Managed Identities, Service Principals | [x] |

**Notes**: Azure identity is significantly richer than AWS IAM. Entra ID (formerly Azure AD) is a full identity platform, not just cloud resource access control. Splitting into two guides: one for the identity platform itself, one for Azure-specific authorization and workload identity. AWS has only 1 guide here.

---

## Subcategory 4: Networking & Content Delivery (7 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 7 | `azure-vnet-architecture.md` | Azure VNet: Network Architecture | VNets, Subnets, NSGs, ASGs, Route Tables, NAT Gateway | [x] |
| 8 | `azure-dns-traffic-manager.md` | Azure DNS & Traffic Manager | Azure DNS, Traffic Manager, DNS Zones | [x] |
| 9 | `azure-front-door-cdn.md` | Azure Front Door & CDN | Front Door, Azure CDN, WAF integration | [x] |
| 10 | `azure-load-balancer-app-gateway.md` | Azure Load Balancer & Application Gateway | Load Balancer (L4), Application Gateway (L7), WAF v2 | [x] |
| 11 | `azure-api-management.md` | Azure API Management | APIM tiers, policies, developer portal, versioning | [x] |
| 12 | `azure-expressroute-vpn.md` | Azure ExpressRoute & VPN Gateway | ExpressRoute, VPN Gateway, S2S/P2S VPN | [x] |
| 13 | `azure-private-link-virtual-wan.md` | Azure Private Link & Virtual WAN | Private Link, Private Endpoints, Virtual WAN, VNet Peering | [x] |

**Notes**: Direct parallel to AWS networking guides. Azure networking has strong equivalents for every AWS networking service. Traffic Manager is Azure's DNS-based global load balancer (Route 53 routing policies equivalent).

---

## Subcategory 5: Compute Services (4 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 14 | `azure-virtual-machines.md` | Azure Virtual Machines for System Architects | VMs, VM Scale Sets, Availability Sets/Zones, Spot VMs | [x] |
| 15 | `azure-functions.md` | Azure Functions for System Architects | Functions, Triggers/Bindings, Durable Functions, Consumption vs Premium | [x] |
| 16 | `azure-container-services.md` | Azure Container Services: ACI, AKS, and Container Apps | ACI, AKS, Container Apps, comparison/selection | [x] |
| 17 | `azure-app-service.md` | Azure App Service for System Architects | App Service, App Service Plans, Deployment Slots, WebJobs | [x] |

**Notes**: Azure has 4 compute guides vs AWS's 3 because App Service (PaaS web hosting) is a major Azure differentiator with no direct AWS equivalent at the same level of integration. Container Apps is also a significant addition beyond what AKS covers.

---

## Subcategory 6: Storage Services (2 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 18 | `azure-blob-storage.md` | Azure Blob Storage for System Architects | Blob Storage, tiers (Hot/Cool/Cold/Archive), lifecycle, immutability | [x] |
| 19 | `azure-managed-disks-files.md` | Azure Managed Disks & Azure Files | Managed Disks (Ultra/Premium/Standard), Azure Files, Azure NetApp Files | [x] |

**Notes**: Direct parallel to AWS S3 and EBS/EFS guides.

---

## Subcategory 7: Database Services (5 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 20 | `azure-sql-database.md` | Azure SQL Database & Managed Instance | SQL Database, SQL Managed Instance, Elastic Pools, Hyperscale | [x] |
| 21 | `azure-cosmos-db.md` | Azure Cosmos DB for System Architects | Cosmos DB, consistency models, partitioning, multi-model APIs | [x] |
| 22 | `azure-cache-redis.md` | Azure Cache for Redis | Tiers, clustering, geo-replication, data persistence | [x] |
| 23 | `azure-synapse-analytics.md` | Azure Synapse Analytics for System Architects | Dedicated/Serverless SQL pools, Spark pools, Data Explorer pools | [x] |
| 24 | `azure-database-selection.md` | Azure Database Service Selection | Decision framework across all Azure database services | [x] |

**Notes**: Azure SQL is more tightly integrated than AWS RDS because it's Microsoft's own database. Cosmos DB is a major differentiator with its multi-model, globally distributed design and five consistency levels. Synapse replaces the separate data warehouse concept.

---

## Subcategory 8: Infrastructure as Code (3 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 25 | `azure-bicep-fundamentals.md` | Azure Bicep: Fundamentals | Bicep language, modules, parameters, resource declarations | [x] |
| 26 | `azure-bicep-advanced.md` | Azure Bicep: Advanced Patterns | Modules, conditional deployments, loops, template specs | [x] |
| 27 | `azure-arm-templates.md` | ARM Templates & Deployment Patterns | ARM JSON templates, deployment modes, nested/linked templates | [x] |

**Notes**: Bicep is Azure's first-party IaC language (transpiles to ARM). It deserves two guides because it's the recommended approach. ARM templates get one guide for legacy/context. The generic IaC guides (Terraform, etc.) already exist in the parent infrastructure category. AWS has 4 CloudFormation guides; Azure has 3 because Bicep is simpler than CloudFormation.

---

## Subcategory 9: Application Integration & Messaging (4 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 28 | `azure-service-bus.md` | Azure Service Bus for System Architects | Queues, Topics/Subscriptions, Sessions, dead-lettering | [x] |
| 29 | `azure-event-grid.md` | Azure Event Grid for System Architects | Event Grid, topics, event schemas, filtering, CloudEvents | [x] |
| 30 | `azure-logic-apps.md` | Azure Logic Apps & Durable Functions | Logic Apps, workflow orchestration, Durable Functions patterns | [x] |
| 31 | `azure-event-hubs.md` | Azure Event Hubs for System Architects | Event Hubs, partitions, consumer groups, Kafka compatibility | [x] |

**Notes**: Service Bus ≈ SQS+SNS, Event Grid ≈ EventBridge, Logic Apps ≈ Step Functions (but broader), Event Hubs ≈ Kinesis.

---

## Subcategory 10: Security & Compliance (5 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 32 | `azure-defender-sentinel.md` | Microsoft Defender for Cloud & Sentinel | Defender for Cloud, Microsoft Sentinel, security posture | [ ] |
| 33 | `azure-monitor-diagnostic-settings.md` | Azure Activity Log & Diagnostic Settings | Activity Log, Diagnostic Settings, Azure Policy auditing | [ ] |
| 34 | `azure-firewall-ddos.md` | Azure Firewall & DDoS Protection | Azure Firewall, DDoS Protection, Firewall Manager | [ ] |
| 35 | `azure-key-vault.md` | Azure Key Vault for System Architects | Keys, Secrets, Certificates, HSM, access policies vs RBAC | [ ] |
| 36 | `azure-policy-governance.md` | Azure Policy & Governance | Azure Policy, Blueprints, Landing Zones, compliance dashboards | [ ] |

**Notes**: Direct parallel to AWS security guides. Azure Policy is significantly more powerful than AWS Config rules for governance. Landing Zones concept is Azure's equivalent of Control Tower.

---

## Subcategory 11: Management & Governance (4 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 37 | `azure-monitor.md` | Azure Monitor for System Architects | Metrics, Logs, Alerts, Workbooks, Log Analytics workspace | [ ] |
| 38 | `azure-application-insights.md` | Azure Application Insights | APM, distributed tracing, availability tests, smart detection | [ ] |
| 39 | `azure-automation-arc.md` | Azure Automation & Azure Arc | Automation runbooks, Update Management, Arc for hybrid | [ ] |
| 40 | `azure-cost-management.md` | Azure Cost Management & Optimization | Cost Management, Budgets, Reservations, Azure Advisor cost | [ ] |

**Notes**: Application Insights is Azure's APM and distributed tracing (combines aspects of X-Ray and CloudWatch Application Insights). Azure Arc extends Azure management to on-prem/multi-cloud resources.

---

## Subcategory 12: Developer Tools & CI/CD (3 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 41 | `azure-devops-pipelines.md` | Azure DevOps Pipelines for System Architects | YAML pipelines, stages, environments, approvals, agents | [ ] |
| 42 | `azure-devops-repos-artifacts.md` | Azure DevOps Repos & Artifacts | Azure Repos (Git), Artifacts (NuGet/npm/Maven feeds), Boards integration | [ ] |
| 43 | `github-actions-azure.md` | GitHub Actions for Azure Deployments | GitHub Actions, OIDC auth, Azure deployment workflows | [ ] |

**Notes**: Azure DevOps is a comprehensive ALM platform. GitHub Actions is increasingly the preferred CI/CD for Azure deployments (Microsoft owns GitHub). Both deserve coverage. Maps to AWS CodePipeline/CodeBuild/CodeDeploy/CDK guides.

---

## Subcategory 13: Analytics & Data Processing (4 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 44 | `azure-data-factory.md` | Azure Data Factory: ETL & Data Integration | Pipelines, data flows, linked services, integration runtimes | [ ] |
| 45 | `azure-synapse-analytics-query.md` | Azure Synapse: Serverless & Dedicated Query | Serverless SQL pools, on-demand querying, external tables | [ ] |
| 46 | `azure-power-bi.md` | Power BI for System Architects | Power BI Service, datasets, dataflows, embedded analytics | [ ] |
| 47 | `azure-data-architecture.md` | Modern Data Architecture on Azure | Lakehouse, medallion architecture, data mesh on Azure | [ ] |

**Notes**: Data Factory ≈ Glue, Synapse serverless ≈ Athena, Power BI ≈ QuickSight (but far more dominant in the market). Azure data architecture guide covers the same territory as the AWS data architecture guide.

**Important**: Guide #42 focuses on the query/analytics side of Synapse (Athena equivalent), while guide #20 in the Database section covers Synapse as a data warehouse platform (Redshift equivalent). Minimal overlap: #20 covers provisioned pools, capacity, and Synapse as a database; #42 covers serverless querying, external tables, and on-demand analytics.

---

## Subcategory 14: Machine Learning & AI (5 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 48 | `azure-machine-learning.md` | Azure Machine Learning: ML Platform Essentials | Workspaces, compute, pipelines, MLflow integration, endpoints | [ ] |
| 49 | `azure-ai-vision.md` | Azure AI Vision Services | Computer Vision, Custom Vision, Face API, Document Intelligence | [ ] |
| 50 | `azure-ai-language.md` | Azure AI Language Services | Language Understanding, Text Analytics, Translator, QnA Maker | [ ] |
| 51 | `azure-ai-speech.md` | Azure AI Speech Services | Speech-to-Text, Text-to-Speech, Speech Translation | [ ] |
| 52 | `azure-ai-service-selection.md` | Azure AI & ML Service Selection | Decision framework across all Azure AI/ML services | [ ] |

**Notes**: Direct parallel to AWS ML/AI guides. Azure AI Services (formerly Cognitive Services) map to AWS Rekognition/Textract/Comprehend/Translate/Transcribe/Polly. Azure OpenAI Service should also be covered in the selection guide as it's a major differentiator.

---

## Subcategory 15: Migration & Hybrid Cloud (3 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 53 | `azure-migration-strategy.md` | Azure Migration Strategy | Cloud Adoption Framework, migration phases, assessment | [ ] |
| 54 | `azure-migrate-services.md` | Azure Migrate & Database Migration Service | Azure Migrate, DMS, App Service Migration Assistant | [ ] |
| 55 | `azure-hybrid-cloud-architecture.md` | Azure Hybrid Cloud Architecture | Azure Arc, Azure Stack HCI, hybrid patterns | [ ] |

**Notes**: Azure has strong hybrid story through Azure Arc and Azure Stack. Cloud Adoption Framework is Microsoft's comprehensive migration methodology. Maps directly to AWS migration guides.

---

## Subcategory 16: Serverless Architecture (2 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 56 | `serverless-architecture-patterns-azure.md` | Serverless Architecture Patterns on Azure | Functions, Logic Apps, Event Grid, API Management, Cosmos DB serverless | [ ] |
| 57 | `azure-functions-advanced.md` | Azure Functions: Advanced Patterns | Durable Functions, custom handlers, deployment models, scaling | [ ] |

**Notes**: Durable Functions (stateful orchestration within Functions) is a significant Azure differentiator. Maps to AWS serverless patterns + SAM guides.

---

## Subcategory 17: Container Orchestration (Advanced) (2 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 58 | `azure-acr-container-security.md` | Azure Container Registry & Container Security | ACR, image scanning, content trust, Defender for Containers | [ ] |
| 59 | `advanced-container-patterns-azure.md` | Advanced Container Patterns on Azure | AKS advanced networking, service mesh, KEDA, GitOps | [ ] |

**Notes**: Direct parallel to AWS container orchestration guides.

---

## Subcategory 18: Architecture Patterns (Advanced) (2 guides)

| # | File Name | Title | Azure Services Covered | Status |
|---|-----------|-------|----------------------|--------|
| 60 | `multi-region-architecture-azure.md` | Multi-Region Architecture on Azure | Paired regions, Azure Front Door, Cosmos DB multi-region, Traffic Manager | [ ] |
| 61 | `disaster-recovery-azure.md` | Disaster Recovery on Azure | Azure Site Recovery, geo-redundant storage, DR patterns | [ ] |

**Notes**: Direct parallel to AWS architecture patterns guides. Azure's paired regions concept and Azure Site Recovery are unique aspects.

---

## Total Guide Count: 61

| Subcategory | Guide Count |
|-------------|-------------|
| Architecture Principles | 1 |
| Subscription & Resource Organization | 3 |
| Identity & Access Management | 2 |
| Networking & Content Delivery | 7 |
| Compute Services | 4 |
| Storage Services | 2 |
| Database Services | 5 |
| Infrastructure as Code | 3 |
| Application Integration & Messaging | 4 |
| Security & Compliance | 5 |
| Management & Governance | 4 |
| Developer Tools & CI/CD | 3 |
| Analytics & Data Processing | 4 |
| Machine Learning & AI | 5 |
| Migration & Hybrid Cloud | 3 |
| Serverless Architecture | 2 |
| Container Orchestration (Advanced) | 2 |
| Architecture Patterns (Advanced) | 2 |
| **Total** | **61** |

---

## Recommended Creation Order

Build guides in dependency order so earlier guides can be referenced by later ones.

### Phase 1: Foundations (Guides 1-6)
These establish the architectural principles, organizational structure, and identity model that everything else depends on. Subscription and resource organization comes first because every Azure resource lives within this hierarchy.
1. Azure Well-Architected Framework
2. Azure Subscription & Tenant Architecture
3. Azure Resource Organization & Tagging
4. Azure Billing & Enterprise Enrollment
5. Azure Entra ID
6. Azure RBAC & Managed Identities

### Phase 2: Core Infrastructure (Guides 7-13)
Networking is foundational to every other service.
7. Azure VNet Architecture
8. Azure DNS & Traffic Manager
9. Azure Front Door & CDN
10. Azure Load Balancer & Application Gateway
11. Azure API Management
12. Azure ExpressRoute & VPN Gateway
13. Azure Private Link & Virtual WAN

### Phase 3: Compute & Storage (Guides 14-19)
The workhorses that everything runs on.
14. Azure Virtual Machines
15. Azure Functions
16. Azure Container Services
17. Azure App Service
18. Azure Blob Storage
19. Azure Managed Disks & Azure Files

### Phase 4: Data Layer (Guides 20-24)
Database services that applications depend on.
20. Azure SQL Database & Managed Instance
21. Azure Cosmos DB
22. Azure Cache for Redis
23. Azure Synapse Analytics
24. Azure Database Service Selection

### Phase 5: Integration & Messaging (Guides 28-31)
How services communicate.
28. Azure Service Bus
29. Azure Event Grid
30. Azure Logic Apps & Durable Functions
31. Azure Event Hubs

### Phase 6: Infrastructure as Code (Guides 25-27)
How to deploy and manage everything from Phases 1-5.
25. Azure Bicep Fundamentals
26. Azure Bicep Advanced
27. ARM Templates & Deployment Patterns

### Phase 7: Security & Compliance (Guides 32-36)
Securing and governing the infrastructure.
32. Microsoft Defender for Cloud & Sentinel
33. Azure Activity Log & Diagnostic Settings
34. Azure Firewall & DDoS Protection
35. Azure Key Vault
36. Azure Policy & Governance

### Phase 8: Operations & Observability (Guides 37-40)
Monitoring, managing, and optimizing.
37. Azure Monitor
38. Azure Application Insights
39. Azure Automation & Azure Arc
40. Azure Cost Management & Optimization

### Phase 9: Developer Tools & CI/CD (Guides 41-43)
Build and deployment pipelines.
41. Azure DevOps Pipelines
42. Azure DevOps Repos & Artifacts
43. GitHub Actions for Azure Deployments

### Phase 10: Analytics & Data (Guides 44-47)
Data processing, querying, and visualization.
44. Azure Data Factory
45. Azure Synapse Serverless Query
46. Power BI for System Architects
47. Modern Data Architecture on Azure

### Phase 11: AI & Machine Learning (Guides 48-52)
AI/ML services and selection.
48. Azure Machine Learning
49. Azure AI Vision Services
50. Azure AI Language Services
51. Azure AI Speech Services
52. Azure AI & ML Service Selection

### Phase 12: Advanced Patterns (Guides 53-61)
Migration, hybrid, serverless, containers, and architecture patterns.
53. Azure Migration Strategy
54. Azure Migrate & Database Migration Service
55. Azure Hybrid Cloud Architecture
56. Serverless Architecture Patterns on Azure
57. Azure Functions Advanced Patterns
58. Azure Container Registry & Container Security
59. Advanced Container Patterns on Azure
60. Multi-Region Architecture on Azure
61. Disaster Recovery on Azure

---

## Configuration Updates Required

When guides are created, `assets/data/study_guides_config.json` needs a new "Azure" top-level category with all 17 subcategories and their guides registered. This should be done incrementally as each phase is completed.

## Format and Style Reference

Each guide should follow the format established by the AWS guides:
- **Front matter**: layout, title, category (Azure), subcategory, description, tags
- **Opening section**: "What is [Service]" with a blockquote pull-quote
- **Problem framing**: "What Problems [Service] Solves" with before/after comparison
- **How it works**: Core concepts and components
- **Architecture patterns**: Common deployment patterns and best practices
- **Decision frameworks**: When to use what (comparison tables where applicable)
- **Cost considerations**: Pricing model and relative cost positioning (see Content Scope below)
- **Integration points**: How the service connects to other Azure services
- **AWS comparison table**: Side-by-side with the equivalent AWS service(s)
- **Common pitfalls**: Practical mistakes and how to avoid them
- **Key takeaways**: Actionable insights (not a summary of what was already said)

Tags should use the established vocabulary with `azure` replacing `aws` and adding Azure-specific service tags.

## Content Scope Guidelines

### Pricing: Relative Positioning, Not Dollar Amounts

Azure pricing changes frequently. Specific dollar amounts go stale and create a maintenance burden. Guides should convey pricing insights that remain useful over time:

**Do include:**
- Pricing model type (pay-per-request, fixed monthly, hourly + data processed, per-unit)
- Relative cost comparisons between tiers ("Standard v2 is roughly one-quarter the cost of classic Premium")
- Relative cost comparisons between services ("Application Gateway is 5-7x more expensive than Load Balancer")
- Cost structure differences that affect architecture decisions ("significant minimum monthly cost even with zero traffic")
- Cost model differences vs AWS equivalents ("fixed monthly vs pure pay-per-request")

**Do not include:**
- Specific dollar amounts for individual tiers or SKUs
- Per-GB, per-request, or per-hour rates
- Pricing tables with dollar columns
- Regional pricing variations

**The test:** If a price change would make the statement wrong, it's too specific. "Standard v2 costs roughly one-quarter of classic Premium" survives a price change. "$700/month vs $2,794/month" does not.

### Depth: Concepts and Decisions Over Reference Material

Guides teach understanding and decision-making, not CLI syntax or configuration steps:

**Do include:**
- How the service works conceptually (architecture, components, data flow)
- When and why to use each tier, SKU, or configuration option
- Tradeoffs between options (with comparison tables)
- Common mistakes and how to avoid them
- How the service relates to other Azure services and to AWS equivalents

**Do not include:**
- CLI commands, API syntax, or step-by-step configuration instructions
- Exhaustive feature matrices that replicate Microsoft documentation
- Version history or changelog details
- Exact limits and quotas that change frequently (reference the docs for current limits)

**Exception:** Include specific technical values when they directly inform architecture decisions (e.g., "each CU represents approximately 2,500 concurrent connections" helps with capacity planning; "/27 minimum for GatewaySubnet" prevents a common misconfiguration).

## Key Differences from AWS Guides to Keep in Mind

1. **Subscription & org hierarchy is foundational** - Tenant → Management Groups → Subscriptions → Resource Groups → Resources; no AWS equivalent at this depth
2. **Entra ID is far richer than IAM** - full identity platform, not just resource access control
3. **App Service has no direct AWS equivalent** - unique PaaS compute platform
4. **Bicep is unique to Azure** - no AWS equivalent (CloudFormation is JSON/YAML)
5. **Azure DevOps is a full ALM suite** - more comprehensive than AWS CodeSuite
6. **Cosmos DB's consistency models** - unique five-level consistency spectrum
7. **Azure Policy** - more powerful governance than AWS Config
8. **Azure Arc** - extends Azure management to any infrastructure
9. **Paired Regions** - Azure's unique approach to regional redundancy
10. **Azure OpenAI Service** - significant AI differentiator to cover in selection guide
11. **Managed Identities** - cleaner workload identity than AWS IAM roles for services
12. **Enterprise billing hierarchy** - EA departments, accounts, and enrollment structure unlike AWS consolidated billing

## Azure-Specific Concepts Considered but Not Given Separate Guides

These concepts are important but are covered within existing guides rather than needing their own:

- **Azure Portal / CLI / PowerShell / Cloud Shell**: Covered contextually in each guide (conceptual, not CLI syntax)
- **Azure Resource Manager (ARM)**: Covered in the Bicep/ARM IaC guides; ARM is the deployment plane, not a standalone topic
- **Azure Lighthouse**: Covered in Subscription & Tenant Architecture (multi-tenant management)
- **Azure Service Health / Resource Health**: Covered in Azure Monitor guide
- **Azure Advisor**: Covered across WAF guide and Cost Management guide
- **Microsoft Purview (data governance)**: Covered in Modern Data Architecture guide
- **Azure Static Web Apps**: Covered in App Service guide as a related compute option
- **Azure SignalR Service**: Covered in App Service guide (real-time web features)
- **Azure Notification Hubs**: Covered in Application Integration guide as a messaging option
- **Azure Service Fabric**: Not included; largely superseded by AKS and Container Apps for new workloads

---

## Progress Tracking

**Last Updated**: 2026-02-10
**Guides Completed**: 31 / 61
**Current Phase**: Phase 6 Complete - Phase 7 next (Guide #32: Microsoft Defender for Cloud & Sentinel)
