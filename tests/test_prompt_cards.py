import importlib.util
import json
from pathlib import Path

import pytest

from newspeak.analysis.manifest import sha256_file
from newspeak.evals.prompt_cards import (
    CONTAMINATION_REPORT_PLACEHOLDER,
    PURPOSE_PLACEHOLDER,
    build_prompt_set_card,
    render_prompt_set_card,
)


def _write_prompt_set(path: Path) -> None:
    rows = [
        {
            "prompt_id": "gate_001",
            "split_role": "gate",
            "source_type": "custom_authored",
            "task_category": "instruction_following",
            "safety_category": "benign",
            "prompt": "Explain why token counts must be success-conditioned.",
            "holdout": True,
        },
        {
            "prompt_id": "main_001",
            "split_role": "main_eval",
            "source_type": "benchmark",
            "task_category": "math",
            "safety_category": "benign_sensitive",
            "prompt": "Solve a benchmark-style arithmetic word problem.",
            "holdout": True,
            "source_ref": "benchmark:example",
        },
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def test_build_prompt_set_card_validates_counts_and_hashes_file(tmp_path):
    prompt_jsonl = tmp_path / "gate_prompts.jsonl"
    _write_prompt_set(prompt_jsonl)

    card = build_prompt_set_card(prompt_jsonl, title="Gate Prompt Set Card", root=tmp_path)

    assert card.title == "Gate Prompt Set Card"
    assert card.status == "draft"
    assert card.purpose == PURPOSE_PLACEHOLDER
    assert card.summary.records == 2
    assert card.summary.split_roles == {"gate": 1, "main_eval": 1}
    assert card.summary.source_types == {"benchmark": 1, "custom_authored": 1}
    assert card.summary.task_categories == {"instruction_following": 1, "math": 1}
    assert card.summary.safety_categories == {"benign": 1, "benign_sensitive": 1}
    assert card.summary.holdout == {"true": 2}
    assert card.digest.path == "gate_prompts.jsonl"
    assert card.digest.sha256 == sha256_file(prompt_jsonl)


def test_render_prompt_set_card_includes_required_markdown_fields(tmp_path):
    prompt_jsonl = tmp_path / "smoke.jsonl"
    _write_prompt_set(prompt_jsonl)

    markdown = render_prompt_set_card(prompt_jsonl, root=tmp_path)

    assert markdown.startswith("# Smoke Prompt Set Card\n")
    assert f"Purpose: {PURPOSE_PLACEHOLDER}" in markdown
    assert "- Records: 2" in markdown
    assert "- Split: gate=1, main_eval=1" in markdown
    assert "- Source: benchmark=1, custom_authored=1" in markdown
    assert "- Task: instruction_following=1, math=1" in markdown
    assert "- Safety: benign=1, benign_sensitive=1" in markdown
    assert "- Holdout: true=2" in markdown
    assert f"- SHA256: `{sha256_file(prompt_jsonl)}`" in markdown
    assert f"Contamination report path: {CONTAMINATION_REPORT_PLACEHOLDER}" in markdown


def test_build_prompt_set_card_rejects_invalid_prompt_sets(tmp_path):
    prompt_jsonl = tmp_path / "invalid.jsonl"
    prompt_jsonl.write_text(
        json.dumps(
            {
                "prompt_id": "gate_001",
                "split_role": "gate",
                "source_type": "custom_authored",
                "task_category": "instruction_following",
                "safety_category": "benign",
                "prompt": "This eval prompt is not marked holdout.",
                "holdout": False,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="prompt set validation failed"):
        build_prompt_set_card(prompt_jsonl, root=tmp_path)


def test_make_prompt_set_card_script_writes_output(tmp_path):
    prompt_jsonl = tmp_path / "prompts.jsonl"
    output = tmp_path / "card.md"
    _write_prompt_set(prompt_jsonl)
    script = Path(__file__).resolve().parents[1] / "scripts" / "make_prompt_set_card.py"
    spec = importlib.util.spec_from_file_location("make_prompt_set_card", script)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    exit_code = module.main(
        [
            str(prompt_jsonl),
            "--output",
            str(output),
            "--title",
            "Generated Prompt Card",
            "--root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert output.read_text(encoding="utf-8").startswith("# Generated Prompt Card\n")
