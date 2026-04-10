# Harness-Lab Experiment Plan

Last updated: 2026-04-10
Status: active

## Goal

Use this repository to understand harness engineering by practice, not only by reading. Each experiment should convert one abstract idea into a concrete, repeatable workflow or artifact.

## Global research question

Which harness-engineering patterns are worth migrating into a future host repository, and in what order?

## Success criteria for the lab as a whole

- We can clearly explain each major harness-engineering layer in our own words.
- We complete at least one runnable or inspectable experiment for each layer.
- We can identify a migration order for a larger host repository.
- We produce artifacts that can be reused directly in the future 2.0 refactor.
- We can distinguish runtime compaction from repository garbage collection and validate both experimentally.

## Experiment layers

### Layer A. Agent-first repository structure

Question:
Can a small repo be organized so an agent can navigate it with minimal prompting?

Experiments:

1. Use the current repo as the docs-first baseline.
2. Ask an agent to locate source-of-truth docs and follow them.
3. Record path length, steering needed, and top-level context size.
4. Compare with a variant that uses one oversized instruction file.

Artifacts:

- current repository layout
- Experiment 001 result
- comparison notes between small-map and giant-manual approaches

Success criteria:

- the agent finds the right docs without repeated human steering
- the failure mode of the giant-manual approach is documented

### Layer B. Progressive disclosure and agent legibility

Question:
How little top-level context can we give before performance drops?

Experiments:

1. Create an index-based doc tree.
2. Give the agent only the top-level map.
3. Measure whether it navigates to the right detailed file.
4. Intentionally introduce stale docs and observe failure modes.

Artifacts:

- doc index structure
- stale-doc and duplicate-guidance failure case notes
- checklist for repo legibility

Success criteria:

- we identify what top-level information must always be present
- we identify what information can safely stay in deeper docs

### Layer C. Feedback loops and code taste

Question:
Which feedback loops most improve agent reliability with the least setup cost?

Experiments:

1. Use a toy codebase with formatting, linting, tests, and a structural rule.
2. Ask an agent to make a change until all checks pass.
3. Add one custom rule that encodes a style or architecture invariant.
4. Compare outcomes with and without the custom rule.
5. Compare requirement-only, review-comment, generic failing-check, and remediation-oriented failing-check feedback on the same violation.
6. Score which feedback shape is most ready for an autonomous repair loop.
7. Run a live repair A/B so the stronger feedback representation is tested against a real Codex execution loop, not only a static scorer.

Artifacts:

- toy project
- rule definitions
- before/after analysis of output quality

Success criteria:

- at least one custom invariant measurably improves output consistency
- we can state which loops belong in every future repo by default
- we can identify which feedback representations should be automated by default

### Layer D. Plans and long-horizon execution

Question:
Do explicit execution plans improve outcomes for multi-step tasks?

Experiments:

1. Define a medium-complexity refactor task.
2. Run it once without a checked-in plan.
3. Run it once with a checked-in execution plan.
4. Compare restartability, error recovery, and result quality.

Artifacts:

- `PLANS.md`-style template
- one completed plan example
- comparison notes

Success criteria:

- the plan-driven run is easier to resume and audit
- the plan format is good enough to reuse in the main repo

### Layer E. Multi-agent collaboration

Question:
How should work be partitioned so multiple agents help instead of colliding?

Experiments:

1. Split a toy feature into two or three independent workstreams.
2. Run one agent per workstream.
3. Use explicit ownership and artifact-based coordination.
4. Compare against a run where ownership is vague.

Artifacts:

- ownership template
- work-splitting checklist
- collision and merge notes

Success criteria:

- conflicts are reduced by explicit ownership boundaries
- we learn which tasks are safe to parallelize and which should stay local

### Layer F. Git workflow and version control

Question:
What Git habits best support agent-heavy development?

Experiments:

1. Try short-lived branches with small commits.
2. Try worktree-based parallel tasks.
3. Compare branch-per-task versus nested changes in one branch.
4. Evaluate when commit granularity helps or hurts agent recovery.

Artifacts:

- branch strategy note
- worktree usage note
- PR or patch checklist

Success criteria:

- we define a practical Git workflow for agent-heavy work
- we identify which habits should be mandatory in the future 2.0 refactor

### Layer G. Evaluation harnesses

Question:
How do we know whether the harness is actually improving outcomes?

Experiments:

1. Define a small task suite.
2. Score runs on correctness, steering overhead, reproducibility, and repair cost.
3. Repeat the suite after improving docs or tooling.

Artifacts:

- evaluation rubric
- run log table
- trend notes across iterations

Success criteria:

- we can show whether a harness change improved or worsened performance
- evaluation is lightweight enough to repeat regularly

### Layer H. Entropy and garbage collection

Question:
How do we stop agent-generated drift, stale docs, and uneven patterns from compounding?

Experiments:

1. Define a small set of golden principles for docs, plans, scripts, and experiment artifacts.
2. Introduce stale docs, duplicate helpers, or abandoned artifacts in a toy repo snapshot.
3. Run a cleanup pass with a checklist or script.
4. Compare frequent cleanup versus delayed cleanup.

Artifacts:

- golden-principles note
- cleanup checklist or hygiene script
- before/after cleanup notes

Success criteria:

- the cleanup pass catches at least stale knowledge and one duplication pattern
- cleanup is light enough to run continuously
- we can clearly separate repository garbage collection from runtime compaction

## Proposed order

1. Layer A
2. Layer B
3. Layer H
4. Layer D
5. Layer C
6. Layer F
7. Layer E
8. Layer G

Rationale:

- first establish the repository map
- then validate progressive disclosure and stale-doc failure modes
- then add cleanup before drift compounds
- then add long-horizon planning
- then enforce stronger quality loops
- then refine Git and collaboration mechanics
- finally add a more formal evaluation loop

## First concrete sprint

### Sprint 1 objective

Run the first repository-legibility experiment and define the first garbage-collection rules.

Status note:

- Experiment 001, Experiment 002, Experiment 003, Experiment 004, Experiment 005, Experiment 006, Experiment 007, Experiment 008, Experiment 009, Experiment 010, Experiment 011, and Experiment 012 were completed on 2026-04-06.
- Layer B now has evidence for both oversized-manual failure and stale-or-duplicate guidance failure.
- Layer G now has a lightweight recurring scoreboard that ranks patterns by outcome gain, steering gain, reproducibility, and cost.
- Experiment 012 was refined again on 2026-04-08 after two days of use in another project, then simplified on 2026-04-10 to better complement Codex's built-in harness.
- Experiment 013 was completed on 2026-04-09 and then refined twice on 2026-04-10 into a minimal training-specific scaffold inspired by `auto-deep-researcher-24x7`.
- A lightweight generic harness template now exists with four durable docs (`project`, `architecture`, `task`, `log`) plus an architecture-rule hook.
- A minimal model-training scaffold now exists with durable project context, a short work log, and explicit `configs/`, `src/`, and `scripts/` structure guides.
- The next useful step is a cross-agent template pilot that checks whether the same scaffold stays effective across different model agents or agent styles.

### Sprint 1 tasks

1. Finalize repo structure and docs.
2. Run Experiment 001: can an agent locate the source-of-truth docs with minimal steering?
3. Record the navigation path and top-level context size.
4. Draft an initial garbage-collection checklist for docs, plans, experiments, and helper scripts.
5. Define the oversized-manual comparison case for Experiment 002.
6. Record observations in the experiment log.

### Sprint 1 exit criteria

- Experiment 001 has a written result
- the next A/B comparison is defined
- an initial garbage-collection checklist exists
- we can explain why short maps beat oversized manuals in this repo

## Migration lens back to a future host repository

For each completed experiment, answer:

1. Is this pattern useful for the host repository?
2. If yes, should it be applied at repo level, module level, or workflow level?
3. What is the smallest safe pilot in the target repo?
4. What risks appear when domain-specific workflows and higher-stakes requirements are involved?
5. Which cleanup tasks should be automated before migrating the pattern into a higher-risk repo?
