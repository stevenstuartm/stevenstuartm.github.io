---
layout: post
title: "Identity vs Positional Architecture: Design for Open Connections, not Closed Boxes"
date: 
description: "Service architectures are often adopted rather than chosen. The root of the choice is a question we tend not to ask: does a request earn legitimacy from its network position, or from verified identity? That single choice determines where authority lives, how teams are organized, and whether a system can adapt as the domain evolves."
tags: [architecture, api-design, distributed-systems, security, design-patterns, microservices]
---

Every service request arrives with a question embedded in it: what makes this request legitimate? The answer determines more about a system than any framework, pattern, or compliance requirement, and two answers exist that are not compatible.

The first answer is network position. A request is legitimate because it arrived from the right place: behind the perimeter, having passed through the right intermediaries, originating from a subnet the architecture trusts. This is **positional architecture**. Trust is derived from where a request came from, and maintaining that trust requires a hierarchy of positions, each level conferring legitimacy on the level below it.

The second answer is verified identity. A request is legitimate because the caller has proven who it is and what it is authorized to do, regardless of where it originated in the network. This is **identity-oriented architecture**. Trust is derived from credentials, which means no hierarchy is needed: every service validates every caller the same way, and services relate to each other as peers with bounded authority over their own domains.

These are not style preferences. They are different beliefs about what architecture is for. An architect who treats the primary design problem as structuring communication paths, deciding who can talk to whom and through what intermediaries, will naturally build positional systems. An architect who treats the primary design problem as structuring ownership, deciding what each service holds sole authority over and where the domain's natural seams lie, will naturally build identity-oriented ones. Both orientations produce consistent systems. Only one of them produces systems that can be clearly understood, cleanly owned, and adapted as the domain evolves.

Most teams have never examined which of these questions their architecture is answering. The choice was made before anyone had the context to make it: inherited from a previous system, copied from a reference architecture that looked credible, grown from incremental decisions that each seemed reasonable and collectively produced something no one designed. This post names what was actually chosen and examines what each choice costs.

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

This is **positional architecture**. The checkout client never calls the domain services directly; it calls a chain of intermediary services, each owned by a different team, each a separate deployment with its own logs and its own failure modes. This is the default pattern in many larger organizations. It is also what teams build when a compliance review recommends network segmentation, and what teams inherit when they copy what large, successful systems appeared to look like.

The same checkout feature built without the intermediaries:

```
Checkout Client
        |               |
        ▼               ▼
  OrderService     PaymentService    ← called directly; each validates the caller's credentials
        |
    orders DB
```

This is **identity-oriented architecture**. The checkout client is an authorized caller that presents credentials each domain service validates directly. No facade. No orchestrator. Authorization comes from the credential, not from which service a request passed through.

Before deciding which to build, or before accepting the one already in place, three questions:

- When a payment fails at checkout, how many service logs do you check to find out why?
- If `OrderService` adds a `discount_applied` field, how many other services and teams does exposing it to the client touch?
- Which specific component in the positional diagram does your compliance framework actually require, and where does it say so?

Two words that get conflated but are quite distinct and relevant here: *layer* and *tier*. A **tier** is a physical deployment boundary; a distinct infrastructure unit. A **layer** is a conceptual boundary, a level of abstraction, a concern, a responsibility assigned to a component.

Identity-oriented architecture has tiers: an API tier that serves synchronous consumer requests, a worker tier that processes async jobs. But each tier holds clear, bounded authority. Neither is a mandatory intermediary in another tier's call path; conceptual concerns like validation, authorization, and representation live inside the service that owns them. Identity-oriented architecture can have many services and still be flat, because "flat" describes the call path, not the service count.

Positional architecture tends toward a 1:1 mapping between layers and tiers: the facade layer becomes a facade tier, the adapter layer becomes an adapter tier, the orchestration layer becomes an orchestration tier. When that happens, every conceptual boundary becomes a physical hop in the call path, with its own deployment, its own failure mode, and its own implicit authority claim. That 1:1 mapping is where all the costs examined in this post accumulate. If you cannot clearly name what distinct authority a tier holds, what it and only it decides, it has no reason to exist as a tier.

**Positional architecture** (what is conventionally called layered service architecture, because the hierarchy required to give network position meaning produces structural layers) places intermediary components in the synchronous call path between consumers and the services that own domain logic. A consumer never calls a domain service directly; it calls a facade, gateway, or adapter that decides what to pass through, translate, or aggregate. Each intermediary is a mandatory hop. Every call travels the full path. Every hop is a component that must exist, be deployed, be monitored, and be authorized to call the next thing in the chain. Each hop is also an authority claim; as the rest of this post argues, most of those claims are never examined.

**Identity-oriented architecture** (what is conventionally called flat architecture, because without positional hierarchy the call graph is naturally flat) removes the mandatory intermediaries. Consumers call domain services directly, presenting their own identity credentials on every call. The domain service is the sole authority over its data and logic; nothing sits between it and its callers. Every caller authenticates directly. No component derives authority from its position in the network; authority comes from credentials verified by the domain service itself. Async work follows the same principle: a worker pulls from a queue and calls domain services as an authorized client, just like any other consumer, with no inbound endpoint of its own.

## Two Beliefs About What Architecture Is For

The structural difference between these two architectures traces back to a more fundamental divergence, one that runs at the level of belief rather than pattern. Two types of architects approach a new system with genuinely different answers to the same foundational question: what is architecture for?

One answer is that architecture is for structuring communication. The primary design problem is deciding who can talk to whom, in what order, through what intermediaries. This orientation reaches for containers first. Before the domain is understood, there are boxes: a facade box, an orchestration box, a domain service box. The domain is then fitted into those containers. The structure defines what goes in it rather than the contents defining their need for a boundary. Hierarchy is natural here because containers nest; a box inside a box inside a box is structurally coherent even if it is organizationally arbitrary. Every layer can justify its existence as a communication controller, a mediator between the boxes above and below it. This is the box designer's orientation, and it produces positional architecture not from negligence but from a sincere belief that structuring the communication path is the primary architectural obligation.

