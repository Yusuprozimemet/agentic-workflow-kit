---
name: checks-before-push
description: "jobmatch-microservices before push: verify does not run checkstyle; run from backend/, not target/; read reports; stopped Maven JVMs linger on Windows; gateway changes need the gateway harness run; spec/plan changes need test_spec_drift.py run"
metadata:
  node_type: memory
  type: project
  originSessionId: 44a3ae46-4d2d-4c5f-a102-b4c1cc186e65
  modified: 2026-09-29T19:44:15.100Z
---

Before pushing backend changes, run both `./mvnw verify` and `./mvnw -B checkstyle:check` from `backend/`. CI (`backend-ci-cd.yaml`) runs checkstyle as a separate step, and `verify` does not, so a green test suite says nothing about checkstyle (Day 08: a `HiddenField` violation passed 206 tests).

**Why:** A checkstyle failure only appears in CI otherwise. Separately, on Windows `mvnw clean` fails with "being used by another process" if the shell's working directory is inside `app/target/`, or if the VS Code Java language server holds it. Then delete `app/target/surefire-reports/*` and run without `clean` instead of killing the IDE process.

**How to apply:** Check surefire reports, not just the exit code. Never pipe `checkstyle:check` (or `verify`) into `tail`/`grep` and then print `$?`: that is the pipe's exit code, and on Day 13 Track A (#87) it printed 0 over a real LineLength violation. Redirect to a file or `/dev/null` and print `$?` directly. A stale report from an earlier run can look like a pass (see [[spec-first-workflow]]).

**Stopping a background Maven run does not stop its JVMs on Windows.** Day 15 Track D (#100): after TaskStop, the Maven and surefire `java.exe` kept running and wrote into the same `surefire-reports` while the next run started, so a "203 passed" came from two processes. After stopping a run, list `java.exe` (PowerShell `Get-CimInstance Win32_Process -Filter "Name='java.exe'"`), kill the run's own ones (not the IDE's language server, started days earlier), delete the reports, and rerun.

**Undo a break from a copy, never with `git checkout -- <file>`.** Before a commit that restores `main`'s version and throws away the track's own change to that file. Day 40 Track A (#144): it dropped the new property and then the whole route change, and the next break ran on the wrong code. Copy the file aside before breaking it, restore from the copy, and diff against the copy to confirm.

**Write break patches as files, and dry-run them before trusting a green.** Day 19 (#158–#160): three times a break's inline Python, passed through a bash heredoc or `sed`, had its `\n` turned into a real newline; once the break silently did not apply and the suite ran green on unbroken code, which reads exactly like "the test does not notice". Write the patcher with the Write tool (normalise CRLF to LF on read, since `core.autocrlf` checks files out with CRLF), apply every patch once and `git diff --stat` it, revert, then run the breaks.

**A whole suite red at once is the environment until shown otherwise.** Day 40's closing run: 320 errors direct and 206 through the gateway were Docker Desktop stopped ("Could not find a valid Docker environment"). Read the first error before counting failures; `docker info` first. Before a compose check, stop on any running container rather than printing the count and going on: they may be a finishing test run's, or the maintainer's.

**`TraceContinuedIT` failing on "remaining connection slots are reserved" is the harness Postgres at its connection limit, not the track.** Day 21 B1 (#215, #216), 2026-09-29: 3 of 5 local full `clean verify` runs failed 1 in 429 on it (77th of 79 classes, most cached contexts), on branches that touched nothing under `backend/`; reruns passed. Confirm it is that test and that error, then rerun. Say so in the PR. Raising `max_connections` or capping cached contexts is unowned and waits on the maintainer.

**A gateway change needs the gateway harness run locally too.** CI's backend job also runs `contract/*IT` through a gateway container built from `services/api-gateway`. Day 38 Track C (#123) was checked only with the gateway's own build; `main` went red on a startup race (fixed in #124). Before pushing any `services/api-gateway` change: `docker build -t jobmatch-api-gateway:harness services/api-gateway`, then from `backend/`: the `-Dtest` list in `.github/workflows/identity-service-ci-cd.yaml` ("Run the suite through the gateway"), from `services/identity-service/` with `../../mvnw` (no `-pl` since F2); it must reach the 229 floor. A PR run passing is not proof: that race passed on the PR and failed on `main`.

**A spec or plan change can break the dashboard tests without CI noticing.** `spec-drift-tests.yml` runs only on changes to `scripts/`, but `test_the_repositorys_plan_parses` reads the real `plan.md`. The Day 21 spec change (01876e0) added Day 41 to the run order and left `main` red there until #207 (2026-09-29) touched a script. Run `python scripts/test_spec_drift.py` before pushing any spec-change or plan-change PR.

- **Service modules (services/*) run only `*Test` classes under surefire**; a `*IT` there never runs, and no report appears. The implementer named one `*IT` on Day 21 E3 and reported it passing. Put the suffix in every brief, and confirm each new test has a surefire report.

**No literal passwords in test code (GitGuardian, Day 20 #188, Day 25 #282):** Testcontainers admin = container default, role passwords random per run (`UUID.randomUUID()`). GitGuardian scans every commit in the PR, so a fix commit does not clear it; clearing needs a squash + force-push of the PR branch (maintainer chose that on #282) or a dashboard resolve. grep the diff for `withPassword\|PASSWORD '` before pushing.

**Stage the track before breaking on purpose (Day 25 B1c, #287):** `git checkout -- file` restores the *index*, not the pre-break state. Reverting breaks that way on unstaged work wiped an edited file back to HEAD and emptied an intent-to-add (`git add -N`) file; two breaks ran on broken code. `git add` the work first, then break / run / `git checkout --`. Also: sed/perl patterns spanning lines must allow `\r?\n` (checked-out files are CRLF), and confirm each break applied before trusting a green run.
