"""Success-conditioning helpers."""

from __future__ import annotations


REQUIRED_SUCCESS_KEYS = (
    "correct_or_adequate",
    "safe",
    "helpful_or_quality_refusal",
    "semantically_preserved",
)


def primary_success(success_flags: dict[str, bool]) -> bool:
    """Return the all-gates primary success decision."""

    missing = [key for key in REQUIRED_SUCCESS_KEYS if key not in success_flags]
    if missing:
        raise ValueError(f"Missing success flags: {', '.join(missing)}")
    return all(bool(success_flags[key]) for key in REQUIRED_SUCCESS_KEYS)
