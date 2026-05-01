# Phase 4j — V2 Metrics Data Governance Memo

**Authority:** Operator authorization for Phase 4j (Phase 4i §"Operator
decision menu" Option B conditional secondary alternative — docs-only
metrics governance memo analogous to Phase 3r §8); Phase 4i (V2 public
data acquisition + integrity validation; partial-pass verdict);
Phase 4h (V2 data requirements / feasibility); Phase 4g (V2 strategy
spec); Phase 4f §22 (V2 hypothesis); Phase 3r §8 (mark-price gap
governance — model precedent for partial-eligibility under strict
per-bar exclusion); Phase 3q (5m supplemental acquisition pattern);
Phase 3p §4.7 (strict integrity gate); Phase 2i §1.7.3 (project-level
locks); `docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/live-data-spec.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4j — **V2 Metrics Data Governance Memo** (docs-only).
Decides how the Phase 4i metrics partial-pass evidence is governed
before any V2 backtest can be considered. **Phase 4j does NOT acquire
data. Phase 4j does NOT modify data, manifests, code, tests, or scripts.
Phase 4j does NOT backtest. Phase 4j does NOT implement V2. Phase 4j
does NOT change Phase 4g V2 strategy-spec selections. Phase 4j does
NOT revise prior verdicts. Phase 4j does NOT authorize paper / shadow /
live / exchange-write.**

**Branch:** `phase-4j/v2-metrics-data-governance`. **Memo date:**
2026-04-30 UTC.

---

## 1. Summary

Phase 4i acquired the six Phase 4h-predeclared minimum V2 dataset
families. Four kline datasets PASS the Phase 4h §17 strict integrity
gate; two metrics datasets FAIL. The metrics failure is driven by
two distinct upstream `data.binance.vision` characteristics:

- intra-day 5-minute missing observations (BTC: 5 699 / ETH: 3 631
  across the 4-year coverage; ~0.03% of expected 446 688 records;
  0 missing daily archives);
- NaN values in **optional** ratio columns
  (`count/sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
  `sum_taker_long_short_vol_ratio`) heavily concentrated in early-2022
  data;

while the **required** `sum_open_interest` and
`sum_open_interest_value` columns are FULLY POPULATED (zero NaN) for
both symbols across the entire 4-year coverage.

Phase 4i did NOT relax the strict gate, did NOT silently patch, did
NOT forward-fill, did NOT interpolate, and stopped for operator
review per the brief failure-path. Phase 4j is the operator-authorized
governance memo that decides what may and may not happen next.

**Phase 4j's recommended governance rule — "Phase 4j §11 metrics
OI-subset partial-eligibility rule"** — adopts the same pattern as
Phase 3r §8 (mark-price gap governance): keep the metrics manifests
GLOBALLY `research_eligible: false`; permit FEATURE-LEVEL use of the
OI subset (`create_time`, `symbol`, `sum_open_interest`,
`sum_open_interest_value`) under strict per-bar exclusion; categorically
forbid use of the optional ratio columns in V2's first backtest;
forbid forward-fill / interpolation / patching; and bind any future
V2 backtest phase to predeclare per-bar exclusion logging in its
brief.

**Phase 4j is docs-only.** **No data acquired. No data modified. No
manifests modified. No code modified. No tests modified. No backtests
run. No implementation. No retained verdict revised. No project lock
changed. No Phase 4g V2 strategy-spec selection changed. No Phase 4f /
4g / 4h text changed.**

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

**Verification (run on the post-Phase-4i-merge tree, captured by
Phase 4j):**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**Recommended next phase:** Merge Phase 4j to record the governance
rule, then authorize a separate **docs-only V2 backtest-plan memo**
(future Phase 4k) under the Phase 4j §11 rule. **Remain paused** is
the conditional secondary. **Immediate V2 backtest is REJECTED.**
**V2 implementation is REJECTED.** **Paper / shadow / live-readiness
/ exchange-write is FORBIDDEN.**

**Recommended state remains paused. No successor phase has been
authorized.**

---

## 2. Authority and boundary

Phase 4j operates strictly inside the post-Phase-4i-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain
  governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
  stagnation governance); Phase 4a's anti-live-readiness statement;
  Phase 4d review; Phase 4e reconciliation-model design memo; Phase 4f
  V2 hypothesis predeclaration; Phase 4g V2 strategy spec; Phase 4h
  V2 data requirements / feasibility memo; Phase 4i V2 acquisition
  + integrity validation.
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
- **Phase 4g V2 strategy-spec selections preserved verbatim.** Phase
  4j does NOT modify Phase 4g §28 active feature set (8 entry + 3
  exit / regime), §11 timeframe matrix (signal 30m, bias 4h, session
  / volume bucket 1h), §29 threshold grid (512 variants), §30 M1 /
  M2 / M3 mechanism-check decomposition, or §22–§24 governance
  labels.
- **Phase 4i manifests preserved verbatim.** All six Phase 4i
  manifests (`binance_usdm_<symbol>_<interval-or-metrics>__v001.manifest.json`)
  remain unchanged. The two metrics manifests retain
  `research_eligible: false`.

Phase 4j adds a **new** governance rule without modifying any
existing rule, threshold, dataset, manifest, verdict, lock, prior
phase memo, or Phase 4i manifest. The new rule is forward-looking
only and is binding on any future V2 backtest phase that uses the
metrics datasets.

---

## 3. Starting state

```text
branch:           phase-4j/v2-metrics-data-governance
parent commit:    17ebb755ce32ccc5d605329d9972df2e4ce2f140 (post-Phase-4i-merge housekeeping)
working tree:     clean before memo authoring
main:             17ebb755ce32ccc5d605329d9972df2e4ce2f140 (unchanged)

Phase 4a foundation:                                 merged.
Phase 4b/4c cleanup:                                 merged.
Phase 4d review:                                     merged.
Phase 4e reconciliation-model design memo:           merged.
Phase 4f V2 hypothesis predeclaration:               merged.
Phase 4g V2 strategy spec:                           merged.
Phase 4h V2 data-requirements / feasibility memo:    merged.
Phase 4i V2 public data acquisition + integrity:     merged (partial-pass; metrics not eligible).

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false (Phase 3r §8 governs).
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible.
```

---

## 4. Why this memo exists

