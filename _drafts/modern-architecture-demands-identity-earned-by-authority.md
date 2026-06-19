---
layout: post
title: "Modern Architecture Demands Identity Earned by Authority"
date: 
description: "Whether trust comes from network position or verified identity is not just a security decision; it shapes the entire architecture. The same belief that produces position-based auth produces layered services, because in both cases legitimacy is granted by placement rather than earned by ownership."
tags: [architecture, api-design, distributed-systems, security, design-patterns, microservices]
---

Every service request arrives with the same question: what makes this request legitimate?

One answer is network position. A request is legitimate because it arrived from the right place: behind the perimeter, through the right intermediaries, from a subnet the architecture trusts. This is **positional architecture**: trust derived from where a request came from.

The other answer is verified identity. A request is legitimate because the caller has proven who it specifically is and what it is authorized to do, with credentials that name its bounded scope, not just its network address. This is **identity-oriented architecture**: trust derived from what a caller is, not where it sits. Every service validates every caller the same way; services relate as peers with clear, bounded authority over their own domains.

The same distinction runs through how services claim authority. In a positional system, a service's authority comes from its layer placement: which tier it sits in determines what it controls. Authority is granted by position in the hierarchy, just as trust is granted by position in the network. In an identity-oriented system, a service's authority comes from what it owns: the canonical data, the validation rules, the contract that governs its domain. Authority is earned by ownership, just as trust is earned by proven identity.

**Identity earned through authority. Position granted influence.** These are not style preferences or security policies chosen in isolation. They are the same belief about what confers legitimacy, playing out at every level of the system. The choice determines where authority lives, how teams are organized, and whether a system can adapt as the domain evolves.

The choice of which style to use is often made before anyone had the context to make it: inherited from a previous system, copied from a reference architecture that looked credible, or grown from incremental decisions that collectively produced something no one designed.

## Two Models

The services behind a checkout feature might be arranged like this in a larger engineering organization:

```
Checkout Client
        |
        ▼
CheckoutFacade          ← owned by the API team; shapes the response for this consumer
        |
        ▼
CheckoutOrchestrator    ← owned by the platform team; coordinates the checkout flow
        |               |
        ▼               ▼
  OrderService     PaymentService    ← domain services that own the actual data and rules
        |
    orders DB
```

This is **positional architecture**. The checkout client never calls the domain services directly; it calls a chain of intermediary services, each owned by a different team, each a separate deployment with its own logs and its own failure modes. It is the default in many larger organizations, what teams build when a compliance review recommends network segmentation, and what they inherit when they copy what previous large systems looked like.

The same checkout feature built without the intermediaries:

```
Checkout Client
        |               |
        ▼               ▼
  OrderService ──► PaymentService    ← any authorized caller; each validates the caller's credentials
        |
    orders DB
```

This is **identity-oriented architecture**. The checkout client is an authorized caller that presents credentials each domain service validates directly. No dedicated orchestrator sits in the path. Authorization comes from the credential, not from which service a request passed through.

`OrderService` can also call `PaymentService` directly. `PaymentService` is a functional foundation, narrower in scope and authoritative over payment data and integrations, while `OrderService` holds broader business workflow authority and coordinates accordingly. Both are legitimate callers because authorization is verified by identity, not inferred from position. The difference between this and the positional `CheckoutOrchestrator` above is that `OrderService` has genuine authority over the checkout workflow; it is not an intermediary layer inserted to manage communication.

Before deciding which to build, or before accepting the one already in place, three questions:

- When a payment fails at checkout, how many service logs do you check to find out why?
- If `OrderService` adds a `discount_applied` field, how many other services and teams does exposing it to the client touch?
- Which specific component in the positional diagram does your compliance framework actually require, and where does it say so?

**Positional architecture** (conventionally called layered service architecture) places intermediary components in the synchronous call path between consumers and the services that own domain logic. A consumer never calls a domain service directly; it calls a facade, gateway, or adapter that decides what to pass through, translate, or aggregate. Every call travels the full path; every intermediary must exist, be deployed, be monitored, and be authorized. Each hop is also an authority claim, and as the rest of this post argues, most of those claims are never examined.

**Identity-oriented architecture** (conventionally called flat architecture) removes the mandatory intermediaries. Consumers call domain services directly with their own credentials. The domain service is the sole authority over its data and logic; nothing sits between it and its callers, and no component derives trust from network position. Async workers follow the same principle: they pull from a queue and call domain services as authorized clients, with no inbound endpoint of their own.

A **tier** is a physical deployment boundary, while a **layer** is a conceptual one: an abstraction, a concern, a responsibility.

Identity-oriented architecture has tiers (an API tier for synchronous requests, a worker tier for async), but each holds clear, bounded authority. Neither is a mandatory intermediary in another's call path. The architecture can have many services and still be flat, because "flat" describes the call path, not the service count.

Positional architecture collapses layers into tiers: the facade layer becomes a facade tier, the adapter layer an adapter tier, the orchestration layer an orchestration tier. Every conceptual boundary becomes a physical hop with its own deployment, failure mode, and implicit authority claim. That 1:1 mapping is where all the costs in this post accumulate. If you cannot name what distinct authority a tier holds (what it and only it decides), it has no reason to exist as a tier.