The other answer is that architecture is for structuring ownership. The primary design problem is deciding who owns what: which concept belongs to which bounded context, what a service and only it decides, where the domain's natural seams actually run. This orientation begins with the domain, not with containers. Boundaries are discovered by working with the domain until the seams reveal themselves, then drawn to reflect what the business actually treats as distinct. Connections between bounded contexts are relationships between things that already exist and already own their domain; they are drawn after the ownership is understood, not before. This is the connection drawer's orientation, and it produces identity-oriented architecture not from a preference for simplicity but from a belief that ownership is what architecture is for, and that communication structure follows from ownership rather than the other way around.

Neither orientation is incompetent. The box designer working from an established reference architecture is applying patterns that were correct solutions to specific constraints at some point in the industry's history. The problem is not their reasoning; it is that the question they are answering is not the question the system has. A system built to control communication paths rather than to reflect domain ownership will need to keep controlling those paths as the domain evolves, because the structure was never derived from the domain in the first place. The cargo cult and the ice man anti-pattern are mechanisms by which positional architecture spreads; this is the quieter one. You do not need to copy a pattern blindly to produce a system organized around the wrong principle. You only need to believe that communication structure is what architecture is for.

## Authority Has Two Dimensions

Every architectural component makes a claim. The claim isn't always stated, but it is always present: this component has authority over something. Data, logic, a decision, a contract. The question that follows from this has to have a clear, self-describing answer: what does this component have authority over? Without that answer, the component has no legitimate reason to exist.

Authority here isn't about permissions or access control, though those are downstream of it. It's about ownership: who decides what is true, and why is that the right place for that decision to live? A domain service that owns a bounded context has authority because it owns the canonical representation of the data in that context, the validation rules that govern it, and the contract it exposes to callers. Anything that needs that data goes through the domain service; the domain service is the truth. A worker that consumes from a queue has authority over its own processing schedule and the side effects it produces. An external-facing API has authority over the consumer contract and the versioning decisions that protect it. In each case, the authority is bounded, named, and unambiguous.

**Authority granularity** is how finely authority is divided across services. A service that owns a broad domain has coarse granularity; many services each owning a narrow slice have fine granularity. Neither is inherently correct; granularity is a claim about where the domain's natural seams lie. Divide too coarsely and unrelated concerns couple together; divide too finely and you've drawn permanent boundaries before the domain has shown you where they belong.

**Authority strength** is how complete and unambiguous a service's claim is over its domain. High authority strength means the service owns the data, the validation rules, the contract, and the canonical representation; nothing else reads its database, replicates its logic, or makes decisions on its behalf. Low authority strength means ownership is shared across components that each hold a piece of what should be a single, bounded claim. Shared authority doesn't stay quietly shared; it becomes a site of drift, where different components enforce subtly different rules and no one is certain which is correct.

These dimensions are independent, and their interaction is where architectural styles diverge. Positional architecture tends toward low authority strength regardless of granularity, because every intermediary in the call path holds a piece of the authority that should belong to the domain service: the contract shape, the validation logic, the routing decision. Fine granularity amplifies this. A system with many small services each routing through multiple intermediary layers has fragmented authority at both levels simultaneously; the services are clear in isolation and ungovernable collectively.

When a layer has unclear authority, when it translates but doesn't own, when it routes but doesn't decide, when it aggregates data from services that each consider themselves the source of truth, the layer exists to compensate for an architectural choice that was never examined. And unclear authority doesn't stay unclear quietly. It becomes a site of conflict.

This maps directly to what plays out in teams when organizational authority isn't defined. When no one knows who owns a decision, it gets made by whoever has the most leverage in the moment, or it doesn't get made at all, or it gets made twice by different people with different assumptions. The same thing happens architecturally. A layer without clear authority becomes a place where logic drifts in because someone needed it somewhere and this was close enough. Where validation leaks because the domain service enforces one version of a rule and the facade enforces a subtly different one. Where a breaking change propagates unpredictably because nothing downstream knew the layer was authoritative and nothing upstream knew it wasn't.

Positional systems make this structural. Every intermediary introduces a new authority claim that has to be clearly bounded, clearly justified, and clearly maintained as the system evolves. In practice, that clarity doesn't survive delivery pressure, team turnover, and the ordinary entropy of a codebase changing faster than its documentation. The layers accumulate. The authority claims blur. What started as a clear delegation of responsibility becomes a question that different engineers answer differently depending on which part of the codebase they know.

DDD's bounded context is the principled answer to the granularity question: a bounded context is a claim that a natural seam exists in the domain at this point, a seam that reflects how the business actually thinks about its concepts, and that crossing it requires deliberate translation. That claim should be earned through domain understanding, not assumed from a reference architecture. Starting with a smaller number of services and extracting boundaries as the domain reveals its seams is safer than committing to fine-grained decomposition before anyone has that understanding. Once a boundary is enforced through contracts, separate deployments, and team ownership, correcting it is expensive.

High granularity combined with high authority strength, applied before the domain is understood, is the failure mode. A system decomposed into many services, each maintaining strict authority over its narrow slice, carries the full coordination cost of many contracts, many deployment dependencies, and many sources of breaking changes, all imposed on a domain structure that may not yet reflect how the business actually works. The system becomes expensive to operate and fragile in the face of any domain evolution. This isn't an argument against authority strength; it's an argument for earning granularity rather than presuming it.

Identity-oriented architecture and DDD address these two dimensions together. DDD provides the framework for finding the right granularity by driving boundaries from domain understanding rather than network topology. Identity-oriented architecture maximizes authority strength at whatever granularity the domain warrants by removing intermediaries that would otherwise dilute it. The bounded context becomes a service that owns everything in its domain, called directly by authorized consumers, evolving with the domain because no intermediate layer has hardened a claim against it.

## Why Structural Metrics Are the Wrong Starting Point

Coupling, cohesion, and connascence are diagnostic instruments with a specific legitimate use: finding decomposition opportunities in existing legacy systems. When an architect inherits an undifferentiated codebase and needs to locate natural seams, these metrics tell you where change propagates, which modules cluster naturally, and where implicit dependencies have calcified. They help locate candidates for decomposition.

