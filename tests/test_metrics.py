from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from narrativepulse.metrics import (
    analyze_document,
    compare_documents,
)
from narrativepulse.parser import parse_text


class MetricsTests(unittest.TestCase):
    def test_analyze_document_outputs(self) -> None:
        parsed = parse_text('We write. "We test."')
        metrics = analyze_document(parsed, top=5)
        self.assertGreaterEqual(metrics.lexical_diversity, 0.0)
        self.assertLessEqual(metrics.lexical_diversity, 1.0)
        self.assertGreaterEqual(metrics.dialogue_ratio, 0.0)
        self.assertLessEqual(metrics.dialogue_ratio, 1.0)
        self.assertEqual(len(metrics.style_signature), 4)

    def test_compare_documents_similarity_range(self) -> None:
        parsed_a = parse_text("Short line. Short line.")
        parsed_b = parse_text("Very different wording appears here.")
        comparison = compare_documents(parsed_a, parsed_b, top=5)
        self.assertGreaterEqual(comparison.style_similarity, 0.0)
        self.assertLessEqual(comparison.style_similarity, 1.0)


if __name__ == "__main__":
    unittest.main()