## Two Beliefs About What Architecture Is For

The structural difference between these architectures runs deeper than pattern: it's a difference in belief about what architecture is for.

One answer: architecture is for structuring communication. The design problem is deciding who can talk to whom and through what intermediaries. This orientation draws boxes first (facade box, orchestration box, domain service box) then fits the domain into them. Hierarchy is natural because boxes nest; every layer can justify itself as a mediator between the layers above and below it. This produces positional architecture not from negligence but from a sincere belief that structuring the communication path is the primary architectural obligation.

The other answer: architecture is for structuring ownership. The design problem is deciding who owns what: which concept belongs to which bounded context, what a service and only it decides, where the domain's natural seams lie. Boundaries are discovered by working with the domain until its seams reveal themselves, not assumed from a reference architecture. Connections between bounded contexts are drawn after ownership is understood. This produces identity-oriented architecture not from a preference for simplicity but from the belief that communication structure follows from ownership, not the other way around.

Neither orientation is incompetent. The box designer applying established reference patterns is using solutions that were correct answers to specific constraints at some point. The problem isn't the reasoning; it's that the question being answered is not the question the system has. A system built to control communication paths will keep needing to control them as the domain evolves, because the structure was never derived from the domain. This is the quieter mechanism by which positional architecture spreads, quieter than cargo-culting or the ice man pattern but more pervasive. You don't need to copy a pattern blindly. You only need to believe that structuring communication paths is what architecture is for.

## Authority Has Two Dimensions

Authority is not assigned to a service after it is named; it is what the service is. Every architectural component makes a claim, always present even when unstated: this component has authority over something. Data, logic, a decision, a contract. That claim has to have a clear answer: what does this component have authority over? Without one, the component has no legitimate reason to exist.

Authority isn't about permissions or access control, though those are downstream of it. It's about ownership: who decides what is true, and why is that the right place for the decision? A domain service owns the canonical representation of its data, the validation rules governing it, and the contract it exposes; anything needing that data goes through the service. A worker owns its processing schedule and the side effects it produces. An external-facing API owns its consumer contract and versioning decisions. In each case, the authority is bounded, named, and unambiguous.

When authority is clear and bounded, access follows a need-to-know principle: a caller gets what its authority legitimately requires for a specific context, not everything its network position would allow. When authority is positional, access becomes clearance: the caller belongs to the internal network, so it can reach what the internal network can reach. Clearance is never sufficient on its own; a positional system treats it as though it is.

**Authority granularity** is how finely authority is divided. Coarse: one service owns a broad domain. Fine: many services each own a narrow slice. Neither is inherently correct; granularity is a claim about where the domain's natural seams lie. Divide too coarsely and unrelated concerns couple; divide too finely and you've drawn permanent boundaries before the domain has shown you where they belong.

**Authority strength** is how complete a service's claim is over its domain. High strength means the service owns the data, the validation rules, the contract, and the canonical representation; nothing else reads its database, replicates its logic, or makes decisions on its behalf. Low strength means ownership is shared across components that each hold a piece of what should be a single, bounded claim. Shared authority doesn't stay quietly shared; it becomes a site of drift where different components enforce subtly different rules and no one is certain which is correct.

These dimensions are independent, but their interaction is where the architectural styles diverge. Positional architecture tends toward low authority strength at any granularity, because every intermediary in the call path holds a piece of the authority that should belong to the domain service: the contract shape, the validation logic, the routing decision. Fine granularity amplifies this: many small services each routing through multiple intermediary layers fragments authority at both dimensions simultaneously, clear in isolation but ungovernable collectively.

When a layer translates but doesn't own, routes but doesn't decide, aggregates from services that each claim to be the truth, it exists to compensate for an architectural choice that was never examined. Unclear authority doesn't stay quiet; it becomes a site of conflict.

The same dynamic plays out in teams. A layer without clear authority becomes a place where logic drifts in because someone needed it somewhere and it was close enough, where validation leaks because the domain service enforces one version of a rule and the facade a subtly different one, and where a breaking change propagates unpredictably because nothing downstream knew the layer was authoritative and nothing upstream knew it wasn't. Every intermediary introduces an authority claim that has to be clearly bounded, justified, and maintained as the system evolves. In practice, that clarity doesn't survive delivery pressure, team turnover, and the ordinary entropy of a codebase changing faster than its documentation.

DDD's bounded context answers the granularity question through domain understanding rather than reference architecture. That claim should be earned, not assumed. Starting with fewer services and extracting boundaries as the domain reveals its seams is safer than committing to fine-grained decomposition before anyone has that understanding. Once a boundary is enforced through contracts, separate deployments, and team ownership, correcting it is expensive. Identity-oriented architecture maximizes authority strength at whatever granularity the domain warrants by removing intermediaries that would otherwise dilute it.

## Adopted, Not Chosen

### Copying the Form Without Understanding the Problem

