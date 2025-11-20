---
layout: post
title: "Stop Forcing REST onto Domain-Driven Architectures"
date: 2025-09-27
series: "Architecture Insights"
tags: [architecture, api-design, ddd, microservices]
description: "Why REST's resource-centric design conflicts with domain-driven architectures and how RPC provides better alignment with business operations."
---

I've spent years watching teams wrestle with REST in domain-driven systems. The pattern keeps repeating: start with clean REST endpoints, then gradually compromise as business operations don't map to resource CRUD. By the time you're done, you've abandoned most REST principles anyway while keeping the complexity.

The mismatch isn't accidental. REST's resource-centric model assumes a world of global, consistent entities. Domain-driven design deliberately rejects that assumption. When you build systems around bounded contexts and business capabilities, RPC-style APIs provide better alignment without the architectural contortions.

## Bounded Contexts Break REST's Core Assumptions

Domain-driven design creates different models of the same entity within different contexts. In the Orders context, a "User" might be `{id, shippingAddress}`. In the Identity context, that same user is `{id, email, preferences}`. Each context owns its own model because each serves different business capabilities.

REST's resource-centric design assumes you can navigate a graph of globally consistent resources. The `/users/{userId}/orders` pattern looks clean until you ask: which service owns "users"? The Orders service needs customer information, but it doesn't own the canonical user representation. The Identity service owns users but knows nothing about orders.

Teams resolve this by abandoning REST principles while keeping REST-like paths:
- Add context prefixes: `/orders/api/users/{userId}/orders`
- Use domain-specific naming: `/orders/customers/{customerId}/orders`
- Treat cross-context queries as search: `/orders/search?customerId={id}`

Some teams preserve clean REST URLs through gateway routing, mapping `/users/{id}/orders` to `/orders-service/customers/{id}/orders` internally. This creates brittle configuration where a routing mistake can expose the wrong bounded context's model of a user to callers expecting a different representation.

## Business Operations Don't Map to Resource CRUD

REST works well when business operations map cleanly to create, read, update, and delete. When operations become more complex, the resource model breaks down.

Consider "partially cancel an order for specific line items." This isn't updating an order resource. It's a business operation with validation rules, inventory adjustments, and refund calculations. Teams force this into REST through:
- Abusing PATCH `/orders/{id}/line-items` with operation-encoding request bodies
- Breaking the pattern with POST `/orders/{id}/partial-cancel`
- Creating artificial resource representations that model workflows instead of entities

Each approach abandons REST principles. The first hides operations inside generic update endpoints. The second admits operations exist but pretends they're still resource-oriented. The third creates phantom resources that don't represent actual domain entities.

## REST's Technical Benefits Rarely Apply

REST's architectural constraints provide real benefits in certain contexts. HTTP caching through intermediary proxies can reduce server load. Hypermedia enables clients to discover capabilities dynamically. The uniform interface allows generic tooling to work across different APIs.

Domain-driven systems rarely benefit from these properties. Network proxies caching `/orders/12345` don't understand business events. When an order gets cancelled or shipped, the cached representation becomes stale. Cache-Control headers help, but you're broadcasting time-based expiration into the void and hoping intermediaries respect it.

Most teams never implement hypermedia controls anyway. They learn "REST" from tutorials teaching HTTP + JSON + resource URLs, never encountering the actual constraints that make REST architecturally significant. They end up with HTTP-based RPC that pretends to be RESTful without gaining any of the benefits Roy Fielding described.

## RPC Aligns with Domain Operations

RPC-style APIs maintain consistency between API design and business capabilities. Operations like `/orders/cancel`, `/orders/refund`, and `/orders/split-shipment` map directly to what the business actually does. There's no translation layer between domain language and API structure.

Documentation becomes clearer because each endpoint serves a single purpose. Compare `POST /orders/cancel` with explicit parameters to `PUT /orders/{id}` which might update the order status, or add line items, or change shipping addresses, or trigger cancellation depending on the request body. The generic resource update endpoint forces clients to understand complex state machines hidden behind a uniform interface.

## Choose Based on Your Domain Model

REST works well for entity-driven systems with globally consistent resources. Media libraries, inventory systems, and configuration management often fit this model. Resources have stable identities and standard CRUD operations align with business needs.

Domain-driven systems with business operations and bounded contexts align better with RPC. Use explicit, verb-based endpoints that map directly to business capabilities. Stop forcing operations into resource updates. Stop pretending different bounded contexts can share resource definitions.
