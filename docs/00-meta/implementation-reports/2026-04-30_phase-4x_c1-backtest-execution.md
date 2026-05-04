# Phase 4x — C1 Backtest Execution

**Authority:** Operator authorization for Phase 4x (Phase 4w §"Operator decision menu" Option A primary recommendation: Phase 4x — C1 Backtest Execution, docs-and-code, standalone research script). Phase 4w (C1 backtest-plan memo); Phase 4v (C1 strategy spec memo); Phase 4u (C1 hypothesis-spec memo); Phase 4t (post-G1 fresh-hypothesis discovery); Phase 4s (post-G1 strategy research consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks).

**Phase:** 4x — **C1 Backtest Execution** (docs-and-code; standalone research script). Implements `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology and runs the predeclared C1 — Volatility-Contraction Expansion Breakout backtest on BTCUSDT primary / ETHUSDT comparison across LOW / MEDIUM / HIGH cost cells over the train (2022-01-01..2023-06-30 UTC) / validation (2023-07-01..2024-06-30 UTC) / OOS holdout (2024-07-01..2026-03-31 UTC) windows; evaluates 32 variants (= 2^5) over five binary axes; computes M1 / M2 / M3 / M4 / M5 with bootstrap (B = 10 000; pinned RNG seed 202604300); computes deflated Sharpe with N = 32, PBO (train→validation rank-based; train→OOS rank-based; CSCV S = 16 with C(16, 8) = 12 870 combinations); evaluates 12 catastrophic-floor predicates (CFP-1..CFP-12); declares Verdict A / B / C / D. **Phase 4x is docs-and-code in standalone-script mode.** No source code, tests, existing scripts, data, or manifests were modified. **Phase 4x does NOT authorize Phase 4y.**

**Branch:** `phase-4x/c1-backtest-execution`. **Memo date:** 2026-05-04 UTC.

---

## Summary

**Final Verdict: C — C1 framework HARD REJECT.**

**Binding catastrophic-floor drivers:** CFP-2 (negative BTC OOS HIGH expectancy: train-best variant mean_R = -0.3633), CFP-3 (catastrophic profit-factor 0.4413 < 0.50 AND max_drawdown_R = 54.55 > 10R), CFP-6 (deflated Sharpe = -20.8173 ≤ 0).

**CFPs that did NOT trigger:** CFP-1 (train-best produced 149 OOS HIGH trades; 0/32 variants below 30); CFP-4 (BTC fail AND ETH fail; ETH cannot rescue BTC, but ETH also failed M3-comparator so no false-positive rescue path); CFP-5 (train HIGH mean_R = -0.4778 already negative, so OOS-only failure is not the pattern); CFP-7 (max-month fraction 7.4%); CFP-8 (worst sensitivity degradation 0.155R < 0.20R threshold); **CFP-9 NOT triggered (transition_rate_per_480 = 3.33; train-best 149 trades; 100% of variants produce ≥ 30 trades)**; CFP-10/11/12 (forbidden-input access counters all 0 by construction).

**Categorical observation: C1's failure mode is structurally distinct from both V2 and G1.** V2 (Phase 4l) failed at design-stage incompatibility producing 0 trades from a stop-distance filter. G1 (Phase 4r) failed at regime-gate-meets-setup intersection sparseness producing 0 active-regime trades. **C1 (this phase) fires plenty of trades — 149 BTC OOS HIGH trades for the train-best variant; 213 OOS candidate transitions; transition rate 3.33 per 480 30m bars — but the strategy is loss-making after costs.** This is a *third distinct* failure mode: trade machinery works correctly, opportunity rate is healthy, no overfitting (PBO low across all three horizons), no concentration, no sensitivity fragility — but the C1 thesis is empirically wrong on BTC OOS HIGH. The compression-box-with-buffer breakout is consistently loss-making across all 32 variants, all three windows, and all three cost cells.

**Forensic observation (NOT a parameter-selection input; recorded for the project record):** The contraction precondition makes performance *worse*, not better. C1 transition trades produce mean_R = -0.3633 vs. non-contraction baseline mean_R = -0.1192 (a -0.2440R differential, with bootstrap 95% CI [-0.4101, -0.0810] strictly negative). C1 also underperforms always-active-same-geometry baseline (-0.2201R differential, CI [-0.3859, -0.0556]) and delayed-breakout baseline (-0.2930R differential). This pattern means C1 is **anti-validated**: contraction-state-tied transitions are systematically worse than the same close-beyond-compression-box-with-buffer rule fired without the contraction precondition. The hypothesis that "compression releases improve directional breakout outcomes" is empirically rejected on BTC OOS HIGH under the Phase 4v locked spec.

**C1 first-spec is terminally HARD REJECTED as retained research evidence only.** **No C1 rescue is authorized:** no C1-prime / C1-narrow / C1-extension / C1 hybrid; no C1 with relaxed C_width / B_width / S_buffer / T_mult / N_comp / W_width / L_delay / close-location thresholds; no Phase 4v amendment based on Phase 4x forensic numbers; no Phase 4w methodology amendment; no immediate C1 rerun. Phase 4w stop conditions hold: forbidden-input access counters all 0; no lookahead; no transition-dependency violation; no manifest modification; no data acquisition; no `src/prometheus/` modification; no test modification; no existing-script modification; no Phase 4r / 4l / 4i / 3q / 3s acquisition / diagnostics / backtest script execution.

## Authority and boundary

- **Authority granted:** create `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology (standalone research script; no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no network I/O; no credentials; no `.env`; no Binance API; pure pyarrow + numpy + stdlib + matplotlib optional); read existing local Parquet under `data/normalized/klines/`; read existing manifests under `data/manifests/`; write local gitignored research outputs under `data/research/phase4x/`; create the Phase 4x execution report; create the Phase 4x closeout.
- **Authority NOT granted:** modify `src/prometheus/`, tests, or existing scripts (forbidden); modify `data/raw/`, `data/normalized/`, or `data/manifests/` (forbidden); create new manifests or v003 (forbidden); acquire / download data (forbidden); use network I/O (forbidden); use credentials (forbidden); contact Binance APIs or `data.binance.vision` (forbidden); create paper / shadow / live runtime (forbidden); imply live-readiness (forbidden); start Phase 4y or any successor phase (forbidden); revise any retained verdict or project lock (forbidden); amend Phase 4v / 4w / 4j §11 / 4k methodology (forbidden); create C1-prime / C1-narrow / C1-extension / C1 hybrid (forbidden); use V2 Phase 4l forensic stop-distance numbers as design inputs (forbidden); use G1 Phase 4r active-fraction / always-active / inactive-pseudo-trade results as thresholds or tuning targets (forbidden).

