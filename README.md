# Agentic workflow kit

A spec-first way to change a codebase with coding agents, one day spec at a time, and a dashboard
that measures it. It holds the agent briefs (`.claude/agents/`), the spec rules
(`specs/README.md`), the pull request template and CI (`.github/`), the dashboard
(`scripts/spec-drift.py`, `docs/dashboard/`), and the tools and their tests (`scripts/`).
[CLAUDE.md](CLAUDE.md) gives the working order, [plan.md](plan.md) the goal, and
[docs/workflow.md](docs/workflow.md) draws it.

## Starting a project from it

1. Copy the kit without its history, from the kit's folder:
   `mkdir ../<project> && git archive HEAD | tar -x -C ../<project>` (copying the folder carries
   the kit's `.git`). There, delete `kit/` (`rm -r kit`) and start the history on `main`:
   `git init -b main`. The dashboard reads the branch `main` by name and stops without it.
2. Fill every `<!-- PROJECT: … -->`: `git grep -n "PROJECT:"` lists them (`CLAUDE.md`, the
   agents, `specs/README.md`, the PR template, `docs/workflow.md`, `scripts/spec-drift.py`). Fill
   `plan.md`'s `<name>` and `<NN>`, and `spec-drift.config.json`: every field is empty until the
   project has what it names (services, moved paths, an infra workflow, PR areas, frozen files).
   `test_count` is absent: added as `{"files": "<path regex>", "test": "<line regex>"}`, "Frozen
   files stay unedited" also fails a PR whose count of matching lines falls (`scripts/invariants.py`).
3. Add a workflow that runs the project's own tests: the kit's CI checks the workflow, not the
   code. Require it with the others below.
4. Write each day's spec from [specs/_template.md](specs/_template.md), as
   `specs/day-NN-<slug>.md`. At a stop (**Stop and evaluate.** in `plan.md`'s list) the next
   step waits until `plan.md` has a `## Course correction after Phase N` section, N the stop
   item's phase.
5. Optional: a tracker key, as a repository variable `JIRA_KEY` (Settings, Secrets and
   variables, Actions, Variables). "Compare the names" in `.github/workflows/pr-checks.yml`
   reads it; unset, no key is checked.
6. Optional, for Python `unittest` tests: a repository variable `TRACK_RED_RUNNER` set to
   `unittest`. "Track tests seen red" then runs each test a track's `new` criteria name, on the
   code before the track and on the track (`scripts/track-red.py`). Unset, it reports "not
   configured" and passes; any other value fails it as a configuration error. It finds tests by
   `unittest` discovery under `tests/`; `scripts/seen-red.py`, which it runs them with, copies only
   the changed files under `tests/` onto the old code, and `scripts/evidence.py` looks a named test
   up as a Python class under `tests/`. Another language keeps the `seen red:` record by hand
   (`specs/README.md`), with `python scripts/seen-red.py -- <its test command>` if its tests live
   under `tests/`.

On GitHub, in this order:

- Before the first push, Pages with source "GitHub Actions": every merge to `main` republishes
  the dashboard, and without Pages the first push's Dashboard run fails at "Publish to Pages"
  (404).
- A public repository, or a paid plan for Pages and branch protection on a private one.
- Before Day 1, branch protection on `main`: a pull request before merging, and these checks
  required by name: "Description uses the template", "Diff stays reviewable", "Branch, title,
  commits and Jira keys agree", "Frozen files stay unedited", "Dashboard metric tests gate", and
  the project's tests. The settings page offers only checks that have already run; the API takes
  any name. Write the rule to a file (a bash heredoc fails in PowerShell):

  ```json
  {"required_status_checks": {"strict": false, "contexts": ["Description uses the template",
    "Diff stays reviewable", "Branch, title, commits and Jira keys agree",
    "Frozen files stay unedited", "Dashboard metric tests gate", "<the project's tests>"]},
   "enforce_admins": false, "required_pull_request_reviews": null, "restrictions": null}
  ```

  and run `gh api -X PUT repos/<owner>/<repo>/branches/main/protection --input <file>`. Then tick
  "Require a pull request before merging" on the settings page: the API ties it to a review rule.
- "Every service is wired into compose and Prometheus" checks nothing until `services/` exists,
  and passes. A project with no services leaves it out of the required checks, or deletes the job.
- The kit has no workflow for the project's own tests: each project adds one (for example
  `.github/workflows/tests.yml`) before Day 1 and requires its check by name, as above. The
  kit's workflows test only its own tools.
- "Track tests seen red" reports on every pull request; with `TRACK_RED_RUNNER` set (item 6
  above), require it by name too.

Locally: Python with `numpy` (and `pyyaml` for `scripts/test_service_wiring.py`), `node` for the
page tests, and `gh`, logged in.

## A session's prompt

One session per step (`CLAUDE.md`). Replies are what a session costs: in the kit's first copy a
step ran about 80 replies at about 75k context each, 97% of it read from cache, so the number of
replies, not their size, is the lever. The prompt carries only the step, the baseline and the
stop. Lessons go in `CLAUDE.md`'s Pitfalls, where every session reads them; notes only a run of
sessions needs (a checklist, open items) go in a memory file the prompt names by path. In that
copy the prompt went from about 130 lines to 35, to the same effect.

```
Day NN track A: <what>, on `day-NN/track-a-<slug>` from fresh main. Under 400 lines.
Notes: <memory file> (read in parts with grep, not whole).
Baseline (check all in ONE shell command, print one line per item; if anything differs, stop):
- main at <sha>, clean tree
- <the test command>: <N> OK
Token rules: batch independent calls in one reply; pre-push checks as one command; test and CI
output filtered to counts and failures; `gh pr checks <n> --watch > <scratch>/checks.txt`, then
print only the final `gh pr checks <n>`. Report each check, then stop. Don't merge: I merge.
When I say "merged" (I'll /compact first): pull main, run the tests, report the counts and the
next step, give the next session's prompt in this shape, and stop.
```

## `kit/`: the record of the copy

The kit was copied from a finished project and cleaned into this starter. `kit/` keeps that record,
for this repository only:

- [kit/SOURCE.md](kit/SOURCE.md): where every file came from, at which commit, with its hash, and
  how it has changed since.
- [kit/CHANGES.md](kit/CHANGES.md): the changes proposed and made, each with its decision.
- The source project's `CLAUDE.md`, `plan.md`, lab notebook and other data, in a folder of
  `kit/` named after it, and two of its day specs in [kit/examples/](kit/examples/), kept as
  references. They are not instructions for this repository. [kit/lessons/](kit/lessons/): the
  lessons its maintainer kept.
- `kit/compare-page.py`: the source project's data drawn by this page, box by box, against a saved run.
- `kit/starter-check.py`: what a copy starts with. It builds HEAD without `kit/` in a fresh
  folder and checks that the dashboard builds and draws with no remote and that no line names the
  source project. CI runs it on every pull request ("The starter names no project").
