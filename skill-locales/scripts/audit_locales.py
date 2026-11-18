#!/usr/bin/env python3
"""audit_locales.py — compare each locale edition of a skill against the
canonical edition and report structural loss (headings, code blocks).
Usage: python3 audit_locales.py <collection_root> [out.json]
Expects <root>/skills/<name>/SKILL.md (canonical) and
<root>/docs/<locale>/skills/<name>/SKILL.md (locale editions), matched
by directory name. Also reports orphan editions (no canonical
counterpart) and, among flagged pairs, stub editions whose length is
under 5% of the canonical edition. Deterministic; stdlib only.
"""
import os, re, sys, json
from collections import defaultdict

def split(t):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    return (m.group(1), m.group(2)) if m else ("", t)

def load(p):
    return open(p, encoding="utf-8", errors="ignore").read()

def heads(b): return len(re.findall(r"^#{1,4}\s+", b, re.M))
def blocks(b): return len(re.findall(r"```", b)) // 2

def main():
    root = sys.argv[1]
    canon = {}
    sd = os.path.join(root, "skills")
    for d in sorted(os.listdir(sd)):
        p = os.path.join(sd, d, "SKILL.md")
        if os.path.isfile(p):
            canon[d] = split(load(p))[1]
    rows = []
    orphans = 0
    dd = os.path.join(root, "docs")
    for loc in sorted(os.listdir(dd)):
        ld = os.path.join(dd, loc, "skills")
        if not os.path.isdir(ld):
            continue
        for d in sorted(os.listdir(ld)):
            p = os.path.join(ld, d, "SKILL.md")
            if not os.path.isfile(p):
                continue
            if d not in canon:
                orphans += 1
                continue
            tb = split(load(p))[1]; cb = canon[d]
            dh = heads(tb) - heads(cb); db = blocks(tb) - blocks(cb)
            ratio = round(len(tb) / max(len(cb), 1), 3)
            rows.append({"skill": d, "locale": loc, "d_headings": dh,
                         "d_blocks": db, "loss": dh < 0 or db < 0,
                         "len_ratio": ratio})
    per_loc = defaultdict(lambda: [0, 0])
    for r in rows:
        per_loc[r["locale"]][0] += r["loss"]; per_loc[r["locale"]][1] += 1
    summary = {"pairs": len(rows), "orphan_editions": orphans,
               "any_structural_loss": sum(1 for r in rows if r["loss"]),
               "heading_loss": sum(1 for r in rows if r["d_headings"] < 0),
               "codeblock_loss": sum(1 for r in rows if r["d_blocks"] < 0),
               "stub_editions_among_flagged": sum(1 for r in rows if r["loss"] and r["len_ratio"] < 0.05),
               "per_locale_loss": {k: f"{a}/{b}" for k, (a, b) in sorted(per_loc.items())}}
    print(json.dumps(summary, indent=1))
    if len(sys.argv) > 2:
        json.dump({"summary": summary, "rows": rows}, open(sys.argv[2], "w"), indent=1)

if __name__ == "__main__":
    main()
