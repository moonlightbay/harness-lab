from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_command(args: list[str], cwd: Path) -> tuple[bool, str]:
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    output = (result.stdout + result.stderr).strip()
    return result.returncode == 0, output


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python verify-basic.py <workspace_root>")

    workspace_root = Path(sys.argv[1]).resolve()
    checks: list[dict[str, object]] = []

    compile_ok, compile_output = run_command(
        [sys.executable, "-m", "compileall", "report_app", "tests"],
        workspace_root,
    )
    checks.append(
        {
            "name": "package-compiles",
            "passed": compile_ok,
            "detail": compile_output or "compileall passed",
        }
    )

    tests_ok, tests_output = run_command(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        workspace_root,
    )
    checks.append(
        {
            "name": "unit-tests-pass",
            "passed": tests_ok,
            "detail": tests_output or "unittest passed",
        }
    )

    cli_ok, cli_output = run_command(
        [sys.executable, "-m", "report_app.cli"],
        workspace_root,
    )

    unique_items_ok = False
    summary_line_ok = False
    payload_detail = cli_output

    if cli_ok:
        try:
            payload = json.loads(cli_output)
            unique_items_ok = "unique_items" in payload
            summary_line_ok = "summary_line" in payload
            payload_detail = json.dumps(payload, sort_keys=True)
        except json.JSONDecodeError:
            payload_detail = f"invalid json: {cli_output}"

    checks.append(
        {
            "name": "unique-items-field",
            "passed": unique_items_ok,
            "detail": payload_detail,
        }
    )
    checks.append(
        {
            "name": "summary-line-field",
            "passed": summary_line_ok,
            "detail": payload_detail,
        }
    )

    readme_path = workspace_root / "README.md"
    readme_content = readme_path.read_text(encoding="utf-8")
    readme_ok = "summary_line" in readme_content and "unique_items" in readme_content
    checks.append(
        {
            "name": "readme-updated",
            "passed": readme_ok,
            "detail": "README mentions unique_items and summary_line",
        }
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
