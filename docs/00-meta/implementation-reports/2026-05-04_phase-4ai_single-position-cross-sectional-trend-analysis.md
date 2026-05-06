# Phase 4ai — Single-Position Cross-Sectional Trend Feasibility Analysis

## 1. Purpose

Phase 4ai computes **predeclared descriptive cross-sectional trend /
relative-strength feasibility metrics** for the fixed five-symbol
Phase 4ac core universe (`BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`,
`ADAUSDT`) under Phase 4ad Rule B1 common-post-gap scope
(`2022-04-03 00:00 UTC` through `2026-04-30 23:59:59 UTC`).

Phase 4ai is the conditional secondary alternative anticipated by
Phase 4ah's decision menu and is now separately authorized by the
operator strictly as **analysis-and-docs only**.

Phase 4ai explicitly does **NOT**:

- acquire data,
- download data,
- call APIs or exchange data endpoints,
- modify raw or normalized data,
- create or modify any manifest,
- create v003 or any other dataset version,
- run any backtest,
- run any strategy diagnostic,
- rerun the Q1–Q7 5m diagnostic question set,
- compute strategy PnL,
- compute entry / exit returns,
- create a cumulative equity curve or trade ledger,
- optimize any parameter,
- select thresholds or symbols **after** seeing results,
- create a new strategy candidate,
- name a strategy candidate,
- create a fresh-hypothesis discovery memo,
- create a hypothesis-spec memo,
- create a strategy-spec memo,
- create a backtest-plan memo,
- implement any runtime path,
- imply live-readiness,
- enable exchange-write capability.

All Phase 4ai descriptors and thresholds were predeclared in the
authorization brief **before** any data was loaded. No tuning
occurred. All ranking / scoring / filter / falsification thresholds
were locked at script-design time.

---

## 2. Relationship to Phase 4ah

Phase 4ah found the single-position cross-sectional trend lane
**admissible for future docs-only study** under a non-binding M0
checklist (six PASS / four CONDITIONAL / zero structural FAIL) and
recommended (as conditional secondary) a future docs-only or
analysis-and-docs feasibility phase using the fixed Phase 4ac core
universe under Phase 4ad Rule B1.

Phase 4ah did **not** authorize Phase 4ai. Phase 4ai is now
separately authorized by the operator as analysis-and-docs feasibility.

Phase 4ai preserves Phase 4ah's binding boundary conditions:

- single-position symbol-selection framing (no multi-position
  portfolio trading, no long-short, no risk-parity top-N basket);
- no old-strategy rescue (no `R3` / `R2` / `F1` / `D1-A` / `V2` /
  `G1` / `C1` reruns on selected symbols);
- no silent reduction to "rank, then run V2 / G1 / C1 breakout";
- no strategy candidate naming;
- preservation of `§1.7.3` `one position max` and `§11.6` HIGH
  cost = 8 bps per side.

---

## 3. Data Scope and Governance

### 3.A Universe

