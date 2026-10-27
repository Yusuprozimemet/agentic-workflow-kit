---
name: spec-first-workflow
description: "How the user wants day specs worked in jobmatch-microservices - read spec vs code first, spec-change PR, one PR per track, wait for merge, closing PR"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 44a3ae46-4d2d-4c5f-a102-b4c1cc186e65
  modified: 2026-09-27T11:17:00.294Z
---

Work the day specs in `specs/` one day at a time, in order. For each day: read the spec against the actual code and run its verify command before writing code, and fix any spec defects in their own PR first. Then open one PR per track, branched from fresh `main` after each merge (never stacked). Finish with a closing PR that ticks the criteria with their evidence, adds Notes to the spec, and updates the README's "Results to date" and measurement table. The estimate counts track PRs only, not the spec change or the closing PR. After opening a PR, stop and wait for the user to say "merged".

**Why:** Reading the spec against the code found a defect on 7 of the first 8 days, including verify commands that ran nothing. The user values a public record of corrections, including Claude's own mistakes.

**After every "merged", before the next step:** since PR #79 (2026-09-23) the merge itself republishes the public dashboard to GitHub Pages (https://yusuprozimemet.github.io/jobmatch-microservices/, `.github/workflows/dashboard.yml`). On fresh `main`, run `python scripts/spec-drift.py --out spec-drift.json` and tell the user the next step it prints. Do NOT republish the old claude.ai dashboard artifact (https://claude.ai/artifact/P4hgiTKiESmCEGRL75oQ58): on 2026-09-27 the user said it no longer needs updating, since GitHub Pages replaces it.

**How to apply:** Before trusting a new test that passes both before and after the change, make it fail on purpose. Record departures from the spec instead of silently deviating. Related: [[checks-before-push]].
