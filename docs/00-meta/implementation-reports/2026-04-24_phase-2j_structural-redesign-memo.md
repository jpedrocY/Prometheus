# Phase 2j — Structural Redesign Memo (R1a + R3)

**Working directory:** `C:\Prometheus`
**Branch:** `phase-2j/structural-redesign-memo` (created from `main` at `8a34f20` — verified clean working tree, synchronized with `origin/main` after the Phase 2i PR #10 merge)
**Author:** Claude Code (Phase 2j)
**Date:** 2026-04-24
**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; no post-hoc loosening per §11.3.5); Phase 2g comparison report (REJECT ALL verdict); Phase 2h decision memo (provisional Option B primary recommendation); Phase 2i Gate 1 plan §§ 6–14.A and §26 (three operator Gate 1 conditions applied); Phase 2i redesign-analysis memo (carry-forward set R1a + R3 capped at ≤ 2); Phase 2j Gate 1 plan §§ 4–18.
**Scope:** Decision/planning memo only. No code, no new backtests, no new variants, no data downloads, no Binance API calls, no MCP/Graphify, no `.mcp.json`, no Phase 4 work, no fallback-Wave-2 start, no edits to `docs/12-roadmap/technical-debt-register.md`.

This memo follows the operator's required structure (sections A–J).

---

## A. Executive summary

Phase 2j writes complete rule specs for the two carry-forward candidates from Phase 2i:

- **R1a — Volatility-percentile setup** (Family-S structural redesign): replaces the v1 setup-validity predicate (range-width ≤ 1.75 × ATR20 + drift cap 0.35 × range) with a percentile-based shape (current 15m ATR(20) ≤ X-th percentile of trailing-N ATR distribution). Keeps the 8-bar setup window for setup_high / setup_low determination. Committed sub-parameters: **percentile threshold X = 25** (bottom quartile); **lookback length N = 200** (≈ 50 hours of 15m bars). Falsifiable hypothesis: passes Phase 2f §10.3 vs. H0 on R, with no §10.3 disqualification floor triggered.

- **R3 — Fixed-R exit with time stop** (Family-X structural redesign): replaces the staged-trailing exit machinery (Stage 3 risk reduction at +1.0 R, Stage 4 break-even at +1.5 R, Stage 5 trailing at +2.0 R, Stage 7 stagnation gate) with a two-rule terminal exit (fixed-R take-profit + unconditional time-stop). Initial structural stop, exchange-side STOP_MARKET protective stop, and entry/setup/bias/trigger logic are all kept. Committed sub-parameters: **R-target = 2.0 R**; **time-stop bars = 8**. Falsifiable hypothesis: passes Phase 2f §10.3 vs. H0 on R, with no §10.3 disqualification floor triggered.

**Why R1a and R3 (not R1b or R2).** Phase 2i §3.2 chose R1a because it targets the dominant 58% no-valid-setup funnel rejection on the most evidence-grounded axis (single-axis structural; Wave-1 H-A1 eliminated window-length tweaks); chose R3 because it targets a structurally inactive part of H0 (trailing fired 0/41 BTC, 1/47 ETH) with a clean topology change. Phase 2i §3.2 explicitly excluded R1b (regime classifier is higher-DOF / harder cross-symbol robustness) and R2 (pullback entry needs new pending-limit-fill logic in the backtester; lower trade count makes per-fold consistency harder).

**Why this is still planning, not execution.** This memo writes specs only. No backtests are run, no code is written, no parameters are tuned. The eventual execution against R/V data is a separate operator-approved phase (Phase 2k or later). Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds and the GAP-036 fold convention apply unchanged for that future phase. R1a's and R3's committed sub-parameter values are pre-committed for that future phase — no "different threshold because the redesign is different" loosening is allowed.

**Headline recommendation, provisional and subject to operator review:** **Both R1a and R3 advance to a future operator-approved execution-planning phase**, with R3 prioritized for first execution because its rule shape is more contained, its sub-parameters are more clearly research-default, and its falsifiability surface is smaller. Reasoning is in section H.

---

## B. Fixed evidence recap

### B.1 Phase 2e baseline facts that matter for R1a and R3

Source: `docs/00-meta/implementation-reports/2026-04-20_phase-2e-baseline-summary.md`.

R-window (2022-01..2025-01) baseline numbers used as the comparison anchor:

- **BTCUSDT H0 on R**: 33 trades, WR 30.30%, expR −0.459, PF 0.26, net −3.39%, max DD 3.67%, L/S 16/17, exits dominated by STOP and STAGNATION (TRAIL near zero).
- **ETHUSDT H0 on R**: 33 trades, WR 21.21%, expR −0.475, PF 0.32, net −3.53%, max DD 4.13%, L/S 13/20.

Funnel rejections that motivate the candidates (FULL-window numbers; ratios identical on R since the funnel is a per-bar attribution):

