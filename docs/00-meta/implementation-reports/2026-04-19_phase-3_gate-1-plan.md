# Phase 3 — Gate 1 Plan: Backtesting and Strategy Conformance

**Date:** 2026-04-19
**Phase:** 3 — Backtesting and Strategy Conformance
**Current branch:** `main` at `4a35887` (Merge PR #4, Phase 2c landed)
**Proposed branch:** `phase-3/backtest-strategy-conformance` (off `main`, **not created yet — awaiting Gate 1 approval**)
**Author:** Claude Code, on behalf of operator
**Status:** GATE 1 PLAN — research/backtest only. No implementation has started. No branch created. No files edited. No dependencies installed. No network activity. No credentials. No exchange-write.

---

## 0. Executive Summary

Phase 3 plans the **v1 breakout strategy implementation** and a **research-only historical backtester** that consumes the Phase 2 / 2b / 2c data foundation and produces reviewable trade logs, equity curves, drawdown series, R-multiple distributions, and validation-checklist conformance evidence.

**What Phase 3 delivers (scope):**

1. A pure, dependency-free **strategy calculation module** (`src/prometheus/strategy/v1_breakout/`) that encodes the locked v1 breakout logic — 1h EMA trend bias, 8-bar consolidation detection, breakout triggers, structural stop, staged trade management — and returns typed intents (`EntryIntent`, `StopUpdateIntent`, `ExitIntent`) without touching persistence, runtime state, or exchange-adjacent code.
2. A **research backtest engine** (`src/prometheus/research/backtest/`) that drives the strategy bar-by-bar against historical data, simulates fills under documented assumptions (next-bar-open baseline, slippage buckets, taker commission, funding accrual), and records trade outcomes.
3. A **reporting layer** that emits trade logs, equity curves, drawdown metrics, and a `BacktestReportManifest` citing the exact dataset manifest versions consumed, for reproducibility.
4. **~120–150 new tests** across strategy conformance, no-lookahead invariants, fill/stop/funding mechanics, rounding-against-exchangeInfo, and end-to-end smoke runs on synthetic + real 2026-03 data.
5. A **Gate 2 review report** and a **Phase 3 checkpoint report** in `docs/00-meta/implementation-reports/`.

**What Phase 3 does NOT deliver (explicit non-goals):** no live trading; no exchange adapter; no credentials; no `.env`; no order placement; no REST/WebSocket calls; no authenticated Binance endpoints; no data downloads; no `.mcp.json`; no Graphify; no dashboard; no Phase 4 runtime state / kill switch / persistence / SAFE_MODE; no walk-forward statistical conclusions beyond what 2026-03 data can demonstrably support.

**Critical Gate 1 decisions requested from operator:** 7 strategy/backtest ambiguities (§11.A), 4 risk-framework decisions (§11.B), 2 data-contract clarifications (§11.C), and 1 data-sufficiency question (§11.D — propose **Phase 2e** as a separate operator-approved wider-backfill task for walk-forward validation). All are surfaced explicitly — none are resolved silently.

**Plain-English statement of purpose:** after Phase 3, we will be able to answer the question *"does the v1 breakout strategy, as specified, produce correct signals and trade outcomes on real BTCUSDT 2026-03 data, measured against documented fill/cost assumptions?"* — but not yet the question *"is this strategy profitable enough to promote."* The second question requires multi-year data (Phase 2e) and walk-forward discipline (out-of-Phase-3 work).

---

## 1. Plain-English Explanation of Phase 3

**The problem Phase 3 solves.** Phase 2 + 2b + 2c gave us a clean, version-controlled, integrity-checked historical dataset for BTCUSDT and ETHUSDT 2026-03: 15m OHLCV klines, derived 1h bars, 15m mark-price klines, funding events, and an exchangeInfo snapshot. Phase 3 is the first phase where that data is *used* — specifically, to simulate the locked v1 breakout strategy on historical candles and verify that its signal, entry, stop, management, exit, and cost behavior matches the specification.

**What "strategy conformance" means.** It does **not** mean "the strategy is profitable." It means: if you hand-check a signal on a known sequence of bars, the engine produces the same signal the spec says it should. If you move time forward one bar, the no-lookahead tests prove that no future bar leaked into the decision. If the 1h EMA bias uses only completed 1h bars — never a forming one — there is a test that asserts it. If a stop is placed, it respects `tickSize`. If a position is held across a funding event, the funding cost is applied with the correct sign. These are objectively testable properties.

**What the backtest engine is, and isn't.** The engine is a pure Python, deterministic simulator that walks bar-by-bar through a historical window, calls strategy logic on each completed bar, and produces trade records. It is **not** a runtime, it is **not** stateful across invocations, it does **not** persist anything except report files, and it does **not** reach out to any exchange or network. Running it twice on the same inputs produces byte-identical outputs.

**Why execution-related behavior is out of scope here.** Phase 4 will own stateful runtime concerns (SAFE_MODE, kill switch, reconciliation states, persistence of in-flight trades). Phase 6 will own fake-exchange dry-run mechanics (order submission lifecycle, ACK handling, user-stream events, cancel-and-replace). Phase 3 simulates the **strategy/risk math** in isolation against historical data — nothing more. This keeps the blast radius small and the tests focused.

**Why the Phase 2 data foundation maps cleanly into Phase 3.** The data layer already enforces UTC-ms timestamps, strict bar identity, `close_time = open_time + interval_ms - 1`, 1h alignment against four exact 15m bars, and invalid-window explicit handling. The backtester inherits those invariants for free — it just needs to implement the *point-in-time gating rule* (a bar is "visible" to the strategy only when the simulation clock has advanced past its close time).

---

## 2. Current Branch / Status Verification Commands

Run before branch creation (§3) to confirm starting state. None of these have side effects.

```bash
git -C c:/Prometheus rev-parse --abbrev-ref HEAD
# expected: main

git -C c:/Prometheus status --short
# expected: (empty — clean)

git -C c:/Prometheus log --oneline -5
# expected top line: 4a35887 Merge pull request #4 from jpedrocY/phase-2c/...

git -C c:/Prometheus rev-list --left-right --count HEAD...@{u}
# expected: 0  0  (local main up to date with origin/main)

uv --version       # expected: uv 0.11.7
python --version   # expected: Python 3.12.4
```

**Abort gate.** If the branch is not `main`, if the working tree is not clean, if we are ahead/behind origin/main, or if uv/python are not the expected versions, STOP and produce a ChatGPT Setup Escalation Prompt before any further Phase 3 action.

---

## 3. Proposed Branch Name

`phase-3/backtest-strategy-conformance`

**Why this name:**
- `phase-3/` — matches the established per-phase branch prefix pattern (`phase-1/…`, `phase-2/…`, `phase-2b/…`, `phase-2c/…`).
- `backtest-strategy-conformance` — reflects the twin goals per `docs/12-roadmap/phase-gates.md` §"Phase 3": implement the strategy and prove conformance against the specification on historical data. This leaves the door open for a later `phase-3b/…` branch if wider-backfill walk-forward work is split off.

**Branch creation happens only after Gate 1 approval.** No `git checkout -b` during planning.

---

## 4. Exact Scope

### 4.1 What Phase 3 SHALL implement

1. **Locked v1 breakout strategy** (long + short, BTCUSDT primary, ETHUSDT research/comparison-only) per `docs/03-strategy-research/v1-breakout-strategy-spec.md`:
   - 1h EMA(50)/EMA(200) trend bias with three-condition check (crossover, price vs EMA(50), EMA(50) slope over 3 completed bars)
   - 15m ATR(20)-based setup/consolidation detection (8-bar window, range ≤ 1.75×ATR, net drift ≤ 0.35×setup_range)
   - 15m breakout trigger with six-condition check (bias, valid setup, close-beyond-level+0.10×ATR, true-range ≥ ATR, close position inside bar 75%/25%, normalized-ATR regime filter)
   - Initial structural stop: `min(setup_low, breakout_low) − 0.10×ATR` (long mirror for short)
   - Stop-distance filter `0.60×ATR ≤ stop_distance ≤ 1.80×ATR` (reject trades outside band)
   - No-trade filters relevant to backtesting (items 1–4 from spec §"No-Trade Filters"; items 5–10 are live-only and simplified/omitted)
   - Stage 2–7 management (no-movement → −0.25R at +1R → break-even at +1.5R → 2.5×ATR trail at +2R → stagnation exit at +8 bars / no +1R)
   - Re-entry rules (new complete setup + new signal required post-exit)

2. **Research backtest engine** per `docs/03-strategy-research/v1-breakout-backtest-plan.md`:
   - Event loop over completed 15m bars in strict `open_time` ascending order
   - Point-in-time gating: a bar becomes "visible" to the strategy when the simulation cursor advances past `open_time + interval_ms`
   - 1h bias lookup using the most recent 1h bar whose `open_time + 3_600_000 ≤ decision_time_ms` (canonical form — see §11.C.D4)
   - Next-bar-open baseline fill model (entry at next 15m bar's `open`)
   - Stop evaluation against **mark-price klines** (consistent with live `workingType=MARK_PRICE`)
   - Three slippage buckets (LOW / MEDIUM / HIGH — parameterized; exact bps to be chosen at Gate 2, sensitivity-reported at checkpoint)
   - Taker commission with configurable rate (parameterized across {0.05%, 0.04%, 0.02%} sensitivity variants — see §11.A.A5)
   - Funding accrual: sum of funding events whose `funding_time ∈ [entry_fill_time, exit_fill_time]` (inclusive both ends — see §11.A.A6), with correct direction sign
   - Quantity rounding: floor to `LOT_SIZE.stepSize` from the Phase 2c exchangeInfo snapshot (BTCUSDT live filters; see §11.C.D2 for commissionRate/leverageBracket gap handling)
   - Position sizing: `risk_amount = sizing_equity × risk_fraction`, `risk_budget = risk_amount × risk_usage_fraction`, `raw_qty = risk_budget / stop_distance`, then min-across leverage cap + notional cap + stepSize floor; reject if final qty < `LOT_SIZE.minQty` (sizing framework §"Sizing Pipeline")
   - One-position-max, no-pyramiding, no-reversal-while-positioned enforcement
   - BTCUSDT and ETHUSDT as independent simulations (no cross-symbol state)

3. **Reporting layer**:
   - Per-trade record JSON + Parquet with the full schema in §8.D
   - Equity curve (cumulative net PnL by `exit_fill_time`) as Parquet
   - Drawdown series (rolling max-drawdown from peak) as Parquet
   - R-multiple histogram data as Parquet
   - Summary metrics JSON (win rate, expectancy, profit factor, max drawdown, worst streak, long/short split, exit-reason counts, cost-assumption labels)
   - `BacktestReportManifest` JSON per run citing: engine version, strategy version, config, dataset manifest versions consumed (15m klines, 1h derived, mark-price klines, funding events, exchangeInfo snapshot), simulation window `[start_ms, end_ms)`, generation timestamp
   - Reports written to `data/derived/backtests/<experiment_name>/<run_id>/…` (proposed path; see §8)

4. **Tests** (target ~120–150 new tests):
   - Pure strategy calculations (EMA, ATR, setup detection, trigger evaluation, stop, management) — fixture-based, deterministic
   - No-lookahead invariants (mechanically enforced)
   - Completed-bar-only enforcement
   - 1h bias uses only completed bars
   - Fill-assumption tests (next-bar-open, gap-through rule once chosen)
   - Stop-placement tests (including tickSize rounding)
   - Stage 2–7 management tests (hand-constructed MFE scenarios)
   - Cost-model conformance (fees, slippage buckets, funding direction/sign)
   - Rounding conformance (stepSize floor, minQty reject, minNotional reject)
   - End-to-end smoke run on synthetic fixtures (deterministic output)
   - End-to-end smoke run on real 2026-03 BTCUSDT data (small — handful of trades expected)
   - End-to-end smoke run on real 2026-03 ETHUSDT data (comparison parity)
   - Zero-trade edge cases (no bias, no setup, no trigger, window too short for warmup)

5. **Phase 3 reports** under `docs/00-meta/implementation-reports/`:
   - `2026-04-19_phase-3_gate-1-plan.md` (this file)
   - `<date>_phase-3_gate-2-review.md` (pre-commit review before the final commit batch)
   - `<date>_phase-3-checkpoint-report.md` (end of phase)

### 4.2 What Phase 3 SHALL NOT implement

Non-goals are listed in detail in §5.

---

## 5. Explicit Non-Goals

Phase 3 **MUST NOT** include any of the following. A Phase 3 PR that touches any item below should be rejected on scope grounds.

| # | Non-goal | Rationale / owning phase |
|---|----------|--------------------------|
| 1 | Live trading of any kind | Phases 6–9; requires approved gate + operator sign-off |
| 2 | Exchange adapter (real Binance client) | Phase 6 (dry-run) → Phase 8 (tiny-live) |
| 3 | Order placement / simulation via real Binance APIs | Phase 6+ |
| 4 | REST calls to `/fapi/*` (any endpoint, public or private) | No exchange connectivity in Phase 3; Phase 2d (deferred) owns authenticated slice |
| 5 | WebSocket user-stream or market-stream integration | Phase 5/6 |
| 6 | Credentials (production, testnet, BNB-discount, …) | No credentials until the approved phase gate |
| 7 | `.env` file creation | Explicitly forbidden; Phase 1 policy retained |
| 8 | `.mcp.json` creation / MCP server activation | Phase-0 policy retained |
| 9 | Graphify activation | Phase-0 policy retained |
| 10 | Dashboard / web UI / operator console | Phase 5 |
| 11 | Alerting (Telegram / n8n) | Phase 5 |
| 12 | Runtime state machine (SAFE_MODE, kill switch, reconciliation states) | **Phase 4** |
| 13 | SQLite / runtime persistence layer | Phase 4 |
| 14 | Stop confirmation / cancel-and-replace / STOP_PENDING_CONFIRMATION | Phase 6 (dry-run) |
| 15 | Emergency unprotected-position handling | Phase 4/6 |
| 16 | Data downloads (no new `data.binance.vision` fetches) | Separate operator-approved task (**Phase 2e**) |
| 17 | Authenticated endpoint usage (`leverageBracket`, `commissionRate`, account) | Separate operator-approved task (**Phase 2d**) |
| 18 | Walk-forward statistical conclusions / holdout promotion decisions | Requires Phase 2e data + post-Phase-3 analysis; Phase 3 does not produce promotion-grade evidence |
| 19 | Parameter optimization / grid search that shapes v1 defaults | Would contaminate Layer A→C separation per `walk-forward-validation.md` |
| 20 | Touching `docs/12-roadmap/technical-debt-register.md` without explicit operator approval | Per operator directive carried from Phase 2c |
| 21 | Touching `.claude/` agent/rule files | Agent pack is stable |
| 22 | Touching `CLAUDE.md` or `docs/00-meta/current-project-state.md` | Content ownership is operator-gated |
| 23 | New runtime dependencies beyond what `uv sync` already resolves (see §7) | Requires explicit Gate 1 approval line if proposed |
| 24 | Cross-symbol portfolio logic / multi-position simulation | BTCUSDT+ETHUSDT run as **independent** simulations per `exposure-limits.md` research allowlist |
| 25 | Intrabar / tick-level simulation | Strategy is completed-bar-only per spec |

---

## 6. Proposed Files and Directories

All paths are relative to repo root `c:\Prometheus`. Every file below is either **NEW** or flagged **MODIFY (narrow)**. No deletions proposed. No file outside this list will be touched during Phase 3 implementation.

### 6.1 New source code under `src/prometheus/`

```
src/prometheus/strategy/                         [NEW package]
  __init__.py                                    [NEW]
  indicators.py                                  [NEW] — EMA, ATR, rolling helpers (pure functions, no state)
  types.py                                       [NEW] — TrendBias, SetupWindow, BreakoutSignal, EntryIntent,
                                                         StopUpdateIntent, ExitIntent, TradeStage Pydantic/dataclass models
  v1_breakout/                                   [NEW subpackage]
    __init__.py                                  [NEW]
    bias.py                                      [NEW] — 1h EMA bias computation + three-condition evaluator
    setup.py                                     [NEW] — 8-bar consolidation detector + drift cap
    trigger.py                                   [NEW] — breakout trigger (long/short), six-condition check
    stop.py                                      [NEW] — initial structural stop + stop-distance filter
    management.py                                [NEW] — Stage 2–7 management rules (MFE tracking, stop moves)
    strategy.py                                  [NEW] — public entry point: V1BreakoutStrategy, on_completed_bar(),
                                                         stateless outside a Session object that holds per-bar context
```

**Design principles for `strategy/`:**
- Pure functions where possible. State lives in a narrow `StrategySession` dataclass that the backtester constructs per symbol.
- No imports from `research/`, `exchange/`, `persistence/`, `risk.runtime`, or any Binance client.
- Allowed imports: `prometheus.core.*`, `numpy` (for vectorized EMA/ATR — see §7), stdlib.
- Each function has docstring citations to spec sections (e.g., `"""Per v1-breakout-strategy-spec.md §"Higher-Timeframe Trend Bias"."""`).

### 6.2 New source code under `src/prometheus/research/backtest/`

```
src/prometheus/research/backtest/                [NEW package]
  __init__.py                                    [NEW]
  config.py                                      [NEW] — BacktestConfig Pydantic model (window, symbols, sizing_equity,
                                                         risk_fraction, risk_usage_fraction, slippage_bucket,
                                                         taker_fee_rate, notional_cap, adapter=FAKE)
  simulation_clock.py                            [NEW] — point-in-time cursor; predicate `bar_visible_at(t_now_ms, bar)`
  fills.py                                       [NEW] — next-bar-open fill + slippage application + gap-through rule
  stops.py                                       [NEW] — mark-price stop evaluation per bar (hit/no-hit, fill price)
  sizing.py                                      [NEW] — wraps sizing-framework formula: equity → risk → qty, with
                                                         stepSize floor + minQty reject + minNotional reject + caps
  accounting.py                                  [NEW] — running equity, fees, funding accrual across held positions
  funding_join.py                                [NEW] — time-window join of FundingRateEvent rows to open positions
  engine.py                                      [NEW] — main bar-by-bar loop; orchestrates strategy → sizing → fill →
                                                         stop-check → management → exit → PnL
  trade_log.py                                   [NEW] — TradeRecord Pydantic model + Parquet writer
  report.py                                      [NEW] — equity/drawdown/R-multiple computation + BacktestReportManifest
  cli.py                                         [NEW] — `python -m prometheus.research.backtest.cli` (small, explicit)
```

### 6.3 Modified existing files (narrow edits only)

```
src/prometheus/core/__init__.py                  [MODIFY] — re-export new strategy/backtest types if cleaner than
                                                            subpath imports (operator review at Gate 2)
src/prometheus/research/data/__init__.py         [MODIFY] — possibly add `read_exchange_info_snapshot` convenience;
                                                            else leave untouched
configs/dev.example.yaml                         [MODIFY, optional] — add documentation-only `backtest:` block
                                                            (scenario window, sizing_equity, slippage/fee defaults).
                                                            No loader consumes it in Phase 3.
docs/00-meta/implementation-ambiguity-log.md     [MODIFY] — append Phase 3 GAP entries as ambiguities resolve during
                                                            implementation (GAP-014 onward)
```

### 6.4 New tests

```
tests/unit/strategy/                             [NEW directory]
  __init__.py                                    [NEW]
  test_indicators.py                             [NEW] — EMA/ATR correctness against hand-computed fixtures
  test_types.py                                  [NEW] — model invariant tests (frozen/strict/extra=forbid)
  v1_breakout/
    __init__.py                                  [NEW]
    test_bias.py                                 [NEW] — long/short/neutral bias cases; EMA warmup; slope rule
    test_setup.py                                [NEW] — valid/invalid 8-bar windows; drift cap; range cap
    test_trigger.py                              [NEW] — six-condition trigger for long/short; ATR regime filter
    test_stop.py                                 [NEW] — initial stop calc; 0.60/1.80 ATR filter; tickSize rounding
    test_management.py                           [NEW] — Stage 2–7 transitions with hand-built MFE paths
    test_strategy_end_to_end.py                  [NEW] — synthetic mini-scenario: full entry→stage3→stage5→exit
    test_no_lookahead.py                         [NEW] — mechanical: any call reads only bars with
                                                            close_time < decision_time_ms

tests/unit/research/backtest/                    [NEW directory]
  __init__.py                                    [NEW]
  test_simulation_clock.py                       [NEW] — bar_visible_at predicate boundary cases
  test_fills.py                                  [NEW] — next-bar-open baseline; slippage; end-of-data reject
  test_stops.py                                  [NEW] — mark-price stop hit; gap-through behavior
  test_sizing.py                                 [NEW] — full sizing pipeline; caps; rounding; below-minQty reject;
                                                          notional-cap bind; leverage-cap bind
  test_accounting.py                             [NEW] — running equity; fee accrual; funding accrual sign; MAE/MFE
  test_funding_join.py                           [NEW] — inclusive-both-ends window join; sign; multi-event
  test_engine.py                                 [NEW] — toy 50-bar scenario deterministic run
  test_trade_log.py                              [NEW] — TradeRecord schema, Parquet round-trip, JSON sidecar
  test_report.py                                 [NEW] — equity/drawdown/R-multiple computation; manifest generation
  test_cli.py                                    [NEW] — argument parsing; config validation; refuses to run with
                                                          adapter != FAKE

tests/simulation/                                [NEW directory per codebase-structure.md §"Simulation tests"]
  __init__.py                                    [NEW]
  test_backtest_synthetic_end_to_end.py          [NEW] — synthetic fixture → engine → report (deterministic)
  test_backtest_real_2026_03_btcusdt.py          [NEW] — real BTC 2026-03 → engine → report sanity checks
                                                          (trade count reasonable; no NaN; manifests cited)
  test_backtest_real_2026_03_ethusdt.py          [NEW] — parity on ETH
  test_backtest_invariants.py                    [NEW] — no-lookahead + completed-bar invariants over a real run
```

### 6.5 Non-committed / git-ignored outputs

Generated at run time. **Committed to `.gitignore` during Phase 3 if not already covered**:

```
data/derived/backtests/**                        [generated, git-ignored]
  <experiment_name>/<run_id>/
    trade_log.parquet
    trade_log.json                               (sidecar for easy review)
    equity_curve.parquet
    drawdown.parquet
    r_multiple_hist.parquet
    summary_metrics.json
    backtest_report.manifest.json
```

`.gitignore` check: `research/data/raw|normalized|derived/**` is already covered; `data/raw|normalized|derived/**` was added in Phase 2. Phase 3 must verify `data/derived/backtests/**` is git-ignored by the existing `data/derived/**` pattern before first run. If it is not, a narrow `.gitignore` edit will be proposed at Gate 2 (single-line addition), with operator approval required.

### 6.6 Files deliberately untouched

- `.claude/**`
- `CLAUDE.md`
- `docs/00-meta/current-project-state.md`
- `docs/12-roadmap/technical-debt-register.md` (unless operator explicitly authorizes a TD-006 annotation follow-up — separate from Phase 3)
- `.mcp.example.json` / `.mcp.graphify.template.json` / `.mcp.json` (never creating the last)
- Any file under `src/prometheus/research/data/` already written in Phases 2/2b/2c (unless a strictly additive re-export is needed — flagged in 6.3)
- Any docs under `docs/04-data/**`, `docs/06-execution-exchange/**`, `docs/07-risk/**`, `docs/10-security/**`, `docs/11-interface/**` (Phase 3 consumes them; it does not revise them)

---

## 7. Dependency Additions

**Proposal: ADD `numpy` as a runtime dependency.**

### 7.1 Rationale

- EMA(50), EMA(200), ATR(20), rolling max/min, rolling high/low, and rolling true-range computations are used in the hot loop of the backtester. Hand-written Python loops for these are both slower and more error-prone than numpy vectorized equivalents.
- `numpy` is a de-facto standard in the Python quantitative stack and is already a transitive dependency of `pyarrow` (part of the Phase 2 footprint). Adding it as a direct dependency **does not introduce new third-party code into the environment** — it only pins the direct use.
- Alternative: implement indicators by hand with Python loops. This is possible but (a) slows real-data runs, (b) increases the probability of implementation bugs vs. well-tested numpy, and (c) fights a battle that doesn't need fighting for a research tool.
- Strict mypy already has `ignore_missing_imports = true` for `pyarrow`/`duckdb`; numpy ships stubs natively in recent versions, so no mypy override is needed.

### 7.2 Proposed pin

`numpy>=2.0,<3.0` in `[project.dependencies]` of `pyproject.toml`. The exact resolved version will be captured in `uv.lock`.

### 7.3 No other dependencies proposed

- `pandas`: **explicitly rejected**. DuckDB + pyarrow + pydantic + numpy cover all data manipulation needed. Adding pandas would introduce a second way to do the same thing.
- `polars`: **explicitly rejected** for Phase 3 (could be reconsidered in a later phase if vectorized dataframe workflows dominate).
- `matplotlib` / `plotly` / `seaborn`: **out of scope**. Phase 3 produces data artifacts (Parquet + JSON). Plotting belongs to Phase 5 (dashboard) or external notebook workflows.
- Any statistics / ML / optimization library (`scipy`, `statsmodels`, `scikit-learn`): **out of scope**. v1 is rules-based.

### 7.4 If operator rejects the numpy addition

Fallback: implement indicators in pure Python with stdlib `statistics` and `collections.deque`. Tests identical. Performance ~10–20× slower on real data but still well within acceptable limits for one-month backtests. Plan remains viable without numpy. Operator decides at Gate 1.

---

## 8. Data Inputs

### 8.1 Real 2026-03 data (present on disk, Phase 2b/2c origin)

| Dataset | Path | Manifest |
|---------|------|----------|
| BTC 15m klines | `data/normalized/klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/` | `binance_usdm_btcusdt_15m__v001.manifest.json` |
| ETH 15m klines | `data/normalized/klines/symbol=ETHUSDT/interval=15m/year=2026/month=03/` | `binance_usdm_ethusdt_15m__v001.manifest.json` |
| BTC 1h derived | `data/derived/bars_1h/standard/symbol=BTCUSDT/interval=1h/year=2026/month=03/` | `binance_usdm_btcusdt_1h_derived__v001.manifest.json` |
| ETH 1h derived | `data/derived/bars_1h/standard/symbol=ETHUSDT/interval=1h/year=2026/month=03/` | `binance_usdm_ethusdt_1h_derived__v001.manifest.json` |
| BTC 15m mark-price | `data/normalized/mark_price_klines/symbol=BTCUSDT/interval=15m/year=2026/month=03/` | `binance_usdm_btcusdt_markprice_15m__v001.manifest.json` |
| ETH 15m mark-price | `data/normalized/mark_price_klines/symbol=ETHUSDT/interval=15m/year=2026/month=03/` | `binance_usdm_ethusdt_markprice_15m__v001.manifest.json` |
| BTC funding | `data/normalized/funding_rate/symbol=BTCUSDT/year=2026/month=03/` | `binance_usdm_btcusdt_funding__v001.manifest.json` |
| ETH funding | `data/normalized/funding_rate/symbol=ETHUSDT/year=2026/month=03/` | `binance_usdm_ethusdt_funding__v001.manifest.json` |
| exchangeInfo snapshot | `data/derived/exchange_info/2026-04-19T21-22-59Z.json` | **none — see §11.C.D1** |

### 8.2 Synthetic Phase 2 fixtures

`tests/fixtures/market_data/synthetic.py` — deterministic seeded generator. Reused for unit tests only. Not used for any result cited as evidence.

### 8.3 No new downloads in Phase 3

Phase 3 does **not** extend any data range, does **not** run any `BulkDownloader`, does **not** call any REST endpoint. If walk-forward validation beyond 2026-03 is required, it is proposed as a separate operator-approved task (**Phase 2e**; see §11.D.DS1 and §16).

---

## 9. Strategy Implementation Plan

### 9.1 Locked v1 breakout rules (per strategy spec)

Rules enumerated in §4.1 item 1. Code structure mirrors the spec sections:

| Spec section | Module | Function/class |
|---|---|---|
| "Higher-Timeframe Trend Bias" | `strategy/v1_breakout/bias.py` | `compute_1h_bias(completed_1h_bars) -> TrendBias` |
| "Setup / Consolidation Rules" | `strategy/v1_breakout/setup.py` | `detect_setup(last_8_15m_bars, atr_20) -> SetupWindow \| None` |
| "Entry Trigger Rules" (long) | `strategy/v1_breakout/trigger.py` | `evaluate_long_trigger(bias, setup, breakout_bar, atr_20) -> BreakoutSignal \| None` |
| "Entry Trigger Rules" (short) | `strategy/v1_breakout/trigger.py` | `evaluate_short_trigger(…)` |
| "Initial Stop Logic" | `strategy/v1_breakout/stop.py` | `compute_initial_stop(direction, setup, breakout_bar, atr_20) -> float` |
| "Stop-distance filter" | `strategy/v1_breakout/stop.py` | `passes_stop_distance_filter(stop_distance, atr_20) -> bool` |
| "Exit Logic" (Stage 2–5) | `strategy/v1_breakout/management.py` | `TradeManagement.update(position, completed_bar, atr_20) -> StopUpdateIntent \| ExitIntent \| None` |
| "No-Trade Filters" | `strategy/v1_breakout/strategy.py` | `_apply_backtest_filters(…)` — live-only filters (stream staleness etc.) no-op in backtest |
| "Re-Entry Rules" | `strategy/v1_breakout/strategy.py` | `_can_re_enter(session_state, last_exit, …)` |

### 9.2 Output contract (strategy → backtest engine)

Pure-typed intents:

```python
@frozen
class EntryIntent:
    symbol: Symbol
    direction: Direction  # LONG | SHORT
    signal_bar_open_time: int
    proposed_entry_reference_price: float  # signal-bar close (proxy for pre-fill)
    initial_stop: float
    stop_distance: float  # abs(ref_price - initial_stop)
    atr_20_at_signal: float
    justification: dict  # bias snapshot, setup window, trigger condition values

@frozen
class StopUpdateIntent:
    symbol: Symbol
    new_stop: float
    direction_check_rule: RiskReducingOnly  # enforces no-widening
    reason: StopMoveStage  # STAGE_3 | STAGE_4 | STAGE_5_TRAIL

@frozen
class ExitIntent:
    symbol: Symbol
    reason: ExitReason  # STAGNATION | TRAILING_BREACH | MANAGED_SIGNAL
    triggering_bar_close_time: int
```

The strategy produces intents; the engine validates, sizes, fills, and records. The strategy never touches simulated balance, never counts bars outside its warmup window, never reads future bars.

### 9.3 Session state (per symbol, per backtest run)

A narrow object holding:
- 1h bias history (tail of completed 1h bars)
- 15m rolling window for setup detection
- 15m ATR(20) rolling computation
- Current position state: FLAT / LONG_POSITIONED / SHORT_POSITIONED
- Current stop level (if positioned)
- Current trade stage (Stage 2 / 3 / 4 / 5)
- MFE / MAE trackers
- Bars-in-trade counter
- Last exit reference (for re-entry rule)

No global state. No I/O. The backtest engine constructs one `StrategySession` per symbol per run.

---

## 10. Backtest Engine: Detailed Rule Plan

### 10.1 Completed-bar-only timing enforcement

Encoded in `simulation_clock.py`:

```python
def bar_visible_at(t_now_ms: int, bar: NormalizedKline) -> bool:
    return t_now_ms >= bar.open_time + interval_duration_ms(bar.interval)
```

**Canonical form adopted** (resolving §11.C.D4): a bar is visible when at least one full interval duration has elapsed since its open. Equivalent to `t_now_ms > close_time`, but expressed against `open_time + duration` for clarity.

Engine invariant: the strategy receives only bars satisfying `bar_visible_at(t_now_ms, bar)`. Enforced by a narrow accessor that the strategy must call through — direct access to the raw kline list is not permitted (lint-level check).

### 10.2 1h bias lookup (point-in-time valid)

```python
def select_1h_bias_bar(completed_1h_bars: list[NormalizedKline], decision_time_ms: int) -> NormalizedKline:
    # Most recent 1h bar whose full 1h duration has elapsed strictly before decision_time_ms.
    # Canonical form: bar.open_time + 3_600_000 <= decision_time_ms
    eligible = [b for b in completed_1h_bars if b.open_time + 3_600_000 <= decision_time_ms]
    if not eligible:
        raise InsufficientWarmupError(...)
    return max(eligible, key=lambda b: b.open_time)
```

`decision_time_ms` = `signal_bar.open_time + 900_000` (the instant the 15m signal bar closes).

### 10.3 No-lookahead / no-forward-leakage enforcement

Three layers of defense:

1. **Gated access**: `StrategySession` exposes only `bars_visible_at(t_now_ms)` — a filtered tuple. No `.all_bars` field exists on the session.
2. **ATR/EMA computation locks**: indicators are computed once per bar close and cached. A later call at the same `t_now_ms` returns the cached value — attempting to re-compute with future data is a `LookaheadError`.
3. **Mechanical test** (in `test_no_lookahead.py`): construct a synthetic series, run the strategy up to bar N, mutate bar N+1 to an extreme value, re-run up to bar N, assert the signal at bar N is identical. If the implementation reads bar N+1 during bar N's decision, the test fails.

### 10.4 Fill model — baseline

**Entry fill:** `fill_price = next_bar.open`, where `next_bar` is the 15m bar whose `open_time == signal_bar.open_time + 900_000`.

`fill_time_ms = next_bar.open_time`.

**Slippage applied to entry:** `effective_entry_price = fill_price × (1 + slippage_bps × sign / 10_000)`, where `sign = +1 for long`, `-1 for short` (adverse direction).

**End-of-data rule:** if the signal bar is the last bar in the window (no next bar exists), the trade is logged as `UNFILLED_END_OF_DATA` and not entered. No "wrap-around" fill.

### 10.5 Stop-hit evaluation (mark-price primary)

Per bar after entry:

```python
def check_stop_hit(position: OpenPosition, mark_price_bar: MarkPriceKline) -> StopHit | None:
    if position.direction == LONG:
        if mark_price_bar.low <= position.current_stop:
            # gap-through rule (see §11.A.A4)
            if mark_price_bar.open <= position.current_stop:
                # adverse gap — fill at bar open
                fill_price = mark_price_bar.open
            else:
                # intrabar trigger — fill at stop level
                fill_price = position.current_stop
            # apply exit slippage
            fill_price *= (1 - slippage_bps / 10_000)
            return StopHit(fill_price=fill_price, fill_time_ms=mark_price_bar.close_time + 1)
    # short mirror
    return None
```

**Gap-through rule proposed: Option 2 (fill at open when bar opens beyond stop)** — §11.A.A4 flags this for operator approval.

### 10.6 Commission / funding / slippage

**Commission:** `fee = |fill_price| × quantity × fee_rate`. Applied to entry and to exit. Default proposal: parameterize `fee_rate` across `{0.0005, 0.0004, 0.0002}`; primary result cited with `0.0005`.

**Funding:** at each completed 15m bar, check if any FundingRateEvent has `funding_time ∈ (previous_bar_close_time, current_bar_close_time]`. For each matched event and each held position:

```python
direction_sign = +1 if direction == LONG else -1
# positive rate means longs pay → long's funding_pnl is negative
funding_pnl = position_notional × funding_rate × (-direction_sign)
```

Window boundary proposal for entry/exit: **inclusive both ends** (`T_entry <= funding_time <= T_exit`) — §11.A.A6 flags for operator approval.

**Slippage:** three labeled buckets. Numeric defaults proposed (to be confirmed at Gate 2):
- LOW: 1 bps (0.01%)
- MEDIUM: 3 bps (0.03%)
- HIGH: 8 bps (0.08%)

Applied to both entry and exit. Primary result cited with MEDIUM. Reports include all three buckets as sensitivity rows.

### 10.7 Position sizing (per sizing-framework)

Implemented in `sizing.py`. Inputs: `sizing_equity_usdt`, `risk_fraction`, `risk_usage_fraction`, `stop_distance`, `proposed_entry_reference_price`, `symbol_filters` (from exchangeInfo), `max_effective_leverage`, `max_notional_internal_usdt`.

Pipeline exactly per `docs/07-risk/position-sizing-framework.md §"Sizing Pipeline"`:

1. Risk amount: `risk_fraction × sizing_equity`
2. Risk budget: `risk_amount × risk_usage_fraction`
3. Raw qty: `risk_budget / stop_distance`
4. Leverage cap qty: `(sizing_equity × max_effective_leverage) / proposed_entry_price`
5. Notional cap qty: `max_notional_internal / proposed_entry_price`
6. Candidate qty: `min(raw_qty, lev_cap_qty, notional_cap_qty)`
7. Floor to stepSize (from `LOT_SIZE` filter)
8. If `floored_qty < LOT_SIZE.minQty` → reject (REJECTED_BELOW_MINQTY)
9. If `floored_qty × proposed_entry_price < MIN_NOTIONAL.notional` → reject (REJECTED_BELOW_MIN_NOTIONAL)
10. Emit `sizing_limited_by` label ∈ {STOP_RISK, MAX_EFFECTIVE_LEVERAGE, INTERNAL_NOTIONAL_CAP, STEP_SIZE_FLOOR}

**Parameters requiring operator decision** (§11.B):
- `sizing_equity_usdt` starting value
- `risk_usage_fraction` (0.90 or 1.00 for backtest)
- `max_notional_internal_usdt` research cap

### 10.8 Trade lifecycle model

State machine per `StrategySession`:

```
FLAT
  └─ on EntryIntent + sizing passes → ENTERED_PENDING_FILL
                                         └─ on next bar open → OPEN_POSITION (Stage 2)

OPEN_POSITION (Stage 2)
  ├─ on stop hit → CLOSED (exit_reason=STOP)
  ├─ on MFE ≥ +1R → OPEN_POSITION (Stage 3)
  └─ on bars_in_trade ≥ 8 AND MFE < +1R → CLOSED (exit_reason=STAGNATION, fill at next bar open)

OPEN_POSITION (Stage 3)
  ├─ on stop hit → CLOSED (STOP, new stop = -0.25R)
  └─ on MFE ≥ +1.5R → OPEN_POSITION (Stage 4)

OPEN_POSITION (Stage 4)
  ├─ on stop hit → CLOSED (STOP, new stop = break-even)
  └─ on MFE ≥ +2.0R → OPEN_POSITION (Stage 5, trailing active)

OPEN_POSITION (Stage 5)
  ├─ on stop hit → CLOSED (STOP, trail level)
  └─ on trail breach at bar close → CLOSED (exit_reason=TRAILING_BREACH)

CLOSED → FLAT (after recording trade)
```

Re-entry allowed only when a new complete setup + new trigger fires after reaching `FLAT`. `last_exit_bar` recorded for debugging.

### 10.9 Position tracking

Fields on `OpenPosition`:
- `entry_fill_time_ms`, `entry_fill_price`, `quantity`, `notional`, `direction`
- `current_stop`, `current_stage`, `bars_in_trade`
- `running_mfe_r`, `running_mae_r` (R-units, computed against initial stop distance)
- `high_water_mark_price`, `low_water_mark_price` (for trailing)
- `accrued_funding_pnl` (sum of funding events during holding)

---

## 11. Ambiguities / Conflicts to Surface

This section consolidates all ambiguities surfaced during Phase 3 Gate 1 research by the strategy, risk, and data specialist agents. **Every item below requires operator decision before implementation proceeds.**

### 11.A. Strategy / backtest ambiguities

| ID | Title | Recommended | Risk |
|---|---|---|---|
| A1 | 1h normalized ATR filter: 15m ATR or 1h ATR? Which close? | Use 1h ATR(20) and latest completed 1h close — matches the "1h" label. Surface to operator. | MEDIUM |
| A2 | Stop-distance filter reference price: signal-bar close vs actual fill? | Signal-bar close (all info known at signal time; fill not yet realized). | LOW |
| A3 | Exit fill price for trailing/stagnation exits | Next-bar-open (consistent with entry; conservative). | LOW |
| A4 | Gap-through stop rule | Fill at bar open if gap; else fill at stop level. Realistic for STOP_MARKET. | MEDIUM (materially affects tail losses) |
| A5 | Taker commission rate | Parameterize {0.05%, 0.04%, 0.02%}; primary = 0.05%. | LOW |
| A6 | Funding event join window boundary | Inclusive both ends (`T_entry <= t <= T_exit`). | LOW |
| A7 | ExchangeInfo snapshot date mismatch (2026-04-19 snapshot used for 2026-03 window) | Accept as proxy for Phase 3 conformance; operator-approve acceptance limitation. | LOW |

### 11.B. Risk-framework decisions (not locked in risk docs)

| ID | Title | Recommended | Risk |
|---|---|---|---|
| R1 | Starting sizing_equity_usdt (not locked anywhere) | Propose `10_000` USDT as Phase 3 research default; flat (non-compounding) for primary variant; compounding as sensitivity. | LOW |
| R2 | Risk-usage fraction in backtest: 0.90 (live default) or 1.00 (pure risk)? | Primary = 0.90 (matches live sizing); 1.00 reported as sensitivity. | LOW |
| R3 | Research internal notional cap | Propose `100_000` USDT (well above any size 10k-equity * 2x-leverage could produce); surfaced so it never silently binds. | LOW |
| R4 | Risk fraction — primary variant | 0.0025 (0.25%, matches live default); 0.005, 0.01 as sensitivity sweeps per sizing spec research allowance. | LOW |

### 11.C. Data-contract clarifications

| ID | Title | Recommended | Risk |
|---|---|---|---|
| D1 | exchangeInfo snapshot has no `DatasetManifest` entry | Accept the timestamp-named JSON as sufficient for Phase 3; log as GAP and consider a retroactive manifest emission in a separate small task. Do not block Phase 3 on it. | LOW |
| D2 | Validation checklist Gate 1 requires leverage-bracket and commissionRate snapshots, which are authenticated endpoints deferred to Phase 2d | **Hard gap against strict reading.** Phase 3 proceeds with placeholder commission rates (sensitivity-reported) and no leverage-bracket check (not used in v1 because max_effective_leverage = 2x is well below any published bracket threshold). Document as accepted limitation. | MEDIUM — operator must confirm this accepted-limitation reading |
| D3 | 1h derived manifest `predecessor_version` is null; derivation provenance only in `sources` field | Non-blocking. Phase 3 cites `sources` in the report manifest. Future data-layer fix may populate `predecessor_version`. | LOW |
| D4 | 1h bias comparator form precision | Canonical form adopted: `bar.open_time + 3_600_000 <= decision_time_ms`. Documented explicitly in `simulation_clock.py`. | LOW |

### 11.D. Data-sufficiency question

| ID | Title | Recommended | Risk |
|---|---|---|---|
| DS1 | 2026-03 data (31 days) is sufficient for Gate 1 conformance / mechanics; insufficient for Validation Gates 4–6 (walk-forward, robustness, ETH comparison at scale) | **Propose Phase 2e** as a separate operator-approved wider-backfill task. Phase 3 completes on 2026-03 scope without attempting walk-forward statistical conclusions. Phase 2e scope proposal: BTC + ETH 15m bulk for 2022-01 through 2026-03 via existing `BulkDownloader` (no code changes beyond month iteration). Submitted to operator post-Phase-3 or in parallel if operator prefers. | HIGH if conflated with Phase 3 |

### 11.E. Operator is asked to confirm or override each recommendation

For each of A1–A7, R1–R4, D1–D4, DS1, operator should respond at Gate 1 approval with either "accept recommendation" or "use Option X / value Y instead." Any silent acceptance of the default carries the risk of baking a research default into code review evidence. Explicit confirmation is preferred.

---

## 12. Validation / Conformance Tests

Mapped to `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` Gates 1, 2, 3. Gates 4–8 are out of Phase 3 scope (see §5 non-goal 18).

### 12.1 Strategy rule conformance (Gate 2)

- EMA(50)/EMA(200) correctness against hand-computed series
- ATR(20) correctness (Wilder's method — spec-confirmed)
- 1h bias three-condition check: long, short, neutral cases
- 8-bar setup window: valid, invalid (range too wide), invalid (drift too large)
- Breakout trigger: all six conditions; single-condition failures for each
- Initial stop formula for long and short
- Stop-distance filter accept/reject cases
- Stage 2–7 transitions with hand-built MFE paths
- Re-entry rule: blocked immediately post-exit, allowed after new setup+trigger

### 12.2 Timestamp conformance

- All timestamps UTC milliseconds throughout engine internals
- 1h bias selection uses canonical `open_time + 3_600_000 <= decision_time_ms`
- 15m → 1h alignment verified on real derived data
- Completed-bar-only — a forming bar is never accessed

### 12.3 No-lookahead

- Mechanical test: mutate future bar, assert past decision unchanged
- `StrategySession` exposes no direct access to future bars
- Indicators cached per `t_now_ms`; recompute attempts raise

### 12.4 Fill assumptions

- Entry fill = `next_bar.open`
- End-of-data → no fill
- Slippage applied with correct direction sign
- Gap-through rule (§11.A.A4 choice) tested

### 12.5 Stop assumptions

- Mark-price bars used for stop evaluation (not standard klines)
- Stop widening forbidden (enforced by `risk_reducing_only_check`)
- Stop price rounded to `tickSize`

### 12.6 Funding assumptions

- Inclusive-both-ends window (§11.A.A6 choice) tested
- Direction sign correct (long pays when rate positive)
- Multi-event held position tested
- Funding event outside holding window not applied

### 12.7 ExchangeInfo rounding assumptions

- Quantity floors to `stepSize`
- Below-minQty rejects (does not scale up)
- Below-minNotional rejects
- Price rounds to `tickSize`

### 12.8 Engine invariants

- One-position-max enforced
- No-pyramiding enforced
- No-reversal-while-positioned enforced
- BTCUSDT and ETHUSDT simulations fully independent

---

## 13. Output Artifact Plan

### 13.1 Layout

```
data/derived/backtests/
  <experiment_name>/
    <run_id>/                       # <run_id> = UTC timestamp + short hash of config
      trade_log.parquet             # one row per closed trade
      trade_log.json                # sidecar for easy review
      equity_curve.parquet          # cumulative PnL by trade close time
      drawdown.parquet              # rolling max-drawdown
      r_multiple_hist.parquet       # histogram bins + counts
      summary_metrics.json          # all aggregate metrics
      backtest_report.manifest.json # provenance + dataset linkage
      config_snapshot.json          # exact BacktestConfig used
```

### 13.2 What is committed

**Nothing under `data/derived/backtests/` is committed.** All run outputs are git-ignored. This matches the Phase 2 `data/` posture.

### 13.3 What IS committed

- Phase 3 code (src + tests)
- Phase 3 reports under `docs/00-meta/implementation-reports/`
- Any ambiguity-log updates
- Any `configs/dev.example.yaml` additions (documentation-only)
- Any `pyproject.toml` / `uv.lock` changes if numpy is approved (§7)

### 13.4 Summary format for ChatGPT / operator review

Each run produces a short human-readable summary that can be pasted into chat:

```
Phase 3 Backtest — <experiment_name> / <run_id>
================================================
Window:           2026-03-01T00:00:00Z to 2026-04-01T00:00:00Z
Symbols:          BTCUSDT (primary), ETHUSDT (comparison)
Config:           risk_fraction=0.0025, risk_usage=0.90, leverage_cap=2x,
                  notional_cap=100000 USDT, slippage=MEDIUM (3 bps),
                  fee_rate=0.05% taker, adapter=FAKE, sizing_equity=10000

BTCUSDT:
  Trades: 11  (7 long, 4 short)
  Win rate: 45.5%
  Net PnL: +2.8%  |  Gross: +3.6%  |  Fees: -0.4%  |  Funding: -0.3%  |  Slippage: -0.1%
  Max drawdown: -1.4% (from 1.012 peak to 0.997 trough)
  Expectancy: +0.35 R/trade
  Profit factor: 1.42
  Exit reasons: STOP=5, STAGNATION=3, TRAILING=3

ETHUSDT:
  … (same shape)

Dataset manifests consumed:
  binance_usdm_btcusdt_15m__v001
  binance_usdm_btcusdt_1h_derived__v001
  binance_usdm_btcusdt_markprice_15m__v001
  binance_usdm_btcusdt_funding__v001
  exchange_info_2026-04-19T21-22-59Z (unmanifested — GAP-XXX)
  … (ETH variants)

Warnings: 0 invalid windows. 2 bars with funding at exact entry time → counted inclusive.
```

These figures are **illustrative only** — not predictions of Phase 3 results.

---

## 14. Safety Constraints

| Constraint | Phase 3 behavior |
|---|---|
| Production Binance API keys | **Not created, not requested, not used** |
| `.env` | **Not created** |
| Credentials in any form | **None** |
| Exchange-write capability | **None** — engine takes no IO beyond reading local Parquet + writing local reports |
| REST calls to `/fapi/*` | **None** |
| WebSocket connections | **None** |
| Third-party market-data sources | **None** |
| Authenticated endpoints | **None** — placeholder fees/leverage; sensitivity analysis over fee rates |
| `.mcp.json` / MCP servers | **Not created / not enabled** |
| Graphify | **Not enabled** |
| Dashboard / UI / manual trading controls | **None** |
| Data downloads | **None** — uses existing on-disk data only |
| Real exchange state / order lifecycle / user stream | **None** |
| Persistence runtime / SQLite / kill switch | **None** — simulation state is per-process, discarded after run |
| Runtime mode (SAFE_MODE) | **N/A — no runtime exists** |
| `docs/12-roadmap/technical-debt-register.md` edits | **None** unless explicitly authorized by operator as a separate task |
| `.claude/` / `CLAUDE.md` / `current-project-state.md` edits | **None** |
| Destructive git operations | **None** — only `git checkout -b`, `git add <narrow paths>`, `git commit`, `git mv` if rename is needed |
| `--force`, `--no-verify`, `git add -f` | **Never used** |
| Network access during tests | **Zero** — no fixture requires network |

### 14.1 Mechanical guardrails planned

1. `BacktestConfig.adapter` is a `StrEnum` with value `FAKE` only. Any attempt to set it to a `REAL` or `LIVE` value raises at config validation. The enum has no such value in Phase 3.
2. `research/backtest/*.py` modules have an import-time assertion blocking any import from `prometheus.exchange.*` or from any module matching `binance_rest.*`, `binance_ws.*`, etc. The engine has no exchange surface.
3. All report file writes use `write_path.parent.mkdir(parents=True, exist_ok=True)` scoped to `data/derived/backtests/`. No writes anywhere else.
4. `mypy --strict` continues to pass on all new source files.

---

## 15. Ambiguity / Spec-Gap Items to Log

Upon Gate 1 approval, append these entries to `docs/00-meta/implementation-ambiguity-log.md` using the standard format. IDs continue from GAP-20260419-013 (Phase 2c last).

- **GAP-20260419-014** — 1h normalized ATR filter ambiguity (§11.A.A1). Status: OPEN pending operator decision.
- **GAP-20260419-015** — Stop-distance filter reference price for backtest (§11.A.A2). Status: RECOMMENDED; confirm.
- **GAP-20260419-016** — Exit fill price for managed exits (§11.A.A3). Status: RECOMMENDED; confirm.
- **GAP-20260419-017** — Gap-through stop rule (§11.A.A4). Status: RECOMMENDED (Option 2); confirm.
- **GAP-20260419-018** — Taker commission rate source and sensitivity range (§11.A.A5, §11.C.D2). Status: RECOMMENDED.
- **GAP-20260419-019** — Funding event join window boundary (§11.A.A6). Status: RECOMMENDED.
- **GAP-20260419-020** — ExchangeInfo snapshot date proxy (2026-04-19 → 2026-03) (§11.A.A7, §11.C.D1). Status: RECOMMENDED as accepted limitation.
- **GAP-20260419-021** — Starting sizing_equity_usdt for Phase 3 research default (§11.B.R1). Status: RECOMMENDED (10,000 USDT).
- **GAP-20260419-022** — Risk-usage fraction in backtest 0.90 vs 1.00 (§11.B.R2). Status: RECOMMENDED (0.90 primary, 1.00 sensitivity).
- **GAP-20260419-023** — Research internal notional cap value (§11.B.R3). Status: RECOMMENDED (100,000 USDT).
- **GAP-20260419-024** — Validation Gate 1 "commissionRate + leverageBracket snapshots available" vs. deferred authenticated endpoints (§11.C.D2). Status: OPEN — requires explicit operator accepted-limitation confirmation.
- **GAP-20260419-025** — Phase 2e wider historical backfill for walk-forward validation (§11.D.DS1). Status: OUT-OF-PHASE-3 proposal requiring operator approval.

---

## 16. Technical-Debt Register Items Potentially Affected

**Per operator directive, no edits to `docs/12-roadmap/technical-debt-register.md` during Phase 3.**

For reference only — items this phase interacts with, to be surfaced as follow-up if operator approves a separate register update:

- **TD-006** (Binance API verification): three new slices in Phase 3 cite the existing Phase 2c verifications; no new endpoints exercised. No new TD-006 surface.
- **TD-016** (statistical thresholds require evidence): Phase 3 produces 2026-03 mechanics evidence; cannot discharge TD-016. Remains OPEN.
- **TD-018** (tiny-live notional cap value TBD): Phase 3 defines a *research* cap (proposed 100,000 USDT) distinct from the live cap. Does not resolve TD-018.
- **Potential NEW item — Phase 2e wider backfill**: if operator agrees the walk-forward data gap should be tracked, a new TD entry (e.g., TD-021) could be added post-Phase-3. Not proposed here; surfaced only.
- **Potential NEW item — Phase 2d authenticated endpoints**: leverageBracket + commissionRate gap (§11.C.D2) is already implicit in Phase 2c's deferral; operator may want to track under a new TD entry.

---

## 17. Proposed Commit Structure

**Commit granularity target: 6–8 small, reviewable commits, each individually buildable and testable.** Mirrors the Phase 2b/2c discipline. Each commit ends with a green quality-gate suite.

| # | Theme | Files (indicative) |
|---|---|---|
| 1 | `strategy/` pure types + indicators | `strategy/__init__.py`, `strategy/indicators.py`, `strategy/types.py`, `tests/unit/strategy/test_indicators.py`, `tests/unit/strategy/test_types.py` |
| 2 | `strategy/v1_breakout/` bias + setup + trigger | `bias.py`, `setup.py`, `trigger.py`, matching tests |
| 3 | `strategy/v1_breakout/` stop + management + end-to-end strategy | `stop.py`, `management.py`, `strategy.py`, matching tests incl. `test_strategy_end_to_end.py` + `test_no_lookahead.py` |
| 4 | `research/backtest/` config + clock + fills + stops + sizing | `config.py`, `simulation_clock.py`, `fills.py`, `stops.py`, `sizing.py`, matching tests |
| 5 | `research/backtest/` accounting + funding_join + trade_log | `accounting.py`, `funding_join.py`, `trade_log.py`, matching tests |
| 6 | `research/backtest/` engine + report + cli | `engine.py`, `report.py`, `cli.py`, matching tests |
| 7 | `tests/simulation/` end-to-end on real 2026-03 data | 4 simulation tests |
| 8 | Ambiguity-log updates + Gate-1 plan + Gate-2 review + `configs/dev.example.yaml` doc-only block (if proposed) | docs + configs |
| (9) | `numpy` dep addition if approved at Gate 1 | `pyproject.toml`, `uv.lock` — **could be commit 0** if numpy is approved, run before any strategy work |

**Commit order is a recommendation; final sequence confirmed at Gate 2. Each commit is self-contained: quality gates (`ruff check`, `ruff format --check`, `mypy`, `pytest`) pass at every commit tip.**

**No pushes during Phase 3.** Branch remains local until Gate 2 approval authorizes push + PR.

---

## 18. Gate 2 Review Format

At Gate 2 (pre-commit review, after all code is written and gates pass locally), produce `docs/00-meta/implementation-reports/<date>_phase-3_gate-2-review.md` with the following sections:

1. Executive summary (1 paragraph)
2. Files changed, by commit — full list with line counts
3. Quality-gate results (ruff + mypy + pytest output, counts)
4. Tests added: count + test-file breakdown
5. Tests removed or modified: should be zero; justify if nonzero
6. Scope verification vs. §4.1 — item-by-item
7. Non-goal verification vs. §5 — item-by-item confirmation that each non-goal was not touched
8. Safety constraints verification — same table as §14 with `PASS / observed behavior` column
9. Ambiguity decisions applied — list of GAP-014 through GAP-025 with final chosen option
10. Dependency changes — if numpy was added, cite `pyproject.toml` and `uv.lock` deltas
11. Real-data smoke run results — summary table (symbol, trade count, net PnL, max DD, exit reasons) per §13.4, illustrative only
12. `git diff --stat` over the commits
13. Proposed commit order for final `git commit` sequence
14. Request for Gate 2 approval

Following Gate 2 approval, commits are executed in the approved order, and a final **Phase 3 Checkpoint Report** is produced with the format required by `.claude/rules/prometheus-phase-workflow.md`.

---

## 19. Gate 1 Approval Requests

Operator, please respond on each of the following so implementation can begin:

1. **Overall plan approval** — accept, modify, or reject.
2. **Branch name** — `phase-3/backtest-strategy-conformance` acceptable?
3. **numpy dependency (§7)** — approve add, approve as optional fallback to pure-Python, or reject?
4. **Ambiguities §11.A (A1–A7)** — confirm recommendations or override each.
5. **Risk decisions §11.B (R1–R4)** — confirm recommendations or override each.
6. **Data clarifications §11.C (D1–D4)** — confirm recommendations; particularly **D2 requires explicit operator accepted-limitation confirmation** because it is the only item that could be read as a Validation-Gate-1 noncompliance.
7. **Phase 2e proposal §11.D.DS1** — acknowledge deferral; Phase 3 proceeds on 2026-03 scope only. Confirm.
8. **Report artifact location** — `data/derived/backtests/**` git-ignored via existing pattern acceptable? If not, propose alternative.
9. **Commit granularity §17** — 6–8 commits acceptable? Preference for fewer larger vs. more smaller?
10. **Any additional non-goals, constraints, or scope restrictions** before Phase 3 begins.

**No implementation will start until all of the above are explicitly answered.**

---

## Appendix A — File Provenance

This plan was produced from:

- `docs/00-meta/current-project-state.md`
- `docs/00-meta/ai-coding-handoff.md`
- `docs/00-meta/implementation-ambiguity-log.md` (entries 001–013)
- `docs/00-meta/implementation-reports/2026-04-19_phase-2c-checkpoint-report.md`
- `docs/00-meta/implementation-reports/2026-04-19_phase-2c_gate-2-review.md`
- `docs/12-roadmap/phase-gates.md`
- `docs/12-roadmap/technical-debt-register.md`
- `docs/03-strategy-research/v1-breakout-strategy-spec.md`
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
- `docs/05-backtesting-validation/cost-modeling.md`
- `docs/05-backtesting-validation/walk-forward-validation.md`
- `docs/05-backtesting-validation/backtesting-principles.md`
- `docs/04-data/data-requirements.md`
- `docs/04-data/timestamp-policy.md`
- `docs/04-data/dataset-versioning.md`
- `docs/04-data/historical-data-spec.md`
- `docs/08-architecture/codebase-structure.md`
- `docs/08-architecture/internal-event-contracts.md`
- `docs/08-architecture/event-flows.md`
- `docs/07-risk/position-sizing-framework.md`
- `docs/07-risk/stop-loss-policy.md`
- `docs/07-risk/exposure-limits.md`
- Phase 2/2b/2c source code at `src/prometheus/core/*.py`, `src/prometheus/research/data/*.py`
- Phase 2/2b/2c test patterns at `tests/unit/**`, `tests/integration/**`
- On-disk data manifests at `data/manifests/*.manifest.json`
- `.claude/rules/prometheus-core.md`, `.claude/rules/prometheus-safety.md`, `.claude/rules/prometheus-phase-workflow.md`, `.claude/rules/prometheus-mcp-and-secrets.md`

Specialist agents consulted in parallel:
- `prometheus-strategy-backtest-engineer` (strategy/backtest methodology synthesis)
- `prometheus-risk-state-engineer` (sizing/stop/exposure in backtest context)
- `prometheus-data-validation-engineer` (dataset contract / manifests / quality checks)

No code was written, no branch was created, no file was edited except this plan file, no dependency was installed, no network call was made, and no credential was referenced. Plan is read-only except for the file this plan is written to.

**End of Phase 3 Gate 1 Plan. Awaiting operator review.**