Structural metrics help identify candidates for decomposition; they cannot validate whether the resulting boundary is correct. That question belongs to the domain.

A payment flow and an order flow that share significant implementation surface may look, by coupling metrics, like an obvious decomposition target. Whether that coupling represents a problem or a natural feature of the same bounded context depends entirely on whether the business distinguishes those concepts as separate authorities over their own data. If the domain treats them as one thing, splitting them produces two services that will spend their operational life negotiating over shared concepts neither fully owns. The metric identified a pattern; only domain understanding can say whether that pattern is actually a problem.

This is why Richards and Ford open *Fundamentals of Software Architecture* with three laws that bear directly on this:

> 1. **Everything in software architecture is a trade-off**
> 2. **Why is more important than how**
> 3. **Most decisions exist on a spectrum, not binary choices**

Structural metrics describe the "how" of a system's current state. Tradeoffs are impossible to reason about without the "why," and the "why" is domain knowledge: what authority does this component actually hold, does the product require that authority to be separate from adjacent concerns, and where do the domain's natural seams actually run? Coupling is not binary either; a high coupling score is not automatically a problem that demands splitting. The domain tells you where on that spectrum a given relationship belongs, and no metric substitutes for that judgment.

For a new system, structural metrics provide no signal at all. There is no legacy coupling to measure, no accumulated cohesion failures to observe, no established connascence to trace. The only basis for early boundary decisions is domain understanding, and that has to be earned by working closely enough with the product to know which concepts the business actually treats as separate, and where splitting an apparent seam would fragment natural authority that belongs together. Drawing a boundary before the domain has been understood deeply enough to support it produces a constraint that calcifies against the product as it evolves.

Positional architecture compounds this problem. When intermediary tiers are introduced based on patterns copied from reference architectures rather than on specific domain requirements, the structural complexity they add becomes the thing metrics measure. The coupling between a facade tier and a domain tier looks like an architectural signal that demands a fix. Meanwhile, the authority question (whether any of those tiers reflects a genuine domain distinction the product actually needs) goes unasked, because the measurement produced something that felt like analysis. Architects who know the domain can identify which components hold genuine, bounded authority and which are coordination wrappers that accumulated logic because the architecture had nowhere else to put it. Structural metrics cannot make that distinction.

## Adopted, Not Chosen

### Copying the Form Without Understanding the Problem

There's a name for the pattern of copying the form of something successful without understanding what made it successful: cargo cult behavior. You observe that mature, at-scale systems have multiple API layers and carefully segmented internal services. You conclude that serious, production-grade architecture looks like that. You build yours to look like that, before your system has any of the problems that architecture exists to solve.

Netflix, Uber, and their peers arrived at their architectural complexity through years of growth that created specific, observable problems, most of them legible only in retrospect. At the scale they operate, independent deployment of individual services is worth the coordination cost. The facades and gateway layers they run exist because at their traffic volume and team size, the alternatives create worse problems. They earned those layers by living with the pain that justified adding them.

The teams that copy the pattern don't have that evidence. They have a new domain they don't fully understand yet, a team that doesn't need the independence guarantees that justify deep decomposition, and a system that hasn't yet revealed where its real scaling or organizational pressure will sit. But the architecture is already in place, and it will shape every subsequent decision about team boundaries, contracts, and service topology.

### Each Solution Created the Next Problem

This isn't a team-level failure in isolation; it's an industry-level habit with a traceable history. SOA was a response to the monolith's inability to scale independent team ownership across large enterprises. Microservices were a response to SOA's heavyweight contracts, centralized governance, and enterprise service buses that became coordination bottlenecks. API gateways and orchestration layers were added to manage the operational complexity that microservice proliferation introduced. Each solution created the conditions for the next problem, and each response was another layer of network-boundary decomposition stacked on the last. Most of what makes large distributed systems hard to operate today isn't inherent to the problem domain; it's complexity that exists to manage the complexity introduced by a previous era's solution. When the consistent pattern is to respond to accidental complexity with more structural complexity rather than with domain understanding, the pattern itself is the signal.

The question that short-circuits this pattern is: what evidence do we have that this layer is delivering value that a simpler design wouldn't? That question sounds obvious. It almost never gets asked. Published blueprints don't present themselves as solutions to specific problems; they present themselves as what serious, production-grade systems look like. Teams adopt them to look credible, not because they've verified the pattern solves a problem they actually have.

### The Ice Man Anti-Pattern

The enterprise service bus was not primarily an orchestration pattern. It was a resource efficiency pattern. Organizations in the SOA era were operating expensive physical infrastructure, and centralizing message routing, transformation, and protocol mediation let many services share costly computing capacity rather than each provisioning it redundantly. Orchestration was an artifact of that centralization: when everything routes through a central hub, coordination logic gravitates there because it is adjacent to the routing logic already present.

That origin matters because it explains what actually gets carried forward. Architects who built systems in the SOA era did not learn to reach for a centralized coordinator because coordination logic belongs centrally. They learned it because that is where the shared infrastructure was, and putting coordination logic there solved multiple problems at once on constrained hardware. The hardware constraint is gone. Cloud infrastructure makes per-service resource provisioning economically trivial. The coordination pattern remains, now detached from the economics that generated it.

When an orchestration layer appears in a modern system, the more useful examination is not whether it coordinates effectively but why centralized coordination seemed like the right tool. In most cases the domain did not produce that answer; the architect's prior experience did. The layer accumulates cross-domain logic not because any domain could not own it, but because a central coordinator is the familiar solution for cross-domain work, and familiar tools get reached for before they get examined.

This is what the ice man anti-pattern describes: an instinct preserved from an era whose constraints have been resolved by infrastructure. The architect is not trying to rebuild an ESB. They are applying a coordination pattern learned when that pattern was the correct answer to a specific, real constraint. Recognizing it requires tracing the pattern back to its origin and asking whether the constraint it was built to address is still present. For most modern deployments, it is not.

### What Monoliths Get Right

