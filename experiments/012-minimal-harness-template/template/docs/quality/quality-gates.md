# Quality Gates

## Every wave closes with the same gate

1. Review the diff.
2. Run the relevant checks.
3. Run the verification commands.
4. Update the work log.
5. Make a local commit if the wave is clean.

## Notes

- `diff review` should happen before the final closeout.
- `checks` should cover both functional and structural expectations.
- `verification` should be the smallest reliable proof, not a vague statement.
- `work log` updates should capture what changed and what still needs follow-up.
- `local commit` is the default closeout for a clean wave.
