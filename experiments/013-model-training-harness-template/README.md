# Experiment 013 - Model Training Harness Template

Last updated: 2026-04-09

## Goal

Create a compact reusable harness template for model-training repositories that keeps long-running agent work controllable, cheap to resume, and easy to hand off across different model agents.

## Hypothesis

If the training template keeps only the shortest useful control surface, then one scaffold can support training code creation, tuning, debugging, reproduction, and reporting without turning into a training platform or a giant manual.

## Setup

- Inspiration source: `https://github.com/Xiangyue-Zhang/auto-deep-researcher-24x7`
- Base lab template: `../012-minimal-harness-template/template/`
- Template manifest: `manifest.json`
- Template root: `template/`
- Validator: `validate-template.py`

The new template keeps these core surfaces:

- stable training brief
- compressed agent state
- single next-action queue
- wave-based execution plan
- run log
- training rules and quality gates
- top-level guidance check
- training-rule check

It intentionally does not include a runtime loop, a scheduler, GPU code, or slash commands. It is a repo harness, not an execution engine.

## Evaluation criteria

- Pass if the template stays small and top-level guidance remains current and singular.
- Pass if the validator confirms the required training docs, checks, and placeholders exist.
- Strong pass if the template exposes a full training work loop with brief, wave, verification, run log, commit cadence, and upstream-sync handling while remaining concise.

## Result

Initial run on 2026-04-09: pass.

- validator verdict: `pass`
- total checks passed: `13 / 13`
- top-level pack words: `289`
- stale references: `0`
- authority conflicts: `0`

Interpretation:

- The borrowed idea from `auto-deep-researcher-24x7` is not the runtime implementation. It is the control shape: stable brief, rolling state, explicit next step, and low-cost recurring loop.
- The template stays docs-first and model-agnostic, so any capable agent can pick it up without depending on one vendor runtime.
- The training-specific additions are narrow: experiment brief, evaluation protocol, compute-and-ops note, run log, and training rules.

See `artifacts/template-guidance-check.json`, `artifacts/template-training-rules-check.json`, `artifacts/template-validation.json`, and `artifacts/run-2026-04-09.md`.
