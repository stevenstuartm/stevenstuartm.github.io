---
layout: guide
title: "Architecture Styles"
category: Architecture
subcategory: Styles
---

# Architecture Styles

## Understanding Styles

An architecture style describes a system's topology and characteristics (both pros and cons).

**Styles define:**

- Component topology & organization
- Physical architecture (monolithic/distributed)
- Deployment patterns
- Communication methods
- Data topology

## Choosing a Style

### Decision Factors

**Understand first:**

- Domain requirements & workflows
- Architecture characteristics needed
- Data architecture constraints
- Deployment environment (on-prem/cloud/hybrid)
- Organizational factors (budget, politics, maturity)
- Team structure & capabilities

### Key Questions

1. **Monolith or distributed?** Single quantum vs multiple?
2. **Where should data live?** Single DB, domain DBs, or per-service?
3. **Sync or async?** Trade performance for reliability

**Default to synchronous; use asynchronous only when necessary.**

---

## Monolithic Styles

### Layered Architecture

**Topology**: Presentation → Business → Persistence → Database

**Key Concepts:**

- Technical partitioning by role
- Layers of isolation (closed layers)
- **Sinkhole antipattern**: Requests pass through without logic

**Use When:**

Small apps, tight budgets, starting point

**Avoid When:**

Large apps, high scalability needed

---

### Pipeline Architecture

**Topology**: Pipes (communication) + Filters (processing)

**Filters:**

Producer → Transformer → Tester → Consumer

**Key Concepts:**

- Unidirectional flow
- Compositional reuse
- Stateless, single-purpose filters

**Use When:**

ETL, ordered one-way processing, tight budgets

**Avoid When:**

Complex workflows, high scale, bidirectional communication

---

### Microkernel Architecture

**Topology**: Core system + Plug-ins

**Key Concepts:**

- **Core**: Minimal functionality (happy path)
- **Plug-ins**: Specialized processing, extensions
- **Registry**: Tracks available plug-ins
- Point-to-point or remote communication

**Risks:**

- Volatile core (should be stable)
- Plug-in dependencies (should only talk to core)

**Use When:**

Product-based apps, customization needed, domain variations

**Avoid When:**

High scalability required

---

### Modular Monolith

**Topology**: Single deployment, domain-partitioned modules

**Communication:**

- **Peer-to-peer**: Direct invocation (simple but risky)
- **Mediator**: Abstraction layer (decoupled)

**Risks:**

- Getting too big
- Excessive code reuse blurring boundaries
- Too much intermodule communication

**Use When:**

Tight budgets, new systems, domain-focused teams, DDD

**Avoid When:**

High operational characteristics needed, frequent technical changes

---

## Distributed Styles

### Service-Based Architecture

**Topology**: UI + Coarse-grained domain services (4-12) + Database

**Key Concepts:**

- Domain services with API facade → Business → Persistence
- Remote access via REST/messaging/RPC
- Flexible database topologies
- Can use API Gateway

**Data Options:**

- Monolithic database (most common)
- Domain databases
- Service-specific databases
- Use logical partitioning for schema changes

**Risks:**

- Too much interservice communication
- Too many services (>12)
- Excessive data sharing

**Use When:**

Pragmatic distributed architecture, domain teams

**Avoid When:**

Transactions across services needed

---

### Event-Driven Architecture

**Topology:**

Event broker + Event processors

**Flow:**

Initiating event → Processor → Derived events → More processors

**Key Concepts:**

- **Events vs Messages**: "I did this" vs "do this"
- **Choreographed**: No central coordinator (broadcast)
- **Mediated**: Orchestrator controls workflow
- Asynchronous fire-and-forget
- Broadcast one-to-many

**Event Payloads:**

- **Data-based**: All data in event (faster, brittle)
- **Key-based**: Only ID in event (consistent, slower)
- Avoid anemic events & Swarm of Gnats

**Data Topologies:**

- Monolithic (easiest, single point of failure)
- Domain databases (better fault tolerance)
- Dedicated per service (best isolation)

**Risks:**

- Nondeterministic side effects
- Static coupling via contracts
- Too much synchronous communication
- Difficult state management

