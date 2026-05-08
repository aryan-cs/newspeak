#!/usr/bin/env python3
"""Validate a manually translated parallel JSONL dataset.

This script does not generate translations. It checks that required fields exist
before a human/model-assisted translation workflow is accepted downstream.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {
    "english_prompt",
    "dialect_prompt",
    "english_answer",
    "dialect_answer",
    "task_category",
    "safety_label",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args(argv)

    failures = []
    with args.jsonl.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            record = json.loads(line)
            missing = sorted(REQUIRED_FIELDS - set(record))
            if missing:
                failures.append({"line": line_no, "missing": missing})

    if failures:
        print(json.dumps({"passed": False, "failures": failures}, indent=2))
        return 1
    print(json.dumps({"passed": True, "records": line_no if "line_no" in locals() else 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
