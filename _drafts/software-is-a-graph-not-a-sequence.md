---
layout: post
title: "AI in Practice: Software Is a Graph"
date: 
description: "Why relationship-oriented design produces better AI-assisted code, and what this reveals about the nature of software itself."
series: "AI in Practice"
tags: [ai, architecture, design-patterns, oop]
---

I've been experimenting with how different framings affect AI-generated output, and a pattern emerged that I didn't expect. The prompts that produce the best code barely mention code at all. When I describe actors and relationships—"the scheduler notifies workers when jobs are available"—the code comes out cleaner, more coherent, and requires fewer iterations. When I specify technical details—function signatures, data structures, specific patterns to use—the results are messier, full of subtle misalignments between what I asked for and what I actually needed.

The less I talk about code, the better the code becomes.

## The Native Language of Models

Language models learned from human communication. Requirements discussions, architecture documents, design explanations, technical conversations. Humans naturally communicate through actors and relationships. We say "the user requests something from the service, which checks with the database" because that's how we think about systems.

Technical specifications are translations of this natural understanding into implementation details. When you give a model the translation instead of the original, you're asking it to work backwards—to infer the relationships from the technical choices, then generate code that serves those inferred relationships.

Sometimes it guesses wrong.

Actor-relationship framing skips the translation step entirely. The model receives the same information an architect would give a senior developer: here's what exists, here's how it relates, make it work. The technical decisions emerge from understanding rather than compliance.

## Why Typed Languages Fly While Dynamic Languages Struggle

The pattern extends beyond prompting into the code itself. AI navigates .NET codebases with remarkable fluency. It traces dependencies, understands contracts, refactors confidently. The same model struggles with equivalent JavaScript—hesitating, making incorrect assumptions about what calls what, losing track of relationships that exist only at runtime.

The difference is information density.

In .NET, when you write `IOrderService` depending on `IInventoryRepository`, that relationship is explicit and discoverable. The compiler enforces it. The model can read it directly from the artifacts. The codebase is a graph of typed relationships, and the model can traverse that graph.

JavaScript lacks this. Relationships exist implicitly—through runtime behavior, naming conventions, or patterns that have to be recognized rather than read. The model reconstructs a map that was never drawn, inferring structure from clues rather than reading it from declarations.

This isn't a critique of JavaScript. It's an observation about what makes AI effective: explicit relationships encoded in the medium itself.

## Creating Anchors Where None Exist

When the medium lacks explicit relationships, you can create them yourself.

Consider CSS. Raw styling has no semantic structure—just properties applied to selectors. But if you name classes to reflect identity and purpose—`.order-summary`, `.inventory-alert`, `.user-action-primary`—you've created a relationship vocabulary before any implementation exists. The model now has named concepts to work with. It can reason about "the order summary displays the total" because both concepts have stable identifiers.

This is what TypeScript does for JavaScript. What interfaces do for implementations. What domain-driven design does for business logic. You're not adding ceremony—you're encoding relationships that would otherwise exist only in your head.

The abstraction layer isn't overhead. It's information.

## The Scripting Objection

Someone who writes bash or PowerShell daily might find this thesis unconvincing. Scripts are sequences of commands—about as far from object-oriented design as code gets—and AI handles them reasonably well.

But look closer at what's actually happening.

When you write a script, the relationships exist *outside the script itself*. The filesystem has structure. Processes have names and dependencies. Pipes connect producers to consumers. Environment variables carry context. The operating system is a graph of relationships, and the script is choreography over that existing graph.

The script doesn't define the relationships—it navigates them. When AI helps write a bash script, it draws on its understanding of those external relationships: how files relate to directories, how processes relate to streams, how commands relate to their inputs and outputs. The script works because the map already exists in the OS.

This reinforces the point rather than refuting it. The relationships are always there. The question is whether you make them explicit in your artifacts or rely on them existing somewhere else—in the runtime, in the operating system, in your head, in tribal knowledge that evaporates when the original author leaves.

The developer who sees relationships everywhere—even in a "simple" script—writes different code than the one who sees only operations. They name things to reflect identity. They structure commands to reveal dependencies. They build scripts that others can read as a map of what's happening rather than a sequence to execute blindly.

Seeing the graph doesn't change what the computer does. It changes what humans and AI can understand about what the computer does. And that understanding is what makes systems maintainable across time and across people.

## The Functional Paradox

