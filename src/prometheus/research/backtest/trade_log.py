"""Trade record model + Parquet writer.

Schema matches Phase 3 Gate 1 plan §8.D.1.
"""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel, ConfigDict, Field

from prometheus.core.symbols import Symbol

from ..backtest.config import SlippageBucket
from .accounting import TradePnL
from .sizing import SizingLimitedBy

TRADE_LOG_SCHEMA_VERSION = "trade_log_v1"


class TradeRecord(BaseModel):
    """One row of the backtest trade log.

    All timestamps are UTC Unix milliseconds (canonical).
    """

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    trade_id: str = Field(min_length=1)
    symbol: Symbol
    direction: str  # LONG | SHORT
    signal_bar_open_time_ms: int
    entry_fill_time_ms: int
    entry_fill_price: float
    initial_stop: float
    stop_distance: float
    quantity: float
    notional_usdt: float
    sizing_limited_by: SizingLimitedBy
    realized_risk_usdt: float
    exit_reason: str  # STOP | TRAILING_BREACH | STAGNATION | END_OF_DATA
    exit_fill_time_ms: int
    exit_fill_price: float
    gross_pnl: float
    entry_fee: float
    exit_fee: float
    funding_pnl: float
    net_pnl: float
    net_r_multiple: float
    mfe_r: float
    mae_r: float
    bars_in_trade: int
    slippage_bucket: SlippageBucket
    fee_rate_assumption: float
    stop_was_gap_through: bool


def trade_record_to_dict(rec: TradeRecord) -> dict[str, object]:
    data = rec.model_dump()
    # StrEnums dump as the underlying string; keep explicit.
    data["sizing_limited_by"] = str(rec.sizing_limited_by.value)
    data["slippage_bucket"] = str(rec.slippage_bucket.value)
    data["symbol"] = str(rec.symbol.value)
    return data


def trade_record_to_parquet_table(records: list[TradeRecord]) -> pa.Table:
    """Convert a list of TradeRecord into a pyarrow.Table."""
    rows = [trade_record_to_dict(r) for r in records]
    schema = pa.schema(
        [
            ("trade_id", pa.string()),
            ("symbol", pa.string()),
            ("direction", pa.string()),
            ("signal_bar_open_time_ms", pa.int64()),
            ("entry_fill_time_ms", pa.int64()),
            ("entry_fill_price", pa.float64()),
            ("initial_stop", pa.float64()),
            ("stop_distance", pa.float64()),
            ("quantity", pa.float64()),
            ("notional_usdt", pa.float64()),
            ("sizing_limited_by", pa.string()),
            ("realized_risk_usdt", pa.float64()),
            ("exit_reason", pa.string()),
            ("exit_fill_time_ms", pa.int64()),
            ("exit_fill_price", pa.float64()),
            ("gross_pnl", pa.float64()),
            ("entry_fee", pa.float64()),
            ("exit_fee", pa.float64()),
            ("funding_pnl", pa.float64()),
            ("net_pnl", pa.float64()),
            ("net_r_multiple", pa.float64()),
            ("mfe_r", pa.float64()),
            ("mae_r", pa.float64()),
            ("bars_in_trade", pa.int64()),
            ("slippage_bucket", pa.string()),
            ("fee_rate_assumption", pa.float64()),
            ("stop_was_gap_through", pa.bool_()),
        ]
    )
    columns: dict[str, list[object]] = {name: [] for name in schema.names}
    for row in rows:
        for name in schema.names:
            columns[name].append(row[name])
    arrays = [
        pa.array(columns[name], type=field.type)
        for name, field in zip(schema.names, schema, strict=True)
    ]
    return pa.Table.from_arrays(arrays, schema=schema)


def write_trade_log(records: list[TradeRecord], dest_parquet: Path, dest_json: Path) -> None:
    """Write the trade log as both Parquet and JSON.

    Parquet is the canonical artifact; JSON is a sidecar for easy
    human review and quick diffing in PRs.
    """
    dest_parquet.parent.mkdir(parents=True, exist_ok=True)
    dest_json.parent.mkdir(parents=True, exist_ok=True)
    table = trade_record_to_parquet_table(records)
    pq.write_table(table, dest_parquet)
    payload = {
        "schema_version": TRADE_LOG_SCHEMA_VERSION,
        "trade_count": len(records),
        "trades": [trade_record_to_dict(r) for r in records],
    }
    dest_json.write_text(json.dumps(payload, indent=2, sort_keys=True))


def trade_pnl_fields_to_record_args(pnl: TradePnL) -> dict[str, float]:
    """Helper: build the TradeRecord PnL subset from a TradePnL object."""
    return {
        "gross_pnl": pnl.gross_pnl,
        "entry_fee": pnl.entry_fee,
        "exit_fee": pnl.exit_fee,
        "funding_pnl": pnl.funding_pnl,
        "net_pnl": pnl.net_pnl,
        "net_r_multiple": pnl.net_r_multiple,
    }
