---
layout: case-study
title: "When Real-Time Push Needs Product Context"
subtitle: "A proof-of-concept for routing WebSocket messages through product entitlements, and what it taught about validating requirements before building infrastructure"
description: "A custom SignalR service that dynamically resolved channel names from user entitlements and message scopes. The architecture was sound, the POC worked at moderate scale, but the underlying problem was solved with better caching before real-time push was needed. An honest look at buy-vs-build when managed alternatives exist."
role: "System Architect"
date: 2025-01-01
headline_metric: "POC, Never Shipped"
headline_detail: "Sound architecture, unvalidated requirement"
category: "decision"
category_label: "Architecture Decision"
technologies:
  - .NET
  - ASP.NET Core SignalR
  - AWS SQS
  - AWS EventBridge
  - AWS DynamoDB
  - AWS ECS
  - MessagePack
---

## The Problem

The web application was data-hungry. It served authenticated users with paid content products, and those users expected near-real-time updates: sector alerts, trade alerts, application news, and scanner notifications. The existing pattern of polling APIs on interval was getting slower as the product surface grew, and the team knew that adding more polling endpoints would only make the responsiveness problem worse.

The straightforward solution would have been WebSocket-based push notifications. Subscribe to a topic, receive messages when they arrive. But the platform had a complicating factor that made generic pub/sub insufficient: users had different product entitlements, and the same topic needed to deliver different content to different users based on what they had paid for.

A user subscribed to product "CHLT" who asked for "News" should only receive news relevant to that product. A user with "FullAccess" should receive everything. A message published to the "News" topic with scope limited to "CHLT" and "FullAccess" should reach both of those users but not a user who only subscribed to "Sfc." The routing logic lived entirely on the server side; the client should never need to know about product-scoped channels or entitlement resolution. From the client's perspective, subscribing to "News" should just work.

This was a repeating pattern across the platform: context drove product and user decisions, and those decisions were involved in nearly every feature more than having the convenience of generic configuration and generic behavior.

The team scoped this as a proof-of-concept: build a working solution, validate the architecture at moderate scale, and determine whether the investment was justified before committing to production infrastructure. That framing matters for understanding the decisions that followed.

## Why Not Something Off-the-Shelf?

The team evaluated alternatives before building custom, but in retrospect, the evaluation was narrower than it should have been. The AWS primitives were legitimately poor fits, but the team stopped there without seriously evaluating managed real-time services that were better suited to the problem.

### AWS Primitives: Fair Rejections

**API Gateway WebSockets** provide a managed connection layer, but the routing model is flat. A client connects, a route key selects a Lambda handler, and that handler must implement all business logic for determining who receives what. The subscribe path would have required a Lambda authorizer to look up entitlements, resolve them into channel identifiers, and manage group membership in an external store like DynamoDB. The publish path would have required another Lambda to resolve message scopes into target connections by querying that same store. At that point, API Gateway is just a WebSocket transport layer and all the context-driven routing lives in custom code anyway.

**SNS filtering** requires the subscriber to declare upfront which attributes to filter on. The design goal was the opposite: clients subscribe to a human-readable topic like "News" and the server resolves the actual filtering based on server-side context the client has no knowledge of. SNS doesn't support dynamic fan-out where the channel name itself is derived from user context.

**AppSync subscriptions** require the client to specify what it's subscribing to with enough specificity for the filter to work. The client would need to know its own product entitlements, which defeats the purpose of server-side resolution.

These were reasonable rejections. None of these services are designed for the "subscribe to a topic, let the server figure out the rest" pattern.

### Managed Real-Time Services: The Gap in the Evaluation

Where the evaluation fell short was in not seriously considering purpose-built real-time messaging services like Pusher or Ably. These services support exactly the pattern the team was trying to build.

Pusher's private channels use an authorization callback where the server decides which channels a connection is allowed to join. The flow would have been: client subscribes to "News," Pusher calls the authorization endpoint, the endpoint looks up the user's product entitlements, and approves subscription to `private-news-CHLT` and `private-news-Sfc`. That authorization callback is maybe 50 lines of code sitting behind an endpoint the team already knew how to build.

