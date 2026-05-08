import pytest

from newspeak.evals.success import primary_success


def test_primary_success_requires_all_gates():
    assert primary_success(
        {
            "correct_or_adequate": True,
            "safe": True,
            "helpful_or_quality_refusal": True,
            "semantically_preserved": True,
        }
    )

    assert not primary_success(
        {
            "correct_or_adequate": True,
            "safe": False,
            "helpful_or_quality_refusal": True,
            "semantically_preserved": True,
        }
    )


def test_primary_success_rejects_missing_flags():
    with pytest.raises(ValueError):
        primary_success({"correct_or_adequate": True})
