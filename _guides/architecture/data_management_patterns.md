---
title: "Data Management Patterns"
category: Architecture
---


## Overview

Data management patterns address how distributed systems handle data storage, access, and consistency across multiple services and databases.

## Table of Contents

- [Database per Service](#database-per-service)
- [Shared Database](#shared-database)
- [Event Sourcing](#event-sourcing)
- [CQRS (Command Query Responsibility Segregation)](#cqrs-command-query-responsibility-segregation)
- [Materialized View](#materialized-view)

---

## Database per Service

**What it is:** Each microservice owns its data and database, ensuring loose coupling and service autonomy.

**Why use it:** Enables independent service development, allows optimal database selection per service, and prevents tight coupling through shared data.

**When to use:**
- Building microservices architecture
- Services have different data storage requirements
- Want to enable independent service evolution
- Need to prevent database-level coupling

**Challenges:**
- No ACID transactions across services
- Data consistency becomes more complex
- Reporting across services requires aggregation

**Example:** E-commerce system where user service uses SQL database, product catalog uses document database, and recommendation engine uses graph database.

## Shared Database

**What it is:** Multiple services access the same database, sharing data directly.

**Why use it:** Simplifies data consistency, enables ACID transactions, and reduces data duplication.

**When to use:**
- Tight coupling between services is acceptable
- ACID transactions across services are required
- Migrating from monolithic applications
- Services have significant data overlap

**Drawbacks:**
- Creates tight coupling between services
- Database becomes a bottleneck
- Reduces service autonomy
- Schema changes affect multiple services

## Event Sourcing

**What it is:** Stores all changes to application state as a sequence of events rather than storing current state directly.

**Why use it:** Provides complete audit trail, enables temporal queries, and supports event replay for debugging or analytics.

**When to use:**
- Need complete audit trail of all changes
- Want to replay events for testing or analytics
- Implementing complex business domains
- Building systems that benefit from temporal queries

**Considerations:**
- Event store grows continuously
- Complex queries may require rebuilding state
- Need to handle event schema evolution

**Example:** Banking system that stores all account transactions as events (deposit, withdrawal, transfer) and calculates current balance by replaying events.

## CQRS (Command Query Responsibility Segregation)

**What it is:** Separates read and write operations into different models, often with separate databases optimized for each operation type.

**Why use it:** Optimizes read and write operations independently, enables different scaling strategies, and supports complex read requirements.

**When to use:**
- Read and write patterns are significantly different
- Need to scale reads and writes independently
- Complex reporting requirements
- Different consistency requirements for reads and writes

**Implementation options:**
- Separate models, same database
- Separate databases for reads and writes
- Event sourcing for writes, projections for reads

**Example:** Social media platform with write-optimized database for posts and read-optimized database with denormalized data for feeds and searches.

## Materialized View

**What it is:** Pre-computed and stored query results that are periodically updated, optimizing read performance for complex queries.

**Why use it:** Improves query performance, reduces computational load during reads, and enables complex aggregations.

**When to use:**
- Complex queries are expensive to compute
- Query results don't need to be real-time
- Read-heavy workloads with predictable query patterns

**Trade-offs:**
- Data freshness vs. performance
- Storage space for additional views
- Complexity of keeping views updated

**Example:** E-commerce analytics dashboard showing daily sales summaries, computed overnight and stored for fast display during business hours.

---

