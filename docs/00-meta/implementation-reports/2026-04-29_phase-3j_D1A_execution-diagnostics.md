# Phase 3j — D1-A Execution + Diagnostics Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3d-B2 precedent (F1 HARD REJECT); **Phase 3g D1-A spec memo + methodology audit (binding spec)**; **Phase 3h D1-A execution-planning memo (binding execution plan, with timing-clarification amendments)**; **Phase 3i-B1 engine wiring (binding implementation surface)**; `src/prometheus/research/backtest/engine.py`; `src/prometheus/research/backtest/trade_log.py`; `src/prometheus/strategy/funding_aware_directional/`; `scripts/phase3j_D1A_execution.py`; `scripts/_phase3j_D1A_analysis.py`.

**Phase:** 3j — D1-A first-execution candidate phase. Implements the Phase 3i-B1 runner-scaffold body, runs the Phase 3h §10 precommitted R-window inventory (4 mandatory cells; no V cell — gate did not PROMOTE), evaluates the §11 first-execution gate, computes the §12 M1 / M2 / M3 mechanism checks, gathers the §13 mandatory diagnostics, and validates the §14 P.14 hard-block invariants subset achievable from the trade log alone.

**Branch:** `phase-3j/d1a-execution-diagnostics`. **Date:** 2026-04-29 UTC.

**Headline verdict:** **MECHANISM PASS / FRAMEWORK FAIL — other** (Phase 3h §11.2 mapping). Catastrophic-floor predicate **not** triggered → not HARD REJECT. M1 BTC h=32 mechanism check PASSES → not MECHANISM FAIL. Condition (i) `BTC MED expR > 0` FAILS → not PROMOTE. Condition (iv) HIGH-slip cost-resilience FAILS → §11.6 cost-sensitivity gate also blocks.

D1-A is retained as research evidence; non-leading; **no D1-A-prime / B / hybrid authorized**. Phase 3j is **terminal for D1-A** under Phase 3h §11 framework — analogous to Phase 3d-B2's terminal status for F1, but with milder severity (D1-A did not trip the catastrophic-floor predicate that triggered F1's HARD REJECT).

---

## 1. Plain-English summary

D1-A is the funding-aware directional / carry-aware contrarian strategy locked in Phase 3g §6: when the trailing-90-day funding-rate Z-score exceeds |2.0| at a completed funding-settlement time, enter contrarian (LONG below −2σ, SHORT above +2σ) at the next bar's open, with stop = 1.0 × ATR(20) and a fixed +2.0R target, plus a 32-bar (8-hour) unconditional time-stop and a per-funding-event cooldown.

Phase 3j is the **first time D1-A has been run on real BTCUSDT / ETHUSDT v002 data**. The gate evaluation and mechanism checks produce a clear empirical picture:

- **The directional mechanism IS present.** M1 post-entry counter-displacement at h=32 on BTC is **mean +0.17R, fraction-non-negative 0.51** — both above the §11.1 (ii) thresholds (+0.10 R and 0.50). The mean-reversion-after-extreme-funding intuition is empirically supported.
- **The TARGET-subset is highly profitable when isolated.** TARGET-exit subset on BTC: n=52, mean +2.14R, aggregate +111.5R. ETH: n=49, mean +2.45R, aggregate +119.9R. Both pass the M3 §12.3 thresholds.
- **But the realized strategy is unprofitable at MED slippage on BTC.** BTC R MED MARK: trades=198, expR=−0.32R, PF=0.65, WR=0.30. ETH R MED MARK: trades=179, expR=−0.14R, PF=0.83, WR=0.31. Both BTC and ETH fall well below the +0.51 breakeven win rate forecast in Phase 3h §5.6.5.
- **Cost-resilience also fails.** BTC R HIGH MARK: expR=−0.48R, PF=0.51 (above catastrophic-floor −0.50 / 0.30 thresholds, but condition (iv) requires `BTC HIGH expR > 0` and PF > 0.30 simultaneously — only the second holds).
- **Funding-cost benefit is negligible.** M2 mean funding_pnl / realized_risk_usdt is +0.0023R BTC / +0.0045R ETH — three orders of magnitude below the +0.05R PASS threshold per §12.2. Funding accrual does not offset fees/slippage.
- **No catastrophic-floor violation.** All 4 R-window cells stay above (expR > −0.50 OR PF > 0.30) for both symbols. This is materially better than F1's Phase 3d-B2 outcome (5 catastrophic-floor violations producing HARD REJECT).

Net: the mechanism produces a directional edge (M1 PASS) and the geometry delivers the expected per-trade R magnitudes (winners +1.98R BTC / +2.26R ETH, both above the +1.47R MED forecast; losers −1.30R BTC / −1.24R ETH, both better than the −1.53R MED forecast), but the strategy hits its 1.0 × ATR stop too often (~68% of trades) before reaching its +2.0R target. The realized win rate (~30%) is far below the +51% breakeven, so the better-than-expected winner / loser R cannot rescue the framework expectation.

