---
name: item-7-before-remeasure
description: "Six-kits plan item 7 (defect IDs, PR #90) landed before the 2026-11-09 token re-measure, against the plan's order, and why the confound is small"
metadata:
  type: project
---

`kit/six-kits-plan.md` put item 7, defect recurrence, after the token re-measure (about
2026-11-09), so that nothing but the hooks of 2026-11-02 moves the per-reply numbers in that
window. It landed first: PR #90 merged on 2026-11-03, inside the window.

The confound is small. A reply's context starts with `CLAUDE.md`, the memory index and the agent
definitions, and PR #90 changed none of them. It touched `scripts/spec-drift.py`,
`scripts/relabel.py`, their tests, `scripts/demo-data.py`, the dashboard page, and a few lines of
`specs/README.md` and `specs/_template.md`, which a session reads only when a step opens them.
Its own replies count as one more merged PR in the window, like any other.

**Why:** the re-measure decides item 6 and whether the ladder stays; a reader of its numbers
should know what else moved in the window.
**How to apply:** when reading the re-measure, name PR #90 as inside the window and judge it as
above. Next time, keep the plan's order or say in the PR why it changes. Related:
[[token-remeasure]].
