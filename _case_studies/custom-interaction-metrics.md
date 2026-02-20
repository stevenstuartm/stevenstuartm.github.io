---
layout: case-study
title: "When Your Product Outgrows Generic Metrics"
subtitle: "A lightweight, purpose-built solution for tracking product engagement when off-the-shelf tools don't fit"
description: "When existing analytics platforms couldn't support rich user context for paid content, a custom dual-storage metrics pipeline was built using DynamoDB for ingestion and MySQL for aggregated summaries, with configurable time-decay scoring."
role: "System Architect"
date: 2025-01-01
headline_metric: "Custom Metrics Pipeline"
headline_detail: "DynamoDB queue → background processor → MySQL summaries"
category: "technical"
category_label: "Technical Deep-Dive"
technologies:
  - .NET
  - AWS DynamoDB
  - AWS Aurora (MySQL)
  - AWS ECS
  - HotChocolate (GraphQL)
---

## The Problem

The platform served approximately 120,000 users across multiple applications, offering paid content products that users subscribed to and consumed over time. The business had three concrete needs that no existing component could serve.

First, the organization needed to understand which content, products, and pages were most effective. Without interaction data, content strategy was guesswork. The team needed to know what users actually engaged with so they could invest in the content that drove value and deprecate what didn't.

Second, marketing needed per-user topic interest profiles. Understanding which subjects each user gravitated toward allowed targeted campaigns and personalized outreach. Generic aggregate metrics couldn't distinguish between a user interested in Topic A and a user interested in Topic B; both looked the same in a page-view count.

Third, and most ambitiously, the product team wanted to present more relevant content to users in real-time based on detected engagement patterns. The concept was similar to how Amazon surfaces recommendations: once sufficient engagement bias exists for a user, the product should reflect that bias by presenting the most relevant content first. This required not just tracking what users did, but computing weighted engagement scores that the client application could consume on each request, at a rate that was acceptable to both system availability and user experience.

This was not a web analytics problem. Standard analytics tools answer questions about aggregate traffic patterns and conversion funnels for public content. The questions here required per-user, per-product tracking of authenticated sessions against specific content items within a paid ecosystem.

No existing API in the system was suitable for managing application-specific activity, metadata, or user interaction history. The concerns were cohesive enough that splitting them across existing services would have created coupling that made no architectural sense. A new component was needed to represent these concerns together.

## Why Not Off-the-Shelf?

Before building anything custom, the team evaluated several existing solutions. Each was rejected for specific, defensible reasons.

### Google Analytics

Google Analytics is designed to answer "how are people finding us and what content performs." It is not designed to answer "how is user X progressing through our product over time." GA does not support the degree of per-user context required for tracking customer-specific content consumption and interest within a paid product.

Metrics like "time on page" are built for measuring public engagement with free content. For paid content where the business context matters more than the traffic source, those metrics don't translate to business value. A user spending 30 minutes on a page might indicate deep engagement or they might have left the tab open. In a paid content context, the distinction matters, and GA can't make it.

### Third-Party Analytics SDKs

The client-side resource consumption on the primary site was already staggering. The browser was overloaded with API calls, scripts, and third-party integrations. Adding another tracking SDK would have made that problem worse.

The platform also relied heavily on client-side caching to reduce network and server costs. A third-party solution that depended on server-side tracking would not have worked with the lazy caching strategy already in place. Every additional client-side dependency carried real performance cost, and the team had previously made a deliberate decision not to add generic "always on" tracking for exactly this reason.

### Full Analytics Platforms

Platforms like Mixpanel and Amplitude provide rich user-level analytics, but they come with significant cost and commitment. The full scope of what the organization needed was not yet clear. Committing to a vendor contract before understanding the actual requirements would have meant paying for capabilities that might never be used, or worse, discovering that the chosen platform didn't support a critical use case after the contract was signed.

Cost was a persistent constraint across all technology decisions at this organization. The more complete third-party solutions were far too expensive for what was actually needed at that stage.

### The Custom Investment Tradeoff

A small custom solution offered the right balance: low cost, development agility, and the ability to discover requirements organically before committing to a vendor. If the requirements eventually grew beyond what it could support, the team was willing to evaluate a more mature platform, but the path to that migration would not have been trivial. Everything was consolidated in a single API, and all marketing and product consumers accessed insights through that API rather than querying the database directly. The data warehouse summaries flowing to QuickSight via Snowflake were more of a short-term convenience for reporting than a core architectural commitment. Building custom first meant the organization could learn what it actually needed with a minimal investment, rather than guessing at requirements and hoping a vendor's feature set happened to align.

