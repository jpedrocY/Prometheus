"""Phase 4bn-AN — tests for the longer-horizon sibling label family.

Covers the sibling schema constants, the config-hash determinism, the label
kernel's reference/censoring/direction logic on a hand-computable synthetic
fixture (no real data), the research-namespace writer's path discipline and
overwrite refusal, and the orchestrator's pure split/summary helpers.
"""

from __future__ import annotations

import math
from decimal import Decimal
from pathlib import Path

import numpy as np
import pyarrow as pa
import pytest

from prometheus.research.microstructure import longhorizon_labels_schema_v001 as s
from prometheus.research.microstructure.labels_compute_v002 import NormalizedDayRef
from prometheus.research.microstructure.labels_schema_v002 import LabelSchemaErrorV002
from prometheus.research.microstructure.longhorizon_labels_compute_v001 import (
    LabelComputationErrorV002,
    LongHorizonLabelLineage,
    compute_longhorizon_labels_for_day,
    write_longhorizon_label_dataset,
)

_HEX = "0" * 64
_LINEAGE = LongHorizonLabelLineage(
    source_feature_manifest_sha256="a" * 64,
    source_feature_parquet_sha256="b" * 64,
    source_feature_successor_state_sha256="c" * 64,
    source_phase_4bm_j_gate_report_sha256="d" * 64,
    source_normalized_manifest_sha256="e" * 64,
    source_raw_manifest_sha256="f" * 64,
    label_config_hash="1" * 64,
)


# ---------------------------------------------------------------------------
# Schema / identity
# ---------------------------------------------------------------------------


def test_family_identity_and_horizons() -> None:
    assert s.LONGHORIZON_LABEL_DATASET_FAMILY == (
        "microstructure_labels_longhorizon_aggtrades_v001"
    )
    assert s.LONGHORIZON_LABEL_DATASET_FAMILY != s.FROZEN_SHORT_HORIZON_FAMILY
    assert s.LONGHORIZON_HORIZONS == ("5m", "30m", "1h")
    assert s.LONGHORIZON_HORIZON_MS == (300_000, 1_800_000, 3_600_000)
    assert s.LONGHORIZON_LEAD == "5m"
    assert s.LONGHORIZON_SECONDARY == ("30m", "1h")
    # Every longer horizon strictly less than one UTC day.
    assert all(ms < s.UTC_DAY_MS for ms in s.LONGHORIZON_HORIZON_MS)


def test_schema_columns_exact() -> None:
    assert s.LONGHORIZON_LABEL_NAMES == (
        "forward_log_return_5m",
        "forward_log_return_30m",
        "forward_log_return_1h",
        "forward_direction_5m",
        "forward_direction_30m",
        "forward_direction_1h",
    )
    assert s.LONGHORIZON_LABEL_SUPPORT_COLUMN_NAMES == (
        "reference_row_index_5m",
        "reference_timestamp_ms_5m",
        "horizon_censored_flag_5m",
        "reference_row_index_30m",
        "reference_timestamp_ms_30m",
        "horizon_censored_flag_30m",
        "reference_row_index_1h",
        "reference_timestamp_ms_1h",
        "horizon_censored_flag_1h",
        "label_invalid_price_flag",
        "label_any_censored_flag",
    )
    assert len(s.LONGHORIZON_LABEL_SCHEMA) == 17 + 1 + 6 + 11
    assert len(set(s.LONGHORIZON_LABEL_SCHEMA)) == len(s.LONGHORIZON_LABEL_SCHEMA)


def test_no_forbidden_substrings_and_no_cost_threshold_in_policy() -> None:
    from prometheus.research.microstructure.labels_schema_v002 import (
        assert_no_forbidden_label_substrings_v002,
    )

    assert_no_forbidden_label_substrings_v002(s.LONGHORIZON_LABEL_SCHEMA)
    pol = s.LONGHORIZON_DIRECTION_THRESHOLD_POLICY
    assert "no_deadband" in pol
    assert "no_bp_threshold" in pol
    assert "no_threshold_optimization" in pol
    assert "no_cost_based_threshold" in pol
    assert "no_learned_threshold" in pol
    assert "no_magnitude_label" in pol


