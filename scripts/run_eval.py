#!/usr/bin/env python3
"""Create compliance reports or schema-ready results from raw generations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from newspeak.dialect.structured_simple import StructuredSimpleChecker
from newspeak.dialect.validator import DialectValidator
from newspeak.evals.success_labels import (
    index_success_labels,
    load_success_labels,
    validate_success_labels,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generations", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--mode", choices=["compliance", "results"], default="compliance")
    parser.add_argument("--success-labels", type=Path, default=None)
    args = parser.parse_args(argv)

    generations = _load_jsonl(args.generations)
    dialect_validator = DialectValidator.from_dialect_dir()
    structured_checker = StructuredSimpleChecker()

    if args.mode == "compliance":
        report = [
            _compliance_record(record, dialect_validator, structured_checker)
            for record in generations
        ]
        _write_jsonl(args.output, report)
        print(f"Wrote {len(report)} compliance records to {args.output}")
        return 0

    if args.success_labels is None:
        print(
            "Result creation requires --success-labels; refusing to fabricate success flags.",
            file=sys.stderr,
        )
        return 2

    loaded_labels = load_success_labels(args.success_labels)
    label_validation = validate_success_labels(loaded_labels)
    if not label_validation.passed:
        print("Success-label validation failed; refusing result creation.", file=sys.stderr)
        for error in label_validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    labels = index_success_labels(loaded_labels)
    results = []
    missing = []
    for record in generations:
        key = (str(record["prompt_id"]), str(record["arm"]))
        label = labels.get(key)
        if label is None:
            missing.append(key)
            continue
        compliance = _compliance_record(record, dialect_validator, structured_checker)
        success = label.success_flags()
        metadata = dict(record.get("metadata", {}))
        metadata["compliance"] = compliance
        metadata["success_label"] = label.to_metadata()
        results.append(
            {
                "run_id": record["run_id"],
                "prompt_id": record["prompt_id"],
                "arm": record["arm"],
                "model_id": record["model_id"],
                "tokenizer_id": record["tokenizer_id"],
                "response": record["response"],
                "metrics": record["metrics"],
                "success": success,
                "metadata": metadata,
            }
        )

    if missing:
        print(f"Missing success labels for {len(missing)} generation records.", file=sys.stderr)
        for prompt_id, arm in missing[:20]:
            print(f"- {prompt_id} / {arm}", file=sys.stderr)
        return 2

    _write_jsonl(args.output, results)
    print(f"Wrote {len(results)} result records to {args.output}")
    return 0


def _load_jsonl(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"Line {line_no}: expected JSON object")
            records.append(payload)
    return records


def _compliance_record(
    record: dict[str, object],
    dialect_validator: DialectValidator,
    structured_checker: StructuredSimpleChecker,
) -> dict[str, object]:
    response = str(record.get("response", ""))
    arm = str(record.get("arm", ""))
    if arm == "StructuredSimple-English":
        result = structured_checker.validate(response)
        return {
            "prompt_id": record.get("prompt_id"),
            "arm": arm,
            "target": "structured_simple",
            "passed": result.passed,
            "details": result.to_dict(),
        }
    if arm == "StyleOnly-Newspeak":
        return {
            "prompt_id": record.get("prompt_id"),
            "arm": arm,
            "target": "style_only_not_dialect_compliance",
            "passed": None,
            "details": {},
        }
    if "Newspeak" in arm or arm in {"InputOutput-Newspeak", "VisibleReasoning-Newspeak"}:
        result = dialect_validator.validate(response)
        return {
            "prompt_id": record.get("prompt_id"),
            "arm": arm,
            "target": "dialect",
            "passed": result.passed,
            "details": result.to_dict(),
        }
    return {
        "prompt_id": record.get("prompt_id"),
        "arm": arm,
        "target": "none",
        "passed": None,
        "details": {},
    }


def _write_jsonl(path: Path, records: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
