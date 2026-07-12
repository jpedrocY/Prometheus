"""Phase 4bn-AR — verdict-logic tests (frozen Phase 4bn-AP §24/§25 hierarchy).

Synthetic scalar-evidence tests: CONTINUE only when every strict 5m requirement
holds; 30m/1h can never upgrade a failed 5m to CONTINUE; a hard-negative holdout
reversal forces STOP; a clean absence of frozen positives is STOP; ambiguous bands
route to INVESTIGATE. Calibration classification is a diagnostic only.
"""

from __future__ import annotations

import pytest

from prometheus.research.microstructure import longhorizon_baseline_verdict_v001 as v


def _ev(horizon: str, **over) -> v.HorizonEvidence:
    """CONTINUE-passing baseline evidence for one horizon, overridable per field."""
    base = dict(
        horizon=horizon,
        val_acc_l2=0.55, val_acc_majority=0.50, val_acc_persistence=0.51,
        val_balacc_l2=0.40, val_balacc_majority=0.3333,
        val_macro_f1_l2=0.30, val_macro_f1_majority=0.22,
        holdout_acc_l2=0.54, holdout_acc_majority=0.50, holdout_acc_persistence=0.51,
        val_date_block_count=45, val_date_blocks_beat_both=40,
        val_month_block_count=2, val_month_blocks_beat_both=2,
        conf_tail_n=1000, conf_tail_acc=0.60, conf_tail_majority_acc=0.50,
        calibration_verdict=v.CALIBRATION_USABLE,
    )
    base.update(over)
    return v.HorizonEvidence(**base)


def _null(horizon: str, **over) -> v.HorizonEvidence:
    """Clean-null (no frozen positive) evidence for one horizon."""
    base = dict(
        horizon=horizon,
        val_acc_l2=0.500, val_acc_majority=0.500, val_acc_persistence=0.505,
        val_balacc_l2=0.3333, val_balacc_majority=0.3333,
        val_macro_f1_l2=0.22, val_macro_f1_majority=0.22,
        holdout_acc_l2=0.500, holdout_acc_majority=0.500, holdout_acc_persistence=0.505,
        val_date_block_count=45, val_date_blocks_beat_both=0,
        val_month_block_count=2, val_month_blocks_beat_both=0,
        conf_tail_n=0, conf_tail_acc=0.0, conf_tail_majority_acc=0.50,
        calibration_verdict=v.CALIBRATION_UNUSABLE,
    )
    base.update(over)
    return v.HorizonEvidence(**base)


# ---------------------------------------------------------------------------
# Calibration classification
# ---------------------------------------------------------------------------


def test_classify_calibration_usable_ranking_unusable() -> None:
    assert v.classify_calibration(tail_n=100, tail_acc=0.6, majority_acc=0.5, ece=0.02) == (
        v.CALIBRATION_USABLE
    )
    assert v.classify_calibration(tail_n=100, tail_acc=0.6, majority_acc=0.5, ece=0.20) == (
        v.CALIBRATION_RANKING_ONLY
    )
    assert v.classify_calibration(tail_n=0, tail_acc=0.0, majority_acc=0.5, ece=0.02) == (
        v.CALIBRATION_UNUSABLE
    )
    assert v.classify_calibration(tail_n=100, tail_acc=0.4, majority_acc=0.5, ece=0.02) == (
        v.CALIBRATION_UNUSABLE
    )


# ---------------------------------------------------------------------------
# CONTINUE
# ---------------------------------------------------------------------------


def test_continue_when_all_5m_requirements_hold() -> None:
    out = v.compute_longhorizon_verdict(
        primary=_ev("5m"), secondaries=[_ev("30m"), _ev("1h")]
    )
    assert out["verdict"] == v.VERDICT_CONTINUE
    assert out["ambiguous_conditions_matched"] == []
    assert out["stop_reasons"] == []


@pytest.mark.parametrize(
    "override",
    [
        {"val_acc_l2": 0.515},                       # +1.5pp maj: fails 2pp both-floors
        {"val_acc_persistence": 0.54},               # fails 2pp vs persistence
        {"val_macro_f1_l2": 0.24},                    # macro-F1 uplift < 0.03
        {"val_balacc_l2": 0.336},                     # balanced-acc uplift < 1.0pp
        {"val_date_blocks_beat_both": 10},            # date blocks not majority
        {"val_month_blocks_beat_both": 1},            # not every month
        {"conf_tail_n": 0},                           # no >=0.8 tail
        {"conf_tail_acc": 0.40},                      # tail does not beat majority floor
    ],
)
def test_continue_requires_every_strict_5m_criterion(override) -> None:
    out = v.compute_longhorizon_verdict(
        primary=_ev("5m", **override), secondaries=[_null("30m"), _null("1h")]
    )
    assert out["verdict"] != v.VERDICT_CONTINUE