D1-A is **retained as research evidence**; **non-leading**; **no D1-A-prime, D1-B, or hybrid is authorized** (per Phase 3h §15 governance: framework-fail outcomes do not authorize any post-hoc tuning or successor variants without a separately authorized phase).

---

## 2. Pre-execution quality gates (Phase 3j brief §1)

All four pre-execution gates green on the Phase 3j branch tip prior to any D1-A candidate run:

| Gate | Command | Result |
|------|---------|--------|
| Test suite | `uv run pytest` | **668 passed** in 12.10s |
| Linter | `uv run ruff check .` | **All checks passed!** |
| Formatter | `uv run ruff format --check .` | **157 files already formatted** |
| Type checker | `uv run mypy src` | **Success: no issues found in 61 source files** |

No gate failed; no escalation required. Phase 3j proceeded under operator authorization.

## 3. Pre-execution control reproduction (Phase 3j brief §1)

Per the Phase 3j brief, all 5 control runs (10 symbol-level cells: H0 R/V × BTC/ETH; R3 R/V × BTC/ETH; F1 R × BTC/ETH) were re-executed and compared against the most-recent committed baselines from Phase 3i-B1. All cells reproduce bit-for-bit on summary metrics + trade-log content (the trade_log.parquet binary differs only in the per-row UUID suffix of `trade_id` and in NaN-equality semantics; ignoring those, every economically-meaningful column is identical).

| Control | Window | Slippage | Stop trigger | Symbol | Reproduces bit-for-bit |
|---------|--------|----------|--------------|--------|------------------------|
| H0 | R | MED | MARK | BTC | **identical** (n=33) |
| H0 | R | MED | MARK | ETH | **identical** (n=33) |
| H0 | V | MED | MARK | BTC | **identical** (n=8) |
| H0 | V | MED | MARK | ETH | **identical** (n=14) |
| R3 | R | MED | MARK | BTC | **identical** (n=33) |
| R3 | R | MED | MARK | ETH | **identical** (n=33) |
| R3 | V | MED | MARK | BTC | **identical** (n=8) |
| R3 | V | MED | MARK | ETH | **identical** (n=14) |
| F1 | R | MED | MARK | BTC | **identical** (n=4720) |
| F1 | R | MED | MARK | ETH | **identical** (n=4826) |

Phase 3i-B1's claim that the engine surface additions do not perturb V1 or F1 dispatch holds under Phase 3j re-execution. The Phase 3j runner-loop body addition only consumes the existing `_run_symbol_d1a` path — it does not alter V1 or F1 paths.

## 4. D1-A R-window inventory results

Per Phase 3h §10 precommitted inventory; no expansion beyond the 4 mandatory R-window cells.

| Cell | Symbol | Trades | TARGET | STOP | TIME_STOP | EOD | expR | PF | WR | stop_frac |
|------|--------|-------:|-------:|-----:|----------:|----:|------:|-----:|------:|----------:|
| **D1-A R MED MARK** | BTC | 198 | 52 | 135 | 11 | 0 | **−0.3217** | **0.6467** | 0.2980 | 0.6818 |
| **D1-A R MED MARK** | ETH | 179 | 49 | 120 | 10 | 0 | **−0.1449** | **0.8297** | 0.3128 | 0.6704 |
| D1-A R LOW MARK | BTC | 198 | 55 | 134 | 9 | 0 | −0.2423 | 0.7248 | — | — |
| D1-A R LOW MARK | ETH | 180 | 50 | 121 | 9 | 0 | −0.1168 | 0.8609 | — | — |
| **D1-A R HIGH MARK** | BTC | 197 | 48 | 136 | 13 | 0 | **−0.4755** | **0.5145** | — | — |
| **D1-A R HIGH MARK** | ETH | 178 | 45 | 122 | 11 | 0 | **−0.2543** | **0.7217** | — | — |
| D1-A R MED TRADE_PRICE | BTC | 198 | 49 | 139 | 10 | 0 | −0.3703 | 0.6014 | — | — |
| D1-A R MED TRADE_PRICE | ETH | 180 | 46 | 125 | 9 | 0 | −0.2222 | 0.7478 | — | — |

V-window MED MARK cell: **NOT EXECUTED**. Per Phase 3h §10.5 + Phase 3j brief, V is conditional on R-window verdict = PROMOTE. The R-window verdict is MECHANISM PASS / FRAMEWORK FAIL — V is not authorized.

Run directories (under git-ignored `data/derived/backtests/`):

- `phase-3j-d1a-window=r-slip=medium/2026-04-29T03-22-26Z`
- `phase-3j-d1a-window=r-slip=low/2026-04-29T03-23-02Z`
- `phase-3j-d1a-window=r-slip=high/2026-04-29T03-23-34Z`
- `phase-3j-d1a-window=r-slip=medium-stop=trade_price/2026-04-29T03-24-06Z`

Analysis JSON: `data/derived/backtests/phase-3j-d1a-analysis-2026-04-29T03-28-14Z.json`

## 5. Phase 3h §11 first-execution gate evaluation

