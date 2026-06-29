"""Phase 4bn-AA — offline unit tests for the pre-v002 split-policy artefact.

Pure, offline, synthetic tests of
:mod:`prometheus.research.microstructure.pre_v002_split_policy`. No production
data, no ``data/microstructure``, no ``data/research``, no manifests, no Parquet,
no network, no RNG, and no dependence on the local machine timezone.
"""

from __future__ import annotations

import os
import time
from datetime import UTC, datetime

import pytest

from prometheus.research.microstructure import (
    pre_v002_split_policy as policy,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _ms(iso: str) -> int:
    """Return epoch ms for an ISO-8601 UTC timestamp string."""
    return int(datetime.fromisoformat(iso).replace(tzinfo=UTC).timestamp() * 1000)


# ---------------------------------------------------------------------------
# 1. Policy name
# ---------------------------------------------------------------------------


def test_policy_name_exact() -> None:
    assert (
        policy.SPLIT_POLICY_NAME
        == "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"
    )


# ---------------------------------------------------------------------------
# 2. Date constants match Phase 4bn-Y
# ---------------------------------------------------------------------------


def test_date_constants_match_phase_4bn_y() -> None:
    assert policy.PRE_V002_START_DATE == "2024-03-01"
    assert policy.PRE_V002_END_DATE == "2024-11-30"
    assert policy.TRAIN_START_DATE == "2024-03-01"
    assert policy.TRAIN_END_DATE == "2024-09-30"
    assert policy.TRAIN_VALIDATION_EMBARGO_DATE == "2024-10-01"
    assert policy.VALIDATION_START_DATE == "2024-10-02"
    assert policy.VALIDATION_END_DATE == "2024-11-15"
    assert policy.VALIDATION_HOLDOUT_EMBARGO_DATE == "2024-11-16"
    assert policy.HOLDOUT_START_DATE == "2024-11-17"
    assert policy.HOLDOUT_END_DATE == "2024-11-30"


# ---------------------------------------------------------------------------
# 3 + 4. Date counts and arithmetic
# ---------------------------------------------------------------------------


def test_date_counts() -> None:
    assert len(policy.train_dates()) == policy.EXPECTED_TRAIN_DATE_COUNT == 214
    assert (
        len(policy.validation_dates()) == policy.EXPECTED_VALIDATION_DATE_COUNT == 45
    )
    assert len(policy.holdout_dates()) == policy.EXPECTED_HOLDOUT_DATE_COUNT == 14
    assert len(policy.embargo_dates()) == policy.EXPECTED_EMBARGO_DATE_COUNT == 2
    assert len(policy.segment_dates()) == policy.EXPECTED_TOTAL_DATE_COUNT == 275


def test_date_arithmetic_214_1_45_1_14_equals_275() -> None:
    assert 214 + 1 + 45 + 1 + 14 == 275
    assert (
        policy.EXPECTED_TRAIN_DATE_COUNT
        + 1
        + policy.EXPECTED_VALIDATION_DATE_COUNT
        + 1
        + policy.EXPECTED_HOLDOUT_DATE_COUNT
        == policy.EXPECTED_TOTAL_DATE_COUNT
    )
    assert policy.validate_policy_arithmetic() is True


# ---------------------------------------------------------------------------
# 5 - 12. split_for_date boundaries
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2024-03-01", policy.TRAIN),  # 5
        ("2024-09-30", policy.TRAIN),  # 6
        ("2024-10-01", policy.EMBARGO),  # 7
        ("2024-10-02", policy.VALIDATION),  # 8
        ("2024-11-15", policy.VALIDATION),  # 9
        ("2024-11-16", policy.EMBARGO),  # 10
        ("2024-11-17", policy.HOLDOUT),  # 11
        ("2024-11-30", policy.HOLDOUT),  # 12
    ],
)
def test_split_for_date_boundaries(date_str: str, expected: str) -> None:
    assert policy.split_for_date(date_str) == expected


