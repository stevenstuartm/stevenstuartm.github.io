---
title: "AAA Cycle: Phase 1 - Align with the Need"
layout: guide
category: Software Development Lifecycle
subcategory: AAA Cycle
description: "Understand the problem before committing to a solution."
tags: [sdlc, aaa-cycle, requirements, stakeholder-management, collaboration, practical]
---

## Phase Overview

### Purpose

**Understand the problem space before making commitments.** Build trust with stakeholders, surface constraints, and establish shared understanding of success.

### The Universal Pattern

Regardless of project size or methodology, alignment follows these steps:

1. **Understand the need**: What problem? Why now?
2. **Identify stakeholders**: Who cares? Who decides?
3. **Surface constraints**: What limits our options?
4. **Assess risk**: What could go wrong?
5. **Estimate effort**: How much work?
6. **Get agreement**: Are we aligned to proceed?

The depth and formality scale with scope and risk, but these questions remain constant.

<blockquote class="pull-quote">
<p>Understand the problem before committing to a solution.</p>
</blockquote>

### Recursive Application

Align applies at every level of work:

- **Program Level** (months): Full depth with comprehensive charter
- **Project Level** (weeks): Medium depth with focused discovery
- **Sprint Level** (days): Lightweight with story grooming
- **Feature Level** (hours): Quick alignment on acceptance criteria

### Entry & Exit

**You start with**: A project concept or business need

**You deliver**: Approved project charter with stakeholder sign-off

---

## Core Activities

### 1. Initial Stakeholder Discovery

**Set expectations and understand the landscape.**

**Key Questions**:
- What problem are we solving? Why now?
- What does success look like?
- Who else needs to be involved?
- What are the hard constraints (timeline, budget, technology, compliance)?
- What keeps you up at night about this project?

**How to Do This Well**:
- Listen more than you talk—take notes, ask clarifying questions, observe dynamics
- Don't jump to solutions yet—stay neutral and build trust first
- Demonstrate genuine interest in stakeholder needs, not just their requirements
- In every meeting, ask "Who else should be involved?"

<div class="callout callout--warning">
<p class="callout__title">Red Flags</p>
<ul>
<li>Missing key stakeholders (operations, security, compliance, end users)</li>
<li>Vague success criteria ("make it faster")</li>
<li>Stakeholders who don't understand what alignment involves</li>
<li>Pressure to "start coding" without proper discovery</li>
</ul>
</div>

---

### 2. Requirements Discovery

**Translate business needs into clear, prioritized requirements.**

**Functional Requirements**:
- What tasks must users complete?
- What business rules govern the process?
- What data needs to be captured or integrated?

**Architectural Characteristics** (often missed):
- Performance: Response time, throughput expectations
- Scalability: Growth projections for users and data
- Availability: Uptime requirements
- Security: Authentication, authorization, data protection (see [Security Foundations](/study-guides/security/security-foundations.html){:target="_blank" rel="noopener noreferrer"})
- Compliance: Regulatory requirements (GDPR, HIPAA, etc.) (see [Compliance & Governance](/study-guides/security/compliance-governance.html){:target="_blank" rel="noopener noreferrer"})

**Prioritization**:
- Must have vs. should have vs. could have
- MVP scope vs. future enhancements
- Force-rank if everything is "critical"

**How to Do This Well**:
- Ask "why" repeatedly to get to root needs
- Probe for architectural characteristics explicitly—stakeholders often forget them
- Push for measurable, testable criteria (not "it should be fast" but "page loads < 2 seconds")
- Document acceptance criteria clearly so there's no ambiguity later
- Think holistically about how requirements impact architecture

<div class="callout callout--warning">
<p class="callout__title">Red Flags</p>
<ul>
<li>Gold plating (collecting every nice-to-have)</li>
<li>Vague, unmeasurable requirements ("fast," "scalable," "user-friendly")</li>
<li>No prioritization or everything is P0</li>
<li>Analysis paralysis (too long in discovery)</li>
<li>Accepting vague requirements without pushing for specifics</li>
</ul>
</div>

---

### 3. Constraint & Risk Assessment

**Surface limitations and potential blockers while they're cheap to address.**

**Constraints to Document**:
- Technical (platform mandates, technology restrictions, integration requirements)
- Resource (budget, team size/skills, timeline pressures)
- Compliance (industry standards, data residency, audit requirements)
- Organizational (governance policies, procurement processes, support requirements)

