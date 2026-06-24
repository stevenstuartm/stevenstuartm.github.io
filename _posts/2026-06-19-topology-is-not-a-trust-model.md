---
layout: post
title: "Topology Is Not a Trust Model"
date: 2026-06-19
description: "What makes a service request legitimate? Most teams treat it as an authentication question, but the answer is also an architectural one. One school of thought grants legitimacy by placement; the other demands it be earned through verified ownership. Both beliefs shape the credential model and the service structure simultaneously."
tags: [architecture, api-design, distributed-systems, security, design-patterns, microservices]
---

Every service request arrives with the same question: what makes this request legitimate? 

Most teams treat this solely as an authentication problem, but the answer reaches much further than that. It shapes how services are structured, where trust boundaries are drawn and defended, and how teams own their work.

Two schools of thought answer the question differently:

- One answer is the claim of relative position. A request is legitimate because it arrived from the right place, to the right place: from behind the perimeter, through the right intermediaries, from a subnet the architecture trusts, or toward a service that grants access on that same basis. This is **positional architecture**: legitimacy granted by placement.
- The other answer is verified identity and, as such, bounded authority. A request is legitimate because the caller has proven who it is and what it is authorized to do. Credentials name its bounded scope, not just its network address. This is **identity-oriented architecture**: legitimacy earned by ownership. Every service validates every caller the same way, and all services relate to each other as **peers** with clear, **bounded authority** over their own domains.

The contrast between **Bounded Authority** and **Positional Claim** is not as simple as a separate authentication decision and a separate architecture decision. It typically reflects a single belief about where legitimacy comes from, and that belief determines where authority lives in the system, how teams own their work, and whether the system can adapt as the domain evolves.

In practice, a system's answer at the client boundary and its answer internally are independent choices; a system can be identity-oriented externally and positional internally, or vice versa. The underlying belief tends to be consistent even when the implementation differs. This post focuses on internal architecture, where that belief determines the most profound trade-offs.

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

This is **positional architecture**. The checkout client never calls the domain services directly; it calls a chain of intermediary services, each owned by a different team, each a separate deployment with its own logs and its own points of failure. Auth happens once, at the edge; everything behind it is trusted because it arrived from the right place.

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

Authority is ownership: a domain service holds the canonical representation of its data, the validation rules governing it, and the contract it exposes. When multiple components claim authority over the same facts, each enforces subtly different rules. No component is the definitive answer, and the drift between them is slow, then sudden.

The most compelling argument for adding an orchestration layer is avoiding the death star: an uncontrolled web of lateral calls between peer services where no component owns the full decision. Cascading call chains are a sound instinct; calls should flow down through the domain, not sideways across peer services. The problem is not the goal; it is the implementation. Positional architecture uses layer placement to enforce the cascade, but placement without authority creates pass-through components that fragment the very authority they were supposed to preserve. When authority has broken down, sideways calls become necessary because no single component owns the full decision.

Bounded authority inverts this: a service with tight, well-named scope has no need to reach sideways for decisions it already owns. When one bounded domain genuinely needs to coordinate with another, the call is direct and well-understood. The concern about sibling calls disappears when those siblings are precisely named and their authority is unambiguous. The tangled dependencies of a death star emerge from many poorly bounded components, not from well-bounded ones communicating directly.

What also disappears is the need to engineer cascade depth; the shallow call stack is a diagnostic, not a design target. Domain workers, async processors that extend a domain's own authority rather than crossing into another's, handle deeper processing without adding managed service hops. The managed call stack stays shallow not by design but as a consequence of services that own their decisions completely. At scale, a composite domain that coordinates sub-domains can produce a similar structure. What makes it legitimate is that every participant holds genuine authority over its own concern, not that it occupies the correct layer position.

Identity-oriented architecture enforces bounded authority structurally by removing intermediaries that would otherwise fragment it. Every caller presents credentials naming its bounded scope; services without a clear domain claim have no legitimate place to sit. Every service either holds authority over its own domain or exists only to access someone else's.

## Accumulated, Not Designed

Positional architecture can be a deliberate choice; when it is, its trade-offs should be known and accepted. More often it arrives through one of a few recurring paths, each reasonable on its own terms, none of which examined the trust model they were collectively building.