# ---------------------------------------------------------------------------
# 13 - 15. Out-of-segment dates raise
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "date_str",
    ["2024-02-29", "2024-12-01", "2025-02-14", "2023-12-31", "2025-03-01"],
)
def test_split_for_date_out_of_segment_raises(date_str: str) -> None:
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.split_for_date(date_str)


# ---------------------------------------------------------------------------
# 16. All v002 terminal dates raise
# ---------------------------------------------------------------------------


def test_all_v002_terminal_dates_raise() -> None:
    for d in policy._date_range_inclusive("2024-12-01", "2025-02-28"):
        with pytest.raises(policy.PreV002SplitPolicyError):
            policy.split_for_date(d)


# ---------------------------------------------------------------------------
# 17. All sealed-test dates raise
# ---------------------------------------------------------------------------


def test_all_sealed_test_dates_raise() -> None:
    for d in policy._date_range_inclusive("2025-02-14", "2025-02-28"):
        with pytest.raises(policy.PreV002SplitPolicyError):
            policy.split_for_date(d)


# ---------------------------------------------------------------------------
# 18. Timestamp assignment uses UTC date
# ---------------------------------------------------------------------------


def test_timestamp_assignment_uses_utc_date() -> None:
    # 2024-10-01T23:59:59.999Z is still the embargo date.
    assert (
        policy.split_for_timestamp_ms(_ms("2024-10-01T23:59:59.999"))
        == policy.EMBARGO
    )
    # 2024-10-02T00:00:00.000Z is the first validation instant.
    assert (
        policy.split_for_timestamp_ms(_ms("2024-10-02T00:00:00.000"))
        == policy.VALIDATION
    )
    # Boundary constants match the exact instants.
    assert _ms("2024-10-02T00:00:00.000") == policy.BOUNDARY_TRAIN_VALIDATION_MS
    assert (
        policy.split_for_timestamp_ms(policy.BOUNDARY_TRAIN_VALIDATION_MS - 1)
        == policy.EMBARGO
    )
    assert (
        policy.split_for_timestamp_ms(policy.BOUNDARY_TRAIN_VALIDATION_MS)
        == policy.VALIDATION
    )
    # Train/validation/holdout interior instants.
    assert (
        policy.split_for_timestamp_ms(_ms("2024-09-30T12:00:00.000")) == policy.TRAIN
    )
    assert (
        policy.split_for_timestamp_ms(_ms("2024-11-17T00:00:00.000"))
        == policy.HOLDOUT
    )


# ---------------------------------------------------------------------------
# 19. Local timezone cannot affect timestamp split
# ---------------------------------------------------------------------------


def test_local_timezone_does_not_affect_split() -> None:
    saved = os.environ.get("TZ")
    try:
        for tz in ("UTC", "America/New_York", "Asia/Tokyo", "Pacific/Kiritimati"):
            os.environ["TZ"] = tz
            if hasattr(time, "tzset"):
                time.tzset()
            # An instant just before the boundary stays in the embargo date,
            # regardless of the process-local timezone.
            assert (
                policy.split_for_timestamp_ms(
                    policy.BOUNDARY_TRAIN_VALIDATION_MS - 1
                )
                == policy.EMBARGO
            )
            assert (
                policy.split_for_timestamp_ms(policy.BOUNDARY_TRAIN_VALIDATION_MS)
                == policy.VALIDATION
            )
    finally:
        if saved is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = saved
        if hasattr(time, "tzset"):
            time.tzset()


# ---------------------------------------------------------------------------
# 20. Boundary timestamp constants are exact
# ---------------------------------------------------------------------------


def test_boundary_timestamp_constants_exact() -> None:
    assert _ms("2024-10-02T00:00:00") == policy.BOUNDARY_TRAIN_VALIDATION_MS
    assert _ms("2024-11-17T00:00:00") == policy.BOUNDARY_VALIDATION_HOLDOUT_MS
    assert policy.BOUNDARY_TRAIN_VALIDATION_MS == 1727827200000
    assert policy.BOUNDARY_VALIDATION_HOLDOUT_MS == 1731801600000
    assert policy.MIN_BOUNDARY_EMBARGO_MS == 60_000
    assert policy.MAX_LABEL_HORIZON_MS == 60_000
    assert policy.utc_date_start_ms("2024-10-02") == policy.BOUNDARY_TRAIN_VALIDATION_MS
    assert (
        policy.utc_date_start_ms("2024-11-17")
        == policy.BOUNDARY_VALIDATION_HOLDOUT_MS
    )


