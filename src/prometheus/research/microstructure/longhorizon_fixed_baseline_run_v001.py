"""Phase 4bn-AR — fixed long-horizon baseline run + pre-registered verdict.

The **fixed run-once baseline** slot (phase 2) of the Phase 4bn-AP long-horizon
ML-arc plan, executed over the verified Phase 4bn-AQ long-horizon dataset
specification. It trains the three frozen baseline families once each, per
authorized horizon, and records exactly one Phase 4bn-AP §25 verdict under the
frozen Phase 4bn-AE §16 thresholds. **No model / feature / hyperparameter /
threshold search.**

Targets (Phase 4bn-AP §17/§24): primary decision target ``forward_direction_5m``;
secondary diagnostics ``forward_direction_30m`` / ``forward_direction_1h`` (reported,
never able to upgrade a failed 5m to continuation).

Baselines (Phase 4bn-AP §21, implementations reused verbatim from the committed
Phase 4bn-B ``ml_baseline_models_v002`` pure-numpy suite):

1. **majority** — the modal ``train`` class, determined separately per horizon from
   that horizon's valid train targets only, frozen for validation / holdout.
2. **persistence** — ``sign(rolling_log_return_past_window_60s)`` (Phase 4bn-AP §22;
   the longest available past-window return feature; the SAME signal for all three
   long horizons — no horizon-matched 5m/30m/1h feature is created).
3. **L2 multinomial-logistic** — one independent 3-class softmax model per horizon,
   fit once by mini-batch SGD with the **frozen** Phase 4bn-B/AJ constants
   (1 epoch, batch 8192, lr 0.1, L2 1e-4, grad-clip 10, seed 20260528). Each trainer
   owns its RNG, so reading each partition once and dispatching to the three trainers
   is exactly equivalent to three independent chronological passes.

Data path (read-only / streamed / bounded-memory):

- verifies the seven Phase 4bn-AQ artefacts + fourteen Phase 4bb-F sidecars, the
  dataset-contract-hash agreement, the feature / label source bindings, the split
  identity and per-horizon support counts, and the leakage-proof flags;
- **applies** the AQ-fitted ``train_only_transform.json`` statistics (never refits —
  nothing is fit on validation / holdout);
- reads only the AQ-bound admitted pre-v002 45-feature + long-horizon label Parquet
  (275 partitions; embargo excluded from all fitting and scoring), verifying every
  per-parquet ``.sha256`` and strict per-row alignment in streaming batches;
- fits the three L2 models on ``train`` only; scores all three baselines on
  ``validation`` (primary decision evidence) and ``holdout`` (no-reversal
  confirmation) per horizon;
- computes the frozen aggregate / date-block / month-block / calibration /
  >= 0.8 confidence-tail diagnostics and records exactly one verdict;
- writes compact JSON artefacts + Phase 4bb-F sidecars to the single local
  **gitignored** namespace only. No row-level predictions; no model binaries.

Hard boundaries (fail-closed): never reads the v002 terminal window or the sealed
test (``test_rows_loaded = 0``); mutates no AH / AJ / AN / AQ namespace; reruns no
builder; imputes no target; runs no strategy / signals / PnL / backtest; ranks no
features; selects no model; tunes no threshold; flips no eligibility; authorizes no
successor. A favourable result is an information diagnostic only (Phase 4bn-AE
§8/§19) — no result licenses a tradability / economic claim.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, cast

import numpy as np
import numpy.typing as npt
import pyarrow.compute as pc
import pyarrow.parquet as pq

from . import build_longhorizon_ml_dataset_v001 as aq
from . import longhorizon_baseline_verdict_v001 as verdict_mod
from . import longhorizon_ml_dataset_contract_v001 as contract
from . import ml_baseline_design_v002 as design
from . import ml_baseline_metrics_v002 as metrics
from . import ml_baseline_models_v002 as models
from . import pre_v002_ml_dataset_contract as ae
from . import pre_v002_split_policy as split_policy

# ---------------------------------------------------------------------------
# Identity / paths
# ---------------------------------------------------------------------------

RUN_PHASE = "phase-4bn-ar"
BASELINE_VERSION = "longhorizon_pre_v001_fixed_run"

REPO_ROOT = aq.REPO_ROOT
AQ_NAMESPACE = contract.OUTPUT_NAMESPACE
OUTPUT_NAMESPACE = (
    "data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run"
)

# Persistence baseline signal (Phase 4bn-AP §22): the longest available past-window
# log-return feature — the SAME feature for all three long horizons (no new feature).
PERSISTENCE_FEATURE = "rolling_log_return_past_window_60s"

PRIMARY_HORIZON = contract.PRIMARY_HORIZON            # "5m"
SECONDARY_HORIZONS = contract.SECONDARY_HORIZONS      # ("30m", "1h")
HORIZONS = contract.HORIZONS                          # ("5m", "30m", "1h")

FAMILY_MAJORITY = design.BASELINE_MAJORITY_CLASS
FAMILY_PERSISTENCE = design.BASELINE_PERSISTENCE_PAST_RETURN
FAMILY_LINEAR = design.BASELINE_LOGISTIC_REGRESSION_L2
FAMILIES: tuple[str, str, str] = (FAMILY_MAJORITY, FAMILY_PERSISTENCE, FAMILY_LINEAR)

# Binding constants re-verified against the AQ artefacts (fail closed on drift).
EXPECTED_DATASET_CONTRACT_HASH = (
    "a310eabf7854ae13ffed1baa2d57a8cf557a3d90dec24337a61e4ca26a9c3873"
)
EXPECTED_FEATURE_LIST_HASH = (
    "8e705ba8800421ae0ccc55cdbf115a36dce9f27f8682e552e2b59c4ab83df7b9"
)
EXPECTED_LABEL_CONFIG_HASH = contract.LABEL_CONFIG_HASH
EXPECTED_AN_LABEL_MANIFEST_SHA256 = (
    "b1ee9afd8dadc410216516f6fa291aa49a26ba788480eb7d98126fc45919f4c0"
)

# Per-horizon valid-target support (from the verified AQ manifest).
EXPECTED_SUPPORT: dict[str, dict[str, int]] = {
    "train": {"5m": 304_816_127, "30m": 304_816_127, "1h": 304_816_127},
    "validation": {"5m": 68_578_296, "30m": 68_578_296, "1h": 68_578_296},
    "holdout": {"5m": 23_534_374, "30m": 23_525_986, "1h": 23_512_252},
}

_AQ_ARTEFACTS = (
    "dataset_manifest.json",
    "split_index.json",
    "train_only_transform.json",
    "leakage_split_integrity_proof.json",
    "source_binding.json",
    "sidecar_inventory.json",
    "build_run_record.json",
)

HIGH_CONFIDENCE_THRESHOLD = ae.HIGH_CONFIDENCE_THRESHOLD  # 0.8

# The admitted pre-v002 segment has exactly 275 daily partitions (fail closed on
# drift). Exposed as a module constant only so the offline test suite can exercise
# the full orchestration on a small synthetic fixture.
EXPECTED_PARTITION_COUNT = 275


class LongHorizonFixedBaselineError(RuntimeError):
    """Raised when a Phase 4bn-AR fixed-baseline invariant fails closed."""


# ---------------------------------------------------------------------------
# AQ artefact loading + re-verification (read-only; never mutates AQ)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AqArtefacts:
    """The seven re-verified Phase 4bn-AQ dataset-spec artefacts (read-only)."""

    manifest: dict[str, Any]
    split_index: dict[str, Any]
    transform: dict[str, Any]
    proof: dict[str, Any]
    source_binding: dict[str, Any]
    sidecar_inventory: dict[str, Any]
    build_run_record: dict[str, Any]
    sha256: dict[str, str]


def load_and_verify_aq_artefacts(namespace: str = AQ_NAMESPACE) -> AqArtefacts:
    """Load the seven AQ artefacts read-only, re-verifying sidecars + invariants.

    Fails closed (:class:`LongHorizonFixedBaselineError`) on any sidecar mismatch,
    dataset-contract-hash disagreement, feature/label binding drift, split-count or
    per-horizon-support drift, or leakage-flag regression. Reads only; mutates
    nothing.
    """
    base = REPO_ROOT / namespace
    loaded: dict[str, dict[str, Any]] = {}
    shas: dict[str, str] = {}
    for name in _AQ_ARTEFACTS:
        path = base / name
        if not path.is_file():
            raise LongHorizonFixedBaselineError(f"missing AQ artefact {path}")
        sidecar = path.with_name(name + ".sha256")
        if not sidecar.is_file():
            raise LongHorizonFixedBaselineError(f"missing AQ sidecar {sidecar}")
        digest = aq.sha256_file(path)
        side_sha, side_name = aq.parse_sidecar(sidecar.read_text(encoding="utf-8"))
        if side_name != name:
            raise LongHorizonFixedBaselineError(
                f"AQ sidecar name {side_name!r} != {name!r}"
            )
        if side_sha != digest:
            raise LongHorizonFixedBaselineError(
                f"AQ artefact {name} sha {digest[:12]}… != sidecar {side_sha[:12]}…"
            )
        loaded[name] = json.loads(path.read_text(encoding="utf-8"))
        shas[name] = digest

    art = AqArtefacts(
        manifest=loaded["dataset_manifest.json"],
        split_index=loaded["split_index.json"],
        transform=loaded["train_only_transform.json"],
        proof=loaded["leakage_split_integrity_proof.json"],
        source_binding=loaded["source_binding.json"],
        sidecar_inventory=loaded["sidecar_inventory.json"],
        build_run_record=loaded["build_run_record.json"],
        sha256=shas,
    )
    _assert_aq_invariants(art)
    return art


def _assert_aq_invariants(art: AqArtefacts) -> None:
    """Fail closed unless the AQ artefacts encode the expected bound state."""
    man, proof, tr, sb = art.manifest, art.proof, art.transform, art.source_binding

    # Dataset-contract-hash agreement across manifest / source-binding / proof.
    for payload, name in ((man, "manifest"), (sb, "source_binding"), (proof, "proof")):
        if payload.get("dataset_contract_hash") != EXPECTED_DATASET_CONTRACT_HASH:
            raise LongHorizonFixedBaselineError(
                f"AQ {name} dataset_contract_hash mismatch"
            )

    # Feature source binding.
    if int(man.get("feature_count", -1)) != 45:
        raise LongHorizonFixedBaselineError("AQ manifest feature_count != 45")
    if len(man.get("feature_list", [])) != 45:
        raise LongHorizonFixedBaselineError("AQ manifest feature_list length != 45")
    if man.get("feature_list_hash") != EXPECTED_FEATURE_LIST_HASH:
        raise LongHorizonFixedBaselineError("AQ manifest feature_list_hash mismatch")
    if tr.get("feature_list_hash") != EXPECTED_FEATURE_LIST_HASH:
        raise LongHorizonFixedBaselineError("AQ transform feature_list_hash mismatch")
    if tuple(man.get("feature_list", [])) != tuple(contract.ALLOWED_FEATURE_COLUMNS):
        raise LongHorizonFixedBaselineError("AQ feature_list != contract allowlist")

    # Label source binding.
    fs = man.get("source_bindings", {})
    if fs.get("label_family") != contract.LABEL_FAMILY:
        raise LongHorizonFixedBaselineError("AQ manifest label_family mismatch")
    if fs.get("label_config_hash") != EXPECTED_LABEL_CONFIG_HASH:
        raise LongHorizonFixedBaselineError("AQ manifest label_config_hash mismatch")
    if fs.get("label_manifest_sha256") != EXPECTED_AN_LABEL_MANIFEST_SHA256:
        raise LongHorizonFixedBaselineError("AQ manifest AN label_manifest_sha256 mismatch")

    # Split identity + counts.
    sr = man.get("split_raw_rows", {})
    expected_raw = {
        "train": 304_816_127, "embargo": 3_071_370,
        "validation": 68_578_296, "holdout": 23_535_902,
    }
    for k, v in expected_raw.items():
        if int(sr.get(k, -1)) != v:
            raise LongHorizonFixedBaselineError(f"AQ split_raw_rows[{k}] mismatch")
    if int(man.get("streamed_row_count", -1)) != contract.EXPECTED_ROW_COUNT:
        raise LongHorizonFixedBaselineError("AQ streamed_row_count mismatch")
    per_date = art.split_index.get("per_date", [])
    if len(per_date) != 275:
        raise LongHorizonFixedBaselineError("AQ split_index per_date != 275")
    date_split_counts: dict[str, int] = {}
    for entry in per_date:
        date_split_counts[str(entry.get("split"))] = (
            date_split_counts.get(str(entry.get("split")), 0) + 1
        )
    expected_date_counts = {"train": 214, "embargo": 2, "validation": 45, "holdout": 14}
    for k, v in expected_date_counts.items():
        if date_split_counts.get(k) != v:
            raise LongHorizonFixedBaselineError(
                f"AQ split_index date count for {k} != {v}"
            )

    # Per-horizon support.
    psh = man.get("per_split_horizon_support", {})
    for sp, hm in EXPECTED_SUPPORT.items():
        for h, want in hm.items():
            got = psh.get(sp, {}).get(h, {}).get("valid_target")
            if int(got if got is not None else -1) != want:
                raise LongHorizonFixedBaselineError(
                    f"AQ support {sp}/{h} valid_target {got} != {want}"
                )

    # Leakage / scope flags.
    if proof.get("alignment_mismatches") != 0:
        raise LongHorizonFixedBaselineError("AQ proof alignment_mismatches != 0")
    bc = proof.get("per_horizon_boundary_crossing_rows", {})
    if not bc or any(int(v) != 0 for v in bc.values()):
        raise LongHorizonFixedBaselineError("AQ proof boundary crossings != 0")
    for flag in ("v002_terminal_window_read", "sealed_test_split_touched"):
        if proof.get(flag) is not False or man.get(flag) is not False:
            raise LongHorizonFixedBaselineError(f"AQ {flag} != false")
    if int(proof.get("test_rows_loaded", -1)) != 0 or int(man.get("test_rows_loaded", -1)) != 0:
        raise LongHorizonFixedBaselineError("AQ test_rows_loaded != 0")
    if proof.get("data_committed") is not False:
        raise LongHorizonFixedBaselineError("AQ proof data_committed != false")
    naf = man.get("non_authorization_flags", {})
    if not naf or any(v is not False for v in naf.values()):
        raise LongHorizonFixedBaselineError("AQ non_authorization_flags not all false")

    # Transform binding.
    if tr.get("fit_split") != "train":
        raise LongHorizonFixedBaselineError("AQ transform fit_split != train")
    if tr.get("standardization_rule") != contract.STANDARDIZATION_RULE:
        raise LongHorizonFixedBaselineError("AQ transform standardization_rule mismatch")
    if int(tr.get("train_primary_valid_rows", -1)) != 304_816_127:
        raise LongHorizonFixedBaselineError("AQ transform train_primary_valid_rows mismatch")
    if len(tr.get("per_feature", {})) != 45:
        raise LongHorizonFixedBaselineError("AQ transform per_feature count != 45")


# ---------------------------------------------------------------------------
# Train-only standardizer (APPLIES the AQ transform; never refits)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrainOnlyStandardizer:
    """Apply the AQ-fitted train-only transform to a feature matrix.

    Replicates the committed Phase 4bn-AJ ``fixed_zero_for_null_numeric`` model-matrix
    convention verbatim: null / non-finite numeric cells are imputed to the fixed
    ``IMPUTATION_FILL_VALUE`` (0.0) before standardization; boolean flag columns
    (``STANDARDIZE_BOOLEAN_FLAGS = False``) pass through their imputed 0/1 value; the
    denominator is ``max(train_std, epsilon)``. Statistics are never recomputed.
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
        if x_raw.shape[1] != len(self.columns):
            raise LongHorizonFixedBaselineError(
                f"feature width {x_raw.shape[1]} != {len(self.columns)}"
            )
        x = np.where(np.isfinite(x_raw), x_raw, self.fill_value).astype(
            np.float64, copy=False
        )
        denom = np.maximum(self.std, self.epsilon)
        standardized: npt.NDArray[Any] = (x - self.mean) / denom
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
        epsilon=float(
            transform.get("standardization_epsilon", contract.STANDARDIZATION_EPSILON)
        ),
        fill_value=float(
            transform.get("imputation_fill_value", contract.IMPUTATION_FILL_VALUE)
        ),
    )


