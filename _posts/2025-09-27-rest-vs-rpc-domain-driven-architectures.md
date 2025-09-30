---
layout: post
title: "REST Is the Wrong Choice for Domain-Driven Architectures"
date: 2025-09-27
tags: [architecture, api-design, ddd, microservices]
description: "Why REST's resource-centric design conflicts with domain-driven architectures and how RPC provides better alignment with business operations."
---

Modern architectures are more often domain-driven, not entity-driven: modular monoliths, DDD implementations, and capability-based microservices.

REST's resource-centric design fundamentally conflicts with domain-driven architectures. While REST's technical mechanics remain useful, its conceptual framework breaks down in systems with bounded contexts. RPC approaches provide clearer, more maintainable APIs that align with business operations.

## 1. The Architectural Incompatibility

**Bounded contexts reject global resources:** DDD bounded contexts create different models of the same entity. "User" in Orders: `{id, shippingAddress}`. In Identity: `{id, email, preferences}`. REST demands global consistency, making this incompatible.

**Path naming becomes impossible:** REST suggests `/users/{userId}/orders`, but which service owns "users"? Solutions abandon REST:
- `/orders/api/users/{userId}/orders` (context prefixes)
- `/orders/customers/{customerId}/orders` (domain-specific naming)
- `/orders/search?customerId={id}` (cross-context as search)

**Configuration complexity creates risk:** Preserving clean REST URLs through gateway routing creates brittle configuration. Mapping `/users/{id}/orders` to `/orders-service/customers/{id}/orders` is a "config bug waiting to happen."

## 2. REST Patterns Break Under Business Pressure

**Resource models can't handle operations:** REST works for CRUD but fails for complex business operations. "Partially cancel order for specific line items" forces awkward choices:
- Abuse PATCH `/orders/{id}/line-items` with operation-encoding bodies
- Break pattern with POST `/orders/{id}/partial-cancel`
- Create artificial resource representations that are really workflows

## 3. Technical Benefits Don't Deliver

**Network caching is context-blind:** Proxies caching `/orders/12345` don't understand business events (cancelled, shipped). TTL headers sent "into the void" create dangerous staleness.

**Cargo cult REST:** Teams pursue "REST" from tutorials teaching HTTP + JSON + resource URLs, never encountering actual constraints (hypermedia, uniform interface). They apply a solution without a problem.

## 4. RPC Provides Better Alignment

**Operations map to reality:** RPC maintains consistency: `/orders/cancel`, `/orders/refund`, `/orders/split-shipment`. Operations map directly to business capabilities.

**Documentation becomes clearer:** RPC produces cleaner docs with single-purpose operations instead of `PUT /orders/{id}` that might update status OR add items.

## Conclusion

For domain-driven architectures, RPC is more honest about business operations. I prefer to embrace explicit, verb-based endpoints using POST as default. I prefer to maintain consistency within bounded contexts rather than forcing artificial global standards.