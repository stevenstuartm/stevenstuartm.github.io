---
layout: post
title: "Troubleshooting Production: Discipline Under Pressure"
date: 2025-11-08
description: "The teams that resolve incidents fastest are the ones disciplined enough to slow down and understand what they're fixing. Reproduction is the fulcrum; without it, you're guessing. Master the fundamentals before the crisis hits."
series: "Development Practice"
tags: [incident-response, production, debugging, troubleshooting]
---

Something is broken in production, and you need to fix it. Whether you're investigating alone at 2 AM or coordinating a war room with twenty people, the principles are the same.

Most troubleshooting failures aren't from lack of effort; engineers work hard during incidents. The failures come from skipping fundamentals: investigating without reproduction, treating assumptions as facts, fixing symptoms instead of causes, changing multiple things simultaneously. These mistakes extend outages, create incomplete fixes, and guarantee you'll fight the same incident again.

Effective troubleshooting follows a disciplined process, one that works whether you're debugging locally or coordinating across systems. The teams that resolve incidents fastest are the ones disciplined enough to slow down and understand what they're fixing.

## Gather Facts, Not Interpretations

Pressure creates the urge to act immediately. The problem is, acting on incomplete information wastes more time than gathering facts would have taken.

You need facts, not interpretations. Facts are observable and measurable:
- Exact wording of error messages
- Precise timestamps with time zones
- Specific metric values showing deviation
- What changed recently (deployments, configuration, infrastructure, dependencies)

When someone says "the database is slow" or "the network is flaky" or "the deployment broke something," they're offering conclusions, not observations. These interpretations might be correct, but they skip the actual observation that leads to understanding. "The database is slow" tells you nothing actionable; you need to know what "slow" actually means. Is query execution time up? Is CPU saturated? Are there lock waits? Each observation leads to different investigations.

Start with these questions:
- **When did it start?** Exact time, gradual or sudden onset
- **What is the scope?** All users, specific regions, particular features, certain request types
- **What are the symptoms?** Error rates, latency percentiles, failure modes, resource consumption
- **What changed?** Deployments, configuration updates, traffic pattern shifts, dependency changes

Consider an API latency spike from 100ms to 2000ms. Facts gathered:
- **When did it start?** 14:47 UTC (sudden)
- **What is the scope?** Only read-heavy endpoints affected
- **What are the symptoms?** Database CPU at 95%, query execution times 20x normal
- **What changed?** Database maintenance window started at 14:45 UTC

Now you have an interpretation you can test: database maintenance degraded read performance. Check what the maintenance window did, verify query performance, and confirm the correlation.

During active incidents, capture artifacts immediately:
- Thread dumps or process snapshots showing current state
- Detailed logs with correlation IDs linking related events
- Metrics before, during, and after the issue
- Network traces showing request/response timing
- Resource utilization (CPU, memory, disk, network) across relevant systems

These artifacts become invaluable when you're trying to understand timing-dependent issues or correlate events across distributed systems.

## Test Assumptions, Don't Trust Them

Every incident reveals assumptions you didn't know you were making; under pressure, untested assumptions become expensive mistakes.

