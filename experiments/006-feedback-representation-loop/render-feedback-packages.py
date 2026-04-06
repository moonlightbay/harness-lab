from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


def load_spec(spec_path: Path) -> dict:
    return json.loads(spec_path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def render_docs_only(spec: dict) -> str:
    return dedent(
        f"""
        # Task excerpt

        Architecture expectation:

        - normalization logic belongs in `report_app/domain.py`
        - report-building logic belongs in `report_app/service.py`
        - `report_app/cli.py` should stay thin and delegate to the service layer

        Relevant task: {spec["task_name"]}
        """
    ).strip()


def render_review_comment(spec: dict) -> str:
    return dedent(
        """
        # Review comment

        This change still violates the architecture expectation even though the tests pass.

        Please move `normalize_items` back to `report_app/domain.py` and move `build_report` back to `report_app/service.py`. `report_app/cli.py` should only delegate to the service layer instead of constructing `unique_items` and `summary_line` directly. Re-run `python check-architecture.py <workspace_root>` after the cleanup.
        """
    ).strip()


def render_generic_check(spec: dict) -> str:
    first = spec["violations"][0]
    second = spec["violations"][1]
    boundary = spec["violations"][2]
    return dedent(
        f"""
        Architecture check failed.

        - Found `{first["symbol"]}` in `{first["actual_files"][0]}` and `{first["actual_files"][1]}`.
        - Found `{second["symbol"]}` in `{second["actual_files"][0]}` and `{second["actual_files"][1]}`.
        - `{boundary["file"]}` constructs `unique_items` and `summary_line` directly.

        Expected boundaries:
        - `{first["symbol"]}` only in `{first["expected_file"]}`
        - `{second["symbol"]}` only in `{second["expected_file"]}`
        - `{boundary["file"]}` delegates to the service layer

        3 of 6 architecture checks failed.
        """
    ).strip()


def render_remediation_check(spec: dict) -> str:
    first = spec["violations"][0]
    second = spec["violations"][1]
    boundary = spec["violations"][2]
    return dedent(
        f"""
        Architecture check failed for the current workspace.

        Actual:
        - `{first["symbol"]}` found in `{first["actual_files"][0]}` and `{first["actual_files"][1]}`
        - `{second["symbol"]}` found in `{second["actual_files"][0]}` and `{second["actual_files"][1]}`
        - {boundary["actual_behavior"]}

        Expected:
        - Keep `{first["symbol"]}` only in `{first["expected_file"]}`
        - Keep `{second["symbol"]}` only in `{second["expected_file"]}`
        - {boundary["expected_behavior"]}

        Fix:
        1. Delete the duplicate `{first["symbol"]}` definition from `{first["actual_files"][0]}`.
        2. Delete the duplicate `{second["symbol"]}` definition from `{second["actual_files"][0]}`.
        3. Import `build_report` from `report_app/service.py` in `report_app/cli.py` and delegate there instead.
        4. Re-run `{spec["verification_commands"][1]}` and `{spec["verification_commands"][0]}`.

        Pass condition:
        - {spec["pass_condition"]}
        """
    ).strip()


PACKAGE_RENDERERS = [
    {
        "name": "docs-only",
        "origin": "task-documentation",
        "format": "markdown-note",
        "feedback_file": "feedback.md",
        "renderer": render_docs_only,
    },
    {
        "name": "review-comment",
        "origin": "human-review",
        "format": "markdown-comment",
        "feedback_file": "feedback.md",
        "renderer": render_review_comment,
    },
    {
        "name": "failing-check-generic",
        "origin": "automated-check",
        "format": "plain-text-check-output",
        "feedback_file": "feedback.txt",
        "renderer": render_generic_check,
    },
    {
        "name": "failing-check-remediation",
        "origin": "automated-check-with-remediation",
        "format": "plain-text-check-output",
        "feedback_file": "feedback.txt",
        "renderer": render_remediation_check,
    },
]


def main() -> int:
    experiment_root = Path(__file__).resolve().parent
    spec_path = experiment_root / "fixtures" / "violation-spec.json"
    packages_root = experiment_root / "packages"
    spec = load_spec(spec_path)

    for package in PACKAGE_RENDERERS:
        package_root = packages_root / package["name"]
        package_root.mkdir(parents=True, exist_ok=True)
        metadata = {
            "name": package["name"],
            "origin": package["origin"],
            "format": package["format"],
            "feedback_file": package["feedback_file"],
            "source_spec": str(spec_path.relative_to(experiment_root)),
        }
        write_text(package_root / "package.json", json.dumps(metadata, indent=2))
        write_text(
            package_root / package["feedback_file"],
            package["renderer"](spec),
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
