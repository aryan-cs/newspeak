# Paper Outline

Working title: **Language Under Constraint: Capability, Efficiency, and Safety
Transfer in Newspeak-Style Language Models**

## Abstract

State the intervention, core controls, success-conditioned token metric, and
whether the dialect beats concise English under capability/safety constraints.
Do not add result claims until the main experiment is complete.

## 1. Introduction

- Motivation: token efficiency, controlled language, safety transfer.
- Problem: raw brevity can hide capability and safety loss.
- Contribution: tokenizer-aware productive dialect, `StructuredSimple-English`
  and `StyleOnly-Newspeak` controls, success-conditioned evaluation protocol.

## 2. Related Work

- Controlled natural languages and technical language.
- Controllable simplification and lexical simplification.
- Tokenization and prompt compression.
- Style as a jailbreak vector.
- Multilingual safety transfer.
- Fine-tuning alignment drift.

## 3. Dialect Design

- Original Newspeak-inspired dialect principles.
- Productive morphology and technical passthrough.
- Safety vocabulary requirements.
- `StructuredSimple-English` comparator.
- Validator and checker design.

## 4. Experimental Setup

- Model family and tokenizer selection.
- Core arms: `Base-English`, `Base-Concise`, `StructuredSimple-English`,
  `Prompt-Newspeak`, `ICL-Newspeak`, `TokenizerAware-Newspeak`,
  `StyleOnly-Newspeak`.
- Smoke and gate prompt sets.
- Benchmarks and custom safety diagnostics.

## 5. Metrics

- Success-conditioned token savings.
- Capability non-inferiority.
- Safety non-inferiority.
- Dialect compliance.
- Semantic preservation.
- Latency as secondary metric under fixed infrastructure.

## 6. Results

Status: not yet run.

Planned tables:

- Tokenizer audit by vocabulary category.
- Gate set token savings by arm.
- Success rates by arm.
- Capability and safety deltas.
- Safety mechanism diagnostics.

## 7. Qualitative Analysis

Status: not yet run.

Planned examples:

- Compression success.
- Concise-English win/null-result case.
- Safety-vocabulary collapse.
- Style-only degradation.
- Technical passthrough case.

## 8. Limitations

- Primary-tokenizer scope.
- Artificial dialect generality.
- Validator scope.
- Human-rater comprehension.
- Compute limits.
- Latent reasoning unobservability.

## 9. Ethics and Safety

- Copyright handling for *Nineteen Eighty-Four*.
- Harmful prompt handling.
- Human rater protections.
- Non-publication of unnecessary harmful generations.

## 10. Conclusion

Summarize whether tokenizer-aware structured dialect design produces efficient
utility beyond concise English while preserving safety.
