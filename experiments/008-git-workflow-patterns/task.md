# Task

Compare two Git working patterns for agent-heavy development.

Task A:

- update `src/feature_a.py`
- add an alpha note to `README.md`

Task B:

- update `src/feature_b.py`
- add a beta note to `README.md`

Scenario 1 keeps both tasks nested in one dirty branch and one workspace.

Scenario 2 gives each task its own branch and its own worktree.

The question is not whether Git can represent both states. The question is which state is easier to resume, review, discard, and ship without manual diff surgery.
