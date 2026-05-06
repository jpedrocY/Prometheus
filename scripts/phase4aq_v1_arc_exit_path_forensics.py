"""Phase 4aq - V1-Arc Exit-Path Forensic Computation.

Authority: Phase 4ap (V1-arc exit-path forensic plan; merged 4cad1f6).
Phase 4ao (exit-path methodology / artefact harmonization; merged
6c59c5b). Phase 4an (historical exit-path inventory; merged a73c00b).
Phase 4am (backtest-logic audit; merged dfaa26a). Phase 4al (exit
architecture / trade-management M0 admissibility; merged f97f850).
Phase 4ak (M0 governance adoption; merged 2c626bc).

Brief: docs-and-code forensic computation. Reads only existing local
V1-arc trade-log artefacts under data/derived/backtests/phase-2*. No
network I/O. No Binance API. No data.binance.vision. No authenticated
REST. No private endpoints. No public-endpoint code calls. No user
stream / WebSocket / listenKey. No credentials. No `.env`. No MCP /
Graphify / `.mcp.json`. No data acquisition. No backtest execution. No
historical-strategy-script execution. No data modification. No manifest
modification. No existing-trade-log modification. No `src/prometheus/`
modification. No test modification. No retained verdict revised. No
project lock changed. No M0 governance modified.

Population scope (Phase 4ap §6 / §7):
    Included: H0, R3, R1a, R1b-narrow, R2.
    Excluded: F1, D1-A, V2, G1, C1, 5m research thread.

R3 inclusion is descriptive baseline-of-record context only. No R3
optimization. No R3-prime. No R3 rescue. No baseline-of-record revision.
No conversion of R3 forensic findings into parameters, thresholds,
entry logic, exit logic, or new strategy candidates.

Allowlisted V1-arc artefact directories (Phase 4ap §10):

    H0:
      phase-2e-baseline
      phase-2g-wave1-h0-r
    R3:
      phase-2l-r3-r
      phase-2l-r3-r-slip=LOW
      phase-2l-r3-r-slip=HIGH
      phase-2l-r3-r-stop=TRADE_PRICE
      phase-2l-r3-v
    R1a:
      phase-2m-r1a-r1a_plus_r3-r
      phase-2m-r1a-r1a_plus_r3-r-slip=LOW
      phase-2m-r1a-r1a_plus_r3-r-slip=HIGH
      phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE
      phase-2m-r1a-r1a_plus_r3-v
    R1b-narrow:
      phase-2s-r1b-r1b_narrow-r
      phase-2s-r1b-r1b_narrow-r-slip=LOW
      phase-2s-r1b-r1b_narrow-r-slip=HIGH
      phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE
      phase-2s-r1b-r1b_narrow-v
    R2:
      phase-2w-r2-r2_r3-r
      phase-2w-r2-r2_r3-r-slip=LOW
      phase-2w-r2-r2_r3-r-slip=HIGH
      phase-2w-r2-r2_r3-r-stop=TRADE_PRICE
      phase-2w-r2-r2_r3-r-fill=limit-at-pullback
      phase-2w-r2-r2_r3-v

Phase 4ap-locked governance (binding for this script):

    timeframe                      = 15m bar-extreme only
    stop_trigger_domain (inferred) = trade_price_backtest
    cost_lock                      = §11.6 = 8 bps slippage per side
    fee_assumption                 = trade-record fee_rate_assumption
    no lower-timeframe data        = no 5m / 1m / aggTrades / tick / mark-price
    no rerun                       = no historical script re-execution
    no acquisition                 = no data download
    no modification                = no existing artefact / manifest / source modified
    fail-closed boundaries         = SC-1..SC-11 (Phase 4ap §17)

Output root (default):
    data/research/phase4aq/

This is a local research output directory. It is gitignored (see
.gitignore). Outputs are reproducible from this script and existing
V1-arc trade-log artefacts; they are not committed to git.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
import sys
from collections import OrderedDict, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

# ---------------------------------------------------------------------------
# Phase 4aq locked configuration
# ---------------------------------------------------------------------------

PHASE_ID = "4aq"
PHASE_NAME = "V1-Arc Exit-Path Forensic Computation"

# Phase 4ap §10 allowlist: each entry maps a directory name to the canonical
# Phase 4ap labels (population, window_type, cost_cell, stop_domain_variant,
# fill_variant). Cost-cell labels at the directory level reflect the
# directory naming convention. Per-trade `slippage_bucket` is preserved as
# the ground-truth per-trade cost cell.
DIRECTORY_ALLOWLIST: dict[str, dict[str, str]] = OrderedDict(
    [
        # H0
        (
            "phase-2e-baseline",
            {
                "population": "H0",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2g-wave1-h0-r",
            {
                "population": "H0",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        # R3
        (
            "phase-2l-r3-r",
            {
                "population": "R3",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2l-r3-r-slip=LOW",
            {
                "population": "R3",
                "window_type": "R",
                "cost_cell": "LOW",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2l-r3-r-slip=HIGH",
            {
                "population": "R3",
                "window_type": "R",
                "cost_cell": "HIGH",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2l-r3-r-stop=TRADE_PRICE",
            {
                "population": "R3",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "TRADE_PRICE",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2l-r3-v",
            {
                "population": "R3",
                "window_type": "V",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        # R1a
        (
            "phase-2m-r1a-r1a_plus_r3-r",
            {
                "population": "R1a",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2m-r1a-r1a_plus_r3-r-slip=LOW",
            {
                "population": "R1a",
                "window_type": "R",
                "cost_cell": "LOW",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2m-r1a-r1a_plus_r3-r-slip=HIGH",
            {
                "population": "R1a",
                "window_type": "R",
                "cost_cell": "HIGH",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE",
            {
                "population": "R1a",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "TRADE_PRICE",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2m-r1a-r1a_plus_r3-v",
            {
                "population": "R1a",
                "window_type": "V",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        # R1b-narrow
        (
            "phase-2s-r1b-r1b_narrow-r",
            {
                "population": "R1b-narrow",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2s-r1b-r1b_narrow-r-slip=LOW",
            {
                "population": "R1b-narrow",
                "window_type": "R",
                "cost_cell": "LOW",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2s-r1b-r1b_narrow-r-slip=HIGH",
            {
                "population": "R1b-narrow",
                "window_type": "R",
                "cost_cell": "HIGH",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE",
            {
                "population": "R1b-narrow",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "TRADE_PRICE",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2s-r1b-r1b_narrow-v",
            {
                "population": "R1b-narrow",
                "window_type": "V",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        # R2
        (
            "phase-2w-r2-r2_r3-r",
            {
                "population": "R2",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2w-r2-r2_r3-r-slip=LOW",
            {
                "population": "R2",
                "window_type": "R",
                "cost_cell": "LOW",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2w-r2-r2_r3-r-slip=HIGH",
            {
                "population": "R2",
                "window_type": "R",
                "cost_cell": "HIGH",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2w-r2-r2_r3-r-stop=TRADE_PRICE",
            {
                "population": "R2",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "TRADE_PRICE",
                "fill_variant": "default",
            },
        ),
        (
            "phase-2w-r2-r2_r3-r-fill=limit-at-pullback",
            {
                "population": "R2",
                "window_type": "R",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "limit-at-pullback",
            },
        ),
        (
            "phase-2w-r2-r2_r3-v",
            {
                "population": "R2",
                "window_type": "V",
                "cost_cell": "default",
                "stop_domain_variant": "default",
                "fill_variant": "default",
            },
        ),
    ]
)

INCLUDED_POPULATIONS = ("H0", "R3", "R1a", "R1b-narrow", "R2")
EXCLUDED_POPULATION_TOKENS = ("f1", "d1a", "d1-a", "v2", "g1", "c1", "5m")

# Phase 4ap §11: required trade-log fields. The script fails closed if any
# required field is missing.
REQUIRED_FIELDS = (
    "trade_id",
    "direction",
    "symbol",
    "entry_fill_time_ms",
    "exit_fill_time_ms",
    "entry_fill_price",
    "exit_fill_price",
    "initial_stop",
    "stop_distance",
    "realized_risk_usdt",
    "gross_pnl",
    "net_pnl",
    "net_r_multiple",
    "entry_fee",
    "exit_fee",
    "funding_pnl",
    "fee_rate_assumption",
    "slippage_bucket",
    "exit_reason",
    "bars_in_trade",
    "mfe_r",
    "mae_r",
    "stop_was_gap_through",
)
OPTIONAL_FIELDS = ("quantity", "notional_usdt", "schema_version")

# Phase 4ap §14: §11.6 cost lock per side.
SLIPPAGE_BPS_PER_SIDE = {"LOW": 1, "MEDIUM": 4, "HIGH": 8}

# Phase 4al §14.C ambiguity bands (descriptive heuristic only; not gates).
AMBIGUITY_BAND_5M_USABLE_LOW = 0.02  # < 2%
AMBIGUITY_BAND_5M_USABLE_HIGH = 0.10  # 2%-10%
AMBIGUITY_BAND_5M_TOO_COARSE = 0.20  # > 20%


# ---------------------------------------------------------------------------
# Logging helpers (stdout only; no file logger; no secret leakage)
# ---------------------------------------------------------------------------


def info(msg: str) -> None:
    print(f"[phase4aq] {msg}")


def warn(msg: str) -> None:
    print(f"[phase4aq][warn] {msg}", file=sys.stderr)


class FailClosedError(RuntimeError):
    """Raised when a Phase 4ap fail-closed precondition is violated."""


# ---------------------------------------------------------------------------
# Discovery and loading
# ---------------------------------------------------------------------------


def latest_run_dir(directory: Path) -> Path | None:
    """Return the lexicographically-largest immediate timestamped subdir.

    Phase 2 backtest convention names runs `YYYY-MM-DDTHH-MM-SSZ`, which
    sort correctly under lexicographic ordering. The latest run is taken
    per directory.
    """
    candidates = [p for p in directory.iterdir() if p.is_dir()]
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.name)
    return candidates[-1]


def select_canonical_ledger(symbol_dir: Path) -> tuple[Path, str] | None:
    """Return (path, source_format) for canonical ledger.

    Phase 4ap §10 / brief §21: prefer Parquet, fall back to JSON. Never
    load both. Returns None if neither is present.
    """
    parquet = symbol_dir / "trade_log.parquet"
    if parquet.is_file():
        return (parquet, "parquet")
    json_path = symbol_dir / "trade_log.json"
    if json_path.is_file():
        return (json_path, "json")
    return None


def load_trade_log_parquet(path: Path) -> list[dict[str, Any]]:
    table = pq.read_table(path)
    rows: list[dict[str, Any]] = []
    columns = table.column_names
    pylists = {col: table.column(col).to_pylist() for col in columns}
    n = table.num_rows
    for i in range(n):
        rec: dict[str, Any] = {col: pylists[col][i] for col in columns}
        rows.append(rec)
    return rows


def load_trade_log_json(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "trades" in data and isinstance(data["trades"], list):
            return data["trades"]
        raise FailClosedError(
            f"Unrecognized JSON trade-log structure at {path}; "
            f"expected list or dict with 'trades' key."
        )
    raise FailClosedError(f"Unrecognized JSON trade-log type at {path}: {type(data).__name__}")


def validate_required_fields(rows: list[dict[str, Any]], source: Path) -> list[str]:
    """Return list of missing-field names (empty if all present).

    Field is considered present if at least one row contains the key.
    Phase 4ap SC-2: missing required field is fail-closed.
    """
    if not rows:
        return []
    keys: set[str] = set()
    for r in rows:
        keys.update(r.keys())
    missing = [f for f in REQUIRED_FIELDS if f not in keys]
    return missing


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------


def is_finite(x: Any) -> bool:
    try:
        return x is not None and math.isfinite(float(x))
    except (TypeError, ValueError):
        return False


def safe_div(num: Any, den: Any) -> float | None:
    if not (is_finite(num) and is_finite(den)):
        return None
    if float(den) == 0.0:
        return None
    return float(num) / float(den)


def compute_metrics(trade: dict[str, Any]) -> dict[str, Any]:
    """Compute Phase 4ap §12 descriptive metrics for one trade.

    All metrics are descriptive. None of these implies a strategy signal,
    a parameter recommendation, an entry rule, an exit rule, a regime
    filter, or any rescue framing.
    """
    realized_risk = trade.get("realized_risk_usdt")
    gross_pnl = trade.get("gross_pnl")
    net_pnl = trade.get("net_pnl")
    entry_fee = trade.get("entry_fee")
    exit_fee = trade.get("exit_fee")
    funding_pnl = trade.get("funding_pnl")
    mfe_r = trade.get("mfe_r")
    mae_r = trade.get("mae_r")
    net_r = trade.get("net_r_multiple")
    notional = trade.get("notional_usdt")
    quantity = trade.get("quantity")
    entry_price = trade.get("entry_fill_price")
    bucket = trade.get("slippage_bucket")
    exit_reason = trade.get("exit_reason")
    bars_in_trade = trade.get("bars_in_trade")

    fees_sum: float | None = None
    if is_finite(entry_fee) and is_finite(exit_fee):
        fees_sum = float(entry_fee) + float(exit_fee)

    gross_R = safe_div(gross_pnl, realized_risk)
    cost_in_R: float | None = None
    if (
        is_finite(gross_pnl)
        and is_finite(net_pnl)
        and is_finite(realized_risk)
        and float(realized_risk) != 0.0
    ):
        cost_in_R = (float(gross_pnl) - float(net_pnl)) / float(realized_risk)
    fee_in_R = safe_div(fees_sum, realized_risk)
    funding_in_R = safe_div(funding_pnl, realized_risk)

    # Phase 4ap §12: estimated_slippage_in_R is descriptive ONLY; round-trip
    # slippage = 2 * per_side bps mapped from slippage_bucket.
    estimated_slippage_in_R: float | None = None
    estimated_slippage_basis: str = "NA"
    bps_per_side = SLIPPAGE_BPS_PER_SIDE.get(str(bucket).upper()) if bucket is not None else None
    if bps_per_side is not None and is_finite(realized_risk) and float(realized_risk) != 0.0:
        if is_finite(notional):
            est_notional = float(notional)
            estimated_slippage_basis = "notional_usdt"
        elif is_finite(quantity) and is_finite(entry_price):
            est_notional = abs(float(quantity)) * float(entry_price)
            estimated_slippage_basis = "abs(quantity)*entry_fill_price"
        else:
            est_notional = None
            estimated_slippage_basis = "missing_notional_and_quantity"
        if est_notional is not None:
            round_trip_bps = 2.0 * bps_per_side
            slip_usdt = est_notional * round_trip_bps / 10_000.0
            estimated_slippage_in_R = slip_usdt / float(realized_risk)

    cost_reconciliation_note = (
        "estimated; cost_in_R is exact-from-fields "
        "(gross_pnl - net_pnl) / realized_risk_usdt; "
        "fee_in_R and funding_in_R are exact-from-fields; "
        "estimated_slippage_in_R is descriptive only and uses "
        "slippage_bucket and notional/quantity; "
        "the identity "
        "cost_in_R == fee_in_R + estimated_slippage_in_R + funding_in_R "
        "is NOT asserted."
    )

    reached_1R = bool(is_finite(mfe_r) and float(mfe_r) >= 1.0)
    reached_2R = bool(is_finite(mfe_r) and float(mfe_r) >= 2.0)
    reached_3R = bool(is_finite(mfe_r) and float(mfe_r) >= 3.0)

    mfe_capture_ratio: float | None = None
    if is_finite(mfe_r) and float(mfe_r) > 0.0 and is_finite(net_r):
        mfe_capture_ratio = float(net_r) / float(mfe_r)

    giveback_from_mfe: float | None = None
    if is_finite(mfe_r) and is_finite(net_r):
        giveback_from_mfe = float(mfe_r) - float(net_r)

    # Phase 4ap §12: favorable-before-stop flag for STOP exits is a proxy
    # only; the existing 15m schema does not preserve intrabar event order.
    favorable_excursion_before_stop_proxy: bool | None
    is_stop = isinstance(exit_reason, str) and "STOP" in exit_reason.upper()
    if is_stop and is_finite(mfe_r):
        favorable_excursion_before_stop_proxy = float(mfe_r) > 0.0
    else:
        favorable_excursion_before_stop_proxy = None

    # Phase 4ap §12: adverse-before-favorable cannot be determined from
    # final MFE/MAE alone. Mark NOT_AUDITABLE.
    adverse_before_favorable_flag = "NOT_AUDITABLE_FROM_EXISTING_FIELDS"

    bar_resolution_ambiguity_flag = bool(
        is_finite(bars_in_trade) and int(bars_in_trade) == 0
    )

    return {
        "MFE_R": float(mfe_r) if is_finite(mfe_r) else None,
        "MAE_R": float(mae_r) if is_finite(mae_r) else None,
        "net_R": float(net_r) if is_finite(net_r) else None,
        "gross_R": gross_R,
        "cost_in_R": cost_in_R,
        "fee_in_R": fee_in_R,
        "funding_in_R": funding_in_R,
        "estimated_slippage_in_R": estimated_slippage_in_R,
        "estimated_slippage_basis": estimated_slippage_basis,
        "cost_reconciliation_note": cost_reconciliation_note,
        "reached_plus_1R_flag": reached_1R,
        "reached_plus_2R_flag": reached_2R,
        "reached_plus_3R_flag": reached_3R,
        "mfe_capture_ratio": mfe_capture_ratio,
        "giveback_from_mfe": giveback_from_mfe,
        "favorable_excursion_before_stop_proxy": favorable_excursion_before_stop_proxy,
        "adverse_before_favorable_flag": adverse_before_favorable_flag,
        "bar_resolution_ambiguity_flag": bar_resolution_ambiguity_flag,
    }


# ---------------------------------------------------------------------------
# Aggregation helpers
# ---------------------------------------------------------------------------


def quantile(values: list[float], q: float) -> float | None:
    """Linear-interpolation quantile. Returns None for empty input."""
    if not values:
        return None
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = q * (len(s) - 1)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return s[lo]
    frac = pos - lo
    return s[lo] * (1 - frac) + s[hi] * frac


def numeric_summary(values: list[float | None]) -> dict[str, Any]:
    finite = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    if not finite:
        return {
            "n": 0,
            "n_nonfinite": sum(1 for v in values if v is None or not math.isfinite(float(v))),
            "mean": None,
            "stdev": None,
            "min": None,
            "p10": None,
            "p25": None,
            "p50": None,
            "p75": None,
            "p90": None,
            "p95": None,
            "p99": None,
            "max": None,
        }
    n = len(finite)
    return {
        "n": n,
        "n_nonfinite": sum(1 for v in values if v is None or not math.isfinite(float(v))),
        "mean": statistics.fmean(finite),
        "stdev": statistics.pstdev(finite) if n >= 2 else 0.0,
        "min": min(finite),
        "p10": quantile(finite, 0.10),
        "p25": quantile(finite, 0.25),
        "p50": quantile(finite, 0.50),
        "p75": quantile(finite, 0.75),
        "p90": quantile(finite, 0.90),
        "p95": quantile(finite, 0.95),
        "p99": quantile(finite, 0.99),
        "max": max(finite),
    }


def fmt_float(x: Any) -> str:
    if x is None:
        return ""
    try:
        f = float(x)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(f):
        return ""
    return f"{f:.6f}"


def write_csv(path: Path, header: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Phase 4aq V1-arc exit-path forensic computation (descriptive only)"
    )
    p.add_argument(
        "--backtests-root",
        default="data/derived/backtests",
        help=(
            "Root directory of historical V1-arc backtest artefacts "
            "(default: data/derived/backtests)."
        ),
    )
    p.add_argument(
        "--output-root",
        default="data/research/phase4aq",
        help=(
            "Output directory for Phase 4aq local research outputs "
            "(default: data/research/phase4aq)."
        ),
    )
    return p.parse_args()


def build_loaded_artifacts_manifest(
    backtests_root: Path,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Discover allowlisted V1-arc directories and pick the latest run.

    Returns (manifest_rows, fail_closed_messages). manifest_rows is one
    row per (directory, run_id, symbol, ledger_path).
    """
    manifest_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    for dir_name, labels in DIRECTORY_ALLOWLIST.items():
        dir_path = backtests_root / dir_name
        if not dir_path.is_dir():
            failures.append(f"MISSING_ALLOWLISTED_DIR: {dir_path}")
            continue
        run_dir = latest_run_dir(dir_path)
        if run_dir is None:
            failures.append(f"NO_RUN_SUBDIR: {dir_path}")
            continue
        for symbol in ("BTCUSDT", "ETHUSDT"):
            symbol_dir = run_dir / symbol
            if not symbol_dir.is_dir():
                failures.append(f"MISSING_SYMBOL_DIR: {symbol_dir}")
                continue
            sel = select_canonical_ledger(symbol_dir)
            if sel is None:
                failures.append(f"NO_LEDGER_FOUND: {symbol_dir}")
                continue
            ledger_path, fmt = sel
            manifest_rows.append(
                {
                    "run_family": dir_name,
                    "run_id": run_dir.name,
                    "symbol": symbol,
                    "selected_source_format": fmt,
                    "selected_source_path": str(ledger_path).replace("\\", "/"),
                    "population": labels["population"],
                    "window_type": labels["window_type"],
                    "cost_cell": labels["cost_cell"],
                    "stop_domain_variant": labels["stop_domain_variant"],
                    "fill_variant": labels["fill_variant"],
                    "stop_trigger_domain_inferred": "trade_price_backtest",
                    "timeframe": "15m",
                }
            )
    return manifest_rows, failures


