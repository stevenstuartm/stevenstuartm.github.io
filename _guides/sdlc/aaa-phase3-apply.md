---
title: "AAA Cycle: Phase 3 - Apply the Plan and Deliver"
layout: guide
category: Software Development Lifecycle
subcategory: AAA Cycle
description: "Execute with discipline while maintaining alignment."
tags: [sdlc, aaa-cycle, implementation, delivery, governance, practical]
---

## Phase Overview

### Purpose

**Execute the agreed plan with discipline while maintaining continuous alignment.** This is sustained execution with governance, quality assurance, stakeholder communication, and value delivery.

<blockquote class="pull-quote">
<p>Apply is not blind execution; it's disciplined delivery that honors the agreement while maintaining the courage to pause when discovery demands it.</p>
</blockquote>

### The Universal Pattern

Regardless of project size or methodology, application follows these steps:

1. **Implement incrementally**: Build in small batches
2. **Maintain quality**: Test continuously, don't compromise
3. **Govern architecture**: Ensure integrity through reviews
4. **Keep stakeholders aligned**: Regular communication and demos
5. **Deploy reliably**: Automate and practice
6. **Reflect and improve**: Learn from experience

The frequency and formality scale with methodology, but the principles remain constant.

### Recursive Application

Apply applies at every level of work:

- **Program Level** (months): Multiple projects, portfolio governance, quarterly reviews
- **Project Level** (weeks): Team executing sprints, regular demos, project retrospective
- **Sprint Level** (days): Daily development, sprint review, sprint retro
- **Feature Level** (hours): Code, test, review, merge with continuous integration

### Entry & Exit

**You start with**: Approved architecture and implementation plan from Phase 2

**You deliver**: Working software in production that meets business objectives

---

## The Core Value: Honoring the Agreement While Learning

**Apply is not blind execution.** It's disciplined delivery that honors what was agreed in Phase 2 while maintaining the courage to pause and realign when discovery demands it.

Discovery during implementation is inevitable:
- Implementation reveals hidden complexity
- Building the first version surfaces better approaches
- Edge cases emerge that invalidate assumptions
- Dependencies appear that change timelines
- User feedback shifts priorities

<div class="callout callout--note">
<p class="callout__title">Discovery Is Not Failure</p>
<p>This is the inevitable outcome of doing real work. Teams that ship based on broken assumptions, just to avoid "changing the plan," deliver work that misses the mark.</p>
</div>

The discipline of Apply is knowing when to:
- **Continue**: Discovery confirms the approach; keep executing
- **Adapt**: Minor adjustments within the agreed scope and architecture
- **Pause and Realign**: Discovery invalidates core assumptions; cycle back to Align or Agree

### When to Pause vs. Adapt

<div class="comparison">
<div class="content-card content-card--accent-warning">
<h4>Pause and Realign</h4>
<ul>
<li>Technical discovery: Assumed approach won't work</li>
<li>Scope discovery: Original scope misunderstood</li>
<li>Dependency discovery: Critical dependencies emerge</li>
<li>Value discovery: Better problem to solve revealed</li>
<li>Risk discovery: Unforeseen risks make approach unacceptable</li>
</ul>
</div>
<div class="content-card content-card--accent">
<h4>Adapt and Continue</h4>
<ul>
<li>Minor technical adjustments within the architecture</li>
<li>Small scope clarifications that don't change the core agreement</li>
<li>Implementation details that don't affect stakeholders</li>
<li>Performance optimizations within agreed SLOs</li>
</ul>
</div>
</div>

