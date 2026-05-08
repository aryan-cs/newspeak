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
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--left-text-field", default="prompt")
    parser.add_argument("--right-text-field", default="prompt")
    parser.add_argument("--left-id-field", default="prompt_id")
    parser.add_argument("--right-id-field", default="prompt_id")
    parser.add_argument("--ngram-size", type=int, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args(argv)

    config = _load_config(args.config)
    ngram_size = args.ngram_size or int(config.get("ngram_size", 5))
    threshold = args.threshold or float(config.get("threshold", 0.8))

    left_records = load_jsonl_text_records(args.left, args.left_text_field, args.left_id_field)
    right_records = load_jsonl_text_records(args.right, args.right_text_field, args.right_id_field)
    findings = find_overlaps(left_records, right_records, ngram_size, threshold)
    print(json.dumps([finding.to_dict() for finding in findings], indent=2, sort_keys=True))
    return 1 if findings else 0


def _load_config(path: Path | None) -> dict[str, object]:
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    methods = payload.get("methods", {})
    if not isinstance(methods, dict):
        return {}
    ngram = methods.get("ngram_jaccard", {})
    if not isinstance(ngram, dict):
        return {}
    return {
        "ngram_size": ngram.get("ngram_size", 5),
        "threshold": ngram.get("threshold", 0.8),
    }


if __name__ == "__main__":
    raise SystemExit(main())
