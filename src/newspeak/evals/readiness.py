"""Milestone readiness checks for the research protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from newspeak.evals.model_config import validate_model_config_file
from newspeak.evals.prompt_set import load_prompt_records, validate_prompt_records
from newspeak.evals.validator_gold import evaluate_gold_records, load_gold_records


@dataclass
class ReadinessReport:
    milestone: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: dict[str, object] = field(default_factory=dict)

    @property
    def ready(self) -> bool:
        return not self.blockers

    def to_dict(self) -> dict[str, object]:
        return {
            "milestone": self.milestone,
            "ready": self.ready,
            "blockers": self.blockers,
            "warnings": self.warnings,
            "checks": self.checks,
        }


def check_milestone1(
    root: Path,
    *,
    min_validator_gold_records: int = 100,
    min_validator_precision: float = 0.95,
    min_validator_recall: float = 0.85,
) -> ReadinessReport:
    root = root.resolve()
    report = ReadinessReport(milestone="milestone1")
    required_files = [
        "dialect/spec.md",
        "dialect/structured_simple_spec.md",
        "dialect/lexicon.yaml",
        "dialect/morphology.yaml",
        "dialect/safety_terms.yaml",
        "scripts/validate_dialect.py",
        "scripts/validate_structured_simple.py",
        "scripts/audit_tokenizers.py",
    ]
    missing = [path for path in required_files if not (root / path).exists()]
    report.checks["required_files"] = {"checked": required_files, "missing": missing}
    for path in missing:
        report.blockers.append(f"missing required Milestone 1 file: {path}")

    model_config_path = root / "configs/models/tokenizers.yaml"
    if model_config_path.exists():
        model_validation = validate_model_config_file(
            model_config_path,
            require_milestone1_ready=True,
        )
        report.checks["model_config"] = model_validation.to_dict()
        report.blockers.extend(f"model config: {error}" for error in model_validation.errors)
        report.warnings.extend(f"model config: {warning}" for warning in model_validation.warnings)
    else:
        report.blockers.append("missing configs/models/tokenizers.yaml")

    gold_path = root / "data/eval_sets/validator_gold/examples.jsonl"
    if gold_path.exists():
        gold_records = load_gold_records(gold_path)
        evaluation = evaluate_gold_records(gold_records)
        report.checks["validator_gold"] = evaluation.to_dict()
        report.checks["validator_gold"]["min_required_records"] = min_validator_gold_records
        if evaluation.total < min_validator_gold_records:
            report.blockers.append(
                "validator gold set is too small for deployment thresholding: "
                f"{evaluation.total} < {min_validator_gold_records}"
            )
        if evaluation.precision is None or evaluation.precision < min_validator_precision:
            report.blockers.append(
                "validator precision below threshold: "
                f"{evaluation.precision} < {min_validator_precision}"
            )
        if evaluation.recall is None or evaluation.recall < min_validator_recall:
            report.blockers.append(
                f"validator recall below threshold: {evaluation.recall} < {min_validator_recall}"
            )
    else:
        report.blockers.append("missing validator gold JSONL file")

    return report


def check_milestone2(
    root: Path,
    *,
    min_smoke_prompts: int = 50,
    max_smoke_prompts: int = 100,
    min_gate_prompts: int = 200,
) -> ReadinessReport:
    root = root.resolve()
    report = ReadinessReport(milestone="milestone2")
    report.checks["smoke_prompt_set"] = _check_prompt_set(
        root / "data/eval_sets/smoke/prompts.jsonl",
        min_records=min_smoke_prompts,
        max_records=max_smoke_prompts,
    )
    report.checks["gate_prompt_set"] = _check_prompt_set(
        root / "data/eval_sets/gate/prompts.jsonl",
        min_records=min_gate_prompts,
        max_records=None,
    )

    for label in ("smoke_prompt_set", "gate_prompt_set"):
        check = report.checks[label]
        if isinstance(check, dict):
            report.blockers.extend(f"{label}: {error}" for error in check.get("errors", []))
            report.warnings.extend(f"{label}: {warning}" for warning in check.get("warnings", []))
    return report


def _check_prompt_set(
    path: Path,
    *,
    min_records: int,
    max_records: int | None,
) -> dict[str, object]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "records": 0,
            "errors": [f"missing {path}"],
            "warnings": [],
        }
    records = load_prompt_records(path)
    validation = validate_prompt_records(records)
    errors = list(validation.errors)
    warnings = list(validation.warnings)
    if len(records) < min_records:
        errors.append(f"expected at least {min_records} records, found {len(records)}")
    if max_records is not None and len(records) > max_records:
        errors.append(f"expected at most {max_records} records, found {len(records)}")
    return {
        "path": str(path),
        "exists": True,
        "records": len(records),
        "errors": errors,
        "warnings": warnings,
        "summary": validation.summary,
    }
