# Training Rules

## Stable rules

- Keep one trusted baseline visible at all times.
- Change one training slice per wave unless the plan says otherwise.
- Do not claim wins without the evaluation protocol.
- Keep long context in docs, not in chat history.

## Forbidden patterns

- Mixing data, model, infra, and reporting changes in one undocumented wave.
- Comparing against an unclear baseline.
- Leaving logs or notes updated without the matching verification command.
- Treating mainline sync as free context instead of a declared translation task.

## Promotion path

When a rule repeats often enough, move it from prose into `checks/training-rules.json` or into a reusable skill.
