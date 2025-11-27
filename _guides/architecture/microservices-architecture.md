---
layout: guide
title: "Microservices Architecture"
category: Architecture
subcategory: Styles
description: "Fine-grained distributed architecture maximizing evolvability and independence through bounded contexts and service isolation."
tags: [architecture, distributed-systems, microservices, scalability, domain-driven-design, practical]
---

Microservices architecture, popularized by Martin Fowler and James Lewis in 2014, takes distributed architecture to its logical extreme. The system splits into many fine-grained services, each representing a small, focused business capability. Each service owns its data, deploys independently, and can use different technologies. This maximizes evolvability and team autonomy but requires significant operational maturity.

## How It Works

Each microservice represents a bounded context from Domain-Driven Design: a cohesive business capability with clear boundaries. Services follow a "share nothing" philosophy. They don't share databases, libraries, or runtime dependencies. Communication happens exclusively through well-defined APIs (REST, gRPC, messaging).

The architecture emphasizes independent deployability. Each service can deploy without coordinating with other services. Teams can release changes frequently without waiting for orchestrated release windows.

### Core Principles

**Bounded Context Alignment**: Each microservice maps to a bounded context. The service boundary is the context boundary. Everything needed to fulfill the context's responsibility lives within the service.

**Data Isolation**: Each service has its own database (Database-per-Service pattern). No shared databases. No direct database access across services. This eliminates coupling through shared schemas but creates challenges for queries spanning multiple services.

**Independent Deployability**: Services deploy independently. A change to Service A doesn't require deploying Service B. This enables continuous deployment and reduces deployment risk.

**Technology Diversity**: Services can use different languages, frameworks, and databases. Choose the best technology for each service's needs. The Order Service might use Java and PostgreSQL while the Analytics Service uses Python and MongoDB.

**Decentralized Governance**: No central architecture board approving technology choices. Teams make decisions for their services. Establish guardrails (security standards, observability requirements) but allow autonomy within those bounds.

## Service Granularity

How fine-grained should microservices be? No magic formula exists. Three factors guide sizing:

### Purpose

Does the service represent a cohesive business capability that a team can reason about and own? If the service does too much, split it. If multiple services must coordinate for every request, consolidate them.

A "Customer Service" handling registration, authentication, preferences, orders, and invoicing is too broad. Split into Authentication Service, Customer Profile Service, and Order History Service.

Conversely, if you have separate services for "Calculate Tax," "Apply Discount," and "Update Total" that must coordinate for every cart operation, they're too granular. Consolidate into a single Cart Service.

### Transactions

If services constantly need distributed transactions, they're too fine-grained. Microservices deliberately avoid distributed transactions (two-phase commit, XA protocols) because they couple services and reduce availability.

If you need cross-service transactions, two options exist:
1. **Fix service boundaries**: The services belong together. Merge them.
2. **Use Saga pattern**: Implement compensating transactions for eventual consistency.

Frequent need for cross-service transactions indicates wrong boundaries.

### Choreography

How much inter-service communication does a workflow require? The more services talk to each other, the more network latency, failure modes, and complexity you introduce.

If completing an order requires 15 service calls, you have too many services or wrong boundaries. Either consolidate services or rethink the workflow to reduce coordination.

High choreography (many services communicating to accomplish a task) suggests wrong boundaries. Services should be relatively independent, not constantly collaborating.

## Data Management

### Database-per-Service Pattern

Each service owns its database with complete data isolation. This is mandatory in microservices, not optional.

**Implementation approaches**:
- **Separate database instances**: Each service has its own database server
- **Separate schemas**: Services share a database server but use separate schemas with restricted access
- **Separate tables**: Services use separate tables with naming conventions and access controls

True isolation requires separate database instances, but separate schemas with enforced access controls can work pragmatically.

### Handling Queries Spanning Services

When you need data from multiple services:

**API Composition**: Query each service's API and aggregate results in the application layer. Simple but can be slow (multiple round trips) and complicated (partial failures).

**CQRS**: Maintain separate read models optimized for queries. Services publish events. Read model subscribers build query-optimized views that denormalize data across boundaries.

**Data Replication**: Services subscribe to events from other services and maintain local copies of needed data. Trades consistency for query performance.

### Transaction Management

Avoid distributed transactions. Use one of these patterns instead:

**Saga Pattern**: Break transactions into a series of local transactions with compensating actions. If a later step fails, execute compensating transactions to undo earlier steps.

**Eventual Consistency**: Accept that data will be temporarily inconsistent. Design workflows to tolerate this. Most business processes are naturally eventually consistent.

**Redesign Boundaries**: If you frequently need transactions across services, the boundaries are wrong. Reconsider what belongs together.

## Operational Patterns

### Sidecar Pattern

Each service deploys with a sidecar proxy handling operational concerns: monitoring, logging, circuit breaking, retries, service discovery, and distributed tracing.

The service doesn't implement these concerns. It makes simple calls to localhost. The sidecar handles the complexity.

**Advantages**: Separates business logic from operational concerns. Consistent operational capabilities across polyglot services. Upgradable without changing services.