- **`no valid setup` ~57–58%** on both symbols — the dominant rejection that R1a targets.
- **`neutral bias` ~37%** on both symbols — second-largest; not addressed by R1a or R3 (would have been R1b's target).
- **`no close-break` ~5%** on both symbols — third-largest; not addressed.
- **Trailing filters** (TR < ATR, close-location, ATR regime, stop-distance) each < 0.5% — not the binding constraint on funnel attrition.

Exit mix on the wave-1 H0 baseline (FULL window):
- BTC: STOP 22 / STAGNATION 19 / TRAIL 0.
- ETH: STOP 35 / STAGNATION 11 / TRAIL 1.

The trailing-exit count near zero is the structural evidence that motivates R3.

### B.2 Phase 2g wave-1 facts that matter for R1a and R3

Source: `docs/00-meta/implementation-reports/2026-04-24_phase-2g_wave1_variant-comparison.md`.

Wave-1 verdict on R-window: **REJECT ALL** under Phase 2f §10.3 disqualification floor. All four single-axis variants (H-A1, H-B2, H-C1, H-D3) failed against H0 on BTC.

Direct evidence relevant to R1a:

- **H-A1 (setup window 8 → 10)** showed setup-window length is not the binding parameter (BTC trades 33 → 13, expR worsens to −0.831 R). R1a takes the structural-redesign approach to the same axis: replace the predicate's *form* (range-based ratio → percentile ranking), not just the *length*.

Direct evidence relevant to R3:

- **H-D3 (break-even +1.5 R → +2.0 R)** produced essentially identical entry/exit counts and marginally worse expR (−0.475 vs −0.459 on BTC) — confirming that within the staged-trailing exit philosophy, threshold tweaks don't move the needle. R3 takes the structural-redesign approach: replace the staged-trailing topology entirely.
- **H-B2 (expansion 1.0 → 0.75 × ATR20)** showed that loosening the trigger improves edge (Δexp +0.133 R, ΔPF +0.17) but proportionally increases drawdown (|maxDD| ratio 1.505x, vetoed by §10.3 disqualification). This is diagnostic input for R3: any future redesign that increases trade count must have an exit machinery capable of handling the proportionally larger drawdown. R3's fixed-2R + time-stop is a candidate exit shape that (a) doesn't depend on trailing-machine behavior, (b) caps the per-trade time-at-risk at 8 bars, and (c) can be evaluated as a clean structural commitment.

### B.3 Phase 2i rationale for choosing R1a and R3

Source: `docs/00-meta/implementation-reports/2026-04-24_phase-2i_redesign-analysis.md` §3.2.

- **R1a was chosen** because it targets the largest funnel rejection (58% no-valid-setup) on a single axis whose parametric equivalent (H-A1 window length) was tested and failed. A volatility-percentile shape consumes a different signal-form (rolling-percentile of ATR) than range-based ratio — a genuine rule-shape change. Implementation is contained to the setup detector. Highest-evidence-grounded structural candidate among Family S.
- **R3 was chosen** because it targets a structurally inactive part of the current strategy (trailing-exit count near zero) with an exit-philosophy commitment that removes most of the staged-trailing machinery. Cleanly contained to TradeManagement. Spec is the most achievable for R3 because the exit form is the simplest to pre-declare.
- **R1b (ADX/regime HTF bias) was NOT chosen** because regime classifiers have higher overfitting risk and harder ETH-as-comparison cross-symbol robustness; carrying both R1a and R1b would also exceed the ≤ 2 cap and constitute a multi-axis structural change that the §2.2 R1 coherence test had already split.
- **R2 (pullback-confirmed entry) was NOT chosen** because the wave-1 stop-out evidence is indirect; the backtester needs new pending-limit-fill logic; and the reduction in trade count makes per-fold consistency harder to establish.

### B.4 Explicit preservation contracts

Phase 2j preserves exactly:

- **The Phase 2g wave-1 verdict (REJECT ALL).** No re-derivation. No re-ranking. Wave-1 numbers may be cited diagnostically (as in §B.2 above) but do not serve as comparison baselines for R1a or R3.
- **H0 as the sole comparison anchor.** All §10.3 / §10.4 evaluation for any future R1a or R3 execution is against H0 (locked Phase 2e baseline re-run on R), never against wave-1 variants.
- **The Phase 2i ≤ 2 carry-forward discipline.** Only R1a and R3 are specced. No third candidate is added.
- **The Phase 2h provisional recommendation framing.** Phase 2h is the input that led to Phase 2i; Phase 2i is the input that led to Phase 2j. Neither is a target for revision.

---

## C. Full redesign spec for R1a — Volatility-percentile setup

### C.1 Objective / thesis

**Thesis.** The dominant 58% no-valid-setup funnel rejection results from a setup shape (range-width as a fraction of ATR, with a drift cap) that does not reliably capture volatility-contraction periods preceding genuine breakouts. Replacing this rule shape with a percentile-based predicate that ranks the current ATR against its trailing distribution captures regime-aligned volatility contractions more cleanly. Wave-1 H-A1 already eliminated the "tweak the window length" alternative; H-A2 / H-A3 (range-width ceiling and drift-cap value tweaks) are parametric and untested. R1a is the structural-redesign equivalent that changes the predicate's *form*, not just its *values*.

### C.2 Exact rule shape

At the close of every completed 15m bar B that is the **breakout candidate** (i.e., B is the bar at which an entry intent is being evaluated):

1. The setup window is the **8 completed 15m bars strictly before B** (preserved from H0; same as `prior_8` in `src/prometheus/strategy/v1_breakout/strategy.py:362–366` per the v1 spec). This determines `setup_high` (max of those 8 bars' high) and `setup_low` (min of those 8 bars' low) — used downstream by the trigger.
2. **Setup-validity predicate (R1a-specific, replaces H0's two-clause predicate):**
   - Compute the 15m ATR(20) value as of the close of bar B−1 (the last bar of the setup window). Call this `atr_prior_15m` — same definition as H0.
   - Compute the rolling distribution of `atr_prior_15m` over the trailing **N completed 15m bars ending at B−1** (N committed in §C.6).
   - The setup is **valid** iff `atr_prior_15m` ≤ the **X-th percentile** of that distribution (X committed in §C.6). Lower percentile = volatility contraction.
3. If the setup-validity predicate fails, the bar is rejected with funnel attribution `rejected_no_valid_setup` (same as H0; no new rejection bucket needed).
4. If it passes, downstream logic (trigger, ATR regime check, stop calculation, sizing) runs unchanged from H0.

### C.3 Exact inputs used

- **15m completed klines**, ending at the close of bar B−1 (used for both the setup window and the trailing N-bar percentile distribution).
- **15m Wilder ATR(20)**, computed at the close of B−1 (already maintained as `_15m_atr_before_latest` in `StrategySession`).
- **Rolling N-bar window of historical 15m ATR(20) values** (new — see §C.5 implementation impact).

No 1h inputs. No mark-price inputs. No funding inputs.

### C.4 Exact timeframes

- **Decision timeframe:** 15m (same as H0).
- **Bias timeframe:** 1h (unchanged; R1a does not touch bias).
- **Setup window:** 8 × 15m = 2 hours (unchanged from H0).
- **Percentile lookback:** N × 15m bars (committed in §C.6).

### C.5 Exact setup-validity predicate (mathematical form)

Let `A_t` denote the 15m Wilder ATR(20) value computed at the close of bar `t`. At decision time at the close of bar B (the breakout candidate):

```
A_prior = A_{B-1}
Q_prior = { A_{B-N}, A_{B-N+1}, ..., A_{B-1} }    (N values, ending at B-1)

setup_valid iff
    rank(A_prior, Q_prior) <= floor(X * N / 100)
```

where `rank(v, S)` returns the 1-indexed ascending rank of `v` within sorted multiset `S` (ties broken by stable order). Equivalently: the setup is valid iff `A_prior` is in the bottom X% of the trailing-N distribution.

**Boundary cases:**

- Until **B ≥ N + 21** (enough history for both the percentile lookback and the ATR(20) seed at B−N), the setup-validity predicate **rejects** (same warmup behavior as the existing min_15m_bars_for_signal floor; an updated floor is computed for R1a in §C.10).
- If `Q_prior` contains any NaN (insufficient ATR seed at any point in the lookback), the predicate **rejects**.
- If two or more values in `Q_prior` tie with `A_prior` at the X-th percentile boundary, the rank-based comparison resolves ties by stable order; the predicate is deterministic.

### C.6 Exact committed sub-parameter values

- **Percentile threshold X = 25** — the bottom quartile of the trailing-N distribution. **Justification:** 25th percentile is the standard "compressed-volatility regime" cutoff in volatility-contraction literature (e.g., Bollinger-band squeeze references commonly use the bottom quartile or bottom decile; 25% is the more lenient end of that range, which preserves trade frequency while still requiring meaningful contraction). Round number; not selected by fitting.
- **Lookback length N = 200 bars** — approximately 50 hours of 15m bars (≈ 2.08 days). **Justification:** 200 bars captures multi-session volatility regime context without either being so short that the percentile is dominated by recent intra-session noise (N < 50) or so long that the percentile lags genuine regime shifts (N > 500). Round number consistent with common rolling-window conventions.
- **Minimum sample / warmup rule:** the predicate rejects until `bars_observed_15m ≥ N + ATR_PERIOD + 1` (= 200 + 20 + 1 = **221 bars**), matching the existing project pattern of "warmup until both the window AND the indicator seed are valid". The eventual execution phase computes this warmup floor explicitly and adjusts `MIN_15M_BARS_FOR_SIGNAL` accordingly.

These values are committed singularly. The execution phase does not sweep them. If a different value is needed, it requires a new operator-approved spec.

### C.7 Exact relationship to existing trigger / bias / entry / stop / exit logic

R1a only changes the setup-validity predicate. Everything else is preserved:

- **Trigger:** unchanged. The breakout-bar TR vs. ATR check, close-break-by-buffer check, close-location top-25%/bottom-25% check, and ATR-regime check all use H0's logic (`evaluate_long_trigger` / `evaluate_short_trigger` with default `expansion_atr_mult=1.0` per `trigger.py`).
- **Bias:** unchanged. 1h EMA(50) / EMA(200) + slope rule per `bias.py` and `StrategySession._update_1h_bias`.
- **Entry:** unchanged. Market entry on the next-bar open after the breakout-bar close (per `engine.py:269` window logic and `_maybe_open_trade`).
- **Stop:** unchanged. Structural stop = `min(setup_low, breakout_bar_low) - 0.10 × ATR20` for long (symmetric for short) per `stop.py:compute_initial_stop`. Stop-distance band 0.60 ≤ d ≤ 1.80 × ATR20 unchanged.
- **Exit:** unchanged from H0. Stage 3 risk reduction at +1.0 R, Stage 4 break-even at +1.5 R, Stage 5 trailing at +2.0 R with 2.5 × ATR20 trail, +1.0 R MFE stagnation gate at 8 bars — all preserved as H0 specifies.
- **Sizing:** unchanged. risk_fraction=0.0025, risk_usage=0.90, max_leverage=2.0, notional_cap=100_000, taker=0.0005, slippage=MEDIUM, equity=10_000.

### C.8 What H0 rules are replaced

- **Setup-validity predicate** (the two-clause rule in `setup.py:detect_setup`: range_width ≤ 1.75 × ATR20 AND |close[-1] - open[-8]| ≤ 0.35 × range_width). R1a replaces this entire predicate with the §C.5 percentile rule.
- The `MAX_RANGE_ATR_MULT = 1.75` and `MAX_DRIFT_RATIO = 0.35` constants in `setup.py` are no longer in the rule logic.

### C.9 What H0 rules remain unchanged

- The 8-bar setup window (preserved; R1a still uses the 8 bars strictly before the breakout candidate to define `setup_high` / `setup_low`).
- The `SETUP_SIZE = 8` constant in `setup.py` (kept; R1a does not touch window length per Wave-1 H-A1 evidence).
- The setup-window keying convention ("strictly before the breakout bar" per GAP-20260424-034 verification).
- Trigger, bias, entry, stop, exit, sizing — all per §C.7.
- Project-level locks per Phase 2i §1.7.3 (BTCUSDT live primary, one-way mode, isolated margin, one position max, 0.25% live risk, 2x leverage, mark-price stops, v002 datasets).

### C.10 Implementation impact (descriptive only — Phase 2j writes no code)

A future execution phase would extend the strategy package as follows. **Phase 2j does not write any of this code; it is described here only so the spec is complete.**

- `V1BreakoutConfig` would gain three new optional fields: `setup_predicate_kind: Literal["RANGE_BASED", "VOLATILITY_PERCENTILE"]` (default RANGE_BASED preserves H0); `setup_percentile_threshold: int = 25` (used only when kind is VOLATILITY_PERCENTILE); `setup_percentile_lookback: int = 200`.
- `setup.py` would add a sibling function `detect_setup_volatility_percentile(prior_bars, atr_prior_15m, atr_history, *, percentile_threshold: int, lookback: int)` returning `SetupWindow | None`.
- `StrategySession` would maintain a rolling deque of `atr_prior_15m` values of length `setup_percentile_lookback` (similar to the existing `_1h_ema_fast_history`).
- `MIN_15M_BARS_FOR_SIGNAL` becomes config-aware: for VOLATILITY_PERCENTILE, the warmup floor is `lookback + ATR_PERIOD + 1` (= 221 at committed values).
- `V1BreakoutStrategy.maybe_entry` would dispatch to `detect_setup` or `detect_setup_volatility_percentile` based on `config.setup_predicate_kind`.
- `_IncrementalIndicators` in `diagnostics.py` would maintain the parallel ATR-history ring for funnel-attribution accuracy.
- New tests would prove (a) defaults preserve H0 bit-for-bit, (b) at VOLATILITY_PERCENTILE with X=25, N=200 the predicate rejects degenerate cases (NaN ATR seeds, insufficient history, ties at boundary), (c) the funnel counter increments `rejected_no_valid_setup` for both predicate kinds.

This implementation surface is comparable in size to Phase 2g's wave-1 wiring (10 source files modified + 1 new test file). No new dependencies. No structural changes to the engine or backtest config beyond the new optional fields.

### C.11 Expected mechanism of improvement

The percentile-based predicate is **regime-aware**: it ranks the current ATR against the recent distribution rather than against an absolute threshold (ATR multiplier). In low-volatility regimes the absolute ATR is small, so H0's `range_width ≤ 1.75 × ATR20` admits many setups (because the ATR floor is low), but those setups may not represent genuine compression — just normal low-vol behavior. In high-volatility regimes the absolute ATR is large, so H0's predicate rejects most bars (because compression looks too tight relative to a large ATR). R1a's percentile rule normalizes this: a setup is "valid" iff the current vol is in the bottom 25% of the recent N-bar distribution, regardless of absolute level. The mechanism of improvement: capture genuine contraction-then-expansion patterns more cleanly across all volatility regimes, reducing the 58% no-valid-setup rejection without admitting noise.

### C.12 Expected main failure mode

The most likely failure mode: the percentile filter at X=25 admits *too much* — it captures bars where the current vol is locally low but not in a genuine pre-breakout compression. The trade frequency increases, the stop-out rate stays high (because the filter doesn't actually identify breakout-prone setups), and expR worsens or holds flat. This is the H-A2 pattern (range-width ceiling 1.75 → 2.00 — untested but conjectured) playing out via a different rule shape. If R1a fails on R via §10.3 disqualification on worse expR / worse PF, this is the most plausible cause.

Less likely but possible failure modes:
- Lookback N=200 is too short for some regimes (filter responds too quickly to vol shifts), or too long for others (filter lags). Symptoms: per-fold expR varies more than H0 across fold boundaries.
- Boundary cases (NaN seeds, ties at the 25th percentile) produce more rejections than expected, reducing trade frequency below H0. Symptoms: trade count drops and expR doesn't change much.

The Phase 2k execution phase's per-fold + per-regime diagnostics (per Phase 2i §2.5.5) would distinguish these failure modes.

### C.13 Why R1a is structural and not parametric

The §1.7 binding test (Phase 2i memo §1.7.1):

- Rule shape changes from "range-based ratio" to "percentile-based ranking". The predicate's mathematical form is different: H0 uses `(max - min) / ATR ≤ 1.75` (a ratio comparison); R1a uses `rank(ATR_now, ATR_history) ≤ 25%` (a quantile/order-statistic comparison). Different operation, different signal type.
- Rule input domain changes: H0's predicate consumes `[setup_high, setup_low, atr_prior_15m, drift]`; R1a's predicate consumes `[atr_prior_15m, atr_history_N]`. Different inputs (no setup_high/setup_low/drift in the predicate; new atr_history input).

Even though R1a has parameter values (X=25, N=200), the rule shape change is genuine. Per Phase 2i §1.7.2, "changing a numeric threshold while keeping the same rule shape" is parametric (e.g., 1.75 → 2.00); R1a is changing the *form* of the predicate, not just a threshold within the form.

### C.14 GAP dispositions

| GAP | Topic | R1a disposition |
|---|---|---|
| GAP-20260424-030 | Break-even +1.5R vs +2.0R rule-text conflict | **CARRIED** — R1a keeps current exit logic, so the conflict stays open. To be resolved by a separate redesign or by GAP-030's eventual operator decision. |
| GAP-20260424-031 | EMA slope wording (discrete vs. fitted) | **CARRIED** — R1a keeps current bias rule. |
| GAP-20260424-032 | Mark-price stop-trigger sensitivity | **CARRIED — required report cut for any future R1a execution wave** per Phase 2i §2.5.5. The execution phase must run R1a with `stop_trigger_source=TRADE_PRICE` and report comparison vs. MARK_PRICE. |
| GAP-20260424-033 | Stagnation window classification | **CARRIED** — R1a keeps current exit including stagnation. |

No GAPs are SUPERSEDED by R1a.

### C.15 Candidate-specific falsifiable hypothesis

> **R1a hypothesis (pre-committed):** On R = 2022-01-01 → 2025-01-01 with v002 datasets, R1a (Volatility-percentile setup with X=25, N=200, all other rules from H0 unchanged) produces a §10.3-passing result vs. H0 baseline — i.e., either §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) or §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse by > 1.0 pp), with no §10.3 disqualification floor triggered (no worse expR, no worse PF, |maxDD| ≤ 1.5× baseline).
>
> **The hypothesis is FALSIFIED if** R1a fails §10.3 on BTC OR triggers §10.3 disqualification on BTC, OR triggers §10.3 disqualification on ETH (per §11.4 ETH-as-comparison: ETH must not catastrophically fail).
>
> **The hypothesis is INDETERMINATE if** results clear §10.3 on R but fail on V (per §11.3 top-1–2 promotion to V; failure on V does not retroactively change R-window classification but does end the candidate's wave).

### C.16 Candidate-specific mandatory diagnostics beyond the common framework

In addition to the common framework's per-regime expR / MFE distribution / long-short asymmetry / mark-price sensitivity (per Phase 2i §2.5.5, restated in section F below), R1a's execution phase must also record:

- **Setup-validity rate per fold.** The fraction of bars where R1a's predicate is `valid` vs. H0's predicate's valid rate, per 6-month fold and per symbol. This is the diagnostic that confirms R1a is changing the funnel attribution as expected.
- **ATR-percentile distribution at trade entries.** The realized percentile rank of `atr_prior_15m` at each filled entry — i.e., where in the trailing-N distribution the entries actually fell. If R1a's filter is admitting non-compression bars (the §C.12 failure mode), this distribution will not concentrate near the bottom of the rank.

These two diagnostics are mandatory for R1a; they are not required for R3 (and not required for the common framework).

---

## D. Full redesign spec for R3 — Fixed-R exit with time stop

### D.1 Objective / thesis

**Thesis.** The H0 staged-trailing exit philosophy (Stage 3 risk reduction at +1.0 R, Stage 4 break-even at +1.5 R, Stage 5 trailing at 2.5 × ATR20, Stage 7 stagnation gate at 8 bars + 1.0 R MFE) is structurally inactive on the wave-1 BTC baseline (TRAIL exits = 0/41) and dominated by STOP and STAGNATION outcomes. The trailing-machine never fires because most trades stop out before reaching +2.0 R MFE. R3 replaces the entire 7-stage state machine with a two-rule terminal exit (fixed-R take-profit + unconditional time-stop) that aligns with how trades actually behave: lock in a 2-R win when it happens; exit at 8 bars regardless of outcome.

This thesis is structural, not parametric, because the trade-management state machine collapses from 7 stages (initial → risk-reduced → break-even → trailing → terminal) to 3 (initial → target-pending → terminal). The Stage 3 / 4 / 5 transitions are removed entirely, not merely retuned.

### D.2 Exact exit philosophy

Three terminal-exit rules, evaluated in the following priority order at every completed 15m bar after the entry fill:

1. **Protective-stop hit (highest priority; identical to H0).** If the mark-price 15m kline at this bar's open_time intersects the active protective stop level (at H0's structural stop = `min(setup_low, breakout_bar_low) - 0.10 × ATR20` for long; symmetric for short), the trade closes per `stops.evaluate_stop_hit`. Exit reason = `STOP`. Slippage applied per the active config.
2. **Take-profit hit.** If the bar's high (long) or low (short) reaches `entry_price + R_TARGET × initial_R` (long) or `entry_price - R_TARGET × initial_R` (short), the trade closes at the next bar's open. Exit reason = `TAKE_PROFIT` (new exit reason; see §D.10 implementation impact). The R_TARGET commitment is in §D.6.
3. **Time-stop fire.** If `bars_in_trade ≥ TIME_STOP_BARS`, the trade closes at the next bar's open regardless of MFE / MAE. Exit reason = `TIME_STOP` (new exit reason). The TIME_STOP_BARS commitment is in §D.6.

If none of the three fires, the trade continues to the next bar.

### D.3 Exact take-profit rule

- **Long:** trade closes if `bar.high ≥ entry_price + R_TARGET × initial_R`. The fill happens at the **next bar's open** (consistent with H0's exit-fill convention per `engine.py` and `fills.exit_fill_price`). Slippage applied. Note: this is a high-of-bar trigger followed by next-bar-open fill — same conservative conservative-fill convention as H0's managed exits.
- **Short:** trade closes if `bar.low ≤ entry_price - R_TARGET × initial_R`. Fill at next bar's open with slippage.