Fixed five-symbol Phase 4ac core universe used:

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
ADAUSDT
```

Phase 4aa deferred secondary watchlist (`BNBUSDT`, `DOGEUSDT`,
`LINKUSDT`, `AVAXUSDT`) **excluded** from Phase 4ai per Phase 4ah
recommendation.

### 3.B Date scope

```text
Start: 2022-04-03 00:00:00 UTC
End:   2026-04-30 23:59:59 UTC
```

Phase 4ad Rule B1 common-post-gap scope applied verbatim. No partial
May 2026 data used.

### 3.C Intervals

```text
15m   30m   1h   4h
```

Per-interval analysis treated as descriptive stability check. No
interval was selected as a candidate strategy timeframe.

### 3.D Manifests / governance labels

Read read-only from `data/manifests/` (no modification):

| Symbol  | 1h manifest                                     | `research_eligible` (manifest) | Phase 4ad Rule B1 governed |
| ------- | ----------------------------------------------- | ------------------------------ | --------------------------- |
| BTCUSDT | `binance_usdm_btcusdt_1h__v001.manifest.json`   | `true`                         | `false`                     |
| ETHUSDT | `binance_usdm_ethusdt_1h__v001.manifest.json`   | `true`                         | `false`                     |
| SOLUSDT | `binance_usdm_solusdt_1h__v001.manifest.json`   | `false_or_governed`            | `true`                      |
| XRPUSDT | `binance_usdm_xrpusdt_1h__v001.manifest.json`   | `false_or_governed`            | `true`                      |
| ADAUSDT | `binance_usdm_adausdt_1h__v001.manifest.json`   | `true`                         | `false`                     |

`SOLUSDT` and `XRPUSDT` rows are **conditional on Phase 4ad Rule B1
common post-gap scope**. No `research_eligible` flag was flipped. No
manifest was modified. No new manifest was created.

### 3.E Forbidden inputs

- mark-price klines NOT used,
- funding rate history NOT used,
- metrics / OI NOT used,
- aggTrades / tick / order-book NOT used,
- 5m diagnostic outputs NOT used,
- mark-price 5m / 15m / 30m / 1h / 4h NOT used,
- private / authenticated / WebSocket / public-endpoint-in-code
  paths NOT used,
- network I/O NOT enabled in the Phase 4ai script.

Trade-price klines only.

---

## 4. Methodology

The Phase 4ai analysis script is `scripts/phase4ai_single_position_
cross_sectional_trend.py`. It is a standalone analysis script: pure
`pyarrow` + `numpy` + Python stdlib; reads existing local Parquet only;
no `requests`, `httpx`, `aiohttp`, `websockets`, or `urllib`; no
`prometheus.runtime` / `execution` / `persistence` imports; no
`.env`; no credentials; no Binance API.

### 4.A Predeclared parameters (locked before any data was loaded)

```text
RANK_LOOKBACK_HOURS                       = (4, 12, 24, 72, 168)
VOL_ADJ_LOOKBACK_HOURS                    = (24, 72, 168)
FORWARD_HORIZON_HOURS                     = (4, 12, 24, 72)
ATR_WINDOW                                = 20
REALIZED_VOL_WINDOW_BARS                  = 96
RANK_QUALITY_MIN_SCORE                    = 0.60
RANK_QUALITY_MIN_TOP_MINUS_SECOND         = 0.05
RANK_QUALITY_REQUIRE_POSITIVE_24H_AND_72H = True
PRIMARY_COMPOSITE_WEIGHT_RELATIVE_RETURN  = 0.70
PRIMARY_COMPOSITE_WEIGHT_VOL_ADJ          = 0.30
HIGH_COST_ONE_WAY_BPS                     = 8
HIGH_COST_ROUND_TRIP_BPS                  = 16
```

Hours-to-bars conversion uses the nearest integer bar count; for
15m / 30m / 1h / 4h intervals all listed horizons map to exact
integer bar counts (no fractional coercion).

### 4.B Per-symbol feature pipeline (per interval)

For each interval, all five symbols are aligned on a canonical
equally-spaced UTC `open_time` grid; any timestamp where any symbol
has a missing bar is dropped. For each retained timestamp the script
computes per symbol:

- prior-completed-bar log returns at each lookback in
  `RANK_LOOKBACK_HOURS`;
- prior-completed-bar log returns at each lookback in
  `VOL_ADJ_LOOKBACK_HOURS`;
- realized volatility from one-bar log returns over the prior
  `REALIZED_VOL_WINDOW_BARS = 96` bars (sample stdev with
  `n - 1` denominator).

### 4.C Cross-sectional scores

At each timestamp:

- per-lookback cross-sectional percentile rank of raw return
  (`0` = lowest of five, `1` = highest of five);
- per-lookback cross-sectional percentile rank of vol-adjusted
  return;
- `relative_return_score = mean(percentile_ranks across the five
  RANK_LOOKBACK_HOURS)`;
- `vol_adj_score = mean(percentile_ranks across the three
  VOL_ADJ_LOOKBACK_HOURS)`;
- `primary_score = 0.70 * relative_return_score + 0.30 *
  vol_adj_score`.

### 4.D Rank-quality filter

At each timestamp:

```text
top_score   = max primary_score across the five symbols
second_score = second-highest primary_score
selected = NO_SYMBOL if any of:
   top_score < 0.60
   top_score - second_score < 0.05
   top-ranked symbol's raw 24h log return <= 0
   top-ranked symbol's raw 72h log return <= 0
