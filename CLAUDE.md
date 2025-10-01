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
- **_includes/**: Reusable HTML partials (header.html, footer.html)
- **_posts/**: Blog posts in Markdown with YAML front matter (format: YYYY-MM-DD-title.md)
- **_site/**: Generated static site (excluded from git)
- **pages/**: Site pages (blog, resume, about, tech-radar)
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

### Permalinks
Posts use the permalink structure: `/blog/:year/:month/:day/:title/`

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