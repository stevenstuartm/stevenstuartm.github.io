---
layout: case-study
title: "When Architecture Patterns Don't Match the Problem"
subtitle: "Lessons from three attempts to build a distributed event processing platform"
description: "A fintech company built three successive solutions to process millions of financial events for real-time alerts. Each failed for different technical reasons, but the same organizational pattern persisted. This case study examines what went wrong and what should have been built instead."
role: "Software Developer"
date: 2023-01-01
technologies:
  - AWS SQS
  - AWS EventBridge
  - AWS DynamoDB
  - Akka
  - Microservices
---

## Executive Summary

Over six years, a fintech company built three successive solutions to process millions of financial transaction events for real-time customer alerts. Each solution lasted approximately two years before stakeholders demanded change. Each failed for different technical reasons, but a common organizational pattern persisted throughout: development teams remained out of alignment with stakeholder needs, and that gap was never closed.

This case study examines what went wrong technically and organizationally, why the third solution's architecture was mismatched to the problem, and what should have been built instead.

**Key lessons:**
- Distribution is an optimization, not a starting point
- Don't abandon good designs because of bad implementations
- Pattern selection requires trade-off analysis against actual requirements
- Observability isn't optional for financial systems
- Organizational alignment problems can't be solved with architecture changes alone

## The Business Context

The company operated as an intermediary layer between banks, credit unions, and end users. Rather than requiring smaller financial institutions to build their own user interfaces and complex integrations, the platform provided a rich UI experience backed by transaction processing infrastructure.

The primary feature under development was real-time transaction alerts: customers subscribe to events on their accounts, and they receive email or SMS notifications when transactions occur. The processing happened primarily after transactions had been accepted by the financial institutions.

**Scale and constraints:**
- Millions of financial transaction events to process
- 8+ development teams needing to plug processors and workflows into the platform
- Financial compliance requirements demanding audit trails and reliability
- Customer SLAs with real monetary penalties for failures

## Solution 1: The Monolith

The first attempt was a monolithic system built around a legacy scheduler. The architecture was poorly documented and poorly understood by the teams who inherited it.

**Why it failed:**
- Teams could not plug their processors and workflows into the existing infrastructure
- The system's behavior was opaque, making modifications risky
- No clear extension points existed for new functionality
- Scaling required manual configuration and human intervention rather than automated elasticity
- Non-containerized infrastructure made scaling expensive and slow

After approximately two years, stakeholders demanded change. The diagnosis was correct: the monolith couldn't support multi-team extensibility or cost-effective scaling. The prescription was a move to microservices.

## Solution 2: The Coordinator

The second solution introduced a microservices architecture with a central coordinator pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                    Central Coordinator                       │
│          (Queue management, event brokering)                 │
└──────────┬──────────────────┬──────────────────┬────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Domain Processor │ │ Domain Processor │ │ Domain Processor │
│    (Team A)      │ │    (Team B)      │ │    (Team C)      │
│                  │ │                  │ │                  │
│ Registers metadata│ │ Registers metadata│ │ Registers metadata│
│ for alert UI     │ │ for alert UI     │ │ for alert UI     │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

Each processor registered its metadata with the coordinator, which the alert management UI used to show customers what alerts were available.

**What worked:**
- Central location for audit and retry logic
- Each processor was a holistic domain processor owned by a single team
- Simple to understand: clear data flow, clear ownership
- Easy to reason about scaling at the coordinator level

**Why it was abandoned:**
- The implementation was poorly coded, leading to connection deadlocks
- The service wasn't designed to scale horizontally
- Queues were not used properly, creating resource exhaustion
- A refactor was deemed too expensive

**Why Solution 2 could have been redeemed:**

The value of Solution 2 wasn't that it was "good" but that it started with fewer components and consistent abstraction layers. This created options:

- When you wanted to bypass one layer for a new one, or go straight to a queue, you could do that incrementally
- You might end up with two versions of the same platform running in parallel, which enabled incremental migration without breaking changes
- The architecture supported gradual evolution rather than requiring wholesale replacement
- A lightweight adapter or API gateway could have been used to "two-step" the migration to a new solution while preserving the single abstraction layer

