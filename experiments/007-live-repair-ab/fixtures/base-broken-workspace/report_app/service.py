from __future__ import annotations

from report_app.domain import normalize_items


def build_report(items: list[str]) -> dict[str, object]:
    normalized = normalize_items(items)
    return {
        "items": normalized,
        "item_count": len(normalized),
    }