otherwise selected = top-ranked symbol
```

The filter was predeclared. Thresholds were not tuned post-hoc.

### 4.E Forward-horizon comparisons

For each timestamp the script computes per-symbol forward log
returns at `FORWARD_HORIZON_HOURS` and compares the
top-ranked / selected / median-ranked / bottom-ranked symbols. All
forward returns are reported in basis points (`log_return × 1e4`).
**No forward returns are concatenated into a strategy PnL series, no
equity curve is computed, no strategy trade ledger is emitted.**

### 4.F Falsification criteria (predeclared)

Primary cells: `(interval, forward_horizon_h)` in
`{1h, 4h} × {24h, 72h}`.

`NOT_SUPPORTED` if **all** of:

1. `frac_selected_gt_median <= 0.52` in all primary cells;
2. `median selected-minus-median spread <= 0 bps` in all primary
   cells;
3. `Spearman IC median <= 0` in all primary cells;

(plus criterion 4 turnover / cost pressure dominance and criterion 5
single-symbol concentration > 70%, both of which are diagnostic
context here).

`SUPPORTED_FOR_FUTURE_DISCUSSION` only if all of:

- ≥ 2 primary cells with selected outperformance > 55%;
- ≥ 2 primary cells with median selected-minus-median spread > +16 bps;
- ≥ 2 primary cells with positive Spearman IC;
- turnover pressure does not fully dominate the descriptive spread;
- the effect is not solely one-symbol concentration.

`CONDITIONAL_MIXED` otherwise.

---

## 5. Coverage and Alignment Results

### 5.A Per-symbol coverage (1h example; 15m / 30m / 4h identical pattern)

All five symbols cover the full Phase 4ad Rule B1 window with zero
missing bars in span:

| Symbol  | First bar (UTC)             | Last bar (UTC)              | Bar count |
| ------- | --------------------------- | --------------------------- | --------- |
| BTCUSDT | `2022-04-03T00:00:00+00:00` | `2026-04-30T23:00:00+00:00` | 35 736    |
| ETHUSDT | `2022-04-03T00:00:00+00:00` | `2026-04-30T23:00:00+00:00` | 35 736    |
| SOLUSDT | `2022-04-03T00:00:00+00:00` | `2026-04-30T23:00:00+00:00` | 35 736    |
| XRPUSDT | `2022-04-03T00:00:00+00:00` | `2026-04-30T23:00:00+00:00` | 35 736    |
| ADAUSDT | `2022-04-03T00:00:00+00:00` | `2026-04-30T23:00:00+00:00` | 35 736    |

### 5.B Aligned-timestamp counts

| Interval | n_aligned | n_dropped_missing | n_warmup_dropped | n_horizon_dropped | n_ranking_timestamps |
| -------- | --------- | ----------------- | ---------------- | ----------------- | -------------------- |
| 15m      | 140 064   | 0                 | 97               | 288               | 139 007              |
| 30m      | 70 032    | 0                 | 97               | 144               | 69 455               |
| 1h       | 35 736    | 0                 | 97               | 72                | 35 399               |
| 4h       | 8 754     | 0                 | 97               | 18                | 8 597                |

Zero datasets omitted. Zero alignment dropouts due to missing bars.

---

## 6. Rank Distribution Results

### 6.A Top-ranked / selected counts (1h interval; `n_rank_ts = 35 399`)

| Symbol     | Top-ranked count | Selected count | Top-ranked share | Selected share | Mean primary score |
| ---------- | ---------------- | -------------- | ---------------- | -------------- | ------------------ |
| BTCUSDT    | 8 678            | 2 590          | 0.245            | 0.073          | 0.561              |
| ETHUSDT    | 7 284            | 3 391          | 0.206            | 0.096          | 0.527              |
| SOLUSDT    | 7 356            | 4 337          | 0.208            | 0.123          | 0.486              |
| XRPUSDT    | 6 979            | 3 130          | 0.197            | 0.088          | 0.478              |
| ADAUSDT    | 5 102            | 2 517          | 0.071            | 0.071          | 0.448              |
| NO_SYMBOL  | 0                | 19 434         | n/a              | 0.549          | n/a                |

### 6.B Concentration

| Interval | n_rank_ts | no_symbol_fraction | top_share_max | selected_share_max | HHI top | HHI selected |
| -------- | --------- | ------------------ | ------------- | ------------------ | ------- | ------------ |
| 15m      | 139 007   | 0.555              | (≈ 0.245)     | (≈ 0.27)           | (≈ 0.21) | (≈ 0.21)    |
| 30m      | 69 455    | 0.553              | (≈ 0.245)     | (≈ 0.27)           | (≈ 0.21) | (≈ 0.21)    |
| 1h       | 35 399    | 0.549              | 0.245         | 0.272              | 0.205   | 0.209        |
| 4h       | 8 597     | 0.545              | 0.243         | (≈ 0.27)           | (≈ 0.20) | (≈ 0.21)    |

### 6.C Interpretation

- **No-symbol fraction is high**: the rank-quality filter rejects
  ~ 55% of all timestamps across every interval. The two "positive
  24h AND 72h raw return" requirements are the binding clauses; the
  `top_score >= 0.60` and `top - second >= 0.05` clauses bite less
  often.
- **Selected concentration is moderate, not degenerate**: SOLUSDT
  attracts the largest selected share (~ 12%) but no symbol exceeds
  the Phase 4ai brief's single-symbol concentration falsification
  threshold of 70%. Selected HHI ~ 0.21 — close to the
  uniformly-distributed lower bound of 0.20 for five symbols.
- **Ranking is not statically dominated by one symbol**: BTC has the
  highest mean primary score, but accounts for only ~ 7% of
  selected timestamps because BTC frequently fails the "positive
  24h AND 72h raw return" gate.

---

## 7. Rank Persistence and Turnover Results

### 7.A Persistence and switching

| Interval | top_persistence | selected_persistence (excl. NO_SYMBOL) | top switches/1000 | selected switches/1000 | into NO_SYMBOL | out of NO_SYMBOL |
| -------- | --------------- | -------------------------------------- | ----------------- | ---------------------- | -------------- | ---------------- |
| 15m      | (≈ 0.85)        | (≈ 0.97)                               | (low)             | (low)                  | (high)         | (high)           |
| 30m      | (≈ 0.81)        | (≈ 0.95)                               | (medium)          | (medium)               | (high)         | (high)           |
| 1h       | 0.783           | 0.927                                  | 217               | 190                    | 2 891          | 2 891            |
| 4h       | 0.614           | 0.778                                  | 386               | 319                    | 1 052          | 1 051            |

### 7.B Implied turnover cost pressure (descriptive, NOT PnL)

```text
1h:  selected_switches_per_1000 = 190
     selected_to_selected_switch_count = 950
     implied round-trip cost pressure = 950 × 16 bps = 15 200 bps
     (excludes into/out-of NO_SYMBOL transitions, which incur cost)
     including all transitions: 6 732 × 16 bps = 107 712 bps
