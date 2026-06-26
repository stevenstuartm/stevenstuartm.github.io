---
layout: post
title: "Choreography Distributes Execution, Not Authority"
date: 2026-06-26
description: "Choreography looks like it respects authority because each service handles its own domain correctly. But the business transaction itself has no owner, and distributed execution doesn't make that any less a problem."
tags: [architecture, system-design, distributed-systems, design-patterns, ddd]
---

The appeal of choreography is structural, not aesthetic. Each service owns its domain and handles its own events. No service reaches into another's data. Deployment is independent. Coupling is loose. Everything looks correct at the service level, and when you examine each individual component, you won't find an obvious violation.

But when a customer places an order, who owns that?

Not OrderService; it owns order state. Not InventoryService; it owns stock reservation. Not PaymentService; it owns payment capture. In choreography, the checkout process exists only as an emergent property of event flows across those services. No component holds authority over the process itself. The business transaction is concrete and has real consequences, but it has no owner, and distributed execution doesn't make it less concrete; it just makes the missing authority harder to see.

## What Looks Like Authority Distribution

Each domain service in a choreographed system correctly holds authority over its concern. OrderService can only change order state through its own aggregate root. InventoryService does the same. The local authority claims are sound. This is what makes the pattern so easy to accept before you've seen it fail: when you examine each component, you find authority correctly placed. The problem isn't visible at the component level.

Tracing through a full business transaction reveals it. Consider placing an order: OrderService accepts and reserves the order, InventoryService reserves the stock, PaymentService captures payment. Each step fires an event; each service reacts to events fired by others. But if payment capture fails and the saga needs to compensate, the question of who decides to compensate and who is responsible for the final state of the transaction has no clear answer. The process is nobody's responsibility because nobody owns it.

This isn't a failure of individual services. It's a failure to recognize that the business transaction is itself a thing that needs an authority.

## The Command Parallel

CQRS commands make this structural role visible in a different context. A `PlaceOrder` command takes many possible originating paths, a button click, an API call, an admin action, and collapses them into a single named, bounded concept. The command is not domain data and it doesn't hold business state. Its job is to protect the contour of an intention: to say that these paths all converge on one named act with one authority over it. Without the command, each originating path becomes its own implicit authority and they drift.

The saga orchestrator does the same thing for a process. It doesn't own orders, inventory, or payments. It owns `PlaceOrder` as a process: the sequence, the failure states, the compensation decisions. It names something that choreography leaves implicit. And because it names it, the process has an authority that can be audited, examined, and tested.

The structural move is identical in both cases: create a named boundary around something that would otherwise be emergent behavior with no owner.

## Naming Is an Authority Claim

When a component owns something, you can name what it owns. OrderService owns order lifecycle. PaymentService owns payment capture. In choreography, you cannot name who owns the checkout process, because the answer is nobody. The process has no contour; there is no component whose behavioral coherence includes "place an order end to end."

This is the test. If you cannot name the authority over a concept, the authority is missing. The concept might still exist, as a choreographed process demonstrably does, but existing without an authority is precisely the condition that produces drift. The process shape is implicit in event and reaction pairs, and when those pairs change across services, the process shape changes with them, silently, without any owner to notice.

Choreography makes this invisible during construction. The costs arrive under change pressure or failure: a process step needs to change and you don't know what events are being consumed where; a compensation fails and you need to reconstruct the saga state by correlating events across services; a new requirement needs to sit between two existing steps and coordinating the event contracts across service teams takes months.

## Orchestration as the Default

Orchestration's correctness isn't that it produces better components; it's that it names the process. You can point to something and say: this is the authority over this business transaction. The consequence of the process failing to reach a compensation has a clear owner. When the saga is in an unknown state, there is one place to look. When the process needs to change, there is one place to change it.

Choreography's correctness requires demonstrating that process ownership doesn't matter, which means demonstrating that the consequences of losing saga state under failure are acceptable. That is a high bar, and most systems can't meet it honestly. At very large scale, a central orchestrator can itself become a bottleneck severe enough that the trade is worth making, but that trade should be made explicitly and deliberately, not chosen by default because choreography felt like cleaner architecture.

The burden of proof belongs on choreography. Orchestration is the safe default because it preserves something choreography does not: a named authority over the process itself.
