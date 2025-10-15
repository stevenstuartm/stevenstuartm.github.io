---
title: "AAA Cycle: Phase 2 - Agree to the Plan"
layout: guide
category: Software Development Lifecycle
subcategory: AAA Cycle Framework
description: "Design the solution and secure commitment to the approach."
---

## Phase Overview

### Purpose

**Transform aligned understanding into concrete, approved technical plans.** Design the solution, validate critical assumptions, and secure commitment on approach and resources.

### What You Accomplish

- Design system architecture with clear component boundaries
- Validate technical feasibility through proof of concepts
- Define quality standards and testing approach
- Establish performance targets with SLAs and SLOs
- Analyze total cost of ownership and return on investment
- Create detailed implementation plan with resource commitment
- Secure formal approval to proceed

### Entry & Exit

**You start with**: Approved project charter from Phase 1

**You deliver**: Approved architecture and implementation plan with resource commitment

---

## Core Activities

### 1. Architecture Design

**Define the system architecture that meets requirements within constraints.**

**Key Design Decisions**:
- **Architectural Style**: Monolithic, microservices, serverless, event-driven?
  - Consider: Scalability needs, team skills, operational maturity, cost
  - See [Architecture Styles](/study-guides/architecture/ArchitectureStyles.html)
- **Component Boundaries**: How do you break the system into pieces?
  - Define responsibilities, interfaces, and data ownership
- **Integration Patterns**: How do components and external systems communicate?
  - Synchronous (REST, gRPC) vs. asynchronous (messaging, events)
  - See [Communication Patterns](/study-guides/architecture/communication_patterns.html), [Integration Patterns](/study-guides/architecture/integration_patterns.html)
- **Data Architecture**: How is data stored and managed?
  - SQL, NoSQL, caching strategy, consistency requirements
  - See [Data Architecture](/study-guides/data-architecture.html), [Data Management Patterns](/study-guides/architecture/data_management_patterns.html)
- **Non-Functional Requirements**: How do you achieve performance, scalability, reliability?
  - Design for required response times, uptime targets, and throughput
  - See [Performance & Scalability Patterns](/study-guides/architecture/performance_scalability_patterns.html), [Reliability Patterns](/study-guides/architecture/reliability_patterns.html)

**Document Your Decisions**:
- Architecture Decision Records (ADRs): Context → Decision → Consequences
- Document WHY, not just WHAT
- Record alternatives considered and why they were rejected
- See [Architecture Decisions & Leadership](/study-guides/architecture/ArchitectureDecisionsLeadership.html), [Governance](/study-guides/architecture/governance.html)

**Core Principle**: Evaluate multiple options before deciding. Don't just pick what you know. Document trade-offs explicitly. Design for 2x growth, not 100x. Start simple, add complexity only when needed (YAGNI).

