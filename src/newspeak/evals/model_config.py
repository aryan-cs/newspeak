"""Model and tokenizer config validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from newspeak.dialect.config import load_mapping


@dataclass
class ModelConfigValidation:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: dict[str, object] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "summary": self.summary,
        }


def validate_model_config_file(
    path: Path,
    *,
    require_milestone1_ready: bool = False,
) -> ModelConfigValidation:
    return validate_model_config(load_mapping(path), require_milestone1_ready=require_milestone1_ready)


def validate_model_config(
    config: dict[str, Any],
    *,
    require_milestone1_ready: bool = False,
) -> ModelConfigValidation:
    validation = ModelConfigValidation()
    primary = config.get("primary")
    comparisons = config.get("comparison_tokenizers")

    if not isinstance(primary, dict):
        validation.errors.append("primary must be a mapping")
        primary = {}
    if not isinstance(comparisons, list):
        validation.errors.append("comparison_tokenizers must be a list")
        comparisons = []

    primary_selected = _is_selected(primary)
    selected_comparisons = [
        item for item in comparisons if isinstance(item, dict) and _is_selected(item)
    ]
    validation.summary = {
        "primary_status": primary.get("status"),
        "primary_selected": primary_selected,
        "selected_comparison_tokenizers": len(selected_comparisons),
        "milestone1_ready": primary_selected and len(selected_comparisons) >= 2,
    }

    _validate_tokenizer_entry(primary, "primary", validation)
    if primary_selected and not _nonempty(primary.get("model_family")):
        validation.warnings.append("primary selected without model_family")

    for index, item in enumerate(comparisons):
        if not isinstance(item, dict):
            validation.errors.append(f"comparison_tokenizers[{index}] must be a mapping")
            continue
        _validate_tokenizer_entry(item, f"comparison_tokenizers[{index}]", validation)

    if require_milestone1_ready and not validation.summary["milestone1_ready"]:
        validation.errors.append(
            "Milestone 1 tokenizer audit requires one selected primary tokenizer "
            "and at least two selected comparison tokenizers."
        )
    elif not validation.summary["milestone1_ready"]:
        validation.warnings.append(
            "Milestone 1 tokenizer audit is not ready: select one primary tokenizer "
            "and at least two comparison tokenizers."
        )

    return validation


def _validate_tokenizer_entry(
    entry: dict[str, Any],
    label: str,
    validation: ModelConfigValidation,
) -> None:
    status = entry.get("status")
    if status not in {"selected", "unselected"}:
        validation.errors.append(f"{label}.status must be 'selected' or 'unselected'")
        return
    if status == "selected":
        if not _nonempty(entry.get("tokenizer_id")):
            validation.errors.append(f"{label}.tokenizer_id must be set when selected")
        if not _nonempty(entry.get("revision")):
            validation.errors.append(f"{label}.revision must be set when selected")
    else:
        if _nonempty(entry.get("tokenizer_id")) or _nonempty(entry.get("revision")):
            validation.warnings.append(f"{label} has tokenizer metadata while status is unselected")


def _is_selected(entry: dict[str, Any]) -> bool:
    return entry.get("status") == "selected"


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())
