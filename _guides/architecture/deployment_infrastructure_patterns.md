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

Infrastructure layer that handles service-to-service communication, providing observability, security, and traffic management.

**Use When**:
- Large number of microservices
- Need consistent security and observability
- Complex traffic management requirements
- Multiple teams developing services

**Components**:

- **Data Plane**: Sidecar proxies handling traffic
- **Control Plane**: Configures and manages proxies

**Example**: Kubernetes cluster with Istio service mesh providing mTLS encryption, traffic splitting for canary deployments, and distributed tracing.

```
Service Mesh:
  Control Plane (Istio):
    - Policy configuration
    - Telemetry collection
    - Service discovery

  Data Plane (Envoy Sidecars):
    - Traffic routing
    - Load balancing
    - Circuit breaking
    - Observability
```

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
