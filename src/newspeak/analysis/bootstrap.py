"""Bootstrap utilities for paired gate metrics."""

from __future__ import annotations

import random
from statistics import median
from typing import Sequence


def median_relative_reduction(values: Sequence[tuple[float, float]]) -> float:
    """Return median relative reduction from baseline to candidate counts."""

    reductions = []
    for baseline, candidate in values:
        if baseline <= 0:
            continue
        reductions.append((baseline - candidate) / baseline)
    if not reductions:
        raise ValueError("No valid positive baseline counts.")
    return float(median(reductions))


def paired_bootstrap_ci(
    values: Sequence[tuple[float, float]],
    *,
    iterations: int = 1000,
    confidence: float = 0.95,
    seed: int = 0,
) -> tuple[float, float]:
    """Return a percentile bootstrap CI for median relative token reduction."""

    valid = [(baseline, candidate) for baseline, candidate in values if baseline > 0]
    if not valid:
        raise ValueError("No valid positive baseline counts.")
    if iterations <= 0:
        raise ValueError("iterations must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    rng = random.Random(seed)
    estimates = []
    for _ in range(iterations):
        sample = [valid[rng.randrange(len(valid))] for _ in range(len(valid))]
        estimates.append(median_relative_reduction(sample))
    estimates.sort()
    lower_q = (1 - confidence) / 2
    upper_q = 1 - lower_q
    return (_quantile(estimates, lower_q), _quantile(estimates, upper_q))


def _quantile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("Cannot compute quantile for empty values.")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = q * (len(sorted_values) - 1)
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    fraction = position - lower
    return float(sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction)
