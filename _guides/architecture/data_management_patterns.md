---
layout: guide
title: "Data Management Patterns"
category: Architecture
subcategory: Patterns
description: "Database patterns for distributed systems including database-per-service, CQRS, event sourcing, saga pattern, and handling data consistency challenges."
tags: [architecture, design-patterns, databases, distributed-systems, microservices, consistency]
---

Data management patterns address how distributed systems handle data storage, access, and consistency across multiple services and databases.

## Database per Service

Each microservice owns its data and database, ensuring loose coupling and service autonomy.

**Use When**:
- Building microservices architecture
- Services have different data storage requirements
- Want to enable independent service evolution
- Need to prevent database-level coupling

<div class="callout callout--warning">
<p class="callout__title">Database per Service Challenges</p>
<ul>
<li>No ACID transactions across services</li>
<li>Data consistency becomes more complex</li>
<li>Reporting across services requires aggregation</li>
</ul>
</div>

**Example**: E-commerce system where user service uses SQL database, product catalog uses document database, and recommendation engine uses graph database.

```
User Service → PostgreSQL
Product Service → MongoDB
Recommendation Service → Neo4j
```

---

## Shared Database

<div class="comparison">
<div class="content-card content-card--accent">
<h4>When to Use Shared Database</h4>
<ul>
<li>Tight coupling between services is acceptable</li>
<li>ACID transactions across services are required</li>
<li>Migrating from monolithic applications</li>
<li>Services have significant data overlap</li>
</ul>
</div>
<div class="content-card content-card--accent-secondary">
<h4>Drawbacks of Shared Database</h4>
<ul>
<li>Creates tight coupling between services</li>
<li>Database becomes a bottleneck</li>
<li>Reduces service autonomy</li>
<li>Schema changes affect multiple services</li>
</ul>
</div>
</div>

---

## Event Sourcing

*Pattern popularized by Martin Fowler and Greg Young in early 2000s*

Stores all changes to application state as an immutable sequence of events rather than storing only current state. The current state is derived by replaying events from the beginning.

<blockquote class="pull-quote">
<p>Event sourcing maintains a complete audit trail of all changes, allowing you to replay events for testing, analytics, or answering temporal queries like "what was the state at time X?"</p>
</blockquote>

**Use When**:
- Need complete audit trail of all changes
- Want to replay events for testing or analytics
- Implementing complex business domains (especially with Domain-Driven Design)
- Building systems that benefit from temporal queries

<div class="callout callout--warning">
<p class="callout__title">Event Sourcing Considerations</p>
<ul>
<li>Event store grows continuously (implement snapshotting for performance)</li>
<li>Complex queries may require rebuilding state from events</li>
<li>Need to handle event schema evolution carefully</li>
<li>Deleting data is complex (GDPR compliance requires special handling)</li>
</ul>
</div>

**Example**: Banking system that stores all account transactions as events (deposit, withdrawal, transfer) and calculates current balance by replaying events.

```
Events: [Deposit($100), Withdrawal($30), Deposit($50)]
Current Balance = Sum of events = $120
Can also query: "What was balance on March 1st?" by replaying events up to that date
```

---

## CQRS (Command Query Responsibility Segregation)

*Pattern introduced by Greg Young (2010), based on Bertrand Meyer's Command-Query Separation principle (1988)*

Separates read (query) and write (command) operations into different models, often with separate databases optimized for each operation type. Goes beyond CQS by using separate data models, not just separate methods.

**Use When**:
- Read and write patterns are significantly different
- Need to scale reads and writes independently
- Complex reporting requirements
- Different consistency requirements for reads and writes
- Working with Event Sourcing (natural fit)

<div class="callout callout--note">
<p class="callout__title">CQRS Implementation Options</p>
<p><strong>Simple</strong>: Separate models, same database</p>
<p><strong>Advanced</strong>: Separate databases for reads and writes</p>
<p><strong>Full</strong>: Event sourcing for writes, materialized projections for reads</p>
</div>

**Example**: Social media platform with write-optimized database for posts and read-optimized database with denormalized data for feeds and searches.

```
Write: Post Service → Command DB (normalized)
Read: Feed Service → Query DB (denormalized, optimized for feeds)
Sync: Command DB → Events → Update Query DB
```

<div class="callout callout--warning">
<p class="callout__title">Warning</p>
<p>CQRS adds complexity. Don't use unless you have a specific problem it solves.</p>
</div>

---

## Materialized View

Pre-computed and stored query results that are periodically updated, optimizing read performance for complex queries.

**Use When**:
- Complex queries are expensive to compute
- Query results don't need to be real-time
- Read-heavy workloads with predictable query patterns

**Trade-offs**:
- Data freshness vs. performance
- Storage space for additional views
- Complexity of keeping views updated

**Example**: E-commerce analytics dashboard showing daily sales summaries, computed overnight and stored for fast display during business hours.

```
Nightly Job: Compute sales by category, region, time period → Store in materialized view
Dashboard: SELECT * FROM daily_sales_summary WHERE date = today
```

---

## Quick Reference

### Pattern Comparison

| Pattern | Data Distribution | Consistency | Complexity | Use Case |
|---------|------------------|-------------|------------|----------|
| **Database per Service** | Isolated | Eventual | High | Microservices independence |
| **Shared Database** | Shared | Strong | Low | Monolith or tight coupling OK |
| **Event Sourcing** | Event log | Eventual | High | Audit trail, event replay |
| **CQRS** | Separate read/write | Varies | Medium-High | Different read/write patterns |
| **Materialized View** | Cached | Stale | Low | Expensive query optimization |

### Decision Tree

**Independent services?** → Database per Service
**Need ACID across services?** → Shared Database (consider monolith instead)
**Need full audit trail?** → Event Sourcing
**Different read/write patterns?** → CQRS
**Expensive queries?** → Materialized View

### Consistency Trade-offs

**Strong Consistency**: Shared Database | CQRS (same DB)
**Eventual Consistency**: Database per Service | Event Sourcing | CQRS (separate DBs)
**Stale Data OK**: Materialized View

---
