---
layout: post
title: "Don't Share Code, Share Values"
date: 2026-01-06
description: "Shared libraries promise reuse and consistency but deliver coupling and coordination overhead. The time saved by not writing code is dwarfed by version conflicts, blocked teams, and governance theater. If you think you need a shared library, you've probably misidentified the actual problem."
series: "Architecture Insights"
tags: [architecture, distributed-systems, microservices, governance]
---

This is a highly opinionated take on shared libraries when used for and by internal systems. After seeing costs explode for trivial tasks and critical production updates failing to deliver on time in nearly every organization I have witnessed, I am willing to take an extreme stance on the subject.

## Shared Libraries Violate Core Principles

Distributing components isn't just about distributing work. It's about the Single Responsibility Principle applied at the system level: clear ownership, implementation isolation, and infrastructural independence. These benefits are often implicit in the decision to distribute, but they're the whole point. The share-nothing principle makes this explicit. Services should be autonomous, independently deployable, and free from implementation coupling. When services share nothing, teams can deploy, scale, and evolve independently. The Open/Closed Principle reinforces this at the code level. Code should be open for extension but closed for modification, allowing new behavior without risking breakage to existing consumers.

Shared libraries violate these principles. They create little monoliths: siblings cast from the same mold, coupled through shared implementation despite being distributed in name.

Yet the pitch keeps coming: "We have this code in three places. Let's consolidate it into a shared library. We'll save time, ensure consistency, and make everyone's life easier." It sounds reasonable, yet it ignores decades of architectural pain and lessons learned. The decision only calculates the cost of duplication while ignoring the cost of sharing across teams, domains, and technical boundaries.

Before we dive into why shared libraries are so detrimental, let's use the next two sections to define the scope of what we mean by shared libraries and when they are okay and when they are not.

## Don't Reinvent the Wheel vs. Don't Share Internal Types

There's a meaningful distinction between using established external libraries and sharing internal abstractions.

Using mature, well-tested libraries for universal problems makes sense. Logging frameworks, HTTP clients, serialization libraries, and authentication middleware exist because these problems are universal and well-understood. Someone else solved them better than you would, and the cost of depending on their solution is low because the solution is stable.

Sharing your internal `CustomerDto` across services is different. Sharing your "standard" repository pattern is different. Sharing your domain models between bounded contexts is different. These aren't universal problems with stable solutions. They're your internal abstractions, and forcing them on other teams assumes those teams should think the same way you do.

The distinction matters: external libraries abstract universal problems. Internal shared libraries impose your specific mental model on teams that might have legitimately different needs.

## SDKs Are Different

There's an important distinction between shared libraries and SDKs.

An SDK abstracts what you expose: the public contract of a service or platform. It exists because external consumers shouldn't need to construct HTTP requests, handle auth tokens, or parse response formats. The SDK serves the consumer by making your service easier to use correctly.

An SDK also has a different lifecycle. The platform and its features are built first; the SDK comes into being afterward, at the proper time and in the proper manner for a different audience. Even when the SDK is your primary product, it's still an abstraction of external ingress points and external representations. The SDK's development and release cycles are separate from the internal teams building features, because the dynamics between customer and development team are different from the dynamics between internal teams.

A shared library abstracts how you think internally: your domain models, your patterns, your "standard way" of doing things. It exists because someone decided other teams should think the same way. The shared library serves a governance impulse, not the consumer. And unlike an SDK, it tries to couple internal teams to the same release cycle and the same implementation decisions.

The SDK says: "Here's how to use our thing."
The shared library says: "Here's how you should build your thing."

One is a service to consumers. The other is an imposition on autonomous teams disguised as help.

## Your Runtime Already Solved This

The shared library pitch often targets "utility code" that your runtime already provides. If you're using .NET, the framework gives you HTTP clients, JSON serialization, logging abstractions, dependency injection, and configuration management. Why would you need an internal shared library wrapping `HttpClient` when `HttpClient` exists and is battle-tested by millions of applications?

The urge to share usually targets exactly this kind of code: wrappers, helpers, and utilities that add a thin layer over framework primitives. But the framework primitives are already shared. They're already tested. They're already documented. Your wrapper just adds coordination overhead on top of something that didn't need wrapping.

This varies by ecosystem. Python's dependency management is notoriously painful, and shared internal libraries compound the problem. You're coordinating versions across teams in an ecosystem that already struggles with version conflicts. The runtime that makes sharing easiest is often the one where sharing is least necessary.

## The Costs Nobody Calculates

When someone proposes a shared library, they calculate the savings: "This code exists in five services. If we consolidate, we only maintain it once."

What they don't calculate:

**Version conflicts and upgrade pain.** Five teams now depend on your library. They release on different cadences. One team needs a breaking change. Now you're either maintaining multiple versions indefinitely or forcing upgrades on teams that have other priorities. The "one place to maintain" becomes "one place that blocks everyone."

**Teams blocked waiting for changes.** A team needs functionality the library doesn't have. They can't just add it. They need to coordinate with the library owners, get the change approved, wait for a release, and then upgrade. What would have been a two-hour change becomes a two-week dependency chain.

**Debugging across boundaries.** When something breaks, the investigation now spans your code and the library code. Your team doesn't own the library. Maybe they don't fully understand it. The abstraction that was supposed to simplify their lives has added a layer they have to dig through.

