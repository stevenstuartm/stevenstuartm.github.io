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
>
> -- Mark Richards & Neal Ford, *Fundamentals of Software Architecture* (2020)

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

*Concept introduced by Meilir Page-Jones (1992), popularized in software architecture by Jim Weirich and Kevin Rutherford*

Describes coupling types more precisely than simple metrics. Two components are connascent if changing one requires changing the other to maintain correctness.

**Static (source-code level)**:

- **Name**: Components must agree on entity names (e.g., method names, variable names)
  - *Example*: Renaming a method requires updating all call sites
- **Type**: Components must agree on data types
  - *Example*: Changing parameter from `int` to `String` breaks callers
- **Meaning**: Components must agree on the meaning of values
  - *Example*: Both must interpret `status = 1` as "active"
- **Position**: Components must agree on parameter order
  - *Example*: `calculateTotal(price, tax)` vs `calculateTotal(tax, price)`
- **Algorithm**: Components must agree on a particular algorithm
  - *Example*: Both encryption and decryption must use same algorithm

**Dynamic (runtime level)**:

- **Execution**: Order of execution matters
  - *Example*: Must call `connect()` before `sendData()`
- **Timing**: Timing of execution matters (race conditions)
  - *Example*: Two threads accessing shared state without synchronization
- **Values**: Multiple values must change together
  - *Example*: Updating width requires updating height to maintain aspect ratio
- **Identity**: Components must reference the same entity
  - *Example*: Multiple services must point to the same user record

**Properties** (used to evaluate connascence):

- **Strength**: Ease of refactoring (name < type < meaning < position < algorithm)
- **Locality**: How close modules are (connascence within a module is less problematic than across services)
- **Degree**: Size of impact (how many components are affected)

**Improvement Strategy**:

1. Minimize overall connascence in the system
2. Minimize connascence across architectural boundaries
3. Maximize connascence within boundaries (high cohesion)

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

**Fitness Functions** (*evolutionary architecture concept by Neal Ford, Rebecca Parsons, and Patrick Kua*):

Objective integrity assessments of architecture characteristics. Like unit tests for architecture.

*Examples*:
- Performance: Automated tests failing if response time >200ms
- Modularity: Tests failing if cyclomatic complexity >10
- Dependency: Tests failing if service calls forbidden dependencies
- Security: Tests failing if vulnerabilities detected in dependencies

---

## Architecture Quantum

*Concept from Mark Richards & Neal Ford's Fundamentals of Software Architecture (2020)*

An independently deployable artifact with high functional cohesion and synchronous connascence. In simpler terms: the smallest useful piece of the system that can be deployed on its own.

**Requirements**:

- **Independent deployment**: Can be deployed without deploying other parts
- **High functional cohesion**: Does something purposeful and complete
- **Synchronous connascence**: All parts within the quantum that must work together synchronously

**Examples**:

- **Single quantum (monolith)**: Entire e-commerce application deployed as one unit
- **Multiple quanta (microservices)**: Separate Order Service, Payment Service, Inventory Service each deployable independently
- **Hybrid**: Modular monolith with separate background job processor (2 quanta)

**Why it matters**: Determines architectural style, deployment strategy, scalability approach, and team organization. More quanta = more flexibility but more operational complexity.

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

> "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure."
>
> -- Melvin Conway (1967)

Often paraphrased as: "Organizations design systems that mirror their communication structures."

**Implication**: Team structure directly influences architecture. Domain-partitioned architectures work best with cross-functional teams; technical-partitioned architectures often create communication barriers between layers.

**Inverse Conway Maneuver**: Deliberately structure teams to encourage the desired architecture.

---

## Distributed Computing

### Fallacies of Distributed Computing

*Originally identified by Peter Deutsch (1994), later expanded by James Gosling and others at Sun Microsystems*

False assumptions developers make about distributed systems that lead to problems:

1. **Network is reliable** → Networks fail; use retries, timeouts, circuit breakers
2. **Latency is zero** → Network calls are orders of magnitude slower than local calls; minimize round trips
3. **Bandwidth is infinite** → It's limited and costly; be mindful of payload sizes
4. **Network is secure** → Secure everything: encrypt in transit, authenticate, authorize
5. **Topology doesn't change** → Services move, scale, fail; use service discovery
6. **There is one administrator** → Many teams manage different parts; coordinate changes
7. **Transport cost is zero** → Infrastructure, bandwidth, serialization all have costs
8. **Network is homogeneous** → Mix of hardware, OSs, network equipment; handle incompatibilities

*Additional modern considerations*:

9. **Versioning is easy** → Complex in production; plan for backward compatibility
10. **Compensating transactions always work** → They have limitations; some operations aren't reversible
11. **Observability is optional** → Critical for debugging distributed systems; invest early

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

*Framework by Matthew Skelton and Manuel Pais from "Team Topologies" (2019)*

Four fundamental team types for organizing software delivery:

**Stream-Aligned Teams**: Aligned to a flow of work from a business domain
- Focus on single business domains
- Move quickly delivering discrete value
- Primary team type in most organizations

**Enabling Teams**: Bridge capability gaps across stream-aligned teams
- Provide research, learning, specialized knowledge
- Help teams overcome obstacles
- Temporary assistance, not permanent dependencies

**Complicated-Subsystem Teams**: Build and maintain systems requiring specialized knowledge
- Handle highly specialized systems requiring deep expertise
- Reduce cognitive load on stream-aligned teams
- Examples: video processing, mathematical algorithms, real-time trading engines

**Platform Teams**: Provide internal products that accelerate stream-aligned teams
- Self-service APIs, tools, services as internal product foundation
- Reduce burden on stream-aligned teams
- Treat other teams as customers

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
