from __future__ import annotations

import ast
import json
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


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python check-architecture.py <workspace_root>")

    workspace_root = Path(sys.argv[1]).resolve()
    app_root = workspace_root / "report_app"

    domain_path = app_root / "domain.py"
    service_path = app_root / "service.py"
    cli_path = app_root / "cli.py"

    domain_tree = parse_python(domain_path)
    service_tree = parse_python(service_path)
    cli_tree = parse_python(cli_path)

    py_files = sorted(app_root.glob("*.py"))
    function_locations: dict[str, list[str]] = {}
    for py_file in py_files:
        functions = defined_functions(parse_python(py_file))
        for function_name in functions:
            function_locations.setdefault(function_name, []).append(py_file.name)

    checks = []

    def add_check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    add_check(
        "normalize-items-in-domain",
        "normalize_items" in defined_functions(domain_tree),
        "Expected normalize_items in report_app/domain.py",
    )
    add_check(
        "normalize-items-only-in-domain",
        function_locations.get("normalize_items", []) == ["domain.py"],
        f"Found normalize_items in {function_locations.get('normalize_items', [])}",
    )
    add_check(
        "build-report-in-service",
        "build_report" in defined_functions(service_tree),
        "Expected build_report in report_app/service.py",
    )
    add_check(
        "build-report-only-in-service",
        function_locations.get("build_report", []) == ["service.py"],
        f"Found build_report in {function_locations.get('build_report', [])}",
    )
    add_check(
        "service-imports-normalize-items",
        imported_from_module(service_tree, {"report_app.domain", ".domain", "domain"}, "normalize_items"),
        "Expected service.py to import normalize_items from domain.py",
    )
    add_check(
        "cli-delegates-to-service",
        imported_from_module(cli_tree, {"report_app.service", ".service", "service"}, "build_report")
        and not contains_report_field_literals(cli_path),
        "Expected cli.py to import build_report and avoid constructing report fields directly",
    )

    passed = sum(1 for item in checks if item["passed"])
    result = {
        "workspace_root": str(workspace_root),
        "checks": checks,
        "summary": {
            "passed": passed,
            "total": len(checks),
        },
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
