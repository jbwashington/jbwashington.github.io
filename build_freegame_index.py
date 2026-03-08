#!/usr/bin/env python3
"""
Generate an index page for the free-game directory.
Scans all .md files organized by topic and creates a browsable index.
Terminal brutalist theme (#CEFF00 on black).
"""

import os
from pathlib import Path
from datetime import datetime
import re

FREEGAME_DIR = Path(__file__).parent / "free-game"
OUTPUT_FILE = FREEGAME_DIR / "index.html"


def extract_title_from_markdown(md_file):
    """Extract the first H1 title from a markdown file."""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    return line[2:].strip()
        # Fallback to filename
        return md_file.stem.replace('-', ' ').title()
    except Exception as e:
        print(f"Error reading {md_file}: {e}")
        return md_file.stem.replace('-', ' ').title()


def get_file_modified_time(file_path):
    """Get the last modified time of a file."""
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def generate_index():
    """Generate the free-game index page."""
    # Find all topic directories
    topic_dirs = [d for d in FREEGAME_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]

    if not topic_dirs:
        print("No topic directories found in free-game directory")
        return

    # Organize snippets by topic
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
            # Relative path from free-game directory
            rel_path = md_file.relative_to(FREEGAME_DIR)
            snippets.append({
                'filename': md_file.name,
                'path': str(rel_path),
                'title': title,
                'modified': modified
            })

        # Sort by modified time (newest first)
        snippets.sort(key=lambda x: x['modified'], reverse=True)
        topics[topic_name] = snippets
        total_snippets += len(snippets)

    # Get recent snippets across all topics
    all_snippets = []
    for topic_name, snippets in topics.items():
        for snippet in snippets:
            snippet['topic'] = topic_name
            all_snippets.append(snippet)
    all_snippets.sort(key=lambda x: x['modified'], reverse=True)
    recent_snippets = all_snippets[:10]

    now = datetime.now()

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Game - Code Snippets & Learnings</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fragment+Mono:ital@0;1&display=swap" rel="stylesheet">
    <style>
        :root {{
            --green: #CEFF00;
            --green-dim: #a5cc00;
            --green-bright: #daff4d;
            --green-glow: rgba(206, 255, 0, 0.15);
            --black: #000;
            --dark: #0a0a0a;
            --gray: #333;
            --gray-light: #666;
            --cyan: #0ff;
            --yellow: #ff0;
            --white: #e5e5e5;
            --font-mono: 'Fragment Mono', 'SF Mono', 'Fira Code', monospace;
        }}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html {{ font-size: 15px; }}

        body {{
            font-family: var(--font-mono);
            background: var(--black);
            color: var(--white);
            line-height: 1.7;
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
        }}

        body::after {{
            content: "";
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0px, rgba(0,0,0,0.05) 1px, transparent 1px, transparent 3px);
            z-index: 9999;
        }}

        body::before {{
            content: "";
            position: fixed; top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            background: radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.4) 100%);
            z-index: 9998;
        }}

        ::selection {{ background: var(--green); color: var(--black); }}

        .wrapper {{
            max-width: 800px;
            margin: 0 auto;
            padding: 1.5rem;
        }}

        a {{
            color: var(--cyan);
            text-decoration: none;
            border-bottom: 1px dashed var(--cyan);
            transition: all 0.15s ease;
        }}

        a:hover {{
            color: var(--yellow);
            border-bottom-color: var(--yellow);
            text-shadow: 0 0 8px rgba(255, 255, 0, 0.3);
        }}

        /* Header */
        .page-header {{
            border-bottom: 2px solid var(--green);
            padding-bottom: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .page-header h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--green-bright);
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .page-header h1::before {{ content: "# "; color: var(--gray-light); }}

        .page-header p {{
            color: var(--white);
            font-size: 0.85rem;
            margin-bottom: 0.75rem;
        }}

        .back-link {{
            font-size: 0.8rem;
            color: var(--green-dim);
            border-bottom: none;
        }}

        .back-link:hover {{
            color: var(--green);
            border-bottom: none;
        }}

        /* Search */
        .search-box {{
            width: 100%;
            padding: 0.6rem 1rem;
            background: var(--dark);
            border: 2px solid var(--gray);
            color: var(--green);
            font-family: var(--font-mono);
            font-size: 0.85rem;
            margin-bottom: 1.5rem;
            transition: border-color 0.15s ease;
        }}

        .search-box:focus {{
            outline: none;
            border-color: var(--green);
            box-shadow: 0 0 10px var(--green-glow);
        }}

        .search-box::placeholder {{ color: var(--gray-light); }}

        /* Section headings */
        .section-heading {{
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--green-bright);
            margin-bottom: 1rem;
            padding-bottom: 0.3rem;
            border-bottom: 1px dashed var(--gray);
        }}

        .section-heading::before {{ content: "## "; color: var(--gray-light); }}

        /* Recent snippets */
        .recent-grid {{
            display: grid;
            gap: 0.5rem;
            grid-template-columns: 1fr 1fr;
            margin-bottom: 2rem;
        }}

        .snippet-card {{
            border: 1px solid var(--gray);
            padding: 0.75rem 1rem;
            background: var(--dark);
            transition: all 0.15s ease;
        }}

        .snippet-card:hover {{
            border-color: var(--green);
            box-shadow: 3px 3px 0 var(--green-dim);
        }}

        .snippet-card .card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.4rem;
        }}

        .snippet-card .tag {{
            font-size: 0.65rem;
            padding: 0.1rem 0.4rem;
            border: 1px solid var(--green-dim);
            color: var(--green-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .snippet-card .date {{
            font-size: 0.65rem;
            color: var(--gray-light);
        }}

        .snippet-card h3 {{
            font-size: 0.85rem;
            font-weight: 700;
        }}

        .snippet-card h3 a {{
            color: var(--green);
            border-bottom: none;
        }}

        .snippet-card h3 a:hover {{
            color: var(--green-bright);
            text-shadow: 0 0 10px var(--green-glow);
            border-bottom: none;
        }}

        /* Topic sections */
        .topic-section {{
            border: 2px solid var(--green);
            margin-bottom: 1rem;
            box-shadow: 4px 4px 0 var(--green-dim);
        }}

        .topic-header {{
            background: var(--green);
            color: var(--black);
            padding: 0.3rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .topic-body {{
            padding: 0.75rem;
            background: var(--dark);
        }}

        .snippet-list {{
            display: grid;
            gap: 0.3rem;
            grid-template-columns: 1fr 1fr;
        }}

        .snippet-item {{
            padding: 0.4rem 0.6rem;
            border: 1px solid transparent;
            transition: all 0.15s ease;
        }}

        .snippet-item:hover {{
            border-color: var(--gray);
            background: rgba(206, 255, 0, 0.03);
        }}

        .snippet-item a {{
            color: var(--cyan);
            font-size: 0.8rem;
            border-bottom: none;
        }}

        .snippet-item a:hover {{
            color: var(--yellow);
            border-bottom: none;
        }}

        /* Info box */
        .info-box {{
            border: 2px solid var(--green);
            margin-top: 2rem;
            box-shadow: 4px 4px 0 var(--green-dim);
        }}

        .info-box-header {{
            background: var(--green);
            color: var(--black);
            padding: 0.3rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .info-box-body {{
            padding: 1rem;
            background: var(--dark);
        }}

        .info-box-body p {{
            color: var(--white);
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }}

        .info-box-body p:last-child {{ margin-bottom: 0; }}

        .info-box-body strong {{ color: var(--green-bright); }}

        /* No results */
        .no-results {{
            display: none;
            text-align: center;
            padding: 3rem 0;
            color: var(--gray-light);
        }}

        .no-results.visible {{ display: block; }}

        .no-results p:first-child {{ font-size: 1rem; margin-bottom: 0.5rem; }}
        .no-results p:last-child {{ font-size: 0.8rem; }}

        /* Footer */
        .page-footer {{
            margin-top: 1.5rem;
            text-align: center;
            font-size: 0.7rem;
            color: var(--gray-light);
            padding-top: 1rem;
            border-top: 1px dashed var(--gray);
        }}

        @media (max-width: 600px) {{
            html {{ font-size: 14px; }}
            .recent-grid, .snippet-list {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="page-header">
            <h1>free game</h1>
            <p>Code snippets and learnings organized by topic. Quick reference for LLM prompts or personal use.</p>
            <a href="/" class="back-link">[&lt;- back to blog]</a>
        </div>

        <input
            type="text"
            id="search"
            placeholder="$ grep -ri 'search' snippets/"
            class="search-box"
            onkeyup="filterSnippets()"
        >

        <h2 class="section-heading">recent snippets</h2>
        <div class="recent-grid">
"""

    # Add recent snippets
    for snippet in recent_snippets:
        html += f"""            <div class="snippet-card">
                <div class="card-top">
                    <span class="tag">{snippet['topic']}</span>
                    <span class="date">{snippet['modified'].strftime('%Y-%m-%d')}</span>
                </div>
                <h3><a href="{snippet['path']}">{snippet['title']}</a></h3>
            </div>
"""

    html += """        </div>

        <h2 class="section-heading">browse by topic</h2>
"""

    # Add topics with snippets
    for topic_name, snippets in sorted(topics.items()):
        topic_display = topic_name.replace('-', ' ')
        count_label = f"{len(snippets)} snippet{'s' if len(snippets) != 1 else ''}"
        html += f"""        <div class="topic-section">
            <div class="topic-header">
                <span>~/{topic_display}</span>
                <span>{count_label}</span>
            </div>
            <div class="topic-body">
                <div class="snippet-list">
"""

        for snippet in snippets:
            html += f"""                    <div class="snippet-item">
                        <a href="{snippet['path']}">{snippet['title']}</a>
                    </div>
"""

        html += """                </div>
            </div>
        </div>
"""

    html += f"""
        <div class="no-results" id="no-results">
            <p>no snippets found</p>
            <p>try a different search term</p>
        </div>

        <div class="info-box">
            <div class="info-box-header">~/about</div>
            <div class="info-box-body">
                <p>These are concise, single-topic snippets that I've learned and want to remember. Perfect for copy-pasting into LLM prompts or referencing later. All snippets are markdown files that can be easily read and modified.</p>
                <p><strong>topics:</strong> {len(topics)} | <strong>total snippets:</strong> {total_snippets}</p>
            </div>
        </div>

        <div class="page-footer">
            <p>generated {now.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>

    <script>
        function filterSnippets() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const snippetCards = document.querySelectorAll('.snippet-card');
            const topicSections = document.querySelectorAll('.topic-section');
            const noResults = document.getElementById('no-results');
            let visibleCount = 0;

            snippetCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    card.style.display = 'block';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            topicSections.forEach(section => {{
                const snippetItems = section.querySelectorAll('.snippet-item');
                let sectionHasVisible = false;

                snippetItems.forEach(item => {{
                    const text = item.textContent.toLowerCase();
                    if (text.includes(searchTerm)) {{
                        item.style.display = 'block';
                        sectionHasVisible = true;
                        visibleCount++;
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});

                section.style.display = sectionHasVisible ? 'block' : 'none';
            }});

            if (visibleCount === 0) {{
                noResults.classList.add('visible');
            }} else {{
                noResults.classList.remove('visible');
            }}
        }}
    </script>
</body>
</html>
"""

    # Write the file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  Found {len(topics)} topics with {total_snippets} snippets")


if __name__ == "__main__":
    generate_index()