- **Organic accumulation** — a facade added for consumer shaping, an orchestrator grown to coordinate a flow no single service owned, an adapter added for a protocol mismatch. Each decision was reasonable when made; the architecture they collectively implied was not.
- **Pattern cargo-culting** — Netflix and Uber earned their layers by living through the specific, observable problems that justified them. Teams that copy the pattern have a new domain, a smaller team, and a system that hasn't revealed where the real scaling pressure will sit.
- **Historical misapplication** — the enterprise service bus was not an orchestration pattern; it was a resource efficiency pattern rooted in the economics of shared physical infrastructure. **Orchestration was an artifact of that centralization.** Cloud removes both constraints, but the coordination pattern persists in new systems, detached from the economics that justified it.
- **Compliance overreach** — PCI-DSS mandates network isolation for the Cardholder Data Environment specifically, not for architectures generally. HIPAA, SOX, and GDPR impose no network topology requirements at all. The pressure comes from auditors trained on perimeter models, not from the text of the frameworks themselves.

The cases where positional architecture genuinely earns its cost are narrow. Fully realized with the controls described above, it produces the most demonstrably auditable environment available; that level of control needs to deliver value a simpler design would not. The one scenario that legitimately forces a specific boundary component is integration with systems outside your change control: acquisitions, partner APIs, and legacy systems that can't support identity-oriented calls. A facade at that boundary is a quarantine scoped to one boundary, not a commitment to positional architecture throughout the system. Almost every other use arrived through one of the paths above, and the controls that would justify it arrive later, applied unevenly, because delivery pressure consistently wins.

## What Positional Architecture Costs

The costs compound predictably as the system grows:

- Debugging requires tracing the entire layer topology; what looks like a one-hour fix often takes a day once hop-tracing is factored in
- Change velocity slows because a domain model change requires coordinated updates across every dependent layer, turning internal changes into multi-team coordination exercises
- Testing multiplies because you need unit tests at each layer, contract tests between layers, and integration tests across the full stack
- Infrastructure costs compound because you're running compute and paying for network traffic at every layer, sometimes several times per external request
- Capacity planning is nonlinear because one unit of external load fans out to multiple internal calls with different resource profiles at each layer

The real coupling is not shared code but shared call chains: every consumer request travels through the same intermediary services in the same order, and every intermediary couples to the services below it. The layers are separate deployments with separate teams, but a change in any domain service propagates upward through every adapter and facade that depends on it, exactly as it would in a tightly coupled monolith. Every positional system carries the full cost of distributed architecture, including separate deployments, coordinated releases, and network hops, without the independence those costs were supposed to buy.

Identity-oriented architecture enforces a discipline that prevents this. A consumer calls a domain service directly; that service may call one or more supporting services, but the chain ends there. Flatten the call chain to one hop and each service can be reasoned about, scaled, and deployed on its own terms.

At sufficient coupling depth, a true monolith is more defensible: it at least eliminates network hops, serialization overhead, and the coordination cost of deploying multiple services to ship a single feature. Those costs are the price of independence. When independence was never achieved, the price is paid with nothing received in return.

## The Asymmetric Security Posture of Positional Systems

A positional system built to its full specification is the most controlled environment available: mutual TLS on every hop, audit logging at every tier, explicit authorization at each layer. The security problem is not the model; it is the belief that sustains the model and what that belief implies about where security effort should be concentrated.

### Network Membership Is Not Identity

In a positional system, a service's authority comes from its layer placement. Its identity is its tier: facade-tier service, orchestration-tier service, domain-tier service. When that service authenticates to call another, the most natural credential is one that proves it belongs to the trusted network: a cert granted by the internal CA, a service mesh identity that says "internal." That credential proves network citizenship, not bounded identity. It answers "are you one of us?" rather than "are you specifically OrderService with authority over orders?" The credential reflects the architecture's actual belief: legitimacy comes from position, not from ownership.

The positional claim works symmetrically: a caller presents legitimacy by arriving from the right place, and a service grants it by sitting in the right place. Network membership is the credential in both directions.

Teams in positional systems concentrate security effort at the edge because the edge is where external callers prove they belong. Everything behind it applies implicit trust, because belonging to the internal network already proved legitimacy. This is not a discipline failure; it is the architecture's trust model applied consistently.

That trust model is exactly what attackers exploit. A single vulnerability such as server-side request forgery, request smuggling, or a compromised internal service gives access to the entire soft interior. The blast radius is the full internal network, not the narrow scope of whatever was actually breached: the difference between rotating one service's credentials and conducting a full incident response across every internal system.

### Authentication Is Not Authorization

