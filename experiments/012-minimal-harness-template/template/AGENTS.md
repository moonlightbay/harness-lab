# AGENTS.md

## Repository purpose

This repository uses a small docs-first migration harness so agents can find the current map before moving code.

## How to work here

- Read `README.md`, `docs/knowledge/repository-overview.md`, and `docs/plans/migration-plan.md` before changing structure.
- Treat `docs/plans/migration-plan.md` as the source of truth for the active migration roadmap.
- Record outcomes in `docs/plans/migration-log.md`.
- Copy `docs/plans/execution-plan-template.md` for multi-step work.
- Fill the `[TO_FILL]` migration docs before major refactors.
- Run `checks/check-top-level-guidance.py` and repo-specific validation before finalizing.

## Expectations

- Keep `AGENTS.md` short.
- Keep top-level guidance current and singular.
- Encode at least one explicit architecture rule in `checks/architecture-rules.json`.
