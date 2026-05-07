"""Public-only microstructure raw event writer primitive.

Phase 4aw scaffold-only. Atomic write-then-rename, paired SHA256
finalization, no overwrite, no project data writes.

The writer accepts a caller-provided ``root_dir``. The Phase 4aw
scaffold deliberately rejects any path that resolves under the
project ``data/microstructure/`` tree, because that tree is gitignored
but must remain empty until a separately authorized future phase
implements collectors. Tests use pytest ``tmp_path``.

Design choices:

- JSONL records (one JSON object per line) without compression.
  Phase 4au / 4av called for ``.jsonl.zst``; zstandard is not in the
  project's current dependency set, so the scaffold uses uncompressed
  JSONL and documents zstd compression as future work in the Phase
  4aw memo. Adding zstd later is an additive change.
- Append-only writes go to a ``.tmp`` sibling next to the target.
- ``close()`` finalizes by computing SHA256 over the bytes on disk,
  renaming ``<target>.tmp`` to ``<target>`` atomically, and writing
  ``<target>.sha256`` next to it.
- Refuses to overwrite an existing final file.
- Detects a stale ``.tmp`` companion on construction; the caller
  must explicitly delete it before retrying.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Any

# Forbidden absolute or relative path fragments. The scaffold must not
# write under the project's reserved microstructure data tree.
_FORBIDDEN_PATH_FRAGMENTS: tuple[str, ...] = (
    "data/microstructure",
    "data\\microstructure",
)


class RawWriterError(RuntimeError):
    """Base error for raw-writer scaffold failures."""


class RawWriterPathError(RawWriterError):
    """Raised when a path is rejected by scaffold safety checks."""


class RawWriterAlreadyExistsError(RawWriterError):
    """Raised when a final target path already exists."""


@dataclass(frozen=True)
class RawWriterFileSummary:
    """Summary returned by :meth:`RawWriter.close`.

    Intended to be consumed later by manifest construction code, but
    Phase 4aw does NOT couple this directly to manifest mutation —
    callers must explicitly translate this into a ``FileEntry``.
    """

    path: str
    sha256: str
    event_count: int
    start_time_ms: int
    end_time_ms: int


class RawWriter:
    """Append-only JSONL raw event writer with atomic finalization.

    Usage::

        writer = RawWriter(target_path)
        writer.append({"event_time_ms": 1, ...})
        summary = writer.close()
    """

    def __init__(self, target_path: Path) -> None:
        if not isinstance(target_path, Path):
            raise RawWriterPathError("target_path must be a pathlib.Path")
        if target_path.is_dir():
            raise RawWriterPathError(f"target_path must not be a directory: {target_path}")
        _reject_project_data_path(target_path)

        self._target_path = target_path
        self._tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
        self._sha_path = target_path.with_suffix(target_path.suffix + ".sha256")

        if target_path.exists():
            raise RawWriterAlreadyExistsError(
                f"refusing to overwrite existing target {target_path}"
            )
        if self._tmp_path.exists():
            raise RawWriterAlreadyExistsError(
                f"stale .tmp companion exists at {self._tmp_path}; "
                "remove it explicitly before reopening"
            )

        target_path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self._tmp_path.open("wb")
        self._closed = False
        self._event_count = 0
        self._start_time_ms: int | None = None
        self._end_time_ms: int | None = None

    def append(self, record: dict[str, Any]) -> None:
        """Append one JSON-serializable record.

        ``event_time_ms`` (int) is required and is used to track the
        start/end bounds reported in the close summary.
        """
        if self._closed:
            raise RawWriterError("writer is closed")
        if not isinstance(record, dict):
            raise RawWriterError("record must be a dict")
        if "event_time_ms" not in record:
            raise RawWriterError("record must include event_time_ms")
        event_time = record["event_time_ms"]
        if not isinstance(event_time, int) or isinstance(event_time, bool):
            raise RawWriterError("event_time_ms must be an int")

        line = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        self._fh.write(line)
        self._event_count += 1
        if self._start_time_ms is None or event_time < self._start_time_ms:
            self._start_time_ms = event_time
        if self._end_time_ms is None or event_time > self._end_time_ms:
            self._end_time_ms = event_time

    def close(self) -> RawWriterFileSummary:
        """Atomically finalize the file and emit the summary.

        Steps:

        1. Flush + fsync the ``.tmp`` file.
        2. Compute SHA256 by re-reading the ``.tmp`` bytes.
        3. Refuse if the final target already exists.
        4. Rename ``<target>.tmp`` to ``<target>`` (``Path.replace``).
        5. Write ``<target>.sha256`` containing the digest hex.
        """
        if self._closed:
            raise RawWriterError("writer already closed")
        self._fh.flush()
        # fsync may not be supported on every platform/test fixture.
        # The scaffold tolerates this; future production capture can
        # require fsync explicitly.
        with contextlib.suppress(OSError, AttributeError):
            os.fsync(self._fh.fileno())
        self._fh.close()
        self._closed = True

        digest = _sha256_file(self._tmp_path)

        if self._target_path.exists():
            # An overwrite race was reached only if something else created
            # the target between __init__ and close. Refuse and leave the
            # .tmp file in place for operator inspection.
            raise RawWriterAlreadyExistsError(
                f"final target appeared during write: {self._target_path}"
            )

        self._tmp_path.replace(self._target_path)
        self._sha_path.write_text(f"{digest}  {self._target_path.name}\n", encoding="utf-8")

        return RawWriterFileSummary(
            path=str(self._target_path),
            sha256=digest,
            event_count=self._event_count,
            start_time_ms=self._start_time_ms or 0,
            end_time_ms=self._end_time_ms or 0,
        )

    def __enter__(self) -> RawWriter:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not self._closed:
            with contextlib.suppress(Exception):
                self._fh.close()


def _reject_project_data_path(target_path: Path) -> None:
    """Reject any path that resolves under project ``data/microstructure``.

    The check is conservative: it inspects both the literal path string
    and the resolved absolute form. Tests that pass pytest ``tmp_path``
    pass through untouched.
    """
    candidates = (str(target_path), str(target_path.resolve()))
    for candidate in candidates:
        normalized = candidate.replace("\\", "/").lower()
        for fragment in _FORBIDDEN_PATH_FRAGMENTS:
            normalized_fragment = fragment.replace("\\", "/").lower()
            if normalized_fragment in normalized:
                raise RawWriterPathError(
                    f"target_path {target_path!r} resolves under the reserved "
                    "data/microstructure tree; the Phase 4aw scaffold may not "
                    "write under project data paths"
                )


def _sha256_file(path: Path) -> str:
    """Compute SHA256 hex digest of ``path``."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65_536), b""):
            h.update(chunk)
    return h.hexdigest()
