---
layout: guide
title: "Architecture Foundations"
category: Architecture
subcategory: Foundations
description: "Essential principles of software architecture including trade-off analysis, architectural thinking, modularity patterns, and the difference between architecture and design."
---

# Architecture Foundations

## Core Laws

> 1. **Everything in software architecture is a trade-off**
> 2. **Why is more important than how**
> 3. **Most decisions exist on a spectrum, not binary choices**
> -- Mark Richards & Neal Ford

**Architecture** consists of:

- **Structure**: System components and relationships
- **Characteristics**: Capabilities the system must deliver
- **Components**: Behavioral building blocks
- **Style**: Implementation pattern and topology
- **Decisions**: Rules and constraints guiding construction

## Architectural Thinking

### Architecture vs Design

**Architecture** = Strategic, long-term, hard to change, significant trade-offs
**Design** = Tactical, short-term, easier to change, fewer trade-offs

Ask yourself: How much planning? How many people affected? Long-term vision or short-term action?

### Technical Breadth vs Depth

Architects need **breadth** (knowing a little about many things) over **depth** (expertise in one area).

**Goal**: Move things from "unknown unknowns" → "known unknowns" → "knowns" (when needed)

**Common Dysfunctions**:

- Trying to maintain expertise in too many areas → burnout
- **Stale expertise**: Outdated knowledge treated as current
- **Frozen Caveman antipattern**: Reverting to irrational past-trauma concerns instead of objective assessment

### Core Skills

**Trade-Off Analysis**:

> "Programmers know the benefits of everything and the trade-offs of nothing. Architects need to understand both." -- Rich Hickey

Everything has trade-offs. The answer is often "it depends" on: environment, business drivers, culture, budgets, timelines, skills.

**Business Translation**:

Translate business requirements → architecture characteristics (scalability, performance, availability)

Common business justifications: **Cost** | **Time to market** | **User satisfaction** | **Strategic positioning**

**Hands-On Coding Balance**:

Avoid the **Bottleneck Trap**: Don't own critical-path code. Delegate framework code; focus on minor features 1-3 iterations ahead.

Stay hands-on via: POCs | Technical debt | Bug fixes | Automation | Code reviews

---

## Modularity & Coupling

### Cohesion (Best → Worst)

1. **Functional**: Everything essential together
2. **Sequential**: Output → Input chain
3. **Communicational**: Shared communication
4. **Procedural**: Specific execution order
5. **Temporal**: Related only by timing
6. **Logical**: Logically but not functionally related
7. **Coincidental**: Unrelated (worst)

### Coupling Metrics

**Afferent (incoming)**: Dependencies on this component
**Efferent (outgoing)**: This component's dependencies

**Key Metrics**:

- **Abstractness**: Abstract / Concrete ratio
- **Instability**: Efferent / (Efferent + Afferent)
- **Distance from Main Sequence**: Balance of abstractness & instability
  - Zone of Uselessness: Too abstract
  - Zone of Pain: Too concrete

### Connascence

Describes coupling types more precisely than simple metrics.

**Static (source-code)**:

- **Name**: Agree on names
- **Type**: Agree on types
- **Meaning**: Agree on value meanings
- **Position**: Agree on parameter order
- **Algorithm**: Agree on algorithms

**Dynamic (runtime)**:

- **Execution**: Order matters
- **Timing**: Timing matters (race conditions)
- **Values**: Multiple values change together
- **Identity**: Reference same entity

**Properties**:

- **Strength**: Ease of refactoring
- **Locality**: How close modules are
- **Degree**: Size of impact

**Improvement Strategy**:

1. Minimize overall connascence
2. Minimize across boundaries
3. Maximize within boundaries

---

## Architecture Characteristics

### Definition Criteria

Must meet three criteria:

1. Specify non-domain consideration
2. Influence structural design
3. Be critical to success

### Categories