# ---------------------------------------------------------------------------
# Streaming partition read (reuses the AQ verified read path + per-horizon filter)
# ---------------------------------------------------------------------------

_ALIGNMENT_KEYS = list(contract.ALIGNMENT_KEYS)
_FEATURE_KEY_COLS = [*_ALIGNMENT_KEYS, "utc_date"]
_LABEL_READ_COLS = [
    *_ALIGNMENT_KEYS,
    "utc_date",
    contract.LABEL_INVALID_PRICE_FLAG,
    *[contract.DIRECTION_COLUMN_BY_HORIZON[h] for h in HORIZONS],
    *[contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h] for h in HORIZONS],
]


@dataclass
class _KeptHorizon:
    """One horizon's model-eligible rows in a partition."""

    keep_idx: npt.NDArray[Any]  # positions kept for this horizon
    y: npt.NDArray[Any]         # int8 {-1,0,1} for the kept rows


@dataclass
class _PartitionBatch:
    """Standardized features + per-horizon kept targets for one partition."""

    x_std: npt.NDArray[Any]              # (n, 45) standardized
    persistence_sign: npt.NDArray[Any]  # (n,) int8 {-1,0,1}
    by_horizon: dict[str, _KeptHorizon]
    n_rows: int


def _read_partition(ref: aq.PartitionRef, std: TrainOnlyStandardizer) -> _PartitionBatch | None:
    """Read one model-eligible partition, standardize, and per-horizon filter.

    Returns ``None`` for embargo dates (dropped in full). Applies the exact AQ
    per-horizon drop precedence (invalid → censored → null_direction); never imputes
    a target.
    """
    if ref.split == split_policy.EMBARGO:
        return None
    ltab = pq.read_table(ref.label_parquet, columns=_LABEL_READ_COLS)
    ftab = pq.read_table(
        ref.feature_parquet,
        columns=[*_FEATURE_KEY_COLS, *contract.ALLOWED_FEATURE_COLUMNS],
    )
    n = aq._check_alignment_vectorized(ftab, ltab, ref.date)

    invalid = np.asarray(
        ltab.column(contract.LABEL_INVALID_PRICE_FLAG).to_numpy(zero_copy_only=False)
    ).astype(bool)

    x_raw = np.empty((n, len(std.columns)), dtype=np.float64)
    for j, col in enumerate(std.columns):
        x_raw[:, j] = aq._col_to_float64(ftab, col)
    x_std = std.transform(x_raw)

    past = x_raw[:, std.persistence_index]
    past = np.where(np.isfinite(past), past, std.fill_value)
    persistence_sign = np.sign(past).astype(np.int8)

    by_horizon: dict[str, _KeptHorizon] = {}
    for h in HORIZONS:
        dir_col = ltab.column(contract.DIRECTION_COLUMN_BY_HORIZON[h])
        dir_null = np.asarray(dir_col.is_null().to_numpy(zero_copy_only=False))
        dir_filled = np.asarray(pc.fill_null(dir_col, -2).to_numpy(zero_copy_only=False))
        censored = np.asarray(
            ltab.column(contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h]).to_numpy(
                zero_copy_only=False
            )
        ).astype(bool)
        drop_invalid = invalid
        drop_censored = censored & ~drop_invalid
        drop_null_dir = dir_null & ~drop_invalid & ~drop_censored
        keep = ~(drop_invalid | drop_censored | drop_null_dir)
        keep_idx = np.nonzero(keep)[0]
        # Kept rows exclude null directions, so the filled sentinel (-2) never
        # survives; kept targets are strictly in {-1, 0, +1}.
        y = dir_filled[keep_idx].astype(np.int8)
        by_horizon[h] = _KeptHorizon(keep_idx=keep_idx, y=y)

    return _PartitionBatch(
        x_std=x_std,
        persistence_sign=persistence_sign,
        by_horizon=by_horizon,
        n_rows=n,
    )


