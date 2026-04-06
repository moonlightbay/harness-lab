# Scoring Rubric

## Result quality - 7 points

- New script exists at `scripts/generate-report.ps1`.
- Old script `scripts/export-report.ps1` is removed.
- Output includes `generated_at`.
- Output includes `item_count`.
- Tests target the new script and the new fields.
- README usage example is updated.
- Changelog entry is added.

## Restartability - 5 points

- Run package includes a checked-in plan.
- Current status is written down.
- Changed files or completed steps are written down.
- Next step or remaining risk is written down.
- Verification status is written down.

## Auditability - 4 points

- Decision log exists.
- Verification log exists.
- Commands or checks are recorded.
- Assumptions or constraints are recorded.
