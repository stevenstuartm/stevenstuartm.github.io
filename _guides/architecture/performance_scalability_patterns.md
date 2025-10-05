---
title: "Performance and Scalability Patterns"
category: Architecture
---


## Overview

These patterns focus on optimizing system performance, handling increased load, and ensuring systems can scale efficiently as demand grows.

## Table of Contents

- [Throttling and Rate Limiting](#throttling-and-rate-limiting)
- [Cache-Aside](#cache-aside)
- [Cache-Through](#cache-through)
- [Sharding](#sharding)

---

## Throttling and Rate Limiting

**What it is:** Controls the rate of requests to prevent system overload and ensure fair resource usage.

**Why use it:** Prevents system overload, ensures service availability, and provides fair access to resources.

**When to use:**
- Protecting against traffic spikes
- Ensuring fair usage among clients
- Preventing abuse or DDoS attacks
- Managing resource costs

**Implementation strategies:**
- **Token bucket:** Allows bursts up to bucket capacity
- **Fixed window:** Limits requests per time window
- **Sliding window:** More accurate than fixed window
- **Leaky bucket:** Smooth request rate

**Example:** API gateway limiting each API key to 1000 requests per hour, with burst allowance of 100 requests per minute.

## Cache-Aside

**What it is:** Application manages cache explicitly, loading data from cache first and falling back to database if not found.

**Why use it:** Improves performance, reduces database load, and gives applications full control over caching logic.

**When to use:**
- Need fine-grained control over caching
- Cache and database can become inconsistent temporarily
- Read-heavy workloads with predictable access patterns

**How it works:**
1. Check cache for data
2. If cache miss, load from database
3. Store data in cache for future requests
4. Handle cache invalidation on updates

**Example:** User profile service that checks Redis cache first, loads from PostgreSQL on cache miss, and stores result in cache.

## Cache-Through

**What it is:** Cache sits between application and database, automatically loading and storing data.

**Why use it:** Simplifies application code, ensures cache consistency, and reduces cache management complexity.

**When to use:**
- Want automatic cache management
- Can tolerate cache-through latency
- Prefer consistency over performance

**Example:** Application server with cache-through layer that automatically manages product catalog caching between application and database.

## Sharding

**What it is:** Horizontally partitions data across multiple database instances based on a sharding key.

**Why use it:** Enables horizontal scaling, distributes load across multiple servers, and overcomes single database limitations.

**When to use:**
- Single database cannot handle load
- Data set is too large for one server
- Need to scale beyond vertical limits

**Sharding strategies:**
- **Range-based:** Partition by value ranges
- **Hash-based:** Use hash function on sharding key
- **Directory-based:** Lookup service maps keys to shards

**Challenges:**
- Complex queries across shards
- Rebalancing when adding/removing shards
- Handling hot spots

**Example:** Social media platform sharding user data by user ID hash, distributing users evenly across database shards.

---

