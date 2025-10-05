---
layout: guide
title: "Reliability Patterns"
category: Architecture
subcategory: Patterns
---

# Reliability Patterns

Reliability patterns help systems handle failures gracefully, maintain availability, and provide consistent service even when individual components fail.

## Circuit Breaker

Prevents cascading failures by stopping requests to a failing service and providing fallback responses.

**States**:

- **Closed**: Normal operation, requests pass through
- **Open**: Service is failing, requests are blocked
- **Half-Open**: Testing if service has recovered

**Use When**:
- Calling external services that may be unreliable
- Want to prevent cascading failures
- Need to provide fallback behavior during outages

**Example**: Payment service that stops calling external payment gateway when it's down and returns cached "payment pending" responses instead of timing out.

```
Closed: Request → Payment Gateway (success rate > 90%)
↓ (failures exceed threshold)
Open: Request → Immediate failure with fallback (60 seconds)
↓ (timeout expires)
Half-Open: Test request → Payment Gateway
  If success → Closed
  If failure → Open (reset timer)
```

---

## Retry Pattern

Automatically retries failed operations with appropriate delays and limits.

**Use When**:
- Operations may fail due to temporary issues
- Network calls that might timeout
- Operations are idempotent (safe to retry)

**Retry Strategies**:

- **Fixed Delay**: Wait same amount between retries
- **Exponential Backoff**: Increase delay exponentially
- **Random Jitter**: Add randomness to prevent thundering herd

**Considerations**:
- Only retry transient failures
- Implement maximum retry limits
- Ensure operations are idempotent

**Example**: API client retrying failed HTTP requests with exponential backoff.

```
Attempt 1: Immediate → Fail
Attempt 2: Wait 1s → Fail
Attempt 3: Wait 2s → Fail
Attempt 4: Wait 4s → Success
```

---

## Bulkhead Pattern

Isolates system resources to prevent failures in one area from affecting others, similar to ship compartments.

**Use When**:
- Different operations have varying criticality
- Want to isolate resource usage
- Need to maintain core functionality during partial failures

**Implementation Approaches**:

- Separate connection pools
- Different thread pools
- Resource quotas and limits

**Example**: Web application with separate thread pools for user requests, admin operations, and background tasks to prevent admin operations from blocking user traffic.

```
User Thread Pool (50 threads) → User Requests
Admin Thread Pool (10 threads) → Admin Operations
Background Thread Pool (20 threads) → Background Tasks

If admin operations saturate their pool, user requests unaffected
```

---

## Timeout Pattern

Sets maximum wait time for operations to complete, preventing indefinite blocking.

**Use When**:
- Making network calls
- Operations that might hang indefinitely
- Need predictable response times

**Example**: API gateway with 30-second timeout for backend services, returning error response if backend doesn't respond in time.

```
Request → Backend Service
  If response within 30s → Return response
  If no response after 30s → Return 504 Gateway Timeout
```

---

## Quick Reference

### Pattern Comparison

| Pattern | Purpose | Complexity | When to Use |
|---------|---------|------------|-------------|
| **Circuit Breaker** | Prevent cascading failures | Medium | External service calls |
| **Retry** | Handle transient failures | Low | Network operations |
| **Bulkhead** | Isolate failures | Medium | Different criticality levels |
| **Timeout** | Prevent indefinite waits | Low | Any network operation |

### Combining Patterns

Circuit Breaker + Retry:
```
Retry (3 attempts with backoff)
  ↓
Circuit Breaker (stops retries if service consistently fails)
  ↓
Timeout (ensures each attempt has max wait time)
```

### Decision Tree

**Preventing cascading failures?** → Circuit Breaker
**Temporary network glitches?** → Retry with backoff
**Isolating critical vs non-critical?** → Bulkhead
**Operations might hang?** → Timeout

### Best Practices

**Circuit Breaker**: Monitor failure rate, adjust thresholds based on SLA
**Retry**: Use exponential backoff with jitter, limit max retries
**Bulkhead**: Size pools based on resource capacity and criticality
**Timeout**: Set based on P99 latency, not average

---
