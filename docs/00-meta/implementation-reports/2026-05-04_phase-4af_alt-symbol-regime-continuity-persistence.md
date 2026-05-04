# Phase 4af — Alt-Symbol Regime-Continuity and Directional-Persistence Feasibility Memo

## 1. Purpose

Phase 4af computes descriptive regime-continuity and directional-persistence
metrics for the Phase 4ac core symbol set
(`BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`)
at intervals `15m`, `30m`, `1h`, `4h`, under Phase 4ad Rule B1
(common post-gap start `2022-04-03 00:00 UTC`).

Phase 4af is **analysis-and-docs only**. It exists to help answer whether any
alt-symbol substrate shows enough directional persistence, trend-state
continuity, or post-expansion follow-through to *eventually* justify a
docs-only fresh-hypothesis discovery memo, or whether remain-paused is still
the correct posture.

Explicit non-actions:

```text
no data acquisition
no data download
no API calls
no endpoint calls
no data modification
no manifest creation or modification
no v003 or any dataset version
no backtests
no strategy diagnostics
no Q1-Q7 rerun
no strategy PnL
no entry / exit strategy returns
no parameter optimization
no threshold selection for any future strategy
no new strategy candidate
no fresh-hypothesis discovery memo
no hypothesis-spec memo
no strategy-spec memo
no backtest-plan memo
no implementation
no live-readiness
no exchange-write
no R3 / R2 / F1 / D1-A / V2 / G1 / C1 rescue
```

Phase 4af preserves every retained verdict and every project lock verbatim.
It does not adopt Phase 4z, Phase 4aa, or Phase 4ab recommendations as
binding governance. It does not broaden Phase 4ac results beyond data /
integrity evidence. It does not broaden Phase 4ad Rules A / B / C beyond
prospective analysis-time scope. It does not flip any `research_eligible`
flag, modify any committed manifest, or modify any normalized data.

## 2. Data Scope and Governance

Symbols analyzed:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Intervals analyzed:

```text
15m
30m
1h
4h
```

Analysis window:

```text
start  : 2022-04-03 00:00:00 UTC  (Phase 4ad Rule B1 common post-gap)
end    : 2026-04-30 23:59:59 UTC  (cell ends at last available bar)
```

Phase 4ad Rule B1 was applied verbatim. SOL/XRP cells are labeled
`Phase4ad_RuleB1_common_post_gap`. ADA cells are PASS per Phase 4ac. BTC/ETH
30m / 1h / 4h cells use Phase 4ac `__v001` PASS manifests; BTC/ETH 15m cells
use Phase 2 `__v002` legacy-eligible manifests (treated as `PASS_or_legacy`).

Mark-price datasets were **not** used. Phase 4ad Rule A was deferred per
Phase 4af brief recommendation.

Metrics / open-interest data were **not** used.

AggTrades / tick / order-book data were **not** used.

Funding history was **not** used (Phase 4af brief explicitly recommends
keeping funding optional/secondary; not centered).

Coverage table summary (20 cells; 0 omitted; 0 missing bars in observed
span):

| symbol  | interval | bars     | governance scope                          |
| ------- | -------- | -------- | ----------------------------------------- |
| BTCUSDT | 15m      | 140 064  | PASS_or_legacy_phase2_eligible_via_v002   |
| BTCUSDT | 30m      |  70 032  | PASS                                      |
| BTCUSDT | 1h       |  35 736  | PASS                                      |
| BTCUSDT | 4h       |   8 754  | PASS                                      |
| ETHUSDT | 15m      | 140 064  | PASS_or_legacy_phase2_eligible_via_v002   |
| ETHUSDT | 30m      |  70 032  | PASS                                      |
| ETHUSDT | 1h       |  35 736  | PASS                                      |
| ETHUSDT | 4h       |   8 754  | PASS                                      |
| SOLUSDT | 15m      | 142 944  | Phase4ad_RuleB1_common_post_gap           |
| SOLUSDT | 30m      |  71 472  | Phase4ad_RuleB1_common_post_gap           |
| SOLUSDT | 1h       |  35 736  | Phase4ad_RuleB1_common_post_gap           |
| SOLUSDT | 4h       |   8 934  | Phase4ad_RuleB1_common_post_gap           |
| XRPUSDT | 15m      | 142 944  | Phase4ad_RuleB1_common_post_gap           |
| XRPUSDT | 30m      |  71 472  | Phase4ad_RuleB1_common_post_gap           |
| XRPUSDT | 1h       |  35 736  | Phase4ad_RuleB1_common_post_gap           |
| XRPUSDT | 4h       |   8 934  | Phase4ad_RuleB1_common_post_gap           |
| ADAUSDT | 15m      | 142 944  | PASS                                      |
| ADAUSDT | 30m      |  71 472  | PASS                                      |
| ADAUSDT | 1h       |  35 736  | PASS                                      |
| ADAUSDT | 4h       |   8 934  | PASS                                      |

All SOL/XRP findings in §5–§11 are labeled `conditional on Phase 4ad Rule B1
common post-gap scope`.

## 3. Methodology

All metric parameters are **descriptive and predeclared, not optimized**.
Metric values are computed from prior-completed bars only; no lookahead
beyond the explicitly defined forward-window construction in §7 (which is
itself descriptive forward-return measurement, not entry/exit logic).

Predeclared parameters:

