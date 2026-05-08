#!/usr/bin/env python3
"""Generation entry point placeholder.

Real generation backends are intentionally not enabled until model/tokenizer
selection and prompt-set holdout rules are complete.
"""

from __future__ import annotations

import sys


def main() -> int:
    print(
        "Generation is blocked until model/tokenizer selection and gate prompt sets are frozen.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
