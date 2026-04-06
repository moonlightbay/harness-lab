# Experiment 010 Rubric

Each pack is scored out of 12 points.

## 1. Required-path coverage (0-4)

- 1 point per required path mentioned at least once.
- Required paths:
  - `README.md`
  - `docs/knowledge/harness-engineering-overview.md`
  - `docs/plans/experiment-plan.md`
  - `docs/plans/experiment-log.md`

## 2. Freshness (0-4)

- Start from 4 points.
- Subtract 2 points for each unique markdown path reference that does not exist in the repo.
- Rationale: a dead path is a harder failure than a live-but-ambiguous path because it turns the next navigation step into a dead end.
- Floor at 0.

## 3. Authority clarity (0-4)

- Start from 4 points.
- Subtract 1 point for each topic whose "Source of truth for ..." claim points to the wrong file.
- Subtract 1 point for each topic with more than one distinct source-of-truth claim.
- Floor at 0.

## Interpretation

- `12 / 12`: clean top-level map
- `8-11 / 12`: usable but carries ambiguity or extra risk
- `0-7 / 12`: agent-legibility failure that should be cleaned up
