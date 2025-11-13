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
- Include YAML front matter with: layout, title, category, subcategory, description, and tags
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
tags: [tag1, tag2, tag3, tag4]
---
```

**Important**: Tables in Markdown must have a blank line before them to render correctly in Jekyll/Kramdown.

### Study Guide Tagging System

**CRITICAL**: All study guides must include tags for discoverability and filtering.

**Tag format**:
- Lowercase, hyphenated format (e.g., `decision-making`, `cost-analysis`)
- 4-8 tags per guide (target average: 5-6 tags)
- Tags appear in YAML front matter as an array: `tags: [tag1, tag2, tag3]`

**Tag vocabulary categories**:

1. **Core Disciplines**: `architecture`, `algorithms`, `data-structures`, `security`, `design-patterns`, `distributed-systems`, `infrastructure`, `cloud-computing`, `databases`, `networking`, `testing`, `devops`

2. **Skill Levels**: `fundamentals`, `advanced`, `practical`

3. **Application Contexts**: `performance`, `scalability`, `reliability`, `maintainability`, `observability`

4. **Specific Technologies**: `aws`, `microservices`, `kubernetes`, `oop`, `functional-programming`, `cicd`, `terraform`, `cloudformation`

5. **Business & Process**: `cost-analysis`, `decision-making`, `governance`, `leadership`, `collaboration`, `sdlc`, `agile`, `modeling`, `threat-modeling`

6. **Common Concept Tags**: `statistics`, `analytics`, `hypothesis-testing`, `messaging`, `consistency`, `resilience`, `legacy-systems`, `modernization`, `risk-management`, `workflow`, `transactions`, `caching`, `rate-limiting`, `deployment`, `consensus`, `coordination`, `integration`, `automation`, `documentation`, `complexity-analysis`

**Tagging guidelines**:
- Choose tags that reflect **core concepts covered** in the guide
- Include tags for **related disciplines** to enable cross-category discovery
- Add **skill level** tags (`fundamentals`, `advanced`, `practical`) to help users navigate learning paths
- Include **technology-specific** tags when applicable
- Prioritize tags that enable **cross-cutting discovery** (e.g., all guides about "decision-making" regardless of category)

**Standard procedure for tagging new guides**:
1. Read the guide content to understand core concepts
2. Select 4-8 tags from the established vocabulary
3. Add tags field to YAML front matter before the closing `---`
4. Ensure tags align with similar guides in the same or related categories

**Example tags for common guide types**:
- Architecture pattern guide: `architecture`, `design-patterns`, `distributed-systems`, `microservices`, `practical`
- DSA guide: `algorithms`, `data-structures`, `complexity-analysis`, `fundamentals`, `interview-prep`
- OOP guide: `oop`, `design-patterns`, `solid`, `maintainability`, `practical`
- Security guide: `security`, `threats`, `vulnerabilities`, `defense`, `practical`
- SDLC guide: `sdlc`, `methodology`, `collaboration`, `stakeholder-management`, `practical`

**Why tags matter**:
- Enable **filtering** on study guides and blog pages by concept, not just category
- Support **cross-category discovery** (find all content about "performance" across Architecture, DSA, and Infrastructure)
- Act as a **lightweight index** without the overhead of full-text search
- Improve **SEO** by adding semantic metadata to content
- Create **learning paths** by connecting related guides across categories

### Study Guides Configuration

**Critical**: When adding or removing study guide files, ALWAYS update the configuration file:
- **Configuration file**: `assets/data/study_guides_config.json`
- This JSON file controls which guides appear on the study guides listing page
- Structure: Categories → Subcategories → Guides array

**Standard procedure for adding a new study guide**:
1. Create the markdown file in `_guides/` (organized by category subdirectory)
2. Include proper YAML front matter with category, subcategory, description, **and tags**
3. **Immediately update** `assets/data/study_guides_config.json`:
   - Add new subcategory if needed (with name and description)
   - Add the guide filename to the appropriate subcategory's `guides` array
4. Test locally to verify the guide appears on the study guides page

**IMPORTANT**: Do not forget to add tags when creating a new guide. Tags are critical for discoverability and filtering.

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
- Study guides MUST include tags (4-8 tags from the established vocabulary)
- Use descriptive titles and ensure proper front matter
- Include meta descriptions for better SEO
- Study guides should have comprehensive table of contents
- Ensure proper markdown formatting, especially blank lines before tables
- Organize study guides by category and subcategory for better navigation

### Content Discovery Features

**Tagging system** (implemented):
- All 105+ study guides have been tagged with 4-8 tags each
- Tags enable cross-category discovery (e.g., find all "decision-making" content regardless of category)
- Tag vocabulary is standardized across core disciplines, skill levels, application contexts, technologies, and processes
- Blog posts already have tags in place

**Filtering UI** (planned):
- Client-side JavaScript filtering for study guides page (filter by category, subcategory, tags)
- Client-side JavaScript filtering for blog page (filter by series, tags)
- Optional: Unified "Browse by Tag" page showing all content with specific tags
- No backend required; filters operate on existing JSON data and front matter
- Provides "cheap index" functionality without full-text search overhead

### Code Examples
- **Default to C# for programming examples** unless the subject is language-specific
- Use the appropriate language when the topic requires it (e.g., Terraform uses HCL, CloudFormation uses YAML/JSON, Python for data science)
- For general programming concepts, algorithms, or patterns, prefer C# examples

## Writing Standards for All Site Content

**IMPORTANT**: The following writing standards apply to ALL narrative content on the site—blog posts, study guides, page content, descriptions, etc. The only exceptions are content-specific structural requirements (e.g., study guide front matter, blog post date format). When creating any narrative content, follow these standards.

### Automated Linter Rules

**These rules are enforced by `lint_content.py`**. The linter will catch violations automatically. When you create content, the linter will run and flag these issues:

**AI-tell phrases (automatically detected)**:
- "the key insight", "the insight", "the takeaway"
- "it's important to note", "it's worth noting", "it should be noted"
- "in conclusion", "in summary", "final version", "final conclusion"
- "ultimately", "essentially", "fundamentally" (when used as filler)
- "at the end of the day", "the bottom line is"

**AI-tell colon constructions (automatically detected)**:
- "What's converging:", "A critical distinction:", "The difference:", "The key:", "The point:", "Here's why:"
- These announce importance rather than stating it directly

**Em-dashes in sentences (automatically detected)**:
- Avoid using em-dashes (—) in prose; use semicolons, commas, or periods instead
- Parentheses are acceptable for clarifying asides

**Missing articles (pattern-based detection)**:
- Include "a" or "the" for clarity
- ❌ "masquerading as process" → ✅ "masquerading as a process"
- ❌ "reconsolidate agreement" → ✅ "reconsolidate the agreement"

**Run-on sentences (heuristic detection)**:
- Sentences with 2+ semicolons will be flagged
- Sentences over 150 characters with multiple semicolons and commas will be flagged
- These are warnings; use judgment to determine if the sentence needs breaking up

**Choppy parallel structures (pattern detection)**:
- Telegraphic fragments that should flow together will be flagged
- Pattern: "X says Y. The other says Z." → Should be: "X says Y and the other says Z."
- Pattern: "One side does X. Another does Y." → Should be: "One side does X while another does Y."
- These create staccato rhythm instead of natural narrative flow

**How to use the linter**:
```bash
python lint_content.py _posts/2025-11-08-your-post.md
```

The linter will output violations with line numbers and suggestions. Fix violations before considering the content ready for review.

### Writing Principles Requiring Judgment

**These principles cannot be automated**. Apply them thoughtfully during drafting and review.

#### Clarity and Brevity

**Clarity through brevity**:
- Cut unnecessary words that obscure the point
- Use bullet points and lists strategically for structural advantages, not as a crutch
- Break long sections into digestible subsections with clear headers
- Ensure section titles accurately reflect their content
- If a point can be made in fewer words, do so

**Data and claims require sources**:
- Any market statistics, survey results, or industry data MUST include the source
- Format: "62% of users (Source: Company Name Report 2024)"
- Data without sources is meaningless and damages credibility
- Link to sources when possible

#### Formatting and Structure

- Headers must have blank lines before them (Jekyll/Kramdown requirement)
- Use tables for comparisons instead of prose when appropriate
- Keep sections focused; if a section is too long, break it up

#### Sentence Flow and Punctuation

**Use semicolons and commas purposefully for natural flow**:
- Combine closely related thoughts with semicolons or commas when it improves narrative rhythm
- ❌ "Something is broken in production. You need to fix it." (too choppy)
- ✅ "Something is broken in production, and you need to fix it." (natural flow)
- ❌ "Most troubleshooting failures aren't from lack of effort. Engineers work hard during incidents."
- ✅ "Most troubleshooting failures aren't from lack of effort; engineers work hard during incidents."

**Avoid run-on sentences that force buffering**:
- Punctuation must serve a purpose: improving flow or adding clarity
- Don't chain too many thoughts together; the reader shouldn't need to hold an entire massive sentence in memory to understand the conclusion
- ❌ "With reproduction, you have a test case that consistently triggers the race condition; after your fix, the test passes, and you know it works before it touches production." (too much chaining)
- ✅ "With reproduction, you have a test case that consistently triggers the race condition. After your fix, the test passes. You know it works before it touches production." (digestible chunks)
- ❌ "If the answer is 'exception in cleanup code path,' the fix isn't just patching that one path; it's recognizing that error-handling code paths lack test coverage across the system." (forces buffering)
- ✅ "If the answer is 'exception in cleanup code path,' the fix isn't just patching that one path. It's recognizing that error-handling code paths lack test coverage across the system." (clear separation)

**Guidelines**:
- Use commas/semicolons to connect two related thoughts
- Use periods when adding a third thought or when the combined sentence becomes too long
- Write as you think: natural internal narrative, not telegraphic fragments or over-complicated constructions
- Each sentence should carry one clear idea or two closely related ideas, not three or more

#### Title-Content Alignment

- Section titles should clearly indicate what the section contains
- Avoid generic titles like "The Problem"; be specific
- Readers should understand the section's purpose from the title alone

#### Avoid Choppy and Generic Content

Writing that feels choppy or overly generic undermines the impact of the content. Watch for these patterns:
- **Choppy openings**: Sentence fragments or noun-heavy constructions that lack natural flow
  - ❌ "Lack of architectural decision records creates assumption of incompetence"
  - ✅ "When architectural decision records don't exist, future teams assume incompetence rather than recognizing intentional tradeoffs"
- **Telegraphic parallel structures**: Short sentences with parallel structure that should flow together
  - ❌ "When do we update dependencies? One side says always stay current. The other says only update when forced."
  - ✅ "When should we update dependencies? One side says to always stay current and the other says to only update when forced."
  - ❌ "Some teams automate everything. Others rely on manual processes."
  - ✅ "Some teams automate everything while others rely on manual processes."
  - Missing conjunctions (and, but, while, yet) create staccato rhythm instead of conversational flow
- **Generic examples**: Vague statements that readers can easily dismiss as obvious
  - ❌ "Leadership proposes moving back to on-premises infrastructure... Months later they celebrate success"
  - ✅ Provide specific numbers, timelines, and concrete consequences ($2M → $800K over 18 months, but 99.9% → 95% availability, ops team triples, DR becomes tape-based)
- **Awkward semicolon + fragment patterns**: Using semicolons to introduce quotes or fragments creates choppy rhythm
  - ❌ "The rebuild proposal emerges naturally from this dysfunction; 'Let's start fresh...'"
  - ✅ "The rebuild proposal emerges naturally from this dysfunction. 'Let's start fresh,' someone suggests."
- **Command-style paragraphs**: Lists of imperative sentences without context feel robotic
  - ❌ "State the real problem. Define measurable success criteria. Evaluate the alternatives."
  - ✅ Use bold headers with explanatory follow-ups: "**State the real problem, not the symptom.** The symptom is 'AWS is expensive.' The real problem is..."

#### Providing Examples

Specific details make abstract concepts concrete and credible. Include:
- Actual numbers (costs, percentages, timelines)
- Specific technologies and trade-offs
- Real consequences, not just "it got worse"
- Natural narrative flow, not telegraphic lists

### Content Quality Workflow

**When creating content, follow this workflow**:

1. **Draft**: Write content applying the writing principles above
2. **Lint**: Run `python lint_content.py <filepath>` and fix all violations
3. **Self-review**: Check for issues the linter cannot detect:
   - Is the narrative flow natural, or does it feel choppy?
   - Are examples specific with concrete numbers and consequences?
   - Do section titles accurately reflect their content?
   - Are bullet points used strategically (for actionable items) vs. as a crutch?
   - Is punctuation serving a purpose (flow/clarity) or just chaining thoughts?
4. **Manual review**: User reviews for nuanced issues, content accuracy, and overall quality

**Remember**: The linter catches mechanical issues. You must still apply judgment for voice, flow, examples, and narrative quality.

### Creating Social Media Summaries from Blog Posts

When creating LinkedIn or social media summaries of blog posts, apply these principles for maximum impact:

**1. Lead with the hook and solution signal**
- Open with the provocative thesis immediately
- Signal that a concrete solution exists early: "So try a different approach"
- Don't bury the solution promise in later paragraphs

**2. Trust intelligent readers**
- Assume readers can fill in obvious gaps without exhaustive explanation
- Remove unnecessary elaboration that weakens punch
- ❌ "Decisions made without understanding constraints, requirements that shift mid-implementation, or scope creep that forces compromises"
- ✅ "unclear communication with stakeholders and a lack of governance between tech leads and developers"

**3. Use standalone punchy statements**
- Give key points their own paragraph for emphasis
- ✅ "When you later say 'we need to pay down tech debt,' stakeholders hear 'we want to fix our mistakes instead of delivering features.'"
- Standing alone creates impact that inline text doesn't

**4. Be specific about root causes**
- Add dimensions that the full post explores in detail
- Don't just say "communication problems"—specify "unclear communication with stakeholders AND lack of governance between tech leads and developers"

**5. Simplify solution presentation**
- Use clean bulleted lists instead of bold inline text for scannability
- Format for the platform (LinkedIn favors bullets over dense paragraphs)

**6. Cut redundant phrases**
- ❌ "Stop asking stakeholders to pay for past mistakes. Start presenting forward-looking opportunities."
- ✅ "Start presenting forward-looking opportunities." (the contrast is implied)

**7. Shorter, punchier sentences**
- ✅ "Regardless of the origin of the problem, the term 'tech debt' nearly guarantees de-prioritization."
- More direct than elaborate constructions

**Testing the summary**:
- Run `python lint_content.py --text "<summary_text>"` to check for AI-tell phrases and other violations
- Read it aloud—does it sound like how you'd explain it in person?
- Could an intelligent reader grasp the thesis and solution in 30 seconds?

**Key principle**: Social summaries are not compressed blog posts. They're standalone artifacts that capture the thesis, hint at the reasoning, and present the solution clearly. Assume smart readers who don't need hand-holding.

## Content-Specific Guidelines

The following sections contain guidelines specific to particular content types on the site.

### Study Guide Content Philosophy

**Focus on actionable knowledge over reference material**:
- Avoid generic "Further Reading" sections with book lists and external links
- Avoid template sections with fill-in-the-blank structures (readers can create their own)
- Avoid extensive checklists that become reference cards rather than learning material
- **DO NOT add "Resources" sections** unless explicitly requested by the user
- **DO NOT add "Next Steps" sections** - study guides should be self-contained
- Links to tools/frameworks should be inline where mentioned, not collected in a separate section

**Do include**:
- Core concepts, definitions, and formulas
- Decision frameworks and comparison models
- Real-world examples that demonstrate practical application
- Common pitfalls and how to avoid them
- Best practices derived from experience
- Key takeaways that summarize actionable insights
- Inline links using `{:target="_blank" rel="noopener noreferrer"}` for external resources when mentioned

**Guiding principle**: Readers should learn things they didn't know and understand what they can and should do with that knowledge, without being overwhelmed by supplementary reference material. Study guides must be effective on their own.

### Study Guide Content Quality Standards

**CRITICAL: Explain before prescribing**:
- Always provide substantive explanations of what concepts, frameworks, and tools actually ARE before describing when/how to use them
- Don't jump straight to "When to use" without first explaining the fundamentals
- Readers need to understand the subject matter before they can make informed decisions about applying it
- Example: When documenting a framework, explain its structure, components, and how it works BEFORE listing use cases

**CRITICAL: Link inline, not in separate sections**:
- If you reference a specific tool, framework, organization, website, or resource in the content, provide an inline link where it's mentioned
- Use descriptive link text so readers know what they're clicking on
- Format: `[Tool Name](https://example.com){:target="_blank" rel="noopener noreferrer"}`
- Do NOT create separate "Resources" or "Further Reading" sections

**CRITICAL: Concepts over code syntax**:
- Unless the guide's topic is directly coupled to code and how to code, remain conceptual
- Avoid CLI examples, API syntax, or implementation code that rapidly becomes outdated
- Focus on the WHY and WHEN, not the exact HOW
- Describe operations conceptually (e.g., "use the CLI to create a change set")
- Link to official documentation inline where relevant for current syntax
- CLI syntax, API endpoints, and tool-specific commands are reference material, not learning material
- Exception: Include code when the guide teaches coding concepts (algorithms, design patterns, language features)

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

**CRITICAL: Natural prose over robotic lists**

Blog posts should read like thoughtful essays, not manuals or checklists. The default should be smooth narrative prose that reflects an inner dialog and pleasing voice. Use bullet points strategically for actual structural advantages (comparisons, options, steps), not as a crutch to avoid writing coherent paragraphs.

**When bullet points make sense**:
- ✅ Listing distinct options or alternatives
- ✅ Presenting step-by-step procedures
- ✅ Comparing features or characteristics side-by-side
- ✅ Enumerating red flags or warning signs
- ✅ Call-to-action checklists (diagnostic questions, troubleshooting steps, action items)
- ✅ **Conclusion sections with actionable next steps** (when concluding with specific actions the reader should take)

**When prose works better**:
- ❌ Explaining concepts or reasoning (use flowing paragraphs)
- ❌ Providing examples (weave them into narrative)
- ❌ Connecting ideas (use transitions, not bullets)
- ❌ Describing how things work (use descriptive prose)

**Key principle**: If the reader needs to scan and act on specific items (like diagnostic questions during an incident), use bullets for clarity. If the reader needs to understand a concept or follow reasoning, use prose for flow.

**Conclusions and call-to-action**: When concluding a post with actionable steps the reader should take, use bullets. Long comma-separated lists force the reader to buffer too much context. Clear bullet points make each action scannable and memorable.

**Example of effective conclusion bullets**:
```markdown
Or you can demand discipline:
- Discover what you're building before estimating
- Test your assumptions
- Agree on specific outcomes with clear success criteria
- Build what was agreed, or realign when discovery demands it
- Measure whether you actually delivered value
```

**Test for when to use bullets**: If a sentence contains multiple items separated by commas or semicolons, and those items are things the reader should remember or act on, convert it to a bulleted list. Examples:
- ❌ "Capture these artifacts: thread dumps, detailed logs, metrics, network traces, and resource utilization."
- ✅ Use bullets listing each artifact type
- ❌ "Facts gathered: spike started at 14:47 UTC, only read-heavy endpoints affected, database CPU at 95%."
- ✅ Use bullets matching the diagnostic question structure
- ❌ "Mitigation includes: restart the service, route traffic around failing component, increase resource limits."
- ✅ Use bullets listing each mitigation action

**Example transformations**:
```markdown
❌ Robotic/manual style:
**Without reproduction, you cannot:**
- Confirm you understand the problem
- Test whether your fix works
- Distinguish correlation from causation

✅ Natural prose style:
Think about what reproduction actually proves. If you can trigger the issue deliberately, you know the conditions that cause it. You understand not just that something broke, but why it breaks. Without that understanding, you're guessing—about the problem and about whether your fix actually works.
```

**Smooth transitions**: Sections should flow naturally. Use connecting phrases like "Think about...", "Consider...", "The problem is...", "Here's what happens..." rather than abrupt topic changes.

**Integrate examples naturally**: Instead of **Example:** labels, use "Consider this pattern:" or "Here's a concrete example:" or weave examples directly into the narrative.

**CRITICAL: Avoid AI-tell phrases and choppy grammar**:
These phrases and patterns are obvious indicators of AI-generated content and must be avoided:
- ❌ "The key insight" / "The insight" / "The takeaway"
- ❌ "It's important to note" / "It's worth noting" / "It should be noted"
- ❌ "In conclusion" / "In summary" / "Final version" / "Final conclusion"
- ❌ "Ultimately" / "Essentially" / "Fundamentally" (when used as filler)
- ❌ "At the end of the day" / "The bottom line is"
- ❌ Section headers like "The Insight", "The Problem", "The Solution", "The Key"
- ❌ Colon constructions announcing importance: "What's converging:", "A critical distinction:", "The difference:"
- ❌ Sentence fragments with dashes: "What's converging -", "The point -"
- ❌ Missing articles creating choppy grammar: "masquerading as process" (use "as a process"), "Distributed systems made expected failures high-frequency" (use "made expected failures more frequent" or "made failures frequent")

**Write naturally instead**:
- ✅ State insights directly without meta-commentary
- ✅ Use active voice and direct statements
- ✅ Let the content speak for itself without labeling it as "key" or "important"
- ✅ Use complete grammar with articles ("a", "the") instead of consolidated shorthand
- ✅ Prefer simpler words when they convey the same meaning
- ✅ Write as you would speak to someone in person
- ✅ Use complete sentences with natural flow, not telegraphic fragments
- ✅ Default to narrative prose; use bullets strategically, not reflexively

**Example transformations**:
```markdown
❌ The key insight: AAA applies at any scale
✅ AAA applies at any scale

❌ It's important to note that alignment comes first
✅ Alignment comes first

❌ AAA is fundamentally about how we value
✅ AAA is about how we value

❌ ## The Insight
✅ ## Why This Matters (or a specific descriptive header)

❌ masquerading as process
✅ masquerading as a process

❌ reconsolidate agreement
✅ reconsolidate the agreement

❌ What's converging -
✅ Several trends are converging...

❌ A critical distinction:
✅ The distinction matters because... (or just state it directly)

❌ Distributed systems made expected failures high-frequency
✅ Distributed systems made expected failures more frequent
✅ In distributed systems, expected failures happen frequently
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