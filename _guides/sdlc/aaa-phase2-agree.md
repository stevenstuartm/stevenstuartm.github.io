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

### The Universal Pattern

Regardless of project size or methodology, agreement follows these steps:

1. **Design the solution** - How will we build this?
2. **Validate assumptions** - Will this approach work?
3. **Define quality standards** - How good is good enough?
4. **Set performance targets** - What's the bar for success?
5. **Analyze costs** - What's the total investment and return?
6. **Plan the work** - What's the sequence and effort?
7. **Get commitment** - Do we all agree to proceed?

The depth and formality scale with scope and risk, but these questions remain constant.

### Recursive Application

Agree applies at every level of work:

- **Program Level** (weeks): Full architecture design, comprehensive POC, detailed TCO/ROI
- **Project Level** (days): Component design, targeted spikes, focused cost analysis
- **Sprint Level** (hours): Technical design discussion, quick validation
- **Feature Level** (minutes): Code review validates approach

### Entry & Exit

**You start with**: Approved project charter from Phase 1

**You deliver**: Approved architecture and implementation plan with resource commitment

---

## Core Activities

### 1. Architecture Design

**Define the system architecture that meets requirements within constraints.**

**Key Design Decisions**:

- **Architectural Characteristics**: What quality attributes matter most?
  - Identify 7 characteristics critical to success (e.g., performance, scalability, availability, security, maintainability)
  - Prioritize the 3 most important characteristics—these drive architecture style selection
  - Use structured worksheets to evaluate characteristics and select appropriate style
  - See [Architecture Foundations](/study-guides/architecture/ArchitectureFoundations.html#architecture-characteristics)
  - **Worksheets**: [Architecture Characteristics & Style Selection Worksheets](https://developertoarchitect.com/downloads/worksheets.html)

- **Architectural Style**: Monolithic, microservices, serverless, event-driven?
  - Choose style based on top 3 architectural characteristics
  - Consider: Scalability needs, team skills, operational maturity, cost
  - See [Architecture Styles](/study-guides/architecture/ArchitectureStyles.html)

- **Component Boundaries**: How do you break the system into pieces?
  - Define responsibilities, interfaces, and data ownership
  - Align boundaries with domain partitioning when possible

- **Integration Patterns**: How do components and external systems communicate?
  - Synchronous (REST, gRPC) vs. asynchronous (messaging, events)
  - See [Communication Patterns](/study-guides/architecture/communication_patterns.html), [Integration Patterns](/study-guides/architecture/integration_patterns.html)

- **Data Architecture**: How is data stored and managed?
  - SQL, NoSQL, caching strategy, consistency requirements
  - See [Data Architecture](/study-guides/data-architecture.html), [Data Management Patterns](/study-guides/architecture/data_management_patterns.html)

**Document Your Decisions**:
- Architecture Decision Records (ADRs): Context → Decision → Consequences
- Document WHY, not just WHAT
- Record alternatives considered and why they were rejected
- See [Architecture Decisions & Leadership](/study-guides/architecture/ArchitectureDecisionsLeadership.html), [Governance](/study-guides/architecture/governance.html)

**How to Do This Well**:
- Evaluate multiple options before deciding—don't just pick what you know
- Document trade-offs explicitly for future reference
- Design for 2x growth, not 100x—start simple, add complexity only when needed (YAGNI)
- Involve senior engineers throughout design—get team buy-in early
- Consider operations from the start—how will this be deployed, monitored, maintained?
- Use proven patterns over novel approaches unless there's clear justification

**Red Flags**:
- Resume-driven architecture (choosing trendy tech, not what fits)
- Over-engineering (building for scale you'll never need)
- Under-engineering (ignoring future growth)
- Ignoring operations (hard to deploy, monitor, maintain)
- Not documenting decisions
- Designing in a vacuum without team input

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

**How to Do This Well**:
- Test the riskiest assumptions first—focus on what you're most uncertain about
- Use real data, not toy data—real scenarios reveal real problems
- Measure actual performance, don't guess—collect hard numbers
- Involve the team who'll implement—they need the learning experience
- Time-box strictly and take shortcuts—it's about learning, not building
- Decide quickly: go/adjust/pivot based on findings
- Delete POC code when done—resist the temptation to productionize it

**Red Flags**:
- POC becomes production code (quality shortcuts in production)
- Testing easy things instead of real risks
- No clear success criteria
- POC drags on indefinitely without decisions
- Ignoring or downplaying negative POC findings

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

**How to Do This Well**:
- Test the contract, not the implementation—focus on behavior
- Automate from day one—make quality non-negotiable
- Fail fast—quick tests first, slow tests later in the pipeline
- Make tests reliable—flaky tests erode confidence and waste time
- Design for testability—architecture should make testing easy
- Don't compromise on quality gates—they prevent production issues

**Red Flags**:
- Testing ice cream cone (too many E2E tests, not enough unit tests)
- No automation (manual testing only)
- Skipping or delaying security testing
- Quality theater (tests exist but don't catch defects)
- Under-investing in test infrastructure

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

**How to Do This Well**:
- Don't chase "nines" without justification—understand the cost of each nine
- Use percentiles (95th, 99th), not averages—averages hide outliers
- Build in margin—SLO should be tighter than SLA to avoid breaches
- Make targets visible with dashboards—transparency drives accountability
- Use error budgets to balance reliability with feature velocity
- Base targets on architecture capabilities—start conservative

**Red Flags**:
- Measuring the wrong things (vanity metrics)
- No error budget (teams become risk-averse or burn out)
- SLAs more aggressive than SLOs (no safety margin)
- No monitoring plan for measuring SLIs
- Targets that ignore dependency SLOs (unrealistic given downstream limitations)
- Setting targets that sound good but are unachievable

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

**How to Do This Well**:
- Plan collaboratively with the team—their input improves accuracy and buy-in
- Use historical velocity data when available
- Provide ranges, not point estimates—acknowledge uncertainty
- Make contingency buffer explicit (typically 20-30%)
- Plan in waves: detailed for near-term, high-level for distant future
- Listen to team concerns—they often identify real risks

**Red Flags**:
- Architect or PM creates plan without developer input
- No buffer time for surprises
- Ignoring team velocity data
- Forgetting non-development work (meetings, reviews, support)
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

**How to Do This Well**:
- Include ongoing operational costs, not just upfront development
- Account for scaling—costs change with growth
- Factor in technical debt paydown over time
- Build in contingency for unknowns (typically 15-25%)
- Review cloud cost calculators and pricing models carefully

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

**How to Do This Well**:
- Be conservative in benefit estimates, realistic in cost estimates
- Show best-case, likely-case, worst-case scenarios
- Include time value of money for multi-year projections
- Tie benefits to measurable business metrics from Phase 1 success criteria
- Prove business value clearly to secure commitment

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

**How to Do This Well**:
- Present in person, don't just email the plan
- Walk through interactively, don't just present slides
- Tailor to audience—business-focused for stakeholders, technical for architects
- Listen to concerns—stakeholder intuition may identify real issues
- Be transparent about risks and uncertainties
- Be willing to adjust based on feedback
- Get written sign-off, not just verbal approval
- Ensure stakeholders understand and formally commit