Ably provides a similar token-based authorization model, and both services offer message history (comparable to the lookback pattern) as a built-in feature. The per-message TTL, deduplication, and replay that required a custom DynamoDB table and fire-and-forget replay logic in the custom solution are standard capabilities in these platforms.

AWS IoT Core also supports per-client topic policies based on identity claims, with MQTT topics that could map naturally to the product-scoped pattern. The topic structure `news/CHLT`, `news/Sfc` with IAM-style policies restricting which topics each user can subscribe to would achieve the same result.

The honest reason these weren't evaluated seriously was that the team defaulted to building within the technology stack it already operated. The organization ran .NET services on ECS, had SignalR expertise, and had authorization infrastructure ready to use. The reflex was to compose from familiar components rather than evaluate whether a managed service could address the same requirements.

That said, managed services come with their own tradeoffs that the evaluation would have surfaced. Pusher and Ably charge per connection and per message. At moderate scale those costs can exceed what AWS infrastructure costs for the same workload, especially when the AWS components use PAY_PER_REQUEST billing that scales to near-zero during quiet periods. The authorization callback model also introduces latency because Pusher must call the team's endpoint, the endpoint must look up entitlements, and the response must travel back before the subscription completes. In the custom solution, that authorization lookup happened in-process with no network round trip. For a platform that highly valued client-API responsiveness, that latency difference mattered.

There's also an agility consideration. With a custom solution, the team controlled the full stack. Changes to routing logic, new channel behaviors, debugging connection issues, and operational tuning were all within the team's domain. With a managed service, those capabilities are constrained by the vendor's API surface, release cycle, and outage profile.

The point isn't that managed services were clearly better. It's that they should have been part of the evaluation so the tradeoffs could be weighed deliberately rather than defaulted past.

## Solution Architecture

The system had two primary flows: subscribing to topics and publishing messages to subscribers. Both flows passed through the same context resolution layer that translated between human-readable topics and product-scoped SignalR groups.

### Subscribe Flow

```
┌──────────────┐    WebSocket     ┌──────────────────────────────────────────────┐
│  Client App  │ ──────────────▶  │            ContentHub (SignalR)              │
│              │  Subscribe(      │                                              │
│              │  ["News",        │  Extracts authenticated Principal            │
│              │   "Alerts"])     │  Delegates to PubSubAdapter                  │
└──────────────┘                  └────────────────────┬─────────────────────────┘
                                                       │
                                                       ▼
                                  ┌──────────────────────────────────────────────┐
                                  │           PubSubAdapter.Subscribe            │
                                  │                                              │
                                  │  1. Looks up HubConfig from Parameter Store  │
                                  │  2. Calls AuthorizationService               │
                                  │  3. Iterates eligible channels               │
                                  │  4. Adds connection to SignalR groups         │
                                  │  5. Fire-and-forget lookback replay          │
                                  └────────────────────┬─────────────────────────┘
                                                       │
                                                       ▼
                                  ┌──────────────────────────────────────────────┐
                                  │     AuthorizationService                     │
                                  │                                              │
                                  │  1. Gets user's product entitlements         │
                                  │     (e.g., Products: ["CHLT", "Sfc"])        │
                                  │  2. Converts to MessageScopes                │
                                  │  3. For each matching ChannelConfig:         │
                                  │     BuildEligibleChannelNames(scopes)        │
                                  │  4. Returns: "News" → ["News-CHLT",         │
                                  │                        "News-Sfc"]           │
                                  └──────────────────────────────────────────────┘
```

### Publish Flow

```
┌────────────────┐      ┌──────────────┐      ┌─────────────┐
│ Domain Service │ ───▶ │ EventBridge  │ ───▶ │  SQS Queue  │
│ (publishes     │      │ (routes by   │      │  (buffered)  │
│  event)        │      │  event type) │      │              │
└────────────────┘      └──────────────┘      └──────┬──────┘
                                                      │
                                                      ▼
                                       ┌──────────────────────────┐
                                       │  QueuedMessagesWorker    │
                                       │  (BackgroundService)     │
                                       │  Polls every 30 seconds  │
                                       └────────────┬─────────────┘
                                                     │
                                                     ▼
                                       ┌──────────────────────────┐
                                       │  PubSubAdapter.Publish   │
                                       │                          │
                                       │  1. Resolve message      │
                                       │     scopes to channels   │
                                       │  2. Save lookback copy   │
                                       │     to DynamoDB (if      │
                                       │     enabled)             │
                                       │  3. Send to each         │
                                       │     SignalR group         │
                                       └──────────────────────────┘
```

