---
layout: page
title: Blog
description: "Learn from real-world software architecture challenges: system design patterns, AWS optimization, Domain-Driven Design, microservices, and engineering leadership insights."
permalink: /blog/
---

{% if site.posts.size > 0 %}
<div class="post-list">
    {% for post in site.posts %}
    <article class="post-preview">
        <a href="{{ post.url | relative_url }}" class="post-link">
            <h3>{{ post.title }}</h3>
            <p class="post-meta">
                <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
            </p>
            {% if post.excerpt %}
            <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 50 }}</p>
            {% endif %}
            <span class="read-more">Read more →</span>
        </a>
    </article>
    {% endfor %}
</div>
{% else %}
<p>No posts yet. Add your first post to the <code>_posts/</code> directory using the format: <code>YYYY-MM-DD-title.md</code></p>
{% endif %}