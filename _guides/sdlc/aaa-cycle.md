---
title: "AAA Cycle: Align-Agree-Apply"
layout: guide
category: Software Development Lifecycle
subcategory: SDLC & Modeling
description: "A personal framework for consistent agile execution through three phases: Align with the need, Agree to the plan, and Apply the plan and deliver."
---

## Table of Contents
1. [Overview](#overview)
2. [Phase 1: Align with the Need](#phase-1-align-with-the-need)
3. [Phase 2: Agree to the Plan](#phase-2-agree-to-the-plan)
4. [Phase 3: Apply the Plan and Deliver](#phase-3-apply-the-plan-and-deliver)

---

## Overview

The **AAA Cycle** (Align-Agree-Apply) is a personal framework for consistent agile execution that maintains focus on deliverables through three key phases. This framework ensures that teams move systematically from understanding needs to delivering solutions, with clear gates and objectives at each stage.

---

## Phase 1: Align with the Need

The alignment phase focuses on thoroughly understanding the problem space, stakeholders, and constraints before making commitments.

### Stakeholder & Requirements Analysis

**Identify and Engage Stakeholders:**
- Map all stakeholders (sponsors, users, technical teams, business owners)
- Understand their perspectives, concerns, and success criteria
- Establish communication channels and engagement patterns

**Define Clear Project Goals:**
- Articulate the business problem being solved
- Define measurable success criteria
- Establish project vision and objectives
- Use SMART criteria (Specific, Measurable, Achievable, Relevant, Time-bound) to define deliverables

**Gather Requirements:**
- Document significant use cases and user stories
- Identify functional and non-functional requirements
- Prioritize requirements based on business value
- Validate understanding with stakeholders

### Project Scope & Planning

**Document Project Parameters:**
- **Timing**: Project timeline, milestones, and deadlines
- **Sequence**: Order of deliverables and implementation phases
- **Dependencies**: Internal and external dependencies that affect delivery
- **Integration Points**: Where the solution connects with existing systems

**Surface and Document Assumptions:**
- Extract implicit assumptions from stakeholder conversations
- Document technical assumptions about the environment
- Identify business assumptions that could affect the project
- Validate critical assumptions early

**Assess Constraints:**
- **System Quality Attributes**: Performance, scalability, reliability requirements
- **Compliance Requirements**: Regulatory, legal, and industry standards
- **Resource Constraints**: Budget, team size, skill availability
- **Technical Constraints**: Platform limitations, technology mandates

**Evaluate Risks:**
- **Unknowns**: Identify areas with insufficient information
- **Quality/Functionality Intersections**: Where quality requirements might conflict with features
- **Organizational Risk Appetite**: Understand acceptable risk levels
- **Technical Risks**: New technologies, integrations, complexity
- **Business Risks**: Market timing, competitive pressures

**Create Development and Infrastructure Estimates:**
- Break down work into estimable chunks
- Estimate development effort (story points, hours, or t-shirt sizes)
- Estimate infrastructure and operational costs
- Include time for learning, spikes, and unknowns
- Build in contingency for risk mitigation

### Project Charter Essentials

The project charter formally authorizes the project and provides the project manager with authority to allocate resources.

**Key Components:**

1. **Executive Summary**
   - High-level project overview
   - Primary goals and objectives
   - Recommended approach and methodology
   - Key personnel and roles

2. **Scope Definition**
   - Clear in-scope items and deliverables
   - Explicit out-of-scope items to manage expectations
   - Boundaries and interfaces with other systems/projects

3. **Authority Levels**
   - Decision-making authority delegated to project manager
   - Budget authority and spending limits
   - Resource allocation permissions
   - Escalation paths for issues beyond PM authority

4. **Communication Plan**
   - Stakeholder communication cadence and methods
   - Status reporting frequency and format
   - Meeting schedules (standups, reviews, retrospectives)
   - Decision documentation approach

5. **Data Storage Strategy**
   - Where project artifacts will be stored
   - Version control approach
   - Documentation repositories
   - Access controls and security

6. **High-Level Risks**
   - Top 5-10 risks identified during alignment
   - Initial risk mitigation strategies
   - Risk owners and escalation procedures

7. **Success Criteria**
   - Measurable definition of project success
   - Acceptance criteria for deliverables
   - Quality gates and validation approaches

---

## Phase 2: Agree to the Plan

The agreement phase transforms aligned understanding into concrete, approved plans with clear technical direction and resource commitments.

### Design & Architecture Agreement

**High-Level Design:**
- Define system architecture and major components
- Document layers (presentation, service, data)
- Map component interactions and workflows
- Identify integration points and interfaces
- Choose architectural patterns (microservices, monolithic, event-driven, etc.)

**Service Level Agreements and Objectives:**
- Define SLAs for uptime, performance, and availability
- Establish SLOs (Service Level Objectives) for key metrics
- Set SLIs (Service Level Indicators) to measure performance
- Document support and maintenance expectations

**Quality Assurance Plan:**
- Define testing strategy (unit, integration, e2e, performance)
- Establish code quality standards and review processes
- Identify automated testing tools and frameworks
- Plan for security testing (SAST, DAST, penetration testing)
- Define acceptance criteria and validation approach

**Budget Allocations:**
- Break down budget by phase and work stream
- Allocate resources for infrastructure and tooling
- Plan for contingency and risk mitigation
- Establish procurement processes for third-party services

**Realistic Estimations:**
- Refine estimates from alignment phase with more detail
- Use historical data and team velocity where available
- Include buffer for unknowns and technical debt
- Account for learning curves on new technologies
- Validate estimates with the team performing the work

**Working Proof of Concept:**
- Build a minimal PoC to validate technical approach
- Demonstrate feasibility of key technical decisions
- Identify technical risks early
- Provide concrete basis for final estimations
- Get stakeholder feedback on direction before full commitment

---

## Phase 3: Apply the Plan and Deliver

The application phase executes the agreed plan, maintaining focus on delivery while adapting to learnings and changes.

### Implementation & Delivery

**Detailed Component Design:**
- Break high-level design into detailed technical specifications
- Define interfaces, data models, and API contracts
- Document component responsibilities and interactions
- Assign clear ownership and accountability for each component

**Architecture Reviews:**
- Regular design sessions with architects and senior engineers
- Review technical decisions against architectural standards
- Validate alignment with non-functional requirements
- Identify and address technical debt proactively

**Tech Stack Selection:**
When choosing technologies, frameworks, and tools, consider:

- **Requirements Support**: Does the technology meet functional and non-functional requirements?
- **Popularity & Community**: Active community, good documentation, available talent pool
- **Cost Considerations**: Licensing, hosting, operational costs
- **Longevity & Stability**: Is the technology mature and well-maintained?
- **Security Posture**:
  - Check CVE databases for known vulnerabilities
  - Assess supply chain security (dependencies, maintainers)
  - Evaluate security update frequency and responsiveness
- **In-House Expertise**: Does the team have experience, or is training needed?
- **Open Contribution**: Can the team contribute back and influence direction?
- **Vendor Lock-In**: Evaluate portability and switching costs

**Iterative Development:**
- Implement in small, releasable increments
- Continuously integrate and test changes
- Gather feedback early and often
- Adapt plans based on learnings while maintaining alignment with goals

**Delivery and Deployment:**
- Follow CI/CD best practices for consistent, reliable deployments
- Implement monitoring and observability from day one
- Plan for zero-downtime deployments and rollback capabilities
- Validate each release against acceptance criteria
- Maintain close communication with stakeholders on progress

---

## Using the AAA Cycle

### Iteration and Feedback

The AAA Cycle is not strictly linear - teams may iterate within phases or return to earlier phases when new information emerges:

- **Realignment**: When significant new requirements or constraints emerge
- **Re-agreement**: When technical approaches need revision or budget adjustments are needed
- **Continuous Application**: Delivery happens in iterations, with regular feedback loops

### Integration with SDLC Methodologies

The AAA Cycle complements various SDLC methodologies:

- **Agile/Scrum**: Each sprint can follow a mini AAA cycle
- **Waterfall**: AAA phases map naturally to traditional waterfall gates
- **Shape Up**: Alignment and agreement happen during shaping; application during building
- **Kanban**: AAA principles guide work item progression through the board

### Keys to Success

1. **Don't Rush Alignment**: Taking time to truly understand needs prevents costly rework
2. **Get Real Agreement**: Ensure stakeholders genuinely agree, not just nod along
3. **Stay Aligned During Application**: Regular check-ins ensure delivery stays on target
4. **Document Decisions**: Capture why decisions were made to inform future phases
5. **Embrace Iteration**: Be willing to revisit earlier phases when needed
