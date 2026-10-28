# Specs

Spec-driven development. **No code without a spec. No spec without checkable acceptance criteria.**

## Workflow

1. Read the day spec against the code, and run every acceptance check on the code as it is.
   Fix what that turns up in a spec-change PR before any track starts.
2. Branch per track: `day-04/track-b-saved-jobs-tests`.
3. Build only what **In scope** lists.
4. Copy the acceptance criteria into the PR description and tick them.
5. The day is done when every box is ticked and **Verify** passes on `main`.

## Rules

- **The spec is the contract.** Found work outside it? Add a line to that day's *Notes*
  and raise it. Do not widen the PR — CI rejects diffs over 400 lines.
- **Criteria must be checkable by someone who did not write the code.**
  "Auth works" is not a criterion. "`POST /api/auth/login` returns 200 with a
  `Set-Cookie` containing `HttpOnly` and `SameSite=Lax`" is.
- **Every criterion is `new` or `hold`, and every check has been seen to fail.** A check that
  cannot fail proves nothing, and in jobmatch-microservices, Phases 0 and 1 had three kinds of
  them: a CI gate that never ran the integration tests (Day 02), a verify command that ran no
  tests (Day 08), and greps for TODO markers that did not exist, so the criterion ticked itself
  (Days 08 and 09).
  - `new` is behaviour that does not exist yet. The check must fail on today's code, and the
    spec says how ("the grep finds two"). A `new` check that passes before the work is wrong.
    The track PR that adds its test runs it on the code before the day (the code change
    stashed, CLAUDE.md "The implementer") and says what it reported, "FAILED (failures=2)";
    the closing PR copies it into the Evidence as "seen red first on `<sha>`'s code". In
    wordtally, Days 4 and 5 recorded their breaks but not this, and each close had to run it.
  - `hold` must stay true through the change: contract tests passing unedited, a statement
    count. It passes before and after, so passing says nothing. Break the code on purpose once,
    watch the check fail, record what it reported, and revert. In jobmatch-microservices, Day
    08 did this with a per-posting loop: the query-count test failed with 2, 21 and 25
    statements.
  - The proof goes in the PR that first runs the check: the spec-change PR if the check exists
    already, the track's PR if a track adds it (a Track 0). The closing PR links it when it
    ticks the box.
  - The record is one line of its own: `broken: <what was broken> → <what the check reported>`,
    or `broken: none → <why>` in a PR that broke nothing. The PR that ran the break carries it
    in its description; the closing PR copies it under the criterion it ticks. `spec-drift.py`
    reads no other wording as a break. `scripts/break.py` runs one break and
    prints the line.
  - A ticked criterion carries its evidence under it, each piece with the PR it landed in; a
    copied `broken:` line ends with the PR that ran it:

    ```
    - [x] C01.2 **hold** — <the criterion>
      Evidence: `CliTest.test_counts` (#4); `python -m unittest discover -s tests` (#4).
      broken: the total left out → AssertionError: 2 != 3 (#4)
    ```
  - A grep is broken both ways: once with the thing it looks for put back (it must find it),
    once with a near miss it must not match (a longer name, a fully qualified form, a comment).
    In jobmatch-microservices, two of the paper's escapes were greps that matched too much or
    too little (D22-017, D23-028).
  - A check that diffs against a base names a fixed SHA, `main` before the day, never `main`:
    once the track merges, `main` is the change, the diff is empty, and the check ticks itself.
    In wordtally, Days 2 and 3 both wrote `main` first.
  - A check of JSON output compares the parsed object, not the string: on Windows a path in it
    has its backslashes escaped (wordtally, Day 5).
  - A check whose break bites on one system only (a carriage return on Windows) says so, and
    that a local run there guards it, not CI: CI's Linux run passes either way. In wordtally,
    Days 2 and 4 had one each.
  - The closing PR copies breaks; it does not run the first one. A criterion whose only
    `broken:` lines the close itself ran was a check no track had shown can fail: record it as a
    `Defect` (`found: close`). In jobmatch-microservices, four of the paper's six spec escapes
    were these. After the merge,
    the dashboard lists them under "Criteria first broken at the close".
