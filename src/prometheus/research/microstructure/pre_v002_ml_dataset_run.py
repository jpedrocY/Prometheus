"""Phase 4bn-AH — pre-v002 data-reading ML dataset builder (single controlled run).

This is the **data-reading** realisation of the Phase 4bn-AF code-only skeleton.
It reads the locally-gated pre-v002 BTCUSDT aggTrades feature (4bn-S) and label
(4bn-W) segments, verifies every source binding, assembles the leakage-proof
pre-v002 ML dataset **specification** for the
``microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`` contract, and
writes it — with Phase 4bb-F canonical ``.sha256`` sidecars — to the single
authorized local **gitignored** output namespace
``data/research/microstructure/ml_datasets/pre_v002_contract_v001/``.

Design (budget-safe, honest):

The dataset **artefact** is a *compact specification*, not a re-materialisation of
the 45-column model matrix. A full ``400,001,695 × 45`` float64 matrix is
``~144 GiB`` — it would breach the Phase 4bn-L ``125 GiB`` derived-footprint hard
cap and would merely duplicate the already-gated feature Parquet. Instead this
builder streams every partition once (bounded memory) and materialises:

- the **train-only fitted transform statistics** (per-feature train mean / std,
  fit on the ``train`` split only — validation / holdout / embargo excluded);
- a **per-date split / filter index** (split label, raw + filtered row counts,
  drop accounting by reason);
- per-split / per-UTC-month **row and class-distribution** summaries;
- a **machine-checkable leakage / split-integrity proof**;
- a **dataset manifest** binding every source hash, the split policy, the 45-column
  allowlist + its hash, and the all-``False`` non-authorization flags.

Hard boundaries (all enforced, fail-closed): reads **only** the pre-v002
normalized-lineage / feature / label sources bound by the Phase 4bn-AC contract;
never reads the v002 terminal window or the sealed test (``test_rows_loaded = 0``);
imputes no target; fits transforms on ``train`` only; writes **only** inside the
authorized namespace; commits nothing; trains no model; scores nothing; runs no
diagnostics / strategy / PnL / backtest; flips no eligibility; sets no manifest
field; authorizes no successor.

It imports and reuses the Phase 4bn-AF skeleton (``pre_v002_ml_dataset_contract``,
``pre_v002_ml_dataset_builder``, ``pre_v002_ml_dataset_proof``) and the Phase
4bn-AA split artefact (``pre_v002_split_policy``); it never wraps, copies, or
reuses the v002-terminal loader ``ml_baseline_dataset_v002``.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
import subprocess
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from . import pre_v002_ml_dataset_builder as builder
from . import pre_v002_ml_dataset_contract as contract
from . import pre_v002_ml_dataset_proof as proof
from . import pre_v002_split_policy as split_policy
from .pre_v002_ml_dataset_builder import PreV002MlDatasetError

# ---------------------------------------------------------------------------
# Identity / paths
# ---------------------------------------------------------------------------

RUN_PHASE = "phase-4bn-ah"
DATASET_VERSION = "pre_v002_contract_v001"

REPO_ROOT = Path(__file__).resolve().parents[4]

OUTPUT_NAMESPACE = (
    "data/research/microstructure/ml_datasets/pre_v002_contract_v001"
)

_MANIFEST_DIR = "data/microstructure/manifests"
_GATE_DIR = "data/microstructure/gate-reports"

NORMALIZED_MANIFEST_PATH = (
    f"{_MANIFEST_DIR}/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
)
FEATURE_MANIFEST_PATH = (
    f"{_MANIFEST_DIR}/"
    "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json"
)
LABEL_MANIFEST_PATH = (
    f"{_MANIFEST_DIR}/"
    "microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json"
)
NORMALIZED_GATE_PATH = (
    f"{_GATE_DIR}/normalized/microstructure_normalized_aggtrades_v001__v002"
    "_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json"
)
FEATURE_GATE_PATH = (
    f"{_GATE_DIR}/features/microstructure_features_aggtrades_v001__v002"
    "_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json"
)
LABEL_GATE_PATH = (
    f"{_GATE_DIR}/labels/microstructure_labels_aggtrades_v001__v002"
    "_pre_v002_segment_4bn_w__phase-4bn-x__1781897304431__5bcae53ee843.json"
)

GIB = 1024 ** 3

# Budget thresholds (Phase 4bn-L; carried verbatim from the skeleton proof module).
DERIVED_FOOTPRINT_WARN_GIB = proof.DERIVED_FOOTPRINT_WARN_GIB
DERIVED_FOOTPRINT_HARD_GIB = proof.DERIVED_FOOTPRINT_HARD_GIB
TOTAL_DERIVED_STACK_WARN_GIB = proof.TOTAL_DERIVED_STACK_WARN_GIB
TOTAL_DERIVED_STACK_HARD_GIB = proof.TOTAL_DERIVED_STACK_HARD_GIB
RUNTIME_WARN_HOURS = proof.RUNTIME_WARN_HOURS
RUNTIME_HARD_HOURS = proof.RUNTIME_HARD_HOURS
TEMP_WARN_GIB = proof.TEMP_WARN_GIB
TEMP_HARD_GIB = proof.TEMP_HARD_GIB
D_DRIVE_MIN_FREE_GIB_BEFORE = proof.D_DRIVE_MIN_FREE_GIB_BEFORE
D_DRIVE_FAIL_CLOSED_DURING_GIB = proof.D_DRIVE_FAIL_CLOSED_DURING_GIB


class PreV002MlDatasetRunError(PreV002MlDatasetError):
    """Raised when a Phase 4bn-AH data-reading run invariant fails closed."""


# ---------------------------------------------------------------------------
# Small pure helpers (sha256, Phase 4bb-F sidecars)
# ---------------------------------------------------------------------------


def sha256_file(path: str | Path) -> str:
    """Return the hex SHA256 of the file at *path* (streamed, 1 MiB chunks)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sidecar(sidecar_text: str) -> tuple[str, str]:
    """Parse a Phase 4bb-F ``<sha256>␠␠<basename>`` sidecar line.

    Returns ``(sha256_hex, basename)``. Fails closed on any line that is not the
    canonical two-space form with a 64-hex digest.
    """
    line = sidecar_text.strip("\n")
    if "  " not in line:
        raise PreV002MlDatasetRunError(f"sidecar not two-space canonical: {line!r}")
    sha, name = line.split("  ", 1)
    if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        raise PreV002MlDatasetRunError(f"sidecar sha not 64-hex: {sha!r}")
    if not name:
        raise PreV002MlDatasetRunError("sidecar missing basename")
    return sha, name


