---
layout: post
title: "JWTs Are for Authentication, Not Authorization"
date: 2025-10-10
series: "Architecture Insights"
tags: [security, architecture, jwt, authentication, authorization]
description: "Why embedding authorization in JWTs creates security risks and UX problems. Learn the difference between authentication and authorization, and why session-based grants are worth the minimal latency cost."
---

JSON Web Tokens (JWTs) have become ubiquitous in modern web applications, but they're often misused. The most common mistake? Treating them as an authorization solution when they're fundamentally an authentication mechanism. This misunderstanding leads to security vulnerabilities, poor user experience, and operational headaches.

## The Problem: Immutability Meets Reality

JWTs are immutable by design. Once signed and issued, the claims inside cannot be changed until expiration. This works for authentication—your identity doesn't change mid-session. But it creates significant problems for authorization.

Real-world scenarios:

- A user's subscription expires, but they retain full access for another hour
- An employee is terminated, but their JWT grants system access until it expires
- A security breach requires immediate permission revocation across a role
- A customer upgrades their plan, but doesn't see new features until token refresh

The immutability creates a window of risk or poor user experience—minutes to hours depending on token TTL.

## The Common "Solution" That Doesn't Work

The typical response: shorten JWT lifetimes (5-15 minutes) and refresh aggressively. This creates new problems:

- **Chatty network traffic**: Constant token requests
- **Doesn't solve the core issue**: Still a delay window, just shorter
- **Added complexity**: More moving parts, more failure modes

This just works around the fundamental mismatch between immutable tokens and dynamic authorization.

## The Latency Myth

The argument for embedding authorization in JWTs centers on performance: "We can't afford to hit the database on every request." This is a false tradeoff.

The numbers:

- **JWT validation**: ~1-2ms
- **Session lookup + grant retrieval**: ~5-10ms (DynamoDB, properly indexed)
- **Total latency added**: ~3-8ms

For a typical API request (50-200ms), this is imperceptible. In return, you gain:

- **Immediate revocation**: Security and UX problems solved instantly
- **Predictable behavior**: No "it works sometimes" bugs
- **Simpler mental model**: Authorization lives in one place

### No Cache Required

Many engineers assume they need Redis or Memcached for fast session lookups. In practice, a well-designed DynamoDB table delivers single-digit millisecond reads without cache cluster complexity:

- No cache warming or invalidation logic
- No cache infrastructure to manage
- No cache-database synchronization issues
- Often lower cost at scale than running a cache cluster

## Where JWTs Still Shine: Limiting Token Exposure

If JWTs shouldn't carry authorization, what's their value? **Limiting the blast radius of token exposure.**

The pattern:

1. **JWT contains**: Identity, session ID, source/device info, expiration (1 hour)
2. **On each request**: Validate JWT, look up session, fetch current grants
3. **JWT refresh**: Client auto-requests new JWT when approaching expiration
4. **Refresh token**: Single-use, longer-lived (days/weeks)

If a JWT is leaked:

- Token is only valid for 1 hour maximum
- Next refresh can be denied if session is invalidated
- Session ID enables tracking token usage

The refresh mechanism isn't about keeping authorization current—it's about minimizing the window where a compromised token remains useful.

## Microservices and Shared State

A common concern: session-based authorization introduces shared state into a distributed system, creating dependencies and potential bottlenecks.

This is legitimate, but the authentication vs. authorization distinction still applies:

- **Authentication (JWT validation)**: Stateless, no external dependencies
- **Authorization (grant lookup)**: Requires current state from a shared data store, not in-memory session state

Patterns that preserve service autonomy:

- **Shared session store**: DynamoDB, Postgres—fast reads, externalized state
- **Authorization service/API**: Centralized grant logic, cacheable at the edge
- **API gateway enrichment**: Gateway fetches grants once, enriches downstream requests

You're not adding stateful sessions to individual services—you're externalizing authorization to a shared, scalable data layer that services query independently.

## Hybrid Approaches and Their Complexity

Some teams use hybrid models:

- **Coarse-grained roles in JWT, fine-grained permissions server-side**: JWT contains "admin," but specific capabilities are fetched
- **JWT blocklists**: Track revoked tokens in a shared store for early invalidation
- **Short-lived JWTs with embedded permissions**: Aggressive refresh (every 5 minutes) to approximate real-time changes
- **Version numbers in JWTs**: Token includes permission version, server checks if current

These attempt to balance statelessness with dynamic authorization. In practice, they introduce significant complexity:

- **Tuning difficulty**: How short should JWT TTL be? How to cache the blocklist? When to check versions?
- **Debugging challenges**: Authorization bugs span token structure, refresh timing, cache invalidation, and server logic
- **Partial solutions**: Still have stale permission windows or require coordination
- **Operational overhead**: More moving parts, more failure modes

The complexity cost rarely justifies the benefits. You're building infrastructure to work around the mismatch between immutable tokens and dynamic authorization, when session lookup solves it directly.

## The Product and Subscription Reality

Product-driven systems tie authorization to constantly changing factors:

- Subscription tiers (Free, Pro, Enterprise)
- Feature flags (gradual rollouts, A/B tests)
- Usage limits (API calls, storage, seats)
- Time-based access (trials, seasonal features)

Embedding these in JWTs means your product is always out of sync with reality.

## Internal Systems Need This More

It's tempting to think: "For internal systems, we can put roles in the JWT—employees don't change roles often."

But internal systems have:

- Higher security requirements (sensitive data and capabilities)
- Greater blast radius (compromised admin access affects everyone)
- Compliance needs (SOC2, GDPR, HIPAA require immediate revocation)
- Audit requirements ("When did this person lose access?" must be answerable)

The places where JWT authorization seems acceptable are often where it's most dangerous.

## The Operational Flexibility Tradeoff

JWT-based authorization can work for systems with simple, stable permission models. For MVPs or rarely-changing authorization, embedding claims in tokens is reasonable.

The key consideration is operational flexibility. With session-based authorization, you can change system behavior for all in-flight tokens without deploying code or coordinating services.

**Session-based approach:**
- New permission model? Update the authorization service.
- Emergency capability revoke? Single database update.
- A/B test a feature gate? Flip a flag in the session store.
- Temporary elevated access? Grant expires automatically server-side.
- Fix a permission logic bug? Every request immediately uses new logic.

**JWT-based approach:**
- Client updates for new token structures
- Coordinated service deployments if multiple services parse claims
- Migration logic for old vs. new token formats
- Careful timing to avoid breaking in-flight tokens
- Wait for token expiration before changes take effect

**Single-point control versus distributed state.** Session-based authorization centralizes logic in one place. JWT authorization distributes it across every token in existence, requiring coordination and time for changes.

As systems grow, simple role checks evolve into feature flags, subscription tiers, usage quotas, and time-based access. The coupling between token format and authorization logic constrains how quickly you can adapt.

## Conclusion

JWTs are excellent for authentication—cryptographically signed, time-limited proof of identity. But they're a poor fit for authorization because authorization is inherently dynamic.

The 5ms latency cost of real-time grant checking is negligible compared to the security risks, user experience problems, and operational complexity of making immutable tokens carry mutable authorization data.

Use JWTs for establishing identity and limiting token exposure windows. For authorization, embrace the few milliseconds of latency and gain predictability, security, and operational flexibility.