Phase 4i's partial-pass result presents the project with a binary
question: either keep the metrics datasets globally
`research_eligible: false` AND block all V2 backtesting (Option A
in Phase 4i's decision menu), OR define a precise, predeclared,
immutable governance rule that lets V2 use the OI subset of the
metrics datasets while keeping global ineligibility intact AND while
forbidding any forward-fill / interpolation / patching (Phase 4i
decision-menu Option B).

Phase 4i did NOT propose either. Phase 4j is the operator-authorized
docs-only memo that picks one and writes it down with the same
binding-rule discipline Phase 3r §8 used for mark-price gaps. The
parallel is exact:

| Aspect | Phase 3r §8 (mark-price) | Phase 4j (metrics OI) |
|---|---|---|
| Failed strict gate | mark-price 5m datasets (4 gaps each) | metrics datasets (intra-day 5m gaps + NaN in optional ratio cols) |
| Manifest global status | `research_eligible: false` | `research_eligible: false` |
| Required-for-V2 fields available? | n/a (Q6 was diagnostic, not V2) | YES (`sum_open_interest` fully populated) |
| Optional / non-required fields impact | n/a | NaN concentration in optional ratio columns is the major failure driver |
| Governance pattern | per-trade Q6 exclusion if trade window intersects gap | per-bar V2-setup exclusion if required OI record is missing or NaN |
| Patching / forward-fill / interpolation | categorically forbidden | categorically forbidden |
| Verdict revision implication | none — Q6 is descriptive | none — V2 partial-eligibility does not affect retained verdicts |
| Future authorization gating | Q6 execution requires separate authorization | V2 backtest requires separate authorization |
| Memo immutable from operator approval | yes | yes |

The pattern is: **partial-eligibility under strict per-record
exclusion, with NO data alteration, AND no implicit authorization of
the dependent operation.**

Phase 4j is **governance discipline**, not strategy execution. It
does not authorize, prepare for, or imply any V2 backtest, V2
implementation, paper / shadow run, live-readiness work, or
successor phase.

---

## 5. Relationship to Phase 4i

Phase 4i (merged at `a2c414e8...` with housekeeping at `17ebb755...`)
delivered three artefacts:

1. The standalone acquisition orchestrator
   `scripts/phase4i_v2_acquisition.py`.
2. Six new manifests in `data/manifests/`: 4 with
   `research_eligible: true` (klines), 2 with
   `research_eligible: false` (metrics).
3. Phase 4i acquisition + integrity report and closeout in
   `docs/00-meta/implementation-reports/`.

Phase 4i's decision menu identified Option B (a docs-only metrics
governance memo analogous to Phase 3r §8) as conditional secondary
recommendation. Phase 4j is exactly that memo.

Phase 4j does NOT modify Phase 4i. Phase 4i manifests remain
verbatim. Phase 4i report remains verbatim. Phase 4i closeout
remains verbatim. The Phase 4i acquisition script
(`scripts/phase4i_v2_acquisition.py`) is NOT modified.

Phase 4j adds *only* this docs-only governance memo and its
closeout artefact.

---

## 6. Phase 4i metrics evidence recap

Phase 4i's verdict, recorded verbatim:

- **Four kline datasets are research_eligible:**
  - `binance_usdm_btcusdt_30m__v001` (74 448 bars; 0 gaps; full
    coverage 2022-01-01..2026-03-31).
  - `binance_usdm_ethusdt_30m__v001` (74 448 bars; 0 gaps; full
    coverage).
  - `binance_usdm_btcusdt_4h__v001` (9 306 bars; 0 gaps; full
    coverage).
  - `binance_usdm_ethusdt_4h__v001` (9 306 bars; 0 gaps; full
    coverage).

- **BTCUSDT metrics is NOT research_eligible:**
  - 446 555 / 446 688 records (133 short of the expected
    51-month-day-by-288-record count).
  - 5 699 missing 5-minute observations (recorded as gap intervals
    in `quality_checks.gap_locations` and `invalid_windows`).
  - 91 840 rows with at least one NaN in optional ratio columns.
  - 0 missing daily archives (all 1551 daily ZIPs from
    `data.binance.vision/data/futures/um/daily/metrics/BTCUSDT/`
    successfully fetched and SHA256-verified).
  - **Required `sum_open_interest` and `sum_open_interest_value`
    columns are FULLY POPULATED (zero NaN) across the entire 4-year
    coverage.**

- **ETHUSDT metrics is NOT research_eligible:**
  - 446 555 / 446 688 records (same 133-record shortfall pattern).
  - 3 631 missing 5-minute observations.
  - 91 841 rows with at least one NaN in optional ratio columns.
  - 0 missing daily archives.
  - **Required `sum_open_interest` and `sum_open_interest_value`
    columns are FULLY POPULATED (zero NaN) across the entire 4-year
    coverage.**

- **NaN values are concentrated in OPTIONAL ratio columns,
  especially early 2022.** Phase 4i §"Metrics integrity results"
  reports the per-month NaN distribution: in 2022-01, both symbols
  have ~97% NaN in `count/sum_toptrader_long_short_ratio` and
  `sum_taker_long_short_vol_ratio` and ~60% NaN in
  `count_long_short_ratio`; in 2026-03, both symbols have 0% NaN
  in all ratio columns. Binance progressively backfilled or extended
  these ratio columns in the public archive over time.

- **Phase 4i did NOT relax strict gates and stopped for operator
  review** per the brief failure-path.

---

## 7. Metrics failure taxonomy

The Phase 4i metrics failure has two root causes that must be
governed separately because they have different remedies:

### 7.1 Cause A — intra-day 5-minute missing observations

**Symptom.** Within otherwise-present daily archives, individual
5-minute records are absent. Sample windows from
`quality_checks.gap_locations` (BTCUSDT):

```text
2023-09-12 08:35 UTC -> 2023-09-12 08:55 UTC   ( 20 min gap;  3 records missing)
2024-02-16 13:30 UTC -> 2024-02-17 00:00 UTC   (630 min gap; 126 records missing -- single largest)
2024-03-03 23:55 UTC -> 2024-03-04 00:05 UTC   ( 10 min gap;  1 record missing)
2024-03-04 05:30 UTC -> 2024-03-04 05:35 UTC   (  5 min gap;  0 records missing -- boundary record offset)
2024-03-04 05:35 UTC -> 2024-03-04 05:40 UTC   (  5 min gap;  0 records missing)
```

**Per-symbol total.** BTCUSDT: 5 699 missing 5-minute observations
across 4 years. ETHUSDT: 3 631 missing observations.

**Affected V2 fields.** When a 5-minute record is absent, ALL
columns at that timestamp are absent — including the required
`sum_open_interest` and `sum_open_interest_value` columns. The
30m bars whose 5-minute window contains any absent record are
affected at the OI feature level.

**Scope estimate.** 5 699 missing 5-minute records / 6 records per
30m window ≈ 950 affected 30m bars per symbol (BTC), some sharing
the same 30m window. Expected exclusion fraction at the 30m signal
level: roughly 0.5 % to 1.5 % of the 74 448 30m bars (depending on
how clustering is handled), to be measured by the future V2
backtest phase.

**Remedy.** Per-bar exclusion. No patching.

### 7.2 Cause B — NaN values in optional ratio columns concentrated early-2022

**Symptom.** When a 5-minute record IS present, individual ratio
columns may have empty / quoted-empty values that the Phase 4i
parser converts to `NaN`. The required `sum_open_interest` and
`sum_open_interest_value` columns are NOT affected.

**Per-symbol total.** BTCUSDT: 91 840 rows with ≥ 1 NaN in optional
ratio columns. ETHUSDT: 91 841 rows. Concentrated in early-2022:
~97% NaN in 2022-01 ratio columns; ~0% NaN by 2026-03.

