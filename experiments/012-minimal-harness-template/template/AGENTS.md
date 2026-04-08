# AGENTS.md

## Repository purpose

This repository uses a small docs-first harness for long-running agent work across refactors, migrations, feature delivery, stabilization, and cleanup.

## Default read set

- `README.md`
- `docs/knowledge/repository-overview.md`
- `docs/state/agent-state.md`
- `docs/state/next-action.md`
- `docs/plans/active-plan.md`

Read deeper docs only when the task touches architecture boundaries, risky systems, upstream sync, or legacy cleanup.

## Expectations

- Keep `AGENTS.md` short.
- Keep top-level guidance current and singular.
- Keep `docs/state/agent-state.md` compressed and current.
- Keep `docs/state/next-action.md` limited to one queue item.
- Work in waves with allowed files, stop conditions, verification, and rollback.
- Close each wave with diff review, checks, verification, work-log update, and a local commit.
- Encode at least one explicit architecture rule in `checks/architecture-rules.json`.
- Turn recurring friction into a rule, check, or skill.
