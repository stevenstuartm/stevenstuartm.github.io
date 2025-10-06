---
layout: guide
title: "Data Architecture & Processing"
category: Architecture
subcategory: Data & Infrastructure
description: "Comprehensive data architecture covering database fundamentals, ACID properties, ETL pipelines, big data processing, and modern data lakehouse architectures."
---

# Data Architecture & Processing

## Table of Contents

- [Database Fundamentals](#database-fundamentals)
- [ETL (Extract, Transform, Load)](#etl-extract-transform-load)
- [Big Data Processing](#big-data-processing)
- [Modern Data Architectures](#modern-data-architectures)
- [Quick Reference](#quick-reference)

---

## Database Fundamentals

### ACID Properties

ACID properties ensure your database doesn't lose or corrupt data when multiple operations happen at once.

**Atomicity** - All or nothing. If you're transferring $100 between bank accounts, either both the deduction AND addition happen, or neither does. No money disappears into thin air.

**Consistency** - Rules are enforced. If you have a rule that inventory can't go negative, the database won't let you sell more items than you have in stock.

**Isolation** - Transactions don't interfere with each other. Two people trying to book the last airplane seat won't both succeed - one will get it, the other gets an error.

**Durability** - Once confirmed, it's permanent. When the system says your order went through, it survives even if the server crashes five minutes later.


---

## ETL (Extract, Transform, Load)

### Overview
ETL is how you get data from where it lives (your CRM, website, spreadsheets) into where you can analyze it (your data warehouse). Most companies pull from 10+ different systems, each with different formats and quirks.

### Extract - Getting the Data Out

**Full Extraction**: Copy everything every time. Simple but slow and resource-heavy. Good for small datasets or one-time migrations.

**Incremental Extraction**: Only copy what's changed since last time. Much more efficient but requires tracking changes. Most production systems use this.

**Real-world example**: Your e-commerce site might do full extraction of your small product catalog weekly, but incremental extraction of customer orders every hour.

### Transform - Making Data Useful

This is where messy real-world data becomes clean, consistent data you can actually analyze.

**Common transformations**:
- **Cleaning**: "N/A", "NULL", "", "Not Available" all become a standard null value
- **Standardization**: "M/F", "Male/Female", "1/0" all become consistent gender codes  
- **Business logic**: Raw transactions become "Customer Lifetime Value" through calculations
- **Joining**: Combine customer info from your CRM with purchase history from your e-commerce platform

**Key insight**: Transformation often takes 70% of your ETL effort. Don't underestimate it.

### Load - Putting Data Where It Belongs

**Full Load**: Replace everything in the target. Clean but can create downtime.

**Incremental Load**: Only add/update changed records. Faster and no downtime, but more complex logic.

### Major ETL Challenges

**Different data sources, different problems**: Your Salesforce API works differently than your Google Analytics export, which works differently than your accounting system's CSV files.

**Things break**: Source systems change their APIs, network connections fail, data formats shift. Plan for failures.

**Performance**: What works for 1,000 records might be painfully slow for 1 million records.


---

## Big Data Processing

### When You Need Big Data Approaches
- **Volume**: More data than fits comfortably in memory or processes in reasonable time
- **Variety**: Mix of databases, files, APIs, real-time streams
- **Velocity**: Data arrives faster than traditional batch processing can handle

### MapReduce - The Big Idea
Break big problems into smaller pieces that can run in parallel, then combine the results.

**Example - Counting Words Across 1000 Documents**:
- **Map phase**: Each server counts words in 10 documents  
- **Reduce phase**: One server adds up all the "the" counts, another adds all the "dog" counts, etc.
- **Result**: Total word counts across all documents

**Why it works**: You can throw more servers at the problem to go faster. The framework handles failures, scheduling, and coordination automatically.

### Batch vs Real-time Processing

**Batch Processing**:
- **Good for**: Historical analysis, complex calculations, cost efficiency
- **Example**: Nightly processing of the day's sales data for reporting
- **Tradeoff**: High latency but comprehensive and reliable

**Real-time Processing**:
- **Good for**: Immediate responses, monitoring, personalization
- **Example**: Fraud detection on credit card transactions
- **Tradeoff**: Low latency but limited historical context

**Lambda Architecture**: Run both batch and real-time processing, combine the results. Get comprehensive analysis AND fast responses, but double the complexity.

---

## Modern Data Architectures

### Data Warehouse vs Data Lake vs Data Lakehouse

**Data Warehouse**:
- **What**: Structured data, optimized for business reporting
- **Best for**: Executive dashboards, financial reports, regulatory compliance
- **Think**: Your company's "source of truth" for business metrics
- **Examples**: Snowflake, BigQuery, Redshift

**Data Lake**:
- **What**: Store any type of data in raw format, figure out structure later
- **Best for**: Data science, machine learning, exploratory analysis
- **Think**: A big bucket where you dump everything, organize it when needed
- **Challenge**: Can become a "data swamp" without proper organization

**Data Lakehouse**:
- **What**: Combines warehouse performance with lake flexibility
- **Best for**: Organizations that want both structured reporting AND data science
- **Think**: One system instead of maintaining separate warehouse and lake
- **Examples**: Databricks Delta Lake, Apache Iceberg

**Choosing**: Small company with clear reporting needs? Start with warehouse. Lots of unstructured data and data science? Consider lakehouse. Just getting started? Warehouse is simpler.

### Data Mesh

**Core idea**: Instead of one central data team managing everything, each business domain (Marketing, Sales, Customer Service) owns and manages their own data.

**Key principles**:
- **Domain ownership**: Marketing team owns marketing data, knows it best
- **Data as product**: Treat data like a product with customers and quality standards  
- **Self-service platform**: Provide tools so domains don't need deep technical expertise
- **Federated governance**: Common standards, but domains implement them locally

**When it works**: Large organizations with mature data teams in each business area.

**When it doesn't**: Small companies, organizations without technical expertise in business domains, or anywhere lacking strong data culture.

### Modern Data Stack (MDS)

**The pattern**: Best-of-breed cloud tools connected by APIs rather than one monolithic platform.

**Typical stack**:
1. **Ingestion**: Fivetran, Airbyte (connect to data sources)
2. **Storage**: Snowflake, BigQuery (cloud data warehouse)  
3. **Transformation**: dbt (SQL-based transformations)
4. **BI**: Looker, Tableau, PowerBI (dashboards and reports)
5. **Observability**: Monte Carlo, Great Expectations (monitor data quality)

**Benefits**: Choose the best tool for each job, avoid vendor lock-in, faster innovation.

**Challenges**: More tools to manage, integration complexity, potential security gaps.

---

## Quick Reference

### Architecture Patterns

| Architecture | Best For | Trade-off |
|--------------|----------|-----------|
| **Data Warehouse** | Business reporting, structured data | Less flexible, structured only |
| **Data Lake** | Data science, ML, exploration | Can become "data swamp" |
| **Data Lakehouse** | Both structured & unstructured | More complex |
| **Data Mesh** | Large orgs with domain expertise | Requires mature teams |

### ETL vs ELT

**ETL** (Extract, Transform, Load): Transform before loading
- **Good for**: Resource-constrained environments, complex transformations
- **Bad for**: Cloud warehouses with cheap compute

**ELT** (Extract, Load, Transform): Load raw data, transform in warehouse
- **Good for**: Cloud warehouses, flexibility, modern data stack
- **Bad for**: Limited warehouse resources

### Processing Models

**Batch Processing**:
- Scheduled intervals (hourly, daily, weekly)
- High latency, comprehensive analysis
- Lower cost, simpler

**Stream Processing**:
- Real-time as data arrives
- Low latency, immediate insights
- Higher cost, more complex

**Lambda Architecture**: Both batch and streaming (high complexity)

### Key Concepts

**ACID**: Atomicity, Consistency, Isolation, Durability - database transaction guarantees
**CDC**: Change Data Capture - track database changes in real-time
**Data Contract**: Agreement defining data quality, schema, delivery expectations
**Data Lineage**: Map of data origin, transformations, and destinations
**dbt**: Data build tool - SQL-based transformation framework
**Slowly Changing Dimensions**: Techniques for tracking historical changes

---