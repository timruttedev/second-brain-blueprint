"""Tests for the YAML subset loader.

Run from the repository root:
    python3 -m unittest discover -s 00-system/scripts -t 00-system/scripts
"""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import miniyaml  # noqa: E402


class TestScalars(unittest.TestCase):
    def test_plain_mapping(self):
        self.assertEqual(miniyaml.loads("a: 1\nb: two"), {"a": 1, "b": "two"})

    def test_types(self):
        got = miniyaml.loads("i: -3\nt: true\nf: false\nn: null\ne: ~")
        self.assertEqual(got, {"i": -3, "t": True, "f": False, "n": None, "e": None})

    def test_quotes_keep_special_characters(self):
        got = miniyaml.loads('a: "**/*.en.ts"\nb: \'x: y\'')
        self.assertEqual(got, {"a": "**/*.en.ts", "b": "x: y"})

    def test_value_may_contain_a_colon(self):
        got = miniyaml.loads("url: https://example.com/owner\nanchor: a.md#current-state")
        self.assertEqual(got["url"], "https://example.com/owner")
        self.assertEqual(got["anchor"], "a.md#current-state")

    def test_comments_are_dropped_but_not_inside_quotes(self):
        got = miniyaml.loads('# lead\na: 1  # trailing\nb: "x # y"')
        self.assertEqual(got, {"a": 1, "b": "x # y"})

    def test_leading_document_brandr(self):
        self.assertEqual(miniyaml.loads("---\na: 1"), {"a": 1})


class TestStructure(unittest.TestCase):
    def test_nested_mapping(self):
        got = miniyaml.loads("outer:\n  inner:\n    leaf: 1\n")
        self.assertEqual(got, {"outer": {"inner": {"leaf": 1}}})

    def test_sequence_of_scalars(self):
        got = miniyaml.loads("relevant:\n  - src/**\n  - docs/**\n")
        self.assertEqual(got, {"relevant": ["src/**", "docs/**"]})

    def test_sequence_of_mappings(self):
        src = (
            "projects:\n"
            "  - project: a\n"
            "    kind: brand\n"
            "    relevant:\n"
            "      - src/**\n"
            "  - project: b\n"
            "    kind: product\n"
        )
        got = miniyaml.loads(src)
        self.assertEqual(
            got,
            {
                "projects": [
                    {"project": "a", "kind": "brand", "relevant": ["src/**"]},
                    {"project": "b", "kind": "product"},
                ]
            },
        )

    def test_top_level_sequence(self):
        got = miniyaml.loads("- project: a\n  kind: brand\n- project: b\n")
        self.assertEqual(got, [{"project": "a", "kind": "brand"}, {"project": "b"}])

    def test_mapping_of_sequences(self):
        src = "routing:\n  pricing:\n    - a.md#x\n    - b.md#y\n  seo:\n    - c.md#z\n"
        got = miniyaml.loads(src)
        self.assertEqual(got, {"routing": {"pricing": ["a.md#x", "b.md#y"], "seo": ["c.md#z"]}})

    def test_key_without_value_is_none(self):
        self.assertEqual(miniyaml.loads("a:\nb: 1"), {"a": None, "b": 1})

    def test_empty_document(self):
        self.assertIsNone(miniyaml.loads("# nothing\n\n"))


class TestRejections(unittest.TestCase):
    def assertRejected(self, src, needle):
        with self.assertRaises(miniyaml.YamlError) as ctx:
            miniyaml.loads(src)
        self.assertIn(needle, str(ctx.exception))

    def test_tab_indentation(self):
        self.assertRejected("a:\n\tb: 1\n", "tabs")

    def test_anchor(self):
        self.assertRejected("a: &ref 1\n", "anchors")

    def test_flow_collection(self):
        self.assertRejected("a: [1, 2]\n", "flow collections")

    def test_block_scalar(self):
        self.assertRejected("a: |\n  text\n", "block scalars")

    def test_duplicate_key(self):
        self.assertRejected("a: 1\na: 2\n", "duplicate key")

    def test_second_document(self):
        self.assertRejected("a: 1\n---\nb: 2\n", "single document")

    def test_garbage_line(self):
        self.assertRejected("a: 1\nnonsense\n", "expected 'key: value'")

    def test_error_names_the_line(self):
        with self.assertRaises(miniyaml.YamlError) as ctx:
            miniyaml.loads("a: 1\nb: 2\nc: [3]\n")
        self.assertIn("line 3", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
