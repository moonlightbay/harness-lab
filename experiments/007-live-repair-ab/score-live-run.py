from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
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
    for index, line in enumerate(raw_text.splitlines()):
        normalized = line.lstrip("\ufeff")
        if normalized.strip():
            try:
                events.append(json.loads(normalized))
            except json.JSONDecodeError as exc:
                raise json.JSONDecodeError(exc.msg, normalized, exc.pos) from exc
    return events


def summarize_events(events: list[dict]) -> dict:
    turn_count = 0
    input_tokens = 0
    output_tokens = 0
    cached_input_tokens = 0
    item_types = Counter()

    for event in events:
        if event.get("type") == "turn.completed":
            usage = event.get("usage", {})
            turn_count += 1
            input_tokens += usage.get("input_tokens", 0)
            output_tokens += usage.get("output_tokens", 0)
            cached_input_tokens += usage.get("cached_input_tokens", 0)

        item = event.get("item")
        if isinstance(item, dict):
            item_type = item.get("type")
            if item_type:
                item_types[item_type] += 1

    return {
        "turn_count": turn_count,
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
        "item_type_counts": dict(item_types),
    }


def load_changed_files(workspace_root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(workspace_root), "diff", "--name-only", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in completed.stdout.splitlines() if line.strip()]


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python score-live-run.py <workspace_root> <events_path>",
            file=sys.stderr,
        )
        return 1

    workspace_root = Path(argv[1]).resolve()
    events_path = Path(argv[2]).resolve()
    repo_root = Path(__file__).resolve().parents[2]

    verify_script = repo_root / "experiments" / "005-lint-feedback-loop" / "verify-basic.py"
    architecture_script = repo_root / "experiments" / "005-lint-feedback-loop" / "check-architecture.py"

    functional = run_json_command([sys.executable, str(verify_script), str(workspace_root)], repo_root)
    architecture = run_json_command([sys.executable, str(architecture_script), str(workspace_root)], repo_root)
    events = load_events(events_path)
    telemetry = summarize_events(events)
    changed_files = load_changed_files(workspace_root)

    functional_score = functional["summary"]["passed"]
    architecture_score = architecture["summary"]["passed"]

    result = {
        "workspace_root": str(workspace_root),
        "functional": functional,
        "architecture": architecture,
        "total": {
            "score": functional_score + architecture_score,
            "max": functional["summary"]["total"] + architecture["summary"]["total"],
        },
        "telemetry": telemetry,
        "changed_files": changed_files,
        "changed_file_count": len(changed_files),
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
