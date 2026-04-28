"""Backtest configuration model.

All parameters the engine needs to run. Defaults reflect operator
decisions recorded at Phase 3 Gate 1 (GAP-014 through GAP-023 in
docs/00-meta/implementation-ambiguity-log.md).

Phase 3 restriction: ``adapter`` is ``BacktestAdapter.FAKE`` only.
The enum has no live value. Any later live execution layer must be
introduced through a phase-gate-approved phase that adds a new
adapter type, not by mutating this enum.
"""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from prometheus.core.symbols import Symbol
from prometheus.strategy.mean_reversion_overextension.variant_config import MeanReversionConfig
from prometheus.strategy.v1_breakout.variant_config import V1BreakoutConfig


class StrategyFamily(StrEnum):
    """Selects the strategy family the backtest engine dispatches to.

    V1_BREAKOUT (default) is the locked Phase 2e family with the H0/R3/
    R1a/R1b-narrow/R2 axes. MEAN_REVERSION_OVEREXTENSION is the F1
    family from Phase 3b §4. Phase 3d-B1 wires the engine dispatch:
    selecting MEAN_REVERSION_OVEREXTENSION requires
    ``mean_reversion_variant`` to be a non-None ``MeanReversionConfig``
    and forbids passing ``strategy_variant`` overrides on top of the
    V1 default. F1 candidate execution itself is reserved for Phase 3d-B2;
    Phase 3d-B1 only proves the dispatch surface and engine path exist
    without changing V1 H0/R3 behavior.
    """

    V1_BREAKOUT = "V1_BREAKOUT"
    MEAN_REVERSION_OVEREXTENSION = "MEAN_REVERSION_OVEREXTENSION"


class BacktestAdapter(StrEnum):
    """Phase-3 allowed adapters. FAKE is the only value in Phase 3."""

    FAKE = "FAKE"


