---
layout: post
title: "Topology Is Not a Trust Model"
date: 2026-06-19
description: "What makes a service request legitimate? Most teams treat it as an authentication question, but the answer is also an architectural one. One school of thought grants legitimacy by placement; the other demands it be earned through verified ownership. Both beliefs shape the credential model and the service structure simultaneously."
tags: [architecture, api-design, distributed-systems, security, design-patterns, microservices]
---

Every service request arrives with the same question: what makes this request legitimate? 

Most teams treat this soley as an authentication problem, but the answer reaches much further than that. It shapes how services are structured, where trust boundaries are drawn and defended, and how teams own their work.

Two schools of thought answer the question differently.

One answer is the claim of network position. A request is legitimate because it arrived from the right place: behind the perimeter, through the right intermediaries, or from a subnet the architecture trusts. This is **positional architecture**: legitimacy granted by placement.

The other answer is verified identity and, as such, bounded authority. A request is legitimate because the caller has proven who it is and what it is authorized to do. Credentials name its bounded scope, not just its network address. This is **identity-oriented architecture**: legitimacy earned by ownership. Every service validates every caller the same way, and all services relate to each other as **peers** with clear, **bounded authority** over their own domains.

In practice, a system's answer at the client boundary and its answer internally are independent choices. A system can be identity-oriented externally and positional internally, or vice versa. The underlying belief tends to be consistent even when the implementation differs. This post focuses on internal architecture, where that belief determines the most profound trade-offs.

At the core of contention is the contrast between **Bounded Authority** and **Positional Claim**. This is not as simple as a separate authentication decision and a separate architecture decision. It tends to be one belief about where legitimacy comes from. That belief determines where authority lives in the system, how teams own their work, and whether the system can adapt as the domain evolves.

## Two Models

The services behind a checkout feature might be arranged like this in a larger engineering organization:

```
Checkout Client
        │ ← identity verified here (edge)
        ▼
CheckoutFacade          ← owned by the API team; shapes the response for this consumer
        │ ← internal; trusted by position, not verified identity
        ▼
CheckoutOrchestrator    ← owned by the platform team; coordinates the checkout flow
        │               │
        ▼               ▼
  OrderService     PaymentService    ← no credential check; trusted because internal
        │
    orders DB
```

This is **positional architecture**. The checkout client never calls the domain services directly; it calls a chain of intermediary services, each owned by a different team, each a separate deployment with its own logs and its own failure modes. Auth happens once, at the edge; everything behind it is trusted because it arrived from the right place.

The same checkout feature built without the intermediaries:

```
Checkout Client
        │ [checkout token]         │ [checkout token]
        ▼                          ▼
  OrderService ──[order-svc token]──► PaymentService
[validates caller]                  [validates caller]
        │
    orders DB
```

This is **identity-oriented architecture**. The checkout client is an authorized caller that presents credentials each domain service validates directly. No dedicated orchestrator sits in the path. Authorization comes from the identity's credential, either as an external actor or an internal actor. When OrderService calls PaymentService, it presents its own service identity; the client's token is never forwarded.

These are examples of the pure forms of each model. Real systems sometimes mix them: identity-oriented credentials at the public edge with positional trust internally, or the reverse. The diagrams show the pattern that emerges when a single belief about legitimacy is applied consistently from client to domain service.

## Bounded Authority

Authority isn't about permissions or access control, though those are downstream of it. It's about ownership: who decides what is true, and why is that the right place for the decision? A domain service owns the canonical representation of its data, the validation rules governing it, and the contract it exposes. In each case, the authority is bounded, named, and unambiguous.

