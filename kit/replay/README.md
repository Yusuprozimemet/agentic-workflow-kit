# Frozen replay set

This evaluates the spec-auditor's detection ability on frozen snapshots. It does not by
itself measure the value of the whole workflow. The format, the rules and 16 cases exist; a reduced baseline of 7 is in [results](results.md).

## Cases and keys

Kinds: `historical-defect`, `broken-check` (a check that cannot fail), `cross-day`
(ownership or hand-off across days), and `clean` ("no defect" is correct).
Development cases may be read, re-run and used to refine the auditor's brief. Held-out cases
run only against a fixed auditor revision. Any subsequent change to
`.claude/agents/spec-auditor.md` makes that held-out result stale for the new revision.
Both repositories are public: development keys are committed; held-out keys stay outside
the repository, pinned by sha256 of their exact file bytes. Do not publish private keys in runs.

Each manifest case has `id` (letters, digits, underscores or hyphens), `kind`, `split`
(`development` or `held-out`), `source: {repo, commit}` (jobmatch-microservices, 40 hex),
`spec` (day spec path inside snapshot), `task`, `origin` (fix PR, defects entry, or clean rationale),
`key`, and `verified` (null or `{by, date}` with an ISO date).
Export the pinned commit history-free with `git archive` into a short path such as C:/ae;
the [earlier replay](../lessons/spec-auditor-eval.md) hit Windows MAX_PATH. Run sequentially.

Development `key` is a manifest-relative path under `keys/` (thus `kit/replay/keys/`).
Held-out `key` is only `{"sha256": "<64 hex>"}`; scoring reads DIR/CASE-ID.json from `--keys DIR`.
A key is a JSON list of findings with unique `id`, `statement`, `severity`, `full` (what earns
full credit), and `partial` (what earns partial credit, or null for none). All text is nonempty.
Blocking: prevents safe or correct progress on the day's work.
Major: a substantive defect requiring correction, without blocking progress.
Minor: a smaller correctness defect with limited impact.
Clean keys are empty; other keys contain findings. The maintainer verifies every key before
scoring, recording who and when in the manifest. Unverified cases cannot be scored.
After a key edit, verify it again before the next run (and update its fingerprint if held-out).
Never change a key during a run.

## Runs and scoring

Run `python kit/replay/replay-set.py check` (optional `--manifest PATH`). It validates
development keys and held-out fingerprints, reports problems, split/kind counts and unverified IDs.
Run `python kit/replay/replay-set.py score RUN.json --keys PRIVATE_DIR` to tally human judgments.
Both commands exit 1 on invalid input; check accepts the empty manifest.
Run JSON has this shape (all case metrics are nonnegative; paths refer to saved auditor output):

```json
{"kit_commit":"<40 hex>","auditor_sha256":"<64 hex>","model":"model revision",
 "cases":{"CASE-ID":{"output":"saved/output.txt","minutes":12,"tokens":100000,
 "review_minutes":4,"findings":{"F1":"full","F2":"partial","F3":"missed"},
 "extras":[{"judgment":"valid-outside-key","severity":"major","evidence":"output.txt:12; code:34"}]}}}
```

The scorer reads the saved output and judges every key finding as `full`, `partial` or `missed`.
Every extra auditor finding is judged `false-alarm`, `valid-outside-key` or `duplicate`, with
severity and cited evidence. Cases may be scored as a subset; every selected key must be fully judged.
Matching is a person's judgment; this script only tallies it. Record auditor minutes/tokens
separately from the scorer's review minutes. The kit commit and auditor brief sha256 fix the run version;
the scorer records these, but does not establish the saved output's provenance or enforce run secrecy.

Report full, partial and missed separately, never as one weighted number.
Strict recall = full / expected; lenient recall = (full + partial) / expected.
Missed blocking findings have their own line. False alarms are counted, including every
blocking or major false alarm on a clean case (minor false alarms count too).
Precision = matched / (matched + false alarms), where matched = full + partial.
Zero denominators print "n/a". Totals sum counts before computing ratios.
Valid findings outside the key are reported without raising recall or counting as false alarms;
propose them for a verified key edit before the next run. Duplicates do not affect scores.

Runs so far, and how far each one goes, are in [results.md](results.md).
