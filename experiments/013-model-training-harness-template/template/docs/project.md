# Project

## Goal

[TO_FILL] State the training objective, model family, and the target metric or debugging outcome.

## Baseline

[TO_FILL] Record the current trusted config, checkpoint, metric, and commit or tag.

## Data and metrics

[TO_FILL] Name datasets, splits, seeds, the primary metric, and the rule for fair comparison.

## Constraints

[TO_FILL] Note compute budget, runtime limit, forbidden changes, review triggers, and external dependencies.

## Repo structure

- `configs/`: keep `base/`, `experiments/`, and `debug/` configs here.
- `src/data/`: loading, preprocessing, and dataset utilities.
- `src/models/`: model definitions or adapters.
- `src/train/`: training loop, losses, optimizers, and callbacks.
- `src/eval/`: evaluation, metrics, and report export.
- `scripts/`: reproducible commands for data prep, training, evaluation, and smoke tests.
- `docs/`: stable project context and the short work log.
- `artifacts/` or `runs/`: generated outputs that should stay out of git.