When the publish path resolves a message with scopes `["CHLT", "FullAccess"]` against a channel config for "News," it produces the channel names `["News-CHLT", "News-FullAccess"]` and sends the message to those SignalR groups. Users in `"News-Sfc"` never see it because the message's scopes don't include "Sfc."

## The Smart Channel Concept

The core innovation was an indirection layer between client-facing topics and internal SignalR groups. Clients subscribed to topics. The server resolved those topics into scoped channels based on configuration, user entitlements, and message content. Neither subscribers nor publishers needed to know about this resolution; it happened transparently in the adapter layer.

### Configuration-Driven Channel Topology

The entire hub, channel, and filter structure was externalized to AWS Parameter Store as JSON, loaded at service startup. Adding a new topic or changing how channels mapped to products required a configuration change, not a code deployment.

A simplified example of the configuration structure:

```json
{
  "Hubs": [
    {
      "Name": "Content",
      "Type": "PubSub",
      "Channels": [
        {
          "Name": "News-[ScopeValue]",
          "Topic": "News",
          "IsPublishableByUser": false,
          "Filters": [
            { "Type": "Product Codes", "Values": ["*"] }
          ],
          "LookBack": {
            "IsEnabled": true,
            "TtlPeriodType": "CalendarDay",
            "TtlValue": 1
          }
        },
        {
          "Name": "Site Visit Count",
          "Topic": "SiteVisits",
          "IsPublishableByUser": false,
          "Filters": []
        }
      ],
      "FilterCollections": [
        {
          "Name": "AllProducts",
          "Filters": [
            { "Type": "Product Codes", "Values": ["*"] }
          ]
        }
      ]
    }
  ]
}
```

Two patterns are visible here. The "News" channel uses a `[ScopeValue]` placeholder in its name and a wildcard product filter. At runtime, this single configuration entry produces N concrete SignalR groups, one per product code in the subscriber's entitlements or the message's scopes. The "Site Visit Count" channel has no filters, which means it resolves to a single static group that all subscribers and all messages use.

Filter collections provided DRY reuse. A set of filters defined once under `FilterCollections` could be referenced by name from any channel configuration, preventing duplication when multiple channels shared the same product-scoping rules.

### How Channel Resolution Works

The channel resolution algorithm takes a list of scopes (derived from either the user's entitlements or the message's declared audience) and returns the concrete channel names that apply. The logic follows a priority chain:

```
BuildEligibleChannelNames(scopes):

  ┌─ Channel has no filters?
  │   YES → Return static channel name (replace [ScopeValue] with "*")
  │          Everyone gets the same channel.
  │
  ├─ Scopes contain Product Codes?
  │   YES → Check channel's product filter:
  │          ┌─ Filter is wildcard ("*")?
  │          │   → Every product code in scope becomes its own channel
  │          │     e.g., ["CHLT", "Sfc"] → ["News-CHLT", "News-Sfc"]
  │          │
  │          └─ Filter has specific values?
  │              → Only matching product codes become channels
  │              e.g., filter ["CHLT"], scope ["CHLT", "Sfc"] → ["News-CHLT"]
  │
  └─ No product match? Fall through to Feature Names
      → Same matching logic against feature name filters
      → Return matching feature-based channel names
```

The `[ScopeValue]` placeholder in the channel name template gets replaced with each concrete value during resolution. When a wildcard filter is present, every value in the scope produces its own channel. When specific values are listed, only matching values produce channels. This gave the configuration author precise control over how fine-grained the routing was per topic.

### A Concrete Example

Consider two users and one published message:

