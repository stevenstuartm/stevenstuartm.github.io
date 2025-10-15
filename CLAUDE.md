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
- Include YAML front matter with: layout, title, date, and optional tags
- Use `layout: post` (set by default in config)

Example:
```yaml
---
layout: post
title: "Your Post Title"
date: 2025-09-29
tags: [architecture, design-patterns]
---
```

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