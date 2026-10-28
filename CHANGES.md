# Proposed changes

Items marked **Done** are applied; the rest are not. Each batch is one commit, chosen by the
maintainer, with the copied tests passing before and after. A done item names its batch; the
batch's commit subject starts `Batch N:` (`git log --oneline --grep '^Batch N:'`). Smallest and safest first. "Tests" says whether a copied test covers
the change today.

Baseline, at `9151c8f`: 6 of 8 copied suites pass. `test_relabel.py` (1 of 8 failing) and
`test_spec_drift.py` (1 of 69 failing) fail only because jobmatch files are missing (items 8 and 9).
`spec-drift.py` crashes in a repository with no remote (item 14).

## Small: ignores, text, dangling references

1. **`.gitignore`: `__pycache__/`.** Running `python scripts/test_*.py` leaves
   `scripts/__pycache__/` untracked. Add the line. Why: the kit's excerpt has only the dashboard
   cache. Tests: no.
   **Done in Batch 1.**

2. **`docs/dashboard/index.html`: the name.** Line 6 `<title>JobMatch Spec Drift</title>`, line 15
   `jobmatch-microservices` in the eyebrow. Change: a project name, from the same config value as
   items 11-12, filled in by `--build`. Why: every project's page says JobMatch. Tests: no.

3. **`docs/dashboard/dashboard.js`: the name.** Lines 587-588 write
   `jobmatch-microservices · Day …`. Change: as item 2. Tests: no.

   **Items 2 and 3 done in Batch 1, differently from the proposal:** fewer lines than a config value
   filled in by `--build` (the data carries no repository name). `dashboard.js` has one marked value,
   `const PROJECT = "jobmatch-microservices";  // PROJECT: …`, used for the eyebrow and the tab
   title; `index.html` has a neutral `<title>Spec Drift</title>` and an empty eyebrow, both set by
   the script. A project edits that one line. The tab title becomes `jobmatch-microservices Spec
   Drift` where it was `JobMatch Spec Drift`.

4. **`specs/README.md` line 75: dangling link** to `../docs/paper/success-criteria.md` (not
   copied; `check-links.py` reports it). Change: drop the link or name the idea it points to in
   place. Tests: no.
   **Done in Batch 1:** the link removed; the text `` `docs/paper/success-criteria.md` `` kept.

5. **`docs/lab-notebook.md`: three dangling links** (lines 3 and 1088 to `../README.md`, line 1095
   to `paper/success-criteria.md`). Change: none if the notebook stays jobmatch's record (flag J);
   otherwise replace it with an empty notebook template. Why: it is jobmatch data. Tests: no.
   **Done in Batch 1:** the three links removed, their text kept; the notebook stays jobmatch's
   record.