- **A contract test's timing is part of what it expects.** A test in <!-- PROJECT: the frozen
  tests' path --> is frozen in its expected values and in when it expects them. One that asserted
  an effect at once and now waits for it, or waits longer than it did, expects something else,
  even with every value unedited. In jobmatch-microservices, Day 25 did this to
  `AccountDeletionIT`: the saved jobs came to go by the `user.deleted` event,
  the test came to poll apps_db for 10 s, and deletion became eventually consistent through the
  public API, a `savedCount` that counts a deleted user's saves for a few seconds. The edit was
  approved, but read as values only, and no test asserted that count until #441 (paper, §4.1).
  So a new or longer wait, poll bound or timeout in a contract test is a departure: the
  spec-change PR names it before the work, with the bound and what the API shows until it
  passes; the maintainer approves it; and a test outside <!-- PROJECT: the frozen tests' path -->
  pins that public effect within the bound, as, in jobmatch-microservices,
  `SavedCountAfterDeletionIT` does. A wait raised to quiet a flaky test is
  the same change.
- **Tracks inside a day run in parallel. Days run in order.** Day N assumes N-1 is merged.
- **Record every defect in the day's *Notes* when it is found**, one `Defect` line each, with
  three fields:
  - `found:` where, exactly one of `auditor`, `spec-change PR` (before any code); `review`,
    `break on purpose`, `self`, `Track <X>` (before merge); `close`, `dashboard`,
    `Day <NN> review` (after the track merged: an escape).
  - `cause:` exactly one of `spec` (wrong, missing a case, or not meetable as written),
    `implementation` (the spec was right, the code did not do it), `process` (the workflow and
    the record around the code: branch names, Jira keys, a break run wrong, a track announced
    and never opened) or `environment` (tooling, CI, the machine, a library).
  - `made:` the day whose work holds the defect, merged or not (`Day 21`, or `none` for work outside any
    day). When it is not this day, the defect is an escape from that day, whatever `found:` says.

  Two tags are easy to get wrong; in wordtally, Days 1 and 3 got both wrong and Day 2 the
  first, and the blind rater's pass corrected each:
  - A defect caught in the spec-change PR, before any code, is `found: spec-change PR`, even
    when the session that wrote the spec caught it itself: a break run with the wrong `bash`
    and run again before the PR opened. `self` is for the implementer or the main session
    catching its own code before merge.
  - A defect in the implementer's draft, caught by its own test run before it reported, is
    `made: Day NN`, this day, not `none`: the draft is the day's work, merged or not.

  One line per problem: the same kind of problem in two PRs is two lines, a review of seven
  drafts is as many lines as it finds problems, and an auditor's three findings are three lines
  (wordtally, Day 2, wrote them as one). In jobmatch-microservices, the paper had to
  decide all three of these after the data (its §5.3); deciding them on the day is cheaper. A
  track whose code the main session rewrote beyond review fixes gets a `Rewrite` line. In
  jobmatch-microservices, these are the counts `docs/paper/success-criteria.md` judges H1–H3 by; its
  amendment maps `process` and the `found:` values above.

  At the close, a reader who wrote none of it labels them again, blind
  ([`scripts/relabel.py`](../scripts/relabel.py), the `defect-rater` agent): the tagger has also
  written the work, and in jobmatch-microservices, on Days 21–28 a blind rater disagreed with 11 of 82 causes and 16 stages,
  mostly defects made on one day and found on another. The closing PR lists each disagreement
  and decides it: the tag kept, with the reason, or changed in the Notes. A tag is never changed
  without a line in the PR.
- **IDs.** Each criterion starts with its ID, `C28.3` for Day
  28's third, and keeps it when others are added or dropped. Each item a day leaves for later is
  a `Hand-off` line in its Notes with an ID, `H28.1`, and the day or the maintainer it goes to.
  The receiving spec picks it up by citing the ID; naming the day does not. `spec-drift.py`
  lists what no later day picks up, and any track a PR announces ("E1c, next") that no branch
  ever names.
- Changing a spec is normal. Change it in a PR *before* the work, not after.
- Specs written before the `new`/`hold` rule get their criteria tagged in that day's
  spec-change PR, when the spec is read against the code.

## Layout

```
specs/
  README.md        this file
  _template.md     start a new day from this
  day-NN-slug.md   one file per day
```

## Map to plan.md

| Days | Phase | Outcome | Status |
|---|---|---|---|
<!-- PROJECT: one row per phase: its days, its number and name, its outcome, and its status -->

## Provisional specs

<!-- PROJECT: which specs were written from plan.md before their phase, and when each is re-read against the code -->

## Stopping points

<!-- PROJECT: the days that end a phase, and what each leaves standing on its own -->
