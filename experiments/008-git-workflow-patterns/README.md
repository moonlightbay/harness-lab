# Experiment 008 - Git Workflow Patterns

Last updated: 2026-04-06

## Goal

Compare nested dirty changes in one branch against branch-per-task worktrees, then measure which Git pattern gives clearer isolation and easier recovery for agent-heavy work.

## Hypothesis

If two independent tasks stay nested in one dirty branch, review scope and restart clarity will degrade. If each task gets its own branch and worktree, isolation should improve enough to remove manual splitting and cross-task contamination.

## Setup

- Fixture template: `fixtures/repo-template/`
- Workflow spec: `workflow-spec.json`
- Scenario runner: `run-git-workflow-comparison.py`
- Scoring script: `compare-workflow-patterns.py`
- Scoring rubric: `rubric.md`

The experiment builds two Git scenarios from the same fixture repo:

- `nested-single-branch`: task A and task B accumulate in one dirty branch and one workspace
- `branch-per-task-worktrees`: task A and task B live in separate branches and separate worktrees

## Evaluation criteria

- Pass if both scenarios are created from the same base commit.
- Pass if the worktree scenario scores higher on task isolation and resume clarity.
- Strong pass if the nested scenario requires manual splitting while the worktree scenario does not.

## Result

Initial run on 2026-04-06: pass.

- `nested-single-branch`: 0 / 8
- `branch-per-task-worktrees`: 8 / 8
- Delta: +8 in favor of the worktree pattern
- Verdict: branch-per-task worktrees preserve task isolation better

Observed difference:

- The nested branch accumulated `README.md`, `src/feature_a.py`, and `src/feature_b.py` in one dirty workspace, so neither task had a dedicated reviewable scope.
- The worktree pattern kept task A in `worktree-a` and task B in `worktree-b`, each with exactly two changed files and only its own README marker.

See `artifacts/nested-scenario.json`, `artifacts/worktree-scenario.json`, `artifacts/workflow-comparison.json`, and `artifacts/run-2026-04-06.md`.
