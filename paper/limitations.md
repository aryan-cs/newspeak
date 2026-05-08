# Limitations Draft

- The first paper is primary-tokenizer optimized; cross-tokenizer audits are
  generalization diagnostics unless the dialect is redesigned for tokenizer-family
  agnosticism.
- The validator is not a semantic parser and requires gold-set evaluation before
  primary compliance claims.
- Success-conditioned token savings can hide low success rates unless success
  rates are reported for each arm.
- Latent reasoning cannot be proven to occur in the dialect.
- Human raters may learn the dialect unevenly.
- Back-translation can mask dialect-specific failures and is diagnostic only.
