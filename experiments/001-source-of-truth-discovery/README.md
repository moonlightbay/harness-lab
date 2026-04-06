# Experiment 001 - Source-of-Truth Discovery

Last updated: 2026-04-06

## Goal

Verify that a documentation-first repo with a short `AGENTS.md` lets an agent find the correct source-of-truth docs before making structural changes.

## Hypothesis

If the repo's top-level map is short and explicit, an agent can identify the required knowledge and planning docs with zero human clarification and low upfront context load.

## Setup

- Repo under test: current `harness-lab` root
- Agent task: before changing repository structure, identify the source-of-truth docs and active roadmap
- Top-level map under test: `AGENTS.md` and `README.md`
- Measurement artifacts: `measure-map.ps1`, `artifacts/top-level-map-metrics.json`, and `artifacts/initial-run-2026-04-06.md`

## Evaluation criteria

- Pass if the agent finds `README.md`, `docs/knowledge/harness-engineering-overview.md`, and `docs/plans/experiment-plan.md` before editing.
- Pass if no human clarification is required.
- Strong pass if the top-level map stays small enough to scan quickly and remains easy to update.
- Follow-up comparison: run the same task against an oversized-manual variant in Experiment 002.

## Result

Initial run on 2026-04-06: pass.

- Required docs were found before any edits.
- Human clarification required: 0.
- Top-level navigation pack: 2 files, 55 lines, 294 words.
- Top-level navigation pack metrics are stored in `artifacts/top-level-map-metrics.json`.
- The follow-up giant-manual comparison was completed in `../002-big-manual-comparison/`.
