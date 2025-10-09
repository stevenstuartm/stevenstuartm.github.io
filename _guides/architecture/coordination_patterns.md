---
layout: guide
title: "Coordination Patterns"
category: Architecture
subcategory: Patterns
description: "Distributed coordination patterns including leader election, distributed locks, consensus algorithms, and managing shared resources across multiple nodes."
---

# Coordination Patterns

Coordination patterns enable multiple distributed nodes to work together effectively, ensuring consistency, preventing conflicts, and managing shared resources.

## Leader Election

Selects one node from a group to coordinate activities or make decisions on behalf of the group.

**Use When**:
- Need single coordinator for distributed operations
- Preventing duplicate processing
- Coordinating resource access
- Managing distributed state

**Example**: Cluster of background job processors electing a leader to coordinate job distribution and prevent duplicate processing.

```
[Node 1 (Leader), Node 2 (Follower), Node 3 (Follower)]
↓
Leader distributes jobs: Node 2 → Job A, Node 3 → Job B
↓
If Leader fails, new election: Node 2 becomes Leader
```

**Common Implementations**: ZooKeeper | etcd | Consul | Raft consensus

---

## Distributed Lock

Coordinates access to shared resources across multiple distributed nodes to prevent conflicts. Provides mutual exclusion in distributed systems.

**Use When**:
- Multiple nodes might access same resource concurrently
- Need to prevent duplicate operations (e.g., sending duplicate emails)
- Coordinating updates to shared state
- Ensuring only one node performs a specific task

**Challenges**:

- **Lock holder failure**: Requires timeout/lease mechanism (lock expires automatically)
- **Network partitions**: Can cause split-brain scenarios (two nodes think they have lock)
- **Performance impact**: Distributed coordination adds latency
- **Deadlocks**: Possible if not carefully designed

**Key Properties**:

- **Mutual exclusion**: Only one node holds lock at a time
- **Deadlock-free**: Lock eventually released even if holder crashes
- **Fault tolerance**: Works despite node failures

**Example**: Multiple instances of order processing service using distributed lock to ensure only one instance processes each order.

```
Instance 1: Acquire lock(order-123, TTL=30s) → SUCCESS → Process order → Release lock
Instance 2: Acquire lock(order-123) → BLOCKED → Wait → Lock released → Acquire → Process next order

If Instance 1 crashes while holding lock → Lock expires after 30s → Instance 2 can acquire
```

**Common Implementations**:
- **Redis Redlock**: Distributed algorithm using multiple Redis instances (proposed by Salvatore Sanfilippo)
- **ZooKeeper**: Ephemeral nodes for locks
- **etcd**: Lock API with TTL
- **Consul**: Session-based locks

**Warning**: Distributed locks are complex. Consider using message queues or database constraints when possible.

---

## Consensus

Ensures multiple nodes agree on a value or decision, even in the presence of failures. Fundamental building block for distributed systems requiring strong consistency.

**Use When**:
- Need strong consistency guarantees
- Handling mission-critical decisions
- Implementing distributed databases (etcd, Consul, CockroachDB)
- Building fault-tolerant systems with replicated state

**Common Algorithms**:

**Paxos** (*Leslie Lamport, 1989*):
- Classic consensus algorithm, notoriously difficult to understand
- Proven correct, widely studied
- Used in Google Chubby, Apache Cassandra (variant)

**Raft** (*Diego Ongaro & John Ousterhout, 2013*):
- Designed to be more understandable than Paxos
- Leader-based with strong consistency
- Clear leader election, log replication, safety guarantees
- Used in etcd, Consul, CockroachDB
- Majority (quorum) required for decisions

**PBFT - Practical Byzantine Fault Tolerance** (*Castro & Liskov, 1999*):
- Tolerates Byzantine failures (malicious/arbitrary behavior)
- Used in blockchain systems
- More expensive: 3f+1 nodes needed to tolerate f failures

**Example**: Distributed database using Raft consensus to ensure all replicas agree on transaction ordering and committed state.

```
Client → Write request → Leader
Leader → Propose to followers → [Follower 1, Follower 2]
Majority (2 of 3) agrees → Commit to log → Acknowledge client
```

**CAP Theorem Consideration**: Consensus algorithms choose **Consistency + Partition Tolerance** over Availability during network partitions

**Trade-offs**:
- **Pros**: Strong consistency, proven correctness, fault tolerance
- **Cons**: Lower availability during network partitions, performance overhead, requires quorum

---

## Quick Reference

### Pattern Comparison

| Pattern | Purpose | Consistency | Complexity |
|---------|---------|-------------|------------|
| **Leader Election** | Designate coordinator | Eventual | Medium |
| **Distributed Lock** | Prevent concurrent access | Strong | Medium |
| **Consensus** | Agree on values | Strong | High |

### When to Choose

**Leader Election**: Need coordinator but can tolerate brief periods without one
**Distributed Lock**: Need to prevent concurrent access to critical resources
**Consensus**: Need all nodes to agree on critical decisions

### Implementation Tools

**ZooKeeper**: All three patterns
**etcd**: All three patterns
**Redis**: Distributed lock (Redlock)
**Consul**: Leader election, distributed lock
**Raft libraries**: Consensus

---
