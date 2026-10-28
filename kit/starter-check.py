"""The starter check (CHANGES.md item 72): what a person who copies this repository and deletes kit/
starts with, made from HEAD.

1. HEAD's files without kit/ in a fresh folder, `git init -b main`, one commit.
2. No day specs: no specs/day-*.
3. spec-drift.py --build with no GitHub remote writes the page, and stderr holds only its NO_REMOTE line.
4. The page draws in node (test_spec_drift.py's drawn(page=)): no error, nothing logged, no panel failed.
5. No line names the project the kit was copied from, except where EXEMPT says why.

    python kit/starter-check.py    # a line per step; on the first that fails, exit 1 with a last line naming it

It needs what the page tests need: numpy and node. Its folder is a temporary one, removed after.
"""
import ast
import importlib.util
import io
import os
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# Item 72's list. Left out for false hits: `Day \d+` and `#\d+` (the rules' examples, the branch
# grammar), migration, gateway, AWS, Java (TEST_PATH names .java), V1, and Maven (item 60's rules).
MARKERS = (r"jobmatch|hackyourfuture|KAN-[0-9]|identity-service|job-service|api-gateway|mvnw|checkstyle|surefire"
           r"|flyway|terraform|localstack|infra-ci|eu-west-1|\bECS\b")

# The files that still name it, kept by a maintainer's decision (CHANGES.md, Batch 8), each with why.
EXEMPT = {
    ".claude/agents/architecture-auditor.md": "the source project's system, as marked examples (item 70)",
    ".claude/agents/security-ops-auditor.md": "the source project's system, as marked examples (item 70)",
    ".claude/agents/spec-auditor.md": "evidence from the source project, marked as its (item 61)",
    "specs/README.md": "evidence from the source project, marked as its (item 63)",
    "CLAUDE.md": "evidence from the source project, marked as its (item 65)",
    "scripts/break.py": "the Maven rules, inert for any other command (item 60)",
    "scripts/test_break.py": "the Maven rules' tests (item 60)",
    "scripts/infra-summary.py": "the infra panel's summary, off without an infra workflow (items 55, 56)",
    "scripts/test_infra_summary.py": "the infra summary's tests (items 55, 56)",
}
# And in scripts/test_spec_drift.py, PageProseTest.MARKERS alone: the words the page's prose must not hold.
LISTED = ("scripts/test_spec_drift.py", "PageProseTest", "MARKERS")


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, check=True).stdout


def listed_lines(copy):
    """The line numbers of LISTED's assignment."""
    path, cls, name = LISTED
    with open(os.path.join(copy, path), encoding="utf-8") as f:
        tree = ast.parse(f.read())
    body = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls).body
    node = next(n for n in body if isinstance(n, ast.Assign) and [t.id for t in n.targets] == [name])
    return range(node.lineno, node.end_lineno + 1)


def hits(copy):
    """Each line the marker search finds, outside the exemptions, as (path, line number)."""
    found = subprocess.run(["git", "-C", copy, "grep", "-n", "-I", "-i", "-E", "-e", MARKERS],
                           capture_output=True, encoding="utf-8", errors="replace").stdout
    keep = listed_lines(copy)
    out = []
    for line in found.splitlines():
        path, n, _ = line.split(":", 2)
        if path not in EXEMPT and not (path == LISTED[0] and int(n) in keep):
            out.append((path, int(n)))
    return out


def main():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        copy = os.path.join(tmp, "starter")
        with tarfile.open(fileobj=io.BytesIO(git(ROOT, "archive", "--format=tar", "HEAD"))) as tar:
            members = [m for m in tar.getmembers() if m.name.split("/")[0] != "kit"]
            tar.extractall(copy, members, **({"filter": "data"} if hasattr(tarfile, "data_filter") else {}))
        git(copy, "init", "-q", "-b", "main")
        git(copy, "add", "-A")
        git(copy, "-c", "user.name=starter", "-c", "user.email=starter@example.com", "commit", "-q", "-m", "Start")
        files = len(git(copy, "ls-files").splitlines())
        print(f"1. HEAD without kit/: {files} files, one commit on main")

        days = [f for f in os.listdir(os.path.join(copy, "specs")) if f.startswith("day-")]
        if days:
            raise SystemExit(f"2. failed: {len(days)} day specs in specs/")
        print("2. no day specs")

        spec = importlib.util.spec_from_file_location("starter_tests", os.path.join(copy, "scripts", "test_spec_drift.py"))
        tests = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tests)
        page = os.path.join(tmp, "index.html")
        env = {k: v for k, v in os.environ.items() if k not in ("GH_REPO", "GH_HOST")}
        built = subprocess.run([sys.executable, os.path.join("scripts", "spec-drift.py"), "--build", page,
                                "--cache", os.path.join(tmp, "cache.json")],
                               cwd=copy, env=env, capture_output=True, encoding="utf-8", errors="replace")
        # One print, gh's reason in brackets: gh says it in one line with no remote, in several with no token.
        alone = re.fullmatch(re.escape(tests.sd.NO_REMOTE) + r" \(gh repo view: .*\)\n", built.stderr, re.S)
        if built.returncode or not os.path.exists(page) or not alone or "Traceback" in built.stderr:
            raise SystemExit(f"3. failed: exit {built.returncode}, page written: {os.path.exists(page)}, "
                             f"stderr: {built.stderr.strip()[-300:]!r}")
        print("3. spec-drift.py --build wrote the page; stderr: the NO_REMOTE line alone")

        error, panels, logged = tests.drawn(page=page)
        failed = [box for box, html in panels.items() if "This panel failed" in html]
        if error or logged or failed:
            raise SystemExit(f"4. failed: error {error!r}, {len(logged)} logged, panels failed: {failed}")
        print(f"4. the page draws {len(panels)} boxes: no error, nothing logged, no panel failed")

        found = hits(copy)
        if found:
            named = sorted({path for path, _ in found})
            raise SystemExit(f"5. failed: {len(found)} lines in {len(named)} files name the source project: "
                             f"{', '.join(named)}")
        print(f"5. no line names the source project outside the {len(EXEMPT) + 1} exemptions")
    print("starter check: 5 of 5 steps pass")


if __name__ == "__main__":
    main()
