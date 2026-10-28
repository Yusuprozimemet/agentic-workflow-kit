# Agentic workflow kit

The spec-first workflow that migrated jobmatch-microservices, copied out so another project can
use it: the agent briefs (`.claude/agents/`), the spec rules (`specs/README.md`), the pull request
template and CI (`.github/`), the dashboard (`scripts/spec-drift.py`, `docs/dashboard/`), the
tools and their tests (`scripts/`), and the lessons the maintainer kept (`lessons/`).

- [SOURCE.md](SOURCE.md) records where every file came from, at which jobmatch commit, with its
  hash, and how it has changed since the copy.
- [CHANGES.md](CHANGES.md) lists the proposed changes, and marks the ones that are done.
- The root [CLAUDE.md](CLAUDE.md), [plan.md](plan.md) and the two day specs in [specs/](specs/)
  (Days 12 and 36) are jobmatch's, kept as references. They are not instructions for this
  repository.

To start a new project, begin from [templates/](templates/): `CLAUDE.template.md`,
`plan.template.md` and `spec.template.md`, copied to the project's root (the spec into `specs/`).