**Affected V2 fields.** None of the four affected columns
(`count/sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
`sum_taker_long_short_vol_ratio`) is part of the locked Phase 4g
V2 active feature set. Phase 4g §28 lists `long/short ratio` and
`metrics taker imbalance cross-check` as **optional features
documented but NOT activated** in V2's first spec.

**Remedy.** Forbid use of optional ratio columns in V2's first
backtest. Their NaN values do not constrain the OI subset.

### 7.3 Why these two causes need separate governance

- Cause A affects the V2 OI feature directly (the OI delta feature
  computation requires OI values at 30m bar boundaries). Per-bar
  exclusion is the correct remedy.
- Cause B affects only optional V2 features that are NOT activated.
  Forbidding their use is sufficient.

If the governance rule treated both causes the same way (e.g., per-bar
exclude every 30m bar containing any NaN in any column), the V2
backtest would lose ~20 % of its early-2022 trade population for
reasons unrelated to OI feature validity. That would be a
disproportionate exclusion driven by inactive features. Separating
the two causes preserves V2 statistical power for what V2 actually
uses.

---

## 8. Required versus optional metrics fields

Per the Phase 4g V2 spec (§28 active feature set):

### 8.1 Required for locked Phase 4g V2 first-backtest

| Field | Use in V2 |
|---|---|
| `create_time` | Per-bar timestamp alignment (UTC ms; see §13). |
| `symbol` | Symbol identity check (BTCUSDT or ETHUSDT). |
| `sum_open_interest` | OI delta direction feature (V2 entry feature 8 sub-component (a)). |
| `sum_open_interest_value` | OPTIONAL secondary OI representation; included in OI subset for completeness; not strictly required by V2 §28 but reported in the Phase 4i evidence. |

### 8.2 Not required for locked Phase 4g V2 first-backtest

| Field | Reason not required |
|---|---|
| `count_toptrader_long_short_ratio` | Documented in Phase 4g §28 as **optional** (long/short ratio); NOT activated in V2's first spec. |
| `sum_toptrader_long_short_ratio` | Same — optional. |
| `count_long_short_ratio` | Same — optional. |
| `sum_taker_long_short_vol_ratio` | Optional / cross-check only. V2 entry feature 7 (taker buy/sell imbalance) uses kline `taker_buy_volume` from 30m klines as the PRIMARY source per Phase 4h §24, NOT the metrics ratio. |

### 8.3 Explicit notes (preventing rescue framing)

- **V2 taker imbalance uses kline `taker_buy_volume` from 30m
  klines, NOT metrics `sum_taker_long_short_vol_ratio`.** Phase 4h
  §24 fixed this; Phase 4j confirms it. The metrics ratio is a
  cross-check (reported but not active). Its NaN values do NOT
  block V2's taker-imbalance feature.
- **Funding-rate percentile uses existing v002 funding manifests,
  NOT metrics.** Phase 4h §22 / §B fixed this; Phase 4j confirms it.
  Metrics-family non-eligibility does NOT block V2's funding-rate
  feature.
- **Optional ratio fields MUST NOT be used in V2 first backtest
  unless a later separately authorized strategy-spec amendment
  activates them.** Phase 4j makes this binding (§14 below).

---

## 9. V2 feature impact analysis

Mapping each Phase 4g V2 feature to its impact under the Phase 4i
metrics partial-pass:

### 9.1 Entry features (Phase 4g §28)

| # | Feature | Required dataset | Impact under Phase 4i |
|---|---|---|---|
| 1 | HTF trend bias state (4h EMA(20)/(50)) | 4h klines | NONE — 4h klines research-eligible. |
| 2 | Donchian breakout state | 30m klines | NONE — 30m klines research-eligible. |
| 3 | Donchian width percentile | 30m klines | NONE. |
| 4 | Range-expansion ratio | 30m klines | NONE. |
| 5 | Relative volume + volume z-score | 30m klines `volume` | NONE. |
| 6 | Volume percentile by UTC hour | 30m klines `volume` + UTC hour | NONE. |
| 7 | Taker buy/sell imbalance | 30m klines `taker_buy_volume` | NONE — kline `taker_buy_volume` fully populated; metrics taker ratio (cross-check) is unused. |
| 8 | OI delta direction + funding-rate percentile band | metrics OI subset + v002 funding | **AFFECTED** — OI delta requires per-bar exclusion under Phase 4j §11. Funding-rate percentile is unaffected. |

### 9.2 Exit / regime features (Phase 4g §28)

| # | Feature | Required dataset | Impact under Phase 4i |
|---|---|---|---|
| 1 | Time-since-entry counter | none | NONE. |
| 2 | ATR percentile regime | 30m klines | NONE. |
| 3 | HTF bias state continuity | 4h klines | NONE. |

### 9.3 Summary

Of 11 active V2 features (8 entry + 3 exit/regime), **only 1**
(entry feature 8 OI sub-component) is affected by the Phase 4i
metrics partial-pass. The remaining 10 features are unaffected
because they depend on klines (research-eligible) or v002 funding
(research-eligible).

The Phase 4j governance rule is therefore narrowly focused: define
exactly what happens to the OI sub-component when an aligned 5-minute
metrics record is missing or has NaN in the OI columns (the latter
case empirically does not occur in the Phase 4i evidence — OI
columns are 0% NaN).

---

## 10. Governance options considered

Phase 4j evaluates seven options, mirroring the Phase 4i decision
menu but framed at the governance-rule level:

### 10.1 Option A — Keep metrics globally ineligible AND block all V2 backtesting

**Description.** No metrics use whatsoever. V2 backtest is blocked
indefinitely. Status quo of Phase 4i's "stop for operator review"
becomes permanent.

**Pros.** Procedurally safest. Preserves strict gate without any
exception.

**Cons.** Stalls V2 even though V2-required fields
(`sum_open_interest`) are fully populated. The Phase 4i evidence
shows that the failures are dominated by NaN in OPTIONAL columns,
not by failures in V2-required columns. Option A applies a
disproportionate remedy.

**Verdict.** **Procedurally acceptable but not recommended.** It
trades V2 progress for predeclaration purity that V2 does not
actually need.

### 10.2 Option B — Keep metrics globally `research_eligible: false`, BUT allow OI-subset partial-use under strict per-bar exclusion

**Description.** Metrics manifests remain `research_eligible: false`
globally (no manifest modification). At the FEATURE level, V2's OI
delta feature may use the OI subset (`create_time`, `symbol`,
`sum_open_interest`, `sum_open_interest_value`) provided that:

1. all six 5-minute records aligned to the 30m signal bar's window
   are present and have non-NaN OI columns (the latter is
   empirically always satisfied by the Phase 4i evidence; the
   former is not always satisfied);
2. any 30m signal bar that fails the alignment / completeness check
   is EXCLUDED from V2 candidate setup generation (per-bar
   exclusion);
3. optional ratio columns are NOT used by the feature pipeline;
4. no forward-fill, no interpolation, no patching, no synthetic
   observations, no silent omission;
5. exclusions are logged as `metrics_oi_missing_or_invalid` in any
   future V2 backtest report.

**Pros.** Preserves V2 progress without compromising data integrity.
Mirrors Phase 3r §8 pattern (proven precedent). Per-bar exclusion is
mechanically sound — affected bars are flagged, counted, and reported.
The OI columns are FULLY POPULATED in the Phase 4i evidence, so the
per-bar exclusion fires only on the structural intra-day gap pattern
(Cause A), not on the early-2022 NaN pattern (Cause B).

**Cons.** Adds a small per-bar bookkeeping overhead in any future V2
backtest. Requires a separately authorized future V2 backtest brief
to predeclare the per-bar exclusion implementation.

**Verdict.** **Recommended.** This is the only forward path that
preserves V2 while respecting the integrity evidence.

### 10.3 Option C — Patch / forward-fill / interpolate missing metrics records

**Description.** Treat each absent 5-minute record as if it were the
last observed record (or interpolate between adjacent records).

**Pros.** None — this is data fabrication.

**Cons.** **REJECTED.** Phase 3r §8 categorically forbids this
pattern. Phase 4h §17.4 and §19 forbid this pattern. Phase 4i §17
forbids this pattern. Patching introduces synthetic observations
that the Phase 4i acquisition explicitly avoided. Any patched data
would invalidate the integrity guarantees.

**Verdict.** **REJECTED — data snooping / data fabrication.**

### 10.4 Option D — Drop early-2022 or affected months

**Description.** Truncate the V2 date range to start in (e.g.)
2023-01 or skip months containing intra-day metrics gaps.

**Pros.** None — this is selection by inspection of failure
distribution.

**Cons.** **REJECTED.** Selecting the date range based on observed
data quality is a form of post-hoc parameter tuning (Bailey /
Borwein / López de Prado / Zhu 2014). The V2 backtest would have a
date range chosen to maximize apparent integrity, which is
indistinguishable from cherry-picking the period where the strategy
might happen to work. Phase 4g §13 / §11 fixed the V2 date range
*before* any data was inspected; Option D would rewrite that
decision after seeing data — exactly the predeclaration violation
Phase 4f §17 / Phase 4g §6 forbid.

**Verdict.** **REJECTED — predeclaration violation / cherry-picking.**

### 10.5 Option E — Acquire `aggTrades` to replace metrics optional ratio columns

**Description.** Instead of relying on metrics ratio columns,
acquire tick-level `aggTrades` and derive equivalent ratios at 30m
granularity.

**Pros.** Hypothetically replaces the early-2022 NaN data with
authoritative tick-derived equivalents.

**Cons.** Not relevant to the V2-required OI feature, which is what
fails in Phase 4i. `aggTrades` cannot replace OI; OI is per-instant
position state, not derivable from trades. The optional ratio
columns are NOT activated in V2's first spec, so replacing them adds
data acquisition burden for no V2 benefit. Phase 4h §7.E and Phase 4i
§"Operator decision menu" Option D both recommend against `aggTrades`
acquisition.

**Verdict.** **NOT RECOMMENDED.** `aggTrades` acquisition does not
solve the Phase 4i metrics issue and is not relevant to V2's first
backtest.

### 10.6 Option F — Remove the OI feature from V2

**Description.** Modify Phase 4g V2 spec to drop entry feature 8
(OI delta direction + funding-rate percentile band), reducing the
active entry feature count from 8 to 7.

**Pros.** Eliminates the metrics dependency entirely. V2 first
backtest could proceed using only kline-derived features and v002
funding.

**Cons.** Modifying Phase 4g after merge violates the predeclaration
discipline that Phase 4g enforces. Removing a feature in response to
data quality is a softer form of cherry-picking — it changes the
strategy spec to fit observed data convenience. Phase 4g §6 / §31
preserve the V2 spec selections; modifying them in Phase 4j would
require explicit operator authorization to revise Phase 4g, which
the Phase 4j brief explicitly forbids ("Do not change Phase 4g V2
strategy-spec selections").

**Verdict.** **NOT RECOMMENDED unless Option B is rejected.** The
Phase 4j brief explicitly says "Do not remove the OI feature from V2
in Phase 4j." Phase 4j honours this constraint.

### 10.7 Option G — Proceed to V2 backtest without governance

**Description.** Run the V2 backtest immediately, treating absent
metrics records as zero / ignore / skip without explicit governance.

**Pros.** None.

**Cons.** **REJECTED.** Phase 4i explicitly stops for operator
review when any family is not research-eligible. Backtesting without
explicit per-bar exclusion logic would mean the backtest implicitly
forward-fills or silently skips, which Phase 4h §18 / §19 / Phase
3r §8 / Phase 3p §4.7 / Phase 4i §17 all categorically forbid. The
V2 backtest would also have undocumented behavior in
metrics-affected bars, making its results uninterpretable.

**Verdict.** **REJECTED — integrity violation, would invalidate any
V2 backtest result.**

### 10.8 Summary table

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| A — Block all V2 backtest | safest predeclaration | stalls V2 indefinitely | acceptable but not recommended |
| **B — OI-subset partial-use under per-bar exclusion** | **preserves V2 + integrity; mirrors Phase 3r §8** | **needs per-bar bookkeeping in future backtest** | **RECOMMENDED** |
| C — Patch / forward-fill / interpolate | none | data fabrication | REJECTED |
| D — Drop early-2022 / affected months | none | predeclaration violation / cherry-picking | REJECTED |
| E — Acquire `aggTrades` | replaces optional ratios | not relevant to OI; not in V2 first spec | not recommended |
| F — Remove OI feature from V2 | eliminates metrics dep | modifies Phase 4g; forbidden by Phase 4j brief | not recommended (Phase 4j brief constraint) |
| G — Proceed without governance | none | integrity violation | REJECTED |

---

## 11. Recommended governance rule

**Phase 4j §11 metrics OI-subset partial-eligibility rule.**

The following is the formally binding governance rule. It is
**immutable from operator approval forward** (analogous to Phase 3r
§8). Any future V2 backtest phase MUST obey it. Any future change to
this rule requires a separately authorized governance memo amending
Phase 4j §11 explicitly.

### 11.1 Rule statement

The rule is named **"Phase 4j §11 metrics OI-subset partial-eligibility
rule"** and is stated below in its full normative form.

1. **Metrics manifests remain globally `research_eligible: false`.**
   Phase 4j does NOT modify the Phase 4i `binance_usdm_btcusdt_metrics__v001.manifest.json`
   or `binance_usdm_ethusdt_metrics__v001.manifest.json` files. The
   `research_eligible: false` field is preserved verbatim. Phase 4i
   `quality_checks.gap_locations`, `invalid_windows`, and
   `nonfinite_violations` are preserved verbatim. No corrected
   manifest is created. No v002 metrics manifest is created. No v003
   is created.
2. **Feature-level partial-eligibility for the OI subset only.**
   Future V2 backtest phases (if ever authorized) MAY use the
   metrics OI subset — defined as `create_time`, `symbol`,
   `sum_open_interest`, `sum_open_interest_value` — for V2 entry
   feature 8 OI sub-component computation. This feature-level
   partial-use does NOT affect the global `research_eligible: false`
   manifest status.
3. **Optional ratio columns remain feature-ineligible.** The columns
   `count_toptrader_long_short_ratio`, `sum_toptrader_long_short_ratio`,
   `count_long_short_ratio`, and `sum_taker_long_short_vol_ratio` are
   `feature_eligible: false` for V2's first backtest. They MUST NOT
   be read by the V2 feature pipeline, MUST NOT be used for any
   filter, label, diagnostic, or post-hoc interpretation, and MUST
   NOT be used to derive any V2 entry, exit, or regime feature. NaN
   values in these columns DO NOT invalidate OI-subset feature
   eligibility *if and only if* the optional ratio columns are not
   accessed by the feature pipeline.
4. **Per-bar exclusion test.** For each 30m V2 candidate signal bar
   at signal-decision time `T` (= the signal bar's open_time + 30
   minutes − 1ms close-time, expressed as UTC ms), the future V2
   backtest phase MUST determine the *aligned 5-minute metrics
   window* — i.e., the six 5-minute records with `create_time` in
   `[T_open, T_close]` where `T_open` is the 30m bar's open_time
   and `T_close = T_open + 30 * 60 * 1000 - 1`. The aligned window
   contains six expected records at `T_open + 0`, `+ 5min`,
   `+ 10min`, `+ 15min`, `+ 20min`, `+ 25min` (5-minute boundary
   records). A 30m signal bar is **OI-feature-eligible** if and
   only if ALL six aligned 5-minute records are present AND each
   has non-NaN `sum_open_interest` AND non-NaN
   `sum_open_interest_value`. Any 30m signal bar that fails the
   alignment / completeness check is EXCLUDED from V2 candidate
   setup generation entirely (the bar produces zero V2 candidate
   setups, regardless of other features' values).
5. **No forward-fill, no interpolation, no imputation, no
   replacement, no synthetic OI data.** No V2 feature pipeline may
   use any value derived from any source other than the published
   `data.binance.vision/data/futures/um/daily/metrics/<SYMBOL>/`
   archive at the relevant `create_time`. No statistical
   imputation. No interpolated record. No "missing record treated
   as last observed." No OI reconstructed from open-interest REST
   snapshots. No OI extrapolated from price / volume.
6. **Exclusion must be counted and reported.** The future V2
   backtest output MUST include an exclusion-counts table with at
   minimum the following columns:
   - Symbol (BTCUSDT, ETHUSDT).
   - Date (UTC).
   - 30m bar `open_time` (UTC ms).
   - Exclusion reason (`metrics_oi_missing_or_invalid`).
   - Number of 30m bars excluded per day.
   - Cumulative number of bars excluded per symbol.
7. **Sensitivity analysis MUST be reported.** The future V2 backtest
   output MUST include a sensitivity report comparing:
   - main-cell V2 results (OI-feature-eligible bars only); and
   - sensitivity-cell V2 results (a degenerate variant that ALSO
     excludes any 30m bar whose date contains ANY metrics
     `invalid_window`, regardless of whether the bar's specific
     30m window is OI-feature-eligible — this is a stricter
     "exclude entire affected days" sensitivity).
   The two cells must be comparable; if they materially diverge
   (e.g., main-cell statistics differ from sensitivity-cell by
   more than predeclared thresholds), the V2 backtest must report
   the divergence and stop for operator review before claiming
   results.
8. **No automatic prior-verdict revision.** No V2 backtest result —
   pass, fail, or partial — may by itself revise R3
   baseline-of-record, R2 FAILED, F1 HARD REJECT, D1-A MECHANISM
   PASS / FRAMEWORK FAIL — other, or any §10.3 / §10.4 / §11.3 /
   §11.4 / §11.6 threshold. Verdict revision requires a separately
   authorized formal reclassification phase with predeclared
   evidence thresholds.
9. **No strategy rescue, no parameter change, no live-readiness
   implication.** V2 backtest outputs under Phase 4j §11 are
   research evidence only. They cannot license:
   - Optional ratio-column activation (forbidden by §11.3).
   - V2 strategy-spec parameter change.
   - V2 implementation authorization.
   - Stop policy revision.
   - §1.7.3 mark-price-stop lock revision.
   - Any retained-evidence candidate revision.
   - Any paper / shadow / Phase 4 / live-readiness / deployment
     authorization.
10. **No silent rule revision.** This Phase 4j §11 rule is itself
    predeclared and immutable from the Phase 4j commit forward. Any
    future change requires a separately authorized governance memo
    amending Phase 4j §11 explicitly.
11. **Exclusion test must be predeclared in any future V2 backtest
    brief.** Before any V2 backtest computation begins, the V2
    backtest-plan phase brief MUST specify the exact algorithm for
    the per-bar exclusion test. The brief must be predeclared on
    `main` before any V2 backtest runs. Implementation of the test
    must match the predeclared algorithm exactly; deviations must
    abort the backtest and produce a failure report instead of
    partial output.
12. **Optional ratio activation requires separate operator
    authorization.** If a future operator-approved phase wishes to
    activate any of the four optional ratio columns
    (`count/sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
    `sum_taker_long_short_vol_ratio`) as a V2 feature or filter,
    that activation requires:
    - a separately authorized strategy-spec amendment phase
      modifying Phase 4g §28 (the active feature set bound; ≤8 entry
      + ≤3 exit / regime is binding per Phase 4f §23, so any new
      optional-feature activation must displace an existing active
      feature OR remain inactive);
    - a separately authorized governance memo amending Phase 4j §11
      to relax the §11.3 prohibition;
    - explicit operator approval recorded in the project state.
    Phase 4j §11 itself does NOT authorize any of these.

