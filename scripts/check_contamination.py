#!/usr/bin/env python3
"""Check exact and n-gram overlap between two JSONL prompt files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.analysis.contamination import find_overlaps, load_jsonl_text_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--left-text-field", default="prompt")
    parser.add_argument("--right-text-field", default="prompt")
    parser.add_argument("--left-id-field", default="prompt_id")
    parser.add_argument("--right-id-field", default="prompt_id")
    parser.add_argument("--ngram-size", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=0.8)
    args = parser.parse_args(argv)

    left_records = load_jsonl_text_records(args.left, args.left_text_field, args.left_id_field)
    right_records = load_jsonl_text_records(args.right, args.right_text_field, args.right_id_field)
    findings = find_overlaps(left_records, right_records, args.ngram_size, args.threshold)
    print(json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
