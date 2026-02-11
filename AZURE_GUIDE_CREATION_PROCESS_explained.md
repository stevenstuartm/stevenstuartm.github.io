# Azure Guide Creation Process - How It Works and Why

This document explains the reasoning behind the guide creation process for anyone who wants to understand the approach, its tradeoffs, and the alternatives.

---

## What We're Doing

We're creating 61 Azure study guides for a Jekyll-based website. Each guide is a ~500-700 line Markdown file covering an Azure service or service group. The guides follow a strict format with specific front matter fields, section structure, content quality rules, and writing style requirements. They need to be registered in a JSON config file to appear on the website.

## The Default Approach: One Fresh Session Per Guide

The simplest correct approach is to give each guide its own clean session. A new session starts with an empty context, writes one guide, validates it, and ends. No guide ever pays for another guide's context.

### How it works

1. Start a new session
2. Tell it: "Read `AZURE_GUIDE_CREATION_PROCESS.md` and `AZURE_GUIDES_PLAN.md`. Create the next guide in the current phase."
3. The session reads the plan (~50 lines for the relevant phase), reads the template guide (~700 lines for format reference), writes the guide (~600 lines), lints it, updates config and plan
4. Session ends

Total context per guide: ~1,500 lines. This is fixed regardless of whether you're writing guide #20 or guide #61 because each session starts clean.

### Why this is the better default

**It solves the accumulation problem by eliminating it.** The original motivation for parallel agents was that writing multiple guides in one session causes context accumulation: guide 6 pays for guides 1-5 sitting in memory. A fresh session per guide has no accumulation by definition. The problem never arises.

**It's simpler.** No agent orchestration, no model selection logic, no resume-for-validation step, no coordination between background tasks. The process doc, the plan file, and the template guide are the only moving parts. State carries between sessions through the plan file's progress tracking.

**It uses the most capable model throughout.** The session uses whatever model you're running (opus, sonnet, etc.) for both writing and validation. There's no quality compromise from delegating to a cheaper model, no risk of generic recommendations in synthesis-heavy guides, and no need to categorize guides by complexity.

**Validation is straightforward.** The model writes the guide, then validates it in the same context (the content is already there), then runs the linter. No need for a multi-layer validation pipeline across different model tiers.

### Why this is not the better default

**It costs roughly 9x more per guide than the parallel haiku approach.** Each guide consumes ~1,500 lines of tokens at the full model rate. The parallel haiku approach runs most of those tokens at haiku rates (roughly 1/10th to 1/15th the cost) and only uses the expensive model for ~70 lines of coordination per guide. Over 61 guides, this difference is substantial.

**It's slower if you want to do multiple guides per sitting.** Each guide takes 1-3 minutes. If you want to knock out a full phase of 5 guides, that's 5-15 minutes sequentially vs 1-3 minutes with parallel agents. If you're stepping away and letting it run, this doesn't matter. If you're watching it, it does.

**It doesn't scale.** For 61 guides, you need 61 separate sessions (or at least ~12 sessions, one per phase). Each session requires you to initiate it and provide the starting prompt. The parallel approach lets you do an entire phase in one session with one prompt.

### When to use each approach

| Scenario | Better approach |
|----------|----------------|
| Writing 1-2 guides with full attention | Fresh session per guide |
| Working through a phase and stepping away | Fresh session per phase (write guides sequentially within one session, accepting some accumulation) |
| Batch-creating an entire phase quickly | Parallel agents (the process doc approach) |
| Cost is the primary constraint | Parallel haiku agents |
| Simplicity is the primary constraint | Fresh session per guide |
| Quality of synthesis/recommendation sections matters most | Fresh session with the most capable model |

---

## The Optimized Approach: Parallel Agents with Model Selection

This is the approach documented in `AZURE_GUIDE_CREATION_PROCESS.md`. It optimizes for cost and speed at the expense of process complexity.

### Why it exists

Writing 6 guides sequentially in one conversation creates context accumulation: the model processes the entire conversation history on every message, so guide 6 costs far more than guide 1 because guides 1-5 are still in memory. At 61 guides, this becomes prohibitively expensive.

