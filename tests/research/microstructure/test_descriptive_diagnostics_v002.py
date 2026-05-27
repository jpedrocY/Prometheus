"""Unit tests for the Phase 4bm-W descriptive diagnostics kernel and report.

Offline tests using small synthetic parquet partitions written under
``tmp_path``. No network, no reads of the real ``data/microstructure/``
artefacts, no mutation of any repository artefact.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from prometheus.research.microstructure import (
    descriptive_diagnostics_v002 as dd,
)
from prometheus.research.microstructure import diagnostics_report_v002 as rep
from prometheus.research.microstructure import (
    diagnostics_split_policy_v002 as policy,
)

ENVELOPE = policy.ENVELOPE_TERMINAL_UNIX_MS


def _build_label_table(
    utc_date: str,
    n: int,
    *,
    base_offset_ms: int = 0,
    returns: dict[str, list[float | None]] | None = None,
    directions: dict[str, list[int | None]] | None = None,
    censored: dict[str, list[bool]] | None = None,
    break_censor_rule: bool = False,
    bad_direction: bool = False,
) -> pa.Table:
    """Build a synthetic per-day label table with the v002 column subset."""
    day_start = policy.utc_date_start_ms(utc_date)
    src = np.array(
        [day_start + base_offset_ms + i for i in range(n)], dtype=np.int64
    )
    row_index = np.arange(n, dtype=np.int64)
    agg = np.arange(1000, 1000 + n, dtype=np.int64)

    cols: dict[str, pa.Array] = {
        "row_index": pa.array(row_index),
        "agg_trade_id": pa.array(agg),
        "feature_timestamp_ms": pa.array(src),
        "source_transact_time_ms": pa.array(src),
        "feature_config_hash": pa.array([dd.EXPECTED_FEATURE_CONFIG_HASH] * n),
        "label_config_hash": pa.array([dd.EXPECTED_LABEL_CONFIG_HASH] * n),
        "symbol": pa.array(["BTCUSDT"] * n),
        "utc_date": pa.array([utc_date] * n),
        "dataset_version": pa.array(["v002"] * n),
    }

    any_cens = np.zeros(n, dtype=bool)
    for h in dd.HORIZONS:
        h_ms = dd.HORIZON_MS[h]
        rule_flag = (src + h_ms) > ENVELOPE
        flag = (
            rule_flag
            if censored is None
            else np.array(censored[h], dtype=bool)
        )
        if break_censor_rule and h == "1s":
            flag = ~rule_flag  # deliberately wrong
        any_cens |= flag

        if returns is not None and h in returns:
            ret_vals = returns[h]
        else:
            ret_vals = [
                None if flag[i] else (1e-4 * ((i % 5) - 2)) for i in range(n)
            ]
        if directions is not None and h in directions:
            dir_vals = directions[h]
        else:
            dir_vals = [
                None
                if (rv is None)
                else (1 if rv > 0 else (-1 if rv < 0 else 0))
                for rv in ret_vals
            ]
            if bad_direction and h == "1s" and n > 0:
                dir_vals = list(dir_vals)
                dir_vals[0] = 7  # out-of-domain

        cols[f"forward_log_return_{h}"] = pa.array(ret_vals, type=pa.float64())
        cols[f"forward_direction_{h}"] = pa.array(dir_vals, type=pa.int8())
        cols[f"horizon_censored_flag_{h}"] = pa.array(
            [bool(x) for x in flag], type=pa.bool_()
        )

    cols["label_invalid_price_flag"] = pa.array([False] * n, type=pa.bool_())
    cols["label_any_censored_flag"] = pa.array(
        [bool(x) for x in any_cens], type=pa.bool_()
    )
    return pa.table(cols)


def _build_feature_table(label_table: pa.Table) -> pa.Table:
    return pa.table(
        {
            "row_index": label_table.column("row_index"),
            "agg_trade_id": label_table.column("agg_trade_id"),
            "feature_timestamp_ms": label_table.column("feature_timestamp_ms"),
            "source_transact_time_ms": label_table.column(
                "source_transact_time_ms"
            ),
            "feature_config_hash": label_table.column("feature_config_hash"),
        }
    )


def _write(tmp: Path, name: str, table: pa.Table) -> Path:
    p = tmp / name
    pq.write_table(table, p)
    return p


def test_summarize_clean_train_partition(tmp_path: Path) -> None:
    t = _build_label_table("2024-12-01", 10)
    p = _write(tmp_path, "labels.parquet", t)
    summary = dd.summarize_label_partition(p, "2024-12-01")

    assert summary.split == policy.TRAIN
    assert summary.row_count == 10
    assert summary.n_invalid_price == 0
    assert summary.n_any_censored_flag_mismatch == 0
    assert summary.n_row_index_violation == 0
    assert summary.n_src_ne_feature_ts == 0
    assert summary.n_out_of_partition_day == 0
    assert summary.embargo_count == 0
    for h in dd.HORIZONS:
        hs = summary.horizon_stats[h]
        assert hs.n_censor_rule_mismatch == 0
        assert hs.n_censored_not_null == 0
        assert hs.n_dir_domain_violation == 0
        assert hs.n_dir_sign_mismatch == 0
        assert hs.n_censored == 0  # train day far from envelope terminal
        assert hs.n_return_nonnull == 10


def test_summarize_detects_censor_rule_mismatch(tmp_path: Path) -> None:
    t = _build_label_table("2024-12-01", 6, break_censor_rule=True)
    p = _write(tmp_path, "labels.parquet", t)
    summary = dd.summarize_label_partition(p, "2024-12-01")
    assert summary.horizon_stats["1s"].n_censor_rule_mismatch == 6


def test_summarize_detects_direction_domain_violation(tmp_path: Path) -> None:
    t = _build_label_table("2024-12-01", 6, bad_direction=True)
    p = _write(tmp_path, "labels.parquet", t)
    summary = dd.summarize_label_partition(p, "2024-12-01")
    assert summary.horizon_stats["1s"].n_dir_domain_violation >= 1


def test_envelope_terminal_censoring_on_final_day(tmp_path: Path) -> None:
    # Place rows so that source_transact_time_ms + 60_000 > envelope for some.
    n = 5
    day = "2025-02-28"
    # offset so last rows are within 60s of envelope terminal
    base = ENVELOPE - policy.utc_date_start_ms(day) - 30_000
    t = _build_label_table(day, n, base_offset_ms=int(base))
    p = _write(tmp_path, "labels.parquet", t)
    summary = dd.summarize_label_partition(p, "2025-02-28")
    assert summary.split == policy.TEST
    # 60s horizon should be censored for all (T+60000 > envelope), rule consistent
    assert summary.horizon_stats["60s"].n_censor_rule_mismatch == 0
    assert summary.horizon_stats["60s"].n_censored == n
    # censored rows have null returns (null discipline holds)
    assert summary.horizon_stats["60s"].n_censored_not_null == 0


def test_embargo_count_on_train_last_day(tmp_path: Path) -> None:
    # Rows straddling T_TV - within last 60s of 2025-01-14 are embargoed.
    day = "2025-01-14"
    day_start = policy.utc_date_start_ms(day)
    # one row 30s before boundary (embargoed), one row 90s before (not)
    boundary = policy.BOUNDARY_TRAIN_VALIDATION_MS
    src_vals = [boundary - 30_000, boundary - 90_000]
    n = 2
    cols = {
        "row_index": pa.array(np.arange(n, dtype=np.int64)),
        "agg_trade_id": pa.array(np.arange(n, dtype=np.int64)),
        "feature_timestamp_ms": pa.array(np.array(src_vals, dtype=np.int64)),
        "source_transact_time_ms": pa.array(np.array(src_vals, dtype=np.int64)),
        "feature_config_hash": pa.array([dd.EXPECTED_FEATURE_CONFIG_HASH] * n),
        "label_config_hash": pa.array([dd.EXPECTED_LABEL_CONFIG_HASH] * n),
        "symbol": pa.array(["BTCUSDT"] * n),
        "utc_date": pa.array([day] * n),
        "dataset_version": pa.array(["v002"] * n),
        "label_invalid_price_flag": pa.array([False] * n, type=pa.bool_()),
        "label_any_censored_flag": pa.array([False] * n, type=pa.bool_()),
    }
    for h in dd.HORIZONS:
        cols[f"forward_log_return_{h}"] = pa.array([1e-4, -1e-4], type=pa.float64())
        cols[f"forward_direction_{h}"] = pa.array([1, -1], type=pa.int8())
        cols[f"horizon_censored_flag_{h}"] = pa.array(
            [False, False], type=pa.bool_()
        )
    p = _write(tmp_path, "labels.parquet", pa.table(cols))
    assert day_start <= src_vals[0] < day_start + policy.UTC_DAY_MS
    summary = dd.summarize_label_partition(p, day)
    assert summary.embargo_count == 1
    assert summary.boundary_crossing_per_horizon["60s"] == 1


def test_alignment_clean_and_mismatch(tmp_path: Path) -> None:
    lt = _build_label_table("2024-12-01", 8)
    ft = _build_feature_table(lt)
    lp = _write(tmp_path, "labels.parquet", lt)
    fp = _write(tmp_path, "features.parquet", ft)
    al = dd.summarize_alignment_partition(lp, fp, "2024-12-01")
    assert al.row_count_match
    assert al.n_agg_trade_id_mismatch == 0
    assert al.n_source_transact_time_mismatch == 0
    assert al.feature_config_hash_match

    # Corrupt one agg_trade_id in the feature table.
    bad_agg = ft.column("agg_trade_id").to_numpy(zero_copy_only=False).copy()
    bad_agg[0] += 999
    ft2 = ft.set_column(
        ft.schema.get_field_index("agg_trade_id"),
        "agg_trade_id",
        pa.array(bad_agg),
    )
    fp2 = _write(tmp_path, "features2.parquet", ft2)
    al2 = dd.summarize_alignment_partition(lp, fp2, "2024-12-01")
    assert al2.n_agg_trade_id_mismatch == 1


def test_histogram_quantile_tail_returns_none() -> None:
    counts = [0] * dd.HISTOGRAM_N_BINS
    # All mass in underflow.
    q = dd._histogram_quantile(5.0, underflow=10, overflow=0, counts=counts)
    assert q is None
    # All mass in overflow.
    q2 = dd._histogram_quantile(5.0, underflow=0, overflow=10, counts=counts)
    assert q2 is None


def _fake_run(monkeypatch_counts: int = 90) -> dd.DiagnosticsRun:
    return dd.DiagnosticsRun(
        partition_summaries=[],
        alignment_summaries=[],
        label_manifest={"diagnostics_authorized": False},
        feature_manifest={},
        label_partition_count_on_disk=monkeypatch_counts,
        feature_partition_count_on_disk=monkeypatch_counts,
        label_sidecar_count_on_disk=monkeypatch_counts,
        feature_sidecar_count_on_disk=monkeypatch_counts,
    )


def _matching_split_aggs() -> dict[str, rep.SplitAggregate]:
    aggs = {s: rep._new_split_aggregate(s) for s in policy.SPLIT_NAMES}
    aggs["train"].partition_count = 45
    aggs["validation"].partition_count = 30
    aggs["test"].partition_count = 15
    aggs["train"].row_count = dd.EXPECTED_TOTAL_ROW_COUNT
    # Put the recorded censored counts into the test split's horizons.
    for h in dd.HORIZONS:
        aggs["test"].horizon_stats[h].n_censored = (  # type: ignore[index]
            dd.EXPECTED_CENSORED_PER_HORIZON[h]
        )
    return aggs


def test_derive_verdict_pass_with_caveats_on_clean_family() -> None:
    run = _fake_run()
    aggs = _matching_split_aggs()
    structural = dict.fromkeys(
        rep._sum_structural([]).keys(), 0
    )
    alignment = dict.fromkeys(rep._sum_alignment(run).keys(), 0)
    global_censored = dict(dd.EXPECTED_CENSORED_PER_HORIZON)
    v = rep.derive_verdict(run, aggs, structural, alignment, global_censored)
    assert v.blocking_failures == []
    # envelope censoring + approximate quantiles + manifest historical flag
    assert v.verdict == rep.VERDICT_PASS_WITH_CAVEATS
    assert any("envelope-terminal censoring" in c for c in v.caveats)


def test_derive_verdict_fail_on_structural_violation() -> None:
    run = _fake_run()
    aggs = _matching_split_aggs()
    structural = dict.fromkeys(rep._sum_structural([]).keys(), 0)
    structural["censor_rule_mismatch"] = 3
    alignment = dict.fromkeys(rep._sum_alignment(run).keys(), 0)
    global_censored = dict(dd.EXPECTED_CENSORED_PER_HORIZON)
    v = rep.derive_verdict(run, aggs, structural, alignment, global_censored)
    assert v.verdict == rep.VERDICT_FAIL
    assert any("censor_rule_mismatch" in f for f in v.blocking_failures)


def test_derive_verdict_fail_on_row_count() -> None:
    run = _fake_run(monkeypatch_counts=90)
    aggs = _matching_split_aggs()
    aggs["train"].row_count = 123  # wrong total
    structural = dict.fromkeys(rep._sum_structural([]).keys(), 0)
    alignment = dict.fromkeys(rep._sum_alignment(run).keys(), 0)
    global_censored = dict(dd.EXPECTED_CENSORED_PER_HORIZON)
    v = rep.derive_verdict(run, aggs, structural, alignment, global_censored)
    assert v.verdict == rep.VERDICT_FAIL
    assert any("total_row_count" in f for f in v.blocking_failures)


def test_write_outputs_creates_files_and_sidecars(tmp_path: Path) -> None:
    run = _fake_run()
    # Build a minimal payload via build_payload using empty summaries.
    payload = rep.build_payload(run, created_at_unix_ms=123, code_commit_sha="abc")
    out_root = tmp_path / "data" / "research" / "diag"
    written = rep.write_outputs(
        out_root, payload, created_at_unix_ms=123, code_commit_sha="abc"
    )
    assert written.summary_json_path.is_file()
    assert written.summary_sidecar_path.is_file()
    assert written.manifest_json_path.is_file()
    # Sidecar canonical Phase 4bb-F format: "<sha>  <basename>\n".
    body = written.summary_sidecar_path.read_bytes()
    assert body.endswith(b"\n")
    text = body.decode("ascii")
    sha, sep, name = text[:64], text[64:66], text[66:].rstrip("\n")
    assert sha == written.summary_json_sha256
    assert sep == "  "
    assert name == written.summary_json_path.name
    # Round-trip JSON is valid and deterministic-keyed.
    loaded = json.loads(written.summary_json_path.read_text(encoding="utf-8"))
    assert loaded["phase_id"] == "4bm-w"
    assert loaded["descriptive_only"] is True


def test_write_outputs_refuses_data_microstructure(tmp_path: Path) -> None:
    run = _fake_run()
    payload = rep.build_payload(run, created_at_unix_ms=1, code_commit_sha="x")
    bad_root = tmp_path / "data" / "microstructure" / "diag"
    with pytest.raises(rep.DiagnosticsReportError):
        rep.write_outputs(
            bad_root, payload, created_at_unix_ms=1, code_commit_sha="x"
        )
