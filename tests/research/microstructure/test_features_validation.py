"""Phase 4bh tests: features_validation.validate_feature_dataset."""

from __future__ import annotations

import json

import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import (
    FEATURE_SCHEMA_V001,
    FeatureCheckStatus,
    FeatureLineage,
    atomic_write_feature_manifest,
    build_feature_config,
    build_feature_manifest,
    compute_aggtrades_features,
    read_normalized_parquet,
    validate_feature_dataset,
    write_feature_dataset,
    write_feature_sha256_sidecar,
)
from prometheus.research.microstructure.features_validation import (
    FeatureValidationError,
)

from ._features_fixtures import (
    SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
    build_feature_fixture,
)


def _build_and_write(tmp_path):
    bundle = build_feature_fixture(tmp_path)
    src, parquet_sha, _ = read_normalized_parquet(bundle.normalized_parquet_path)
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
    feat = compute_aggtrades_features(
        source_table=src, config=cfg, lineage=lineage
    )
    out, parquet_sha_out, parquet_size, sidecar, _ = write_feature_dataset(
        table=feat,
        output_path=bundle.feature_parquet_path,
        write_sha256_sidecar=True,
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
        row_count=feat.num_rows,
        feature_config_hash=cfg.feature_config_hash,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=SYNTHETIC_PHASE_4BF_GATE_REPORT_SHA,
        code_commit_sha="0" * 40,
        created_at_unix_ms=1_700_000_000_000,
    )
    manifest_sha, _ = atomic_write_feature_manifest(
        bundle.feature_manifest_path, manifest, refuse_overwrite=True
    )
    sidecar_path = bundle.feature_manifest_path.with_suffix(
        bundle.feature_manifest_path.suffix + ".sha256"
    )
    write_feature_sha256_sidecar(
        sidecar_path,
        target_filename=bundle.feature_manifest_path.name,
        sha256_hex=manifest_sha,
        refuse_overwrite=True,
    )
    return bundle, cfg, lineage, parquet_sha


def test_validate_feature_dataset_returns_pass(tmp_path) -> None:
    bundle, cfg, lineage, parquet_sha = _build_and_write(tmp_path)
    result = validate_feature_dataset(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=lineage.source_phase_4bf_gate_report_sha256,
        feature_config_hash=cfg.feature_config_hash,
    )
    failures = [c for c in result.checks if c.status != FeatureCheckStatus.PASS]
    assert failures == []
    assert result.overall_status == FeatureCheckStatus.PASS


def test_validate_detects_sidecar_mismatch(tmp_path) -> None:
    bundle, cfg, lineage, parquet_sha = _build_and_write(tmp_path)
    sidecar = bundle.feature_parquet_path.with_suffix(
        bundle.feature_parquet_path.suffix + ".sha256"
    )
    sidecar.write_text("0" * 64 + "  bogus.parquet\n", encoding="ascii")
    result = validate_feature_dataset(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=lineage.source_phase_4bf_gate_report_sha256,
        feature_config_hash=cfg.feature_config_hash,
    )
    failed_ids = {c.check_id for c in result.checks if c.status != FeatureCheckStatus.PASS}
    assert "4bh.parquet.sidecar_matches" in failed_ids


def test_validate_detects_manifest_research_eligible_true(tmp_path) -> None:
    bundle, cfg, lineage, parquet_sha = _build_and_write(tmp_path)
    text = bundle.feature_manifest_path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    parsed["research_eligible"] = True
    bundle.feature_manifest_path.write_text(
        json.dumps(parsed, sort_keys=True, indent=2), encoding="utf-8"
    )
    # Update sidecar to match new bytes so we don't fail at sidecar check.
    import hashlib as _hashlib

    new_sha = _hashlib.sha256(bundle.feature_manifest_path.read_bytes()).hexdigest()
    sidecar = bundle.feature_manifest_path.with_suffix(
        bundle.feature_manifest_path.suffix + ".sha256"
    )
    sidecar.write_text(
        f"{new_sha}  {bundle.feature_manifest_path.name}\n", encoding="ascii"
    )
    result = validate_feature_dataset(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=lineage.source_phase_4bf_gate_report_sha256,
        feature_config_hash=cfg.feature_config_hash,
    )
    ids = {c.check_id for c in result.checks if c.status != FeatureCheckStatus.PASS}
    assert "4bh.manifest.research_eligible_false" in ids


def test_validate_missing_parquet_raises(tmp_path) -> None:
    bundle = build_feature_fixture(tmp_path)
    with pytest.raises(FeatureValidationError):
        validate_feature_dataset(
            feature_parquet_path=tmp_path / "missing.parquet",
            feature_manifest_path=bundle.feature_manifest_path,
            source_normalized_parquet_path=bundle.normalized_parquet_path,
            source_normalized_manifest_sha256="a" * 64,
            source_normalized_parquet_sha256="b" * 64,
            source_successor_state_sha256="c" * 64,
            source_phase_4bf_gate_report_sha256="d" * 64,
            feature_config_hash="e" * 64,
        )


def test_validate_detects_row_count_mismatch(tmp_path) -> None:
    bundle, cfg, lineage, parquet_sha = _build_and_write(tmp_path)
    text = bundle.feature_manifest_path.read_text(encoding="utf-8")
    parsed = json.loads(text)
    parsed["row_count"] = parsed["row_count"] + 1
    bundle.feature_manifest_path.write_text(
        json.dumps(parsed, sort_keys=True, indent=2), encoding="utf-8"
    )
    import hashlib as _hashlib

    new_sha = _hashlib.sha256(bundle.feature_manifest_path.read_bytes()).hexdigest()
    sidecar = bundle.feature_manifest_path.with_suffix(
        bundle.feature_manifest_path.suffix + ".sha256"
    )
    sidecar.write_text(
        f"{new_sha}  {bundle.feature_manifest_path.name}\n", encoding="ascii"
    )
    result = validate_feature_dataset(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=lineage.source_phase_4bf_gate_report_sha256,
        feature_config_hash=cfg.feature_config_hash,
    )
    ids = {c.check_id for c in result.checks if c.status != FeatureCheckStatus.PASS}
    assert "4bh.row_count.parquet_eq_manifest" in ids


def test_round_trip_parquet_and_manifest_pair_validates(tmp_path) -> None:
    bundle, cfg, lineage, parquet_sha = _build_and_write(tmp_path)
    # Confirm column order survives parquet round-trip.
    re_read = pq.read_table(bundle.feature_parquet_path)
    assert tuple(re_read.column_names) == FEATURE_SCHEMA_V001
    result = validate_feature_dataset(
        feature_parquet_path=bundle.feature_parquet_path,
        feature_manifest_path=bundle.feature_manifest_path,
        source_normalized_parquet_path=bundle.normalized_parquet_path,
        source_normalized_manifest_sha256=bundle.normalized_manifest_sha256,
        source_normalized_parquet_sha256=parquet_sha,
        source_successor_state_sha256=bundle.successor_state_sha256,
        source_phase_4bf_gate_report_sha256=lineage.source_phase_4bf_gate_report_sha256,
        feature_config_hash=cfg.feature_config_hash,
    )
    assert result.overall_status == FeatureCheckStatus.PASS
