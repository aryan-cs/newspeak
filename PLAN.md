# Newspeak LLM Research Plan

## Project Summary

This project studies whether a language model modified to operate through a Newspeak-inspired controlled dialect can reduce inference-token usage while preserving capability and safety alignment.

The central research problem is not whether a model can imitate a fictional style. The defensible research question is:

> What happens to capability, safety behavior, and token efficiency when a general-purpose language model is forced to communicate through a deliberately compressed, semantically constrained English-like dialect?

The intended paper should make a measured empirical claim about the tradeoff between linguistic compression, task performance, and alignment transfer.

## Working Title

**Language Under Constraint: Capability, Efficiency, and Safety Transfer in Newspeak-Style Language Models**

## Thesis

This project tests the thesis:

> A tokenizer-aware productive controlled dialect can produce success-conditioned token savings over normal and concise English while remaining non-inferior on capability and safety. If it cannot beat concise English, that null result is the main finding.

The paper should avoid claiming that a model's latent reasoning is literally "in Newspeak." The project can test observable interfaces, generated rationales, output distributions, trained behavior, and safety outcomes. It cannot directly inspect or prove the language of hidden internal reasoning.

## First Paper Scope

The first paper should be narrower than the full research program.

Primary claim:

> A tokenizer-aware productive controlled dialect can achieve statistically significant success-conditioned token savings relative to normal English, and its value must be judged against concise-English and generic controlled-English controls while preserving capability and safety within predeclared non-inferiority margins.

This claim is falsifiable. If `Base-Concise` matches the dialect's success-conditioned token savings without additional safety or capability cost, the paper should report a negative result: structured dialect design does not outperform simple brevity prompting for efficiency, even if it improves dialect compliance. That outcome is still publishable if the protocol is clean because it separates linguistic structure from ordinary concision.

The first paper should treat broad capability benchmarking, visible-rationale compression, strict lexicon decoding, and LoRA/SFT as supporting ablations or follow-up phases. The spine is efficiency under safety and capability constraints.

## Venue and Scope Target

Default target: **TMLR** as a full empirical methods paper. This supports the tokenizer audit, safety diagnostics, human evaluation, and null-result framing without forcing an artificially short benchmark suite.

If the target changes to ACL/EMNLP Findings or a short-paper venue, shrink the suite to:

- One knowledge/reasoning benchmark.
- One math or code benchmark.
- One instruction-following/helpfulness set.
- HarmBench or StrongREJECT.
- XSTest.
- The custom dialect semantic-equivalence and tokenizer-efficiency suite.

If the target changes to NeurIPS Datasets and Benchmarks, emphasize the dialect specification, benchmark registry, validation data, and reproducibility artifacts.

## Novelty Positioning

The project sits near several active literatures and should differentiate itself explicitly:

- **Multilingual safety transfer:** Existing work studies safety degradation across natural languages, especially low-resource or typologically distant languages. This project instead constructs an English-derived controlled dialect with known rules, known vocabulary, and controllable tokenizer properties. The point is not language coverage but causal control over linguistic compression.
- **Style as a jailbreak vector:** Recent style-safety work, including *When Style Breaks Safety*, shows that superficial style patterns can increase jailbreak success and that style-tuned models can become vulnerable to matching jailbreak styles. This project must distinguish productive semantic compression from superficial style transfer and include safety diagnostics for style-induced vulnerability.
- **Fine-tuning alignment drift:** Prior work shows that ordinary or adversarial fine-tuning can erode safety. Any LoRA/SFT arm here should be framed as testing dialect-specific drift and mitigation, not as rediscovering that fine-tuning can weaken alignment.
- **Prompt compression and tokenizer research:** The novel angle is tokenizer-aware vocabulary design for a controlled language, evaluated through success-conditioned efficiency rather than raw brevity.

Before submission, re-check *When Style Breaks Safety* and related style-jailbreak work for overlap with `StyleOnly-Newspeak`. If those papers already test productive compression versus surface style, the manuscript must narrow its claim to the tokenizer-aware success-conditioned protocol or cite their result as prior confirmation.

## Core Research Questions

Primary first-paper questions:

1. Does a tokenizer-aware Newspeak-inspired controlled dialect reduce total and output tokens after conditioning on correctness, usefulness, and safety?
2. Do those success-conditioned savings exceed what can be achieved by ordinary concise-English prompting?
3. Does the dialect preserve safety within predeclared margins for both harmful compliance and over-refusal?

Secondary questions:

4. Does generic controlled English behave differently from the Newspeak-inspired productive dialect?
5. Which safety mechanism explains any degradation: obscured safety vocabulary, evaluator/classifier misunderstanding, style-induced jailbreak vulnerability, or fine-tuning alignment drift?
6. Does a strict closed lexicon create artificial disadvantages relative to a productive, rule-based controlled dialect?
7. Can visible reasoning traces be expressed in the controlled dialect without degrading final-answer quality?