# ---------------------------------------------------------------------------
# Per-horizon evaluator registry
# ---------------------------------------------------------------------------


@dataclass
class EvalRegistry:
    """Holds per-(horizon, family, split, block) evaluators + L2 calibration."""

    agg: dict[tuple[str, str, str], models.StreamingEvaluator] = field(default_factory=dict)
    by_month: dict[tuple[str, str, str, str], models.StreamingEvaluator] = field(
        default_factory=dict
    )
    by_date: dict[tuple[str, str, str, str], models.StreamingEvaluator] = field(
        default_factory=dict
    )
    calib: dict[tuple[str, str], metrics.CalibrationSummary] = field(default_factory=dict)

    def _ev(
        self,
        store: dict[Any, models.StreamingEvaluator],
        key: tuple[Any, ...],
        horizon: str,
        family: str,
        split: str,
    ) -> models.StreamingEvaluator:
        ev = store.get(key)
        if ev is None:
            ev = models.StreamingEvaluator(family=family, split=split, horizon=horizon)
            store[key] = ev
        return ev

    def update(
        self,
        *,
        horizon: str,
        family: str,
        split: str,
        month: str,
        date: str,
        y_true: npt.NDArray[Any],
        pred_class: npt.NDArray[Any],
        pred_proba: npt.NDArray[Any],
    ) -> None:
        targets: tuple[tuple[dict[Any, models.StreamingEvaluator], tuple[Any, ...]], ...] = (
            (self.agg, (horizon, family, split)),
            (self.by_month, (horizon, family, split, month)),
            (self.by_date, (horizon, family, split, date)),
        )
        for store, key in targets:
            self._ev(store, key, horizon, family, split).update(
                y_true=y_true,
                predicted_class=pred_class,
                predicted_proba=pred_proba,
                forward_log_returns=None,
            )

    def update_calibration(
        self,
        horizon: str,
        split: str,
        pred_proba: npt.NDArray[Any],
        pred_class: npt.NDArray[Any],
        y_true: npt.NDArray[Any],
    ) -> None:
        key = (horizon, split)
        cs = self.calib.get(key)
        if cs is None:
            cs = metrics.CalibrationSummary(
                family=FAMILY_LINEAR, split=split, horizon=horizon
            )
            self.calib[key] = cs
        cs.update(predicted_proba=pred_proba, predicted_class=pred_class, y_true=y_true)


