# Phase 4p — G1 Strategy Spec Memo

**Authority:** Operator authorization for Phase 4p (Phase 4o §"Operator
decision menu" Option A primary recommendation: Phase 4p — G1 Strategy
Spec Memo, docs-only). Phase 4o (G1 hypothesis-spec memo); Phase 4n
(Candidate B selected as primary fresh-hypothesis direction); Phase
4m §"Fresh-hypothesis validity gate" (18 binding requirements);
Phase 4m §"Forbidden rescue observations"; Phase 4l (V2 backtest
execution Verdict C HARD REJECT — terminal for V2 first-spec); Phase
4k (V2 backtest-plan methodology binding); Phase 4j §11 (metrics
OI-subset partial-eligibility binding rule); Phase 4i (V2
acquisition + integrity validation; partial pass); Phase 4h (V2
data-requirements / feasibility); Phase 4g (V2 strategy spec); Phase
4f (V2 hypothesis predeclaration); Phase 3v §8 (stop-trigger-domain
governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope /
stagnation governance); Phase 3r §8 (mark-price gap governance);
Phase 3t §12 (validity gate); Phase 3m (regime-first research
framework memo precedent); Phase 3c §7.3 (catastrophic-floor
predicate); Phase 2w §16.1 (R2 §11.6 cost-sensitivity FAIL); Phase
2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level
locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`;
`docs/03-strategy-research/v1-breakout-backtest-plan.md`;
`docs/05-backtesting-validation/v1-breakout-validation-checklist.md`;
`docs/04-data/data-requirements.md`;
`docs/04-data/timestamp-policy.md`;
`docs/04-data/dataset-versioning.md`;
`docs/07-risk/stop-loss-policy.md`;
`docs/07-risk/position-sizing-framework.md`;
`docs/07-risk/exposure-limits.md`;
`docs/12-roadmap/phase-gates.md`;
`docs/12-roadmap/technical-debt-register.md`;
`docs/00-meta/ai-coding-handoff.md`;
`docs/00-meta/implementation-ambiguity-log.md`;
`.claude/rules/prometheus-core.md`;
`.claude/rules/prometheus-safety.md`;
`.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4p — **G1 Strategy Spec Memo** (docs-only). Defines the
exact ex-ante G1 — Regime-First Breakout Continuation strategy
specification from the Phase 4o hypothesis-spec layer. **Phase 4p
does NOT run a backtest, run diagnostics, acquire data, modify
data, modify manifests, write implementation code, modify
`src/prometheus/`, modify tests, modify scripts, create a runnable
strategy, create V3 implementation, or authorize paper / shadow /
live / exchange-write.** **Phase 4p is text-only.**

**Branch:** `phase-4p/g1-strategy-spec-memo`. **Memo date:**
2026-05-02 UTC.

---

## Summary

Phase 4p translates Phase 4o's G1 conceptual hypothesis-spec into
a complete ex-ante strategy specification. Phase 4p commits, before
any backtest is run or any data is touched, every methodological
choice that a future backtest-plan / backtest-execution phase would
be required to honor:

- **Strategy name:** G1 — Regime-First Breakout Continuation
  (preserved verbatim from Phase 4o).
- **Data inputs:** existing v002 BTCUSDT / ETHUSDT 15m + 1h-derived
  klines + Phase 4i 30m / 4h klines + v002 funding manifests; **no
  Phase 4q data-requirements memo required** before the future
  backtest-plan memo.
- **Timeframes:** regime classifier primary timeframe = **4h**;
  regime persistence support = **1h**; signal timeframe = **30m**;
  next-30m-bar-open execution.
- **Regime state machine:** 4 states (`regime_inactive`,
  `regime_candidate`, `regime_active`, `regime_cooldown`) with
  exact transition rules using prior-completed bars only.
- **Regime classifier:** composite top-level state machine that
  consumes (a) HTF trend condition (4h EMA(20)/(50) discrete
  comparison + slope-rising); (b) trend persistence (4h directional
  efficiency over last 12 completed 4h bars; ≥ E_min); (c)
  volatility regime (30m ATR(20) rolling 480-bar percentile in band
  [P_atr_low, P_atr_high]); (d) liquidity adequacy (30m volume
  vs. rolling 480-bar median ≥ V_liq_min); (e) funding pathology
  (v002 funding percentile over trailing 90 events outside band
  [P_fund_low, P_fund_high]).
- **Inside-regime breakout setup:** 30m signal; long breakout =
  completed 30m close > prior N_breakout-bar high + B_atr × ATR(20)
  (excluding current bar); short = mirror; **N_breakout = 12** and
  **B_atr = 0.10** chosen from first principles for the 30m
  timeframe inside the active-regime distribution.
