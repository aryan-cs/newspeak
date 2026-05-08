#!/usr/bin/env python3
"""Report protocol readiness for Milestone 1 or Milestone 2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.readiness import check_milestone1, check_milestone2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--milestone", choices=["1", "2"], required=True)
    parser.add_argument("--min-validator-gold-records", type=int, default=100)
    parser.add_argument("--min-smoke-prompts", type=int, default=50)
    parser.add_argument("--max-smoke-prompts", type=int, default=100)
    parser.add_argument("--min-gate-prompts", type=int, default=200)
    args = parser.parse_args(argv)

    if args.milestone == "1":
        report = check_milestone1(
            args.root,
            min_validator_gold_records=args.min_validator_gold_records,
        )
    else:
        report = check_milestone2(
            args.root,
            min_smoke_prompts=args.min_smoke_prompts,
            max_smoke_prompts=args.max_smoke_prompts,
            min_gate_prompts=args.min_gate_prompts,
        )
    print(json.dumps(report.to_dict(), indent=2, sort_keys=True))
    return 0 if report.ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
