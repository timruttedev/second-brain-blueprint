"""Tests for init.py.

Run from the repository root:
    python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts

init.py rewrites a whole repository in one go, so every test runs it on a
copy: a small synthetic repository for exact expectations, and one full
copy of this repository to prove it works on the real thing.
"""

import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))

import init  # noqa: E402

ARGS = ["--name", "Alex Morgan", "--language", "English",
        "--timezone", "Europe/Berlin"]


def snapshot(root):
    """{relative path: hash} of every file, to prove nothing changed."""
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run(root, *args):
    r = subprocess.run([sys.executable, str(root / "00-system/scripts/init.py"), *args],
                       cwd=root, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout, r.stderr


class Synthetic(unittest.TestCase):
    """A minimal repository with one example of everything init touches."""

    FILES = {
        "AGENTS.md": "# Agents\n\nOwner: <OWNER_NAME>, speaks <OWNER_LANGUAGE>.\n",
        "GETTING-STARTED.md": (
            "# Getting started\n\nReplace <OWNER_NAME> via init.py.\n\n"
            "<!-- blueprint-only:start -->\nBlueprint text.\n"
            "<!-- blueprint-only:end -->\n\nStays.\n"),
        "README.md": "# The blueprint\n",
        "CHANGELOG.md": "# Changelog\n",
        "CONTRIBUTING.md": "# Contributing\n",
        "SECURITY.md": "# Security\n",
        "00-system/templates/README.owner.md": "# <OWNER_NAME>'s Second Brain\n",
        "00-system/current-context.md": (
            "---\ntype: system\nupdated: YYYY-MM-DD\n---\n\n# Current Context\n"
            "\n- `<OWNER_NAME>`: ...\n"),
        "00-system/indexes/projects.md": (
            "---\ncreated: YYYY-MM-DD\n---\n\n# Projects\n\n"
            "Format: `- YYYY-MM-DD: note`\n"),
        "00-system/workflows/reviews.md": (
            "# Reviews\n\nRuns at 07:00 <TIMEZONE>.\n\n```\nupdated: YYYY-MM-DD\n```\n"
            "\n```\n<!-- blueprint-only:start -->\nshown as an example\n"
            "<!-- blueprint-only:end -->\n```\n"),
        # canary.md links here
        "00-system/learning/patterns.md": (
            "# Patterns\n\n## A check that silently reports green is worse than none\n"),
        "examples/README.md": "# Example\n",
        ".github/workflows/checks.yml": "name: checks\n",
        ".github/ISSUE_TEMPLATE/bug.md": "bug\n",
        ".github/PULL_REQUEST_TEMPLATE.md": "pr\n",
    }

    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp())
        scripts = self.root / "00-system" / "scripts"
        scripts.mkdir(parents=True)
        for name in ("init.py", "linkcheck.py", "canary.md"):
            shutil.copy(HERE / name, scripts / name)
        for name, text in self.FILES.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def read(self, name):
        return (self.root / name).read_text(encoding="utf-8")

    def test_placeholders_replaced(self):
        code, out, err = run(self.root, *ARGS)
        self.assertEqual(code, 0, out + err)
        self.assertEqual(self.read("AGENTS.md"),
                         "# Agents\n\nOwner: Alex Morgan, speaks English.\n")
        self.assertIn("07:00 Europe/Berlin", self.read("00-system/workflows/reviews.md"))
        self.assertIn("Next steps", out)

    def test_getting_started_keeps_placeholders_but_loses_blocks(self):
        run(self.root, *ARGS)
        text = self.read("GETTING-STARTED.md")
        self.assertIn("<OWNER_NAME>", text)
        self.assertNotIn("Blueprint text", text)
        self.assertNotIn("blueprint-only", text)
        self.assertIn("Stays.", text)

    def test_dates_only_in_context_and_indexes(self):
        run(self.root, *ARGS)
        today = init.today_in("Europe/Berlin").isoformat()
        self.assertIn(f"updated: {today}", self.read("00-system/current-context.md"))
        projects = self.read("00-system/indexes/projects.md")
        self.assertIn(f"created: {today}", projects)
        self.assertIn("`- YYYY-MM-DD: note`", projects)
        self.assertIn("updated: YYYY-MM-DD", self.read("00-system/workflows/reviews.md"))

    def test_markers_inside_code_fence_stay(self):
        run(self.root, *ARGS)
        self.assertIn("shown as an example", self.read("00-system/workflows/reviews.md"))

    def test_readme_replaced(self):
        run(self.root, *ARGS)
        self.assertEqual(self.read("README.md"), "# Alex Morgan's Second Brain\n")

    def test_blueprint_files_deleted_ci_kept(self):
        run(self.root, *ARGS)
        for name in ("examples", "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md",
                     ".github/ISSUE_TEMPLATE", ".github/PULL_REQUEST_TEMPLATE.md"):
            self.assertFalse((self.root / name).exists(), name)
        self.assertTrue((self.root / ".github/workflows/checks.yml").is_file())
        self.assertTrue((self.root / "00-system/scripts/init.py").is_file())

    def test_keep_examples_keeps_only_examples(self):
        run(self.root, *ARGS, "--keep-examples")
        self.assertTrue((self.root / "examples/README.md").is_file())
        self.assertFalse((self.root / "CHANGELOG.md").exists())

    def test_dry_run_writes_nothing(self):
        before = snapshot(self.root)
        code, out, _ = run(self.root, *ARGS, "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(snapshot(self.root), before)
        self.assertIn("would update  AGENTS.md", out)
        self.assertIn("would delete  examples", out)
        self.assertIn("Dry run", out)

    def test_second_run_refuses_and_force_is_idempotent(self):
        run(self.root, *ARGS)
        after_first = snapshot(self.root)
        code, out, _ = run(self.root, *ARGS)
        self.assertEqual(code, 1)
        self.assertIn("initialized already", out)
        code, out, _ = run(self.root, *ARGS, "--force")
        self.assertEqual(code, 0)
        self.assertEqual(snapshot(self.root), after_first)

    def test_unknown_time_zone_is_refused(self):
        before = snapshot(self.root)
        code, _, err = run(self.root, "--name", "A", "--language", "English",
                           "--timezone", "Mars/Olympus")
        self.assertEqual(code, 2)
        self.assertIn("Unknown time zone", err)
        self.assertEqual(snapshot(self.root), before)

    def test_value_with_angle_bracket_is_refused(self):
        code, _, _ = run(self.root, "--name", "<OWNER_NAME>", "--language", "x",
                         "--timezone", "Europe/Berlin")
        self.assertEqual(code, 2)

    def test_missing_owner_readme_keeps_readme(self):
        (self.root / "00-system/templates/README.owner.md").unlink()
        _, _, err = run(self.root, *ARGS)
        self.assertIn("README.owner.md is missing", err)
        self.assertEqual(self.read("README.md"), "# The blueprint\n")


class TestStripBlueprintOnly(unittest.TestCase):
    def test_block_removed_with_markers(self):
        text, n, unclosed = init.strip_blueprint_only(
            "a\n<!-- blueprint-only:start -->\nb\n<!-- blueprint-only:end -->\nc\n")
        self.assertEqual((text, n, unclosed), ("a\nc\n", 1, False))

    def test_inline_mention_is_not_a_marker(self):
        src = "Use `<!-- blueprint-only:start -->` to mark a block.\n"
        self.assertEqual(init.strip_blueprint_only(src), (src, 0, False))

    def test_unclosed_block_is_left_alone(self):
        src = "a\n<!-- blueprint-only:start -->\nb\n"
        self.assertEqual(init.strip_blueprint_only(src), (src, 0, True))

    def test_tilde_fence_protects_markers(self):
        src = "~~~\n<!-- blueprint-only:start -->\nx\n<!-- blueprint-only:end -->\n~~~\n"
        self.assertEqual(init.strip_blueprint_only(src), (src, 0, False))


class RealCopy(unittest.TestCase):
    """init.py on a full copy of this repository."""

    def setUp(self):
        self.root = pathlib.Path(tempfile.mkdtemp()) / "brain"
        shutil.copytree(REPO, self.root, ignore=shutil.ignore_patterns(
            ".git", "__pycache__"))

    def tearDown(self):
        shutil.rmtree(self.root.parent, ignore_errors=True)

    def test_full_run(self):
        code, out, err = run(self.root, *ARGS)
        # The exit code mirrors linkcheck on the result; other files may be
        # mid-edit, so only the effects are asserted strictly here.
        self.assertIn(code, (0, 1), out + err)
        self.assertIn("Next steps", out)
        left = []
        for path in self.root.rglob("*"):
            if not path.is_file() or path.name in ("GETTING-STARTED.md", "init.py",
                                                   "test_init.py"):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            left += [f"{path.relative_to(self.root)}: {p}"
                     for p in init.PLACEHOLDERS if p in text]
        self.assertEqual(left, [])
        self.assertFalse((self.root / "examples").exists())
        context = (self.root / "00-system/current-context.md").read_text(encoding="utf-8")
        self.assertNotIn("updated: YYYY-MM-DD", context)
        owner = self.root / "00-system/templates/README.owner.md"
        if owner.is_file():
            self.assertIn("Alex Morgan", (self.root / "README.md").read_text(encoding="utf-8"))
        code, _, _ = run(self.root, *ARGS)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