class SlippageBucket(StrEnum):
    """Labeled slippage tier. Actual bps values live in BacktestConfig."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class StopTriggerSource(StrEnum):
    """Which price stream evaluates protective-stop hits.

    MARK_PRICE matches the live protective-stop configuration
    (workingType=MARK_PRICE) and is the default. TRADE_PRICE is a
    research-only sensitivity switch introduced in Phase 2g to
    quantify how stop-trigger choice affects reported performance
    (GAP-20260424-032).
    """

    MARK_PRICE = "MARK_PRICE"
    TRADE_PRICE = "TRADE_PRICE"


# Default slippage bps per bucket (one side of the trade).
# Round-trip slippage is 2x per-side because entry + exit both slip
# adversely. The caller can override via ``BacktestConfig.slippage_bps_map``.
DEFAULT_SLIPPAGE_BPS: dict[SlippageBucket, float] = {
    SlippageBucket.LOW: 1.0,
    SlippageBucket.MEDIUM: 3.0,
    SlippageBucket.HIGH: 8.0,
}


class BacktestConfig(BaseModel):
    """All parameters the backtester needs.

    See Phase 3 Gate 1 plan §10 and operator decisions logged in
    ``docs/00-meta/implementation-ambiguity-log.md`` GAP-014..GAP-023.
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    experiment_name: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    symbols: tuple[Symbol, ...] = Field(min_length=1)

    # Simulation window: start_ms is inclusive, end_ms is exclusive.
    window_start_ms: int = Field(gt=0)
    window_end_ms: int = Field(gt=0)

    # Sizing
    sizing_equity_usdt: float = Field(gt=0)  # R1: default 10_000
    risk_fraction: float = Field(gt=0, lt=1)  # R4: default 0.0025
    risk_usage_fraction: float = Field(gt=0, le=1)  # R2: default 0.90
    max_effective_leverage: float = Field(gt=0)  # default 2.0
    max_notional_internal_usdt: float = Field(gt=0)  # R3: default 100_000

    # Costs
    taker_fee_rate: float = Field(gt=0, lt=1)  # A5 primary: 0.0005
    slippage_bucket: SlippageBucket
    slippage_bps_map: dict[SlippageBucket, float] = Field(
        default_factory=lambda: dict(DEFAULT_SLIPPAGE_BPS)
    )

    # Data roots (absolute or relative to cwd at run time). Engine
    # resolves and reads Parquet/JSON under these.
    klines_root: Path
    mark_price_root: Path
    funding_root: Path
    bars_1h_root: Path
    exchange_info_path: Path

    # Output location (engine creates subdir <experiment_name>/<run_id>/).
    reports_root: Path

    # Adapter is FAKE-only in Phase 3.
    adapter: BacktestAdapter = BacktestAdapter.FAKE

    # Strategy family dispatch. Default = V1_BREAKOUT preserves all
    # existing behavior bit-for-bit. MEAN_REVERSION_OVEREXTENSION is
    # the F1 family per Phase 3b §4; Phase 3d-B1 lifts the
    # implementation guard to allow engine dispatch when the
    # ``mean_reversion_variant`` field is also supplied.
    strategy_family: StrategyFamily = StrategyFamily.V1_BREAKOUT

    # Strategy variant overrides. Default = locked Phase 2e baseline (H0).
    # Phase 2g wave-1 sets exactly one field per variant.
    strategy_variant: V1BreakoutConfig = Field(default_factory=V1BreakoutConfig)

    # F1 mean-reversion-after-overextension variant. Phase 3d-B1: the
    # engine routes per-bar evaluation to the F1 path when
    # ``strategy_family == MEAN_REVERSION_OVEREXTENSION`` AND this
    # field is a non-None ``MeanReversionConfig``. The validator below
    # enforces the dispatch invariants.
    mean_reversion_variant: MeanReversionConfig | None = None

    # Which price stream evaluates stops. MARK_PRICE (default) mirrors
    # the live protective-stop workingType; TRADE_PRICE is a Phase 2g
    # sensitivity switch (GAP-20260424-032).
    stop_trigger_source: StopTriggerSource = StopTriggerSource.MARK_PRICE

    @model_validator(mode="after")
    def _check(self) -> BacktestConfig:
        if self.window_end_ms <= self.window_start_ms:
            raise ValueError("window_end_ms must be > window_start_ms")
        if self.adapter != BacktestAdapter.FAKE:
            raise ValueError("Phase 3 only supports BacktestAdapter.FAKE")
        if self.risk_fraction > 0.05:
            # Research sensitivity allows up to 2% per sizing framework;
            # hard reject values above 5% as a sanity floor to catch
            # config typos.
            raise ValueError(f"risk_fraction {self.risk_fraction} exceeds 5% sanity cap")
        if self.max_effective_leverage > 10.0:
            raise ValueError(
                f"max_effective_leverage {self.max_effective_leverage} exceeds 10x sanity cap"
            )
        # Ensure every bucket has a bps value.
        for bucket in SlippageBucket:
            if bucket not in self.slippage_bps_map:
                raise ValueError(f"slippage_bps_map missing bucket {bucket}")
        # Strategy-family dispatch invariants (Phase 3d-B1).
        if self.strategy_family == StrategyFamily.V1_BREAKOUT:
            if self.mean_reversion_variant is not None:
                raise ValueError(
                    "mean_reversion_variant must be None when strategy_family=V1_BREAKOUT"
                )
        elif self.strategy_family == StrategyFamily.MEAN_REVERSION_OVEREXTENSION:
            if self.mean_reversion_variant is None:
                raise ValueError(
                    "mean_reversion_variant must be a MeanReversionConfig when "
                    "strategy_family=MEAN_REVERSION_OVEREXTENSION"
                )
            # Disallow non-default V1 strategy_variant overrides on the F1
            # path. F1 does not consume ``strategy_variant``; allowing
            # non-default V1 axes alongside F1 would suggest mixed-family
            # behavior that the engine does not implement.
            default_v1 = V1BreakoutConfig()
            if self.strategy_variant != default_v1:
                raise ValueError(
                    "strategy_variant must be the V1BreakoutConfig default when "
                    "strategy_family=MEAN_REVERSION_OVEREXTENSION; F1 does not "
                    "consume V1 axes"
                )
        return self

    @property
    def slippage_bps(self) -> float:
        """Return the active bucket's bps value."""
        return self.slippage_bps_map[self.slippage_bucket]
