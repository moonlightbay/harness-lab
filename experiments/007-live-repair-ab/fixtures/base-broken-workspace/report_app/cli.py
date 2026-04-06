from __future__ import annotations

import json
from pathlib import Path


def load_items(config_path: Path) -> list[str]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    return list(payload["items"])


def normalize_items(items: list[str]) -> list[str]:
    normalized = []
    for item in items:
        cleaned = item.strip().lower()
        if cleaned:
            normalized.append(cleaned)
    return normalized


def build_report(items: list[str]) -> dict[str, object]:
    normalized = normalize_items(items)
    unique_items = sorted(set(normalized))
    return {
        "items": normalized,
        "item_count": len(normalized),
        "unique_items": unique_items,
        "summary_line": f"{len(normalized)} items across {len(unique_items)} unique values",
    }


def main() -> None:
    config_path = Path(__file__).resolve().parents[1] / "config" / "items.json"
    report = build_report(load_items(config_path))
    print(json.dumps(report))


if __name__ == "__main__":
    main()