**Tradeoffs**: More components to deploy and manage. Additional resource overhead per service.

### Service Mesh

A service mesh provides a unified control plane managing all sidecars consistently across hundreds or thousands of services.

**Examples**: Istio, Linkerd, Consul Connect

**Capabilities**:
- Traffic management (routing, load balancing, timeouts)
- Security (mTLS, access control)
- Observability (metrics, tracing, logging)
- Resilience (retries, circuit breakers, rate limiting)

**When needed**: When you have many services and managing operational concerns individually becomes unwieldy. Service meshes add complexity, so adopt them when the operational burden justifies it.

## Characteristics

| Characteristic | Rating | Notes |
|----------------|--------|-------|
| **Simplicity** | ⭐ | Distributed system complexity is high |
| **Scalability** | ⭐⭐⭐⭐⭐ | Independent scaling of services |
| **Evolvability** | ⭐⭐⭐⭐⭐ | Services evolve independently |
| **Deployability** | ⭐⭐⭐⭐⭐ | Continuous independent deployment |
| **Testability** | ⭐⭐ | Integration testing is complex |
| **Fault Tolerance** | ⭐⭐⭐⭐ | Failures isolated to individual services |
| **Cost** | ⭐ | High operational cost and infrastructure complexity |

## When Microservices Architecture Fits

**Large systems where different parts need different operational characteristics**: Some services need 99.99% availability while others tolerate downtime. Some need extreme scalability while others have minimal load. Microservices let you optimize each service independently.

**Organizations with mature DevOps practices**: Automated deployment pipelines, comprehensive observability, container orchestration, and sophisticated monitoring. Without this maturity, managing dozens of services becomes overwhelming.

**Teams organized by business domains who need true independence**: Each team owns services end-to-end. They can deploy without coordinating with other teams. Teams move at their own pace.

**Systems where evolvability matters more than simplicity**: When requirements change constantly and you need to evolve different parts of the system at different rates without affecting others.

**High-scale consumer applications**: Systems handling millions of users where different capabilities have wildly different scaling needs. Social feeds, recommendations, user profiles all scale differently.

## When to Avoid Microservices Architecture

**Simple domains where a modular monolith would suffice**: If the domain is straightforward and doesn't justify the operational complexity. Many systems that adopt microservices would be better served by well-structured monoliths.

**Organizations without operational maturity**: Managing distributed systems requires sophisticated tooling, monitoring, and processes. If you don't have mature CI/CD, observability, and incident response, microservices will overwhelm your team.

**Small teams that would spend more time on infrastructure than features**: If your team spends more time managing Kubernetes, service meshes, and observability than building business features, the architecture is wrong for your scale.

**Systems requiring frequent distributed transactions**: If your workflows constantly need strong consistency across services, you're fighting the architecture. Microservices embrace eventual consistency.

**Tight deadlines requiring fast delivery**: Building microservices takes longer than building monoliths initially. If speed to market matters most and you can refactor later, start with a monolith.

## Common Antipatterns

### Grains of Sand

Services become so fine-grained that operational overhead drowns out benefits. Managing hundreds of tiny services becomes harder than managing a monolith.

**Example**: Separate services for "Calculate Tax," "Validate Address," "Format Phone Number." These are functions, not services.

**Solution**: Services should represent cohesive business capabilities, not individual functions. If a service has only 2-3 operations and can't function independently, it's too small.

### Shared Libraries Breaking Bounded Contexts

Teams create shared libraries for "reuse." Services depend on these libraries. When libraries change, all dependent services must redeploy. You've lost independent deployability.

**Solution**: Duplicate code rather than share if the duplication maintains independence. Shared libraries are acceptable only for truly cross-cutting concerns (logging frameworks, telemetry SDKs) provided by the platform team, not domain logic.

### Distributed Monolith

Services depend so tightly on each other that they can't change independently. Every change requires coordinating deployments across multiple services. You have distributed system complexity without distributed system benefits.

**Symptoms**: Cascade deployments (must deploy A, then B, then C), services sharing databases, services sharing libraries, services making many synchronous calls to each other.

**Solution**: Redesign service boundaries. Services should be loosely coupled. Use asynchronous messaging for coordination. Accept eventual consistency.

### Chatty Communication

Services make many fine-grained calls to each other. Network latency kills performance. The system becomes slower than a monolith.

**Solution**: Coarsen APIs. Services should have coarse-grained interfaces that minimize round trips. Or cache frequently accessed data locally (accepting eventual consistency).

## Evolution and Alternatives

When microservices architecture stops fitting:

**Consolidate related services**: If you have too many services or wrong boundaries, merge related services. Your 50 microservices might become 15 larger services. This is service-based architecture.

**Return to modular monolith**: If operational complexity outweighs benefits and you don't actually need independent deployment, consolidate back to a modular monolith. Keep the domain boundaries as modules.

**Add orchestration for complex workflows**: If service choreography becomes unmanageable, introduce workflow orchestrators for critical flows while maintaining microservices for individual capabilities.

For more architectural style options, see the [Architecture Styles](/study-guides/architecture/ArchitectureStyles.html) overview.
