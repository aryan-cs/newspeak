from pathlib import Path

from newspeak.analysis.manifest import artifact_digest, sha256_file


def test_artifact_digest_reports_relative_path_and_size(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("hello\n", encoding="utf-8")

    digest = artifact_digest(artifact, tmp_path)

    assert digest.path == "artifact.txt"
    assert digest.bytes == 6
    assert digest.sha256 == sha256_file(artifact)
