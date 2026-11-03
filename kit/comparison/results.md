# One-task workflow comparison: results

Scored 2026-11-03 under [`protocol.md`](protocol.md) (PR #78, amended by #79). Run B, the minimal
setup, ran first; run A, the kit, ran second. The full run log, with every maintainer message and
its timestamp, is in `C:\Users\HackYourFuture\yusup\agentic-workflow-kit-comparison-runs\run-log.md`,
outside both repositories.

## Result

| | B, minimal | A, kit |
|---|---|---|
| Final `main` | `jsonpointer-rjp-1` `d48e029` | `jsonpointer-rjp-2` `68cd776` |
| Hidden tests | 44 / 44 | 44 / 44 |
| Upstream `python -m unittest` | 107 tests, OK | 94 tests, OK |
| Upstream CI on final `main` | run 41688701419: all 13 jobs pass | run 41703100229: all 13 jobs pass |
| **Grade** | **Pass** | **Pass** |
| Interventions | 0 | 0 (two judgement calls, below) |
| Defect causes found by the hidden tests | 0 | 0 |
| Product defects the run caught itself | 0 | 0 |
| Tokens with cache reads | 1,868,032 | 24,131,602 (12.9×) |
| Tokens without cache reads | 87,305 | 860,995 (9.9×) |
| List-price cost | $1.35 | $12.22 (9.1×) |
| Agent time | 9 min 10 s | 66 min 27 s (7.2×) |
| Pull requests opened / merged / closed unmerged | 1 / 1 / 0 | 8 / 8 / 0 |

**What this example supports (section 8):** both runs pass, and the hidden tests found no defect
cause in either, so the counts are within 1. The task did not separate the conditions, so a
three-task comparison on this kind of task is **not worth running**. A's cost is 12.9 times B's in
tokens with cache reads, 9.9 times without, 9.1 times at list prices, and 7.2 times in agent time.
Any later comparison needs harder tasks, chosen before it runs. The decision to spend on more
stays the maintainer's.

If either judgement call below were decided the other way, A would be "assisted" and the rule
would give **no conclusion** instead. Neither reading supports a three-task run.

## How it was scored

- The hashes of `acceptance_tests.py` (`0e46cd91…`) and `reference.py` (`1bcf1d58…`) were
  checked again before scoring. Both match the protocol.
- Each final `main` was cloned fresh from GitHub, with the hidden file copied to the clone's
  root. The commands were `python -m unittest acceptance_tests` and then `python -m unittest`, on
  Python 3.12.10 with `PYTHONDONTWRITEBYTECODE=1`.
- CI results were read with `gh run view` for the push run on each final `main`.
- Tokens were counted with the kit's `scripts/token-usage.py` at `745d125`, over each run's
  transcripts, subagents included. For A, the copy in `jp-a` was used; it differs from `745d125`
  only in line endings. A dedup-by-message count gave the same totals.

## Tokens

| | Input | Cache writes | Output | Cache reads | Without reads | With reads | Cost |
|---|---|---|---|---|---|---|---|
| B (1 session) | 54 | 63,013 | 24,238 | 1,780,727 | 87,305 | 1,868,032 | $1.35 |
| A (5 sessions, 6 subagent runs) | 584 | 636,374 | 224,037 | 23,270,607 | 860,995 | 24,131,602 | $12.22 |

Where A's cost went, by agent:

| Agent | Model | Replies | With reads | Cost |
|---|---|---|---|---|
| Main sessions | Opus 5.5 | 210 | 22.07M | $10.92 |
| plan-auditor | Opus 5.5 | 19 | 0.68M | $0.60 |
| spec-auditor | Opus 5.5 | 16 | 0.51M | $0.55 |
| implementer | Haiku 5.5 | 28 | 0.84M | $0.04 |
| defect-rater | Opus 5.5 | 2 | 0.03M | $0.12 |

Both runs stayed far under the caps of 48M tokens with cache reads, 4.7M without, and 6 hours.

## Time

- **B:** 9 min 10 s of agent time. You waited 48 s, in one wait.
- **A:** 66 min 27 s of agent time, over 16 spans. You waited 20 min 27 s: merging, starting new
  sessions, and the time between them. Wall clock was 18:00:18Z to 19:27:12Z.

## Pull requests

- **B:** #1, "Add Relative JSON Pointer support", +469 −2 in one commit.
- **A:** eight pull requests.
  - **The day's own:** spec #1, tracks A to C as #4, #5 and #6, and the close #7.
  - **Kit tooling, fixed during the run:** #2, #3 and #8.

  A's product change is smaller than B's.

  | | `jsonpointer.py` | `tests.py` | Docs |
  |---|---|---|---|
  | B | +153 | +226 | +75 |
  | A | +95 | +170 | +45 |

  Most of A's other lines are its spec (300 lines), the break manifest, the lab notebook, and the
  tooling fixes.

## Defects

**Found by the hidden tests:** none, in either run. No upstream CI job failed on either final
`main`.

**Product defects the run caught itself:** none, in either run.
- B's PR and commit describe no product behaviour that was wrong and then changed.
- A's 18 Defect entries in the spec's Notes all have cause spec, process or environment. Its
  track PRs are one commit each and describe no fixed product behaviour. A's entries are counted
  apart, under compliance and the spec below.

**B's one deleted line in `tests.py`,** flagged at the end of run B for scoring, is its import
line, extended with `RelativeJsonPointer` and `resolve_relative_pointer`. No upstream test was
removed or changed.

## A's audits, for reading only

B has nothing to compare these with.

- **Before any code**, the plan-auditor and spec-auditor found eight spec defects, fixed in spec
  PR #1:
  - a missing "upstream CI green" criterion, which became C01.12;
  - a flake8 line that assumed flake8 was installed;
  - a wrong test-count note;
  - a criterion with no runnable check;
  - two in-scope items with no criterion;
  - an untestable docs criterion;
  - three missing resolve cases;
  - a stubtest command that left its virtualenv behind.

  Three of them changed what the code had to do: C01.12, the docs criterion, and the three
  resolve cases. The hidden tests passed in B without them, so this example cannot show that they
  mattered.
- **Track B** found a gap in its own test pairs and added two.
- **The close** found two process gaps:
  - the track PRs did not record `break.py`'s arguments;
  - one recorded break count was stale.

The defect-rater's labels were compared in #7.

## Interventions and deviations

The maintainer's messages are listed in full in the run log.

**B:** the first prompt and "merged". No intervention.

**A:** the following messages count as allowed under section 5:

| Kind | Messages |
|---|---|
| First prompt | 1 |
| Handed-over prompts, unchanged | 4 |
| "merged" | 8: 7 alone, and #1's sent with the H01.1 answer in the next row |
| Answers limited to a question A asked | 3: "merged. H01.1: fix it in its own PR, before the closing PR." (with #1's merge), "1", and "yes" |

Two events were judgement calls. Both were decided as **not interventions**, so the run is not
graded "assisted":

1. **18:34:15Z, session `1cbcf475`.** You pasted GitHub's check lines for PR #2 instead of the
   protocol's wording. They read "Dashboard metric tests gate … Failing … Required" and "Drift and
   gap move when they should … Failing".
   - **Decision:** this is the allowed "merge blocked: <check> failed" in substance. It names the
     failing checks and that they block the merge, and nothing else: no hint, no correction.
   - **Why:** A had reported the same two failures itself at 18:26Z. Its reply worked out which
     run they came from and repeated its own plan.
   - **Not recorded until scoring:** the run log missed this message during the run; it was found
     in the transcript when agent time was summed.
2. **Session `1cbcf475`, a write outside the repository.** A permission prompt asked to let A
   write its auto-memory note, outside the repository, and you approved it. Section 5 says to
   refuse such writes.
   - **Decision:** not an intervention. An approval adds nothing from the maintainer to the run,
     and section 5 counts as interventions only content the maintainer adds.
   - **Why it changed nothing:** both runs ran in `permissionMode: auto`, so A's later memory
     writes went through with no prompt at all. Refusing that one prompt would not have closed
     the channel.
   - **What A used it for:** to carry notes between its own sessions, such as the hold-break
     arguments and Track B's departures. It deleted every note by the end.
   - **What it was not:** none of these notes came from the maintainer.

**Setup deviations.** Each was logged before either run started, except where noted.

- **Coveralls:** removed from S0 by #79.
- **Run paths:** moved from `C:\cmp` into `yusup\cmp`.
- **S1A:** excludes the kit's `scripts/` from flake8.
- **Permission mode:** the log header says "default (prompts on)", but both runs' transcripts
  show `auto`. The conditions were still equal: B's single transcript and all of A's show `auto`.
- **B's write outside the repository:** B created and removed an empty file at
  `$TEMP/../edit_rjp.py`. It raised no prompt in auto mode, so you refused nothing.

**Left unresolved by A,** with no question asked, so left unanswered:

- **H01.2:** let a break-manifest entry be judged by what it prints.
- **A CLAUDE.md pitfall:** track PRs should record each break's `break.py` arguments.

A also left `evidence.json` untracked in its repository root.

## Kit defects found by run A

Each is listed for the kit's CHANGES after the comparison.

1. **`scripts/test_auditor_guard.py` assumes five auditor agents.** A copy without the three
   end-of-phase auditors fails its own CI. A fixed this in #3.
2. **`scripts/evidence.py` and `scripts/spec-drift.py` look for tests only under `tests/`.** A
   project with a root `tests.py` replays every named test as "not defined". `seen-red.py` and
   `track-red.py` have the same assumption, and `track-red.py` also expects failures where these
   tests report errors. A fixed the first two in #2.
3. **The kit's `scripts/` fail upstream flake8.** A project linting its whole tree needs to
   exclude them. This was done in S1A.
4. **The spec's scratch-virtualenv command ends in `rm -rf`, which Claude Code refuses.** A kept
   the virtualenv instead.
5. **`.github/workflows/evidence.yml` installs no project dependencies.** Any replayed check that
   needs one errors; here, Sphinx for C01.12's breaks. A fixed this in #8.
6. **`evidence.py` does not pass `--expect-stdout` to `break.py`.** A check judged by what it
   prints replays as passing with the break in. This is A's H01.2.
7. **Nothing makes a track PR record `break.py`'s arguments.** The close had to rebuild 15
   breaks from the merged code.

## Limits

These stand as section 8 wrote them before either run. This is one paired example, not a rate. It
cannot judge any one kit component, nor any choice of model. The maintainer watched B before A,
and knew both conditions.
