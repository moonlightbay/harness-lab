# AGENTS.md

## Repository purpose

This repository is a small experimental lab for learning harness engineering before applying it to a larger host project.

## How to work here

- Keep the repository documentation-first.
- Prefer small experiments over large frameworks.
- Treat `docs/knowledge/` as the source of truth for research notes.
- Treat `docs/plans/experiment-plan.md` as the source of truth for the active learning roadmap.
- Record experiment outcomes in `docs/plans/experiment-log.md`.

## Expectations for agents

- Before changing structure, read `README.md`, `docs/knowledge/harness-engineering-overview.md`, and `docs/plans/experiment-plan.md`.
- Keep `AGENTS.md` short; deeper detail belongs in `docs/`.
- When adding a new experiment, create a dedicated folder under `experiments/` and document:
  - goal
  - hypothesis
  - setup
  - evaluation criteria
  - result
- Prefer reproducible scripts and written findings over ad hoc notes.

## Quality bar

- Every experiment should produce an artifact: code, script, plan, or written conclusion.
- Every experiment should define success criteria before implementation.
- If a rule becomes stable and repeatedly useful, move it from notes into repository structure or automation.
