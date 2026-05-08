"""Lightweight contamination and near-duplicate checks."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class TextRecord:
    id: str
    text: str


@dataclass(frozen=True)
class OverlapFinding:
    left_id: str
    right_id: str
    kind: str
    score: float

    def to_dict(self) -> dict[str, object]:
        return {
            "left_id": self.left_id,
            "right_id": self.right_id,
            "kind": self.kind,
            "score": self.score,
        }


def normalize_text(text: str) -> str:
    return " ".join(TOKEN_RE.findall(text.lower()))


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def token_ngrams(text: str, n: int = 5) -> set[tuple[str, ...]]:
    tokens = TOKEN_RE.findall(text.lower())
    if len(tokens) < n:
        return {tuple(tokens)} if tokens else set()
    return {tuple(tokens[index : index + n]) for index in range(len(tokens) - n + 1)}


def jaccard(left: set[tuple[str, ...]], right: set[tuple[str, ...]]) -> float:
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def find_overlaps(
    left_records: Iterable[TextRecord],
    right_records: Iterable[TextRecord],
    ngram_size: int = 5,
    ngram_threshold: float = 0.8,
) -> list[OverlapFinding]:
    right_list = list(right_records)
    right_hashes = {record.id: sha256_text(record.text) for record in right_list}
    right_ngrams = {record.id: token_ngrams(record.text, ngram_size) for record in right_list}

    findings: list[OverlapFinding] = []
    for left in left_records:
        left_hash = sha256_text(left.text)
        left_ngrams = token_ngrams(left.text, ngram_size)
        for right in right_list:
            if left_hash == right_hashes[right.id]:
                findings.append(OverlapFinding(left.id, right.id, "exact_hash", 1.0))
                continue
            score = jaccard(left_ngrams, right_ngrams[right.id])
            if score >= ngram_threshold:
                findings.append(OverlapFinding(left.id, right.id, "ngram_jaccard", score))
    return findings


def load_jsonl_text_records(path: Path, text_field: str = "prompt", id_field: str = "prompt_id") -> list[TextRecord]:
    records: list[TextRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            record_id = str(payload.get(id_field, f"{path.name}:{line_no}"))
            text = payload.get(text_field)
            if not isinstance(text, str):
                raise ValueError(f"Missing text field {text_field!r} on line {line_no}")
            records.append(TextRecord(record_id, text))
    return records