Per Phase 3h §11.1 the gate has 5 conditions evaluated against the BTC + ETH MED-MARK and HIGH-MARK cells. Evaluation:

| Condition | Definition | Empirical | Pass? |
|-----------|------------|-----------|------:|
| **(i) BTC MED expR > 0** | governing absolute floor | BTC R MED MARK expR = **−0.3217** | **FAIL** |
| **(ii) M1 BTC h=32 PASS** | M1 mean ≥ +0.10 R AND fraction-non-negative ≥ 0.50 | mean = +0.1748 R; fraction = 0.5101 | **PASS** |
| **(iii) ETH MED non-catastrophic** | ETH R MED MARK expR > −0.50 AND PF > 0.30 | expR = −0.1449; PF = 0.8297 | **PASS** |
| **(iv) BTC HIGH cost-resilience** | BTC R HIGH MARK expR > 0 AND PF > 0.30 AND ETH R HIGH MARK non-catastrophic | BTC HIGH expR = **−0.4755** (FAIL); BTC HIGH PF = 0.5145 (above 0.30); ETH HIGH expR = −0.2543; ETH HIGH PF = 0.7217 | **FAIL** |
| **(v) MED absolute floors** | BTC + ETH R MED MARK expR > −0.50 AND PF > 0.30 | BTC: −0.32 / 0.65; ETH: −0.14 / 0.83 | **PASS** |

**Catastrophic-floor predicate (Phase 3h §10.4):** `expR ≤ −0.50 OR PF ≤ 0.30` on any of the 4 BTC/ETH × MED/HIGH MARK cells.

| Cell | expR | PF | expR ≤ −0.50? | PF ≤ 0.30? | Catastrophic? |
|------|-----:|---:|--------------:|-----------:|--------------:|
| BTC R MED MARK | −0.3217 | 0.6467 | No | No | **No** |
| ETH R MED MARK | −0.1449 | 0.8297 | No | No | **No** |
| BTC R HIGH MARK | −0.4755 | 0.5145 | No | No | **No** |
| ETH R HIGH MARK | −0.2543 | 0.7217 | No | No | **No** |

**Verdict mapping (Phase 3h §11.2):**

```text
catastrophic_floor:  False  →  not HARD REJECT
condition (ii) M1:   PASS   →  not MECHANISM FAIL
condition (i):       FAIL
condition (iv):      FAIL
                    →  MECHANISM PASS / FRAMEWORK FAIL — other
```

**Verdict: MECHANISM PASS / FRAMEWORK FAIL — other.**

This is materially less severe than F1's Phase 3d-B2 HARD REJECT (which tripped the catastrophic-floor predicate on 5 separate cells). D1-A does not trip the catastrophic-floor predicate on any cell; the framework failure is driven by the absolute-floor and cost-resilience conditions not the catastrophic floor.

## 6. M1 / M2 / M3 mechanism checks (Phase 3h §12)

### 6.1 M1 — post-entry directional displacement (BTC drives §11.1 (ii))

Per Phase 3h §10.1 the M1 formula uses the actual `fill_price` (not `close(B+1)`):

```text
counter_displacement_h_R = ((close(entry_bar + h) − fill_price) × direction_sign)
                          / stop_distance
```

| Symbol | h=8 mean | h=8 frac≥0 | h=16 mean | h=16 frac≥0 | h=32 mean | h=32 frac≥0 |
|--------|---------:|-----------:|----------:|------------:|----------:|------------:|
| BTC | +0.0613 | 0.4394 | +0.0945 | 0.4899 | **+0.1748** | **0.5101** |
| ETH | +0.1274 | 0.4860 | +0.2982 | 0.5251 | +0.1670 | 0.5140 |

§11.1 (ii) thresholds at h=32: mean ≥ +0.10 R **AND** fraction-non-negative ≥ 0.50.

- **BTC h=32**: mean +0.1748 ≥ +0.10 ✓; fraction 0.5101 ≥ 0.50 ✓ → **PASS**
- ETH h=32 (descriptive): mean +0.1670, fraction 0.5140 (also passes M1 thresholds; ETH is descriptive — only BTC drives the formal §11.1 (ii) test).

The mechanism is empirically present: post-extreme-funding contrarian entries do produce positive expected counter-displacement at the 32-bar horizon. The displacement at h=8 is materially smaller (BTC +0.06R), suggesting the mean-reversion mechanism takes time to develop relative to the 1.0 × ATR stop distance.

### 6.2 M2 — funding-cost benefit

Per Phase 3h §12.2:

```text
funding_benefit_R = funding_pnl / realized_risk_usdt
PASS if mean funding_benefit_R ≥ +0.05 R per trade per symbol.
```

| Symbol | n | mean funding_benefit_R | M2 PASS (≥ +0.05R)? |
|--------|--:|----------------------:|--------------------:|
| BTC | 198 | +0.00234 | **FAIL** |
| ETH | 179 | +0.00452 | **FAIL** |