```text
EMA_FAST                          = 50
EMA_SLOW                          = 200
EMA_SLOPE_LAG                     = 3 bars
ATR_WINDOW                        = 20
ROLLING_WINDOW                    = 96 bars
FORWARD_WINDOWS                   = (1, 2, 4, 8) bars
PERSISTENCE_MOVE_THRESHOLDS_BPS   = (16, 24, 32)
EXPANSION_THRESHOLD_MULTIPLIERS   = (1.5,)
VOL_REGIME_QUANTILE               = 0.75
HIGH_COST_BPS_PER_SIDE            = 8.0   (§11.6 preserved)
ROUND_TRIP_COST_BPS               = 16.0  (§11.6 preserved)
```

### 3.1 Trend-state persistence (§5)

State definitions:

```text
UP      = close > EMA(50) AND EMA(50) > EMA(200)
DOWN    = close < EMA(50) AND EMA(50) < EMA(200)
MIXED   = otherwise (when both EMAs valid)
UNKNOWN = either EMA invalid (warmup)
```

For each symbol / interval, Phase 4af reports state fractions, contiguous
run lengths (median, mean, p75, max for UP and DOWN; median and mean for
MIXED), full transition counts among `{UP, DOWN, MIXED}`, and self-transition
probabilities `P(state[t+1] == s | state[t] == s)` for `UP`, `DOWN`, `MIXED`.

### 3.2 EMA-slope persistence (§6)

```text
SLOPE_POS  = EMA50[t] >  EMA50[t - 3]
SLOPE_NEG  = EMA50[t] <  EMA50[t - 3]
SLOPE_FLAT = EMA50[t] == EMA50[t - 3]
```

Reported per cell: fractions, run counts, median run lengths for POS/NEG,
and self-transition probabilities for POS/NEG.

### 3.3 Post-expansion follow-through (§7)

Expansion event mask:

```text
expansion[t] := range_bps[t] > 1.5 × rolling_median(range_bps[t-96..t-1])
```

Expansion-bar direction:

```text
bar_dir_up = close[t] >= open[t]
```

For each forward window `N ∈ {1, 2, 4, 8}` bars:

- `forward_return_bps[t, N] = (log(close[t+N]) - log(close[t])) × 1e4`,
- `same_direction_followthrough` if (bar_dir_up AND fr > 0) OR (bar_dir_down AND fr < 0),
- `opposite_direction_reversal` if (bar_dir_up AND fr < 0) OR (bar_dir_down AND fr > 0),
- Same-direction with magnitude thresholds 16 / 24 / 32 bps.

Comparison to unconditional reference: fraction of all bars where
`|forward_return_bps| > 16 bps` for the same forward window.

### 3.4 Directional sign persistence (§8)

For close-to-close log return `r[t] = log(close[t]) - log(close[t-1])`,
ignoring `r[t] == 0`:

- `frac_sign_repeats_next_k` for `k ∈ {1, 2, 4}` consecutive bars,
- Pearson autocorrelation of `r` at lags `1`, `2`, `4`.

### 3.5 Volatility-regime persistence (§9)

```text
high_vol[t] := atr_bps[t] > rolling_quantile_0.75(atr_bps[t-96..t-1])
```

Reported per cell: high-vol fraction, run count, median and p75 high-vol
run lengths, self-transition probability, and overlap counts of high-vol
bars with `UP` / `DOWN` / `MIXED` trend states.

### 3.6 Cost-adjusted continuation sufficiency (§10)

For each forward window `N ∈ {1, 2, 4, 8}` and each threshold
`T ∈ {16, 24, 32}` bps, fraction of bars where
`|forward_return_bps[t, N]| > T`, both unconditional and conditional on:

- `state[t] == UP`,
- `state[t] == DOWN`,
- `expansion[t]` (post-expansion).

### 3.7 Cross-symbol rankings (§11)

Per-interval rankings (low to high) for: median UP run length, median DOWN
run length, P(UP self-transition), P(DOWN self-transition), UP fraction,
DOWN fraction, P(high-vol self-transition), high-vol fraction,
frac_sign_repeats_1, lag-1 return autocorrelation. Per-interval rankings at
N=4 and N=8 for: same-direction follow-through, same-direction-with-mag
{16, 24, 32} bps. Per-interval rankings at N=4, threshold=16 bps for:
unconditional, UP-state, post-expansion absolute-move fractions.

All §11 rankings are substrate descriptions only. They do not select a
strategy symbol. They do not authorize a strategy spec.

## 4. Coverage Results

All 20 (symbol, interval) cells produced complete data over the analysis
window with **0 missing bars in span** for every cell. No datasets were
omitted. Phase 4ad Rule B1 was applied as the cross-symbol boundary
condition; SOL/XRP early-2022 archive gaps fall before `2022-04-03 00:00
UTC` and are therefore outside the analysis window by construction. No
flag was flipped, no manifest modified.

Bar counts per cell (full coverage):

```text
15m : 140 064 (BTC, ETH) ; 142 944 (SOL, XRP, ADA)
30m :  70 032 (BTC, ETH) ;  71 472 (SOL, XRP, ADA)
1h  :  35 736  (all 5 symbols at 1h ran through 2026-04-30 23:00 UTC)
4h  :   8 754 (BTC, ETH) ;   8 934 (SOL, XRP, ADA)
```

