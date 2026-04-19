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
from prometheus.strategy.types import EntryIntent, ExitIntent, ExitReason, StopUpdateIntent
from prometheus.strategy.v1_breakout import StrategySession, V1BreakoutStrategy

from .accounting import Accounting, TradePnL, compute_trade_pnl
from .config import BacktestConfig
from .fills import entry_fill_price, exit_fill_price
from .funding_join import apply_funding_accrual
from .simulation_clock import next_15m_open_time
from .sizing import SizingLimitedBy, compute_size
from .stops import StopHit, evaluate_stop_hit
from .trade_log import TradeRecord


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


@dataclass
class BacktestRunResult:
    """Aggregate outputs of a single backtest run."""

    config: BacktestConfig
    per_symbol_trades: dict[Symbol, list[TradeRecord]]
    accounting_per_symbol: dict[Symbol, Accounting]
    warnings: list[str]

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

    def __init__(self, config: BacktestConfig) -> None:
        self._config = config
        self._strategy = V1BreakoutStrategy()

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
            run = _SymbolRun(symbol=symbol, session=StrategySession(symbol=symbol))
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

        return BacktestRunResult(
            config=self._config,
            per_symbol_trades=per_symbol_trades,
            accounting_per_symbol=accounting_per_symbol,
            warnings=warnings,
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

        for bar_15m in klines_15m:
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

            # If we have an open trade, check stop-hit against this
            # bar's mark-price bar BEFORE running management for the
            # next bar. Rationale: a stop-out fires intrabar based
            # on mark-price; management moves happen at bar close.
            if run.open_trade is not None:
                mark_bar = mark_by_open.get(bar_15m.open_time)
                if mark_bar is not None:
                    hit = evaluate_stop_hit(
                        direction_long=run.open_trade.direction_long,
                        current_stop=run.open_trade.current_stop,
                        mark_bar=mark_bar,
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

            # If flat, and this bar is within the config window, try
            # to produce an entry signal. Entry fills on the NEXT bar.
            if (
                run.open_trade is None
                and config.window_start_ms <= bar_15m.open_time < config.window_end_ms
            ):
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
