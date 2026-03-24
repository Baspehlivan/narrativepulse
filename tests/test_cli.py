from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
SAMPLE_A = ROOT / "examples" / "sample_a.txt"
SAMPLE_B = ROOT / "examples" / "sample_b.txt"


class CliTests(unittest.TestCase):
    def _env(self) -> dict[str, str]:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        return env

    def test_analyze_command(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "narrativepulse", "analyze", str(SAMPLE_A)],
            capture_output=True,
            text=True,
            check=False,
            env=self._env(),
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("core_metrics:", result.stdout)
        self.assertIn("repetition_hotspots:", result.stdout)

    def test_compare_command(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "narrativepulse",
                "compare",
                str(SAMPLE_A),
                str(SAMPLE_B),
            ],
            capture_output=True,
            text=True,
            check=False,
            env=self._env(),
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("style_similarity:", result.stdout)
        self.assertIn("metric_deltas (A - B):", result.stdout)


if __name__ == "__main__":
    unittest.main()
