# Scoring Rubric

## Diagnosis clarity - 4 points

- States that the current run failed an architecture or boundary expectation.
- Names both violated symbols: `normalize_items` and `build_report`.
- Names the offending file: `report_app/cli.py`.
- Names the expected target files: `report_app/domain.py` and `report_app/service.py`.

## Repair guidance - 4 points

- Gives an explicit fix direction for `normalize_items`.
- Gives an explicit fix direction for `build_report`.
- Restates that `report_app/cli.py` should delegate instead of constructing report fields directly.
- Includes a concrete rerun command.

## Loop readiness - 4 points

- Uses labeled sections or another machine-friendly structure.
- Separates actual state from expected state.
- Defines a pass condition.
- Gives enough information that an agent could attempt the repair without extra human translation.
