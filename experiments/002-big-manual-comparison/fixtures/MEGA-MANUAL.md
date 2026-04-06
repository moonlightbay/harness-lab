# Giant Manual Fixture

This file is an experiment fixture.

It intentionally represents a poor top-level instruction style for an agent-first repository.

It is long, repetitive, and front-loads generic explanation before it gets to the concrete files that matter.

Do not treat this file as the real source of truth for `harness-lab`.

The real repo keeps short maps at the top level and deeper detail in linked documents.

## Purpose

This repository exists to study harness engineering by practice.

The broader aim is to transfer validated patterns into a larger host repository.

The lab favors small experiments, written conclusions, and reusable process artifacts.

The lab is intentionally documentation-first.

The lab should remain small enough that each experiment changes only one idea at a time.

The lab should not turn into a framework before the patterns are understood.

The lab should prefer evidence over taste alone.

The lab should capture recurring lessons in the repository rather than leaving them in chat history.

The lab should keep humans in the steering role and agents in the execution role.

The lab should keep experiments inspectable by a later reader who did not see the original conversation.

## Working view of harness engineering

Harness engineering is the practice of designing the environment around an agent so that the agent can work reliably.

That environment includes repository layout, tool access, persistence, execution plans, feedback loops, cleanup, and evaluation.

The goal is not only better model output in one turn.

The goal is better task reliability over longer horizons.

This means the repository needs to be legible to both humans and agents.

It also means the repository needs to be resistant to entropy.

Agents can generate a lot of useful material quickly.

Agents can also spread mediocre patterns quickly.

A good harness contains both acceleration and constraint.

The constraint side matters because taste, architecture, and process hygiene drift if they are not encoded.

## What this repository values

The repository values short maps over giant manuals.

The repository values explicit source-of-truth documents over implicit tribal knowledge.

The repository values plans for long tasks.

The repository values small experiments over platform building.

The repository values inspectable artifacts over ad hoc notes.

The repository values cleanup as a normal maintenance activity.

The repository values migration discipline because the target project is higher risk.

The repository values readability because experiments should teach, not just execute.

The repository values reproducibility because the lessons need to survive restarts.

The repository values progressive disclosure because not every detail belongs in the first screenful.

## Typical workflow expectations

An agent should first understand the repo purpose.

An agent should then identify the authoritative docs for the current task.

An agent should avoid changing repository structure without checking those docs.

An agent should record experiment outcomes in the log.

An agent should create a dedicated experiment folder when adding a new experiment.

An agent should define the experiment goal, hypothesis, setup, evaluation criteria, and result.

An agent should prefer reproducible scripts.

An agent should avoid long, fragile, hand-waved explanations when measurable proxies are available.

An agent should distinguish runtime compaction from repository garbage collection.

An agent should update plans when the roadmap changes.

## Why giant manuals are problematic

A giant manual can contain all the required facts and still be the wrong shape for real work.

The problem is not only token count.

The problem is delayed access to the few concrete facts that determine what to read next.

The problem is hidden priority.

The problem is that repetition feels safe while actually increasing scan cost.

The problem is that duplicated guidance ages unevenly.

The problem is that readers need a map before they need an encyclopedia.

The problem is worse for agents because long undifferentiated text competes for context budget with the task itself.

The problem is also worse over time because more instructions tend to accumulate while old ones remain.

The problem is subtle because coverage can remain high while usability drops.

## Expanded recap of the repository layers

Layer A is about whether the repository is shaped clearly enough for an agent to navigate.

Layer B is about how much top-level context is enough before performance drops.

Layer C is about feedback loops, code taste, and enforceable quality boundaries.

Layer D is about plans and restartability for multi-step work.

Layer E is about multi-agent coordination and ownership.

Layer F is about Git workflow under higher task throughput.

Layer G is about evaluation harnesses so improvement claims can be tested.

Layer H is about entropy and garbage collection so the repository does not degrade as agent output accumulates.

All of these layers matter, but they do not all belong in the first navigation artifact.

The first navigation artifact should route the reader, not explain the full curriculum in place.

That is the central point this fixture is designed to stress.

## Long-form reminders that duplicate earlier guidance

Keep the repo small enough to reason about.

Keep experiment artifacts inspectable.

Keep the roadmap versioned.

Keep knowledge notes versioned.

Keep the source of truth explicit.

Keep the cleanup loop active.

Keep the migration lens visible.

Keep the next experiment concrete.

Keep the environment legible.

Keep the instructions updated.

## Practical task framing for an agent

Before editing, identify the repository purpose, the active roadmap, the current knowledge summary, and the experiment log.

Do not assume a giant manual should be the main system of record just because it is large.

If the manual references linked documents, prefer those linked documents for current truth.

If the manual duplicates linked documents, expect the linked documents to age better.

If there is tension between brevity and explicitness, keep the top-level artifact brief but directly linked.

If repeated cleanup rules keep showing up, move them into structure or automation.

## Finally, the concrete file map

The root readme is `README.md`.

The current knowledge summary is `docs/knowledge/harness-engineering-overview.md`.

The active roadmap is `docs/plans/experiment-plan.md`.

The experiment log is `docs/plans/experiment-log.md`.

The experiment index is `experiments/README.md`.

The short agent map is `AGENTS.md`.

For a structural change, read the short agent map and then follow the linked source-of-truth docs above.

If you need the current research notes, use `docs/knowledge/`.

If you need experiment outputs, use `experiments/`.
