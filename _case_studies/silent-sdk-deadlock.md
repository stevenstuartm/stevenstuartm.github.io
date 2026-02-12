---
layout: case-study
title: "When a Trusted Dependency Becomes a Silent Killer"
subtitle: "A silent deadlock in a trusted SDK bypassed every test we had, and plan continuation bias cost me two days I didn't need to lose"
description: "A production outage traced to a silent thread deadlock in AWS SDK v4 that bypassed all functional and regression testing. This case study covers the detection, the false leads, the investigation mistakes, and the process failures that let a third-party bug reach production undetected."
role: "System Architect"
date: 2025-11-05
headline_metric: "Silent SDK Deadlock"
headline_detail: "bypassed all existing tests, 3-day investigation"
category: "failure"
category_label: "Investigation Lessons"
technologies:
  - AWS SDK .NET
  - AWS ECS Fargate
  - DynamoDB
  - Entity Framework
  - Dapper
  - .NET
---

## Executive Summary

On a Friday afternoon, our primary website started failing. Most requests to the CMS proxy API were returning errors, and our health checks fired the first alert. The API itself showed no signs of container stress. ECS metrics were clean. The service appeared healthy by every measure except the one that mattered: it wasn't serving requests.

Within an hour I had identified that the real failure was in the authentication service, rolled back all APIs to a known-good version, and restored production. But the rollback blocked a feature we had just released and were actively selling, so I needed to find and fix the root cause before redeploying.

