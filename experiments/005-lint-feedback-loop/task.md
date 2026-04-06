# Task

Use the base task repo as a toy refactor target.

Required change:

Add two new report fields to the CLI output:

- `unique_items`
- `summary_line`

Behavior rules:

1. Input items must still be normalized to lowercase and trimmed.
2. `unique_items` should contain a sorted unique list.
3. `summary_line` should look like `3 items across 2 unique values`.
4. Update the README example to mention the richer output.

Architecture expectation:

- normalization logic belongs in `report_app/domain.py`
- report-building logic belongs in `report_app/service.py`
- `report_app/cli.py` should stay thin and delegate to the service layer
