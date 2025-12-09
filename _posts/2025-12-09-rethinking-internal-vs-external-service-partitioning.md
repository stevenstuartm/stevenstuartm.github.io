---
title: "Rethinking Internal vs External Service Partitioning"
date: 2025-12-09
description: "The question of how to separate internal from external service layers assumes the separation should exist. Often it shouldn't, and when it does, the answer is simpler than a whole new service tier."
series: "Architecture Insights"
tags: [architecture, microservices, ddd, api-design, distributed-systems]
---

Someone recently asked me something that surfaces constantly in service architecture discussions:

*"How do you separate internal endpoint protocols from external public APIs without duplicating logic?"*

It's a good question, and one I've wrestled with on multiple systems. But before I answer it directly, I want to step back and examine an assumption baked into the question itself: that internal and external service layers *should* be separated as a default architectural stance.

I don't think they should, and understanding why changes how you'd answer the original question.

<blockquote class="pull-quote">
<p>The question isn't how to separate internal from external services cleanly. It's whether you need the separation at all.</p>
</blockquote>

## What This Argument Is Not About

To be clear about scope: this argument is against a blanket internal service tier that always sits between external APIs and your domain services. It's not an argument against app-specific APIs that serve legitimate purposes.

A Backend-for-Frontend that aggregates data for a mobile app, an internal operations tool with its own auth provider, or a partner portal with specialized authorization requirements are all valid. These exist because they serve distinct clients with distinct needs, not because someone decided to create an "internal" tier. These APIs don't prevent other consumers from accessing the underlying services directly. They're additional entry points, not mandatory chokepoints.

What we're arguing against is the pattern where every external request must flow through an internal tier, where the internal tier duplicates logic that belongs in domain services, and where the existence of the tier leads teams to treat it as the place where things happen rather than a thin translation layer.

## The Costs Nobody Budgeted For

When teams introduce an internal service layer distinct from their external APIs, they're often optimizing for a threat model they haven't articulated. What they get instead is a set of costs that compound over time.

### The Obvious Costs

These are typically acknowledged but waved away as "the price of good architecture":

**Latency increases.** Every call now traverses an additional network hop. What was a function call becomes a serialization-deserialization round trip with all the failure modes that entails.

**Infrastructure duplicates.** The internal tier needs its own load balancers, monitoring, alerting, and capacity planning. None of this is free, and none of it adds business value.

**Deployment pipelines multiply.** Another service means another CI/CD pipeline, another set of environments, another thing to coordinate during releases.

### The Subtle Costs

These compound faster because they're harder to measure and easier to ignore:

**Security rigor degrades.** Internal services tend toward lower security standards. The reasoning feels sound ("it's behind the firewall, it's just us"), but it produces the crunchy-outside-chewy-inside topology that attackers love. Once the perimeter is breached, lateral movement is trivial.

**Governance diverges.** When you have two tiers, you now have two sets of APIs to govern. Teams often apply rigorous versioning policies and documentation standards to the external tier while treating internal APIs more casually. This isn't inevitable, but the split creates the conditions for it. Without deliberate effort to maintain parity, the internal tier drifts toward informal coordination that doesn't scale.

**Development agility suffers.** Every feature now requires coordinating changes across layers in ways that don't show up on sprint boards. The internal API becomes a bottleneck that every team routes through. What was meant to provide flexibility becomes a coupling point.

**Bounded contexts get undermined.** If you're practicing DDD or building microservices, this should feel especially wrong. The whole point is bounded contexts that own their data and behavior. A centralized internal service layer reintroduces the orchestration and coupling you were trying to escape, recreating the anti-patterns of service-oriented architecture that the industry moved away from for good reasons.

## Anti-Patterns to Recognize

The internal service layer can fail in distinct ways, and conflating them makes the problem harder to diagnose.

### The Gateway Logic Inversion

