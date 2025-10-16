# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based GitHub Pages personal website for Steven Stuart, featuring a blog focused on software architecture, system design, and technology insights. The site is deployed directly to GitHub Pages.

## Development Commands

### Local Development
```bash
# Install dependencies
bundle install

# Run local development server (usually port 4000)
bundle exec jekyll serve

# Build the site (output to _site/)
bundle exec jekyll build
```

## Architecture

### Jekyll Structure
- **_config.yml**: Site configuration, author info, social links, and build settings
- **_layouts/**: HTML templates that wrap content
  - `default.html`: Base template with header/footer includes
  - `home.html`: Homepage layout (extends default) with recent posts section
  - `post.html`: Blog post template with metadata and tags
  - `page.html`: Generic page template
  - `radar.html`: Tech radar page template with D3.js visualization
  - `guide.html`: Study guide template with table of contents
  - `guides.html`: Study guides listing page template
  - `blog-listing.html`: Blog listing page template
- **_includes/**: Reusable HTML partials (header.html, footer.html)
- **_posts/**: Blog posts in Markdown with YAML front matter (format: YYYY-MM-DD-title.md)
- **_guides/**: Study guides in Markdown organized by topic
- **_site/**: Generated static site (excluded from git)
- **pages/**: Site pages (blog, resume, about, tech-radar, study-guides)
- **assets/**: Static assets
  - `css/main.css`: Custom stylesheets with CSS variables for theming
  - `js/`: JavaScript files including D3.js and radar visualization
  - `data/radar-data.json`: Tech radar data (quadrants, rings, entries)
  - `img/`: Images and favicon

### Content Files
- **index.md**: Homepage content (uses home layout)
- **pages/blog.md**: Blog listing page
- **pages/resume.md**: Resume/CV page
- **pages/about.md**: About page
- **pages/tech-radar.md**: Interactive tech radar visualization (uses radar layout)
- **pages/study-guides.md**: Study guides listing page
- **pages/study-routine.md**: Study routine and learning methodology page
- **pages/upcoming.md**: Upcoming blog posts and content

### Permalinks
- Posts use the permalink structure: `/blog/:year/:month/:day/:title.html`
- Study guides use the permalink structure: `/study-guides/:path.html`

**Important for SEO**: All URLs end with `.html` extension. When generating blog post URLs, always include the `.html` suffix.

### Blog Post Format
All blog posts must:
- Be placed in `_posts/` with filename format `YYYY-MM-DD-title.md`
- Include YAML front matter with: layout, title, date, description, series, and tags
- Use `layout: post` (set by default in config)

Example:
```yaml
---
layout: post
title: "Your Post Title"
date: 2025-09-29
description: "Concise summary that captures the core thesis and key points of the post"
series: "Technology & Tools"
tags: [architecture, design-patterns]
---
```

**CRITICAL: Required front matter fields**:
- **description**: A 1-2 sentence summary that captures the core thesis. Used for SEO and post previews.
- **series**: Must match one of the existing series names in `assets/data/blog_series_config.json`

**Standard procedure for creating a new blog post**:
1. Create the markdown file in `_posts/` with correct date format
2. Include complete YAML front matter (layout, title, date, description, series, tags)
3. **Immediately update** `assets/data/blog_series_config.json`:
   - Add the post filename to the appropriate series' `posts` array
   - Posts are listed in reverse chronological order (newest first)
4. Update `assets/data/upcoming-items.json` if the post was planned:
   - Change status from "planned" to "completed"
   - Update deliveryDate to actual publish date

**Existing blog series** (from blog_series_config.json):
- **Architecture Insights**: Deep dives into architectural patterns, code quality, and system design principles
- **Technology & Tools**: Practical lessons from infrastructure, frameworks, and development tools
- **Development Practice**: Insights on agile methodologies, learning strategies, and career growth
- **Industry & Culture**: Perspectives on hiring practices, leadership, and industry trends

**Common gotcha**: Creating a blog post without updating blog_series_config.json will result in the post not appearing in the series listing on the blog page. Always modify both files together.

### Study Guide Format
All study guides must:
- Be placed in `_guides/` directory (can be organized in subdirectories by topic)
- Include YAML front matter with: layout, title, category, subcategory, and description
- Use `layout: guide`
- Include proper markdown formatting with blank lines before tables

Example:
```yaml
---
title: "Guide Title"
layout: guide
category: Main Category
subcategory: Subcategory
description: "Brief description of the guide content"
---
```

**Important**: Tables in Markdown must have a blank line before them to render correctly in Jekyll/Kramdown.

### Study Guides Configuration

**Critical**: When adding or removing study guide files, ALWAYS update the configuration file:
- **Configuration file**: `assets/data/study_guides_config.json`
- This JSON file controls which guides appear on the study guides listing page
- Structure: Categories → Subcategories → Guides array

**Standard procedure for adding a new study guide**:
1. Create the markdown file in `_guides/` (organized by category subdirectory)
2. Include proper YAML front matter with category, subcategory, and description
3. **Immediately update** `assets/data/study_guides_config.json`:
   - Add new subcategory if needed (with name and description)
   - Add the guide filename to the appropriate subcategory's `guides` array
4. Test locally to verify the guide appears on the study guides page

**Example configuration entry**:
```json
{
  "name": "Business & Economics",
  "description": "Cost analysis, ROI, and financial aspects of architecture",
  "guides": [
    "tco-roi.md"
  ]
}
```

**Common gotcha**: Creating a guide file without updating the config will result in the guide existing but not being discoverable on the website. Always modify both files together.

## Tech Radar

The site includes an interactive tech radar feature built with D3.js:
- **Data Source**: `assets/data/radar-data.json` contains all radar entries
- **Visualization**: Uses Zalando's tech radar visualization library
- **Data Structure**:
  - 4 quadrants: Languages & Frameworks, Platforms, Techniques, Tools
  - 4 rings: ADOPT, TRIAL, ASSESS, HOLD
  - Each entry includes: id, label, quadrant, ring, moved status, and description
- **Features**: Dual view (radar/list), clickable items with detail modals, responsive design

### Updating the Tech Radar

To add/modify radar entries, edit `assets/data/radar-data.json`:
- Quadrants are indexed 0-3
- Rings are indexed 0-3 (0=ADOPT, 1=TRIAL, 2=ASSESS, 3=HOLD)
- Movement indicators: 0=no change, 1=moved in, -1=moved out, 2=new entry

## Site Configuration

- Uses kramdown markdown processor
- Configured for GitHub Pages deployment via github-pages gem
- Theme: Custom CSS with CSS variables for maintainability
- Author: Steven Stuart (stevenstuartm@gmail.com)
- GitHub: stevenstuartm
- LinkedIn: steven-stuart-2974978a

### Link Behavior

**Links that should open in new tabs must be explicitly marked** using Kramdown's inline attribute syntax:

**For external links** (or any link that should open in a new tab):
```markdown
[Link Text](https://example.com){:target="_blank" rel="noopener noreferrer"}
```

**For internal links** (default behavior, stays in same tab):
```markdown
[Link Text](/study-guides/some-guide.html)
```

**Why this approach**:
- Explicit and clear in the source markdown
- Developers can see intent directly in the content
- No hidden JavaScript magic that could confuse maintainers
- Full control over which links open in new tabs vs. same tab
- Follows Kramdown's standard inline attribute list (IAL) syntax

**Security note**: Always include `rel="noopener noreferrer"` with `target="_blank"` to prevent potential security vulnerabilities

## Best Practices

### When Working with Code
- Always read files before editing to understand context
- Maintain consistent formatting and indentation
- Test changes locally with `bundle exec jekyll serve` before committing
- Blog posts must follow the YYYY-MM-DD-title.md naming convention
- Keep radar data JSON properly formatted and validated

### Content Guidelines
- Blog posts should include meaningful tags for discoverability
- Use descriptive titles and ensure proper front matter
- Include meta descriptions for better SEO
- Study guides should have comprehensive table of contents
- Ensure proper markdown formatting, especially blank lines before tables
- Organize study guides by category and subcategory for better navigation

### Blog Post Writing Standards

**CRITICAL: Clarity through brevity**:
When writing blog posts, prioritize clarity over verbosity:
- Cut unnecessary words that obscure the point
- Use bullet points and lists instead of dense paragraphs for structural advantages
- Break long sections into digestible subsections with clear headers
- Ensure section titles accurately reflect their content
- If a point can be made in fewer words, do so

**Data and claims require sources**:
- Any market statistics, survey results, or industry data MUST include the source
- Format: "62% of users (Source: Company Name Report 2024)"
- Data without sources is meaningless and damages credibility
- Link to sources when possible

**Formatting for readability**:
- Headers must have blank lines before them (Jekyll/Kramdown requirement)
- Use tables for comparisons instead of prose when appropriate
- Bulleted lists for advantages/disadvantages, not paragraph form
- Keep sections focused - if a section is too long, break it up

**Title-content alignment**:
- Section titles should clearly indicate what the section contains
- Avoid generic titles like "The Problem" - be specific
- Readers should understand the section's purpose from the title alone

### Study Guide Content Philosophy

**Focus on actionable knowledge over reference material**:
- Avoid generic "Further Reading" sections with book lists and external links
- Avoid template sections with fill-in-the-blank structures (readers can create their own)
- Avoid extensive checklists that become reference cards rather than learning material

**Do include**:
- Core concepts, definitions, and formulas
- Decision frameworks and comparison models
- Real-world examples that demonstrate practical application
- Common pitfalls and how to avoid them
- Best practices derived from experience
- Key takeaways that summarize actionable insights

**Guiding principle**: Readers should learn things they didn't know and understand what they can and should do with that knowledge, without being overwhelmed by supplementary reference material.

### Study Guide Content Quality Standards

**CRITICAL: Explain before prescribing**:
- Always provide substantive explanations of what concepts, frameworks, and tools actually ARE before describing when/how to use them
- Don't jump straight to "When to use" without first explaining the fundamentals
- Readers need to understand the subject matter before they can make informed decisions about applying it
- Example: When documenting a framework, explain its structure, components, and how it works BEFORE listing use cases

**CRITICAL: Link to mentioned resources**:
- If you reference a specific tool, framework, organization, website, or resource in the content, ALWAYS provide a link to it
- Add a "Resources" or "Resources and References" section for each major topic with official documentation links
- Include links to:
  - Official homepages and documentation
  - Tools and web consoles mentioned in the text
  - Standards bodies and certification programs
  - Key whitepapers and reference materials
- Organize resources logically (by framework, by topic, etc.)
- Use descriptive link text so readers know what they're clicking on

**Example of proper structure**:
```markdown
### Framework Name

**What it is:**
[Detailed explanation of the framework, its components, structure, and how it works]

**When to use:**
[Use cases and decision criteria]

**Resources:**
- [Official Homepage](https://example.com)
- [Documentation](https://docs.example.com)
- [Tool or Console](https://console.example.com)
```

### Architecture Terminology Standards

**CRITICAL: Use correct architecture terminology**

When writing about software architecture, always use proper terminology:

**Architectural Characteristics (NOT "Non-Functional Requirements")**:
- Correct term: **Architectural Characteristics**
- Also acceptable: Quality attributes, "-ilities"
- ❌ Avoid: "Non-functional requirements" (outdated term)
- Reference: [Architecture Foundations](/study-guides/architecture/ArchitectureFoundations.html#architecture-characteristics)

**Selection process for architectural characteristics**:
1. Identify **7 characteristics** that are critical to the project's success
2. Prioritize the **top 3** characteristics—these drive architecture style selection
3. Use structured worksheets to evaluate and select: [Developer to Architect Worksheets](https://developertoarchitect.com/downloads/worksheets.html)

**Characteristics must meet three criteria**:
- Specify non-domain consideration
- Influence structural design
- Be critical to success

**Common categories**:
- **Operational**: Availability, Performance, Scalability, Reliability, Recoverability
- **Structural**: Maintainability, Extensibility, Portability, Upgradeability
- **Cross-Cutting**: Security, Privacy, Supportability, Accessibility

**When writing AAA Phase 2 (Agree) content**:
- List "Architectural Characteristics" as the FIRST design decision
- Emphasize that the top 3 characteristics drive the architecture style choice
- Reference the worksheets for systematic evaluation
- Link to Architecture Foundations guide for detailed explanations

### Study Guide Organization Patterns

**Existing category structure**:
- **Architecture**: Foundations, Styles, Leadership, Design, Patterns, Data & Infrastructure, Business & Economics
- **Data Structures & Algorithms**: Fundamentals, Linear Data Structures, Trees & Heaps, Graphs, Hash Tables & Algorithms
- **Object-Oriented Programming**: OOP Foundations, Design Patterns
- **Security**: Security Fundamentals, Threats & Defense, Application Security, Governance & Response
- **Software Development Lifecycle**: SDLC & Modeling
- **AI & Machine Learning**: Machine Learning
- **Data & Analytics**: Analytics
- **Observability**: Monitoring & Observability
- **Networking**: Network Fundamentals
- **Web Development**: SEO & Web

**File organization conventions**:
- Architecture guides live in `_guides/architecture/` subdirectory
- DSA guides live in `_guides/dsa/` subdirectory
- OOP guides live in `_guides/oop/` subdirectory
- Security guides live in `_guides/security/` subdirectory
- SDLC guides live in `_guides/sdlc/` subdirectory
- Top-level guides (observability, networking, etc.) live directly in `_guides/`

**When to create new subcategories**:
- Group related guides under a coherent theme
- Subcategory should have clear, descriptive name and purpose
- Include helpful description that explains the content scope
- Consider if the subcategory will have multiple guides (avoid single-guide subcategories unless it's a starting point for planned expansion)

### Markdown Formatting Requirements
- **Tables**: Always include a blank line before markdown tables
- **Headers**: Use proper header hierarchy (H1 → H2 → H3)
- **Code blocks**: Use triple backticks with language specification
- **Links**: Use markdown link syntax for internal references

### Writing Style and Voice

**CRITICAL: Avoid AI-tell phrases**:
These phrases are obvious indicators of AI-generated content and must be avoided:
- ❌ "The key insight"
- ❌ "It's important to note"
- ❌ "It's worth noting"
- ❌ "It should be noted"
- ❌ "In conclusion" / "In summary"
- ❌ "Ultimately" / "Essentially" / "Fundamentally" (when used as filler)
- ❌ "At the end of the day"
- ❌ "The bottom line is"

**Write naturally instead**:
- ✅ State insights directly without meta-commentary
- ✅ Use active voice and direct statements
- ✅ Let the content speak for itself without labeling it as "key" or "important"

**Example transformations**:
```markdown
❌ The key insight: AAA applies at any scale
✅ AAA applies at any scale

❌ It's important to note that alignment comes first
✅ Alignment comes first

❌ AAA is fundamentally about how we value
✅ AAA is about how we value
```

### AAA Cycle Content Philosophy

The AAA Cycle represents a specific philosophical approach that must be maintained consistently:

**What AAA Is**:
- A guiding discipline and principle, NOT a framework or methodology
- A way of valuing before a way of working
- A philosophy that transcends SDLC methodologies (Agile, Waterfall, etc.)
- Guardrails against common failures, not a rigid checklist

**Core AAA Values (always present in this order)**:
1. **Align** = Human connection comes first (understanding needs before solutions)
2. **Agree** = Shared commitment (genuine agreement before execution)
3. **Apply** = Honoring agreements (applying what was agreed, not just "delivering")

**Critical positioning**:
- Never compare AAA to SDLC methodologies as if it's competing with them
- Emphasize that "delivery" is NOT the goal - applying the agreement is
- Focus on preventing failures through broken values, not broken processes
- Present concrete activities as "examples of the discipline in practice" rather than required steps
- Frame strict frameworks (like Scrum) as often becoming defensive/political rather than trust-based
- Distinguish "agile" (principle) from "Agile" (branded methodology with ceremonies)
- AAA is about being flexible on *how* while unwavering on *what matters* (values)

**When updating AAA content**:
- Lead with the philosophical value, then show practical application
- Use "The Core Value" headings to reinforce the discipline aspect
- Emphasize human connection and relationships throughout
- Avoid language that makes AAA sound like just another process framework

**Consistent terminology**:
- "Guiding discipline" or "principle" (not "framework" or "methodology")
- "Living this discipline" (not "steps to follow" or "tasks to complete")
- "What [Phase] Produces" (not "what you deliver")
- "Guards against failure" (not "ensures success")

**Featured guide description pattern** (for homepage):
When featuring AAA on the homepage, always emphasize:
1. What it is NOT (not a framework)
2. That it's a way of valuing
3. How it transcends methodologies
4. The three core values explicitly
5. Its role as providing guardrails

### AAA Cycle Guide Structure Pattern

**CRITICAL: Eliminate redundant summaries**

AAA guides (and all study guides) should NOT have final summary sections that repeat content. Instead:

**Standard structure for AAA phase guides**:

1. **Phase Overview** (upfront context)
   - Purpose statement
   - The Universal Pattern (numbered steps for this phase)
   - Recursive Application (how it scales from hours to months)
   - Entry & Exit (what you start with, what you deliver)

2. **Core Activities** (detailed sections)
   - Each activity has: description, key points, "How to Do This Well", and "Red Flags"
   - **"How to Do This Well"** replaces "Core Principles" - provides actionable guidance
   - **Red Flags** include both obvious issues and common failure modes
   - Integrate principles directly where they apply rather than listing separately

3. **Supporting Sections** (as needed)
   - Detailed breakdowns (e.g., Project Charter, Cost Analysis)
   - Each with its own actionable guidance embedded

**What to avoid**:
- ❌ "Essential Principles" section at the end
- ❌ "What Matters Most" summary lists
- ❌ "Common Failure Modes" as separate section (integrate into Red Flags)
- ❌ Repeating the Universal Pattern at the end (it's already in Overview)

**Why this works**:
- Readers get context upfront with the Universal Pattern
- Main content is comprehensive and actionable on its own
- No need to re-read a summary if the main content is clear
- Prevents redundancy and maintains focus throughout

## Maintaining This File

**IMPORTANT**: Claude Code should proactively keep this CLAUDE.md file up to date during conversations.

### When to Update CLAUDE.md

Update this file whenever:
1. **New patterns emerge** - If architectural patterns, naming conventions, or project-specific approaches are discovered during a session
2. **Project structure changes** - New directories, major file reorganizations, or build process changes
3. **Common tasks are repeated** - If the same task is performed multiple times, document it as a standard procedure
4. **Important decisions are made** - Architecture choices, technology selections, or design patterns adopted
5. **Gotchas are discovered** - Edge cases, quirks, or common mistakes to avoid
6. **Dependencies change** - New gems, plugins, or significant configuration updates
7. **Content patterns established** - New blog series, content organization methods, or writing conventions

### Session Management

At the end of substantial work sessions:
1. Review what was accomplished
2. Identify any new patterns or learnings that would benefit future sessions
3. Proactively ask if CLAUDE.md should be updated with these learnings
4. Update CLAUDE.md with relevant information
5. Commit the changes if significant

### What NOT to Include

- Temporary or session-specific information
- Highly detailed implementation notes (use code comments instead)
- User-specific preferences (unless they're project standards)
- Duplicate information already covered elsewhere in the file