The counter-argument is that service meshes like Istio and Linkerd can retrofit mutual TLS and per-hop authentication onto a positional system without changing service code. That solves authentication, not authorization. A mesh-issued cert says "authenticated internal service." It does not say "OrderService, authorized for these operations on order data." A compromised internal service holds an equally valid cert; the mesh cannot tell the difference because the credential encodes network membership, not bounded ownership. The mechanism changed; what it proves didn't.

The distinction is clearance versus need-to-know. A top secret clearance does not entitle the holder to read everything at or below that classification level; access to any specific document still requires a demonstrable need for this information in this context. Clearance is necessary but never sufficient. A service mesh cert that proves "authenticated internal service" is a clearance: it proves tier membership and nothing else. Positional architectures issue clearances and treat them as sufficient authorization. Identity-oriented architectures demand need-to-know: a specific, bounded authority claim for this actor in this context, independent of where that actor sits in the network.

Identity-oriented architecture inverts this at the root. Every service presents credentials that prove a specific bounded identity: not "I'm internal" but "I'm OrderService, authorized for these operations on order data." A compromised component can only act within its authorization scope. The security model and the architectural model are aligned because they share the same belief: legitimacy comes from what you are, not from where you sit. In practice, a caller authenticates against an identity provider, receives a short-lived token scoped to its bounded authority, and presents it directly to the domain service; the service validates scope against the requested operation, with no intermediate hop in the path.

### The Attack Surface Objection Is Circular

A common gut response is that identity-oriented architecture increases the attack surface by exposing domain services directly.

Attack surface is a count of publicly reachable endpoints, and nothing about positional architecture bounds that count. A positional system can grow its public layer without end; every new consumer-facing feature adds endpoints regardless of whether intermediary tiers exist. Intermediary tiers sit behind those public endpoints, not instead of them; they add internal endpoints, not replace external ones.

In an identity-oriented system, rate limiting, IP flagging, geographic constraints, and gateway-level checks apply everywhere without exception, because there is no interior to fall back on. There is no class of endpoint that gets lighter treatment because a perimeter supposedly already handled it. Positional architecture doesn't make the public layer more secure than a well-secured identity-oriented one; it adds internal layers that receive implicit trust, while the identity-oriented system applies the same controls to every surface.

## Layer Boundaries Become Team Boundaries

Positional architecture tends to produce horizontal teams organized around the layers themselves. The backend team owns domain services, the platform team owns orchestration, the API team owns the external facade. Each team's incentives point inward; the backend team is rewarded for internal quality, not consumer outcomes, and the orchestration team optimizes for the calls it coordinates rather than the features consumers need. Every capability that crosses a layer boundary requires coordination, negotiation, and synchronized releases.

This is Conway's Law expressed architecturally: organizations design systems that mirror their communication structures, then their communication structures solidify around those systems. The result is teams in conflict about the architecture rather than the product. Who owns the latency that appeared between the orchestrator and the domain service? Whose responsibility is it when the contract between the facade and the adapter breaks? These arguments look like culture problems when they're actually architectural ones. The clearest sign that an architecture is serving itself rather than its system is when teams spend more time reasoning about which layer a change belongs to than building the change.

## The Discipline Objection

The most common response is that teams with strong governance, comprehensive testing, and mature observability can operate positional systems effectively. A well-governed positional system beats an undisciplined identity-oriented one. Penetration testing, contract testing between layers, and distributed tracing across hops all work, and teams that apply them consistently can operate positional systems at scale.

The objection treats discipline as an architectural substitute, and it isn't. Both styles require the same disciplines. The difference is what those disciplines cost when you add layers: in a positional system, a change at any hop can ripple through every connected hop, and the connections aren't visible without tracing the full topology. In an identity-oriented system, the discipline a team applies to its own domain stays local. Both options require the same investment; one multiplies the cost of that investment across a topology that grows with the system.

## Conclusion

Does legitimacy come from who you are, or from where you sit? Positional architecture defaults toward position as the answer; identity-oriented architecture answers with ownership, and communication structure follows from that rather than preceding it. A system built to control communication paths will keep needing to control them as the domain evolves, because the structure was never derived from the domain.

Positional architecture is not the wrong answer. It becomes the wrong answer when it arrives by default rather than by deliberate commitment, when teams inherit the cost without making the trade-off explicit. A system that earns its layers by living with the problems they solve is a different thing from one that inherits them from a diagram.
