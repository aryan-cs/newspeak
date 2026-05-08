"""Tokenizer audit utilities for dialect terms and paraphrases."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Protocol

from .config import load_mapping


class TokenizerLike(Protocol):
    name: str

    def count(self, text: str) -> int:
        ...


@dataclass(frozen=True)
class WhitespaceTokenizer:
    """Deterministic fallback tokenizer for tests and smoke checks.

    This is not a model-tokenizer substitute for reported results.
    """

    name: str = "whitespace"

    def count(self, text: str) -> int:
        return len(text.split())


class HuggingFaceTokenizer:
    def __init__(self, tokenizer_id: str, revision: str | None = None) -> None:
        from transformers import AutoTokenizer

        kwargs = {"revision": revision} if revision else {}
        self.tokenizer_id = tokenizer_id
        self.revision = revision
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, **kwargs)
        self.name = f"hf:{tokenizer_id}" if revision is None else f"hf:{tokenizer_id}@{revision}"

    def count(self, text: str) -> int:
        return len(self.tokenizer.encode(text, add_special_tokens=False))


class TiktokenTokenizer:
    def __init__(self, encoding_or_model: str) -> None:
        import tiktoken

        self.encoding_or_model = encoding_or_model
        try:
            self.encoding = tiktoken.encoding_for_model(encoding_or_model)
            prefix = "tiktoken_model"
        except KeyError:
            self.encoding = tiktoken.get_encoding(encoding_or_model)
            prefix = "tiktoken"
        self.name = f"{prefix}:{encoding_or_model}"

    def count(self, text: str) -> int:
        return len(self.encoding.encode(text))


@dataclass(frozen=True)
class AuditRow:
    term: str
    paraphrase: str | None
    counts: dict[str, int]
    paraphrase_counts: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "term": self.term,
            "paraphrase": self.paraphrase,
            "counts": self.counts,
            "paraphrase_counts": self.paraphrase_counts,
        }


def audit_terms(
    terms: list[str],
    tokenizers: list[TokenizerLike],
    paraphrases: dict[str, str] | None = None,
) -> list[AuditRow]:
    """Count each term and optional paraphrase under each tokenizer."""

    paraphrases = paraphrases or {}
    rows: list[AuditRow] = []
    for term in terms:
        paraphrase = paraphrases.get(term)
        rows.append(
            AuditRow(
                term=term,
                paraphrase=paraphrase,
                counts={tokenizer.name: tokenizer.count(term) for tokenizer in tokenizers},
                paraphrase_counts=(
                    {tokenizer.name: tokenizer.count(paraphrase) for tokenizer in tokenizers}
                    if paraphrase
                    else {}
                ),
            )
        )
    return rows


def tokenizer_from_spec(spec: str) -> TokenizerLike:
    if spec == "whitespace":
        return WhitespaceTokenizer()
    if spec.startswith("hf:"):
        body = spec.removeprefix("hf:")
        tokenizer_id, _, revision = body.partition("@")
        return HuggingFaceTokenizer(tokenizer_id=tokenizer_id, revision=revision or None)
    if spec.startswith("tiktoken:"):
        return TiktokenTokenizer(spec.removeprefix("tiktoken:"))
    raise ValueError(
        "Unknown tokenizer spec. Use 'whitespace', 'hf:ORG/MODEL[@REVISION]', "
        "or 'tiktoken:ENCODING_OR_MODEL'."
    )


def load_terms_from_lexicon(path: Path) -> list[str]:
    """Load candidate terms from a lexicon file."""

    mapping = load_mapping(path)
    roots = mapping.get("roots", {})
    terms: list[str] = []
    if isinstance(roots, dict):
        for values in roots.values():
            if isinstance(values, list):
                terms.extend(str(value) for value in values)
    return sorted(set(terms))


def write_jsonl(rows: list[AuditRow], path: Path) -> None:
    """Write audit rows as JSONL."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row.to_dict(), sort_keys=True) + "\n")
