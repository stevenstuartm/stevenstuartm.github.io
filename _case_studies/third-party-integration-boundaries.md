---
layout: case-study
title: "When Third-Party Integration Meets Domain Boundaries"
subtitle: "Distributing Discord concerns across domains instead of centralizing them"
description: "When integrating a third-party service like Discord into a domain-driven system, architects face a fundamental question: should provider concerns live inside existing domains or become their own bounded context? This case study examines the tradeoffs through a concrete Discord integration, arguing for a distributed approach as intentional short-term debt with a clear evolution path."
role: "System Architect"
date: 2025-01-01
technologies:
  - Discord API
  - OAuth 2.0
  - Domain-Driven Design
  - Microservices
---

## Executive Summary

The company sells access to content published on a Discord server across multiple channels. The initial implementation relied on manual verification: employees confirm purchases and assign Discord roles by hand. As the product matures, this workflow needs automation.

Automating access requires integrating Discord into multiple existing domains: authorization needs role mappings, subscription management needs plan-to-role assignments, user management needs Discord identity storage, and registration needs OAuth orchestration. This raises an architectural question: should Discord become its own API, or should Discord concerns be distributed across these existing domains?

I chose distribution. Each domain owns the Discord concepts relevant to its responsibilities. This is intentional short-term debt driven by two architectural characteristics I prioritize: cost and agility. With a single small team and limited time, creating a centralized Discord API would introduce coordination overhead and slow discovery. The distributed approach allows each domain to evolve its Discord integration independently.

This case study examines that decision, the alternatives considered, what would trigger evolution toward centralization, and why I consider this a rare example of true technical debt: intentional, with understood interest, and a clear payback plan.

## The Business Context

The company operates as a content platform where customers purchase access to various products and services. One product grants access to a Discord server where the company publishes content and customers engage in community discussions.

The current workflow is entirely manual:

1. Customer purchases a Discord access plan through the normal purchase flow
2. Customer receives an email directing them to create a Discord account and join the company server
3. Customer provides their registered email through a Discord workflow
4. An employee manually verifies the customer's plan in a spreadsheet
5. The employee assigns the appropriate Discord role, granting channel access
6. When a customer's plan changes (upgrade, downgrade, cancellation), an employee must notice the change and manually update their Discord role

Discord roles control channel visibility. A "Premium" role might grant access to exclusive channels, while a "Free" role provides limited access. The mapping between subscription plans and Discord roles is the core business logic that needs automation.

### Why This Matters

The manual process creates several problems:

- **Delayed access**: Customers wait for human verification before accessing content they've paid for
- **Inconsistent state**: Plan changes aren't immediately reflected in Discord access
- **Operational burden**: Employee time spent on manual verification scales linearly with customer growth
- **Error-prone**: Spreadsheet-based tracking invites mistakes

The solution needs to automate the entire flow: OAuth-based Discord linking, automatic role assignment based on plans, and real-time role updates when plans change.

## The Existing Domain Architecture

Before discussing where Discord fits, here's the relevant portion of the existing architecture:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Prime (Frontend)                                │
│                     User-facing web application                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│    Registrar API      │ │  Subscription Mgmt    │ │   Authorization API   │
│                       │ │        API            │ │                       │
│ • User registration   │ │ • Plan management     │ │ • Access rules        │
│ • OAuth orchestration │ │ • Billing integration │ │ • Product permissions │
│ • Onboarding flows    │ │ • Billing events      │ │ • Feature flags       │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
                                      │
                                      ▼
                          ┌───────────────────────┐
                          │      Users API        │
                          │                       │
                          │ • User profiles       │
                          │ • Identity data       │
                          │ • GraphQL interface   │
                          └───────────────────────┘
```

Each API owns its domain completely. The Authorization API determines what users can access. The Subscription Management API handles plans and billing events from the payment provider. The Registrar API orchestrates user onboarding. The Users API stores identity and profile data.

## The Options Considered

### Option 1: Distributed Integration (Domain-Owned)

Each domain owns the Discord concepts relevant to its responsibilities:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                                   Prime                                        │
│                        Discord OAuth UI components                             │
└───────────────────────────────────────────────────────────────────────────────┘
                                       │
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
          ▼                            ▼                            ▼
┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐
│    Registrar API     │  │  Subscription Mgmt   │  │  Authorization API   │
│                      │  │                      │  │                      │
│ Discord OAuth flow   │  │ plan_discord_roles   │  │ discord_roles table  │
│ Discord registration │  │ (which plans grant   │  │ (role metadata,      │
│                      │  │  which roles)        │  │  assignability rules)│
│   ┌──────────────┐   │  │   ┌──────────────┐   │  │   ┌──────────────┐   │
│   │Discord Client│   │  │   │Discord Client│   │  │   │Discord Client│   │
│   └──────────────┘   │  │   └──────────────┘   │  │   └──────────────┘   │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
                                                               │
                                                    User authorization
                                                         sync
                                                               │
                                       ┌───────────────────────┘
                                       ▼
                          ┌──────────────────────┐
                          │      Users API       │
                          │                      │
                          │ user_discord_accounts│
                          │ (Discord ↔ user      │
                          │  identity mapping)   │
                          └──────────────────────┘
```