## Hypotheses

### H1: Token Efficiency

A productive Newspeak-inspired dialect can reduce characters and words, but model-token savings will depend on tokenizer-aware vocabulary design. Invented or rare words may tokenize inefficiently and erase apparent compression gains. The primary bar is not beating verbose English; it is beating `Base-Concise` on successful responses.

### H2: Capability Retention

Soft constraints such as prompting and in-context examples will preserve more task performance than hard lexicon constraints. Strict closed-vocabulary decoding will likely reduce open-ended capability and should be treated as an ablation, not the main intervention.

### H3: Safety Transfer

Safety alignment may not transfer cleanly under dialect shift. The dialect may increase harmful compliance if safety concepts are obscured, or increase over-refusal if compressed terms resemble unsafe categories.

### H4: Training Effects

Fine-tuning or LoRA adaptation may improve dialect compliance and token efficiency, but can introduce alignment drift or catastrophic forgetting. Safety-oriented training data should be evaluated separately from general dialect training.

### H5: Reasoning Trace Compression

For models that expose visible reasoning or scratchpads, forcing those traces into the dialect may reduce verbosity but may also remove uncertainty, qualifications, or step-level distinctions needed for reliable reasoning.

## Dialect Design

### Design Principle

The dialect should be inspired by Newspeak-like mechanisms rather than copied from the novel. It should be a clean research artifact with explicit rules, licensing clarity, and reproducible validation.

The exact fictional lexicon from *Nineteen Eighty-Four* should not be used as the full project vocabulary or shipped as a derived dataset. The project can cite Orwell as conceptual motivation while defining an original controlled dialect.

### Why Not a Strict Lexicon as the Main Condition

A strict lexicon would confound the study. If model performance drops, the cause might be:

- Loss of necessary technical vocabulary.
- Extra burden from paraphrasing concepts.
- Tokenizer inefficiency for invented terms.
- Reduced expressivity rather than reduced reasoning ability.
- Safety-boundary ambiguity from missing policy-relevant words.

Therefore, strict lexicon enforcement should be an experimental endpoint, not the default model interface.

### Dialect Levels

1. **Loose Style Layer**
   - Model is instructed to use shorter, simpler, Newspeak-like language.
   - No validator enforcement.
   - Useful as a low-cost baseline.

2. **Rule-Based Productive Dialect**
   - Restricted synonym sets.
   - Productive morphology for negation, intensity, and evaluation.
   - Technical passthrough terms allowed under explicit rules.
   - This is the primary dialect condition.

3. **Tokenizer-Aware Productive Dialect**
   - Same as above, but vocabulary choices are optimized for the target tokenizer.
   - Measures whether compression is real at the model-token level.

4. **Strict Lexicon Dialect**
   - Closed or near-closed vocabulary.
   - Technical terms must be decomposed or passed through under tightly limited rules.
   - Used as an ablation to measure the cost of maximal constraint.

## Tokenizer Risk

The dialect must be designed against the tokenizer actually used by the evaluated model. Otherwise, a word that looks shorter to humans can use more model tokens than the English phrase it replaces.

Required checks:

- Token count for every candidate dialect term.
- Token count for common English paraphrases.
- Fertility by category: safety, math, code, science, policy, uncertainty, refusal.
- Compression at the response level, not just at the word level.
- Multi-tokenizer comparison on the primary tokenizer plus at least two other model-family tokenizers.

Tokenizer-aware design should not hide capability costs. The final paper must report model tokens, bytes, characters, and words.

The first paper is scoped as **primary-tokenizer optimized**. Cross-tokenizer results are generalization diagnostics, not the main claim, unless the dialect is redesigned to be tokenizer-family agnostic. If the vocabulary overfits one tokenizer, report that as a limitation and avoid claiming general token efficiency across model families.

### Gating Condition

Tokenizer efficiency is a go/no-go gate before large-scale evaluation or fine-tuning.

Before moving past the dialect prototype, the project must show on a representative pilot set that the productive dialect produces meaningful model-token savings relative to normal English and is not trivially dominated by concise English. The exact gate should be set after a small pilot, but a reasonable starting point is:

- At least 10% median output-token reduction versus `Base-English` on successful responses.
- No increase in total tokens caused by prompt overhead after the first-turn setup is amortized or explicitly accounted for.
- No systematic token inflation in safety, uncertainty, math, code, or technical terminology.
- A clear comparison against `Base-Concise`; if concise English matches the savings, the paper pivots to a negative-result framing.