This is where monoliths earn their reputation, and it has nothing to do with preferring simplicity for its own sake. A monolith defers the commitment until the evidence exists to support it. You learn what a service boundary should look like by living with domain logic in one place. You discover which consumers need which representations by watching real usage, not by anticipating hypothetical ones. You find out where the actual scaling pressure sits by running the system, not by modeling it. Once you've extracted a service, introduced an adapter, or built a coordination layer, you've made a claim about the domain's shape. Starting with a monolith means that claim has to be earned before it gets made permanent.

## What Positional Architecture Means in Practice

A positional architecture places intermediary components between consumers and the services that own domain logic. These intermediaries take different forms depending on the problem they were introduced to solve. External-facing facades present domain data in consumer-friendly shapes and absorb changes in the internal model. Protocol adapters translate between REST and gRPC, or between synchronous and asynchronous communication. Orchestration services aggregate calls to multiple backends into a single consumer response. The intended benefit of all of them is insulation: consumers are protected from changes to internal implementation, and internal teams can evolve without breaking external contracts.

**In practice, the layers accumulate, and each new one arrives for a different reason.** The facade gets added at the external boundary. An adapter appears when a new service speaks a different protocol. An orchestrator grows when a consumer operation needs data from three services that were never designed to coordinate. A glue microservice appears when two services owned by different teams need to collaborate and neither team will own the coordination, so the gap between them becomes a service. What started as a single translation layer ends up as four or five hops of different component types, each with its own team, deployment cadence, and failure mode. What started as architecture ends up as geography; requests travel through multiple hops before reaching the logic that actually handles the work, and each hop is a potential failure point with its own logging format and its own error behavior.

The costs show up predictably, and they compound as the system grows:

- Debugging requires understanding the entire layer topology before you can locate a problem — what looks like a one-hour fix often takes a day once the hop-tracing is factored in
- Change velocity slows because a modification to a domain model requires coordinated updates across every layer that depends on it, turning features that touch internal models into multi-team coordination exercises
- Testing multiplies because you need unit tests at each layer, contract tests between layers, and integration tests across the full stack — each new layer added roughly doubles the testing surface
- Infrastructure costs compound because you're running compute and paying for network traffic at every layer, sometimes several times per external request
- Capacity planning is nonlinear because one unit of external load fans out to multiple internal calls, and the resource profile differs at each layer, making projections harder to get right and over-provisioning the common hedge

## The Distributed Monolith

The distributed monolith failure mode is usually described as a system where microservices share a database or a common codebase, coupling tightly in the ways a monolith does while paying the coordination costs of a distributed system. Positional architecture produces a more common variant that is harder to recognize: not shared code, but shared call chains. Every consumer request travels through the same intermediary services in the same order, and every intermediary couples to the services below it. The layers are separate deployments with separate teams, but a change in any domain service propagates upward through every adapter and facade that depends on it, exactly as it would in a tightly coupled monolith. Every positional system carries the full cost of distributed architecture: separate deployments, coordinated releases, network hops, and independent failure modes at each tier. In a system where coupling runs through every shared call chain, the independence those costs were supposed to buy never materializes.

Identity-oriented architecture enforces a structural discipline that prevents this. A consumer calls a domain service directly. That domain service may call one supporting service (an auth service, a feature-flag service, something domain-agnostic), but the chain ends there. A domain service does not call another domain service that in turn calls another. Async workers operate outside this constraint; they pull from a queue and call domain services as ordinary clients, with no inbound call chain. The discipline is a single hop between a domain service and any service it depends on, no deeper.

That constraint is meaningful because chained service calls are how distributed monoliths form. Each hop in a synchronous call chain is a dependency: a service that cannot respond independently because it must first wait for a response from another service, which may be waiting on another in turn. Flatten the chain to one hop and each service can be reasoned about, scaled, and deployed on its own terms. Extend the chain and the system starts to behave like a distributed monolith in the ways that matter: response latency accumulates across hops, failures cascade further than the failure that caused them, and a change requires tracing a path through services that were never meant to couple.

At sufficient coupling depth, a true monolith is a more defensible architecture than a positional distributed system. A monolith with the same coupling profile at least eliminates network hops, serialization overhead, distributed tracing, and the coordination cost of deploying multiple services to ship a single feature. Those costs are the price of independence. When independence does not exist because coupling was never addressed, the price is paid with nothing received in return.

## The Asymmetric Security Posture of Positional Systems

**The most serious cost of positional architecture is one that gets treated as a footnote: the security posture it creates is asymmetric by design.**

Teams in positional systems concentrate security effort at the edge. The external-facing layer gets TLS, authentication, rate limiting, and careful review. Everything behind it (the adapters, the orchestrators, the domain services) receives requests from other internal components and applies implicit trust, assuming that anything that made it past the perimeter is legitimate.

This assumption is exactly what attackers exploit. A single vulnerability like server-side request forgery, request smuggling, or a compromised internal service gives access to the entire soft interior. The perimeter was solid and everything behind it was unprotected. The blast radius of any internal compromise is the full internal layer, not the narrow scope of whatever was actually breached. In a breach scenario, that difference in scope is the difference between rotating one service's credentials and conducting a full incident response across every internal system.

The counter-argument is that you can retrofit zero-trust onto a positional system. Service meshes like Istio and Linkerd exist precisely for this; they add mutual TLS and per-hop identity verification to internal traffic without changing service code. That capability works. But retrofitting it requires applying a discipline consistently across every internal boundary in a system that was designed with the opposite assumption, and maintaining that consistency as the system evolves. The implicit trust model is the default; zero-trust is the override. In practice, most positional systems have that override applied unevenly, because the architecture never required it and the pressure to apply it uniformly rarely survives the next delivery deadline.

Identity-oriented architecture inverts the default. Every service validates every call because no network position confers trust. A compromised component can only act within its authorization scope, not within the full blast radius of the internal network. You still need rigorous authorization design to realize this property. The difference is that you're building on a foundation where verification is the starting assumption rather than an expensive add-on.

### The Attack Surface Objection Is Circular

The predictable response to this argument is that identity-oriented architecture increases the attack surface by exposing domain services directly. That concern dissolves under examination.

