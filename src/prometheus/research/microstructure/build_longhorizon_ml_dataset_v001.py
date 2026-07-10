"""Phase 4bn-AQ — long-horizon pre-v002 ML dataset builder (single controlled run).

The **data-reading** realisation of the Phase 4bn-AP long-horizon ML baseline
pre-registration's dataset-build step. It binds the already-gated Phase 4bn-AH
45-feature causal aggTrades source (Phase 4bn-S features / Phase 4bn-O
normalized lineage) to the Phase 4bn-AN long-horizon label family
(``microstructure_labels_longhorizon_aggtrades_v001``; horizons ``5m/30m/1h``;
``label_config_hash edaeafde…``), verifies every source binding, and writes — with
Phase 4bb-F canonical ``.sha256`` sidecars — a **compact dataset specification**
to the single authorized local **gitignored** namespace
``data/research/microstructure/ml_datasets/longhorizon_pre_v001/``.

Design (budget-safe, honest): mirrors the proven Phase 4bn-AH compact-spec build.
The dataset artefact is NOT a re-materialised ``400,001,695 × 45`` float64 matrix
(~144 GiB — it would breach the Phase 4bn-L 125 GiB derived-footprint hard cap and
merely duplicate the already-gated feature Parquet). Instead this builder streams
every partition once (bounded memory) and materialises:

- the **train-only fitted transform statistics** for the frozen 45 features (fit on
  the ``train`` split only, over rows valid for the primary ``forward_direction_5m``
  target; validation / holdout / embargo excluded);
- a **per-date split / per-horizon support index** (split, raw rows, per-horizon
  valid / censored / null-direction / invalid-price accounting);
- per-split × per-horizon **support / censoring / class-distribution** summaries;
- a **machine-checkable leakage / split-integrity proof** (strict positional
  alignment over the 5 keys, per-horizon zero earlier-model-split boundary
  crossings, no imputation, no v002/sealed access, all non-authorization flags
  False);
- a **feature ↔ label source-binding** artefact (feature manifest / config / gate
  SHAs bound to the AN long-horizon label family + ``label_config_hash``, with the
  per-date ``paired_source_feature_parquet_sha256`` cross-check);
- a **dataset manifest**, a **sidecar inventory**, and a **build run record**.

Hard boundaries (all enforced, fail-closed): reads **only** the admitted pre-v002
feature + long-horizon label sources; never the v002 terminal window or the sealed
test (``test_rows_loaded = 0``); imputes no target; fits transforms on ``train``
only; writes **only** inside the authorized namespace; commits nothing; trains no
model; scores nothing; produces no prediction / metric / baseline; runs no
diagnostics / strategy / PnL / backtest; mutates no AH / AJ / AN namespace; flips
no eligibility; sets no manifest field; authorizes no successor.

It reuses the Phase 4bn-AF skeleton validators (``pre_v002_ml_dataset_builder``),
the proof schema (``pre_v002_ml_dataset_proof``), the Phase 4bn-AA split artefact
(``pre_v002_split_policy``), and the Phase 4bn-AH sidecar / budget helpers.
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

from . import longhorizon_ml_dataset_contract_v001 as contract
from . import pre_v002_ml_dataset_builder as builder
from . import pre_v002_ml_dataset_proof as proof
from . import pre_v002_split_policy as split_policy
from .pre_v002_ml_dataset_builder import PreV002MlDatasetError

# ---------------------------------------------------------------------------
# Identity / paths
# ---------------------------------------------------------------------------

RUN_PHASE = "phase-4bn-aq"
DATASET_VERSION = contract.DATASET_VERSION

REPO_ROOT = Path(__file__).resolve().parents[4]

OUTPUT_NAMESPACE = contract.OUTPUT_NAMESPACE

_MANIFEST_DIR = "data/microstructure/manifests"
_GATE_DIR = "data/microstructure/gate-reports"

# Committed feature / normalized source witnesses (the AH 45-feature source).
NORMALIZED_MANIFEST_PATH = (
    f"{_MANIFEST_DIR}/"
    "microstructure_normalized_aggtrades_v001__v002_pre_v002_segment_4bn_o.json"
)
FEATURE_MANIFEST_PATH = (
    f"{_MANIFEST_DIR}/"
    "microstructure_features_aggtrades_v001__v002_pre_v002_segment_4bn_s.json"
)
NORMALIZED_GATE_PATH = (
    f"{_GATE_DIR}/normalized/microstructure_normalized_aggtrades_v001__v002"
    "_pre_v002_segment_4bn_o__phase-4bn-p__1780599605192__3fd795ceac4f.json"
)
FEATURE_GATE_PATH = (
    f"{_GATE_DIR}/features/microstructure_features_aggtrades_v001__v002"
    "_pre_v002_segment_4bn_s__phase-4bn-t__1780674917156__e647435c81d7.json"
)

# The Phase 4bn-AN long-horizon label family (research namespace, gitignored).
_LABEL_FAMILY_DIR = (
    "data/research/microstructure/labels/"
    "microstructure_labels_longhorizon_aggtrades_v001_pre_v002"
)
LABEL_MANIFEST_PATH = (
    f"{_LABEL_FAMILY_DIR}/_manifest/"
    "microstructure_labels_longhorizon_aggtrades_v001_pre_v002.manifest.json"
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


class LongHorizonMlDatasetRunError(PreV002MlDatasetError):
    """Raised when a Phase 4bn-AQ data-reading run invariant fails closed."""


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
    """Parse a Phase 4bb-F ``<sha256>␠␠<basename>`` sidecar line."""
    line = sidecar_text.strip("\n")
    if "  " not in line:
        raise LongHorizonMlDatasetRunError(
            f"sidecar not two-space canonical: {line!r}"
        )
    sha, name = line.split("  ", 1)
    if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
        raise LongHorizonMlDatasetRunError(f"sidecar sha not 64-hex: {sha!r}")
    if not name:
        raise LongHorizonMlDatasetRunError("sidecar missing basename")
    return sha, name


def sidecar_line(sha256_hex: str, basename: str) -> str:
    """Return the canonical Phase 4bb-F ``<sha256>␠␠<basename>\\n`` sidecar text."""
    if len(sha256_hex) != 64:
        raise LongHorizonMlDatasetRunError("sha256 must be 64 hex chars")
    return f"{sha256_hex}  {basename}\n"


def write_json_with_sidecar(path: Path, payload: dict[str, Any]) -> tuple[str, str]:
    """Write *payload* as pretty JSON to *path* and a canonical ``.sha256`` sidecar."""
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")
    digest = sha256_file(path)
    sidecar = path.with_name(path.name + ".sha256")
    sidecar.write_text(
        sidecar_line(digest, path.name), encoding="utf-8", newline="\n"
    )
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

    The Phase 4bn-AQ dataset artefact is a *compact specification* (kilobytes to a
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
        raise LongHorizonMlDatasetRunError(
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
    """Resolve a manifest inventory path (recorded relative to ``data/``)."""
    rel = inventory_path.replace("\\", "/")
    if not rel.startswith("data/"):
        rel = f"data/{rel}"
    return REPO_ROOT / rel


# v002-terminal window modes that mean "referenced but NOT read" (safe).
_V002_SAFE_REFERENCE_MODES = frozenset(
    {"by_reference", "by_reference_only", "excluded", "none", ""}
)
_KNOWN_BINANCE_USDM_MARKETS = frozenset(
    {"usdm_futures", "binance_usdm_futures", "binance-usdm-futures", "um", "usdⓈ-m"}
)


def _market(manifest: dict[str, Any]) -> str:
    market = manifest.get("market")
    if isinstance(market, str) and market.lower() in _KNOWN_BINANCE_USDM_MARKETS:
        return contract.MARKET
    return str(market)


def _source_family(manifest: dict[str, Any]) -> str:
    fam = manifest.get("data_family") or manifest.get("source_family")
    if isinstance(fam, str) and fam.lower() in ("aggtrades", "aggtrade"):
        return contract.SOURCE_FAMILY
    return str(fam)


def _contains_v002_terminal(manifest: dict[str, Any]) -> bool:
    mode = str(manifest.get("v002_terminal_window_mode", "")).lower()
    return mode not in _V002_SAFE_REFERENCE_MODES


@dataclass(frozen=True)
class SourceBinding:
    """Verified feature + long-horizon label source binding."""

    normalized_manifest_sha256: str
    feature_manifest_sha256: str
    feature_config_hash: str
    normalized_gate_report_sha256: str
    feature_gate_report_sha256: str
    label_config_hash: str
    label_family: str
    label_manifest_sha256: str
    feature_manifest: dict[str, Any]
    label_manifest: dict[str, Any]


def _require(actual: str, expected: str, *, label: str) -> None:
    if actual != expected:
        raise LongHorizonMlDatasetRunError(
            f"{label} mismatch: expected {expected!r}, got {actual!r}"
        )


def verify_feature_source_binding() -> tuple[str, str, str, str, str, dict[str, Any]]:
    """Verify the committed normalized + feature manifest / gate hashes.

    Verifies the four committed witnesses (normalized manifest / gate, feature
    manifest / gate) against the imported Phase 4bn-AH contract constants, rejects
    the v002-terminal ``819cfa7a…`` feature config hash, and confirms the feature
    manifest source-scope. The **label** side is verified independently against the
    AN long-horizon manifest in :func:`verify_label_source_binding` — this dataset
    binds NO 15s label family. Returns ``(norm_m_sha, feat_m_sha, feat_config_hash,
    norm_g_sha, feat_g_sha, feature_manifest)``.
    """
    norm_m_sha = sha256_file(REPO_ROOT / NORMALIZED_MANIFEST_PATH)
    feat_m_sha = sha256_file(REPO_ROOT / FEATURE_MANIFEST_PATH)
    norm_g_sha = sha256_file(REPO_ROOT / NORMALIZED_GATE_PATH)
    feat_g_sha = sha256_file(REPO_ROOT / FEATURE_GATE_PATH)

    feature_manifest = _load_json(FEATURE_MANIFEST_PATH)
    feature_config_hash = str(feature_manifest["feature_config_hash"])

    _require(
        norm_m_sha,
        contract.EXPECTED_NORMALIZED_MANIFEST_SHA256,
        label="normalized manifest_sha256",
    )
    _require(
        norm_g_sha,
        contract.EXPECTED_NORMALIZED_GATE_REPORT_SHA256,
        label="normalized gate_report_sha256",
    )
    _require(
        feat_m_sha,
        contract.EXPECTED_FEATURE_MANIFEST_SHA256,
        label="feature manifest_sha256",
    )
    _require(
        feat_g_sha,
        contract.EXPECTED_FEATURE_GATE_REPORT_SHA256,
        label="feature gate_report_sha256",
    )
    # Reject the v002-terminal-bound feature config identity before accepting.
    if feature_config_hash == contract.REJECTED_V002_FEATURE_CONFIG_HASH or (
        feature_config_hash.startswith(
            contract.REJECTED_V002_FEATURE_CONFIG_HASH_PREFIX
        )
    ):
        raise LongHorizonMlDatasetRunError(
            "feature_config_hash is the rejected v002-terminal identity"
        )
    _require(
        feature_config_hash,
        contract.EXPECTED_FEATURE_CONFIG_HASH,
        label="feature_config_hash",
    )

    # Feature manifest source-scope defence-in-depth.
    fm = feature_manifest
    manifest_like = {
        "symbol": fm.get("symbol"),
        "market": _market(fm),
        "source_family": _source_family(fm),
        "start_date": fm.get("date_start"),
        "end_date": fm.get("date_end"),
        "feature_partition_count": int(fm.get("date_count", -1)),
        "row_count": int(fm.get("actual_feature_row_count", fm.get("total_row_count", -1))),
        "contains_v002_terminal": _contains_v002_terminal(fm),
        "contains_sealed_test": bool(fm.get("sealed_test_split_touched")),
        "full_envelope": bool(fm.get("full_envelope")),
        "private_source": False,
        "authenticated_source": False,
        "external_source": False,
    }
    builder.validate_source_scope(manifest_like)
    return norm_m_sha, feat_m_sha, feature_config_hash, norm_g_sha, feat_g_sha, fm


def verify_label_source_binding(feature_manifest_sha256: str) -> tuple[dict[str, Any], str]:
    """Verify the AN long-horizon label manifest binds to this feature source.

    Fails closed unless the AN manifest declares the long-horizon family, the
    frozen ``label_config_hash edaeafde…`` (and NOT the rejected v002/short-horizon
    hashes), the 5m/30m/1h horizons, the 275-date / 400,001,695-row pre-v002
    segment, and the SAME feature-manifest SHA the committed feature source
    verified to. Returns ``(label_manifest, label_manifest_sha256)``.
    """
    label_manifest_sha = sha256_file(REPO_ROOT / LABEL_MANIFEST_PATH)
    lm = _load_json(LABEL_MANIFEST_PATH)
    identity = lm.get("identity", {})
    binding = lm.get("source_binding", {})

    family = str(identity.get("dataset_family"))
    if family != contract.LABEL_FAMILY:
        raise LongHorizonMlDatasetRunError(
            f"label family {family!r} != {contract.LABEL_FAMILY!r}"
        )
    lch = str(identity.get("label_config_hash"))
    if lch != contract.LABEL_CONFIG_HASH:
        raise LongHorizonMlDatasetRunError(
            f"label_config_hash {lch!r} != expected {contract.LABEL_CONFIG_HASH!r}"
        )
    if lch in (
        contract.REJECTED_V002_LABEL_CONFIG_HASH,
        contract.REJECTED_SHORT_HORIZON_LABEL_CONFIG_HASH,
    ):
        raise LongHorizonMlDatasetRunError(
            "label_config_hash is a rejected out-of-scope identity"
        )
    horizons = tuple(identity.get("horizons", ()))
    if horizons != contract.HORIZONS:
        raise LongHorizonMlDatasetRunError(
            f"label horizons {horizons!r} != {contract.HORIZONS!r}"
        )
    if int(binding.get("date_count", -1)) != contract.EXPECTED_PARTITION_COUNT:
        raise LongHorizonMlDatasetRunError("label date_count must be 275")
    if int(binding.get("total_row_count", -1)) != contract.EXPECTED_ROW_COUNT:
        raise LongHorizonMlDatasetRunError(
            f"label total_row_count must be {contract.EXPECTED_ROW_COUNT}"
        )
    bound_feat_sha = str(binding.get("source_feature_manifest_sha256"))
    if bound_feat_sha != feature_manifest_sha256:
        raise LongHorizonMlDatasetRunError(
            "AN label manifest source_feature_manifest_sha256 does not match the "
            "verified committed feature-manifest SHA (feature/label sources diverge)"
        )
    if str(binding.get("feature_config_hash")) != contract.EXPECTED_FEATURE_CONFIG_HASH:
        raise LongHorizonMlDatasetRunError(
            "AN label manifest feature_config_hash mismatch"
        )
    return lm, label_manifest_sha


@dataclass(frozen=True)
class PartitionRef:
    """One verified feature+long-horizon-label partition reference for a date."""

    date: str
    split: str
    feature_parquet: Path
    label_parquet: Path
    feature_sha256: str
    label_sha256: str
    row_count: int


def verify_per_parquet_sidecars_and_inventory(
    binding_feature_manifest: dict[str, Any],
    label_manifest: dict[str, Any],
    *,
    progress: bool = False,
) -> list[PartitionRef]:
    """Verify all 275 feature + 275 long-horizon label Parquet against inventory.

    For every date, verifies (a) the feature Parquet SHA against the feature
    manifest inventory + on-disk sidecar, (b) the long-horizon label Parquet SHA
    against the AN manifest inventory + on-disk sidecar, (c) the AN-recorded
    ``paired_source_feature_parquet_sha256`` equals the feature manifest SHA
    (feature ↔ label cross-binding), (d) equal per-day row counts, and (e) the
    AN-recorded split equals the deterministic split-policy assignment. Returns the
    ordered, verified partition references (embargo dates included).
    """
    feat_inv = {
        str(e["date"]): e for e in binding_feature_manifest["per_file_inventory"]
    }
    lab_inv = {str(e["date"]): e for e in label_manifest["per_day_inventory"]}
    if len(feat_inv) != 275 or len(lab_inv) != 275:
        raise LongHorizonMlDatasetRunError(
            f"partition counts must be 275/275, got {len(feat_inv)}/{len(lab_inv)}"
        )

    seg = split_policy.segment_dates()
    if set(feat_inv) != set(seg) or set(lab_inv) != set(seg):
        raise LongHorizonMlDatasetRunError(
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

        # Cross-binding: the AN label partition was built against exactly this
        # feature partition (fail closed if the paired feature SHA diverges).
        paired = str(le["paired_source_feature_parquet_sha256"])
        if paired != str(fe["feature_parquet_sha256"]):
            raise LongHorizonMlDatasetRunError(
                f"{date_str}: AN paired feature sha {paired[:12]}… != feature "
                f"inventory sha {str(fe['feature_parquet_sha256'])[:12]}…"
            )

        f_rows = int(fe["row_count"])
        l_rows = int(le["row_count"])
        if f_rows != l_rows:
            raise LongHorizonMlDatasetRunError(
                f"{date_str}: feature rows {f_rows} != label rows {l_rows}"
            )

        policy_split = split_policy.split_for_date(date_str)
        an_split = str(le.get("split"))
        if an_split != policy_split:
            raise LongHorizonMlDatasetRunError(
                f"{date_str}: AN split {an_split!r} != policy split {policy_split!r}"
            )

        refs.append(
            PartitionRef(
                date=date_str,
                split=policy_split,
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
        raise LongHorizonMlDatasetRunError(f"missing {layer} parquet {parquet_path}")
    sidecar_path = parquet_path.with_name(parquet_path.name + ".sha256")
    if not sidecar_path.is_file():
        raise LongHorizonMlDatasetRunError(f"missing {layer} sidecar {sidecar_path}")
    sidecar_sha, sidecar_name = parse_sidecar(
        sidecar_path.read_text(encoding="utf-8")
    )
    if sidecar_name != parquet_path.name:
        raise LongHorizonMlDatasetRunError(
            f"{layer} sidecar name {sidecar_name!r} != {parquet_path.name!r}"
        )
    actual = sha256_file(parquet_path)
    if actual != inventory_sha:
        raise LongHorizonMlDatasetRunError(
            f"{layer} {parquet_path.name}: sha {actual[:12]}… != inventory "
            f"{inventory_sha[:12]}…"
        )
    if actual != sidecar_sha:
        raise LongHorizonMlDatasetRunError(
            f"{layer} {parquet_path.name}: sha {actual[:12]}… != sidecar "
            f"{sidecar_sha[:12]}…"
        )


def _git(args: list[str]) -> str:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip() or "unknown"
    except (subprocess.SubprocessError, OSError):
        return "unknown"


def split_authority_commit_sha() -> str:
    """Return the git commit SHA that last touched the split-policy module."""
    module_rel = "src/prometheus/research/microstructure/pre_v002_split_policy.py"
    return _git(["log", "-1", "--format=%H", "--", module_rel])


def bind_split_authority() -> str:
    """Confirm the split-policy identity + arithmetic; return its commit SHA."""
    if split_policy.SPLIT_POLICY_NAME != (
        "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"
    ):
        raise LongHorizonMlDatasetRunError("split policy name mismatch")
    split_policy.validate_policy_arithmetic()
    return split_authority_commit_sha()


# ---------------------------------------------------------------------------
# Streaming column readers / accumulators
# ---------------------------------------------------------------------------

_ALIGNMENT_KEYS = list(contract.ALIGNMENT_KEYS)  # row_index, agg_trade_id, ft_ms, stt_ms
_FEATURE_KEY_COLS = [*_ALIGNMENT_KEYS, "utc_date"]

_LABEL_READ_COLS = [
    *_ALIGNMENT_KEYS,
    "utc_date",
    contract.LABEL_INVALID_PRICE_FLAG,
    *[contract.DIRECTION_COLUMN_BY_HORIZON[h] for h in contract.HORIZONS],
    *[contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h] for h in contract.HORIZONS],
    *[contract.REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON[h] for h in contract.HORIZONS],
]

# Per-horizon drop reasons (per-horizon precedence: invalid → censored → null_dir).
HORIZON_DROP_REASONS: tuple[str, ...] = (
    "invalid_price",
    "censored",
    "null_direction",
)

# Later-split boundary each earlier model split's forward target must not reach.
_EARLIER_SPLIT_BOUNDARY_MS: dict[str, int] = {
    split_policy.TRAIN: split_policy.BOUNDARY_TRAIN_VALIDATION_MS,
    split_policy.VALIDATION: split_policy.BOUNDARY_VALIDATION_HOLDOUT_MS,
}


def _col_to_float64(table: pa.Table, name: str) -> np.ndarray[Any, Any]:
    """Return a float64 numpy array for column *name*, casting strings/bools."""
    col = table.column(name)
    casted = pc.cast(col, "float64")
    return np.asarray(casted.to_numpy(zero_copy_only=False), dtype=np.float64)


@dataclass
class _FeatureStats:
    """Streaming train-only accumulators for one feature column."""

    count: int = 0
    nan_count: int = 0
    total: float = 0.0
    total_sq: float = 0.0

    def update(self, arr: np.ndarray[Any, Any]) -> None:
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


def _empty_horizon_accounting() -> dict[str, int]:
    return {
        "valid_target": 0,
        "censored": 0,
        "null_direction": 0,
        "invalid_price": 0,
        "class_-1": 0,
        "class_0": 0,
        "class_1": 0,
    }


@dataclass
class _RunAccumulators:
    """All streaming accumulators for the single run."""

    feature_stats: dict[str, _FeatureStats] = field(default_factory=dict)
    per_date: list[dict[str, object]] = field(default_factory=list)
    split_raw_rows: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    split_invalid_rows: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    # per (split, horizon) -> accounting dict
    split_horizon: dict[str, dict[str, dict[str, int]]] = field(default_factory=dict)
    month_split_rows: dict[str, dict[str, int]] = field(default_factory=dict)
    boundary_crossings: dict[str, int] = field(default_factory=dict)
    alignment_rows_checked: int = 0
    alignment_mismatches: int = 0
    train_primary_valid_rows: int = 0
    test_rows_loaded: int = 0

    def __post_init__(self) -> None:
        for col in contract.ALLOWED_FEATURE_COLUMNS:
            self.feature_stats[col] = _FeatureStats()
        for sp in split_policy.MODEL_ELIGIBLE_SPLITS:
            self.split_horizon[sp] = {
                h: _empty_horizon_accounting() for h in contract.HORIZONS
            }
        for sp in (split_policy.TRAIN, split_policy.VALIDATION):
            for h in contract.HORIZONS:
                self.boundary_crossings[f"{sp}:{h}"] = 0


def _check_alignment_vectorized(
    ftab: pa.Table, ltab: pa.Table, date_str: str
) -> int:
    """Fail closed unless the 4 keys + utc_date match element-wise; return rows."""
    n_f = int(ftab.num_rows)
    n_l = int(ltab.num_rows)
    if n_f != n_l:
        raise LongHorizonMlDatasetRunError(
            f"{date_str}: feature rows {n_f} != label rows {n_l}"
        )
    for key in _ALIGNMENT_KEYS:
        fa = ftab.column(key).to_numpy(zero_copy_only=False)
        la = ltab.column(key).to_numpy(zero_copy_only=False)
        if not np.array_equal(fa, la):
            raise LongHorizonMlDatasetRunError(
                f"{date_str}: alignment key {key!r} mismatch"
            )
    fu = ftab.column("utc_date").to_numpy(zero_copy_only=False)
    lu = ltab.column("utc_date").to_numpy(zero_copy_only=False)
    if not np.array_equal(fu, lu):
        raise LongHorizonMlDatasetRunError(f"{date_str}: utc_date mismatch")
    return n_f


def _bool_col(table: pa.Table, name: str) -> np.ndarray[Any, Any]:
    return np.asarray(
        table.column(name).to_numpy(zero_copy_only=False)
    ).astype(bool)


def _process_partition(ref: PartitionRef, acc: _RunAccumulators) -> None:
    """Stream one partition: verify alignment, per-horizon account, fit train."""
    split = ref.split
    if split not in split_policy.ALL_SPLITS:
        raise LongHorizonMlDatasetRunError(f"{ref.date}: unexpected split {split!r}")

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
        # Embargo dates are dropped in full; no per-horizon accounting / stats.
        acc.per_date.append(
            {
                "date": ref.date,
                "split": split,
                "raw_row_count": n,
                "per_horizon": {
                    h: {"embargo_dropped": n} for h in contract.HORIZONS
                },
            }
        )
        return

    invalid = _bool_col(ltab, contract.LABEL_INVALID_PRICE_FLAG)
    acc.split_invalid_rows[split] += int(invalid.sum())

    per_date_horizon: dict[str, dict[str, int]] = {}
    keep_by_horizon: dict[str, np.ndarray[Any, Any]] = {}

    for h in contract.HORIZONS:
        dir_col = ltab.column(contract.DIRECTION_COLUMN_BY_HORIZON[h])
        dir_null = np.asarray(dir_col.is_null().to_numpy(zero_copy_only=False))
        dir_vals = np.asarray(
            pc.fill_null(dir_col, -2).to_numpy(zero_copy_only=False)
        )
        censored = _bool_col(ltab, contract.CENSORED_FLAG_COLUMN_BY_HORIZON[h])

        drop_invalid = invalid
        drop_censored = censored & ~drop_invalid
        drop_null_dir = dir_null & ~drop_invalid & ~drop_censored
        keep = ~(drop_invalid | drop_censored | drop_null_dir)
        keep_by_horizon[h] = keep

        hacc = acc.split_horizon[split][h]
        kept = int(keep.sum())
        hacc["valid_target"] += kept
        hacc["censored"] += int(drop_censored.sum())
        hacc["null_direction"] += int(drop_null_dir.sum())
        hacc["invalid_price"] += int(drop_invalid.sum())
        kept_dir = dir_vals[keep]
        hacc["class_-1"] += int((kept_dir == -1).sum())
        hacc["class_0"] += int((kept_dir == 0).sum())
        hacc["class_1"] += int((kept_dir == 1).sum())

        per_date_horizon[h] = {
            "valid_target": kept,
            "censored": int(drop_censored.sum()),
            "null_direction": int(drop_null_dir.sum()),
            "invalid_price": int(drop_invalid.sum()),
        }

        # Earlier-model-split boundary crossing proof (train / validation only).
        if split in _EARLIER_SPLIT_BOUNDARY_MS:
            boundary = _EARLIER_SPLIT_BOUNDARY_MS[split]
            ref_col = ltab.column(contract.REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON[h])
            ref_null = np.asarray(ref_col.is_null().to_numpy(zero_copy_only=False))
            ref_vals = np.asarray(
                pc.fill_null(ref_col, -1).to_numpy(zero_copy_only=False)
            )
            crossings = int(((~ref_null) & (ref_vals >= boundary)).sum())
            acc.boundary_crossings[f"{split}:{h}"] += crossings

    acc.per_date.append(
        {
            "date": ref.date,
            "split": split,
            "raw_row_count": n,
            "invalid_price_rows": int(invalid.sum()),
            "per_horizon": per_date_horizon,
        }
    )

    # Train-only transform fitting over primary-target (5m) valid rows.
    if read_feature_matrix:
        primary_keep = keep_by_horizon[contract.PRIMARY_HORIZON]
        keep_idx = np.nonzero(primary_keep)[0]
        acc.train_primary_valid_rows += int(keep_idx.size)
        for col in contract.ALLOWED_FEATURE_COLUMNS:
            arr = _col_to_float64(ftab, col)
            acc.feature_stats[col].update(arr[keep_idx])


# ---------------------------------------------------------------------------
# Run proof (real) — reuses the skeleton conservative-posture validator
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BuilderRunProof:
    """Real Phase 4bn-AQ run proof: conservative sections + real IO fields."""

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
    label_family: str
    label_config_hash: str
    output_namespace_path: str
    output_namespace_created: bool
    no_data_io: bool  # False for the real run (it reads data)
    per_horizon_boundary_crossing_rows: dict[str, int] = field(default_factory=dict)


def _conservative_mirror(rp: BuilderRunProof) -> proof.DatasetBuilderProof:
    """Build a skeleton-shaped proof mirroring the conservative sections."""
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
    """Fail closed unless *rp* encodes a valid, conservative, budget-safe run."""
    # 1. Conservative posture via the existing skeleton path.
    proof.validate_dataset_builder_proof(_conservative_mirror(rp))

    # 2. Real budget preflight must have run, measured disk, and passed.
    b = rp.budget_preflight
    if b.is_placeholder or not b.ran_preflight or not b.measured_disk:
        raise LongHorizonMlDatasetRunError(
            "run proof budget preflight must be real, run, and disk-measured"
        )
    if not b.passed or b.breaches:
        raise LongHorizonMlDatasetRunError(
            f"run proof budget preflight did not pass: {b.breaches!r}"
        )
    if b.d_free_gib_before < D_DRIVE_MIN_FREE_GIB_BEFORE:
        raise LongHorizonMlDatasetRunError(
            "run proof records D: free below 500 GiB floor"
        )

    # 3. Real IO fields: reads data and creates the namespace exactly once.
    if rp.no_data_io is not False:
        raise LongHorizonMlDatasetRunError("run proof no_data_io must be False (reads)")
    if rp.output_namespace_created is not True:
        raise LongHorizonMlDatasetRunError(
            "run proof output_namespace_created must be True"
        )
    if rp.output_namespace_path != OUTPUT_NAMESPACE + "/":
        raise LongHorizonMlDatasetRunError("run proof output namespace path mismatch")

    # 4. Long-horizon label binding.
    if rp.label_family != contract.LABEL_FAMILY:
        raise LongHorizonMlDatasetRunError("run proof label_family mismatch")
    if rp.label_config_hash != contract.LABEL_CONFIG_HASH:
        raise LongHorizonMlDatasetRunError("run proof label_config_hash mismatch")

    # 5. Per-horizon boundary crossings must be zero.
    if any(v != 0 for v in rp.per_horizon_boundary_crossing_rows.values()):
        raise LongHorizonMlDatasetRunError(
            f"per-horizon boundary crossings must be zero: "
            f"{rp.per_horizon_boundary_crossing_rows!r}"
        )
    if rp.split.test_rows_loaded != 0:
        raise LongHorizonMlDatasetRunError("run proof test_rows_loaded must be 0")
    if rp.alignment.mismatched_rows != 0:
        raise LongHorizonMlDatasetRunError("run proof alignment mismatches must be 0")


def feature_list_hash(
    columns: tuple[str, ...] = contract.ALLOWED_FEATURE_COLUMNS,
) -> str:
    """Return the SHA256 of the canonical-ordered 45-column feature list."""
    return hashlib.sha256("\n".join(columns).encode("utf-8")).hexdigest()


def dataset_contract_hash() -> str:
    """Return a deterministic identity hash over the dataset contract binding."""
    payload = {
        "dataset_family": contract.DATASET_FAMILY,
        "contract_name": contract.CONTRACT_NAME,
        "contract_version": contract.CONTRACT_VERSION,
        "amendment_id": contract.CONTRACT_AMENDMENT_ID,
        "feature_count": contract.FEATURE_COUNT,
        "feature_list_hash": feature_list_hash(),
        "feature_config_hash": contract.EXPECTED_FEATURE_CONFIG_HASH,
        "feature_manifest_sha256": contract.EXPECTED_FEATURE_MANIFEST_SHA256,
        "label_family": contract.LABEL_FAMILY,
        "label_config_hash": contract.LABEL_CONFIG_HASH,
        "horizons": list(contract.HORIZONS),
        "primary_target": contract.PRIMARY_TARGET,
        "secondary_targets": list(contract.SECONDARY_TARGETS),
        "split_policy_name": contract.SPLIT_POLICY_NAME,
        "standardization_rule": contract.STANDARDIZATION_RULE,
        "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def run(
    *,
    output_namespace: str = OUTPUT_NAMESPACE,
    progress: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Execute the single controlled data-reading build; return a summary dict.

    Fails closed (raising :class:`LongHorizonMlDatasetRunError`) on any pre-read,
    alignment, split, boundary, budget, or output violation, writing nothing on
    failure. With ``dry_run=True``, performs the full source-binding pre-read
    verification (manifests, gates, 550 sidecars, cross-binding) but reads no
    feature/label rows and writes nothing. On a full success it writes the compact
    dataset artefacts + Phase 4bb-F sidecars inside *output_namespace* only.
    """
    t0 = time.monotonic()
    out_dir = REPO_ROOT / output_namespace

    # One-run guard: refuse to overwrite a completed build.
    manifest_path = out_dir / "dataset_manifest.json"
    if manifest_path.exists():
        raise LongHorizonMlDatasetRunError(
            "dataset already built at this namespace; a rerun requires separate "
            "operator authorization (no safe idempotent overwrite is defined)"
        )

    # --- Budget preflight (before any write; D: >= 500 GiB) ---
    d_free_before = measure_d_free_gib()
    preflight = evaluate_budget_preflight(d_free_before)
    if not preflight.passed:
        raise LongHorizonMlDatasetRunError(
            f"budget preflight failed closed: {preflight.breaches!r}"
        )

    # --- Pre-read checks (before any feature/label row read) ---
    if progress:
        print("[pre-read] verifying feature + normalized manifest/gate hashes…", flush=True)
    (
        norm_m_sha,
        feat_m_sha,
        feat_config_hash,
        norm_g_sha,
        feat_g_sha,
        feature_manifest,
    ) = verify_feature_source_binding()
    if progress:
        print("[pre-read] verifying long-horizon label source binding…", flush=True)
    label_manifest, label_manifest_sha = verify_label_source_binding(feat_m_sha)
    split_commit = bind_split_authority()

    binding = SourceBinding(
        normalized_manifest_sha256=norm_m_sha,
        feature_manifest_sha256=feat_m_sha,
        feature_config_hash=feat_config_hash,
        normalized_gate_report_sha256=norm_g_sha,
        feature_gate_report_sha256=feat_g_sha,
        label_config_hash=contract.LABEL_CONFIG_HASH,
        label_family=contract.LABEL_FAMILY,
        label_manifest_sha256=label_manifest_sha,
        feature_manifest=feature_manifest,
        label_manifest=label_manifest,
    )

    if progress:
        print("[pre-read] verifying 550 per-parquet sidecars + cross-binding…", flush=True)
    refs = verify_per_parquet_sidecars_and_inventory(
        feature_manifest, label_manifest, progress=progress
    )
    if len(refs) != 275:
        raise LongHorizonMlDatasetRunError(f"expected 275 partitions, got {len(refs)}")

    if dry_run:
        elapsed = time.monotonic() - t0
        summary = {
            "phase": RUN_PHASE,
            "mode": "dry_run",
            "contract_name": contract.CONTRACT_NAME,
            "partitions_verified": len(refs),
            "feature_manifest_sha256": feat_m_sha,
            "label_manifest_sha256": label_manifest_sha,
            "label_config_hash": contract.LABEL_CONFIG_HASH,
            "budget_preflight_passed": preflight.passed,
            "d_free_gib_before": preflight.d_free_gib_before,
            "output_namespace": OUTPUT_NAMESPACE + "/",
            "output_written": False,
            "elapsed_seconds": round(elapsed, 1),
        }
        if progress:
            print(f"[dry-run done] {json.dumps(summary, indent=2)}", flush=True)
        return summary

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
        raise LongHorizonMlDatasetRunError(
            f"streamed row total {total_rows} != expected "
            f"{contract.EXPECTED_ROW_COUNT}"
        )

    # --- Assemble the leakage / split-integrity proof ---
    # Skeleton FilteringProof shape: {split: {reason: count}} — use the primary
    # (5m) horizon accounting so the conservative validator's imputation check
    # runs over the decision horizon.
    dropped_by_split_and_reason = {
        sp: {
            "invalid_price": acc.split_horizon[sp][contract.PRIMARY_HORIZON][
                "invalid_price"
            ],
            "censored": acc.split_horizon[sp][contract.PRIMARY_HORIZON]["censored"],
            "null_direction": acc.split_horizon[sp][contract.PRIMARY_HORIZON][
                "null_direction"
            ],
        }
        for sp in split_policy.MODEL_ELIGIBLE_SPLITS
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
        label_family=contract.LABEL_FAMILY,
        label_config_hash=contract.LABEL_CONFIG_HASH,
        output_namespace_path=OUTPUT_NAMESPACE + "/",
        output_namespace_created=True,
        no_data_io=False,
        per_horizon_boundary_crossing_rows=dict(acc.boundary_crossings),
    )

    # Validate BEFORE writing anything (pre-write gate).
    validate_builder_run_proof(run_proof)

    # --- Write artefacts (only now; only inside the namespace) ---
    assert_budget_during()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = _write_artefacts(
        out_dir, binding, acc, run_proof, split_commit, feat_m_sha, label_manifest_sha
    )

    elapsed = time.monotonic() - t0
    summary = {
        "phase": RUN_PHASE,
        "contract_name": contract.CONTRACT_NAME,
        "dataset_family": contract.DATASET_FAMILY,
        "output_namespace": OUTPUT_NAMESPACE + "/",
        "total_rows": total_rows,
        "split_raw_rows": dict(acc.split_raw_rows),
        "train_primary_valid_rows": acc.train_primary_valid_rows,
        "per_split_horizon_support": {
            sp: {h: acc.split_horizon[sp][h]["valid_target"] for h in contract.HORIZONS}
            for sp in split_policy.MODEL_ELIGIBLE_SPLITS
        },
        "per_horizon_boundary_crossing_rows": dict(acc.boundary_crossings),
        "test_rows_loaded": acc.test_rows_loaded,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
        "budget_preflight_passed": run_proof.budget_preflight.passed,
        "d_free_gib_before": run_proof.budget_preflight.d_free_gib_before,
        "elapsed_seconds": round(elapsed, 1),
        "artefacts": written,
        "split_policy_commit_sha": split_commit,
        "feature_list_hash": flh,
        "label_config_hash": contract.LABEL_CONFIG_HASH,
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
    feat_m_sha: str,
    label_manifest_sha: str,
) -> dict[str, str]:
    """Write the compact dataset artefacts + Phase 4bb-F sidecars; return shas."""
    repo_sha = _git(["rev-parse", "HEAD"])
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    flh = run_proof.active_feature_list_hash
    contract_hash = dataset_contract_hash()

    # 1. train-only transform statistics (fit on the train split only).
    per_feature: dict[str, dict[str, Any]] = {}
    for col in contract.ALLOWED_FEATURE_COLUMNS:
        mean, std = acc.feature_stats[col].mean_std()
        denom = max(std, contract.STANDARDIZATION_EPSILON)
        per_feature[col] = {
            "train_mean": mean,
            "train_std": std,
            "standardization_denominator": denom,
            "train_count": acc.feature_stats[col].count,
            "train_null_count": acc.feature_stats[col].nan_count,
        }
    transform = {
        "fit_split": "train",
        "fit_row_selection": (
            "train_split_rows_valid_for_primary_target_forward_direction_5m"
        ),
        "train_primary_valid_rows": acc.train_primary_valid_rows,
        "standardization_rule": contract.STANDARDIZATION_RULE,
        "standardization_epsilon": contract.STANDARDIZATION_EPSILON,
        "imputation_rule": contract.IMPUTATION_RULE,
        "imputation_fill_value": contract.IMPUTATION_FILL_VALUE,
        "standardize_boolean_flags": contract.STANDARDIZE_BOOLEAN_FLAGS,
        "feature_count": contract.FEATURE_COUNT,
        "feature_list": list(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": flh,
        "per_feature": per_feature,
    }

    # 2. split index (per-date split + per-horizon support/censoring).
    split_index = {
        "split_policy_name": split_policy.SPLIT_POLICY_NAME,
        "split_policy_module_path": contract.SPLIT_POLICY_MODULE_PATH,
        "split_policy_commit_sha": split_commit,
        "horizons": list(contract.HORIZONS),
        "per_date": acc.per_date,
    }

    month_block = {m: dict(sp) for m, sp in sorted(acc.month_split_rows.items())}

    per_split_horizon = {
        sp: {h: dict(acc.split_horizon[sp][h]) for h in contract.HORIZONS}
        for sp in split_policy.MODEL_ELIGIBLE_SPLITS
    }

    # 3. source binding.
    source_binding = {
        "repo_commit_sha": repo_sha,
        "branch": branch,
        "ap_preregistration_state": (
            "LONGHORIZON_ML_BASELINE_PREREGISTRATION_MERGED_TO_MAIN"
        ),
        "feature_source": {
            "feature_family": "microstructure_features_aggtrades_v001",
            "feature_manifest_sha256": feat_m_sha,
            "feature_config_hash": binding.feature_config_hash,
            "feature_gate_report_sha256": binding.feature_gate_report_sha256,
            "normalized_manifest_sha256": binding.normalized_manifest_sha256,
            "normalized_gate_report_sha256": binding.normalized_gate_report_sha256,
            "feature_count": contract.FEATURE_COUNT,
            "feature_list_hash": flh,
            "feature_list": list(contract.ALLOWED_FEATURE_COLUMNS),
        },
        "label_source": {
            "label_family": contract.LABEL_FAMILY,
            "label_family_contract_name": contract.LABEL_FAMILY_CONTRACT_NAME,
            "label_config_hash": contract.LABEL_CONFIG_HASH,
            "label_manifest_sha256": label_manifest_sha,
            "horizons": list(contract.HORIZONS),
            "horizon_ms": list(contract.HORIZON_MS),
            "primary_target": contract.PRIMARY_TARGET,
            "secondary_targets": list(contract.SECONDARY_TARGETS),
            "cross_binding": (
                "per_date_an_paired_source_feature_parquet_sha256_"
                "equals_feature_manifest_inventory_sha256"
            ),
        },
        "split_policy_name": contract.SPLIT_POLICY_NAME,
        "transform_policy": contract.STANDARDIZATION_RULE,
        "dataset_contract_hash": contract_hash,
    }

    # 4. leakage / split / integrity proof.
    proof_payload = _proof_to_json(run_proof)
    proof_payload["strict_alignment_keys"] = [
        *contract.ALIGNMENT_KEYS,
        "utc_date",
    ]
    proof_payload["alignment_rows_checked"] = acc.alignment_rows_checked
    proof_payload["alignment_mismatches"] = acc.alignment_mismatches
    proof_payload["per_horizon_censored_targets_excluded_without_imputation"] = True
    proof_payload["embargo_rows_used_in_model_splits"] = 0
    proof_payload["v002_terminal_window_read"] = False
    proof_payload["sealed_test_split_touched"] = False
    proof_payload["test_rows_loaded"] = 0
    proof_payload["data_committed"] = False
    proof_payload["frozen_v002_family_mutated"] = False
    proof_payload["longhorizon_label_family_mutated"] = False
    proof_payload["ah_dataset_namespace_mutated"] = False
    proof_payload["forbidden_feature_scan_clean"] = (
        len(builder.find_forbidden_columns(contract.ALLOWED_FEATURE_COLUMNS)) == 0
    )
    proof_payload["dataset_contract_hash"] = contract_hash

    # 5. dataset manifest.
    dataset_manifest = {
        "dataset_family": contract.DATASET_FAMILY,
        "dataset_name": contract.CONTRACT_NAME,
        "dataset_version": DATASET_VERSION,
        "contract_version": contract.CONTRACT_VERSION,
        "amendment_id": contract.CONTRACT_AMENDMENT_ID,
        "phase": RUN_PHASE,
        "sibling_short_horizon_contract": contract.SIBLING_SHORT_HORIZON_CONTRACT,
        "symbol": contract.SYMBOL,
        "market": contract.MARKET,
        "source_family": contract.SOURCE_FAMILY,
        "segment_start_date": contract.START_DATE,
        "segment_end_date": contract.END_DATE,
        "expected_row_count": contract.EXPECTED_ROW_COUNT,
        "streamed_row_count": acc.alignment_rows_checked,
        "primary_target": contract.PRIMARY_TARGET,
        "primary_horizon_ms": contract.PRIMARY_HORIZON_MS,
        "secondary_targets": list(contract.SECONDARY_TARGETS),
        "horizons": list(contract.HORIZONS),
        "horizon_ms": list(contract.HORIZON_MS),
        "target_classes": list(contract.TARGET_CLASSES),
        "feature_count": contract.FEATURE_COUNT,
        "feature_list": list(contract.ALLOWED_FEATURE_COLUMNS),
        "feature_list_hash": flh,
        "dataset_contract_hash": contract_hash,
        "source_bindings": {
            "normalized_manifest_sha256": binding.normalized_manifest_sha256,
            "feature_manifest_sha256": feat_m_sha,
            "feature_config_hash": binding.feature_config_hash,
            "normalized_gate_report_sha256": binding.normalized_gate_report_sha256,
            "feature_gate_report_sha256": binding.feature_gate_report_sha256,
            "label_family": contract.LABEL_FAMILY,
            "label_config_hash": contract.LABEL_CONFIG_HASH,
            "label_manifest_sha256": label_manifest_sha,
        },
        "split_raw_rows": dict(acc.split_raw_rows),
        "split_invalid_rows": dict(acc.split_invalid_rows),
        "per_split_horizon_support": per_split_horizon,
        "month_block_split_rows": month_block,
        "train_primary_valid_rows": acc.train_primary_valid_rows,
        "decision_block_units": list(contract.DECISION_BLOCK_UNITS),
        "metric_granularities": list(contract.METRIC_GRANULARITIES),
        "row_level_metrics_descriptive_only": (
            contract.ROW_LEVEL_METRICS_DESCRIPTIVE_ONLY
        ),
        "dependence_caveat": (
            "aggTrades long-horizon (5m/30m/1h) forward labels overlap heavily; "
            "rows are NOT independent; per-row metrics are descriptive only and "
            "per-row significance language is forbidden (Phase 4bn-AE Option 1). "
            "Cost reference 8 bps/side / 16 bps round-trip is descriptive only; "
            "this dataset expresses no tradability / PnL / edge."
        ),
        "decimation_stride": contract.DECIMATION_STRIDE,
        "decimation_policy": contract.DECIMATION_POLICY,
        "non_authorization_flags": contract.NON_AUTHORIZATION_FLAGS,
        "no_models": True,
        "no_predictions": True,
        "no_metrics": True,
        "test_rows_loaded": 0,
        "v002_terminal_window_read": False,
        "sealed_test_split_touched": False,
    }

    written: dict[str, str] = {}
    ordered: tuple[tuple[str, dict[str, Any]], ...] = (
        ("train_only_transform.json", transform),
        ("split_index.json", split_index),
        ("source_binding.json", source_binding),
        ("leakage_split_integrity_proof.json", proof_payload),
        ("dataset_manifest.json", dataset_manifest),
    )
    for name, payload in ordered:
        digest, _ = write_json_with_sidecar(out_dir / name, payload)
        written[name] = digest

    # 6. build run record.
    build_run_record = {
        "phase": RUN_PHASE,
        "contract_name": contract.CONTRACT_NAME,
        "output_namespace_rel": OUTPUT_NAMESPACE + "/",
        "repo_commit_sha": repo_sha,
        "branch": branch,
        "streamed_row_count": acc.alignment_rows_checked,
        "budget_preflight_passed": run_proof.budget_preflight.passed,
        "d_free_gib_before": run_proof.budget_preflight.d_free_gib_before,
        "no_data_committed": True,
    }
    digest, _ = write_json_with_sidecar(
        out_dir / "build_run_record.json", build_run_record
    )
    written["build_run_record.json"] = digest

    # 7. sidecar inventory (over the produced artefacts + their sidecars).
    inventory = {
        "phase": RUN_PHASE,
        "output_namespace_rel": OUTPUT_NAMESPACE + "/",
        "artefact_count": len(written),
        "entries": [
            {
                "artefact": name,
                "artefact_sha256": digest,
                "sidecar": f"{name}.sha256",
            }
            for name, digest in sorted(written.items())
        ],
    }
    inv_digest, _ = write_json_with_sidecar(
        out_dir / "sidecar_inventory.json", inventory
    )
    written["sidecar_inventory.json"] = inv_digest
    return written


def _proof_to_json(rp: BuilderRunProof) -> dict[str, Any]:
    return {
        "phase": RUN_PHASE,
        "contract_name": rp.contract_name,
        "amendment_id": rp.amendment_id,
        "dataset_family": contract.DATASET_FAMILY,
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
        "label_family": rp.label_family,
        "label_config_hash": rp.label_config_hash,
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
    "HORIZON_DROP_REASONS",
    "LABEL_MANIFEST_PATH",
    "LongHorizonMlDatasetRunError",
    "OUTPUT_NAMESPACE",
    "PartitionRef",
    "RealBudgetPreflight",
    "SourceBinding",
    "assert_budget_during",
    "bind_split_authority",
    "dataset_contract_hash",
    "evaluate_budget_preflight",
    "feature_list_hash",
    "main",
    "measure_d_free_gib",
    "parse_sidecar",
    "run",
    "sha256_file",
    "sidecar_line",
    "split_authority_commit_sha",
    "validate_builder_run_proof",
    "verify_feature_source_binding",
    "verify_label_source_binding",
    "verify_per_parquet_sidecars_and_inventory",
    "write_json_with_sidecar",
]
