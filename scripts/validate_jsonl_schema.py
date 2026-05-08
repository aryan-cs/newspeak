#!/usr/bin/env python3
"""Validate JSONL records against one of the repository JSON schemas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.schema_validation import load_schema, validate_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--schema", required=True, type=Path)
    args = parser.parse_args(argv)

    validation = validate_jsonl(args.jsonl, load_schema(args.schema))
    print(json.dumps(validation.to_dict(), indent=2, sort_keys=True))
    return 0 if validation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