def excluded_population_check(rows: list[dict[str, Any]]) -> str | None:
    """Phase 4ap SC-5: scan run_family for excluded population tokens."""
    for r in rows:
        rf = str(r.get("run_family", "")).lower()
        for tok in EXCLUDED_POPULATION_TOKENS:
            # Token-with-dash boundaries to avoid false positives like
            # 'phase-2g-wave1-h-c1-r' containing 'c1'. The allowlist already
            # excludes those, so scan run_family fully.
            if tok in rf and not any(
                allowed in rf
                for allowed in (
                    "phase-2e-baseline",
                    "phase-2g-wave1-h0-r",
                    "phase-2l-r3",
                    "phase-2m-r1a",
                    "phase-2s-r1b",
                    "phase-2w-r2",
                )
            ):
                return (
                    "EXCLUDED_POPULATION_TOKEN_DETECTED: "
                    f"run_family={r.get('run_family')} token={tok}"
                )
    return None


def load_all_trades(
    manifest_rows: list[dict[str, Any]], backtests_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Load all trades. Returns (labelled_trade_rows, schema_validation_rows)."""
    labelled: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    for art in manifest_rows:
        ledger_path = Path(art["selected_source_path"])
        fmt = art["selected_source_format"]
        if fmt == "parquet":
            trades = load_trade_log_parquet(ledger_path)
        else:
            trades = load_trade_log_json(ledger_path)
        missing = validate_required_fields(trades, ledger_path)
        present_optional = []
        if trades:
            keys = set()
            for t in trades:
                keys.update(t.keys())
            present_optional = [f for f in OPTIONAL_FIELDS if f in keys]
        schema_rows.append(
            {
                "run_family": art["run_family"],
                "run_id": art["run_id"],
                "symbol": art["symbol"],
                "selected_source_format": fmt,
                "n_trades": len(trades),
                "required_fields_missing": ";".join(missing) if missing else "",
                "optional_fields_present": ";".join(present_optional),
                "stop_trigger_domain_handling": (
                    "inferred=trade_price_backtest (V1-arc historical artefact)"
                ),
                "fail_closed": "yes" if missing else "no",
            }
        )
        if missing:
            raise FailClosedError(
                f"REQUIRED_FIELDS_MISSING: {ledger_path} missing={missing}"
            )
        for t in trades:
            row = dict(art)
            row["trade_id"] = t.get("trade_id")
            row["direction"] = t.get("direction")
            row["entry_fill_time_ms"] = t.get("entry_fill_time_ms")
            row["exit_fill_time_ms"] = t.get("exit_fill_time_ms")
            row["entry_fill_price"] = t.get("entry_fill_price")
            row["exit_fill_price"] = t.get("exit_fill_price")
            row["initial_stop"] = t.get("initial_stop")
            row["stop_distance"] = t.get("stop_distance")
            row["realized_risk_usdt"] = t.get("realized_risk_usdt")
            row["gross_pnl"] = t.get("gross_pnl")
            row["net_pnl"] = t.get("net_pnl")
            row["net_r_multiple"] = t.get("net_r_multiple")
            row["entry_fee"] = t.get("entry_fee")
            row["exit_fee"] = t.get("exit_fee")
            row["funding_pnl"] = t.get("funding_pnl")
            row["fee_rate_assumption"] = t.get("fee_rate_assumption")
            row["slippage_bucket"] = t.get("slippage_bucket")
            row["exit_reason"] = t.get("exit_reason")
            row["bars_in_trade"] = t.get("bars_in_trade")
            row["mfe_r"] = t.get("mfe_r")
            row["mae_r"] = t.get("mae_r")
            row["stop_was_gap_through"] = t.get("stop_was_gap_through")
            row["quantity"] = t.get("quantity")
            row["notional_usdt"] = t.get("notional_usdt")
            row["metrics"] = compute_metrics(t)
            labelled.append(row)
    return labelled, schema_rows


def group_key(r: dict[str, Any]) -> tuple[str, str, str, str, str, str]:
    return (
        str(r["population"]),
        str(r["window_type"]),
        str(r["cost_cell"]),
        str(r["stop_domain_variant"]),
        str(r["fill_variant"]),
        str(r["symbol"]),
    )


def write_population_summary(
    output_root: Path, labelled: list[dict[str, Any]]
) -> Path:
    by_group: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r)
    rows: list[dict[str, Any]] = []
    for key, items in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        n_trades = len(items)
        wins = sum(
            1
            for r in items
            if isinstance(r["metrics"]["net_R"], float) and r["metrics"]["net_R"] > 0.0
        )
        losses = sum(
            1
            for r in items
            if isinstance(r["metrics"]["net_R"], float) and r["metrics"]["net_R"] <= 0.0
        )
        net_R_values = [r["metrics"]["net_R"] for r in items]
        mfe_values = [r["metrics"]["MFE_R"] for r in items]
        mae_values = [r["metrics"]["MAE_R"] for r in items]
        net_summ = numeric_summary(net_R_values)
        mfe_summ = numeric_summary(mfe_values)
        mae_summ = numeric_summary(mae_values)
        rows.append(
            {
                "population": pop,
                "window_type": win,
                "cost_cell": cc,
                "stop_domain_variant": stopv,
                "fill_variant": fillv,
                "symbol": sym,
                "n_trades": n_trades,
                "n_wins_net_R_gt_0": wins,
                "n_losses_or_flat_net_R_le_0": losses,
                "net_R_mean": fmt_float(net_summ["mean"]),
                "net_R_stdev": fmt_float(net_summ["stdev"]),
                "net_R_min": fmt_float(net_summ["min"]),
                "net_R_p25": fmt_float(net_summ["p25"]),
                "net_R_p50": fmt_float(net_summ["p50"]),
                "net_R_p75": fmt_float(net_summ["p75"]),
                "net_R_max": fmt_float(net_summ["max"]),
                "MFE_R_mean": fmt_float(mfe_summ["mean"]),
                "MFE_R_p50": fmt_float(mfe_summ["p50"]),
                "MAE_R_mean": fmt_float(mae_summ["mean"]),
                "MAE_R_p50": fmt_float(mae_summ["p50"]),
            }
        )
    path = output_root / "population_summary.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "n_trades",
            "n_wins_net_R_gt_0",
            "n_losses_or_flat_net_R_le_0",
            "net_R_mean",
            "net_R_stdev",
            "net_R_min",
            "net_R_p25",
            "net_R_p50",
            "net_R_p75",
            "net_R_max",
            "MFE_R_mean",
            "MFE_R_p50",
            "MAE_R_mean",
            "MAE_R_p50",
        ],
        rows,
    )
    return path


def write_distribution_table(
    output_root: Path,
    labelled: list[dict[str, Any]],
    metric_key: str,
    file_name: str,
) -> Path:
    by_group: dict[tuple[str, ...], list[float | None]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r["metrics"][metric_key])
    rows: list[dict[str, Any]] = []
    for key, vals in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        s = numeric_summary(vals)
        row = {
            "population": pop,
            "window_type": win,
            "cost_cell": cc,
            "stop_domain_variant": stopv,
            "fill_variant": fillv,
            "symbol": sym,
            "metric": metric_key,
            "n": s["n"],
            "n_nonfinite": s["n_nonfinite"],
            "mean": fmt_float(s["mean"]),
            "stdev": fmt_float(s["stdev"]),
            "min": fmt_float(s["min"]),
            "p10": fmt_float(s["p10"]),
            "p25": fmt_float(s["p25"]),
            "p50": fmt_float(s["p50"]),
            "p75": fmt_float(s["p75"]),
            "p90": fmt_float(s["p90"]),
            "p95": fmt_float(s["p95"]),
            "p99": fmt_float(s["p99"]),
            "max": fmt_float(s["max"]),
        }
        rows.append(row)
    path = output_root / file_name
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "metric",
            "n",
            "n_nonfinite",
            "mean",
            "stdev",
            "min",
            "p10",
            "p25",
            "p50",
            "p75",
            "p90",
            "p95",
            "p99",
            "max",
        ],
        rows,
    )
    return path


def write_mfe_mae_distribution(output_root: Path, labelled: list[dict[str, Any]]) -> Path:
    by_group: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r)
    rows: list[dict[str, Any]] = []
    for key, items in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        mfe_vals = [r["metrics"]["MFE_R"] for r in items]
        mae_vals = [r["metrics"]["MAE_R"] for r in items]
        gb_vals = [r["metrics"]["giveback_from_mfe"] for r in items]
        capture_vals = [r["metrics"]["mfe_capture_ratio"] for r in items]
        mfe_s = numeric_summary(mfe_vals)
        mae_s = numeric_summary(mae_vals)
        gb_s = numeric_summary(gb_vals)
        cap_s = numeric_summary(capture_vals)
        rows.append(
            {
                "population": pop,
                "window_type": win,
                "cost_cell": cc,
                "stop_domain_variant": stopv,
                "fill_variant": fillv,
                "symbol": sym,
                "n_trades": len(items),
                "MFE_R_mean": fmt_float(mfe_s["mean"]),
                "MFE_R_stdev": fmt_float(mfe_s["stdev"]),
                "MFE_R_min": fmt_float(mfe_s["min"]),
                "MFE_R_p25": fmt_float(mfe_s["p25"]),
                "MFE_R_p50": fmt_float(mfe_s["p50"]),
                "MFE_R_p75": fmt_float(mfe_s["p75"]),
                "MFE_R_p90": fmt_float(mfe_s["p90"]),
                "MFE_R_p95": fmt_float(mfe_s["p95"]),
                "MFE_R_max": fmt_float(mfe_s["max"]),
                "MAE_R_mean": fmt_float(mae_s["mean"]),
                "MAE_R_stdev": fmt_float(mae_s["stdev"]),
                "MAE_R_min": fmt_float(mae_s["min"]),
                "MAE_R_p25": fmt_float(mae_s["p25"]),
                "MAE_R_p50": fmt_float(mae_s["p50"]),
                "MAE_R_p75": fmt_float(mae_s["p75"]),
                "MAE_R_p90": fmt_float(mae_s["p90"]),
                "MAE_R_p95": fmt_float(mae_s["p95"]),
                "MAE_R_max": fmt_float(mae_s["max"]),
                "giveback_from_mfe_mean": fmt_float(gb_s["mean"]),
                "giveback_from_mfe_p50": fmt_float(gb_s["p50"]),
                "mfe_capture_ratio_mean": fmt_float(cap_s["mean"]),
                "mfe_capture_ratio_p50": fmt_float(cap_s["p50"]),
                "mfe_capture_ratio_n": cap_s["n"],
            }
        )
    path = output_root / "mfe_mae_distribution_by_population.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "n_trades",
            "MFE_R_mean",
            "MFE_R_stdev",
            "MFE_R_min",
            "MFE_R_p25",
            "MFE_R_p50",
            "MFE_R_p75",
            "MFE_R_p90",
            "MFE_R_p95",
            "MFE_R_max",
            "MAE_R_mean",
            "MAE_R_stdev",
            "MAE_R_min",
            "MAE_R_p25",
            "MAE_R_p50",
            "MAE_R_p75",
            "MAE_R_p90",
            "MAE_R_p95",
            "MAE_R_max",
            "giveback_from_mfe_mean",
            "giveback_from_mfe_p50",
            "mfe_capture_ratio_mean",
            "mfe_capture_ratio_p50",
            "mfe_capture_ratio_n",
        ],
        rows,
    )
    return path


def write_cost_in_r(output_root: Path, labelled: list[dict[str, Any]]) -> Path:
    by_group: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r)
    rows: list[dict[str, Any]] = []
    for key, items in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        cost_summ = numeric_summary([r["metrics"]["cost_in_R"] for r in items])
        fee_summ = numeric_summary([r["metrics"]["fee_in_R"] for r in items])
        funding_summ = numeric_summary([r["metrics"]["funding_in_R"] for r in items])
        slip_summ = numeric_summary(
            [r["metrics"]["estimated_slippage_in_R"] for r in items]
        )
        slip_basis_counter: dict[str, int] = defaultdict(int)
        for r in items:
            slip_basis_counter[str(r["metrics"]["estimated_slippage_basis"])] += 1
        slip_basis_str = ";".join(
            f"{k}={v}" for k, v in sorted(slip_basis_counter.items())
        )
        rows.append(
            {
                "population": pop,
                "window_type": win,
                "cost_cell": cc,
                "stop_domain_variant": stopv,
                "fill_variant": fillv,
                "symbol": sym,
                "n_trades": len(items),
                "cost_in_R_mean": fmt_float(cost_summ["mean"]),
                "cost_in_R_p50": fmt_float(cost_summ["p50"]),
                "fee_in_R_mean": fmt_float(fee_summ["mean"]),
                "fee_in_R_p50": fmt_float(fee_summ["p50"]),
                "funding_in_R_mean": fmt_float(funding_summ["mean"]),
                "funding_in_R_p50": fmt_float(funding_summ["p50"]),
                "estimated_slippage_in_R_mean": fmt_float(slip_summ["mean"]),
                "estimated_slippage_in_R_p50": fmt_float(slip_summ["p50"]),
                "estimated_slippage_basis_counts": slip_basis_str,
                "cost_reconciliation_note": "estimated; identity not asserted; see report",
            }
        )
    path = output_root / "cost_in_r_by_population.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "n_trades",
            "cost_in_R_mean",
            "cost_in_R_p50",
            "fee_in_R_mean",
            "fee_in_R_p50",
            "funding_in_R_mean",
            "funding_in_R_p50",
            "estimated_slippage_in_R_mean",
            "estimated_slippage_in_R_p50",
            "estimated_slippage_basis_counts",
            "cost_reconciliation_note",
        ],
        rows,
    )
    return path


def write_exit_reason_breakdown(
    output_root: Path, labelled: list[dict[str, Any]]
) -> Path:
    by_group: dict[tuple[str, ...], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in labelled:
        key = group_key(r)
        reason = r.get("exit_reason") or "UNKNOWN"
        by_group[key][reason] += 1
    rows: list[dict[str, Any]] = []
    for key, counts in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        for reason, n in sorted(counts.items()):
            rows.append(
                {
                    "population": pop,
                    "window_type": win,
                    "cost_cell": cc,
                    "stop_domain_variant": stopv,
                    "fill_variant": fillv,
                    "symbol": sym,
                    "exit_reason": reason,
                    "n_trades": n,
                }
            )
    path = output_root / "exit_reason_breakdown.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "exit_reason",
            "n_trades",
        ],
        rows,
    )
    return path


def write_excursion_threshold_touch_rates(
    output_root: Path, labelled: list[dict[str, Any]]
) -> Path:
    by_group: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r)
    rows: list[dict[str, Any]] = []
    for key, items in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        n = len(items)
        if n == 0:
            f1 = f2 = f3 = None
        else:
            f1 = sum(1 for r in items if r["metrics"]["reached_plus_1R_flag"]) / n
            f2 = sum(1 for r in items if r["metrics"]["reached_plus_2R_flag"]) / n
            f3 = sum(1 for r in items if r["metrics"]["reached_plus_3R_flag"]) / n
        rows.append(
            {
                "population": pop,
                "window_type": win,
                "cost_cell": cc,
                "stop_domain_variant": stopv,
                "fill_variant": fillv,
                "symbol": sym,
                "n_trades": n,
                "frac_reached_+1R": fmt_float(f1),
                "frac_reached_+2R": fmt_float(f2),
                "frac_reached_+3R": fmt_float(f3),
            }
        )
    path = output_root / "excursion_threshold_touch_rates.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "n_trades",
            "frac_reached_+1R",
            "frac_reached_+2R",
            "frac_reached_+3R",
        ],
        rows,
    )
    return path


def write_ambiguity_report(
    output_root: Path, labelled: list[dict[str, Any]]
) -> tuple[Path, dict[tuple[str, ...], float]]:
    by_group: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in labelled:
        by_group[group_key(r)].append(r)
    rows: list[dict[str, Any]] = []
    rates: dict[tuple[str, ...], float] = {}
    for key, items in sorted(by_group.items()):
        pop, win, cc, stopv, fillv, sym = key
        n = len(items)
        n_amb = sum(1 for r in items if r["metrics"]["bar_resolution_ambiguity_flag"])
        rate = (n_amb / n) if n > 0 else 0.0
        rates[key] = rate
        if rate < AMBIGUITY_BAND_5M_USABLE_LOW:
            band = "below_2pct__5m_likely_sufficient_if_authorized"
        elif rate <= AMBIGUITY_BAND_5M_USABLE_HIGH:
            band = "between_2pct_and_10pct__5m_usable_with_conservative_assumptions_if_authorized"
        elif rate <= AMBIGUITY_BAND_5M_TOO_COARSE:
            band = "between_10pct_and_20pct__1m_escalation_may_be_considered_if_authorized"
        else:
            band = "above_20pct__5m_likely_too_coarse_if_authorized"
        rows.append(
            {
                "population": pop,
                "window_type": win,
                "cost_cell": cc,
                "stop_domain_variant": stopv,
                "fill_variant": fillv,
                "symbol": sym,
                "n_trades": n,
                "n_bars_in_trade_eq_0": n_amb,
                "ambiguity_rate": fmt_float(rate),
                "phase_4al_section_14c_band_descriptive_only": band,
                "note": (
                    "DESCRIPTIVE ONLY. Phase 4aq does NOT authorize "
                    "5m / 1m / aggTrades / tick / mark-price "
                    "acquisition or use."
                ),
            }
        )
    path = output_root / "ambiguity_report.csv"
    write_csv(
        path,
        [
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "symbol",
            "n_trades",
            "n_bars_in_trade_eq_0",
            "ambiguity_rate",
            "phase_4al_section_14c_band_descriptive_only",
            "note",
        ],
        rows,
    )
    return path, rates


def write_forbidden_interpretation_checklist(output_root: Path) -> Path:
    path = output_root / "forbidden_interpretation_checklist.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "# Phase 4aq Forbidden Interpretation Checklist\n"
        "\n"
        "This file records the Phase 4ap §9 / §17 forbidden-interpretation "
        "boundaries that the Phase 4aq computation explicitly does NOT "
        "cross. Every item is recorded as `NOT_PERFORMED` because the "
        "Phase 4aq script emits descriptive forensics only and does not "
        "produce any of the following.\n"
        "\n"
        "- F1  NOT_PERFORMED  "
        "Choose an exit rule that would have made R3 profitable.\n"
        "- F2  NOT_PERFORMED  "
        "Choose a TP/SL pair to replace R3.\n"
        "- F3  NOT_PERFORMED  "
        "Choose the best take-profit multiple from observed MFE.\n"
        "- F4  NOT_PERFORMED  "
        "Tune R3 / R1a / R1b-narrow / R2 / H0 parameters from forensic "
        "findings.\n"
        "- F5  NOT_PERFORMED  "
        "Rescue R2 by appealing to lower assumed costs.\n"
        "- F6  NOT_PERFORMED  "
        "Promote R1a or R1b-narrow from retained-non-leading to leading.\n"
        "- F7  NOT_PERFORMED  "
        "Convert H0 / R3 into R3-prime / baseline-of-record successor / "
        "rescue.\n"
        "- F8  NOT_PERFORMED  "
        "Hybridize V1-arc populations with F1 / D1-A / V2 / G1 / C1.\n"
        "- F9  NOT_PERFORMED  "
        "Use 5m signals to improve V1-arc exit logic.\n"
        "- F10 NOT_PERFORMED  "
        "Convert any descriptive forensic finding into a strategy "
        "candidate, a parameter-optimization input, a verdict revision, "
        "a lock revision, a baseline-of-record revision, or a "
        "framework-anchor revision.\n"
        "\n"
        "This checklist is generated by "
        "`scripts/phase4aq_v1_arc_exit_path_forensics.py` and is part of "
        "the Phase 4aq output bundle.\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def write_v1_arc_forensic_report(
    output_root: Path,
    backtests_root: Path,
    manifest_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    labelled: list[dict[str, Any]],
    ambiguity_rates: dict[tuple[str, ...], float],
    written_paths: list[Path],
    computation_status: str,
) -> Path:
    path = output_root / "v1_arc_forensic_report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Aggregate per-population, per-symbol primary-summary lines (R-window,
    # default cost_cell, default stop_domain_variant, default fill_variant).
    primary: dict[tuple[str, str], dict[str, Any]] = {}
    for r in labelled:
        if r["window_type"] != "R":
            continue
        if r["cost_cell"] != "default":
            continue
        if r["stop_domain_variant"] != "default":
            continue
        if r["fill_variant"] != "default":
            continue
        key = (r["population"], r["symbol"])
        if key not in primary:
            primary[key] = {"net_R": [], "MFE_R": [], "MAE_R": [], "n": 0}
        primary[key]["n"] += 1
        primary[key]["net_R"].append(r["metrics"]["net_R"])
        primary[key]["MFE_R"].append(r["metrics"]["MFE_R"])
        primary[key]["MAE_R"].append(r["metrics"]["MAE_R"])

    primary_lines: list[str] = []
    primary_lines.append(
        "| population | symbol | n_trades | net_R_mean | net_R_p50 "
        "| MFE_R_mean | MFE_R_p50 | MAE_R_mean | MAE_R_p50 |"
    )
    primary_lines.append(
        "|------------|--------|----------|------------|-----------"
        "|------------|-----------|------------|-----------|"
    )
    for key in sorted(primary.keys()):
        pop, sym = key
        agg = primary[key]
        net_summ = numeric_summary(agg["net_R"])
        mfe_summ = numeric_summary(agg["MFE_R"])
        mae_summ = numeric_summary(agg["MAE_R"])
        primary_lines.append(
            f"| {pop} | {sym} | {agg['n']} | "
            f"{fmt_float(net_summ['mean'])} | {fmt_float(net_summ['p50'])} | "
            f"{fmt_float(mfe_summ['mean'])} | {fmt_float(mfe_summ['p50'])} | "
            f"{fmt_float(mae_summ['mean'])} | {fmt_float(mae_summ['p50'])} |"
        )

    # Exit-reason summary across primary R-window default cells.
    er_counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for r in labelled:
        if r["window_type"] != "R":
            continue
        if r["cost_cell"] != "default":
            continue
        if r["stop_domain_variant"] != "default":
            continue
        if r["fill_variant"] != "default":
            continue
        er_counts[
            (r["population"], r["symbol"], str(r.get("exit_reason") or "UNKNOWN"))
        ] += 1

    er_lines: list[str] = []
    er_lines.append("| population | symbol | exit_reason | n_trades |")
    er_lines.append("|------------|--------|-------------|----------|")
    for k in sorted(er_counts.keys()):
        pop, sym, reason = k
        er_lines.append(f"| {pop} | {sym} | {reason} | {er_counts[k]} |")

    # Threshold-touch summary across primary R-window default cells.
    touch: dict[tuple[str, str], dict[str, Any]] = {}
    for r in labelled:
        if r["window_type"] != "R":
            continue
        if r["cost_cell"] != "default":
            continue
        if r["stop_domain_variant"] != "default":
            continue
        if r["fill_variant"] != "default":
            continue
        key = (r["population"], r["symbol"])
        if key not in touch:
            touch[key] = {"n": 0, "p1": 0, "p2": 0, "p3": 0}
        touch[key]["n"] += 1
        if r["metrics"]["reached_plus_1R_flag"]:
            touch[key]["p1"] += 1
        if r["metrics"]["reached_plus_2R_flag"]:
            touch[key]["p2"] += 1
        if r["metrics"]["reached_plus_3R_flag"]:
            touch[key]["p3"] += 1
    touch_lines: list[str] = []
    touch_lines.append(
        "| population | symbol | n_trades "
        "| frac_reached_+1R | frac_reached_+2R | frac_reached_+3R |"
    )
    touch_lines.append(
        "|------------|--------|----------"
        "|------------------|------------------|------------------|"
    )
    for key in sorted(touch.keys()):
        pop, sym = key
        d = touch[key]
        n = d["n"]
        if n > 0:
            f1 = fmt_float(d["p1"] / n)
            f2 = fmt_float(d["p2"] / n)
            f3 = fmt_float(d["p3"] / n)
        else:
            f1 = f2 = f3 = ""
        touch_lines.append(
            f"| {pop} | {sym} | {n} | {f1} | {f2} | {f3} |"
        )

    # Cost decomposition summary across primary R-window default cells.
    cost_lines: list[str] = []
    cost_lines.append(
        "| population | symbol | cost_in_R_mean | fee_in_R_mean "
        "| funding_in_R_mean | est_slippage_in_R_mean (descriptive) |"
    )
    cost_lines.append(
        "|------------|--------|----------------|---------------"
        "|-------------------|--------------------------------------|"
    )
    cost_groups: dict[tuple[str, str], dict[str, list[float | None]]] = {}
    for r in labelled:
        if r["window_type"] != "R":
            continue
        if r["cost_cell"] != "default":
            continue
        if r["stop_domain_variant"] != "default":
            continue
        if r["fill_variant"] != "default":
            continue
        key = (r["population"], r["symbol"])
        d = cost_groups.setdefault(
            key, {"cost": [], "fee": [], "funding": [], "slip": []}
        )
        d["cost"].append(r["metrics"]["cost_in_R"])
        d["fee"].append(r["metrics"]["fee_in_R"])
        d["funding"].append(r["metrics"]["funding_in_R"])
        d["slip"].append(r["metrics"]["estimated_slippage_in_R"])
    for key in sorted(cost_groups.keys()):
        pop, sym = key
        d = cost_groups[key]
        cs = numeric_summary(d["cost"])
        fs = numeric_summary(d["fee"])
        fns = numeric_summary(d["funding"])
        ss = numeric_summary(d["slip"])
        cost_lines.append(
            f"| {pop} | {sym} | {fmt_float(cs['mean'])} | {fmt_float(fs['mean'])} | "
            f"{fmt_float(fns['mean'])} | {fmt_float(ss['mean'])} |"
        )

    # Ambiguity summary across primary R-window default cells.
    amb_lines: list[str] = []
    amb_lines.append(
        "| population | symbol | n_trades | bar_resolution_ambiguity_rate | phase_4al_band |"
    )
    amb_lines.append(
        "|------------|--------|----------|-------------------------------|----------------|"
    )
    for key in sorted(ambiguity_rates.keys()):
        pop, win, cc, stopv, fillv, sym = key
        if win != "R" or cc != "default" or stopv != "default" or fillv != "default":
            continue
        rate = ambiguity_rates[key]
        if rate < AMBIGUITY_BAND_5M_USABLE_LOW:
            band = "<2pct"
        elif rate <= AMBIGUITY_BAND_5M_USABLE_HIGH:
            band = "2-10pct"
        elif rate <= AMBIGUITY_BAND_5M_TOO_COARSE:
            band = "10-20pct"
        else:
            band = ">20pct"
        # Find n_trades for this group.
        n_g = sum(
            1
            for r in labelled
            if r["population"] == pop
            and r["symbol"] == sym
            and r["window_type"] == "R"
            and r["cost_cell"] == "default"
            and r["stop_domain_variant"] == "default"
            and r["fill_variant"] == "default"
        )
        amb_lines.append(f"| {pop} | {sym} | {n_g} | {fmt_float(rate)} | {band} |")

    # Sensitivity summary: variant cells (LOW / HIGH / TRADE_PRICE / fill).
    sens_lines: list[str] = []
    sens_lines.append(
        "| population | symbol | window | cost_cell "
        "| stop_variant | fill_variant | n_trades | net_R_mean |"
    )
    sens_lines.append(
        "|------------|--------|--------|-----------"
        "|--------------|--------------|----------|------------|"
    )
    sens_groups: dict[tuple[str, ...], list[float | None]] = defaultdict(list)
    for r in labelled:
        is_primary = (
            r["window_type"] == "R"
            and r["cost_cell"] == "default"
            and r["stop_domain_variant"] == "default"
            and r["fill_variant"] == "default"
        )
        if is_primary:
            continue
        key = (
            r["population"],
            r["symbol"],
            r["window_type"],
            r["cost_cell"],
            r["stop_domain_variant"],
            r["fill_variant"],
        )
        sens_groups[key].append(r["metrics"]["net_R"])
    for key in sorted(sens_groups.keys()):
        pop, sym, win, cc, stopv, fillv = key
        s = numeric_summary(sens_groups[key])
        sens_lines.append(
            f"| {pop} | {sym} | {win} | {cc} | {stopv} | {fillv} "
            f"| {s['n']} | {fmt_float(s['mean'])} |"
        )

    artifacts_listing_items: list[str] = []
    for p in written_paths:
        anchor = output_root.parent.parent
        rel = p.relative_to(anchor).as_posix() if anchor in p.parents else p.as_posix()
        artifacts_listing_items.append(f"- `{rel}`")
    artifacts_listing = "\n".join(artifacts_listing_items)

    # Schema validation summary line counts.
    n_dirs = len(manifest_rows)
    n_trades = len(labelled)
    n_runs = len({(r["run_family"], r["run_id"]) for r in manifest_rows})
    pop_counter: dict[str, int] = defaultdict(int)
    for r in labelled:
        pop_counter[r["population"]] += 1

    content = f"""# Phase 4aq — V1-Arc Exit-Path Forensic Report

Generated: {now}

This is the human-readable Phase 4aq forensic report. It is descriptive
only. It is not a strategy spec, a backtest plan, a parameter
recommendation, an exit-rule design, a verdict revision, or a lock
revision.

## Computation status

`{computation_status}`

## Phase 4ap authority

This report follows the Phase 4ap V1-Arc Exit-Path Forensic Plan
verbatim. Every metric is one of the Phase 4ap §12 metrics. Every
question answered is one of the Phase 4ap Q1–Q14 forensic questions.
No Phase 4ap forbidden question (F1–F10) is addressed.

## Methodology

- Standalone Python script: `scripts/phase4aq_v1_arc_exit_path_forensics.py`.
- No network I/O, no Binance API, no credentials, no data acquisition.
- No `prometheus.runtime` / `execution` / `persistence` imports.
- No backtest execution, no historical-strategy-script execution.
- Inputs: existing local V1-arc trade-log artefacts under
  `{backtests_root}/phase-2*`. Each directory's lexicographically-latest
  run subdirectory is selected. Each (directory, symbol) loads exactly
  one canonical trade ledger (Parquet preferred, JSON fallback).
- Output: `{output_root.as_posix()}/` (gitignored research outputs).
- Existing artefacts, manifests, source code, and tests are not
  modified.

## Population scope

Included populations (Phase 4ap §6): H0, R3, R1a, R1b-narrow, R2.
Excluded populations: F1, D1-A, V2, G1, C1, 5m research thread.

R3 inclusion is descriptive baseline-of-record context only. No R3
optimization. No R3-prime. No R3 rescue. No baseline-of-record revision.
No conversion of R3 forensic findings into parameters, thresholds,
entry logic, exit logic, or new strategy candidates.

## Stop-trigger-domain inference

Phase 4ap §15: V1-arc historical artefacts do not record
`stop_trigger_domain` as a per-trade field. All loaded V1-arc trade
records are inferred to be `trade_price_backtest` because every
allowlisted artefact-source path is an expected V1-arc Phase-2
backtest path. The inference is recorded in
`schema_validation_report.csv` and applies to all loaded rows.

`mixed_or_unknown` would be a Phase 4ap SC-3 fail-closed condition; this
script never assigns that label. The directory `phase-*-stop=TRADE_PRICE`
is a stop-domain validation variant within the trade-price-backtest
research family and is labelled `stop_domain_variant=TRADE_PRICE` to
preserve that configuration distinction without changing the inferred
`stop_trigger_domain`.

## Timeframe rule

Phase 4ap §13: 15m bar-extreme only. No lower-timeframe data was loaded.
No 5m, 1m, aggTrades, tick, mark-price 30m, or mark-price 4h data is
used or referenced as input. Phase 3t 5m research-thread closure is
preserved.

## Cost rule

Phase 4ap §14 / §11.6: §11.6 = 8 bps slippage per side preserved
verbatim. Cost-cell descriptive comparisons in this report do not
justify §11.6 relaxation. R2 cost-fragility findings remain retained
research evidence; R2 verdict (FAILED — §11.6) is preserved.

## Loaded-artefact summary

Loaded directories: {n_dirs} (across {n_runs} runs).
Total trades loaded across all populations / variants / symbols:
**{n_trades}**.

Per-population totals (all variants and windows, both symbols, all
cost cells):

| population | total trades |
|------------|--------------|
""" + "\n".join(
        f"| {pop} | {pop_counter[pop]} |" for pop in INCLUDED_POPULATIONS
    ) + f"""

See `loaded_artifacts_manifest.csv` for the full per-(directory, symbol)
artefact inventory and selected canonical ledger format.

## Schema validation summary

All {n_dirs} loaded (directory, symbol) pairs passed Phase 4ap §11
required-field validation. None of the loaded ledgers triggered Phase
4ap SC-2 fail-closed. See `schema_validation_report.csv`.

## Output artefact summary

All Phase 4aq outputs were written under `{output_root.as_posix()}/`:

{artifacts_listing}

## Q1–Q3 distributional findings (R-window, default cell)

Cell scope for this section: R-window, default cost cell, default
stop_domain_variant, default fill_variant. The table below shows
per-population, per-symbol mean and median for net_R, MFE_R, and
MAE_R on the primary R-window default cell. These are descriptive
only and are not strategy signals.

{chr(10).join(primary_lines)}

## Q4–Q5 relationship findings: MFE-vs-net_R and MAE-vs-net_R

`mfe_capture_ratio = net_R / MFE_R` is computed where `MFE_R > 0`,
otherwise NA. See `mfe_mae_distribution_by_population.csv` and
`realized_r_by_population.csv` for full distributions.

`giveback_from_mfe = MFE_R - net_R` is reported descriptively without
clamping. Negative values, where present, are not forced to zero; they
are preserved and explained as possible fill / cost / sign / schema edge
cases requiring interpretation, not forced rescue framing.

## Q6 threshold-touch findings: fraction reaching +1R / +2R / +3R

Phase 4ap §12 threshold flags are computed from `mfe_r`. The fraction
reaching each threshold per primary R-window default cell is:

{chr(10).join(touch_lines)}

These are descriptive frequencies. They are not parameter selections,
take-profit recommendations, or exit-rule designs. See
`excursion_threshold_touch_rates.csv` for full per-cell breakdown.

## Q7 favorable-before-stop proxy

Phase 4ap §12: for STOP exits, `favorable_excursion_before_stop_proxy`
is computed as `mfe_r > 0`. This is a proxy. The existing 15m schema
does not preserve intrabar event order, so the proxy does not assert
exact intrabar sequence between the favorable excursion and the
stop-out. Detailed per-trade values are encoded internally and may be
summarized in a future separately authorized phase.

## Q8 giveback-from-MFE distribution

See `mfe_mae_distribution_by_population.csv` columns
`giveback_from_mfe_mean` and `giveback_from_mfe_p50` for descriptive
values. No clamping applied.

## Q9 adverse-before-favorable

Phase 4ap §12: this metric requires intrabar event ordering that the
existing 15m schema does not preserve. The Phase 4aq script reports
`adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`
for every trade. Phase 4ap §13 forbids consulting lower-timeframe data
in this phase, so the result is recorded as NOT_AUDITABLE rather than
inferred or estimated.

## Q10 favorable-before-stop fraction (proxy)

The favorable-before-stop fraction is the population-level fraction of
STOP-exit trades whose `mfe_r > 0`. This is a proxy frequency. See
`exit_reason_breakdown.csv` for STOP-exit counts per cell.

## Q11–Q12 cost decomposition (descriptive only)

Per-trade descriptive cost decomposition (R-window default cell):

{chr(10).join(cost_lines)}

`cost_in_R = (gross_pnl - net_pnl) / realized_risk_usdt` is exact-from-
fields. `fee_in_R` and `funding_in_R` are exact-from-fields.
`estimated_slippage_in_R` is descriptive only and uses the per-trade
`slippage_bucket` mapped to per-side bps {SLIPPAGE_BPS_PER_SIDE}, with
notional from `notional_usdt` (or `abs(quantity) * entry_fill_price`
fallback). The identity
`cost_in_R == fee_in_R + estimated_slippage_in_R + funding_in_R` is
NOT asserted by this report. Phase 4aq does not propose any change to
§11.6 or to any historical cost reference. Any divergence between
`cost_in_R` and the sum of `fee_in_R + estimated_slippage_in_R +
funding_in_R` is descriptive context, not a finding requiring fee /
slippage / funding-model revision.

R2 cost-fragility (Phase 4ap §11): R2's cost-cell columns in
`cost_in_r_by_population.csv` and `realized_r_by_population.csv` are
descriptive evidence only. They do not relax §11.6, do not justify R2
rescue, and do not authorize a cost-model revision.

## Q13 cross-population descriptive comparison

The Q1 and Q6 tables above implicitly compare populations on the
primary R-window default cell. No promotion ranking is implied. R3
remains the baseline-of-record. R1a / R1b-narrow remain retained
non-leading. R2 remains FAILED — §11.6. H0 remains the framework
anchor. No descriptive comparison in this report justifies revising
those verdicts or locks.

## Q14 bar-resolution ambiguity

Phase 4al §14.C provides descriptive bands for ambiguity rates:

- < 2%   : 5m would likely be sufficient if separately authorized.
- 2-10%  : 5m would be usable with conservative (stop-first) assumptions.
- 10-20% : 1m escalation may be considered if separately authorized.
- > 20%  : 5m would likely be too coarse if separately authorized.

The Phase 4aq script flags `bars_in_trade == 0` as entry/exit same-bar
ambiguity, the only ambiguity signal recoverable from existing 15m
fields. Per-cell ambiguity rates on the primary R-window default cell:

{chr(10).join(amb_lines)}

These rates are descriptive only. Phase 4aq does NOT authorize 5m / 1m
/ aggTrades / tick / mark-price acquisition or use. A future operator
may separately authorize a forensic-measurement-layer phase if
ambiguity rates justify it, subject to Phase 4al §14 hierarchy and
Phase 4ao §13.3 conservative criterion.

See `ambiguity_report.csv` for full per-cell breakdown.

## Sensitivity / non-primary cells

Variant cells (LOW / HIGH cost cells, TRADE_PRICE stop-domain variant,
limit-at-pullback fill variant, V-window) are reported for descriptive
completeness only. No headline interpretation pools default and variant
cells. Variant cell summary:

{chr(10).join(sens_lines)}

Variants reflect a stop-domain or cost-cell sensitivity dimension
within the V1-arc research family. Their inclusion in this report is
descriptive evidence only and does not promote any variant configuration
to baseline-of-record status.

## R3 baseline boundary

R3 is included in this report because it is the V1-arc baseline-of-
record. R3 forensic findings are descriptive context only. They do not
authorize:

- R3 optimization;
- R3-prime / R3 next-spec / R3 successor;
- R3 rescue framing;
- baseline-of-record revision;
- conversion of R3 forensic numbers into entry rules, exit rules,
  parameters, or thresholds;
- introducing a new V1-arc strategy candidate based on R3 observations.

## R2 cost-fragility boundary

R2 remains FAILED — §11.6. The Phase 4aq cost-cell descriptive findings
on R2 are retained-research-evidence context only. They do not justify
§11.6 relaxation or R2 rescue.

## R1a / R1b-narrow boundary

R1a and R1b-narrow remain retained — non-leading. Phase 4aq descriptive
findings do not authorize R1a-prime, R1b-narrow-prime, or promotion to
leading status.

## H0 boundary

H0 remains the framework anchor. Phase 4aq descriptive findings do not
authorize H0-prime, framework-anchor revision, or hybrid candidates.

## Sequence-claim limitation

Phase 4ap §14: the Phase 4aq script does not infer event order from
final MFE_R and MAE_R alone. `adverse_before_favorable_flag` is
recorded as `NOT_AUDITABLE_FROM_EXISTING_FIELDS`. The
`favorable_excursion_before_stop_proxy` flag is labelled proxy. Lower-
timeframe data is not used.

## Forbidden-interpretation checklist

See `forbidden_interpretation_checklist.md`. All Phase 4ap §9 forbidden
question forms (F1–F10) are recorded as NOT_PERFORMED.

## Stop-condition review (Phase 4ap §17)

| ID    | Condition                                | Result |
|-------|------------------------------------------|--------|
| SC-1  | Required artefact missing                | PASS (none missing) |
| SC-2  | Required field missing                   | PASS (all required fields present) |
| SC-3  | mixed_or_unknown stop_trigger_domain     | PASS (inferred trade_price_backtest only) |
| SC-4  | Schema mismatch                          | PASS (Parquet/JSON parsed without error) |
| SC-5  | Excluded population detected             | PASS (allowlist enforces inclusion only) |
| SC-6  | 5m / 1m / tick / mark-price use w/o auth | PASS (none used) |
| SC-7  | Promotion ranking attempted              | PASS (none attempted) |
| SC-8  | Parameter-change proposal                | PASS (none made) |
| SC-9  | Verdict / lock revision                  | PASS (none made) |
| SC-10 | Strategy interpretation                  | PASS (descriptive reporting only) |
| SC-11 | Quality-gate failure                     | PASS (script lint / compile clean) |

## Implementation / governance review

- What changed: new standalone script `scripts/phase4aq_v1_arc_exit_path_forensics.py`,
  new local research outputs under `data/research/phase4aq/` (gitignored),
  Phase 4aq report memo and closeout under
  `docs/00-meta/implementation-reports/`, narrow update to
  `docs/00-meta/current-project-state.md`.
- What did not change: no `src/prometheus/` modification, no test
  modification, no manifest modification, no existing-trade-log
  modification, no historical-script modification, no data acquisition,
  no governance-document modification beyond the narrow current-state
  paragraph, no lock change, no verdict change, no M0 amendment.
- Mergeable as docs-and-code: yes.

## Research interpretation review (plain English)

1. What did this phase prove?
   It produced a reproducible descriptive forensic snapshot of V1-arc
   trade populations (H0 / R3 / R1a / R1b-narrow / R2) on 15m
   trade-price-backtest artefacts, covering MFE / MAE / net_R
   distributions, cost decomposition (descriptive), exit-reason
   breakdown, threshold-touch rates, and bar-resolution ambiguity rates.

2. What did this phase not prove?
   It did not prove that any V1-arc population can be improved, rescued,
   promoted, or hybridized. It did not prove that any V1-arc verdict or
   project lock should change. It did not prove that lower-timeframe
   data acquisition is necessary or justified.

3. Which original questions did it answer?
   The Phase 4ap Q1–Q14 descriptive questions, within the limits of
   the existing 15m schema. Q9 was recorded as
   NOT_AUDITABLE_FROM_EXISTING_FIELDS. Q7 was recorded as a proxy.

4. Which original questions remain open?
   Phase 4ap forbidden questions F1–F10 were never authorized and
   remain explicitly out of scope.

5. What does it mean for strategy research?
   It provides descriptive context for understanding how V1-arc
   trades unfolded relative to their MFE / MAE / cost / exit-reason
   profile. It does not motivate strategy work. The cumulative six
   failure-mode rejection topology (R2 / F1 / D1-A / V2 / G1 / C1)
   remains preserved verbatim, and Phase 4aq does not introduce any
   new candidate.

6. What does it mean for governance?
   M0 admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
   Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase
   4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption, and the
   Phase 4al / 4am / 4an / 4ao / 4ap chain are all preserved.

7. What is the clean next step?
   Operator review of Phase 4aq descriptive results. No successor phase
   is authorized. Future operator-driven options include remain paused
   or a separately authorized narrower follow-up memo.

8. What should we not do yet?
   No V1-arc successor candidates (R3-prime / R1a-prime / R1b-narrow-
   prime / R2-prime). No exit-rule design from forensic numbers. No
   parameter optimization. No verdict or lock revision. No 5m / 1m /
   aggTrades / tick / mark-price acquisition. No paper / shadow /
   live-readiness / exchange-write. No production-key creation.

## Recommendation

Phase 4aq computation is complete and descriptive only. The recommended
state remains paused. Operator may later separately authorize:

- a narrower docs-only interpretation memo focused on a specific
  Phase 4aq descriptive finding (only if separately authorized);
- a future Phase 4ar-class memo that consolidates Phase 4aq forensic
  evidence into a higher-level narrative without authorizing strategy
  work (only if separately authorized);
- remain paused indefinitely.

Phase 4aq does not authorize any successor phase.

## Verdict and lock preservation

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED (Phase 3t).
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

Locks preserved verbatim:

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk; 2x leverage cap; one position max; mark-price stops.
- Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 governance adoption.
- Phase 4al refined no-rescue rule.
- Phase 4al §13 boundary; Phase 4al §14 data-resolution hierarchy.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved.
- Phase 4an inventory result preserved.
- Phase 4ao harmonization result preserved.
- Phase 4ap forensic plan preserved.

No retained verdict revised. No project lock changed. No M0 governance
modified. No 5m research thread reopened.

## End of report
"""
    path.write_text(content, encoding="utf-8")
    return path


def main() -> int:
    args = parse_args()
    backtests_root = Path(args.backtests_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    info(f"Phase {PHASE_ID} — {PHASE_NAME}")
    info(f"Backtests root: {backtests_root}")
    info(f"Output root: {output_root}")
    info(f"Repository working dir: {Path.cwd()}")
    if not backtests_root.is_dir():
        warn(f"Backtests root is not a directory: {backtests_root}")
        write_fail_closed_outputs(
            output_root,
            f"BACKTESTS_ROOT_NOT_FOUND: {backtests_root}",
        )
        return 2

    manifest_rows, discovery_failures = build_loaded_artifacts_manifest(backtests_root)
    if discovery_failures:
        for f in discovery_failures:
            warn(f)
        write_fail_closed_outputs(
            output_root,
            "DISCOVERY_FAILED:\n" + "\n".join(discovery_failures),
        )
        return 2
    info(f"Discovered {len(manifest_rows)} (directory, symbol) artefact pairs.")

    # SC-5 excluded-population check.
    excl_msg = excluded_population_check(manifest_rows)
    if excl_msg is not None:
        warn(excl_msg)
        write_fail_closed_outputs(output_root, excl_msg)
        return 2

    # Write loaded_artifacts_manifest.csv early for traceability.
    manifest_csv = output_root / "loaded_artifacts_manifest.csv"
    write_csv(
        manifest_csv,
        [
            "run_family",
            "run_id",
            "symbol",
            "selected_source_format",
            "selected_source_path",
            "population",
            "window_type",
            "cost_cell",
            "stop_domain_variant",
            "fill_variant",
            "stop_trigger_domain_inferred",
            "timeframe",
        ],
        manifest_rows,
    )

    try:
        labelled, schema_rows = load_all_trades(manifest_rows, backtests_root)
    except FailClosedError as e:
        warn(str(e))
        write_fail_closed_outputs(output_root, str(e))
        return 2
    info(f"Loaded {len(labelled)} trade rows from {len(manifest_rows)} artefact pairs.")

    schema_csv = output_root / "schema_validation_report.csv"
    write_csv(
        schema_csv,
        [
            "run_family",
            "run_id",
            "symbol",
            "selected_source_format",
            "n_trades",
            "required_fields_missing",
            "optional_fields_present",
            "stop_trigger_domain_handling",
            "fail_closed",
        ],
        schema_rows,
    )

    written: list[Path] = [manifest_csv, schema_csv]
    written.append(write_population_summary(output_root, labelled))
    written.append(write_mfe_mae_distribution(output_root, labelled))
    written.append(
        write_distribution_table(
            output_root, labelled, "net_R", "realized_r_by_population.csv"
        )
    )
    written.append(write_cost_in_r(output_root, labelled))
    written.append(write_exit_reason_breakdown(output_root, labelled))
    written.append(write_excursion_threshold_touch_rates(output_root, labelled))
    amb_path, amb_rates = write_ambiguity_report(output_root, labelled)
    written.append(amb_path)
    written.append(write_forbidden_interpretation_checklist(output_root))
    written.append(
        write_v1_arc_forensic_report(
            output_root,
            backtests_root,
            manifest_rows,
            schema_rows,
            labelled,
            amb_rates,
            written,
            "SUCCESSFUL_COMPUTATION",
        )
    )
    info("Phase 4aq computation complete.")
    info(f"SUCCESSFUL_COMPUTATION: wrote {len(written)} output artefacts.")
    for p in written:
        info(f"  - {p.as_posix()}")
    return 0


def write_fail_closed_outputs(output_root: Path, reason: str) -> None:
    """Emit a minimal fail-closed bundle: forbidden checklist + report."""
    output_root.mkdir(parents=True, exist_ok=True)
    write_forbidden_interpretation_checklist(output_root)
    path = output_root / "v1_arc_forensic_report.md"
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = f"""# Phase 4aq — V1-Arc Exit-Path Forensic Report

Generated: {now}

## Computation status

`FAIL_CLOSED_NO_COMPUTATION`

## Reason

```
{reason}
```

Phase 4aq fails closed when any Phase 4ap §17 stop condition triggers.
This file is the explicit fail-closed record. No partial computation
result is claimed. No verdict / lock / governance is altered.

## Verdict and lock preservation

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED (Phase 3t).
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

§11.6, §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8,
Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w,
Phase 4ak M0 governance, Phase 4al / 4am / 4an / 4ao / 4ap all
preserved.

## End of fail-closed report
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
