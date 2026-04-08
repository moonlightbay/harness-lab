# Experiment 012 - Generic Harness Template

Last updated: 2026-04-08

## Goal

Turn the default-tier patterns from Experiment 011, plus the field-tested principles from a real host project, into one reusable generic harness template that any model agent can pick up without long chat history.

## Hypothesis

If the highest-value harness patterns are mostly low-cost structural rules, they should fit inside a small reusable scaffold instead of requiring a large framework. A validator should be able to prove that the scaffold includes the essential pieces for state compression, next-action control, wave execution, quality gates, cadence, entropy management, and harness self-improvement.

## Setup

- Source scoreboard: `../011-evaluation-harness/artifacts/evaluation-scoreboard.json`
- Template manifest: `manifest.json`
- Template root: `template/`
- Template validator: `validate-template.py`

The template includes the default-tier patterns plus the field-proven control mechanisms:

- short top-level map
- current singular top-level guidance
- checked-in execution plan template
- custom architecture rule hook
- branch-per-task worktree guidance
- `agent-state` + `next-action`
- fixed per-wave execution loop
- five-commit review cadence
- upstream sync as a translation task
- harness self-improvement via rules, checks, and skills

Excluded from the base template:

- role-divided workflow: useful, but conditional and expensive
- remediation-oriented live repair feedback: still needs more data

## Evaluation criteria

- Pass if the template includes every default-tier pattern from Experiment 011.
- Pass if the validator confirms that the template top-level map is small, current, and singular.
- Strong pass if the template also exposes reusable hooks for plans, architecture rules, and Git workflow without requiring repo-specific customization yet.

## Result

Latest run on 2026-04-08: pass.

- validator verdict: `pass`
- total checks passed: `16 / 16`
- top-level pack words: `287`
- stale references: `0`
- authority conflicts: `0`

Included modules:

- `AGENTS.md` + `README.md` as the short top-level map
- `docs/knowledge/repository-overview.md`
- `docs/knowledge/current-state.md`
- `docs/knowledge/desired-state.md`
- `docs/knowledge/work-scope.md`
- `docs/knowledge/operating-constraints.md`
- `docs/knowledge/boundaries-and-interfaces.md`
- `docs/knowledge/risk-register.md`
- `docs/state/agent-state.md`
- `docs/state/next-action.md`
- `docs/plans/active-plan.md`
- `docs/plans/work-log.md`
- `docs/plans/execution-plan-template.md`
- `docs/workflows/execution-loop.md`
- `docs/workflows/git-workflow.md`
- `docs/workflows/upstream-sync.md`
- `docs/workflows/harness-improvement.md`
- `docs/quality/working-rules.md`
- `docs/quality/quality-gates.md`
- `docs/quality/legacy-code-policy.md`
- `checks/check-top-level-guidance.py`
- `checks/check-architecture.py`
- `checks/architecture-rules.json`
- `skills/README.md`

Interpretation:

- The default-tier harness patterns can be compressed into a small scaffold without losing clarity.
- The resulting template is not tied to migration-only work. It can support refactors, feature work, cleanup, stabilization, and migration.
- The `agent-state` and `next-action` pair is now first-class, which makes handoff and resume much cheaper across agents and conversations.
- This gives the lab a concrete generic harness artifact instead of only a recommendation list.

See `artifacts/template-validation.json`, `artifacts/template-guidance-check.json`, `artifacts/template-architecture-check.json`, and `artifacts/run-2026-04-08.md`.
