# Language Under Constraint: Capability, Efficiency, and Safety Transfer in Newspeak-Style Language Models

Status: manuscript scaffold. Results are not yet run.

## Abstract

This paper will evaluate whether a tokenizer-aware productive controlled dialect
can reduce model-token usage while preserving capability and safety. The primary
comparison is against concise English, and all token savings are conditioned on
responses remaining correct, safe, helpful, and semantically preserved. This
draft intentionally contains no empirical claims until the gate and main
experiments are complete.

## 1. Introduction

Language models often spend many tokens on natural-language redundancy,
qualification, and style. A compressed controlled dialect may reduce generation
cost, but shorter output is only useful if the response remains correct, safe,
and adequate. This project studies that tradeoff with a Newspeak-inspired but
original productive dialect.

The core claim is falsifiable: if ordinary concise-English prompting achieves
the same success-conditioned token savings, the paper reports that structured
artificial dialects do not improve efficient utility beyond brevity prompting
under this protocol.

## 2. Related Work

The study connects controlled natural languages, controllable simplification,
tokenization research, style-as-jailbreak findings, multilingual safety transfer,
and fine-tuning alignment drift. Detailed notes and citation anchors are in
`paper/related_work.md` and `paper/references.bib`.

## 3. Dialect and Comparator Design

The dialect is an original productive controlled dialect with restricted roots,
productive morphology, technical passthrough, and explicit safety vocabulary.
`StructuredSimple-English` controls for sentence-shape and morphology constraints
without tokenizer-aware compression. `StyleOnly-Newspeak` controls for superficial
style shift.

## 4. Experimental Setup

The first implementation phase builds the validators, tokenizer audit, prompt
cards, manifest entries, and schema files required before any model evaluation.
The first gate will use at least 200 prompts and retain at least 120 successful
paired items after success-conditioning.

## 5. Metrics

Primary metric: success-conditioned token savings for `TokenizerAware-Newspeak`
versus `Base-Concise`, with `Base-English` as the absolute baseline.

Safety and capability are evaluated through predeclared non-inferiority margins.
Dialect compliance and semantic preservation are measured separately.

## 6. Results

Not yet run. This section must remain empty of findings until the relevant
manifest entries, generated outputs, and analyses exist.

## 7. Qualitative Analysis

Not yet run. Planned cases include compression successes, concise-English wins,
style-only safety failures, safety-vocabulary collapse, and technical passthrough.

## 8. Limitations

The first paper is primary-tokenizer optimized. Cross-tokenizer results are
diagnostic unless later work redesigns the dialect for tokenizer-family
agnosticism. The validator is not a semantic parser. Back-translation can mask
dialect-specific failures and is diagnostic only.

## 9. Ethics and Safety

The project uses *Nineteen Eighty-Four* only as conceptual motivation. It does
not copy substantial text, ship extracted vocabulary tables, or create
novel-derived training data. Harmful prompts and generations require controlled
handling and should not be published unless necessary and licensed.

## 10. Conclusion

To be completed after the main experiment.