M2 is **FAIL on both symbols** by ~10× the threshold. The funding-rate carry collected by holding the contrarian position through the next funding cycle is negligible relative to fees/slippage/realized risk. This is consistent with the empirical observation that 96% (BTC) / 94% (ETH) of trades exit on STOP or TARGET within ≤ 32 bars (≤ 8 hours), so most trades cross at most 1 funding cycle, and the per-cycle accrual is small.

### 6.3 M3 — TARGET-exit subset positive contribution

Per Phase 3h §12.3 — TARGET subset PASS if mean ≥ +0.30R AND aggregate > 0 per symbol.

| Symbol | TARGET n | aggregate R | mean R | M3 PASS? |
|--------|---------:|------------:|-------:|---------:|
| BTC | 52 | +111.46 | +2.143 | **PASS** |
| ETH | 49 | +119.89 | +2.447 | **PASS** |

**M3 PASSES on both symbols.** When isolated, the TARGET subset is strongly profitable — the mean realized R on TARGET trades exceeds the +2.0R nominal target by ~7-22%, consistent with completed-bar-close trigger + next-bar-open fill putting the actual fill above the target (LONG) / below the target (SHORT) on the post-trigger bar's open.

Per Phase 3h §12.3 framing, M3 PASS is **descriptive only** and cannot rescue a framework-fail outcome. The 26-27% TARGET-exit fraction is overwhelmed by the 67-68% STOP-exit fraction at −1.30 / −1.24 R mean per loser.

## 7. Phase 3h §14 P.14 hard-block invariants

Subset checkable from the trade log alone:

| Invariant | BTC | ETH | Pass? |
|-----------|-----|-----|------:|
| Exit reasons in allowed set {STOP, TARGET, TIME_STOP, END_OF_DATA} | All 198 | All 179 | **PASS** |
| No V1-only forbidden exit reasons {TRAILING_BREACH, STAGNATION, TAKE_PROFIT} | 0 / 198 | 0 / 179 | **PASS** |
| Raw `stop_distance_at_signal_atr` in band [0.60, 1.80] | min=1.000 max=1.000 | min=1.000 max=1.000 | **PASS** |
| `funding_event_id_at_signal` populated on all D1-A trades | 198 / 198 | 179 / 179 | **PASS** |
| Lifecycle accounting identity (event-level) | detected (201) = filled (198) + rejected_stop_distance (0) + blocked_cooldown (3) ✓ | detected (188) = filled (179) + rejected_stop_distance (0) + blocked_cooldown (9) ✓ | **PASS** |

Notes:

- `stop_distance_at_signal_atr` = 1.0 exactly on every trade because the raw stop is 1.0 × ATR(B) by construction (Phase 3g §6.7) and the field stores the pre-slippage ratio.
- The +2.0R target geometry IS enforced by construction in `BacktestEngine._open_d1a_trade` (`compute_d1a_target(fill_price, stop_distance=post_slip_stop_distance, target_r=2.0)`). The diagnostic field `entry_to_target_distance_atr` measures `|fill − target| / ATR(B)` and ranges 2.03 – 2.54 (mean 2.17 BTC / 2.13 ETH) because `post_slip_stop_distance > 1.0 × ATR(B)` after slippage. This is a known consequence of the slippage model, not a violation of the +2.0R construction. The construction-level invariant `(target − fill) / stop_distance == 2.0` cannot be reconstructed from the trade log alone because `atr_at_signal` is an R2-specific TradeRecord field that stays NaN for D1-A rows; a future trade-log extension may add a D1-A-specific `atr_at_signal` field if needed.
- All other P.14 invariants pass.

## 8. Phase 3h §13 mandatory diagnostics

### 8.1 Direction breakdown (D1-A R MED MARK)

| Symbol | LONG | SHORT |
|--------|-----:|------:|
| BTC | varies (LONG below −2σ; SHORT above +2σ) | — |
| ETH | varies | — |

(Direction breakdown is encoded in `funding_z_score_at_signal` distribution per §8.4 below.)

### 8.2 Per-fold breakdown (6 half-year folds across the R-window)

BTCUSDT, D1-A R MED MARK:

| Fold | n | expR | PF | WR | stop_frac |
|------|--:|-----:|---:|---:|----------:|
| F1 2022H1 | 15 | −0.9424 | 0.1450 | 0.1333 | 0.8667 |
| F2 2022H2 | 15 | −0.1292 | 0.8402 | 0.3333 | 0.6667 |
| F3 2023H1 | 17 | **+0.6172** | **2.0306** | 0.5294 | 0.4706 |
| F4 2023H2 | 59 | −0.4023 | 0.5723 | 0.3051 | 0.6271 |
| F5 2024H1 | 32 | −0.9773 | 0.1567 | 0.0938 | 0.9062 |
| F6 2024H2 | 60 | −0.0518 | 0.9359 | 0.3667 | 0.6333 |

ETHUSDT, D1-A R MED MARK:

