# configs/

Use this directory for tracked configuration only.

Recommended split:

- `base/`: stable defaults shared across runs
- `experiments/`: small overrides for one idea
- `debug/`: cheap smoke-test configs

Rules:

- prefer layered configs over copied full files
- name configs by intent, not by date alone
- record the exact config path in `docs/log.md`
