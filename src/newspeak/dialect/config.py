"""Configuration loading helpers.

The repository stores early rule files as JSON-compatible YAML. If PyYAML is
available, it is used; otherwise the standard-library JSON parser reads the same
files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DIALECT_DIR = PROJECT_ROOT / "dialect"


def load_mapping(path: Path) -> dict[str, Any]:
    """Load a JSON-compatible YAML mapping from disk."""

    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except ModuleNotFoundError:
        data = json.loads(text)

    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def flatten_values(value: Any) -> set[str]:
    """Flatten nested config values into a lowercase string set."""

    out: set[str] = set()
    if isinstance(value, str):
        out.add(value.lower())
    elif isinstance(value, list):
        for item in value:
            out.update(flatten_values(item))
    elif isinstance(value, dict):
        for item in value.values():
            out.update(flatten_values(item))
    return out
