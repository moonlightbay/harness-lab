# Repository Overview

Last updated: 2026-04-06

## Purpose

This template is a starter scaffold for a future host repository that wants a minimal but explicit harness for migration and refactor work.

## Core conventions

- The top-level map stays short.
- Every major topic has one clear source-of-truth file.
- Migration context lives in deeper docs with `[TO_FILL]` placeholders until the repository owner fills them.
- Multi-step migration work gets a checked-in execution plan.
- At least one architecture invariant should be encoded as a reusable check.

## Directory map

- `docs/knowledge/`: stable overview plus current-state and target-state migration context
- `docs/plans/`: active migration roadmap, execution plans, and migration log
- `docs/quality/`: migration rules and acceptance criteria
- `docs/workflows/`: Git and collaboration notes
- `checks/`: repo validation hooks

## Migration note

Start small. Fill the placeholder docs before large code moves, then keep repo-specific detail in the deeper docs rather than in the top-level map.
