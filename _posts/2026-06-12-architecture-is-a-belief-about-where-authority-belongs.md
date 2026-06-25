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

Authority placement alone isn't enough to evaluate an architecture. A system can name its authorities without enforcing them, or enforce boundaries without ever naming what they contain. Two properties measure how well an authority claim holds: how well the authority is contoured, and how strongly its boundary is enforced.

### Contour

Contour is the precision of the authority claim, calibrated by two conditions:

- **Behavioral coherence**: the authority's decisions, facts, and behaviors change together for the same reasons
- **Operational coherence**: no behavior inside the boundary needs to scale or fail independently of the others

Contour is correctly calibrated when everything inside the boundary satisfies both. CQRS splits read and write models for the same domain not because they are behaviorally incoherent, but because their operational envelopes are incompatible; reads run at far higher volume than writes. A well-contoured authority can be named precisely without qualification: "CustomerFulfillmentsService" or "OrderCheckoutService" tells you what it owns, while "OrderService" does not. That need for a follow-up sentence is the signal that contour is misaligned.

### Bond

Bond is the enforcement strength of the boundary, calibrated by:

- **Consequence of bypass**: what breaks when the boundary fails

A strongly bonded authority has no known bypass; all interactions must go through its contract. A weakly bonded authority has routes around it such as direct database access, internal calls that skip validation, or shared state that circumvents the service layer. Bond strength is proportional to consequence: a payment processing boundary that is bypassed can produce corrupted financial state; a read model that serves slightly stale data can tolerate a weaker bond.

| | Strong Bond | Weak Bond |
|---|---|---|
| **Well-contoured** | Named and enforced | Named but bypassed |
| **Poorly-contoured** | Enforced without clarity | Neither named nor enforced |

The most common outcome is the bottom-right cell: authority that is neither named nor enforced, producing the drift that most refactoring efforts eventually uncover. Architecture style is a statement about where contour and bond balance for a given system. A modular monolith makes a different bet about behavioral coherence and consequence of bypass than a microservices architecture does; neither is universally right, and both are answers to the same calibration question.

## Poor Contour Schedules Drift

Poor contour doesn't create a risk of drift. It schedules it.

When two components hold partial authority over the same concern, they evolve independently. Different teams touch them at different times, under different pressures, for different reasons, and neither has complete visibility into what the other owns. Given any sustained change activity, they will diverge. This is not a failure of discipline or communication; it is the mechanical consequence of splitting an authority claim without resolving the overlap.

### Early Optimization Locks In Miscontoured Authority

The most persistent version of this problem arrives through early optimization. Before a domain's behavioral coherence is understood, before teams know what changes together and what doesn't, structural decisions get made: services get decomposed, schemas get separated, ownership gets assigned. These decisions optimize for things visible right now, like team size, apparent independence, and deployment topology, rather than for behavioral coherence, which only becomes clear under change pressure.

These decisions create structural momentum. Once services are deployed with cross-cutting queries, the cost of realigning authority is high enough to be deferred indefinitely. The miscontour gets locked in with infrastructure investment, team ownership models, and service-level agreements built around it. Drift doesn't just begin at that point; it becomes permanent, because the structure that was supposed to be provisional is now load-bearing.

### The Correlation Between Decision and Consequence Is Hidden

Architectural arguments often fail for two compounding reasons: the failure they predict arrives years after the decision that caused it, and the cost of that failure is rarely expressed in terms legible to the people who control the structure.

When a facade's validation rules and a domain service's validation rules diverge, no one traces that back to the decision to put business logic in a routing layer. They trace it to a human error: someone forgot to update both files. When a decomposed architecture becomes expensive to change because every modification requires coordinating across several services, no one traces that back to service boundaries drawn before behavioral coherence was understood. They trace it to team coordination or some other proximate cause.

The lag between a poor authority placement and its visible consequences is measured in years, not sprints. By the time the drift is painful, the architectural decision is ancient history and the causal chain has been lost.

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

`OrderPaymentMgr` mixes order lifecycle logic with payment processing. `InventoryUserMgr` mixes stock management with user account concerns. Neither manager is contoured to a single domain; neither controller is contoured to a single workflow. And underneath all of it, a single database holds everything.

**Contour**: undefined. Behavioral coherence was never applied; `OrderPaymentMgr` conflates order lifecycle with payment processing, behaviors that change for entirely different reasons.
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

Contour has improved on paper: there are named services with named responsibilities. Bond has improved in structure but not in practice. Each service has its own schema, which declares a boundary. But PaymentService queries the orders schema directly, and that bypass exists for any service that knows the connection string. A change to the order data model requires coordinating with every service that queries it, which turns out to be all of them. That is the consequence of the bypass, and it surfaces not at the point of access but at the point of change.

**Contour**: named but not coherent. The names exist, but the boundaries weren't drawn along behavioral coherence lines; PaymentService queries order data because order state and payment decisions are tightly coupled in practice, and the boundary didn't account for that.
**Bond**: declared but bypassed. The consequence of cross-schema access was underestimated; it materializes the first time the order data model changes and every dependent service breaks with it.

This is the most common intermediate state: the full complexity of distributed services without the independence those services were supposed to deliver.

### Shared Authority Through a Facade

With services now decomposed but `CheckoutController` and `AdminController` still reaching across all of them, the team consolidates the entry point into a single facade: a unified consumer-facing API that shapes responses and hides the internal service structure from callers.

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

**Contour**: split across two behavioral concerns. Validation rules change when business requirements change; response shaping changes when clients change. Behavioral coherence says these belong to different authorities, but the facade holds both.
**Bond**: split across two enforcement points. The consequence is inconsistent behavior; the rule a caller sees depends on which enforcement point their request path reaches first.

A facade that shapes responses without making domain decisions holds clear, bounded authority over presentation concerns. The moment it acquires business logic, it becomes a second authority over the domain, and drift between the two is a matter of time. The fix is not to remove the facade but to clarify what it owns: routing, shaping, and aggregating results are legitimate; deciding what constitutes a valid order is not.

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

**Contour**: named and coherent. Order lifecycle, payment processing, and inventory management each change for different reasons; the boundaries reflect that behavioral coherence.
**Bond**: strong, proportional to the consequence of bypass. State transitions through aggregate roots carry high consequence if violated; the aggregate root enforces accordingly.

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

**Contour**: the orchestrator has no behavioral coherence. "Coordination" expands to absorb state management, error recovery, and retry logic from multiple domains; these are behaviors that change for entirely different reasons and have no business sharing an owner.
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

**Contour**: coherent at every level. The event log owns the record of facts; each aggregate root owns the decisions it makes in response. These are genuinely distinct behavioral concerns, and each is sized to exactly what changes together.
**Bond**: strong throughout, scaled to the consequence of bypass at each boundary. Event records are immutable; state changes only happen through aggregate roots.

## The Pattern Behind Every Failure

Each failure in this evolution had a belief at its root, not examined as a belief but embedded in a deployment choice, a team assignment, or a pattern adoption.

Most architectural disagreements, traced far enough, are arguments about authority that the participants haven't recognized as such. Making the question explicit is what turns a structural intuition into an argument that can be examined, challenged, and defended.

