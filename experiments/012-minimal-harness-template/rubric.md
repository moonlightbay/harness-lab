# Experiment 012 Rubric

The template is validated as a lightweight generic harness scaffold that assumes Codex already carries part of the live work loop.

## 1. Structural presence

- required files exist
- durable docs for project, architecture, current task, and log are all present
- architecture rule hook exists and has at least one sample rule

## 2. Top-level legibility

- `AGENTS.md` + `README.md` stay within the configured top-level word budget
- required top-level paths are all mentioned
- no stale markdown path references appear in the top-level pack
- no duplicate or conflicting source-of-truth claims appear in the top-level pack

## 3. Minimal durable context

- `docs/project.md` captures repo purpose, shape, constraints, and key paths
- `docs/architecture.md` captures boundaries, stable interfaces, hotspots, and rule hooks
- `docs/task.md` carries one current task plus verification and blockers
- `docs/log.md` stays brief and append-only

## 4. Placeholder discipline

- the checked-in docs contain `[TO_FILL]` markers and the expected sections
- the template makes it obvious which human-supplied context must be filled before large work begins

## 5. Outcome

- `pass`: all checks pass
- `fail`: one or more checks fail
