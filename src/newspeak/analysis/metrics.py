"""Basic result aggregation helpers."""

from __future__ import annotations

from statistics import median


def median_token_reduction(baseline_counts: list[int], candidate_counts: list[int]) -> float:
    """Return median relative token reduction for paired counts.

    Positive values mean the candidate used fewer tokens.
    """

    if len(baseline_counts) != len(candidate_counts):
        raise ValueError("Paired count lists must have equal length.")
    reductions = []
    for baseline, candidate in zip(baseline_counts, candidate_counts):
        if baseline <= 0:
            continue
        reductions.append((baseline - candidate) / baseline)
    if not reductions:
        raise ValueError("No valid baseline counts.")
    return float(median(reductions))
