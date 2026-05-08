# Methods Draft

Status: skeleton. Do not add results until experiments are run.

## Dialect

The dialect is an original productive controlled dialect inspired by Newspeak-like
mechanisms. It uses a restricted seed lexicon, productive morphology, technical
passthrough rules, and explicit safety/refusal vocabulary.

## Comparator

`StructuredSimple-English` uses short plain-English sentences, one idea per
sentence, technical passthrough, and the same morphology slots where idiomatic.
It does not use tokenizer-aware compression or compressed coinages.

## Core Arms

- `Base-English`
- `Base-Concise`
- `StructuredSimple-English`
- `Prompt-Newspeak`
- `ICL-Newspeak`
- `TokenizerAware-Newspeak`
- `StyleOnly-Newspeak`

## Primary Metric

Success-conditioned token savings are computed on paired prompts where both the
candidate and comparator satisfy all gates: correctness/task adequacy, safety,
minimum helpfulness/refusal quality, and semantic preservation.

## Gate

The generated-response gate uses at least 200 prompts and requires at least 120
successful paired items after success-conditioning.
