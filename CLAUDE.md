# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a **hybrid Jekyll + static HTML site** with three main content sections:

1. **Blog** (`_posts/`) - Traditional Jekyll blog posts
2. **Utils** (`utils/`) - Single-file HTML browser tools (no build step, no frameworks)
3. **Free Game** (`free-game/`) - Markdown code snippets organized by topic for LLM prompting

### Critical Architectural Pattern: Auto-Generated Indices

The utils and free-game sections use **Python scripts to auto-generate their index pages**:

- `build_utils_index.py` - Scans `utils/*.html`, extracts titles/descriptions from HTML tags, generates `utils/index.html`
- `build_freegame_index.py` - Scans `free-game/*/*.md`, extracts H1 titles, generates `free-game/index.html`

**Important:** These indices are committed to git and deployed with the site. They are NOT generated during Jekyll build.

### Navigation

Custom navigation is defined in `_config.yml` via `header_pages`:
```yaml
header_pages:
    - about.md
    - utils/index.html
    - free-game/index.html
```

Changes to `_config.yml` require restarting the Jekyll server.

## Development Commands

### Local Development
```bash
# Install Jekyll dependencies
bundle install

# Rebuild indices (MUST run after adding utils/snippets)
./rebuild_indices.sh
# Or individually:
python3 build_utils_index.py
python3 build_freegame_index.py

# Serve site locally
bundle exec jekyll serve
# Visit http://localhost:4000
```

### Adding Content

**New blog post:**
```bash
# Create file: _posts/YYYY-MM-DD-title.md
# Jekyll picks it up automatically
```

**New util:**
```bash
# 1. Create utils/tool-name.html (use template in free-game/web/single-file-html-template.md)
# 2. Rebuild index
python3 build_utils_index.py
```

**New free-game snippet:**
```bash
# 1. Create free-game/{topic}/snippet-name.md
# 2. Ensure first line is H1 title: # Title Here
# 3. Rebuild index
python3 build_freegame_index.py
```

## Utils Design Philosophy

Utils follow Simon Willison's single-file HTML methodology ([reference](https://simonwillison.net/2025/Dec/10/html-tools/)):

### Non-Negotiable Constraints
- **Single-file HTML** - All HTML, CSS, JS in one file
- **No React/frameworks** - Vanilla JavaScript only
- **No build steps** - No npm, webpack, bundlers
- **CDN dependencies** - Load from CDNs (Tailwind, Pyodide, etc.)
- **Client-side only** - Everything runs in browser
- **localStorage for persistence** - Never send data to servers

### Required Features
Every util must include:
- Tailwind CSS via CDN: `<script src="https://cdn.tailwindcss.com"></script>`
- Copy-to-clipboard functionality using `navigator.clipboard.writeText()`
- localStorage for state persistence (user input, settings, API keys)
- Responsive design (works on mobile)

### Index Generation Details
`build_utils_index.py` extracts metadata via regex:
- **Title**: From `<title>` tag
- **Description**: From first `<p class="...text-gray-600...">` tag

When creating utils, ensure these tags exist for proper index generation.

## Free Game Design Philosophy

Free game snippets are optimized for **copy-pasting into LLM prompts**:

- One topic per file
- Concise, self-contained examples
- Organized by topic directories (`javascript/`, `python/`, `web/`, `wasm/`, `cli/`)
- First line must be H1 title for index generation: `# Title`

## Deployment

Site deploys to GitHub Pages on push to `master` branch.

**Critical:** Index files (`utils/index.html`, `free-game/index.html`) must be committed to git. They are not generated during deployment.

## File Locations

```
_posts/                      # Jekyll blog posts
utils/                       # Single-file HTML tools
  *.html                     # Individual tools
  index.html                 # Auto-generated (commit this!)
free-game/                   # Code snippets
  {topic}/*.md              # Snippets by topic
  index.html                # Auto-generated (commit this!)
build_utils_index.py         # Index generator
build_freegame_index.py      # Index generator
rebuild_indices.sh           # Convenience script
_config.yml                  # Jekyll config (restart server after changes)
```

## Common Workflow

```bash
# Add new util
vim utils/my-tool.html
python3 build_utils_index.py
git add utils/
git commit -m "Add my-tool util"

# Add new snippet
vim free-game/javascript/my-snippet.md
python3 build_freegame_index.py
git add free-game/
git commit -m "Add my-snippet"

# Deploy
git push origin master
```