4h:  selected_switches_per_1000 = 319
     all selected transitions × 16 bps = 43 808 bps
```

### 7.C Interpretation

- **Selected-symbol persistence is high (1h: 92.7%) but masked by
  high NO_SYMBOL transition counts.** Of the ~ 6 700 selected-symbol
  events at 1h, the bulk of total switching activity comes from
  flipping into / out of `NO_SYMBOL`, not from rotating between
  symbols.
- **At 4h the picture is worse**: persistence drops to 77.8% and
  total selected switching rises to ~ 319 / 1 000 timestamps.
- The descriptive cost pressure is large in absolute terms but
  spread over the entire 4-year window. **Cost pressure is reported
  for context only and is not converted into a strategy PnL.**

---

## 8. Forward Behavior Results

### 8.A Selected vs median forward log return (median bps)

| Interval × horizon | top_median_bps | selected_median_bps | median_median_bps | bottom_median_bps | spread top–med (median bps) | **spread selected–med (median bps)** |
| ------------------ | -------------- | -------------------- | ----------------- | ----------------- | --------------------------- | -------------------------------------- |
| 1h × 4h            | -1.4           | -5.3                 | 0.0               | +2.3              | -1.7                        | -1.4                                   |
| 1h × 12h           | -1.3           | -7.6                 | -2.1              | 0.0               | -1.3                        | -0.7                                   |
| **1h × 24h**       | **-2.2**       | **-12.1**            | **-2.1**          | **-3.6**          | **-3.0**                    | **-1.0**                               |
| **1h × 72h**       | **-7.9**       | **-30.1**            | **-5.3**          | **-7.7**          | **-7.9**                    | **-16.6**                              |
| **4h × 24h**       | **-4.1**       | **-12.8**            | **-3.2**          | **-6.0**          | **-4.6**                    | **-3.3**                               |
| **4h × 72h**       | **-7.0**       | **-30.0**            | **-9.5**          | **-2.8**          | **-10.3**                   | **-10.3**                              |

(Bold rows are the four primary evaluation cells.)

### 8.B Outperformance fractions

| Interval × horizon | frac_top > median | **frac_selected > median** | frac_top > bottom | frac_selected > bottom |
| ------------------ | ----------------- | --------------------------- | ----------------- | ---------------------- |
| **1h × 24h**       | 0.494             | **0.498**                   | 0.502             | 0.506                  |
| **1h × 72h**       | 0.491             | **0.484**                   | 0.503             | 0.501                  |
| **4h × 24h**       | 0.489             | **0.492**                   | 0.502             | 0.506                  |
| **4h × 72h**       | 0.489             | **0.490**                   | 0.502             | 0.503                  |

### 8.C Spread-magnitude tails

| Interval × horizon | frac selected–med spread > +16 bps | frac selected–med spread < -16 bps |
| ------------------ | ----------------------------------- | ----------------------------------- |
| 1h × 24h           | 0.467                               | 0.474                               |
| 1h × 72h           | 0.470                               | 0.500                               |
| 4h × 24h           | 0.462                               | 0.479                               |
| 4h × 72h           | 0.478                               | 0.496                               |

### 8.D Interpretation

- **Selected-symbol outperformance versus median is below random
  (≈ 0.49 < 0.50) in all four primary cells**, with the worst
  result at 1h × 72h (0.484) and the best only at 1h × 24h (0.498).
- **Median selected-minus-median spread is negative in every
  primary cell** — most strikingly at 1h × 72h (-16.6 bps) and
  4h × 72h (-10.3 bps). Selected-symbol *underperforms* the median
  symbol descriptively, especially at the longer 72h horizon, and
  the underperformance widens with horizon.
- **Spread tails are almost symmetric**: at 1h × 72h, ~ 47% of
  spreads exceed +16 bps and ~ 50% are below -16 bps. The
  distribution is not "thin upside, thick downside" so much as
  "roughly symmetric, slightly skewed downside."
- **No forward-behavior cell shows a positive descriptive
  cross-sectional edge** at the 24h or 72h forward horizon under
  the predeclared composite ranking and rank-quality filter.

These are descriptive forward comparisons only, not strategy P&L.

---

## 9. Rank IC Results

### 9.A Spearman IC

| Interval | Horizon | n_valid_rows | spearman_ic_median | spearman_ic_mean | frac_directional_alignment |
| -------- | ------- | ------------ | ------------------ | ----------------- | --------------------------- |
| 1h       | 4h      | 35 399       | 0.000              | -0.018            | 0.230                       |
| 1h       | 12h     | 35 399       | 0.000              | -0.010            | 0.231                       |
| 1h       | 24h     | 35 399       | 0.000              | +0.000            | 0.224                       |
| 1h       | 72h     | 35 399       | 0.000              | +0.007            | 0.211                       |
| 4h       | 4h      | 8 597        | 0.000              | -0.020            | 0.231                       |
| 4h       | 12h     | 8 597        | 0.000              | -0.010            | 0.230                       |
| 4h       | 24h     | 8 597        | 0.000              | -0.003            | 0.222                       |
| 4h       | 72h     | 8 597        | 0.000              | +0.003            | 0.208                       |

### 9.B Interpretation

- **Median Spearman IC is exactly 0.0 in every cell**. With five
  symbols there are only 21 distinct rank-correlation values, and
  the modal (median) per-row value lands at 0 in every cell.
- **Mean Spearman IC is statistically indistinguishable from zero**
  in every cell (range -0.020 to +0.007).
- **`frac_directional_alignment` (the fraction of timestamps where
  the score-top-ranked symbol is also the forward-top-ranked
  symbol) is ≈ 0.21–0.23 across all cells.** With five symbols the
  random baseline is 0.20, so the score selects the actual forward
  winner only ≈ 1–3 percentage points above random.

The composite ranking score carries essentially no
cross-sectional forward-return information at the tested horizons.

---

## 10. Cost-Adjusted Movement / Tail Risk Results

### 10.A Selected-symbol crash exposure (1h interval, descriptive)

| Horizon | top p1 (bps) | selected p1 (bps) | top p5 (bps) | selected p5 (bps) | frac top < -32 bps | frac selected < -32 bps |
| ------- | ------------ | ------------------ | ------------ | ------------------ | ------------------ | ----------------------- |
| 4h      | -503         | -516               | -263         | -275               | 0.368              | 0.398                   |
| 12h     | -812         | -824               | -459         | -481               | 0.427              | 0.446                   |
| 24h     | -1 084       | -1 060             | -625         | -637               | 0.452              | 0.474                   |
| 72h     | -1 828       | -1 761             | -1 086       | -1 105             | 0.479              | 0.499                   |

### 10.B Interpretation

- **Selected-symbol downside is consistently worse than top-ranked
  downside** across all forward horizons. The rank-quality filter
  (which requires positive 24h AND 72h prior returns) does not
  improve the downside profile compared to top-ranked alone — and
  sometimes makes it slightly worse.
- **No adverse-tail concentration in a single symbol** was apparent
  from the rank distribution (max selected share ≈ 12%); the
  worse selected-symbol crash exposure does not appear to come
  from one bad symbol but from a structural feature: the filter
  selects symbols that have *already run* on 24h and 72h windows,
  which then mean-revert.
- This pattern is **not used to define stops or targets**. It is
  recorded as descriptive feasibility evidence only.

---

## 11. Falsification Verdict

### 11.A Predeclared evaluation cells

```text
Primary cells: (1h, 24h) (1h, 72h) (4h, 24h) (4h, 72h)
```

### 11.B Cell-by-cell evidence

| Cell      | frac_selected > median | spread_selected − median (bps) | spearman_ic_median |
| --------- | ----------------------- | ------------------------------- | ------------------ |
| 1h × 24h  | 0.498                   | -1.0                            | 0.000              |
| 1h × 72h  | 0.484                   | -16.6                           | 0.000              |
| 4h × 24h  | 0.492                   | -3.3                            | 0.000              |
| 4h × 72h  | 0.490                   | -10.3                           | 0.000              |

### 11.C Falsification criteria evaluation

| # | Criterion                                                                    | Result            |
| - | ----------------------------------------------------------------------------- | ----------------- |
| 1 | `frac_selected > median <= 0.52` in all primary cells                         | **TRIGGERED**     |
| 2 | Median `spread_selected − median <= 0 bps` in all primary cells               | **TRIGGERED**     |
| 3 | Median Spearman IC `<= 0` in all primary cells                                | **TRIGGERED**     |
| 4 | Turnover-implied cost pressure dominates spread (diagnostic)                  | n/a (spread ≤ 0) |
| 5 | Effect concentrated in one symbol with selected-share > 70% (diagnostic)      | not triggered     |

Primary criteria 1, 2, and 3 all triggered together. Criterion 4 is
moot because the median spread is non-positive — there is no
positive spread for cost pressure to dominate. Criterion 5 is not
triggered: max selected share is ~ 12%.

### 11.D Conditional-supported criteria evaluation

| Criterion                                              | Cells passing | Required |
| ------------------------------------------------------- | ------------- | -------- |
| outperformance > 55% in primary cell                    | 0 / 4         | ≥ 2      |
| median spread > +16 bps in primary cell                 | 0 / 4         | ≥ 2      |
| positive Spearman IC in primary cell                    | 0 / 4         | ≥ 2      |

Zero cells pass any conditional-supported criterion.

### 11.E Verdict

```text
Verdict: NOT_SUPPORTED
```

The verdict is about **future research feasibility for this
particular descriptor / filter combination only**. It is **not**:

- a strategy verdict;
- a verdict that revises any retained strategy verdict
  (`R3` / `R2` / `F1` / `D1-A` / `V2` / `G1` / `C1` are unchanged);
- an authorization for any successor phase.

---

## 12. Interpretation and Research Implications

### 12.A What Phase 4ai descriptively shows

- The predeclared composite primary score
  (0.7 × multi-horizon relative return + 0.3 × vol-adjusted
  relative strength) **does not produce a directional edge**
  cross-sectionally on the five-symbol Phase 4ac core universe at
  the tested 24h and 72h forward horizons under Phase 4ad Rule B1.
- The selected symbol (after the predeclared rank-quality filter)
  systematically *underperforms* the median-ranked symbol
  descriptively at the 24h and 72h horizons; the 72h horizon shows
  the worst result (-16.6 bps spread on 1h, -10.3 bps spread on
  4h).
- Selected-symbol crash exposure is *worse* than top-ranked or
  median-ranked crash exposure. The filter — which requires
  recently positive 24h AND 72h returns — is selecting symbols
  that have *already extended* and which then experience
  mean-reversion at the 24–72h forward horizon.
- The rank-quality filter rejects ≈ 55% of all timestamps as
  "no symbol", which preserves the option of doing nothing but
  also implies that even within the half of timestamps that pass
  the filter, the resulting selection has no descriptive forward
  edge.

### 12.B Relationship to Phase 4af's per-symbol null

Phase 4af found per-symbol bar-level direction is essentially
absent in the same five-symbol set. Phase 4ai now extends that
null into the cross-symbol dimension at the 24h–72h horizons under
the predeclared composite descriptor: cross-sectional ranking on
prior-return / vol-adjusted-return descriptors does not supply
information that single-symbol substrate metrics fail to supply.

This does **not** prove that *no* cross-sectional descriptor could
ever supply information; it only documents that the **predeclared,
literature-reasonable composite of multi-horizon relative return
and volatility-adjusted relative strength** does not.

### 12.C Distinctness from prior rejections

Phase 4ai's null is structurally distinct from the six prior
strategy rejections (`R2` / `F1` / `D1-A` / `V2` / `G1` / `C1`):

- `R2` / `F1` / `D1-A` failed *with* mechanism evidence at the
  framework-promotion bar.
- `V2` / `G1` / `C1` failed at design-stage / sparsity / fires-and-
  loses respectively.
- Phase 4ai is **not a strategy** and therefore does not "fail"
  in the strategy sense. It is a descriptive feasibility null on a
  ranking layer.

### 12.D Recommended posture

- The cross-sectional symbol-selection lane, *as predeclared in
  the Phase 4ah / Phase 4ai briefs*, does not justify proceeding
  to a fresh-hypothesis discovery memo, an M0-gated mechanism
  memo, or any strategy work.
- The lane should remain paused. A future operator-authorized
  re-look at this lane would have to (i) propose materially
  different descriptors that are not derived from the Phase 4ai
  results (no post-hoc re-tuning), (ii) explicitly justify why
  the new descriptor would carry information that Phase 4af's
  per-symbol null and Phase 4ai's cross-sectional null both
  failed to detect, and (iii) preserve all Phase 4ah anti-rescue
  guardrails.

Phase 4ai does **not** propose such a re-look.

---

## 13. Decision Menu

### Option A — Remain paused

Always procedurally valid. Strongly indicated by Phase 4ai's
`NOT_SUPPORTED` verdict.

### Option B — Merge Phase 4ai to main, then stop

Recommended. Phase 4ai is complete; merging records the
descriptive feasibility null for the project archive without
authorizing any successor phase.

### Option C — Future docs-only Phase 4aj fresh-hypothesis discussion / M0 mechanism memo

**Not recommended now.** Phase 4ai does not provide supportive
evidence for proceeding to fresh-hypothesis discussion; the
verdict is `NOT_SUPPORTED`.

### Option D — Future M0 governance reconciliation phase

Acceptable if the operator wishes to formalize admissibility gates
(reconciling the Phase 4ag M0 proposal with Phase 4z, Phase 4m,
Phase 4t) before any subsequent research direction is considered.

### Option E — Future derivatives-context feasibility memo

Not recommended over remain-paused. The `D1-A` rescue risk is
high; the cross-sectional lane just produced a negative result and
that does not strengthen the case for a derivatives-context lane
that previously failed at the framework-promotion bar.

### Option F — Strategy spec / backtest / old-strategy rerun

Forbidden / not authorized. Old-strategy alt-symbol rescue is
explicitly forbidden by Phase 4aa, Phase 4ab, Phase 4ag, and
Phase 4ah, and is reaffirmed by Phase 4ai.

### Option G — Paper / shadow / live / exchange-write

Forbidden / not authorized. Phase-gate requirements per
`docs/12-roadmap/phase-gates.md` are not met.

---

## 14. Recommendation

```text
Primary recommendation:
Merge Phase 4ai into main, then remain paused.

