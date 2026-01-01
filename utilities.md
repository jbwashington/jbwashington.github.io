---
layout: page
title: Browser Utilities
permalink: /utilities/
---

A collection of standalone browser-based tools and utilities. All tools run entirely in your browser with no backend required - just open and use!

## Favicon Generator
Generate all favicon and app icon formats from a single SVG or PNG. Perfect for web projects, PWAs, and app development.

**Features:**
- SVG and PNG input with drag-and-drop support
- Generate favicon.ico with multiple sizes (16/32/48)
- Apple touch icons (180x180, 152x152, 120x120)
- Android/PWA icons (192x192, 512x512, maskable variants)
- Microsoft tiles (70x70, 150x150, 310x150, 310x310)
- Safari pinned tab SVG
- Auto-generated HTML snippet for head tag
- Auto-generated site.webmanifest
- Auto-generated browserconfig.xml
- Download all icons as ZIP

[Open Favicon Generator](favicon-generator.html){: .btn}

---

## AI Workbench
Local-first LLM interface with tiered provider support. Chat with AI models running entirely in your browser, connect to local Ollama instances, or use cloud APIs - all with a unified interface.

**Features:**
- Chrome Built-in AI (Gemini Nano) - zero config, runs locally in Chrome
- Ollama integration for local LLM servers
- BYOK (Bring Your Own Key) support for OpenAI, Groq, OpenRouter
- Transformers.js fallback for any browser (Phi-3, Qwen2, TinyLlama)
- Document context for RAG-lite conversations
- Writing assistant with improve, simplify, expand, summarize tools
- Streaming responses with real-time output
- Settings persistence with localStorage
- Export/import conversations and documents

**Provider Priority:**
1. Chrome AI (Gemini Nano) - Best: fast, private, zero config
2. Ollama (localhost) - Power users with local models
3. API Keys - Cloud power when needed
4. Transformers.js - Works anywhere, offline capable

[Open AI Workbench](ai-workbench.html){: .btn}

---

## Contact Scraper
Extract contact information from any website. Scrape emails, phone numbers, addresses, and avatars with support for structured data parsing.

**Features:**
- Scrape by URL or paste HTML directly
- CORS proxy support for cross-origin requests
- Schema.org structured data extraction
- Export results as JSON or CSV
- No backend required - runs entirely in browser

[Open Contact Scraper](contact-scraper.html){: .btn}

---

## M3U Editor
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

## Browser Fingerprint Analyzer
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

## Markdown to PDF
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

## YouTube Video Transcriber
Offline AI-powered video transcription using OpenAI's Whisper model running entirely in your browser. Upload audio or video files and get accurate transcripts with timestamps.

**Features:**
- Whisper AI model (tiny, base, or small) runs in browser via Transformers.js
- Support for 99+ languages with auto-detection
- Upload audio/video files (MP3, MP4, WAV, M4A, WEBM, OGG)
- Export transcripts as TXT, SRT (subtitles), or VTT (captions)
- Timestamp support for video editing
- Copy to clipboard functionality
- 100% privacy-focused - all processing in browser
- Model cached locally after first download (~74MB for base model)
- Works offline after initial setup

**Note:** YouTube URL support requires downloading videos manually first (use yt-dlp or similar), then upload via the file input. This ensures your privacy - no data sent to external servers.

[Open YouTube Transcriber](youtube-transcriber.html){: .btn}

---

## OpenGraph Inspector
Preview how your links appear across social media platforms, messaging apps, and SMS. Validate OpenGraph metadata and optimize how your content is shared.

**Features:**
- Platform-specific previews (Facebook, Twitter, LinkedIn, WhatsApp, Slack, iMessage)
- Parse OpenGraph, Twitter Card, and general meta tags
- Validate metadata against best practices
- Image dimension recommendations per platform
- Export metadata as JSON
- Copy meta tags to clipboard for easy implementation
- CORS proxy support for fetching external URLs
- Visual validation feedback (pass/warn/fail indicators)

**Supported Platforms:**
- **Facebook**: 1200 × 630 pixels
- **Twitter**: 800 × 418 pixels (summary_large_image)
- **LinkedIn**: 1200 × 627 pixels
- **WhatsApp**: 300 × 157 pixels
- **Slack**: 800 × 418 pixels
- **iMessage**: 300 × 157 pixels

[Open OpenGraph Inspector](opengraph-inspector.html){: .btn}

---

## Technology Stack

All utilities are built with:
- Pure HTML/CSS/JavaScript (no build tools required)
- CDN-imported libraries (no npm/node_modules)
- Progressive enhancement for better compatibility
- Responsive design for mobile and desktop

### External APIs Used (Optional)
- **Favicon Generator**: JSZip (CDN) for ZIP downloads - no external APIs, all local processing
- **AI Workbench**: Chrome Built-in AI APIs, Ollama API, OpenAI/Groq/OpenRouter APIs, Transformers.js (CDN)
- **Contact Scraper**: AllOrigins/CORSProxy for cross-origin requests
- **M3U Editor**: Xtream Codes API, AWS SDK for S3 sync
- **Fingerprint Analyzer**: IPify (IP detection), ipapi.co (geolocation)
- **Markdown to PDF**: Marked.js (markdown parsing), jsPDF (PDF generation), html2canvas (HTML rendering)
- **YouTube Transcriber**: Transformers.js (Whisper model via CDN) - 100% offline after model download
- **OpenGraph Inspector**: AllOrigins/CORSProxy for cross-origin requests - all parsing done locally

---

## Privacy & Security

All tools run entirely in your browser. Your data never leaves your device unless you explicitly:
- Fetch data from external URLs
- Sync to your own S3 storage
- Export data as files

**No tracking, no analytics, no data collection.**
