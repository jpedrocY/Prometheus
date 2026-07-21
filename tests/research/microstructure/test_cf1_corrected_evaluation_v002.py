"""Phase 4bn-BB — tests for the corrected two-feature CF-1 evaluation.

Covers: design shapes (baseline 4 / augmented 6); train-only z-score (ddof=0); zero-variance,
rank, condition, non-finite, min-training and min-block guards; the QLIKE formula and zero-RV
retention; equal block weighting; the deterministic stratified moving-block bootstrap; exact
P1/P2/P3 routing (valid pass, valid fail, invalid run); and the absence of any x3 / mean
dependency. No market data is opened.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from prometheus.research.microstructure import cf1_corrected_contract_v002 as cc
from prometheus.research.microstructure import cf1_corrected_evaluation_v002 as ev
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
    """Generate a synthetic valid-origin dataset with a tunable feature signal (two features)."""
    rng = np.random.default_rng(seed)
    rows: list[ev.OriginRow] = []

    def emit(origin_ms: int, block_id: str) -> None:
        lrvh = rng.normal(-10.0, 1.0)
        lrvd = rng.normal(-10.0, 0.8)
        lrvw = rng.normal(-10.0, 0.6)
        rv_h, rv_d, rv_w = math.exp(lrvh), math.exp(lrvd), math.exp(lrvw)
        z = rng.normal()
        if constant_features:
            x1 = x2 = 1.0
        else:
            x1 = math.exp(z + 0.05 * rng.normal())
            x2 = math.exp(0.9 * z + 0.05 * rng.normal())
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
            )
        )

    m0 = cf1.utc_date_start_ms("2024-03-01")
    for j in range(n_warmup):
        emit(m0 + j * HOUR, "")
    for block_id, start, _end in cf1.BLOCKS:
        s = cf1.utc_date_start_ms(start)
        count = 60 if (short_block is not None and block_id == short_block) else n_eval
        for j in range(count):
            emit(s + (2 + j) * HOUR, block_id)
    return rows


# ---------------------------------------------------------------------------
# Design shape / OLS / preprocessing
# ---------------------------------------------------------------------------


def test_origin_row_has_no_mean_field() -> None:
    fields = ev.OriginRow.__dataclass_fields__
    assert "x1" in fields and "x2" in fields
    assert "x3" not in fields


def test_design_shapes_baseline_4_augmented_6() -> None:
    rows = _make_rows(signal_strength=0.5, seed=1, n_eval=120, n_warmup=120)
    train = rows[:200]
    log_har = ev._log_har(train)
    log_feat = ev._log_features(train)
    assert log_feat.shape[1] == 2  # exactly two microstructure columns
    tr = ev.fit_train_transform(log_feat)
    z = ev.apply_transform(log_feat, tr)
    design_b = ev._design_baseline(log_har)
    design_a = ev._design_augmented(log_har, z)
    assert design_b.shape[1] == cc.BASELINE_N_PARAMS == 4
    assert design_a.shape[1] == cc.AUGMENTED_N_PARAMS == 6


def test_train_transform_ddof0_and_zero_variance_flag() -> None:
    feats = np.array([[0.0, 1.0], [2.0, 1.0]], dtype=np.float64)
    tr = ev.fit_train_transform(feats)
    assert tr.zero_variance is True  # column 1 constant
    assert tr.std[0] == 1.0  # population std of {0,2}
    assert tr.mean.shape == (2,)


def test_ols_recovers_linear_and_guards() -> None:
    rng = np.random.default_rng(0)
    n = 200
    har = rng.normal(size=(n, 3))
    design = ev._design_baseline(har)
    beta_true = np.array([0.7, 0.5, 0.3, 0.2])
    fit = ev.fit_ols(design, design @ beta_true, cc.BASELINE_N_PARAMS)
    assert fit.ok
    assert np.allclose(fit.beta, beta_true, atol=1e-8)


def test_ols_too_few_origins_guard() -> None:
    design = np.ones((10, 6), dtype=np.float64)
    design[:, 1:] = np.random.default_rng(1).normal(size=(10, 5))
    fit = ev.fit_ols(design, np.zeros(10), cc.AUGMENTED_N_PARAMS)
    assert not fit.ok
    assert fit.reason == "too_few_training_origins"


def test_ols_zero_variance_regressor_guard() -> None:
    n = 100
    design = np.ones((n, 6), dtype=np.float64)
    fit = ev.fit_ols(design, np.zeros(n), cc.AUGMENTED_N_PARAMS)
    assert not fit.ok
    assert fit.reason == "zero_variance_regressor"


def test_ols_rank_deficient_guard() -> None:
    rng = np.random.default_rng(2)
    n = 200
    har = rng.normal(size=(n, 3))
    z = rng.normal(size=(n, 2))
    z[:, 1] = z[:, 0]  # duplicate column -> rank deficient augmented design
    design = ev._design_augmented(har, z)
    fit = ev.fit_ols(design, rng.normal(size=n), cc.AUGMENTED_N_PARAMS)
    assert not fit.ok
    assert fit.reason in {"rank_deficient", "condition_number_exceeded", "zero_variance_regressor"}


# ---------------------------------------------------------------------------
# QLIKE
# ---------------------------------------------------------------------------


def test_qlike_zero_rv_retained_and_finite() -> None:
    rv = np.array([0.0, 1e-8, 1.0], dtype=np.float64)
    y_hat = np.log(np.array([1e-8, 1e-8, 1.0], dtype=np.float64))
    res = ev.qlike(rv, y_hat)
    assert res.finite
    assert np.all(np.isfinite(res.values))


def test_qlike_formula_and_minimum() -> None:
    rv = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    good = ev.qlike(rv, np.log(rv))
    bad = ev.qlike(rv, np.log(rv) + 1.0)
    assert float(np.mean(good.values)) < float(np.mean(bad.values))
    assert float(np.mean(good.values)) < 1e-12
    # Explicit formula check at one point.
    v = 2.0 + cf1.TARGET_EPSILON
    h = max(math.exp(math.log(3.0)), cf1.TARGET_EPSILON)
    ratio = v / h
    expected = ratio - math.log(ratio) - 1.0
    single = ev.qlike(np.array([2.0]), np.array([math.log(3.0)]))
    assert single.values[0] == pytest.approx(expected, rel=1e-12)


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


def test_bootstrap_block_length_cube_root_ceil() -> None:
    assert ev._bootstrap_block_length(100) == 5
    assert ev._bootstrap_block_length(1000) == 10


def test_bootstrap_deterministic_and_seeded() -> None:
    rng = np.random.default_rng(3)
    blocks = [rng.normal(0.5, 0.2, size=120) for _ in range(cf1.N_BLOCKS)]
    lb1, s1, lens1 = ev.stratified_moving_block_bootstrap(blocks)
    lb2, s2, lens2 = ev.stratified_moving_block_bootstrap(blocks)
    assert lb1 == lb2
    assert np.array_equal(s1, s2)
    assert lens1 == lens2
    assert s1.shape[0] == cc.BOOTSTRAP_REPLICATES == 10_000
    assert lb1 > 0.0


def test_bootstrap_negative_mean_negative_lb() -> None:
    rng = np.random.default_rng(4)
    blocks = [rng.normal(-0.5, 0.2, size=120) for _ in range(cf1.N_BLOCKS)]
    lb, _s, _l = ev.stratified_moving_block_bootstrap(blocks)
    assert lb < 0.0


# ---------------------------------------------------------------------------
# End-to-end verdict routing
# ---------------------------------------------------------------------------


def test_evaluate_pass_with_signal() -> None:
    rows = _make_rows(signal_strength=1.2, seed=20260715)
    result = ev.evaluate(rows)
    assert result.verdict == ev.CF1_VALID_PASS
    assert result.valid and result.p1 and result.p2 and result.p3
    assert result.delta_equal > 0.0
    assert result.positive_block_count >= 6
    assert result.lb95 > 0.0
    assert len(result.blocks) == 7
    for b in result.blocks:
        assert b.n_eval >= cc.MIN_BLOCK_VALID_ORIGINS
        assert b.augmented_rank == 6
        assert b.baseline_rank == 4
        assert len(b.augmented_beta) == 6
        assert len(b.baseline_beta) == 4


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


def test_no_eval_leakage_expanding_training() -> None:
    rows = _make_rows(signal_strength=1.0, seed=5)
    b1_start = cf1.utc_date_start_ms("2024-04-01")
    train = ev._training_rows_for_block(rows, b1_start)
    assert all(r.target_end_ms <= b1_start - cf1.EMBARGO_MS for r in train)
    b1_eval_ids = {r.origin_ms for r in rows if r.block_id == "B1"}
    assert not (b1_eval_ids & {r.origin_ms for r in train})


def test_equal_block_weighting() -> None:
    rows = _make_rows(signal_strength=0.8, seed=11)
    result = ev.evaluate(rows)
    d_values = [b.d_i for b in result.blocks]
    assert result.delta_equal == pytest.approx(float(np.mean(d_values)), rel=1e-12)
