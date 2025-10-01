# stevenstuartm.github.io

Personal website and blog for Steven Stuart, featuring articles on software architecture, system design, and technology insights.

## About

This is a Jekyll-based static site deployed on GitHub Pages. The site includes:

- **Blog**: Technical articles on software architecture, design patterns, and engineering practices
- **Tech Radar**: Interactive visualization of technologies and tools
- **Resume**: Professional experience and skills
- **About**: Background and contact information

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

## Deployment

This site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

Live site: [https://stevenstuartm.com](https://stevenstuartm.com)

## License

© 2025 Steven Stuart. All rights reserved.

## Contact

- Email: stevenstuartm@gmail.com
- GitHub: [@stevenstuartm](https://github.com/stevenstuartm)
- LinkedIn: [steven-stuart-2974978a](https://www.linkedin.com/in/steven-stuart-2974978a)