---
layout: post
title: "Architecture Is a Belief About Where Authority Belongs"
date: 2026-06-12
description: "SOLID, normalization, least privilege, and bounded contexts come from different traditions, but they share a structural claim: that where authority lives shapes success and failure"
tags: [architecture, design-patterns, solid, software-design, system-design, ddd]
---

SOLID, database normalization, least privilege, and bounded contexts come from entirely different traditions. They appear in different books, get argued about in separate communities, and are rarely taught together in the same breath. On the surface, they seem to address completely separate problems. Trace the failures each one prevents, though, and they all lead back to the same question.

When I encounter a design decision I'm unsure about, I always ask the same thing: **where does authority live, and how bounded is it**? That's what all of them are answering. The domains differ; the principle doesn't.

## Where Authority Belongs

Authority in a software system is the assignment of decision-making power. Something is authoritative over a piece of data when it is the canonical source of truth for that data, and authoritative over a behavior when it is the only thing that can legitimately change or enforce it.

The best practices across software engineering are measurements of this. The Single Responsibility Principle says a class should have one reason to change; the implied claim is that it should hold authority over exactly one concern. Database normalization says no fact should be authoritative in more than one place; each normal form tightens that rule one step further. Least privilege says a process should hold only the authority it can justify; anything beyond that is unbounded authority waiting to be exploited. Bounded contexts in domain-driven design name regions of authority explicitly; within a context, a term has one precise meaning and one authoritative representation.

These aren't separate concerns that happened to share a category. They are each saying the same thing: put authority in the right place, bound it tightly, and don't let it leak.

## Measuring Authority Strength

Authority placement alone isn't enough to evaluate an architecture. A system can name its authorities without enforcing them, or enforce boundaries without ever naming what they contain. Two properties measure how well an authority claim holds: how precisely the authority is scoped, and how strongly its boundary is enforced. They fail independently and require different fixes; sharpening scope without strengthening the bond makes the problem clearer without solving it, while enforcing a poorly scoped boundary just enforces confusion more consistently.

- **Scope** is the precision of the authority claim, calibrated by **behavioral coherence**: whether the authority's decisions, facts, and behaviors change together for the same reasons. A well-scoped authority owns exactly what changes together, and that ownership can be named precisely without qualification. "CustomerFulfillmentsService" or "OrderCheckoutService" tells you what it owns. "OrderService" does not; it requires a follow-up sentence, and that need for qualification is the signal that scope is misaligned. Scope that is too narrow fragments authority across many owners and raises coordination costs; when it's too broad, changes that don't belong together accumulate under one owner.

- **Bond** is the enforcement strength of the boundary, calibrated by **consequence of bypass**: what breaks when the boundary fails. A strongly bonded authority has no known bypass; all interactions must go through its contract. A weakly bonded authority has routes around it such as direct database access, internal calls that skip validation, or shared state that circumvents the service layer. Bond strength is proportional to the consequence of bypass: a payment processing boundary that is bypassed can produce corrupted financial state; a read model that serves slightly stale data can tolerate a weaker bond.

| | Strong Bond | Weak Bond |
|---|---|---|
| **Well-scoped** | Named and enforced | Named but bypassed |
| **Poorly-scoped** | Enforced without clarity | Neither named nor enforced |

The most common outcome is the bottom-right cell: authority that is neither named nor enforced, producing the drift that most refactoring efforts eventually uncover. Architecture style is a statement about where scope and bond balance for a given system. A modular monolith makes a different bet about behavioral coherence and consequence of bypass than a microservices architecture does; neither is universally right, and both are answers to the same calibration question.

## Authority in Practice: An Order Workflow

An order workflow is a useful thread to follow because it touches most of the patterns where authority gets misplaced. Here is what happens to authority as a typical order system evolves.

### No Authority Declared

The system starts as a single application. Order management, payment processing, inventory tracking, and user accounts share a codebase and a database.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│   CheckoutController       AdminController           │
│           │                       │                  │
│           └───────────┬───────────┘                  │
│                       │                              │
│           ┌───────────┴───────────────────┐          │
│           ▼                               ▼          │
│    OrderPaymentMgr ◄──────────► InventoryUserMgr     │
│           │                               │          │
│           └───────────┬───────────────────┘          │
│                       │                              │
│                   Shared DB                          │
└──────────────────────────────────────────────────────┘
```

Both controllers reach into the entire manager layer. `CheckoutController` calls `OrderPaymentMgr` to initiate a purchase and `InventoryUserMgr` to check stock. `AdminController` calls the same managers to modify orders, adjust inventory, and update accounts. The managers cross-call each other when they need data the other holds.

`OrderPaymentMgr` mixes order lifecycle logic with payment processing. `InventoryUserMgr` mixes stock management with user account concerns. Neither manager is scoped to a single domain; neither controller is scoped to a single workflow. And underneath all of it, a single database holds everything.

**Scope**: undefined. Behavioral coherence was never applied; `OrderPaymentMgr` conflates order lifecycle with payment processing, behaviors that change for entirely different reasons.
**Bond**: none. With no boundaries declared, the consequence of bypass is invisible; there is nothing to bypass and nothing to break until the system is large enough that the cost becomes unavoidable.

This is not inherently wrong for an early-stage system. The problem is not the monolith; it is that authority was never considered. When the system grows, there is nothing to grow from.

### Decomposition Without Authority

The team recognizes that `OrderPaymentMgr` and `InventoryUserMgr` are too broad and splits them into per-domain services. Each service deploys independently and owns its own code. They may even have separate schemas on the same database instance, or fully separate database instances. The infrastructure topology doesn't determine the authority structure; the data access patterns do.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│   CheckoutController       AdminController           │
│                                                      │
│    OrderService    PaymentService    InventorySvc    │
│         │               │                │           │
│    [orders DB]    [payments DB]    [inventory DB]    │
│         ▲               │                            │
│         └───────────────┘                            │
│          PaymentService reads orders data            │
│          directly across domain boundary             │
└──────────────────────────────────────────────────────┘
```

