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

Distributes incoming requests across multiple service instances to prevent any single instance from becoming overwhelmed, improving availability, reliability, and scalability.

**Use When**:
- Multiple instances of the same service exist
- Need to distribute traffic to prevent bottlenecks
- Want high availability through redundancy
- Horizontal scaling required

**Common Algorithms**:

- **Round Robin**: Distributes requests sequentially across instances in circular order
  - *Simple, no state required, assumes equal capacity*
- **Weighted Round Robin**: Assigns different weights to instances based on capacity
  - *Example*: 2x capacity server gets 2x traffic
- **Least Connections**: Routes to the instance with fewest active connections
  - *Better for long-lived connections or varying request durations*
- **Least Response Time**: Routes to instance with fastest response time
  - *Requires health monitoring, adapts to performance*
- **IP Hash/Sticky Sessions**: Routes requests from the same client to the same instance
  - *Maintains session state, but can cause imbalance*
- **Geographic/Latency-based**: Routes based on client location or proximity
  - *Optimizes for network latency*

**Load Balancer Types**:
- **Layer 4 (Transport)**: Routes based on IP/port (TCP/UDP) - fast but limited routing logic
- **Layer 7 (Application)**: Routes based on HTTP headers, URLs, cookies - slower but flexible

**Example**: E-commerce with three web server instances. Load balancer receives requests and distributes them evenly, ensuring no single server is overloaded during peak shopping.

```
Client → Load Balancer → [Server 1, Server 2, Server 3]
```

**Common implementations**: NGINX, HAProxy, AWS ELB/ALB, Envoy

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

Continuous flow of events that can be processed in real-time or stored for later processing. Unlike Pub/Sub, event streams maintain a persistent, ordered log of events.

**Use When**:
- Need real-time data processing
- Want to maintain event history and replay capability
- Building analytics platforms
- Implementing event sourcing
- Multiple consumers need to process same events at different rates

**Key Characteristics**:
- **Ordered events**: Events maintain sequence within partitions
- **Event replay**: Can reprocess events from any point in time
- **Multiple consumers**: Each consumer tracks own position independently
- **Durability**: Events persisted to disk, not just in-memory
- **Retention**: Events stored for configurable time period (hours to forever)

**Stream vs Pub/Sub**:
- Pub/Sub: Message deleted after delivery to all subscribers (ephemeral)
- Event Streaming: Events retained and can be replayed (durable log)

**Example**: Financial trading platform where stock price changes are streamed continuously to update displays and trigger automated trading rules.

```
Stock Exchange → Event Stream (Kafka) → [Display Service, Trading Engine, Analytics Service]
                                       Each consumer maintains own offset
```

**Common implementations**: Apache Kafka, Amazon Kinesis, Apache Pulsar, Azure Event Hubs

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