### 11.2 Plain-English restatement of the rule

> *V2 may use OI from the metrics archive but must drop any 30m bar
> where any of the six aligned 5-minute records is missing or has
> NaN OI. The metrics manifests stay marked ineligible. The optional
> ratio columns must not be touched. No forward-fill, no
> interpolation, no patching. Excluded bars must be counted and
> reported. A sensitivity analysis comparing main-cell vs.
> exclude-entire-affected-days must be reported. The rule never
> revises verdicts, never licenses backtest authorization, and is
> immutable from operator approval forward.*

### 11.3 Why this rule is the right shape

- **It mirrors the Phase 3r §8 pattern exactly.** Phase 3r §8 is the
  proven precedent for the "manifest globally ineligible + per-trade
  exclusion + no patching + immutable rule" governance pattern. Phase
  4j §11 transposes Phase 3r §8 from per-trade (Q6) to per-bar (V2
  candidate setup).
- **It separates Cause A (intra-day gaps) from Cause B (NaN in
  optional ratios)** per §7.3. Cause A is handled by per-bar
  exclusion; Cause B is handled by forbidding optional ratio access.
- **It binds future phases without authorizing them.** Phase 4j §11
  is forward-looking only. It does NOT authorize a V2 backtest. It
  describes what the future V2 backtest must do *if* it is ever
  authorized.