**Data ownership:**
- **Authorization API**: `discord_roles` table with role metadata (which roles exist, which are assignable, default roles for free/paid users)
- **Subscription Management API**: `plan_discord_roles` table mapping plans to roles
- **Users API**: `user_discord_accounts` table linking platform users to Discord identities
- **Registrar API**: No persistent Discord data; orchestrates OAuth flow and registration

**Workflow:**
1. User initiates Discord linking through Prime
2. Registrar API handles OAuth, obtains Discord identity
3. Registrar API stores identity mapping via Users API
4. Registrar API triggers authorization sync
5. Authorization API reads user's plans (from Subscription Management), determines correct roles, updates Discord

When a plan changes (billing webhook), the Subscription Management API triggers the same authorization sync, and roles update automatically.

**What remains centralized:**

Distributing client code doesn't mean abandoning governance. Configuration and credentials are managed through AWS Parameter Store, giving us:

- Single source of truth for Discord API credentials
- Consistent client configuration (timeouts, retry policies) across all domains
- Centralized audit trail of configuration changes
- Environment-specific settings without code changes

The distributed approach applies to code, not to operational governance. Security and configuration management aren't "Phase 2" concerns.

### Option 2: Thin Provider API

Centralize Discord API access while keeping business logic in domains:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              Discord Provider API                              │
│                                                                                │
│  • Discord API client (credentials, rate limiting, retries)                   │
│  • OAuth token management                                                      │
│  • Role assignment operations                                                  │
│  • Server membership operations                                                │
│  • No business logic about WHEN to assign roles                               │
└───────────────────────────────────────────────────────────────────────────────┘
                    ▲                    ▲                    ▲
                    │                    │                    │
       ┌────────────┘                    │                    └────────────┐
       │                                 │                                 │
┌──────┴───────────────┐  ┌──────────────┴─────────────┐  ┌───────────────┴────┐
│    Registrar API     │  │  Subscription Mgmt API     │  │  Authorization API │
│                      │  │                            │  │                    │
│ Calls provider for   │  │ plan_discord_roles table   │  │ discord_roles      │
│ OAuth operations     │  │ (still owns plan→role      │  │ (still owns role   │
│                      │  │  mappings)                 │  │  metadata)         │
└──────────────────────┘  └────────────────────────────┘  └────────────────────┘
```

The provider becomes an Anti-Corruption Layer: it translates between Discord's API and domain-friendly operations. Domains still own their Discord-related data and logic, but they call the provider instead of embedding Discord client code.

### Option 3: Thick Provider API

Centralize both Discord access AND Discord-related data:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              Discord Provider API                              │
│                                                                                │
│  • Discord API client                                                          │
│  • OAuth token management                                                      │
│  • discord_roles table                                                         │
│  • plan_discord_roles table                                                    │
│  • user_discord_accounts table                                                 │
│  • Role sync logic                                                             │
└───────────────────────────────────────────────────────────────────────────────┘
                    ▲                    ▲
                    │                    │
       ┌────────────┘                    └────────────┐
       │                                              │
┌──────┴───────────────┐               ┌──────────────┴─────────────┐
│    Registrar API     │               │  Subscription Mgmt API     │
│                      │               │                            │
│ Delegates OAuth to   │               │ Notifies provider of       │
│ provider             │               │ plan changes               │
└──────────────────────┘               └────────────────────────────┘
```

The provider owns everything Discord-related. Domains notify it of relevant events (plan changes, user registration), and the provider handles the rest.

## The Decision: Distributed Integration

I chose Option 1 (distributed) for now, with a planned evolution to Option 2 (thin provider) once the solution matures.

### Why Not a Thick Provider?

Option 3 creates problematic coupling. Role synchronization requires reading a user's current plans and applying authorization rules. If the Discord provider owns this logic, it must either:

1. **Call into Subscription Management and Authorization APIs** to get the data it needs, creating circular dependencies and distributed transactions
2. **Duplicate plan and authorization data** into its own storage, creating consistency problems
3. **Receive all relevant data in the sync request**, forcing callers to assemble context that the provider then processes

