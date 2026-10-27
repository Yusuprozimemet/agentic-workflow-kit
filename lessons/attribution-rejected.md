---
name: attribution-rejected
description: Per-name attribution of spec-drift gap moves was tested offline 2026-10-08 and dropped; do not propose it again
metadata:
  node_type: memory
  type: project
  originSessionId: f3162914-310e-4e12-84d3-244b5fd01cf8
  modified: 2026-10-08T20:14:51.105Z
---

Per-name attribution of gap moves in `scripts/spec-drift.py` (each name's share of the masked log1p spec and code vectors, compared merge to merge) was tested offline on 2026-10-08 and dropped by the maintainer.

The top known names on code PRs (#1, #80, #52) were mostly names entering the code for the first time, which name coverage and Jaccard already count. On spec PRs the output was renormalization noise. log1p was needed: with raw counts, postingId and userId led the lists. Every gap move above 0.85° came in Days 1–14. The largest after merge 120 was 0.72° (#183), and the gap has stayed below the chance band since #80.

**Why:** Attribution only renamed what the set view already shows. Building it would add a dashboard panel with nothing new in it.

**How to apply:** Don't propose attribution again. The one new finding was a split of each Δgap into drift on known names and entry of new vocabulary, computed by re-angling merge i under merge i−1's `known` mask. It is parked: optional, low priority, in its own small PR outside the days, after the criterion-ID fix ([[day32-c2b-handoff]]). The lab-notebook paragraph was written in Day 33's closing PR (#363), under "What is being measured" ([[spec-first-workflow]]).
