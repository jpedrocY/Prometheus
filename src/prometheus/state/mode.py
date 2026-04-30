"""Runtime mode enum.

Per `docs/08-architecture/state-model.md` §Top-Level Runtime Modes,
the runtime uses a small set of primary modes. Phase 4a implements
the strategy-agnostic subset:

- ``SAFE_MODE``: startup default; entries blocked; only safety,
  verification, reconciliation, recovery, cancellation, protection,
  or flattening actions are allowed.
- ``RUNNING``: entries are allowed if other gates also permit them.
  In Phase 4a's strategy-agnostic context this is "the runtime is
  willing to accept fake decisions"; no real strategy is wired in.
- ``BLOCKED``: a blocking control flag (kill switch / pause /
  operator review required) prevents normal progression.
- ``EMERGENCY``: an emergency condition (e.g., position without
  confirmed protection) is active.
- ``RECOVERY_REQUIRED``: reconciliation or restart recovery must
  complete before normal continuation.

Phase 4a's startup rule (per Phase 3x §9.1 / state-model.md §Startup
rule): on every process start, enter ``SAFE_MODE`` regardless of the
prior persisted mode.
"""

from __future__ import annotations

from enum import StrEnum


class RuntimeMode(StrEnum):
    """Top-level runtime mode."""

    SAFE_MODE = "SAFE_MODE"
    RUNNING = "RUNNING"
    BLOCKED = "BLOCKED"
    EMERGENCY = "EMERGENCY"
    RECOVERY_REQUIRED = "RECOVERY_REQUIRED"
