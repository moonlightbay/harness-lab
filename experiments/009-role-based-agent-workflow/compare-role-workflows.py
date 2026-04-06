from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    artifacts_root = experiment_root / "artifacts"

    single = load_json(artifacts_root / "single-generalist-score.json")
    role_based = load_json(artifacts_root / "role-based-score.json")

    single_product = single["product"]["total"]["score"]
    role_product = role_based["product"]["total"]["score"]
    single_audit = single["auditability"]["summary"]["passed"]
    role_audit = role_based["auditability"]["summary"]["passed"]

    if role_product > single_product:
        verdict = "role-based-better-on-product-and-auditability"
    elif role_product == single_product and role_audit > single_audit:
        if role_based["telemetry"]["input_tokens"] > single["telemetry"]["input_tokens"]:
            verdict = "role-division-improves-auditability-at-higher-cost"
        else:
            verdict = "role-division-improves-auditability"
    elif role_product < single_product:
        verdict = "single-agent-better-on-product"
    else:
        verdict = "inconclusive"

    result = {
        "single_generalist": single,
        "role_based": role_based,
        "deltas": {
            "product_score": role_product - single_product,
            "auditability_score": role_audit - single_audit,
            "session_count": role_based["telemetry"]["session_count"] - single["telemetry"]["session_count"],
            "turn_count": role_based["telemetry"]["turn_count"] - single["telemetry"]["turn_count"],
            "input_tokens": role_based["telemetry"]["input_tokens"] - single["telemetry"]["input_tokens"],
            "output_tokens": role_based["telemetry"]["output_tokens"] - single["telemetry"]["output_tokens"],
        },
        "verdict": verdict,
        "recommendation": "Use role-divided workflows when audit trail and review traceability matter more than raw token efficiency; keep a single generalist path for small low-risk tasks.",
    }

    (artifacts_root / "role-workflow-comparison.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
