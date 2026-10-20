# /// script
# requires-python = ">=3.11"
# dependencies = ["fastembed>=0.4", "numpy", "scikit-learn", "pyyaml"]
# ///
"""
Build the /archive/ section from the private inventory.

Private inputs (gitignored, in .inventory/):
    *.jsonl          raw inventory records (see .inventory/SCHEMA.md)
    decisions.yml    per-id publish decisions + overrides (you edit this)
    themes.yml       named themes with seed ids (pinned; see embed_archive.py)
    denylist.txt     strings that must never appear in public output

Public outputs (committed):
    _data/archive.json        approved items, themes, related links
    archive/<id>/index.md     one page per item (body below front matter is
                              hand-written and preserved across rebuilds)

Commands:
    uv run build_archive.py decide   fill decisions.yml with defaults for new ids
    uv run build_archive.py review   write the review checklist (markdown)
    uv run build_archive.py apply F  read a ticked checklist back into decisions.yml
    uv run build_archive.py build    generate the public data + pages (default)

Every build refuses to write if a denylisted or secret-shaped string would
end up in public output.
"""

import datetime
import json
import os
import re
import sys

import numpy as np
import yaml

import embed_archive as emb

ROOT = emb.ROOT
INV = emb.INV
DECISIONS = os.path.join(INV, "decisions.yml")
THEMES = os.path.join(INV, "themes.yml")
DENYLIST = os.path.join(INV, "denylist.txt")
DATA_OUT = os.path.join(ROOT, "_data", "archive.json")
PAGES = os.path.join(ROOT, "archive")
GENERATED_MARK = "generated_by: build_archive.py"
REPO_TREE = "https://github.com/jbwashington/jbwashington.github.io/tree/master"

# Fields that may leave the machine. Everything else (source_path,
# sensitivity_notes, external_deps, ...) stays in the private inventory.
PUBLIC_FIELDS = ["title", "kind", "summary_plain", "how_it_works", "first_built",
                 "last_touched", "cool_factor", "self_contained", "tags"]

# Built-in secret / private-infra shapes, on top of denylist.txt.
SECRET_PATTERNS = [
    r"\b100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d{1,3}\.\d{1,3}\b",  # tailnet CGNAT IPs
    r"\b192\.168\.\d{1,3}\.\d{1,3}\b",
    r"\.ts\.net\b",
    r"\b(sk|pk|rk)-[A-Za-z0-9_-]{16,}",
    r"\bgh[pousr]_[A-Za-z0-9]{20,}",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bxox[abpr]-[A-Za-z0-9-]{10,}",
    r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b",  # telegram bot token
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}",  # any email address
]

# Inventory bookkeeping tags that mean nothing to a reader.
TAG_DROP = {"already-on-site", "overlaps-local-project", "remote-only", "pre-llm", "site",
            "james-built", "third-party", "sanitize"}

# Plain-English names for each kind, for readers who don't live in a terminal.
KINDS = {
    "skill": ("AI skill", "Instructions an AI agent loads when a task calls for them, like a recipe card."),
    "hook": ("Agent hook", "A script that runs automatically at a moment in an AI session (before a command, when it stops) to steer or guard it."),
    "slash-command": ("Slash command", "A shortcut typed into the AI chat, like /afk, that kicks off a saved routine."),
    "subagent": ("Sub-agent", "A specialist AI persona the main agent can hand a job to."),
    "mcp-server": ("MCP server", "A plug that gives AI agents a new ability, such as reading a task board or placing a call, through a standard protocol."),
    "cli": ("Command-line tool", "A small program run from the terminal."),
    "api": ("API", "A service other programs can call."),
    "model": ("Model", "A trained AI model or a configuration of one."),
    "prompt": ("Prompt", "Wording that reliably gets an AI to behave a certain way."),
    "technique": ("Technique", "A pattern or hard-won lesson, written down so it isn't learned twice."),
    "util": ("Browser tool", "A single web page you can use right now, no install."),
    "artifact": ("Living document", "A self-contained HTML document that carries its own editing instructions."),
    "app": ("App", "A complete application."),
    "library": ("Library", "Reusable code other projects build on."),
    "plugin": ("Plugin", "An add-on that extends another tool."),
    "automation": ("Automation", "Something that runs on a schedule by itself."),
    "doc": ("Document", "A reference or runbook."),
    "note": ("Note", "A page from the personal wiki."),
    "asset": ("Asset", "Images, audio, or other media."),
    "blog-candidate": ("Story", "A build log or write-up."),
    "other": ("Thing", "Hard to categorize, still worth keeping."),
}

