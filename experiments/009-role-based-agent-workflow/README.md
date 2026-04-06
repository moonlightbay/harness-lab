# Experiment 009 - Role-Based Agent Workflow

Last updated: 2026-04-06

## Goal

Compare a single generalist agent against a role-divided agent workflow, then measure whether role separation improves auditability and handoff quality on the same coding task.

## Hypothesis

If the same coding task is handled by a sequential role pipeline (`coordinator -> implementer -> reviewer -> repair`) instead of one generalist agent, final product quality should stay at least as good while coordination artifacts and review traceability improve. The tradeoff should be higher run cost.

## Setup

- Base task fixture: `fixtures/base-task/`
- Shared task description: `task.md`
- Role prompts: `prompts/`
- Workflow runner: `run-role-based-workflow.py`
- Single-run scorer: `score-workflow-run.py`
- Comparison script: `compare-role-workflows.py`
- Scoring rubric: `rubric.md`

Two workflows are run from the same base workspace:

- `single-generalist`
- `role-based`

The role-based workflow uses four sequential Codex sessions:

1. coordinator
2. implementer
3. reviewer
4. repair

## Evaluation criteria

- Pass if both workflows start from the same base task and complete real Codex runs.
- Pass if the role-based workflow matches or exceeds the single-agent product score.
- Strong pass if the role-based workflow produces a clearly better audit trail, even if it costs more tokens or turns.

## Result

Initial run on 2026-04-06: pass.

- `single-generalist`: product 11 / 11, auditability 3 / 8
- `role-based`: product 11 / 11, auditability 8 / 8
- Verdict: role division improves auditability at higher cost

Observed tradeoff:

- Both workflows reached the same final product quality.
- The role-based workflow produced a much richer coordination and review trail:
  - `coordination-brief.md`
  - `implementation-note.md`
  - `review.md`
  - `repair-note.md`
- The role-based workflow also cost much more:
  - sessions: `1 -> 4`
  - turns: `1 -> 4`
  - input tokens: `91320 -> 310519`
  - output tokens: `2663 -> 9245`

Interpretation:

- For a small coding task, role division did not improve the product itself.
- It did improve auditability and handoff quality substantially, which is the real value of the role-based pattern.

See `artifacts/single-generalist-score.json`, `artifacts/role-based-score.json`, `artifacts/role-workflow-comparison.json`, and `artifacts/run-2026-04-06.md`.