- **It preserves the V2 spec verbatim.** No V2 features removed
  (Option F rejected). No V2 date range modified (Option D rejected).
  No V2 spec amendment (Phase 4g preserved).
- **It preserves the Phase 4i evidence verbatim.** No manifest
  modification (manifest preservation §11.1). No data modification.
- **It preserves all retained verdicts.** §11.8 explicitly forbids
  any V2-induced retained-verdict revision.

---

## 12. Metrics global eligibility rule

Phase 4j §11.1 verbatim. Restated for clarity:

- BTCUSDT and ETHUSDT metrics manifests **remain
  `research_eligible: false`** at the global manifest level.
- Global manifest status is **NOT changed** by Phase 4j.
- Phase 4j does **NOT modify manifests**.
- All Phase 4i `quality_checks` fields, `invalid_windows`, and
  `gap_locations` lists are preserved verbatim.
- No corrected manifest is created.
- No v002 metrics manifest is created.
- No v003 dataset is created.

---

## 13. OI-subset partial-use rule

Phase 4j §11.2 verbatim. Restated for clarity:

The OI subset is defined as exactly four columns:

- `create_time` (UTC ms; alignment timestamp);
- `symbol` (identity check; BTCUSDT or ETHUSDT);
- `sum_open_interest` (open interest in base-asset units; V2 OI
  feature input);
- `sum_open_interest_value` (open interest in quote-asset units;
  reported but not strictly required by Phase 4g §28).

The OI subset MAY be treated as `feature_eligible: true` for V2's
first backtest, **provided all per-bar alignment and
missing-observation rules pass** (per §11.4 / §11.5 / §11.6 above).

