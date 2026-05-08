#!/usr/bin/env python3
"""Analyze JSONL results with success-conditioned token metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.analysis.results import (
    load_result_records,
    paired_success_reduction,
    summarize_by_arm,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--baseline-arm", default=None)
    parser.add_argument("--candidate-arm", default=None)
    parser.add_argument(
        "--token-field",
        default="output_tokens",
        choices=["prompt_tokens", "output_tokens", "total_tokens"],
    )
    args = parser.parse_args(argv)

    records = load_result_records(args.jsonl)
    payload: dict[str, object] = {
        "records": len(records),
        "arms": [summary.to_dict() for summary in summarize_by_arm(records)],
    }
    if args.baseline_arm or args.candidate_arm:
        if not args.baseline_arm or not args.candidate_arm:
            parser.error("--baseline-arm and --candidate-arm must be provided together")
        payload["paired_success_reduction"] = paired_success_reduction(
            records,
            baseline_arm=args.baseline_arm,
            candidate_arm=args.candidate_arm,
            token_field=args.token_field,
        ).to_dict()

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
