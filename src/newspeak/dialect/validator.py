"""Rule-based validator for the Newspeak-inspired productive dialect."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import Iterable

from .config import DIALECT_DIR, flatten_values, load_mapping


WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*|https?://\S+|\d+(?:\.\d+)?")
CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


@dataclass(frozen=True)
class Violation:
    """One validator finding."""

    token: str
    violation_type: str
    message: str


@dataclass
class ValidationResult:
    """Validation output with enough detail for audits and tests."""

    passed: bool
    violations: list[Violation] = field(default_factory=list)
    checked_tokens: int = 0
    passthrough_tokens: int = 0

    def to_dict(self) -> dict[str, object]:
        return {
            "passed": self.passed,
            "checked_tokens": self.checked_tokens,
            "passthrough_tokens": self.passthrough_tokens,
            "violations": [violation.__dict__ for violation in self.violations],
        }


@dataclass(frozen=True)
class DialectRules:
    """Compiled rule sets for dialect validation."""

    allowed_terms: frozenset[str]
    technical_allowlist: frozenset[str]
    forbidden_terms: frozenset[str]
    prefixes: frozenset[str]
    suffixes: frozenset[str]


class DialectValidator:
    """Validate lexical and productive-morphology compliance.

    The validator is intentionally conservative. It is suitable for screening and
    unit tests, but PLAN.md still requires a gold-set evaluation before using it
    for primary compliance claims.
    """

    def __init__(self, rules: DialectRules):
        self.rules = rules

    @classmethod
    def from_dialect_dir(cls, dialect_dir: Path = DIALECT_DIR) -> "DialectValidator":
        lexicon = load_mapping(dialect_dir / "lexicon.yaml")
        morphology = load_mapping(dialect_dir / "morphology.yaml")
        safety = load_mapping(dialect_dir / "safety_terms.yaml")

        allowed = set()
        allowed.update(flatten_values(lexicon.get("function_words", [])))
        allowed.update(flatten_values(lexicon.get("roots", {})))
        allowed.update(flatten_values(safety))
        technical = flatten_values(lexicon.get("technical_allowlist", []))
        forbidden = flatten_values(lexicon.get("forbidden_source_terms", []))

        prefixes = frozenset(str(key).lower() for key in morphology.get("prefixes", {}).keys())
        suffixes = frozenset(str(key).lower() for key in morphology.get("suffixes", {}).keys())

        return cls(
            DialectRules(
                allowed_terms=frozenset(allowed),
                technical_allowlist=frozenset(technical),
                forbidden_terms=frozenset(forbidden),
                prefixes=prefixes,
                suffixes=suffixes,
            )
        )

    def validate(self, text: str) -> ValidationResult:
        scrubbed = self._remove_code(text)
        violations: list[Violation] = []
        checked = 0
        passthrough = 0

        for token in self._tokens(scrubbed):
            if self._is_passthrough(token):
                passthrough += 1
                continue

            checked += 1
            lowered = token.lower()

            if lowered in self.rules.forbidden_terms:
                violations.append(
                    Violation(
                        token=token,
                        violation_type="forbidden_source_term",
                        message="Term is forbidden for project assets.",
                    )
                )
                continue

            if self._is_allowed(lowered):
                continue

            violations.append(
                Violation(
                    token=token,
                    violation_type="lexicon",
                    message="Token is not allowed by lexicon, morphology, or passthrough rules.",
                )
            )

        return ValidationResult(
            passed=not violations,
            violations=violations,
            checked_tokens=checked,
            passthrough_tokens=passthrough,
        )

    def _is_allowed(self, lowered: str) -> bool:
        if lowered in self.rules.allowed_terms:
            return True
        if self._is_hyphenated_productive_form(lowered):
            return True
        if self._has_allowed_suffix(lowered):
            return True
        return False

    def _is_hyphenated_productive_form(self, lowered: str) -> bool:
        if "-" not in lowered:
            return False
        prefix, _, root = lowered.partition("-")
        return prefix in self.rules.prefixes and self._is_allowed(root)

    def _has_allowed_suffix(self, lowered: str) -> bool:
        for suffix in self.rules.suffixes:
            if lowered.endswith(suffix) and len(lowered) > len(suffix) + 1:
                stem = lowered[: -len(suffix)]
                if stem in self.rules.allowed_terms:
                    return True
        return False

    def _is_passthrough(self, token: str) -> bool:
        lowered = token.lower()
        if lowered in self.rules.technical_allowlist:
            return True
        if token.startswith("http://") or token.startswith("https://"):
            return True
        if token.replace(".", "", 1).isdigit():
            return True
        if token.isupper() and len(token) > 1:
            return True
        if "_" in token:
            return True
        if token[:1].isupper() and len(token) > 1:
            return True
        return False

    @staticmethod
    def _remove_code(text: str) -> str:
        without_fences = CODE_FENCE_RE.sub(" ", text)
        return INLINE_CODE_RE.sub(" ", without_fences)

    @staticmethod
    def _tokens(text: str) -> Iterable[str]:
        return (match.group(0) for match in WORD_RE.finditer(text))
