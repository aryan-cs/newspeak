# Gate Prompt Set

Status: not yet authored.

The gate set must contain at least 200 evaluation-only prompts and retain at
least 120 successful paired items after success-conditioning.

Required file when authored:

- `prompts.jsonl`

Each record must satisfy `schemas/prompt_set.schema.json`.
Validate before use:

```bash
PYTHONPATH=src python3 scripts/validate_prompt_set.py data/eval_sets/gate/prompts.jsonl
PYTHONPATH=src python3 scripts/summarize_prompt_set.py data/eval_sets/gate/prompts.jsonl
```
