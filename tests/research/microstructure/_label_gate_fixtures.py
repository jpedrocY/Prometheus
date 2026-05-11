"""Shared mini-fixture helpers for the Phase 4bj-E label-family
eligibility-gate tests.

Builds a self-consistent label parquet + label manifest pair under a
pytest ``tmp_path / "data" / "microstructure" / ...`` tree by chaining:

1. ``_labels_fixtures.build_normalized_table`` + ``build_feature_table``
   to produce a tiny aligned normalized parquet and feature parquet;
2. ``compute_aggtrade_labels_v001`` (real Phase 4bj-C label kernel) to
   produce the 39-column label table;
3. ``write_label_dataset_v001`` (real labels_io atomic writer) to
   produce the label parquet + paired SHA256 sidecar;
4. ``build_label_manifest_v001`` (real label manifest builder) to
   produce the JSON manifest;
5. ``atomic_write_label_manifest`` + ``write_label_sha256_sidecar``
   (real label-manifest atomic writers) to produce the manifest +
   paired sidecar.

The fixture uses **synthetic** lineage SHAs, not the production-locked
Phase 4bj-C constants. As a result, Group F SHA-equality checks (label
parquet SHA, label manifest SHA, lineage SHAs, label_config_hash) and
Group G/H/L expected-count checks (which compare against the locked
1,681,098-row, BTCUSDT 2025-01-15 production constants) FAIL on the
fixture by design. The orchestrator MUST still:

- run every check without raising,
- write a single gate report + paired SHA256 sidecar under
  ``data/microstructure/gate-reports/labels/`` (and only there),
- never mutate the label parquet, label manifest, or source artefact,
- record ``research_eligible_after = False`` and
  ``no_successor_authorization = True`` invariants on the report,
- aggregate counts correctly,
- expose the result via :class:`LabelGateResult`.

These fixtures never touch the real ``data/microstructure/`` tree.
They never call any endpoint, never use credentials, and never write
anywhere outside *tmp_path*.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from prometheus.research.microstructure import (
    LabelLineage,
    atomic_write_label_manifest,
    build_label_config_hash,
    build_label_manifest_v001,
    compute_aggtrade_labels_v001,
    derive_label_manifest_output_path,
    derive_label_output_path,
    write_label_dataset_v001,
    write_label_sha256_sidecar,
)

from ._labels_fixtures import (
    build_feature_table,
    build_normalized_table,
)

# Synthetic 64-char lowercase hex SHAs distinct from the Phase 4bj-C
# production-locked constants. These intentionally do NOT match the
# Phase 4bj-E gate's expected SHAs so that the SHA-equality and
# expected-count checks FAIL on the fixture by design.
SYNTH_FEATURE_PARQUET_SHA = "a" * 64
SYNTH_FEATURE_MANIFEST_SHA = "b" * 64
SYNTH_FEATURE_SUCCESSOR_STATE_SHA = "c" * 64
SYNTH_PHASE_4BI_B_GATE_REPORT_SHA = "d" * 64
SYNTH_NORMALIZED_PARQUET_SHA = "e" * 64


@dataclass(frozen=True)
class LabelGateFixtureBundle:
    """Complete Phase 4bj-E mini-fixture under *tmp_path*."""

    tmp_root: Path
    microstructure_root: Path
    labels_root: Path
    manifests_root: Path
    output_root: Path
    repo_root: Path
    label_parquet_path: Path
    label_parquet_sidecar_path: Path
    label_manifest_path: Path
    label_manifest_sidecar_path: Path
    feature_parquet_path: Path
    feature_manifest_path: Path
    label_parquet_sha: str
    label_manifest_sha: str
    feature_parquet_sha: str
    feature_manifest_sha: str
    label_config_hash: str
    row_count: int
    code_commit_sha: str


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _default_transact_times() -> list[int]:
    # 12 events with monotonic timestamps and a same-timestamp pair to
    # exercise the tie-break path. The kernel's label censoring only
    # depends on these timestamps; the actual values are arbitrary.
    return [
        1_736_899_205_109,
        1_736_899_205_500,
        1_736_899_206_109,
        1_736_899_207_000,
        1_736_899_210_000,
        1_736_899_210_000,  # same-timestamp tie
        1_736_899_212_000,
        1_736_899_215_000,
        1_736_899_230_000,
        1_736_899_260_000,
        1_736_899_300_000,
        1_736_899_400_000,
    ]


def _default_prices() -> list[str]:
    return [
        "96514.9",
        "96515.0",
        "96515.1",
        "96514.8",
        "96516.0",
        "96516.1",
        "96515.5",
        "96517.0",
        "96514.0",
        "96518.0",
        "96513.0",
        "96520.0",
    ]


def build_label_gate_fixture(
    tmp_path: Path,
    *,
    symbol: str = "BTCUSDT",
    utc_date: str = "2025-01-15",
    code_commit_sha: str = "0" * 40,
) -> LabelGateFixtureBundle:
    """Build a complete Phase 4bj-E label-family gate fixture.

    All outputs live under *tmp_path*. No real ``data/microstructure/``
    write occurs. The fixture's SHAs do not match the production-locked
    Phase 4bj-C constants.
    """
    repo_root = tmp_path
    microstructure_root = tmp_path / "data" / "microstructure"
    labels_root = microstructure_root / "labels"
    manifests_root = microstructure_root / "manifests"
    labels_root.mkdir(parents=True, exist_ok=True)
    manifests_root.mkdir(parents=True, exist_ok=True)

    # 1. Build tiny normalized and feature tables.
    transact_time_ms = _default_transact_times()
    prices = _default_prices()
    normalized = build_normalized_table(
        transact_time_ms=transact_time_ms,
        prices=prices,
        symbol=symbol,
        utc_date=utc_date,
    )
    feature_tbl = build_feature_table(normalized=normalized)

    # 2. Write the source feature parquet and a minimal manifest sidecar
    #    so K* / I* / J* checks can run against real on-disk feature data.
    feature_parquet_path = labels_root.parent / "features" / (
        f"microstructure_features_aggtrades_v001/{symbol}/2025/01/"
        f"{symbol}-features-aggtrades-{utc_date}.parquet"
    )
    feature_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(feature_tbl, feature_parquet_path)
    feature_manifest_path = (
        manifests_root / "microstructure_features_aggtrades_v001__v001.json"
    )
    feature_manifest_path.write_text(
        '{\n  "dataset_family": "microstructure_features_aggtrades_v001",\n'
        '  "version": "v001"\n}\n',
        encoding="utf-8",
    )

    # 3. Build the deterministic label_config_hash using the synthetic
    #    lineage SHAs that match what the manifest will carry.
    label_config_hash = build_label_config_hash(
        source_feature_manifest_sha256=SYNTH_FEATURE_MANIFEST_SHA,
        source_feature_parquet_sha256=SYNTH_FEATURE_PARQUET_SHA,
        source_feature_successor_state_sha256=SYNTH_FEATURE_SUCCESSOR_STATE_SHA,
        source_phase_4bi_b_gate_report_sha256=SYNTH_PHASE_4BI_B_GATE_REPORT_SHA,
    )

    # 4. Run the real Phase 4bj-C label kernel.
    lineage = LabelLineage(
        source_feature_manifest_sha256=SYNTH_FEATURE_MANIFEST_SHA,
        source_feature_parquet_sha256=SYNTH_FEATURE_PARQUET_SHA,
        source_feature_successor_state_sha256=SYNTH_FEATURE_SUCCESSOR_STATE_SHA,
        source_phase_4bi_b_gate_report_sha256=SYNTH_PHASE_4BI_B_GATE_REPORT_SHA,
        source_normalized_parquet_sha256=SYNTH_NORMALIZED_PARQUET_SHA,
        label_config_hash=label_config_hash,
    )
    label_table, summary = compute_aggtrade_labels_v001(
        feature_table=feature_tbl,
        normalized_table=normalized,
        symbol=symbol,
        utc_date=utc_date,
        lineage=lineage,
    )

    # 5. Write the label parquet + paired SHA256 sidecar atomically.
    label_parquet_path = derive_label_output_path(
        output_root=labels_root, symbol=symbol, utc_date=utc_date
    )
    label_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    written_path, label_sha, label_size, sidecar_path, _sidecar_sha = (
        write_label_dataset_v001(
            table=label_table,
            output_path=label_parquet_path,
            write_sha256_sidecar=True,
        )
    )
    assert sidecar_path is not None, "fixture expects sidecar to be written"

    # 6. Build and write the label manifest + paired sidecar.
    rel_path = (
        f"labels/microstructure_labels_aggtrades_v001/{symbol}/"
        f"{utc_date.split('-')[0]}/{utc_date.split('-')[1]}/"
        f"{symbol}-labels-aggtrades-{utc_date}.parquet"
    )
    manifest = build_label_manifest_v001(
        symbol=symbol,
        utc_date=utc_date,
        label_parquet_relative_path=rel_path,
        label_parquet_sha256=label_sha,
        label_parquet_size_bytes=label_size,
        row_count=label_table.num_rows,
        label_config_hash=label_config_hash,
        source_feature_manifest_sha256=SYNTH_FEATURE_MANIFEST_SHA,
        source_feature_parquet_sha256=SYNTH_FEATURE_PARQUET_SHA,
        source_feature_successor_state_sha256=SYNTH_FEATURE_SUCCESSOR_STATE_SHA,
        source_phase_4bi_b_gate_report_sha256=SYNTH_PHASE_4BI_B_GATE_REPORT_SHA,
        source_normalized_parquet_sha256=SYNTH_NORMALIZED_PARQUET_SHA,
        invalid_price_row_count=summary.invalid_price_row_count,
        censored_per_horizon=summary.censored_per_horizon,
        code_commit_sha=code_commit_sha,
        created_at_unix_ms=1_700_000_000_000,
    )
    label_manifest_path = derive_label_manifest_output_path(
        manifests_root=manifests_root
    )
    manifest_sha, _ = atomic_write_label_manifest(
        label_manifest_path, manifest, refuse_overwrite=True
    )
    label_manifest_sidecar_path = label_manifest_path.with_suffix(
        label_manifest_path.suffix + ".sha256"
    )
    write_label_sha256_sidecar(
        label_manifest_sidecar_path,
        target_filename=label_manifest_path.name,
        sha256_hex=manifest_sha,
        refuse_overwrite=True,
    )

    output_root = microstructure_root

    return LabelGateFixtureBundle(
        tmp_root=tmp_path,
        microstructure_root=microstructure_root,
        labels_root=labels_root,
        manifests_root=manifests_root,
        output_root=output_root,
        repo_root=repo_root,
        label_parquet_path=written_path,
        label_parquet_sidecar_path=sidecar_path,
        label_manifest_path=label_manifest_path,
        label_manifest_sidecar_path=label_manifest_sidecar_path,
        feature_parquet_path=feature_parquet_path,
        feature_manifest_path=feature_manifest_path,
        label_parquet_sha=_hash_file(written_path),
        label_manifest_sha=_hash_file(label_manifest_path),
        feature_parquet_sha=_hash_file(feature_parquet_path),
        feature_manifest_sha=_hash_file(feature_manifest_path),
        label_config_hash=label_config_hash,
        row_count=label_table.num_rows,
        code_commit_sha=code_commit_sha,
    )


__all__ = [
    "SYNTH_FEATURE_MANIFEST_SHA",
    "SYNTH_FEATURE_PARQUET_SHA",
    "SYNTH_FEATURE_SUCCESSOR_STATE_SHA",
    "SYNTH_NORMALIZED_PARQUET_SHA",
    "SYNTH_PHASE_4BI_B_GATE_REPORT_SHA",
    "LabelGateFixtureBundle",
    "build_label_gate_fixture",
]


def _arrange(table: pa.Table) -> pa.Table:
    """Re-arrange columns; unused but kept for symmetry with sibling fixtures."""
    return table
