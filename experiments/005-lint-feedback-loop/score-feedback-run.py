from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_json_script(script_path: Path, workspace_root: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(script_path), str(workspace_root)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python score-feedback-run.py <run_root>")

    run_root = Path(sys.argv[1]).resolve()
    workspace_root = run_root / "workspace"

    basic_result = run_json_script(Path(__file__).with_name("verify-basic.py"), workspace_root)
    architecture_result = run_json_script(Path(__file__).with_name("check-architecture.py"), workspace_root)

    total_score = basic_result["summary"]["passed"] + architecture_result["summary"]["passed"]
    total_max = basic_result["summary"]["total"] + architecture_result["summary"]["total"]

    score = {
        "run_root": str(run_root),
        "functional": basic_result,
        "architecture": architecture_result,
        "total": {
            "score": total_score,
            "max": total_max,
        },
    }
    print(json.dumps(score, indent=2))


if __name__ == "__main__":
    main()