If this gate fails, the project should stop adaptation work and report the tokenizer result directly rather than spending compute on a dialect that does not compress at the model level.

## Dialect Specification Components

The repository should include a formal dialect specification with:

- Allowed base vocabulary.
- Productive prefix and suffix rules.
- Negation rules.
- Intensity rules.
- Comparatives and superlatives.
- Technical-term passthrough policy.
- Numeric, code, math, citation, and proper-noun policy.
- Safety-policy vocabulary.
- Refusal vocabulary.
- Ambiguity and uncertainty vocabulary.
- Grammar constraints.
- Examples and counterexamples.

The dialect must include enough vocabulary for safe, honest refusals. A compressed language that cannot express uncertainty, risk, consent, legality, or harm is not a viable aligned assistant interface.

## Model Intervention Arms

All experiments should use paired prompts across all arms where possible.

| Arm | Role | Description | Purpose |
| --- | --- | --- | --- |
| `Base-English` | Core | Unmodified model, normal English prompts and responses | Main capability and safety baseline |
| `Base-Concise` | Core | Same model instructed to answer briefly | Controls for brevity alone |
| `Controlled-English` | Core | Basic English 850-word controlled-language baseline with the same technical passthrough policy as the dialect | Controls for generic controlled language |
| `Prompt-Newspeak` | Core | System prompt asks for Newspeak-style output | Tests instruction-only behavior |
| `ICL-Newspeak` | Core | Few-shot examples demonstrate the dialect | Tests in-context dialect induction |
| `TokenizerAware-Newspeak` | Core | Productive dialect with vocabulary chosen against the model tokenizer | Tests the primary efficiency claim |
| `StyleOnly-Newspeak` | Core | Surface Newspeak-like aesthetic without productive vocabulary compression | Separates style shift from semantic compression |
| `Repair-Newspeak` | Diagnostic | Generate, validate, then revise until compliant | Separates solving from dialect expression |
| `InputOutput-Newspeak` | Diagnostic | User prompts and model outputs are both dialect-translated | Tests full interface shift |
| `VisibleReasoning-Newspeak` | Ablation | Any visible reasoning or rationale is also dialect-constrained | Tests reasoning-trace compression |
| `LoRA-Newspeak` | Ablation | Adapter fine-tuned on parallel English-to-dialect examples | Tests lightweight model modification |
| `LoRA-Newspeak-Safety` | Ablation | LoRA with safety, refusal, benign-sensitive, and policy-boundary examples | Tests safety-preserving adaptation |
| `Hard-Constrained` | Ablation | Constrained decoding against lexicon/grammar validator | Upper bound on compliance, likely lower capability |

The `StyleOnly-Newspeak` arm is core because safety findings are not interpretable without it. If `StyleOnly-Newspeak` degrades safety as much as `TokenizerAware-Newspeak`, the result likely belongs to style-shift safety rather than semantic compression. If only `TokenizerAware-Newspeak` degrades safety, the mechanism is more likely vocabulary compression, ambiguity, or safety-term loss.

The `Controlled-English` arm is pinned to a Basic English 850-word baseline because it is a general controlled-English comparator with a clear vocabulary-size target and does not import the domain-specific maintenance-document assumptions of ASD-STE100. The project should freeze and ship its normalized control lexicon and rules after confirming redistribution status; if redistribution is not appropriate, publish a fetch/build script and the exact source/version metadata.

## Model Selection

Use open-weight models for reproducibility. At minimum:

- One small model suitable for iteration.
- One stronger model in the same family for scale comparison.
- Prefer instruction-tuned bases with known benchmark behavior.
- Freeze model identifiers, revisions, tokenizer versions, inference settings, and chat templates.

Candidate families can include Llama, Qwen, Mistral, Gemma, or comparable open models. The exact choice should be made based on licensing, hardware availability, tokenizer behavior, and reproducibility.

Closed API models can be used only as external comparison points, not as the primary scientific artifact.

## Data Strategy

### Dataset Coverage

The project needs evaluation coverage for:

- General capability.
- Math.
- Code.
- Instruction following.
- Truthfulness and calibration.
- Summarization and closed-document QA.
- Harmful compliance.
- Over-refusal.
- Prompt injection and instruction hierarchy.
- Bias and fairness.
- Dialect compliance.
- Semantic equivalence.

### Parallel Dialect Data

Create a verified parallel dataset:

- English prompt.
- Dialect prompt.
- English answer.
- Dialect answer.
- Task category.
- Safety label.
- Expected scoring method.
- Dialect compliance score.
- Semantic-equivalence review status.

No fake, filler, or synthetic-only data should be used as final evaluation data without validation. Synthetic generation can be used for candidate creation, but final training and evaluation records require automated checks plus human or expert review where appropriate.

