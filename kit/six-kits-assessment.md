# Assessment of the kit after the six-kits plan

2026-11-03, on `main` at `e5c51fa` (the merge of PR #90). A reading of the repository as it is,
by a session (Fable 5.1) that did not write the plan or its pull requests. Every claim below was
checked against a file, a command run today, or a merged pull request's body; where it could not
be, it says so. Nothing here changes a rule.

## 1. Implementation status of `kit/six-kits-plan.md`

The plan's five "adopt now" items and one of its three "improve later" items are merged. The
kit's own test suite ran today: 461 tests, OK, in 164 s (`python -m unittest discover` in
`scripts/`).

| Item | Status | Evidence |
|---|---|---|
| 1. Size-of-change ladder | **Done** | PR #85 (+30/−1, docs). `specs/README.md` lines 14–26: the three-rung table, the rule "take the lowest rung that qualifies, and say which in the PR", the area list from `pr-names.py`, `broken: none` for a docs-only area PR. `specs/_short-template.md` gained a Notes section with a `Defect` line. `CLAUDE.md` lines 24–25 point at the table. `docs/architecture.md` lines 262 and 268 draw the area-branch arm. The ladder row for short specs now says "the replay", since item 2 merged. PRs #86–#90 each name their rung in the body. |
| 2. Short specs replayed | **Done, untested in production** | PR #87 (+155/−16). `scripts/evidence.py`: `CHANGE_MERGE` (line 64) finds the merge of `change/<slug>` or a squash that adds `specs/changes/<slug>.md` (lines 129–130, 321–338); criteria `S-<slug>.N` (line 63); breaks from `specs/breaks/<slug>.json`. `close-evidence.py` replays "the short spec landed by a push", and `evidence.yml` runs on every push to `main`. Seen red: `test_evidence.ShortSpecTest` failed on `main` (failures=3, errors=1). Broken on purpose: the breaks path → "1 failed". One PR, not the two the plan allowed. **Not shown:** no project has yet merged a `change/` branch through `evidence.yml`; the kit repository has no `specs/changes/`, so the only evidence is the unit tests. |
| 3. Replies per merged PR, `--split` | **Done** | PR #86 (+117/−13). `scripts/token-usage.py` lines 512, 544, 554: `--split DATE` adds a second split to `--compare`; each side prints its merged pull requests and replies per PR, read as `spec-drift.py` reads them. Seen red: `test_token_usage` on `main` → errors=4. Broken on purpose with the failing assertion quoted. Run today (`--compare --split 2026-11-03`): 36.8 replies per merged PR before 2026-11-02, 50.3 on 2026-11-02, 54.6 on 2026-11-03. The split date is typed by hand; nothing stores the ladder's landing date. |
| 4. "Not proven" in the replay | **Done** | PR #88 (+121/−28). `evidence.py` lines 76, 172, 348–375: an unticked criterion is reported `not proven` and passes only with a `Not proven: <why>` line under it *at the closing commit* (the break on purpose was exactly reading it from the working tree instead, and the test caught it); each criterion gets a `proved by <test, command, break, reader>` line; a ticked criterion with none of the first three fails unless a reader's reason is recorded. `specs/README.md` lines 228–232 and `_short-template.md` state the rule. Seen red: 7 of 38 tests failed on `main`. Side change not in the plan: a `broken:` line alone now proves a criterion (the "named test" check becomes n/a); the PR says so. Gap: `specs/_template.md` (the day template) carries no `Not proven:` hint; only the short template does. |
| 5. One ending per auditor finding | **Done, not counted** | PR #89 (+14/−0, docs). `specs/README.md` lines 191–198: four endings (`fixed`, `known limit`, `maintainer action`, `rejected`), "Auditor findings: none" when empty, and "Nothing counts the endings" yet. `.claude/agents/spec-auditor.md` line 71 tells the auditor to write one copyable line per finding. `.github/pull_request_template.md` line 40 has the self-check. No CI check reads it; `broken: none` is honest. |
| 6. Context warning hook | **Not implemented, as planned** | Conditional on the 2026-11-09 re-measure showing sessions past 150k. `.claude/settings.json` has only `auditor-guard.py`, `read-guard.py` and `cap-output.py`. Whether a hook can read the session's context size is still on the plan's "Unverified" list and cannot be settled from the repository. |
| 7. Defect IDs and `same-as:` | **Done, earlier than planned** | PR #90 (+179/−12). `specs/_template.md` lines 37–39: `D<NN>.<n>` and optional `same-as:`. `specs/README.md` lines 133–148 (a short spec's Defect lines take no ID). `scripts/spec-drift.py` lines 336–394: `defect_lines()` and `recurrence()`, with problems reported for an ID that is missing, duplicated, not earlier, or names nothing; printed at line 1647. `docs/dashboard/dashboard.js` lines 996–1004 show the count. `scripts/relabel.py` strips `same-as:` with the tags (lines 9–10, 25, 55). Two breaks on purpose, both reported. The plan put items 6 and 7 "after the re-measure" so nothing else moves the per-reply numbers; #90 landed on 2026-11-03 and its body names "step 6 in its order" without saying it is early. The change alters no file a reply reads at its start, so the confound is small, but the departure is unrecorded. |
| 8. Three runs per replay | **Not done** | `kit/replay/results.md` still has one run per case, 7 of 16 cases. The plan leaves this to the maintainer's funding decision; nothing in the repository records one. |