Attack surface is a count of publicly reachable endpoints, and nothing about positional architecture bounds that count. A positional system can grow its public layer without end; every new consumer-facing feature adds endpoints regardless of whether intermediary tiers exist. The intermediary tiers sit behind those public endpoints, not instead of them; they don't reduce the count, they add internal ones. The number of services a product needs to expose is determined by product requirements, not by whether a facade stands in front of the domain.

At the infrastructure level, every service container sits behind private IPs. Load balancers and routing rules govern which traffic reaches which surface. That is true of identity-oriented and positional systems equally; the hardware and virtual instance exposure is identical in both. What architectural style determines is not how many endpoints exist or how the network is structured, but whether every endpoint is treated as a full security obligation.

In an identity-oriented system, every endpoint is. Rate limiting, IP flagging, geographic constraints, and gateway-level checks apply everywhere without exception, because there is no interior to fall back on. There is no class of endpoint that receives implicit trust because of where it sits in the network, and no class that gets lighter treatment because a perimeter supposedly already handled it. Security is uniform by design.

Positional architecture doesn't make the public layer more secure than a well-secured identity-oriented one. It adds internal layers that receive implicit trust because they sit behind the perimeter, while the identity-oriented system applies the same controls to every surface. The attack surface objection assumes the perimeter model provides something the identity-oriented model lacks. The asymmetric security posture described above is exactly why it doesn't.

<blockquote class="pull-quote">
<p>Breach the perimeter once and the entire interior is yours. The architecture guarantees it.</p>
</blockquote>

## What Identity-Oriented Architecture Looks Like

**In an identity-oriented architecture, no intermediary service layer sits between a consumer and the domain service it's calling.** Load balancers and firewalls handle edge concerns; that's true of any system. Identity-oriented architecture removes any service that exists only to intermediate the call. A consumer with appropriate authorization calls the domain service directly. The domain service validates, executes, and responds. That's the full path.

<blockquote class="pull-quote">
<p>The services are not hidden; they're protected.</p>
</blockquote>

Hiding services behind intermediary layers creates the soft interior problem. Protecting services through authorization means every caller proves who they are and what they're allowed to do, regardless of where the request originates.

In practice, this looks like a payment service that exposes an endpoint for processing a charge. A consumer (whether an internal checkout service, a mobile client, or an external partner) authenticates against an identity provider and receives a short-lived token scoped to what its authorization allows. When it calls the payment service, it presents that token. The payment service validates the token, checks the scope against the requested operation, and executes. There is no intermediate service in that path. No component sees the request without also verifying authorization. The payment service doesn't infer trust from the caller's network address; it reads it from the token.

### How Scaling Works in an Identity-Oriented System

Edge gateway layers offer one genuine scaling benefit: they can absorb burst traffic through caching, circuit breaking, and request coalescing, reducing load that reaches internal services. In systems with highly variable traffic, that absorption can be meaningful. The cost is that you're now operating two scaling problems instead of one. When the real bottleneck is in an internal service, the facade's burst absorption delays the pressure signal rather than eliminating it. One unit of external load still produces one unit of eventual scaling pressure on the service that does the work; the facade determines when that pressure surfaces, not whether it does.

In an identity-oriented system, one unit of external load produces one unit of scaling pressure on the service that handles it. The metrics that matter, including request rate, CPU, and memory pressure, are all observable on exactly the thing you're scaling. In production, this manifests as a direct relationship between load and infrastructure: scale the service experiencing pressure and the effect is immediate. There's no call chain to reason through to find the bottleneck.

I've seen this hold even with multiple protocols on the same service. The cost of protocol handling, whether parsing HTTP/2 or deserializing protocol buffers versus JSON, is small compared to what a service actually does. Business logic, database I/O, and computation dominate the execution profile. Whether a request arrived via REST or gRPC changes nothing about the internal work, so scaling behavior is identical because the work being done is identical.

### Shared Services Are Not Hidden Layers

A reasonable objection surfaces here: if an auth service, user service, or tenant service is called by many other services, doesn't that create the same structure? It doesn't. The difference is ownership.

An intermediary doesn't own the thing it handles. A `CheckoutFacade` that shapes order data for a mobile client doesn't own order data; `OrderService` does. The facade exists only to proxy to something else. Remove it and `OrderService` still works; only the mobile-specific shaping is lost.

An auth service, by contrast, owns auth data: the tokens, the sessions, the identity records, the validation rules. Remove it and the system has no canonical source of truth for any of those concepts. That's not an intermediary; it's a domain service whose consumers happen to be other services rather than end clients. The distinction is direct: does the service hold authority over its own domain, or does it exist to access someone else's?

The access scope is a separate concern. An auth service whose endpoints are only callable by internal services is scoped that way because its consumers are internal, not because it sits behind anything. Any authorized caller presents credentials; the auth service validates them and responds. Scope is configuration. The architecture doesn't change.

What this means in practice is that identity-oriented architecture tends toward fewer services with stronger authority, not more services with weaker authority. Without wrapping layers that accumulate for organizational or coordination reasons, decomposition follows domain seams. Each service is larger in scope, stronger in authority, and scaled on its own terms. A service called by many other services is not a problem to be solved with an additional layer on top; it's a well-designed domain service doing exactly what well-designed domain services do.

Cross-cutting concerns like logging, tracing, and rate limiting are still a design choice in any architecture. Identity-oriented architecture offers no neutral, unclaimed space to put them. They have to be owned by infrastructure, by a domain service, or they surface as an explicit coordination question. That explicitness is useful: it forces the question of whether something belongs to the domain or to the platform, and who is accountable for it either way.

One principle holds regardless of which pattern a team chooses: architecture should serve the domain, not the other way around. A decision that can't be justified by a specific domain requirement, a demonstrated team constraint, or a concrete compliance obligation is a decision being made for the architecture's sake. Make tradeoffs for the domain. Adapt them as the domain reveals what it actually needs. The most expensive architectural commitments are the ones made before anyone had enough information to make them, and no pattern, however well-established, is exempt from that test.

## Versioning as a Structural Advantage

Facades provide one genuine versioning benefit: they can absorb internal changes without forcing consumer updates. If a domain model changes, a well-maintained facade can translate to the old shape while the internal service moves forward. That capability is the strongest legitimate argument for translation layers at domain boundaries.

