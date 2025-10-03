---
title: "Orchestration and Choreography Patterns"
category: Architecture
---

← [Back to Architecture Patterns Index](./README.md)

## Overview

These patterns define how multiple services coordinate to complete complex business processes, either through centralized control (orchestration) or distributed coordination (choreography).

## Table of Contents

- [Orchestration Pattern](#orchestration-pattern)
- [Choreography Pattern](#choreography-pattern)
- [Saga Pattern](#saga-pattern)

---

## Orchestration Pattern

**What it is:** A centralized approach where a single orchestrator service controls and coordinates the execution of multiple services in a specific sequence.

**Why use it:** Provides centralized control, easier error handling and monitoring, and clear workflow visibility.

**When to use:**
- Need centralized control over business processes
- Complex workflows with multiple steps
- Require transaction-like behavior across services
- Need detailed workflow monitoring and error handling

**Considerations:**
- Orchestrator can become a single point of failure
- Risk of creating a distributed monolith
- May introduce performance bottlenecks

**Example:** Order fulfillment process where an orchestrator coordinates payment processing, inventory reservation, shipping arrangement, and customer notification in sequence.

## Choreography Pattern

**What it is:** A distributed approach where each service knows when to act and what to do without central coordination, typically through event-driven communication.

**Why use it:** Promotes loose coupling, eliminates single points of failure, and enables better scalability.

**When to use:**
- Services can operate independently
- Don't need strict workflow control
- Want maximum decoupling between services
- Building event-driven architectures

**Challenges:**
- Difficult to monitor and debug workflows
- Complex error handling and compensation
- No central view of the business process

**Example:** E-commerce system where placing an order triggers events that cause inventory, payment, and shipping services to act independently without central coordination.

## Saga Pattern

**What it is:** Manages distributed transactions by breaking them into a series of local transactions, each with a compensating action to undo changes if needed.

**Why use it:** Ensures data consistency across multiple services without requiring distributed transactions (ACID).

**When to use:**
- Need to maintain consistency across multiple services
- Services have separate databases
- Cannot use distributed transactions
- Long-running business processes

**Implementation approaches:**
- **Orchestration-based:** Central coordinator manages the saga
- **Choreography-based:** Services coordinate through events

**Example:** Travel booking saga that reserves flight, hotel, and car rental. If any step fails, compensating transactions cancel previous reservations.

---

← [Back to Architecture Patterns Index](./README.md)