---
layout: case-study
title: "When Third-Party Integration Meets Domain Boundaries"
subtitle: "Embedding Discord concerns within domains instead of extracting them to a dedicated service"
description: "Should third-party integration concerns live inside existing domains or become their own bounded context? This case study examines the tradeoffs through a Discord integration, choosing a domain-embedded approach as intentional short-term debt."
role: "System Architect"
date: 2026-01-27
headline_metric: "Intentional Debt"
headline_detail: "Documented tradeoffs & evolution triggers"
category: "design"
category_label: "Architecture & Design"
technologies:
  - Discord API
  - OAuth 2.0
  - DDD
  - Microservices
---

## Executive Summary

The company sells access to content published on a Discord server across multiple channels. The initial implementation relied on manual verification: employees confirm purchases and assign Discord roles by hand. As the product matures, this workflow needs automation.

Automating access requires integrating Discord into multiple existing domains: authorization needs role mappings, subscription management needs plan-to-role assignments, user management needs Discord identity storage, and registration needs OAuth orchestration. This raises an architectural question: should Discord become its own API, or should Discord concerns be embedded within these existing domains?

I chose embedding. Each domain owns the Discord concepts relevant to its responsibilities. This is intentional short-term debt driven by two architectural characteristics I prioritize: cost and agility. With a single small team and limited time, extracting a dedicated Discord API would introduce coordination overhead and slow discovery. The domain-embedded approach allows each domain to evolve its Discord integration independently.

**Timeline**: The decision and initial implementation took approximately one week. The architecture will evolve to a thin provider when specific triggers occur: multiple similar third-party integrations, team growth beyond a single team, or significantly increased API call volume.

This case study examines that decision, the alternatives considered, what would trigger evolution toward centralization, and why I consider this a rare example of true technical debt: intentional, with understood interest, and a clear payback plan.

## The Business Context

The company operates as a content platform where customers purchase access to various products and services. One product grants access to a Discord server where the company publishes content and customers engage in community discussions.

This is the first time the company sells access to content published on a platform it doesn't directly own. Previous products were delivered through infrastructure the company controlled. Discord introduces new variables: a third-party API, external identity systems, platform-specific access controls. This novelty is part of why discovery and agility were prioritized so heavily in the architectural decision.

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

The solution needs to automate the entire flow, including OAuth-based Discord linking, automatic role assignment based on plans, and real-time role updates when plans change.

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
│ • Email verification  │ │ • Billing integration │ │ • Product permissions │
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

### Option 1: Domain-Embedded Integration

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

**Authorization API** owns role metadata. This table defines which Discord roles exist, which can be assigned programmatically, and which serve as defaults for free or paid users:

```sql
CREATE TABLE discord_roles (
   id INT NOT NULL AUTO_INCREMENT,
   discord_id VARCHAR(30) NOT NULL,
   name VARCHAR(100) NOT NULL,
   is_assignable BOOLEAN NOT NULL DEFAULT 0,
   is_plan_assignable BOOLEAN NOT NULL DEFAULT 0,
   is_default_free BOOLEAN NULL,
   is_default_paid BOOLEAN NULL,
   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (id),
   UNIQUE KEY UK_discord_roles_discord_id (discord_id)
);
```

**Subscription Management API** owns plan-to-role mappings. This determines which Discord roles a given subscription plan grants:

```sql
CREATE TABLE plan_discord_roles (
   id INT NOT NULL AUTO_INCREMENT,
   plan_id INT UNSIGNED NOT NULL,
   role_id INT NOT NULL,
   CONSTRAINT UC_RoleId_PlanId UNIQUE (plan_id, role_id),
   CONSTRAINT FK_PlanDiscordRoles_Plans FOREIGN KEY (plan_id) REFERENCES plans(id),
   PRIMARY KEY (id)
);
```

**Users API** owns the identity mapping between platform users and Discord accounts:

```sql
CREATE TABLE user_discord_accounts (
    user_id INT NOT NULL,
    discord_id VARCHAR(20) NOT NULL,
    discord_username VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_discord_id (discord_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id)
);
```

