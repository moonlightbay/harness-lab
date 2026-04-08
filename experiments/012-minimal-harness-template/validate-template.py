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

    plan_text = (TEMPLATE_ROOT / "docs/plans/execution-plan-template.md").read_text(encoding="utf-8")
    missing_sections = [section for section in MANIFEST["required_plan_sections"] if section not in plan_text]
    add_check(
        "execution-plan-template-sections",
        not missing_sections,
        "Missing sections: none" if not missing_sections else f"Missing sections: {missing_sections}",
    )

    git_text = (TEMPLATE_ROOT / "docs/workflows/git-workflow.md").read_text(encoding="utf-8").lower()
    missing_git_terms = [term for term in MANIFEST["required_git_terms"] if term.lower() not in git_text]
    add_check(
        "git-workflow-note-covers-worktrees",
        not missing_git_terms,
        "Missing git terms: none" if not missing_git_terms else f"Missing git terms: {missing_git_terms}",
    )

    execution_loop_text = read_lower("docs/workflows/execution-loop.md")
    missing_execution_loop_terms = [
        term for term in MANIFEST["required_execution_loop_terms"] if term.lower() not in execution_loop_text
    ]
    add_check(
        "execution-loop-covers-core-cycle",
        not missing_execution_loop_terms,
        (
            "Missing execution loop terms: none"
            if not missing_execution_loop_terms
            else f"Missing execution loop terms: {missing_execution_loop_terms}"
        ),
    )

    quality_gate_text = read_lower("docs/quality/quality-gates.md")
    missing_quality_gate_terms = [
        term for term in MANIFEST["required_quality_gate_terms"] if term.lower() not in quality_gate_text
    ]
    add_check(
        "quality-gates-cover-closeout",
        not missing_quality_gate_terms,
        (
            "Missing quality gate terms: none"
            if not missing_quality_gate_terms
            else f"Missing quality gate terms: {missing_quality_gate_terms}"
        ),
    )

    legacy_policy_text = read_lower("docs/quality/legacy-code-policy.md")
    missing_legacy_terms = [
        term for term in MANIFEST["required_legacy_policy_terms"] if term.lower() not in legacy_policy_text
    ]
    add_check(
        "legacy-code-policy-covers-classification",
        not missing_legacy_terms,
        (
            "Missing legacy policy terms: none"
            if not missing_legacy_terms
            else f"Missing legacy policy terms: {missing_legacy_terms}"
        ),
    )

    upstream_sync_text = read_lower("docs/workflows/upstream-sync.md")
    missing_upstream_terms = [
        term for term in MANIFEST["required_upstream_sync_terms"] if term.lower() not in upstream_sync_text
    ]
    add_check(
        "upstream-sync-covers-translation",
        not missing_upstream_terms,
        (
            "Missing upstream sync terms: none"
            if not missing_upstream_terms
            else f"Missing upstream sync terms: {missing_upstream_terms}"
        ),
    )

    harness_improvement_text = read_lower("docs/workflows/harness-improvement.md")
    missing_improvement_terms = [
        term for term in MANIFEST["required_harness_improvement_terms"] if term.lower() not in harness_improvement_text
    ]
    add_check(
        "harness-improvement-covers-rules-checks-skills",
        not missing_improvement_terms,
        (
            "Missing harness improvement terms: none"
            if not missing_improvement_terms
            else f"Missing harness improvement terms: {missing_improvement_terms}"
        ),
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
    missing_placeholder_sections = {}
    docs_without_placeholder_token = []

    for relative_path, required_sections in placeholder_docs.items():
        text = (TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8")
        missing_sections = [section for section in required_sections if section not in text]
        if missing_sections:
            missing_placeholder_sections[relative_path] = missing_sections
        if placeholder_token not in text:
            docs_without_placeholder_token.append(relative_path)

    add_check(
        "placeholder-doc-sections",
        not missing_placeholder_sections,
        (
            "Missing placeholder sections: none"
            if not missing_placeholder_sections
            else f"Missing placeholder sections: {missing_placeholder_sections}"
        ),
    )
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
