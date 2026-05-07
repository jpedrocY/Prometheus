"""Public-only microstructure manifest data model.

Phase 4aw scaffold-only. Defines the manifest data model that a
future capture phase will populate. ``research_eligible`` defaults to
``False`` and ``eligibility_gate_status`` defaults to ``pending``.

This module deliberately does NOT expose a public helper to flip
``research_eligible`` to ``True``. The future eligibility gate is the
only path that may flip that flag, and the gate is not implemented in
Phase 4aw. The :meth:`MicrostructureManifest.flip_research_eligible`
method exists structurally but always raises
:class:`ManifestImmutableError`. This protects the manifest from
silent or accidental promotion.

This module:

- does NOT call endpoints;
- does NOT open WebSockets;
- does NOT download archives;
- does NOT create directories;
- does NOT create real project manifests;
- does NOT write to ``data/microstructure/``;
- only saves/loads when the caller passes an explicit path
  (intended for tests using pytest ``tmp_path``).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .invalid_window import InvalidWindow


class ManifestImmutableError(RuntimeError):
    """Raised when a forbidden manifest mutation is attempted.

    Most notably, attempting to flip ``research_eligible`` to ``True``
    via :meth:`MicrostructureManifest.flip_research_eligible` always
    raises this — only the future eligibility gate (separately
    authorized in a later phase) may perform that transition.
    """


class EligibilityGateStatus(StrEnum):
    """Tri-state eligibility gate status for the future capture stack."""

    PENDING = "pending"
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True)
class FileEntry:
    """A single raw or normalized file referenced by the manifest."""

    path: str
    sha256: str
    event_count: int
    start_time_ms: int
    end_time_ms: int

    def __post_init__(self) -> None:
        if not isinstance(self.path, str) or not self.path:
            raise ValueError("path must be a non-empty string")
        if not isinstance(self.sha256, str) or len(self.sha256) != 64:
            raise ValueError("sha256 must be a 64-character hex string")
        if not isinstance(self.event_count, int) or self.event_count < 0:
            raise ValueError("event_count must be a non-negative int")
        if not isinstance(self.start_time_ms, int) or isinstance(self.start_time_ms, bool):
            raise ValueError("start_time_ms must be an int")
        if not isinstance(self.end_time_ms, int) or isinstance(self.end_time_ms, bool):
            raise ValueError("end_time_ms must be an int")
        if self.end_time_ms < self.start_time_ms:
            raise ValueError("end_time_ms must be >= start_time_ms")


@dataclass
class MicrostructureManifest:
    """Microstructure dataset manifest.

    Mutation surface is intentionally narrow: append-only file and
    invalid-window lists. ``research_eligible`` cannot be flipped to
    ``True`` through this scaffold; see
    :meth:`flip_research_eligible`.
    """

    dataset_family: str
    version: str
    symbol: str
    source: str
    endpoint: str
    capture_mode: str
    schema_version: str
    endpoint_docs_reference: str
    capture_config_hash: str
    code_commit_sha: str
    governance_labels: dict[str, str] = field(default_factory=dict)
    start_time_ms: int = 0
    end_time_ms: int = 0
    event_count: int = 0
    file_count: int = 0
    files: list[FileEntry] = field(default_factory=list)
    invalid_windows: list[InvalidWindow] = field(default_factory=list)
    retention_warning: str | None = None
    proxy_warning: str | None = None
    research_eligible: bool = False
    eligibility_gate_status: EligibilityGateStatus = EligibilityGateStatus.PENDING

    def __post_init__(self) -> None:
        for label, value in (
            ("dataset_family", self.dataset_family),
            ("version", self.version),
            ("symbol", self.symbol),
            ("source", self.source),
            ("endpoint", self.endpoint),
            ("capture_mode", self.capture_mode),
            ("schema_version", self.schema_version),
            ("endpoint_docs_reference", self.endpoint_docs_reference),
            ("capture_config_hash", self.capture_config_hash),
            ("code_commit_sha", self.code_commit_sha),
        ):
            if not isinstance(value, str) or not value:
                raise ValueError(f"{label} must be a non-empty string")

    def append_file(self, entry: FileEntry) -> None:
        """Append a :class:`FileEntry` and update derived counters."""
        self.files.append(entry)
        self.file_count = len(self.files)
        self.event_count += entry.event_count
        if self.start_time_ms == 0 or entry.start_time_ms < self.start_time_ms:
            self.start_time_ms = entry.start_time_ms
        if entry.end_time_ms > self.end_time_ms:
            self.end_time_ms = entry.end_time_ms

    def append_invalid_window(self, window: InvalidWindow) -> None:
        """Append an :class:`InvalidWindow` to the manifest."""
        self.invalid_windows.append(window)

    def flip_research_eligible(self, *_args: Any, **_kwargs: Any) -> None:
        """Always raise :class:`ManifestImmutableError`.

        Phase 4aw does not implement the eligibility gate. Manifests
        must remain ``research_eligible=False`` until a separately
        authorized future phase adds a real gate. This method exists
        only so that callers cannot quietly assume a flip path.
        """
        raise ManifestImmutableError(
            "research_eligible cannot be flipped by the Phase 4aw scaffold; "
            "only the future eligibility gate (separately authorized) may do so"
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a JSON-friendly dict."""
        return {
            "dataset_family": self.dataset_family,
            "version": self.version,
            "symbol": self.symbol,
            "source": self.source,
            "endpoint": self.endpoint,
            "capture_mode": self.capture_mode,
            "schema_version": self.schema_version,
            "endpoint_docs_reference": self.endpoint_docs_reference,
            "capture_config_hash": self.capture_config_hash,
            "code_commit_sha": self.code_commit_sha,
            "governance_labels": dict(self.governance_labels),
            "start_time_ms": self.start_time_ms,
            "end_time_ms": self.end_time_ms,
            "event_count": self.event_count,
            "file_count": self.file_count,
            "files": [
                {
                    "path": f.path,
                    "sha256": f.sha256,
                    "event_count": f.event_count,
                    "start_time_ms": f.start_time_ms,
                    "end_time_ms": f.end_time_ms,
                }
                for f in self.files
            ],
            "invalid_windows": [w.to_dict() for w in self.invalid_windows],
            "retention_warning": self.retention_warning,
            "proxy_warning": self.proxy_warning,
            "research_eligible": self.research_eligible,
            "eligibility_gate_status": self.eligibility_gate_status.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> MicrostructureManifest:
        """Round-trip from :meth:`to_dict` output.

        ``research_eligible`` is deliberately re-read from the input;
        future strict loading should reject ``research_eligible=True``
        unless ``eligibility_gate_status`` is ``pass``, but Phase 4aw
        intentionally leaves that strict check to the future
        eligibility-gate phase.
        """
        manifest = cls(
            dataset_family=str(data["dataset_family"]),
            version=str(data["version"]),
            symbol=str(data["symbol"]),
            source=str(data["source"]),
            endpoint=str(data["endpoint"]),
            capture_mode=str(data["capture_mode"]),
            schema_version=str(data["schema_version"]),
            endpoint_docs_reference=str(data["endpoint_docs_reference"]),
            capture_config_hash=str(data["capture_config_hash"]),
            code_commit_sha=str(data["code_commit_sha"]),
            governance_labels=dict(data.get("governance_labels", {})),
            start_time_ms=int(data.get("start_time_ms", 0)),
            end_time_ms=int(data.get("end_time_ms", 0)),
            event_count=int(data.get("event_count", 0)),
            file_count=int(data.get("file_count", 0)),
            retention_warning=data.get("retention_warning"),
            proxy_warning=data.get("proxy_warning"),
            research_eligible=bool(data.get("research_eligible", False)),
            eligibility_gate_status=EligibilityGateStatus(
                data.get("eligibility_gate_status", EligibilityGateStatus.PENDING.value)
            ),
        )
        for raw in data.get("files", []):
            manifest.files.append(
                FileEntry(
                    path=str(raw["path"]),
                    sha256=str(raw["sha256"]),
                    event_count=int(raw["event_count"]),
                    start_time_ms=int(raw["start_time_ms"]),
                    end_time_ms=int(raw["end_time_ms"]),
                )
            )
        manifest.file_count = len(manifest.files)
        for raw in data.get("invalid_windows", []):
            manifest.invalid_windows.append(InvalidWindow.from_dict(raw))
        return manifest

    def save(self, path: Path) -> None:
        """Write the manifest as JSON to ``path``.

        Caller-controlled path only. Phase 4aw tests use pytest
        ``tmp_path``. Refuses to overwrite an existing file.
        """
        if not isinstance(path, Path):
            raise TypeError("path must be a pathlib.Path")
        if path.exists():
            raise ManifestImmutableError(
                f"refusing to overwrite existing manifest at {path}"
            )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> MicrostructureManifest:
        """Load a manifest from ``path`` (caller-provided)."""
        if not isinstance(path, Path):
            raise TypeError("path must be a pathlib.Path")
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))
