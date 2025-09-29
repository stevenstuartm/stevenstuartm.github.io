---
layout: page
title: Blog
---

{% if site.posts.size > 0 %}
<div class="post-list">
    {% for post in site.posts %}
    <article class="post-preview">
        <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
        <p class="post-meta">
            <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
        </p>
        {% if post.excerpt %}
        <p class="post-excerpt">{{ post.excerpt | strip_html | truncatewords: 50 }}</p>
        {% endif %}
        <a href="{{ post.url | relative_url }}" class="read-more">Read more →</a>
    </article>
    {% endfor %}
</div>
{% else %}
<p>No posts yet. Add your first post to the <code>_posts/</code> directory using the format: <code>YYYY-MM-DD-title.md</code></p>
{% endif %}