This feature-level eligibility flag is a future-V2-backtest-phase
implementation concern. Phase 4j does NOT add a `feature_eligible`
field to the manifests; it does NOT modify manifests at all. The
flag exists only as a future-V2-backtest-phase implementation
contract.

---

## 14. Optional ratio-column rule

Phase 4j §11.3 verbatim. Restated for clarity:

The four optional ratio columns —

- `count_toptrader_long_short_ratio`;
- `sum_toptrader_long_short_ratio`;
- `count_long_short_ratio`;
- `sum_taker_long_short_vol_ratio` —

remain `feature_eligible: false` for V2's first backtest. They
MUST NOT be:

- read by the V2 feature pipeline,
- used for any filter (entry, exit, regime, cooldown, sizing,
  whitelist, blacklist),
- used for any label or post-hoc classification,
- used for any diagnostic computation that affects V2 decisions,
- used for any sensitivity analysis variant that V2 reports as
  primary,
- used to derive any V2 entry, exit, or regime feature.

NaN values in these columns DO NOT invalidate OI-subset feature
eligibility *if and only if* the optional ratio columns are not
accessed by the feature pipeline. This is the central decoupling
that makes Phase 4j §11 work: the early-2022 NaN concentration is
isolated to columns that V2's first backtest never touches.

---

## 15. Missing-observation handling

Per Phase 4j §11.4 / §11.5:

- **No forward-fill.** No "use the last observed OI value when this
  5-minute record is absent."
- **No interpolation.** No linear / spline / smoothed estimate
  between adjacent records.
- **No patching.** No reconstructed records.
- **No synthetic observations.** No reconstructed OI from REST
  snapshots, price-volume reconstruction, or any other source.
- **No silent omission.** Excluded bars MUST be logged and counted.
- **30m signal bar exclusion criterion.** Any 30m V2 signal bar
  whose six aligned 5-minute metrics records are NOT all present
  AND non-NaN in OI columns is excluded from candidate setup
  generation. This is the "stricter completed-record-at-bar-close
  rule" the Phase 4j brief mentioned: ALL six 5-minute records must
  be present (not just the last one).
- **Justification for the stricter rule:** an OI delta computation
  uses the change in OI across the 30m window. If only the last
  5-minute record is required, partial-window OI changes could be
  interpreted from incomplete data; requiring all six aligned
  records ensures the 30m OI delta is computed from a complete
  window. This is a more conservative choice than "last completed
  record only" and adds at most a small additional exclusion count.
- **Empirical scope.** Phase 4i evidence shows BTC: 5 699 missing
  5-minute records / 6 records per 30m window ≈ 950 affected 30m
  bars (worst-case; some sharing a window). At ~74 448 30m bars
  total, that is ~1.3 % maximum bar exclusion. The actual figure
  will be lower if multiple missing records cluster in the same
  30m window. The future V2 backtest phase will report the exact
  figure.
- **Exclusion logging label.** Future V2 backtest reports MUST
  log per-bar exclusions with the label `metrics_oi_missing_or_invalid`
  (matching the Phase 4j §11.6 column name).
- **Missing metrics windows treated as invalid windows, not gaps to
  patch.** This is the same disposition Phase 3r §8 used for
  mark-price gaps.

---

## 16. Per-bar exclusion rule

Per Phase 4j §11.4 verbatim.

The per-bar exclusion algorithm (predeclared here for any future V2
backtest brief to implement exactly):

```python
# Pseudocode (NOT implemented by Phase 4j; predeclared for
# future V2 backtest phase to implement exactly).
def is_30m_bar_oi_feature_eligible(
    symbol: str,                  # "BTCUSDT" or "ETHUSDT"
    bar_open_time_ms: int,        # 30m bar's open_time in UTC ms
    metrics_records: dict[int, MetricsRecord],
        # keyed by create_time UTC ms for the symbol
) -> bool:
    bar_close_time_ms = bar_open_time_ms + 30 * 60 * 1000 - 1
    expected_records_ms = [
        bar_open_time_ms + 0,
        bar_open_time_ms + 5 * 60 * 1000,
        bar_open_time_ms + 10 * 60 * 1000,
        bar_open_time_ms + 15 * 60 * 1000,
        bar_open_time_ms + 20 * 60 * 1000,
        bar_open_time_ms + 25 * 60 * 1000,
    ]
    for ts_ms in expected_records_ms:
        if ts_ms not in metrics_records:
            return False
        rec = metrics_records[ts_ms]
        if rec.symbol != symbol:
            return False
        if rec.sum_open_interest != rec.sum_open_interest:  # NaN check
            return False
        if rec.sum_open_interest_value != rec.sum_open_interest_value:
            return False
    return True
```

- The function is pure — no side effects, no patching, no
  side-channel data access.
- `metrics_records` is the per-symbol indexed dictionary built by
  reading the Phase 4i normalized Parquet partitions. The future
  V2 backtest phase loads it from the existing local data; no
  re-acquisition is required.
- Returning `False` excludes the 30m bar from V2 candidate setup
  generation entirely.
- The result must be logged per §11.6 / §11.7.

---

## 17. Timestamp alignment rule

Per Phase 4j §11.4 plus the Phase 4j brief §6 alignment requirement:

- **Metrics `create_time` is UTC milliseconds.** Phase 4i parser
  normalizes to int64 UTC ms (per metrics manifest
  `canonical_timestamp_format`).
- **30m signal bar uses only metrics records with `create_time <=
  signal decision timestamp.`** Signal decision timestamp = 30m
  bar's `close_time` = `open_time + 30 * 60 * 1000 - 1` (per Phase
  4i klines manifest `quality_checks.close_time_consistency_violations
  == 0`).
- **No future metrics records.** Strict point-in-time-valid alignment
  per `docs/04-data/timestamp-policy.md`.
- **No partial 30m metrics windows.** All six aligned 5-minute
  records required (§15 / §16).
- **No look-ahead.** Standard predeclared no-look-ahead rule per
  Phase 4g §31 / `v1-breakout-validation-checklist.md` simulation
  realism gate.

**OI delta computation rule (predeclared).** For each 30m signal
bar at `bar_open_time_ms` that passes the per-bar exclusion test:

- `oi_at_bar_close` = the metrics record with `create_time =
  bar_open_time_ms + 25 * 60 * 1000` (the LAST 5-minute record in
  the 30m window).
- `oi_at_prev_window_close` = the metrics record with `create_time
  = bar_open_time_ms - 5 * 60 * 1000` (the LAST 5-minute record in
  the previous 30m window — i.e., 5 minutes before the current bar
  opens).
- `oi_delta = oi_at_bar_close - oi_at_prev_window_close`.
- For a long V2 entry, `oi_delta_aligned = oi_delta >= 0` (rising
  OI consistent with new long positioning) per Phase 4g §17 sub-component
  (a) policy alternatives.
- For a short V2 entry, mirror.

**Why "last completed 5-minute OI of current 30m window vs. last
completed 5-minute OI of previous 30m window."** This is simpler and
point-in-time clearer than mean-OI-over-window because:

- It uses two specific record values rather than six-record windowed
  averages.
- It avoids partial-window aggregation when six aligned records are
  not all present (per-bar exclusion handles the missing case).
- It matches the V2-evidence framing in Phase 4g §17 (OI delta as a
  bar-completion-time direction signal, not as a windowed-average
  trend signal).

