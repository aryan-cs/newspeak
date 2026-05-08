#!/usr/bin/env python3
"""Validate success-label JSONL records before result materialization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.success_labels import load_success_labels, validate_success_labels


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("success_labels_jsonl", type=Path)
    args = parser.parse_args(argv)

    validation = validate_success_labels(load_success_labels(args.success_labels_jsonl))
    print(json.dumps(validation.to_dict(), indent=2, sort_keys=True))
    return 0 if validation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
