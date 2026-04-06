# Experiment 005 - Lint Feedback Loop

Last updated: 2026-04-06

## Goal

Compare a basic feedback loop against a stronger feedback loop on the same toy refactor task, then measure whether an added architecture rule improves output consistency beyond syntax and unit tests alone.

## Hypothesis

Syntax checks and unit tests can allow structurally poor changes to pass, while a small custom architecture rule can preserve layering and reduce duplicated logic without increasing tooling complexity much.

## Setup

- Base task: `task.md` and `fixtures/base-task/`
- Basic feedback run: `runs/basic-feedback/`
- Strong feedback run: `runs/strong-feedback/`
- Functional verifier: `verify-basic.py`
- Architecture checker: `check-architecture.py`
- Run scorer: `score-feedback-run.py`
- Comparison script: `compare-feedback-runs.py`
- Scoring rubric: `rubric.md`

## Evaluation criteria

- Pass if both runs satisfy the functional checks.
- Pass if the strong feedback run scores higher on architecture consistency.
- Strong pass if the basic-feedback run shows how functionality can pass while structure still degrades.

## Result

Initial run on 2026-04-06: pass.

- Basic feedback total score: 8 / 11.
- Strong feedback total score: 11 / 11.
- Both runs passed all functional checks.
- Architecture score improved from 3 / 6 to 6 / 6 with the added custom rule.

See `artifacts/basic-feedback-score.json`, `artifacts/strong-feedback-score.json`, `artifacts/feedback-comparison.json`, and `artifacts/run-2026-04-06.md`.
