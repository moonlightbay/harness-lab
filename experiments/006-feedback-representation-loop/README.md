# Experiment 006 - Feedback Representation Loop

Last updated: 2026-04-06

## Goal

Compare four ways of expressing the same architecture violation, then measure which feedback package is most ready for an agent repair loop.

## Hypothesis

The same invariant becomes much more useful when feedback includes diagnosis, remediation, and rerun instructions. Requirement-only feedback should be weakest, while a failing check with explicit remediation should be strongest.

## Setup

- Shared violation spec: `fixtures/violation-spec.json`
- Feedback-package generator: `render-feedback-packages.py`
- Single-package scorer: `score-feedback-package.py`
- Comparison runner: `compare-feedback-packages.py`
- Generated packages: `packages/`
- Scoring rubric: `rubric.md`

## Evaluation criteria

- Pass if all four feedback packages are generated from the same violation spec.
- Pass if the remediation-oriented failing check scores highest on repair-loop readiness.
- Strong pass if the docs-only package scores lowest and the review-comment and generic-check packages sit in the middle.

## Result

Initial run on 2026-04-06: pass.

- `docs-only`: 3 / 12
- `review-comment`: 9 / 12
- `failing-check-generic`: 5 / 12
- `failing-check-remediation`: 12 / 12
- Verdict: remediation-oriented failing checks are the strongest default harness feedback for autonomous repair.

Caveat: this is a controlled representation study. It compares feedback shapes generated from the same violation object, but it is not yet a repeated live-agent benchmark.

See `artifacts/docs-only-score.json`, `artifacts/review-comment-score.json`, `artifacts/failing-check-generic-score.json`, `artifacts/failing-check-remediation-score.json`, `artifacts/feedback-representation-comparison.json`, and `artifacts/run-2026-04-06.md`.
