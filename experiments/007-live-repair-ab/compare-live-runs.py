from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    artifacts_root = experiment_root / "artifacts"

    generic = load_json(artifacts_root / "generic-check-score.json")
    remediation = load_json(artifacts_root / "remediation-check-score.json")

    generic_score = generic["total"]["score"]
    remediation_score = remediation["total"]["score"]

    if remediation_score > generic_score:
        verdict = "remediation-check-wins-on-outcome"
    elif remediation_score < generic_score:
        verdict = "generic-check-wins-on-outcome"
    else:
        generic_cost = {
            "turn_count": generic["telemetry"]["turn_count"],
            "input_tokens": generic["telemetry"]["input_tokens"],
            "output_tokens": generic["telemetry"]["output_tokens"],
            "changed_file_count": generic["changed_file_count"],
        }
        remediation_cost = {
            "turn_count": remediation["telemetry"]["turn_count"],
            "input_tokens": remediation["telemetry"]["input_tokens"],
            "output_tokens": remediation["telemetry"]["output_tokens"],
            "changed_file_count": remediation["changed_file_count"],
        }

        remediation_no_worse = all(
            remediation_cost[key] <= generic_cost[key] for key in remediation_cost
        )
        remediation_strictly_better = any(
            remediation_cost[key] < generic_cost[key] for key in remediation_cost
        )
        generic_no_worse = all(
            generic_cost[key] <= remediation_cost[key] for key in generic_cost
        )
        generic_strictly_better = any(
            generic_cost[key] < remediation_cost[key] for key in generic_cost
        )

        if remediation_no_worse and remediation_strictly_better:
            verdict = "remediation-check-wins-on-cost"
        elif generic_no_worse and generic_strictly_better:
            verdict = "generic-check-wins-on-cost"
        else:
            verdict = "inconclusive"

    result = {
        "generic_check": generic,
        "remediation_check": remediation,
        "deltas": {
            "total_score": remediation_score - generic_score,
            "turn_count": remediation["telemetry"]["turn_count"] - generic["telemetry"]["turn_count"],
            "input_tokens": remediation["telemetry"]["input_tokens"] - generic["telemetry"]["input_tokens"],
            "output_tokens": remediation["telemetry"]["output_tokens"] - generic["telemetry"]["output_tokens"],
            "changed_file_count": remediation["changed_file_count"] - generic["changed_file_count"],
        },
        "verdict": verdict,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
