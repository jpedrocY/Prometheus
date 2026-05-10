"""Phase 4bj-C label validation tests (synthetic fixtures only)."""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure.labels_compute import (
    LabelLineage,
    compute_aggtrade_labels_v001,
)
from prometheus.research.microstructure.labels_io import (
    atomic_write_label_manifest,
    atomic_write_label_parquet,
    write_label_sha256_sidecar,
)
from prometheus.research.microstructure.labels_manifest import (
    build_label_manifest_v001,
)
from prometheus.research.microstructure.labels_schema import (
    LABEL_HORIZONS_V001,
    build_label_config_hash,
)
from prometheus.research.microstructure.labels_validation import (
    LabelCheckStatus,
    LabelValidationError,
    iter_failures,
    to_summary_dict,
    validate_label_dataset_v001,
)

from ._labels_fixtures import build_feature_table, build_normalized_table


def _hash_path(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _build_full_artefacts(
    tmp_path: Path,
    *,
    feat_timestamps: list[int],
    feat_prices: list[str],
) -> dict[str, Path]:
    norm = build_normalized_table(
        transact_time_ms=feat_timestamps,
        prices=feat_prices,
    )
    feat = build_feature_table(normalized=norm)

    norm_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "normalized"
        / "microstructure_normalized_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-aggTrades-2025-01-15.parquet"
    )
    feat_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "features"
        / "microstructure_features_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-features-aggtrades-2025-01-15.parquet"
    )
    feat_manifest_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "manifests"
        / "microstructure_features_aggtrades_v001__v001.json"
    )
    norm_path.parent.mkdir(parents=True, exist_ok=True)
    feat_path.parent.mkdir(parents=True, exist_ok=True)
    feat_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(norm, norm_path)
    pq.write_table(feat, feat_path)
    feat_manifest_path.write_text(
        json.dumps({"dataset_family": "microstructure_features_aggtrades_v001"}),
        encoding="utf-8",
    )

    src_feat_manifest_sha = _hash_path(feat_manifest_path)
    src_feat_parquet_sha = _hash_path(feat_path)
    src_feat_successor_sha = "a" * 64
    src_phase_4bi_b_sha = "b" * 64
    src_norm_parquet_sha = _hash_path(norm_path)

    label_config_hash = build_label_config_hash(
        source_feature_manifest_sha256=src_feat_manifest_sha,
        source_feature_parquet_sha256=src_feat_parquet_sha,
        source_feature_successor_state_sha256=src_feat_successor_sha,
        source_phase_4bi_b_gate_report_sha256=src_phase_4bi_b_sha,
    )
    lineage = LabelLineage(
        source_feature_manifest_sha256=src_feat_manifest_sha,
        source_feature_parquet_sha256=src_feat_parquet_sha,
        source_feature_successor_state_sha256=src_feat_successor_sha,
        source_phase_4bi_b_gate_report_sha256=src_phase_4bi_b_sha,
        source_normalized_parquet_sha256=src_norm_parquet_sha,
        label_config_hash=label_config_hash,
    )

    table, summary = compute_aggtrade_labels_v001(
        feature_table=feat,
        normalized_table=norm,
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        lineage=lineage,
    )

    label_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "labels"
        / "microstructure_labels_aggtrades_v001"
        / "BTCUSDT"
        / "2025"
        / "01"
        / "BTCUSDT-labels-aggtrades-2025-01-15.parquet"
    )
    parquet_sha, parquet_size = atomic_write_label_parquet(label_path, table)
    parquet_sidecar = label_path.with_suffix(label_path.suffix + ".sha256")
    write_label_sha256_sidecar(
        parquet_sidecar,
        target_filename=label_path.name,
        sha256_hex=parquet_sha,
    )

    label_manifest_path = (
        tmp_path
        / "data"
        / "microstructure"
        / "manifests"
        / "microstructure_labels_aggtrades_v001__v001.json"
    )
    manifest_dict = build_label_manifest_v001(
        symbol="BTCUSDT",
        utc_date="2025-01-15",
        label_parquet_relative_path=label_path.as_posix(),
        label_parquet_sha256=parquet_sha,
        label_parquet_size_bytes=parquet_size,
        row_count=table.num_rows,
        label_config_hash=label_config_hash,
        source_feature_manifest_sha256=src_feat_manifest_sha,
        source_feature_parquet_sha256=src_feat_parquet_sha,
        source_feature_successor_state_sha256=src_feat_successor_sha,
        source_phase_4bi_b_gate_report_sha256=src_phase_4bi_b_sha,
        source_normalized_parquet_sha256=src_norm_parquet_sha,
        invalid_price_row_count=summary.invalid_price_row_count,
        censored_per_horizon=summary.censored_per_horizon,
    )
    manifest_sha, _ = atomic_write_label_manifest(label_manifest_path, manifest_dict)
    manifest_sidecar = label_manifest_path.with_suffix(
        label_manifest_path.suffix + ".sha256"
    )
    write_label_sha256_sidecar(
        manifest_sidecar,
        target_filename=label_manifest_path.name,
        sha256_hex=manifest_sha,
    )
    return {
        "label_parquet": label_path,
        "label_manifest": label_manifest_path,
        "feature_parquet": feat_path,
        "feature_manifest": feat_manifest_path,
        "normalized_parquet": norm_path,
        "src_feat_manifest_sha": src_feat_manifest_sha,
        "src_feat_parquet_sha": src_feat_parquet_sha,
        "src_feat_successor_sha": src_feat_successor_sha,
        "src_phase_4bi_b_sha": src_phase_4bi_b_sha,
        "src_norm_parquet_sha": src_norm_parquet_sha,
        "label_config_hash": label_config_hash,
    }


