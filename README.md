# James Washington's Blog

Personal website and blog with browser-based tools and code snippets.

## Structure

- **Blog** (`/_posts/`) - Jekyll blog posts
- **Utils** (`/utils/`) - Single-file HTML tools that run entirely in the browser
- **Free Game** (`/free-game/`) - Code snippets and learnings organized by topic

## Local Development

### Prerequisites

- Ruby and Bundler
- Python 3 (for building indices)

### Setup

```bash
# Install dependencies
bundle install

# Build the utils and free-game indices
python3 build_utils_index.py
python3 build_freegame_index.py

# Serve the site locally
bundle exec jekyll serve

# Visit http://localhost:4000
```

### Adding New Content

**New blog post:**
```bash
# Create a new file in _posts/
touch _posts/YYYY-MM-DD-title.md
```

**New util:**
```bash
# Create a new HTML file in utils/
touch utils/my-new-tool.html

# Rebuild the index
python3 build_utils_index.py
```

**New free-game snippet:**
```bash
# Create a new markdown file in the appropriate topic directory
touch free-game/javascript/my-snippet.md

# Rebuild the index
python3 build_freegame_index.py
```

### Helper Script

Use `./rebuild_indices.sh` to rebuild both indices at once:

```bash
./rebuild_indices.sh
```

## Utils Philosophy

Utils are single-file HTML applications inspired by [Simon Willison's tools](https://simonwillison.net/2025/Dec/10/html-tools/):

- **No build steps** - Pure HTML, CSS, and JavaScript
- **No frameworks** - No React, Vue, etc.
- **CDN dependencies** - Load libraries from CDNs, not npm
- **Client-side only** - Everything runs in the browser
- **localStorage for persistence** - API keys and data stay local
- **Copy-paste friendly** - Easy input and output

### Template

Use the template in `free-game/web/single-file-html-template.md` as a starting point for new tools.

## Free Game Philosophy

Free game snippets are:

- **Concise** - One topic per file
- **Self-contained** - Include all necessary context
- **LLM-friendly** - Optimized for copy-pasting into prompts
- **Organized by topic** - Easy to browse and find

## Deployment

This site is deployed to GitHub Pages automatically when you push to the `master` branch.

## License

Blog posts and snippets are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code (utils and examples) is MIT licensed.
