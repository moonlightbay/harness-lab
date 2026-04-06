from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ROOT = Path(__file__).resolve().parent
SUITE_SPEC_PATH = EXPERIMENT_ROOT / "suite-spec.json"
ARTIFACTS_DIR = EXPERIMENT_ROOT / "artifacts"


def load_json(relative_path: str) -> dict:
    raw_bytes = (ROOT / relative_path).read_bytes()

    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "utf-8"):
        try:
            return json.loads(raw_bytes.decode(encoding))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue

    raise ValueError(f"Could not decode JSON artifact: {relative_path}")


def clamp(value: int, minimum: int = 0, maximum: int = 4) -> int:
    return max(minimum, min(maximum, value))


def classify_recommendation(net_value: int, verdict: str) -> str:
    if verdict == "inconclusive":
        return "needs-more-data"
    if net_value >= 8:
        return "default"
    if "higher-cost" in verdict or "at-higher-cost" in verdict:
        return "conditional"
    if net_value >= 5:
        return "conditional"
    if "improves" in verdict or "better" in verdict:
        return "conditional"
    return "conditional"


def evaluate_short_map(payload: dict) -> dict:
    delta = payload["deltas"]
    primary = 4 if payload["verdict"] == "giant-manual-is-functionally-complete-but-structurally-worse" else 2
    steering = 4 if delta["first_required_mention_line_delta"] >= 100 else 3
    reproducibility = 4
    cost = 0
    notes = [
        f"word_multiplier={delta['word_multiplier']}",
        f"first_required_mention_line_delta={delta['first_required_mention_line_delta']}",
        f"density_delta={delta['density_delta']}",
    ]
    return {
        "preferred_pattern": "short-top-level-map",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_guidance_freshness(payload: dict) -> dict:
    baseline = payload["baseline"]["score"]["total_points"]
    stale = payload["stale_doc"]["score"]["total_points"]
    duplicate = payload["duplicate_guidance"]["score"]["total_points"]
    worst_gap = baseline - min(stale, duplicate)
    primary = 4 if worst_gap >= 6 else 3
    steering = 4
    reproducibility = 4
    cost = 0
    notes = [
        f"baseline_total={baseline}",
        f"stale_doc_total={stale}",
        f"duplicate_guidance_total={duplicate}",
    ]
    return {
        "preferred_pattern": "current-singular-guidance",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_plan_vs_no_plan(payload: dict) -> dict:
    deltas = payload["deltas"]
    primary = 4 if deltas["total"] >= 8 else 3
    steering = 4 if (deltas["restartability"] >= 4 and deltas["auditability"] >= 4) else 3
    reproducibility = 4
    cost = 1
    notes = [
        f"result_quality_delta={deltas['result_quality']}",
        f"restartability_delta={deltas['restartability']}",
        f"auditability_delta={deltas['auditability']}",
        f"total_delta={deltas['total']}",
    ]
    return {
        "preferred_pattern": "checked-in-execution-plan",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_lint_feedback(payload: dict) -> dict:
    deltas = payload["deltas"]
    primary = 3 if deltas["architecture"] >= 3 else 2
    steering = 3 if deltas["architecture"] >= 3 else 2
    reproducibility = 4
    cost = 1
    notes = [
        f"functional_delta={deltas['functional']}",
        f"architecture_delta={deltas['architecture']}",
        f"total_delta={deltas['total']}",
    ]
    return {
        "preferred_pattern": "custom-architecture-rule",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_git_worktree(payload: dict) -> dict:
    primary = 4 if payload["delta"] >= 8 else 3
    steering = 4
    reproducibility = 4
    cost = 1
    notes = [
        f"delta={payload['delta']}",
        "nested_single_branch=0/8",
        "branch_per_task_worktrees=8/8",
    ]
    return {
        "preferred_pattern": "branch-per-task-worktrees",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_role_based_workflow(payload: dict) -> dict:
    deltas = payload["deltas"]
    primary = 0 if deltas["product_score"] == 0 else 2
    steering = 4 if deltas["auditability_score"] >= 5 else 3
    reproducibility = 2
    cost = 4 if deltas["input_tokens"] >= 100000 else 3
    notes = [
        f"product_score_delta={deltas['product_score']}",
        f"auditability_score_delta={deltas['auditability_score']}",
        f"session_count_delta={deltas['session_count']}",
        f"input_tokens_delta={deltas['input_tokens']}",
    ]
    return {
        "preferred_pattern": "role-divided-workflow",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


def evaluate_live_repair_feedback(payload: dict) -> dict:
    deltas = payload["deltas"]
    primary = 0
    steering = 1 if deltas["changed_file_count"] != 0 else 0
    reproducibility = 2
    cost = 2
    notes = [
        f"total_score_delta={deltas['total_score']}",
        f"input_tokens_delta={deltas['input_tokens']}",
        f"output_tokens_delta={deltas['output_tokens']}",
        f"changed_file_count_delta={deltas['changed_file_count']}",
    ]
    return {
        "preferred_pattern": "remediation-oriented-live-feedback",
        "verdict": payload["verdict"],
        "primary_outcome_gain": primary,
        "steering_gain": steering,
        "reproducibility": reproducibility,
        "cost_penalty": cost,
        "notes": notes,
    }


EVALUATORS = {
    "short_map": evaluate_short_map,
    "guidance_freshness": evaluate_guidance_freshness,
    "plan_vs_no_plan": evaluate_plan_vs_no_plan,
    "lint_feedback": evaluate_lint_feedback,
    "git_worktree": evaluate_git_worktree,
    "role_based_workflow": evaluate_role_based_workflow,
    "live_repair_feedback": evaluate_live_repair_feedback,
}


def build_case_result(case_spec: dict) -> dict:
    payload = load_json(case_spec["comparison_artifact"])
    evaluator = EVALUATORS[case_spec["extractor"]]
    scores = evaluator(payload)

    primary = clamp(scores["primary_outcome_gain"])
    steering = clamp(scores["steering_gain"])
    reproducibility = clamp(scores["reproducibility"])
    cost = clamp(scores["cost_penalty"])
    net_value = primary + steering + reproducibility - cost
    recommendation = classify_recommendation(net_value, scores["verdict"])

    return {
        "case_id": case_spec["case_id"],
        "experiment": case_spec["experiment"],
        "layer": case_spec["layer"],
        "pattern": case_spec["pattern"],
        "preferred_pattern": scores["preferred_pattern"],
        "comparison_artifact": case_spec["comparison_artifact"],
        "verdict": scores["verdict"],
        "scores": {
            "primary_outcome_gain": primary,
            "steering_gain": steering,
            "reproducibility": reproducibility,
            "cost_penalty": cost,
            "net_value": net_value,
        },
        "recommendation_tier": recommendation,
        "notes": scores["notes"],
    }


def render_markdown(scoreboard: dict) -> str:
    lines = [
        "# Evaluation Harness Summary",
        "",
        f"Generated at: {scoreboard['generated_at']}",
        "",
        "## Recommendation tiers",
        "",
    ]

    for tier in ("default", "conditional", "needs-more-data"):
        lines.append(f"### {tier}")
        tier_cases = [case for case in scoreboard["cases"] if case["recommendation_tier"] == tier]
        if not tier_cases:
            lines.append("- none")
        else:
            for case in tier_cases:
                scores = case["scores"]
                lines.append(
                    f"- `{case['case_id']}`: net={scores['net_value']} "
                    f"(primary={scores['primary_outcome_gain']}, steering={scores['steering_gain']}, "
                    f"reproducibility={scores['reproducibility']}, cost={scores['cost_penalty']})"
                )
        lines.append("")

    lines.extend(
        [
            "## Ranked cases",
            "",
        ]
    )

    for case in scoreboard["ranked_cases"]:
        scores = case["scores"]
        lines.append(
            f"- `{case['case_id']}` -> `{case['recommendation_tier']}` "
            f"(net={scores['net_value']}, verdict={case['verdict']})"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    spec = json.loads(SUITE_SPEC_PATH.read_text(encoding="utf-8"))
    cases = [build_case_result(case_spec) for case_spec in spec]
    ranked_cases = sorted(cases, key=lambda case: (-case["scores"]["net_value"], case["case_id"]))

    tier_counts = {
        tier: sum(1 for case in cases if case["recommendation_tier"] == tier)
        for tier in ("default", "conditional", "needs-more-data")
    }

    scoreboard = {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "suite_name": "harness-lab-lightweight-scoreboard",
        "case_count": len(cases),
        "tier_counts": tier_counts,
        "cases": cases,
        "ranked_cases": ranked_cases,
    }

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "evaluation-scoreboard.json").write_text(
        json.dumps(scoreboard, indent=2),
        encoding="utf-8",
    )
    (ARTIFACTS_DIR / "evaluation-summary.md").write_text(
        render_markdown(scoreboard),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
