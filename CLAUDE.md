# Claude Code Instructions for jbwashington.github.io

## Project Overview

This is a GitHub Pages site serving as a personal portfolio and collection of browser-based utilities. The site hosts standalone, self-contained tools that run entirely in the browser with no backend infrastructure required.

## Project Philosophy

**Key Principles:**
1. **No React** - All utilities use pure HTML/CSS/JavaScript
2. **No Build Tools** - No webpack, no npm build scripts, no compilation
3. **CDN-Only Dependencies** - All external libraries loaded via CDN
4. **Privacy-First** - No tracking, no analytics, no data collection
5. **Self-Contained** - Each tool is a single HTML file with inline CSS/JS
6. **Offline-Capable** - Tools work offline except when fetching external data
7. **Mobile-Responsive** - All tools work on mobile and desktop

## Current Browser Utilities

### 1. Contact Scraper (`contact-scraper.html`)
**Purpose:** Extract contact information from any website

**Features:**
- Scrape by URL or paste HTML directly
- Extract emails, phone numbers, addresses, avatars
- Schema.org structured data parsing
- CORS proxy support (AllOrigins, CORSProxy.io)
- Export results as JSON or CSV

**Technologies:**
- Vanilla JavaScript (ES6+)
- Fetch API
- DOMParser for HTML parsing
- Regex for contact pattern matching
- File API for downloads

**External APIs:**
- AllOrigins/CORSProxy (optional, for CORS bypass)

---

### 2. M3U Editor (`m3u-editor.html`)
**Purpose:** Professional IPTV playlist manager with cloud sync

**Features:**
- Connect to Xtream Codes API servers
- Load and edit M3U/M3U8 playlists
- Drag-and-drop channel reordering
- Search and filter by category
- S3-compatible cloud storage sync (AWS S3, Cloudflare R2, etc.)
- LocalStorage persistence

**Technologies:**
- Vanilla JavaScript (ES6+)
- AWS SDK (browser version) - loaded via CDN
- LocalStorage API
- Drag and Drop API
- File API for M3U parsing

**CDN Dependencies:**
```html
<script src="https://sdk.amazonaws.com/js/aws-sdk-2.1691.0.min.js"></script>
```

**External APIs:**
- Xtream Codes player_api.php (user-provided credentials)
- S3-compatible storage (user-provided keys)

---

### 3. Browser Fingerprint Analyzer (`fingerprint-analyzer.html`)
**Purpose:** Analyze browser uniqueness and privacy exposure

**Features:**
- Calculate uniqueness score (0-100%)
- Canvas fingerprinting detection
- WebGL fingerprinting analysis
- Audio context fingerprinting
- WebRTC leak detection
- IP geolocation
- System and hardware detection
- Privacy risk assessment
- Export complete fingerprint data

**Technologies:**
- Canvas API
- WebGL API
- Web Audio API
- WebRTC API
- Navigator API
- Screen API

**External APIs:**
- ipify.org (IP detection)
- ipapi.co (geolocation)

---

## Site Structure

```
jbwashington.github.io/
├── index.md              # Jekyll home page
├── about.md              # About page
├── utilities.md          # Jekyll utilities page (appears in nav)
├── tools.html            # Standalone tools landing page
├── contact-scraper.html  # Contact extraction utility
├── m3u-editor.html       # IPTV playlist manager
├── fingerprint-analyzer.html # Browser fingerprint analyzer
├── _config.yml           # Jekyll configuration
├── _includes/            # Jekyll includes
├── _posts/               # Blog posts
├── assets/               # Static assets
└── CLAUDE.md            # This file (AI development instructions)
```

## Development Guidelines

### Adding New Utilities

When adding a new browser-based utility, follow this template:

1. **File Structure:** Single HTML file with inline CSS and JavaScript
2. **Naming:** Use kebab-case (e.g., `new-tool.html`)
3. **No External Files:** All CSS and JS must be inline or CDN-loaded
4. **Styling Pattern (Minimal System Design):**
   ```css
   - Background: Light gray (#fdfdfd) - no gradients
   - Cards: White with 1px gray borders (#d4d4d4) - no rounded corners or shadows
   - System fonts: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI"...
   - Color palette (system colors only):
     * Primary: Blue (#1e69d8) for links only
     * Text: Gray (#5c5c5c) for body, dark (#111111) for headings
     * Borders: Gray (#d4d4d4)
     * Buttons: White background with gray borders (no colored buttons)
     * Code bg: Dark (#222222) or light (#f6f8fa)
   - Typography: Font weight 500 for headings (not 600-700)
   - Buttons: Neutral colors with subtle hover states (background: #f6f8fa)
   - NO EMOJIS: Use text labels only
   - NO COLORED BUTTONS: All buttons use system colors (white/gray)
   - Responsive grid layouts
   - Minimal animations: Only background-color transitions on hover
   ```

5. **JavaScript Pattern:**
   ```javascript
   - Use async/await for asynchronous operations
   - Error handling with try/catch
   - User feedback via toast notifications or alerts
   - LocalStorage for persistence when appropriate
   - Export functionality (JSON/CSV when applicable)
   ```

