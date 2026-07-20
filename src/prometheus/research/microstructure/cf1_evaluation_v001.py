"""Phase 4bn-AZ — CF-1 evaluation: walk-forward OLS, QLIKE, bootstrap, verdict routing.

Implements the frozen Phase 4bn-AY evaluation contract over a set of assembled valid
CF-1 origin rows (target RV, HAR lookbacks, and the three sign-invariant microstructure
snapshots). This module owns:

- the expanding anchored walk-forward with one fit per evaluation block;
- the one-day training-origin embargo (purge subsumed);
- train-only log + z-score preprocessing (population std, ``ddof = 0``);
- the HAR-style OLS baseline and the nested augmented OLS (``numpy.linalg.lstsq``);
- the numerical guards (rank, condition number, zero-variance regressor, non-finite
  coefficients, minimum training / block origins);
- the QLIKE loss with the ``v = RV + 1e-16`` / ``h = max(exp(y_hat), 1e-16)`` safeguard;
- ``d_{i,t}``, ``D_i``, ``Delta_equal``, ``rho``, and the descriptive MSE / MZ R2 metrics;
- the stratified-by-block non-circular moving-block bootstrap (``PCG64(20260715)``,
  10,000 replicates, linear 0.05 lower quantile);
- P1/P2/P3/P4 and the exact ``CF1_VALID_PASS`` / ``CF1_VALID_FAIL`` / ``CF1_INVALID_RUN``
  verdict routing.

No data I/O, no network, no credentials. Pure numpy over rows handed in by the caller.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from . import cf1_realized_volatility_v001 as cf1

# Verdict / outcome vocabulary (frozen).
CF1_VALID_PASS = "CF1_VALID_PASS"
CF1_VALID_FAIL = "CF1_VALID_FAIL"
CF1_INVALID_RUN = "CF1_INVALID_RUN"


class Cf1EvaluationError(RuntimeError):
    """Raised on a structural evaluation-input error (not a scientific outcome)."""


@dataclass(frozen=True)
class OriginRow:
    """One assembled, valid CF-1 origin: target, HAR lookbacks, and feature snapshot.

    All rows passed to :func:`evaluate` must already be valid paired origins per the
    contract (target + HAR + feature all computable). ``block_id`` is ``""`` for a
    train-only warmup origin (e.g. March 2024) that belongs to no evaluation block.
    """

    origin_ms: int
    target_end_ms: int
    block_id: str
    rv: float
    log_rv: float
    rv_h: float
    rv_d: float
    rv_w: float
    x1: float  # rolling_aggtrade_count_60s (> 0)
    x2: float  # rolling_quantity_sum_60s (> 0)
    x3: float  # rolling_quantity_mean_60s (> 0)


# ---------------------------------------------------------------------------
# Design-matrix construction
# ---------------------------------------------------------------------------


def _log_har(rows: list[OriginRow]) -> npt.NDArray[np.float64]:
    """Return the (n, 3) HAR log-variance regressor block ``ln(RV_. + eps)``."""
    eps = cf1.TARGET_EPSILON
    out = np.empty((len(rows), 3), dtype=np.float64)
    for i, r in enumerate(rows):
        out[i, 0] = math.log(r.rv_h + eps)
        out[i, 1] = math.log(r.rv_d + eps)
        out[i, 2] = math.log(r.rv_w + eps)
    return out


def _log_features(rows: list[OriginRow]) -> npt.NDArray[np.float64]:
    """Return the (n, 3) natural-log microstructure feature block (pre-standardization)."""
    out = np.empty((len(rows), 3), dtype=np.float64)
    for i, r in enumerate(rows):
        out[i, 0] = math.log(r.x1)
        out[i, 1] = math.log(r.x2)
        out[i, 2] = math.log(r.x3)
    return out


def _targets(rows: list[OriginRow]) -> npt.NDArray[np.float64]:
    return np.array([r.log_rv for r in rows], dtype=np.float64)


def _rv_actual(rows: list[OriginRow]) -> npt.NDArray[np.float64]:
    return np.array([r.rv for r in rows], dtype=np.float64)


@dataclass(frozen=True)
class TrainTransform:
    """Train-only z-score statistics for the three log microstructure features."""

    mean: npt.NDArray[np.float64]  # (3,)
    std: npt.NDArray[np.float64]  # (3,) population std, ddof=0
    zero_variance: bool


def fit_train_transform(train_log_feat: npt.NDArray[np.float64]) -> TrainTransform:
    """Fit the train-only mean / population-std transform; flag zero-variance columns."""
    mean = train_log_feat.mean(axis=0)
    std = train_log_feat.std(axis=0, ddof=0)
    zero_variance = bool(np.any(std == 0.0))
    return TrainTransform(mean=mean, std=std, zero_variance=zero_variance)


def apply_transform(
    log_feat: npt.NDArray[np.float64], tr: TrainTransform
) -> npt.NDArray[np.float64]:
    """Apply the train-only z-score with ``max(std, 1e-8)`` denominator floor."""
    denom = np.maximum(tr.std, cf1.STANDARDIZATION_EPSILON)
    return (log_feat - tr.mean) / denom


def _design_baseline(log_har: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    n = log_har.shape[0]
    return np.concatenate([np.ones((n, 1), dtype=np.float64), log_har], axis=1)


def _design_augmented(
    log_har: npt.NDArray[np.float64], z_feat: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    n = log_har.shape[0]
    return np.concatenate([np.ones((n, 1), dtype=np.float64), log_har, z_feat], axis=1)


# ---------------------------------------------------------------------------
# OLS + numerical guards
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OlsFit:
    beta: npt.NDArray[np.float64]
    condition_number: float
    rank: int
    n_train: int
    ok: bool
    reason: str


def _condition_number(design: npt.NDArray[np.float64]) -> float:
    sv = np.linalg.svd(design, compute_uv=False)
    if sv.size == 0 or sv[-1] <= 0.0:
        return math.inf
    return float(sv[0] / sv[-1])


def _has_zero_variance_regressor(design: npt.NDArray[np.float64]) -> bool:
    """Return True iff any non-intercept column of *design* has zero variance."""
    if design.shape[1] <= 1:
        return False
    return bool(np.any(design[:, 1:].std(axis=0, ddof=0) == 0.0))


def fit_ols(design: npt.NDArray[np.float64], y: npt.NDArray[np.float64], n_params: int) -> OlsFit:
    """Fit deterministic OLS via ``numpy.linalg.lstsq`` with the frozen numerical guards."""
    n_train = design.shape[0]
    if n_train < cf1.MIN_TRAIN_ORIGINS:
        return OlsFit(np.zeros(n_params), math.inf, 0, n_train, False, "too_few_training_origins")
    if _has_zero_variance_regressor(design):
        return OlsFit(np.zeros(n_params), math.inf, 0, n_train, False, "zero_variance_regressor")
    cond = _condition_number(design)
    if not math.isfinite(cond) or cond > cf1.CONDITION_NUMBER_MAX:
        return OlsFit(np.zeros(n_params), cond, 0, n_train, False, "condition_number_exceeded")
    beta_raw, _residuals, rank, _sv = np.linalg.lstsq(design, y, rcond=None)
    beta = np.asarray(beta_raw, dtype=np.float64)
    if int(rank) < n_params:
        return OlsFit(beta, cond, int(rank), n_train, False, "rank_deficient")
    if not bool(np.all(np.isfinite(beta))):
        return OlsFit(beta, cond, int(rank), n_train, False, "non_finite_coefficients")
    return OlsFit(beta, cond, int(rank), n_train, True, "")


def predict(
    design: npt.NDArray[np.float64], beta: npt.NDArray[np.float64]
) -> npt.NDArray[np.float64]:
    return design @ beta


# ---------------------------------------------------------------------------
# QLIKE + secondary metrics
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class QlikeResult:
    values: npt.NDArray[np.float64]
    finite: bool


def qlike(rv: npt.NDArray[np.float64], y_hat: npt.NDArray[np.float64]) -> QlikeResult:
    """QLIKE with the frozen ``v = RV + eps`` / ``h = max(exp(y_hat), eps)`` safeguard."""
    eps = cf1.TARGET_EPSILON
    v = rv + eps
    h = np.maximum(np.exp(y_hat), eps)
    ratio = v / h
    with np.errstate(divide="ignore", invalid="ignore"):
        loss = ratio - np.log(ratio) - 1.0
    finite = bool(
        np.all(np.isfinite(v))
        and np.all(v > 0)
        and np.all(np.isfinite(h))
        and np.all(h > 0)
        and np.all(np.isfinite(ratio))
        and np.all(np.isfinite(loss))
    )
    return QlikeResult(values=loss, finite=finite)


def mse_on_variance(rv: npt.NDArray[np.float64], y_hat: npt.NDArray[np.float64]) -> float:
    """Mean of ``(RV - exp(y_hat))^2`` (descriptive; never decision-bearing)."""
    resid = rv - np.exp(y_hat)
    return float(np.mean(resid * resid))


def mincer_zarnowitz_r2(
    log_rv_actual: npt.NDArray[np.float64], y_hat: npt.NDArray[np.float64]
) -> float:
    """MZ R2: regress actual ``ln(RV+eps)`` on ``[1, y_hat]``; standard coefficient of det."""
    n = log_rv_actual.shape[0]
    design = np.concatenate([np.ones((n, 1), dtype=np.float64), y_hat.reshape(n, 1)], axis=1)
    beta, _res, _rank, _sv = np.linalg.lstsq(design, log_rv_actual, rcond=None)
    fitted = design @ beta
    ss_res = float(np.sum((log_rv_actual - fitted) ** 2))
    mean = float(np.mean(log_rv_actual))
    ss_tot = float(np.sum((log_rv_actual - mean) ** 2))
    if ss_tot == 0.0:
        return 0.0
    return 1.0 - ss_res / ss_tot


# ---------------------------------------------------------------------------
# Per-block fitting / scoring
# ---------------------------------------------------------------------------


@dataclass
class BlockResult:
    block_id: str
    n_train: int
    n_eval: int
    baseline_qlike: float
    augmented_qlike: float
    d_i: float
    baseline_mse: float
    augmented_mse: float
    baseline_mz_r2: float
    augmented_mz_r2: float
    baseline_condition_number: float
    augmented_condition_number: float
    baseline_rank: int
    augmented_rank: int
    baseline_beta: list[float]
    augmented_beta: list[float]
    zero_rv_count: int
    d_series: npt.NDArray[np.float64] = field(repr=False)
    ok: bool = True
    reason: str = ""
    eval_origin_ms: list[int] = field(default_factory=list, repr=False)
    yhat_base: npt.NDArray[np.float64] = field(
        default_factory=lambda: np.zeros(0, dtype=np.float64), repr=False
    )
    yhat_aug: npt.NDArray[np.float64] = field(
        default_factory=lambda: np.zeros(0, dtype=np.float64), repr=False
    )
    qlike_base: npt.NDArray[np.float64] = field(
        default_factory=lambda: np.zeros(0, dtype=np.float64), repr=False
    )
    qlike_aug: npt.NDArray[np.float64] = field(
        default_factory=lambda: np.zeros(0, dtype=np.float64), repr=False
    )


def _training_rows_for_block(rows: list[OriginRow], block_start_ms: int) -> list[OriginRow]:
    """Expanding anchored training set: valid origins whose target ends >= 24h before block."""
    cutoff = block_start_ms - cf1.EMBARGO_MS
    return [r for r in rows if r.target_end_ms <= cutoff]


def _eval_rows_for_block(rows: list[OriginRow], block_id: str) -> list[OriginRow]:
    return [r for r in rows if r.block_id == block_id]


def fit_and_score_block(rows: list[OriginRow], block_id: str) -> BlockResult:
    """Fit both models on the expanding training set and score them on the block."""
    block_start = cf1.utc_date_start_ms(dict((b[0], b[1]) for b in cf1.BLOCKS)[block_id])
    train = _training_rows_for_block(rows, block_start)
    evals = _eval_rows_for_block(rows, block_id)
    n_train = len(train)
    n_eval = len(evals)

    empty = np.zeros(0, dtype=np.float64)
    if n_eval < cf1.MIN_BLOCK_VALID_ORIGINS:
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            math.inf,
            math.inf,
            0,
            0,
            [],
            [],
            0,
            empty,
            False,
            "block_below_minimum_valid_origins",
        )

    train_log_har = _log_har(train)
    train_log_feat = _log_features(train)
    y_train = _targets(train)
    tr = fit_train_transform(train_log_feat)
    if tr.zero_variance:
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            math.inf,
            math.inf,
            0,
            0,
            [],
            [],
            0,
            empty,
            False,
            "zero_variance_feature_regressor",
        )

    z_train = apply_transform(train_log_feat, tr)
    design_b_train = _design_baseline(train_log_har)
    design_a_train = _design_augmented(train_log_har, z_train)

    fit_b = fit_ols(design_b_train, y_train, cf1.BASELINE_N_PARAMS)
    fit_a = fit_ols(design_a_train, y_train, cf1.AUGMENTED_N_PARAMS)
    if not fit_b.ok:
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            fit_b.condition_number,
            math.inf,
            fit_b.rank,
            0,
            [],
            [],
            0,
            empty,
            False,
            f"baseline_{fit_b.reason}",
        )
    if not fit_a.ok:
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            fit_b.condition_number,
            fit_a.condition_number,
            fit_b.rank,
            fit_a.rank,
            list(fit_b.beta),
            [],
            0,
            empty,
            False,
            f"augmented_{fit_a.reason}",
        )

    eval_log_har = _log_har(evals)
    eval_log_feat = _log_features(evals)
    z_eval = apply_transform(eval_log_feat, tr)
    design_b_eval = _design_baseline(eval_log_har)
    design_a_eval = _design_augmented(eval_log_har, z_eval)
    rv_eval = _rv_actual(evals)
    log_rv_eval = _targets(evals)

    yhat_b = predict(design_b_eval, fit_b.beta)
    yhat_a = predict(design_a_eval, fit_a.beta)
    if not (bool(np.all(np.isfinite(yhat_b))) and bool(np.all(np.isfinite(yhat_a)))):
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            fit_b.condition_number,
            fit_a.condition_number,
            fit_b.rank,
            fit_a.rank,
            list(fit_b.beta),
            list(fit_a.beta),
            0,
            empty,
            False,
            "non_finite_forecast",
        )

    q_b = qlike(rv_eval, yhat_b)
    q_a = qlike(rv_eval, yhat_a)
    if not (q_b.finite and q_a.finite):
        return BlockResult(
            block_id,
            n_train,
            n_eval,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            fit_b.condition_number,
            fit_a.condition_number,
            fit_b.rank,
            fit_a.rank,
            list(fit_b.beta),
            list(fit_a.beta),
            0,
            empty,
            False,
            "non_finite_qlike",
        )

    d_series = q_b.values - q_a.values
    d_i = float(np.mean(d_series))
    return BlockResult(
        block_id=block_id,
        n_train=n_train,
        n_eval=n_eval,
        baseline_qlike=float(np.mean(q_b.values)),
        augmented_qlike=float(np.mean(q_a.values)),
        d_i=d_i,
        baseline_mse=mse_on_variance(rv_eval, yhat_b),
        augmented_mse=mse_on_variance(rv_eval, yhat_a),
        baseline_mz_r2=mincer_zarnowitz_r2(log_rv_eval, yhat_b),
        augmented_mz_r2=mincer_zarnowitz_r2(log_rv_eval, yhat_a),
        baseline_condition_number=fit_b.condition_number,
        augmented_condition_number=fit_a.condition_number,
        baseline_rank=fit_b.rank,
        augmented_rank=fit_a.rank,
        baseline_beta=[float(v) for v in fit_b.beta],
        augmented_beta=[float(v) for v in fit_a.beta],
        zero_rv_count=int(np.count_nonzero(rv_eval == 0.0)),
        d_series=d_series,
        ok=True,
        reason="",
        eval_origin_ms=[r.origin_ms for r in evals],
        yhat_base=yhat_b,
        yhat_aug=yhat_a,
        qlike_base=q_b.values,
        qlike_aug=q_a.values,
    )


# ---------------------------------------------------------------------------
# Stratified moving-block bootstrap (contract section 29)
# ---------------------------------------------------------------------------


def _bootstrap_block_length(n_i: int) -> int:
    return int(math.ceil(n_i ** (1.0 / 3.0)))


def stratified_moving_block_bootstrap(
    d_series_by_block: list[npt.NDArray[np.float64]],
    *,
    replicates: int = cf1.BOOTSTRAP_REPLICATES,
    seed: int = cf1.BOOTSTRAP_SEED,
) -> tuple[float, npt.NDArray[np.float64], list[int]]:
    """Return ``(LB_95, delta_equal_samples, block_lengths)`` for the frozen bootstrap.

    Seven blocks stay separate; each block resamples non-circular moving blocks of
    length ``ceil(n_i^(1/3))`` (allowed starts ``0..n_i-l_i``) with replacement,
    concatenated to at least ``n_i`` and truncated to exactly ``n_i``. Per replicate
    ``D_i^(b) = mean`` and ``Delta_equal^(b) = (1/7) sum_i D_i^(b)``. ``LB_95`` is the
    linear 0.05 quantile.
    """
    if len(d_series_by_block) != cf1.N_BLOCKS:
        raise Cf1EvaluationError(f"bootstrap needs {cf1.N_BLOCKS} blocks")
    rng = np.random.Generator(np.random.PCG64(seed))
    delta = np.zeros(replicates, dtype=np.float64)
    block_lengths: list[int] = []
    for d in d_series_by_block:
        n_i = d.shape[0]
        ell = _bootstrap_block_length(n_i)
        block_lengths.append(ell)
        if ell > n_i:
            raise Cf1EvaluationError("bootstrap block length exceeds block size")
        n_starts = n_i - ell + 1  # allowed start positions 0 .. n_i - ell
        n_blocks_needed = int(math.ceil(n_i / ell))
        starts = rng.integers(0, n_starts, size=(replicates, n_blocks_needed))
        # (replicates, n_blocks_needed, ell) index matrix, then flatten + truncate to n_i.
        offsets = np.arange(ell, dtype=np.int64)
        idx = starts[:, :, None] + offsets[None, None, :]
        idx = idx.reshape(replicates, n_blocks_needed * ell)[:, :n_i]
        sampled = d[idx]  # (replicates, n_i)
        delta += sampled.mean(axis=1)
    delta /= float(cf1.N_BLOCKS)
    lb95 = float(np.quantile(delta, cf1.BOOTSTRAP_LOWER_QUANTILE, method="linear"))
    return lb95, delta, block_lengths


# ---------------------------------------------------------------------------
# Verdict routing
# ---------------------------------------------------------------------------


@dataclass
class EvaluationResult:
    verdict: str
    invalid_reason: str
    blocks: list[BlockResult]
    delta_equal: float
    rho: float
    baseline_qlike_equal: float
    augmented_qlike_equal: float
    positive_block_count: int
    lb95: float
    bootstrap_block_lengths: list[int]
    p1: bool
    p2: bool
    p3: bool
    p4: bool


def evaluate(rows: list[OriginRow]) -> EvaluationResult:
    """Run the full frozen CF-1 evaluation over the assembled valid origins.

    Returns exactly one of ``CF1_VALID_PASS`` / ``CF1_VALID_FAIL`` / ``CF1_INVALID_RUN``.
    A numerical / structural guard failure routes to ``CF1_INVALID_RUN`` (no scientific
    pass or fail). Bootstrap runs only when all seven blocks are valid.
    """
    block_results: list[BlockResult] = []
    for block_id in cf1.BLOCK_IDS:
        block_results.append(fit_and_score_block(rows, block_id))

    # Any block failing a structural / numerical guard -> CF1_INVALID_RUN.
    invalid = [b for b in block_results if not b.ok]
    if invalid:
        return EvaluationResult(
            verdict=CF1_INVALID_RUN,
            invalid_reason=f"{invalid[0].block_id}:{invalid[0].reason}",
            blocks=block_results,
            delta_equal=0.0,
            rho=0.0,
            baseline_qlike_equal=0.0,
            augmented_qlike_equal=0.0,
            positive_block_count=0,
            lb95=0.0,
            bootstrap_block_lengths=[],
            p1=False,
            p2=False,
            p3=False,
            p4=False,
        )

    d_by_block = [b.d_series for b in block_results]
    d_values = np.array([b.d_i for b in block_results], dtype=np.float64)
    delta_equal = float(np.mean(d_values))
    baseline_qlike_equal = float(np.mean([b.baseline_qlike for b in block_results]))
    augmented_qlike_equal = float(np.mean([b.augmented_qlike for b in block_results]))
    rho = delta_equal / baseline_qlike_equal if baseline_qlike_equal != 0.0 else 0.0
    positive_block_count = int(np.count_nonzero(d_values > 0.0))

    lb95, _samples, block_lengths = stratified_moving_block_bootstrap(d_by_block)

    p1 = delta_equal > 0.0
    p2 = positive_block_count >= 6
    p3 = lb95 > 0.0
    p4 = all(b.ok and b.n_eval >= cf1.MIN_BLOCK_VALID_ORIGINS for b in block_results)

    verdict = CF1_VALID_PASS if (p1 and p2 and p3 and p4) else CF1_VALID_FAIL
    return EvaluationResult(
        verdict=verdict,
        invalid_reason="",
        blocks=block_results,
        delta_equal=delta_equal,
        rho=rho,
        baseline_qlike_equal=baseline_qlike_equal,
        augmented_qlike_equal=augmented_qlike_equal,
        positive_block_count=positive_block_count,
        lb95=lb95,
        bootstrap_block_lengths=block_lengths,
        p1=p1,
        p2=p2,
        p3=p3,
        p4=p4,
    )


__all__ = [
    "CF1_INVALID_RUN",
    "CF1_VALID_FAIL",
    "CF1_VALID_PASS",
    "BlockResult",
    "Cf1EvaluationError",
    "EvaluationResult",
    "OlsFit",
    "OriginRow",
    "QlikeResult",
    "TrainTransform",
    "apply_transform",
    "evaluate",
    "fit_and_score_block",
    "fit_ols",
    "fit_train_transform",
    "mincer_zarnowitz_r2",
    "mse_on_variance",
    "predict",
    "qlike",
    "stratified_moving_block_bootstrap",
]