**Evolution toward bloat.** The library starts focused. Then another team needs something slightly different. Then another. The library accumulates features to serve multiple masters. It becomes a grab-bag of loosely related functionality, coupled together because they share a package, not because they belong together.

## The Testing Burden Doesn't Shrink

Sharing code doesn't reduce your testing burden.

You still need load testing, chaos testing, penetration testing, and UAT. The fact that two services use the same HTTP client implementation doesn't mean you can skip validating either service's behavior under load.

If two teams copy-pasted the same code, they'd both still test their systems. The testing happens regardless. The only thing the shared library added was coordination overhead on top of the testing you were always going to do.

The "efficiency" of shared code is an illusion that ignores where the actual costs lie.

## The Cohesion and Coupling Diagnosis

If two services genuinely need the same function, you have three possibilities:

**It's a cohesion problem.** That function belongs in one place and should be called, not duplicated. Extract it into a service with an API. Now there's a clear owner, a clear contract, and no shared implementation coupling consumers together.

**It's a coupling problem.** You've drawn your boundaries wrong. The services that "need" the same code are actually more related than you thought. Reconsider where the boundary belongs rather than papering over the boundary violation with a shared dependency.

**It's genuinely independent.** The similarity is coincidental. Both services need to format dates or parse JSON or validate email addresses. Copy the code. Move on. The duplication costs less than the coordination, and the implementations can evolve independently as each service's needs diverge.

A shared library is almost never the right answer because it solves a problem that doesn't exist (duplicated code) while creating problems that do (coupling, versioning, blocked teams).

## No Architecture Style Wants This

The shared library pitch assumes that code reuse across boundaries is inherently valuable. But examine any coherent architectural paradigm and the opposite becomes clear:

**Layered architecture** separates concerns into distinct layers. Sharing code across layers violates the separation you created them for. If your presentation layer and your data layer share a library, you've coupled what you explicitly designed to be independent.

**Domain-driven architecture** creates autonomous domains with clear boundaries. Shared libraries create exactly the coupling you architected to avoid. If Domain A and Domain B share implementation code, they're not really autonomous. They're a distributed monolith with extra steps.

**Functional/technical architecture** defines components accessed through explicit interfaces. If you need a shared package to reuse behavior, your component boundaries are wrong. The behavior should live in a component that others call, not in a library that everyone imports.

Every architectural style has a theory about where boundaries belong and why. Shared libraries violate those boundaries. If your architecture says "these things are separate" and your dependency graph says "actually they share this code," one of them is wrong.

## The Governance Theater Problem

Shared libraries often emerge from a governance impulse: "Teams are doing things inconsistently. We need to standardize."

The instinct isn't wrong, and consistency matters. But shared libraries are governance theater. They create the appearance of consistency without addressing the underlying problem.

If teams are building things inconsistently, the question is why. Usually it's because they don't share the same understanding of what matters, what the tradeoffs are, and what "good" looks like. That's an alignment problem. It requires conversation, documentation, and shared values.

Forcing everyone to use the same library doesn't create alignment. It creates compliance. Teams will use your library and still build inconsistent systems because the library doesn't encode the thinking and testing.

Governance through values: "Here's why we authenticate this way, here are the tradeoffs, here's what we're optimizing for. Align your implementation to these principles."

Governance through code: "Use this library or you're non-compliant."

The first creates alignment while preserving autonomy. Teams understand the principles and can make good decisions in novel situations. The second creates coupling while providing the illusion of alignment. Teams comply without understanding, and the moment they hit a situation the library doesn't cover, they're lost.

## The Exception: Security Protocols

There's one domain where shared libraries make sense. Shared libraries can work for security protocols like ingress handling, service-to-service authentication, and encryption standards.

Why security is different:

- **The domain is stable and well-understood.** Authentication patterns don't change week to week. The library doesn't need constant evolution to serve its consumers.
- **The cost of getting it wrong is catastrophic.** Security isn't a place for teams to make independent decisions and learn from mistakes. The blast radius is too large.
- **The surface area is thin and focused.** A good security library does one thing. It's not a grab-bag of utilities that grows to serve multiple purposes.
- **Autonomy isn't the goal.** You actually want teams to do security the same way. The coupling is a feature, not a bug.

Even here, the library should be as minimal as possible. Provide the security primitive and get out of the way. The moment it starts accumulating "helpful" utilities beyond its core purpose, it's sliding toward the problems that plague other shared libraries.

## What to Do Instead

When you feel the urge to create a shared library, pause and diagnose the actual problem:

**If it's a capability multiple services need:** Build a service, not a library. Expose an API. Now there's clear ownership, independent deployment, and consumers that can't get version-locked.

**If it's a pattern you want to standardize:** Write documentation. Explain the principles, the tradeoffs, and the reasoning. Let teams implement the pattern in their own codebases. They'll understand it better than if they'd just imported your abstraction.

**If it's truly just duplicated code:** Let it be duplicated. The coordination cost of sharing exceeds the maintenance cost of duplication. And the duplicates can evolve independently as needs diverge.

**If it's a security primitive:** Fine. Build the library. Keep it minimal, stable, and focused. Recognize it's a necessary evil, not a model to emulate.

The shared library is a solution to a problem that rarely exists in the form people imagine. Code duplication isn't what slows teams down. Building the wrong thing is the real enemy. Obsessing over shared code compliance and version alignment diverts attention from what matters: sharing quality and development values, and keeping each domain focused on its specific goals.

Don't share code. Share values.
