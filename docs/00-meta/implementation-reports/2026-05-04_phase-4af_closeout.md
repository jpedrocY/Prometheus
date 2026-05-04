# Phase 4af Closeout — Alt-Symbol Regime-Continuity and Directional-Persistence Feasibility Memo

## Phase identity

- Phase title: Alt-Symbol Regime-Continuity and Directional-Persistence
  Feasibility Memo
- Phase status: analysis-and-docs only
- Phase branch: `phase-4af/alt-symbol-regime-continuity-persistence`
- Base main SHA: `c57afa4447ad4e8ae3c12ac2c26891c612f03a57`

## Files created

```text
scripts/phase4af_alt_symbol_regime_persistence.py
docs/00-meta/implementation-reports/2026-05-04_phase-4af_alt-symbol-regime-continuity-persistence.md
docs/00-meta/implementation-reports/2026-05-04_phase-4af_closeout.md
```

## Files updated narrowly

```text
docs/00-meta/current-project-state.md   (Phase 4af paragraph added; prior phase preserved)
```

## Local analysis outputs (gitignored; NOT committed)

```text
data/research/phase4af/run_metadata.json
data/research/phase4af/tables/coverage.csv
data/research/phase4af/tables/trend_state_persistence.csv
data/research/phase4af/tables/trend_state_transitions.csv
data/research/phase4af/tables/ema_slope_persistence.csv
data/research/phase4af/tables/post_expansion_followthrough.csv
data/research/phase4af/tables/sign_persistence.csv
data/research/phase4af/tables/vol_regime_persistence.csv
data/research/phase4af/tables/cost_continuation_sufficiency.csv
data/research/phase4af/tables/cross_symbol_rankings.csv
data/research/phase4af/tables/omitted_datasets.csv
```

## Phase 4af summary

Phase 4af computed descriptive regime-continuity and
directional-persistence metrics for the Phase 4ac core symbol set
(`BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`) at intervals
`15m`, `30m`, `1h`, `4h`, under Phase 4ad Rule B1 common post-gap scope
(`2022-04-03 00:00 UTC` through `2026-04-30 23:59:59 UTC`).

Phase 4af processed 20 (symbol, interval) cells with 0 omitted datasets
and 0 missing bars in observed span. Mark-price datasets were not used
(Phase 4ad Rule A deferred per brief recommendation). Metrics / OI were
not used. AggTrades / tick / order-book were not used. Funding history
was not used.

Phase 4af findings (descriptive substrate-feasibility evidence only):

- Trend-state self-transition probabilities are uniformly very high
  (`P(UP self)` range 0.919–0.940; `P(DOWN self)` range 0.923–0.940)
  across all 20 cells. There is no differentiating cross-symbol edge.
- EMA-slope self-transition probabilities are uniformly very high
  (range 0.94–0.96 both directions). No differentiating edge.
- Post-expansion same-direction follow-through fractions are at or
  below 0.50 across all 80 (symbol, interval, N ∈ {1, 2, 4, 8}) cells.
  No same-direction substrate bias.
- Bar-level sign persistence (`frac_sign_repeats_next_1`) is
  consistently slightly below 0.50; lag-1 return autocorrelation is near
  zero on every cell. No directional-persistence advantage.
- Volatility-regime self-transition probabilities are uniformly high
  (0.91–0.94). High-vol regime is direction-agnostic.
- Cost-adjusted absolute movement (>16 bps over 4 bars) frequencies grow
  from ~0.58 (BTC 15m) to ~0.95 (SOL 4h); UP-state and DOWN-state
  conditional fractions are within ±2 percentage points of unconditional.
  Trend conditioning provides no cost-adjusted directional advantage.
- Phase 4ae cost-cushion ranking `SOL > ADA > XRP > ETH > BTC` is
  descriptively confirmed at coarser intervals.

## Boundary confirmations

Phase 4af did **NOT**:

- acquire data;
- download data;
- call `data.binance.vision`;
- call Binance APIs;
- call any authenticated REST endpoint;
- call any private endpoint;
- call any public endpoint from code;
- consult user stream / WebSocket / listenKey lifecycle;
- use credentials or `.env`;
- enable network I/O;
- modify any raw or normalized data;
- create any new manifest;
- modify any existing manifest;
- create v003 or any other dataset version;
- run any backtest;
- run any strategy diagnostic;
- rerun Q1–Q7;
- compute strategy PnL;
- compute entry / exit strategy returns;
- optimize parameters;
- select thresholds for a future strategy;
- create a new strategy candidate;
- name a new strategy;
- create a fresh-hypothesis discovery memo;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- modify `src/prometheus/`, tests, or existing scripts;
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime /
  G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;
- amend any specialist governance file (beyond the narrow
  `current-project-state.md` update);
- adopt any Phase 4z / Phase 4aa / Phase 4ab recommendation as binding
  governance;
- broaden Phase 4ac results into binding cross-project governance;
- broaden Phase 4ad Rules A / B / C beyond their prospective
  analysis-time scope;
- broaden Phase 4ae findings beyond descriptive substrate-feasibility
  evidence;
- authorize Phase 4ag / Phase 5 / Phase 4 canonical / any successor
  phase;
- authorize paper / shadow / live / exchange-write / production keys /
  authenticated APIs / private endpoints / user stream / WebSocket /
  MCP / Graphify / `.mcp.json` / credentials.

## Retained verdicts (preserved verbatim)

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

## Project locks (preserved verbatim)

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

## Phase 4af recommendation

Primary: `Option A — remain paused.`

Conditional secondary: `Option B — future narrower follow-up feasibility
memo`, only if separately authorized and clearly framed so as to not
become a strategy spec; not started by Phase 4af.

NOT recommended: `Option C — fresh-hypothesis discovery memo` at this
time.

NOT recommended: `Option D — mark-price stop-domain feasibility under
Phase 4ad Rule A` at this time.

FORBIDDEN: paper / shadow / live / exchange-write / production keys /
authenticated APIs / private endpoints / user stream / WebSocket / MCP
/ Graphify / `.mcp.json` / credentials.

## Successor authorization status

```text
Phase 4ag                  : NOT authorized
Phase 5                    : NOT authorized
Phase 4 canonical          : NOT authorized
any other successor phase  : NOT authorized
```

## Recommended state

```text
remain paused unless the operator separately authorizes a future phase
```
