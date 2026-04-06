from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run_json_command(args: list[str], cwd: Path) -> dict:
    completed = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def load_events(events_path: Path) -> list[dict]:
    raw_text = None
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            raw_text = events_path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if raw_text is None:
        raise UnicodeDecodeError("utf-8", b"", 0, 1, f"Could not decode {events_path}")

    events = []
    for line in raw_text.splitlines():
        normalized = line.lstrip("\ufeff")
        if normalized.strip():
            events.append(json.loads(normalized))
    return events


def summarize_events(events_paths: list[Path]) -> dict:
    turn_count = 0
    input_tokens = 0
    cached_input_tokens = 0
    output_tokens = 0
    session_count = len(events_paths)

    for path in events_paths:
        for event in load_events(path):
            if event.get("type") == "turn.completed":
                usage = event.get("usage", {})
                turn_count += 1
                input_tokens += usage.get("input_tokens", 0)
                cached_input_tokens += usage.get("cached_input_tokens", 0)
                output_tokens += usage.get("output_tokens", 0)

    return {
        "session_count": session_count,
        "turn_count": turn_count,
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
    }


def heading_present(content: str, heading: str) -> bool:
    return heading.lower() in content.lower()


def auditability_checks(workspace_root: Path, mode: str) -> list[dict]:
    checks: list[dict] = []

    delivery_note = workspace_root / "delivery-note.md"
    coordination_brief = workspace_root / "coordination-brief.md"
    implementation_note = workspace_root / "implementation-note.md"
    review_note = workspace_root / "review.md"
    repair_note = workspace_root / "repair-note.md"

    if mode == "single-generalist":
        delivery_exists = delivery_note.exists()
        delivery_content = delivery_note.read_text(encoding="utf-8") if delivery_exists else ""
        checks.extend(
            [
                {
                    "name": "workflow-note-exists",
                    "passed": delivery_exists,
                    "detail": "Expected delivery-note.md for the single-agent workflow.",
                },
                {
                    "name": "workflow-note-has-files-changed",
                    "passed": delivery_exists and heading_present(delivery_content, "Files Changed"),
                    "detail": "Expected Files Changed in delivery-note.md.",
                },
                {
                    "name": "workflow-note-has-verification",
                    "passed": delivery_exists and heading_present(delivery_content, "Verification"),
                    "detail": "Expected Verification in delivery-note.md.",
                },
                {
                    "name": "coordination-brief-exists",
                    "passed": False,
                    "detail": "Role-specific coordination artifact not present in the single-agent workflow.",
                },
                {
                    "name": "coordination-brief-structured",
                    "passed": False,
                    "detail": "Role-specific coordination artifact not present in the single-agent workflow.",
                },
                {
                    "name": "implementation-note-structured",
                    "passed": False,
                    "detail": "Role-specific implementation note not present in the single-agent workflow.",
                },
                {
                    "name": "review-note-structured",
                    "passed": False,
                    "detail": "Role-specific review note not present in the single-agent workflow.",
                },
                {
                    "name": "repair-note-structured",
                    "passed": False,
                    "detail": "Role-specific repair note not present in the single-agent workflow.",
                },
            ]
        )
        return checks

    coordination_exists = coordination_brief.exists()
    implementation_exists = implementation_note.exists()
    review_exists = review_note.exists()
    repair_exists = repair_note.exists()

    coordination_content = coordination_brief.read_text(encoding="utf-8") if coordination_exists else ""
    implementation_content = implementation_note.read_text(encoding="utf-8") if implementation_exists else ""
    review_content = review_note.read_text(encoding="utf-8") if review_exists else ""
    repair_content = repair_note.read_text(encoding="utf-8") if repair_exists else ""

    checks.extend(
        [
            {
                "name": "workflow-note-exists",
                "passed": coordination_exists,
                "detail": "Expected coordination-brief.md for the role-based workflow.",
            },
            {
                "name": "coordination-brief-structured",
                "passed": coordination_exists
                and all(
                    heading_present(coordination_content, heading)
                    for heading in [
                        "Goal",
                        "Scope",
                        "Allowed Files",
                        "Verification",
                        "Handoff Checklist",
                    ]
                ),
                "detail": "Expected Goal, Scope, Allowed Files, Verification, and Handoff Checklist in coordination-brief.md.",
            },
            {
                "name": "implementation-note-exists",
                "passed": implementation_exists,
                "detail": "Expected implementation-note.md.",
            },
            {
                "name": "implementation-note-structured",
                "passed": implementation_exists
                and heading_present(implementation_content, "Files Changed")
                and heading_present(implementation_content, "Verification Run"),
                "detail": "Expected Files Changed and Verification Run in implementation-note.md.",
            },
            {
                "name": "review-note-exists",
                "passed": review_exists,
                "detail": "Expected review.md.",
            },
            {
                "name": "review-note-structured",
                "passed": review_exists
                and heading_present(review_content, "status:")
                and heading_present(review_content, "Verification"),
                "detail": "Expected status: and Verification in review.md.",
            },
            {
                "name": "repair-note-exists",
                "passed": repair_exists,
                "detail": "Expected repair-note.md.",
            },
            {
                "name": "repair-note-structured",
                "passed": repair_exists
                and heading_present(repair_content, "Result")
                and heading_present(repair_content, "Verification"),
                "detail": "Expected Result and Verification in repair-note.md.",
            },
        ]
    )
    return checks


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python score-workflow-run.py <run_root> <mode>",
            file=sys.stderr,
        )
        return 1

    run_root = Path(argv[1]).resolve()
    mode = argv[2]
    workspace_root = run_root / "workspace"
    repo_root = Path(__file__).resolve().parents[2]

    verify_script = repo_root / "experiments" / "005-lint-feedback-loop" / "verify-basic.py"
    architecture_script = repo_root / "experiments" / "005-lint-feedback-loop" / "check-architecture.py"

    functional = run_json_command([sys.executable, str(verify_script), str(workspace_root)], repo_root)
    architecture = run_json_command([sys.executable, str(architecture_script), str(workspace_root)], repo_root)

    audit_checks = auditability_checks(workspace_root, mode)
    audit_passed = sum(1 for check in audit_checks if check["passed"])

    session_artifacts_root = run_root / "session_artifacts"
    events_paths = sorted(session_artifacts_root.glob("*-events.jsonl"))
    telemetry = summarize_events(events_paths)

    result = {
        "run_root": str(run_root),
        "mode": mode,
        "product": {
            "functional": functional,
            "architecture": architecture,
            "total": {
                "score": functional["summary"]["passed"] + architecture["summary"]["passed"],
                "max": functional["summary"]["total"] + architecture["summary"]["total"],
            },
        },
        "auditability": {
            "checks": audit_checks,
            "summary": {
                "passed": audit_passed,
                "total": len(audit_checks),
            },
        },
        "telemetry": telemetry,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
