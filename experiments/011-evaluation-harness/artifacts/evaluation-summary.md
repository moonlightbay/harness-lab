# Evaluation Harness Summary

Generated at: 2026-04-06T21:31:45.201881+08:00

## Recommendation tiers

### default
- `short-top-level-map`: net=12 (primary=4, steering=4, reproducibility=4, cost=0)
- `current-singular-guidance`: net=12 (primary=4, steering=4, reproducibility=4, cost=0)
- `checked-in-execution-plan`: net=11 (primary=4, steering=4, reproducibility=4, cost=1)
- `custom-architecture-rule`: net=9 (primary=3, steering=3, reproducibility=4, cost=1)
- `branch-per-task-worktrees`: net=11 (primary=4, steering=4, reproducibility=4, cost=1)

### conditional
- `role-divided-workflow`: net=2 (primary=0, steering=4, reproducibility=2, cost=4)

### needs-more-data
- `remediation-oriented-live-feedback`: net=1 (primary=0, steering=1, reproducibility=2, cost=2)

## Ranked cases

- `current-singular-guidance` -> `default` (net=12, verdict=coverage-alone-does-not-protect-agent-legibility)
- `short-top-level-map` -> `default` (net=12, verdict=giant-manual-is-functionally-complete-but-structurally-worse)
- `branch-per-task-worktrees` -> `default` (net=11, verdict=worktree-pattern-preserves-task-isolation-better)
- `checked-in-execution-plan` -> `default` (net=11, verdict=plan-driven-run-is-easier-to-resume-and-audit)
- `custom-architecture-rule` -> `default` (net=9, verdict=strong-feedback-loop-preserves-structure-better)
- `role-divided-workflow` -> `conditional` (net=2, verdict=role-division-improves-auditability-at-higher-cost)
- `remediation-oriented-live-feedback` -> `needs-more-data` (net=1, verdict=inconclusive)
