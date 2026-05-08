"""Lightweight checker for the StructuredSimple-English comparator."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


SENTENCE_RE = re.compile(r"[^.!?\n]+[.!?]?")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*|\d+(?:\.\d+)?")
COMPRESSED_MARKERS = ("plusgood", "doubleplus", "goodthink", "oldspeak", "thoughtcrime")


@dataclass(frozen=True)
class StructuredViolation:
    violation_type: str
    message: str
    span: str


@dataclass
class StructuredResult:
    passed: bool
    violations: list[StructuredViolation] = field(default_factory=list)
    sentence_count: int = 0
    word_count: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "sentence_count": self.sentence_count,
            "word_count": self.word_count,
            "violations": [violation.__dict__ for violation in self.violations],
        }


class StructuredSimpleChecker:
    """Check the comparator's sentence-shape constraints."""

    def __init__(self, max_sentence_words: int = 20, max_conjunctions: int = 1):
        self.max_sentence_words = max_sentence_words
        self.max_conjunctions = max_conjunctions

    def validate(self, text: str) -> StructuredResult:
        violations: list[StructuredViolation] = []
        sentences = [sentence.strip() for sentence in SENTENCE_RE.findall(text) if sentence.strip()]
        total_words = 0

        for sentence in sentences:
            words = WORD_RE.findall(sentence)
            total_words += len(words)

            if len(words) > self.max_sentence_words:
                violations.append(
                    StructuredViolation(
                        violation_type="sentence_length",
                        message=f"Sentence has {len(words)} words; limit is {self.max_sentence_words}.",
                        span=sentence,
                    )
                )

            conjunctions = len(re.findall(r"\b(and|but|or|while|although|because)\b", sentence, re.I))
            if conjunctions > self.max_conjunctions:
                violations.append(
                    StructuredViolation(
                        violation_type="multi_idea",
                        message="Sentence likely contains more than one main idea.",
                        span=sentence,
                    )
                )

            lowered = sentence.lower()
            for marker in COMPRESSED_MARKERS:
                if marker in lowered:
                    violations.append(
                        StructuredViolation(
                            violation_type="compressed_marker",
                            message="StructuredSimple-English must not use Newspeak-style coinages.",
                            span=marker,
                        )
                    )

        return StructuredResult(
            passed=not violations,
            violations=violations,
            sentence_count=len(sentences),
            word_count=total_words,
        )
