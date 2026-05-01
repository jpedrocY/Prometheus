# Phase 4h — V2 Data Requirements and Feasibility Memo

**Authority:** Operator authorization for Phase 4h (Phase 4g §38 primary
recommendation: docs-only V2 data-requirements and feasibility memo);
Phase 4g (V2 strategy spec — `Participation-Confirmed Trend Continuation`);
Phase 4f §21 (data-source feasibility matrix); Phase 3q (5m supplemental
acquisition pattern); Phase 3r §8 (mark-price gap governance);
Phase 3p §4–§7 (data-requirements / manifest / integrity-check pattern);
Phase 3o §6 / Phase 3p §8 (forbidden question forms; predeclaration
discipline); Phase 2i §1.7.3 (project-level locks);
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/historical-data-spec.md`;
`docs/04-data/live-data-spec.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4h — **V2 Data Requirements and Feasibility Memo**
(docs-only). Translates Phase 4g's locked V2 strategy spec into an
exact data-requirements and feasibility plan before any V2 data
acquisition, backtest, implementation, or analysis. **Phase 4h does
NOT acquire data. Phase 4h does NOT download data. Phase 4h does NOT
modify data, manifests, code, tests, or scripts. Phase 4h does NOT
create v003. Phase 4h does NOT backtest. Phase 4h does NOT implement.
Phase 4h does NOT claim profitability. Phase 4h does NOT revise prior
verdicts. Phase 4h does NOT authorize paper / shadow / live /
exchange-write.**

**Branch:** `phase-4h/v2-data-requirements-and-feasibility`. **Memo
date:** 2026-04-30 UTC.

---

## 1. Summary

Phase 4g locked the V2 strategy spec (signal 30m, bias 4h, session/volume
bucket 1h, 8 entry features + 3 exit/regime features, 512-variant
threshold grid, M1/M2/M3 mechanism-check decomposition, four governance
labels). Phase 4h is the docs-only data-requirements / feasibility memo
that operationalizes Phase 4g's data needs without acquiring or modifying
any data.

Phase 4h evaluates which dataset families are required by the Phase 4g
V2 spec, classifies each against (a) what is already in v002 / v001-of-5m,
(b) what is available from public unauthenticated Binance bulk archives,
(c) what is forbidden (private / authenticated / spot / order-book L2),
and (d) what would be derived versus directly acquired. It predeclares
the dataset-versioning convention, directory layout, manifest field set,
integrity-check rules, `research_eligible` rules, invalid-window
handling, and timestamp / alignment policy that any future V2 acquisition
phase MUST follow. It also predeclares an acquisition execution plan
preview that a future authorized phase (Phase 4i) would implement.

**Feasibility verdict — POSITIVE under defined boundary.** All Phase 4g
V2 features can be derived from public unauthenticated Binance bulk
archives (`klines`, `markPriceKlines`, `fundingRate` REST event archive,
`metrics` daily archive, optionally `aggTrades` monthly archive) using
the same Phase 3q acquisition pattern. **No private / authenticated /
spot / order-book / user-stream data is required.** Two dataset family
categories that do not yet exist in the repository — `metrics` (5-minute
granularity, contains open interest + taker buy/sell ratio + long/short
ratio in one file) and (optionally) `aggTrades` (tick-level taker
classifier) — would need to be acquired in a future Phase 4i.

Phase 4h does NOT authorize Phase 4i. Phase 4h is the data-requirements
memo; Phase 4i acquisition would be a separate, explicit operator
authorization.

**Verification (run on the post-Phase-4g-merge tree):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No code, tests, scripts, data, manifests, specs, locks, thresholds,
or prior verdicts were modified by Phase 4h.**

**Recommended next phase:** **Phase 4i — V2 Public Data Acquisition and
Integrity Validation (docs-and-data, public bulk archives only, no
credentials)** primary; **remain paused** conditional secondary.
**No** immediate backtest; **no** implementation; **no** paper /
shadow / live / exchange-write.

**Recommended state remains paused. No successor phase has been
authorized.**

---

## 2. Authority and boundary

Phase 4h operates strictly inside the post-Phase-4g-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain
  governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
  stagnation governance); Phase 3x §6 / §10; Phase 4a–4e runtime /
  quality / reconciliation governance; Phase 4f V2 hypothesis
  predeclaration; Phase 4g V2 strategy spec.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary
  live; ETHUSDT research / comparison only; one-symbol-only live;
  one-position max; 0.25% risk; 2× leverage cap; mark-price stops;
  v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 /
  §11.4 / §11.6 (= 8 bps HIGH per side).
- **Retained-evidence verdicts preserved verbatim.** R3
  baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 /
  F1 / D1-A retained research evidence only; R2 FAILED — §11.6;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.**
  `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.**
  `.claude/rules/prometheus-mcp-and-secrets.md`.
- **Phase 4g V2 strategy-spec selections preserved.** Phase 4h does
  NOT re-optimize or modify Phase 4g's selections. If Phase 4h
  identifies a feasibility blocker, it records the blocker and
  recommends a separately-authorized future memo to revise the spec;
  it does not unilaterally edit Phase 4g.

---

## 3. Starting state

```text
branch:           phase-4h/v2-data-requirements-and-feasibility
parent commit:    9291ea732e25d78f1ced2013064539cc3d9ac808 (post-Phase-4g-merge housekeeping)
working tree:     clean before memo authoring
main:             9291ea732e25d78f1ced2013064539cc3d9ac808 (unchanged)

