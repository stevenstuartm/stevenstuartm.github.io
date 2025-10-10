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

### Markdown Formatting Requirements
- **Tables**: Always include a blank line before markdown tables
- **Headers**: Use proper header hierarchy (H1 → H2 → H3)
- **Code blocks**: Use triple backticks with language specification
- **Links**: Use markdown link syntax for internal references