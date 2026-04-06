from __future__ import annotations


def normalize_items(items: list[str]) -> list[str]:
    normalized = []
    for item in items:
        cleaned = item.strip().lower()
        if cleaned:
            normalized.append(cleaned)
    return normalized
