# Phase 4r — G1 Backtest Execution

**Authority:** Operator authorization for Phase 4r (Phase 4q §"Operator decision menu" Option A primary recommendation: Phase 4r — G1 Backtest Execution, docs-and-code standalone research script). Phase 4q (G1 Backtest-Plan Memo, methodology binding); Phase 4p (G1 Strategy Spec Memo, locked); Phase 4o (G1 hypothesis-spec); Phase 4n (Candidate B selection); Phase 4m (18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility, preserved but unused); Phase 4i (acquired research-eligible v001 30m / 4h klines); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4r — **G1 Backtest Execution** (docs-and-code). Implements and runs the standalone G1 backtest exactly as predeclared by Phase 4q. **Phase 4r does NOT implement G1 inside `src/prometheus/`. Phase 4r does NOT modify runtime / execution / persistence / risk / exchange / strategy modules. Phase 4r does NOT modify tests or existing scripts. Phase 4r does NOT acquire data, modify data, or modify manifests. Phase 4r does NOT authorize paper / shadow / live / exchange-write.**

**Branch:** `phase-4r/g1-backtest-execution`. **Run date:** 2026-05-03 UTC.

---

## Summary

Phase 4r implemented `scripts/phase4r_g1_backtest.py` as a standalone research backtest script (pure pyarrow + numpy + stdlib; no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no `requests/httpx/aiohttp/websockets/urllib`; no `.env` reads; no credentials; no Binance API calls; no network I/O) and ran the predeclared G1 — Regime-First Breakout Continuation backtest exactly under the Phase 4q methodology over the locked train (2022-01-01..2023-06-30 UTC) / validation (2023-07-01..2024-06-30 UTC) / OOS holdout (2024-07-01..2026-03-31 UTC) windows on BTCUSDT-primary / ETHUSDT-comparison, evaluating all 32 variants of the Phase 4p locked grid across LOW / MEDIUM / HIGH cost cells with §11.6 = 8 bps preserved verbatim, computing M1 / M2 / M3 / M4 with bootstrap (B = 10 000; pinned RNG seed 202604300), PBO (train→validation; train→OOS) and CSCV PBO with S = 16 / C(16, 8) = 12 870 combinations, deflated Sharpe with N = 32, and 12 catastrophic-floor predicate evaluations. **Final verdict: C — G1 framework HARD REJECT.** Binding catastrophic-floor driver: **CFP-1 critical** — 32 / 32 variants produced fewer than 30 OOS HIGH trades on BTCUSDT; the BTC-train-best variant produced **0 OOS HIGH trades**. Subordinate triggers: **CFP-9** (regime active fraction = 2.03% < 5% threshold on BTC OOS for the train-best variant), **CFP-3** (mechanically triggered because profit-factor = 0 under empty arrays, subordinate to CFP-1), and **CFP-4** (degenerate trigger: M3 BTC FAIL AND a trivial M4 ETH "PASS" because both ETH active and inactive populations are 0 — also subordinate to CFP-1). M1 / M2 / M3 mechanism checks were not meaningfully evaluable due to the zero-trade G1 active population. **Always-active baseline produced 124 trades on OOS HIGH with mean_R = −0.34** and **inactive-population pseudo-trades produced 124 trades on OOS HIGH with mean_R = −0.34** for the train-best variant — confirming the breakout-and-stop machinery itself does fire, but G1's 5-dimension regime gate intersected with the 30m Donchian breakout produces zero qualifying candidates. **Root mechanism observation (forensic, NOT a parameter-selection input):** Phase 4p's locked composite regime classifier (HTF trend AND DE_4h ≥ E_min AND ATR percentile in band AND relative-volume ≥ V_liq_min AND funding percentile in band) is so narrow that for every variant in the 32-variant grid, the breakout-trigger arrival times and the regime-active windows do not intersect on BTCUSDT OOS HIGH. **G1 first-spec is terminally HARD REJECTED as retained research evidence only**, structurally analogous to Phase 4l V2 Verdict C but at a different mechanism layer (regime-gate-meets-setup intersection vs. V2's stop-distance-filter rejection). **No G1 rescue authorized:** no G1-prime, G1-narrow, G1-extension, classifier-relaxation amendment, K_confirm amendment, ATR-band amendment, V_liq_min amendment, funding-band amendment, E_min amendment, breakout-rule amendment, or Phase 4p G1 strategy-spec amendment is authorized by Phase 4r. **No V2 / F1 / D1-A / R2 rescue authorized.** **No paper / shadow / live / exchange-write authorized.** Whole-repo quality gates remain clean (`ruff check .` PASS; `pytest` 785 PASS; `mypy --strict` 0 issues across 82 source files).

## Authority and boundary

- **Authority granted:** create `scripts/phase4r_g1_backtest.py`; read existing local normalized data (Phase 4i 30m / 4h klines + v002 funding); read existing manifests (read-only, SHA-pinned); write local gitignored research outputs under `data/research/phase4r/`; create the Phase 4r execution report (this file); create the Phase 4r closeout artefact.
- **Authority NOT granted:** implement G1 inside `src/prometheus/` (forbidden); modify any source / test / script / data / manifest (forbidden); acquire data (forbidden); modify Phase 4p / 4q / 4j §11 / 4k / 3v §8 / 3w §6 / §7 / §8 / 3r §8 governance (forbidden); revise any retained verdict (forbidden); start Phase 4s or any successor phase (forbidden); authorize paper / shadow / live / exchange-write / production keys (forbidden).
- **Hard rule:** Phase 4r does NOT modify the Phase 4p G1 strategy-spec selections nor introduce any G1-prime / G1-narrow / G1-extension. The verdict in this report stands on the Phase 4p locked spec exactly.

## Starting state

```text
Branch (Phase 4r):          phase-4r/g1-backtest-execution
main / origin/main:         e019bee97edb689d5b36d5270bb577de04b2a24a (unchanged)
Phase 4q memo commit:       44e0fde6eb9ac44d24da710c49ceaecc5454c961 (merged)
Phase 4q closeout commit:   e85e3839966cf0a9e66d350dd3c2d5ace1944808 (merged)
Phase 4q merge commit:      b6d9595018af9e29a4bbb9ce0d72d64516c531d1 (merged)
Phase 4q housekeeping:      e019bee97edb689d5b36d5270bb577de04b2a24a (merged)
Working-tree state:         clean except for the Phase 4r script and reports
Quality gates (initial):    ruff PASS; pytest 785 PASS; mypy strict 0 issues
                            across 82 source files
```

## Relationship to Phase 4q

- Phase 4q **defined the future G1 backtest methodology** in full (data inputs and manifest handling; standalone-script boundary; exact future command shape; explicit-column data-loading rules; deterministic feature-computation algorithms; composite regime-classifier pseudocode; deterministic regime-state-machine update rules; signal generation; entry / exit simulation; cost / funding model; position-sizing / exposure rules; threshold-grid handling for the locked Phase 4p 32-variant grid (= 2^5) over five binary axes; M1 / M2 / M3 / M4 mechanism-check implementation plans with the Phase 4p numeric thresholds; PBO / DSR / CSCV plan; chronological train / validation / OOS holdout windows reused verbatim from Phase 4k; BTCUSDT-primary / ETHUSDT-comparison protocol; 12 catastrophic-floor predicates; Verdict A / B / C / D taxonomy; required reporting tables; required plots; 24-item stop-condition list; reproducibility requirements with pinned RNG seed 202604300 and manifest SHA pinning).
- Phase 4q **did NOT authorize Phase 4r execution.**
- The operator now explicitly authorized Phase 4r.
- Phase 4r is docs-and-code (script + reports + local gitignored outputs).
- **Phase 4r implementation matches Phase 4q methodology exactly.** No Phase 4q methodology amendment is introduced.

## Methodology adherence statement

Phase 4r implements Phase 4q exactly. All Phase 4q binding rules are honored:

- Standalone-script boundary at `scripts/phase4r_g1_backtest.py` (no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no `requests / httpx / aiohttp / websockets / urllib`; no `.env`; no credentials; no Binance API; no network I/O).
- Pure pyarrow + numpy + stdlib runtime stack (mirroring Phase 4l).
- Local Parquet inputs only (Phase 4i v001 30m / 4h trade-price klines for BTCUSDT and ETHUSDT; v002 funding for BTCUSDT and ETHUSDT). No metrics OI; no optional ratio columns; no mark-price; no aggTrades; no spot / cross-venue; no 5m diagnostic outputs as features.
- Manifest SHA pinning + `research_eligible` verification at startup; convention: v002 funding manifests lack the `research_eligible` field and are treated as eligible by inheritance from prior phases.
- Locked 32-variant grid over five binary axes (`E_min`, ATR band, `V_liq_min`, funding band, `K_confirm`); deterministic lexicographic variant ordering documented in `run_metadata.json`; **N_R and T_stop are fixed (not active axes).**
- Locked fixed parameters: `N_breakout = 12`, `B_atr = 0.10`, `N_stop = 12`, `S_buffer = 0.10`, stop-distance bounds `[0.50, 2.20] × ATR(20)`, `N_R = 2.0`, `T_stop = 16`, `C_cooldown = 4`, EMA pair `(20, 50)` on 4h, slope-rising lookback `3` 4h bars, DE lookback `12` 4h bars, ATR period `20`, ATR percentile lookback `480` 30m bars, liquidity median lookback `480` 30m bars, funding lookback `90` events.
- Position sizing preserved verbatim from §1.7.3: 0.25% risk per trade; 2× leverage cap; one position max; sizing equity 100 000 USDT (R-relative; no compounding).
- Cost model preserved verbatim from §11.6: LOW = 1 bp, MEDIUM = 4 bps, HIGH = 8 bps slippage per side; taker fee 4 bps per side; no maker rebates; no live fee assumption; funding cost included.
- Validation windows reused verbatim from Phase 4k: train 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC; validation 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC; OOS holdout 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC.
- BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC (CFP-4 enforced).
- Bootstrap B = 10 000; RNG seed = 202604300 pinned.
- DSR with N = 32, M = 1, skew/kurtosis correction; DSR-aware train-best variant selection (with raw-Sharpe tie-break).
- PBO train→validation, train→OOS as rank-based proxies; CSCV with S = 16 sub-samples, C(16, 8) = 12 870 combinations enumerated exactly; PBO_cscv reported.
- All 12 CFPs evaluated. CFPs 10 / 11 / 12 enforced runtime-stop by construction (the script's only data path is the explicit-column kline + funding loaders); CFPs 1..9 evaluated post-run.
- Verdict A / B / C / D taxonomy applied.
- Random-regime baseline NOT included (Phase 4q decision: diagnostic only; not binding; not implemented).

## Script implementation summary

`scripts/phase4r_g1_backtest.py` is a single-file standalone research script. Its module-level layout:

```text
- Constants block (Phase 4p locked fixed parameters, §1.7.3 risk locks,
  §11.6 cost cells, mechanism thresholds, CFP thresholds, DSR significance).
- StopCondition exception (raised on any Phase 4q stop condition).
- Data classes: ManifestRef, SymbolKlineData, SymbolFundingData, Variant,
  TradeRecord, VariantResult, StateMachineTrace, SymbolFeatures,
  RunPaths, RunContext.
- Manifest loader with SHA256 pinning + research_eligible verification.
- Explicit-column Parquet loaders for klines (open_time, close_time, open,
  high, low, close, volume) and funding (funding_time, funding_rate).
- Feature computation: ema_seeded, true_range, atr_wilder,
  directional_efficiency, rolling_max/min/percentile/median (excluding
  current bar), funding_percentile_at_timestamp, compute_htf_trend_state,
  build_companion_30m_idx_for_4h, build_latest_completed_4h_idx_for_30m,
  compute_symbol_features.
- build_variants(): deterministic lexicographic 32-variant grid.
- compute_favorable_per_4h(): per-variant 4h favorable_long/short arrays.
- run_state_machine_4h(): deterministic 4-state transitions per Phase 4q.
- compute_breakout_signals(): direction-blind 30m Donchian.
- map_4h_state_to_30m_active / inactive: regime-active / inactive masks.
- simulate_trades_for_signal_array(): entry / exit / cost / funding;
  stop > take-profit > time-stop precedence with stop-first tie-break.
- aggregate_trades(): per-window VariantResult (trade_count, win_rate,
  mean_R, median_R, total_R, max_dd_R, profit_factor, sharpe).
- Statistics: _norm_inv (Acklam), expected_max_sharpe_random,
  compute_skewness_kurtosis, deflated_sharpe_ratio,
  bootstrap_diff_mean_ci, _sharpe, cscv_pbo, pbo_rank_based.
- CSV / JSON writers; UTC parsing helper; optional matplotlib plotters
  (graceful skip when matplotlib is not installed).
- main() orchestration: argparse, RunContext, manifest loading, data
  loading, variant grid, per-variant simulation across symbols and cost
  cells with G1 / always-active / inactive populations, train-best
  variant selection by DSR, M1 / M2 / M3 / M4 evaluation, PBO + CSCV,
  CFP-1..CFP-12 evaluation, verdict declaration, table writes, plot
  writes, run_metadata.json.
```

The script is parsed by Python (`python -c "import ast; ast.parse(...)"`) at write time and passes ruff. The script only writes to `data/research/phase4r/` (gitignored); never to `data/raw/`, `data/normalized/`, or `data/manifests/`.

## Data inputs and manifest SHA pinning

Manifest references pinned in `data/research/phase4r/tables/manifest_references.csv`:

```text
binance_usdm_btcusdt_30m__v001       Phase 4i 30m klines, research_eligible=true
binance_usdm_btcusdt_4h__v001        Phase 4i 4h  klines, research_eligible=true
binance_usdm_btcusdt_funding__v002   v002 funding, research_eligible=true (by convention)
binance_usdm_ethusdt_30m__v001       Phase 4i 30m klines, research_eligible=true
binance_usdm_ethusdt_4h__v001        Phase 4i 4h  klines, research_eligible=true
binance_usdm_ethusdt_funding__v002   v002 funding, research_eligible=true (by convention)
```

Each manifest's SHA256 is computed at run start and recorded in `manifest_references.csv`. The full manifest references CSV is committed (small) under `data/research/phase4r/tables/manifest_references.csv` is local-only / gitignored; the SHAs are computed deterministically from the manifests in `data/manifests/`.

**No Phase 4i metrics manifests are loaded** (Phase 4j §11 governance preserved verbatim but unused). **No mark-price manifests are loaded** (Phase 3r §8 governance preserved). **No 5m manifests are loaded** (Phase 3o / 3p / 3q diagnostic-only governance preserved).

**No manifest is modified.** **No new manifest is created.** **No data is acquired.** **No write occurs to `data/raw/`, `data/normalized/`, or `data/manifests/`.**

## Forbidden input verification

Static-scan results (run before backtest execution; counts of substring occurrences in `scripts/phase4r_g1_backtest.py`):

```text
forbidden imports                      occurrences
  import requests                      0
  import httpx                         0
  import aiohttp                       0
  import urllib3                       0
  from urllib.request                  0
  from urllib import request           0
  import websockets                    0
  import websocket                     0
  from prometheus.runtime              0
  import prometheus.runtime            0
  from prometheus.execution            0
  import prometheus.execution          0
  from prometheus.persistence          0
  import prometheus.persistence        0

forbidden data names                   occurrences
  metrics_oi                           2  (audit-counter field name only;
                                          runtime access count = 0)
  metrics OI                           0
  sum_open_interest                    0
  count_toptrader_long_short_ratio     0
  sum_toptrader_long_short_ratio       0
  count_long_short_ratio               0
  sum_taker_long_short_vol_ratio       0
  markprice                            0
  mark_price                           2  (audit-counter field name only;
                                          runtime access count = 0)
  aggTrades                            0
  aggtrades                            2  (audit-counter field name only;
                                          runtime access count = 0)
  spot data                            0
  cross-venue                          0
  cross_venue                          2  (audit-counter field name only;
                                          runtime access count = 0)
  ' Q1 ' .. ' Q7 '                     0
```

The four substrings remaining (`metrics_oi`, `mark_price`, `aggtrades`, `cross_venue`) appear exclusively as **audit-counter field names** that record `0` in `forbidden_work_confirmation.csv` and in the CFP-12 detail dict. Per Phase 4q §"Static scan nuance": "If the script must include forbidden names for guard checks, document why and ensure runtime access count is zero." **All audited access counts are zero.** The script's only data path is via the explicit-column Parquet loaders for klines and funding; there is no code path that would access metrics, mark-price, aggTrades, spot, or cross-venue data.

Runtime access counts (from `forbidden_work_confirmation.csv`):

```text
metrics_oi_access_count                    0
mark_price_access_count                    0
aggtrades_access_count                     0
spot_access_count                          0
cross_venue_access_count                   0
optional_ratio_column_access_count         0
network_io_attempts                        0
credential_reads                           0
env_file_reads                             0
data_raw_writes                            0
data_normalized_writes                     0
data_manifest_modifications                0
v003_creations                             0
src_prometheus_modifications               0
test_modifications                         0
existing_script_modifications              0
```

## Future-script-boundary compliance

```text
Path:                          scripts/phase4r_g1_backtest.py
Imports (top-level):           argparse, hashlib, itertools, json, math, sys,
                               collections.abc.Sequence,
                               dataclasses.dataclass / field,
                               datetime (UTC, datetime, timedelta),
                               pathlib.Path, typing.Any,
                               numpy, pyarrow.parquet
Imports (optional, guarded):   matplotlib (try-imported in plot helpers;
                               graceful skip if absent — was absent in this
                               run; all plots reported as skipped).
Network libraries imported:    none
.env reads:                    none
Credential reads:              none
Binance API calls:             none
data.binance.vision contact:   none (no network I/O)
Writes:                        only to data/research/phase4r/ (gitignored)
RNG seed:                      202604300 (pinned; passed to numpy default_rng)
prometheus.* imports:          none
exchange adapter imports:      none
```

## Backtest command

Exact command run (PowerShell-friendly):

```text
.venv/Scripts/python scripts/phase4r_g1_backtest.py \
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
  --output-dir data/research/phase4r \
  --rng-seed 202604300
```

No deviation from the Phase 4q predeclared command shape.

## Output directory

```text
data/research/phase4r/
├── run_metadata.json
├── tables/
│   ├── manifest_references.csv
│   ├── parameter_grid.csv
│   ├── split_boundaries.csv
│   ├── feature_schema.csv
│   ├── regime_state_transitions.csv
│   ├── regime_active_fraction_by_symbol_window.csv
│   ├── btc_train_variants.csv
│   ├── btc_validation_variants.csv
│   ├── btc_oos_variants.csv
│   ├── eth_train_variants.csv
│   ├── eth_validation_variants.csv
│   ├── eth_oos_variants.csv
│   ├── btc_train_best_variant.csv
│   ├── btc_train_best_cost_cells.csv
│   ├── active_vs_inactive_m1.csv
│   ├── g1_vs_always_active_m2.csv
│   ├── m1_m2_m3_m4_summary.csv
│   ├── cost_sensitivity.csv
│   ├── pbo_summary.csv
│   ├── deflated_sharpe_summary.csv
│   ├── cscv_rankings.csv
│   ├── trade_distribution_by_month_regime.csv
│   ├── catastrophic_floor_predicates.csv
│   ├── verdict_declaration.csv
│   └── forbidden_work_confirmation.csv
└── plots/                       (empty in this run; matplotlib unavailable)
```

`data/research/phase4r/` is gitignored and not committed.

## Data-loading verification

- 30m kline columns loaded explicitly: `[open_time, close_time, open, high, low, close, volume]`. Total rows per symbol: **74 448** (BTCUSDT and ETHUSDT identical).
- 4h kline columns loaded explicitly: `[open_time, close_time, open, high, low, close, volume]`. Total rows per symbol: **9 306** (BTCUSDT and ETHUSDT identical).
- Funding columns loaded explicitly: `[funding_time, funding_rate]`. Funding event count: BTCUSDT and ETHUSDT v002 (multi-year). The optional `mark_price` column on the funding parquet schema is **NOT** loaded.
- All frames stable-sorted by `open_time` (klines) / `funding_time` (funding) ascending.
- Duplicate-row check: zero duplicates detected per symbol per interval (no stop condition triggered).
- Timestamp policy verified: integer milliseconds; bar identity = (symbol, interval, open_time).
- Completed-bar discipline: features and signals consume `close_time <= now_decision`; no partial-bar consumption.

## Feature-computation verification

All Phase 4q feature plans implemented:

```text
EMA(20) on 4h close          (Wilder-style alpha = 2/(n+1); SMA seed)
EMA(50) on 4h close          (Wilder-style alpha = 2/(n+1); SMA seed)
EMA20 discrete slope-rising  (vs t-3 4h bars; Phase 3w)
DE_4h (12-bar)               (|close[t] - close[t-12]| / sum(|diff|))
ATR_20 on 30m                (Wilder; SMA seed over first 20 30m TRs)
ATR_pct_480                  (percentile rank of ATR_20 in prior 480 bars)
relative_volume              (volume / median(prior 480-bar volume))
funding_pct_90               (rank in trailing 90 funding events at t_4h)
prior_12_high                (max high over prior 12 30m bars; excl. current)
prior_12_low                 (min low  over prior 12 30m bars; excl. current)
structural_stop_long         (prior_12_low - 0.10 x ATR_20)
structural_stop_short_high   (prior_12_high + 0.10 x ATR_20)
stop_distance_atr            (|entry - stop| / ATR_20)
companion_30m_idx_for_4h     (30m bar with close_time == 4h close_time)
latest_completed_4h_idx_for_30m  (lookup for state-machine state per 30m bar)
```

All features use prior-completed bars only. Warmup periods produce NaN until enough lookback exists; classifier evaluates as `unfavorable` during warmup.

## Regime-classifier verification

Composite classifier evaluated per 4h bar (independent of breakout signal):

- HTF trend state: `+1 LONG` if `EMA_20 > EMA_50 AND close_4h > EMA_20 AND EMA_20[t] > EMA_20[t-3]`; `-1 SHORT` mirror; `0 NEUTRAL` otherwise.
- DE pass: `DE_4h(t) >= V.E_min`.
- ATR pass: `V.P_atr_low <= ATR_pct_480(companion_30m) <= V.P_atr_high`.
- Liquidity pass: `relative_volume(companion_30m) >= V.V_liq_min`.
- Funding pass: `V.P_fund_low <= funding_pct_90(t_4h) <= V.P_fund_high`.
- `favorable_long(t_4h, V) = (HTF == LONG) AND DE_pass AND ATR_pass AND LIQ_pass AND FUND_pass`.
- `favorable_short` = mirror.
- `unfavorable` = NOT favorable_long AND NOT favorable_short.

Classifier hard rules verified (CFP-11 = false in `catastrophic_floor_predicates.csv`):

- Classifier does not consult breakout signal (signal is computed downstream).
- Classifier does not consult future bars (all features use prior-completed lookback only).
- Classifier does not consult 5m diagnostic outputs (no 5m data loaded).
- Classifier does not use V2 Phase 4l forensic numbers (Phase 4p locked thresholds only).

## Regime-state-machine verification

Four-state machine implemented per Phase 4q §"Regime-state-machine implementation plan":

```text
States:        0=inactive, 1=candidate, 2=active, 3=cooldown
Direction:     0=none, +1=long, -1=short
K_confirm:     {2, 3}      (axis 5 of grid)
C_cooldown:    4           (fixed)
```

Transitions evaluated only on completed 4h bar boundaries; per-(symbol, variant) independent traces. Hard rules verified:

- No direction switch inside `regime_active`.
- No entries outside `regime_active` (signal generation is gated by the per-30m-bar mapping `latest_completed_4h_idx_for_30m`).
- Position lifecycle independent of regime state after entry (Option A).
- Trade-driven cooldown supported via `exit_event_4h_idx` (kept for interface completeness; the train-best variant produced zero trades, so no exit events were emitted in the final run; the state-machine forced-exit branch is reachable but not exercised in this dataset).

## Signal-generation verification

```text
At each completed 30m bar t_30m:
  read s_4h(t_30m) = state at latest_completed_4h_idx_for_30m[t_30m]
  if s_4h != regime_active: no signal evaluated.
  if regime_active LONG:
    long_setup := close_30m[t] > prior_12_high[t] + 0.10 * ATR_20[t]
  if regime_active SHORT:
    short_setup := close_30m[t] < prior_12_low[t]  - 0.10 * ATR_20[t]
  apply stop-distance gate at entry-time using next-bar open and structural
    stop computed at signal close: REJECT if not in [0.50, 2.20] x ATR_20.
```

No 5m triggers. No V2 8-feature AND chain. No R2 pullback-retest. No F1 mean-reversion. No D1-A funding-Z-score directional rule. One signal evaluation per completed 30m bar per variant per symbol.

CFP-11 `signal_outside_active_count = 0` confirmed: signals are emitted only when the latest-completed-4h state is `regime_active`.

## Entry / exit simulation verification

```text
Entry:                     market at next 30m bar open after accepted signal close
Stop:                      structural stop fixed at entry; not widened
Target:                    fixed +2.0 R take-profit
Time-stop:                 16 completed 30m bars; exit at next bar open
Stop precedence:           stop > take-profit > time-stop
Same-bar tie-break:        stop wins (conservative)
No break-even:             yes
No trailing stop:          yes
One position max:          yes; new candidates dropped while positioned
No pyramiding:             yes
No reversal while positioned: yes
BTCUSDT primary:           yes
ETHUSDT comparison only:   yes (no portfolio P&L; same 32 variants per symbol)
```

## Cost / funding model verification

```text
LOW    = 1   bp slippage per side
MEDIUM = 4   bps slippage per side
HIGH   = 8   bps slippage per side    (§11.6 promotion gate; verbatim)
Taker fee per side = 4 bps
No maker rebates
No live fee assumption
Funding cost: applied at every completed funding event whose funding_time
  is strictly between entry_open_time and exit_realized_time;
  sign convention: positive funding rate => longs pay shorts; v002 funding
  manifest funding_rate is the per-event rate.
Funding cost included in trade_R = (raw_R + funding_cost_R).
```

## Position-sizing / exposure verification

```text
sizing_equity        = 100 000 USDT (constant; R-relative results;
                       no compounding)
risk_fraction        = 0.0025
max_leverage         = 2.0
max_positions        = 1
max_active_stops     = 1
position_size_units  = sizing_equity * risk_fraction / abs(R_per_unit)
leverage cap applied if position_notional > max_leverage * sizing_equity
below-min-notional / zero-rounded handling: implementation-level only;
  no stop condition triggered in this run because (a) trade count is zero
  for the train-best variant, and (b) the simulation is R-based.
```

## Threshold-grid summary

```text
Variant count:                 32  (= 2^5)
Axes (lexicographic order):
  ATR_band      in {[20, 80], [30, 70]}
  E_min         in {0.30, 0.40}
  K_confirm     in {2, 3}
  V_liq_min     in {0.80, 1.00}
  funding_band  in {[15, 85], [25, 75]}
Variant ordering:              deterministic lexicographic
                               (documented in run_metadata.json)
Grid extension:                forbidden (none performed)
Grid reduction:                forbidden (all 32 variants reported)
N_R fixed at 2.0:              not an active axis (Phase 4p locked)
T_stop fixed at 16:            not an active axis (Phase 4p locked)
```

## Search-space-control summary

```text
DSR  N = 32, M = 1, skew/kurtosis correction; train-best variant selected
     by DSR-aware criterion (raw-Sharpe tie-break).
PBO  train -> validation = 0.000   (rank-based proxy)
PBO  train -> OOS         = 0.000   (rank-based proxy)
CSCV S = 16; C(16, 8) = 12 870 combinations enumerated.
PBO_cscv = 0.500 (mechanically trivial under degenerate populations
               with widespread zero-trade variants).
```

## Train / validation / OOS windows

Reused verbatim from Phase 4k:

```text
Train          : 2022-01-01 00:00:00 UTC .. 2023-06-30 23:30:00 UTC  (~18 months)
Validation     : 2023-07-01 00:00:00 UTC .. 2024-06-30 23:30:00 UTC  (~12 months)
OOS holdout    : 2024-07-01 00:00:00 UTC .. 2026-03-31 23:30:00 UTC  (~21 months;
                                                                     primary G1 evidence cell)
```

Same 32 variants evaluated independently per symbol; no cross-symbol optimization; train-best variant identifier is carried into validation and OOS reporting.

## BTCUSDT primary results

Train-best variant identifier (BTCUSDT, train, MEDIUM cost, G1 population): **id=0** (label `E=0.30|ATR=[20,80]|Vliq=0.80|Fund=[15,85]|K=2`). DSR(train) = 0.000; raw Sharpe(train) = 0.000.

```text
BTC train-best (id=0) cost-cell breakdown:
  window         cost_cell  trade_count  mean_R  total_R  max_dd_R  PF  sharpe
  train          LOW        0            0       0        0         0   0
  train          MEDIUM     0            0       0        0         0   0
  train          HIGH       0            0       0        0         0   0
  validation     LOW        0            0       0        0         0   0
  validation     MEDIUM     0            0       0        0         0   0
  validation     HIGH       0            0       0        0         0   0
  oos            LOW        0            0       0        0         0   0
  oos            MEDIUM     0            0       0        0         0   0
  oos            HIGH       0            0       0        0         0   0
```

All 32 variants × 3 cost cells × 3 windows for BTCUSDT G1 produced **zero trades**. The maximum BTC G1 trade count across all 32 variants × all windows × all cost cells is small (training MEDIUM total trades across all 32 variants = 4; OOS HIGH total across all 32 variants = 0). The G1 regime-active fractions are very narrow on BTC (train-best variant: train 3.60%, validation 1.46%, OOS 2.03%).

## ETHUSDT comparison results

```text
ETH train-best (id=0) cost-cell breakdown:
  All windows / cost cells: trade_count = 0
```

ETH G1 produces zero qualifying trades for the train-best variant across all windows and cost cells. ETH cannot rescue BTC (CFP-4 enforced; M3 BTC FAIL with M4 ETH "trivial PASS" triggers CFP-4).

## Cost sensitivity results

Across 32 variants × LOW / MEDIUM / HIGH × train / validation / OOS × BTC / ETH:

- All BTC G1 cells have `trade_count = 0` and `mean_R = 0` for the train-best variant (id 0). A handful of other variants produce 1–2 trades on train MEDIUM but never reach the 30-trade threshold on OOS HIGH.
- HIGH cost (the §11.6 promotion gate) preserves verbatim the same null result: G1's regime gate exclusion dominates the cost-sensitivity analysis. There is no "HIGH cost survives" finding for any G1 cell.

## M1 regime-validity negative-test results

```text
G1 active OOS HIGH (train-best id=0):    n=0,   mean_R=0.0
inactive OOS HIGH (same variant):        n=124, mean_R=-0.3416
diff (active - inactive):                0.0    (degenerate; active is empty)
bootstrap 95% CI (B=10,000):             [0.0, 0.0]
Pass threshold:                          diff >= +0.10R AND CI_lower > 0
M1 result:                               FAIL
```

The inactive-population pseudo-trades (breakouts during regime_inactive / candidate / cooldown) on the train-best variant produce 124 trades with mean_R = −0.34 on OOS HIGH. The active population is empty. The differential is methodologically un-evaluable; M1 reports FAIL by construction.

## M2 regime-gating value-add results

```text
G1 OOS HIGH (train-best id=0):                        n=0,   mean_R=0.0
always-active baseline OOS HIGH (same variant):       n=124, mean_R=-0.3416
diff (G1 - always-active):                            0.0    (degenerate)
bootstrap 95% CI (B=10,000):                          [0.0, 0.0]
Pass threshold:                                       diff >= +0.05R AND CI_lower > 0
M2 result:                                            FAIL
```

Always-active baseline (same Donchian breakout, same stop, same target, same time-stop, same cost cell, no regime gate) produces 124 trades on OOS HIGH with mean_R = −0.34. G1 regime gate produces 0 trades. M2 cannot evaluate non-trivially; reports FAIL.

## M3 inside-regime co-design validity results

```text
BTC OOS HIGH mean_R (train-best id=0):                0.0
BTC OOS HIGH trade_count:                             0
Pass threshold:                                       mean_R > 0 AND
                                                      trade_count >= 30 AND
                                                      no CFP-1 / 2 / 3
M3 result:                                            FAIL
```

## M4 cross-symbol robustness results

```text
ETH OOS HIGH G1 - inactive_R differential (id=0):     0.0  (both populations empty)
BTC differential (G1 - inactive):                     0.0  (both populations empty)
Directional consistency:                              True (degenerate; both 0)
Pass threshold:                                       eth_diff >= 0 AND directional consistency
M4 result:                                            PASS (degenerate / trivial)
ETH cannot rescue BTC:                                CFP-4 enforces this:
                                                      M3 FAIL AND M4 PASS = trigger.
```

The M4 "PASS" is degenerate because both ETH G1 and ETH inactive populations are empty for the train-best variant, producing a `0 ≥ 0` differential. Phase 4q's CFP-4 is exactly the safeguard: a degenerate ETH PASS does not rescue a BTC FAIL. CFP-4 is triggered (see "Catastrophic-floor predicate results" below).

## Negative-test diagnostics

The active-vs-inactive (M1) and always-active (M2) negative tests are reported above. Random-regime baseline was not included by Phase 4q's decision (diagnostic only; not binding; not implemented). No additional negative-test diagnostics were performed.

## PBO / deflated Sharpe / CSCV results

```text
PBO (train -> validation, rank-based proxy):     0.000
PBO (train -> OOS,        rank-based proxy):     0.000
PBO (CSCV S=16, C(16,8)=12,870 combinations):    0.500
   (mechanically trivial under widespread zero-trade variants)

Deflated Sharpe (per variant):                   all 0.000
   (because all 32 variants have train trade_count < 2 OR Sharpe = 0;
   skew/kurtosis corrections are inert under zero-variance arrays;
   DSR is methodologically inert under the zero-trade root cause)

Train-best variant by DSR-aware criterion:       id=0 (deterministic
                                                 tie-break: lowest variant id
                                                 among DSR=0 / Sharpe=0 ties).
```

CFP-6 (`PBO > 0.50`) is **not** triggered: the rank-based PBOs are 0.0 (mechanically because train-best across windows is dominated by zero-trade outcomes). CSCV reports 0.500 which is not strictly > 0.50. CFP-6 is reported `false`.

## Regime active-fraction results

Selected `regime_active_fraction_by_symbol_window.csv` rows for representative variants on BTCUSDT:

```text
variant_id  window      total_30m  active_30m  long_active  short_active  active_fraction
0           train       26 208     944         448          496           0.03602
0           validation  17 568     256         168          88            0.01457
0           oos         30 672     624         416          208           0.02034   <-- train-best
1           train       26 208     640         304          336           0.02442
1           validation  17 568     144         88           56            0.00820
1           oos         30 672     376         256          120           0.01226
2           train       26 208     544         240          304           0.02076
2           validation  17 568     168         120          48            0.00956
2           oos         30 672     472         312          160           0.01539
```

The BTC OOS active fraction for the train-best variant (id=0) is **2.03%**, well below the CFP-9 threshold of 5%. **CFP-9 triggers.** Across all 32 variants, no variant exceeds 5% active fraction on any window. The mechanism observation: G1's locked 5-dimension classifier is structurally too narrow under the Phase 4p locked thresholds.

## Trade distribution by month / regime

```text
trade_distribution_by_month_regime.csv: empty (zero OOS HIGH G1 trades for the
                                                train-best variant).
```

CFP-7 (`max_month_fraction > 0.50`) is `false` (no trades, no concentration to assess).

## Catastrophic-floor predicate results

Full table written to `data/research/phase4r/tables/catastrophic_floor_predicates.csv`:

```text
CFP-1   triggered=TRUE   binding driver
        - btc_below_30_count: 32 / 32 variants
        - fraction: 1.0
        - train_best_oos_high_trade_count: 0
CFP-2   triggered=FALSE
        - violator count: 0  (no variant with mean_R <= -0.20R because all
                              G1 means are 0 under zero trades)
CFP-3   triggered=TRUE   subordinate / mechanical
        - violator count: 32  (every variant has profit_factor=0 under
                               empty arrays; max_dd_R=0 is fine, but
                               profit_factor < 0.50 is a mechanical artifact
                               of the zero-trade population)
CFP-4   triggered=TRUE   subordinate / degenerate
        - M3 BTC FAIL AND M4 ETH "trivial PASS" -> CFP-4 fires; in this run
          the trigger is degenerate because both M3 and M4 are computed on
          zero-trade populations.
CFP-5   triggered=FALSE
        - train_mean_R: 0.0
        - oos_mean_R:   0.0
        - condition (train_mean_R > 0 AND oos_mean_R <= 0) is false.
CFP-6   triggered=FALSE
        - pbo_train_validation: 0.000
        - pbo_train_oos:        0.000
        - pbo_cscv:             0.500  (not strictly > 0.50)
CFP-7   triggered=FALSE
        - no OOS HIGH trades; no concentration
CFP-8   triggered=FALSE
        - main_mean_R: 0.0
        - worst sensitivity mean_R: 0.0
        - degradation: 0.0  (sensitivity cells also produce zero trades;
                             degradation is undefined / non-degraded by
                             construction)
CFP-9   triggered=TRUE   independent driver
        - oos_total_30m_bars: 30 672
        - oos_active_30m_bars: 624
        - active_fraction: 0.02034   < 0.05
CFP-10  triggered=FALSE  (audit count = 0; no optional ratio columns read)
CFP-11  triggered=FALSE  (no future-bar use; no signal dependency;
                          signal_outside_active_count = 0)
CFP-12  triggered=FALSE  (audit counts = 0 for all forbidden inputs)
```

**Binding drivers (independent CFPs):** CFP-1 critical (zero trades on the train-best variant on OOS HIGH; 32 / 32 variants below the 30-trade threshold) and CFP-9 (regime-active fraction 2.03% < 5%). CFP-3 and CFP-4 are subordinate / mechanical: CFP-3 fires because profit-factor on empty arrays is zero (Phase 4q-required CFP-3 evaluation rule applied verbatim), and CFP-4 fires because M3 FAIL with a degenerate M4 trivial PASS satisfies the Phase 4q-required predicate verbatim. The verdict driver is **CFP-1 critical**, with CFP-9 as the structural mechanism explanation.

## Required tables produced

All 25 required tables are written under `data/research/phase4r/tables/`:

```text
run_metadata.json                       (top-level)
manifest_references.csv                 (6 manifests; SHA-pinned)
parameter_grid.csv                      (32 variants; 5 axes)
split_boundaries.csv                    (3 windows)
feature_schema.csv                      (12 features)
regime_state_transitions.csv            (per-symbol per-train-best variant)
regime_active_fraction_by_symbol_window.csv  (32 variants × 3 windows × 2 syms = 192 rows)
btc_train_variants.csv                  (96 rows: 32 variants × 3 cost cells)
btc_validation_variants.csv             (96 rows)
btc_oos_variants.csv                    (96 rows)
eth_train_variants.csv                  (96 rows)
eth_validation_variants.csv             (96 rows)
eth_oos_variants.csv                    (96 rows)
btc_train_best_variant.csv              (1 row + columns)
btc_train_best_cost_cells.csv           (9 rows: 3 windows × 3 cost cells)
active_vs_inactive_m1.csv               (M1 detail)
g1_vs_always_active_m2.csv              (M2 detail)
m1_m2_m3_m4_summary.csv                 (4 rows)
cost_sensitivity.csv                    (576 rows: 32 variants × 3 windows × 3 cost cells × 2 syms)
pbo_summary.csv                         (3 rows)
deflated_sharpe_summary.csv             (32 rows)
cscv_rankings.csv                       (12 870 rows × CSCV detail)
trade_distribution_by_month_regime.csv  (0 rows; zero OOS HIGH G1 trades)
catastrophic_floor_predicates.csv       (12 rows)
verdict_declaration.csv                 (verdict + key/value)
forbidden_work_confirmation.csv         (16 audit-zero rows)
```

## Required plots produced

All 11 required plots were attempted but skipped because matplotlib is not installed in the project virtualenv. Plot helpers in the script are guarded with try-import and degrade gracefully (no stop condition). Plot files were not written. The future report (or a follow-up phase if matplotlib is added to the project's optional research dependencies) may produce these plots from the committed local CSV outputs without re-running the backtest. Phase 4q §"Required plots" allows: "If any required plot cannot be produced, future report must state why and whether this affects Verdict D." — Verdict D is not appropriate here because the plot absence is a tooling availability issue, not a methodology / governance / data / implementation stop; verdict-driving evidence (tables, mechanism checks, CFP results) is complete and unaffected.

## Stop-condition audit

No Phase 4q stop condition triggered during the run. Specifically:

- Required manifest missing: not triggered.
- Manifest SHA mismatch: not triggered.
- `research_eligible` mismatch: not triggered (v002 funding manifest convention applied: absence of the field => eligible by inheritance).
- Local data file missing or corrupted: not triggered.
- Forbidden input access (metrics OI / mark-price / aggTrades / spot / cross-venue / 5m diagnostic outputs / non-binding manifest): not triggered (audit counts = 0; static scan = 0 forbidden imports; loaders use explicit-column lists).
- Network I/O / credential read / `.env` read: not triggered.
- Write to `data/raw/` / `data/normalized/` / `data/manifests/`: not triggered (only `data/research/phase4r/` was written).
- Modification of existing `src/` / tests / scripts: not triggered.
- Classifier uses future bars: not triggered.
- Classifier depends on breakout signal: not triggered.
- Signal emitted outside `regime_active`: not triggered (`signal_outside_active_count = 0`).
- Trade emitted despite stop-distance rejection: not triggered.
- Multi-direction emission while regime is single-direction-active: not triggered.
- Timestamp misalignment: not triggered.
- Duplicate `(symbol, interval, open_time)` row: not triggered.
- Partial-bar consumption: not triggered.
- Validation report incomplete: not triggered (all 25 required tables produced).
- ruff fail: not triggered.
- pytest fail or test count regression below 785: not triggered.
- mypy strict fail: not triggered.
- Variant grid expanded beyond 32 or contracted below 32: not triggered (32 variants).
- Variant ordering changes between train / validation / OOS: not triggered (deterministic lexicographic ordering preserved; same variant id used in validation / OOS reporting).
- Non-pinned RNG seed: not triggered (RNG seed = 202604300 pinned).
- Bootstrap impossible due to insufficient sample (Verdict D path): not triggered. Bootstrap was attempted on a 0-element G1 active population and a 124-element inactive population; the implementation returns `(0.0, 0.0, 0.0)` for an empty input array (per the Phase 4q-required "fail-quiet for an empty array" specification implicit in the bootstrap procedure). The methodology gap is not a Verdict-D condition because (a) the *non-empty* baseline populations (inactive: 124 trades; always-active: 124 trades) are reported in full, and (b) the binding driver is CFP-1 quantitative, not a methodology / governance / data / implementation stop.

## Reproducibility evidence

```text
Manifest SHA pinning:                    yes (manifest_references.csv)
Commit SHA pinning at run start:         starting from
                                         e019bee97edb689d5b36d5270bb577de04b2a24a
                                         (main); branch phase-4r/g1-backtest-execution
                                         commits added by Phase 4r.
Deterministic variant ordering:          yes (axis lexicographic; 32 variants)
Pinned RNG seed:                         202604300
Stable sort:                             yes (open_time / funding_time)
Idempotent outputs:                      yes (rerunning the orchestrator
                                         overwrites files identically)
No network:                              confirmed (audit counts = 0)
No credentials:                          confirmed (audit counts = 0)
Exact command line:                      logged in run_metadata.json
Python / numpy versions:                 logged in run_metadata.json
                                         (Python 3.12.4; numpy version per env)
Per-table SHA256:                        not computed in this run for
                                         compactness; can be added in a
                                         follow-up phase if separately
                                         authorized.
```

## Verdict declaration

**Final Verdict: C — G1 framework HARD REJECT.**

**Decision basis:** any single CFP triggered = HARD REJECT (Phase 4q §"Verdict taxonomy"). Multiple CFPs triggered in this run; the binding (independent) driver is **CFP-1 critical** (insufficient trade count: 32 / 32 variants below the 30-trade threshold on OOS BTC HIGH; the train-best variant produced **0 OOS HIGH trades**). **CFP-9** triggers as an independent structural driver (regime-active fraction 2.03% < 5%). **CFP-3** and **CFP-4** are subordinate / mechanical triggers under the zero-trade root cause.

**Mechanism observation (forensic; NOT a parameter-selection input):** Phase 4p's locked composite regime classifier (HTF trend AND DE_4h ≥ E_min AND ATR percentile in band AND relative-volume ≥ V_liq_min AND funding percentile in band) over the five binary axes is structurally too narrow for the chosen 30m Donchian breakout setup on the v002 / Phase 4i datasets across the locked train / validation / OOS windows. Across all 32 variants, the regime-active windows and the breakout-trigger arrival times do not intersect with sufficient frequency to produce a 30-trade OOS HIGH population for any variant. Always-active breakout (no regime gate) on the same setup, stop, target, time-stop, and HIGH cost cell produces 124 trades for the train-best variant with mean_R = −0.34 — confirming the breakout-and-stop machinery itself fires, but the regime gate filters out essentially all candidates.

**G1 first-spec is terminally HARD REJECTED as retained research evidence only.** This is structurally analogous to Phase 4l V2 Verdict C HARD REJECT but at a different mechanism layer: V2 was rejected by the V1-inherited 0.60–1.80 × ATR stop-distance filter; G1 is rejected by the regime-gate-meets-setup intersection sparseness. Phase 4m §"Forbidden rescue observations" applies analogously: no G1 with widened classifier; no G1 with reduced K_confirm; no G1 with relaxed bands; no G1-prime / G1-narrow / G1-extension / G1 hybrid; no Phase 4p amendment based on Phase 4r forensic numbers; no choosing thresholds from Phase 4r forensic active-fraction numbers; no immediate backtest based on observed root cause.

## What this does not authorize

Phase 4r does NOT authorize:

- implementation of G1 inside `src/prometheus/`;
- runtime / execution / persistence / risk / exchange / strategy module modification;
- paper / shadow / live / exchange-write capability;
- production-key creation;
- authenticated APIs / private endpoints / public endpoint clients / user stream / WebSocket / listenKey lifecycle;
- MCP / Graphify / `.mcp.json` / credentials work;
- Phase 4 canonical;
- Phase 4s or any successor phase;
- any G1 rescue (G1-prime / G1-narrow / G1-extension / classifier amendment / K_confirm amendment / band amendment / E_min amendment / breakout-rule amendment / stop-distance bound amendment / N_R amendment / T_stop amendment / position-sizing amendment / Phase 4p G1 strategy-spec amendment / Phase 4q methodology amendment);
- any V2 / F1 / D1-A / R2 rescue;
- any new strategy spec or runnable strategy.

## Forbidden-work confirmation

Phase 4r did NOT do any of the following:

- start Phase 4s or any successor phase;
- implement G1 inside `src/prometheus/`;
- modify runtime / execution / persistence / risk / exchange / strategy code;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`);
- modify `data/raw/` / `data/normalized/` / `data/manifests/`;
- create new manifests;
- create v003;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- run acquisition scripts;
- run diagnostics;
- rerun Q1–Q7;
- acquire mark-price data;
- acquire aggTrades;
- acquire spot data;
- acquire cross-venue data;
- use metrics OI;
- use optional metrics ratio columns;
- use 5m Q1–Q7 findings as regime indicators;
- use V2 Phase 4l stop-distance failure numbers to choose thresholds;
- modify Phase 4p G1 strategy-spec selections;
- modify Phase 4q methodology;
- modify Phase 4j §11 governance;
- modify Phase 4k methodology;
- revise retained verdicts;
- revise project locks, thresholds, parameters, or governance rules;
- change §11.6 / §1.7.3 / Phase 3r governance / Phase 3v governance / Phase 3w governance / Phase 4j governance / Phase 4k methodology;
- start Phase 4 canonical;
- create G1-prime / G1-extension / G1-narrow / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- implement reconciliation;
- implement a real exchange adapter;
- implement exchange-write capability;
- place or cancel orders;
- use / request / store credentials;
- add authenticated REST / private endpoints / public endpoint clients / user stream / WebSocket / listenKey lifecycle;
- enable MCP / Graphify or modify `.mcp.json`;
- create `.env` files;
- deploy anything;
- create paper / shadow runtime;
- imply live-readiness.

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
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price stops
                      (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q
                            : all preserved verbatim
Phase 4r                    : G1 backtest execution; Verdict C HARD REJECT
                              (this phase; new)
Recommended state           : paused
```

## Operator decision menu

**Recommended next step:** Phase 4s — Post-G1 Strategy Research Consolidation Memo (docs-only), analogous to Phase 4m (post-V2) and Phase 3e (post-F1) and Phase 3k (post-D1-A) precedents. Phase 4s would consolidate the G1 outcome into the project's research record, document the four-fold rejection topology now on file (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism-vs-framework mismatch; V2 design-stage incompatibility; **G1 regime-gate-meets-setup intersection sparseness**), preserve forbidden-rescue observations, and either recommend remain-paused or recommend a new fresh-hypothesis discovery memo under the Phase 4m 18-requirement validity gate.

**Alternative — conditional secondary:** remain paused. Acceptable if the operator prefers not to consolidate now.

**NOT recommended:** any G1 rescue (G1-prime / G1-narrow / G1-extension / classifier amendment / K_confirm amendment / band amendment / E_min amendment / breakout-rule amendment / stop-distance bound amendment); any V2 / F1 / D1-A / R2 rescue; immediate G1 implementation; data acquisition; paper / shadow / live; Phase 4 canonical; exchange-write; production keys; authenticated APIs.

**FORBIDDEN:** Phase 4 canonical; paper / shadow / live; exchange-write; production keys; authenticated REST; private endpoints; user stream; WebSocket; MCP; Graphify; `.mcp.json`; credentials; G1-prime / G1-extension based on Phase 4r forensic numbers.

**Phase 4s is NOT authorized by this Phase 4r execution report.** Phase 4s execution would require a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4s                       : NOT authorized
Phase 4 (canonical)            : NOT authorized
Paper / shadow                 : NOT authorized
Live-readiness                 : NOT authorized
Deployment                     : NOT authorized
Production-key creation        : NOT authorized
Authenticated REST             : NOT authorized
Private endpoints              : NOT authorized
User stream / WebSocket        : NOT authorized
Exchange-write capability      : NOT authorized
MCP / Graphify                 : NOT authorized
.mcp.json / credentials        : NOT authorized
G1 implementation              : NOT authorized
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
New family research            : NOT authorized at this boundary; would
                                  require a separately authorized
                                  fresh-hypothesis discovery memo under
                                  the Phase 4m 18-requirement validity
                                  gate.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4s (G1 post-mortem consolidation memo) or remain paused. Until then, the project remains at the post-Phase-4r G1 backtest-execution boundary.

---

**Phase 4r is docs-and-code. The standalone backtest script and three Markdown artefacts (this report, Phase 4r closeout, and a future merge closeout) are the only files added by this branch. Verdict C — G1 framework HARD REJECT is the binding research outcome. G1 first-spec is terminally rejected as retained research evidence only. No project lock changed. No retained verdict revised. Paper/shadow, live-readiness, deployment, production keys, and exchange-write all remain unauthorized.**