## Solution Architecture

The system was designed as a three-layer pipeline: lightweight ingestion into a transient queue, background batch processing into durable summaries, and a query layer that computed weighted engagement scores on read.

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Applications                        │
│              (Authenticated users + anonymous visitors)            │
└───────────────────────────┬──────────────────────────────────────┘
                            │
                      REST API calls
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                         UX API Service                            │
│                        (.NET on ECS)                              │
│                                                                   │
│   POST /ux/user/appaction      POST /ux/appaction                 │
│   (authenticated users)        (anonymous, rate-limited)          │
│                                                                   │
│   POST /ux/user/actions/gettopicvaluefrequency                    │
│   (weighted frequency query)                                      │
│                                                                   │
│   GraphQL /graphql                                                │
│   (application alerts, cached)                                    │
└───────┬───────────────────────────────────────┬──────────────────┘
        │                                       │
        │  write (fire-and-forget)              │  read/write
        ▼                                       ▼
┌──────────────────┐                ┌─────────────────────────┐
│  AWS DynamoDB    │                │    AWS Aurora (MySQL)    │
│                  │   background   │                         │
│  Ingestion Queue │──processing──▶ │  Actors                 │
│  (transient)     │   (interval)   │  Actor Claims           │
│                  │                │  Action History Periods  │
│  PAY_PER_REQUEST │                │  Action History Summary  │
└──────────────────┘                └─────────────────────────┘
```

The ingestion layer writes raw events to DynamoDB as fast as they arrive. A background processor running on a configurable interval (default: 10 minutes) scans the queue, aggregates events by actor, topic, scope, and application, then upserts summary records into MySQL. The query layer reads those summaries and computes time-decay weighted frequency scores to rank content by engagement.

## Data Model

### DynamoDB: Ingestion Queue

The `ux_queuedactionhistory` table in DynamoDB served as a transient write-ahead queue. Events landed here immediately on ingestion and were deleted after processing.

```
Table: ux_queuedactionhistory
Billing: PAY_PER_REQUEST

┌────────────────┬──────────────┬─────────────────────────────────────┐
│ Actor (HASH)   │ OccurredAt   │ Attributes                          │
│                │ (RANGE)      │                                     │
├────────────────┼──────────────┼─────────────────────────────────────┤
│ "1|user-uuid"  │ 2024-03-15.. │ ActorValue, ActorTypeId, ActionId,  │
│ "2|192.168.1.1"│ 2024-03-15.. │ ApplicationId, Topic, ActorClaims,  │
│                │              │ ScopeTopic, ScopeValue              │
└────────────────┴──────────────┴─────────────────────────────────────┘

