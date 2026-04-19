from __future__ import annotations

import pytest

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.cli import build_parser, config_from_args
from prometheus.research.backtest.config import BacktestAdapter, SlippageBucket


def test_parser_minimal() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--experiment",
            "exp-1",
            "--run-id",
            "r-1",
            "--symbols",
            "BTCUSDT",
            "--window-start-ms",
            "1000000",
            "--window-end-ms",
            "2000000",
            "--klines-root",
            "k",
            "--bars-1h-root",
            "h",
            "--mark-root",
            "m",
            "--funding-root",
            "f",
            "--exchange-info",
            "ei.json",
            "--reports-root",
            "out",
        ]
    )
    cfg = config_from_args(args)
    assert cfg.symbols == (Symbol.BTCUSDT,)
    assert cfg.slippage_bucket == SlippageBucket.MEDIUM
    assert cfg.sizing_equity_usdt == 10_000.0
    assert cfg.risk_fraction == 0.0025
    assert cfg.adapter == BacktestAdapter.FAKE


def test_parser_rejects_unknown_symbol() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "--experiment",
                "x",
                "--run-id",
                "r",
                "--symbols",
                "SOLUSDT",
                "--window-start-ms",
                "1",
                "--window-end-ms",
                "2",
                "--klines-root",
                ".",
                "--bars-1h-root",
                ".",
                "--mark-root",
                ".",
                "--funding-root",
                ".",
                "--exchange-info",
                "ei.json",
                "--reports-root",
                "o",
            ]
        )


def test_parser_symbols_are_tuple_unique() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "--experiment",
            "x",
            "--run-id",
            "r",
            "--symbols",
            "BTCUSDT,ETHUSDT",
            "--window-start-ms",
            "1",
            "--window-end-ms",
            "2",
            "--klines-root",
            ".",
            "--bars-1h-root",
            ".",
            "--mark-root",
            ".",
            "--funding-root",
            ".",
            "--exchange-info",
            "ei.json",
            "--reports-root",
            "o",
        ]
    )
    cfg = config_from_args(args)
    assert cfg.symbols == (Symbol.BTCUSDT, Symbol.ETHUSDT)