Synthetic or model-generated records are acceptable only when they are:

- Clearly labeled as generated.
- Validated for dialect compliance.
- Checked for semantic equivalence.
- Deduplicated against evaluation data.
- Excluded from claims that require independent human-authored ground truth.

### Training Data

Training data should include:

- General assistant responses.
- Task-solving examples.
- Refusals.
- Safe completion of benign-sensitive requests.
- Boundary cases where the model should explain limits.
- Uncertainty and calibration examples.
- Math and code examples where exact syntax must not be distorted.
- Technical passthrough examples.

### Evaluation Data

Evaluation data must be held out from training and translation examples. Any generated dialect translations of benchmark prompts should be versioned and reviewed for semantic equivalence.

### Contamination Controls

Required controls:

- Pin benchmark names, versions, splits, and licenses.
- Log model identifiers, tokenizer identifiers, revisions, hashes, chat templates, and inference settings.
- Keep translated evaluation prompts held out from training and prompt examples.
- Exclude benchmark examples and near-duplicates from SFT data.
- Run deduplication against training and evaluation sets using exact hashes, normalized n-gram overlap, MinHash or SimHash near-duplicate detection, and embedding-similarity review above a predeclared threshold.
- Store the exact prompt template used for each arm.
- Preserve raw generations and scoring metadata for audit.

## Capability Evaluation

Use a compact but representative benchmark suite.

### Knowledge and Reasoning

- MMLU or MMLU-Pro.
- GPQA subset if budget allows.
- DROP or a comparable reading-comprehension benchmark.

### Math

- GSM8K.
- MATH subset or another harder math subset if budget allows.

### Coding

- HumanEval.
- MBPP or LiveCodeBench.

For coding tasks, code blocks should not be forced into dialect. The natural-language explanation can be dialect-constrained, but code syntax must remain valid programming language syntax.

### Instruction Following

- IFEval.
- Custom instruction-following tasks that include length, format, and dialect constraints.

### Open-Ended Assistance

- A small curated helpfulness set.
- Pairwise human or model-judge evaluation with length-bias controls.
- Summarization and closed-document QA tasks where factuality can be checked.

## Safety and Alignment Evaluation

Safety evaluation must include both under-refusal and over-refusal.

### Harmful Compliance

- HarmBench.
- JailbreakBench.
- StrongREJECT or comparable refusal robustness benchmark.

### Over-Refusal

- XSTest.
- Benign-sensitive prompts involving words or topics that resemble unsafe domains but should be answered.

### Safety Understanding

- SafetyBench or equivalent safety QA.
- Custom policy-boundary prompts translated into the dialect.

### Truthfulness and Calibration

- TruthfulQA or comparable truthfulness benchmark.
- Short-answer factuality tasks.
- Uncertainty-expression prompts that test whether the dialect can represent doubt and epistemic limits.

### Bias and Fairness

- BBQ or comparable bias benchmark.
- Include tests where compressed evaluative vocabulary could collapse important distinctions.

### Instruction Hierarchy and Prompt Injection

Create a small custom set for:

- System-vs-user instruction conflicts.
- Attempts to exploit dialect ambiguity.
- Requests to redefine dialect safety terms.
- Requests to hide harmful intent behind compressed vocabulary.

### Safety Mechanism Diagnostics

If safety changes, the experiment must separate possible mechanisms:

1. **Obscured Safety Vocabulary**
   - Compare English harmful prompts, dialect-translated harmful prompts, and dialect prompts with explicit safety vocabulary preserved.
   - Test whether adding approved safety terms restores refusal behavior.
   - Tag unsafe prompts by whether harm cues are explicit, euphemized, or dialect-compressed.

2. **Evaluator or Classifier Misreading**
   - Score safety outputs in three ways: native dialect response, back-translated English response, and human audit.
   - Compare LLM-judge and safety-classifier decisions against human labels on a stratified sample.

3. **Style-Induced Jailbreak Vulnerability**
   - Include style-only controls that impose surface style without semantic compression.
   - Compare attack success on plain harmful prompts, style-augmented harmful prompts, and productive-dialect harmful prompts.
   - Treat the style-only arm as a direct bridge to style-as-jailbreak prior work.

4. **Fine-Tuning Alignment Drift**
   - Compare no-training, general LoRA, dialect LoRA, and safety-augmented dialect LoRA.
   - Run English safety regression tests after every adaptation step.

Without these diagnostics, safety findings will be difficult to interpret.

## Newspeak-Specific Evaluation

### Dialect Compliance

Measure:

- Lexicon violation rate.
- Grammar violation rate.
- Unauthorized synonym rate.
- Technical passthrough correctness.
- Refusal vocabulary correctness.
- Validator pass rate.