Hash Key:  Actor     — composite "{TypeId}|{Value}" (e.g., "1|user-uuid")
Range Key: OccurredAt — UTC timestamp for ordering within an actor
```

The composite hash key pattern (`{TypeId}|{Value}`) allowed efficient queries for all events belonging to a specific actor. The range key on `OccurredAt` provided chronological ordering within each actor's partition, which the processor used to determine the latest occurrence timestamps for summaries.

PAY_PER_REQUEST billing meant the queue cost nearly nothing during low-activity periods and scaled automatically during spikes without capacity planning.

### MySQL: Durable Summary Storage

Four tables in Aurora MySQL stored the processed and aggregated data.

**Actors**

```sql
CREATE TABLE ux_actors (
   Id       bigint       NOT NULL AUTO_INCREMENT,
   Value    varchar(100) NOT NULL,
   TypeId   smallint     NOT NULL,
   PRIMARY KEY (Id),
   INDEX Idx_ux_actors_Key (Value),
   CONSTRAINT UC_Value_Type UNIQUE (Value, TypeId)
);
```

The actor table abstracted identity. A `TypeId` of 1 represented an authenticated user (identified by user ID), while a `TypeId` of 2 represented an anonymous visitor (identified by IP address). This abstraction allowed the entire pipeline to handle both actor types uniformly without branching logic throughout the codebase.

**Actor Claims**

```sql
CREATE TABLE ux_actorclaims (
   Id          bigint       NOT NULL AUTO_INCREMENT,
   ActorId     bigint       NOT NULL,
   Value       varchar(100) NOT NULL,
   TypeId      smallint     NOT NULL,
   FirstUsedOn DateTime     NOT NULL,
   LastUsedOn  DateTime     NOT NULL,
   PRIMARY KEY (Id),
   INDEX Idx_ux_actorclaims_ActorId (ActorId),
   CONSTRAINT FK_ActorClaim_Actor FOREIGN KEY (ActorId) REFERENCES ux_actors(Id),
   CONSTRAINT UC_Actor_Value_Type UNIQUE (ActorId, Value, TypeId)
);
```

Claims enriched actor records with additional identity signals like IP addresses and email addresses. The `FirstUsedOn` and `LastUsedOn` timestamps tracked when each claim was first and most recently associated with an actor, providing a lightweight identity timeline without storing every individual event.

**Action History Periods**

```sql
CREATE TABLE ux_actionhistoryperiods (
   Id             bigint      NOT NULL AUTO_INCREMENT,
   ActorId        bigint      NOT NULL,
   Topic          varchar(50) NOT NULL,
   PeriodStartsOn DateTime    NOT NULL,
   PeriodEndsOn   DateTime    NOT NULL,
   IsClosed       Boolean     NOT NULL,
   PRIMARY KEY (Id),
   INDEX Idx_ux_actionhistoryperiods_ActorId (ActorId),
   CONSTRAINT UC_Actor_Topic_Period UNIQUE (ActorId, Topic, PeriodStartsOn)
);
```

Periods defined configurable rolling time windows per actor per topic. The default period was 30 days, but each topic could have its own period length via configuration stored in AWS Parameter Store. When a period expired, the processor closed it and created a new one. The scoring algorithm used the two most recent periods (current and previous) to compute time-decay weighted frequencies.

**Action History Summaries**

```sql
CREATE TABLE ux_actionhistorysummaries (
   Id                     bigint      NOT NULL AUTO_INCREMENT,
   ActionHistoryPeriodId  bigint      NOT NULL,
   ApplicationId          varchar(50) NULL,
   ScopeTopic             varchar(50) NULL,
   ScopeValue             varchar(50) NULL,
   ActionTotal            int         NOT NULL,
   LatestOccurrenceAt     DateTime    NOT NULL,
   FirstOccurrenceAt      DateTime    NOT NULL,
   PRIMARY KEY (Id),
   CONSTRAINT FK_ActionHistorySummary_ActionHistoryPeriod
       FOREIGN KEY (ActionHistoryPeriodId) REFERENCES ux_actionhistoryperiods(Id),
   CONSTRAINT UC_Period_App_Topic_Value
       UNIQUE (ActionHistoryPeriodId, ApplicationId, ScopeTopic, ScopeValue)
);
```

Summaries aggregated event counts per period, per application, per scope. The unique constraint on `(ActionHistoryPeriodId, ApplicationId, ScopeTopic, ScopeValue)` ensured upsert behavior: new events incremented existing totals rather than creating duplicate rows. `FirstOccurrenceAt` and `LatestOccurrenceAt` tracked when engagement started and when it was most recent within each period.

### Entity Relationships

```
┌──────────────┐       ┌──────────────────┐
│  ux_actors   │       │ ux_actorclaims   │
│              │1    * │                  │
│  Id (PK)     ├───────│  ActorId (FK)    │
│  Value       │       │  Value           │
│  TypeId      │       │  TypeId          │
│              │       │  FirstUsedOn     │
│              │       │  LastUsedOn      │
└──────┬───────┘       └──────────────────┘
       │
       │ 1
       │
       │ *
