"""Result loading and success-conditioned paired analyses."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
from statistics import median
from typing import Any

from newspeak.analysis.bootstrap import paired_bootstrap_ci
from newspeak.evals.success import primary_success


@dataclass(frozen=True)
class ArmSummary:
    arm: str
    records: int
    primary_success_records: int
    median_successful_output_tokens: float | None
    median_successful_total_tokens: float | None

    def to_dict(self) -> dict[str, object]:
        return {
            "arm": self.arm,
            "records": self.records,
            "primary_success_records": self.primary_success_records,
            "median_successful_output_tokens": self.median_successful_output_tokens,
            "median_successful_total_tokens": self.median_successful_total_tokens,
        }


@dataclass(frozen=True)
class PairedReduction:
    baseline_arm: str
    candidate_arm: str
    token_field: str
    paired_success_records: int
    median_relative_reduction: float | None
    median_baseline_tokens: float | None
    median_candidate_tokens: float | None
    bootstrap_ci: tuple[float, float] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "baseline_arm": self.baseline_arm,
            "candidate_arm": self.candidate_arm,
            "token_field": self.token_field,
            "paired_success_records": self.paired_success_records,
            "median_relative_reduction": self.median_relative_reduction,
            "median_baseline_tokens": self.median_baseline_tokens,
            "median_candidate_tokens": self.median_candidate_tokens,
            "bootstrap_ci": self.bootstrap_ci,
        }


def load_result_records(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"Line {line_no}: expected JSON object")
            records.append(payload)
    return records


def summarize_by_arm(records: list[dict[str, Any]]) -> list[ArmSummary]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[str(record["arm"])].append(record)

    summaries: list[ArmSummary] = []
    for arm, arm_records in sorted(grouped.items()):
        successful = [record for record in arm_records if is_primary_success(record)]
        summaries.append(
            ArmSummary(
                arm=arm,
                records=len(arm_records),
                primary_success_records=len(successful),
                median_successful_output_tokens=_median_metric(successful, "output_tokens"),
                median_successful_total_tokens=_median_metric(successful, "total_tokens"),
            )
        )
    return summaries


def paired_success_reduction(
    records: list[dict[str, Any]],
    *,
    baseline_arm: str,
    candidate_arm: str,
    token_field: str = "output_tokens",
    bootstrap_iterations: int = 0,
    bootstrap_confidence: float = 0.95,
    bootstrap_seed: int = 0,
) -> PairedReduction:
    by_key: dict[tuple[str, str], dict[str, Any]] = {}
    for record in records:
        by_key[(str(record["prompt_id"]), str(record["arm"]))] = record

    reductions: list[float] = []
    baseline_counts: list[float] = []
    candidate_counts: list[float] = []
    paired_counts: list[tuple[float, float]] = []
    prompt_ids = {str(record["prompt_id"]) for record in records}
    for prompt_id in sorted(prompt_ids):
        baseline = by_key.get((prompt_id, baseline_arm))
        candidate = by_key.get((prompt_id, candidate_arm))
        if baseline is None or candidate is None:
            continue
        if not is_primary_success(baseline) or not is_primary_success(candidate):
            continue
        baseline_count = _metric_value(baseline, token_field)
        candidate_count = _metric_value(candidate, token_field)
        if baseline_count is None or candidate_count is None or baseline_count <= 0:
            continue
        baseline_counts.append(baseline_count)
        candidate_counts.append(candidate_count)
        paired_counts.append((baseline_count, candidate_count))
        reductions.append((baseline_count - candidate_count) / baseline_count)

    ci = None
    if paired_counts and bootstrap_iterations > 0:
        ci = paired_bootstrap_ci(
            paired_counts,
            iterations=bootstrap_iterations,
            confidence=bootstrap_confidence,
            seed=bootstrap_seed,
        )

    return PairedReduction(
        baseline_arm=baseline_arm,
        candidate_arm=candidate_arm,
        token_field=token_field,
        paired_success_records=len(reductions),
        median_relative_reduction=float(median(reductions)) if reductions else None,
        median_baseline_tokens=float(median(baseline_counts)) if baseline_counts else None,
        median_candidate_tokens=float(median(candidate_counts)) if candidate_counts else None,
        bootstrap_ci=ci,
    )


def is_primary_success(record: dict[str, Any]) -> bool:
    success = record.get("success", {})
    if not isinstance(success, dict):
        return False
    if "primary_success" in success:
        return bool(success["primary_success"])
    return primary_success(success)


def _median_metric(records: list[dict[str, Any]], token_field: str) -> float | None:
    values = [_metric_value(record, token_field) for record in records]
    numeric_values = [value for value in values if value is not None]
    return float(median(numeric_values)) if numeric_values else None


def _metric_value(record: dict[str, Any], token_field: str) -> float | None:
    metrics = record.get("metrics", {})
    if not isinstance(metrics, dict):
        return None
    value = metrics.get(token_field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)
