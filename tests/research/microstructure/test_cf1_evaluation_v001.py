"""Phase 4bn-AZ — tests for the CF-1 evaluation (OLS, QLIKE, bootstrap, verdict routing).

Covers: intercept + train-only standardization (ddof=0), no evaluation leakage,
zero-variance / rank / condition / min-origin numerical guards, QLIKE zero-RV retention
and same-epsilon symmetry, the equal-weighted primary estimand, 6-of-7 block consistency,
the deterministic stratified moving-block bootstrap (block-specific l_i, linear 0.05
quantile), and exact PASS / FAIL / INVALID routing. No market data is opened.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from prometheus.research.microstructure import cf1_evaluation_v001 as ev
from prometheus.research.microstructure import cf1_realized_volatility_v001 as cf1

HOUR = cf1.HOUR_MS


def _make_rows(
    *,
    signal_strength: float,
    seed: int,
    n_eval: int = 150,
    n_warmup: int = 300,
    constant_features: bool = False,
    short_block: str | None = None,
) -> list[ev.OriginRow]:
    """Generate a synthetic valid-origin dataset with a tunable feature signal.

    When ``signal_strength > 0`` the log-variance target depends on a latent ``z`` that
    the three log-features proxy closely, so the augmented model improves QLIKE. When
    ``signal_strength == 0`` the features are unrelated noise (no incremental signal).
    """
    rng = np.random.default_rng(seed)
    rows: list[ev.OriginRow] = []

    def emit(origin_ms: int, block_id: str) -> None:
        lrvh = rng.normal(-10.0, 1.0)
        lrvd = rng.normal(-10.0, 0.8)
        lrvw = rng.normal(-10.0, 0.6)
        rv_h, rv_d, rv_w = math.exp(lrvh), math.exp(lrvd), math.exp(lrvw)
        z = rng.normal()
        if constant_features:
            x1 = x2 = x3 = 1.0
        else:
            x1 = math.exp(z + 0.05 * rng.normal())
            x2 = math.exp(0.9 * z + 0.05 * rng.normal())
            x3 = math.exp(1.1 * z + 0.05 * rng.normal())
        log_rv = (
            -3.0 + 0.5 * lrvh + 0.3 * lrvd + 0.2 * lrvw + signal_strength * z + 0.05 * rng.normal()
        )
        rv = math.exp(log_rv)
        rows.append(
            ev.OriginRow(
                origin_ms=origin_ms,
                target_end_ms=origin_ms + cf1.HORIZON_MS,
                block_id=block_id,
                rv=rv,
                log_rv=math.log(rv + cf1.TARGET_EPSILON),
                rv_h=rv_h,
                rv_d=rv_d,
                rv_w=rv_w,
                x1=x1,
                x2=x2,
                x3=x3,
            )
        )

    # Warmup (train-only) origins in March.
    m0 = cf1.utc_date_start_ms("2024-03-01")
    for j in range(n_warmup):
        emit(m0 + j * HOUR, "")
    # Per-block eval origins.
    for block_id, start, _end in cf1.BLOCKS:
        s = cf1.utc_date_start_ms(start)
        count = 60 if (short_block is not None and block_id == short_block) else n_eval
        for j in range(count):
            emit(s + (2 + j) * HOUR, block_id)
    return rows


# ---------------------------------------------------------------------------
# OLS + preprocessing
# ---------------------------------------------------------------------------


def test_train_transform_ddof0_and_zero_variance_flag() -> None:
    feats = np.array([[0.0, 1.0, 2.0], [2.0, 1.0, 4.0]], dtype=np.float64)
    tr = ev.fit_train_transform(feats)
    # Column 1 is constant -> zero variance flagged.
    assert tr.zero_variance is True
    # Population std (ddof=0) of column 0 over {0,2} is 1.0.
    assert tr.std[0] == 1.0


def test_ols_intercept_recovers_linear_relationship() -> None:
    rng = np.random.default_rng(0)
    n = 200
    har = rng.normal(size=(n, 3))
    design = ev._design_baseline(har)
    beta_true = np.array([0.7, 0.5, 0.3, 0.2])
    y = design @ beta_true
    fit = ev.fit_ols(design, y, cf1.BASELINE_N_PARAMS)
    assert fit.ok
    assert np.allclose(fit.beta, beta_true, atol=1e-8)


def test_ols_too_few_origins_is_guarded() -> None:
    design = np.ones((10, 4), dtype=np.float64)
    design[:, 1:] = np.random.default_rng(1).normal(size=(10, 3))
    fit = ev.fit_ols(design, np.zeros(10), cf1.BASELINE_N_PARAMS)
    assert not fit.ok
    assert fit.reason == "too_few_training_origins"


def test_ols_zero_variance_regressor_guarded() -> None:
    n = 100
    design = np.ones((n, 4), dtype=np.float64)  # all non-intercept columns constant
    fit = ev.fit_ols(design, np.zeros(n), cf1.BASELINE_N_PARAMS)
    assert not fit.ok
    assert fit.reason == "zero_variance_regressor"


# ---------------------------------------------------------------------------
# QLIKE
# ---------------------------------------------------------------------------


def test_qlike_zero_rv_retained_and_finite() -> None:
    rv = np.array([0.0, 1e-8, 1.0], dtype=np.float64)
    y_hat = np.log(np.array([1e-8, 1e-8, 1.0], dtype=np.float64))
    res = ev.qlike(rv, y_hat)
    assert res.finite
    assert res.values.shape == (3,)
    assert np.all(np.isfinite(res.values))


def test_qlike_lower_for_better_forecast_same_epsilon() -> None:
    rv = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    good = ev.qlike(rv, np.log(rv))  # perfect forecast
    bad = ev.qlike(rv, np.log(rv) + 1.0)  # biased forecast
    assert float(np.mean(good.values)) < float(np.mean(bad.values))
    # Perfect forecast QLIKE ~ 0.
    assert float(np.mean(good.values)) < 1e-12


def test_qlike_min_at_v_equals_h() -> None:
    rv = np.array([1.0], dtype=np.float64)
    res = ev.qlike(rv, np.log(rv + cf1.TARGET_EPSILON))
    assert res.values[0] >= 0.0
    assert res.values[0] < 1e-12


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


def test_bootstrap_block_length_is_cube_root_ceil() -> None:
    assert ev._bootstrap_block_length(100) == 5  # ceil(100^(1/3)) = ceil(4.64) = 5
    assert ev._bootstrap_block_length(1000) == 10


def test_bootstrap_deterministic_and_within_range() -> None:
    rng = np.random.default_rng(3)
    blocks = [rng.normal(0.5, 0.2, size=120) for _ in range(cf1.N_BLOCKS)]
    lb1, s1, lens1 = ev.stratified_moving_block_bootstrap(blocks)
    lb2, s2, lens2 = ev.stratified_moving_block_bootstrap(blocks)
    assert lb1 == lb2
    assert np.array_equal(s1, s2)
    assert lens1 == lens2
    assert s1.shape[0] == cf1.BOOTSTRAP_REPLICATES
    # All-positive differentials -> lower bound is positive.
    assert lb1 > 0.0


def test_bootstrap_negative_mean_gives_negative_lower_bound() -> None:
    rng = np.random.default_rng(4)
    blocks = [rng.normal(-0.5, 0.2, size=120) for _ in range(cf1.N_BLOCKS)]
    lb, _s, _l = ev.stratified_moving_block_bootstrap(blocks)
    assert lb < 0.0


# ---------------------------------------------------------------------------
# Secondary metrics
# ---------------------------------------------------------------------------


def test_mse_and_mz_r2_perfect_forecast() -> None:
    rv = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float64)
    y_hat = np.log(rv)
    assert ev.mse_on_variance(rv, y_hat) < 1e-18
    log_rv = np.log(rv + cf1.TARGET_EPSILON)
    r2 = ev.mincer_zarnowitz_r2(log_rv, y_hat)
    assert r2 == pytest.approx(1.0, abs=1e-8)


# ---------------------------------------------------------------------------
# End-to-end verdict routing
# ---------------------------------------------------------------------------


def test_evaluate_pass_with_signal() -> None:
    rows = _make_rows(signal_strength=1.2, seed=20260715)
    result = ev.evaluate(rows)
    assert result.verdict == ev.CF1_VALID_PASS
    assert result.p1 and result.p2 and result.p3 and result.p4
    assert result.delta_equal > 0.0
    assert result.positive_block_count >= 6
    assert result.lb95 > 0.0
    assert len(result.blocks) == 7
    for b in result.blocks:
        assert b.n_eval >= cf1.MIN_BLOCK_VALID_ORIGINS


def test_evaluate_fail_without_signal() -> None:
    rows = _make_rows(signal_strength=0.0, seed=101)
    result = ev.evaluate(rows)
    assert result.verdict == ev.CF1_VALID_FAIL
    assert not (result.p1 and result.p2 and result.p3)


def test_evaluate_invalid_short_block() -> None:
    rows = _make_rows(signal_strength=1.0, seed=7, short_block="B4")
    result = ev.evaluate(rows)
    assert result.verdict == ev.CF1_INVALID_RUN
    assert "B4" in result.invalid_reason


def test_evaluate_invalid_zero_variance_features() -> None:
    rows = _make_rows(signal_strength=0.0, seed=9, constant_features=True)
    result = ev.evaluate(rows)
    assert result.verdict == ev.CF1_INVALID_RUN
    assert "zero_variance" in result.invalid_reason


def test_no_eval_leakage_expanding_training_precedes_block() -> None:
    rows = _make_rows(signal_strength=1.0, seed=5)
    b1_start = cf1.utc_date_start_ms("2024-04-01")
    train = ev._training_rows_for_block(rows, b1_start)
    # Every training origin's target ends at least 24h before the block start.
    assert all(r.target_end_ms <= b1_start - cf1.EMBARGO_MS for r in train)
    # No B1 eval origin is in the B1 training set.
    b1_eval_ids = {r.origin_ms for r in rows if r.block_id == "B1"}
    assert not (b1_eval_ids & {r.origin_ms for r in train})