**User A** has products `["CHLT", "Sfc"]`. When User A subscribes to "News," the authorization service resolves their entitlements into scopes, and the channel config produces `["News-CHLT", "News-Sfc"]`. User A's connection joins both SignalR groups.

**User B** has products `["FullAccess"]`. The same subscription request produces `["News-FullAccess"]`. User B joins one group.

**A message arrives** with topic "News" and scopes `[{ Type: "Product Codes", Values: ["CHLT", "FullAccess"] }]`. The publish path resolves this to channel names `["News-CHLT", "News-FullAccess"]` and sends the message to both groups.

User A receives the message because they are in `"News-CHLT"`. User B receives it because they are in `"News-FullAccess"`. If a third user had only product "Sfc," they would not receive this message because "Sfc" is not in the message's scopes. The client never needed to know about any of this filtering. It subscribed to "News" and received relevant news.

```
Subscribe Resolution:
                                    ┌─── News-CHLT  ◄── User A
  User A (CHLT, Sfc)               │
  subscribes to "News" ──────────▶ ├─── News-Sfc   ◄── User A
                                    │
  User B (FullAccess)               │
  subscribes to "News" ──────────▶ └─── News-FullAccess ◄── User B

Publish Resolution:

  Message: Topic="News"
  Scopes: ["CHLT", "FullAccess"]
           │
           ├──▶ News-CHLT       → User A receives ✓
           ├──▶ News-FullAccess  → User B receives ✓
           │
           └──▶ News-Sfc        → not targeted (Sfc not in message scopes)
```

### Symmetry Between Subscribe and Publish

Both paths used the same channel resolution logic, which was a deliberate design choice. On subscribe, the user's entitlements became the scopes. On publish, the message's declared audience became the scopes. The same resolution applied in both directions, which meant the system was self-consistent: any channel a user was placed into could also be targeted by a message, and any channel a message was sent to would only contain users who were entitled to receive it.

The authorization service bridged user identity and message scopes by looking up the user's product and feature entitlements from the existing authorization infrastructure and converting them into the same `MessageScope` format that published messages used. This translation happened once per subscribe call. Because the authorization service was an existing platform component, the SignalR service didn't need to duplicate any entitlement logic.

## The Lookback Pattern

WebSocket connections are ephemeral. A user might connect to the application after a message was published, or their connection might drop and reconnect. Without a catch-up mechanism, those users would miss messages that arrived while they were disconnected.

The lookback pattern solved this by persisting recent messages to DynamoDB with configurable TTLs and replaying them to new connections during the subscribe handshake.

### How Lookback Works

Each channel configuration had an optional lookback setting with three properties: whether lookback was enabled, the TTL period type (either calendar day or minutes), and the TTL value. A calendar day TTL of 1 meant the message expired at midnight the following day. A minutes TTL of 60 meant the message expired one hour after creation. DynamoDB's native TTL feature handled the cleanup automatically.

```
Lookback Save (on publish):

  Message published to lookback-enabled channel
           │
           ▼
  ┌────────────────────────────────────────────┐
  │  Is lookback enabled for this channel?      │
  │                                             │
  │  YES → Stamp message with eligible channels │
  │         Compute TTL from config:            │
  │         ┌─ CalendarDay? → midnight + N days │
  │         └─ Minutes?     → now + N minutes   │
  │         Save to DynamoDB with TTL           │
  │                                             │
  │  NO  → Skip (message is ephemeral)         │
  └────────────────────────────────────────────┘
```

Each persisted message included an eligible channels array that recorded which specific channel names the message was published to. This was important for the replay step: when a new connection subscribed, the lookback query needed to know which of the user's channels each message belonged to, since a single topic might have multiple channel names and the user might only be in some of them.

### Replay on Subscribe

After a user's connection was added to its eligible SignalR groups, the adapter fired a lookback replay as a fire-and-forget operation so it wouldn't block the subscribe response.