(BTC / ETH 30m / 4h end at 2026-03-31 because their `__v001` Phase 4i
normalized partitions stop there; BTC / ETH 1h continues to 2026-04-30
because Phase 4ac added 1h Phase 4i `__v001` extending later. This is a
data-availability detail, not a quality issue, and does not affect any
cross-symbol comparison or any §11 ranking, because all cells exceed the
warmup requirements for every reported metric.)

## 5. Trend-State Persistence Results

| symbol  | interval | frac_up | frac_down | up_run_med | down_run_med | P(UP self) | P(DOWN self) |
| ------- | -------- | ------- | --------- | ---------- | ------------ | ---------- | ------------ |
| BTCUSDT | 15m      | 0.333   | 0.313     | 5.0        | 4.0          | 0.927      | 0.924        |
| BTCUSDT | 30m      | 0.330   | 0.320     | 5.0        | 4.0          | 0.933      | 0.925        |
| BTCUSDT | 1h       | 0.342   | 0.312     | 4.0        | 5.0          | 0.936      | 0.931        |
| BTCUSDT | 4h       | 0.330   | 0.316     | 4.0        | 6.0          | 0.940      | 0.939        |
| ETHUSDT | 15m      | 0.324   | 0.319     | 4.0        | 4.0          | 0.926      | 0.928        |
| ETHUSDT | 30m      | 0.320   | 0.322     | 4.0        | 4.0          | 0.930      | 0.929        |
| ETHUSDT | 1h       | 0.312   | 0.332     | 5.0        | 4.0          | 0.936      | 0.927        |
| ETHUSDT | 4h       | 0.297   | 0.353     | 5.0        | 5.0          | 0.931      | 0.931        |
| SOLUSDT | 15m      | 0.311   | 0.335     | 4.0        | 5.0          | 0.927      | 0.932        |
| SOLUSDT | 30m      | 0.307   | 0.344     | 4.0        | 5.0          | 0.931      | 0.934        |
| SOLUSDT | 1h       | 0.309   | 0.348     | 5.0        | 5.0          | 0.935      | 0.936        |
| SOLUSDT | 4h       | 0.292   | 0.345     | 3.0        | 7.0          | 0.926      | 0.940        |
| XRPUSDT | 15m      | 0.301   | 0.333     | 4.0        | 4.0          | 0.919      | 0.923        |
| XRPUSDT | 30m      | 0.290   | 0.343     | 4.0        | 4.0          | 0.923      | 0.924        |
| XRPUSDT | 1h       | 0.281   | 0.355     | 4.0        | 5.0          | 0.923      | 0.930        |
| XRPUSDT | 4h       | 0.248   | 0.374     | 4.0        | 6.0          | 0.920      | 0.934        |
| ADAUSDT | 15m      | 0.292   | 0.353     | 4.0        | 4.0          | 0.923      | 0.927        |
| ADAUSDT | 30m      | 0.278   | 0.365     | 5.0        | 4.0          | 0.927      | 0.931        |
| ADAUSDT | 1h       | 0.258   | 0.384     | 4.0        | 5.0          | 0.932      | 0.932        |
| ADAUSDT | 4h       | 0.210   | 0.447     | 4.0        | 5.0          | 0.931      | 0.939        |

Interpretation (descriptive only):

- Self-transition probabilities for `UP` and `DOWN` are uniformly very high
  across all 20 cells: `P(UP self)` ranges 0.919–0.940 and `P(DOWN self)`
  ranges 0.923–0.940. This reflects an arithmetic property of slow-EMA
  state machines on fine bars — once the state is set it tends to persist
  for many bars before flipping — rather than a directional-edge property.
- Median run lengths are short (3–7 bars) across all symbols, intervals,
  and directions, despite the high self-transition probability. Mean run
  lengths are larger (≈ 13–17 bars) due to a long tail of long
  uninterrupted regimes (max runs reach 100–290 bars).
- BTC's clean trend bias from Phase 4ae appears as **balanced** UP/DOWN
  fractions (0.31–0.34 UP, 0.31–0.32 DOWN at all intervals) — Phase 4ae
  recorded that BTC sits "above EMA(50)" ~50–52% of the time and
  "EMA(50) > EMA(200)" ~50–52% of the time, which decomposes into ~33%
  UP, ~32% DOWN, ~35% MIXED here.
- ADA at 4h is sharply asymmetric: 0.21 UP vs 0.45 DOWN. ADA / XRP
  generally show DOWN dominance at 1h and 4h. SOL is intermediate. ETH at
  4h is mildly DOWN-dominant (0.297 UP vs 0.353 DOWN). This reflects the
  observed sample-period drift; **it is not predictive evidence**.
- The cross-symbol `P(UP self)` and `P(DOWN self)` rankings are
  essentially flat: BTC marginally edges out at the 4h boundary
  (`P(UP self)=0.940`, `P(DOWN self)=0.939`) but the spread across all
  five symbols at any interval is on the order of 1–2 percentage points.

Phase 4ae's cost-cushion ranking `SOL > ADA > XRP > ETH > BTC` and "BTC is
the most cleanly trending substrate by simple EMA regime proxies" are
**not** contradicted here — but they are also **not amplified** by trend
self-transition statistics. Trend continuity per se does not differentiate
the symbols.

These are descriptive regime-continuity metrics. They are NOT regime
filters, NOT entry rules, and NOT a strategy candidate.

## 6. EMA-Slope Persistence Results

