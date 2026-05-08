import json

from newspeak.evals.readiness import check_milestone1, check_milestone2


def _prompt(prompt_id, split_role):
    return {
        "prompt_id": prompt_id,
        "split_role": split_role,
        "source_type": "custom_authored",
        "task_category": "instruction_following",
        "safety_category": "benign",
        "prompt": f"Explain protocol check {prompt_id}.",
        "holdout": True,
    }


def test_milestone2_reports_missing_prompt_sets(tmp_path):
    report = check_milestone2(tmp_path, min_smoke_prompts=1, min_gate_prompts=1)

    assert not report.ready
    assert any("smoke_prompt_set" in blocker for blocker in report.blockers)
    assert any("gate_prompt_set" in blocker for blocker in report.blockers)


def test_milestone2_accepts_valid_prompt_sets_with_test_thresholds(tmp_path):
    smoke_dir = tmp_path / "data/eval_sets/smoke"
    gate_dir = tmp_path / "data/eval_sets/gate"
    smoke_dir.mkdir(parents=True)
    gate_dir.mkdir(parents=True)
    smoke_dir.joinpath("prompts.jsonl").write_text(
        json.dumps(_prompt("smoke_001", "smoke")) + "\n",
        encoding="utf-8",
    )
    gate_dir.joinpath("prompts.jsonl").write_text(
        json.dumps(_prompt("gate_001", "gate")) + "\n",
        encoding="utf-8",
    )

    report = check_milestone2(
        tmp_path,
        min_smoke_prompts=1,
        max_smoke_prompts=2,
        min_gate_prompts=1,
    )

    assert report.ready
    assert report.checks["smoke_prompt_set"]["records"] == 1
    assert report.checks["gate_prompt_set"]["records"] == 1


def test_milestone1_current_repo_is_not_ready_until_tokenizers_and_gold_are_real():
    report = check_milestone1(
        __import__("pathlib").Path.cwd(),
        min_validator_gold_records=100,
    )

    assert not report.ready
    assert any("Milestone 1 tokenizer audit requires" in blocker for blocker in report.blockers)
    assert any("validator gold set is too small" in blocker for blocker in report.blockers)
