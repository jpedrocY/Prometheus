"""Risk-engine skeletons for the Phase 4a local safe runtime foundation.

Phase 4a implements three risk skeletons:

- ``sizing`` — local risk-sizing calculation only (no order placement;
  no live notional decision).
- ``exposure`` — local/fake exposure gates only (one-symbol-only live
  lock; one-position max; no pyramiding; no reversal).
- ``stop_validation`` — local stop validation only (must enforce the
  Phase 3v `stop_trigger_domain` label scheme; no real placement; no
  Binance calls).

All three modules are deliberately strategy-agnostic. They consume
test fixtures and synthetic inputs only; they do NOT fetch live
account equity, do NOT query a real exchange, and do NOT place orders.
"""

from __future__ import annotations

from .errors import (
    ExposureGateError,
    MissingMetadataError,
    RiskError,
    SizingError,
    StopValidationError,
)
from .exposure import (
    ExposureDecision,
    ExposureSnapshot,
    PositionSide,
    evaluate_entry_candidate,
)
from .sizing import (
    LOCKED_LIVE_LEVERAGE_CAP,
    LOCKED_LIVE_RISK_FRACTION,
    SizingInputs,
    SizingResult,
    compute_sizing,
)
from .stop_validation import (
    StopRequest,
    StopUpdateRequest,
    validate_initial_stop,
    validate_stop_update,
)

__all__ = [
    "LOCKED_LIVE_LEVERAGE_CAP",
    "LOCKED_LIVE_RISK_FRACTION",
    "ExposureDecision",
    "ExposureGateError",
    "ExposureSnapshot",
    "MissingMetadataError",
    "PositionSide",
    "RiskError",
    "SizingError",
    "SizingInputs",
    "SizingResult",
    "StopRequest",
    "StopUpdateRequest",
    "StopValidationError",
    "compute_sizing",
    "evaluate_entry_candidate",
    "validate_initial_stop",
    "validate_stop_update",
]
