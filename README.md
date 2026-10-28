# Agentic workflow kit

The spec-first workflow that migrated jobmatch-microservices, copied out so another project can
use it: the agent briefs (`.claude/agents/`), the spec rules (`specs/README.md`), the pull request
template and CI (`.github/`), the dashboard (`scripts/spec-drift.py`, `docs/dashboard/`), the
tools and their tests (`scripts/`), and the lessons the maintainer kept (`kit/lessons/`).

- [kit/SOURCE.md](kit/SOURCE.md) records where every file came from, at which jobmatch commit, with its
  hash, and how it has changed since the copy.
- [kit/CHANGES.md](kit/CHANGES.md) lists the proposed changes, and marks the ones that are done.
- jobmatch's [CLAUDE.md](kit/jobmatch/CLAUDE.md), [plan.md](kit/jobmatch/plan.md), lab notebook and
  other data are in [kit/jobmatch/](kit/jobmatch/), and two of its day specs (Days 12 and 36) in
  [kit/examples/](kit/examples/), kept as references. They are not instructions for this
  repository.

To start a new project, begin from [templates/](templates/): `CLAUDE.template.md`,
`plan.template.md` and `spec.template.md`, copied to the project's root (the spec into `specs/`).
