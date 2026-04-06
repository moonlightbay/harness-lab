# Scoring Rubric

## Functional checks - 5 points

- Package compiles.
- Unit tests pass.
- Output includes `unique_items`.
- Output includes `summary_line`.
- README mentions the richer output.

## Architecture checks - 6 points

- `normalize_items` exists in `report_app/domain.py`.
- `normalize_items` is not defined outside `report_app/domain.py`.
- `build_report` exists in `report_app/service.py`.
- `build_report` is not defined outside `report_app/service.py`.
- `report_app/service.py` imports `normalize_items`.
- `report_app/cli.py` imports `build_report` and does not construct report fields directly.