Validator evaluation is required before the validator is used for data gating or compliance reporting:

- Build a gold-labeled validator test set with valid and invalid examples, including technical passthrough, math, code, refusals, uncertainty language, and adversarial near-misses.
- Use human annotation and adjudication for valid/invalid labels.
- Report precision, recall, and F1 overall and by violation category.
- Deployment target: precision >= 0.95 for gating training/evaluation data and recall >= 0.85 for compliance reporting.
- If the validator misses these thresholds, use it as a screening tool only and rely on human audit for primary compliance claims.

### Semantic Preservation

Measure:

- Human adequacy rating.
- Task-score preservation.
- Contradiction rate.
- Missing-caveat rate.
- Back-translation equivalence as a screening and diagnostic metric only.

Back-translation must not be the primary semantic-preservation metric because it can normalize away dialect-specific failures. Use stratified human review of high-score and low-score back-translations, especially cases where back-translation says "equivalent" but the original dialect response is compressed, ambiguous, or safety-relevant.

### Compression

Report:

- Output tokens.
- Prompt tokens.
- Total tokens.
- Characters.
- Bytes.
- Words.
- Latency.
- Estimated cost.
- Tokens per correct answer.
- Tokens per safe answer.

Token savings should be reported both unconditionally and conditioned on success.

Latency is a secondary metric unless measured under fixed infrastructure. When reported, include total wall-clock generation time, time-to-first-token, tokens per second, hardware, inference backend, quantization, batch size, max-token cap, sampling configuration, warmup policy, and number of repeats.

## Primary Outcome Metrics

1. **Capability Delta**
   - Difference from `Base-English` on objective benchmarks.

2. **Safety Delta**
   - Difference in harmful compliance and false refusal.

3. **Success-Conditioned Token Savings**
   - Token reduction only on prompts where the response remains correct and safe.
   - Primary comparison is `TokenizerAware-Newspeak` versus `Base-Concise`, with `Base-English` as the absolute baseline.

4. **Dialect Compliance**
   - Percent of responses passing validator checks.

5. **Semantic Preservation**
   - Percent of dialect responses judged equivalent to the English answer.

### Success-Conditioning Decision Rule

For the primary efficiency metric, a response is successful only if it simultaneously satisfies all applicable gates:

- **Correctness or task adequacy:** objective benchmark correctness, unit-test pass, or human adequacy above the predeclared threshold.
- **Safety appropriateness:** harmful requests are refused without actionable harmful content; benign requests are not falsely refused.
- **Minimum helpfulness or refusal quality:** the response is not merely short; it provides enough useful content, caveats, or safe alternatives for the task type.
- **Semantic preservation:** dialect responses do not change the answer, omit required caveats, or introduce contradictions.

Primary success-conditioned token savings are computed on the paired intersection for each comparison: the same prompt must be successful for both `TokenizerAware-Newspeak` and the comparator. Also report each arm's success rate over all prompts, so token savings cannot hide failures. Secondary analyses may condition on correctness-only, safety-only, or helpfulness-only, but those are not the primary claim.

Ambiguous cases are failures for the primary metric. For example, a technically correct answer that over-refuses a benign request, a safe refusal that gives no clear boundary or safe alternative, or a short answer that omits a required caveat does not count as successful.

## Non-Inferiority Criteria

Define these before running the main experiment.

Example starting criteria:

- Capability-preserving if objective score drops by no more than 3 to 5 absolute percentage points.
- Safety-preserving if harmful compliance does not increase by more than 1 to 2 absolute percentage points.
- Helpfulness-preserving if pairwise preference loss is within a predeclared margin after length-bias correction.
- Efficient only if success-conditioned total-token reduction is statistically significant and practically meaningful against both `Base-English` and `Base-Concise`.

These margins should be revisited after pilot variance estimates.

## Statistical Analysis

Use paired analysis wherever possible because each prompt appears across all arms.

Recommended methods:

- Power estimates after the pilot phase to size the main evaluation.
- Paired bootstrap confidence intervals for token savings and score deltas.
- McNemar tests for paired binary correctness/refusal outcomes.
- Mixed-effects logistic regression for correctness and safety outcomes.
- Mixed-effects linear or negative-binomial models for token counts.
- Multiple-comparison correction across benchmark families.
- Stratified analysis by task domain, model size, and intervention level.

Power plan:

- Use pilot variance to power the main evaluation at 80% power.
- Target detectable effects: at least a 10% median token reduction, a 5 percentage-point capability delta, and a 5 percentage-point safety/refusal delta.
- If pilot variance makes these targets infeasible, shrink the venue scope or treat affected outcomes as exploratory.

