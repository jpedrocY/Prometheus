"""Phase 4bn-AZ — tests for the CF-1 realized-volatility kernel + boundary proof.

Covers: causal completed-interval boundary semantics, the greatest-row_index tie,
covered-minute predicate, execution-access boundary rejection, HAR lookback assembly,
feature-snapshot alignment (``P_at`` over feature timestamps), and the deterministic
synthetic timestamp-boundary proof. No market data is opened by any test.
"""

from __future__ import annotations

from decimal import Decimal

import numpy as np
import pytest

from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1

HOUR = cf1.HOUR_MS
MIN = cf1.MINUTE_MS


def _base() -> int:
    return cf1.utc_date_start_ms("2024-06-01")


# ---------------------------------------------------------------------------
# Constants / dates
# ---------------------------------------------------------------------------


def test_allowed_dates_count_and_exclusions() -> None:
    allowed = cf1.allowed_utc_dates()
    assert len(allowed) == 244
    assert "2024-10-01" not in allowed
    assert "2024-03-01" in allowed and "2024-10-31" in allowed
    assert "2024-11-01" not in allowed


def test_forbidden_partition_guard_rejects_november_and_october1() -> None:
    for bad in ("2024-10-01", "2024-11-01", "2024-11-16", "2024-11-17", "2024-12-01", "2025-02-14"):
        with pytest.raises(cf1.Cf1ForbiddenPartitionError):
            cf1.assert_partition_allowed(bad)
    assert cf1.assert_partition_allowed("2024-06-15") == "2024-06-15"


def test_no_broad_glob_includes_forbidden_dates() -> None:
    allowed = set(cf1.allowed_utc_dates())
    for _reason, lo, hi in cf1.forbidden_date_ranges():
        # Every forbidden range date is absent from the allowlist.
        assert lo not in allowed and hi not in allowed


def test_block_assignment_by_origin_date() -> None:
    assert cf1.block_for_origin_ms(cf1.utc_date_start_ms("2024-04-15")) == "B1"
    assert cf1.block_for_origin_ms(cf1.utc_date_start_ms("2024-10-15")) == "B7"
    assert cf1.block_for_origin_ms(cf1.utc_date_start_ms("2024-03-15")) is None  # warmup
    assert cf1.block_for_origin_ms(cf1.utc_date_start_ms("2024-10-01")) is None  # embargo


# ---------------------------------------------------------------------------
# Boundary semantics (P_at, (a, b])
# ---------------------------------------------------------------------------


def test_p_at_greatest_row_index_tie() -> None:
    # Two trades share the exact instant; canonical sort puts greater row_index last.
    ts = np.array([100, 200, 200, 300], dtype=np.int64)
    prices = [Decimal("1"), Decimal("2"), Decimal("3"), Decimal("4")]
    idx = cf1.p_at_index(ts, 200)
    assert prices[idx] == Decimal("3")  # greatest row_index at ts=200


def test_p_at_none_before_first_trade() -> None:
    ts = np.array([100, 200], dtype=np.int64)
    assert cf1.p_at_index(ts, 50) == -1


def test_rv_over_trades_captures_boundary_jump_right_closed() -> None:
    base = _base()
    h9, h10 = base + 9 * HOUR, base + 10 * HOUR
    # Flat 100 through 09:59:59.999, then 110 exactly at 10:00:00.000.
    ts = np.array([h9 - 1, h9, h10 - 1, h10], dtype=np.int64)
    prices = [Decimal("100")] * 3 + [Decimal("110")]
    res = cf1.compute_rv_over_trades(ts, prices, h9, h10)
    # r_60 = ln(110/100) captured; RV > 0.
    assert res.rv > 0.0
    assert res.covered_minutes >= 1


def test_rv_target_excludes_origin_time_jump() -> None:
    base = _base()
    h10, h11 = base + 10 * HOUR, base + 11 * HOUR
    # Jump to 110 at exactly 10:00; then flat 110 to 11:00.
    ts = np.array([h10 - 1, h10, h10 + MIN, h11], dtype=np.int64)
    prices = [Decimal("100"), Decimal("110"), Decimal("110"), Decimal("110")]
    res = cf1.compute_rv_over_trades(ts, prices, h10, h11)
    # G_0 = P_at(10:00) = 110; the 100->110 jump is not re-counted; RV == 0.
    assert res.rv == pytest.approx(0.0, abs=1e-18)