# ---------------------------------------------------------------------------
# Metric enrichment + block helpers
# ---------------------------------------------------------------------------


def _enrich_metrics(ev: models.StreamingEvaluator) -> dict[str, Any]:
    """Return the evaluator metrics + derived distribution / zero-rate fields."""
    d = ev.as_dict()
    conf = ev.confusion
    n = int(conf.sum())
    pred_dist = conf.sum(axis=0)
    true_dist = conf.sum(axis=1)
    names = design.CLASS_LABELS
    d["predicted_class_distribution"] = {
        design.CLASS_DISPLAY_NAMES[names[i]]: int(pred_dist[i]) for i in range(3)
    }
    d["true_class_distribution"] = {
        design.CLASS_DISPLAY_NAMES[names[i]]: int(true_dist[i]) for i in range(3)
    }
    flat_idx = 1
    d["zero_class_prevalence"] = (float(true_dist[flat_idx]) / n) if n else 0.0
    d["predicted_zero_rate"] = (float(pred_dist[flat_idx]) / n) if n else 0.0
    return d


def _block_beats_both(
    reg: EvalRegistry, horizon: str, split: str, by: str
) -> tuple[int, int, dict[str, bool]]:
    """Return ``(block_count, blocks_where_L2_beats_both_floors, per_block)``.

    A block counts only if it has L2, majority, and persistence evaluators with > 0
    rows. "Beats both" means L2 accuracy strictly exceeds BOTH the majority and the
    persistence floor accuracy in that block.
    """
    store = reg.by_month if by == "month" else reg.by_date
    keys = sorted(
        {k[3] for k in store if k[0] == horizon and k[2] == split and k[1] == FAMILY_LINEAR}
    )
    beats = 0
    total = 0
    per_block: dict[str, bool] = {}
    for blk in keys:
        lin = store.get((horizon, FAMILY_LINEAR, split, blk))
        maj = store.get((horizon, FAMILY_MAJORITY, split, blk))
        per = store.get((horizon, FAMILY_PERSISTENCE, split, blk))
        if lin is None or maj is None or per is None or lin.n_rows == 0:
            continue
        total += 1
        won = lin.accuracy() > maj.accuracy() and lin.accuracy() > per.accuracy()
        per_block[blk] = won
        if won:
            beats += 1
    return total, beats, per_block


def _confidence_tail(
    cs: metrics.CalibrationSummary, majority_acc: float
) -> dict[str, Any]:
    """Compute the >= 0.8 confidence-tail summary + ECE for one (horizon, split)."""
    cd = cs.as_dict()
    bins = cast(list[dict[str, Any]], cd["bins"])
    total_n = sum(int(b["n_rows"]) for b in bins)
    tail_n = 0
    tail_correct = 0.0
    ece = 0.0
    for b in bins:
        n_b = int(b["n_rows"])
        if n_b == 0:
            continue
        emp = float(b["empirical_accuracy"])
        mean_p = float(b["mean_max_predicted_proba"])
        ece += (n_b / total_n) * abs(emp - mean_p) if total_n else 0.0
        if float(b["bin_low"]) >= HIGH_CONFIDENCE_THRESHOLD:
            tail_n += n_b
            tail_correct += emp * n_b
    tail_acc = (tail_correct / tail_n) if tail_n else 0.0
    calib_verdict = verdict_mod.classify_calibration(
        tail_n=tail_n, tail_acc=tail_acc, majority_acc=majority_acc, ece=ece
    )
    return {
        "horizon": cs.horizon,
        "split": cs.split,
        "expected_calibration_error": ece,
        "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        "confidence_tail_n": int(tail_n),
        "confidence_tail_fraction": (tail_n / total_n) if total_n else 0.0,
        "confidence_tail_accuracy": float(tail_acc),
        "majority_accuracy_floor": float(majority_acc),
        "confidence_tail_beats_majority_floor": bool(tail_n > 0 and tail_acc > majority_acc),
        "calibration_verdict": calib_verdict,
        "reliability_bins": bins,
    }


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def verify_preflight(*, progress: bool = True) -> dict[str, Any]:
    """Read-only preflight: verify AQ artefacts, bindings, 550 sidecars, budget.

    Reads no feature/label rows and writes nothing. Fails closed on any mismatch.
    Returns a compact summary. Used by the ``--dry-run`` CLI mode before the single
    controlled run.
    """
    d_free_before = aq.measure_d_free_gib()
    preflight = aq.evaluate_budget_preflight(d_free_before)
    if not preflight.passed:
        raise LongHorizonFixedBaselineError(
            f"budget preflight failed closed: {preflight.breaches!r}"
        )
    art = load_and_verify_aq_artefacts()
    build_standardizer(art.transform)
    (_, feat_m_sha, _, _, _, feature_manifest) = aq.verify_feature_source_binding()
    label_manifest, label_manifest_sha = aq.verify_label_source_binding(feat_m_sha)
    if label_manifest_sha != EXPECTED_AN_LABEL_MANIFEST_SHA256:
        raise LongHorizonFixedBaselineError("AN label manifest sha drift vs binding")
    aq.bind_split_authority()
    refs = aq.verify_per_parquet_sidecars_and_inventory(
        feature_manifest, label_manifest, progress=progress
    )
    if len(refs) != EXPECTED_PARTITION_COUNT:
        raise LongHorizonFixedBaselineError(
            f"expected {EXPECTED_PARTITION_COUNT} partitions, got {len(refs)}"
        )
    if aq.dataset_contract_hash() != EXPECTED_DATASET_CONTRACT_HASH:
        raise LongHorizonFixedBaselineError("recomputed dataset_contract_hash mismatch")
    out_exists = (
        (REPO_ROOT / OUTPUT_NAMESPACE / "run_manifest.json").exists()
        or (REPO_ROOT / OUTPUT_NAMESPACE / "verdict.json").exists()
    )
    return {
        "phase": RUN_PHASE,
        "mode": "dry_run",
        "aq_artefacts_verified": len(_AQ_ARTEFACTS),
        "partitions_verified": len(refs),
        "dataset_contract_hash": EXPECTED_DATASET_CONTRACT_HASH,
        "label_manifest_sha256": label_manifest_sha,
        "budget_preflight_passed": preflight.passed,
        "d_free_gib_before": preflight.d_free_gib_before,
        "output_namespace": OUTPUT_NAMESPACE + "/",
        "output_already_exists": out_exists,
    }


