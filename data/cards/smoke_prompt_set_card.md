# Smoke Prompt Set Card

Status: planned, not yet authored.

Purpose: 50 to 100 prompt smoke test for infrastructure checks, variance estimates,
and obvious failure detection before the 200+ prompt gate set.

Holdout policy: prompts are evaluation-only and excluded from SFT, repair,
synthetic-data, translation-example, and few-shot pools.

Required checks before use:

- Validate records with `scripts/validate_prompt_set.py`.
- Summarize coverage with `scripts/summarize_prompt_set.py`.
- Screen against all training candidates and few-shot examples with
  `scripts/check_contamination.py --config configs/evals/dedup.yaml`.
- Add checksum and contamination report path to `MANIFEST.md`.
