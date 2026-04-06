# Task

Use one shared architecture violation from Experiment 005 as the repair target.

The broken workspace already passes syntax and unit tests, but it still violates the architecture expectation:

- `normalize_items` was duplicated into `report_app/cli.py`
- `build_report` was duplicated into `report_app/cli.py`
- `report_app/cli.py` constructs `unique_items` and `summary_line` directly instead of delegating to the service layer

This experiment does not compare different rules. It compares different ways of expressing the same failure:

1. requirement-only documentation
2. a human review comment
3. a generic failing check
4. a failing check with remediation instructions

The question is which representation gives an agent the clearest path from failure to repair.
