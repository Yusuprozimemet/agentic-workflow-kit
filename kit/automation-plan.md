# Automation plan: agents work, CI and code owners gate

2026-11-06. A plan, nothing built. Bearing (12 day specs, 84 merged pull requests) is finished,
and optimization closed with [#103](six-kits-plan.md#how-the-re-measure-decides). This file says
how the kit lets an agent run a day's steps unattended, and what stays with the maintainer.

## Goal and cost baseline

The maintainer writes `plan.md`; an agent runs the day specs, tracks and closes in a container;
CI and code owners decide what may merge. The human is needed for `plan.md`, the kit, and the
files only a human may change.

What it costs today, from [Cost baseline for automation](six-kits-plan.md#cost-baseline-for-automation):
**$1.86 per merged pull request**, main sessions only, and **34.4 replies per merged pull
request** (bearing, 84 PRs; $2.39 with subagents). An unattended run is judged against these
two numbers: replies per PR should not rise, and neither should the dollars.

## What bearing's record shows

Counted on bearing at `2862637`, all 84 pull requests merged.

**Defect lines: 156** (`day-01` to `day-12`, the two template lines left out).

| Found by | Lines | | Cause | Lines |
|---|---:|---|---|---:|
| auditor | 98 | | spec | 112 |
| close | 11 | | process | 36 |
| self | 10 | | environment | 6 |
| spec-change PR | 7 | | implementation | 2 |
| Track A, B, C, D | 18 | | | |
| review | 5 | | | |
| break on purpose | 4 | | | |
| dashboard | 3 | | | |

- Of the five `review` lines, two are the maintainer's: D01.23 and D01.24, both "did not stop
  after merged", both process, both now refused by `scripts/step-guard.py`. The other three
  (D02.8, D02.9, D11.12) are the main session reviewing the implementer's drafts.
- So the maintainer's review caught **no code defect** on GitHub. That is a lower bound: a
  catch made in chat and fixed before the PR leaves no Defect line.
- Four defects escaped from an earlier day (`made:` not the spec's own day): D04.1, D07.5,
  D08.8, D12.11.

**`human:` lines: 97 on 65 pull requests** (#20, which added the line, to #84): correction 34,
none yet 30, kit 17, "the maintainer started this step" 9, park 2, and one each of direction,
go, scoping, review and decision. The free-form types are why PR 5 names start, decision,
correction, relay and park.

Re-run, in Git Bash:

```bash
cd ../bearing/specs
grep -h '^- \*\*Defect\*\*' day-*.md | sed -E 's/.*found: ([^·]*) ·.*/\1/' | sort | uniq -c
grep -h '^- \*\*Defect\*\*' day-*.md | sed -E 's/.*cause: ([^·]*) ·.*/\1/' | sort | uniq -c
gh pr list -R Yusuprozimemet/bearing --state all --limit 300 --json number,body > prs.json
python -c "import json,re,collections as c;p=json.load(open('prs.json'));L=[(x['number'],m.group(1)) for x in p for l in (x['body'] or '').splitlines() for m in [re.match(r'\s*[-*]?\s*\x60?human:\s*([a-z]+)',l)] if m and '<type>' not in l];print(len(L),len({n for n,_ in L}),c.Counter(t for _,t in L))"
```

## Prerequisites

1. **The kit's `main` is unprotected today.** `gh api repos/<owner>/agentic-workflow-kit/branches/main/protection`
   returns 404 "Branch not protected", and there is no ruleset. The maintainer turns on branch
   protection by hand, as a settings change, not a PR. Bearing's `main` is protected: eight
   required checks, no required review, admins not enforced.
2. **The agent needs its own non-admin identity**, a machine user or a GitHub App, or
   `enforce_admins` turned on. A pull request's author cannot approve it, so if the agent
   pushes as the maintainer, the maintainer cannot give the code-owner review; and an admin's
   token passes protection that admins are not held to. Decided at the container test; settled
   before PR 7.
3. **PR 6 needs a local `--no-ff` merge** titled "Merge pull request #N from …/day-NN/close-the-day".
   `scripts/evidence.py:91` finds a day's closing commit by that title only, and the merge ref
   GitHub builds for a pull request is titled "Merge <sha> into <sha>".

## The gate: CI and code owners

CI is the gate. An agent opens pull requests; it merges nothing. A pull request merges when
the required checks pass and, where it touches a protected file, a code owner has approved.

CODEOWNERS names the maintainer on the files only a human may change:

- `.github/` (the workflows and the template that are the gate itself)
- `.claude/` (hooks and agent briefs)
- `CLAUDE.md`, `plan.md`, `specs/README.md`, `spec-drift.config.json`
- `CODEOWNERS` itself

The kit has no CODEOWNERS file today. PR 7 adds it; after it merges, the maintainer turns on
required code-owner review. Until then nothing in the repository stops an agent's pull request
from editing these files.

## When a gate may run without a human

A gate (a check, an auditor, a review step) becomes **eligible** for autonomy when it catches
injected defects of each kind it is meant to stop:

- **code**: a break on purpose, replayed from the day's break manifest (`specs/breaks/`);
- **spec**: a criterion loosened, a check that cannot fail, a claim the code contradicts;
- **record**: a `broken:` line with no manifest entry, Evidence that cites no PR, a missing
  Defect line.

Injection only makes a gate eligible: injected defects are easier than real ones. What
**measures** it afterwards is defects that escape past a merge: a Defect line whose `made:` is
an earlier day, or one found at `close` or by the `dashboard`. One escape in a gate's class
returns that gate to the maintainer. Agreement with the maintainer is not a measure: on
bearing the review left no rejection on GitHub to agree with.

## Evidence replay before the merge

Today `.github/workflows/evidence.yml` runs on `push` to `main` and `workflow_dispatch` only,
after the merge it checks. PR 6 adds a run on plain `pull_request`: read-only `contents`, no
secrets, the PR's own code on a throw-away merge (prerequisite 3). Never `pull_request_target`:
it runs with the base repository's token and secrets, and running the PR's code there is the
known way to steal them. No workflow in the kit uses it today.

## The container (decided 2026-11-06)

A container replaces bubblewrap, not wraps it: the same image on Docker Desktop and on a
GitHub Ubuntu runner.

- **Egress allowlist:** the Anthropic API and GitHub; nothing else leaves.
- **Mounts:** a fresh clone only. No home folder, no `gh` login, no Claude credentials from the
  host.
- **Token:** pushes branches and opens pull requests; no `workflows` permission, so a push
  that touches `.github/workflows/` is refused.
- **No `--bare`:** in Claude Code 2.1.170 it skips hooks and CLAUDE.md, and the kit's four
  hooks (`auditor-guard`, `read-guard`, `step-guard`, `cap-output`, wired in
  `.claude/settings.json`) are part of the workflow. A mode, if any, is set with
  `--permission-mode`.

The container limits damage to the machine only. What may merge is still decided by branch
protection and CODEOWNERS.

## Remaining order

1. **Container test** on a scratch repository: a report, no kit PR. It answers: do the four
   hooks act headless without `--bare` (each passes silently when `CLAUDE_PROJECT_DIR` is
   unset, so exiting 0 proves nothing); is egress outside the allowlist blocked; is a push to
   `.github/workflows/` refused; how does the agent authenticate; which identity (prerequisite 2).
2. **PR 4** `tooling/agent-container`: the image and how to run it.
3. **PR 5** `tooling/human-lines`: the `human:` line in the kit's template and CLAUDE.md, with
   the types start, decision, correction, relay, park.
4. **PR 6** `tooling/evidence-on-pr`: replay on `pull_request`.
5. **PR 7** `tooling/codeowners`: the file. After it merges, the maintainer turns on required
   code-owner review.
6. **PR 8** `tooling/injection-harness`: injects code, spec and record defects and counts what
   each gate caught.

## What stays with the maintainer

- Merging, and whether auto-merge is ever turned on (off on the kit and on bearing today).
- `plan.md`, every kit change, and loosening a spec.
- The CODEOWNERS paths, branch protection, and the agent's identity and token.
- Promoting a gate after injection, and taking it back after an escape.
- Every run the agent parks: a doubt stops the run and goes into a report for the maintainer.

## Unverified

- Whether the hooks fire in the container without `--bare`, and how it authenticates there.
- Whether the egress allowlist holds and the `workflows` refusal works as GitHub documents.
- Whether a pull request's throw-away merge replays a close the same way the merge on `main`
  does.
