# Site Rebranding Plan

This site (stevenstuartm.github.io) is being refocused as a **personal marketing and mentorship site** for Steven Stuart.
The broader publishing content (study guides, tech radar, blog posts) has moved to the partner site: **lucentowl.com**.

---

## Context

- **This site**: Personal brand — hiring pitch, mentorship, about, and personal blog content authored by Steven
- **Partner site (lucentowl.com)**: Multi-author publishing platform — study guides, tech radar, general posts
- **URL structure**: Paths are identical across both sites, so lucentowl.com/X corresponds to stevenstuartm.github.io/X

---

## Work Items

### 1. Custom 404 Page — `404.html` ✅
- Keep existing extensionless-URL → `.html` redirect logic
- Add friendly message for genuine 404s: content has moved to lucentowl.com
- Use JavaScript to construct the equivalent lucentowl.com URL from `window.location.pathname` and display it as a visible, copyable link (no silent redirect)
- Message: generic ("content may have moved to our partner site")

### 2. Remove Sections — Study Guides, Tech Radar ✅
- [x] Delete `pages/study-guides.md`
- [x] Delete `pages/tech-radar.md`
- [x] Delete `pages/study-routine.md`
- [x] Remove nav links — dropped "Tech Radar" from Insights dropdown, removed entire "Learning" dropdown from `_includes/header.html`
- [x] Keep `_guides/` directory and files intact (not deleted — just not navigable from this site)
- Note: Inbound links to these pages hit the 404 page, which directs users to lucentowl.com

### 3. Homepage — `index.md` ✅
- [x] Update `featured_items` URLs to point to lucentowl.com
- [x] Add partner site callout in `_layouts/home.html` (between hero and featured cards)
- [x] Study Guides and Tech Radar content-type cards now link to lucentowl.com (external, opens in new tab)

### 4. About Page — `pages/about.md` ✅
- [x] Added lucentowl.com mention in the "Let's Connect" section

---

## Decisions

| Decision | Choice | Reason |
|---|---|---|
| 404 redirect behavior | Visible link, not silent redirect | Prudent users distrust magic redirects; transparency builds trust |
| 404 message tone | Generic ("may have moved") | No maintenance burden if lucentowl.com paths ever change |
| Content deletion | Stub/remove pages, keep files | Avoids accidental data loss; 404 page covers inbound links |

---

## Status

- `_posts/` emptied (all moved to `_drafts/`) ✅
- 404 page updated ✅
- Study guide / tech radar pages removed ✅
- Nav updated (removed Tech Radar and Learning dropdown) ✅
- Homepage updated ✅
- About page updated ✅
- CLAUDE.md and content guides updated ✅
- `_config.yml` exclude list updated ✅

### 6. Remove Blog and Case Studies ✅
- [x] Deleted `pages/blog.md` and `pages/case-studies.md`
- [x] Removed Case Studies and Blog from Insights nav dropdown; flattened to direct Philosophy link
- [x] Removed entire content-type-cards section from `_layouts/home.html`
- [x] Updated partner notice to mention blog posts

### Remaining
- [ ] Style the `.partner-notice` element in `assets/css/main.css` to match the site design
- [ ] Decide what the homepage should feature if not linking to lucentowl.com content (or keep current featured items pointing there)
