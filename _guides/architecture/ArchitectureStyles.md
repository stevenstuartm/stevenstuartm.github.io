---
layout: guide
title: "Architecture Styles"
category: Architecture
subcategory: Styles
description: "Comprehensive guide to architectural styles from monolithic layered and pipeline to distributed microservices, event-driven, and space-based architectures."
---

# Architecture Styles

An architecture style describes a system's topology and characteristics (both pros and cons).

**Styles define**: Component topology | Physical architecture (monolithic/distributed) | Deployment patterns | Communication methods | Data topology

## Choosing a Style

**Understand first**:

- Domain requirements & workflows
- Architecture characteristics needed
- Data architecture constraints
- Deployment environment (on-prem/cloud/hybrid)
- Organizational factors (budget, politics, maturity)
- Team structure & capabilities

**Key Questions**:

1. **Monolith or distributed?** Single quantum vs multiple?
2. **Where should data live?** Single DB, domain DBs, or per-service?
3. **Sync or async?** Trade performance for reliability

**Default to synchronous; use asynchronous only when necessary.**

---

## Monolithic Styles

### Layered Architecture

**Topology**: Presentation → Business → Persistence → Database

**Key Concepts**:

- Technical partitioning by role
- Layers of isolation (closed layers)
- **Sinkhole antipattern**: Requests pass through without logic

**Use When**: Small apps, tight budgets, starting point
**Avoid When**: Large apps, high scalability needed

### Pipeline Architecture

**Topology**: Pipes (communication) + Filters (processing)

**Filters**: Producer → Transformer → Tester → Consumer

**Key Concepts**:

- Unidirectional flow
- Compositional reuse
- Stateless, single-purpose filters

**Use When**: ETL, ordered one-way processing, tight budgets
**Avoid When**: Complex workflows, high scale, bidirectional communication

### Microkernel Architecture

*Also known as Plug-in Architecture*

**Topology**: Core system + Plug-ins

**Key Concepts**:

- **Core**: Minimal functionality implementing the "happy path" or baseline behavior
- **Plug-ins**: Specialized processing, extensions, custom variations
- **Registry**: Tracks available plug-ins (can be simple as config file or runtime discovery)
- Communication: Point-to-point (in-process) or remote (separate deployment)

**Examples**: Eclipse IDE (plug-in based), product customization platforms, tax software with state-specific plug-ins

**Risks**: Volatile core (should be stable), Plug-in dependencies (should only talk to core, not each other)

**Use When**: Product-based apps, customization needed, domain variations
**Avoid When**: High scalability required

### Modular Monolith

**Topology**: Single deployment, domain-partitioned modules

**Communication**:

- **Peer-to-peer**: Direct invocation (simple but risky)
- **Mediator**: Abstraction layer (decoupled)

**Risks**: Getting too big, excessive code reuse blurring boundaries, too much intermodule communication

**Use When**: Tight budgets, new systems, domain-focused teams, DDD
**Avoid When**: High operational characteristics needed, frequent technical changes

---

## Distributed Styles

### Service-Based Architecture

**Topology**: UI + Coarse-grained domain services (4-12) + Database

**Key Concepts**:

- Domain services with API facade → Business → Persistence
- Remote access via REST/messaging/RPC
- Flexible database topologies
- Can use API Gateway

**Data Options**: Monolithic database (most common) | Domain databases | Service-specific databases

**Risks**: Too much interservice communication, too many services (>12), excessive data sharing

**Use When**: Pragmatic distributed architecture, domain teams
**Avoid When**: Transactions across services needed

### Event-Driven Architecture

**Topology**: Event broker + Event processors

**Flow**: Initiating event → Processor → Derived events → More processors

**Key Concepts**:

- **Events vs Messages**: "I did this" vs "do this"
- **Choreographed**: No central coordinator (broadcast)
- **Mediated**: Orchestrator controls workflow
- Asynchronous fire-and-forget
- Broadcast one-to-many

**Event Payloads**:

- **Data-based**: All data in event (faster, brittle)
- **Key-based**: Only ID in event (consistent, slower)

**Risks**: Nondeterministic side effects, static coupling via contracts, too much synchronous communication, difficult state management

**Use When**: Flexible action-based events, high responsiveness, complex workflows
**Avoid When**: Well-structured data requests, need certainty and control

### Microservices Architecture