def run(*, output_namespace: str = OUTPUT_NAMESPACE, progress: bool = True) -> dict[str, Any]:
    """Execute the single fixed long-horizon baseline run + verdict.

    Fails closed on any pre-run check, alignment, numerical, or output-boundary
    violation. On success writes compact JSON artefacts + Phase 4bb-F sidecars inside
    *output_namespace* only (no model binaries, no row-level predictions).
    """
    t0 = time.monotonic()
    out_dir = REPO_ROOT / output_namespace

    # One-run / no-overwrite guard.
    if (out_dir / "run_manifest.json").exists() or (out_dir / "verdict.json").exists():
        raise LongHorizonFixedBaselineError(
            "AR baseline already run at this namespace; a rerun requires separate "
            "operator authorization (no result-seeking rerun is permitted)"
        )

    # Budget preflight (D: >= 500 GiB before start).
    d_free_before = aq.measure_d_free_gib()
    preflight = aq.evaluate_budget_preflight(d_free_before)
    if not preflight.passed:
        raise LongHorizonFixedBaselineError(
            f"budget preflight failed closed: {preflight.breaches!r}"
        )

    # Pre-run verification (read-only).
    if progress:
        print("[pre-run] verifying 7 AQ artefacts + 14 sidecars…", flush=True)
    art = load_and_verify_aq_artefacts()
    std = build_standardizer(art.transform)

    if progress:
        print("[pre-run] verifying feature + label source bindings…", flush=True)
    (
        norm_m_sha,
        feat_m_sha,
        feat_config_hash,
        norm_g_sha,
        feat_g_sha,
        feature_manifest,
    ) = aq.verify_feature_source_binding()
    label_manifest, label_manifest_sha = aq.verify_label_source_binding(feat_m_sha)
    if label_manifest_sha != EXPECTED_AN_LABEL_MANIFEST_SHA256:
        raise LongHorizonFixedBaselineError("AN label manifest sha drift vs binding")
    split_commit = aq.bind_split_authority()

    if progress:
        print("[pre-run] verifying 550 per-parquet sidecars + cross-binding…", flush=True)
    refs = aq.verify_per_parquet_sidecars_and_inventory(
        feature_manifest, label_manifest, progress=progress
    )
    if len(refs) != EXPECTED_PARTITION_COUNT:
        raise LongHorizonFixedBaselineError(
            f"expected {EXPECTED_PARTITION_COUNT} partitions, got {len(refs)}"
        )

    contract_hash = aq.dataset_contract_hash()
    if contract_hash != EXPECTED_DATASET_CONTRACT_HASH:
        raise LongHorizonFixedBaselineError("recomputed dataset_contract_hash mismatch")

    # --- Fit pass: three independent L2 SGD models on train only ---
    trainers = {
        h: models.build_l2_logistic_regression_trainer(
            len(contract.ALLOWED_FEATURE_COLUMNS)
        )
        for h in HORIZONS
    }
    train_counts: dict[str, dict[int, int]] = {h: {-1: 0, 0: 0, 1: 0} for h in HORIZONS}
    n_train_rows: dict[str, int] = {h: 0 for h in HORIZONS}
    for i, ref in enumerate(refs):
        if ref.split != split_policy.TRAIN:
            continue
        batch = _read_partition(ref, std)
        if batch is None:
            continue
        for h in HORIZONS:
            kh = batch.by_horizon[h]
            if kh.y.size == 0:
                continue
            x_h = batch.x_std[kh.keep_idx]
            for cls in (-1, 0, 1):
                train_counts[h][cls] += int((kh.y == cls).sum())
            trainers[h].partial_fit(x_h, kh.y)
            n_train_rows[h] += int(kh.y.size)
        if progress and (i + 1) % 25 == 0:
            aq.assert_budget_during()
            print(
                f"[fit] {i + 1}/275 (train rows fit 5m={n_train_rows['5m']:,})",
                flush=True,
            )
    linear_models = {h: trainers[h].finalize() for h in HORIZONS}

    # Numerical guard + cross-check re-derived support/class counts vs AQ manifest.
    numerical_guard_ok = True
    for h in HORIZONS:
        if not bool(np.all(np.isfinite(linear_models[h].weights))):
            numerical_guard_ok = False
        if n_train_rows[h] != EXPECTED_SUPPORT["train"][h]:
            raise LongHorizonFixedBaselineError(
                f"re-derived train rows[{h}] {n_train_rows[h]} != AQ "
                f"{EXPECTED_SUPPORT['train'][h]}"
            )
        aq_hclass = art.manifest["per_split_horizon_support"]["train"][h]
        if (
            train_counts[h][-1] != int(aq_hclass["class_-1"])
            or train_counts[h][0] != int(aq_hclass["class_0"])
            or train_counts[h][1] != int(aq_hclass["class_1"])
        ):
            raise LongHorizonFixedBaselineError(
                f"re-derived train class counts[{h}] {train_counts[h]} != AQ manifest"
            )
    if not numerical_guard_ok:
        raise LongHorizonFixedBaselineError(
            "numerical guard failed: non-finite L2 weights (fail-closed, no verdict)"
        )

    majority_models = {
        h: models.fit_majority_class_baseline(train_counts[h], sum(train_counts[h].values()))
        for h in HORIZONS
    }
    majority_labels = {h: int(majority_models[h].majority_label()) for h in HORIZONS}

    # --- Eval pass: score all three baselines on validation + holdout, per horizon ---
    reg = EvalRegistry()
    n_eval_rows: dict[str, int] = {h: 0 for h in HORIZONS}
    for i, ref in enumerate(refs):
        if ref.split not in (split_policy.VALIDATION, split_policy.HOLDOUT):
            continue
        batch = _read_partition(ref, std)
        if batch is None:
            continue
        split = ref.split
        month = ref.date[:7]
        for h in HORIZONS:
            kh = batch.by_horizon[h]
            if kh.y.size == 0:
                continue
            x_h = batch.x_std[kh.keep_idx]
            per_sign_h = batch.persistence_sign[kh.keep_idx]
            maj_pred = majority_models[h].predict_batch(x_h)
            per_pred = models.PersistenceBaseline.predict_from_signs(per_sign_h)
            lin_pred = linear_models[h].predict_batch(x_h)
            for family, pred in (
                (FAMILY_MAJORITY, maj_pred),
                (FAMILY_PERSISTENCE, per_pred),
                (FAMILY_LINEAR, lin_pred),
            ):
                reg.update(
                    horizon=h, family=family, split=split, month=month, date=ref.date,
                    y_true=kh.y, pred_class=pred.predicted_class,
                    pred_proba=pred.predicted_proba,
                )
            reg.update_calibration(
                h, split, lin_pred.predicted_proba, lin_pred.predicted_class, kh.y
            )
            n_eval_rows[h] += int(kh.y.size)
        if progress and (i + 1) % 10 == 0:
            aq.assert_budget_during()
            print(f"[eval] {i + 1}/275 (val+holdout rows 5m={n_eval_rows['5m']:,})", flush=True)

    elapsed = time.monotonic() - t0
    payloads = _assemble_payloads(
        art=art, reg=reg, linear_models=linear_models, majority_labels=majority_labels,
        train_counts=train_counts, n_train_rows=n_train_rows, n_eval_rows=n_eval_rows,
        split_commit=split_commit, preflight=preflight, contract_hash=contract_hash,
        feat_m_sha=feat_m_sha, norm_m_sha=norm_m_sha, feat_g_sha=feat_g_sha,
        norm_g_sha=norm_g_sha, feat_config_hash=feat_config_hash,
        label_manifest_sha=label_manifest_sha, numerical_guard_ok=numerical_guard_ok,
        elapsed=elapsed,
    )

    # --- Write artefacts (only inside the AR namespace) ---
    aq.assert_budget_during()
    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, str] = {}
    ordered = (
        "run_manifest.json", "frozen_config.json", "source_binding.json",
        "model_parameters.json", "aggregate_metrics.json", "per_date_metrics.json",
        "per_month_metrics.json", "calibration_summary.json",
        "confidence_tail_summary.json", "verdict.json", "run_record.json",
    )
    for name in ordered:
        digest, _ = aq.write_json_with_sidecar(out_dir / name, payloads[name])
        written[name] = digest

    inventory = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "output_namespace_rel": output_namespace + "/",
        "artefact_count": len(written),
        "entries": [
            {"artefact": name, "artefact_sha256": digest, "sidecar": f"{name}.sha256"}
            for name, digest in sorted(written.items())
        ],
    }
    inv_digest, _ = aq.write_json_with_sidecar(out_dir / "sidecar_inventory.json", inventory)
    written["sidecar_inventory.json"] = inv_digest

    summary = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "output_namespace": output_namespace + "/",
        "verdict": payloads["verdict.json"]["verdict"],
        "primary_horizon": PRIMARY_HORIZON,
        "n_train_rows_fit": n_train_rows,
        "n_eval_rows": n_eval_rows,
        "majority_labels": majority_labels,
        "elapsed_seconds": round(elapsed, 1),
        "artefacts": written,
    }
    if progress:
        print(f"[done] {json.dumps(summary, indent=2)}", flush=True)
    return summary