**How to handle discovery**:
1. Document what you learned (what assumption broke, what's now understood)
2. Assess impact (timeline, cost, scope, quality, risk)
3. Present options to stakeholders (continue as-is, adapt, or realign)
4. If realignment needed, cycle back to Align or Agree phases
5. Update the agreement and communicate changes
6. Resume execution with the new understanding

<blockquote class="pull-quote">
<p>Realignment isn't scope creep or project failure. It's the discipline to incorporate learning and maintain integrity with stakeholders.</p>
</blockquote>

---

## Core Activities

### 1. Implementation & Architecture Governance

**Build incrementally while maintaining architectural integrity.**

**Implementation Approach**:
- Work in small, releasable increments
- Continuously integrate and test changes
- Gather feedback early and often
- Adapt based on learnings while maintaining alignment with goals

**Architecture Governance**:
- **Architecture Decision Records (ADRs)**: Document significant decisions as they're made
- **Architecture Reviews**: Weekly or bi-weekly review of significant changes
- **Code Reviews**: Review for architectural conformance, not just correctness
- **Tech Stack Governance**: Evaluate new libraries/frameworks before adoption
  - Check for vulnerabilities (CVE databases)
  - Assess licensing and legal implications
  - Ensure alignment with organizational standards
- **Architecture Health Checks**: Monthly/quarterly assessment of system health
  - Code quality metrics (coverage, complexity, duplication)
  - Technical debt tracking and paydown planning
  - Architectural violations
- See [Governance](/study-guides/architecture/governance.html){:target="_blank" rel="noopener noreferrer"}, [Governance Frameworks](/study-guides/architecture/governance-frameworks.html){:target="_blank" rel="noopener noreferrer"}, [Governance Tools](/study-guides/architecture/governance-tools.html){:target="_blank" rel="noopener noreferrer"}

**Decision Point: Architecture Conformance**:
- Is implementation staying true to approved architecture?
- Are component interactions matching designed interfaces?
- Is technical debt being tracked and managed?
- When do you need to adjust architecture vs. enforce conformance?

**Process for Architecture Changes**:
1. Document the need (new ADR)
2. Assess impact (timeline, cost, risk)
3. Present to stakeholders for approval
4. Update architecture documentation
5. Communicate change to team

**How to Do This Well**:
- Review early and often—catch issues when they're easy to fix
- Balance governance and autonomy—don't become a bottleneck
- Make ADRs lightweight—don't let documentation become a burden
- Treat technical debt as backlog items—track and prioritize like features
- Work in small, releasable increments to reduce risk
- Continuously integrate and test changes
- Gather feedback early and adapt based on learnings

<div class="callout callout--warning">
<p class="callout__title">Governance Red Flags</p>
<ul>
<li><strong>Architecture astronauts</strong>: Over-governing, creating bottlenecks</li>
<li><strong>No governance</strong>: Inconsistent implementation, architectural drift</li>
<li><strong>Ignoring technical debt</strong>: Until it's unmanageable</li>
<li><strong>No ADRs</strong>: Decisions not documented for future reference</li>
<li><strong>Rigid adherence to plan</strong>: When reality clearly differs</li>
<li><strong>Late architectural reviews</strong>: Finding issues after merge</li>
</ul>
</div>

---

### 2. Continuous Stakeholder Alignment

**Maintain alignment throughout implementation as discovery happens.**

Alignment isn't achieved once in Phase 2 and then frozen. It's maintained continuously as implementation reveals new information. The team and stakeholders must stay aligned on what's being built, why it matters, and what trade-offs are being made.

**Regular Touchpoints**:
- **Sprint/Iteration Reviews**: Demo working software, gather feedback, validate direction
- **Stakeholder Updates**: Status on progress, blockers, risks, budget, timeline
- **Daily Standups**: Team synchronization (internal, not for stakeholders)
- **Scope Management**: Evaluate change requests, re-prioritize based on learnings
- **Risk Monitoring**: Review risk register, update status, implement mitigations
- **Retrospectives**: Reflect on what went well, identify improvements

**Decision Point: Stay the Course vs. Pivot**:
- **Continue as planned**: Implementation on track, stakeholders satisfied, no major risks
- **Adjust course**: Significant new information, requirements changed, technical approach not working

**Process for Changes**:
1. Document proposed change
2. Assess impact (timeline, cost, scope, quality)
3. Present options to stakeholders
4. Get approval
5. Update plan and communicate
6. May cycle back to Align or Agree phases if needed

**How to Do This Well**:
- Communicate proactively—share status, risks, issues early
- Translate technical to business—help stakeholders understand progress
- Show working software—demos are more powerful than status reports
- Be transparent—share good and bad news honestly
- Respond to feedback quickly—show stakeholder input matters
- Hold regular sprint/iteration reviews with working software
- Monitor risks continuously and implement mitigations

<div class="callout callout--warning">
<p class="callout__title">Stakeholder Alignment Red Flags</p>
<ul>
<li><strong>Communication vacuum</strong>: No updates until the end</li>
<li><strong>Yes to everything</strong>: Accepting all changes, scope balloons</li>
<li><strong>Ignoring feedback</strong>: Stakeholders give input but team doesn't respond</li>
<li><strong>No retrospectives</strong>: Team doesn't reflect or improve</li>
<li><strong>Hiding problems</strong>: Not escalating risks/issues early</li>
<li><strong>Stakeholders surprised at delivery</strong>: Lost alignment during execution</li>
</ul>
</div>

---

### 3. Quality Assurance

**Ensure quality through continuous testing and validation.**

**Testing Activities**:
- **Test-Driven Development**: Write unit tests before or with code
- **Automated Testing**:
  - Unit tests run on every commit
  - Integration tests in CI pipeline
  - E2E tests before merges or nightly
  - Performance tests periodically
  - Security scans integrated in pipeline
- **Code Reviews**: Peer review all changes (bugs, security, design, standards)
- **Security Testing**:
  - SAST: Static code analysis every build
  - Dependency scanning: Check vulnerable libraries daily
  - DAST: Dynamic testing in staging
  - Penetration testing: Before launch
  - See [Security Testing](/study-guides/security/security-testing.html){:target="_blank" rel="noopener noreferrer"}, [Application Security](/study-guides/security/application-security.html){:target="_blank" rel="noopener noreferrer"}
- **Performance Testing**:
  - Load testing before releases
  - Stress testing to find breaking points
  - Performance regression testing
  - Validate SLO targets
- **User Acceptance Testing**: Business users test against acceptance criteria before release

**Quality Gates**:
- **Pre-merge**: Tests pass, review approved
- **Pre-release**: All acceptance criteria met, no critical bugs, security scan clean
- **Pre-production**: UAT passed, performance validated, rollback plan tested

<div class="callout callout--tip">
<p class="callout__title">Ready for Release Checklist</p>
<ul>
<li>All acceptance criteria met</li>
<li>Test coverage targets achieved</li>
<li>No critical/high-severity bugs</li>
<li>Security scan passed</li>
<li>Performance meets SLOs</li>
<li>UAT completed and approved</li>
<li>Documentation complete</li>
<li>Monitoring and alerting configured</li>
</ul>
</div>

**How to Do This Well**:
- Test early, test often—shift left on quality
- Automate everything practical—free humans for exploratory testing
- Make tests fast and reliable—invest in test infrastructure
- Fail fast—run quickest tests first in the pipeline
- Don't compromise on quality gates—they exist for good reasons
- Test in production—use feature flags, canaries, synthetic monitoring
- Integrate security testing throughout development, not at the end
- Ensure quality relentlessly—maintain standards under pressure

<div class="callout callout--warning">
<p class="callout__title">Quality Assurance Red Flags</p>
<ul>
<li><strong>Testing as afterthought</strong>: Not integrated into development</li>
<li><strong>Low test coverage</strong>: Or no coverage tracking at all</li>
<li><strong>Slow or flaky tests</strong>: Developers ignore them</li>
<li><strong>Security deferred</strong>: Ignoring security until the end</li>
<li><strong>No UAT</strong>: Deploying without user validation</li>
<li><strong>Lowering the quality bar</strong>: Compromising quality for speed</li>
</ul>
</div>

---

### 4. Deployment & Operations

**Deploy reliably and transition operations smoothly.**

**CI/CD Pipeline**:
- Automate build, test, and deployment
- Implement deployment strategies (blue/green, canary, rolling)
- Configure release automation
- Set up automated rollback
- See [CI/CD](/study-guides/sdlc/cicd.html){:target="_blank" rel="noopener noreferrer"}, [DevSecOps](/study-guides/sdlc/devsecops.html){:target="_blank" rel="noopener noreferrer"}

**Deployment Strategy Selection**:
- **All-at-once**: Simple but risky, downtime required
- **Rolling**: Gradual replacement, no downtime, can roll back
- **Blue/Green**: Two environments, instant switchover, easy rollback
- **Canary**: Deploy to subset first, monitor, then full rollout
- See [Deployment Strategies](/study-guides/infrastructure/deployment-strategies.html){:target="_blank" rel="noopener noreferrer"}, [Deployment & Infrastructure Patterns](/study-guides/architecture/deployment_infrastructure_patterns.html){:target="_blank" rel="noopener noreferrer"}

**Monitoring & Observability** (before deployment):
- Instrument code with logging, metrics, tracing
- Set up dashboards for key metrics
- Configure alerting for SLO violations
- Implement health checks and readiness probes
- See [Observability Fundamentals](/study-guides/observability-fundamentals.html){:target="_blank" rel="noopener noreferrer"}

**Production Deployment**:
1. Execute deployment via automation
2. Monitor deployment progress
3. Validate health checks
4. Monitor key metrics (error rates, performance)
5. Roll back if issues detected

**Post-Deployment Validation**:
- Smoke testing in production
- Monitor error rates and performance
- Validate SLO compliance
- Gather user feedback
- Address any issues immediately

**Deployment Decision: Deploy or Rollback**:

<div class="comparison">
<div class="content-card content-card--accent">
<h4>Deploy</h4>
<ul>
<li>Automation completed without errors</li>
<li>Health checks passing</li>
<li>Error rates within normal range</li>
<li>Performance meets SLOs</li>
<li>No critical issues</li>
</ul>
</div>
<div class="content-card content-card--accent-warning">
<h4>Rollback</h4>
<ul>
<li>High error rates</li>
<li>Performance degradation</li>
<li>Health checks failing</li>
<li>Critical functionality broken</li>
<li>Security issue discovered</li>
</ul>
</div>
</div>

**Operations Handoff**:
- Train operations team
- Provide runbooks for common issues
- Document troubleshooting procedures
- Establish on-call rotation
- Define escalation paths

**How to Do This Well**:
- Automate everything—deployments, rollbacks, monitoring
- Deploy frequently—small, frequent deployments reduce risk
- Use feature flags—decouple deployment from feature release
- Monitor proactively—don't wait for users to report issues
- Test rollback regularly—it should be routine, not exceptional
- Practice chaos engineering—test resilience in production
- Involve operations early—engage them from Phase 2 onwards
- Deploy reliably with proven automation strategies

<div class="callout callout--warning">
<p class="callout__title">Deployment Red Flags</p>
<ul>
<li><strong>Manual deployments</strong>: Error-prone and slow</li>
<li><strong>No rollback plan</strong>: Or untested rollback procedure</li>
<li><strong>Insufficient monitoring</strong>: Flying blind in production</li>
<li><strong>Deploying on Fridays</strong>: No one around to fix issues</li>
<li><strong>Big bang releases</strong>: Too much at once, high risk</li>
<li><strong>No operations handoff plan</strong>: Dev team owns production indefinitely</li>
</ul>
</div>

---

### 5. Delivery & Handoff

**Complete delivery and transition to ongoing operations.**

**Final Validation**:
- Complete User Acceptance Testing
- Validate all acceptance criteria met
- Confirm SLOs being achieved
- Address any final issues
- Get stakeholder sign-off on delivery

**Documentation Completion**:
- Finalize user documentation (guides, FAQs)
- Complete technical documentation (architecture, APIs)
- Update architecture diagrams to as-built state
- Create/update operations runbooks
- Archive project artifacts

**Operations Handoff**:
- Train operations team on the system
- Review runbooks and troubleshooting
- Clarify support model and escalation
- Transfer ownership of monitoring/alerting
- Establish SLA for support response

**Retrospective**:
- Reflect on entire project (not just last sprint)
- What went well? What didn't?
- What would we do differently?
- Capture lessons learned
- Celebrate team accomplishments

**Project Closure**:
- Final project report to stakeholders
- Close out budget and financials
- Archive project artifacts
- Release team members to other work
- Plan for ongoing enhancements (if applicable)

<div class="callout callout--tip">
<p class="callout__title">Delivery Acceptance Criteria</p>
<ul>
<li>All must-have requirements implemented</li>
<li>Acceptance criteria met and validated</li>
<li>UAT completed and approved</li>
<li>SLOs being met in production</li>
<li>Documentation complete</li>
<li>Operations team trained and ready</li>
<li>Stakeholders satisfied with delivery</li>
</ul>
</div>

**Post-Launch Considerations**:
- **Warranty/Support Period**: Team available for post-launch issues (2-4 weeks typical)
- **Enhancements Backlog**: Known improvements deferred to future
- **Ongoing Maintenance**: Who owns the system long-term?
- **Success Metrics**: How will we measure ongoing success?

**How to Do This Well**:
- Define "done" clearly with acceptance criteria from Phase 1
- Document as you go—don't leave all documentation for the end
- Involve operations early—engage them throughout the project
- Run blameless retrospectives—focus on learning, not blame
- Celebrate wins—recognize team effort and accomplishments
- Plan for ongoing support—warranty period, enhancement backlog
- Implement incrementally throughout the project
- Reflect on the entire project and capture lessons learned

<div class="callout callout--warning">
<p class="callout__title">Delivery Red Flags</p>
<ul>
<li><strong>No clear acceptance criteria</strong>: Project drags on indefinitely</li>
<li><strong>Poor documentation</strong>: Operations struggles to support</li>
<li><strong>No retrospective</strong>: Missing opportunity to learn</li>
<li><strong>Ghosting operations</strong>: Dev team disappears after launch</li>
<li><strong>Skipping celebration</strong>: Not acknowledging effort</li>
<li><strong>Repeating mistakes</strong>: No reflection on what went poorly</li>
</ul>
</div>
