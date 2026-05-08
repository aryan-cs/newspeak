from newspeak.evals.model_config import validate_model_config


def test_unselected_scaffold_passes_but_is_not_ready():
    validation = validate_model_config(
        {
            "primary": {"status": "unselected", "model_family": None, "tokenizer_id": None},
            "comparison_tokenizers": [
                {"status": "unselected", "tokenizer_id": None},
                {"status": "unselected", "tokenizer_id": None},
            ],
        }
    )

    assert validation.passed
    assert validation.summary["milestone1_ready"] is False
    assert validation.warnings


def test_require_milestone1_ready_turns_not_ready_into_error():
    validation = validate_model_config(
        {
            "primary": {"status": "unselected"},
            "comparison_tokenizers": [],
        },
        require_milestone1_ready=True,
    )

    assert not validation.passed
    assert any("Milestone 1 tokenizer audit requires" in error for error in validation.errors)


def test_selected_entries_require_tokenizer_id_and_revision():
    validation = validate_model_config(
        {
            "primary": {"status": "selected", "tokenizer_id": "model/tokenizer", "revision": ""},
            "comparison_tokenizers": [
                {"status": "selected", "tokenizer_id": None, "revision": "abc123"},
                {"status": "selected", "tokenizer_id": "other/tokenizer", "revision": "def456"},
            ],
        }
    )

    assert not validation.passed
    assert any("primary.revision" in error for error in validation.errors)
    assert any("comparison_tokenizers[0].tokenizer_id" in error for error in validation.errors)


def test_ready_config_has_primary_and_two_comparisons():
    validation = validate_model_config(
        {
            "primary": {
                "status": "selected",
                "model_family": "example",
                "tokenizer_id": "org/model-a",
                "revision": "aaa",
            },
            "comparison_tokenizers": [
                {"status": "selected", "tokenizer_id": "org/model-b", "revision": "bbb"},
                {"status": "selected", "tokenizer_id": "org/model-c", "revision": "ccc"},
            ],
        },
        require_milestone1_ready=True,
    )

    assert validation.passed
    assert validation.summary["milestone1_ready"] is True
