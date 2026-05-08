#!/usr/bin/env python3
"""Validate text against StructuredSimple-English sentence-shape rules."""

from __future__ import annotations

import argparse
import json
import sys

from newspeak.dialect.structured_simple import StructuredSimpleChecker


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", help="Text to validate. Reads stdin if omitted.")
    parser.add_argument("--max-sentence-words", type=int, default=20)
    args = parser.parse_args(argv)

    text = args.text if args.text is not None else sys.stdin.read()
    result = StructuredSimpleChecker(max_sentence_words=args.max_sentence_words).validate(text)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
