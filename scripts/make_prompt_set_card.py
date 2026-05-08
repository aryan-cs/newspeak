#!/usr/bin/env python3
"""Render a Markdown card for a validated prompt-set JSONL file."""

from __future__ import annotations

import argparse
from pathlib import Path

from newspeak.evals.prompt_cards import (
    CONTAMINATION_REPORT_PLACEHOLDER,
    PURPOSE_PLACEHOLDER,
    render_prompt_set_card,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt_jsonl", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--status", default="draft")
    parser.add_argument("--purpose", default=PURPOSE_PLACEHOLDER)
    parser.add_argument("--contamination-report-path", default=CONTAMINATION_REPORT_PLACEHOLDER)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    markdown = render_prompt_set_card(
        args.prompt_jsonl,
        title=args.title,
        status=args.status,
        purpose=args.purpose,
        contamination_report_path=args.contamination_report_path,
        root=args.root,
    )

    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