The optimized approach solves this by running each guide in an isolated agent context (no accumulation) and using a cheaper model (haiku) for most guides (lower per-token cost).

### Parallel agents with isolated contexts

Each guide is written by a separate agent that runs in its own context window. The main conversation never sees the full 600 lines of each guide. It only sees the linter output (~5-10 lines) and a front matter spot-check (~10 lines). This cuts the token cost in the main context by roughly 95% per guide.

Agents launch concurrently in a single message, so six guides generate simultaneously instead of sequentially.

### Background vs synchronous agents

Claude Code's Task tool can launch agents in two modes. The choice between them has significant implications for workflow automation.

**Synchronous agents** (no `run_in_background` flag):

Multiple synchronous agents launched in a single message run in parallel and block until all complete. The orchestrator receives all results in one response and can immediately proceed to the next step (validation, linting, etc.) without any user intervention. This is the correct mode for multi-step pipelines where steps depend on each other.

**Background agents** (`run_in_background: true`):

Background agents return immediately with a task ID and output file path. The orchestrator can continue doing other work while they run. However, the orchestrator cannot automatically detect when a background agent completes and take action. It can only act when the user sends a message, which means every step transition requires a "continue" prompt from the user. This defeats the purpose of an automated pipeline.

**When to use each mode:**

| Scenario | Mode | Why |
|----------|------|-----|
| Multi-step pipeline (write → validate → lint → update) | Synchronous | Steps chain automatically without user input |
| Long-running task while the user works on something else | Background | User can do other work and check results later |
| Independent tasks with no follow-up steps | Either | No downstream dependencies, so blocking vs non-blocking doesn't matter |
| Tasks where the orchestrator needs results to decide what to do next | Synchronous | The orchestrator needs the result before it can proceed |

**The key tradeoff**: Background agents save the user from waiting during long operations, but they break automated pipelines because the orchestrator has no event-driven way to react to completion. Synchronous agents force the user to wait for the response, but the orchestrator can chain an arbitrary number of steps without any user intervention.

For this guide creation process, synchronous is the correct choice. The pipeline has 5 dependent steps, and the user's intent is "run the whole phase" not "start writing and I'll check back later."

### Short prompts with a format reference

Every guide needs the same formatting rules, content quality rules, and structural pattern. Instead of repeating 150 lines of instructions in every agent prompt, the agent is told to read an existing guide file and follow its format. The unique content per prompt is just ~30 lines: the front matter and topic list.

### Self-validation via resume

After an agent writes a guide, the same agent is resumed (it keeps its full context) and asked to verify the content against a checklist. The agent already has the entire guide in its context from writing it, so validation costs only the incremental tokens for the review prompt and any fixes. The alternative would be reading the full file in the main context to validate, which negates most of the savings.

### Automatic model selection

Not all guides require the same level of reasoning. The process automatically selects a cheaper or more capable model based on the guide's characteristics.

**Category A: Single-service descriptive guides (~50 of 61)**

These guides describe what a service is, how it works, its tiers and options, and common pitfalls. The "decisions" are mostly tier selection within a single service. The structure is well-defined and the information is widely available. A cheaper, faster model (haiku) handles these well because the reasoning is one-dimensional: compare options along known axes.

Examples: Azure VMs, Azure Functions, Blob Storage, Azure SQL Database, Key Vault.

**Category B: Cross-service synthesis guides (~8-10 of 61)**

These guides require multi-dimensional reasoning: "if you have THIS consistency requirement AND THIS latency budget AND THIS query pattern, then Cosmos DB wins, but if you also need ad-hoc SQL joins, you're in a tradeoff space where..." A cheaper model tends to flatten these into simpler heuristics ("use Cosmos DB for global distribution, SQL for relational") while a more capable model identifies the non-obvious edge cases and tensions.

Examples: Database Service Selection, Modern Data Architecture, AI/ML Service Selection, Serverless Architecture Patterns, Multi-Region Architecture, Disaster Recovery.

**How it's detected automatically:**

The orchestrator determines which model to use based on signals already present in the plan file:

