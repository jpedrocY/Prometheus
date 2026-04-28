"""F1 MeanReversionConfig locked-spec preservation tests.

Phase 3b §4 locks every field at a single value; the model must:

    - default to those locked values exactly,
    - reject any override (via Field constraints OR model_post_init),
    - be frozen + extra=forbid,
    - round-trip through model_dump_json / model_validate_json.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prometheus.strategy.mean_reversion_overextension import MeanReversionConfig
from prometheus.strategy.mean_reversion_overextension.variant_config import (
    MEAN_REFERENCE_WINDOW_BARS,
    OVEREXTENSION_THRESHOLD_ATR_MULTIPLE,
    OVEREXTENSION_WINDOW_BARS,
    STOP_BUFFER_ATR_MULTIPLE,
    STOP_DISTANCE_MAX_ATR,
    STOP_DISTANCE_MIN_ATR,
    TIME_STOP_BARS,
)


def test_default_config_matches_phase_3b_locked_values() -> None:
    cfg = MeanReversionConfig()
    assert cfg.overextension_window_bars == 8
    assert cfg.overextension_threshold_atr_multiple == 1.75
    assert cfg.mean_reference_window_bars == 8
    assert cfg.stop_buffer_atr_multiple == 0.10
    assert cfg.time_stop_bars == 8
    assert cfg.stop_distance_min_atr == 0.60
    assert cfg.stop_distance_max_atr == 1.80


def test_default_config_uses_module_constants() -> None:
    cfg = MeanReversionConfig()
    assert cfg.overextension_window_bars == OVEREXTENSION_WINDOW_BARS
    assert cfg.overextension_threshold_atr_multiple == OVEREXTENSION_THRESHOLD_ATR_MULTIPLE
    assert cfg.mean_reference_window_bars == MEAN_REFERENCE_WINDOW_BARS
    assert cfg.stop_buffer_atr_multiple == STOP_BUFFER_ATR_MULTIPLE
    assert cfg.time_stop_bars == TIME_STOP_BARS
    assert cfg.stop_distance_min_atr == STOP_DISTANCE_MIN_ATR
    assert cfg.stop_distance_max_atr == STOP_DISTANCE_MAX_ATR


def test_baseline_classmethod_is_default() -> None:
    assert MeanReversionConfig.baseline() == MeanReversionConfig()


def test_config_is_frozen() -> None:
    cfg = MeanReversionConfig()
    with pytest.raises(Exception):  # noqa: B017 — pydantic frozen raises ValidationError
        cfg.overextension_window_bars = 10  # type: ignore[misc]


def test_config_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(unknown_axis=1)  # type: ignore[call-arg]


def test_override_overextension_window_bars_rejected() -> None:
    # Field constraint (ge=8, le=8) blocks at validation time.
    with pytest.raises(ValidationError):
        MeanReversionConfig(overextension_window_bars=10)


def test_override_overextension_threshold_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(overextension_threshold_atr_multiple=2.0)


def test_override_mean_reference_window_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(mean_reference_window_bars=12)


def test_override_stop_buffer_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(stop_buffer_atr_multiple=0.20)


def test_override_time_stop_bars_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(time_stop_bars=16)


def test_override_stop_distance_min_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(stop_distance_min_atr=0.50)


def test_override_stop_distance_max_rejected() -> None:
    with pytest.raises(ValidationError):
        MeanReversionConfig(stop_distance_max_atr=2.50)


def test_explicit_locked_values_accepted() -> None:
    cfg = MeanReversionConfig(
        overextension_window_bars=8,
        overextension_threshold_atr_multiple=1.75,
        mean_reference_window_bars=8,
        stop_buffer_atr_multiple=0.10,
        time_stop_bars=8,
        stop_distance_min_atr=0.60,
        stop_distance_max_atr=1.80,
    )
    assert cfg == MeanReversionConfig()


def test_round_trip_json() -> None:
    cfg = MeanReversionConfig()
    payload = cfg.model_dump_json()
    restored = MeanReversionConfig.model_validate_json(payload)
    assert restored == cfg
