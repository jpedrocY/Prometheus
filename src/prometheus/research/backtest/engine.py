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

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from uuid import uuid4

from prometheus.core.events import FundingRateEvent
from prometheus.core.exchange_info import SymbolInfo
from prometheus.core.klines import NormalizedKline
from prometheus.core.mark_price_klines import MarkPriceKline
from prometheus.core.symbols import Symbol
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
from .config import BacktestConfig, StopTriggerSource
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
        warnings: list[str] = []
        per_symbol_trades: dict[Symbol, list[TradeRecord]] = {}
        accounting_per_symbol: dict[Symbol, Accounting] = {}
        r2_counters_per_symbol: dict[Symbol, R2LifecycleCounters] = {}

        for symbol in self._config.symbols:
            if symbol not in klines_15m_per_symbol:
                warnings.append(f"symbol {symbol} has no 15m data; skipping")
                continue
            if symbol not in klines_1h_per_symbol:
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

        return BacktestRunResult(
            config=self._config,
            per_symbol_trades=per_symbol_trades,
            accounting_per_symbol=accounting_per_symbol,
            warnings=warnings,
            r2_counters_per_symbol=r2_counters_per_symbol,
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
        )
        run.trades.append(rec)

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
