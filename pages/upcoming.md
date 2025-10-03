---
layout: page
title: Upcoming Content
description: "Planned features and content coming to stevenstuartm.com"
permalink: /upcoming/
---

Stay tuned for new features and content I'm working on. Here's what's on the roadmap:

<div id="upcoming-list" class="upcoming-list">
  <!-- Content will be generated from JSON data -->
</div>

<script>
// Load upcoming items from JSON file
fetch('{{ "/assets/data/upcoming-items.json" | relative_url }}')
  .then(response => response.json())
  .then(data => {
    renderUpcomingItems(data);
  })
  .catch(error => {
    console.error('Error loading upcoming items:', error);
    document.getElementById('upcoming-list').innerHTML = '<p>Unable to load upcoming items. Please try again later.</p>';
  });

function renderUpcomingItems(items) {
  const container = document.getElementById('upcoming-list');

  // Sort items by delivery date (earliest first)
  const sortedItems = items.sort((a, b) => {
    return new Date(a.deliveryDate) - new Date(b.deliveryDate);
  });

  let html = '';

  sortedItems.forEach(item => {
    // Format the date for display (parse as local date to avoid timezone issues)
    const [year, month, day] = item.deliveryDate.split('-');
    const date = new Date(year, month - 1, day);
    const formattedDate = date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    // Format status for display
    const statusDisplay = item.status.charAt(0).toUpperCase() + item.status.slice(1);

    html += `
      <div class="upcoming-item status-${item.status}">
        <div class="upcoming-header">
          <div class="upcoming-title-row">
            <h3>${item.title}</h3>
            <span class="status-badge status-${item.status}">${statusDisplay}</span>
          </div>
          <span class="delivery-date">${formattedDate}</span>
        </div>
        <p class="upcoming-description">${item.description}</p>
      </div>
    `;
  });

  container.innerHTML = html;
}
</script>
