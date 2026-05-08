# StructuredSimple-English Comparator Specification

Status: draft for Milestone 1. Freeze before Milestone 2.

## Purpose

`StructuredSimple-English` controls for structured language constraint without
Newspeak-inspired semantic compression or tokenizer-aware vocabulary choices.

It should share the dialect's sentence-shape and technical passthrough structure
while remaining plain English.

## Rules

- Use short plain-English sentences.
- Starting target: 20 words or fewer per sentence.
- Use one main idea per sentence.
- Use ordinary plain-English vocabulary.
- Do not use tokenizer-aware synonym substitution.
- Do not use compressed coinages.
- Do not enforce a closed lexicon.
- Preserve technical terms, code, math notation, proper nouns, citations, URLs,
  and numeric expressions.
- Use the same safety, refusal, ambiguity, and uncertainty vocabulary as the
  dialect where appropriate.
- Productive negation and degree morphology are permitted only when idiomatic
  plain English or explicitly shared with the dialect rules.

## Checker Scope

The lightweight checker measures:

- Sentence length.
- Obvious multi-idea sentence patterns.
- Code/math/proper-noun passthrough handling.
- Disallowed compressed coinage markers.

It is a diagnostic checker, not a training-data gate.

## Why Not Basic English

Basic English was designed for human learnability and reading comprehension. Its
operator-verb paraphrase strategy tests a different theory from productive
morphological compression. It remains related-work context only.
