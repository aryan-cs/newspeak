#!/usr/bin/env python3
"""Create compliance reports or schema-ready results from raw generations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from newspeak.dialect.structured_simple import StructuredSimpleChecker
from newspeak.dialect.validator import DialectValidator
from newspeak.evals.success import REQUIRED_SUCCESS_KEYS, primary_success


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

    labels = _load_success_labels(args.success_labels)
    results = []
    missing = []
    for record in generations:
        key = (str(record["prompt_id"]), str(record["arm"]))
        label = labels.get(key)
        if label is None:
            missing.append(key)
            continue
        compliance = _compliance_record(record, dialect_validator, structured_checker)
        success = {flag: bool(label[flag]) for flag in REQUIRED_SUCCESS_KEYS}
        success["primary_success"] = primary_success(success)
        metadata = dict(record.get("metadata", {}))
        metadata["compliance"] = compliance
        if "notes" in label:
            metadata["success_label_notes"] = label["notes"]
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


def _load_success_labels(path: Path) -> dict[tuple[str, str], dict[str, object]]:
    labels: dict[tuple[str, str], dict[str, object]] = {}
    for line_no, payload in enumerate(_load_jsonl(path), start=1):
        missing = [field for field in ("prompt_id", "arm", *REQUIRED_SUCCESS_KEYS) if field not in payload]
        if missing:
            raise ValueError(f"Line {line_no}: missing success-label fields: {', '.join(missing)}")
        key = (str(payload["prompt_id"]), str(payload["arm"]))
        if key in labels:
            raise ValueError(f"Line {line_no}: duplicate success label for {key[0]} / {key[1]}")
        labels[key] = payload
    return labels


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