┌──────┴───────────────────┐       ┌──────────────────────────────┐
│ ux_actionhistoryperiods  │       │ ux_actionhistorysummaries    │
│                          │1    * │                              │
│  Id (PK)                 ├───────│  ActionHistoryPeriodId (FK)  │
│  ActorId (FK)            │       │  ApplicationId               │
│  Topic                   │       │  ScopeTopic                  │
│  PeriodStartsOn          │       │  ScopeValue                  │
│  PeriodEndsOn            │       │  ActionTotal                 │
│  IsClosed                │       │  LatestOccurrenceAt          │
│                          │       │  FirstOccurrenceAt           │
└──────────────────────────┘       └──────────────────────────────┘
```

## The Ingestion Layer

The API exposed two endpoints for recording actions. Authenticated users submitted through `POST /ux/user/appaction`, which extracted identity from the JWT token and associated the action with a known user. Anonymous visitors submitted through `POST /ux/appaction`, which required an explicit application ID and used the caller's IP address as the actor identity.

Both endpoints followed the same pattern: sanitize input, extract the IP address, enforce rate limits, then write one or more `QueuedActionHistory` records to DynamoDB. Each action carried a `Topic` (the category of interaction) and optional `Scopes` (specific content items within that topic). If an action included multiple scopes, the API wrote one DynamoDB record per scope, all sharing the same `ActionId` to maintain the association.

```csharp
// Each scope generates its own queued record, linked by ActionId
foreach (var scope in request.Scopes)
{
    var queuedAction = QueuedActionHistory.CreateUserAction(
        principal, actionId, request.Topic, now, actorClaims, scope);
    await _queuedActionRepository.Save(queuedAction);
}
```

Rate limiting for anonymous actions used a sliding window of 5 requests per minute per IP address, enforced through a shared rate limiting service backed by a distributed cache. This prevented abuse without blocking legitimate anonymous tracking like UTM click attribution.

The `Topic` and `Scope` model was deliberately generic. A topic might represent a category of content, while scope values within that topic might represent individual content items. This schema-free approach meant the system could track new types of interactions by sending new topic/scope combinations from the client, without any backend changes.

## The Processing Pipeline

The `QueuedActionsProcessor` ran as a .NET `BackgroundService` within the same ECS container as the API. On a configurable interval (default: 10 minutes), it scanned the DynamoDB queue and aggregated events into MySQL summaries.

```
Processing Flow:

1. Scan DynamoDB for distinct actor hashes
                    │
2. For each actor:  │
   ┌────────────────▼────────────────────────────┐
   │  Check rate limit (actor lock)               │
   │  If locked → skip (another instance owns it) │
   └────────────────┬────────────────────────────┘
                    │
   ┌────────────────▼────────────────┐
   │  Fetch all queued actions       │
   │  for this actor from DynamoDB   │
   └────────────────┬────────────────┘
                    │
   ┌────────────────▼────────────────┐
   │  Upsert Actor record in MySQL   │
   │  Update claims if changed       │
   └────────────────┬────────────────┘
                    │
   ┌────────────────▼─────────────────────────────┐
   │  Group actions by Topic                       │
   │    └─ Group by (ScopeTopic, ScopeValue)       │
   │         └─ Group by ApplicationId             │
   │              └─ Count total, track timestamps  │
   │              └─ Upsert ActionHistorySummary   │
   │              └─ Delete processed from DynamoDB │
   └───────────────────────────────────────────────┘
```

### Actor Locking

The processor used the same distributed rate limiting service as the API to implement actor-level locks. Before processing an actor's events, it checked whether that actor was already locked by another instance. This allowed the service to scale horizontally without duplicate processing and without needing a dedicated distributed lock service.

```csharp
// A simple way to allow for scaling the consumer and
// to not have duplicate processing or to give preference
// to "noisy" users.
var hasExceededRateLimit = await _rateLimitService
    .HasExceededStaticRateLimit(
        RateLimitActor, ActorLockTopic,
        ActorLockWindow, ActorLockLimit, actorHash);

if (hasExceededRateLimit)
    continue;
```

The lock window was configurable independently from the processing interval, allowing the team to tune processing frequency and lock duration for different environments.

### Period Management

Each actor's actions within a topic were organized into time-bounded periods. When the processor encountered actions for an actor/topic combination, it checked for an active (non-closed) period. If no active period existed or the current period had expired, the processor closed the old period and created a new one.

Period length was configurable per topic through AWS Parameter Store, with a default of 30 days. A topic with short-lived engagement patterns could use a 7-day period, while a topic tracking long-term content progression could use 90 days.

```csharp
var topicMetricSettings = _appMetricsConfiguration
    .Settings.FindTopicMetricSettings(topic);