CODE_PATHS = {"link", "vendor", "make-public", "writeup"}
VENDORABLE = {"skill", "slash-command", "hook", "prompt", "cli", "plugin", "util",
              "automation", "subagent"}


def load_yaml(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return yaml.safe_load(f) or default


def dump_yaml(path, data):
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=True, allow_unicode=True, width=100)


def default_decision(r):
    """Starting point for review, from the inventory agent's recommendation."""
    rec = r.get("publish_recommendation")
    sens = r.get("sensitivity")
    repo = r.get("repo") or {}
    on_site = "already-on-site" in (r.get("tags") or [])
    publish = rec in ("publish", "publish-sanitized") or (
        rec == "writeup-only" and sens in ("public", "personal-private"))
    if sens in ("client", "work", "family", "nsfw", "secrets-risk", "security-research"):
        publish = publish and rec != "writeup-only" and sens not in ("family", "nsfw", "secrets-risk")
    if on_site or repo.get("public"):
        path = "link"
    elif (r.get("self_contained") == "yes" and r.get("kind") in VENDORABLE
          and rec == "publish"):
        path = "vendor"
    elif repo.get("url") and (r.get("cool_factor") or 0) >= 4 and r.get("self_contained") != "no":
        path = "make-public"
    else:
        path = "writeup"
    return {"publish": bool(publish), "path": path}


def records():
    return {r["id"]: r for r in emb.load_records()}


def cmd_decide():
    decisions = load_yaml(DECISIONS, {})
    added = 0
    for rid, r in records().items():
        if rid not in decisions:
            decisions[rid] = default_decision(r)
            added += 1
    dump_yaml(DECISIONS, decisions)
    print(f"{added} new ids added to {DECISIONS} ({len(decisions)} total)")


def merged(recs, decisions):
    """Apply decisions: overrides, merges (merge_into), publish filter.
    Items are keyed by public slug (decision `slug`, else the inventory id),
    since inventory ids can carry private names."""
    out, slug = {}, {}
    for rid, r in recs.items():
        d = decisions.get(rid) or default_decision(r)
        if d.get("merge_into"):
            continue
        item = {k: r.get(k) for k in PUBLIC_FIELDS}
        item.update({k: v for k, v in d.items() if k in PUBLIC_FIELDS})
        item["tags"] = sorted(set(item["tags"] or []) - TAG_DROP)
        slug[rid] = item["id"] = d.get("slug", rid)
        item["inventory_id"] = rid
        item["publish"] = d.get("publish", False)
        item["path"] = d.get("path", "writeup")
        item["theme"] = d.get("theme")
        item["llm_era"] = r.get("llm_era", True)
        item["links"] = public_links(r, d)
        item["site_path"] = site_path(r)
        out[item["id"]] = item
    for rid, d in decisions.items():
        target = slug.get((d or {}).get("merge_into"))
        if target and rid in recs:
            t, r = out[target], recs[rid]
            t["tags"] = sorted((set(t["tags"] or []) | set(r.get("tags") or [])) - TAG_DROP)
            dates = [x for x in (t["first_built"], r.get("first_built")) if x]
            t["first_built"] = min(dates) if dates else None
            dates = [x for x in (t["last_touched"], r.get("last_touched")) if x]
            t["last_touched"] = max(dates) if dates else None
            for k, v in public_links(r, d).items():
                t["links"].setdefault(k, v)
    return {k: v for k, v in out.items() if v["publish"]}


def public_links(r, d):
    links = dict(d.get("links") or {})
    repo = r.get("repo") or {}
    if repo.get("public") and repo.get("url") and not repo["url"].endswith("jbwashington.github.io"):
        links.setdefault("repo", repo["url"])
    src = r.get("source_path") or ""
    m = re.search(r"/Developer/personal/artifacts/(.+)$", src) or \
        re.search(r"/Documents/artifacts/personal/(.+)$", src)
    if m and os.path.exists(os.path.expanduser(f"~/Developer/personal/artifacts/{m.group(1)}")):
        links.setdefault("live", f"https://jbwashington.github.io/artifacts/{m.group(1)}")
    return links