6. **Update Landing Pages:**
   - Add card to `tools.html`
   - Add section to `utilities.md`

### Code Style

**HTML:**
- Semantic HTML5 elements
- Accessibility attributes (ARIA when needed)
- Mobile-first viewport meta tag

**CSS:**
- Follow minimal system design language (clean, professional, no decorative elements)
- Use CSS Grid for layouts
- Flexbox for component alignment
- Simple 1px borders instead of box shadows
- No border-radius (keep rectangular for consistency)
- No colored buttons - all buttons use white/gray system colors
- Minimal transitions (background-color only on hover, no transforms)
- Mobile-responsive with media queries (@media max-width: 600px)
- Font weight 500 for headings, 400 for body text
- No emojis anywhere in the UI

**JavaScript:**
- ES6+ syntax (const/let, arrow functions, template literals)
- No jQuery or other heavy libraries
- Prefer native browser APIs
- Comment complex logic
- Use descriptive variable names

### CDN Libraries (When Needed)

Only use CDN libraries when absolutely necessary. Prefer native browser APIs.

**Approved CDN libraries:**
- AWS SDK (for S3 operations): `https://sdk.amazonaws.com/js/aws-sdk-2.1691.0.min.js`
- Any library that cannot be reasonably implemented from scratch

**Do NOT use:**
- React, Vue, Angular, or any framework
- jQuery
- Lodash/Underscore
- Moment.js (use native Date API)
- Axios (use native fetch)

### Privacy & Security

**Rules:**
1. Never send user data to external servers without explicit consent
2. Never use tracking scripts or analytics
3. Never store sensitive data (credentials, keys) in cookies or localStorage
4. Warn users before making external API calls
5. Use HTTPS for all external requests
6. Validate and sanitize all user input
7. Use Content Security Policy when possible

### External API Usage

**Guidelines:**
- Always optional (tool should work offline when possible)
- User-provided credentials only (no hardcoded API keys)
- Clear documentation of what data is sent where
- CORS proxy options when needed
- Rate limiting awareness
- Error handling for network failures

## Testing Checklist

Before committing new utilities:

- [ ] Works on Chrome, Firefox, Safari
- [ ] Mobile responsive (test at 375px, 768px, 1024px)
- [ ] All features functional without network (when applicable)
- [ ] Export/download features work
- [ ] LocalStorage persistence works
- [ ] Error messages are user-friendly
- [ ] No console errors
- [ ] Privacy-respecting (no tracking, no unnecessary requests)
- [ ] Accessible (keyboard navigation, screen reader friendly)
- [ ] Fast loading (< 2s on 3G)

## Git Workflow

**Commit Message Format:**
```
<action>: <brief description>

<detailed description of changes>
- Bullet points for specific changes
- What was added/modified/removed
- Why the change was made

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Examples:**
```
add: contact scraper utility

Added standalone contact extraction tool with:
- URL scraping with CORS proxy support
- HTML paste functionality
- Schema.org structured data parsing
- JSON/CSV export

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Future Utility Ideas

Based on existing GitHub projects:

### High Priority
1. **Markdown to PDF Converter** - Live editor with PDF export
2. **LLM Chat Playground** - Groq/OpenAI API playground with streaming
3. **Web Scraper Tool** - Generic HTML parser and data extractor
4. **Audio Visualizer** - Ambient sound mixer with visualizations
5. **Pomodoro Timer** - Productivity timer with audio notifications

### Medium Priority
6. **Vector Search Demo** - Show how embeddings work (requires API key)
7. **PDF Text Extractor** - Extract text from PDF files
8. **Digital Signature Pad** - Capture and download signatures
9. **HTML Screenshot Tool** - Convert HTML elements to images
10. **GitHub Stats Dashboard** - Personal GitHub metrics viewer

### Technical Exploration
11. **WASM Demos** - Showcase WebAssembly capabilities
12. **Transformers.js Demo** - In-browser ML models
13. **SQLite in Browser** - sql.js demonstrations
14. **WebGPU Experiments** - GPU-accelerated computations

## Technologies to Explore

**Browser APIs:**
- WebAssembly (WASM)
- WebGPU
- WebTransport
- File System Access API
- Web Bluetooth
- Web USB
- WebXR

**Libraries (CDN-only):**
- Transformers.js (in-browser ML)
- sql.js (SQLite in browser)
- PDF.js (PDF rendering)
- Three.js (3D graphics)
- Chart.js (data visualization)
- Marked.js (Markdown parsing)
- jsPDF (PDF generation)

## Deployment

**Deployment Method:** GitHub Actions (Jekyll 4.x)

This site uses GitHub Actions for deployment instead of the default GitHub Pages build process. This allows us to use ANY Jekyll plugin without whitelist restrictions, including `jekyll-ai-domain-data`.

**GitHub Actions Workflow:**
- Location: `.github/workflows/jekyll.yml`
- Trigger: Push to `master` branch or manual dispatch
- Ruby Version: 3.1
- Jekyll Version: 4.3.x
- Deployment: Automatic to GitHub Pages