def test_strict_lt_operator_would_omit_boundary_jump() -> None:
    base = _base()
    h10 = base + 10 * HOUR
    ts = np.array([h10 - 1, h10], dtype=np.int64)
    prices = [Decimal("100"), Decimal("110")]
    # Correct P_at (<=) sees 110; a strict-< left-limit would see 100.
    assert prices[cf1.p_at_index(ts, h10)] == Decimal("110")
    p_minus = int(np.searchsorted(ts, h10, side="left")) - 1
    assert prices[p_minus] == Decimal("100")


def test_interval_length_must_be_one_hour() -> None:
    ts = np.array([0], dtype=np.int64)
    with pytest.raises(cf1.Cf1ContractError):
        cf1.compute_rv_over_trades(ts, [Decimal("1")], 0, 30 * MIN)


# ---------------------------------------------------------------------------
# Coverage (tau_{k-1} < ts <= tau_k), 29 vs 30, carry-forward, zero-RV retained
# ---------------------------------------------------------------------------


def _minute_grid_from(ts_list: list[int], px_list: list[str], seg_id: str = "A") -> cf1.MinuteGrid:
    grid = cf1.new_minute_grid(seg_id, "2024-06-01", "2024-06-01")
    ts = np.array(ts_list, dtype=np.int64)
    px = [Decimal(p) for p in px_list]
    cf1.fill_minute_grid_from_trades(grid, ts, px)
    return grid


def test_coverage_threshold_29_invalid_30_valid() -> None:
    base = _base()
    h0 = base  # hour starting at midnight
    # One trade at the seed (00:00) so P_at is known everywhere; add trades in the
    # first 30 minute-subintervals only -> exactly 30 covered.
    trades = [(base, "100")]
    for k in range(1, 31):  # minutes 1..30 covered
        trades.append((base + k * MIN, "100"))
    grid29 = _minute_grid_from([t for t, _ in trades[:30]], [p for _, p in trades[:30]])
    res29 = cf1.hourly_rv_from_grid(grid29, h0)
    assert res29.covered_minutes == 29
    assert not res29.valid
    grid30 = _minute_grid_from([t for t, _ in trades], [p for _, p in trades])
    res30 = cf1.hourly_rv_from_grid(grid30, h0)
    assert res30.covered_minutes == 30
    assert res30.valid


def test_zero_rv_valid_and_retained() -> None:
    base = _base()
    h0 = base
    # A trade every minute at constant price -> RV == 0 but fully covered / valid.
    ts_list = [base + k * MIN for k in range(0, 61)]
    px_list = ["100"] * 61
    grid = _minute_grid_from(ts_list, px_list)
    res = cf1.hourly_rv_from_grid(grid, h0)
    assert res.rv == 0.0
    assert res.covered_minutes == 60
    assert res.valid  # zero-RV interval is valid and retained


def test_covered_minute_boundary_assignment() -> None:
    base = _base()
    # Trade exactly at tau_k (minute boundary) counts for the minute ENDING at tau_k.
    grid = _minute_grid_from([base, base + MIN], ["100", "101"])
    # minute index 1 corresponds to (base, base+MIN]; the base+MIN trade is inside it.
    assert bool(grid.covered[1])
    # minute index 0 (the seg-start boundary) has no preceding minute -> not covered.
    assert not bool(grid.covered[0])


# ---------------------------------------------------------------------------
# Access boundary: Oct 31 22:00 valid, 23:00 invalid; no November open
# ---------------------------------------------------------------------------


def test_october_31_boundary_rule() -> None:
    o22 = cf1.utc_date_start_ms("2024-10-31") + 22 * HOUR
    o23 = cf1.utc_date_start_ms("2024-10-31") + 23 * HOUR
    assert cf1.is_allowed_date(cf1.utc_date_for_timestamp_ms(o22 + cf1.HORIZON_MS))  # 23:00 ok
    assert not cf1.is_allowed_date(cf1.utc_date_for_timestamp_ms(o23 + cf1.HORIZON_MS))  # 11-01


