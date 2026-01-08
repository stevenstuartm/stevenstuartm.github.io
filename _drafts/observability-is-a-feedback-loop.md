---
layout: post
title: "Observability Is a Feedback Loop"
date: 2025-01-07
description: "Many organizations have invested heavily in observability tooling but gained little operational insight. Dashboards exist that nobody watches. Alerts fire that nobody investigates. The appearance of observability substitutes for the reality of understanding your systems."
series: "Technology & Tools"
tags: [observability, monitoring, devops, architecture, operations]
---

## The Observability Paradox

We have more visibility into our systems than ever before. Dashboards proliferate. Alerts stream into Slack channels. Terabytes of logs accumulate in aggregation platforms. Yet when something breaks, engineers still find themselves asking: "What actually happened?"

The tooling exists. The data exists. The understanding doesn't.

This gap between observability investment and operational insight is widespread. Organizations buy sophisticated platforms, instrument their services, build dashboards during incidents, configure alerts on everything that moves—and somehow end up less able to answer basic questions than they were before. Not because the tools are bad, but because observability isn't a tooling problem. It's a design problem.

## The Dashboard Graveyard

Every organization has one. A folder somewhere in Grafana or Datadog filled with dashboards created during incidents, never looked at again, slowly rotting as the system evolves.

The pattern is predictable. Something breaks at 2 AM. Engineers scramble to understand what's happening. Someone creates a dashboard to visualize the relevant metrics. The incident resolves. The dashboard is never opened again.

Three months later, the services those dashboards monitor have changed. The metrics they display may no longer exist. The thresholds they highlight are no longer meaningful. But the dashboards remain, accumulating like sediment, creating the illusion of coverage.

Nobody owns these dashboards. Nobody maintains them. They were created to answer a specific question during a specific crisis, and once that crisis passed, so did their relevance. Yet they persist in the navigation menu, making the observability estate look more comprehensive than it actually is.

The dashboard graveyard isn't a cleanup problem. It's a symptom of reactive instrumentation—building visibility in response to incidents rather than in anticipation of operational questions. When dashboards are created under pressure, they're optimized for the crisis at hand, not for ongoing operational understanding.

## Alert Fatigue Is a Design Failure

When alerts are routinely ignored, the conventional diagnosis is operator desensitization. Engineers have become numb to notifications. The solution, supposedly, is better discipline—pay attention to your alerts.

This gets causality backwards. Alert fatigue isn't a discipline problem. It's a design failure.

Consider a payment processing system. A customer attempts a purchase, but their card is declined due to insufficient funds. The payment gateway returns a rejection. The system logs this as an ERROR.

This is the system working correctly. The card was declined because it should have been declined. Insufficient funds is a handled business case, not an exception. But because it's logged as an error, it shows up in error dashboards. It triggers error-rate alerts. It contributes to the ambient noise that operators learn to ignore.

Over time, "payment errors" become background radiation. The team knows most of them are just declined cards, so they stop investigating. Then a real problem emerges—the payment gateway starts timing out, or an integration partner pushes a breaking change—and it gets buried in the noise. Nobody notices because "payment errors are always high."

The fix isn't more vigilant operators. The fix is correctly categorizing what an error actually is:

- **Expected success**: The happy path. Does this even need to be logged at verbose levels?
- **Expected failure**: Business logic correctly rejecting something—declined payments, validation failures, rate limiting. This is INFO, not ERROR.
- **Unexpected failure**: Something genuinely went wrong that demands investigation. This is a true exception.

When these categories blur together, everything becomes noise. When alerts fire for expected failures, operators learn that alerts are usually false positives. When operators learn that alerts are usually false positives, they stop responding to alerts. When they stop responding to alerts, real incidents get missed.

Alert fatigue is the predictable consequence of logging design that doesn't distinguish between "the system handled this correctly" and "something is actually broken."

## The Archaeology Problem

"Can you verify the performance of this component?"

"Can you check the errors for tenant X over the past week?"

These questions should be simple. In a well-designed observability system, they take minutes. In most organizations, they take hours—if they can be answered at all.

The problem isn't the tooling. I've seen New Relic implementations that required genuine expertise just to construct basic queries, not because New Relic is inherently complex, but because the organization's instrumentation was inconsistent, logs were unstructured, and correlation IDs either didn't exist or didn't propagate reliably. Every investigation became archaeology.

