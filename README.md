# Software Architecture & System Design Blog

A practical resource for software architects and engineers, featuring real-world insights on cloud architecture, distributed systems, and modern development practices.

## What You'll Find Here

- **Study Guides**: comprehensive guides covering Architecture, Data Structures & Algorithms, Object-Oriented Programming, Security, SDLC, AI/ML, and more—organized by category and tagged for easy discovery
- **Blog**: In-depth posts on software architecture, system design patterns, Domain-Driven Design, AWS, .NET, microservices, and engineering leadership
- **Tech Radar**: Interactive visualization exploring technology choices, assessments, and recommendations based on production experience
- **Practical Lessons**: Real project learnings—architectural decisions that worked (and those that didn't), cloud optimization strategies, and team leadership insights

## Purpose

This site exists to help developers level up to architects and teams build better production systems through:
- Honest assessments of architectural patterns and technologies
- Real-world examples from migrating monoliths to microservices, optimizing cloud infrastructure, and leading engineering teams
- Actionable strategies backed by 15+ years of hands-on experience

## Local Development

### Prerequisites

- Ruby (2.7 or higher)
- Bundler gem

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/stevenstuartm/stevenstuartm.github.io.git
   cd stevenstuartm.github.io
   ```

2. Install dependencies:
   ```bash
   bundle install
   ```

3. Run the local development server:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000`

### Building

To build the site for production:

```bash
bundle exec jekyll build
```

The generated site will be in the `_site/` directory.

## Project Structure

```
.
├── _config.yml           # Site configuration
├── _layouts/             # Page templates (default, home, post, guide, radar, blog-listing)
├── _includes/            # Reusable HTML components
├── _posts/               # Blog posts (Markdown, YYYY-MM-DD-title.md format)
├── _guides/              # Study guides organized by category
│   ├── architecture/    # Architecture guides
│   ├── dsa/             # Data Structures & Algorithms
│   ├── oop/             # Object-Oriented Programming
│   ├── security/        # Security guides
│   ├── sdlc/            # Software Development Lifecycle
│   └── ...              # Other categories
├── pages/               # Site pages (blog, study-guides, tech-radar, resume, about)
├── assets/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript (D3.js, radar visualization, reading progress)
│   ├── data/            # JSON data files (radar-data, blog series config, study guides config)
│   └── img/             # Image assets
└── index.md             # Homepage
```

## Writing Content

### Blog Posts

Blog posts are written in Markdown and placed in the `_posts/` directory with the filename format `YYYY-MM-DD-title.md`.

Each post requires YAML front matter:

```yaml
---
layout: post
title: "Your Post Title"
date: 2025-09-29
description: "Brief summary for SEO and previews"
series: "Architecture Insights"
tags: [architecture, design-patterns]
---

Your content here...
```

**Important**: When creating a new blog post, also update `assets/data/blog_series_config.json` to add the post to its series.

### Study Guides

Study guides are organized in `_guides/` by category. Each guide requires:

```yaml
---
layout: guide
title: "Guide Title"
category: Main Category
subcategory: Subcategory
description: "Brief description"
tags: [tag1, tag2, tag3, tag4]
---

Your content here...
```

**Important**: When creating a new study guide, also update `assets/data/study_guides_config.json` to make it discoverable on the study guides page.

## Technology Stack

- **Framework**: Jekyll (static site generator)
- **Hosting**: GitHub Pages
- **Frontend**: Custom CSS with D3.js for tech radar visualization
- **Content**: Markdown-based blog posts with YAML front matter

## Deployment

Automatically deployed to GitHub Pages on push to `main` branch.

**Live site**: [https://stevenstuartm.com](https://stevenstuartm.com)

## Contributing

Found a typo or issue? Feel free to open an issue or submit a pull request.

## License

Content © 2025 Steven Stuart. All rights reserved.
Code licensed under MIT.