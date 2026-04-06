# Experiment 007 - Live Repair A/B

Last updated: 2026-04-06

## Goal

Run two real Codex repair loops against the same broken workspace, then compare whether a remediation-oriented architecture check produces a better live repair outcome than a generic failing check.

## Hypothesis

If both runs start from the same broken snapshot and use the same prompt, a remediation-oriented failing check should either:

- achieve a higher final score, or
- achieve the same final score with fewer turns or less token usage

than a generic failing check.

## Setup

- Base broken fixture: `fixtures/base-broken-workspace/`
- Generic-check overlay: `overlays/generic-check/check-architecture.py`
- Remediation-check overlay: `overlays/remediation-check/check-architecture.py`
- Shared live prompt: `prompts/live-repair.txt`
- Run preparation script: `prepare-live-runs.ps1`
- Run executor: `run-live-repair-ab.ps1`
- Single-run scorer: `score-live-run.py`
- Comparison script: `compare-live-runs.py`

Each run gets:

- the same broken workspace
- the same task text
- the same `verify-basic.py`
- the same Codex model and CLI settings

The only intentional difference is the runtime feedback style emitted by `check-architecture.py`.

## Evaluation criteria

- Pass if both live runs execute from isolated workspaces generated from the same fixture.
- Pass if the remediation-check run outperforms the generic-check run on final score or on repair cost.
- Strong pass if the remediation-check run reaches 11 / 11 while the generic-check run does not.

## Result

Initial run on 2026-04-06: inconclusive.

- Both runs reached 11 / 11 and fully repaired the workspace in one Codex turn.
- `generic-check`: 11 / 11, 1 turn, 123871 input tokens, 2219 output tokens, 2 changed files.
- `remediation-check`: 11 / 11, 1 turn, 105458 input tokens, 2931 output tokens, 3 changed files.
- Verdict: inconclusive. The remediation check used fewer input tokens, but it also produced more output tokens and touched one extra file (`verify-basic.py`), so the cost signals moved in different directions.

Interpretation:

- On this small repair target, the generic failing check was already strong enough for Codex to recover fully.
- The remediation-oriented check did not improve final correctness, but it did change the repair path and encouraged a more harness-friendly update to `verify-basic.py`.

See `artifacts/generic-check-score.json`, `artifacts/remediation-check-score.json`, `artifacts/live-comparison.json`, `artifacts/generic-check-final.txt`, `artifacts/remediation-check-final.txt`, and `artifacts/run-2026-04-06.md`.
