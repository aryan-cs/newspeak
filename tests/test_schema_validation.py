import json

from newspeak.evals.schema_validation import validate_jsonl, validate_value


def test_validate_value_accepts_required_object_fields():
    schema = {
        "type": "object",
        "required": ["id", "count"],
        "properties": {
            "id": {"type": "string"},
            "count": {"type": "integer", "minimum": 0},
        },
        "additionalProperties": False,
    }

    assert validate_value({"id": "a", "count": 1}, schema) == []


def test_validate_value_reports_missing_extra_and_minimum_errors():
    schema = {
        "type": "object",
        "required": ["id", "count"],
        "properties": {
            "id": {"type": "string"},
            "count": {"type": "integer", "minimum": 0},
        },
        "additionalProperties": False,
    }

    errors = validate_value({"count": -1, "extra": True}, schema)
    messages = {(error.path, error.message) for error in errors}

    assert ("$.id", "missing required field") in messages
    assert ("$.extra", "additional property not allowed") in messages
    assert ("$.count", "expected >= 0") in messages


def test_validate_jsonl_counts_records_and_errors(tmp_path):
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {"id": {"type": "string"}},
        "additionalProperties": False,
    }
    path = tmp_path / "records.jsonl"
    path.write_text(
        json.dumps({"id": "ok"}) + "\n" + json.dumps({"id": 5}) + "\n",
        encoding="utf-8",
    )

    validation = validate_jsonl(path, schema)

    assert validation.records == 2
    assert not validation.passed
    assert validation.errors[0].path == "line 2.id"


def test_validate_value_supports_arrays_and_enums():
    schema = {
        "type": "object",
        "required": ["items"],
        "properties": {
            "items": {
                "type": "array",
                "items": {"type": "string", "enum": ["a", "b"]},
            }
        },
        "additionalProperties": False,
    }

    errors = validate_value({"items": ["a", "c"]}, schema)

    assert errors[0].path == "$.items[1]"
    assert "expected one of" in errors[0].message