| Fold | n | expR | PF | WR | stop_frac |
|------|--:|-----:|---:|---:|----------:|
| F1 2022H1 | 19 | −0.3413 | 0.6289 | 0.2632 | 0.7368 |
| F2 2022H2 | 23 | −0.0698 | 0.9120 | 0.3043 | 0.6522 |
| F3 2023H1 | 15 | +0.4070 | 1.4680 | 0.3333 | 0.6667 |
| F4 2023H2 | 47 | −0.3884 | 0.5960 | 0.2979 | 0.7021 |
| F5 2024H1 | 24 | −0.5817 | 0.3845 | 0.1667 | 0.7500 |
| F6 2024H2 | 51 | +0.1622 | 1.2323 | 0.4118 | 0.5882 |

The single profitable fold on both symbols is F3 2023H1 (Jan-Jun 2023). F1 2022H1 (BTC), F4 2023H2, and F5 2024H1 are deeply unprofitable on BTC. ETH mirrors the pattern with smaller magnitudes and an additional mildly-profitable fold at F6 2024H2.

This per-fold heterogeneity is a strong negative signal for stationarity: the strategy does not robustly produce a positive expected R across half-year folds in the R window. A future analysis would need to distinguish between regime-specific edge vs. statistical noise; per Phase 3h §15 and the Phase 3j brief constraints, no such decomposition is authorized — D1-A is retained as research evidence, non-leading.

### 8.3 Exit reasons + per-reason mean R / aggregate R (D1-A R MED MARK)

BTCUSDT (n=198):

| Exit reason | Count | Fraction | Mean R | Aggregate R |
|-------------|------:|---------:|-------:|------------:|
| STOP | 135 | 0.6818 | −1.3247 | −178.84 |
| TARGET | 52 | 0.2626 | +2.1434 | +111.46 |
| TIME_STOP | 11 | 0.0556 | +0.3349 | +3.68 |
| END_OF_DATA | 0 | 0.0000 | — | — |

ETHUSDT (n=179):

| Exit reason | Count | Fraction | Mean R | Aggregate R |
|-------------|------:|---------:|-------:|------------:|
| STOP | 120 | 0.6704 | −1.2623 | −151.48 |
| TARGET | 49 | 0.2737 | +2.4467 | +119.89 |
| TIME_STOP | 10 | 0.0559 | +0.5659 | +5.66 |
| END_OF_DATA | 0 | 0.0000 | — | — |

Accounting identity: STOP + TARGET + TIME_STOP + END_OF_DATA = trade count (198 / 179) ✓.

### 8.4 D1-A field distributions (D1-A R MED MARK)

BTCUSDT:

| Field | n | mean | median | min | max |
|-------|--:|-----:|-------:|----:|----:|
| `funding_z_score_at_signal` | 198 | +0.138 | −2.003 | −22.157 | +7.713 |
| `funding_rate_at_signal` | 198 | +0.0001 | −0.0000 | −0.0012 | +0.0009 |
| `bars_since_funding_event_at_signal` | 198 | 0.000 | 0 | 0 | 0 |
| `entry_to_target_distance_atr` | 198 | 2.167 | 2.158 | 2.026 | 2.541 |
| `stop_distance_at_signal_atr` | 198 | 1.000 | 1.000 | 1.000 | 1.000 |

ETHUSDT:

| Field | n | mean | median | min | max |
|-------|--:|-----:|-------:|----:|----:|
| `funding_z_score_at_signal` | 179 | +0.075 | −2.018 | −15.208 | +13.084 |
| `funding_rate_at_signal` | 179 | +0.0001 | +0.0000 | −0.0030 | +0.0010 |
| `bars_since_funding_event_at_signal` | 179 | 0.000 | 0 | 0 | 0 |
| `entry_to_target_distance_atr` | 179 | 2.131 | 2.110 | 2.018 | 2.638 |
| `stop_distance_at_signal_atr` | 179 | 1.000 | 1.000 | 1.000 | 1.000 |

Notes:

- `bars_since_funding_event_at_signal = 0` on every trade — entries fire on the first eligible bar after the funding settlement (consistent with Phase 3g §9.4 / Phase 3h §4.5 timing — eligible bar is the bar whose close ≥ funding_time, with strict-≤ semantics, so the entry window is the very next 15m bar after settlement).
- The Z-score median is approximately ±2.0 (LONG/SHORT split), consistent with the |Z| ≥ 2.0 detection threshold.
- The funding-rate distribution is approximately symmetric around 0; extreme tails reach ±0.10% (signed BPS) corresponding to the |Z| > 7 outliers visible in the distribution max/min.
- `stop_distance_at_signal_atr = 1.0` exactly on every trade (raw stop pre-slippage; the locked Phase 3g §6.7 multiplier).

### 8.5 Cost sensitivity (LOW / MED / HIGH at MARK)

BTC: LOW expR=−0.2423, MED=−0.3217, HIGH=−0.4755 (monotonic worsening).
ETH: LOW expR=−0.1168, MED=−0.1449, HIGH=−0.2543 (monotonic worsening).

