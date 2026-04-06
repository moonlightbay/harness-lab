# Experiment Log

Use this file to record outcomes as the lab progresses.

## Template

### YYYY-MM-DD - Experiment name

- Layer:
- Hypothesis:
- Setup:
- Commands or workflow:
- Result:
- What worked:
- What failed:
- What to change next:
- Reusable lesson for future host repos:

## Entries

### 2026-04-06 - Lab initialized

- Layer: A / B / D groundwork
- Hypothesis: A small documentation-first repo is enough to begin learning harness engineering effectively.
- Setup: Initialized `harness-lab`, added `AGENTS.md`, overview notes, source notes, and an experiment plan.
- Commands or workflow: repo initialization and first documentation pass.
- Result: ready for the first real experiments.
- What worked: the smallest useful skeleton is clear.
- What failed: no runnable experiment exists yet.
- What to change next: add the first toy project and comparison scenario.
- Reusable lesson for future host repos: start with structure and plans before starting invasive refactors.

### 2026-04-06 - Experiment 001: source-of-truth discovery

- Layer: A with H groundwork
- Hypothesis: A short top-level repo map is enough for an agent to find the source-of-truth docs before editing, and the first cleanup rules can be derived from that run.
- Setup: Used the current `harness-lab` repo as the baseline docs-first case. Measured the top-level map with `experiments/001-source-of-truth-discovery/measure-map.ps1` and recorded the observed navigation path in the experiment folder.
- Commands or workflow: followed `AGENTS.md`, read `README.md`, `docs/knowledge/harness-engineering-overview.md`, and `docs/plans/experiment-plan.md` before editing; then generated `artifacts/top-level-map-metrics.json` from the measurement script.
- Result: pass. Required docs were found before any edits and no human clarification was needed.
- What worked: the short map made the source-of-truth docs explicit, and the top-level context stayed small enough to scan quickly.
- What failed: the baseline alone could not prove that the short map was better than a larger but complete alternative.
- What to change next: extend the comparison into cleanup and stale-doc failure cases.
- Reusable lesson for future host repos: keep the top-level agent map short, name the source-of-truth docs explicitly, and pair that with lightweight cleanup rules before the repo grows.

### 2026-04-06 - Experiment 002: big manual comparison

- Layer: A / B
- Hypothesis: A giant single-manual instruction file can preserve required-path coverage but still reduce discoverability by increasing scan cost and burying the useful file references.
- Setup: Reused the required paths from Experiment 001, created `experiments/002-big-manual-comparison/fixtures/MEGA-MANUAL.md` as the oversized-manual fixture, and compared it against the baseline pack with `experiments/002-big-manual-comparison/compare-navigation-packs.ps1`.
- Commands or workflow: measured the baseline pack (`AGENTS.md` + `README.md`) and the fixture manual with the shared script `experiments/shared/measure-navigation-pack.ps1`, then wrote the comparison output to `artifacts/navigation-pack-comparison.json`.
- Result: the comparison succeeded and the giant manual was functionally complete but structurally worse. Both packs covered all four required paths, but the giant manual expanded from 294 to 1036 words, pushed the first required path mention from line 12 to line 185, and dropped path-mention density from 2.72 to 0.48 per 100 words.
- What worked: the shared measurement script made the A/B comparison repeatable and showed that coverage alone is not enough; placement and density also matter.
- What failed: this is still a synthetic fixture, not a blinded multi-agent study, so the result is strong structural evidence rather than a broad behavioral benchmark.
- What to change next: run the same comparison against stale-doc and duplicate-guidance variants, then turn the cleanup checklist into a repeatable garbage-collection pass.
- Reusable lesson for future host repos: do not replace a short repo map with a single large manual. Keep top-level guidance short, link outward, and measure discoverability with concrete proxies instead of relying on completeness alone.

### 2026-04-06 - Experiment 003: garbage collection pass

