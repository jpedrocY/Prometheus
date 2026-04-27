# Phase 2v — R2 Gate 2 Review

**Phase:** 2v — R2 Gate 1 execution plan, pre-commit Gate 2 review.
**Review date:** 2026-04-27 UTC.
**Working directory:** `C:\Prometheus`.
**Reviewers:** Operator + ChatGPT (joint review of Phase 2u spec memo and Phase 2v Gate 1 execution plan).

**Authority:** Phase 2u R2 spec memo §A–§P (committed singularly per §F); Phase 2v R2 Gate 1 execution plan §§1–6; Phase 2f §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2i §1.7 binding test and §1.7.3 project-level locks; Phase 2t R2 Gate 1 planning memo (GO recommendation conditional on §11.3 discipline locks).

**Outcome:** Gate 2 found **one blocking correction** in the R2 candidate-lifecycle definition. The correction is structural (a missing cancellation reason in the pending-state machine), not parametric — no committed sub-parameter values are changed. The correction is applied as an in-place amendment to both Phase 2u (spec memo) and Phase 2v (execution plan); the resulting amended documents are the authoritative R2 specification and execution plan for any future operator-approved Phase 2w execution phase.

**Scope:** Docs-only review and amendment. **No code, no runs, no parameter tuning, no candidate-set widening, no Phase 4 / paper-shadow / live-readiness work, no MCP / Graphify / `.mcp.json`, no credentials, no spec sub-parameter changes.** This Gate 2 review does **not** authorize the Phase 2w execution phase; it amends the Phase 2u/2v artifacts so that, when the operator does authorize execution, the R2 candidate-lifecycle is unambiguous and complete.

---

## 1. Finding summary

| # | Finding                                                                                                                                                                                                       | Severity      | Affected sections                                                                                                       |
|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|--------------------------------------------------------------------------------------------------------------------------|
| 1 | The R2 candidate-lifecycle is missing a STRUCTURAL_INVALIDATION cancellation reason. A pending candidate whose structural-stop reference has been breached on a non-touch bar would erroneously continue pending. | **BLOCKING**   | Phase 2u §B / §E.2 / §E.6 / §J.4 / §L / §P.1; Phase 2v §3.1.2 / §3.1.5 / §3.1.6 / §3.1.7 / §3.2.3 / §4.1 / §6.1.        |
| 2 | The §P.6 / Phase 2v run #10 limit-at-pullback intrabar fill model needs explicit "diagnostic-only, never a production path" framing to prevent future drift toward exposing it as a tunable knob.                  | CLARIFICATION | Phase 2u §F.4; Phase 2v §1.5 (run #10 row note) / §4.6 / §6.2.                                                          |

Finding #1 blocks execution authorization. Finding #2 is a clarification that strengthens existing language; it does not block but is bundled with finding #1's amendment for atomicity.

---

## 2. The blocker (finding #1)

### 2.1 What's missing

Per Phase 2u §E.2 (pre-amendment), the per-bar evaluation predicate for a pending LONG candidate at bar `t ∈ (B, B + 8]` was:

```
Cancel_bias_t        := (Bias_t != LONG)
Cancel_opposite_t    := OppSignal_t (with direction = SHORT)
Touched_t            := (low_t <= candidate.pullback_level)
Confirmed_t          := (close_t > candidate.structural_stop_level)
```

Order of evaluation (first-match wins):

1. If `Cancel_bias_t` → CANCEL(BIAS_FLIP).
2. Else if `Cancel_opposite_t` → CANCEL(OPPOSITE_SIGNAL).
3. Else if `Touched_t AND Confirmed_t` → READY_TO_FILL.
4. Else continue.

The `Confirmed_t = (close_t > structural_stop_level)` predicate was checked **only as part of the touch-and-confirmation joint check at step 3**. On a bar with no touch (`low_t > pullback_level`), `Confirmed_t` was not evaluated, and the candidate continued pending regardless of whether the close had violated the structural-stop reference.

### 2.2 Why this is a defect

Consider a bar t with: `low_t > candidate.pullback_level` (no touch) AND `close_t ≤ candidate.structural_stop_level` (close has breached the structural stop on the breakout-side, with no retest having occurred).

Under the pre-amendment rule, none of the three cancellation predicates fires (bias OK, no opposite signal, no touch); the candidate continues pending. But the breakout has been structurally invalidated — the close is on the *wrong side* of the stop reference, meaning if the trade had already entered, it would already be in stop territory.

