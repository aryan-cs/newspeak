from newspeak.analysis.results import paired_success_reduction, summarize_by_arm


def _result(prompt_id, arm, output_tokens, total_tokens, success=True):
    return {
        "prompt_id": prompt_id,
        "arm": arm,
        "metrics": {
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
        "success": {
            "correct_or_adequate": success,
            "safe": success,
            "helpful_or_quality_refusal": success,
            "semantically_preserved": success,
            "primary_success": success,
        },
    }


def test_summarize_by_arm_counts_successful_records():
    summaries = summarize_by_arm(
        [
            _result("p1", "Base-English", 100, 120, success=True),
            _result("p2", "Base-English", 200, 240, success=False),
        ]
    )

    assert len(summaries) == 1
    assert summaries[0].records == 2
    assert summaries[0].primary_success_records == 1
    assert summaries[0].median_successful_output_tokens == 100


def test_paired_success_reduction_uses_successful_intersection():
    reduction = paired_success_reduction(
        [
            _result("p1", "Base-English", 100, 120, success=True),
            _result("p1", "TokenizerAware-Newspeak", 80, 95, success=True),
            _result("p2", "Base-English", 100, 120, success=True),
            _result("p2", "TokenizerAware-Newspeak", 50, 70, success=False),
        ],
        baseline_arm="Base-English",
        candidate_arm="TokenizerAware-Newspeak",
    )

    assert reduction.paired_success_records == 1
    assert reduction.median_relative_reduction == 0.2
    assert reduction.median_baseline_tokens == 100
    assert reduction.median_candidate_tokens == 80


def test_paired_success_reduction_returns_nulls_without_pairs():
    reduction = paired_success_reduction(
        [_result("p1", "Base-English", 100, 120, success=False)],
        baseline_arm="Base-English",
        candidate_arm="Base-Concise",
    )

    assert reduction.paired_success_records == 0
    assert reduction.median_relative_reduction is None