Report tradeoff frontiers:

- Token reduction vs capability loss.
- Token reduction vs harmful compliance.
- Token reduction vs over-refusal.
- Dialect compliance vs capability.
- Dialect compliance vs safety.

## Human Evaluation

Human review should be used for:

- Semantic equivalence of translated prompts.
- Adequacy of dialect answers.
- Safety-critical responses.
- Over-refusal edge cases.
- Refusal quality.
- Cases where automated judges may misunderstand dialect vocabulary.

Collect:

- Rater instructions.
- Rating rubric.
- Inter-rater reliability.
- Adjudication process.
- Sampled examples for qualitative analysis.
- Safety handling guidance for harmful-content exposure.
- Dialect comprehension checks so raters understand the controlled vocabulary before judging adequacy.

Initial human-evaluation target:

- At least two independent raters per item.
- A pilot calibration round before final annotation.
- Inter-rater agreement target of Cohen's kappa or Krippendorff's alpha >= 0.70 for categorical labels where applicable.
- Stratified sample covering correct, incorrect, unsafe, over-refused, high-compression, and low-compliance responses.
- Pilot sample of 100 to 200 paired items.
- Main sample of 500 to 1,000 judged responses, adjusted after power estimates and pilot disagreement rates.
- Blinded condition labels and randomized response order.
- Rater dialect-training task with a comprehension check before live annotation.

The rubric should be written before annotation begins and should separate semantic equivalence, task adequacy, safety correctness, refusal quality, and dialect comprehensibility.

Refusal quality dimensions:

- Correct refusal boundary.
- Clear statement of what cannot be provided.
- Brief safety rationale when appropriate.
- Non-dismissive tone.
- Safe alternative or redirection where appropriate.
- No actionable harmful detail.

## Expected Failure Modes

1. **Strict Lexicon Confound**
   - Model fails because required words are banned, not because reasoning degraded.

2. **Tokenizer Mismatch**
   - Short-looking dialect uses more tokens than English.

3. **Safety Vocabulary Collapse**
   - Dialect lacks terms needed to express risk, legality, consent, or uncertainty.

4. **Judge Misclassification**
   - Automated safety classifiers or LLM judges misread dialect responses.

5. **Translation Artifacts**
   - Dialect prompt translation changes task difficulty.

6. **Over-Compression**
   - Answers omit caveats, assumptions, or stepwise reasoning.

7. **Alignment Drift**
   - Fine-tuning for dialect compliance weakens refusal behavior.

8. **Benchmark Leakage**
   - Training examples overlap with evaluation tasks.

9. **Code and Math Corruption**
   - Dialect constraints alter formal syntax or precise mathematical language.

10. **False Efficiency**
    - Token savings come only from shorter, less useful answers.

11. **Short-Answer-Only Gains**
    - Dialect compression helps short answers but disappears for long-form reasoning, careful refusals, or high-context tasks.

12. **Tokenizer Overfit**
    - Tokenizer-aware vocabulary works for one tokenizer but fails across model families.

13. **Hidden Ambiguity**
    - Humans accept compressed dialect wording that objective scoring later reveals as incomplete or wrong.

14. **Low-Quality Refusals**
    - Safety refusals become shorter but less actionable, less clear, or less empathetic.

15. **Rater Learning Effects**
    - Human raters learn the dialect unevenly, making adequacy ratings noisy.

16. **Back-Translation Masking**
    - Back-translation normalizes away dialect-specific errors and makes outputs look safer or more adequate than they are.

The concise-output controls are mandatory because raw token savings are not meaningful unless answers remain correct, useful, and safe.

## Null-Result Framing

If `Base-Concise` matches or beats the dialect on success-conditioned model tokens while preserving capability and safety, the first paper should not force a positive claim. The paper becomes:

> Structured artificial dialects do not improve efficient utility beyond ordinary brevity prompting under this protocol, though they may still offer measurable compliance, interpretability, or control benefits.

This should be stated before experiments begin so a negative result is not treated as a failed project.

## Ethics, Safety, and Copyright

### Copyright

The project should cite *Nineteen Eighty-Four* as conceptual motivation but avoid copying substantial text or shipping a full extracted novel lexicon. The research dialect should be original, rule-based, and documented as a separate artifact.

*Nineteen Eighty-Four* was published in 1949 and should be treated as under U.S. copyright through 2044 under the 95-year publication-term framing, entering the public domain no earlier than January 1, 2045 in the United States. Treat this as unambiguous for project purposes: quote sparingly, cite normally, and do not publish copied vocabulary tables, extracted lexicons, passages, or novel-derived training corpora as core data.

### Dual Use

