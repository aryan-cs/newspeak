# Reproducibility Manifest

This manifest records the artifacts needed to reproduce reportable claims.
A run is not reproducible until its manifest entry is complete.

## Update Cadence

Update this file after every milestone that produces reportable artifacts and
before any public result, paper draft, model release, or data release.

## Required Fields Per Run

- Model IDs, revisions, hashes, and licenses.
- Tokenizer versions and checksums.
- Dataset names, versions, splits, licenses, and checksums.
- Prompt-set IDs and checksums.
- Dialect spec version and validator version.
- `StructuredSimple-English` spec version and rule-checker version.
- Validator gold-set version and validator evaluation results.
- Dependency lockfile hash.
- Benchmark, evaluator, and judge versions.
- Human-evaluation rubric version and annotation batch IDs.
- Inference config, seeds, sampling parameters, and max-token settings.
- Hardware, backend, quantization, batch size, and latency-measurement settings.
- Contamination and deduplication report paths.
- Result file paths and checksums.
- Raw generation file paths and checksums.
- Success-label file paths and annotation batch IDs.
- Per-artifact relative paths and checksums.
- Repository commit SHA and remote URL.

## Manifest Entries

### scaffold-2026-05-08

- Status: scaffold only; no model outputs or benchmark results.
- Repository: `https://github.com/aryan-cs/newspeak`
- Commit SHA: repository commit that adds this scaffold entry.
- Plan: `PLAN.md`
- Dialect specs: draft files under `dialect/`
- Generated results: none.
- Public claims enabled by this entry: repository structure and protocol only.

Machine-readable entry drafts can be generated with:

```bash
PYTHONPATH=src python3 scripts/create_manifest_entry.py \
  --entry-id scaffold-2026-05-08 \
  --status scaffold \
  PLAN.md README.md
```

Generated manifest-entry JSON is a draft input for this file. It does not
replace the human-readable notes about scope, exclusions, and claim status.
