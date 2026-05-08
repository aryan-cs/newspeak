#!/usr/bin/env python3
"""Prepare or run resumable generation for validated prompt sets."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from newspeak.evals.arms import DIRECT_ARMS, build_messages, load_few_shots
from newspeak.evals.generation import (
    H200_PROJECT_ROOT,
    TransformersGenerator,
    assert_heavy_root,
    load_completed_keys,
    prepare_request_record,
    raw_generation_record,
    text_metrics,
    write_jsonl,
)
from newspeak.evals.prompt_set import load_prompt_records, validate_prompt_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt-set", required=True, type=Path)
    parser.add_argument("--arm", required=True, choices=sorted(DIRECT_ARMS))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model-id", required=True)
    parser.add_argument("--tokenizer-id", default=None)
    parser.add_argument("--revision", default=None)
    parser.add_argument("--few-shot-jsonl", default=None)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--backend", choices=["prepare", "transformers"], default="prepare")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--heavy-root", type=Path, default=H200_PROJECT_ROOT)
    args = parser.parse_args(argv)

    tokenizer_id = args.tokenizer_id or args.model_id
    records = load_prompt_records(args.prompt_set)
    validation = validate_prompt_records(records)
    if not validation.passed:
        print("Prompt set validation failed; refusing generation.", file=sys.stderr)
        for error in validation.errors:
            print(f"- {error}", file=sys.stderr)
        return 2

    few_shots = load_few_shots(args.few_shot_jsonl)
    completed = load_completed_keys(args.output) if args.resume else set()
    append = args.resume and args.output.exists()

    if args.backend == "prepare":
        prepared = []
        for record in records:
            key = (record.prompt_id, args.arm)
            if key in completed:
                continue
            messages = build_messages(args.arm, record.prompt, few_shots)
            prepared.append(
                prepare_request_record(
                    run_id=args.run_id,
                    prompt_id=record.prompt_id,
                    arm=args.arm,
                    model_id=args.model_id,
                    tokenizer_id=tokenizer_id,
                    prompt=record.prompt,
                    messages=messages,
                    metadata={
                        "prompt_source_type": record.source_type,
                        "prompt_source_ref": record.source_ref,
                        "task_category": record.task_category,
                        "safety_category": record.safety_category,
                    },
                )
            )
        write_jsonl(args.output, prepared, append=append)
        print(f"Prepared {len(prepared)} request records at {args.output}")
        return 0

    assert_heavy_root(Path.cwd(), args.heavy_root)
    generator = TransformersGenerator(
        model_id=args.model_id,
        tokenizer_id=tokenizer_id,
        revision=args.revision,
        seed=args.seed,
    )
    generated = []
    for record in records:
        key = (record.prompt_id, args.arm)
        if key in completed:
            continue
        messages = build_messages(args.arm, record.prompt, few_shots)
        response, prompt_tokens, output_tokens, latency_ms = generator.generate(
            messages,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        generated.append(
            raw_generation_record(
                run_id=args.run_id,
                prompt_id=record.prompt_id,
                arm=args.arm,
                model_id=args.model_id,
                tokenizer_id=tokenizer_id,
                prompt=record.prompt,
                messages=messages,
                response=response,
                metrics=text_metrics(
                    response,
                    prompt_tokens=prompt_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                ),
                metadata={
                    "prompt_source_type": record.source_type,
                    "prompt_source_ref": record.source_ref,
                    "task_category": record.task_category,
                    "safety_category": record.safety_category,
                    "revision": args.revision,
                    "max_new_tokens": args.max_new_tokens,
                    "temperature": args.temperature,
                    "top_p": args.top_p,
                    "seed": args.seed,
                },
            )
        )
        write_jsonl(args.output, generated[-1:], append=append or len(generated) > 1)
    print(f"Generated {len(generated)} response records at {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