The cost is what happens when the change is in the facade itself, or when the facade fails to absorb an internal change correctly. In a positional system, a breaking change at any layer has to propagate through every intermediary above it. Some get updated on schedule and some don't, and finding where an inconsistency lives requires reasoning about the full topology. Every coordinated update across adapters, orchestrators, and presentation facades is engineering time that isn't delivering features; organizations running large positional systems often find that simple API changes take weeks because of the coordination surface involved.

In an identity-oriented architecture, a version change is a single coordinated decision. The service owns all its representations, whether REST, GraphQL, or gRPC, and they move together. The tradeoff is that there's no absorption layer: consumers talking directly to a domain service must update when the domain changes. Whether that favors identity-oriented or positional depends on the stability of your domain model and the size of your consumer population. A mature, stable domain with a large and heterogeneous consumer base may find a facade's absorption worth its maintenance cost. An early-stage domain with a small number of known consumers almost never does, and most systems face that second scenario far longer than they spend in the first.

## What the Cloud Changes

On on-premises infrastructure, the internal networking constraint was real. A single hardware gateway handling both internet ingress and internal service-to-service traffic means a traffic spike from outside competes with internal call volume for the same physical resource. Separating internal routing onto its own dedicated gateway was a legitimate architectural response to a hardware constraint.

### Cloud Infrastructure Removes the Constraint

On cloud, that constraint doesn't exist in the same form. Internal calls within a VPC or VNet never leave the virtual network. The load balancer and container infrastructure share managed network resources that scale automatically without any planning or intervention. The cloud provider solves the resource contention problem at the platform level, which makes the architectural workaround it was addressing unnecessary overhead.

The DynamoDB parallel clarifies what happened to space-based architecture. Data grids and in-memory computation layers were sophisticated solutions to the problem of relational databases not scaling horizontally under high write loads. DynamoDB didn't improve on space-based architecture; it removed the reason to use it. The underlying problem was solved at the platform level and the complex workaround pattern became cost without benefit.

Cloud networking does the same for the internal gateway concern. Fixed hardware capacity was the problem. The dedicated internal network layer was the workaround. Cloud infrastructure fixes the capacity problem directly, which means carrying that workaround into a cloud-native system means paying the architectural cost without the problem being present. Architects who built systems in on-premises positional environments often bring this assumption with them; in a cloud-native identity-oriented system, internal calls stay within the virtual network, the load balancer scales with the workload, and the network resource management that once justified a dedicated layer is handled by infrastructure that never requires attention.

### AWS and Azure's Default Mental Models

The identity-oriented versus positional debate plays out at the infrastructure level too, and the contrast between AWS and Azure's default approaches illustrates how provider defaults compound the mental models architects carry into system design.

Azure's prescriptive Cloud Adoption Framework leads with hub-and-spoke networking, Corp/Online segmentation, and Landing Zone architectures. These are governance structures for large multi-subscription organizations, not API design prescriptions. But the mental model they establish (that network topology is the primary isolation and security mechanism) creates familiarity with positional thinking. Position in the network confers trust.

AWS's model leads with IAM. Every resource has an identity, every call requires explicit authorization, and account boundaries provide isolation without network segmentation as the primary control. Developers who spend years working in that model develop an instinct to ask "what is this caller authorized to do" rather than "what network can this request come from." That mental model maps directly to identity-oriented architecture.

Neither cloud determines your API design; an AWS team can build positional systems and an Azure team can build identity-oriented ones. But defaults compound. Organizations that arrive at Azure through enterprise procurement paths often bring existing positional architecture assumptions with them, and the infrastructure defaults don't push back. Teams that reach for AWS in a developer-led context often build flatter by default, because the infrastructure they're most familiar with already thinks in identities rather than network positions.

## Where Complex Logic and Async Work Belong

Putting async message handling and event processing in public-facing APIs is an availability and scaling problem. These concerns have different resource profiles and failure modes than synchronous request handling, and mixing them degrades both.

### A Worker Is Not a Facade

The async problem doesn't require a layer at all. Synchronous work belongs directly in the domain service, with no intermediary needed to reach it. Asynchronous work belongs in a worker, and a worker isn't the kind of layer this post has been arguing against, because it has no endpoint. Nothing calls it. It pulls events or messages off a queue or bus on its own schedule and calls into domain services as a client, the same way any other consumer does.

That's the structural distinction that matters. A facade sits in the synchronous call path between a consumer and a domain service: every call a consumer makes travels through the facade before reaching the service that owns the logic, which makes the facade a mandatory intermediary, exactly the kind of soft interior the security section described. A worker sits entirely outside that call path. It's still an actor in the system, but no one calls it; it only calls out, and only when it has work pulled from its own queue.

The domain service doesn't know or care whether the caller is a public consumer or a worker; it validates and responds the same way either way. Workers carry their own identity and call domain services with explicit authorization. There is no implicit trust and no soft interior, because the worker presents credentials just like any other consumer and because there's no inbound surface on the worker itself for anything to reach.

### Independent Scaling and Local Ownership

Because a worker calls the domain service as an ordinary client rather than intercepting calls to it, async work scales and deploys independently of everything else. Worker queue depth is a direct signal of processing backlog, completely independent of API latency. The two scale independently because they're different services with different resource profiles and different failure modes. When a batch job puts unusual pressure on the worker pool, the public API is unaffected. When a traffic spike hits the public API, workers continue processing their queue undisturbed.

Workers can also change without breaking changes because they have no external consumers. The team that owns the domain owns the workers. Deployment decisions are local.

## Team Ownership as a Structural Property

### Positional Architecture Produces Horizontal Teams

Positional architecture tends to produce horizontal teams organized around the layers themselves. The backend team owns the domain services. The platform team owns the orchestration layer. The API team owns the external-facing facade. The frontend team consumes it. Each team's incentives point inward toward their own layer; the backend team is rewarded for internal quality, not for consumer outcomes, and the orchestration team optimizes for the calls it coordinates rather than the features consumers need. Every capability that crosses a layer boundary requires coordination, negotiation, and synchronized releases. That coordination cost accumulates in calendar time: changes a single team could ship in a day often take weeks when the design, negotiation, and staged deployment span multiple teams.

