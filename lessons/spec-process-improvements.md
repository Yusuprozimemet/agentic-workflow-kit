---
name: spec-process-improvements
description: "Which spec-process changes the user adopted after the Sep 2026 drift analysis, in what order, and how each was scoped"
metadata:
  node_type: memory
  type: project
  originSessionId: 4d5bce22-ed4a-49b9-bed5-cee9f46c51ce
  modified: 2026-09-23T09:47:27.854Z
---

After the spec-drift analysis (artifact https://claude.ai/artifact/P4hgiTKiESmCEGRL75oQ58, scripts were in a session scratchpad), the user reviewed six proposed spec-process changes on 2026-09-23 and settled:

1. **new/hold criterion tags + every check seen failing**: adopted first, PR #55 (template, specs/README, PR checklist). Existing specs get tagged in their own day's spec-change PR, starting Day 10.
2. **Counted claims carry the command that counted them**: keep command + expected number, NOT pasted output. The rule is "state how you counted", since grep has blind spots too.
3. **Spec lint in CI** (backticked names must exist): build after #1, and lint only In scope + Acceptance criteria (Notes/Out of scope mention old names). Complements #2 and doesn't replace it.
4. **Detail only two days ahead**: REJECTED. Keep acceptance criteria and invariants detailed all the way ahead, and write implementation detail at N+2. Far-day specificity is what found cross-day contradictions (Day 02 vs 13 JSESSIONID, Day 03 vs 08).
5. **Estimates**: count overhead PRs separately. The track-only overrun for Days 1–8 is ~1.1× (23 planned vs ~26 code PRs), and Day 05 is the outlier. The user prefers planned-vs-actual lines per track over PR counts.
6. **Test review with a planted defect**: it must be blind (separate agent session or a random script revealed after merge), and review catches must be logged first. CodeRabbit skips this repo (<10 stars), so the user is the only reviewer.

**Why:** The user wants these to read as decisions, not a wishlist. A "What to change" section on the artifact waits until they have decided what they adopt.
**How to apply:** Follow the order above. Expect Phase 2 to show mixed spec-vs-code gap closing, with the clean read at Phase 3. Related: [[spec-first-workflow]].
