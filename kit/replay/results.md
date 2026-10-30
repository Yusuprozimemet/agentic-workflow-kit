# Replay results

## Baseline, 2026-10-30 (reduced: 7 of 16 cases)

**What was run.** One spec-auditor run per case, with the [rules](README.md) in effect at kit
commit `6cc16edf1a7d8d9d38453d4ace27e18e7e0fabde`. The auditor brief was jobmatch's own at
`7cbae28920b08953f63a8c05ff549dcd89b7a910`, sha256
`506dc155c89a746d5a9994d6a216e4a83b897fa9d37d0db5cae41bafc2524db6`. The run used Claude Code
2.1.170 with claude-opus-4-8 and claude-haiku-4-5-20251001. Each case was exported
history-free into a fresh path, and the only prompt was "Audit Day N.", with the day number. The
saved outputs, the judging sheet and the run JSON are kept outside this repository.

**Which cases.**
- **Development:** the first three cases in the manifest were run.
- **Held-out:** one case of each kind, the first of that kind in manifest order. This rule was
  fixed before any held-out output existed.
- **Not run:**
  - dev-day28-review-ownership was interrupted by the maintainer, and not re-run.
  - The other eight cases were cut for time and token cost.

**Who judged.** Claude (an agent), not a person. The maintainer asked for this because the
implementing agent had hit its rate limit. The judge had seen the development keys before
judging, but not the held-out keys. Every output was read in full before its key. The
development keys are in this repository. The held-out keys were self-checked by the agent that
wrote them, and accepted by the maintainer.

### Per case: the auditor's cost

| Case | Kind | Minutes | Tokens |
|---|---|---:|---:|
| dev-day21-harness-routing | historical-defect | 9.8 | 2,038,185 |
| dev-day24-network-checks | historical-defect | 5.0 | 999,118 |
| dev-day27-consumer-isolation | historical-defect | 5.1 | 959,873 |
| held-day03 | clean | 3.8 | 571,445 |
| held-day07 | historical-defect | 6.9 | 628,475 |
| held-day08 | broken-check | 5.0 | 511,245 |
| held-day18 | cross-day | 3.2 | 295,910 |
| **Total** | | **38.9** | **6,004,251** |

The token figures include cache reads. The total is made up of:

| Token type | Tokens |
|---|---:|
| Input | 15,794 |
| Cache creation | 413,387 |
| Cache read | 5,417,821 |
| Output | 157,249 |

Without cache reads, the total is 586,430.

The agent spent about 3 minutes judging each case. This is not a person's review time, and the
later comparison should not compare against it.

### Scores

These come from `replay-set.py score`. The held-out cases are shown only as a total, so that
their keys stay unpublished.

| Cases | Full | Partial | Missed | Strict recall | Lenient recall | Missed blocking | False alarms | Precision | Valid outside key |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| dev-day21-harness-routing | 0 | 0 | 2 | 0.00 | 0.00 | 2 | 1 | 0.00 | 1 |
| dev-day24-network-checks | 2 | 3 | 5 | 0.20 | 0.50 | 0 | 0 | 1.00 | 1 |
| dev-day27-consumer-isolation | 2 | 0 | 8 | 0.20 | 0.20 | 3 | 0 | 1.00 | 2 |
| Development, total | 4 | 3 | 15 | 0.18 | 0.32 | 5 | 1 | 0.88 | 4 |
| Held-out, 4 cases, total | 5 | 7 | 1 | 0.38 | 0.92 | 0 | 1 | 0.92 | 4 |
| All 7 | 9 | 10 | 16 | 0.26 | 0.54 | 5 | 2 | 0.90 | 8 |

### How far these numbers go

- **This is one example per kind, not a rate.** There is one run per case. Seven cases cannot
  support a rate for any kind.
- **The held-out cases are held out from this run only.** Each snapshot SHA leads to its fix PR
  through jobmatch's public history.
- **The judge is a single agent.** It made the full/partial calls against the written rubrics,
  and where an output met only part of a full rubric it chose the stricter reading. A person, or
  a second rater, could score these differently.
- **The development and held-out totals are not comparable.** The development keys
  (historical-defect only) hold 22 findings. The held-out cases cover all four kinds, and their
  keys hold 13.

**What the later comparison must do.** It must re-run these same 7 cases, with the same scoring.
If it needs the rest of the set, it should first run the 9 cases left out here, under this
baseline's revision.
