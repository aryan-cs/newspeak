"""Generation record helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import time
from typing import Iterable

from newspeak.evals.arms import ChatMessage


H200_PROJECT_ROOT = Path("/home/aryang9/sandbox/newspeak")


@dataclass(frozen=True)
class GenerationMetrics:
    prompt_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    characters: int
    bytes: int
    words: int
    latency_ms: float | None = None
    time_to_first_token_ms: float | None = None
    tokens_per_second: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "characters": self.characters,
            "bytes": self.bytes,
            "words": self.words,
            "latency_ms": self.latency_ms,
            "time_to_first_token_ms": self.time_to_first_token_ms,
            "tokens_per_second": self.tokens_per_second,
        }


def text_metrics(
    text: str,
    prompt_tokens: int | None = None,
    output_tokens: int | None = None,
    latency_ms: float | None = None,
) -> GenerationMetrics:
    total_tokens = None
    if prompt_tokens is not None and output_tokens is not None:
        total_tokens = prompt_tokens + output_tokens
    tokens_per_second = None
    if output_tokens is not None and latency_ms and latency_ms > 0:
        tokens_per_second = output_tokens / (latency_ms / 1000)
    return GenerationMetrics(
        prompt_tokens=prompt_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        characters=len(text),
        bytes=len(text.encode("utf-8")),
        words=len(text.split()),
        latency_ms=latency_ms,
        tokens_per_second=tokens_per_second,
    )


def write_jsonl(path: Path, records: Iterable[dict[str, object]], append: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with path.open(mode, encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def load_completed_keys(path: Path) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    completed: set[tuple[str, str]] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            completed.add((str(payload["prompt_id"]), str(payload["arm"])))
    return completed


def raw_generation_record(
    *,
    run_id: str,
    prompt_id: str,
    arm: str,
    model_id: str,
    tokenizer_id: str,
    prompt: str,
    messages: list[ChatMessage],
    response: str,
    metrics: GenerationMetrics,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "prompt_id": prompt_id,
        "arm": arm,
        "model_id": model_id,
        "tokenizer_id": tokenizer_id,
        "prompt": prompt,
        "messages": [message.to_dict() for message in messages],
        "response": response,
        "metrics": metrics.to_dict(),
        "metadata": metadata or {},
    }


def prepare_request_record(
    *,
    run_id: str,
    prompt_id: str,
    arm: str,
    model_id: str,
    tokenizer_id: str,
    prompt: str,
    messages: list[ChatMessage],
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "prompt_id": prompt_id,
        "arm": arm,
        "model_id": model_id,
        "tokenizer_id": tokenizer_id,
        "prompt": prompt,
        "messages": [message.to_dict() for message in messages],
        "status": "prepared_request_not_model_output",
        "metadata": metadata or {},
    }


def assert_heavy_root(current: Path, heavy_root: Path = H200_PROJECT_ROOT) -> None:
    resolved = current.resolve()
    heavy_resolved = heavy_root.resolve()
    if resolved != heavy_resolved and heavy_resolved not in resolved.parents:
        raise RuntimeError(
            "Heavy generation is only allowed inside "
            f"{heavy_resolved}. Current directory is {resolved}."
        )


class TransformersGenerator:
    def __init__(
        self,
        *,
        model_id: str,
        tokenizer_id: str,
        revision: str | None,
        seed: int | None,
    ) -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if seed is not None:
            torch.manual_seed(seed)

        tokenizer_kwargs = {"revision": revision} if revision else {}
        model_kwargs = {"revision": revision} if revision else {}
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, **tokenizer_kwargs)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype="auto",
            **model_kwargs,
        )

    def generate(
        self,
        messages: list[ChatMessage],
        *,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
    ) -> tuple[str, int, int, float]:
        chat = [message.to_dict() for message in messages]
        input_ids = self.tokenizer.apply_chat_template(
            chat,
            add_generation_prompt=True,
            return_tensors="pt",
        ).to(self.model.device)
        prompt_tokens = int(input_ids.shape[-1])

        started = time.perf_counter()
        generated = self.model.generate(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0,
            temperature=temperature if temperature > 0 else None,
            top_p=top_p,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        elapsed_ms = (time.perf_counter() - started) * 1000
        response_ids = generated[0][prompt_tokens:]
        output_tokens = int(response_ids.shape[-1])
        response = self.tokenizer.decode(response_ids, skip_special_tokens=True).strip()
        return response, prompt_tokens, output_tokens, elapsed_ms
