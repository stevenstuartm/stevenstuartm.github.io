---
layout: page
title: Case Studies
description: "Real-world architecture challenges, solutions, and results from production systems"
permalink: /case-studies.html
---

Deep dives into real projects: the problems faced, architectural decisions made, tradeoffs considered, and measurable outcomes achieved.

---

<div class="guides-page">
    <div class="guides-main">
        <div class="guide-cards">
{% if site.case_studies and site.case_studies.size > 0 %}
{% assign sorted_case_studies = site.case_studies | sort: 'date' | reverse %}
  {% for case_study in sorted_case_studies %}
  <article class="guide-card">
    <a href="{{ case_study.url | relative_url }}" class="guide-link">
      <h3>{{ case_study.title }}</h3>
      {% if case_study.subtitle %}
      <div class="guide-card-meta">
        <span class="case-study-subtitle">{{ case_study.subtitle }}</span>
      </div>
      {% endif %}
      {% if case_study.description %}
      <p class="guide-excerpt">{{ case_study.description }}</p>
      {% elsif case_study.excerpt %}
      <p class="guide-excerpt">{{ case_study.excerpt | strip_html | truncatewords: 40 }}</p>
      {% endif %}
      <span class="read-more">Read case study →</span>
    </a>
  </article>
  {% endfor %}
{% else %}
  <div class="coming-soon-message">
    <h3>Case Studies Coming Soon</h3>
    <p>I'm currently documenting detailed case studies of architecture projects, including challenges, solutions, and measurable results. Check back soon for in-depth analysis of:</p>
    <ul>
      <li><strong>80% Cloud Cost Reduction</strong> — Infrastructure optimization and service consolidation strategy</li>
      <li><strong>Serverless Migration at Scale</strong> — First AWS Lambda adoption and architecture patterns</li>
      <li><strong>Microservices Stability</strong> — Eliminating transaction instability in distributed systems</li>
      <li><strong>Real-time Notification Platform</strong> — Building instant alerts across web and mobile channels</li>
    </ul>
    <p>Want to be notified when these are published? <a href="{{ '/about.html' | relative_url }}">Connect with me on LinkedIn</a>.</p>
  </div>
{% endif %}
        </div>
    </div>
</div>

<style>
.case-study-subtitle {
  color: var(--color-text-light);
  font-size: 0.95rem;
}

.coming-soon-message {
  background-color: var(--color-card-bg);
  border-left: 4px solid var(--color-accent);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  text-align: center;
  grid-column: 1 / -1;
}

.coming-soon-message h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.coming-soon-message p {
  margin-bottom: var(--spacing-md);
  line-height: 1.8;
}

.coming-soon-message ul {
  text-align: left;
  max-width: 600px;
  margin: var(--spacing-lg) auto;
  list-style: none;
  padding: 0;
}

.coming-soon-message ul li {
  margin-bottom: var(--spacing-sm);
  padding-left: var(--spacing-md);
  position: relative;
}

.coming-soon-message ul li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: var(--color-primary);
}
</style>
