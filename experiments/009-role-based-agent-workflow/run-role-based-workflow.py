from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import stat
import time
from pathlib import Path


def run_command(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def log(message: str) -> None:
    print(message, flush=True)


def handle_remove_readonly(func, path, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=handle_remove_readonly)


def init_repo(workspace_root: Path) -> None:
    run_command(["git", "init", "-q"], workspace_root)
    run_command(["git", "config", "user.name", "harness-lab"], workspace_root)
    run_command(["git", "config", "user.email", "lab@example.invalid"], workspace_root)
    run_command(["git", "add", "."], workspace_root)
    run_command(["git", "commit", "-qm", "baseline task fixture"], workspace_root)


def prepare_run(run_root: Path, fixture_root: Path, task_path: Path, verify_script: Path, architecture_script: Path) -> None:
    remove_tree(run_root)
    workspace_root = run_root / "workspace"
    shutil.copytree(fixture_root, workspace_root)
    shutil.copy2(task_path, workspace_root / "TASK.md")
    shutil.copy2(verify_script, workspace_root / "verify-basic.py")
    shutil.copy2(architecture_script, workspace_root / "check-architecture.py")
    write_text(workspace_root / ".gitignore", "__pycache__/\n*.pyc\n")
    init_repo(workspace_root)
    (run_root / "session_artifacts").mkdir(parents=True, exist_ok=True)


def exec_codex(
    prompt_text: str,
    cwd: Path,
    final_message_path: Path,
    events_path: Path,
    label: str,
    timeout_seconds: int = 1800,
) -> None:
    log(f"[start] {label}")
    started_at = time.time()
    completed = subprocess.run(
        [
            "codex",
            "exec",
            "-m",
            "gpt-5.4",
            "-c",
            'model_reasoning_effort="high"',
            "--dangerously-bypass-approvals-and-sandbox",
            "--json",
            "-o",
            str(final_message_path),
            "-C",
            str(cwd),
            prompt_text,
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
    )
    write_text(events_path, completed.stdout)
    elapsed = time.time() - started_at
    log(f"[done] {label} in {elapsed:.1f}s")


def run_single_workflow(experiment_root: Path, run_root: Path) -> None:
    prompt = (experiment_root / "prompts" / "single-generalist.txt").read_text(encoding="utf-8")
    workspace_root = run_root / "workspace"
    artifacts_root = run_root / "session_artifacts"
    exec_codex(
        prompt,
        workspace_root,
        artifacts_root / "single-final.txt",
        artifacts_root / "single-events.jsonl",
        label="single-generalist",
    )


def run_role_workflow(experiment_root: Path, run_root: Path) -> None:
    run_role_stages(experiment_root, run_root, ["coordinator", "implementer", "reviewer", "repair"])


def run_role_stages(experiment_root: Path, run_root: Path, selected_roles: list[str]) -> None:
    workspace_root = run_root / "workspace"
    session_artifacts = run_root / "session_artifacts"
    all_roles = [
        ("coordinator", "coordinator.txt"),
        ("implementer", "implementer.txt"),
        ("reviewer", "reviewer.txt"),
        ("repair", "repair.txt"),
    ]

    for role_name, prompt_file in all_roles:
        if role_name not in selected_roles:
            continue
        prompt = (experiment_root / "prompts" / prompt_file).read_text(encoding="utf-8")
        exec_codex(
            prompt,
            workspace_root,
            session_artifacts / f"{role_name}-final.txt",
            session_artifacts / f"{role_name}-events.jsonl",
            label=f"role-based:{role_name}",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workflow",
        choices=["all", "single-generalist", "role-based"],
        default="all",
        help="Run all workflows or only one workflow.",
    )
    parser.add_argument(
        "--reuse-existing-single",
        action="store_true",
        help="When running only role-based, keep the existing single-generalist run untouched.",
    )
    parser.add_argument(
        "--skip-prepare",
        action="store_true",
        help="Reuse the existing selected workflow run directory instead of recreating it.",
    )
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="Prepare the selected workflow workspace but do not run Codex sessions.",
    )
    parser.add_argument(
        "--role-stages",
        nargs="*",
        choices=["coordinator", "implementer", "reviewer", "repair"],
        help="When running role-based, restrict execution to the listed stages.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    experiment_root = Path(__file__).resolve().parent
    runs_root = experiment_root / "runs"
    artifacts_root = experiment_root / "artifacts"
    artifacts_root.mkdir(parents=True, exist_ok=True)

    fixture_root = experiment_root / "fixtures" / "base-task"
    task_path = experiment_root / "task.md"
    repo_root = experiment_root.parents[1]
    verify_script = repo_root / "experiments" / "005-lint-feedback-loop" / "verify-basic.py"
    architecture_script = repo_root / "experiments" / "005-lint-feedback-loop" / "check-architecture.py"

    single_run_root = runs_root / "single-generalist"
    role_run_root = runs_root / "role-based"

    if args.workflow in {"all", "single-generalist"}:
        if not args.skip_prepare:
            log("[prepare] single-generalist")
            prepare_run(single_run_root, fixture_root, task_path, verify_script, architecture_script)
        if not args.prepare_only:
            run_single_workflow(experiment_root, single_run_root)

    if args.workflow in {"all", "role-based"}:
        if args.workflow == "role-based" and args.reuse_existing_single:
            log("[reuse] existing single-generalist run")
        if not args.skip_prepare:
            log("[prepare] role-based")
            prepare_run(role_run_root, fixture_root, task_path, verify_script, architecture_script)
        if not args.prepare_only:
            selected_roles = args.role_stages or ["coordinator", "implementer", "reviewer", "repair"]
            run_role_stages(experiment_root, role_run_root, selected_roles)

    print(
        json.dumps(
            {
                "single_generalist_run": str(single_run_root),
                "role_based_run": str(role_run_root),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
