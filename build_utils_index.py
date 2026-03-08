#!/usr/bin/env python3
"""
Generate an index page for the utils directory.
Scans all .html files and creates a searchable index.
Terminal brutalist theme (#CEFF00 on black).
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

        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else html_file.stem.replace('-', ' ').title()

        # Extract description from meta or first p tag
        desc_match = re.search(r'<p[^>]*class="[^"]*text-gray-600[^"]*"[^>]*>(.*?)</p>', content, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else "A useful browser-based tool"

        return title, description
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return html_file.stem.replace('-', ' ').title(), "A useful browser-based tool"


def get_file_modified_time(file_path):
    """Get the last modified time of a file."""
    return datetime.fromtimestamp(os.path.getmtime(file_path))


def generate_index():
    """Generate the utils index page."""
    # Find all HTML files (excluding index.html)
    html_files = [f for f in UTILS_DIR.glob("*.html") if f.name != "index.html"]

    if not html_files:
        print("No HTML files found in utils directory")
        return

    # Extract info for each file
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

    # Sort by modified time (newest first)
    tools.sort(key=lambda x: x['modified'], reverse=True)

    now = datetime.now()

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utils - Browser-Based Tools</title>
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
            --white: #ccc;
            --font-mono: 'Fragment Mono', 'SF Mono', 'Fira Code', monospace;
        }}

        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

        html {{ font-size: 15px; }}

        body {{
            font-family: var(--font-mono);
            background: var(--black);
            color: var(--green);
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

        /* Tool cards */
        .tools-grid {{
            display: grid;
            gap: 0.75rem;
        }}

        .tool-card {{
            border: 1px solid var(--gray);
            padding: 1rem;
            background: var(--dark);
            transition: all 0.15s ease;
        }}

        .tool-card:hover {{
            border-color: var(--green);
            box-shadow: 3px 3px 0 var(--green-dim);
        }}

        .tool-card h2 {{
            font-size: 1rem;
            font-weight: 700;
            color: var(--green);
            margin-bottom: 0.3rem;
        }}

        .tool-card h2 a {{
            color: var(--green);
            border-bottom: none;
        }}

        .tool-card h2 a:hover {{
            color: var(--green-bright);
            text-shadow: 0 0 10px var(--green-glow);
            border-bottom: none;
        }}

        .tool-card .desc {{
            color: var(--white);
            font-size: 0.8rem;
            margin-bottom: 0.5rem;
        }}

        .tool-card .meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.7rem;
            color: var(--gray-light);
        }}

        .tool-card .meta a {{
            color: var(--green-dim);
            font-size: 0.75rem;
            border: 1px solid var(--gray);
            padding: 0.15rem 0.5rem;
            border-bottom: 1px solid var(--gray);
        }}

        .tool-card .meta a:hover {{
            background: var(--green);
            color: var(--black);
            border-color: var(--green);
        }}

        /* Terminal info box */
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
        }}
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="page-header">
            <h1>utils</h1>
            <p>Browser-based tools that run entirely in your browser. No data leaves your device.</p>
            <a href="/" class="back-link">[&lt;- back to blog]</a>
        </div>

        <input
            type="text"
            id="search"
            placeholder="$ grep -i 'search' tools/*"
            class="search-box"
            onkeyup="filterTools()"
        >

        <div class="tools-grid" id="tools-grid">
"""

    # Add tool cards
    for tool in tools:
        html += f"""            <div class="tool-card">
                <h2><a href="{tool['filename']}">{tool['title']}</a></h2>
                <p class="desc">{tool['description']}</p>
                <div class="meta">
                    <span>{tool['modified'].strftime('%Y-%m-%d')}</span>
                    <a href="{tool['filename']}">[open]</a>
                </div>
            </div>
"""

    html += f"""        </div>

        <div class="no-results" id="no-results">
            <p>no tools found</p>
            <p>try a different search term</p>
        </div>

        <div class="info-box">
            <div class="info-box-header">~/about</div>
            <div class="info-box-body">
                <p>All tools are self-contained HTML files that run entirely in your browser. No servers, no tracking, no data collection. Fork them, modify them, share them.</p>
                <p><strong>total tools:</strong> {len(tools)}</p>
            </div>
        </div>

        <div class="page-footer">
            <p>generated {now.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </div>

    <script>
        function filterTools() {{
            const searchTerm = document.getElementById('search').value.toLowerCase();
            const toolCards = document.querySelectorAll('.tool-card');
            const noResults = document.getElementById('no-results');
            let visibleCount = 0;

            toolCards.forEach(card => {{
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    card.style.display = 'block';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
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
    print(f"  Found {len(tools)} tools")


if __name__ == "__main__":
    generate_index()
