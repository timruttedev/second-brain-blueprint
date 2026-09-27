"""Tests for linkcheck.py.

Run from the repository root:
    python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts

The script is only useful if it does NOT report what is fine: a check with
false alarms gets ignored after the second run. Several anchor rules
(inline code, underscore, emoji) are easy to get wrong, so each one has its
own test here.
"""

import pathlib
import sys
import tempfile
import unittest
from datetime import date, timedelta

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import linkcheck as lc  # noqa: E402


class TempRoot:
    """Point lc.ROOT at a temporary directory for the duration of a test."""

    def __init__(self):
        self.dir = pathlib.Path(tempfile.mkdtemp())

    def __enter__(self):
        self.old = lc.ROOT
        lc.ROOT = self.dir
        return self.dir

    def __exit__(self, *exc):
        lc.ROOT = self.old


class TestSlug(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(lc.slug("## Where the data comes from"),
                         "where-the-data-comes-from")

    def test_non_ascii_letters_stay(self):
        self.assertEqual(lc.slug("### Notes on café culture"),
                         "notes-on-café-culture")

    def test_inline_code_counts_for_the_anchor(self):
        self.assertEqual(lc.slug("### `Unresolved`: open questions"),
                         "unresolved-open-questions")

    def test_underscore_stays(self):
        self.assertEqual(lc.slug("### The `max_lines` field"),
                         "the-max_lines-field")

    def test_emoji_leaves_two_hyphens(self):
        # 'Step 1.2 ⚠️ Setup' -> dot gone, emoji gone, both spaces stay
        self.assertEqual(lc.slug("### Step 1.2 ⚠️ Setup"),
                         "step-12--setup")

    def test_bold_and_link(self):
        self.assertEqual(lc.slug("## **Plan** versus [actual](./x.md)"),
                         "plan-versus-actual")

    def test_duplicate_heading_gets_suffix(self):
        text = "# History\n\n## History\n"
        self.assertEqual(lc.anchors(text), {"history", "history-1"})

    def test_heading_in_code_block_does_not_count(self):
        text = "```bash\n# not an anchor\n```\n\n## Real\n"
        self.assertEqual(lc.anchors(text), {"real"})

    def test_heading_in_tilde_fence_does_not_count(self):
        text = "~~~\n## Format example\n~~~\n\n## Real\n"
        self.assertEqual(lc.anchors(text), {"real"})

    def test_heading_in_html_comment_does_not_count(self):
        text = "<!--\n## Hidden\n-->\n## Real\n"
        self.assertEqual(lc.anchors(text), {"real"})


class TestStripping(unittest.TestCase):
    def test_code_block_is_ignored(self):
        text = "before\n```\n[x](./missing.md)\n```\nafter"
        self.assertEqual([t for _, t in lc.links(text)], [])

    def test_backticks_followed_by_prose_are_not_a_fence(self):
        """A ``` example in the middle of a sentence does not open a block.

        CommonMark: the info string of a ``` fence must not contain another
        backtick. Treating this line as a fence would hide every link in
        the rest of the file.
        """
        text = ("  ```-example that starts with `## YYYY-MM-DD`.\n"
                "[real](./here.md)\n")
        self.assertEqual([t for _, t in lc.links(text)], ["./here.md"])

    def test_fence_with_language_stays_a_fence(self):
        text = "```bash\n[x](./missing.md)\n```\n[real](./here.md)"
        self.assertEqual([t for _, t in lc.links(text)], ["./here.md"])

    def test_file_ending_inside_code_block_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / "open.md"
            path.write_text("Text\n\n```\ncode\n\nmore\n", encoding="utf-8")
            self.assertEqual([(p.name, no) for p, no in lc.open_fences([path])],
                             [("open.md", 3)])

    def test_closed_code_block_is_not_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / "closed.md"
            path.write_text("Text\n\n```\ncode\n```\n\nAfter\n", encoding="utf-8")
            self.assertEqual(lc.open_fences([path]), [])

    def test_inline_code_is_ignored(self):
        text = "Format: `- [name](../../05-people/file.md): relation`"
        self.assertEqual([t for _, t in lc.links(text)], [])

    def test_html_comment_is_ignored(self):
        text = "<!-- superseded by [new](./YYYY-MM-DD-slug.md): reason -->"
        self.assertEqual([t for _, t in lc.links(text)], [])

    def test_multiline_comment_is_ignored(self):
        text = "<!--\n[x](./missing.md)\n-->\n[real](./here.md)"
        self.assertEqual([t for _, t in lc.links(text)], ["./here.md"])

    def test_line_numbers_stay_correct(self):
        text = "```\ncode\n```\n\n[x](./target.md)"
        self.assertEqual(list(lc.links(text)), [(5, "./target.md")])

    def test_external_links_and_images_are_skipped(self):
        text = "[a](https://example.com) ![img](./b.png) [c](mailto:x@example.com)"
        self.assertEqual([t for _, t in lc.links(text)], [])


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.folder = pathlib.Path(tempfile.mkdtemp())
        (self.folder / "target.md").write_text(
            "# Title\n\n## The section\n", encoding="utf-8")

    def _write(self, content):
        path = self.folder / "source.md"
        path.write_text(content, encoding="utf-8")
        return [path]

    def test_valid_link_and_anchor(self):
        files = self._write("[a](./target.md) [b](./target.md#the-section)")
        self.assertEqual(lc.check(files), [])

    def test_missing_file(self):
        files = self._write("[a](./nothere.md)")
        (_, _, target, kind), = lc.check(files)
        self.assertEqual((target, kind), ("./nothere.md", "missing"))

    def test_missing_anchor(self):
        files = self._write("[a](./target.md#other-section)")
        (_, _, _, kind), = lc.check(files)
        self.assertEqual(kind, "anchor")

    def test_anchor_in_same_file(self):
        files = self._write("# Head\n\n[up](#head) [gone](#missing)")
        (_, _, target, kind), = lc.check(files)
        self.assertEqual((target, kind), ("#missing", "anchor"))

    def test_link_to_directory_is_fine(self):
        (self.folder / "subfolder").mkdir()
        files = self._write("[a](./subfolder/)")
        self.assertEqual(lc.check(files), [])

    def test_link_to_non_markdown(self):
        (self.folder / "data.csv").write_text("x", encoding="utf-8")
        files = self._write("[a](./data.csv)")
        self.assertEqual(lc.check(files), [])


class TestCanary(unittest.TestCase):
    """The canary must scream when the check stops checking.

    A run that reports "0 findings" without having found the deliberately
    broken link in `canary.md` did not check the repository; it only looked
    like it did.
    """

    def setUp(self):
        self.path = (lc.ROOT / lc.CANARY).resolve()

    def test_expected_finding_is_removed_and_no_error(self):
        findings = [(self.path, 7, lc.CANARY_TARGET, "missing")]
        real, silent = lc.split_canary(findings, [self.path])
        self.assertEqual(real, [])
        self.assertIsNone(silent)

    def test_missing_finding_is_an_error(self):
        real, silent = lc.split_canary([], [self.path])
        self.assertEqual(real, [])
        self.assertIn("CANARY SILENT", silent)

    def test_other_findings_in_the_canary_are_reported(self):
        other = (self.path, 9, "./also-broken.md", "missing")
        findings = [(self.path, 7, lc.CANARY_TARGET, "missing"), other]
        real, silent = lc.split_canary(findings, [self.path])
        self.assertEqual(real, [other])
        self.assertIsNone(silent)

    def test_single_file_run_does_not_check_the_canary(self):
        other = (lc.ROOT / "AGENTS.md").resolve()
        _, silent = lc.split_canary([], [other])
        self.assertIsNone(silent)

    def test_the_canary_exists_and_carries_its_link(self):
        self.assertTrue(self.path.is_file(), f"{lc.CANARY} is missing")
        self.assertIn(lc.CANARY_TARGET, self.path.read_text(encoding="utf-8"))
        self.assertFalse((self.path.parent / lc.CANARY_TARGET).exists(),
                         "the canary target must not exist")

    def test_real_run_finds_the_canary(self):
        findings = lc.check([self.path])
        self.assertIn(lc.CANARY_TARGET, [f[2] for f in findings])


class TestOrphans(unittest.TestCase):
    def test_path_in_text_counts_as_mention(self):
        # Workflows and templates are named as a path, not linked
        with TempRoot() as root:
            # README is exempt itself, so the test checks only the mention rule
            (root / "README.md").write_text(
                "Use `templates/project.md`.", encoding="utf-8")
            (root / "templates").mkdir()
            (root / "templates" / "project.md").write_text("x", encoding="utf-8")
            (root / "templates" / "unused.md").write_text("x", encoding="utf-8")
            files = sorted(root.rglob("*.md"))
            self.assertEqual([p.name for p in lc.orphans(files)], ["unused.md"])

    def test_examples_take_no_part(self):
        # Neither reported as orphans, nor able to hide a real orphan.
        with TempRoot() as root:
            (root / "examples" / "06-knowledge").mkdir(parents=True)
            (root / "examples" / "06-knowledge" / "sample.md").write_text(
                "See `lonely.md` and `06-knowledge/lonely.md`.", encoding="utf-8")
            (root / "06-knowledge").mkdir()
            (root / "06-knowledge" / "lonely.md").write_text("a", encoding="utf-8")
            files = sorted(root.rglob("*.md"))
            self.assertEqual([lc.relative(p) for p in lc.orphans(files)],
                             ["06-knowledge/lonely.md"])

    def test_readme_and_journal_are_not_orphans(self):
        with TempRoot() as root:
            (root / "02-journal").mkdir()
            (root / "README.md").write_text("[x](./linked.md)", encoding="utf-8")
            (root / "linked.md").write_text("a", encoding="utf-8")
            (root / "lonely.md").write_text("a", encoding="utf-8")
            (root / "02-journal" / "2030-01-01.md").write_text("a", encoding="utf-8")
            files = sorted(root.rglob("*.md"))
            self.assertEqual([p.name for p in lc.orphans(files)], ["lonely.md"])


class TestTypes(unittest.TestCase):
    """The value only counts in the frontmatter.

    The taxonomy table, examples and YAML blocks in text contain plenty of
    'type:' lines. Counting them would flag every file that writes about
    the schema, and the check would be switched off after the first run.
    """

    def write(self, text):
        path = pathlib.Path(tempfile.mkdtemp()) / "x.md"
        path.write_text(text, encoding="utf-8")
        return [path]

    def test_allowed_type_is_silent(self):
        self.assertEqual(lc.types(self.write("---\ntype: area\n---\n\n# A\n")), [])

    def test_invented_type_is_reported(self):
        findings = lc.types(self.write("---\ntype: work-context\n---\n\n# A\n"))
        self.assertEqual([(no, v) for _, no, v in findings], [(2, "work-context")])

    def test_line_number_with_fields_before(self):
        files = self.write("---\ncreated: 2030-01-01\ntype: area-note\n---\n\n# A\n")
        self.assertEqual([no for _, no, _ in lc.types(files)], [3])

    def test_type_in_body_text_does_not_count(self):
        files = self.write("---\ntype: area\n---\n\n| type: nonsense | x |\n")
        self.assertEqual(lc.types(files), [])

    def test_type_in_code_block_does_not_count(self):
        files = self.write("---\ntype: area\n---\n\n```yaml\ntype: nonsense\n```\n")
        self.assertEqual(lc.types(files), [])

    def test_no_frontmatter_is_silent(self):
        self.assertEqual(lc.types(self.write("# Only a heading\n\ntype: x\n")), [])

    def test_taxonomy_itself_is_exempt(self):
        with TempRoot() as root:
            (root / "00-system").mkdir()
            path = root / "00-system" / "taxonomy.md"
            path.write_text("---\ntype:        # one type from the table above\n---\n",
                            encoding="utf-8")
            self.assertEqual(lc.types([path]), [])

    def test_path_outside_root_does_not_crash(self):
        files = self.write("---\ntype: invented\n---\n")
        findings = lc.types(files)
        self.assertEqual(len(findings), 1)
        self.assertEqual(lc.relative(findings[0][0]), files[0].as_posix())

    def test_empty_type_does_not_swallow_next_line(self):
        files = self.write("---\ntype:\nstatus: active\n---\n")
        self.assertEqual(lc.types(files), [])


class TestFrontmatter(unittest.TestCase):
    """Status values and field names, same false-alarm trap as types().

    Every documented status vocabulary must stay silent, not only the base
    one: decisions use `accepted`, which the base vocabulary lacks.
    """

    def write(self, text):
        path = pathlib.Path(tempfile.mkdtemp()) / "x.md"
        path.write_text(text, encoding="utf-8")
        return [path]

    def test_base_vocabulary_is_silent(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: project\nstatus: active\n---\n")), [])

    def test_decision_accepted_is_silent(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: decision\nstatus: accepted\n---\n")), [])

    def test_automated_capture_with_source_is_silent(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: capture\nsource: mail\n---\n")), [])

    def test_comment_after_value_does_not_count(self):
        # The decision template lists its vocabulary after the value.
        self.assertEqual(lc.frontmatter(self.write(
            "---\nstatus: accepted   # proposed | accepted | superseded\n---\n")), [])

    def test_unknown_status_is_reported(self):
        files = self.write("---\ntype: knowledge\nstatus: current\n---\n")
        self.assertEqual([(no, k, v) for _, no, k, v in lc.frontmatter(files)],
                         [(3, "status", "current")])

    def test_unknown_field_is_reported(self):
        files = self.write("---\ntype: area\nemployer: Example Corp\n---\n")
        self.assertEqual([(no, k, v) for _, no, k, v in lc.frontmatter(files)],
                         [(3, "field", "employer")])

    def test_documented_extra_fields_are_silent(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: project\narchived: 2030-01-01\nmax_lines: 80\n---\n")), [])

    def test_field_in_body_text_does_not_count(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: area\n---\n\nemployer: only in the text\n")), [])

    def test_indented_line_is_not_a_key(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: area\nscope:\n  - one\n  - two\n---\n")), [])

    def test_claude_directory_is_exempt(self):
        with TempRoot() as root:
            (root / ".claude" / "skills").mkdir(parents=True)
            path = root / ".claude" / "skills" / "SKILL.md"
            path.write_text("---\nname: brain-triage\ndescription: x\n---\n",
                            encoding="utf-8")
            self.assertEqual(lc.frontmatter([path]), [])

    def test_known_sensitivities_are_silent(self):
        for level in ("public", "private", "confidential", "restricted"):
            with self.subTest(level=level):
                self.assertEqual(lc.frontmatter(self.write(
                    f"---\ntype: person\nsensitivity: {level}\n---\n")), [])

    def test_unknown_sensitivity_is_reported(self):
        files = self.write("---\ntype: person\nsensitivity: secret\n---\n")
        self.assertEqual([(no, k, v) for _, no, k, v in lc.frontmatter(files)],
                         [(3, "sensitivity", "secret")])

    def test_sensitivity_in_body_does_not_count(self):
        self.assertEqual(lc.frontmatter(self.write(
            "---\ntype: area\n---\n\nsensitivity: whatever\n")), [])

    def test_github_directory_is_exempt(self):
        with TempRoot() as root:
            (root / ".github" / "ISSUE_TEMPLATE").mkdir(parents=True)
            path = root / ".github" / "ISSUE_TEMPLATE" / "bug.md"
            path.write_text("---\nname: Bug\nabout: x\ntype: bug\n---\n",
                            encoding="utf-8")
            self.assertEqual(lc.frontmatter([path]), [])
            self.assertEqual(lc.types([path]), [])

    def test_several_findings_in_one_file(self):
        files = self.write("---\nstatus: nonsense\ninvented: yes\n---\n")
        self.assertEqual(len(lc.frontmatter(files)), 2)


class TestLineBudgets(unittest.TestCase):
    """Only the frontmatter field counts, never a sentence in the text."""

    def write(self, text):
        path = pathlib.Path(tempfile.mkdtemp()) / "x.md"
        path.write_text(text, encoding="utf-8")
        return [path]

    def test_no_field_is_silent(self):
        self.assertEqual(lc.line_budgets(self.write(
            "---\ntype: system\n---\n\n# A\n\nlots of text\n")), [])

    def test_within_budget_is_silent(self):
        self.assertEqual(lc.line_budgets(self.write(
            "---\ntype: system\nmax_lines: 130\n---\n\n# A\n")), [])

    def test_over_budget_is_reported(self):
        findings = lc.line_budgets(self.write(
            "---\ntype: system\nmax_lines: 5\n---\n\n# A\n" + "x\n" * 10))
        self.assertEqual([(b, a) for _, b, a in findings], [(5, 16)])

    def test_exactly_on_budget_is_silent(self):
        self.assertEqual(lc.line_budgets(self.write(
            "---\nmax_lines: 6\n---\n" + "x\n" * 3)), [])

    def test_prose_line_does_not_count(self):
        self.assertEqual(lc.line_budgets(self.write(
            "---\ntype: system\n---\n\nBudget: max_lines: 3 in the text.\n"
            + "x\n" * 20)), [])

    def test_no_frontmatter_is_silent(self):
        self.assertEqual(lc.line_budgets(self.write(
            "# A\n\nmax_lines: 2\n" + "x\n" * 20)), [])

    def test_nonsense_value_does_not_crash(self):
        self.assertEqual(lc.line_budgets(self.write(
            "---\nmax_lines: soon\n---\n" + "x\n" * 20)), [])


class TestDueEvaluations(unittest.TestCase):
    """Organization log: an open evaluation needs a date.

    The two costly cases have their own tests: a date in the prose is not a
    deadline (otherwise the check flags entries that never got one), and an
    entry without any date must not stay silent forever (otherwise the rule
    is just a sentence again).
    """

    ENTRY = ("## 2030-01-06: Title\n\n"
             "Observation: something\n"
             "Change:      something\n"
             "Reason:      something\n"
             "Result:      {}\n"
             "Reversible:  yes\n")

    def setUp(self):
        self.root = TempRoot()
        self.folder = self.root.__enter__()
        (self.folder / "00-system" / "learning" / "organization-log").mkdir(parents=True)

    def tearDown(self):
        self.root.__exit__()

    def write(self, text, name="2030-01.md"):
        path = self.folder / "00-system" / "learning" / "organization-log" / name
        path.write_text(text, encoding="utf-8")
        return [path]

    def test_closed_evaluation_is_silent(self):
        files = self.write(self.ENTRY.format("**Keep**, confirmed."))
        self.assertEqual(lc.due_evaluations(files, today=date(2030, 6, 1)), [])

    def test_passed_review_date_is_reported(self):
        files = self.write(self.ENTRY.format("_open, review on 2030-01-20._"))
        findings = lc.due_evaluations(files, today=date(2030, 1, 21))
        self.assertEqual([f[2] for f in findings],
                         ["review date 2030-01-20 passed"])

    def test_future_review_date_is_silent(self):
        files = self.write(self.ENTRY.format("_open, review on 2030-02-01._"))
        self.assertEqual(lc.due_evaluations(files, today=date(2030, 1, 22)), [])

    def test_date_before_heading_is_not_a_deadline(self):
        files = self.write(self.ENTRY.format(
            "_open. Tried once on 2030-01-06, check at the next optimize run._"))
        self.assertEqual(lc.due_evaluations(files, today=date(2030, 1, 22)), [])

    def test_no_date_is_reported_after_grace_period(self):
        files = self.write(self.ENTRY.format("_open, check at the next review._"))
        late = date(2030, 1, 6) + timedelta(days=lc.GRACE_DAYS)
        self.assertEqual(lc.due_evaluations(files, today=late - timedelta(days=1)), [])
        findings = lc.due_evaluations(files, today=late)
        self.assertEqual(len(findings), 1)
        self.assertIn("without a review date", findings[0][2])

    def test_pending_counts_as_open(self):
        files = self.write(self.ENTRY.format("_pending, check at the next review._"))
        self.assertEqual(len(lc.due_evaluations(files, today=date(2030, 3, 1))), 1)

    def test_german_date_is_not_a_deadline(self):
        # Only ISO dates count. A DD.MM.YYYY date is prose, so the entry
        # falls under the grace period instead.
        files = self.write(self.ENTRY.format("_open, review on 20.01.2030._"))
        self.assertEqual(lc.due_evaluations(files, today=date(2030, 1, 21)), [])

    def test_examples_log_is_exempt_unless_asked(self):
        folder = self.folder / "examples" / "00-system" / "learning" / "organization-log"
        folder.mkdir(parents=True)
        path = folder / "2030-01.md"
        path.write_text(self.ENTRY.format("_open, review on 2030-01-20._"),
                        encoding="utf-8")
        self.assertEqual(lc.due_evaluations([path], today=date(2030, 6, 1)), [])
        self.assertEqual(len(lc.due_evaluations(
            [path], today=date(2030, 6, 1), include_examples=True)), 1)

    def test_file_outside_the_log_is_exempt(self):
        path = self.folder / "anything.md"
        path.write_text(self.ENTRY.format("_open._"), encoding="utf-8")
        self.assertEqual(lc.due_evaluations([path], today=date(2030, 6, 1)), [])


class TestSignposts(unittest.TestCase):
    """Dated entries belong in the month files, not in the signposts."""

    def setUp(self):
        self.root = TempRoot()
        self.folder = self.root.__enter__()
        (self.folder / "00-system" / "learning" / "observations").mkdir(parents=True)

    def tearDown(self):
        self.root.__exit__()

    def write(self, rel, text):
        path = self.folder / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return [path]

    def test_dated_heading_in_orglog_signpost_is_reported(self):
        files = self.write("00-system/learning/organization-log.md",
                           "# Organization Log\n\n## 2030-01-06: Moved x\n")
        self.assertEqual([no for _, no in lc.signpost_entries(files)], [3])

    def test_dated_bullet_in_observations_signpost_is_reported(self):
        files = self.write("00-system/learning/observations.md",
                           "# Observations\n\n- 2030-01-15: friction\n")
        self.assertEqual([no for _, no in lc.signpost_entries(files)], [3])

    def test_format_example_in_fence_is_silent(self):
        files = self.write("00-system/learning/organization-log.md",
                           "# Log\n\n```\n## 2030-01-06: example\n```\n"
                           "- `## YYYY-MM-DD` is the heading format\n")
        self.assertEqual(lc.signpost_entries(files), [])

    def test_month_file_is_not_a_signpost(self):
        files = self.write("00-system/learning/observations/2030-01.md",
                           "- 2030-01-15: friction\n")
        self.assertEqual(lc.signpost_entries(files), [])

    def test_examples_signpost_is_checked_too(self):
        files = self.write("examples/00-system/learning/organization-log.md",
                           "## 2030-01-06: Moved x\n")
        self.assertEqual(len(lc.signpost_entries(files)), 1)


class TestCli(unittest.TestCase):
    def test_unknown_flag_is_rejected(self):
        import subprocess
        r = subprocess.run([sys.executable, str(pathlib.Path(lc.__file__)),
                            "--no-such-flag"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("unrecognized arguments", r.stderr)


if __name__ == "__main__":
    unittest.main()