**Registrar API** has no persistent Discord data. It orchestrates the OAuth flow and registration, then delegates storage to the Users API and triggers authorization sync.

**Workflow:**
1. User initiates Discord linking through Prime
2. Registrar API handles OAuth, obtains Discord identity
3. Registrar API stores identity mapping via Users API
4. Registrar API triggers authorization sync
5. Authorization API reads user's plans (from Subscription Management), determines correct roles, updates Discord

When a plan changes (billing webhook), the Subscription Management API triggers the same authorization sync, and roles update automatically.

**What remains centralized:**

Embedding client code in each domain doesn't mean abandoning governance. Configuration and credentials are managed through AWS Parameter Store, giving us:

- Single source of truth for Discord API credentials
- Consistent client configuration (timeouts, retry policies) across all domains
- Centralized audit trail of configuration changes
- Environment-specific settings without code changes

The domain-embedded approach applies to code, not to operational governance. Security and configuration management aren't "Phase 2" concerns.

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

## The Decision: Domain-Embedded Integration

I chose Option 1 (domain-embedded) for now, with a planned evolution to Option 2 (extracted provider) once the solution matures.

### Why Not a Thick Provider?

Option 3 inverts the natural dependency direction. Domains at the center should call out to the fringe; the fringe should not reach into the center. A provider exists to be used by domains, not to use them.

Role synchronization requires reading a user's current plans and applying authorization rules. If the Discord provider owns this logic, it must either:

1. **Call into Subscription Management and Authorization APIs** to get the data it needs, which means a fringe concern reaching into the domain center
2. **Duplicate plan and authorization data** into its own storage, creating consistency problems
3. **Receive all relevant data in the sync request**, forcing callers to assemble context that the provider then processes

None of these are clean. The current architecture has Authorization reading from Subscription Management, but that's different: both are cross-cutting concern domains at the center. Shared domains exist to be used AND to use each other. A thick Discord provider is a peripheral integration, not a shared domain. It belongs on the fringe, called by domains, not calling into them.

The Authorization API already exists to answer "what can this user access?" Adding Discord as another access type fits naturally. Extracting that logic into a Discord provider would fragment authorization decisions across services.

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

Creating a provider now would force us to define an interface before understanding what each domain actually needs from Discord. We'd be designing an abstraction during the period when we're still discovering requirements. The feature has a limited time window to prove value. If it succeeds, we can spend additional time maturing the architecture. If it fails, we've avoided building infrastructure for something that didn't work out.

This calculus changes with team growth. With multiple teams, waiting days or weeks for another team to update a shared API doesn't solve anyone's problem during discovery. But it becomes worthwhile once patterns stabilize and the coordination cost is amortized across many uses.

### The Architectural Characteristics Driving This Decision

Two characteristics dominate my priorities for this system:

| Characteristic | Definition | How Embedding Serves It |
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

| Trigger | Current State | Evolution Signal |
|---------|---------------|------------------|
| Multiple providers | 1 (Discord only) | 2+ providers with similar patterns |
| Team structure | Single small team | Multiple teams needing Discord integration |
| API call volume | Infrequent (OAuth, role changes) | Real-time sync, frequent operations |
| API complexity | Small, stable subset | Frequent Discord API changes requiring coordinated updates |

### Trigger 1: Multiple Third-Party Providers With Similar Patterns

If the company integrates Slack, Telegram, or other community platforms alongside Discord, the domain-embedded approach multiplies:

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

But more providers doesn't automatically justify extraction. Each provider has its own API, its own concepts, and its own quirks. If providers have genuinely different needs, embedding each separately may still be appropriate. The trigger for extraction isn't just "more providers" but "more providers with similar enough patterns that a shared abstraction adds value rather than forcing awkward compromises."

If a second provider emerged with very similar integration patterns, that would be a stronger signal to extract. But even then, the decision would be circumstantial rather than automatic.

### Trigger 2: Team Growth

With a single team, coordination overhead is just context switching. With multiple teams, a shared provider creates blocking dependencies:

- Team A owns Authorization and needs a Discord operation to change
- Team B owns the Discord provider
- Team A waits days or weeks for Team B to update the provider API

During discovery, this wait time is unacceptable. The feature has a limited window to prove value, and blocking on another team's backlog doesn't solve the problem that needed to be solved.

But with embedded code, coordination still happens, just through shared values rather than shared code. If teams communicate as they should, they align on conventions for error handling, retry logic, and API usage. Conway's Law still applies, but the communication happens through documentation and review rather than through API contracts.

The trigger for extraction isn't team count alone. It's when the coordination cost of maintaining consistent behavior across embeddings exceeds the blocking cost of waiting on a shared provider. That typically happens once patterns stabilize and discovery gives way to steady-state operation.

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

Phase 1 (Current): Domain-Embedded
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

**Mitigation**: Share values, not code. The duplication is limited (we use a small API surface), and creating another container just to eliminate copy-paste is often worse than communicating governance and design between tech leads. When evolving to Phase 2, the provider consolidates the client code, but only after we understand what that client actually needs to do.

### Consequence: Inconsistent Error Handling

Each domain might handle Discord API errors differently.

**Mitigation**: Share values, not code. Establish conventions in the ADR: retry logic, timeout configuration, error categorization. Teams share these values through documentation and code review, not through forced code sharing. The goal is consistent behavior through shared understanding, not identical implementations.

## Key Lessons

### 1. Provider vs. Domain Is a Spectrum, Not a Binary

The choice isn't "extract everything" or "embed everything." Discord API access (infrastructure) can be extracted while Discord business logic (domain) stays embedded in domains. The thin provider + adapter pattern achieves this separation.

### 2. Architectural Characteristics Should Drive the Decision

Without explicit priorities, architectural debates become opinion battles. When I say "cost and agility matter most for this system," the domain-embedded approach follows logically. A different system prioritizing consistency and maintainability would choose differently.

### 3. Intentional Debt Requires a Payback Plan

"We'll clean it up later" isn't a plan. Intentional debt specifies: what triggers evolution, what the evolved state looks like, and what interest we're paying until then. Without these, it's just rationalized shortcuts.

### 4. Small Teams Have Different Optimal Architectures

Coordination overhead that's negligible for a single team becomes significant with multiple teams. The "right" architecture depends on who's building it, not just what's being built.

Small teams can share values without sharing code. Conventions, ADRs, and code review create consistent behavior across embeddings without the blocking dependencies of a shared provider. As teams grow, shared code can evolve from those shared values, not as a substitute for them but as a natural extension. The values remain; the code becomes their embodiment.

### 5. Integration Discovery Differs from Domain Discovery

Conventional wisdom says monolithic approaches aid discovery in greenfield systems, and that's true when you're still learning where domain boundaries belong. But this isn't greenfield. The domains are established, each with its own maturity, pace, and team concerns.

The discovery here is different: how does Discord fit into each domain's existing responsibilities? Each domain needs room to evolve its integration without being blocked by a shared abstraction that's also changing. Creating a centralized provider now would force premature abstraction, defining an interface before knowing what each domain actually needs from it. Once integration patterns stabilize across domains, centralization captures what was learned.

## Conclusion

Where should third-party integration logic live? The answer depends on what you're optimizing for and how mature your understanding is.

For a small team in discovery mode with a single third-party integration, embedding within domains minimizes coordination overhead and maximizes agility. The cost is duplication and scattered concerns.

For a mature system with multiple teams and stabilized patterns, a thin provider centralizes infrastructure concerns while domain adapters preserve business logic ownership. The cost is coordination overhead and potential bottlenecks.

I chose embedding now, with a clear path to extraction. This is intentional debt, not neglect. The interest is understood, the payback plan is defined, and the triggers for evolution are explicit. When those triggers occur, the architecture will evolve. Until then, it serves the current needs.

The worst outcome would be building a centralized provider prematurely, paying coordination costs during the period when agility matters most, only to discover the abstraction doesn't fit the actual usage patterns. Better to let patterns emerge, then capture them.
