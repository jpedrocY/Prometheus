"""Phase 4bm-Q check-suite unit tests — small unit-level checks that
do not require synthetic artefact fixtures.

The exhaustive end-to-end validation of the check suite is provided by
``test_multiday_label_gate.py`` which runs the orchestrator against the
real local gitignored Phase 4bm-O artefacts; this file holds only
fixture-free unit checks of the data-model and locked constants.
"""
from __future__ import annotations

from prometheus.research.microstructure.labels_schema_v002 import LABEL_SCHEMA_V002
from prometheus.research.microstructure.multiday_label_gate_checks import (
    CHECK_ORDER,
    EXPECTED_CENSORED_PER_HORIZON,
    EXPECTED_DATE_COUNT,
    EXPECTED_DATE_END,
    EXPECTED_DATE_START,
    EXPECTED_ENVELOPE_TERMINAL_UNIX_MS,
    EXPECTED_FEATURE_CONFIG_HASH,
    EXPECTED_FEATURE_MANIFEST_SHA,
    EXPECTED_INVALID_PRICE_ROW_COUNT,
    EXPECTED_LABEL_COLUMN_COUNT,
    EXPECTED_LABEL_CONFIG_HASH,
    EXPECTED_LABEL_MANIFEST_SHA,
    EXPECTED_LABEL_MANIFEST_SIDECAR_SHA,
    EXPECTED_LABEL_SCHEMA_COLUMN_COUNT,
    EXPECTED_LINEAGE_COLUMN_COUNT,
    EXPECTED_SUPPORT_COLUMN_COUNT,
    EXPECTED_SYMBOL,
    EXPECTED_TOTAL_LABEL_ROW_COUNT,
    SAMPLE_DATES,
    MultidayLabelGateCheckResult,
    MultidayLabelGateCheckStatus,
)


def test_check_order_is_60_in_documented_order() -> None:
    assert len(CHECK_ORDER) == 60
    # Group counts: 15 + 10 + 11 + 6 + 7 + 4 + 7 = 60.
    by_group: dict[str, int] = {}
    for cid in CHECK_ORDER:
        by_group[cid[0]] = by_group.get(cid[0], 0) + 1
    assert by_group == {"A": 15, "B": 10, "C": 11, "D": 6, "E": 7, "F": 4, "G": 7}


def test_expected_label_row_count_locked() -> None:
    assert EXPECTED_TOTAL_LABEL_ROW_COUNT == 155_153_449


def test_expected_label_manifest_sha_locked() -> None:
    assert EXPECTED_LABEL_MANIFEST_SHA == (
        "5e17074d051e9f41415e6c693ba8039be5cf551e8ed9753792824ff48d7d53ed"
    )
    assert EXPECTED_LABEL_MANIFEST_SIDECAR_SHA == (
        "451d5b884f9f245981612f415d700f3e0bf54fe6276e8916c6ce387f82b77cbd"
    )


def test_expected_label_config_hash_locked() -> None:
    assert EXPECTED_LABEL_CONFIG_HASH == (
        "352bad410a5e7023c295e8a6fb944d071c46191fca8626a66b12ff74eed2c560"
    )


def test_expected_feature_lineage_constants_locked() -> None:
    assert EXPECTED_FEATURE_MANIFEST_SHA == (
        "512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"
    )
    assert EXPECTED_FEATURE_CONFIG_HASH == (
        "819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"
    )


def test_expected_date_envelope_locked() -> None:
    assert EXPECTED_DATE_COUNT == 90
    assert EXPECTED_DATE_START == "2024-12-01"
    assert EXPECTED_DATE_END == "2025-02-28"
    assert EXPECTED_SYMBOL == "BTCUSDT"


def test_expected_envelope_terminal_locked() -> None:
    assert EXPECTED_ENVELOPE_TERMINAL_UNIX_MS == 1_740_787_199_996


def test_expected_censored_per_horizon_locked() -> None:
    assert dict(EXPECTED_CENSORED_PER_HORIZON) == {
        "1s": 14, "5s": 39, "15s": 170, "60s": 634,
    }
    assert EXPECTED_INVALID_PRICE_ROW_COUNT == 0


def test_schema_column_counts_internally_consistent() -> None:
    assert EXPECTED_LABEL_SCHEMA_COLUMN_COUNT == 40
    assert EXPECTED_LINEAGE_COLUMN_COUNT == 17
    assert EXPECTED_LABEL_COLUMN_COUNT == 8
    assert EXPECTED_SUPPORT_COLUMN_COUNT == 14
    assert len(LABEL_SCHEMA_V002) == EXPECTED_LABEL_SCHEMA_COLUMN_COUNT
    assert (
        EXPECTED_LINEAGE_COLUMN_COUNT
        + 1  # label_config_hash
        + EXPECTED_LABEL_COLUMN_COUNT
        + EXPECTED_SUPPORT_COLUMN_COUNT
        == EXPECTED_LABEL_SCHEMA_COLUMN_COUNT
    )


def test_sample_dates_six_representative() -> None:
    assert SAMPLE_DATES == (
        "2024-12-01", "2024-12-31", "2025-01-15",
        "2025-01-31", "2025-02-15", "2025-02-28",
    )
    # All sample dates are within the locked envelope.
    assert SAMPLE_DATES[0] == EXPECTED_DATE_START
    assert SAMPLE_DATES[-1] == EXPECTED_DATE_END


def test_check_result_to_dict_roundtrip() -> None:
    r = MultidayLabelGateCheckResult(
        check_id="A1", group="A", status=MultidayLabelGateCheckStatus.PASS,
        blocking=True, expected="x", observed="x", detail="ok",
    )
    d = r.to_dict()
    assert d == {
        "check_id": "A1", "group": "A", "status": "PASS",
        "blocking": True, "expected": "x", "observed": "x", "detail": "ok",
    }