Shared authority doesn't stay quietly shared; it becomes a site of drift where different components enforce subtly different rules and no one is certain which is correct. A layer that translates but doesn't own, routes but doesn't decide, or aggregates from services that each claim to be the truth fragments authority in ways that need to be consciously bounded and justified; the goal is to decide those tradeoffs intentionally, not let them accumulate unexamined. That drift also plays out in teams: a layer without clear authority becomes a place where validation leaks because the domain service enforces one version of a rule and the facade a subtly different one, where a breaking change propagates unpredictably because nothing downstream knew the layer was authoritative and nothing upstream knew it wasn't.

Identity-oriented architecture maximizes authority strength at whatever granularity the domain warrants by removing intermediaries that would otherwise dilute it. Starting with fewer services and extracting boundaries as the domain reveals its seams is safer than committing to fine-grained decomposition before that understanding exists. Once a boundary is enforced through contracts, separate deployments, and team ownership, correcting it is expensive. Whatever sits at the external boundary must call the domain service that owns the data; a component that reaches past it to the database isn't a facade, it's a competing authority over the same data. The same test applies to services called by many other services: an auth service that owns tokens, sessions, and identity records is a domain service whose consumers happen to be other services, not an intermediary. Every service either holds authority over its own domain or exists only to access someone else's.

## Accumulated, Not Designed

Positional architecture can be a deliberate choice; when it is, its trade-offs should be known and accepted. More often it arrives uninvited: a facade is added at the boundary for consumer shaping, an orchestrator grows to coordinate a flow no single service owned, an adapter appears for a protocol mismatch. Each decision is reasonable in isolation; the trust model they collectively imply is rarely examined. Drawing boxes first (facade, orchestration, domain service) and fitting the domain into them isn't incompetence; it's applying patterns that were correct answers to specific constraints at some point. The problem isn't the reasoning; it's that the question being answered is not the question the system has.

Copying the form of something successful without understanding what made it successful compounds this. Netflix, Uber, and their peers arrived at architectural complexity through years of growth that created specific, observable problems. They earned those layers by living with the pain that justified adding them. Teams that copy the pattern have a new domain they don't fully understand yet, a team size that doesn't need those independence guarantees, and a system that hasn't yet revealed where the real scaling pressure will sit. SOA was a response to the monolith's inability to scale independent team ownership. Microservices were a response to SOA's heavyweight contracts. API gateways and orchestration layers were added to manage the complexity microservice proliferation introduced. Each solution created the conditions for the next problem, adding another layer of network-boundary decomposition on the last. The question that short-circuits this is almost never asked: what evidence do we have that this layer delivers value a simpler design wouldn't?

The enterprise service bus is the clearest historical example. It was not primarily an orchestration pattern; it was a resource efficiency pattern. Organizations in the SOA era were operating expensive physical infrastructure where centralizing message routing let many services share costly computing capacity, and on-premises a single hardware gateway handled both internet ingress and internal service-to-service traffic. **Orchestration was an artifact of that centralization.** Cloud removes both constraints: per-service provisioning is economically trivial, and internal calls within a VPC never leave the virtual network. The coordination pattern often persists in new systems, detached from the economics that justified it. An architect is probably not trying to rebuild an ESB; they are incorrectly applying a coordination pattern learned when it was the correct answer to a real constraint.

## What Positional Architecture Costs

The costs compound predictably as the system grows:

- Debugging requires tracing the entire layer topology; what looks like a one-hour fix often takes a day once hop-tracing is factored in
- Change velocity slows because a domain model change requires coordinated updates across every dependent layer, turning internal changes into multi-team coordination exercises
- Testing multiplies because you need unit tests at each layer, contract tests between layers, and integration tests across the full stack
- Infrastructure costs compound because you're running compute and paying for network traffic at every layer, sometimes several times per external request
- Capacity planning is nonlinear because one unit of external load fans out to multiple internal calls with different resource profiles at each layer

The most common failure mode is not shared code, but shared call chains: every consumer request travels through the same intermediary services in the same order, and every intermediary couples to the services below it. The layers are separate deployments with separate teams, but a change in any domain service propagates upward through every adapter and facade that depends on it, exactly as it would in a tightly coupled monolith. Every positional system carries the full cost of distributed architecture (separate deployments, coordinated releases, network hops) without the independence those costs were supposed to buy.