That took three days. Friday through Sunday, working alone while one colleague was on vacation and another was locked in third-party meetings. The root cause turned out to be a silent thread deadlock introduced in [AWS SDK .NET v4's core authentication library](https://github.com/aws/aws-sdk-net/issues/4020){:target="_blank" rel="noopener noreferrer"} that starved the thread pool under production load until the service couldn't respond. I spent two of those three days chasing the wrong hypothesis. The rewrite I did for nothing wasn't the root cause. The package I trusted most was.

**What failed:**
- A third-party SDK shipped a critical thread-locking bug without declaring it as a breaking change
- Our deployment process trusted well-known vendors and skipped load testing for a release that appeared low-risk
- My investigation process locked onto a plausible-but-wrong hypothesis for two days before I let go of it

## The System

The production environment ran roughly 20 APIs on AWS ECS Fargate behind application load balancers. The CMS proxy API served as the front door for the primary website, caching content transformations from a third-party CMS for controlled consumption by website products. Total request volume across the system sat between 100 and 1,000 requests per second.

The authentication service handled token validation and user grant verification for content entitlements. By design, it operated on a high-security, low-trust model: every request required a fresh DynamoDB call to validate tokens and confirm user grants. There was no auth caching. Every CMS API request triggered an auth API call, and every auth API call triggered a DynamoDB call. This made the auth service the highest-throughput internal dependency in the system, and it made DynamoDB the hottest path in the entire architecture. That was not a concern. DynamoDB had consistently proven itself capable of handling this load, and relying on it for the auth hot path had solved real performance and reliability problems that earlier designs had struggled with.

## Detection and Initial Response

Health checks caught the issue first and sent an alert to the IT support email. From the website's perspective, most requests to the CMS API were failing, but not all. The failure pattern looked like throttling: some requests succeeded while most did not.

My first instinct was to check the CMS API container itself. ECS metrics showed nothing abnormal. CPU, memory, and network were all within normal ranges. The container was not stressed, and yet it could not serve traffic. That disconnect was the first clue that the problem wasn't where it appeared to be.

The logging on the CMS API was thorough, and it told a different story than the metrics. Alongside the primary errors, I saw smaller downstream warnings that traced the flow of the failure. The CMS API wasn't the service failing. It was waiting on the authentication service, which was not returning successful responses when the CMS service attempted to validate user tokens and confirm content grants.

But when I looked at the auth service directly, its metrics were clean. No CPU spikes, no memory pressure, no error rates in the dashboards. Other APIs in the system could be reached, but the CMS and auth services could not. Knowing the architecture, I understood that those two weren't uniquely broken. Any other API would have exhibited the same failure had it been called as frequently.

## The Rollback Decision

Before diving into root cause analysis, I rolled back the deployment. The complication was that the latest release had been a broad upgrade across all APIs, so I couldn't roll back just the auth service. Every API went back to the previous known-good version.

Production was stable within an hour. But the rollback came with a cost: a feature we had just launched and were actively selling required changes from the new deployment, specifically a more efficient approach to gathering complex user grants for custom business logic. That feature was now blocked.

The business was alerted immediately. To their credit, they understood the complexity and did not add pressure beyond what the situation already carried. They knew we were working the issue continuously.

## The Investigation

With production stable, I needed to find the bug in the auth service and redeploy everything. I started where any reasonable investigation would start: my own code changes.

### First Lead: The Shared Package

The deployment included a change to an internal shared package that controlled common distributed security concepts and logic. This package contained an HTTP client used when calling the auth API, and since it was one of the few pieces of shared code between services, it warranted scrutiny.

I examined the errors and warnings in the logs and confirmed that the failures were not originating from anything in the shared package. The HTTP client changes had no correlation to the log patterns. Unit tests confirmed the code was sound at scale. This lead was eliminated relatively quickly.

### The Entity Framework Rabbit Hole

This is where the investigation went sideways.

The auth API's health endpoint used Entity Framework to verify database connectivity, and I had noticed an AWS health check error when calling that endpoint. Since those health checks rely on EF to determine service health, and since I had made minor changes to EF behavior, query structure, and library versions in the latest deployment, this seemed like a strong lead.

I knew from experience how unpredictable EF context management and thread pool behavior could be. The auth service's hot request path involved EF, and the health check was failing intermittently. The circumstantial evidence lined up. There were no direct database usage issues, but EF's internal threading model seemed like a plausible culprit for the kind of silent degradation I was seeing.

So I dug in. I analyzed the EF context lifecycle, the query execution patterns, and the thread pool interactions. I reviewed every change I had made to the EF configuration and queries. When nothing conclusive surfaced, I kept going. I was convinced the problem was there; I just hadn't found it yet.

Eventually, I rewrote the entire data access layer in Dapper to eliminate EF as a variable. The queries in the auth service were simple enough that a full ORM was unnecessary, and replacing EF with Dapper made the data access layer simpler and more predictable. But I did it for the wrong reason, at the wrong time, and it violated a principle I knew well: change one thing at a time and deploy only what is needed. The Dapper rewrite did not fix the problem.

After it failed, I had to accept that EF was not the cause. The health check errors I had been chasing were a symptom of the broader failure, not the source. The auth service's target group was attempting to scale because the API couldn't return successful responses, and the health check failures were a downstream effect of that scaling behavior. I had spent roughly two days on this lead, and "getting closer" was the only thing keeping me on it. That is how plan continuation bias works: the sunk effort makes the current path feel more valuable than starting over, even when starting over is exactly what you should do.

### The Breakthrough

With my own code changes eliminated and EF ruled out, I turned to the remaining variable: third-party NuGet package upgrades included in the deployment. I started testing downgrades one at a time in the dev environment, but none of the individual rollbacks resolved the issue.

Then I did what I should have done much earlier. I read the patch notes.

The AWS SDK for .NET had released version 4 of its core library, and buried in the changes was a modification to the credential refresh logic. The SDK had introduced a background refresh mechanism for credentials that created a deadlock under concurrent load. Threads would hang silently waiting for credential refresh to complete, and that refresh was itself waiting on a thread that was already blocked. No exceptions were thrown. No errors were logged. The thread pool simply starved until the service could not process requests.

The specific service that triggered this deadlock so aggressively was the auth API's call to DynamoDB. Every token validation required a DynamoDB call, every DynamoDB call went through the AWS SDK's credential resolution, and every credential resolution now had a chance of deadlocking under load. At 100-1,000 requests per second flowing through this path, the deadlock manifested quickly and consistently in production while remaining invisible in lower-traffic environments.

And every AWS package in the system depended on this core library version.

### The Fix

I rolled back nearly all AWS SDK NuGet packages across the affected APIs to a known safe version. The auth service was the most critical, but several other APIs that called AWS services needed the same treatment.

The irony was hard to miss. AWS had recently experienced a DynamoDB DNS outage around the same time, so I was dealing with a very different DynamoDB-adjacent issue within the same service window.

After the package rollbacks and redeployment, the system was fully restored including the blocked feature. AWS later acknowledged the bug and [released a fix in version 4.0.103.0](https://github.com/aws/aws-sdk-net/issues/4020){:target="_blank" rel="noopener noreferrer"}, which reverted the problematic background refresh changes.

We never upgraded those AWS packages again. Not because we couldn't, but because we had no pressing reason to, and when we eventually do, it won't happen without a proper load test.

In the weeks that followed, I wrote two posts born directly from this experience: one on [package upgrade discipline](/blog/2025/11/07/when-to-update-packages.html){:target="_blank" rel="noopener noreferrer"} and one on [troubleshooting under pressure](/blog/2025/11/08/troubleshooting-production.html){:target="_blank" rel="noopener noreferrer"}. They were reminders to myself more than anything, written while the mistakes were still fresh enough to be honest about.

## Key Lessons

### 1. Load test when dependencies change, not just when your code changes

We had run a complete regression before pushing the release and made a deliberate decision that a full load test was not needed. That decision was defensible for our own code changes, which were isolated and well-understood. What it failed to account for was that we had also upgraded third-party packages, and the risk profile of package upgrades is entirely different from first-party code changes. A package upgrade can introduce behavioral changes that are invisible to functional tests and only surface under production concurrency. The AWS SDK deadlock was exactly this kind of failure: functionally correct, catastrophically broken under load.

### 2. Trusted vendors still need verification

Over three years, we had upgraded AWS SDK packages roughly 30 times without incident. The AWS and Microsoft packages were the only ones we trusted enough to skip deep investigation on every upgrade. We actively reviewed changelogs and tested changes for every other dependency. This wasn't a blanket policy failure; it was a targeted trust that turned out to be misplaced. The cost of one undetected bug exceeded the cumulative time we would have spent reviewing changelogs and running load tests for every prior upgrade. "Trusted" should never be a synonym for "untested." I wrote about this broader principle in [Package Updates Are Investments, Not Hygiene Tasks](/blog/2025/11/07/when-to-update-packages.html){:target="_blank" rel="noopener noreferrer"}.

### 3. Time-box your hypotheses

If the EF lead had been obviously wrong, I would have abandoned it quickly. The danger was that it was plausible enough to sustain investigation for two days while I solved the wrong problem. A second set of eyes would have helped enormously, but with one colleague on vacation and another unavailable, there was no one to challenge the hypothesis. The counterfactual is painful: if I had started by reading the patch notes for every upgraded package, this might have been a four-hour investigation instead of a three-day one. Define what "disproven" looks like before you start, and force yourself to consider alternative explanations at fixed intervals.

### 4. Read the patch notes before reading the code

When a deployment introduces a failure and your own code changes are ruled out, the next step should be reviewing every third-party change in detail, starting with the patch notes and changelogs. I went to code analysis and package downgrade testing before I went to patch notes. That ordering cost me time. Patch notes are the cheapest investigation step and should come first.

### 5. Change one thing at a time during incident response

The Dapper rewrite happened to improve the codebase, but deploying it alongside the actual fix meant I changed two variables at once. If the rewrite had introduced its own subtle bug, I would have been chasing a second ghost on top of the first. During incident response, every change should be the minimum needed to test the current hypothesis. Improvements belong in a separate deployment after the incident is resolved. I wrote more about this and other troubleshooting disciplines in [Why the Fastest Incident Responders Slow Down First](/blog/2025/11/08/troubleshooting-production.html){:target="_blank" rel="noopener noreferrer"}.
