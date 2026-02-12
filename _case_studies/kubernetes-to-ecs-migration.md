---
layout: case-study
title: "When Someone Else's Problem Becomes Your Solution"
subtitle: "Two years of Kubernetes operational pain, self-blame, and a three-day migration to ECS that should have happened sooner"
description: "A small team adopted Kubernetes without evaluating fit, spent two years blaming themselves for the operational overhead, and eventually migrated to ECS Fargate in three days. This case study covers the full journey: the breaking changes, the denial, and the moment the team realized they had adopted someone else's problem."
role: "System Architect"
date: 2024-12-01
headline_metric: "20% More Value Delivered"
headline_detail: "3-day migration, zero outages since"
category: "success"
category_label: "Migration Win"
technologies:
  - Kubernetes
  - AWS EKS
  - AWS ECS Fargate
  - CloudFormation
  - Docker
---

## Executive Summary

Three years ago, I adopted Kubernetes for a project running about 20 containers on AWS. I didn't evaluate whether it fit the problem. Well, I thought I did, but I never stopped to reconsider after an initial analysis. I assumed that if "everyone else was using K8s", we should too.

The hosting cost was striking once I actually did the math. We ran three clusters across two environments, which meant six EKS control planes at [$0.10/hour each](https://aws.amazon.com/eks/pricing/){:target="_blank" rel="noopener noreferrer"}, roughly $438/month just for the management layer. The actual compute costs were far less than the control plane fees. We were paying more for the privilege of running Kubernetes than for the workload itself. (A fact that does not make me look so good, now does it?) But even the hosting costs weren't the real story. The real cost was four hours per week of architect time spent manually tuning resource allocations, full weeks lost to upgrade cycles, customer-facing outages caused by the platform's own scaling automation, and the opportunity cost of features that didn't ship because IT leadership was consumed by infrastructure operations.

For most of the proceeding two years, we assumed we were the problem. We just needed to learn how to run Kubernetes correctly. That assumption however broke after conversations with other engineers who had lived through the same experience. It was something like a K8s PTSD support group. Team after team had the same stories about version upgrade nightmares, scaling that didn't respect budgets, and cloud provider abstractions that added complexity instead of removing it. We weren't incompetent. We had all adopted a tool built for Google-scale problems and tried to make it work for smaller, simpler workloads on a single cloud provider.

Eventually, I openly admitted my mistake and moved every container to AWS ECS Fargate. The migration took three days. Customer-facing outages from scaling events dropped to zero, and the total expected value score of delivered projects increased by roughly 20%. We didn't just ship faster; we shipped more projects and higher-value projects. I can't isolate a perfect causal ratio between the migration and that improvement, but the increase in completed projects happened on the same timeline, and the team's capacity was no longer being drained by infrastructure operations.

**Key lessons:**
- Technology selection driven by industry hype instead of requirements analysis leads to expensive mismatches
- Self-blame (of the wrong sort) and sunk cost thinking can delay obvious decisions by years
- Managed cloud-native services exist precisely to avoid the complexity that K8s introduces
- A tool built for someone else's problem at someone else's scale becomes your problem at your scale

## When the Doubt Started

The first real crack appeared during a Kubernetes minor version upgrade. Again, a minor version upgrade. The new version introduced breaking changes with the standard agents that EKS had previously installed on our clusters on our behalf. That was a large flaw in the original setup. Some of those agents were installed automatically by EKS without our involvement; others we had installed manually. The result was an inconsistent management surface where some components were under AWS's control and others were under ours, and the version upgrade put them at odds with each other.

The fix wasn't a patch. It would have required rebuilding entire clusters from scratch, for every cluster we ran.

I could assign blame three ways, to Kubernetes itself, to AWS EKS's abstraction layer, and to our own gaps in understanding. But that realization was itself the point. If running a container orchestration platform requires deep expertise in both the orchestration layer and the cloud provider's specific abstraction of it, the solution is not sustainable for a team our size.

Compare this to virtually any other cloud service. You set it up once and walk away. Upgrades are usually automatic, and when they're not, they're simple and predictable. A container orchestration solution should not behave like a JavaScript project with a hundred npm packages, where every version bump creates cascading compatibility issues across layers you don't fully control.

## The Operational Tax

The version upgrade was the crack, but the daily reality had been eroding us for much longer.

### Scaling That Caused Outages

Kubernetes scaling signals never properly integrated with the cloud-native infrastructure underneath EKS, and the speed of K8s scaling decisions was lost in translation to the underlying AWS layer. This was mostly a problem between the K8s control plane and the AWS target groups. Also, during node scale-up and scale-down events, K8s would initiate changes without respecting Pod Disruption Budgets. It wouldn't enforce that at least N replicas of a service stayed running during scaling and updates.

Critical customer-facing processes would simply vanish. Not degrade. Vanish. Infrastructure automation that was supposed to improve reliability was causing outages. Maybe it only happened once in every hundred scaling events, but that's the wrong way to think about it. When a scaling event takes down a customer-facing process, the question isn't how often it happens relative to total events. The question is whether the platform can be trusted not to cause outages at all. A platform that occasionally kills the services it's supposed to protect has a fundamental reliability problem.

Before anyone asks: yes, we tuned the health checks, scale-down delays, and scale-up delays to match each container's startup and readiness characteristics. That's a common source of scaling issues and we got it right. It didn't matter. The disruption budgets were still not enforced during node-level scaling events.

The "solution" was to increase the minimum number of replicas per service, which defeats the entire purpose of auto-scaling. I never found a real fix for this. EKS [requires significantly more operational overhead](https://www.fairwinds.com/blog/strengths-and-weaknesses-of-aks-eks-and-gke){:target="_blank" rel="noopener noreferrer"} than GKE or AKS, with less pre-configured automation and more manual configuration for exactly these kinds of integration points. The [upgrade process alone](https://komodor.com/blog/the-2024-managed-kubernetes-showdown-gke-vs-aks-vs-eks/){:target="_blank" rel="noopener noreferrer"} requires separate control plane and node group management, and EKS is consistently the slowest among major providers to adopt new Kubernetes versions.

### The Time Tax

Three ongoing costs consumed my capacity every week.

About four hours per week went to resource allocation tuning. Constant small adjustments to CPU and memory allocations per service and per node group. To benefit from K8s's resource efficiency, I had to be the direct source of that benefit. Load testing beforehand was never enough to define optimal defaults for a service; it took weeks of production issues and incremental tweaking to dial in each one.

Each K8s upgrade consumed a full week of sustained research and testing. There was no budget to spin up a parallel environment, so the dev environment had to serve double duty. That meant the rest of the team was blocked during upgrade cycles. And again, we are talking about a "managed" EKS solution, not a pure K8s solution that I could test locally.

Then there was constant news monitoring. Staying current on upcoming K8s changes was mandatory because falling behind on versions meant the cloud provider would charge additional fees for running unsupported releases. If you didn't track what was coming in the next few months, you'd get caught off guard by forced upgrade deadlines and surcharges. Of course, I do this for all AWS and third party tools we use, but the difference is that other tools do not pull the rug from under me and run me over with a bus loaded with documents telling me the pain is all in my head.

### Operational Cost Summary

| Cost Category | Impact |
|:---|:---|
| Resource allocation tuning | ~4 hours/week of architect time |
| K8s upgrade cycles | ~1 full week per upgrade, blocking dev environment |
| Version monitoring | Ongoing; miss it and face surcharges |
| Scaling outages | Customer-facing processes vanishing during node changes |
| Pod Disruption Budgets | Never respected; workaround negated auto-scaling value |

## Why It Took So Long

Two things delayed the migration even after the doubt set in.

First, feature priorities. Certain platforms and capabilities had to be completed before we could absorb the risk and disruption of a migration. The business couldn't wait while we rearchitected infrastructure.

Second, and more honestly, denial. I saw Kubernetes everywhere. Conference talks, blog posts, hiring trends, job descriptions. It felt safer to go with the crowd than to question whether the tool fit our context. Admitting that K8s was wrong for us felt like admitting incompetence, not recognizing a mismatch. To a degree, I suppose you might call this resume-driven development. We wanted to learn what others knew. Nevermind that most of us all share the same ignorance.

## The Migration

After wasting yet another full week trying to push through a K8s upgrade, the team just wanted to be done. The conversation with leadership was straightforward: operational cost and opportunity cost. More money saved and more features delivered. They needed no further persuasion. Every layer of the company had felt the pain by proxy. They had felt the unavailability of their most important IT leadership, whose time was being consumed by K8s operations instead of strategic work.

The only real objection was availability during the cutover. But the plan was straightforward and the simplicity of the approach dissolved the concern.

The migration to AWS ECS Fargate took three days. We moved one service at a time, standing it up on ECS and verifying stability before touching the next. Each K8s service stayed running until its ECS counterpart was confirmed healthy. The cutover itself was simple AWS plumbing: DNS A records pointing to new ALBs, each ALB routing to ECS target groups. We stood up separate ALBs for each cluster boundary (public services, private services, and workers), so each group could be migrated and validated independently.

Task definitions replaced Kubernetes manifests. AWS networking replaced custom overlays. The application code didn't change at all.

The one friction point was ECS task definitions. There's no separation between pod configuration and container image configuration the way K8s has it; everything is collapsed into the task definition. Getting this to work well in the CI/CD pipeline took some rework, but it was manageable.

CloudFormation stacks made the infrastructure side straightforward: destroy and create, deterministic every time. This was the sharpest contrast with EKS, where third-party component versions and schema version conflicts had made every infrastructure change unpredictable between upgrades and over time.

No rollback moments, no close calls, zero issues. The entire migration was anticlimactic, and that anticlimax is itself the point. Two years of complexity and operational pain, replaced in three days by something that just worked.

## Results

With three clusters across two environments, we were running six EKS control planes. At [$0.10/hour per cluster](https://aws.amazon.com/eks/pricing/){:target="_blank" rel="noopener noreferrer"}, that's roughly $438/month just for the control plane layer, and it jumps to $0.60/hour ($432/month per cluster, $2,592/month total) if you fall behind onto an extended-support K8s version. The actual compute costs were nearly identical on both platforms and trivial by comparison. ECS has no equivalent control plane fee. We were paying more for the management layer than for the workload it managed. But the numbers that mattered most were the ones that never appeared on an invoice.

| Metric | Before (K8s/EKS) | After (ECS Fargate) |
|:---|:---|:---|
| Monthly control plane cost | ~$438 (6 clusters × $73) | $0 |
| Monthly compute cost | Nearly identical | Nearly identical |
| Architect time on infrastructure ops | ~4 hrs/week + upgrade weeks | Near zero |
| Disruption budget violations | Recurring, never resolved | Zero, ever |
| Customer-facing outages from scaling | Regular | None |
| Spot instance utilization | Difficult, limited | Easy, effective |
| Delivered project value | Baseline | ~20% increase in expected value score |

At larger scale with heavier compute, the control plane fee becomes a smaller fraction of total cost. But at our scale, the management layer was the dominant expense, and eliminating it was immediate savings. The human cost made the case even more overwhelming. Four hours per week of architect time reclaimed. Full upgrade weeks eliminated. Leadership available for strategic work instead of cluster operations.

ECS Fargate has never once violated a disruption budget. Never once caused an outage. Zero effort required to achieve this. Spot instances also became much easier and more effective to use on Fargate, pushing costs down even further.

The total expected value score of delivered projects increased by roughly 20% after the migration. More projects completed, and higher-value projects at that. The team could focus on the business instead of managing someone else's software.

### A Note on Fargate Pricing

Early criticism of ECS Fargate centered on cost; when it launched, Fargate was genuinely more expensive than managing your own EC2 instances or K8s nodes. That reputation is outdated. AWS [cut Fargate prices by up to 50% in January 2019](https://aws.amazon.com/blogs/compute/aws-fargate-price-reduction-up-to-50/){:target="_blank" rel="noopener noreferrer"}, introduced Fargate Spot (up to 70% savings) and Compute Savings Plans (up to 50%), and added Graviton/ARM support at 20% lower cost with better performance. The price gap that once justified self-managed Kubernetes has largely closed, and for teams without dedicated platform engineers, the total cost of ownership comparison isn't even close.

With all of that said, I do miss: `kubectl apply` and YAML-based declarative changes made versioned service updates easier, even compared to CloudFormation. The deployment ergonomics of K8s were genuinely good. But the golden violin wasn't worth the deal with the devil. I am allowed a little melodrama.

## Key Lessons

### 1. Technology selection requires honest requirements analysis

Before adopting Kubernetes, I should have asked five questions honestly: Do we need multi-cloud? Are we running hundreds of microservices? Do we have dedicated platform engineers? Is the operational overhead justified? Do we need fine-grained orchestration control? The answer to every one was no.

### 2. Self-blame delays obvious decisions

The denial period cost us at least a year. We assumed the problem was our technical competence rather than our tool selection. Talking to other teams who had the same experience broke through that assumption. We were still to blame, just not for the immediate reasons that so many blog posts and tech influencers claim.

### 3. Managed services exist for a reason

The entire premise of cloud computing is to avoid unnecessary operational complexity in order to reduce costs of all kinds and increase agility without sacrificing observability. Kubernetes is not built for that goal. It's built for the scenario where scale is so large that even a tiny cost or resource optimization makes a material difference, and where dedicated platform teams exist to absorb the operational overhead.

### 4. Don't adopt someone else's problem

Kubernetes was built to handle the challenges of the company that built it. We so often adopt someone else's solution to their problem and make their problem our own, rather than finding solutions built for our actual needs. If you're not operating at the scale that justifies the complexity, you're paying the complexity tax for nothing.

### 5. Not all migration improvements are about the technology

Not all improvements during technology migrations are actually due to the technology change itself. Often it's the realignment with best practices or business use cases that provides the real benefit. But in this case, it genuinely was the technology choice. We replaced a tool that demanded constant expertise and attention with one that handled the same workload transparently.
