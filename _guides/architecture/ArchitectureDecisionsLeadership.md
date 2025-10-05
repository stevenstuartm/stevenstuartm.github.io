---
layout: guide
title: "Architecture Decisions & Leadership"
category: Architecture
subcategory: Leadership
---

# Architecture Decisions & Leadership

## Architect Responsibilities

1. Make Architecture Decisions - Define decisions and principles guiding technology choices
2. Continually Analyze - Assess architecture vitality as business and technology change
3. Keep Current - Stay updated on technical and industry trends
4. Ensure Compliance - Verify teams follow defined decisions and principles
5. Understand Technologies - Technical breadth over depth
6. Know the Business - Understand domain, problems, goals, requirements
7. Lead Teams - Exceptional interpersonal skills: teamwork, facilitation, leadership
8. Navigate Politics - Negotiation skills to get decisions approved

---

## Decision-Making

### Architectural Decision Antipatterns

**1. Covering Your Assets**

Fear of being wrong prevents making decisions.

**Solutions**

- Last Responsible Moment: Decide when cost of deferring > risk of deciding
- Collaborate: Validate feasibility with dev teams

**2. Groundhog Day**

Decisions get revisited repeatedly because people don't know why they were made.

**Solution**

Provide technical AND business justifications: Cost | Time to market | User satisfaction | Strategic positioning

**3. Email-Driven Architecture**

Decisions lost, forgotten, or unknown.

**Solution**

- Store in single system of record
- Email only links, not decision bodies

### Architectural Significance

A decision is architecturally significant if it affects:

- Structure (patterns/styles)
- Characteristics (performance, scalability)
- Dependencies (coupling)
- Interfaces (access/orchestration)
- Construction techniques (platforms, frameworks, tools)

---

## Architectural Decision Records (ADRs)

### Structure

**Title**

Numbered sequentially with short phrase

Example: "42. Use Asynchronous Messaging Between Order and Payment Services"

**Status**

- Proposed | Accepted | Superseded | RFC (with deadline)

**Approval Criteria**

- Cost thresholds (e.g., >$5K requires review)
- Cross-team impact
- Security implications

**Context**

Forces at play: "What situation forces this decision?"

- Specific circumstances
- Possible alternatives
- Area affected

**Decision**

Affirmative, commanding voice: "We will use asynchronous messaging between services."

Include full justification. **Why > How**

**Consequences**

Overall impact (pros and cons). Include trade-off analysis.

Example: Better responsiveness (25ms vs 3,100ms) but complex error handling

**Compliance**

How will it be measured and governed?

Manual checks | Automated fitness functions | Tools (ArchUnit, NetArchTest)

**Notes**

Metadata: Author | Approval date | Approved by | Last modified | Superseded date

### Storage

Store in dedicated repository or wiki accessible to all stakeholders.

---

## Team Leadership

### Making Teams Effective

**Collaboration**

Break down architect/developer barriers. Form strong bidirectional relationships. Architecture changes every iteration—tight collaboration essential.

**Constraints & Boundaries**

Create appropriate constraints forming a "room" for teams. Provide right level of guidance—not too much, not too little.

### Architect Personalities

**Control-Freak Architect**

Too fine-grained decisions, tight boundaries, too many constraints → teams lose autonomy

**Armchair Architect**

Disconnected, no implementation details, loose boundaries → teams do architect's work

**Effective Architect**

Appropriate constraints, ensures collaboration, right guidance level, removes roadblocks

### Elastic Leadership

How involved should you be? Consider:

**Team Familiarity**

Better they know each other → less involvement

**Team Size**

Small (≤5) less | Large (>12) more

**Experience**

More juniors → more mentoring | More seniors → facilitator role

**Project Complexity**

High → more availability | Low → less involvement

**Project Duration**

Longer → more involvement over time

### Team Warning Signs

**Process Loss (Brooks's Law)**

"More people = more time"

**Indicators**

Frequent merge conflicts, working on same code, getting in each other's way

**Solution**

Find parallelism; avoid adding people without parallel work

**Pluralistic Ignorance**

Everyone privately rejects a norm but publicly agrees

**Solution**

Smaller teams where people feel safe to speak

**Diffusion of Responsibility**

Large teams → unclear responsibilities → dropped work

**Solution**

Clear roles, right-sized teams

---

## Providing Guidance

### Design Principles

Use principles to form constraint boundaries.

**Example: Third-Party Library Decision Framework**

**Special Purpose (Developer Decision)**

- Specific functionality (PDFs, barcodes)
- Developer decides independently

**General Purpose (Architect Approval)**

- Wrappers on language APIs
- Developer analysis + architect approval

**Framework (Architect Decision)**

- Entire layers (persistence, IoC)
- Highly invasive
- Architect decides entirely

### Business Justifications

Ask for business value to increase awareness and enable better decisions.

---

## Leveraging Checklists

**When to Use**

- Processes without set order
- Frequently skipped steps
- Common error-prone tasks

**Guidelines**

- Keep small
- Automate what you can
- Don't overdo it

**Useful Checklists**

1. Developer code completion ("definition of done")
2. Unit & functional testing (edge cases, unusual scenarios)
3. Software release (build/deployment steps)

**Getting Buy-In**

- Explain reasoning
- Collaborative creation (ownership)

**Hawthorne Effect**

Perception of monitoring encourages compliance

---

## Negotiation Skills

### With Business Stakeholders

- Pay attention to buzzwords/jargon (contain clues)
- Gather information before negotiating
- State things in qualified cost and time
- Divide and conquer to qualify demands

### With Other Architects

- Demonstration defeats discussion
- Avoid being overly argumentative or personal
- Calm leadership + clear reasoning wins

### With Developers

- Provide justification (not dictates)
- Have them arrive at the solution themselves

---

## Integrating with Development Teams

### Control Your Calendar

**Meetings Imposed on You**

- Ask why you're needed
- Attend only for relevant topics
- Could meeting notes suffice?

**Meetings You Impose**

- Keep to absolute minimum
- Set and stick to agenda
- Schedule at day edges (morning, after lunch, late)

### Physical Presence

**On-site**

- Sit with the team
- Walk around, be visible
- Block time for conversations, questions, coaching

**Remote**

- Use video calls effectively
- Establish regular check-ins
- Maintain open communication

### Respect Developer Flow State

Flow = 100% brain engagement where hours feel like minutes.
Don't disrupt flow. Pay attention to team productivity patterns.

---

## The 4 Cs of Architecture Leadership

1. Communication: Clear, effective information sharing
2. Collaboration: Working together toward goals
3. Clear: Unambiguous direction and decisions
4. Concise: Direct, to-the-point guidance

Avoid accidental complexity through these principles.

---

## Leading by Example

**Be Pragmatic, Yet Visionary**

Balance practical reality with future aspirations. Requires maturity and practice.

**Lead Through Example**

Don't "pull rank." Gain respect through actions, not title.

**Remember**

Technical knowledge alone doesn't solve problems—people skills are essential.

---

## Summary

**The Effective Architect**

**Technical Skills**

- Broad technical knowledge
- Understanding trade-offs
- Making informed decisions

**People Skills**

- Collaboration and communication
- Negotiation and influence
- Leadership by example

**Business Acumen**

- Domain knowledge
- Business justifications
- Strategic thinking

**Decision Quality**

- Well-documented (ADRs)
- Properly justified
- Appropriately governed
- Clearly communicated

**Key Takeaways**

- Architecture is as much about people as technology
- Document decisions with ADRs
- Provide appropriate constraints, not too many or too few
- Respect team dynamics and flow
- Lead by example, not by authority
