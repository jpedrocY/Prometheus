from __future__ import annotations

import pytest

from prometheus.research.backtest.accounting import Accounting, compute_trade_pnl


class TestComputeTradePnl:
    def test_long_winning_trade(self) -> None:
        pnl = compute_trade_pnl(
            direction_long=True,
            entry_price=100.0,
            exit_price=110.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0005,
            funding_accrued=0.0,
        )
        # Gross = (110-100)*1 = 10. Fees = 0.05 + 0.055 = 0.105. Net = 9.895.
        assert pnl.gross_pnl == pytest.approx(10.0)
        assert pnl.entry_fee == pytest.approx(0.05)
        assert pnl.exit_fee == pytest.approx(0.055)
        assert pnl.net_pnl == pytest.approx(10.0 - 0.05 - 0.055 + 0.0)
        assert pnl.net_r_multiple == pytest.approx(pnl.net_pnl / (5.0 * 1.0))

    def test_long_losing_trade(self) -> None:
        pnl = compute_trade_pnl(
            direction_long=True,
            entry_price=100.0,
            exit_price=95.0,
            quantity=2.0,
            stop_distance=5.0,
            taker_fee_rate=0.0005,
            funding_accrued=-0.1,  # paid funding
        )
        assert pnl.gross_pnl == pytest.approx(-10.0)
        # Net R should be roughly -1 R (modulo fees + funding).
        assert pnl.net_r_multiple < -1.0

    def test_short_winning_trade(self) -> None:
        pnl = compute_trade_pnl(
            direction_long=False,
            entry_price=100.0,
            exit_price=95.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0005,
            funding_accrued=0.0,
        )
        assert pnl.gross_pnl == pytest.approx(5.0)

    def test_funding_adds_to_net(self) -> None:
        pnl_no_funding = compute_trade_pnl(
            direction_long=True,
            entry_price=100.0,
            exit_price=100.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0,
            funding_accrued=0.0,
        )
        pnl_funding = compute_trade_pnl(
            direction_long=True,
            entry_price=100.0,
            exit_price=100.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0,
            funding_accrued=-0.5,
        )
        assert pnl_funding.net_pnl == pytest.approx(pnl_no_funding.net_pnl - 0.5)

    def test_invalid_inputs(self) -> None:
        with pytest.raises(ValueError):
            compute_trade_pnl(
                direction_long=True,
                entry_price=100.0,
                exit_price=105.0,
                quantity=0.0,
                stop_distance=5.0,
                taker_fee_rate=0.0,
                funding_accrued=0.0,
            )


class TestAccounting:
    def test_start_rejects_non_positive(self) -> None:
        with pytest.raises(ValueError):
            Accounting.start(starting_equity=0.0)

    def test_flat_accounting_accumulates(self) -> None:
        acc = Accounting.start(starting_equity=10_000.0)
        pnl_a = compute_trade_pnl(
            direction_long=True,
            entry_price=100.0,
            exit_price=110.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0,
            funding_accrued=0.0,
        )
        acc.apply_trade(pnl_a)
        assert acc.equity == pytest.approx(10_010.0)
        pnl_b = compute_trade_pnl(
            direction_long=True,
            entry_price=110.0,
            exit_price=105.0,
            quantity=1.0,
            stop_distance=5.0,
            taker_fee_rate=0.0,
            funding_accrued=0.0,
        )
        acc.apply_trade(pnl_b)
        assert acc.equity == pytest.approx(10_005.0)
        assert acc.trades_closed == 2
        assert acc.return_fraction == pytest.approx(5.0 / 10_000.0)