**GitHub Pages Configuration:**
- Source: GitHub Actions (not branch-based)
- Custom domain: Not configured
- HTTPS: Enabled (enforced)

**Build Process:**
1. GitHub Actions checks out repository
2. Sets up Ruby 3.1 environment
3. Installs dependencies with bundle
4. Builds Jekyll site with production environment
5. Uploads artifact to GitHub Pages
6. Deploys to https://jbwashington.github.io/

**Deployment Time:** ~2-3 minutes

**URLs:**
- Base: `https://jbwashington.github.io/`
- Tools: `https://jbwashington.github.io/<tool-name>.html`
- Landing: `https://jbwashington.github.io/tools.html`
- AI Domain Data: `https://jbwashington.github.io/.well-known/domain-profile.json`

**First-Time Setup:**

After pushing the GitHub Actions workflow, you need to configure GitHub Pages to use Actions:

1. Go to repository Settings → Pages
2. Under "Build and deployment" → "Source"
3. Select "GitHub Actions" (not "Deploy from a branch")
4. Save changes

**Local Development:**

```bash
# Install dependencies (first time only)
bundle install

# Serve locally
bundle exec jekyll serve

# Build for production
JEKYLL_ENV=production bundle exec jekyll build
```

**AI Domain Data Plugin:**

The `jekyll-ai-domain-data` plugin is configured to generate `.well-known/domain-profile.json` following the AI Domain Data Standard v0.1.1. However, GitHub Pages has issues serving plugin-generated files in the `.well-known` directory.

**Workaround:** Static file approach (currently in use)
- File location: `.well-known/domain-profile.json` (committed to repository)
- Live URL: https://jbwashington.github.io/.well-known/domain-profile.json
- Must be updated manually when site information changes

**Current Profile Data:**
- Name: James Washington
- Description: Personal website and blog for James Washington.
- Contact: jbwashington@gmail.com
- Website: https://jbwashington.github.io
- Logo: https://github.com/jbwashington.png
- Entity Type: Person (capitalized - required by schema)
- Version: 0.1.1

**Updating the Domain Profile:**

When site information changes, manually edit `.well-known/domain-profile.json`:

```json
{
  "$schema": "https://aiddstandard.org/schema/v0.1.1/domain-profile.json",
  "version": "0.1.1",
  "name": "James Washington",
  "description": "Personal website and blog for James Washington.",
  "website": "https://jbwashington.github.io",
  "contact": "jbwashington@gmail.com",
  "entity_type": "Person",
  "logo": "https://github.com/jbwashington.png"
}
```

**Important Notes:**
- `entity_type` must be capitalized: Person, Organization, Blog, NGO, Community, Project, CreativeWork, SoftwareApplication, or Thing
- Keep plugin configuration in `_config.yml` for future compatibility
- The `.well-known` directory is included in Jekyll's `include` config to ensure deployment

## Performance Targets

**Goals:**
- First Contentful Paint: < 1s
- Time to Interactive: < 2s on 3G
- Total page size: < 500KB per utility
- No render-blocking resources
- Mobile Lighthouse score: > 90

**Optimization Strategies:**
- Inline critical CSS
- Defer non-critical JavaScript
- Lazy load images
- Use modern image formats (WebP)
- Minimize CDN dependencies
- Enable compression

## Maintenance

**Regular Tasks:**
- Update CDN library versions annually
- Test in latest browsers quarterly
- Review privacy practices
- Check external API availability
- Update documentation

**Breaking Changes:**
- Always maintain backward compatibility
- Never remove utilities without deprecation notice
- Version utilities if major changes needed

## Support & Documentation

**User Support:**
- Tools should be self-explanatory
- Include inline help text
- Provide usage examples
- Error messages should suggest solutions

**Developer Documentation:**
- This file (CLAUDE.md) for AI-assisted development
- README.md for general project info (if needed)
- Inline code comments for complex logic
- utilities.md for user-facing documentation

## License & Attribution

**License:** Not specified (add MIT or appropriate license)

**Attribution:**
- Credit external APIs used
- Link to CDN library documentation
- Acknowledge data sources

---

## Quick Reference

### Starting a New Utility

```bash
# 1. Create new HTML file
touch new-utility.html

# 2. Use this template structure:
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name - Description</title>
    <style>/* Inline CSS */</style>
</head>
<body>
    <div class="container">
        <!-- Tool UI -->
    </div>
    <script>/* Inline JavaScript */</script>
</body>
</html>

# 3. Test locally
# 4. Update tools.html and utilities.md
# 5. Commit and push
git add new-utility.html tools.html utilities.md
git commit -m "add: new utility tool"
git push origin master
```

### Testing Locally

```bash
# Option 1: Python HTTP server
python3 -m http.server 8000

# Option 2: Jekyll (for .md pages)
bundle exec jekyll serve

# Open browser to localhost:8000 or localhost:4000
```

---

**Last Updated:** 2025-12-31
**Project Lead:** James Washington (@jbwashington)
**AI Assistant:** Claude Code (Sonnet 4.5)
