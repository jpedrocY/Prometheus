"""Local SQLite persistence for restart-critical runtime control state.

Per `docs/08-architecture/database-design.md` §Recommended V1 Database
Engine: SQLite + WAL is acceptable for v1's "single live writer,
single dedicated NUC" model. Phase 4a uses local SQLite only with
strict configuration:

- ``journal_mode = WAL``,
- ``foreign_keys = ON``,
- ``synchronous = FULL`` (durability over throughput; v1 is low-rate),
- ``busy_timeout`` configured.

Phase 4a does NOT introduce remote database support. Phase 4a does NOT
persist secrets in any table. Phase 4a does NOT auto-resume a
persisted ``RUNNING`` mode on restart — startup always enters
SAFE_MODE per `state.fresh_control_state` regardless of last
persisted mode (per Phase 3x §9.2 / `state-model.md` §Startup rule).

Per Phase 3v §9 / Phase 3w §9: persisted records carry the four
governance labels as first-class fields where governed semantics
apply. ``mixed_or_unknown`` fails closed at the persistence boundary
via ``prometheus.core.governance.require_valid``.
"""

from __future__ import annotations

from .runtime_store import (
    RuntimeStore,
    RuntimeStoreError,
)

__all__ = [
    "RuntimeStore",
    "RuntimeStoreError",
]
