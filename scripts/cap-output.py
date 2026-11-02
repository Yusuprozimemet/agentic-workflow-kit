"""A long Bash result keeps its first and last 3,000 characters in the context; the rest is saved.

    python scripts/cap-output.py     # PostToolUse on Bash: prints the replacement output, if any

The hook in the project settings (.claude/settings.json) runs it after every Bash command. Bash
output is most of what the 2k-cap saving in token-usage.py --simulate would cut, since every later
reply re-reads it. So a stdout of more than 8,000 characters
is cut to its head and tail, with one line between them that names the saved file. That file is
the full stdout, written to .claude/tool-output/ (gitignored) before anything is cut.

Three results pass unchanged: one of 8,000 characters or fewer; one with stderr or an interruption,
since a failing command's error often ends its output and the model needs all of it; and one whose
full output cannot be saved, since a cut without the file would lose the middle for good.

Bash's tool_response has no exit code, so stderr and `interrupted` stand in for failure. The reply
keeps Bash's own object (stdout, stderr, interrupted, ...) with only stdout replaced: a plain string
in updatedToolOutput is silently ignored.

The settings' command finds this script through CLAUDE_PROJECT_DIR, read in Python, and exits 0
without it: VS Code Copilot reads the same settings, runs the hook for every tool and sets no such
variable (see auditor-guard.py).
"""
import json
import os
import sys
import uuid

LIMIT = 8000
KEEP = 3000
SAVED = os.path.join(".claude", "tool-output")


def cut(stdout, path):
    note = f"[cut {len(stdout) - 2 * KEEP} chars; full output: {path}; use Read with offset/limit or grep]"
    return f"{stdout[:KEEP]}\n{note}\n{stdout[-KEEP:]}"


def handle(data, project):
    resp = data.get("tool_response")
    if not isinstance(resp, dict):
        return None
    stdout = resp.get("stdout") or ""
    if len(stdout) <= LIMIT or resp.get("stderr") or resp.get("interrupted"):
        return None
    folder = os.path.join(project, SAVED)
    path = os.path.abspath(os.path.join(folder, uuid.uuid4().hex + ".txt"))
    try:
        os.makedirs(folder, exist_ok=True)
        with open(path, "wb") as f:
            f.write(stdout.encode("utf-8", "replace"))
    except OSError:
        return None
    text = cut(stdout, path)
    return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": dict(resp, stdout=text)}}


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        return
    project = os.environ.get("CLAUDE_PROJECT_DIR")
    if not project:
        return
    out = handle(data, project)
    if out:
        print(json.dumps(out))


if __name__ == "__main__":
    main()