```
Lookback Replay (on subscribe):

  For each lookback-enabled channel the user subscribed to:
           │
           ▼
  ┌─────────────────────────────────────────────────────┐
  │  Query DynamoDB for non-expired messages by topic    │
  │                                                      │
  │  Track sent message UUIDs (deduplication set)        │
  │                                                      │
  │  For each of the user's eligible channel names:      │
  │    Filter saved messages where:                      │
  │      - message's eligible channels include this one  │
  │      - message UUID not already sent                 │
  │                                                      │
  │    Send each matching message directly to            │
  │    this specific connection (not the group)          │
  │                                                      │
  │    Add UUID to deduplication set                     │
  └─────────────────────────────────────────────────────┘
```

The deduplication set prevented duplicate delivery. If a message was eligible for multiple channels that the user subscribed to (for example, a message scoped to both "CHLT" and "Sfc" for a user with both products), the UUID check ensured the user received it only once.

### DynamoDB as the Lookback Store

The lookback table used `Topic` as the hash key and `CreatedAt` as the range key, with PAY_PER_REQUEST billing. This was a deliberately simple model. Lookback queries always filtered by topic, and the range key provided chronological ordering within each topic's partition.

```
Table: messagehub-pubsub-messages
Billing: PAY_PER_REQUEST

┌────────────────┬──────────────┬─────────────────────────────┐
│ Topic (HASH)   │ CreatedAt    │ Attributes                  │
│                │ (RANGE)      │                             │
├────────────────┼──────────────┼─────────────────────────────┤
│ "News"         │ 2025-03-15.. │ UUID, Message, Scopes,      │
│ "Alerts"       │ 2025-03-15.. │ EligibleChannels, DynamoTTL │
└────────────────┴──────────────┴─────────────────────────────┘
```

PAY_PER_REQUEST billing meant the lookback store cost nearly nothing during quiet periods and scaled automatically during spikes. The TTL-based expiration meant no cleanup jobs were needed; DynamoDB handled garbage collection natively.

## Message Ingestion Pipeline

Messages reached the SignalR service through an event-driven pipeline. Internal domain services published events to AWS EventBridge, which routed them by event type to an SQS queue. A background worker within the SignalR service consumed the queue and passed messages through the adapter layer.

### The Worker

The worker ran as a .NET `BackgroundService` co-located with the API in the same ECS container. It started two consumers in parallel: one for the main queue polling every 30 seconds, and one for the dead letter queue polling every 30 minutes. Both consumers used the same message processor; the only difference was the polling interval and queue name.

```
┌──────────────────────────────────────────────────────────┐
│                   QueuedMessagesWorker                     │
│                   (BackgroundService)                      │
│                                                           │
│   ┌─────────────────────┐    ┌─────────────────────────┐  │
│   │   Main Consumer     │    │    DLQ Consumer          │  │
│   │   Poll: 30 seconds  │    │    Poll: 30 minutes      │  │
│   │   Queue: pubsub-    │    │    Queue: pubsub-        │  │
│   │     messagepublished│    │     messagepublished-dlq  │  │
│   └─────────┬───────────┘    └───────────┬──────────────┘  │
│             │                             │                 │
│             └──────────┬──────────────────┘                 │
│                        ▼                                    │
│           ┌────────────────────────┐                        │
│           │  Message Processor     │                        │
│           │                        │                        │
│           │  Deserialize event  →  │                        │
│           │  Extract message   →   │                        │
│           │  PubSubAdapter.Publish │                        │
│           └────────────────────────┘                        │
└──────────────────────────────────────────────────────────┘
```

The consumer pipeline handled retries and dead-lettering automatically. If a message failed processing, SQS retained it for retry up to a configurable maximum of 3 attempts with a 30-second visibility timeout. After exhausting retries, the message moved to the DLQ where the slower consumer would attempt reprocessing on a 30-minute cycle, serving as a safety net for transient infrastructure failures.

### Co-located Processing

The worker ran inside the same ECS container as the API, not as a separate service. The organization had a well-established pattern of extracting background processing into dedicated worker nodes when internal overhead competed with public endpoint performance. Several other services in the platform followed that extraction pattern. In this case, the API was lightweight enough that the processing overhead posed no measurable contention, so the team avoided the operational cost of a separate deployment. The extraction path was proven and straightforward if processing ever needed its own scaling profile.

## Infrastructure Decisions

