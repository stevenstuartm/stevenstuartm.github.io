---
layout: post
title: "Caching Before Understanding"
date: 
description: "Most caching failures aren't technical—they're decisional. Teams cache before answering two fundamental questions: what's the data scope, and what's the data lifecycle? Without those answers, you're not optimizing. You're creating invisible infrastructure that will haunt you."
tags: [architecture, performance, caching, distributed-systems]
---

Something was slow, so someone added a cache. Six months later, nobody remembers it exists. The data it returns is sometimes wrong, but the bugs are intermittent and unreproducible. The cache has become invisible infrastructure—not in any architecture diagram, not in any deployment docs, just silently returning stale data.

This is how most caching failures happen. Not because caching is technically difficult, but because the decision to cache wasn't really a decision at all. It was an impulse. Someone felt something was slow, reached for the first performance tool that came to mind, and created a hidden private repository of state that nobody agreed to and nobody knows how to invalidate.

## The Accidental Cache

Caching has a friction problem, but the friction is in the wrong place. It's trivial to add a cache—a decorator here, a Redis call there, maybe a local dictionary that "just holds things for a bit." But it's painful to understand what's cached, painful to debug cache-related issues, and often impossible to find the cache that's causing problems.

The result is what I call the accidental cache: infrastructure that exists not because someone made a deliberate architectural decision, but because adding a cache was easier than understanding why something was slow. These caches share common characteristics:

- Nobody agreed to them
- Nobody remembers they exist
- Nobody knows how to invalidate them properly
- Nobody can find them when debugging

When you see cache-related bugs that nobody can reproduce, or data that's "sometimes wrong," or invalidation logic scattered across multiple services with no clear ownership—you're probably looking at accidental caches. They weren't designed. They accumulated.

## Two Questions Before Caching Anything

Before reaching for a caching solution, you need to answer two fundamental questions. Your answers determine whether caching makes sense at all, and if so, where to cache and how to invalidate.

### What Is the Data Scope?

Scope isn't about ownership—it's about specificity and nature. How narrowly or broadly is this data used?