Solution 2 did have an event store in the central coordinator, but it was implemented as a simple queue rather than as durable storage with proper state management. It didn't support rollbacks or saga orchestration. Moving event persistence to the processor level (as proposed later in this case study) would have fixed that limitation while preserving the coordinator's architectural strengths.

**The critical mistake:** Rather than investing in fixing the implementation while preserving these architectural strengths, the organization chose to start over with a completely different architecture. This pattern would prove costly.

## Solution 3: Pipes & Filters

The third solution adopted a distributed pipes and filters architecture. Each actor had complete autonomy: its own authentication, its own AWS SQS access, and its own scaling behavior via Akka. A single central service handled subscriptions, metadata, and workflow registration, but communication between actors was distributed via SQS rather than synchronous API calls.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Central Registration Service                            │
│                                                                              │
│    Subscriptions    │    Metadata (UI)    │    Workflow (Parent/Child)      │
│                                                                              │
│                         All in-memory registration                           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                    Actors register on startup (concurrency bugs)
                                    │
                         ┌──────────┴──────────┐
                         │    Event Source     │
                         └──────────┬──────────┘
                                    │
                                   SQS
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │   Actor A   │──SQS──│   Actor B   │──SQS──│   Actor C   │
       │  (SQS+Auth) │       │  (SQS+Auth) │       │  (SQS+Auth) │
       │  DynamoDB   │       │  DynamoDB   │       │  DynamoDB   │
       │  Akka scale │       │  Akka scale │       │  Akka scale │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
             SQS                   SQS                   SQS
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │   Actor D   │       │   Actor E   │       │   Actor F   │
       │  (SQS+Auth) │       │  (SQS+Auth) │       │  (SQS+Auth) │
       │  DynamoDB   │       │  DynamoDB   │       │  DynamoDB   │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                   SQS
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    Notification Service    │
                    └───────────────────────────┘