- Layer: H
- Hypothesis: A lightweight audit pass can reliably catch repo entropy such as stale planning state, missing bookkeeping, duplicate helpers, orphan artifacts, and placeholders, and a cleaned snapshot should reduce those findings to zero.
- Setup: Created a dirty fixture and a clean fixture under `experiments/003-garbage-collection-pass/fixtures/`, then implemented `audit-garbage-collection.ps1` and `compare-audit-runs.ps1` to evaluate both snapshots with the same rules.
- Commands or workflow: ran the audit against `fixtures/dirty/` and `fixtures/clean/`, wrote the outputs to `artifacts/dirty-audit.json` and `artifacts/clean-audit.json`, then compared them in `artifacts/audit-comparison.json`.
- Result: pass. The dirty fixture produced 5 findings across 5 categories, the clean fixture produced 0 findings, and the comparison reported 100% cleanup effectiveness.
- What worked: the audit categories were simple but covered multiple realistic entropy modes, and the before/after fixture pair made the result reproducible instead of anecdotal.
- What failed: the audit rules are still heuristic and snapshot-based; they do not yet inspect semantic drift inside full prose documents.
- What to change next: carry the same discipline into the next experiment by testing whether explicit checked-in plans improve restartability on a longer multi-step task.
- Reusable lesson for future host repos: repository garbage collection should be treated as a normal automated hygiene pass. Even simple checks catch real drift before it compounds into agent-facing confusion.

### 2026-04-06 - Experiment 004: plan vs no plan

- Layer: D
- Hypothesis: A checked-in execution plan should improve restartability and auditability on a medium-complexity refactor, and it should reduce the chance of missing low-salience requirements.
- Setup: Defined one shared refactor task in `experiments/004-plan-vs-no-plan/task.md`, then created two run packages under `runs/no-plan/` and `runs/with-plan/` for the same task. Implemented `verify-workspace.ps1`, `score-run-package.ps1`, and `compare-run-packages.ps1` to score both packages with the same rubric.
- Commands or workflow: scored the no-plan package into `artifacts/no-plan-score.json`, scored the plan-driven package into `artifacts/with-plan-score.json`, then compared them in `artifacts/run-comparison.json`.
- Result: pass. The no-plan package scored 7 / 16 and the plan-driven package scored 16 / 16. The plan-driven run improved result quality by 1 point, restartability by 4 points, and auditability by 4 points.
- What worked: the controlled task and scoring rubric made the comparison inspectable, and the split between workspace verification and run-package scoring made it clear that plans help even when the code changes are similar.
- What failed: this is still a controlled run-package comparison rather than a blind repeated trial with multiple agents, so it is better as structural evidence than as a performance benchmark.
- What to change next: move on to `lint-feedback-loop/` and test whether explicit feedback loops improve output consistency on a toy codebase.
- Reusable lesson for future host repos: for multi-step refactors, plans should be treated as executable artifacts, not optional notes. They materially improve handoff, review, and restart quality even when the final code looks similar.

### 2026-04-06 - Experiment 005: lint feedback loop

- Layer: C
- Hypothesis: Syntax checks and unit tests can still allow structurally poor agent output, while adding one custom architecture rule can preserve layering and reduce duplicated logic.
- Setup: Defined one shared toy refactor task in `experiments/005-lint-feedback-loop/task.md`, then created `runs/basic-feedback/` and `runs/strong-feedback/` for the same task. Implemented `verify-basic.py`, `check-architecture.py`, `score-feedback-run.py`, and `compare-feedback-runs.py` to score both runs with the same rubric.
- Commands or workflow: scored the basic-feedback run into `artifacts/basic-feedback-score.json`, scored the strong-feedback run into `artifacts/strong-feedback-score.json`, then compared them in `artifacts/feedback-comparison.json`.
- Result: pass. Both runs passed all five functional checks, but the basic-feedback run scored only 3 / 6 on architecture while the strong-feedback run scored 6 / 6. Total score improved from 8 / 11 to 11 / 11.
- What worked: the toy task isolated the failure mode cleanly. Basic feedback was enough to pass syntax and tests, but it still allowed domain logic and report-building logic to drift into `cli.py`.
- What failed: this is still a controlled artifact comparison, not a repeated study over many tasks or models, so it demonstrates the shape of the problem rather than a population-level benchmark.
- What to change next: compare how the same invariant behaves under requirement-only feedback, review comments, generic failing checks, and remediation-oriented failing checks before moving on to Git workflow.
- Reusable lesson for future host repos: tests are necessary but not sufficient. A small custom structure rule can catch degradations that functional checks will happily let through.

