---
layout: guide
title: "Event-Driven Architecture"
category: Architecture
subcategory: Styles
description: "Asynchronous event-based architecture enabling responsiveness, decoupling, and scalability through event brokers and reactive processors."
tags: [architecture, distributed-systems, messaging, scalability, async, practical]
---

Event-driven architecture organizes a system around asynchronous event broadcasts. Components publish events representing things that happened ("order placed," "payment processed," "inventory depleted"). Other components listen for events they care about and react accordingly. There's no direct coupling between event publishers and subscribers.

This architecture enables high responsiveness, complex workflows with many independent reactions, and systems that must handle unpredictable, variable workloads.

## How It Works

An event broker sits at the center, receiving events from publishers and routing them to subscribers. When something significant happens in one part of the system, it publishes an event. The broker broadcasts the event to all interested subscribers. Each subscriber processes the event independently and may publish new derived events in response.

For example, an "order placed" event might trigger inventory reservation, payment processing, and shipping notification, all happening asynchronously and independently. Each processor does its work and publishes new events ("inventory reserved," "payment captured") that other processors might react to.

### Core Components

**Event Producers**: Components that detect significant occurrences and publish events. These can be user actions (button clicks), system events (scheduled tasks), or domain events (state changes).

**Event Broker**: Infrastructure that receives events and routes them to subscribers. Can be a message queue (RabbitMQ, AWS SQS), event stream (Kafka, AWS Kinesis), or pub/sub service (Google Pub/Sub, AWS SNS).

**Event Consumers/Processors**: Components that subscribe to specific event types and react. Each processor runs independently, processes the event, performs its logic, and potentially publishes new events.

**Event Store** (optional): Persistent log of all events for auditing, replay, or event sourcing patterns.

## Events vs Messages

This distinction is fundamental and often misunderstood.

**Events** announce what happened and are informational, not prescriptive. "Inventory depleted" is an event. It states a fact. The publisher doesn't know or care who reacts. Multiple subscribers might react in different ways: one might trigger reordering, another might send alerts, and a third might update analytics.

**Messages** command what should happen. "Replenish inventory" is a message. It's prescriptive. The sender expects specific action from a specific receiver. Messages create tighter coupling because the sender knows about the receiver and expects particular behavior.

Event-driven architectures use events. Publishers broadcast facts. Subscribers independently decide how to react. This maximizes decoupling.

## Architectural Patterns

### Choreographed Event-Driven

No central coordinator exists; events broadcast freely and processors react independently. Workflows emerge from the collective reactions of independent processors.

**How it works**: The Order Service publishes an "OrderPlaced" event. The Inventory Service subscribes, reserves stock, and publishes a "StockReserved" event. The Payment Service subscribes, processes payment, and publishes a "PaymentCaptured" event. The Shipping Service subscribes to both events, waits for both, then publishes a "ShipmentScheduled" event.

**Advantages**: Maximum decoupling. Services don't know about each other. Easy to add new reactions (subscribe to events). No single point of failure. Highly scalable.

**Tradeoffs**: Workflows are hard to trace and debug. No single view shows the complete workflow. Understanding what happens when an event publishes requires examining all subscribers. Error handling is complex. If one processor fails, how do others know? State management is distributed.

**When to use**: Complex workflows with many independent reactions. Systems where new reactions are frequently added. Domains where loose coupling matters more than workflow visibility.

### Mediated Event-Driven

An orchestrator controls workflow. It receives events, makes decisions based on state, and triggers subsequent actions. The orchestrator knows the complete workflow and coordinates processors.

**How it works**: Order orchestrator receives "OrderPlaced" event. It calls Inventory Service to reserve stock. After success, it calls Payment Service to capture payment. After both succeed, it calls Shipping Service to schedule shipment.

**Advantages**: Central workflow visibility. Easy to understand and debug. State management is centralized. Error handling is explicit. Can implement complex conditional logic, timeouts, and retries.

**Tradeoffs**: Reintroduces coupling. The orchestrator knows about all services. Creates a potential bottleneck. Orchestrator becomes a single point of failure unless highly available. Reduces system flexibility because adding new reactions requires changing the orchestrator.

**When to use**: Workflows requiring central control and visibility. Systems where error handling and retry logic are complex. Domains where workflow understanding and debugging matter more than maximum decoupling.

## Event Payload Strategies

### Data-Based Events

Events include all relevant data in the payload. An "OrderPlaced" event contains customer details, order items, prices, and addresses: everything needed to process the order.