```

Instead of using AWS EventBridge for fan-out, a custom solution was built to register parent/child processor relationships via the central registration service. Actors registered themselves with this single service on startup, which introduced concurrency bugs and created a single point of failure for subscriptions, metadata, and workflow routing.

**What worked:**
- Clean, well-structured code with good unit tests
- Queue-based communication throughout
- Testable locally using LocalStack
- DynamoDB for ephemeral workflow data

**What failed:**

### Architecture Problems

| Problem | Description | Impact |
|---------|-------------|--------|
| **Message bloat** | Actors didn't transform messages as intended; they added entire new context to payloads | Enormous network costs, bandwidth exhaustion |
| **No centralized control** | Each actor operated independently with no coordination | Impossible to audit, conflicted with financial compliance needs |
| **Custom fan-out** | Built custom parent/child registration instead of using EventBridge | Added complexity, introduced concurrency bugs during startup |
| **Shared infrastructure** | Actors ran on the same tier as UI APIs | Processing spikes caused UI unavailability |

### Operational Problems

| Problem | Description | Impact |
|---------|-------------|--------|
| **DLQs unused** | Dead letter queues were added but never monitored or processed | Lost events in a financial system |
| **No observability** | No centralized monitoring or alerting | Weeks passed before critical problems were detected |
| **Per-actor scaling** | Each actor had its own Akka scaling behavior | Impossible to identify bottlenecks or predict capacity |
| **In-memory metadata** | Central registration for processors used in-memory storage | Constant startup failures, single point of failure |

### Data Problems

| Problem | Description | Impact |
|---------|-------------|--------|
| **Stale DynamoDB data** | Decision-gate actors had configs that fell out of sync | Incorrect routing, inconsistent behavior |
| **Noisy neighbors** | One tenant could consume most of an actor's processing capacity | Unfair resource allocation, SLA violations |
| **SQS visibility timeout games** | Constant tuning to account for processing latency and tenant partitioning | Fragile configuration, message reprocessing |
| **Component-specific config** | Configurations tied to components, not domains | Nightmare for support teams when components changed |

### Developer Experience Problems

| Problem | Description | Impact |
|---------|-------------|--------|
| **Coupled deployments** | Any change required updating every actor simultaneously | Massive deployment cost, developer burnout |
| **API sprawl** | Teams created new APIs for every change | Fragmentation, inconsistency, maintenance burden |
| **No rollback capability** | Pipes and filters provides no saga pattern | Failed workflows left partial state with no compensation |

**The result:** After approximately two years, the accumulated failures led to SLA violations and significant customer payouts. The organization discovered problems weeks after they began because there was no observability, and by then the damage was done.

## Pattern Analysis: Why Pipes & Filters Was Wrong

The pipes and filters pattern makes specific assumptions about how data flows through a system:

| Pattern Assumption | Reality in This System |
|--------------------|------------------------|
| Each filter performs a stateless transformation | Actors added unrelated context, didn't transform |
| Filters are independent and composable | Actors required access to shared concepts and integrations |
| Scaling is per-filter based on throughput | Per-actor Akka scaling made bottlenecks invisible |
| Failure handling is per-filter | No saga support meant partial failures couldn't roll back |

The pattern was selected without formal trade-off analysis. Development teams weren't allowed to see the proposal, and no documentation existed explaining why this architecture was chosen over alternatives or what trade-offs were accepted.

**What should have triggered concern:**
- Financial systems require audit trails; pipes and filters distributes control
- The use case wasn't transformation; it was enrichment and routing
- Multi-tenant systems need fair resource allocation; per-actor scaling can't provide this
- Fan-out complexity suggested EventBridge, not custom registration

## The Organizational Pattern That Never Changed

Across all three solutions, the same organizational dynamic persisted:

**Development teams remained out of alignment with stakeholder needs.** Stakeholders demanded "change" every two years, but the actual requirements were never crystallized in a way that could be validated. Each solution was a technical response to stakeholder frustration rather than a deliberate answer to clearly defined needs.

**Architecture decisions were made without trade-off analysis.** Solution 3 was proposed without documented rationale, and the development teams building it weren't even allowed to see the proposal that mandated it.

No architecture can fix an alignment problem, and the pattern persisted because the organizational issue was never addressed.

## What Should Have Been Built

Based on the actual requirements and constraints, here's an architecture that would have addressed the real problems:

### Principle 1: Separate Concerns Cleanly

```
┌───────────────────────────────────────┐
│           Alert Management UI          │
│      (Customer subscription mgmt)      │
└───────────────────┬───────────────────┘
                    │ reads
                    ▼
┌───────────────────────────────────────┐      ┌─────────────────────────┐
│       Alert Feature Metadata DB        │◀─────│   Versioned Migration   │
│         (Available alert types,        │      │        Tasks            │
│          subscription options)         │      │  (No code deployment)   │
└───────────────────────────────────────┘      └─────────────────────────┘

                    ║ No coupling - UI metadata is completely
                    ║ separate from event processing
                    ╨

┌───────────────────────────────────────┐
│           Transaction Events           │
│         (From financial systems)       │
└───────────────────┬───────────────────┘
                    │
                    ▼
┌───────────────────────────────────────────────────────────────────────┐
│                          AWS EventBridge                               │
│                (Fan-out routing, no custom registration)               │
└──────────┬────────────────────┬────────────────────┬──────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Domain Processor │  │ Domain Processor │  │ Domain Processor │
│    (Team A)      │  │    (Team B)      │  │    (Team C)      │
│                  │  │                  │  │                  │
│ Just processes.  │  │ Just processes.  │  │ Just processes.  │
│ No registration. │  │ No registration. │  │ No registration. │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