Copying the form of something successful without understanding what made it successful is cargo cult behavior. You observe that mature, at-scale systems have multiple API layers and carefully segmented services. You conclude that serious, production-grade architecture looks like that. You build yours to look like that, before your system has any of the problems that architecture exists to solve.

Netflix, Uber, and their peers arrived at architectural complexity through years of growth that created specific, observable problems. They earned those layers by living with the pain that justified adding them. Teams that copy the pattern don't have that evidence: they have a new domain they don't fully understand yet, a team size that doesn't need those independence guarantees, and a system that hasn't yet revealed where the real scaling or organizational pressure will sit. But the architecture is already in place, shaping every subsequent decision about team boundaries, contracts, and service topology.

### Each Solution Created the Next Problem

This isn't a team-level failure in isolation; it's an industry-level habit with a traceable history. SOA was a response to the monolith's inability to scale independent team ownership. Microservices were a response to SOA's heavyweight contracts and enterprise service buses that became coordination bottlenecks. API gateways and orchestration layers were added to manage the complexity that microservice proliferation introduced. Each solution created the conditions for the next problem, adding another layer of network-boundary decomposition on the last. Most of what makes large distributed systems hard to operate today isn't inherent to the problem domain; it's the complexity of managing complexity left behind by the previous era's solution. When the consistent response to accidental complexity is more structural complexity rather than domain understanding, the pattern itself is the signal.

The question that short-circuits this: what evidence do we have that this layer delivers value a simpler design wouldn't? It sounds obvious, and it almost never gets asked. Published blueprints don't present themselves as solutions to specific problems; they present themselves as what serious, production-grade systems look like. Teams adopt them to look credible, not because they've verified the pattern solves a problem they actually have.

### The Ice Man Anti-Pattern

The enterprise service bus was not primarily an orchestration pattern; it was a resource efficiency pattern. Organizations in the SOA era were operating expensive physical infrastructure, and centralizing message routing, transformation, and protocol mediation let many services share costly computing capacity. Orchestration was an artifact of that centralization: when everything routes through a central hub, coordination logic gravitates there because it's adjacent to the routing logic already present. The hardware constraint is gone; cloud infrastructure makes per-service provisioning economically trivial. The coordination pattern remains, now detached from the economics that generated it.

This is the ice man anti-pattern: an instinct preserved from an era whose constraints have been resolved by infrastructure. The architect isn't trying to rebuild an ESB; they're applying a coordination pattern learned when it was the correct answer to a specific, real constraint. When an orchestration layer appears in a modern system, the useful question isn't whether it coordinates effectively but why centralized coordination seemed like the right tool. In most cases the domain didn't produce that answer; the architect's prior experience did.

### What Monoliths Get Right

Monoliths earn their reputation here. A monolith defers the commitment until the evidence exists to support it. You learn what a service boundary should look like by living with domain logic in one place. You discover which consumers need which representations by watching real usage, not anticipating hypothetical ones. You find out where the actual scaling pressure sits by running the system, not modeling it. Once you've extracted a service, introduced an adapter, or built a coordination layer, you've made a claim about the domain's shape. Starting with a monolith means that claim has to be earned before it gets made permanent.

## What Positional Architecture Means in Practice

A positional architecture places intermediary components between consumers and the services that own domain logic. External-facing facades present domain data in consumer-friendly shapes. Protocol adapters translate between REST and gRPC or between synchronous and asynchronous communication. Orchestration services aggregate calls to multiple backends into a single consumer response. The intended benefit is insulation: consumers protected from internal changes, internal teams free to evolve without breaking contracts.

**In practice, the layers accumulate, and each arrives for a different reason.** The facade gets added at the external boundary. An adapter appears when a new service speaks a different protocol. An orchestrator grows when a consumer operation needs data from three services never designed to coordinate. A glue microservice appears when two teams need their services to collaborate and neither will own the coordination, so the gap between them becomes a service. What started as a single translation layer ends up as four or five hops of different component types, each with its own team, deployment cadence, and failure mode. Each is a potential failure point with its own logging format and error behavior.

The costs show up predictably, and they compound as the system grows:

- Debugging requires understanding the entire layer topology before you can locate a problem; what looks like a one-hour fix often takes a day once the hop-tracing is factored in
- Change velocity slows; a domain model change requires coordinated updates across every dependent layer, turning internal changes into multi-team coordination exercises
- Testing multiplies because you need unit tests at each layer, contract tests between layers, and integration tests across the full stack; each new layer roughly doubles the testing surface
- Infrastructure costs compound because you're running compute and paying for network traffic at every layer, sometimes several times per external request
- Capacity planning is nonlinear because one unit of external load fans out to multiple internal calls, and the resource profile differs at each layer, making projections harder and over-provisioning the common response

## The Distributed Monolith

The distributed monolith failure mode is usually described as microservices sharing a database or codebase, coupling tightly in the ways a monolith does while paying the coordination costs of a distributed system. Positional architecture produces a more common variant that's harder to recognize: not shared code, but shared call chains. Every consumer request travels through the same intermediary services in the same order, and every intermediary couples to the services below it. The layers are separate deployments with separate teams, but a change in any domain service propagates upward through every adapter and facade that depends on it, exactly as it would in a tightly coupled monolith. Every positional system carries the full cost of distributed architecture (separate deployments, coordinated releases, network hops) without the independence those costs were supposed to buy.