def sidecar_line(sha256_hex: str, basename: str) -> str:
    """Return the canonical Phase 4bb-F ``<sha256>␠␠<basename>\\n`` sidecar text."""
    if len(sha256_hex) != 64:
        raise PreV002MlDatasetRunError("sha256 must be 64 hex chars")
    return f"{sha256_hex}  {basename}\n"


def write_json_with_sidecar(path: Path, payload: dict[str, Any]) -> tuple[str, str]:
    """Write *payload* as pretty JSON to *path* and a canonical ``.sha256`` sidecar.

    Returns ``(artefact_sha256, sidecar_relpath)``. Both files are created inside
    the caller-provided directory only; no path outside it is resolved.
    """
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    digest = sha256_file(path)
    sidecar = path.with_name(path.name + ".sha256")
    sidecar.write_text(sidecar_line(digest, path.name), encoding="utf-8", newline="\n")
    return digest, sidecar.name


# ---------------------------------------------------------------------------
# Budget preflight (real Phase 4bn-L)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RealBudgetPreflight:
    """Real Phase 4bn-L budget preflight result (measured; not a placeholder)."""

    is_placeholder: bool = False
    ran_preflight: bool = True
    measured_disk: bool = True
    wrote_output: bool = False
    passed: bool = False
    breaches: tuple[str, ...] = ()
    d_free_gib_before: float = 0.0
    derived_footprint_warn_gib: int = DERIVED_FOOTPRINT_WARN_GIB
    derived_footprint_hard_gib: int = DERIVED_FOOTPRINT_HARD_GIB
    total_derived_stack_warn_gib: int = TOTAL_DERIVED_STACK_WARN_GIB
    total_derived_stack_hard_gib: int = TOTAL_DERIVED_STACK_HARD_GIB
    runtime_warn_hours: int = RUNTIME_WARN_HOURS
    runtime_hard_hours: int = RUNTIME_HARD_HOURS
    temp_warn_gib: int = TEMP_WARN_GIB
    temp_hard_gib: int = TEMP_HARD_GIB
    d_drive_min_free_gib_before: int = D_DRIVE_MIN_FREE_GIB_BEFORE
    d_drive_fail_closed_during_gib: int = D_DRIVE_FAIL_CLOSED_DURING_GIB


def evaluate_budget_preflight(d_free_gib_before: float) -> RealBudgetPreflight:
    """Return a real preflight result; fail closed if ``D:`` free < 500 GiB.

    The Phase 4bn-AH dataset artefact is a *compact specification* (kilobytes to a
    few megabytes), so the derived-footprint / total-stack / temp caps are never
    approached; the binding gate is the ``D:`` ≥ 500 GiB-before floor. This helper
    takes the measured free space as an argument so it is unit-testable.
    """
    breaches: list[str] = []
    if d_free_gib_before < D_DRIVE_MIN_FREE_GIB_BEFORE:
        breaches.append(
            f"D: free {d_free_gib_before:.1f} GiB < required "
            f"{D_DRIVE_MIN_FREE_GIB_BEFORE} GiB before start"
        )
    return RealBudgetPreflight(
        passed=not breaches,
        breaches=tuple(breaches),
        d_free_gib_before=round(d_free_gib_before, 2),
    )


def measure_d_free_gib(reference_path: str | Path = REPO_ROOT) -> float:
    """Return the free space (GiB) of the drive holding *reference_path*."""
    usage = shutil.disk_usage(Path(reference_path))
    return usage.free / GIB


def assert_budget_during(reference_path: str | Path = REPO_ROOT) -> float:
    """Fail closed if live free space drops below 350 GiB during execution."""
    free_gib = measure_d_free_gib(reference_path)
    if free_gib < D_DRIVE_FAIL_CLOSED_DURING_GIB:
        raise PreV002MlDatasetRunError(
            f"D: free {free_gib:.1f} GiB fell below the "
            f"{D_DRIVE_FAIL_CLOSED_DURING_GIB} GiB fail-closed floor during the run"
        )
    return free_gib


# ---------------------------------------------------------------------------
# Pre-read verification
# ---------------------------------------------------------------------------


def _load_json(path: str | Path) -> dict[str, Any]:
    with open(REPO_ROOT / path, encoding="utf-8") as fh:
        loaded: dict[str, Any] = json.load(fh)
        return loaded


def _resolve_data_path(inventory_path: str) -> Path:
    """Resolve a manifest inventory path (recorded relative to ``data/``).

    Manifest inventories record paths like
    ``microstructure/features/…/x.parquet`` (relative to the ``data/`` root). This
    prepends ``data/`` when absent and returns an absolute path under the repo.
    """
    rel = inventory_path.replace("\\", "/")
    if not rel.startswith("data/"):
        rel = f"data/{rel}"
    return REPO_ROOT / rel


