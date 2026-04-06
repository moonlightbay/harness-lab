from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "id",
    "description",
    "detection_hint",
    "remediation_hint",
    "rerun_hint",
]


def main() -> int:
    repo_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    rules_path = repo_root / "checks" / "architecture-rules.json"

    if not rules_path.exists():
        print(json.dumps({"verdict": "fail", "summary": {"valid_rule_count": 0, "invalid_rule_count": 1}, "details": ["Missing checks/architecture-rules.json"]}, indent=2))
        return 1

    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    invalid_rules = []
    valid_count = 0

    for index, rule in enumerate(rules):
        missing = [field for field in REQUIRED_FIELDS if not str(rule.get(field, "")).strip()]
        if missing:
            invalid_rules.append({"rule_index": index, "missing_fields": missing})
        else:
            valid_count += 1

    result = {
        "verdict": "pass" if valid_count >= 1 and not invalid_rules else "fail",
        "summary": {
            "rule_count": len(rules),
            "valid_rule_count": valid_count,
            "invalid_rule_count": len(invalid_rules),
        },
        "invalid_rules": invalid_rules,
    }

    print(json.dumps(result, indent=2))
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
