# Strong Feedback Loop

Checks available during this run:

- `python -m compileall report_app tests`
- `python -m unittest discover -s tests -v`
- `python check-architecture.py <workspace_root>`

The extra architecture rule enforces that normalization stays in `domain.py`, report building stays in `service.py`, and `cli.py` remains thin.