Scope has improved on paper: there are named services with named responsibilities. Bond has improved in structure but not in practice. Each service has its own schema, which declares a boundary. But PaymentService queries the orders schema directly, and that bypass exists for any service that knows the connection string. A change to the order data model requires coordinating with every service that queries it, which turns out to be all of them. That is the consequence of the bypass, and it surfaces not at the point of access but at the point of change.

**Scope**: named but not coherent. The names exist, but the boundaries weren't drawn along behavioral coherence lines; PaymentService queries order data because order state and payment decisions are tightly coupled in practice, and the boundary didn't account for that.
**Bond**: declared but bypassed. The consequence of cross-schema access was underestimated; it materializes the first time the order data model changes and every dependent service breaks with it.

This is the most common intermediate state: the full complexity of distributed services without the independence those services were supposed to deliver.

### Shared Authority Through a Facade

With services now decomposed but `CheckoutController` and `AdminController` still reaching across all of them, the team consolidates the entry point into a single facade: a unified consumer-facing API that shapes responses and hides the internal service structure from callers.

The InventoryService follows the same decomposition pattern as Order and Payment; the remaining diagrams narrow to those two to keep the authority problem visible without adding a third context where authority breaks differently.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│                      OrderFacade                     │
│               [validates order here]                 │
│                  │                │                  │
│                  ▼                ▼                  │
│            OrderService      PaymentService          │
│         [also validates]          │                  │
│                  │                │                  │
│            [orders DB]       [payments DB]           │
└──────────────────────────────────────────────────────┘
```

The facade validates order requests before passing them to OrderService. But OrderService also validates orders at the domain level, as it must. The same business rules now live in two places. When a rule changes (say, orders above a certain value require a manual approval step), both the facade and the domain service need to update. One gets updated; the other doesn't. Now clients going through the facade see one behavior and any direct caller of OrderService sees another.

Neither layer is clearly the authority. Both claim to be.

**Scope**: split across two behavioral concerns. Validation rules change when business requirements change; response shaping changes when clients change. Behavioral coherence says these belong to different authorities, but the facade holds both.
**Bond**: split across two enforcement points. The consequence is inconsistent behavior; the rule a caller sees depends on which enforcement point their request path reaches first.

A facade that shapes responses without making domain decisions holds clear, bounded authority over presentation concerns. The moment it acquires business logic, it becomes a second authority over the domain, and drift between the two is a matter of time. The fix is not to remove the facade but to clarify what it owns: routing, shaping, and aggregating results are legitimate; deciding what constitutes a valid order is not.

Getting from this state to properly bounded domains is a migration, not a rewrite. The Strangler Fig pattern is the right mechanism when the client-facing API must stay stable while the internal boundaries are rebuilt: the facade keeps the client contract intact, all business logic moves to the domain services, and cross-domain data queries are replaced with explicit service-boundary calls one by one. Whether that migration is warranted depends on how significantly the internal data model or technology needs to change. A team that undertakes it without a strong reason pays the transition cost without a compelling destination.

What makes the Strangler pattern succeed is a clear definition of done: a point where the facade holds no authority over domain decisions and each domain service holds all of it. Without that endpoint, the migration stalls at the first delivery pressure, the facade accumulates logic again, and the shared authority problem becomes permanent.

### Domain-Driven Decomposition

When the migration completes, each domain exclusively owns its data. More importantly, each domain has modeled its own aggregate root: the object that controls all access to the entities within its boundary.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│  ┌──────────────────┐    ┌──────────────────┐        │
│  │  OrderService    │    │  PaymentService  │        │
│  │                  │    │                  │        │
│  │  OrderAggRoot    │───►│  PaymentAggRoot  │        │
│  │                  │    │                  │        │
│  │  [orders DB]     │    │  [payments DB]   │        │
│  └──────────────────┘    └──────────────────┘        │
└──────────────────────────────────────────────────────┘
```

