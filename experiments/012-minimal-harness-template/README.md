# Experiment 012 - Migration Harness Template

Last updated: 2026-04-06

## Goal

Turn the default-tier patterns from Experiment 011 into one reusable migration harness template, then validate that the template stays small, current, and structurally ready for guided refactors in another repository.

## Hypothesis

If the highest-value harness patterns are mostly low-cost structural rules, they should fit inside a small reusable migration scaffold instead of requiring a large framework. A validator should be able to prove that the scaffold includes the essential pieces, plus the key migration placeholder docs, without drifting into a giant manual.

## Setup

- Source scoreboard: `../011-evaluation-harness/artifacts/evaluation-scoreboard.json`
- Template manifest: `manifest.json`
- Template root: `template/`
- Template validator: `validate-template.py`

The template includes only the default-tier patterns:

- short top-level map
- current singular top-level guidance
- checked-in execution and migration plan templates
- custom architecture rule hook
- branch-per-task worktree guidance

The template also adds migration-specific placeholder docs that the target repository owner must fill before large refactors start:

- current system inventory
- target architecture
- migration scope
- domain constraints
- migration rules
- acceptance checklist

Excluded from the base template:

- role-divided workflow: useful, but conditional and expensive
- remediation-oriented live repair feedback: still needs more data

## Evaluation criteria

- Pass if the template includes every default-tier pattern from Experiment 011.
- Pass if the validator confirms that the template top-level map is small, current, and singular.
- Strong pass if the template also exposes reusable hooks for plans, architecture rules, and Git workflow without requiring repo-specific customization yet.

## Result

Initial run on 2026-04-06: pass.

- validator verdict: `pass`
- total checks passed: `11 / 11`
- top-level pack words: `220`
- stale references: `0`
- authority conflicts: `0`

Included modules:

- `AGENTS.md` + `README.md` as the short top-level map
- `docs/knowledge/repository-overview.md`
- `docs/knowledge/current-system.md`
- `docs/knowledge/target-architecture.md`
- `docs/knowledge/migration-scope.md`
- `docs/knowledge/domain-constraints.md`
- `docs/plans/migration-plan.md`
- `docs/plans/migration-log.md`
- `docs/plans/execution-plan-template.md`
- `docs/workflows/git-workflow.md`
- `docs/quality/migration-rules.md`
- `docs/quality/acceptance-checklist.md`
- `checks/check-top-level-guidance.py`
- `checks/check-architecture.py`
- `checks/architecture-rules.json`

Interpretation:

- The default-tier harness patterns can be compressed into a small scaffold without losing clarity.
- The resulting template is not a framework. It is a migration-ready repo starter plus two validation hooks and a set of explicit placeholder docs.
- This gives the lab a concrete migration artifact instead of only a recommendation list.

See `artifacts/template-validation.json`, `artifacts/template-guidance-check.json`, `artifacts/template-architecture-check.json`, and `artifacts/run-2026-04-06.md`.