This project touches jailbreak and harmful-compliance evaluation. Harmful prompts and responses should be handled according to benchmark licenses and safety norms. The public repo should avoid publishing unnecessary harmful generations.

### Safety Reporting

Report safety degradations clearly. If fine-tuning causes alignment drift, that is a central result, not an implementation failure to hide.

### Human Subjects

If human raters are used, define data handling, consent process, compensation, and exposure limits for harmful content.

## Repository Structure

Planned structure:

```text
newspeak/
  PLAN.md
  README.md
  CITATION.cff
  MANIFEST.md
  pyproject.toml
  configs/
    models/
    evals/
    training/
  dialect/
    spec.md
    schema.md
    lexicon.yaml
    morphology.yaml
    safety_terms.yaml
    examples.md
  data/
    raw/
    interim/
    processed/
    eval_sets/
    cards/
  scripts/
    validate_dialect.py
    translate_dataset.py
    run_generation.py
    run_eval.py
    analyze_results.py
  src/
    newspeak/
      dialect/
      evals/
      training/
      analysis/
  notebooks/
  results/
    pilots/
    main/
  paper/
    outline.md
    related_work.md
    figures/
    references.bib
  tests/
```

Generated data, model outputs, and checkpoints should be excluded from git unless they are small, licensed, and intended for publication.

Core artifacts to maintain:

- Dialect specification.
- Lexicon schema.
- Validator.
- Benchmark registry.
- Experiment configs.
- Data cards.
- Model cards for adapted models.
- Evaluation harness.
- Results schema.
- Analysis scripts and notebooks.
- Paper outline.
- Citation file.
- Reproducibility manifest.

`CITATION.cff` should start as a placeholder with the project title, initial authors, repository URL, and message indicating that final citation metadata will be completed when the manuscript has a stable title, author order, DOI, arXiv identifier, or proceedings reference.

## Implementation Milestones

### Milestone 0: Protocol and Project Scaffold

- Initialize repository.
- Add `PLAN.md`.
- Add README with project goals and non-goals.
- Add dependency and formatting setup.
- Add basic result and data directory policies.

### Milestone 1: Dialect Prototype

- Draft dialect spec.
- Create initial lexicon and morphology rules.
- Implement validator.
- Add unit tests for validator behavior.
- Run tokenizer-efficiency audit on candidate vocabulary.
- Audit candidate vocabulary on the primary tokenizer plus at least two other model-family tokenizers.
- Build a gold-labeled validator test set and meet validator precision/recall deployment thresholds before using validator scores as primary measurements.
- Report token savings by model tokenizer before safety or capability benchmark work begins.
- Apply the tokenizer go/no-go gate: median token reduction versus `Base-English`, no systematic inflation in safety/technical language, and an explicit comparison to `Base-Concise`.
- If `Base-Concise` dominates, pivot to the negative-result framing before any LoRA/SFT work.

### Milestone 2: Baseline Evaluations

- Select one small open-weight model.
- Run core arms: `Base-English`, `Base-Concise`, `Controlled-English`, `Prompt-Newspeak`, `ICL-Newspeak`, `TokenizerAware-Newspeak`, and `StyleOnly-Newspeak`.
- Evaluate a small balanced prompt set.
- Analyze token savings, compliance, and obvious capability loss.

### Milestone 3: Evaluation Harness and Registry

- Integrate objective benchmarks.
- Add safety benchmark adapters.
- Add result schema.
- Add paired analysis scripts.
- Add reproducible config files.
- Implement contamination screening and deduplication before any parallel data is allowed into training.

### Milestone 4: Dialect Data Creation

- Build parallel English/dialect dataset.
- Run benchmark-overlap and near-duplicate screening before finalizing the data.
- Validate dialect compliance.
- Review semantic equivalence.
- Split into train, validation, and held-out evaluation sets.

### Milestone 5: Adaptation

- Train LoRA or comparable adapter.
- Train safety-augmented LoRA variant.
- Record all training configs and seeds.
- Evaluate English regression performance.

### Milestone 6: Main Experiment

- Run all predeclared arms.
- Store raw outputs and metadata.
- Compute primary and secondary metrics.
- Run human audit on sampled cases.

### Milestone 7: Human Audit

- Run rater study.
- Measure inter-rater agreement.
- Adjudicate disputed items.
- Update qualitative failure analysis.

### Milestone 8: Paper Draft

- Write methods.
- Write results.
- Build figures and tables.
- Add qualitative examples.
- Release reproducibility package.

## Training and Adaptation Plan

Training should be phased so that expensive adaptation does not happen before the dialect and metrics are stable.

1. **Prompting**
   - Start with system prompts and direct style instructions.
   - Establish whether the base model can follow the dialect at all.