The pending candidate carries a structural promise: "if I get filled, I will enter at a price *above* the structural stop on the breakout-side." A bar with `close_t ≤ structural_stop_level` violates that promise prospectively — there is no longer any plausible pullback-and-confirmation that recovers the breakout structure. Letting the candidate persist creates a dead-pool of stale candidates that can never legitimately fill (they would either expire at B+8 or, in pathological cases, fill at a price the stop-distance filter would reject).

### 2.3 What the operator-mandated fix specifies

A new cancellation reason **STRUCTURAL_INVALIDATION** fires whenever the close has breached the structural-stop reference, **regardless of whether the touch occurred**:

- **LONG:** STRUCTURAL_INVALIDATION fires at bar t if `close_t ≤ candidate.structural_stop_level`.
- **SHORT:** STRUCTURAL_INVALIDATION fires at bar t if `close_t ≥ candidate.structural_stop_level`.

It is inserted into the cancellation precedence at position 3, between OPPOSITE_SIGNAL (position 2) and TOUCH+CONFIRMATION (now position 4):

```
1. BIAS_FLIP
2. OPPOSITE_SIGNAL
3. STRUCTURAL_INVALIDATION   ← NEW
4. TOUCH + CONFIRMATION
5. CONTINUE
```

This precedence ordering means:

- A bar with close ≤ stop AND no touch: STRUCTURAL_INVALIDATION cancels the candidate (the previously-uncovered case).
- A bar with close ≤ stop AND touch (touch + close-violating-stop on the same bar): STRUCTURAL_INVALIDATION wins at step 3; step 4's TOUCH + CONFIRMATION is never reached. The candidate is correctly cancelled instead of erroneously continuing as "touch without confirmation".
- A bar with close > stop AND touch: STRUCTURAL_INVALIDATION does not fire at step 3; TOUCH + CONFIRMATION fires at step 4 → READY_TO_FILL. Behavior unchanged from pre-amendment.
- A bar with close > stop AND no touch: STRUCTURAL_INVALIDATION does not fire; TOUCH + CONFIRMATION does not fire (no touch); step 5 CONTINUE. Behavior unchanged from pre-amendment.

### 2.4 Subtle implication for the confirmation predicate at step 4

After the amendment, the confirmation predicate `Confirmed_t = (close_t > structural_stop_level)` at step 4 is **mechanically redundant**: any bar that reaches step 4 has already been verified to have `close_t > structural_stop_level` by virtue of step 3 not firing. The predicate is retained at step 4 for **symmetry and readability** — the rule's defining shape is "touch + close-not-violating-stop", and stating both conjuncts at step 4 documents the rule completely. It costs nothing to evaluate twice; the implementation may keep both checks or short-circuit at step 4 (relying on step 3's precedence) at the implementer's discretion. The committed semantics is unchanged either way.

### 2.5 What the fix is NOT

The fix is **not** a change to any Phase 2u §F committed sub-parameter:

- Pullback level: still `setup.setup_high` (LONG) / `setup.setup_low` (SHORT).
- Confirmation rule: still "close not violating structural stop" (the rule's defining predicate is unchanged; STRUCTURAL_INVALIDATION makes the same check apply on every bar, not only on touch bars).
- Validity window: still N = 8 bars.
- Fill model: still next-bar-open after confirmation.

The fix is a **completeness correction** to the pending-state machine: the same close-vs-structural-stop predicate that defined "confirmation" at the touch bar now also defines an explicit cancellation on every pending bar, eliminating the gap between "touch with violation" (previously misclassified as "continue pending") and "non-touch with violation" (previously misclassified as "continue pending").

### 2.6 What §10.3 thresholds, §1.7 binding test, and falsifiable hypothesis remain

All preserved unchanged:

- Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds: applied unchanged.
- Phase 2i §1.7 binding test: R2 still passes (rule-shape change; rule-input domain change; trade-lifecycle topology change verbatim per §1.7.1). The amendment adds one cancellation predicate inside the new state machine; it does not change R2's structural classification.
- Phase 2u §O candidate-specific falsifiable hypothesis: unchanged. The §10.3 paths, §11.4 ETH-as-comparison, and M1/M2/M3 mechanism predictions are not affected by the cancellation precedence completion.
- Phase 2u §F sub-parameter commitments: all four axes unchanged.

---

## 3. The clarification (finding #2)

### 3.1 Limit-at-pullback intrabar is diagnostic-only

Phase 2v run #10 and Phase 2u §P.6 introduce a **limit-at-pullback intrabar** fill model as a fill-model sensitivity diagnostic against the §F.4-committed next-bar-open-after-confirmation model. The pre-amendment language was clear that this is a sensitivity cut, but did not explicitly forbid it from later being exposed as a production / default config path.

### 3.2 The fix

The amendment makes explicit:

- The committed R2 fill model is **next-bar-open after confirmation** (§F.4). This is the only fill model that produces R2 trade records eligible for §10.3 evaluation.
- The **limit-at-pullback intrabar** fill model is a **diagnostic-only sensitivity measurement**. It is run once per execution wave (Phase 2v run #10) for §P.6 reporting purposes and never as a production path.
- The implementation must **not** expose the fill model as a configurable knob on `V1BreakoutConfig` (e.g., as an `EntryFillModel` enum field). The committed fill model is hard-coded for `EntryKind.PULLBACK_RETEST`. The diagnostic-only sensitivity run is implemented via a **runner-script `--fill-model` argument**, not via a config field, so the production code path always uses the committed model.
- A future operator-approved phase that wants to test alternative fill models must introduce a new candidate (e.g., R2-limit) with its own non-fitting rationale, full §F-style commitment, and full §1.7 binding-test re-evaluation. It cannot be added as a config tweak under R2.

### 3.3 Why this matters

The Phase 2u §F.4 non-fitting rationale anchors the fill model to "H0's existing market-on-next-bar-open convention" — the most-conservative realism choice. If a future phase silently adds the limit-at-pullback intrabar model as a `V1BreakoutConfig` field, the discipline boundary between "committed value" and "configurable knob" weakens. The amendment closes that boundary explicitly: the diagnostic exists only as a runner-script flag, never as a config field.

---

## 4. Affected sections in Phase 2u (`2026-04-27_phase-2u_R2_spec-memo.md`)

The amendment touches the following sections in the Phase 2u spec memo. All edits are surgical — no committed sub-parameter values change.

| Section | Edit                                                                                                                                                                                                                                                       |
|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Top-of-file Status block | Add Gate 2 amendment notice with reference to this review file.                                                                                                                                                                                      |
| §B (Exact rule shape, R2 pseudocode) | Add STRUCTURAL_INVALIDATION cancellation check between OPPOSITE_SIGNAL and TOUCH+CONFIRMATION in the per-bar loop.                                                                                                                                |
| §E.2 (Per-bar evaluation predicate, LONG) | Add `Cancel_structural_t := (close_t <= candidate.structural_stop_level)` predicate definition. Update order-of-evaluation list to insert STRUCTURAL_INVALIDATION at position 3; renumber TOUCH+CONFIRMATION to position 4 and CONTINUE to position 5. |
| §E.6 (Boundary cases) | Replace the "Touch-without-confirmation" bullet with two clarified bullets covering the new STRUCTURAL_INVALIDATION precedence behavior. Add a new bullet documenting same-bar STRUCTURAL_INVALIDATION + touch precedence (STRUCTURAL_INVALIDATION wins). |
| §F.4 (Fill model commitment) | Add explicit "diagnostic-only, never a production path" framing for the §P.6 limit-at-pullback intrabar fill model.                                                                                                                                      |
| §J.4 (Diagnostics funnel) | Add `expired_candidates_structural_invalidation` bucket between `expired_candidates_opposite_signal` and `expired_candidates_stop_distance_at_fill`.                                                                                                  |
| §J.5 (Tests, descriptive) | Reflect the new STRUCTURAL_INVALIDATION cancellation in the test-coverage description.                                                                                                                                                                  |
| §L.2 (Pullback exceeds stop) | Update language to distinguish in-pending STRUCTURAL_INVALIDATION (close-violates-stop on any bar) from at-fill STOP_DISTANCE_AT_FILL (fill-time band rejection); the failure-mode taxonomy is now finer.                                              |
| §P.1 (Fill rate) | Add `expired_candidates_structural_invalidation` row in the cancellation decomposition. Update the accounting identity restated here.                                                                                                                       |

The amended Phase 2u memo is the authoritative spec. The pre-amendment version remains in git history; the amendment notice at the top of the file links to this Gate 2 review for context.

---

## 5. Affected sections in Phase 2v (`2026-04-27_phase-2v_R2_gate-1-execution-plan.md`)

The amendment touches the following sections in the Phase 2v Gate 1 execution plan. All edits propagate the Phase 2u amendment into the execution-mechanics layer.

| Section | Edit                                                                                                                                                                                                                                       |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Top-of-file Status block | Add Gate 2 amendment notice with reference to this review file.                                                                                                                                                                       |
| §1.5 (Run inventory, run #10 row) | Add note that limit-at-pullback intrabar is **diagnostic-only**; not a production / default config path.                                                                                                                          |
| §3.1.2 (entry_lifecycle.py) | Update `evaluate_pending_candidate` return-set to include `CANCEL_STRUCTURAL_INVALIDATION`. Update precedence list to: bias-flip → opposite-signal → structural-invalidation → touch+confirmation.                                |
| §3.1.5 (Diagnostics funnel) | Add `expired_candidates_structural_invalidation` bucket to the funnel-bucket list.                                                                                                                                                  |
| §3.1.6 (Per-trade record schema) | Add `STRUCTURAL_INVALIDATION` to the `cancellation_reason` enumerated values.                                                                                                                                                  |
| §3.1.7 (Tests) | Replace existing `test_R2_long_touch_without_confirm_continues_pending` (now mechanically incorrect under the amended precedence) with `test_R2_long_close_violates_stop_triggers_structural_invalidation`. Add three new tests: `test_R2_structural_invalidation_long`, `test_R2_structural_invalidation_short`, `test_R2_structural_invalidation_precedence_after_opposite_signal`, `test_R2_structural_invalidation_precedence_before_touch_confirmation`. Update `test_R2_cancellation_precedence` to cover the full 4-step ordering. |
| §3.2.3 (Implementation-bug check) | Update accounting identity to include the new bucket: `registered_candidates = expired_candidates_no_pullback + expired_candidates_bias_flip + expired_candidates_opposite_signal + expired_candidates_structural_invalidation + expired_candidates_stop_distance_at_fill + trades_filled_R2`. |
| §4.1 (P.1 — Fill rate) | Update the cancellation-decomposition table description to add the STRUCTURAL_INVALIDATION row. Table is now 6 rows (5 cancellation reasons + filled) × 2 columns (BTC, ETH).                                                              |
| §4.6 (P.6 — Fill-model sensitivity) | Strengthen the "diagnostic-only" language: explicit statement that limit-at-pullback intrabar must remain a runner-script `--fill-model` flag, never a `V1BreakoutConfig` field.                                                       |
| §6.1 (Implementation risks) | Add a new risk row: "STRUCTURAL_INVALIDATION precedence not enforced correctly in the per-bar evaluator." Mitigation: explicit precedence tests including same-bar cases.                                                                |
| §6.2 (Fill-model sensitivity risk) | Strengthen the diagnostic-only framing.                                                                                                                                                                                          |

The amended Phase 2v plan is the authoritative execution plan. The pre-amendment version remains in git history.

---

## 6. Test-list amendment summary

The Phase 2v §3.1.7 test list changes as follows:

**Removed (mechanically incorrect under amended precedence):**

- `test_R2_long_touch_without_confirm_continues_pending` — under the amended precedence, a bar with `low_t ≤ pullback_level AND close_t ≤ structural_stop_level` triggers STRUCTURAL_INVALIDATION at step 3 (CANCEL), not "continue pending" at step 5. The pre-amendment test asserts incorrect behavior and is replaced.

**Added:**

- `test_R2_long_close_violates_stop_triggers_structural_invalidation` (replaces the removed test) — bar with `low_t ≤ pullback_level AND close_t ≤ structural_stop_level` (LONG) → CANCEL(STRUCTURAL_INVALIDATION).
- `test_R2_structural_invalidation_long` — non-touch bar with `low_t > pullback_level AND close_t ≤ structural_stop_level` (LONG) → CANCEL(STRUCTURAL_INVALIDATION).
- `test_R2_structural_invalidation_short` — non-touch bar with `high_t < pullback_level AND close_t ≥ structural_stop_level` (SHORT) → CANCEL(STRUCTURAL_INVALIDATION).
- `test_R2_structural_invalidation_precedence_after_opposite_signal` — bar where opposite-signal AND structural-violation both fire → CANCEL(OPPOSITE_SIGNAL) wins (precedence position 2 < 3).
- `test_R2_structural_invalidation_precedence_before_touch_confirmation` — touch bar where `low_t ≤ pullback_level AND close_t ≤ structural_stop_level` → CANCEL(STRUCTURAL_INVALIDATION) wins (precedence position 3 < 4); touch+confirmation is never reached.

**Updated:**

- `test_R2_cancellation_precedence` — generalized from "bias-flip wins over touch+confirmation" to cover the full 4-step ordering (bias-flip > opposite-signal > structural-invalidation > touch+confirmation).
- `test_R2_long_confirm_without_touch_continues_pending` — semantically unchanged (a bar with `low_t > pullback_level AND close_t > structural_stop_level` still continues pending at step 5), but the test docstring should reference the amended precedence so future readers understand the bar passed step 3 (no structural invalidation) before reaching step 5.

**Net change to estimated test count.** Phase 2v §3.1.7 estimated 30–50 new R2 tests pre-amendment. Post-amendment: 33–53 (one removed; four added; one renamed; one updated). The "expected pytest count" range in §3.2.1 updates from ~461–481 to ~464–484.

---

## 7. What is NOT changed

The Gate 2 amendment is surgical. The following are **explicitly preserved unchanged**:

- **Phase 2u §F sub-parameter commitments.** All four axes (pullback level, confirmation rule, validity window, fill model) committed at the Phase 2u §F values. No alternative tested. No sweep authorized.
  - Pullback level: `setup.setup_high` (LONG) / `setup.setup_low` (SHORT).
  - Confirmation: close not violating structural stop (LONG: `close_t > structural_stop_level`; SHORT: `close_t < structural_stop_level`).
  - Validity window: N = 8 completed 15m bars.
  - Committed fill model: next-bar-open after confirmation.
- **Phase 2u §F non-fitting anchors.** All four anchors documented in §F unchanged. All four axes still anchor to existing project conventions.
- **Phase 2u §O falsifiable hypothesis.** §10.3 paths, §11.4 ETH-as-comparison, §11.6 cost-sensitivity, M1/M2/M3 mechanism-validation predictions all unchanged.
- **Phase 2u §M Phase 2i §1.7 binding-test evaluation.** R2 still structural per §1.7.1's verbatim trade-lifecycle topology example. The amendment adds one cancellation predicate inside the same state machine; it does not change R2's structural classification.
- **Phase 2v §1 execution scope.** Datasets (locked v002), symbols (BTC primary / ETH secondary per §1.7.3), time windows (R = 2022-01-01 → 2025-01-01; V = 2025-01-01 → 2026-04-01), cost model (MED/MARK default; LOW/HIGH and TRADE_PRICE sensitivities) all unchanged.
- **Phase 2v §1.5 run inventory.** Still 10 runs; same variant × window × slippage × stop-trigger combinations; run #10 (limit-at-pullback intrabar) still present but with strengthened diagnostic-only framing.
- **Phase 2v §2 control variants.** H0 / R3 / R2+R3 control configurations unchanged. Expected control reproduction numbers (Phase 2e baseline; Phase 2l locked; Phase 2s V-window locked) unchanged.
- **Phase 2v §5 gate criteria.** §10.3 disqualification floor; §10.3.a / §10.3.c paths; §10.3.b mechanically unavailable; §11.4 ETH-as-comparison; §11.6 cost-sensitivity; §11.3 V-window — all unchanged. Combined verdict classification table unchanged.
- **Phase 2v §6 risk checklist.** Existing risks unchanged; one new risk row added (STRUCTURAL_INVALIDATION precedence enforcement) per §5 above.
- **Phase 2i §1.7.3 project-level locks.** BTCUSDT primary; ETHUSDT research/comparison only; one-position max; one-symbol-only; 0.25% risk; 2× leverage; mark-price stops; v002 datasets — all unchanged.
- **GAP dispositions.** GAP-20260424-030 / 031 / 032 / 033 / 036 and GAP-20260419-015 all carried unchanged. No new GAP entries introduced by the amendment.
- **Phase 2j §C.6 R1a sub-parameters.** Frozen.
- **Phase 2j §D.6 R3 sub-parameters.** Frozen (R3 is the locked exit baseline for R2).
- **Phase 2r §F R1b-narrow sub-parameter.** Frozen.

---

## 8. Verification

The amendment is verified to be correct by:

1. **Cancellation precedence completeness.** The five-step precedence (BIAS_FLIP → OPPOSITE_SIGNAL → STRUCTURAL_INVALIDATION → TOUCH+CONFIRMATION → CONTINUE) covers every combination of `(touched, confirmed, bias_flip, opposite_signal)` deterministically. No bar can fall through all five steps without producing one of {CANCEL, READY_TO_FILL, CONTINUE}.
2. **Confirmation predicate consistency.** Step 4's `Confirmed_t = (close_t > structural_stop_level)` predicate at the touch bar is identical to step 3's `NOT Cancel_structural_t = (close_t > structural_stop_level)` negation. The amendment does not introduce a new structural reference; it applies the same close-vs-stop check on every bar instead of only at the touch bar.
3. **No double-cancellation.** First-match-wins precedence guarantees at most one cancellation per bar. A bar with bias_flip AND structural_violation produces CANCEL(BIAS_FLIP) only; the candidate is consumed at step 1 and step 3 is never reached.
4. **No silent fills.** A bar with structural_violation can no longer reach step 4 (touch+confirmation) → no fill is recorded on a bar with close-violating-stop. Pre-amendment, this case was impossible only because confirmation was bundled with touch; post-amendment, the same protection is explicit and applies to non-touch bars too.
5. **Sub-parameter immutability.** The amendment introduces one new cancellation predicate within the existing state machine; no §F committed value is changed.
6. **Backward compatibility for H0.** Default `entry_kind = MARKET_NEXT_BAR_OPEN` does not register PendingCandidates and does not run the per-bar evaluator; H0 / R3 / R1a / R1b-narrow baseline reproduction is unaffected by the amendment. The Phase 2v §3.2.2 control reproduction tests still apply unchanged.

---

## 9. Approval recommendation

**Subject to operator approval**, the Gate 2 amendments to Phase 2u and Phase 2v are applied. The amended documents are the authoritative R2 specification and execution plan. Phase 2v Gate 1 execution authorization is now contingent on:

- Operator review and approval of this Gate 2 review document.
- Operator review and approval of the amended Phase 2u and Phase 2v files.
- Separate operator authorization to begin a Phase 2w execution phase implementing the amended spec.

This Gate 2 review does **not** by itself authorize execution. The next operator decision is whether to:

- (a) Approve the amendments and authorize Phase 2w execution.
- (b) Request further amendments.
- (c) Defer Phase 2w authorization (consolidation at R3 stays as Phase 2p Option A; R2 spec is preserved as ready-to-execute when authorized).

---

## 10. Threshold preservation, wave/phase preservation, safety posture

**Threshold preservation.** Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved. Phase 2j §D.6 R3 sub-parameters preserved. Phase 2r §F R1b-narrow sub-parameter preserved. Phase 2u §F R2 sub-parameters preserved singularly. GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged. No new GAP entries introduced. Phase 2i §1.7.3 project-level locks preserved.

**Wave / phase preservation.** Phase 2g Wave-1 REJECT ALL preserved as historical evidence only. Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen; baseline-of-record per Phase 2p). Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D). Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged. Phase 2t R2 Gate 1 planning memo preserved. Phase 2u R2 spec memo amended in place per §4 above. Phase 2v R2 Gate 1 execution plan amended in place per §5 above. H0 anchor preserved as the sole §10.3 / §10.4 anchor.

**Safety posture.** Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No edits to source files, test files, scripts, datasets, or manifests **in Phase 2v Gate 2 review**. No `data/` writes. No Phase 4 work. No paper/shadow planning. No live-readiness claim. No code in this Gate 2 review. No backtests. No parameter tuning. No spec sub-parameter changes. No new ideas introduced beyond the operator-mandated correction. No candidate-set widening (only R2 + H0 + R3 controls remain on the run inventory). The amended Phase 2u spec memo and Phase 2v execution plan are the docs-only outputs of this review.

---

**End of Phase 2v Gate 2 review.** One blocking finding (STRUCTURAL_INVALIDATION cancellation completeness) and one clarification (limit-at-pullback diagnostic-only) identified, scoped, applied as in-place amendments to Phase 2u and Phase 2v, and verified for correctness without changing any committed sub-parameter, falsifiable-hypothesis threshold, or §1.7.3 project-level lock. Awaiting operator approval of the amended documents and explicit authorization for any future Phase 2w execution phase. **Stop after producing this review and the amended docs.**
