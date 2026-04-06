from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


class CliOutputTests(unittest.TestCase):
    def test_cli_outputs_items_and_count(self) -> None:
        workspace_root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, "-m", "report_app.cli"],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(result.stdout)
        self.assertIn("items", payload)
        self.assertIn("item_count", payload)


if __name__ == "__main__":
    unittest.main()
