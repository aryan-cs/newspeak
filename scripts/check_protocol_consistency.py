#!/usr/bin/env python3
"""Check that protocol-critical labels stay consistent across scaffold files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_ARMS = {
    "Base-English",
    "Base-Concise",
    "StructuredSimple-English",
    "Prompt-Newspeak",
    "ICL-Newspeak",
    "TokenizerAware-Newspeak",
    "StyleOnly-Newspeak",
    "Repair-Newspeak",
    "InputOutput-Newspeak",
    "VisibleReasoning-Newspeak",
    "LoRA-Newspeak",
    "LoRA-Newspeak-Safety",
    "HighCompliance-Constrained",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    root = args.root.resolve()
    errors: list[str] = []

    result_schema = json.loads((root / "schemas/results.schema.json").read_text(encoding="utf-8"))
    schema_arms = set(result_schema["properties"]["arm"]["enum"])
    missing_schema_arms = sorted(REQUIRED_ARMS - schema_arms)
    extra_schema_arms = sorted(schema_arms - REQUIRED_ARMS)
    if missing_schema_arms:
        errors.append(f"results schema missing arms: {', '.join(missing_schema_arms)}")
    if extra_schema_arms:
        errors.append(f"results schema has unrecognized arms: {', '.join(extra_schema_arms)}")

    plan_text = (root / "PLAN.md").read_text(encoding="utf-8")
    for arm in sorted(REQUIRED_ARMS):
        if arm not in plan_text:
            errors.append(f"PLAN.md does not mention arm: {arm}")
    if '"Hard-Constrained"' in plan_text or "`Hard-Constrained` |" in plan_text:
        errors.append("PLAN.md appears to use Hard-Constrained as a formal arm label")

    structured_simple_script = root / "scripts/validate_structured_simple.py"
    if not structured_simple_script.exists():
        errors.append("missing scripts/validate_structured_simple.py")
    dialect_validator_script = root / "scripts/validate_dialect.py"
    if not dialect_validator_script.exists():
        errors.append("missing scripts/validate_dialect.py")

    payload = {"passed": not errors, "errors": errors}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