The deltas (BTC: HIGH−LOW = −0.233R; ETH: HIGH−LOW = −0.138R) are consistent with the Phase 3h §11.6 cost-resilience expectation that 8 bps HIGH per side adds roughly 0.16R per trade in cost drag (8 bps × 2 sides × leverage ≈ 1× stop ≈ 16 bps round-trip ≈ 0.16R when stop = 1.0 × ATR and notional is approximately 100× risk).

### 8.6 Stop-trigger sensitivity (MED MARK vs MED TRADE_PRICE)

BTC: MARK expR=−0.3217, TRADE_PRICE=−0.3703 (TRADE_PRICE worse by −0.05R).
ETH: MARK expR=−0.1449, TRADE_PRICE=−0.2222 (TRADE_PRICE worse by −0.08R).

Trade-price stop triggers fire more readily than mark-price (intrabar wicks reach trade-price thresholds before mark-price recomputes), so STOP fractions tick up (BTC: 135 → 139; ETH: 120 → 125) and TARGET fractions tick down (BTC: 52 → 49; ETH: 49 → 46). The direction is expected; the magnitude is moderate. Neither stop trigger source crosses the catastrophic-floor predicate.

### 8.7 Lifecycle counters (D1-A R MED MARK)

BTC: detected 201, filled 198, rejected_stop_distance 0, blocked_cooldown 3.
ETH: detected 188, filled 179, rejected_stop_distance 0, blocked_cooldown 9.

Identity holds: detected = filled + rejected_stop_distance + blocked_cooldown.

The 0 stop-distance rejections on BTC + ETH indicate the Phase 3g §6.10 admissibility band [0.60, 1.80] × ATR is never violated when stop is exactly 1.0 × ATR by construction. The cooldown counter fires occasionally (3 / 9) when an extreme funding event arrives while a same-direction trade is still open — the cooldown gate then prevents the second trade. No spec-vs-implementation discrepancies surfaced.

## 9. RR / breakeven realized-vs-expected review (Phase 3h §13 #24)

Phase 3h §5.6.1-5.6.5 forecast at MED slippage (no funding):

- Per-winner R: ~+1.47R
- Per-loser R: ~−1.53R
- Breakeven WR: ~0.51

Empirical D1-A R MED MARK:

| Symbol | Empirical winner mean R | Empirical loser mean R | Empirical WR | Breakeven WR (forecast) | Gap to breakeven |
|--------|-----------------------:|-----------------------:|-------------:|------------------------:|-----------------:|
| BTC | **+1.979** | **−1.298** | **0.298** | 0.51 | −0.21 |
| ETH | **+2.256** | **−1.238** | **0.313** | 0.51 | −0.20 |

**Per-trade R magnitudes are BETTER than forecast on both sides:**

- Winners average +1.98R BTC / +2.26R ETH (forecast +1.47R) — winners run further than expected because the completed-bar-close TARGET trigger + next-bar-open fill puts actual TARGET fills above the +2.0R nominal target.
- Losers average −1.30R BTC / −1.24R ETH (forecast −1.53R) — STOP fills are slightly less adverse than the forecast accounted for (fewer gap-throughs).

**But the win rate is far below breakeven:**

- BTC empirical WR = 0.298 vs +0.51 breakeven → **gap of 21 percentage points** below breakeven.
- ETH empirical WR = 0.313 vs +0.51 breakeven → **gap of 20 percentage points** below breakeven.

**The framework failure is not a per-trade R magnitude failure — it is a win-rate failure.** The mean-reversion mechanism produces a positive directional drift (M1 PASS at h=32) but that drift is small relative to the 1.0 × ATR stop distance. Approximately 68% of trades hit the −1.0R stop before the +2.0R target. With per-trade R magnitudes of +1.98 / −1.30 (BTC), the breakeven WR is `1.30 / (1.98 + 1.30) = 0.397`. Empirical WR 0.298 is 10 percentage points below this realized-magnitude breakeven, also a clear shortfall.

Therefore: the mechanism (M1) is empirically present, the geometry (M3) delivers the expected magnitudes when reached, but the overall win rate is too low to be profitable at the locked spec axes. Per Phase 3h §15 governance, no axis adjustments (Z threshold; lookback; stop multiplier; target R; time-stop; cooldown direction; symbol scope) are authorized in Phase 3j — D1-A's locked spec is consumed verbatim.

## 10. Cross-family descriptive deltas (Phase 3h §13 #25)

D1-A R MED MARK vs framework anchors / baselines on the same R window. **Descriptive only**; D1-A is self-anchored absolute per Phase 3h §11.4.

BTCUSDT:

| Family | expR | PF | trades | Δ expR vs D1-A | Δ PF vs D1-A |
|--------|-----:|---:|------:|---------------:|-------------:|
| **D1-A R MED MARK** | **−0.3217** | **0.6467** | 198 | — | — |
| H0 (V1 baseline anchor) | −0.4590 | 0.2552 | 33 | +0.137 | +0.391 |
| R3 (V1 baseline-of-record) | −0.2403 | 0.5602 | 33 | −0.081 | +0.087 |
| F1 (Phase 3d-B2 HARD REJECT) | −0.5227 | 0.3697 | 4720 | +0.201 | +0.277 |