The external API layer accumulates orchestration and business logic while the actual services become thin data accessors. This recreates the enterprise service bus anti-pattern: the integration layer becomes the brain, and the services become dumb pipes to databases. It happens naturally when teams treat the external API as "the product" and internal services as implementation details.

You'll recognize this when changes to business rules require modifying the API gateway or external layer rather than the owning service. The bounded context no longer owns its behavior; it's been hollowed out into something that just fetches and stores data.

### The Sinkhole

The internal layer exists but adds no value. Requests pass through unchanged, adding latency and failure modes without transformation, validation, or any other justification. This happens when teams try to keep layers thin but still feel obligated to have them. The layer exists because the architecture diagram says it should, not because it serves a purpose.

### The Common Root Cause

These patterns emerge from the same root cause. Teams build the boundary into their application code rather than treating it as infrastructure configuration. Once the layer exists in code, it either attracts logic because it's convenient, or it sits empty because removing it feels like admitting a mistake. Resisting this requires discipline or, better, keeping the layers thin enough that there's nowhere for logic to accumulate and being willing to remove layers that aren't earning their keep.

## When the Split Is Actually Justified

I'm not arguing the separation is never warranted. But the legitimate cases are narrower than common practice suggests. Before introducing the split, ask yourself:

<blockquote class="pull-quote">
<p>What specific threat model or regulatory requirement does this network boundary enforce that cannot be achieved through authentication, authorization, and encryption at the service level?</p>
</blockquote>

If the answer is "defense in depth" or "best practice," that's worth examining more closely. Defense in depth is genuinely valuable, but the question is whether this particular boundary provides meaningful defense or just the appearance of it. A network boundary that leads teams to relax security rigor on internal services isn't defense in depth; it's defense instead of depth. The goal should be strong security at every layer, regardless of where the request originates.

The cases that do justify the split:

**Hard compliance boundaries.** When regulations mandate network segmentation with different audit requirements (PCI-DSS cardholder data environments, HIPAA PHI zones), the compliance cost of not partitioning exceeds the architectural overhead. This is a genuine forcing function, not a design preference.

**Protocol translation that actually matters.** When external consumers legitimately need REST and OpenAPI for tooling compatibility, but internal communication benefits from gRPC and protobuf for performance. Even then, this justifies a thin translation layer at the edge that handles only protocol concerns, not a full "internal services" tier with its own business logic.

**Resale or partner APIs with different SLAs.** When you're exposing functionality to paying customers or partners who expect different availability guarantees, rate limits, or support tiers than internal consumers require. A partner integration API might need stricter input validation, partner-specific data transformations, or detailed audit logging for compliance that would be overhead for internal use. The adapter pattern works well here: the same application core serves both audiences, but the external adapter handles partner-specific contract requirements. Rate limiting and usage metering enforcement still belongs in infrastructure (your API gateway enforces the limits), but the adapter contains the business rules about what limits apply to each partner tier.

## The Duplication That's Actually Desirable

The original question asks about avoiding duplicated logic, which suggests the questioner is likely working in a domain-driven or microservices context where bounded contexts exist. That's also the context where duplication concerns are most nuanced, because DDD expects a degree of duplication across bounded contexts. This is intentional.

A "customer" in order processing carries different attributes and behaviors than a "customer" in case management. These aren't the same entity viewed through different lenses; they're distinct aspects of a larger concept, each owned by the context that cares about them. Trying to unify them into a canonical Customer service is how you get the distributed monolith: every context coupled to a shared definition that fits none of them well.

This sounds like it would proliferate duplication everywhere, but in practice it doesn't. If your granularity, coupling, cohesion, and connascence are well-balanced, these cross-context representations are relatively rare. Most of your domain concepts live entirely within a single context. The ones that span contexts are explicitly modeled as such, with clear translation at context boundaries.

Two kinds of duplication exist in these systems:

<div class="comparison">
<div class="content-card content-card--accent-warning">
<h4>Accidental Duplication (eliminate)</h4>
<ul>
<li>Business rules copy-pasted into multiple places</li>
<li>Validation logic scattered across layers because nobody knew where it belonged</li>
<li>Transformation code that exists only because the architecture forced an unnecessary hop</li>
</ul>
</div>
<div class="content-card content-card--accent">
<h4>Essential Duplication (preserve)</h4>
<ul>
<li>Each bounded context's representation of shared concepts</li>
<li>Intentionally distinct models optimized for different context needs</li>
<li>Clear translations at context boundaries rather than shared definitions</li>
</ul>
</div>
</div>

When your order context and your support context both have a "customer" concept, those aren't copies of the same thing that drifted apart. They're intentionally distinct representations, each optimized for its context's needs.

## Answering the Original Question

Back to what started this: *"How do you separate internal endpoint protocols from external public APIs without duplicating logic?"*

If you genuinely need both internal RPC and external REST, and you've verified that you do, the answer is thin adapters over a shared application core.

```
┌─────────────────────────────────────────┐
│              Adapters                   │
│  ┌─────────┐ ┌─────────┐ ┌───────────┐  │
│  │  REST   │ │  gRPC   │ │  Message  │  │
│  │Adapter  │ │ Adapter │ │  Adapter  │  │
│  └────┬────┘ └────┬────┘ └─────┬─────┘  │
│       │           │            │        │
│       ▼           ▼            ▼        │
│  ┌─────────────────────────────────────┐│
│  │       Application Service           ││
│  │      (protocol-agnostic)            ││
│  └─────────────────────────────────────┘│
│                   │                     │
│                   ▼                     │
│  ┌─────────────────────────────────────┐│
│  │          Domain Model               ││
│  └─────────────────────────────────────┘│
└─────────────────────────────────────────┘
```

The adapters handle protocol serialization, transport-specific error mapping, and request validation that's genuinely protocol-specific (HTTP headers vs gRPC metadata). They do not contain business rules, orchestration logic, or data transformation beyond wire format concerns. If you're familiar with hexagonal architecture or ports and adapters, this is the same principle: the transport mechanism is an implementation detail that shouldn't leak into your domain.

You will have separate DTOs for REST versus gRPC. This isn't duplication; it's appropriate decoupling. Your protobuf messages and OpenAPI schemas should evolve independently based on consumer needs. Trying to share them creates coupling that defeats the purpose of having separate protocols in the first place.

What you share is the domain model and application logic. The mapping from transport DTOs to domain commands and queries is mechanical and belongs in the adapter layer.

### Versioning Lives in the Adapters Too

When external consumers need long-term backward compatibility, the adapter layer handles version translation. Your REST adapter can maintain v1 and v2 endpoints that both map to the same application core:

```
v1 adapter: "fullName" → domain.FirstName + " " + domain.LastName
v2 adapter: "firstName", "lastName" → domain.FirstName, domain.LastName
```

The v1 adapter translates the old contract into current domain operations. When you eventually deprecate v1, you remove one adapter. The domain and application layers never knew the difference.

This also means you don't need to architect for versioning from day one. Start by exposing your services directly. When you actually have external consumers with different compatibility needs, add the adapter. The pattern is something you introduce when the need materializes, not something you speculatively invest in.

Both adapters should call the application service directly. The distinction between internal and external is a deployment and network concern, not an architectural layer. Your load balancer, API gateway, or service mesh can handle routing. Your code shouldn't encode that topology.

## Common Objections

**"What about external-specific concerns like rate limiting, OAuth, API keys, and usage metering?"** These belong in the network and infrastructure layers, not in a separate application service tier. Web application firewalls, API gateways, and service meshes handle rate limiting, traffic shaping, and tenant isolation before requests ever reach your application. OAuth token validation happens at the gateway or in middleware. API key management and usage metering can be handled by the gateway, a sidecar, or adapter-level instrumentation. None of these require a separate internal service layer; they're cross-cutting infrastructure concerns.

