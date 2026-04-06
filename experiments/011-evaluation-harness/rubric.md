# Experiment 011 Rubric

Each case is normalized to four dimensions.

## 1. Primary outcome gain (0-4)

How much the preferred pattern improves the main success signal of the underlying task.

- `4`: strong decisive improvement
- `3`: clear moderate improvement
- `2`: mild improvement
- `1`: weak improvement
- `0`: no clear improvement or inconclusive

For navigation and workflow cases, this is the main task success signal rather than only code correctness.

## 2. Steering gain (0-4)

How much the preferred pattern improves navigation clarity, restartability, auditability, or task isolation.

- `4`: strong control improvement
- `3`: clear improvement
- `2`: useful but limited improvement
- `1`: minor improvement
- `0`: no clear steering advantage

## 3. Reproducibility (0-4)

How repeatable and inspectable the evidence is.

- `4`: scripted comparison with stable artifacts and clear scoring
- `3`: scripted but with a synthetic or narrow fixture
- `2`: real run evidence with only one or very few samples
- `1`: partly manual or weakly instrumented
- `0`: not reproducible

## 4. Cost penalty (0-4)

How much overhead the preferred pattern adds.

- `0`: no meaningful extra cost or cheaper than the alternative
- `1`: small overhead
- `2`: moderate overhead
- `3`: high overhead
- `4`: very high overhead

## Aggregate score

`net_value = primary_outcome_gain + steering_gain + reproducibility - cost_penalty`

## Recommendation tiers

- `default`: `net_value >= 8` and the case is not inconclusive
- `conditional`: either `net_value >= 5` with a conclusive verdict, or a conclusive case that shows strong steering gain but also high cost
- `needs-more-data`: the case verdict is inconclusive
