# Experiment 003 - Garbage Collection Pass

Last updated: 2026-04-06

## Goal

Turn the initial garbage-collection checklist into a repeatable audit pass that can detect stale planning state, missing experiment bookkeeping, duplicate helpers, orphan artifacts, and placeholder files.

## Hypothesis

A lightweight audit script run against a small repo snapshot should catch at least stale state and one duplication pattern, and a cleaned snapshot should reduce those findings to zero without requiring a heavy framework.

## Setup

- Dirty fixture: `fixtures/dirty/`
- Clean fixture: `fixtures/clean/`
- Audit script: `audit-garbage-collection.ps1`
- Comparison script: `compare-audit-runs.ps1`
- Supporting note: `golden-principles.md`

## Evaluation criteria

- Pass if the dirty fixture produces at least four findings across more than one category.
- Pass if the clean fixture produces zero findings.
- Strong pass if the findings map directly back to the checklist and are easy to explain to a later reader.

## Result

Initial run on 2026-04-06: pass.

- Dirty fixture findings: 5 across 5 categories.
- Clean fixture findings: 0.
- Cleanup effectiveness: 100%.
- The audit caught planned/current overlap, missing log coverage, an orphan artifact, duplicate helper logic, and a placeholder file.

See `artifacts/dirty-audit.json`, `artifacts/clean-audit.json`, `artifacts/audit-comparison.json`, and `artifacts/run-2026-04-06.md`.