Identity-oriented architecture enforces a discipline that prevents this. A consumer calls a domain service directly; that service may call one or more supporting services, but the chain ends there. Flatten the call chain to one hop and each service can be reasoned about, scaled, and deployed on its own terms.

At sufficient coupling depth, a true monolith is more defensible: it at least eliminates network hops, serialization overhead, and the coordination cost of deploying multiple services to ship a single feature. Those costs are the price of independence. When independence was never achieved, the price is paid with nothing received in return.

## The Asymmetric Security Posture of Positional Systems

A positional system built to its full specification is the most controlled environment available: mutual TLS on every hop, audit logging at every tier, explicit authorization at each layer. The security problem is not the model. It is the belief that sustains the model, and what that belief implies about where security effort should be concentrated.

In a positional system, a service's authority comes from its layer placement. Its identity, such as it has one, is its tier: facade-tier service, orchestration-tier service, domain-tier service. When that service authenticates to call another, the most natural credential is one that proves it belongs to the trusted network: a cert granted by the internal CA, a service mesh identity that says "internal." That credential proves network citizenship, not bounded identity. It answers "are you one of us?" rather than "are you specifically OrderService with authority over orders?" The credential reflects the architecture's actual belief: legitimacy comes from position, not from ownership.

Teams in positional systems concentrate security effort at the edge because the edge is where external callers prove they belong. Everything behind it applies implicit trust, because belonging to the internal network already proved legitimacy. This is not a discipline failure; it is the architecture's trust model applied consistently.

That trust model is exactly what attackers exploit. A single vulnerability such as server-side request forgery, request smuggling, or a compromised internal service gives access to the entire soft interior. The blast radius is the full internal network, not the narrow scope of whatever was actually breached: the difference between rotating one service's credentials and conducting a full incident response across every internal system.

The counter-argument is that service meshes like Istio and Linkerd can retrofit mutual TLS and per-hop authentication onto a positional system without changing service code. That solves authentication, not authorization. A mesh-issued cert says "authenticated internal service." It does not say "OrderService, authorized for these operations on order data." A compromised internal service holds an equally valid cert; the mesh cannot tell the difference because the credential encodes network membership, not bounded ownership. The mechanism changed; what it proves didn't.

The distinction is clearance versus need-to-know. A top secret clearance does not entitle the holder to read everything at or below that classification level. Access to a specific piece of information still requires a specific reason: a bounded, demonstrable need for this information in this context. Clearance is necessary but never sufficient. A service mesh cert that proves "authenticated internal service" is a clearance. It proves tier membership and nothing else; it says nothing about what the caller owns or why this specific access is legitimate for this operation. Positional architectures issue clearances and treat them as sufficient authorization. Identity-oriented architectures demand need-to-know: a specific, bounded authority claim that makes this access legitimate for this actor in this context, independent of where that actor sits in the network.

Identity-oriented architecture inverts this at the root. Every service presents credentials that prove a specific bounded identity: not "I'm internal" but "I'm OrderService, authorized for these operations on order data." A compromised component can only act within its authorization scope. The security model and the architectural model are aligned because they share the same belief: legitimacy comes from what you are, not from where you sit. In practice, a caller authenticates against an identity provider, receives a short-lived token scoped to its bounded authority, and presents it directly to the domain service; the service validates scope against the requested operation, with no intermediate hop in the path.

### The Attack Surface Objection Is Circular

A common gut response is that identity-oriented architecture increases the attack surface by exposing domain services directly.

Attack surface is a count of publicly reachable endpoints, and nothing about positional architecture bounds that count. A positional system can grow its public layer without end; every new consumer-facing feature adds endpoints regardless of whether intermediary tiers exist. Intermediary tiers sit behind those public endpoints, not instead of them; they add internal endpoints, not replace external ones.