Phase 4a foundation:                       merged.
Phase 4b/4c cleanup:                       merged.
Phase 4d review:                           merged.
Phase 4e reconciliation-model design memo: merged.
Phase 4f V2 hypothesis predeclaration:     merged.
Phase 4g V2 strategy spec:                 merged.

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false.
```

---

## 4. Why this memo exists

Phase 4g's V2 spec lists the features it requires (8 entry + 3 exit/
regime) and the data domains they depend on (trade-price klines,
mark-price klines, funding-rate history, open-interest history,
taker-buy/sell flow). Phase 4g §32 also gave a high-level data-source
preview. But Phase 4g did not commit to:

- exact dataset-version names for new families;
- exact directory layout for new families;
- exact manifest field structure for new families;
- exact integrity-check rules and `research_eligible` rules for new
  families;
- exact invalid-window handling rules for the families that Phase 3r §8
  did not already cover;
- exact alignment / timestamp policy mapping V2 features to bar-completion
  rules;
- exact predeclaration of which features would be `acquired directly`
  vs. `derived from existing data`;
- exact data-acquisition execution plan preview for a future Phase 4i.

Without those commitments, a future V2 acquisition phase would either:

(a) **invent the rules at acquisition time**, which would invert the
    project's discipline of predeclaring rules *before* operating on
    data (per Phase 3p / Phase 3q precedent), OR

(b) **fail closed because the rules are missing**, which delays V2
    research without a deliverable from Phase 4h.

Phase 4h commits the rules now, explicitly, before any data is acquired.
This is the same anti-data-snooping / pre-declaration discipline the
project applied to the Phase 3o predeclared 5m diagnostic question set
and the Phase 3p predeclared per-question outcome-interpretation rules.

Phase 4h is **data-design discipline**, not data acquisition. It does
not authorize, prepare for, or imply any data acquisition, any backtest,
any implementation, any paper / shadow run, any live-readiness work, or
any successor phase.

---

## 5. Relationship to Phase 4g V2 strategy spec

Phase 4g (merged at `ce9659f6...` with housekeeping at
`9291ea73...`) selected the following V2 spec choices that drive
Phase 4h's data requirements:

| Phase 4g choice | Value |
|---|---|
| Signal timeframe | **30m** |
| Higher-timeframe bias | **4h** (EMA(20)/(50) discrete comparison) |
| Session / volume bucket | **1h** |
| 5m | **diagnostic-only, NOT primary signal** |
| Active entry features | **8** |
| Active exit / regime features | **3** |
| Threshold-grid variants | **512** (= 2^9) |
| `stop_trigger_domain` (research) | **`trade_price_backtest`** |
| `stop_trigger_domain` (future runtime) | **`mark_price_runtime`** |
| `stop_trigger_domain` (future mark-price validation) | **`mark_price_backtest_candidate`** |
| `break_even_rule` | **`disabled`** |
| `ema_slope_method` | **`discrete_comparison`** |
| `stagnation_window_role` | **`metric_only`** |
| `mixed_or_unknown` | **invalid / fail-closed for all four schemes** |

The 8 active entry features and 3 active exit / regime features (per
Phase 4g §28):

**Entry features:**

1. HTF trend bias state (4h EMA(20)/(50) discrete comparison).
2. Donchian breakout state (signal-timeframe Donchian high(N1) / low(N1)).
3. Donchian width percentile (compression precondition).
4. Range-expansion ratio (breakout-bar TR vs. trailing mean).
5. Relative volume + volume z-score.
6. Volume percentile by UTC hour.
7. Taker buy/sell imbalance.
8. OI delta direction + funding-rate percentile band.

**Exit / regime features:**

1. Time-since-entry counter.
2. ATR percentile regime.
3. HTF bias state continuity.

Phase 4h's data-requirements analysis below maps each of these features
back to its dataset dependency.

---

## 6. V2 data-requirements overview

V2 requires data sufficient to compute 8 entry features and 3 exit /
regime features at 30m resolution, conditioned on a 4h higher-timeframe
bias and 1h session bucket, on BTCUSDT primary (live-research) and
ETHUSDT comparison-only, over a multi-year date range covering the
v002-equivalent 2022-01..2026-03 period.

**Data domains required:**

1. **Trade-price klines** at **30m** and **4h** (for both BTCUSDT and
   ETHUSDT).
2. **Mark-price klines** at **30m** and **4h** (live-readiness path
   only — `mark_price_backtest_candidate` future modeling step;
   research backtest uses `trade_price_backtest`).
3. **Funding-rate history** (per-event 8h cadence; for both BTCUSDT
   and ETHUSDT).
4. **Open-interest history** (5-minute granularity from the `metrics`
   archive; for both BTCUSDT and ETHUSDT).
5. **Taker buy/sell flow** (5-minute granularity from the `metrics`
   archive; for both BTCUSDT and ETHUSDT).
6. **Long/short ratio** (5-minute granularity from the `metrics`
   archive; OPTIONAL — only if a future V2-extension phase activates
   this currently-non-active feature).
7. **(Optional) `aggTrades`** (tick-level; only if `metrics`
   `taker_buy_sell_volume_ratio` is shown to be insufficient for V2
   spec needs).
8. **(Already in repo) v002 funding** for both symbols.
9. **(Already in repo) v002 15m / 1h klines** as a fallback or
   cross-check source for 30m / 4h derivation.
10. **(Already in repo, partial) v001-of-5m trade-price klines**
    (research-eligible).
11. **(Already in repo, partial) v001-of-5m mark-price klines**
    (`research_eligible: false`; bound by Phase 3r §8 governance).

**Data domains explicitly NOT required:**

- order-book L2 depth (FORBIDDEN: requires authenticated / WebSocket
  feed);
- wallet-state / account-balance (FORBIDDEN: authenticated REST);
- user stream / listenKey lifecycle (FORBIDDEN);
- spot-leg klines / spot orderbook (NOT REQUIRED: v1 is perpetual
  only);
- cross-venue data (NOT REQUIRED: single-venue, Binance USDⓈ-M only);
- daily kline (NOT REQUIRED: 4h bias is the largest V2 timeframe).

---

## 7. Required dataset families

For each Phase 4g V2 feature, this section identifies the required
dataset family.

### A. Trade-price klines

**Required:**

- BTCUSDT 30m trade-price klines.
- ETHUSDT 30m trade-price klines.
- BTCUSDT 4h trade-price klines.
- ETHUSDT 4h trade-price klines.

**Existing repository state:**

- v002 has BTCUSDT 15m + 1h-derived (research-eligible).
- v002 has ETHUSDT 15m + 1h-derived (research-eligible).
- v001-of-5m has BTCUSDT 5m (research-eligible) and ETHUSDT 5m
  (research-eligible).
- **30m and 4h are NOT currently in the repository** as named
  datasets.

**Acquisition vs. derivation preference (predeclared):**

| Option | Recommended? | Reason |
|---|---|---|
| **Acquire 30m direct from `data.binance.vision` bulk archive** (`klines/<SYMBOL>/30m/`) | **YES — primary path** | Matches v002's bulk-archive-first pattern; provides authoritative monthly aggregations with paired SHA256 checksums; clean lineage; no derivation ambiguity. |
| **Derive 30m from local v001-of-5m via 6-bar aggregation** | OPTIONAL fallback | Avoids any Binance fetch; relies on Phase 3q v001-of-5m research-eligibility; introduces aggregation logic that must be tested for OHLC reconstruction correctness. |
| **Acquire 4h direct from `data.binance.vision` bulk archive** (`klines/<SYMBOL>/4h/`) | **YES — primary path** | Same rationale as 30m. |
| **Derive 4h from 1h-derived v002 OR 30m direct OR 5m via 48-bar aggregation** | OPTIONAL fallback | Acceptable but adds derivation complexity; prefer direct acquisition for primary lineage. |

**Phase 4h predeclared preference:** **direct acquisition** for both
30m and 4h, with derivation reserved as an operator-approved fallback
only if direct acquisition is unavailable for a specific month. This
parallels the v002 / v001-of-5m precedent: every interval used in
research has its own bulk-archive-sourced manifest.

**Phase 4h does NOT acquire any of this data.**

### B. Mark-price klines

**Required (live-readiness path only — DEFERRED):**

- BTCUSDT 30m mark-price klines.
- ETHUSDT 30m mark-price klines.
- BTCUSDT 4h mark-price klines.
- ETHUSDT 4h mark-price klines.

**Existing repository state:**

- v002 has BTCUSDT 15m mark-price klines and ETHUSDT 15m mark-price
  klines (with the same four upstream Binance maintenance-window
  gaps as Phase 3q v001-of-5m mark-price; v002's manifest
  `invalid_windows: []` is technically inaccurate but locked per
  Phase 3q precedent).
- v001-of-5m has BTCUSDT 5m mark-price (`research_eligible: false`,
  4 gaps) and ETHUSDT 5m mark-price (`research_eligible: false`,
  4 gaps).
- **30m and 4h mark-price are NOT currently in the repository.**

**Phase 4h predeclared policy:**

- V2's primary backtest is `trade_price_backtest`. The first V2
  backtest (if ever authorized) does NOT require 30m / 4h mark-price.
- A future `mark_price_backtest_candidate` modeling pass — required
  for live-readiness validation per Phase 3v §8.5 — DOES require
  30m / 4h mark-price klines for both symbols.
- **Phase 4h DEFERS 30m / 4h mark-price acquisition** to a separately
  authorized future phase (likely Phase 4i mark-price extension or a
  later phase). If Phase 4i is authorized, the operator may scope it
  to `trade_price_backtest`-only data (excluding mark-price 30m / 4h)
  to keep Phase 4i tractable; the live-readiness `mark_price_backtest_candidate`
  path is a strictly later concern.
- **Phase 3r §8 mark-price gap governance applies verbatim** to any
  future 30m / 4h mark-price acquisition. The four upstream
  maintenance-window gaps (BTC: 2022-07-30/31, 2022-10-02,
  2023-02-24, 2023-11-10; ETH: 2022-07-12, 2022-10-02, 2023-02-24,
  2023-11-10) will be detectable at 30m / 4h granularity (each gap
  is at least 30 minutes long; at 4h granularity, gaps may be
  partially absorbed depending on alignment). Any 30m / 4h
  mark-price dataset acquired in a future phase MUST follow Phase
  3r §8 invalid-window-exclusion semantics; **MUST NOT silently
  patch, forward-fill, interpolate, or re-mark `research_eligible:
  true` without explicit governance modification.**

**Phase 4h does NOT relax `research_eligible` rules for mark-price.**
Phase 3r §8 governance is preserved verbatim.

**Phase 4h does NOT acquire any mark-price data.**

### C. Funding-rate history / premium index

**Required:**

- BTCUSDT funding-rate history (8h cadence per BTCUSDT USDⓈ-M
  perpetual settlement schedule).
- ETHUSDT funding-rate history (8h cadence per ETHUSDT USDⓈ-M
  perpetual settlement schedule).

**Existing repository state:**

- v002 has both: `binance_usdm_btcusdt_funding__v002` and
  `binance_usdm_ethusdt_funding__v002`. **Both research-eligible.**
- Sourced from `https://fapi.binance.com/fapi/v1/fundingRate` REST
  endpoint per v002 manifest `notes` field (Phase 2c funding-rate
  REST ingest, window: 1640995200000 → 1775001599999 UTC ms,
  i.e., 2022-01-01..2026-03-31).

**Coverage check:**

- v002 funding ranges to 2026-03-31. V2's predeclared date range is
  2022-01-01..2026-03-31 (per §13 below). **v002 funding coverage is
  sufficient for V2's first backtest.**
- A future Phase 4i may re-validate this coverage and may extend
  forward in time if a later operator decision authorizes inclusion
  of 2026-04 onward (currently NOT recommended per §13's
  freshness-drift policy).

**Phase 4h predeclared preference:** **reuse v002 funding manifests
verbatim.** No new funding dataset version is required for V2's
first backtest. Phase 4i (if authorized) would NOT re-acquire
funding data unless v002's REST-based provenance is judged
insufficient (which Phase 4h does NOT recommend).

**Funding alignment to V2 signal bars:**

- V2 signal timeframe is 30m. Funding events occur at 00:00 / 08:00
  / 16:00 UTC (8h cadence). For each 30m signal bar, the most
  recent completed funding event timestamp is at most 8h prior.
- Phase 4h predeclares the alignment rule: a V2 funding-percentile
  feature value at signal-bar `t` uses the funding rate of the
  most recent funding event with `funding_time <= t` AND
  `t - funding_time <= 8h`. If no funding event satisfies the
  constraint (e.g., during an unusually long gap), the V2 setup
  for that bar is `research_eligible: false` for the funding
  feature only and the trade is rejected fail-closed.
- This rule is consistent with Phase 4g §22.4 and `live-data-spec.md`
  bar-completion-only requirements.

**Phase 4h does NOT acquire any funding-rate data.**

### D. Open-interest history

**Required:**

- BTCUSDT open-interest history at 5-minute granularity (the lowest
  granularity at which `data.binance.vision` publishes the `metrics`
  family).
- ETHUSDT open-interest history at 5-minute granularity.

**Existing repository state:**

- **NOT in repository.** No `metrics`-family dataset exists in v002
  or v001-of-5m.
- The bulk-archive source family is at:
  `https://data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/<SYMBOL>-metrics-YYYY-MM-DD.zip`
  (daily archives; 5-minute records inside each archive).

