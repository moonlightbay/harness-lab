# Migration Harness Template

A small docs-first scaffold for migrating and refactoring another repository with agent support.

Source of truth for repository overview: `docs/knowledge/repository-overview.md`
Source of truth for active migration roadmap: `docs/plans/migration-plan.md`
Source of truth for migration log: `docs/plans/migration-log.md`

## Layout

- `AGENTS.md`: short agent-facing map
- `docs/knowledge/`: repo overview plus migration context placeholders
- `docs/plans/`: migration roadmap, migration log, and plan template
- `docs/quality/`: migration rules and acceptance notes
- `docs/workflows/`: team workflow notes
- `checks/`: reusable validation hooks

## Suggested next steps

1. Read `docs/knowledge/repository-overview.md`.
2. Read `docs/plans/migration-plan.md`.
3. Fill the `[TO_FILL]` docs under `docs/knowledge/` and `docs/quality/`.
4. Copy `docs/plans/execution-plan-template.md` for each migration wave.
5. Add one repo-specific architecture rule and keep concurrent tasks in branch-per-task worktrees.
