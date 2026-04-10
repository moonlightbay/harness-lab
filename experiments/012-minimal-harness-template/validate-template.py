from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


EXPERIMENT_ROOT = Path(__file__).resolve().parent
TEMPLATE_ROOT = EXPERIMENT_ROOT / "template"
MANIFEST = json.loads((EXPERIMENT_ROOT / "manifest.json").read_text(encoding="utf-8"))


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text.strip())) if text.strip() else 0


def run_json_command(command: list[str]) -> dict:
    completed = subprocess.run(
        command,
        cwd=TEMPLATE_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(completed.stdout)


def read_lower(relative_path: str) -> str:
    return (TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8").lower()


def main() -> None:
    checks = []

    def add_check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    required_files = MANIFEST["required_files"]
    missing_files = [path for path in required_files if not (TEMPLATE_ROOT / path).exists()]
    add_check(
        "required-files-exist",
        not missing_files,
        "Missing files: none" if not missing_files else f"Missing files: {missing_files}",
    )

    top_level_paths = MANIFEST["top_level_pack_files"]
    top_level_words = 0
    for relative_path in top_level_paths:
        top_level_words += word_count((TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8"))
    add_check(
        "top-level-pack-stays-small",
        top_level_words <= MANIFEST["top_level_word_budget"],
        f"Top-level word count: {top_level_words}; budget: {MANIFEST['top_level_word_budget']}",
    )

    guidance_result = run_json_command([sys.executable, "checks/check-top-level-guidance.py", "."])
    add_check(
        "required-top-level-paths-covered",
        guidance_result["summary"]["required_paths_covered"] == guidance_result["summary"]["required_path_count"],
        (
            f"Covered {guidance_result['summary']['required_paths_covered']} of "
            f"{guidance_result['summary']['required_path_count']} required paths."
        ),
    )
    add_check(
        "no-stale-top-level-references",
        guidance_result["summary"]["stale_reference_count"] == 0,
        f"Stale references: {guidance_result['summary']['stale_reference_count']}",
    )
    add_check(
        "no-authority-conflicts",
        guidance_result["summary"]["authority_conflict_count"] == 0,
        f"Authority conflicts: {guidance_result['summary']['authority_conflict_count']}",
    )
    add_check(
        "no-wrong-authority-claims",
        guidance_result["summary"]["wrong_authority_count"] == 0,
        f"Wrong authority topics: {guidance_result['summary']['wrong_authority_count']}",
    )

    project_text = (TEMPLATE_ROOT / "docs/project.md").read_text(encoding="utf-8")
    missing_project_sections = [section for section in MANIFEST["required_project_sections"] if section not in project_text]
    add_check(
        "project-doc-ready",
        not missing_project_sections,
        "Missing sections: none" if not missing_project_sections else f"Missing sections: {missing_project_sections}",
    )

    architecture_text = (TEMPLATE_ROOT / "docs/architecture.md").read_text(encoding="utf-8")
    missing_architecture_sections = [
        section for section in MANIFEST["required_architecture_sections"] if section not in architecture_text
    ]
    add_check(
        "architecture-doc-ready",
        not missing_architecture_sections,
        (
            "Missing sections: none"
            if not missing_architecture_sections
            else f"Missing sections: {missing_architecture_sections}"
        ),
    )

    task_text = (TEMPLATE_ROOT / "docs/task.md").read_text(encoding="utf-8")
    missing_task_sections = [section for section in MANIFEST["required_task_sections"] if section not in task_text]
    add_check(
        "task-doc-ready",
        not missing_task_sections,
        "Missing sections: none" if not missing_task_sections else f"Missing sections: {missing_task_sections}",
    )

    log_text = (TEMPLATE_ROOT / "docs/log.md").read_text(encoding="utf-8")
    missing_log_sections = [section for section in MANIFEST["required_log_sections"] if section not in log_text]
    add_check(
        "log-doc-ready",
        not missing_log_sections,
        "Missing sections: none" if not missing_log_sections else f"Missing sections: {missing_log_sections}",
    )

    architecture_result = run_json_command([sys.executable, "checks/check-architecture.py", "."])
    add_check(
        "architecture-rule-hook-ready",
        architecture_result["summary"]["valid_rule_count"] >= 1 and architecture_result["summary"]["invalid_rule_count"] == 0,
        (
            f"Valid rules: {architecture_result['summary']['valid_rule_count']}; "
            f"invalid rules: {architecture_result['summary']['invalid_rule_count']}"
        ),
    )

    placeholder_token = MANIFEST["placeholder_token"]
    placeholder_docs = MANIFEST["placeholder_docs"]
    docs_without_placeholder_token = []

    for relative_path, required_sections in placeholder_docs.items():
        text = (TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8")
        if placeholder_token not in text:
            docs_without_placeholder_token.append(relative_path)

    add_check(
        "placeholder-markers-exist",
        not docs_without_placeholder_token,
        (
            "Placeholder marker missing: none"
            if not docs_without_placeholder_token
            else f"Placeholder marker missing: {docs_without_placeholder_token}"
        ),
    )

    passed_count = sum(1 for check in checks if check["passed"])
    total_count = len(checks)
    verdict = "pass" if passed_count == total_count else "fail"

    result = {
        "generated_at": __import__("datetime").datetime.now().astimezone().isoformat(),
        "template_root": str(TEMPLATE_ROOT),
        "checks": checks,
        "summary": {
            "passed": passed_count,
            "total": total_count,
            "top_level_word_count": top_level_words,
            "guidance_verdict": guidance_result["verdict"],
            "architecture_verdict": architecture_result["verdict"],
            "placeholder_doc_count": len(placeholder_docs),
        },
        "verdict": verdict,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
