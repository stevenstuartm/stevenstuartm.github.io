---
layout: post
title: "Why Your Agile Team Might Be Building on Hope, Not Discipline"
date: 2025-10-23
description: "It is impossible to deliver what is expected and valuable if there has been no agreement on the expectation. Without discovery and genuine agreement, you're operating on hope, not discipline."
tags: [agile, requirements, aaa-cycle, estimation]
---

## Agreement Requires Discovery

You cannot deliver value without agreement on what constitutes value. You cannot have agreement without discovery of what you're actually building. And you cannot apply discovery to improve the agreement if you're afraid of "documentation" and refuse to step outside pointless timeboxes and absurd estimations based on nothing but assumptions.

<blockquote class="pull-quote">
<p>Without agreement on what constitutes value, you're not iterating toward anything. You're operating on hope, not discipline.</p>
</blockquote>

## Misalignment Disguised as Agreement

Software development frequently operates on fictional agreements, creating misaligned teams.

The problem isn't new to "Agile" methodologies. Waterfall documentation could be equally full of untested assumptions and vague requirements. But user stories have made the problem worse by treating minimal documentation as a virtue. Scrum, the dominant framework in most Agile transformations, has turned this into structural dysfunction.

A user story like "As a user, I want to search products" is not an agreement. It's a placeholder. Teams estimate it ("Five points"), commit to it, hand it to a developer, and expect results. But what does "search" mean? What edge cases exist? What trade-offs are acceptable? How do we measure success?

None of this was discussed. But everyone acts as if agreement exists. When the developer delivers something that vaguely resembles search, the story is marked "done." The team remains misaligned on whether value was delivered because there was never genuine agreement on what "done" meant.

## Why We Don't Test Assumptions

Estimating based on untested assumptions is not planning. It's guessing. And when teams base commitments on guesses, they're building on sand.

The pattern is familiar: estimate based on assumptions, commit to the estimate, discover during implementation that the assumptions were wrong, then ship anyway because the timebox ends. Discovery gets reframed as scope creep rather than learning. The timebox becomes more important than the outcome.

In the real world, implementation reveals hidden complexity. Edge cases emerge. Dependencies appear. Most teams don't have the discipline to pause and realign when discovery changes everything.

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

Testing assumptions prevents building the wrong thing. But this discipline directly conflicts with how most teams actually work. Scrum, the dominant framework in Agile transformations, has no mechanism for this. Sprint planning happens in hours. There's no time to test assumptions; teams just estimate based on them and commit.

### The Spike Problem

The conflict becomes obvious the moment someone suggests introducing spikes. A spike is exploratory work to reduce uncertainty: exactly what testing assumptions requires.

But spikes create political and metric chaos in Scrum:
- **How do you estimate a spike?** The whole point is you don't know enough to estimate
- **How do you measure velocity?** Spikes don't deliver features
- **What happens if the spike invalidates the sprint plan?** Scrum has no answer
- **Do spikes count as "done" work?** They produce knowledge, not shippable code

