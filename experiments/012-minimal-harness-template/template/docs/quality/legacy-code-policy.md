# Legacy Code Policy

## Classification comes first

Do not delete questionable code on sight. Classify it first.

## Allowed classifications

- `isolate`: keep it running but move it away from new clean structure.
- `keep`: leave it in place because it is still stable and useful.
- `deprecate`: mark it for removal after a safe replacement exists.
- `clean`: remove it because it is unused, unsafe, or already replaced.

## Required note

Record the chosen classification in the work log or plan before large cleanup.
