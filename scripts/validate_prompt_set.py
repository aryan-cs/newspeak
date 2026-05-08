#!/usr/bin/env python3
"""Validate a smoke/gate/evaluation prompt-set JSONL file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.prompt_set import load_prompt_records, validate_prompt_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_jsonl", type=Path)
    args = parser.parse_args(argv)

    validation = validate_prompt_records(load_prompt_records(args.prompt_jsonl))
    print(json.dumps(validation.to_dict(), indent=2, sort_keys=True))
    return 0 if validation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
