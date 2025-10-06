---
layout: guide
title: "Performance and Scalability Patterns"
category: Architecture
subcategory: Patterns
description: "Optimize system performance and scale with patterns for caching, throttling, load shedding, horizontal/vertical scaling, and partitioning strategies."
---

# Performance and Scalability Patterns

These patterns optimize system performance, handle increased load, and ensure systems can scale efficiently as demand grows.

## Throttling and Rate Limiting

Controls the rate of requests to prevent system overload and ensure fair resource usage.

**Use When**:
- Protecting against traffic spikes
- Ensuring fair usage among clients
- Preventing abuse or DDoS attacks
- Managing resource costs

**Implementation Strategies**:

- **Token Bucket**: Allows bursts up to bucket capacity
- **Fixed Window**: Limits requests per time window
- **Sliding Window**: More accurate than fixed window
- **Leaky Bucket**: Smooth request rate

**Example**: API gateway limiting each API key to 1000 requests per hour, with burst allowance of 100 requests per minute.

```
Client → API Gateway (Rate Limiter) → Backend
  Request 1-100: ALLOWED (burst)
  Request 101-1000: ALLOWED (within hourly limit)
  Request 1001: REJECTED (429 Too Many Requests)
```

---

## Cache-Aside

Application manages cache explicitly, loading data from cache first and falling back to database if not found.

**Use When**:
- Need fine-grained control over caching
- Cache and database can become inconsistent temporarily
- Read-heavy workloads with predictable access patterns

**How It Works**:

1. Check cache for data
2. If cache miss, load from database
3. Store data in cache for future requests
4. Handle cache invalidation on updates

**Example**: User profile service that checks Redis cache first, loads from PostgreSQL on cache miss, and stores result in cache.

```
GET /user/123:
  1. Check Redis for user:123
  2. If miss, query PostgreSQL
  3. Store in Redis with TTL
  4. Return to client

UPDATE /user/123:
  1. Update PostgreSQL
  2. Invalidate Redis cache for user:123
```

---

## Cache-Through

Cache sits between application and database, automatically loading and storing data.

**Use When**:
- Want automatic cache management
- Can tolerate cache-through latency
- Prefer consistency over performance

**Example**: Application server with cache-through layer that automatically manages product catalog caching between application and database.

```
Application → Cache Layer → Database
  Read: Cache handles fetching from DB if not cached
  Write: Cache handles updating both cache and DB
```

---

## Sharding

Horizontally partitions data across multiple database instances based on a sharding key.

**Use When**:
- Single database cannot handle load
- Data set is too large for one server
- Need to scale beyond vertical limits

**Sharding Strategies**:

- **Range-based**: Partition by value ranges
- **Hash-based**: Use hash function on sharding key
- **Directory-based**: Lookup service maps keys to shards

**Challenges**:
- Complex queries across shards
- Rebalancing when adding/removing shards
- Handling hot spots

**Example**: Social media platform sharding user data by user ID hash, distributing users evenly across database shards.

```
User ID 1234 → hash(1234) % 4 = 2 → Shard 2
User ID 5678 → hash(5678) % 4 = 1 → Shard 1
User ID 9012 → hash(9012) % 4 = 0 → Shard 0
```

---

## Quick Reference

### Pattern Comparison

| Pattern | Purpose | Complexity | Performance Gain |
|---------|---------|------------|-----------------|
| **Throttling** | Prevent overload | Low | N/A (protection) |
| **Cache-Aside** | Reduce DB load | Low | High for reads |
| **Cache-Through** | Simplify caching | Low | Medium for reads |
| **Sharding** | Horizontal scaling | High | High for reads/writes |

### Decision Tree

**Protecting against overload?** → Throttling and Rate Limiting
**Read-heavy workload?** → Cache-Aside or Cache-Through
**Single DB can't handle load?** → Sharding
**Need fine-grained cache control?** → Cache-Aside
**Want simple cache management?** → Cache-Through

### Cache Strategies

**Cache-Aside** (Lazy Loading):
- **Pros**: Only cache what's needed, simple to implement
- **Cons**: Cache misses impact performance, manual invalidation

**Cache-Through** (Write-Through):
- **Pros**: Data always in cache, simpler application code
- **Cons**: Every write pays cache penalty, unused data cached

### Sharding Considerations

**Range-based**: Easy to implement, risk of hot spots
**Hash-based**: Even distribution, complex range queries
**Directory-based**: Flexible, additional lookup overhead

---
