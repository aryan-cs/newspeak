"""Manifest helper functions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class ArtifactDigest:
    path: str
    sha256: str
    bytes: int

    def to_dict(self) -> dict[str, object]:
        return {"path": self.path, "sha256": self.sha256, "bytes": self.bytes}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_digest(path: Path, root: Path | None = None) -> ArtifactDigest:
    root = root or Path.cwd()
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root.resolve())
    except ValueError:
        relative = resolved
    return ArtifactDigest(
        path=str(relative),
        sha256=sha256_file(resolved),
        bytes=resolved.stat().st_size,
    )


def git_value(root: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    value = completed.stdout.strip()
    return value or None


def git_commit(root: Path) -> str:
    return git_value(root, "rev-parse", "HEAD") or "unknown"


def git_remote_url(root: Path) -> str | None:
    return git_value(root, "config", "--get", "remote.origin.url")


def git_dirty(root: Path) -> bool | None:
    status = git_value(root, "status", "--porcelain")
    if status is None:
        return None
    return bool(status)


def build_manifest_entry(
    entry_id: str,
    status: str,
    artifact_paths: list[Path],
    root: Path | None = None,
    remote_url: str | None = None,
) -> dict[str, object]:
    root = (root or Path.cwd()).resolve()
    entry: dict[str, object] = {
        "entry_id": entry_id,
        "status": status,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo_commit": git_commit(root),
        "repo_dirty": git_dirty(root),
        "artifacts": [artifact_digest(path, root).to_dict() for path in artifact_paths],
    }
    resolved_remote_url = remote_url if remote_url is not None else git_remote_url(root)
    if resolved_remote_url:
        entry["remote_url"] = resolved_remote_url
    return entry