Where `initial_R = abs(entry_price - initial_stop)` (the per-trade risk magnitude at entry, identical to H0's `r_magnitude` in `management.py`).

If a single bar both hits the protective stop and crosses the take-profit threshold, the **protective stop wins** (priority 1 in §D.2). This matches H0's "stop is highest priority" convention and is the conservative choice (simulating the worst-case outcome).

### D.4 Exact time-stop rule

- The bar counter increments on every completed 15m bar after the entry fill (same as `bars_in_trade` in `management.TradeManagement`).
- When `bars_in_trade ≥ TIME_STOP_BARS` (= 8 per §D.6 commitment), and neither the protective stop nor the take-profit has fired on this bar, the trade closes at the next bar's open. Exit reason = `TIME_STOP`.
- The time-stop is **unconditional** — there is no MFE gate. This is different from H0's stagnation rule (which requires `MFE < +1.0 R` at 8 bars). R3's time-stop fires regardless of MFE.

### D.5 Exact interaction with the initial stop

The initial structural stop is **preserved**:

- `initial_stop = min(setup_low, breakout_bar_low) - 0.10 × ATR20` for long (symmetric for short) per H0's `stop.compute_initial_stop`.
- Stop-distance band 0.60 × ATR20 ≤ stop_distance ≤ 1.80 × ATR20 unchanged.
- Exchange-side STOP_MARKET protective stop with `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE` — unchanged.
- The protective stop is **never moved** during the trade. There is no Stage 3 risk reduction (H0's stop move to entry − 0.25 × initial_R), no Stage 4 break-even (H0's stop move to entry_price), no Stage 5 trailing (H0's trail at 2.5 × ATR20 from peak). R3's stop level stays at the initial structural stop until either the protective stop, the take-profit, or the time-stop fires.

This is the structural simplification: H0's "stop moves three times during the trade" becomes R3's "stop stays where it started".

### D.6 Exact committed sub-parameter values

- **R_TARGET = 2.0** — the take-profit multiple. **Justification:** 2.0 R is the standard "double-the-risk" fixed-target convention in trading literature; cleanly aligns with H0's existing Stage 5 trailing-activation threshold (which fires at +2.0 R MFE in H0); the most defensible round number that is neither too tight (1.0 R doesn't capture the asymmetry that breakout strategies typically exploit) nor too far (3.0 R requires market moves that the wave-1 H0 baseline rarely produces — only 2 BTC trades in the entire 41-trade wave-1 baseline reached +2.0 R MFE, and ~5 reached +3.0 R MFE according to Phase 2g exit-mix evidence).
- **TIME_STOP_BARS = 8** — the time-based exit horizon. **Justification:** 8 bars matches H0's existing stagnation-window count (`STAGNATION_BARS = 8` in `management.py:43`), preserving project-level continuity with how the v1 spec already thinks about time horizons. Round number aligned with existing convention; not selected by fitting.

These values are committed singularly. The execution phase does not sweep them (e.g., does not test 1.5 R / 2.0 R / 2.5 R, or 6 / 8 / 10 bars). If a different value is needed, it requires a new operator-approved spec.

### D.7 Whether any staged management remains

**No.** The 7-stage state machine (`TradeStage.STAGE_2_INITIAL → STAGE_3_RISK_REDUCED → STAGE_4_BREAK_EVEN → STAGE_5_TRAILING → terminal exit`) collapses to 3 effective states: `INITIAL` (post-entry, no exit triggered yet), `TARGET_PENDING` (R_TARGET hit, awaiting next-bar-open fill), and terminal. There is no risk reduction, no break-even move, no trailing.

### D.8 Whether break-even remains or is removed

**Removed.** Stage 4's break-even logic (`management.py:215`: stop moved to entry_price when MFE ≥ +1.5 R) is removed entirely. R3's protective stop remains at the initial structural stop until terminal exit.

### D.9 Whether trailing remains or is removed

**Removed.** Stage 5's trailing logic (`management.py:230`: stop activated at +2.0 R MFE, trailing at 2.5 × ATR20 from highest_high_since_entry / lowest_low_since_entry) is removed entirely. The 2.5 × ATR20 trailing multiplier is no longer in the rule.

### D.10 What H0 rules are replaced

- **Stage 3 risk reduction** (`management.py:202`): MFE ≥ +1.0 R → stop moved to entry_price ± 0.25 × initial_R. **REPLACED with: nothing.** R3 has no Stage 3.
- **Stage 4 break-even** (`management.py:215`): MFE ≥ +1.5 R → stop moved to entry_price. **REPLACED with: nothing.**
- **Stage 5 trailing activation** (`management.py:230`): MFE ≥ +2.0 R → trailing active using 2.5 × ATR20 trail from peak. **REPLACED with: take-profit at exactly +2.0 R (R_TARGET = 2.0).**
- **Stage 7 stagnation gate** (`management.py:272`: bars_in_trade ≥ 8 AND MFE < +1.0 R → exit). **REPLACED with: unconditional time-stop at 8 bars (no MFE gate).**

The constants `STAGE_3_MFE_R = 1.0`, `STAGE_3_NEW_STOP_R = -0.25`, `STAGE_4_MFE_R = 1.5`, `STAGE_5_MFE_R = 2.0`, `TRAIL_ATR_MULT = 2.5`, `STAGNATION_MFE_THRESHOLD_R = 1.0` are no longer in R3's rule logic. `STAGNATION_BARS = 8` is reused as `TIME_STOP_BARS = 8` (numerically identical, semantically different — see GAP-033 disposition in §D.13).

### D.11 What H0 rules remain unchanged

- **Setup-validity predicate** (the H0 range-based ratio + drift cap rule in `setup.py`). R3 does not touch the setup.
- **HTF bias rule** (1h EMA(50)/EMA(200) + slope per `bias.py`). R3 does not touch the bias.
- **Trigger** (the six-condition long/short trigger per `trigger.py`). R3 does not touch the trigger.
- **Entry timing** (market entry on next-bar open after breakout-bar close). R3 does not touch the entry.
- **Initial structural stop formula** (`stop.compute_initial_stop`). R3 preserves the initial stop calculation exactly as H0.
- **Stop-distance band** (0.60 ≤ d ≤ 1.80 × ATR20 per `stop.passes_stop_distance_filter`). R3 preserves this filter.
- **Exchange-side STOP_MARKET protective stop** with `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE`. R3 preserves the exchange-side stop semantics.
- **Sizing pipeline** (`sizing.compute_size`). R3 does not touch sizing.
- **Re-entry lockout** (`StrategySession.can_re_enter` requires `setup_size` bars after exit). R3 preserves re-entry lockout.
- **Project-level locks per Phase 2i §1.7.3** (BTCUSDT live primary, one-position max, isolated margin, 0.25% live risk, 2x leverage cap, mark-price stops, v002 datasets).

### D.12 Implementation impact (descriptive only — Phase 2j writes no code)

A future execution phase would extend the strategy package as follows. **Phase 2j does not write any of this code.**

- `V1BreakoutConfig` would gain three new optional fields: `exit_kind: Literal["STAGED_TRAILING", "FIXED_R_TIME_STOP"]` (default STAGED_TRAILING preserves H0); `exit_r_target: float = 2.0`; `exit_time_stop_bars: int = 8`.
- `management.py` would either add a sibling `FixedRTimeStopManagement` class or extend `TradeManagement.on_completed_bar` to dispatch on `exit_kind`. The `ExitReason` enum would gain `TAKE_PROFIT` and `TIME_STOP` values.
- `V1BreakoutStrategy.manage` would route through the new dispatcher.
- `engine.py` and `report.py` would handle the two new exit reasons in trade-record emission and reporting (monthly/yearly breakdown counters extended).
- New tests would prove (a) defaults preserve H0 bit-for-bit, (b) at FIXED_R_TIME_STOP with 2.0 R / 8 bars, the management transitions only between INITIAL → TAKE_PROFIT or INITIAL → TIME_STOP or INITIAL → STOP, (c) take-profit fills happen at next-bar open with slippage, (d) time-stop fires unconditionally at 8 bars, (e) initial protective stop is never moved during the trade.

This implementation surface is comparable in size to or smaller than R1a's: ~5–7 source files modified + 1 new test file. No new dependencies. No structural changes to the engine or backtest config beyond the new optional fields.

### D.13 Expected mechanism of improvement

The H0 staged-trailing exit philosophy is structurally inactive on the wave-1 BTC baseline: TRAIL exit count is **0 of 41 trades**. Most trades exit via STOP (22) or STAGNATION (19) before reaching the +2.0 R MFE trailing-activation threshold. The Stage 3 / 4 transitions add overhead (multiple stop moves) without changing the outcome distribution. R3 replaces this inactive machinery with a clean two-rule terminal exit:

- **Take-profit at +2.0 R** systematically locks in the rare 2-R winners that H0's trailing would have captured equally (since H0's trail activates at +2.0 R MFE) but without the trailing whipsaw that drags a winner back below 2.0 R after the trail activates.
- **Time-stop at 8 bars (unconditional)** systematically caps per-trade time-at-risk. H0's stagnation-with-MFE-gate is conditional (`bars_in_trade ≥ 8 AND MFE < +1.0 R`), which means a trade that reached +1.0 R but then drifted back below H0's break-even can sit in limbo. R3's time-stop closes it.

