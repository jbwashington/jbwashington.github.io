# /// script
# requires-python = ">=3.11"
# dependencies = ["fastembed>=0.4", "numpy", "scikit-learn"]
# ///
"""
Embeddings for the archive: propose themes and find related items.

Embeds only public-safe text fields (title, kind, summary_plain, how_it_works,
tags) with a local model (bge-small via ONNX; no API key, nothing leaves the
machine). Vectors are cached by text hash in .inventory/embeddings.npz, so
reruns only embed new or changed records.

Run directly to PROPOSE themes for review (writes .inventory/groups.json):

    uv run embed_archive.py [--groups 24]

Themes are proposed once, then named and pinned in _data/archive_themes.yml.
After that, build_archive.py assigns each new item to the nearest pinned theme,
so adding one item never reshuffles the whole site.
"""

import argparse
import collections
import glob
import hashlib
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
INV = os.path.join(ROOT, ".inventory")
CACHE = os.path.join(INV, "embeddings.npz")
MODEL = "BAAI/bge-small-en-v1.5"


def load_records():
    recs = []
    for path in sorted(glob.glob(os.path.join(INV, "*.jsonl"))):
        with open(path) as f:
            recs.extend(json.loads(line) for line in f if line.strip())
    return recs


def text_for(r):
    return " | ".join([
        r.get("title", ""),
        r.get("kind", ""),
        r.get("summary_plain", ""),
        r.get("how_it_works", ""),
        " ".join(r.get("tags") or []),
    ])


def embed(texts):
    """Return L2-normalized vectors for texts, embedding only cache misses."""
    cache = {}
    if os.path.exists(CACHE):
        z = np.load(CACHE)
        cache = dict(zip(z["keys"].tolist(), z["vecs"]))
    keys = [hashlib.sha1(t.encode()).hexdigest() for t in texts]
    missing = {k: t for k, t in zip(keys, texts) if k not in cache}
    if missing:
        from fastembed import TextEmbedding
        model = TextEmbedding(MODEL)
        for k, v in zip(missing, model.embed(list(missing.values()))):
            cache[k] = np.asarray(v, dtype=np.float32)
        np.savez(CACHE, keys=np.array(list(cache)), vecs=np.stack(list(cache.values())))
    vecs = np.stack([cache[k] for k in keys])
    return vecs / np.linalg.norm(vecs, axis=1, keepdims=True)


def related(vecs, ids, k=5, min_sim=0.66):
    """Top-k nearest neighbors per item above min_sim (bge-small sims run high:
    median pair ~0.58, median nearest neighbor ~0.75)."""
    sims = vecs @ vecs.T
    np.fill_diagonal(sims, -1)
    out = {}
    for i, rid in enumerate(ids):
        nn = np.argsort(-sims[i])[:k]
        out[rid] = [ids[j] for j in nn if sims[i, j] >= min_sim]
    return out


def main():
    from sklearn.cluster import AgglomerativeClustering

    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=int, default=0,
                    help="number of themes to propose (default: about one per 10 items)")
    args = ap.parse_args()

    recs = [r for r in load_records() if r.get("publish_recommendation") != "exclude"]
    vecs = embed([text_for(r) for r in recs])
    n = args.groups or max(2, round(len(recs) / 10))
    # Ward on unit vectors gives balanced groups; average-linkage cosine
    # collapses into one giant blob because bge-small similarities are compressed.
    labels = AgglomerativeClustering(n_clusters=n, linkage="ward").fit_predict(vecs)

    by_group = collections.defaultdict(list)
    for r, g in zip(recs, labels):
        by_group[int(g)].append(r)
    groups = []
    for members in sorted(by_group.values(), key=len, reverse=True):
        tags = collections.Counter(t for r in members for t in set(r.get("tags") or []))
        groups.append({
            "top_tags": [t for t, _ in tags.most_common(5)],
            "ids": [m["id"] for m in members],
            "titles": [m["title"] for m in members],
        })
    with open(os.path.join(INV, "groups.json"), "w") as f:
        json.dump({"model": MODEL, "groups": groups}, f, indent=1)
    print(f"{len(recs)} records -> {n} proposed themes; sizes {[len(g['ids']) for g in groups]}")


if __name__ == "__main__":
    main()
