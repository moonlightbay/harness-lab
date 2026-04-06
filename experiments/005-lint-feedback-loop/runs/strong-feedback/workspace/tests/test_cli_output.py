from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class CliOutputTests(unittest.TestCase):
    def test_cli_outputs_summary_fields(self) -> None:
        workspace_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "report_app.cli"],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["items"], ["alpha", "beta", "beta", "gamma"])
        self.assertEqual(payload["item_count"], 4)
        self.assertEqual(payload["unique_items"], ["alpha", "beta", "gamma"])
        self.assertEqual(payload["summary_line"], "4 items across 3 unique values")


if __name__ == "__main__":
    unittest.main()
