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

Coordinates access to shared resources across multiple distributed nodes to prevent conflicts.

**Use When**:
- Multiple nodes might access same resource
- Need to prevent duplicate operations
- Coordinating updates to shared state

**Challenges**:

- Lock holder failure requires timeout/lease mechanism
- Network partitions can cause split-brain scenarios
- Performance impact of distributed coordination

**Example**: Multiple instances of order processing service using distributed lock to ensure only one instance processes each order.

```
Instance 1: Acquire lock(order-123) → SUCCESS → Process order → Release lock
Instance 2: Acquire lock(order-123) → BLOCKED → Wait → Lock released → Process next order
```

**Common Implementations**: Redis (Redlock) | ZooKeeper | etcd

---

## Consensus

Ensures multiple nodes agree on a value or decision, even in the presence of failures.

**Use When**:
- Need strong consistency guarantees
- Handling mission-critical decisions
- Implementing distributed databases
- Building fault-tolerant systems

**Common Algorithms**:

- **Raft**: Leader-based consensus with strong consistency
- **PBFT**: Byzantine fault tolerant consensus
- **Paxos**: Classic consensus algorithm

**Example**: Distributed database using Raft consensus to ensure all replicas agree on transaction ordering and committed state.

```
Client → Write request → Leader
Leader → Propose to followers → [Follower 1, Follower 2]
Majority agrees → Commit → Acknowledge client
```

**Trade-offs**: Strong consistency | Lower availability during network partitions | Performance overhead

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