**Use When:**

Flexible action-based events, high responsiveness, complex workflows

**Avoid When:**

Well-structured data requests, need certainty and control

---

### Microservices Architecture

**Topology:**

Fine-grained services + API layer + Distributed data

**Key Concepts:**

- **Bounded context**: DDD-inspired "share nothing"
- **Granularity**: Purpose, transactions, choreography guide sizing
- **Data isolation**: Each service owns data (Database-per-Service required)
- **Sidecar pattern**: Operational concerns (monitoring, circuit breakers)
- **Service mesh**: Unified control across sidecars

**Communication:**

- Protocol-aware heterogeneous interoperability
- Choreography (no mediator) or Orchestration (mediator)

**Transactions:**

- Avoid distributed transactions
- Fix granularity instead
- **Saga pattern**: Mediator with compensating transactions

**Risks:**

- **Grains of Sand**: Services too fine-grained
- Too much interservice communication
- Excessive data sharing
- Code reuse breaking bounded contexts

**Use When:**

High modularity/scalability/evolvability, domain teams, independent deployment

**Avoid When:**

Transactions across services needed, simple domains, small teams

---

### Orchestration-Driven SOA

**Topology:**

Service taxonomy + ESB/Orchestration engine

**Service Taxonomy:**

1. **Business**: Coarse-grained entry points
2. **Enterprise**: Fine-grained reusable building blocks
3. **Application**: One-off implementations
4. **Infrastructure**: Operational concerns

**Key Concepts:**

- Orchestration engine stitches services
- Message bus for integration
- Reuse philosophy (caused coupling problems)

**Historical Context:**

- Expensive resources led to reuse-at-all-costs
- Technical partitioning taken to extreme
- Mostly failed; lessons learned influenced modern styles

**Modern Use:**

ESBs for integration only (not full architecture)

**Risk:**

Accidental SOA antipattern

---

### Space-Based Architecture

**Topology:**

Processing units + Virtualized middleware + Data pumps/writers/readers

**Key Concepts:**

- **Removes database bottleneck**: In-memory data grids
- **Processing units**: App logic + in-memory cache
- **Virtualized middleware**:
  - Messaging grid: Routes requests
  - Data grid: Synchronizes caches
  - Processing grid: Orchestrates multi-unit requests
  - Deployment manager: Elastic scaling
- **Data pumps**: Async DB updates via messaging

**Caching Models:**

- **Replicated**: Fast, fault-tolerant, limited by size
- **Distributed**: Consistent, slower, single point of failure
- **Near-cache**: Hybrid (not recommended)

**Data Synchronization:**

- Eventual consistency
- Asynchronous updates
- Potential collisions with high update rates

**Risks:**

- Frequent database reads
- Data collisions during replication
- High data volumes
- Synchronization bottlenecks

**Use When:**

Extreme scalability/elasticity, variable unpredictable load

**Avoid When:**

Frequent cold starts, heavy archived data reads, low tolerance for eventual consistency
---

## Quick Comparison

| Style | Best For | Avoid When | Cost | Scalability |
|-------|----------|------------|------|-------------|
| **Layered** | Small apps, tight budgets | Large scalable systems | $ | 1 |
| **Pipeline** | ETL, one-way processing | Complex workflows | $ | 1 |
| **Microkernel** | Customizable products | High scalability | $ | 1 |
| **Modular Monolith** | Domain teams, DDD | High operational demands | $ | 1 |
| **Service-Based** | Pragmatic distributed | Cross-service transactions | $$ | 3 |
| **Event-Driven** | Responsiveness, scale | Deterministic workflows | $$$ | 4 |
| **Microservices** | Evolvability, independence | Simple domains, small teams | $$$$$ | 5 |
| **SOA** | Legacy integration | New architectures | $$$$ | 4 |
| **Space-Based** | Extreme scale, elasticity | Frequent DB reads | $$$$ | 5 |

---

## Summary

**Remember:**

Every style has trade-offs. Choose based on your context, constraints, and priorities.

**Decision Flow:**

1. Understand domain & characteristics
2. Determine monolith vs distributed
3. Choose data topology
4. Select communication pattern
5. Validate against constraints
