# Dialect Rule Schema

The config files in this directory are JSON-compatible YAML so they can be read
without a YAML dependency during early development.

## `lexicon.yaml`

Required top-level fields:

- `version`: integer schema version.
- `function_words`: closed-class words allowed in ordinary grammar.
- `roots`: original dialect roots grouped by semantic category.
- `technical_allowlist`: exact passthrough terms expected in early examples.
- `forbidden_source_terms`: terms that should not appear because they are copied
  from the novel or otherwise unsuitable for project assets.

## `morphology.yaml`

Required top-level fields:

- `version`: integer schema version.
- `prefixes`: productive prefixes with semantic labels.
- `suffixes`: productive suffixes with semantic labels.
- `hyphenated_patterns`: allowed pattern names for hyphenated forms.
- `sentence`: sentence-level heuristic defaults.

## `safety_terms.yaml`

Required top-level fields:

- `version`: integer schema version.
- `refusal`: permitted refusal-boundary words.
- `uncertainty`: permitted uncertainty words.
- `harm`: permitted harm/risk words.
- `consent_privacy`: permitted consent and privacy words.
- `legal_medical_financial`: permitted caution terms.
- `safe_alternatives`: permitted redirection terms.