Functional programming optimizes for human reasoning about isolated pieces. Stateless functions, pure transformations, immutability—these patterns help developers understand code without holding the whole system in memory. If a function has no side effects and depends only on its inputs, you can reason about it in isolation.

But AI doesn't share this constraint. Models can hold vast context simultaneously. What they struggle with is implicit relationships—the very thing functional decomposition deliberately obscures.

SOLID principles and object-oriented design encode relationships explicitly. When you see `OrderProcessor` depending on `IPaymentGateway` and `IInventoryService`, the model immediately understands who the actors are, what responsibilities belong where, and how changes propagate. Functional code often scatters this across dozens of pure functions where the relationships exist only in the call graph—a graph that must be reconstructed rather than read.

The patterns that felt like ceremony to humans turn out to be rich semantic information for models.

## The Business Analyst Advantage

It has long been standard practice to start projects by defining actors and assigning them to relationships—to systems, components, or other actors. Context diagrams, use cases, domain models. We do this to gain alignment before building anything.

Why would an AI need anything less than a human consultant needs in the first meeting with a stakeholder?

Start with the actors, the containers, the relationships. This is especially true if you know little about software. Which raises an interesting possibility: someone skilled in communication and business analysis might outperform a career software developer at AI-assisted development. Not because they understand code better, but because they understand *alignment* better. They know how to define what exists and how it relates before anyone writes a line of code.

AI isn't quite there yet, but we're getting close at an astounding rate.

I've been a developer for fifteen years, and the results improve dramatically when I stop being code-oriented. The instinct to specify technical details—function signatures, data structures, implementation patterns—actively works against me. The machine handles that part better than I do. What it needs from me is clarity about actors and relationships.

You can't out-code a machine. So why try?

I've written before about how the bottleneck has shifted from technical execution to business judgment. This is the practical implication: use the tool the same way, using the same principles we've always known we ought to use but were too busy to follow. The discovery work, the domain modeling, the stakeholder alignment—these were always supposed to come first. We just skipped them under deadline pressure and went straight to code. Now the code writes itself, and the bottleneck is exactly where it should have been all along: understanding what we're building and why.

## The Tech Debt Misconception

A common criticism: AI generates so much tech debt that any productivity gains are illusory. You move fast now, pay later.

But this argument assumes good direction producing sloppy output. The real dynamic is often reversed: poor direction producing exactly what was asked for, which happens to be unmaintainable.

When you prompt with technical specifications divorced from context—"create a function that takes these parameters and returns this shape"—you get fragmented code that does precisely that thing in isolation. No understanding of where it fits. No coherent relationship to adjacent components. No architectural intent. The AI delivered what you specified, and what you specified was a sequence of operations with no map.

When you prompt with actors and relationships—"the order processor validates inventory before confirming with payment"—the AI produces code that reflects that structure. The dependencies make sense. The boundaries are coherent. The code is maintainable because it was generated from a maintainable mental model.

The tech debt isn't coming from the AI. It's coming from prompts that encode sequences instead of graphs. The developer who complains about AI-generated spaghetti is often the same developer who would have written tangled code themselves, just slower.

Relationship-oriented prompting doesn't just produce faster results. It produces *better* results. The same principles that make code maintainable by humans—clear boundaries, explicit dependencies, named concepts—are exactly what makes AI generate maintainable code in the first place.

## The Compounding Advantage

Developers who embrace relationship-oriented design get compounding returns from AI assistance:

- **Better generation** because relationships are explicit in prompts
- **Better navigation** because the codebase encodes its own structure
- **Better refactoring** because the model can trace impacts through declared dependencies
- **Better maintenance** because contracts are clear to both humans and machines

Those who resist explicit relationships—preferring minimal ceremony, implicit contracts, runtime flexibility—optimize against their own leverage. Every relationship that exists only in the developer's head is a relationship the AI cannot see.

## The Underlying Truth

Software is a graph of relationships, not a sequence of operations.

The developers who internalized this—through object-oriented design, through domain modeling, through architecture patterns—built systems that encode what things are and how they relate. The ones who resisted built systems that encode what happens and in what order.

AI understands graphs. It struggles with sequences that imply graphs without drawing them.

The old lessons about modeling domains, defining contracts, and separating concerns weren't just about managing complexity for human minds. They were about capturing the true nature of software in the artifacts themselves. The type system, the interfaces, the dependency declarations—these aren't bureaucratic overhead. They're the map.

And now we have tools that can read that map, if we bother to draw it.
