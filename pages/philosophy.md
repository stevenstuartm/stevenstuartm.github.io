---
layout: page
title: Philosophy
description: "Seven disciplines that guide how I approach software development, architecture, leadership, and career growth."
permalink: /philosophy.html
---

## What I Believe

These disciplines represent my current understanding of what makes software development work. They're informed by years of building systems, leading teams, and watching projects succeed and fail.

---

## 1. Seek Hardship

<blockquote class="pull-quote">
<p>If you are not sincerely seeking truth, you will never accept it.</p>
</blockquote>

There's a difference between ten years of experience and one year repeated ten times. Real accumulation means building new capabilities, taking on broader responsibilities, and establishing feedback loops that expose what you don't know. Staying comfortable feels like progress but produces competence at yesterday's problems.

Seek problems you can't yet solve and questions you don't yet know to ask. The most dangerous gaps are the ones you can't see. Maintain quality independent of approval; no one flagging your code doesn't mean the code is good.

**Going deeper**: [What Engineering Leaders Ask That Others Don't](/blog/2025/06/11/characteristics-of-leaders-mentors-software-development.html){:target="_blank" rel="noopener noreferrer"} examines the questions that reveal leadership characteristics.

---

## 2. Build to Learn

<blockquote class="pull-quote">
<p>Real capability comes from building, failing, and fixing, not collecting badges.</p>
</blockquote>

Learning platforms sell completion checkmarks and the feeling of progress, not actual capability. That green badge feels good, but it doesn't mean you can build something without the training wheels.

Watching someone else code doesn't teach you to code, just like watching diving competitions doesn't teach you to swim. Understanding concepts intellectually isn't the same as being able to do. Sandboxed environments with no dependency conflicts, no environment setup, and no deployment challenges create the illusion of progress while keeping you dependent on structured guidance.

Real learning happens when you're forced to make decisions without a script, when you get stuck and have to figure out why, when you realize your solution doesn't scale and you need to rethink it. Build real projects, even terrible ones. That broken app taught you more than any polished tutorial. Read official documentation; framework creators document their tools better than third-party instructors. Study real code; thousands of production codebases are available to learn from.

The pattern is simple: do something, fail at it, learn why you failed, improve, repeat. No platform can give it to you because it requires struggle.

**Going deeper**: [Learning Platforms Sell Badges, Not Skills](/blog/2025/08/27/why-i-cancelled-all-learning-subscriptions.html){:target="_blank" rel="noopener noreferrer"} explains why building beats consuming.

---

## 3. Genuine Discipline Comes from Core Values

<blockquote class="pull-quote">
<p>Most project failures stem from broken values, not broken processes.</p>
</blockquote>

I've watched teams follow every ritual in the Scrum guide and still fail spectacularly. The standups happened, the retrospectives happened, the burndown charts looked great. But the team started with solutions before understanding needs, collected sign-offs instead of building genuine commitment, and chased task completion instead of honoring agreements. The process was perfect; the values were broken.

<div class="card-group">
<div class="content-card content-card--accent">
<h4>Align</h4>
<p>Human connection comes first. Before solutions, timelines, or technology, connect with people. Alignment is building understanding and trust, not extracting requirements.</p>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Agree</h4>
<p>Shared commitment matters. Agreement isn't documentation or sign-offs; it's mutual understanding and genuine commitment to walk the path together.</p>
</div>
<div class="content-card content-card--accent-warning">
<h4>Apply</h4>
<p>Honor what was agreed. The goal isn't "delivery"; it's applying the agreement. When reality demands changes, return to align and agree again.</p>
</div>
</div>

This discipline transcends methodology. You can practice AAA within Scrum, Kanban, Waterfall, or whatever your organization uses. The ceremonies are secondary; the values are primary.

The discipline also extends to technical work. When engineers integrate code, they align on intentions before modifying shared code, agree on interfaces and contracts, and apply those agreements in implementation. Test-driven development embodies this directly: write the agreement first (the test), then honor it in implementation. CI/CD automates the verification, and build failures surface broken agreements. The same values that prevent project failures prevent integration failures.

Organizations often respond to past failures by adding controls: approval gates, mandatory reviews, process checkpoints. These look like risk mitigation but often indicate a lack of trust in the underlying values. If you need strangling controls to prevent bad outcomes, the discipline isn't there, and more process won't fix that.

**Going deeper**: [AAA Cycle](/study-guides/sdlc/aaa-cycle.html){:target="_blank" rel="noopener noreferrer"} explains the full discipline with practical guidance for each phase.

---

## 4. Measure Outcomes, Not Activity

<blockquote class="pull-quote">
<p>When a measure becomes a target, it ceases to be a good measure. — Goodhart's Law</p>
</blockquote>

Velocity charts go up and to the right. Sprint completions hit 100%. The dashboard is green. And the product slowly dies because no one asks whether any of it mattered.

Activity metrics measure how fast you moved, not whether you moved in the right direction. Story points completed tells you nothing about problems solved. Burndown charts tell you nothing about customer satisfaction. Code coverage tells you nothing about whether the tests catch real bugs. These metrics are easy to track and satisfying to optimize, which makes them dangerous. Teams optimize what they measure, and measuring activity produces more activity.

Outcome measurement requires harder questions. Did the feature solve the actual problem? Would users notice if we removed it? Did the architectural change actually improve reliability, or did we just move complexity somewhere else? These questions don't fit neatly into dashboards, but they're the only ones that matter.

**Going deeper**: [Why Your Agile Team Might Be Building on Hope, Not Discipline](/blog/2025/10/23/the-agile-masquerade.html){:target="_blank" rel="noopener noreferrer"} examines why frameworks that optimize for predictable metrics fail to deliver value.

---

## 5. Make Truth Accessible

<blockquote class="pull-quote">
<p>Clarity does not simplify truth. It makes truth accessible so that it can be held, tested, and defended by everyone it reaches.</p>
</blockquote>

A decision no one else can understand is a decision no one else can challenge. When architectural choices live in one person's head, when trade-offs are never written down, when technical rationale hides behind jargon that stakeholders can't engage with, the result isn't expertise. It's fragility. The team becomes dependent on whoever holds the context, and everyone else is left rubber-stamping decisions they can't evaluate.

Clarity is not simplification. Simplification strips nuance to make things easier; clarity preserves the full truth and makes it reachable. Documenting why you chose eventual consistency over strong consistency isn't dumbing it down. It's making the trade-off visible so that future teams can evaluate whether the conditions still hold. When the original constraints change and no one recorded what they were, the next team assumes incompetence rather than recognizing intentional trade-offs made under different circumstances.

This applies at every level. Architecture decision records capture the reasoning behind structural choices. Clear interface contracts make integration points understandable without tribal knowledge. Explicit success criteria make it possible to measure whether a feature delivered value. If you can't explain a decision clearly enough for someone else to challenge it, you might not understand it well enough yourself.

**Going deeper**: [The Measure of a Decision](/blog/2026/03/05/the-measure-of-a-decision.html){:target="_blank" rel="noopener noreferrer"} explores the criteria that determine whether decisions affecting others have integrity.

---

## 6. Complete Features, Not Intervals

<blockquote class="pull-quote">
<p>Time boundaries fragment work; feature boundaries deliver value.</p>
</blockquote>

Interval-based development organizes work around fixed time periods, not around completing features. When timeboxes become the primary organizing principle, they corrupt even well-aligned teams. Work fragments across sprint cycles. Features sit incomplete when boundaries arrive. Discovery mid-sprint forces awkward choices between shipping incomplete work or carrying it over.

The alternative is to organize around completing meaningful work. Shape features before committing to them: define clear boundaries, identify risks, clarify what "done" looks like. Give each feature appropriate time bounds based on its complexity, not universal sprint durations. Let work flow through the system when it's ready, not when the calendar says so. When time bounds are exceeded, stop and reassess rather than pushing through.

Rhythm and tempo come from alignment and natural feature boundaries, not predetermined calendars. Features take as long as they take, bounded by constraints that force honest conversations when things run long.

**Going deeper**: [Shaped Kanban: Complete Features, Not Sprints](/blog/2025/11/17/shaped-kanban.html){:target="_blank" rel="noopener noreferrer"} provides the complete framework for flow-based work with disciplined constraints.

---

## 7. Build for Change, Not Perfection

<blockquote class="pull-quote">
<p>Systems that survive aren't written perfectly; they bend without breaking.</p>
</blockquote>

You will never get it right the first time. That's not a failure; it's how software development works. Requirements clarify through building. Edge cases emerge through usage. Performance bottlenecks surface under real load. Teams that treat first attempts as gospel spend months polishing solutions to the wrong problem.

The systems that survive are the ones designed to evolve. Single responsibility keeps components focused so changes don't cascade. Dependency injection decouples implementations so they can be swapped. Configuration externalizes changeable behavior. Failing fast and loud surfaces problems immediately instead of hiding them.

These aren't academic principles. They're survival strategies. Perfect code written for yesterday's requirements fails when reality shifts. Adaptable code survives because it expects change.

**Going deeper**: [Adaptability Over Cleverness: What Makes Code Actually Good](/blog/2025/08/05/good-code-is-adaptable-code.html){:target="_blank" rel="noopener noreferrer"} examines principles and practices for building systems that evolve.
