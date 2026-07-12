"""Phase 4bn-AR — long-horizon fixed-baseline pre-registered verdict logic.

Pure, offline, deterministic verdict module for the Phase 4bn-AR fixed
long-horizon baseline run. It encodes — as frozen code, before any result is
seen — the Phase 4bn-AP §24/§25 decision hierarchy applied to the ``5m`` primary
target, with ``30m`` / ``1h`` as secondary diagnostics that can only route a
non-clean primary to ``INVESTIGATE_AMBIGUOUS`` (never upgrade a failed primary to
continuation). It records exactly one of:

- ``CONTINUE_ONE_BOUNDED_FOLLOWUP`` — every strict Phase 4bn-AP 5m requirement
  holds (frozen Phase 4bn-AE §16 thresholds, verbatim);
- ``INVESTIGATE_AMBIGUOUS`` — CONTINUE does not hold, there is no hard-negative
  holdout reversal, and at least one explicit Phase 4bn-AP ambiguous condition
  applies (authorises no further run — at most a later docs-only decision memo);
- ``STOP_LONGHORIZON_ML_ARC`` — neither CONTINUE nor an explicit ambiguous
  condition applies (a hard holdout reversal, or a clean absence of any frozen
  positive information diagnostic).

The thresholds are the frozen Phase 4bn-AE §16 constants
(``SUCCESS_ACCURACY_UPLIFT_PP = 2.0`` over **both** floors,
``SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = 1.0`` over the majority floor,
``SUCCESS_MACRO_F1_UPLIFT = 0.03`` over the majority floor) plus the block
(> 50 % of validation date blocks; **every** validation month block) and
holdout-non-reversal rules. They are **not** relaxed after any result is seen.
The narrow-miss interpretation band (:data:`NARROW_MISS_FLOOR_PP`) is a fixed,
pre-registered constant that only ever routes between ``INVESTIGATE_AMBIGUOUS``
and ``STOP_LONGHORIZON_ML_ARC``; it can never fabricate a ``CONTINUE`` outcome.

No I/O. No network. Imports only the standard library and the frozen Phase
4bn-AE contract constants.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import pre_v002_ml_dataset_contract as ae

# ---------------------------------------------------------------------------
# Verdict identifiers (Phase 4bn-AP §25)
# ---------------------------------------------------------------------------

VERDICT_CONTINUE = "CONTINUE_ONE_BOUNDED_FOLLOWUP"
VERDICT_INVESTIGATE = "INVESTIGATE_AMBIGUOUS"
VERDICT_STOP = "STOP_LONGHORIZON_ML_ARC"

# Frozen Phase 4bn-AE §16 thresholds (verbatim; never relaxed after a result).
SUCCESS_ACCURACY_UPLIFT_PP = ae.SUCCESS_ACCURACY_UPLIFT_PP            # 2.0
SUCCESS_BALANCED_ACCURACY_UPLIFT_PP = ae.SUCCESS_BALANCED_ACCURACY_UPLIFT_PP  # 1.0
SUCCESS_MACRO_F1_UPLIFT = ae.SUCCESS_MACRO_F1_UPLIFT                 # 0.03
HIGH_CONFIDENCE_THRESHOLD = ae.HIGH_CONFIDENCE_THRESHOLD            # 0.8

# Calibration expected-calibration-error band for a "usable" verdict (fixed,
# pre-registered; diagnostic only — never a trading gate).
CALIBRATION_USABLE_ECE = 0.05

# Narrow-miss interpretation band (pre-registered, fixed before the run). A
# primary accuracy uplift over BOTH floors of at least this many pp but below the
# frozen +2.0 pp bar is a "narrowly missed threshold" (Phase 4bn-AP §25 ambiguous
# condition) — it can only route STOP -> INVESTIGATE, never produce CONTINUE.
NARROW_MISS_FLOOR_PP = 1.0

CALIBRATION_USABLE = "usable"
CALIBRATION_RANKING_ONLY = "ranking_only"
CALIBRATION_UNUSABLE = "unusable"


class LongHorizonVerdictError(RuntimeError):
    """Raised when verdict inputs are malformed."""


# ---------------------------------------------------------------------------
# Calibration classification (diagnostic only)
# ---------------------------------------------------------------------------


def classify_calibration(
    *, tail_n: int, tail_acc: float, majority_acc: float, ece: float
) -> str:
    """Return the diagnostic calibration verdict for one (horizon, split).

    ``usable`` — the >= 0.8 confidence tail exists, beats the majority floor,
    and the reliability error is small; ``ranking_only`` — the tail beats the
    majority floor but is materially miscalibrated (overconfident); ``unusable``
    — no >= 0.8 tail, or it does not beat the majority floor. This is a
    descriptive diagnostic (Phase 4bn-AE §17); it is never a trading signal.
    """
    if tail_n <= 0 or tail_acc <= majority_acc:
        return CALIBRATION_UNUSABLE
    if ece <= CALIBRATION_USABLE_ECE:
        return CALIBRATION_USABLE
    return CALIBRATION_RANKING_ONLY


# ---------------------------------------------------------------------------
# Per-horizon evidence (scalar; the exact quantities the frozen rules consume)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HorizonEvidence:
    """Frozen, scalar evidence for one target horizon (validation + holdout)."""

    horizon: str
    # Validation aggregate accuracy for the three baselines.
    val_acc_l2: float
    val_acc_majority: float
    val_acc_persistence: float
    # Validation balanced accuracy / macro-F1 (L2 vs majority floor).
    val_balacc_l2: float
    val_balacc_majority: float
    val_macro_f1_l2: float
    val_macro_f1_majority: float
    # Holdout aggregate accuracy (for the no-reversal assessment).
    holdout_acc_l2: float
    holdout_acc_majority: float
    holdout_acc_persistence: float
    # Validation block evidence (L2 beats BOTH floors).
    val_date_block_count: int
    val_date_blocks_beat_both: int
    val_month_block_count: int
    val_month_blocks_beat_both: int
    # Validation >= 0.8 confidence tail (L2) vs majority floor + calibration.
    conf_tail_n: int
    conf_tail_acc: float
    conf_tail_majority_acc: float
    calibration_verdict: str


@dataclass(frozen=True)
class HorizonDerived:
    """Deterministic derived predicates / uplifts for one horizon."""

    horizon: str
    acc_uplift_vs_majority_pp: float
    acc_uplift_vs_persistence_pp: float
    beats_majority_2pp: bool
    beats_persistence_2pp: bool
    beats_both_floors_acc_2pp: bool
    macro_f1_uplift: float
    macro_f1_meets_0p03: bool
    balanced_accuracy_uplift_pp: float
    balanced_accuracy_meets_1pp: bool
    val_date_frac_beats_both: float
    val_date_majority_beats_both: bool
    val_month_all_beat_both: bool
    conf_tail_exists: bool
    conf_tail_beats_majority: bool
    calibration_usable: bool
    holdout_acc_uplift_vs_majority_pp: float
    holdout_acc_uplift_vs_persistence_pp: float
    holdout_full_reversal: bool
    classification_improves: bool
    some_frozen_positive: bool
    narrow_acc_miss: bool
    continue_all_requirements_met: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "horizon": self.horizon,
            "acc_uplift_vs_majority_pp": self.acc_uplift_vs_majority_pp,
            "acc_uplift_vs_persistence_pp": self.acc_uplift_vs_persistence_pp,
            "beats_majority_2pp": self.beats_majority_2pp,
            "beats_persistence_2pp": self.beats_persistence_2pp,
            "beats_both_floors_acc_2pp": self.beats_both_floors_acc_2pp,
            "macro_f1_uplift": self.macro_f1_uplift,
            "macro_f1_meets_0p03": self.macro_f1_meets_0p03,
            "balanced_accuracy_uplift_pp": self.balanced_accuracy_uplift_pp,
            "balanced_accuracy_meets_1pp": self.balanced_accuracy_meets_1pp,
            "val_date_frac_beats_both": self.val_date_frac_beats_both,
            "val_date_majority_beats_both": self.val_date_majority_beats_both,
            "val_month_all_beat_both": self.val_month_all_beat_both,
            "conf_tail_exists": self.conf_tail_exists,
            "conf_tail_beats_majority": self.conf_tail_beats_majority,
            "calibration_usable": self.calibration_usable,
            "holdout_acc_uplift_vs_majority_pp": self.holdout_acc_uplift_vs_majority_pp,
            "holdout_acc_uplift_vs_persistence_pp": (
                self.holdout_acc_uplift_vs_persistence_pp
            ),
            "holdout_full_reversal": self.holdout_full_reversal,
            "classification_improves": self.classification_improves,
            "some_frozen_positive": self.some_frozen_positive,
            "narrow_acc_miss": self.narrow_acc_miss,
            "continue_all_requirements_met": self.continue_all_requirements_met,
        }


def derive_horizon(ev: HorizonEvidence) -> HorizonDerived:
    """Compute the deterministic derived predicates for one horizon."""
    acc_up_maj = (ev.val_acc_l2 - ev.val_acc_majority) * 100.0
    acc_up_per = (ev.val_acc_l2 - ev.val_acc_persistence) * 100.0
    beats_maj = acc_up_maj >= SUCCESS_ACCURACY_UPLIFT_PP
    beats_per = acc_up_per >= SUCCESS_ACCURACY_UPLIFT_PP
    beats_both = beats_maj and beats_per

    mf1_up = ev.val_macro_f1_l2 - ev.val_macro_f1_majority
    mf1_pass = mf1_up >= SUCCESS_MACRO_F1_UPLIFT
    bal_up = (ev.val_balacc_l2 - ev.val_balacc_majority) * 100.0
    bal_pass = bal_up >= SUCCESS_BALANCED_ACCURACY_UPLIFT_PP

    date_frac = (
        ev.val_date_blocks_beat_both / ev.val_date_block_count
        if ev.val_date_block_count > 0
        else 0.0
    )
    date_majority = ev.val_date_block_count > 0 and date_frac > 0.5
    month_all = (
        ev.val_month_block_count > 0
        and ev.val_month_blocks_beat_both == ev.val_month_block_count
    )

    tail_exists = ev.conf_tail_n > 0
    tail_beats = tail_exists and ev.conf_tail_acc > ev.conf_tail_majority_acc
    calib_usable = ev.calibration_verdict == CALIBRATION_USABLE

    hold_up_maj = (ev.holdout_acc_l2 - ev.holdout_acc_majority) * 100.0
    hold_up_per = (ev.holdout_acc_l2 - ev.holdout_acc_persistence) * 100.0
    reversal_maj = acc_up_maj > 0.0 and hold_up_maj < 0.0
    reversal_per = acc_up_per > 0.0 and hold_up_per < 0.0
    holdout_reversal = reversal_maj or reversal_per

    classification_improves = beats_both and mf1_pass
    some_positive = (
        beats_maj or beats_per or mf1_pass or bal_pass or date_majority or tail_beats
    )
    # Narrow miss of the +2.0 pp both-floor accuracy bar (both floors within the
    # [NARROW_MISS_FLOOR_PP, 2.0) pp band), only meaningful when the bar is missed.
    narrow_acc_miss = (not beats_both) and (
        min(acc_up_maj, acc_up_per) >= NARROW_MISS_FLOOR_PP
    )

    continue_all = (
        beats_both
        and mf1_pass
        and bal_pass
        and date_majority
        and month_all
        and tail_beats
        and not holdout_reversal
    )

    return HorizonDerived(
        horizon=ev.horizon,
        acc_uplift_vs_majority_pp=acc_up_maj,
        acc_uplift_vs_persistence_pp=acc_up_per,
        beats_majority_2pp=beats_maj,
        beats_persistence_2pp=beats_per,
        beats_both_floors_acc_2pp=beats_both,
        macro_f1_uplift=mf1_up,
        macro_f1_meets_0p03=mf1_pass,
        balanced_accuracy_uplift_pp=bal_up,
        balanced_accuracy_meets_1pp=bal_pass,
        val_date_frac_beats_both=date_frac,
        val_date_majority_beats_both=date_majority,
        val_month_all_beat_both=month_all,
        conf_tail_exists=tail_exists,
        conf_tail_beats_majority=tail_beats,
        calibration_usable=calib_usable,
        holdout_acc_uplift_vs_majority_pp=hold_up_maj,
        holdout_acc_uplift_vs_persistence_pp=hold_up_per,
        holdout_full_reversal=holdout_reversal,
        classification_improves=classification_improves,
        some_frozen_positive=some_positive,
        narrow_acc_miss=narrow_acc_miss,
        continue_all_requirements_met=continue_all,
    )


def _secondary_positive(d: HorizonDerived) -> bool:
    """A secondary horizon shows positive frozen diagnostic evidence.

    Defined as: beats BOTH floors on validation accuracy by the frozen +2.0 pp
    margin AND a macro-F1 uplift >= 0.03, with NO hard-negative holdout reversal.
    A secondary positive can only route a non-clean primary to
    ``INVESTIGATE_AMBIGUOUS``; it can never upgrade a failed primary to
    ``CONTINUE`` (Phase 4bn-AP §24).
    """
    return (
        d.beats_both_floors_acc_2pp
        and d.macro_f1_meets_0p03
        and not d.holdout_full_reversal
    )


def compute_longhorizon_verdict(
    *,
    primary: HorizonEvidence,
    secondaries: list[HorizonEvidence],
) -> dict[str, object]:
    """Return the frozen Phase 4bn-AP §24/§25 verdict (no softening).

    Precedence: (1) evaluate CONTINUE first; (2) a hard-negative holdout reversal
    of the primary uplift forces STOP; (3) otherwise evaluate the explicit
    Phase 4bn-AP ambiguous conditions — any match -> INVESTIGATE; (4) else STOP.
    30m/1h are secondary diagnostics only and cannot upgrade a failed 5m to
    CONTINUE.
    """
    if primary.horizon != "5m":
        raise LongHorizonVerdictError(
            f"primary horizon must be '5m', got {primary.horizon!r}"
        )
    pd = derive_horizon(primary)
    sds = [derive_horizon(s) for s in secondaries]
    secondary_positive_flags = {s.horizon: _secondary_positive(s) for s in sds}
    any_secondary_positive = any(secondary_positive_flags.values())

    ambiguous_conditions: list[str] = []
    stop_reasons: list[str] = []

    if pd.continue_all_requirements_met:
        verdict = VERDICT_CONTINUE
    elif pd.holdout_full_reversal:
        verdict = VERDICT_STOP
        stop_reasons.append(
            "internal holdout reverses the sign of the 5m validation uplift against "
            f"at least one required floor (holdout_acc_uplift_vs_majority_pp="
            f"{pd.holdout_acc_uplift_vs_majority_pp:.4f}, vs_persistence_pp="
            f"{pd.holdout_acc_uplift_vs_persistence_pp:.4f})"
        )
    else:
        # No CONTINUE and no hard-negative reversal: evaluate ambiguity.
        if pd.val_date_majority_beats_both != pd.val_month_all_beat_both:
            ambiguous_conditions.append("mixed_date_and_month_block_evidence")
        if pd.classification_improves and not pd.conf_tail_beats_majority:
            ambiguous_conditions.append(
                "classification_improves_but_calibration_fails"
            )
        if pd.classification_improves and not pd.continue_all_requirements_met:
            ambiguous_conditions.append(
                "validation_improves_holdout_or_criteria_inconclusive_no_reversal"
            )
        if any_secondary_positive:
            ambiguous_conditions.append(
                "primary_5m_not_clean_but_secondary_30m_or_1h_positive"
            )
        if pd.narrow_acc_miss:
            ambiguous_conditions.append("accuracy_threshold_narrowly_missed_no_reversal")
        if pd.some_frozen_positive:
            ambiguous_conditions.append("information_suggested_but_not_clean")

        if ambiguous_conditions:
            verdict = VERDICT_INVESTIGATE
        else:
            verdict = VERDICT_STOP
            stop_reasons.append(
                "5m shows no frozen positive information diagnostic (no floor beaten "
                "by >= 2.0 pp, no macro-F1 >= 0.03, no balanced-accuracy >= 1.0 pp, no "
                "date-block majority, no >= 0.8 confidence tail beating the majority "
                "floor) and no secondary 30m/1h positive evidence"
            )

    return {
        "verdict": verdict,
        "primary_horizon": primary.horizon,
        "ambiguous_conditions_matched": ambiguous_conditions,
        "stop_reasons": stop_reasons,
        "secondary_positive_flags": secondary_positive_flags,
        "primary_derived": pd.as_dict(),
        "secondary_derived": {s.horizon: s.as_dict() for s in sds},
        "thresholds": {
            "success_accuracy_uplift_pp": SUCCESS_ACCURACY_UPLIFT_PP,
            "success_balanced_accuracy_uplift_pp": SUCCESS_BALANCED_ACCURACY_UPLIFT_PP,
            "success_macro_f1_uplift": SUCCESS_MACRO_F1_UPLIFT,
            "high_confidence_threshold": HIGH_CONFIDENCE_THRESHOLD,
            "calibration_usable_ece": CALIBRATION_USABLE_ECE,
            "narrow_miss_floor_pp": NARROW_MISS_FLOOR_PP,
            "date_block_rule": "L2_beats_BOTH_floors_in_more_than_half_of_validation_dates",
            "month_block_rule": "L2_beats_BOTH_floors_in_EVERY_validation_month",
        },
    }


__all__ = [
    "CALIBRATION_RANKING_ONLY",
    "CALIBRATION_UNUSABLE",
    "CALIBRATION_USABLE",
    "CALIBRATION_USABLE_ECE",
    "HIGH_CONFIDENCE_THRESHOLD",
    "HorizonDerived",
    "HorizonEvidence",
    "LongHorizonVerdictError",
    "NARROW_MISS_FLOOR_PP",
    "SUCCESS_ACCURACY_UPLIFT_PP",
    "SUCCESS_BALANCED_ACCURACY_UPLIFT_PP",
    "SUCCESS_MACRO_F1_UPLIFT",
    "VERDICT_CONTINUE",
    "VERDICT_INVESTIGATE",
    "VERDICT_STOP",
    "classify_calibration",
    "compute_longhorizon_verdict",
    "derive_horizon",
]
