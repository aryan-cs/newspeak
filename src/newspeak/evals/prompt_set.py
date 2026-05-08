"""Prompt-set loading and validation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Iterable

from newspeak.analysis.contamination import TextRecord, find_overlaps


EVAL_ONLY_ROLES = {"smoke", "gate", "main_eval", "human_eval"}
VALID_SOURCE_TYPES = {"custom_authored", "benchmark", "derived_translation"}
VALID_SPLIT_ROLES = EVAL_ONLY_ROLES | {"training_candidate"}
REQUIRED_FIELDS = {
    "prompt_id",
    "split_role",
    "source_type",
    "task_category",
    "safety_category",
    "prompt",
    "holdout",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | {"source_ref", "expected_scoring", "notes"}


@dataclass(frozen=True)
class PromptRecord:
    prompt_id: str
    split_role: str
    source_type: str
    task_category: str
    safety_category: str
    prompt: str
    holdout: bool
    source_ref: str | None = None
    expected_scoring: str | None = None
    notes: str = ""

    @classmethod
    def from_payload(cls, payload: dict[str, object], line_no: int) -> "PromptRecord":
        missing = sorted(REQUIRED_FIELDS - set(payload))
        if missing:
            raise ValueError(f"Line {line_no}: missing required fields: {', '.join(missing)}")
        extra = sorted(set(payload) - ALLOWED_FIELDS)
        if extra:
            raise ValueError(f"Line {line_no}: unknown fields: {', '.join(extra)}")

        return cls(
            prompt_id=_expect_str(payload, "prompt_id", line_no),
            split_role=_expect_str(payload, "split_role", line_no),
            source_type=_expect_str(payload, "source_type", line_no),
            task_category=_expect_str(payload, "task_category", line_no),
            safety_category=_expect_str(payload, "safety_category", line_no),
            prompt=_expect_str(payload, "prompt", line_no),
            holdout=_expect_bool(payload, "holdout", line_no),
            source_ref=_optional_str(payload, "source_ref", line_no),
            expected_scoring=_optional_str(payload, "expected_scoring", line_no),
            notes=_optional_str(payload, "notes", line_no) or "",
        )

    def to_text_record(self) -> TextRecord:
        return TextRecord(self.prompt_id, self.prompt)


@dataclass
class PromptSetValidation:
    records: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict[str, object] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "records": self.records,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": self.summary,
        }


@dataclass(frozen=True)
class PromptSetSummary:
    records: int
    split_roles: dict[str, int]
    source_types: dict[str, int]
    task_categories: dict[str, int]
    safety_categories: dict[str, int]
    holdout: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "records": self.records,
            "split_roles": self.split_roles,
            "source_types": self.source_types,
            "task_categories": self.task_categories,
            "safety_categories": self.safety_categories,
            "holdout": self.holdout,
        }


def load_prompt_records(path: Path) -> list[PromptRecord]:
    records: list[PromptRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Line {line_no}: invalid JSON: {exc.msg}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"Line {line_no}: expected JSON object")
            records.append(PromptRecord.from_payload(payload, line_no))
    return records


def validate_prompt_records(records: Iterable[PromptRecord]) -> PromptSetValidation:
    seen_ids: set[str] = set()
    validation = PromptSetValidation()
    materialized = list(records)
    validation.records = len(materialized)
    validation.summary = summarize_prompt_records(materialized).to_dict()

    if not materialized:
        validation.warnings.append("prompt set is empty")

    for record in materialized:
        if record.prompt_id in seen_ids:
            validation.errors.append(f"{record.prompt_id}: duplicate prompt_id")
        seen_ids.add(record.prompt_id)

        if record.split_role not in VALID_SPLIT_ROLES:
            validation.errors.append(f"{record.prompt_id}: invalid split_role {record.split_role!r}")

        if record.source_type not in VALID_SOURCE_TYPES:
            validation.errors.append(f"{record.prompt_id}: invalid source_type {record.source_type!r}")

        if record.split_role in EVAL_ONLY_ROLES and not record.holdout:
            validation.errors.append(f"{record.prompt_id}: eval-only prompt must set holdout=true")

        if record.source_type in {"benchmark", "derived_translation"} and not record.source_ref:
            validation.errors.append(f"{record.prompt_id}: source_ref required for {record.source_type}")

        if not record.prompt.strip():
            validation.errors.append(f"{record.prompt_id}: prompt must not be empty")

        if not record.prompt_id.strip():
            validation.errors.append(f"{record.prompt_id!r}: prompt_id must not be empty")

        if not record.task_category.strip():
            validation.errors.append(f"{record.prompt_id}: task_category must not be empty")

        if not record.safety_category.strip():
            validation.errors.append(f"{record.prompt_id}: safety_category must not be empty")

    overlaps = find_overlaps(
        [record.to_text_record() for record in materialized],
        [record.to_text_record() for record in materialized],
        ngram_size=5,
        ngram_threshold=1.0,
    )
    for finding in overlaps:
        if finding.left_id < finding.right_id:
            validation.errors.append(
                f"{finding.left_id}/{finding.right_id}: duplicate normalized prompt text"
            )

    return validation


def summarize_prompt_records(records: Iterable[PromptRecord]) -> PromptSetSummary:
    materialized = list(records)
    return PromptSetSummary(
        records=len(materialized),
        split_roles=dict(sorted(Counter(record.split_role for record in materialized).items())),
        source_types=dict(sorted(Counter(record.source_type for record in materialized).items())),
        task_categories=dict(sorted(Counter(record.task_category for record in materialized).items())),
        safety_categories=dict(
            sorted(Counter(record.safety_category for record in materialized).items())
        ),
        holdout=dict(
            sorted(Counter("true" if record.holdout else "false" for record in materialized).items())
        ),
    )


def _expect_str(payload: dict[str, object], field: str, line_no: int) -> str:
    value = payload[field]
    if not isinstance(value, str):
        raise ValueError(f"Line {line_no}: {field} must be a string")
    return value


def _optional_str(payload: dict[str, object], field: str, line_no: int) -> str | None:
    value = payload.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Line {line_no}: {field} must be a string or null")
    return value


def _expect_bool(payload: dict[str, object], field: str, line_no: int) -> bool:
    value = payload[field]
    if not isinstance(value, bool):
        raise ValueError(f"Line {line_no}: {field} must be a boolean")
    return value
