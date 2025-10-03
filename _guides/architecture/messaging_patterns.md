---
title: "Messaging Patterns"
category: Architecture
---

← [Back to Architecture Patterns Index](./README.md)

## Overview

Messaging patterns ensure reliable, consistent, and efficient message handling in distributed systems, addressing challenges like delivery guarantees, ordering, and failure handling.

## Table of Contents

- [Transactional Outbox](#transactional-outbox)
- [Transactional Inbox](#transactional-inbox)
- [Claim Check](#claim-check)
- [Dead Letter Queue](#dead-letter-queue)
- [Priority Queue](#priority-queue)

---

## Transactional Outbox

**What it is:** Ensures reliable message publishing by storing messages in the same database transaction as business data, then publishing them separately.

**Why use it:** Guarantees message delivery, maintains consistency between data and messages, and handles partial failures gracefully.

**When to use:**
- Need to guarantee message publishing after data changes
- Cannot afford to lose messages
- Database and message broker are separate systems

**How it works:**
1. Store business data and message in same transaction
2. Separate process reads outbox table and publishes messages
3. Mark messages as published after successful delivery

**Example:** Order service that saves new orders and outbox events in same transaction, ensuring order notifications are always sent.

## Transactional Inbox

**What it is:** Ensures idempotent message processing by tracking processed messages in the database.

**Why use it:** Prevents duplicate message processing, maintains data consistency, and handles message redelivery safely.

**When to use:**
- Messages might be delivered multiple times
- Processing must be idempotent
- Cannot afford duplicate processing

**Example:** Inventory service that tracks processed order messages to prevent double inventory reduction if the same order message is delivered twice.

## Claim Check

**What it is:** Stores large message payloads separately and sends only a reference (claim check) through the messaging system.

**Why use it:** Reduces message size, improves messaging system performance, and handles large payloads efficiently.

**When to use:**
- Message payloads are large (images, documents)
- Messaging system has size limitations
- Want to optimize message broker performance

**How it works:**
1. Store large payload in external storage (S3, database)
2. Send message with reference ID
3. Receiver uses reference to retrieve actual payload

**Example:** Document processing system that stores uploaded files in S3 and sends processing messages containing only the S3 key.

## Dead Letter Queue

**What it is:** A queue for messages that cannot be processed successfully after multiple retry attempts.

**Why use it:** Prevents message loss, enables manual investigation of failures, and maintains system flow despite processing issues.

**When to use:**
- Messages might fail processing due to various reasons
- Need to investigate processing failures
- Cannot afford to lose messages completely

**Example:** Email service that moves undeliverable messages to dead letter queue for manual review and potential reprocessing.

## Priority Queue

**What it is:** Processes messages based on priority levels rather than arrival order.

**Why use it:** Ensures critical messages are processed first, supports SLA requirements, and enables differentiated service levels.

**When to use:**
- Messages have different priority levels
- Some operations are more time-sensitive
- Need to meet different SLA requirements

**Example:** Customer support system that processes VIP customer messages before standard customer messages.

---

← [Back to Architecture Patterns Index](./README.md)