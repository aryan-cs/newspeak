#!/usr/bin/env python3
"""Validate model and tokenizer selection config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.evals.model_config import validate_model_config_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/models/tokenizers.yaml"))
    parser.add_argument("--require-milestone1-ready", action="store_true")
    args = parser.parse_args(argv)

    validation = validate_model_config_file(
        args.config,
        require_milestone1_ready=args.require_milestone1_ready,
    )
    print(json.dumps(validation.to_dict(), indent=2, sort_keys=True))
    return 0 if validation.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