| symbol  | interval | frac_pos | frac_neg | pos_med | neg_med | P(POS self) | P(NEG self) |
| ------- | -------- | -------- | -------- | ------- | ------- | ----------- | ----------- |
| BTCUSDT | 15m      | 0.511    | 0.489    | 9       | 8       | 0.950       | 0.948       |
| BTCUSDT | 30m      | 0.512    | 0.488    | 10      | 9       | 0.952       | 0.949       |
| BTCUSDT | 1h       | 0.512    | 0.488    | 9       | 9       | 0.953       | 0.951       |
| BTCUSDT | 4h       | 0.503    | 0.497    | 10      | 11      | 0.955       | 0.954       |
| ETHUSDT | 15m      | 0.506    | 0.494    | 9       | 9       | 0.951       | 0.950       |
| ETHUSDT | 30m      | 0.506    | 0.494    | 10      | 9       | 0.952       | 0.950       |
| ETHUSDT | 1h       | 0.502    | 0.498    | 9       | 10      | 0.951       | 0.951       |
| ETHUSDT | 4h       | 0.478    | 0.522    | 8       | 8       | 0.946       | 0.950       |
| SOLUSDT | 15m      | 0.492    | 0.508    | 8       | 9       | 0.950       | 0.952       |
| SOLUSDT | 30m      | 0.487    | 0.513    | 10      | 9       | 0.952       | 0.954       |
| SOLUSDT | 1h       | 0.486    | 0.514    | 9       | 10      | 0.952       | 0.954       |
| SOLUSDT | 4h       | 0.475    | 0.525    | 9       | 11      | 0.951       | 0.956       |
| XRPUSDT | 15m      | 0.491    | 0.509    | 8       | 9       | 0.946       | 0.948       |
| XRPUSDT | 30m      | 0.484    | 0.516    | 8       | 9       | 0.947       | 0.950       |
| XRPUSDT | 1h       | 0.479    | 0.521    | 9       | 10      | 0.947       | 0.951       |
| XRPUSDT | 4h       | 0.444    | 0.556    | 9.5     | 10      | 0.945       | 0.956       |
| ADAUSDT | 15m      | 0.482    | 0.518    | 8       | 9       | 0.947       | 0.951       |
| ADAUSDT | 30m      | 0.475    | 0.525    | 9       | 10      | 0.948       | 0.953       |
| ADAUSDT | 1h       | 0.458    | 0.542    | 9       | 10      | 0.948       | 0.956       |
| ADAUSDT | 4h       | 0.409    | 0.591    | 9       | 10      | 0.942       | 0.960       |

Interpretation (descriptive only):

- Slope-state self-transition probabilities are uniformly very high (0.94 –
  0.96 across all cells, both directions). This is again largely arithmetic:
  EMA slope at lag 3 changes sign infrequently because the EMA is smooth.
- POS/NEG fractions skew toward NEG for the alts, especially XRP and ADA at
  4h. This mirrors the trend-state DOWN dominance in §5 — the same
  underlying sample drift, expressed via a different lens.
- Median run lengths are ≈ 8–11 bars, consistent across symbols and
  intervals.

Discussion: this is descriptive continuity evidence only. **Phase 3w §7
EMA-slope governance is not altered by Phase 4af.** Phase 4af does not
propose or imply any EMA-slope-derived strategy rule.

## 7. Post-Expansion Follow-Through Results

Same-direction follow-through fractions, expansion threshold = 1.5 ×
rolling-median range, forward windows N ∈ {1, 2, 4, 8} bars.

| symbol  | interval | event_count | N=1 same-dir | N=2 same-dir | N=4 same-dir | N=8 same-dir |
| ------- | -------- | ----------- | ------------ | ------------ | ------------ | ------------ |
| BTCUSDT | 15m      | 34 006      | 0.464        | 0.463        | 0.470        | 0.473        |
| BTCUSDT | 30m      | 17 925      | 0.463        | 0.464        | 0.471        | 0.481        |
| BTCUSDT | 1h       |  9 355      | 0.460        | 0.460        | 0.474        | 0.480        |
| BTCUSDT | 4h       |  2 246      | 0.484        | 0.484        | 0.500        | 0.483        |
| ETHUSDT | 15m      | 32 593      | 0.458        | 0.460        | 0.469        | 0.474        |
| ETHUSDT | 30m      | 16 956      | 0.455        | 0.459        | 0.471        | 0.471        |
| ETHUSDT | 1h       |  8 973      | 0.454        | 0.462        | 0.468        | 0.482        |
| ETHUSDT | 4h       |  2 169      | 0.470        | 0.483        | 0.494        | 0.488        |
| SOLUSDT | 15m      | 29 504      | 0.467        | 0.467        | 0.477        | 0.478        |
| SOLUSDT | 30m      | 15 492      | 0.476        | 0.475        | 0.475        | 0.483        |
| SOLUSDT | 1h       |  7 932      | 0.466        | 0.467        | 0.482        | 0.485        |
| SOLUSDT | 4h       |  1 973      | 0.479        | 0.479        | 0.501        | 0.471        |
| XRPUSDT | 15m      | 30 376      | 0.454        | 0.459        | 0.461        | 0.469        |
| XRPUSDT | 30m      | 16 163      | 0.463        | 0.462        | 0.469        | 0.481        |
| XRPUSDT | 1h       |  8 332      | 0.459        | 0.463        | 0.466        | 0.473        |
| XRPUSDT | 4h       |  2 158      | 0.457        | 0.467        | 0.481        | 0.481        |
| ADAUSDT | 15m      | 28 705      | 0.455        | 0.452        | 0.465        | 0.475        |
| ADAUSDT | 30m      | 15 070      | 0.454        | 0.463        | 0.468        | 0.476        |
| ADAUSDT | 1h       |  7 760      | 0.461        | 0.465        | 0.465        | 0.478        |
| ADAUSDT | 4h       |  1 977      | 0.474        | 0.488        | 0.490        | 0.483        |