**Specificity spectrum:**
- Person-specific (single user's preferences)
- Tenant-specific (organization configuration)
- App-specific (feature flags for this application)
- Global defaults (shared reference data)

**Nature spectrum:**
- Component-local (only this service uses it)
- Domain-wide (multiple services in this domain)
- Cross-domain (shared across bounded contexts)

The narrower the scope, the safer the cache. A person-specific cache has a single consumer, clear invalidation points (logout, explicit refresh), and limited blast radius when stale. A cross-domain cache serving global defaults? Now you need to coordinate invalidation across every consumer, each with different staleness tolerances you probably haven't asked about.

### What Is the Data Lifecycle?

How does this data change? The answer determines your invalidation strategy—or whether you need one at all.

**Immutable reference data:** Country codes, currency definitions, historical records. Cache aggressively with long TTLs. Invalidation is rare enough to handle manually or through deployments.

**Slowly-changing configuration:** Feature flags, tenant settings, pricing tiers. TTL-based expiration often works. The staleness budget is usually minutes to hours, and consumers can tolerate brief inconsistency.

**Volatile transactional state:** User balances, inventory counts, session data. Short TTLs or no caching at all. The staleness budget is seconds or less, and "eventual consistency" often means "wrong."

**Real-time derived data:** Leaderboards, dashboards, aggregations. Often better served by materialized views or streaming than by caching.

If you can't clearly identify where your data falls on this spectrum, you don't understand the use case well enough to cache it.

## The Dangerous Zone: Broad Scope Meets Short Lifecycle

Plot scope against lifecycle, and you'll find a dangerous quadrant: broad scope combined with short lifecycle. This is where caching causes the most pain.

Narrow scope with long lifecycle? Safe. Cache a user's timezone preference locally; it rarely changes and only they need it.

Broad scope with long lifecycle? Usually fine. Cache country code lookups globally; the data is immutable and everyone needs the same values.

Narrow scope with short lifecycle? Manageable. Cache a user's unread notification count; it changes frequently but the blast radius is small.

Broad scope with short lifecycle? Dangerous. Now you're caching volatile data that multiple consumers depend on, each with different expectations about freshness. Invalidation becomes coordination. Staleness complaints from one consumer mask correct behavior for another. You've created a distributed consistency problem without the distributed consistency primitives.

## Eager Loading vs. Lazy Loading: Different Questions Entirely

These aren't two variations of the same strategy. They're answers to fundamentally different questions.

### Eager Loading (Preloading)

Eager caching answers: "I have mostly immutable data that will be used millions of times. Can I trade memory for guaranteed instant access?"

This is for reference data: lookup tables, configuration that changes through deployments, static content that every request needs. You're paying the cost upfront in memory and startup time, but the payoff is zero cache misses and minimal invalidation complexity.

If you're eager-caching data that changes frequently, you've answered the wrong question. If the data volume is too large to hold in memory, you might have a larger architectural issue—that's not a caching problem, it's a data modeling problem.

### Lazy Loading (Cache-Aside)

Lazy caching answers: "I have a hot path that's causing load on my database. Can I absorb that load by caching results as they're requested?"

This should be the *last* optimization, not the first. Before lazy caching, ask:

- Have you optimized the query itself?
- Have you added appropriate indexes?
- Have you paginated the results?
- Have you protected the endpoint from abuse (rate limiting, request coalescing)?
- Have you confirmed this path is actually hot, with data?

Lazy caching before doing these things doesn't solve problems—it masks them. You'll still have the slow query, the missing index, the unbounded result set. You'll just also have a cache that hides the pain until it expires and the thundering herd arrives.

## Where You Cache Matters More Than How

The worst caching failures come from caching in the wrong place: neither at the source nor at the client, but somewhere in the middle.

**The source** knows when data changes. It can invalidate accurately because it controls the writes.

**The client** knows what staleness it can tolerate. It can set appropriate TTLs because it understands its own use case.

**The middle** knows neither. A shared service layer caching data for multiple consumers doesn't know when the source will change and doesn't know each consumer's staleness budget. It's guessing on both ends.

When you cache in the middle, you get invalidation cycles that don't align with the producer's writes or the consumer's reads. You get "eventual consistency" that never actually converges because different consumers are reading from different cache states. You get impossible-to-debug scenarios where the same request returns different data depending on which cache instance serves it.

Cache at the edges. The source can cache what it knows is safe to cache. The client can cache what it knows it can tolerate stale. The middle should be a pass-through unless you've explicitly designed it otherwise—and that design should include clear invalidation contracts with both the source and all consumers.

## Signs You Cached Too Early

How do you know if your system has accidental caches or premature caching decisions? Look for these symptoms:

**Invalidation logic everywhere.** Cache invalidation calls scattered across multiple services, often inconsistent. Some paths invalidate, others forget to. The invalidation "strategy" is really just hopeful guessing.

**Cache-related bugs nobody can explain.** Data that's "sometimes wrong." Issues that disappear on retry. Bugs that only reproduce in production, never locally. Someone eventually says "maybe it's a cache thing" and everyone nods knowingly but nobody knows which cache.

**Caches nobody remembers.** During an incident, someone discovers a local cache that's been there for two years. Nobody on the current team added it. It's not documented. It might be contributing to the problem, or it might be the only thing preventing a worse problem—no one knows.

**TTLs chosen by intuition.** "I set it to five minutes because that seemed reasonable." No analysis of actual staleness tolerance. No measurement of cache hit rates. Just vibes.

**"Just clear the cache" as a fix.** When cache invalidation becomes part of the troubleshooting runbook, something is wrong. You're treating symptoms, not causes.

## What Disciplined Caching Looks Like

Caching done well starts with the two questions—scope and lifecycle—and only proceeds if the answers are clear.

**Explicit decisions.** Every cache is a deliberate architectural choice, documented and visible. Not a private implementation detail, but a contract that other components can depend on or avoid.

**Defined staleness budgets.** For each cached data type, there's a clear answer to "how stale can this be?" The TTL derives from that answer, not from intuition.

**Invalidation contracts.** If the cache requires invalidation beyond TTL expiry, there's an explicit contract: who invalidates, when, and how consumers know it happened.

**Observability.** Cache hit rates, miss rates, eviction rates, and staleness metrics. You can answer "is this cache helping?" with data rather than assumptions.

**Periodic review.** Access patterns change. The hot path from two years ago might not be hot anymore. The cache that was essential might now be creating more problems than it solves.

## The Hardest Part Isn't Technical

The hardest part of caching isn't choosing between Redis and Memcached, or configuring TTLs, or implementing cache-aside patterns. The hardest part is having the discipline to ask the fundamental questions before reaching for the easy answer.

What's the scope of this data? What's its lifecycle? Do I actually understand the access patterns, or am I guessing? Is this cache the last optimization or the first?

Most teams skip these questions because adding a cache is faster than answering them. That speed becomes debt. The cache becomes invisible. The bugs become intermittent. And six months later, someone else is debugging your impulse decision.

Cache deliberately or don't cache at all. There's no middle ground that doesn't eventually become a support burden.
