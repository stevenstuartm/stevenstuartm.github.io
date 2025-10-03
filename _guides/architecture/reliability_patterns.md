---
title: "Reliability Patterns"
category: Architecture
---

← [Back to Architecture Patterns Index](./README.md)

## Overview

Reliability patterns help systems handle failures gracefully, maintain availability, and provide consistent service even when individual components fail.

## Table of Contents

- [Circuit Breaker](#circuit-breaker)
- [Retry Pattern](#retry-pattern)
- [Bulkhead Pattern](#bulkhead-pattern)
- [Timeout Pattern](#timeout-pattern)

---

## Circuit Breaker

**What it is:** Prevents cascading failures by stopping requests to a failing service and providing fallback responses.

**Why use it:** Improves system resilience, prevents resource exhaustion, and enables graceful degradation.

**States:**
- **Closed:** Normal operation, requests pass through
- **Open:** Service is failing, requests are blocked
- **Half-Open:** Testing if service has recovered

**When to use:**
- Calling external services that may be unreliable
- Want to prevent cascading failures
- Need to provide fallback behavior during outages

**Example:** Payment service that stops calling external payment gateway when it's down and returns cached "payment pending" responses instead of timing out.

## Retry Pattern

**What it is:** Automatically retries failed operations with appropriate delays and limits.

**Why use it:** Handles transient failures, improves system reliability, and reduces the impact of temporary issues.

**When to use:**
- Operations may fail due to temporary issues
- Network calls that might timeout
- Operations are idempotent (safe to retry)

**Retry strategies:**
- **Fixed delay:** Wait same amount between retries
- **Exponential backoff:** Increase delay exponentially
- **Random jitter:** Add randomness to prevent thundering herd

**Considerations:**
- Only retry transient failures
- Implement maximum retry limits
- Ensure operations are idempotent

## Bulkhead Pattern

**What it is:** Isolates system resources to prevent failures in one area from affecting others, similar to ship compartments.

**Why use it:** Contains failures, maintains partial system functionality, and prevents resource exhaustion cascades.

**When to use:**
- Different operations have varying criticality
- Want to isolate resource usage
- Need to maintain core functionality during partial failures

**Implementation approaches:**
- Separate connection pools
- Different thread pools
- Resource quotas and limits

**Example:** Web application with separate thread pools for user requests, admin operations, and background tasks to prevent admin operations from blocking user traffic.

## Timeout Pattern

**What it is:** Sets maximum wait time for operations to complete, preventing indefinite blocking.

**Why use it:** Prevents resource exhaustion, enables faster failure detection, and maintains system responsiveness.

**When to use:**
- Making network calls
- Operations that might hang indefinitely
- Need predictable response times

**Example:** API gateway with 30-second timeout for backend services, returning error response if backend doesn't respond in time.

---

← [Back to Architecture Patterns Index](./README.md)