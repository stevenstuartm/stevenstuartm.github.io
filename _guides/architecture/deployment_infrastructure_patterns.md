---
layout: guide
title: "Deployment and Infrastructure Patterns"
category: Architecture
subcategory: Patterns
description: "Infrastructure patterns including sidecar, ambassador, anti-corruption layer, blue-green deployment, and canary releases for robust deployment strategies."
---

# Deployment and Infrastructure Patterns

These patterns address how applications are deployed, managed, and operated in distributed environments, focusing on infrastructure concerns and operational efficiency.

## Sidecar Pattern

Deploys supporting functionality (logging, monitoring, configuration) in a separate process alongside the main application.

**Use When**:
- Need consistent cross-cutting functionality
- Applications use different technologies
- Cannot modify existing applications
- Want to centralize auxiliary functions

**Common Uses**:

- Service mesh proxies
- Logging and monitoring agents
- Configuration management
- Security and authentication

**Example**: Microservice with Envoy sidecar proxy that handles load balancing, circuit breaking, and observability without modifying application code.

```
Pod:
  ├── Application Container (business logic)
  └── Envoy Sidecar (networking, observability, security)

All network traffic goes through Envoy sidecar
```

---

## Ambassador Pattern

A specialized sidecar that handles all outbound network requests for an application, acting as a proxy.

**Use When**:
- Need consistent networking policies
- Want to handle retries, timeouts centrally
- Applications make many external calls
- Need to add networking features without code changes

**Example**: Legacy application with ambassador container that adds circuit breaking, retries, and service discovery to external API calls.

```
Application → Ambassador → External Services
  Ambassador handles:
    - Service discovery
    - Retries
    - Circuit breaking
    - TLS termination
```

---

## Backend for Frontend (BFF)

Creates separate backend services tailored to specific frontend applications or client types.

**Use When**:
- Supporting multiple client types (web, mobile, IoT)
- Clients have different data requirements
- Want to optimize for specific user experiences
- Generic APIs are too complex or inefficient for clients

**Example**: E-commerce platform with separate BFFs for web browsers (rich product data), mobile apps (lightweight responses), and IoT devices (minimal data).

```
Web Browser → Web BFF (rich product details, high-res images)
Mobile App → Mobile BFF (compressed images, minimal data)
IoT Device → IoT BFF (product IDs only, no images)
```

---

## Service Mesh

*Popularized by Buoyant's Linkerd (2016) and later Istio (2017)*

Dedicated infrastructure layer that handles service-to-service communication, providing observability, security, and traffic management without requiring code changes. Implements the sidecar pattern at scale.

**Use When**:
- Large number of microservices (typically >10-20 services)
- Need consistent security and observability across all services
- Complex traffic management requirements (canary, A/B testing, retries, timeouts)
- Multiple teams developing services in different languages
- Want to extract networking concerns from application code

**Components**:

**Data Plane** (per-service sidecar proxies):
- Intercepts all network traffic for the service
- Implements routing, load balancing, retries, circuit breaking
- Collects metrics and traces
- Common proxy: **Envoy** (high-performance C++ proxy)

**Control Plane** (centralized management):
- Configures all data plane proxies
- Manages certificates for mTLS
- Collects telemetry and distributes policies
- Provides service discovery

**Example**: Kubernetes cluster with Istio service mesh providing mTLS encryption, traffic splitting for canary deployments, and distributed tracing.

```
Service Mesh Architecture:

Control Plane (Istio Components):
  - Pilot: Traffic management, service discovery
  - Citadel: Certificate management, mTLS
  - Galley: Configuration management
  - Telemetry: Metrics collection

Data Plane (Envoy Sidecars):
  Each microservice pod contains:
    - Application Container (business logic)
    - Envoy Sidecar Proxy (networking)
      - Mutual TLS encryption
      - Traffic routing & load balancing
      - Circuit breaking & retries
      - Metrics & distributed tracing
```

**Popular Service Meshes**:
- **Istio**: Feature-rich, complex, large footprint
- **Linkerd**: Lightweight, simpler, Rust-based
- **Consul Connect**: HashiCorp, multi-platform
- **AWS App Mesh**: Managed service mesh for AWS

**Trade-offs**:
- **Pros**: Zero code changes, consistent policies, powerful traffic management
- **Cons**: Operational complexity, resource overhead (CPU/memory for sidecars), latency increase (~1-5ms per hop)

---

## Quick Reference

### Pattern Comparison

| Pattern | Scope | Complexity | Use Case |
|---------|-------|------------|----------|
| **Sidecar** | Single app | Low | Cross-cutting concerns |
| **Ambassador** | Outbound calls | Low | Centralize networking |
| **BFF** | Per client type | Medium | Client-specific needs |
| **Service Mesh** | All services | High | Large-scale microservices |

### Decision Tree

**Need cross-cutting functionality?** → Sidecar
**Centralize outbound networking?** → Ambassador
**Different client requirements?** → BFF
**Many microservices needing consistent policies?** → Service Mesh

### Implementation Tools

**Sidecar**: Kubernetes sidecars | Docker Compose
**Ambassador**: Envoy | NGINX
**BFF**: Custom services | API Gateway with routing
**Service Mesh**: Istio | Linkerd | Consul Connect

### When to Avoid

**Sidecar**: Adds complexity for simple apps
**Ambassador**: Unnecessary for apps with few external calls
**BFF**: Overkill for single client type
**Service Mesh**: Too complex for <10 services

---
