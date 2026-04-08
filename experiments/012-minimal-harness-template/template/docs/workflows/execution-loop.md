# Execution Loop

## Default loop

1. Read the smallest useful context.
2. Confirm the current wave and allowed files.
3. Make the smallest useful change.
4. Review the diff.
5. Run checks and verification.
6. Update the work log.
7. Make a local commit if the wave is clean.

## Operating rules

- Always work in a `wave` or slice with a clear stop point.
- Prefer the `smallest useful context` instead of rereading every document.
- Always do a `diff review` before declaring the wave done.
- Always run `verification` instead of assuming the change is correct.
- Always update the `work log`.
- End with a `local commit` when the wave is clean.
