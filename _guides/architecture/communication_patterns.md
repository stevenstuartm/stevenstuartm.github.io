---
title: "Communication Patterns"
category: Architecture
---

## Overview

Communication patterns define how services and components interact with each other in distributed systems. These patterns are fundamental to building scalable and reliable architectures.

## Table of Contents

- [Load Balancing](#load-balancing)
- [Publisher-Subscriber (Pub/Sub)](#publisher-subscriber-pubsub)
- [Request-Response](#request-response)
- [Event Streaming](#event-streaming)

---

## Load Balancing

**What it is:** A pattern that distributes incoming requests across multiple service instances to prevent any single instance from becoming overwhelmed.

**Why use it:** Improves system availability, distributes load evenly, and enables horizontal scaling.

**When to use:**
- Multiple instances of the same service exist
- Need to distribute traffic to prevent bottlenecks
- Want to achieve high availability through redundancy

**Common algorithms:**
- **Round Robin:** Distributes requests sequentially across instances
- **Least Connections:** Routes to the instance with fewest active connections
- **Weighted Round Robin:** Assigns different weights to instances based on capacity
- **Sticky Sessions:** Routes requests from the same client to the same instance
- **Geographic:** Routes based on client location

**Example:** An e-commerce application with three web server instances. The load balancer receives requests and distributes them evenly, ensuring no single server is overloaded during peak shopping periods.

## Publisher-Subscriber (Pub/Sub)

**What it is:** An asynchronous messaging pattern where publishers send messages to topics without knowing who will receive them, and subscribers listen to topics without knowing who sent the messages.

**Why use it:** Decouples message producers from consumers, enables event-driven architectures, and supports scalable communication.

**When to use:**
- Need asynchronous communication between services
- Want to broadcast events to multiple consumers
- Building event-driven architectures
- Need to scale message processing independently

**Delivery mechanisms:**
- **Competing Consumers:** Each message is consumed by only one subscriber
- **Fanout:** Each message is delivered to all subscribers

**Example:** An order processing system where placing an order publishes an event. Multiple services (inventory, payment, shipping, notifications) subscribe to order events and react accordingly.

## Request-Response

**What it is:** A synchronous communication pattern where a client sends a request and waits for a response from the server.

**Why use it:** Simple to implement and understand, provides immediate feedback, and works well for operations requiring immediate results.

**When to use:**
- Need immediate response from the server
- Operation requires confirmation before proceeding
- Implementing CRUD operations
- User interface needs real-time feedback

**Example:** A user authentication service where a login request must return success/failure immediately to determine if the user can proceed.

## Event Streaming

**What it is:** Continuous flow of events that can be processed in real-time or stored for later processing.

**Why use it:** Enables real-time processing, supports event replay, and provides a complete audit trail.

**When to use:**
- Need real-time data processing
- Want to maintain event history
- Building analytics platforms
- Implementing event sourcing

**Example:** Financial trading platform where stock price changes are streamed continuously to update displays and trigger automated trading rules.

---