@dataclass(frozen=True)
class SourceBinding:
    """Verified source binding (manifests, gates, config hashes, inventories)."""

    normalized_manifest_sha256: str
    feature_manifest_sha256: str
    label_manifest_sha256: str
    feature_config_hash: str
    label_config_hash: str
    normalized_gate_report_sha256: str
    feature_gate_report_sha256: str
    label_gate_report_sha256: str
    feature_manifest: dict[str, Any]
    label_manifest: dict[str, Any]


def verify_manifest_and_gate_hashes() -> SourceBinding:
    """Verify the three manifests + three gate reports bind to the contract.

    Computes the SHA256 of every manifest and gate-report file, reuses the
    skeleton :func:`builder.validate_manifest_hashes` for the config-hash / v002
    rejection path, and fails closed on any mismatch. Returns the verified
    binding (with the loaded feature / label manifests for inventory reads).
    """
    norm_m_sha = sha256_file(REPO_ROOT / NORMALIZED_MANIFEST_PATH)
    feat_m_sha = sha256_file(REPO_ROOT / FEATURE_MANIFEST_PATH)
    lab_m_sha = sha256_file(REPO_ROOT / LABEL_MANIFEST_PATH)
    norm_g_sha = sha256_file(REPO_ROOT / NORMALIZED_GATE_PATH)
    feat_g_sha = sha256_file(REPO_ROOT / FEATURE_GATE_PATH)
    lab_g_sha = sha256_file(REPO_ROOT / LABEL_GATE_PATH)

    feature_manifest = _load_json(FEATURE_MANIFEST_PATH)
    label_manifest = _load_json(LABEL_MANIFEST_PATH)
    feature_config_hash = str(feature_manifest["feature_config_hash"])
    label_config_hash = str(label_manifest["label_config_hash"])

    # Reuse the skeleton validator for the full manifest / config / gate binding
    # (this also rejects the v002-terminal 819cfa7a… / 352bad41… hashes).
    builder.validate_manifest_hashes(
        normalized_like={
            "manifest_sha256": norm_m_sha,
            "gate_report_sha256": norm_g_sha,
            "partition_count": 275,
        },
        feature_like={
            "manifest_sha256": feat_m_sha,
            "feature_config_hash": feature_config_hash,
            "gate_report_sha256": feat_g_sha,
            "partition_count": 275,
        },
        label_like={
            "manifest_sha256": lab_m_sha,
            "label_config_hash": label_config_hash,
            "gate_report_sha256": lab_g_sha,
            "partition_count": 275,
        },
    )
    return SourceBinding(
        normalized_manifest_sha256=norm_m_sha,
        feature_manifest_sha256=feat_m_sha,
        label_manifest_sha256=lab_m_sha,
        feature_config_hash=feature_config_hash,
        label_config_hash=label_config_hash,
        normalized_gate_report_sha256=norm_g_sha,
        feature_gate_report_sha256=feat_g_sha,
        label_gate_report_sha256=lab_g_sha,
        feature_manifest=feature_manifest,
        label_manifest=label_manifest,
    )


def verify_source_scope(binding: SourceBinding) -> None:
    """Reuse the skeleton :func:`builder.validate_source_scope` on real manifests.

    Builds a ``manifest_like`` mapping from the actual feature / label manifest
    fields and fails closed on any scope drift, wrong count, wrong row total, or a
    forbidden danger flag.
    """
    fm = binding.feature_manifest
    lm = binding.label_manifest
    for name, m in (("feature", fm), ("label", lm)):
        manifest_like = {
            "symbol": m.get("symbol"),
            "market": _market(m),
            "source_family": _source_family(m),
            "start_date": m.get("date_start"),
            "end_date": m.get("date_end"),
            "feature_partition_count": int(m.get("date_count", -1)),
            "label_partition_count": int(m.get("date_count", -1)),
            "normalized_partition_count": int(m.get("date_count", -1)),
            "row_count": int(m.get("total_row_count", -1)),
            "contains_v002_terminal": _contains_v002_terminal(m),
            "contains_sealed_test": bool(m.get("sealed_test_split_touched")),
            "full_envelope": bool(m.get("full_envelope")),
            "private_source": False,
            "authenticated_source": False,
            "external_source": False,
        }
        builder.validate_source_scope(manifest_like)
        if int(m.get("test_rows_loaded", -1)) != 0:
            raise PreV002MlDatasetRunError(
                f"{name} manifest test_rows_loaded must be 0"
            )
        # Defence-in-depth: reject a v002-terminal window mode that is not a safe
        # by-reference / excluded mode (the pre-v002 segment must never include it).
        mode = str(m.get("v002_terminal_window_mode", "")).lower()
        if mode not in _V002_SAFE_REFERENCE_MODES:
            raise PreV002MlDatasetRunError(
                f"{name} manifest v002_terminal_window_mode {mode!r} is not a safe "
                "by-reference / excluded mode"
            )


# The whole Prometheus microstructure stack is Binance USDⓈ-M futures; the
# manifest layer records the market as ``usdm_futures`` while the Phase 4bn-AC
# contract token is the fully-qualified ``binance_usdm_futures``. These are the
# same venue; any other value fails closed via validate_source_scope.
_KNOWN_BINANCE_USDM_MARKETS = frozenset(
    {"usdm_futures", "binance_usdm_futures", "binance-usdm-futures", "um", "usdⓈ-m"}
)
# v002-terminal window modes that mean "referenced but NOT read" (safe). A mode
# outside this set (e.g. an inclusion / full-envelope mode) fails closed.
_V002_SAFE_REFERENCE_MODES = frozenset(
    {"by_reference", "by_reference_only", "excluded", "none", ""}
)