None of these are clean. The Authorization API already exists to answer "what can this user access?" Adding Discord as another access type fits naturally. Extracting that logic into a Discord provider would fragment authorization decisions across services.

### Why Not a Thin Provider (Yet)?

Option 2 is the likely evolution, but creating it now would cost more than it saves.

**Current state:**
- Single small team
- Limited development time
- One third-party integration (Discord)
- Need for rapid discovery as requirements clarify

**What a thin provider adds:**
- Another service to deploy and maintain
- API contract to design and version
- Coordination overhead when Discord integration needs change

**What a thin provider removes:**
- Duplicate Discord client code across domains
- Inconsistent error handling and retry logic

With one integration and one team, the coordination overhead exceeds the benefit of centralization. Each domain can evolve its Discord usage independently without waiting for provider changes.

### The Architectural Characteristics Driving This Decision

Two characteristics dominate my priorities for this system:

| Characteristic | Definition | How Distribution Serves It |
|----------------|------------|---------------------------|
| **Cost** | Minimize development and operational expense | No new service to build/deploy/maintain; no coordination overhead; faster time to solution |
| **Agility** | Ability to respond quickly to changing requirements | Each domain evolves independently; no bottleneck on provider changes; discovery happens in parallel |

A centralized provider optimizes for different characteristics:

| Characteristic | Definition | How Centralization Serves It |
|----------------|------------|------------------------------|
| **Consistency** | Uniform behavior across the system | Single implementation of Discord access; consistent error handling |
| **Maintainability** | Ease of understanding and modifying | One place to find Discord code; clear boundary |

For a mature system with multiple teams, consistency and maintainability might dominate. For a small team in discovery mode, cost and agility matter more.

## What Changes When Conditions Change

This decision isn't permanent. Several triggers would shift the calculus toward centralization.

### Trigger 1: Multiple Third-Party Providers

If the company integrates Slack, Telegram, or other community platforms alongside Discord, the distributed approach multiplies:

```
Current (1 provider):
  - Authorization owns discord_roles
  - Subscription Mgmt owns plan_discord_roles
  - Users owns user_discord_accounts
  - 3 domains × 1 provider = 3 integration points

Future (3 providers):
  - Authorization owns discord_roles, slack_roles, telegram_roles
  - Subscription Mgmt owns plan_discord_roles, plan_slack_roles, plan_telegram_roles
  - Users owns user_discord_accounts, user_slack_accounts, user_telegram_accounts
  - 3 domains × 3 providers = 9 integration points
```

At some threshold, the pattern becomes unwieldy. A provider abstraction starts making sense, though the exact threshold depends on how similar the integrations are.

### Trigger 2: Team Growth

With a single team, coordination overhead is just context switching. With multiple teams:

- Team A owns Authorization and needs Discord role sync to change
- Team B owns the Discord provider
- Team A now depends on Team B's backlog and priorities

Conway's Law suggests the architecture should match the communication structure. Multiple teams might benefit from clearer boundaries, even if those boundaries add coordination cost.

### Trigger 3: Processing Load

Currently, Discord API calls are infrequent: OAuth during registration, role updates on plan changes. If usage patterns shift (real-time presence sync, message integration, frequent role checks), centralized rate limiting and connection pooling become valuable.

### Trigger 4: Discord API Complexity

Discord's API evolves. If changes require coordinated updates across domains, a centralized provider absorbs that complexity. Currently, each domain uses a small, stable subset of the API, so this isn't pressing.

## This Is Intentional Technical Debt

Technical debt is often unintentional: shortcuts taken under pressure that accumulate interest over time. This is different. This is deliberate:

**The principal**: Duplicate Discord client code across domains; no single place to understand "how we talk to Discord."

**The interest**: When Discord changes their API or we need consistent retry logic, we update multiple places. When debugging Discord issues, we check multiple services.

**The payback plan**: Once the Discord integration proves itself and matures, consolidate API access into a thin provider. Domains keep their data and logic but call the provider instead of embedding client code. The provider becomes an Anti-Corruption Layer.