*Popularized by Martin Fowler and James Lewis (2014), building on SOA and Domain-Driven Design principles*

**Topology**: Fine-grained services + API layer + Distributed data

**Key Concepts**:

- **Bounded context** (from DDD): Services follow "share nothing" philosophy within business boundaries
- **Granularity**: Purpose, transactions, choreography guide sizing (no magic formula)
- **Data isolation**: Each service owns its data (Database-per-Service pattern required)
- **Sidecar pattern**: Operational concerns (monitoring, circuit breakers) deployed alongside service
- **Service mesh**: Unified control plane managing sidecars (e.g., Istio, Linkerd)

**Transactions**:

- Avoid distributed transactions (2PC, XA) - they break independence
- Fix granularity if you need cross-service transactions
- **Saga pattern**: Use compensating transactions when needed (see Orchestration patterns)

**Risks**: **Grains of Sand antipattern** (services too fine-grained), too much interservice communication, excessive data sharing, code reuse breaking bounded contexts

**Use When**: High modularity/scalability/evolvability, domain teams, independent deployment
**Avoid When**: Transactions across services needed, simple domains, small teams

### Orchestration-Driven SOA

**Topology**: Service taxonomy + ESB/Orchestration engine

**Service Taxonomy**:

1. **Business**: Coarse-grained entry points
2. **Enterprise**: Fine-grained reusable building blocks
3. **Application**: One-off implementations
4. **Infrastructure**: Operational concerns

**Key Concepts**:

- Orchestration engine stitches services
- Message bus for integration
- Reuse philosophy (caused coupling problems)

**Modern Use**: ESBs for integration only (not full architecture)

**Risk**: Accidental SOA antipattern

### Space-Based Architecture

*Also called Tuple Space or Cloud Architecture Pattern*

**Topology**: Processing units + Virtualized middleware + Data pumps/writers/readers

**Key Concepts**:

- **Removes database bottleneck**: All active data in replicated in-memory data grids
- **Processing units**: Self-contained app logic + in-memory cache replica
- **Virtualized middleware**:
  - Messaging grid: Manages input requests and sessions
  - Data grid: Manages data replication across processing units
  - Processing grid: Manages distributed request processing
  - Deployment manager: Handles elasticity (spins up/down units)
- **Data pumps**: Async database updates via messaging (eventual consistency)

**Caching Models**:

- **Replicated**: All data copied to every processing unit (fast reads, fault-tolerant, limited by memory)
- **Distributed**: Data partitioned across units (consistent, slower, single point of failure if not replicated)
- **Near-cache**: Hybrid approach (adds complexity, generally not recommended)

**Examples**: Concert ticket sales, online auctions, financial trading platforms with variable load

**Risks**: Frequent database reads, data collisions during replication, high data volumes, synchronization bottlenecks

**Use When**: Extreme scalability/elasticity, variable unpredictable load
**Avoid When**: Frequent cold starts, heavy archived data reads, low tolerance for eventual consistency

---

## Quick Reference

### Style Comparison

| Style | Monolith/Distributed | Best For | Avoid When |
|-------|---------------------|----------|------------|
| **Layered** | Monolith | Small apps, tight budgets | Large scalable systems |
| **Pipeline** | Monolith | ETL, one-way processing | Complex workflows |
| **Microkernel** | Monolith | Customizable products | High scalability |
| **Modular Monolith** | Monolith | Domain teams, DDD | High operational demands |
| **Service-Based** | Distributed | Pragmatic distributed | Cross-service transactions |
| **Event-Driven** | Distributed | Responsiveness, scale | Deterministic workflows |
| **Microservices** | Distributed | Evolvability, independence | Simple domains, small teams |
| **SOA** | Distributed | Legacy integration | New architectures |
| **Space-Based** | Distributed | Extreme scale, elasticity | Frequent DB reads |

### Decision Flow

1. Understand domain & characteristics
2. Determine monolith vs distributed
3. Choose data topology
4. Select communication pattern
5. Validate against constraints

### Data Topology Options

**Monolithic Database**: Single shared database
- **Pros**: Simple, ACID transactions
- **Cons**: Tight coupling, bottleneck

**Domain Databases**: Database per domain
- **Pros**: Domain autonomy
- **Cons**: Cross-domain queries complex

**Service-Specific**: Database per service
- **Pros**: Maximum independence
- **Cons**: Most complex, no distributed transactions

---