def test_happy_path_validates(tmp_path: Path) -> None:
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000, 3_000, 80_000],
        feat_prices=["100", "110", "120", "130"],
    )
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bundle["src_feat_manifest_sha"],
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bundle["label_config_hash"],
    )
    failures = list(iter_failures(result))
    assert failures == []
    assert result.overall_status == LabelCheckStatus.PASS
    summary = to_summary_dict(result)
    assert summary["checks_fail"] == 0


def test_schema_mismatch_caught(tmp_path: Path) -> None:
    # Build legit artefacts.
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000],
        feat_prices=["100", "200"],
    )
    # Overwrite the parquet with a column added at the end (bypass writer
    # discipline by using pyarrow directly to a fresh path, then swap).
    table = pq.read_table(bundle["label_parquet"])
    extra = pa.array([0, 0], type=pa.int64())
    bad = table.append_column(pa.field("forbidden_pnl_col", pa.int64()), extra)
    bundle["label_parquet"].unlink()
    pq.write_table(bad, bundle["label_parquet"])
    # Resync sidecar so we exercise the schema check (not the sidecar check).
    new_sha = _hash_path(bundle["label_parquet"])
    sidecar = bundle["label_parquet"].with_suffix(
        bundle["label_parquet"].suffix + ".sha256"
    )
    sidecar.write_text(f"{new_sha}  {bundle['label_parquet'].name}\n", encoding="ascii")
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bundle["src_feat_manifest_sha"],
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bundle["label_config_hash"],
    )
    assert result.overall_status == LabelCheckStatus.FAIL
    ids = {c.check_id for c in result.checks if c.status == LabelCheckStatus.FAIL}
    assert "4bj-c.parquet.column_order_matches" in ids
    assert "4bj-c.parquet.no_forbidden_substrings" in ids


def test_row_count_mismatch_caught(tmp_path: Path) -> None:
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000],
        feat_prices=["100", "200"],
    )
    # Manually rewrite the label manifest to claim a different row count.
    raw = json.loads(bundle["label_manifest"].read_text(encoding="utf-8"))
    raw["row_count"] = 99
    bundle["label_manifest"].unlink()
    manifest_sha, _ = atomic_write_label_manifest(bundle["label_manifest"], raw)
    sidecar = bundle["label_manifest"].with_suffix(
        bundle["label_manifest"].suffix + ".sha256"
    )
    sidecar.unlink()
    write_label_sha256_sidecar(
        sidecar,
        target_filename=bundle["label_manifest"].name,
        sha256_hex=manifest_sha,
    )
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bundle["src_feat_manifest_sha"],
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bundle["label_config_hash"],
    )
    assert result.overall_status == LabelCheckStatus.FAIL
    ids = {c.check_id for c in result.checks if c.status == LabelCheckStatus.FAIL}
    assert "4bj-c.row_count.parquet_eq_manifest" in ids