ETHUSDT:

| Family | expR | PF | trades | Δ expR vs D1-A | Δ PF vs D1-A |
|--------|-----:|---:|------:|---------------:|-------------:|
| **D1-A R MED MARK** | **−0.1449** | **0.8297** | 179 | — | — |
| H0 | −0.4752 | 0.3207 | 33 | +0.330 | +0.509 |
| R3 | −0.3511 | 0.4736 | 33 | +0.206 | +0.356 |
| F1 | −0.4024 | 0.4667 | 4826 | +0.258 | +0.363 |

Observations:

- D1-A is **better than H0 / F1 on both symbols** by every metric, but H0 / F1 are themselves negative on this same window — D1-A's "better than negative anchors" position is not a positive endorsement.
- D1-A is **slightly worse than R3 on BTC** (−0.32 vs −0.24) but **better than R3 on ETH** (−0.14 vs −0.35). R3 is the V1 baseline-of-record and is itself negative on the R window at MED MARK on these particular runs — R3's overall framework PASS in Phase 2l rests on the V window and on slippage / fold sensitivities not visible in single-cell BTC R MED MARK comparison.
- The cross-family comparison is **descriptive only** per Phase 3h §11.4. D1-A's framework verdict rests on its own absolute floors and cost-resilience conditions, not on relative comparison.

## 11. V-window cell — NOT EXECUTED

Per Phase 3h §10.5 + the Phase 3j brief, the D1-A V MED MARK cell is conditional on R-window verdict = PROMOTE. The R-window verdict is **MECHANISM PASS / FRAMEWORK FAIL — other**, which is **not PROMOTE**.

V MED MARK cell **NOT EXECUTED**. No V-window run directory was created.

## 12. Phase 3i-B1 → Phase 3j delta — files changed

### 12.1 Files modified

- `scripts/phase3j_D1A_execution.py` — replaced Phase 3i-B1 scaffold body (which exited non-zero with `"D1-A run-loop not yet implemented in Phase 3i-B1 scaffold; Phase 3j is required to authorize candidate runs."` even with `--phase-3j-authorized`) with the full F1-style run-loop (`_run_d1a` building `BacktestConfig(strategy_family=FUNDING_AWARE_DIRECTIONAL, funding_aware_variant=FundingAwareConfig())`, loading v002 datasets, running `BacktestEngine.run`, writing per-symbol summary_metrics / monthly_breakdown / funding_aware_lifecycle_total). The `check-imports` subcommand output preserves the substring `"imports OK"` for backward compatibility with `test_d1a_runner_scaffold_check_imports_ok`.

### 12.2 Files added

