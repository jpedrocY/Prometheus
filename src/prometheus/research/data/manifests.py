"""Dataset manifest model and JSON I/O.

Mirrors docs/04-data/dataset-versioning.md. Manifests are immutable once
written: ``write_manifest`` refuses to overwrite an existing file and
raises :class:`ManifestError`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

from prometheus.core.errors import ManifestError
from prometheus.core.intervals import Interval
from prometheus.core.symbols import Symbol

_VERSION_PATTERN = re.compile(r"^[a-z0-9_]+__v\d{3,}$")


def _as_tuple(value: object) -> object:
    """Coerce list -> tuple so JSON round-trips work under strict mode."""
    if isinstance(value, list):
        return tuple(value)
    return value


def _as_symbol_tuple(value: object) -> object:
    """Coerce to tuple[Symbol, ...], converting string elements from JSON."""
    if isinstance(value, list | tuple):
        return tuple(Symbol(v) if isinstance(v, str) else v for v in value)
    return value


def _as_interval_tuple(value: object) -> object:
    """Coerce to tuple[Interval, ...], converting string elements from JSON."""
    if isinstance(value, list | tuple):
        return tuple(Interval(v) if isinstance(v, str) else v for v in value)
    return value


_SymbolTuple = Annotated[tuple[Symbol, ...], BeforeValidator(_as_symbol_tuple)]
_IntervalTuple = Annotated[tuple[Interval, ...], BeforeValidator(_as_interval_tuple)]
_StringTuple = Annotated[tuple[str, ...], BeforeValidator(_as_tuple)]


class InvalidWindow(BaseModel):
    """A contiguous range of missing or unusable bars for a dataset."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    start_open_time_ms: int
    end_open_time_ms: int
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_range(self) -> InvalidWindow:
        if self.end_open_time_ms < self.start_open_time_ms:
            raise ValueError("end_open_time_ms must be >= start_open_time_ms")
        return self


class DatasetManifest(BaseModel):
    """Metadata describing a published dataset version.

    Required fields per docs/04-data/dataset-versioning.md. Dataset
    versions follow the pattern ``<dataset_name>__v<NNN>``.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    dataset_name: str = Field(min_length=1)
    dataset_version: str
    dataset_category: str = Field(min_length=1)
    created_at_utc_ms: int
    canonical_timezone: Literal["UTC"]
    canonical_timestamp_format: Literal["unix_milliseconds"]
    symbols: _SymbolTuple
    intervals: _IntervalTuple
    sources: _StringTuple
    schema_version: str = Field(min_length=1)
    pipeline_version: str = Field(min_length=1)
    partitioning: _StringTuple
    primary_key: _StringTuple
    generator: str = Field(min_length=1)
    predecessor_version: str | None
    invalid_windows: Annotated[tuple[InvalidWindow, ...], BeforeValidator(_as_tuple)]
    notes: str

    @model_validator(mode="after")
    def _validate(self) -> DatasetManifest:
        if not _VERSION_PATTERN.fullmatch(self.dataset_version):
            raise ValueError(
                f"dataset_version {self.dataset_version!r} must match <dataset_name>__v<NNN>"
            )
        if not self.dataset_version.startswith(f"{self.dataset_name}__v"):
            raise ValueError(
                f"dataset_version {self.dataset_version!r} must start with {self.dataset_name}__v"
            )
        if self.created_at_utc_ms <= 0:
            raise ValueError("created_at_utc_ms must be positive")
        if len(self.symbols) == 0:
            raise ValueError("symbols must not be empty")
        if self.predecessor_version is not None:
            if not _VERSION_PATTERN.fullmatch(self.predecessor_version):
                raise ValueError(
                    f"predecessor_version {self.predecessor_version!r} "
                    f"must match <dataset_name>__v<NNN>"
                )
            if self.predecessor_version == self.dataset_version:
                raise ValueError("predecessor_version must differ from dataset_version")
        return self


def read_manifest(path: Path) -> DatasetManifest:
    """Load a dataset manifest from JSON."""
    if not path.is_file():
        raise ManifestError(f"manifest not found: {path}")
    text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    return DatasetManifest.model_validate(payload)


def write_manifest(path: Path, manifest: DatasetManifest) -> None:
    """Write a manifest as JSON. Refuses to overwrite an existing file."""
    if path.exists():
        raise ManifestError(f"manifest already exists and cannot be overwritten: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = manifest.model_dump(mode="json")
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