Teams resort to absurdities: estimating the exploration itself (defeating the purpose), hiding spikes as "technical tasks" within stories (obscuring what's actually happening), or skipping spikes entirely and guessing (back to building on sand).

<blockquote class="pull-quote">
<p>Frameworks like Scrum optimize for predictable metrics while actual work requires validated understanding. Discovery threatens the illusion of control.</p>
</blockquote>

The spike problem reveals a fundamental tension.

This tension exists in most organizations. Teams recognize when they're misaligned: estimates feel like guesses and commitments feel fictional. But introducing discipline like assumption testing creates friction: it reveals uncertainty, delays commitment, and challenges established metrics. The question becomes: how do misaligned teams regain alignment within systems that resist it?

## The False Dilemma

The immediate objection is predictable: "You're advocating for analysis paralysis. We can't spend months discovering requirements before shipping anything."

This is a false dilemma. The choice isn't between doing nothing and doing everything. It's not "ship immediately with no understanding" versus "achieve perfect knowledge before starting."

**This is about being actually agile.**

True agility means adapting to changing priorities and changing understanding. Discovery is inevitable. That means having the discipline to incorporate what you discover, not shipping anyway because the timebox ends.

The discipline isn't perfect upfront requirements or endless discovery. It's simpler:
1. Identify what you know vs. what you're assuming
2. Test critical assumptions before making initial commitments (not all assumptions, just the ones that matter)
3. Agree on what "done" looks like with explicit constraints and success criteria
4. Discover new information during implementation (this will happen)
5. **Pause and reconsolidate the agreement when discovery changes everything**
6. Update the agreement based on what you learned and continue, or deliver what was agreed

This is continuous alignment, not upfront perfection. You start with enough understanding to commit responsibly, then maintain discipline to realign as you learn.

**How much initial discovery is enough?** Enough to commit responsibly to specific outcomes while acknowledging what you don't yet know. For a simple CRUD screen, that might be 30 minutes of conversation. For a complex workflow with edge cases and integrations, it might be a week of prototyping and user testing. The rigor matches the risk. But this is just the starting point; you'll continue discovering and realigning throughout implementation.

**What about real-world constraints?** Leadership demands roadmaps. Sales needs commitments. The business can't wait. True. But shipping the wrong thing on schedule doesn't solve those constraints. It just delays the reckoning. The choice is: negotiate realistic commitments based on actual understanding, or make fictional commitments and deal with the consequences later.

**Isn't this just good engineering?** Yes. That's exactly the point. The discipline of testing assumptions, agreeing on outcomes, and realigning based on discovery is what competent engineering looks like. Scrum's structure actively works against this discipline by optimizing for predictable metrics (velocity, sprint completion, roadmap commitments) over validated understanding.

## What Real Agreement Requires

The [AAA Cycle](/study-guides/sdlc/aaa-cycle.html){:target="_blank" rel="noopener noreferrer"} provides the discipline:

**Align** = Understand the problem before proposing solutions
- What are we trying to accomplish?
- What do we actually know vs. assume?
- Identify and test critical assumptions before committing
- What are the critical unknowns?

**Agree** = Commit to specific outcomes with known constraints and clear success criteria
- What are the use cases and edge cases we're handling?
- What trade-offs are we accepting and what do we gain?
- What does "done" look like specifically?
- **What triggers reconsideration?**

**Apply** = Honor the agreement while surfacing learnings
- Build what was agreed (not what's easiest)
- Document what we discover
- **Trigger realignment when assumptions break**

AAA is harder than Scrum because it requires thinking and courage. You can't hide behind "the story says" or "the sprint ends Friday." You must understand the problem deeply enough to agree on a specific solution with clear success criteria. You must say "we learned something that invalidates this approach; let's stop and reconsider" even when it's uncomfortable.

Scrum is easier because it's mechanical: pick stories, estimate, commit, deliver, repeat. No hard conversations required. No accountability to actual value. But mechanical process without understanding produces mechanical results: code that "works" in the narrowest sense but fails to deliver value.

## Interval-Based vs Flow-Based Frameworks

The fundamental issue with Scrum is that it's interval-based, not flow-based. Scrum organizes work around time intervals (sprints), not around completing features. This creates structural pressure that corrupts even teams that start with genuine alignment.

### The Corruption Pattern

Timeboxes corrupt alignment. Here's how it happens:

A team begins with clear understanding. They know the problem, they've identified the stakeholders, and they've agreed on what success looks like. Leadership decides to "adopt Scrum" to make the project more predictable. Sprint planning begins.

The first sprint ends. The feature isn't done, but the sprint is. The team demonstrates half-finished work. They celebrate "shipping on time" even though nothing actually shipped.

The second sprint ends. The feature is closer but still incomplete. Different parts were built in different sprints. Integration becomes a problem deferred to "later." The retrospective focuses on improving the sprint process, not on why the feature is fragmented.

By the third sprint, the team has stopped thinking about features at all. They think about story points, velocity, and sprint goals. The metric became the mission. The feature (the actual deliverable) is now secondary to completing the sprint.

This isn't a failure of discipline. This is the timebox doing exactly what it's designed to do: force artificial breaks in meaningful momentum. The team had alignment. The timebox destroyed it by substituting process compliance for value delivery.

### The Data: Projects Still Failing

Despite two decades of Agile adoption, project failure rates remain staggering:

- Projects adopting Agile Manifesto practices are **268% more likely to fail** than those which do the opposite (Source: [Engprax 2024 Study](https://www.engprax.com/post/268-higher-failure-rates-for-agile-software-projects-study-finds){:target="_blank" rel="noopener noreferrer"} of 600 UK/US software engineers)
- Only **42% of Agile projects succeed**; 47% are late, over budget, or fail to satisfy customers, and 11% fail completely (Source: Standish Group CHAOS Report 2020: Beyond Infinity)
- **47% of Agile Transformations fail**, and since 77% of those transformations are Scrum transformations, most failures are down to Scrum implementation (Source: [Scrum Inc.](https://www.scruminc.com/why-47-of-agile-transformations-fail/){:target="_blank" rel="noopener noreferrer"})

The problem isn't "bad implementation." The problem is that Scrum protects leaders from accountability, not teams from failure. Velocity metrics give the illusion of progress. Sprint completions create the appearance of discipline. Leadership can point to charts and burndown graphs while the product slowly dies.

### Even the Authors Know

The original authors of the Agile Manifesto have watched what happened to their creation and expressed public disappointment. While they don't "own" agile principles, their voices carry weight as witnesses to how corporate frameworks and certification mills corrupted values into commodities.

**Dave Thomas**, one of the 17 Manifesto signatories, declared "[Agile is Dead](https://pragdave.me/blog/2014/03/04/time-to-kill-agile.html){:target="_blank" rel="noopener noreferrer"}" in 2014. He argued that the word "agile" had been subverted to the point of meaninglessness, with the agile community becoming an arena for consultants and vendors to sell services and products. Thomas notably refused to participate in Agile events after Snowbird, didn't affiliate with the Agile Alliance, and didn't do any "agile" consultancy. His critique focused on how commercialization conflicted with the original spirit of the Manifesto.

**Ron Jeffries**, co-creator of Extreme Programming and Manifesto signatory, published "[Developers Should Abandon Agile](https://ronjeffries.com/articles/018-01ff/abandon-1/){:target="_blank" rel="noopener noreferrer"}" in 2018. He coined the terms "Faux Agile" and "Dark Agile" to describe approaches that made developers' lives worse rather than better. Jeffries heard from many developers that "Agile sucks" and "Scrum sucks" because most organizations claiming to do "Agile" were actually doing Scrum. He noted that poor implementations lead to more interference with developers, less time to do the work, higher pressure, and demands to "go faster." Even Ken Schwaber, one of Scrum's creators, admitted this situation made him sad.

**Martin Fowler** identified "the Agile Industrial Complex" as the first major problem facing agile software development in his 2018 keynote at Agile Australia. He described the collection of consultants, experts, and managers who try to assert "best practice" rather than letting teams decide how to work. Fowler argued that "a lot of what is being pushed goes really against a lot of our precepts," particularly the realization that people operate at their best when they choose how they want to work. He called the Agile Industrial Complex imposing methods upon people "an absolute travesty."

**Allen Holub** (not a Manifesto signatory, but a prominent agile advocate who has worked closely with several signatories) has been particularly vocal. He states that Scrum has never been about real agility and is all about selling certificates. Holub argues that you can "implement Scrum perfectly and not be in the least bit agile." He notes that words like "certification," "Scrum master," "Sprint," and "story point" do not appear in the Agile Manifesto and Principles. At the very top of the Manifesto is "Individuals and interactions over processes and tools," yet the word "agile" has come to mean rigid adherence to both process and tools.

Even **Ken Schwaber**, Scrum's co-creator, has expressed disappointment: "Scrum has been more successful than I could have ever imagined, but I am still disappointed with most Scrum implementations." He has repeatedly noted that organizations are full of superficial adoptions including ScrumButs, FlaccidScrum, and Copy Paste Scrum.

Timeboxes and corporate frameworks have corrupted agile values. The certification industry turned principles into products. Scrum masters replaced collaboration with ceremony. Sprint planning replaced discovery with guessing. Velocity replaced value delivery with theater.

These corruptions didn't happen by accident. They happened because frameworks optimized for what executives want: predictability, metrics, and plausible deniability when projects fail. Scrum gives leadership charts and processes to point at while avoiding the hard work of genuine alignment. The timebox becomes a shield against accountability for whether anything valuable was actually built.

The authors don't own agile principles, but they watched those principles get buried under frameworks that sabotage the very values they tried to codify. That sabotage has caused, is causing, and will continue to cause projects to fail before they even start. Not because teams lack discipline, but because the frameworks they're forced to follow actively prevent the discipline that real agility requires.

### The Feedback Loop Lie

Scrum sells itself on "inspect and adapt." Feedback loops are supposed to compensate for uncertainty. They don't.

Feedback loops are lies when alignment doesn't exist first. Without genuine agreement on what you're building and why, iteration just cycles through the same confusion faster. The retrospective identifies process problems. The sprint review shows incomplete work. The daily standup surfaces blockers. None of this matters if the team never agreed on what they're building or why it matters.

Here's what Scrum doesn't measure:
- Quality of the solution
- Customer satisfaction with the outcome
- Whether the feature solves the actual problem
- Whether the team understood what they were building

Here's what Scrum does measure:
- Velocity (how fast you're going in the wrong direction)
- Sprint completion (ceremony compliance)
- Story point burndown (imaginary progress on imaginary units)

Scrum cannot be done "correctly" because it optimizes for the wrong things. It doesn't demand alignment. It doesn't place customer needs above ceremony compliance. It's a system of fear and defensiveness disguised as empiricism.

The abstraction is the point. Scrum keeps everyone in the dark so failure looks like "part of the plan." The product isn't done, but the sprint is. The customer isn't satisfied, but velocity is stable. The architecture is collapsing, but the burndown chart looks good.

### Framework Comparison

<div class="comparison">
<div class="content-card content-card--accent-warning">
<h4>Interval-Based Frameworks</h4>
<p><em>Scrum, traditional sprints</em></p>
<ul>
<li>Organize around fixed time periods</li>
<li>Success = finishing when the interval ends</li>
<li>Metrics focus on velocity and sprint completion</li>
<li>Discovery threatens the schedule</li>
<li>"Done" means "the sprint is over"</li>
<li><strong>Corrupts alignment</strong> by making the timebox the commitment instead of the feature</li>
</ul>
</div>
<div class="content-card content-card--accent">
<h4>Flow-Based Frameworks</h4>
<p><em>Kanban, continuous delivery</em></p>
<ul>
<li>Organize around completing defined features</li>
<li>Success = delivering the agreed outcome</li>
<li>Metrics focus on lead time and value delivered</li>
<li>Discovery informs scope adjustment within the feature</li>
<li>"Done" means "we delivered what we agreed to build"</li>
<li><strong>Supports alignment</strong> because there's no artificial deadline</li>
</ul>
</div>
</div>

Flow-based approaches naturally support the discipline of agreement. You define an initial outcome and commit to delivering value, not hitting a timeline. When discovery reveals complexity or better approaches, you reconsolidate the agreement by adjusting scope within the feature boundary, extending the work, or pivoting based on what you learned. The feature commitment creates accountability to an outcome, not to a calendar.

Interval-based frameworks corrupt alignment by design. The timebox becomes the commitment. "Done" becomes arbitrary: whatever state the code is in when the sprint ends. Discovery becomes an inconvenience rather than legitimate learning. Teams become misaligned on what "done" even means because they're optimizing for sprint completion, not feature completion.

Simpler, more honest approaches deliver clarity through human connection and contextual decisions. They maintain that clarity by refusing to compromise on alignment and the application of genuine agreements. When alignment exists, the timebox is redundant. When alignment doesn't exist, the timebox is a distraction masquerading as a discipline.

### Alternatives That Support Alignment

**Kanban** eliminates timeboxes entirely. Work flows continuously based on capacity, not calendar. Features are pulled when there's capacity to work on them and completed when they're actually done. WIP (work in progress) limits prevent overload without imposing artificial deadlines. "Done" means the feature delivers the agreed value, period.

**Lean Software Development** focuses on eliminating waste, including wasteful ceremonies that create the illusion of progress. Deliver fast by removing delays and validating assumptions early, not by imposing timeboxes that fragment features. Amplify learning through rapid feedback on working software, not through retrospectives about process compliance.

**Extreme Programming (XP)** emphasizes practices over process: test-driven development, continuous integration, pair programming, and collective code ownership. These practices create the technical agility to respond when discovery changes understanding. "Done" means passing tests and meeting acceptance criteria, not surviving until the sprint ends.

None of these approaches are perfect. Leadership that demands certainty over understanding will corrupt any framework. But these approaches don't have Scrum's structural flaws. They don't force artificial breaks in momentum. They don't make the calendar more important than the outcome. They support alignment instead of corrupting it.

## The Choice

You can continue the pattern: estimate based on assumptions, commit to fictional agreements, ship whatever fits the timebox, call it "done" when the sprint ends, and hope you're delivering value.

Or you can demand discipline:
- Discover what you're building before estimating
- Test your assumptions
- Agree on specific outcomes with clear success criteria
- Build what was agreed, or realign when discovery demands it
- Measure whether you actually delivered value

You cannot iterate toward value without agreement on what constitutes value. Without genuine agreement on outcomes, you're just building things and hoping they matter.

<blockquote class="pull-quote">
<p>That's not agile. That's hope masquerading as a process.</p>
</blockquote>
