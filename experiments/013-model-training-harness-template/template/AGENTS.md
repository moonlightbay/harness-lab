# AGENTS.md

## Repository purpose

This repository uses a small docs-first harness for model training.

## Default read set

- `README.md`
- `docs/knowledge/training-overview.md`
- `docs/state/agent-state.md`
- `docs/state/next-action.md`
- `docs/plans/active-plan.md`

Read deeper docs only when the task changes metrics, datasets, compute, or upstream interfaces.

## Expectations

- Keep `AGENTS.md` short.
- Keep top-level guidance current and singular.
- Keep `docs/state/agent-state.md` compressed and current.
- Keep `docs/state/next-action.md` limited to one queue item.
- Work in waves with allowed files, stop conditions, verification, and rollback.
- Close each wave with diff review, checks, dry-run, verification, run-log update, and a local commit.
- Treat mainline sync as a translation task.
- Turn repeated friction into a rule, check, or skill.
