# Artifact — skill-locales

Verifiable skill artifact accompanying the submission on structural
loss in locale editions of public skills.

## Contents

- `skill-locales/SKILL.md` — the skill (installable as-is in any host
  that loads SKILL.md-based skills).
- `skill-locales/scripts/audit_locales.py` — the deterministic audit
  script the skill invokes.
- `reproduction.json` — the report produced by the run below.

## Environment requirements

- Python 3.10 or newer (standard library only; nothing to install).
- A checkout of the public collection studied in the paper
  (Everything Claude Code / ECC), or any collection with canonical
  skills under `skills/` and locale editions under
  `docs/<locale>/skills/`.

## Reproduction

```bash
python3 skill-locales/scripts/audit_locales.py <collection_root> report.json
```

Expected summary on the studied collection:

```json
{
  "pairs": 516,
  "orphan_editions": 2,
  "any_structural_loss": 177,
  "heading_loss": 171,
  "codeblock_loss": 109,
  "stub_editions_among_flagged": 34
}
```

The studied snapshot is pinned to ECC commit
`d2ef2680594f9a17526a6e1a2e18b3d242c5d17b` (v2.2.3);
`snapshot-manifest.txt` lists the SHA-256 of every studied file
(canonical skills and locale editions).

The full per-pair deltas are in `report.json` (`rows`).
