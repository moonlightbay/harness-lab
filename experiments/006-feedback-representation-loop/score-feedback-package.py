from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ACTION_WORDS = ("move", "keep", "remove", "delete", "import", "delegate", "re-run", "rerun")
SECTION_LABELS = ("actual:", "expected:", "fix:", "pass condition:")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_package(package_root: Path) -> tuple[dict, str]:
    metadata = load_json(package_root / "package.json")
    feedback_path = package_root / metadata["feedback_file"]
    return metadata, feedback_path.read_text(encoding="utf-8")


def contains_all(text: str, values: list[str]) -> bool:
    lowered = text.lower()
    return all(value.lower() in lowered for value in values)


def line_has_fix(text: str, symbol: str, expected_file: str) -> bool:
    for line in text.splitlines():
        lowered = line.lower()
        if symbol.lower() in lowered and expected_file.lower() in lowered:
            if any(word in lowered for word in ACTION_WORDS):
                return True
    return False


def has_cli_guidance(text: str) -> bool:
    for line in text.splitlines():
        lowered = line.lower()
        if "cli.py" not in lowered:
            continue
        if any(token in lowered for token in ("delegate", "thin", "avoid", "import `build_report`", "import build_report")):
            return True
    return False


def has_rerun_command(text: str, commands: list[str]) -> bool:
    lowered = text.lower()
    return any(command.lower() in lowered for command in commands)


def has_labeled_sections(text: str) -> bool:
    labels_found = sum(1 for label in SECTION_LABELS if label in text.lower())
    heading_count = len(re.findall(r"^#.+$", text, flags=re.MULTILINE))
    return labels_found >= 2 or heading_count >= 3


def separates_actual_and_expected(text: str) -> bool:
    lowered = text.lower()
    return "actual:" in lowered and "expected:" in lowered


def defines_pass_condition(text: str, pass_condition: str) -> bool:
    lowered = text.lower()
    return "pass condition:" in lowered or pass_condition.lower() in lowered or "6 / 6 passed" in lowered


def can_agent_act_without_translation(
    names_symbols: bool,
    names_expected_files: bool,
    fix_normalize: bool,
    fix_build_report: bool,
    cli_guidance: bool,
    rerun_command: bool,
) -> bool:
    return all(
        [
            names_symbols,
            names_expected_files,
            fix_normalize,
            fix_build_report,
            cli_guidance,
            rerun_command,
        ]
    )


def score_feedback(package_root: Path, spec_path: Path) -> dict:
    spec = load_json(spec_path)
    metadata, feedback_text = load_package(package_root)

    required_symbols = spec["required_symbols"]
    expected_files = spec["expected_files"]
    offending_file = spec["offending_file"]
    violation_one = spec["violations"][0]
    violation_two = spec["violations"][1]

    states_failure = any(
        token in feedback_text.lower()
        for token in ("failed", "failure", "violates", "violation", "check failed")
    )
    names_symbols = contains_all(feedback_text, required_symbols)
    names_offending_file = offending_file.lower() in feedback_text.lower() or "cli.py" in feedback_text.lower()
    names_expected_files = contains_all(feedback_text, expected_files)
    fix_normalize = line_has_fix(feedback_text, violation_one["symbol"], violation_one["expected_file"])
    fix_build_report = line_has_fix(feedback_text, violation_two["symbol"], violation_two["expected_file"])
    cli_guidance = has_cli_guidance(feedback_text)
    rerun_command = has_rerun_command(feedback_text, spec["verification_commands"])
    labeled_sections = has_labeled_sections(feedback_text)
    actual_vs_expected = separates_actual_and_expected(feedback_text)
    pass_condition = defines_pass_condition(feedback_text, spec["pass_condition"])
    agent_ready = can_agent_act_without_translation(
        names_symbols,
        names_expected_files,
        fix_normalize,
        fix_build_report,
        cli_guidance,
        rerun_command,
    )

    checks = [
        {
            "name": "states-architecture-failure",
            "passed": states_failure,
            "detail": "Mentions that the current run failed or violated an architecture expectation.",
        },
        {
            "name": "names-violated-symbols",
            "passed": names_symbols,
            "detail": f"Mentions {required_symbols}.",
        },
        {
            "name": "names-offending-file",
            "passed": names_offending_file,
            "detail": f"Mentions {offending_file}.",
        },
        {
            "name": "names-expected-files",
            "passed": names_expected_files,
            "detail": f"Mentions {expected_files}.",
        },
        {
            "name": "fix-direction-normalize-items",
            "passed": fix_normalize,
            "detail": f"Gives a direct fix for {violation_one['symbol']}.",
        },
        {
            "name": "fix-direction-build-report",
            "passed": fix_build_report,
            "detail": f"Gives a direct fix for {violation_two['symbol']}.",
        },
        {
            "name": "cli-should-delegate",
            "passed": cli_guidance,
            "detail": "Restates that cli.py should delegate instead of constructing report fields directly.",
        },
        {
            "name": "includes-rerun-command",
            "passed": rerun_command,
            "detail": f"Includes one of {spec['verification_commands']}.",
        },
        {
            "name": "uses-machine-friendly-structure",
            "passed": labeled_sections,
            "detail": "Uses labeled sections or dense headings that a harness could preserve cleanly.",
        },
        {
            "name": "separates-actual-and-expected",
            "passed": actual_vs_expected,
            "detail": "Separates actual state from expected state.",
        },
        {
            "name": "defines-pass-condition",
            "passed": pass_condition,
            "detail": "Defines what success looks like after the repair.",
        },
        {
            "name": "agent-can-act-without-translation",
            "passed": agent_ready,
            "detail": "Contains enough detail for an agent to attempt the repair without extra human interpretation.",
        },
    ]

    passed_count = sum(1 for check in checks if check["passed"])

    return {
        "package_root": str(package_root),
        "metadata": metadata,
        "summary": {
            "score": passed_count,
            "max": len(checks),
        },
        "checks": checks,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python score-feedback-package.py <package_root> <spec_path>",
            file=sys.stderr,
        )
        return 1

    package_root = Path(argv[1]).resolve()
    spec_path = Path(argv[2]).resolve()
    result = score_feedback(package_root, spec_path)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
