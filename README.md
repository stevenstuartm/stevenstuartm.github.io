# Software Architecture & System Design Blog

A practical resource for software architects and engineers, featuring real-world insights on cloud architecture, distributed systems, and modern development practices.

## What You'll Find Here

- **Technical Articles**: In-depth posts on software architecture, system design patterns, Domain-Driven Design, AWS, .NET, microservices, and engineering leadership
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
├── _layouts/             # Page templates
├── _includes/            # Reusable HTML components
├── _posts/               # Blog posts (Markdown)
├── assets/
│   ├── css/             # Stylesheets
│   ├── data/            # JSON data files
│   └── images/          # Image assets
├── index.md             # Homepage
├── blog.md              # Blog listing page
├── resume.md            # Resume/CV
└── about.md             # About page
```

## Writing Blog Posts

Blog posts are written in Markdown and placed in the `_posts/` directory with the filename format:

```
YYYY-MM-DD-title.md
```

Each post requires YAML front matter:

```yaml
---
layout: post
title: "Your Post Title"
date: 2025-09-29
tags: [architecture, design-patterns]
---

Your content here...
```

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