An order's state can only change through the Order aggregate root: `Order.Accept()`, `Order.Fulfill()`, `Order.Cancel()`. The aggregate root enforces the invariants that govern those transitions. PaymentService cannot read the orders table; if it needs order data, it calls the Order context's service boundary.

**Scope**: named and coherent. Order lifecycle, payment processing, and inventory management each change for different reasons; the boundaries reflect that behavioral coherence.
**Bond**: strong, proportional to the consequence of bypass. State transitions through aggregate roots carry high consequence if violated; the aggregate root enforces accordingly.

This is also the condition that enables independent deployment. The concept of architecture quanta (from Richards and Ford's *Fundamentals of Software Architecture*) describes an independently deployable unit with high functional cohesion (what this framework calls behavioral coherence) and no shared structural dependencies on other units. Strong scope and strong bond produce the preconditions quanta requires. That deployment freedom follows from authority clarity rather than preceding it; designing for deployment independence without establishing authority first tends to produce the earlier failures in this sequence: separately deployed components that still share structural dependencies across domain boundaries.

Authority is now in the right place, and the next evolution needs to keep it there.

### Events Added Incorrectly

The team adds event-driven architecture to decouple the services. A saga orchestrator coordinates the checkout flow by reacting to events and issuing commands.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│  ┌──────────────────┐    ┌──────────────────┐        │
│  │  OrderService    │    │  PaymentService  │        │
│  │                  │    │                  │        │
│  │  OrderAggRoot    │    │  PaymentAggRoot  │        │
│  │       ▲          │    │        ▲         │        │
│  │  [orders DB]     │    │  [payments DB]   │        │
│  └────────┬─────────┘    └────────┬─────────┘        │
│           │                       │                  │
│           └──── SagaOrchestrator ─┘                  │
│                [sets state, issues commands]          │
└──────────────────────────────────────────────────────┘
```

The orchestrator coordinates the flow by reaching into each context and directing what happens next. It tells the Order aggregate root to update the order status. It tells the Payment aggregate root to charge the card. Events that were supposed to decouple the system have instead created a new central authority that sits outside any context and above any aggregate root.

**Scope**: the orchestrator has no behavioral coherence. "Coordination" expands to absorb state management, error recovery, and retry logic from multiple domains; these are behaviors that change for entirely different reasons and have no business sharing an owner.
**Bond**: weakened at the highest-consequence points. The orchestrator bypasses aggregate roots to set state directly, violating the bond exactly where consequence of bypass is greatest.

The mistake is treating events as a coordination mechanism rather than a record of facts. The orchestrator becomes what the shared database was two stages earlier: a bypass path that dissolves the authority boundaries the architecture was supposed to enforce.

### Events as Facts

The corrected version gives the event log a precise authority claim and leaves state authority where it was.

```text
┌──────────────────────────────────────────────────────┐
│                   OrderApplication                   │
│                                                      │
│  ┌──────────────────┐    ┌──────────────────┐        │
│  │  OrderService    │    │  PaymentService  │        │
│  │                  │    │                  │        │
│  │  OrderAggRoot    │    │  PaymentAggRoot  │        │
│  │                  │    │                  │        │
│  │  OrderPlaced ────┼───►│  reacts to fact; │        │
│  │  OrderFulfilled  │    │  makes its own   │        │
│  │  OrderCancelled  │    │  decision        │        │
│  │                  │    │                  │        │
│  │  [orders DB]     │    │  [payments DB]   │        │
│  └──────────────────┘    └──────────────────┘        │
└──────────────────────────────────────────────────────┘
```

The Order aggregate root emits events as facts: `OrderPlaced`, `OrderFulfilled`, `OrderCancelled`. These are records of decisions the aggregate root has already made; they are not instructions to other contexts. The Payment context reacts to `OrderPlaced` by initiating payment processing, but it makes that decision autonomously. No orchestrator tells it what to do.

The event log holds authority over what happened. Each aggregate root holds authority over its own state transitions. Neither claims the other's authority.

**Scope**: coherent at every level. The event log owns the record of facts; each aggregate root owns the decisions it makes in response. These are genuinely distinct behavioral concerns, and each is sized to exactly what changes together.
**Bond**: strong throughout, scaled to the consequence of bypass at each boundary. Event records are immutable; state changes only happen through aggregate roots.

## The Pattern Behind Every Failure

Every failure in this evolution was the consequence of a belief held without examination. The monolith's implicit belief was that authority didn't need to be located at all. The decomposed services believed that naming a boundary was the same as enforcing one. The facade believed it could hold authority over shaping and domain logic simultaneously. The saga orchestrator believed coordination was a kind of ownership. Each belief produced exactly the failure it implied.

Architecture is not the diagram or the deployment topology. It is the answer a system has given to the question of where authority lives. That answer shapes every boundary, every contract, and nearly every way the system can go wrong.