### 2026-04-06 - Experiment 006: feedback representation loop

- Layer: C
- Hypothesis: The same architecture invariant becomes far more useful to an agent when feedback includes diagnosis, remediation, and rerun instructions. Requirement-only feedback should be weakest, and remediation-oriented failing checks should be strongest.
- Setup: Captured one shared architecture violation spec in `experiments/006-feedback-representation-loop/fixtures/violation-spec.json`, generated four feedback packages with `render-feedback-packages.py`, then scored them with `score-feedback-package.py` and `compare-feedback-packages.py`.
- Commands or workflow: rendered `docs-only`, `review-comment`, `failing-check-generic`, and `failing-check-remediation` packages from the same violation spec, wrote per-package scores into `artifacts/*-score.json`, then compared them in `artifacts/feedback-representation-comparison.json`.
- Result: pass. The remediation-oriented failing check scored highest for loop-readiness, the docs-only package scored lowest, and the review-comment and generic-check packages landed in the middle.
- What worked: using one shared violation spec kept the comparison fairer than hand-writing unrelated examples, and the rubric separated diagnosis quality from repair guidance.
- What failed: this is still a controlled representation study, not yet a repeated live agent benchmark, so it shows which feedback shapes are stronger on paper rather than measuring repair success over many real runs.
- What to change next: move on to a Git workflow experiment, or return later with a live repeated repair-loop benchmark that uses the same four feedback shapes.
- Reusable lesson for future host repos: stable invariants should be encoded as failing checks, and the best checks should tell an agent what failed, where it failed, how to fix it, and what to rerun next.

### 2026-04-06 - Experiment 007: live repair A/B

- Layer: C
- Hypothesis: On the same broken workspace, a remediation-oriented architecture check should either produce a better final repair or reach the same repair state with lower live repair cost than a generic failing check.
- Setup: Copied the broken workspace from Experiment 005 into `experiments/007-live-repair-ab/fixtures/base-broken-workspace/`, then prepared two isolated run workspaces under `runs/generic-check/` and `runs/remediation-check/`. Both used the same task, prompt, model, and verifier, but each run received a different `check-architecture.py` overlay.
- Commands or workflow: executed two serial `codex exec` runs through `run-live-repair-ab.ps1`, captured JSONL events and final messages, then scored each repaired workspace with `score-live-run.py` and compared them with `compare-live-runs.py`.
- Result: inconclusive. Both runs repaired the workspace to 11 / 11 in one turn. The remediation-check run used fewer input tokens, but it also produced more output tokens and touched one extra file, so the cost signals were mixed rather than clearly better.
- What worked: the isolated-workspace design kept the A/B fairer than the earlier controlled artifact studies, and both check variants were strong enough to drive a real repair loop to completion.
- What failed: the task was too small to force a clear separation between generic and remediation-oriented failing checks. Static representation differences from Experiment 006 did not translate into a decisive live-run winner here.
- What to change next: either raise task complexity or repeat the same A/B several times before drawing a stronger conclusion about live repair cost.
- Reusable lesson for future host repos: remediation-oriented checks are still valuable, but on small bounded repairs a competent model may already recover from a generic failing check. Live benchmarks need enough task difficulty to expose the real payoff of richer feedback.

### 2026-04-06 - Experiment 008: git workflow patterns

- Layer: F
- Hypothesis: When two active tasks accumulate in one dirty branch, isolation and restart clarity collapse. Branch-per-task worktrees should preserve review scope and make interruption recovery cleaner.
- Setup: Created a small fixture repo under `experiments/008-git-workflow-patterns/fixtures/repo-template/`, then used `run-git-workflow-comparison.py` to build two scenarios from the same base commit: one nested dirty branch and one branch-per-task worktree setup. Scored both scenarios with `compare-workflow-patterns.py`.
- Commands or workflow: generated `artifacts/nested-scenario.json` and `artifacts/worktree-scenario.json`, then compared them into `artifacts/workflow-comparison.json`.
- Result: pass. The nested single-branch scenario scored 0 / 8, while the branch-per-task worktree scenario scored 8 / 8. The worktree pattern removed cross-task file contamination and kept README markers isolated per task.
- What worked: using real `git worktree` commands on a toy repo made the result concrete instead of theoretical, and the marker-based README check caught contamination that file lists alone could have hidden.
- What failed: the scorer is intentionally structural and binary, so it does not yet quantify softer tradeoffs such as branch management overhead or merge frequency.
- What to change next: move on to a multi-agent split-task experiment that uses this branch-per-task worktree pattern as the default coordination substrate.
- Reusable lesson for future host repos: if two tasks are active at once, give them separate branches and separate worktrees. Do not stack unrelated dirty changes in one branch and expect clean review or easy recovery.