## Starting state

```text
Branch (Phase 4x):    phase-4x/c1-backtest-execution
main / origin/main:   5105a74a28778b22b30e9dc2b9da788615672eb7 (unchanged)
Phase 4w merge:       16336b7abecbb43b3a522c56035ae0d88a8f7763 (merged)
Phase 4w housekeep:   5105a74a28778b22b30e9dc2b9da788615672eb7 (merged)
Working-tree state:   clean (no tracked modifications); only gitignored
                      transients .claude/scheduled_tasks.lock and
                      data/research/ are untracked and will not be
                      committed.
Quality gates (verified at run start):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Relationship to Phase 4w

- Phase 4w predeclared the entire future Phase 4x methodology (data-loading; feature computation; signal generation; entry / exit simulation; cost / funding model; sizing / exposure; 32-variant grid handling; PBO / DSR / CSCV; M1 / M2 / M3 / M4 / M5; CFP-1..CFP-12; Verdict taxonomy; reporting tables; required plots; stop conditions; reproducibility).
- Phase 4w did NOT authorize Phase 4x.
- The operator explicitly authorized Phase 4x.
- Phase 4x implements `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology.
- All 32 binding tables predeclared by Phase 4w were produced (see `Required tables produced` below).
- Plots were skipped because matplotlib was unavailable in the project virtual environment; per Phase 4w, plot absence does NOT cause Verdict D when all 32 binding tables are complete and absence is documented.

## Methodology adherence statement

Phase 4x implements the Phase 4w methodology verbatim:

- **Variant cardinality:** 32 (= 2^5) over the five Phase 4v binary axes (`B_width`, `C_width`, `N_comp`, `S_buffer`, `T_mult`); deterministic lexicographic ordering; no extension; no reduction; no early exit; all 32 variants reported.
- **Fixed parameters:** `W_width = 240`; `L_delay = 1`; close-location 0.70 long / 0.30 short; `T_stop_bars = 2 × N_comp`; no HTF gate; no funding input; no volume gate; no metrics OI; no ATR-percentile stop-distance gate; `break_even_rule = disabled`; `ema_slope_method = not_applicable`; `stagnation_window_role = not_active`; `stop_trigger_domain = trade_price_backtest`; `risk_fraction = 0.0025`; `max_leverage = 2.0`; `max_positions = 1`; `sizing_equity = 100 000 USDT`.
- **Cost cells:** LOW = 1 bp / MEDIUM = 4 bps / HIGH = 8 bps slippage per side; taker fee = 4 bps per side; no maker rebates; no live-fee assumptions; funding excluded; **§11.6 = 8 bps HIGH preserved verbatim**.
- **Validation windows reused verbatim from Phase 4k:** train 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC; validation 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC; OOS 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC.
- **Train-best selection:** BTC train MEDIUM cost cell; deflated-Sharpe-aware criterion; raw-Sharpe tie-break; lowest variant_id tie-break; same identifier carried into validation, OOS, and ETH comparison.
- **Bootstrap:** B = 10 000; pinned RNG seed 202604300.
- **CSCV:** S = 16 chronological OOS sub-samples; C(16, 8) = 12 870 combinations; tractable and computed exactly with no silent approximation.
- **PBO:** train→validation rank-based; train→OOS rank-based; CSCV PBO; CFP-6 binding > 0.50.
- **Negative tests:** non-contraction breakout baseline (M1, binding); always-active-same-geometry baseline (M2.a, binding); delayed-breakout baseline (M2.b, binding); active opportunity-rate diagnostic (M3 + CFP-9, binding); random-contraction baseline skipped (per Phase 4w optional default).
- **CFPs:** all 12 evaluated with Phase 4w-specified thresholds.

## Script implementation summary

Path: `scripts/phase4x_c1_backtest.py`. Single-file standalone research script (~2300 lines including docstrings, dataclasses, helpers, 32 table writers, and main orchestration). Imports: `argparse`, `hashlib`, `itertools`, `json`, `math`, `sys`, `collections.Counter`, `collections.abc.Sequence`, `dataclasses`, `datetime`, `pathlib.Path`, `typing.Any`, `numpy`, `pyarrow.parquet`. **No** `prometheus.runtime`, `prometheus.execution`, `prometheus.persistence` imports. **No** exchange adapter imports. **No** `requests` / `httpx` / `aiohttp` / `urllib3` / `urllib.request` / `websockets` / `websocket` imports. **No** `.env` access. **No** credential access. **No** Binance API calls. **No** network I/O.

