# Agentic workflow kit

A spec-first way to change a codebase with coding agents, one day spec at a time, and a dashboard
that measures it. It holds the agent briefs (`.claude/agents/`), the spec rules
(`specs/README.md`), the pull request template and CI (`.github/`), the dashboard
(`scripts/spec-drift.py`, `docs/dashboard/`), and the tools and their tests (`scripts/`).
[CLAUDE.md](CLAUDE.md) gives the working order, [plan.md](plan.md) the goal, and
[docs/workflow.md](docs/workflow.md) draws it.

## Starting a project from it

1. Copy the folder, delete `kit/` (`rm -r kit`), and start the history on `main`:
   `git init -b main`. The dashboard reads the branch `main` by name and stops without it.
2. Fill every `<!-- PROJECT: … -->`: `git grep -n "PROJECT:"` lists them (`CLAUDE.md`, the
   agents, `specs/README.md`, the PR template, `docs/workflow.md`). Fill `plan.md`'s `<name>` and
   `<NN>`, and `spec-drift.config.json`: every field is empty until the project has what it
   names (services, moved paths, an infra workflow, PR areas, frozen files).
3. Write each day's spec from [specs/_template.md](specs/_template.md), as
   `specs/day-NN-<slug>.md`.
4. Optional: a tracker key. With a repository variable `JIRA_KEY`, add
   `JIRA_KEY: ${{ vars.JIRA_KEY }}` to the env of "Compare the names" in
   `.github/workflows/pr-checks.yml`; unset, no key is checked.

On GitHub:

- Pages with source "GitHub Actions": every merge to `main` republishes the dashboard.
- A public repository, or a paid plan for Pages and branch protection on a private one.
- Branch protection on `main`: a pull request before merging, and these checks required by name:
  "Description uses the template", "Diff stays reviewable", "Branch, title, commits and Jira keys
  agree", "Frozen files stay unedited", "Dashboard metric tests gate".

Locally: Python with `numpy`, `node` for the page tests, and `gh`, logged in.

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
