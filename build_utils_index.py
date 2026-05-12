#!/usr/bin/env python3
"""
Generate an index page for the utils directory.
Scans all .html files and creates a searchable index that inherits the site theme.
"""

import os
from pathlib import Path
from datetime import datetime
import re

UTILS_DIR = Path(__file__).parent / "utils"
OUTPUT_FILE = UTILS_DIR / "index.html"


def extract_title_and_description(html_file):
    """Extract title and description from HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else html_file.stem.replace('-', ' ').title()

        desc_match = re.search(r'<p[^>]*class="[^"]*text-gray-600[^"]*"[^>]*>(.*?)</p>', content, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else "A browser-based tool."

        return title, description
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return html_file.stem.replace('-', ' ').title(), "A browser-based tool."


def get_file_modified_time(file_path):
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def generate_index():
    html_files = [f for f in UTILS_DIR.glob("*.html") if f.name != "index.html"]

    if not html_files:
        print("No HTML files found in utils directory")
        return

    tools = []
    for html_file in html_files:
        title, description = extract_title_and_description(html_file)
        modified = get_file_modified_time(html_file)
        tools.append({
            'filename': html_file.name,
            'title': title,
            'description': description,
            'modified': modified
        })

    tools.sort(key=lambda x: x['modified'], reverse=True)

    html = """---
layout: default
title: Utils
permalink: /utils/
---

<header class="hero" style="margin-bottom:48px;">
  <h1 class="hero-title" style="font-size:clamp(3rem,8vw,6rem);">Utils.</h1>
  <p class="hero-subtitle">Single-file browser tools. No build step, no tracking, no servers. Fork any of them &mdash; they all run client-side.</p>
</header>

<section>
  <p class="section-label">tools</p>

  <input
    type="text"
    id="utils-search"
    placeholder="filter tools&hellip;"
    class="utils-search"
    onkeyup="filterUtils()"
    autocomplete="off"
  >

  <ul class="post-list" id="utils-list">
"""

    for tool in tools:
        html += f"""    <li data-search="{tool['title'].lower()} {tool['description'].lower()}">
      <a class="post-list-link" href="{tool['filename']}">
        <span class="post-title-text">{tool['title']}</span>
        <span class="post-meta">{tool['modified'].strftime('%Y &middot; %b %d')}</span>
        <span class="post-excerpt">{tool['description']}</span>
      </a>
    </li>
"""

    html += """  </ul>

  <p class="post-excerpt" id="utils-empty" style="display:none;margin-top:24px;">No tools match that filter.</p>
</section>

<style>
  .utils-search {
    width: 100%;
    max-width: 480px;
    padding: 10px 14px;
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid var(--rule);
    border-radius: 4px;
    font: inherit;
    font-size: 0.95rem;
    color: var(--ink);
    margin-bottom: 16px;
    transition: border-color 0.15s, background 0.15s;
  }
  .utils-search:focus {
    outline: none;
    border-color: var(--orange);
    background: #ffffff;
  }
  .utils-search::placeholder { color: var(--muted-soft); }
</style>

<script>
  function filterUtils() {
    var q = document.getElementById('utils-search').value.toLowerCase().trim();
    var items = document.querySelectorAll('#utils-list > li');
    var visible = 0;
    items.forEach(function (li) {
      var hay = li.getAttribute('data-search') || '';
      var match = !q || hay.indexOf(q) !== -1;
      li.style.display = match ? '' : 'none';
      if (match) visible++;
    });
    document.getElementById('utils-empty').style.display = visible === 0 ? '' : 'none';
  }
</script>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE}")
    print(f"  Found {len(tools)} tools")


if __name__ == "__main__":
    generate_index()