Interpretation (descriptive only):

- **Post-expansion same-direction follow-through is essentially at or
  marginally below 0.50 across the entire 5×4×4 grid (80 cells).** No cell
  exceeds 0.501. The closest to 0.50 are SOL 4h N=4 (0.501) and BTC 4h N=4
  (0.500); all others are 0.45–0.49. This means that **conditional on a
  large-range expansion bar, the next 1 / 2 / 4 / 8-bar move is roughly
  as likely to reverse direction as to continue.**
- The mild apparent lift toward 0.48–0.50 at N=4 / N=8 on 4h cells is
  partly because longer-horizon directional outcomes asymptotically
  symmetrize around 0.50 in the absence of a directional edge (mechanical:
  random sign in cumulative noise). It is not a same-direction signal.
- Same-direction-with-magnitude (>16 / 24 / 32 bps) frequencies *do* grow
  with N and with interval, but this growth tracks the unconditional
  reference frequency (Section 10) — i.e., it reflects movement magnitude
  scaling, not a same-direction-specific advantage.
- Reading the post-expansion table together with §10: post-expansion bars
  show somewhat **larger** absolute moves than unconditional bars (this
  is mechanical: by construction, expansion bars sit at the upper tail of
  range), but the **direction** of the larger move is essentially random.

This is a substantive Phase 4af descriptive finding:

```text
Substrate-level expansion-event same-direction follow-through is
essentially at or below 0.50 for every (symbol, interval, N) cell tested.
```

This is consistent with Phase 4l V2 and Phase 4r G1 outcomes at the
mechanism layer: a large-range expansion bar by itself is not predictive of
same-direction continuation in the substrate. **Phase 4af does not infer
strategy returns from this. Phase 4af does not authorize a strategy.**

## 8. Directional Sign Persistence Results

| symbol  | interval | sign_repeat_1 | sign_repeat_2 | sign_repeat_4 | lag1 autocorr | lag2    | lag4    |
| ------- | -------- | ------------- | ------------- | ------------- | ------------- | ------- | ------- |
| BTCUSDT | 15m      | 0.475         | 0.216         | 0.0400        | -0.007        | -0.010  | -0.002  |
| BTCUSDT | 30m      | 0.469         | 0.213         | 0.0402        | -0.014        | -0.006  | +0.001  |
| BTCUSDT | 1h       | 0.470         | 0.209         | 0.0379        | -0.009        | -0.004  | +0.003  |
| BTCUSDT | 4h       | 0.461         | 0.207         | 0.0400        |  0.000        | +0.005  | +0.006  |
| ETHUSDT | 15m      | 0.474         | 0.214         | 0.0396        |  0.000        | -0.010  | -0.001  |
| ETHUSDT | 30m      | 0.469         | 0.214         | 0.0411        | -0.003        | -0.008  | +0.004  |
| ETHUSDT | 1h       | 0.470         | 0.212         | 0.0397        | +0.005        | -0.006  | +0.004  |
| ETHUSDT | 4h       | 0.477         | 0.222         | 0.0453        | +0.001        | +0.021  | +0.001  |
| SOLUSDT | 15m      | 0.477         | 0.219         | 0.0428        | -0.015        | -0.006  | -0.005  |
| SOLUSDT | 30m      | 0.475         | 0.220         | 0.0439        | -0.019        | -0.017  | +0.000  |
| SOLUSDT | 1h       | 0.474         | 0.216         | 0.0417        | -0.009        | -0.014  | -0.003  |
| SOLUSDT | 4h       | 0.486         | 0.231         | 0.0499        | -0.003        | +0.007  | +0.016  |
| XRPUSDT | 15m      | 0.467         | 0.211         | 0.0396        | -0.022        | -0.015  | -0.006  |
| XRPUSDT | 30m      | 0.468         | 0.213         | 0.0406        | -0.012        | -0.018  | +0.003  |
| XRPUSDT | 1h       | 0.475         | 0.216         | 0.0413        | -0.005        | -0.006  | +0.010  |
| XRPUSDT | 4h       | 0.472         | 0.211         | 0.0380        | +0.009        | +0.004  | +0.015  |
| ADAUSDT | 15m      | 0.464         | 0.207         | 0.0395        | -0.019        | -0.020  | +0.004  |
| ADAUSDT | 30m      | 0.465         | 0.210         | 0.0411        | -0.040        | +0.004  | -0.004  |
| ADAUSDT | 1h       | 0.467         | 0.212         | 0.0396        | +0.004        | -0.013  | +0.015  |
| ADAUSDT | 4h       | 0.479         | 0.221         | 0.0467        | +0.017        | +0.012  | +0.009  |

Interpretation (descriptive only):

