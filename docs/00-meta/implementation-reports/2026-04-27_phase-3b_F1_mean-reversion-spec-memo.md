# Phase 3b — F1 Mean-Reversion-After-Overextension Spec Memo

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks (H0 anchor for V1 breakout family; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2j §C.6 / §D.6 / §11.3.5 single-sub-parameter commitment discipline; Phase 2p §C.1 (R3 V1-breakout baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved unchanged); Phase 3a new-strategy-family discovery memo §4.1 / §5 / §6 (F1 ranked rank-1 near-term candidate); `docs/03-strategy-research/v1-breakout-strategy-spec.md` (canonical V1 conventions: 15m signal timeframe, 1h higher-timeframe bias, ATR(20) on 15m as canonical volatility unit, 8-bar setup window, [0.60, 1.80] × ATR(20) stop-distance band, 0.10 × ATR(20) buffer convention, completed-bar-only discipline, market entry at next-bar-open after signal close); `docs/05-backtesting-validation/backtesting-principles.md` (no leakage; chronological integrity; cost realism mandatory); `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` (Gate 1 data integrity; Gate 5 robustness; Gate 6 exit-model comparison); `docs/04-data/data-requirements.md` (v002 dataset coverage); `docs/04-data/dataset-versioning.md` (versioned feature dataset requirements); `docs/05-backtesting-validation/cost-modeling.md` (all validation net of cost); `src/prometheus/research/backtest/config.py:55-59` (canonical slippage tiers LOW=1.0 / MED=3.0 / HIGH=8.0 bps per side; `taker_fee_rate=0.0005`; `BacktestAdapter.FAKE` only in Phase 3).

**Phase:** 3b — Docs-only **specification memo** for F1 (mean-reversion-after-overextension), the Phase 3a rank-1 near-term family candidate. Phase 2j-style: pre-commit one rule per axis with non-fitting rationale; identify falsifiable mechanism predictions; enumerate failure modes; specify mandatory diagnostics; address overfitting risk; produce GO / NO-GO recommendation for any potential downstream Phase 3c execution-planning phase.

**Branch:** `phase-3b/f1-mean-reversion-spec`. **Memo date:** 2026-04-27 UTC.

**Status:** Spec drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / credentials / `data/` work.** R3 remains V1 baseline-of-record. H0 remains V1 framework anchor. R1a / R1b-narrow / R2 remain retained research evidence. Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3b is deciding

Phase 3b is **specification-only**, not execution and not parameter search. It is the natural successor to the Phase 3a discovery memo, which ranked F1 (mean-reversion-after-overextension) as the rank-1 near-term family candidate among eight surveyed non-breakout families. Phase 3a's recommendation was: **"Authorize Phase 3b — F1 family spec-writing memo."** The operator authorized that path; this memo is the authorized output.

What Phase 3b is asking:

> Given that the V1 breakout-continuation family has likely reached its useful ceiling (Phase 2x), the framework cost-policy is preserved (Phase 2y), and F1 has been ranked as the strongest near-term family candidate (Phase 3a), **can a clean, single-rule, non-fit, falsifiable F1 specification be written, and does that specification justify a downstream Phase 3c execution-planning phase?**

What Phase 3b is **not** asking:

- Not asking whether to **execute** F1. Phase 3b produces a memo; execution requires a separately-authorized Phase 3c execution-planning phase plus a Phase 3d execution phase.
- Not asking which thresholds to choose. The brief's §4 binds: one conceptual value/rule per axis, anchored to existing project conventions where possible; no ranges, no options, no variant lists.
- Not asking to inspect any Phase 3a / Phase 2 results to choose F1's parameters. Phase 2j §C.6 / §11.3.5 binding rule applies: parameters are **pre-committed** before any execution.
- Not asking whether to revise any threshold or lift any §1.7.3 lock.
- Not asking to begin paper/shadow, Phase 4, live-readiness, or deployment work.

The output of Phase 3b is a single specification memo with one committed value/rule per axis, a falsifiable mechanism-prediction set, a mandatory-diagnostics checklist for any future execution, and a GO / NO-GO recommendation for downstream Phase 3c planning. Phase 3b does **not** authorize any execution.

---

## 2. F1 market hypothesis

### 2.1 Why overextension may revert

In a market dominated by short-horizon noise plus longer-horizon structural drift, when the short-horizon component produces a one-sided cumulative move that exceeds the local volatility unit, three forces tend to oppose continuation:

1. **Inventory pressure.** Short-horizon liquidity-taking that produces overextension consumes available passive liquidity at one side of the book; counter-flow rebuilds passive depth and tilts subsequent fills against the overextension direction.
2. **Profit-taking by directional participants.** Participants who entered earlier in the overextension move take profits, increasing counter-flow.
3. **Volatility mean-reversion.** Realized volatility is mean-reverting at short horizons; an overextended bar's high realized vol reduces the conditional probability of further same-direction expansion at the next horizon.

The hypothesis is **falsifiable**: if these forces are weak relative to short-horizon directional drift, F1 mean-reversion entries will be stopped out at a higher rate than they hit the mean target, and the strategy will produce negative aggregate net-of-cost expectancy. Phase 3c execution would test exactly this.

This hypothesis is **mechanism-grounded**, not pattern-fitted. The same forces are referenced in `docs/03-strategy-research/v1-breakout-strategy-spec.md` "Failure Modes" §1 (chop with repeated false breaks) — the V1 breakout family expects to lose under exactly the conditions F1 expects to profit.

### 2.2 Why this is genuinely non-breakout

The clean family-shift test is whether F1 reduces to V1 breakout under any parameter mapping. It does not, on three independent grounds:

1. **Setup predicate is the structural inverse.** V1's setup-validity predicate is a compression condition (`setup_range_width ≤ 1.75 × ATR(20)` AND `|close[-1] - open[-8]| ≤ 0.35 × setup_range_width`). F1's overextension predicate, specified in §4.1 below, is a directional-displacement condition over the same 8-bar window using the same ATR(20) anchor — but inverted. V1 fires when bars stay within a tight range; F1 fires when bars produce net directional drift exceeding the same range cap. The two predicates are structurally non-overlapping: a compressed window (V1 setup-eligible) cannot simultaneously have cumulative drift exceeding the range cap (F1 setup-eligible).
2. **Direction relative to displacement is opposite.** V1 longs after upward breakout; F1 longs after downward overextension. V1 shorts after downward breakout; F1 shorts after upward overextension. Same market, opposite directional bet at the trigger moment.
3. **Trade thesis is opposite.** V1's exit philosophy (R3) is fixed-R take-profit + 8-bar time-stop; the +2.0 R take-profit anchors on the breakout direction continuing. F1's exit philosophy (§4.5 below) is mean-reference target; the target anchors on reversion against the overextension direction. The trade lives or dies on opposite hypotheses.

There is no parameter mapping that makes F1 reduce to V1.

### 2.3 What V1 breakout failure mode F1 targets

V1 breakout's documented failure mode #1 is **chop with repeated false breaks** (`v1-breakout-strategy-spec.md` §"Failure Modes"). This is the dominant V1 loss pattern: in sideways markets, the breakout setup predicate fires repeatedly on shallow ranges, the trigger fires on small directional bars, and the trades get stopped out as price reverts.

F1 is the structural complement: when V1 fails (sideways markets), F1 thrives (sideways markets are exactly where mean-reversion-after-overextension should produce edge). The two families are not redundant; they are structurally complementary, addressing opposite regimes.

The Phase 2 evidence supports this framing operationally:

- **F4 2024H1 was the worst per-fold cell across the entire V1 breakout family arc** (per Phase 2g / 2h / 2l / 2m / 2s / 2w). H0 BTC F4 = −1.025 R; R3 BTC F4 = −0.870 R; R3 ETH F4 = −0.836 R. R3 reduced damage but did not solve the regime incompatibility. The 2024H1 regime is where mean-reversion-after-overextension would plausibly produce its strongest edge.
- **Phase 2x §4.6 BTC/ETH asymmetry diagnosis** documented that V1's edge is more demonstrable on ETH (where breakouts continue more reliably) and weaker on BTC (where chop / mean-reversion behavior dominates). F1 inverts this asymmetry plausibly: BTC's tighter spreads + chop tendency favors mean-reversion.

### 2.4 Why BTCUSDT-primary compatibility is plausible

Three structural reasons F1 should align with §1.7.3 BTCUSDT-primary live scope:

1. **Spread profile.** BTCUSDT-perp has tighter realized spreads than ETHUSDT-perp (Phase 2y §5.1.8). Mean-reversion's tight stop-and-target geometry is more sensitive to spread width than V1's structural-stop-and-trail geometry. BTC's narrower spread is structurally favorable for F1.
2. **Depth profile.** BTCUSDT-perp has deeper top-of-book + first-5-levels depth than ETHUSDT-perp. Mean-reversion fills face less impact slippage at typical Prometheus-scale notionals ($4K–$20K typical, up to $200K cap).
3. **Regime mix.** BTCUSDT-perp produces longer chop/range periods than ETHUSDT-perp does (ETH tends to produce sharper trending moves). F1's hypothesized edge is regime-specific to chop; BTC's regime mix is more F1-favorable.

These are **plausibility arguments**, not edge claims. The empirical question is whether F1 produces clean BTC PROMOTE under §10.3-style discipline; Phase 3c execution would test this.

---

## 3. Exact strategy-family definition

### 3.1 Signal family name

```
F1 — Mean-Reversion-After-Overextension
```

Symbol-stable name for code identifiers, dataset versions, and report references: `mean_reversion_overextension`. Distinguishable from V1 breakout family (`v1_breakout`). New strategy module would live at `src/prometheus/strategy/v2_mean_reversion/` (or similar; exact path is a Phase 3c implementation decision).

### 3.2 Allowed directionality

**Long AND short.** F1 is bidirectional by symmetric construction:

- **Long entry** after **downward** overextension (cumulative negative displacement exceeds threshold; mean reference is above entry).
- **Short entry** after **upward** overextension (cumulative positive displacement exceeds threshold; mean reference is below entry).

No directional asymmetry is built into the spec; F1 fires symmetrically on both sides.

Rationale for not rejecting one direction: the mean-reversion mechanism (§2.1) is direction-symmetric. Rejecting one direction would be results-fitting (the kind Phase 2j §11.3.5 forbids).

Operational constraints inherited from §1.7.3 / `v1-breakout-strategy-spec.md`:

- **One position maximum at any time.** No pyramiding. No reversal while positioned. Symmetric to V1.
- **One symbol live.** BTCUSDT primary; ETHUSDT research/comparison only. Per §1.7.3.
- **One-way mode + isolated margin.** Per §1.7.3.

### 3.3 Timeframe basis

- **Signal timeframe:** 15m. Same as V1 breakout per `v1-breakout-strategy-spec.md`.
- **No higher-timeframe bias filter in F1's committed spec.** Per §4.8 (regime filter, if any), F1 commits to no explicit regime filter; per-regime decomposition is a §11 diagnostic, not a §4 entry gate.

Why 15m: matches V1 breakout's signal timeframe; uses the same canonical bar identity (`symbol + interval=15m + open_time`); leverages the same v002 dataset stack; allows direct cross-family diagnostic comparison without timeframe-conversion confounds.

### 3.4 Which completed bars are used

**Completed 15m bars only** for all signal evaluation, mean-reference computation, stop computation, target computation, time-stop computation, and exit decisions. Strict per `data-requirements.md` §"Core Data Principles" #1.

For overextension predicate evaluation at decision-time bar B (where B is the most recently completed 15m bar):

- The 8 completed 15m bars consumed are bars at indices `[B-7, B-6, B-5, B-4, B-3, B-2, B-1, B]`.
- ATR(20) is computed on the trailing 20 completed 15m bars: `[B-19, ..., B]`.
- The decision is made at bar B's close; entry fills at next-bar-open, i.e., at bar `B+1`'s open price.

### 3.5 No intrabar lookahead

All predicates use **completed-bar values only**:

- Cumulative displacement uses completed-bar closes.
- ATR(20) uses completed-bar high/low/close.
- Mean reference (§4.2) uses completed-bar closes.
- Entry confirmation (§4.3) is at completed-bar close (no intrabar trigger).
- Protective stop (§4.4) is structural, computed at signal time from completed-bar values; not moved intra-trade.
- Target check (§4.5) uses completed-bar close-vs-mean comparison; fill at next-bar-open after target-cross.
- Time stop (§4.6) counts completed bars from entry-fill bar (`B+1`).

### 3.6 No future-data leakage

For any decision at bar B's close:

- All inputs are from bars at index ≤ B.
- All evaluations use `close_time(bar_B) ≤ decision_time` per `timestamp-policy.md`.
- No look-ahead through 1h-bias resampling (F1 does not use 1h bias per §3.3).
- No look-ahead through SMA(8) (uses only bars `[B-7, ..., B]`).
- No look-ahead through ATR(20) (uses only bars `[B-19, ..., B]`).
- No look-ahead through stop computation (uses `lowest_low([B-7, ..., B])` for longs, `highest_high([B-7, ..., B])` for shorts).
- No look-ahead through target computation (frozen SMA(8) value at bar B's close).

This is enforced by the engine's per-bar evaluation discipline already established for V1 breakout (Phase 2v §3.2.2 bit-for-bit reproduction).

---

## 4. Single committed rule per axis

Per the operator brief: "Commit EXACTLY ONE conceptual value/rule for each required axis. Must not use multiple options or ranges. Must not be chosen because it would likely improve results."

Each rule below pre-commits a singular value with non-fitting rationale per §5. Phase 3c execution must use these exact rules without modification.

### 4.1 Overextension definition

**Committed rule:** `cumulative_displacement_8bar(B) = close(B) − close(B−8)`. F1 fires an overextension event at bar B's close iff:

```
| cumulative_displacement_8bar(B) |  >  1.75 × ATR(20)(B)
```

with the **direction** of the overextension equal to `sign(cumulative_displacement_8bar(B))`. A positive sign is upward overextension (triggers a candidate **short** entry); a negative sign is downward overextension (triggers a candidate **long** entry).

### 4.2 Mean / reference level

**Committed rule:** `mean_reference(B) = SMA(8)(B) = (1/8) × Σ_{i=0..7} close(B−i)`. The mean reference is the simple moving average of close prices over the same 8 completed 15m bars used by the overextension predicate.

### 4.3 Entry confirmation rule

**Committed rule:** **Market entry at the open of the bar immediately following the overextension-detection bar B.** Entry bar is `B+1`; entry price is `open(B+1)`. **No confirmation candle required.**

### 4.4 Protective stop definition

**Committed rule (long entries):** `initial_stop = lowest_low([B−7, ..., B]) − 0.10 × ATR(20)(B)`.

**Committed rule (short entries):** `initial_stop = highest_high([B−7, ..., B]) + 0.10 × ATR(20)(B)`.

The protective exchange-side stop is `STOP_MARKET` with `closePosition=true`, `workingType=MARK_PRICE`, `priceProtect=TRUE` — identical to the v1 protective-stop spec (`v1-breakout-strategy-spec.md` §"Protective Exchange-Side Stop"). **Stop is never moved intra-trade** (no trailing, no break-even shift, no widening, no narrowing).

### 4.5 Profit target / exit definition

**Committed rule:** Profit target = `mean_reference(B) = SMA(8)(B)`, frozen at signal-time bar B's close. Exit triggers when, on a completed 15m bar `t > B`:

- For longs: `close(t) ≥ frozen_mean_reference`.
- For shorts: `close(t) ≤ frozen_mean_reference`.

Exit fill at `open(t+1)`.

### 4.6 Time stop / max hold rule

**Committed rule:** **Unconditional time-stop at 8 completed 15m bars from entry-fill.** If at the close of bar `B+1+8 = B+9` the trade has not exited via target (§4.5) or stop (§4.4), exit at market at `open(B+10)`.

### 4.7 Cooldown / re-entry rule

**Committed rule:** After exit (any reason — target, stop, or time-stop), no new same-direction F1 entry on the same symbol may be initiated until the cumulative displacement predicate (§4.1) re-forms in the same direction **after** at least one completed 15m bar where `| cumulative_displacement_8bar(t) | ≤ 1.75 × ATR(20)(t)` (i.e., the overextension state has unwound).

In plain English: F1 cannot re-enter the same overextension. A completely fresh overextension event must form after the prior trade exits.

### 4.8 Regime filter (if any)

**Committed rule:** **No explicit regime filter in F1's spec.** F1 fires whenever the overextension predicate (§4.1) and the stop-distance admissibility rule (§4.9) are simultaneously satisfied, regardless of the prevailing 1h trend bias or volatility regime.

### 4.9 Stop-distance admissibility rule

**Committed rule:** Reject the candidate entry at signal-time bar B if the computed stop distance falls outside the band:

```
stop_distance ∈ [0.60, 1.80] × ATR(20)(B)
```

where `stop_distance = |entry_price_estimate(open(B+1) ≈ close(B)) − initial_stop|`. (Phase 3c's executed run uses the actual `open(B+1)` once available; per Phase 2u §E.3 / Phase 2w P.14 convention, the de-slipped raw next-bar-open is the reference.)

If the stop-distance falls outside the band, the F1 entry is rejected; no order is placed; the cooldown rule (§4.7) does not apply because no trade was opened.

---

## 5. Non-fitting rationale for each committed rule

Per the operator brief: "Must be anchored to existing project conventions where possible. Must not be chosen because it would likely improve results."

### 5.1 Rationale for §4.1 overextension definition

- **Window length N=8.** Same as V1 breakout's setup window length (`v1-breakout-strategy-spec.md` §"Setup window"). Anchored to existing project convention; not chosen because 8 bars produces a particular trade frequency.
- **Threshold 1.75 × ATR(20).** Same numeric as V1 breakout's `setup_range_width ≤ 1.75 × ATR(20)` cap. Used here as a **structural inversion**: F1 fires when 8-bar cumulative displacement exceeds the same threshold V1 uses to bound the 8-bar range width. This anchors F1's threshold to V1's threshold mechanically, not to a fitted F1-specific value.
- **Cumulative-displacement metric.** `close(B) − close(B−8)` is the simplest unbiased summary of net 8-bar drift. Anchored to V1's existing drift-metric convention (`abs(close[-1] - open[-8])` per V1 setup, but using `close − close` instead of `close − open` to match the SMA(8) reference's close-based construction).

### 5.2 Rationale for §4.2 mean reference

- **SMA over close, window 8.** Window matches §4.1 (same 8 bars). Simple-moving-average is the simplest unbiased mean estimator on the relevant window; using EMA or a different window would require an additional choice (decay coefficient or window-length tuning) that would be results-driven.
- **Why not the midpoint of the 8-bar high/low.** Midpoint over high/low is more sensitive to single-bar wicks (high-impact spike bars distort the mean); SMA over close is the closing-price unbiased mean which is the natural reversion target.
- **Why frozen at signal time.** A rolling target (recomputed at each bar) introduces moving-target ambiguity and creates an additional implicit parameter (which window length is used for the rolling target). Freezing at signal time eliminates that degree of freedom.

### 5.3 Rationale for §4.3 entry confirmation

- **Market entry at next-bar-open after B.** Identical to V1 breakout's committed fill model (`v1-breakout-strategy-spec.md` §"Entry Execution Method"). Anchored to the same engine fill machinery already validated through Phase 2g / 2l / 2m / 2s / 2w.
- **No confirmation candle required.** Adding a confirmation requirement (e.g., "wait for first counter-direction close") would introduce an additional axis (definition of confirmation) that would be results-driven. The R2 evidence (Phase 2w §11.6) showed pullback-entry geometries are slippage-fragile; F1's market-on-next-bar-open avoids that geometry by construction.

### 5.4 Rationale for §4.4 protective stop

- **Structural stop = lowest-low / highest-high of the 8-bar overextension window + 0.10 × ATR(20) buffer.** Identical buffer convention to V1 breakout's `min(setup_low, breakout_bar_low) - 0.10 × ATR(20)` structural stop (`v1-breakout-strategy-spec.md` §"Initial Stop Logic"). Anchored to V1's existing structural-stop convention; the only difference is which 8-bar window the extreme is taken from (V1 uses the setup window; F1 uses the overextension window — both are 8 bars, both use `min(low)` / `max(high)`).
- **Why `closePosition=true / workingType=MARK_PRICE / priceProtect=TRUE`.** Identical to V1's protective-stop spec and to the live `STOP_MARKET` workingType policy under §1.7.3.
- **Stop never moved intra-trade.** Inherited from R3's "protective stop never moved" discipline (Phase 2j §D.10). Used here as a "generic risk-control reference" per the operator brief §6, not as full R3 exit-machinery inheritance.

### 5.5 Rationale for §4.5 profit target

- **Target = SMA(8) at signal time.** This IS the F1 thesis: reversion to the 8-bar mean. The target is mechanism-defined, not a fitted R-multiple. Using a fixed R-multiple target (e.g., +2.0 R like R3) would be an exit-machinery import from V1, not the F1 thesis.
- **Why exit on completed-bar close-vs-mean.** Completed-bar close is the strict-leakage-free definition (`data-requirements.md` §"Core Data Principles" #1).
- **Why fill at `open(t+1)`.** Same fill model as V1's exit machinery (next-bar-open after exit-trigger close). Anchored to engine convention.

### 5.6 Rationale for §4.6 time stop

- **8-bar time-stop, unconditional.** Anchored directly to R3's locked sub-parameter `exit_time_stop_bars = 8` (Phase 2p §C.1). R3's 8-bar value was itself chosen to match V1's Stage 7 stagnation horizon (`v1-breakout-strategy-spec.md` §"Stage 7"); Phase 2j §D.6 anchored R3 sub-parameters to existing H0 stage-trigger thresholds. F1 inherits the same 8-bar horizon as a generic risk-control reference (per the operator brief §6 wording about R3 references), not as R3's full `FIXED_R_TIME_STOP` topology.
- **Why unconditional.** Conditional time-stop (e.g., "8 bars without +0.5 R MFE") would introduce an additional MFE-threshold parameter that would be results-driven. Unconditional eliminates that degree of freedom.

### 5.7 Rationale for §4.7 cooldown / re-entry

- **No same-direction re-entry until overextension state unwinds.** Mirrors V1 breakout's re-entry rule (`v1-breakout-strategy-spec.md` §"Re-Entry Rules": "no same-direction re-entry until a new valid setup window has formed after the previous exit"). F1's analog: no same-direction re-entry until a fresh overextension event forms after the prior trade exits.
- **Why a clean unwind requirement.** Without it, F1 could chase the same overextended move repeatedly during a single regime, producing high per-trade correlation. The unwind-then-reform requirement provides natural decorrelation. Anchored to V1's same-direction-cooldown convention; not chosen for results.

### 5.8 Rationale for §4.8 regime filter

- **No explicit regime filter.** Three reasons:
  1. **Mechanism universality claim.** F1's hypothesis (§2.1) is that the inventory / profit-taking / vol-MR forces apply to all regimes; an explicit regime filter would presume the answer to the empirical question.
  2. **Non-fitting discipline.** Adding a "neutral-bias-only" filter (long allowed only when 1h bias is not strongly down; short only when not strongly up) would be selected to avoid the §10 expected failure mode #1 (trend-continuation destroys mean-reversion entries) — a results-driven choice forbidden by the brief.
  3. **Per-regime diagnostic adequacy.** The §11 mandatory-diagnostics list includes per-regime decomposition (1h-volatility tercile classification per Phase 2l/2m/2s/2w convention). Phase 3c execution will reveal empirically whether F1 fails in trending regimes; if so, that becomes Phase 3c-or-later evidence for a hypothetical F1-prime regime-conditional spec — not a Phase 3b pre-fit.

### 5.9 Rationale for §4.9 stop-distance admissibility

- **Same band [0.60, 1.80] × ATR(20) as V1 breakout.** Anchored directly to V1's existing stop-distance filter (`v1-breakout-strategy-spec.md` §"Stop-distance filter"). Reusing the same band uses an established research convention; choosing a different band would require a fitted F1-specific value.
- **Why band rejection rather than band re-sizing.** Re-sizing (e.g., scaling position to fit a different stop) would introduce a sizing-vs-stop interaction not present in V1. Band rejection is mechanically identical to V1's behavior.

---

## 6. Distinguishing F1 from V1 breakout

Per the operator brief: F1 must not be V1 breakout in disguise. Six distinguishing properties:

### 6.1 No breakout trigger

V1 fires on `breakout_bar_close > setup_high + 0.10 × ATR(20)` (long) or `< setup_low - 0.10 × ATR(20)` (short) — a strict crossing of a structural level. F1 fires on `| cumulative_displacement_8bar | > 1.75 × ATR(20)` — a magnitude-of-drift condition that does not require any structural-level crossing. Predicate space is structurally non-overlapping (§2.2).

### 6.2 No breakout buffer

V1 uses a 0.10 × ATR(20) buffer beyond the setup high/low to require breakout strength. F1 has no analogous buffer because it has no structural level to cross — the predicate is on cumulative displacement, not on level-crossing.

(Note: F1's protective stop §4.4 does use a 0.10 × ATR(20) buffer beyond the 8-bar extreme, mirroring V1's structural-stop buffer convention. This is a stop-buffer, not a trigger-buffer; the two play different roles.)

### 6.3 No range-break continuation thesis

V1's thesis is **continuation**: directional moves continue when a higher-timeframe trend is established and short-term price compresses then breaks out. F1's thesis is **reversion**: cumulative directional moves over a short horizon revert toward the local mean (§2.1). The two theses are logically opposite.

### 6.4 No R3 exit inheritance (only generic risk-control references)

R3's exit machinery is `exit_kind=FIXED_R_TIME_STOP` with `exit_r_target=2.0` and `exit_time_stop_bars=8` — a fixed-R take-profit at +2.0 R **plus** an unconditional 8-bar time-stop. F1 inherits **only** the 8-bar unconditional time-stop (§4.6) as a generic risk-control reference; it does **not** inherit the fixed-R take-profit. F1's profit target is the SMA(8) mean reference (§4.5), which is the mean-reversion thesis, not R3's continuation-anchored R-target.

This is explicit per the operator brief §6: "no R3 exit inheritance unless explicitly justified as a generic risk-control reference." The 8-bar time-stop is justified as a generic risk-control reference because (a) it matches V1's Stage 7 stagnation horizon — i.e., it was an existing project convention before R3 — and (b) without a time-stop, F1 trades that neither hit target nor stop could remain open indefinitely under non-reverting conditions, which is operationally unsafe.

### 6.5 No higher-timeframe bias filter

V1 uses 1h EMA(50)/EMA(200) trend bias as a hard gate (`v1-breakout-strategy-spec.md` §"Higher-Timeframe Trend Bias"). F1 has no 1h bias filter (§4.8). F1 fires symmetrically on both directions regardless of 1h trend state.

### 6.6 No hidden V1 reuse

The F1 spec does not import V1's setup-validity predicate, V1's breakout trigger, V1's 1h bias filter, or V1's R-multiple-anchored exit machinery. The only shared elements are:

- **The 15m signal timeframe** — same as V1 by deliberate engine-and-cost-comparability choice (§3.3).
- **The ATR(20) volatility unit** — same as V1 by canonical-volatility-unit anchor (§5.1).
- **The 0.10 × ATR(20) stop-buffer convention** — same as V1 by stop-buffer-convention anchor (§5.4).
- **The [0.60, 1.80] × ATR(20) stop-distance admissibility band** — same as V1 by admissibility-band anchor (§5.9).
- **The next-bar-open fill model** — same as V1 by engine-fill-model anchor (§5.3).
- **The protective `STOP_MARKET / closePosition / workingType=MARK_PRICE` configuration** — same as V1 by §1.7.3 lock and live-execution-mirror anchor (§5.4).

These are **convention shares**, not predicate shares. None of them constitute V1's breakout mechanism.

---

## 7. Required data inputs

### 7.1 v002 dataset sufficiency

**Sufficient.** F1 requires only:

- BTCUSDT 15m kline data (close, high, low) — present in v002.
- ETHUSDT 15m kline data — present in v002.
- 15m ATR(20) — derivable from v002 kline data using existing engine ATR primitive.
- Funding-rate data — present in v002 (used unchanged for cost realism per §8.4).
- Mark-price kline data — present in v002 (used unchanged for stop-trigger evaluation per §8.5).
- Exchange metadata snapshots — present in v002 (used unchanged for symbol-precision and order-validity).

No additional raw data is required. v002 has full coverage for F1 spec-writing AND first execution (Phase 3d, if and when authorized).

### 7.2 Required derived features

Three new derived features are required, all computable from v002 kline data:

1. `cumulative_displacement_8bar(B) = close(B) − close(B−8)` — single scalar per symbol per 15m bar.
2. `sma_8_close(B) = (1/8) × Σ_{i=0..7} close(B−i)` — single scalar per symbol per 15m bar.
3. `overextension_flag(B) = (| cumulative_displacement_8bar(B) | > 1.75 × ATR(20)(B))` — boolean per symbol per 15m bar.

These are computed from existing v002 close and ATR(20) data; no new raw ingestion.

### 7.3 New versioned feature dataset

**Recommended.** Per `dataset-versioning.md` §"Datasets that must be versioned" (derived datasets), a new versioned feature dataset should be created when the F1 spec progresses to Phase 3c implementation. Recommended naming per the existing convention `<dataset_name>__vNNN`:

- `mean_reversion_features_btcusdt_15m__v001`
- `mean_reversion_features_ethusdt_15m__v001`

Each manifest should record: symbol, interval, schema, source dataset version (the v002 kline + ATR datasets), computation code reference, and creation timestamp per `dataset-versioning.md` §"Minimum required manifest fields".

This is **not** a v003 raw-data bump. v002 raw-data versions are unchanged and used directly. Only new derived feature datasets are added.

### 7.4 v003 raw-data need

**Not required** for Phase 3b spec-writing or for any Phase 3c execution. v002 raw data is sufficient.

A v003 raw-data bump might become relevant in a hypothetical future scenario:

- New raw data sources (e.g., order-book snapshots for execution-realism per Phase 2y §5.1.3) — out of Phase 3 scope.
- ETH-microstructure depth/spread data for live-realism (Phase 2y §5.1.8) — out of Phase 3 scope.

Phase 3b explicitly does not propose v003.

---

## 8. Backtester / engine implications

### 8.1 Existing engine support

The existing `src/prometheus/research/backtest/engine.py` engine, as evolved through Phase 2w, supports F1 with the following additions. The Phase 2w R2 implementation pattern (Phase 2w-A: new strategy module + dispatch keyword) is the pattern F1 would follow.

Existing engine behaviors that F1 reuses unchanged:

- Per-completed-bar evaluation loop with strict completed-bar discipline.
- ATR(20) computation primitive.
- Slippage application (LOW / MEDIUM / HIGH per `config.py:55-59`, unchanged).
- Taker fee application (`taker_fee_rate=0.0005`, unchanged).
- Funding integration over hold period (unchanged).
- Mark-price stop-trigger evaluation (default; TRADE_PRICE as sensitivity diagnostic).
- Trade record output (parquet + JSON; will need F1-specific column additions).
- Manifest generation (will need F1 strategy variant identifier in `config_snapshot.json`).
- §10.3 / §10.4 / §11.3 / §11.4 / §11.6 metric computation (applied to F1's results unchanged; cross-family interpretation per §12).

### 8.2 New strategy module

A new strategy module would be required at (recommended path) `src/prometheus/strategy/v2_mean_reversion/`. The module would contain:

- `variant_config.py` — `MeanReversionConfig` Pydantic model with the §4 axes as locked fields.
- `strategy.py` — `MeanReversionStrategy` class implementing the per-bar evaluation logic (overextension detection, entry signal, target/stop/time-stop checks, cooldown/re-entry rule).
- `entry_lifecycle.py` — entry-state types (no PendingCandidate-style lifecycle is needed; F1 uses immediate market-on-next-bar-open per §4.3).
- `__init__.py` — public exports.

The engine would acquire a strategy-family dispatch (analogous to the V1 breakout `EntryKind` enum dispatch added in Phase 2w-A): a new top-level `StrategyFamily` enum (e.g., `V1_BREAKOUT`, `MEAN_REVERSION`) plus a corresponding `BacktestConfig.strategy_variant` polymorphism. Phase 3c would specify the exact dispatch shape.

Estimated implementation surface (Phase 2t §J.6-style budget, for any future Phase 3d execution phase): 1500–2500 lines of source + tests + scripts. This is comparable to Phase 2w R2's 2700-line surface (which included a full Pending-Candidate lifecycle + 5-step precedence + 43 R2 unit tests), so 1500–2500 reflects F1's simpler entry-lifecycle structure (no pending candidates, no precedence rules, no fill-time rejection cascades).

### 8.3 New diagnostics

F1-specific diagnostics required for Phase 3d execution:

- **Overextension-magnitude distribution** — histogram of `| cumulative_displacement_8bar |` at signal-time bar B for fired entries; mean / median / p25 / p75 / max.
- **Distance-to-mean distribution** — `| open(B+1) − sma_8_close(B) |` divided by `ATR(20)(B)` for fired entries; per direction.
- **Entry-to-target distance** — `| sma_8_close(B) − open(B+1) |` in price units; same expressed in R-multiples.
- **Stop-distance distribution** — `stop_distance` from §4.9 for fired entries; band-violation rejection counts per direction.
- **Cooldown / re-entry attribution** — number of overextension events that fired entries vs were blocked by §4.7 cooldown; cooldown duration distribution per cycle.

Cross-family diagnostics (supporting §12 cross-family references):

- Overlap with V1 breakout signals on the same bars (intersection-trade analysis): how many F1 entries occur on bars where V1 also has a setup/trigger? Per Phase 2w P.5 convention.
- Per-regime decomposition using the same 1h-volatility tercile classifier as Phase 2l §6.1 / Phase 2w §11.9 (low_vol / med_vol / high_vol; trailing 1000-bar window).

### 8.4 Existing cost model applies unchanged

The canonical cost model (`src/prometheus/research/backtest/config.py:55-87`) applies to F1 unchanged:

- Slippage tiers LOW=1.0 / MED=3.0 / HIGH=8.0 bps per side (unchanged per Phase 2y closeout).
- Taker fee rate 0.0005 (unchanged).
- Funding integration over hold period (unchanged).
- Net-of-cost net_r_multiple computation per `cost-modeling.md` (unchanged).
- §11.6 HIGH-slippage cost-sensitivity gate evaluation (unchanged thresholds and gate definition per Phase 2y).

F1 inherits the same cost-realism discipline as V1 breakout. F1's mean-reversion geometry produces shorter R-distances on average (target = SMA(8); structural stop beyond 8-bar extreme), so per-trade cost is a larger fraction of edge — this is exactly the §11.6 cost-fragility risk flagged in §10.7 below.

### 8.5 Mark-price stop-trigger semantic

Per `v1-breakout-strategy-spec.md` and Phase 2g GAP-20260424-032: mark-price stop-trigger is the default; trade-price is a sensitivity diagnostic. Same applies to F1. The existing engine `stop_trigger_source: StopTriggerSource = StopTriggerSource.MARK_PRICE` default is unchanged.

The §11 mandatory-diagnostics list includes mark-price-vs-trade-price sensitivity for F1's first execution, mirroring the Phase 2l / 2m / 2s / 2w pattern.

---

## 9. Falsifiable mechanism predictions

Three mechanism predictions, written in M1 / M2 / M3 style per Phase 2u §K / Phase 2v §5.2 convention. Phase 3b does not compute anything; these are pre-declared expectations to be evaluated empirically by Phase 3d execution.

### 9.1 M1 — overextension reversion

**Prediction:** On bars where F1 fires an entry, the next-N-bar (N=8, matching the §4.6 time-stop horizon) cumulative directional displacement against the overextension direction should exceed zero in expectation, net of cost.

**Diagnostic at execution time:** for each fired F1 entry, compute the post-entry net displacement at horizons {1, 2, 4, 8} completed bars. Aggregate per symbol per direction. The mean post-entry counter-displacement should be positive at all four horizons, and should be statistically distinguishable from zero at the 8-bar horizon (the longest matching the time-stop).

**Pass threshold (pre-declared):** at least 50% of fired F1 entries on BTCUSDT should produce non-negative counter-displacement at the 8-bar post-entry horizon, AND the mean counter-displacement at the 8-bar horizon should be ≥ +0.10 R per trade (R measured in F1's own R-distance units).

**Fail threshold:** if mean counter-displacement at the 8-bar horizon is ≤ 0 R per trade on BTCUSDT, M1 fails — the overextension-reversion mechanism is not operative; F1's edge claim is mechanism-falsified regardless of any framework PROMOTE/FAIL outcome.

### 9.2 M2 — chop-regime stop-out fraction

**Prediction:** On chop / range-bound regimes (operationalized as the low-vol tercile of the 1h-volatility classifier per Phase 2l §6.1 convention), F1's stop-out fraction should be **lower** than V1 breakout's stop-out fraction in the same regime.

**Diagnostic at execution time:** compute F1's per-regime stop-exit fraction from the F1 trade log; compare to H0 (V1 breakout baseline) and R3 stop-exit fractions on the same R-window's same low-vol regime trades (already on record per Phase 2l §6.1).

**Pass threshold (pre-declared):** F1's low-vol-regime stop-out fraction on BTCUSDT < H0's low-vol-regime stop-out fraction on BTCUSDT, with magnitude ≥ 0.10 (i.e., F1 stops out at least 10 percentage points less often than V1 in low-vol).

**Fail threshold:** if F1's low-vol stop-out fraction is ≥ H0's, M2 fails — the chop-regime advantage hypothesis (§2.3) is not supported.

### 9.3 M3 — mean-reversion target-exit positive contribution

**Prediction:** F1's TARGET exits (where the trade closes via §4.5 mean-reference cross) should produce positive aggregate net-of-cost R-multiple contribution. That is: `Σ_target_exits net_r_multiple > 0` after fees + slippage.

**Diagnostic at execution time:** compute aggregate net-of-cost R-multiple for the subset of F1 trades that exit via TARGET; compute counts; compare to STOP-exit and TIME-STOP-exit subsets.

**Pass threshold (pre-declared):** TARGET-exit aggregate net R-multiple > 0 on BOTH BTCUSDT and ETHUSDT; mean per-target-exit R-multiple ≥ +0.30 R (acknowledging the SMA(8) target produces R-multiples typically below +1.0 R given the geometric relationship between entry-to-stop and entry-to-mean distances).

**Fail threshold:** if TARGET-exit aggregate net R-multiple is ≤ 0 on either symbol, M3 fails — the mean-reversion target's claimed edge does not survive cost realism even when target-exit subset is isolated.

### 9.4 Combined mechanism reading

Phase 2v §5.3 cross-tabulation pattern applied to F1:

| M1 | M2 | M3 | Reading |
|----|----|----|---------|
| PASS | PASS | PASS | **Mechanism FULLY supported.** F1 thesis confirmed mechanically. Independent of §10.3 framework PROMOTE/FAIL verdict. |
| PASS | PASS | FAIL | Reversion happens but cost erodes target-exit contribution. Cost-fragility likely. |
| PASS | FAIL | PASS | Reversion happens; chop-regime advantage absent. F1 produces edge in unexpected regimes. |
| PASS | FAIL | FAIL | Reversion happens but neither chop-advantage nor cost-survivable target-exit. Family thesis weak. |
| FAIL | * | * | **Mechanism FALSIFIED.** F1's central claim (overextension reverts) is empirically wrong. |

---

## 10. Expected failure modes

Per the operator brief: enumerate the failure modes Phase 3d execution should anticipate.

### 10.1 Trend continuation destroys mean-reversion entries

**Mechanism:** in a strong trending regime (e.g., 2024H1 or extended directional moves), the cumulative-displacement predicate fires repeatedly on overextension events that continue rather than revert. Each F1 entry stops out at the structural-stop level; the same overextension state re-forms after the cooldown unwinds and re-fires; the cycle repeats.

**Empirical signature:** high stop-out fraction in high-vol or trending regimes (M2 fails); aggregate negative R per fold during the trending period; per-fold consistency degrades.

**Mitigation under unchanged spec:** none — F1 does not regime-filter. The §11 per-regime decomposition diagnostic surfaces the failure mode for Phase 3c-or-later regime-conditional spec consideration.

### 10.2 Stops too tight under high volatility

**Mechanism:** F1's structural stop is `lowest_low([B−7..B]) − 0.10 × ATR(20)`. On high-vol bars, the 8-bar low can be very close to the entry; the resulting stop distance is ≤ 0.60 × ATR(20) and falls outside the §4.9 admissibility band. The trade is rejected; no F1 entry fires on these bars even though the overextension predicate fires.

**Empirical signature:** non-trivial fraction of overextension events rejected by §4.9 stop-distance band; rejected events are concentrated in high-vol regimes.

**Mitigation under unchanged spec:** none — the rejection is the spec's intended behavior. The §11 cooldown / re-entry attribution diagnostic surfaces the rejection rate.

### 10.3 Targets too small after costs

**Mechanism:** F1's target is the SMA(8) at signal time. The entry-to-target distance is structurally smaller than V1 breakout's entry-to-+2.0R distance. Per-trade R-multiples on TARGET exits are typically below +1.0 R. After round-trip costs (16 bps round-trip slippage at HIGH + 10 bps round-trip taker fees = 26 bps total at HIGH; ~0.05–0.10 R per trade depending on R-distance), the TARGET-exit aggregate contribution can collapse.

**Empirical signature:** §11.6 §10.3 disqualification at HIGH slippage; M3 FAIL on either symbol.

**Mitigation under unchanged spec:** none — this is exactly the structural risk the §11.6 gate is designed to identify. Per Phase 2y closeout, the gate is preserved; F1 either clears it cleanly or it doesn't.

### 10.4 Excessive trade frequency

**Mechanism:** F1's overextension predicate fires more often than V1 breakout's setup-and-trigger combination. Per Phase 3a §4.1 estimate, F1 could produce 80–120 trades per R-window per symbol, vs V1's 33. High trade frequency × small per-trade R-multiples × non-trivial cost = aggregate cost erosion exceeding aggregate edge.

**Empirical signature:** per-trade expR small in absolute terms; aggregate netPct dominated by cost stack rather than directional edge.

**Mitigation under unchanged spec:** none — frequency is mechanism-determined. The §11 trade-count and frequency diagnostic surfaces this for execution-time interpretation.

### 10.5 False mean reference

**Mechanism:** the SMA(8) at signal time may not be a meaningful equilibrium value. In a trending regime, SMA(8) is itself drifting; targeting a drifting reference can systematically miss (target too far in continuation regimes, target already crossed in chop regimes).

**Empirical signature:** entry-to-target distance distribution shows large left-tail (target already near entry → trivial wins) AND large right-tail (target far from entry → time-stop fires before target reached); §11.5 distance-to-mean diagnostic non-uniform.

**Mitigation under unchanged spec:** none — SMA(8) is the committed reference. A future F1-prime spec could specify a different reference (e.g., longer-window mean), but that would be Phase 3c-or-later, not Phase 3b.

### 10.6 BTC/ETH asymmetry

**Mechanism:** Phase 2x §4.6 documented that BTC and ETH have different microstructure and regime profiles. F1's plausibility argument (§2.4) was BTC-favorable. ETH could behave differently — higher spread, shallower depth, more trending regimes — producing F1 ETH degradation similar to R1a's BTC asymmetry (inverted).

**Empirical signature:** §11.4 ETH-as-comparison fails; ETH F1 produces §10.3 disqualification while BTC clears.

**Mitigation under unchanged spec:** none. Per §1.7.3, BTC is primary; an ETH-degrading variant remains research-evidence under §11.4 governance.

### 10.7 §11.6 HIGH-slippage failure

**Mechanism:** per §10.3 above, F1's target geometry produces small R-multiples on TARGET exits. At HIGH = 8 bps slippage (per Phase 2y closeout), the round-trip cost is 16 bps slippage + 10 bps fees = 26 bps total. The Phase 2w R2 precedent demonstrates that mean-reversion-style geometries (smaller R-distance + smaller per-trade payoff) can cleanly clear §10.3 at MED slippage and FAIL §11.6 at HIGH.

**Empirical signature:** §11.6 disqualification on one or both symbols at HIGH slippage.

**Mitigation under unchanged spec:** none — Phase 2y closed Option C with "keep §11.6 = 8 bps unchanged". F1 either clears §11.6 or it doesn't; failure is informative even if §10.3 PROMOTES at MED.

### 10.8 Engine implementation bugs

**Mechanism:** any new strategy module introduces a non-zero risk of leakage, lookback-window off-by-one, frozen-vs-rolling-target confusion, or cooldown-rule misimplementation. Phase 2w R2's implementation included two analysis-script bugs (Δ|maxDD| sign convention; P.14 post-slip vs raw band reference) that were caught before final analysis; the engine itself was bug-free.

**Mitigation under Phase 3c planning + Phase 3d execution:** Phase 2v §3.2.2 bit-for-bit reproduction discipline applied to H0/R3 controls; Phase 2w P.14 hard-block check pattern adapted for F1 (e.g., F1-specific accounting identity; cooldown re-entry attribution; stop-distance band enforcement). These are Phase 3c / Phase 3d obligations, not Phase 3b spec details.

---

## 11. Mandatory diagnostics for any future execution

Per the operator brief: enumerate the diagnostics that any Phase 3d execution must produce. Phase 3b lists requirements; Phase 3c plans the exact computation; Phase 3d implements and reports.

### 11.1 Per-trade aggregate diagnostics

- Trade count and frequency (per symbol per R-window per V-window).
- Long/short split (count, expR, PF per direction).
- Win rate per symbol per direction.
- Average per-trade R-multiple.
- Profit factor.
- Net percentage (`netPct`).
- Maximum drawdown (`|maxDD|`) per symbol.

### 11.2 Per-regime decomposition

Per the Phase 2l §6.1 / Phase 2w §11.9 convention: 1h-volatility tercile classifier with trailing 1000-bar Wilder ATR(20) percentile rank; tercile boundaries at 33rd / 67th percentiles; classification at the most recent completed 1h bar before entry-fill.

For each variant (F1 + H0 cross-family reference + R3 cross-family reference) per symbol per regime cell:

- Trade count `n`.
- expR.
- PF.
- WR.

### 11.3 Per-fold consistency

Per the Phase 2f §11.2 / GAP-20260424-036 convention: 5 rolling folds across the R-window; partial-train front-edge first fold; 6-month test windows stepping 6 months. For each F1 fold-symbol cell:

- Trade count `n`.
- expR.
- PF.
- ΔvH0.
- ΔvR3 (descriptive cross-family reference per §12).

### 11.4 Exit-reason fractions

- Stop-exit fraction.
- Target-exit fraction (F1's TARGET exits via §4.5).
- Time-stop fraction (F1's 8-bar §4.6).
- (Sum should equal 1.0 to within rounding; identity check is a P.14-style hard block.)

### 11.5 F1-specific distributions

- **Overextension magnitude distribution.** Histogram of `| cumulative_displacement_8bar(B) | / ATR(20)(B)` for fired F1 entries (i.e., the magnitude is normalized in ATR units). Mean / median / p25 / p75 / max.
- **Distance-to-mean distribution.** Histogram of `| sma_8_close(B) − open(B+1) | / ATR(20)(B)` for fired F1 entries.
- **Entry-to-target distance.** Same as distance-to-mean for fired F1 entries; same expressed as a fraction of the per-trade R-distance (i.e., target-distance ÷ stop-distance).
- **Stop-distance distribution.** `stop_distance / ATR(20)(B)` for fired F1 entries (within the §4.9 admissibility band [0.60, 1.80] by construction).
- **Cooldown / re-entry attribution.** Count of overextension events that (a) fired an entry; (b) were blocked by §4.9 stop-distance admissibility; (c) were blocked by §4.7 cooldown rule.

### 11.6 Cost-sensitivity sweep

Per Phase 2l §8 / Phase 2m §10 / Phase 2w §7 convention: F1 evaluated at each slippage tier (LOW = 1.0 bps per side; MED = 3.0 bps per side committed; HIGH = 8.0 bps per side per `config.py:55-59` and Phase 2y closeout). Per-tier per-symbol expR, PF, netPct, maxDD, ΔvH0, §10.3 verdict at that tier.

### 11.7 Mark-price vs trade-price sensitivity

Per Phase 2g GAP-20260424-032 convention. F1 evaluated at MARK_PRICE (default) and TRADE_PRICE for the §11.6 sensitivity diagnostic. Bit-identical match on bars without gap-throughs is the expected pattern (per Phase 2l / 2m / 2s / 2w precedent).

### 11.8 MFE / MAE distribution

Per Phase 2l §6.2 / Phase 2w §11.11 convention. Per fired F1 entry: MFE (maximum favorable excursion) and MAE (maximum adverse excursion) in R-multiples. Mean / median / max per direction per symbol.

### 11.9 Cross-family reference comparisons

Per §12 below: F1 vs H0 (descriptive cross-family reference, NOT governing anchor) and F1 vs R3 (descriptive cross-family reference, NOT governing baseline). The cross-family deltas are computed in the same metric space (ΔexpR, ΔPF, Δ|maxDD|pp) as Phase 2l / 2m / 2s / 2w used for V1-internal variant-vs-anchor comparison, but the **interpretation is different** (§12.4): F1 vs H0 is a cross-family benchmark for "is F1 producing an absolute edge improvement over a zero-strategy null?", not for "is F1 a better V1 breakout variant?".

### 11.10 P.14-style implementation-bug checks

Phase 2w P.14 hard-block pattern adapted for F1:

- **Accounting identity:** `n_target_exits + n_stop_exits + n_time_stop_exits + n_open_at_window_end = n_trades`.
- **No exit-reason leakage:** F1 must not produce `TRAILING_BREACH` or `STAGNATION` exits (those are V1-breakout-specific exit reasons; F1 uses `STOP`, `TARGET`, `TIME_STOP`, `END_OF_DATA`).
- **Stop-distance band enforcement:** all fired F1 entries must have raw (de-slipped) stop_distance ∈ [0.60, 1.80] × ATR(20)(B). Post-slip values may exceed the band by slippage; raw values must not.
- **Cooldown enforcement:** zero F1 same-direction re-entries with overlapping overextension state.
- **Frozen target invariant:** F1 target value at exit equals the SMA(8) value computed at signal-time bar B's close (frozen).
- **Frozen stop invariant:** F1 protective stop at exit equals the structural stop computed at signal-time bar B's close (frozen).
- **No look-ahead:** all F1 decisions at bar B use only bars at index ≤ B; engine's per-bar evaluation discipline confirmed by H0 control reproduction.

---

## 12. Promotion / failure framework

Per the operator brief: how should §10.3 / §10.4 / §11.3 / §11.4 / §11.6 apply to F1, given F1 is a new family rather than a V1-internal variant?

### 12.1 H0 remains the formal V1 breakout family framework anchor

H0 is the locked Phase 2e baseline for the V1 breakout family per Phase 2i §1.7.3. **H0 is V1-family-specific.** H0 is **not** F1's framework anchor. F1's promotion governance must not treat H0 as the comparison baseline whose deltas are tested against §10.3.a / §10.3.b / §10.3.c thresholds — those thresholds were calibrated for V1-internal variant-vs-baseline improvement testing.

### 12.2 R3 is a V1 breakout reference, not the governing F1 baseline

R3 is the V1 breakout baseline-of-record per Phase 2p §C.1. R3 is **V1-family-specific exit machinery**. R3 is **not** F1's baseline-of-record. F1's per-trade expR / PF / |maxDD| compared to R3 produces deltas that are **descriptive cross-family references**, not §10.3 governing metrics.

The Phase 2x §4.6 BTC/ETH-asymmetry framing applies symmetrically here: comparing F1's BTC results to R3's BTC results would unfairly require F1 to beat R3 on R3's terms (V1-breakout-cleared exit machinery); F1 has different mechanism, different trade frequency, different cost profile.

### 12.3 F1 establishes its own first-execution baseline

If Phase 3d execution proceeds, F1's first execution is **self-anchored**:

- F1's R-window aggregate expR per symbol is the first F1 result.
- The §10.3 framework's promotion paths (a) / (b) / (c) and disqualification floors apply to **F1 vs a zero-strategy null**, not to F1 vs H0.
- F1 vs zero-strategy null:
  - PROMOTE if F1 produces positive aggregate net-of-cost expR on at least one symbol AND the M1 mechanism prediction (§9.1) passes on BTCUSDT.
  - PROMOTE-with-caveats if F1 produces positive aggregate net-of-cost expR on at least one symbol but M1 fails (mechanism falsified despite framework PROMOTE).
  - Disqualified if F1 produces aggregate net-of-cost expR ≤ 0 on both symbols (no edge to capture).

### 12.4 Cross-family references are descriptive, not governing

F1 vs H0 deltas (computed per §11.9) inform interpretation but do not gate promotion. Two specific cases:

- **F1 vs H0 produces ΔexpR > +0.10 R AND F1 absolute aggregate expR < 0:** F1 is "less negative than H0". This is the same shape R3's first-PROMOTE result had (R3 BTC −0.240 vs H0 −0.459). For R3 inside the V1 family, this was a clean PROMOTE. **For F1 as a new family, this is descriptively informative but not equivalent.** F1's PROMOTE governance under §12.3 requires absolute positive expR or M1-passing mechanism support, not just being-less-negative-than-V1.
- **F1 vs H0 produces ΔexpR < 0 AND F1 absolute aggregate expR > 0:** F1 produces positive absolute edge but smaller magnitude than H0's negative edge magnitude. This would be a clean F1 PROMOTE under §12.3 even though F1 is "worse than V1 by a §10.3.a-type metric" — because the metric is mis-applied across families.

### 12.5 §10.4 hard reject

§10.4 hard reject (`expR < −0.50 OR PF < 0.30` AND `Δn ≥ +50%`) was calibrated for V1-internal variants where increased trade count is a red flag. For F1, increased trade count vs H0 is **expected by mechanism** (§10.4 / Phase 3a §4.1: 80–120 trades vs 33). §10.4 should apply to F1's absolute thresholds (`expR < −0.50` OR `PF < 0.30`), not to the trade-count delta. If F1 produces aggregate expR ≤ −0.50 R on either symbol or PF ≤ 0.30 on either symbol, F1 is hard-rejected regardless of mechanism support.

### 12.6 §11.3 V-window discipline

§11.3 V-window discipline applies unchanged: V-window is no-peeking; if F1 PROMOTES on R, the V-window is run as direction-of-improvement confirmation; V does not retroactively re-classify R-window verdict; sample-size caveats apply.

### 12.7 §11.4 ETH-as-comparison

§11.4 BTC-must-clear / ETH-must-not-catastrophically-fail rule applies unchanged. Per §1.7.3, BTCUSDT is primary live; ETH is comparison-only. F1 PROMOTE governance under §12.3 requires BTC PROMOTE; ETH catastrophic failure (e.g., ETH expR ≤ −0.50 R) blocks combined family-PROMOTE even if BTC clears.

### 12.8 §11.6 cost-sensitivity gate

§11.6 HIGH-slippage cost-sensitivity gate (8 bps per side per Phase 2y closeout) applies unchanged. F1 must clear §10.3 disqualification at HIGH on both symbols. F1's structural cost-sensitivity risk (§10.7) makes this the most-likely failure mode.

### 12.9 §11.3.5 binding rule

No threshold change. No post-hoc loosening of §10.3 / §10.4 / §11.3 / §11.4 / §11.6 to rescue any F1 outcome. If F1 fails §11.6 at HIGH (the same way R2 did), F1's framework verdict is FAILED per the same discipline that produced R2's FAILED verdict.

### 12.10 Avoiding unfair cross-family comparison

The operator brief specifies: "how to avoid unfairly comparing a new family to an old family." Three explicit disciplines:

1. **F1's primary judgment is on F1's own absolute edge** (§12.3), not on F1-vs-V1 deltas.
2. **F1's M1 / M2 / M3 mechanism predictions** (§9) are F1-internal falsification tests; they do not require F1 to "beat" V1.
3. **F1's §11.6 cost-sensitivity is judged on F1's own absolute results at HIGH slippage** (e.g., F1 BTC expR > 0 at HIGH? F1 PF > 0.30 at HIGH?), not on F1-vs-H0 deltas at HIGH.

Cross-family references (F1 vs H0 / F1 vs R3) appear in reports but are explicitly labeled as descriptive, not governing.

---

## 13. Overfitting risk analysis

### 13.1 Why F1 is vulnerable to threshold fitting

F1's spec involves multiple numerical anchors (window N=8, threshold 1.75 × ATR, target = SMA(8), stop buffer = 0.10 × ATR, time-stop horizon = 8 bars, cooldown rule, stop-distance band [0.60, 1.80] × ATR). Each anchor is a degree of freedom. Without discipline, a Phase 3c-or-later execution could iterate:

- "8 bars didn't work; try 6, 10, 12."
- "1.75 × ATR threshold didn't work; try 1.50 or 2.00."
- "SMA(8) target didn't work; try EMA(20) or VWAP."
- "0.10 × ATR buffer didn't work; try 0.05 or 0.20."
- "[0.60, 1.80] band didn't work; widen it."
- "Add a regime filter to disqualify trending regimes."
- "Add a confirmation candle to reduce false signals."

Each iteration introduces fit risk. With three R-window symbols × two V-window cross-checks × multiple regime cells × LOW/MED/HIGH cost tiers, the multiple-comparisons surface is large. A determined search would find some combination that produces a clean §10.3 PROMOTE; that combination would likely be over-fit and fail in any new period.

This is exactly the failure mode `backtesting-principles.md` "Risks and Failure Modes" warns against: "repeated parameter tuning until something works."

### 13.2 How the single-spec rule prevents this

Phase 2j §C.6 / §11.3.5 binding rule: ONE conceptual value/rule per axis. Phase 3b commits singularly per §4. Phase 3c execution must use these exact rules. Phase 3d's reported result is the result; failure is failure; no Phase 3d-internal re-tuning is permitted.

### 13.3 What must be forbidden in execution

Phase 3c execution-planning and Phase 3d execution must explicitly forbid:

- **Parameter sweeps over F1 axes.** No grid search over window length / threshold / target horizon / stop buffer / time-stop horizon / stop-distance band.
- **Per-symbol parameter tuning.** No "BTC works at threshold X but ETH at Y" cherry-picking.
- **V-window peeking for R-window parameter selection.** §11.3 no-peeking discipline preserves V as out-of-sample.
- **Regime-conditional spec mutations during execution.** If §11.2 per-regime decomposition shows trending-regime degradation, that becomes evidence for any future F1-prime spec; it does NOT authorize mid-execution F1 spec mutation.
- **Confirmation-candle additions during execution.** Adding entry confirmation mid-execution to "improve" the result is post-hoc fitting.
- **Cost-tier selection for promotion.** §11.6 evaluates HIGH; failing at HIGH is failing at §11.6 regardless of MED clearance.
- **Cross-family comparison-baseline gaming.** F1 promotion under §12.3 must not be reframed mid-execution as "F1 beats H0" if F1 fails its own absolute-edge test.
- **Sub-parameter introduction.** F1's spec has no sub-parameters in the Phase 2j §D.6-style "sub-parameters can be tuned within a committed spec" sense. Every numerical anchor is a primary committed value.

---

## 14. GO / NO-GO decision for Phase 3c execution planning

This recommendation is **provisional and evidence-based, not definitive**. The operator decides whether to authorize a downstream Phase 3c execution-planning phase.

### 14.1 GO criteria evaluation

The operator brief specifies four GO/NO-GO conditions:

1. **GO only if F1 can be specified cleanly without tuning.** ✓ MET — §4 commits one rule per axis; §5 anchors each rule to existing project conventions; §13 forbids parameter sweeps and mid-execution mutations.
2. **NO-GO if the spec requires too many arbitrary parameters.** ✓ MET — F1's spec has no arbitrary parameters; every numerical anchor is anchored to V1 breakout conventions (window N=8 from V1 setup window; threshold 1.75 × ATR from V1 setup_range_width cap; SMA(8) from same window; 0.10 × ATR buffer from V1 stop convention; 8-bar time-stop from R3/V1 stagnation horizon; [0.60, 1.80] band from V1 admissibility filter).
3. **NO-GO if it degenerates into V1 breakout under another name.** ✓ MET — §6 distinguishes F1 from V1 on six independent grounds; the §4.1 overextension predicate is the structural inverse of V1's setup-validity predicate (§2.2); F1's mean-reversion target is logically opposite to V1/R3's continuation-anchored exit machinery.
4. **NO-GO if cost sensitivity appears structurally fatal.** ⚠ FLAGGED — F1's mean-reversion geometry produces small per-trade R-multiples; §10.7 + §11.6 = 8 bps HIGH cost-sensitivity is the most-likely failure mode. **However**, this is not a Phase 3b spec defect; it is the structural risk Phase 3c-or-later execution will empirically test. Per Phase 2y closeout, the §11.6 gate is the disciplined evaluator of cost-fragility; F1 either clears or it doesn't, and either outcome is informative.

The cost-sensitivity flag is NOT a NO-GO blocker because:
- The §11.6 gate is doing exactly what it was designed to do — discriminating between cost-robust and cost-fragile candidates.
- F1's potential §11.6 failure would be an additional data point in the "entry/target axis improvements are cost-fragile" pattern Phase 2x §4.5 documented.
- Phase 3b's job is to specify F1 cleanly; whether F1 survives §11.6 is Phase 3d's empirical question.

### 14.2 GO recommendation

**GO** — Phase 3c execution planning is **provisionally recommended** as the next downstream docs-only phase if and when the operator authorizes it.

Phase 3c would be a Phase 2k/2t/2v-style execution-planning memo:
- Define exact run inventory (variants × windows × slippage × stop-trigger-source).
- Specify exact engine-implementation surface (new strategy module, new dispatch enum, new diagnostic counters).
- Pre-declare exact computational formulas for §11 diagnostics.
- Pre-declare §10.3 / §10.4 / §11.3 / §11.4 / §11.6 evaluation per §12.
- Specify hard-block test additions (P.14-style for F1).
- Specify H0 / R3 control re-run discipline (cross-family reference-only, per §12.4).
- Produce a Phase 3c GO/NO-GO recommendation for Phase 3d execution implementation.

Phase 3c is **docs-only**; it does not authorize implementation. Phase 3d would be the first phase that authorizes code-writing, test-writing, and backtest execution.

### 14.3 Phase 3c GO does NOT authorize

- **No code change.** Phase 3c is docs-only.
- **No backtest run.** Phase 3c is docs-only.
- **No threshold change.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds verbatim.
- **No project-level lock change.** §1.7.3 verbatim.
- **No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials / `data/` work.**
- **No Phase 3d execution implementation.** Phase 3d would require its own separately-authorized phase.

### 14.4 Alternative: NO-GO and remain paused

If the operator judges that Phase 3c execution planning is not the right next step, **remaining paused** is a valid alternative:

- The Phase 3b spec memo itself (this document) becomes the family-research artifact even without Phase 3c authorization.
- Phase 2x Option A (remain paused after Phase 2y closure) continues to be valid.
- F1's spec is preserved for any future revival.

The recommendation is **GO for Phase 3c if any active path is desired**, with **remain-paused as the legitimate alternative** under the operator's discretion.

---

## 15. Explicit project-state preservation statement

Phase 3b explicitly preserves the following:

- **R3 remains the V1 breakout baseline-of-record** per Phase 2p §C.1. Locked sub-parameters: `exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. R3 is **not** F1's anchor or baseline (§12.2).
- **H0 remains the formal V1 breakout framework anchor** per Phase 2i §1.7.3. H0 is **not** F1's framework anchor (§12.1); F1 uses self-anchoring per §12.3.
- **R1a remains research evidence only** per Phase 2p §D. Retained-for-future-hypothesis-planning. Not the current default. Not the deployable path.
- **R1b-narrow remains research evidence only** per Phase 2s §13.
- **R2 remains research evidence only** per Phase 2w §16.3. Framework verdict FAILED — §11.6 cost-sensitivity blocks. Mechanism evidence (M1 + M3 PASS; M2 FAIL) preserved as descriptive.
- **No threshold change.** Phase 2f §10.3 / §10.4 / §11.3 / §11.4 / **§11.6 = 8 bps HIGH** preserved verbatim per Phase 2f §11.3.5 / Phase 2y closeout. `src/prometheus/research/backtest/config.py:55-59` unchanged.
- **No project-level lock change.** §1.7.3 BTCUSDT primary, ETHUSDT research/comparison only, one-symbol-only live, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets — all preserved verbatim.
- **No paper/shadow planning is authorized.** Phase 2p §F.2 / post-Phase-2w / Phase 2x §6 / Phase 2y §8.4 / Phase 3a §7 deferrals stand.
- **No Phase 4 (runtime / state / persistence) is authorized.** Same authorities.
- **No live-readiness, deployment, exchange-write capability, production keys, MCP / Graphify / `.mcp.json` activation, credentials.**
- **No `data/` commits.**
- **No code change.** No file in `src/`, `tests/`, or `scripts/` is touched by Phase 3b.
- **No spec change to existing documents.** `v1-breakout-strategy-spec.md`, `v1-breakout-validation-checklist.md`, `cost-modeling.md`, `backtesting-principles.md`, `phase-gates.md`, `technical-debt-register.md`, `data-requirements.md`, `dataset-versioning.md`, `current-project-state.md`, `ai-coding-handoff.md` all preserved.
- **No Phase 3c authorization.** Phase 3b recommends GO for Phase 3c (§14.2) provisionally; the operator separately authorizes Phase 3c (or doesn't).
- **No V1 breakout family revival.** F1 is a new family; V1 R3 remains paused-as-baseline-of-record without active V1-family research.

---

**End of Phase 3b F1 mean-reversion-after-overextension specification memo.** Sections 1–15 complete per the operator brief's required structure. F1 specified single-rule per axis with non-fitting rationale anchored to existing V1 breakout / Phase 2 conventions; F1 distinguished from V1 breakout on six independent grounds; v002 datasets sufficient with new derived feature dataset required; engine-implementation surface estimated at 1500–2500 lines; M1 / M2 / M3 falsifiable mechanism predictions pre-declared; expected failure modes enumerated including §11.6 cost-fragility flag; mandatory diagnostics enumerated for any future Phase 3d execution; promotion/failure framework specifies F1 self-anchoring with H0/R3 as descriptive cross-family references only; overfitting risk analysis applies §11.3.5 single-spec discipline; **GO (provisional) recommendation for Phase 3c execution planning** as the next downstream docs-only phase if and when the operator authorizes it; **remain-paused** is the legitimate alternative. Project state preserved verbatim. R3 V1 baseline-of-record / H0 V1 framework-anchor / R1a-R1b-narrow-R2 retained-research-evidence preserved. No threshold change. No project-lock change. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / credentials / `data/` work. **NO-GO for any execution / paper-shadow / Phase 4 / live-readiness / deployment / threshold-change / project-lock change.** Awaiting operator review.
