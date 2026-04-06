# Experiment 004 - Plan vs No Plan

Last updated: 2026-04-06

## Goal

Compare a no-plan run and a plan-driven run on the same medium-complexity refactor task, then score the two run packages for result quality, restartability, and auditability.

## Hypothesis

A checked-in execution plan should improve restartability and auditability, and it should also reduce the chance of missing low-salience task requirements.

## Setup

- Base task: `task.md` and `fixtures/base-task/`
- No-plan run package: `runs/no-plan/`
- Plan-driven run package: `runs/with-plan/`
- Workspace verifier: `verify-workspace.ps1`
- Run scorer: `score-run-package.ps1`
- Comparison script: `compare-run-packages.ps1`
- Scoring rubric: `rubric.md`

## Evaluation criteria

- Pass if the plan-driven run scores higher on restartability and auditability.
- Strong pass if the plan-driven run also scores higher on result quality.
- The comparison is valid only if both run packages target the same refactor task.

## Result

Initial run on 2026-04-06: pass.

- No-plan total score: 7 / 16.
- Plan-driven total score: 16 / 16.
- Result quality improved from 6 / 7 to 7 / 7.
- Restartability improved from 1 / 5 to 5 / 5.
- Auditability improved from 0 / 4 to 4 / 4.

See `artifacts/no-plan-score.json`, `artifacts/with-plan-score.json`, `artifacts/run-comparison.json`, and `artifacts/run-2026-04-06.md`.