def test_assemble_origin_rejects_out_of_access_target_endpoint() -> None:
    # Build a segment-B hourly series long enough; the 23:00 origin must be invalid.
    grid = cf1.new_minute_grid("B", "2024-10-02", "2024-10-31")
    # Mark all prices known / covered (synthetic dense grid at constant price).
    grid.price = [Decimal("100")] * grid.n_minutes
    grid.price_known[:] = True
    grid.covered[:] = True
    series = cf1.build_hourly_series(grid)
    o23 = cf1.utc_date_start_ms("2024-10-31") + 23 * HOUR
    res = cf1.assemble_origin_target(series, o23)
    assert not res.valid
    assert res.invalid_reason == "target_crosses_inaccessible_boundary"


def test_assemble_origin_weekly_lookback_within_segment() -> None:
    grid = cf1.new_minute_grid("B", "2024-10-02", "2024-10-31")
    grid.price = [Decimal("100")] * grid.n_minutes
    grid.price_known[:] = True
    grid.covered[:] = True
    series = cf1.build_hourly_series(grid)
    # An early-October origin whose 168h weekly window predates 2024-10-02 is invalid.
    early = cf1.utc_date_start_ms("2024-10-03") + 5 * HOUR
    res = cf1.assemble_origin_target(series, early)
    assert not res.valid
    assert res.invalid_reason == "har_unavailable"
    # A late-October origin with a full weekly window inside segment B is valid.
    late = cf1.utc_date_start_ms("2024-10-20") + 12 * HOUR
    res2 = cf1.assemble_origin_target(series, late)
    assert res2.valid
    assert res2.rv_target == 0.0  # constant price -> zero RV, still valid


# ---------------------------------------------------------------------------
# HAR lookbacks
# ---------------------------------------------------------------------------


def test_har_means_over_constant_grid_are_zero_and_valid() -> None:
    grid = cf1.new_minute_grid("A", "2024-03-01", "2024-03-31")
    grid.price = [Decimal("100")] * grid.n_minutes
    grid.price_known[:] = True
    grid.covered[:] = True
    series = cf1.build_hourly_series(grid)
    origin = cf1.utc_date_start_ms("2024-03-20") + 6 * HOUR
    res = cf1.assemble_origin_target(series, origin)
    assert res.valid
    assert res.rv_h == 0.0 and res.rv_d == 0.0 and res.rv_w == 0.0


def test_no_stitch_across_segments_via_segment_id() -> None:
    # An origin whose date is in segment A cannot be assembled against a segment-B series.
    grid = cf1.new_minute_grid("B", "2024-10-02", "2024-10-31")
    grid.price = [Decimal("100")] * grid.n_minutes
    grid.price_known[:] = True
    grid.covered[:] = True
    series = cf1.build_hourly_series(grid)
    sept_origin = cf1.utc_date_start_ms("2024-09-20") + 12 * HOUR
    res = cf1.assemble_origin_target(series, sept_origin)
    assert not res.valid


# ---------------------------------------------------------------------------
# Deterministic synthetic timestamp-boundary proof
# ---------------------------------------------------------------------------


def test_synthetic_boundary_proof_passes_and_is_deterministic() -> None:
    r1 = cf1.run_synthetic_timestamp_boundary_proof()
    r2 = cf1.run_synthetic_timestamp_boundary_proof()
    assert r1["timestamp_boundary_proof_passed"] is True
    assert r1 == r2
    assert r1["market_data_opened"] is False
    assert r1["reserve_touched"] is False
    names = {c["name"] for c in r1["checks"]}  # type: ignore[union-attr]
    for required in (
        "same_timestamp_greatest_row_index_tie",
        "interval_0900_1000_captures_boundary_jump",
        "interval_1000_1100_starts_from_110_no_recount",
        "rv_target_1000_excludes_origin_time_jump",
        "trade_at_1100_included_in_target_1000_1100",
        "feature_snapshot_1000_may_include_1000_row",
        "strict_lt_or_half_open_variant_fails_validation",
        "oct31_2200_valid_2300_invalid",
        "november_1_partition_rejected_before_open",
    ):
        assert required in names


def test_synthetic_boundary_proof_all_checks_pass() -> None:
    result = cf1.run_synthetic_timestamp_boundary_proof()
    for check in result["checks"]:  # type: ignore[union-attr]
        assert check["passed"] is True, check
