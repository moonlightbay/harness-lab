# Experiment Log

Use this file to record outcomes as the lab progresses.

## Template

### YYYY-MM-DD - Experiment name

- Layer:
- Hypothesis:
- Setup:
- Commands or workflow:
- Result:
- What worked:
- What failed:
- What to change next:
- Reusable lesson for `ms_bci_laboratory`:

## Entries

### 2026-04-06 - Lab initialized

- Layer: A / B / D groundwork
- Hypothesis: A small documentation-first repo is enough to begin learning harness engineering effectively.
- Setup: Initialized `harness-lab`, added `AGENTS.md`, overview notes, source notes, and an experiment plan.
- Commands or workflow: repo initialization and first documentation pass.
- Result: ready for the first real experiments.
- What worked: the smallest useful skeleton is clear.
- What failed: no runnable experiment exists yet.
- What to change next: add the first toy project and comparison scenario.
- Reusable lesson for `ms_bci_laboratory`: start with structure and plans before starting invasive refactors.

### 2026-04-06 - Experiment 001: source-of-truth discovery

- Layer: A with H groundwork
- Hypothesis: A short top-level repo map is enough for an agent to find the source-of-truth docs before editing, and the first cleanup rules can be derived from that run.
- Setup: Used the current `harness-lab` repo as the baseline docs-first case. Measured the top-level map with `experiments/001-source-of-truth-discovery/measure-map.ps1` and recorded the observed navigation path in the experiment folder.
- Commands or workflow: followed `AGENTS.md`, read `README.md`, `docs/knowledge/harness-engineering-overview.md`, and `docs/plans/experiment-plan.md` before editing; then generated `artifacts/top-level-map-metrics.json` from the measurement script.
- Result: pass. Required docs were found before any edits and no human clarification was needed.
- What worked: the short map made the source-of-truth docs explicit, and the top-level context stayed small enough to scan quickly.
- What failed: the oversized-manual comparison case has not been run yet, so the result is a baseline rather than a full A/B comparison.
- What to change next: build Experiment 002 for the giant-manual comparison and reuse the same measurement format.
- Reusable lesson for `ms_bci_laboratory`: keep the top-level agent map short, name the source-of-truth docs explicitly, and pair that with lightweight cleanup rules before the repo grows.
