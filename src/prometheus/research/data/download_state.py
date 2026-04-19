"""Persistent state for resumable bulk downloads.

One :class:`DownloadState` file per ``(dataset_name)`` under
``data/manifests/_downloads/<dataset_name>__state.json``. The state
tracks per-month progress through the download/verify/extract/normalize
pipeline so interrupted runs can resume cheaply and idempotently.

Writes are atomic via ``<path>.partial`` + rename. Unlike the
:class:`DatasetManifest`, the download-state file is mutable; every
successful transition rewrites it.
"""

from __future__ import annotations

import json
import os
from enum import StrEnum
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from prometheus.core.errors import PrometheusError


class DownloadStatus(StrEnum):
    """Lifecycle of a single month's download + ingest."""

    PENDING = "PENDING"
    DOWNLOADING = "DOWNLOADING"
    DOWNLOADED = "DOWNLOADED"
    VERIFYING = "VERIFYING"
    VERIFIED = "VERIFIED"
    EXTRACTING = "EXTRACTING"
    EXTRACTED = "EXTRACTED"
    NORMALIZING = "NORMALIZING"
    NORMALIZED = "NORMALIZED"
    FAILED_DOWNLOAD = "FAILED_DOWNLOAD"
    FAILED_CHECKSUM = "FAILED_CHECKSUM"
    FAILED_EXTRACT = "FAILED_EXTRACT"
    FAILED_NORMALIZE = "FAILED_NORMALIZE"


class DownloadStateError(PrometheusError):
    """Raised when the download-state file is malformed or inconsistent."""


def _to_status(value: object) -> object:
    if isinstance(value, str):
        return DownloadStatus(value)
    return value


_Status = Annotated[DownloadStatus, BeforeValidator(_to_status)]


class MonthDownloadState(BaseModel):
    """Per-month progress record.

    Keys are set lazily as the month moves through the lifecycle. A
    month in ``NORMALIZED`` state carries every field populated; a
    month in ``PENDING`` carries only ``status``.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    status: _Status
    zip_sha256: str | None = None
    downloaded_at_utc_ms: int | None = None
    verified_at_utc_ms: int | None = None
    normalized_at_utc_ms: int | None = None
    raw_path: str | None = None
    normalized_path: str | None = None
    row_count: int | None = None
    last_error: str | None = None


class DownloadState(BaseModel):
    """Root download-state document for a single dataset."""

    model_config = ConfigDict(strict=True, extra="forbid")

    dataset_name: str = Field(min_length=1)
    schema_version: str = Field(default="download_state_v1", min_length=1)
    last_updated_utc_ms: int
    months: dict[str, MonthDownloadState]

    def with_month(
        self, year: int, month: int, state: MonthDownloadState, now_ms: int
    ) -> DownloadState:
        """Return a new :class:`DownloadState` with one month replaced."""
        key = f"{year:04d}-{month:02d}"
        new_months = dict(self.months)
        new_months[key] = state
        return DownloadState(
            dataset_name=self.dataset_name,
            schema_version=self.schema_version,
            last_updated_utc_ms=now_ms,
            months=new_months,
        )

    def status_for(self, year: int, month: int) -> DownloadStatus:
        key = f"{year:04d}-{month:02d}"
        record = self.months.get(key)
        return record.status if record else DownloadStatus.PENDING


def read_state(path: Path) -> DownloadState:
    """Load a download-state file from JSON.

    If the file does not exist, raises :class:`FileNotFoundError`;
    callers typically use :func:`read_or_init_state` instead.
    """
    if not path.is_file():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise DownloadStateError(f"state file is not valid JSON: {path}") from exc
    return DownloadState.model_validate(payload)


def read_or_init_state(path: Path, dataset_name: str, now_ms: int) -> DownloadState:
    """Load an existing state file or return a fresh one for ``dataset_name``."""
    if path.is_file():
        loaded = read_state(path)
        if loaded.dataset_name != dataset_name:
            raise DownloadStateError(
                f"state file dataset_name mismatch: expected {dataset_name!r}, "
                f"got {loaded.dataset_name!r} at {path}"
            )
        return loaded
    return DownloadState(
        dataset_name=dataset_name,
        last_updated_utc_ms=now_ms,
        months={},
    )


def write_state(path: Path, state: DownloadState) -> None:
    """Write the state file atomically via ``.partial`` + rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = state.model_dump(mode="json")
    partial = path.with_suffix(path.suffix + ".partial")
    partial.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(partial, path)