Identity-oriented architecture enforces a structural discipline that prevents this. A consumer calls a domain service directly. That service may call one supporting service (auth, feature flags, something domain-agnostic), but the chain ends there. Async workers operate outside this constraint entirely: they pull from a queue and call domain services as ordinary clients, with no inbound call chain. The discipline is a single hop between a domain service and any service it depends on, no deeper.

That constraint matters because chained service calls are how distributed monoliths form. Each hop is a dependency: a service that can't respond until the service below it does, which may be waiting on another in turn. Flatten the chain to one hop and each service can be reasoned about, scaled, and deployed on its own terms. Extend the chain and the system starts to behave like a distributed monolith in the ways that matter: response latency accumulates, failures cascade further than the failure that caused them, and a change requires tracing through services that were never meant to couple.

At sufficient coupling depth, a true monolith is more defensible: it at least eliminates network hops, serialization overhead, and the coordination cost of deploying multiple services to ship a single feature. Those costs are the price of independence. When independence was never achieved, the price is paid with nothing received in return.

## The Asymmetric Security Posture of Positional Systems

**The most serious cost of positional architecture is one that gets treated as a footnote: the security posture it creates is not just asymmetric, it is the natural consequence of what positional architecture believes.**

In a positional system, a service's authority comes from its layer placement. Its identity, such as it has one, is its tier: facade-tier service, orchestration-tier service, domain-tier service. When that service authenticates to call another, the most natural credential is one that proves it belongs to the trusted network: a cert granted by the internal CA, a service mesh identity that says "internal." That credential proves network citizenship, not bounded identity. It answers "are you one of us?" rather than "are you specifically OrderService with authority over orders?" The credential reflects the architecture's actual belief: legitimacy comes from position, not from ownership.

Teams in positional systems concentrate security effort at the edge because the edge is where external callers prove they belong. Everything behind it applies implicit trust, because belonging to the internal network already proved legitimacy. This is not a discipline failure; it is the architecture's trust model applied consistently.

That trust model is exactly what attackers exploit. A single vulnerability such as server-side request forgery, request smuggling, or a compromised internal service gives access to the entire soft interior. The blast radius is the full internal network, not the narrow scope of whatever was actually breached: the difference between rotating one service's credentials and conducting a full incident response across every internal system.

The counter-argument is that you can retrofit zero-trust onto a positional system. Service meshes like Istio and Linkerd add mutual TLS and per-hop authentication without changing service code. That capability works technically. What it cannot do is change what the credentials prove. A cert that says "you are an authenticated internal service" still proves network citizenship. OrderService and a compromised internal service in the same network can both hold valid certs; the difference between them is what they own, and citizenship-based credentials do not carry that information. Retrofitting the mechanism does not change the architecture's belief about what legitimacy means.

The distinction is clearance versus need-to-know. A top secret clearance does not entitle the holder to read everything at or below that classification level. Access to a specific piece of information still requires a specific reason: a bounded, demonstrable need for this information in this context. Clearance is necessary but never sufficient. A service mesh cert that proves "authenticated internal service" is a clearance. It proves tier membership and nothing else; it says nothing about what the caller owns or why this specific access is legitimate for this operation. Positional architectures issue clearances and treat them as sufficient authorization. Identity-oriented architectures demand need-to-know: a specific, bounded authority claim that makes this access legitimate for this actor in this context, independent of where that actor sits in the network.

Identity-oriented architecture inverts this at the root. Every service presents credentials that prove a specific bounded identity: not "I'm internal" but "I'm OrderService, authorized for these operations on order data." A compromised component can only act within its authorization scope. The security model and the architectural model are aligned because they share the same belief: legitimacy comes from what you are, not from where you sit.

### The Attack Surface Objection Is Circular

The predictable response is that identity-oriented architecture increases the attack surface by exposing domain services directly. That concern dissolves under examination.

Attack surface is a count of publicly reachable endpoints, and nothing about positional architecture bounds that count. A positional system can grow its public layer without end; every new consumer-facing feature adds endpoints regardless of whether intermediary tiers exist. Intermediary tiers sit behind those public endpoints, not instead of them; they add internal endpoints, not replace external ones. What a product exposes is determined by requirements, not by whether a facade stands in front of the domain.

In an identity-oriented system, rate limiting, IP flagging, geographic constraints, and gateway-level checks apply everywhere without exception, because there is no interior to fall back on. There is no class of endpoint that gets lighter treatment because a perimeter supposedly already handled it. Positional architecture doesn't make the public layer more secure than a well-secured identity-oriented one; it adds internal layers that receive implicit trust, while the identity-oriented system applies the same controls to every surface. The attack surface objection assumes the perimeter model provides something the identity-oriented model lacks. The asymmetric security posture described above is exactly why it doesn't.

<blockquote class="pull-quote">
<p>Breach the perimeter once and the entire interior is yours. The architecture guarantees it.</p>
</blockquote>

