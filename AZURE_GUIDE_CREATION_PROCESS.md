# Azure Guide Creation Process

Instructions for Claude Code to follow when creating Azure study guides.

---

## Task

Continue creating Azure study guides following the plan in `_guides/infrastructure/azure/AZURE_GUIDES_PLAN.md`. Check the Progress Tracking section at the bottom for the current phase and next guide number.

## Step 1: Read the Plan

Read `_guides/infrastructure/azure/AZURE_GUIDES_PLAN.md` to identify the current phase and which guides are next. Each phase lists guide numbers, file names, titles, and topics.

## Step 2: Select Model Per Guide

Before launching agents, categorize each guide and select the appropriate model.

**Use haiku** for single-service descriptive guides where the value is organizing known facts into the standard structure. These guides describe what a service is, how it works, its tiers/options, and common pitfalls.

**Use sonnet** for guides that require cross-service synthesis, decision frameworks, or architectural judgment across multiple services. These guides need to weigh tradeoffs that depend on architectural context and produce recommendations a reader couldn't easily derive from reading individual service docs.

**Automatic detection rules** (apply in order):

1. If the guide title contains **"Selection"** → sonnet (decision frameworks comparing multiple services)
2. If the guide title contains **"Patterns"** and is in an "Advanced" subcategory → sonnet (cross-service architectural composition)
3. If the guide title contains **"Architecture"** and is in subcategory 16+ (Serverless, Container Orchestration, Architecture Patterns) → sonnet (advanced cross-cutting patterns)
4. If the plan's Notes section for the guide mentions **cross-service synthesis, composition, or decision frameworks spanning multiple services** → sonnet
5. Otherwise → **haiku**

**Guides that trigger sonnet** (from the current plan):

| Guide # | Title | Reason |
|---------|-------|--------|
| 24 | Azure Database Service Selection | "Selection" - compares 5 database services |
| 47 | Modern Data Architecture on Azure | Cross-service composition (Data Factory + Synapse + Power BI + storage) |
| 52 | Azure AI & ML Service Selection | "Selection" - compares all AI/ML services |
| 56 | Serverless Architecture Patterns on Azure | "Patterns" in advanced subcategory - cross-service composition |
| 59 | Advanced Container Patterns on Azure | "Patterns" in advanced subcategory |
| 60 | Multi-Region Architecture on Azure | Advanced architecture - cross-service resilience patterns |
| 61 | Disaster Recovery on Azure | Advanced architecture - cross-cutting DR patterns |

All other guides use haiku.

## Step 3: Launch Agents in Parallel

Launch one agent per guide with a short prompt (~30 lines):

- Specify the file path: `_guides/infrastructure/azure/<filename>.md`
- Provide the exact front matter (title, layout: guide, category: Azure, subcategory, description, tags)
- List topics to cover as bullet points (from the plan's "Azure Services Covered" column and Notes)
- Include this instruction block:

> Read `_guides/infrastructure/azure/azure-vnet-architecture.md` for format and style reference. Follow the same structure: blockquote pull-quote opening, What Problems X Solves, How X Differs from AWS table, core concept sections, architecture patterns, common pitfalls (Problem/Result/Solution format), and key takeaways. No CLI commands, no dollar amounts, inline links to Microsoft Learn with `{:target="_blank" rel="noopener noreferrer"}`, blank lines before tables, no AI-tell phrases, no Resources/Further Reading sections.

- Set `model` to the value determined in Step 2
- Set `run_in_background: true`

## Step 4: Resume Agents for Self-Validation

After each agent completes, resume it (using the agent ID) with this prompt:

> Re-read the file you just wrote. Verify: (a) front matter has all required fields (title, layout, category, subcategory, description, tags), (b) blank lines before every markdown table, (c) no dollar amounts or CLI commands, (d) no AI-tell phrases like 'key insight', 'fundamentally', 'it's important to note', 'ultimately', 'essentially', (e) blockquote pull-quote exists in opening section, (f) AWS comparison table exists, (g) Common Pitfalls section uses Problem/Result/Solution format, (h) Key Takeaways section exists. Fix any issues found.

This is cheap because the agent already has the content in context from writing it.

## Step 5: Lint in Main Context

Run the linter on each file:

```
python lint_content.py _guides/infrastructure/azure/<filename>.md
```

Fix any violations. The output is small (line numbers and suggestions only).

## Step 6: Spot-Check Front Matter

Read only the first ~10 lines of each file to confirm YAML front matter is correct. Do NOT read the full body.

## Step 7: Update Config and Plan

1. **Update `assets/data/study_guides_config.json`**: Add guide file paths under the Azure category. Create new subcategory entries if the phase introduces a new subcategory.
2. **Update `AZURE_GUIDES_PLAN.md`**: Mark guides as `[x]`, update Guides Completed count and Current Phase at the bottom.

## Key Files

| File | Purpose |
|------|---------|
| `_guides/infrastructure/azure/AZURE_GUIDES_PLAN.md` | Master plan with all 61 guides, phases, and status |
| `assets/data/study_guides_config.json` | Config that controls which guides appear on the website |
| `_guides/infrastructure/azure/azure-vnet-architecture.md` | Format reference (tell agents to read this) |
| `lint_content.py` | Content linter (run from repo root) |
