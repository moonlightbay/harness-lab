# Experiment 002 - Big Manual Comparison

Last updated: 2026-04-06

## Goal

Compare the current short top-level repo map against an oversized single-manual variant and measure how much discoverability degrades even when required paths are still present.

## Hypothesis

An oversized manual can preserve path coverage, but it will make the first useful instruction harder to find by increasing scan cost, delaying the first mention of key paths, and lowering signal density.

## Setup

- Baseline pack: `AGENTS.md` and `README.md`
- Comparison pack: `fixtures/MEGA-MANUAL.md`
- Shared measurement script: `../shared/measure-navigation-pack.ps1`
- Comparison script: `compare-navigation-packs.ps1`
- Required paths:
  - `README.md`
  - `docs/knowledge/harness-engineering-overview.md`
  - `docs/plans/experiment-plan.md`
  - `docs/plans/experiment-log.md`

## Evaluation criteria

- The comparison is valid only if both packs cover all required paths.
- The giant manual is considered structurally worse if it is much longer and pushes the first useful path references significantly later in the reading order.
- A strong negative result for the giant manual means it adds context load without adding navigation value.

## Result

Initial run on 2026-04-06: the giant manual remained functionally complete but was structurally worse than the short map.

- Both packs covered all four required paths.
- Baseline pack: 2 files, 55 lines, 294 words.
- Giant manual pack: 1 file, 201 lines, 1036 words.
- First required path mention moved from pack line 12 to pack line 185.
- Average first-mention position moved from 14.75 to 188.
- Required-path mentions per 100 words dropped from 2.72 to 0.48.

See `artifacts/navigation-pack-comparison.json` and `artifacts/run-2026-04-06.md` for the recorded comparison.
