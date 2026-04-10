from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
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

    missing_files = [path for path in MANIFEST["required_files"] if not (TEMPLATE_ROOT / path).exists()]
    add_check(
        "required-files-exist",
        not missing_files,
        "Missing files: none" if not missing_files else f"Missing files: {missing_files}",
    )

    top_level_words = sum(
        word_count((TEMPLATE_ROOT / relative_path).read_text(encoding="utf-8"))
        for relative_path in MANIFEST["top_level_pack_files"]
    )
    add_check(
        "top-level-pack-stays-small",
        top_level_words <= MANIFEST["top_level_word_budget"],
        f"Top-level word count: {top_level_words}; budget: {MANIFEST['top_level_word_budget']}",
    )

    guidance_result = run_json_command([sys.executable, "checks/check-top-level-guidance.py", "."])
    add_check(
        "top-level-guidance-healthy",
        guidance_result["verdict"] == "pass",
        (
            f"Covered {guidance_result['summary']['required_paths_covered']} of "
            f"{guidance_result['summary']['required_path_count']} required paths; "
            f"stale references: {guidance_result['summary']['stale_reference_count']}; "
            f"wrong authority topics: {guidance_result['summary']['wrong_authority_count']}; "
            f"authority conflicts: {guidance_result['summary']['authority_conflict_count']}"
        ),
    )

    project_text = (TEMPLATE_ROOT / "docs/project.md").read_text(encoding="utf-8")
    missing_project_sections = [section for section in MANIFEST["required_project_sections"] if section not in project_text]
    add_check(
        "project-doc-ready",
        not missing_project_sections,
        "Missing sections: none" if not missing_project_sections else f"Missing sections: {missing_project_sections}",
    )

    log_text = (TEMPLATE_ROOT / "docs/log.md").read_text(encoding="utf-8")
    missing_log_sections = [section for section in MANIFEST["required_log_sections"] if section not in log_text]
    add_check(
        "log-doc-ready",
        not missing_log_sections,
        "Missing sections: none" if not missing_log_sections else f"Missing sections: {missing_log_sections}",
    )

    config_text = read_lower("configs/README.md")
    missing_config_terms = [term for term in MANIFEST["required_config_terms"] if term.lower() not in config_text]
    add_check(
        "config-guide-ready",
        not missing_config_terms,
        "Missing terms: none" if not missing_config_terms else f"Missing terms: {missing_config_terms}",
    )

    src_text = read_lower("src/README.md")
    missing_src_terms = [term for term in MANIFEST["required_src_terms"] if term.lower() not in src_text]
    add_check(
        "src-guide-ready",
        not missing_src_terms,
        "Missing terms: none" if not missing_src_terms else f"Missing terms: {missing_src_terms}",
    )

    script_text = read_lower("scripts/README.md")
    missing_script_terms = [term for term in MANIFEST["required_script_terms"] if term.lower() not in script_text]
    add_check(
        "script-guide-ready",
        not missing_script_terms,
        "Missing terms: none" if not missing_script_terms else f"Missing terms: {missing_script_terms}",
    )

    placeholder_token = MANIFEST["placeholder_token"]
    docs_without_placeholder_token = []

    for relative_path in MANIFEST["placeholder_docs"]:
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
    result = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "template_root": str(TEMPLATE_ROOT),
        "checks": checks,
        "summary": {
            "passed": passed_count,
            "total": total_count,
            "top_level_word_count": top_level_words,
            "guidance_verdict": guidance_result["verdict"],
            "placeholder_doc_count": len(MANIFEST["placeholder_docs"]),
        },
        "verdict": "pass" if passed_count == total_count else "fail",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
