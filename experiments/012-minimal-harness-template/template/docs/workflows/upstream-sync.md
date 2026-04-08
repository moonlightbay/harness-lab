# Upstream Sync

## Treat upstream changes as translation work

When new changes arrive from `mainline`, treat them as a `translation task`.

## Rules

- Pull the upstream change into its own slice.
- Translate the new behavior into the current structure intentionally.
- `do not mix` unrelated upstream sync with local redesign in one uncontrolled step.

## Output

Record what changed upstream, what was translated, and what still needs follow-up.
