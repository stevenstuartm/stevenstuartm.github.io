---
layout: post
title: "Microservices or Monoliths? (Yeah, I Know...)"
date: 2025-06-21
series: "Architecture Insights"
tags: [architecture, microservices, monoliths, system-design]
description: "Why monoliths are effective for discovery and microservices are optimizations—principles for choosing the right architecture for your context."
---

An old debate, yet I contemplate it with every new project. There's no universal answer—choose the architecture that fits your context, constraints, and discovery needs.

## Core Principles

**1. Microservices Are Optimizations, Monoliths Enable Discovery**

Microservices solve specific problems: team scaling, independent deployment, technology diversity. Monoliths accelerate discovery—learning boundaries, understanding domains, validating assumptions quickly.

Start with what helps you learn fastest. Optimize when you understand what needs optimizing.

**2. Monoliths Don't Excuse Poor Code Quality**

The monolith stigma stems from poor practices, not architecture. Apply SOLID principles, clear boundaries, and good design regardless of deployment strategy. Poor leadership produces garbage code in any architecture.

**3. Speed to Market vs. Perfect Architecture**

Ship and learn. Don't block product development waiting for the "perfect" architecture. Make reversible decisions, establish clear boundaries, iterate based on real usage.

**4. Data Boundaries Matter From Day One**

Define data ownership early. Sharing databases between services isn't wrong initially, but ensure clean boundaries for future separation. Tangled data models block evolution.

**5. Abstract Infrastructure Early**

API gateways and service abstractions provide flexibility before you know your final infrastructure. Small upfront investment, significant future optionality.

## My Approach

Start with **domain-based services**—modular monoliths organized along natural business boundaries (bounded contexts). This provides:
- Clear separation of concerns
- Team autonomy within domains
- Easy path to microservices when needed
- Faster initial development than distributed systems

Split into microservices when you have evidence: independent scaling needs, team coordination bottlenecks, or technology requirements that justify operational complexity.