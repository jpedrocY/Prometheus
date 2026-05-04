# Phase 4w — C1 Backtest-Plan Memo

**Authority:** Operator authorization for Phase 4w (Phase 4v §"Operator decision menu" Option A primary recommendation: Phase 4w — C1 Backtest-Plan Memo, docs-only). Phase 4v (C1 strategy spec memo); Phase 4u (C1 hypothesis-spec memo); Phase 4t (post-G1 fresh-hypothesis discovery); Phase 4s (post-G1 strategy research consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery); Phase 4m (post-V2 consolidation; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4f (external strategy research landscape memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/04-data/data-requirements.md`; `docs/04-data/live-data-spec.md`; `docs/04-data/timestamp-policy.md`; `docs/04-data/dataset-versioning.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4w — **C1 Backtest-Plan Memo** (docs-only). Translates the locked Phase 4v C1 strategy spec into a precise, reproducible, fail-closed *future* Phase 4x backtest methodology. Phase 4w predeclares exactly how a future standalone C1 backtest execution would load data, compute C1 features, generate transitions / signals, simulate entries / exits / costs, evaluate the 32-variant grid, compute M1 / M2 / M3 / M4 / M5, compute PBO / deflated Sharpe / CSCV, evaluate CFP-1 through CFP-12, produce required reports / tables / plots, enforce stop conditions, and declare a final Verdict A / B / C / D classification. **Phase 4w does NOT run a backtest, write backtest code, create `scripts/phase4x_c1_backtest.py`, modify scripts, acquire data, modify data, modify manifests, modify `src/prometheus/`, modify tests, create a runnable strategy, start Phase 4x, or authorize paper / shadow / live / exchange-write.** **Phase 4w is text-only.**

**Branch:** `phase-4w/c1-backtest-plan-memo`. **Memo date:** 2026-05-04 UTC.

---

## Summary

Phase 4w is the methodological mirror of Phase 4q applied to C1, narrowed by C1's 32-variant grid (= 2^5 — same cardinality as G1 in Phase 4p / 4q) and broadened by C1's compression-box geometry plus M1 contraction-vs-non-contraction negative-test framework, M2 always-active-same-geometry baseline plus delayed-breakout baseline, opportunity-rate viability floors, and CFP-9 sparse-intersection-collapse / CFP-11 transition-dependency-violation enrichments. Phase 4w predeclares (binding for any future Phase 4x execution): (1) future standalone-script boundary at `scripts/phase4x_c1_backtest.py` (no `prometheus.runtime/execution/persistence` imports; no exchange adapters; no `requests/httpx/aiohttp/websockets/urllib`; no `.env`; no credentials; no Binance API; no network I/O; pure pyarrow + numpy + stdlib); (2) future local output directory `data/research/phase4x/` (gitignored; not committed); (3) exact future command shape covering 2022-01-01..2026-03-31 with train 2022-01-01..2023-06-30 / validation 2023-07-01..2024-06-30 / OOS 2024-07-01..2026-03-31 UTC; `--primary-symbol BTCUSDT`; `--comparison-symbol ETHUSDT`; `--rng-seed 202604300`; (4) data-loading rules with explicit column lists; Phase 4i v001 30m / 4h klines + v002 15m / 1h-derived klines only; manifest SHA pinning; `research_eligible` verification; fail-closed on any mismatch; (5) feature-computation algorithms (compression-box high / low / width over prior `N_comp` bars; rolling-median width over prior `W_width = 240` bars; contraction-state predicate; `contraction_recently_active` window with `L_delay = 1`; close-location ratio; long / short transition predicates; structural stop derived from compression-box invalidation with `S_buffer × box_width`; measured-move target `T_mult × box_width`; positive-R guard; ATR(20) Wilder diagnostic only); (6) signal-generation pseudocode (long-only on `LONG_TRANSITION[t]`; short-only on `SHORT_TRANSITION[t]`; no V2 8-feature AND chain; no R2 pullback-retest; no F1 mean-reversion; no D1-A funding-Z-score; no G1 multi-dimension AND classifier; no 5m features); (7) entry / exit simulation (next-30m-bar-open market entry; fixed initial structural stop; measured-move target; `T_stop_bars = 2 × N_comp`; stop > target > time-stop precedence; same-bar ambiguity = stop-first conservative; no break-even; no trailing); (8) cost / funding model verbatim (LOW = 1 bp / MED = 4 bps / HIGH = 8 bps; taker fee 4 bps; funding excluded from C1 first-spec; §11.6 = 8 bps preserved); (9) position sizing / exposure (0.25% risk; 2× leverage cap; one position max; no pyramiding; no reversal; BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC); (10) **32-variant threshold-grid handling** (5 binary axes — `N_comp` ∈ {8, 12}; `C_width` ∈ {0.45, 0.60}; `B_width` ∈ {0.05, 0.10}; `S_buffer` ∈ {0.10, 0.20}; `T_mult` ∈ {1.5, 2.0}; deterministic lexicographic ordering; no extension; no reduction; no early exit; all 32 variants reported; train-best variant by deflated Sharpe on BTC train MEDIUM; same identifier in validation / OOS / ETH comparison; `W_width`, `L_delay`, close-location, `T_stop_bars`, no HTF gate, no funding input, no volume gate, no metrics OI, no ATR-percentile stop-distance gate all fixed); (11) search-space control (DSR with N = 32; PBO train→validation, train→OOS rank-based; CSCV S = 16 with C(16, 8) = 12 870 combinations; ~412 000 sub-evaluations tractable; **no silent approximation**); (12) M1 contraction-vs-non-contraction (≥ +0.10R; bootstrap 95% CI lower > 0); M2 C1-vs-always-active-same-geometry (≥ +0.05R BTC OOS HIGH; CI lower > 0; AND C1 ≥ delayed-breakout); M3 BTC OOS HIGH `mean_R > 0` AND `trade_count ≥ 30` AND no CFP-1 / 2 / 3 trigger AND opportunity-rate floors satisfied; M4 ETH non-negative differential AND directional consistency; ETH cannot rescue BTC; bootstrap B = 10 000; RNG seed = 202604300; M5 compression-box structural validity diagnostic-only; (13) negative-test framework (non-contraction breakout baseline binding; always-active-same-geometry baseline binding; delayed-breakout baseline binding; active opportunity-rate diagnostic binding; random-contraction baseline diagnostic-only); (14) chronological train / validation / OOS holdout windows reused verbatim from Phase 4k / Phase 4q; (15) BTCUSDT-primary / ETHUSDT-comparison protocol (same 32 variants evaluated independently per symbol; no cross-symbol optimization; no portfolio P&L); (16) 12 catastrophic-floor predicates with C1-specific evaluation rules (CFPs 10 / 11 / 12 are runtime-stop; CFPs 1..9 are post-run verdict predicates; CFP-9 enriched as opportunity-rate / sparse-intersection collapse; CFP-11 enriched as transition-dependency violation; any single CFP triggered = HARD REJECT unless a stop-condition / incomplete-methodology issue makes Verdict D more appropriate); (17) Verdict A (PASS) / B (PARTIAL) / C (HARD REJECT) / D (INCOMPLETE) taxonomy; (18) required reporting tables (32 tables; analogous to Phase 4q's 22-table list, adapted for C1's compression-box / transition framing); (19) required plots (16 plots; analogous to Phase 4q's 9-plot list, adapted for C1); (20) 24-item stop-condition list (manifest mismatch; forbidden-input access; lookahead detection; transition-dependency violation; write attempts; ruff / pytest / mypy fail; etc.); (21) reproducibility requirements (manifest SHA pinning; commit SHA pinning; deterministic variant ordering; pinned RNG seed 202604300; idempotent outputs; no network; no credentials). **Phase 4w recommendation:** Option A — Phase 4x C1 Backtest Execution (docs-and-code standalone research script) primary; Option B — remain paused conditional secondary. **Phase 4w did NOT authorize Phase 4x.** **C1 remains pre-research only:** strategy-spec defined (Phase 4v); backtest-plan methodology defined (this memo); not implemented; not backtested; not validated; not live-ready; **not a rescue of R3 / R2 / F1 / D1-A / V2 / G1**.

## Authority and boundary

- **Authority granted:** create the Phase 4w docs-only backtest-plan memo; create the Phase 4w closeout; predeclare the future Phase 4x standalone-script boundary; predeclare exact data-loading rules; predeclare exact feature-computation algorithms; predeclare exact signal-generation rules; predeclare exact trade-simulation rules; predeclare exact cost / funding model; predeclare exact position-sizing / exposure rules; predeclare exact threshold-grid handling; predeclare exact PBO / DSR / CSCV plan; predeclare exact M1 / M2 / M3 / M4 / M5 implementation plans; predeclare exact CFP-1..CFP-12 evaluation algorithms; predeclare exact Verdict A / B / C / D taxonomy; predeclare exact reporting tables / plots / stop conditions / reproducibility requirements; recommend a future Phase 4x execution phase as conditional primary, or remain-paused as conditional secondary.
- **Authority NOT granted:** run a backtest (forbidden); write backtest code (forbidden); create `scripts/phase4x_c1_backtest.py` (forbidden); write any implementation code (forbidden); modify `src/prometheus/`, tests, or existing scripts (forbidden); acquire / modify / patch / regenerate / replace data (forbidden); modify manifests (forbidden); create v003 (forbidden); create paper / shadow / live path (forbidden); authorize exchange-write (forbidden); authorize Phase 4x or any successor phase (forbidden); authorize production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden); modify any project lock or governance rule (forbidden); revise any retained verdict (forbidden).
- **Hard rule:** Phase 4w is text-only. No code is written. No data is touched. No backtest is run.

## Starting state

```text
Branch (Phase 4w):    phase-4w/c1-backtest-plan-memo
main / origin/main:   7c731d1322ff8ced829a97f0c5a83ef8a7f726c6 (unchanged)
Phase 4v merge:       62290cd9d03550de3577dbc74ba2263ef132e4e2 (merged)
Phase 4v housekeep:   7c731d1322ff8ced829a97f0c5a83ef8a7f726c6 (merged)
Working-tree state:   clean (no tracked modifications); only gitignored
                      transients .claude/scheduled_tasks.lock and
                      data/research/ are untracked and will not be
                      committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Relationship to Phase 4v

- Phase 4v locked the complete C1 strategy spec (timeframes, contraction measure, expansion transition, breakout geometry, stop / target / time-stop / sizing model, opportunity-rate floors, mechanism-check thresholds, CFP thresholds, threshold grid, validation windows, data-requirements decision).
- Phase 4v did NOT authorize backtesting, backtest-plan methodology, implementation, or Phase 4w.
- Phase 4v recommended Phase 4w as conditional primary.
- The operator now explicitly authorized Phase 4w.
- Phase 4w remains docs-only.
- Phase 4w MUST NOT run the C1 backtest, write the C1 script, modify any source / test / script / data / manifest, or authorize Phase 4x.
- Phase 4w MUST honor every Phase 4v locked decision verbatim:
  - signal timeframe = 30m;
  - no HTF gate;
  - no funding input;
  - no volume gate;
  - no metrics OI;
  - no ATR-percentile stop-distance gate;
  - compression-box-based contraction measure;
  - directional close-beyond-compression-box-with-buffer expansion transition;
  - close-location 0.70 long / 0.30 short;
  - structural stop = compression-box invalidation;
  - measured-move target;
  - time-stop = 2 × N_comp 30m bars;
  - 0.25% risk / 2× leverage / one position max preserved verbatim from §1.7.3;
  - §11.6 = 8 bps HIGH per side preserved verbatim;
  - 32-variant grid over five binary axes only;
  - fixed parameters W_width = 240; L_delay = 1; close-location 0.70 / 0.30; T_stop_bars = 2 × N_comp;
  - validation windows reused verbatim from Phase 4k;
  - BTCUSDT primary; ETHUSDT comparison only; ETH cannot rescue BTC;
  - existing data sufficient; no Phase 4w-prerequisite data-requirements memo required; no acquisition required.
- Phase 4w MUST honor the Phase 4u central anti-G1 discipline (no top-level state machine; no multi-dimension AND classifier; no broad regime gate; entry rule fires on the contraction-to-expansion transition itself, not over the duration of the contraction state).
- Phase 4w MUST honor the Phase 4u opportunity-rate viability principle (intrinsic to the theory; predeclared *before* any data is touched; NOT derived from Phase 4r forensic numbers).

## Backtest purpose

The future Phase 4x backtest is a research-only test of:

- whether C1's volatility-contraction expansion hypothesis has evidence after costs, particularly under §11.6 = 8 bps HIGH per side;
- whether transition-tied contraction breakouts outperform non-contraction breakouts (M1);
- whether transition-tied entries outperform an always-active-same-geometry breakout baseline (M2 main);
- whether transition-tied entries outperform a delayed-breakout baseline (M2 timing claim);
- whether C1 preserves adequate opportunity-rate / sample viability (M3 + opportunity-rate floors + CFP-9);
- whether BTCUSDT primary results are directionally supported by ETHUSDT comparison without ETH rescuing BTC (M4 + CFP-4);
- whether C1's catastrophic-floor predicates (CFP-1..CFP-12) all clear (verdict-binding floor).

The future Phase 4x backtest is **NOT**:

- implementation of a runnable trading strategy;
- paper-readiness;
- live-readiness;
- exchange-write authorization;
- production-key authorization;
- a rescue of R3 / R2 / F1 / D1-A / V2 / G1;
- a license to amend Phase 4v / 4u / 4j §11 / 4k governance based on observed forensic numbers;
- a license to extend or reduce the 32-variant grid;
- a license to enable any forbidden input (mark-price; aggTrades; spot; cross-venue; metrics OI; optional ratio columns; 5m diagnostics);
- a license to acquire data;
- a license to revise any retained verdict.

## Backtest non-goals

The future Phase 4x backtest will explicitly NOT do any of the following:

- it will NOT acquire data;
- it will NOT modify data under `data/raw/`, `data/normalized/`, or `data/manifests/`;
- it will NOT create new manifests;
- it will NOT create v003;
- it will NOT modify `src/prometheus/`;
- it will NOT modify tests;
- it will NOT modify existing scripts (`scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- it will NOT run any acquisition or diagnostics or prior-phase backtest script;
- it will NOT use authenticated REST, private endpoints, public endpoints in code, user stream, WebSocket, listenKey, or any network I/O;
- it will NOT read `.env`;
- it will NOT touch credentials;
- it will NOT use mark-price (any timeframe);
- it will NOT use aggTrades;
- it will NOT use spot or cross-venue data;
- it will NOT use metrics OI or optional ratio columns;
- it will NOT use 5m Q1–Q7 diagnostic outputs as features or design inputs;
- it will NOT use Phase 4l V2 forensic stop-distance numbers as design inputs;
- it will NOT use Phase 4r G1 active-fraction / always-active / inactive-pseudo-trade results as thresholds or tuning targets;
- it will NOT extend the 32-variant grid or reduce it below 32;
- it will NOT change variant ordering between train / validation / OOS;
- it will NOT change windows post-hoc;
- it will NOT use future bars or partial bars in strategy decisions;
- it will NOT introduce any new active feature beyond the Phase 4v-locked list;
- it will NOT promote a sensitivity-cell perturbation into an active variant;
- it will NOT silently approximate CSCV, DSR, or PBO;
- it will NOT propose paper / shadow / live / Phase 4 canonical;
- it will NOT amend any project lock, governance rule, or retained verdict.

## C1 strategy-spec recap

```text
Strategy name:                 C1 — Volatility-Contraction Expansion Breakout
Variant cardinality:           exactly 32 (= 2^5)
Five binary axes:
  Axis 1: N_comp     ∈ {8, 12}        (compression-box lookback in 30m bars)
  Axis 2: C_width    ∈ {0.45, 0.60}   (contraction-width threshold vs
                                        rolling-median width)
  Axis 3: B_width    ∈ {0.05, 0.10}   (expansion-trigger buffer as fraction
                                        of compression-box width)
  Axis 4: S_buffer   ∈ {0.10, 0.20}   (stop buffer as fraction of
                                        compression-box width beyond box edge)
  Axis 5: T_mult     ∈ {1.5, 2.0}     (target multiplier of compression-box
                                        width)
Fixed (cardinality 1; not axes):
  W_width                  = 240    (30m bars; rolling-median window)
  L_delay                  = 1      (max delay from contraction end to
                                      breakout trigger, in 30m bars)
  close_location_long      = 0.70   (long requires close in upper 30%
                                      of bar range)
  close_location_short     = 0.30   (short requires close in lower 30%
                                      of bar range)
  T_stop_bars              = 2 × N_comp   (16 if N_comp=8; 24 if N_comp=12;
                                            structurally tied to N_comp;
                                            NOT a separate axis)
  HTF gate                 = NONE
  funding input            = NONE   (excluded from C1 first-spec)
  volume input             = NONE   (reported diagnostically only)
  metrics OI               = NONE   (Phase 4j §11 preserved; not used by C1)
  optional ratio columns   = FORBIDDEN (CFP-10)
  break_even_rule          = disabled
  ema_slope_method         = not_applicable
  stagnation_window_role   = not_active
  stop_trigger_domain (research) = trade_price_backtest
  risk_fraction            = 0.0025
  max_leverage             = 2.0
  max_positions            = 1
  max_active_protective_stops = 1
C1 first-spec does not use:
  funding;
  metrics OI;
  optional metrics ratio columns;
  mark-price (any timeframe);
  aggTrades;
  spot;
  cross-venue;
  order book;
  private / authenticated data;
  user stream / WebSocket / listenKey;
  5m Q1–Q7 diagnostics;
  V2 Phase 4l forensic numbers;
  G1 Phase 4r forensic numbers.
```

## Data inputs and manifest handling

The future Phase 4x must use exactly the following data inputs:

```text
Required (research-eligible per Phase 4i):
  binance_usdm_btcusdt_30m__v001          (74 448 bars; primary signal
                                            timeframe; trade-price klines)
  binance_usdm_ethusdt_30m__v001          (74 448 bars; ETH comparison
                                            signal timeframe)

Optional (reporting-context only; NOT rule inputs):
  binance_usdm_btcusdt_4h__v001           (9 306 bars; 4h reporting context;
                                            NOT a C1 rule input)
  binance_usdm_ethusdt_4h__v001           (9 306 bars; same)
  binance_usdm_btcusdt_15m__v002          (sanity / fallback; NOT rule input)
  binance_usdm_ethusdt_15m__v002          (sanity / fallback; NOT rule input)
  binance_usdm_btcusdt_1h_derived__v002   (1h reporting context only;
                                            NOT a C1 rule input)
  binance_usdm_ethusdt_1h_derived__v002   (same)

Excluded from C1 first-spec rules (NOT loaded by default):
  binance_usdm_btcusdt_funding__v002      (funding excluded from C1
                                            first-spec)
  binance_usdm_ethusdt_funding__v002      (same)
  binance_usdm_btcusdt_metrics__v001      (metrics OI not used; CFP-10 / 12
                                            preserved)
  binance_usdm_ethusdt_metrics__v001      (same)
  Mark-price datasets (any timeframe)     (Phase 3r §8 governance; CFP-12)
  aggTrades                                (CFP-12)
  spot data                                (CFP-12)
  cross-venue data                         (CFP-12)
  Order-book data                          (CFP-12)
```

Manifest handling rules (binding for any future Phase 4x):

```text
1. Read each required manifest from data/manifests/ before any data is loaded.
2. Pin the manifest SHA256 hashes in run_metadata.json:
   {
     "manifest_path": "data/manifests/binance_usdm_btcusdt_30m__v001.manifest.json",
     "manifest_sha256": "<computed-sha256-at-load-time>",
     "research_eligible": true
   }
3. Verify research_eligible flag where the manifest carries the field.
   If the field is absent from a manifest the project has historically
   treated as a canonical research input (e.g. v002 funding manifests
   in earlier phases — though funding is NOT loaded by C1 first-spec),
   document the inheritance and treat as eligible only if explicitly
   noted; otherwise fail closed.
4. Verify per-data-file SHA256 against the manifest where the manifest
   exposes per-file hashes.
5. FAIL CLOSED on any of:
     manifest missing;
     manifest SHA mismatch;
     research_eligible mismatch;
     local data file missing;
     local data file corrupted;
     duplicate (symbol, interval, open_time) row;
     unsorted bars by open_time.
6. NEVER modify a manifest.
7. NEVER create a manifest.
8. NEVER acquire data.
9. NEVER write to data/raw/, data/normalized/, or data/manifests/.
10. NEVER load a non-binding (research_eligible: false) manifest as a
    rule input.
```

## Future script boundary

Predeclared future script path:

```text
scripts/phase4x_c1_backtest.py
```

The future script must:

- be a **standalone research script only**;
- have **no `prometheus.runtime.*` imports**;
- have **no `prometheus.execution.*` imports**;
- have **no `prometheus.persistence.*` imports**;
- have **no exchange adapter imports**;
- have **no `requests`, `httpx`, `aiohttp`, `websocket`, `websockets`, or `urllib`-network usage**;
- **never read `.env`**;
- **never access credentials**;
- **never contact Binance APIs or any external HTTP service**;
- **never write to `data/raw/`, `data/normalized/`, or `data/manifests/`**;
- write output **only to gitignored local research outputs under `data/research/phase4x/`**;
- use **only pyarrow + numpy + stdlib + matplotlib (optional, plot-only)**;
- enforce all C1 strategy-spec rules verbatim;
- enforce all Phase 4w methodology verbatim;
- emit a final Verdict A / B / C / D in `data/research/phase4x/tables/verdict_declaration.csv`.

**Phase 4w MUST NOT create the script.** The script may only be created by a separately authorized Phase 4x.

## Future command shape

Predeclared exact future command shape (Windows; analogous to Phase 4q's command shape):

```bat
.venv\Scripts\python scripts\phase4x_c1_backtest.py ^
  --start 2022-01-01 ^
  --end 2026-03-31 ^
  --train-start 2022-01-01 ^
  --train-end 2023-06-30 ^
  --validation-start 2023-07-01 ^
  --validation-end 2024-06-30 ^
  --oos-start 2024-07-01 ^
  --oos-end 2026-03-31 ^
  --symbols BTCUSDT ETHUSDT ^
  --primary-symbol BTCUSDT ^
  --comparison-symbol ETHUSDT ^
  --output-dir data/research/phase4x ^
  --rng-seed 202604300
```

Equivalent POSIX form:

```bash
.venv/bin/python scripts/phase4x_c1_backtest.py \
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

If a future Phase 4x execution differs from this command shape (e.g., adds a flag, removes a flag, changes a window boundary), it must justify the divergence in the Phase 4x execution report and must not silently differ.

`--rng-seed 202604300` is the same seed used in Phase 4l (V2) and Phase 4r (G1). Phase 4w recommends keeping the seed pinned at 202604300 for cross-phase reproducibility consistency. The operator may choose a fresh seed in the Phase 4x authorization brief; if so, the Phase 4x report must record the seed change rationale.

## Data-loading plan

Loaders for each timeframe must use **explicit column lists** to prevent accidental loading of forbidden columns. The future Phase 4x must implement:

```text
30m kline loader (BTCUSDT, ETHUSDT — Phase 4i v001):
  Required columns:
    open_time         INT64 (UTC milliseconds; canonical bar-identity key)
    open              FLOAT64
    high              FLOAT64
    low               FLOAT64
    close             FLOAT64
    volume            FLOAT64       (diagnostic-only; NOT a rule input)
    close_time        INT64 (UTC milliseconds; close = open_time + 30 min - 1 ms)
  Forbidden:
    no other columns are loaded; metrics OI columns, optional ratio columns,
    mark-price columns, taker buy/sell columns, and number-of-trades columns
    must NOT be requested (CFP-10 / CFP-12).

4h kline loader (BTCUSDT, ETHUSDT — Phase 4i v001):
  Required columns: open_time, open, high, low, close, volume, close_time
  Use:               reporting-context only; NOT a rule input

15m kline loader (BTCUSDT, ETHUSDT — v002):
  Required columns: open_time, open, high, low, close, volume, close_time
  Use:               sanity / fallback only; NOT a rule input

1h kline loader (BTCUSDT, ETHUSDT — v002 1h-derived):
  Required columns: open_time, open, high, low, close, volume, close_time
  Use:               reporting-context only; NOT a rule input

Funding loader:                       NOT INVOKED by Phase 4x (excluded from
                                       first-spec).
Metrics loader:                       NOT INVOKED by Phase 4x (forbidden;
                                       CFP-10 / CFP-12).
Mark-price loader:                    NOT INVOKED by Phase 4x (forbidden;
                                       CFP-12).
aggTrades loader:                     NOT INVOKED by Phase 4x (forbidden;
                                       CFP-12).
Spot / cross-venue loaders:           NOT INVOKED by Phase 4x (forbidden;
                                       CFP-12).
```

Loader behavior contract:

```text
1. Read manifest first; pin SHA256.
2. Read each Parquet file from the canonical local path documented in the
   manifest.
3. Verify file SHA256 against manifest where the manifest exposes per-file
   hashes.
4. Filter columns to the explicit list above.
5. Filter rows by [start, end] UTC ms inclusive.
6. Stable-sort by (symbol, interval, open_time).
7. Verify uniqueness of (symbol, interval, open_time); duplicates = STOP
   condition.
8. Verify timestamp policy:
     bar identity = (symbol, interval, open_time);
     open_time and close_time are integer UTC milliseconds;
     close_time = open_time + interval_ms - 1 ms;
     all timestamps are in UTC.
9. Completed-bar discipline:
     any bar consumed for strategy decisioning at decision_time t' must
     satisfy close_time <= decision_time;
     partial-bar consumption = STOP condition (CFP-11).
10. NEVER use bars with open_time > decision_time (lookahead = CFP-11).
```

## Feature computation plan

The future Phase 4x must implement the following exact feature-computation algorithms. All computations use **prior-completed bars only**.

### A. Compression box (per completed 30m bar t)

```text
compression_box_high[t]    := max(high[t-N_comp], ..., high[t-1])
compression_box_low[t]     := min(low[t-N_comp],  ..., low[t-1])
compression_box_width[t]   := compression_box_high[t] - compression_box_low[t]

Notes:
- The window covers exactly N_comp prior completed bars [t-N_comp .. t-1].
- The current bar t is excluded from the compression-box computation.
- If compression_box_width[t] <= 0, the feature is invalid; do NOT emit a
  signal at bar t. Log the event in compression_box_diagnostics.csv.
- Warmup: any bar t with t - N_comp < 0 (insufficient history) is skipped
  with no signal. The earliest possible compression-box-eligible bar is
  index N_comp.
```

### B. Rolling-median compression-box width (per completed 30m bar t)

```text
rolling_median_width[t]    := median(compression_box_width[t-W_width],
                                      ..., compression_box_width[t-1])

Notes:
- W_width = 240 prior completed 30m bars (~5 trading days).
- If insufficient lookback (t - W_width - N_comp < 0), no signal is emitted.
- If rolling_median_width[t] <= 0 (degenerate), no signal is emitted.
- The earliest possible signal-eligible bar is index N_comp + W_width.
- Median is the standard non-interpolated definition (numpy.median with
  default behavior is acceptable; document the choice in the Phase 4x
  execution report).
```

### C. Contraction-state predicate

```text
contraction_state[t] := (compression_box_width[t]
                        <= C_width × rolling_median_width[t])

Notes:
- Boolean per-bar predicate.
- C_width is from Axis 2 of the threshold grid.
- contraction_state[t] is computed only for bars where both
  compression_box_width and rolling_median_width are valid.
```

### D. Contraction-recently-active window

```text
contraction_recently_active[t] := any(
    contraction_state[k] for k in [t - L_delay, ..., t]
)

Notes:
- L_delay = 1 (fixed). The window is exactly two consecutive bars:
    [t - 1, t].
- If contraction_state[t-1] OR contraction_state[t] is true, then
  contraction_recently_active[t] is true.
- This bounded-delay discipline matches the Phase 4u central anti-G1
  design: the entry rule fires AT the contraction-to-expansion transition
  (within L_delay), not over the duration of the contraction state.
```

### E. Close-location ratio

```text
EPSILON                     := 1e-12 (predeclared tiny positive guard)
range_t                     := high[t] - low[t]

if range_t <= EPSILON:
    close_location_long[t]  := INVALID
    close_location_short[t] := INVALID
    do NOT emit a signal at bar t.
    log in compression_box_diagnostics.csv.
else:
    close_location_long[t]  := (close[t] - low[t]) / range_t
    close_location_short[t] := (high[t] - close[t]) / range_t
                              # equivalently 1 - close_location_long[t];
                              # implementation may use either form, but
                              # must be consistent throughout.

Note:
- Phase 4w specifies the close-location form for SHORT as
  (high[t] - close[t]) / range_t. The SHORT_TRANSITION rule then requires
  close_location_short[t] >= 0.70 instead of close_location_long[t] <= 0.30.
  Both forms are mathematically equivalent because:
    close_location_short[t] = 1 - close_location_long[t]
  Phase 4w accepts either implementation form provided the equivalent
  threshold is used consistently. Phase 4v's strategy-spec text used the
  (close - low) / range form for both long and short; Phase 4x must
  document which form it implements in feature_schema.csv.
- The Phase 4v-locked threshold is "close in upper 30% for long" /
  "close in lower 30% for short". Implementations must enforce this
  semantics regardless of which form is chosen.
```

### F. LONG_TRANSITION predicate

```text
LONG_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] > compression_box_high[t] + B_width × compression_box_width[t]
    AND close_location_long[t] >= 0.70
```

### G. SHORT_TRANSITION predicate

```text
SHORT_TRANSITION[t] :=
    contraction_recently_active[t]
    AND close[t] < compression_box_low[t] - B_width × compression_box_width[t]
    AND close_location_long[t] <= 0.30
       (equivalently: close_location_short[t] >= 0.70 if the high - close
        form is used)
```

### H. Stop and target

```text
For LONG (when LONG_TRANSITION[t] is true at decision time):
  long_stop[t]   := compression_box_low[t]  - S_buffer × compression_box_width[t]
  long_target[t] := entry_price             + T_mult   × compression_box_width[t]
  R_long_per_unit := entry_price - long_stop[t]

For SHORT (when SHORT_TRANSITION[t] is true at decision time):
  short_stop[t]   := compression_box_high[t] + S_buffer × compression_box_width[t]
  short_target[t] := entry_price             - T_mult   × compression_box_width[t]
  R_short_per_unit := short_stop[t] - entry_price

Notes:
- S_buffer is from Axis 4 of the threshold grid.
- T_mult is from Axis 5 of the threshold grid.
- entry_price is the open of the next 30m bar after the signal close
  (see Entry simulation plan).
- R_per_unit must be strictly positive at candidate-generation time.
- Non-positive R rejects the candidate; the rejection is logged in
  the compression-box diagnostics with reason `non_positive_R`.
```

### I. Time-stop

```text
T_stop_bars := 2 × N_comp
            (= 16 if N_comp = 8; = 24 if N_comp = 12)

Notes:
- Structurally tied to N_comp; NOT a separate axis.
- The time-stop fires at the next 30m bar's open after T_stop_bars
  completed 30m bars have elapsed since entry (i.e., on the bar with
  index entry_bar + T_stop_bars + 1).
- See Exit simulation plan for full precedence rules.
```

### J. ATR(20) diagnostic

C1 first-spec has **no ATR-percentile stop-distance gate**. However, Phase 4v's "Stop-distance discipline" section explicitly requires diagnostic `stop_distance_atr` reporting:

> `stop_distance_atr` may be **reported diagnostically** by any future Phase 4w / 4x backtest, but is NOT a binding entry gate in first-spec.

Phase 4w decides: **include ATR(20) Wilder diagnostic computation in Phase 4x**, with the strict rule that `stop_distance_atr` may NOT reject candidates and may NOT influence variant selection or verdict declaration.

```text
ATR(20) Wilder smoothing (per completed 30m bar t):
  TR[t]       := max(high[t] - low[t],
                     abs(high[t]   - close[t-1]),
                     abs(low[t]    - close[t-1]))
  ATR_20[t]   := Wilder-smoothed TR over 20 bars
                 (warmup: SMA(TR, 20) at index 19; thereafter
                  ATR_20[t] = (ATR_20[t-1] * 19 + TR[t]) / 20)

Stop-distance diagnostic (per signal bar t at entry):
  stop_distance_atr[t] := abs(entry_price - stop_price) / ATR_20[t]
                          # uses ATR_20 at the signal-close bar t (NOT at
                          # the entry bar t+1) — this avoids any "future
                          # ATR" lookahead, since the entry bar's ATR
                          # would require the entry bar's TR which uses
                          # entry-bar high / low / close not yet known
                          # at decision time.

Reporting (diagnostic; NOT a gate):
  Stratify trades by stop_distance_atr quintile; report mean_R per
  quintile; report distribution histogram. If the distribution is
  extreme (e.g., median > 5 × ATR or < 0.20 × ATR for the train-best
  variant), Phase 4x MUST flag in the execution report's diagnostics
  section, but MUST NOT self-license a parameter rescue.
```

## Transition and signal generation implementation plan

Predeclared signal-generation pseudocode (the future Phase 4x must implement this verbatim in its main loop):

```text
At each completed 30m bar t (decision time = close_time[t] = open_time[t+1]):

  # 1. Warmup check: require enough lookback for compression-box and
  #    rolling-median computations.
  if t < (N_comp + W_width):
      skip; no signal.

  # 2. Compression box (prior-completed bars only).
  cbh := max(high[t-N_comp..t-1])
  cbl := min(low[t-N_comp..t-1])
  cbw := cbh - cbl
  if cbw <= 0:
      log invalid_compression_box_width; no signal.

  # 3. Rolling-median compression-box width over prior W_width bars.
  rmw := median(compression_box_width[t-W_width..t-1])
  if rmw <= 0:
      log invalid_rolling_median_width; no signal.

  # 4. Contraction-state predicate (local; per-bar).
  contraction_state[t] := (cbw <= C_width × rmw)

  # 5. Recent-contraction window (bounded delay).
  contraction_recently_active[t] :=
      any(contraction_state[k] for k in [t - L_delay, ..., t])
  # With L_delay = 1: contraction_state[t-1] OR contraction_state[t].

  # 6. Close-location ratio.
  range_t := high[t] - low[t]
  if range_t <= EPSILON:
      log invalid_close_location; no signal.
  else:
      cl_long  := (close[t] - low[t]) / range_t
      cl_short := (high[t] - close[t]) / range_t

  # 7. Long-transition predicate.
  long_transition := (
      contraction_recently_active[t]
      AND close[t] > cbh + B_width × cbw
      AND cl_long >= 0.70
  )

  # 8. Short-transition predicate (mirror).
  short_transition := (
      contraction_recently_active[t]
      AND close[t] < cbl - B_width × cbw
      AND cl_short >= 0.70   # equivalently cl_long <= 0.30
  )

  # 9. Defensive degeneracy check.
  if long_transition AND short_transition:
      # Both cannot logically coexist on a normal bar (close cannot be
      # > cbh + B_width × cbw AND < cbl - B_width × cbw simultaneously
      # given cbh >= cbl). If this occurs, treat as invalid data and
      # raise a STOP condition (CFP-11) in the execution.
      raise STOP("degenerate_double_transition")

  # 10. Position state.
  if positioned:
      drop any new transitions; no new candidate. (no pyramiding;
      no reversal while positioned.)

  # 11. Candidate generation (long).
  if long_transition AND not positioned:
      stop_price := cbl - S_buffer × cbw
      entry_price := open[t+1]   # next 30m bar open (lookahead-safe:
                                  # decision_time = close_time[t]; entry
                                  # is on the next bar by construction).
      R_per_unit := entry_price - stop_price
      if R_per_unit <= 0:
          log non_positive_R; reject.
      else:
          target_price := entry_price + T_mult × cbw
          schedule LONG entry at bar t+1 with stop=stop_price,
                                            target=target_price,
                                            T_stop_bars=2 × N_comp.

  # 12. Candidate generation (short, mirror).
  if short_transition AND not positioned:
      stop_price := cbh + S_buffer × cbw
      entry_price := open[t+1]
      R_per_unit := stop_price - entry_price
      if R_per_unit <= 0:
          log non_positive_R; reject.
      else:
          target_price := entry_price - T_mult × cbw
          schedule SHORT entry at bar t+1 with stop, target, T_stop_bars.

  # 13. Hard rules — emit no signal under any of:
  - insufficient lookback;
  - duplicate (symbol, interval, open_time);
  - timestamp-policy violation;
  - bar t is partial (close_time[t] > decision_time);
  - transition fired more than L_delay bars after contraction ended
    (CFP-11);
  - already positioned;
  - R_per_unit <= 0 (degenerate);
  - any forbidden-input access (CFP-10 / CFP-12).
```

The pseudocode above is **prescriptive**. Any future Phase 4x execution must implement it line-for-line. Deviations require a separately authorized methodology amendment.

## Entry simulation plan

```text
Entry timing:
  At the OPEN of the next 30m bar after the confirmed signal close.
  decision_time      = close_time[t]      (signal close)
  entry_bar          = t + 1
  entry_price        = open[entry_bar]    (next 30m bar's open)
Order type:
  Market entry assumption (no limit-order modeling; no slippage-improvement
  modeling beyond the cost-cell slippage applied below).
Intrabar entry:
  FORBIDDEN.
Partial fills:
  FORBIDDEN (modeled as a single fill at entry_price ± slippage at the
  entry bar's open).
One position max:
  ENFORCED (trades are sequential within a symbol; no concurrent positions).
Pyramiding:
  FORBIDDEN.
Reversal in position:
  FORBIDDEN — opposite-direction transitions while positioned are dropped,
  not used to flip the position.
BTCUSDT primary; ETHUSDT comparison only.
No portfolio sizing across symbols.
Edge case — entry_bar missing (e.g., end-of-data):
  If t+1 has no completed 30m bar in the dataset, the signal at t is
  rejected with reason `entry_bar_missing` and the candidate is logged
  in the trade-rejection diagnostics (NOT a STOP unless the gap violates
  the timestamp policy elsewhere).
Edge case — gap between bar t and bar t+1:
  Timestamp policy requires open_time[t+1] = open_time[t] + 30 min.
  A gap (open_time[t+1] > open_time[t] + 30 min) is a STOP condition for
  the entire run (CFP-11 / data-governance), not just the candidate.
```

## Exit simulation plan

```text
At each completed 30m bar t' after entry (entry_bar < t'):

  bars_in_trade := t' - entry_bar

  # Compute touches conservatively (bar high / low extremes).
  if side == LONG:
      stop_touched   := low[t']  <= stop_price
      target_touched := high[t'] >= target_price
  else:  # SHORT
      stop_touched   := high[t'] >= stop_price
      target_touched := low[t']  <= target_price

  time_due := bars_in_trade >= T_stop_bars

  # Stop precedence: stop > target > time-stop.
  if stop_touched AND target_touched:
      # Same-bar ambiguity: stop wins (conservative).
      exit_reason := STOP
      exit_price  := stop_price
  elif stop_touched:
      exit_reason := STOP
      exit_price  := stop_price
  elif target_touched:
      exit_reason := TARGET
      exit_price  := target_price
  elif time_due:
      exit_reason := TIME_STOP
      exit_price  := open[t' + 1]   # exit at next 30m bar's open
                                    # (if t'+1 is unavailable, exit at
                                    #  close[t']; record the variant in
                                    #  diagnostics and document as
                                    #  end-of-data handling).
  else:
      continue holding.

# Apply costs (LOW / MEDIUM / HIGH cells) — see Cost model section.
# No break-even.
# No trailing stop.
# No regime-driven exit (no regime state machine).
# No funding-driven exit (funding excluded).
# No discretionary exit.
# Position lifecycle is independent of subsequent contraction states.
```

The conservative "stop wins on same-bar ambiguity" rule is preserved verbatim from Phase 4v / Phase 4q / Phase 4k. This is the worst-case assumption for the trader; future Phase 4x must NOT implement an optimistic alternative (target wins) without separate operator authorization.

End-of-data handling for time-stop:

```text
If exit_reason == TIME_STOP and bar (t' + 1) is the last bar in the
dataset or beyond the end-of-window boundary:
  - The exit_price defaults to close[t'] (last known price within the
    data window) instead of open[t' + 1].
  - The trade is logged with end_of_data_time_stop = true.
  - No imputation or extrapolation; no synthetic bars.
  - This is a normal end-of-dataset edge case and is NOT a STOP condition.
  - The Phase 4x execution report must record the count of such trades.
```

## Cost model implementation plan

Preserved verbatim from §11.6 / Phase 4k / Phase 4q / Phase 4v:

```text
Cost cells (per side):
  LOW    = 1   bp slippage per side
  MEDIUM = 4   bps slippage per side       (used for train-best variant
                                             selection)
  HIGH   = 8   bps slippage per side       (§11.6 promotion gate;
                                             primary OOS evaluation cell)
Taker fee per side             = 4 bps
Maker rebate                   = NOT used
Live fee model                 = NOT used
Funding cost                   = NOT applied to C1 first-spec trade R
                                  (funding excluded; positions are short
                                   enough that funding-rate impact is
                                   small relative to slippage + fees,
                                   but if Phase 4x chooses to record a
                                   funding-cost diagnostic alongside,
                                   this must be predeclared in
                                   run_metadata.json before any data is
                                   touched and the diagnostic must NOT
                                   alter trade R).

Cost application (per round-trip trade; cost in basis points):
  total_cost_bps_per_side(cell) := cell_slippage + 4   (taker fee)
  cost_factor(cell)             := total_cost_bps_per_side(cell) / 10 000

  LONG entry execution:
    long_entry_executed = entry_price × (1 + cost_factor)
  LONG exit execution:
    long_exit_executed  = exit_price  × (1 - cost_factor)
  SHORT entry execution:
    short_entry_executed = entry_price × (1 - cost_factor)
  SHORT exit execution:
    short_exit_executed  = exit_price  × (1 + cost_factor)

Realized trade R (after costs):
  For LONG:
    raw_pnl = (long_exit_executed - long_entry_executed) × position_size_units
    R_after_costs = raw_pnl / (sizing_equity × risk_fraction)
                   = (long_exit_executed - long_entry_executed)
                     / (long_entry_executed - long_stop)
                   approx. (ignoring cost effect on stop-distance numerator)
    Phase 4x must compute realized R using the executed entry / exit
    prices and the original (pre-cost) stop_price for the R denominator;
    this preserves R as a normalized "stop-distance multiple" measure.

Promotion blocked if HIGH cost fails:
  R2-precedent preserved verbatim. If BTC OOS HIGH mean_R for the
  train-best variant is <= 0, CFP-2 triggers regardless of LOW / MEDIUM
  results.
```

Cost-cell sensitivity reporting:

```text
The Phase 4x report must contain a cost-sensitivity table comparing
mean_R, median_R, profit_factor, sharpe, max_drawdown_R, and trade_count
for the train-best variant across LOW / MEDIUM / HIGH cells on:
  BTC train, BTC validation, BTC OOS;
  ETH train, ETH validation, ETH OOS.
Verdict-driving cell: BTC OOS HIGH (primary).
```

## Position sizing and exposure implementation plan

Preserved verbatim from §1.7.3 / Phase 4v:

```text
Constants:
  sizing_equity                = 100 000 USDT (constant-equity research
                                                 assumption; no compounding;
                                                 R-relative results)
  risk_fraction                = 0.0025         (0.25% per trade)
  max_leverage                 = 2.0            (2× cap)
  max_positions                = 1
  max_active_protective_stops  = 1

Position sizing (per candidate):
  R_per_unit := abs(entry_price - stop_price)
  if R_per_unit <= 0:
      reject candidate (already enforced at signal generation);
      log non_positive_R; do not size.

  position_size_units_uncapped := (sizing_equity × risk_fraction) / R_per_unit

  position_notional_uncapped   := position_size_units_uncapped × entry_price
  max_notional                 := max_leverage × sizing_equity
                                 = 200 000 USDT

  if position_notional_uncapped > max_notional:
      position_size_units      := max_notional / entry_price
      cap_applied              := true
      log leverage_cap_applied with details.
  else:
      position_size_units      := position_size_units_uncapped
      cap_applied              := false

Below-min-notional / lot-size rounding:
  If exchange-metadata snapshot is locally available (Phase 4x is NOT
  required to load exchange metadata; if it does, it must use only locally
  cached snapshots with no network I/O), compute the rounded position size
  using the exchange's lot-size step. If the rounded size is below the
  minimum lot, reject with reason `below_min_lot`. If exchange metadata
  is NOT loaded, Phase 4x must explicitly state in run_metadata.json
  that no live-notional claim is made and continue with the R-based
  research sizing.

BTCUSDT primary; ETHUSDT comparison only.
ETH cannot rescue BTC. CFP-4 enforces this.
No portfolio sizing across symbols.
```

## Threshold-grid handling

```text
Variant cardinality:        exactly 32 (= 2^5)
Variant ordering:           deterministic lexicographic (alphabetical axis
                             names ascending; numerical values within each
                             axis ascending)
Axis order (alphabetical):
  Axis A: B_width    in {0.05, 0.10}
  Axis B: C_width    in {0.45, 0.60}
  Axis C: N_comp     in {8, 12}
  Axis D: S_buffer   in {0.10, 0.20}
  Axis E: T_mult     in {1.5, 2.0}

Variant identifier:
  variant_id ∈ {0, 1, ..., 31}
  variant_id = (
      bit_T_mult * 16 +
      bit_S_buffer * 8 +
      bit_N_comp * 4 +
      bit_C_width * 2 +
      bit_B_width * 1
  )
  where bit_X = 0 for the lower value and 1 for the higher value of axis X.

  Example: variant_id=0 corresponds to
    (B_width=0.05, C_width=0.45, N_comp=8, S_buffer=0.10, T_mult=1.5).
  Example: variant_id=31 corresponds to
    (B_width=0.10, C_width=0.60, N_comp=12, S_buffer=0.20, T_mult=2.0).

  Phase 4x MUST document the exact variant table in
  data/research/phase4x/tables/parameter_grid.csv with columns
  variant_id, B_width, C_width, N_comp, S_buffer, T_mult, T_stop_bars
  (where T_stop_bars = 2 × N_comp is included for clarity but is NOT
  an axis).

Train-best selection (per Phase 4q / 4v):
  cell                = BTC train MEDIUM
  primary criterion   = deflated Sharpe (DSR) on cell trade-R series;
                        higher DSR wins
  tie-break 1         = raw Sharpe (higher wins)
  tie-break 2         = lowest variant_id
  Same train-best variant_id is carried into validation, OOS, and ETH
  comparison.

Grid extension:             FORBIDDEN. Phase 4x must not add a 6th axis,
                             expand any axis to >2 values, or mix-in a
                             sensitivity-cell perturbation as a 33rd
                             active variant.
Grid reduction:             FORBIDDEN. All 32 variants must be evaluated
                             and reported, regardless of early degenerate
                             results.
Early exit on bad variants: FORBIDDEN. No outcome-driven shortcut.
Outcome-driven threshold selection: FORBIDDEN.
Outcome-driven axis-value swap:     FORBIDDEN.
```

## Search-space control

```text
Grid size N                     = 32

Deflated Sharpe (DSR):
  DSR computation per Bailey & López de Prado (2014).
  N = 32 is small enough that DSR is well-defined (N >= 2 required;
  N = 32 yields a small but non-trivial deflation).
  Use skew/kurtosis correction where the trade-R sample size is >= 30;
  otherwise document a fallback (e.g., zero-skew/zero-kurtosis estimate
  with a flag in the deflated_sharpe_summary.csv).
  If the trade_count for a variant is < 30, DSR may be N/A and CFP-1
  may trigger (per Phase 4v opportunity-rate floors).

PBO (Probability of Backtest Overfitting):
  Report PBO for two horizons:
    PBO_train_validation:  rank-based mapping of train Sharpe to validation
                           rank; PBO = fraction of variants in train top
                           half that are in validation bottom half.
    PBO_train_oos:         same logic, train -> OOS.
  Both PBO horizons are computed on the BTC primary symbol with HIGH cost.

CSCV (Combinatorially Symmetric Cross-Validation):
  S = 16 chronological OOS sub-samples drawn from the full (train +
  validation + OOS) period (or from a CSCV-defined re-partition; Phase 4x
  must document the exact partition strategy).
  C(16, 8) = 12 870 train/test sub-sample combinations.
  For each combination, the train-best variant is identified on the
  train half by the same DSR-aware criterion, and its rank on the test
  half is recorded.
  PBO_cscv = fraction of combinations where the train-best variant is
              in the bottom half of test ranks.
  Total sub-evaluations: 32 variants × 12 870 combinations ≈ 411 840;
  with cached per-variant trade tables this is computationally tractable
  (analogous to Phase 4q / 4r).
  No silent approximation of CSCV. If exact CSCV is infeasible due to
  resource constraints, Phase 4x must STOP and emit Verdict D with a
  clear methodology-incomplete failure record.

Outcome-driven sensitivity perturbations:
  Phase 4w specifies CFP-8 perturbation ranges (see CFP-8 below). These
  perturbations are evaluated as DIAGNOSTIC sensitivity cells, NOT as
  new active variants. The 32-variant grid does NOT change.
```

## Chronological validation plan

```text
Train window (~18 months):
  start: 2022-01-01 00:00:00 UTC
  end:   2023-06-30 23:30:00 UTC (inclusive on close_time)
  Typical 30m bar count: ~26 207 bars per symbol.

Validation window (~12 months):
  start: 2023-07-01 00:00:00 UTC
  end:   2024-06-30 23:30:00 UTC (inclusive on close_time)
  Typical 30m bar count: ~17 568 bars per symbol.

OOS holdout window (~21 months):
  start: 2024-07-01 00:00:00 UTC
  end:   2026-03-31 23:30:00 UTC (inclusive on close_time)
  Typical 30m bar count: ~30 672 bars per symbol.
  Primary C1 evidence cell: BTC OOS HIGH.

Rules (binding):
  - No window modification post-hoc.
  - No data shuffling.
  - No leakage (any computation at decision_time t may consume only bars
    with close_time <= decision_time).
  - Same 32 variants evaluated independently per symbol.
  - No cross-symbol optimization.
  - ETH cannot rescue BTC.
  - Train-best variant identified once on BTC train MEDIUM by DSR-aware
    criterion; same variant identifier carried into validation, OOS,
    and ETH comparison.
  - Window boundaries are inclusive on the open_time for the start day's
    first 30m bar (00:00:00 UTC) and inclusive on the close_time for the
    end day's last 30m bar (23:30:00 UTC, with close_time = 23:59:59.999
    UTC).
  - Compression-box and rolling-median features may consume bars from
    immediately before the train start (warmup) provided those bars are
    within the loaded data range; this avoids artificially-zero signals
    at the start of the train window. Phase 4x must document the warmup
    boundary clearly in feature_schema.csv.
```

## BTCUSDT primary / ETHUSDT comparison protocol

```text
Primary symbol:           BTCUSDT
Comparison symbol:        ETHUSDT
ETH cannot rescue BTC:    enforced via CFP-4 (BTC fails M3 AND ETH passes
                           M4 = HARD REJECT regardless).
Per-symbol reporting:     all tables are reported per symbol per window
                           per cost cell per variant.
Train-best:               identified on BTC train MEDIUM; same variant
                           identifier applied to ETH; no separate ETH
                           train-best.
No portfolio sizing:      results are not aggregated across symbols.
No cross-symbol optimization: forbidden.
Same RNG seed:            202604300 is used for any bootstrap on both
                           symbols.
ETH purpose:              cross-symbol robustness evidence (M4); supports
                           BTC promotion only as a non-negative directional
                           consistency check, never as a substitute.
```

## M1 mechanism-check implementation plan

M1 — Contraction-state validity (binding):

```text
Definition:
  C1 transition trades must outperform a non-contraction breakout
  baseline.

Non-contraction baseline:
  Same close-beyond-compression-box-with-buffer rule;
  evaluated on bars where contraction_recently_active[t] is FALSE;
  same stop, target, time-stop, cost cell;
  same one-position-max / no-pyramiding / no-reversal constraints;
  same BTCUSDT primary / ETHUSDT comparison protocol.

Implementation:
  Run a parallel synthetic backtest with the same compression-box
  geometry, same close-beyond-buffer rule, same close-location threshold,
  same stop / target / time-stop, same cost cell, BUT with the
  contraction_recently_active[t] gate INVERTED:
    long_baseline := (
        NOT contraction_recently_active[t]
        AND close[t] > cbh + B_width × cbw
        AND cl_long >= 0.70
    )
    short_baseline := (
        NOT contraction_recently_active[t]
        AND close[t] < cbl - B_width × cbw
        AND cl_short >= 0.70
    )

Pass criteria (BTC OOS HIGH, train-best variant_id):
  C1_mean_R - non_contraction_mean_R >= +0.10R
  AND bootstrap 95% CI lower bound (B = 10 000) > 0.

Bootstrap:
  Bootstrap-by-trade resampling with replacement.
  B = 10 000 resamples.
  RNG seed = 202604300.
  CI = bootstrap percentile interval (2.5%, 97.5%).
  Lower bound > 0 means the differential is statistically separable
  from zero in the positive direction.

Sample-size guardrails:
  If C1_trade_count < 30 OR non_contraction_trade_count < 30:
      M1 FAIL (insufficient sample for bootstrap to be informative).
      CFP-1 may also trigger.
  Report sample sizes for both populations.

Reporting:
  data/research/phase4x/tables/non_contraction_m1.csv with columns:
    symbol, window, cost_cell, variant_id,
    c1_trade_count, c1_mean_R, c1_median_R, c1_total_R,
    non_contraction_trade_count, non_contraction_mean_R,
    differential_mean_R, bootstrap_ci_lower, bootstrap_ci_upper,
    M1_pass.
```

## M2 mechanism-check implementation plan

M2 — Expansion-transition value-add (binding):

```text
Two binding sub-criteria; both must pass for M2 PASS.

Sub-criterion M2.a — C1 vs always-active-same-geometry baseline:
  Always-active baseline:
    Same close-beyond-compression-box-with-buffer rule;
    NO contraction precondition (i.e., contraction_recently_active[t]
    constraint is removed; evaluate on ALL bars);
    same stop, target, time-stop, cost cell;
    same one-position / no-pyramiding / no-reversal constraints.
  Pass: C1_mean_R - always_active_mean_R >= +0.05R on BTC OOS HIGH
        AND bootstrap CI lower (B = 10 000) > 0.

Sub-criterion M2.b — C1 vs delayed-breakout baseline:
  Delayed-breakout baseline:
    Same close-beyond-compression-box-with-buffer rule;
    REQUIRES contraction_state to have been active at some point in the
    past (e.g., t - L_delay - 5 .. t - L_delay - 1, i.e., the contraction
    state was active strictly more than L_delay bars ago and has since
    ended);
    same stop, target, time-stop, cost cell.
  Pass: C1_mean_R - delayed_breakout_mean_R >= 0 on BTC OOS HIGH.

Implementation:
  Two parallel synthetic backtests for the train-best variant_id, mirror
  of the M1 implementation. Use the same fixed parameters as C1 except
  for the contraction-precondition gate.

Sample-size guardrails:
  If always_active_trade_count < 30 OR delayed_breakout_trade_count < 30:
      Report the small-sample state explicitly; M2 may still PASS or
      FAIL depending on bootstrap CI but the report must flag the
      sample-size limitation.

Reporting:
  data/research/phase4x/tables/c1_vs_always_active_m2.csv
  data/research/phase4x/tables/delayed_breakout_m2.csv
  Combined M2 summary in m1_m2_m3_m4_m5_summary.csv.
```

## M3 mechanism-check implementation plan

M3 — Inside-spec co-design validity (binding):

```text
All five sub-criteria must hold for M3 PASS:

  (i)   BTC OOS HIGH train-best variant mean_R > 0;
  (ii)  BTC OOS HIGH train-best variant trade_count >= 30;
  (iii) No CFP-1 / CFP-2 / CFP-3 trigger (CFP details below);
  (iv)  Opportunity-rate floors satisfied:
          - candidate-transition rate (LONG_TRANSITION OR SHORT_TRANSITION
            event count) >= 1 per 480 30m bars on BTC OOS HIGH;
          - BTC OOS HIGH executed trade_count >= 30 for train-best
            variant;
          - >=50% of 32 variants produce BTC OOS HIGH trade_count >= 30;
  (v)   No CFP-9 trigger (sparse-intersection collapse).

Reporting:
  data/research/phase4x/tables/m1_m2_m3_m4_m5_summary.csv
  data/research/phase4x/tables/opportunity_rate_summary.csv with columns:
    symbol, window, cost_cell, variant_id,
    candidate_transition_count, candidate_transition_rate_per_480_bars,
    executed_trade_count, executed_trade_rate_per_480_bars,
    M3_pass.
```

## M4 mechanism-check implementation plan

M4 — Cross-symbol robustness (binding):

```text
Definition:
  ETH OOS HIGH non-negative differential AND directional consistency.

Differential:
  ETH_C1_mean_R - ETH_non_contraction_mean_R >= 0
  (same train-best variant_id used on ETH).

Directional consistency:
  Sign(ETH_C1_mean_R - ETH_baseline_mean_R) == Sign(BTC_C1_mean_R -
                                                   BTC_baseline_mean_R)
  i.e., if BTC C1 outperforms baseline, ETH C1 must also outperform
  baseline (no sign flip).

Sample-size guardrails:
  If ETH_C1_trade_count < 30 OR ETH_baseline_trade_count < 30:
      M4 may degenerate to a "trivial" PASS or FAIL; the trivial-PASS
      case (both sides empty) MUST trigger CFP-4 if BTC fails M3.

ETH cannot rescue BTC:
  CFP-4 triggers if M3 BTC FAILS AND M4 ETH PASSES (regardless of how
  ETH passes — including trivial PASS via empty arrays).
  This rule is binding.

Reporting:
  data/research/phase4x/tables/m1_m2_m3_m4_m5_summary.csv
```

## M5 diagnostic implementation plan

M5 — Compression-box structural validity (DIAGNOSTIC ONLY in first-spec):

```text
Phase 4w decides: include M5 as a DIAGNOSTIC TABLE ONLY in Phase 4x.
M5 is NOT a binding gate. M5 cannot promote or reject a variant. M5
does NOT influence Verdict A / B / C / D.

Definition (diagnostic):
  Compare the C1 stop model (compression-box invalidation:
  stop = compression_box_low - S_buffer × compression_box_width for long;
  mirror for short) against an alternative diagnostic stop model
  (generic ATR-buffered structural stop:
  stop_alt = entry_price - 1.0 × ATR_20 for long; mirror for short).

Diagnostic comparison:
  For the train-best variant on BTC OOS HIGH:
    Replay the trade entries with the alternative stop_alt;
    compute mean_R, median_R, profit_factor, max_drawdown_R for both
    stop models; report side-by-side.

Implementation simplicity boundary:
  If implementing M5 adds non-trivial complexity to the Phase 4x
  execution code, Phase 4x is permitted to skip M5 and report N/A
  in m1_m2_m3_m4_m5_summary.csv with a note explaining the skip.
  Skipping M5 does NOT trigger CFP-1 / 2 / 3 / 6 / 9 and does NOT
  affect the verdict.

Reporting:
  data/research/phase4x/tables/m1_m2_m3_m4_m5_summary.csv (M5 column)
  data/research/phase4x/tables/compression_box_diagnostics.csv
```

## Negative-test implementation plan

Required (binding for Phase 4x):

```text
1. non_contraction_breakout_baseline (M1)
   Same setup, contraction_recently_active GATE INVERTED.
   Reporting: non_contraction_m1.csv

2. always_active_same_geometry_breakout_baseline (M2.a)
   Same setup, contraction_recently_active GATE REMOVED.
   Reporting: c1_vs_always_active_m2.csv

3. delayed_breakout_baseline (M2.b)
   Same setup, contraction_recently_active REPLACED with a strictly
   delayed predicate (contraction was active >L_delay bars ago and has
   since ended; specifically active in [t - L_delay - 5 .. t - L_delay
   - 1] AND not active in [t - L_delay .. t]).
   Reporting: delayed_breakout_m2.csv

4. active_opportunity_rate_diagnostic (M3 + CFP-9)
   Measure candidate-transition rate, executed trade count, by-month
   distributions, by-symbol distributions, by-variant distributions.
   Reporting: opportunity_rate_summary.csv,
              candidate_transition_rate_by_symbol_window_variant.csv,
              transition_distribution_by_month.csv.
```

Optional (diagnostic-only by default; Phase 4w recommends include if low overhead):

```text
5. random_contraction_baseline
   Replace contraction_state[t] with a random Bernoulli with the same
   active-fraction as the real contraction-state series for the train-best
   variant. Use a separate RNG seed derived deterministically from the
   main seed (e.g., seed_random_contraction = 202604300 + 1 = 202604301)
   to avoid coupling with the bootstrap RNG.
   Same setup, stop, target, time-stop, cost.
   Diagnostic only; NOT a promotion gate; NOT a verdict driver.
   Phase 4x may skip random_contraction_baseline if implementation
   overhead is non-trivial; document the skip in
   m1_m2_m3_m4_m5_summary.csv.
```

If non-contraction or always-active baseline performs equally well or better than C1, M1 / M2 fails.
If delayed-breakout outperforms transition-tied, the transition-timing claim fails (M2.b).
If random-contraction performs similarly to real-contraction, the contraction-specificity is weak (diagnostic only).
If opportunity-rate collapses, CFP-9 triggers and M3 fails.

## PBO / deflated Sharpe / CSCV plan

```text
Deflated Sharpe (DSR):
  Per-variant DSR on BTC train MEDIUM trade-R series.
  N = 32 (grid size); skew/kurtosis correction where trade_count >= 30.
  DSR <= 0 for the train-best variant triggers CFP-6.
  DSR distribution across all 32 variants reported in
  deflated_sharpe_summary.csv.

PBO (rank-based):
  PBO_train_validation:
    Rank variants by train HIGH Sharpe (descending) and by validation
    HIGH Sharpe (descending). PBO = fraction of variants in train top
    half (16 variants) that are in validation bottom half (16 variants).
  PBO_train_oos:
    Same logic, train HIGH -> OOS HIGH.
  PBO > 0.50 on either horizon triggers CFP-6.

PBO (CSCV):
  S = 16 chronological OOS sub-samples drawn from the OOS holdout
  period (i.e., the OOS window 2024-07-01..2026-03-31 is partitioned
  into 16 contiguous chronological sub-periods of approximately equal
  length, each ~39 days).
  C(16, 8) = 12 870 train/test sub-sample combinations.
  For each combination:
    "train_half" = 8 sub-samples chosen from the 16; "test_half" = the
                   remaining 8;
    For each variant, compute its Sharpe on the train_half and on the
    test_half;
    Identify the train-best variant by DSR-aware criterion on the
    train_half;
    Record the rank of the train-best variant on the test_half.
  PBO_cscv = fraction of combinations where the train-best variant
              is in the bottom half (rank > 16) of test_half ranks.
  PBO_cscv > 0.50 triggers CFP-6.

Reporting:
  data/research/phase4x/tables/pbo_summary.csv with columns:
    pbo_metric, value, threshold, cfp_triggered.
  data/research/phase4x/tables/deflated_sharpe_summary.csv with columns:
    variant_id, btc_train_med_dsr, btc_train_high_dsr,
    btc_validation_high_dsr, btc_oos_high_dsr,
    eth_oos_high_dsr.
  data/research/phase4x/tables/cscv_rankings.csv with columns:
    combination_id, train_best_variant_id, test_rank, test_sharpe;
    OR cscv_rankings.parquet if size > a Phase 4x-defined threshold.

Compute budget:
  32 variants × 12 870 combinations = 411 840 sub-evaluations.
  With cached per-variant per-sub-sample trade tables, this is tractable.
  No silent approximation.
  If exact CSCV is infeasible, Phase 4x must STOP and emit Verdict D.
```

## Catastrophic-floor predicate implementation plan

The following CFP-1..CFP-12 evaluation algorithms are predeclared verbatim from Phase 4v with C1-specific thresholds. Phase 4x must implement these exactly.

### CFP-1 — Insufficient trade count

```text
Trigger if either:
  (a) BTC train-best variant OOS HIGH trade_count < 30; OR
  (b) more than 50% of the 32 variants have BTC OOS HIGH
      trade_count < 30 (i.e., > 16 variants below 30).

Both conditions are reported separately in
catastrophic_floor_predicates.csv.

Either trigger = CFP-1 ON.
```

### CFP-2 — Negative BTC OOS HIGH expectancy

```text
Trigger if either:
  (a) BTC train-best variant OOS HIGH mean_R <= 0; OR
  (b) any variant flagged for promotion has mean_R <= 0
      (in C1 first-spec, only the train-best variant is a promotion
       candidate, so condition (b) reduces to (a) — but the predicate
       is preserved verbatim from Phase 4v for cross-phase consistency).
```

### CFP-3 — Catastrophic profit-factor / drawdown

```text
Trigger if either:
  (a) BTC train-best variant OOS HIGH profit_factor < 0.50; OR
  (b) BTC train-best variant OOS HIGH max_drawdown_R > 10R.

profit_factor = sum(positive trade R) / abs(sum(negative trade R))
                (NaN if no losing trades; treated as +inf in code; if
                 no winning trades, profit_factor = 0; if both zero,
                 profit_factor = NaN; in all NaN/inf cases, defer
                 to mean_R sign for CFP-2 and skip CFP-3 (a) but
                 still evaluate CFP-3 (b)).

max_drawdown_R = peak-to-trough cumulative-R drawdown in R-units.
```

### CFP-4 — BTC failure with ETH pass

```text
Trigger if M3 BTC FAILS AND M4 ETH PASSES.
ETH cannot rescue BTC, regardless of how ETH passes (including
trivial-PASS via empty arrays — see M4 sample-size guardrails).
```

### CFP-5 — Train-only success / OOS failure

```text
Trigger if BTC train-best variant has:
  train HIGH mean_R > 0
  AND OOS HIGH mean_R <= 0.
```

### CFP-6 — Excessive PBO / DSR failure

```text
Trigger if any of:
  PBO_train_validation > 0.50;
  PBO_train_oos > 0.50;
  PBO_cscv > 0.50;
  train-best DSR <= 0.
```

### CFP-7 — Regime / month overconcentration

```text
Trigger if any single calendar month (UTC) accounts for >50% of total
OOS BTC HIGH trades for the train-best variant.

Reporting: trade_distribution_by_month.csv with per-month counts.
```

### CFP-8 — Sensitivity fragility

```text
Trigger if a small predeclared perturbation around any of the five
structural axes causes:
  >0.20R degradation in OOS HIGH mean_R (vs the train-best variant's
   own OOS HIGH mean_R); OR
  flips mean_R sign (positive -> negative).

Perturbation ranges (predeclared per Phase 4v § Catastrophic-floor
predicates and re-stated here verbatim):
  N_comp:     {6, 10, 14}     (extending {8, 12} by ±2 with 10 in between)
  C_width:    {0.40, 0.65}    (extending {0.45, 0.60} by ±0.05)
  B_width:    {0.025, 0.15}   (extending {0.05, 0.10})
  S_buffer:   {0.05, 0.30}    (extending {0.10, 0.20})
  T_mult:     {1.0, 2.5}      (extending {1.5, 2.0})

Sensitivity-cell evaluation:
  Replay the train-best variant's setup with each axis individually
  perturbed to its CFP-8 range values, holding the other four axes at
  the train-best variant's settings. Each axis perturbation is its own
  diagnostic cell.

  For axis N_comp = 6:  recompute compression-box, rolling-median, and
                        T_stop_bars (which would be 12). All other
                        train-best axes held fixed.
  For axis C_width = 0.40: recompute contraction_state predicate.
  Etc.

  Sensitivity cells are DIAGNOSTIC / CFP-8 checks. They are NOT new
  active variants. They do NOT enter the 32-variant grid. They do NOT
  participate in DSR / PBO / CSCV computation.

Reporting:
  data/research/phase4x/tables/cost_sensitivity.csv may also include
  these axis-sensitivity rows; OR a separate sensitivity_perturbation.csv
  table is acceptable. Phase 4x should choose one and document it in
  the execution report.
```

### CFP-9 — Opportunity-rate / sparse-intersection collapse

```text
Trigger if any of:
  (a) BTC OOS HIGH candidate-transition rate < 1 per 480 30m bars
      (i.e., <64 candidate transitions in the ~30 672-bar OOS window
      for the train-best variant);
  (b) BTC OOS HIGH executed trade_count < 30 for the train-best
      variant (overlaps with CFP-1 (a); CFP-1 binds if so);
  (c) >50% of 32 variants have BTC OOS HIGH trade_count < 30
      (overlaps with CFP-1 (b); CFP-1 binds if so).

Reporting: opportunity_rate_summary.csv
```

### CFP-10 — Forbidden optional ratio access

```text
Trigger if any of these column names is read at any time during the run:
  count_toptrader_long_short_ratio
  sum_toptrader_long_short_ratio
  count_long_short_ratio
  sum_taker_long_short_vol_ratio

Phase 4j §11 governance. Phase 4x must implement a runtime-stop scan
on the column-load path so that any attempted load of these columns
raises immediately and aborts the run.

This is a runtime-stop CFP (Verdict D path), not a post-run verdict
predicate.
```

### CFP-11 — Lookahead / transition-dependency violation

```text
Trigger if any of:
  (a) classifier or signal uses any bar with close_time >
      decision_time (lookahead);
  (b) signal generated without prior contraction precondition
      (contraction_recently_active[t] = false at signal time);
  (c) entry fired more than L_delay bars after contraction state
      ended;
  (d) same-bar AND-chain that consults the breakout-trigger of the
      same evaluation in a lookahead-like way (e.g., looking at
      future bar's close to confirm current bar's transition);
  (e) partial-bar consumption (e.g., evaluating a transition on a
      bar whose close_time > decision_time);
  (f) degenerate double-transition (LONG_TRANSITION AND
      SHORT_TRANSITION simultaneously true on the same bar — see
      Signal generation logic, step 9);
  (g) entry_bar gap (open_time[entry_bar] - open_time[signal_bar]
      != 30 minutes).

This is a runtime-stop CFP (Verdict D path).

Phase 4x must implement defensive assertions in the signal-generation
loop to catch these violations and abort.
```

### CFP-12 — Data governance violation

```text
Trigger if any of:
  - metrics OI is loaded;
  - mark-price (any timeframe) is loaded;
  - aggTrades is loaded;
  - spot or cross-venue data is loaded;
  - non-binding (research_eligible: false) manifest is loaded as a rule
    input;
  - network I/O is attempted (any HTTP / WebSocket / DNS resolution);
  - credentials or .env are read;
  - write attempted to data/raw/, data/normalized/, or data/manifests/;
  - manifest is modified;
  - v003 is created;
  - private / authenticated REST / user-stream / WebSocket / listenKey
    path is touched.

This is a runtime-stop CFP (Verdict D path). Phase 4x must implement
process-level constraints (e.g., refusing to import network libraries,
refusing to open files for writing under data/raw/, etc.) to enforce
this categorically.

Audit counters in forbidden_work_confirmation.csv (see Required
reporting tables) report the runtime evidence:
  metrics_oi_access_count
  optional_ratio_column_access_count
  mark_price_access_count
  aggtrades_access_count
  spot_access_count
  cross_venue_access_count
  network_io_attempts
  credential_reads
  env_file_reads
  data_raw_writes
  data_normalized_writes
  data_manifest_modifications
  v003_creations
  src_prometheus_modifications
  test_modifications
  existing_script_modifications
All must be 0 for a clean run.
```

### CFP precedence and verdict mapping

```text
Runtime-stop CFPs (CFP-10 / CFP-11 / CFP-12):
  - Abort the run immediately on first detection.
  - Emit Verdict D (INCOMPLETE — methodology / governance violation).
  - Verdict D supersedes any partial CFP-1..CFP-9 evaluation.

Post-run verdict CFPs (CFP-1 / CFP-2 / CFP-3 / CFP-4 / CFP-5 / CFP-6 /
                       CFP-7 / CFP-8 / CFP-9):
  - Evaluated after the full 32-variant run completes.
  - Any single trigger = Verdict C HARD REJECT.
  - Multiple triggers reported; the first triggered (lowest-numbered)
    is recorded as the binding driver in verdict_declaration.csv;
    the others are recorded as independent / subordinate / mechanical
    drivers (analogous to Phase 4r's CFP-1 critical / CFP-9 independent
    / CFP-3 mechanical / CFP-4 mechanical recording).

Verdict precedence:
  Runtime-stop CFP triggered      -> Verdict D
  Any post-run CFP triggered      -> Verdict C
  All M1 / M2 / M3 / M4 PASS AND
  no CFP triggered                -> Verdict A
  Some M1..M4 PASS but not all
  AND no CFP triggered            -> Verdict B
```

## Verdict taxonomy

```text
Verdict A — C1 framework PASS:
  M1 PASS AND M2 PASS (both M2.a AND M2.b) AND M3 PASS AND M4 PASS
  AND no CFP-1..CFP-12 triggered
  AND HIGH cost survives (BTC OOS HIGH mean_R > 0).
  Outcome: research-promotable; M3 / M5 evidence retained; NOT
            implementation authorization; NOT live-readiness; further
            phases require separate operator authorization.

Verdict B — C1 framework PARTIAL PASS:
  Some mechanism checks pass (e.g., M1 PASS but M2 FAIL, or M3 PASS but
  M4 FAIL on a non-CFP-4 axis), no CFP-1..CFP-12 triggered.
  Outcome: research evidence only; non-leading; NOT promotable; NOT
            implementation authorization.

Verdict C — C1 framework HARD REJECT:
  Any single CFP-1 / CFP-2 / CFP-3 / CFP-4 / CFP-5 / CFP-6 / CFP-7 /
  CFP-8 / CFP-9 trigger,
  OR all M1 / M2 / M3 / M4 fail.
  Outcome: terminal for C1 first-spec; retained as research evidence
            only; NO C1-prime / C1-narrow / C1-extension / C1 hybrid
            authorized.

Verdict D — C1 framework INCOMPLETE:
  Runtime-stop CFP-10 / CFP-11 / CFP-12 trigger,
  OR methodology / governance / data / implementation stop condition,
  OR invalid results due to bootstrap sample-size collapse,
  OR incomplete report,
  OR impossible required computation (e.g., CSCV cannot complete
     without silent approximation).
  Outcome: re-run after methodology / data / governance fix is required
            before any verdict can be declared. Phase 4x execution must
            emit Verdict D explicitly rather than silently producing
            Verdict A / B / C with degraded methodology.
```

## Required reporting tables

The future Phase 4x must produce the following 32 tables under `data/research/phase4x/tables/` (each as `.csv` unless noted):

```text
Run-level tables:
  1. run_metadata.json
       Run command shape; all argument values; manifest SHAs; commit SHA;
       package versions; Python version; OS; UTC timestamps for run start
       and end; pinned RNG seed; random_contraction subseed if used;
       host name; user (NOT credentials); fail-closed predicate flags.
  2. manifest_references.csv
       manifest_path, manifest_sha256, research_eligible, dataset_name,
       row_count_loaded, columns_loaded, start_open_time_ms,
       end_open_time_ms, data_file_sha256_verified.
  3. parameter_grid.csv
       variant_id, B_width, C_width, N_comp, S_buffer, T_mult,
       T_stop_bars (= 2 × N_comp; informational only).
  4. split_boundaries.csv
       window, start_utc, end_utc, start_open_time_ms, end_open_time_ms,
       expected_30m_bar_count, observed_30m_bar_count.
  5. feature_schema.csv
       feature_name, definition, prior_completed_only, source_columns,
       window, axis_id (if axis), fixed_value (if fixed),
       close_location_form_used.
  6. signal_schema.csv
       signal_name, definition_pseudocode, dependencies, transition_form,
       defensive_assertions.

Compression / transition tables:
  7. compression_state_summary.csv
       symbol, window, variant_id, total_bars, contraction_state_count,
       contraction_state_fraction, contraction_recently_active_count,
       contraction_recently_active_fraction.
  8. compression_box_diagnostics.csv
       symbol, decision_time_utc, variant_id, reason_code, count.
  9. candidate_transition_rate_by_symbol_window_variant.csv
       symbol, window, cost_cell, variant_id,
       long_transition_count, short_transition_count, total_transition_count,
       window_bar_count, transition_rate_per_480_bars.
 10. transition_distribution_by_month.csv
       symbol, window, variant_id, year_month_utc, transition_count.

Variant-level result tables:
 11. btc_train_variants.csv
       variant_id, cost_cell, trade_count, mean_R, median_R, total_R,
       std_R, sharpe, profit_factor, max_drawdown_R,
       leverage_cap_applied_count, end_of_data_time_stop_count.
 12. btc_validation_variants.csv (same columns)
 13. btc_oos_variants.csv (same columns)
 14. eth_train_variants.csv (same columns)
 15. eth_validation_variants.csv (same columns)
 16. eth_oos_variants.csv (same columns)

Train-best variant tables:
 17. btc_train_best_variant.csv
       variant_id, B_width, C_width, N_comp, S_buffer, T_mult,
       train_med_dsr, train_med_sharpe, train_high_sharpe,
       selection_criterion_summary.
 18. btc_train_best_cost_cells.csv
       cost_cell, mean_R, median_R, total_R, sharpe, profit_factor,
       trade_count, max_drawdown_R.

Mechanism-check tables:
 19. non_contraction_m1.csv (per the M1 implementation plan)
 20. c1_vs_always_active_m2.csv (per the M2.a implementation plan)
 21. delayed_breakout_m2.csv (per the M2.b implementation plan)
 22. m1_m2_m3_m4_m5_summary.csv
       symbol, window, cost_cell, variant_id,
       M1_pass, M2a_pass, M2b_pass, M2_pass, M3_pass, M4_pass,
       M5_diagnostic_summary, overall_M_pass.

Opportunity-rate / sensitivity tables:
 23. opportunity_rate_summary.csv (per the M3 implementation plan)
 24. cost_sensitivity.csv
       cost_cell, mean_R, median_R, profit_factor, sharpe,
       max_drawdown_R, trade_count, applied_to_window.

Search-space control tables:
 25. pbo_summary.csv (per PBO plan)
 26. deflated_sharpe_summary.csv (per DSR plan)
 27. cscv_rankings.csv (or .parquet if size-bound; per CSCV plan)

Distribution / diagnostic tables:
 28. trade_distribution_by_month.csv
       symbol, window, cost_cell, variant_id, year_month_utc,
       trade_count, mean_R, total_R.
 29. stop_distance_atr_diagnostics.csv
       symbol, window, cost_cell, variant_id, trade_id,
       stop_distance_atr, R_at_exit, exit_reason.
       (Diagnostic only; NOT a gate.)
 30. compression_box_diagnostics.csv (already listed at #8 — combined)

Verdict tables:
 31. catastrophic_floor_predicates.csv
       cfp_id, name, value_or_metric, threshold, triggered,
       binding_driver_flag, evaluation_window, evaluation_cost_cell,
       notes.
 32. verdict_declaration.csv
       final_verdict (A | B | C | D),
       binding_driver_cfp_or_M (if any),
       independent_drivers,
       subordinate_drivers,
       summary_text,
       run_complete_utc.

Forbidden-work confirmation:
  forbidden_work_confirmation.csv
       audit_field, observed_count, expected_count (always 0).
       (See CFP-12 audit counters list.)
```

If a table cannot be produced for a substantive methodology reason (e.g., M5 diagnostic skipped), Phase 4x must record this explicitly in the execution report and emit either Verdict D (if the missing table is binding) or annotate the absence (if M5-style optional). Tables 1, 2, 3, 4, 5, 6, 11..18, 22, 25, 26, 27, 31, 32 are binding; absence of any of them = Verdict D.

## Required plots

The future Phase 4x should produce the following 16 plots under `data/research/phase4x/plots/` (PNG, with matplotlib; if matplotlib is unavailable, plots may be skipped without affecting verdict, but the absence must be documented):

```text
Cumulative-R curves:
  1. cumulative_R_BTC_train_validation_oos.png
       Train-best variant; per cost-cell line.
  2. cumulative_R_ETH_train_validation_oos.png
       Same train-best variant_id; ETH; per cost-cell line.

Compression / transition timelines:
  3. compression_transition_timeline_BTC.png
       OOS window; binary contraction_state strip + binary
       contraction_recently_active strip + transition-event scatter.
  4. compression_transition_timeline_ETH.png (same for ETH)

C1 vs baselines:
  5. c1_vs_non_contraction_R_distribution.png
       Histogram or violin plot of per-trade R for C1 and non-contraction
       baseline on BTC OOS HIGH train-best variant.
  6. c1_vs_always_active_mean_R.png
       Bar chart comparing mean_R for C1 vs always-active baseline
       across cost cells.
  7. delayed_breakout_comparison.png
       Bar chart for transition-tied vs delayed-breakout baseline.

Opportunity-rate / candidates:
  8. opportunity_rate_by_month_BTC.png
       Monthly candidate-transition count + executed trade count.
  9. candidate_transition_rate_by_variant.png
       32-variant bar chart of candidate-transition rate per 480 bars
       on BTC OOS HIGH.

Search-space control:
 10. dsr_distribution.png
       Distribution histogram of DSR across 32 variants on BTC train MED.
 11. pbo_rank_distribution.png
       Distribution of train-best ranks on test-half across CSCV
       combinations.

Drawdown / monthly cumulative R:
 12. btc_oos_drawdown.png
       Train-best variant; BTC OOS HIGH; drawdown-R curve over time.
 13. monthly_cumulative_R_BTC_oos.png
       Monthly cumulative-R bars for BTC OOS HIGH train-best variant.

Trade-R distribution:
 14. trade_R_distribution.png
       Histogram of per-trade R; per-cost-cell overlay.

Diagnostic distributions:
 15. stop_distance_atr_distribution.png
       Histogram / boxplot of stop_distance_atr at entry across all
       BTC OOS HIGH C1 trades for the train-best variant.
 16. compression_box_width_distribution.png
       Histogram of compression_box_width and rolling_median_width
       on BTC OOS HIGH for the train-best variant.
```

If any plot cannot be produced (e.g., matplotlib unavailable; same as Phase 4r's experience), the future Phase 4x execution report must state why and confirm whether this affects the verdict. Plot absence does NOT automatically cause Verdict D, provided all 32 binding tables are produced.

## Stop conditions

The future Phase 4x must immediately STOP and produce a failure report (Verdict D) if any of the following occurs:

```text
Manifest / data:
  - required manifest missing;
  - manifest SHA mismatch;
  - research_eligible mismatch (where applicable);
  - local data file missing;
  - local data corrupted;
  - non-binding manifest loaded as a rule input.

Forbidden inputs (CFP-10 / CFP-12):
  - metrics OI loaded;
  - optional ratio column accessed;
  - mark-price loaded (any timeframe);
  - aggTrades loaded;
  - spot / cross-venue loaded;
  - 5m diagnostic outputs loaded as features;
  - non-binding manifest loaded.

Forbidden behavior (CFP-11 / CFP-12):
  - private / authenticated / API / WebSocket / network path touched;
  - credential read or store attempted;
  - .env read attempted;
  - write attempted to data/raw/, data/normalized/, or data/manifests/;
  - modification of existing src/prometheus/ files;
  - modification of existing tests;
  - modification of existing scripts.

Lookahead / transition-dependency violations (CFP-11):
  - future bar consumed (close_time > decision_time);
  - partial bar consumed in a strategy decision;
  - signal emitted without contraction_recently_active being true;
  - entry fired beyond L_delay bars after contraction ended;
  - same-bar AND-chain that consults a future-bar's value;
  - degenerate double-transition (LONG and SHORT both true on same bar).

Data integrity:
  - timestamp misalignment;
  - duplicate (symbol, interval, open_time) row;
  - bar gap (open_time[entry_bar] - open_time[signal_bar] != 30 minutes);
  - trade emitted despite R <= 0.

Methodology:
  - validation report incomplete;
  - variant grid expanded beyond 32 or contracted below 32;
  - variant ordering changes between train / validation / OOS;
  - RNG seed not pinned;
  - bootstrap impossible due to insufficient sample where Phase 4w
    requires Verdict D (e.g., M1 / M2 sample-size collapse with no
    informative bootstrap CI);
  - CSCV silently approximated (e.g., S < 16 or fewer than 12 870
    combinations evaluated without explicit Verdict D declaration).

Quality gates (these must be checked before merge of Phase 4x; they are
not strictly runtime-stops for the backtest itself, but Phase 4x is
expected to ensure they pass before reporting):
  - ruff check . fails;
  - pytest fails or test count regresses below 785;
  - mypy strict fails.
```

## Reproducibility requirements

```text
Manifest SHA pinning:
  Each loaded manifest's SHA256 hash is recorded in run_metadata.json
  at run start; any subsequent re-run that observes a different SHA
  fails closed with a clear "manifest_sha_mismatch" error.

Commit SHA pinning:
  The current git HEAD commit SHA is recorded in run_metadata.json.
  Re-runs from a different commit are permitted but the new SHA is
  recorded.

Deterministic variant ordering:
  Variant ordering is deterministic per the lexicographic rule above.
  variant_id 0..31 maps to the same parameter-tuple across all runs.

Pinned RNG seed:
  --rng-seed 202604300 (recommended; same as Phase 4l / 4r).
  All bootstraps (M1, M2.a, M2.b, etc.) use deterministic RNG seeded
  from this seed (per-bootstrap seeds may be derived deterministically
  to avoid coupling, e.g., main_seed for general bootstrap;
  main_seed + 1 for random_contraction subseed if used).

Stable sorting:
  All bar arrays, trade arrays, and table outputs are stable-sorted
  by (symbol, interval, open_time) or (symbol, window, variant_id,
  trade_open_time) as appropriate.

Idempotent outputs:
  Re-running with the same inputs (same manifests, same windows, same
  command, same seed) produces byte-identical CSV outputs (modulo
  per-row floating-point precision, which Phase 4x must standardize
  e.g., to 6 decimal places for human-readable mean_R columns).

No network:
  The script must not make any network call. Phase 4x may verify by
  importing only allowed packages and running a network-disabled
  test (or by static-scan in CI; Phase 4w does not require this but
  recommends it).

No credentials:
  No credential read; no .env read; no API keys; no signed payloads.

Environment reporting:
  run_metadata.json includes: Python version (e.g., 3.11.x), OS,
  pyarrow version, numpy version, matplotlib version (if used).

Table-content hashing (recommended):
  For each binding table, Phase 4x may compute and record a SHA256 of
  the canonical CSV bytes in run_metadata.json under
  "table_sha256_map". This supports cross-run identity verification.
```

## What future Phase 4x may create

If a separately authorized Phase 4x execution is approved, it may create:

```text
- scripts/phase4x_c1_backtest.py
  (standalone research script per the future-script-boundary rules
   above; new file; no modifications to existing scripts)

- docs/00-meta/implementation-reports/2026-04-30_phase-4x_c1-backtest-execution.md
  (the Phase 4x execution report; new file)

- docs/00-meta/implementation-reports/2026-04-30_phase-4x_closeout.md
  (the Phase 4x closeout artefact; new file)

- local gitignored outputs under data/research/phase4x/
  (tables/ and plots/; not committed; reproducible from the script
   with pinned RNG seed)
```

Future Phase 4x must NOT:

- modify `src/prometheus/`;
- modify tests unless separately justified by an explicit Phase 4x
  authorization-brief clause (Phase 4w recommends NO test changes);
- modify existing scripts (`scripts/phase3q_5m_acquisition.py`,
  `scripts/phase3s_5m_diagnostics.py`,
  `scripts/phase4i_v2_acquisition.py`,
  `scripts/phase4l_v2_backtest.py`,
  `scripts/phase4r_g1_backtest.py`);
- modify `data/raw/`, `data/normalized/`, or `data/manifests/`;
- create new manifests;
- create v003;
- acquire data;
- create paper / shadow / live runtime;
- imply live readiness;
- authorize Phase 4 canonical, paper / shadow, exchange-write, production
  keys, authenticated APIs, private endpoints, user stream, WebSocket,
  MCP, Graphify, `.mcp.json`, or credentials work.

## What this does not authorize

Phase 4w does NOT authorize:

- Phase 4x execution (must be separately authorized);
- a backtest run;
- writing of code;
- creation of `scripts/phase4x_c1_backtest.py` or any other script;
- creation of a runnable strategy;
- modification of `src/prometheus/`, tests, or existing scripts;
- modification of `data/raw/`, `data/normalized/`, or `data/manifests/`;
- creation of new manifests or v003;
- data acquisition;
- paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- start of Phase 4 canonical;
- amendment of any project lock (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- amendment of any governance rule (Phase 3r / 3v / 3w / 4j §11 / 4k);
- amendment of any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0);
- amendment of the Phase 4v C1 strategy spec;
- amendment of the Phase 4u C1 hypothesis spec;
- creation of C1-prime / C1-narrow / C1-extension / C1 hybrid;
- creation of G1-prime / G1-narrow / G1-extension / G1 hybrid;
- creation of V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- creation of F1 / D1-A / R2 rescue;
- proposal of a 5m strategy / hybrid / variant.

## Forbidden-work confirmation

Phase 4w did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`);
- run `scripts/phase4r_g1_backtest.py`;
- run `scripts/phase4l_v2_backtest.py`;
- run `scripts/phase4i_v2_acquisition.py`;
- run `scripts/phase3q_5m_acquisition.py`;
- run `scripts/phase3s_5m_diagnostics.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- revise any retained verdict (R3 / R2 / R1a / R1b-narrow / F1 / D1-A / V2 / G1 / H0);
- change any project lock;
- create a runnable strategy;
- create V3 / H2 / G2 / any runnable candidate name beyond C1's (already-defined) hypothesis-spec / strategy-spec layers;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- propose a 5m strategy / hybrid / variant;
- start Phase 4x / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
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
                       binding driver; CFP-9 independent driver;
                       terminal for G1 first-spec)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
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
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v
                            : all preserved verbatim
Phase 4w                    : C1 backtest-plan memo (this phase; new; docs-only)
C1                          : pre-research only;
                              hypothesis-spec defined in Phase 4u;
                              strategy-spec defined in Phase 4v;
                              backtest-plan methodology defined in
                              Phase 4w (this memo);
                              not implemented; not backtested; not validated;
                              not live-ready;
                              not a rescue of R3 / R2 / F1 / D1-A / V2 / G1
Recommended state           : Phase 4x conditional primary;
                              remain-paused conditional secondary
```

## Operator decision menu

- **Option A — primary recommendation:** Phase 4x — C1 Backtest Execution (docs-and-code; standalone research script). Phase 4x would create `scripts/phase4x_c1_backtest.py` exactly under the Phase 4w methodology, run the predeclared 32-variant C1 backtest on BTCUSDT primary / ETHUSDT comparison across LOW / MEDIUM / HIGH cost cells over the train / validation / OOS windows, evaluate M1 / M2 / M3 / M4 / M5, compute PBO / DSR / CSCV, evaluate CFP-1..CFP-12, and emit Verdict A / B / C / D. Phase 4x must NOT modify `src/prometheus/`, tests, or existing scripts; must NOT acquire data; must NOT create runtime / paper / shadow / live capability.
- **Option B — conditional secondary:** remain paused.

NOT recommended:

- immediate C1 implementation in `src/prometheus/` — REJECTED;
- data acquisition — REJECTED (Phase 4v already determined existing data is sufficient);
- paper / shadow / live-readiness — FORBIDDEN;
- Phase 4 canonical — FORBIDDEN;
- production-key creation / authenticated APIs / private endpoints / user stream / WebSocket — FORBIDDEN;
- MCP / Graphify / `.mcp.json` / credentials — FORBIDDEN;
- exchange-write capability — FORBIDDEN;
- any G1 / V2 / R2 / F1 / D1-A rescue — FORBIDDEN;
- any C1-prime / C1-narrow / C1-extension / C1 hybrid — FORBIDDEN.

**Phase 4x is NOT authorized by this Phase 4w memo.** Phase 4x execution requires a separate explicit operator authorization brief.

## Next authorization status

```text
Phase 4x                       : NOT authorized
Phase 4y                       : NOT authorized
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
C1 implementation              : NOT authorized
C1 backtest execution          : NOT authorized
C1 data acquisition            : NOT authorized (none required;
                                  Phase 4v determined existing data
                                  sufficient)
G1 / V2 / R2 / F1 / D1-A rescue: NOT authorized; not proposed
G1-prime / G1-extension axes   : NOT authorized; not proposed
G1-narrow / G1 hybrid          : NOT authorized; not proposed
V2-prime / V2-variant          : NOT authorized; not proposed
C1-prime / C1-extension        : NOT authorized; not proposed
Retained-evidence rescue       : NOT authorized; not proposed
5m strategy / hybrid           : NOT authorized; not proposed
ML feasibility                 : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                               : NOT authorized; data unavailable.
```

The next step is operator-driven: the operator decides whether to authorize Phase 4x (C1 Backtest Execution, docs-and-code) or remain paused. Until then, the project remains at the post-Phase-4w backtest-plan boundary.

---

**Phase 4w was docs-only. No source code, tests, scripts, data, manifests, or successor phases were created or modified. Recommended state: Phase 4x conditional primary; remain-paused conditional secondary. No next phase authorized.**
