**Assessment of the kit against the private-evaluation argument**

30 October 2026. Reviewed through commit `49fcf2d497a7ee8d3a74760399422d85ba85e8e0`.
This is an assessment and proposed next steps, not a change to the workflow rules.

**The work is meaningful, and its direction is sound.** The kit provides a usable foundation
for making agent-assisted engineering checkable. Several choices directly address
the difficult part of the private-evaluation argument: defining good work, establishing that a check
can detect bad work, preserving evidence, and correcting the standard when experience exposes
its gaps. The remaining question is whether the complete workflow delivers enough additional
quality to justify its human effort, time and cost. The repository does not yet settle that.

The assessment is: **strong engineering foundation; promising evaluation practice; incomplete
evidence of comparative effectiveness.** The next substantive milestone should be a small,
frozen replay evaluation set. Integration cleanup should be bounded so it does not displace that work.

The connection to Nadella is specific. His argument is that firms can retain their own standards
of performance and assess different models against them. The kit helps a project express and
retain those standards. It does not itself contain every adopting project's domain benchmark.
The domain knowledge lives in that project's cases, contracts, failure examples and acceptance
decisions. The reusable scripts are the infrastructure around that knowledge.
[Interview transcript, answer beginning at 9:07](https://ceointerviews.ai/interview/3137860/).
The page and passage were checked on 30 October 2026. The marker starts the answer containing
the benchmark remark; it is not the exact timestamp of that sentence. This verifies the
published transcript's attribution, not the original audio independently.

Also distinguish evaluation from model training: this kit supplies feedback to people and
agent workflows. Its tests do not, by themselves, perform reinforcement learning or update a
model's weights. That does not diminish their usefulness.

| What the argument calls for | What the kit provides | Assessment |
|---|---|---|
| A definition of good work | Plan, day specs, stable criterion IDs, `new` and `hold` criteria | Strong foundation; usefulness still depends on choosing the right behavior to check |
| Feedback that can be verified | Deliberate breaks, tests run against earlier code, evidence replay | Substantial implementation; activation and coverage are incomplete |
| Accumulated organizational judgment | Defect records, hand-offs, lessons, approved departures and retrospectives | Valuable, concrete learning retained outside chat history |
| Evaluation of the evaluators | Blind relabeling and a historical spec-auditor replay | Real early evidence; not yet a stable, independently scored benchmark |
| Choosing models by results | Portable specs and Python tools, with agent roles currently configured for Claude | A foundation for comparison; no controlled model-selection result established |
| Evidence of business value | Token accounting and rework records | Human effort and outcome comparisons remain insufficient |

**What the kit handles well**

The strongest design choice is requiring evidence that checks can fail. A green test may be
irrelevant, skipped, or accidentally satisfied. The distinction between `new` behavior failing
on old code and `hold` behavior failing under a deliberate break addresses this directly.
The rules also recognize subtler traps: setup errors are not assertion failures, moving `main`
is a bad reference for a historical comparison, stale reports are misleading, and a longer
timeout can change an API contract. These are operational lessons from actual failures.
See [spec rules](../specs/README.md), [break runner](../scripts/break.py) and
[track verification](../scripts/track-red.py).

The kit goes beyond recording claims. [Evidence replay](../scripts/evidence.py) can check
named-test existence, execute Verify commands and rerun recorded mutations in scratch
worktrees at historical commits. Its report distinguishes failures, execution errors and
inapplicable checks. The dashboard detects changed spec/break inputs and mismatched closing
commits instead of treating every saved report as current. This is a meaningful advance over
the source project's earlier, manually attested `broken:` lines. A named test existing is
still different from its execution or its adequacy, but the tool gives those claims something
concrete to attach to.

The workflow also questions the specification. The plan auditor asks whether the steps deliver the
goal; the spec auditor asks whether the day's premises and checks hold. That is especially
relevant to knowledge work: an agent can execute a mistaken instruction perfectly. The
maintainer's decisions and preserved contract tests provide additional checks outside the
implementer's immediate reasoning. The [auditor brief](../.claude/agents/spec-auditor.md) and
[invariant checker](../scripts/invariants.py) make this division explicit.

The record includes evidence against the project's own hypotheses. The source retrospective admits
that specs were agent-written, that the cause-labeling choices could reverse a hypothesis,
that review effort was under-recorded, and that one service arguably should not have been
extracted. That makes the work more credible. Discovering that a change was unnecessary is
useful engineering evidence even when its implementation passed tests.
See the [source retrospective](jobmatch/lab-notebook.md#retrospective).

Blind relabeling is another good choice. A second reader sees defect descriptions without
their original tags, and disagreements require a recorded decision. The historical record
reports disagreements on 11 of 82 causes and 16 stages. These counts remain in the opening
docstring of [relabel.py](../scripts/relabel.py#L8) and in the
[spec rules](../specs/README.md#L117). That is evidence that measurement
needed correction, rather than a reason to hide disagreement. Its limitation is that the
second reader still receives the first writer's description: omitted defects and misleading
descriptions remain outside this check. See [relabeling](../scripts/relabel.py) and the
[rater brief](../.claude/agents/defect-rater.md).

Reuse has also been tested. The Wordtally pilot exercised five days, reordered work,
stopping points, hand-offs and the new reporting tools; its findings fed back into the kit.
The starter check builds an empty copy without the source-project record. This supports the
claim that the kit is reusable beyond its original migration, although it does not establish
broad adoption or effectiveness across teams. See [change record, items 74–83](CHANGES.md).

**What the evidence does not yet establish**

The repository contains useful case-study evidence, not a controlled demonstration that this
method beats a simpler workflow. The source retrospective reports 475 defect entries: 20 in
the system being migrated and 455 in the agent's own work. These are recorded entries, not
475 independently verified production incidents. More discoveries can mean better detection,
more defects introduced, more detailed recording, or some combination. Raw counts cannot
separate those explanations.

The same retrospective describes changes in models, reviewers, taxonomy and recording rules
during the project. Its earlier and later rework counts use different definitions. It openly
states that there was no comparison arm without specs. Consequently, claims such as “spec
quality matters more than model capability,” “the kit reduces defects by X%,” or “this saves
money” are not established. That is a limit on the conclusion, not a verdict that the work
has no value. [Source retrospective](jobmatch/lab-notebook.md#retrospective).

There is already an embryonic benchmark: the [spec-auditor replay](lessons/spec-auditor-eval.md)
used four history-free, pre-fix snapshots and scored against later fixes. It reports roughly
20/27 recall and identifies cross-day ownership as a weakness. That is much closer to the
private-evaluation idea than counting completed PRs. But the listed results total 19 full
findings plus two partials; the approximate 20 implies partial credit whose rule should be
explicit. “No false alarms in spot-checks” does not establish a precision estimate. Four
retrospectively selected cases, with an auditor informed by accumulated lessons, cannot show
performance on unseen work. Retain these as development cases and add untouched evaluation
cases. The note reports 11–21 minutes and 90–140k tokens per run, so cost also matters.

The gap angle and name coverage are useful diagnostics, but they cannot grade correctness.
An identifier can appear in both spec and code while its behavior is wrong. The code says this
explicitly, and the source retrospective says the angle stayed near 40 degrees over much of
the work. Keep these measurements subordinate to behavior, escapes and review effort.
The [rejected attribution experiment](lessons/attribution-rejected.md) is a good example of
declining to build a metric that added little information.

**Concrete gaps in the current kit**

| Finding | Why it matters | Recommended change |
|---|---|---|
| `evidence.py` is implemented, but the closing instructions do not require its manifest/report workflow and supplied CI does not invoke it on project evidence | A project can follow the advertised sequence and finish with recorded evidence that was never replayed | Document manifest creation and replay explicitly; design an appropriate required verification check |
| `track-red.py` requires a backticked `Test:` field, while the day template shows `Evidence:` but no `Test:` field | An adopter enabling the optional runner is not given a ready-to-use criterion format | Add a compatible example, including track-to-criterion ownership |
| `TRACK_RED_RUNNER` unset passes as “not configured”; frozen patterns start empty; projects must supply their own test workflow | A green set of kit checks is not proof that project behavior was checked | Make setup readiness visible and distinguish active, inactive and inapplicable controls |
| `specs/README.md` says tracks run in parallel; `CLAUDE.md` requires each to start after the previous merge | Two authoritative instructions prescribe different execution orders | Choose and document one rule, consistent with the maintainer's sequential merge practice |
| Closing criteria can be reworded; the current checks do not establish that their meaning stayed unchanged | A result can appear complete after its target was weakened | Review criterion changes against the accepted pre-track spec; route substantive changes through the explicit spec-change process |

These findings come from the [setup instructions](../README.md),
[working order](../CLAUDE.md), [day template](../specs/_template.md),
[PR workflow](../.github/workflows/pr-checks.yml), and the evidence tools themselves.
The starter's empty settings are reasonable template defaults. The issue is knowing when a
copied project has actually activated its controls.

Evidence gating needs one implementation detail thought through: the existing replay command
locates a **merged** closing commit. It cannot simply be made a pre-merge requirement for that
same closing PR. A pre-merge variant would need explicit candidate/base revisions; historical
replay can remain a post-merge check that blocks advancement when it fails. Report freshness
at a historical close also does not prove that the behavior still holds on today's code;
current application CI must cover that separately.

Fresh agent contexts reduce shared conversation bias, but do not guarantee independent
judgment. The historical writer, auditors and rater used the same model family. The hook is
also explicitly documented as a command guard rather than a sandbox. These are correctly
disclosed limitations. Keep the attended workflow; this assessment supplies no evidence for
removing the maintainer from consequential decisions.

**Recommended next steps**

1. **Bound the integration cleanup to one PR and one working session.** Align the template
   with the runner, reconcile track ordering, and document the existing evidence manifest and
   replay sequence. Describe which controls are active or manual. Preserve missing, stale and
   failed evidence as separate states. Defer new gating machinery, dashboard work and broader
   refactoring to named follow-ups if they exceed that scope. The time limit applies to polish;
   it does not justify describing an unresolved check as enforced.

2. **Make the frozen replay set the next substantive deliverable.** Start with roughly 12–20 bounded
   cases as a practical pilot, not a statistically conclusive sample. Include genuine historical
   defects, deliberately broken checks, cross-day ownership problems, and clean cases where the
   correct finding is “no defect.” Keep each starting snapshot, task, expected behavior,
   scoring rubric and severity decision together. Record full and partial credit separately.
   The maintainer verifies the answer key before scoring runs; keep some cases unseen while
   refining the auditor. Separate development cases from held-out cases in the manifest.
   Public historical examples are useful regression cases, but are not private or held-out
   merely because they are called a benchmark. Completion means the snapshots and scoring rules
   are fixed by revision, the development/held-out split is recorded, and one baseline run has
   saved outputs, per-case scores, review time and token use. A manifest and a results table
   are enough to start. This evaluates the auditor's detection ability; it does not by itself
   establish the value of the whole engineering workflow.
   The [replay format and rules](replay/README.md) and 16 cases exist; a reduced baseline of 7
   is in [results](replay/results.md).

3. **Run one small comparison after the baseline exists.** For an initial estimate of the whole
   workflow's value, use three bounded implementation tasks, each attempted with the kit and
   with a simpler baseline: a written task, application tests and normal review. These need
   task-level acceptance checks; an auditor-only replay set cannot substitute for them. Keep
   model version, starting code, permissions, budget and final checks fixed. Use fresh sessions
   and a predetermined assistance rule; record every intervention. Blind scoring where practical,
   and disclose when the maintainer knows the condition. Run each condition once initially;
   treat differences as exploratory because task selection and run variation can dominate such
   a small sample. Repeated trials and independent raters are later upgrades, not prerequisites
   for this first estimate or for completing the replay set.
   Not run: [deferred for token cost](CHANGES.md#91-defer-the-workflow-comparison-and-keep-or-simplify-for-token-cost).

4. **Measure benefit and burden together.** Record behavior acceptance, severe missed defects,
   false alarms, human review minutes, corrective edits, elapsed time, and model/tool cost.
   Separate workflow compliance from product outcomes. Specify the observation window for
   escaped defects and distinguish model-only output from the final human-assisted result.
   Define acceptable tradeoffs before seeing scores: for example, a maintainer-approved
   maximum extra review time for a reduction in serious misses. There is no universal threshold
   this repository can supply on its own.

5. **Keep or simplify components based on the result.** If the full kit prevents important
   misses at an acceptable cost, retain it for comparable work. If it mainly produces additional
   bookkeeping, reduce low-yield audits and ceremony while retaining the checks that catch real
   faults. Once the standard is stable, compare another model against it. That is the point at
   which owning the evaluation starts to provide evidence for model choice.
   Not decided: it waits for the comparison, which is [deferred](CHANGES.md#91-defer-the-workflow-comparison-and-keep-or-simplify-for-token-cost).

For a future knowledge-work application, the transferable part is this discipline. A forecast
needs factual checks, source reconciliation, explicit assumptions, expert judgment about risks,
and eventual outcome review. PR naming and identifier overlap cannot supply those standards.
Choose one such workflow and its domain rubric before claiming general knowledge-work coverage.

**Verification and scope**

The review inspected the current instructions, workflows, core checkers, tests, source retrospective,
auditor-evaluation note and pilot/change records. The initial 12 Python test files were run:
278 tests passed. During the review, the repository advanced through PR #30; its five added
diff-limit tests also passed, bringing the exercised total to **283 tests across 13 files**.
The intervening merge changed that new test file, its CI trigger and the change record; it did
not alter the previously tested Python implementations. The starter check passed all five
steps, and the dashboard comparison matched all 57 saved boxes.

Those runs establish that the kit's tested mechanics work in this local environment. They do
not re-establish historical migration outcomes, live GitHub protection settings, auditor
accuracy, human review effort or financial benefit. Historical figures above are attributed
to the saved project records; the migration and auditor pilot were not rerun.

The strongest justified description of the kit today is: **a tested, reusable workflow that
turns agent-assisted engineering decisions into checkable contracts and retained evidence,
with early evaluation experience and explicitly documented limits.** That is a meaningful
result already. The next question to answer is narrower and measurable: which parts improve
outcomes on unseen tasks enough to earn their cost?
