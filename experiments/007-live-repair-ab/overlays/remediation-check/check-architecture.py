from __future__ import annotations

import ast
import sys
from pathlib import Path


def parse_python(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def defined_functions(tree: ast.AST) -> set[str]:
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def imported_from_module(tree: ast.AST, module_names: set[str], imported_name: str) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in module_names:
            if any(alias.name == imported_name for alias in node.names):
                return True
    return False


def contains_report_field_literals(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    return any(token in content for token in ['"unique_items"', "'unique_items'", '"summary_line"', "'summary_line'"])


def main() -> int:
    workspace_root = Path.cwd()
    app_root = workspace_root / "report_app"

    domain_tree = parse_python(app_root / "domain.py")
    service_tree = parse_python(app_root / "service.py")
    cli_path = app_root / "cli.py"
    cli_tree = parse_python(cli_path)

    function_locations: dict[str, list[str]] = {}
    for py_file in sorted(app_root.glob("*.py")):
        functions = defined_functions(parse_python(py_file))
        for function_name in functions:
            function_locations.setdefault(function_name, []).append(py_file.name)

    failures = []

    if function_locations.get("normalize_items", []) != ["domain.py"]:
        failures.append(
            {
                "actual": f"normalize_items found in {function_locations.get('normalize_items', [])}",
                "expected": "normalize_items only in domain.py",
                "fix": "Delete the duplicate normalize_items definition from report_app/cli.py and keep the function in report_app/domain.py.",
            }
        )

    if function_locations.get("build_report", []) != ["service.py"]:
        failures.append(
            {
                "actual": f"build_report found in {function_locations.get('build_report', [])}",
                "expected": "build_report only in service.py",
                "fix": "Delete the duplicate build_report definition from report_app/cli.py and keep the function in report_app/service.py.",
            }
        )

    if not imported_from_module(service_tree, {"report_app.domain", ".domain", "domain"}, "normalize_items"):
        failures.append(
            {
                "actual": "service.py does not import normalize_items from domain.py",
                "expected": "service.py imports normalize_items from report_app/domain.py",
                "fix": "Import normalize_items into report_app/service.py and delegate normalization there.",
            }
        )

    if not (
        imported_from_module(cli_tree, {"report_app.service", ".service", "service"}, "build_report")
        and not contains_report_field_literals(cli_path)
    ):
        failures.append(
            {
                "actual": "cli.py still constructs report fields directly or does not import build_report",
                "expected": "cli.py imports build_report from report_app/service.py and delegates to it",
                "fix": "Import build_report in report_app/cli.py, call it from main(), and remove direct construction of unique_items and summary_line.",
            }
        )

    passed = 6 - len(failures)
    if failures:
        print("Architecture check failed.")
        print("")
        print("Actual:")
        for failure in failures:
            print(f"- {failure['actual']}")
        print("")
        print("Expected:")
        for failure in failures:
            print(f"- {failure['expected']}")
        print("")
        print("Fix:")
        for index, failure in enumerate(failures, start=1):
            print(f"{index}. {failure['fix']}")
        print("")
        print("Re-run:")
        print("- python check-architecture.py")
        print("- python verify-basic.py")
        print("")
        print("Pass condition:")
        print("- Architecture check summary reaches 6 / 6")
        print("- Basic verifier still passes")
        return 1

    print("Architecture check summary:")
    print("- Passed: 6 / 6")
    print("- All architecture checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
