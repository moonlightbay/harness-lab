# Review comment

This change still violates the architecture expectation even though the tests pass.

Please move `normalize_items` back to `report_app/domain.py` and move `build_report` back to `report_app/service.py`. `report_app/cli.py` should only delegate to the service layer instead of constructing `unique_items` and `summary_line` directly. Re-run `python check-architecture.py <workspace_root>` after the cleanup.