**Operational**: Availability | Continuity | Performance | Recoverability | Reliability | Robustness | Scalability

**Structural**: Configurability | Extensibility | Maintainability | Portability | Upgradeability

**Cloud**: On-demand scalability | On-demand elasticity | Zone-based availability | Region-based privacy

**Cross-Cutting**: Accessibility | Authentication | Authorization | Legal | Privacy | Security | Supportability

### Selection Process

1. Start with explicit requirements
2. Identify implicit needs
3. Focus on trade-offs and priorities
4. **Limit to 3-7 characteristics** (the magic number)

### Measuring & Governing

**Challenges**: Vague definitions, varying interpretations, too composite

**Solutions**:

- **Operational**: Performance metrics, response times
- **Structural**: Cyclomatic complexity (target: <5, acceptable: <10), code metrics
- **Process**: Test coverage, deployment success rates
- **Fitness Functions**: Automated integrity assessments

---

## Architecture Quantum

The smallest part of the system that runs independently.

**Requirements**:

- Independent deployment
- High functional cohesion (does something purposeful)
- Synchronous connascence within boundaries

**Determines**: Single quantum (monolith) vs multiple quanta (distributed)

---

## Partitioning Strategies

### Technical Partitioning

Organized by technical capabilities (presentation, business, persistence).

**Pros**: Clear technical separation, aligns with layered patterns
**Cons**: High global coupling, scattered domain concepts, difficult data migration

### Domain Partitioning

Organized by business domains/workflows (DDD approach).

**Pros**: Models business, easier cross-functional teams, simpler distributed migration
**Cons**: Customization appears in multiple places

### Conway's Law

> "Organizations design systems that mirror their communication structures"

Team structure influences architecture. Domain-partitioned works best with cross-functional teams; technical-partitioned often creates barriers.

---

## Distributed Computing

### Fallacies to Avoid

1. Network is reliable → Plan for failures
2. Latency is zero → Measure and optimize
3. Bandwidth is infinite → It's limited and costly
4. Network is secure → Secure everything
5. Topology never changes → Stay coordinated
6. One administrator → Many; communicate widely
7. Transport cost is zero → Infrastructure is expensive
8. Network is homogeneous → Plan for incompatibility
9. Versioning is easy → Complex; plan carefully
10. Compensating updates work → Have limitations
11. Observability is optional → Critical for debugging

### Monolith vs Distributed Decision

**Choose Distributed when**:

- Different parts need different characteristics
- High scalability/availability required
- Teams need independent deployment
- Domain boundaries are clear

**Choose Monolithic when**:

- Single characteristic set suffices
- Simpler deployment preferred
- Smaller team/scope
- Cost/complexity must minimize

---

## Team Topologies

**Stream-Aligned Teams**: Focus on single business domains. Move quickly delivering discrete value.

**Enabling Teams**: Bridge capability gaps. Provide research, learning, specialized knowledge.

**Complicated-Subsystem Teams**: Handle highly specialized systems requiring deep expertise. Reduce cognitive load.

**Platform Teams**: Provide self-service APIs, tools, services as internal product foundation.

---

## Quick Reference

### Decision Framework

| Question | Monolith | Distributed |
|----------|----------|-------------|
| Different characteristics per part? | No | Yes |
| Scalability critical? | Low-Medium | High |
| Deployment independence? | No | Yes |
| Clear domain boundaries? | No | Yes |
| Team size | Small | Multiple teams |

### Coupling Reduction Checklist

- [ ] Minimize connascence across service boundaries
- [ ] Maximize cohesion within components
- [ ] Prefer domain partitioning for distributed systems
- [ ] Limit architecture characteristics to 3-7
- [ ] Measure coupling with afferent/efferent metrics

### Key Metrics

**Cyclomatic Complexity**: Target <5, Acceptable <10
**Architecture Characteristics**: Limit to 3-7
**Connascence**: Minimize across boundaries, maximize within

---
