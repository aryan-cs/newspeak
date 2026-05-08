"""Evaluate validators against JSONL validator-gold records."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Iterable

from newspeak.dialect.structured_simple import StructuredSimpleChecker
from newspeak.dialect.validator import DialectValidator


@dataclass(frozen=True)
class GoldRecord:
    id: str
    target: str
    text: str
    expected_valid: bool
    violation_types: list[str]
    notes: str
    annotator_batch_id: str


@dataclass
class GoldEvaluation:
    total: int = 0
    true_positive: int = 0
    true_negative: int = 0
    false_positive: int = 0
    false_negative: int = 0
    failures: list[dict[str, object]] = field(default_factory=list)

    @property
    def precision(self) -> float | None:
        denom = self.true_positive + self.false_positive
        return self.true_positive / denom if denom else None

    @property
    def recall(self) -> float | None:
        denom = self.true_positive + self.false_negative
        return self.true_positive / denom if denom else None

    @property
    def f1(self) -> float | None:
        if self.precision is None or self.recall is None:
            return None
        denom = self.precision + self.recall
        return 2 * self.precision * self.recall / denom if denom else None

    @property
    def accuracy(self) -> float | None:
        return (self.true_positive + self.true_negative) / self.total if self.total else None

    def to_dict(self) -> dict[str, object]:
        return {
            "total": self.total,
            "true_positive": self.true_positive,
            "true_negative": self.true_negative,
            "false_positive": self.false_positive,
            "false_negative": self.false_negative,
            "precision": self.precision,
            "recall": self.recall,
            "f1": self.f1,
            "accuracy": self.accuracy,
            "failures": self.failures,
        }


def load_gold_records(path: Path) -> list[GoldRecord]:
    records: list[GoldRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            try:
                records.append(
                    GoldRecord(
                        id=payload["id"],
                        target=payload["target"],
                        text=payload["text"],
                        expected_valid=bool(payload["expected_valid"]),
                        violation_types=list(payload["violation_types"]),
                        notes=payload["notes"],
                        annotator_batch_id=payload["annotator_batch_id"],
                    )
                )
            except KeyError as exc:
                raise ValueError(f"Missing field {exc.args[0]!r} on line {line_no}") from exc
    return records


def evaluate_gold_records(
    records: Iterable[GoldRecord],
    dialect_validator: DialectValidator | None = None,
    structured_checker: StructuredSimpleChecker | None = None,
) -> GoldEvaluation:
    dialect_validator = dialect_validator or DialectValidator.from_dialect_dir()
    structured_checker = structured_checker or StructuredSimpleChecker()
    evaluation = GoldEvaluation()

    for record in records:
        if record.target == "dialect":
            result = dialect_validator.validate(record.text)
            predicted_valid = result.passed
            details = result.to_dict()
        elif record.target == "structured_simple":
            result = structured_checker.validate(record.text)
            predicted_valid = result.passed
            details = result.to_dict()
        else:
            raise ValueError(f"Unknown target {record.target!r} for {record.id}")

        evaluation.total += 1
        if predicted_valid and record.expected_valid:
            evaluation.true_positive += 1
        elif predicted_valid and not record.expected_valid:
            evaluation.false_positive += 1
        elif not predicted_valid and record.expected_valid:
            evaluation.false_negative += 1
        else:
            evaluation.true_negative += 1

        if predicted_valid != record.expected_valid:
            evaluation.failures.append(
                {
                    "id": record.id,
                    "target": record.target,
                    "expected_valid": record.expected_valid,
                    "predicted_valid": predicted_valid,
                    "details": details,
                }
            )

    return evaluation