The pattern repeats: "The deployment succeeded" (but did health checks pass?), "The service is healthy" (but is it actually responding correctly?), "The cache is working" (but what's the hit rate?). Every incident surfaces assumptions about what "succeeded" or "healthy" or "working" actually means.

The most dangerous assumption is "the recent change was unrelated." This causes more extended outages than any other pattern. Correlation matters even when causation isn't obvious. Seemingly unrelated changes can have unexpected interactions. A configuration change in one system can affect dependencies in non-obvious ways. A deployment that touched "just the frontend" can expose race conditions in backend services. Don't dismiss correlation just because the connection isn't immediately clear.

Build verification into your communication. Transform assumptive questions into verifiable ones:
- Instead of "Is the service up?" → "Show me a successful request through the service right now"
- Instead of "Did the deployment finish?" → "What version is running in production, and how did you verify it?"
- Instead of "Are we getting traffic?" → "What's the current request rate compared to baseline?"

This shifts from binary yes/no answers to demonstrable evidence.

I've seen this pattern repeatedly: service returns 200 status codes, but users report errors. Everyone assumes "200 means success," then someone tests the assumption and discovers the application catches exceptions, logs them, and returns 200 with an error payload. The response body contains error messages, not successful data. The team was looking at the wrong signal the entire time.

## Reproduction: The Fulcrum of Investigation

Almost nothing in troubleshooting starts or finishes without reproduction. Miss this point and you could spend days searching for what you could have targeted in the first hour.

Think about what reproduction actually proves. If you can trigger the issue deliberately, you know the conditions that cause it; you understand not just that something broke, but why it breaks. Without that understanding, you're guessing about the problem and about whether your fix actually works.

Consider the typical pattern: users report intermittent login failures, you check logs, see authentication errors, and update session configuration. The errors stop. Did you fix it? Maybe the config helped, maybe the issue stopped on its own, maybe it's happening less frequently but you're not seeing it. You have no way to know, which means the next time it happens you start from zero again.

Compare that to actually reproducing the issue: you discover failures occur when the session store becomes unavailable, and you can trigger it by stopping the session store. Now you know what's happening. After your fix, stopping the session store no longer causes failures because you added failover logic. You proved the fix works. That's the difference reproduction makes.

### How to Reproduce

Start with the simplest reproduction path:
1. Can you trigger it in your local environment?
2. Can you recreate it in a test environment with production-like configuration?
3. Can you safely reproduce it in production under controlled conditions?

The key is isolating variables systematically:
- Test one factor at a time
- Control for data volume, timing, concurrent operations
- Document the exact sequence that triggers the issue

When you can't reproduce locally:
- Identify what's different (data scale, network topology, configuration, timing)
- Increase observability to capture detailed state when the issue occurs
- Use feature flags or canary deployments to test hypotheses in production safely

Here's a concrete example: application crashes under high load, and you suspect a race condition in request handling. Without reproduction, you modify the locking logic, deploy, and hope load testing catches any issues. With reproduction, you have a test case that consistently triggers the race condition. After your fix, the test passes. You know it works before it touches production.

The reproduction test case you built during the incident doesn't end when the incident ends. Turn it into an automated test. Not every issue can be captured this way; some depend on production scale or specific environmental conditions. But when you can automate the reproduction, you've built permanent protection. The problem that took hours to diagnose now fails a test in seconds if someone reintroduces it.

### Common Reproduction Mistakes

The most common mistake is assuming intermittent means irreproducible. Intermittent issues have conditions that trigger them; you just haven't identified the conditions yet. The issue might occur when specific events happen in a certain sequence, or when timing aligns in particular ways, or when resource thresholds are crossed. Calling it "intermittent" and moving on skips the investigation.

Another pattern: stopping investigation once you find correlation. Correlation shows you where to look; reproduction proves causation. Just because deployments happen before errors doesn't mean deployments cause errors. Reproduce the issue by deploying to prove the connection.

Then there's declaring victory too early: the issue hasn't recurred in an hour, so you close the incident, and it happens again the next day. Absence of the problem isn't proof you fixed it. Reproduction before and after the fix is proof.

## Change One Thing at a Time

Changing multiple variables simultaneously destroys your ability to understand what worked.

The discipline:
1. Change one variable
2. Observe the result
3. Document the outcome
4. Repeat

This feels slow, but it's faster than changing everything and having no idea what mattered.

Think about what happens when you make simultaneous changes. If it works, you don't know which change mattered. Did all three contribute, or was it just one? You'll never know, which means you've now committed to maintaining all three changes even though some might be irrelevant or even slightly harmful.

If it fails, you don't know which change made it worse. You can't roll back precisely. You have to revert everything and start over, losing whatever progress you might have made.

Legitimate exceptions exist:
- **Rolling back a deployment**: Reverting multiple coupled changes as a unit makes sense because they were deployed together
- **Emergency mitigation**: Immediate actions to restore service (like increasing resources) can happen together if they're all clearly mitigation, not fixes
- **Coupled changes**: Configuration that requires corresponding code changes should be deployed together

## Fix the Cause, Not the Symptom

Stopping at the first visible problem leaves root causes unaddressed. You'll fight the same incident again.

Understand the layers:
- **Symptom**: What you observe is broken
- **Surface cause**: The immediate technical reason for the symptom
- **Root cause**: Why the surface cause happened

Service returns 500 errors (symptom). Database connection pool exhausted (surface cause). Connection leak in error-handling code path (root cause). Fixing the symptom means restarting the service; it restores service temporarily. Fixing the surface cause means increasing pool size; it delays the inevitable. Fixing the root cause means patching the connection leak; it prevents recurrence.

The real fix emerges when you stop asking "why" and start seeing patterns. If the answer is "exception in cleanup code path," the fix isn't just patching that one path. It's recognizing that error-handling code paths lack test coverage across the system. The fix becomes adding tests for error scenarios and reviewing exception handling patterns throughout the codebase. That's how you prevent the next instance of this class of problem.

Distinguish mitigation from fix:

**Mitigation** (restores service quickly):
- Restart the service
- Route traffic around failing component
- Increase resource limits
- Roll back the deployment

**Fix** (prevents recurrence):
- Address root cause
- Add monitoring and alerting
- Improve test coverage
- Update runbooks

Both have value, but don't confuse them. Document the chain clearly:
- What we did to restore service (mitigation)
- What we're doing to prevent recurrence (fix)
- What we're adding to detect it earlier next time (observability)

This documentation becomes critical during post-mortems and when training new team members.

## War Rooms: Applying Principles Under Coordination Pressure

Everything above applies whether you're debugging alone or coordinating across teams. War rooms add coordination overhead; the principles don't change, but the communication requirements intensify.

### Roles

Establish clear roles upfront:
- **Incident Commander**: Coordinates response, makes final decisions, owns communication to leadership
- **Subject Matter Experts**: Investigate specific systems (database, network, application, infrastructure)
- **Scribe**: Documents timeline, actions taken, hypotheses tested, decisions made
- **Communications Lead**: Updates stakeholders, manages customer communication

Without role clarity, you get duplicate work, missed actions, and no record of what's been tried. The scribe role seems like a luxury, but it becomes critical when you need to reconstruct what happened.

Red flags:
- Multiple people issuing commands simultaneously
- No one writing down what's being tried
- Same hypothesis tested multiple times by different people
- Unclear who has authority to make rollback decisions

Apply the troubleshooting principles collectively through clear communication standards. For reproduction: "Can anyone reproduce this issue? If yes, document exactly how. If no, that's our first priority." For facts versus interpretations: "The database is slow" is an interpretation; "Database query time is 2000ms, baseline is 100ms" is a fact. For testing assumptions: when someone says "the service is healthy," the incident commander asks "Show me a successful request."

The incident commander explicitly approves changes and ensures only one change happens at a time across all teams. Before implementing a fix, confirm the team agrees on the root cause, not just the symptom being addressed.

### Hero mentality
Hero mentality in war rooms creates single points of failure and prevents knowledge sharing.

What hero mentality looks like:
- "I'll handle this alone; everyone else stay out"
- Making changes without communicating what or why
- Refusing to hand off when fatigued because "only I understand this"

Why this fails predictably:
- One person can't sustain extended incident response (burnout is real)
- When heroes fix things alone, understanding doesn't spread
- Fatigue increases error rates; fresh perspective helps
- If the hero is unavailable next time, the team starts from zero

The collaborative alternative:
- Explain your reasoning as you investigate
- Ask for input before making significant changes
- Hand off to fresh teammates when fatigued
- Document decisions so others can understand and continue

Celebrate collaborative wins, not individual heroics. Value knowledge transfer as highly as problem resolution.

## Master the Fundamentals

Troubleshooting is a discipline that applies universally, whether debugging alone or coordinating war rooms.

Reproduction is the fulcrum. Without it, you're guessing about the problem and guessing about the fix. With it, you prove understanding and validate solutions. Miss this point and you waste days searching for what you could have targeted early.

Gather facts before acting. Pressure creates the urge to do something immediately, but acting on incomplete information wastes more time than gathering facts would have taken. Test assumptions explicitly. Incidents reveal what you assumed about systems. The most dangerous assumption is dismissing recent changes as unrelated. Verify rather than trust.

Change one thing at a time. Sequential changes build understanding while simultaneous changes destroy your ability to know what worked. If multiple changes fix the problem, you can't identify which mattered. If they fail, you can't isolate what made it worse. The discipline feels slow but proves faster than reverting everything and starting over.

Fix causes, not symptoms. Understand the layers: symptom, surface cause, root cause. Dig deeper by asking why repeatedly until you see patterns in how problems emerge. Distinguish mitigation (restores service) from fixes (prevents recurrence).

In war rooms, apply the same principles with clear roles. Coordination doesn't change the fundamentals; it amplifies the importance of disciplined investigation and clear communication.

The teams that resolve incidents fastest are the ones disciplined enough to slow down and understand what they're fixing.
