import json

import pytest

from newspeak.evals.prompt_set import (
    PromptRecord,
    load_prompt_records,
    summarize_prompt_records,
    validate_prompt_records,
)


def _record(**overrides):
    payload = {
        "prompt_id": "gate_001",
        "split_role": "gate",
        "source_type": "custom_authored",
        "task_category": "instruction_following",
        "safety_category": "benign",
        "prompt": "Explain why response token counts must be success-conditioned.",
        "holdout": True,
        "source_ref": None,
        "expected_scoring": "human_adequacy",
        "notes": "test-only fixture",
    }
    payload.update(overrides)
    return PromptRecord.from_payload(payload, line_no=1)


def test_valid_prompt_set_passes():
    validation = validate_prompt_records([_record()])

    assert validation.passed
    assert validation.summary["records"] == 1
    assert validation.summary["split_roles"] == {"gate": 1}


def test_eval_prompt_must_be_holdout():
    validation = validate_prompt_records([_record(holdout=False)])

    assert not validation.passed
    assert any("holdout=true" in error for error in validation.errors)


def test_benchmark_prompt_requires_source_ref():
    validation = validate_prompt_records([_record(source_type="benchmark", source_ref=None)])

    assert not validation.passed
    assert any("source_ref required" in error for error in validation.errors)


def test_duplicate_prompt_ids_and_text_are_errors():
    records = [
        _record(prompt_id="one", prompt="Count the output tokens."),
        _record(prompt_id="one", prompt="Different prompt text."),
        _record(prompt_id="two", prompt="Count the output tokens!"),
    ]

    validation = validate_prompt_records(records)

    assert not validation.passed
    assert any("duplicate prompt_id" in error for error in validation.errors)
    assert any("duplicate normalized prompt text" in error for error in validation.errors)


def test_unknown_fields_are_rejected():
    with pytest.raises(ValueError, match="unknown fields"):
        PromptRecord.from_payload(
            {
                "prompt_id": "gate_001",
                "split_role": "gate",
                "source_type": "custom_authored",
                "task_category": "instruction_following",
                "safety_category": "benign",
                "prompt": "Explain the gate rule.",
                "holdout": True,
                "unexpected": "not allowed",
            },
            line_no=1,
        )


def test_load_prompt_records_reports_line_numbers(tmp_path):
    path = tmp_path / "prompts.jsonl"
    path.write_text(json.dumps({"prompt_id": "missing_fields"}) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Line 1: missing required fields"):
        load_prompt_records(path)


def test_summarize_prompt_records_counts_categories():
    records = [
        _record(prompt_id="one", task_category="math", safety_category="benign"),
        _record(prompt_id="two", task_category="code", safety_category="benign_sensitive"),
    ]

    summary = summarize_prompt_records(records)

    assert summary.task_categories == {"code": 1, "math": 1}
    assert summary.safety_categories == {"benign": 1, "benign_sensitive": 1}
    assert summary.holdout == {"true": 2}