**`metrics` family content (per [Binance public-data repo](https://github.com/binance/binance-public-data)):**

Each record carries the following columns (5-minute granularity,
across the same date range covered by klines / markPriceKlines):

- `create_time`
- `symbol`
- `sum_open_interest` (open interest in base-asset units at the
  5-minute boundary)
- `sum_open_interest_value` (open interest in quote-asset units)
- `count_toptrader_long_short_ratio` (count-based; top-20% by margin
  balance)
- `sum_toptrader_long_short_ratio` (sum-based; top-20% by margin
  balance)
- `count_long_short_ratio` (account-based; broad)
- `sum_taker_long_short_vol_ratio` (taker buy / taker sell volume
  ratio over the 5-minute window)

**Implication:** the `metrics` daily archive is a **single source**
that simultaneously provides:

- **open-interest history** (used by V2 entry feature 8);
- **taker buy/sell imbalance** (used by V2 entry feature 7); and
- **long/short ratio** (an OPTIONAL feature documented but NOT
  activated by Phase 4g §28).

This consolidates three of Phase 4g's data dependencies into one
acquisition target.

**Phase 4h predeclared preference:** acquire `metrics` daily archives
for BTCUSDT and ETHUSDT for the V2 date range (§13). Resample to 30m
during normalization (aggregate the six 5-minute records per 30m
window). Compute V2's OI-delta feature at 30m granularity from the
30m-resampled OI series.

**Phase 4h does NOT acquire any `metrics` data.**

### E. Taker buy/sell flow

**Required:** taker buy/sell ratio at the 30m signal bar (used by V2
entry feature 7).

**Primary source — `metrics` daily archive:**

The `sum_taker_long_short_vol_ratio` column in the `metrics` archive
provides the taker buy/sell volume ratio at 5-minute granularity.
Aggregated over 30m (six 5-minute records per 30m window), this
yields a per-30m-bar taker-imbalance metric.

**Definition (predeclared):**

- 5-minute `taker_buy_volume` and `taker_sell_volume` are not
  directly given as separate columns by the `metrics` archive
  (which provides the *ratio*, not the raw counts). However, the
  Binance USDⓈ-M `klines` archive's columns include `taker_buy_volume`
  (which can be subtracted from total `volume` to derive taker_sell_volume).
- **Phase 4h predeclares the primary derivation:** taker_imbalance at
  the 30m bar = `sum(taker_buy_volume over 30m) / sum(total_volume
  over 30m)` from the existing kline data. The kline-derived
  taker-buy-volume column is itself sufficient to compute imbalance
  at any timeframe.
- The `metrics` archive's `sum_taker_long_short_vol_ratio` column is
  available as a **cross-check / sanity-validation** source.

**Phase 4h predeclared preference:**

| Source | Role |
|---|---|
| **kline `taker_buy_volume` column** at 30m (acquired with klines) | **PRIMARY** for V2 taker-imbalance feature |
| **`metrics` `sum_taker_long_short_vol_ratio`** at 5-minute resampled to 30m | Cross-check / sanity validation |
| **`aggTrades` monthly archive** | **Fallback only** if `metrics`-derived ratio is shown to be insufficient |

**Why klines' `taker_buy_volume` is sufficient for V2:** V2's
participation gate requires the breakout bar's taker-buy fraction
to exceed a predeclared threshold (per Phase 4g §17 sub-component
(d), grid `T_imb_min ∈ {0.55, 0.60}`). The kline `taker_buy_volume`
column directly enables computing `taker_buy_fraction =
taker_buy_volume / total_volume` at the 30m breakout bar's
resolution. No tick-level reconstruction is required. The
`metrics` archive's ratio is a derivative quantity over the same
window; klines' explicit volume columns are higher-fidelity.

**Phase 4h does NOT acquire any `aggTrades` data.** `aggTrades`
acquisition is reserved as a fallback only if a future analysis
proves klines' `taker_buy_volume` is insufficient for V2's needs
(which Phase 4h does NOT expect).

**Phase 4h does NOT use private / order-book / user-stream data.**

### F. Volume features

**Required:** relative volume; volume z-score; volume percentile by
UTC hour (V2 entry feature 5 + sub-component (c) of feature 6).

**Source:** `volume` column in the 30m trade-price kline archive
(once acquired per §A).

**Derivations (predeclared):**

- **Relative volume** at bar `t`:
  `volume(t) / mean(volume(t-L_vol..t-1))` where L_vol = 240 30m
  bars (= 5 days; per Phase 4g §29). Computed at signal-bar
  completion.
- **Volume z-score** at bar `t`:
  `(volume(t) - mean) / stdev` over the same L_vol window.
- **Volume percentile by UTC hour** at bar `t`: the percentile of
  `volume(t)` within the trailing distribution of 30m breakout-bar
  volumes *for the same UTC hour* over L_session = 60 days (per
  Phase 4g §29). This requires bucketing 30m bars by the UTC hour
  in which they fall; each 1h bucket contains two 30m bars; the
  percentile is computed within each hour-bucket independently.

**No additional dataset family is required for volume features.** All
derivable from 30m klines.

### G. Existing Phase 3q 5m supplemental data — diagnostic-only role

**Phase 3q v001-of-5m datasets** (BTCUSDT 5m + ETHUSDT 5m trade-price,
research-eligible; BTCUSDT 5m + ETHUSDT 5m mark-price,
`research_eligible: false`) are **NOT used as a primary V2 signal
source** under Phase 4g §11.4 (5m diagnostic-only). V2 entry rules,
exit rules, and threshold grids do not depend on 5m data.

**Permitted V2 use of v001-of-5m data (diagnostic-only):**

- post-trade diagnostic analysis (analogous to Phase 3s) on V2 trades
  if a future authorized phase opens that question;
- 30m derivation as an OPTIONAL fallback path per §A above (acceptable
  only if direct 30m acquisition fails);
- **NEVER as a primary signal source.**

**Phase 4h preserves Phase 3t §14.2 (5m research-thread closure) and
Phase 3q / 3r mark-price `research_eligible: false` governance verbatim.**

---

## 8. Existing available datasets

| Dataset version | Symbol | Family | Interval | Research-eligible? | V2 use |
|---|---|---|---|---|---|
| `binance_usdm_btcusdt_15m__v002` | BTCUSDT | klines | 15m | YES | available as derivation fallback |
| `binance_usdm_btcusdt_1h_derived__v002` | BTCUSDT | klines | 1h | YES | available as 4h-derivation fallback |
| `binance_usdm_ethusdt_15m__v002` | ETHUSDT | klines | 15m | YES | available as derivation fallback |
| `binance_usdm_ethusdt_1h_derived__v002` | ETHUSDT | klines | 1h | YES | available as 4h-derivation fallback |
| `binance_usdm_btcusdt_markprice_15m__v002` | BTCUSDT | markPriceKlines | 15m | YES (locked, manifest `invalid_windows: []` known inaccurate per Phase 3q precedent) | NOT used by V2 first backtest (`trade_price_backtest`) |
| `binance_usdm_ethusdt_markprice_15m__v002` | ETHUSDT | markPriceKlines | 15m | YES (same precedent) | NOT used by V2 first backtest |
| `binance_usdm_btcusdt_funding__v002` | BTCUSDT | fundingRate | per-event 8h | YES | **PRIMARY** funding-rate source for V2 |
| `binance_usdm_ethusdt_funding__v002` | ETHUSDT | fundingRate | per-event 8h | YES | **PRIMARY** funding-rate source for V2 |
| `binance_usdm_btcusdt_5m__v001` | BTCUSDT | klines | 5m | YES | diagnostic-only role |
| `binance_usdm_ethusdt_5m__v001` | ETHUSDT | klines | 5m | YES | diagnostic-only role |
| `binance_usdm_btcusdt_markprice_5m__v001` | BTCUSDT | markPriceKlines | 5m | NO (4 gaps; Phase 3r §8) | bound by Phase 3r §8 governance |
| `binance_usdm_ethusdt_markprice_5m__v001` | ETHUSDT | markPriceKlines | 5m | NO (4 gaps; Phase 3r §8) | bound by Phase 3r §8 governance |

(Older `__v001` non-5m manifests exist alongside `__v002` for
provenance; v002 supersedes them in retained-evidence verdicts.)

---

## 9. Missing required datasets

For V2's first backtest (per Phase 4g §31's `trade_price_backtest`
provenance), the following dataset families are **missing** and
would need to be acquired in a future Phase 4i:

| Missing family | Symbols | Granularity | Source family | Direct or derived | Required for V2 first backtest? |
|---|---|---|---|---|---|
| Trade-price klines, 30m | BTCUSDT, ETHUSDT | 30m | `data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/30m/` | direct (preferred) or derive from 15m / 5m | **YES** |
| Trade-price klines, 4h | BTCUSDT, ETHUSDT | 4h | `data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/4h/` | direct (preferred) or derive from 1h / 30m | **YES** |
| Open-interest + taker-buy/sell-ratio + long/short-ratio | BTCUSDT, ETHUSDT | 5m (within `metrics` daily archive) | `data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/` | direct, then resampled to 30m | **YES** (OI, taker imbalance) |

For V2's future `mark_price_backtest_candidate` modeling pass (NOT
required by V2's first backtest; deferred until separately authorized):

| Missing family | Symbols | Granularity | Source family | Direct or derived | Required for V2 first backtest? |
|---|---|---|---|---|---|
| Mark-price klines, 30m | BTCUSDT, ETHUSDT | 30m | `data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/30m/` | direct (preferred) | NO (deferred) |
| Mark-price klines, 4h | BTCUSDT, ETHUSDT | 4h | `data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/4h/` | direct (preferred) | NO (deferred) |

For V2 OPTIONAL features (NOT activated by Phase 4g §28):

| Missing family | Symbols | Granularity | Source family | Required for V2 first backtest? |
|---|---|---|---|---|
| `aggTrades` (tick-level) | BTCUSDT, ETHUSDT | tick | `data.binance.vision/data/futures/um/monthly/aggTrades/<SYMBOL>/` | NO (fallback / future-only) |

**Summary:** Phase 4i (if authorized) MUST acquire {30m klines × 2,
4h klines × 2, `metrics` × 2}, optionally extend with {30m markPriceKlines
× 2, 4h markPriceKlines × 2, aggTrades × 2}. The minimum set for
V2's first backtest is **6 dataset families** (30m × 2 + 4h × 2 +
metrics × 2).

---

## 10. Public-source feasibility

All required dataset families are available from the public,
unauthenticated `data.binance.vision` bulk archive, consistent with
the Phase 3q acquisition pattern:

| Family | Source URL pattern | Granularity | Verified? |
|---|---|---|---|
| Trade-price klines | `https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip` | 30m, 4h | YES (existing v002 / v001-of-5m use this convention; intervals 30m and 4h are documented and available from the [Binance public-data repo](https://github.com/binance/binance-public-data)) |
| Mark-price klines | `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/<INTERVAL>/<SYMBOL>-<INTERVAL>-<YYYY>-<MM>.zip` | 30m, 4h | YES (existing v001-of-5m markprice uses this convention) |
| Funding-rate history | `https://fapi.binance.com/fapi/v1/fundingRate?symbol=<SYMBOL>` (REST endpoint, paginated) | per-event | YES (existing v002 funding uses this REST source) |
| `metrics` (OI + taker imbalance + long/short ratio) | `https://data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/<SYMBOL>-metrics-<YYYY>-<MM>-<DD>.zip` | 5m records inside daily archive | YES ([Binance Data Collection — `data/futures/um/daily/metrics/`](https://data.binance.vision/?prefix=data%2Ffutures%2Fum%2Fdaily%2Fmetrics%2F)) |
| `aggTrades` | `https://data.binance.vision/data/futures/um/monthly/aggTrades/<SYMBOL>/<SYMBOL>-aggTrades-<YYYY>-<MM>.zip` | tick | YES ([Binance public-data repo](https://github.com/binance/binance-public-data)) |
| Paired SHA256 checksum | `<base-archive-URL>.CHECKSUM` | per-archive | YES (Phase 3q precedent) |

**Authentication:** none required. **Credentials:** none used.
**API keys:** none required. **MCP / Graphify / `.mcp.json`:** none
touched.

**Phase 4h does NOT make any HTTP request.** All endpoint references
are documentation-only; no network I/O is performed by this memo.

---

## 11. Forbidden / private data boundary

Phase 4h preserves the project's safety / secrets discipline verbatim:

**FORBIDDEN sources (any future acquisition phase MUST NOT use):**

- **Private / authenticated REST endpoints.** Any endpoint requiring
  an API key or signed request.
- **User stream / listenKey / WebSocket private state.** Account-state,
  wallet, fill notifications, private order updates.
- **Order-book L2 depth feeds.** Snapshot or delta. Both spot and
  perpetual.
- **Production-key-dependent endpoints.** `/fapi/v1/openOrders`,
  `/fapi/v2/account`, `/fapi/v2/balance`, etc. — any endpoint
  returning private state.
- **Spot leg data.** v1 is perpetual only; spot data is not
  authorized even for research.
- **Cross-venue data.** v1 is single-venue (Binance USDⓈ-M).

**ALLOWED sources (Phase 4h-approved):**

- `data.binance.vision` public unauthenticated bulk archive (klines,
  markPriceKlines, metrics, aggTrades), including paired `.CHECKSUM`
  files.
- `https://fapi.binance.com/fapi/v1/fundingRate` (public REST endpoint
  used by v002 funding manifests; no signed request required;
  symbol-only query).
- Existing repository data (v002 / v001-of-5m / Phase 3q manifests)
  for derivation fallback or cross-validation only.

**No credentials of any kind are required, requested, used, stored,
or referenced by Phase 4h or by any future Phase 4i.** No `.env`
files, no API key prompts, no signed-request infrastructure.

---

## 12. Dataset versioning convention

Phase 4h proposes the following dataset-version names, consistent
with the existing v002 / v001-of-5m naming pattern (per
`docs/04-data/dataset-versioning.md`):

**For V2 first backtest (REQUIRED if Phase 4i is authorized):**

```text
binance_usdm_btcusdt_30m__v001
binance_usdm_ethusdt_30m__v001
binance_usdm_btcusdt_4h__v001
binance_usdm_ethusdt_4h__v001
binance_usdm_btcusdt_metrics__v001          (5-minute OI / taker / long-short ratio)
binance_usdm_ethusdt_metrics__v001
```

**For V2 future mark-price live-readiness validation (DEFERRED;
NOT required by Phase 4i if Phase 4i is scoped to first backtest only):**

```text
binance_usdm_btcusdt_markprice_30m__v001
binance_usdm_ethusdt_markprice_30m__v001
binance_usdm_btcusdt_markprice_4h__v001
binance_usdm_ethusdt_markprice_4h__v001
```

**For V2 OPTIONAL aggTrades fallback (DEFERRED; NOT recommended):**

```text
binance_usdm_btcusdt_aggtrades__v001
binance_usdm_ethusdt_aggtrades__v001
```

**Versioning rules (predeclared per Phase 3q precedent):**

- All new V2 datasets start at `__v001`. They do not bump v002 or
  v001-of-5m.
- Each new manifest's `predecessor_dataset_versions` field references
  the closest existing predecessor where applicable (e.g.,
  `binance_usdm_btcusdt_30m__v001`'s predecessor would be
  `binance_usdm_btcusdt_15m__v002` or `binance_usdm_btcusdt_5m__v001`,
  depending on whether 30m is direct-acquired or derived).
- v002 manifests are NOT modified.
- v001-of-5m manifests are NOT modified.
- No v003 family bump.

**Phase 4h does NOT create any of these manifests.** The names are
pre-declared so a future Phase 4i can use them without renaming.

---

## 13. Date-range requirements

**V2 first backtest target date range (predeclared):**

```text
2022-01-01 00:00:00 UTC  →  2026-03-31 23:59:59.999 UTC
```

**Justification:**

- Matches Phase 3q v001-of-5m supplemental coverage exactly,
  preserving cross-dataset comparability (30m bars derivable from
  5m without coverage gaps).
- Matches v002 retained-evidence trade-population coverage
  (1641014100000..1770879600000 UTC ms = 2022-01-01 05:15..2026-02-12
  07:00); the 2022-01-01 / 2026-03-31 endpoints provide a strict
  superset.
- Provides at least two non-overlapping out-of-sample windows
  (e.g., train 2022-01..2024-12 / OOS-1 2025-01..2025-06 / OOS-2
  2025-07..2026-03) for the multi-window validation requirement
  (Phase 4g §31).
- 2026-04 onward is **explicitly excluded** to avoid:
  - freshness drift (data may not yet be available in bulk-archive
    for the most recent month at acquisition time);
  - partial-month boundary issues at acquisition time;
  - operator-time-of-acquisition coupling that would make the
    dataset version dependent on when the acquisition phase ran.

**Symbol coverage requirements:**

- BTCUSDT (primary research symbol).
- ETHUSDT (comparison-only).
- No additional symbols (per §1.7.3).

**Strict superset coverage requirement:** acquired data MUST cover
the full date range with zero gaps for trade-price / metrics families.
Mark-price gaps follow Phase 3r §8 governance (recorded as
`invalid_windows`, not silently patched).

---

## 14. Symbol coverage requirements

Per §1.7.3 / Phase 4g §9:

- **BTCUSDT USDⓈ-M perpetual:** primary research symbol; future live
  symbol (gated; not authorized).
- **ETHUSDT USDⓈ-M perpetual:** research / comparison-only; never
  promoted to live without separate authorization.
- **No multi-asset portfolio.**
- **No cross-venue.**
- **No spot leg.**
- **No hedge mode.**
- **No additional perpetual symbols** (no SOLUSDT, no BNBUSDT, no
  any other symbol).

Phase 4h does NOT propose adding additional symbols.

---

## 15. Directory layout proposal

Phase 4h proposes the following directory layout, consistent with
the existing v002 / v001-of-5m layout (per `docs/04-data/historical-data-spec.md`):

```text
data/
├─ raw/
│  └─ binance_usdm/
│     ├─ klines/
│     │  └─ symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/<SYMBOL>-<INTERVAL>-YYYY-MM.zip
│     ├─ markPriceKlines/
│     │  └─ symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/<SYMBOL>-<INTERVAL>-YYYY-MM.zip   (DEFERRED)
│     ├─ metrics/
│     │  └─ symbol={BTCUSDT,ETHUSDT}/year=YYYY/month=MM/<SYMBOL>-metrics-YYYY-MM-DD.zip                     (one zip per day)
│     └─ aggTrades/
│        └─ symbol={BTCUSDT,ETHUSDT}/year=YYYY/month=MM/<SYMBOL>-aggTrades-YYYY-MM.zip                       (OPTIONAL / DEFERRED)
├─ normalized/
│  ├─ klines/
│  │  └─ symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/part-0000.parquet
│  ├─ mark_price_klines/
│  │  └─ symbol={BTCUSDT,ETHUSDT}/interval={30m,4h}/year=YYYY/month=MM/part-0000.parquet                     (DEFERRED)
│  ├─ metrics/
│  │  └─ symbol={BTCUSDT,ETHUSDT}/granularity=5m/year=YYYY/month=MM/part-0000.parquet
│  └─ agg_trades/
│     └─ symbol={BTCUSDT,ETHUSDT}/year=YYYY/month=MM/part-0000.parquet                                        (OPTIONAL / DEFERRED)
└─ manifests/
   ├─ binance_usdm_btcusdt_30m__v001.manifest.json
   ├─ binance_usdm_ethusdt_30m__v001.manifest.json
   ├─ binance_usdm_btcusdt_4h__v001.manifest.json
   ├─ binance_usdm_ethusdt_4h__v001.manifest.json
   ├─ binance_usdm_btcusdt_metrics__v001.manifest.json
   ├─ binance_usdm_ethusdt_metrics__v001.manifest.json
   ├─ binance_usdm_btcusdt_markprice_30m__v001.manifest.json    (DEFERRED)
   ├─ binance_usdm_ethusdt_markprice_30m__v001.manifest.json    (DEFERRED)
   ├─ binance_usdm_btcusdt_markprice_4h__v001.manifest.json     (DEFERRED)
   ├─ binance_usdm_ethusdt_markprice_4h__v001.manifest.json     (DEFERRED)
   ├─ binance_usdm_btcusdt_aggtrades__v001.manifest.json        (OPTIONAL / DEFERRED)
   └─ binance_usdm_ethusdt_aggtrades__v001.manifest.json        (OPTIONAL / DEFERRED)
```

**`.gitignore` precedent:** `/data/raw/`, `/data/normalized/`,
`/data/derived/` are git-ignored per the existing v002 / Phase 3q
convention. `/data/manifests/*.manifest.json` files are committed.

**Phase 4h does NOT create any of these directories or files.**

---

## 16. Manifest requirements

Each new V2 dataset manifest MUST include the following fields,
consistent with the existing v002 / v001-of-5m manifest schema
(per `docs/04-data/dataset-versioning.md`):

| Field | Type | Required | Description |
|---|---|---|---|
| `dataset_id` / `dataset_version` | string | YES | e.g., `binance_usdm_btcusdt_30m__v001` |
| `dataset_name` | string | YES | e.g., `binance_usdm_btcusdt_30m` |
| `dataset_category` | string | YES | e.g., `normalized_kline`, `metrics_record`, `mark_price_kline` |
| `schema_version` | string | YES | e.g., `kline_v1`, `metrics_v1`, `mark_price_kline_v1` |
| `symbols` | list[string] | YES | e.g., `["BTCUSDT"]` |
| `intervals` | list[string] | YES | e.g., `["30m"]`, `["4h"]`, `[]` for funding/metrics |
| `canonical_timezone` | string | YES | `UTC` |
| `canonical_timestamp_format` | string | YES | `unix_milliseconds` |
| `partitioning` | list[string] | YES | e.g., `["symbol", "interval", "year", "month"]` |
| `primary_key` | list[string] | YES | e.g., `["symbol", "interval", "open_time"]` |
| `created_at_utc_ms` | int64 | YES | manifest creation time |
| `pipeline_version` | string | YES | e.g., `prometheus@0.0.0` |
| `generator` | string | YES | e.g., `scripts.phase4i_v2_acquisition` (future Phase 4i) |
| `predecessor_dataset_versions` | list[string] OR null | YES | e.g., `["binance_usdm_btcusdt_15m__v002"]` for derived datasets; null for fully-direct |
| `sources` | list[string] | YES | sorted list of bulk-archive URL patterns or REST endpoints |
| `date_range_start_open_time_utc_ms` | int64 | YES | first bar `open_time` |
| `date_range_end_open_time_utc_ms` | int64 | YES | last bar `open_time` |
| `bar_count` (or `record_count`) | int64 | YES | total normalized rows |
| `raw_archive_count` | int64 | YES | number of raw archives downloaded |
| `raw_sha256_index` | dict[string, string] OR list of {file, sha256} | YES | SHA256 of each raw archive |
| `quality_checks` | object | YES | per-family integrity-check object (see §17) |
| `invalid_windows` | list[object] | YES | invalid-window list (empty for clean datasets; populated for mark-price gaps per Phase 3r §8) |
| `research_eligible` | bool | YES | per family; per integrity-check verdict |
| `notes` | string | OPTIONAL | freeform; e.g., Phase 4i framing |
| `command_used` | string | YES | exact command used for acquisition (no credentials) |
| `code_commit` | string | YES | Phase 4i commit SHA for reproducibility |
| `acquisition_completed_utc_ms` | int64 | YES | when acquisition finished |
| `no_credentials_confirmation` | bool | YES | always `true` (sanity check) |
| `private_endpoint_used` | bool | YES | always `false` (sanity check) |

**Phase 4h does NOT create any manifest.** The schema is predeclared
so Phase 4i can implement it directly.

---

## 17. Integrity-check requirements

Phase 4h predeclares the per-family integrity-check rules. Phase 3p §6.2
and the existing v002 / v001-of-5m manifests' `quality_checks` objects
are the precedent.

### 17.1 Trade-price klines (30m, 4h)

| Check | Threshold | Action on fail |
|---|---|---|
| `monotone_timestamps` | true (strictly increasing `open_time`) | `research_eligible: false` |
| `duplicate_timestamps` | 0 | `research_eligible: false` |
| `boundary_alignment_violations` (`open_time mod (interval_ms) != 0`) | 0 | `research_eligible: false` |
| `close_time_consistency_violations` (`close_time != open_time + interval_ms - 1`) | 0 | `research_eligible: false` |
| `gaps_detected` | 0 | `research_eligible: false` (per Phase 3p §4.7 strict gate) |
| `gap_locations` | empty list expected | populated if gaps; window-precision recorded |
| `ohlc_sanity_violations` (low ≤ open, close, high; high ≥ open, close, low) | 0 | `research_eligible: false` |
| `volume_sanity_violations` (volume < 0; taker_buy_volume < 0; taker_buy_volume > volume) | 0 | `research_eligible: false` |
| `taker_buy_volume_present` | true (column exists, non-null) | `research_eligible: false` |
| `symbol_consistency_violations` | 0 | `research_eligible: false` |
| `interval_consistency_violations` | 0 | `research_eligible: false` |
| `date_range_coverage` | start ≤ 1640995200000 (2022-01-01 UTC) AND end ≥ 1775001599999 (2026-03-31 23:59:59.999 UTC) | `research_eligible: false` |

### 17.2 Mark-price klines (30m, 4h — DEFERRED)

Same as 17.1, plus:

| Check | Threshold | Action on fail |
|---|---|---|
| `gaps_detected` | 0 (strict per Phase 3p §4.7) | `research_eligible: false` |
| `invalid_windows` | populated verbatim if gaps detected | NOT silently patched (Phase 3r §8) |
| `volume column expected` | NO (mark-price klines lack volume by spec) | `volume_sanity_violations: n/a` |

### 17.3 Funding-rate (REUSING v002)

Per `binance_usdm_btcusdt_funding__v002` / `binance_usdm_ethusdt_funding__v002`:

| Check | Threshold | Action on fail |
|---|---|---|
| `monotone_timestamps` (`funding_time` strictly increasing) | true | n/a (already locked) |
| `duplicate_timestamps` | 0 | n/a (already locked) |
| `expected_cadence` | nominal 8h between consecutive events (variable cadence allowed; Binance documents non-strict 8h cadence around DST / maintenance) | recorded; not blocking |
| `missing_funding_events` (consecutive gap > 24h) | 0 expected | recorded; flagged for review |
| `numeric_sanity` (`funding_rate` finite; abs ≤ 0.01 = 1.0% per-event) | within Binance documented limits | extreme value flagged for review (do NOT silently exclude) |
| `extreme_value_flagging` (e.g., `|funding_rate| > 0.005` = 50 bps per-event) | flag count recorded | informational only |
| `date_range_coverage` (≥ V2 target range) | 1640995200000 ≤ start; 1775001599999 ≤ end | `research_eligible: false` |
| `alignment_to_signal_bars` (V2 30m signal bar at time `t` aligns to most recent funding event with `funding_time ≤ t` AND `t - funding_time ≤ 8h`) | predeclared rule | per-bar fail-closed if no aligned event |

**Phase 4h does NOT modify v002 funding manifests.**

### 17.4 `metrics` (5-minute granularity inside daily archive)

| Check | Threshold | Action on fail |
|---|---|---|
| `monotone_timestamps` (`create_time` strictly increasing within each daily archive; concatenated archives strictly increasing across days) | true | `research_eligible: false` |
| `duplicate_timestamps` | 0 | `research_eligible: false` |
| `expected_cadence` (5-minute boundary alignment; `create_time mod 300000 == 0`) | 0 violations | `research_eligible: false` |
| `missing_observations` (consecutive 5-minute gap > 5 minutes within a day) | 0 expected per day; documented per-symbol if Binance maintenance creates gaps similar to mark-price gaps | `research_eligible: false` if any day has gaps; `invalid_windows` populated; manifests may carry `research_eligible: false` per Phase 3r §8 precedent until governance is extended for `metrics` family |
| `nonnegative_oi` (`sum_open_interest ≥ 0`; `sum_open_interest_value ≥ 0`) | 0 violations | `research_eligible: false` |
| `bounded_taker_long_short_vol_ratio` (typically 0..∞; Binance returns finite positive values) | non-negative finite | `research_eligible: false` if non-finite or negative |
| `nonnegative_long_short_ratios` (count + sum ratios non-negative finite) | 0 violations | `research_eligible: false` |
| `symbol_consistency_violations` | 0 | `research_eligible: false` |
| `date_range_coverage` (≥ V2 target range; daily archive must cover every day in [2022-01-01, 2026-03-31]) | 0 missing days | `research_eligible: false` |
| `alignment_to_30m_signal_bars` (resampled to 30m for V2 use) | predeclared rule (six 5-minute records per 30m) | per-bar fail-closed if any 5-minute records missing in the 30m window |

**Phase 4h-predeclared invalid-window-handling for `metrics`:** if
upstream Binance maintenance creates gaps in `metrics` similar to
the mark-price 4-gap pattern, Phase 4i MUST record those gaps
verbatim in `invalid_windows` (analogous to Phase 3r §8 mark-price
governance). Phase 4i MUST NOT silently patch, forward-fill, or
interpolate. **The first Phase 4i acquisition MUST report any
detected gaps for operator review before declaring `research_eligible:
true`.**

### 17.5 `aggTrades` (OPTIONAL / DEFERRED)

| Check | Threshold | Action on fail |
|---|---|---|
| `monotone_timestamps` | true | `research_eligible: false` |
| `duplicate_aggTradeId` | 0 | `research_eligible: false` |
| `aggregation_correctness` (price > 0; quantity > 0; `is_buyer_maker` boolean; first/last trade IDs consistent) | 0 violations | `research_eligible: false` |
| `taker_buy_volume_sanity` (sum within 30m window matches kline `taker_buy_volume` to within rounding tolerance) | match within 1e-8 quote-asset units | recorded for cross-check; not blocking |
| `coverage_per_30m_signal_bar` (each 30m bar has ≥1 aggTrade record OR explicit zero-volume window confirmed) | 0 missing bars within trading-day windows | recorded; not blocking unless required as primary source |

**Phase 4h does NOT recommend `aggTrades` acquisition.** It is a
fallback only.

---

## 18. `research_eligible` rules

Phase 4h predeclares strict `research_eligible` rules consistent
with Phase 3p §4.7 and Phase 3r §8:

1. **Core trade-price kline data (30m / 4h).** Any unhandled gap
   (`gaps_detected != 0`) FAILS `research_eligible`. No forward-fill,
   no silent patching, no relaxation. Strict gate.
2. **Required taker-flow data (kline `taker_buy_volume` column).**
   Any null / missing `taker_buy_volume` for a 30m signal bar FAILS
   `research_eligible` for V2 entry features at that bar; the bar
   is excluded from V2 candidate setups (treated as data-stale per
   `live-data-spec.md` §"Live freshness as trading gate").
3. **Required OI / metrics data.** Any gap in `metrics` 5-minute
   coverage at the 30m signal bar boundary FAILS `research_eligible`
   for V2 entry feature 8 (OI delta direction + funding-rate
   percentile band) at that bar; the bar is excluded from V2
   candidate setups. The `metrics` dataset itself FAILS
   `research_eligible` if any day has gaps.
4. **Required funding-rate data.** Any V2 30m signal bar that has no
   completed funding event with `funding_time ≤ t AND t - funding_time
   ≤ 8h` FAILS `research_eligible` for V2 entry feature 8 at that
   bar.
5. **Mark-price gaps.** Phase 3r §8 governance applies verbatim. Mark
   price datasets remain `research_eligible: false` if any gap is
   detected. Phase 4h does NOT change Phase 3r §8.
6. **Forward-fill / interpolation / imputation:** FORBIDDEN across any
   missing core observation. No silent patching. Any deviation MUST
   be predeclared in a separately-authorized governance memo (analogous
   to Phase 3r §8 for mark-price). Phase 4h does NOT predeclare any
   such deviation.
7. **Unknown source coverage.** A dataset whose source coverage cannot
   be verified (e.g., bulk archive month missing, REST pagination
   incomplete) FAILS `research_eligible` until coverage is proven.
   Fail-closed.
8. **Private / authenticated-source dependency.** A dataset that
   requires private / authenticated sources to compute FAILS
   `research_eligible` at design time. Phase 4h FORBIDS adding any
   feature that requires private data.

**Per-feature `research_eligible` semantics:** because V2's spec uses
8 entry features that ALL must align (per Phase 4g §13), failure of
any required dataset for a 30m bar means the entire setup is
research-ineligible at that bar; the bar is excluded from V2 candidate
trades but does NOT propagate to other bars.

---

## 19. Invalid-window handling

Phase 4h predeclares the invalid-window handling rules:

| Scenario | Recorded as | Action |
|---|---|---|
| Trade-price kline gap (`gaps_detected != 0`) | `invalid_windows`: `[{prev_open_time_ms, next_open_time_ms, duration_ms}]` | Dataset `research_eligible: false`; affected V2 setups excluded; **no silent patching** |
| Mark-price kline gap (any) | `invalid_windows`: per Phase 3r §8 verbatim | Dataset `research_eligible: false`; future Q6-style or `mark_price_backtest_candidate` analyses MUST exclude trades whose holding period intersects an invalid window per Phase 3r §8 |
| Metrics record missing | `invalid_windows`: `[{prev_create_time_ms, next_create_time_ms, duration_ms}]` per affected day | Dataset `research_eligible: false`; affected V2 setups excluded |
| Funding-rate event missing (gap > 24h) | per-window record in funding manifest's `invalid_windows` (or in V2's per-bar exclusion log if reusing v002 funding) | V2 setups whose alignment rule fails fail-closed for that bar |
| `aggTrades` missing window (OPTIONAL) | `invalid_windows`: per affected window | recorded; non-blocking unless `aggTrades` is the primary taker-imbalance source (currently NOT) |

**Default rule:** any unrecorded / silently-handled missing
observation FAILS `research_eligible`. **No interpolation. No
forward-fill. No silent omission. No retroactive `research_eligible:
true` after observing a gap.**

**Phase 3q / Phase 3r mark-price precedent applies:** the four upstream
maintenance-window gaps documented for mark-price 5m and mark-price
15m must be re-detected at 30m / 4h granularity in any future
Phase 4i mark-price acquisition. The `invalid_windows` field MUST be
populated verbatim. The dataset MUST carry `research_eligible: false`
unless and until a separately authorized governance memo extends
Phase 3r §8 to non-5m mark-price intervals.

---

## 20. Mark-price data policy

Phase 4h predeclares the V2 mark-price data policy:

- **V2 first backtest** uses `trade_price_backtest` provenance per
  Phase 4g §24. **Mark-price 30m / 4h klines are NOT required for the
  first backtest.**
- A future **`mark_price_backtest_candidate` modeling pass** —
  required for live-readiness validation per Phase 3v §8.5 — DOES
  require 30m / 4h mark-price klines for both symbols. This pass is
  **DEFERRED** until separately authorized.
- **Phase 3r §8 mark-price gap governance applies verbatim** to any
  future 30m / 4h mark-price acquisition. The four upstream
  maintenance-window gaps will be detectable at 30m granularity (each
  gap is at least 30 minutes; some are 24+ hours). At 4h granularity,
  some gaps may be partially absorbed depending on alignment;
  detection logic must check gap windows that span any portion of an
  expected 4h bar.
- **Mark-price stops in runtime / paper / live:** `mark_price_runtime`
  per Phase 3v §8 governance. This is a *runtime* concern, not a
  research data concern. The 30m / 4h mark-price kline acquisition,
  when authorized, supports backtesting the runtime path's stop
  behavior, not the runtime path itself.
- **No mark-price patching.** Phase 4h does NOT propose any change
  to Phase 3r §8 invalid-window-exclusion semantics.

**Phase 4h does NOT acquire any mark-price data.**

---

## 21. Trade-price kline requirements

| Requirement | 30m | 4h |
|---|---|---|
| Symbol | BTCUSDT, ETHUSDT | BTCUSDT, ETHUSDT |
| Source | `data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/...` | same |
| Date range | 2022-01..2026-03 (51 months) | same |
| Records per archive | ~1488 (30m × 31 days) at full month; smaller for Feb / partial months | ~186 (4h × 31 days) at full month |
| Schema | `kline_v1` (existing) | same |
| Columns required | `open_time`, `open`, `high`, `low`, `close`, `volume`, `close_time`, `quote_asset_volume`, `count`, `taker_buy_volume`, `taker_buy_quote_asset_volume`, `ignore` | same |
| `taker_buy_volume` non-null (V2 entry feature 7) | YES | n/a (4h is bias-only; V2 does not compute taker imbalance at 4h) |
| Acquisition style | direct (preferred); 6-bar aggregation from 5m as fallback | direct (preferred); 8-bar aggregation from 30m or 4-bar from 1h-derived as fallback |
| Manifest | `binance_usdm_<symbol>_<interval>__v001` | same |
| Integrity gate | per §17.1 | per §17.1 |

---

## 22. Funding-rate requirements

V2 funding-rate requirements are **fully satisfied by existing v002
funding manifests** (`binance_usdm_btcusdt_funding__v002` and
`binance_usdm_ethusdt_funding__v002`):

| Requirement | Source |
|---|---|
| BTCUSDT funding-rate history, full V2 date range | `binance_usdm_btcusdt_funding__v002` (covers 2022-01-01..2026-03-31) |
| ETHUSDT funding-rate history, full V2 date range | `binance_usdm_ethusdt_funding__v002` (same range) |
| Per-event 8h cadence (variable around DST / maintenance) | preserved as-is |
| Alignment to V2 30m signal bars | Phase 4h-predeclared rule (per §7.C above) |

**Phase 4i (if authorized) MUST NOT re-acquire funding data unless
the operator separately authorizes a new funding manifest version.**
Reusing v002 funding manifests preserves cross-dataset comparability
with retained-evidence verdicts.

**Funding-window-proximity feature:** Phase 4g §27 records funding-window
proximity as observable but not active in V2's first spec. If a
future V2-extension memo activates it, the derivation is from existing
v002 funding event timestamps; no new dataset acquisition is required.

---

## 23. Open-interest requirements

V2 OI requirements are satisfied by future Phase 4i `metrics` daily
archive acquisition (per §7.D and §17.4):

| Requirement | Source |
|---|---|
| BTCUSDT OI history, 5-minute granularity, full V2 date range | `binance_usdm_btcusdt_metrics__v001` (Phase 4i, future) |
| ETHUSDT OI history, 5-minute granularity, full V2 date range | `binance_usdm_ethusdt_metrics__v001` (Phase 4i, future) |
| OI delta direction at 30m bar (V2 entry feature 8 sub-component) | derived from `sum_open_interest` resampled to 30m |
| OI percentile band at 30m bar | derived (trailing N_oi window per Phase 4g §29) |
| Alignment to V2 30m signal bars | resample 6 × 5-minute records per 30m bar; require all 6 records present (else fail-closed per §18 rule 3) |

**Phase 4i (if authorized) acquires `metrics` archives, not a separate
OI archive.** The `metrics` archive simultaneously provides OI, taker
imbalance, and long/short ratio.

---

## 24. Taker-flow / imbalance requirements

V2 taker-imbalance requirement (entry feature 7):

| Source | Role | Granularity |
|---|---|---|
| **klines `taker_buy_volume` column** at 30m | **PRIMARY** for `taker_buy_fraction = taker_buy_volume / volume` at the 30m breakout bar | 30m |
| `metrics` `sum_taker_long_short_vol_ratio` resampled to 30m | Cross-check / sanity validation | 5-minute resampled to 30m |
| `aggTrades` monthly archive | Fallback only (not recommended) | tick |

**Phase 4h-predeclared definition of V2 taker_buy_fraction:**

```
taker_buy_fraction(t) = taker_buy_volume(t) / volume(t)
```

where both columns come from the 30m kline at signal-bar `t`. The
threshold `T_imb_min ∈ {0.55, 0.60}` (Phase 4g §29) gates V2 setups
on `taker_buy_fraction(t) ≥ T_imb_min` for long breakouts (mirror for
shorts: `1 - taker_buy_fraction(t) ≥ T_imb_min`).

**No `aggTrades` acquisition recommended.** klines alone provide the
required `taker_buy_volume` column at 30m granularity.

---

## 25. Volume percentile / UTC-hour bucket derivation

Volume features (Phase 4g entry features 5 and 6) derive from the
30m kline `volume` column:

| Feature | Derivation | Lookback |
|---|---|---|
| Relative volume at bar `t` | `volume(t) / mean(volume(t-L_vol..t-1))` | L_vol = 240 30m bars (5 days) |
| Volume z-score at bar `t` | `(volume(t) - mean) / stdev` over L_vol | L_vol = 240 |
| Volume percentile by UTC hour at bar `t` | percentile of `volume(t)` in trailing distribution of 30m bars *with the same UTC hour* over L_session days | L_session = 60 days |

**UTC hour bucket:** 24 hours × 2 30m bars per hour = 48 30m bars per
day, but the bucket key is the UTC *hour* (00..23), so each hour has
two 30m bars per day. Each session bucket holds `~60 days × 2` = 120
30m bars per UTC-hour-bucket. The percentile is well-defined for any
UTC hour with at least, say, 60 observations (= 30 days), which the
60-day window guarantees.

**No additional dataset family is required.** All derivable from 30m
klines.

---

## 26. Session / timing feature derivation

Per Phase 4g §27:

| Feature | Derivation | Source |
|---|---|---|
| UTC hour bucket (always-recorded) | `floor(open_time_ms / 3600000) % 24` | derived from 30m kline `open_time` |
| Funding-window proximity (recorded; not active in first V2 spec) | `t - last_funding_time_ms`; `next_funding_time_ms - t` | derived from v002 funding event timestamps |

**No additional dataset family is required for timing features.**

---

## 27. Feature-to-dataset mapping

The following table maps every active Phase 4g V2 feature to its
required dataset and classifies feasibility per §6 categories.

### Entry features

| # | Feature | Required dataset(s) | Classification | Phase 4i required? |
|---|---|---|---|---|
| 1 | HTF trend bias state (4h EMA(20)/(50) discrete comparison) | BTCUSDT 4h klines, ETHUSDT 4h klines | available from public bulk archive (4h klines); derivable from 1h-derived v002 as fallback | YES (4h klines acquisition) |
| 2 | Donchian breakout state (signal-timeframe Donchian high(N1) / low(N1)) | BTCUSDT 30m klines, ETHUSDT 30m klines | available from public bulk archive (30m klines); derivable from 5m / 15m as fallback | YES (30m klines acquisition) |
| 3 | Donchian width percentile (compression precondition) | BTCUSDT 30m klines, ETHUSDT 30m klines | derivable from 30m klines (no new acquisition beyond #2) | (covered by #2) |
| 4 | Range-expansion ratio (breakout-bar TR vs. trailing mean) | BTCUSDT 30m klines, ETHUSDT 30m klines | derivable from 30m klines (no new acquisition beyond #2) | (covered by #2) |
| 5 | Relative volume + volume z-score | BTCUSDT 30m klines `volume`, ETHUSDT 30m klines `volume` | derivable from 30m klines (no new acquisition beyond #2) | (covered by #2) |
| 6 | Volume percentile by UTC hour | BTCUSDT 30m klines `volume`, ETHUSDT 30m klines `volume` | derivable from 30m klines + UTC hour derivation (no new acquisition beyond #2) | (covered by #2) |
| 7 | Taker buy/sell imbalance | BTCUSDT 30m klines `taker_buy_volume` column, ETHUSDT 30m klines `taker_buy_volume` column | derivable from 30m klines `taker_buy_volume` (no new acquisition beyond #2). `metrics` `sum_taker_long_short_vol_ratio` available as cross-check. | (covered by #2; `metrics` cross-check is bonus) |
| 8 | OI delta direction + funding-rate percentile band | BTCUSDT `metrics` archive (5-minute OI), v002 BTCUSDT funding manifest; ETHUSDT `metrics` archive, v002 ETHUSDT funding manifest | OI delta requires public bulk archive `metrics` (Phase 4i NEW); funding-rate percentile reuses v002 funding (no new acquisition) | YES (`metrics` acquisition) |

### Exit / regime features

| # | Feature | Required dataset(s) | Classification | Phase 4i required? |
|---|---|---|---|---|
| 1 | Time-since-entry counter | none (clock + entry timestamp only) | derivable from V2 trade record only; no dataset family required | NO |
| 2 | ATR percentile regime (recorded; not acted on as exit) | BTCUSDT 30m klines, ETHUSDT 30m klines | derivable from 30m klines (no new acquisition beyond entry feature #2) | (covered by entry #2) |
| 3 | HTF bias state continuity (recorded; not acted on as exit) | BTCUSDT 4h klines, ETHUSDT 4h klines | derivable from 4h klines (no new acquisition beyond entry feature #1) | (covered by entry #1) |

**Summary:** the minimum Phase 4i acquisition set for V2's first
backtest covers **6 dataset families**:

- 30m klines × 2 symbols (covers entry features 2, 3, 4, 5, 6, 7;
  exit/regime feature 2)
- 4h klines × 2 symbols (covers entry feature 1; exit/regime feature 3)
- `metrics` × 2 symbols (covers entry feature 8 OI sub-component)

(Funding-rate is reused from v002. Time-since-entry feature requires no
data family. Mark-price klines are deferred to a future
`mark_price_backtest_candidate` phase.)

---

## 28. Timeframe coverage requirements

Per Phase 4g §11:

| Timeframe | Role | Acquired? | Resolution |
|---|---|---|---|
| 5m | diagnostic-only (Phase 3q v001-of-5m) | already in repo | research-eligible (trade-price); not eligible (mark-price) |
| 15m | derivation fallback for 30m | already in repo (v002) | research-eligible |
| 30m | **V2 SIGNAL** | **Phase 4i acquisition** (NEW) | research-eligible after acquisition |
| 1h | session / volume bucket; derivation fallback for 4h | already in repo (v002 1h-derived) | research-eligible |
| 4h | **V2 HTF BIAS** | **Phase 4i acquisition** (NEW) | research-eligible after acquisition |
| daily | NOT REQUIRED | n/a | n/a |

---

## 29. Symbol coverage requirements

Per §14:

- **BTCUSDT** USDⓈ-M perpetual: required for V2 first backtest.
- **ETHUSDT** USDⓈ-M perpetual: required for V2 first backtest
  (cross-symbol validation per Phase 4g §31).
- **No additional symbols.**

---

## 30. Date-range requirements

Per §13:

- **Target range:** 2022-01-01 00:00:00 UTC → 2026-03-31 23:59:59.999 UTC.
- **Strict superset of v002 / v001-of-5m coverage.** Cross-dataset
  comparability with retained-evidence verdicts.
- **2026-04 onward EXCLUDED** to avoid freshness drift / partial-month
  issues.

---

## 31. Alignment and timestamp policy

Per `docs/04-data/timestamp-policy.md`:

- All timestamps UTC; canonical representation is Unix milliseconds
  (`int64`).
- **Bar identity:** `(symbol, interval, open_time)`.
- **No look-ahead alignment.** A V2 30m signal at bar `t` (open at
  `t`, close at `t + 30m - 1ms`) may use only:
  - 30m bars with `open_time ≤ t` (current and historical 30m);
  - 4h bars with `open_time + 4h ≤ t + 30m` (most recent COMPLETED 4h
    bar);
  - 1h bars with `open_time + 1h ≤ t + 30m` (most recent COMPLETED
    1h bar, used for session bucket);
  - funding events with `funding_time ≤ t + 30m` (most recent
    completed funding event);
  - `metrics` 5-minute records with `create_time ≤ t + 30m` (most
    recent completed 5-minute records, all 6 within the 30m window);
  - NEVER future or partial bars.
- **Bar-completed-only decisioning.** V2 evaluates the entry rule at
  the close of each 30m bar. The decision uses the JUST-COMPLETED
  30m bar's data. No intrabar entries.
- **No use of future funding / OI / flow values.** Strict
  point-in-time-valid alignment.
- **30m signal bar completion:** required.
- **4h bias bar completion:** required (the most recent fully completed
  4h bar at signal-bar `t`).
- **1h session bucket completion:** required.
- **5m diagnostic-only:** any post-trade diagnostic using 5m data is
  outside V2's primary signal path.

---

## 32. Cost / slippage data assumptions

Phase 4h preserves the existing cost / slippage model verbatim:

- **§11.6 = 8 bps HIGH per side** (16 bps round-trip HIGH). Preserved.
- **MEDIUM-slip cell:** standard backtest reporting cell.
- **LOW-slip cell:** sensitivity cell only.
- **Funding cost:** included in P&L (V2 reuses v002 funding event
  data for funding cost).
- **Fee model:** taker fee 0.04% per side default for USDⓈ-M futures
  (≈ 4 bps per side). The §11.6 HIGH cost cell adds slippage on top.
- **No cost-model relaxation.**
- **No live fee assumption.**
- **No maker-rebate assumption.**

**Phase 4h does NOT acquire any execution-cost data.** All cost
inputs come from the existing locked cost model.

**Future V2 backtest must use the existing cost model unless
separately revised by authorized evidence.**

---

## 33. Data-acquisition execution plan preview

The following preview is for a **future** Phase 4i V2 acquisition phase.
Phase 4h does NOT authorize acquisition.

**Suggested branch name (for future Phase 4i):**
`phase-4i/v2-public-data-acquisition-and-integrity-validation`.

**Suggested acquisition script (for future Phase 4i):**

- File: `scripts/phase4i_v2_acquisition.py` (NEW; Phase 4h does NOT
  create).
- Pattern: standalone orchestrator analogous to
  `scripts/phase3q_5m_acquisition.py`. Public bulk archive only. No
  credentials. No private endpoints. No `prometheus.research.data.*`
  modification. No Interval-enum extension required (the existing
  enum supports 30m, 4h, 5m; only `metrics` and `aggTrades` would
  introduce new categories, which the standalone script can handle
  without modifying the package).
- Inputs: V2 date range (2022-01-01..2026-03-31), symbols (BTCUSDT,
  ETHUSDT), required families (30m klines, 4h klines, `metrics`),
  optional families (markPrice 30m / 4h, aggTrades — DEFERRED unless
  separately authorized).
- Outputs: new `data/raw/...`, `data/normalized/...`, and
  `data/manifests/*.manifest.json` files; integrity-check report
  per §17 rules.

**Allowed sources (Phase 4i constraint):**

- `https://data.binance.vision/data/futures/um/monthly/klines/<SYMBOL>/<INTERVAL>/...`
- `https://data.binance.vision/data/futures/um/monthly/markPriceKlines/<SYMBOL>/<INTERVAL>/...`
  (DEFERRED unless separately authorized)
- `https://data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/...`
- `https://data.binance.vision/data/futures/um/monthly/aggTrades/<SYMBOL>/...`
  (OPTIONAL / DEFERRED)
- Paired `<base-URL>.CHECKSUM` for SHA256 verification.

**No credentials. No private endpoints. No authenticated REST. No
WebSocket. No user stream. No order-book L2 depth. No spot data. No
cross-venue.**

**Acquisition-time SHA256 verification:** every raw archive must be
verified against its paired `.CHECKSUM` before normalization.
Acquisition fails closed on checksum mismatch.

**Normalization to Parquet:** per existing `prometheus.research.data`
conventions (where applicable) or via a Phase 4i standalone
normalizer.

**Manifest generation:** per §16 schema. Generated atomically at the
end of acquisition; partial / failed runs do NOT write a manifest
(fail-closed).

**Integrity report:** generated per §17 rules. If any check FAILS,
Phase 4i acquisition stops for operator review (analogous to Phase
3q's stop-for-review on mark-price gaps).

**Stop conditions for Phase 4i (fail-closed):**

- checksum mismatch on any raw archive;
- missing month / missing day in any required family;
- `gaps_detected != 0` in trade-price klines (strict gate);
- `monotone_timestamps` violation;
- `boundary_alignment_violations` > 0;
- `ohlc_sanity_violations` > 0;
- `volume_sanity_violations` > 0;
- coverage < V2 target range;
- attempt to acquire any private / authenticated endpoint;
- attempt to write secrets or credentials;
- attempt to bypass the public bulk archive.

**Phase 4h does NOT execute any of this.** Phase 4i would be a
separately authorized phase.

---

## 34. What this does not authorize

Phase 4h explicitly does NOT authorize, propose, or initiate any of
the following:

- **V2 data acquisition.** Phase 4i is a separate operator decision.
- **V2 backtest.** Forbidden until Phase 4i is complete and a
  separately authorized V2 backtest phase is briefed.
- **V2 implementation.** Forbidden until V2 backtest evidence is in
  AND a separately authorized implementation phase exists.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.
- **Phase 4i or any successor phase.** Phase 4h is docs-only;
  successor authorization is a separate operator decision.
- **Live exchange-write capability.** Architectural prohibition
  unchanged.
- **Production Binance keys, authenticated APIs, private endpoints,
  user stream, WebSocket, listenKey lifecycle, production alerting,
  Telegram / n8n production routes, MCP, Graphify, `.mcp.json`,
  credentials, exchange-write capability.** None of these is
  touched, enabled, or implied.
- **Strategy implementation, rescue, or new candidate** (other than
  the bounded V2 spec already locked by Phase 4g).
- **Phase 4g V2 strategy-spec re-optimization.** Phase 4h does NOT
  modify Phase 4g selections. If a feasibility blocker is found
  (none identified by Phase 4h), Phase 4h would record it; it
  would not unilaterally edit Phase 4g.
- **R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A revision.**
  Preserved verbatim.
- **Lock change.** §1.7.3 / §11.6 / mark-price stops preserved.
- **Data acquisition / patching / regeneration / modification.**
- **v002 dataset / manifest modification.**
- **Phase 3q v001-of-5m manifest modification.**
- **v003 creation.**
- **Diagnostics / Q1–Q7 rerun / backtests.** None run.
- **Phase 3v stop-trigger-domain governance modification.** Preserved.
- **Phase 3w break-even / EMA slope / stagnation governance
  modification.** Preserved.
- **Phase 3r §8 mark-price gap governance modification.** Preserved.
- **Reconciliation implementation.** Phase 4e reconciliation-model
  design preserved verbatim, not implemented.
- **Paper / shadow / live-readiness / deployment.** Not authorized.

---

## 35. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4i / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched, or
  commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 data acquisition.**
- **No data acquired.** No `data/` artefact modified. No public Binance
  endpoint consulted in code.
- **No implementation code written.** Phase 4h is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env`
  modification.
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4h performs no network I/O
  via code; web research used `WebSearch` tool only against public
  documentation pages.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.** V2 is a new ex-ante hypothesis,
  NOT a re-parameterized successor of any retained-evidence candidate.
- **No 5m strategy / hybrid / retained-evidence successor / new
  variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **No data acquisition / download / patch / regeneration /
  modification.**
- **No data manifest modification.**
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A
  all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g text modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/04-data/data-requirements.md` substantive change.**
- **No `docs/04-data/live-data-spec.md` substantive change.**
- **No `docs/04-data/timestamp-policy.md` substantive change.**
- **No `docs/04-data/dataset-versioning.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md`
  substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive
  change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4h branch.** Per the Phase 4h brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 36. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4h
  deliverables exist as branch-only artefacts pending operator review.
- **Phase 4h output:** docs-only V2 data-requirements / feasibility
  memo + closeout artefact on the Phase 4h branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4h startup).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a executed and merged.
  Phase 4b/4c cleanups merged. Phase 4d review merged. Phase 4e
  reconciliation-model design memo merged. Phase 4f V2 hypothesis
  predeclaration merged. Phase 4g V2 strategy spec merged. Phase 4h
  V2 data-requirements / feasibility memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4h).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code; awaits separately authorized future implementation
  phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements). NOT
  implemented; NOT backtested; NOT validated; NOT live-ready.
- **OPEN ambiguity-log items after Phase 4h:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4h/v2-data-requirements-and-feasibility`
  exists locally and (after push) on `origin/phase-4h/...`. NOT
  merged to main.

---

## 37. Operator decision menu

Phase 4h presents the following operator decision options:

- **Option A — Remain paused.** Procedurally acceptable; Phase 4h
  deliverables exist as branch artefacts. Defers Phase 4i.
- **Option B — Phase 4i: V2 Public Data Acquisition and Integrity
  Validation.** **PRIMARY RECOMMENDATION.** Implement the §33
  acquisition execution plan: acquire 30m klines × 2 symbols, 4h
  klines × 2 symbols, `metrics` × 2 symbols from public bulk
  archives; SHA256-verify; normalize to Parquet; generate manifests
  per §16 schema; run integrity checks per §17; produce a Phase 4i
  acquisition + integrity report analogous to Phase 3q.
  Mark-price 30m / 4h and aggTrades acquisition deferred unless
  separately scoped. Phase 4i would itself be docs-and-data, not
  strategy implementation.
- **Option C — Revise V2 spec or data requirements.** **NOT
  RECOMMENDED.** Phase 4h has not identified any feasibility blocker
  that justifies revising Phase 4g.
- **Option D — Immediate V2 backtest.** **REJECTED.** Cannot be done
  before data is acquired AND would be data-snooping per Bailey/
  Borwein/López de Prado/Zhu 2014.
- **Option E — V2 implementation.** **REJECTED.** Requires successful
  backtest evidence (which does not exist) AND a separate authorization
  (which does not exist).
- **Option F — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of these
  gates is met.

**Phase 4h recommendation: Option B (Phase 4i V2 Public Data
Acquisition and Integrity Validation) primary; Option A (remain
paused) conditional secondary.** No further options recommended.

---

## 38. Next authorization status

**No next phase has been authorized.** Phase 4h's recommendation is
**Option B (Phase 4i V2 Public Data Acquisition and Integrity
Validation) as primary**, with **Option A (remain paused) as
conditional secondary**. Options C / D / E are not recommended;
Option F is forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has been
issued.

The 5m research thread remains operationally complete and closed (per
Phase 3t). The implementation-readiness boundary remains reviewed (per
Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers
remain RESOLVED at the governance level (per Phase 3v + Phase 3w).
The Phase 4a safe-slice scope is implemented (per Phase 4a). The
Phase 4b script-scope quality-gate restoration is complete (per Phase
4b). The Phase 4c state-package quality-gate residual cleanup is
complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete
(per Phase 4d). The Phase 4e reconciliation-model design memo is
complete (per Phase 4e). The Phase 4f V2 hypothesis predeclaration is
complete (per Phase 4f). The Phase 4g V2 strategy spec is complete
(per Phase 4g). The Phase 4h V2 data-requirements / feasibility memo
is complete on this branch (this phase). **Recommended state remains
paused.**
