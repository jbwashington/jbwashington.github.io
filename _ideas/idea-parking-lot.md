---
layout: idea
title: "This idea parking lot"
status: built
date: 2026-07-08
built: 2026-07-08
one_liner: "A place to park app ideas I don't have time for, that grows into a build log when I finally get to one."
tags: [jekyll, meta, writing]
link: /ideas/
---

## The pitch

I have more app ideas than time. Most of them evaporate — scribbled in a note,
never revisited. I wanted a spot on the site where I can drop an idea in thirty
seconds while it's hot, and then, whenever I actually get around to building it,
turn that same page into a build log: what I shipped, how the goal drifted from
the original pitch, and what I learned.

The rule: parking an idea should be cheap (one file, a title, a sentence), and
coming back to it should feel rewarding rather than like homework.

## Build log

### 2026-07-08

Built as a Jekyll collection (`_ideas/`) rather than another Python-generated
index like `utils/` and `free-game/`. Each idea is one markdown file. Frontmatter
carries a `status` that walks `idea → building → built` (or `shelved`), plus the
capture date and an optional ship date. The `/ideas/` page groups entries by
status; a single `idea` layout renders the badge, dates, tags, and body.

The body is deliberately open-ended: it starts as just **The pitch** and gains
**Build log**, **What changed**, and **Learnings** sections only when there's
something to say.

## What changed

The first sketch had a separate "retrospective" concept bolted on. Collapsed it:
the retrospective *is* just more sections appended to the same file over time, so
the page and its history live in one place. Also considered fabricating a few
placeholder ideas to fill the index — decided against it. An honest empty parking
lot is better than a fake-busy one; this meta-entry is the only seed.

## Learnings

- A Jekyll collection was the right call over the Python-index pattern: idea pages
  want real permalinks and evolving bodies, which Liquid handles natively.
- Making the *first action* trivial (copy `_TEMPLATE.md`, fill three fields) is the
  whole point. If parking an idea takes more than a minute, the backlog stays empty.
