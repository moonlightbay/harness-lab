# Experiment 010 - Stale Doc and Duplicate Guidance

Last updated: 2026-04-06

## Goal

Compare a clean short top-level map against two Layer B failure modes, then measure how stale authority claims and duplicate source-of-truth claims erode agent legibility even when required paths are still present.

## Hypothesis

If a repo keeps the current paths visible but adds stale authority claims or duplicate source-of-truth claims, raw path coverage can remain high while navigation quality degrades. The stale-doc variant should score worst because it points to dead paths. The duplicate-guidance variant should still look complete but become ambiguous.

## Setup

- Baseline pack: `AGENTS.md` + `README.md`
- Stale-doc fixture: `fixtures/STALE-TOP-LEVEL-MAP.md`
- Duplicate-guidance fixture: `fixtures/DUPLICATE-GUIDANCE-MAP.md`
- Shared navigation metrics: `../shared/measure-navigation-pack.ps1`
- Pack scorer: `score-legibility-pack.ps1`
- Comparison script: `compare-legibility-packs.ps1`
- Scoring rubric: `rubric.md`

All three packs are scored against the same required paths:

- `README.md`
- `docs/knowledge/harness-engineering-overview.md`
- `docs/plans/experiment-plan.md`
- `docs/plans/experiment-log.md`

The scorer combines three signals:

- required-path coverage
- stale markdown path references
- authority clarity, based on whether "Source of truth for ..." claims are wrong or duplicated

## Evaluation criteria

- Pass if all three packs are measured with the same scorer.
- Pass if at least one failure-mode fixture preserves full required-path coverage but still scores lower than the baseline because of stale or conflicting guidance.
- Strong pass if both fixtures keep required-path coverage but still lose decisively on freshness or authority clarity.

## Result

Initial run on 2026-04-06: pass.

- `baseline`: 12 / 12
- `stale-doc`: 6 / 12
- `duplicate-guidance`: 8 / 12
- Verdict: coverage alone does not protect agent legibility

Observed difference:

- The stale-doc fixture still mentioned all required current paths, but it assigned authority to two dead files: `docs/plans/current-roadmap.md` and `docs/plans/run-log.md`.
- The duplicate-guidance fixture kept every path live, but it gave the roadmap and experiment log two competing "source of truth" claims each.
- The baseline pack stayed short, had no dead references, and made no conflicting authority claims.

Interpretation:

- A pack can look complete while still steering an agent into the wrong place.
- Stale authority is the sharpest failure because it turns the first step into a dead end.
- Duplicate authority is less severe than stale authority, but it still adds ambiguity and should be treated as a repo-legibility failure.

See `artifacts/baseline-pack-score.json`, `artifacts/stale-doc-pack-score.json`, `artifacts/duplicate-guidance-pack-score.json`, `artifacts/legibility-failure-comparison.json`, and `artifacts/run-2026-04-06.md`.
