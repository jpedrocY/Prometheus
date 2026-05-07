"""Tests for the public-only microstructure scaffold config (Phase 4aw)."""

from __future__ import annotations

import pytest

from prometheus.research.microstructure.allowlist import EndpointNotAllowedError
from prometheus.research.microstructure.config import (
    ConfigValidationError,
    DatasetFamilyConfig,
    EligibilityGateThresholds,
    InvalidWindowThresholds,
    MicrostructureConfig,
    validate_config,
)


def _valid_family() -> DatasetFamilyConfig:
    return DatasetFamilyConfig(
        family="microstructure_raw_aggtrades_v001",
        layer="raw",
        capture_mode="ws_live_capture_required",
        schema_version="v001",
        endpoint_docs_reference="phase-4at-section-6.1",
    )


def _valid_config(**overrides: object) -> MicrostructureConfig:
    base: dict[str, object] = {
        "endpoint_allowlist": ("@aggTrade", "@bookTicker"),
        "endpoint_denylist": ("/fapi/v1/order", "userDataStream"),
        "symbol_allowlist": ("BTCUSDT", "ETHUSDT"),
        "storage_root": "data/microstructure",
        "dataset_family_config": (_valid_family(),),
    }
    base.update(overrides)
    return MicrostructureConfig(**base)  # type: ignore[arg-type]


def test_valid_config_passes() -> None:
    validate_config(_valid_config())


def test_default_thresholds_used_when_omitted() -> None:
    config = _valid_config()
    assert isinstance(config.invalid_window_thresholds, InvalidWindowThresholds)
    assert isinstance(config.eligibility_gate_thresholds, EligibilityGateThresholds)


def test_empty_allowlist_rejected() -> None:
    with pytest.raises(ConfigValidationError):
        validate_config(_valid_config(endpoint_allowlist=()))


def test_duplicate_allowlist_entry_rejected() -> None:
    with pytest.raises(ConfigValidationError):
        validate_config(_valid_config(endpoint_allowlist=("@aggTrade", "@aggTrade")))


def test_unknown_endpoint_in_allowlist_rejected() -> None:
    with pytest.raises(EndpointNotAllowedError):
        validate_config(_valid_config(endpoint_allowlist=("/fapi/v3/something",)))


def test_denylisted_endpoint_in_allowlist_rejected() -> None:
    with pytest.raises(EndpointNotAllowedError):
        validate_config(
            _valid_config(endpoint_allowlist=("/fapi/v1/order", "@aggTrade"))
        )


def test_credential_shaped_storage_root_rejected() -> None:
    with pytest.raises(ConfigValidationError):
        validate_config(_valid_config(storage_root="path/to/api_key/output"))


def test_unknown_symbol_rejected_without_explicit_extras() -> None:
    with pytest.raises(ConfigValidationError):
        validate_config(_valid_config(symbol_allowlist=("BTCUSDT", "SOLUSDT")))


def test_unknown_symbol_admitted_via_explicit_extras() -> None:
    validate_config(
        _valid_config(symbol_allowlist=("BTCUSDT", "SOLUSDT")),
        explicit_extra_symbols={"SOLUSDT": "phase-4ac-core-symbol"},
    )


def test_lowercase_symbol_rejected() -> None:
    with pytest.raises(ConfigValidationError):
        validate_config(_valid_config(symbol_allowlist=("btcusdt",)))


def test_dataset_family_layer_rejected_when_unknown() -> None:
    with pytest.raises(ConfigValidationError):
        DatasetFamilyConfig(
            family="microstructure_raw_aggtrades_v001",
            layer="not-a-layer",
            capture_mode="ws_live_capture_required",
            schema_version="v001",
            endpoint_docs_reference="phase-4at-section-6.1",
        )


def test_dataset_family_capture_mode_rejected_when_unknown() -> None:
    with pytest.raises(ConfigValidationError):
        DatasetFamilyConfig(
            family="microstructure_raw_aggtrades_v001",
            layer="raw",
            capture_mode="not-a-mode",
            schema_version="v001",
            endpoint_docs_reference="phase-4at-section-6.1",
        )


def test_invalid_window_thresholds_reject_negatives() -> None:
    with pytest.raises(ConfigValidationError):
        InvalidWindowThresholds(max_clock_skew_ms=-1)


def test_eligibility_gate_thresholds_reject_out_of_range_fraction() -> None:
    with pytest.raises(ConfigValidationError):
        EligibilityGateThresholds(max_invalid_window_fraction=1.5)


def test_denylist_block_can_contain_denylist_tokens() -> None:
    # The endpoint_denylist field is allowed to contain denylisted token
    # patterns — that is its purpose. Validation must not reject them.
    validate_config(
        _valid_config(
            endpoint_denylist=(
                "/fapi/v1/order",
                "/fapi/v1/forceOrders",
                "userDataStream",
                "listenKey",
                "api_key",
                ".mcp.json",
                "Graphify",
            )
        )
    )


def test_credential_shaped_family_rejected() -> None:
    # ``api_key`` is one of the canonical credential-shaped denylist tokens.
    with pytest.raises(ConfigValidationError):
        DatasetFamilyConfig(
            family="microstructure_api_key_aggtrades_v001",
            layer="raw",
            capture_mode="ws_live_capture_required",
            schema_version="v001",
            endpoint_docs_reference="phase-4at-section-6.1",
        )
