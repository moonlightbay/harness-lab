from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_spec(experiment_root: Path) -> dict:
    return load_json(experiment_root / "workflow-spec.json")


def find_context_for_task(scenario: dict, task_id: str) -> dict | None:
    for context in scenario["contexts"]:
        if context["assigned_tasks"] == [task_id]:
            return context
    return None


def score_scenario(scenario: dict, spec: dict) -> dict:
    checks = []

    for task_id, task in spec["tasks"].items():
        context = find_context_for_task(scenario, task_id)
        has_dedicated_workspace = context is not None
        checks.append(
            {
                "name": f"{task_id}-dedicated-workspace",
                "passed": has_dedicated_workspace,
                "detail": f"Expected a dedicated workspace for {task_id}.",
            }
        )

        if context is None:
            checks.extend(
                [
                    {
                        "name": f"{task_id}-expected-files-only",
                        "passed": False,
                        "detail": f"No dedicated workspace for {task_id}, so file isolation failed.",
                    },
                    {
                        "name": f"{task_id}-readme-marker-isolated",
                        "passed": False,
                        "detail": f"No dedicated workspace for {task_id}, so README isolation failed.",
                    },
                    {
                        "name": f"{task_id}-review-scope-small",
                        "passed": False,
                        "detail": f"No dedicated workspace for {task_id}, so review scope failed.",
                    },
                ]
            )
            continue

        expected_files = sorted(task["expected_files"])
        changed_files = sorted(context["changed_files"])
        other_task_markers = {
            other_task_id: other_task["readme_marker"]
            for other_task_id, other_task in spec["tasks"].items()
            if other_task_id != task_id
        }
        present_markers = context["present_readme_markers"]

        checks.append(
            {
                "name": f"{task_id}-expected-files-only",
                "passed": changed_files == expected_files,
                "detail": f"Changed files: {changed_files}; expected: {expected_files}",
            }
        )
        checks.append(
            {
                "name": f"{task_id}-readme-marker-isolated",
                "passed": present_markers == [task_id],
                "detail": f"Present README markers: {present_markers}; expected only [{task_id}]",
            }
        )
        checks.append(
            {
                "name": f"{task_id}-review-scope-small",
                "passed": len(changed_files) <= len(expected_files),
                "detail": f"Review scope size: {len(changed_files)}; expected max: {len(expected_files)}",
            }
        )

    passed = sum(1 for check in checks if check["passed"])
    return {
        "scenario": scenario["scenario"],
        "checks": checks,
        "summary": {
            "passed": passed,
            "total": len(checks),
        },
        "contexts": scenario["contexts"],
    }


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    artifacts_root = experiment_root / "artifacts"
    spec = load_spec(experiment_root)
    nested = load_json(artifacts_root / "nested-scenario.json")
    worktree = load_json(artifacts_root / "worktree-scenario.json")

    nested_score = score_scenario(nested, spec)
    worktree_score = score_scenario(worktree, spec)

    result = {
        "nested_single_branch": nested_score,
        "branch_per_task_worktrees": worktree_score,
        "delta": worktree_score["summary"]["passed"] - nested_score["summary"]["passed"],
        "verdict": "worktree-pattern-preserves-task-isolation-better"
        if worktree_score["summary"]["passed"] > nested_score["summary"]["passed"]
        else "inconclusive",
        "recommendation": "Use branch-per-task worktrees when two active tasks must proceed in parallel; avoid stacking unrelated dirty changes in one branch.",
    }

    (artifacts_root / "workflow-comparison.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