def test_lineage_sha_mismatch_caught(tmp_path: Path) -> None:
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000],
        feat_prices=["100", "200"],
    )
    bad_expected_feat_manifest_sha = "f" * 64
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bad_expected_feat_manifest_sha,
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bundle["label_config_hash"],
    )
    assert result.overall_status == LabelCheckStatus.FAIL
    ids = {c.check_id for c in result.checks if c.status == LabelCheckStatus.FAIL}
    assert "4bj-c.manifest.source_feature_manifest_sha256_matches" in ids


def test_label_config_hash_mismatch_caught(tmp_path: Path) -> None:
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000],
        feat_prices=["100", "200"],
    )
    bad_hash = "e" * 64
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bundle["src_feat_manifest_sha"],
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bad_hash,
    )
    assert result.overall_status == LabelCheckStatus.FAIL
    ids = {c.check_id for c in result.checks if c.status == LabelCheckStatus.FAIL}
    assert "4bj-c.manifest.label_config_hash_matches" in ids


def test_research_eligible_true_in_manifest_is_caught(tmp_path: Path) -> None:
    bundle = _build_full_artefacts(
        tmp_path,
        feat_timestamps=[1_000, 2_000],
        feat_prices=["100", "200"],
    )
    raw = json.loads(bundle["label_manifest"].read_text(encoding="utf-8"))
    raw["research_eligible"] = True
    raw["eligibility_gate_status"] = "pass"
    bundle["label_manifest"].unlink()
    manifest_sha, _ = atomic_write_label_manifest(bundle["label_manifest"], raw)
    sidecar = bundle["label_manifest"].with_suffix(
        bundle["label_manifest"].suffix + ".sha256"
    )
    sidecar.unlink()
    write_label_sha256_sidecar(
        sidecar,
        target_filename=bundle["label_manifest"].name,
        sha256_hex=manifest_sha,
    )
    result = validate_label_dataset_v001(
        label_parquet_path=bundle["label_parquet"],
        label_manifest_path=bundle["label_manifest"],
        feature_parquet_path=bundle["feature_parquet"],
        feature_manifest_path=bundle["feature_manifest"],
        normalized_parquet_path=bundle["normalized_parquet"],
        source_feature_manifest_sha256=bundle["src_feat_manifest_sha"],
        source_feature_parquet_sha256=bundle["src_feat_parquet_sha"],
        source_feature_successor_state_sha256=bundle["src_feat_successor_sha"],
        source_phase_4bi_b_gate_report_sha256=bundle["src_phase_4bi_b_sha"],
        source_normalized_parquet_sha256=bundle["src_norm_parquet_sha"],
        expected_label_config_hash=bundle["label_config_hash"],
    )
    assert result.overall_status == LabelCheckStatus.FAIL
    ids = {c.check_id for c in result.checks if c.status == LabelCheckStatus.FAIL}
    assert "4bj-c.manifest.research_eligible_false" in ids
    assert "4bj-c.manifest.eligibility_gate_status_pending" in ids


def test_missing_label_parquet_fails_validation_error(tmp_path: Path) -> None:
    label_path = tmp_path / "x.parquet"
    manifest_path = tmp_path / "x.json"
    feat_path = tmp_path / "f.parquet"
    feat_manifest_path = tmp_path / "fm.json"
    norm_path = tmp_path / "n.parquet"
    with pytest.raises(LabelValidationError):
        validate_label_dataset_v001(
            label_parquet_path=label_path,
            label_manifest_path=manifest_path,
            feature_parquet_path=feat_path,
            feature_manifest_path=feat_manifest_path,
            normalized_parquet_path=norm_path,
            source_feature_manifest_sha256="0" * 64,
            source_feature_parquet_sha256="0" * 64,
            source_feature_successor_state_sha256="0" * 64,
            source_phase_4bi_b_gate_report_sha256="0" * 64,
            source_normalized_parquet_sha256="0" * 64,
            expected_label_config_hash="0" * 64,
        )


def test_horizon_constants_locked() -> None:
    # Sanity: ensure validation imports preserve canonical horizons.
    assert LABEL_HORIZONS_V001 == ("1s", "5s", "15s", "60s")