Static forbidden-import scan (run prior to commit): all 10 forbidden import names produced 0 occurrences. Static forbidden-data-name scan (run prior to commit): occurrences of `metrics`, `mark_price`, `aggTrades`, `spot`, `cross-venue` are confined to (a) the module docstring describing what is NOT done, (b) the comment in `_run` describing the data-loading boundary, (c) the required CFP-12 audit-counter field names (`metrics_oi_access_count`, `mark_price_access_count`, `aggtrades_access_count`, `spot_access_count`, `cross_venue_access_count`) per Phase 4w spec, and (d) the docstring and row labels of `_write_forbidden_work_confirmation` per Phase 4w spec. Runtime access counts for all of these are 0 by construction (the script's only data path is the explicit-column 30m kline loader).

## Data inputs and manifest SHA pinning

```text
Required (research-eligible per Phase 4i; loaded as primary signal timeframe):
  binance_usdm_btcusdt_30m__v001
    sha256: 3cdf6fb91ffca8acc2a69ae05a00745a031360c01c585a75f876c64d42230da8
    research_eligible: True
    bar_count: 74 448 30m bars
  binance_usdm_ethusdt_30m__v001
    sha256: 0a7502c5e09916529e50951bd503e1a2ac95d372e99ba65f4cb3bfb1477e3afd
    research_eligible: True
    bar_count: 74 448 30m bars

Not loaded (excluded from C1 first-spec; allowed reporting context only;
unused by Phase 4x):
  binance_usdm_btcusdt_4h__v001 / binance_usdm_ethusdt_4h__v001
  binance_usdm_btcusdt_15m__v002 / binance_usdm_ethusdt_15m__v002
  binance_usdm_btcusdt_1h_derived__v002 / binance_usdm_ethusdt_1h_derived__v002

Forbidden (not loaded; CFP-10 / CFP-12 audit counters all 0):
  funding (any version); metrics (any version);
  mark-price (any timeframe); aggTrades; spot; cross-venue; order book.
```

Manifests are loaded once at run start. SHA256 hashes are computed by the script and pinned in `run_metadata.json` and `manifest_references.csv`. `research_eligible` is verified for both 30m manifests (both True). No manifest is modified. No new manifest is created. No data is acquired.

## Forbidden input verification

Per `forbidden_work_confirmation.csv` (audit counters all 0 by construction):

```text
metrics_oi_access_count                : 0
optional_ratio_column_access_count     : 0
mark_price_access_count                : 0
aggtrades_access_count                 : 0
spot_access_count                      : 0
cross_venue_access_count               : 0
network_io_attempts                    : 0
credential_reads                       : 0
env_file_reads                         : 0
data_raw_writes                        : 0
data_normalized_writes                 : 0
data_manifest_modifications            : 0
v003_creations                         : 0
src_prometheus_modifications           : 0
test_modifications                     : 0
existing_script_modifications          : 0
```

The script's only data path is `load_kline_symbol_interval` with the explicit column list `[open_time, close_time, open, high, low, close, volume]`. No metrics loader exists. No funding loader is invoked. No mark-price loader is referenced. No aggTrades / spot / cross-venue / order-book code path exists. No `requests` / `httpx` / `aiohttp` / `urllib3` / `urllib.request` / `websockets` / `websocket` import exists. No `.env` is read. No credentials are accessed. No write to `data/raw/`, `data/normalized/`, or `data/manifests/` occurs. No new manifest is created. No v003 is created.

## Future-script-boundary compliance

The script complies with all Phase 4w future-script-boundary rules:

- standalone research script only;
- no `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` imports;
- no exchange adapter imports;
- pure pyarrow + numpy + stdlib (matplotlib optional plot-only);
- no `.env`;
- no credentials;
- no Binance API;
- no network I/O;
- writes only to gitignored `data/research/phase4x/`;
- emits final Verdict A / B / C / D in `data/research/phase4x/tables/verdict_declaration.csv`.

## Backtest command

Exact command run:

```text
.venv/Scripts/python scripts/phase4x_c1_backtest.py \
  --start 2022-01-01 \
  --end 2026-03-31 \
  --train-start 2022-01-01 \
  --train-end 2023-06-30 \
  --validation-start 2023-07-01 \
  --validation-end 2024-06-30 \
  --oos-start 2024-07-01 \
  --oos-end 2026-03-31 \
  --symbols BTCUSDT ETHUSDT \
  --primary-symbol BTCUSDT \
  --comparison-symbol ETHUSDT \
  --output-dir data/research/phase4x \
  --rng-seed 202604300
```

Command shape matches the Phase 4w predeclared shape verbatim. No flags activate forbidden inputs.

## Output directory

```text
data/research/phase4x/
  run_metadata.json
  tables/                       (32 binding CSV tables)
  plots/                        (empty; matplotlib unavailable in venv)
```

`data/research/phase4x/` is gitignored and is NOT committed. Reproducible from the script with the pinned RNG seed 202604300.

## Data-loading verification

`scripts/phase4x_c1_backtest.py::load_kline_symbol_interval` was invoked twice (BTCUSDT 30m, ETHUSDT 30m). Each call:

- read every `part-*.parquet` under `data/normalized/klines/symbol={SYMBOL}/interval=30m/`;
- requested only the explicit column list `[open_time, close_time, open, high, low, close, volume]`;
- stable-sorted by `open_time`;
- verified uniqueness of `(symbol, interval, open_time)` (no duplicates detected);
- yielded 74 448 30m bars per symbol over 2022-01-01..2026-03-31 UTC.

No partial-bar consumption (all `close_time <= decision_time` for any decision). No timestamp gap was treated as a usable bar. No funding / metrics / mark-price / aggTrades / spot / cross-venue / order-book loader was invoked.

## Feature-computation verification

Per-symbol features (variant-agnostic) computed once per symbol:

- ATR(20) Wilder smoothing for the diagnostic `stop_distance_atr` reporting (NOT an entry gate; not used in candidate rejection);
- close-location ratios `close_location_long = (close - low) / (high - low)` and `close_location_short = (high - close) / (high - low)` with epsilon = 1e-12 guard for degenerate bars (high == low).

Per-(symbol, variant) features computed once per (symbol, variant_id) pair (32 variants × 2 symbols = 64 feature tables):

- `compression_box_high[t] = max(high[t-N_comp..t-1])` (prior-completed only; current bar excluded);
- `compression_box_low[t] = min(low[t-N_comp..t-1])` (same);
- `compression_box_width[t] = compression_box_high - compression_box_low`;
- `rolling_median_width[t] = median(compression_box_width[t-W_width..t-1])` with `W_width = 240` prior-completed bars (current bar excluded);
- `contraction_state[t] = (compression_box_width[t] <= C_width × rolling_median_width[t])` with epsilon-guarded validity;
- `contraction_recently_active[t] = any(contraction_state[k] for k in [t - L_delay, t])` with `L_delay = 1` (i.e., true if bar t-1 OR bar t is in contraction state);
- `LONG_TRANSITION[t] = contraction_recently_active AND close > cbh + B_width × cbw AND close_location_long >= 0.70`;
- `SHORT_TRANSITION[t] = contraction_recently_active AND close < cbl - B_width × cbw AND close_location_short >= 0.70` (equivalent to `close_location_long <= 0.30`);
- `structural_stop_long = compression_box_low - S_buffer × compression_box_width` (compression-box invalidation);
- `structural_stop_short = compression_box_high + S_buffer × compression_box_width`;
- non-contraction baseline (M1): same close-beyond-buffer rule on bars where `contraction_recently_active` is false;
- always-active-same-geometry baseline (M2.a): same close-beyond-buffer rule with no contraction precondition;
- delayed-breakout baseline (M2.b): contraction active in `[t - L_delay - 5, t - L_delay - 1]` AND inactive in `[t - L_delay, t]` AND breakout-with-buffer.

All features use prior-completed bars only by construction. The `rolling_*_excluding_current` helpers exclude the current bar from the lookback window, which prevents lookahead at the feature layer.

## Transition / signal-generation verification

Signal generation pseudocode is implemented verbatim per Phase 4w. Defensive degeneracy check for `LONG_TRANSITION AND SHORT_TRANSITION` simultaneously true on the same bar is implemented; under normal high/low/close constraints both cannot logically coexist (close cannot exceed `cbh + B_width × cbw` AND fall below `cbl - B_width × cbw` simultaneously when `cbh >= cbl`). Empirically zero cases observed (`degenerate_double_transition: false` in CFP-11). No partial-bar consumption (decision time = signal bar's `close_time`; entry uses next-bar `open` at index t+1). No future-bar lookahead (CFP-11 audit fields all clean).

## Entry / exit simulation verification

Entry timing: market entry at the OPEN of the next 30m bar after the confirmed signal close (decision_time = close_time[t]; entry_bar = t+1; entry_price = open[entry_bar]). No intrabar entries. No partial fills. One position max. No pyramiding. No reversal while positioned.

Exit precedence: stop > target > time-stop. Same-bar stop+target ambiguity resolves to stop (conservative; matches Phase 4w spec verbatim). Time-stop fires at `T_stop_bars = 2 × N_comp` 30m bars; exit at next 30m bar's open, or at `close[t']` if `t'+1` is unavailable (end-of-data edge).

Stop-distance ATR diagnostic: `stop_distance_atr = |entry - stop| / ATR_20[signal_bar]` recorded per trade in `stop_distance_atr_diagnostics.csv`; **NOT** used to reject candidates in C1 first-spec; **NOT** used in variant selection or verdict declaration.

## Cost model verification

Per Phase 4w / §11.6 / Phase 4v:

- LOW = 1 bp slippage per side; MEDIUM = 4 bps slippage per side; HIGH = 8 bps slippage per side;
- taker fee = 4 bps per side;
- no maker rebates; no live-fee assumptions;
- funding excluded (no funding loader invoked);
- per-side cost factor applied to entry and exit independently (long entry slipped up by `cost`; long exit slipped down by `cost`; short entry slipped down by `cost`; short exit slipped up by `cost`);
- realized R computed from executed entry / exit prices using the original (pre-cost) stop-distance R denominator.

§11.6 = 8 bps HIGH preserved verbatim. R2 cost-fragility precedent honored: any variant with BTC OOS HIGH `mean_R ≤ 0` triggers CFP-2.

## Position-sizing / exposure verification

Per Phase 4w / §1.7.3:

- `sizing_equity = 100 000` USDT (constant-equity research assumption; no compounding; R-relative results);
- `risk_fraction = 0.0025` (0.25% per trade);
- `max_leverage = 2.0` (2× cap);
- `max_positions = 1`;
- `position_size_units = sizing_equity × risk_fraction / abs(R_per_unit)`;
- if `position_notional > max_leverage × sizing_equity` then size capped to `max_leverage × sizing_equity / entry_price`;
- BTCUSDT primary; ETHUSDT comparison only;
- ETH cannot rescue BTC.

Leverage cap applied where required (capped trades logged per the simulation output; not separately tabulated).

## Threshold-grid summary

```text
Variant cardinality                : 32 (= 2^5)
Variant ordering                   : deterministic lexicographic
                                     (alphabetical axis names)
Axis order (alphabetical)          :
  Axis A: B_width    in {0.05, 0.10}
  Axis B: C_width    in {0.45, 0.60}
  Axis C: N_comp     in {8, 12}
  Axis D: S_buffer   in {0.10, 0.20}
  Axis E: T_mult     in {1.5, 2.0}
variant_id encoding                : variant_id = bit_T_mult * 16
                                     + bit_S_buffer * 8 + bit_N_comp * 4
                                     + bit_C_width * 2 + bit_B_width * 1
Fixed (cardinality 1; not axes):
  W_width                          = 240 30m bars
  L_delay                          = 1
  close-location                   = 0.70 long / 0.30 short
  T_stop_bars                      = 2 × N_comp
  HTF gate                         = NONE
  funding input                    = NONE
  volume input                     = NONE
  metrics OI                       = NONE
  ATR-percentile stop-distance gate= NONE
```

Train-best variant_id = **21** (`B_width = 0.10`, `C_width = 0.45`, `N_comp = 12`, `S_buffer = 0.10`, `T_mult = 2.0`, `T_stop_bars = 24`); selected on BTC train MEDIUM cost cell by deflated-Sharpe-aware criterion; deflated_sharpe = -20.8173; raw_sharpe (train MEDIUM) = -0.3635. Same variant_id carried into validation, OOS, and ETH comparison.

## Search-space-control summary

```text
Grid size N                        : 32
Bootstrap iterations (M1, M2)      : 10 000 (pinned)
RNG seed                           : 202604300 (pinned)
DSR (Bailey & López de Prado)      : computed per-variant on BTC train MEDIUM
                                     trade-R series with skew/kurtosis
                                     correction
PBO_train_validation (rank-based)  : 0.375  (below 0.50 threshold; OK)
PBO_train_oos (rank-based)         : 0.219  (below 0.50 threshold; OK)
PBO_cscv                           : 0.094  (below 0.50 threshold; OK)
CSCV S                             : 16 chronological OOS sub-samples
CSCV combinations                  : C(16, 8) = 12 870 (all evaluated;
                                     no silent approximation)
```

PBO does not trigger CFP-6. **DSR for the train-best variant is -20.8173 ≤ 0; this triggers CFP-6 from the DSR side.** The combination of low PBO and very negative DSR indicates that the strategy is NOT failing because of overfitting to the grid — it is failing because the strategy itself is loss-making across nearly all variants (so no overfitting to a "lucky" subset is possible).

## Train / validation / OOS windows

Reused verbatim from Phase 4k:

```text
Train          : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC
                 (~18 months; 26 207 30m bars per symbol)
Validation     : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC
                 (~12 months; 17 568 30m bars per symbol)
OOS holdout    : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC
                 (~21 months; 30 672 30m bars per symbol)
                 Primary C1 evidence cell: BTC OOS HIGH.
```

No window modification post-hoc. No data shuffling. No leakage. Same 32 variants evaluated independently per symbol; no cross-symbol optimization. ETH cannot rescue BTC.

## BTCUSDT primary results

Train-best variant 21 (`B=0.10|C=0.45|N=12|S=0.10|T=2.0`):

```text
Window         | Cell    | n   | win_rate | mean_R   | total_R   | max_dd_R | PF     | sharpe
---------------+---------+-----+----------+----------+-----------+----------+--------+--------
train          | LOW     |  93 |   33.3 % | -0.3095  |  -28.7789 |   30.51  | 0.5417 | -0.2941
train          | MEDIUM  |  93 |   32.3 % | -0.3816  |  -35.4875 |   37.05  | 0.4715 | -0.3635
train          | HIGH    |  93 |   32.3 % | -0.4778  |  -44.4322 |   45.78  | 0.3912 | -0.4554
validation     | LOW     |  90 |   34.4 % | -0.3688  |  -33.1932 |   33.88  | 0.4636 | -0.3616
validation     | MEDIUM  |  90 |   33.3 % | -0.4733  |  -42.5950 |   42.83  | 0.3815 | -0.4530
validation     | HIGH    |  90 |   30.0 % | -0.6126  |  -55.1306 |   55.23  | 0.2976 | -0.5654
oos            | LOW     | 149 |   41.6 % | -0.1701  |  -25.3422 |   28.46  | 0.6804 | -0.1751
oos            | MEDIUM  | 149 |   38.3 % | -0.2529  |  -37.6780 |   39.05  | 0.5655 | -0.2600
oos            | HIGH    | 149 |   37.6 % | -0.3633  |  -54.1258 |   54.55  | 0.4413 | -0.3721
```

**Primary verdict cell (BTC OOS HIGH):** 149 trades; win_rate 37.6%; mean_R = **-0.3633**; total_R = -54.1258; max_drawdown_R = 54.55; profit_factor = 0.4413; sharpe = -0.3721. Strategy is loss-making across all windows and all cost cells.

All 32 BTC OOS HIGH variants are loss-making (range: mean_R ≈ -0.10 to -0.44; trade_count 149 to 515). This confirms C1 is broadly invalidated, not narrowly at the train-best variant.

## ETHUSDT comparison results

Same train-best variant_id = 21 carried into ETH:

```text
Window         | Cell    | n   | mean_R   | total_R   | sharpe
---------------+---------+-----+----------+-----------+---------
oos            | HIGH    | 109 | -0.2140  |  -23.3302 | -0.2148
```

All 32 ETH OOS HIGH variants are also loss-making (range: mean_R ≈ -0.10 to -0.24). ETH performs slightly less badly than BTC but is still negative; **ETH cannot rescue BTC** (CFP-4 rule honored). M4 differential `arr_eth_c1.mean - arr_eth_nc.mean = -0.1589` is negative; directional consistency check holds (BTC differential -0.2440 is also negative; both signs are aligned), so M4 is FAIL on the non-negative-differential leg.

## Cost sensitivity results

Train-best variant 21 BTC OOS:

```text
Cost cell      | mean_R   | profit_factor | sharpe
---------------+----------+---------------+---------
LOW   (1bp)    | -0.1701  | 0.6804        | -0.1751
MEDIUM (4bps)  | -0.2529  | 0.5655        | -0.2600
HIGH  (8bps)   | -0.3633  | 0.4413        | -0.3721
```

Even at LOW cost (well below the realistic taker-fee floor), the strategy is loss-making. Cost is NOT the binding driver of the failure; the strategy is structurally loss-making before costs are amplified.

## M1 contraction-state validity results

```text
Sample sizes (BTC OOS HIGH):
  C1 transitions:           n_c1 = 149  mean_R = -0.3633
  Non-contraction baseline: n_nc = 793  mean_R = -0.1192
  Differential (C1 - nc):                    diff = -0.2440
  Bootstrap 95% CI (B=10000, seed 202604300):
                                  CI = [-0.4101, -0.0810]
Threshold:                       diff >= +0.10R AND CI lower > 0
M1: FAIL  (diff is strongly negative AND CI strictly negative)
```

The contraction precondition is *anti-validated*: the same close-beyond-buffer rule fired without the contraction precondition (i.e., on bars where contraction_recently_active is false) outperforms the contraction-tied rule by 0.244R per trade with a strictly-negative bootstrap CI. This is empirically strong evidence against the C1 thesis.

## M2 expansion-transition value-add results

```text
M2.a — C1 vs always-active-same-geometry:
  Sample sizes (BTC OOS HIGH):
    C1:           n_c1 = 149  mean_R = -0.3633
    always-active: n_aa = 908  mean_R = -0.1431
    Differential:                    diff = -0.2201
    Bootstrap 95% CI:                CI = [-0.3859, -0.0556]
  Threshold:    diff >= +0.05R AND CI lower > 0
  M2.a: FAIL  (diff strongly negative; CI strictly negative)

M2.b — C1 vs delayed-breakout:
  Sample sizes (BTC OOS HIGH):
    C1:       n_c1 = 149  mean_R = -0.3633
    delayed:  n_dl =  57  mean_R = -0.0702
    Differential:                    diff = -0.2930
  Threshold:    diff >= 0R
  M2.b: FAIL

M2 (combined): FAIL  (M2.a AND M2.b both FAIL)
```

Both M2 sub-criteria fail. C1 transitions perform 0.220R worse than the same setup without the contraction precondition (M2.a) and 0.293R worse than the delayed-breakout baseline (M2.b). The transition-timing claim is also empirically rejected.

## M3 inside-spec co-design validity results

```text
BTC OOS HIGH train-best variant:
  mean_R                                  : -0.3633   (THRESHOLD: > 0)        FAIL
  trade_count                             :    149    (threshold: >= 30)      OK
  CFP-1 trigger                           :  False                            OK
  CFP-2 trigger                           :  TRUE                             FAIL
  CFP-3 trigger                           :  TRUE                             FAIL
  Opportunity-rate floors:
    candidate_transition_rate_per_480bars :   3.33   (threshold: >= 1)        OK
    train-best OOS HIGH trade_count       :    149   (threshold: >= 30)       OK
    variants_pass_fraction (>= 30 trades) :  100.0%  (threshold: >= 50.0%)    OK
M3: FAIL  (mean_R <= 0 AND CFP-2 / CFP-3 trigger)
```

M3 fails primarily due to negative expectancy (CFP-2) and catastrophic profit-factor / drawdown (CFP-3). Opportunity-rate floors are clean — C1 generates plenty of candidates and plenty of executed trades; **the failure is not "no opportunity," it is "the opportunity is loss-making."**

## M4 cross-symbol robustness results

```text
BTC OOS HIGH C1 - non-contraction differential : -0.2440
ETH OOS HIGH C1 - non-contraction differential : -0.1589
Directional consistency                        : YES (both negative)
M4 differential threshold                       : >= 0
M4: FAIL  (ETH differential is negative)
```

ETH does not rescue BTC. Both symbols show the same anti-validation pattern (contraction-tied transitions perform worse than non-contraction baseline). CFP-4 ((not M3_pass) AND M4_pass) does NOT trigger because M4 also fails.

## M5 diagnostic results

Diagnostic only per Phase 4w; skipped in Phase 4x to keep the script's geometry computation single-stop-model. Reported as `M5: DIAGNOSTIC_ONLY` in `m1_m2_m3_m4_m5_summary.csv`. Does NOT affect verdict declaration.

## Negative-test diagnostics

```text
Population (BTC OOS HIGH, train-best variant 21):
                      n      mean_R    PF     sharpe
  C1 transitions     149   -0.3633   0.4413  -0.3721
  non-contraction    793   -0.1192    -      -
  always-active      908   -0.1431    -      -
  delayed-breakout    57   -0.0702    -      -
```

All four populations are negative-mean_R, but C1 is the *worst* of the four. The contraction-tied transitions are not just non-additive; they are *destructive* relative to the same close-beyond-buffer rule fired without the contraction precondition.

## PBO / deflated Sharpe / CSCV results

```text
PBO_train_validation (rank-based)  : 0.375  (below 0.50; CFP-6 OK on this leg)
PBO_train_oos (rank-based)         : 0.219  (below 0.50; CFP-6 OK on this leg)
PBO_cscv (S=16, C(16,8)=12 870)    : 0.094  (below 0.50; CFP-6 OK on this leg)
DSR (train-best, N=32)             : -20.8173  (<= 0; CFP-6 TRIGGERED on DSR)
```

PBO does not detect overfitting because the strategy is loss-making across nearly all variants (no "lucky" overfit to detect). DSR is very negative because the train-best raw Sharpe is also negative (-0.363) — the deflation from N=32 makes the negative DSR much larger in magnitude. **CFP-6 triggers via the DSR ≤ 0 condition.**

## Opportunity-rate results

```text
BTC OOS window (2024-07-01..2026-03-31 UTC):
  total_30m_bars                       : 30 672
  oos_total_transitions (long+short)   : 213
  transition_rate_per_480_bars         : 3.33
  train-best OOS HIGH executed trades  : 149
  variants with >= 30 trades (BTC OOS HIGH) : 32 / 32 (100.0%)

CFP-9 (sparse-intersection collapse):  NOT TRIGGERED.
```

C1's opportunity-rate framework is empirically validated as healthy. The strategy fires plenty of candidates; the train-best variant generates well above the M3 trade-count floor; every variant satisfies the floor. **C1 does not fail at the opportunity-rate / sparse-intersection layer (categorically distinct from G1).**

## Trade distribution by month

Train-best variant 21 BTC OOS HIGH trade distribution:

```text
Total trades across 21-month OOS window: 149
Maximum-month concentration            : 11 trades (2025-06)
Maximum-month fraction                 : 7.4%
CFP-7 threshold                        : > 50% triggers
CFP-7: NOT TRIGGERED.
```

Trades are well-distributed across months. The failure is not driven by a single regime or month.

## Catastrophic-floor predicate results

```text
CFP   | Result    | Driver / detail
------+-----------+----------------------------------------------------------------
CFP-1 | OK        | train-best 149 trades; 0/32 variants below 30
CFP-2 | TRIGGER   | BTC OOS HIGH train-best mean_R = -0.3633 <= 0
CFP-3 | TRIGGER   | profit_factor = 0.4413 < 0.50;
                  | max_drawdown_R = 54.55 > 10R
CFP-4 | OK        | M3 BTC FAIL AND M4 ETH FAIL; no rescue scenario
CFP-5 | OK        | train HIGH mean_R = -0.4778 already negative;
                  | OOS-only failure pattern not present
CFP-6 | TRIGGER   | train-best DSR = -20.8173 <= 0
                  | (PBO all below 0.50: 0.375, 0.219, 0.094)
CFP-7 | OK        | max-month 2025-06 with 11 trades = 7.4% (well below 50%)
CFP-8 | OK        | worst sensitivity degradation = 0.155R
                  | (axis N_comp = 6); below 0.20R threshold; no sign flip
CFP-9 | OK        | transition_rate_per_480 = 3.33 >= 1;
                  | 100% of variants produce >= 30 trades
CFP-10| OK        | optional-ratio-column access count = 0
CFP-11| OK        | no future bar / partial bar / signal-without-contraction /
                  | entry-beyond-L_delay / degenerate-double-transition observed
CFP-12| OK        | all forbidden-input audit counters = 0
```

**Binding drivers:** CFP-2, CFP-3, CFP-6 are all triggered. Per Phase 4w precedence, the lowest-numbered triggered CFP is the binding driver: **CFP-2 (negative BTC OOS HIGH expectancy) is the binding driver**; CFP-3 and CFP-6 are independent / co-binding. CFP-1 / CFP-9 explicitly do NOT trigger — C1's failure is categorically distinct from V2 (Phase 4l, CFP-1 critical) and G1 (Phase 4r, CFP-1 critical + CFP-9 independent).

## Required tables produced

All 32 binding tables produced under `data/research/phase4x/tables/`:

```text
1.  run_metadata.json
2.  manifest_references.csv
3.  parameter_grid.csv
4.  split_boundaries.csv
5.  feature_schema.csv
6.  signal_schema.csv
7.  compression_state_summary.csv
8.  compression_box_diagnostics.csv
9.  candidate_transition_rate_by_symbol_window_variant.csv
10. transition_distribution_by_month.csv
11. btc_train_variants.csv
12. btc_validation_variants.csv
13. btc_oos_variants.csv
14. eth_train_variants.csv
15. eth_validation_variants.csv
16. eth_oos_variants.csv
17. btc_train_best_variant.csv
18. btc_train_best_cost_cells.csv
19. non_contraction_m1.csv
20. c1_vs_always_active_m2.csv
21. delayed_breakout_m2.csv
22. m1_m2_m3_m4_m5_summary.csv
23. opportunity_rate_summary.csv
24. cost_sensitivity.csv
25. pbo_summary.csv
26. deflated_sharpe_summary.csv
27. cscv_rankings.csv
28. trade_distribution_by_month.csv
29. stop_distance_atr_diagnostics.csv
30. sensitivity_perturbation.csv
31. catastrophic_floor_predicates.csv
32. verdict_declaration.csv
33. forbidden_work_confirmation.csv  (Phase 4w-required audit table)
```

## Required plots produced

All 16 Phase 4w-required plots were attempted but **all were skipped** because matplotlib was unavailable in the project virtual environment (same outcome as Phase 4r). Per Phase 4w explicit rule ("plot absence does NOT automatically cause Verdict D when all 32 binding tables are complete and absence is documented"), plot absence does NOT change the verdict from C to D. The verdict-driving tables are all complete.

```text
Skipped (matplotlib unavailable):
  cumulative_R_BTC_train_validation_oos.png
  cumulative_R_ETH_train_validation_oos.png
  compression_transition_timeline_BTC.png
  compression_transition_timeline_ETH.png
  c1_vs_non_contraction_R_distribution.png
  c1_vs_always_active_mean_R.png
  delayed_breakout_comparison.png
  opportunity_rate_by_month_BTC.png
  candidate_transition_rate_by_variant.png
  dsr_distribution.png
  pbo_rank_distribution.png
  btc_oos_drawdown.png
  monthly_cumulative_R_BTC_oos.png
  trade_R_distribution.png
  stop_distance_atr_distribution.png
  compression_box_width_distribution.png
```

## Stop-condition audit

No stop condition triggered during the run:

- no manifest missing or SHA mismatch;
- no `research_eligible` mismatch (both 30m manifests are research_eligible: true);
- no local data file missing or corrupted;
- no forbidden input access (CFP-10 / CFP-12 audit counters all 0);
- no network I/O attempted;
- no credential / `.env` access;
- no write attempted to `data/raw/`, `data/normalized/`, or `data/manifests/`;
- no modification of existing `src/` / tests / scripts;
- no future-bar consumption (CFP-11 audit clean);
- no partial-bar consumption;
- no signal emitted without `contraction_recently_active` (CFP-11 audit field 0);
- no entry fired beyond `L_delay` (CFP-11 audit field 0);
- no trade emitted despite `R <= 0` (rejected at signal-generation; counted in rejection logic);
- no timestamp misalignment;
- no duplicate `(symbol, interval, open_time)` row;
- ruff / pytest / mypy all pass (785 tests; 82 source files);
- variant grid is exactly 32 (no expansion / contraction);
- variant ordering identical across train / validation / OOS;
- RNG seed pinned at 202604300;
- bootstrap completed B = 10 000 iterations on M1 / M2.a sample sizes (149 vs 793 / 149 vs 908) without sample-size collapse;
- CSCV computed exactly with S = 16 / C(16, 8) = 12 870 combinations (no silent approximation).

## Reproducibility evidence

```text
Manifest SHA pinning            : both 30m manifests pinned in
                                  run_metadata.json + manifest_references.csv
Commit SHA pinning              : <Phase 4x branch commit SHA — see
                                  Phase 4x closeout>
Deterministic variant ordering  : variant_id 0..31 mapped via lexicographic
                                  bit-encoding; preserved across
                                  train / validation / OOS / ETH
Pinned RNG seed                 : 202604300 (used for both bootstrap and
                                  any internal random ops)
Stable sorting                  : bars stable-sorted by (symbol, interval,
                                  open_time)
Idempotent outputs              : tables under data/research/phase4x/ are
                                  fully reproducible by re-running the
                                  same command with the same seed
No network                      : 0 network attempts; pyarrow + numpy +
                                  stdlib only
No credentials                  : 0 credential reads; 0 .env reads
Environment                     : Python 3.12.4; numpy and pyarrow versions
                                  recorded in run_metadata.json
```

## Verdict declaration

```text
Verdict       : C — C1 framework HARD REJECT
Basis         : CFP triggered (HARD REJECT): CFP-2, CFP-3, CFP-6
M1 pass       : False
M2 pass       : False
M3 pass       : False
M4 pass       : False
Best variant  : id=21, label=B=0.10|C=0.45|N=12|S=0.10|T=2.0
Run complete  : 2026-05-04T01:09:11.031198+00:00 UTC
```

**C1 first-spec is terminally HARD REJECTED as retained research evidence only.**

## What this does not authorize

Phase 4x does NOT authorize:

- Phase 4y or any successor phase;
- C1 implementation in `src/prometheus/`;
- C1 backtest rerun;
- C1 spec amendment based on Phase 4x forensic numbers;
- Phase 4w methodology amendment based on Phase 4x forensic numbers;
- C1-prime / C1-narrow / C1-extension / C1 hybrid;
- G1-prime / G1-narrow / G1-extension / G1 hybrid;
- V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- F1 / D1-A / R2 rescue;
- 5m strategy / hybrid;
- ML feasibility;
- microstructure / aggTrades / mark-price / spot / cross-venue acquisition;
- paper / shadow / live / exchange-write;
- Phase 4 canonical;
- production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials.

## Forbidden-work confirmation

Phase 4x did NOT do any of the following:

- modify `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run any acquisition / diagnostics / prior-phase backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict;
- change any project lock;
- create a runnable strategy under `src/prometheus/`;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- propose a 5m strategy / hybrid / variant;
- start Phase 4y / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding; CFP-9 independent; terminal for G1 first-spec)
C1                  : HARD REJECT (Phase 4x — Verdict C; CFP-2 binding;
                       CFP-3 / CFP-6 co-binding; terminal for C1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w
                            : all preserved verbatim
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in Phase 4w;
                              backtest executed in Phase 4x (this phase) =
                              Verdict C HARD REJECT;
                              not implemented; not validated; not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : remain paused;
                              post-C1 consolidation memo (analogous to
                              Phase 4s post-G1) conditional secondary
```

## Operator decision menu

- **Option A — primary recommendation:** remain paused. Phase 4x has produced a clean Verdict C HARD REJECT for C1 first-spec. The project record now contains six terminal strategy verdicts (R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 HARD REJECT; G1 HARD REJECT; C1 HARD REJECT) plus the H0 framework anchor and R3 baseline-of-record (with R1a / R1b-narrow as retained non-leading research evidence). No new ex-ante hypothesis is currently under consideration. Remaining paused gives the operator time to review the post-C1 evidence before authorizing any successor phase.
- **Option B — conditional secondary:** Phase 4y — Post-C1 Strategy Research Consolidation Memo (docs-only), analogous to Phase 4s (post-G1) and Phase 4m (post-V2). Phase 4y would consolidate Phase 4x findings into the project's strategy-research record, update the rejection topology with C1's distinct failure mode (fires-and-loses; contraction-anti-validation), and reaffirm every retained verdict / project lock without authorizing rescue or successor.

NOT recommended:

- C1 implementation in `src/prometheus/` — REJECTED;
- C1 rerun with relaxed thresholds — REJECTED;
- Phase 4v amendment / Phase 4w amendment based on Phase 4x forensic numbers — REJECTED;
- C1-prime / C1-narrow / C1-extension / C1 hybrid — FORBIDDEN;
- G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN;
- paper / shadow / live-readiness — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write — FORBIDDEN.

## Next authorization status

```text
Phase 4y (post-C1 consolidation): NOT authorized
Phase 4z and beyond              : NOT authorized
Phase 4 (canonical)              : NOT authorized
Paper / shadow                   : NOT authorized
Live-readiness                   : NOT authorized
Deployment                       : NOT authorized
Production-key creation          : NOT authorized
Authenticated REST               : NOT authorized
Private endpoints                : NOT authorized
User stream / WebSocket          : NOT authorized
Exchange-write capability        : NOT authorized
MCP / Graphify                   : NOT authorized
.mcp.json / credentials          : NOT authorized
C1 implementation                : NOT authorized; terminal-rejected
C1 rerun                         : NOT authorized; terminal-rejected
C1 spec amendment                : NOT authorized; FORBIDDEN
Phase 4w methodology amendment   : NOT authorized; FORBIDDEN
G1 / V2 / R2 / F1 / D1-A rescue  : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes     : NOT authorized; FORBIDDEN
V2-prime / V2-variant            : NOT authorized; FORBIDDEN
C1-prime / C1-extension          : NOT authorized; FORBIDDEN
Retained-evidence rescue         : NOT authorized; FORBIDDEN
5m strategy / hybrid             : NOT authorized; not proposed
ML feasibility                   : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                 : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                 : NOT authorized; FORBIDDEN
```

The next step is operator-driven: the operator decides whether to remain paused or authorize Phase 4y (Post-C1 Strategy Research Consolidation Memo, docs-only). Until then, the project remains at the post-Phase-4x C1 HARD REJECT boundary on the Phase 4x branch (not merged to main).

---

**Phase 4x is docs-and-code in standalone-script mode. No source code, tests, existing scripts, data, manifests, or successor phases were created or modified. Final Verdict: C — C1 framework HARD REJECT (CFP-2 binding; CFP-3 / CFP-6 co-binding; terminal for C1 first-spec). Recommended state: remain paused; post-C1 consolidation memo conditional secondary. No next phase authorized.**
