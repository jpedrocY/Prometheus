"""Governance label schemes (single source of truth).

Per Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3, four governance label
schemes are binding prospectively on any future evidence or runtime
artefact: ``stop_trigger_domain``, ``break_even_rule``,
``ema_slope_method``, ``stagnation_window_role``. For all four schemes,
``mixed_or_unknown`` is invalid and must fail closed at any decision
boundary (block trade / block verdict / block persist / block
evidence-promotion).

This module is the *single* code-level source of truth for the four
schemes. All Phase 4a runtime code paths that touch governed semantics
(persistence, event validation, risk-engine validation, fake-exchange
adapter, read-only state view) import from this module rather than
copying value lists.
"""

from __future__ import annotations

from enum import StrEnum

from .errors import PrometheusError


class GovernanceLabelError(PrometheusError):
    """Raised when a governance label is invalid or `mixed_or_unknown`.

    Per Phase 3v §8.4 / Phase 3w §6.3 / §7.3 / §8.3, any decision
    boundary encountering an ambiguous or out-of-scheme label value
    must fail closed; raising this exception is the canonical fail-
    closed signal.
    """


class StopTriggerDomain(StrEnum):
    """Phase 3v §8.4 stop-trigger domain label scheme.

    - ``trade_price_backtest``: historical or research backtest using
      trade-price stop-trigger modeling.
    - ``mark_price_runtime``: future runtime / paper / live stop-trigger
      pathway using ``workingType=MARK_PRICE``. Required for any
      artifact claiming live-readiness relevance.
    - ``mark_price_backtest_candidate``: research backtest explicitly
      modeling mark-price stop-triggers.
    - ``mixed_or_unknown``: invalid; fails closed at any decision
      boundary.
    """

    TRADE_PRICE_BACKTEST = "trade_price_backtest"
    MARK_PRICE_RUNTIME = "mark_price_runtime"
    MARK_PRICE_BACKTEST_CANDIDATE = "mark_price_backtest_candidate"
    MIXED_OR_UNKNOWN = "mixed_or_unknown"


class BreakEvenRule(StrEnum):
    """Phase 3w §6.3 break-even rule label scheme.

    - ``disabled``: no break-even step (R3 / F1 / D1-A historical
      provenance).
    - ``enabled_plus_1_5R_mfe``: Stage-4 break-even at +1.5R MFE
      (H0 / R1a / R1b-narrow / R2 historical provenance per spec
      line 380).
    - ``enabled_plus_2_0R_mfe``: Stage-4 break-even at +2.0R MFE
      (H-D3 wave-1 variant provenance; not retained-evidence).
    - ``enabled_other_predeclared``: any other predeclared rule with
      explicit MFE threshold and explicit predeclared evaluation
      threshold.
    - ``mixed_or_unknown``: invalid; fails closed.
    """

    DISABLED = "disabled"
    ENABLED_PLUS_1_5R_MFE = "enabled_plus_1_5R_mfe"
    ENABLED_PLUS_2_0R_MFE = "enabled_plus_2_0R_mfe"
    ENABLED_OTHER_PREDECLARED = "enabled_other_predeclared"
    MIXED_OR_UNKNOWN = "mixed_or_unknown"


class EmaSlopeMethod(StrEnum):
    """Phase 3w §7.3 EMA-slope method label scheme.

    - ``discrete_comparison``: ``EMA[now] > EMA[now − 3h]`` (long);
      ``EMA[now] < EMA[now − 3h]`` (short). Canonical for V1-family
      retained-evidence backtests.
    - ``fitted_slope``: regression-fit slope over last N completed 1h
      bars with N predeclared. Not used by any retained-evidence
      backtest.
    - ``other_predeclared``: any other predeclared method with explicit
      specification.
    - ``not_applicable``: for strategy families that do not use 1h EMA
      bias as primary entry filter (F1 / D1-A historical provenance).
    - ``mixed_or_unknown``: invalid; fails closed.
    """

    DISCRETE_COMPARISON = "discrete_comparison"
    FITTED_SLOPE = "fitted_slope"
    OTHER_PREDECLARED = "other_predeclared"
    NOT_APPLICABLE = "not_applicable"
    MIXED_OR_UNKNOWN = "mixed_or_unknown"


