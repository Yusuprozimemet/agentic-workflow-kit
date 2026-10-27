---
name: spec-auditor-eval
description: "2026-10-09 replay test of the spec-auditor on 4 pre-fix snapshots (Days 21, 24, 27, 28): ~75% recall, blind spot is cross-day ownership"
metadata:
  node_type: memory
  type: project
  originSessionId: 72d6d813-9fe5-4c81-9c90-cd0fda57f578
  modified: 2026-10-08T22:26:14.899Z
---

Replayed today's spec-auditor (Opus) on history-free snapshots taken before spec-change PRs #211, #250, #261, #319, scored against what those PRs fixed.

- Day 21: 2/2 (both missed by the original audit). Day 28: 1/5. Day 24: 8/10. Day 27: 8/10 + 2 partial. Total ≈ 20/27.
- Misses are almost all cross-day ownership / whole-plan items (Day 28 review-list gaps, unowned `matching` role and grants, phase-3 tag, DLQ retention), which the plan-auditor caught originally.
- No false alarms in the spot-checks; it also found real defects outside the key (two Day 28 ones were fixed later in the real history).
- Each run takes 11-21 min and 90-140k tokens. Snapshots need a short path (C:/ae) because of Windows MAX_PATH, and runs must be sequential because the `:harness` image tags are shared.

**Why:** the maintainer asked whether the auditors are good compared with proposed role-based "experiment auditors".
**How to apply:** don't expect the spec-auditor to find unowned hand-offs across days; that is the plan-auditor's job (see [[auditors-on-opus]]). The pasted experiment-level auditors were not tested.