1. **Title keywords**: "Selection" or "Patterns" (in advanced subcategories) indicate cross-service synthesis
2. **Subcategory placement**: Guides in "Architecture Patterns (Advanced)", "Serverless Architecture", or "Container Orchestration (Advanced)" are cross-cutting by nature
3. **Plan notes**: Notes that mention cross-service composition or decision frameworks spanning multiple services

This isn't perfect. A guide could be miscategorized in either direction. But the cost of getting it wrong is low: a haiku-written synthesis guide might have slightly generic recommendations (easily caught in review), while a sonnet-written descriptive guide just costs more than necessary with no quality downside. The heuristic is more than sufficient for study guides where the structure is well-defined and the plan provides clear metadata.

### Could you verify which model is better?

Yes. The most targeted test would be: pick the hardest upcoming guide (like Database Service Selection, which compares 5 services across multiple dimensions) and generate it with both haiku and sonnet. Compare specifically the decision framework and recommendation sections. If haiku's recommendations feel generic ("use SQL for relational, Cosmos for NoSQL") while sonnet identifies nuanced tradeoffs ("SQL Managed Instance gives you cross-database queries that Cosmos can't, but Cosmos's five consistency levels let you tune the CAP tradeoff per-request"), that confirms the split is worthwhile. If they're comparable, haiku across the board saves cost with no quality loss.

---

## The Validation Pipeline

Both approaches use the same validation checks; they just differ in where the work happens.

### What gets checked