## What Identity-Oriented Architecture Looks Like

**In an identity-oriented architecture, no intermediary service sits between a consumer and the domain service it's calling.** Load balancers and firewalls are still there; that's true of any system. A consumer with appropriate authorization calls the domain service directly. The domain service validates, executes, and responds.

<blockquote class="pull-quote">
<p>The services are not hidden; they're protected.</p>
</blockquote>

Hiding services behind intermediary layers creates the soft interior problem. Protecting services through authorization means every caller proves who they are and what they're allowed to do, regardless of where the request originates.

In practice, this looks like a payment service that exposes an endpoint for processing a charge. A consumer (whether an internal checkout service, a mobile client, or an external partner) authenticates against an identity provider and receives a short-lived token scoped to what its authorization allows. That scope is the caller's identity; the token encodes what it owns and needs, not which network segment it came from. When it calls the payment service, it presents that token. The payment service validates the token, checks the scope against the requested operation, and executes. There is no intermediate service in that path. No component sees the request without also verifying authorization. The payment service doesn't infer trust from the caller's network address; it reads it from the token.

### How Scaling Works in an Identity-Oriented System

Edge gateway layers offer one genuine scaling benefit: they can absorb burst traffic through caching, circuit breaking, and request coalescing, reducing load that reaches internal services. In systems with highly variable traffic, that absorption can be meaningful. The cost is that you're now operating two scaling problems instead of one. When the real bottleneck is in an internal service, the facade's burst absorption delays the pressure signal rather than eliminating it. One unit of external load still produces one unit of eventual scaling pressure on the service that does the work; the facade determines when that pressure surfaces, not whether it does.

In an identity-oriented system, one unit of external load produces one unit of scaling pressure on the service that handles it. Request rate, CPU, and memory pressure are all observable on exactly the thing you're scaling. Scale the service experiencing pressure and the effect is immediate. There's no call chain to reason through to find the bottleneck.


### Shared Services Are Not Hidden Layers

A reasonable objection surfaces here: if an auth service, user service, or tenant service is called by many other services, doesn't that create the same structure? It doesn't. The difference is ownership.

An intermediary doesn't own the thing it handles. A `CheckoutFacade` that shapes order data for a mobile client doesn't own order data; `OrderService` does. Remove the facade and `OrderService` still works; only the mobile-specific shaping is lost.

An auth service, by contrast, owns auth data: the tokens, the sessions, the identity records, the validation rules. Remove it and the system has no canonical source of truth for any of those concepts. That's not an intermediary; it's a domain service whose consumers happen to be other services rather than end clients. The distinction: does the service hold authority over its own domain, or does it exist to access someone else's?

Scope is a separate concern. An auth service whose endpoints are only callable by internal services is scoped that way because its consumers are internal, not because it sits behind anything. Any authorized caller presents credentials; the auth service validates them and responds. Scope is configuration; the architecture doesn't change. Identity-oriented architecture therefore tends toward fewer services with stronger authority; without wrapping layers that accumulate for organizational or coordination reasons, decomposition follows domain seams. A service called by many other services isn't a problem to solve with an additional layer; it's a well-designed domain service.

Cross-cutting concerns like logging, tracing, and rate limiting still need owners. Identity-oriented architecture offers no neutral, unclaimed space to put them. They belong to infrastructure, to a domain service, or they surface as an explicit coordination question. That explicitness forces the question of whether something belongs to the domain or to the platform, and who is accountable for it either way.

## What the Cloud Changes

On on-premises infrastructure, a single hardware gateway handling both internet ingress and internal service-to-service traffic meant a traffic spike from outside competed with internal call volume for the same physical resource. Separating internal routing onto its own dedicated gateway was a legitimate response to that constraint.

### Cloud Infrastructure Removes the Constraint

On cloud, that constraint doesn't exist. Internal calls within a VPC or VNet never leave the virtual network. Load balancers and container infrastructure share managed network resources that scale automatically. The cloud provider solves the resource contention problem at the platform level. Architects who built systems on-premises often bring the internal gateway assumption into cloud-native work, but the resource management that once justified a dedicated layer is handled by infrastructure that never requires attention.

## Where Complex Logic and Async Work Belong

Putting async message handling and event processing in public-facing APIs is an availability and scaling problem. These concerns have different resource profiles and failure modes than synchronous request handling, and mixing them degrades both.

### A Worker Is Not a Facade

The async problem doesn't require a layer at all. Synchronous work belongs in the domain service. Async work belongs in a worker, and a worker isn't the kind of layer this post argues against, because it has no endpoint. Nothing calls it. It pulls events or messages off a queue on its own schedule and calls into domain services as a client, the same way any other consumer does.

That's the structural distinction that matters. A facade sits in the synchronous call path: every consumer call travels through it before reaching the service that owns the logic, making it a mandatory intermediary. A worker sits entirely outside that path. No one calls it; it only calls out, and only when it has work pulled from its own queue.

