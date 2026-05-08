#!/usr/bin/env python3
"""Validate text against the Newspeak-inspired dialect rules."""

from __future__ import annotations

import argparse
import json
import sys

from newspeak.dialect.validator import DialectValidator


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text", nargs="?", help="Text to validate. Reads stdin if omitted.")
    args = parser.parse_args(argv)

    text = args.text if args.text is not None else sys.stdin.read()
    result = DialectValidator.from_dialect_dir().validate(text)
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
