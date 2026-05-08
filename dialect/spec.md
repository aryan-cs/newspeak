# Newspeak-Inspired Dialect Specification

Status: draft for Milestone 1. This is an original research dialect. It does not
copy or ship a vocabulary table from *Nineteen Eighty-Four*.

## Purpose

The dialect is designed to test whether structured semantic compression can
reduce model tokens while preserving correctness, helpfulness, and safety.

It is not a closed lexicon for the main experiment. It is a productive controlled
dialect with explicit morphology, technical passthrough rules, and safety
vocabulary.

## Design Principles

- Prefer a small set of reusable roots over large synonym sets.
- Prefer productive morphology for negation, degree, and evaluation.
- Preserve exact formal syntax for code, math, citations, URLs, and numbers.
- Preserve enough vocabulary for uncertainty, consent, legality, harm, and
  refusal boundaries.
- Optimize candidate terms against the primary tokenizer only after the baseline
  productive rules are defined.

## Allowed Text Classes

1. **Core roots:** task-general roots in `dialect/lexicon.yaml`.
2. **Function words:** articles, prepositions, auxiliaries, and connectors needed
   for grammatical English.
3. **Safety terms:** refusal, uncertainty, legality, consent, and harm terms in
   `dialect/safety_terms.yaml`.
4. **Productive forms:** valid prefix/root/suffix combinations defined in
   `dialect/morphology.yaml`.
5. **Technical passthrough:** domain terms, code, math notation, proper nouns,
   citations, numbers, and URLs when preserving exact meaning requires them.

## Productive Morphology

The draft morphology uses transparent forms rather than fictional terms:

- Negation: `non-X`, `not X`, `un-X` when idiomatic.
- Degree: `more-X`, `most-X`, `less-X`.
- Risk/intensity: `over-X`, `under-X` where idiomatic.
- Actor/action derivation: `X-er`, `X-ing`, `X-ed` when idiomatic.

The tokenizer-aware version may later choose shorter roots or forms, but only
after the tokenizer gate is defined.

## Technical Passthrough

Technical passthrough is allowed for:

- Programming-language syntax and identifiers.
- Mathematical notation and variable names.
- Scientific, medical, legal, and policy terms that cannot be safely compressed.
- Proper nouns, citations, benchmark names, URLs, and numeric expressions.

The validator records passthrough usage so later analysis can distinguish real
compression from technical escape hatches.

## Safety Requirements

The dialect must be able to express:

- Refusal boundaries.
- Uncertainty.
- Harm risk.
- Legal/medical/financial caution.
- Consent and privacy.
- Safe alternatives.

A shorter answer is not successful if it removes the boundary or rationale that
makes a refusal safe and usable.

## Compliance Levels

- **Pass:** all lexical/morphological checks pass, and technical passthrough is
  justified by allowed categories.
- **Soft violation:** understandable but uses unauthorized synonyms or avoidable
  non-dialect words.
- **Hard violation:** changes meaning, hides safety-critical wording, corrupts
  formal syntax, or uses copied novel-derived vocabulary.

## Validator Scope

The initial validator is a lexical and rule-structure checker. It is not a full
semantic parser. Primary compliance claims require validator evaluation against a
gold-labeled set plus human audit when needed.
