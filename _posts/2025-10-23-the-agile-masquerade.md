---
layout: post
title: "The Agile Masquerade: Building on Assumptions, Shipping on Hope"
date: 2025-10-23
description: "It is impossible to deliver what is expected and valuable if there has been no agreement on the expectation or how we measure value. Without discovery and quantification, you're operating on hope, not discipline."
series: "Industry & Culture"
tags: [agile, requirements, aaa-cycle, estimation]
---

## Agreement Requires Discovery

You cannot deliver value without agreement on what constitutes value.

You cannot have agreement without discovery of what you're actually building.

You cannot apply discovery to improve the agreement if you're afraid of "documentation" and refuse to step outside pointless timeboxes and absurd estimations based on nothing but assumptions.

**You cannot iterate on what you cannot quantify. Otherwise, you're operating on hope, not discipline.**

## Misalignment Disguised as Agreement

Software development frequently operates on fictional agreements, creating misaligned teams. The problem isn't new to "Agile" methodologies; waterfall documentation could be equally full of untested assumptions and vague requirements. But user stories have made the problem worse by treating minimal documentation as a virtue.

A user story like "As a user, I want to search products" is not an agreement. It's a placeholder. Teams estimate it ("Five points"), commit to it, hand it to a developer, and expect results. But what does "search" mean? What edge cases exist? What trade-offs are acceptable? How do we measure success?

None of this was discussed. But everyone acts as if agreement exists. When the developer delivers something that vaguely resembles search, the story is marked "done." The team remains misaligned on whether value was delivered because value was never quantified.

## Why We Don't Test Assumptions

Estimating based on untested assumptions is not planning. It's guessing. And when teams base commitments on guesses, they're building on sand.

The pattern is familiar: estimate based on assumptions, commit to the estimate, discover during implementation that the assumptions were wrong, then ship anyway because the timebox ends. Discovery gets reframed as scope creep rather than learning. The timebox becomes more important than the outcome.

In the real world, implementation reveals hidden complexity. Edge cases emerge. Dependencies appear. The question is: do you have the discipline to pause and realign when discovery changes everything?

### The Missing Discipline

Architects know better. An architect's first step is to identify stakeholders, understand general intent, **identify assumptions, and test assumptions before committing**. Developers and product owners should do the same.

{% include linkedin-link.html url="https://www.linkedin.com/in/isaac-carter/" %} Isaac Carter emphasizes this in his Catalyst Framework: test assumptions to gain alignment. Not alignment on what we assume, but alignment on what we've validated.

What does testing assumptions look like?

**Assumption**: Users need advanced search filters.
**Test**: Show mockups to actual users. Do they use filters or just type keywords?
**Result**: 80% ignore filters. The assumption was wrong.

**Assumption**: This feature will take 2 weeks.
**Test**: Spike the riskiest part. Build a prototype of the core complexity.
**Result**: The spike reveals hidden dependencies. The real estimate is 6 weeks.

**Assumption**: This refactoring will improve performance.
**Test**: Profile the actual bottleneck. Measure current performance.
**Result**: The bottleneck is elsewhere. The refactoring won't help.

**Testing assumptions prevents building the wrong thing.** But Scrum has no mechanism for this. Sprint planning happens in hours. There's no time to test assumptions; just estimate based on them and commit.

### The Spike Problem

Scrum's flaws become obvious the moment someone suggests introducing spikes. A spike is exploratory work to reduce uncertainty: exactly what testing assumptions requires.

But spikes create political and metric chaos in Scrum:
- **How do you estimate a spike?** The whole point is you don't know enough to estimate
- **How do you measure velocity?** Spikes don't deliver features
- **What happens if the spike invalidates the sprint plan?** Scrum has no answer
- **Do spikes count as "done" work?** They produce knowledge, not shippable code