- **Structural stop:** N_stop = 12 (matched to N_breakout for
  setup-stop coherence); S_buffer = 0.10 × ATR(20). Stop-distance
  quality bounds are **derived from active-regime ATR distribution**
  (not V1's 0.60–1.80 × ATR): minimum 0.50 × ATR(20), maximum 2.20 ×
  ATR(20) — both justified inside the spec from active-regime
  structure analysis.
- **Target model:** fixed-R take-profit; **N_R ∈ {2.0, 2.5}** (2-
  variant axis). No break-even. No trailing stop. Same-bar
  ambiguity = stop-first conservative.
- **Time-stop:** **T_stop ∈ {12, 16}** completed 30m bars (= 6h or
  8h). Position-vs-regime: **Option A** (position lifecycle
  independent of regime; degradation does NOT force exit).
- **Position sizing:** 0.25% risk per trade; 2× leverage cap; one
  position max (§1.7.3 preserved verbatim).
- **Cost model:** §11.6 = 8 bps slippage per side preserved;
  LOW = 1 bp / MEDIUM = 4 bps / HIGH = 8 bps cells; taker fee =
  4 bps per side; funding cost included in P&L.
- **Threshold grid:** **32 variants** (= 2^5) over 5 binary axes —
  small enough to keep PBO / DSR / CSCV computation tractable and
  deflated-Sharpe-correction-clean (Phase 4k Option B preserved at
  smaller scale; Phase 4g §29's 512-variant overbreadth explicitly
  avoided).
- **Mechanism-check thresholds (M1 / M2 / M3 / M4):** M1 active >
  inactive by ≥ +0.10R mean_R, bootstrap 95% CI lower bound > 0;
  M2 G1 > always-active baseline by ≥ +0.05R mean_R under HIGH
  cost, bootstrap 95% CI lower bound > 0; M3 BTC OOS HIGH mean_R >
  0 AND trade_count ≥ 30 AND no CFP-1 / CFP-2 / CFP-3 trigger; M4
  ETH mean_R differential non-negative AND mechanism directionally
  consistent.
- **Catastrophic-floor predicates:** 12 predicates adapted from
  Phase 4k with G1-specific thresholds.
- **Validation windows:** train 2022-01-01..2023-06-30 UTC;
  validation 2023-07-01..2024-06-30 UTC; OOS holdout
  2024-07-01..2026-03-31 UTC (reused from Phase 4k methodology).
- **BTCUSDT primary; ETHUSDT comparison only;** ETH cannot rescue
  BTC.

**Phase 4p is the strategy-spec layer.** The future Phase 4q —
G1 Backtest-Plan Memo (docs-only) would predeclare the backtest
methodology / variant ordering / execution model / reporting tables
/ stop conditions, analogous to how Phase 4k did for V2.

**Phase 4p does NOT:**

- run a backtest;
- implement G1 in `src/prometheus/`;
- acquire or modify data;
- modify manifests;
- create paper / shadow / live runtime;
- authorize exchange-write capability;
- revise prior verdicts;
- change project locks;
- authorize Phase 4q.

**Phase 4p IS:** the precise specification a future Phase 4q
backtest-plan memo and a future Phase 4r execution phase (if both
are ever authorized) would be required to honor verbatim.

**Verification:**

- `ruff check .`: All checks passed.
- `pytest`: 785 passed.
- `mypy --strict src/prometheus`: Success: no issues found in 82
  source files.

**No project lock changed.** **No retained verdict revised.**

**Recommended next operator choice:** **Option A (PRIMARY) — Phase
4q G1 Backtest-Plan Memo (docs-only).** Conditional secondary:
remain paused.

**Phase 4 canonical remains unauthorized.** **Phase 4q / any
successor phase remains unauthorized.** **Paper / shadow,
live-readiness, deployment, production keys, authenticated APIs,
private endpoints, user stream, WebSocket, MCP, Graphify,
`.mcp.json`, credentials, and exchange-write all remain
unauthorized.**

**Recommended state remains paused outside conditional Phase 4q.
No next phase authorized by Phase 4p.**

---

## Authority and boundary

Phase 4p operates strictly inside the post-Phase-4o-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10;
  Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t
  consolidation; Phase 3t §12 validity gate; Phase 3u §10 / §11;
  Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4a's anti-live-readiness
  statement; Phase 4d review; Phase 4e reconciliation-model design
  memo; Phase 4f V2 hypothesis predeclaration; Phase 4g V2 strategy
  spec; Phase 4h V2 data-requirements / feasibility memo; Phase 4i
  V2 acquisition + integrity validation; Phase 4j §11 metrics
  OI-subset partial-eligibility rule; Phase 4k V2 backtest-plan
  methodology; Phase 4l V2 backtest execution Verdict C HARD REJECT;
  Phase 4m post-V2 strategy research consolidation memo +
  18-requirement fresh-hypothesis validity gate; Phase 4n fresh-
  hypothesis discovery memo (Candidate B selected); Phase 4o G1
  hypothesis-spec memo (G1 conceptual layer + 6 binding regime-first
  principles + classifier constraints).
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md`
  unchanged.
- **Project-level locks preserved verbatim.** §1.7.3.
- **Phase 2f thresholds preserved verbatim.** §11.6 = 8 bps HIGH
  per side.
- **Retained-evidence verdicts preserved verbatim.** R3 / H0 / R1a /
  R1b-narrow / R2 / F1 / D1-A / V2.
- **Safety rules preserved verbatim.**
- **MCP and secrets rules preserved verbatim.**

Phase 4p adds *only* a docs-only strategy-spec memo, without
modifying any prior phase memo, any data, any code under
`src/prometheus/`, any rule, any threshold, any manifest, any verdict,
any lock, or any gate.

---

## Starting state

```text
branch:           phase-4p/g1-strategy-spec-memo
parent commit:    74eda85d8b3ae55c7944de2d883eeece0f24da65 (post-Phase-4o-merge housekeeping)
working tree:     clean before memo authoring (transient .claude/scheduled_tasks.lock + gitignored data/research/ excluded)
main:             74eda85d8b3ae55c7944de2d883eeece0f24da65 (unchanged)

Phase 4a foundation:                                          merged.
Phase 4b/4c cleanup:                                          merged.
Phase 4d review:                                              merged.
Phase 4e reconciliation-model design memo:                    merged.
Phase 4f V2 hypothesis predeclaration:                        merged.
Phase 4g V2 strategy spec:                                    merged.
Phase 4h V2 data-requirements / feasibility memo:             merged.
Phase 4i V2 public data acquisition + integrity:              merged (partial-pass).
Phase 4j V2 metrics data governance memo:                     merged (Phase 4j §11 binding).
Phase 4k V2 backtest-plan memo:                               merged.
Phase 4l V2 backtest execution:                               merged (Verdict C HARD REJECT).
Phase 4m post-V2 strategy research consolidation memo:        merged.
Phase 4n fresh-hypothesis discovery memo:                     merged (Candidate B selected).
Phase 4o G1 regime-first breakout hypothesis-spec memo:       merged.

Repository quality gate:           fully clean.
research thread (5m):              operationally complete and closed (Phase 3t).
v002 datasets:                     locked; manifests untouched.
v001-of-5m datasets:               trade-price research-eligible; mark-price research_eligible:false.
Phase 4i datasets:                 30m + 4h klines × 2 research-eligible; metrics × 2 NOT research-eligible.
```

---

## Relationship to Phase 4o

- **Phase 4o predeclared G1 as a hypothesis-spec.** Hypothesis name,
  6 binding regime-first principles, 4-state regime state machine
  (states + purposes only, no threshold), classifier constraints
  (allowed dimensions + forbidden inputs + 5 binding rules),
  candidate dimensions (qualitatively evaluated), inside-regime
  breakout concept (no concrete entry rules), co-design principles,
  cost-sensitivity argument (§11.6 preserved), data-readiness
  assessment, M1 / M2 / M3 / M4 mechanism-check framework
  (conceptual), 12 catastrophic-floor predicates (conceptual),
  forbidden rescue interpretations.
- **Phase 4o did not define a full strategy spec.** Final regime
  classifier formula, regime state-machine transition thresholds,
  signal timeframe / HTF timeframe choices, inside-regime breakout
  setup geometry, stop / target / sizing thresholds, threshold grid,
  exact data requirements, exact mechanism-check pass thresholds,
  and exact pass / fail gate numerical bounds were all explicitly
  deferred to Phase 4p.
- **Phase 4o recommended Phase 4p as primary.** Conditional
  secondary was remain paused.
- **The operator now authorizes Phase 4p.**
- **Phase 4p must remain docs-only.**
- **Phase 4p must not run a backtest, acquire data, or implement
  code.**

**Phase 4o adoption preserved verbatim by Phase 4p:**

- Strategy name: G1 — Regime-First Breakout Continuation.
- Six binding regime-first principles.
- 4-state regime state machine concept.
- Allowed and forbidden classifier dimensions.
- Inside-regime co-design constraints.
- Forbidden default inheritance list.
- Position sizing locks.
- §11.6 = 8 bps HIGH per side.
- M1 / M2 / M3 / M4 mechanism-check framework.
- Negative-test framework.
- 12 catastrophic-floor predicates.

---

## Strategy name

**G1 — Regime-First Breakout Continuation.**

Preserved verbatim from Phase 4o §"Hypothesis name". The "G1"
prefix denotes a new strategy generation distinct from the V-family
(V1 / V2). The "1" indicates it is the first regime-first hypothesis;
future regime-first variants would be G2, G3, etc., subject to
separate operator authorization.

**Forbidden alternative names (preserved verbatim from Phase 4o):**

- V3 (V2 successor implied);
- V2-prime;
- R3-prime;
- R1c;
- R1a-extension;
- R1b-extension;
- any name implying direct rescue.

---

## Strategy thesis

G1 — Regime-First Breakout Continuation hypothesizes that:

> Trend-continuation breakouts on BTCUSDT perpetual futures have
> qualitatively different risk-adjusted outcomes inside vs. outside
> a predeclared favorable regime. **Inside a confirmed favorable
> regime** — defined as: an upward (or downward) HTF trend with
> sufficient persistence; volatility in a non-pathological band;
> adequate liquidity at signal time; non-pathological funding
> context — **breakout entries** with structurally co-designed
> stop / target / sizing produce positive expectancy that survives
> §11.6 HIGH cost. **Outside the favorable regime** — when one or
> more of trend / persistence / volatility / liquidity / funding
> conditions degrade — **the strategy is completely inactive** and
> generates no candidate signals.

The thesis is testable: M1 (active vs. inactive comparison) is the
primary validity test. If the regime classifier doesn't sort
outcomes meaningfully — i.e., if inactive-regime breakouts perform
equally well or better than active-regime breakouts — the thesis
fails.

The thesis is **structurally distinct** from prior Prometheus
strategies because regime gating is implemented as a **top-level
state machine** that determines whether to even evaluate breakout
conditions, not as a per-bar AND filter on top of an always-active
breakout signal.

---

## Why this is not a rescue

The most common rescue trap for Candidate B (per Phase 4n / Phase 4o)
is "R1a / R1b-narrow but with another bolt-on regime filter". Phase
4p's design is structurally distinct from this trap on multiple
levels:

- **State-machine gating, not per-bar filtering.** R1a evaluates
  every signal bar's volatility-percentile filter; R1b-narrow
  evaluates every signal bar's bias-strength threshold. G1 evaluates
  the regime classifier at the **strategy-active vs. strategy-inactive**
  level; outside `regime_active` the strategy doesn't compute a
  signal at all.
- **Composite classifier with explicit confirmation.** R1a / R1b-
  narrow use a single per-bar predicate. G1's classifier is a
  composite (trend + persistence + volatility + liquidity + funding
  context) that requires confirmation persistence
  (`regime_candidate` → `regime_active` only after K_confirm
  completed bars).
- **No V1 / V2 setup geometry inheritance.** Phase 4p chooses
  N_breakout = 12 (not V1's 8 or V2's 20/40), B_atr = 0.10 (V1
  buffer matched but rationalized for 30m timeframe), and
  stop-distance bounds derived from the active-regime ATR
  distribution rather than from V1's 0.60–1.80 × ATR.
- **No 5m diagnostic findings as features or thresholds.** Phase 3o
  §6 forbidden question forms preserved.
- **No Phase 4l forensic numbers.** V2's observed 3-5 × ATR
  stop-distance distribution does NOT inform G1's bounds; G1's
  bounds come from active-regime 30m ATR percentile analysis from
  first principles.

Phase 4p's specification is therefore **G1**, not "R1a-prime" or
"V2-prime" or "R3-prime" or any other rescue label.

---

## Preserved verdicts and locks

Phase 4p preserves verbatim:

- **H0 remains FRAMEWORK ANCHOR** (Phase 2i §1.7.3).
- **R3 remains BASELINE-OF-RECORD** (Phase 2p §C.1).
- **R1a remains RETAINED — NON-LEADING.**
- **R1b-narrow remains RETAINED — NON-LEADING.**
- **R2 remains FAILED — §11.6** (Phase 2w §16.1).
- **F1 remains HARD REJECT** (Phase 3c §7.3 / Phase 3d-B2 terminal).
- **D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other** (Phase
  3h §11.2 / Phase 3j terminal).
- **5m thread remains CLOSED operationally** (Phase 3t).
- **V2 remains HARD REJECT — structural CFP-1 critical** (Phase 4l;
  terminal for V2 first-spec).
- **No verdict is revised.**
- **No project lock is changed.**
- **§11.6 HIGH cost remains 8 bps per side.**
- **§1.7.3 project-level locks remain unchanged** (BTCUSDT primary
  live; ETHUSDT research / comparison only; one position max; 0.25%
  risk; 2× leverage cap; mark-price stops; v002 verdict provenance).
- **Phase 4j §11 metrics OI-subset partial-eligibility rule remains
  binding.**
- **Phase 4k V2 backtest-plan methodology remains binding** for any
  future backtest pattern reuse.
- **Phase 3v §8 stop-trigger-domain governance remains binding.**
- **Phase 3w §6 / §7 / §8 governance remains binding.**
- **Phase 3r §8 mark-price gap governance remains binding.**

---

## Data requirements decision

**Phase 4p decision: No Phase 4q data-requirements memo required
before future backtest-plan memo.**

G1 reuses existing locally-acquired data:

- **v002 BTCUSDT 15m trade-price klines** (research-eligible).
- **v002 ETHUSDT 15m trade-price klines** (research-eligible).
- **v002 BTCUSDT 1h-derived trade-price klines** (research-eligible).
- **v002 ETHUSDT 1h-derived trade-price klines** (research-eligible).
- **Phase 4i BTCUSDT 30m trade-price klines** (research-eligible).
- **Phase 4i ETHUSDT 30m trade-price klines** (research-eligible).
- **Phase 4i BTCUSDT 4h trade-price klines** (research-eligible).
- **Phase 4i ETHUSDT 4h trade-price klines** (research-eligible).
- **v002 BTCUSDT funding manifests.**
- **v002 ETHUSDT funding manifests.**

**G1 does NOT use** in this first spec:

- Phase 4i metrics OI subset (the funding pathology dimension uses
  v002 funding manifests directly; OI is not a primary regime-
  classifier dimension in this first spec to keep scope tight and
  avoid Phase 4j §11 governance overhead).
- Mark-price 30m / 4h (NOT acquired; deferred per Phase 4h §20).
- aggTrades (NOT acquired; deferred per Phase 4h §7.E).
- Spot data, cross-venue data (forbidden by §1.7.3).
- Optional metrics ratio columns (forbidden by Phase 4j §11.3).
- Authenticated APIs, private endpoints, user stream, WebSocket,
  listenKey lifecycle (forbidden by safety rules).
- 5m Q1–Q7 diagnostic outputs as strategy features or regime
  indicators (Phase 3o §6 forbidden question forms preserved).

**No data acquisition authorized by Phase 4p.** **No manifest
modification.**

---

## Data inputs

Future backtest (if ever authorized) MUST consume EXACTLY the
following datasets:

| Dataset | Manifest | research_eligible | Use in G1 |
|---|---|---|---|
| `binance_usdm_btcusdt_15m__v002` | v002 manifest | true | (optional fallback signal timeframe; not used in primary spec) |
| `binance_usdm_btcusdt_1h_derived__v002` | v002 manifest | true | (1h regime-persistence support timeframe) |
| `binance_usdm_btcusdt_30m__v001` | Phase 4i manifest | true | **primary signal timeframe** |
| `binance_usdm_btcusdt_4h__v001` | Phase 4i manifest | true | **regime classifier primary timeframe** |
| `binance_usdm_ethusdt_15m__v002` | v002 manifest | true | (optional fallback) |
| `binance_usdm_ethusdt_1h_derived__v002` | v002 manifest | true | 1h regime-persistence support |
| `binance_usdm_ethusdt_30m__v001` | Phase 4i manifest | true | **comparison signal timeframe** |
| `binance_usdm_ethusdt_4h__v001` | Phase 4i manifest | true | **comparison regime classifier timeframe** |
| `binance_usdm_btcusdt_funding__v002` | v002 manifest | (per v002 lock) | **funding pathology classifier dimension** |
| `binance_usdm_ethusdt_funding__v002` | v002 manifest | (per v002 lock) | comparison funding pathology |

**No new dataset, no v003, no manifest modification.** Future
backtest reads existing Parquet partitions from
`data/normalized/klines/symbol=<SYMBOL>/interval=<INTERVAL>/...`
and `data/normalized/funding_rate/symbol=<SYMBOL>/...`.

**Forbidden inputs (per Phase 4o + Phase 4p):**

- mark-price 30m / 4h klines;
- mark-price 5m klines (Phase 3q v001-of-5m; `research_eligible: false`);
- mark-price 15m klines (v002 mark-price; reserved for future
  `mark_price_backtest_candidate` validation step per Phase 3v §8.5);
- aggTrades data;
- spot data;
- cross-venue data;
- Phase 4i metrics OI subset (NOT used by G1 first spec; Phase 4j
  §11 governance preserved but unused);
- optional metrics ratio columns;
- v003 (does not exist; not authorized);
- modified Phase 4i / v002 / v001-of-5m manifests;
- authenticated REST / private endpoints / user stream / WebSocket /
  listenKey lifecycle;
- 5m Q1–Q7 diagnostic outputs.

---

## Timeframes

Phase 4p selects exact timeframes:

| Role | Selected | Rationale |
|---|---|---|
| **Regime classifier primary timeframe** | **4h** | TSMOM / trend-following literature (Moskowitz / Ooi / Pedersen 2012; Hurst et al. 2017) supports HTF horizons of weeks-to-months; 4h on a 30m signal yields HTF / signal ratio of 8:1 — sufficient persistence for regime characterization. |
| **Regime persistence support timeframe** | **1h** | Optional secondary HTF; used in trend-persistence directional efficiency computation if Phase 4q chooses to include it. v002 1h-derived sufficient. |
| **Signal timeframe** | **30m** | Phase 4f §11.1 reasoning preserved: 30m halves V1 15m turnover (cost-survival friendlier) while retaining sufficient signal density for multi-year sample size. |
| **ETHUSDT comparison** | same | Per §1.7.3 / Phase 4g §10 protocol. |

**Execution assumption:** entry at next 30m bar's open after a
completed signal-bar entry condition. **No intrabar entries.** **No
partial fills.** **No limit-resting entries.**

**Phase 4p does NOT use:**

- 5m as primary signal (Phase 3t §14.2);
- 1m as primary signal (not authorized; would require Phase 4q for
  acquisition).

---

## Regime state machine specification

States and exact transition rules:

### State 1: `regime_inactive`

- **Initial state** at the start of each backtest run.
- **Purpose:** strategy is dormant; no signal computation; classifier
  runs continuously.
- **Allowed:** classifier evaluation on completed bars.
- **Forbidden:** entry signal computation; order placement.
- **Transition out:** `inactive → candidate` on the first completed
  4h bar where the favorable regime condition (§"Regime classifier
  formula" below) holds.

### State 2: `regime_candidate`

- **Purpose:** early evidence of regime shift; awaiting confirmation.
- **Allowed:** classifier continues; may transition.
- **Forbidden:** entry signal computation; order placement.
- **Transitions:**
  - `candidate → active` if the favorable regime condition holds for
    **K_confirm = 3 consecutive completed 4h bars** (~12 hours of
    persistence). Two variants in the threshold grid: **K_confirm
    ∈ {2, 3}** (axis 5).
  - `candidate → inactive` if the favorable regime condition fails
    on any single completed 4h bar before confirmation (no timeout
    grace period; a single failure resets to inactive).

### State 3: `regime_active`

- **Purpose:** confirmed favorable regime; strategy active.
- **Allowed:** entry signal evaluation at completed 30m bar
  boundaries; entry orders if signals + risk gates pass.
- **Forbidden:** entry under `mixed_or_unknown` governance label
  (Phase 3v §8.4); entry without classifier == active at signal
  time.
- **Transitions:**
  - `active → cooldown` after a completed trade exit (any reason:
    stop, take-profit, time-stop).
  - `active → cooldown` if regime-degradation signal fires (favorable
    regime condition breaks on a completed 4h bar; classifier
    transitions to non-favorable).
  - `active` does NOT exit immediately on a `regime_candidate-like`
    weak signal; it requires a clear favorable-regime failure.

### State 4: `regime_cooldown`

- **Purpose:** post-trade or post-degradation pause; no new entries.
- **Allowed:** existing position management (stop / take-profit /
  time-stop continue per the exit model).
- **Forbidden:** new entries; same-direction re-entry; opposite-
  direction reversal.
- **Transitions:**
  - `cooldown → inactive` if the favorable regime condition fails
    on any completed 4h bar during cooldown.
  - `cooldown → active` after **C_cooldown = 4 completed 4h bars
    (= 16 hours)** if the favorable regime condition still holds at
    the end of the cooldown.

### Position-vs-regime interaction

**Phase 4p chooses Option A** per Phase 4o §"Strategy-active versus
strategy-inactive behavior":

- **Position lifecycle is independent of regime state.** If regime
  transitions from `active` to `cooldown` or `inactive` during an
  open position, the position continues until its exit rules
  trigger (stop / take-profit / time-stop).
- **Rationale:** Option A keeps the exit model deterministic and
  decoupled from classifier instability. Option B (regime
  degradation forces position exit) would introduce a regime-driven
  exit that interacts non-trivially with the target / time-stop
  logic and risks early cuts on noisy regime classifier
  transitions.

### State machine summary

```text
                    ┌──────────────────┐
                    │ regime_inactive  │ ← initial state
                    └────┬─────────────┘
                         │  (favorable regime condition holds at completed 4h bar)
                         ▼
                    ┌──────────────────┐
                    │ regime_candidate │
                    └────┬─────────────┘
                         │  (K_confirm consecutive completed 4h bars)
                ┌────────┼──────────────┐
                ▼                       ▼
           ┌───────────────┐     (favorable regime fails →)
           │ regime_active │     regime_inactive
           └────┬──────────┘
                │ (trade exit OR regime degradation)
                ▼
           ┌───────────────────┐
           │ regime_cooldown   │
           └────┬──────────────┘
                │ (C_cooldown bars elapsed)
                │ + favorable regime still holds?
        ┌───────┼───────┐
        ▼               ▼
   regime_active   regime_inactive
```

### Transition discipline

- **All transitions use prior-completed bars only.** No lookahead.
- **All transition criteria are predeclared** (Phase 4p binding).
- **The state machine is deterministic** given classifier inputs.
- **The state machine has bounded memory:** `regime_candidate` →
  `regime_active` requires only the most recent K_confirm completed
  4h bars; `regime_cooldown` → `regime_active` requires only the
  most recent C_cooldown completed 4h bars; no unbounded path-
  dependence.

---

## Regime classifier formula

The regime classifier is a **composite predicate** evaluated on
completed 4h bars. It returns one of three classifier states (per
4h bar): `favorable_long`, `favorable_short`, `unfavorable`.

### Inputs

The classifier consumes the following completed-bar features:

1. **HTF trend score** (4h): EMA(20) and EMA(50) on completed 4h
   close prices, plus EMA(20) slope-rising condition.
2. **Trend persistence** (4h): directional efficiency over last 12
   completed 4h bars.
3. **Volatility regime** (30m): ATR(20) percentile rank over a
   rolling 480-bar window of prior completed 30m bars (most recent
   ATR percentile available at the 4h-bar close time).
4. **Liquidity adequacy** (30m): volume ratio over a rolling 480-bar
   median of prior completed 30m bars (most recent volume ratio at
   the 4h-bar close time).
5. **Funding pathology** (v002 funding events): percentile rank of
   the most recent completed funding event's rate over a trailing
   90 events.

### Classifier formula

#### HTF trend condition

For each completed 4h bar at time `t_4h`:

- `EMA20(t_4h)` = EMA(20) of completed 4h closes through `t_4h`.
- `EMA50(t_4h)` = EMA(50) of completed 4h closes through `t_4h`.

**Bullish trend condition:**

- `EMA20(t_4h) > EMA50(t_4h)` AND
- `close(t_4h) > EMA20(t_4h)` AND
- `EMA20(t_4h) > EMA20(t_4h - 3 × 4h)` (rising slope vs. 3 4h bars
  earlier; discrete comparison per Phase 3w §7.3).

**Bearish trend condition:** strict mirror.

**Neutral:** otherwise.

#### Trend persistence condition

`directional_efficiency(t_4h) = |close(t_4h) - close(t_4h - 12 × 4h)|
                              / Σ_{i=t_4h-11..t_4h} |close(i) - close(i-1)|`

Range: [0, 1]; higher means more directional / less choppy.

**Phase 4p threshold:** `E_min ∈ {0.30, 0.40}` (axis 1 of threshold
grid). Persistence condition passes if
`directional_efficiency(t_4h) >= E_min`.

#### Volatility condition

For each completed 4h bar at time `t_4h`:

- Take the most recent completed 30m ATR(20) percentile available
  at `t_4h_close = t_4h_open + 4h - 1ms`.
- Specifically: at the 30m bar with `open_time` such that
  `open_time + 30min ≤ t_4h_close`, compute ATR(20) percentile
  rank over a rolling 480-bar window of prior completed 30m bars.

**Phase 4p threshold band:** `[P_atr_low, P_atr_high] ∈ {[20, 80],
[30, 70]}` (axis 2 of threshold grid). Volatility condition passes
if percentile is in band.

**Why band, not lower-half only:** breakouts in compression-only
regimes are V2's failure mode; breakouts in chaos-only regimes are
unstable. The band excludes both pathological extremes.

#### Liquidity condition

For each completed 4h bar at time `t_4h`:

- Take the most recent completed 30m volume available at
  `t_4h_close`.
- Compute the median 30m volume over a rolling 480-bar window of
  prior completed 30m bars.

**Phase 4p threshold:** `V_liq_min ∈ {0.80, 1.00}` (axis 3 of
threshold grid). Liquidity condition passes if
`current_30m_volume / rolling_median >= V_liq_min`.

**Rationale:** R2's failure pattern (HIGH cost breaks marginal
expectancy from low-liquidity entry timing) suggests that excluding
sub-median-liquidity bars at signal time should reduce cost-
fragility. Phase 4p uses 30m volume vs. rolling 480-bar (10-day)
median rather than V2's UTC-hour percentile to keep the formulation
simple and avoid V2 inheritance.

#### Funding pathology condition

For each completed 4h bar at time `t_4h`:

- Identify the most recent completed funding event with
  `funding_time <= t_4h_close`.
- Compute the percentile rank of that event's funding rate over the
  trailing 90 completed funding events (≈ 30 days at 8h cadence on
  BTCUSDT USDⓈ-M).

**Phase 4p threshold band:** `[P_fund_low, P_fund_high] ∈ {[15, 85],
[25, 75]}` (axis 4 of threshold grid). Funding pathology condition
passes (i.e., funding is non-pathological / regime-allowable) if
percentile is in band.

**Rationale:** D1-A demonstrated funding extremes contain
information; G1 uses funding as **risk-context filter** (avoid
trading during pathological extremes), NOT as directional trigger.
Phase 4p deliberately chooses a wider band than V2 ([20, 80] / [30,
70]) and a narrower one ([25, 75] / [15, 85]) to avoid inheriting
V2 thresholds blindly while preserving the conceptual approach.

### Composite favorable regime

For each completed 4h bar:

**`favorable_long`** if:

- HTF trend condition is **bullish** AND
- Trend persistence condition passes AND
- Volatility condition passes AND
- Liquidity condition passes AND
- Funding pathology condition passes.

**`favorable_short`** if:

- HTF trend condition is **bearish** AND
- Trend persistence condition passes AND
- Volatility condition passes AND
- Liquidity condition passes AND
- Funding pathology condition passes.

**`unfavorable`** otherwise.

The regime state machine consumes this 4h-bar classifier output and
applies the K_confirm / C_cooldown rules per §"Regime state machine
specification".

---

## Regime transition rules

Per §"Regime state machine specification" §"State 2: regime_candidate"
and §"State 4: regime_cooldown":

- **`inactive → candidate`:** any single completed 4h bar with
  `favorable_long` or `favorable_short` (single-bar trigger).
- **`candidate → active`:** **K_confirm consecutive completed 4h
  bars** with the same `favorable_long` (or `favorable_short`)
  classifier output. K_confirm ∈ {2, 3} per axis 5 of threshold
  grid.
- **`candidate → inactive`:** any single completed 4h bar where
  the classifier returns `unfavorable` OR the opposite direction
  (`favorable_long` ↔ `favorable_short` direction switch resets
  candidate state to inactive).
- **`active → cooldown`:** trade exit (stop / take-profit / time-
  stop) OR classifier returns `unfavorable` on a completed 4h bar.
- **`cooldown → inactive`:** classifier returns `unfavorable` on a
  completed 4h bar during cooldown.
- **`cooldown → active`:** **C_cooldown = 4 completed 4h bars**
  elapsed since cooldown entered AND classifier remains
  `favorable_long` (or `favorable_short`, matching the original
  active-direction).

**No direction switch within active.** If the original active
direction was `favorable_long` and the classifier transitions to
`favorable_short` during cooldown, the cooldown continues to
inactive (cooldown does NOT promote to opposite-direction active).

---

## Strategy-active and strategy-inactive behavior

### When `regime_active` (and signal direction matches active direction):

- Entry signals are computed at completed 30m bar boundaries (per
  §"Inside-regime breakout setup").
- If a long setup signal fires AND active direction is
  `favorable_long` AND no position is open AND no cooldown:
  - market entry order placed at next 30m bar's open;
  - position sized per 0.25% risk + 2× leverage cap;
  - protective stop set per §"Structural stop model";
  - take-profit set per §"Target model";
  - time-stop counter starts.
- Mirror for short.

### When NOT `regime_active`:

- **No** entry signal computation.
- **No** breakout evaluation function invoked.
- **No** orders placed.
- **No** new position opened.
- Existing position management continues (Option A: stop / take-
  profit / time-stop continue per the exit rules).
- The regime classifier continues running on completed 4h bars.

### When direction mismatch (e.g., active = long, completed 30m bar shows short breakout):

- **No entry.** Direction must match active regime direction.

---

## Inside-regime breakout setup

Phase 4p selects the exact breakout setup:

### Long breakout

A long breakout setup is generated at completed 30m bar `t_30m`
when ALL of the following hold:

1. Regime state machine is in `regime_active` with
   `direction = favorable_long`.
2. No active cooldown.
3. No position currently open.
4. **Donchian-style breakout structure:** `close(t_30m) >
   max(high[t_30m - N_breakout × 30m : t_30m - 30m]) +
   B_atr × ATR(20)(t_30m)`.
   - `N_breakout = 12` completed 30m bars (= 6 hours of prior bars).
   - `B_atr = 0.10` (matches V1 / R3 buffer convention; not V2's
     fixed value).
   - The prior-N_breakout-bar high is computed EXCLUDING the current
     bar (per V1 / R3 / V2 lookback convention).
5. **No governance-label failure:** `stop_trigger_domain =
   trade_price_backtest`; `break_even_rule = disabled`;
   `ema_slope_method = discrete_comparison`;
   `stagnation_window_role = not_active`. `mixed_or_unknown` is
   invalid and fails closed at any decision boundary (Phase 3v §8 /
   Phase 3w §6 / §7 / §8).

### Short breakout

Strict mirror image with `direction = favorable_short`,
`close(t_30m) < min(low[t_30m - N_breakout × 30m : t_30m - 30m]) -
B_atr × ATR(20)(t_30m)`.

### Why these specific values

- **N_breakout = 12** (6 hours of prior 30m bars). Chosen from first
  principles: shorter than V2's N=20 / 40 (which produced 0 trades
  due to wide structural stops); longer than V1's N=8 (which is
  calibrated for 15m, not 30m). 12 bars on 30m ≈ 6 hours, comparable
  in calendar time to V1's 8 bars on 15m (= 2 hours) when accounting
  for the 30m / 15m timeframe ratio plus the additional regime-
  conditioning that allows wider lookback.
- **B_atr = 0.10**. Matches V1's buffer convention to absorb noise.
  Phase 4p does NOT inherit V1's stop-distance bounds (which are the
  G1-forbidden default), only the buffer concept.
- **No 8-feature AND chain.** G1's regime gating already filters out
  most unfavorable bars at the state-machine level; the inside-
  regime entry condition is intentionally simpler than V2's 8-feature
  AND chain.
- **Direction must match active regime direction.** This is the
  binding G1 constraint: only long breakouts in `favorable_long`
  regime; only short breakouts in `favorable_short` regime.

---

## Entry rules

Per §"Inside-regime breakout setup" + execution model:

1. **Signal evaluation time:** completed 30m bar's close-time =
   `open_time + 30 × 60 × 1000 - 1` ms.
2. **Entry order time:** next 30m bar's `open_time` after signal.
3. **Entry order type:** MARKET.
4. **Entry fill assumption:** at next 30m bar's `open` price.
5. **No intrabar entries. No partial fills. No limit-resting
   entries.**
6. **One position max per symbol** (§1.7.3 preserved).
7. **No pyramiding** (§1.7.3 preserved).
8. **No reversal while positioned** (§1.7.3 preserved).
9. **Same-direction cooldown** prevents immediate re-entry after
   exit; opposite-direction reversal during cooldown forbidden.

---

## Structural stop model

### Long initial stop

`initial_stop_long(t_30m) = min(low[t_30m - N_stop × 30m : t_30m - 30m]) - S_buffer × ATR(20)(t_30m)`

- `N_stop = 12` (matches N_breakout for setup-stop coherence).
- `S_buffer = 0.10` (matches B_atr for buffer consistency).
- The prior-N_stop-bar low EXCLUDES the current bar.
- The current bar's own low is NOT included in setup_low (this is
  a deliberate departure from V1 / R3's `min(setup_low,
  breakout_bar_low)`; G1's stop is structural to the prior window
  only, simplifying the setup-stop math and avoiding V2's failure
  mode where the breakout-bar's intra-bar low can pull setup_low
  far below the breakout close).

### Short initial stop

Strict mirror.

### R definition

`R(t_30m) = |entry_price - initial_stop|`

where `entry_price = open(t_30m + 30min)` (next bar's open).

### Stop-distance quality bounds (G1-specific, derived from active-regime structure)

**Minimum bound:** `0.50 × ATR(20)(t_30m)`. Below this, the stop
sits inside expected intra-regime noise and would produce too-tight
stops vulnerable to whipsaw.

**Maximum bound:** `2.20 × ATR(20)(t_30m)`. Above this, the
target × N_R math becomes implausible (e.g., 3 × ATR stop with
N_R = 2 requires 6 × ATR move; trade frequency collapses).

**Phase 4p justification for [0.50, 2.20]:** these bounds are
derived from active-regime ATR(20) structure analysis at first
principles, NOT from V1's 0.60–1.80 × ATR or from V2's Phase 4l
forensic numbers. The wider band on both sides accommodates G1's
N_breakout = N_stop = 12 setup geometry, which produces larger
prior-window low/high spreads than V1's N=8 but smaller than V2's
N=20 / 40.

If `stop_distance < 0.50 × ATR` OR `stop_distance > 2.20 × ATR` at
signal time, **the trade is rejected** (no entry placed). This is
a trade-quality filter, not a sizing constraint.

### Stop trigger domain

Per Phase 3v §8 binding (preserved verbatim):

- **Research / backtest:** `stop_trigger_domain = trade_price_backtest`.
- **Future runtime / paper / live (NOT authorized):**
  `mark_price_runtime`.
- **Future live-readiness validation step (NOT authorized):**
  `mark_price_backtest_candidate`.
- **`mixed_or_unknown` is invalid and fails closed at any decision
  boundary.**

---

## Target model

### Fixed-R take-profit

`take_profit_long(t_30m) = entry_price + N_R × R`

`take_profit_short(t_30m) = entry_price - N_R × R`

**`N_R ∈ {2.0, 2.5}`** (axis 6 of threshold grid).

### No break-even

`break_even_rule = disabled` (Phase 3w §6.3 declared value;
preserved verbatim from Phase 4g §21 / R3 baseline-of-record;
canonical for G1).

### No trailing stop

Intentional. G1's first spec uses fixed-R + time-stop only. Adding
trailing stops would compound exit-rule degrees of freedom and is
deferred to future G1-extension memos (none authorized).

### Same-bar stop / take-profit ambiguity

**Conservative tie-break: stop wins.** If a single 30m bar's
high/low/close range admits BOTH stop and take-profit triggering,
the simulation MUST resolve as stop. Justification: the actual
realized intra-bar path is unknown; assuming stop-first is loss-
realizing and matches V1 / R3 / V2 convention.

### Stop-precedence

1. If protective stop triggers first → exit at stop.
2. Else if take-profit triggers first → exit at take-profit.
3. Else if time-stop horizon elapses → exit at next 30m bar's open
   at market.

---

## Time-stop model

**`T_stop ∈ {12, 16}`** completed 30m bars (= 6h or 8h) (axis 7 of
threshold grid).

After T_stop completed 30m bars elapsed since entry, the position
exits at the next 30m bar's open at market regardless of MFE / MAE.

**Rationale:**

- 6h–8h matches the expected regime persistence for a confirmed
  active 4h-classifier regime with K_confirm = 2-3 4h bars. A
  trade that hasn't reached its target or stop within 6-8 hours is
  likely caught in regime degradation; closing at time-stop avoids
  drawn-out time-decay losses.
- Matches Phase 4g §29 axis 9 cardinality (2 values) but NOT the
  same values blindly: V2 used T_stop ∈ {12, 16}; G1 uses the same
  cardinality and values *deliberately* because they correspond to
  the same calendar-time horizons; this is conceptual reuse of a
  reasonable horizon, NOT V2 rescue (V2 failed at the stop-distance
  filter level, not the time-stop level).

### Position-vs-regime interaction

**Option A (chosen by Phase 4p):** position lifecycle independent
of regime. If regime transitions from `active` → `cooldown` /
`inactive` during an open position, the position continues until
its exit rules trigger (stop / take-profit / time-stop). Regime
degradation does NOT force exit.

This is the more conservative choice and avoids cascading
regime-instability-driven exits.

---

## Position sizing and exposure rules

Preserved verbatim from §1.7.3:

- **Initial live risk per trade:** **0.25%** of sizing equity.
- **Effective leverage cap:** **2×**.
- **Max concurrent positions:** **1**.
- **Symbol scope:** **BTCUSDT only for live**; ETHUSDT research /
  comparison only.
- **No pyramiding:** Phase 4p does not introduce add-on logic.
- **No reversal while positioned:** opposite-direction reversal
  during an open position is forbidden.
- **Lot-size rounding:** position_size_qty rounded down to lot-size
  increment; below-minimum-quantity rejects.

Sizing computation (R3 / V1 / V2 convention preserved):

```text
position_size_qty = floor((equity × 0.0025) / stop_distance)

subject to:
  position_size_qty × entry_price ≤ effective_leverage_cap × equity
  position_size_qty × entry_price ≤ internal_notional_cap
  position_size_qty ≥ exchange_min_quantity (else trade rejected)
```

**No live notional claims by Phase 4p.** **No internal_notional_cap
specified at Phase 4p**; that is a runtime config concern (§1.7.3
mandatory before any live operation; not authorized by Phase 4p).

---

## Cost model

Preserved verbatim from Phase 4k / Phase 4g §26 / §11.6:

- **§11.6 = 8 bps slippage per side preserved verbatim.** No
  relaxation.
- **Taker fee:** **4 bps per side** default for USDⓈ-M futures.
- **Cost cells for any future backtest:**
  - **LOW:** 1 bp slippage per side → 4 + 4 + 1 + 1 = 10 bps
    round-trip;
  - **MEDIUM:** 4 bps slippage per side → 4 + 4 + 4 + 4 = 16 bps
    round-trip (canonical reporting cell);
  - **HIGH:** 8 bps slippage per side → 4 + 4 + 8 + 8 = 24 bps
    round-trip (§11.6 promotion gate).
- **No maker rebate.**
- **No live fee assumption** (no VIP / BNB-payment / partner-rebate
  discounts).
- **Funding cost included in P&L.** For each open G1 position
  spanning a funding event, position is debited / credited per
  the published funding rate × position notional × funding-fraction.
- **Promotion blocked if HIGH cost fails on BTCUSDT primary.**

**G1 must survive §11.6 HIGH on BTCUSDT primary in any future
backtest.** This is binding.

---

## Threshold grid

Phase 4p commits a **compact 32-variant grid** (= 2^5) over 5
binary axes. Phase 4g §29's 512-variant overbreadth is explicitly
avoided.

| Axis # | Parameter | Selected values | Cardinality |
|---|---|---|---|
| **1** | `E_min` (trend persistence minimum) | `{0.30, 0.40}` | 2 |
| **2** | `[P_atr_low, P_atr_high]` (volatility band) | `{[20, 80], [30, 70]}` | 2 |
| **3** | `V_liq_min` (liquidity minimum) | `{0.80, 1.00}` | 2 |
| **4** | `[P_fund_low, P_fund_high]` (funding band) | `{[15, 85], [25, 75]}` | 2 |
| **5** | `K_confirm` (regime confirmation length) | `{2, 3}` 4h bars | 2 |

**Total: 2^5 = 32 variants.**

### Fixed parameters (cardinality 1)

- `N_breakout` = 12 30m bars.
- `B_atr` (breakout buffer) = 0.10 × ATR(20).
- `N_stop` = 12 30m bars.
- `S_buffer` (stop buffer) = 0.10 × ATR(20).
- Stop-distance min = 0.50 × ATR(20).
- Stop-distance max = 2.20 × ATR(20).
- `N_R` (target multiplier) = **2.0** (single fixed value).
- `T_stop` (time-stop horizon) = **16** completed 30m bars (single
  fixed value).
- `C_cooldown` = 4 completed 4h bars.
- HTF EMA pair: `(20, 50)` on 4h.
- HTF slope-rising lookback: `3` 4h bars.
- Trend-persistence lookback: `12` 4h bars.
- Volatility ATR period: `20` 30m bars.
- Volatility percentile lookback: `480` 30m bars (10 days).
- Liquidity median lookback: `480` 30m bars (10 days).
- Funding lookback: `90` events.

**Note:** N_R and T_stop are fixed in this first-spec G1 to keep the
grid at 32 variants. A future G1-extension memo may introduce
N_R ∈ {2.0, 2.5} and T_stop ∈ {12, 16} as additional axes (would
expand to 128 variants), but this requires separate operator
authorization and the additional axes must be predeclared before
data is touched.

### Search-space control

- **Compact grid (32 variants).** PBO / DSR / CSCV computation is
  tractable: deflated-Sharpe correction handles N variants with
  cost ~log(N) → log(32) = 5; CSCV with S = 16 sub-samples handles
  N = 32 at C(16, 8) = 12 870 combinations × 32 variants =
  ~412 000 sub-evaluations (well within Python-runtime feasibility).
- **No grid extension.** Phase 4p commits 32 variants; future
  backtest must NOT add variants without explicit re-predeclaration.
- **Deterministic variant ordering.** Lexicographic by axis name
  then axis value (analogous to Phase 4k §"Search-space control").
- **No early exit on bad variants.** All 32 variants reported.
- **No outcome-driven threshold selection.** Variant identification
  uses deflated Sharpe / PBO / CSCV correction, not raw in-sample
  Sharpe.
- **Forbidden axes:**
  - V2 stop-distance rescue values;
  - V1 0.60–1.80 × ATR inherited bounds;
  - optional metrics ratio columns;
  - 5m diagnostics features.

---

## Signal generation logic

The full signal evaluation logic at completed 30m bar `t_30m` (after
all data through `t_30m_close` is available):

```text
def evaluate_g1_signal(t_30m):
    # Step 1: classify regime at the most recent completed 4h bar
    t_4h = most_recent_completed_4h_bar(t_30m_close)
    regime_class = classifier(t_4h)
    # regime_class ∈ {favorable_long, favorable_short, unfavorable}

    # Step 2: update state machine (deterministic per t_4h)
    state, direction = state_machine.update(regime_class, t_4h)

    # Step 3: no signal outside regime_active
    if state != "regime_active":
        return None

    # Step 4: check direction match for setup
    if direction == "favorable_long":
        if not long_breakout_setup(t_30m):
            return None
        if not stop_distance_in_band(long_stop_distance(t_30m)):
            return None
        return {"side": "long", "t_30m": t_30m}

    elif direction == "favorable_short":
        if not short_breakout_setup(t_30m):
            return None
        if not stop_distance_in_band(short_stop_distance(t_30m)):
            return None
        return {"side": "short", "t_30m": t_30m}

    return None
```

### Forbidden signal additions

- **No 5m signal triggers.** Phase 3t §14.2 preserved.
- **No discretionary overrides.**
- **No post-hoc rescue variants.**
- **No D1-A funding-Z-score directional rule.**
- **No F1 mean-reversion logic.**
- **No R2 pullback-retest entry.**
- **No multi-asset / cross-sectional optimization.**
- **No hedge mode** (§1.7.3).

---

## Exit logic

Per §"Structural stop model" + §"Target model" + §"Time-stop model":

### Stop-precedence (binding)

1. **Stop trigger first.** If on bar `t > t_entry` (during open
   position):
   - Long: `low(t) ≤ stop_price` → exit at `stop_price`.
   - Short: `high(t) ≥ stop_price` → exit at `stop_price`.
2. **Take-profit trigger first** (only if stop not triggered on
   same bar):
   - Long: `high(t) ≥ tp_price` → exit at `tp_price`.
   - Short: `low(t) ≤ tp_price` → exit at `tp_price`.
3. **Time-stop:** if neither stop nor TP triggered within `T_stop`
   completed 30m bars → exit at next 30m bar's open at market.

### Same-bar ambiguity

Conservative tie-break: stop wins.

### Cooldown trigger

Any exit (stop / TP / time-stop) transitions regime state machine
to `regime_cooldown` per §"Regime state machine specification".

### Position-vs-regime

Option A: position lifecycle independent of regime. Regime
degradation does NOT force exit.

---

## Metrics OI governance, if used

**G1 first spec does NOT use Phase 4i metrics OI subset.** Phase 4j
§11 governance is preserved verbatim but unused by G1.

Rationale: Phase 4o §"Allowed classifier dimensions" lists "optional
OI context only if Phase 4j §11 OI-subset governance is preserved";
Phase 4p elects to NOT use OI in the first spec to keep scope tight,
avoid Phase 4j §11 governance overhead, and ensure all five
classifier dimensions can be computed from kline + funding data
alone.

If a future G1-extension memo adds OI context as a classifier
dimension, **Phase 4j §11 binding rule applies** verbatim:

- Metrics manifests remain globally `research_eligible: false`.
- Per-bar OI-feature-eligibility check: all six aligned 5-minute
  records present + non-NaN `sum_open_interest` AND non-NaN
  `sum_open_interest_value`.
- Optional ratio columns categorically forbidden.
- No forward-fill, interpolation, imputation, synthetic data, or
  silent omission.
- Required exclusion-counts and main-cell vs. exclude-entire-
  affected-days sensitivity reporting.

This is documented for future reference only; Phase 4p does NOT
introduce OI dependency.

---

## Forbidden inputs

Phase 4p forbids (binding for any future G1 backtest):

- **mark-price 30m / 4h klines** (NOT acquired; deferred per Phase
  4h §20);
- **mark-price 5m klines** (Phase 3q v001-of-5m;
  `research_eligible: false`);
- **mark-price 15m klines** (v002 mark-price; reserved for future
  `mark_price_backtest_candidate` validation step per Phase 3v §8.5);
- **aggTrades** (NOT acquired; deferred per Phase 4h §7.E);
- **spot data** (forbidden by §1.7.3);
- **cross-venue data** (forbidden by §1.7.3);
- **Phase 4i metrics OI subset** (NOT used by G1 first spec; Phase
  4j §11 preserved but unused);
- **optional metrics ratio columns** (forbidden by Phase 4j §11.3);
- **v003** (does not exist; not authorized);
- **modified Phase 4i / v002 / v001-of-5m manifests** (preserved
  verbatim);
- **authenticated REST / private endpoints / public endpoints in
  code / user stream / WebSocket / listenKey lifecycle** (forbidden
  by safety rules);
- **5m Q1–Q7 diagnostic outputs as strategy features or regime
  indicators** (Phase 3o §6 forbidden question forms preserved);
- **V2 Phase 4l observed stop-distance failure numbers as design
  inputs** (Bailey et al. 2014 / Phase 4m anti-data-snooping
  discipline).

---

## Mechanism-check thresholds

Phase 4p commits exact numeric thresholds for M1 / M2 / M3 / M4.

### M1 — Regime-validity negative test

**Claim:** Inside `regime_active`, breakout continuation has
materially better risk-adjusted outcomes than outside `regime_active`.

**Test design:**

- For each variant in the 32-variant grid, compute hypothetical
  G1 long+short signals at completed 30m bar boundaries in BOTH
  `regime_active` AND `regime_inactive` periods (the latter is a
  "would-have-been" trade population, NOT actually traded).
- For each population, compute mean_R after MEDIUM-cost cell on
  OOS holdout window.
- **Pass criterion:** `mean_R(active) - mean_R(inactive) >= +0.10R`
  on BOTH BTCUSDT and ETHUSDT, with bootstrap-by-trade B = 10 000
  95% CI lower bound > 0.
- **Fail criterion:** any of the above fails on either symbol.

**M1 FAIL on BTCUSDT alone is sufficient for V2-style HARD REJECT**
(analogous to F1's failure pattern).

### M2 — Regime-gating value-add over always-active baseline

**Claim:** G1 (regime-gated) outperforms an always-active breakout
baseline, especially at HIGH cost.

**Test design:**

- For each variant, compute always-active baseline trade population
  (same N_breakout / B_atr / N_stop / S_buffer / N_R / T_stop;
  but classifier always returns `favorable_long` for upward
  breakouts and `favorable_short` for downward; classifier-
  conditioning is removed).
- Compare `mean_R(G1 @ HIGH cost)` vs. `mean_R(always-active @
  HIGH cost)` on OOS holdout, BTCUSDT primary.
- **Pass criterion:** `mean_R(G1, HIGH) - mean_R(always-active,
  HIGH) >= +0.05R` on BOTH BTCUSDT and ETHUSDT, with bootstrap-CI
  lower bound > 0.
- **Fail criterion:** below threshold or wrong-signed on either
  symbol.

**M2 FAIL** indicates regime-gating doesn't add value beyond simpler
baselines; G1 framework PARTIAL PASS at most.

### M3 — Inside-regime co-design validity

**Claim:** Inside-regime entry / stop / target / sizing co-design
produces adequate trade count AND positive OOS expectancy WITHOUT
catastrophic-floor trigger.

**Test design:**

- For BTC-train-best variant on BTCUSDT primary:
  - Trade count on OOS holdout ≥ **30** trades.
  - `mean_R(BTC OOS, MEDIUM-cost) > 0`.
  - `mean_R(BTC OOS, HIGH-cost) > 0` (i.e., §11.6 cost-survival).
  - No CFP-1 / CFP-2 / CFP-3 trigger.

**M3 FAIL** indicates co-design failed; G1 framework HARD REJECT
likely.

### M4 — Cross-symbol robustness

**Claim:** ETHUSDT comparison is directionally consistent with
BTCUSDT primary; ETH cannot rescue BTC.

**Test design:**

- BTCUSDT primary must pass M1 / M2 / M3 independently (Phase 4g
  §10 / Phase 4k preserved).
- ETHUSDT comparison must show:
  - `mean_R(ETH OOS, MEDIUM-cost)` non-negative;
  - directional sign match between ETH and BTC for M1 differential
    (active > inactive on both);
  - directional sign match between ETH and BTC for M2 differential
    (G1 > always-active on both).
- **Pass criterion:** all three above.
- **Fail criterion:** any of the three fails.

**Important:** ETH passing alone is NOT sufficient. CFP-4 (BTC
fails with ETH pass) overrides cross-symbol rescue attempts.

### Bootstrap configuration

- **Bootstrap iterations:** B = 10 000 (Phase 4k convention
  preserved).
- **Bootstrap method:** by-trade resampling with replacement.
- **Confidence level:** 95% (two-sided).
- **Pinned RNG seed:** must be predeclared in any future Phase 4q
  backtest-plan brief; suggested seed = `202604300` (Phase 4l
  convention).

---

## Negative-test specification

The negative-test component of M1 is critical for regime-first.

### Required components

1. **Active vs. inactive comparison** (M1 core test, see §"Mechanism-
   check thresholds").
2. **Always-active baseline comparison** (M2 core test).
3. **Optional random-regime baseline** (additional safeguard;
   Phase 4q decision whether to include).

### Random-regime baseline (optional)

If included by Phase 4q:

- Replace classifier with a random binary state generator with the
  same active-regime fraction as G1's empirical regime-active
  fraction.
- Use a separate fixed RNG seed (e.g., 202604301) for reproducibility.
- Compute random-regime baseline mean_R on OOS HIGH cost.
- **Pass criterion:** G1 mean_R > random-regime baseline mean_R by
  ≥ +0.03R on BOTH symbols.
- **Failure interpretation:** if G1 doesn't beat random-regime
  baseline, the classifier carries no information.

### Failure modes

- **Inactive regime equally favorable:** M1 differential ≤ 0;
  hypothesis fails.
- **Sample-size collapse from regime gating:** if active-regime
  fraction × signal density × OOS window length yields < 30 trades
  per variant on BTCUSDT, **CFP-1 fires**.
- **Train-only success:** if train-window M1 / M2 / M3 pass but
  validation / OOS fail, **CFP-5 / CFP-9 fires**.

---

## Catastrophic-floor predicates

Phase 4p commits exact CFP-1..CFP-12 thresholds for G1.

| Predicate | Trigger | Threshold |
|---|---|---|
| **CFP-1** | Insufficient trade count | < 30 OOS trades on BTC primary for the BTC-train-best variant |
| **CFP-2** | Negative OOS expectancy under HIGH cost | `mean_R(BTC OOS, HIGH) < 0` for BTC-train-best variant |
| **CFP-3** | Catastrophic drawdown / PF floor failure | `max_dd_R(BTC OOS, HIGH) > 8R` OR `profit_factor(BTC OOS, HIGH) < 0.50` |
| **CFP-4** | BTC failure with ETH pass | BTC fails any of M1 / M2 / M3 / CFP-2 / CFP-3 but ETH passes M1 / M2 / M3 |
| **CFP-5** | Train-only performance with OOS failure | `train_sharpe > 1.0` AND `oos_sharpe < 0.0` for BTC-train-best variant |
| **CFP-6** | Excessive PBO | `PBO (train → OOS) > 0.5` |
| **CFP-7** | Overconcentration in one month / regime | One calendar month contributes > 50% of total R on OOS holdout |
| **CFP-8** | Regime sensitivity failure | M1 active vs. inactive differential ≤ 0 (regime classifier doesn't sort outcomes) |
| **CFP-9** | Regime excludes too much data / sample-size collapse | Active-regime fraction × signal density × OOS window yields < 20 trades per variant on BTC primary |
| **CFP-10** | Forbidden input access | Static-scan or runtime introspection detects access to optional metrics ratio columns / mark-price / aggTrades / spot / cross-venue / authenticated APIs |
| **CFP-11** | Regime classifier lookahead or dependency on signal | Classifier consumes any future bar OR depends on entry signal presence |
| **CFP-12** | Data governance violation | Phase 4j §11 / Phase 3r §8 / Phase 3v §8 / Phase 3w / Phase 4k methodology violation; OR write attempt to `data/raw/` / `data/normalized/` / `data/manifests/` |

**Any single CFP triggering produces Verdict C HARD REJECT for G1
first-spec**, analogous to F1 / V2 patterns.

### Note on CFP-3 thresholds

CFP-3 thresholds (max_dd_R > 8R OR PF < 0.50) are **tighter than
Phase 4k's CFP-3 (max_dd_R > 10R)** because G1's regime-first
gating should produce qualitatively cleaner trade distributions
(by hypothesis); a > 8R drawdown in the active regime would be
strong evidence of regime-gating failure.

### Note on CFP-9

CFP-9 ("regime excludes too much data / sample-size collapse")
fires at a tighter threshold than CFP-1 (20 trades vs. 30 trades)
to catch the specific regime-first failure mode where the
classifier is too restrictive. CFP-1 is about absolute
insufficiency; CFP-9 is about classifier over-restriction.

---

## Validation windows

Phase 4p reuses Phase 4k's chronological split verbatim (justified
because the same v002 / Phase 4i datasets are reused; no new data
acquisition; chronological boundaries already validated by Phase
4k methodology):

| Window | Start (UTC) | End (UTC) | Span | Use |
|---|---|---|---|---|
| **Training / model-selection** | 2022-01-01 00:00:00 | 2023-06-30 23:30:00 | ~18 months | per-variant Sharpe; DSR; CSCV; variant selection |
| **Validation / selection-confirmation** | 2023-07-01 00:00:00 | 2024-06-30 23:30:00 | ~12 months | selection-confirmation (NOT used for variant re-selection) |
| **Out-of-sample holdout** | 2024-07-01 00:00:00 | 2026-03-31 23:30:00 | ~21 months | **primary G1 evidence cell** |

**Total span:** ~51 months exact = full Phase 4i / v002 coverage.

**Discipline (preserved verbatim from Phase 4k):**

- No data shuffle.
- No leakage.
- No window modification post-hoc.
- Validation window NOT used for variant re-selection.
- OOS holdout window NOT used for variant selection AND NOT used
  for validation-window Sharpe ranking.
- All boundaries are at 30m bar boundaries.

### Walk-forward extension

Optional secondary analysis (Phase 4q decision): 4 rolling 12-month
OOS windows over 2024-07..2026-03 starting at 2024-07, 2024-10,
2025-01, 2025-04 (overlapping). If omitted, must be justified.

---

## BTCUSDT primary / ETHUSDT comparison protocol

Preserved verbatim from §1.7.3 / Phase 4g §10 / Phase 4k:

- **BTCUSDT is primary.** G1's primary evidence is BTCUSDT.
- **ETHUSDT is comparison-only.** Cross-symbol consistency required.
- **ETH cannot rescue BTC failure.** CFP-4 fires if BTC fails M1 /
  M2 / M3 / CFP-2 / CFP-3 but ETH passes.
- **No multi-asset portfolio.** v1 is BTCUSDT only.
- **No cross-symbol optimization.** The same 32 variants are
  evaluated independently per symbol.
- **No BTC-only / ETH-only cherry-picking after outcomes.**
- **Backtest report must present BTC and ETH per-variant outcomes
  side-by-side for transparency**, NOT as a basis for cross-symbol
  selection.

---

## Required future backtest artefacts

The future Phase 4q — G1 Backtest-Plan Memo (docs-only) and the
future Phase 4r — G1 Backtest Execution phase (docs-and-code, if
both are ever authorized) MUST include:

### Required reporting tables (analogous to Phase 4k §"Required reporting tables"):

1. Run metadata (Phase 4r commit SHA; Phase 4p plan commit SHA;
   manifest SHAs; RNG seeds; etc.).
2. Dataset manifest references with SHA pinning.
3. Parameter grid (32 variants).
4. Train / validation / OOS split boundaries.
5. Per-variant trade summaries: BTCUSDT × 3 windows × MEDIUM-slip.
6. Per-variant trade summaries: ETHUSDT × 3 windows × MEDIUM-slip.
7. BTC-train-best variant identification.
8. BTC-train-best cost-cell sensitivity (LOW / MEDIUM / HIGH).
9. M1 / M2 / M3 / M4 mechanism-check tables.
10. Cost sensitivity per variant per cost cell.
11. PBO summary (train → OOS).
12. Deflated Sharpe summary per variant.
13. CSCV S = 16 sub-sample rankings (or compressed equivalent).
14. Regime classifier statistics (active-regime fraction; transition
    counts; classifier stability across train / validation / OOS).
15. Regime active vs. inactive comparison (M1 backbone).
16. Always-active baseline comparison (M2 backbone).
17. Trade distribution by year / month / regime (CFP-7 evaluation).
18. Verdict declaration (A / B / C / D classification).
19. Catastrophic-floor predicate results (12 predicates).
20. Forbidden-work confirmation (runtime introspection).

### Required plot artefacts (if matplotlib is available; otherwise document absence):

- Cumulative-R curves BTC + ETH per window;
- Regime state-machine timeline (regime_active fraction over time);
- Active vs. inactive R distribution histograms;
- DSR distribution per variant;
- PBO sub-sample rank distribution;
- Drawdown curve;
- Trade-distribution histogram;
- Monthly-bucketed cumulative R.

### Verdict taxonomy

- **Verdict A — G1 framework PASS:** all M1 / M2 / M3 / M4 pass; no
  CFP triggers; §11.6 HIGH cost-survival on BTCUSDT primary.
- **Verdict B — G1 framework PARTIAL PASS:** some mechanisms pass
  but not all (e.g., M1 ✓ but M2 ✗); no catastrophic-floor.
- **Verdict C — G1 framework HARD REJECT:** any catastrophic-floor
  predicate fires.
- **Verdict D — G1 framework INCOMPLETE:** methodology / governance
  / data violation; results invalid.

---

## Stop conditions for future backtest

Future Phase 4r execution MUST stop and produce a failure report on:

- required manifest missing;
- manifest SHA256 mismatch;
- local data file not found / corrupted;
- optional ratio column accessed (CFP-10);
- 5m Q1–Q7 finding accessed as feature / threshold;
- mark-price / aggTrades / spot / cross-venue accessed (CFP-12);
- regime classifier consumes future bars (CFP-11);
- regime classifier depends on entry signal (CFP-11);
- timestamp misalignment;
- trades emitted on excluded bars;
- trade count insufficient on > 50% of variants (CFP-1);
- validation report incomplete;
- authentication-API / private-endpoint / live-API access attempt;
- credential read / store attempt;
- network I/O outside `data.binance.vision` public bulk (and the
  script does not need any network I/O at all because data is local);
- write attempt to `data/raw/`, `data/normalized/`, `data/manifests/`;
- pytest test count regression;
- ruff / mypy violation.

Each is a fail-closed boundary.

---

## What future Phase 4q / 4r would need to do

### Phase 4q — G1 Backtest-Plan Memo (docs-only) [primary recommended next phase]

- Predeclare the exact Python script structure for the standalone
  G1 backtest orchestrator (analogous to
  `scripts/phase4l_v2_backtest.py`).
- Predeclare the exact data-loading interface (what columns are
  loaded; explicit column lists; metrics OI subset NOT loaded).
- Predeclare the exact regime classifier implementation algorithm
  (equivalent to Phase 4j §16 OI-exclusion algorithm in spirit:
  precise pseudocode for the deterministic state machine).
- Predeclare the exact trade simulation algorithm (entry timing;
  fill assumption; stop / TP / time-stop precedence; cooldown
  triggers).
- Predeclare the exact cost-cell modeling.
- Predeclare the exact M1 / M2 / M3 / M4 computation algorithms.
- Predeclare the exact CFP-1..CFP-12 evaluation algorithms.
- Predeclare the exact reporting table schemas.
- Predeclare the exact stop-condition matchers.
- Predeclare the exact verdict-taxonomy decision tree.
- Predeclare reproducibility requirements (manifest SHA pinning;
  RNG seed pinning; deterministic variant ordering; idempotent
  rerun).
- Predeclare the standalone-script discipline: no `prometheus.runtime.*`
  / `prometheus.execution.*` / `prometheus.persistence.*` /
  network-I/O imports; no test modification; preserved whole-repo
  quality gate.

### Phase 4r — G1 Backtest Execution (docs-and-code) [future, requires Phase 4q first]

- Implement the standalone G1 backtest orchestrator per Phase 4q.
- Run the 32-variant backtest on the predeclared train / validation /
  OOS holdout windows under three cost cells.
- Produce the G1 backtest report.
- Stop. Phase 4r does NOT recommend any successor phase by design.

**Phase 4p does NOT authorize Phase 4q or Phase 4r.** Authorization
is a separate operator decision. Phase 4p RECOMMENDS Phase 4q as
the primary next-step option.

---

## What this does not authorize

Phase 4p explicitly does NOT authorize:

- **Phase 4q backtest-plan memo.** Recommended but NOT authorized.
- **Phase 4r backtest execution.** NOT authorized.
- **G1 implementation under `src/prometheus/strategy/`.** NOT
  authorized.
- **G1 paper / shadow runtime.** FORBIDDEN.
- **G1 live-readiness work.** FORBIDDEN.
- **G1 exchange-write capability.** FORBIDDEN.
- **G1-prime / G2 / G1-relaxed / G1-narrow / G1 hybrid spec.** Not
  defined; not authorized.
- **V2 / F1 / D1-A / R2 rescue.** All forbidden per Phase 4m.
- **Phase 4g V2 strategy-spec amendment.** Preserved verbatim.
- **Phase 4j §11 metrics OI-subset rule amendment.** Preserved
  verbatim.
- **Phase 4k V2 backtest-plan methodology amendment.** Preserved
  verbatim.
- **§11.6 / §1.7.3 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r
  §8 modification.** All preserved verbatim.
- **R3 / H0 / V1 strategy spec revision.** Preserved.
- **5m research thread reopening.** Phase 3t preserved.
- **Mark-price 30m / 4h acquisition.** Deferred per Phase 4h §20.
- **`aggTrades` acquisition.** Deferred per Phase 4h §7.E.
- **v003 dataset creation.** NOT authorized.
- **Manifest modification.** All Phase 4i / v002 / v001-of-5m
  manifests preserved verbatim.
- **Reconciliation implementation.** Phase 4e design preserved
  verbatim, not implemented.
- **Phase 4 (canonical).** Per `docs/12-roadmap/phase-gates.md`.

---

## Forbidden-work confirmation

- **No Phase 4q / Phase 4r / Phase 4 canonical / successor phase
  started.**
- **No V2 / V2-prime / V2-narrow / V2-relaxed / V2 hybrid spec
  authored.**
- **No V3 or any new strategy spec authored beyond G1 first spec.**
- **No F1 / D1-A / R2 rescue spec authored.**
- **No threshold grid extended beyond 32 variants.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.** Phase 4p is text-only.
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No `.claude/rules/**` modification.**
- **No data acquired.**
- **No data modified.**
- **No public Binance endpoint consulted.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.** Phase 4p performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No diagnostics run.**
- **No Phase 3o / 3p Q1–Q7 question rerun.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No `scripts/phase4l_v2_backtest.py` execution.**
- **No data acquisition / download / patch / regeneration /
  modification.**
- **No data manifest modification.** All
  `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No Phase 4i manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A / V2 all preserved.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance
  modification.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 4j §11 metrics OI-subset governance modification.**
- **No Phase 4k V2 backtest-plan methodology modification.**
- **No Phase 4f / 4g / 4h / 4i / 4j / 4k / 4l / 4m / 4n / 4o text
  modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md`
  substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`
  substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive
  change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4p branch.** Per Phase 4p brief.
- **No optional ratio-column access in any code.** Phase 4p is
  text-only; no code.
- **No 5m Q1-Q7 finding used as feature or threshold.**
- **No V2 Phase 4l forensic number used as design input.**
- **No merge to main.**
- **No successor phase started.**

---

## Remaining boundary

- **Recommended state:** **paused** outside conditional Phase 4q
  authorization. Phase 4p deliverables exist as branch-only
  artefacts pending operator review.
- **Phase 4p output:** docs-only G1 strategy-spec memo + Phase 4p
  closeout artefact.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files.
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4
  (canonical) remains not authorized. Phase 4a–4o all merged. Phase
  4p G1 strategy-spec memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **Metrics OI-subset partial-eligibility governance:** Phase 4j §11
  (preserved verbatim; unused by G1 first spec).
- **V2 backtest methodology governance:** Phase 4k (preserved
  verbatim; reusable as template for future Phase 4q G1 backtest-
  plan memo).
- **V2 first-spec terminal verdict:** Phase 4l Verdict C HARD REJECT
  (preserved verbatim).
- **Phase 4m post-V2 strategy research consolidation:** complete
  (preserved verbatim); 18-requirement fresh-hypothesis validity
  gate binding.
- **Phase 4n fresh-hypothesis discovery:** complete (preserved
  verbatim); Candidate B selected.
- **Phase 4o G1 hypothesis-spec:** complete (preserved verbatim).
- **G1 strategy spec:** predeclared by Phase 4p (this phase).
  Conditional on separate operator authorization, Phase 4q would
  proceed to a docs-only G1 backtest-plan memo.
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **OPEN ambiguity-log items after Phase 4p:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A / V2 retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; V2
  HARD REJECT (Phase 4l, structural CFP-1 critical, terminal for V2
  first-spec); §11.6 = 8 bps HIGH per side; §1.7.3 project-level
  locks; mark-price stops; v002 verdict provenance; Phase 3q
  mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4p/g1-strategy-spec-memo` exists locally
  and (after push) on `origin`. NOT merged to main.

---

## Operator decision menu

### Option A — Phase 4q G1 Backtest-Plan Memo (PRIMARY RECOMMENDATION)

Authorize a separate **docs-only** Phase 4q — G1 Backtest-Plan Memo
that predeclares the exact backtest methodology, script structure,
data-loading interface, classifier implementation algorithm, trade
simulation algorithm, M1 / M2 / M3 / M4 computation algorithms,
CFP-1..CFP-12 evaluation algorithms, reporting table schemas, stop-
condition matchers, verdict-taxonomy decision tree, and
reproducibility requirements. Phase 4q would NOT acquire data, NOT
run backtests, NOT implement code.

### Option B — Remain paused (CONDITIONAL SECONDARY)

If the operator prefers not to commit to Phase 4q, remain paused.

### Option C — Phase 4r immediate execution (REJECTED)

A backtest before Phase 4q backtest-plan is data-snooping risk.
REJECTED.

### Option D — G1 implementation under `src/prometheus/strategy/` (REJECTED)

Implementation requires successful backtest evidence. REJECTED.

### Option E — V2 / F1 / D1-A / R2 rescue (REJECTED / FORBIDDEN)

Per Phase 4m §"Forbidden rescue observations".

### Option F — Paper / shadow / live / exchange-write / Phase 4 canonical (FORBIDDEN)

Per `docs/12-roadmap/phase-gates.md`.

### Phase 4p recommendation

**Phase 4p recommendation: Option A (Phase 4q — G1 Backtest-Plan
Memo, docs-only) primary; Option B (remain paused) conditional
secondary.** Options C / D / E / F not recommended / rejected /
forbidden.

---

## Next authorization status

**No next phase has been authorized.** Phase 4p's recommendation is
**Option A (Phase 4q — G1 Backtest-Plan Memo, docs-only) as
primary**, with **Option B (remain paused) as conditional
secondary**. Other options not recommended / rejected / forbidden.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b script-scope quality-gate restoration
is complete (per Phase 4b). The Phase 4c state-package quality-gate
residual cleanup is complete (per Phase 4c). The Phase 4d
post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e
reconciliation-model design memo is complete (per Phase 4e). The
Phase 4f V2 hypothesis predeclaration is complete (per Phase 4f).
The Phase 4g V2 strategy spec is complete (per Phase 4g). The Phase
4h V2 data-requirements / feasibility memo is complete (per Phase
4h). The Phase 4i V2 public data acquisition + integrity validation
is complete (per Phase 4i; partial-pass). The Phase 4j V2 metrics
data governance memo is complete (per Phase 4j; Phase 4j §11
binding). The Phase 4k V2 backtest-plan memo is complete (per
Phase 4k; methodology binding). The Phase 4l V2 backtest execution
is complete (per Phase 4l; Verdict C HARD REJECT terminal for V2
first-spec). The Phase 4m post-V2 strategy research consolidation
memo is complete (per Phase 4m; 18-requirement validity gate
binding). The Phase 4n fresh-hypothesis discovery memo is complete
(per Phase 4n; Candidate B selected). The Phase 4o G1 hypothesis-
spec memo is complete (per Phase 4o). The Phase 4p G1 strategy-
spec memo is complete on this branch (this phase).

**Recommended state remains paused outside conditional Phase 4q
backtest-plan memo. No next phase authorized.**
