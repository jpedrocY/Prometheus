"""Local/fake exposure-gate skeleton.

Implements `docs/07-risk/exposure-limits.md` §Locked V1 Exposure Rules
1–10 against an explicit ``ExposureSnapshot`` (fake-position state
only — Phase 4a does not query a real exchange).

Rules enforced:

- Rule 1: BTCUSDT only — non-BTCUSDT live entry rejects.
- Rule 2: One position maximum — any existing strategy-owned position
  blocks new entries.
- Rule 3: No pyramiding — same-direction entry while positioned
  rejects.
- Rule 4: No reversal entry while positioned — opposite-direction
  entry while positioned rejects.
- Rule 7 (partial): Entry-in-flight — if an entry is in flight,
  new entries are blocked.
- Rule 9 (partial): Missing protection — if a position exists without
  confirmed protection, all new entries are blocked.
- Manual / non-bot exposure — if external exposure is detected,
  blocks new bot entries.

The gate operates on a pure ``ExposureSnapshot`` value object. The
runtime layer is responsible for constructing the snapshot from
fake-adapter state in Phase 4a; live-exchange-derived snapshots are
out of scope for Phase 4a per Phase 3x §6.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from prometheus.core.symbols import Symbol

from .errors import ExposureGateError


class PositionSide(StrEnum):
    """Side of a fake or candidate position."""

    LONG = "long"
    SHORT = "short"


class ExposureSnapshot(BaseModel):
    """Frozen snapshot of fake exposure state at a decision instant.

    Phase 4a's strategy-agnostic framing: this snapshot represents
    fake-adapter state, not real exchange state. In a future Phase
    that includes live capability, an analogous snapshot would be
    constructed from exchange-authoritative data.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    symbol: Symbol
    has_position: bool
    position_side: PositionSide | None = None
    protection_confirmed: bool
    entry_in_flight: bool
    manual_or_non_bot_exposure: bool


class ExposureDecision(BaseModel):
    """Result of an exposure-gate evaluation."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    allowed: bool
    reason: str


def evaluate_entry_candidate(
    *,
    candidate_symbol: Symbol,
    candidate_side: PositionSide,
    snapshot: ExposureSnapshot,
    live_symbol: Symbol = Symbol.BTCUSDT,
) -> ExposureDecision:
    """Return an ``ExposureDecision`` for a candidate entry.

    The function does NOT raise for "blocked" outcomes; it returns a
    structured decision so callers can record the reason on the audit
    log. Truly invalid inputs (e.g., snapshot inconsistencies) raise
    ``ExposureGateError``.
    """
    if snapshot.has_position and snapshot.position_side is None:
        raise ExposureGateError(
            "snapshot has_position is True but position_side is None"
        )
    if snapshot.symbol != candidate_symbol:
        raise ExposureGateError(
            f"snapshot symbol {snapshot.symbol} does not match "
            f"candidate symbol {candidate_symbol}"
        )

    # Rule 1 — BTCUSDT only for live (Phase 4a uses BTCUSDT as the
    # default live symbol; ETHUSDT is research/comparison only).
    if candidate_symbol != live_symbol:
        return ExposureDecision(
            allowed=False,
            reason=f"Rule 1: live entry restricted to {live_symbol}",
        )

    # Manual / non-bot exposure blocks new bot entries.
    if snapshot.manual_or_non_bot_exposure:
        return ExposureDecision(
            allowed=False,
            reason="manual or non-bot exposure detected; blocking new bot entries",
        )

    # Rule 7 (partial) — entry in flight blocks new entries.
    if snapshot.entry_in_flight:
        return ExposureDecision(
            allowed=False,
            reason="Rule 7: entry-in-flight blocks new exposure",
        )

    if snapshot.has_position:
        # Rule 9 (partial) — position without confirmed protection
        # blocks all new entries.
        if not snapshot.protection_confirmed:
            return ExposureDecision(
                allowed=False,
                reason="Rule 9: position exists without confirmed protection",
            )

        # Rule 3 — no pyramiding (same-direction).
        if snapshot.position_side == candidate_side:
            return ExposureDecision(
                allowed=False,
                reason="Rule 3: no pyramiding (same-direction entry while positioned)",
            )

        # Rule 4 — no reversal entry while positioned.
        if snapshot.position_side != candidate_side:
            return ExposureDecision(
                allowed=False,
                reason="Rule 4: no reversal entry while positioned",
            )

        # Rule 2 — one position maximum (catch-all if neither
        # pyramiding nor reversal applied; e.g., side mapping changed).
        return ExposureDecision(
            allowed=False,
            reason="Rule 2: one position maximum; existing position blocks entry",
        )

    return ExposureDecision(allowed=True, reason="exposure gates pass")
