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
    cli_tree = parse_python(app_root / "cli.py")

    function_locations: dict[str, list[str]] = {}
    for py_file in sorted(app_root.glob("*.py")):
        functions = defined_functions(parse_python(py_file))
        for function_name in functions:
            function_locations.setdefault(function_name, []).append(py_file.name)

    failures = []

    if function_locations.get("normalize_items", []) != ["domain.py"]:
        failures.append(f"Found normalize_items in {function_locations.get('normalize_items', [])}")

    if function_locations.get("build_report", []) != ["service.py"]:
        failures.append(f"Found build_report in {function_locations.get('build_report', [])}")

    if not imported_from_module(service_tree, {"report_app.domain", ".domain", "domain"}, "normalize_items"):
        failures.append("service.py does not import normalize_items from domain.py")

    if not (
        imported_from_module(cli_tree, {"report_app.service", ".service", "service"}, "build_report")
        and not contains_report_field_literals(app_root / "cli.py")
    ):
        failures.append("cli.py does not delegate cleanly to build_report")

    passed = 6 - len(failures)
    print("Architecture check summary:")
    print(f"- Passed: {passed} / 6")
    if failures:
        print("- Failures:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("- All architecture checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
