---
layout: guide
title: "Migration Patterns"
category: Architecture
subcategory: Patterns
---

# Migration Patterns

Migration patterns help organizations modernize legacy systems gradually and safely, minimizing risk while maintaining business continuity during transformation.

## Strangler Fig Pattern

Gradually replaces legacy system functionality by routing traffic to new services while keeping the old system running.

**Use When**:
- Migrating large legacy systems
- Cannot replace entire system at once
- Need to maintain business continuity
- Want to reduce migration risk

**How It Works**:

1. Place facade in front of legacy system
2. Implement new functionality in new services
3. Route new requests to new services
4. Gradually migrate existing functionality
5. Remove legacy system when fully replaced

**Example**: Migrating monolithic order system by implementing new order processing service and routing new orders there while keeping legacy system for existing orders.

```
Phase 1: All traffic → Legacy System
Phase 2: Facade → {New orders → New Service, Existing orders → Legacy}
Phase 3: Facade → New Service only
Phase 4: Remove facade and legacy system
```

---

## Anti-Corruption Layer

A translation layer that isolates new systems from legacy systems by converting between different data models and protocols.

**Use When**:
- Integrating with legacy systems that cannot be changed
- Legacy and new systems have very different models
- Want to prevent legacy complexity from affecting new code

**Example**: New customer management system with anti-corruption layer that translates between modern REST/JSON APIs and legacy SOAP/XML services.

```
New System (REST/JSON) ↔ Anti-Corruption Layer ↔ Legacy System (SOAP/XML)

Anti-Corruption Layer:
  - Translates data models
  - Converts protocols
  - Validates and sanitizes data
  - Provides clean interface to new system
```

---

## Branch by Abstraction

Gradually replaces system components by creating abstraction layers and switching implementations behind the abstraction.

**Use When**:
- Replacing critical system components
- Cannot afford system downtime
- Want to test new implementation alongside old one
- Need ability to quickly rollback changes

**Example**: Replacing payment processor by creating payment abstraction, implementing new processor behind abstraction, and gradually routing traffic to new implementation.

```
Step 1: Create abstraction
  Code → PaymentAbstraction (interface)
          ├── OldProcessor (current)
          └── NewProcessor (being built)

Step 2: Route percentage of traffic
  10% → NewProcessor
  90% → OldProcessor

Step 3: Increase gradually
  50% → NewProcessor
  50% → OldProcessor

Step 4: Complete migration
  100% → NewProcessor
  Remove OldProcessor
```

---

## Quick Reference

### Pattern Comparison

| Pattern | Migration Speed | Risk | Rollback Ease |
|---------|----------------|------|---------------|
| **Strangler Fig** | Gradual | Low | Easy |
| **Anti-Corruption Layer** | N/A (integration) | Low | N/A |
| **Branch by Abstraction** | Gradual | Low | Very Easy |

### Decision Tree

**Replacing entire system?** → Strangler Fig
**Integrating with unchangeable legacy?** → Anti-Corruption Layer
**Replacing critical component?** → Branch by Abstraction

### Migration Strategies

**Strangler Fig**:
- **Pros**: Incremental, low risk, business continuity
- **Cons**: Both systems running (higher cost), longer timeline

**Anti-Corruption Layer**:
- **Pros**: Isolates complexity, clean new system
- **Cons**: Additional layer, translation overhead

**Branch by Abstraction**:
- **Pros**: Easy rollback, gradual traffic shifting, no downtime
- **Cons**: Abstraction overhead, both implementations maintained

### Best Practices

**Strangler Fig**:
1. Start with new features
2. Migrate high-value, low-risk features next
3. Save complex, tightly-coupled features for last
4. Monitor both systems during migration

**Anti-Corruption Layer**:
1. Keep layer simple and focused
2. Don't let legacy concepts leak into new system
3. Test translations thoroughly
4. Plan for eventual removal

**Branch by Abstraction**:
1. Start with small traffic percentage
2. Monitor metrics closely
3. Have clear rollback criteria
4. Remove old implementation promptly after success

---
