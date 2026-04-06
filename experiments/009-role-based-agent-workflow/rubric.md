# Scoring Rubric

## Product quality - 11 points

- Functional checks: 5 points from `verify-basic.py`
- Architecture checks: 6 points from `check-architecture.py`

## Auditability - 8 points

- `delivery-note.md` exists for the single-agent workflow, or `coordination-brief.md` exists for the role-based workflow.
- Role-based `coordination-brief.md` includes `Goal`, `Scope`, `Allowed Files`, `Verification`, and `Handoff Checklist`.
- `implementation-note.md` exists.
- `implementation-note.md` includes `Files Changed` and `Verification Run`.
- `review.md` exists.
- `review.md` includes `status:` and a verification section.
- `repair-note.md` exists.
- `repair-note.md` records whether code changes were required after review.

## Cost signals

- number of Codex sessions
- total turn count
- total input tokens
- total output tokens

## Interpretation

- Final product quality is primary.
- Auditability is the main expected gain from role division.
- Higher auditability with higher cost is still a meaningful positive result for this experiment.
