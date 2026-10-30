"""Commit-to-spec lookup against real throwaway Git repositories."""
import os
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from evidence import closing_spec
from test_evidence import GIT_ENV


class ClosingSpecTest(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, ignore_errors=True)
        self.git("init", "-q", "-b", "main")
        self.git("commit", "-q", "--allow-empty", "-m", "base")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, env=GIT_ENV,
                              capture_output=True, text=True, check=True).stdout

    def merge(self, specs=(), subject="Merge pull request #9 from owner/day-07/close-the-day"):
        self.git("switch", "-q", "-c", "close")
        os.makedirs(os.path.join(self.repo, "specs"))
        for name in specs:
            with open(os.path.join(self.repo, "specs", name), "w") as file:
                file.write("# Day 07\n")
        self.git("add", ".")
        self.git("commit", "-q", "--allow-empty", "-m", "close")
        self.git("switch", "-q", "main")
        self.git("merge", "-q", "--no-ff", "-m", subject, "close")

    def lookup(self):
        # Only route the production Git calls to the fixture; Git itself is real.
        with patch("evidence.git", side_effect=self.git):
            return closing_spec("HEAD")

    def test_one_spec(self):
        self.merge(("day-07-example.md",))
        self.assertEqual(self.lookup(), "specs/day-07-example.md")

    def test_ordinary_merge(self):
        self.merge(subject="Merge pull request #9 from owner/tooling/example")
        self.assertIsNone(self.lookup())

    def test_direct_commit(self):
        self.assertIsNone(self.lookup())  # A root commit has no parents.
        self.git("commit", "-q", "--allow-empty", "-m",
                 "Merge pull request #9 from owner/day-07/close-the-day")
        self.assertIsNone(self.lookup())

    def test_missing_spec(self):
        self.merge()
        with self.assertRaisesRegex(ValueError, "day-07: expected one spec, found 0"):
            self.lookup()

    def test_two_specs(self):
        self.merge(("day-07-a.md", "day-07-b.md"))
        with self.assertRaisesRegex(ValueError, "day-07: expected one spec, found 2"):
            self.lookup()


if __name__ == "__main__":
    unittest.main()
