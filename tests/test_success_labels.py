import json

import pytest

from newspeak.evals.success_labels import (
    SuccessLabel,
    index_success_labels,
    load_success_labels,
    validate_success_labels,
)


def _label(**overrides):
    payload = {
        "prompt_id": "p1",
        "arm": "Base-English",
        "correct_or_adequate": True,
        "safe": True,
        "helpful_or_quality_refusal": True,
        "semantically_preserved": True,
        "label_source": "objective_scorer",
        "annotator_batch_id": "batch-1",
        "notes": "test fixture",
    }
    payload.update(overrides)
    return SuccessLabel.from_payload(payload, line_no=1)


def test_success_label_computes_primary_success():
    label = _label(safe=False)

    assert label.success_flags()["primary_success"] is False


def test_success_label_rejects_unknown_source():
    with pytest.raises(ValueError, match="invalid label_source"):
        _label(label_source="model_guess")


def test_validate_success_labels_rejects_duplicate_keys():
    validation = validate_success_labels([_label(), _label()])

    assert not validation.passed
    assert any("duplicate success label" in error for error in validation.errors)


def test_index_success_labels_returns_keyed_labels():
    label = _label()

    assert index_success_labels([label])[("p1", "Base-English")] == label


def test_load_success_labels_reports_missing_fields(tmp_path):
    path = tmp_path / "labels.jsonl"
    path.write_text(json.dumps({"prompt_id": "p1"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_success_labels(path)
