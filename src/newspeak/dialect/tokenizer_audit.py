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
