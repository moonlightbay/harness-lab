# Source Notes

Last updated: 2026-04-06

## Primary sources

Terminology note:

- In this repo, "garbage collection" means recurring cleanup of stale docs, duplicate helpers, abandoned artifacts, and weak patterns.
- That is different from runtime compaction, which manages context pressure inside long-running agent threads.

### 1. Harness engineering: leveraging Codex in an agent-first world

- Source: https://openai.com/index/harness-engineering/
- Date: 2026-02-11
- Why it matters:
  - best public articulation of "harness engineering" as a practice
  - explains agent-first repository design, progressive disclosure, plans, architecture, feedback loops, and entropy cleanup
- Key takeaways:
  - keep `AGENTS.md` short and treat it as a map
  - use structured `docs/` as the system of record
  - version plans, completed work, and tech debt
  - enforce architecture and taste with linters and structural tests
  - optimize for agent legibility, not only human convenience
  - encode "golden principles" and run recurring cleanup tasks to counter entropy and garbage collection problems

### 2. Unlocking the Codex harness: how we built the App Server

- Source: https://openai.com/index/unlocking-the-codex-harness/
- Date: 2026-02-04
- Why it matters:
  - clarifies what the runtime harness includes beyond the model loop
- Key takeaways:
  - the harness includes thread lifecycle, persistence, config/auth, and tool execution
  - a stable protocol layer matters when multiple clients use the same core harness
  - event streams and resumable threads are central to long-running agent work

### 3. From model to agent: Equipping the Responses API with a computer environment

- Source: https://openai.com/index/equip-responses-api-computer-environment/
- Date: 2026-03-11
- Why it matters:
  - explains practical requirements for turning models into usable agents
- Key takeaways:
  - a shell tool plus a workspace/container makes many real workflows possible
  - environment design solves issues like intermediate files, network policy, timeouts, and retries
  - when the context window fills, the harness needs compaction rather than raw transcript growth
  - bounded output and workspace files are part of keeping long tasks manageable
  - reusable skills package recurring workflows into composable units

### 4. Using PLANS.md for multi-hour problem solving

- Source: https://cookbook.openai.com/articles/codex_exec_plans/
- Date: 2025-10-07
- Why it matters:
  - gives a concrete method for plan-driven long-running tasks
- Key takeaways:
  - long tasks need explicit execution plans
  - plans should be living documents with progress and decision logs
  - the plan should contain enough context for restartability
  - the plan itself should be self-contained enough to survive context loss or a fresh restart

## Secondary ecosystem references

### 5. AGENTS.md

- Source: https://agents.md/
- Why it matters:
  - open ecosystem convention for agent-facing repository instructions
- Key takeaways:
  - `AGENTS.md` is the README for agents
  - nested `AGENTS.md` files can specialize instructions by directory
  - the closest file wins when instructions differ

### 6. Open Harness

- Source: https://openharness.ai/
- Why it matters:
  - useful for understanding harness portability across different agent stacks
- Key takeaways:
  - focuses on a universal API layer across agent harnesses
  - more relevant to portability and comparison than to first-step repo refactoring

### 7. OpenHands

- Source: https://github.com/openhands
- Why it matters:
  - representative open-source agent engineering ecosystem project
- Key takeaways:
  - useful to watch for benchmarks, workflows, and autonomous coding system design
  - not the same thing as the specific "harness engineering" repository method discussed above

## Notes for future research

Topics still worth deeper study:

- which parts of harness engineering transfer well to hardware-integrated desktop software
- how to adapt lighter merge gates to a high-risk medical/robotics codebase
- how to build evaluation harnesses for GUI + hardware workflows
- how to combine local agents and cloud agents safely in a regulated engineering context
- which cleanup tasks belong to repository garbage collection versus runtime compaction
- what the right cleanup cadence is for a documentation-first lab repo
