---
layout: post
title: "Why I Migrated from Kubernetes to ECS"
date: 2025-09-08
series: "Technology & Tools"
tags: [kubernetes, aws, architecture, cost-optimization]
description: "Two years ago I adopted Kubernetes without evaluating whether I needed it. The result: $2K/month in unnecessary costs and constant operational overhead. Here's what I learned about technology selection and hype."
---

Two years ago, I adopted Kubernetes for a project running about 20 containers. I didn't evaluate whether I needed it; I just assumed that if everyone else was using K8s, we should too. The result was $2K/month in unnecessary costs and endless operational headaches.

Last month I migrated to AWS ECS Fargate. The costs dropped immediately, operations simplified dramatically, and I finally admitted what should have been obvious from the start: I never needed Kubernetes in the first place.

This isn't a criticism of Kubernetes. It's a criticism of my own decision-making. As an architect, my job is to evaluate tradeoffs before making commitments. Instead, I got caught up in industry hype and skipped the most basic step: asking whether the technology actually fit the problem.

## The Questions I Didn't Ask

Before adopting Kubernetes, I should have asked:

- **Do we need multi-cloud deployment?** No. We were committed to AWS.
- **Are we running hundreds of microservices?** No. We had about 20 containers.
- **Do we have dedicated platform engineers?** No. The team managed the cluster alongside feature work.
- **Is the operational overhead justified?** No. Weekend cluster maintenance and constant node optimization weren't adding value.
- **Do we need fine-grained control over orchestration?** No. We needed reliable deployments and auto-scaling, which managed services provide out of the box.

I didn't ask these questions honestly. I saw Kubernetes everywhere (conference talks, blog posts, hiring trends) and assumed adoption was inevitable. The technology had momentum, so it felt safer to go with the crowd than to question whether it was the right fit.

## What Kubernetes Is Built For

Kubernetes excels at massive scale with dedicated platform teams. If you're running thousands of services across multiple clouds like Google or Netflix, it makes sense. You need the flexibility, the control, and the ability to abstract infrastructure. The operational overhead is justified because the problem demands it.

For small teams running dozens of containers on a single cloud provider, Kubernetes is overkill. It's like using a semi truck for pizza delivery. The truck works, but the maintenance costs, licensing requirements, and fuel consumption don't match the actual need.

Most teams just need containers to deploy reliably, scale automatically, and integrate with their cloud provider's ecosystem. They don't need to manage clusters, optimize node utilization, or debug networking overlays.

## What Actually Fit the Problem

AWS ECS Fargate turned out to be the right answer for this project. It's fully managed, integrates natively with AWS services, and costs significantly less. No cluster management, no node optimization, no operational overhead.

The migration took 3 days. Again, 3 days. Task definitions replaced Kubernetes manifests, IAM roles replaced service accounts, and AWS networking replaced custom overlays. The application code didn't change at all.

After the migration:
- Costs dropped by roughly 60%
- Deployment complexity decreased significantly
- Integration with AWS services (IAM, CloudWatch, Secrets Manager) became straightforward
- The team stopped spending weekends troubleshooting cluster issues

Similar managed container solutions exist across cloud providers (Azure Container Instances, Google Cloud Run). The key is evaluating what fits your actual needs rather than following industry trends.

## The Real Lesson

Technology choices should be driven by constraints and requirements, not hype. Before adopting something new, ask whether it solves a problem you actually have. If the answer isn't clear, the default should be skepticism, not enthusiasm.

The boring, simple solution is usually the right solution. Managed services often fit better than self-managed infrastructure. Cloud-native primitives often work better than vendor-neutral abstractions.

As architects, we're supposed to protect our organizations from expensive assumptions. That means asking hard questions about our specific context before committing to trendy technologies, even when the entire industry seems to be moving in one direction.

Kubernetes didn't fail me; I failed to do my homework.