def _market(manifest: dict[str, Any]) -> str:
    market = manifest.get("market")
    if isinstance(market, str) and market.lower() in _KNOWN_BINANCE_USDM_MARKETS:
        return contract.MARKET
    return str(market)


def _contains_v002_terminal(manifest: dict[str, Any]) -> bool:
    mode = str(manifest.get("v002_terminal_window_mode", "")).lower()
    return mode not in _V002_SAFE_REFERENCE_MODES


def _source_family(manifest: dict[str, Any]) -> str:
    fam = manifest.get("data_family") or manifest.get("source_family")
    # Normalize common recorded spellings to the contract token.
    if isinstance(fam, str) and fam.lower() in ("aggtrades", "aggtrade"):
        return contract.SOURCE_FAMILY
    return str(fam)


@dataclass(frozen=True)
class PartitionRef:
    """One verified feature+label partition reference for a UTC date."""

    date: str
    split: str
    feature_parquet: Path
    label_parquet: Path
    feature_sha256: str
    label_sha256: str
    row_count: int


def verify_per_parquet_sidecars_and_inventory(
    binding: SourceBinding, *, progress: bool = False
) -> list[PartitionRef]:
    """Verify all 275 feature + 275 label Parquet against inventory and sidecars.

    For every inventory entry, computes the Parquet SHA256 and fails closed unless
    it matches (a) the manifest inventory hash and (b) the on-disk ``.sha256``
    sidecar (parsed as a Phase 4bb-F two-space line). Confirms exactly 275
    partitions per layer and pairs them by UTC date. Returns the ordered, verified
    partition references (one per in-segment date, embargo dates included).
    """
    fm = binding.feature_manifest
    lm = binding.label_manifest
    feat_inv = {str(e["date"]): e for e in fm["per_file_inventory"]}
    lab_inv = {str(e["date"]): e for e in lm["per_day_outputs"]}
    if len(feat_inv) != 275 or len(lab_inv) != 275:
        raise PreV002MlDatasetRunError(
            f"partition counts must be 275/275, got {len(feat_inv)}/{len(lab_inv)}"
        )

    seg = split_policy.segment_dates()
    if set(feat_inv) != set(seg) or set(lab_inv) != set(seg):
        raise PreV002MlDatasetRunError(
            "manifest inventory dates do not match the 275 pre-v002 segment dates"
        )

    refs: list[PartitionRef] = []
    for i, date_str in enumerate(seg):
        fe = feat_inv[date_str]
        le = lab_inv[date_str]
        fpath = _resolve_data_path(str(fe["feature_parquet_path"]))
        lpath = _resolve_data_path(str(le["label_parquet_path"]))
        _verify_one(fpath, str(fe["feature_parquet_sha256"]), layer="feature")
        _verify_one(lpath, str(le["label_parquet_sha256"]), layer="label")
        f_rows = int(fe["row_count"])
        l_rows = int(le["row_count"])
        if f_rows != l_rows:
            raise PreV002MlDatasetRunError(
                f"{date_str}: feature rows {f_rows} != label rows {l_rows}"
            )
        refs.append(
            PartitionRef(
                date=date_str,
                split=split_policy.split_for_date(date_str),
                feature_parquet=fpath,
                label_parquet=lpath,
                feature_sha256=str(fe["feature_parquet_sha256"]),
                label_sha256=str(le["label_parquet_sha256"]),
                row_count=f_rows,
            )
        )
        if progress and (i + 1) % 25 == 0:
            print(f"[pre-read] verified {i + 1}/275 partitions", flush=True)
    return refs


def _verify_one(parquet_path: Path, inventory_sha: str, *, layer: str) -> None:
    if not parquet_path.is_file():
        raise PreV002MlDatasetRunError(f"missing {layer} parquet {parquet_path}")
    sidecar_path = parquet_path.with_name(parquet_path.name + ".sha256")
    if not sidecar_path.is_file():
        raise PreV002MlDatasetRunError(f"missing {layer} sidecar {sidecar_path}")
    sidecar_sha, sidecar_name = parse_sidecar(
        sidecar_path.read_text(encoding="utf-8")
    )
    if sidecar_name != parquet_path.name:
        raise PreV002MlDatasetRunError(
            f"{layer} sidecar name {sidecar_name!r} != {parquet_path.name!r}"
        )
    actual = sha256_file(parquet_path)
    if actual != inventory_sha:
        raise PreV002MlDatasetRunError(
            f"{layer} {parquet_path.name}: sha {actual[:12]}… != inventory "
            f"{inventory_sha[:12]}…"
        )
    if actual != sidecar_sha:
        raise PreV002MlDatasetRunError(
            f"{layer} {parquet_path.name}: sha {actual[:12]}… != sidecar "
            f"{sidecar_sha[:12]}…"
        )


def split_authority_commit_sha() -> str:
    """Return the git commit SHA that last touched the split-policy module."""
    module_rel = "src/prometheus/research/microstructure/pre_v002_split_policy.py"
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", module_rel],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip() or "unknown"
    except (subprocess.SubprocessError, OSError):
        return "unknown"


def bind_split_authority() -> str:
    """Confirm the split-policy identity + arithmetic; return its commit SHA."""
    if split_policy.SPLIT_POLICY_NAME != (
        "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"
    ):
        raise PreV002MlDatasetRunError("split policy name mismatch")
    split_policy.validate_policy_arithmetic()
    return split_authority_commit_sha()


# ---------------------------------------------------------------------------
# Streaming column readers / accumulators
# ---------------------------------------------------------------------------

