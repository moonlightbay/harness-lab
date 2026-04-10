# Generic Harness Template

A small docs-first scaffold for long-running agent work with Codex.

Source of truth for project context: `docs/project.md`
Source of truth for architecture notes: `docs/architecture.md`
Source of truth for current task: `docs/task.md`
Source of truth for work log: `docs/log.md`

## Layout

- `AGENTS.md`: short agent-facing map
- `docs/`: durable context, current task, and short log
- `checks/`: reusable validation hooks

## Suggested next steps

1. Read `docs/project.md` and `docs/task.md`.
2. Read `docs/architecture.md` before structural changes.
3. Fill the `[TO_FILL]` docs before large changes start.
4. Add one repo-specific architecture rule in `checks/architecture-rules.json`.
