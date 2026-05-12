#!/usr/bin/env python3
"""
Generate an index page for the free-game directory.
Scans all .md files organized by topic and creates a browsable index
that inherits the site theme.
"""

import os
from pathlib import Path
from datetime import datetime

FREEGAME_DIR = Path(__file__).parent / "free-game"
OUTPUT_FILE = FREEGAME_DIR / "index.html"


def extract_title_from_markdown(md_file):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
        return md_file.stem.replace('-', ' ').title()
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return md_file.stem.replace('-', ' ').title()


def get_file_modified_time(file_path):
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def generate_index():
    topic_dirs = [d for d in FREEGAME_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]

    if not topic_dirs:
        print("No topic directories found in free-game directory")
        return

    topics = {}
    total_snippets = 0

    for topic_dir in sorted(topic_dirs):
        topic_name = topic_dir.name
        md_files = list(topic_dir.glob("*.md"))

        if not md_files:
            continue

        snippets = []
        for md_file in md_files:
            title = extract_title_from_markdown(md_file)
            modified = get_file_modified_time(md_file)
            rel_path = md_file.relative_to(FREEGAME_DIR)
            snippets.append({
                'filename': md_file.name,
                'path': str(rel_path),
                'title': title,
                'modified': modified,
                'topic': topic_name,
            })

        snippets.sort(key=lambda x: x['modified'], reverse=True)
        topics[topic_name] = snippets
        total_snippets += len(snippets)

    html = """---
layout: default
title: Free Game
permalink: /free-game/
---

<header class="hero" style="margin-bottom:48px;">
  <h1 class="hero-title" style="font-size:clamp(3rem,8vw,6rem);">Free<br>Game.</h1>
  <p class="hero-subtitle">Self-contained code snippets organized by topic. Copy-paste them into LLM prompts or use them as quick reference.</p>
</header>

<section>
  <p class="section-label">browse by topic</p>
  <div class="featured-masonry" id="freegame-masonry">
"""

    for topic_name in sorted(topics.keys()):
        snippets = topics[topic_name]
        count_label = f"{len(snippets)} snippet{'s' if len(snippets) != 1 else ''}"
        html += f"""    <div class="featured-card" data-topic="{topic_name}">
      <div class="featured-card-tag">{topic_name}</div>
      <h3 class="featured-card-title">~/{topic_name}</h3>
      <ul style="list-style:none;margin:10px 0 0;padding:0;">
"""
        for snippet in snippets:
            html += f"""        <li style="margin:4px 0;font-size:0.9rem;"><a href="{snippet['path']}" style="color:var(--ink);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s,color .15s;" onmouseover="this.style.color='var(--orange)';this.style.borderBottomColor='var(--orange)';" onmouseout="this.style.color='var(--ink)';this.style.borderBottomColor='transparent';">{snippet['title']}</a></li>
"""
        html += f"""      </ul>
      <div class="featured-card-meta">
        <span>{count_label}</span>
      </div>
    </div>
"""

    html += f"""  </div>
</section>

<p class="section-label" style="margin-top:48px;">{len(topics)} topics &middot; {total_snippets} snippets</p>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated {OUTPUT_FILE}")
    print(f"  Found {len(topics)} topics with {total_snippets} snippets")


if __name__ == "__main__":
    generate_index()