_ALIGNMENT_KEYS = list(contract.ALIGNMENT_KEYS)  # row_index, agg_trade_id, ft_ms, stt_ms
_LABEL_READ_COLS = [
    contract.PRIMARY_TARGET,
    contract.PRIMARY_LOG_RETURN,
    contract.PRIMARY_CENSORED_FLAG,
    contract.LABEL_INVALID_PRICE_FLAG,
    *_ALIGNMENT_KEYS,
    "utc_date",
]
_FEATURE_KEY_COLS = [*_ALIGNMENT_KEYS, "utc_date"]


def _col_to_float64(table: pa.Table, name: str) -> np.ndarray:
    """Return a float64 numpy array for column *name*, casting strings/bools."""
    col = table.column(name)
    casted = pc.cast(col, "float64")  # decimal-strings, ints, bools → float64
    return np.asarray(casted.to_numpy(zero_copy_only=False), dtype=np.float64)


@dataclass
class _FeatureStats:
    """Streaming train-only accumulators for one feature column."""

    count: int = 0
    nan_count: int = 0
    total: float = 0.0
    total_sq: float = 0.0

    def update(self, arr: np.ndarray) -> None:
        finite = np.isfinite(arr)
        self.nan_count += int((~finite).sum())
        vals = arr[finite]
        self.count += int(vals.size)
        self.total += float(vals.sum())
        self.total_sq += float(np.square(vals).sum())

    def mean_std(self) -> tuple[float, float]:
        if self.count == 0:
            return 0.0, 0.0
        mean = self.total / self.count
        var = max(self.total_sq / self.count - mean * mean, 0.0)
        return mean, math.sqrt(var)


@dataclass
class _RunAccumulators:
    """All streaming accumulators for the single run."""

    feature_stats: dict[str, _FeatureStats] = field(default_factory=dict)
    per_date: list[dict[str, object]] = field(default_factory=list)
    split_raw_rows: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    split_filtered_rows: dict[str, int] = field(
        default_factory=lambda: defaultdict(int)
    )
    split_dropped: dict[str, dict[str, int]] = field(default_factory=dict)
    split_class_counts: dict[str, dict[str, int]] = field(default_factory=dict)
    month_split_rows: dict[str, dict[str, int]] = field(default_factory=dict)
    max_stt_by_split: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    alignment_rows_checked: int = 0
    alignment_mismatches: int = 0
    test_rows_loaded: int = 0

    def __post_init__(self) -> None:
        for col in contract.ALLOWED_FEATURE_COLUMNS:
            self.feature_stats[col] = _FeatureStats()
        for sp in split_policy.MODEL_ELIGIBLE_SPLITS:
            self.split_dropped[sp] = {r: 0 for r in builder.DROP_REASONS}
            self.split_class_counts[sp] = {"-1": 0, "0": 0, "1": 0}


def _check_alignment_vectorized(
    ftab: pa.Table, ltab: pa.Table, date_str: str
) -> int:
    """Fail closed unless the 4 alignment keys match element-wise; return rows."""
    n_f = int(ftab.num_rows)
    n_l = int(ltab.num_rows)
    if n_f != n_l:
        raise PreV002MlDatasetRunError(
            f"{date_str}: feature rows {n_f} != label rows {n_l}"
        )
    for key in _ALIGNMENT_KEYS:
        fa = ftab.column(key).to_numpy(zero_copy_only=False)
        la = ltab.column(key).to_numpy(zero_copy_only=False)
        if not np.array_equal(fa, la):
            raise PreV002MlDatasetRunError(
                f"{date_str}: alignment key {key!r} mismatch"
            )
    # optional keys
    fu = ftab.column("utc_date").to_numpy(zero_copy_only=False)
    lu = ltab.column("utc_date").to_numpy(zero_copy_only=False)
    if not np.array_equal(fu, lu):
        raise PreV002MlDatasetRunError(f"{date_str}: utc_date mismatch")
    return n_f


def _process_partition(ref: PartitionRef, acc: _RunAccumulators) -> None:
    """Stream one partition: verify alignment, filter, split-account, fit train."""
    split = ref.split
    # Hard guard: never read a v002/sealed date (split_for_date already raised for
    # out-of-segment dates during verification; this is defence-in-depth).
    if split not in split_policy.ALL_SPLITS:
        raise PreV002MlDatasetRunError(f"{ref.date}: unexpected split {split!r}")

    ltab = pq.read_table(ref.label_parquet, columns=_LABEL_READ_COLS)
    read_feature_matrix = split == split_policy.TRAIN
    fcols = (
        [*_FEATURE_KEY_COLS, *contract.ALLOWED_FEATURE_COLUMNS]
        if read_feature_matrix
        else _FEATURE_KEY_COLS
    )
    ftab = pq.read_table(ref.feature_parquet, columns=fcols)

    n = _check_alignment_vectorized(ftab, ltab, ref.date)
    acc.alignment_rows_checked += n
    acc.split_raw_rows[split] += n

    month = ref.date[:7]
    acc.month_split_rows.setdefault(month, defaultdict(int))
    acc.month_split_rows[month][split] += n

    if split == split_policy.EMBARGO:
        # Embargo dates are dropped in full; no filtering / stats / class counts.
        acc.per_date.append(
            {
                "date": ref.date,
                "split": split,
                "raw_row_count": n,
                "filtered_row_count": 0,
                "dropped_by_reason": {"embargo_date_dropped": n},
            }
        )
        return

    # Track the max source_transact_time_ms for the earlier-split boundary proof.
    stt = ltab.column("source_transact_time_ms").to_numpy(zero_copy_only=False)
    if stt.size:
        acc.max_stt_by_split[split] = max(
            acc.max_stt_by_split[split], int(stt.max())
        )

    # Vectorised target filtering (drop precedence: invalid → censored → null_dir
    # → null_log_return); never impute.
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

    d = acc.split_dropped[split]
    d["invalid_price"] += int(drop_invalid.sum())
    d["censored"] += int(drop_censored.sum())
    d["null_direction"] += int(drop_null_dir.sum())
    d["null_log_return"] += int(drop_null_lr.sum())
    kept = int(keep.sum())
    acc.split_filtered_rows[split] += kept

    # Class distribution over kept rows.
    dir_vals = direction.to_numpy(zero_copy_only=False)
    kept_dir = np.asarray(dir_vals)[keep]
    cc = acc.split_class_counts[split]
    cc["-1"] += int((kept_dir == -1).sum())
    cc["0"] += int((kept_dir == 0).sum())
    cc["1"] += int((kept_dir == 1).sum())

    # Train-only transform fitting (kept rows only, train split only).
    if read_feature_matrix:
        keep_idx = np.nonzero(keep)[0]
        for col in contract.ALLOWED_FEATURE_COLUMNS:
            arr = _col_to_float64(ftab, col)
            acc.feature_stats[col].update(arr[keep_idx])

    acc.per_date.append(
        {
            "date": ref.date,
            "split": split,
            "raw_row_count": n,
            "filtered_row_count": kept,
            "dropped_by_reason": {
                "invalid_price": int(drop_invalid.sum()),
                "censored": int(drop_censored.sum()),
                "null_direction": int(drop_null_dir.sum()),
                "null_log_return": int(drop_null_lr.sum()),
            },
        }
    )


