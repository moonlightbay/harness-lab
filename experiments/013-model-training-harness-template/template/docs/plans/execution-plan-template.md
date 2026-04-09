# Execution Plan Template

## Goal

State the exact training outcome or debugging target.

## Wave

Name the current wave or slice.

## Scope

Describe what this wave is allowed to change and what it intentionally leaves alone.

## Baseline

Record the current trusted baseline run, metric, and commit.

## Constraints

List hard constraints such as GPU budget, runtime cap, safety limits, and forbidden changes.

## Allowed files

List the files or directories that this wave may modify.

## Stop conditions

List the conditions that should end the wave even if more ideas remain.

## Plan

1. Read the smallest useful context.
2. Make one bounded training change.
3. Review the diff before launching costly work.
4. Run dry-run or cheap checks first.
5. Run the declared verification command.
6. Update the run log and next action.

## Verification

List the exact commands and expected signals.

## Rollback

List how to undo the wave safely if the result regresses or the run is invalid.

## Risks

List the main ways this wave can fail or produce misleading results.

## Handoff

State what the next agent needs to know if this wave stops early.
