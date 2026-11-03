"""The Evidence replay installs what the replayed checks need before it replays them.

The tests run the workflow's own text: the `run:` block of the step "Install what the replayed
checks need" in .github/workflows/evidence.yml, read from the file, in bash (Git's own on Windows,
not WSL's), in a scratch directory, with a stand-in `python` first on PATH that records its
arguments and installs nothing.

    python scripts/test_evidence_workflow.py    # needs PyYAML
"""
import os
import shutil
import subprocess
import tempfile
import unittest

import yaml

from test_diff_limit import BASH

HERE = os.path.dirname(os.path.abspath(__file__))
WORKFLOW = os.path.join(HERE, "..", ".github", "workflows", "evidence.yml")
STEP = "Install what the replayed checks need"
REPLAY = "Replay the closing merge"


def step():
    """The step's run: text."""
    with open(WORKFLOW, encoding="utf-8") as f:
        for s in yaml.safe_load(f)["jobs"]["replay"]["steps"]:
            if s.get("name") == STEP:
                return s["run"]
    raise AssertionError(f"no step named {STEP!r} in evidence.yml")


class EvidenceWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        bin_dir = os.path.join(self.dir, "bin")
        os.mkdir(bin_dir)
        self.calls = os.path.join(self.dir, "calls.txt")
        with open(os.path.join(bin_dir, "python"), "w", newline="\n") as f:
            f.write(f'#!/bin/sh\necho "$*" >> "{self.calls.replace(os.sep, "/")}"\n')
        os.chmod(os.path.join(bin_dir, "python"), 0o755)
        self.work = os.path.join(self.dir, "work")
        os.mkdir(self.work)
        self.path = bin_dir.replace(os.sep, "/")

    def run_step(self):
        # Git's bash on Windows wants PATH entries as /c/..., which cygpath gives; elsewhere it is absent
        path = f'export PATH="$(cygpath -u "{self.path}" 2>/dev/null || echo "{self.path}"):$PATH"\n'
        p = subprocess.run([BASH, "-c", path + step()], cwd=self.work, capture_output=True, text=True)
        calls = open(self.calls).read().splitlines() if os.path.exists(self.calls) else []
        return p.returncode, p.stdout + p.stderr, calls

    def test_the_install_comes_before_the_replay(self):
        with open(WORKFLOW, encoding="utf-8") as f:
            names = [s.get("name") for s in yaml.safe_load(f)["jobs"]["replay"]["steps"]]
        self.assertIn(STEP, names)
        self.assertLess(names.index(STEP), names.index(REPLAY))

    def test_a_requirements_txt_is_installed(self):
        open(os.path.join(self.work, "requirements.txt"), "w").close()
        code, out, calls = self.run_step()
        self.assertEqual(code, 0, out)
        self.assertEqual(calls, ["-m pip install -r requirements.txt"])

    def test_with_no_requirements_txt_nothing_is_installed(self):
        code, out, calls = self.run_step()
        self.assertEqual(code, 0, out)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
