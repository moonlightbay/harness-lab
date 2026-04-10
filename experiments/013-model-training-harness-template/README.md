# Experiment 013 - Minimal Model Training Scaffold

Last updated: 2026-04-10

## Goal

Refine the training harness again so the repository keeps only training-specific durable context and structure guidance, without duplicating Codex's session-level harness.

## Hypothesis

If the scaffold keeps only project facts, repo-shape guidance, and a short work log, then it should stay useful for training work without repeating the task-tracking loop Codex already provides.

## Setup

- Inspiration source: `https://github.com/Xiangyue-Zhang/auto-deep-researcher-24x7`
- Previous version: the 2026-04-09 training harness variant in this experiment
- Template manifest: `manifest.json`
- Template root: `template/`
- Validator: `validate-template.py`

The refined scaffold keeps only these defaults:

- `docs/project.md`: stable project context, baseline, metrics, constraints, and repo shape
- `docs/log.md`: brief append-only work record
- `configs/`, `src/`, and `scripts/` guides for training repo structure
- `checks/check-top-level-guidance.py` for top-level map health

It intentionally drops checked-in task tracking, plans, workflows, quality rules, and skills from the copied template so the starter stays focused on the parts Codex cannot carry across sessions by itself.

## Evaluation criteria

- Pass if the top-level pack stays short and points to one singular set of source-of-truth docs.
- Pass if the validator confirms the two core docs and three structure guides are present and ready to fill.
- Strong pass if the scaffold gives enough direction for agents to create a sane training layout without needing a long manual.

## Result

Refinement run on 2026-04-10: pass.

- validator verdict: `pass`
- total checks passed: `9 / 9`
- top-level pack words: `140`
- stale references: `0`
- authority conflicts: `0`

Interpretation:

- The most reusable part of the training template is the durable project brief plus the directory contract, not the checked-in task loop.
- Removing `docs/task.md` avoids mirroring Codex's own plan and next-step management.
- Keeping `configs/README.md`, `src/README.md`, and `scripts/README.md` preserves the part that actually helps an agent shape a good training repository.

See `artifacts/template-guidance-check.json`, `artifacts/template-validation.json`, and `artifacts/run-2026-04-10.md`.