WebSocket connections impose infrastructure requirements that standard HTTP APIs don't. The team made several deliberate choices to support persistent connections reliably.

### Dedicated Load Balancer and Cluster

WebSocket connections require sticky sessions at the load balancer level. A client's connection must consistently route to the same backend instance for the lifetime of that connection. This meant the SignalR service couldn't share an Application Load Balancer with other HTTP services that used round-robin routing. Each environment got its own ALB and ECS cluster dedicated to the SignalR service.

This is a fundamental requirement of WebSocket infrastructure, not a cost of the custom approach specifically. The connection lifecycle of a persistent WebSocket is incompatible with the request-response lifecycle of a standard HTTP API. Any WebSocket-based solution (custom or managed) would have required the team to operate dedicated infrastructure for the connection layer, or pay a vendor to operate it. The team chose to operate it themselves on infrastructure they already understood.

### Transport and Protocol

The client connected with WebSocket-only transport, bypassing SignalR's default HTTP negotiation handshake. This eliminated an extra round trip on connection establishment at the cost of falling back to long polling if WebSockets were unavailable. Since the dedicated ALB was configured specifically for WebSocket support, the fallback scenario was not a concern.

Messages used MessagePack binary serialization over the WebSocket connection. Compared to JSON, MessagePack produces smaller payloads and faster serialization, which mattered for a connection that might deliver dozens of messages per minute for active topics.

### Client Resilience

The client implemented a custom retry policy with linear backoff: 1 second for the first retry, increasing by 1 second each attempt, capped at 30 seconds. The policy retried indefinitely, never giving up on reconnection. On successful reconnection, the client automatically re-invoked the subscribe method to rejoin SignalR groups and trigger lookback replay. This made connection drops transparent to the user: the client reconnected, resubscribed, received any missed messages through lookback, and continued receiving live updates.

```
Connection Resilience:

  Connection drops
       │
       ▼
  Retry with linear backoff (1s, 2s, 3s, ... 30s cap)
       │
       ▼
  Reconnected
       │
       ▼
  Auto-resubscribe to all topics
       │
       ├──▶ Rejoin SignalR groups
       └──▶ Lookback replays missed messages
```

### Authentication

JWT tokens were passed on the initial WebSocket connection via an access token factory callback. The SignalR hub's subscribe method was protected by an authorization policy ensuring only authenticated users with the correct role could subscribe to topics. The authorization check happened once per hub method invocation, not per message delivery, so it didn't add latency to the real-time push path.

## Design Decisions Worth Noting

### Thin Hub, Fat Adapter

The SignalR hub itself contained exactly one method: `Subscribe`. It extracted the authenticated principal from the connection context, forwarded the requested topics and connection ID to the adapter, and returned. All business logic (channel resolution, lookback, authorization) lived in the `PubSubAdapter`. This separation meant the adapter could be tested independently of SignalR's connection infrastructure, and the same adapter logic could serve both the hub's subscribe path and the SQS worker's publish path.

### HubFacade Abstraction

The adapter didn't interact with SignalR's `IHubContext` directly. Instead, a facade wrapped hub contexts in a dictionary keyed by hub name, providing methods like `PublishToChannel`, `PublishToConnection`, and `Subscribe`. This indirection made the adapter hub-agnostic. If the platform later needed a second hub type (for example, a separate admin notification hub with different authorization rules), the facade could support it without changing the adapter's publish or subscribe logic.

### IsPublishableByUser Gate

Each channel configuration included an `IsPublishableByUser` flag. When a message came from a user through the authenticated publish path, the authorization service filtered out channels where this flag was false. When a message came from the SQS worker as an internal system message, the flag was ignored. This created a clean separation between channels that accepted user-generated content and channels that were strictly server-to-client.

### Configuration Over Code

The hub, channel, and filter topology was entirely externalized to AWS Parameter Store. Adding a new alert type, creating a new product-scoped channel, or changing the lookback TTL for a topic required updating a JSON configuration document, not deploying code. Filter collections provided reuse: a common set of product filters defined once could be referenced by name from any number of channel configurations.