The mechanism of improvement is **distributional cleanup**: the per-trade R distribution becomes bimodal (stop-out at −R, or take-profit at +2 R, with a tail of time-stops in between), removing the +0.25 R / +0 R / +1.5 R intermediate outcomes that H0's staged-trailing produces. If the breakout family has any genuine edge, R3 should expose it more cleanly; if it doesn't, R3 should fail cleanly without the noise that H0's multi-stage exits introduce.

### D.14 Expected main failure mode

The most likely failure mode: real big winners (those that reach +3 R, +4 R, +5 R MFE) are clipped at +2 R. If the breakout family's edge depends on the rare big winners (which is plausible for breakout-continuation strategies), R3's fixed-2 R cap erodes that edge by design. Symptoms: expR is similar or slightly worse than H0; PF is similar or slightly worse; the per-fold expR distribution shows the worst folds are about as bad as H0's worst folds (because R3 doesn't help in regimes where the strategy doesn't work) and the best folds are no better than H0's best folds (because R3 caps the upside).

Less likely but possible failure modes:
- The 8-bar unconditional time-stop fires on slow-developing winners that would have reached +2 R if given 12 or 16 bars. Symptoms: TIME_STOP exit count is high; per-trade hold-time mean is near 8; per-regime expR shows the time-stop is biting in low-volatility regimes.
- The lack of break-even / trailing means trades that reach +1.5 R MFE can drift back to the initial stop, producing a worse drawdown profile than H0 in regimes where H0's break-even would have salvaged them. Symptoms: per-fold |maxDD| ratio of R3 vs. H0 exceeds 1.5x on at least one fold.