**"Isn't this just ignoring defense in depth?"** Defense in depth means security at every layer, not a hard perimeter around a soft interior. If your internal services would be vulnerable without the network boundary protecting them, the boundary is masking a problem rather than solving it. Strong authentication, authorization, and input validation should exist at every service regardless of whether the caller is internal or external.

**"We inherited this architecture. Are you saying we should rewrite everything?"** Not at all. If you have a working system with internal/external separation, the cost of restructuring likely outweighs the benefits. The argument here is against adopting this pattern as a default for new systems. If you're stuck with the split, resist the temptation to add more business logic to it. New features should go in the services that own them, not in the coordination layer between internal and external tiers.

**"External APIs need different versioning strategies. Internal APIs can break freely while external ones need years of backward compatibility."** This question contains two assumptions worth examining.

*"Internal APIs can break freely."* Breaking changes are expensive for any consumer, internal or external. Internal teams that have to constantly adapt to upstream changes are teams not delivering their own roadmap. Good API design minimizes breaking changes regardless of audience:

- **Additive changes**: New fields don't break existing consumers
- **Optional fields**: Consumers ignore what they don't need
- **Careful deprecation**: Warn before removing, give migration time

These practices work for internal consumers just as well as external ones. If your internal APIs break frequently, the problem is design discipline, not a missing architectural layer.

*"External APIs need years of backward compatibility."* This is often true, and as discussed above, the adapter layer handles version translation. A separate internal service tier doesn't help with versioning; it just adds another place where version mismatches can occur.

**"Don't external APIs need to hide internal fields or shape data differently?"** This is already solved by standard API design practices that apply regardless of architecture. You should be using DTOs rather than exposing domain models directly, surrogate keys or UUIDs rather than internal database IDs, and endpoint-specific authorization for sensitive fields. None of this requires a separate service tier; it's just good API hygiene for any endpoint. If you genuinely need different response shapes for different consumers, that's exactly what thin adapters handle without duplicating business logic.

**"But doesn't a network boundary provide real security value for auditing and access control?"** If your security model depends on the network boundary, you have a fragile security model. Internal services should authenticate callers, authorize operations, validate inputs, and audit access exactly as external services do. The tooling exists: service meshes provide mTLS and identity propagation, authorization can be policy-based at every service, and audit logging doesn't care whether the request came from inside or outside the network. The internal/external split often *weakens* security by creating a false sense of safety ("it's internal, we don't need to be as careful"). The breaches that make headlines typically involve lateral movement after an attacker gets past the perimeter. Strong security at every layer isn't just good practice for external APIs; it's the only model that survives contact with a determined attacker.

**"What about app-specific APIs like a Backend-for-Frontend or an internal operations tool?"** As discussed in "What This Argument Is Not About," these are different from an internal service tier. App-specific APIs exist to serve particular clients with distinct needs. They're additional entry points, not gatekeepers that everything must flow through. The distinction matters: an ops tool with its own auth provider is just another consumer of your services, not a blanket internal layer that hides everything behind it.

## Conclusion

The external/internal service layer split has legitimate use cases, but they're narrower than common practice suggests. What often happens instead is that the split recreates the very problems modern architecture was supposed to solve:

- **The enterprise service bus anti-pattern**: logic accumulating in the boundary layer
- **The sinkhole**: layers that exist on diagrams but add no value
- **The crunchy-outside-chewy-inside security model**: the topology attackers exploit

The tradeoffs don't disappear just because your reasoning is sound. These failure modes are the same ones that plagued legacy architectures, and no amount of clever design eliminates the underlying tension.

Before adopting this pattern as a default, ask what problem you're actually solving and what tradeoffs you're willing to accept. When you do need multiple protocols or entry points, keep the adapters thin and let them share the same application core.

<blockquote class="pull-quote">
<p>Often the better answer isn't a clever way to share code between layers; it's recognizing that the layers might not need to exist as separate things in the first place.</p>
</blockquote>