**Red Flags**:
- Resume-driven architecture (choosing trendy tech, not what fits)
- Over-engineering (building for scale you'll never need)
- Under-engineering (ignoring future growth)
- Ignoring operations (hard to deploy, monitor, maintain)
- Not documenting decisions

---

### 2. Technical Proof of Concept

**Validate critical technical assumptions before full commitment.**

**When to Build a POC**:
- Using new or unfamiliar technology
- Complex integration with unclear feasibility
- Performance requirements that need validation
- High uncertainty in technical approach
- Team needs to learn new skills/tools

**What to Validate**:
- **Integration**: Can we actually connect? Does their API work as documented?
- **Performance**: Can we meet response time targets? Where are bottlenecks?
- **Technology Feasibility**: Does this framework do what we need? What's the learning curve?
- **Security**: Can we implement required controls?

**POC Best Practices**:
- Define clear goals: What specific questions need answering?
- Time-box it (3-7 days typical)
- Take shortcuts: Hard-code, skip error handling—it's throwaway code
- Document findings: What worked? What didn't? Surprises?
- Update estimates based on learnings
- Throw away the code (POC ≠ production)

**Core Principle**: Test the riskiest assumptions first. Use real data, not toy data. Measure actual performance, don't guess. Involve the team who'll implement. Decide quickly: go/adjust/pivot.

**Red Flags**:
- POC becomes production code
- Testing easy things instead of real risks
- No clear success criteria
- POC drags on indefinitely
- Ignoring POC findings

---

### 3. Quality & Testing Strategy

**Define how you'll ensure quality throughout development.**

**Testing Pyramid**:
- **Unit Tests** (70-80%): Test individual functions/methods
- **Integration Tests** (15-20%): Test component interactions
- **End-to-End Tests** (5-10%): Test complete workflows
- **Manual Testing**: Exploratory and UAT

**Security Testing**:
- **SAST**: Static code analysis on every build
- **Dependency Scanning**: Check for vulnerable libraries
- **DAST**: Dynamic testing in staging
- **Penetration Testing**: Before launch
- See [Security Testing](/study-guides/security/security-testing.html), [Application Security](/study-guides/security/application-security.html)

**Performance Testing**:
- Load testing for expected traffic
- Stress testing to find breaking points
- Validate SLO targets before production

**Quality Gates**:
- Code commit: Tests pass, linting passes, review approved
- Merge to main: All tests pass, coverage target met
- Release: E2E tests pass, security scan clean, UAT approved

**Core Principle**: Test the contract, not the implementation. Automate what's practical. Fail fast—quick tests first, slow tests later. Make tests reliable—flaky tests erode confidence. Don't compromise on quality gates.

**Red Flags**:
- Testing ice cream cone (too many E2E tests, not enough unit tests)
- No automation (manual testing only)
- No security testing until the end
- Quality theater (tests exist but don't catch defects)

---

### 4. SLA/SLO Definition

**Establish measurable performance and availability targets.**

**Key Concepts**:
- **SLI** (Service Level Indicator): Metric measuring service quality
  - Examples: Request latency, availability, error rate, throughput
- **SLO** (Service Level Objective): Target value for an SLI
  - Example: "95% of requests complete in < 200ms"
  - Internal goal used by engineering
- **SLA** (Service Level Agreement): Commitment to customers
  - Usually less aggressive than SLO (buffer for margin)
  - May have consequences if not met (refunds, penalties)
- **Error Budget**: Allowable amount of downtime/failures
  - 99.9% availability = 43.8 minutes downtime per month
  - Balances reliability vs. velocity of change

**Choose SLIs That Matter to Users**:
- Availability: % of time service is operational
- Latency: Response time (use 95th or 99th percentile, not average)
- Error Rate: % of requests that fail
- Throughput: Requests per second handled

**Setting Targets**:
- Based on business requirements from Phase 1
- Balanced between ambition and feasibility
- More aggressive than current baseline (if improving existing system)

**Core Principle**: Don't chase "nines" without justification. Use percentiles, not averages. Build in margin—SLO should be tighter than SLA. Make targets visible with dashboards. Use error budgets to balance reliability with feature velocity.

**Red Flags**:
- Measuring the wrong things (vanity metrics)
- No error budget (teams become risk-averse)
- SLAs more aggressive than SLOs
- No monitoring plan for measuring SLIs
- Targets that ignore dependency SLOs

---

### 5. Detailed Planning & Budget

**Create concrete implementation plan with resource commitment.**

**Work Breakdown**:
- Break components into implementable stories/tasks
- Identify dependencies between work items
- Sequence work based on dependencies and risk
- Group work into sprints/iterations or releases

**Estimation Refinement**:
- Refine estimates from Phase 1 based on POC learnings
- Use team velocity if available
- Include time for testing, reviews, rework
- Account for meetings, support, non-development work
- Add contingency buffer (20-30%)

**Resource Allocation**:
- Assign team members to work streams
- Identify skill gaps and training needs
- Coordinate with other projects for shared resources

**Project Schedule**:
- Map work to timeline with milestones
- Identify critical path
- Mark dependencies on external teams/vendors

**Core Principle**: Plan with the team—their input improves accuracy and buy-in. Use historical velocity data. Provide ranges, not point estimates. Make contingency buffer explicit. Plan in waves: detailed for near-term, high-level for distant future.

**Red Flags**:
- Architect creates plan without developer input
- No buffer time for surprises
- Ignoring team velocity
- Forgetting non-development work
- Unrealistic dependency assumptions

---

## Cost Analysis

### Total Cost of Ownership (TCO)

**Comprehensive view of all costs over the system's lifetime.**

For detailed guidance, see [Total Cost of Ownership](/study-guides/architecture/total-cost-of-ownership.html).

**Cost Categories**:

**1. Development Costs**:
- Labor (developers, architects, testers, designers)
- Training and onboarding
- Contractor/consultant fees
- Tooling and licenses

**2. Infrastructure Costs**:
- Cloud compute, storage, networking (ongoing)
- Databases and managed services
- CDN and data transfer
- Non-production environments (dev, test, staging)

**3. Third-Party Services**:
- APIs and SaaS subscriptions
- Authentication providers
- Payment processors
- Monitoring and observability tools

**4. Operational Costs**:
- Support staff and on-call rotation
- Maintenance and bug fixes
- Security patching and updates
- Monitoring and incident response

**5. Hidden Costs**:
- Vendor lock-in and switching costs
- Technical debt and refactoring
- Compliance and audit requirements
- Disaster recovery and backup
- End-of-life and decommissioning

**Core Principle**: Include ongoing operational costs, not just upfront development. Account for scaling—costs change with growth. Factor in technical debt paydown. Build in contingency for unknowns.

---

### Return on Investment (ROI)

**Justify the investment by demonstrating business value.**

For detailed guidance, see [Return on Investment](/study-guides/architecture/return-on-investment.html).

**ROI Formula**:
```
ROI = (Net Benefit / Total Cost) × 100%

Where:
Net Benefit = Total Benefits - Total Costs
```

**Quantifiable Benefits**:
- **Revenue increase**: New sales, upsell opportunities, market expansion
- **Cost savings**: Reduced operational costs, headcount savings, efficiency gains
- **Risk reduction**: Avoided security breaches, compliance penalties, downtime
- **Productivity gains**: Time saved per transaction, faster processes, reduced errors

**Qualitative Benefits** (harder to quantify but still valuable):
- Improved customer satisfaction
- Better employee experience
- Competitive advantage
- Brand reputation
- Strategic positioning

**Time to Value**:
- When do benefits start accruing?
- How long until ROI is positive (payback period)?
- What's the long-term ROI (3-5 years)?

**Core Principle**: Be conservative in benefit estimates, realistic in cost estimates. Show best-case, likely-case, worst-case scenarios. Include time value of money for multi-year projections. Tie benefits to measurable business metrics from Phase 1 success criteria.

---

### Plan Review & Approval

**Present complete plan and secure formal approval.**

**What to Present**:
- Architecture overview (high-level, not too technical)
- Key design decisions and trade-offs (ADRs)
- POC findings and validation
- Quality and testing approach
- SLAs and performance targets
- Timeline and milestones
- Budget breakdown and ROI analysis
- Risks and mitigation strategies

**Architecture Review**:
- Present to senior technical staff first
- Walk through key decisions
- Address technical concerns
- Get architecture sign-off

**Stakeholder Presentation**:
- Tailor to audience (business-focused, not deep technical)
- Use visuals (diagrams, charts, tables)
- Anticipate questions
- Be transparent about risks and uncertainties

**Signs of Readiness**:
- ✅ Stakeholders can explain the approach to others
- ✅ Technical team confident in the design
- ✅ Budget and resources formally committed
- ✅ Risks acknowledged and mitigation agreed
- ✅ Timeline accepted as realistic

**Core Principle**: Present in person, don't just email. Walk through, don't just present slides. Listen to concerns—stakeholder intuition may identify real issues. Be willing to adjust based on feedback. Get written sign-off, not just verbal approval.

---

## Essential Principles

### The Universal Pattern

Regardless of project size or methodology:

1. **Design the solution** - How will we build this?
2. **Validate assumptions** - Will this approach work?
3. **Define quality standards** - How good is good enough?
4. **Set performance targets** - What's the bar for success?
5. **Analyze costs** - What's the total investment and return?
6. **Plan the work** - What's the sequence and effort?
7. **Get commitment** - Do we all agree to proceed?

**The depth and formality scale with scope and risk, but these questions remain constant.**

### Recursive Application

Agree applies at every level:

**Program Level** (weeks): Full architecture design, comprehensive POC, detailed TCO/ROI
**Project Level** (days): Component design, targeted spikes, focused cost analysis
**Sprint Level** (hours): Technical design discussion, quick validation
**Feature Level** (minutes): Code review validates approach

### Common Failure Modes

**Designing in a Vacuum**:
- Architect designs alone without team input
- Results in unimplementable or misunderstood designs
- Solution: Involve senior engineers throughout. Get team buy-in.

**POC Becomes Production**:
- Team builds POC with production quality
- Results in wasted time, delayed learning
- Solution: Time-box strictly. Take shortcuts. Delete POC code.

**Over-Engineering**:
- Designing for scale/complexity you don't need yet
- Results in longer dev time, harder maintenance
- Solution: Start simple. Design for 2x, not 100x. Use proven patterns.

**Under-Investing in Quality**:
- Skipping test automation or security testing
- Results in slow, buggy releases, security incidents
- Solution: Automate from day one. Make quality non-negotiable.

**Unrealistic SLOs**:
- Setting targets that sound good but are unachievable
- Results in constant firefighting, burnout
- Solution: Base on architecture capabilities. Start conservative.

**Planning Without the Team**:
- PM or architect creates plan without developer input
- Results in wrong estimates, no commitment
- Solution: Involve team in estimation. Listen to concerns.

**Incomplete Cost Analysis**:
- Only considering upfront development costs
- Results in budget surprises from operations/scaling
- Solution: Include TCO. Factor in ongoing operational costs.

**Weak ROI Justification**:
- Can't articulate business value clearly
- Results in budget challenges, project cancellation
- Solution: Tie to measurable business metrics. Show scenarios.

### What Matters Most

**Evaluate alternatives**: Don't just pick what you know
**Document trade-offs**: Explain WHY, not just WHAT
**Validate assumptions**: Test risky assumptions with POCs
**Design for testability**: Make quality verification easy
**Set realistic targets**: Balance ambition with feasibility
**Plan collaboratively**: Team involvement = better estimates + buy-in
**Analyze total costs**: Include ongoing operations, not just development
**Prove business value**: Clear ROI justification secures commitment
**Get real approval**: Stakeholders understand and formally commit
