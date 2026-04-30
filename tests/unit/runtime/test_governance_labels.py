"""Phase 4a tests for the four governance label schemes.

Each scheme must reject ``mixed_or_unknown`` via ``require_valid``,
and parsing functions must reject out-of-scheme values.
"""

from __future__ import annotations

import pytest

from prometheus.core.governance import (
    BreakEvenRule,
    EmaSlopeMethod,
    GovernanceLabelError,
    StagnationWindowRole,
    StopTriggerDomain,
    is_fail_closed,
    parse_break_even_rule,
    parse_ema_slope_method,
    parse_stagnation_window_role,
    parse_stop_trigger_domain,
    require_valid,
)


def test_stop_trigger_domain_values_match_phase_3v_8_4() -> None:
    """Phase 3v §8.4 enumerates exactly four values."""
    expected = {
        "trade_price_backtest",
        "mark_price_runtime",
        "mark_price_backtest_candidate",
        "mixed_or_unknown",
    }
    assert {member.value for member in StopTriggerDomain} == expected


def test_break_even_rule_values_match_phase_3w_6_3() -> None:
    expected = {
        "disabled",
        "enabled_plus_1_5R_mfe",
        "enabled_plus_2_0R_mfe",
        "enabled_other_predeclared",
        "mixed_or_unknown",
    }
    assert {member.value for member in BreakEvenRule} == expected


def test_ema_slope_method_values_match_phase_3w_7_3() -> None:
    expected = {
        "discrete_comparison",
        "fitted_slope",
        "other_predeclared",
        "not_applicable",
        "mixed_or_unknown",
    }
    assert {member.value for member in EmaSlopeMethod} == expected


def test_stagnation_window_role_values_match_phase_3w_8_3() -> None:
    expected = {
        "not_active",
        "metric_only",
        "active_rule_predeclared",
        "mixed_or_unknown",
    }
    assert {member.value for member in StagnationWindowRole} == expected


@pytest.mark.parametrize(
    "label",
    [
        StopTriggerDomain.MIXED_OR_UNKNOWN,
        BreakEvenRule.MIXED_OR_UNKNOWN,
        EmaSlopeMethod.MIXED_OR_UNKNOWN,
        StagnationWindowRole.MIXED_OR_UNKNOWN,
    ],
)
def test_require_valid_rejects_mixed_or_unknown(label: object) -> None:
    """Phase 3v §8.4 / Phase 3w §6.3 / §7.3 / §8.3 fail-closed rule."""
    assert is_fail_closed(label)  # type: ignore[arg-type]
    with pytest.raises(GovernanceLabelError):
        require_valid(label)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "label",
    [
        StopTriggerDomain.MARK_PRICE_RUNTIME,
        StopTriggerDomain.TRADE_PRICE_BACKTEST,
        StopTriggerDomain.MARK_PRICE_BACKTEST_CANDIDATE,
        BreakEvenRule.DISABLED,
        BreakEvenRule.ENABLED_PLUS_1_5R_MFE,
        EmaSlopeMethod.DISCRETE_COMPARISON,
        EmaSlopeMethod.NOT_APPLICABLE,
        StagnationWindowRole.NOT_ACTIVE,
        StagnationWindowRole.ACTIVE_RULE_PREDECLARED,
    ],
)
def test_require_valid_accepts_in_scheme_values(label: object) -> None:
    require_valid(label)  # type: ignore[arg-type]
    assert not is_fail_closed(label)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "parser, bad_value",
    [
        (parse_stop_trigger_domain, "mark_price"),
        (parse_break_even_rule, "enabled_plus_3_0R_mfe"),
        (parse_ema_slope_method, "linear_fit"),
        (parse_stagnation_window_role, "active"),
    ],
)
def test_parsers_reject_out_of_scheme_values(parser, bad_value: str) -> None:
    with pytest.raises(GovernanceLabelError):
        parser(bad_value)


def test_parsers_round_trip_in_scheme_values() -> None:
    assert (
        parse_stop_trigger_domain("mark_price_runtime")
        is StopTriggerDomain.MARK_PRICE_RUNTIME
    )
    assert parse_break_even_rule("disabled") is BreakEvenRule.DISABLED
    assert (
        parse_ema_slope_method("discrete_comparison")
        is EmaSlopeMethod.DISCRETE_COMPARISON
    )
    assert (
        parse_stagnation_window_role("not_active")
        is StagnationWindowRole.NOT_ACTIVE
    )


def test_governance_labels_share_single_source_of_truth() -> None:
    """``mixed_or_unknown`` must use the same string sentinel everywhere."""
    sentinel = "mixed_or_unknown"
    assert StopTriggerDomain.MIXED_OR_UNKNOWN.value == sentinel
    assert BreakEvenRule.MIXED_OR_UNKNOWN.value == sentinel
    assert EmaSlopeMethod.MIXED_OR_UNKNOWN.value == sentinel
    assert StagnationWindowRole.MIXED_OR_UNKNOWN.value == sentinel