**Advantages**:
- Subscribers process events immediately without additional queries
- Resilient (subscribers don't depend on other services being available)
- Fast (no network calls to fetch data)
- Works well offline or with eventual connectivity

**Tradeoffs**:
- Brittle (changing data structures breaks subscribers)
- Data duplication across events and subscribers
- Large event payloads consume bandwidth and storage
- Events contain data that not all subscribers need

**When to use**: High availability requirements, subscribers need complete data, network latency matters, subscribers should work even if source systems are down.

### Key-Based Events

Events include only identifiers. An "OrderPlaced" event contains the order ID. Subscribers query for full data when needed.

**Advantages**:
- Stable contracts (IDs rarely change)
- Small event payloads
- Data consistency (subscribers always fetch current data)
- Subscribers get only data they need

**Tradeoffs**:
- Slower (requires additional queries)
- Creates runtime dependencies on source services
- Higher latency
- Subscribers fail if source services are unavailable

**When to use**: Data changes frequently, consistency matters more than speed, event payloads would be very large, source services are highly available.

## Characteristics

| Characteristic | Rating | Notes |
|----------------|--------|-------|
| **Simplicity** | ⭐⭐ | Asynchronous workflows are harder to reason about |
| **Scalability** | ⭐⭐⭐⭐⭐ | Excellent horizontal scaling, decoupled components |
| **Evolvability** | ⭐⭐⭐⭐ | Easy to add new reactions, harder to change events |
| **Deployability** | ⭐⭐⭐⭐ | Independent deployment of processors |
| **Testability** | ⭐⭐ | Difficult to test complete workflows |
| **Performance** | ⭐⭐⭐⭐⭐ | High responsiveness, asynchronous processing |
| **Fault Tolerance** | ⭐⭐⭐⭐ | Failures isolated to individual processors |

## When Event-Driven Architecture Fits

**Systems requiring high responsiveness**: Actions must happen quickly without waiting for synchronous processing. Users submit requests and get immediate confirmation. Processing happens asynchronously in the background.

**Complex workflows with many independent reactions to the same trigger**: When one event triggers multiple unrelated actions. User registration triggers: welcome email, analytics tracking, account provisioning, onboarding workflow, CRM record creation. These can all happen independently.

**Domains with unpredictable, variable workloads**: Asynchronous processing smooths demand spikes. Events queue up during high load. Processors work through the backlog at sustainable pace. The system remains responsive even under load.

**Systems where loose coupling is critical**: When parts of the system change frequently or when you need to add new capabilities without modifying existing components. Event-driven architecture enables this through the subscribe/publish pattern.

**IoT and real-time data processing**: Sensors publish events constantly. Multiple systems need to react (storage, analytics, alerting). Event-driven architecture handles high-volume streaming data naturally.

## When to Avoid Event-Driven Architecture

**Applications with deterministic workflows where certainty and control matter more than flexibility**: Financial transactions requiring strong consistency. Workflows where each step must complete before the next begins. Processes where audit trails must show exact ordering.

**Systems where understanding and debugging workflows is critical**: Regulated environments requiring clear workflow documentation. Domains where workflow changes require regulatory approval. Systems where debugging production issues must be straightforward.

**Teams without experience managing eventual consistency and distributed state**: Event-driven systems are eventually consistent. Different processors might temporarily see different state. If the team doesn't understand these challenges, they'll create data consistency bugs.

**Simple workflows that don't benefit from asynchronous processing**: If the workflow is linear with few steps, synchronous request/response is simpler. Don't add event-driven complexity unless you need its benefits.

## Common Pitfalls

**Nondeterministic side effects**: Events trigger unpredictable numbers of reactions. You publish an event expecting three reactions but ten occur. Or two reactions interfere with each other. Solution: Make processors idempotent. Document expected reactions. Monitor actual behavior.

**Static coupling via contracts**: Changing event structure breaks subscribers. Event evolution requires coordinating all subscribers. Solution: Version events. Support multiple event versions during transitions. Use flexible schemas (add fields, don't remove).

**Too much synchronous communication between processors**: Processors make synchronous calls to each other, defeating the asynchronous purpose. You've built a distributed monolith with event broker overhead. Solution: Processors should be fully independent. If they need data from others, subscribe to those events and maintain local copies.

**Difficult state management**: No single component knows the full system state. Debugging why something happened requires tracing event chains across multiple processors. Solution: Implement distributed tracing. Use correlation IDs on events. Maintain event stores for replay and auditing.

**Event storms**: A single event triggers cascades of derived events. The system bogs down processing events. Solution: Be selective about what warrants an event. Implement circuit breakers. Monitor event volumes.

## Evolution and Alternatives

When event-driven architecture stops fitting:

**Add workflow orchestration**: If choreography becomes too complex to understand and debug, introduce orchestrators for critical workflows while keeping event-driven patterns for independent reactions.

**Hybrid with synchronous services**: Use event-driven architecture for asynchronous workflows and independent reactions. Use synchronous services for queries and transactional operations. Many systems combine both.

**Implement CQRS and Event Sourcing**: If state management becomes problematic, fully commit to event sourcing. Store events as the source of truth. Build read models from events. This embraces the event-driven model completely.

For more architectural style options, see the [Architecture Styles](/study-guides/architecture/ArchitectureStyles.html) overview.
