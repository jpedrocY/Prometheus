"""Phase 4bn-B — local output writer / sidecar discipline tests.

Verifies that the Phase 4bn-B output writers:

- write every JSON / CSV artefact under the approved gitignored namespace
  ``data/research/microstructure/ml-baselines/phase-4bn-b/``;
- pair every output with a canonical Phase 4bb-F sidecar:
  ``<sha256_lowercase_hex><two ASCII spaces><basename>\\n`` — no CRLF,
  no BOM, no extra fields;
- compute the recorded SHA256 to match the actual on-disk SHA256;
- never produce output anywhere under ``data/microstructure/``.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from prometheus.research.microstructure import ml_baseline_design_v002 as design
from prometheus.research.microstructure import ml_baseline_report_v002 as report


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def test_resolve_output_root_is_under_approved_namespace(tmp_path: Path) -> None:
    out = report.resolve_output_root(tmp_path)
    rel = out.relative_to(tmp_path)
    assert tuple(rel.parts) == design.OUTPUT_NAMESPACE_PARTS
    # And the literal segments are correct.
    assert rel.parts == (
        "data",
        "research",
        "microstructure",
        "ml-baselines",
        "phase-4bn-b",
    )


def test_write_json_artefact_writes_canonical_sidecar(tmp_path: Path) -> None:
    out_root = report.resolve_output_root(tmp_path)
    payload = {"phase_id": design.PHASE_ID, "n": 42}
    path, sha, sidecar, sidecar_sha = report.write_json_artefact(
        output_root=out_root,
        basename="example_payload.json",
        payload=payload,
    )
    assert path.exists()
    assert sidecar.exists()
    # SHA matches on-disk bytes.
    assert sha == _hash_bytes(path.read_bytes())
    # Sidecar body format.
    body = sidecar.read_bytes()
    assert body == f"{sha}  {path.name}\n".encode()
    assert body.endswith(b"\n")
    assert b"\r" not in body
    # Sidecar self-SHA matches.
    assert sidecar_sha == _hash_bytes(body)
    # Sidecar path discipline.
    assert sidecar.suffix == ".sha256"
    assert sidecar.name == path.name + ".sha256"


def test_write_csv_table_writes_canonical_sidecar(tmp_path: Path) -> None:
    out_root = report.resolve_output_root(tmp_path)
    path, sha, sidecar, _ = report.write_csv_table(
        output_root=out_root,
        basename="example_metrics.csv",
        header=["family", "split", "horizon", "metric_name", "metric_value"],
        rows=[
            ["majority_class_prior", "train", "15s", "accuracy", 0.5],
            ["majority_class_prior", "validation", "15s", "accuracy", 0.45],
        ],
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    # LF-only line endings.
    assert "\r" not in text
    assert text.endswith("\n")
    # Sidecar format.
    body = sidecar.read_bytes()
    assert body == f"{sha}  {path.name}\n".encode()


def test_canonical_sidecar_format_exact_two_spaces_no_bom(tmp_path: Path) -> None:
    out_root = report.resolve_output_root(tmp_path)
    path, sha, sidecar, _ = report.write_json_artefact(
        output_root=out_root,
        basename="format_check.json",
        payload={"k": "v"},
    )
    raw = sidecar.read_bytes()
    # Match the canonical Phase 4bb-F format literally: 64 hex + two
    # spaces + basename + LF.
    assert re.fullmatch(rb"[0-9a-f]{64}  format_check\.json\n", raw) is not None
    assert not raw.startswith(b"\xef\xbb\xbf")


def test_outputs_never_land_under_data_microstructure(tmp_path: Path) -> None:
    out = report.resolve_output_root(tmp_path)
    parts = out.relative_to(tmp_path).parts
    assert "microstructure" in parts  # under data/research/microstructure
    assert parts[0] == "data" and parts[1] == "research"


def test_feature_schema_payload_has_phase_4bn_b_identity() -> None:
    payload = report.build_feature_schema_payload()
    assert payload["phase_id"] == design.PHASE_ID
    assert payload["n_features"] == 45
    assert payload["feature_config_hash"] == design.EXPECTED_FEATURE_CONFIG_HASH
    assert payload["excluded_lineage_column_names"] == list(
        design.EXCLUDED_LINEAGE_COLUMN_NAMES
    )


def test_run_manifest_payload_records_test_holdout_sealed() -> None:
    payload = report.build_run_manifest_payload(
        created_at_unix_ms=1_700_000_000_000,
        code_commit_sha="abc1234",
        label_manifest_sha256="0" * 64,
        feature_manifest_sha256="1" * 64,
        label_manifest_path="microstructure/manifests/label.json",
        feature_manifest_path="microstructure/manifests/feature.json",
        output_basenames={},
        output_sha256s={},
        output_sidecar_basenames={},
        output_sidecar_sha256s={},
        run_duration_seconds=10.5,
        train_n_partitions=45,
        validation_n_partitions=30,
        test_n_partitions_unused=15,
        train_supervised_rows_per_horizon={"15s": 100, "60s": 90},
        validation_supervised_rows_per_horizon={"15s": 50, "60s": 45},
        train_censored_rows_per_horizon={"15s": 0, "60s": 0},
        validation_censored_rows_per_horizon={"15s": 0, "60s": 0},
        train_embargoed_rows=10,
        validation_embargoed_rows=5,
        test_rows_loaded=0,
        runtime_environment={"python_version": "3.11"},
    )
    assert payload["test_holdout_sealed"] is True
    assert payload["test_rows_loaded"] == 0
    assert payload["non_authorization"]["used_test_holdout_for_training"] is False
    assert payload["non_authorization"]["mutated_manifest"] is False
    assert payload["non_authorization"]["authorized_successor_phase"] is False


def test_per_horizon_payload_records_no_selection_flags() -> None:
    payload = report.build_per_horizon_summary_payload(
        per_horizon={
            "15s": {"train": {}, "validation": {}},
            "60s": {"train": {}, "validation": {}},
        },
        class_balance_by_split_horizon={},
    )
    assert payload["no_model_selected_as_best"] is True
    assert payload["no_threshold_tuned"] is True
    assert payload["no_feature_ranked"] is True
    assert payload["no_strategy_or_signals_generated"] is True
    assert payload["no_pnl_simulated"] is True
    assert payload["no_backtest_run"] is True


def test_transform_metadata_records_train_only_fit() -> None:
    payload = report.build_transform_metadata_payload(
        standardizer_dict={"fitted": True, "n_features": 45},
        train_n_partitions=45,
        train_n_supervised_rows_per_horizon={"15s": 0, "60s": 0},
    )
    assert payload["fit_split"] == "train"
    assert payload["test_holdout_used_for_fit"] is False
    assert payload["test_holdout_used_for_transform"] is False
    assert payload["validation_apply_only"] is True