### 2026-04-06 - Experiment 009: role-based agent workflow

- Layer: E
- Hypothesis: A role-divided workflow (`coordinator -> implementer -> reviewer -> repair`) should preserve product quality while producing a much stronger audit trail than a single generalist agent, at the cost of more sessions and tokens.
- Setup: Reused the toy report task from Experiment 005, then ran two real Codex workflows under `experiments/009-role-based-agent-workflow/`: one `single-generalist` run and one `role-based` run. Added structured prompt contracts for each role and scored both runs with `score-workflow-run.py` and `compare-role-workflows.py`.
- Commands or workflow: executed the single-agent workflow once, then executed the role-based workflow as four sequential Codex sessions (`coordinator`, `implementer`, `reviewer`, `repair`). Wrote score outputs to `artifacts/single-generalist-score.json` and `artifacts/role-based-score.json`, then compared them in `artifacts/role-workflow-comparison.json`.
- Result: pass. Both workflows reached product score 11 / 11, but the single-agent workflow scored only 3 / 8 on auditability while the role-based workflow scored 8 / 8. The role-based workflow required 4 sessions instead of 1 and increased total input tokens by 219199.
- What worked: the role prompts produced distinct artifacts instead of collapsing back into one generalist behavior, and the sequential session design made the handoff trail explicit and inspectable.
- What failed: the added auditability came with a large cost increase, and on this small task the role split did not improve product quality itself.
- What to change next: move on to a parallel split-task experiment so Layer E can test when multiple agents should work concurrently instead of sequentially.
- Reusable lesson for future host repos: role-based multi-agent workflows are most justified when reviewability, compliance, or handoff traceability matter. For small low-risk tasks, a single generalist agent may be cheaper with no product-quality loss.

### 2026-04-06 - Experiment 010: stale doc and duplicate guidance

- Layer: B
- Hypothesis: Stale authority claims and duplicate source-of-truth claims can preserve raw path coverage while still degrading agent legibility. Stale authority should be worse because it sends the next navigation step to a dead file.
- Setup: Reused the shared navigation measurement script from Experiments 001 and 002, then added two top-level fixture maps under `experiments/010-stale-doc-and-duplicate-guidance/fixtures/`. Implemented `score-legibility-pack.ps1` and `compare-legibility-packs.ps1` to score the baseline pack, the stale-doc fixture, and the duplicate-guidance fixture with the same rubric.
- Commands or workflow: scored the baseline pack into `artifacts/baseline-pack-score.json`, scored the stale-doc fixture into `artifacts/stale-doc-pack-score.json`, scored the duplicate-guidance fixture into `artifacts/duplicate-guidance-pack-score.json`, then compared them in `artifacts/legibility-failure-comparison.json`.
- Result: pass. All three packs preserved `4 / 4` required-path coverage, but the baseline scored `12 / 12`, the stale-doc fixture scored `6 / 12`, and the duplicate-guidance fixture scored `8 / 12`.
- What worked: the scorer combined coverage with freshness and authority clarity, so the result showed that short context alone is not enough. Both failure fixtures were shorter than the baseline but still more misleading.
- What failed: this is still a controlled document-fixture study rather than a repeated live agent navigation benchmark, so it measures steering-risk proxies instead of broad behavior.
- What to change next: build a lightweight evaluation harness so the growing experiment set can be tracked under one shared scoreboard.
- Reusable lesson for future host repos: top-level guidance must stay short, current, and singular. Dead source-of-truth links and duplicate ownership claims should be treated as garbage-collection failures even when the current docs are still mentioned somewhere else.
