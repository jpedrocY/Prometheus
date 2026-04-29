"""D1-A FundingAwareConfig locked-spec preservation tests.

Phase 3g §6 + §5.6.5 Option A locks every field at a single value;
the model must:

    - default to those locked values exactly,
    - reject any override (via Field constraints OR model_post_init),
    - be frozen + extra=forbid (no regime_filter or other fields),
    - round-trip through model_dump_json / model_validate_json.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from prometheus.strategy.funding_aware_directional import FundingAwareConfig
from prometheus.strategy.funding_aware_directional.variant_config import (
    COOLDOWN_RULE,
    DIRECTION_LOGIC,
    FUNDING_Z_SCORE_LOOKBACK_DAYS,
    FUNDING_Z_SCORE_LOOKBACK_EVENTS,
    FUNDING_Z_SCORE_THRESHOLD,
    STOP_DISTANCE_ATR_MULTIPLIER,
    STOP_DISTANCE_MAX_ATR,
    STOP_DISTANCE_MIN_ATR,
    TARGET_R_MULTIPLE,
    TIME_STOP_BARS,
)


def test_default_config_matches_phase_3g_locked_values() -> None:
    cfg = FundingAwareConfig()
    assert cfg.funding_z_score_threshold == 2.0
    assert cfg.funding_z_score_lookback_days == 90
    assert cfg.funding_z_score_lookback_events == 270
    assert cfg.stop_distance_atr_multiplier == 1.0
    assert cfg.target_r_multiple == 2.0
    assert cfg.time_stop_bars == 32
    assert cfg.cooldown_rule == "per_funding_event"
    assert cfg.stop_distance_min_atr == 0.60
    assert cfg.stop_distance_max_atr == 1.80
    assert cfg.direction_logic == "contrarian"


def test_default_config_uses_module_constants() -> None:
    cfg = FundingAwareConfig()
    assert cfg.funding_z_score_threshold == FUNDING_Z_SCORE_THRESHOLD
    assert cfg.funding_z_score_lookback_days == FUNDING_Z_SCORE_LOOKBACK_DAYS
    assert cfg.funding_z_score_lookback_events == FUNDING_Z_SCORE_LOOKBACK_EVENTS
    assert cfg.stop_distance_atr_multiplier == STOP_DISTANCE_ATR_MULTIPLIER
    assert cfg.target_r_multiple == TARGET_R_MULTIPLE
    assert cfg.time_stop_bars == TIME_STOP_BARS
    assert cfg.cooldown_rule == COOLDOWN_RULE
    assert cfg.stop_distance_min_atr == STOP_DISTANCE_MIN_ATR
    assert cfg.stop_distance_max_atr == STOP_DISTANCE_MAX_ATR
    assert cfg.direction_logic == DIRECTION_LOGIC


def test_baseline_classmethod_is_default() -> None:
    assert FundingAwareConfig.baseline() == FundingAwareConfig()


def test_config_is_frozen() -> None:
    cfg = FundingAwareConfig()
    with pytest.raises(Exception):  # noqa: B017 — pydantic frozen raises ValidationError
        cfg.funding_z_score_threshold = 1.5  # type: ignore[misc]


def test_config_rejects_extra_fields_including_regime_filter() -> None:
    """Phase 3g §6.13: regime_filter is None — extra=forbid prevents
    callers from passing one."""
    with pytest.raises(ValidationError):
        FundingAwareConfig(regime_filter="low_vol_only")  # type: ignore[call-arg]


def test_rejects_alternate_threshold() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(funding_z_score_threshold=1.5)


def test_rejects_alternate_target() -> None:
    """Phase 3g §5.6.5 Option A: target locked at +2.0R; +1.0R, +1.5R,
    +3.0R all rejected."""
    with pytest.raises(ValidationError):
        FundingAwareConfig(target_r_multiple=1.0)
    with pytest.raises(ValidationError):
        FundingAwareConfig(target_r_multiple=1.5)
    with pytest.raises(ValidationError):
        FundingAwareConfig(target_r_multiple=3.0)


def test_rejects_alternate_lookback_days() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(funding_z_score_lookback_days=60)


def test_rejects_alternate_lookback_events() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(funding_z_score_lookback_events=180)


def test_rejects_alternate_time_stop() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(time_stop_bars=16)
    with pytest.raises(ValidationError):
        FundingAwareConfig(time_stop_bars=64)


def test_rejects_alternate_stop_distance_multiplier() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(stop_distance_atr_multiplier=0.50)


def test_rejects_alternate_stop_distance_band() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(stop_distance_min_atr=0.30)
    with pytest.raises(ValidationError):
        FundingAwareConfig(stop_distance_max_atr=2.50)


def test_rejects_non_contrarian_direction_logic() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(direction_logic="momentum")  # type: ignore[arg-type]


def test_rejects_non_per_funding_event_cooldown() -> None:
    with pytest.raises(ValidationError):
        FundingAwareConfig(cooldown_rule="bar_count")  # type: ignore[arg-type]


def test_round_trip_json() -> None:
    cfg = FundingAwareConfig()
    blob = cfg.model_dump_json()
    rt = FundingAwareConfig.model_validate_json(blob)
    assert rt == cfg