6. **Dangling paths in backticks.** `check-links.py` does not see these, because they are not
   Markdown links:
   - `.claude/agents/security-ops-auditor.md`: `docs/runbooks/deploy.md`, `scripts/db-setup.py`,
     `scripts/db-init/`, `scripts/deploy-preflight.sh`, `scripts/teardown-check.sh`,
     `scripts/write-secrets.sh`.
   - `.claude/agents/architecture-auditor.md`: `scripts/infra-checks.py`,
     `scripts/teardown-check.sh`.
   - `CLAUDE.md`: `scripts/db-setup.py`, `scripts/db-init/`. The template has these as a placeholder
     already.

   Change: in the two agents, replace the paths with a placeholder ("the project's deploy runbook
   and setup scripts"). Leave `CLAUDE.md` as jobmatch's reference copy. Why: an auditor told to read
   a file that does not exist reports a finding about the kit, not the project. Tests: no.

   **Done in Batch 1, as examples rather than placeholders:** the paths are kept and marked
   "jobmatch's, as examples" (security-ops: the Infrastructure bullet and the database-role
   scripts; architecture: `scripts/infra-checks.py`, `scripts/teardown-check.sh`); no other word
   changed. `CLAUDE.md` left as jobmatch's reference copy.

   **Known, checked by hand.** `check-links.py` is not extended. These backticked paths in the
   agents and spec rules do not exist in the kit (found by listing every backticked path with a `/`
   and testing it, Batch 1); each is jobmatch's, or a pattern rather than a file:
   - `architecture-auditor.md`: `scripts/infra-checks.py`, `scripts/teardown-check.sh` (marked),
     `services/identity-service/src/test/.../contract/`.
   - `implementer.md`: `db/migration`, `services/identity-service/`, `src/test/.../contract/`
     (P agent, wording kept, not marked).
   - `security-ops-auditor.md`: `docs/runbooks/deploy.md`, `infra/terraform/`,
     `infra/terraform/bootstrap/`, `scripts/db-init/`, `scripts/db-setup.py`,
     `scripts/deploy-preflight.sh`, `scripts/teardown-check.sh`, `scripts/write-secrets.sh` (marked),
     `services/api-gateway/`.
   - `specs/README.md`: `contract/`, `day-04/track-b-saved-jobs-tests` (a branch name),
     `docs/paper/success-criteria.md` (its link removed, item 4).
   - `CLAUDE.md`: `scripts/db-setup.py`, `scripts/db-init/` (jobmatch's reference copy).

7. **`templates/`: links that resolve only after the copy.** `check-links.py` reports 12 links in
   `templates/CLAUDE.template.md` and `templates/plan.template.md` (`plan.md`, `specs/`, …). They
   resolve once a template is copied to a project's root. Two are false hits on
   `](<!-- PROJECT: GitHub Pages URL -->)`. Change: none to the files. Say in a templates README
   that they are meant for the root. Tests: no.

## Tests that read jobmatch's own files

8. **`scripts/test_relabel.py` line 40, `PaperSampleTest`:** expects 82 defect entries and 11
   escapes in `specs/day-21..28` (82 != 0 in the kit). Change: skip when those specs are absent
   (`unittest.skipUnless`), or move the check to a fixture of two small specs. Why: it measures
   jobmatch's record, not the tool. Tests: it is the test.
   **Done in Batch 2, as a fixture:** `SampleTest` writes two small day specs (Days 21 and 22) with
   the qualified `found:` values older Notes use, and checks the same three things: 7 entries, 3
   escapes, none without a stage.
   - `broken: relabel.stage keeps a qualified found: value's "(...)" → AssertionError: Lists differ: [] != ['auditor (spec-auditor)', 'review (Track A)']`
   - `broken: relabel.made never reads a defect as made on an earlier day → AssertionError: 3 != 2`

9. **`scripts/test_spec_drift.py` line 739, `test_the_repositorys_plan_parses`:** reads the real
   `plan.md` and `specs/`, and hard-codes Phase 6's cut days `(29, 30, 31)`. In the kit,
   jobmatch's plan lists Days 17-43 but only Days 12 and 36 exist. Change: keep the test (every
   project wants "my plan parses") but drop the `(29, 30, 31)` literal, reading cut days from the
   plan instead. Why: it is the right check, with jobmatch's numbers in it. Tests: it is the test.
   **Done in Batch 2, as a fixture rather than by reading cut days from the plan:**
   `test_a_plan_and_its_specs_parse` writes a plan.md (Days 12, 11, 13; a stop after Phase 3 lifted
   by its course correction; Days 16-17 **cut**) and nine empty specs to a temp dir, reads them as
   the old test read the repository's, and checks the same two things. The cut days `(16, 17)` are
   the fixture's own.
   - `broken: run_order no longer takes a **cut** item's days out → AssertionError: Lists differ: [10, 11, 12, 13, 14, 15, 16, 17, 18] != [10, 11, 12, 13, 14, 15, 18]`
   - `broken: run_order no longer finds the course correction that lifts a stop → AssertionError: 15 is not None`

## CI jobs that are jobmatch's

10. **`.github/workflows/dashboard.yml` lines 15-19: `workflow_run` on `"Infra checks"`.** That
    workflow is jobmatch's `infra-ci.yaml`, not copied. In the kit the trigger never fires, so it is
    harmless but misleading. Change: remove the block, or name the project's own infra workflow
    from config. Tests: no.
    **Done in Batch 3, by a comment only:** GitHub fires `workflow_run` only for a workflow with that
    name, so with none the trigger is already inert; the block is kept, with a comment saying so. Not
    seen on GitHub (the kit has no remote).

11. **`.github/workflows/pr-checks.yml` job 4, "Every service is wired into compose and
    Prometheus" (`service-wiring.py`).** It reads `services/*`, `docker-compose.yml` and
    `observability/prometheus.yml`; with no `services/`, `os.listdir` raises and the job fails on
    every PR. Change: run it only when `docker-compose.yml` exists
    (`if: hashFiles('docker-compose.yml') != ''`), or move it out of the kit's default
    `pr-checks.yml`. Tests: `test_service_wiring.py` covers the script (7/7 pass), not the job's
    condition.
    **Done in Batch 3, on `services/` rather than `docker-compose.yml`:** the step running
    `service-wiring.py` has `if: hashFiles('services/**') != ''`. `hashFiles` is not available in a
    job-level `if:`, so the condition is on the step; `test_service_wiring.py` (fixtures only) still
    runs. Correction: run in the kit, the script fails first on the missing `docker-compose.yml`
    (`FileNotFoundError`), not in `os.listdir`. Not seen on GitHub (no remote).

12. **`.github/workflows/pr-checks.yml` job 3 and `scripts/invariants.py`: frozen paths.**
    `IDENTITY_TESTS` names `services/identity-service/.../nl/hackyourfuture/project/backend/`, and
    the migration pattern is `services/.+/db/…V*__*.sql`. In the kit it passes without checking
    anything. Change: read the frozen-path patterns from config (contract tests, applied
    migrations); with none set, the job says so instead of passing silently. Why: the rule
    "contract tests and applied migrations stay unedited" is process; the paths are jobmatch's.
    Tests: `test_invariants.py` (8/8) uses `IDENTITY = "services/identity-service"` and would need
    the same config.
    **Part done in Batch 3, the job only:** its compare step runs only
    `if: hashFiles('services/**') != ''`, so with no `services/` the step shows as skipped instead of
    passing after checking nothing. The frozen paths are still jobmatch's, written in
    `invariants.py`; the config part stays open. **Done in Batch 4** as item 57.

13. **`scripts/pr-names.py` lines 34, 37, 39: the Jira key `KAN-`.** Change: take the key prefix
    from config (or any `[A-Z]+-\d+`), with none meaning "no tracker". Tests:
    `test_pr_names.py` (12/12; 21 lines name `KAN`).
    **Done in Batch 4, as an environment variable with jobmatch's default:** `JIRA_KEY`, read like
    the script's other inputs (`PR_BRANCH`, …); unset or empty, it is `KAN`, so jobmatch's behaviour
    is unchanged. Empty counts as unset because an unset CI variable (`${{ vars.JIRA_KEY }}`)
    arrives as `""`. `pr-checks.yml` does not pass it yet: a project that uses another key adds it
    to the "Compare the names" step's `env:`. "No tracker" is not done. `test_pr_names.py`: 15/15,
    with and without `JIRA_KEY` set in the shell.
    - `broken: pr-names' default key is XYZ, not KAN → AssertionError: Lists differ: ['the description names KAN-6, not KAN-5'] != []`
    - `broken: an empty JIRA_KEY is taken as the key → AssertionError: 'KAN' != ''`
    - `broken: pr-names ignores JIRA_KEY → AssertionError: Lists differ: ['the description names ABC-7, not ABC-166'] != []`
    - `broken: pr-names ignores JIRA_KEY, run as a command → AssertionError: 1 != 0 : 0 problems over the branch, the title and 1 commits`
    - `broken: a close title's key prefix stays KAN whatever JIRA_KEY says → AssertionError: Lists differ: ['a Day 43 close comes from day-43/close-t[38 chars]97`'] != []`

## spec-drift.py

14. **`main()` line 1169: crash with no GitHub remote.** `gh repo view` exits 1 ("no git remotes
    found"); `run()` raises `CalledProcessError`, and nothing is written: neither `--out` nor
    `--build` produced a file in a two-commit scratch repository. Change: when `gh repo view`
    fails, warn and carry on with git only (no PRs, no runs, owner None), so a new project gets a
    page from its first commit. Why: Step 4 could not check the page, or whether its output names
    jobmatch, because of this. Tests: no; the tests call functions, not `main()`. Add one.
    - **Done in Batch 5:** `github()` holds `main()`'s three `gh` calls. When `gh repo view` fails
      (`CalledProcessError`) it prints `NO_REMOTE` to stderr with gh's message, and returns no PRs,
      no runs and the note; `main()` appends the note to `meta.caveats`, which the page lists, and
      to its last line. A missing `gh` (`FileNotFoundError`) is not caught. The test calls
      `github()`, not `main()`; the scratch run below is what checked `main()`.
      - `broken: github() lets gh repo view's failure through, as before → FAILED (errors=1)` (the
        error, read from the run: `subprocess.CalledProcessError: Command '('gh', 'repo', 'view', …)' returned non-zero exit status 1.`)
      - `broken: github() gives no note when there is no remote → AssertionError: Tuples differ: ([], [], None) != ([], [], 'No GitHub remote: read from git only, so[43 chars]ty.')`
      - `broken: github() says no remote when there is one → AssertionError: Tuples differ: ([{'n[39 chars] [], 'No GitHub remote: read from git only, so[43 chars]ty.') != ([{'n[39 chars] [], None)`
    - Owner and repo: spec-drift has no hard-coded owner or repo. It uses whatever `gh repo view`
      resolves, so it does not fall back to jobmatch's. The Pages URL appears only in `CLAUDE.md`
      (twice; placeholders in the template).

15. **Line 1063: `infra()` reads `gh run list --workflow infra-ci.yaml`.** It is wrapped in a try
    and returns empty runs when absent, so this is not a crash risk once item 14 is fixed. Change:
    take the workflow name from config, or none. Tests: `sd.infra` used once in
    `test_spec_drift.py`.

16. **jobmatch history tables:**
    - `RENAMED` (lines 69-70, PRs #296 and #298) and `MOVED` (lines 77-82, six directory moves by
      PR number, `backend/…` → `services/…`).
    - The Verify base `max(("backend", ""), …)` (line 926).

    Change: move them to a per-project data file (empty for a new project), and keep jobmatch's
    rows only as test fixtures. Why: they replay jobmatch's directory history; in another
    repository they match nothing, or match a coincidental PR number. Tests: `sd.MOVED` (2) and
    `sd.RENAMED` (3) are used in `test_spec_drift.py`.

17. **Lines 104-110: jobmatch's service map.** `SERVICE` (monolith packages → services), and
    `OWN_PACKAGE`/`IMPORT` on `nl.hackyourfuture.project.backend`, feed the "imports crossing
    services" metric. Change: config, or turn the metric off when unset. Tests: not directly.

18. **Lines 97-103: the day placeholders `PLATFORM`, `CLEANUP`, `CLOSEOUT`.** These are jobmatch's
    three unnumbered days (the platform step, the cleanup day, the close-out day), which
    `run_order()` recognises by words in plan.md's "Day-by-day specs" list. Change: keep the
    mechanism; document the words in `templates/plan.template.md`, or make the list
    configurable. Tests: yes (`sd.PLATFORM`, `sd.CLEANUP`, `sd.CLOSEOUT`, 4 each).

19. **`docs/dashboard/dashboard.js` line 574: `PHASES`, jobmatch's eight phase names.** Change:
    have spec-drift read the `### Phase N — <name>` headings from plan.md into the data, and have
    the page use them. Tests: no (the page has none); test the parsing in `test_spec_drift.py`.

## Process text kept word for word in the CLAUDE template

20. **`templates/CLAUDE.template.md`: jobmatch facts inside the process sections.** These were
    kept word for word as asked:
    - "up to Day 17, 64% …" (One session per step).
    - "Maven, surefire and CI logs" (output rule).
    - The end-of-Phase-7 / `terraform destroy` row of the auditors table.
    - "Haiku 5.5 (Haiku 4.5 up to Day 33)" (The implementer).
    - "Maven only with `clean`" and "never started Maven" (the break bullet; this describes what
      `break.py` does).

    Change: each becomes a placeholder or a general phrase. Item 6's agents go with the Phase 7
    row. Tests: no.
    **Done** in `dashboard/process-text` (item 65), except the break bullet's "Maven", still open there.

## Gaps the templates do not cover

21. **`templates/spec.template.md`: two parts of a full day it lacks.** Day 36 has both:
    - A provenance paragraph under the header ("Split from Day 33 by …").
    - A `## How the checks read the plan` section, saying how its criteria are checked.

    Change: add an optional `## How the checks work` section and a one-line "Origin" hint. Tests:
    no.

## Found while applying

22. **`scripts/break.py` on Python: a stale `.pyc` can stand in for the break.** Found in Batch 2.
    Two breaks of `spec-drift.py` in a row (`**cut**` → `**gone**`, then `after` → `before`) each
    made the file one byte longer, and both were written within the same second. Python's bytecode
    cache checks only the source's size and whole-second mtime, so the second run loaded the first
    break's `.pyc` and reported the first break's failure (`Lists differ: [... 16, 17 ...]`) as the
    second's. With `scripts/__pycache__` deleted, the second break reported its own failure
    (`15 is not None`). A break whose replacement has the find text's length, written in the second
    the source was last compiled, could likewise run the unbroken code. Not fixed here; every break
    in these batches ran with `PYTHONDONTWRITEBYTECODE=1` and `scripts/__pycache__` deleted first.
    Change, if wanted: have `break.py` run the command with `PYTHONDONTWRITEBYTECODE=1` and delete
    the broken file's cached bytecode before and after. Tests: `test_break.py` would need one.

23. **The scratch run (Batch 5): what a new repository's page shows.** A scratch repository made
    from the kit's working tree at Batch 5, with a toy `plan.md` (one phase, "First step", Day 1) and
    one toy spec (`specs/day-01-toy-file.md`, from `templates/spec.template.md`), two commits, no
    remote. `--out` and `--build` each wrote their file, in about a second each; stderr held only the
    `NO_REMOTE` line, with gh's "no git remotes found". Not fixed here:
    - **The branch must be `main`.** The first run, on the `master` that `git init` made, failed in
      `snapshots()`: `git log --first-parent main` exited 128 and nothing was written. After
      `git branch -m master main`, both files were written. `spec-drift.py` names `main` twice
      (lines 395 and 1064).
    - **Names of jobmatch:** 3 in the data, 4 in the page. The data's come from copied jobmatch
      files, not the script: `specs/day-12-jwt-issuance.md` (`jobmatch-identity`, `jobmatch-api`)
      and `docs/dashboard/deployment.json` (its domain). The page adds `PROJECT` (item 2), so the
      eyebrow reads `jobmatch-microservices · Day 01 of 3 · 1 merged PRs`.
    - **jobmatch content without the name:** the kit's example specs, Days 12 and 36, are listed as
      "ready" days; the tokens panel is jobmatch's `token-usage.json`; the deployment and
      conclusion panels are jobmatch's `deployment.json` and `docs/lab-notebook.md`; the roadmap
      labels phases 1, 2 and 7 with `PHASES` (item 19), "Modularise in place", "Gateway + JWT",
      "ECS + Terraform", where the toy plan says "First step"; panel text names jobmatch's four
      services, Days 1-4's contract tests, #310 and AWS.
    - **Commits without a PR:** both are titled `Initial commit: monolith + migration plan` and
      kind `origin` (line 399), and the eyebrow counts `N - 1` snapshots as merged PRs: "1 merged
      PRs" with none.
    - **Empty panels:** with no PRs, "Share of the gap closed by the spec" shows `NaN%`.
    The eyebrow's count, the `NaN%` and the day total are fixed in item 25. Still open, noted from
    the deployed kit page:
    - **A flat gap angle.** The name-gap angle is 70.8° at all 13 merges of the kit's data, first
      to last, so no PR has closed or widened it and the gap share has nothing to divide (it shows
      "–" after item 25).
    - **jobmatch's constants in `dashboard.js`.** `PROJECT` (`jobmatch-microservices`, item 2),
      `PHASES` (jobmatch's eight phase names, item 19) and `STOPS` (`[16, 20, 24, 28, 35]`,
      jobmatch's stopping points) are set in the page, not read from `plan.md`. Done in Batch 2
      (items 46-48).

75. **`scripts/spec-drift.py`: `kit/` read as the project's code.** Found on the kit's published
    page after Batch 1: #7 moved the name-gap angle from 70.8° to 61.81°, its first move (item 23).
    `code_counts()` greps every file but `*.md`, `data`, `screenshots`, `docs/dashboard` and
    `package-lock.json`, so it read `kit/page/jobmatch-data.json`, jobmatch's data, full of
    jobmatch's spec names, as code. `kit/` is the cleanup's tooling; a copy deletes it (item 72).
    **Done in `dashboard/kit-out-of-gap`.** Each place `spec-drift.py` reads the tree:
    - the gap's code side (`code_counts()`): `kit` excluded. On this repository #7's step is now
      0 (70.8° before and after it), was -8.99; coverage and name coverage at #7 and #8 fall back
      to #6's. No other row changes.
    - work kinds (`work_kind()`): `kit/` was `prod`, which feeds "Production code" and the test
      ratio; it is now `tooling`, as `scripts/` is: #7's 152 prod lines are tooling.
    - code churn: kept. It counts `scripts/` and `.github/` too; `kit/` is changed code like them.
    - hand-offs (`git grep` for `Day N`): kept. Only comment lines count; `kit/` has none, nor
      has `scripts/live-checks.py`, which Batch 7 moves to `kit/jobmatch/`.
    - service boundaries, test state, criterion scopes, spec files: kept. They read `.java`,
      `specs/` and `plan.md`, or paths a spec names; none is under `kit/`.
    The comparison stays 53 of 53: jobmatch's data is precomputed. Tests: new
    `test_a_file_under_kit_is_tooling_and_not_code_the_gap_reads`; 82 tests, was 81.
    - `broken: code_counts() greps kit/ as code, as before → AssertionError: 19.35 != 32.25`
    - `broken: work_kind() puts kit/ in prod, as before → AssertionError: {'spec': 0, 'context': 0, 'prod': 1, 'test': 0, 'tooling': 0} != {'spec': 0, 'context': 0, 'prod': 0, 'test': 0, 'tooling': 1}`

## Found on GitHub

24. **`scripts/spec-drift.py`: a planned day with no spec crashed the build.** The first push to
    `main` failed Dashboard's "Build the page": `KeyError: 18` in `next_step()`
    (`by_day[d]["status"]`). The kit's `plan.md` is jobmatch's; its run order lists Days 17-43 and
    only Days 12 and 36 have specs, so a planned day had no `by_day` entry. It reproduced locally,
    with the remote and without; the Batch 5 scratch run used a toy plan whose days all had specs.
    Any new project hits it: plan.md lists days before their specs are written. `settle()` had the
    same lookup for the first unfinished day; in the kit Day 12 comes first, so it did not crash
    there. Tests: no.
    **Done in `dashboard/planned-day-without-spec`:** `settle()` stops at a planned day not in
    `by_day`, as at a placeholder, so no day is active and the page shows "between days".
    `next_step()` counts it unfinished; when it is next, the step reads `Day NN: write its day spec
    (plan.md lists it, specs/ has none)`. Other days unchanged. New test
    `test_a_planned_day_without_a_spec_is_next_to_write`. A planned day skipped for good still
    reads as next until plan.md drops it or marks it **cut**.
    - `broken: next_step() looks up every planned day in by_day, as before → FAILED (errors=1)`
    - `broken: settle() looks up the first unfinished planned day in by_day, as before → FAILED (errors=1)`

25. **`docs/dashboard/dashboard.js`: three counts wrong on a new repository.** The deployed kit page
    read `Day 12 of 2 · 12 merged PRs` and showed `NaN%` for "Share of the gap closed by the spec".
    jobmatch's page computes the same fields right only because its history hid the bug: every row
    on its `main` but the first is a PR merge (431 of 432), its only `origin` row is that first
    one, where the gap loop starts after it, and every day it planned has a spec (42).
    - **Merged PRs were `N - 1`**, every commit after the first. The kit's `main` has 11 direct
      commits (5507876 to 2f24de3) before 2 PR merges. The count is now the rows with a PR, which
      is how `snapshots()` reads a PR (a `Merge pull request #N` subject) and what the page's
      `merged` list already held.
    - **The gap share summed `byKind[origin]`,** a key it does not have: `undefined + 0` is `NaN`.
      `origin` rows (the plan as written, a commit with no PR) are left out, as the kind charts
      leave them out (`["spec", "code", "close", "other"]`). With no gap closed, the share is
      "–", not `0 / 0`: the kit's gap is flat (item 23).
    - **The day total was the days with specs** (`days.length`: 2 in the kit). It is now the days
      in `plan.md`'s run order (`DATA.order`) together with the days that have a spec, so a cut day
      with a spec still counts: 21 in the kit, 42 in jobmatch as before.
    Not changed: `N - 1` "merges" in the gap note, the PR range and the conclusion; the
    "`done` of `days.length` days finished" lines in the today panel and the conclusion; and, on
    the kit's data, `drawLines()` throws in `lineChart()` (`end` is undefined), so the panels
    drawn after it are not, in node as on the page.
    Tests: new `PageTest` in `test_spec_drift.py`, one test per count, each with its own rows. It
    runs `dashboard.js` in node on a stub document and reads the eyebrow and the stat; it needs
    node. 74 tests, was 71.
    **Done in `dashboard/counts-on-a-new-repo`.** On jobmatch's live data the page gives the same
    as before: `between days · 431 merged PRs`, `-52%`, and with Day 35 set as the current day,
    `Day 35 of 42` both before and after.
    - `broken: the eyebrow counts every commit after the first as a merged PR, as before → AssertionError: 'between days · 4 merged PRs' != 'between days · 2 merged PRs'`
    - `broken: byKind adds every row after the first, origin included, as before → AssertionError: '–' != '-100%'`
    - `broken: the day total is the days with specs, as before → AssertionError: '· Day 12 of 6 ·' not found in 'jobmatch-microservices · Day 12 of 3 · 0 merged PRs'`

    **The throw, done in `dashboard/charts-on-short-history`.** `lineChart()` labelled each line's
    end with `pts[pts.length - 1]`, and a series with no point has none: `TypeError: Cannot read
    properties of undefined (reading '0')` at the label. On the kit's data it was "Service
    boundaries" (`moved`): `placed` is `{}` on all 14 rows, since no `.java` file is in a package of
    `SERVICE` (item 17), so the share is null throughout. "Tests per line of code" was next: the
    ratio is null below 1,000 production lines, and the kit has 1. The throw came in `setSel()`, after
    the `lines`, `cover` and `evidence-history` charts, so `moved`, `test-ratio`, `churn`, the
    `placed` line, "What each merge did to the gap" and "Where the corrections landed" were not
    drawn. In jobmatch's 432 rows every series of every chart has a point. "Pull requests per day"
    was drawn before the throw, as bare axes: none of the kit's PRs is on a `day-NN/` branch.
    - `lineChart()` skips a series with no point, as its bands already did.
    - `lineChart()` takes `empty`, the text it shows in the page's empty-state line
      (`<p class="load-error">`, as Tokens, Infrastructure and Deployment do) when no solid line
      has a point. "Service boundaries" and "Tests per line of code" give one.
    - "Pull requests per day" shows such a line when no day has a PR.
    On the kit's data the six panels now read: three drawn (gap per merge, spec and code, the
    corrections) and three empty-state lines (services, the ratio, PRs per day). On jobmatch's live
    data, before and after, all 53 boxes the page writes hold the same HTML and SVG, byte for byte,
    with no error (the page run in node on a DOM that keeps what is drawn, the selection at the
    last merge). `PROJECT` stays open (items 2 and 23).
    Tests: new `PageTest.test_a_short_history_draws_every_panel_or_says_why_not`, rows and days
    shaped like the kit's; 75 tests, was 74.
    - `broken: lineChart draws every series, as before, even one with no point → AssertionError: "Cannot read properties of undefined (reading '0')" is not None`
    - `broken: lineChart draws bare axes when no solid line has a point → AssertionError: '<p class="load-error">No service code yet' not found in '<svg viewBox="0 0 1000 190" …' : moved`
    - `broken: the per-day chart draws bare axes when no day has a PR → AssertionError: '<p class="load-error">No day has a merged pull request yet' not found in '<svg viewBox="0 0 1000 240" …' : perday`

26. **Found with item 25's throw fixed; not changed.**
    - **"Where the corrections landed" labels a commit with no PR `#null`:** its column labels
      write `"#" + r.pr`, not `prLabel(r)`. The kit's direct commits are columns; jobmatch's only
      such row is the first, which the heatmap leaves out.
    - **The `placed` line under "Service boundaries" reads `At #3: ` and stops** when the selected
      merge has no service code; the empty-state line above it says why. No jobmatch row has an
      empty `placed` (0 of 432), so a fix would not change its page. Change, if wanted: write
      nothing when `placed` is empty. Tests: no.
    - **The page tests do not run on a PR that changes only the page.** "Dashboard metric tests"
      (`spec-drift-tests.yml`) runs `test_spec_drift.py`, node included on `ubuntu-latest`, only when
      a PR touches one of the files in its `PATHS`, and `docs/dashboard/dashboard.js` is not one.
      Change, if wanted: add it to `PATHS`. Tests: no.
    - **One failing chart still blanks every panel drawn after it.** Each `draw*()` runs in one
      chain in `boot()` and `setSel()`; isolating each panel would keep a failure to its own box.
      Not done: it is a change of design, and a `try`/`catch` per panel would also hide errors
      unless it shows them.

27. **`.github/workflows/spec-drift-tests.yml`: the page tests now run on a PR that changes only
    the page** (item 26, third bullet). `docs/dashboard/dashboard.js` is added to `PATHS`, written
    as the other entries are: a `$`-anchored alternative with its dots escaped. Checked with the
    job's own `grep -qE`: it matches `docs/dashboard/dashboard.js`, and not `dashboard.css`,
    `index.html` or `xdocs/dashboard/dashboard.js`. No new step: the node page check is `PageTest`
    in `test_spec_drift.py`, which the job already runs on `ubuntu-latest`, where node is
    installed. A PR that changes this workflow runs the tests anyway, so this PR's own run does
    not show the filter works; the first PR after it that changes only `dashboard.js` does.
    **Done in `dashboard/panel-isolation`.**

28. **`docs/dashboard/dashboard.js`: each panel draws on its own** (item 26, fourth bullet). The
    two places the panels are called in order, the end of `boot()` and `setSel()`, call each
    `draw*()` through `panel(id, draw)`. When one throws, `panel()` sends the error to
    `console.error` and writes `This panel failed: <message>` into the panel's first box, in the
    page's empty-state line (`class="load-error"`; a `<caption>` when the box is a table, `tbl`),
    and the panels after it still draw. A panel is one `draw*()`, as the calls already split them:
    a throw in one of `drawLines()`'s seven charts replaces its first box, `lines`. The chart
    functions are not changed.
    On jobmatch's live data, before and after, all 53 boxes hold the same HTML and SVG, byte for
    byte, with no error and nothing logged.
    Tests: `DRAW` gives the page a `console` that records what `console.error` gets, and `drawn()`
    returns it and takes fields that replace the data's; new
    `PageTest.test_a_panel_that_throws_says_so_and_the_panels_after_it_still_draw`, verification
    that is not a list; 76 tests, was 75.
    - `broken: panel() draws without catching, so a throw stops the page, as before → AssertionError: 'V.filter is not a function' is not None`
    **Done in `dashboard/panel-isolation`.**

## Starter cleanup (proposed)

The goal is now a clean starter: copy the folder, fill in the placeholders, start Day 1. This
section is the inventory for it; nothing here is applied. Plan: (1) this inventory, (2) cleanup
batches, (3) a starter check, (4) a pilot on a toy project.

Baseline at `8ba8631`: the 8 suites pass, 133 tests (break 7, infra_summary 8, invariants 8,
pr_names 15, service_wiring 7, token_usage 4, relabel 8, spec_drift 76); the node page check
(`PageTest`, inside `test_spec_drift.py`) 5 of 5.

Kinds: **D** jobmatch's data, **C** a jobmatch value in code, **F** a feature only a jobmatch-like
project uses, **B** a jobmatch fact inside process text. "53 boxes" is the check the last PRs
used: jobmatch's live data, from its Pages page, run through the page in node, every box the
same HTML and SVG byte for byte. Files with no jobmatch markers: the PR template (but see item
68), `specs/_template.md`, `templates/plan.template.md`, `templates/spec.template.md`,
`check-links.py`, `dashboard.css`, `test_token_usage.py`, `test_infra_summary.py`.

Two kit bugs turned up, beyond the cleanup (items 38 and 39): each would break the pilot.

### D: jobmatch's data

29. **D, `plan.md`** (471 lines). Read by `spec-drift.py` (run order, stop, phase of each day, a
    spec-change PR's kind), the plan- and spec-auditor, and the page's roadmap. No test reads it
    (Batch 2). Proposal: move it to `kit/jobmatch/plan.md`; `templates/plan.template.md` becomes
    the root `plan.md` by `git mv`. The same for `templates/CLAUDE.template.md` (item 30).
    `templates/spec.template.md` is byte-identical to `specs/_template.md`: delete it, and
    `templates/` goes. Open: does `spec-drift.py --build` run with no `plan.md`, for the merge
    between the two moves (Batch 7)? Check it in Batch 7a.
30. **D, root `CLAUDE.md`** (jobmatch's, 28 marker lines). Read by every session as instructions:
    the reason this session had to be told to ignore it. Proposal: move to `kit/jobmatch/`, and
    the template takes its place (item 29).
31. **D, `specs/day-12-jwt-issuance.md`, `specs/day-36-ecs-services.md`.** Read by `spec-drift.py`
    as days of this repository: the kit's page lists them as "ready" (item 23). Proposal: move to
    `kit/examples/`, where `spec-drift.py` does not look (it reads `specs/day-*`).
32. **D, `docs/lab-notebook.md`** (1,118 lines). Read by `spec-drift.py`'s `conclusion()` (the
    `**Read … end of Phase N.**` paragraphs and the "What is being measured" table, on the page)
    and the plan-auditor ("Results to date"). Proposal: move to `kit/jobmatch/`; a new
    `docs/lab-notebook.md` of headings only: `## Results to date`, `## What is being measured`
    with an empty two-column table, `## Retrospective`. The headings are what the readers need.
33. **D, `docs/audit-findings.md`.** Read by the fourth `CAVEATS` line (item 43), `plan.md` and
    `specs/README.md`'s map (item 63). Proposal: move to `kit/jobmatch/`.
34. **D, `docs/defects.md`.** SOURCE.md flags it P, but it is jobmatch's list of defects, Days
    1-43 (395 marker lines of 456). Read only by the lab notebook. Proposal: move to
    `kit/jobmatch/`; correct its SOURCE.md flag to J.
35. **D, `docs/dashboard/token-usage.json`.** Read by `spec-drift.py`'s `tokens()` and the Tokens
    panel; `test_spec_drift.py` names its path only as a file the work kinds leave out. Proposal:
    replace with `[]`, which is what `token-usage.py` writes with no transcripts. The starter check
    shows whether the panel's empty state holds.
36. **D, `docs/dashboard/deployment.json`.** `deployment()` returns None when absent, and the panel
    already says "Nothing deployed yet". Proposal: move to `kit/jobmatch/`.
37. **D, `lessons/`** (9 files, the maintainer's jobmatch memory). Read by nothing but README.md.
    Six are process lessons with jobmatch's evidence; `checks-before-push.md` is half Maven.
    Proposal: move to `kit/lessons/`. A new project starts with no lessons; its own memory
    collects them.

### C: jobmatch values in code

38. **C, `spec-drift.py` line 61, `BREAK_LINE_FROM_PR = 310`. A kit bug.** `break_state()` returns
    "not measured" for any PR numbered under 310, so a new project's `broken:` lines are not read
    until its PR #310 (checked: `break_state('broken: x → y', 7)` is `not measured`). The page
    repeats the number: `dashboard.js` lines 479-483 ("Since #310", "before #310 are not
    measured") and `index.html` line 115. Proposal: the cutoff goes in the data
    (`meta.break_line_from_pr`), 0 in the kit (every PR measured), and the page writes the "before
    #N" sentence only when it is above 0. 53 boxes: kept, by giving the live data the field with
    310. Tests: `test_spec_drift.py` uses 310 in its PR fixtures; they get the field set.
    **Done** in `dashboard/starter-bugs`. 310 is when jobmatch's rules began to ask for the line:
    its #310 (`4d81fbd`, "one fixed line for break evidence, in place of three regexes") replaced
    regexes over free text, and PRs before it were never asked. The cutoff stays one marked value,
    `BREAK_LINE_FROM_PR = 0  # PROJECT: …`, written to `meta.break_line_from_pr`, until Batch 3's
    project file takes it; jobmatch keeps its results by setting 310 there. The page writes "Since
    #N" and the "before #N" line only when the field is above 0; `index.html` line 115 no longer
    names #310. The comparison gives jobmatch's data 310 and holds 53 of 53; without the field,
    only `breaks` differs. Tests: the one 310-dependent assertion sets 310 itself; new
    `test_a_new_project_reads_the_break_line_from_its_first_pr` and
    `PageTest.test_the_break_panel_names_the_first_pr_only_when_there_is_one`.
39. **C, `spec-drift.py` lines 543 and 547: a number under 10 is "a phase number". A kit bug.**
    `run_order()` drops every number below 10 from plan.md's "Day-by-day specs" list, so Days 1-9
    can be neither ordered nor stopped at (checked: `1. Phase 0: Days 3, 1, 2. **Stop and
    evaluate.**` gives `[1, 2, 3, …]` and no stop). The pilot's two or three days would hit it.
    Proposal: drop only the number after `Phase`; read every other number as a day. jobmatch's
    plan gives the same order (a test pins it with the Batch 2 fixture plus a Day 1-9 case).
    Data only: 53 boxes kept.
    **Done** in `dashboard/starter-bugs`. It told days from phases by size: every number under 10
    was a phase. Now the number after `Phase`, or a range after `Phases` ("Phases 6–7", which the
    tests' plan has), is dropped before the days are read, in `last` too; every other number is a
    day. jobmatch's phase numbers all follow `Phase`: "Phase 3:", "after Phase 7",
    "end-of-Phase-7". On jobmatch's plan and its 42 specs at the source commit, the old and new
    `run_order()` give the same order and no stop. Tests:
    `test_a_day_under_10_is_a_day_and_only_a_phase_number_is_not` (Days 3, 1, 2 with a stop, then
    4-5) and `test_jobmatchs_plan_runs_in_its_order` (jobmatch's list as it ended).
40. **C, `spec-drift.py` lines 97-103 and 1127-1132: the three unnumbered days** (item 18).
    `PLATFORM`, `CLEANUP`, `CLOSEOUT` are found by the phrases `numbered from`, `numbered after
    the last` and `close-out` in plan.md; `next_step()` then says "numbered from 38 (plan.md,
    Course correction after Phase 2)", "Course correction after Phase 5", "Phase 7 outcome".
    Proposal: keep the mechanism; `next_step()` quotes the plan's own line instead of jobmatch's
    section names; the plan template documents the list's grammar (`Phase N:`, `**cut**`,
    `**Stop and evaluate.**`, `numbered from N`, `numbered after the last`). Data only.
    **Done** in `dashboard/page-words`: the mechanism kept. `unwritten_lines(plan)` finds the item
    each placeholder comes from, as `run_order()` reads it; `next_step()` says `Day NN: write its
    day spec (plan.md: "<the item>")`, NN the `numbered from` number or the day after the last, as
    `unwritten()` gives it. The three constants' comments describe the grammar; the plan
    template's list comment adds `**cut**`, `numbered from N`, `numbered after the last` and
    `close-out`. jobmatch's data is unchanged: its next step is computed once, at its own build.
    - `broken: next_step() names the plan without quoting its item → AssertionError: 'Day [13 chars] day spec (plan.md)' != 'Day [13 chars] day spec (plan.md: "A step the plan adds, numbered from 20.")'`
41. **C, `spec-drift.py` lines 70-83, 927: jobmatch's directory history** (item 16): `RENAMED`
    (#296, #298), `MOVED` (six moves by PR number, `backend/…` → `services/…`), the Verify base
    `max(("backend", ""), …)`. Proposal: one project file, `spec-drift.config.json` at the root,
    empty in the kit (`renamed`, `moved`, `verify_bases`); jobmatch's rows become test fixtures
    under neutral names. Data only. Tests: `sd.MOVED` (2 uses), `sd.RENAMED` (3).
    **Done in Batch 3** (`dashboard/project-file`): `project_config()` reads the file; `renamed` and
    `moved` are lists of `[pr, old, new]`; `verify_bases` lists the bases before the root, which is
    always last (`VERIFY_BASES`, `("",)` when empty); `removal_history()` reads `MOVED` when called,
    not when defined. jobmatch's rows are `PROJECT` in `test_spec_drift.py`, under neutral names
    (`backend` → `core`, the services → `account`, `stock`, `orders`, `pricing`); `RemovalTest`
    reads it. `broken: project_config() reads "move", not the file's "moved" → AssertionError: 0 != 6`
42. **C, `spec-drift.py` lines 106-111, the docstring's lines 24-26: the service map** (item 17):
    `SERVICE`, `OWN_PACKAGE`, `IMPORT` on `nl.hackyourfuture.project.backend`, and `.java` only.
    Proposal: in the item 41 file (`services`: package → service; the package root); with none,
    the "Service boundaries" panel shows its empty state (item 25 already draws one). 53 boxes:
    kept (the live data carries the counts already made).
    **Done in Batch 3:** `services` (package → service) and `package_root` (dotted), two top-level
    fields, the simplest shape; `OWN_PACKAGE` and `IMPORT` are built from the root. `.java` only is
    kept. With none, `placed` and `crossings` are empty, as on this repository before.
    `broken: project_config() drops the file's services → AssertionError: Tuples differ: ({}, {}) != ({'orders': [3, 0], 'stock': [0, 2]}, {'orders>account': 1, 'stock>orders': 1})`
43. **C, `spec-drift.py` lines 126-127: a caveat citing jobmatch's audit** ("0.871 … 0.433 …
    AR-8"). Proposal: keep the first clause, drop the measurement and the reference. Data only.
    **Done** in `dashboard/constants-into-data`: "Name coverage counts test and tooling files as
    code." The test checks that clause, and that no caveat holds a digit or a `.md` file.
    - `broken: the caveat cites the audit, as before → AssertionError: 'Name coverage counts test and tooling files as code.' not found in [...]`
44. **C, `spec-drift.py` lines 328 and 400: two jobmatch habits.** `kind()` counts any
    `day-01/` or `day-02/` branch as code (jobmatch's first days had no track names), and a
    commit with no PR is titled `Initial commit: monolith + migration plan`. Proposal: drop the
    `day-0[12]` clause; use the commit's subject. Data only.
    **Done** in `dashboard/constants-into-data`: a merge is code when its branch or title says
    `track`; a commit with no PR keeps its subject (here: "Copy the workflow from
    jobmatch-microservices at 7cbae28, unchanged"). jobmatch's data is precomputed: 53 boxes kept.
    - `broken: kind() counts any day-01/ or day-02/ branch as code, as before → AssertionError: 'code' != 'other'`
45. **C, `spec-drift.py` lines 395 and 1064: the branch `main`** (item 23). Proposal: keep `main`
    (the CI, branch rules and CLAUDE.md all say it), and fail with one line saying the branch
    must be `main` instead of git's exit 128. README tells the copier `git init -b main`.
    **Done** in `dashboard/constants-into-data`: `snapshots()` checks for `main` first and exits
    with `spec-drift.py reads the branch main, and this repository has none: git branch -m main`.
    Line 1064 is `infra()`'s `gh run list --branch main`, a filter, not a lookup: unchanged.
    - `broken: snapshots() runs git log on a missing main, as before → AssertionError: 'git exited 128' != 'spec-drift.py reads the branch main, and [40 chars]main'`
46. **C, `dashboard.js` line 592, `PROJECT = "jobmatch-microservices"`** (item 2). Proposal:
    `spec-drift.py` writes `meta.project`, the repository name from `gh repo view`, or the
    folder's name with no remote; the page reads it. 53 boxes: kept, the live data given
    `project`.
    **Done** in `dashboard/constants-into-data`: `project_name()` (`gh repo view --json name`, else
    the folder of `git rev-parse --show-toplevel`) into `meta.project`; here `agentic-workflow-kit`.
    - `broken: the page names the project in a constant, as before → AssertionError: False is not true : jobmatch-microservices · between days · 0 merged PRs`
47. **C, `dashboard.js` lines 594-595, `PHASES`** (item 19). Proposal: `spec-drift.py` reads the
    `### Phase N — <name>` headings into `meta.phases`. On jobmatch's own plan the names differ
    from the constant in four phases (1 adds "(no network yet)", 5 "+ events", 6 lacks "(cut)",
    7 is "ECS on Fargate"), so the 53 boxes hold only with the constant's names given to the live
    data; the comparison says so.
    **Decision (maintainer, Batch 0 PR):** accepted: the four names change for jobmatch's data too; the comparison does not fake
    the old names, and the PR lists the boxes that change.
    **Done** in `dashboard/constants-into-data`: `phases()` reads `### Phase N — <name>` (em dash,
    en dash or hyphen) into a list by phase number, `""` for a number with no heading. The page
    escapes each name: the template's `<name>` would otherwise be a tag. The comparison gives
    jobmatch's data its plan's names; only `roadmap` differs (with item 48's stops).
    - `broken: phases() lists the headings in order, not by phase number → AssertionError: Lists differ: ['Lay the ground', 'Build it (later)'] != ['Lay the ground', '', 'Build it (later)']`
48. **C, `dashboard.js` line 596, `STOPS = [16, 20, 24, 28, 35]`.** jobmatch's phase-end tags;
    its plan names one stop (Day 28). Proposal: `meta.stops`, the days plan.md's list marks
    **Stop and evaluate** plus those under its "Stopping points" heading (the template's). 53
    boxes: kept with the five given to the live data. Open: should a stop be what the plan says,
    or every phase's last day, as the constant was?
    **Decision (maintainer, Batch 0 PR):** only what the plan marks. The plan template gets a way to mark them (Batch 2).
    **Done** in `dashboard/constants-into-data`: `stops()` is each list item marked **Stop and
    evaluate**, its last day, a stop since lifted included (`run_order()`'s stop is the one still
    in force). One mark, the list's: the "Stopping points" heading is not read, so the two cannot
    disagree; the template says so under that heading and documents the list under "Day-by-day
    specs". jobmatch: `[28]`. The legend reads "Stop and evaluate", was "Ends a phase".
    - `broken: stops() drops a stop a course correction lifted → AssertionError: Lists differ: [] != [2, 6]`
49. **C, `dashboard.js`: jobmatch text inside boxes.** Line 156 ("the monolith and the plan
    written for it"), 287 ("the Java packages in spec-drift.py's `SERVICE` map"), 310 ("still in
    the monolith"), 479-483 (#310, item 38), 687 ("before the evidence format (#55)"), 846
    ("infra-ci … touches infra/"). Proposal: neutral words, or the value from the data. **This
    cannot keep the 53 boxes byte for byte** where the words change in a box jobmatch's data
    fills (156, 310, 687). Open: allow a stated diff, those boxes only, listed in the PR?
    **Decision (maintainer, Batch 0 PR):** accepted: a diff in those three boxes only, listed in the PR.
    **Done** in `dashboard/page-words`: 156 "the code and the plan written for it"; 287 the
    packages under `services` in `spec-drift.config.json`; 310 "still in place", "in place";
    687 the title without "(#55)"; 846 "No infra summary on main yet: it appears after the infra
    workflow next runs on main." (479-483 were item 38's, Batch 1.) Two comments too (the run
    order's example, the ratio's 1,000 lines). Of the three boxes allowed, one differs on
    jobmatch's data, `evidence`, saved with `--write`; `readout` and `placed` draw jobmatch's last
    merge, which shows neither sentence. Not changed: the `moved` chart's label, "Share of the four
    services' main source lines under services/", is in a box the Decision does not allow; open.
    - `broken: the boxes say a part-moved service is still in the monolith → AssertionError: '<b>b[28 chars]es) · <b>orders</b> 40 lines out, 30 still in the monolith</p>' != '<b>b[28 chars]es) · <b>orders</b> 40 lines out, 30 still in place</p>'`
50. **C, `index.html`: jobmatch prose around the panels.** Lines 79 (four services, the monolith),
    94 (Days 1–4, the 1,000-line start), 115 (#310), 137 (infra-ci, Terraform, AWS, LocalStack,
    Days 32 and 36), 150 (Day 35, C35.16-17), 181 (`backend/`, job-service), 189 (Day 17,
    H28.1, Day 25's E1c, #298), 210 ("saved_jobs leaving jobs/", Maven-free but jobmatch's
    example). Proposal: neutral words. This text is outside the 53 boxes, so they hold; the
    starter check's marker search is what checks it. Open: is the 1,000-line start in line 94 a
    constant in `dashboard.js` too? Check in the batch.
    **Done** in `dashboard/page-words`: the listed lines (115 was item 38's) and three the list
    missed, of the same kind: 52 (Days 38-40 and 17), 170 (`GatewayHarnessIT`, #55, Day 9,
    #310), 201 (three jobmatch names as examples, dropped). The prose names the project file's
    fields (`services`, `infra_workflow`, `verify_bases`, `moved`) where it named jobmatch's
    values. The 1,000-line start is `RATIO_FROM` in `dashboard.js`; the prose keeps the number and
    gives a reason that is not jobmatch's Days 1-4. `PageProseTest` holds the markers it checks.
    - `broken: the deployment panel's prose names Day 35 again → AssertionError: Lists differ: ['Day 35'] != []`
51. **C, `pr-names.py` line 30 and 33-34: `KAN` and `AREAS`.** `JIRA_KEY` defaults to jobmatch's
    `KAN` (item 13); `AREAS` lists jobmatch's areas (`paper`, `trial`, `security`,
    `dependabot`). Proposal: no default key (unset is "no tracker": no key is checked); `AREAS`
    keeps the generic ones (`workflow`, `tooling`, `dashboard`, `docs`, `specs`, `plan`, `ci`),
    and the item 41 file may add more. Tests: `test_pr_names.py` names `KAN` in 45 lines; they
    set `JIRA_KEY=KAN` instead of relying on the default. `pr-checks.yml`'s job title "Branch,
    title, commits and Jira keys agree" stays (a required check's name; item 69).
    **Done in Batch 4** (`dashboard/check-inputs`): `JIRA_KEY` unset or empty, the key's text is
    `(?!)`, which matches nothing, so no key is checked and a `XYZ-97 ` title prefix is text;
    `AREAS` is the seven generic areas plus the project file's `areas` (a list of names, empty in
    the kit), read by pr-names.py's own `project_areas()`: a few lines, where sharing
    `project_config()` would import `spec-drift.py` and numpy into a CI job. The tests set
    `JIRA_KEY=ABC` (the escapes and samples renamed: `ABC-5`, `search-client`, `orders-consumer`);
    new `KeyTest` (unset or empty, set), `AreasTest` and a command test with no key; 16 tests,
    was 15. The docstring's history paragraph (#237, KAN-5, #321) is left for item 61-70's text.
    - `broken: with JIRA_KEY unset, pr-names checks any key → AssertionError: Lists differ: [] != ['the description names ABC-6, not ABC-5']`
    - `broken: project_areas() reads "area", not the file's "areas" → AssertionError: Tuples differ: ('research', 'security') != ()`
52. **C, `token-usage.py` lines 36-38: transcripts found by path.** The folder name is derived
    from the repository's own path, so a copy in another folder finds its own transcripts
    (checked: this folder gives `c--users-hackyourfuture-yusup-agentic-workflow-kit`, and
    `~/.claude/projects` has it in two cases, which the lower-cased compare covers). But the
    match is a prefix (`startswith`), to take in worktree folders: a sibling named with this
    one's name and more, such as `agentic-workflow-kit-pilot`, is counted as this project's too.
    Proposal: match the exact name, or the name followed by `--` (a worktree). The pilot must not
    sit in a folder whose name starts with the kit's until then. Tests: `test_token_usage.py`
    calls `count()`, not `transcripts()`; add one.
    **Decision (maintainer, Batch 0 PR):** fixed in Batch 1, as its third bug.
    **Done** in `dashboard/starter-bugs`: a folder is read when its name is this repository's, or
    that and `--` (a worktree under `.claude/worktrees/`). New `TranscriptsTest`: of the folders
    `<name>`, `<name>--claude-worktrees-a`, `<name>-pilot`, `<name>2` and `other`, only the first
    two are read. Item 73's last bullet (keep the project out of such a folder) is no longer needed.
53. **C, paths and names that locate this repository.** Checked: `spec-drift.py` takes owner and
    repo from `gh repo view`, and every `gh` call follows the remote; `.spec-drift-cache.json` is
    next to the script (`CACHE_FILE`) and ignored by git; the Pages workflow deploys to whatever
    repo it runs in. Written in: the Pages URL in root `CLAUDE.md` (item 30), `docs/workflow.md`
    line 78 (item 66), `lessons/spec-first-workflow.md` (item 37); the memory path
    `~/.claude/projects/*jobmatch-microservices*/memory/` in
    `agentic-engineering-auditor.md` line 35 (item 70). Proposal: each a placeholder, below.
54. **C, the tests' fixtures.** `test_spec_drift.py` (96 marker lines), `test_relabel.py` (13),
    `test_break.py` (4), `test_invariants.py` (10), `test_service_wiring.py` (10),
    `test_pr_names.py` (45) use jobmatch names as sample values (`identity-service`, `KAN-5`,
    `#310`). Proposal: each batch that changes a script makes its test's values neutral; the
    marker search (step 3) reads the tests too, so none is left.

### F: features for a jobmatch-like project

55. **F, the infra panel:** `spec-drift.py`'s `infra()` (`gh run list --workflow infra-ci.yaml`),
    `infra-summary.py` and its test, `dashboard.yml`'s `workflow_run` on "Infra checks", the
    "Infrastructure, as CI last checked it" panel. Already off when absent: `infra()` returns no
    runs, the panel says "No infra-ci summary on main yet". Proposal: keep, off; the workflow's
    file name in the item 41 file (none: `infra()` not called); neutral panel text (item 50).
    Removing it would drop a panel (the 53 boxes fall) and one of the 8 suites.
    **Decision (maintainer, Batch 0 PR):** keep, off when its inputs are absent.
    **The workflow name done in Batch 3:** `infra_workflow` in the project file; `infra(workflow)`
    returns no runs and asks gh nothing when it is empty. The check is inside `infra()`, not around
    its call in `main()`, so a test can see it; the effect is the same. The panel text: Batch 5.
    `broken: infra() asks gh when the project file names no workflow → AssertionError: Tuples differ: ({'ru[22 chars]e}, [('gh', 'run', 'list', '--workflow', '', '[108 chars]l')]) != ({'ru[22 chars]e}, [])`
56. **F, the deployment panel and `scripts/live-checks.py`.** The panel is off without
    `deployment.json` (item 36). `live-checks.py` checks jobmatch's Day 35 criteria (C35.16-17)
    on a host; no workflow runs it, and no test covers it. Proposal: keep the panel, off; move
    `live-checks.py` to `kit/jobmatch/` as an example a project rewrites.
    **Decision (maintainer, Batch 0 PR):** keep the panel, off when its input is absent.
57. **F, `invariants.py` and `pr-checks.yml` job 3** (item 12, part done). The frozen paths are
    jobmatch's (`IDENTITY_TESTS`, `services/.+/db/…V*__*.sql`); the step is skipped with no
    `services/`. Proposal: the frozen patterns in the item 41 file (`frozen`: contract tests,
    applied migrations); none set, the step prints "nothing frozen" and passes, in place of the
    `services/**` condition. Tests: `test_invariants.py` passes the patterns in.
    **Done in Batch 4** (`dashboard/check-inputs`): `frozen` is a list of regular expressions over
    the path, as `PROTECTED` was, so jobmatch's four move over unchanged; empty in the kit.
    `frozen_patterns(base)` reads them with `git show <base>:spec-drift.config.json`, the base's
    copy, so a PR that empties `frozen` and edits a migration still fails; none, it prints
    ``Nothing frozen: spec-drift.config.json sets no `frozen` patterns.`` and exits 0. The step's
    `services/**` condition is gone. The OK and failure lines say "frozen file", not "Day 1-4
    test"; the job's name stays (a required check). The tests' base commit holds jobmatch's
    patterns under neutral names (`account-service`, `com/example/core`, `CoreApplicationTests`);
    new `…test_with_nothing_frozen_it_says_so_and_passes` and
    `…test_the_patterns_are_the_bases_so_a_change_cannot_unfreeze_what_it_edits`; 10 tests, was 8.
    - `broken: with nothing frozen, invariants.py compares anyway → AssertionError: 'Nothing frozen: spec-drift.config.json se[22 chars]s.\n' != 'OK: no frozen file was modified, deleted [64 chars]).\n'`
    - ``broken: invariants.py reads the frozen patterns from the head, not the base → AssertionError: 'modified: services/account-service/src/main/resources/db/migration/V1__init.sql' not found in 'Nothing frozen: spec-drift.config.json sets no `frozen` patterns.\n'``
58. **F, `service-wiring.py` and `pr-checks.yml` job 4** (item 11, done as skip). Compose and
    Prometheus wiring for `services/*`. Proposal: keep, off as it is; its job name stays
    generic enough. Open: remove it from the default `pr-checks.yml` instead?
    **Decision (maintainer, Batch 0 PR):** keep it in `pr-checks.yml`, off when there are no services.
59. **F, `.gitattributes` lines 5-7: `mvnw` line endings.** Harmless without `mvnw`. Proposal:
    drop the three lines; keep `*.sh` LF.
    **Done** in `dashboard/process-text`: the three lines and the blank line before them dropped;
    `*.sh` LF kept. `broken: none → a checkout rule for files the kit does not have; nothing reads it`
60. **F, `break.py` lines 9, 17, 49-54, 75-76: the Maven rules** (`mvnw` as `mvnw.cmd` on Windows; a
    Maven command must `clean`). Inert for other commands. Proposal: keep; they are general
    lessons about stale builds that only fire on Maven.

### B: jobmatch facts inside process text

The process text stays word for word; only the fact becomes `<!-- PROJECT: … -->`. Where a
placeholder cannot carry it without rewording, the item says so.

61. **B, `.claude/agents/spec-auditor.md`.**
    - Lines 21-22: "For Maven: delete `*/target/surefire-reports` first, read the reports rather
      than the exit code, and run `../mvnw -B checkstyle:check` too." → "For
      <!-- PROJECT: the build tool -->: delete <!-- PROJECT: the test report directory --> first,
      read the reports rather than the exit code, and run <!-- PROJECT: the check CI runs that the
      build does not, e.g. a linter --> too."
    - Lines 38-39: "Day 13 left the `Secure` cookie flag to Day 16, which never saw it; the Phase
      0-1 audit found 8 of 19 such hand-offs dropped, half done or breaking early." This is
      evidence, not a fact a project fills in. **A placeholder cannot fix it.** Open: keep it as
      jobmatch's evidence ("In the project this kit came from, …", a rewording), or cut the
      clause.
    **Decision (maintainer, Batch 0 PR):** keep the evidence, prefixed "In jobmatch-microservices,", and change nothing
    else in the sentence.
    - Line 43: `grep -rniE "expires on Day|until Day|TODO day-" services frontend scripts
      --include=*.java --include=*.ts --include=*.py --include=*.yaml` → `… <!-- PROJECT: source
      directories --> <!-- PROJECT: --include for each source extension -->`.
    **Done** in `dashboard/process-text`, as proposed and decided. The prefix follows a colon, so
    it reads "in jobmatch-microservices,", lower case. `broken: none → text only`
62. **B, `.claude/agents/implementer.md`.**
    - Lines 27-30: "Run the tests the brief names, from `services/identity-service/`
      (`../../mvnw -B test -Dtest='...' -Dsurefire.failIfNoSpecifiedTests=false`) or with `-f
      services/api-gateway/pom.xml` for the gateway. Delete `*/target/surefire-reports` first …
      Run `../../mvnw -B checkstyle:check` too: `verify` does not run it, and CI does." → "Run the
      tests the brief names, <!-- PROJECT: from where, and the command that runs named tests -->.
      Delete <!-- PROJECT: the test report directory --> first and read the reports, not the exit
      code. <!-- PROJECT: any check CI runs that the test command does not, and the command -->."
    - Lines 35-36: "anything in `src/test/.../contract/` or the Day 01 harness self-tests, or any
      applied migration (`db/migration` V1–V16, or a module migration already on `main`)" →
      "anything in <!-- PROJECT: the frozen tests' path -->, or <!-- PROJECT: anything applied
      that is never edited, e.g. migrations -->".
    - Line 42: "Put an apostrophe in a Flyway baseline description." → `<!-- PROJECT: a pitfall
      of this project's tools, one line each -->`.
    - Line 53: "; checkstyle: <exit code>" → "; <!-- PROJECT: the extra check -->: <exit code>".
    - `plan-auditor.md` line 35 ("roles and migrations") is a general list: no change.
      `defect-rater.md`: no hit.
    **Done** in `dashboard/process-text`, as proposed; the pitfall placeholder stays a list item.
    `broken: none → text only`
63. **B, `specs/README.md`: jobmatch evidence inside the rules.** Lines 22-24 (Phases 0-1's
    three kinds of checks that checked nothing, Days 02, 08, 09), 29-30 (Day 08's query count),
    37 ("from #310 on", item 38), 41 and 44 (the paper's escapes, D22-017, D23-028), 46-57 (Day
    25's `AccountDeletionIT`, #441, `SavedCountAfterDeletionIT`), 59 ("from Day 21 on"), 72-76
    (the paper's §5.3, `docs/paper/success-criteria.md`, H1–H3), 80 (Days 21–28, 11 of 82), 84-89
    ("from Day 28's spec change on", "Specs before Day 28 keep their form"). **Most cannot be
    fixed by a placeholder:** they are evidence for a rule, and the dates ("from Day 21 on") are
    when jobmatch adopted it; for a new project each rule holds from Day 1, so the date is cut,
    not filled. Proposal: cut the date clauses (a starter has no "before"); for the evidence,
    open (as item 61). The process sentences around them stay word for word. The contract-test
    rule (46-57) also needs `contract/` → `<!-- PROJECT: the frozen tests' path -->`.
    **Decision (maintainer, Batch 0 PR):** the evidence is kept, prefixed "In jobmatch-microservices,", nothing else changed
    (as item 61); the "from Day 21 on" and "from Day 28 on" clauses are cut.
    **Done** in `dashboard/process-text`: nine evidence passages prefixed ("in" mid-sentence), the
    two clauses cut, both `contract/` → the placeholder. Also cut, as date clauses of the same
    kind: "(from #310 on)" (item 38) and "Specs before Day 28 keep their form". Kept: the last
    rule's "Specs written before the `new`/`hold` rule" (a rule for older specs, no jobmatch
    date). Extra: `spec-drift.py`'s comment "IDs, from Day 28's spec change on" → "IDs".
    `broken: none → text and one comment`
64. **B, `specs/README.md` lines 103-134: "Map to plan.md", "Provisional specs", "Stopping
    points".** jobmatch's data, whole. Proposal: each section's heading kept with a one-line
    `<!-- PROJECT: … -->` (the table's header row kept: Days | Phase | Outcome | Status).
    **Done** in `dashboard/process-text`, as proposed. `broken: none → text only`
65. **B, `templates/CLAUDE.template.md`** (item 20, still open), plus:
    - Line 11: "The dashboard, Jira and memory only record the others" → "The dashboard,
      <!-- PROJECT: the tracker, e.g. Jira --> and memory only record the others".
    - Lines 3, 56, 138: "the migration" → "the project" (a reword of one word each).
    - Line 57: "up to Day 17, 64% of the main sessions' context tokens were read after a session
      had passed 300k" is evidence (open, as item 61).
      **Decision (maintainer, Batch 0 PR):** kept, prefixed "In jobmatch-microservices," (as
      item 61).
    - Line 65: "Maven, surefire and CI logs" → "<!-- PROJECT: build and test --> and CI logs".
    - Line 82 and 89-91: "the end of Phase 7, before `terraform destroy`", "while the deployment is
      up, beside the plan-auditor on Phase 7" → "<!-- PROJECT: the end of the last phase, and
      what ends it -->" (item 70).
    - Line 97: "on Haiku 5.5 (Haiku 4.5 up to Day 33)" → "on <!-- PROJECT: the implementer's
      model -->".
    - Lines 114-116: "Maven only with `clean`", "never started Maven" describe what `break.py`
      does (item 60): keep, or "a build only with `clean`". Open.
    **Done** in `dashboard/process-text`, with item 20. Line 3 already held a placeholder, so two
    "the migration" changed. Lines 89-91 read "at `<!-- PROJECT: the end of the last phase, and
    what ends it -->`, beside the plan-auditor on the last phase and on the whole plan" (wording
    chosen here). Lines 114-116 kept, undecided. `broken: none → text only`
66. **B, `docs/workflow.md`.** Line 18 (CI node "tests, checkstyle,") → "tests, <!-- PROJECT:
    checks -->,"; line 70 ("Phase 7 ends, before `terraform destroy`") as item 65; line 78 (the
    jobmatch Pages URL) → `<!-- PROJECT: GitHub Pages URL -->`.
    **Done** in `dashboard/process-text`, with two departures. A comment cannot go in a Mermaid
    label, so line 18 reads "tests, checks,". The URL placeholder sits beside "dashboard", not in
    a link: `check-links.py` read `[dashboard](<!-- … -->)` as a broken link. `broken: none → text only`
67. **B, `docs/agent-workflow.svg` and `.png`.** The drawing says "checkstyle," "verify +
    checkstyle; read reports, not exit codes", "a Day 1–4 contract test needs an edit". **A
    placeholder cannot go in a picture.** Proposal: neutral words in the SVG ("the checks CI
    runs", "a frozen test needs an edit"), and the PNG made again from it. Open: how the PNG was
    made in jobmatch.
    **Decision (maintainer, Batch 0 PR):** find out how the PNG was made (its git log, any source file next to it, the
    docs that mention it). If it cannot be made again, a Mermaid diagram in Markdown replaces it.
    Decided in Batch 6.
    **Done** in `dashboard/process-text`. The PNG was Inkscape's export of the SVG (jobmatch
    4caddd5 added both, "and a PNG render"; its `tEXt` chunk reads `Software: www.inkscape.org`,
    at the SVG's 1400×970). Inkscape and the drawing's font, Architects Daughter, are not on this
    machine, so (maintainer, Batch 6) both files are removed and a Mermaid flowchart takes the
    image's place in `docs/workflow.md`: what the two diagrams there did not draw, the before-push
    break loop and "Stop and ask, do not patch". The SVG's 288 lines put the PR over 400; the
    maintainer chose `Oversized:` over a split. `broken: none → a picture's words; nothing reads them`
68. **B, `.github/pull_request_template.md`, "Contract impact".** "Does this change a mart the
    backend reads, or the shape of an endpoint? … tag the backend reviewer" is jobmatch's (a dbt
    mart). The heading is required by the template check. Proposal: keep the heading and "Say
    "None" if not"; the question → `<!-- PROJECT: what a contract is here, and who reviews a
    change to it -->`.
    **Done** in `dashboard/process-text`: the section's comment is the placeholder and "Say "None"
    if not."; the heading and "None" kept. `broken: none → the template check reads the heading only`
69. **B, `.github/workflows/`: comments and one job name.** `pr-checks.yml` lines 16-17 ("the Day
    1-4 tests"), 27 (KAN-5, KAN-6), 132 (job name "Applied migrations and the Day 1-4 tests stay
    unedited"); `spec-drift-tests.yml` lines 7-8; `dashboard.yml` lines 3-4 ("the migration
    dashboard", "where the migration stands"), 15 and 31 (infra-ci). Proposal: comments to neutral
    words; the job name to "Frozen files stay unedited" (item 57). A job name is what branch
    protection requires, so the README names the new one (item 73).
    **Done** in `dashboard/process-text`, the rename included (maintainer, Batch 6: they swap the
    required check before the merge). Line 27's KAN example is evidence: prefixed "in
    jobmatch-microservices,". Job 5's name, "Branch, title, commits and Jira keys agree", kept.
    New `JobNameTest.test_the_job_that_runs_it_is_named_for_frozen_files` in
    `test_invariants.py`: the job that runs `invariants.py` is named "Frozen files stay unedited".
    `broken: pr-checks.yml job 3 named as in jobmatch → AssertionError: Lists differ: ['Applied migrations and the Day 1-4 tests stay unedited'] != ['Frozen files stay unedited']`
70. **B, the three end-of-phase auditors** (`security-ops-`, `architecture-`,
    `agentic-engineering-auditor.md`). Their frame is jobmatch's ending: "Run once at the end of
    Phase 7, before terraform destroy", "the end of the whole migration", "A monolith migrated to
    microservices", the AWS and Terraform checks, the marked example paths (item 6). Proposal:
    "the end of Phase 7, before terraform destroy" → "<!-- PROJECT: the end of the last phase,
    and what ends it -->"; "the whole migration" → "the whole project"; line 23 of
    agentic-engineering → `<!-- PROJECT: what the project is -->`; line 35's memory path →
    `~/.claude/projects/<this project's folder>/memory/`; the AWS read-only rules kept as
    "on the cloud account, if any". **The security-ops Infrastructure and Application lists
    (lines 27-37, 48-51) are jobmatch's system, not a fact:** open: a placeholder list, or keep
    them as marked examples.
    **Decision (maintainer, Batch 0 PR):** a placeholder list, with jobmatch's list as an example in the comment.
    **Done** in `dashboard/process-text`, as proposed and decided. Wording chosen here: "while the
    deployment, if any, is still up"; "never apply or destroy infrastructure" for Terraform's two
    commands; "Do not touch the cloud account, if any" (architecture). Extras of the same kind,
    each a placeholder with jobmatch's as the example: security-ops' `aws sts` credential and
    `DEPLOY_ENABLED`, and architecture's gate and boundary lists. `broken: none → text only`
71. **B, `README.md`.** Says the kit is jobmatch's copy and points at jobmatch's references.
    Proposal: rewritten in Batch 8 for the person copying it (item 73).

### Batches

One PR each, under 400 changed lines, in this order. Each keeps the 8 suites and the node page
check green, and runs the 53-box comparison; where it cannot hold byte for byte, the item says so.

**Decision (maintainer, Batch 0 PR):** from Batch 1 on, the comparison holds byte for byte,
except the differences the PR names.

0. **The comparison, as a script.** It is run by hand today and not committed. `kit/compare-page.py`:
   fetch the jobmatch page (or read a saved copy), take its embedded data, add the fields later
   batches move into the data (`project`, `phases`, `stops`, `break_line_from_pr`: jobmatch's
   values), draw the page in node with the `DRAW` stub from `test_spec_drift.py`, and print the
   boxes that differ from a saved run. Files: `kit/compare-page.py`.
   **Done** in `tooling/page-comparison`. It reads a saved copy, never the network:
   `kit/page/jobmatch-data.json` (575 KB, one line) is the published page's `window.SPEC_DRIFT`
   value byte for byte, fetched on 2026-10-28; `kit/page/jobmatch-boxes.sha256` (4 KB, 55 lines)
   is the saved run: the error and what went to `console.error`, then each box's HTML as
   `<sha256>  <box>`, one box a line. Not JSON: GitGuardian read four `"token-…": "<hash>"` lines
   as secrets. The live page's own inlined `dashboard.js` draws the same 53 boxes as this
   repository's, with no error and nothing logged. A named difference is accepted by rewriting the
   saved run (`--write`) in the PR that names it; its diff is one line per box. CI runs it as
   `PageTest.test_jobmatchs_data_draws_the_boxes_it_drew` (skipped once `kit/` is gone), so
   `test_spec_drift.py` has 77 tests, was 76; `spec-drift-tests.yml`'s `PATHS` gains `kit/`'s
   script and fixtures. Two things the break showed: (1) hover tooltips are not boxes (`DRAW`'s
   `addEventListener` does nothing), so the comparison cannot see them: a first break, the Tokens
   tooltip's "context per reply", passed with 53 of 53 the same; (2) `break.py` quotes only the
   last line, so the summary line names the boxes that differ.
1. **The three kit bugs** (38, 39, and 52's prefix match: a decision of the Batch 0 PR) and
   item 45's error line. `spec-drift.py`, `dashboard.js`,
   `index.html` line 115, `test_spec_drift.py`.
   **Done** in `dashboard/starter-bugs`, the three bugs (38, 39, 52), plus `token-usage.py` and
   `test_token_usage.py`. Item 45's error line was not in the maintainer's brief for this batch:
   not done, still open.
   1b. **`kit/` out of the gap** (item 75). **Done** in `dashboard/kit-out-of-gap`.
2. **Page constants into the data** (46, 47, 48) and the data-only fixes (43, 44). `spec-drift.py`,
   `dashboard.js`, `test_spec_drift.py`.
   **Done** in `dashboard/constants-into-data`, with item 45, plus `templates/plan.template.md`
   and `kit/compare-page.py`. The comparison's `LATER` now holds what jobmatch's plan gives;
   `roadmap` alone differs, saved with `--write`: Phases 1, 5, 6, 7 renamed, Days 16, 20, 24
   and 35 no longer stops, the legend's "Stop and evaluate". 88 tests, was 82.
3. **The project file** (41, 42, 55's workflow name): `spec-drift.config.json`, `spec-drift.py`,
   `test_spec_drift.py`.
   **Done** in `dashboard/project-file`, with the three `broken:` lines under the items. The kit's
   file sets every field empty. On this repository, `spec-drift.py`'s output before and after
   differs in `now.generated` and `meta.provenance.script_edited` only. 53 of 53 boxes the same.
   92 tests, was 88.
4. **The checks' inputs** (51, 57): `pr-names.py`, `invariants.py`, their tests, `pr-checks.yml`.
   **Done** in `dashboard/check-inputs`, plus `spec-drift.config.json` (`areas`, `frozen`, both
   empty), with the four `broken:` lines under the items. On its own PR, pr-names read no key and
   invariants nothing frozen. 53 of 53 boxes the same. 153 tests, was 150.
5. **The page's words** (40's texts, 49, 50): `dashboard.js`, `index.html`, `spec-drift.py`'s
   `next_step()`. 53 boxes: a stated diff on items 49's boxes, if allowed.
   **Done** in `dashboard/page-words`, plus `templates/plan.template.md` (item 40's grammar), with
   the three `broken:` lines under the items. `evidence` alone differs, saved with `--write`; 53
   of 53 the same after. 156 tests, was 153.
6. **Process text** (61-70, 59): the agents, `specs/README.md`, `docs/workflow.md`, the SVG and
   PNG, the PR template, the workflow comments, `templates/CLAUDE.template.md`, `.gitattributes`.
   Needs the decisions on items 61, 63, 65, 70 first.
   **Done** in `dashboard/process-text`, with item 20 and the `broken:` lines under the items.
   Labelled `Oversized:` (the SVG's removal; the maintainer's choice over a split). 53 of 53
   boxes the same. 157 tests, was 156.
7. **The data out, the templates in,** in two PRs, because `git diff --numstat` counts a moved
   file as 0 lines only when its path is free: (a) `git mv` of items 29-37 and 56's script to
   `kit/jobmatch/`, `kit/examples/`, `kit/lessons/`, plus SOURCE.md and CHANGES.md to `kit/`;
   (b) `git mv` of the templates to `plan.md` and `CLAUDE.md`, the empty notebook and
   `token-usage.json` (item 35), and `templates/` removed.
8. **The starter check and the README** (72, 73).

### 72. The starter check (step 3)

A script, `kit/starter-check.sh`, and a job in `spec-drift-tests.yml` that runs it on every PR:

1. `git archive HEAD | tar -x` into a fresh folder, without `kit/`; `git init -b main`; one commit.
2. No `specs/day-*`; `plan.md` is the template (after Batch 7b it already is).
3. `python scripts/spec-drift.py --build` with no remote: it must write the page, and stderr hold
   only the `NO_REMOTE` line. In Actions, `gh` has no token and no remote, so this is the path a
   new project takes too.
4. The node page check on that page: every panel draws or shows its empty state, nothing goes to
   `console.error`, and no box reads "This panel failed". This needs `PageTest`'s `drawn()` to take
   a page path; small change in Batch 8.
5. A marker search over the copy: `git grep -niE` for `jobmatch`, `hackyourfuture`, `KAN-[0-9]`,
   `identity-service`, `job-service`, `api-gateway`, `mvnw`, `checkstyle`, `surefire`, `flyway`,
   `terraform`, `localstack`, `infra-ci`, `eu-west-1`, `\bECS\b`. It finds nothing. Left out, for
   false hits: `Day \d+` and `#\d+` (the rules' examples and the branch grammar), `migration` (a
   general word), `gateway`, `AWS`, `Java` (`TEST_PATH` names `.java`), `V1`. `Maven` is left out
   while item 60's rules stay in `break.py`; `mvnw` and `checkstyle` are not.

SOURCE.md and CHANGES.md: **move to `kit/`** with the lessons, jobmatch's examples and the two
scripts above. The README tells the person copying to delete `kit/` (one `rm -r kit`); the
marker search leaves it out. Excluding them would lose the record of what changed; keeping
them at the root would put jobmatch's history in every project.

### 73. What the README tells the person copying

- Copy the folder, `rm -r kit`, `git init -b main` (the branch must be `main`, item 45).
- Fill every `<!-- PROJECT: … -->`: `git grep -n "PROJECT:"` lists them (CLAUDE.md, plan.md, the
  agents, `specs/README.md`, the PR template, `docs/workflow.md`), and `spec-drift.config.json`.
- Optional: `JIRA_KEY` as a repository variable, passed in `pr-checks.yml` (item 51).
- GitHub: Pages with source "GitHub Actions"; a public repository, or a paid plan for Pages and
  branch protection on a private one; branch protection on `main` requiring the checks by name
  ("Description uses the template", "Diff stays reviewable", the names check, "Frozen files stay
  unedited", "Dashboard metric tests gate") and a pull request before merge.
- Locally: Python with `numpy`, `node` for the page tests, `gh` logged in.
- Keep the project in a folder whose name does not start another's (item 52), until that is
  fixed.

### 74. What the pilot (step 4) must exercise

Each of these has never run in the kit; the pilot runs each once:

- A day end to end on `day-NN/` branches: the spec-change PR, one track PR, the closing PR.
- The plan-auditor (first day of a phase), the spec-auditor, the implementer on a track, the
  defect-rater on the blind file.
- `relabel.py blind` and `compare`, with at least one tagged `Defect`.
- `token-usage.py` on the pilot's own transcripts, and the Tokens panel filling.
- `break.py` on the pilot's code, its `broken:` line in a track PR, and the page reading it as
  "recorded" (item 38).
- A PR over 400 lines failing "Diff stays reviewable", then passing with `Oversized:`.
- The panels a day fills: "Pull requests per day", the gap angle moving, the `new`/`hold` tags
  and the evidence behind the ticks, a hand-off with an ID picked up by the next day.
- A plan whose order is not by number, with a stop on a day under 10 (item 39).

### Open questions

All decided by the maintainer in the Batch 0 PR, each under its item: 47, 48, 49, 52, 55,
56, 58, 61, 63, 65, 67, 70, and the comparison's rule under Batches.

- Items 61, 63, 65: jobmatch's evidence inside the rules: keep it, marked as jobmatch's, or cut
  it? A placeholder cannot carry it.
- Item 70: the security-ops lists of jobmatch's system: a placeholder list, or marked examples?
- Item 49: may Batch 5 change named boxes on jobmatch's data, with the diff stated?
- Item 47: the comparison gives jobmatch's data the constant's phase names, not what its plan's
  headings say; acceptable?
- Item 48: a stop is what the plan marks, or every phase's last day?
- Item 58: keep `service-wiring.py` off in `pr-checks.yml`, or take it out?
- Item 67: how was `agent-workflow.png` made?
- Items 55, 56: keep the infra and deployment panels (off), as proposed, or remove them, which
  loses the 53-box comparison and one suite?
