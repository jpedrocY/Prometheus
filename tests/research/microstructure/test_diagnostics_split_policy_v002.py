"""Unit tests for the Phase 4bm-W chronological split-policy helpers.

Pure, offline tests of
:mod:`prometheus.research.microstructure.diagnostics_split_policy_v002`.
No network, no filesystem mutation, no parquet I/O.
"""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    diagnostics_split_policy_v002 as policy,
)


def test_date_counts_match_recorded_policy() -> None:
    assert len(policy.train_dates()) == policy.EXPECTED_TRAIN_DATE_COUNT == 45
    assert (
        len(policy.validation_dates())
        == policy.EXPECTED_VALIDATION_DATE_COUNT
        == 30
    )
    assert len(policy.test_dates()) == policy.EXPECTED_TEST_DATE_COUNT == 15
    assert len(policy.all_dates()) == policy.EXPECTED_TOTAL_DATE_COUNT == 90


def test_all_dates_contiguous_and_disjoint() -> None:
    all_d = policy.all_dates()
    assert all_d[0] == "2024-12-01"
    assert all_d[-1] == "2025-02-28"
    union = set(policy.train_dates()) | set(policy.validation_dates()) | set(
        policy.test_dates()
    )
    assert union == set(all_d)
    assert len(union) == 90  # disjoint (no overlap)


@pytest.mark.parametrize(
    "date,expected",
    [
        ("2024-12-01", policy.TRAIN),
        ("2025-01-14", policy.TRAIN),
        ("2025-01-15", policy.VALIDATION),
        ("2025-02-13", policy.VALIDATION),
        ("2025-02-14", policy.TEST),
        ("2025-02-28", policy.TEST),
    ],
)
def test_split_for_date_boundaries(date: str, expected: str) -> None:
    assert policy.split_for_date(date) == expected


def test_split_for_date_out_of_envelope_raises() -> None:
    with pytest.raises(policy.SplitPolicyError):
        policy.split_for_date("2024-11-30")
    with pytest.raises(policy.SplitPolicyError):
        policy.split_for_date("2025-03-01")


def test_boundary_ms_constants() -> None:
    assert policy.BOUNDARY_TRAIN_VALIDATION_MS == 1736899200000
    assert policy.BOUNDARY_VALIDATION_TEST_MS == 1739491200000
    assert policy.MIN_BOUNDARY_EMBARGO_MS == 60_000


def test_split_for_source_transact_time_ms() -> None:
    # 1 ms before T_TV is still 2025-01-14 (train); exactly T_TV is validation.
    assert (
        policy.split_for_source_transact_time_ms(
            policy.BOUNDARY_TRAIN_VALIDATION_MS - 1
        )
        == policy.TRAIN
    )
    assert (
        policy.split_for_source_transact_time_ms(
            policy.BOUNDARY_TRAIN_VALIDATION_MS
        )
        == policy.VALIDATION
    )
    assert (
        policy.split_for_source_transact_time_ms(
            policy.BOUNDARY_VALIDATION_TEST_MS
        )
        == policy.TEST
    )


def test_embargo_window_and_predicate() -> None:
    win = policy.earlier_split_embargo_window_ms(policy.TRAIN)
    assert win == (
        policy.BOUNDARY_TRAIN_VALIDATION_MS - 60_000,
        policy.BOUNDARY_TRAIN_VALIDATION_MS,
    )
    # Just inside the embargo window (excluded from train).
    assert policy.is_embargoed(policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS - 1)
    assert policy.is_embargoed(
        policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS - 60_000
    )
    # One ms before the window: not embargoed.
    assert not policy.is_embargoed(
        policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS - 60_001
    )
    # The boundary itself belongs to the later split; not an earlier-split row.
    assert not policy.is_embargoed(
        policy.TRAIN, policy.BOUNDARY_TRAIN_VALIDATION_MS
    )


def test_test_split_never_embargoed() -> None:
    assert policy.earlier_split_embargo_window_ms(policy.TEST) is None
    assert not policy.is_embargoed(policy.TEST, policy.BOUNDARY_VALIDATION_TEST_MS)


def test_boundary_crossing_window_per_horizon() -> None:
    for h, ms in policy.HORIZON_MS.items():
        win = policy.boundary_crossing_window_ms(policy.TRAIN, h)
        assert win == (
            policy.BOUNDARY_TRAIN_VALIDATION_MS - ms,
            policy.BOUNDARY_TRAIN_VALIDATION_MS,
        )
    assert policy.boundary_crossing_window_ms(policy.TEST, "60s") is None


def test_snapshot_is_serialisable_and_records_prohibited_uses() -> None:
    snap = policy.SplitPolicySnapshot().as_dict()
    assert snap["split_policy_name"] == policy.SPLIT_POLICY_NAME
    assert snap["no_shuffle_rule"] is True
    assert snap["random_split_allowed"] is False
    assert set(snap["prohibited_test_holdout_uses"]) == set(
        policy.PROHIBITED_TEST_HOLDOUT_USES
    )
    assert len(policy.PROHIBITED_TEST_HOLDOUT_USES) == 7
