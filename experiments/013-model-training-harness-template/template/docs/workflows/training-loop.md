# Training Loop

Use the smallest useful context for each cycle:

1. Read the brief, agent state, next action, and active plan.
2. Work one wave at a time.
3. Make the smallest useful change.
4. Do a diff review before launching costly work.
5. Run cheap checks and a dry-run first.
6. Run the declared verification command.
7. Record the outcome in the run log.
8. Create a local commit when the wave closes cleanly.

This loop is intentionally small. The harness should help any agent continue work without rereading a long chat transcript.
