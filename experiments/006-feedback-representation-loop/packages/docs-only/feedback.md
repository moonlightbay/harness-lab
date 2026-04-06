# Task excerpt

Architecture expectation:

- normalization logic belongs in `report_app/domain.py`
- report-building logic belongs in `report_app/service.py`
- `report_app/cli.py` should stay thin and delegate to the service layer

Relevant task: Add unique_items and summary_line to CLI output