var activeActionPeriod = new ActionHistoryPeriod()
{
    ActorId = actorId,
    Topic = topic,
    PeriodStartsOn = DateTime.UtcNow.Date,
    PeriodEndsOn = DateTime.UtcNow.Date
        .AddDays(topicMetricSettings.PeriodRangeDays),
    IsClosed = false
};
```

### Summary Aggregation

Within each period, the processor maintained one summary record per unique combination of `(ApplicationId, ScopeTopic, ScopeValue)`. New events incremented the existing `ActionTotal` and updated the `LatestOccurrenceAt` timestamp. The unique constraint in MySQL ensured that concurrent processors couldn't create duplicate summaries.

Batch processing also provided a natural deduplication boundary. Because the processor grouped all of an actor's queued events before summarizing, it could count meaningful interactions rather than raw event volume. If a user clicked the same content item 100 times in a minute, those events arrived in DynamoDB as 100 records, but the processor aggregated them into a single count increment per scope value per batch. The grouping by `(ScopeTopic, ScopeValue, ApplicationId)` collapsed noisy bursts into actual engagement signal without requiring any explicit deduplication logic.

After successfully upserting a summary, the processor deleted the corresponding source records from DynamoDB. This kept the queue lean and ensured that events were processed exactly once under normal operation.

## The Scoring Algorithm

The scoring algorithm was the component that connected raw interaction data to the business decisions described earlier. The rankings it produced determined which content to surface more prominently for each user, which product categories a user showed the strongest affinity toward, and where package-level upsell opportunities existed based on demonstrated engagement patterns. Without a scoring layer, the pipeline would have been a data warehouse. With it, the pipeline became a decision engine that the client applications could query on every request.

The query endpoint `POST /ux/user/actions/gettopicvaluefrequency` returned a ranked list of scope values for a given user, topic, and scope topic. The ranking was based on a time-decay weighted frequency that combined the current period's totals with a decaying weight from the previous period.

### How the Weighting Works

The algorithm pulled the two most recent periods for the actor/topic combination: the current (open) period and the previous (closed) period. For each distinct scope value present in either period, it computed a weighted total:

```
previousPeriodWeight = max(0.1, daysRemainingInCurrentPeriod / periodRangeDays)
weightedTotal = (previousPeriodTotal * previousPeriodWeight) + currentPeriodTotal
```

Early in a new period, the previous period's data carries significant weight because `daysRemainingInCurrentPeriod` is close to `periodRangeDays`. As the current period progresses and accumulates its own data, the previous period's influence naturally decays toward its floor of 10%. The floor prevents historical engagement from being completely discarded, which would cause abrupt ranking changes at period boundaries.

### Practical Example

Consider a user on a 30-day period. In the previous period, they engaged heavily with Category A (45 actions) and lightly with Category B (10 actions). In the current period, their interest is shifting: they're slowing down on Category A and picking up Category B. The table below shows how the weighted totals evolve across the full period as the decay takes effect and new actions accumulate.

| Day | Previous Weight | Cat A (prev: 45, current) | Cat A Weighted | Cat B (prev: 10, current) | Cat B Weighted | Leader |
|:---:|:---------------:|:-------------------------:|:--------------:|:-------------------------:|:--------------:|:------:|
| 1   | 0.97            | 0                         | 43.65          | 0                         | 9.70           | A      |
| 5   | 0.83            | 3                         | 40.35          | 12                        | 20.30          | A      |
| 10  | 0.67            | 5                         | 35.15          | 18                        | 24.70          | A      |
| 15  | 0.50            | 7                         | 29.50          | 22                        | 27.00          | A      |
| 20  | 0.33            | 8                         | 22.85          | 26                        | 29.30          | **B**  |
| 25  | 0.17            | 9                         | 16.65          | 30                        | 31.70          | **B**  |
| 30  | 0.10            | 10                        | 14.50          | 33                        | 34.00          | **B**  |

On day 1, the previous period dominates. Category A leads by a wide margin because the user's 45 historical actions carry nearly full weight. By day 15, the gap has narrowed: the previous period's influence has halved, and Category B's growing current activity is closing the distance. By day 20, Category B overtakes Category A. The user's real-time behavior has shifted, and the rankings now reflect that shift.

At the end of the period (day 30), the previous weight hits its floor of 10%. Category A's 45 historical actions contribute only 4.50 to the weighted total, while its 10 current actions carry full weight. The historical signal is still present (it hasn't dropped to zero), but it no longer dominates the ranking. If the user's interest continues to shift in the next period, the transition will be even more pronounced as this period's Category B totals become the new "previous" data.

## Design Decisions Worth Noting

### DynamoDB as the Queue, Not SQS or Kinesis

SQS would have been the conventional choice for a message queue, but the processing pattern needed actor-partitioned access. The processor needed to fetch all events for a specific actor in a single query, group them, and process them as a batch. DynamoDB's hash key partitioning made this access pattern natural: scan for distinct actors, then query each actor's partition for all events.

With SQS, the processor would have needed to consume messages one at a time (or in batches of up to 10), accumulate them in memory grouped by actor, and handle the complexity of visibility timeouts across a potentially large number of in-flight messages. DynamoDB's scan-then-query pattern was simpler and more aligned with the batch processing model. It also meant that noisy bursts from a single user (clicking the same item repeatedly in quick succession) were naturally collapsed during batch aggregation rather than consuming per-message processing overhead.

Kinesis was also considered, primarily because its shard-based architecture provides built-in partitioning and ordering. However, several factors made it a poor fit for this workload.

Kinesis is designed for continuous stream processing where consumers read records sequentially from shards. The processor here ran on a 10-minute interval and needed random access by actor, not sequential consumption of an entire stream. Using Kinesis would have meant either running a continuous consumer (more infrastructure than the workload justified) or reading from checkpoint positions on interval, which requires managing shard iterators and checkpoint state that DynamoDB's simple scan-then-query pattern avoids entirely.

The access pattern mismatch was the larger problem. Even with the actor ID as the Kinesis partition key to co-locate each actor's events on the same shard, the consumer would still need to read the shard sequentially and filter by actor. DynamoDB lets the processor query a single actor's events directly by hash key without consuming unrelated records from the same partition.

Kinesis also charges per shard-hour regardless of throughput, so shards incur cost even during idle periods. At the ingestion rates this system handled, that cost model was wasteful compared to DynamoDB's PAY_PER_REQUEST billing, which scaled to near-zero during low-activity periods and only charged for actual reads and writes. Kinesis sharding would have been justified if the system needed to handle sustained high-throughput ingestion or if multiple independent consumers needed to read the same event stream, but neither applied here.

Finally, Kinesis has a default retention window of 24 hours. If the processor fell behind or experienced an extended outage, events older than the retention window would be lost permanently. DynamoDB items have no retention limit and persist until explicitly deleted, which provided a more forgiving safety net for a batch processor running on interval.

### MySQL for Summaries, Not DynamoDB

While DynamoDB handled ingestion well, the summary queries needed relational capabilities. The scoring algorithm required joining periods with their summaries, filtering by open/closed status, and ordering by multiple attributes. Entity Framework Core provided familiar patterns for these operations, and Aurora MySQL was already in the organization's infrastructure stack.

Storing summaries in DynamoDB would have required denormalization that made the period management logic significantly more complex without any corresponding benefit. The summary read patterns were predictable and low-volume (one query per user per content retrieval), so Aurora's query capabilities were worth the tradeoff against DynamoDB's scalability.

### Background Processing, Not Real-Time

The summaries powered content recommendations and engagement reports, neither of which required sub-second freshness. A 10-minute processing interval meant the data was fresh enough for its consumers while batching writes to MySQL and reducing overall write amplification.

Batching also simplified error handling. If the processor failed mid-batch, the undeleted DynamoDB records would be picked up on the next interval. There was no complex acknowledgment protocol, and the processing was naturally idempotent at the summary level since totals were additive and timestamps tracked maximums.

The processor ran co-located with the API as a `BackgroundService` rather than in a dedicated worker cluster. The organization routinely extracted background processing into separate worker nodes when internal overhead competed with public endpoint performance, but the API in this case was efficient enough that the processing posed no measurable contention. Co-location kept the deployment simple and the infrastructure cost minimal.

### The Actor Abstraction

Using a generic Actor model instead of tying directly to user IDs solved two problems. First, it allowed tracking anonymous visitors (by IP) and authenticated users through the same pipeline without conditional logic. Second, it provided a stable identity layer that the metrics system owned, decoupled from the authentication system's user model.

The claims system attached identity signals like email addresses and IP addresses to actors with timestamps. This created a lightweight identity graph that could connect anonymous pre-login behavior to authenticated post-login behavior when the same IP or email appeared in both contexts.

### The Generic Topic/Scope Model

The most deliberate design choice was keeping the content categorization schema-free. Rather than defining tables for specific content types, the system used a generic `Topic` and `Scope` (with its own `Topic` and `Value`) to represent any categorization hierarchy.

This choice came directly from the reasoning behind building custom in the first place: the team did not yet fully understand the scope of what they needed. A generic model meant the client applications could start tracking new types of interactions by sending new topic/scope combinations, without any backend schema changes, migrations, or deployments. The same pipeline that tracked content views could track feature usage, campaign attribution, or any other interaction category the business discovered it needed.

## What This Enabled

The pipeline addressed each of the three business needs that motivated it, and it did so through two consumption paths: batch reporting via QuickSight and real-time API queries from the client applications.

### Content Effectiveness

Summary data flowed into AWS QuickSight through the existing Snowflake ETL process, giving the content team visibility into which content, products, and pages were actually driving engagement. Aggregated action totals per scope value across all users showed what content performed and what didn't, broken down by application and time period. Content strategy shifted from intuition to data: the team could see which topics users returned to, which content items were consumed once and abandoned, and where engagement dropped off across the product catalog.

### Marketing Intelligence

Per-user engagement profiles gave marketing the topic interest data they needed. By querying a user's weighted frequency scores, marketing could segment users by their demonstrated interests rather than by demographics or purchase history alone. A user with high engagement bias toward a specific content category could receive targeted campaigns for related products. The anonymous action tracking with UTM parameters also connected campaign spend to content engagement without adding client-side tracking scripts, closing the attribution loop between marketing spend and product usage.

### Real-Time Product Personalization

The weighted frequency API endpoint was the most technically impactful consumer of the data. Client applications called `gettopicvaluefrequency` on each authenticated request to retrieve a user's ranked content preferences. The response was a simple ordered list of scope values ranked by engagement bias, which the client used to reorder content presentation. Users who engaged heavily with a particular content category saw that category featured more prominently, similar to how Amazon surfaces product recommendations based on accumulated browsing and purchase behavior.

The time-decay weighting was critical to making this work. Without decay, a user who binge-consumed one category months ago would see stale recommendations forever. With decay, the rankings naturally reflected current interests while retaining enough historical signal to avoid jarring shifts at period boundaries. The 10-minute processing interval meant personalization data was fresh enough to feel responsive without requiring real-time stream processing infrastructure.

All of this was achieved without adding any third-party scripts to the client, without increasing the client-side resource footprint, and at a DynamoDB + Aurora cost that was negligible compared to what a third-party analytics platform would have charged.

## Tradeoffs and Limitations

The solution was explicitly designed as a discovery-phase investment, and it carried tradeoffs that would need to be addressed if the requirements grew substantially.

**Batch latency, not real-time.** The 10-minute processing interval meant engagement data was always slightly stale. For content recommendations and reporting dashboards, this was acceptable. For use cases requiring real-time triggers (like sending a notification immediately when a user completes a content milestone), the architecture would need a streaming layer.

**Summary aggregation loses event-level granularity.** Once events were processed into summaries, the individual event records were deleted from DynamoDB. This meant the system could answer "user X viewed Category A content 45 times in this period" but not "user X viewed item Y at 2:47 PM on March 15th." If event-level analysis became necessary, the processing pipeline would need to archive raw events to S3 before deletion.

**Simple scoring, not behavioral analytics.** The time-decay weighted frequency algorithm was effective for ranking relative engagement but didn't support more sophisticated analysis like session reconstruction, funnel analysis, cohort comparison, or predictive modeling. These were capabilities that a mature analytics platform would provide out of the box.

**Co-located processor, not a dedicated worker.** The processor ran as a background service within the same ECS container as the API. The organization had a well-established pattern of extracting background processing into separate worker nodes in a different cluster when internal overhead competed with the scaling and responsiveness of public-facing endpoints. Several other services in the system used this pattern. In this case, the API was efficient enough that the processing overhead posed no measurable threat to endpoint performance, so there was no reason to pay the operational cost of a separate deployment. If projections ever showed the processing contending with API throughput, the extraction path was already proven and straightforward.

These were known limitations at the time of design. If the business requirements grew significantly, the team was prepared to evaluate a more mature analytics platform, but that migration would not have been a simple swap. The API was the single integration point for all consumers, which contained the blast radius of any future change, but the data warehouse coupling through Snowflake and QuickSight would have required its own migration path. The custom solution was a deliberate investment in discovery, not a permanent architecture, but also not something that could be lifted and replaced without effort.
