from newspeak.analysis.contamination import TextRecord, find_overlaps, normalize_text, sha256_text


def test_normalized_hash_ignores_case_and_punctuation():
    assert sha256_text("Hello, WORLD!") == sha256_text("hello world")
    assert normalize_text("Hello, WORLD!") == "hello world"


def test_find_overlaps_detects_exact_and_near_duplicates():
    left = [
        TextRecord("left_exact", "count the model output tokens"),
        TextRecord("left_near", "explain safe refusal boundary for harmful request"),
    ]
    right = [
        TextRecord("right_exact", "Count the model output tokens."),
        TextRecord("right_near", "explain safe refusal boundary for harmful request now"),
    ]

    findings = find_overlaps(left, right, ngram_size=3, ngram_threshold=0.5)
    kinds = {(finding.left_id, finding.right_id, finding.kind) for finding in findings}

    assert ("left_exact", "right_exact", "exact_hash") in kinds
    assert ("left_near", "right_near", "ngram_jaccard") in kinds