- `frac_sign_repeats_next_1` is consistently slightly **below** 0.50
  (range 0.461–0.486 across all 20 cells). Random-walk would yield
  exactly 0.50 (excluding zero-sign bars). Two consecutive repeats land
  ~0.21 (vs random 0.25); four consecutive repeats land ~0.04 (vs random
  ≈ 0.0625). All three rows of evidence are consistent with **bar-level
  return signs being marginally mean-reverting or roughly symmetric, not
  same-sign persistent**.
- Lag-1 return autocorrelation is near zero at every cell (range -0.040
  to +0.017). The largest negative autocorrelation is ADA 30m
  (-0.040). The largest positive autocorrelation is ADA 4h (+0.017).
  No cell shows lag-1 autocorrelation that meaningfully exceeds noise.
- Lag-2 and lag-4 autocorrelations are also near zero; ETH 4h lag-2
  (+0.021) and SOL 4h lag-4 (+0.016) are the visible outliers but remain
  small.

There is no bar-level directional persistence advantage on any substrate
at any of the four intervals tested. This is descriptive only.

## 9. Volatility-Regime Persistence Results

| symbol  | interval | frac_high_vol | high_vol_run_med | P(high_vol self) |
| ------- | -------- | ------------- | ---------------- | ---------------- |
| BTCUSDT | 15m      | 0.268         | 10               | 0.938            |
| BTCUSDT | 30m      | 0.301         | 12               | 0.942            |
| BTCUSDT | 1h       | 0.286         |  8               | 0.927            |
| BTCUSDT | 4h       | 0.266         |  5               | 0.917            |
| ETHUSDT | 15m      | 0.263         |  9               | 0.933            |
| ETHUSDT | 30m      | 0.289         | 10               | 0.932            |
| ETHUSDT | 1h       | 0.280         |  7               | 0.919            |
| ETHUSDT | 4h       | 0.280         |  6               | 0.917            |
| SOLUSDT | 15m      | 0.261         |  8               | 0.931            |
| SOLUSDT | 30m      | 0.288         |  9               | 0.932            |
| SOLUSDT | 1h       | 0.279         |  7               | 0.925            |
| SOLUSDT | 4h       | 0.270         |  4               | 0.917            |
| XRPUSDT | 15m      | 0.260         | 10               | 0.937            |
| XRPUSDT | 30m      | 0.278         |  9               | 0.938            |
| XRPUSDT | 1h       | 0.265         |  7               | 0.930            |
| XRPUSDT | 4h       | 0.261         |  8               | 0.933            |
| ADAUSDT | 15m      | 0.265         |  8               | 0.931            |
| ADAUSDT | 30m      | 0.279         |  8               | 0.933            |
| ADAUSDT | 1h       | 0.278         |  7               | 0.924            |
| ADAUSDT | 4h       | 0.271         |  4               | 0.915            |

High-vol overlap with trend states (counts):

| symbol  | interval | overlap_up | overlap_down | overlap_mixed |
| ------- | -------- | ---------- | ------------ | ------------- |
| BTCUSDT | 4h       | 817        | 854          | 604           |
| ETHUSDT | 4h       | 764        | 967          | 657           |
| SOLUSDT | 4h       | 848        | 940          | 575           |
| XRPUSDT | 4h       | 841        | 833          | 583           |
| ADAUSDT | 4h       | 679        | 1 033        | 645           |

Interpretation (descriptive only):

- High-vol regime fractions are uniform (≈ 0.26–0.30 across every cell),
  consistent with the construction: by definition the rolling-quantile
  threshold is the local 0.75 cut, so the high-vol fraction targets ~0.25
  in steady state with mild drift due to transient warmup and trend.
- Self-transition probabilities are uniformly high (0.91–0.94). High-vol
  regimes are persistent at the bar level.
- High-vol bars overlap meaningfully with both UP and DOWN states.
  Volatility regime is **not** a directional indicator; it is roughly
  state-agnostic at the substrate level. The 4h overlap counts are
  comparable across UP and DOWN for most symbols; ADA 4h skews toward
  DOWN-overlap (1 033 vs 679) consistent with §5.

Volatility regime is persistent but is not a directional edge. Phase 4af
does not propose any volatility-filter strategy and does not amend Phase
3w EMA-slope governance or any other lock.

## 10. Cost-Adjusted Continuation Sufficiency

Forward window N=4, threshold = 16 bps (round-trip §11.6 HIGH cost).

| symbol  | interval | uncond | UP-state | DOWN-state | post-expansion |
| ------- | -------- | ------ | -------- | ---------- | -------------- |
| BTCUSDT | 15m      | 0.581  | 0.585    | 0.603      | 0.677          |
| BTCUSDT | 30m      | 0.682  | 0.683    | 0.696      | 0.769          |
| BTCUSDT | 1h       | 0.765  | 0.771    | 0.771      | 0.834          |
| BTCUSDT | 4h       | 0.887  | 0.890    | 0.881      | 0.915          |
| ETHUSDT | 15m      | 0.670  | 0.669    | 0.692      | 0.744          |
| ETHUSDT | 30m      | 0.759  | 0.755    | 0.775      | 0.815          |
| ETHUSDT | 1h       | 0.827  | 0.829    | 0.826      | 0.870          |
| ETHUSDT | 4h       | 0.916  | 0.923    | 0.914      | 0.925          |
| SOLUSDT | 15m      | 0.794  | 0.805    | 0.795      | 0.841          |
| SOLUSDT | 30m      | 0.852  | 0.860    | 0.850      | 0.882          |
| SOLUSDT | 1h       | 0.895  | 0.903    | 0.891      | 0.917          |
| SOLUSDT | 4h       | 0.953  | 0.951    | 0.955      | 0.964          |
| XRPUSDT | 15m      | 0.729  | 0.746    | 0.731      | 0.789          |
| XRPUSDT | 30m      | 0.801  | 0.823    | 0.797      | 0.852          |
| XRPUSDT | 1h       | 0.859  | 0.881    | 0.848      | 0.886          |
| XRPUSDT | 4h       | 0.928  | 0.938    | 0.921      | 0.952          |
| ADAUSDT | 15m      | 0.772  | 0.778    | 0.773      | 0.820          |
| ADAUSDT | 30m      | 0.835  | 0.846    | 0.834      | 0.874          |
| ADAUSDT | 1h       | 0.883  | 0.899    | 0.876      | 0.906          |
| ADAUSDT | 4h       | 0.944  | 0.949    | 0.935      | 0.954          |