This is Conway's Law expressed architecturally: organizations tend to design systems that mirror their communication structures, and then their communication structures solidify around those systems. The architecture created misaligned incentives, and the political friction that follows is predictable. The backend team that controls the internal layer can make decisions that affect every consumer without living with the consequences. The API team becomes a translator between teams with conflicting priorities and authority over neither.

The result is teams in conflict with each other about the architecture rather than about the product. Who owns the latency that appeared between the orchestrator and the domain service? Whose responsibility is it when the contract between the facade and the adapter breaks? Who approves changes that cross a layer boundary nobody actually controls? These arguments consume engineering energy that was never directed at the customer, and they look like culture problems when they're actually architectural ones.

### Vertical Slice Teams and Conway's Law

Identity-oriented architecture with vertical slice teams reduces this friction structurally. The team that decides to add a capability is the team that builds it. There is no negotiation because there is no other team in the path. Breaking your own contract has immediate consequences because you feel them directly.

Identity-oriented architecture also functions as a forcing function against near-sighted decisions. In a positional system, adding another intermediary service carries no visible short-term cost, so the question of whether it should exist never gets asked. The decision accumulates quietly until there are five hops in the call path and the layers have become teams, each with their own roadmap and their own idea of whose problem the next thing is. Identity-oriented architecture removes that option. Every service has to be owned, named, and justified before it earns a place in the system. You can't hide a vague coordination layer inside an abstraction nobody questions.

<blockquote class="pull-quote">
<p>Ownership isn't a cultural initiative that requires management reinforcement; it's the default state because there's nowhere else to hand the problem.</p>
</blockquote>

## Clarity, Unity, and Adaptability

Two properties any production system should protect are clarity about what each component is responsible for, and unity in how teams understand and work with the whole. Both are prerequisites for a third, adaptability, and positional architecture erodes all three.

### The Comprehension Test

Clarity shows up first in onboarding. When a new developer, a support engineer, or an architect unfamiliar with the system asks how it works, the answer is either a diagram with a handful of services each clearly owning a bounded domain, or it is a tour through a layered call graph explaining what each intermediary contributes to a path no single team owns end-to-end. The first produces immediate comprehension. The second produces a map that takes weeks to internalize and still leaves open the question of which layer is authoritative for any given decision.

The same test now applies to AI-assisted development. Pointing a language model at a flat set of sibling service repositories and their contracts produces coherent, accurate assistance: the model can reason about what each service owns, what a caller can request, and where a change will propagate. Pointing it at a dependency graph of interconnected intermediaries produces unreliable assistance, because the model faces the same problem any human does. The source of truth for any given concept is unclear, and relationships between components are defined by network position rather than explicit ownership. AI tooling amplifies whatever clarity or confusion is already present in the architecture. Identity-oriented systems get better assistance; positional systems compound their navigability problems in every tool that tries to reason about them.

### Division in Code and Teams

Unity is what gets fragmented when teams organize around layers rather than domains. The backend team optimizes for internal quality, the platform team optimizes for the orchestration layer, and the API team optimizes for the consumer contract. Each team is doing its job and none of them are doing the product's job, because the product's job crosses every layer boundary and no single team can make the decisions that would serve it. That fragmentation shows up in code as validation logic duplicated across layers with subtly different rules, and in teams as coordination overhead that scales with the number of layers more than with the number of engineers.

### The Architecture That Calcifies Against Change

Adaptability is the property that suffers most durably. A system that can adapt quickly when the domain changes is one where a team can locate the relevant code, understand what it does, make the change, and verify the result without coordinating releases across multiple layer owners. Identity-oriented architecture with strong authority boundaries supports that. Positional architecture resists it: every domain change that touches a contract must propagate through adapters, facades, and orchestrators owned by different teams on different release schedules. The architecture that is presented as flexibility produces rigidity, because every layer is a commitment made before the domain showed whether it needed to move in that direction.

The clearest sign that an architecture is serving itself rather than its system is when teams spend more time reasoning about which layer a change belongs to than building the change. In a positional system, that balance tips over time: the architecture becomes its own subject of coordination, a set of territorial claims about which team owns which boundary rather than which domain belongs to whom. In an identity-oriented system, the boundary is the domain, and the domain is what the product actually does.

## The Discipline Objection

The most common response to this argument is that architecture is a secondary concern. Teams with strong governance, comprehensive testing, and mature observability practices can operate positional systems effectively, and teams without those disciplines will struggle regardless of which architecture they choose.

### What the Objection Gets Right

A well-governed positional system beats an undisciplined identity-oriented one. Penetration testing, contract testing between layers, distributed tracing across hops: these practices exist, they work, and teams that apply them can operate positional systems at scale.

### Where It Fails

But the objection treats discipline as an architectural substitute, and it isn't. Both architectural styles require those disciplines. Security testing, observability, and contract management aren't optional in either model. The difference is what those disciplines cost when you add layers.

In a positional system, discipline doesn't just get applied more often; it gets applied across a dependency graph that's hard to reason about. A change at any hop can ripple through every other hop connected to it, and the connections aren't visible without tracing the whole topology. Observability requires distributed tracing threaded through every hop, correlation IDs maintained across logging formats that differ at each layer, and aggregated visibility into a call chain that doesn't naturally surface as a single thing. Security coverage requires hardening the perimeter and verifying that implicit trust inside it doesn't create exposure. Testing requires coverage at each layer, contract testing between them, and integration testing across the full stack.

Identity-oriented architecture doesn't reduce that workload; each bounded-context service still owns its own observability, security, and testing investment. "Flat" doesn't mean "one thing." What changes is predictability. Domains share nothing: no shared packages, no shared proxies, no forcing function binding one team's release to another's. That makes the dependency graph a set of direct, declared calls between services that authenticate each other, rather than an implicit web of trust threaded through shared infrastructure. Governance happens through values and communication between teams, not through an architectural chokepoint everyone has to pass through and agree on. That's what lets domains evolve in parallel without breaking development tempo: the discipline a team applies to its own domain stays local instead of rippling unpredictably into work for every other team along the call chain.