**Risk Categories**:
- Technical: New technologies, complex integrations, unknowns
- Schedule: Aggressive timelines, resource availability
- Business: Market timing, competitive pressure
- Organizational: Stakeholder alignment, political challenges
- Operational: Deployment complexity, support readiness

**Risk Mitigation Approaches**:
- **Avoid**: Change approach to eliminate risk
- **Mitigate**: Reduce likelihood or impact
- **Transfer**: Use vendors/insurance to shift risk
- **Accept**: Acknowledge and plan contingency

**How to Do This Well**:
- Extract implicit constraints—stakeholders often assume you know their limitations
- Challenge "requirements" that are actually preferences
- Quantify risks with likelihood and impact scoring
- Map dependencies on other teams/systems explicitly
- Budget time for organizational overhead (approvals, procurement, access delays)
- Be honest about uncertainties—don't sugarcoat risks

<div class="callout callout--warning">
<p class="callout__title">Red Flags</p>
<ul>
<li>Treating preferences as constraints</li>
<li>Missing organizational/political risks</li>
<li>Risk lists without mitigation strategies</li>
<li>Assuming assumptions are validated without testing them</li>
<li>Underestimating non-technical delays (approvals, access provisioning)</li>
</ul>
</div>

---

### 4. Initial Sizing & Estimation

**Provide realistic ballpark estimates for go/no-go decisions.**

**Estimation Approach**:
- Break solution into major components/epics
- Estimate effort using analogous estimation, planning poker, or t-shirt sizing
- Include infrastructure and operational costs
- Account for testing, deployment, documentation
- Add contingency buffer (typically 20-30%)

**Provide Ranges, Not Point Estimates**:
- "4-6 months" is more honest than "5 months"
- Explain methodology and assumptions
- Flag high-uncertainty areas

<blockquote class="pull-quote">
<p>Be realistic, not optimistic. Frame alignment as risk mitigation.</p>
</blockquote>

**Feasibility Assessment**:
- Go: Estimates fit within constraints
- No-Go: Not feasible, recommend cancellation
- Pivot: Adjust scope/timeline/approach to make feasible

**How to Do This Well**:
- Be realistic, not optimistic—frame alignment as risk mitigation
- Involve the team—engineers doing the work should validate estimates
- Show your work and include contingency explicitly
- Provide ranges ("4-6 months") not false precision ("4.3 months")
- Explain methodology and assumptions clearly
- Flag high-uncertainty areas for stakeholder awareness

<div class="callout callout--warning">
<p class="callout__title">Red Flags</p>
<ul>
<li>False precision ("4.3 months")</li>
<li>Anchoring bias (stakeholder suggests timeline, skews your estimate)</li>
<li>Ignoring non-development work (testing, deployment, documentation)</li>
<li>No contingency buffer (typically 20-30%)</li>
<li>Estimating without team input</li>
</ul>
</div>

---

## Visual Communication During Alignment

### Purpose

**Use diagrams to build shared understanding, not to create documentation.**

During Align, visualization serves discovery. The goal is to ensure stakeholders share the same mental model of the problem space, system boundaries, and key relationships. These are working artifacts, not formal documentation.

<blockquote class="pull-quote">
<p>Use diagrams to build shared understanding, not to create documentation.</p>
</blockquote>

### What Works at This Stage

**C4 Level 1 (Context Diagrams)**:
- Shows the system boundary and external dependencies
- Helps stakeholders understand what's in scope vs. out of scope
- Clarifies which external systems, teams, or users are involved
- Useful when: Multiple systems interact, scope boundaries are unclear, or stakeholders have different assumptions about what's included

**Simple Box-and-Arrow Sketches**:
- Whiteboard-level clarity for exploring ideas
- No formal notation required—focus on communication
- Easy to change as understanding evolves
- Useful when: Exploring concepts collaboratively, testing different mental models, or facilitating stakeholder discussions

**Data Flow Diagrams**:
- Shows how information moves through the system
- Identifies sources, destinations, and transformations
- Useful when: The problem centers on data movement, integration points are unclear, or compliance requires data flow documentation

### When to Create Diagrams

**Create diagrams when**:
- Stakeholders have different mental models of the system boundary
- External dependencies or integrations are unclear
- Multiple teams or systems are involved and roles need clarification
- Compliance or governance requires visual documentation of scope
- Verbal descriptions create confusion or misalignment

