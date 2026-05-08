#!/usr/bin/env python3
"""Evaluate dialect and StructuredSimple validators on a JSONL gold set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.validator_gold import evaluate_gold_records, load_gold_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "gold_jsonl",
        type=Path,
        nargs="?",
        default=Path("data/eval_sets/validator_gold/examples.jsonl"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    evaluation = evaluate_gold_records(load_gold_records(args.gold_jsonl))
    payload = evaluation.to_dict()
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0 if not payload["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
