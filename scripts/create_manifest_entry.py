#!/usr/bin/env python3
"""Create a machine-readable MANIFEST.md entry draft for artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from newspeak.analysis.manifest import build_manifest_entry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entry-id", required=True)
    parser.add_argument("--status", default="planned")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--remote-url", default=None)
    parser.add_argument("artifacts", nargs="*", type=Path)
    args = parser.parse_args(argv)

    entry = build_manifest_entry(
        entry_id=args.entry_id,
        status=args.status,
        artifact_paths=args.artifacts,
        root=args.root,
        remote_url=args.remote_url,
    )
    print(json.dumps(entry, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
