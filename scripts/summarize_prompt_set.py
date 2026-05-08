#!/usr/bin/env python3
"""Summarize a prompt-set JSONL file without scoring model outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.prompt_set import load_prompt_records, summarize_prompt_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_jsonl", type=Path)
    args = parser.parse_args(argv)

    summary = summarize_prompt_records(load_prompt_records(args.prompt_jsonl))
    print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
