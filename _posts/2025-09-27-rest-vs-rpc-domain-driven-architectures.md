---
layout: post
title: "REST Is the Wrong Choice for Domain-Driven Architectures"
date: 2025-09-27
tags: [architecture, api-design, ddd, microservices]
description: "Why REST's resource-centric design conflicts with domain-driven architectures and how RPC provides better alignment with business operations."
---

Modern systems favor domain-driven design: modular monoliths, bounded contexts, and capability-based microservices. REST's resource-centric model fundamentally conflicts with these architectures.

When building DDD systems, RPC-style APIs provide clearer alignment with business operations and avoid the architectural contortions required to force-fit REST patterns onto bounded contexts.

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

For domain-driven architectures, RPC-style APIs honestly reflect business operations. Use explicit, verb-based endpoints (`/orders/cancel`, `/orders/refund`) that map directly to capabilities. Maintain consistency within bounded contexts rather than forcing artificial global resource models.

**When to use REST:** Entity-driven systems with global resources (media libraries, inventory, configuration management).

**When to use RPC:** Domain-driven systems with business operations and bounded contexts.