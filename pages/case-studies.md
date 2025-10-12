---
layout: page
title: Case Studies
description: "Real-world architecture challenges, solutions, and results from production systems"
permalink: /case-studies.html
---

Deep dives into real projects: the problems faced, architectural decisions made, tradeoffs considered, and measurable outcomes achieved.

<div style="text-align: center; margin: 1.5rem 0;">
  <p style="margin-bottom: 0.75rem; color: var(--color-text-light); font-size: 0.9rem;">Find these case studies valuable?</p>
  {% include share-linkedin.html %}
</div>

---

<div class="case-studies-list">
{% if site.case_studies and site.case_studies.size > 0 %}
{% assign sorted_case_studies = site.case_studies | sort: 'date' | reverse %}
  {% for case_study in sorted_case_studies %}
  <article class="case-study-card">
    <div class="case-study-card-header">
      <h2><a href="{{ case_study.url | relative_url }}">{{ case_study.title }}</a></h2>
      {% if case_study.subtitle %}
      <p class="case-study-card-subtitle">{{ case_study.subtitle }}</p>
      {% endif %}
    </div>

    <div class="case-study-card-meta">
      {% if case_study.company %}
      <span class="meta-item"><strong>Company:</strong> {{ case_study.company }}</span>
      {% endif %}
      {% if case_study.role %}
      <span class="meta-item"><strong>Role:</strong> {{ case_study.role }}</span>
      {% endif %}
      {% if case_study.date %}
      <span class="meta-item"><strong>Year:</strong> {{ case_study.date | date: "%Y" }}</span>
      {% endif %}
    </div>

    {% if case_study.excerpt %}
    <p class="case-study-card-excerpt">{{ case_study.excerpt | strip_html | truncatewords: 40 }}</p>
    {% endif %}

    {% if case_study.technologies %}
    <div class="case-study-card-technologies">
      {% for tech in case_study.technologies limit:5 %}
      <span class="tech-tag">{{ tech }}</span>
      {% endfor %}
      {% if case_study.technologies.size > 5 %}
      <span class="tech-tag-more">+{{ case_study.technologies.size | minus: 5 }} more</span>
      {% endif %}
    </div>
    {% endif %}

    <a href="{{ case_study.url | relative_url }}" class="read-more">Read case study →</a>
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

<style>
.case-studies-list {
  margin-top: var(--spacing-xl);
}

.case-study-card {
  background-color: var(--color-card-bg);
  border-left: 4px solid var(--color-primary);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s ease;
}

.case-study-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.case-study-card-header h2 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 1.5rem;
}

.case-study-card-header h2 a {
  color: var(--color-text);
  text-decoration: none;
}

.case-study-card-header h2 a:hover {
  color: var(--color-primary);
}

.case-study-card-subtitle {
  color: var(--color-text-light);
  font-size: 1.1rem;
  margin-bottom: var(--spacing-sm);
}

.case-study-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  font-size: 0.9rem;
  color: var(--color-text-light);
}

.meta-item {
  display: inline-block;
}

.case-study-card-excerpt {
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
  color: var(--color-text);
}

.case-study-card-technologies {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.tech-tag {
  display: inline-block;
  background-color: var(--color-bg);
  color: var(--color-text);
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
  border: 1px solid var(--color-border);
}

.tech-tag-more {
  display: inline-block;
  color: var(--color-text-light);
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
  font-style: italic;
}

.read-more {
  color: var(--color-primary);
  font-weight: 500;
  text-decoration: none;
  display: inline-block;
}

.read-more:hover {
  text-decoration: underline;
}

.coming-soon-message {
  background-color: var(--color-card-bg);
  border-left: 4px solid var(--color-accent);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  text-align: center;
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

@media (max-width: 768px) {
  .case-study-card-meta {
    flex-direction: column;
    gap: var(--spacing-xs);
  }
}
</style>