1. **Structural review**: Front matter fields, blockquote pull-quote, AWS comparison table, Common Pitfalls format, Key Takeaways section
2. **Automated linter**: `lint_content.py` catches AI-tell phrases, em-dashes, missing articles, run-on sentences, lazy parentheticals
3. **Front matter spot-check**: Confirm YAML fields are correct (this is the highest-impact check because wrong front matter means the guide won't render on the website)

### How it works in each approach

**Fresh session per guide:** The model writes the guide, validates it in the same context (content already there), runs the linter, fixes violations. All in one session, one model, no coordination.

**Parallel agents:** Layer 1 (structural review) happens in the cheap agent context via resume. Layer 2 (linter) runs as a shell command in the main context with minimal output. Layer 3 (front matter spot-check) reads only 10 lines in the main context. The full guide body never enters the main context.

### Why not just read everything in the main context?

Reading a 600-line file in the main context costs tokens on every subsequent message for the rest of the conversation. If you validate 6 guides by reading them fully, that's 3,600 lines inflating the context for all future work. The three-layer approach catches the same issues at a fraction of the cost by keeping the full content in cheap agent contexts and only surfacing small, targeted signals (linter output, front matter) to the main context.

This concern doesn't apply to the fresh-session approach because each session ends after one guide. There is no "rest of the conversation" to inflate.

---

## All Alternatives at a Glance

### Default: Fresh session per guide

- **Pros**: Simplest, highest quality, no accumulation, no process complexity
- **Cons**: ~9x more expensive per guide than haiku agents, sequential (slower for batch work), requires initiating each session
- **When it makes sense**: When simplicity and quality matter more than cost and speed

### Optimized: Parallel haiku/sonnet agents (the process doc)

- **Pros**: ~9x cheaper, parallel execution, automatic model selection
- **Cons**: Process complexity (agent orchestration, resume, coordination), potential quality tradeoff on synthesis guides
- **When it makes sense**: When doing a full phase in one sitting, or when cost is a constraint

### Write everything in one session sequentially

- **Pros**: Full quality control, no coordination overhead
- **Cons**: Extremely expensive (context accumulation), very slow, context window may fill before finishing a phase
- **When it makes sense**: If you're writing 1-2 guides and want maximum quality within a single session

### Write all guides in one massive prompt

- **Pros**: Theoretically fastest
- **Cons**: Quality degrades badly with very long outputs, no error recovery, can't parallelize
- **When it makes sense**: Never, for content of this length and quality requirement

### No self-validation, just lint and manual review

- **Pros**: Simpler process, fewer round-trips
- **Cons**: More violations survive to manual review, structural issues caught later
- **When it makes sense**: If the linter covers most quality rules you care about (it doesn't catch missing AWS comparison tables or wrong section ordering)

---

## Why These Specific Quality Checks?

The content has strict requirements defined in CLAUDE.md:

- **No CLI commands or code**: These guides teach concepts, not syntax. Syntax goes stale.
- **No dollar amounts**: Azure pricing changes constantly. Relative comparisons ("2x more expensive") survive price changes.
- **No AI-tell phrases**: The site has a specific voice. Phrases like "key insight" or "it's important to note" are obvious AI tells.
- **Blank lines before tables**: Jekyll's Kramdown Markdown parser requires this or tables don't render.
- **Front matter fields**: Missing fields mean the guide won't appear correctly on the website.
- **Config registration**: A guide file without a config entry exists on disk but is invisible on the website.

The linter automates the mechanical checks. The structural review catches content-level issues. The spot-check catches the highest-impact rendering issues. Together they form a quality pipeline that works regardless of which approach you choose.

---

## Parallel Agent Behavior: Throttling, Scaling, and Phasing

### Can parallel agents get throttled by CPU or network?

Each agent is a separate API call to Anthropic's servers. The constraints are:

- **Anthropic rate limits**: Your account has a tokens-per-minute and requests-per-minute cap. 5 parallel haiku agents are well within safe territory. You'd likely start seeing rate limit errors somewhere around 10-15+ concurrent agents, depending on your plan tier.
- **Local machine**: Minimal concern. Agents are I/O-bound (waiting on API responses), not CPU-bound. The local work is just file reads and writes. Your machine won't break a sweat with 5 or even 15 agents.
- **Network**: Each agent streams a response, but the bandwidth is trivial compared to modern connections.

Token cost savings from parallel agents are real, but the savings are in token volume, not in rate limit headroom. Parallel agents don't use fewer tokens per guide; they use cheaper tokens (haiku vs opus) and avoid context accumulation. The parallelism saves wall-clock time, not API capacity.

### Is a single agent better for long-running series of work?

Two separate considerations:

**For a new project (variety of tasks):** One at a time is generally better. Each task might inform the next (you discover a pattern, hit an issue, change your mind). Serial work preserves that feedback loop. Parallel only makes sense when the tasks are truly independent, as they are here because each guide covers a different Azure service with no dependency on the others.

**For 100 guides in a day:** Parallel is actually safer for throughput, not less safe. A single agent can't carry 100 guides in one session because context windows fill up, and each "resume" carries the full prior transcript. By guide 10-15 the agent is sluggish and expensive because it's re-reading everything. Independent agents with short prompts are stateless and cheap. If one fails, you re-run just that one. If a single-agent chain fails at guide 47, you have to figure out where to restart.

The risk with parallelism isn't safety; it's **quality control**. You lose the ability to catch a systemic issue early (like all 5 agents making the same formatting mistake) before it multiplies across all guides. That's what the validation and lint steps are for: they catch systemic issues after each phase rather than after all 100 guides.

### Why wait for all agents to complete before starting the next phase?

The orchestrator waits for all write agents to finish before starting validation. With synchronous agents launched in a single message, this happens naturally: all agents run in parallel and the orchestrator receives all results at once, then immediately launches the next batch (validation agents) in the next message.

**Why this phased approach works well:**

1. **The process doc prescribes sequential phases**: Step 3 (write) then Step 4 (self-validate) then Step 5 (lint) then Step 6 (spot-check). Each step depends on the prior step completing for that file.
2. **Error detection**: If an agent fails to write a file, resuming it for validation would be wasted work. Waiting confirms all files exist before proceeding.
3. **Context window management**: Phasing keeps the orchestrator's context clean and manageable by processing one batch of results at a time.
4. **No user intervention needed**: Because synchronous agents block until complete, the entire pipeline (write → validate → lint → spot-check → update config) runs as one continuous flow. The user says "proceed with the next phase" once, and the orchestrator handles all 5 steps automatically.

**How it could be optimized:**

There's no reason the orchestrator can't start validating Guide 20 the moment its write agent finishes, while Guide 24 is still being written. This pipelining would save wall-clock time at the cost of slightly more complex orchestration logic. The process doc doesn't specify this level of pipelining because the added complexity rarely pays off: the write agents for a single phase typically finish within seconds of each other, so the idle wait between "first agent done" and "last agent done" is minimal.