Interpretation (descriptive only):

- Most bars on most symbols at most intervals show |forward 4-bar move| >
  16 bps unconditionally (range 0.58–0.95 across the 5×4 grid), reflecting
  Phase 4ae's cost-cushion ranking and confirming that **substrate
  movement magnitude exceeds round-trip cost frequently**.
- The lift from `unconditional` to `post-expansion` is small but
  consistent (≈ +5–10 percentage points), a mechanical consequence of
  expansion-bar selection sitting in the upper tail of range.
- The `UP-state` and `DOWN-state` conditional fractions are nearly
  identical to the unconditional fraction at every cell (within ±2
  percentage points). **Trend-state conditioning provides no
  cost-adjusted directional advantage** in this descriptive view.
- SOL leads at every interval (0.79 / 0.85 / 0.90 / 0.95) and BTC
  trails 15m / 30m (0.58 / 0.68) but converges by 1h / 4h (0.77 / 0.89).
  This is consistent with Phase 4ae's cost-cushion ranking (SOL > ADA >
  XRP > ETH > BTC) at coarser intervals.
- The 16-bps threshold is movement-sufficiency context, **not** an entry
  signal. A bar where |forward move| > 16 bps is not equivalent to a
  profitable trade; the direction is not predicted (see §7 same-direction
  follow-through ≤ 0.50).

These thresholds reflect movement magnitude relative to §11.6 HIGH cost
context. They are **not** target/stop levels and are not strategy
parameters.

## 11. Cross-Symbol Feasibility Summary

Substrate-level descriptive comparison across the dimensions explored:

### 11.1 Where symbols differ meaningfully

- **Movement magnitude / cost cushion** (Phase 4ae and §10):
  `SOL > ADA > XRP > ETH > BTC` at finer intervals; convergence at 4h.
- **Trend-state symmetry** (§5): BTC has the most balanced UP/DOWN
  fractions; ADA / XRP have the strongest DOWN dominance over the
  analysis window. This reflects the sample period.

### 11.2 Where symbols look essentially the same

- **Trend-state self-transition probabilities** (§5): all 20 cells fall
  in 0.92–0.94. No symbol has a meaningful trend-continuity edge.
- **EMA-slope self-transition probabilities** (§6): all 20 cells fall in
  0.94–0.96. No symbol has a meaningful slope-persistence edge.
- **Post-expansion same-direction follow-through** (§7): all 80 cells at
  or below 0.501 across N ∈ {1, 2, 4, 8}. **No symbol shows a
  same-direction follow-through bias.**
- **Bar-level sign persistence** (§8): all 20 cells slightly below 0.50
  for `frac_sign_repeats_next_1`; lag-1 autocorrelation near zero on all
  cells. **No symbol shows bar-level directional persistence.**
- **High-vol self-transition probabilities** (§9): all 20 cells fall in
  0.91–0.94. High-vol persistence is uniform.
- **Trend-state conditional cost-adjusted continuation** (§10): UP-state
  and DOWN-state conditional fractions are within ±2 percentage points
  of unconditional at every cell. **Trend conditioning does not provide a
  cost-adjusted directional advantage.**

### 11.3 Whether Phase 4ae's cost-cushion ranking is supported

Phase 4ae recorded `SOL > ADA > XRP > ETH > BTC` cost cushion. Phase 4af
§10 shows the same ranking at coarser intervals: SOL leads, BTC trails at
15m / 30m, with convergence by 4h. **Phase 4af descriptively confirms
Phase 4ae's substrate-feasibility cost-cushion finding.** It does NOT
broaden Phase 4ae findings beyond descriptive substrate-feasibility
evidence.

### 11.4 Whether 1h / 4h appear more or less promising than 15m / 30m

- **More promising at 1h / 4h**: cost-adjusted absolute movement (§10),
  which approaches 0.83–0.95 by 4h on every symbol; this means substrate
  movement reliably exceeds round-trip cost on coarser intervals.
- **Not more promising at 1h / 4h**: same-direction follow-through (§7)
  remains at or below 0.50, so the additional movement is direction-free.
  Bar-level sign persistence (§8) does not improve at coarser intervals.
- **Less promising at 1h / 4h for symmetry-sensitive analyses**: alts
  (XRP, ADA) become increasingly DOWN-dominant at 4h, which is sample
  drift, not predictive evidence; a strategy depending on UP/DOWN
  balance might be sensitive to this.

### 11.5 Whether any symbol looks promising enough for future hypothesis discovery

