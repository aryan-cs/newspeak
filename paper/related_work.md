# Related Work Notes

This file records citation targets before manuscript prose is written.

## Controlled Natural Languages

- Kuhn's controlled natural language survey anchors the classic CNL taxonomy.
- ASD-STE100 and Attempto Controlled English are relevant comparators but are not
  used as core baselines because their goals differ from tokenizer-aware
  productive compression.
- Basic English is context only; it is explicitly rejected as the core comparator.

## Text Simplification and Controllable Simplification

- Nisioi et al. provide an early neural text simplification anchor.
- ACCESS and CROSS provide controllable simplification references.
- Iterative edit-based simplification and explicit paraphrasing work bridge
  classic simplification and current LLM control.

## Tokenization and Compression

The paper should distinguish human-visible brevity from model-token savings and
report model tokens, bytes, characters, and words.

## Safety and Alignment Transfer

- Multilingual safety-transfer work motivates distribution-shift risk.
- *When Style Breaks Safety* motivates the `StyleOnly-Newspeak` core arm.
- Fine-tuning drift work motivates English safety regression after adaptation.

## Open TODOs

- Verify final venue/citation metadata for *When Style Breaks Safety* before submission.
- Add BibTeX entries for all anchors once final citation keys are chosen.
