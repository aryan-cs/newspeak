import pytest

from newspeak.dialect.tokenizer_audit import WhitespaceTokenizer, audit_terms, tokenizer_from_spec


def test_audit_terms_counts_terms_and_paraphrases():
    rows = audit_terms(
        ["safe"],
        [WhitespaceTokenizer()],
        paraphrases={"safe": "not harmful"},
    )

    assert len(rows) == 1
    assert rows[0].counts["whitespace"] == 1
    assert rows[0].paraphrase_counts["whitespace"] == 2


def test_tokenizer_from_spec_supports_whitespace():
    tokenizer = tokenizer_from_spec("whitespace")

    assert tokenizer.name == "whitespace"
    assert tokenizer.count("one two") == 2


def test_tokenizer_from_spec_rejects_unknown_prefix():
    with pytest.raises(ValueError, match="Unknown tokenizer spec"):
        tokenizer_from_spec("unknown:model")
