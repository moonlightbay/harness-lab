# Scoring Rubric

## Outcome quality - 11 points

- Functional checks: 5 points from `verify-basic.py`
- Architecture checks: 6 points from the external scorer based on `exp005`

## Repair cost indicators

- turn count from Codex JSONL events
- input tokens from Codex JSONL events
- output tokens from Codex JSONL events
- changed file count from `git diff --name-only`

## Success interpretation

- Higher outcome score wins.
- If both runs tie on outcome score, lower repair cost wins.
- If both runs tie on score and cost is mixed, treat the result as inconclusive and record which cost indicators moved in which direction.
