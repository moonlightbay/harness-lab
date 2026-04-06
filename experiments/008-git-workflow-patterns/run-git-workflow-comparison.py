from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def copy_template(src: Path, dst: Path) -> None:
    shutil.copytree(src, dst)


def init_repo(repo_root: Path, base_branch: str) -> None:
    run(["git", "init", "-q"], repo_root)
    run(["git", "config", "user.name", "harness-lab"], repo_root)
    run(["git", "config", "user.email", "lab@example.invalid"], repo_root)
    run(["git", "add", "."], repo_root)
    run(["git", "commit", "-qm", "base fixture"], repo_root)
    run(["git", "branch", "-M", base_branch], repo_root)


def apply_task(workspace_root: Path, task: dict) -> None:
    readme_path = workspace_root / "README.md"
    code_path = workspace_root / task["code_file"]

    readme = readme_path.read_text(encoding="utf-8").rstrip() + "\n"
    readme += f"\n- {task['readme_marker']}\n"
    readme_path.write_text(readme, encoding="utf-8")

    code = code_path.read_text(encoding="utf-8").rstrip() + task["code_snippet"]
    code_path.write_text(code + "\n", encoding="utf-8")


def collect_context(
    workspace_root: Path,
    context_name: str,
    assigned_tasks: list[str],
    task_markers: dict[str, str],
) -> dict:
    changed_files = [
        line
        for line in run(["git", "diff", "--name-only"], workspace_root).splitlines()
        if line.strip()
    ]
    status = [
        line
        for line in run(["git", "status", "--short"], workspace_root).splitlines()
        if line.strip()
    ]
    readme_content = (workspace_root / "README.md").read_text(encoding="utf-8")
    present_markers = [
        task_id for task_id, marker in task_markers.items() if marker in readme_content
    ]
    return {
        "context_name": context_name,
        "branch": run(["git", "branch", "--show-current"], workspace_root),
        "assigned_tasks": assigned_tasks,
        "changed_files": sorted(changed_files),
        "status": status,
        "present_readme_markers": sorted(present_markers),
    }


def load_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_nested_scenario(temp_root: Path, template_root: Path, spec: dict) -> dict:
    repo_root = temp_root / "nested-repo"
    copy_template(template_root, repo_root)
    init_repo(repo_root, spec["base_branch"])
    run(["git", "checkout", "-qb", spec["nested_branch"]], repo_root)

    apply_task(repo_root, spec["tasks"]["task_a"])
    apply_task(repo_root, spec["tasks"]["task_b"])

    task_markers = {
        task_id: task["readme_marker"] for task_id, task in spec["tasks"].items()
    }
    context = collect_context(
        repo_root,
        context_name="combined-workspace",
        assigned_tasks=["task_a", "task_b"],
        task_markers=task_markers,
    )

    return {
        "scenario": "nested-single-branch",
        "base_branch": spec["base_branch"],
        "contexts": [context],
    }


def build_worktree_scenario(temp_root: Path, template_root: Path, spec: dict) -> dict:
    repo_root = temp_root / "worktree-repo"
    copy_template(template_root, repo_root)
    init_repo(repo_root, spec["base_branch"])

    task_markers = {
        task_id: task["readme_marker"] for task_id, task in spec["tasks"].items()
    }
    contexts = []

    for task_id, task in spec["tasks"].items():
        run(["git", "branch", task["branch"], spec["base_branch"]], repo_root)
        workspace_root = temp_root / task["workspace"]
        run(["git", "worktree", "add", "-q", str(workspace_root), task["branch"]], repo_root)
        apply_task(workspace_root, task)
        contexts.append(
            collect_context(
                workspace_root,
                context_name=task["workspace"],
                assigned_tasks=[task_id],
                task_markers=task_markers,
            )
        )

    return {
        "scenario": "branch-per-task-worktrees",
        "base_branch": spec["base_branch"],
        "contexts": contexts,
    }


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    artifacts_root = experiment_root / "artifacts"
    artifacts_root.mkdir(parents=True, exist_ok=True)

    spec = load_spec(experiment_root / "workflow-spec.json")
    template_root = experiment_root / "fixtures" / "repo-template"

    with tempfile.TemporaryDirectory(prefix="exp008-") as temp_dir:
        temp_root = Path(temp_dir)
        nested = build_nested_scenario(temp_root, template_root, spec)
        worktree = build_worktree_scenario(temp_root, template_root, spec)

    (artifacts_root / "nested-scenario.json").write_text(
        json.dumps(nested, indent=2) + "\n",
        encoding="utf-8",
    )
    (artifacts_root / "worktree-scenario.json").write_text(
        json.dumps(worktree, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "nested": nested,
                "worktree": worktree,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