The domain service doesn't know or care whether the caller is a public consumer or a worker; it validates and responds the same way either way. Workers carry their own identity and call with explicit authorization. There's no implicit trust and no soft interior: the worker presents credentials like any other consumer, and there's no inbound surface on the worker itself for anything to reach.

### Independent Scaling and Local Ownership

Because a worker calls the domain service as an ordinary client rather than intercepting calls to it, async work scales and deploys independently. Worker queue depth is a direct signal of processing backlog; when a batch job puts unusual pressure on the worker pool, the public API is unaffected. Workers can also change without breaking changes because they have no external consumers; the team that owns the domain owns the workers, and deployment decisions stay local.

## Where Third-Party Integrations Belong

A provider service integrates with a third-party system and carries no business logic of its own. Its authority is the integration boundary: what the external system expects, how errors from it are handled, how its event format maps to internal concepts.

### Form Factor Follows What the Integration Requires

Neither style needs to assume a 1:1 relationship between integrations and services. The form should follow what the integration actually requires.

If the integration is outbound only (sending data or triggering actions in an external system), a worker is often enough. Nothing calls into it; it pulls work from a queue and calls the third party on its own schedule. No inbound endpoint means no service boundary is required.

When a new integration appears and its scope is not yet clear, placing it inside the domain service temporarily is a legitimate first step. The domain already holds the business context around the integration; deferring extraction buys time to understand what the new actor needs to be and what form it should take. That decision is easier from working code than from a diagram drawn before the integration was built.

When multiple integrations serve the same broader purpose, such as several payment processors the system might switch between or several SMS providers used to cover regional availability, a single consolidated provider service holds stronger authority than several thin ones. Each thin service owns a fragment of what should be one cohesive claim; a consolidated service can make routing decisions, enforce consistent retry behavior, and present a stable interface regardless of which third party is currently active.

### Inbound Traffic and Where the Public Surface Sits

Webhooks and SSO callbacks invert the direction: a third party calls into your system and something has to receive that call. In identity-oriented architecture, the provider service owns that inbound surface directly; an authorized external caller presents credentials and the service validates them, the same way any other authorized caller does.

Positional architecture creates structural pressure to place an intermediary in front: an API gateway, a dedicated ingress service, or as the integration count grows, a generic cloud function layer that dispatches by event type. That pattern reproduces the CheckoutFacade at the infrastructure layer. The gateway receives the call but has no authority over the integration; the provider service has the authority but no inbound surface. The split arises from what the architectural style makes structurally easy, not from what the domain requires.

When the provider service owns its inbound surface directly, validation, logging, retry behavior, event parsing, and error responses live in one place with one team responsible. When the external system changes its authentication scheme or event format, there is one place to update.

## A Service Is Not a Container

Positional architecture collapses authority and hosting into a 1:1 relationship: the layer becomes the tier and the tier becomes the container. Every conceptual boundary produces a deployment unit. That mapping is so ingrained that it carries over as a default assumption even when the architectural style changes, making a large number of services feel operationally prohibitive before the question of how they should be hosted has been asked.

A service is a unit of authority. It owns data, enforces rules, and exposes a contract. A component is a unit of hosting: a container, a process, a deployed artifact. These are independent choices.

Multiple services can be co-hosted in a single deployed container while maintaining separate logical authority boundaries. Callers call the same endpoints either way; they do not know and do not need to know whether two services run as separate containers or as modules within one. What they know is the contract each service exposes. The hosting arrangement is invisible to them.

A system with a dozen third-party integrations does not need a dozen containers. Provider services that share a broader purpose can be co-hosted, deployed together, and share infrastructure without sharing authority. Each owns its integration boundary; where it runs is a separate concern.

Co-hosting is also a consolidation path. Related services that have grown scattered across independent deployments can be gathered into a single component to reduce operational surface while keeping their authority boundaries intact. The constraint that breaks co-hosting is independent scaling: if one integration handles consistent low volume and another handles traffic spikes, keeping them in the same container ties the scaling of one to the other. At that point, separate components are the right answer, and clearly drawn authority boundaries make that extraction straightforward.

The concern about container proliferation follows from the 1:1 assumption, not from having many services. Flat architecture separates the questions: what does this service own, and where should it run?

## Team Ownership as a Structural Property

### Positional Architecture Produces Horizontal Teams

Positional architecture tends to produce horizontal teams organized around the layers themselves. The backend team owns domain services, the platform team owns orchestration, the API team owns the external facade, and the frontend team consumes it. Each team's incentives point inward; the backend team is rewarded for internal quality, not consumer outcomes, and the orchestration team optimizes for the calls it coordinates rather than the features consumers need. Every capability that crosses a layer boundary requires coordination, negotiation, and synchronized releases. Changes a single team could ship in a day often take weeks when the design, negotiation, and staged deployment span multiple teams.

This is Conway's Law expressed architecturally: organizations design systems that mirror their communication structures, then their communication structures solidify around those systems. The architecture created misaligned incentives; the friction that follows is predictable. The backend team can make decisions affecting every consumer without living with the consequences. The API team becomes a translator between teams with conflicting priorities and authority over neither.