# ---------------------------------------------------------------------------
# Run proof (real) — reuses the skeleton conservative-posture validator
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BuilderRunProof:
    """Real Phase 4bn-AH run proof: conservative sections + real IO fields."""

    contract_name: str
    amendment_id: str
    split: proof.SplitProof
    alignment: proof.AlignmentProof
    filtering: proof.FilteringProof
    evaluation: proof.EvaluationPreregistrationProof
    non_authorization: proof.NonAuthorizationProof
    budget_preflight: RealBudgetPreflight
    split_policy_commit_sha: str
    active_feature_list_hash: str
    output_namespace_path: str
    output_namespace_created: bool
    no_data_io: bool  # False for the real run (it reads data)
    per_horizon_boundary_crossing_rows: dict[str, int] = field(default_factory=dict)


def _conservative_mirror(rp: BuilderRunProof) -> proof.DatasetBuilderProof:
    """Build a skeleton-shaped proof mirroring the conservative sections.

    The mirror carries the placeholder budget / no-output / no-data-io shape the
    skeleton validator expects, so the split / alignment / filtering / evaluation /
    non-authorization sections are validated by the *existing*
    :func:`proof.validate_dataset_builder_proof` path.
    """
    return proof.DatasetBuilderProof(
        contract_name=rp.contract_name,
        amendment_id=rp.amendment_id,
        split=rp.split,
        alignment=rp.alignment,
        filtering=rp.filtering,
        evaluation=rp.evaluation,
        budget_preflight=proof.BudgetPreflightPlaceholder(),
        non_authorization=rp.non_authorization,
        output_namespace_created=False,
        no_data_io=True,
    )


def validate_builder_run_proof(rp: BuilderRunProof) -> None:
    """Fail closed unless *rp* encodes a valid, conservative, budget-safe run.

    Validates the conservative posture through the existing skeleton validator
    (:func:`proof.validate_dataset_builder_proof`) and then the real-IO fields
    specific to the data-reading run.
    """
    # 1. Conservative posture via the existing skeleton path.
    proof.validate_dataset_builder_proof(_conservative_mirror(rp))

    # 2. Real budget preflight must have run, measured disk, and passed.
    b = rp.budget_preflight
    if b.is_placeholder or not b.ran_preflight or not b.measured_disk:
        raise PreV002MlDatasetRunError(
            "run proof budget preflight must be real, run, and disk-measured"
        )
    if not b.passed or b.breaches:
        raise PreV002MlDatasetRunError(
            f"run proof budget preflight did not pass: {b.breaches!r}"
        )
    if b.d_free_gib_before < D_DRIVE_MIN_FREE_GIB_BEFORE:
        raise PreV002MlDatasetRunError("run proof records D: free below 500 GiB floor")

    # 3. Real IO fields: the run reads data and creates the namespace exactly once.
    if rp.no_data_io is not False:
        raise PreV002MlDatasetRunError("run proof no_data_io must be False (it reads)")
    if rp.output_namespace_created is not True:
        raise PreV002MlDatasetRunError("run proof output_namespace_created must be True")
    if rp.output_namespace_path != OUTPUT_NAMESPACE + "/":
        raise PreV002MlDatasetRunError("run proof output namespace path mismatch")

    # 4. Per-horizon boundary crossings must be zero.
    if any(v != 0 for v in rp.per_horizon_boundary_crossing_rows.values()):
        raise PreV002MlDatasetRunError(
            f"per-horizon boundary crossings must be zero: "
            f"{rp.per_horizon_boundary_crossing_rows!r}"
        )
    if rp.split.test_rows_loaded != 0:
        raise PreV002MlDatasetRunError("run proof test_rows_loaded must be 0")


def feature_list_hash(columns: tuple[str, ...] = contract.ALLOWED_FEATURE_COLUMNS) -> str:
    """Return the SHA256 of the canonical-ordered 45-column feature list."""
    return hashlib.sha256("\n".join(columns).encode("utf-8")).hexdigest()


