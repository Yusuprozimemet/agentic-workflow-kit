# One-task workflow comparison: protocol

This is the cheaper route that [item 91](../CHANGES.md#91-defer-the-workflow-comparison-and-keep-or-simplify-for-token-cost)
left open: one task, run once with the kit (A) and once without it (B). Every decision below was
fixed on 2026-11-03, before either run. A change after that date goes in a PR that names it as a
departure, and the result reports it. Nothing here has been run yet. The result will go in
`kit/comparison/results.md`.

The [assessment's](../ASSESSMENT.md) recommendation 3 asks for three tasks. This protocol runs
one, so it gives one paired example and no rate. What it can show is fixed in
[section 8](#8-what-it-can-and-cannot-show) before any result exists.

## 1. The task

**Target repository:** [stefankoegl/python-json-pointer](https://github.com/stefankoegl/python-json-pointer),
the `jsonpointer` library: one module (`jsonpointer.py`, 446 lines), type stubs in
`jsonpointer-stubs/`, and `tests.py`, run with `python -m unittest`. Its CI runs flake8, a build
check, `mypy.stubtest`, a docs build and the tests on seven Pythons.

**Starting commit:** `7c78531542c81ee0d308cb044244c0b1adf37b39` ("bump version to 3.8",
2026-11-02).

**Why this task.** It comes from none of jobmatch, wordtally or the replay set: every case in
`kit/replay/manifest.json` is from jobmatch-microservices. The library has no Relative JSON
Pointer code at that commit. The only upstream trace is issue #34, which asks whether the feature
belongs in the library and was closed on 2026-10-02 for lack of traction. It holds no design and no
code, and both runs can see it. The feature has a written standard, so hidden tests can be
written now, and it touches the module, the stubs, the tests and the docs: one or two tracks.

**The task statement.** Both runs get this text word for word, between the lines:

---

Add Relative JSON Pointer support to jsonpointer, following draft-bhutton-relative-json-pointer-00, with this public API in jsonpointer.py:

1. `RelativeJsonPointer(rel)` parses a relative pointer string. The grammar is: a non-negative integer with no leading zeros (`0`, `1`, `12`, not `01`); then, optionally, an index manipulation, which is `+` or `-` followed by a positive integer with no leading zeros; then either `#` or a JSON Pointer (empty, or starting with `/`, with the same escape rules as `JsonPointer`). Any other string raises `JsonPointerException`. `str(p)` returns the string `p` was built from.
2. `RelativeJsonPointer.resolve(doc, base, default)` takes `base`, a `JsonPointer` or a JSON Pointer string naming the starting location in `doc`, and an optional `default`. Evaluation: (a) the starting location must exist in `doc`; (b) go up as many levels as the integer says, and going above the document root fails; (c) with an index manipulation, the location reached must be an array element: add to or subtract from its index, and an index outside the array fails; (d) with `#`, return the location's member name in its parent object (a string) or its index in its parent array (an int), and `#` at the document root fails; (e) otherwise, resolve the JSON Pointer part from that location and return the value. A failure raises `JsonPointerException`, or returns `default` when one is given (`None` included). An invalid `base` string always raises `JsonPointerException`.
3. `resolve_relative_pointer(doc, base, rel, default)` is a module-level function that does the same as `RelativeJsonPointer(rel).resolve(doc, base, default)`, with `default` optional.

The existing behaviour of `JsonPointer`, `resolve_pointer` and `set_pointer` must not change. Add tests, and document the new API.

---

## 2. Acceptance tests

**Written now, held outside every repository.** They are in
`C:\Users\HackYourFuture\yusup\agentic-workflow-kit-comparison-keys\`, beside the kit's folder.
That folder is not in the kit, not in either run repository, and not on GitHub:

| File | sha256 |
|---|---|
| `acceptance_tests.py`: 44 test methods | `0e46cd91cde679709ca22f53e0e39b0de330ad5c093f08c9691b4a401b440e0d` |
| `reference.py`: an implementation used only to check the tests | `1bcf1d58ccb12f54848232433d96071bf68fa3881b37175f11238aa581790d66` |

The tests cover the draft's twelve examples, index manipulation, the `#` cases, escapes and empty
member names, each kind of failure, defaults, the grammar, the module function and the old API.
Each test imports the new names itself, so a missing name fails each test, not the file.

**Checked before run B, by the maintainer** (this session was not allowed to run the upstream
code). In a scratch clone at the starting commit, with the file copied to the clone's root:
`python -m unittest acceptance_tests` must report 44 tests, all failing or erroring. Then, with
`reference.py` appended to `jsonpointer.py`, it must report `Ran 44 tests` and `OK`. Both lines
go in the run log. If a test is wrong, it is fixed before run B, the hashes above change in a PR,
and the result names the fix.

**Scored only after both runs have finished,** on each run's final `main`, in a fresh clone, with
the same file:

- **Pass:** all 44 pass, and every job of the upstream CI workflow passes on that commit (flake8,
  the build check, `mypy.stubtest`, the docs build, and the tests on every Python).
- **Partial:** 33 to 43 pass (at least 75%) and the upstream `python -m unittest` passes; or all
  44 pass but an upstream CI job fails.
- **Fail:** fewer than 33 pass, or the upstream tests fail, or `jsonpointer` does not import.

The hashes are checked again before scoring. A mismatch voids the comparison.

## 3. Conditions

Both runs start from the same **setup commit S0**, made by the maintainer on top of the starting
commit and nothing more: the branch is renamed `main`; the two `master` filters in
`.github/workflows/test.yaml` become `main`; `.github/workflows/publish.yml` is deleted, so no
run can publish to PyPI.

**A, the kit.** On S0, the kit is copied in as its README's "Starting a project from it" says,
from the kit's `main` at the merge of this protocol's PR (its sha goes in the run log). `kit/`
is deleted, so this protocol is not in the copy. Placeholders are filled with these values, in
one setup commit S1A:

- project: "adds Relative JSON Pointer support to the jsonpointer library"; no tracker; no
  Pages URL (the dashboard is `python scripts/spec-drift.py --out spec-drift.json`, run
  locally);
- build and test: `python -m unittest`, read as its "Ran N tests" and "OK" lines; style:
  `flake8`;
- contract tests: the test methods already in `tests.py` at the starting commit are never
  edited; no migrations bullet;
- implementer model: `claude-haiku-5-5`, as the kit ships it; last phase: Phase 1, with no
  end-of-phase auditors, since they judge the kit, not the task;
- any other placeholder: the nearest value above, or deleted when it names something the
  project lacks (services, a tracker, migrations).

`plan.md` holds the task statement as its one phase, Phase 1, with one day. Its "Done when" is
that the statement's API exists, its tests pass, and upstream CI is green on `main`.
`spec-drift.config.json` stays empty. On GitHub: the repository variable `STYLE_CHECK_COMMAND` is
`pip install -q flake8 && flake8`, `TRACK_RED_RUNNER` stays unset (the tests are not under
`tests/`), and the Dashboard workflow is disabled (`gh workflow disable dashboard.yml`), because
a private repository on a free plan has no Pages. A follows CLAUDE.md's day order: plan-auditor
and spec-auditor, a spec PR, one PR per track with the implementer, a closing PR with the
defect-rater, and the evidence check after the closing merge. A ends when it reports that check
and the next step.

**B, the minimal setup.** On S0, one setup commit S1B adds this `CLAUDE.md` and nothing else:

```markdown
# Working in this repository

- Style check: `flake8` (configured in `setup.cfg`). It must pass before a push.
- Tests: `python -m unittest`. They must pass before a push.
```

B has no auditors, specs, agents, hooks, kit scripts or closing step. B ends when it says the
task is done and its last PR has merged.

**The same for both:**

- The main session's model is `claude-opus-5-5`, set with `/model` before the first prompt and
  checked in the transcripts afterwards.
- A's implementer runs on `claude-haiku-5-5` and A's auditors as their files say. B may use
  Claude Code's built-in subagents. A therefore writes code with a smaller model than B. That is
  the kit as it ships, and the result names it as a confound.
- Both run in the same Claude Code version, in the VS Code extension, in the same permission
  mode; all three go in the run log.
- User-level settings, hooks and skills stay unchanged across both runs, and the sha256 of
  `~/.claude/settings.json` is logged. There is no user-level `CLAUDE.md`. The run repositories'
  paths are new, so project memory starts empty.
- Both repositories are private on GitHub, under the maintainer's account, and are created by the
  maintainer before run B. If the plan gives a private repository branch protection, A gets the
  README's required checks and B gets none, as a minimal setup would have none. If it does not,
  the maintainer applies A's required checks by hand: an A pull request is merged only when they
  pass, and otherwise gets the reply "merge blocked: <check> failed". That reply stands in for
  GitHub and does not count as an intervention.
- Neither condition gets a code review from the maintainer. Merging is the only human act on
  the code, so both results are model output, apart from the logged interventions.

**First prompts.** Each is the task statement, then one fixed line:

- B: "Work in this repository. Open pull requests against main; I merge them and say
  "merged". Stop when the task is done."
- A: "This is plan.md's Phase 1, a single day. Follow CLAUDE.md: write the Day 1 spec from
  specs/_template.md, then start Day 1."

After that, A opens each new session with the next-session prompt it handed over itself, pasted
unchanged. The maintainer starts a new session where A's CLAUDE.md asks for one, and never uses
`/compact`. B stays in one session, and Claude Code's automatic compaction is allowed.

## 4. Budget

**Sizing, from item 90.** The reduced baseline ran the spec-auditor 7 times: 6,004,251 tokens,
586,430 of them not cache reads, in 38.9 minutes; about 0.86 million tokens and 5.6 minutes per
auditor run. Run A holds three agent runs of about that size (plan-auditor, spec-auditor,
defect-rater) and about five main-session steps. The README puts a step at about 80 replies of
about 75k context, roughly 6 million tokens. That makes A about 33 million tokens, about five times
item 90's whole baseline.

**The cap, the same for each run:** 48,000,000 tokens including cache reads (8 times item 90's
total), or 4,700,000 tokens without cache reads (8 times its 586,430), whichever comes first.
**Wall-clock:** 6 hours of agent time, the sum of the spans from each maintainer message to the
agent's last reply before the next one. Time spent waiting for the maintainer is logged
separately and does not count. A run must also finish within 5 calendar days.

**On hitting a cap,** the maintainer interrupts at once, sends nothing more and starts no new
session. Open pull requests stay unmerged. The run is scored on its `main` as it stands, with the
cap, the time and the step it reached recorded. The hidden tests are also run on the newest
unmerged branch, and that score is reported as "not delivered".

**Counting.** The maintainer checks the totals at every session boundary and every
maintainer message, so a cap passed mid-session stops the run at the next one. Tokens are counted
by `scripts/token-usage.py` from each run's own transcripts. The script finds them by its own
folder's path, so:

- A: `python scripts/token-usage.py --out <scratch>/a-tokens.json` in A's repository. A fresh
  `--out` path is used, because the script keeps the larger of the file's counts and the
  transcripts', and the kit's copied `docs/dashboard/token-usage.json` holds the kit's own rows.
- B: the kit's `scripts/token-usage.py`, at the same kit sha, is copied untracked into
  `<B>/scripts/` after the run, run the same way, then deleted.

Main sessions and subagents are both counted. Input, cache writes, output and cache reads are
reported separately, and so is the script's list-price cost. The run paths must not be
prefixes of one another, because the script matches a project folder by name.

## 5. Assistance rule

During a run the maintainer may send only:

- the first prompt (section 3), and A's own next-session prompts, pasted unchanged;
- "merged", after merging a pull request the run opened;
- "continue", when a session stops before the end of its step with no question asked;
- an answer to a question the run asked, limited to what was asked;
- "merge blocked: <check> failed" (section 3).

Permission prompts are approved, except a read or write outside the run's repository, which is
refused. Each refusal is logged.

Anything else is an **intervention**: a hint, a correction, a pointer to a file, a fix by hand, a
rerun, or a question answered beyond what was asked. Each intervention is logged with its
timestamp, the session, its full text and its reason, and counts against the run. The result
reports the count beside the grade, and a run with any intervention is graded "assisted". The
run log is kept in `C:\Users\HackYourFuture\yusup\agentic-workflow-kit-comparison-runs\`, outside
both repositories. Each run's log has every maintainer message, with its timestamp.

## 6. Order and isolation

- **B runs first,** to the end, and then A. Before run B: the setup commits, both repositories,
  the hidden-test check (section 2) and the run log's header (versions, shas, paths).
- Each run has its own repository, at a new path (for example `C:\cmp\jp-b` and `C:\cmp\jp-a`),
  and only fresh sessions opened there. No session of either run opens the other's path, the
  keys folder or the kit's folder; permission prompts for them are refused.
- No prompt names the other condition, its repository or its results. The hidden tests run on
  neither result until both have finished.
- The maintainer knows each condition and watched B before A. The result says so: this cannot be
  blinded with one person.

## 7. What gets recorded

For each run, in the run log and then in `kit/comparison/results.md`:

| Measure | How |
|---|---|
| Acceptance | Pass, partial or fail (section 2), with the hidden tests passed out of 44 and each upstream CI job's result |
| Defects found by the hidden tests | Each failing hidden test, and each failing upstream CI job, grouped by cause after reading the code, with the test names |
| Defects the run caught itself | Each product behaviour the run's own PR descriptions, commit messages or spec Notes say was wrong in code it had written, and changed before its final `main`. Workflow fixes (PR names, diff size, wording) are counted apart, as compliance, not product defects |
| Tokens | From `token-usage.py`: input, cache writes, output, and cache reads, each apart; totals with and without cache reads; list-price cost |
| Minutes | Agent time (section 4), and the maintainer's wait time apart |
| Pull requests | Opened, merged, and closed without merging |
| Interventions | The count, and each one's text (section 5); refused permission prompts apart |

A's audit findings, and which of them changed the code, are recorded from its PRs, for reading
only; B has nothing to compare them with.

## 8. What it can and cannot show

Written before either run:

- **It is one paired example, not a rate.** One task and one run per condition: task choice and
  run-to-run variation can produce any difference seen. Nothing here estimates how often the kit
  helps.
- **It cannot decide keep-or-simplify** (assessment recommendation 5, which waits on
  recommendation 4's benefit-and-burden measure across tasks). It cannot judge any one component
  either: A differs from B in auditors, specs, hooks, PR discipline and implementer model all at
  once.
- **It cannot inform a choice of model** (recommendation 5's last step). Both runs use one model,
  and A's code comes from a smaller one.
- **What it can show:** on one unseen task, what the kit's full day costs beside a minimal
  setup, and whether that cost bought a difference the hidden tests can see.

**When the full three-task comparison is worth its cost**, decided now:

- **Worth running** if the grades differ (pass against partial or fail), or if the grades match
  but the hidden tests find at least 2 more defect causes in one run than in the other. Either
  is a difference big enough that three tasks could test whether it repeats.
- **Not worth running on this kind of task** if both pass with defect counts within 1 of each
  other: the task did not separate the conditions. The result then records A's cost as a
  multiple of B's, and any later comparison needs harder tasks, chosen before it runs.
- **No conclusion** if either run hits a cap or is graded "assisted" before it finishes, or if
  both fail. The task or the budget is then wrong, and is fixed in a new protocol before any
  three-task run.

The decision to spend on three tasks stays the maintainer's. These rules say only what this
example would support.