The result is teams in conflict about the architecture rather than the product. Who owns the latency that appeared between the orchestrator and the domain service? Whose responsibility is it when the contract between the facade and the adapter breaks? Who approves changes that cross a layer boundary nobody actually controls? These arguments consume engineering energy that was never directed at the customer, and they look like culture problems when they're actually architectural ones.

### Vertical Slice Teams and Conway's Law

Identity-oriented architecture with vertical slice teams reduces this friction structurally. The team that decides to add a capability is the team that builds it; there's no negotiation because there's no other team in the path. Breaking your own contract has immediate consequences because you feel them directly. In a positional system, adding another intermediary carries no visible short-term cost, so the question of whether it should exist never gets asked. The decision accumulates quietly until there are five hops in the call path and the layers have become teams, each with their own roadmap. Identity-oriented architecture removes that option. Every service has to be owned, named, and justified before it earns a place in the system.

<blockquote class="pull-quote">
<p>Ownership isn't a cultural initiative that requires management reinforcement; it's the default state because there's nowhere else to hand the problem.</p>
</blockquote>

## Clarity, Unity, and Adaptability

Any production system needs clarity about what each component is responsible for, unity in how teams understand the whole, and adaptability as the domain evolves. Positional architecture erodes all three.

### The Comprehension Test

Clarity shows up first in onboarding. When a new developer, a support engineer, or an architect unfamiliar with the system asks how it works, the answer is either a handful of services each clearly owning a bounded domain, or a tour through a layered call graph explaining what each intermediary contributes to a path no single team owns end-to-end. The first produces immediate comprehension. The second produces a map that takes weeks to internalize and still leaves open the question of which layer is authoritative for any given decision.

### Division in Code and Teams

Unity fragments when teams organize around layers rather than domains. The backend team optimizes for internal quality, the platform team for orchestration, the API team for the consumer contract. Each team is doing its job and none of them are doing the product's job, because the product's job crosses every layer boundary and no single team can make the decisions that would serve it. That fragmentation shows up in code as validation logic duplicated across layers with subtly different rules, and in teams as coordination overhead that scales with the number of layers more than with the number of engineers.

### The Architecture That Calcifies Against Change

Adaptability is the property that suffers most durably. Every domain change touching a contract must propagate through adapters, facades, and orchestrators owned by different teams on different release schedules. The architecture presented as flexibility produces rigidity, because every layer is a commitment made before the domain showed whether it needed to move in that direction. The clearest sign that an architecture is serving itself rather than its system is when teams spend more time reasoning about which layer a change belongs to than building the change. In an identity-oriented system, the boundary is the domain, and the domain is what the product actually does.

## The Discipline Objection

The most common response to this argument is that architecture is a secondary concern. Teams with strong governance, comprehensive testing, and mature observability practices can operate positional systems effectively, and teams without those disciplines will struggle regardless of which architecture they choose.

### What the Objection Gets Right

A well-governed positional system beats an undisciplined identity-oriented one. Penetration testing, contract testing between layers, distributed tracing across hops: these practices exist, they work, and teams that apply them can operate positional systems at scale.

### Where It Fails

The objection treats discipline as an architectural substitute, and it isn't. Both architectural styles require those disciplines. The difference is what those disciplines cost when you add layers.

In a positional system, discipline gets applied across a dependency graph that's hard to reason about. A change at any hop can ripple through every connected hop, and the connections aren't visible without tracing the whole topology. Observability requires distributed tracing threaded through every hop, correlation IDs maintained across logging formats that differ at each layer, and aggregated visibility into a call chain that doesn't naturally surface as a single thing. In an identity-oriented system, the dependency graph becomes a set of direct, declared calls between services that authenticate each other, and the discipline a team applies to its own domain stays local rather than rippling into work for every other team along the call chain.

Both options require the same disciplines. One multiplies the cost of every discipline across a dependency graph that grows harder to reason about with every layer added. If you're going to invest in governance, testing, and observability anyway, the architecture that keeps that dependency graph predictable is the better starting point.

## The Genuine Limitations

### The Representation Problem

The most common is the representation problem. Different consumers often need different shapes of the same domain data. The options consistent with identity-oriented architecture are adding representations directly to the canonical service, using GraphQL to let consumers declare the shape they need, or accepting that consumers handle transformation client-side. Distributing validation logic across services is not one of them; that guarantees drift.

### Backend for Frontend as an Identity-Oriented Pattern

The Backend for Frontend (BFF) pattern is a modern variant that fits here: a thin, consumer-specific service that calls domain services directly with its own authorization identity, owned by the team closest to that consumer. This fits within identity-oriented architecture when each BFF is a genuine client of domain services rather than an intercepting intermediary. It falls outside it when BFFs accumulate business logic, hold data, or lack a clear owner; at that point the distinction from a facade collapses.

### When a Thin Facade Is Acceptable

When external contracts genuinely require something more, thin facades are acceptable as a pragmatic concession rather than an architectural pattern. The key constraint is that these facades do one thing: translate. They carry no business logic, no validation, no data ownership. The case for that concession strengthens with domain maturity: a stable domain with a large, heterogeneous consumer base may find a facade's ability to absorb internal model changes worth its maintenance cost; a new domain with a small number of known consumers almost never does, and most systems spend far longer in that second situation than they expect.