- **Alert feature metadata and subscriptions** live in a versioned database, updated via separate migration tasks. No deployed code changes needed for metadata updates. The UI reads what alerts are available, customers subscribe through this service, and processors query it to determine which customers to notify for a given event. The subscription service is a stable API that processors consume, not something processors register with.
- **Event processing** is handled by async processors that just process. EventBridge routing rules are managed through infrastructure-as-code, tied to component versions rather than runtime registration. Processors don't self-register with internal coordinators or maintain UI metadata. When a processor receives an event, it queries the subscription service to find matching customers.
- **Fan-out routing** uses AWS EventBridge's native capabilities, eliminating custom parent/child registration logic and the concurrency bugs that came with it.

### Principle 2: Start with Domain Processors, Distribute When Proven

Solution 2 got this right: each domain/feature team owns their own processor. Distribution is an optimization to a proven need, and there was never any proven need for distributing work beyond single domain processors.

- Use share-nothing architecture: domains handle themselves
- No central coordinator needed
- Add Kinesis or other streaming only when measurement proves necessity

When workflows span multiple domains, use eventful choreography rather than orchestration. Each domain publishes events to EventBridge when its work completes, and other domains subscribe to events they care about. This adds documentation complexity (you need to track which domains produce and consume which events), but it's the correct trade-off for a high-agility, multi-team environment where teams need to evolve independently.

### Principle 3: Queuing Strategy Depends on Ordering Requirements

The right queuing approach depends on whether strict ordering matters for your domain:

**When ordering doesn't matter: SQS Fair Queues**

For domains where events can be processed in any order, [SQS Fair Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html){:target="_blank" rel="noopener noreferrer"} provide automatic noisy-neighbor mitigation. By setting `MessageGroupId` on messages (typically to the tenant ID), SQS automatically ensures fair resource allocation across tenants without custom code. This would have solved the noisy-neighbor problem in Solution 3 with zero implementation effort.

Fair Queues work because they're Standard queues with fairness semantics: virtually unlimited throughput, no in-flight message limits per tenant, and automatic dwell-time fairness. The trade-off is no ordering guarantees.

**When ordering matters: Persist-then-consume pattern**

For domains requiring strict ordering (e.g., transaction sequences where order affects balance calculations), SQS FIFO has throughput constraints that create back-pressure during traffic spikes. The alternative is to persist events first and consume based on configurable rate and priority:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Domain Processor                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   Event Store   │───▶│         Processing Logic            │ │
│  │   (DynamoDB)    │    │  • Partitioned by tenant            │ │
│  │                 │    │  • Configurable consumption rate    │ │
│  │  PK: TenantID   │    │  • Priority-based processing        │ │
│  │  SK: Timestamp  │    │  • Claim Check for large payloads   │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
│           │                              │                       │
│           ▼                              ▼                       │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   Audit Trail   │    │      Async Observability            │ │
│  │   (per domain)  │    │   (aggregated centrally)            │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

**Ordering in DynamoDB**: DynamoDB maintains sort key order within a partition. By using `TenantID` as the partition key and a timestamp or sequence number as the sort key, you get ordered reads per tenant for free. The processor queries each tenant's partition in order, processes at a configurable rate, and marks items as processed. This gives you FIFO semantics per tenant without SQS FIFO's throughput constraints.

**Fair consumption across tenants**: The processor controls the consumption rate per tenant, ensuring no single tenant monopolizes processing capacity. This is the configurable priority queue the system needed but never had. You can implement round-robin across tenants, weighted priority based on SLA tier, or burst allowances with rate limiting. All of this is controlled by your code rather than queue configuration.

| SQS-Only Approach | Persist-then-Consume Approach |
|--------------------|------------------------------|
| Visibility timeouts constantly tuned | Persistent state eliminates timeout games |
| Consumer memory pressure | Read what you need, when you need it |
| FIFO throughput constraints (300-3000 msg/s per group) | DynamoDB scales to your write capacity |
| Ordering only within message groups | Ordering within partitions with tenant isolation |
| Can't see traffic patterns until consumed | Visible backlog enables predictive scaling |
| "How many nodes?" = guess | "How many nodes?" = data-driven from backlog metrics |

**Note on saga patterns**: The original Solution 3 had no rollback capability when workflows failed mid-stream. Saga orchestration addresses this, but it's orthogonal to the queuing strategy. Whether you use SQS or persist-then-consume, compensating transactions need to be designed into the workflow. The persist-then-consume approach makes saga state easier to manage because the event store already has the workflow history.

