#!/usr/bin/env python3
"""Run a tokenizer audit over the current dialect lexicon."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.dialect.tokenizer_audit import (
    WhitespaceTokenizer,
    audit_terms,
    load_terms_from_lexicon,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lexicon", type=Path, default=Path("dialect/lexicon.yaml"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    terms = load_terms_from_lexicon(args.lexicon)
    rows = audit_terms(terms, [WhitespaceTokenizer()])

    if args.output:
        write_jsonl(rows, args.output)
    else:
        print(json.dumps([row.to_dict() for row in rows], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
