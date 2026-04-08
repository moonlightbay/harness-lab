# Repository Overview

Last updated: 2026-04-06

## Purpose

This template is a starter scaffold for a repository that wants a minimal but explicit harness for long-running agent work.

## Core conventions

- The top-level map stays short.
- Every major topic has one clear source-of-truth file.
- Current state and next action are kept in separate short docs.
- Long-running work is split into waves or slices with explicit boundaries.
- Durable context lives in deeper docs with `[TO_FILL]` placeholders until the repository owner fills them.
- At least one architecture invariant should be encoded as a reusable check.

## Directory map

- `docs/knowledge/`: stable overview, boundaries, interfaces, constraints, and risks
- `docs/state/`: compressed state for handoff and continuation
- `docs/plans/`: active plan, execution plans, and work log
- `docs/quality/`: stable rules, gates, architecture checks, and legacy code policy
- `docs/workflows/`: execution loop, cadence, upstream sync, and harness improvement
- `checks/`: repo validation hooks
- `skills/`: reusable high-frequency operations

## Usage note

Start small. Fill the placeholder docs before large code moves, then keep repo-specific detail in the deeper docs rather than in the top-level map.