Teams resort to absurdities: estimating the exploration itself (defeating the purpose), hiding spikes as "technical tasks" within stories (obscuring what's actually happening), or skipping spikes entirely and guessing (back to building on sand).

The spike problem reveals a fundamental tension: frameworks, like Scrum, optimize for predictable metrics while real work requires validated understanding. Discovery threatens the illusion of control.

This tension exists in most organizations. Teams recognize when they're misaligned: estimates feel like guesses and commitments feel fictional. But introducing discipline like assumption testing creates friction: it reveals uncertainty, delays commitment, and challenges established metrics. The question becomes: how do misaligned teams regain alignment within systems that resist it?

## The False Dilemma

The immediate objection is predictable: "You're advocating for analysis paralysis. We can't spend months discovering requirements before shipping anything."

This is a false dilemma. The choice isn't between doing nothing and doing everything. It's not "ship immediately with no understanding" versus "achieve perfect knowledge before starting."

**This is about being actually agile.**

True agility means adapting to changing priorities and changing understanding. Discovery is inevitable. The question is: do you have the discipline to incorporate what you discover, or do you ship anyway because the timebox ends?

The discipline isn't perfect upfront requirements or endless discovery. It's simpler:
1. Identify what you know vs. what you're assuming
2. Test critical assumptions before making initial commitments (not all assumptions, just the ones that matter)
3. Commit to initial quantifiable outcomes with explicit constraints
4. Discover new information during implementation (this will happen)
5. **Pause and reconsolidate the agreement when discovery changes everything**
6. Update the agreement based on what you learned and continue, or deliver what was agreed

This is continuous alignment, not upfront perfection. You start with enough understanding to commit responsibly, then maintain discipline to realign as you learn.

**How much initial discovery is enough?** Enough to commit responsibly to initial quantifiable outcomes while acknowledging what you don't yet know. For a simple CRUD screen, that might be 30 minutes of conversation. For a complex workflow with edge cases and integrations, it might be a week of prototyping and user testing. The rigor matches the risk. But this is just the starting point; you'll continue discovering and realigning throughout implementation.

**What about real-world constraints?** Leadership demands roadmaps. Sales needs commitments. The business can't wait. True. But shipping the wrong thing on schedule doesn't solve those constraints. It just delays the reckoning. The choice is: negotiate realistic commitments based on actual understanding, or make fictional commitments and deal with the consequences later.

**Isn't this just good engineering?** Yes. That's exactly the point. The discipline of testing assumptions, agreeing on outcomes, and realigning based on discovery is what competent engineering looks like. The challenge is that organizational pressures often optimize for predictable metrics (velocity, sprint completion, roadmap commitments) over validated understanding.

**Can't you do this within Scrum?** Yes, and many teams do. The challenge is that Scrum's structure creates pressure: timeboxes push toward premature commitment, velocity metrics can penalize discovery, and sprint commitments create expectations. But teams can work within these constraints:
- Use sprint planning to identify critical assumptions, not just estimate stories
- Allocate capacity for spikes and treat them as legitimate work
- Make "triggers for reconsideration" an explicit part of sprint commitments
- When discovery invalidates the plan mid-sprint, call it out and negotiate rather than silently cutting corners

The framework isn't the enemy; the lack of discipline is. **The point is simpler: test your assumptions, commit to measurable outcomes, and be willing to stop and realign when you learn something important.** You can practice this discipline within any framework. It just requires courage to say "we learned something important; let's pause and reconsider" even when the calendar says to keep moving.

## What Real Agreement Requires

The [AAA Cycle](/study-guides/sdlc/aaa-cycle.html) provides the discipline:

**Align** = Understand the problem before proposing solutions
- What are we trying to accomplish?
- What do we actually know vs. assume?
- Identify and test critical assumptions before committing
- What are the critical unknowns?

**Agree** = Commit to specific, quantifiable outcomes with known constraints
- What are the use cases and edge cases we're handling?
- What trade-offs are we accepting and what do we gain?
- What does "done" look like in measurable terms?
- **What triggers reconsideration?**

**Apply** = Honor the agreement while surfacing learnings
- Build what was agreed (not what's easiest)
- Document what we discover
- **Trigger realignment when assumptions break**

AAA is harder than Scrum because it requires thinking and courage. You can't hide behind "the story says" or "the sprint ends Friday." You must understand the problem deeply enough to agree on a quantifiable solution. You must say "we learned something that invalidates this approach; let's stop and reconsider" even when it's uncomfortable.

Scrum is easier because it's mechanical: pick stories, estimate, commit, deliver, repeat. No hard conversations required. No accountability to actual value. But mechanical process without understanding produces mechanical results: code that "works" in the narrowest sense but fails to deliver value.

## Feature-Based vs Interval-Based Frameworks

The fundamental issue with Scrum is that it's interval-based, not feature-based. Scrum organizes work around time intervals (sprints), not around completing features. This creates structural pressure that makes team misalignment more likely.

**Interval-based frameworks** (Scrum, traditional sprints):
- Organize around fixed time periods
- Success = finishing when the interval ends
- Metrics focus on velocity and sprint completion
- Discovery threatens the schedule
- "Done" means "the sprint is over"
- **Creates risk of misalignment** because teams may ship to meet the timebox rather than the outcome

**Feature-based frameworks** (Shape Up, incremental delivery):
- Organize around completing defined features
- Success = delivering the agreed outcome
- Metrics focus on value delivered
- Discovery informs scope adjustment
- "Done" means "we delivered what we agreed to build"
- **Supports alignment** because commitment is to the outcome, not the calendar

Feature-based frameworks naturally support the discipline of agreement. You define an initial outcome and commit to delivering value, not hitting a timeline. When discovery reveals complexity or better approaches, you reconsolidate the agreement by adjusting scope within the feature boundary, extending the work, or pivoting based on what you learned. The feature commitment creates accountability to an outcome, not to a calendar.

Interval-based frameworks make alignment harder. The timebox becomes the commitment. "Done" becomes arbitrary; whatever state the code is in when the sprint ends. Discovery becomes an inconvenience rather than legitimate learning. Teams become misaligned on what "done" even means.

This doesn't mean interval-based frameworks doom teams to misalignment. But they require extra discipline to maintain focus on outcomes over bureaucracy. Teams must consciously resist the pressure to ship incomplete work just because the calendar says so, and actively work to stay aligned on actual value delivery.

The SDLC landscape offers many approaches: [Shape Up](/study-guides/sdlc/shape-up.html) prioritizes shaping work before betting on it. Kanban focuses on flow and continuous delivery. Lean emphasizes eliminating waste by validating assumptions early. Each has strengths.

But no framework can prevent organizational dysfunction. Leadership that demands certainty over understanding will corrupt any approach. What matters isn't the framework. It's the discipline of real agreement: identify assumptions, test them, commit to quantifiable outcomes, realign when discovery demands it.

## The Choice

You can continue the pattern: estimate based on assumptions, commit to fictional agreements, ship whatever fits the timebox, call it "done" when the sprint ends, and hope you're delivering value.

Or you can demand discipline: discover what you're building before estimating, test your assumptions, agree on quantifiable outcomes, build what was agreed or realign when discovery demands it, and measure whether you actually delivered value.

**You cannot iterate on what you cannot quantify. Without agreement on measurable outcomes, you're just building things and hoping they matter.**

That's not agile. That's hope masquerading as a process.