# ---------------------------------------------------------------------------
# 21 + 22. Horizon validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("h", [1000, 5000, 15000, 60000])
def test_horizon_validation_accepts_allowed(h: int) -> None:
    assert policy.validate_horizon_ms(h) == h
    assert h in policy.ALLOWED_HORIZONS_MS


@pytest.mark.parametrize("h", [0, 999, 2000, 30000, 120000, -1000])
def test_horizon_validation_rejects_invalid(h: int) -> None:
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.validate_horizon_ms(h)


def test_horizon_validation_rejects_bool() -> None:
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.validate_horizon_ms(True)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# 23 + 24. Boundary-crossing helper catches crossings
# ---------------------------------------------------------------------------


def test_train_row_crossing_into_validation_boundary() -> None:
    # A row one ms before the validation boundary with any horizon crosses it.
    t = policy.BOUNDARY_TRAIN_VALIDATION_MS - 1
    assert policy.is_earlier_split_boundary_crossing(t, 1000, policy.TRAIN) is True
    assert policy.is_earlier_split_boundary_crossing(t, 60000, policy.TRAIN) is True


def test_validation_row_crossing_into_holdout_boundary() -> None:
    t = policy.BOUNDARY_VALIDATION_HOLDOUT_MS - 1
    assert (
        policy.is_earlier_split_boundary_crossing(t, 1000, policy.VALIDATION) is True
    )
    assert (
        policy.is_earlier_split_boundary_crossing(t, 60000, policy.VALIDATION) is True
    )


# ---------------------------------------------------------------------------
# 25 + 26. Interior rows do not cross
# ---------------------------------------------------------------------------


def test_interior_train_row_does_not_cross() -> None:
    t = _ms("2024-06-01T12:00:00")
    assert policy.split_for_timestamp_ms(t) == policy.TRAIN
    assert policy.is_earlier_split_boundary_crossing(t, 60000, policy.TRAIN) is False


def test_interior_validation_row_does_not_cross() -> None:
    t = _ms("2024-10-20T12:00:00")
    assert policy.split_for_timestamp_ms(t) == policy.VALIDATION
    assert (
        policy.is_earlier_split_boundary_crossing(t, 60000, policy.VALIDATION) is False
    )


def test_full_date_purge_dominates_60s_no_real_train_row_crosses() -> None:
    # The latest real train instant (2024-09-30T23:59:59.999Z) + 60s lands on
    # the embargo date 2024-10-01, well short of the 2024-10-02 boundary.
    t = _ms("2024-09-30T23:59:59.999")
    assert policy.split_for_timestamp_ms(t) == policy.TRAIN
    assert policy.is_earlier_split_boundary_crossing(t, 60000, policy.TRAIN) is False


# ---------------------------------------------------------------------------
# 27. Holdout has no next split to cross
# ---------------------------------------------------------------------------


def test_holdout_next_split_crossing_is_false() -> None:
    t = policy.BOUNDARY_VALIDATION_HOLDOUT_MS  # first holdout instant
    assert policy.split_for_timestamp_ms(t) == policy.HOLDOUT
    assert policy.is_earlier_split_boundary_crossing(t, 60000, policy.HOLDOUT) is False
    assert policy.earlier_split_embargo_window_ms(policy.HOLDOUT) is None
    assert policy.boundary_crossing_window_ms(policy.HOLDOUT, 60000) is None


def test_boundary_crossing_out_of_segment_and_embargo_raise() -> None:
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.is_earlier_split_boundary_crossing(
            _ms("2024-12-15T00:00:00"), 1000, policy.TRAIN
        )
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.is_earlier_split_boundary_crossing(
            policy.BOUNDARY_TRAIN_VALIDATION_MS - 1, 1000, policy.EMBARGO
        )