**Dropped items, checked:** no implementer stop hook in `settings.json`; no autonomy key in
`spec-drift.config.json` (its keys are the eight the plan lists, all empty in the kit); no
`.claude/skills/`; the implementer stays on Haiku as before and no other routing exists; the
hooks of 2026-11-02 are the only per-reply levers in place. All as the plan says.

**Housekeeping the plan did not list:** `kit/CHANGES.md` ends at item 130 (PR #83); PRs #84–#90
are not recorded there, though the kit's convention is to record every PR. `docs/workflow.md`
does not mention the ladder.

## 2. Strong sides

These are mechanisms, not intentions. Each is in the repository and most are exercised by the
kit's own pull requests from today.

- **Every check must have been seen to fail, and the failure is recorded.** `scripts/seen-red.py`
  runs a branch's tests on `main`'s code in a scratch worktree; `scripts/break.py` applies one
  exact replacement, runs the check without a shell, restores the bytes, and prints both the
  `broken:` line and a `manifest:` entry. PRs #86, #87, #88 and #90 all carry the seen-red
  count and the quoted failure. The break in #88 caught a real fault in its own design (reading
  `Not proven:` from the working tree). Few workflows make the "can this test fail" question
  mechanical.
- **Evidence is replayed after the merge, at the commit, by CI.** `evidence.yml` runs on every
  push to `main`; `evidence.py` reads the spec at the closing commit, re-runs the Verify
  commands and the recorded breaks, and now reports unticked criteria and what proved each. The
  closing PR cannot gate itself, which the docs state rather than hide.
- **Spec wording and test counts are protected by CI**, not by convention: "Criteria keep their
  wording", "Frozen files stay unedited", "Diff stays reviewable" (400 lines, override only
  with a written `Oversized:` reason), "Branch, title, commits and Jira keys agree".
- **Role separation with a hook behind it.** Auditors are read-only and `auditor-guard.py`
  blocks writing git and `gh` commands and compares HEAD, refs, stash and status at their stop.
  The implementer (Haiku) never commits; the main session reviews, breaks and writes the PR. The
  docs say exactly what the guard cannot see (`python -c` that writes a file).
- **Defects are a first-class record with a blind second rating.** Every defect is a tagged line
  (`found`, `cause`, `made`, now an ID and `same-as:`); `relabel.py` strips the tags and a
  separate agent re-labels; the close must decide each disagreement in writing. Recurrence is now
  counted.
