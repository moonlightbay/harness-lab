# src/

Recommended split:

- `src/data/`: dataset loading and preprocessing
- `src/models/`: model definitions or adapters
- `src/train/`: training loop, losses, optimizers, and callbacks
- `src/eval/`: evaluation, metrics, and prediction export
- `src/common/`: shared helpers only when reused by multiple modules

Rules:

- keep entrypoints in `scripts/`
- keep configs out of code
- keep experiment-specific hacks local until they prove reusable
