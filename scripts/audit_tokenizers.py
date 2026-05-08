#!/usr/bin/env python3
"""Run a tokenizer audit over the current dialect lexicon."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.dialect.tokenizer_audit import (
    audit_terms,
    load_terms_from_lexicon,
    tokenizer_from_spec,
    write_jsonl,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lexicon", type=Path, default=Path("dialect/lexicon.yaml"))
    parser.add_argument(
        "--tokenizer",
        action="append",
        default=None,
        help=(
            "Tokenizer spec. Use 'whitespace', 'hf:ORG/MODEL[@REVISION]', or "
            "'tiktoken:ENCODING_OR_MODEL'. Repeat for multiple tokenizers."
        ),
    )
    parser.add_argument("--paraphrases", type=Path, default=None)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    terms = load_terms_from_lexicon(args.lexicon)
    tokenizers = [tokenizer_from_spec(spec) for spec in (args.tokenizer or ["whitespace"])]
    paraphrases = _load_paraphrases(args.paraphrases)
    rows = audit_terms(terms, tokenizers, paraphrases=paraphrases)

    if args.output:
        write_jsonl(rows, args.output)
    else:
        print(json.dumps([row.to_dict() for row in rows], indent=2, sort_keys=True))
    return 0


def _load_paraphrases(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Paraphrases file must be a JSON object mapping term to paraphrase.")
    return {str(key): str(value) for key, value in payload.items()}


if __name__ == "__main__":
    raise SystemExit(main())