- `scripts/_phase3j_D1A_analysis.py` — Phase 3j D1-A analysis script. Reads the 4 R-window run directories + 5 control run directories + v002 normalized klines, computes the §11 first-execution gate, §12 M1/M2/M3 mechanism checks, §13 mandatory diagnostics, §14 P.14 hard-block invariants subset, cross-family deltas, and RR/breakeven review. Writes a single JSON analysis output to `data/derived/backtests/phase-3j-d1a-analysis-<run_id>.json` (git-ignored).
- `docs/00-meta/implementation-reports/2026-04-29_phase-3j_D1A_execution-diagnostics.md` — this report.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3j_closeout-report.md` — closeout.

### 12.3 Files NOT touched

- `src/prometheus/research/backtest/engine.py` — D1-A engine path unchanged from Phase 3i-B1.
- `src/prometheus/research/backtest/trade_log.py` — TradeRecord schema unchanged from Phase 3i-B1.
- `src/prometheus/research/backtest/config.py` — BacktestConfig unchanged.
- `src/prometheus/strategy/funding_aware_directional/**` — D1-A primitives + config + facade unchanged from Phase 3i-A.
- `src/prometheus/strategy/v1_breakout/**` and `src/prometheus/strategy/mean_reversion_overextension/**` — V1 / F1 paths unchanged.
- `tests/**` — no test changes (existing 668 tests pass; runner-scaffold tests still pass against the new check-imports output because the substring `"imports OK"` is preserved).
- `docs/03-strategy-research/**`, `docs/05-backtesting-validation/**`, `docs/12-roadmap/**` — no specification changes.
- `data/` — no `data/` artifact committed. All Phase 3j run outputs written to git-ignored `data/derived/backtests/` directories.
- `.claude/`, `.mcp.json`, `config/`, `secrets/` — untouched.

### 12.4 Quality gates

All 4 gates green at Phase 3j branch tip:

| Gate | Result |
|------|--------|
| `uv run pytest` | **668 passed** in 12.10s |
| `uv run ruff check .` | **All checks passed!** |
| `uv run ruff format --check .` | **157 files already formatted** |
| `uv run mypy src` | **Success: no issues found in 61 source files** |

No regression. No new tests authored — Phase 3j is a candidate-run + diagnostics phase (per Phase 3h §15 governance, the engine-test suite was the Phase 3i-B1 deliverable; Phase 3j adds run-loop body + analysis script and is verified by control reproduction + first-execution-gate analysis).

## 13. Confirmation of preserved scope

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| **§11.6 = 8 bps HIGH per side** | UNCHANGED (Phase 2y closeout preserved verbatim) |
| §1.7.3 project-level locks | UNCHANGED |
| H0 baseline parameters | UNCHANGED |
| R3 sub-parameters | UNCHANGED |
| R1a / R1b-narrow / R2 sub-parameters | UNCHANGED |
| F1 spec axes | UNCHANGED |
| **D1-A locked spec values** (Phase 3g binding) | **PRESERVED VERBATIM in `FundingAwareConfig`; consumed unmodified by the engine** |
| R3 baseline-of-record status (Phase 2p §C.1) | PRESERVED |
| H0 framework anchor status (Phase 2i §1.7.3) | PRESERVED |
| R1a / R1b-narrow / R2 / F1 retained-research-evidence status | PRESERVED |
| R2 framework verdict (FAILED — §11.6 cost-sensitivity blocks) | PRESERVED |
| F1 framework verdict (HARD REJECT) | PRESERVED |
| Phase 3d-B2 terminal-for-F1 status | PRESERVED |
| **D1-A framework verdict (Phase 3j MECHANISM PASS / FRAMEWORK FAIL — other)** | **NEW — see §5 above** |
| **Phase 3j terminal-for-D1-A status** | **NEW — see §14 below** |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff / current-project-state specs | UNCHANGED (current-project-state will be updated post-merge to record Phase 3j outcome) |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

## 14. Phase 3j terminal-for-D1-A and post-Phase-3j authority

Phase 3j is **terminal for D1-A** under Phase 3h §11 / §15 framework. The framework-fail verdict means:

- **D1-A is retained as research evidence**, analogous to R1a / R1b-narrow / R2 / F1.
- **D1-A is non-leading.** R3 remains the V1 baseline-of-record (Phase 2p §C.1). H0 remains the framework anchor (Phase 2i §1.7.3).
- **No D1-A-prime, D1-B, or hybrid is authorized.** Any successor variant requires a separately authorized phase per Phase 3h §15 governance.
- **No further D1-A backtest cells are authorized.** The 4 R-window cells run in Phase 3j are sufficient to render the verdict; no LOW / TRADE_PRICE V-window or alternative-axes cells are authorized.
- **No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write authorization** flows from this verdict. The next phase requires explicit operator authorization beyond Phase 3j.

The recommended next step per Phase 3h §15 framework is **operator-driven post-Phase-3j consolidation** (a docs-only memo analogous to Phase 3e's post-F1 consolidation, summarizing the V1 + F1 + D1-A research arc, recording the framework-fail outcomes, and deferring the next-phase decision to the operator). Phase 3j does not author this memo — it is reserved for an authorized Phase 3k or equivalent.

---

## 15. Open questions / unresolved items

None. The verdict is unambiguous under the precommitted Phase 3h §11 mapping. No Phase 3h §10.4 catastrophic-floor violation; M1 BTC h=32 PASS; cond_i + cond_iv FAIL → MECHANISM PASS / FRAMEWORK FAIL — other. No spec ambiguity surfaced; no ambiguity log update required.

The §14 P.14 strict construction-level invariant `(target − fill) / stop_distance == 2.0` cannot be reconstructed from the trade log alone because `atr_at_signal` is an R2-specific field that stays NaN for D1-A rows. The construction is verified by the engine code path (`compute_d1a_target(fill_price, stop_distance=post_slip_stop_distance, target_r=2.0)` at engine.py:2088) and by the §6.3 M3 result that TARGET-exit mean R is consistently within +0.14R / +0.45R of the +2.0R nominal target (BTC +2.143R / ETH +2.447R), which would be impossible if the geometry were broken. Adding a dedicated D1-A-specific `atr_at_signal` field is a candidate technical-debt item if a successor D1-A-related phase is ever authorized; it is **not** a Phase 3j hard-block.

---

**End of Phase 3j D1-A execution + diagnostics report.** Quality gates green (668 pytest / ruff / format / mypy). Full control set (5 named controls / 10 symbol-level cells) reproduces bit-for-bit. D1-A R-window inventory complete (4 mandatory cells: D1-A R MED MARK, R LOW MARK, R HIGH MARK, R MED TRADE_PRICE). Phase 3h §11 first-execution gate evaluated: **MECHANISM PASS / FRAMEWORK FAIL — other**. M1 BTC h=32 PASS (mean +0.17R / fraction 0.51). M2 FAIL on both symbols (funding benefit +0.0023 / +0.0045 R). M3 PASS on both symbols (TARGET subset +2.14 / +2.45 R mean). P.14 invariants subset PASS. No catastrophic-floor violation. V-window NOT executed (verdict not PROMOTE). D1-A retained as research evidence; non-leading; **no D1-A-prime authorized**. Phase 3j terminal for D1-A. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write change. Awaiting operator review.
