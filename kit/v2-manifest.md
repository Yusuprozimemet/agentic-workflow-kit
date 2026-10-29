# Kit v2: file manifest

Each file in the kit at `6418ac3` or Wordtally at `82b4ce7`, by content with line endings
normalised. "Base" is `563fc31`, the kit before Wordtally started; for every file changed on both
sides it equals Wordtally's first snapshot `df0c205`, so it is their common base. Treatments:
retain (the kit's), copy (Wordtally's), merge (`git merge-file` kit, base, Wordtally), exclude.
Decisions where behaviour met: [CHANGES.md](CHANGES.md), item 76.

| File | Kit and Wordtally | Treatment | Source | Purpose |
|---|---|---|---|---|
| `.claude/agents/agentic-engineering-auditor.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing (CHANGES 78) |
| `.claude/agents/architecture-auditor.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing (CHANGES 78) |
| `.claude/agents/defect-rater.md` | differ | retain | kit `6418ac3` | kit template; compared in step 4: Wordtally's differences name its project or are wording the kit has since replaced (CHANGES 78) |
| `.claude/agents/implementer.md` | differ | retain | kit `6418ac3` | kit template; compared in step 4: Wordtally's differences name its project or are wording the kit has since replaced (CHANGES 78) |
| `.claude/agents/plan-auditor.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing (CHANGES 78) |
| `.claude/agents/security-ops-auditor.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing (CHANGES 78) |
| `.claude/agents/spec-auditor.md` | differ | retain | kit `6418ac3` | kit template; compared in step 4: Wordtally's differences name its project or are wording the kit has since replaced (CHANGES 78) |
| `.claude/settings.json` | Wordtally only | copy | Wordtally `82b4ce7` | auditor hook wiring; the kit had no settings file |
| `.gitattributes` | differ | retain | kit `6418ac3` | kit convention |
| `.github/pull_request_template.md` | differ | retain | kit `6418ac3` | kit template; compared in step 4: Wordtally's differences name its project or are wording the kit has since replaced (CHANGES 78) |
| `.github/workflows/README.md` | same | retain | kit `6418ac3` | the same on both sides |
| `.github/workflows/dashboard.yml` | same | retain | kit `6418ac3` | the same on both sides |
| `.github/workflows/pr-checks.yml` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | kit config and check names, plus the seen-red job (opt-in: step 3); Wordtally's PR numbers taken out (CHANGES 78) |
| `.github/workflows/spec-drift-tests.yml` | differ | copy + fix | Wordtally `82b4ce7` | Wordtally's suites, then every `scripts/test_*.py`, wider trigger paths, the token test on Windows and the starter in the gate (CHANGES 78) |
| `.github/workflows/tests.yml` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's app tests; each project brings its own |
| `.gitignore` | differ | merge by hand | kit `6418ac3` | kit's lines, plus spec-drift.json and .env |
| `CLAUDE.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing, the auditors' hook and its limits, seen-red.py and a CRLF break pitfall (CHANGES 78) |
| `README.md` | differ | retain + add | kit `6418ac3` | kit template, plus `test_count` and `TRACK_RED_RUNNER` setup (CHANGES 77) and the project's own test workflow (CHANGES 78) |
| `docs/dashboard/dashboard.css` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | Wordtally's new panels with the kit's fixes; reviewed together; a panel's boxes shrink and its list items wrap at phone width (CHANGES 79) |
| `docs/dashboard/dashboard.js` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | Wordtally's new panels with the kit's fixes; reviewed together |
| `docs/dashboard/evidence-checks.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's results; absent until a project writes one (step 3) |
| `docs/dashboard/index.html` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | Wordtally's new panels with the kit's fixes; reviewed together; the relabel panel's day-specific sentence made general (CHANGES 78) |
| `docs/dashboard/token-usage.json` | differ | retain | kit `6418ac3` | starter's empty list |
| `docs/lab-notebook.md` | differ | retain | kit `6418ac3` | starter version; Wordtally's holds its project |
| `docs/spec-drift-improvement.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's improvement plans |
| `docs/workflow-improvement-plan.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's improvement plans |
| `docs/workflow.md` | differ | retain + port | kit `6418ac3` | kit template, plus the post-merge audit timing (CHANGES 78) |
| `experiments/jev/e1/build.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/cases.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/results/floor.jsonl` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/results/jev.jsonl` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/results/opus.jsonl` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/rubric.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/set.sha256` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/e1/test_build.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/run.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/score.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/test_run.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `experiments/jev/test_score.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's experiment and results |
| `plan.md` | differ | retain | kit `6418ac3` | starter version; Wordtally's holds its project |
| `scripts/auditor-guard.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | newer tool; Wordtally's PR number taken out (CHANGES 78) |
| `scripts/break.py` | differ | retain | kit `6418ac3` | the kit's break.py: output assertions, command-not-run refusal, path cleanup |
| `scripts/check-links.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/evidence.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | evidence report; adapted to the kit's break.py (CHANGES 76); Wordtally's day references taken out (CHANGES 78) |
| `scripts/infra-summary.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/invariants.py` | differ | copy | Wordtally `82b4ce7` | newer tool; kit had none or an unchanged copy |
| `scripts/pr-names.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/relabel.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/seen-red.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | newer tool; Wordtally's PR numbers taken out (CHANGES 78) |
| `scripts/service-wiring.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/spec-drift.py` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | both sides' regressions; conflicts resolved to the kit's (CHANGES 76); Wordtally's name taken out of a comment (CHANGES 78) |
| `scripts/test_auditor_guard.py` | Wordtally only | copy | Wordtally `82b4ce7` | newer tool; kit had none or an unchanged copy |
| `scripts/test_break.py` | differ | retain | kit `6418ac3` | the kit's break.py: output assertions, command-not-run refusal, path cleanup; Wordtally's name taken out of comments (CHANGES 78) |
| `scripts/test_evidence.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | evidence report; adapted to the kit's break.py (CHANGES 76); Wordtally's day references taken out (CHANGES 78) |
| `scripts/test_infra_summary.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/test_invariants.py` | differ | copy | Wordtally `82b4ce7` | newer tool; kit had none or an unchanged copy |
| `scripts/test_pr_names.py` | differ | retain | kit `6418ac3` | kit change: JIRA_KEY repository-variable regressions |
| `scripts/test_relabel.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/test_seen_red.py` | Wordtally only | copy | Wordtally `82b4ce7` | newer tool; kit had none or an unchanged copy |
| `scripts/test_service_wiring.py` | same | retain | kit `6418ac3` | the same on both sides |
| `scripts/test_spec_drift.py` | differ | merge | kit `6418ac3` + Wordtally `82b4ce7`, base `563fc31` | both sides' regressions; conflicts resolved to the kit's (CHANGES 76); Wordtally's name taken out of comments and fixtures (CHANGES 78) |
| `scripts/test_token_usage.py` | same | retain + add | kit `6418ac3` | kit tests, Wordtally's long-path test moved in, legacy-row merge test |
| `scripts/test_track_red.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | newer tool, plus the `--runner` tests (CHANGES 77) |
| `scripts/token-usage.py` | differ | copy + fix | Wordtally `82b4ce7` | per-agent tokens; older rows without an agent kept as unknown (CHANGES 76) |
| `scripts/track-red.py` | Wordtally only | copy + fix | Wordtally `82b4ce7` | newer tool; opt-in through `--runner`, CI's `TRACK_RED_RUNNER` (CHANGES 77); Wordtally's PR numbers taken out (CHANGES 78) |
| `spec-drift.config.json` | differ | retain | kit `6418ac3` | starter version; Wordtally's holds its project |
| `specs/README.md` | differ | retain + port | kit `6418ac3` | kit template, plus where seen-red.py does the seen-red run (CHANGES 78) |
| `specs/_template.md` | differ | retain | kit `6418ac3` | kit template; compared in step 4: Wordtally's differences name its project or are wording the kit has since replaced (CHANGES 78) |
| `specs/breaks/day-01.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/breaks/day-02.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/breaks/day-03.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/breaks/day-04.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/breaks/day-05.json` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/day-01-line-word-char-counts.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/day-02-standard-input.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/day-03-top-n.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/day-04-stopwords.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `specs/day-05-json.md` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's day specs and break manifests |
| `tests/__init__.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `tests/contract/__init__.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `tests/contract/test_word_rule.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `tests/test_cli.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `tests/test_token_usage.py` | Wordtally only | exclude (moved) | Wordtally `82b4ce7` | its regression now in scripts/test_token_usage.py |
| `tests/test_word_rule_edges.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `wordtally/__init__.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `wordtally/__main__.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `wordtally/count.py` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `wordtally/stopwords.txt` | Wordtally only | exclude | Wordtally `82b4ce7` | Wordtally's application and its tests |
| `kit/` (25 files) | kit only | retain | kit `6418ac3` | the kit's own records, lessons, examples and checks |
