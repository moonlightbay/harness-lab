# Generic Harness Template

A small docs-first scaffold for long-running agent work with any model agent.

Source of truth for repository overview: `docs/knowledge/repository-overview.md`
Source of truth for current agent state: `docs/state/agent-state.md`
Source of truth for next action queue: `docs/state/next-action.md`
Source of truth for active plan: `docs/plans/active-plan.md`
Source of truth for work log: `docs/plans/work-log.md`

## Layout

- `AGENTS.md`: short agent-facing map
- `docs/knowledge/`: durable context, boundaries, and risks
- `docs/state/`: compressed current state and next action
- `docs/plans/`: active plan, plan template, and work log
- `docs/quality/`: rules, quality gates, and legacy code policy
- `docs/workflows/`: execution loop, git cadence, upstream sync, and harness improvement
- `checks/`: reusable validation hooks
- `skills/`: reusable high-frequency operations

## Suggested next steps

1. Read `docs/knowledge/repository-overview.md`.
2. Read `docs/state/agent-state.md`, `docs/state/next-action.md`, and `docs/plans/active-plan.md`.
3. Fill the `[TO_FILL]` docs before large changes start.
4. Copy `docs/plans/execution-plan-template.md` for the next wave or slice.
5. Add one repo-specific architecture rule and keep concurrent tasks in branch-per-task worktrees.