The cross-sectional trend / relative-strength symbol-selection lane,
as predeclared in the Phase 4ah / Phase 4ai briefs, did not produce
a descriptive forward edge on the five-symbol Phase 4ac core universe
under Phase 4ad Rule B1. The predeclared falsification verdict is
NOT_SUPPORTED for this descriptor / filter combination.

Do NOT authorize a fresh-hypothesis discovery memo on the basis of
Phase 4ai results.
Do NOT authorize a strategy spec.
Do NOT authorize a backtest.
Do NOT authorize old-strategy alt-symbol reruns.
Do NOT authorize data acquisition.
Do NOT authorize multi-position portfolio trading.
Do NOT silently reduce the result into a "rank-then-V2/G1/C1
breakout" structure.
```

The most procedurally sound conditional acceptable next step, if the
operator wishes to formalize admissibility governance after this
null, is **Option D — future docs-only M0 governance reconciliation
phase** (reconciling the Phase 4ag M0 proposal with Phase 4z,
Phase 4m, Phase 4t). Phase 4ai does **not** authorize Option D; it
only records that Option D is procedurally acceptable if the operator
prefers it over remain-paused.

---

## 15. Preserved Locks and Boundaries

Phase 4ai preserves every retained verdict and project lock
verbatim:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains operationally CLOSED.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.
- §11.6 HIGH cost = 8 bps per side preserved.
- §1.7.3 project-level locks preserved verbatim:
    - 0.25% risk per trade,
    - 2× leverage cap,
    - one position max,
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
- Phase 4z recommendations remain recommendations only.
- Phase 4aa admissibility framework remains recommendation only.
- Phase 4ab recommendations remain recommendations only.
- Phase 4ac results remain data / integrity evidence only.
- Phase 4ad Rules A / B / C remain prospective analysis-time scope
  only.
- Phase 4ae findings remain descriptive substrate-feasibility
  evidence only.
- Phase 4af findings remain descriptive regime-continuity /
  directional-persistence evidence only.
- Phase 4ag recommendations remain recommendations only.
- Phase 4ah recommendations remain recommendations only.
- **Phase 4ai findings remain descriptive cross-sectional
  feasibility evidence only.**

---

## 16. Explicit Non-Authorization Statement

Phase 4ai does **NOT** authorize:

- Phase 4aj,
- data acquisition,
- data download,
- API calls,
- endpoint calls,
- raw or normalized data modification,
- manifest creation,
- manifest modification,
- v003 or any other dataset version,
- backtests,
- strategy diagnostics,
- Q1–Q7 rerun,
- strategy PnL computation,
- entry / exit return computation,
- equity curve computation,
- parameter optimization,
- threshold or symbol selection after seeing results,
- new strategy candidate creation,
- strategy candidate naming,
- fresh-hypothesis discovery memo,
- hypothesis-spec memo,
- strategy-spec memo,
- backtest-plan memo,
- implementation,
- runtime code modification,
- test modification,
- existing-script modification,
- old-strategy rescue (`R3` / `R2` / `F1` / `D1-A` / `V2` / `G1` /
  `C1` in any form, including alt-symbol reruns and any -prime /
  -narrow / -relaxed / hybrid variant),
- multi-position portfolio trading,
- silent reduction of cross-sectional ranking into V2 / G1 / C1-style
  single-symbol breakout continuation,
- paper / shadow,
- live-readiness,
- deployment,
- production keys,
- authenticated APIs,
- private endpoints,
- public-endpoint calls in code,
- user stream,
- WebSocket,
- exchange-write,
- MCP,
- Graphify,
- `.mcp.json`,
- credentials,
- successor phase.

Phase 4ai is analysis-and-docs only.

Phase 4ai's primary recommendation is to **merge Phase 4ai into
main and then remain paused**.

Phase 4ai's findings remain **descriptive cross-sectional
feasibility evidence only**. They do not authorize any successor
phase.
