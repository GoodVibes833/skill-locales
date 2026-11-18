---
name: skill-locales
description: Audit locale editions of skills against their canonical edition for structural loss. Compares heading counts and code-block counts between the canonical SKILL.md and each translated edition, and reports editions that are structurally incomplete. Use when maintaining or reading a skill collection that ships translated editions under docs/<locale>/skills/.
---

# skill-locales

Skill collections ship translated (locale) editions of their skills,
typically under `docs/<locale>/skills/`. Nothing in the ecosystem shows
whether a locale edition still carries the full content of the canonical
edition. This skill measures that gap with language-independent
structural metrics only.

## What it does

1. Loads the canonical edition of each skill from `<root>/skills/`.
2. For every locale edition under `<root>/docs/<locale>/skills/` with a
   canonical counterpart, computes:
   - heading-count delta (locale minus canonical);
   - code-block-count delta (locale minus canonical).
3. Flags a pair as structural loss when either delta is negative.
4. Prints a summary (pairs, pairs with any structural loss, heading
   loss, code-block loss, per-locale loss counts) and optionally writes
   the full per-pair report as JSON.

## Invocation

```bash
python3 scripts/audit_locales.py <collection_root> [report.json]
```

## Requirements

- Python 3.10+ standard library only. No network, no model calls.
- Deterministic: the same collection always produces the same report.

## Output

Summary JSON on stdout; with the optional second argument, a full
report (`summary` + per-pair `rows`) written to that path.

## Scope note

Structural loss means the locale edition has fewer sections or code
examples than the canonical edition. It does not judge translation
quality, and an intentionally abridged edition will also be flagged —
the point is that the incompleteness becomes visible.
