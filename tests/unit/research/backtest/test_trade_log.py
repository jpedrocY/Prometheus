from __future__ import annotations

import json

import pyarrow.parquet as pq

from prometheus.core.symbols import Symbol
from prometheus.research.backtest.config import SlippageBucket
from prometheus.research.backtest.sizing import SizingLimitedBy
from prometheus.research.backtest.trade_log import (
    TradeRecord,
    trade_record_to_parquet_table,
    write_trade_log,
)


def _record(trade_id: str = "t-0001") -> TradeRecord:
    return TradeRecord(
        trade_id=trade_id,
        symbol=Symbol.BTCUSDT,
        direction="LONG",
        signal_bar_open_time_ms=1_000_000,
        entry_fill_time_ms=1_000_900,
        entry_fill_price=50_000.0,
        initial_stop=49_000.0,
        stop_distance=1000.0,
        quantity=0.01,
        notional_usdt=500.0,
        sizing_limited_by=SizingLimitedBy.STOP_RISK,
        realized_risk_usdt=10.0,
        exit_reason="STOP",
        exit_fill_time_ms=2_000_000,
        exit_fill_price=49_000.0,
        gross_pnl=-10.0,
        entry_fee=0.25,
        exit_fee=0.245,
        funding_pnl=-0.05,
        net_pnl=-10.545,
        net_r_multiple=-1.0545,
        mfe_r=0.3,
        mae_r=1.0,
        bars_in_trade=5,
        slippage_bucket=SlippageBucket.MEDIUM,
        fee_rate_assumption=0.0005,
        stop_was_gap_through=False,
    )


def test_single_record_round_trip(tmp_path) -> None:
    rec = _record()
    dest_parquet = tmp_path / "t.parquet"
    dest_json = tmp_path / "t.json"
    write_trade_log([rec], dest_parquet, dest_json)
    assert dest_parquet.is_file()
    assert dest_json.is_file()
    # Parquet read-back
    table = pq.read_table(dest_parquet)
    assert table.num_rows == 1
    row = table.to_pylist()[0]
    assert row["trade_id"] == "t-0001"
    assert row["symbol"] == "BTCUSDT"
    assert row["direction"] == "LONG"
    # JSON sidecar sanity
    payload = json.loads(dest_json.read_text())
    assert payload["schema_version"] == "trade_log_v1"
    assert payload["trade_count"] == 1
    assert payload["trades"][0]["trade_id"] == "t-0001"


def test_multiple_records_preserve_order(tmp_path) -> None:
    recs = [_record(f"t-{i:04d}") for i in range(5)]
    dest_parquet = tmp_path / "t.parquet"
    dest_json = tmp_path / "t.json"
    write_trade_log(recs, dest_parquet, dest_json)
    table = pq.read_table(dest_parquet)
    ids = table.column("trade_id").to_pylist()
    assert ids == [f"t-{i:04d}" for i in range(5)]


def test_empty_records_produces_empty_parquet(tmp_path) -> None:
    write_trade_log([], tmp_path / "t.parquet", tmp_path / "t.json")
    table = pq.read_table(tmp_path / "t.parquet")
    assert table.num_rows == 0


def test_table_schema_has_expected_columns() -> None:
    table = trade_record_to_parquet_table([_record()])
    expected = {
        "trade_id",
        "symbol",
        "direction",
        "signal_bar_open_time_ms",
        "entry_fill_time_ms",
        "entry_fill_price",
        "initial_stop",
        "stop_distance",
        "quantity",
        "notional_usdt",
        "sizing_limited_by",
        "realized_risk_usdt",
        "exit_reason",
        "exit_fill_time_ms",
        "exit_fill_price",
        "gross_pnl",
        "entry_fee",
        "exit_fee",
        "funding_pnl",
        "net_pnl",
        "net_r_multiple",
        "mfe_r",
        "mae_r",
        "bars_in_trade",
        "slippage_bucket",
        "fee_rate_assumption",
        "stop_was_gap_through",
        # R2 metadata (Phase 2u, Gate 2 amended; defaults preserve
        # H0/R3/R1a/R1b-narrow trade-log economic columns bit-for-bit).
        "registration_bar_index",
        "fill_bar_index",
        "time_to_fill_bars",
        "pullback_level_at_registration",
        "structural_stop_level_at_registration",
        "atr_at_signal",
        "fill_price",
        "r_distance",
        "cancellation_reason",
        # F1 mean-reversion-after-overextension metadata (Phase 3d-B1;
        # NaN defaults preserve V1 trade-log columns bit-for-bit).
        "overextension_magnitude_at_signal",
        "frozen_target_value",
        "entry_to_target_distance_atr",
        "stop_distance_at_signal_atr",
    }
    assert set(table.schema.names) == expected
