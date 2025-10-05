---
title: "Deployment and Infrastructure Patterns"
category: Architecture
---


## Overview

These patterns address how applications are deployed, managed, and operated in distributed environments, focusing on infrastructure concerns and operational efficiency.

## Table of Contents

- [Sidecar Pattern](#sidecar-pattern)
- [Ambassador Pattern](#ambassador-pattern)
- [Backend for Frontend (BFF)](#backend-for-frontend-bff)
- [Service Mesh](#service-mesh)

---

## Sidecar Pattern

**What it is:** Deploys supporting functionality (logging, monitoring, configuration) in a separate process alongside the main application.

**Why use it:** Separates cross-cutting concerns, enables polyglot architectures, and provides consistent functionality across services.

**When to use:**
- Need consistent cross-cutting functionality
- Applications use different technologies
- Cannot modify existing applications
- Want to centralize auxiliary functions

**Common uses:**
- Service mesh proxies
- Logging and monitoring agents
- Configuration management
- Security and authentication

**Example:** Microservice with Envoy sidecar proxy that handles load balancing, circuit breaking, and observability without modifying application code.

## Ambassador Pattern

**What it is:** A specialized sidecar that handles all outbound network requests for an application, acting as a proxy.

**Why use it:** Centralizes network concerns, enables consistent policies, and simplifies application code.

**When to use:**
- Need consistent networking policies
- Want to handle retries, timeouts centrally
- Applications make many external calls
- Need to add networking features without code changes

**Example:** Legacy application with ambassador container that adds circuit breaking, retries, and service discovery to external API calls.

## Backend for Frontend (BFF)

**What it is:** Creates separate backend services tailored to specific frontend applications or client types.

**Why use it:** Optimizes APIs for different client needs, reduces client complexity, and enables independent frontend evolution.

**When to use:**
- Supporting multiple client types (web, mobile, IoT)
- Clients have different data requirements
- Want to optimize for specific user experiences
- Generic APIs are too complex or inefficient for clients

**Example:** E-commerce platform with separate BFFs for web browsers (rich product data), mobile apps (lightweight responses), and IoT devices (minimal data).

## Service Mesh

**What it is:** Infrastructure layer that handles service-to-service communication, providing observability, security, and traffic management.

**Why use it:** Centralizes networking concerns, provides consistent policies, and enables advanced traffic management without application changes.

**When to use:**
- Large number of microservices
- Need consistent security and observability
- Complex traffic management requirements
- Multiple teams developing services

**Components:**
- **Data plane:** Sidecar proxies handling traffic
- **Control plane:** Configures and manages proxies

**Example:** Kubernetes cluster with Istio service mesh providing mTLS encryption, traffic splitting for canary deployments, and distributed tracing.

---