def per_horizon_boundary_crossings(
    max_stt_by_split: dict[str, int],
) -> dict[str, int]:
    """Return per-horizon earlier-split boundary-crossing counts (must be zero).

    The one-full-UTC-date embargo (2024-10-01, 2024-11-16) strictly dominates the
    ≤ 60 s label horizons, so no train/validation row's ``T + H`` can reach the
    next split boundary. This is proven from the observed per-split max
    ``source_transact_time_ms`` rather than assumed.
    """
    out: dict[str, int] = {}
    for h in split_policy.ALLOWED_HORIZONS_MS:
        crossings = 0
        for sp in (split_policy.TRAIN, split_policy.VALIDATION):
            max_t = max_stt_by_split.get(sp, 0)
            if max_t and split_policy.is_earlier_split_boundary_crossing(max_t, h, sp):
                crossings += 1  # a positive here would fail the run
        out[f"{h}ms"] = crossings
    return out


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run(*, output_namespace: str = OUTPUT_NAMESPACE, progress: bool = True) -> dict[str, Any]:
    """Execute the single controlled data-reading build; return a summary dict.

    Fails closed (raising :class:`PreV002MlDatasetRunError`) on any pre-read,
    alignment, split, budget, or output-boundary violation, writing nothing on
    failure. On success, writes the compact dataset artefacts + Phase 4bb-F
    sidecars inside *output_namespace* only and returns the run summary.
    """
    t0 = time.monotonic()
    out_dir = REPO_ROOT / output_namespace

    # One-run guard: refuse to overwrite a completed build.
    manifest_path = out_dir / "dataset_manifest.json"
    if manifest_path.exists():
        raise PreV002MlDatasetRunError(
            "dataset already built at this namespace; a rerun requires separate "
            "operator authorization (no safe idempotent overwrite is defined)"
        )

    # --- Budget preflight (before any write; D: >= 500 GiB) ---
    d_free_before = measure_d_free_gib()
    preflight = evaluate_budget_preflight(d_free_before)
    if not preflight.passed:
        raise PreV002MlDatasetRunError(
            f"budget preflight failed closed: {preflight.breaches!r}"
        )

    # --- Pre-read checks (before any feature/label row read) ---
    if progress:
        print("[pre-read] verifying manifest + gate hashes…", flush=True)
    binding = verify_manifest_and_gate_hashes()
    verify_source_scope(binding)
    split_commit = bind_split_authority()
    if progress:
        print("[pre-read] verifying 550 per-parquet sidecars…", flush=True)
    refs = verify_per_parquet_sidecars_and_inventory(binding, progress=progress)
    if len(refs) != 275:
        raise PreV002MlDatasetRunError(f"expected 275 partitions, got {len(refs)}")

    # --- Streaming build ---
    acc = _RunAccumulators()
    for i, ref in enumerate(refs):
        _process_partition(ref, acc)
        if progress and (i + 1) % 25 == 0:
            assert_budget_during()
            print(
                f"[build] {i + 1}/275 processed "
                f"(rows checked {acc.alignment_rows_checked:,})",
                flush=True,
            )

    total_rows = acc.alignment_rows_checked
    if total_rows != contract.EXPECTED_ROW_COUNT:
        raise PreV002MlDatasetRunError(
            f"streamed row total {total_rows} != expected "
            f"{contract.EXPECTED_ROW_COUNT}"
        )

    boundary_crossings = per_horizon_boundary_crossings(dict(acc.max_stt_by_split))

    # --- Assemble the leakage / split-integrity proof ---
    dropped_by_split_and_reason = {
        sp: dict(acc.split_dropped[sp]) for sp in split_policy.MODEL_ELIGIBLE_SPLITS
    }
    flh = feature_list_hash()
    run_proof = BuilderRunProof(
        contract_name=contract.CONTRACT_NAME,
        amendment_id=contract.CONTRACT_AMENDMENT_ID,
        split=proof.SplitProof(
            split_policy_commit_sha=split_commit,
            train_date_count=214,
            validation_date_count=45,
            holdout_date_count=14,
        ),
        alignment=proof.AlignmentProof(
            key_alignment_row_count=acc.alignment_rows_checked,
            mismatched_rows=acc.alignment_mismatches,
        ),
        filtering=proof.FilteringProof(
            dropped_by_split_and_reason=dropped_by_split_and_reason,
            targets_imputed=False,
        ),
        evaluation=proof.EvaluationPreregistrationProof(
            active_feature_list_hash=flh,
        ),
        non_authorization=proof.NonAuthorizationProof(),
        budget_preflight=preflight,
        split_policy_commit_sha=split_commit,
        active_feature_list_hash=flh,
        output_namespace_path=OUTPUT_NAMESPACE + "/",
        output_namespace_created=True,
        no_data_io=False,
        per_horizon_boundary_crossing_rows=boundary_crossings,
    )

    # Validate BEFORE writing anything (pre-write gate #12).
    validate_builder_run_proof(run_proof)

    # --- Write artefacts (only now; only inside the namespace) ---
    assert_budget_during()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = _write_artefacts(out_dir, binding, acc, run_proof, split_commit)

    elapsed = time.monotonic() - t0
    summary = {
        "phase": RUN_PHASE,
        "contract_name": contract.CONTRACT_NAME,
        "output_namespace": OUTPUT_NAMESPACE + "/",
        "total_rows": total_rows,
        "split_raw_rows": dict(acc.split_raw_rows),
        "split_filtered_rows": dict(acc.split_filtered_rows),
        "dropped_by_split_and_reason": dropped_by_split_and_reason,
        "per_horizon_boundary_crossing_rows": boundary_crossings,
        "test_rows_loaded": acc.test_rows_loaded,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "budget_preflight_passed": run_proof.budget_preflight.passed,
        "d_free_gib_before": run_proof.budget_preflight.d_free_gib_before,
        "elapsed_seconds": round(elapsed, 1),
        "artefacts": written,
        "split_policy_commit_sha": split_commit,
        "feature_list_hash": flh,
    }
    if progress:
        print(f"[done] {json.dumps(summary, indent=2)}", flush=True)
    return summary


