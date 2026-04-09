# Model Training Harness Template

A compact docs-first scaffold for model-training repos.

This template borrows control ideas from Xiangyue Zhang's `auto-deep-researcher-24x7`: stable brief, rolling state, explicit next step, and a cheap loop. It does not copy that runtime.

Source of truth for training overview: `docs/knowledge/training-overview.md`
Source of truth for current agent state: `docs/state/agent-state.md`
Source of truth for next action queue: `docs/state/next-action.md`
Source of truth for active plan: `docs/plans/active-plan.md`
Source of truth for run log: `docs/plans/run-log.md`

## Layout

- `AGENTS.md`: short agent-facing map
- `docs/knowledge/`: brief, metrics, compute limits, and training context
- `docs/state/`: compressed state and next action
- `docs/plans/`: active plan, plan template, and run log
- `docs/quality/`: rules and quality gates
- `docs/workflows/`: training loop and sync cadence
- `checks/`: reusable validation hooks
- `skills/`: high-frequency operations worth skillifying

## Suggested next steps

1. Read `docs/knowledge/training-overview.md`.
2. Read `docs/state/agent-state.md`, `docs/state/next-action.md`, and `docs/plans/active-plan.md`.
3. Fill the `[TO_FILL]` docs before large experiment waves.
4. Copy `docs/plans/execution-plan-template.md` for the next slice.
5. Add one training rule and one verification command before agent edits start.
