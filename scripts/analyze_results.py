#!/usr/bin/env python3
"""Analyze JSONL results with success-conditioned token metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import median

from newspeak.evals.success import primary_success


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args(argv)

    rows = []
    with args.jsonl.open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            success = record.get("success", {})
            record["success"]["primary_success"] = primary_success(success)
            rows.append(record)

    successful = [row for row in rows if row["success"]["primary_success"]]
    output_tokens = [
        row["metrics"]["output_tokens"]
        for row in successful
        if row["metrics"].get("output_tokens") is not None
    ]
    summary = {
        "records": len(rows),
        "primary_success_records": len(successful),
        "median_output_tokens_successful": median(output_tokens) if output_tokens else None,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