The Phase 2k execution phase's per-fold + per-regime + MFE distribution diagnostics (per Phase 2i §2.5.5) would distinguish these failure modes.

### D.15 Why R3 is structural and not parametric

The §1.7 binding test:

- **Trade-lifecycle topology change.** H0's lifecycle has 7 nominal stages (`STAGE_2_INITIAL`, `STAGE_3_RISK_REDUCED`, `STAGE_4_BREAK_EVEN`, `STAGE_5_TRAILING`, plus terminal STOP / TRAILING_BREACH / STAGNATION / END_OF_DATA). R3's lifecycle has 3 stages (initial, target-pending, terminal). The state-machine topology is different — fewer states, different transition predicates, different terminal-exit reasons. Per Phase 2i §1.7.1, "a change to trade-lifecycle topology" is structural.
- **Rule output coupling change.** In H0, the management object emits `StopUpdateIntent` events (for Stage 3, 4, 5 transitions) and `ExitIntent` events. In R3, the management emits **only** `ExitIntent` events (no stop-move events because the stop never moves intra-trade). The output coupling between management and engine is simpler.
- **Rule shape change.** H0's exit predicates are MFE-threshold-based (`mfe_r ≥ 1.0`, `mfe_r ≥ 1.5`, `mfe_r ≥ 2.0`); R3's exit predicates are price-and-time-based (`bar.high ≥ entry + 2 × initial_R`, `bars_in_trade ≥ 8`). Different signal types (MFE in R-multiples vs. raw price + bar count).

