#!/usr/bin/env python3
"""Compute manifest-ready SHA-256 entries for artifact paths."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.analysis.manifest import artifact_digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    entries = [artifact_digest(path, args.root).to_dict() for path in args.paths]
    print(json.dumps(entries, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