I've also seen AWS CloudWatch setups that made these questions trivial to answer—not because CloudWatch is more powerful, but because the team had discipline around log formatting, context propagation, and trace correlation. The simpler tool, properly implemented, outperformed the sophisticated tool poorly implemented.

The pattern that kills observability isn't tooling choice. It's fragmentation:

- Logs from different services in different formats
- Correlation IDs that don't propagate across service boundaries
- Metrics in one system, logs in another, traces in a third—with no reliable way to connect them
- Imported logs from managed services and third parties that don't conform to your conventions
- Query interfaces that require arcane knowledge of both the tool AND your organization's idiosyncratic implementation

Without consistent formatting and reliable correlation, there's no single source of dependable data. Engineers give up trying to use the observability stack because using it is harder than just reading code and making educated guesses.

## Metrics Without Questions

Instrument everything. Capture all the data. We'll figure out what questions to ask later.

This approach feels prudent. Storage is cheap. You never know what metrics will matter during an incident. Better to have data you don't need than need data you don't have.

The result is metrics sprawl—thousands of time series capturing every conceivable measurement, with no organizing principle connecting them to operational questions. CPU utilization, memory pressure, request latency at p50/p95/p99, queue depths, connection pool usage, cache hit rates, garbage collection pauses, thread counts, file descriptor usage—all captured, all graphable, none of it connected to "how do I know if this system is healthy?"

Data collection becomes a substitute for understanding. The team can point to dashboards full of charts without being able to explain what those charts should look like when things are working correctly, or what deviations actually indicate problems versus normal variation.

Effective instrumentation starts with questions:

- What does healthy look like for this service?
- What are the early warning signs that something is degrading?
- When an incident occurs, what information do we need to diagnose root cause?
- What questions did we struggle to answer in past incidents?

Without these questions driving instrumentation decisions, you end up with data graveyards that mirror the dashboard graveyards—vast accumulations of measurements that nobody looks at because nobody knows what they mean.

## The Three Pillars Myth

Logs, metrics, and traces. The three pillars of observability. Get all three, and you can debug anything.

Except you can't.

The three pillars are capabilities, not outcomes. Having logs doesn't mean your logs are useful. Having metrics doesn't mean your metrics answer operational questions. Having traces doesn't mean your traces actually connect the dots from symptom to cause.

A system can have all three pillars and still be opaque:

- Logs exist but aren't structured, aren't correlated, and bury signal in noise
- Metrics exist but aren't connected to health indicators or alerting thresholds
- Traces exist but don't propagate context across service boundaries

The pillars are tools. Observability is what you do with them. The distinction matters because teams often treat pillar implementation as the goal—we have logging, we have metrics, we have tracing, checkbox complete—without asking whether those implementations actually enable understanding.

## Observability vs. Monitoring

These terms get used interchangeably. They shouldn't.

Monitoring tells you something is wrong. Error rate exceeded threshold. Latency spiked. CPU is maxed out. Monitoring is necessary—you need to know when systems are unhealthy.

Observability helps you understand why. Given that something is wrong, can you follow the thread from symptom to cause? Can you answer novel questions about system behavior without adding new instrumentation?

That last part is the key distinction. Monitoring tells you *that* there's a problem. Observability lets you investigate problems you didn't anticipate, ask questions you didn't predefine, and understand behavior you didn't explicitly instrument for.

Most teams have monitoring and call it observability. They know when things break; they just can't figure out why without extensive manual investigation, adding ad-hoc logging, and waiting for the problem to recur.

The test for actual observability: when an unfamiliar symptom appears, can engineers investigate it systematically using existing instrumentation? Or do they have to add new logging, redeploy, and wait for it to happen again?

## The Cost Dimension

Observability tooling is expensive. Log aggregation at scale costs real money. APM platforms charge per host or per ingested gigabyte. The observability line item on infrastructure budgets has grown substantially over the past decade.

This spend is justified if it reduces incident duration, prevents outages, or accelerates debugging. But in many organizations, the return on observability investment is unclear at best. The tools exist. The dashboards exist. Incidents still take just as long to resolve because nobody can navigate the data.

When observability tooling becomes shelfware—expensive infrastructure that engineers route around rather than rely on—it's just spend. Worse, it's spend that creates the illusion of capability. Leadership sees the dashboards and assumes operational visibility exists. Engineers know the dashboards are useless but don't have standing to challenge the investment.

