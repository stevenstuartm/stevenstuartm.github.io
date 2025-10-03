---
title: "Migration Patterns"
category: Architecture
---

← [Back to Architecture Patterns Index](./README.md)

## Overview

Migration patterns help organizations modernize legacy systems gradually and safely, minimizing risk while maintaining business continuity during transformation.

## Table of Contents

- [Strangler Fig Pattern](#strangler-fig-pattern)
- [Anti-Corruption Layer](#anti-corruption-layer)
- [Branch by Abstraction](#branch-by-abstraction)

---

## Strangler Fig Pattern

**What it is:** Gradually replaces legacy system functionality by routing traffic to new services while keeping the old system running.

**Why use it:** Enables incremental migration, reduces risk, and maintains system availability during modernization.

**When to use:**
- Migrating large legacy systems
- Cannot replace entire system at once
- Need to maintain business continuity
- Want to reduce migration risk

**How it works:**
1. Place facade in front of legacy system
2. Implement new functionality in new services
3. Route new requests to new services
4. Gradually migrate existing functionality
5. Remove legacy system when fully replaced

**Example:** Migrating monolithic order system by implementing new order processing service and routing new orders there while keeping legacy system for existing orders.

## Anti-Corruption Layer

**What it is:** A translation layer that isolates new systems from legacy systems by converting between different data models and protocols.

**Why use it:** Prevents legacy system complexity from spreading, enables clean architecture in new systems, and provides controlled integration.

**When to use:**
- Integrating with legacy systems that cannot be changed
- Legacy and new systems have very different models
- Want to prevent legacy complexity from affecting new code

**Example:** New customer management system with anti-corruption layer that translates between modern REST/JSON APIs and legacy SOAP/XML services.

## Branch by Abstraction

**What it is:** Gradually replaces system components by creating abstraction layers and switching implementations behind the abstraction.

**Why use it:** Enables safe incremental changes, maintains system functionality during migration, and allows easy rollback.

**When to use:**
- Replacing critical system components
- Cannot afford system downtime
- Want to test new implementation alongside old one
- Need ability to quickly rollback changes

**Example:** Replacing payment processor by creating payment abstraction, implementing new processor behind abstraction, and gradually routing traffic to new implementation.

---

← [Back to Architecture Patterns Index](./README.md)