- **Cost is measured on real transcripts, priced, and used to kill ideas.** `token-usage.py`
  reports context per reply, dollars per reply, replies per merged PR, and simulates three
  levers; all three were measured under 10% and dropped (PRs #73–#75). The plan itself rests on
  this: "a reply costs about $0.054 whatever it does", so the number of replies is the lever.
- **Unfavourable results are published.** `kit/comparison/results.md` reports the kit at 9.1×
  the list-price cost, 7.2× the agent time and 8 PRs against 1 for a task where both runs passed
  every hidden test. `kit/replay/results.md` reports the spec-auditor's strict recall at 0.18
  on development cases and 0.38 held out, with 5 blocking findings missed. The plan's "Unverified"
  section lists what it could not check.
- **The kit obeys its own rules.** Today's six PRs each name a rung, stay under 400 lines, and
  carry seen-red or `broken: none` with a reason.

## 3. Weak sides and remaining gaps

- **The cost evidence points the wrong way so far.** Replies per merged PR rose from 36.8
  (before 2026-11-02) to 50.3 and then 54.6 today. Today's window is the plan's own tooling
  work, so it is not a verdict on the ladder, but it is the only post-ladder number and it is
  worse. The one controlled comparison found a 9–13× cost for no measured quality difference.
- **The ladder's cheap rungs are unproven in use.** No `change/` branch has been replayed by CI
  anywhere; no area-branch rung has been used on product work. The kit repository, being a
  template, has no day specs, no `specs/changes/`, and a dashboard that shows example data under
  a banner.
- **The auditors' detection rate is low and measured once.** Strict recall 0.18 and 0.38, one run
  per case, 7 of 16 cases, judged by an agent in about 3 minutes per case. The plan costs two more
  runs at about 12M tokens and leaves them unfunded. Anything that relies on "the spec-auditor
  would have caught it" is resting on these numbers.
- **Much of the quality signal is self-reported text.** `seen red:`, `broken:`, `Not proven:`,
  the four endings, and Defect tags are written by the session that did the work. `break.py`
  formats the `broken:` line from a real run, and CI can re-run `new` criteria only when
  `TRACK_RED_RUNNER` is set; the rest is prose the maintainer reads. The endings are explicitly
  not counted yet.
- **Rules live in long prose.** `CLAUDE.md` (262 lines, about 5k tokens read by every reply),
  `specs/README.md` (275), `docs/architecture.md` (400), seven agent briefs. A newcomer has to
  read roughly 1,800 lines of rules before a first day, and the CLAUDE.md pitfalls section is a
  list of ways the process has already gone wrong on Windows, CRLF, heredocs and WSL.
- **Platform coupling.** Claude Code hooks (with a note that frontmatter hooks were ignored by
  one extension version), `gh`, GitHub Actions, GitHub Pages, Python scripts, transcripts on one
  machine. `token-usage.json` is hand-committed because CI cannot read transcripts; `--split`
  dates are typed by hand.
- **Small gaps from today's work:** `_template.md` lacks the `Not proven:` hint; `CHANGES.md`
  is seven PRs behind; `workflow.md` does not draw the ladder; item 7 landed ahead of the plan's
  order without a note.
- **The plan's unverified list is still unverified:** B's reply count in the comparison, what the
  50k start of a session is made of beyond `CLAUDE.md`, whether a hook can read context size.
- **Sample size.** One origin project (jobmatch), one pilot (wordtally), one comparison task,
  one machine, one maintainer. The measurements are real but they are n=1 in most dimensions.

## 4. Trade-offs, stated both ways

- **Verification strength vs. token and reply cost.** Seen-red, breaks, manifests, replay and a
  blind rating make every "done" checkable at the commit. The price is about 8 PRs and 210 main
  replies where a plain session took 1 and far fewer, on a task where both passed. The ladder is
  the bet that the gates can be kept at a fraction of the ceremony; it is not yet measured.
- **Human control vs. speed.** Nothing merges without the maintainer, nothing starts after a
  phase ends until they say so, one PR at a time from fresh `main`, never stacked. This gives a
  clean audit trail and stops runaway agents, and it serialises all work through one person's
  attention.
- **Day-spec rigour vs. short-path practicality.** A day has auditors, tracks, a close, a blind
  relabel and a replay; a short spec skips the auditors and the relabel; an area branch skips the
  spec. The ladder makes the choice explicit, which is better than the earlier implicit "everything
  is a day", but each lower rung drops a gate, and the rule for choosing is one sentence.
- **Measurement honesty vs. recording overhead.** Every defect, break and finding is written down
  in a fixed format so scripts can count them. That is why the comparison and replay results
  exist. It also means every PR body is long, every close is a checklist, and the session that
  makes a mistake is the one that must write it up.
- **Single-platform depth vs. portability.** Hooks that enforce read-only auditors and ranged
  reads only exist because the kit targets Claude Code on GitHub. Moving to another agent or
  forge loses the enforcement and keeps only the prose.
- **Smaller model for code vs. more review.** Haiku writes the code; Opus reviews, breaks and
  audits. Cheaper tokens per line written, but the expensive session reads everything twice, and
  the docs record the implementer's counts being wrong (45 words reported as 40).
- **Self-measurement vs. independence.** The scripts that measure the kit are in the kit and were
  written by the sessions being measured. They are tested (461 tests) but not independently
  validated.

## 5. What projects it suits

**Good fit.** A single maintainer, or a pair, changing a codebase they must keep running over
weeks or months, where a regression costs more than a day of ceremony: service migrations,
infrastructure, auth, data pipelines, anything with contract tests that must not move. Python
or a stack with a one-line test command, on GitHub, driven through Claude Code. Also any group
studying agent workflows who wants per-reply cost, defect provenance and replayable evidence
rather than anecdotes.

**Poor fit.** Prototypes, spikes, one-off scripts, greenfield exploration where the spec is
unknown until the code exists, and anything under a few hundred lines. A team of several
developers merging in parallel: the one-PR-at-a-time rule and the single merging human are a
bottleneck by design. Projects not on GitHub or not using Claude Code lose the hooks and CI.

**Borderline.** A library change of a few hundred lines with a good upstream test suite, which is
what the comparison ran: the kit cost 9× and found nothing extra. The short-spec and area rungs
exist for this case, and until they are measured the honest answer is "probably too heavy".
Teams with an existing review process: the kit's PR template and CI checks can be adopted alone,
but the day cycle will fight an existing cadence.

## 6. Where it will not pay off

- Work where the cost of a wrong change is low or cheaply reversible.
- Work where the person is not going to read the PRs: the gates are prose checked by a human.
- Time-boxed work: a day is several sessions and several PRs with waits for "merged" between.
- Anything whose tests are not runnable by one command on a fresh checkout, since seen-red,
  breaks and the replay all assume that.
- Teams that cannot or will not keep the paperwork current: the dashboard and replay only count
  what was written in the fixed format, and a half-kept record is worse than none because it
  looks like data.

## 7. Practical maturity today

**As a research and measurement instrument:** usable now, with the sample-size caveats above.
The token accounting, the comparison protocol, the replay set and the defect taxonomy are
concrete, tested and documented, and the results files already show the instrument reporting
against its own design. That is its strongest current use.

**As a production workflow for a serious project:** usable by its author, who has run it on two
projects and knows the pitfalls. Not yet shown usable by someone else: no adopter outside the
author has completed a day, and the setup section of `README.md` plus 1,800 lines of rules is the
onboarding. The gates work; the question the repository cannot yet answer is whether the gates
catch enough to justify their price.

**Before trusting it on important work:**
- The 2026-11-09 re-measure done as the plan says, with the ladder used on real product work in
  that window, and replies per merged PR falling without any quality count worsening.
- At least one `change/` merge replayed by `evidence.yml` on a real project.
- A second replay run on the held-out cases, so the auditor recall has a spread.
- One person other than the author running a day from the README alone and reporting where
  they got stuck.

## 8. Biggest risks of adopting it now

- **Cost without return.** The only comparison shows a large multiple for no measured gain, and
  replies per PR are rising. An adopter can spend a quarter's token budget on process.
- **False confidence.** A green replay means the recorded checks still pass at the commit; it
  does not mean the product is right. The hidden tests in the comparison found nothing in either
  run, and the auditors miss most seeded findings. The `Not proven:` and endings lines are
  honest by design but are free text that nothing counts.
- **Abandonment under load.** Every gate is a line to write and a wait for "merged". When the
  maintainer is busy the paperwork lags, and the measurements then describe a process no longer
  followed. `CHANGES.md` being seven PRs behind on the day the plan landed is a small instance.
- **Maintenance of a large toolchain.** About 10,500 lines of Python in `scripts/`, 461 tests,
  five workflows, seven agent briefs, one maintainer. The pitfalls section shows how much of it
  is Windows- and Claude-Code-version-specific, and an editor update has already silently
  disabled hooks once.
- **Measurement drift.** Hand-committed `token-usage.json`, hand-typed `--split` dates, and a
  dashboard that trusts the format of PR bodies: an unnoticed change in any of them changes the
  numbers without changing the work.

## 9. Highest-leverage next steps

Ranked by expected value given today's state. Nothing new until the first is done.

**Reduce cost without harming quality**
1. **Run the re-measure as written and use the ladder in that window on product work**, not kit
   tooling. Keep the ladder only if replies per merged PR fall with no quality count worse. This
   is the plan's own criterion, and nothing else in the plan matters until it is answered.
2. **Count what the 50k session start is made of.** One short script over a transcript's first
   request. It decides whether anything about `CLAUDE.md` or skills is worth touching, and it
   closes an "Unverified" item for almost nothing.

**Improve quality and evidence**
3. **A second replay run on the four held-out cases only.** Roughly half the cost the plan
   quotes for all seven, and it turns four single numbers into four pairs.
4. **Replay one real short spec through CI** on wordtally or the next pilot, and record the run
   ID in the lessons. Item 2 is tested but has not been seen working.
5. **Count the endings and `Not proven:` reasons in `spec-drift.py`** once two or three days
   have produced them, so the gates added today become data rather than prose.

**Housekeeping, cheap:** record PRs #84–#90 in `CHANGES.md`; add the `Not proven:` hint to
`_template.md`; add the ladder to `docs/workflow.md`; note in the lessons that item 7 landed
before the re-measure.

## 10. Overall judgment

The kit today is a rigorous, well-tested harness for making an agent's claims of "done"
checkable after the fact, plus an honest set of instruments for measuring what that rigour
costs. The plan's adoptable items are all merged, each with its own failing test or a reason why
none exists. What the repository shows is that the gates hold and the measurements run; what it
does not yet show is that the gates are worth their price. Its own comparison says the full day
cycle is an order of magnitude more expensive for no measured gain on a mid-sized task, its own
replay says the auditors miss most of what they are meant to catch, and its first post-ladder
number is worse, not better. A careful adopter should read it as a research-grade process with a
strong evidence trail, take the parts that stand alone (seen red, `break.py`, the PR template and
CI checks, the defect lines) at low cost, and treat the full day cycle as something to adopt
only after the re-measure and a replay with more than one run say it earns its keep.