This was valuable in practice because the product team frequently wanted to add new notification types as they launched new features. Being able to add those through configuration rather than code deployments shortened the turnaround from days to minutes.

## What Actually Happened

The POC worked. The architecture was sound, the channel resolution performed well at moderate scale, the lookback pattern handled reconnection gracefully, and the configuration-driven topology made it easy to add new topics without code changes. As a proof-of-concept, it validated that the pattern was viable.

It never shipped to production.

While the POC was being built, the team found ways to improve the web application's data loading patterns through better lazy loading and caching strategies. The content that had been slow to load (and that motivated the push for real-time updates) became fast enough through smarter client-side data fetching that the urgency for WebSocket push evaporated. The polling-based approach, combined with better caching, delivered an acceptable user experience without the infrastructure complexity that WebSockets would have introduced.

The real-time push feature was deprioritized, and the POC sat on the shelf.

## Honest Retrospective

### Was the architecture good?

Yes. The smart channel concept, where client-facing topics resolve to product-scoped SignalR groups through configuration-driven filters, is a clean pattern. The symmetry between subscribe and publish resolution, where both paths use the same scope-matching logic, made the system self-consistent and easy to reason about. The lookback pattern solved a real problem with WebSocket ephemerality. The thin hub, fat adapter separation made the business logic testable independent of SignalR's connection infrastructure. These are patterns worth documenting and reusing.

### Was building it the right call?

The infrastructure itself was not the problem. A dedicated ALB, ECS cluster, DynamoDB table, SQS queue, and EventBridge rule are standard components for a WebSocket service on AWS, and the operational cost of running them was modest. The team already operated similar infrastructure for other services. The real question is whether the feature justified any investment at all, custom or managed, given that the underlying problem turned out to be solvable without real-time push.

The team's justification for building custom was that "context drives product behavior and no managed service handles that." That argument has merit but also has limits. The context-driven routing logic (looking up entitlements and resolving them into scoped channels) is about 50 lines of logic that would exist regardless of whether it lives in a SignalR adapter, a Pusher authorization callback, or an Ably token request handler. Where the approaches diverge is in the surrounding infrastructure: connection lifecycle management, message persistence, retry handling, and monitoring. The custom approach gave the team full control over latency, cost scaling, and operational behavior. A managed service would have shifted that operational burden to a vendor, at the cost of per-connection pricing, authorization callback latency, and less control over the stack.

Either approach could have been defensible. The less defensible part was investing in either one before validating that the users actually needed real-time push.

### What should have happened instead?

Two things were missing from the process.

First, the requirement should have been validated before the infrastructure was built. The question wasn't "can we build real-time push with product-scoped routing?" It was "do our users actually need real-time push, or is the problem solvable with better data loading?" The answer turned out to be the latter, and the team discovered that through parallel work on caching, not through deliberate validation of the push requirement. If the team had invested a sprint in lazy loading improvements first, the real-time push work might never have started.

Second, the buy-vs-build evaluation should have included managed real-time services, not just AWS primitives. Evaluating API Gateway WebSockets and SNS was evaluating the wrong competition. Pusher, Ably, and AWS IoT Core are purpose-built for the "subscribe to a topic, let the server route based on context" pattern. The team might have still chosen to build custom after evaluating those options. The in-process authorization path, the PAY_PER_REQUEST cost model, and the full operational control are legitimate advantages. But that should have been a deliberate tradeoff decision with numbers attached, not a default that happened because the team never looked beyond AWS primitives.

### What made it a worthwhile exercise anyway?

The POC validated architectural patterns that apply beyond this specific use case. The configuration-driven channel topology, the scope-based resolution algorithm, and the lookback replay pattern are reusable ideas. Building the POC also forced the team to think carefully about WebSocket infrastructure requirements like sticky sessions, reconnection handling, and connection-scoped state, knowledge that informed later infrastructure decisions even though this particular service didn't ship.

It was a well-built solution to a problem that didn't need solving yet. The build-vs-buy question is genuinely close for this use case, with real advantages on both sides. But the more important question was never asked: does the problem exist? Good engineering applied to an unvalidated requirement is still wasted effort, regardless of whether the implementation is custom or off-the-shelf.