def test_config_hash_deterministic_and_distinct() -> None:
    kwargs = {
        "source_feature_manifest_sha256": "a" * 64,
        "source_feature_layer_gate_report_sha256": "b" * 64,
        "source_normalized_manifest_sha256": "c" * 64,
        "source_normalized_layer_gate_report_sha256": "d" * 64,
        "source_raw_manifest_sha256": "e" * 64,
        "feature_config_hash": "f" * 64,
    }
    h1 = s.build_longhorizon_label_config_hash(**kwargs)
    h2 = s.build_longhorizon_label_config_hash(**kwargs)
    assert h1 == h2
    assert len(h1) == 64
    other = dict(kwargs)
    other["feature_config_hash"] = "0" * 64
    assert s.build_longhorizon_label_config_hash(**other) != h1


def test_config_hash_rejects_bad_hex() -> None:
    with pytest.raises(LabelSchemaErrorV002):
        s.build_longhorizon_label_config_hash(
            source_feature_manifest_sha256="nothex",
            source_feature_layer_gate_report_sha256="b" * 64,
            source_normalized_manifest_sha256="c" * 64,
            source_normalized_layer_gate_report_sha256="d" * 64,
            source_raw_manifest_sha256="e" * 64,
            feature_config_hash="f" * 64,
        )


def test_non_authorization_flags_all_false() -> None:
    assert set(s.NON_AUTHORIZATION_FLAGS) == {
        "ml_authorized",
        "diagnostics_authorized",
        "strategy_authorized",
        "signals_authorized",
        "pnl_authorized",
        "backtest_authorized",
        "live_authorized",
        "exchange_write_authorized",
    }
    assert all(v is False for v in s.NON_AUTHORIZATION_FLAGS.values())


# ---------------------------------------------------------------------------
# Kernel correctness on a hand-computable synthetic fixture
# ---------------------------------------------------------------------------


def _make_day(date: str, ts: list[int], prices: list[str]) -> NormalizedDayRef:
    n = len(ts)
    return NormalizedDayRef(
        utc_date=date,
        transact_time_ms=np.array(ts, dtype=np.int64),
        prices_decimal=[Decimal(p) for p in prices],
        agg_trade_id=np.arange(n, dtype=np.int64),
    )


def _feature_table(day: NormalizedDayRef) -> pa.Table:
    n = len(day.transact_time_ms)
    return pa.table(
        {
            "row_index": pa.array(np.arange(n, dtype=np.int64)),
            "agg_trade_id": pa.array(day.agg_trade_id),
            "feature_timestamp_ms": pa.array(day.transact_time_ms),
            "source_transact_time_ms": pa.array(day.transact_time_ms),
        }
    )


def _build_fixture() -> tuple[pa.Table, NormalizedDayRef, NormalizedDayRef, int]:
    # Current day: 31 rows spaced 100_000 ms apart, prices 100..130.
    cur_ts = [i * 100_000 for i in range(31)]
    cur_prices = [str(100 + i) for i in range(31)]
    current = _make_day("2024-03-01", cur_ts, cur_prices)
    # Next day: three rows strictly after current's last (3_000_000), prices up.
    nxt_ts = [3_100_000, 3_600_000, 4_000_000]
    nxt_prices = ["200", "300", "400"]
    nxt = _make_day("2024-03-02", nxt_ts, nxt_prices)
    envelope_terminal = 4_000_000  # next day's last ts
    return _feature_table(current), current, nxt, envelope_terminal