class StagnationWindowRole(StrEnum):
    """Phase 3w §8.3 stagnation-window role label scheme.

    - ``not_active``: no stagnation rule applied (R3 / F1 / D1-A
      historical provenance).
    - ``metric_only``: observed and reported as a trade-quality metric
      but does NOT alter exit behavior. May not be used to silently
      re-introduce an active stagnation rule.
    - ``active_rule_predeclared``: stagnation rule active with
      predeclared ``stagnation_bars`` and ``stagnation_min_mfe_R``
      configuration (H0 / R1a / R1b-narrow / R2 historical provenance
      per spec line 415: ``stagnation_bars = 8``,
      ``stagnation_min_mfe_R = +1.0R``).
    - ``mixed_or_unknown``: invalid; fails closed.
    """

    NOT_ACTIVE = "not_active"
    METRIC_ONLY = "metric_only"
    ACTIVE_RULE_PREDECLARED = "active_rule_predeclared"
    MIXED_OR_UNKNOWN = "mixed_or_unknown"


# All four label types form a closed set.
GovernanceLabel = (
    StopTriggerDomain | BreakEvenRule | EmaSlopeMethod | StagnationWindowRole
)


def is_fail_closed(label: GovernanceLabel) -> bool:
    """Return True iff the label value is the ``mixed_or_unknown`` sentinel.

    The sentinel is invalid at any decision boundary per Phase 3v §8.4
    and Phase 3w §6.3 / §7.3 / §8.3.
    """
    return label.value == "mixed_or_unknown"


def require_valid(label: GovernanceLabel) -> None:
    """Raise ``GovernanceLabelError`` if the label is fail-closed.

    Use this at every decision boundary that consumes a governance
    label (trade-execution, verdict, persistence, event-validation,
    fake-exchange decision).
    """
    if is_fail_closed(label):
        raise GovernanceLabelError(
            f"governance label {label.__class__.__name__} is "
            f"'mixed_or_unknown'; failing closed per Phase 3v §8.4 / "
            f"Phase 3w §6.3 / §7.3 / §8.3"
        )


def parse_stop_trigger_domain(value: str) -> StopTriggerDomain:
    """Parse a stop_trigger_domain string; raise on invalid value.

    Always returns a member of ``StopTriggerDomain``; ``mixed_or_unknown``
    is parsed but separately fails closed via ``require_valid``.
    """
    try:
        return StopTriggerDomain(value)
    except ValueError as exc:
        raise GovernanceLabelError(
            f"invalid stop_trigger_domain value: {value!r}"
        ) from exc


def parse_break_even_rule(value: str) -> BreakEvenRule:
    """Parse a break_even_rule string; raise on invalid value."""
    try:
        return BreakEvenRule(value)
    except ValueError as exc:
        raise GovernanceLabelError(
            f"invalid break_even_rule value: {value!r}"
        ) from exc


def parse_ema_slope_method(value: str) -> EmaSlopeMethod:
    """Parse an ema_slope_method string; raise on invalid value."""
    try:
        return EmaSlopeMethod(value)
    except ValueError as exc:
        raise GovernanceLabelError(
            f"invalid ema_slope_method value: {value!r}"
        ) from exc


def parse_stagnation_window_role(value: str) -> StagnationWindowRole:
    """Parse a stagnation_window_role string; raise on invalid value."""
    try:
        return StagnationWindowRole(value)
    except ValueError as exc:
        raise GovernanceLabelError(
            f"invalid stagnation_window_role value: {value!r}"
        ) from exc