In an identity-oriented system, rate limiting, IP flagging, geographic constraints, and gateway-level checks apply everywhere without exception, because there is no interior to fall back on. There is no class of endpoint that gets lighter treatment because a perimeter supposedly already handled it. Positional architecture doesn't make the public layer more secure than a well-secured identity-oriented one; it adds internal layers that receive implicit trust, while the identity-oriented system applies the same controls to every surface.

## Team Ownership

Positional architecture tends to produce horizontal teams organized around the layers themselves. The backend team owns domain services, the platform team owns orchestration, the API team owns the external facade. Each team's incentives point inward; the backend team is rewarded for internal quality, not consumer outcomes, and the orchestration team optimizes for the calls it coordinates rather than the features consumers need. Every capability that crosses a layer boundary requires coordination, negotiation, and synchronized releases.

This is Conway's Law expressed architecturally: organizations design systems that mirror their communication structures, then their communication structures solidify around those systems. The result is teams in conflict about the architecture rather than the product. Who owns the latency that appeared between the orchestrator and the domain service? Whose responsibility is it when the contract between the facade and the adapter breaks? These arguments look like culture problems when they're actually architectural ones. The clearest sign that an architecture is serving itself rather than its system is when teams spend more time reasoning about which layer a change belongs to than building the change.

## The Discipline Objection

The most common response to this argument is that teams with strong governance, comprehensive testing, and mature observability practices can operate positional systems effectively, making architecture a secondary concern. A well-governed positional system beats an undisciplined identity-oriented one. Penetration testing, contract testing between layers, distributed tracing across hops: these practices work, and teams that apply them consistently can operate positional systems at scale.

The objection treats discipline as an architectural substitute, and it isn't. Both architectural styles require those disciplines. The difference is what those disciplines cost when you add layers. In a positional system, discipline gets applied across a dependency graph that's hard to reason about; a change at any hop can ripple through every connected hop, and the connections aren't visible without tracing the whole topology. In an identity-oriented system, the dependency graph is a set of direct, declared calls between services that authenticate each other, and the discipline a team applies to its own domain stays local. Both options require the same investment. One multiplies the cost of every discipline across a dependency graph that grows harder to reason about with every layer added.

## When Positional Architecture Earns Its Cost

The cases where positional architecture earns its cost are narrower than commonly assumed. Fully realized, with the controls described above, it produces the most demonstrably auditable environment available. Those controls work. The cost of reaching and maintaining them needs to deliver value a simpler design would not.

The one other scenario that legitimately forces a specific boundary component is integration with systems outside your change control: acquisitions, partner APIs, and legacy systems that can't be modified to support identity-oriented calls. A facade at that boundary isn't a commitment to positional architecture; it's a quarantine forced by external constraints, scoped to one boundary.

The problem is that almost no organization that uses positional architecture has consciously committed to it. Teams arrive at it through cargo-culting, inherited decisions, or compliance requirements that turn out to be softer than presented. PCI-DSS mandates network isolation for the Cardholder Data Environment specifically, not for architectures generally. HIPAA, SOX, and GDPR impose no network topology requirements at all. The pressure comes from auditors trained on perimeter models, not from the text of the frameworks themselves. The controls arrive later, applied unevenly, because the architecture doesn't enforce them and delivery pressure consistently wins.

## Conclusion

Does legitimacy come from who you are, or from where you sit? Positional architecture defaults toward position as the answer; identity-oriented architecture answers with ownership, and communication structure follows from that rather than preceding it. A system built to control communication paths will keep needing to control them as the domain evolves, because the structure was never derived from the domain.

Positional architecture is not the wrong answer. It becomes the wrong answer when it arrives by default rather than by deliberate commitment, when teams inherit the cost without making the trade-off explicit. A system that earns its layers by living with the problems they solve is a different thing from one that inherits them from a diagram.
