from __future__ import annotations

from report_app.domain import normalize_items


def build_report(items: list[str]) -> dict[str, object]:
    normalized = normalize_items(items)
    unique_items = sorted(set(normalized))
    return {
        "items": normalized,
        "item_count": len(normalized),
        "unique_items": unique_items,
        "summary_line": f"{len(normalized)} items across {len(unique_items)} unique values",
    }