# ---------------------------------------------------------------------------
# 28. Embargo rows are dropped / not model-eligible
# ---------------------------------------------------------------------------


def test_embargo_rows_not_model_eligible() -> None:
    assert policy.is_model_eligible_split(policy.EMBARGO) is False
    assert policy.is_model_eligible_split(policy.TRAIN) is True
    assert policy.is_model_eligible_split(policy.VALIDATION) is True
    assert policy.is_model_eligible_split(policy.HOLDOUT) is True
    assert policy.is_embargo_date("2024-10-01") is True
    assert policy.is_embargo_date("2024-11-16") is True
    assert policy.is_embargo_date("2024-06-01") is False
    with pytest.raises(policy.PreV002SplitPolicyError):
        policy.is_model_eligible_split("nonsense")


# ---------------------------------------------------------------------------
# 29 - 32. Inventory integrity
# ---------------------------------------------------------------------------


def test_inventory_no_duplicate_dates() -> None:
    inv = policy.policy_date_inventory()
    dates = [d for d, _ in inv]
    assert len(dates) == len(set(dates)) == 275


def test_inventory_no_missing_in_segment_dates() -> None:
    inv = policy.policy_date_inventory()
    dates = {d for d, _ in inv}
    assert dates == set(policy.segment_dates())


def test_no_date_in_two_model_eligible_splits() -> None:
    train_set = set(policy.train_dates())
    val_set = set(policy.validation_dates())
    hold_set = set(policy.holdout_dates())
    assert not (train_set & val_set)
    assert not (train_set & hold_set)
    assert not (val_set & hold_set)


def test_no_embargo_date_is_assignable() -> None:
    emb = set(policy.embargo_dates())
    assignable = (
        set(policy.train_dates())
        | set(policy.validation_dates())
        | set(policy.holdout_dates())
    )
    assert not (emb & assignable)
    for d in emb:
        assert policy.split_for_date(d) == policy.EMBARGO


def test_inventory_split_membership_matches_predicates() -> None:
    for d, split in policy.policy_date_inventory():
        assert policy.is_train_date(d) == (split == policy.TRAIN)
        assert policy.is_validation_date(d) == (split == policy.VALIDATION)
        assert policy.is_holdout_date(d) == (split == policy.HOLDOUT)
        assert policy.is_embargo_date(d) == (split == policy.EMBARGO)


# ---------------------------------------------------------------------------
# 33 - 36. Module hygiene (no RNG / network / heavy-data deps / data paths)
# ---------------------------------------------------------------------------

_SOURCE_PATH = os.path.join(
    os.path.dirname(policy.__file__), "pre_v002_split_policy.py"
)


def _read_source() -> str:
    with open(_SOURCE_PATH, encoding="utf-8") as fh:
        return fh.read()


@pytest.mark.parametrize(
    "needle",
    [
        "import random",
        "from random",
        "import numpy",
        "import socket",
        "import urllib",
        "import requests",
        "import http",
        "import pandas",
        "import pyarrow",
        "import polars",
        "data/microstructure",
        "data/research",
        "data\\\\microstructure",
        "data\\\\research",
        "open(",
        "Path(",
    ],
)
def test_source_has_no_forbidden_tokens(needle: str) -> None:
    assert needle not in _read_source()


def test_source_imports_only_datetime() -> None:
    src = _read_source()
    # The only third-party / stdlib imports are from datetime + __future__.
    assert "from datetime import" in src
    assert "from __future__ import annotations" in src


# ---------------------------------------------------------------------------
# 37 - 39. Contract metadata
# ---------------------------------------------------------------------------


def test_contract_records_non_authorization_flags() -> None:
    c = policy.build_split_policy_contract()
    assert c["v002_terminal_window_read"] is False
    assert c["sealed_test_split_touched"] is False
    assert c["test_rows_loaded"] == 0
    assert c["no_shuffle"] is True
    assert c["no_random_split"] is True
    assert c["no_data_io"] is True
    assert c["no_successor_authorization"] is True
    assert c["set_manifest_chronological_split_policy"] is False
    assert c["flipped_research_eligible"] is False
    assert c["transitioned_eligibility_gate_status"] is False
    assert c["holdout_is_sealed_test"] is False