def site_path(r):
    """Repo-relative path for items already published on this site."""
    src = r.get("source_path") or ""
    if not src.startswith(ROOT + "/"):
        return None
    rel = src[len(ROOT) + 1:]
    if rel.startswith(("_drafts/", "scripts/", "replays/2")) or rel.endswith(".py"):
        return None
    return rel


def site_url(rel):
    """URL for a non-post site path. Posts are resolved by Liquid (their URLs
    include categories)."""
    if rel is None or rel.startswith("_posts/"):
        return None
    if rel.startswith("_ideas/"):
        return "/ideas/" + os.path.splitext(os.path.basename(rel))[0] + "/"
    if rel.startswith("free-game/"):
        return "/free-game/"
    if rel.endswith("index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def assign_themes(items, themes):
    ids = list(items)
    vecs = emb.embed([emb.text_for(items[i]) for i in ids])
    index = {items[i]["inventory_id"]: n for n, i in enumerate(ids)}  # seeds are inventory ids
    llm_themes = [t for t in themes if t.get("era") != "pre-llm"]
    before = next((t for t in themes if t.get("era") == "pre-llm"), None)
    centroids = []
    for t in llm_themes:
        seeds = [index[s] for s in t["seeds"] if s in index]
        centroids.append(vecs[seeds].mean(axis=0) if seeds else np.zeros(vecs.shape[1]))
    centroids = np.stack(centroids)
    for n, item in enumerate(items[i] for i in ids):
        if item["theme"]:
            continue
        if not item["llm_era"] and before:
            item["theme"] = before["slug"]
        else:
            item["theme"] = llm_themes[int(np.argmax(centroids @ vecs[n]))]["slug"]
    return emb.related(vecs, ids)


def scan(text):
    patterns = list(SECRET_PATTERNS)
    if os.path.exists(DENYLIST):
        with open(DENYLIST) as f:
            patterns += [re.escape(l.strip()) for l in f if l.strip() and not l.startswith("#")]
    return sorted({m.group(0) for p in patterns for m in re.finditer(p, text, re.I)})


def page_text(item):
    desc = (item["summary_plain"] or "").replace('"', "'")
    return (f"---\nlayout: archive-item\ntitle: {json.dumps(item['title'])}\n"
            f"item_id: {item['id']}\npermalink: /archive/{item['id']}/\n"
            f"description: \"{desc}\"\n{GENERATED_MARK}\n---\n")


def cmd_build():
    recs = records()
    decisions = load_yaml(DECISIONS, {})
    themes = load_yaml(THEMES, [])
    items = merged(recs, decisions)
    rel = assign_themes(items, themes)

    for slug, item in items.items():
        src = recs[item.pop("inventory_id")].get("source_path") or ""
        item["related"] = [x for x in rel[slug] if x in items]
        item["url"] = site_url(item.pop("site_path"))
        item.pop("publish")
        if item["url"] is None and src.startswith(ROOT + "/_posts/"):
            item["post_path"] = src[len(ROOT) + 1:]
        if os.path.isdir(os.path.join(PAGES, slug, "src")):
            item["links"]["source"] = f"{REPO_TREE}/archive/{slug}/src"
    order = sorted(items, key=lambda i: (items[i]["last_touched"] or "", items[i]["cool_factor"] or 0),
                   reverse=True)
    theme_out = []
    for t in themes:
        # Strongest first within a theme; "before" reads as a timeline instead.
        members = sorted((i for i in order if items[i]["theme"] == t["slug"]),
                         key=lambda i: (items[i]["first_built"] or "") if t.get("era") == "pre-llm"
                         else (items[i]["cool_factor"] or 0, items[i]["last_touched"] or ""),
                         reverse=True)
        if members:
            theme_out.append({"slug": t["slug"], "name": t["name"], "blurb": t["blurb"],
                              "count": len(members), "ids": members})
    data = {
        "generated": datetime.date.today().isoformat(),
        "count": len(items),
        "since": min((i["first_built"] for i in items.values() if i["llm_era"] and i["first_built"]),
                     default=None),
        "themes": theme_out,
        "kinds": {k: {"label": v[0], "explain": v[1]} for k, v in KINDS.items()},
        "order": order,
        "items": items,
    }
    blob = json.dumps(data, indent=1, ensure_ascii=False)
    hits = scan(blob)
    if hits:
        sys.exit(f"REFUSING TO BUILD: {len(hits)} private/secret-shaped strings in public output:\n  "
                 + "\n  ".join(hits))

    os.makedirs(os.path.dirname(DATA_OUT), exist_ok=True)
    with open(DATA_OUT, "w") as f:
        f.write(blob + "\n")

    os.makedirs(PAGES, exist_ok=True)
    for rid, item in items.items():
        path = os.path.join(PAGES, rid, "index.md")
        body = ""
        if os.path.exists(path):
            with open(path) as f:
                parts = f.read().split("---\n", 2)
            body = parts[2] if len(parts) == 3 else ""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(page_text(item) + body)
    removed = 0
    for name in os.listdir(PAGES):
        path = os.path.join(PAGES, name, "index.md")
        if name in items or not os.path.exists(path):
            continue
        with open(path) as f:
            generated = GENERATED_MARK in f.read()
        # Only remove pages this script made, and only if nothing was added beside them.
        if generated and os.listdir(os.path.join(PAGES, name)) == ["index.md"]:
            os.remove(path)
            os.rmdir(os.path.join(PAGES, name))
            removed += 1
    print(f"built {len(items)} items in {len(theme_out)} themes; removed {removed} stale pages")


def cmd_review(out=None):
    """Checklist grouped by theme: [x] = publish. Untick to keep private."""
    recs = records()
    decisions = load_yaml(DECISIONS, {})
    themes = load_yaml(THEMES, [])
    listed = {k: v for k, v in recs.items() if v.get("publish_recommendation") != "exclude"}
    all_items = merged(listed, {k: {**v, "publish": True} for k, v in decisions.items()})
    assign_themes(all_items, themes)
    lines = ["# Archive review", "",
             "Ticked = publish. Untick anything that should stay private. Path is how the code",
             "reaches the site: link (already public), vendor (copy a sanitized copy into the",
             "site), make-public (flip the repo public after a history audit), writeup (no code).",
             "Change a path by editing the word after the id. Excluded items are not listed.", ""]
    for t in themes:
        ids = sorted((i for i, it in all_items.items() if it["theme"] == t["slug"]),
                     key=lambda i: -(all_items[i]["cool_factor"] or 0))
        if not ids:
            continue
        lines += [f"## {t['name']}", ""]
        for i in ids:
            rid = all_items[i]["inventory_id"]
            it, d, r = all_items[i], decisions.get(rid, {}), recs[rid]
            box = "x" if d.get("publish") else " "
            flag = " ⚠️" + r.get("sensitivity") if r.get("sensitivity") not in ("public",) else ""
            lines.append(f"- [{box}] **{it['title']}** — {it['summary_plain']} "
                         f"`{rid}` {d.get('path', 'writeup')} · {'★' * (it['cool_factor'] or 0)}{flag}")
        lines.append("")
    text = "\n".join(lines)
    if out:
        with open(out, "w") as f:
            f.write(text)
        print(f"wrote {out}")
    else:
        print(text)


def cmd_apply(path):
    decisions = load_yaml(DECISIONS, {})
    n = 0
    with open(path) as f:
        for line in f:
            m = re.match(r"- \[([ xX])\] .*`([a-z0-9-]+)` ([a-z-]+)", line)
            if not m or m.group(2) not in decisions:
                continue
            d = decisions[m.group(2)]
            d["publish"] = m.group(1) != " "
            if m.group(3) in CODE_PATHS:
                d["path"] = m.group(3)
            n += 1
    dump_yaml(DECISIONS, decisions)
    print(f"applied {n} lines from {path}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "decide":
        cmd_decide()
    elif cmd == "review":
        cmd_review(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "apply":
        cmd_apply(sys.argv[2])
    elif cmd == "build":
        cmd_build()
    else:
        sys.exit(__doc__)