def test_kernel_reference_current_day() -> None:
    feat, current, nxt, term = _build_fixture()
    table, summary = compute_longhorizon_labels_for_day(
        feature_table=feat,
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=term,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    assert summary.row_count == 31
    cols = table.column_names
    assert tuple(cols) == s.LONGHORIZON_LABEL_SCHEMA
    # Anchor row 0 (ts=0, price 100), 5m target=300_000 -> current row 3 (price 103).
    ref_idx_5m = table.column("reference_row_index_5m").to_pylist()
    ref_ts_5m = table.column("reference_timestamp_ms_5m").to_pylist()
    flr_5m = table.column("forward_log_return_5m").to_pylist()
    dir_5m = table.column("forward_direction_5m").to_pylist()
    assert ref_idx_5m[0] == 3
    assert ref_ts_5m[0] == 300_000
    assert flr_5m[0] == pytest.approx(math.log(103 / 100))
    assert dir_5m[0] == 1
    # Anchor row 0, 30m target=1_800_000 -> current row 18 (price 118).
    ref_idx_30m = table.column("reference_row_index_30m").to_pylist()
    assert ref_idx_30m[0] == 18
    # Anchor row 0, 1h target=3_600_000 -> next row 1 (ts 3_600_000 exact, price 300).
    ref_ts_1h = table.column("reference_timestamp_ms_1h").to_pylist()
    flr_1h = table.column("forward_log_return_1h").to_pylist()
    assert ref_ts_1h[0] == 3_600_000
    assert flr_1h[0] == pytest.approx(math.log(300 / 100))


def test_kernel_cross_day_reference() -> None:
    feat, current, nxt, term = _build_fixture()
    table, _ = compute_longhorizon_labels_for_day(
        feature_table=feat,
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=term,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    # Anchor row 30 (ts=3_000_000, price 130), 5m target=3_300_000 -> next row 0
    # (ts 3_100_000, price 200): the largest envelope row with ts <= target.
    ref_ts_5m = table.column("reference_timestamp_ms_5m").to_pylist()
    flr_5m = table.column("forward_log_return_5m").to_pylist()
    dir_5m = table.column("forward_direction_5m").to_pylist()
    assert ref_ts_5m[30] == 3_100_000
    assert flr_5m[30] == pytest.approx(math.log(200 / 130))
    assert dir_5m[30] == 1


def test_kernel_censoring_beyond_envelope_terminal() -> None:
    feat, current, nxt, term = _build_fixture()
    table, summary = compute_longhorizon_labels_for_day(
        feature_table=feat,
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=term,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    # Anchor row 30 (ts=3_000_000), 30m target=4_800_000 > terminal 4_000_000 -> censored.
    cens_30m = table.column("horizon_censored_flag_30m").to_pylist()
    flr_30m = table.column("forward_log_return_30m").to_pylist()
    dir_30m = table.column("forward_direction_30m").to_pylist()
    any_cens = table.column("label_any_censored_flag").to_pylist()
    assert cens_30m[30] is True
    assert flr_30m[30] is None
    assert dir_30m[30] is None
    assert any_cens[30] is True
    assert summary.censored_per_horizon["30m"] >= 1
    # No censoring flag implies a produced label unless invalid price.
    assert summary.invalid_price_row_count == 0


def test_kernel_direction_sign_matches_return() -> None:
    # Prices strictly decreasing -> all forward returns negative -> direction -1.
    cur_ts = [i * 100_000 for i in range(31)]
    cur_prices = [str(200 - i) for i in range(31)]
    current = _make_day("2024-03-01", cur_ts, cur_prices)
    nxt = _make_day("2024-03-02", [3_100_000, 3_600_000], ["150", "140"])
    table, _ = compute_longhorizon_labels_for_day(
        feature_table=_feature_table(current),
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=3_600_000,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    for h in ("5m", "30m", "1h"):
        flr = table.column(f"forward_log_return_{h}").to_pylist()
        drc = table.column(f"forward_direction_{h}").to_pylist()
        for v, d in zip(flr, drc, strict=True):
            if v is None:
                assert d is None
            elif v < 0:
                assert d == -1
            elif v > 0:
                assert d == 1
            else:
                assert d == 0


def test_kernel_rejects_misaligned_feature_table() -> None:
    feat, current, nxt, term = _build_fixture()
    bad = feat.set_column(
        0, "row_index", pa.array(np.arange(1, 32, dtype=np.int64))
    )
    with pytest.raises(LabelComputationErrorV002):
        compute_longhorizon_labels_for_day(
            feature_table=bad,
            current_day=current,
            next_day=nxt,
            envelope_terminal_unix_ms=term,
            symbol="BTCUSDT",
            utc_date="2024-03-01",
            lineage=_LINEAGE,
        )


# ---------------------------------------------------------------------------
# Writer path discipline / overwrite refusal
# ---------------------------------------------------------------------------


def test_writer_rejects_non_research_path(tmp_path: Path) -> None:
    feat, current, nxt, term = _build_fixture()
    table, _ = compute_longhorizon_labels_for_day(
        feature_table=feat,
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=term,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    bad = tmp_path / "somewhere" / "labels.parquet"
    with pytest.raises(LabelComputationErrorV002):
        write_longhorizon_label_dataset(table=table, output_path=bad)


def test_writer_writes_and_refuses_overwrite(tmp_path: Path) -> None:
    feat, current, nxt, term = _build_fixture()
    table, _ = compute_longhorizon_labels_for_day(
        feature_table=feat,
        current_day=current,
        next_day=nxt,
        envelope_terminal_unix_ms=term,
        symbol="BTCUSDT",
        utc_date="2024-03-01",
        lineage=_LINEAGE,
    )
    out = (
        tmp_path
        / "data"
        / "research"
        / "microstructure"
        / "labels"
        / "x"
        / "BTCUSDT-labels-longhorizon-aggtrades-2024-03-01.parquet"
    )
    wp, sha, size, sc, sc_sha = write_longhorizon_label_dataset(
        table=table, output_path=out
    )
    assert out.exists()
    assert sc is not None and sc.exists()
    assert len(sha) == 64 and size > 0
    # Canonical two-space sidecar body.
    assert sc.read_bytes() == f"{sha}  {out.name}\n".encode("ascii")
    with pytest.raises(LabelComputationErrorV002):
        write_longhorizon_label_dataset(table=table, output_path=out)


# ---------------------------------------------------------------------------
# Orchestrator pure helpers
# ---------------------------------------------------------------------------


def test_orchestrator_split_map_and_accumulator() -> None:
    from scripts import phase4bn_an_build_longhorizon_labels as an

    smap = an._split_by_date()
    assert len(smap) == 275
    counts: dict[str, int] = {}
    for v in smap.values():
        counts[v] = counts.get(v, 0) + 1
    assert counts["train"] == 214
    assert counts["validation"] == 45
    assert counts["holdout"] == 14
    assert counts["embargo"] == 2

    acc = an.HorizonSplitAccumulator()
    acc.ensure_hist()
    # Two supported values: 4 bps and 20 bps (log-return space).
    for bps in (4.0, 20.0):
        acc.support_count += 1
        acc.sum_abs_bps += bps
        acc.max_abs_bps = max(acc.max_abs_bps, bps)
        if bps > 8.0:
            acc.n_gt_8bps += 1
        if bps > 16.0:
            acc.n_gt_16bps += 1
        b = int(bps / an.BPS_BIN_WIDTH)
        acc.hist[b] += 1
    d = acc.to_dict()
    assert d["support_count"] == 2
    assert d["share_abs_gt_8bps"] == 0.5
    assert d["share_abs_gt_16bps"] == 0.5
    assert d["max_abs_forward_log_return_bps"] == 20.0
    assert d["mean_abs_forward_log_return_bps"] == pytest.approx(12.0)


def test_orchestrator_module_imports_no_network() -> None:
    from scripts import phase4bn_an_build_longhorizon_labels as an

    src = Path(an.__file__).read_text(encoding="utf-8")
    for banned in ("requests", "urllib.request", "websocket", "socket.socket", "aiohttp"):
        assert banned not in src
    assert an.OUTPUT_ROOT_REL.startswith("data/research/microstructure/labels/")
