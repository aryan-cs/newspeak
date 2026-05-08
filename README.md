# Newspeak LLM Research

This repository contains the protocol, tooling, and paper artifacts for a study of
whether a tokenizer-aware, Newspeak-inspired controlled dialect can reduce model
tokens while preserving capability and safety alignment.

The first paper is scoped around one falsifiable claim: success-conditioned token
savings must beat concise English while remaining non-inferior on capability and
safety. If concise English matches or beats the dialect, that null result is a
valid outcome.

## Current Status

Implementation is in Milestone 0/1:

- Project scaffold and reproducibility files.
- Dialect and `StructuredSimple-English` specifications.
- Initial validator and structured-simple checker.
- Tokenizer-audit scaffolding.
- Prompt-set validation, summarization, and contamination-check scaffolding.
- Manifest-entry generation for reproducibility logging.
- Paper skeleton and related-work notes.

No model evaluations, benchmark scores, or paper results have been run yet.

## Non-Goals

- Do not copy or publish a vocabulary table from *Nineteen Eighty-Four*.
- Do not treat synthetic/model-generated data as benchmark-independent ground truth.
- Do not report raw token savings without success-conditioned correctness and safety.
- Do not call validator-guided decoding `Hard-Constrained` unless it uses a token-level
  or finite-state legality mechanism with zero false accepts on the compliance gold set
  plus manual audit.

## Repository Map

- `PLAN.md`: research protocol and paper plan.
- `dialect/`: dialect specs, rule schemas, original lexicon seeds, examples.
- `src/newspeak/`: implementation package.
- `scripts/`: CLI entry points for validation, tokenizer audits, generation, eval, analysis.
- `configs/`: model, eval, and training config stubs.
- `schemas/`: result and artifact schemas.
- `data/`: data cards, validator-gold-set location, and non-tracked data areas.
- `results/`: generated outputs and analyses, ignored by default.
- `paper/`: paper outline, related work, references, and section drafts.

## Development

The code is Python-first and currently uses only the standard library for the core
validators. Optional tokenizer backends can be installed later through the
`tokenizers` extra.

```bash
python3 -m compileall src scripts
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 scripts/check_protocol_consistency.py
```

Useful protocol checks:

```bash
PYTHONPATH=src python3 scripts/validate_prompt_set.py data/eval_sets/gate/prompts.jsonl
PYTHONPATH=src python3 scripts/summarize_prompt_set.py data/eval_sets/gate/prompts.jsonl
PYTHONPATH=src python3 scripts/check_contamination.py --config configs/evals/dedup.yaml left.jsonl right.jsonl
PYTHONPATH=src python3 scripts/create_manifest_entry.py --entry-id scaffold --status scaffold PLAN.md README.md
```

Generation pipeline:

```bash
# Mac-safe: writes request records only, with no model outputs.
PYTHONPATH=src python3 scripts/run_generation.py \
  --backend prepare \
  --prompt-set data/eval_sets/gate/prompts.jsonl \
  --arm Base-English \
  --run-id gate-prep \
  --model-id MODEL_ID \
  --output data/interim/gate-prep.requests.jsonl

# Heavy inference is guarded to run only inside /home/aryang9/sandbox/newspeak.
PYTHONPATH=src python3 scripts/run_generation.py \
  --backend transformers \
  --prompt-set data/eval_sets/gate/prompts.jsonl \
  --arm Base-English \
  --run-id gate-h200 \
  --model-id MODEL_ID \
  --output results/pilots/gate-h200.generations.jsonl \
  --resume

# Compliance reports do not create success labels.
PYTHONPATH=src python3 scripts/run_eval.py \
  --mode compliance \
  --generations results/pilots/gate-h200.generations.jsonl \
  --output results/pilots/gate-h200.compliance.jsonl
```

## Data and Results Policy

Generated data, model outputs, checkpoints, and result files are ignored unless
they are small, licensed, reviewed, and explicitly intended for publication.
Every public result must have a corresponding `MANIFEST.md` entry with model,
tokenizer, dataset, prompt, config, result, and commit metadata.
