from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_score(script_path: Path, run_root: Path) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(script_path), str(run_root)],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def main() -> None:
    root = Path(__file__).resolve().parent
    score_script = root / "score-feedback-run.py"
    basic_run = root / "runs" / "basic-feedback"
    strong_run = root / "runs" / "strong-feedback"

    basic_result = run_score(score_script, basic_run)
    strong_result = run_score(score_script, strong_run)

    comparison = {
        "basic_feedback": basic_result,
        "strong_feedback": strong_result,
        "deltas": {
            "functional": strong_result["functional"]["summary"]["passed"] - basic_result["functional"]["summary"]["passed"],
            "architecture": strong_result["architecture"]["summary"]["passed"] - basic_result["architecture"]["summary"]["passed"],
            "total": strong_result["total"]["score"] - basic_result["total"]["score"],
        },
        "verdict": "inconclusive",
    }

    if (
        comparison["deltas"]["functional"] >= 0
        and comparison["deltas"]["architecture"] > 0
        and strong_result["architecture"]["summary"]["passed"] == strong_result["architecture"]["summary"]["total"]
    ):
        comparison["verdict"] = "strong-feedback-loop-preserves-structure-better"

    comparison["recommendation"] = (
        "Keep syntax and tests as the base loop, then add at least one custom architecture rule for agent-facing repos."
        if comparison["verdict"] == "strong-feedback-loop-preserves-structure-better"
        else "Tighten the task or strengthen the architecture rule."
    )

    print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()
