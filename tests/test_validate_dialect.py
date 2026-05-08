from newspeak.dialect.validator import DialectValidator


def test_dialect_validator_accepts_allowed_terms_and_passthrough():
    validator = DialectValidator.from_dialect_dir()
    result = validator.validate("I cannot help with unsafe harm. Use Python to count tokens.")

    assert result.passed
    assert result.checked_tokens > 0
    assert result.passthrough_tokens >= 1


def test_dialect_validator_rejects_forbidden_source_terms():
    validator = DialectValidator.from_dialect_dir()
    result = validator.validate("Use goodthink to solve it.")

    assert not result.passed
    assert any(v.violation_type == "forbidden_source_term" for v in result.violations)


def test_dialect_validator_accepts_productive_hyphenated_forms():
    validator = DialectValidator.from_dialect_dir()
    result = validator.validate("This claim is non-valid.")

    assert result.passed
