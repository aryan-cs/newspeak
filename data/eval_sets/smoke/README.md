# Smoke Prompt Set

Status: not yet authored.

The smoke set must contain 50 to 100 evaluation-only prompts before Milestone 2
smoke testing. Do not place generated model outputs here.

Required file when authored:

- `prompts.jsonl`

Each record must satisfy `schemas/prompt_set.schema.json`.
Validate before use:

```bash
PYTHONPATH=src python3 scripts/validate_prompt_set.py data/eval_sets/smoke/prompts.jsonl
PYTHONPATH=src python3 scripts/summarize_prompt_set.py data/eval_sets/smoke/prompts.jsonl
```
