"""Tests for branch_overview.py, against real temporary git repositories.

Run from the repository root:
    python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts

The costly failure of this script is not a crash but a false "all clear":
a branch that could not be compared must never disappear from the report.
The shallow-clone tests exist for exactly that case.
"""

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE / "branch_overview.py"
sys.path.insert(0, str(HERE))

import branch_overview as bo  # noqa: E402

ENV = dict(
    os.environ,
    GIT_AUTHOR_NAME="Test", GIT_AUTHOR_EMAIL="test@example.com",
    GIT_COMMITTER_NAME="Test", GIT_COMMITTER_EMAIL="test@example.com",
    GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1",
)


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, env=ENV, check=True,
                   capture_output=True)


def commit(cwd, name, text):
    (pathlib.Path(cwd) / name).write_text(text, encoding="utf-8")
    git(cwd, "add", name)
    git(cwd, "commit", "-q", "-m", f"change {name}")


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class TestBranchOverview(unittest.TestCase):
    """origin has main plus three branches that fork at the first commit.

    - feature-a and feature-b both change shared.md (a collision)
    - done is merged into main (must not be listed)
    main moves on by several commits, so a depth-1 clone lacks the fork point.
    """

    @classmethod
    def setUpClass(cls):
        cls.tmp = pathlib.Path(tempfile.mkdtemp())
        work = cls.tmp / "work"
        work.mkdir()
        git(work, "init", "-q", "-b", "main")
        commit(work, "base.md", "base\n")
        git(work, "branch", "feature-a")
        git(work, "branch", "feature-b")
        git(work, "branch", "done")
        for i in range(5):
            commit(work, f"main-{i}.md", f"{i}\n")
        git(work, "switch", "-q", "feature-a")
        commit(work, "shared.md", "a\n")
        commit(work, "only-a.md", "a\n")
        git(work, "switch", "-q", "feature-b")
        commit(work, "shared.md", "b\n")
        git(work, "switch", "-q", "done")
        commit(work, "done.md", "done\n")
        git(work, "switch", "-q", "main")
        git(work, "merge", "-q", "--no-edit", "done")
        commit(work, "after-merge.md", "x\n")
        cls.origin = cls.tmp / "origin.git"
        git(cls.tmp, "clone", "-q", "--bare", str(work), str(cls.origin))
        cls.url = cls.origin.as_uri()  # file:// so that --depth works

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def clone(self, *flags):
        target = pathlib.Path(tempfile.mkdtemp(dir=self.tmp)) / "clone"
        git(self.tmp, "clone", "-q", *flags, self.url, str(target))
        return target

    def run_script(self, cwd, *args):
        r = subprocess.run([sys.executable, str(SCRIPT), "--no-gh", *args],
                           cwd=cwd, env=ENV, capture_output=True, text=True,
                           timeout=120)
        return r.returncode, r.stdout, r.stderr

    def test_full_clone_lists_open_branches_and_collision(self):
        code, out, _ = self.run_script(self.clone())
        self.assertEqual(code, 0)
        self.assertIn("2 open branch(es)", out)
        self.assertIn("feature-a", out)
        self.assertIn("feature-b", out)
        self.assertNotIn("  done\n", out)
        self.assertIn("WARNING: 1 file(s) are on more than one branch.", out)
        self.assertIn("shared.md", out)
        self.assertNotIn("skipped", out)

    def test_counts_commits_and_files(self):
        branches, skipped = bo.collect(cwd=str(self.clone()))
        self.assertEqual(skipped, [])
        a = next(b for b in branches if b["short"] == "feature-a")
        self.assertEqual(a["ahead"], 2)
        self.assertEqual(sorted(a["files"]), ["only-a.md", "shared.md"])
        self.assertGreaterEqual(a["age"], 0)

    def test_strict_exits_1_when_branches_are_open(self):
        code, _, _ = self.run_script(self.clone(), "--strict")
        self.assertEqual(code, 1)

    def test_shallow_clone_reports_skipped_not_all_clear(self):
        clone = self.clone("--depth", "1", "--no-single-branch")
        code, out, _ = self.run_script(clone)
        self.assertEqual(code, 0)
        self.assertIn("branch(es) skipped", out)
        self.assertIn("feature-a", out)
        self.assertIn("--deepen", out)
        self.assertNotIn("main has everything", out)

    def test_shallow_clone_strict_fails(self):
        clone = self.clone("--depth", "1", "--no-single-branch")
        code, _, _ = self.run_script(clone, "--strict")
        self.assertEqual(code, 1)

    def test_fetch_deepens_a_shallow_clone(self):
        clone = self.clone("--depth", "1", "--no-single-branch")
        code, out, _ = self.run_script(clone, "--fetch")
        self.assertEqual(code, 0)
        self.assertNotIn("skipped", out)
        self.assertIn("2 open branch(es)", out)

    def test_fetch_brings_every_branch_into_a_single_branch_clone(self):
        clone = self.clone("--single-branch", "--branch", "main")
        _, out, _ = self.run_script(clone)
        self.assertIn("main has everything", out)  # nothing known yet
        _, out, _ = self.run_script(clone, "--fetch")
        self.assertIn("feature-a", out)
        self.assertIn("feature-b", out)

    def test_failed_fetch_is_not_fatal(self):
        clone = self.clone()
        git(clone, "remote", "set-url", "origin", str(self.tmp / "gone.git"))
        code, out, err = self.run_script(clone, "--fetch")
        self.assertEqual(code, 0)
        self.assertIn("fetch failed", err)
        self.assertIn("2 open branch(es)", out)

    def test_no_origin_main(self):
        lonely = pathlib.Path(tempfile.mkdtemp(dir=self.tmp))
        git(lonely, "init", "-q", "-b", "main")
        code, _, err = self.run_script(lonely)
        self.assertEqual(code, 0)
        self.assertIn("not found", err)


class TestHelpers(unittest.TestCase):
    def test_parse_iso_strict_with_offset(self):
        self.assertEqual(bo.parse_date("2030-01-02T03:04:05+02:00").isoformat(),
                         "2030-01-02T03:04:05+02:00")

    def test_parse_iso_strict_with_z(self):
        self.assertEqual(bo.parse_date("2030-01-02T03:04:05Z").utcoffset().seconds, 0)

    def test_parse_garbage(self):
        self.assertIsNone(bo.parse_date("yesterday"))

    def test_noise(self):
        self.assertTrue(bo.noisy("00-system/learning/observations/2030-01.md"))
        self.assertFalse(bo.noisy("03-projects/x.md"))


if __name__ == "__main__":
    unittest.main()