# ---------------------------------------------------------------------------
# Secondary horizons cannot upgrade a failed 5m to CONTINUE
# ---------------------------------------------------------------------------


def test_secondary_positive_cannot_upgrade_failed_primary_to_continue() -> None:
    # 5m clearly fails; 30m + 1h are strongly positive.
    out = v.compute_longhorizon_verdict(
        primary=_null("5m"), secondaries=[_ev("30m"), _ev("1h")]
    )
    assert out["verdict"] == v.VERDICT_INVESTIGATE  # never CONTINUE
    assert (
        "primary_5m_not_clean_but_secondary_30m_or_1h_positive"
        in out["ambiguous_conditions_matched"]
    )
    assert out["secondary_positive_flags"] == {"30m": True, "1h": True}


# ---------------------------------------------------------------------------
# STOP
# ---------------------------------------------------------------------------


def test_stop_on_clean_null_no_secondary() -> None:
    out = v.compute_longhorizon_verdict(
        primary=_null("5m"), secondaries=[_null("30m"), _null("1h")]
    )
    assert out["verdict"] == v.VERDICT_STOP
    assert out["ambiguous_conditions_matched"] == []
    assert out["stop_reasons"]


def test_stop_on_holdout_full_reversal_even_with_validation_signal() -> None:
    # 5m looks good on validation but holdout reverses vs the majority floor.
    out = v.compute_longhorizon_verdict(
        primary=_ev("5m", holdout_acc_l2=0.49, holdout_acc_majority=0.50),
        secondaries=[_ev("30m"), _ev("1h")],
    )
    assert out["verdict"] == v.VERDICT_STOP
    assert any("holdout reverses" in r for r in out["stop_reasons"])


# ---------------------------------------------------------------------------
# INVESTIGATE
# ---------------------------------------------------------------------------


def test_investigate_on_classification_improves_but_blocks_fail() -> None:
    # Beats both floors + macro-F1, but block agreement fails and no reversal.
    out = v.compute_longhorizon_verdict(
        primary=_ev("5m", val_date_blocks_beat_both=5, val_month_blocks_beat_both=0),
        secondaries=[_null("30m"), _null("1h")],
    )
    assert out["verdict"] == v.VERDICT_INVESTIGATE


def test_investigate_on_classification_improves_but_calibration_fails() -> None:
    out = v.compute_longhorizon_verdict(
        primary=_ev("5m", conf_tail_acc=0.40, calibration_verdict=v.CALIBRATION_UNUSABLE),
        secondaries=[_null("30m"), _null("1h")],
    )
    assert out["verdict"] == v.VERDICT_INVESTIGATE
    assert (
        "classification_improves_but_calibration_fails"
        in out["ambiguous_conditions_matched"]
    )


def test_investigate_on_narrow_accuracy_miss_without_reversal() -> None:
    # +1.5pp over both floors: below the 2.0pp bar but >= the 1.0pp narrow floor;
    # no frozen sub-threshold met, no reversal -> INVESTIGATE (narrow miss).
    out = v.compute_longhorizon_verdict(
        primary=_null(
            "5m",
            val_acc_l2=0.515, val_acc_majority=0.500, val_acc_persistence=0.500,
            holdout_acc_l2=0.515, holdout_acc_majority=0.500, holdout_acc_persistence=0.500,
        ),
        secondaries=[_null("30m"), _null("1h")],
    )
    assert out["verdict"] == v.VERDICT_INVESTIGATE
    assert (
        "accuracy_threshold_narrowly_missed_no_reversal"
        in out["ambiguous_conditions_matched"]
    )


def test_derive_horizon_reports_uplifts_and_predicates() -> None:
    d = v.derive_horizon(_ev("5m"))
    assert d.acc_uplift_vs_majority_pp == pytest.approx(5.0)
    assert d.acc_uplift_vs_persistence_pp == pytest.approx(4.0)
    assert d.beats_both_floors_acc_2pp is True
    assert d.macro_f1_meets_0p03 is True
    assert d.balanced_accuracy_meets_1pp is True
    assert d.val_month_all_beat_both is True
    assert d.conf_tail_beats_majority is True
    assert d.holdout_full_reversal is False
    assert d.continue_all_requirements_met is True


def test_primary_horizon_must_be_5m() -> None:
    with pytest.raises(v.LongHorizonVerdictError):
        v.compute_longhorizon_verdict(primary=_ev("30m"), secondaries=[])
