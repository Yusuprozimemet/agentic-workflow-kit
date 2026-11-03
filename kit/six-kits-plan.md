# Six spec-driven kits: what to adopt, fix and improve

2026-11-03. A research session (Fable 5.1) compared this kit with Spec Kit, BMAD, GSD Core,
Task Master, spec-superflow and loki-mode, and made ten suggestions. A second session checked
each suggestion's claims against the repository, re-ran the token scripts, and turned the ones
that hold into a plan. What the comparison says about the other six kits was not checked here.

## Where the cost is

Measured on this machine's transcripts on 2026-11-03 with `python scripts/token-usage.py
--simulate` and `--compare`, and a one-off count of each main session's first and largest
reply context (not a kit script; the three lines it printed are the rows marked *).

| Measure | Value |
|---|---|
| Main sessions, 2026-10-27 to 2026-11-03 | 90 sessions, 3,509 replies, $190.38 at list prices |
| Replies per session * | median 29, largest 252 |
| Context of a session's first reply * | median 50,614 tokens; smallest 28,452; p90 52,998 |
| Largest context in a session * | median 92,631; 42 sessions passed 100k, 10 passed 150k, none passed 200k |
| Context per reply before and after the hooks of 2026-11-02 | median 86,996 then 70,091; $0.0604 then $0.0442 per reply; two after-days, so no verdict |
| Fresh session whenever the context passes 100k | 18.9% fewer tokens, +$8.94 (+4.7%) |
| Fresh session at 200k or 300k | nothing: no session got there |
| Every tool result capped at 2k | 16.9% fewer tokens, −$9.28 (−4.9%) |
| Mechanical replies run on Haiku | −$9.97 (−5.2%) |

Three things follow. A reply costs about $0.054 whatever it does, and more than half of what
it reads is the session's start, of which `CLAUDE.md` (20,029 bytes, about 5k tokens) is a
tenth. The three per-reply levers already tried, a forced restart, a cap on tool results and
Haiku routing, are each under the 10% bar and were dropped (PRs #73 to #75). Growth past 300k,
the jobmatch figure `CLAUDE.md` cites, does not happen here: one session per step removed it.
What is left is the number of replies, and that is set by how many steps a change takes. The
one-task comparison ([`comparison/results.md`](comparison/results.md)) shows it: run A's main
sessions took 210 replies over 5 sessions and 8 pull requests, 3 of them kit tooling fixes
since landed in #81 to #83, for a change run B made in one session and one pull request. A cost
9.1 times B at list prices, 9.9 times in tokens without cache reads, 12.9 with. B's reply
count is not in the results file.

So the plan puts the size-of-change ladder first, on one condition: the cheap rungs keep the
gates (seen red, broken on purpose, evidence replay, defect lines, a human merge). Per-reply
hygiene (batched calls, filtered logs, ranged reads) is already in `CLAUDE.md` and gets a
measure here, not more text.

## The claims, checked

| # | Suggestion | Verdict | What the repository shows |
|---|---|---|---|
| 1 | A "not proven" section in the closing PR | True; wrong script named | `criteria()` in `scripts/evidence.py` keeps only ticked criteria; an unticked one produces no check line, and only a spec with none ticked fails ("no ticked criterion"). `scripts/close-evidence.py` only finds the commit and calls `evidence.py`. `evidence.py` reads the spec and git, never a pull request's text, so a "not proven" reason has to sit in the spec under the unticked criterion, not in the closing PR's description. |
| 2 | One triage line per auditor finding | Half true | jobmatch's end-of-phase audit ends every finding as a, b, c or d ([`jobmatch/audit-findings.md`](jobmatch/audit-findings.md)). The spec-auditor's brief ends in one line, "ready / N findings, K must be fixed", with no ending per finding; the plan-auditor's hand-off table has outcomes, its findings do not. |
| 3 | Implementer stop hook; "the test-count invariant covers frozen files only" | Premise false, and the fix as drafted does not work | `scripts/invariants.py` `test_count` counts every test the config's rule names, on every PR, in CI, at the merge base and the head. It reads committed trees (`git ls-tree`, `git show`), and the implementer never commits, so a stop hook calling it would count `main` twice. The kit's own `spec-drift.config.json` has no `test_count` rule. No recorded defect in jobmatch or wordtally shows an implementer dropping a test. |
| 4 | A context warning, not a cap | True, not yet useful here | No hook reads context size. No main session on this machine has passed 200k (largest 196,621); 10 of 90 passed 150k and 42 passed 100k. A warning at 200k would never have fired; one at 100k would fire in nearly half the sessions, and a restart there costs +4.7% (`--simulate` today; PR #74 measured +4.1% on 68 sessions). |
| 5 | An autonomy level in `spec-drift.config.json` | Not worth it | The file's keys are read for `renamed`, `moved`, `verify_bases`, `package_root`, `services`, `infra_workflow`, `areas`, `frozen` and `test_count`; nothing would read an autonomy field, and the end-of-phase auditors already answer the question (jobmatch: "Not shown"). |
| 6 | An explicit entry ladder | Partly stale, and the cost lever | Short specs were judged in kit PR #44 and kept; [`docs/architecture.md`](../docs/architecture.md) draws day spec against short spec; `CLAUDE.md`'s Pitfalls already point to short specs (the first draft of this plan said no pointer existed). Missing: the area-branch rung (`workflow/`, `tooling/`, `dashboard/`, `docs/`, `specs/`, `plan/`, `ci/` and `change/` in `scripts/pr-names.py`, plus the project's `areas`) and a rule for which rung a change takes. Unstated anywhere: a short spec skips the spec-auditor, has no Notes or Defect lines (`specs/_short-template.md`), and is never replayed (`evidence.py` reports "not a day spec"). The comparison task was a day by protocol (one phase, one day); A's product diff was 310 lines, under the 400 limit, so size did not rule a short spec out. |
| 7 | Per-step instructions as skills | Overstated | `CLAUDE.md` is 20,029 bytes, about 5k tokens, in the cached prefix; a session's first reply already reads a median 50,614. Skills would save a tenth of the start at cache-read price and add the risk of a step whose skill was never loaded. |
| 8 | Stable defect IDs | True, but an ID alone does not do it | Criteria (`C28.3`) and hand-offs (`H28.1`) have IDs; `Defect` lines have `found:`, `cause:` and `made:` and no ID. `scripts/spec-drift.py` parses no Defect line (only `scripts/relabel.py` does), so counting recurrence needs a parser before a back-reference. |
| 9 | Repeated auditor runs | True; costed wrong | [`replay/results.md`](replay/results.md): one run per case, strict recall 0.18 (development) and 0.38 (held-out). The 7-case baseline cost 6,004,251 tokens with cache reads (586,430 without) and 38.9 minutes, plus about 3 minutes of judging per case. Two more runs are about 12M tokens and two hours of agent time, not an hour. [CHANGES item 91](CHANGES.md) records that the maintainer could not afford more replay. |
| 10 | Mark criteria machine-proven or judgment | Folds into 1 | `evidence.py` already records each check's kind (`named_test`, `verify`, `break`) and marks a command-checked criterion `not_applicable` with the reason. It lacks the unticked list and a reader-judged kind. |

## Plan

### Adopt now

Each is one area-branch PR, under 400 lines, with its own seen-red test or `broken:` line.
None changes what a reply reads, so none confounds the hooks' re-measure; item 1 changes how
many replies a change takes, which item 3 is there to count.

1. **A size-of-change ladder** (6). A table in `specs/README.md`, before "Short specs":

   | Rung | Branch | Qualifies | Keeps |
   |---|---|---|---|
   | area branch | `<area>/<slug>` | no product behaviour changes: kit tooling, docs, dashboard, CI, plan | the branch and title rules, the diff limit, a seen-red test and a `broken:` line when the PR has a check |
   | short spec | `change/<slug>` | one product behaviour, one PR, no contract test, frozen file or `Replaces:` | `S-<slug>.N` criteria tagged `new` or `hold`, seen red, breaks, the behaviour index; after item 2, the replay |
   | day spec | `day-NN/...` | plan work, and anything the rows above exclude | the auditors, tracks, the close, the blind relabel, the replay |

   The rule: take the lowest rung that qualifies and say which in the PR. `_short-template.md`
   gains a Notes section with the day rules' `Defect` lines, so a short spec records what it
   found (the ladder must not drop that gate). One line in `CLAUDE.md`'s "A day, in order"
   points to the table; the Pitfalls bullet stays. `docs/architecture.md`'s "what kind of
   change" diagram gains the area-branch arm. Docs only: `broken: none`.
2. **Short specs replayed** (6, the condition on 1). `evidence.py` finds the merge of
   `change/<slug>` on `--ref` the way `close_commit` finds a close, reads `S-<slug>.N` criteria,
   and takes breaks from `specs/breaks/<slug>.json`; `close-evidence.py` recognises that merge
   so `evidence.yml` replays it. Seen red: a short spec whose recorded break no longer fails
   must be reported, and today it is "not a day spec". Possibly two PRs at the 400-line limit:
   `evidence.py` first, the workflow second.
3. **Replies per step, measured** (the cost principle). `token-usage.py --compare` splits at
   the constant `HOOKS_DAY`; it takes `--split DATE` so the ladder's landing date can be a
   second split, and each side prints replies per merged pull request (main's merge and squash
   commits in the window, as `spec-drift.py` reads them). Lands before the re-measure, so the
   ladder is judged on reply count and not only on context per reply.
4. **"Not proven" in the replay** (1 and 10). `evidence.py` reports each unticked criterion
   under "Acceptance criteria" as `not proven`, and passes it only when a `Not proven:` line
   with a reason sits under it in the spec at the closing commit. The report names, per
   criterion, what proved it: a test, a command, a break, or a reader (a criterion with none
   of the first three stays failed, as today, unless its `Not proven:` line says why a reader
   judged it). Seen red: an unticked criterion with no line fails. One `tooling/` PR.
5. **One line per auditor finding** (2). jobmatch's four endings, reused: fixed, known limit
   with its reason, maintainer action, rejected with the reason. The spec-change PR lists each
   spec-auditor finding with its ending; a rule in `specs/README.md`, a line in the spec-auditor
   brief's output shape, and a self-check line in the PR template. Counting it on the dashboard
   waits for data.

### Improve, after the token re-measure (about 2026-11-09)

The re-measure judges the hooks of 2026-11-02 alone (`token-usage.py --since 2026-11-02 --tools`,
`--compare`). These wait so that nothing else moves the per-reply numbers in that window.

6. **A context warning** (4). Only if the re-measure shows sessions passing 150k: a PostToolUse
   hook that prints one line when the session's context passes a threshold taken from that
   data, telling the session to finish the step and hand over, not to restart (a restart at
   100k costs +4.7%). Whether the hook input lets a hook read the session's last usage is not
   checked yet. Measure before and after with `--compare --split`.
7. **Defect recurrence** (8). An ID per Defect line (`D28.1`) and an optional
   `same-as: D21.2`; `spec-drift.py` first learns to parse Defect lines, then counts a problem
   that comes back. `relabel.py`'s blind file must strip `same-as:` with the tags, or the
   rater sees the earlier defect's labels.
8. **Three runs per replay** (9). About 12M tokens and two hours of agent time for the 7 cases;
   the mean and the spread per case. The maintainer decides whether to fund it (item 91).

### Dropped

- 3, the implementer stop hook: CI's `invariants.py` already blocks a dropped test, the main
  session reads the diff and re-counts the report, `test_count` cannot see an uncommitted
  tree, and no recorded defect motivates it.
- 5, the autonomy level: nothing would read it.
- 7, skills: a tenth of a session's start, at cache-read price, against a step run without
  its instructions. Revisit only if the re-measure shows the start, not the replies, is the cost.
- The three per-reply levers measured and dropped in PRs #73 to #75: Haiku routing, a forced
  fresh session, a cap on every tool result.
- The comparison's own "not worth adopting" list stands: Spec Kit's constitution and analyze,
  Task Master's task tree, spec-superflow's checkpoints, loki-mode's signed receipts,
  multi-platform support.

## Order of pull requests

1. `specs/size-of-change-ladder` (item 1): docs, now.
2. `tooling/token-usage-split-replies` (item 3): now, before the re-measure.
3. `tooling/evidence-short-specs` (item 2), one or two PRs: now; until it merges, the ladder's
   short-spec row says "not replayed".
4. `tooling/evidence-not-proven` (item 4).
5. `specs/finding-endings` (item 5).
6. After the re-measure: 6 and 7; 8 when the maintainer funds it.

## How the re-measure decides

Cost, from `token-usage.py --compare --split <the ladder's merge date>`: median context per
reply, dollars per reply, and replies per merged pull request. The last is the one the ladder
should move. Quality, from what the dashboard and the replay already count over the same
window: every `new` criterion with a `seen red:` line, every `hold` with a `broken:` line,
`evidence.json` with no failed check, the share of Defect lines found after the merge
(`close`, `dashboard`, `Day NN review`) and the blind rater's agreement. A change is kept when
replies per PR fall and none of the quality counts worsen; a change that lowers context per
reply by shortening sessions, while replies per PR hold, has saved nothing.

## Unverified

- B's reply count in the comparison: not in `comparison/results.md`; the run log is outside
  the repository.
- What makes up the 50k a session starts with, beyond `CLAUDE.md`'s 5k: the system prompt,
  tool definitions and memory index are not counted apart by `token-usage.py`.
- jobmatch's "64% read after 300k" is taken from `CLAUDE.md`, not re-counted here.
- Whether a Claude Code hook can read the session's current context size (item 6).