def _write_artefacts(
    out_dir: Path,
    binding: SourceBinding,
    acc: _RunAccumulators,
    run_proof: BuilderRunProof,
    split_commit: str,
) -> dict[str, str]:
    """Write the compact dataset artefacts + Phase 4bb-F sidecars; return shas."""
    # train-only transform statistics (fit on the train split only)
    transform = {
        "fit_split": "train",
        "standardization_rule": contract.STANDARDIZATION_RULE,
        "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
        "imputation_rule": contract.IMPUTATION_RULE,
        "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
        "standardize_boolean_flags": contract.STANDARDIZE_BOOLEAN_FLAGS,
        "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": run_proof.active_feature_list_hash,
        "per_feature": {
            col: {
                "train_mean": acc.feature_stats[col].mean_std()[0],
                "train_std": acc.feature_stats[col].mean_std()[1],
                "train_count": acc.feature_stats[col].count,
                "train_null_count": acc.feature_stats[col].nan_count,
            }
            for col in contract.ALLOWED_FEATURE_COLUMNS
        },
    }

    split_index = {
        "split_policy_name": split_policy.SPLIT_POLICY_NAME,
        "split_policy_module_path": contract.SPLIT_POLICY_MODULE_PATH,
        "split_policy_commit_sha": split_commit,
        "per_date": acc.per_date,
    }

    month_block = {
        m: dict(sp) for m, sp in sorted(acc.month_split_rows.items())
    }
    dataset_manifest = {
        "dataset_name": contract.CONTRACT_NAME,
        "dataset_version": DATASET_VERSION,
        "amendment_id": contract.CONTRACT_AMENDMENT_ID,
        "phase": RUN_PHASE,
        "symbol": contract.SYMBOL,
        "market": contract.MARKET,
        "source_family": contract.SOURCE_FAMILY,
        "segment_start_date": contract.START_DATE,
        "segment_end_date": contract.END_DATE,
        "expected_row_count": contract.EXPECTED_ROW_COUNT,
        "streamed_row_count": acc.alignment_rows_checked,
        "primary_target": contract.PRIMARY_TARGET,
        "primary_horizon_ms": contract.PRIMARY_HORIZON_MS,
        "target_classes": list(contract.TARGET_CLASSES),
        "feature_count": len(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list": list(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": run_proof.active_feature_list_hash,
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
        "split_raw_rows": dict(acc.split_raw_rows),
        "split_filtered_rows": dict(acc.split_filtered_rows),
        "split_class_counts": acc.split_class_counts,
        "dropped_by_split_and_reason": {
            sp: dict(acc.split_dropped[sp])
            for sp in split_policy.MODEL_ELIGIBLE_SPLITS
        },
        "month_block_split_rows": month_block,
        "decision_block_units": list(contract.DECISION_BLOCK_UNITS),
        "metric_granularities": list(contract.METRIC_GRANULARITIES),
        "row_level_metrics_descriptive_only": (
            contract.ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY
        ),
        "dependence_caveat": (
            "aggTrades 15s forward labels overlap heavily; rows are NOT "
            "independent; per-row metrics are descriptive only and per-row "
            "significance language is forbidden (Phase 4bn-AE Option 1)."
        ),
        "decimation_stride": contract.DECIMATION_STRIDE,
        "decimation_policy": contract.DECIMATION_POLICY,
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "test_rows_loaded": 0,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
    }

    run_proof_payload = _proof_to_json(run_proof)

    written: dict[str, str] = {}
    for name, payload in (
        ("train_only_transform.json", transform),
        ("split_index.json", split_index),
        ("dataset_manifest.json", dataset_manifest),
        ("leakage_split_integrity_proof.json", run_proof_payload),
    ):
        digest, _ = write_json_with_sidecar(out_dir / name, payload)
        written[name] = digest
    return written


def _proof_to_json(rp: BuilderRunProof) -> dict[str, Any]:
    return {
        "phase": RUN_PHASE,
        "contract_name": rp.contract_name,
        "amendment_id": rp.amendment_id,
        "split_policy_name": rp.split.split_policy_name,
        "split_policy_module_path": contract.SPLIT_POLICY_MODULE_PATH,
        "split_policy_commit_sha": rp.split_policy_commit_sha,
        "split": asdict(rp.split),
        "alignment": asdict(rp.alignment),
        "filtering": asdict(rp.filtering),
        "evaluation": asdict(rp.evaluation),
        "non_authorization": asdict(rp.non_authorization),
        "budget_preflight": asdict(rp.budget_preflight),
        "active_feature_list_hash": rp.active_feature_list_hash,
        "output_namespace_path": rp.output_namespace_path,
        "output_namespace_created": rp.output_namespace_created,
        "no_data_io": rp.no_data_io,
        "per_horizon_boundary_crossing_rows": rp.per_horizon_boundary_crossing_rows,
    }


def main() -> None:  # pragma: no cover - CLI entry
    summary = run()
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":  # pragma: no cover
    main()


__all__ = [
    "BuilderRunProof",
    "OUTPUT_NAMESPACE",
    "PartitionRef",
    "PreV002MlDatasetRunError",
    "RealBudgetPreflight",
    "SourceBinding",
    "assert_budget_during",
    "bind_split_authority",
    "evaluate_budget_preflight",
    "feature_list_hash",
    "main",
    "measure_d_free_gib",
    "parse_sidecar",
    "per_horizon_boundary_crossings",
    "run",
    "sha256_file",
    "sidecar_line",
    "split_authority_commit_sha",
    "validate_builder_run_proof",
    "verify_manifest_and_gate_hashes",
    "verify_per_parquet_sidecars_and_inventory",
    "verify_source_scope",
    "write_json_with_sidecar",
]
