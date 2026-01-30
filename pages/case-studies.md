---
layout: page
title: Case Studies
description: "Real-world architecture challenges, solutions, and results from production systems"
permalink: /case-studies.html
---

<div class="case-studies-hero">
  <p class="hero-tagline">Real systems. Real decisions. Real outcomes.</p>
  <p class="hero-description">Deep dives into production architecture: the problems faced, decisions made, tradeoffs accepted, and lessons learned. Some succeeded. Some failed. All taught something worth sharing.</p>
</div>

<div class="case-studies-grid">
{% assign sorted_case_studies = site.case_studies | sort: 'date' | reverse %}
{% for case_study in sorted_case_studies %}
  <article class="case-study-card {% if case_study.category %}category-{{ case_study.category }}{% endif %}">
    <a href="{{ case_study.url | relative_url }}" class="case-study-link">

      <div class="card-header">
        {% if case_study.category_label %}
        <span class="category-badge category-{{ case_study.category }}">{{ case_study.category_label }}</span>
        {% endif %}
        <span class="case-study-date">{{ case_study.date | date: "%Y" }}</span>
      </div>

      {% if case_study.headline_metric %}
      <div class="headline-metric">
        <span class="metric-value">{{ case_study.headline_metric }}</span>
        {% if case_study.headline_detail %}
        <span class="metric-detail">{{ case_study.headline_detail }}</span>
        {% endif %}
      </div>
      {% endif %}

      <h3 class="card-title">{{ case_study.title }}</h3>

      {% if case_study.subtitle %}
      <p class="card-subtitle">{{ case_study.subtitle }}</p>
      {% endif %}

      <div class="card-meta">
        {% if case_study.role %}
        <div class="role-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          {{ case_study.role }}
        </div>
        {% endif %}
      </div>

      {% if case_study.technologies %}
      <div class="tech-pills">
        {% for tech in case_study.technologies limit:4 %}
        <span class="tech-pill">{{ tech }}</span>
        {% endfor %}
        {% if case_study.technologies.size > 4 %}
        <span class="tech-pill tech-more">+{{ case_study.technologies.size | minus: 4 }}</span>
        {% endif %}
      </div>
      {% endif %}

      <span class="read-more">Read case study <span class="arrow">→</span></span>
    </a>
  </article>
{% endfor %}
</div>

<style>
/* Hero Section */
.case-studies-hero {
  background: linear-gradient(135deg, var(--color-card-bg) 0%, var(--color-bg) 100%);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg, 12px);
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.hero-tagline {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-primary);
  margin: 0 0 var(--spacing-xs, 0.25rem) 0;
}

.hero-description {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--color-text-light);
  margin: 0;
}

/* Case Studies Grid */
.case-studies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

/* Case Study Card */
.case-study-card {
  background: var(--color-card-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg, 12px);
  overflow: hidden;
  transition: all 0.3s ease;
  position: relative;
}

.case-study-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--color-border);
  transition: background 0.3s ease;
}

.case-study-card.category-success::before {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.case-study-card.category-failure::before {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.case-study-card.category-decision::before {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.case-study-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  border-color: var(--color-primary);
}

.case-study-link {
  display: block;
  padding: var(--spacing-md);
  text-decoration: none;
  color: inherit;
  height: 100%;
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.category-badge {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 10px;
  border-radius: 20px;
  background: var(--color-bg);
  color: var(--color-text-light);
}

.category-badge.category-success {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
}

.category-badge.category-failure {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.category-badge.category-decision {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.case-study-date {
  font-size: 0.85rem;
  color: var(--color-text-light);
}

/* Headline Metric */
.headline-metric {
  background: linear-gradient(135deg, var(--color-bg) 0%, var(--color-card-bg) 100%);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  padding: var(--spacing-xs, 0.25rem) var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
  text-align: center;
}

.metric-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1.2;
}

.metric-detail {
  display: block;
  font-size: 0.75rem;
  color: var(--color-text-light);
}

/* Card Content */
.card-title {
  font-size: 1.15rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.4;
}

.card-subtitle {
  font-size: 0.9rem;
  color: var(--color-text-light);
  margin: 0 0 var(--spacing-md) 0;
  line-height: 1.5;
}

/* Card Meta */
.card-meta {
  margin-bottom: var(--spacing-md);
}

.role-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  color: var(--color-text-light);
  background: var(--color-bg);
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid var(--color-border);
}

.role-badge svg {
  opacity: 0.7;
}

/* Tech Pills */
.tech-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: var(--spacing-md);
}

.tech-pill {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 3px 10px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  color: var(--color-text-light);
  transition: all 0.2s ease;
}

.tech-more {
  background: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.case-study-card:hover .tech-pill {
  border-color: var(--color-primary);
}

/* Read More */
.case-study-card .read-more {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-primary);
  transition: gap 0.2s ease;
}

.case-study-card:hover .read-more {
  gap: 8px;
}

.read-more .arrow {
  transition: transform 0.2s ease;
}

.case-study-card:hover .read-more .arrow {
  transform: translateX(4px);
}

/* Responsive */
@media (max-width: 768px) {
  .case-studies-hero {
    padding: var(--spacing-xs, 0.25rem) var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
  }

  .hero-tagline {
    font-size: 1rem;
  }

  .hero-description {
    font-size: 0.8rem;
  }

  .case-studies-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }

  .case-study-link {
    padding: var(--spacing-sm);
  }

  .card-title {
    font-size: 1rem;
  }

  .card-subtitle {
    font-size: 0.85rem;
  }

  .headline-metric {
    padding: 0.2rem var(--spacing-xs, 0.25rem);
  }

  .metric-value {
    font-size: 0.95rem;
  }

  .metric-detail {
    font-size: 0.7rem;
  }
}
</style>
