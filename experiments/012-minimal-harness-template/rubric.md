# Experiment 012 Rubric

The template is validated as a generic harness scaffold, not a migration-only starter.

## 1. Structural presence

- required files exist
- execution plan template contains the required sections
- architecture rule hook exists and has at least one sample rule
- state, plan, quality, workflow, and skill layers are all present

## 2. Top-level legibility

- `AGENTS.md` + `README.md` stay within the configured top-level word budget
- required top-level paths are all mentioned
- no stale markdown path references appear in the top-level pack
- no duplicate or conflicting source-of-truth claims appear in the top-level pack

## 3. Workflow coverage

- the execution loop covers minimal-context reading, wave execution, diff review, verification, logging, and local commit closeout
- the Git workflow covers branch-per-task worktrees and a five-commit review cadence
- the upstream sync note frames mainline changes as translation work
- the harness-improvement note explains how repeated friction becomes a rule, check, or skill
- the legacy code policy classifies messy code before deletion

## 4. Placeholder discipline

- the long-lived context docs contain `[TO_FILL]` markers and the expected sections
- the template makes it obvious which human-supplied context must be filled before large work begins

## 5. Outcome

- `pass`: all checks pass
- `fail`: one or more checks fail
