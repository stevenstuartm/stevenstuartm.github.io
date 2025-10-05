---
layout: guide
title: "Design & Implementation"
category: Architecture
subcategory: Design
---

# Design & Implementation

## Component Design

### Bounded Contexts (DDD)

**Bounded Context:**

Everything related to a domain portion is visible internally but opaque to other contexts.

Instead of unified entities across the organization (causing coupling), each context creates its own entities and reconciles differences at communication points.

*Example: Each domain has its own Customer class rather than shared organization-wide*

### Coupling Types

**Semantic:**

Natural domain coupling (inventory, catalogs, customers, sales)

**Implementation:**

How you implement dependencies (database choices, service boundaries)

**Static:**

Architecture "wiring"—how services depend on each other

**Dynamic:**

Runtime communication between quanta forming workflows

**Key Principle:**

Low external implementation static coupling between quanta

### Communication Considerations

Synchronous communication is unforgiving in distributed architectures, especially when parts have different characteristics.

Asynchronous has less impact on architecture quanta boundaries.

---

## Component-Based Thinking

Think in **logical components** (not classes) interacting to perform business functions.

### Logical vs Physical Architecture

**Logical:**

- Shows components and interactions
- Matches directory structures and namespaces
- Independent of deployment
- Focus: What the system does

**Physical:**

- Services, UIs, databases
- Deployment topology
- Focus: Where things run

**Best Practice:**

Create logical first, then physical. Logical guides code organization and team guidance.

### Identifying Core Components

**1. Workflow Approach:**

Model major happy-path workflows; identify components from steps.

**2. Actor/Action Approach:**

Identify actors and major actions; derive components from actions.

**3. Avoid The Entity Trap:**

Don't create components based on entities (Customer Manager, Order Manager).

**Entity Trap Problems:**

- Ambiguous names
- Dumping grounds
- Too coarse-grained
- Hard to maintain/test/deploy

**If truly CRUD-based:**

Use CRUD framework instead of architecture.

### Iterative Refinement

1. **Assign User Stories**: Map requirements to components
2. **Analyze Roles**: Ensure cohesion (operations interrelate)
3. **Analyze Characteristics**: Consider scalability, reliability, availability
4. **Iterate**: Refine boundaries and responsibilities

### Component Coupling

**Afferent (Incoming/Fan-in):**

Degree other components depend on this one

**Efferent (Outgoing/Fan-out):**

Degree this component depends on others

**Temporal:**

Nonstatic dependencies (timing/transactions). Hard to detect—found via design docs or error conditions

### Law of Demeter

Components should have limited knowledge of others.

*Note: Doesn't reduce system-wide coupling; redistributes it*

---

## Risk Analysis

### Risk Matrix

**Dimensions:**

1. Impact (Low=1, Medium=2, High=3)
2. Likelihood (Low=1, Medium=2, High=3)

**Score = Impact × Likelihood**

**Risk Levels:**

- 1-2: Low (green)
- 3-4: Medium (yellow)
- 6-9: High (red)

### Risk Assessments

Use architecture characteristics as criteria. Create matrix of characteristics vs context (services, domains, areas).

**Benefits:**

- Considers criteria and context
- Prioritizes effort
- Filters noise
- Tracks risk direction (△ ▽ ○)

### Risk Storming

Collaborative exercise to determine risk within specific dimension.

**Participants:**

Architects + senior developers + tech leads

**Phase 1: Identification (Individual):**

1. Facilitator sends diagram, criteria, logistics
2. Participants analyze independently using risk matrix
3. Write risk on colored sticky notes (green/yellow/red)

**Best Practice:**

Single criterion or context per session

**Phase 2: Consensus (Collaborative):**

1. Post large architecture diagram
2. Place sticky notes on diagram
3. Analyze and reach consensus
4. Consolidate notes
5. **Unproven/unknown tech = highest risk (9)**

**Phase 3: Mitigation (Collaborative):**

1. Identify ways to reduce/eliminate risks
2. Involve business stakeholders (cost vs risk authority)
3. Present options with cost implications
4. Make trade-off decisions

**Bonus:**

Apply to user-story risk in iterations

---

## Diagramming Architecture

### Importance

No matter how brilliant your ideas, if you can't convince managers to fund and developers to build them, they won't happen.

### Representational Consistency

Show relationships before changing views. Show context before details.

### Tools

**Low-fidelity (Early):**

- Whiteboard + phone photo
- Tablet + projector (unlimited canvas, copy/paste, digitized)

**High-fidelity (Final):**

- OmniGraffle, Visio, Lucidchart, Draw.io
- Look for: Layers | Stencils | Magnets (connection points)

**Avoid Irrational Artifact Attachment:**

Time spent ∝ attachment. Use low-fidelity early to enable iteration.

### Standards

**UML (Unified Modeling Language):**

- Created 1980s (Booch, Jacobson, Rumbaugh)
- Still used: Class diagrams, sequence diagrams
- Most types fallen into disuse

**C4 (Context, Container, Component, Class):**

Modern alternative by Simon Brown (2006-2011)

**Levels:**

1. **Context**: Entire system, users, external dependencies
2. **Container**: Physical deployment boundaries
3. **Component**: Component view (architect perspective)
4. **Class**: UML-style class diagrams

**Benefits:**

Active community, templates, keeps up with ecosystem

**ArchiMate:**

Open source from The Open Group. "As small as possible" for enterprise ecosystems.

### Diagram Guidelines

**Titles:**

Title all elements unless very well-known

**Lines:**

- Thick enough to see
- **Solid = synchronous** | **Dotted = asynchronous**
- Arrows show direction

**Shapes:**

- No universal standards (create your own)
- Common: 3D boxes (deployables), rectangles (containers), cylinders (databases)

**Labels:**

Label everything—avoid ambiguity

**Color:**

- Use when it helps distinguish artifacts
- **Accessibility**: Use iconography + color (not color alone)
- Example: Traffic lights use shapes too

**Keys:**

Include if shapes ambiguous. Misinterpreted diagram > no diagram

---

## Summary

**Component Design:**

- Use bounded contexts (DDD)
- Logical before physical architecture
- Avoid entity trap
- Manage coupling intentionally

**Risk Management:**

- Risk matrix for objectivity
- Collaborative risk storming
- Focus on characteristics
- Track direction over time

**Communication:**

- Appropriate fidelity for stage
- Representational consistency
- Adopt standards (C4, ArchiMate)
- Clear, accessible diagrams

**Key Takeaway:**

Good architecture requires both strong technical design and clear communication to all stakeholders.
