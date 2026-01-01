---
layout: post
title: "My Software Development Environment in 2025"
date: 2025-12-31 19:00:00 +0000
categories: development tools
---

After years of refining my workflow, I've settled on a development environment that prioritizes speed, keyboard-driven navigation, and deep integration between tools. Here's a comprehensive look at how I work.

## Terminal & Shell: Ghostty + zsh

### Ghostty Terminal

[Ghostty](https://ghostty.org) has become my terminal of choice. It's a native, GPU-accelerated terminal that's blazingly fast and deeply integrated with macOS. My configuration includes:

**Visual Customization:**
- **Font:** TX-02 at 19pt with font thickening enabled
- **Custom Shaders:** I use adaptive BetterCRT for that subtle retro aesthetic and a blaze cursor animation with a long trail
- **Icon:** Custom plastic-frame style with white ghost on black screen

**Key Features:**
- **Quick Terminal:** Global hotkey (Ctrl+`) for instant terminal dropdown
- **Vim-like Navigation:** Ctrl+hjkl for split navigation (matching my tmux/vim setup)
- **Shell Integration:** Prompt marking for intelligent command completion detection
- **100k Scrollback:** Never lose terminal output

```conf
# Ghostty config excerpt
font-family = TX-02
font-size = 19
keybind = global:ctrl+grave_accent=toggle_quick_terminal
custom-shader = ~/.config/ghostty/shaders/bettercrt-adaptive.glsl
custom-shader = ~/.config/ghostty/shaders/cursor_blaze.glsl
```

The quick terminal feature alone is worth the switch - instant access to a terminal from anywhere in macOS.

### Zsh with Oh My Zsh & Powerlevel10k

My shell setup is built on zsh with several layers of enhancement:

**Core Components:**
- **Oh My Zsh:** Framework for managing zsh configuration
- **Powerlevel10k:** Lightning-fast, highly customizable prompt
- **Shell Integration:** Ghostty-aware prompt handling with proper cursor management

**Productivity Tools:**
- **fzf:** Fuzzy finder for command history, file searching, and more
- **zoxide:** Smart directory jumping (smarter cd)
- **pyenv:** Python version management

**Key Plugins:**
```zsh
plugins=(git textmate macos ollama vercelgate)
```

The integration between Ghostty and zsh is seamless - shell integration features provide proper prompt detection, window title updates, and cursor management within tmux sessions.

## Tmux: Terminal Multiplexer

I live in tmux. My configuration is heavily customized for vim-like navigation and deep integration with both Ghostty and vim.

**Prefix Key:** `Ctrl+a` (easier to reach than the default Ctrl+b)

**Vim-like Navigation:**
```conf
# Pane splitting with context awareness
bind-key v split-window -h -c "#{pane_current_path}"
bind-key s split-window -v -c "#{pane_current_path}"

# Vim-style pane navigation
bind-key h select-pane -L
bind-key j select-pane -D
bind-key k select-pane -U
bind-key l select-pane -R
```

**Seamless Vim Integration:**

Using [vim-tmux-navigator](https://github.com/christoomey/vim-tmux-navigator), I can navigate between vim splits and tmux panes with the same Ctrl+hjkl keybindings. The multiplexer detects when vim is running and passes through the navigation commands appropriately.

**Ghostty Optimizations:**
```conf
# Terminal color support
set-option -g default-terminal "tmux-256color"
set-option -ga terminal-overrides ",ghostty:Tc"

# OSC sequence passthrough for Ghostty features
set -g allow-passthrough on
set -g set-titles on
set -g set-titles-string "#S / #W"
```

**Copy Mode:**
Vi-style copy mode with macOS clipboard integration:
```conf
setw -g mode-keys vi
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "pbcopy"
```

## Vim: The Editor

Despite the prevalence of modern IDEs, vim remains my primary editor. My configuration is optimized for productivity with VSCode-like conveniences.

**Plugin Manager:** vim-plug with automatic installation

**Essential Plugins:**
- **NERDTree:** File explorer (toggle with `,d`)
- **CtrlP:** Fuzzy file finder (Ctrl+P, just like VSCode)
- **vim-tmux-navigator:** Seamless navigation between vim/tmux
- **vim-fugitive:** Git integration directly in vim
- **vim-airline:** Beautiful status line with powerline fonts
- **vim-commentary:** Quick commenting with `gc`
- **vim-surround:** Easily change surrounding quotes/brackets
- **auto-pairs:** Auto-close brackets and quotes

**Keyboard-First Philosophy:**

My leader key is `,` (comma) for easy access:

```vim
" Quick access
nnoremap <leader>d :NERDTreeToggle<CR>
nnoremap <leader>p :CtrlP<CR>

" Save/quit shortcuts
nnoremap <leader>w :w<CR>
nnoremap <leader>q :q<CR>

" Git commands
nnoremap <leader>gs :Git<CR>
nnoremap <leader>gc :Git commit<CR>
nnoremap <leader>gd :Gdiffsplit<CR>
```

**VSCode-like Conveniences:**
```vim
" Save with Ctrl+S
nnoremap <C-s> :w<CR>
inoremap <C-s> <Esc>:w<CR>a

" Buffer navigation like tabs
nnoremap <leader>] :bnext<CR>
nnoremap <leader>[ :bprevious<CR>

" Quick exit from insert mode
inoremap jj <ESC>
```

**Automatic Whitespace Cleanup:**

I auto-strip trailing whitespace on save for Python, JavaScript, TypeScript, Ruby, Markdown, and YAML files.

## Development Tools & Utilities

### OrbStack: Container & VM Management

[OrbStack](https://orbstack.dev) has completely replaced Docker Desktop for me. It's:
- **Fast:** Near-native performance for containers and VMs
- **Lightweight:** Uses 50% less memory than Docker Desktop
- **Seamless:** Better file sharing, networking, and macOS integration
- **Developer-friendly:** Built-in domain names, port forwarding, and shell access

I use it for running databases, testing environments, and containerized development.

### Tailscale: Private Networking

[Tailscale](https://tailscale.com) provides a secure WireGuard-based mesh VPN across all my devices:
- Access my development servers from anywhere
- Secure SSH without exposed ports
- Share development previews with teammates
- Exit nodes for secure browsing on public WiFi

### Obsidian: Knowledge Management

[Obsidian](https://obsidian.md) is where I keep all my development notes, research, and documentation:

```zsh
# Vault location configured in .zshrc
export OBSIDIAN_VAULT_PATH="/Users/jbwashington/Library/Mobile Documents/iCloud~md~obsidian/Documents"
```

I use it for:
- **Code snippets** and quick references
- **Project planning** and architecture docs
- **Learning notes** from courses and documentation
- **Daily logs** of what I'm working on

The Markdown-based system syncs via iCloud and integrates with my workflow via the Obsidian API.

## Package Managers & Runtime Management

I manage multiple language runtimes and tools:

**JavaScript/TypeScript:**
- **bun:** Primary JS runtime and package manager
- **pnpm:** Alternative package manager for certain projects
- **deno:** For modern TypeScript projects

**Python:**
- **pyenv:** Python version management
- **uv:** Ultra-fast Python package installer

**System Packages:**
- **Homebrew:** macOS package manager

**Path Configuration:**
```zsh
export PATH="$HOME/.local/bin:$HOME/bin:/usr/local/bin:$PATH"
export PATH="$PNPM_HOME:$BUN_INSTALL/bin:$PATH"
export PATH="$PYENV_ROOT/bin:$PATH"
```

## Claude Code: AI-Powered Development

[Claude Code](https://claude.ai/claude-code) is deeply integrated into my workflow. It's not just an AI assistant - it's a development partner.

**Shell Integration:**

Claude Code hooks into my shell via custom integration scripts:
```zsh
source /Users/jbwashington/.claude/hooks/utils/shell-integration.sh
```

**Environment Variables:**
```zsh
export CLAUDE_CODE_ENTRYPOINT=cli
export CLAUDECODE=1
```

**How I Use It:**

1. **Code Generation:** Writing boilerplate, utilities, and entire features
2. **Debugging:** Analyzing error messages and suggesting fixes
3. **Documentation:** Generating and updating project documentation
4. **Refactoring:** Large-scale codebase improvements
5. **Learning:** Explaining complex codebases and architectural patterns

The integration with Ghostty means I can invoke Claude Code with a simple command and get AI assistance without leaving my terminal.

## API Keys & Services

My development workflow integrates with numerous AI and cloud services (managed via environment variables):

**AI/LLM Services:**
- OpenAI, Anthropic (Claude), OpenRouter
- Groq, DeepSeek, Mistral, Cerebras
- Gemini, Perplexity, Together AI

**Development APIs:**
- GitHub CLI, Notion, Obsidian
- Replicate, ElevenLabs, Deepgram
- Cloudflare, Tailscale, Vercel

**Media & Data:**
- Unsplash, Pexels, Pixabay
- Firecrawl (web scraping)
- Shodan (security research)

All API keys are stored in my `.zshrc` for easy access across terminal sessions.

## Workflow: Putting It All Together

Here's how these tools work together in a typical development session:

1. **Launch Ghostty** with quick terminal (Ctrl+`)
2. **Navigate** to project with zoxide: `z project-name`
3. **Start tmux session:** `tmux new -s project` or `tmux attach -t project`
4. **Split panes** for different tasks:
   - Pane 1: vim for editing
   - Pane 2: running development server
   - Pane 3: git commands and testing
5. **Edit code in vim** with NERDTree + CtrlP for navigation
6. **Seamless navigation** between vim splits and tmux panes with Ctrl+hjkl
7. **Use Claude Code** for AI assistance when needed
8. **Git workflow** via vim-fugitive or command line
9. **Container services** running via OrbStack
10. **Documentation** in Obsidian for reference

All accessible via keyboard, no mouse required.

## Why This Setup Works

**Speed:** Everything is optimized for minimal latency
- Ghostty's GPU acceleration
- Powerlevel10k's instant prompt
- Vim's lightweight footprint
- OrbStack's native performance

**Consistency:** Uniform keybindings across tools
- Vim navigation (hjkl) everywhere
- Leader key (comma) patterns
- Ctrl+hjkl for splits/panes

**Integration:** Tools work together seamlessly
- Ghostty ↔ tmux ↔ vim navigation
- Shell integration for smart features
- Clipboard sharing across everything
- Claude Code integrated at the shell level

**Flexibility:** Easy to customize and extend
- Dotfiles are simple text files
- Plugins are version-controlled
- Settings sync via git

## Getting Started

If you want to try a similar setup:

1. **Start with Ghostty** - It's free and the foundation of the experience
2. **Add zsh + Oh My Zsh** - Standard on macOS, easy to configure
3. **Learn tmux basics** - Just prefix + % (split) and prefix + " (split) to start
4. **Try vim** with a minimal config - You don't need all my plugins at once
5. **Add tools incrementally** - Don't try to adopt everything at once

My complete dotfiles are available on GitHub (zshrc, vimrc, tmux.conf, Ghostty config).

## Conclusion

This environment has evolved over years of daily use. It's not about using the newest tools - it's about finding what works and refining it. The result is a development environment that feels like an extension of my thoughts, where the tools disappear and I can focus on building.

**Key Takeaways:**
- **Terminal-first workflow** enables speed and consistency
- **Vim keybindings everywhere** create muscle memory
- **AI integration (Claude Code)** augments without replacing core skills
- **Modern tools (Ghostty, OrbStack)** can coexist with traditional Unix tools

Your environment should work for you. Take what makes sense, experiment, and build something that feels natural. The best development environment is the one you understand deeply and can bend to your will.

---

*Have questions about my setup? Want to share yours? Find me on GitHub [@jbwashington](https://github.com/jbwashington).*

*Last updated: December 31, 2025*
