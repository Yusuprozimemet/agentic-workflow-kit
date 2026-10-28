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
    `invariants.py`; the config part stays open.

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
      jobmatch's stopping points) are set in the page, not read from `plan.md`.

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
