# Architecture Rules

This template expects at least one repo-specific architecture rule.

## Rule shape

Each rule should answer:

- what boundary must hold
- how to detect a violation
- how to remediate the violation
- what to rerun after the fix

## Current hook

See `checks/architecture-rules.json` and `checks/check-architecture.py`.

## Related migration docs

- `docs/quality/migration-rules.md`
- `docs/quality/acceptance-checklist.md`
