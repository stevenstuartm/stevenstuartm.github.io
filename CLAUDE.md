# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Content Writing Standards

**Before writing or reviewing any site content**, read the relevant guide in `.claude/content/`:

| Guide | When to use |
| --- | --- |
| [`writing-standards.md`](.claude/content/writing-standards.md) | **Always** — universal linter rules, voice, flow, punctuation, bullet point usage |
| [`blog-post-guide.md`](.claude/content/blog-post-guide.md) | Writing or editing blog posts, creating social media summaries |

After drafting content, run `python lint_content.py <filepath>` to catch mechanical violations.

---

## Project Overview

This is a Jekyll-based GitHub Pages personal website for Steven Stuart. Its purpose is **personal marketing and mentorship** — hiring pitch, philosophy, case studies, and Steven's own blog content. It is not a general publishing platform.

Study guides, the tech radar, and general technical posts have moved to the partner site: **lucentowl.com**. The homepage and about page reference lucentowl.com for those resources. Inbound links to removed content hit a custom 404 page that directs users to lucentowl.com.

See [REBRANDING.md](REBRANDING.md) for the full migration plan and status.

The site is deployed directly to GitHub Pages.

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
  - `home.html`: Homepage layout (extends default) with featured cards and partner site notice
  - `post.html`: Blog post template with metadata and tags
  - `page.html`: Generic page template
  - `blog-listing.html`: Blog listing page template
  - `guide.html`, `guides.html`, `radar.html`: Legacy layouts kept in place; not used by active pages
- **_includes/**: Reusable HTML partials (header.html, footer.html)
- **_posts/**: Blog posts in Markdown with YAML front matter (format: YYYY-MM-DD-title.md)
- **_drafts/**: Draft posts not yet published (includes posts migrated to lucentowl.com)
- **_guides/**: Study guide files — kept intact but not navigable from this site; content lives on lucentowl.com
- **_site/**: Generated static site (excluded from git)
- **pages/**: Site pages (blog, resume, about, philosophy, case-studies)
- **assets/**: Static assets
  - `css/main.css`: Custom stylesheets with CSS variables for theming
  - `js/`: JavaScript files
  - `img/`: Images and favicon

### Content Files
- **index.md**: Homepage content (uses home layout)
- **pages/resume.md**: Resume/CV page
- **pages/about.md**: About page
- **pages/philosophy.md**: Philosophy page

### Permalinks
- Posts use the permalink structure: `/blog/:year/:month/:day/:title.html`

**Important for SEO**: All URLs end with `.html` extension. When generating blog post URLs, always include the `.html` suffix.

### Blog Post Format

All blog posts must:
- Be placed in `_posts/` with filename format `YYYY-MM-DD-title.md`
- Include YAML front matter with: layout, title, date, description, and tags
- Use `layout: post` (set by default in config)

```yaml
---
layout: post
title: "Your Post Title"
date: 2025-09-29
description: "Concise summary that captures the core thesis and key points of the post"
tags: [architecture, design-patterns]
---
```

**CRITICAL: NEVER rename files**:
- ❌ NEVER rename blog post files (`_posts/*.md`) or any other content files
- ❌ NEVER use `git mv` or any other method to rename files
- The filename format `YYYY-MM-DD-title.md` is permanent once created
- If the title changes, update only the `title:` field in the front matter
- **Rationale**: File renames break external links, analytics, bookmarks, and SEO
- This rule is non-negotiable and applies to all content files (posts, guides, pages)

For writing standards, required fields detail, and social media summaries, see [`.claude/content/blog-post-guide.md`](.claude/content/blog-post-guide.md).

## Site Configuration

- Uses kramdown markdown processor
- Configured for GitHub Pages deployment via github-pages gem
- Theme: Custom CSS with CSS variables for maintainability
- Author: Steven Stuart
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
[Link Text](/about.html)
```

Always include `rel="noopener noreferrer"` with `target="_blank"` to prevent security vulnerabilities.

Links to lucentowl.com are external and must use `target="_blank"`.

## Best Practices

### When Working with Code
- Always read files before editing to understand context
- Maintain consistent formatting and indentation
- Test changes locally with `bundle exec jekyll serve` before committing

### Code Examples
- **Default to C# for programming examples** unless the subject is language-specific
- Use the appropriate language when the topic requires it (e.g., Terraform uses HCL, CloudFormation uses YAML/JSON, Python for data science)

## Maintaining This File

**IMPORTANT**: Claude Code should proactively keep this CLAUDE.md file up to date during conversations.

### When to Update CLAUDE.md

Update this file whenever:
1. **New patterns emerge** — architectural patterns, naming conventions, or project-specific approaches discovered during a session
2. **Project structure changes** — new directories, major file reorganizations, or build process changes
3. **Common tasks are repeated** — if the same task is performed multiple times, document it as a standard procedure
4. **Important decisions are made** — architecture choices, technology selections, or design patterns adopted
5. **Gotchas are discovered** — edge cases, quirks, or common mistakes to avoid
6. **Dependencies change** — new gems, plugins, or significant configuration updates

Writing standards and content guidelines belong in the `.claude/content/` guides, not here.

### Session Management

At the end of substantial work sessions:
1. Review what was accomplished
2. Identify any new patterns or learnings that would benefit future sessions
3. Proactively ask if CLAUDE.md or a content guide should be updated with these learnings
4. Commit the changes if significant

### What NOT to Include

- Temporary or session-specific information
- Highly detailed implementation notes (use code comments instead)
- User-specific preferences (unless they're project standards)
- Writing standards and content quality rules (those belong in `.claude/content/`)
- Duplicate information already covered elsewhere in the file
