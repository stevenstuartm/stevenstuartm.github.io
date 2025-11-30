---
layout: guide
title: "Orchestration and Choreography Patterns"
category: Architecture
subcategory: Patterns
description: "Compare centralized orchestration vs distributed choreography for coordinating complex business processes across multiple services with trade-offs and implementation patterns."
tags: [architecture, design-patterns, distributed-systems, microservices, workflow, transactions]
---

These patterns define how multiple services coordinate to complete complex business processes, either through centralized control (orchestration) or distributed coordination (choreography).

## Orchestration Pattern

<blockquote class="pull-quote">
<p>Centralized orchestration provides visibility and control at the cost of creating a coordination bottleneck.</p>
</blockquote>

Centralized approach where a single orchestrator service controls and coordinates the execution of multiple services in a specific sequence.

**Use When**:
- Need centralized control over business processes
- Complex workflows with multiple steps
- Require transaction-like behavior across services
- Need detailed workflow monitoring and error handling

**Considerations**:

- Orchestrator can become a single point of failure
- Risk of creating a distributed monolith
- May introduce performance bottlenecks

**Example**: Order fulfillment process where an orchestrator coordinates payment processing, inventory reservation, shipping arrangement, and customer notification in sequence.

```
Order Orchestrator:
  1. Call Payment Service → Wait for response
  2. If success, call Inventory Service → Wait for response
  3. If success, call Shipping Service → Wait for response
  4. If success, call Notification Service
  5. If any fail, execute compensation logic
```

**Implementation**: AWS Step Functions | Temporal | Camunda | Custom orchestrator

---

## Choreography Pattern

Distributed approach where each service knows when to act and what to do without central coordination, typically through event-driven communication.

**Use When**:
- Services can operate independently
- Don't need strict workflow control
- Want maximum decoupling between services
- Building event-driven architectures

**Considerations**:

- Difficult to monitor and debug workflows
- Complex error handling and compensation
- No central view of the business process

**Example**: E-commerce system where placing an order triggers events that cause inventory, payment, and shipping services to act independently without central coordination.

```
Order Service → OrderCreated event → Event Bus
                                         ↓
          ┌──────────────┬──────────────┼──────────────┐
          ↓              ↓              ↓              ↓
    Inventory      Payment         Shipping      Notification
    Service        Service         Service        Service
```

**Implementation**: Event brokers (Kafka, RabbitMQ, AWS EventBridge)

---

## Saga Pattern

*Pattern introduced by Hector Garcia-Molina and Kenneth Salem (1987), popularized for microservices by Chris Richardson and others*

Manages distributed transactions by breaking them into a series of local transactions, each with a compensating transaction to undo changes if the saga fails. Provides eventual consistency without requiring distributed ACID transactions.

**Use When**:
- Need to maintain consistency across multiple services
- Services have separate databases (Database-per-Service pattern)
- Cannot use distributed transactions (2PC/XA)
- Long-running business processes
- Microservices architecture

**Key Concepts**:

- **Compensating transactions**: Actions that semantically undo previous steps (not always true rollback)
- **Semantic lock**: Resources are locked for the saga duration through business logic, not database locks
- **Trade-off**: Eventual consistency instead of immediate consistency

**Implementation Approaches**:

**Orchestration-based Saga**: Central coordinator (saga orchestrator) manages the saga

```
Saga Orchestrator:
  1. Reserve flight → Success
  2. Reserve hotel → Success
  3. Reserve car → Failed
  4. Compensate: Cancel hotel reservation
  5. Compensate: Cancel flight reservation
  6. Return failure to user
```

*Pros*: Centralized logic, easy to monitor, clear workflow
*Cons*: Orchestrator is single point of coupling

**Choreography-based Saga**: Services coordinate through events

```
Book Flight → FlightReserved event
           → Book Hotel → HotelReserved event
                       → Book Car → CarReservationFailed event
                                 → HotelCancelled event
                                 → FlightCancelled event
```

*Pros*: Loose coupling, no central coordinator
*Cons*: Hard to understand workflow, difficult to debug

**Example**: Travel booking saga that reserves flight, hotel, and car rental. If any step fails, compensating transactions cancel previous reservations.

**Important**: Compensating transactions must be idempotent since they may be retried.

---

<div class="callout callout--tip">
<p class="callout__title">Choosing Between Patterns</p>
<p>Use orchestration when you need visibility into complex workflows and centralized error handling. Use choreography when service independence and loose coupling are more important than workflow visibility.</p>
</div>

## Quick Reference

### Pattern Comparison

| Pattern | Control | Coupling | Monitoring | Use Case |
|---------|---------|----------|------------|----------|
| **Orchestration** | Centralized | Medium-High | Easy | Complex workflows, strict control |
| **Choreography** | Distributed | Low | Difficult | Independent services, loose coupling |
| **Saga** | Either | Varies | Medium | Distributed transactions |

### Decision Framework

**Need strict workflow control?** → Orchestration
**Want loose coupling?** → Choreography
**Need distributed transactions?** → Saga (choose orchestration or choreography based on other needs)

### Trade-offs

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Orchestration</h4>
<p><strong>Pros:</strong></p>
<ul>
<li>Easy to monitor workflows</li>
<li>Clear workflow visualization</li>
<li>Centralized error handling</li>
</ul>
<p><strong>Cons:</strong></p>
<ul>
<li>Single point of failure</li>
<li>Potential bottleneck</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Choreography</h4>
<p><strong>Pros:</strong></p>
<ul>
<li>Loose coupling</li>
<li>No single point of failure</li>
<li>High scalability</li>
</ul>
<p><strong>Cons:</strong></p>
<ul>
<li>Hard to monitor</li>
<li>Complex debugging</li>
<li>No workflow visibility</li>
</ul>
</div>
</div>

<div class="callout callout--note">
<p class="callout__title">Saga Pattern</p>
<p><strong>Pros:</strong> Maintains consistency without distributed transactions</p>
<p><strong>Cons:</strong> Complexity of compensating actions, eventual consistency</p>
</div>

---
