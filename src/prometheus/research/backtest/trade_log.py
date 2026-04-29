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

    # ----- R2 pullback-retest entry metadata (Phase 2u, Gate 2 amended) -----
    # All fields default to H0-equivalent values so MARKET_NEXT_BAR_OPEN
    # (H0/R3/R1a/R1b-narrow) trade records are unchanged in their
    # economically-meaningful columns. Under H0 default, the registration
    # bar IS the signal bar, time_to_fill_bars is 0, the pullback level is
    # not applicable (NaN), the structural stop level equals initial_stop,
    # the ATR at signal is the same value the existing strategy uses
    # for the sizing pipeline, the fill price equals entry_fill_price, and
    # the R-distance is stop_distance / atr_at_signal. The R2 path
    # populates these with the actual frozen-at-registration values.
    #
    # ``cancellation_reason`` is always None for filled trades (R2 or H0);
    # it is reserved for sidecar cancellation/expiry records that 2w-B will
    # add to the per-symbol funnel/diagnostic reports (not to the trade log).
    registration_bar_index: int = -1
    fill_bar_index: int = -1
    time_to_fill_bars: int = 0
    pullback_level_at_registration: float = float("nan")
    structural_stop_level_at_registration: float = float("nan")
    atr_at_signal: float = float("nan")
    fill_price: float = float("nan")
    r_distance: float = float("nan")
    cancellation_reason: str | None = None

    # ----- F1 mean-reversion-after-overextension metadata (Phase 3d-B1) -----
    # Populated only on F1-family trades (strategy_family=
    # MEAN_REVERSION_OVEREXTENSION). For V1 (H0/R3/R1a/R1b-narrow/R2)
    # rows these stay at NaN defaults so the parquet schema remains
    # additive and existing reports are unaffected. Per Phase 3c §4.6
    # diagnostic-fields list:
    #   - overextension_magnitude_at_signal:
    #         |close(B) - close(B-8)| / ATR(20)(B)
    #   - frozen_target_value:
    #         SMA(8)(B) frozen at signal-time bar B's close
    #   - entry_to_target_distance_atr:
    #         |entry_fill_price - frozen_target_value| / ATR(20)(B)
    #   - stop_distance_at_signal_atr:
    #         stop_distance / ATR(20)(B), evaluated on the de-slipped
    #         raw open(B+1) per Phase 3b §4.9 / Phase 3c §11.4
    overextension_magnitude_at_signal: float = float("nan")
    frozen_target_value: float = float("nan")
    entry_to_target_distance_atr: float = float("nan")
    stop_distance_at_signal_atr: float = float("nan")

    # ----- D1-A funding-aware directional metadata (Phase 3i-B1) -----
    # Populated only on D1-A-family trades (strategy_family=
    # FUNDING_AWARE_DIRECTIONAL). For V1 / F1 rows these stay at
    # None / NaN / -1 defaults so the parquet schema remains additive
    # and existing reports are unaffected. Per Phase 3g §9.4 + Phase
    # 3h §5.7 fields list. The ``entry_to_target_distance_atr`` and
    # ``stop_distance_at_signal_atr`` fields above are reused for D1-A
    # (semantically the same: distance to target / stop in ATR
    # multiples). For D1-A by construction:
    #   entry_to_target_distance_atr = 2.0 (target = +2.0R per Phase 3g §5.6.5)
    #   stop_distance_at_signal_atr  = 1.0 (stop = 1.0 × ATR per Phase 3g §6.7)
    funding_event_id_at_signal: str | None = None
    funding_z_score_at_signal: float = float("nan")
    funding_rate_at_signal: float = float("nan")
    bars_since_funding_event_at_signal: int = -1


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
            # R2 pullback-retest entry metadata (Phase 2u, Gate 2 amended).
            # All fields default to H0-equivalent values for non-R2 paths;
            # the parquet schema carries them so a future R2 run shares
            # the same trade-log shape as H0/R3/R1a/R1b-narrow.
            ("registration_bar_index", pa.int64()),
            ("fill_bar_index", pa.int64()),
            ("time_to_fill_bars", pa.int64()),
            ("pullback_level_at_registration", pa.float64()),
            ("structural_stop_level_at_registration", pa.float64()),
            ("atr_at_signal", pa.float64()),
            ("fill_price", pa.float64()),
            ("r_distance", pa.float64()),
            ("cancellation_reason", pa.string()),
            # F1 mean-reversion-after-overextension diagnostic fields
            # (Phase 3d-B1). NaN for V1 rows; populated by the F1
            # engine path per Phase 3c §4.6.
            ("overextension_magnitude_at_signal", pa.float64()),
            ("frozen_target_value", pa.float64()),
            ("entry_to_target_distance_atr", pa.float64()),
            ("stop_distance_at_signal_atr", pa.float64()),
            # D1-A funding-aware directional diagnostic fields
            # (Phase 3i-B1). None/NaN/-1 for V1 / F1 rows; populated
            # by the D1-A engine path per Phase 3g §9.4 + Phase 3h §5.7.
            ("funding_event_id_at_signal", pa.string()),
            ("funding_z_score_at_signal", pa.float64()),
            ("funding_rate_at_signal", pa.float64()),
            ("bars_since_funding_event_at_signal", pa.int64()),
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
