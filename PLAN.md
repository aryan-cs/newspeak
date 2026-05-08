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

> A productive Newspeak-inspired controlled language may improve token efficiency, but only counts as useful if it preserves capability, safety alignment, and semantic adequacy under paired evaluation.

The paper should avoid claiming that a model's latent reasoning is literally "in Newspeak." The project can test observable interfaces, generated rationales, output distributions, trained behavior, and safety outcomes. It cannot directly inspect or prove the language of hidden internal reasoning.

## Core Research Questions

1. Does a Newspeak-inspired controlled dialect reduce generated tokens, total tokens, latency, or estimated inference cost?
2. Are any token savings still present after conditioning on answers that remain correct, helpful, and safe?
3. Does the dialect preserve capability across knowledge, reasoning, coding, instruction-following, and open-ended assistance tasks?
4. Does safety behavior transfer under linguistic constraint, or do harmful compliance and over-refusal rates change?
5. Which intervention level works best: prompting, in-context examples, output repair, constrained decoding, or fine-tuning?
6. Does a strict closed lexicon create artificial disadvantages relative to a productive, rule-based controlled dialect?
7. Can visible reasoning traces be expressed in the controlled dialect without degrading final-answer quality?
8. Are any observed gains still present after controlling for ordinary concise English and generic controlled English?

## Hypotheses

### H1: Token Efficiency

A productive Newspeak-inspired dialect can reduce characters and words, but model-token savings will depend on tokenizer-aware vocabulary design. Invented or rare words may tokenize inefficiently and erase apparent compression gains.

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
- Cross-model tokenizer comparison if multiple model families are used.

Tokenizer-aware design should not hide capability costs. The final paper must report model tokens, bytes, characters, and words.

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

| Arm | Description | Purpose |
| --- | --- | --- |
| `Base-English` | Unmodified model, normal English prompts and responses | Main capability and safety baseline |
| `Base-Concise` | Same model instructed to answer briefly | Controls for brevity alone |
| `Controlled-English` | Simplified Technical English or Basic-English-like control | Controls for generic controlled language |
| `Prompt-Newspeak` | System prompt asks for Newspeak-style output | Tests instruction-only behavior |
| `ICL-Newspeak` | Few-shot examples demonstrate the dialect | Tests in-context dialect induction |
| `Repair-Newspeak` | Generate, validate, then revise until compliant | Separates solving from dialect expression |
| `InputOutput-Newspeak` | User prompts and model outputs are both dialect-translated | Tests full interface shift |
| `VisibleReasoning-Newspeak` | Any visible reasoning or rationale is also dialect-constrained | Tests reasoning-trace compression |
| `LoRA-Newspeak` | Adapter fine-tuned on parallel English-to-dialect examples | Tests lightweight model modification |
| `LoRA-Newspeak-Safety` | LoRA with safety, refusal, benign-sensitive, and policy-boundary examples | Tests safety-preserving adaptation |
| `Hard-Constrained` | Constrained decoding against lexicon/grammar validator | Upper bound on compliance, likely lower capability |

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
- Run deduplication against training and evaluation sets.
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

## Newspeak-Specific Evaluation

### Dialect Compliance

Measure:

- Lexicon violation rate.
- Grammar violation rate.
- Unauthorized synonym rate.
- Technical passthrough correctness.
- Refusal vocabulary correctness.
- Validator pass rate.

### Semantic Preservation

Measure:

- Back-translation equivalence.
- Human adequacy rating.
- Task-score preservation.
- Contradiction rate.
- Missing-caveat rate.

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

## Primary Outcome Metrics

1. **Capability Delta**
   - Difference from `Base-English` on objective benchmarks.

2. **Safety Delta**
   - Difference in harmful compliance and false refusal.

3. **Success-Conditioned Token Savings**
   - Token reduction only on prompts where the response remains correct and safe.

4. **Dialect Compliance**
   - Percent of responses passing validator checks.

5. **Semantic Preservation**
   - Percent of dialect responses judged equivalent to the English answer.

## Non-Inferiority Criteria

Define these before running the main experiment.

Example starting criteria:

- Capability-preserving if objective score drops by no more than 3 to 5 absolute percentage points.
- Safety-preserving if harmful compliance does not increase by more than 1 to 2 absolute percentage points.
- Helpfulness-preserving if pairwise preference loss is within a predeclared margin after length-bias correction.
- Efficient only if success-conditioned total-token reduction is statistically significant and practically meaningful.

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

The concise-output controls are mandatory because raw token savings are not meaningful unless answers remain correct, useful, and safe.

## Ethics, Safety, and Copyright

### Copyright

The project should cite *Nineteen Eighty-Four* as conceptual motivation but avoid copying substantial text or shipping a full extracted novel lexicon. The research dialect should be original, rule-based, and documented as a separate artifact.

In the United States, works published before 1978 can remain protected for 95 years from publication when the relevant requirements are met. Treat *Nineteen Eighty-Four* cautiously for project assets: quote sparingly, cite normally, and do not publish copied vocabulary tables or novel-derived training corpora as core data.

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

### Milestone 2: Baseline Evaluations

- Select one small open-weight model.
- Run `Base-English`, `Base-Concise`, `Prompt-Newspeak`, and `ICL-Newspeak`.
- Evaluate a small balanced prompt set.
- Analyze token savings, compliance, and obvious capability loss.

### Milestone 3: Evaluation Harness and Registry

- Integrate objective benchmarks.
- Add safety benchmark adapters.
- Add result schema.
- Add paired analysis scripts.
- Add reproducible config files.

### Milestone 4: Dialect Data Creation

- Build parallel English/dialect dataset.
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
   - Controlled natural languages.
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

1. Initialize the repository and push the initial planning document.
2. Draft `dialect/spec.md`.
3. Choose the first open-weight model family.
4. Implement a minimal dialect validator.
5. Build a 50 to 100 prompt pilot set covering capability, safety, and open-ended assistance.
6. Run prompt-only and in-context pilot experiments.
7. Use pilot results to refine the dialect before any fine-tuning.

## Related Work Anchors

Initial anchors for the paper:

- Controlled Natural Languages survey: https://direct.mit.edu/coli/article/40/1/121/1455/A-Survey-and-Classification-of-Controlled-Natural
- HELM: https://github.com/stanford-crfm/helm
- LiveBench: https://github.com/LiveBench/LiveBench
- HarmBench: https://arxiv.org/abs/2402.04249
- StrongREJECT: https://arxiv.org/abs/2402.10260
- JailbreakBench: https://arxiv.org/abs/2404.01318
- XSTest: https://arxiv.org/abs/2308.01263
- SafetyBench: https://arxiv.org/abs/2309.07045
- MMLU: https://arxiv.org/abs/2009.03300
- GPQA: https://arxiv.org/abs/2311.12022
- U.S. Copyright Office duration guidance: https://www.copyright.gov/help/faq/faq-duration.html
