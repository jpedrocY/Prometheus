"""Phase 4bn-AJ — pre-v002 fixed baseline run + pre-registered verdict.

This is the **fixed baseline run** slot of the Phase 4bn-AE pre-registered ML-arc
budget (renumbered AF skeleton → AG builder-authorization → AH builder+run → AI
descriptive diagnostics → **AJ fixed baseline run** → AK arc-decision). It runs
the three pre-registered fixed baselines **once each** and records a verdict under
the frozen Phase 4bn-AE §16/§17 success / continue / kill criteria.

Baselines (Phase 4bn-AE §13/§18; implementations reused verbatim from the
committed Phase 4bn-B ``ml_baseline_models_v002`` pure-numpy suite):

1. **majority** — predict the modal ``train``-split class on every row
   (``fit_majority_class_baseline``).
2. **persistence** — predict ``sign(rolling_log_return_past_window_15s)`` matched
   to the 15s target horizon (``PersistenceBaseline``).
3. **linear** — L2 multinomial-logistic softmax regression, fit once by mini-batch
   SGD with the **frozen** Phase 4bn-B hyperparameters
   (``build_l2_logistic_regression_trainer``: 1 epoch, batch 8192, lr 0.1, L2 1e-4,
   grad-clip 10, seed 20260528). No model selection, no hyperparameter search, no
   threshold tuning, no second model family.

Data path (all read-only / streamed / bounded-memory):

- reads the four Phase 4bn-AH dataset-spec artefacts read-only and re-verifies
  their Phase 4bb-F sidecars, the leakage proof flags, the manifest counts, the
  split index, and the train-only transform hash;
- **applies** the AH-fitted ``train_only_transform.json`` statistics (it does not
  refit them — nothing is fit on validation / holdout);
- reads only the AH-verified pre-v002 feature (4bn-S) / label (4bn-W) Parquet via
  the committed Phase 4bn-AH read path, excludes the two embargo dates, drops
  invalid / censored / null rows exactly as AH did (never imputes a target),
  fits the L2 model on ``train`` only, and evaluates all three baselines on
  ``train`` / ``validation`` / ``holdout`` at aggregate / UTC-month / UTC-date
  granularity;
- writes compact aggregate result / proof JSON (Phase 4bb-F sidecars) to the
  single local **gitignored** AJ namespace
  ``data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001/`` —
  no model binaries, no row-level predictions.

Hard boundaries (fail-closed): never reads the v002 terminal window or the sealed
test (``test_rows_loaded = 0``); never mutates the AH namespace; runs no strategy /
signals / PnL / backtest; computes no Sharpe / trading hit-rate; ranks no features;
selects no model; tunes no threshold; flips no eligibility; authorizes no
successor. The ``forward_direction_15s`` target is an information diagnostic only
(Phase 4bn-AE §9/§19) — no result licenses a tradability / economic claim.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import pyarrow.parquet as pq

from . import ml_baseline_design_v002 as design
from . import ml_baseline_metrics_v002 as metrics
from . import ml_baseline_models_v002 as models
from . import pre_v002_ml_dataset_contract as contract
from . import pre_v002_ml_dataset_run as ah
from . import pre_v002_split_policy as split_policy

# ---------------------------------------------------------------------------
# Identity / paths
# ---------------------------------------------------------------------------

RUN_PHASE = "phase-4bn-aj"
BASELINE_VERSION = "pre_v002_fixed_baseline_v001"
HORIZON_LABEL = "15s"

REPO_ROOT = ah.REPO_ROOT
AH_NAMESPACE = ah.OUTPUT_NAMESPACE
OUTPUT_NAMESPACE = (
    "data/research/microstructure/ml_baselines/pre_v002_fixed_baseline_v001"
)

# Persistence baseline uses the past-window log-return matched to the 15s target
# horizon (Phase 4bn-AE §13: "sign of the past-window return").
PERSISTENCE_FEATURE = "rolling_log_return_past_window_15s"

FAMILY_MAJORITY = design.BASELINE_MAJORITY_CLASS
FAMILY_PERSISTENCE = design.BASELINE_PERSISTENCE_PAST_RETURN
FAMILY_LINEAR = design.BASELINE_LOGISTIC_REGRESSION_L2
FAMILIES: tuple[str, str, str] = (FAMILY_MAJORITY, FAMILY_PERSISTENCE, FAMILY_LINEAR)

_AH_ARTEFACTS = (
    "dataset_manifest.json",
    "train_only_transform.json",
    "split_index.json",
    "leakage_split_integrity_proof.json",
)


class PreV002FixedBaselineError(RuntimeError):
    """Raised when a Phase 4bn-AJ fixed-baseline invariant fails closed."""


# ---------------------------------------------------------------------------
# AH artefact loading + re-verification (read-only)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AhArtefacts:
    """The four re-verified Phase 4bn-AH dataset-spec artefacts (read-only)."""

    manifest: dict[str, Any]
    transform: dict[str, Any]
    split_index: dict[str, Any]
    proof: dict[str, Any]
    sha256: dict[str, str]


def load_and_verify_ah_artefacts(namespace: str = AH_NAMESPACE) -> AhArtefacts:
    """Load the four AH artefacts read-only, re-verifying sidecars + invariants.

    Fails closed (``PreV002FixedBaselineError``) if any sidecar mismatches, the
    proof flags are wrong, the manifest counts do not reconcile, the split index
    is not 275 dates, or the transform feature-list hash disagrees with the
    manifest / proof. Reads only; writes / mutates nothing.
    """
    base = REPO_ROOT / namespace
    loaded: dict[str, dict[str, Any]] = {}
    shas: dict[str, str] = {}
    for name in _AH_ARTEFACTS:
        path = base / name
        if not path.is_file():
            raise PreV002FixedBaselineError(f"missing AH artefact {path}")
        sidecar = path.with_name(name + ".sha256")
        if not sidecar.is_file():
            raise PreV002FixedBaselineError(f"missing AH sidecar {sidecar}")
        digest = ah.sha256_file(path)
        side_sha, side_name = ah.parse_sidecar(sidecar.read_text(encoding="utf-8"))
        if side_name != name:
            raise PreV002FixedBaselineError(
                f"AH sidecar name {side_name!r} != {name!r}"
            )
        if side_sha != digest:
            raise PreV002FixedBaselineError(
                f"AH artefact {name} sha {digest[:12]}… != sidecar {side_sha[:12]}…"
            )
        loaded[name] = json.loads(path.read_text(encoding="utf-8"))
        shas[name] = digest

    art = AhArtefacts(
        manifest=loaded["dataset_manifest.json"],
        transform=loaded["train_only_transform.json"],
        split_index=loaded["split_index.json"],
        proof=loaded["leakage_split_integrity_proof.json"],
        sha256=shas,
    )
    _assert_ah_invariants(art)
    return art


def _assert_ah_invariants(art: AhArtefacts) -> None:
    """Fail closed unless the AH artefacts encode the expected preserved state."""
    proof = art.proof
    split = proof.get("split", {})
    if split.get("v002_terminal_window_read") is not False:
        raise PreV002FixedBaselineError("AH proof v002_terminal_window_read != false")
    if split.get("sealed_test_split_touched") is not False:
        raise PreV002FixedBaselineError("AH proof sealed_test_split_touched != false")
    if int(split.get("test_rows_loaded", -1)) != 0:
        raise PreV002FixedBaselineError("AH proof test_rows_loaded != 0")
    for flag in ("no_random", "no_shuffle", "no_kfold", "no_bootstrap"):
        if split.get(flag) is not True:
            raise PreV002FixedBaselineError(f"AH proof split.{flag} != true")
    if split.get("no_embargo_date_used") is not True:
        raise PreV002FixedBaselineError("AH proof no_embargo_date_used != true")
    crossings = proof.get("per_horizon_boundary_crossing_rows", {})
    if any(int(v) != 0 for v in crossings.values()):
        raise PreV002FixedBaselineError("AH proof per-horizon boundary crossings != 0")

    man = art.manifest
    if int(man.get("streamed_row_count", -1)) != contract.EXPECTED_ROW_COUNT:
        raise PreV002FixedBaselineError("AH manifest streamed_row_count mismatch")
    raw = man.get("split_raw_rows", {})
    kept = man.get("split_filtered_rows", {})
    expected_raw = {
        "train": 304_816_127,
        "embargo": 3_071_370,
        "validation": 68_578_296,
        "holdout": 23_535_902,
    }
    expected_kept = {"train": 304_816_127, "validation": 68_578_296, "holdout": 23_535_860}
    for k, v in expected_raw.items():
        if int(raw.get(k, -1)) != v:
            raise PreV002FixedBaselineError(f"AH manifest split_raw_rows[{k}] mismatch")
    for k, v in expected_kept.items():
        if int(kept.get(k, -1)) != v:
            raise PreV002FixedBaselineError(
                f"AH manifest split_filtered_rows[{k}] mismatch"
            )
    if man.get("dropped_by_split_and_reason", {}).get("holdout", {}).get("censored") != 42:
        raise PreV002FixedBaselineError("AH manifest holdout censored drop != 42")

    per_date = art.split_index.get("per_date", [])
    if len(per_date) != 275:
        raise PreV002FixedBaselineError("AH split_index per_date != 275")

    flh = ah.feature_list_hash()
    if art.transform.get("feature_list_hash") != flh:
        raise PreV002FixedBaselineError("AH transform feature_list_hash mismatch")
    if man.get("feature_list_hash") != flh:
        raise PreV002FixedBaselineError("AH manifest feature_list_hash mismatch")
    if proof.get("active_feature_list_hash") != flh:
        raise PreV002FixedBaselineError("AH proof active_feature_list_hash mismatch")
    if art.transform.get("fit_split") != "train":
        raise PreV002FixedBaselineError("AH transform fit_split != train")


# ---------------------------------------------------------------------------
# Train-only standardizer (APPLIES the AH transform; never refits)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrainOnlyStandardizer:
    """Apply the AH-fitted train-only transform to a feature matrix.

    ``mean`` / ``std`` are per-column arrays aligned to
    ``contract.ALLOWED_FEATURE_COLUMNS``. Boolean flag columns
    (``STANDARDIZE_BOOLEAN_FLAGS = False``) pass through their imputed 0/1 value.
    Null numeric values are imputed to the fixed ``IMPUTATION_FILL_VALUE`` (0.0)
    before standardization, matching the AH builder's fit-time null handling.
    """

    columns: tuple[str, ...]
    mean: npt.NDArray[Any]
    std: npt.NDArray[Any]
    is_boolean: npt.NDArray[Any]
    epsilon: float
    fill_value: float

    @property
    def persistence_index(self) -> int:
        return self.columns.index(PERSISTENCE_FEATURE)

    def transform(self, x_raw: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """Return the standardized matrix for *x_raw* (shape ``(n, 45)``)."""
        if x_raw.shape[1] != len(self.columns):
            raise PreV002FixedBaselineError(
                f"feature width {x_raw.shape[1]} != {len(self.columns)}"
            )
        x = np.where(np.isfinite(x_raw), x_raw, self.fill_value).astype(
            np.float64, copy=False
        )
        denom = np.maximum(self.std, self.epsilon)
        standardized: npt.NDArray[Any] = (x - self.mean) / denom
        # Boolean flag columns pass through their imputed value unchanged.
        if self.is_boolean.any():
            standardized[:, self.is_boolean] = x[:, self.is_boolean]
        return standardized


def build_standardizer(transform: dict[str, Any]) -> TrainOnlyStandardizer:
    """Build a :class:`TrainOnlyStandardizer` from ``train_only_transform.json``."""
    cols = contract.ALLOWED_FEATURE_COLUMNS
    per = transform["per_feature"]
    mean = np.array([float(per[c]["train_mean"]) for c in cols], dtype=np.float64)
    std = np.array([float(per[c]["train_std"]) for c in cols], dtype=np.float64)
    boolean_cols = frozenset(design.BOOLEAN_FEATURE_COLUMN_NAMES)
    is_bool = np.array([c in boolean_cols for c in cols], dtype=bool)
    return TrainOnlyStandardizer(
        columns=tuple(cols),
        mean=mean,
        std=std,
        is_boolean=is_bool,
        epsilon=float(transform.get("standardization_epsilon", contract.STANDARDIZATION_EPSILON)),
        fill_value=float(transform.get("imputation_fill_value", contract.IMPUTATION_FILL_VALUE)),
    )


# ---------------------------------------------------------------------------
# Descriptive cost-realism accumulator (Phase 4bn-AE §15; descriptive only)
# ---------------------------------------------------------------------------

# |forward_log_return_15s| histogram bucket edges in basis points. The exact
# > 8 bps (one-way) and > 16 bps (round-trip) shares are read off the cumulative
# counts; approximate quantiles are linearly interpolated within a bucket.
COST_BPS_EDGES: tuple[float, ...] = (
    0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 24.0, 32.0, 48.0,
    64.0, 96.0, 128.0, 192.0, 256.0, 512.0, 1024.0, float("inf"),
)


@dataclass
class CostRealism:
    """Descriptive |forward_log_return_15s| distribution vs the 16 bps lock."""

    n: int = 0
    sum_abs_bps: float = 0.0
    max_abs_bps: float = 0.0
    hist: npt.NDArray[Any] = field(
        default_factory=lambda: np.zeros(len(COST_BPS_EDGES) - 1, dtype=np.int64)
    )

    def update(self, forward_log_return: npt.NDArray[Any]) -> None:
        if forward_log_return.size == 0:
            return
        abs_bps = np.abs(forward_log_return) * 10_000.0
        self.n += int(abs_bps.size)
        self.sum_abs_bps += float(abs_bps.sum())
        m = float(abs_bps.max())
        if m > self.max_abs_bps:
            self.max_abs_bps = m
        edges = np.asarray(COST_BPS_EDGES, dtype=np.float64)
        idx = np.clip(np.digitize(abs_bps, edges, right=False) - 1, 0, self.hist.size - 1)
        np.add.at(self.hist, idx, 1)

    def _share_above_bps(self, thresh_bps: float) -> float:
        if self.n == 0:
            return 0.0
        edges = np.asarray(COST_BPS_EDGES, dtype=np.float64)
        # Count rows strictly above thresh_bps; thresholds coincide with edges.
        above = 0
        for b in range(self.hist.size):
            lo = edges[b]
            if lo >= thresh_bps:
                above += int(self.hist[b])
        return above / float(self.n)

    def _approx_quantile_bps(self, q: float) -> float:
        if self.n == 0:
            return 0.0
        edges = np.asarray(COST_BPS_EDGES, dtype=np.float64)
        target = q * self.n
        cum = 0
        for b in range(self.hist.size):
            c = int(self.hist[b])
            if cum + c >= target:
                lo = edges[b]
                hi = edges[b + 1]
                if not np.isfinite(hi):
                    return float(lo)
                frac = (target - cum) / c if c > 0 else 0.0
                return float(lo + frac * (hi - lo))
            cum += c
        return float(edges[-2])

    def as_dict(self) -> dict[str, Any]:
        return {
            "n_rows": int(self.n),
            "cost_lock_bps_per_side": contract.LOCKED_COST_BPS_PER_SIDE,
            "cost_lock_bps_round_trip": contract.LOCKED_ROUND_TRIP_COST_BPS,
            "mean_abs_return_bps": (self.sum_abs_bps / self.n) if self.n else 0.0,
            "max_abs_return_bps": self.max_abs_bps,
            "approx_median_abs_return_bps": self._approx_quantile_bps(0.5),
            "approx_p90_abs_return_bps": self._approx_quantile_bps(0.90),
            "approx_p99_abs_return_bps": self._approx_quantile_bps(0.99),
            "share_abs_return_gt_8bps_one_way": self._share_above_bps(8.0),
            "share_abs_return_gt_16bps_round_trip": self._share_above_bps(16.0),
            "histogram_bps_edges": list(COST_BPS_EDGES[:-1]) + ["inf"],
            "histogram_counts": [int(x) for x in self.hist],
        }


# ---------------------------------------------------------------------------
# Evaluator registry (family × split × granularity), lazily created
# ---------------------------------------------------------------------------


@dataclass
class EvalRegistry:
    """Holds all per-(family, split, block) streaming evaluators + calibration."""

    agg: dict[tuple[str, str], models.StreamingEvaluator] = field(default_factory=dict)
    by_month: dict[tuple[str, str, str], models.StreamingEvaluator] = field(
        default_factory=dict
    )
    by_date: dict[tuple[str, str, str], models.StreamingEvaluator] = field(
        default_factory=dict
    )
    # Calibration (linear model only), per split, aggregate.
    calib: dict[str, metrics.CalibrationSummary] = field(default_factory=dict)
    # Cost realism per split and per (split, month).
    cost_split: dict[str, CostRealism] = field(default_factory=dict)
    cost_month: dict[tuple[str, str], CostRealism] = field(default_factory=dict)
    # Train class counts (re-derived; cross-checked vs AH manifest).
    train_class_counts: dict[int, int] = field(
        default_factory=lambda: {-1: 0, 0: 0, 1: 0}
    )

    def _ev(
        self,
        store: dict[Any, models.StreamingEvaluator],
        key: tuple[Any, ...],
        family: str,
        split: str,
    ) -> models.StreamingEvaluator:
        ev = store.get(key)
        if ev is None:
            ev = models.StreamingEvaluator(family=family, split=split, horizon=HORIZON_LABEL)
            store[key] = ev
        return ev

    def update(
        self,
        *,
        family: str,
        split: str,
        month: str,
        date: str,
        y_true: npt.NDArray[Any],
        pred_class: npt.NDArray[Any],
        pred_proba: npt.NDArray[Any],
    ) -> None:
        targets: tuple[tuple[dict[Any, models.StreamingEvaluator], tuple[Any, ...]], ...] = (
            (self.agg, (family, split)),
            (self.by_month, (family, split, month)),
            (self.by_date, (family, split, date)),
        )
        for store, key in targets:
            self._ev(store, key, family, split).update(
                y_true=y_true,
                predicted_class=pred_class,
                predicted_proba=pred_proba,
                forward_log_returns=None,
            )

    def update_calibration(
        self,
        split: str,
        pred_proba: npt.NDArray[Any],
        pred_class: npt.NDArray[Any],
        y_true: npt.NDArray[Any],
    ) -> None:
        cs = self.calib.get(split)
        if cs is None:
            cs = metrics.CalibrationSummary(
                family=FAMILY_LINEAR, split=split, horizon=HORIZON_LABEL
            )
            self.calib[split] = cs
        cs.update(predicted_proba=pred_proba, predicted_class=pred_class, y_true=y_true)

    def update_cost(self, split: str, month: str, forward_log_return: npt.NDArray[Any]) -> None:
        cs = self.cost_split.get(split)
        if cs is None:
            cs = CostRealism()
            self.cost_split[split] = cs
        cs.update(forward_log_return)
        km = (split, month)
        cm = self.cost_month.get(km)
        if cm is None:
            cm = CostRealism()
            self.cost_month[km] = cm
        cm.update(forward_log_return)


# ---------------------------------------------------------------------------
# Streaming partition read (reuses the AH verified read path + filtering)
# ---------------------------------------------------------------------------

_LABEL_COLS = list(ah._LABEL_READ_COLS)
_FEATURE_COLS = [*ah._FEATURE_KEY_COLS, *contract.ALLOWED_FEATURE_COLUMNS]


@dataclass
class _KeptBatch:
    y: npt.NDArray[Any]  # int8 {-1,0,1}
    x_std: npt.NDArray[Any]  # (k, 45) standardized
    persistence_sign: npt.NDArray[Any]  # int8 {-1,0,1}
    forward_log_return: npt.NDArray[Any]  # float64


def _read_kept_batch(
    ref: ah.PartitionRef, std: TrainOnlyStandardizer
) -> _KeptBatch | None:
    """Read one model-eligible partition, filter, standardize; return kept rows.

    Returns ``None`` for embargo dates (dropped in full). Reuses the AH alignment
    check and the identical drop precedence (invalid → censored → null_dir →
    null_lr); never imputes a target.
    """
    if ref.split == split_policy.EMBARGO:
        return None
    ltab = pq.read_table(ref.label_parquet, columns=_LABEL_COLS)
    ftab = pq.read_table(ref.feature_parquet, columns=_FEATURE_COLS)
    ah._check_alignment_vectorized(ftab, ltab, ref.date)

    invalid = ltab.column(contract.LABEL_INVALID_PRICE_FLAG).to_numpy(
        zero_copy_only=False
    ).astype(bool)
    censored = ltab.column(contract.PRIMARY_CENSORED_FLAG).to_numpy(
        zero_copy_only=False
    ).astype(bool)
    direction = ltab.column(contract.PRIMARY_TARGET)
    dir_null = np.asarray(direction.is_null().to_numpy(zero_copy_only=False))
    logret = ltab.column(contract.PRIMARY_LOG_RETURN)
    lr_null = np.asarray(logret.is_null().to_numpy(zero_copy_only=False))

    drop_invalid = invalid
    drop_censored = censored & ~drop_invalid
    drop_null_dir = dir_null & ~drop_invalid & ~drop_censored
    drop_null_lr = lr_null & ~drop_invalid & ~drop_censored & ~drop_null_dir
    keep = ~(drop_invalid | drop_censored | drop_null_dir | drop_null_lr)
    keep_idx = np.nonzero(keep)[0]
    if keep_idx.size == 0:
        return _KeptBatch(
            y=np.empty(0, dtype=np.int8),
            x_std=np.empty((0, len(std.columns)), dtype=np.float64),
            persistence_sign=np.empty(0, dtype=np.int8),
            forward_log_return=np.empty(0, dtype=np.float64),
        )

    y = np.asarray(direction.to_numpy(zero_copy_only=False))[keep_idx].astype(np.int8)
    ret = ah._col_to_float64(ltab, contract.PRIMARY_LOG_RETURN)[keep_idx]

    x_raw = np.empty((keep_idx.size, len(std.columns)), dtype=np.float64)
    for j, col in enumerate(std.columns):
        x_raw[:, j] = ah._col_to_float64(ftab, col)[keep_idx]
    x_std = std.transform(x_raw)

    # Persistence sign from the imputed (not standardized) past-window feature.
    past = x_raw[:, std.persistence_index]
    past = np.where(np.isfinite(past), past, std.fill_value)
    persistence_sign = np.sign(past).astype(np.int8)
    return _KeptBatch(y=y, x_std=x_std, persistence_sign=persistence_sign, forward_log_return=ret)


# ---------------------------------------------------------------------------
# Verdict (Phase 4bn-AE §16 / §17), applied to the computed metrics
# ---------------------------------------------------------------------------

VERDICT_KILL = "CLOSE_ML_BASELINE_ARC"
VERDICT_CONTINUE = "CONTINUE_ONE_FOLLOWUP"
VERDICT_INVESTIGATE = "INVESTIGATE_AMBIGUOUS"


@dataclass(frozen=True)
class VerdictInputs:
    """The exact quantities the pre-registered §16/§17 rules consume."""

    val_acc_linear: float
    val_acc_majority: float
    val_acc_persistence: float
    val_balacc_linear: float
    val_balacc_majority: float
    val_macro_f1_linear: float
    val_macro_f1_majority: float
    holdout_acc_uplift_vs_majority: float
    holdout_macro_f1_uplift_vs_majority: float
    val_date_block_agreement: float  # fraction of val dates with positive uplift vs majority
    val_month_block_agreement: float  # fraction of val months with positive uplift vs majority
    calibration_usable: bool
    high_conf_tail_beats_majority: bool
    cost_share_gt_16bps: float


def compute_verdict(v: VerdictInputs) -> dict[str, Any]:
    """Return the pre-registered §16/§17 verdict for *v* (no softening).

    Deterministic function of the frozen Phase 4bn-AE thresholds
    (``SUCCESS_ACCURACY_UPLIFT_PP`` = 2.0 pp over **both** floors,
    ``SUCCESS_BALANCED_ACCURACY_UPLIFT_PP`` = 1.0 pp, ``SUCCESS_MACRO_F1_UPLIFT``
    = 0.03) plus block-agreement (>50%) and holdout-no-sign-reversal.
    """
    acc_pp = contract.SUCCESS_ACCURACY_UPLIFT_PP  # 2.0
    balacc_pp = contract.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP  # 1.0
    f1_abs = contract.SUCCESS_MACRO_F1_UPLIFT  # 0.03

    acc_uplift_vs_majority_pp = (v.val_acc_linear - v.val_acc_majority) * 100.0
    acc_uplift_vs_persistence_pp = (v.val_acc_linear - v.val_acc_persistence) * 100.0
    beats_both_floors_acc = (
        acc_uplift_vs_majority_pp >= acc_pp and acc_uplift_vs_persistence_pp >= acc_pp
    )
    balacc_uplift_pp = (v.val_balacc_linear - v.val_balacc_majority) * 100.0
    macro_f1_uplift = v.val_macro_f1_linear - v.val_macro_f1_majority
    balacc_fails = balacc_uplift_pp < balacc_pp
    macro_f1_fails = macro_f1_uplift < f1_abs

    # Block-agreement: improvement must appear in a MAJORITY (>50%) of validation
    # date-blocks AND month-blocks (§16/§10-§12).
    blocks_majority = (
        v.val_date_block_agreement > 0.5 and v.val_month_block_agreement > 0.5
    )
    # Holdout sign reversal of the validation uplift (accuracy or macro-F1).
    holdout_sign_reversal = (
        v.holdout_acc_uplift_vs_majority < 0.0
        or v.holdout_macro_f1_uplift_vs_majority < 0.0
    )
    calibration_unusable = not v.calibration_usable
    classification_margins_fail = not (beats_both_floors_acc and (macro_f1_uplift >= f1_abs))
    cost_rarely_relevant = v.cost_share_gt_16bps < 0.01  # <1% of 15s moves clear cost

    kill_reasons: list[str] = []
    if not beats_both_floors_acc:
        kill_reasons.append(
            f"validation accuracy does not beat BOTH majority and persistence "
            f"floors by >= {acc_pp} pp "
            f"(vs_majority={acc_uplift_vs_majority_pp:.3f} pp, "
            f"vs_persistence={acc_uplift_vs_persistence_pp:.3f} pp)"
        )
    if balacc_fails and macro_f1_fails:
        kill_reasons.append(
            f"balanced-accuracy uplift < {balacc_pp} pp ({balacc_uplift_pp:.3f}) "
            f"AND macro-F1 uplift < {f1_abs} ({macro_f1_uplift:.4f})"
        )
    if not blocks_majority:
        kill_reasons.append(
            "improvement not present in a majority of validation date/month blocks "
            f"(date_agreement={v.val_date_block_agreement:.3f}, "
            f"month_agreement={v.val_month_block_agreement:.3f})"
        )
    if holdout_sign_reversal:
        kill_reasons.append(
            "internal-holdout dry-run reverses the sign of the validation uplift "
            f"(acc_uplift={v.holdout_acc_uplift_vs_majority:.4f}, "
            f"macro_f1_uplift={v.holdout_macro_f1_uplift_vs_majority:.4f})"
        )
    if calibration_unusable and classification_margins_fail:
        kill_reasons.append(
            "calibration unusable AND classification lift also fails the margins"
        )
    if cost_rarely_relevant and classification_margins_fail:
        kill_reasons.append(
            "cost-descriptive share > 16 bps is tiny AND information lift also fails"
        )

    continue_all = (
        beats_both_floors_acc
        and (macro_f1_uplift >= f1_abs)
        and not holdout_sign_reversal
        and blocks_majority
        and (v.calibration_usable or (beats_both_floors_acc and blocks_majority))
    )

    if kill_reasons:
        verdict = VERDICT_KILL
    elif continue_all:
        verdict = VERDICT_CONTINUE
    else:
        verdict = VERDICT_INVESTIGATE

    return {
        "verdict": verdict,
        "kill_reasons": kill_reasons,
        "derived": {
            "acc_uplift_vs_majority_pp": acc_uplift_vs_majority_pp,
            "acc_uplift_vs_persistence_pp": acc_uplift_vs_persistence_pp,
            "beats_both_floors_accuracy_2pp": beats_both_floors_acc,
            "balanced_accuracy_uplift_pp": balacc_uplift_pp,
            "macro_f1_uplift": macro_f1_uplift,
            "macro_f1_meets_0p03": macro_f1_uplift >= f1_abs,
            "val_date_block_agreement": v.val_date_block_agreement,
            "val_month_block_agreement": v.val_month_block_agreement,
            "blocks_majority_agreement": blocks_majority,
            "holdout_sign_reversal": holdout_sign_reversal,
            "calibration_usable": v.calibration_usable,
            "high_conf_tail_beats_majority": v.high_conf_tail_beats_majority,
            "cost_share_gt_16bps": v.cost_share_gt_16bps,
            "cost_rarely_relevant": cost_rarely_relevant,
        },
        "thresholds": {
            "success_accuracy_uplift_pp": acc_pp,
            "success_balanced_accuracy_uplift_pp": balacc_pp,
            "success_macro_f1_uplift": f1_abs,
            "block_agreement_rule": "majority_gt_50pct_of_validation_date_and_month_blocks",
            "high_confidence_threshold": contract.HIGH_CONFIDENCE_THRESHOLD,
        },
    }


# ---------------------------------------------------------------------------
# Metric enrichment + block-agreement helpers
# ---------------------------------------------------------------------------


def _enrich_metrics(ev: models.StreamingEvaluator) -> dict[str, Any]:
    """Return the evaluator metrics + derived distribution / zero-rate fields."""
    d = ev.as_dict()
    conf = ev.confusion
    n = int(conf.sum())
    pred_dist = conf.sum(axis=0)  # columns = predicted
    true_dist = conf.sum(axis=1)  # rows = true
    names = design.CLASS_LABELS
    d["predicted_class_distribution"] = {
        design.CLASS_DISPLAY_NAMES[names[i]]: int(pred_dist[i]) for i in range(3)
    }
    d["true_class_distribution"] = {
        design.CLASS_DISPLAY_NAMES[names[i]]: int(true_dist[i]) for i in range(3)
    }
    flat_idx = 1  # class 0 == flat
    d["zero_class_prevalence"] = (float(true_dist[flat_idx]) / n) if n else 0.0
    d["predicted_zero_rate"] = (float(pred_dist[flat_idx]) / n) if n else 0.0
    return d


def _block_agreement(reg: EvalRegistry, split: str, by: str) -> float:
    """Fraction of *split* blocks where linear accuracy exceeds the majority floor.

    *by* is ``"month"`` or ``"date"``. Only blocks with >0 rows are counted.
    """
    store = reg.by_month if by == "month" else reg.by_date
    keys = sorted({k[2] for k in store if k[1] == split and k[0] == FAMILY_LINEAR})
    if not keys:
        return 0.0
    positive = 0
    total = 0
    for blk in keys:
        lin = store.get((FAMILY_LINEAR, split, blk))
        maj = store.get((FAMILY_MAJORITY, split, blk))
        if lin is None or maj is None or lin.n_rows == 0:
            continue
        total += 1
        if lin.accuracy() > maj.accuracy():
            positive += 1
    return (positive / total) if total else 0.0


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run(*, output_namespace: str = OUTPUT_NAMESPACE, progress: bool = True) -> dict[str, Any]:
    """Execute the single fixed-baseline run + verdict; return a summary dict.

    Fails closed on any pre-run check, alignment, or output-boundary violation.
    On success writes compact aggregate result / proof JSON + Phase 4bb-F sidecars
    inside *output_namespace* only (no model binaries, no row-level predictions).
    """
    t0 = time.monotonic()
    out_dir = REPO_ROOT / output_namespace

    # One-run guard.
    if (out_dir / "baseline_run_manifest.json").exists():
        raise PreV002FixedBaselineError(
            "AJ baseline already run at this namespace; a rerun requires separate "
            "operator authorization (no result-seeking rerun is permitted)"
        )

    # --- Budget preflight (D: >= 500 GiB) ---
    d_free_before = ah.measure_d_free_gib()
    preflight = ah.evaluate_budget_preflight(d_free_before)
    if not preflight.passed:
        raise PreV002FixedBaselineError(
            f"budget preflight failed closed: {preflight.breaches!r}"
        )

    # --- Pre-run checks (read-only) ---
    if progress:
        print("[pre-run] verifying AH artefacts + sidecars…", flush=True)
    art = load_and_verify_ah_artefacts()
    std = build_standardizer(art.transform)

    if progress:
        print("[pre-run] verifying source bindings + 550 parquet sidecars…", flush=True)
    binding = ah.verify_manifest_and_gate_hashes()
    ah.verify_source_scope(binding)
    split_commit = ah.bind_split_authority()
    refs = ah.verify_per_parquet_sidecars_and_inventory(binding, progress=progress)
    if len(refs) != 275:
        raise PreV002FixedBaselineError(f"expected 275 partitions, got {len(refs)}")

    # --- Fit pass: L2 SGD on train only; re-derive majority train counts ---
    trainer = models.build_l2_logistic_regression_trainer(len(contract.ALLOWED_FEATURE_COLUMNS))
    train_counts = {-1: 0, 0: 0, 1: 0}
    n_train_processed = 0
    for i, ref in enumerate(refs):
        if ref.split != split_policy.TRAIN:
            continue
        batch = _read_kept_batch(ref, std)
        if batch is None or batch.y.size == 0:
            continue
        for cls in (-1, 0, 1):
            train_counts[cls] += int((batch.y == cls).sum())
        trainer.partial_fit(batch.x_std, batch.y)
        n_train_processed += int(batch.y.size)
        if progress and (i + 1) % 25 == 0:
            ah.assert_budget_during()
            print(f"[fit] {i + 1}/275 (train rows fit {n_train_processed:,})", flush=True)
    linear_model = trainer.finalize()

    # Cross-check re-derived train counts vs AH manifest (fail closed on drift).
    ah_train = art.manifest["split_class_counts"]["train"]
    if {str(k): v for k, v in train_counts.items()} != {
        "-1": int(ah_train["-1"]), "0": int(ah_train["0"]), "1": int(ah_train["1"])
    }:
        raise PreV002FixedBaselineError(
            f"re-derived train class counts {train_counts} != AH manifest {ah_train}"
        )
    train_total = sum(train_counts.values())
    majority_model = models.fit_majority_class_baseline(train_counts, train_total)
    majority_label = majority_model.majority_label()

    # --- Eval pass: all three baselines on train/validation/holdout ---
    reg = EvalRegistry()
    reg.train_class_counts = train_counts
    n_eval = 0
    for i, ref in enumerate(refs):
        if ref.split == split_policy.EMBARGO:
            continue
        batch = _read_kept_batch(ref, std)
        if batch is None or batch.y.size == 0:
            continue
        split = ref.split
        month = ref.date[:7]
        maj_pred = majority_model.predict_batch(batch.x_std)
        per_pred = models.PersistenceBaseline.predict_from_signs(batch.persistence_sign)
        lin_pred = linear_model.predict_batch(batch.x_std)
        for family, pred in (
            (FAMILY_MAJORITY, maj_pred),
            (FAMILY_PERSISTENCE, per_pred),
            (FAMILY_LINEAR, lin_pred),
        ):
            reg.update(
                family=family, split=split, month=month, date=ref.date,
                y_true=batch.y, pred_class=pred.predicted_class,
                pred_proba=pred.predicted_proba,
            )
        reg.update_calibration(split, lin_pred.predicted_proba, lin_pred.predicted_class, batch.y)
        reg.update_cost(split, month, batch.forward_log_return)
        n_eval += int(batch.y.size)
        if progress and (i + 1) % 25 == 0:
            ah.assert_budget_during()
            print(f"[eval] {i + 1}/275 (rows evaluated {n_eval:,})", flush=True)

    elapsed = time.monotonic() - t0
    payloads = _assemble_payloads(
        art=art, binding=binding, reg=reg, linear_model=linear_model,
        majority_label=majority_label, split_commit=split_commit,
        preflight=preflight, refs=refs, n_train=n_train_processed, n_eval=n_eval,
        elapsed=elapsed,
    )

    # --- Write artefacts (only inside the AJ namespace) ---
    ah.assert_budget_during()
    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    for name, payload in payloads.items():
        digest, _ = ah.write_json_with_sidecar(out_dir / name, payload)
        written[name] = digest

    summary = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "output_namespace": output_namespace + "/",
        "verdict": payloads["verdict.json"]["verdict"],
        "n_train_rows_fit": n_train_processed,
        "n_rows_evaluated": n_eval,
        "elapsed_seconds": round(elapsed, 1),
        "artefacts": written,
        "majority_label": int(majority_label),
    }
    if progress:
        print(f"[done] {json.dumps(summary, indent=2)}", flush=True)
    return summary


def _assemble_payloads(**kw: Any) -> dict[str, dict[str, Any]]:
    art: AhArtefacts = kw["art"]
    binding = kw["binding"]
    reg: EvalRegistry = kw["reg"]
    linear_model = kw["linear_model"]
    preflight = kw["preflight"]

    # Aggregate metrics per family × split.
    aggregate: dict[str, Any] = {}
    for (family, split), ev in reg.agg.items():
        aggregate.setdefault(family, {})[split] = _enrich_metrics(ev)

    # Month/date block metrics (compact: family × split × block).
    month_block: dict[str, Any] = {}
    for (family, split, month), ev in reg.by_month.items():
        month_block.setdefault(family, {}).setdefault(split, {})[month] = {
            "n_rows": ev.n_rows, "accuracy": ev.accuracy(),
            "balanced_accuracy": ev.balanced_accuracy(), "macro_f1": ev.macro_f1(),
        }
    date_block: dict[str, Any] = {}
    for (family, split, date), ev in reg.by_date.items():
        date_block.setdefault(family, {}).setdefault(split, {})[date] = {
            "n_rows": ev.n_rows, "accuracy": ev.accuracy(),
            "balanced_accuracy": ev.balanced_accuracy(), "macro_f1": ev.macro_f1(),
        }

    # Calibration (linear) per split + high-confidence tail (>= 0.8).
    calibration: dict[str, Any] = {}
    hc_tail_beats_majority: dict[str, bool] = {}
    for split, cs in reg.calib.items():
        cd = cs.as_dict()
        bins = cast(list[dict[str, Any]], cd["bins"])
        maj_acc = reg.agg[(FAMILY_MAJORITY, split)].accuracy()
        hc = contract.HIGH_CONFIDENCE_THRESHOLD
        tail_n = sum(b["n_rows"] for b in bins if b["bin_low"] >= hc)
        tail_correct = 0.0
        for b in bins:
            if b["bin_low"] >= hc:
                tail_correct += b["empirical_accuracy"] * b["n_rows"]
        tail_acc = (tail_correct / tail_n) if tail_n else 0.0
        beats = bool(tail_n > 0 and tail_acc > maj_acc)
        cd["high_confidence_tail_size"] = int(tail_n)
        cd["high_confidence_tail_accuracy"] = float(tail_acc)
        cd["majority_accuracy_floor"] = float(maj_acc)
        cd["high_confidence_tail_beats_majority_floor"] = beats
        for b in bins:
            b["beats_majority_floor"] = bool(b["n_rows"] > 0 and b["empirical_accuracy"] > maj_acc)
        calibration[split] = cd
        hc_tail_beats_majority[split] = beats

    # Cost realism per split + per month.
    cost = {
        "by_split": {sp: cr.as_dict() for sp, cr in reg.cost_split.items()},
        "by_split_month": {
            f"{sp}|{mo}": cr.as_dict() for (sp, mo), cr in reg.cost_month.items()
        },
    }

    # Generalization deltas (train↔val, val↔holdout) for the linear model.
    def _m(split: str) -> dict[str, Any]:
        return cast("dict[str, Any]", aggregate[FAMILY_LINEAR][split])
    stability = {
        "train_validation": metrics.summarize_train_validation_stability(
            train_metrics=_m("train"), validation_metrics=_m("validation")
        ),
        "validation_holdout": metrics.summarize_train_validation_stability(
            train_metrics=_m("validation"), validation_metrics=_m("holdout")
        ),
    }

    # --- Verdict inputs (validation primary; holdout corroboration) ---
    val_lin = aggregate[FAMILY_LINEAR]["validation"]
    val_maj = aggregate[FAMILY_MAJORITY]["validation"]
    val_per = aggregate[FAMILY_PERSISTENCE]["validation"]
    hol_lin = aggregate[FAMILY_LINEAR]["holdout"]
    hol_maj = aggregate[FAMILY_MAJORITY]["holdout"]
    calibration_usable = bool(hc_tail_beats_majority.get("validation", False))
    date_agree = _block_agreement(reg, "validation", "date")
    month_agree = _block_agreement(reg, "validation", "month")
    val_cost = reg.cost_split["validation"].as_dict()
    cost_share_16 = val_cost["share_abs_return_gt_16bps_round_trip"]

    vinputs = VerdictInputs(
        val_acc_linear=val_lin["accuracy"],
        val_acc_majority=val_maj["accuracy"],
        val_acc_persistence=val_per["accuracy"],
        val_balacc_linear=val_lin["balanced_accuracy"],
        val_balacc_majority=val_maj["balanced_accuracy"],
        val_macro_f1_linear=val_lin["macro_f1"],
        val_macro_f1_majority=val_maj["macro_f1"],
        holdout_acc_uplift_vs_majority=hol_lin["accuracy"] - hol_maj["accuracy"],
        holdout_macro_f1_uplift_vs_majority=hol_lin["macro_f1"] - hol_maj["macro_f1"],
        val_date_block_agreement=date_agree,
        val_month_block_agreement=month_agree,
        calibration_usable=calibration_usable,
        high_conf_tail_beats_majority=calibration_usable,
        cost_share_gt_16bps=float(cost_share_16),
    )
    verdict = compute_verdict(vinputs)
    verdict["claim_scope_allowed"] = list(contract.CLAIM_SCOPE_ALLOWED)
    verdict["claim_scope_forbidden"] = list(contract.CLAIM_SCOPE_FORBIDDEN)
    verdict["dependence_caveat"] = art.manifest["dependence_caveat"]
    verdict["horizon"] = HORIZON_LABEL
    verdict["primary_target"] = contract.PRIMARY_TARGET
    verdict["successor_authorized"] = False

    baseline_settings = design.BaselineSettingsSnapshot().as_dict()
    run_manifest = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "contract_name": contract.CONTRACT_NAME,
        "amendment_id": contract.CONTRACT_AMENDMENT_ID,
        "primary_target": contract.PRIMARY_TARGET,
        "primary_horizon_ms": contract.PRIMARY_HORIZON_MS,
        "target_classes": list(contract.TARGET_CLASSES),
        "baseline_families_run": list(FAMILIES),
        "linear_baseline_family": FAMILY_LINEAR,
        "persistence_feature": PERSISTENCE_FEATURE,
        "majority_label": int(kw["majority_label"]),
        "baseline_settings": baseline_settings,
        "linear_train_n_batches": int(linear_model.train_n_batches),
        "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": ah.feature_list_hash(),
        "ah_artefact_sha256": art.sha256,
        "source_bindings": {
            "normalized_manifest_sha256": binding.normalized_manifest_sha256,
            "feature_manifest_sha256": binding.feature_manifest_sha256,
            "label_manifest_sha256": binding.label_manifest_sha256,
            "feature_config_hash": binding.feature_config_hash,
            "label_config_hash": binding.label_config_hash,
            "normalized_gate_report_sha256": binding.normalized_gate_report_sha256,
            "feature_gate_report_sha256": binding.feature_gate_report_sha256,
            "label_gate_report_sha256": binding.label_gate_report_sha256,
        },
        "split_policy_name": split_policy.SPLIT_POLICY_NAME,
        "split_policy_commit_sha": kw["split_commit"],
        "mandatory_metrics": list(contract.MANDATORY_METRICS),
        "metric_granularities": list(contract.METRIC_GRANULARITIES),
        "decision_block_units": list(contract.DECISION_BLOCK_UNITS),
        "row_level_metrics_descriptive_only": contract.ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY,
        "n_train_rows_fit": int(kw["n_train"]),
        "n_rows_evaluated": int(kw["n_eval"]),
        "elapsed_seconds": round(float(kw["elapsed"]), 1),
        "budget_preflight": {
            "passed": preflight.passed, "d_free_gib_before": preflight.d_free_gib_before,
            "is_placeholder": preflight.is_placeholder, "ran_preflight": preflight.ran_preflight,
        },
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "test_rows_loaded": 0,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "verdict": verdict["verdict"],
    }

    proof_payload = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "contract_name": contract.CONTRACT_NAME,
        "reads_ah_namespace_readonly": True,
        "ah_namespace_mutated": False,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "embargo_rows_used": 0,
        "targets_imputed": False,
        "fit_split": "train",
        "fit_on_validation_or_holdout": False,
        "no_random": True, "no_shuffle_across_partitions": True,
        "no_kfold": True, "no_bootstrap": True,
        "no_model_selection": True, "no_hyperparameter_search": True,
        "no_threshold_optimization": True, "no_feature_selection": True,
        "models_run_once_each": True,
        "persisted_model_binaries": False,
        "persisted_row_level_predictions": False,
        "ran_strategy": False, "generated_signals": False,
        "simulated_pnl": False, "ran_backtests": False,
        "computed_sharpe_or_trading_hitrate": False,
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "claim_scope_allowed": list(contract.CLAIM_SCOPE_ALLOWED),
        "claim_scope_forbidden": list(contract.CLAIM_SCOPE_FORBIDDEN),
        "output_namespace_path": OUTPUT_NAMESPACE + "/",
        "authorized_successor_phase": False,
    }

    return {
        "baseline_run_manifest.json": run_manifest,
        "aggregate_metrics.json": {"horizon": HORIZON_LABEL, "by_family_split": aggregate},
        "month_block_metrics.json": {
            "horizon": HORIZON_LABEL, "by_family_split_month": month_block,
        },
        "date_block_metrics.json": {
            "horizon": HORIZON_LABEL, "by_family_split_date": date_block,
        },
        "calibration_summary.json": {"horizon": HORIZON_LABEL, "linear_by_split": calibration},
        "cost_realism.json": cost,
        "generalization_deltas.json": {"linear": stability},
        "verdict.json": verdict,
        "baseline_run_proof.json": proof_payload,
    }


def main() -> None:  # pragma: no cover - CLI entry
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":  # pragma: no cover
    main()


__all__ = [
    "AhArtefacts",
    "BASELINE_VERSION",
    "CostRealism",
    "EvalRegistry",
    "FAMILIES",
    "OUTPUT_NAMESPACE",
    "PERSISTENCE_FEATURE",
    "PreV002FixedBaselineError",
    "RUN_PHASE",
    "TrainOnlyStandardizer",
    "VERDICT_CONTINUE",
    "VERDICT_INVESTIGATE",
    "VERDICT_KILL",
    "VerdictInputs",
    "build_standardizer",
    "compute_verdict",
    "load_and_verify_ah_artefacts",
    "main",
    "run",
]
