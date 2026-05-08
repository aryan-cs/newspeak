from pathlib import Path

from newspeak.evals.validator_gold import evaluate_gold_records, load_gold_records


def test_seed_validator_gold_examples_match_current_validators():
    records = load_gold_records(Path("data/eval_sets/validator_gold/examples.jsonl"))
    evaluation = evaluate_gold_records(records)

    assert evaluation.total == 7
    assert evaluation.failures == []
    assert evaluation.precision == 1.0
    assert evaluation.recall == 1.0