No symbol shows a clean cost-cushion plus regime-persistence plus
post-expansion-follow-through advantage on the substrate. The closest
"interesting" combination is:

```text
SOL at 1h / 4h has:
  - strongest cost cushion (Phase 4ae + §10),
  - high trend-state self-transition (≈ 0.93 at 1h, 0.94 at 4h DOWN),
  - high-vol persistence ≈ 0.92 (≈ 0.92 4h, ≈ 0.93 1h),
  - but post-expansion same-direction follow-through ≤ 0.50,
  - and bar-level sign repeats ≈ 0.474–0.486 (no advantage).
```

**This is not strong enough to displace remain-paused.** A future
fresh-hypothesis discovery memo would need to identify a *non-substrate*
mechanism (something other than substrate persistence per se) — e.g., a
cleanly defined external-context signal, cross-asset signal, or
instrument-microstructure signal — and would still face the project's
six-failure rejection topology (R2 cost-fragility; F1 catastrophic-floor;
D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1
regime-gate-meets-setup intersection sparseness; C1 fires-and-loses /
contraction anti-validation).

### 11.6 What Phase 4af does NOT conclude

- Phase 4af does **not** name a candidate symbol for strategy work.
- Phase 4af does **not** name a candidate interval for strategy work.
- Phase 4af does **not** assert that any (symbol, interval) pair has
  exploitable directional persistence.
- Phase 4af does **not** assert that any (symbol, interval) pair is
  cost-survivable as a strategy substrate.
- Phase 4af does **not** authorize a strategy spec.
- Phase 4af does **not** authorize a backtest.
- Phase 4af does **not** authorize live work.

## 12. Implications for Future Research

Possible future operator decisions, in order of preference:

```text
Option A — remain paused (primary recommendation).
Option B — future narrower follow-up feasibility memo
           (only if separately authorized and clearly framed
            so as to not become a strategy spec).
Option C — future docs-only fresh-hypothesis discovery memo
           (only if evidence is strong enough and the memo clearly
            states why it is not old-strategy rescue).
Option D — mark-price stop-domain feasibility under Phase 4ad Rule A
           (only if needed and separately authorized).
```

**Phase 4af does not authorize any successor phase.** Phase 4af does not
authorize Phase 4ag, Phase 5, Phase 4 canonical, paper/shadow,
live-readiness, deployment, exchange-write, MCP, Graphify, `.mcp.json`,
or credentials.

## 13. Recommendation

Given:

- post-expansion same-direction follow-through ≤ 0.50 universally (§7),
- bar-level sign persistence near zero universally (§8),
- trend-state and slope self-transition probabilities high but uniform
  across symbols and intervals — no differentiating edge (§5, §6),
- volatility regime persistent but state-agnostic in direction (§9),
- cost-adjusted absolute movement frequent but direction-free (§10),
- Phase 4ae cost-cushion ranking confirmed but unaccompanied by a
  same-direction edge (§11.3),

Phase 4af recommends:

```text
Option A — remain paused.
```

Phase 4af explicitly does **not** recommend a fresh-hypothesis discovery
memo at this time. The substrate-level descriptive evidence does not
support a directional thesis; substrate persistence per se is not a
mechanism. The project's six-failure rejection topology suggests that
adding another substrate-driven candidate to the ledger would not
produce different outcomes without a categorically distinct mechanism, and
no such mechanism is implied by Phase 4af's analysis.

If the operator chooses to continue, **Option B (narrower follow-up
feasibility memo)** is the procedurally cleanest secondary alternative,
provided it is framed strictly as descriptive feasibility (not strategy
discovery) and predeclares its scope before any data is touched.

**Phase 4af does not authorize any successor phase.**

## 14. Preserved Locks and Boundaries

Retained verdicts (preserved verbatim):

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- 5m thread remains CLOSED operationally.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

Project locks (preserved verbatim):

- §11.6 HIGH cost = 8 bps per side unchanged.
- §1.7.3 project-level locks unchanged:
  - 0.25% risk;
  - 2× leverage;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 preserved.
- Phase 3v §8 preserved.
- Phase 3w §6 / §7 / §8 preserved.
- Phase 4j §11 preserved.
- Phase 4k preserved.
- Phase 4p preserved.
- Phase 4q preserved.
- Phase 4v preserved.
- Phase 4w preserved.

Recommendation status:

- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence.
- Phase 4ad future-use rules applied prospectively only.
- Phase 4ae findings remain descriptive substrate-feasibility evidence
  only.

## 15. Explicit Non-Authorization Statement

Phase 4af does NOT authorize:

```text
Phase 4ag
Phase 5
Phase 4 canonical
any successor phase
data acquisition
data download
API calls
endpoint calls
data modification
manifest creation
manifest modification
v003 or any dataset version
backtests
strategy diagnostics
Q1-Q7 rerun
strategy PnL
entry / exit strategy returns
optimization
threshold selection for a future strategy
new strategy
fresh-hypothesis memo
hypothesis-spec memo
strategy-spec memo
backtest-plan memo
implementation
old-strategy rescue
R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime
V1-D1 / F1-D1 / any cross-strategy hybrid
paper / shadow
live-readiness
deployment
production keys
authenticated APIs
private endpoints
public endpoint calls in code
user stream
WebSocket
exchange-write
MCP
Graphify
`.mcp.json`
credentials
```

The recommended state remains:

```text
remain paused unless the operator separately authorizes a future phase.
```
