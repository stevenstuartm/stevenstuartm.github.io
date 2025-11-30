---
layout: guide
title: "Messaging Patterns"
category: Architecture
subcategory: Patterns
description: "Reliable messaging patterns including transactional outbox/inbox, saga pattern, event sourcing, and message versioning for distributed systems."
tags: [architecture, design-patterns, messaging, reliability, distributed-systems, transactions]
---

Messaging patterns ensure reliable, consistent, and efficient message handling in distributed systems.

<blockquote class="pull-quote">
<p>The dual-write problem: Writing to a database AND message broker atomically isn't possible without distributed transactions.</p>
</blockquote>

## Transactional Outbox

*Pattern from Chris Richardson's Microservices Patterns (2018), solving the dual-write problem*

Ensures reliable message publishing by storing messages in the same database transaction as business data, then publishing them separately. Guarantees atomicity between database updates and message publishing.

**Problem Solved**: The dual-write problem. Writing to a database AND message broker atomically isn't possible without distributed transactions.

**Use When**:
- Need to guarantee message publishing after data changes
- Cannot afford to lose messages
- Database and message broker are separate systems
- Want to avoid distributed transactions (2PC)

**How It Works**:

1. Store business data and message in same database transaction (atomicity guaranteed)
2. Separate process (Message Relay) reads outbox table and publishes messages
3. Mark messages as published after successful delivery
4. Optional: Delete or archive old published messages

**Example**: Order service saves new orders and outbox events in same transaction, ensuring order notifications are always sent.

```sql
BEGIN TRANSACTION
  INSERT INTO orders (id, customer_id, total) VALUES (...)
  INSERT INTO outbox (message_type, payload, created_at) VALUES ('OrderCreated', {...}, NOW())
COMMIT

-- Separate Message Relay process (polling or CDC)
SELECT * FROM outbox WHERE published = false ORDER BY created_at
PUBLISH to message broker
UPDATE outbox SET published = true, published_at = NOW() WHERE id = ...
```

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Polling</h4>
<p>Periodically query outbox table</p>
<ul>
<li><strong>Pros:</strong> Simple to implement</li>
<li><strong>Cons:</strong> Adds latency</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Change Data Capture (CDC)</h4>
<p>Stream database changes in near real-time</p>
<ul>
<li><strong>Pros:</strong> Lower latency</li>
<li><strong>Cons:</strong> More complex setup</li>
</ul>
</div>
</div>

**Tools**: Debezium (CDC), custom polling service

---

## Transactional Inbox

*Complementary pattern to Transactional Outbox, ensuring idempotent message consumption*

Ensures idempotent message processing by tracking processed messages in the database. Prevents duplicate message processing even when messages are delivered multiple times (at-least-once delivery guarantee).

**Problem Solved**: Message brokers typically provide at-least-once delivery, meaning duplicates are possible. Without deduplication, the same message could be processed multiple times.

**Use When**:
- Messages might be delivered multiple times (at-least-once delivery)
- Processing must be idempotent
- Cannot afford duplicate processing (e.g., charging customer twice)
- Message broker doesn't guarantee exactly-once processing

**How It Works**:

1. Check if message_id exists in inbox table
2. If exists, skip processing (duplicate)
3. If new, process message and record in inbox atomically
4. Use unique constraint to prevent race conditions

**Example**: Inventory service tracks processed order messages to prevent double inventory reduction if the same order message is delivered twice.

```sql
BEGIN TRANSACTION
  -- This INSERT fails if duplicate (UNIQUE constraint on message_id)
  INSERT INTO inbox (message_id, processed_at) VALUES ('msg-12345', NOW())

  -- Only executes if INSERT succeeded (no duplicate)
  UPDATE inventory SET quantity = quantity - order.quantity WHERE product_id = ...
COMMIT
```

**Best Practice**: Keep inbox records for some retention period (days/weeks), then archive/delete to manage table size

---

## Claim Check

*Pattern from Enterprise Integration Patterns by Gregor Hohpe and Bobby Woolf (2003)*

Stores large message payloads separately and sends only a reference (claim check) through the messaging system. Named after the claim check system at coat check counters.

**Use When**:
- Message payloads are large (images, documents, videos)
- Messaging system has size limitations (e.g., Kafka default 1MB, SQS 256KB)
- Want to optimize message broker performance and reduce network traffic
- Large payloads would slow down message processing

**How It Works**:

1. Store large payload in external storage (S3, blob storage, database)
2. Send lightweight message with reference ID through message broker
3. Receiver uses reference to retrieve actual payload from storage
4. Optional: Delete payload after processing

**Example**: Document processing system stores uploaded files in S3 and sends processing messages containing only the S3 key.

```
1. Upload document → S3 → returns key "doc-12345"
2. Send message: {type: "ProcessDocument", s3Key: "doc-12345", bucket: "documents"}
3. Receiver gets message → retrieves document from S3 using key → processes
4. Optional: Delete S3 object after processing
```

<div class="callout callout--tip">
<p class="callout__title">Trade-offs</p>
<p><strong>Pros:</strong> Keeps messages small, works around broker limits, reduces memory usage</p>
<p><strong>Cons:</strong> Extra retrieval step, external storage dependency, consistency challenges (what if message succeeds but payload deleted?)</p>
</div>

---

## Dead Letter Queue

A queue for messages that cannot be processed successfully after multiple retry attempts.

**Use When**:
- Messages might fail processing due to various reasons
- Need to investigate processing failures
- Cannot afford to lose messages completely

**Example**: Email service moves undeliverable messages to dead letter queue for manual review and potential reprocessing.

```
Message → Process → Retry 1 → Retry 2 → Retry 3 → Dead Letter Queue
```

---

## Priority Queue

Processes messages based on priority levels rather than arrival order.

**Use When**:
- Messages have different priority levels
- Some operations are more time-sensitive
- Need to meet different SLA requirements

**Example**: Customer support system processes VIP customer messages before standard customer messages.

```
Priority 1 (VIP): [Msg A, Msg C] → Process immediately
Priority 2 (Standard): [Msg B, Msg D] → Process when Priority 1 empty
```

---

## Quick Reference

### Pattern Comparison

| Pattern | Purpose | Trade-off |
|---------|---------|-----------|
| **Transactional Outbox** | Guarantee message delivery | Additional storage, eventual consistency |
| **Transactional Inbox** | Prevent duplicate processing | Additional storage, unique constraint checks |
| **Claim Check** | Handle large payloads | Extra retrieval step, storage costs |
| **Dead Letter Queue** | Handle failures gracefully | Manual intervention needed |
| **Priority Queue** | Process urgent messages first | Starvation of low-priority messages |

### Decision Tree

**Need guaranteed delivery?** → Transactional Outbox
**Need to prevent duplicates?** → Transactional Inbox
**Message too large?** → Claim Check
**Messages failing repeatedly?** → Dead Letter Queue
**Different urgency levels?** → Priority Queue

---
