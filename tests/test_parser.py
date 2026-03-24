from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from narrativepulse.parser import parse_text


class ParserTests(unittest.TestCase):
    def test_parse_text_counts(self) -> None:
        parsed = parse_text(
            'Hello world. "We test this."'
        )
        self.assertEqual(parsed.paragraph_count, 1)
        self.assertEqual(parsed.sentence_count, 2)
        self.assertGreaterEqual(parsed.token_count, 4)

    def test_empty_text(self) -> None:
        parsed = parse_text("")
        self.assertEqual(parsed.paragraph_count, 0)
        self.assertEqual(parsed.sentence_count, 0)
        self.assertEqual(parsed.token_count, 0)


if __name__ == "__main__":
    unittest.main()
