# Initial Run - 2026-04-06

## Task

Before changing repository structure, identify the source-of-truth docs and active roadmap for `harness-lab`.

## Observed workflow

1. Read `AGENTS.md` to get the repository rules and required prereads.
2. Read `README.md`, `docs/knowledge/harness-engineering-overview.md`, and `docs/plans/experiment-plan.md` before any structural edits.
3. Read `docs/plans/experiment-log.md`, `docs/knowledge/source-notes.md`, and `experiments/README.md` for supporting context.
4. Capture top-level map metrics with `measure-map.ps1`.

## Measures

- Human clarifications: 0
- Required docs found before edit: yes
- Top-level navigation pack: 2 files, 39 lines, 294 words
- Top-level map metrics: see `top-level-map-metrics.json`

## Result

Pass. The short map was enough to guide the agent to the correct source-of-truth docs without repeated steering.

## Next change

Build the oversized-manual comparison case as Experiment 002 and reuse the same metric format.
