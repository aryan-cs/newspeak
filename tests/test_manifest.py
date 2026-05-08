from pathlib import Path

from newspeak.analysis.manifest import artifact_digest, build_manifest_entry, sha256_file


def test_artifact_digest_reports_relative_path_and_size(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("hello\n", encoding="utf-8")

    digest = artifact_digest(artifact, tmp_path)

    assert digest.path == "artifact.txt"
    assert digest.bytes == 6
    assert digest.sha256 == sha256_file(artifact)


def test_build_manifest_entry_hashes_artifacts(tmp_path):
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("manifest\n", encoding="utf-8")

    entry = build_manifest_entry(
        entry_id="unit-test",
        status="draft",
        artifact_paths=[artifact],
        root=tmp_path,
        remote_url="https://example.invalid/repo.git",
    )

    assert entry["entry_id"] == "unit-test"
    assert entry["status"] == "draft"
    assert entry["repo_commit"] == "unknown"
    assert entry["remote_url"] == "https://example.invalid/repo.git"
    assert entry["artifacts"] == [artifact_digest(artifact, tmp_path).to_dict()]