2. **In-Context Learning**
   - Add few-shot examples of prompt translation, answer style, refusals, uncertainty, and technical passthrough.
   - Compare against concise English few-shot controls.

3. **Validator and Repair**
   - Generate normally, validate dialect compliance, then ask the model to repair violations.
   - This separates task-solving ability from expression under constraint.

4. **Constrained Decoding**
   - Use as an ablation for strict compliance.
   - Expect lower capability on open-ended and technical tasks.

5. **LoRA or SFT**
   - Train only after the dialect spec and validator are stable.
   - Use verified parallel data and hold out all translated evaluation prompts.

6. **Safety-Tuned LoRA or SFT**
   - Add safety, refusal, benign-sensitive, and boundary examples.
   - Evaluate whether safety adaptation repairs any alignment drift from dialect training.

## Paper Outline

1. **Abstract**
   - State the intervention, evaluation suite, and primary tradeoff findings.

2. **Introduction**
   - Motivation: compression, controlled language, alignment transfer.
   - Research questions.
   - Contributions.

3. **Related Work**
   - Controlled natural languages for machine translation, technical documentation, semantic parsing, NLG grounding, and domain-specific generation.
   - Tokenization and compression.
   - Constrained decoding.
   - Safety and alignment robustness.
   - Fine-tuning safety risks.

4. **Dialect Design**
   - Newspeak-inspired principles.
   - Original dialect spec.
   - Strict vs productive constraints.
   - Validator and tokenizer-aware design.

5. **Experimental Setup**
   - Models.
   - Intervention arms.
   - Datasets.
   - Training/adaptation.
   - Inference settings.

6. **Metrics**
   - Token efficiency.
   - Capability.
   - Safety.
   - Dialect compliance.
   - Semantic preservation.

7. **Results**
   - Overall tradeoff frontier.
   - Capability by domain.
   - Safety behavior.
   - Token savings conditioned on success.
   - Ablations.

8. **Qualitative Analysis**
   - Representative successes.
   - Failure cases.
   - Safety-boundary ambiguity.
   - Reasoning trace examples.

9. **Limitations**
   - Artificial dialect generality.
   - Benchmark dependence.
   - Judge reliability.
   - Latent reasoning unobservability.
   - Compute limits.

10. **Ethics and Safety**
    - Handling harmful prompts.
    - Copyright considerations.
    - Human rater protections.

11. **Conclusion**
    - Summarize when constrained language helps, hurts, or changes alignment.

## Initial Decision Log

- Use a productive controlled dialect as the main condition.
- Keep strict lexicon enforcement as an ablation.
- Treat exact novel vocabulary as inspiration, not as a copied dataset.
- Start with prompting and in-context learning before fine-tuning.
- Fine-tune only after the dialect validator and evaluation harness are stable.
- Report success-conditioned token savings rather than raw brevity alone.
- Evaluate both harmful compliance and over-refusal.

## Immediate Next Steps

1. Draft `dialect/spec.md`.
2. Choose the first open-weight model family and tokenizer, plus two comparison tokenizers for the Milestone 1 audit.
3. Implement a minimal dialect validator.
4. Build the validator gold set and tokenizer audit for candidate dialect terms.
5. Build a 50 to 100 prompt pilot set covering efficiency, safety, style-only, and concise-English controls.
6. Run prompt-only and in-context pilot experiments.
7. Apply the tokenizer and validator gates and decide whether to continue with the positive-claim or null-result framing.

## Related Work Anchors

Initial anchors for the paper:

- Controlled Natural Languages survey: https://direct.mit.edu/coli/article/40/1/121/1455/A-Survey-and-Classification-of-Controlled-Natural
- Basic English overview: https://en.wikipedia.org/wiki/Basic_English
- ASD-STE100 Simplified Technical English: https://www.asd-europe.org/standards-specifications/simplified-technical-english/
- Attempto Controlled English: https://arxiv.org/abs/cmp-lg/9603003
- HELM: https://github.com/stanford-crfm/helm
- LiveBench: https://github.com/LiveBench/LiveBench
- Low-Resource Languages Jailbreak GPT-4: https://arxiv.org/abs/2310.02446
- HarmBench: https://arxiv.org/abs/2402.04249
- StrongREJECT: https://arxiv.org/abs/2402.10260
- JailbreakBench: https://arxiv.org/abs/2404.01318
- When Style Breaks Safety: https://arxiv.org/abs/2506.07452
- XSTest: https://arxiv.org/abs/2308.01263
- SafetyBench: https://arxiv.org/abs/2309.07045
- MMLU: https://arxiv.org/abs/2009.03300
- GPQA: https://arxiv.org/abs/2311.12022
- U.S. Copyright Office duration guidance: https://www.copyright.gov/help/faq/faq-duration.html
