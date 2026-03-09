# Blog Revival - Setup Complete! 🎉

Your blog has been restructured with three main sections: Blog, Utils, and Free Game.

## What Was Created

### Directory Structure
```
├── _posts/                  # Jekyll blog posts
├── about.md                 # Updated about page
├── utils/                   # Browser-based tools
│   ├── index.html          # Auto-generated index
│   ├── json-formatter.html
│   ├── base64-converter.html
│   ├── uuid-generator.html
│   └── python-playground.html  # WASM-based Python runner
├── free-game/              # Code snippets by topic
│   ├── index.html          # Auto-generated index
│   ├── javascript/
│   ├── python/
│   ├── web/
│   ├── wasm/
│   └── cli/
├── build_utils_index.py    # Index generator for utils
├── build_freegame_index.py # Index generator for free-game
└── rebuild_indices.sh      # Rebuild both indices

```

### Created Tools

**Utils (4 tools):**
1. JSON Formatter - Format, validate, and minify JSON
2. Base64 Converter - Encode/decode with file support
3. UUID Generator - Generate UUIDs with batch support
4. Python Playground - Run Python in browser via WASM (with NumPy!)

**Free Game Snippets (6 snippets across 5 topics):**
- JavaScript: copy-to-clipboard, localStorage helpers
- Web: single-file HTML template
- Python: Pyodide WASM setup
- WASM: SQLite in browser
- CLI: Git aliases

## Next Steps

### 1. Test Locally

```bash
# Install Jekyll dependencies (if needed)
bundle install

# Build the indices
./rebuild_indices.sh

# Serve the site
bundle exec jekyll serve

# Visit http://localhost:4000
```

### 2. Add Content

**New util:**
```bash
# 1. Create HTML file
touch utils/my-tool.html

# 2. Use the template from free-game/web/single-file-html-template.md

# 3. Rebuild index
python3 build_utils_index.py
```

**New free-game snippet:**
```bash
# 1. Create markdown file in appropriate topic
touch free-game/javascript/new-snippet.md

# 2. Write your snippet with H1 title

# 3. Rebuild index
python3 build_freegame_index.py
```

### 3. Deploy

```bash
# Commit and push to deploy via GitHub Pages
git add .
git commit -m "Revived blog with utils and free-game sections"
git push origin master
```

## Key Features

### Utils
- ✅ Single-file HTML (no build step)
- ✅ Tailwind CSS via CDN
- ✅ Copy-to-clipboard functionality
- ✅ localStorage for persistence
- ✅ WASM support (Python, SQLite)
- ✅ Auto-generated searchable index

### Free Game
- ✅ Markdown-based snippets
- ✅ Organized by topic
- ✅ LLM-prompt friendly
- ✅ Auto-generated browsable index
- ✅ Search functionality

### Navigation
- ✅ Updated Jekyll config with custom navigation
- ✅ About page updated
- ✅ All sections linked in header

## Design Philosophy

Inspired by [Simon Willison's approach](https://simonwillison.net/2025/Dec/10/html-tools/):

1. **No build steps** - Everything runs in the browser
2. **No frameworks** - No React, just vanilla JS
3. **CDN dependencies** - No npm, no bundlers
4. **Client-side only** - No servers, no tracking
5. **localStorage** - Keep API keys and data local
6. **Copy-paste friendly** - Easy to use and share

## Maintenance

### Rebuild Indices
After adding new utils or snippets:
```bash
./rebuild_indices.sh
```

### Git Workflow
```bash
# Regular commits
git add .
git commit -m "Added new tool/snippet"
git push

# The indices are committed to git, so they deploy with your site
```

## Useful Commands

```bash
# Serve locally
bundle exec jekyll serve

# Rebuild just utils index
python3 build_utils_index.py

# Rebuild just free-game index
python3 build_freegame_index.py

# Rebuild both
./rebuild_indices.sh

# Check what's in each section
ls utils/*.html
ls free-game/*/*.md
```

## What's Next?

Ideas for expansion:
- Add more utils (color picker, regex tester, markdown preview, etc.)
- Add more free-game topics (databases, APIs, DevOps, etc.)
- Add search across all sections
- Add RSS feed for free-game snippets
- Add "copy code" buttons in free-game snippets
- Create GitHub Action to auto-rebuild indices on push

Happy coding! 🚀
