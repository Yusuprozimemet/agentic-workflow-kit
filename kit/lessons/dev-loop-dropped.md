---
name: dev-loop-dropped
description: "The headless dev loop (#265 agent guard, #266 driver) was dropped on 2026-10-02 and reverted; work stays attended"
metadata:
  node_type: memory
  type: project
  originSessionId: 5d169970-d514-4408-84f1-61d9d2111859
  modified: 2026-10-02T17:49:38.755Z
---

On 2026-10-02 the maintainer dropped the headless dev loop (`scripts/dev-loop.py`, `docs/agentic-loop.md`, the Agent guard workflow) before its first run and had it reverted: #267 reverts #266, then a second PR reverts #265, then "Agent guard" comes off `main`'s required checks.

**Why:** the pre-run setup (bot account + token, review ruleset, sandbox container, second checkout) was more work than the migration needs. It may become a separate project later.

**How to apply:** run every day/track attended, as in [[spec-first-workflow]]. Don't propose reviving the loop or its setup steps in this repository unless the maintainer brings it up.

The design now lives in https://github.com/Yusuprozimemet/devloop (README added 2026-10-02); future loop work goes there, not here.