### Principle 4: Domain-Centric Configuration

| Component-Specific Config (What Was Built) | Domain-Specific Config (What Was Needed) |
|--------------------------------------------|------------------------------------------|
| Config tied to component deployment | Config tied to business domain concepts |
| Component changes break config | Component architecture can change freely |
| Support teams must understand topology | Support teams work with domain concepts |
| SDK consumers coupled to implementation | SDK consumers work with stable abstractions |

### Principle 5: Governance Through Async Observability

- Each domain processor audits all activity properly, in an async manner
- Governance ensures compliance without blocking processing
- Support staff sees problems and traffic summaries as they occur
- No more weeks-long blind spots

The specifics of governance depend on team size and domain nature, but Architecture Decision Records (ADRs) are always a good starting point. This was something the organization never did across any of the three solutions. Documenting why decisions were made creates accountability and helps future teams understand constraints.

### Principle 6: Claim Check for Actual Data Flow

The processors weren't mutating a single payload through stages. Often they weren't even looking at the same data. The Claim Check pattern acknowledges this reality: store large or context-specific data separately and pass references.

When processors need shared data, they query stable domain APIs (like the subscription service) rather than passing bloated payloads between stages. Each workflow is isolated, and all processors must be idempotent. This was another problem in Solution 3: SQS locking and visibility timeout issues meant the same work was sometimes processed more than once, causing duplicate notifications and inconsistent state. With a persisted event store at the processor level, idempotency is enforced by design. You can track which events have been processed and skip duplicates.

### Principle 7: Tenant Isolation at the Processor Level

EventBridge doesn't need to worry about tenants; that's the processor's responsibility. With a persisted event store, processors can implement custom priority and rate-limiting patterns to ensure fair resource allocation across tenants (as described in Principle 3). If traffic patterns demand it, the architecture can evolve: EventBridge rules can point to Kinesis, which manages tenant isolation through shards. The key is that tenant isolation is a processor concern with clear options for scaling, not a system-wide problem with no good answers.

## Key Lessons

### 1. Distribution is an optimization, not a starting point

Solution 3 assumed distribution was necessary from day one, but there was never a proven need for distributing work beyond single domain processors. The better approach: start simple, measure actual bottlenecks, then optimize.

### 2. Architectural flexibility matters more than initial correctness

Solution 2 had significant problems, but it hadn't overextended itself. The simpler architecture left room to evolve: you could fix the implementation, add new layers incrementally, or migrate components without wholesale replacement. Solution 3's distributed complexity closed off those options.

### 3. Pattern selection requires trade-off analysis

Pipes and filters has well-known trade-offs, and those trade-offs conflicted directly with the requirements of this system. No formal analysis was performed, no documentation explained the choice, and development teams weren't even allowed to see the proposal.

### 4. Observability isn't optional for financial systems

Solution 3 had no centralized observability, so problems went undetected for weeks. By the time issues were discovered, SLA violations had already triggered significant customer payouts. In financial systems, you must know what's happening in real-time.

### 5. Organizational alignment problems can't be solved with architecture changes

The same misalignment between development teams and stakeholders persisted across all three solutions. Each architecture change was a technical response to an organizational problem. Until the alignment issue was addressed directly, no architecture would succeed.

## Conclusion

The cycle of build-fail-replace could have been broken at Solution 2. Not because Solution 2 was good, but because it hadn't painted itself into a corner. The architecture was simple enough to fix, extend, or partially replace. Instead, the organization invested in a more complex architecture that closed off those options.

Technical excellence matters, and Solution 3 had clean code and good tests. But technical excellence in service of the wrong pattern still fails. A flawed but flexible architecture can be iteratively improved. An overextended architecture requires starting over.

The path forward was always available: start with simple domain processors, measure actual needs, distribute only when proven necessary, and ensure observability from day one. Most importantly, address the organizational alignment that no architecture can fix.
