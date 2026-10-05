import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aliasx import build, expand


class Counter:
    def __init__(self):
        self.scanned = 0


class AliasExpandTest(unittest.TestCase):
    def test_literal_words_pass_through(self):
        index = build.build_index({"tp": "teleport"}, {}, None, [])
        out = expand.expand(index, "hello world", "r1", {}, Counter())
        self.assertEqual(out["expanded"], "hello world")
        self.assertTrue(all(t["status"] == "literal" for t in out["tokens"]))

    def test_single_alias_expands(self):
        index = build.build_index({"tp": "teleport"}, {}, None, [])
        out = expand.expand(index, "/tp hi", "r2", {}, Counter())
        self.assertEqual(out["expanded"], "teleport hi")
        self.assertEqual(out["tokens"][0]["status"], "expanded")

    def test_unknown_alias_is_kept(self):
        index = build.build_index({"tp": "teleport"}, {}, None, [])
        out = expand.expand(index, "/zzz a", "r3", {}, Counter())
        self.assertEqual(out["tokens"][0]["status"], "unknown")
        self.assertEqual(out["expanded"], "/zzz a")

    def test_build_puts_aliases_in_index(self):
        index = build.build_index({"tp": "teleport"}, {}, None, [])
        self.assertIn("tp", index["effective"])
        self.assertIn("t", index["trie"])

    def test_empty_line(self):
        index = build.build_index({"tp": "teleport"}, {}, None, [])
        out = expand.expand(index, "", "r5", {}, Counter())
        self.assertEqual(out["expanded"], "")
        self.assertEqual(out["tokens"], [])


if __name__ == "__main__":
    unittest.main()
