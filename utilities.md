---
layout: page
title: Browser Utilities
permalink: /utilities/
---

A collection of standalone browser-based tools and utilities. All tools run entirely in your browser with no backend required - just open and use!

## 🔍 Contact Scraper
Extract contact information from any website. Scrape emails, phone numbers, addresses, and avatars with support for structured data parsing.

**Features:**
- Scrape by URL or paste HTML directly
- CORS proxy support for cross-origin requests
- Schema.org structured data extraction
- Export results as JSON or CSV
- No backend required - runs entirely in browser

[Open Contact Scraper](contact-scraper.html){: .btn}

---

## 📺 M3U Editor
Professional IPTV playlist manager with Xtream Codes API integration and cloud sync.

**Features:**
- Connect to Xtream Codes servers
- Load and edit M3U/M3U8 playlists
- Drag-and-drop channel reordering
- Search and filter by category
- S3-compatible cloud storage sync (AWS S3, Cloudflare R2, etc.)
- Local editing with localStorage persistence
- Export modified playlists

[Open M3U Editor](m3u-editor.html){: .btn}

---

## 🔐 Browser Fingerprint Analyzer
Comprehensive privacy and uniqueness analysis tool. See what the internet knows about you and how unique your browser fingerprint is.

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

[Open Fingerprint Analyzer](fingerprint-analyzer.html){: .btn}

---

## 📝 Markdown to PDF
Live markdown editor with instant preview and one-click PDF export. Perfect for writing documentation, blog posts, resumes, and more.

**Features:**
- Real-time markdown preview as you type
- Export to PDF with multiple page sizes (A4, Letter, Legal)
- Export to standalone HTML file
- Quick templates (README, Blog Post, Documentation, Resume)
- Auto-save with localStorage persistence
- Word count, character count, and line count
- Adjustable font sizes
- Keyboard shortcuts (Ctrl/Cmd+S for HTML, Ctrl/Cmd+P for PDF)
- Tab key support for indentation

[Open Markdown to PDF](markdown-to-pdf.html){: .btn}

---

## Technology Stack

All utilities are built with:
- Pure HTML/CSS/JavaScript (no build tools required)
- CDN-imported libraries (no npm/node_modules)
- Progressive enhancement for better compatibility
- Responsive design for mobile and desktop

### External APIs Used (Optional)
- **Contact Scraper**: AllOrigins/CORSProxy for cross-origin requests
- **M3U Editor**: Xtream Codes API, AWS SDK for S3 sync
- **Fingerprint Analyzer**: IPify (IP detection), ipapi.co (geolocation)
- **Markdown to PDF**: Marked.js (markdown parsing), jsPDF (PDF generation), html2canvas (HTML rendering)

---

## Privacy & Security

All tools run entirely in your browser. Your data never leaves your device unless you explicitly:
- Fetch data from external URLs
- Sync to your own S3 storage
- Export data as files

**No tracking, no analytics, no data collection.**
