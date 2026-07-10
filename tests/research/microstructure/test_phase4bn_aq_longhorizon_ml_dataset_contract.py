"""Phase 4bn-AQ — offline tests for the long-horizon ML dataset contract.

Pure constant / validator tests over the inert contract module only. They read
no data, build no dataset, and train nothing.
"""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import (
    longhorizon_labels_schema_v001 as lh_labels,
)
from prometheus.research.microstructure import (
    longhorizon_ml_dataset_contract_v001 as contract,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_builder as builder,
)
from prometheus.research.microstructure import (
    pre_v002_ml_dataset_contract as ah_contract,
)
from prometheus.research.microstructure import (
    pre_v002_split_policy as sp,
)

# ---------------------------------------------------------------------------
# Identity
# ---------------------------------------------------------------------------


def test_dataset_family_and_contract_identity_are_new_and_distinct():
    assert contract.DATASET_FAMILY == "microstructure_ml_dataset_longhorizon_pre_v001"
    assert contract.CONTRACT_NAME == (
        "microstructure_longhorizon_ml_dataset_aggtrades_pre_v002_contract_v001"
    )
    # Distinct from the frozen short-horizon 15s dataset contract.
    assert contract.CONTRACT_NAME != ah_contract.CONTRACT_NAME
    assert contract.SIBLING_SHORT_HORIZON_CONTRACT == ah_contract.CONTRACT_NAME
    assert contract.DATASET_FAMILY != ah_contract.CONTRACT_NAME


def test_amendment_id_shared_with_ae_prereg_layer():
    assert contract.CONTRACT_AMENDMENT_ID == ah_contract.CONTRACT_AMENDMENT_ID
    assert contract.CONTRACT_AMENDMENT_ID == "amendment_001"


def test_source_scope_matches_admitted_pre_v002_segment():
    assert contract.SYMBOL == "BTCUSDT"
    assert contract.MARKET == "binance_usdm_futures"
    assert contract.SOURCE_FAMILY == "aggTrades"
    assert contract.START_DATE == "2024-03-01"
    assert contract.END_DATE == "2024-11-30"
    assert contract.EXPECTED_PARTITION_COUNT == 275
    assert contract.EXPECTED_ROW_COUNT == 400_001_695


# ---------------------------------------------------------------------------
# Feature scope
# ---------------------------------------------------------------------------


def test_feature_count_is_45_and_allowlist_identical_to_ah():
    assert contract.FEATURE_COUNT == 45
    assert len(contract.ALLOWED_FEATURE_COLUMNS) == 45
    assert len(set(contract.ALLOWED_FEATURE_COLUMNS)) == 45
    # The long-horizon dataset reuses the exact AH 45-feature allowlist unchanged.
    assert contract.ALLOWED_FEATURE_COLUMNS == ah_contract.ALLOWED_FEATURE_COLUMNS


def test_forbidden_feature_substring_scan_is_clean():
    found = builder.find_forbidden_columns(contract.ALLOWED_FEATURE_COLUMNS)
    assert found == ()


def test_feature_allowlist_disjoint_from_labels_support_and_censoring():
    # Explicit validator does not raise …
    contract.validate_feature_scope_disjoint_from_labels()
    # … and no label / support / return / censoring column is an allowed feature.
    feats = set(contract.ALLOWED_FEATURE_COLUMNS)
    for col in (
        *contract.DIRECTION_TARGET_COLUMNS,
        *contract.RETURN_METADATA_COLUMNS,
        *contract.LABEL_SUPPORT_COLUMNS,
        contract.LABEL_INVALID_PRICE_FLAG,
        contract.LABEL_ANY_CENSORED_FLAG,
    ):
        assert col not in feats


def test_labels_and_returns_not_present_in_feature_list():
    for col in contract.ALLOWED_FEATURE_COLUMNS:
        assert "forward_direction" not in col
        assert "forward_log_return" not in col
        assert "horizon_censored_flag" not in col
        assert not col.startswith("reference_")
        assert not col.startswith("split_")


# ---------------------------------------------------------------------------
# Label binding
# ---------------------------------------------------------------------------


