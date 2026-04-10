# Experiment 012 - Lightweight Generic Harness Template

Last updated: 2026-04-10

## Goal

Refine the generic harness template so it keeps only the durable repository context that Codex cannot reliably carry across sessions by itself.

## Hypothesis

If Codex already provides solid session-level planning and execution flow, then the repo template can drop explicit state, next-action, workflow, and skill layers while still staying legible and resumable through a small set of checked-in docs plus one architecture rule hook.

## Setup

- Source scoreboard: `../011-evaluation-harness/artifacts/evaluation-scoreboard.json`
- Previous version: the 2026-04-08 generic harness variant in this experiment
- Template manifest: `manifest.json`
- Template root: `template/`
- Template validator: `validate-template.py`

The refined template keeps only these defaults:

- `docs/project.md`: durable repo purpose, current shape, constraints, and key paths
- `docs/architecture.md`: boundaries, stable interfaces, risk hotspots, and rule-hook location
- `docs/task.md`: one current task with scope, verification, and blockers
- `docs/log.md`: brief append-only work record
- `checks/check-top-level-guidance.py`
- `checks/check-architecture.py`
- `checks/architecture-rules.json`

It intentionally removes explicit `agent-state`, `next-action`, plan, workflow, quality-gate, and skill layers because those are partly redundant with Codex's built-in harness and increase read cost.

## Evaluation criteria

- Pass if the top-level pack stays short and points to one singular source of truth for project, architecture, task, and log.
- Pass if the validator confirms the four core docs and architecture rule hook are present and ready to fill.
- Strong pass if the scaffold remains generic enough for refactors, cleanup, migrations, and feature work without falling back into a large manual.

## Result

Latest run on 2026-04-10: pass.

- validator verdict: `pass`
- total checks passed: `12 / 12`
- top-level pack words: `183`
- stale references: `0`
- authority conflicts: `0`

Interpretation:

- The repo still needs checked-in durable context, but it does not need to mirror every step of the live agent loop.
- Keeping `project`, `architecture`, `task`, and `log` preserves handoff value while removing most document-hopping overhead.
- The architecture rule hook remains useful because it captures structural taste in a way the built-in harness alone cannot enforce.

See `artifacts/template-validation.json`, `artifacts/template-guidance-check.json`, `artifacts/template-architecture-check.json`, and `artifacts/run-2026-04-10.md`.
