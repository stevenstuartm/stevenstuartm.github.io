# stevenstuartm.github.io

Personal site for [Steven Stuart](https://stevenstuartm.com) — a personal marketing and mentorship site for a software architect with 15 years of experience in cloud-native platforms and distributed systems.

**Live site**: [https://stevenstuartm.com](https://stevenstuartm.com)

**Partner site**: [https://lucentowl.com](https://lucentowl.com) — study guides, tech radar, and general blog posts live here.

---

## Pages

| Page | Purpose |
|---|---|
| Home | Hiring pitch and overview |
| About | Background, mentorship, and philosophy |
| Resume | Full CV with downloadable PDF/DOCX |
| Software Philosophy | Engineering principles |
| Reading List | Recommended books and sites, with reasoning (path stays `/study-routine.html`) |

---

## Local Development

### Prerequisites

- Ruby (2.7 or higher)
- Bundler gem

### Setup

```bash
git clone https://github.com/stevenstuartm/stevenstuartm.github.io.git
cd stevenstuartm.github.io
bundle install
bundle exec jekyll serve
```

Open [http://localhost:4001](http://localhost:4000).

### Build

```bash
bundle exec jekyll build
```

Output goes to `_site/`.

---

## Project Structure

```
.
├── _config.yml         # Site configuration and author info
├── _layouts/           # Page templates (default, home, page)
├── _includes/          # Reusable partials (header, footer, social links)
├── _drafts/            # Draft content (not published)
├── pages/              # Site pages (about, resume, philosophy, study-routine)
├── assets/
│   ├── css/            # Custom SCSS
│   ├── img/            # Images and favicon
│   └── downloads/      # Resume files
├── .claude/            # Claude Code content guides
├── lint_content.py     # Content linter
└── index.md            # Homepage
```

---

## Technology

- **Framework**: Jekyll (static site generator)
- **Hosting**: GitHub Pages (auto-deployed on push to `main`)
- **Frontend**: Custom CSS

## License

Content © Steven Stuart. All rights reserved.
