# Task

Use the base task repo as a small refactor target.

Required changes:

1. Rename `scripts/export-report.ps1` to `scripts/generate-report.ps1`.
2. Update the generated JSON to include `generated_at`.
3. Update the generated JSON to include `item_count`.
4. Update the test to validate the new fields and the new script path.
5. Update the README usage example to the new script name.
6. Add a changelog entry describing the refactor.

The comparison is about two different run packages for the same task:

- `runs/no-plan/`: the task was executed without a checked-in execution plan.
- `runs/with-plan/`: the task was executed with a checked-in execution plan and progress artifacts.
