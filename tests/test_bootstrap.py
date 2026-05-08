import pytest

from newspeak.analysis.bootstrap import median_relative_reduction, paired_bootstrap_ci


def test_median_relative_reduction_uses_paired_counts():
    value = median_relative_reduction([(100, 80), (200, 100), (50, 50)])

    assert value == 0.2


def test_paired_bootstrap_ci_is_reproducible():
    ci_one = paired_bootstrap_ci(
        [(100, 80), (200, 100), (50, 40)],
        iterations=50,
        seed=7,
    )
    ci_two = paired_bootstrap_ci(
        [(100, 80), (200, 100), (50, 40)],
        iterations=50,
        seed=7,
    )

    assert ci_one == ci_two
    assert ci_one[0] <= ci_one[1]


def test_paired_bootstrap_ci_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="iterations"):
        paired_bootstrap_ci([(100, 80)], iterations=0)
    with pytest.raises(ValueError, match="confidence"):
        paired_bootstrap_ci([(100, 80)], confidence=1.5)
