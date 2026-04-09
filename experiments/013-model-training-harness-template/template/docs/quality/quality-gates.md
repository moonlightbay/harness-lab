# Quality Gates

Every wave should close with the same short gate:

1. Do a diff review.
2. Run cheap checks first.
3. Run a dry-run before expensive training when possible.
4. Run the declared verification command.
5. Update the run log with result and decision.
6. Create a local commit only after the state is coherent.

Use this gate even when the code change is small. Training repos drift fast when agents change code, configs, logs, and notes without one shared closeout rule.
