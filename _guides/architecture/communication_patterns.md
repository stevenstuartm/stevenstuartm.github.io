---
layout: guide
title: "Communication Patterns"
category: Architecture
subcategory: Patterns
description: "Essential patterns for distributed service communication including load balancing, pub/sub, request-reply, circuit breaker, and retry strategies."
---

# Communication Patterns

Communication patterns define how services and components interact in distributed systems.

## Load Balancing

Distributes incoming requests across multiple service instances to prevent any single instance from becoming overwhelmed.

**Use When**:
- Multiple instances of the same service exist
- Need to distribute traffic to prevent bottlenecks
- Want high availability through redundancy

**Common Algorithms**:

- **Round Robin**: Distributes requests sequentially across instances
- **Least Connections**: Routes to the instance with fewest active connections
- **Weighted Round Robin**: Assigns different weights to instances based on capacity
- **Sticky Sessions**: Routes requests from the same client to the same instance
- **Geographic**: Routes based on client location

**Example**: E-commerce with three web server instances. Load balancer receives requests and distributes them evenly, ensuring no single server is overloaded during peak shopping.

```
Client → Load Balancer → [Server 1, Server 2, Server 3]
```

---

## Publisher-Subscriber (Pub/Sub)

Asynchronous messaging pattern where publishers send messages to topics without knowing who will receive them, and subscribers listen to topics without knowing who sent messages.

**Use When**:
- Need asynchronous communication between services
- Want to broadcast events to multiple consumers
- Building event-driven architectures
- Need to scale message processing independently

**Delivery Mechanisms**:

- **Competing Consumers**: Each message consumed by only one subscriber
- **Fanout**: Each message delivered to all subscribers

**Example**: Order processing where placing an order publishes an event. Multiple services (inventory, payment, shipping, notifications) subscribe to order events and react accordingly.

```
Order Service → Order Topic → [Inventory Service, Payment Service, Shipping Service, Notification Service]
```

---

## Request-Response

Synchronous communication pattern where a client sends a request and waits for a response from the server.

**Use When**:
- Need immediate response from the server
- Operation requires confirmation before proceeding
- Implementing CRUD operations
- User interface needs real-time feedback

**Example**: User authentication service where a login request must return success/failure immediately to determine if the user can proceed.

```
Client → [Request] → Auth Service → [Response] → Client
```

**Trade-offs**: Simple to implement and understand, but tight coupling and potential for cascading failures.

---

## Event Streaming

Continuous flow of events that can be processed in real-time or stored for later processing.

**Use When**:
- Need real-time data processing
- Want to maintain event history
- Building analytics platforms
- Implementing event sourcing

**Example**: Financial trading platform where stock price changes are streamed continuously to update displays and trigger automated trading rules.

```
Stock Exchange → Event Stream → [Display Service, Trading Engine, Analytics Service]
```

**Key Characteristics**: Ordered events | Event replay capability | Multiple consumers | Durability

---

## Quick Reference

### Pattern Comparison

| Pattern | Sync/Async | Coupling | Use Case |
|---------|-----------|----------|----------|
| **Load Balancing** | Sync | Medium | Distribute traffic across instances |
| **Pub/Sub** | Async | Low | Broadcast events to multiple services |
| **Request-Response** | Sync | High | Immediate feedback required |
| **Event Streaming** | Async | Low | Real-time processing, event history |

### When to Choose

**Load Balancing**: Already using request-response, need to scale horizontally
**Pub/Sub**: Multiple services need to react to same event
**Request-Response**: User needs immediate confirmation
**Event Streaming**: Need event history and real-time processing

---