The argument "you can operate positional architecture well with enough discipline" is correct. The conclusion "therefore the architecture choice doesn't matter" doesn't follow from it. Both options require the same disciplines. One of them multiplies the cost of every discipline across a dependency graph that grows harder to reason about with every layer you add. If you're going to invest in governance, testing, and observability anyway, the architecture that keeps that dependency graph predictable is the better starting point.

## The Genuine Limitations

### The Representation Problem

The most common is the representation problem. Different consumers often need different shapes of the same domain data. Multiple services writing to the same database is not an option; validation logic must stay canonical, and distributing it across services guarantees drift. The options consistent with identity-oriented architecture are adding representations directly to the canonical service, using GraphQL to let consumers declare the shape they need, or accepting that consumers handle transformation client-side.

### Backend for Frontend as an Identity-Oriented Pattern

The Backend for Frontend (BFF) pattern is a modern variant that fits here: a thin, consumer-specific service that calls domain services directly with its own authorization identity, owned by the team closest to that consumer. A BFF for mobile, a BFF for web, a BFF for external partners. This fits within identity-oriented architecture when each BFF is a genuine client of domain services rather than an intercepting intermediary. It falls outside it when BFFs accumulate business logic, hold data, or when there's no clear owner; at that point the distinction from a facade starts to collapse.

### When a Thin Facade Is Acceptable

When external contracts genuinely require something more, thin facades are acceptable as a pragmatic concession rather than an architectural pattern. The key constraint is that these facades do one thing: translate. They carry no business logic, no validation, no data ownership.

In practice, the right approach depends on context, but the constraint is constant: whatever sits at the external boundary must call the domain service that owns the data, not reach past it. A component that talks directly to the database isn't a facade; it's a competing authority over the same data, and competing authority over data is exactly the problem the post has been arguing against. The domain service is the authority. Anything that bypasses it, whether for convenience, for read performance, or for a specific consumer's preferred query shape, takes on ownership of something it was never supposed to own, and the boundary the domain was meant to enforce disappears.

The valid options at the external boundary are narrow: new endpoints on the domain service when the representation belongs to the same domain and the team owns both, or a BFF service per consumer type that calls domain services with its own authorization identity and is owned by the team closest to that consumer. Both preserve the chain of authority. Neither creates a second claimant on the data.

None of these require revisiting the internal architecture. The flat core stays flat. The facade is a deliberate boundary concession, chosen with full awareness of its cost, not a pattern repeated throughout the system.

## When Positional Architecture Earns Its Cost

Positional architecture, fully realized, does produce the most controlled environment. The rest of this section is about why "fully realized" is the condition that almost never holds.

A positional system built to its full specification applies controls at every boundary: mutual TLS on every internal hop, audit logging at every tier, observability threaded through the complete call chain with correlation IDs that survive format changes between layers, explicit authorization at each layer rather than implicit trust derived from network position, penetration testing scoped to each boundary independently. When every one of those controls is in place and maintained as the system evolves, you have the most hardened architecture available. Every hop requires proof of identity. Every hop is independently audited. The compliance surface is maximally demonstrable because every boundary is visible, logged, and controlled.

That is the genuine case for positional architecture. The one other scenario that legitimately forces a specific boundary component, regardless of overall architecture style, is integration with systems outside your change control: acquisitions, partner APIs, and legacy systems that cannot be modified to support identity-oriented calls. A facade at that boundary isn't a commitment to positional architecture; it's a quarantine forced by external constraints, scoped to one boundary, and nothing about it propagates inward.

The problem is that almost no organization that uses positional architecture has consciously committed to it.

Teams arrive at positional architecture through cargo-culting, inherited decisions that predate any evaluation, or compliance requirements that turn out to be softer than presented. PCI-DSS mandates network isolation for the Cardholder Data Environment specifically, not for architectures generally. FedRAMP High is prescriptive but satisfiable without a positional approach when controls are demonstrated through identity enforcement. HIPAA, SOX, and GDPR impose no network topology requirements at all. The pressure toward positional architecture comes from auditors trained on perimeter models, not from the text of the frameworks themselves. The full positional specification, including mutual TLS everywhere, per-boundary audit, comprehensive observability, and independent penetration testing at each tier, never enters the conversation. The controls arrive later, applied unevenly, because the architecture doesn't enforce them and delivery pressure consistently wins over applying them uniformly. Three of the five hops haven't been tested since the diagram was drawn.

The gap between the architecture as committed to and the architecture as operated is the pattern. Most teams pay the organizational costs of positional architecture, including the debugging overhead, the coordination tax, and the outsized blast radius of any internal compromise, without realizing the security benefits, because realizing those benefits requires a consistent, expensive, ongoing investment that the architecture does not enforce.

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

## The Migration Asymmetry

You can evolve from identity-oriented to positional incrementally. You observe which consumers need different representations, you add facades at those specific boundaries when the need is clear, and internal services remain unchanged. Each addition is local and reversible.

Evolving from positional to identity-oriented is possible in principle; strangler fig migrations, team consolidations, and contract renegotiations can all be done. In practice they rarely are. The layers have become teams, contracts, and organizational commitments. Removing a layer means someone's team loses scope and someone's external contract changes; the engineering cost of a migration typically runs to months, and the organizational cost rarely finds a sponsor willing to absorb it. The more realistic outcome is that positional systems accumulate layers rather than shedding them.

<blockquote class="pull-quote">
<p>Positional systems stay positional until they're rewritten, which is why the architecture decision made early is the one you live with for a long time.</p>
</blockquote>

Starting identity-oriented preserves optionality. Starting with positional architecture narrows it early. That asymmetry alone is a strong argument for starting with the simpler system and adding complexity only when a specific, demonstrated need has appeared, not in anticipation of one that might.

The larger point is not that identity-oriented is better and positional is worse. It's that the evaluation moment (the point at which someone asks what value this structure is delivering) almost never happens before the commitment is made. By the time the answer is visible, the architecture is already a set of teams, contracts, and deployment dependencies. The most expensive version of this mistake isn't paying the wrong costs; it's paying costs that were never examined against the benefits they were supposed to produce.
