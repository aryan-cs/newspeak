from newspeak.dialect.tokenizer_audit import WhitespaceTokenizer, audit_terms


def test_audit_terms_counts_terms_and_paraphrases():
    rows = audit_terms(
        ["safe"],
        [WhitespaceTokenizer()],
        paraphrases={"safe": "not harmful"},
    )

    assert len(rows) == 1
    assert rows[0].counts["whitespace"] == 1
    assert rows[0].paraphrase_counts["whitespace"] == 2
