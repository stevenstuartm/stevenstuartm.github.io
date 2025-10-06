---
layout: guide
title: "Data Management Patterns"
category: Architecture
subcategory: Patterns
description: "Database patterns for distributed systems including database-per-service, CQRS, event sourcing, saga pattern, and handling data consistency challenges."
---

# Data Management Patterns

Data management patterns address how distributed systems handle data storage, access, and consistency across multiple services and databases.

## Database per Service

Each microservice owns its data and database, ensuring loose coupling and service autonomy.

**Use When**:
- Building microservices architecture
- Services have different data storage requirements
- Want to enable independent service evolution
- Need to prevent database-level coupling

**Challenges**:
- No ACID transactions across services
- Data consistency becomes more complex
- Reporting across services requires aggregation

**Example**: E-commerce system where user service uses SQL database, product catalog uses document database, and recommendation engine uses graph database.

```
User Service → PostgreSQL
Product Service → MongoDB
Recommendation Service → Neo4j
```

---

## Shared Database

Multiple services access the same database, sharing data directly.

**Use When**:
- Tight coupling between services is acceptable
- ACID transactions across services are required
- Migrating from monolithic applications
- Services have significant data overlap

**Drawbacks**:
- Creates tight coupling between services
- Database becomes a bottleneck
- Reduces service autonomy
- Schema changes affect multiple services

---

## Event Sourcing

Stores all changes to application state as a sequence of events rather than storing current state directly.

**Use When**:
- Need complete audit trail of all changes
- Want to replay events for testing or analytics
- Implementing complex business domains
- Building systems that benefit from temporal queries

**Considerations**:
- Event store grows continuously
- Complex queries may require rebuilding state
- Need to handle event schema evolution

**Example**: Banking system that stores all account transactions as events (deposit, withdrawal, transfer) and calculates current balance by replaying events.

```
Events: [Deposit($100), Withdrawal($30), Deposit($50)]
Current Balance = Sum of events = $120
```

---

## CQRS (Command Query Responsibility Segregation)

Separates read and write operations into different models, often with separate databases optimized for each operation type.

**Use When**:
- Read and write patterns are significantly different
- Need to scale reads and writes independently
- Complex reporting requirements
- Different consistency requirements for reads and writes

**Implementation Options**:
- Separate models, same database
- Separate databases for reads and writes
- Event sourcing for writes, projections for reads

**Example**: Social media platform with write-optimized database for posts and read-optimized database with denormalized data for feeds and searches.

```
Write: Post Service → Command DB (normalized)
Read: Feed Service → Query DB (denormalized, optimized for feeds)
Sync: Command DB → Events → Update Query DB
```

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
