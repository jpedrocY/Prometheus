"""Shared mini-fixture helpers for the Phase 4bi-B feature-family
eligibility-gate tests.

Builds a Phase 4bh feature mini-fixture using the existing
:mod:`tests.research.microstructure._features_fixtures` helpers, then
runs the Phase 4bh feature kernel to produce a feature parquet +
feature manifest, and finally writes a small Phase 4bd-shaped raw
manifest (so the gate can read it). All artefacts live under a pytest
``tmp_path / "data" / "microstructure"`` tree.

These fixtures never touch the real ``data/microstructure/`` tree.
They never call any endpoint, never use credentials, and never write
anywhere outside *tmp_path*.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from prometheus.research.microstructure import (
    FeatureLineage,
    atomic_write_feature_manifest,
    build_feature_config,
    build_feature_manifest,
    compute_aggtrades_features,
    read_normalized_parquet,
    write_feature_dataset,
    write_feature_sha256_sidecar,
)

from ._features_fixtures import (
    SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
    FeatureFixtureBundle,
    build_feature_fixture,
)

SYNTHETIC_RAW_ZIP_SHA = "f" * 64
SYNTHETIC_RAW_MANIFEST_SHA_PLACEHOLDER = "9" * 64
SYNTHETIC_PHASE_4BB_D_GATE_REPORT_SHA = "8" * 64


@dataclass(frozen=True)
class FeatureGateFixtureBundle:
    """Complete Phase 4bi-B mini-fixture under *tmp_path*."""

    feature_bundle: FeatureFixtureBundle
    feature_parquet_path: Path
    feature_parquet_sidecar_path: Path
    feature_manifest_path: Path
    feature_manifest_sidecar_path: Path
    feature_parquet_sha: str
    feature_manifest_sha: str
    raw_manifest_path: Path
    raw_manifest_sha: str
    output_root: Path
    repo_root: Path
    code_commit_sha: str
    feature_config_hash: str


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_raw_manifest(path: Path) -> None:
    """Write a minimal Phase 4az-shaped raw manifest with the lineage
    flags the Phase 4bi-B gate reads via Group L."""
    payload = {
        "dataset_family": "microstructure_raw_aggtrades_v001",
        "version": "v001",
        "symbol": "BTCUSDT",
        "research_eligible": False,
        "eligibility_gate_status": "pending",
        "files": [
            {
                "path": (
                    "raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/"
                    "BTCUSDT-aggTrades-2025-01-15.zip"
                ),
                "sha256": SYNTHETIC_RAW_ZIP_SHA,
            }
        ],
        "governance_labels": {
            "phase": "4az",
            "stop_trigger_domain": "trade_price_backtest_candidate",
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")


def build_feature_gate_fixture(
    tmp_path: Path,
    *,
    symbol: str = "BTCUSDT",
    utc_date: str = "2025-01-15",
    rows: Sequence[dict[str, Any]] | None = None,
    code_commit_sha: str = "0" * 40,
) -> FeatureGateFixtureBundle:
    """Build a complete Phase 4bi-B feature-family gate fixture.

    Steps:

    1. Build the underlying Phase 4bh feature fixture (normalized
       parquet + normalized manifest + Phase 4bg-B successor-state).
    2. Run the Phase 4bh feature kernel against the normalized parquet
       to produce a feature parquet + paired SHA256 sidecar.
    3. Build and write a feature manifest + paired SHA256 sidecar.
    4. Write a small Phase 4az-shaped raw manifest.
    5. Return paths and SHAs that the Phase 4bi-B gate orchestrator
       can consume directly via :class:`FeatureGateInput`.
    """
    bundle = build_feature_fixture(tmp_path, symbol=symbol, utc_date=utc_date, rows=rows)

    # Read normalized parquet via the public reader (also returns the
    # parquet SHA computed during the read).
    src_table, parquet_sha, _ = read_normalized_parquet(
        bundle.normalized_parquet_path
    )
    cfg = build_feature_config(
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_path=bundle.normalized_manifest_path,
        source_successor_state_path=bundle.successor_state_path,
        output_feature_parquet_path=bundle.feature_parquet_path,
        output_feature_manifest_path=bundle.feature_manifest_path,
    )
    lineage = FeatureLineage(
        source_normalized_parquet_sha256=parquet_sha,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        feature_config_hash=cfg.feature_config_hash,
    )
    feat_table = compute_aggtrades_features(
        source_table=src_table, config=cfg, lineage=lineage
    )
    _path, parquet_sha_out, parquet_size, _sidecar, _ = write_feature_dataset(
        table=feat_table,
        output_path=bundle.feature_parquet_path,
        write_sha256_sidecar=True,
    )

    feature_parquet_sidecar_path = bundle.feature_parquet_path.with_suffix(
        bundle.feature_parquet_path.suffix + ".sha256"
    )

    rel_path = (
        f"features/microstructure_features_aggtrades_v001/{bundle.symbol}/"
        f"{bundle.utc_date.split('-', 1)[0]}/{bundle.utc_date.split('-')[1]}/"
        f"{bundle.symbol}-features-aggtrades-{bundle.utc_date}.parquet"
    )
    manifest = build_feature_manifest(
        symbol=bundle.symbol,
        utc_date=bundle.utc_date,
        feature_parquet_relative_path=rel_path,
        feature_parquet_sha256=parquet_sha_out,
        feature_parquet_size_bytes=parquet_size,
        row_count=feat_table.num_rows,
        feature_config_hash=cfg.feature_config_hash,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        code_commit_sha=code_commit_sha,
        created_at_unix_ms=1_700_000_000_000,
    )
    manifest_sha, _ = atomic_write_feature_manifest(
        bundle.feature_manifest_path, manifest, refuse_overwrite=True
    )
    feature_manifest_sidecar_path = bundle.feature_manifest_path.with_suffix(
        bundle.feature_manifest_path.suffix + ".sha256"
    )
    write_feature_sha256_sidecar(
        feature_manifest_sidecar_path,
        target_filename=bundle.feature_manifest_path.name,
        sha256_hex=manifest_sha,
        refuse_overwrite=True,
    )

    # Raw manifest sibling (Phase 4az-shaped, minimal)
    raw_manifest_path = (
        bundle.manifests_root / "microstructure_raw_aggtrades_v001__v001.json"
    )
    _write_raw_manifest(raw_manifest_path)
    raw_manifest_sha = _hash_file(raw_manifest_path)

    feature_parquet_sha = _hash_file(bundle.feature_parquet_path)
    feature_manifest_sha = _hash_file(bundle.feature_manifest_path)

    output_root = bundle.microstructure_root
    repo_root = tmp_path

    return FeatureGateFixtureBundle(
        feature_bundle=bundle,
        feature_parquet_path=bundle.feature_parquet_path,
        feature_parquet_sidecar_path=feature_parquet_sidecar_path,
        feature_manifest_path=bundle.feature_manifest_path,
        feature_manifest_sidecar_path=feature_manifest_sidecar_path,
        feature_parquet_sha=feature_parquet_sha,
        feature_manifest_sha=feature_manifest_sha,
        raw_manifest_path=raw_manifest_path,
        raw_manifest_sha=raw_manifest_sha,
        output_root=output_root,
        repo_root=repo_root,
        code_commit_sha=code_commit_sha,
        feature_config_hash=cfg.feature_config_hash,
    )


__all__ = [
    "SYNTHETIC_PHASE_4BB_D_GATE_REPORT_SHA",
    "SYNTHETIC_RAW_MANIFEST_SHA_PLACEHOLDER",
    "SYNTHETIC_RAW_ZIP_SHA",
    "FeatureGateFixtureBundle",
    "build_feature_gate_fixture",
]
