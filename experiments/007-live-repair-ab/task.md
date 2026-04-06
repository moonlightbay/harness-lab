# Task

Repair the existing workspace so it satisfies both the functional behavior and the architecture boundary.

Current state:

- The workspace already passes syntax and unit tests.
- The workspace already prints `unique_items` and `summary_line`.
- The workspace still violates the architecture boundary.

Required end state:

- `normalize_items` must live only in `report_app/domain.py`
- `build_report` must live only in `report_app/service.py`
- `report_app/cli.py` must stay thin and delegate to the service layer
- `python verify-basic.py`
- `python check-architecture.py`

The experiment compares two runtime feedback loops, not two different tasks.