**Skip diagrams when**:
- Everyone already shares the same mental model
- The system is simple enough to describe clearly in a few sentences
- You're still discovering what the problem actually is (too early to diagram)
- Creating the diagram would take longer than the value it provides

<div class="callout callout--tip">
<p class="callout__title">How to Do This Well</p>
<ul>
<li><strong>Keep it simple</strong> - Use the minimum formality needed for clarity</li>
<li><strong>Make it collaborative</strong> - Sketch together with stakeholders, don't present finished diagrams</li>
<li><strong>Focus on boundaries</strong> - What's in scope? What's out? Who owns what?</li>
<li><strong>Iterate quickly</strong> - Diagrams should evolve as understanding evolves</li>
<li><strong>Don't over-invest</strong> - These are discovery tools, not deliverables</li>
<li><strong>Test understanding</strong> - Ask stakeholders to explain the diagram back to you</li>
</ul>
</div>

<div class="callout callout--warning">
<p class="callout__title">Red Flags</p>
<ul>
<li>Creating UML class diagrams during Align—you don't know the solution yet</li>
<li>Spending hours on polished diagrams before you've agreed on the problem</li>
<li>Using diagrams to avoid conversations ("here's the architecture, read it")</li>
<li>Formal notation that stakeholders don't understand</li>
<li>Diagrams that become stale immediately because they're not maintained</li>
<li>Diagramming the solution when you're supposed to be understanding the problem</li>
</ul>
</div>

---

## The Project Charter

### Purpose

**Formalize understanding and secure commitment.** The charter is the contract that authorizes the project to proceed.

### Essential Components

#### 1. Executive Summary (1-2 pages)
- Project name, sponsor, and key personnel
- High-level business problem and objectives
- Recommended approach
- Estimated timeline and budget
- Critical success factors

#### 2. Scope Definition
**In-Scope**: Clear deliverables and capabilities
**Out-of-Scope** (equally important): What you're explicitly NOT doing

Example:
```
IN SCOPE:
- Customer portal with login and profile management
- Integration with existing CRM
- Mobile-responsive web design

OUT OF SCOPE:
- Mobile native apps (web only)
- International language support (future phase)
- Integration with legacy billing system (separate project)
```

#### 3. Success Criteria (Measurable)
- Business metrics (revenue, cost savings, conversion rate)
- User metrics (adoption rate, satisfaction)
- Technical metrics (uptime, performance)
- Timeline metrics (launch date, milestones)

Example:
```
Success =
✓ Portal launched by Q3 2025
✓ 70% customer adoption within 3 months
✓ 99.9% uptime achieved
✓ Support calls reduced 30%
✓ Page load < 2 seconds (95th percentile)
```

#### 4. Authority & Decision Rights
- What can you decide autonomously?
- What requires stakeholder approval?
- Escalation path for issues
- Budget authority and spending limits

#### 5. Communication Plan
- Meeting schedules and cadence
- Status reporting approach
- Where artifacts will be stored
- How decisions will be documented

#### 6. Risk Register (Top 5-10)
- Risk description, likelihood, impact
- Mitigation strategy and owner

#### 7. Assumptions & Dependencies
- Key assumptions (and what invalidates them)
- Dependencies on other teams/systems
- Timeline impacts if dependencies delayed

### Minimum vs. Maximum

**Small Projects**: 3-5 pages, simple scope, basic risks
**Large Projects**: 15-20 pages, detailed scope, comprehensive risk register, governance structure

### Getting Real Approval

**Signs of Real Agreement**:
- ✅ Stakeholders can explain the project to others
- ✅ No one is surprised by scope or timeline
- ✅ Budget and resources are committed
- ✅ Risks are acknowledged and accepted
- ✅ Decision rights are clear

**Red Flags**:
- ❌ "Let's just get started and figure it out"
- ❌ Stakeholders disagree on priorities
- ❌ Budget "to be determined"
- ❌ Key stakeholders not present for approval
- ❌ Rushed approval without real review
- ❌ Rubber-stamp approval without understanding

**How to Do This Well**:
- Present the charter in person—don't just email it
- Walk through key sections together
- Ask stakeholders to explain it back to you—test their understanding
- Make the charter scannable with headings, bullets, and tables
- Get formal written sign-off, not just verbal agreement
- Ensure real commitment before proceeding to the Agree phase