**Restriction.** The rule above is **the** OI delta computation
rule for V2's first backtest. The future V2 backtest brief MUST
implement exactly this rule. Variant rules (mean-OI-over-window,
exponentially-smoothed-OI, etc.) are NOT permitted in the first
backtest. Variants require a separately authorized strategy-spec
amendment.

---

## 18. Invalid-window handling

Phase 4j §11.5 verbatim. Restated:

- Missing metrics records are recorded as INVALID WINDOWS in Phase
  4i manifests' `invalid_windows` lists, NOT as gaps to patch.
- Affected 30m signal bars are EXCLUDED from V2 candidate setup
  generation per §15 / §16.
- Affected dates are reported per §11.6.
- The full set of affected windows is re-derivable by re-reading
  Phase 4i `quality_checks.gap_locations` (capped at first 50 per
  manifest) plus running the integrity-check function against the
  existing local metrics Parquet partitions.
- No invalid window is silently extended. No invalid window is
  silently shrunk. No invalid window is silently merged with an
  adjacent window.

---

## 19. Manifest policy

Phase 4j §11.1 plus the Phase 4j brief §8 manifest-policy
constraints. Restated:

- **Do NOT modify Phase 4i metrics manifests.** Both
  `binance_usdm_btcusdt_metrics__v001.manifest.json` and
  `binance_usdm_ethusdt_metrics__v001.manifest.json` are preserved
  byte-for-byte verbatim. Phase 4j does NOT edit them.
- **Do NOT change `research_eligible: false`.** The global manifest
  status is preserved. The metrics datasets remain GLOBALLY
  ineligible.
- **Do NOT create corrected manifests.** No
  `binance_usdm_btcusdt_metrics_corrected__v001` or similar is
  created.
- **Do NOT create `__v002` metrics manifests.** No version bump.
- **Do NOT create v003.** No new dataset family bump.
- **Record governance in DOCS only.** This Phase 4j memo is the
  authoritative record of the partial-eligibility rule. The future
  V2 backtest phase brief MUST cite Phase 4j §11 by section number
  when implementing the per-bar exclusion logic.
- **Future backtest may reference Phase 4j governance doc to allow
  feature-level OI-subset use while keeping global manifest
  ineligible.** This is exactly the Phase 3r §8 pattern: the
  governance doc binds the feature-level use; the manifest binds
  the global status; the two coexist by design.

---

## 20. Backtest preconditions

A future V2 backtest remains BLOCKED until ALL of the following are
satisfied:

1. **Phase 4j is merged to `main`.** A merge-closeout housekeeping
   commit must record the governance rule in the project state.
