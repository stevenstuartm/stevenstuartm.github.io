---
layout: guide
title: "Orchestration and Choreography Patterns"
category: Architecture
subcategory: Patterns
description: "Compare centralized orchestration vs distributed choreography for coordinating complex business processes across multiple services with trade-offs and implementation patterns."
---

# Orchestration and Choreography Patterns

These patterns define how multiple services coordinate to complete complex business processes, either through centralized control (orchestration) or distributed coordination (choreography).

## Orchestration Pattern

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

Manages distributed transactions by breaking them into a series of local transactions, each with a compensating action to undo changes if needed.

**Use When**:
- Need to maintain consistency across multiple services
- Services have separate databases
- Cannot use distributed transactions
- Long-running business processes

**Implementation Approaches**:

**Orchestration-based**: Central coordinator manages the saga

```
Saga Orchestrator:
  1. Reserve flight → Success
  2. Reserve hotel → Success
  3. Reserve car → Failed
  4. Compensate: Cancel hotel reservation
  5. Compensate: Cancel flight reservation
```

**Choreography-based**: Services coordinate through events

```
Book Flight → FlightReserved event
           → Book Hotel → HotelReserved event
                       → Book Car → CarReservationFailed event
                                 → HotelCancelled event
                                 → FlightCancelled event
```

**Example**: Travel booking saga that reserves flight, hotel, and car rental. If any step fails, compensating transactions cancel previous reservations.

---

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

**Orchestration**:
- **Pros**: Easy to monitor, clear workflow, centralized error handling
- **Cons**: Single point of failure, potential bottleneck

**Choreography**:
- **Pros**: Loose coupling, no single point of failure, high scalability
- **Cons**: Hard to monitor, complex debugging, no workflow visibility

**Saga**:
- **Pros**: Maintains consistency without distributed transactions
- **Cons**: Complexity of compensating actions, eventual consistency

---