R_TARGET = 2.0 and TIME_STOP_BARS = 8 are committed parameter values within the structural rule shape (per Phase 2i §1.7.2 — committing a value once is a parameter; sweeping multiple values would be a parametric search). The fact that 2.0 R numerically matches H0's STAGE_5_MFE_R is a coincidence of common conventions, not a sign that R3 is "just" a parameter tweak: the entire state-machine collapse is what makes R3 structural.

### D.16 GAP dispositions

| GAP | Topic | R3 disposition |
|---|---|---|
| GAP-20260424-030 | Break-even +1.5R vs +2.0R rule-text conflict | **SUPERSEDED.** R3 removes the break-even rule from the exit machinery entirely. The +1.5R-vs-+2.0R rule-text conflict becomes moot for R3's spec. To be marked SUPERSEDED in the ambiguity log when R3 is selected for execution. |
| GAP-20260424-031 | EMA slope wording (discrete vs. fitted) | **CARRIED** — R3 keeps current bias rule. |
| GAP-20260424-032 | Mark-price stop-trigger sensitivity | **CARRIED — required report cut for any future R3 execution wave** per Phase 2i §2.5.5. |
| GAP-20260424-033 | Stagnation window (8 bars, +1R gate) classification | **CARRIED-AND-EXTENDED** — R3's 8-bar time-stop is similar in numeric value to H0's stagnation-window count but **semantically different**: R3's time-stop is **unconditional** (no MFE gate); H0's stagnation is **conditional** (`bars_in_trade ≥ 8 AND MFE < +1.0 R`). R3's spec explicitly chooses the unconditional interpretation per §D.4. The original GAP-20260424-033 classification question (parametric vs. structural) is still open for non-R3 contexts; R3's spec resolves it for R3's own use. |

R3 SUPERSEDES GAP-030 and CARRIES-AND-EXTENDS GAP-033. R1a does neither.

### D.17 Candidate-specific falsifiable hypothesis

