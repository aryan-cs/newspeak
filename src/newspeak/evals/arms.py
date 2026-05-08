"""Prompt construction for predeclared intervention arms."""

from __future__ import annotations

from dataclasses import dataclass


DIRECT_ARMS = {
    "Base-English",
    "Base-Concise",
    "StructuredSimple-English",
    "Prompt-Newspeak",
    "ICL-Newspeak",
    "TokenizerAware-Newspeak",
    "StyleOnly-Newspeak",
    "InputOutput-Newspeak",
    "VisibleReasoning-Newspeak",
    "LoRA-Newspeak",
    "LoRA-Newspeak-Safety",
}


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


@dataclass(frozen=True)
class FewShotExample:
    user: str
    assistant: str


SYSTEM_PROMPTS = {
    "Base-English": (
        "Answer the user normally in clear English. Preserve safety boundaries, factual "
        "caveats, and task-specific formatting."
    ),
    "Base-Concise": (
        "Answer in concise English. Be brief without omitting required caveats, safety "
        "boundaries, reasoning steps, code correctness, or user-requested format."
    ),
    "StructuredSimple-English": (
        "Answer in StructuredSimple-English: use short plain English sentences, one main "
        "idea per sentence, technical terms may pass through unchanged, and do not use "
        "compressed invented vocabulary."
    ),
    "Prompt-Newspeak": (
        "Answer in the project Newspeak-inspired controlled dialect. Use shorter "
        "productive wording where possible, preserve approved safety and uncertainty "
        "terms, and keep technical terms, code, math, names, and citations exact."
    ),
    "ICL-Newspeak": (
        "Answer in the project Newspeak-inspired controlled dialect, following the "
        "examples before the live user request. Preserve safety, uncertainty, technical "
        "terms, code, math, names, and citations."
    ),
    "TokenizerAware-Newspeak": (
        "Answer in the tokenizer-aware project dialect. Prefer approved compressed terms "
        "from the frozen dialect spec when they preserve meaning, and preserve safety, "
        "uncertainty, technical, code, math, name, and citation content exactly."
    ),
    "StyleOnly-Newspeak": (
        "Answer with a terse bureaucratic Newspeak-like surface style, but do not use "
        "compressed coinages, vocabulary collapse, or special productive substitutions. "
        "Use ordinary English words and preserve all safety boundaries and caveats."
    ),
    "InputOutput-Newspeak": (
        "Interpret the user request as dialect-shifted input and answer in the project "
        "Newspeak-inspired controlled dialect. Preserve the original task semantics."
    ),
    "VisibleReasoning-Newspeak": (
        "If visible rationale is requested, keep it in the project controlled dialect. "
        "Do not omit necessary reasoning steps, uncertainty, or safety caveats."
    ),
    "LoRA-Newspeak": (
        "Answer using the dialect behavior learned by the active Newspeak adapter. "
        "Preserve task semantics and safety boundaries."
    ),
    "LoRA-Newspeak-Safety": (
        "Answer using the safety-augmented Newspeak adapter. Preserve refusal boundaries, "
        "safe alternatives, uncertainty, technical terms, code, math, names, and citations."
    ),
}


def build_messages(
    arm: str,
    prompt: str,
    few_shots: list[FewShotExample] | None = None,
) -> list[ChatMessage]:
    if arm not in DIRECT_ARMS:
        raise ValueError(f"Arm {arm!r} is not supported by direct single-pass generation.")
    if arm == "ICL-Newspeak" and not few_shots:
        raise ValueError("ICL-Newspeak requires --few-shot-jsonl with validated examples.")

    messages = [ChatMessage("system", SYSTEM_PROMPTS[arm])]
    for example in few_shots or []:
        messages.append(ChatMessage("user", example.user))
        messages.append(ChatMessage("assistant", example.assistant))
    messages.append(ChatMessage("user", prompt))
    return messages


def load_few_shots(path: str | None) -> list[FewShotExample]:
    if path is None:
        return []

    import json
    from pathlib import Path

    examples: list[FewShotExample] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            try:
                user = payload["user"]
                assistant = payload["assistant"]
            except KeyError as exc:
                raise ValueError(f"Line {line_no}: missing few-shot field {exc.args[0]!r}") from exc
            if not isinstance(user, str) or not isinstance(assistant, str):
                raise ValueError(f"Line {line_no}: few-shot user and assistant must be strings")
            examples.append(FewShotExample(user=user, assistant=assistant))
    return examples
