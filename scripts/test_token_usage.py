"""The token counts move with the replies and only then.

Each test writes a small transcript to a temporary folder and runs token-usage.py's count over it:
a reply is counted once, from its last streamed line, and the day comes from the branch.

    python scripts/test_token_usage.py
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("token_usage", os.path.join(HERE, "token-usage.py"))
tu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tu)


def line(message_id="msg_1", request_id="req_1", output=3, branch="day-43/track-a2-x"):
    """One assistant line, as Claude Code writes it per streamed content block."""
    return json.dumps({
        "type": "assistant",
        "requestId": request_id,
        "timestamp": "2026-10-12T10:00:00Z",
        "gitBranch": branch,
        "message": {
            "id": message_id,
            "model": "claude-haiku-5-5-20260101",
            "usage": {"input_tokens": 10, "cache_creation_input_tokens": 0,
                      "cache_read_input_tokens": 0, "output_tokens": output},
        },
    })


class CountTest(unittest.TestCase):
    def count(self, lines):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "session.jsonl")
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return tu.count([path])

    def rows(self, totals):
        return [(key, dict(t)) for key, t in totals.items()]

    def test_a_reply_is_counted_from_its_last_line(self):
        totals = self.count([line(output=3), line(output=120)])
        rows = self.rows(totals)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1]["output"], 120)
        self.assertEqual(rows[0][1]["replies"], 1)

    def test_identical_repeats_count_once(self):
        totals = self.count([line(output=50), line(output=50), line(output=50)])
        rows = self.rows(totals)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1]["output"], 50)
        self.assertEqual(rows[0][1]["replies"], 1)

    def test_different_replies_add_up(self):
        totals = self.count([line(message_id="msg_1", output=10), line(message_id="msg_2", output=20)])
        rows = self.rows(totals)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1]["output"], 30)
        self.assertEqual(rows[0][1]["replies"], 2)

    def test_the_day_comes_from_the_branch(self):
        day43 = self.rows(self.count([line(branch="day-43/track-a2-x")]))
        self.assertEqual(day43[0][0][1], 43)
        main = self.rows(self.count([line(branch="main")]))
        self.assertIsNone(main[0][0][1])


class TranscriptsTest(unittest.TestCase):
    """Only this repository's transcript folders are read: its own and its worktrees'."""

    def test_a_sibling_whose_name_starts_with_this_ones_is_not_read(self):
        root = tempfile.mkdtemp()
        name = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.join(HERE, os.pardir)))
        for folder in (name, name + "--claude-worktrees-a", name + "-pilot", name + "2", "other"):
            os.mkdir(os.path.join(root, folder))
            with open(os.path.join(root, folder, "s.jsonl"), "w", encoding="utf-8") as f:
                f.write(line())
        read = sorted(os.path.basename(os.path.dirname(p)) for p in tu.transcripts(root))
        self.assertEqual(read, [name, name + "--claude-worktrees-a"])


def native(path):
    # The test builds its files with its own \\?\ prefix, not the script's, so it runs on main's code too.
    return "\\\\?\\" + path if os.name == "nt" else path


class LongPathTest(unittest.TestCase):
    def setUp(self):
        self.root = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, native(self.root))
        name = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.join(HERE, os.pardir)))
        self.project = os.path.join(self.root, name)

    def write(self, path, text):
        os.makedirs(native(os.path.dirname(path)), exist_ok=True)
        with open(native(path), "w", encoding="utf-8") as f:
            f.write(text)

    def test_transcript_past_max_path_is_counted(self):
        # A subagent's transcript in a folder past 260 characters, beside a session at a short path.
        self.write(os.path.join(self.project, "short.jsonl"), line(output=3, branch="main") + "\n")
        folder = os.path.join(self.project, "s" * 200, "subagents")
        self.write(os.path.join(folder, "agent-" + "a" * 100 + ".jsonl"), line(message_id="msg_2", output=7, branch="main") + "\n")
        self.write(os.path.join(folder, "agent-" + "a" * 100 + ".meta.json"), '{"agentType": "implementer"}')
        self.assertGreater(len(folder), 260)
        totals = tu.count(tu.transcripts(self.root))
        self.assertEqual({who: t["output"] for (_, _, _, who), t in totals.items()},
                         {"main": 3, "implementer": 7})


class MergeTest(unittest.TestCase):
    """The rows already written are kept, those from before agents were counted among them."""

    def test_a_row_with_no_agent_keeps_its_count_as_unknown(self):
        with tempfile.TemporaryDirectory() as root:
            out = os.path.join(root, "token-usage.json")
            model = "claude-haiku-5-5"  # as rows store it, its date taken off
            legacy = dict(date="2026-10-12", day=43, model=model, input=10, cache_write=0, cache_read=0, output=100, replies=4)
            other = dict(legacy, date="2026-10-11", output=40, replies=2)
            with open(out, "w", encoding="utf-8") as f:
                json.dump([legacy, other], f)
            # Still on disk: one reply of the 2026-10-12 total, the main session's.
            project = os.path.join(root, "projects", re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(os.path.join(HERE, os.pardir))))
            os.makedirs(project)
            with open(os.path.join(project, "s.jsonl"), "w", encoding="utf-8") as f:
                f.write(line(output=30) + "\n")
            run = subprocess.run([sys.executable, os.path.join(HERE, "token-usage.py"), "--transcripts",
                                  os.path.join(root, "projects"), "--out", out], capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            with open(out, encoding="utf-8") as f:
                rows = {(r["date"], r["agent"]): (r["output"], r["replies"]) for r in json.load(f)}
        self.assertEqual(rows, {("2026-10-11", "unknown"): (40, 2),
                                ("2026-10-12", "main"): (30, 1), ("2026-10-12", "unknown"): (70, 3)})


if __name__ == "__main__":
    unittest.main()
