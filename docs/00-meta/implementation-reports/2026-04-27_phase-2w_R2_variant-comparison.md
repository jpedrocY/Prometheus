# Phase 2w — R2 (Pullback-Retest Entry) Variant Comparison Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL preserved as historical evidence only); Phase 2h decision memo; Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary); Phase 2j memo §C / §D; Phase 2k Gate 1 plan; Phase 2l comparison report (R3 PROMOTE locked; baseline-of-record per Phase 2p); Phase 2m comparison report (R1a+R3 promoted-but-non-leading per Phase 2p §D); Phase 2n / 2o / 2p consolidation; Phase 2r R1b-narrow spec memo; Phase 2s R1b-narrow execution comparison report (PROMOTE / PASS-with-caveats; bias-strength judged not the missing mechanism); Phase 2t R2 Gate 1 planning memo (GO recommendation); Phase 2u R2 spec memo (Gate 2 amended); Phase 2v R2 Gate 1 execution plan (Gate 2 amended); Phase 2v Gate 2 review; Phase 2w scope-escalation memo (operator-approved Option (a) staging); Phase 2w-A checkpoint report (implementation + tests + control reproduction green); Phase 2w-B checkpoint report (R2 execution + diagnostics; framework FAILED via §11.6).

**Phase:** 2w — R2 implementation, execution, and final variant-comparison.
**Branch:** `phase-2w/r2-execution`.
**Run dates:** 2026-04-27 UTC.

**Status:** **§10.3 framework verdict: FAILED** under Phase 2v §5.1.7 / §5.4 failure condition 9 — §11.6 cost-sensitivity gate triggers §10.3 disqualification on both BTCUSDT and ETHUSDT at HIGH slippage despite the candidate cleanly clearing §10.3 at MEDIUM (committed) slippage. **Mechanism reading: PARTIALLY SUPPORTED** — M1 (per-trade expectancy improvement on intersection trades) and M3 (R-distance reduction) PASS on BTC; M2 (stop-exit-fraction reduction) FAILS on both symbols. **R2 becomes retained research evidence; R3 remains the baseline-of-record per Phase 2p §C.1.** No live-readiness, paper/shadow, or Phase 4 claim. No code merge to main. No next phase started.

---

## 1. Plain-English summary

Phase 2u defined R2 (pullback-retest entry) as a single-axis structural redesign of H0's entry-lifecycle topology, replacing immediate market-on-next-bar-open fills with a conditional-pending lifecycle: signal at bar B → register PendingCandidate → wait up to 8 bars for price to retest the setup boundary → fill at next-bar open after a confirmation that the close has not violated the structural-stop level → otherwise expire or cancel. The Phase 2v Gate 2 review added a STRUCTURAL_INVALIDATION cancellation reason at precedence position 3 (after BIAS_FLIP and OPPOSITE_SIGNAL, before TOUCH+CONFIRMATION) to close a logic gap on non-touch bars where the close had already breached the structural stop. The four sub-parameters were committed singularly per Phase 2u §F: pullback level = `setup.setup_high` / `setup.setup_low`; confirmation rule = close not violating structural stop; validity window = 8 bars; committed fill model = next-bar-open after confirmation.

R2's hypothesis (Phase 2u §A): on BTC, a non-trivial fraction of H0/R3 stop-outs reflect entering at the breakout-bar's far side from the structural-stop level, where ordinary post-breakout volatility produces a stop-out before directional follow-through develops. Pullback-retest entry should reduce stop-distance, increase position size at fixed equity-risk, tighten the +2R take-profit's absolute price distance, and *should* reduce the stop-exit fraction.

The Phase 2w execution ran R2+R3 on the locked Phase 2e v002 datasets across 6 runs (governing R-window MED slippage MARK_PRICE; LOW slippage; HIGH slippage; TRADE_PRICE stop-trigger; diagnostic-only limit-at-pullback intrabar; V-window confirmation). The H0 and R3 controls reproduced their locked baselines bit-for-bit on all 48 metric cells (re-used from 2w-A; engine kwarg default preserves the committed path).

The findings:

- **R-window MED-slip §10.3 verdict: PROMOTE.** BTC clears §10.3.a + §10.3.c (Δexp +0.184, ΔPF +0.274, |maxDD| ratio 0.45×); ETH clears §10.3.c only (Δexp +0.043 < §10.3.a's +0.10 magnitude threshold). §11.4 ETH-as-comparison satisfied. §10.3 disqualification floor not triggered.
- **§11.6 cost-sensitivity gate: FAILS.** At HIGH slippage (8 bps), R2+R3's BTC Δexp drops to −0.014 (worse than H0) and ETH Δexp drops to −0.230 (severe disqualification). Per Phase 2v §5.4 failure condition 9, this is a hard framework block.
- **Combined framework verdict: FAILED — §11.6 cost-sensitivity blocks.** R2's edge does not survive the cost-realism band Phase 2f §11.6 requires.
- **Mechanism reading: PARTIALLY SUPPORTED.** M1 (BTC intersection-trade Δexp = +0.123 R per trade) ≥ +0.10 R threshold → PASS. M3 (R2 mean stop-distance < R3 mean stop-distance on matched signals) → PASS. M2 (BTC stop-exit fraction R2 0.261 > R3 0.242) → FAIL. M2 also fails on ETH (R2 0.526 > R3 0.424). The smaller-stop / larger-position-size geometry produces a real per-trade-expectancy improvement, but does not reduce the proportion of trades that get stopped out.
- **V-window:** R-window PROMOTE'd at MED, so V was run. BTC R2 V degrades severely (n=5, expR −0.901; sample-size-fragile); ETH R2 V is near-parity with R3 V (n=12, expR −0.108 vs R3 V −0.093). V-window does not change the framework verdict.
- **Implementation correctness: VERIFIED.** All P.14 hard-block checks pass on both symbols (zero TRAILING_BREACH/STAGNATION; protective stop frozen; accounting identity; time_to_fill in range; raw r_distance in band; M3 mechanical reduction). No engine bugs identified.

The Phase 2w outcome: R2 is the third structural-redesign candidate tested (after R1a setup-shape and R1b-narrow bias-shape) that produces a mechanism-partially-supported MED-slip §10.3 PROMOTE while failing some other framework gate. Phase 2t §11.6 anticipated this exact failure-mode shape (entry #2 in the failure list explicitly noted R2's smaller-stop geometry interacts with slippage differently than market-fill geometry; Phase 2u §O recorded §11.6 clearance at HIGH as part of the falsifiable hypothesis).

---

## 2. What was implemented

### 2.1 Source code surface (Phase 2w-A + 2w-B)

| File | Phase | Net source lines | Purpose |
|------|:-----:|----------------:|---------|
| `src/prometheus/strategy/v1_breakout/variant_config.py` | 2w-A | +50 | `EntryKind` enum + `entry_kind` field. Default `MARKET_NEXT_BAR_OPEN` preserves H0 / R3 / R1a / R1b-narrow bit-for-bit. |
| `src/prometheus/strategy/v1_breakout/entry_lifecycle.py` (NEW) | 2w-A | 297 | `PendingCandidate` (frozen; carries the original BreakoutSignal); `CancellationReason` and `PendingEvaluation` enums; `R2_VALIDITY_WINDOW_BARS = 8`; `evaluate_pending_candidate` (5-step precedence per Phase 2v Gate 2 amended §E.2); `evaluate_fill_at_next_bar_open` (fill-time stop-distance band). |
| `src/prometheus/strategy/v1_breakout/strategy.py` | 2w-A | +51 | `StrategySession._pending_candidate` field + `pending_candidate` / `has_pending_candidate` / `register_pending_candidate` / `clear_pending_candidate` lifecycle hooks. |
| `src/prometheus/strategy/v1_breakout/__init__.py` | 2w-A | +19 / −8 | Re-export `EntryKind`, `PendingCandidate`, `CancellationReason`, `PendingEvaluation`, `FillEvaluation`, `R2_VALIDITY_WINDOW_BARS`, `evaluate_pending_candidate`, `evaluate_fill_at_next_bar_open`. |
| `src/prometheus/research/backtest/engine.py` | 2w-A + 2w-B | +476 / −35 | `_R2TradeMetadata`, `R2LifecycleCounters`, `BacktestRunResult.r2_counters_per_symbol`, `_handle_r2_entry_lifecycle`, `_fill_r2_pending_candidate` with runner-script-only `r2_fill_model` kwarg dispatch, R2 dispatch in `_run_symbol`, R2 metadata population in `_record_trade`. |
| `src/prometheus/research/backtest/trade_log.py` | 2w-A | +37 | 9 R2-specific TradeRecord fields with H0-equivalent defaults; parquet schema extended. |
| `src/prometheus/research/backtest/diagnostics.py` | 2w-A | +42 | 5 new R2 cancellation buckets on `SignalFunnelCounts` + `r2_accounting_identity_holds` property. |
| `tests/unit/research/backtest/test_trade_log.py` | 2w-A | +11 | Schema-checking test extended for the 9 new R2 columns. |
| `tests/unit/strategy/v1_breakout/test_entry_lifecycle.py` (NEW) | 2w-A | 764 | 43 R2 unit tests covering every category in Phase 2v §3.1.7 (Gate 2 amended). |
| `scripts/phase2w_R2_execution.py` (NEW) | 2w-B | 543 | Phase 2w runner. VARIANTS = {H0, R3, R2+R3}. Knobs: `--variant`, `--window`, `--slippage`, `--stop-trigger`, `--fill-model`. Emits `r2_lifecycle_total.json` sidecar per symbol. Validates that `--fill-model limit-at-pullback` only runs on `--variant R2+R3`. |
| `scripts/_phase2w_R2_analysis.py` (NEW) | 2w-B + 2w-C | 970 | P.1–P.14 + M1/M2/M3 + §10.3 + §11.6 gate computation. Final 2w-C version includes the P.9 per-regime expR computation (1h-volatility tercile classifier, trailing 1000-bar window per Phase 2l/2m/2s convention). |

**Total source/test/script surface:** ~2,700 lines (Phase 2u §J.6 estimated 1,430–2,130 source/test for 2w-A; the actual implementation came in at the upper bound when the runner + analysis scripts are included). The implementation cost was the deferral reason from Phase 2i §3.2; the Phase 2t §11.1 GO recommendation accepted this cost.

### 2.2 What R2 does (operationally)

When `entry_kind=PULLBACK_RETEST` and a successful H0 trigger + bias + signal-time stop-distance pre-filter pass at bar B:

1. **Register PendingCandidate** at bar B's close. Frozen fields: pullback_level (= `setup.setup_high` for LONG / `setup.setup_low` for SHORT), structural_stop_level (= `compute_initial_stop()` output), atr_at_signal (= `entry.signal.atr_20_15m`), validity_expires_at_index (= B + 8), original BreakoutSignal.
2. **Per-bar evaluation** for each completed 15m bar t in (B, B+8] applies the 5-step precedence (first-match wins):
   - Step 1: BIAS_FLIP if `bias_at_t != candidate.direction`.
   - Step 2: OPPOSITE_SIGNAL if a new opposite-direction trigger fires at bar t close.
   - Step 3: STRUCTURAL_INVALIDATION (Phase 2v Gate 2 amendment) if `close_t ≤ structural_stop_level` (LONG) / `close_t ≥ structural_stop_level` (SHORT) — fires regardless of touch state.
   - Step 4: TOUCH + CONFIRMATION: `low_t ≤ pullback_level AND close_t > structural_stop_level` (LONG; mirrored SHORT) → READY_TO_FILL.
   - Step 5: CONTINUE.
3. **Fill** on READY_TO_FILL at bar t+1 open with the committed next-bar-open-after-confirmation fill model. Fill-time stop-distance filter re-applies the same `[0.60, 1.80] × atr_at_signal` band that H0 applies at signal time. On filter rejection: STOP_DISTANCE_AT_FILL.
4. **Expiry** at bar B+9 if no earlier outcome fired: VALIDITY_WINDOW_ELAPSED.
5. **R3 exit machinery** counts time-stop bars from the FILL bar (R3-consistent interpretation per Phase 2u §G).

The diagnostic-only `limit-at-pullback intrabar` fill model (Phase 2v §P.6 / run #10) lives behind a runner-script-only `--fill-model` flag, never as a `V1BreakoutConfig` field. The committed next-bar-open path is the only path eligible for §10.3 governing evaluation.

---

## 3. Tests and quality gates

### 3.1 Test surface

**474 pytest tests pass.** Up from Phase 2s baseline of 431 by exactly 43 new R2 tests in `tests/unit/strategy/v1_breakout/test_entry_lifecycle.py`. Coverage matrix per Phase 2v §3.1.7 (Gate 2 amended):

| Category | Test count | Notes |
|----------|-----------:|-------|
| H0 baseline preservation under default `entry_kind` | 4 | Includes `test_default_entry_kind_is_market_next_bar_open` and explicit R3-config no-pending invariants. |
| `PendingCandidate` state methods | 3 | Validity boundary at B+1..B+8; expiry strictly past B+8. |
| StrategySession pending hooks | 3 | Register / clear / double-registration rejection / register-during-trade rejection. |
| TOUCH + CONFIRMATION (LONG + SHORT mirrored) | 7 | Touch+confirm → READY_TO_FILL; no-touch / confirm-without-touch → CONTINUE; touch+close-violates-stop → STRUCTURAL_INVALIDATION. |
| Cancellation precedence (5-step ordering) | 8 | BIAS_FLIP; NEUTRAL bias; OPPOSITE_SIGNAL; STRUCTURAL_INVALIDATION (LONG / SHORT no-touch via `model_construct`); precedence after OPPOSITE_SIGNAL; precedence before TOUCH+CONFIRMATION; full 4-precedence-true case. |
| Boundary cases | 3 | Close == structural_stop → invalidation (`<=` admits equality); just above stop → READY_TO_FILL; low == pullback → touch (`<=` admits equality). |
| Fill-time stop-distance | 4 | Within band → fill; below floor → STOP_DISTANCE_AT_FILL; above ceiling → STOP_DISTANCE_AT_FILL; ATR=0 defense-in-depth. |
| Frozen protective-stop invariant | 3 | structural_stop_level / pullback_level / atr_at_signal frozen on the dataclass. |
| Engine-side accounting identity | 4 | Default counters all-zero; identity holds after each terminal outcome; identity breaks when unattributed; SignalFunnelCounts default identity holds. |
| Validity-window expiry | 2 | B+8 within validity; B+9 expired. |
| Pending uniqueness | 2 | Re-register after clear admits; register-during-trade rejected. |

Two STRUCTURAL_INVALIDATION tests verify predicate behavior on inputs that are impossible in valid OHLC (the close-violates-stop without touch case, which would require `close < low` — impossible) using `NormalizedKline.model_construct` to bypass OHLC validation. These document that the 5-step precedence correctly handles the impossible-but-test-isolated case.

### 3.2 Quality-gate results (final, after Phase 2w-C P.9 addition)

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **474 passed in 11.58s** (0 regressions vs 2w-A) |
| Linter | `uv run ruff check .` | **All checks passed** |
| Formatter | `uv run ruff format --check .` | **128 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 50 source files** |

All four gates green throughout 2w-A, 2w-B, and 2w-C. No code regressions.

---

## 4. H0/R3 control reproduction

**All 48 metric cells (6 metrics × 2 symbols × 4 runs) match locked Phase 2e/2l/2s baselines bit-for-bit.** Per Phase 2v §3.2.2 the bit-for-bit reproduction is a hard-block discipline; reproduction passed. The new `EntryKind` dispatch under default `MARKET_NEXT_BAR_OPEN` does not regress baseline behavior.

### 4.1 R-window controls (2022-01-01 → 2025-01-01, MED slippage, MARK_PRICE)

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | Locked baseline | Match? |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|-----------------|:------:|
| H0 | BTCUSDT | 33 | 30.30% | −0.4590 | 0.2552 | −3.392% | −3.675% | Phase 2e (33 / 30.30% / −0.459 / 0.255 / −3.39% / −3.67%) | ✓ |
| H0 | ETHUSDT | 33 | 21.21% | −0.4752 | 0.3207 | −3.527% | −4.134% | Phase 2e | ✓ |
| R3 | BTCUSDT | 33 | 42.42% | −0.2403 | 0.5602 | −1.774% | −2.159% | Phase 2l | ✓ |
| R3 | ETHUSDT | 33 | 33.33% | −0.3511 | 0.4736 | −2.605% | −3.647% | Phase 2l | ✓ |

### 4.2 V-window controls (2025-01-01 → 2026-04-01, MED slippage, MARK_PRICE)

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | Locked baseline | Match? |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|-----------------|:------:|
| H0 | BTCUSDT | 8 | 25.00% | −0.3132 | 0.5410 | −0.557% | −0.874% | Phase 2s | ✓ |
| H0 | ETHUSDT | 14 | 28.57% | −0.1735 | 0.6950 | −0.546% | −0.803% | Phase 2s | ✓ |
| R3 | BTCUSDT | 8 | 25.00% | −0.2873 | 0.5799 | −0.510% | −1.061% | Phase 2s | ✓ |
| R3 | ETHUSDT | 14 | 42.86% | −0.0932 | 0.8242 | −0.293% | −0.940% | Phase 2s | ✓ |

---

## 5. R-window headline comparison

R-window 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE:

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD | L/S | Stops | TPs | Time-stops |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|----:|------:|----:|----------:|
| H0 | BTCUSDT | 33 | 30.30% | −0.459 | 0.255 | −3.39% | −3.67% | 16/17 | 17 | 0 | 0 |
| H0 | ETHUSDT | 33 | 21.21% | −0.475 | 0.321 | −3.53% | −4.13% | 13/20 | 26 | 0 | 0 |
| R3 | BTCUSDT | 33 | 42.42% | −0.240 | 0.560 | −1.77% | −2.16% | 16/17 | 8 | 4 | 21 |
| R3 | ETHUSDT | 33 | 33.33% | −0.351 | 0.474 | −2.61% | −3.65% | 13/20 | 14 | 5 | 14 |
| **R2+R3** | **BTCUSDT** | **23** | **30.43%** | **−0.275** | **0.529** | **−1.42%** | **−1.65%** | **10/13** | **6** | **3** | **14** |
| **R2+R3** | **ETHUSDT** | **19** | **26.32%** | **−0.432** | **0.454** | **−1.85%** | **−2.48%** | **9/10** | **10** | **3** | **6** |

R2 reduces trade count by 30.3% on BTC and 42.4% on ETH versus H0/R3. The surviving trades on BTC have meaningfully better per-trade metrics than H0 (expR +0.184, PF +0.274, maxDD −2.0 pp); on ETH the R2 improvement vs H0 is smaller (expR +0.043, PF +0.133, maxDD −1.7 pp).

---

## 6. Official §10.3 verdict vs H0

### 6.1 §10.3 deltas vs H0 anchor (committed run #3, MED slippage, MARK_PRICE)

| Symbol | Δexp vs H0 | ΔPF vs H0 | Δn% | Δ\|maxDD\|pp | \|maxDD\| ratio |
|--------|-----------:|----------:|----:|------------:|----------------:|
| BTCUSDT | **+0.1836** | **+0.2737** | −30.30% | **−2.028** | **0.448×** |
| ETHUSDT | +0.0434 | +0.1333 | −42.42% | −1.657 | 0.599× |

### 6.2 §10.3 disqualification floor — NOT TRIGGERED

| Veto | BTC | ETH |
|------|-----|-----|
| expR worsens | NO (+0.184) | NO (+0.043) |
| PF worsens | NO (+0.274) | NO (+0.133) |
| \|maxDD\| > 1.5× | NO (0.448× — well below floor) | NO (0.599× — well below floor) |

### 6.3 §10.3 promotion paths

§10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05):

| Symbol | Δexp | ΔPF | §10.3.a result |
|--------|-----:|----:|----------------|
| BTC | +0.184 | +0.274 | **CLEARED** |
| ETH | +0.043 | +0.133 | NOT cleared (Δexp < +0.10) |

§10.3.b (Δn ≥ +50%): **NOT applicable** (Δn < 0; R2 reduces trade count by design).

§10.3.c strict-dominance (Δexp > 0 AND ΔPF > 0 AND Δ|maxDD| ≤ 0):

| Symbol | Δexp | ΔPF | Δ\|maxDD\|pp | §10.3.c result |
|--------|-----:|----:|------------:|----------------|
| BTC | +0.184 | +0.274 | −2.028 | **CLEARED** |
| ETH | +0.043 | +0.133 | −1.657 | **CLEARED** |

### 6.4 §10.4 hard reject — NOT applicable

§10.4 fires only when Δn > 0. R2 has Δn negative on both symbols.

### 6.5 §11.4 ETH-as-comparison — SATISFIED

§11.4 requires BTC must clear and ETH must not catastrophically fail. BTC clears §10.3.a + §10.3.c. ETH clears §10.3.c without triggering any §10.3 disqualification floor. §11.4 satisfied.

### 6.6 R-window MED-slip §10.3 verdict

**MED-slip §10.3: PROMOTE.** R2+R3 clears the framework's MED-slippage band on both symbols.

This is preserved as **descriptive evidence** that R2 *can* clear the framework at the default-cost regime. The combined verdict (§8 below) factors in the §11.6 cost-sensitivity gate which fails at HIGH slippage.

---

## 7. §11.6 cost-sensitivity gate outcome

Per Phase 2v §5.1.7 / §5.4 failure condition 9: R2+R3 must clear §10.3 (no disqualification floor) at HIGH slippage on BOTH symbols. Run #8 governs this.

### 7.1 §11.6 deltas vs H0 at HIGH slippage (run #8)

| Symbol | Δexp vs H0 at HIGH | ΔPF vs H0 | Δ\|maxDD\|pp | \|maxDD\| ratio | Disqualified? |
|--------|-------------------:|----------:|-------------:|----------------:|:-:|
| BTC | **−0.0136** | +0.060 | −1.067 | 0.708× | **YES** (Δexp < 0) |
| ETH | **−0.2295** | −0.065 | −0.633 | 0.847× | **YES** (Δexp < 0; ΔPF < 0) |

### 7.2 §11.6 cross-slippage table

| Symbol | Slippage | expR | Δexp vs H0 | ΔPF vs H0 | maxDD | §10.3 verdict at this tier |
|--------|----------|-----:|----------:|---------:|------:|---------------------------|
| BTC | LOW | −0.180 | +0.279 | +0.413 | −1.18% | PROMOTE |
| BTC | **MEDIUM (committed)** | **−0.275** | **+0.184** | **+0.274** | **−1.65%** | **PROMOTE** |
| BTC | HIGH | −0.473 | **−0.014** | +0.060 | −2.60% | **DISQUALIFIED** |
| ETH | LOW | −0.481 | **−0.006** | +0.045 | −2.30% | **DISQUALIFIED** |
| ETH | **MEDIUM (committed)** | **−0.432** | **+0.043** | **+0.133** | **−2.48%** | **PROMOTE** |
| ETH | HIGH | −0.705 | **−0.230** | −0.065 | −3.50% | **DISQUALIFIED** |

### 7.3 §11.6 verdict

**§11.6: FAILS on both symbols at HIGH slippage.** Per Phase 2v §5.4 failure condition 9, this triggers the framework block. (The ETH LOW disqualification — Δexp −0.006 — is reported here for transparency; even cheaper-than-default cost slips ETH below H0. §11.6 evaluates HIGH specifically per Phase 2v §5.1.7, but the LOW result reinforces the slippage-fragility finding.)

---

## 8. Final combined framework verdict

```
MED-slip §10.3:        PROMOTE (BTC §10.3.a + §10.3.c; ETH §10.3.c)
§11.6 HIGH-slip gate:  FAILS (both BTC and ETH disqualified at HIGH)

COMBINED FRAMEWORK VERDICT: FAILED — §11.6 cost-sensitivity blocks
```

The MED-slip §10.3 PROMOTE is preserved as descriptive evidence that R2+R3 can clear the framework at the default-cost regime. The §11.6 gate failure means the candidate cannot be promoted under unchanged Phase 2f §11.3.5 thresholds.

**This is a documented and anticipated failure mode.** Phase 2t §11.6 explicitly listed §11.6 sensitivity as a risk for R2 (entry #2 in the failure-mode list noted that R2's smaller stop-distance interacts with slippage differently than market-fill geometry). Phase 2u §O recorded §11.6 clearance at HIGH as part of the falsifiable hypothesis. The §11.6 failure was therefore predictable from the spec design; the actual data confirms the prediction.

---

## 9. Supplemental R3-anchor interpretation (descriptive only)

H0 remains the sole governing anchor per Phase 2i §1.7.3. The R3-anchor view is supplemental.

| Symbol | Δexp_R3 | ΔPF_R3 | Δ\|maxDD\|pp_R3 | Δn% (vs R3) |
|--------|--------:|-------:|----------------:|------------:|
| BTCUSDT | **−0.0351** | **−0.0313** | −0.513 | −30.30% |
| ETHUSDT | **−0.0808** | **−0.0196** | +1.165 | −42.42% |

R2's marginal contribution on top of R3 is **negative on aggregate** on both symbols (BTC Δexp_R3 = −0.035; ETH Δexp_R3 = −0.081). On the same R-window, R3 alone produces 33 trades with expR −0.240 (BTC) / −0.351 (ETH); R2+R3 produces 23 BTC trades (expR −0.275) / 19 ETH trades (expR −0.432). The trade-count concentration helps the H0-anchor comparison (R2 selects out the worst trades) but does not improve per-trade expectancy on BTC vs R3 (it slightly worsens it).

This is structurally similar to Phase 2s R1b-narrow's pattern: framework PROMOTE under H0 anchor; near-neutral or negative R3-anchor delta. The §P.5 intersection-trade comparison (§11.5 below) clarifies that on the *same signals* both R2 and R3 trade, R2 produces materially better per-trade results — but R2 also trades fewer signals overall, and the trades it skips were not uniformly the bad ones.

---

## 10. M1/M2/M3 mechanism validation

Per Phase 2v §5.2 / Phase 2u §K mechanism predictions:

| Prediction | Definition | BTC | ETH | Verdict |
|------------|------------|:---:|:---:|---------|
| **M1** | Δexp_R3 ≥ +0.10 R on BTC (per-trade expectancy on intersection trades) | **PASS (+0.123)** | informative (+0.204) | **M1 PASS on BTC** |
| **M2** | BTC stop-exit fraction R2+R3 < R3 alone | FAIL (R2 0.261 > R3 0.242) | FAIL (R2 0.526 > R3 0.424) | **M2 FAIL on both** |
| **M3** | R2+R3 mean R-distance < R3 mean R-distance (mechanically guaranteed by pullback geometry) | **PASS** (BTC R2 mean stop_dist 169.5 < R3 mean 203.4) | **PASS** (ETH R2 mean 10.3 < R3 mean 13.0) | **M3 PASS on both** |

### 10.1 Mechanism reading

**M1 + M3 PASS; M2 FAILS.** The combined reading per Phase 2v §5.3 cross-tabulation:

```
§10.3 framework × M1/M2/M3 mechanism cross-tab (MED-slip):

  MED-slip §10.3 PROMOTE + M1 PASS + M2 FAIL + M3 PASS
  → "PROMOTE — MECHANISM PARTIALLY SUPPORTED"

  Combined (with §11.6 gate):
  → §11.6 FAILS at HIGH slippage
  → "FAILED — §11.6 cost-sensitivity blocks"
```

### 10.2 What "mechanism partially supported" means

R2 actually does what its thesis predicted on the per-trade level:

- **M1 +0.123 R per trade on BTC intersection** — the trades R2 fills (out of those R3 also fills) earn an additional +0.12 R per trade on average. R2 is *not* the R1b-narrow trade-count-reduction-driven pattern: there is genuine per-trade-expectancy improvement.
- **M3 R-distance reduction** — R2 mechanically enters at a smaller stop-distance (BTC mean stop_dist ratio 0.844; ETH 0.815). This is the geometry the spec predicted.

But:

- **M2 stop-exit fraction goes UP, not down.** Phase 2u §K predicted that pullback-retest entries would reduce stop-exit fraction (smaller stop distance + larger position size + closer take-profit ⇒ trades hit the +2R take-profit before the stop). The actual data shows the *opposite*: R2 trades are stopped at a slightly higher rate than R3's broader pool (BTC R2 0.261 vs R3 0.242; ETH R2 0.526 vs R3 0.424).

The interpretation: R2 selects against breakouts that don't pull back, and the surviving "retesting" breakouts are stopped at similar-to-higher rates than R3's full pool. R2's per-trade expectancy improvement comes from price geometry (better entries → larger positions at fixed risk → larger payoff per ATR of follow-through), not from selecting trades with lower stop-out rates.

This is informative — it tells us R2's edge is real but slippage-fragile, because the per-trade expectancy gain is approximately the same magnitude as the slippage-induced cost increase. At HIGH slippage (8 bps), the slippage cost ≈ 0.06 R per trade, which exceeds the BTC M1 improvement of +0.12 R when the directional signal is weak; ETH's smaller M1 improvement is consumed even at MED.

---

## 11. Full P.1–P.14 diagnostics

### 11.1 P.1 Fill rate + cancellation decomposition (run #3)

| Symbol | Registered | Filled | Fill rate | No-pullback | Bias-flip | Opp-signal | Struct-invalid | Stop-dist-at-fill | Identity holds |
|--------|-----------:|-------:|----------:|------------:|----------:|-----------:|---------------:|------------------:|:-:|
| BTCUSDT | 33 | 23 | 69.7% | 3 | 0 | 0 | 0 | 7 | ✓ |
| ETHUSDT | 33 | 19 | 57.6% | 4 | 0 | 0 | 0 | 10 | ✓ |

V-window R2+R3:

| Symbol | Registered | Filled | Fill rate | Stop-dist-at-fill | Identity |
|--------|-----------:|-------:|----------:|-----:|:-:|
| BTCUSDT | 8 | 5 | 62.5% | 3 | ✓ |
| ETHUSDT | 14 | 12 | 85.7% | 2 | ✓ |

**Observations.** BIAS_FLIP / OPPOSITE_SIGNAL / STRUCTURAL_INVALIDATION cancellation buckets are zero on both R-window symbols. The Gate-2-amended STRUCTURAL_INVALIDATION precedence existed but didn't fire on R-window data (every retest bar in the run had close > structural_stop on the breakout side, AND no non-touch bar produced close-violates-stop in valid OHLC). The amendment correctness is verified by unit tests; the runtime data simply doesn't exercise that path. STOP_DISTANCE_AT_FILL is the dominant cancellation reason (7 BTC + 10 ETH on R-window; 5 of 17 cancellations on V-window). Accounting identity holds on every run.

### 11.2 P.2 / P.11 Pullback-touch / time-to-fill distribution

| Symbol | Count | Mean | Median | Min | Max | Histogram (bars-after-registration) |
|--------|------:|-----:|-------:|----:|----:|-------------------------------------|
| BTCUSDT | 23 | 1.70 | 1 | 1 | 5 | {1: 16, 2: 3, 3: 1, 4: 1, 5: 2} |
| ETHUSDT | 19 | 1.32 | 1 | 1 | 5 | {1: 17, 3: 1, 5: 1} |

**Observations.** ~70% of BTC fills and ~89% of ETH fills happen at bar B+1 — the very first bar after the registration. The 8-bar validity window is non-binding for ≥95% of fills. The §F.3 anchor (8 bars) is well-chosen but not stress-tested by the data — a shorter window (e.g., 4 bars) would still capture nearly all fills.

### 11.3 P.3 Stop-distance reduction (R2 vs R3 on matched signals)

| Symbol | Matched | Mean ratio | Median | Min | Max | <1 | =1 | >1 |
|--------|--------:|-----------:|-------:|----:|----:|---:|---:|---:|
| BTCUSDT | 23 | 0.844 | 0.827 | 0.539 | 1.215 | 19 | 0 | 4 |
| ETHUSDT | 19 | 0.815 | 0.851 | 0.485 | 1.056 | 17 | 0 | 2 |

**Observations.** R2 entries produce smaller stop distances on average (mean ratio 0.81–0.84 → ~16–19% reduction). 19/23 BTC and 17/19 ETH trades have ratio < 1.0 (R2 fill closer to stop than R3 would have entered). The ~4 BTC + 2 ETH outliers > 1.0 reflect cases where the touch+confirmation bar's t+1 open is further from the stop than R3's entry would have been (rare but mechanically valid).

### 11.4 P.4 Stop-exit fraction comparison

| Symbol | H0 | R3 | R2+R3 | Δ(R2−R3) | M2 pass? |
|--------|---:|---:|------:|---------:|:--------:|
| BTCUSDT | 0.515 | 0.242 | 0.261 | +0.018 | **✗** |
| ETHUSDT | 0.788 | 0.424 | 0.526 | +0.102 | **✗** |

**Observations (already covered in §10).** M2 fails on both symbols. R2's pullback fills are stopped at a slightly higher fraction than R3's broader pool. This is the most strategically informative finding of Phase 2w: the R2 thesis (smaller stop + larger position ⇒ fewer stop-outs) is partially refuted on the directional side, and the per-trade-expectancy gain is purely from price-geometry, not selection.

### 11.5 P.5 Intersection-trade comparison vs R3 (M1 cut)

For trades that BOTH R3 and R2+R3 enter on the same signal:

| Symbol | Matched | Mean ΔR (R2 − R3) | LONG count | LONG mean ΔR | SHORT count | SHORT mean ΔR |
|--------|--------:|-------------------:|-----------:|-------------:|------------:|--------------:|
| BTCUSDT | 23 | **+0.1227** | 10 | +0.1162 | 13 | +0.1276 |
| ETHUSDT | 19 | **+0.2043** | 9 | −0.0249 | 10 | +0.4105 |

**Observations.**
- **M1 PASS on BTC** (+0.123 R per trade ≥ +0.10 threshold). Direction-symmetric on BTC (LONG +0.116 / SHORT +0.128 — both positive). The mechanism predicted by Phase 2u §K is operative on BTC's intersection.
- **ETH intersection improvement is +0.20 R per trade**, larger than BTC's, but split asymmetrically: LONG −0.025 (slight degradation), SHORT +0.41 (large improvement). Most of ETH's intersection improvement comes from short trades — consistent with Phase 2m R1a+R3 ETH-shorts edge being partially recoverable under R2's entry-mechanic alone.
- M1 is the strongest mechanism-validation cut and distinguishes R2 from the trade-count-reduction-driven R1b-narrow pattern.

### 11.6 P.6 Fill-model sensitivity (run #10 diagnostic-only)

| Symbol | Δ expR (limit-at-pullback − next-bar-open) | Δ PF | Δ trades | "Small divergence" (\|Δexp\| < 0.05)? |
|--------|-------------------------------------------:|-----:|---------:|:---:|
| BTCUSDT | **+0.2371** | (committed PF=0.529; diag PF=0.795) | small | **NO** |
| ETHUSDT | −0.0214 | small | small | **YES** |

**Observations.** BTC fill-model divergence is large (Δexp +0.24 R per trade between the diagnostic limit-at-pullback and the committed next-bar-open paths). The diagnostic-only path produces materially better BTC results than the committed path — but the diagnostic path is **not eligible for §10.3 governing evaluation** per Phase 2v Gate 2 clarification. The divergence is a backtest-vs-live realism flag for any future paper/shadow phase: BTC's R2 outcome is sensitive to the fill-model assumption, and the committed (most-conservative) path is what the framework verdict uses.

ETH fill-model divergence is small (Δexp −0.02 R, within the <0.05 threshold) — ETH's R2 outcome is fill-model-robust at the diagnostic level.

### 11.7 P.7 Long/short asymmetry

| Variant | Symbol | LONG count | SHORT count |
|---------|--------|-----------:|------------:|
| H0 | BTC | 16 | 17 |
| H0 | ETH | 13 | 20 |
| R3 | BTC | 16 | 17 |
| R3 | ETH | 13 | 20 |
| R2+R3 | BTC | 10 | 13 |
| R2+R3 | ETH | 9 | 10 |

R2+R3 cuts roughly proportionally across direction on both symbols. No direction-asymmetric admission introduced by R2's filter. R2 ETH SHORT count dropped from R3's 20 to 10 (50% reduction) — the larger drop reflects ETH's pullback-non-occurrence pattern.

### 11.8 P.8 Per-fold consistency (5 rolling folds, GAP-036)

#### BTC

| Fold | H0 n / expR | R3 n / expR | R2+R3 n / expR | ΔvH0 | ΔvR3 |
|------|-------------|-------------|----------------|-----:|-----:|
| F1 (2022H2) | 4 / −0.024 | 4 / −0.126 | 4 / +0.152 | +0.175 | +0.278 |
| F2 (2023H1) | 6 / −0.481 | 6 / −0.481 | 5 / −0.547 | −0.066 | −0.066 |
| F3 (2023H2) | 9 / −0.238 | 9 / +0.015 | 5 / −0.047 | +0.192 | −0.061 |
| F4 (2024H1) | 6 / −0.524 | 6 / +0.100 | 3 / +0.513 | +1.037 | +0.413 |
| F5 (2024H2) | 4 / −1.025 | 4 / −0.870 | 3 / −0.810 | +0.215 | +0.059 |

#### ETH

| Fold | H0 n / expR | R3 n / expR | R2+R3 n / expR | ΔvH0 | ΔvR3 |
|------|-------------|-------------|----------------|-----:|-----:|
| F1 (2022H2) | 4 / +0.390 | 4 / +0.220 | 2 / +1.339 | +0.948 | +1.118 |
| F2 (2023H1) | 8 / −0.257 | 8 / −0.025 | 4 / −0.255 | +0.003 | −0.229 |
| F3 (2023H2) | 7 / −0.750 | 7 / −0.458 | 3 / −0.219 | +0.532 | +0.239 |
| F4 (2024H1) | 8 / −0.810 | 8 / −0.816 | 6 / −0.691 | +0.119 | +0.125 |
| F5 (2024H2) | 2 / −0.836 | 2 / −0.836 | 2 / −1.016 | −0.179 | −0.179 |

**Fold wins (R2 vs anchor):** BTC vs H0 = 4/5; vs R3 = 3/5. ETH vs H0 = 4/5; vs R3 = 3/5. R2 beats H0 in 8/10 fold-symbol cells; beats R3 in 6/10. **Per-fold sample sizes are at the GAP-036 lower bound** (BTC F4: n=3; ETH F1: n=2; ETH F5: n=2) — single-trade flips can change fold expR sign, so the per-fold consistency reading is informative but operates near the discipline's sample-size floor. Aggregate framework verdict is governing per Phase 2s precedent.

### 11.9 P.9 Per-regime expR (1h-volatility terciles)

Convention: trailing 1000 1h-bar Wilder ATR(20), 33rd/67th percentile boundaries computed per-trade for live-equivalent classification.

#### BTC

| Variant | Regime | n | expR | PF | WR |
|---------|--------|--:|-----:|---:|---:|
| H0 | low_vol | 13 | −0.372 | 0.376 | 30.77% |
| H0 | med_vol | 7 | −0.195 | 0.571 | 57.14% |
| H0 | high_vol | 13 | −0.688 | 0.047 | 15.38% |
| R3 | low_vol | 13 | −0.054 | 0.890 | 38.46% |
| R3 | med_vol | 7 | −0.157 | 0.655 | 57.14% |
| R3 | high_vol | 13 | −0.472 | 0.278 | 38.46% |
| **R2+R3** | low_vol | 12 | **−0.295** | 0.481 | 33.33% |
| **R2+R3** | med_vol | 5 | −0.241 | 0.424 | 20.00% |
| **R2+R3** | high_vol | 6 | −0.265 | 0.648 | 33.33% |

#### ETH

| Variant | Regime | n | expR | PF | WR |
|---------|--------|--:|-----:|---:|---:|
| H0 | low_vol | 12 | −0.184 | 0.729 | 33.33% |
| H0 | med_vol | 7 | −1.040 | 0.000 | 0.00% |
| H0 | high_vol | 14 | −0.442 | 0.191 | 21.43% |
| R3 | low_vol | 12 | −0.177 | 0.747 | 41.67% |
| R3 | med_vol | 7 | −0.915 | 0.062 | 14.29% |
| R3 | high_vol | 14 | −0.219 | 0.550 | 35.71% |
| **R2+R3** | low_vol | 7 | **+0.091** | **1.115** | 42.86% |
| **R2+R3** | med_vol | 5 | −0.745 | 0.051 | 20.00% |
| **R2+R3** | high_vol | 7 | −0.731 | 0.074 | 14.29% |

**Observations.**
- **R2+R3 BTC is most uniform across regimes** — expR −0.30 / −0.24 / −0.27 across low/med/high. R2 reduces the high-vol degradation R3 had (R3 high-vol −0.47 → R2+R3 high-vol −0.27).
- **R2+R3 ETH low_vol is the strongest cell observed** — n=7 / expR +0.091 / PF 1.115 / WR 42.86%. **This is the project's first-ever ETH R-window low_vol cell with positive expR AND PF > 1 outside R1a+R3** (R1a+R3 had ETH low_vol +0.281 / PF 1.353 with n=11; R2+R3 confirms a similar low-vol ETH effect with smaller n and smaller magnitude). Phase 2m R1a+R3's ETH-low-vol edge appears partially recoverable under R2's entry-mechanic.
- **R2+R3 ETH med_vol and high_vol are degraded** vs R3 alone — R2 selects against pullback patterns that would have worked under R3's exit machinery in those regimes.
- Per-regime sample sizes (n=5 to n=14) are small; cell-level reads are sample-fragile.

### 11.10 P.10 R-distance distribution

| Symbol | n | R2 mean R-dist (ATR-norm) | Median | Min | Max (post-slip) | Max (de-slipped, raw) |
|--------|--:|--------------------------:|-------:|----:|----------------:|----------------------:|
| BTCUSDT | 23 | 1.371 | 1.342 | 0.843 | 1.852 | 1.769 |
| ETHUSDT | 19 | 1.322 | 1.321 | 0.880 | 1.649 | (within band) |

**Observations.** R2 trades' R-distances are concentrated in the upper half of the [0.60, 1.80] band on both symbols. Two BTC trades show post-slip R-distance > 1.80 (1.843 and 1.852); both have de-slipped raw R-distance within [0.60, 1.80] (1.642 and 1.769), confirming the engine's band check used the raw next-bar open per Phase 2u §E.3. The post-slip exceedance is a slippage-induced artifact of the recorded fill_price, not a band-enforcement bug. (See §11.13 implementation-bug check.)

### 11.11 P.12 MFE/MAE distribution at fill

| Symbol | Variant | n | MFE mean | MFE max | MAE mean | MAE min |
|--------|---------|--:|---------:|--------:|---------:|--------:|
| BTC | R2+R3 | 23 | **+1.102** | +3.234 | +0.594 | +0.079 |
| BTC | R3 | 33 | +0.792 | +3.083 | +0.635 | +0.168 |
| ETH | R2+R3 | 19 | **+1.128** | +4.742 | +0.637 | +0.091 |
| ETH | R3 | 33 | +1.061 | +3.462 | +0.519 | +0.076 |

**Observations.**
- **R2+R3 mean MFE is HIGHER than R3 alone on both symbols** (BTC +1.10 vs R3 +0.79; ETH +1.13 vs R3 +1.06). This is consistent with the M3 mechanical R-distance reduction: smaller R-distance means each ATR of price movement maps to a larger R-multiple, so R2 trades show larger MFE in R-multiple terms even when the underlying price excursion is similar.
- **R2 max MFE on ETH (+4.742) exceeds R3's max (+3.462)** — there are R2-only trades with very strong follow-through.
- **MAE mean R2+R3 BTC (+0.59) is comparable to R3 (+0.64)** — no signature of R2 trades having systematically worse adverse excursion.
- The MFE distributions confirm R2's geometry produces more upside-R-multiple-per-unit-of-price-movement, even when the per-trade outcome doesn't always materialize.

### 11.12 P.13 Mark-price vs trade-price stop-trigger sensitivity (GAP-032)

| Symbol | Δ expR (TRADE − MARK) | Δ PF | Δ trades | Gap-through (default) | Gap-through (TRADE_PRICE) |
|--------|----------------------:|-----:|---------:|----------------------:|--------------------------:|
| BTCUSDT | +0.0000 | +0.0000 | 0 | 0 | 0 |
| ETHUSDT | +0.0000 | +0.0000 | 0 | 0 | 0 |

**Bit-identical.** Zero gap-through stops on both symbols. Same as Phase 2l / 2m / 2s pattern: MARK_PRICE introduces no systematic bias relative to TRADE_PRICE on this data.

### 11.13 P.14 Implementation-bug checks

All hard-block checks pass on both symbols:

| Check | BTC | ETH |
|-------|:---:|:---:|
| Zero TRAILING_BREACH / STAGNATION exits on R2+R3 | ✓ | ✓ |
| Protective stop equals frozen `structural_stop_level` | ✓ | ✓ |
| R2 lifecycle accounting identity holds | ✓ | ✓ |
| `time_to_fill_bars` in valid range [0, 7] | ✓ | ✓ |
| Raw r_distance in [0.60, 1.80] (de-slipped per Phase 2u §E.3) | ✓ | ✓ |
| Post-slip r_distance count exceeding band (slip-induced; not bug) | 2 | 0 |
| **All hard checks pass** | **✓** | **✓** |

**No engine-correctness issues.** Two BTC trades have post-slip r_distance > 1.80 due to MED-slip slippage on the recorded fill_price; their raw (pre-slip) r_distances are within [0.60, 1.80], confirming the engine's band check at fill time fired correctly.

The analysis script's two pre-fix issues (Δ|maxDD| sign convention; P.14 post-slip vs raw band reference) were script-level interpretive bugs, not engine bugs; both fixed in 2w-B before final analysis. No spec or sub-parameter changes resulted.

---

## 12. V-window evidence (2025-01-01 → 2026-04-01)

R-window MED-slip §10.3 PROMOTE'd, so V-window run #6 was executed per Phase 2v §11.3.

| Variant | Symbol | Trades | WR | expR | PF | netPct | maxDD |
|---------|--------|-------:|---:|-----:|---:|-------:|------:|
| H0 | BTCUSDT | 8 | 25.00% | −0.313 | 0.541 | −0.56% | −0.87% |
| H0 | ETHUSDT | 14 | 28.57% | −0.174 | 0.695 | −0.55% | −0.80% |
| R3 | BTCUSDT | 8 | 25.00% | −0.287 | 0.580 | −0.51% | −1.06% |
| R3 | ETHUSDT | 14 | 42.86% | −0.093 | 0.824 | −0.29% | −0.94% |
| **R2+R3** | **BTCUSDT** | **5** | **20.00%** | **−0.901** | **0.001** | **−1.00%** | **−0.91%** |
| **R2+R3** | **ETHUSDT** | **12** | **41.67%** | **−0.108** | **0.815** | **−0.29%** | **−0.84%** |

**Observations.**

- **R2+R3 BTC V is severely degraded** (n=5, expR −0.901 vs H0 V −0.313 / R3 V −0.287). The 5 trades are concentrated in losses (WR 20%, PF 0.001 — one trade dominates the loss side). Sample-size fragile: 1 trade flip would change the V mean by ~0.20 R. **The §11.3 V-window evidence is uninterpretable on n=5** — the framework verdict per §11.3 is "wave ends; does not retroactively change R-window classification" but the BTC V data is too thin to add evidence one way or the other.
- **R2+R3 ETH V is near-parity with R3 V** (n=12, expR −0.108 vs R3 V −0.093). The R2 ETH path produces nearly the same V-window outcome as R3 alone with 14% fewer trades. ETH's pullback-retest dynamic on the V-window data is consistent with R3's exit machinery; no large gain or loss vs R3.
- V-window does not change the framework verdict. It does not retroactively reverse the R-window MED-slip §10.3 PROMOTE per §11.3 no-peeking discipline, and the §11.6 gate failure on R-window (§7) was already the binding constraint.

The candidate's wave ends here per Phase 2v §11.3 / §5.1.8.

---

## 13. Slippage sensitivity (already covered in §7)

§11.6 cost-sensitivity is the framework block. Re-stated:

- **LOW**: BTC PROMOTE; ETH DISQUALIFIED (Δexp −0.006 vs H0).
- **MEDIUM (committed)**: both PROMOTE.
- **HIGH**: both DISQUALIFIED (BTC Δexp −0.014; ETH Δexp −0.230).

The cost-sensitivity profile is monotonic in slippage — R2's edge erodes as slippage rises. The MEDIUM band is the only slippage tier where R2+R3 PROMOTES on both symbols. Per Phase 2v §5.1.7, the §11.6 gate evaluates HIGH specifically; both symbols disqualify at HIGH; gate fails.

---

## 14. Stop-trigger sensitivity (already covered in §11.12)

Bit-identical between MARK_PRICE and TRADE_PRICE on both symbols. Zero gap-through stops. No GAP-032 implications.

---

## 15. Fill-model sensitivity (already covered in §11.6)

BTC committed expR = −0.275; diagnostic limit-at-pullback expR = −0.038 (Δ = +0.24 R per trade — large divergence). ETH small divergence (Δ = −0.02). The committed model governs; the diagnostic flags BTC fill-model fragility for any future paper/shadow phase.

---

## 16. PASS / FAIL / HOLD classification

### 16.1 Combined verdict

**FAIL — §11.6 cost-sensitivity blocks.**

Per Phase 2v §5.3 cross-tabulation:

| Layer | Result |
|-------|--------|
| §10.3 MED-slip vs H0 (BTC) | PROMOTE (§10.3.a + §10.3.c) |
| §10.3 MED-slip vs H0 (ETH) | PROMOTE (§10.3.c) |
| §10.3 disqualification floor | NOT triggered |
| §11.4 ETH-as-comparison | SATISFIED |
| §10.4 hard reject | NOT applicable (Δn negative) |
| **§11.6 HIGH-slip cost-sensitivity** | **FAILS (BTC + ETH both disqualified)** |
| §11.3 V-window | R-window PROMOTE'd → V ran; BTC uninterpretable on n=5; ETH near-parity with R3 V; wave ends |
| M1 BTC per-trade expectancy | PASS (+0.123 R on intersection) |
| M2 BTC stop-exit fraction | FAIL (R2 0.261 > R3 0.242) |
| M3 R-distance reduction | PASS on both symbols |
| M2 ETH stop-exit fraction | FAIL (R2 0.526 > R3 0.424) |

**Final classification: FAIL.** The MED-slip §10.3 PROMOTE is preserved as descriptive evidence but is blocked by the §11.6 cost-sensitivity gate.

### 16.2 R3 remains the baseline-of-record

Per Phase 2p §C.1, **R3 (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) remains the project's locked baseline-of-record**. Phase 2w does not change this designation:

- R2+R3 did not promote under §10.3 + §11.6 combined; it cannot displace R3.
- R3-anchor descriptive deltas show R2's marginal contribution on top of R3 is negative on aggregate (BTC Δexp_R3 = −0.035; ETH Δexp_R3 = −0.081).
- R3 alone passes §11.6 (its Phase 2l clearance is on record); R3 remains the cleanest framework-cleared structural redesign the project has produced.

The operator may at any future point re-evaluate R3's baseline-of-record status; that is operator-policy territory outside Phase 2w's scope.

### 16.3 R2 becomes retained research evidence

Per Phase 2p §D framing applied to R2:

- **Closed**: R2 is permanently abandoned. NO — premature; mechanism-partially-supported evidence is informative.
- **Dormant**: set aside without explicit revival conditions. NEAR-MISS.
- **Retained-for-future-hypothesis-planning**: alive specifically as research artifact for any future operator-authorized phase that proposes (a) a different fill-model commitment, (b) a different validity-window length, (c) a different confirmation rule, or (d) a different cost-sensitivity threshold revision. **CHOSEN** — matches the Phase 2m R1a / Phase 2s R1b-narrow framings.

R2 is **not** a deployable variant. R2 is **not** the current default / operating path. R2's per-trade-expectancy-improvement evidence (M1 +0.123 R on BTC intersection) is preserved as research-only.

---

## 17. What the verdict does NOT claim

Mirroring Phase 2s §13 + Phase 2m §13:

- **R2 is not live-ready.** R-window aggregate expR is still negative (BTC R2 −0.275; ETH R2 −0.432). Even at MED-slip framework PROMOTE, the candidate is not operationalized.
- **R2 is not paper-shadow-ready.** Operator restrictions on paper/shadow stand per Phase 2p §F.2. Phase 2w does not propose lifting them.
- **R2 is not Phase 4-ready.** Operator restrictions on Phase 4 stand per Phase 2p §F.3. Phase 2w does not propose lifting them.
- **R2 does not displace R3 as the baseline-of-record.** Phase 2p §C.1 R3 designation is unchanged. R2 becomes retained research evidence per §16.3.
- **R2 does not establish absolute edge.** Even MED-slip framework PROMOTE leaves both R-window symbol-aggregates negative.
- **R2 does not establish "BTC entry-timing was the missing mechanism".** M1 PASSES (per-trade expectancy improves on intersection trades) but M2 FAILS (stop-exit fraction does not improve). The R2 thesis is partially correct — R2 produces real per-trade-expectancy gains on BTC's directional follow-through trades — but the gains are slippage-fragile and do not survive HIGH-cost evaluation.
- **R2 does not solve the absolute-edge gap from within the breakout family.** Three structural-redesign candidates (R1a, R1b-narrow, R2) have now produced framework-PROMOTE-with-mechanism-caveat results without producing absolute positive aggregate expR on either symbol. Phase 2p §F.4 family-abandonment pre-conditions become more relevant after Phase 2w; that is operator-policy territory outside Phase 2w's scope.
- **R2 does not propose revision of the §11.6 threshold.** The HIGH-slippage cost-sensitivity threshold is preserved per Phase 2f §11.3.5 (no post-hoc loosening). Any future revision of §11.6 requires a separate operator-authorized phase with documented evidence of the live-trading slippage profile, not a framework-discipline shortcut.
- **The diagnostic limit-at-pullback intrabar fill model is not a deployable path.** It is a §P.6 sensitivity diagnostic per Phase 2v Gate 2 clarification. The committed next-bar-open-after-confirmation model is the only fill model eligible for §10.3 governing evaluation.
- **No Phase 4 / paper-shadow / live-readiness / MCP / Graphify / `.mcp.json` / credentials / deployment / exchange-write proposals** appear anywhere in this report. All operator restrictions stand.

---

## 18. Threshold preservation

Phase 2f §§ 10.3 / 10.4 / 11.3 / 11.4 / 11.6 thresholds applied unchanged. No post-hoc loosening per §11.3.5. Phase 2j §C.6 R1a sub-parameters preserved (R1a is not part of R2). Phase 2j §D.6 R3 sub-parameters preserved (R3 is the locked exit baseline). Phase 2r §F R1b-narrow sub-parameter preserved (R1b-narrow is not part of R2). Phase 2u §F R2 sub-parameters preserved singularly (pullback level = `setup_high`/`setup_low`; confirmation = close-not-violating-stop; validity window = 8 bars; committed fill model = next-bar-open after confirmation). GAP-20260424-036 fold convention applied unchanged. GAP-20260424-031 / 032 / 033 carried forward unchanged. GAP-20260419-015 stop-distance reference-price convention applied unchanged (close_B at registration; fill_price at fill-time check; both with frozen atr_at_signal). **No new GAP entries introduced in Phase 2w.** Phase 2i §1.7.3 project-level locks preserved (H0 anchor; BTCUSDT primary; ETHUSDT research/comparison only; one-position max; one-symbol-only; 0.25% risk; 2× leverage; mark-price stops; v002 datasets).

---

## 19. Wave / phase preservation

- Phase 2g Wave-1 REJECT ALL preserved as historical evidence only.
- Phase 2l R3 PROMOTE preserved unchanged (R3 sub-parameters frozen; baseline-of-record per Phase 2p).
- Phase 2m R1a+R3 mixed-PROMOTE preserved unchanged (retained-for-future-hypothesis-planning per Phase 2p §D).
- Phase 2s R1b-narrow PROMOTE / PASS preserved unchanged (formal-framework-strongest result with explicit per-trade-expectancy and sample-size caveats; bias-strength: not the missing mechanism per operator + ChatGPT joint interpretation).
- Phase 2t R2 Gate 1 planning memo preserved (GO recommendation conditional on §11.3 discipline locks).
- Phase 2u R2 spec memo (Gate 2 amended) preserved.
- Phase 2v R2 Gate 1 execution plan (Gate 2 amended) preserved.
- Phase 2v Gate 2 review preserved.
- Phase 2w-A checkpoint report preserved (implementation + tests + control reproduction).
- Phase 2w-B checkpoint report preserved (R2 execution + diagnostics).
- **R2's MED-slip §10.3 PROMOTE preserved as descriptive evidence** even though the §11.6 gate failure produces a FAILED combined verdict — the framework-discipline distinction between "MED-slip §10.3 outcome" and "combined verdict including §11.6" is the same evidence-preserving discipline applied throughout Phase 2.
- H0 anchor preserved as the sole §10.3 / §10.4 anchor.

---

## 20. Safety posture

Research-only. No live trading. No exchange-write paths. No production keys. No `.mcp.json`, no Graphify, no MCP server activation. No `.env` changes, no credentials, no Binance API calls (authenticated or public). No edits to `docs/12-roadmap/technical-debt-register.md`. No edits to the implementation-ambiguity log. No edits to `.claude/`. No `data/` commits (run artifacts under `data/derived/backtests/phase-2w-r2-*/` are git-ignored; the analysis JSON under `data/derived/backtests/phase-2w-analysis.json` is git-ignored). No Phase 4 work. No paper/shadow planning. No live-readiness claim. R2's slippage-fragility under the §11.6 gate is documented evidence, NOT operationalized. No comparison-baseline shifting. No merge to main. Mark-price stop-trigger semantic preserved (MARK_PRICE default; TRADE_PRICE only as sensitivity diagnostic per run #9). R3 / R1a / R1b-narrow sub-parameters frozen. R2 sub-parameters frozen at Phase 2u §F values. The 8-bar setup window unchanged. The diagnostic-only limit-at-pullback intrabar fill model exists exclusively as the runner-script `--fill-model` flag (Phase 2v Gate 2 clarification); no `V1BreakoutConfig` field added. The §10.3 framework verdict is governed exclusively by run #3 (committed next-bar-open fill model); run #10 informs interpretation only. **No next phase started. No operator-policy proposals.**

---

**End of Phase 2w R2 (pullback-retest entry) variant comparison report.** Sections 1–20 complete. R-window MED-slip §10.3 PROMOTE preserved as descriptive evidence (BTC §10.3.a + §10.3.c; ETH §10.3.c); §11.6 cost-sensitivity gate FAILS at HIGH slippage on both symbols; combined framework verdict **FAILED — §11.6 cost-sensitivity blocks**. Mechanism reading PARTIALLY SUPPORTED (M1 + M3 PASS; M2 FAILS on both symbols). R3 remains the baseline-of-record per Phase 2p §C.1. R2 becomes retained research evidence (Phase 2p §D framing applied). Threshold preservation, wave/phase preservation, safety posture all preserved unchanged. **No code merge to main, no operator-policy proposals, no next phase started — all explicitly outside Phase 2w-C scope per operator instruction.** Awaiting operator/ChatGPT review.
