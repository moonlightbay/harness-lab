# Experiment 011 - Evaluation Harness

Last updated: 2026-04-06

## Goal

Build a lightweight recurring evaluation harness that can score completed harness experiments under one shared scoreboard, then use it to decide which patterns should be adopted by default, which should stay conditional, and which still need more evidence.

## Hypothesis

If the lab already has enough scripted comparison artifacts, a small evaluation harness can normalize them into a common decision frame. The result should separate high-value default patterns from expensive or still-inconclusive ones without rerunning every underlying experiment.

## Setup

- Suite definition: `suite-spec.json`
- Normalization rubric: `rubric.md`
- Evaluator: `evaluate-suite.py`
- Scoreboard artifact: `artifacts/evaluation-scoreboard.json`
- Markdown summary artifact: `artifacts/evaluation-summary.md`

The suite covers seven representative comparison cases:

- short top-level map versus giant manual (`Experiment 002`)
- current singular guidance versus stale or duplicate guidance (`Experiment 010`)
- checked-in plan versus no plan (`Experiment 004`)
- custom architecture rule versus basic feedback only (`Experiment 005`)
- branch-per-task worktrees versus nested dirty branch (`Experiment 008`)
- role-divided workflow versus single generalist (`Experiment 009`)
- remediation-oriented live repair feedback versus generic failing check (`Experiment 007`)

## Evaluation criteria

- Pass if the evaluator can consume all listed comparison artifacts and emit one normalized scoreboard.
- Pass if the scoreboard distinguishes default patterns, conditional patterns, and inconclusive patterns.
- Strong pass if the resulting recommendations match the previously observed experiment conclusions while also exposing cost tradeoffs in one place.

## Result

Initial run on 2026-04-06: pass.

Recommendation tiers from the scoreboard:

- Default:
  - short top-level map
  - current singular top-level guidance
  - checked-in execution plan
  - custom architecture rule
  - branch-per-task worktrees
- Conditional:
  - role-divided workflow
- Needs more data:
  - remediation-oriented live repair feedback

Observed pattern:

- The highest-value defaults were all low-cost structure or process rules.
- The role-divided workflow delivered strong steering and auditability gains, but its token and session cost kept it out of the default tier.
- The live repair feedback comparison stayed inconclusive, so the evaluation harness correctly refused to overclaim.

Interpretation:

- The lab now has a repeatable way to compare harness ideas instead of relying on isolated experiment summaries.
- The next step should be to reuse this evaluation harness after future experiments so the migration recommendation set stays current.

See `artifacts/evaluation-scoreboard.json`, `artifacts/evaluation-summary.md`, and `artifacts/run-2026-04-06.md`.
