"""Running equity + fee + slippage accounting.

Tracks gross PnL, fees, accrued funding, and running equity across
a simulation window. Accounting is flat (non-compounding) by default
per GAP-20260419-021 (R1 primary variant). A compounding variant
can be added by re-seeding ``sizing_equity`` from running equity on
each trade entry.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TradePnL:
    """Computed PnL for a single closed trade."""

    gross_pnl: float
    entry_fee: float
    exit_fee: float
    funding_pnl: float  # signed: negative = cost to the position, positive = received
    net_pnl: float
    net_r_multiple: float  # net_pnl / (stop_distance * quantity)


def compute_trade_pnl(
    *,
    direction_long: bool,
    entry_price: float,
    exit_price: float,
    quantity: float,
    stop_distance: float,
    taker_fee_rate: float,
    funding_accrued: float,
) -> TradePnL:
    """Compute complete PnL accounting for one closed trade.

    ``funding_accrued`` is the sum of signed funding_pnl across all
    funding events during the holding window (see funding_join.py).

    Assumes entry and exit fills already include slippage (see
    fills.py).
    """
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if stop_distance <= 0:
        raise ValueError("stop_distance must be positive")
    if taker_fee_rate < 0:
        raise ValueError("taker_fee_rate must be non-negative")

    if direction_long:
        gross = (exit_price - entry_price) * quantity
    else:
        gross = (entry_price - exit_price) * quantity

    entry_fee = entry_price * quantity * taker_fee_rate
    exit_fee = exit_price * quantity * taker_fee_rate
    net = gross - entry_fee - exit_fee + funding_accrued
    r_denom = stop_distance * quantity
    net_r = net / r_denom if r_denom > 0 else 0.0
    return TradePnL(
        gross_pnl=gross,
        entry_fee=entry_fee,
        exit_fee=exit_fee,
        funding_pnl=funding_accrued,
        net_pnl=net,
        net_r_multiple=net_r,
    )


@dataclass
class Accounting:
    """Running equity tracker across a simulation.

    ``starting_equity`` is fixed; ``equity`` updates after each
    trade close.

    The primary variant is FLAT: sizing continues to use
    ``starting_equity`` (this object does not alter sizing inputs).
    A compounding sensitivity variant would feed ``equity`` back
    into the engine's sizing call.
    """

    starting_equity: float
    equity: float
    realized_pnl: float = 0.0
    trades_closed: int = 0

    @classmethod
    def start(cls, starting_equity: float) -> Accounting:
        if starting_equity <= 0:
            raise ValueError("starting_equity must be positive")
        return cls(starting_equity=starting_equity, equity=starting_equity)

    def apply_trade(self, pnl: TradePnL) -> None:
        self.realized_pnl += pnl.net_pnl
        self.equity = self.starting_equity + self.realized_pnl
        self.trades_closed += 1

    @property
    def return_fraction(self) -> float:
        if self.starting_equity == 0:
            return 0.0
        return self.realized_pnl / self.starting_equity
