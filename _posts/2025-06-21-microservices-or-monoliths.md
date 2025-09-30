---
layout: post
title: "Microservices or Monoliths? (Yeah, I Know...)"
date: 2025-06-21
tags: [architecture, microservices, monoliths, system-design]
description: "Why monoliths are effective for discovery and microservices are optimizations—principles for choosing the right architecture for your context."
---

It is an old and tired topic, and yet surprisingly it is still one that even I need to contemplate when starting a new project. Firstly, let's not be reductive: there is no one solution to any technological challenge. Much like there is no one way to best manage a team or a department. Leverage the responsible solution for the challenge at hand.

## Key Principles

**Microservicing is an optimization** (a series of them actually) driven by discovery, and monolithic design is an effective way to discover what you do not yet know. For the same reason why, as an architect, I rely on developing my thoughts through a working proof of concept, so do monolithic components point the way to something potentially better.

**Monolith does not mean you get to write garbage code.** Monoliths often have a stigma that has nothing to do with architecture. Simply put, with poor leadership comes an avalanche of garbage. The same code quality of a well crafted set of SOLID services can be implemented identically in a monolith.

**Being first to market is overrated,** yet there is no need to block product development because you have not yet decided on the perfect ecosystem.

**Have well defined data boundaries from the start.** It is not wrong to share a database between microservices, but when things do need to change make sure it is not a tangled mess.

**Use those API Gateways to abstract paths and access.** This is not a must-have, but it can be a prudent step that you can take before you need to know much of anything about your targeted future infrastructure.

## My Preference

With that all said... my typical preference, if time allows, is something in between: minimal Domain services. Start developing along the naturally occurring logical or categorical boundaries.