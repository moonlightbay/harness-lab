# experiments

This directory holds small, isolated experiments.

Current experiments:

- `001-source-of-truth-discovery/`: verifies that a short repo map is enough for an agent to find the source-of-truth docs before editing.
- `002-big-manual-comparison/`: compares the short top-level map with an oversized single-manual variant.
- `003-garbage-collection-pass/`: turns the cleanup checklist into a repeatable audit against dirty and clean snapshots.
- `004-plan-vs-no-plan/`: compares no-plan and plan-driven run packages on the same refactor task.
- `005-lint-feedback-loop/`: compares basic functional checks with a stronger feedback loop that adds a custom architecture rule.
- `006-feedback-representation-loop/`: compares four ways of expressing the same architecture failure and scores which one is most loop-ready for agent repair.

Planned next experiments:

- `git-workflow-patterns/`
- `multi-agent-split-task/`
