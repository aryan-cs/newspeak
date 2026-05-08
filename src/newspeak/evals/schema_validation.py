"""Small JSON-schema subset validator for project artifact records.

The project keeps `jsonschema` optional. This module validates the subset used by
the repository schemas: object fields, required keys, additionalProperties,
arrays, primitive types, enums, and numeric minimums.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SchemaError:
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"path": self.path, "message": self.message}


@dataclass
class SchemaValidation:
    records: int = 0
    errors: list[SchemaError] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "records": self.records,
            "errors": [error.to_dict() for error in self.errors],
        }


def load_schema(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Schema file {path} must contain a JSON object.")
    return payload


def validate_jsonl(path: Path, schema: dict[str, Any]) -> SchemaValidation:
    validation = SchemaValidation()
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            validation.records += 1
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                validation.errors.append(SchemaError(f"line {line_no}", f"invalid JSON: {exc.msg}"))
                continue
            validation.errors.extend(validate_value(payload, schema, f"line {line_no}"))
    return validation


def validate_value(value: Any, schema: dict[str, Any], path: str = "$") -> list[SchemaError]:
    errors: list[SchemaError] = []
    expected_type = schema.get("type")
    if expected_type is not None and not _matches_type(value, expected_type):
        errors.append(SchemaError(path, f"expected type {_type_name(expected_type)}"))
        return errors

    if "enum" in schema and value not in schema["enum"]:
        errors.append(SchemaError(path, f"expected one of {schema['enum']!r}"))

    if isinstance(value, (int, float)) and not isinstance(value, bool) and "minimum" in schema:
        minimum = schema["minimum"]
        if value < minimum:
            errors.append(SchemaError(path, f"expected >= {minimum}"))

    if isinstance(value, dict):
        errors.extend(_validate_object(value, schema, path))
    elif isinstance(value, list):
        errors.extend(_validate_array(value, schema, path))
    return errors


def _validate_object(value: dict[str, Any], schema: dict[str, Any], path: str) -> list[SchemaError]:
    errors: list[SchemaError] = []
    required = schema.get("required", [])
    for key in required:
        if key not in value:
            errors.append(SchemaError(f"{path}.{key}", "missing required field"))

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}

    if schema.get("additionalProperties") is False:
        extra = sorted(set(value) - set(properties))
        for key in extra:
            errors.append(SchemaError(f"{path}.{key}", "additional property not allowed"))

    for key, child_schema in properties.items():
        if key in value and isinstance(child_schema, dict):
            errors.extend(validate_value(value[key], child_schema, f"{path}.{key}"))
    return errors


def _validate_array(value: list[Any], schema: dict[str, Any], path: str) -> list[SchemaError]:
    item_schema = schema.get("items")
    if not isinstance(item_schema, dict):
        return []
    errors: list[SchemaError] = []
    for index, item in enumerate(value):
        errors.extend(validate_value(item, item_schema, f"{path}[{index}]"))
    return errors


def _matches_type(value: Any, expected_type: str | list[str]) -> bool:
    if isinstance(expected_type, list):
        return any(_matches_type(value, item) for item in expected_type)
    if expected_type == "null":
        return value is None
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    raise ValueError(f"Unsupported schema type {expected_type!r}")


def _type_name(expected_type: str | list[str]) -> str:
    if isinstance(expected_type, list):
        return " or ".join(expected_type)
    return expected_type