The cost question isn't "how much are we spending on observability?" It's "what are we getting for that spend?" If investigations still require reading code and making guesses, if incidents still take hours to diagnose, if engineers still say "I don't know, let me add some logging"—the tooling isn't delivering value regardless of its sophistication.

## What Actual Observability Looks Like

The common thread through every observability failure—dashboard graveyards, alert fatigue, investigation archaeology—is disconnection. The people designing instrumentation aren't the people using it at 3 AM. The people creating alerts aren't the people being paged. The people building dashboards aren't the people trying to answer operational questions with them.

Observability improves when builders own operations.

### Ownership Changes Everything

When developers are responsible for running what they build, observability stops being an afterthought. You don't log payment declines as errors when you're the one who'll be paged for "high error rate on payment service." You don't create dashboards during incidents and abandon them when you're the one who needs those dashboards working next month. You don't instrument everything and figure out questions later when you're the one drowning in meaningless metrics.

Shift-left isn't just about catching bugs earlier. It's about creating feedback loops that make the consequences of poor observability design immediate and personal. When you own the code, the deployments, and the 2 AM pages, you develop a visceral understanding of what "good observability" actually means. It means you can sleep. It means incidents are diagnosable. It means alerts that fire are alerts worth waking up for.

The teams with the best observability aren't the ones with the most sophisticated tooling. They're the ones where the distance between "I wrote this code" and "I'm responsible when it breaks" is zero.

### The Black Box Mindset

There's a telling difference between developers who test primarily in local environments versus those who test against remote systems. Local testing offers a crutch: when something behaves unexpectedly, you attach a debugger, set breakpoints, and step through execution line by line. You can see inside the box.

Remote testing denies you that luxury. When you can only observe inputs and outputs—when you can't pause execution and inspect state—you're forced to write code that explains itself through its observable behavior. You need structured logs that tell a story. You need traces that connect cause to effect. You need error messages that actually describe what went wrong.

Developers who live in black box environments write more observable code because they've already experienced the constraint. They've felt the frustration of "something broke and I have no idea why" without the escape hatch of a debugger. That experience shapes how they think about instrumentation.

White box thinking says: "I can always figure it out if I need to."
Black box thinking says: "I need to know what happened from what the system tells me."

Production is a black box. The code you deploy will run in environments where you can't attach a debugger. If your testing doesn't prepare you for that reality, your instrumentation won't either.

### Observing the Observers

Here's the meta-insight: if you're observed observing, you'll architect differently.

When observability is someone else's problem—a platform team's responsibility, an SRE's concern—there's no accountability for observability quality. Developers instrument without thinking. Log levels are arbitrary. Alerts are configured and forgotten. Nobody experiences the consequences of these decisions except the people who didn't make them.

But when your dashboards are visible to your team, when your alert configurations are reviewed, when your on-call experience is shared context—the incentives shift. You maintain what you use. You design alerts that mean something because you'll be the one responding to them. You keep signal-to-noise ratio healthy because the noise is your noise.

The best observability implementations aren't technically superior. They're culturally aligned. The people who can improve observability are the same people who suffer when it's poor.

### Practical Shifts

None of this means every organization needs to go full "you build it, you run it." But the principle scales down to individual practice:

**Test like you can't debug.** Force yourself to diagnose issues from logs and metrics before reaching for a debugger. If you can't figure out what happened from observable outputs, your instrumentation needs work—and you'll discover that before production does.

**Own your alerts.** If you're configuring an alert, ask: "Would I want to be woken up for this?" If the answer is no, either the alert shouldn't exist or the severity is wrong. Alerts that nobody wants to respond to are alerts that won't be responded to.

**Question before instrumenting.** Before adding a metric or log statement, articulate the question it answers. "What will I learn from this? What action would I take based on different values?" If you can't answer, you're adding noise.

**Maintain what you create.** That dashboard you built during the last incident? Either maintain it as part of your operational toolkit or delete it. Abandoned dashboards create the illusion of coverage while providing none.

**Classify severity honestly.** Is this an error (something unexpected that demands investigation) or an expected outcome (business logic working correctly)? The distinction matters. When you're on call, you'll wish you'd made it correctly.

The path to actual observability isn't better tooling. It's shorter feedback loops between the people designing systems and the people understanding them in production—ideally, the same people.
