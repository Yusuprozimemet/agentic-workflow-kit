# <Project> plan

<!-- plan.md says what and why; the day specs in specs/ say how. It changes rarely, and only in a
plan-change PR. Keep it short. -->

## Verdict: <one line on what is easy and what is hard>

<Two or three sentences: where the project starts, where it ends, and what makes it hard.>

| Hard part | Why | Fix |
|---|---|---|
| **<risk>** | <what in the code today makes it hard> | <the phase that deals with it> |

## Decisions made before the work

- **<decision>:** <what was chosen, and why>. <!-- e.g. a target platform, decided before Phase N -->

## Target structure

```
<the repository or system layout the project ends at>
```

## Phases

Each phase is a series of <400-line PRs, so CI stays green.

### Phase 0 — <name>
**Goal:** <one sentence>.
- <what the phase delivers>
- **Done when:** <a check someone who did not do the work can run>.

### Phase 1 — <name>
**Goal:** <one sentence>.
- <what the phase delivers>
- **Done when:** <check>.

<!-- add phases as needed -->

## Stopping points

- **Day <NN> (<what it finishes>) is a stopping point.** The plan-auditor reads the whole plan
  against the code before anything goes on.

## Constraints

- <a rule every day keeps, e.g. the contract tests are never edited>

## What we are not doing

- **No <thing>.** <why>

## Course corrections

<!-- Added by plan-change PRs, newest first: what a stopping point or audit found, and what the
maintainer chose. Empty at the start. -->

## Day-by-day specs

The phases are broken into day specs in [`specs/`](specs/). Read
[`specs/README.md`](specs/README.md) for the workflow.

<The order the days run in, if it differs from their numbers.>