def _weights_hash(w: npt.NDArray[Any]) -> str:
    return hashlib.sha256(np.ascontiguousarray(w, dtype=np.float64).tobytes()).hexdigest()


def _assemble_payloads(**kw: Any) -> dict[str, dict[str, Any]]:
    art: AqArtefacts = kw["art"]
    reg: EvalRegistry = kw["reg"]
    linear_models = kw["linear_models"]
    majority_labels: dict[str, int] = kw["majority_labels"]
    train_counts: dict[str, dict[int, int]] = kw["train_counts"]
    preflight = kw["preflight"]
    contract_hash: str = kw["contract_hash"]

    # Aggregate metrics per horizon × family × split.
    aggregate: dict[str, Any] = {}
    for (horizon, family, split), ev in reg.agg.items():
        aggregate.setdefault(horizon, {}).setdefault(family, {})[split] = _enrich_metrics(ev)

    # Date / month block metrics (compact) + block "beats both floors" summaries.
    def _blocks(store_key: str) -> dict[str, Any]:
        store = reg.by_month if store_key == "month" else reg.by_date
        out: dict[str, Any] = {}
        for (horizon, family, split, blk), ev in store.items():
            out.setdefault(horizon, {}).setdefault(family, {}).setdefault(split, {})[blk] = {
                "n_rows": ev.n_rows,
                "accuracy": ev.accuracy(),
                "balanced_accuracy": ev.balanced_accuracy(),
                "macro_f1": ev.macro_f1(),
            }
        return out

    date_block = _blocks("date")
    month_block = _blocks("month")

    block_summary: dict[str, Any] = {}
    for horizon in HORIZONS:
        block_summary[horizon] = {}
        for split in (split_policy.VALIDATION, split_policy.HOLDOUT):
            d_total, d_beats, d_per = _block_beats_both(reg, horizon, split, "date")
            m_total, m_beats, m_per = _block_beats_both(reg, horizon, split, "month")
            block_summary[horizon][split] = {
                "date_block_count": d_total,
                "date_blocks_l2_beats_both": d_beats,
                "date_fraction_beats_both": (d_beats / d_total) if d_total else 0.0,
                "month_block_count": m_total,
                "month_blocks_l2_beats_both": m_beats,
                "month_all_beat_both": bool(m_total > 0 and m_beats == m_total),
                "per_month_beats_both": m_per,
            }

    # Confidence-tail + calibration per horizon × split (L2).
    confidence_tail: dict[str, Any] = {}
    calibration: dict[str, Any] = {}
    for (horizon, split), cs in reg.calib.items():
        maj_acc = aggregate[horizon][FAMILY_MAJORITY][split]["accuracy"]
        tail = _confidence_tail(cs, maj_acc)
        confidence_tail.setdefault(horizon, {})[split] = {
            k: v for k, v in tail.items() if k != "reliability_bins"
        }
        calibration.setdefault(horizon, {})[split] = {
            "horizon": horizon,
            "split": split,
            "calibration_verdict": tail["calibration_verdict"],
            "expected_calibration_error": tail["expected_calibration_error"],
            "reliability_bins": tail["reliability_bins"],
        }

    # --- Build per-horizon evidence for the verdict ---
    def _evidence(horizon: str) -> verdict_mod.HorizonEvidence:
        val_lin = aggregate[horizon][FAMILY_LINEAR]["validation"]
        val_maj = aggregate[horizon][FAMILY_MAJORITY]["validation"]
        val_per = aggregate[horizon][FAMILY_PERSISTENCE]["validation"]
        hol_lin = aggregate[horizon][FAMILY_LINEAR]["holdout"]
        hol_maj = aggregate[horizon][FAMILY_MAJORITY]["holdout"]
        hol_per = aggregate[horizon][FAMILY_PERSISTENCE]["holdout"]
        bs = block_summary[horizon]["validation"]
        ct = confidence_tail[horizon]["validation"]
        return verdict_mod.HorizonEvidence(
            horizon=horizon,
            val_acc_l2=val_lin["accuracy"],
            val_acc_majority=val_maj["accuracy"],
            val_acc_persistence=val_per["accuracy"],
            val_balacc_l2=val_lin["balanced_accuracy"],
            val_balacc_majority=val_maj["balanced_accuracy"],
            val_macro_f1_l2=val_lin["macro_f1"],
            val_macro_f1_majority=val_maj["macro_f1"],
            holdout_acc_l2=hol_lin["accuracy"],
            holdout_acc_majority=hol_maj["accuracy"],
            holdout_acc_persistence=hol_per["accuracy"],
            val_date_block_count=int(bs["date_block_count"]),
            val_date_blocks_beat_both=int(bs["date_blocks_l2_beats_both"]),
            val_month_block_count=int(bs["month_block_count"]),
            val_month_blocks_beat_both=int(bs["month_blocks_l2_beats_both"]),
            conf_tail_n=int(ct["confidence_tail_n"]),
            conf_tail_acc=float(ct["confidence_tail_accuracy"]),
            conf_tail_majority_acc=float(ct["majority_accuracy_floor"]),
            calibration_verdict=str(ct["calibration_verdict"]),
        )

    primary_ev = _evidence(PRIMARY_HORIZON)
    secondary_ev = [_evidence(h) for h in SECONDARY_HORIZONS]
    verdict = verdict_mod.compute_longhorizon_verdict(
        primary=primary_ev, secondaries=secondary_ev
    )
    verdict["primary_target"] = contract.PRIMARY_TARGET
    verdict["secondary_targets"] = list(contract.SECONDARY_TARGETS)
    verdict["claim_scope_allowed"] = list(ae.CLAIM_SCOPE_ALLOWED)
    verdict["claim_scope_forbidden"] = list(ae.CLAIM_SCOPE_FORBIDDEN)
    verdict["dependence_caveat"] = art.manifest["dependence_caveat"]
    verdict["successor_authorized"] = False

    # --- Uplift table (per horizon; validation + holdout) ---
    uplift: dict[str, Any] = {}
    for horizon in HORIZONS:
        row: dict[str, Any] = {}
        for split in (split_policy.VALIDATION, split_policy.HOLDOUT):
            lin = aggregate[horizon][FAMILY_LINEAR][split]
            maj = aggregate[horizon][FAMILY_MAJORITY][split]
            per = aggregate[horizon][FAMILY_PERSISTENCE][split]
            row[split] = {
                "l2_acc_uplift_vs_majority_pp": (lin["accuracy"] - maj["accuracy"]) * 100.0,
                "l2_acc_uplift_vs_persistence_pp": (lin["accuracy"] - per["accuracy"]) * 100.0,
                "l2_balacc_uplift_vs_majority_pp": (
                    lin["balanced_accuracy"] - maj["balanced_accuracy"]
                ) * 100.0,
                "l2_macro_f1_uplift_vs_majority": lin["macro_f1"] - maj["macro_f1"],
            }
        uplift[horizon] = row

    # --- model parameters (per horizon; compact) ---
    model_parameters: dict[str, Any] = {"class_ordering": list(design.CLASS_LABELS)}
    for horizon in HORIZONS:
        m = linear_models[horizon]
        model_parameters[horizon] = {
            "family": m.family,
            "class_ordering": list(design.CLASS_LABELS),
            "n_features": int(m.n_features),
            "weight_matrix": [[float(v) for v in row] for row in m.weights[:-1, :]],
            "intercept_vector": [float(v) for v in m.weights[-1, :]],
            "train_rows_consumed": int(kw["n_train_rows"][horizon]),
            "batches_processed": int(m.train_n_batches),
            "final_parameter_hash": _weights_hash(m.weights),
            "numerical_guard_all_finite": bool(np.all(np.isfinite(m.weights))),
            "majority_label": majority_labels[horizon],
            "train_class_counts": {str(k): v for k, v in train_counts[horizon].items()},
        }

    frozen_config = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "contract_name": contract.CONTRACT_NAME,
        "amendment_id": contract.CONTRACT_AMENDMENT_ID,
        "primary_target": contract.PRIMARY_TARGET,
        "secondary_targets": list(contract.SECONDARY_TARGETS),
        "horizons": list(HORIZONS),
        "target_classes": list(contract.TARGET_CLASSES),
        "class_ordering": list(design.CLASS_LABELS),
        "baseline_families_run": list(FAMILIES),
        "persistence_definition": f"sign({PERSISTENCE_FEATURE})",
        "persistence_feature": PERSISTENCE_FEATURE,
        "frozen_l2_constants": {
            "epochs": design.SGD_EPOCHS,
            "batch_size": design.SGD_BATCH_SIZE,
            "learning_rate": design.SGD_LEARNING_RATE,
            "l2_regularization_strength": design.SGD_L2_REGULARIZATION_STRENGTH,
            "gradient_clip_norm": design.SGD_GRADIENT_CLIP_NORM,
            "rng_seed": design.RNG_SEED,
        },
        "transform": {
            "standardization_rule": contract.STANDARDIZATION_RULE,
            "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
            "standardize_boolean_flags": contract.STANDARDIZE_BOOLEAN_FLAGS,
            "imputation_rule": contract.IMPUTATION_RULE,
            "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
            "fit_split": "train",
            "aq_transform_feature_list_hash": art.transform["feature_list_hash"],
        },
        "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": aq.feature_list_hash(),
        "success_thresholds": {
            "success_accuracy_uplift_pp": ae.SUCCESS_ACCURACY_UPLIFT_PP,
            "success_balanced_accuracy_uplift_pp": ae.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP,
            "success_macro_f1_uplift": ae.SUCCESS_MACRO_F1_UPLIFT,
            "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
        },
        "no_search": {
            "model_search": False, "feature_search": False,
            "hyperparameter_search": False, "threshold_search": False,
            "seed_search": False, "epoch_search": False,
            "cross_validation": False, "calibration_training": False,
        },
    }

    source_binding = {
        "phase": RUN_PHASE,
        "repo_commit_sha": aq._git(["rev-parse", "HEAD"]),
        "branch": aq._git(["rev-parse", "--abbrev-ref", "HEAD"]),
        "ap_preregistration_identity": (
            "LONGHORIZON_ML_DATASET_BUILD_THEN_FIXED_BASELINE_RUN"
        ),
        "aq_dataset_family": contract.DATASET_FAMILY,
        "aq_contract_name": contract.CONTRACT_NAME,
        "aq_dataset_contract_hash": contract_hash,
        "aq_artefact_sha256": art.sha256,
        "feature_source": {
            "feature_manifest_sha256": kw["feat_m_sha"],
            "feature_config_hash": kw["feat_config_hash"],
            "feature_gate_report_sha256": kw["feat_g_sha"],
            "normalized_manifest_sha256": kw["norm_m_sha"],
            "normalized_gate_report_sha256": kw["norm_g_sha"],
            "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
            "feature_list_hash": aq.feature_list_hash(),
        },
        "label_source": {
            "label_family": contract.LABEL_FAMILY,
            "label_config_hash": contract.LABEL_CONFIG_HASH,
            "label_manifest_sha256": kw["label_manifest_sha"],
            "horizons": list(HORIZONS),
            "primary_target": contract.PRIMARY_TARGET,
            "secondary_targets": list(contract.SECONDARY_TARGETS),
        },
        "split_policy_name": contract.SPLIT_POLICY_NAME,
        "split_policy_commit_sha": kw["split_commit"],
        "transform_policy": contract.STANDARDIZATION_RULE,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "data_committed": False,
        "row_level_predictions_written": False,
        "strategy_artifacts_written": False,
        "aq_input_namespace_mutated": False,
        "ah_namespace_mutated": False,
        "aj_namespace_mutated": False,
        "an_namespace_mutated": False,
    }

    run_manifest = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "contract_name": contract.CONTRACT_NAME,
        "primary_target": contract.PRIMARY_TARGET,
        "secondary_targets": list(contract.SECONDARY_TARGETS),
        "baseline_families_run": list(FAMILIES),
        "majority_labels": majority_labels,
        "n_train_rows_fit": kw["n_train_rows"],
        "n_eval_rows": kw["n_eval_rows"],
        "l2_batches_processed": {
            h: int(linear_models[h].train_n_batches) for h in HORIZONS
        },
        "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": aq.feature_list_hash(),
        "dataset_contract_hash": contract_hash,
        "aq_artefact_sha256": art.sha256,
        "split_policy_name": contract.SPLIT_POLICY_NAME,
        "split_policy_commit_sha": kw["split_commit"],
        "numerical_guard_all_finite": bool(kw["numerical_guard_ok"]),
        "elapsed_seconds": round(float(kw["elapsed"]), 1),
        "budget_preflight": {
            "passed": preflight.passed,
            "d_free_gib_before": preflight.d_free_gib_before,
            "is_placeholder": preflight.is_placeholder,
            "ran_preflight": preflight.ran_preflight,
        },
        "uplift_summary": uplift,
        "verdict": verdict["verdict"],
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "test_rows_loaded": 0,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "row_level_predictions_written": False,
        "strategy_artifacts_written": False,
        "data_committed": False,
    }

    run_record = {
        "phase": RUN_PHASE,
        "baseline_version": BASELINE_VERSION,
        "output_namespace_rel": OUTPUT_NAMESPACE + "/",
        "reads_aq_namespace_readonly": True,
        "aq_namespace_mutated": False,
        "reruns_aq_builder": False,
        "reruns_an_builder": False,
        "reruns_ah_builder": False,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "test_rows_loaded": 0,
        "embargo_rows_used": 0,
        "targets_imputed": False,
        "fit_split": "train",
        "fit_on_validation_or_holdout": False,
        "second_full_run": False,
        "no_model_search": True,
        "no_feature_search": True,
        "no_hyperparameter_search": True,
        "no_threshold_search": True,
        "no_seed_search": True,
        "no_cross_validation": True,
        "no_calibration_training": True,
        "models_run_once_each": True,
        "persisted_model_binaries": False,
        "persisted_row_level_predictions": False,
        "ran_strategy": False,
        "generated_signals": False,
        "simulated_pnl": False,
        "ran_backtests": False,
        "computed_sharpe_or_trading_hitrate": False,
        "flip_research_eligible_invoked": False,
        "ml_authorized": False,
        "diagnostics_authorized": False,
        "strategy_authorized": False,
        "signals_authorized": False,
        "pnl_authorized": False,
        "backtest_authorized": False,
        "live_authorized": False,
        "exchange_write_authorized": False,
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "claim_scope_allowed": list(ae.CLAIM_SCOPE_ALLOWED),
        "claim_scope_forbidden": list(ae.CLAIM_SCOPE_FORBIDDEN),
        "authorized_successor_phase": False,
    }

    return {
        "run_manifest.json": run_manifest,
        "frozen_config.json": frozen_config,
        "source_binding.json": source_binding,
        "model_parameters.json": model_parameters,
        "aggregate_metrics.json": {"by_horizon_family_split": aggregate, "uplift": uplift},
        "per_date_metrics.json": {"by_horizon_family_split_date": date_block},
        "per_month_metrics.json": {
            "by_horizon_family_split_month": month_block,
            "block_beats_both_summary": block_summary,
        },
        "calibration_summary.json": {"by_horizon_split": calibration},
        "confidence_tail_summary.json": {"by_horizon_split": confidence_tail},
        "verdict.json": verdict,
        "run_record.json": run_record,
    }


def main() -> None:  # pragma: no cover - CLI entry
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == "__main__":  # pragma: no cover
    main()


__all__ = [
    "AQ_NAMESPACE",
    "AqArtefacts",
    "BASELINE_VERSION",
    "EvalRegistry",
    "FAMILIES",
    "FAMILY_LINEAR",
    "FAMILY_MAJORITY",
    "FAMILY_PERSISTENCE",
    "HORIZONS",
    "LongHorizonFixedBaselineError",
    "OUTPUT_NAMESPACE",
    "PERSISTENCE_FEATURE",
    "PRIMARY_HORIZON",
    "RUN_PHASE",
    "SECONDARY_HORIZONS",
    "TrainOnlyStandardizer",
    "build_standardizer",
    "load_and_verify_aq_artefacts",
    "main",
    "run",
    "verify_preflight",
]
