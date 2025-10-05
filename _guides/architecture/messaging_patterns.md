---
layout: guide
title: "Messaging Patterns"
category: Architecture
subcategory: Patterns
---

# Messaging Patterns

Messaging patterns ensure reliable, consistent, and efficient message handling in distributed systems.

## Transactional Outbox

Ensures reliable message publishing by storing messages in the same database transaction as business data, then publishing them separately.

**Use When**:
- Need to guarantee message publishing after data changes
- Cannot afford to lose messages
- Database and message broker are separate systems

**How It Works**:

1. Store business data and message in same transaction
2. Separate process reads outbox table and publishes messages
3. Mark messages as published after successful delivery

**Example**: Order service saves new orders and outbox events in same transaction, ensuring order notifications are always sent.

```sql
BEGIN TRANSACTION
  INSERT INTO orders (id, customer_id, total) VALUES (...)
  INSERT INTO outbox (message_type, payload) VALUES ('OrderCreated', {...})
COMMIT

-- Separate process
SELECT * FROM outbox WHERE published = false
PUBLISH to message broker
UPDATE outbox SET published = true WHERE id = ...
```

---

## Transactional Inbox

Ensures idempotent message processing by tracking processed messages in the database.

**Use When**:
- Messages might be delivered multiple times
- Processing must be idempotent
- Cannot afford duplicate processing

**Example**: Inventory service tracks processed order messages to prevent double inventory reduction if the same order message is delivered twice.

```sql
BEGIN TRANSACTION
  INSERT INTO inbox (message_id, processed_at) VALUES (...)
  -- If duplicate, INSERT fails
  UPDATE inventory SET quantity = quantity - order.quantity WHERE ...
COMMIT
```

---

## Claim Check

Stores large message payloads separately and sends only a reference (claim check) through the messaging system.

**Use When**:
- Message payloads are large (images, documents)
- Messaging system has size limitations
- Want to optimize message broker performance

**How It Works**:

1. Store large payload in external storage (S3, database)
2. Send message with reference ID
3. Receiver uses reference to retrieve actual payload

**Example**: Document processing system stores uploaded files in S3 and sends processing messages containing only the S3 key.

```
1. Upload document → S3 → returns key "doc-12345"
2. Send message: {type: "ProcessDocument", s3Key: "doc-12345"}
3. Receiver gets message → retrieves document from S3 using key
```

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
