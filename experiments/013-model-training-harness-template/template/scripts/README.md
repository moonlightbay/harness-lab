# scripts/

Keep only reproducible entrypoints here.

Recommended commands:

- `prepare_data`: data download or preprocessing
- `train`: launches training from a config
- `evaluate`: runs validation or test evaluation
- `smoke_test`: cheap check before expensive runs

Rules:

- one script should do one purpose well
- accept config path and output dir explicitly
- print or log the exact rerun command