```
Evolution path:

Phase 1 (Current): Distributed
  - Each domain has Discord client code
  - Fast to build, easy to change independently
  - Interest: duplication across domains

Phase 2 (Future): Thin Provider + Domain Adapters
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        Discord Provider API                              │
  │  • API client, credentials, rate limiting                               │
  │  • Domain-agnostic operations (assign role, get user, etc.)             │
  └─────────────────────────────────────────────────────────────────────────┘
                    ▲                    ▲                    ▲
                    │                    │                    │
  ┌─────────────────┴──┐  ┌──────────────┴──────────┐  ┌─────┴─────────────┐
  │ Registrar Adapter  │  │ Subscription Adapter    │  │ Auth Adapter      │
  │                    │  │                         │  │                   │
  │ Domain-specific    │  │ Domain-specific         │  │ Domain-specific   │
  │ Discord logic      │  │ Discord logic           │  │ Discord logic     │
  └────────────────────┘  └─────────────────────────┘  └───────────────────┘

  - Provider handles Discord API concerns
  - Adapters translate domain needs to provider operations
  - Data stays in domains
  - Business logic stays in domains
```

The adapter pattern preserves domain independence while centralizing infrastructure concerns. Each domain's adapter can evolve its usage of the provider without affecting others.

### Why This Qualifies as True Technical Debt

Most "technical debt" is actually just poor code quality. True technical debt has these properties:

| Property | This Decision |
|----------|---------------|
| **Intentional** | Yes, I chose this knowing the tradeoffs |
| **Understood interest** | Yes, I know what maintenance burden it creates |
| **Clear payback plan** | Yes, evolution to thin provider is defined |
| **Rational tradeoff** | Yes, short-term agility outweighs long-term maintenance |

The decision isn't "we'll fix it later" with no plan. It's "we'll evolve it when these specific triggers occur, in this specific way."

## Consequences and Mitigations

### Consequence: Confusion About Where Discord Logic Lives

Without centralization, developers might not know where to look for Discord-related code.

**Mitigation**: Document the ownership clearly. Discord roles metadata → Authorization. Plan-to-role mappings → Subscription Management. User identity → Users. OAuth orchestration → Registrar. The ADR (Architecture Decision Record) captures this reasoning.

### Consequence: Duplicate Discord Client Code

Each domain embeds its own Discord API client.

**Mitigation**: Accept this for now. The duplication is limited (we use a small API surface), and the cost of coordination exceeds the cost of duplication for a single team. When evolving to Phase 2, the provider eliminates duplication.

### Consequence: Inconsistent Error Handling

Each domain might handle Discord API errors differently.

**Mitigation**: Establish conventions in the ADR. Retry logic, timeout configuration, and error categorization should be consistent even if code is duplicated. Review during code review.

## Key Lessons

### 1. Provider vs. Domain Is a Spectrum, Not a Binary

The choice isn't "centralize everything" or "distribute everything." Discord API access (infrastructure) can centralize while Discord business logic (domain) stays distributed. The thin provider + adapter pattern achieves this separation.

### 2. Architectural Characteristics Should Drive the Decision

Without explicit priorities, architectural debates become opinion battles. When I say "cost and agility matter most for this system," the distributed approach follows logically. A different system prioritizing consistency and maintainability would choose differently.

### 3. Intentional Debt Requires a Payback Plan

"We'll clean it up later" isn't a plan. Intentional debt specifies: what triggers evolution, what the evolved state looks like, and what interest we're paying until then. Without these, it's just rationalized shortcuts.

### 4. Small Teams Have Different Optimal Architectures

Coordination overhead that's negligible for a single team becomes significant with multiple teams. The "right" architecture depends on who's building it, not just what's being built. This will change as the organization grows.

### 5. Integration Discovery Differs from Domain Discovery

Conventional wisdom says monolithic approaches aid discovery in greenfield systems, and that's true when you're still learning where domain boundaries belong. But this isn't greenfield. The domains are established, each with its own maturity, pace, and team concerns.

The discovery here is different: how does Discord fit into each domain's existing responsibilities? Each domain needs room to evolve its integration without being blocked by a shared abstraction that's also changing. Creating a centralized provider now would force premature abstraction, defining an interface before knowing what each domain actually needs from it. Once integration patterns stabilize across domains, centralization captures what was learned.

## Conclusion

Where should third-party integration logic live? The answer depends on what you're optimizing for and how mature your understanding is.

For a small team in discovery mode with a single third-party integration, distribution across domains minimizes coordination overhead and maximizes agility. The cost is duplication and scattered concerns.

For a mature system with multiple teams and stabilized patterns, a thin provider centralizes infrastructure concerns while domain adapters preserve business logic ownership. The cost is coordination overhead and potential bottlenecks.

I chose distribution now, with a clear path to evolution. This is intentional debt, not neglect. The interest is understood, the payback plan is defined, and the triggers for evolution are explicit. When those triggers occur, the architecture will evolve. Until then, it serves the current needs.

The worst outcome would be building a centralized provider prematurely, paying coordination costs during the period when agility matters most, only to discover the abstraction doesn't fit the actual usage patterns. Better to let patterns emerge, then capture them.