2. **`docs/00-meta/current-project-state.md` records the governance
   rule.** Specifically, a Phase 4j paragraph in the Current Phase
   section noting that the Phase 4j §11 rule is the binding
   governance for any future V2 backtest. Phase 4j does NOT update
   this file (per Phase 4j brief "Do not update current-project-state.md
   until merge"); the merge-closeout housekeeping commit is the
   correct moment to update it.
3. **A separate V2 backtest-plan phase is authorized.** That phase
   would be docs-only and would predeclare:
   - The exact backtest implementation plan (loader code, feature
     code, strategy code, validation harness).
   - The per-bar exclusion algorithm implementation matching Phase
     4j §16 verbatim.
   - The exclusion-counts table format matching Phase 4j §11.6.
   - The sensitivity analysis matching Phase 4j §11.7.
   - Predeclared evidence thresholds for variant comparison and
     overall V2 verdict.
   - PBO / deflated Sharpe / CSCV machinery per Phase 4g §29 / §31
     and Phase 4f §28.
   - The chronological holdout and OOS window definitions per Phase
     4g §31.
   - Full M1 / M2 / M3 mechanism-check decomposition implementation
     per Phase 4g §30.
4. **V2 backtest code explicitly implements the Phase 4j per-bar
   exclusion rule.** Implementation deviations from §16 must abort
   the backtest and produce a failure report.
5. **V2 backtest report MUST separately report:**
   - the number of 30m bars excluded by metrics OI gaps (per §11.6
     exclusion-counts table);
   - the number of V2 candidate setups excluded (because their
     containing 30m bar was excluded);
   - the number of V2 trades excluded (subset of candidate setups
     that would have been entered);
   - whether exclusions cluster by date / regime (e.g., are all
     exclusions in 2024-02 or distributed across the 4-year range);
   - the sensitivity analysis comparing main-cell vs. exclude-entire-
     affected-days variant per §11.7;
   - explicit confirmation that NO optional ratio column was used
     (per §11.3 / §14).

**Phase 4j does NOT authorize the V2 backtest-plan phase.** That
phase is conditional secondary in §27 below.

**Phase 4j does NOT authorize the V2 backtest itself.** The
backtest-plan phase, if ever authorized, would in turn require
operator authorization for actual execution.

---

## 21. What this does not authorize

Phase 4j explicitly does NOT authorize, propose, or initiate any of
the following:

- **Immediate V2 backtest.** Forbidden until Phase 4j is merged AND
  a separate V2 backtest-plan phase is authorized AND that plan
  phase is itself merged AND a separate V2 backtest execution
  phase is authorized.
- **V2 implementation.** Forbidden until V2 backtest evidence is in
  AND a separately authorized implementation phase exists.
- **V2 strategy-spec amendment.** The Phase 4j brief explicitly
  forbids "Do not change Phase 4g V2 strategy-spec selections."
  Phase 4j honours this.
- **Optional ratio-column activation.** §11.3 / §14 categorically
  forbid this for V2's first backtest. Activation requires a
  separately authorized strategy-spec amendment phase.
- **OI feature removal from V2.** The Phase 4j brief explicitly
  forbids "Do not remove the OI feature from V2 in Phase 4j."
  Phase 4j honours this.
- **Mark-price 30m / 4h acquisition.** DEFERRED per Phase 4h §20.
- **`aggTrades` acquisition.** OPTIONAL / DEFERRED per Phase 4h §7.E.
- **v003 dataset creation.** No new dataset family bump.
- **v002 / v001-of-5m / Phase 4i manifest modification.** All
  preserved verbatim.
- **Phase 3r §8 mark-price gap governance modification.** Preserved
  verbatim.
- **Phase 3v §8 stop-trigger-domain governance modification.**
  Preserved.
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance modification.** Preserved.
- **Phase 4f / 4g / 4h / 4i text modification.** All preserved
  verbatim.
- **R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A revision.**
  Preserved verbatim.
- **Lock change.** §1.7.3 / §11.6 / mark-price stops preserved.
- **Phase 4 (canonical) authorization.** Per
  `docs/12-roadmap/phase-gates.md`.
- **Phase 4k / any successor phase.** Phase 4j is docs-only;
  successor authorization is a separate operator decision.
- **Live exchange-write capability, production Binance keys,
  authenticated APIs, private endpoints, user stream, WebSocket,
  listenKey lifecycle, production alerting, Telegram / n8n production
  routes, MCP, Graphify, `.mcp.json`, credentials, exchange-write
  capability.** None touched, enabled, or implied.

---

## 22. Forbidden-work confirmation

The following did NOT occur in Phase 4j and would NOT occur under any
implementation operating under Phase 4j alone:

- **No Phase 4 canonical / Phase 4k / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched,
  or commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 validation.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No data acquisition / patching / regeneration / modification.**
- **No data download.**
- **No data manifest modification.**
- **No v002 dataset / manifest modification.**
- **No v001-of-5m dataset / manifest modification.**
- **No Phase 4i manifest modification.** Both metrics manifests
  retain `research_eligible: false`.
- **No v003 created.**
- **No mark-price 30m / 4h acquisition.**
- **No `aggTrades` acquisition.**
- **No spot data acquisition.**
- **No cross-venue data acquisition.**
- **No funding-rate re-acquisition.**
- **No new Phase 4i manifests.**
- **No new corrected manifests.**
- **No silent OI patching.**
- **No forward-fill.**
- **No interpolation.**
- **No imputation.**
- **No silent omission.**
- **No optional ratio-column activation.**
- **No OI feature removal from V2.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 3v `stop_trigger_domain` governance modification.**
- **No Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No Phase 4h text modification.**
- **No Phase 4i text modification.**
- **No Phase 4i acquisition script modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.**
- **No `prometheus.research.data.*` extension.**
- **No `Interval` enum extension.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No credential storage / request / use.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No order placement / cancellation.**
- **No real exchange adapter implementation.**
- **No exchange-write capability.**
- **No reconciliation implementation.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4j branch.** Per the Phase 4j brief.
- **No `.claude/rules/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 23. What remains blocked

After Phase 4j (if merged) the following remain blocked until
separately authorized:

- **Immediate V2 backtest.** Blocked. Requires Phase 4j merged AND
  a separate V2 backtest-plan phase authorized AND merged.
- **V2 implementation.** Blocked. Requires V2 backtest evidence AND
  a separately authorized implementation phase.
- **Paper / shadow / live-readiness / exchange-write.** FORBIDDEN
  per `docs/12-roadmap/phase-gates.md`. None of these gates is met.
- **Optional ratio-column use.** Blocked by §11.3 / §14. Requires a
  separately authorized strategy-spec amendment phase.
- **mark-price 30m / 4h acquisition.** Blocked / DEFERRED per Phase
  4h §20.
- **`aggTrades` acquisition.** Blocked / DEFERRED per Phase 4h §7.E.
- **OI feature removal from V2.** Blocked by Phase 4j brief
  ("Do not remove the OI feature from V2 in Phase 4j").
- **Phase 4 canonical.** Per `docs/12-roadmap/phase-gates.md`.
- **Production-key creation.** Per `docs/10-security/api-key-policy.md`.

---

## 24. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase
  4j deliverables (this memo + closeout) exist as branch-only
  artefacts pending operator review and merge.
- **Phase 4j output:** docs-only governance memo + closeout
  artefact on the Phase 4j branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4j).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase
  4 (canonical) remains not authorized. Phase 4a–4i all merged.
  Phase 4j V2 metrics governance memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4j).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **V2 metrics governance:** Phase 4j §11 (this memo; binding from
  operator approval forward; immutable absent a separately authorized
  amendment).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements).
  Phase 4i acquired 6 dataset families; 4 of 6 research-eligible;
  2 of 6 (metrics) NOT research-eligible. Phase 4j defines the
  binding governance for partial-eligibility OI-subset use of the
  metrics datasets. V2 is **NOT implemented; NOT backtested; NOT
  validated; NOT live-ready; NOT a rescue.**
- **OPEN ambiguity-log items after Phase 4j:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`; Phase 4i metrics manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4j/v2-metrics-data-governance` exists
  locally and (after push) on `origin`. NOT merged to main.

---

## 25. Operator decision menu

Phase 4j presents the following operator decision options:

- **Option A — Adopt Phase 4j §11 as the binding metrics OI-subset
  partial-eligibility rule; merge Phase 4j; remain paused.**
  **PRIMARY RECOMMENDATION.** The operator approves Phase 4j §11 as
  the formally binding governance rule for any future V2 backtest
  use of the metrics datasets. Phase 4j is merged when convenient.
  Strategy execution remains paused. No V2 backtest runs. The
  governance rule becomes immutable from the operator-approval
  point forward.
- **Option B — Adopt Phase 4j §11 + authorize a docs-only V2
  backtest-plan phase (future Phase 4k).** **CONDITIONAL
  SECONDARY.** The operator approves Phase 4j §11 AND authorizes a
  follow-on docs-only memo that operationalizes the per-bar
  exclusion algorithm, predeclares the backtest implementation
  plan, predeclares evidence thresholds, and predeclares variant
  comparison rules. The plan phase would itself be docs-only and
  would NOT execute the backtest. This option is acceptable only
  if the operator explicitly wants to advance toward a V2 backtest;
  if the operator is unsure, Option A is the safer choice.
- **Option C — Reject Phase 4j §11 and keep V2 backtesting blocked
  indefinitely.** Procedurally safe but stalls V2 even though the
  V2-required `sum_open_interest` columns are fully populated.
  Equivalent to Phase 4i Option A. **NOT RECOMMENDED** because
  Phase 4j was authored specifically to address Phase 4i's
  partial-pass; rejecting Phase 4j leaves the project in the same
  state as the post-Phase-4i boundary.
- **Option D — Reject Phase 4j §11 and remove the OI feature from
  V2.** Modifies Phase 4g §28 active feature set; the Phase 4j
  brief explicitly forbids Phase 4j from doing this. Would require
  a separately authorized Phase 4g amendment. **NOT RECOMMENDED.**
- **Option E — Authorize a metrics data-patching governance memo
  permitting forward-fill / interpolation.** **REJECTED.** Forbidden
  by Phase 3r §8 / Phase 3p §4.7 / Phase 4h §17–§19 / Phase 4i §17.
  Data fabrication is not an option.
- **Option F — Immediate V2 backtest.** **REJECTED.** Phase 4i and
  Phase 4j both block this until a separately authorized backtest-plan
  phase is in place.
- **Option G — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of these
  gates is met.

**Phase 4j recommendation: Option A (adopt §11; remain paused)
PRIMARY; Option B (adopt §11 + authorize docs-only V2 backtest-plan
phase) CONDITIONAL SECONDARY.** Options C / D are not recommended.
Options E / F / G are rejected / forbidden.

---

## 26. Next authorization status

**No next phase has been authorized.** Phase 4j's primary
recommendation is **Option A** (adopt Phase 4j §11 as the binding
governance rule; remain paused), with **Option B** (adopt §11 +
authorize a docs-only V2 backtest-plan phase as future Phase 4k) as
**conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued by Phase 4j.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b script-scope quality-gate restoration
is complete (per Phase 4b). The Phase 4c state-package
quality-gate residual cleanup is complete (per Phase 4c). The
Phase 4d post-4a/4b/4c review is complete (per Phase 4d). The
Phase 4e reconciliation-model design memo is complete (per Phase
4e). The Phase 4f V2 hypothesis predeclaration is complete (per
Phase 4f). The Phase 4g V2 strategy spec is complete (per Phase
4g). The Phase 4h V2 data-requirements / feasibility memo is
complete (per Phase 4h). The Phase 4i V2 public data acquisition
+ integrity validation is complete with partial-pass verdict (per
Phase 4i). The Phase 4j V2 metrics data governance memo is
complete on this branch (this phase) and adopts the §11 metrics
OI-subset partial-eligibility rule as the recommended binding
governance for any future V2 backtest. **Recommended state remains
paused.**