> **R3 hypothesis (pre-committed):** On R = 2022-01-01 → 2025-01-01 with v002 datasets, R3 (Fixed-R exit with R_TARGET = 2.0, TIME_STOP_BARS = 8, all entry/setup/bias/trigger rules from H0 unchanged, initial structural stop preserved) produces a §10.3-passing result vs. H0 baseline — i.e., either §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05) or §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse by > 1.0 pp) or §10.3.c (exit-model bake-off strict dominance on both expR and maxDD), with no §10.3 disqualification floor triggered (no worse expR, no worse PF, |maxDD| ≤ 1.5× baseline).
>
> **Note on §10.3.c applicability.** Phase 2f §10.3.c was originally written for an explicit exit-model bake-off (H-D6) that compared multiple exit philosophies side by side. R3 is a *commitment* to one exit philosophy, not a comparative bake-off. R3's hypothesis primarily targets §10.3.a or §10.3.b paths. §10.3.c is included for completeness because R3's structural change is exit-philosophy-only (the setup, bias, trigger, entry, initial stop are all H0); if R3 strictly dominates H0 on both expR and maxDD, that is a clean §10.3.c-style result and qualifies as promotion regardless of the trade-count change.
>
> **The hypothesis is FALSIFIED if** R3 fails §10.3 on BTC OR triggers §10.3 disqualification on BTC, OR triggers §10.3 disqualification on ETH (per §11.4 ETH-as-comparison: ETH must not catastrophically fail).
>
> **The hypothesis is INDETERMINATE if** results clear §10.3 on R but fail on V (per §11.3 top-1–2 promotion to V; failure on V does not retroactively change R-window classification but does end the candidate's wave).

### D.18 Candidate-specific mandatory diagnostics beyond the common framework

In addition to the common framework's per-regime expR / MFE distribution / long-short asymmetry / mark-price sensitivity (per Phase 2i §2.5.5, restated in section F below), R3's execution phase must also record:

- **Exit-reason histogram extended.** The `ExitReason` enum is extended with `TAKE_PROFIT` and `TIME_STOP`. Reports must show counts per symbol per fold for: STOP, TAKE_PROFIT, TIME_STOP, END_OF_DATA. The TRAIL and STAGNATION reasons should not appear (R3 has no trailing or stagnation rule); if they do, the report flags an implementation bug.
- **R-multiple histogram of TAKE_PROFIT exits.** The actual realized R-multiple at TAKE_PROFIT fills (which should cluster tightly near +2.0 R minus slippage). If the cluster is materially off-target (e.g., realized R below +1.8 because of slippage / next-bar-open gap), the report flags it.
- **Time-stop bias diagnostic.** The fraction of TIME_STOP exits where MFE was positive at fire (i.e., a winning trade was prematurely closed) vs. negative (a losing trade was bailed out). This is the diagnostic that quantifies the §D.14 "real big winners are clipped" failure mode.

These three diagnostics are mandatory for R3; they are not required for R1a (which does not change exit logic).

---

## E. Side-by-side redesign comparison

| Aspect | R1a (Volatility-percentile setup) | R3 (Fixed-R exit with time stop) |
|---|---|---|
| **Thesis** | Setup-shape (range-based ratio) is the wrong filter; volatility-percentile predicate captures genuine compressions across regimes. | Staged-trailing exit philosophy is structurally inactive; clean fixed-2R + 8-bar time-stop aligns exits with how trades actually behave. |
| **Family** | S (setup-pattern) | X (exit-philosophy) |
| **Targets which Phase 2g funnel rejection** | 58% no-valid-setup (dominant) | Trailing-machine inactive (0/41 BTC trail exits); stagnation dominates intermediate outcomes |
| **Likely effect on trade count** | Moderate change (could increase if the percentile filter is more permissive in vol-rich regimes; could decrease if it's stricter; H-A1 evidence suggests setup shape is *not* the primary frequency driver) | Unchanged (R3 doesn't gate entries; only changes exit logic) |
| **Likely effect on expectancy** | Uncertain — depends on whether R1a's filter actually identifies breakout-prone setups. Could improve or worsen. | Uncertain — depends on the per-trade R distribution. Could improve (clean 2R wins capture systematically) or worsen (real big winners clipped at 2R). |
| **Likely effect on drawdown** | Mostly unchanged (entries unchanged when filter passes; H0's exit logic still owns drawdown shape) | Plausibly different — R3 removes break-even and trailing, so trades that reach +1.5R MFE in H0 and drift back can now drift to the initial stop. Could be worse on per-fold |maxDD| in some regimes; better in others (fewer mid-trade whipsaws). |
| **Likely implementation complexity** | MEDIUM. Adds new setup-predicate dispatch + rolling ATR-percentile cache + new tests + new funnel-attribution logic. ~10 source files modified. | LOW-MEDIUM. Adds new exit-philosophy dispatch + extended ExitReason enum + new tests. ~5–7 source files modified. Smaller surface than R1a. |
| **Likely overfitting risk** | MEDIUM. Two sub-parameters (X=25, N=200) committed; reasonably defensible as research defaults but each value has a defensible sweep range. | LOW-MEDIUM. Two sub-parameters (R_TARGET=2.0, TIME_STOP_BARS=8) committed; both align with existing project conventions (2.0R matches H0 trailing-activation; 8 bars matches H0 stagnation-window count). Less fitting risk than R1a. |
| **Likely validation burden** | Common framework + R1a-specific diagnostics (setup-validity rate per fold; ATR-percentile distribution at entries). 2 candidate-specific diagnostics on top of the 4-item common framework. | Common framework + R3-specific diagnostics (exit-reason histogram with new TAKE_PROFIT/TIME_STOP reasons; R-multiple histogram of TAKE_PROFIT fills; time-stop bias diagnostic). 3 candidate-specific diagnostics on top of the 4-item common framework. Comparable in burden to R1a. |
| **GAP dispositions** | CARRIES 030, 031, 032, 033. Supersedes nothing. | SUPERSEDES 030. CARRIES 031, 032. CARRIES-AND-EXTENDS 033. |
| **Suitability for first execution** | LOWER. R1a is on the most evidence-grounded axis but its rule shape requires more new infrastructure (rolling ATR-percentile cache; new funnel attribution branch; warmup floor recomputation). The two sub-parameters have wider plausible ranges, increasing fitting risk. | HIGHER. R3 is contained to TradeManagement and the ExitReason enum. Sub-parameters are anchored to existing project conventions (2.0R = H0 trailing-activation; 8 bars = H0 stagnation-window). Falsifiable hypothesis is cleaner because §10.3.c (exit-philosophy strict-dominance) applies. |

**First-execution-suitability ranking:** R3 first; R1a second.

The ranking is not a recommendation that R1a be deferred — both candidates can advance simultaneously to a future operator-approved execution-planning phase. The ranking only states that if the operator wants execution evidence faster, R3's smaller surface, lower fitting risk, and cleaner falsifiability make it the more contained first test.

---

## F. Common validation framework (restated)

This restatement preserves the framework defined in Phase 2i §2.5 and Phase 2j Gate 1 plan §9. Any future execution phase that runs R1a or R3 inherits this framework unchanged.

### F.1 H0 as only comparison anchor

**H0 (the locked Phase 2e baseline re-run on R) is the only comparison anchor for any redesign candidate.** All §10.3 / §10.4 evaluation for R1a or R3 is computed vs. H0's R-window numbers, never vs. wave-1 variants.

### F.2 Wave-1 variants as historical evidence only

**Phase 2g wave-1 variants (H-A1, H-B2, H-C1, H-D3) are historical evidence only, not promotion baselines.** Their R-window numbers may be cited diagnostically (as in §B.2 above) but they do not serve as comparison anchors for any redesign §10.3 / §10.4 evaluation. A redesign that improves over H-B2 but worsens over H0 is disqualified.

### F.3 §10.3 / §10.4 / §11.3 / §11.4 / §11.6 discipline preserved

- **§10.3 promotion paths:** §10.3.a (Δexp ≥ +0.10 R AND ΔPF ≥ +0.05); §10.3.b (Δexp ≥ 0 AND trades + ≥ 50% AND |maxDD| not worse > 1.0 pp); §10.3.c (exit-model bake-off strict dominance — applicable to R3).
- **§10.3 disqualification floor:** worse expR, worse PF, |maxDD| > 1.5× baseline, broken funnel invariant, failed conformity check.
- **§10.4 hard reject:** rising trades AND (expR < −0.50 OR PF < 0.30).
- **§11.3 no-peeking + top-1–2 promotion to V.**
- **§11.4 ETH-as-comparison:** BTC must clear; ETH must not catastrophically fail.
- **§11.6 cost-sensitivity:** any §10.3 pass on MEDIUM slippage must also pass on LOW and HIGH; HIGH-slippage inversion demotes to "fragile".

All thresholds applied unchanged. **Per Phase 2f §11.3.5 the thresholds are pre-committed and cannot be tightened or loosened after seeing results.**

### F.4 R/V split unchanged

- **R window:** 2022-01-01 → 2025-01-01 (36 months). All R1a / R3 ranking happens here.
- **V window:** 2025-01-01 → 2026-04-01 (15 months). Reserved for top-1–2 promoted candidates only. Untouched until promotion.

### F.5 GAP-036 fold convention unchanged

5 rolling folds, fold 1 partial-train (6m), folds 2–5 with full 12m train, all tests inside R. Supplemental 6-half-year appendix per Phase 2g §3.A retained for descriptive coverage.

### F.6 Required diagnostics for R1a or R3 execution (common framework + candidate-specific)

**Common framework (per Phase 2i §2.5.5; mandatory for both R1a and R3):**

- **Per-regime expR.** Classify each trade by realized 1h volatility regime (low / medium / high based on trailing-percentile classification of 1h ATR(20) at entry).
- **MFE distribution.** Histogram of MFE in R-multiples.
- **Per-direction long/short asymmetry.** Separate expR / PF / win rate for long-only and short-only subsets.
- **GAP-032 mark-price stop-trigger sensitivity.** Run the candidate with `stop_trigger_source=TRADE_PRICE` and report comparison vs. MARK_PRICE.

**R1a candidate-specific (per §C.16):**

- Setup-validity rate per fold (R1a vs. H0).
- ATR-percentile distribution at trade entries.

**R3 candidate-specific (per §D.18):**

- Exit-reason histogram extended (STOP / TAKE_PROFIT / TIME_STOP / END_OF_DATA per fold per symbol).
- R-multiple histogram of TAKE_PROFIT exits.
- Time-stop bias diagnostic (sign of MFE at TIME_STOP fire).

### F.7 Candidate-specific success criteria pre-declared before execution

R1a and R3 each have their falsifiable hypotheses pre-declared in §C.15 and §D.17. These hypotheses are the **only** success criteria that apply to their execution. The execution phase cannot add new success criteria after seeing results.

---

## G. Execution-readiness assessment

Per the operator's required structure, each candidate is rated as ready for execution planning, needs one more docs clarification, or should be dropped.

### G.1 R1a — Volatility-percentile setup

**Rating: READY for execution planning.**

Reasoning: the spec is complete (rule shape, inputs, timeframes, predicate, replaced-vs-kept, sub-parameter values committed singularly, falsifiable hypothesis pre-declared, GAPs disposed, diagnostics specified). The committed sub-parameter values (X=25, N=200) are research defaults with literature-backed justification (§C.6) and are pinned for execution. No hidden degrees of freedom remain. The execution phase's Gate 1 plan can adopt this spec directly without further docs work.

**Caveats to flag for the operator before execution:**

- The implementation surface is moderate (~10 source files modified, new rolling ATR-percentile cache, new funnel-attribution branch, recomputed warmup floor). If the operator wants to minimize implementation risk on the first execution, R3 (with its smaller surface) is the easier first test.
- Two sub-parameters with plausible alternative values (e.g., X = 20 or 30; N = 100 or 500) means a future operator-approved Phase 2k could legitimately propose a separate R1a' variant with different committed values. That is a separate spec, not a sweep.

### G.2 R3 — Fixed-R exit with time stop

**Rating: READY for execution planning.**

Reasoning: the spec is complete (exit philosophy, take-profit rule, time-stop rule, interaction with initial stop, removed staged management, sub-parameter values committed singularly, falsifiable hypothesis pre-declared with §10.3.c noted, GAPs disposed including SUPERSEDED of GAP-030 and CARRIED-AND-EXTENDED of GAP-033, diagnostics specified). The committed sub-parameter values (R_TARGET=2.0, TIME_STOP_BARS=8) are anchored to existing project conventions (§D.6) and are pinned for execution. No hidden degrees of freedom remain.

**Caveats to flag for the operator before execution:**

- R3's GAP-033 disposition extends the original GAP question: R3 explicitly chooses the unconditional time-stop interpretation (§D.4). Any future redesign that wants the conditional interpretation (with an MFE gate, like H0's stagnation rule) would need a separate spec.
- The new exit reasons (TAKE_PROFIT, TIME_STOP) are reporting infrastructure changes; the execution phase must extend the trade-record schema, the monthly/yearly aggregator, and the report schema. This is a small but non-zero schema change.

### G.3 Joint readiness

Both R1a and R3 are READY for a future operator-approved Phase 2k execution-planning phase. Phase 2k's Gate 1 plan would adopt the specs in this memo as the binding rule definitions, set up the variant-comparison report contract, and stage the eventual execution against H0 on R per the §F validation framework.

---

## H. Recommendation (provisional; subject to operator/ChatGPT review)

This recommendation is **provisional and evidence-based, not definitive**. It is a judgement about which carry-forward candidate(s) advance to a future operator-approved execution-planning phase, given the spec evidence in sections C–G. It is explicitly **not** any of the following:

- It is **not** a claim that R1a or R3 will produce a positive result. Each is a research bet with a falsifiable hypothesis.
- It is **not** a claim that one candidate is permanently more valuable than the other. The execution-suitability ranking in section E reflects implementation-risk and falsifiability surface, not predicted edge.
- It is **not** a recommendation for live deployment, paper/shadow readiness, or any capital exposure.

With those caveats explicit:

**Primary (provisional): Both R1a and R3 advance to a future operator-approved Phase 2k execution-planning phase, with R3 prioritized for first execution.**

Reasoning:

1. **Both specs are complete (READY per §G).** Each has a single committed value per sub-parameter, a pre-declared falsifiable hypothesis, a GAP disposition, and a candidate-specific diagnostic list. Per §G, neither needs additional docs work before Phase 2k Gate 1 planning.
2. **R3 prioritized first because:** smaller implementation surface, lower fitting risk, sub-parameters anchored to existing project conventions, exit-philosophy structural change is the cleanest topology change in the v1 spec, falsifiability is sharper because §10.3.c (strict-dominance for exit-model changes) applies.
3. **R1a follows immediately after:** R3's result (whether positive or negative) is an informative input for whether R1a should run with H0's exit logic (the spec as written) or whether the operator wants to first commit to a different exit philosophy and then test R1a's setup change against it. This is a sequencing preference, not a deferral.
4. **No third candidate** (R1b regime-bias, R2 pullback-entry) is added — the Phase 2i ≤ 2 carry-forward discipline is preserved.
5. **Phase 4 stays deferred** per existing operator policy. This memo does not propose advancing it.

The recommendation is provisional. Operator/ChatGPT may choose:

- both advance (recommended); or
- only R1a advance (e.g., if the operator judges setup-redesign more important than exit-redesign); or
- only R3 advance (e.g., if the operator judges exit-redesign more contained and wants single-candidate evidence first); or
- neither advance without another docs phase (e.g., if the operator finds the specs underdetermined despite the §G assessment).

---

## I. What would change this recommendation

The recommendation is provisional. The following kinds of evidence or reasoning would justify switching:

### I.1 Switch to "only R1a advances"

- Operator preference for setup-redesign evidence (the dominant 58% funnel rejection) over exit-redesign evidence.
- A reasoned argument that exit-philosophy results (R3) without first knowing whether the setup is producing the right candidate set are uninterpretable.
- Recognition that R3's overlap with the H-D6 fallback reduces R3's information value relative to R1a's untested-axis novelty.

### I.2 Switch to "only R3 advances"

- Operator preference for execution-evidence on the smaller surface first; defer R1a until R3's result is known.
- A reasoned argument that R3's strict-dominance §10.3.c falsifiability is a faster path to clean evidence than R1a's §10.3.a/b paths.
- Recognition that R1a's two-sub-parameter surface is too wide to commit to without more evidence about the right percentile/lookback regime.

### I.3 Switch to "neither advances without more docs"

- Discovery during operator review that R1a's or R3's spec has a hidden degree of freedom that this memo missed (e.g., the percentile rank tie-breaking convention has multiple defensible options that materially change the result; or R3's "time-stop fires on the same bar as a stop hit" priority isn't fully resolved).
- Discovery of a documentation inconsistency in prior phase records (Phase 2e/2f/2g/2h/2i) that requires a docs-only correction phase before any execution work.
- Operator decision to pause strategy work and prioritize a different operational concern.

### I.4 Switch to fallback Wave 2 (H-D6) instead of Phase 2k

- Operator preference for the parameter-search axis that wave 1 left untouched (H-D6 exit-model bake-off) before committing to either structural redesign.
- Phase 2i §3.4 already articulated the conditions under which fallback Wave 2 wins; those conditions still apply.

### I.5 Switch to Phase 4

- Explicit operator policy change accepting that operational infrastructure should be built without strategy-edge confirmation. Current policy is against this; this memo does not propose changing it.

---

## J. Explicit non-proposal list

Phase 2j explicitly does **not** propose any of the following:

- **No execution of R1a or R3.** This memo writes specs only. Execution against R/V data is a separate operator-approved phase (Phase 2k or later).
- **No backtest runs.** No H0 re-run, no R1a run, no R3 run. The Phase 2g v002 dataset and run artifacts are preserved unchanged.
- **No threshold changes.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds and §11.3.5 pre-committed-thresholds discipline are unchanged. R1a and R3 inherit them exactly.
- **No revival of wave-1 variants.** H-A1, H-B2, H-C1, H-D3 remain disqualified per Phase 2g. They are diagnostic citations only.
- **No fallback H-D6 Wave 2 start.** Phase 2h §3.3 / Phase 2i §3.4 fallback path remains a fallback.
- **No Phase 4 start.** Runtime / state / persistence work remains deferred per existing operator policy.
- **No code changes.** No new variant_config fields, no new strategy module, no new test, no new script. The implementation impacts described in §C.10 and §D.12 are descriptive only — they would happen in a future approved phase, not in Phase 2j.
- **No new dependencies.** `pyproject.toml` and `uv.lock` unchanged.
- **No data downloads.** v002 manifests and datasets unchanged.
- **No Binance API calls** (authenticated or public).
- **No MCP / Graphify / `.mcp.json`.**
- **No `technical-debt-register.md` edits.**
- **No expansion of the carry-forward set beyond R1a + R3.** The Phase 2i ≤ 2 carry-forward discipline is preserved.
- **No introduction of a third candidate** (R1b, R2, or any new family) without operator escalation.
- **No comparison of R1a or R3 to wave-1 variants as promotion baselines.** H0 only.
- **No disguised parameter sweeps.** Each sub-parameter (R1a's X and N; R3's R_TARGET and TIME_STOP_BARS) is committed to a single value. No "we'll test 20 / 25 / 30" framing in this memo or in a future Phase 2k Gate 1 plan that adopts this memo.
- **No live deployment, paper/shadow readiness, or capital exposure proposal.**
- **No re-derivation of the wave-1 verdict.** REJECT ALL stands.
- **No re-framing of the Phase 2h provisional recommendation or Phase 2i recommendation.** Both are inputs to Phase 2j, not targets for revision.

---

**End of memo.** Phase 2j is decision/planning only. Section H's recommendation hands the next-boundary decision (advance both / R1a only / R3 only / neither without more docs / fallback Wave 2 / Phase 4) to the operator with the conditions that would change the choice spelled out in section I.