def test_label_family_and_hash_binding():
    assert contract.LABEL_FAMILY == lh_labels.LONGHORIZON_LABEL_DATASET_FAMILY
    assert contract.LABEL_FAMILY == "microstructure_labels_longhorizon_aggtrades_v001"
    assert contract.LABEL_CONFIG_HASH == (
        "edaeafde5cb302158baa6eac197edde363d6b0a9b2c042957e35c56e1553c118"
    )
    # Must not be a rejected out-of-scope label identity.
    assert contract.LABEL_CONFIG_HASH != contract.REJECTED_V002_LABEL_CONFIG_HASH
    assert contract.LABEL_CONFIG_HASH != (
        contract.REJECTED_SHORT_HORIZON_LABEL_CONFIG_HASH
    )


def test_target_horizon_set_and_primary_secondary_roles():
    assert contract.HORIZONS == ("5m", "30m", "1h")
    assert contract.HORIZON_MS == (300_000, 1_800_000, 3_600_000)
    assert contract.PRIMARY_HORIZON == "5m"
    assert contract.PRIMARY_TARGET == "forward_direction_5m"
    assert contract.PRIMARY_HORIZON_MS == 300_000
    assert contract.SECONDARY_HORIZONS == ("30m", "1h")
    assert contract.SECONDARY_TARGETS == (
        "forward_direction_30m",
        "forward_direction_1h",
    )
    contract.validate_target_horizons(contract.HORIZONS)


def test_validate_target_horizons_rejects_short_horizon_set():
    with pytest.raises(contract.LongHorizonMlDatasetContractError):
        contract.validate_target_horizons(("1s", "5s", "15s", "60s"))


def test_direction_and_support_column_maps():
    assert contract.DIRECTION_COLUMN_BY_HORIZON == {
        "5m": "forward_direction_5m",
        "30m": "forward_direction_30m",
        "1h": "forward_direction_1h",
    }
    assert contract.CENSORED_FLAG_COLUMN_BY_HORIZON["5m"] == "horizon_censored_flag_5m"
    assert contract.REFERENCE_TIMESTAMP_COLUMN_BY_HORIZON["1h"] == (
        "reference_timestamp_ms_1h"
    )
    assert contract.TARGET_CLASSES == (-1, 0, 1)


# ---------------------------------------------------------------------------
# Split / transform / posture
# ---------------------------------------------------------------------------


def test_split_policy_identity_is_the_shared_pre_v002_chrono_policy():
    assert contract.SPLIT_POLICY_NAME == sp.SPLIT_POLICY_NAME
    assert contract.SPLIT_POLICY_NAME == (
        "CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO"
    )
    assert contract.EXPECTED_SPLIT_DATE_COUNTS == {
        "train": 214,
        "embargo_1": 1,
        "validation": 45,
        "embargo_2": 1,
        "holdout": 14,
    }


def test_train_only_transform_policy_matches_aj_ap_lock():
    assert contract.STANDARDIZATION_RULE == (
        "subtract_train_mean_divide_by_max_train_std_epsilon"
    )
    assert contract.STANDARDIZATION_EPSILON == 1e-8
    assert contract.STANDARDIZE_BOOLEAN_FLAGS is False
    assert contract.TRAIN_ONLY_FIT_SPLIT == "train"


def test_output_namespace_is_new_gitignored_and_not_ah_namespace():
    assert contract.OUTPUT_NAMESPACE == (
        "data/research/microstructure/ml_datasets/longhorizon_pre_v001"
    )
    assert contract.OUTPUT_NAMESPACE.startswith("data/research/")
    assert ah_contract.OUTPUT_NAMESPACE_PATH.rstrip("/") != contract.OUTPUT_NAMESPACE


def test_all_non_authorization_flags_false():
    assert set(contract.NON_AUTHORIZATION_FLAGS) == {
        "ml_authorized",
        "diagnostics_authorized",
        "strategy_authorized",
        "signals_authorized",
        "pnl_authorized",
        "backtest_authorized",
        "live_authorized",
        "exchange_write_authorized",
    }
    assert all(v is False for v in contract.NON_AUTHORIZATION_FLAGS.values())


def test_cost_lock_descriptive_only():
    assert contract.LOCKED_COST_BPS_PER_SIDE == 8.0
    assert contract.LOCKED_ROUND_TRIP_COST_BPS == 16.0
