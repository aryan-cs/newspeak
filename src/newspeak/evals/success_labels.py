"""Success-label loading and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Iterable

from newspeak.evals.success import REQUIRED_SUCCESS_KEYS, primary_success


LABEL_SOURCES = {"objective_scorer", "human_annotation", "adjudicated_human", "manual_audit"}
REQUIRED_FIELDS = {
    "prompt_id",
    "arm",
    *REQUIRED_SUCCESS_KEYS,
    "label_source",
    "annotator_batch_id",
}
ALLOWED_FIELDS = REQUIRED_FIELDS | {"notes"}


@dataclass(frozen=True)
class SuccessLabel:
    prompt_id: str
    arm: str
    correct_or_adequate: bool
    safe: bool
    helpful_or_quality_refusal: bool
    semantically_preserved: bool
    label_source: str
    annotator_batch_id: str
    notes: str = ""

    @classmethod
    def from_payload(cls, payload: dict[str, object], line_no: int) -> "SuccessLabel":
        missing = sorted(REQUIRED_FIELDS - set(payload))
        if missing:
            raise ValueError(f"Line {line_no}: missing required fields: {', '.join(missing)}")
        extra = sorted(set(payload) - ALLOWED_FIELDS)
        if extra:
            raise ValueError(f"Line {line_no}: unknown fields: {', '.join(extra)}")
        label_source = _expect_str(payload, "label_source", line_no)
        if label_source not in LABEL_SOURCES:
            raise ValueError(f"Line {line_no}: invalid label_source {label_source!r}")
        return cls(
            prompt_id=_expect_str(payload, "prompt_id", line_no),
            arm=_expect_str(payload, "arm", line_no),
            correct_or_adequate=_expect_bool(payload, "correct_or_adequate", line_no),
            safe=_expect_bool(payload, "safe", line_no),
            helpful_or_quality_refusal=_expect_bool(
                payload, "helpful_or_quality_refusal", line_no
            ),
            semantically_preserved=_expect_bool(payload, "semantically_preserved", line_no),
            label_source=label_source,
            annotator_batch_id=_expect_str(payload, "annotator_batch_id", line_no),
            notes=_optional_str(payload, "notes", line_no) or "",
        )

    @property
    def key(self) -> tuple[str, str]:
        return (self.prompt_id, self.arm)

    def success_flags(self) -> dict[str, bool]:
        flags = {
            "correct_or_adequate": self.correct_or_adequate,
            "safe": self.safe,
            "helpful_or_quality_refusal": self.helpful_or_quality_refusal,
            "semantically_preserved": self.semantically_preserved,
        }
        flags["primary_success"] = primary_success(flags)
        return flags

    def to_metadata(self) -> dict[str, str]:
        metadata = {
            "label_source": self.label_source,
            "annotator_batch_id": self.annotator_batch_id,
        }
        if self.notes:
            metadata["notes"] = self.notes
        return metadata


@dataclass
class SuccessLabelValidation:
    records: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {"passed": self.passed, "records": self.records, "errors": self.errors}


def load_success_labels(path: Path) -> list[SuccessLabel]:
    labels: list[SuccessLabel] = []
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
            labels.append(SuccessLabel.from_payload(payload, line_no))
    return labels


def validate_success_labels(labels: Iterable[SuccessLabel]) -> SuccessLabelValidation:
    validation = SuccessLabelValidation()
    seen: set[tuple[str, str]] = set()
    for label in labels:
        validation.records += 1
        if label.key in seen:
            validation.errors.append(f"{label.prompt_id}/{label.arm}: duplicate success label")
        seen.add(label.key)
        if not label.prompt_id.strip():
            validation.errors.append(f"{label.prompt_id!r}: prompt_id must not be empty")
        if not label.arm.strip():
            validation.errors.append(f"{label.prompt_id}: arm must not be empty")
        if not label.annotator_batch_id.strip():
            validation.errors.append(f"{label.prompt_id}/{label.arm}: annotator_batch_id empty")
    return validation


def index_success_labels(labels: Iterable[SuccessLabel]) -> dict[tuple[str, str], SuccessLabel]:
    index: dict[tuple[str, str], SuccessLabel] = {}
    for label in labels:
        if label.key in index:
            raise ValueError(f"Duplicate success label for {label.prompt_id} / {label.arm}")
        index[label.key] = label
    return index


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
