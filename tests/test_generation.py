from pathlib import Path

import pytest

from newspeak.evals.arms import FewShotExample, build_messages
from newspeak.evals.generation import (
    assert_heavy_root,
    prepare_request_record,
    raw_generation_record,
    text_metrics,
)


def test_icl_requires_validated_few_shots():
    with pytest.raises(ValueError, match="requires --few-shot-jsonl"):
        build_messages("ICL-Newspeak", "Explain the protocol.")


def test_build_messages_includes_few_shots_before_live_prompt():
    messages = build_messages(
        "ICL-Newspeak",
        "Live prompt",
        [FewShotExample(user="Example user", assistant="Example assistant")],
    )

    assert [message.role for message in messages] == ["system", "user", "assistant", "user"]
    assert messages[-1].content == "Live prompt"


def test_text_metrics_counts_response_fields():
    metrics = text_metrics("safe short answer", prompt_tokens=10, output_tokens=3, latency_ms=1500)

    assert metrics.total_tokens == 13
    assert metrics.words == 3
    assert metrics.tokens_per_second == 2


def test_prepare_request_records_are_not_model_outputs():
    messages = build_messages("Base-English", "What is the gate?")
    record = prepare_request_record(
        run_id="run",
        prompt_id="p1",
        arm="Base-English",
        model_id="model",
        tokenizer_id="tok",
        prompt="What is the gate?",
        messages=messages,
    )

    assert record["status"] == "prepared_request_not_model_output"
    assert "response" not in record


def test_raw_generation_record_contains_metrics_and_response():
    messages = build_messages("Base-English", "What is the gate?")
    record = raw_generation_record(
        run_id="run",
        prompt_id="p1",
        arm="Base-English",
        model_id="model",
        tokenizer_id="tok",
        prompt="What is the gate?",
        messages=messages,
        response="A gate blocks expensive evaluation until token savings are plausible.",
        metrics=text_metrics("A gate blocks expensive evaluation."),
    )

    assert record["response"].startswith("A gate")
    assert record["metrics"]["characters"] > 0


def test_heavy_root_guard_blocks_non_h200_paths():
    with pytest.raises(RuntimeError, match="Heavy generation is only allowed"):
        assert_heavy_root(Path("/tmp/newspeak"), Path("/home/aryang9/sandbox/newspeak"))
