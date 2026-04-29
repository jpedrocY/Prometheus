"""Main backtest engine: bar-by-bar loop that drives the v1 breakout strategy.

The engine owns:
    - ingest of completed 15m / 1h / mark-price / funding inputs
    - per-bar cursor advancement
    - signal -> size -> fill -> stop-check -> management -> exit
    - trade-record emission
    - end-of-run accounting

The engine does NOT:
    - read the Binance API
    - place live orders
    - persist anything besides its Parquet / JSON outputs
    - mutate any file outside its reports_root
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from uuid import uuid4

from prometheus.core.events import FundingRateEvent
from prometheus.core.exchange_info import SymbolInfo
from prometheus.core.klines import NormalizedKline
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol
from prometheus.strategy.funding_aware_directional import (
    FundingAwareStrategy,
    FundingEvent,
)
from prometheus.strategy.funding_aware_directional import (
    can_re_enter as can_re_enter_d1a,
)
from prometheus.strategy.funding_aware_directional import (
    compute_funding_z_score as compute_d1a_z_score,
)
from prometheus.strategy.funding_aware_directional import (
    compute_stop as compute_d1a_stop,
)
from prometheus.strategy.funding_aware_directional import (
    compute_target as compute_d1a_target,
)
from prometheus.strategy.funding_aware_directional import (
    funding_extreme_event as is_funding_extreme,
)
from prometheus.strategy.funding_aware_directional import (
    passes_stop_distance_filter as passes_d1a_stop_distance_filter,
)
from prometheus.strategy.funding_aware_directional import (
    signal_direction as d1a_signal_direction,
)
from prometheus.strategy.indicators import wilder_atr
from prometheus.strategy.mean_reversion_overextension import (
    MeanReversionStrategy,
    can_re_enter,
    overextension_event,
)
from prometheus.strategy.types import (
    Direction,
    EntryIntent,
    ExitIntent,
    ExitReason,
    StopUpdateIntent,
)
from prometheus.strategy.v1_breakout import (
    R2_VALIDITY_WINDOW_BARS,
    EntryKind,
    PendingCandidate,
    PendingEvaluation,
    StrategySession,
    V1BreakoutStrategy,
    evaluate_fill_at_next_bar_open,
    evaluate_pending_candidate,
)
from prometheus.strategy.v1_breakout.stop import (
    FILTER_MAX_ATR_MULT,
    FILTER_MIN_ATR_MULT,
)

from .accounting import Accounting, TradePnL, compute_trade_pnl
from .config import BacktestConfig, StopTriggerSource, StrategyFamily
from .fills import entry_fill_price, exit_fill_price
from .funding_join import apply_funding_accrual
from .simulation_clock import next_15m_open_time
from .sizing import SizingLimitedBy, compute_size
from .stops import StopHit, evaluate_stop_hit
from .trade_log import TradeRecord


@dataclass
class _R2TradeMetadata:
    """R2-specific provenance for a filled pullback-retest trade.

    Set on ``_OpenTrade`` only when ``entry_kind=PULLBACK_RETEST`` and
    a PendingCandidate has reached READY_TO_FILL → FILL. Under
    H0/R3/R1a/R1b-narrow (entry_kind=MARKET_NEXT_BAR_OPEN), this is
    None and the corresponding ``TradeRecord`` R2 fields default to
    H0-equivalent values per ``trade_log.TradeRecord``.
    """

    registration_bar_index: int
    fill_bar_index: int
    pullback_level_at_registration: float
    structural_stop_level_at_registration: float
    atr_at_signal: float
    fill_price: float


@dataclass
class _F1TradeMetadata:
    """F1 mean-reversion-after-overextension provenance for a filled trade.

    Set on ``_OpenTrade`` only when the engine routes through the
    Phase 3d-B1 F1 dispatch (``strategy_family ==
    MEAN_REVERSION_OVEREXTENSION``). For V1 (H0/R3/R1a/R1b-narrow/R2)
    paths this is None and the corresponding ``TradeRecord`` F1 fields
    default to NaN per ``trade_log.TradeRecord``.

    All values are frozen at signal-time bar B's close per Phase 3b §4
    and Phase 3c §4.6.
    """

    signal_bar_index: int  # B
    fill_bar_index: int  # B+1
    frozen_target: float  # SMA(8)(B)
    atr_at_signal: float  # ATR(20)(B)
    displacement_at_signal: float  # close(B) - close(B-8)
    stop_distance_at_signal: float  # |raw_open(B+1) - initial_stop|
    raw_entry_reference: float  # raw (de-slipped) open(B+1)


@dataclass
class _D1ATradeMetadata:
    """D1-A funding-aware directional / carry-aware provenance for a filled trade.

    Set on ``_OpenTrade`` only when the engine routes through the
    Phase 3i-B1 D1-A dispatch (``strategy_family ==
    FUNDING_AWARE_DIRECTIONAL``). For V1 / F1 paths this is None and
    the corresponding ``TradeRecord`` D1-A fields default to None /
    NaN per ``trade_log.TradeRecord``.

    All values are frozen at signal-time bar B's close per Phase 3g §6
    (with §5.6.5 Option A target +2.0R) and Phase 3h §3 + §6.
    """

    signal_bar_index: int  # B
    fill_bar_index: int  # B+1
    target_price: float  # +2.0R fixed target
    atr_at_signal: float  # ATR(20)(B)
    stop_distance_at_signal: float  # |raw_open(B+1) - initial_stop|
    raw_entry_reference: float  # raw (de-slipped) open(B+1)
    funding_event_id: str  # consumed funding event id (for cooldown)
    funding_time: int  # UTC ms of consumed funding event
    funding_rate: float  # signed funding rate at signal
    funding_z_score: float  # trailing-90-day Z-score at signal
    bars_since_funding_event: int  # bars elapsed at signal-time bar B


@dataclass
class _OpenTrade:
    """Engine-side bookkeeping for a currently open position."""

    symbol: Symbol
    direction_long: bool
    signal_bar_open_time_ms: int
    entry_fill_time_ms: int
    entry_fill_price: float
    initial_stop: float
    stop_distance: float
    quantity: float
    notional: float
    sizing_limited_by: SizingLimitedBy
    realized_risk_usdt: float
    current_stop: float
    stop_was_gap_through: bool = False
    r2_metadata: _R2TradeMetadata | None = None
    f1_metadata: _F1TradeMetadata | None = None
    d1a_metadata: _D1ATradeMetadata | None = None


@dataclass
class R2LifecycleCounters:
    """Per-symbol R2 candidate-lifecycle outcome counts.

    Populated only under ``entry_kind=PULLBACK_RETEST``. Under
    H0 default (MARKET_NEXT_BAR_OPEN) all counters remain 0 and the
    accounting identity holds trivially. Per Phase 2u §J.4 (Gate 2
    amended), the identity is:

        registered = no_pullback + bias_flip + opposite_signal
                   + structural_invalidation + stop_distance_at_fill
                   + filled
    """

    registered: int = 0
    filled: int = 0
    cancelled_bias_flip: int = 0
    cancelled_opposite_signal: int = 0
    cancelled_structural_invalidation: int = 0
    cancelled_stop_distance_at_fill: int = 0
    expired_no_pullback: int = 0

    @property
    def accounting_identity_holds(self) -> bool:
        return self.registered == (
            self.expired_no_pullback
            + self.cancelled_bias_flip
            + self.cancelled_opposite_signal
            + self.cancelled_structural_invalidation
            + self.cancelled_stop_distance_at_fill
            + self.filled
        )


@dataclass
class F1LifecycleCounters:
    """Per-symbol F1 mean-reversion overextension-event funnel counts.

    Populated only under ``strategy_family ==
    MEAN_REVERSION_OVEREXTENSION``. Under the V1 default
    (``V1_BREAKOUT``) all counters remain 0 and the accounting identity
    holds trivially. Per Phase 3b §4 / Phase 3c §4.7 the identity is:

        detected = filled
                 + rejected_stop_distance
                 + blocked_cooldown

    Each detected overextension event is attributed to exactly one
    bucket: cooldown is checked first; on cooldown block the event is
    counted in ``overextension_events_blocked_cooldown``; otherwise
    stop-distance admissibility is checked and either fills the trade
    or counts in ``overextension_events_rejected_stop_distance``.
    """

    overextension_events_detected: int = 0
    overextension_events_filled: int = 0
    overextension_events_rejected_stop_distance: int = 0
    overextension_events_blocked_cooldown: int = 0

    @property
    def accounting_identity_holds(self) -> bool:
        return self.overextension_events_detected == (
            self.overextension_events_filled
            + self.overextension_events_rejected_stop_distance
            + self.overextension_events_blocked_cooldown
        )


@dataclass
class FundingAwareLifecycleCounters:
    """Per-symbol D1-A funding-extreme-event funnel counts.

    Populated only under ``strategy_family ==
    FUNDING_AWARE_DIRECTIONAL``. Under V1 default or F1 dispatch all
    counters remain 0 and the accounting identity holds trivially.
    Per Phase 3g §9.4 (first amendment) / Phase 3h §5.8 the identity
    is event-level, not bar-level:

        funding_extreme_events_detected
        = funding_extreme_events_filled
        + funding_extreme_events_rejected_stop_distance
        + funding_extreme_events_blocked_cooldown

    Each detected funding extreme event (|Z_F| >= 2.0) is attributed
    to exactly one bucket. Repeated 15m bars referencing the same
    ``funding_event_id`` must NOT inflate ``funding_extreme_events_detected``.
    The engine enforces this by tracking the last-processed event id
    per symbol and only invoking funnel bookkeeping on first-encounter
    of each fresh event id.
    """

    funding_extreme_events_detected: int = 0
    funding_extreme_events_filled: int = 0
    funding_extreme_events_rejected_stop_distance: int = 0
    funding_extreme_events_blocked_cooldown: int = 0

    @property
    def accounting_identity_holds(self) -> bool:
        return self.funding_extreme_events_detected == (
            self.funding_extreme_events_filled
            + self.funding_extreme_events_rejected_stop_distance
            + self.funding_extreme_events_blocked_cooldown
        )


@dataclass
class _SymbolRun:
    symbol: Symbol
    session: StrategySession
    trades: list[TradeRecord] = field(default_factory=list)
    open_trade: _OpenTrade | None = None
    next_trade_id_seq: int = 0
    # Index cursors into per-symbol input streams.
    bar_15m_cursor: int = 0
    bar_1h_cursor: int = 0
    # Mark-price and funding are consumed on-demand via binary search.
    r2_counters: R2LifecycleCounters = field(default_factory=R2LifecycleCounters)
    # Index of the registration bar within klines_15m for the active
    # PendingCandidate, if any. Mirrors session.pending_candidate but
    # used by the engine for fill-bar lookup.
    pending_registration_idx: int | None = None
    # Index of the bar at which a pending candidate became READY_TO_FILL,
    # so the next bar's open is the fill price. None when no fill is
    # pending. Cleared after the fill is recorded.
    pending_fill_at_idx: int | None = None
    # Pre-computed open price at registration_bar_index + 1 (R3
    # "would-have-entered-at" reference for the §P.3 stop-distance
    # reduction diagnostic in 2w-B). Captured at registration.
    pending_next_bar_open_at_signal: float | None = None
    # F1 mean-reversion-after-overextension per-symbol state
    # (Phase 3d-B1). All zero / None for V1 paths.
    f1_counters: F1LifecycleCounters = field(default_factory=F1LifecycleCounters)
    f1_last_exit_direction: Direction | None = None
    f1_last_exit_idx: int | None = None
    # D1-A funding-aware directional per-symbol state (Phase 3i-B1).
    # All zero / None for V1 / F1 paths.
    d1a_counters: FundingAwareLifecycleCounters = field(
        default_factory=FundingAwareLifecycleCounters
    )
    # Track the last funding event id we've evaluated to prevent
    # repeated 15m bars referencing the same event from inflating the
    # event-level "detected" counter (Phase 3g §9.4 amended; Phase 3h
    # §14 P.14 invariant 5).
    d1a_last_processed_event_id: str | None = None
    # Per-direction cooldown bookkeeping. After a position closes, the
    # event id that triggered it is recorded here so same-direction
    # re-entries on that same event are blocked per Phase 3g §6.10.
    # Opposite-direction re-entries are never blocked at the event
    # level.
    d1a_last_consumed_event_id: str | None = None
    d1a_last_consumed_direction: Direction | None = None


@dataclass
class BacktestRunResult:
    """Aggregate outputs of a single backtest run."""

    config: BacktestConfig
    per_symbol_trades: dict[Symbol, list[TradeRecord]]
    accounting_per_symbol: dict[Symbol, Accounting]
    warnings: list[str]
    # R2 candidate-lifecycle counters per symbol. All zero for non-R2
    # paths (entry_kind=MARKET_NEXT_BAR_OPEN). 2w-B reporting consumes
    # these to populate the §P.1 fill-rate diagnostic.
    r2_counters_per_symbol: dict[Symbol, R2LifecycleCounters] = field(default_factory=dict)
    # F1 overextension-event funnel counters per symbol. All zero for
    # V1 paths (strategy_family=V1_BREAKOUT). Phase 3d-B1 populates
    # these on the F1 dispatch path.
    f1_counters_per_symbol: dict[Symbol, F1LifecycleCounters] = field(default_factory=dict)
    # D1-A funding-extreme-event funnel counters per symbol. All zero
    # for V1 / F1 paths. Phase 3i-B1 populates these on the D1-A
    # dispatch path.
    funding_aware_counters_per_symbol: dict[Symbol, FundingAwareLifecycleCounters] = field(
        default_factory=dict
    )

    @property
    def total_trades(self) -> int:
        return sum(len(t) for t in self.per_symbol_trades.values())


class BacktestEngine:
    """Drives the v1 breakout strategy against historical data for one config.

    Usage::

        engine = BacktestEngine(config)
        result = engine.run(
            klines_15m_per_symbol={BTC: [...], ETH: [...]},
            klines_1h_per_symbol={...},
            mark_15m_per_symbol={...},
            funding_per_symbol={...},
            symbol_info_per_symbol={...},
        )

    Each ``per_symbol`` mapping must provide data covering the
    ``config.window_start_ms .. window_end_ms`` range plus any
    pre-window warmup bars needed for indicator seeding.
    """

    def __init__(
        self,
        config: BacktestConfig,
        *,
        r2_fill_model: str = "next-bar-open-after-confirmation",
    ) -> None:
        """Construct the engine.

        ``r2_fill_model`` is a **runner-script-only** R2 fill-model
        switch per Phase 2v Gate 2 clarification. The committed fill
        model is ``next-bar-open-after-confirmation`` (Phase 2u §F.4)
        and is the only path eligible for §10.3 governing evaluation.
        The diagnostic alternative ``limit-at-pullback-intrabar`` is
        permitted exclusively for the §P.6 fill-model sensitivity
        diagnostic (Phase 2v run #10) and is intentionally NOT a
        ``V1BreakoutConfig`` field — exposing it as a config field
        would invite drift toward sweeps. Outside the runner-script
        invocation that explicitly opts in, the default committed
        path is the only option.

        Allowed values:
          - "next-bar-open-after-confirmation" (committed; default)
          - "limit-at-pullback-intrabar" (diagnostic-only; runner #10)
        """
        if r2_fill_model not in (
            "next-bar-open-after-confirmation",
            "limit-at-pullback-intrabar",
        ):
            raise ValueError(
                f"unsupported r2_fill_model: {r2_fill_model!r}. "
                "Allowed: next-bar-open-after-confirmation (committed; default) "
                "or limit-at-pullback-intrabar (diagnostic-only)."
            )
        self._config = config
        self._strategy = V1BreakoutStrategy(config.strategy_variant)
        # F1 strategy is only constructed when the dispatch surface is
        # set to MEAN_REVERSION_OVEREXTENSION; the V1 path does not
        # consume it. Constructed here once so per-bar evaluation does
        # not allocate.
        self._mean_reversion_strategy: MeanReversionStrategy | None = None
        if (
            config.strategy_family == StrategyFamily.MEAN_REVERSION_OVEREXTENSION
            and config.mean_reversion_variant is not None
        ):
            self._mean_reversion_strategy = MeanReversionStrategy(config.mean_reversion_variant)
        # D1-A funding-aware strategy is constructed only when the
        # dispatch surface is set to FUNDING_AWARE_DIRECTIONAL; V1 / F1
        # paths do not consume it. Phase 3i-B1 wires per-bar evaluation;
        # the BacktestConfig validator enforces that ``funding_aware_variant``
        # is non-None when ``strategy_family == FUNDING_AWARE_DIRECTIONAL``.
        self._funding_aware_strategy: FundingAwareStrategy | None = None
        if (
            config.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL
            and config.funding_aware_variant is not None
        ):
            self._funding_aware_strategy = FundingAwareStrategy(config.funding_aware_variant)
        self._r2_fill_model = r2_fill_model

    def run(
        self,
        *,
        klines_15m_per_symbol: dict[Symbol, Sequence[NormalizedKline]],
        klines_1h_per_symbol: dict[Symbol, Sequence[NormalizedKline]],
        mark_15m_per_symbol: dict[Symbol, Sequence[MarkPriceKline]],
        funding_per_symbol: dict[Symbol, Sequence[FundingRateEvent]],
        symbol_info_per_symbol: dict[Symbol, SymbolInfo],
    ) -> BacktestRunResult:
        # Phase 3i-A guard lifted by Phase 3i-B1. The D1-A engine
        # dispatch is now wired via ``_run_symbol_d1a``. V1 default and
        # F1 dispatch paths are unchanged; the new D1-A path is
        # selected only when ``strategy_family ==
        # FUNDING_AWARE_DIRECTIONAL`` AND the BacktestConfig validator
        # has approved a non-None ``funding_aware_variant``.
        warnings: list[str] = []
        per_symbol_trades: dict[Symbol, list[TradeRecord]] = {}
        accounting_per_symbol: dict[Symbol, Accounting] = {}
        r2_counters_per_symbol: dict[Symbol, R2LifecycleCounters] = {}
        f1_counters_per_symbol: dict[Symbol, F1LifecycleCounters] = {}
        funding_aware_counters_per_symbol: dict[Symbol, FundingAwareLifecycleCounters] = {}

        is_f1 = self._config.strategy_family == StrategyFamily.MEAN_REVERSION_OVEREXTENSION
        is_d1a = self._config.strategy_family == StrategyFamily.FUNDING_AWARE_DIRECTIONAL

        for symbol in self._config.symbols:
            if symbol not in klines_15m_per_symbol:
                warnings.append(f"symbol {symbol} has no 15m data; skipping")
                continue
            # 1h data is only required for V1 dispatch; F1 has no 1h
            # bias filter per Phase 3b §4.8; D1-A has no 1h bias filter
            # per Phase 3g §6.13 / Phase 3h §3 (no regime filter).
            if not is_f1 and not is_d1a and symbol not in klines_1h_per_symbol:
                warnings.append(f"symbol {symbol} has no 1h data; skipping")
                continue
            if symbol not in mark_15m_per_symbol:
                warnings.append(f"symbol {symbol} has no mark-price data; skipping")
                continue
            if symbol not in funding_per_symbol:
                warnings.append(f"symbol {symbol} has no funding data; skipping")
                continue
            if symbol not in symbol_info_per_symbol:
                warnings.append(f"symbol {symbol} has no exchangeInfo; skipping")
                continue
            run = _SymbolRun(
                symbol=symbol,
                session=StrategySession(symbol=symbol, config=self._config.strategy_variant),
            )
            accounting = Accounting.start(self._config.sizing_equity_usdt)
            if is_d1a:
                self._run_symbol_d1a(
                    run,
                    accounting=accounting,
                    klines_15m=klines_15m_per_symbol[symbol],
                    mark_15m=mark_15m_per_symbol[symbol],
                    funding=funding_per_symbol[symbol],
                    symbol_info=symbol_info_per_symbol[symbol],
                )
            elif is_f1:
                self._run_symbol_f1(
                    run,
                    accounting=accounting,
                    klines_15m=klines_15m_per_symbol[symbol],
                    mark_15m=mark_15m_per_symbol[symbol],
                    funding=funding_per_symbol[symbol],
                    symbol_info=symbol_info_per_symbol[symbol],
                )
            else:
                self._run_symbol(
                    run,
                    accounting=accounting,
                    klines_15m=klines_15m_per_symbol[symbol],
                    klines_1h=klines_1h_per_symbol[symbol],
                    mark_15m=mark_15m_per_symbol[symbol],
                    funding=funding_per_symbol[symbol],
                    symbol_info=symbol_info_per_symbol[symbol],
                )
            per_symbol_trades[symbol] = run.trades
            accounting_per_symbol[symbol] = accounting
            r2_counters_per_symbol[symbol] = run.r2_counters
            f1_counters_per_symbol[symbol] = run.f1_counters
            funding_aware_counters_per_symbol[symbol] = run.d1a_counters

        return BacktestRunResult(
            config=self._config,
            per_symbol_trades=per_symbol_trades,
            accounting_per_symbol=accounting_per_symbol,
            warnings=warnings,
            r2_counters_per_symbol=r2_counters_per_symbol,
            f1_counters_per_symbol=f1_counters_per_symbol,
            funding_aware_counters_per_symbol=funding_aware_counters_per_symbol,
        )

    # ------------------------------------------------------------------
    # Per-symbol bar-by-bar loop
    # ------------------------------------------------------------------

    def _run_symbol(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        klines_15m: Sequence[NormalizedKline],
        klines_1h: Sequence[NormalizedKline],
        mark_15m: Sequence[MarkPriceKline],
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        config = self._config
        # Pre-populate the 1h window with all bars whose close_time <= window_start_ms
        # plus those within the window; the session computes bias only from completed bars.
        # We feed 1h bars as they "complete" in simulation time, synchronized with 15m.
        mark_by_open: dict[int, MarkPriceKline] = {m.open_time: m for m in mark_15m}

        # Walk 15m bars in ascending open_time. We also feed any 1h
        # bars that complete AT OR BEFORE the current 15m bar's close_time.
        bar_1h_idx = 0
        total_1h = len(klines_1h)

        for idx_15m, bar_15m in enumerate(klines_15m):
            t_now_ms = bar_15m.close_time + 1  # simulation clock at bar close
            # Feed any 1h bars that completed at or before t_now_ms.
            while bar_1h_idx < total_1h:
                candidate_1h = klines_1h[bar_1h_idx]
                if candidate_1h.close_time < t_now_ms:
                    run.session.observe_1h_bar(candidate_1h)
                    bar_1h_idx += 1
                else:
                    break

            # Observe the just-completed 15m bar.
            run.session.observe_15m_bar(bar_15m)

            # If we have an open trade, check stop-hit BEFORE running
            # management for the next bar. Source of the stop-evaluation
            # bar is controlled by config.stop_trigger_source:
            #   - MARK_PRICE (default): live-aligned; uses the mark-price
            #     bar keyed by the current 15m open_time.
            #   - TRADE_PRICE: Phase 2g sensitivity switch; uses the
            #     trade-price 15m bar directly.
            if run.open_trade is not None:
                if config.stop_trigger_source == StopTriggerSource.MARK_PRICE:
                    stop_eval_bar: MarkPriceKline | NormalizedKline | None = mark_by_open.get(
                        bar_15m.open_time
                    )
                else:  # TRADE_PRICE
                    stop_eval_bar = bar_15m
                if stop_eval_bar is not None:
                    hit = evaluate_stop_hit(
                        direction_long=run.open_trade.direction_long,
                        current_stop=run.open_trade.current_stop,
                        mark_bar=stop_eval_bar,
                        slippage_bps=config.slippage_bps,
                    )
                    if hit is not None:
                        self._close_trade_on_stop(
                            run,
                            accounting=accounting,
                            hit=hit,
                            funding=funding,
                            symbol_info=symbol_info,
                        )
                        # After a stop close we fall through so the bar
                        # is still observed in the session (already done).
                        continue

                # No stop hit: run management on this bar's close.
                _intent, _diag = self._strategy.manage(run.session, bar_15m)
                if _intent is not None:
                    if isinstance(_intent, StopUpdateIntent):
                        self._apply_stop_update(run, _intent)
                    elif isinstance(_intent, ExitIntent):
                        # Managed exit: fill at NEXT bar's open if available.
                        next_open_time = next_15m_open_time(bar_15m)
                        next_bar = self._find_next_15m(klines_15m, next_open_time)
                        if next_bar is None:
                            # End of data: close at current bar's close as an END_OF_DATA.
                            self._close_trade_end_of_data(
                                run,
                                accounting=accounting,
                                exit_price=bar_15m.close,
                                exit_time_ms=bar_15m.close_time + 1,
                                exit_reason_str=ExitReason.END_OF_DATA.value,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        else:
                            fill_price = exit_fill_price(
                                next_bar=next_bar,
                                direction_long=run.open_trade.direction_long
                                if run.open_trade is not None
                                else True,
                                config=config,
                            )
                            self._close_trade_managed(
                                run,
                                accounting=accounting,
                                next_bar=next_bar,
                                exit_price=fill_price,
                                exit_reason=_intent.reason,
                                funding=funding,
                                symbol_info=symbol_info,
                            )

            # Entry path branches on entry_kind. MARKET_NEXT_BAR_OPEN is
            # H0/R3/R1a/R1b-narrow path (immediate market fill at next
            # bar's open); PULLBACK_RETEST is R2 (Phase 2u, Gate 2 amended)
            # which routes through the conditional-pending lifecycle.
            if run.open_trade is None:
                if config.strategy_variant.entry_kind == EntryKind.PULLBACK_RETEST:
                    self._handle_r2_entry_lifecycle(
                        run,
                        bar_15m=bar_15m,
                        idx_15m=idx_15m,
                        klines_15m=klines_15m,
                        symbol_info=symbol_info,
                    )
                else:
                    # H0/R3/R1a/R1b-narrow path (unchanged from Phase 2s).
                    if config.window_start_ms <= bar_15m.open_time < config.window_end_ms:
                        entry = self._strategy.maybe_entry(run.session)
                        if entry is not None:
                            next_open_time = next_15m_open_time(bar_15m)
                            next_bar = self._find_next_15m(klines_15m, next_open_time)
                            if next_bar is not None:
                                self._maybe_open_trade(
                                    run,
                                    entry=entry,
                                    next_bar=next_bar,
                                    symbol_info=symbol_info,
                                )

        # End of window: if still in a trade, close it as END_OF_DATA.
        if run.open_trade is not None:
            last_bar = klines_15m[-1]
            self._close_trade_end_of_data(
                run,
                accounting=accounting,
                exit_price=last_bar.close,
                exit_time_ms=last_bar.close_time + 1,
                exit_reason_str=ExitReason.END_OF_DATA.value,
                funding=funding,
                symbol_info=symbol_info,
            )

    # ------------------------------------------------------------------
    # Entry
    # ------------------------------------------------------------------

    def _maybe_open_trade(
        self,
        run: _SymbolRun,
        *,
        entry: EntryIntent,
        next_bar: NormalizedKline,
        symbol_info: SymbolInfo,
    ) -> None:
        config = self._config
        is_long = entry.direction.value == "LONG"
        sizing = compute_size(
            sizing_equity_usdt=config.sizing_equity_usdt,
            risk_fraction=config.risk_fraction,
            risk_usage_fraction=config.risk_usage_fraction,
            stop_distance=entry.stop_distance,
            reference_price=entry.reference_price,
            max_effective_leverage=config.max_effective_leverage,
            max_notional_internal_usdt=config.max_notional_internal_usdt,
            symbol_info=symbol_info,
        )
        if not sizing.approved:
            return
        fill_price = entry_fill_price(next_bar=next_bar, direction_long=is_long, config=config)
        assert sizing.limited_by is not None  # approved=True implies labeled
        run.open_trade = _OpenTrade(
            symbol=entry.symbol,
            direction_long=is_long,
            signal_bar_open_time_ms=entry.signal.signal_bar_open_time,
            entry_fill_time_ms=next_bar.open_time,
            entry_fill_price=fill_price,
            initial_stop=entry.initial_stop,
            stop_distance=entry.stop_distance,
            quantity=sizing.quantity,
            notional=sizing.quantity * fill_price,
            sizing_limited_by=sizing.limited_by,
            realized_risk_usdt=sizing.realized_risk_usdt,
            current_stop=entry.initial_stop,
        )
        run.session.on_entry_filled(
            signal=entry.signal,
            fill_price=fill_price,
            fill_time_ms=next_bar.open_time,
            fill_bar=next_bar,
            initial_stop=entry.initial_stop,
        )

    # ------------------------------------------------------------------
    # R2 pullback-retest entry lifecycle (Phase 2u, Gate 2 amended)
    # ------------------------------------------------------------------

    def _handle_r2_entry_lifecycle(
        self,
        run: _SymbolRun,
        *,
        bar_15m: NormalizedKline,
        idx_15m: int,
        klines_15m: Sequence[NormalizedKline],
        symbol_info: SymbolInfo,
    ) -> None:
        """Handle the R2 entry-lifecycle for a single bar.

        Per Phase 2u §B / §E (Gate 2 amended):

            1. If pending candidate is past validity window → EXPIRE
               (counter: expired_no_pullback). Slot is freed.
            2. If pending candidate exists, evaluate per-bar with the
               5-step precedence (BIAS_FLIP > OPPOSITE_SIGNAL >
               STRUCTURAL_INVALIDATION > TOUCH+CONFIRMATION > CONTINUE).
               On READY_TO_FILL: open trade at next bar's open with R2
               metadata (counter: filled). On any CANCEL: increment the
               corresponding counter, clear pending. On CONTINUE:
               return without further action.
            3. If no pending and within window: maybe_entry → register
               PendingCandidate (counter: registered). No immediate
               fill — fill happens later when touch+confirmation fires.

        Per §E.5 pending uniqueness: same-direction signals during
        pending are silently dropped (handled implicitly here because
        the registration path runs only when ``has_pending_candidate``
        is False). Opposite-direction signals trigger OPPOSITE_SIGNAL
        cancellation in step 2; the new opposite-direction signal can
        register a fresh candidate at the same bar (fall-through to
        step 3 after cancellation is intentional).
        """
        config = self._config
        session = run.session

        # Step 1: expiry check
        pending = session.pending_candidate
        if pending is not None and pending.is_expired(idx_15m):
            run.r2_counters.expired_no_pullback += 1
            session.clear_pending_candidate()
            pending = None

        # Step 2: per-bar evaluation if pending exists
        new_intent_after_cancel: EntryIntent | None = None
        if pending is not None:
            bias = session.current_1h_bias()
            # Peek at maybe_entry to detect opposite-direction signal.
            # Under H0's bias-required trigger this only fires when
            # bias is the opposite direction; if it returns same-
            # direction intent we ignore it (silently drop per §E.5).
            new_intent = self._strategy.maybe_entry(session)
            opposite_signal_fires = (
                new_intent is not None and new_intent.direction != pending.direction
            )

            evaluation = evaluate_pending_candidate(
                pending,
                bar_15m,
                bias,
                opposite_signal_fires,
            )

            if evaluation == PendingEvaluation.CANCEL_BIAS_FLIP:
                run.r2_counters.cancelled_bias_flip += 1
                session.clear_pending_candidate()
                # After BIAS_FLIP, re-evaluate registration eligibility
                # below. The new bias may admit an opposite-direction
                # registration this bar (per §E.5 slot-is-free rule).
                pending = None
            elif evaluation == PendingEvaluation.CANCEL_OPPOSITE_SIGNAL:
                run.r2_counters.cancelled_opposite_signal += 1
                session.clear_pending_candidate()
                pending = None
                # The opposite-direction intent that triggered the cancel
                # is the one we should consider for fresh registration
                # below (per §E.5).
                new_intent_after_cancel = new_intent
            elif evaluation == PendingEvaluation.CANCEL_STRUCTURAL_INVALIDATION:
                run.r2_counters.cancelled_structural_invalidation += 1
                session.clear_pending_candidate()
                pending = None
            elif evaluation == PendingEvaluation.READY_TO_FILL:
                self._fill_r2_pending_candidate(
                    run,
                    pending=pending,
                    idx_15m=idx_15m,
                    bar_15m=bar_15m,
                    klines_15m=klines_15m,
                    symbol_info=symbol_info,
                )
                # _fill_r2_pending_candidate is responsible for clearing
                # pending and incrementing the counter (filled OR
                # cancelled_stop_distance_at_fill).
                return
            else:  # CONTINUE
                return

        # Step 3: registration eligibility (no pending, within window)
        if session.has_pending_candidate:
            return
        if not (config.window_start_ms <= bar_15m.open_time < config.window_end_ms):
            return
        if not session.can_re_enter:
            return
        if session.active_trade is not None:
            return

        # Use the cached new_intent if we already called maybe_entry
        # for opposite-signal detection above; otherwise compute now.
        entry = new_intent_after_cancel
        if entry is None:
            entry = self._strategy.maybe_entry(session)
        if entry is None:
            return

        # Register PendingCandidate from the EntryIntent.
        next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
        next_bar_open_at_signal = next_bar.open if next_bar is not None else float("nan")
        pullback_level = (
            entry.signal.setup.setup_high
            if entry.direction == Direction.LONG
            else entry.signal.setup.setup_low
        )
        candidate = PendingCandidate(
            direction=entry.direction,
            registration_bar_index=idx_15m,
            registration_bar_open_time=bar_15m.open_time,
            pullback_level=pullback_level,
            structural_stop_level=entry.initial_stop,
            atr_at_signal=entry.signal.atr_20_15m,
            validity_expires_at_index=idx_15m + R2_VALIDITY_WINDOW_BARS,
            signal_bar_open_time_ms=entry.signal.signal_bar_open_time,
            signal_bar_close_time_ms=entry.signal.signal_bar_close_time,
            next_bar_open_at_signal=next_bar_open_at_signal,
            signal=entry.signal,
        )
        session.register_pending_candidate(candidate)
        run.r2_counters.registered += 1

    def _fill_r2_pending_candidate(
        self,
        run: _SymbolRun,
        *,
        pending: PendingCandidate,
        idx_15m: int,
        bar_15m: NormalizedKline,
        klines_15m: Sequence[NormalizedKline],
        symbol_info: SymbolInfo,
    ) -> None:
        """Open a trade from a READY_TO_FILL PendingCandidate.

        The committed fill model per Phase 2u §F.4 is next-bar-open
        after confirmation. The fill-time stop-distance filter
        re-applies the same band H0 uses at signal time. On filter
        rejection: counter cancelled_stop_distance_at_fill++ and
        pending is cleared without opening a trade.
        """
        config = self._config
        session = run.session
        is_long = pending.direction == Direction.LONG

        # Dispatch on the runner-script-only R2 fill model. The
        # committed model (Phase 2u §F.4) is next-bar-open after
        # confirmation; the diagnostic-only alternative (Phase 2v
        # §P.6 / run #10) is limit-at-pullback intrabar. Both paths
        # share the fill-time stop-distance band re-check and the
        # frozen-structural-stop invariant.
        if self._r2_fill_model == "limit-at-pullback-intrabar":
            # Diagnostic-only: fill at the touch bar at pullback_level
            # with zero slippage (limit-fill maker assumption per
            # Phase 2u §P.6). Same taker fee as committed path
            # (no maker-fee path implemented; Phase 2v Gate 2
            # clarification: this is sensitivity-only).
            fill_bar = bar_15m
            fill_bar_idx = idx_15m
            raw_fill_price = pending.pullback_level
        else:
            # Committed (default): fill at NEXT bar's open, with
            # H0's existing slippage/fee path.
            next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
            if next_bar is None:
                # End of data on the touch+confirmation bar: cannot fill.
                # Treat as no-pullback expiry (the touch+confirmation
                # event happened but the fill cannot be recorded).
                run.r2_counters.expired_no_pullback += 1
                session.clear_pending_candidate()
                return
            fill_bar = next_bar
            fill_bar_idx = idx_15m + 1
            raw_fill_price = next_bar.open

        # Fill-time stop-distance re-check (same band as H0; uses
        # frozen ATR snapshot per Phase 2u §E.3).
        fill_eval = evaluate_fill_at_next_bar_open(
            pending,
            raw_fill_price,
            filter_min_atr_mult=FILTER_MIN_ATR_MULT,
            filter_max_atr_mult=FILTER_MAX_ATR_MULT,
        )
        if not fill_eval.fill:
            run.r2_counters.cancelled_stop_distance_at_fill += 1
            session.clear_pending_candidate()
            return

        # Compute the actual recorded fill price. Committed path uses
        # entry_fill_price() (applies slippage); diagnostic limit path
        # records the pullback level exactly (zero slippage; Phase 2u
        # §P.6 / Phase 2v §4.6).
        if self._r2_fill_model == "limit-at-pullback-intrabar":
            fill_price = pending.pullback_level
        else:
            fill_price = entry_fill_price(next_bar=fill_bar, direction_long=is_long, config=config)
        fill_stop_distance = abs(fill_price - pending.structural_stop_level)
        sizing = compute_size(
            sizing_equity_usdt=config.sizing_equity_usdt,
            risk_fraction=config.risk_fraction,
            risk_usage_fraction=config.risk_usage_fraction,
            stop_distance=fill_stop_distance,
            reference_price=fill_price,
            max_effective_leverage=config.max_effective_leverage,
            max_notional_internal_usdt=config.max_notional_internal_usdt,
            symbol_info=symbol_info,
        )
        if not sizing.approved:
            # Sizing rejection at fill time is conservative; treat as
            # stop-distance-at-fill cancellation (no trade opened).
            run.r2_counters.cancelled_stop_distance_at_fill += 1
            session.clear_pending_candidate()
            return
        assert sizing.limited_by is not None

        run.open_trade = _OpenTrade(
            symbol=fill_bar.symbol,
            direction_long=is_long,
            signal_bar_open_time_ms=pending.signal_bar_open_time_ms,
            entry_fill_time_ms=fill_bar.open_time,
            entry_fill_price=fill_price,
            initial_stop=pending.structural_stop_level,
            stop_distance=fill_stop_distance,
            quantity=sizing.quantity,
            notional=sizing.quantity * fill_price,
            sizing_limited_by=sizing.limited_by,
            realized_risk_usdt=sizing.realized_risk_usdt,
            current_stop=pending.structural_stop_level,
            r2_metadata=_R2TradeMetadata(
                registration_bar_index=pending.registration_bar_index,
                fill_bar_index=fill_bar_idx,
                pullback_level_at_registration=pending.pullback_level,
                structural_stop_level_at_registration=pending.structural_stop_level,
                atr_at_signal=pending.atr_at_signal,
                fill_price=fill_price,
            ),
        )
        # The R2 fill re-uses the BreakoutSignal carried on the
        # PendingCandidate (captured at registration). TradeManagement
        # consumes direction + entry_price + initial_stop +
        # entry_bar.high/low + close_time; the signal field on
        # ``_ActiveTrade`` is provenance-only. For R2 the R3 time-stop
        # horizon counts from the FILL bar (R3-consistent interpretation
        # per Phase 2u §G), which is what ``on_entry_filled`` already
        # does (it sets ``last_processed_close_time = fill_bar.close_time``).
        session.on_entry_filled(
            signal=pending.signal,
            fill_price=fill_price,
            fill_time_ms=fill_bar.open_time,
            fill_bar=fill_bar,
            initial_stop=pending.structural_stop_level,
        )
        session.clear_pending_candidate()
        run.r2_counters.filled += 1

    # ------------------------------------------------------------------
    # Stop / management updates and closes
    # ------------------------------------------------------------------

    def _apply_stop_update(self, run: _SymbolRun, update: StopUpdateIntent) -> None:
        if run.open_trade is None:
            return
        # Risk-reducing-only enforcement is also done inside
        # TradeManagement, but we double-check here for defense in
        # depth (silent drop rather than raise, since the strategy
        # object is the authority).
        if run.open_trade.direction_long:
            if update.new_stop > run.open_trade.current_stop:
                run.open_trade.current_stop = update.new_stop
        else:
            if update.new_stop < run.open_trade.current_stop:
                run.open_trade.current_stop = update.new_stop

    def _close_trade_on_stop(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        hit: StopHit,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        trade = run.open_trade
        trade.stop_was_gap_through = hit.was_gap_through
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=hit.fill_price,
            exit_time_ms=hit.fill_time_ms,
            exit_reason_str=ExitReason.STOP.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.session.on_exit_recorded(hit.fill_time_ms)

    def _close_trade_managed(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        next_bar: NormalizedKline,
        exit_price: float,
        exit_reason: ExitReason,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=next_bar.open_time,
            exit_reason_str=exit_reason.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.session.on_exit_recorded(next_bar.open_time)

    def _close_trade_end_of_data(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        exit_price: float,
        exit_time_ms: int,
        exit_reason_str: str,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=exit_time_ms,
            exit_reason_str=exit_reason_str,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.session.on_exit_recorded(exit_time_ms)

    # ------------------------------------------------------------------
    # Trade recording
    # ------------------------------------------------------------------

    def _record_trade(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        exit_price: float,
        exit_time_ms: int,
        exit_reason_str: str,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        trade = run.open_trade
        active = run.session.active_trade
        mgmt = active.management if active is not None else None
        funding_pnl, _matched = apply_funding_accrual(
            direction_long=trade.direction_long,
            entry_fill_time_ms=trade.entry_fill_time_ms,
            exit_fill_time_ms=exit_time_ms,
            position_notional_usdt=trade.notional,
            funding_events=funding,
        )
        pnl = compute_trade_pnl(
            direction_long=trade.direction_long,
            entry_price=trade.entry_fill_price,
            exit_price=exit_price,
            quantity=trade.quantity,
            stop_distance=trade.stop_distance,
            taker_fee_rate=self._config.taker_fee_rate,
            funding_accrued=funding_pnl,
        )
        accounting.apply_trade(pnl)
        mfe_r = mgmt.mfe_r if mgmt is not None else 0.0
        mae_r = mgmt.mae_r if mgmt is not None else 0.0
        bars_in_trade = mgmt.bars_in_trade if mgmt is not None else 0
        run.next_trade_id_seq += 1
        trade_id = (
            f"{trade.symbol.value}-{trade.entry_fill_time_ms}"
            f"-{run.next_trade_id_seq}-{uuid4().hex[:8]}"
        )
        # R2 metadata population (Phase 2u, Gate 2 amended). For non-R2
        # paths (entry_kind=MARKET_NEXT_BAR_OPEN), r2_metadata is None
        # and the TradeRecord R2 fields stay at their H0-equivalent
        # defaults (NaN floats / -1 ints / None reason).
        if trade.r2_metadata is not None:
            m = trade.r2_metadata
            r2_registration_bar_index = m.registration_bar_index
            r2_fill_bar_index = m.fill_bar_index
            r2_time_to_fill_bars = m.fill_bar_index - m.registration_bar_index - 1
            r2_pullback_level = m.pullback_level_at_registration
            r2_structural_stop = m.structural_stop_level_at_registration
            r2_atr_at_signal = m.atr_at_signal
            r2_fill_price = m.fill_price
            r2_r_distance = (
                abs(m.fill_price - m.structural_stop_level_at_registration) / m.atr_at_signal
                if m.atr_at_signal > 0
                else float("nan")
            )
        else:
            r2_registration_bar_index = -1
            r2_fill_bar_index = -1
            r2_time_to_fill_bars = 0
            r2_pullback_level = float("nan")
            r2_structural_stop = float("nan")
            r2_atr_at_signal = float("nan")
            r2_fill_price = float("nan")
            r2_r_distance = float("nan")
        # F1 metadata population (Phase 3d-B1). For V1 / D1-A paths,
        # f1_metadata is None and the F1 TradeRecord fields stay at
        # NaN defaults.
        if trade.f1_metadata is not None:
            f1m = trade.f1_metadata
            atr_b = f1m.atr_at_signal
            f1_overext_mag = abs(f1m.displacement_at_signal) / atr_b if atr_b > 0 else float("nan")
            f1_frozen_target = f1m.frozen_target
            f1_entry_to_target_atr = (
                abs(trade.entry_fill_price - f1m.frozen_target) / atr_b
                if atr_b > 0
                else float("nan")
            )
            f1_stop_dist_atr = f1m.stop_distance_at_signal / atr_b if atr_b > 0 else float("nan")
        else:
            f1_overext_mag = float("nan")
            f1_frozen_target = float("nan")
            f1_entry_to_target_atr = float("nan")
            f1_stop_dist_atr = float("nan")
        # D1-A metadata population (Phase 3i-B1). For V1 / F1 paths,
        # d1a_metadata is None and the D1-A TradeRecord fields stay at
        # None / NaN defaults. D1-A trades reuse the F1 ``entry_to_target_distance_atr``
        # and ``stop_distance_at_signal_atr`` fields (semantically the
        # same: distance to target / stop in ATR multiples). The F1
        # entry/stop-distance values above are NaN for D1-A trades, so
        # we overwrite them here.
        if trade.d1a_metadata is not None:
            dm = trade.d1a_metadata
            atr_b_d1a = dm.atr_at_signal
            d1a_funding_event_id: str | None = dm.funding_event_id
            d1a_funding_z = dm.funding_z_score
            d1a_funding_rate = dm.funding_rate
            d1a_bars_since = dm.bars_since_funding_event
            f1_entry_to_target_atr = (
                abs(trade.entry_fill_price - dm.target_price) / atr_b_d1a
                if atr_b_d1a > 0
                else float("nan")
            )
            f1_stop_dist_atr = (
                dm.stop_distance_at_signal / atr_b_d1a if atr_b_d1a > 0 else float("nan")
            )
        else:
            d1a_funding_event_id = None
            d1a_funding_z = float("nan")
            d1a_funding_rate = float("nan")
            d1a_bars_since = -1
        rec = TradeRecord(
            trade_id=trade_id,
            symbol=trade.symbol,
            direction="LONG" if trade.direction_long else "SHORT",
            signal_bar_open_time_ms=trade.signal_bar_open_time_ms,
            entry_fill_time_ms=trade.entry_fill_time_ms,
            entry_fill_price=trade.entry_fill_price,
            initial_stop=trade.initial_stop,
            stop_distance=trade.stop_distance,
            quantity=trade.quantity,
            notional_usdt=trade.notional,
            sizing_limited_by=trade.sizing_limited_by,
            realized_risk_usdt=trade.realized_risk_usdt,
            exit_reason=exit_reason_str,
            exit_fill_time_ms=exit_time_ms,
            exit_fill_price=exit_price,
            gross_pnl=pnl.gross_pnl,
            entry_fee=pnl.entry_fee,
            exit_fee=pnl.exit_fee,
            funding_pnl=pnl.funding_pnl,
            net_pnl=pnl.net_pnl,
            net_r_multiple=pnl.net_r_multiple,
            mfe_r=mfe_r,
            mae_r=mae_r,
            bars_in_trade=bars_in_trade,
            slippage_bucket=self._config.slippage_bucket,
            fee_rate_assumption=self._config.taker_fee_rate,
            stop_was_gap_through=trade.stop_was_gap_through,
            registration_bar_index=r2_registration_bar_index,
            fill_bar_index=r2_fill_bar_index,
            time_to_fill_bars=r2_time_to_fill_bars,
            pullback_level_at_registration=r2_pullback_level,
            structural_stop_level_at_registration=r2_structural_stop,
            atr_at_signal=r2_atr_at_signal,
            fill_price=r2_fill_price,
            r_distance=r2_r_distance,
            cancellation_reason=None,
            overextension_magnitude_at_signal=f1_overext_mag,
            frozen_target_value=f1_frozen_target,
            entry_to_target_distance_atr=f1_entry_to_target_atr,
            stop_distance_at_signal_atr=f1_stop_dist_atr,
            funding_event_id_at_signal=d1a_funding_event_id,
            funding_z_score_at_signal=d1a_funding_z,
            funding_rate_at_signal=d1a_funding_rate,
            bars_since_funding_event_at_signal=d1a_bars_since,
        )
        run.trades.append(rec)

    # ------------------------------------------------------------------
    # F1 mean-reversion-after-overextension dispatch (Phase 3d-B1)
    # ------------------------------------------------------------------

    def _run_symbol_f1(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        klines_15m: Sequence[NormalizedKline],
        mark_15m: Sequence[MarkPriceKline],
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        """Per-symbol F1 bar-by-bar lifecycle.

        Phase 3b §4 / Phase 3c §4 binding spec: detect 8-bar cumulative
        overextension > 1.75 × ATR(20)(B) at completed bar B's close;
        market-fill at open(B+1); freeze SMA(8)(B) target and structural
        stop with 0.10 × ATR buffer; honor [0.60, 1.80] × ATR(20)
        stop-distance admissibility evaluated on the de-slipped raw
        open(B+1); same-bar exit priority STOP > TARGET > TIME_STOP;
        unconditional time-stop after 8 completed bars from fill;
        same-direction cooldown blocks re-entry until cumulative
        displacement unwinds.

        F1 does NOT use the V1 1h-bias filter, V1 setup predicate, V1
        breakout trigger, or V1 trade-management trail / break-even /
        risk-reduction stages. F1 emits exactly STOP / TARGET /
        TIME_STOP / END_OF_DATA exit reasons (P.14-style invariant per
        Phase 3c §8.15).
        """
        config = self._config
        assert self._mean_reversion_strategy is not None
        f1_strategy = self._mean_reversion_strategy
        f1_config = f1_strategy.config

        # Pre-compute per-bar arrays once; F1 reads these many times.
        closes: list[float] = [float(b.close) for b in klines_15m]
        highs: list[float] = [float(b.high) for b in klines_15m]
        lows: list[float] = [float(b.low) for b in klines_15m]
        atr20_list: list[float] = wilder_atr(highs, lows, closes, period=20)

        # Per-bar 8-bar cumulative displacement aligned with klines_15m
        # by index. NaN entries before warmup so cooldown helpers can
        # skip them defensively.
        n = len(klines_15m)
        displacement_history: list[float] = []
        for i in range(n):
            if i < f1_config.overextension_window_bars:
                displacement_history.append(float("nan"))
            else:
                displacement_history.append(
                    closes[i] - closes[i - f1_config.overextension_window_bars]
                )

        mark_by_open: dict[int, MarkPriceKline] = {m.open_time: m for m in mark_15m}

        for idx_15m, bar_15m in enumerate(klines_15m):
            # 1. Open trade: STOP > TARGET > TIME_STOP (same-bar priority).
            if run.open_trade is not None:
                assert run.open_trade.f1_metadata is not None
                f1_meta = run.open_trade.f1_metadata
                # STOP check via mark-price (default) or trade-price.
                if config.stop_trigger_source == StopTriggerSource.MARK_PRICE:
                    stop_eval_bar: MarkPriceKline | NormalizedKline | None = mark_by_open.get(
                        bar_15m.open_time
                    )
                else:
                    stop_eval_bar = bar_15m
                if stop_eval_bar is not None:
                    hit = evaluate_stop_hit(
                        direction_long=run.open_trade.direction_long,
                        current_stop=run.open_trade.current_stop,
                        mark_bar=stop_eval_bar,
                        slippage_bps=config.slippage_bps,
                    )
                    if hit is not None:
                        self._close_f1_trade_on_stop(
                            run,
                            accounting=accounting,
                            hit=hit,
                            funding=funding,
                            symbol_info=symbol_info,
                            exit_bar_idx=idx_15m,
                        )
                        continue

                # TARGET / TIME_STOP only fire on bars t > B (signal bar).
                # The fill bar B+1 is t > B (B+1 > B), so target may fire
                # at the fill bar's close per Phase 3b §4.5 wording
                # ("first completed 15m bar t > B"). Time-stop counts
                # bars from fill bar; idx_15m - fill_bar_idx >= 8 means
                # 8 completed bars elapsed since fill (the
                # ``time_stop_bars`` lock).
                if idx_15m > f1_meta.signal_bar_index:
                    direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
                    target_fires = (
                        bar_15m.close >= f1_meta.frozen_target
                        if direction == Direction.LONG
                        else bar_15m.close <= f1_meta.frozen_target
                    )
                    if target_fires:
                        next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
                        if next_bar is None:
                            self._close_f1_trade_end_of_data(
                                run,
                                accounting=accounting,
                                exit_price=bar_15m.close,
                                exit_time_ms=bar_15m.close_time + 1,
                                exit_reason_str=ExitReason.END_OF_DATA.value,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        else:
                            fill_price = exit_fill_price(
                                next_bar=next_bar,
                                direction_long=run.open_trade.direction_long,
                                config=config,
                            )
                            self._close_f1_trade_managed(
                                run,
                                accounting=accounting,
                                next_bar=next_bar,
                                exit_price=fill_price,
                                exit_reason=ExitReason.TARGET,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        continue
                    # TIME_STOP at close of bar B+1+time_stop_bars.
                    bars_since_fill = idx_15m - f1_meta.fill_bar_index
                    if bars_since_fill >= f1_config.time_stop_bars:
                        next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
                        if next_bar is None:
                            self._close_f1_trade_end_of_data(
                                run,
                                accounting=accounting,
                                exit_price=bar_15m.close,
                                exit_time_ms=bar_15m.close_time + 1,
                                exit_reason_str=ExitReason.END_OF_DATA.value,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        else:
                            fill_price = exit_fill_price(
                                next_bar=next_bar,
                                direction_long=run.open_trade.direction_long,
                                config=config,
                            )
                            self._close_f1_trade_managed(
                                run,
                                accounting=accounting,
                                next_bar=next_bar,
                                exit_price=fill_price,
                                exit_reason=ExitReason.TIME_STOP,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        continue

            # 2. No open trade: evaluate F1 entry candidate at bar B's close.
            if run.open_trade is not None:
                continue
            if not (config.window_start_ms <= bar_15m.open_time < config.window_end_ms):
                continue
            # Need 8-bar warmup for displacement; ATR(20) requires at
            # least 21 bars (first ATR seed at index 20).
            if idx_15m < f1_config.overextension_window_bars:
                continue
            atr_b = atr20_list[idx_15m]
            if math.isnan(atr_b) or atr_b <= 0.0:
                continue
            # Need next bar to fill at open(B+1).
            next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
            if next_bar is None:
                continue
            raw_open_b1 = float(next_bar.open)
            # Detect overextension event first (drives the funnel
            # counters' "detected" bucket regardless of cooldown /
            # admissibility outcome).
            fires, sign = overextension_event(
                closes=closes,
                atr20=atr20_list,
                b_index=idx_15m,
                threshold_atr_multiple=f1_config.overextension_threshold_atr_multiple,
            )
            if not fires:
                continue
            direction = Direction.SHORT if sign > 0 else Direction.LONG
            run.f1_counters.overextension_events_detected += 1
            # Cooldown gate: per Phase 3b §4.7, no same-direction
            # re-entry until cumulative displacement unwinds since the
            # prior exit. Opposite direction is never blocked.
            if not can_re_enter(
                candidate_direction=direction,
                last_exit_direction=run.f1_last_exit_direction,
                last_exit_index=run.f1_last_exit_idx,
                displacement_history=displacement_history,
                atr20_history=atr20_list,
                current_index=idx_15m,
                threshold_atr_multiple=f1_config.overextension_threshold_atr_multiple,
            ):
                run.f1_counters.overextension_events_blocked_cooldown += 1
                continue
            # Stop-distance admissibility gate via the strategy facade.
            # ``reference_price`` is the de-slipped raw open(B+1) per
            # Phase 3b §4.9 / Phase 3c §11.4.
            signal = f1_strategy.evaluate_entry_signal(
                b_index=idx_15m,
                closes=closes,
                highs=highs,
                lows=lows,
                atr20=atr20_list,
                reference_price=raw_open_b1,
            )
            if signal is None:
                # Cooldown was passed above, so the only remaining
                # rejection cause is stop-distance admissibility.
                run.f1_counters.overextension_events_rejected_stop_distance += 1
                continue
            run.f1_counters.overextension_events_filled += 1
            self._open_f1_trade(
                run,
                signal=signal,
                signal_bar=bar_15m,
                next_bar=next_bar,
                signal_bar_index=idx_15m,
                fill_bar_index=idx_15m + 1,
                symbol_info=symbol_info,
            )

        # End-of-window: close as END_OF_DATA at last bar's close.
        if run.open_trade is not None:
            last_bar = klines_15m[-1]
            self._close_f1_trade_end_of_data(
                run,
                accounting=accounting,
                exit_price=last_bar.close,
                exit_time_ms=last_bar.close_time + 1,
                exit_reason_str=ExitReason.END_OF_DATA.value,
                exit_bar_idx=len(klines_15m) - 1,
                funding=funding,
                symbol_info=symbol_info,
            )

    def _open_f1_trade(
        self,
        run: _SymbolRun,
        *,
        signal: object,  # MeanReversionEntrySignal; typed via attribute access
        signal_bar: NormalizedKline,
        next_bar: NormalizedKline,
        signal_bar_index: int,
        fill_bar_index: int,
        symbol_info: SymbolInfo,
    ) -> None:
        """Open an F1 trade from a validated entry signal."""
        from prometheus.strategy.mean_reversion_overextension import (
            MeanReversionEntrySignal,
        )

        assert isinstance(signal, MeanReversionEntrySignal)
        config = self._config
        is_long = signal.direction == Direction.LONG
        # Recompute fill price using the engine's slippage convention
        # (entry_fill_price applies adverse slippage). This may differ
        # from signal.reference_price (raw); the stop-distance band has
        # already been validated on the raw value per Phase 3c §11.4.
        fill_price = entry_fill_price(next_bar=next_bar, direction_long=is_long, config=config)
        # Sizing uses the actual filled price + filled stop distance for
        # quantity computation; the band check is on the raw value.
        post_slip_stop_distance = abs(fill_price - signal.initial_stop)
        sizing = compute_size(
            sizing_equity_usdt=config.sizing_equity_usdt,
            risk_fraction=config.risk_fraction,
            risk_usage_fraction=config.risk_usage_fraction,
            stop_distance=post_slip_stop_distance,
            reference_price=fill_price,
            max_effective_leverage=config.max_effective_leverage,
            max_notional_internal_usdt=config.max_notional_internal_usdt,
            symbol_info=symbol_info,
        )
        if not sizing.approved:
            # Sizing rejection at fill time: undo the filled-counter
            # increment and treat as stop-distance rejection (no trade
            # opened, identity preserved). Mirrors R2's fill-time
            # rejection handling.
            run.f1_counters.overextension_events_filled -= 1
            run.f1_counters.overextension_events_rejected_stop_distance += 1
            return
        assert sizing.limited_by is not None
        run.open_trade = _OpenTrade(
            symbol=next_bar.symbol,
            direction_long=is_long,
            signal_bar_open_time_ms=signal_bar.open_time,
            entry_fill_time_ms=next_bar.open_time,
            entry_fill_price=fill_price,
            initial_stop=signal.initial_stop,
            stop_distance=post_slip_stop_distance,
            quantity=sizing.quantity,
            notional=sizing.quantity * fill_price,
            sizing_limited_by=sizing.limited_by,
            realized_risk_usdt=sizing.realized_risk_usdt,
            current_stop=signal.initial_stop,
            f1_metadata=_F1TradeMetadata(
                signal_bar_index=signal_bar_index,
                fill_bar_index=fill_bar_index,
                frozen_target=signal.frozen_target,
                atr_at_signal=signal.atr_at_signal,
                displacement_at_signal=signal.displacement_at_signal,
                stop_distance_at_signal=signal.stop_distance,
                raw_entry_reference=signal.reference_price,
            ),
        )

    def _close_f1_trade_on_stop(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        hit: StopHit,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
        exit_bar_idx: int,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.f1_metadata is not None
        trade = run.open_trade
        trade.stop_was_gap_through = hit.was_gap_through
        direction = Direction.LONG if trade.direction_long else Direction.SHORT
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=hit.fill_price,
            exit_time_ms=hit.fill_time_ms,
            exit_reason_str=ExitReason.STOP.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.f1_last_exit_direction = direction
        run.f1_last_exit_idx = exit_bar_idx

    def _close_f1_trade_managed(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        next_bar: NormalizedKline,
        exit_price: float,
        exit_reason: ExitReason,
        exit_bar_idx: int,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.f1_metadata is not None
        direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=next_bar.open_time,
            exit_reason_str=exit_reason.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.f1_last_exit_direction = direction
        run.f1_last_exit_idx = exit_bar_idx

    def _close_f1_trade_end_of_data(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        exit_price: float,
        exit_time_ms: int,
        exit_reason_str: str,
        exit_bar_idx: int,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.f1_metadata is not None
        direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=exit_time_ms,
            exit_reason_str=exit_reason_str,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.f1_last_exit_direction = direction
        run.f1_last_exit_idx = exit_bar_idx

    # ------------------------------------------------------------------
    # D1-A funding-aware directional dispatch (Phase 3i-B1)
    # ------------------------------------------------------------------

    def _run_symbol_d1a(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        klines_15m: Sequence[NormalizedKline],
        mark_15m: Sequence[MarkPriceKline],
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        """Per-symbol D1-A bar-by-bar lifecycle.

        Phase 3g §6 + §5.6.5 Option A binding spec (with Phase 3h
        timing-clarification amendments): at each completed 15m bar B,
        identify the most-recent completed funding event with
        ``funding_time <= bar_close_time`` (non-strict ≤; equality
        eligible). Compute the trailing-90-day Z-score of that event's
        funding rate (270 prior events; current event excluded from
        its own mean/std). If ``|Z_F| >= 2.0``, emit a contrarian
        entry signal (``Z >= +2`` -> SHORT; ``Z <= -2`` -> LONG).

        Repeated 15m bars referencing the same ``funding_event_id``
        must NOT inflate the event-level "detected" counter; the
        engine tracks the last-processed event id per symbol.

        Entry fills at the next 15m bar's open. Stop = ``1.0 × ATR(20)``
        at fill, never moved (MARK_PRICE trigger). TARGET = ``+2.0R``
        fixed, recorded as TARGET (not TAKE_PROFIT). TARGET triggers
        only on completed-bar close confirmation; LONG ``close >=
        target_price``, SHORT ``close <= target_price``; fills at next
        bar open. No intrabar target-touch fill, no same-close fill.
        Same-bar priority STOP > TARGET > TIME_STOP. TIME_STOP at
        ``B+1+32`` close trigger; ``B+1+33`` open fill. Per-funding-
        event cooldown: same-direction re-entry requires a fresh
        funding event after position close; opposite-direction always
        allowed at any subsequent event.

        D1-A does NOT use the V1 1h-bias filter, V1 setup predicate,
        V1 breakout trigger, V1 trade-management trail / break-even /
        risk-reduction stages, or any F1 overextension predicate. D1-A
        emits exactly STOP / TARGET / TIME_STOP / END_OF_DATA exit
        reasons (P.14-style invariant per Phase 3h §14).
        """
        config = self._config
        assert self._funding_aware_strategy is not None
        d1a_config = self._funding_aware_strategy.config

        closes: list[float] = [float(b.close) for b in klines_15m]
        highs: list[float] = [float(b.high) for b in klines_15m]
        lows: list[float] = [float(b.low) for b in klines_15m]
        atr20_list: list[float] = wilder_atr(highs, lows, closes, period=20)

        # Build sorted FundingEvent list (sorted ascending by funding_time)
        # plus a parallel funding_rates list and a funding_times list for
        # bisect-based lookup.
        sorted_funding: list[FundingRateEvent] = sorted(funding, key=lambda e: e.funding_time)
        funding_event_objs: list[FundingEvent] = [
            FundingEvent(
                event_id=f"{e.symbol.value}-{e.funding_time}",
                funding_time=e.funding_time,
                funding_rate=e.funding_rate,
            )
            for e in sorted_funding
        ]
        funding_rates_chronological: list[float] = [e.funding_rate for e in sorted_funding]
        funding_times: list[int] = [e.funding_time for e in sorted_funding]

        mark_by_open: dict[int, MarkPriceKline] = {m.open_time: m for m in mark_15m}

        for idx_15m, bar_15m in enumerate(klines_15m):
            # 1. Manage open trade: STOP > TARGET > TIME_STOP (same-bar priority).
            if run.open_trade is not None:
                assert run.open_trade.d1a_metadata is not None
                d1a_meta = run.open_trade.d1a_metadata
                # STOP check via mark-price (default) or trade-price.
                if config.stop_trigger_source == StopTriggerSource.MARK_PRICE:
                    stop_eval_bar: MarkPriceKline | NormalizedKline | None = mark_by_open.get(
                        bar_15m.open_time
                    )
                else:
                    stop_eval_bar = bar_15m
                if stop_eval_bar is not None:
                    hit = evaluate_stop_hit(
                        direction_long=run.open_trade.direction_long,
                        current_stop=run.open_trade.current_stop,
                        mark_bar=stop_eval_bar,
                        slippage_bps=config.slippage_bps,
                    )
                    if hit is not None:
                        self._close_d1a_trade_on_stop(
                            run,
                            accounting=accounting,
                            hit=hit,
                            funding=funding,
                            symbol_info=symbol_info,
                            exit_bar_idx=idx_15m,
                        )
                        continue
                # TARGET / TIME_STOP only fire on bars t >= fill_bar_index
                # (the fill bar B+1 itself is the first eligible bar to
                # check completed-close TARGET; the fill at B+1 happens
                # at B+1's OPEN, so by B+1's close the position is open).
                if idx_15m >= d1a_meta.fill_bar_index:
                    direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
                    target_fires = (
                        bar_15m.close >= d1a_meta.target_price
                        if direction == Direction.LONG
                        else bar_15m.close <= d1a_meta.target_price
                    )
                    if target_fires:
                        next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
                        if next_bar is None:
                            self._close_d1a_trade_end_of_data(
                                run,
                                accounting=accounting,
                                exit_price=bar_15m.close,
                                exit_time_ms=bar_15m.close_time + 1,
                                exit_reason_str=ExitReason.END_OF_DATA.value,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        else:
                            fill_price = exit_fill_price(
                                next_bar=next_bar,
                                direction_long=run.open_trade.direction_long,
                                config=config,
                            )
                            self._close_d1a_trade_managed(
                                run,
                                accounting=accounting,
                                next_bar=next_bar,
                                exit_price=fill_price,
                                exit_reason=ExitReason.TARGET,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        continue
                    # TIME_STOP: trigger at close of bar
                    # ``fill_bar_index + time_stop_bars`` per Phase 3g §6.9
                    # / Phase 3h §6.9 clarification. Fill at next bar
                    # open (no same-close fill).
                    time_stop_trigger_idx = d1a_meta.fill_bar_index + d1a_config.time_stop_bars
                    if idx_15m >= time_stop_trigger_idx:
                        next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
                        if next_bar is None:
                            self._close_d1a_trade_end_of_data(
                                run,
                                accounting=accounting,
                                exit_price=bar_15m.close,
                                exit_time_ms=bar_15m.close_time + 1,
                                exit_reason_str=ExitReason.END_OF_DATA.value,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        else:
                            fill_price = exit_fill_price(
                                next_bar=next_bar,
                                direction_long=run.open_trade.direction_long,
                                config=config,
                            )
                            self._close_d1a_trade_managed(
                                run,
                                accounting=accounting,
                                next_bar=next_bar,
                                exit_price=fill_price,
                                exit_reason=ExitReason.TIME_STOP,
                                exit_bar_idx=idx_15m,
                                funding=funding,
                                symbol_info=symbol_info,
                            )
                        continue

            # 2. Identify the latest eligible funding event for bar B's close.
            latest_evt_idx = self._latest_eligible_funding_event_idx(
                funding_times, bar_15m.close_time
            )
            if latest_evt_idx is None:
                continue
            eligible_event = funding_event_objs[latest_evt_idx]
            eligible_event_id = eligible_event.event_id

            # 3. Skip event-funnel bookkeeping if we've already processed
            # this event id (Phase 3g §9.4 amended; Phase 3h §14 P.14
            # invariant 5: repeated bars must not inflate detected count).
            if run.d1a_last_processed_event_id == eligible_event_id:
                continue

            # 4. Pre-detection warmup checks. We deliberately do NOT
            # mark the event as processed if these warmup checks fail,
            # so a later bar (with valid ATR / window / next_bar) can
            # re-evaluate the same event. Per Phase 3g §9.4, detection
            # is event-level — but only events the engine could
            # actually attempt are counted. If a fresh extreme funding
            # event fires entirely before ATR warmup completes, no
            # detection occurs (no trade was ever attemptable).
            if not (config.window_start_ms <= bar_15m.open_time < config.window_end_ms):
                continue
            atr_b = atr20_list[idx_15m]
            if math.isnan(atr_b) or atr_b <= 0.0:
                continue
            next_bar = self._find_next_15m(klines_15m, next_15m_open_time(bar_15m))
            if next_bar is None:
                continue

            # 5. Compute Z-score over the trailing N prior events
            # (current event explicitly excluded from rolling mean/std).
            prior_rates = funding_rates_chronological[:latest_evt_idx]
            z_score = compute_d1a_z_score(
                prior_rates,
                eligible_event.funding_rate,
                lookback_events=d1a_config.funding_z_score_lookback_events,
            )

            if not is_funding_extreme(z_score, threshold=d1a_config.funding_z_score_threshold):
                # Not extreme; mark this event as processed (so we don't
                # recompute Z-score on every subsequent bar referencing
                # it) but do NOT increment the detected counter — only
                # extreme events count.
                run.d1a_last_processed_event_id = eligible_event_id
                continue

            maybe_direction = d1a_signal_direction(
                z_score, threshold=d1a_config.funding_z_score_threshold
            )
            if maybe_direction is None:
                run.d1a_last_processed_event_id = eligible_event_id
                continue
            direction = maybe_direction

            # Detected extreme event — increment funnel and mark
            # processed so subsequent bars referencing this event id
            # are skipped.
            run.d1a_counters.funding_extreme_events_detected += 1
            run.d1a_last_processed_event_id = eligible_event_id

            # 6. Cooldown gate (per-funding-event consumption).
            position_open = run.open_trade is not None
            if not can_re_enter_d1a(
                candidate_direction=direction,
                candidate_event_id=eligible_event_id,
                last_consumed_event_id=run.d1a_last_consumed_event_id,
                last_consumed_direction=run.d1a_last_consumed_direction,
                position_open=position_open,
            ):
                run.d1a_counters.funding_extreme_events_blocked_cooldown += 1
                continue

            # 7. Stop-distance admissibility on the de-slipped raw
            # open(B+1) per Phase 3g §6.11. D1-A's stop_distance is
            # 1.0 × ATR(20) by construction, so the admissibility band
            # [0.60, 1.80] always passes; the check is a guard.
            raw_open_b1 = float(next_bar.open)
            stop_distance_raw = d1a_config.stop_distance_atr_multiplier * atr_b
            if not passes_d1a_stop_distance_filter(
                stop_distance_raw,
                atr_b,
                min_atr=d1a_config.stop_distance_min_atr,
                max_atr=d1a_config.stop_distance_max_atr,
            ):
                run.d1a_counters.funding_extreme_events_rejected_stop_distance += 1
                continue

            initial_stop_raw = compute_d1a_stop(
                fill_price=raw_open_b1,
                atr20=atr_b,
                side=direction,
                multiplier=d1a_config.stop_distance_atr_multiplier,
            )
            target_price_raw = compute_d1a_target(
                fill_price=raw_open_b1,
                stop_distance=stop_distance_raw,
                side=direction,
                target_r=d1a_config.target_r_multiple,
            )

            # Compute bars_since_funding_event diagnostic (signal time).
            # Use the first 15m bar whose open_time >= funding_time as
            # bar 0; subtract from current idx_15m. If funding_time
            # precedes the dataset, count from idx 0.
            bars_since = self._bars_since_funding_event(
                klines_15m, eligible_event.funding_time, idx_15m
            )

            # 9. Open the trade.
            self._open_d1a_trade(
                run,
                next_bar=next_bar,
                signal_bar=bar_15m,
                signal_bar_index=idx_15m,
                fill_bar_index=idx_15m + 1,
                direction=direction,
                raw_open_b1=raw_open_b1,
                initial_stop_raw=initial_stop_raw,
                target_price_raw=target_price_raw,
                stop_distance_raw=stop_distance_raw,
                atr_b=atr_b,
                eligible_event=eligible_event,
                z_score=z_score,
                bars_since=bars_since,
                symbol_info=symbol_info,
            )

        # End-of-window: close any still-open D1-A trade as END_OF_DATA.
        if run.open_trade is not None:
            last_bar = klines_15m[-1]
            self._close_d1a_trade_end_of_data(
                run,
                accounting=accounting,
                exit_price=last_bar.close,
                exit_time_ms=last_bar.close_time + 1,
                exit_reason_str=ExitReason.END_OF_DATA.value,
                exit_bar_idx=len(klines_15m) - 1,
                funding=funding,
                symbol_info=symbol_info,
            )

    # ------------------------------------------------------------------
    # D1-A helpers (Phase 3i-B1)
    # ------------------------------------------------------------------

    @staticmethod
    def _latest_eligible_funding_event_idx(
        funding_times: Sequence[int], bar_close_time: int
    ) -> int | None:
        """Return the index of the most recent funding event with
        ``funding_time <= bar_close_time`` (non-strict ≤; equality
        eligible per Phase 3h §4.5 clarification).

        ``funding_times`` must be sorted ascending. Returns None if no
        event satisfies the condition.
        """
        from bisect import bisect_right

        if not funding_times:
            return None
        # bisect_right finds insertion point for bar_close_time; idx-1
        # is the largest index with funding_time <= bar_close_time
        # (because bisect_right places equal values to the right).
        pos = bisect_right(funding_times, bar_close_time) - 1
        if pos < 0:
            return None
        return pos

    @staticmethod
    def _bars_since_funding_event(
        klines_15m: Sequence[NormalizedKline], funding_time: int, current_idx: int
    ) -> int:
        """Count the number of completed 15m bars between
        ``funding_time`` and the bar at ``current_idx`` (inclusive of
        the current bar). Diagnostic only; -1 if funding_time is after
        the current bar (should not happen at signal time).
        """
        # Find the first bar whose open_time is >= funding_time (the bar
        # that contains or starts at the settlement). bars_since =
        # current_idx - that_idx.
        for i, bar in enumerate(klines_15m):
            if bar.open_time >= funding_time:
                return max(0, current_idx - i)
        # Funding event is after all bars — should not happen at signal
        # time given alignment rule funding_time <= bar_close_time.
        return -1

    def _open_d1a_trade(
        self,
        run: _SymbolRun,
        *,
        next_bar: NormalizedKline,
        signal_bar: NormalizedKline,
        signal_bar_index: int,
        fill_bar_index: int,
        direction: Direction,
        raw_open_b1: float,
        initial_stop_raw: float,
        target_price_raw: float,
        stop_distance_raw: float,
        atr_b: float,
        eligible_event: FundingEvent,
        z_score: float,
        bars_since: int,
        symbol_info: SymbolInfo,
    ) -> None:
        """Open a D1-A trade from a validated funding-extreme entry."""
        config = self._config
        is_long = direction == Direction.LONG
        # Recompute fill price using engine's slippage convention
        # (entry_fill_price applies adverse slippage). The stop-distance
        # band check has already been validated on the de-slipped raw
        # open(B+1) per Phase 3g §6.11.
        fill_price = entry_fill_price(next_bar=next_bar, direction_long=is_long, config=config)
        post_slip_stop_distance = abs(fill_price - initial_stop_raw)
        sizing = compute_size(
            sizing_equity_usdt=config.sizing_equity_usdt,
            risk_fraction=config.risk_fraction,
            risk_usage_fraction=config.risk_usage_fraction,
            stop_distance=post_slip_stop_distance,
            reference_price=fill_price,
            max_effective_leverage=config.max_effective_leverage,
            max_notional_internal_usdt=config.max_notional_internal_usdt,
            symbol_info=symbol_info,
        )
        if not sizing.approved:
            # Sizing rejection at fill time: count as stop-distance
            # rejection (no trade opened, identity preserved).
            run.d1a_counters.funding_extreme_events_rejected_stop_distance += 1
            return
        run.d1a_counters.funding_extreme_events_filled += 1
        # Recompute target on the actual filled price so target_price
        # reflects the post-slip entry. The +2.0R geometry is preserved
        # using the post-slip stop distance.
        target_price_filled = compute_d1a_target(
            fill_price=fill_price,
            stop_distance=post_slip_stop_distance,
            side=direction,
            target_r=self._funding_aware_strategy.config.target_r_multiple
            if self._funding_aware_strategy is not None
            else 2.0,
        )
        assert sizing.limited_by is not None
        run.open_trade = _OpenTrade(
            symbol=next_bar.symbol,
            direction_long=is_long,
            signal_bar_open_time_ms=signal_bar.open_time,
            entry_fill_time_ms=next_bar.open_time,
            entry_fill_price=fill_price,
            initial_stop=initial_stop_raw,
            stop_distance=post_slip_stop_distance,
            quantity=sizing.quantity,
            notional=sizing.quantity * fill_price,
            sizing_limited_by=sizing.limited_by,
            realized_risk_usdt=sizing.realized_risk_usdt,
            current_stop=initial_stop_raw,
            d1a_metadata=_D1ATradeMetadata(
                signal_bar_index=signal_bar_index,
                fill_bar_index=fill_bar_index,
                target_price=target_price_filled,
                atr_at_signal=atr_b,
                stop_distance_at_signal=stop_distance_raw,
                raw_entry_reference=raw_open_b1,
                funding_event_id=eligible_event.event_id,
                funding_time=eligible_event.funding_time,
                funding_rate=eligible_event.funding_rate,
                funding_z_score=z_score,
                bars_since_funding_event=bars_since,
            ),
        )

    def _close_d1a_trade_on_stop(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        hit: StopHit,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
        exit_bar_idx: int,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.d1a_metadata is not None
        trade = run.open_trade
        trade.stop_was_gap_through = hit.was_gap_through
        direction = Direction.LONG if trade.direction_long else Direction.SHORT
        consumed_event_id = run.open_trade.d1a_metadata.funding_event_id
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=hit.fill_price,
            exit_time_ms=hit.fill_time_ms,
            exit_reason_str=ExitReason.STOP.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.d1a_last_consumed_event_id = consumed_event_id
        run.d1a_last_consumed_direction = direction
        # exit_bar_idx is unused for D1-A cooldown (event-level), but
        # parity with F1 is maintained for diagnostic continuity.
        _ = exit_bar_idx

    def _close_d1a_trade_managed(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        next_bar: NormalizedKline,
        exit_price: float,
        exit_reason: ExitReason,
        exit_bar_idx: int,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.d1a_metadata is not None
        direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
        consumed_event_id = run.open_trade.d1a_metadata.funding_event_id
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=next_bar.open_time,
            exit_reason_str=exit_reason.value,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.d1a_last_consumed_event_id = consumed_event_id
        run.d1a_last_consumed_direction = direction
        _ = exit_bar_idx

    def _close_d1a_trade_end_of_data(
        self,
        run: _SymbolRun,
        *,
        accounting: Accounting,
        exit_price: float,
        exit_time_ms: int,
        exit_reason_str: str,
        exit_bar_idx: int,
        funding: Sequence[FundingRateEvent],
        symbol_info: SymbolInfo,
    ) -> None:
        assert run.open_trade is not None
        assert run.open_trade.d1a_metadata is not None
        direction = Direction.LONG if run.open_trade.direction_long else Direction.SHORT
        consumed_event_id = run.open_trade.d1a_metadata.funding_event_id
        self._record_trade(
            run,
            accounting=accounting,
            exit_price=exit_price,
            exit_time_ms=exit_time_ms,
            exit_reason_str=exit_reason_str,
            funding=funding,
            symbol_info=symbol_info,
        )
        run.open_trade = None
        run.d1a_last_consumed_event_id = consumed_event_id
        run.d1a_last_consumed_direction = direction
        _ = exit_bar_idx

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _find_next_15m(
        klines_15m: Sequence[NormalizedKline], target_open_time: int
    ) -> NormalizedKline | None:
        """Linear-scan for the bar with matching open_time.

        Acceptable cost for month-scale backtests. If future phases
        extend the window to multi-year data, this can be switched
        to an index lookup.
        """
        for b in klines_15m:
            if b.open_time == target_open_time:
                return b
            if b.open_time > target_open_time:
                return None
        return None


def iter_trade_records(run_result: BacktestRunResult) -> Iterable[TradeRecord]:
    """Flatten all trade records across symbols in ascending exit time."""
    all_records: list[TradeRecord] = []
    for records in run_result.per_symbol_trades.values():
        all_records.extend(records)
    all_records.sort(key=lambda r: r.exit_fill_time_ms)
    return all_records


__all__ = [
    "BacktestEngine",
    "BacktestRunResult",
    "iter_trade_records",
]


# Silence unused-import warnings from re-exported helpers referenced in
# docstrings. These names are used by tests via the package __init__.
_ = TradePnL
