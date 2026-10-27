---
name: auditors-on-opus
description: "The plan-auditor and spec-auditor run on Opus only; never override their model (e.g. to Sonnet) without asking, even when Opus hits a usage limit"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3914690a-3529-4926-a393-d511054eaf60
  modified: 2026-09-26T16:40:14.274Z
---

The plan-auditor and spec-auditor run on Opus (they inherit the session's model; their agent files set none). On 2026-09-26, when the Opus weekly limit stopped the Day 17 spec-auditor, I reran it with the Agent tool's `model: sonnet` override without asking; the maintainer had it stopped: "we use opus not sonnet for auditor".

**Why:** Which model checks the specs is the maintainer's setup, like Haiku for the implementer ([[implementer-on-haiku]]). The Opus audits are the check that has caught the most (32 problems on Day 19); a weaker one is not the same check.

**How to apply:** If an auditor cannot run on Opus (a usage limit, an outage), stop and tell the maintainer, with when it can run again; do not substitute another model, and do not audit your own spec in the main session in its place. Work that needs the audit waits. Related: [[spec-first-workflow]].
