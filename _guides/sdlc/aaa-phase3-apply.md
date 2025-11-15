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

**This is not failure. This is the inevitable outcome of doing real work.**

The discipline of Apply is knowing when to:
- **Continue**: Discovery confirms the approach; keep executing
- **Adapt**: Minor adjustments within the agreed scope and architecture
- **Pause and Realign**: Discovery invalidates core assumptions; cycle back to Align or Agree

### Triggers for Reconsideration

**When to pause and reconsolidate the agreement**:

- **Technical discovery**: Assumed approach won't work; a different solution is needed
- **Scope discovery**: Original scope misunderstood; what was agreed doesn't match what's actually needed
- **Dependency discovery**: Critical dependencies emerge that change timeline or feasibility
- **Value discovery**: Building the feature reveals a better problem to solve
- **Risk discovery**: Unforeseen risks make the agreed approach unacceptable

**When NOT to pause** (adapt instead):
- Minor technical adjustments within the architecture
- Small scope clarifications that don't change the core agreement
- Implementation details that don't affect stakeholders
- Performance optimizations within agreed SLOs

**How to handle discovery**:
1. Document what you learned (what assumption broke, what's now understood)
2. Assess impact (timeline, cost, scope, quality, risk)
3. Present options to stakeholders (continue as-is, adapt, or realign)
4. If realignment needed, cycle back to Align or Agree phases
5. Update the agreement and communicate changes
6. Resume execution with the new understanding

Realignment isn't scope creep or project failure. It's the discipline to incorporate learning and maintain integrity with stakeholders. Teams that ship based on broken assumptions, just to avoid "changing the plan," deliver work that misses the mark.

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

**Red Flags**:
- Architecture astronauts (over-governing, creating bottlenecks)
- No governance (inconsistent implementation, architectural drift)
- Ignoring technical debt until unmanageable
- Not documenting decisions with ADRs
- Rigid adherence to plan when reality differs
- Late architectural reviews (finding issues after merge)

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

**Red Flags**:
- Communication vacuum (no updates until the end)
- Yes to everything (accepting all changes, scope balloons)
- Ignoring feedback (stakeholders give input but team doesn't respond)
- No retrospectives (team doesn't reflect or improve)
- Hiding problems (not escalating risks/issues early)
- Losing stakeholder alignment during execution
- Team stops communicating, stakeholders surprised at delivery

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

**Decision Point: Ready for Release**:
- ✅ All acceptance criteria met
- ✅ Test coverage targets achieved
- ✅ No critical/high-severity bugs
- ✅ Security scan passed
- ✅ Performance meets SLOs
- ✅ UAT completed and approved
- ✅ Documentation complete
- ✅ Monitoring and alerting configured

**How to Do This Well**:
- Test early, test often—shift left on quality
- Automate everything practical—free humans for exploratory testing
- Make tests fast and reliable—invest in test infrastructure
- Fail fast—run quickest tests first in the pipeline
- Don't compromise on quality gates—they exist for good reasons
- Test in production—use feature flags, canaries, synthetic monitoring
- Integrate security testing throughout development, not at the end
- Ensure quality relentlessly—maintain standards under pressure

**Red Flags**:
- Testing as afterthought
- Low test coverage or no coverage tracking
- Slow or flaky tests that developers ignore
- Ignoring security until the end
- No UAT before deploying
- Lowering quality bar to ship faster
- Compromising quality for speed
- Pressure to deliver leading to cut corners on testing

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

**Deploy** if:
- ✅ Automation completed without errors
- ✅ Health checks passing
- ✅ Error rates within normal range
- ✅ Performance meets SLOs
- ✅ No critical issues

**Rollback** if:
- ❌ High error rates
- ❌ Performance degradation
- ❌ Health checks failing
- ❌ Critical functionality broken
- ❌ Security issue discovered

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

**Red Flags**:
- Manual deployments (error-prone, slow)
- No rollback plan or untested rollback procedure
- Insufficient monitoring (flying blind in production)
- Deploying on Fridays (no one around to fix issues)
- Big bang releases (too much at once, high risk)
- No operations handoff plan
- Dev team owns production indefinitely or abrupt handoff

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

**Delivery Acceptance Criteria**:
- ✅ All must-have requirements implemented
- ✅ Acceptance criteria met and validated
- ✅ UAT completed and approved
- ✅ SLOs being met in production
- ✅ Documentation complete
- ✅ Operations team trained and ready
- ✅ Stakeholders satisfied with delivery

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

**Red Flags**:
- No clear acceptance criteria (project drags on indefinitely)
- Poor documentation (operations struggles to support)
- No retrospective (missing opportunity to learn)
- Ghosting operations team (dev team disappears after launch)
- Skipping celebration (not acknowledging effort)
- No reflection on what went well or poorly
- Repeating mistakes from project to project