def test_contract_records_counts_and_embargo_settings() -> None:
    c = policy.build_split_policy_contract()
    assert c["split_policy_name"] == policy.SPLIT_POLICY_NAME
    assert c["train_date_count"] == 214
    assert c["validation_date_count"] == 45
    assert c["holdout_date_count"] == 14
    assert c["embargo_date_count"] == 2
    assert c["total_date_count"] == 275
    assert c["embargo_dates"] == ["2024-10-01", "2024-11-16"]
    assert c["boundary_train_validation_ms"] == 1727827200000
    assert c["boundary_validation_holdout_ms"] == 1731801600000
    assert c["min_boundary_embargo_seconds"] == 60
    assert c["max_label_horizon_ms"] == 60000
    assert c["one_day_purge_seconds"] == 86_400
    assert c["allowed_horizons_ms"] == [1000, 5000, 15000, 60000]
    assert c["assignment_rule"] == "source_transact_time_ms_utc_date"
    assert c["ordering_rule"] == "chronological_only"


def test_contract_records_pre_v002_only_source_scope() -> None:
    c = policy.build_split_policy_contract()
    assert c["future_allowed_source_scope"] == "pre_v002_only"
    assert c["future_allowed_source_start_date"] == "2024-03-01"
    assert c["future_allowed_source_end_date"] == "2024-11-30"
    assert c["v002_terminal_start_date"] == "2024-12-01"
    assert c["v002_terminal_end_date"] == "2025-02-28"
    assert c["sealed_test_start_date"] == "2025-02-14"
    assert c["sealed_test_end_date"] == "2025-02-28"


def test_contract_is_json_serialisable() -> None:
    import json

    payload = json.dumps(policy.build_split_policy_contract())
    assert policy.SPLIT_POLICY_NAME in payload


# ---------------------------------------------------------------------------
# 40. Stable public exports
# ---------------------------------------------------------------------------


def test_public_exports_stable() -> None:
    for name in policy.__all__:
        assert hasattr(policy, name), name
    for required in (
        "SPLIT_POLICY_NAME",
        "split_for_date",
        "split_for_timestamp_ms",
        "is_earlier_split_boundary_crossing",
        "validate_policy_arithmetic",
        "build_split_policy_contract",
        "PreV002SplitPolicyError",
    ):
        assert required in policy.__all__


# ---------------------------------------------------------------------------
# Extra: embargo window + per-horizon window arithmetic
# ---------------------------------------------------------------------------


def test_earlier_split_embargo_window_arithmetic() -> None:
    assert policy.earlier_split_embargo_window_ms(policy.TRAIN) == (
        policy.BOUNDARY_TRAIN_VALIDATION_MS - 60_000,
        policy.BOUNDARY_TRAIN_VALIDATION_MS,
    )
    assert policy.earlier_split_embargo_window_ms(policy.VALIDATION) == (
        policy.BOUNDARY_VALIDATION_HOLDOUT_MS - 60_000,
        policy.BOUNDARY_VALIDATION_HOLDOUT_MS,
    )
    assert policy.is_embargoed(
        policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS - 1
    )
    assert not policy.is_embargoed(
        policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS - 60_001
    )


def test_boundary_crossing_window_per_horizon() -> None:
    for ms in policy.ALLOWED_HORIZONS_MS:
        assert policy.boundary_crossing_window_ms(policy.TRAIN, ms) == (
            policy.BOUNDARY_TRAIN_VALIDATION_MS - ms,
            policy.BOUNDARY_TRAIN_VALIDATION_MS,
        )
        assert policy.boundary_crossing_window_ms(policy.VALIDATION, ms) == (
            policy.BOUNDARY_VALIDATION_HOLDOUT_MS - ms,
            policy.BOUNDARY_VALIDATION_HOLDOUT_MS,
        )
