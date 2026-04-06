# Harness Engineering Overview

Last updated: 2026-04-06

## 1. Working definition

In the current agentic software engineering context, "harness engineering" is best understood as designing the environment, repository structure, tools, documentation, and feedback loops that allow coding agents to work reliably over long-running tasks.

It is not just prompting. It is also not only the runtime harness itself. It spans:

- repo structure
- agent-facing documentation
- tool/runtime environment
- plans and decision records
- feedback loops
- validation and evaluation harnesses
- collaboration workflow between humans and agents
- cleanup routines that keep agent-created entropy under control

A practical summary is:

> Humans steer. Agents execute. The harness is the engineered system that makes this reliable.

## 2. Important distinction: three different "Harness" meanings

### 2.1 Harness engineering

This is the engineering practice described in recent OpenAI articles. It focuses on agent-first repository design, execution environments, plans, feedback loops, cleanup, and validation.

### 2.2 Harness Open Source / Harness.io

This is a DevOps platform company and product line. It is useful in CI/CD contexts, but it is not the same concept as harness engineering in the agent-first repository sense.

### 2.3 Open Harness

This is a separate open-source project that aims to provide one API across different agent harness implementations. It is relevant as ecosystem context, but it is not the primary thing to study for refactoring a future host repository.

## 3. Core ideas extracted from current sources

### 3.1 Agent-first repository structure

A repository should be shaped so agents can navigate it intentionally instead of receiving one huge instruction blob. A short `AGENTS.md` should point to structured docs that act as the system of record.

Implication for practice:

- keep `AGENTS.md` small
- move deep knowledge into versioned docs
- make architecture, plans, quality rules, and technical debt visible inside the repository

### 3.2 Progressive disclosure and agent legibility

Agents work better when they start with a small, stable map and then discover more detailed context as needed. This is progressive disclosure.

Implication for practice:

- use indexes and clear document ownership
- avoid giant instruction manuals
- keep repo knowledge cross-linked and current
- keep one owner per topic; duplicate "source of truth" claims create ambiguity even when every file still exists
- treat stale top-level links as a harness failure; a short map that points to dead files is worse than a slightly longer clean map
- store important knowledge in the repo, not in chat threads or only in people's heads

### 3.3 Plans are first-class artifacts

Long tasks need persistent execution plans, not just chat history. Plans should carry assumptions, milestones, decision logs, and progress.

Implication for practice:

- use execution plans for long refactors
- version active plans and completed plans
- record why decisions changed

### 3.4 Feedback loops matter more than raw generation speed

Harness engineering shifts effort from manual coding to environment design and feedback loop design. Reliable tests, lints, logs, screenshots, metrics, and review loops become central.

Implication for practice:

- improve observability and reproducibility
- prefer fast verification loops
- encode repeated review feedback into docs or automation
- prefer feedback that states the failing boundary, the offending location, the fix direction, and the rerun command

### 3.5 The runtime harness is more than the model loop

The runtime harness is not only "prompt in, answer out". It also includes thread lifecycle, persistence, config/auth, tool execution, extension points, and the protocol layer that lets different clients drive the same agent core.

Implication for practice:

- separate agent logic from client surface details
- treat thread state and resumability as first-class requirements
- design tool execution, sandbox policy, and extension points explicitly

### 3.6 Context budget management and compaction

Long-running agent work creates a second problem besides code correctness: context pressure. A usable harness needs ways to keep high-value state while dropping low-value output and intermediate clutter.

Implication for practice:

- keep intermediate files in the workspace instead of pasting them into chat
- prefer bounded logs and summaries over raw terminal spam
- treat context compaction as part of runtime design for long tasks

Important distinction:

- compaction is runtime state management for a long-running turn or thread
- garbage collection is repository and process cleanup for drift that accumulates across many runs

### 3.7 Architecture and code taste must be enforceable

Agent-generated systems drift quickly without boundaries. The lesson from current sources is to enforce invariants mechanically rather than relying on human memory.

Implication for practice:

- define explicit layering
- restrict dependency directions
- add structural tests and custom lints
- promote recurring review comments into enforceable rules
- make failing checks remediation-oriented so agents can repair instead of only observing a red status

### 3.8 Multi-agent work requires isolation and orchestration

Recent Codex materials frame multi-agent work as a normal mode, not an exotic one. Isolated worktrees, explicit ownership, and artifact-based coordination reduce conflict.

Implication for practice:

- split work by bounded ownership
- use isolated branches or worktrees
- coordinate via plans, issues, and artifacts rather than implicit shared context

### 3.9 Git workflow changes under higher throughput

OpenAI's public write-up argues that when agent throughput is high, overly heavy merge gates can become counterproductive. However, this is context dependent and should not be copied blindly into a safety-critical or hardware-heavy project.

Implication for practice:

- keep PRs and changesets small
- treat correction cost and waiting cost explicitly
- adopt lighter merge rules only where regression risk is controlled

### 3.10 Entropy and garbage collection

Recent OpenAI material explicitly calls out "entropy and garbage collection" as a harness problem. Agents will copy existing patterns, including mediocre ones. Without recurring cleanup, uneven helpers, stale docs, weak abstractions, and "AI slop" compound.

Implication for practice:

- encode a small set of "golden principles" directly in the repo
- run recurring cleanup tasks instead of waiting for large cleanup days
- treat stale docs, dead experiment artifacts, and duplicate helper logic as harness failures, not cosmetic issues
- capture human taste once, then enforce it continuously through docs, scripts, linters, or cleanup agents

### 3.11 Evaluation harnesses should compare patterns, not only runs

Once a lab accumulates multiple one-off experiments, the next bottleneck is comparison. Without a shared scoreboard, it becomes too easy to overfit to whichever experiment was run most recently.

Implication for practice:

- normalize experiments into a small recurring scorecard
- compare benefit and cost in one place
- keep an explicit "needs more data" bucket so inconclusive wins are not promoted too early

## 4. What seems directly applicable to a future host repository

Most applicable:

- short `AGENTS.md` plus structured docs
- execution plans for long refactors
- per-module validation harnesses
- explicit layering between UI, application, hardware, and runtime
- stronger feedback loops for higher-risk workflows
- doc gardening and lightweight garbage-collection routines for stale knowledge and low-value artifacts
- using agents for documentation, refactors, review, and migration scaffolding

Less directly applicable at the start:

- fully agent-generated repository
- minimal merge gates everywhere
- fully autonomous PR completion without human review

## 5. Initial hypothesis for migration

The best path is probably not "rewrite the whole project with agents".

The better path is:

1. build a small harness-first lab
2. validate repository patterns and workflow patterns
3. add cleanup and evaluation loops before autonomy increases
4. bring the proven pieces back into the main repo incrementally

## 6. Related projects worth monitoring

- OpenAI Codex harness / App Server materials: relevant for runtime and architecture thinking.
- AGENTS.md ecosystem: relevant for agent-facing repo design.
- Open Harness: relevant for understanding portability across harness runtimes.
- OpenHands: relevant as a broader open-source agent engineering ecosystem reference.
