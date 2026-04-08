# Git Workflow

## Default rule

Use branch-per-task worktrees when two active tasks need isolation at the same time.

## Review cadence

Pause every `5 commits` for a branch-level review, plan correction, and push decision.

## Why

- a worktree keeps each task reviewable
- a branch-per-task layout reduces cross-task contamination
- restart and rollback stay clearer than nested dirty changes in one branch

## Suggested commands

1. Create a branch for the task.
2. Create a worktree for that branch.
3. Keep commits small and scoped to one task.
4. Stop after `5 commits` for a review gate before continuing deeper.
5. Remove the worktree after the task is merged or discarded.
