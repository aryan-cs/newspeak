from newspeak.dialect.structured_simple import StructuredSimpleChecker


def test_structured_simple_accepts_short_plain_sentences():
    checker = StructuredSimpleChecker(max_sentence_words=20)
    result = checker.validate("I cannot help with that. I can give a safe summary.")

    assert result.passed
    assert result.sentence_count == 2


def test_structured_simple_rejects_long_sentence():
    checker = StructuredSimpleChecker(max_sentence_words=8)
    result = checker.validate("This sentence has too many words for the configured limit.")

    assert not result.passed
    assert any(v.violation_type == "sentence_length" for v in result.violations)


def test_structured_simple_rejects_compressed_markers():
    checker = StructuredSimpleChecker()
    result = checker.validate("Use goodthink for the answer.")

    assert not result.passed
    assert any(v.violation_type == "compressed_marker" for v in result.violations)
