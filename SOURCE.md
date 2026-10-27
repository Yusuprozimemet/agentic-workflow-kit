# Source

Every file here was copied unchanged from jobmatch-microservices. This is the record later
changes are compared against.

- Source repository: `jobmatch-microservices` (github.com/Yusuprozimemet/jobmatch-microservices)
- Commit: `7cbae28920b08953f63a8c05ff549dcd89b7a910`
- Repository files: the committed blob at that commit (`git cat-file blob <sha>:<path>`), written in
  binary mode. Check: `git show HEAD:<path> | sha256sum` here equals
  `git show <sha>:<path> | sha256sum` in jobmatch.
- Lessons: the maintainer's Claude Code memory files for jobmatch, copied from disk
  (`~/.claude/projects/c--Users-HackYourFuture-yusup-jobmatch-microservices/memory/`); the hash is of
  the disk bytes.

Flags: **P** process, works in any project; **J** jobmatch-specific, copied for reference;
**mixed** process with jobmatch-specific parts.

## Repository files

| Path | Source path | sha256 | Flag |
|---|---|---|---|
| `.claude/agents/plan-auditor.md` | `.claude/agents/plan-auditor.md` | `7d9b977830d4af5d90ad5aa9a76a45042cbc58fb33264ea7347f20ea228cdda0` | P |
| `.claude/agents/spec-auditor.md` | `.claude/agents/spec-auditor.md` | `506dc155c89a746d5a9994d6a216e4a83b897fa9d37d0db5cae41bafc2524db6` | P |
| `.claude/agents/implementer.md` | `.claude/agents/implementer.md` | `e73cd793009b9ed7c292e00d9c6476a35745829a1840c6391be74890af634aea` | P |
| `.claude/agents/defect-rater.md` | `.claude/agents/defect-rater.md` | `b7d32dae0fdb35bfef3016c3bd023764a890c8b13829a3a190737b9b37ec209b` | P |
| `.claude/agents/security-ops-auditor.md` | `.claude/agents/security-ops-auditor.md` | `67f41ca17a5051e171d80d05c26efd8d76e1ca61a1d7088714822f82e2ecee39` | J. Modified in Batch 1: jobmatch-only paths marked as examples (the Infrastructure bullet, and the database-role scripts); no wording changed. |
| `.claude/agents/agentic-engineering-auditor.md` | `.claude/agents/agentic-engineering-auditor.md` | `ca25c4892ef6609d9a8daaa6fb0f03a2b2080bcc25eb8319950f4a079c38a569` | J |
| `.claude/agents/architecture-auditor.md` | `.claude/agents/architecture-auditor.md` | `47be9b561218e82d867040112e7c0c3497689fc3d4d8d7c5a4faea493e4852a5` | J. Modified in Batch 1: `scripts/infra-checks.py` and `scripts/teardown-check.sh` marked as jobmatch examples; no wording changed. |
| `specs/README.md` | `specs/README.md` | `11f4ff3a617b32ecc73bb1fb76aa86ab379d089cea46dbc6280537fad673b028` | P. Modified in Batch 1: line 75: the link to `docs/paper/success-criteria.md` removed, its text kept. |
| `specs/_template.md` | `specs/_template.md` | `a8080d62e4675aaa167b197269f7d99c693b5607e542c040bc6e953b9b12c5b0` | P |
| `specs/day-12-jwt-issuance.md` | `specs/day-12-jwt-issuance.md` | `b4403f7c2b5fff3c199e31bb97a8d8020124b8f453c72bccf454410fc99f0620` | J |
| `specs/day-36-ecs-services.md` | `specs/day-36-ecs-services.md` | `bcebf46a49c4800f4b4d8036200d1a67e63ce56f1c29b0d2814e2b9c551b98b9` | J |
| `.github/pull_request_template.md` | `.github/pull_request_template.md` | `79a102beb775a1b71d1a82c3d0fbd6141a9d447c8ea253c13a992d3d0f4281b1` | P |
| `.github/workflows/pr-checks.yml` | `.github/workflows/pr-checks.yml` | `b4141baab9e46bbb19cf7b3a6605357c8ebbf90956d461ed865fd7ca6761de61` | mixed. Modified in Batch 3: jobs 3 and 4 run their check step only `if: hashFiles('services/**') != ''` (invariants' compare step; `service-wiring.py`, while `test_service_wiring.py` still runs); the template check and the 400-line limit untouched. |
| `.github/workflows/dashboard.yml` | `.github/workflows/dashboard.yml` | `922e27e3d2e106d2ae97931995ebca084a837083feecbabd78058f7aebbbc415` | P. Modified in Batch 3: a comment under the `workflow_run` trigger: with no workflow named "Infra checks", it never fires; the trigger itself kept. |
| `.github/workflows/spec-drift-tests.yml` | `.github/workflows/spec-drift-tests.yml` | `17611315863261c90407c662718665b44416ba032faccc5641af152f37d712c6` | P |
| `.github/workflows/README.md` | `.github/workflows/README.md` | `5bb11eba0f08aa01a1babbfed841b7a18bc27355a22e3646c7750246ffb2c53e` | P |
| `scripts/spec-drift.py` | `scripts/spec-drift.py` | `16675a9c8846ae4c52876f62c0bb29276f9804c4e21306f62d916b830e7e6882` | P |
| `scripts/token-usage.py` | `scripts/token-usage.py` | `1d5a981ab41afaa10fe263993022c548dab6d6feb2df6c28d024cda80f950a89` | P |
| `scripts/infra-summary.py` | `scripts/infra-summary.py` | `a9d733f2f176133e733b2e3fa7de643c5e6a67463e69b88329505ad5891e2bf4` | J |
| `scripts/live-checks.py` | `scripts/live-checks.py` | `d5bf006c5887317d9f682f43a31fc9edc75cf21e3675220de025f667173f9cc9` | J |
| `docs/dashboard/index.html` | `docs/dashboard/index.html` | `187175d922f58c1bbc2ad1473d6e11561321506b4f78c56d8e8ecc3d9836bec1` | P. Modified in Batch 1: `<title>` is `Spec Drift` and the eyebrow starts empty; `dashboard.js` sets both from its `PROJECT` value. |
| `docs/dashboard/dashboard.css` | `docs/dashboard/dashboard.css` | `50a2e322dc720ff31fbe1a02e57aecd222a14402ba0f78bae9b1a464bfa8d801` | P |
| `docs/dashboard/dashboard.js` | `docs/dashboard/dashboard.js` | `b01e13a1444d552cbd0c1df4540cd7394713bb335e3999ccc3e8952cf764f40c` | P. Modified in Batch 1: the project name is one marked value, `const PROJECT` (default `jobmatch-microservices`), used for the eyebrow and the tab title (`${PROJECT} Spec Drift`). |
| `docs/dashboard/token-usage.json` | `docs/dashboard/token-usage.json` | `c137dd53cf034ed38cec03fd2b42c511cea1e3106ee8d9b6e79b160beab0fb65` | J |
| `docs/dashboard/deployment.json` | `docs/dashboard/deployment.json` | `a46ea919947e6a1e0c3e36776af9354947f877390e3ffe93c5b0e8a44b5ff4d0` | J |
| `scripts/break.py` | `scripts/break.py` | `7972981fcf4699c32f33b47ddeec0521cadb7e772d7dbe902b1942c430267554` | P |
| `scripts/relabel.py` | `scripts/relabel.py` | `87d856ed70bb2474bdbe6571d81428bb954da5800795449846e6e5329e2fab0d` | P |
| `scripts/pr-names.py` | `scripts/pr-names.py` | `125051aa4700be36afdb327680bbd086968071b4790420072a859b73ed1f5b05` | P |
| `scripts/invariants.py` | `scripts/invariants.py` | `5320bf99538533df5bae2d470bf7f8a4d085536891e2f87ee634bc137288a21b` | J |
| `scripts/service-wiring.py` | `scripts/service-wiring.py` | `eeb5bf0b2abbe3d8ec2594ecda1737a7a3071a1ca66aa0590fcb54dc3102c3c6` | J |
| `scripts/check-links.py` | `scripts/check-links.py` | `a8aff0d981fa24bc5435d6ebff74d0835797a1c565b2f213a3c6d20380873456` | P |
| `scripts/test_spec_drift.py` | `scripts/test_spec_drift.py` | `f832d00fd2adbe6d324c149d6d35f78c75212043454c49a3c3555df044c43dd0` | P. Modified in Batch 2: `test_the_repositorys_plan_parses` replaced by `test_a_plan_and_its_specs_parse`: it writes its own plan.md (a cut item, a stop lifted by a course correction) and specs/ to a temp dir and reads them the same way. |
| `scripts/test_token_usage.py` | `scripts/test_token_usage.py` | `336aa9d4a760925ca54856b61bba524b0552a22b106e52359b122ffb778b7340` | P |
| `scripts/test_infra_summary.py` | `scripts/test_infra_summary.py` | `765d7ebe9f88fc8e88c39f7a10f24996e814456dfda7f384e639071c8200e9aa` | J |
| `scripts/test_break.py` | `scripts/test_break.py` | `96ba34a2e3bf7331a27be0855182c82b1096c86ab8e06e409a38878157451203` | P |
| `scripts/test_relabel.py` | `scripts/test_relabel.py` | `58c73cdc085dd3988a9ea97a8dde49da27ab8abe49598db79a5f2c2dc37865ae` | P. Modified in Batch 2: `PaperSampleTest` (82 entries, 11 escapes in jobmatch's Days 21-28) replaced by `SampleTest`, two small day specs it writes itself (7 entries, 3 escapes, every found: given a stage); the module docstring's first paragraph says so. |
| `scripts/test_pr_names.py` | `scripts/test_pr_names.py` | `4c50e672ab3a73ac3c2eec3408f168fc9a02bc78517b11d735dc21445c3a8cc2` | P |
| `scripts/test_invariants.py` | `scripts/test_invariants.py` | `2796a58cc5ab1141b137fbaf2cf57a00039896856a011843b70dbbcb4ba7fcb5` | J |
| `scripts/test_service_wiring.py` | `scripts/test_service_wiring.py` | `b42105c0c9a3ca3e4fe98eba450d71cf93f83ee32e3dbc18bad7221cbf889903` | J |
| `CLAUDE.md` | `CLAUDE.md` | `4bc473b17f1c4ddaf9d195339d884d85289d2937ed5e3d03d8bfee22fa2ffd98` | mixed |
| `docs/workflow.md` | `docs/workflow.md` | `72a1cf7547f570d9bcd1058a93d2420ebcb1fbddda1c4bf475a62c3d0837c7e2` | P |
| `docs/agent-workflow.svg` | `docs/agent-workflow.svg` | `e6ddbc0adea3289d673ea14ff3987c0eef2253d99ceed8829a193ae480a1e658` | P |
| `docs/agent-workflow.png` | `docs/agent-workflow.png` | `39b1f3b068af9e87b2f39cc51972e0f56ff84b85188ae28fe6e62789a77676a9` | P |
| `docs/defects.md` | `docs/defects.md` | `90d287e8a51ccc9c179881e430b6b7e64237b93bab9f58f3693a1e72100946c7` | P |
| `docs/lab-notebook.md` | `docs/lab-notebook.md` | `605d3f2b18b432c6ec76260e244890be2f6b4bd2364948133af7876f93cf8e4e` | J. Modified in Batch 1: three dangling links (lines 3 and 1088 to `../README.md`, 1095 to `paper/success-criteria.md`) removed, their text kept. |
| `docs/audit-findings.md` | `docs/audit-findings.md` | `5fd8aba423ec91161dd1dc73614920611a83ccb53bc55c3a54f41fea941ee68a` | J |
| `plan.md` | `plan.md` | `88201b753d9a155136fbf72589416d0cae4c183eae13beed9c2516a4cb84a23f` | J |
| `.gitattributes` | `.gitattributes` | `5a3e1b44d3c45726a00be7ef0545b7846f68146c6369e15581915d1e2b18875a` | mixed |
| `.gitignore` | `.gitignore`, excerpt, lines 241-242 | `83e6f807ad3a1e40037e8c062345d90b5b3afa2fce125489d6c1d3fca0d608ec` (the excerpt) | P. Modified in Batch 1: added `__pycache__/`. |

## Lessons

| Path | Source | sha256 | Flag |
|---|---|---|---|
| `lessons/spec-first-workflow.md` | `memory/spec-first-workflow.md` | `58a236b7062823d13233c52fc8a13253855a041aa855dbe7a746667ba90dafba` | P |
| `lessons/spec-process-improvements.md` | `memory/spec-process-improvements.md` | `999409b1723446eb53196842b503543d19a7e760bb26269dcf0f91b3277d0a5a` | P |
| `lessons/checks-before-push.md` | `memory/checks-before-push.md` | `22afc2c8ccbd2c58f00045940fb03ef71620a65432144ed151ff05dfa2fe9ce9` | mixed |
| `lessons/auditors-on-opus.md` | `memory/auditors-on-opus.md` | `7e6c7b270d3b2d5e03a8634ebdbc15cc1efc5f1ca1f5c6fffaf8135b9a7e9b0c` | P |
| `lessons/implementer-on-haiku.md` | `memory/implementer-on-haiku.md` | source disk (CRLF): `c87586ddfa45aa519e9fde5d2688d559c69e502ef20469426843fce4539e0bd1`; stored in git (LF): `0027a360e7d1c54b0a63ccc16f126b5057b7eede768f7c372227546a9fad99ff` | P |
| `lessons/maintainer-review-style.md` | `memory/maintainer-review-style.md` | source disk (CRLF): `0a3592ce657ce735cd1c8d82f3160d2313c566af9aa38d69b4baa1487e31720a`; stored in git (LF): `707f84329b933b63dced6e8670561dbf0df5780acd38baa6d09a0f5aee840795` | P |
| `lessons/spec-auditor-eval.md` | `memory/spec-auditor-eval.md` | `f9f6c78a63e08b548bfc20913b9bd3442fc27dbb8a7503c40ea6aa64ad2b121a` | P |
| `lessons/attribution-rejected.md` | `memory/attribution-rejected.md` | source disk (CRLF): `4d89a31d44799909db495d7f956a7bbfe0f452d128ccbd849cd914d752a1e96d`; stored in git (LF): `975850bdc45f86ccfa075d517789213493547dd10b431cdc9ca17087d9aad5bc` | P |
| `lessons/dev-loop-dropped.md` | `memory/dev-loop-dropped.md` | `5578f6fb0f588356ac21246489d74ddcdf584e0dda713d61114a4e6e38d3c77a` | P |

Three lessons were CRLF on disk (`attribution-rejected.md`, `implementer-on-haiku.md`,
`maintainer-review-style.md`); `core.autocrlf` stored them LF in git. The only difference is CRLF→LF:
for every lesson, the source with CR removed (`tr -d '\r' < <source> | sha256sum`) hashes the same as
the git blob (`git show HEAD:lessons/<file> | sha256sum`), 9 of 9. Lessons are read, never executed,
so LF in git is kept; the byte-for-byte rule is for the repository files, and those 48 match.

## Notes

- Changes after the copy are recorded in each changed file's row: "Modified in Batch N: <what>".
  A commit cannot name its own hash, so each batch's commit subject starts `Batch N:`; find it with
  `git log --oneline --grep '^Batch N:'`.
- `.gitignore` is an excerpt: lines 241-242 of jobmatch's `.gitignore` (the dashboard
  cache), not the whole file. It is the one copied file that is not a whole file.
- The two example specs are Day 12 (early) and Day 36 (late). No early day shows the full close as it is
  written today: criterion IDs, `broken:` lines and hand-offs start at Day 28. No spec shows the blind
  relabel yet; it exists only in `CLAUDE.md` (A day, in order, step 3) and `scripts/relabel.py`.
- `lessons/checks-before-push.md` is mixed: about half its items are Maven and test-harness lessons
  from jobmatch.
- Correction: the Step 1 inventory said every memory was LF. Three were CRLF. The check used then,
  `grep -lc $'\r'` in Git Bash, could not see CR bytes: that grep treats a pattern of a lone CR as
  empty, so it matches every line of an LF-only file too (15 of 15 lines of `auditors-on-opus.md`,
  which has no CR), and the 0 it printed was not a count of CRLF files. CRs are counted with
  `tr -cd '\r' < <file> | wc -c`.
