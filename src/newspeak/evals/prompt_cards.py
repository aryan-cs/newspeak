"""Markdown cards for validated prompt-set JSONL files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from newspeak.analysis.manifest import ArtifactDigest, artifact_digest
from newspeak.evals.prompt_set import (
    PromptRecord,
    PromptSetSummary,
    load_prompt_records,
    summarize_prompt_records,
    validate_prompt_records,
)


PURPOSE_PLACEHOLDER = "TBD: describe the evaluation purpose and intended use."
CONTAMINATION_REPORT_PLACEHOLDER = "TBD: add contamination report path before use."


@dataclass(frozen=True)
class PromptSetCard:
    title: str
    status: str
    purpose: str
    summary: PromptSetSummary
    digest: ArtifactDigest
    contamination_report_path: str

    def render_markdown(self) -> str:
        sections = [
            f"# {self.title}",
            f"Status: {self.status}.",
            f"Purpose: {self.purpose}",
            "Counts:",
            *self._count_lines(),
            "Checksum:",
            f"- Prompt file: `{self.digest.path}`",
            f"- SHA256: `{self.digest.sha256}`",
            f"- Bytes: {self.digest.bytes}",
            f"Contamination report path: {self.contamination_report_path}",
        ]
        return "\n\n".join(sections) + "\n"

    def _count_lines(self) -> list[str]:
        return [
            f"- Records: {self.summary.records}",
            f"- Split: {_format_counts(self.summary.split_roles)}",
            f"- Source: {_format_counts(self.summary.source_types)}",
            f"- Task: {_format_counts(self.summary.task_categories)}",
            f"- Safety: {_format_counts(self.summary.safety_categories)}",
            f"- Holdout: {_format_counts(self.summary.holdout)}",
        ]


def build_prompt_set_card(
    prompt_jsonl: Path,
    *,
    title: str | None = None,
    status: str = "draft",
    purpose: str = PURPOSE_PLACEHOLDER,
    contamination_report_path: str = CONTAMINATION_REPORT_PLACEHOLDER,
    root: Path | None = None,
) -> PromptSetCard:
    records = load_valid_prompt_records(prompt_jsonl)
    return PromptSetCard(
        title=title or _default_title(prompt_jsonl),
        status=status,
        purpose=purpose,
        summary=summarize_prompt_records(records),
        digest=artifact_digest(prompt_jsonl, root),
        contamination_report_path=contamination_report_path,
    )


def load_valid_prompt_records(prompt_jsonl: Path) -> list[PromptRecord]:
    records = load_prompt_records(prompt_jsonl)
    validation = validate_prompt_records(records)
    if not validation.passed:
        raise ValueError("prompt set validation failed: " + "; ".join(validation.errors))
    return records


def render_prompt_set_card(
    prompt_jsonl: Path,
    *,
    title: str | None = None,
    status: str = "draft",
    purpose: str = PURPOSE_PLACEHOLDER,
    contamination_report_path: str = CONTAMINATION_REPORT_PLACEHOLDER,
    root: Path | None = None,
) -> str:
    return build_prompt_set_card(
        prompt_jsonl,
        title=title,
        status=status,
        purpose=purpose,
        contamination_report_path=contamination_report_path,
        root=root,
    ).render_markdown()


def _format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{name}={count}" for name, count in counts.items())


def _default_title(prompt_jsonl: Path) -> str:
    stem = prompt_jsonl.stem.replace("_", " ").replace("-", " ").strip()
    if not stem:
        return "Prompt Set Card"
    return f"{stem.title()} Prompt Set Card"