The constraint is constant regardless of approach: whatever sits at the external boundary must call the domain service that owns the data, not reach past it. A component that talks directly to the database isn't a facade; it's a competing authority over the same data. The domain service is the authority. Anything that bypasses it, whether for convenience, read performance, or a specific consumer's preferred query shape, takes on ownership of something it was never supposed to own, and the boundary the domain was meant to enforce disappears.

The valid options are narrow: new endpoints on the domain service when the team owns both and the representation belongs to the same domain, or a BFF per consumer type that calls domain services with its own authorization identity. Both preserve the chain of authority; neither creates a second claimant on the data.

None of these require revisiting the internal architecture. The flat core stays flat. The facade is a deliberate boundary concession, not a pattern repeated throughout the system.

## When Positional Architecture Earns Its Cost

Positional architecture, fully realized, produces the most controlled environment. In practice, "fully realized" is the condition that almost never holds.

A positional system built to its full specification applies controls at every boundary: mutual TLS on every internal hop, audit logging at every tier, observability threaded through the complete call chain with correlation IDs that survive format changes between layers, explicit authorization at each layer, penetration testing scoped to each boundary independently. When all of those controls are in place and maintained, you have the most hardened architecture available: every hop requires proof of identity and is independently audited. The compliance surface is maximally demonstrable because every boundary is visible, logged, and controlled.

That is the genuine case for positional architecture. The one other scenario that legitimately forces a specific boundary component, regardless of architecture style, is integration with systems outside your change control: acquisitions, partner APIs, and legacy systems that can't be modified to support identity-oriented calls. A facade at that boundary isn't a commitment to positional architecture; it's a quarantine forced by external constraints, scoped to one boundary, and nothing about it propagates inward.

The problem is that almost no organization that uses positional architecture has consciously committed to it.

Teams arrive at it through cargo-culting, inherited decisions, or compliance requirements that turn out to be softer than presented. PCI-DSS mandates network isolation for the Cardholder Data Environment specifically, not for architectures generally. HIPAA, SOX, and GDPR impose no network topology requirements at all. The pressure toward positional architecture comes from auditors trained on perimeter models, not from the text of the frameworks themselves. The full positional specification never enters the conversation; the controls arrive later, applied unevenly, because the architecture doesn't enforce them and delivery pressure consistently wins.

Most teams pay the organizational costs of positional architecture (the debugging overhead, the coordination tax, the outsized blast radius of any internal compromise) without realizing the security benefits, because realizing those benefits requires consistent, expensive, ongoing investment that the architecture does not enforce.

<div class="callout callout--warning">
<p class="callout__title">The Commitment Test</p>
<p>If you are choosing a positional architecture, these questions determine whether the commitment holds under delivery pressure:</p>
<ul>
<li>Are you applying mutual TLS and explicit authorization on every internal hop, not just at the perimeter?</li>
<li>Is audit logging defined and enforced at every layer boundary independently, not aggregated at the edge?</li>
<li>Is observability threaded through the complete call chain, with correlation IDs that survive every format change between layers?</li>
<li>Is penetration testing scoped to each boundary independently, not just to the external surface?</li>
<li>Does every intermediary component have a named owner with authority and accountability for its evolution?</li>
<li>Is there a committed budget for maintaining these controls under delivery pressure, not just at initial build?</li>
</ul>
<p>If yes to all: positional architecture may be worth its cost. If no to any: you are paying the organizational overhead without receiving the architectural benefit that overhead was meant to fund. Most teams, under honest examination, answer no to most of these; that is why positional architecture is usually an inherited cost rather than a chosen one.</p>
</div>

## Conclusion

These two styles rest on the same foundational question: does legitimacy come from what you are, or from where you sit? Positional architecture answers with position at every level, organizing its auth model around network citizenship and its service topology around layer placement. Identity-oriented architecture answers with ownership at every level: callers prove bounded identity, services earn authority over their domains, and communication structure follows from those answers rather than preceding them.

Positional architecture produces layers, facades, and orchestrators that exist because the architecture needs them, not because the domain does. Those components accumulate their own authority claims, create soft interiors that attackers exploit, organize teams around layers rather than outcomes, and make the system harder to reason about with every hop added. Most teams pay those costs without ever choosing to.

Identity-oriented architecture starts from ownership: what does this service and only this service decide, and where do the domain's natural seams lie? Communication structure follows from those answers, not the other way around. Every caller proves who it is; no network position confers trust, and no intermediary sits in the path unless it holds genuine authority over its own domain. The dependency graph stays predictable because ownership determines it, not communication topology drawn before the domain was understood.

Both styles require the same investment in security, observability, and governance. One multiplies that cost across a dependency graph that grows harder to reason about with every layer added; the other keeps it local and bounded. A system built on position fights to justify that position as the domain evolves. A system built on identity earns its structure from what it owns.

Identity earned its place through authority. Position was granted influence. Authorize the caller, not the hop.
