from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_score(script_path: Path, package_root: Path, spec_path: Path) -> dict:
    completed = subprocess.run(
        [sys.executable, str(script_path), str(package_root), str(spec_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    packages_root = experiment_root / "packages"
    spec_path = experiment_root / "fixtures" / "violation-spec.json"
    artifacts_root = experiment_root / "artifacts"
    artifacts_root.mkdir(parents=True, exist_ok=True)

    score_script = experiment_root / "score-feedback-package.py"
    package_scores: dict[str, dict] = {}

    for package_root in sorted(path for path in packages_root.iterdir() if path.is_dir()):
        score = run_score(score_script, package_root, spec_path)
        package_scores[package_root.name] = score
        score_path = artifacts_root / f"{package_root.name}-score.json"
        score_path.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")

    ranking = sorted(
        (
            {
                "name": name,
                "score": result["summary"]["score"],
                "max": result["summary"]["max"],
                "origin": result["metadata"]["origin"],
            }
            for name, result in package_scores.items()
        ),
        key=lambda item: item["score"],
        reverse=True,
    )

    verdict = "remediation-oriented-check-is-most-loop-ready"
    if ranking[0]["name"] != "failing-check-remediation":
        verdict = "unexpected-top-ranked-package"
    elif ranking[-1]["name"] != "docs-only":
        verdict = "docs-only-did-not-rank-last"

    comparison = {
        "packages": package_scores,
        "ranking": ranking,
        "deltas": {
            "remediation-vs-docs-only": package_scores["failing-check-remediation"]["summary"]["score"]
            - package_scores["docs-only"]["summary"]["score"],
            "remediation-vs-review-comment": package_scores["failing-check-remediation"]["summary"]["score"]
            - package_scores["review-comment"]["summary"]["score"],
            "remediation-vs-generic-check": package_scores["failing-check-remediation"]["summary"]["score"]
            - package_scores["failing-check-generic"]["summary"]["score"],
        },
        "verdict": verdict,
        "recommendation": "Encode stable invariants as failing checks, and prefer remediation-oriented output over requirement-only guidance or bare generic failures.",
    }

    output_path = artifacts_root / "feedback-representation-comparison.json"
    output_path.write_text(json.dumps(comparison, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(comparison, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
