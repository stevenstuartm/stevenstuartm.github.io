---
layout: post
title: "What Does 'Hexagonal Architecture' Actually Mean in Modern Development?"
date: 2025-09-29
tags: [architecture, design-patterns, software-design]
description: "Understanding the difference between hexagonal architecture's structural pattern and achieving testability through modern frameworks—and why it matters."
---

Most developers achieve hexagonal architecture's goals (testability, decoupling) without implementing its structure. Understanding this distinction clarifies what you're actually building.

## 1. The Confusion

**Cockburn's Goals (2005):** "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."

This sounds like what every modern framework encourages: testability, decoupling, multiple interfaces.

**Cockburn's Implementation:** Explicit symmetry treating UI and database identically as external actors. Multiple driving mechanisms as first-class equals (REST, CLI, tests, batch). Ports as distinct boundaries with swappable adapters.

**The Gap:** People achieve the goals using framework DI and think they're "doing hexagonal architecture"—but they're using standard layered patterns (Controller → Service → Repository), not the hexagonal structure.

## 2. What People Are Actually Doing

**Actual Hexagonal (Rare):** Explicit symmetry, multiple equal drivers, real adapter swapping in production.

**Layered Architecture with DI (Most Common):** Framework DI with repository interfaces. Achieves testability and decoupling through framework patterns, not hexagonal structure. Calls interfaces "ports" but still thinks in layers.

**Terminological Confusion (Common):** Using "hexagonal" as shorthand for "clean code" or any architecture with interfaces.

## 3. The Question

Modern frameworks provide built-in DI, testing support, and interface-based design. More importantly, we deploy immutable containers—entire artifacts with dependencies baked in. You don't swap adapters at runtime; you deploy new images through CI/CD pipelines.

Cross-cutting concerns that hexagonal architecture addressed through adapters (monitoring, observability, authentication, rate limiting) are now handled by service meshes and API gateways—external to your application code entirely.

The "swappable adapters" benefit that justified hexagonal structure in 2005 doesn't materialize with immutable infrastructure and externalized concerns.

When you're using framework DI, repository interfaces, and deploying containers with infrastructure managed externally—are you implementing hexagonal structure, or achieving testability and decoupling through standard modern practices?

## 4. Why It Matters

This pattern appears in courses, certifications, and job requirements. The distinction between goals and structure matters for:
- **Learning accurately** — Understanding what you're actually implementing
- **Technical interviews** — Articulating architectural decisions clearly
- **Team alignment** — Avoiding confusion when discussing patterns

**Key takeaway:** Modern frameworks achieve hexagonal architecture's original goals through different means. Unless you're explicitly implementing symmetric drivers and swappable adapters, you're likely using layered architecture with dependency injection—and that's perfectly valid for most systems.