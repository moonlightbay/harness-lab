from __future__ import annotations

import json
from pathlib import Path

from report_app.service import build_report


def load_items(config_path: Path) -> list[str]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return list(payload["items"])


def main() -> None:
    config_path = Path(__file__).resolve().parents[1] / "config" / "items.json"
    report = build_report(load_items(config_path))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
