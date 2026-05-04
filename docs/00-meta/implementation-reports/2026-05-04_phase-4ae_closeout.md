# Phase 4ae Closeout

## Summary

Phase 4ae authored the **Alt-Symbol Substrate-Feasibility Analysis Memo** (analysis-and-docs only) on branch `phase-4ae/alt-symbol-substrate-feasibility-analysis`. Phase 4ae implemented `scripts/phase4ae_alt_symbol_substrate_feasibility.py` (standalone analysis script; reads existing local Parquet only; no network I/O; no API calls; no acquisition; no `prometheus.runtime/execution/persistence` imports) and computed descriptive substrate-feasibility metrics for the Phase 4ac core symbol set (BTCUSDT / ETHUSDT / SOLUSDT / XRPUSDT / ADAUSDT) at intervals 15m / 30m / 1h / 4h, under Phase 4ad Rule B1 (common post-gap start at 2022-04-03 00:00 UTC). The analysis covered 20 (symbol, interval) cells with 0 omitted and 0 missing bars in span; SOL / XRP cells used Phase 4ad Rule B1 governance scope without flipping any `research_eligible` flag; mark-price (Phase 4ad Rule A) was deferred per brief recommendation; metrics / OI and aggTrades / tick / order-book remained out of scope. **Phase 4ae is analysis-and-docs only.** No data acquired or modified. No manifest created or modified. No backtest run. No strategy diagnostics. No Q1–Q7 rerun. No strategy candidate / hypothesis-spec / strategy-spec / backtest-plan created. No `src/prometheus/`, tests, or existing scripts modified. No retained verdict revised. No project lock changed. No governance file amended (beyond the narrow `current-project-state.md` update). **No successor phase authorized.** **Phase 4z / Phase 4aa / Phase 4ab recommendations all remain recommendations only.** **Phase 4ac results remain data / integrity evidence only.** **Phase 4ad Rules A / B / C remain prospective future-use scope rules only; Phase 4ae used Rule B1 verbatim as default cross-symbol scope and did NOT broaden Rule A / B / C beyond their prospective analysis-time scope.**

## Phase 4ae title

**Phase 4ae — Alt-Symbol Substrate-Feasibility Analysis Memo** (analysis-and-docs only).

## Branch

`phase-4ae/alt-symbol-substrate-feasibility-analysis`

## Base main SHA

`10f122e7be70a4080b181573e07a73c88227b0bb`

## Files created

```text
scripts/phase4ae_alt_symbol_substrate_feasibility.py  (new; standalone analysis;
                                                       no network I/O; no API
                                                       calls; ruff clean;
                                                       py compile clean)
docs/00-meta/implementation-reports/2026-05-04_phase-4ae_alt-symbol-substrate-feasibility-analysis.md
                                                       (new; main memo)
docs/00-meta/implementation-reports/2026-05-04_phase-4ae_closeout.md
                                                       (new; this file)
```

## Files updated

```text
docs/00-meta/current-project-state.md  (narrow Phase 4ae paragraph addition;
                                         no broad refresh)
```

## Script created

```text
scripts/phase4ae_alt_symbol_substrate_feasibility.py   (standalone analysis;
                                                        no network I/O;
                                                        no Binance API;
                                                        no data.binance.vision;
                                                        no authenticated REST;
                                                        no private endpoints;
                                                        no public-endpoint
                                                          code calls;
                                                        no WebSocket;
                                                        no user stream;
                                                        no listenKey;
                                                        no exchange-write;
                                                        no MCP / Graphify /
                                                          .mcp.json;
                                                        no credentials;
                                                        no .env;
                                                        no prometheus.runtime
                                                          / execution /
                                                          persistence imports;
                                                        ruff clean;
                                                        py compileall clean;
                                                        deterministic;
                                                        reads only local
                                                          Parquet under
                                                          data/normalized/)
```

## Analysis outputs (local only; NOT committed)

Local outputs were generated under gitignored `data/research/phase4ae/`:

```text
data/research/phase4ae/run_metadata.json
data/research/phase4ae/tables/
  coverage.csv
  kline_metrics.csv
  funding_metrics.csv
  omitted_datasets.csv
  cross_symbol_rankings.csv
  funding_rankings.csv
```

`data/research/phase4ae/` is gitignored per existing `data/research/**` rule. **Local outputs are NOT committed.** They are reproducible by re-running the orchestrator script with the same defaults.

## Analysis-and-docs status

Phase 4ae is **analysis-and-docs**. Phase 4ae added one standalone analysis script, two committed report markdown files, and a narrow `current-project-state.md` update. Local analysis outputs are gitignored. **No source code under `src/prometheus/` modified. No tests modified. No existing scripts modified. No existing manifests modified. No data acquired. No data modified.**

## No data acquisition / download / API calls / endpoint calls

Phase 4ae did NOT:

- acquire any data;
- download any data;
- call `data.binance.vision`;
- call any Binance API;
- call any authenticated REST endpoint;
- call any private endpoint;
- call any public endpoint from code;
- consult any user stream / WebSocket / listenKey lifecycle;
- use any credentials or `.env`;
- enable any network I/O.

The analysis script reads only local Parquet files under `data/normalized/` and read-only inspects committed manifests under `data/manifests/`.

## No raw / normalized data modification

Phase 4ae did NOT:

- modify any raw archive under `data/raw/`;
- modify any normalized Parquet under `data/normalized/`;
- patch / forward-fill / interpolate / impute / synthesize / regenerate / replace any data;
- silently drop or relax integrity gates.

## No manifest creation / modification / v003

Phase 4ae did NOT:

- create any new manifest;
- modify any existing manifest;
- create v003 or any other dataset version;
- flip any `research_eligible` flag;
- modify Phase 4ac manifests.

## No backtests / strategy diagnostics / Q1–Q7 rerun

Phase 4ae did NOT:

- run any backtest (no Phase 2 / 3 / 4l / 4r / 4x rerun; no new backtest);
- run any strategy diagnostic;
- rerun Q1–Q7;
- compute strategy PnL;
- compute entry / exit strategy returns;
- optimize parameters;
- select thresholds for a future strategy.

## No strategy created

Phase 4ae did NOT:

- create a new strategy candidate;
- name a new strategy;
- create a fresh-hypothesis discovery memo;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create R3-prime / R2-prime / F1-prime / D1-A-prime / V2-prime / G1-prime / C1-prime / V1-D1 / F1-D1 / any cross-strategy hybrid;
- create any "rescue" or "improvement" of R3 / R2 / F1 / D1-A / V2 / G1 / C1.

## No prior verdict revised

Phase 4ae preserved every retained verdict verbatim:

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread remains CLOSED operationally.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

No retained verdicts were revised.

## No locks changed

Phase 4ae preserved every project lock verbatim:

- §11.6 HIGH cost = 8 bps per side.
- §1.7.3 project-level locks: 0.25% risk; 2× leverage; one position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule (preserved; not invoked by Phase 4ae).
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec.
- Phase 4w C1 backtest-plan methodology.

No project locks changed.

## Phase 4ad rules applied prospectively only

Phase 4ad Rules A / B / C remain prospective future-use scope rules only.

- **Rule B1 — common post-gap start at 2022-04-03 00:00 UTC** was applied verbatim as the default cross-symbol scope for the Phase 4ae analysis. SOL / XRP kline-derived conclusions are labeled `conditional on Phase 4ad Rule B1 common post-gap scope`. **No `research_eligible` flag was flipped. No manifest was modified.**
- **Rule A — Mark-Price Invalid-Window Exclusion Rule** was NOT invoked. Mark-price datasets were NOT used by Phase 4ae. Mark-price-dependent analysis is deferred per the Phase 4ae brief recommendation; any future analysis that uses mark-price datasets would apply Rule A verbatim.
- **Rule C — PASS-Only Subset Rule** was NOT used exclusively; Rule B1 was the primary scope. PASS subset cells (BTC 1h, ETH 1h, ADA 15m / 30m / 1h / 4h, SOL / XRP / ADA funding) were included in the Rule B1 window alongside the Rule B1-governed SOL / XRP klines.

**Phase 4ae did NOT broaden Phase 4ad Rules A / B / C beyond their prospective analysis-time scope.** Phase 4ad rules remain prospective future-use only; they apply at analysis time and do not modify on-disk data or manifests.

## Recommendation from Phase 4ae memo

```text
Primary recommendation:
Option A — remain paused. The Phase 4ae descriptive substrate-feasibility
metrics are recorded; no strategy candidate is implied. Any further forward
motion is operator-driven.

Conditional secondary:
Option C — future narrower follow-up feasibility memo (only if separately
authorized). NOT recommended over remain-paused.

NOT recommended:
Option B — fresh-hypothesis discovery memo immediately. Premature; the
Phase 4ae descriptive evidence does not by itself justify a candidate, and
the project's six-failure topology (R2 / F1 / D1-A / V2 / G1 / C1) advises
against substrate-driven candidate selection.

FORBIDDEN:
- old-strategy alt-symbol rerun;
- direct strategy-spec memo on alt symbols;
- backtest / paper / shadow / live;
- mark-price feasibility memo without Phase 4ad Rule A predeclaration.
```

## Strongest substrate-feasibility findings (descriptive only)

- **Cost-cushion ranking is consistent across all four intervals: SOL > ADA > XRP > ETH > BTC** (most cushion to least). BTC has the tightest cost cushion at every interval.
- **BTC is the most cleanly trending substrate** over the analysis window: ≈ 50–52% of bars have close > EMA(50) and ≈ 50–52% have EMA(50) > EMA(200) at every interval; balanced across regimes.
- **SOL has the widest funding distribution** (abs p95 = 4.5 bps; ≈ 2.5× wider than BTC's 1.6 bps); SOL's funding flips sign more often than BTC / ETH.
- **BTC's median kline-notional turnover dwarfs the alts** by ≈ 1–2 orders of magnitude. ADA is the thinnest by this proxy (≈ 0.025× BTC).
- **All 20 (symbol, interval) cells produced complete coverage** in the Phase 4ad Rule B1 window with zero missing bars in the observed span.

## Weakest substrate-feasibility findings (descriptive only)

- **No single symbol dominates on every dimension.** The ranking depends on which dimension is prioritized.
- **Wick-fraction differences across symbols are small at the median.** Substrate-level wick behavior is similar across BTC / ETH / SOL / XRP / ADA; trade-price-only wick proxies do NOT strongly differentiate substrates.
- **Absolute-return-expansion frequency is roughly uniform** across symbols (≈ 32–35% of bars exceed 1.5× rolling-median |return|).
- **ADA's lower kline-notional turnover and weaker HTF trend dominance** are descriptive caveats; the lower kline notional is consistent with thinner top-of-book depth but does NOT prove it (kline notional is NOT order-book depth and does NOT support slippage inference).
- **Mark-price stop-pathology behavior is unmeasured** in this memo (deferred per Phase 4ae brief). Phase 3s Q2 5m diagnostic on BTC established V1-family wick-fractions of 0.571–1.000 on adverse stop exits; alt-symbol equivalents would require mark-price + Phase 4ad Rule A invocation in a future authorized memo.

## No successor phase authorized

Phase 4ae does NOT authorize:

- Phase 4af (any kind);
- Phase 5;
- Phase 4 canonical;
- any other named successor phase.

The next step is operator-driven: the operator decides whether to remain paused (with or without merging Phase 4ae) or authorize Phase 4af (or some other phase).

## Working tree / git status evidence

Working tree at memo creation time:

```text
On branch phase-4ae/alt-symbol-substrate-feasibility-analysis
Untracked files (gitignored transients only; not committed):
  .claude/scheduled_tasks.lock
  data/research/        (gitignored; contains Phase 4ae local outputs)
  data/raw/binance_usdm/    (gitignored)
  data/normalized/      (gitignored)
nothing added to commit but untracked files present
```

Repository state at base:

```text
main / origin/main: 10f122e7be70a4080b181573e07a73c88227b0bb (unchanged)
Phase 4ad merge commit:                10f122e7be70a4080b181573e07a73c88227b0bb
Phase 4ad memo commit:                 7b4a0d9f949692cefe36cbd757ef8414166d6071
Phase 4ae branch:                      phase-4ae/alt-symbol-substrate-feasibility-analysis (this branch)
```

Quality gates status: ruff PASS on the Phase 4ae script; py compileall PASS. Whole-repo pytest / ruff / mypy not re-run (Phase 4ae adds only one new analysis script that does not touch `src/prometheus/`, tests, or any existing script). Last-known clean state: ruff PASS; mypy strict 0 issues across 82 source files (verified during Phase 4ac).

## Forbidden-work confirmation

Phase 4ae did NOT do any of the following:

- run a backtest (any phase);
- run any acquisition / diagnostics script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`, `scripts/phase4ac_alt_symbol_acquisition.py`);
- acquire data;
- download data;
- patch / forward-fill / interpolate / impute / synthesize / regenerate / replace any data;
- modify any manifest;
- create any new manifest;
- create v003;
- flip any Phase 4ac `research_eligible` flag;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- amend the Phase 4aa admissibility framework;
- amend the Phase 4ab data-requirements / feasibility framework;
- amend the Phase 4ad gap-governance / scope-revision rules;
- broaden Phase 4ac results into binding cross-project governance;
- broaden Phase 4ad Rules A / B / C beyond their prospective analysis-time scope;
- modify any specialist governance file beyond the narrow `docs/00-meta/current-project-state.md` update;
- adopt any Phase 4z recommendation as binding governance;
- adopt the Phase 4aa admissibility framework as binding governance;
- adopt any Phase 4ab recommendation as binding governance;
- adopt Phase 4ac results as binding governance;
- broaden Phase 4ad rules as binding governance;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create a hypothesis-spec memo;
- create a strategy-spec memo;
- create a backtest-plan memo;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 4af / Phase 5 / Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- merge Phase 4ae to main (the branch is preserved; merge would require separate operator instruction).

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal; preserved)
G1                  : HARD REJECT (Phase 4r terminal; preserved)
C1                  : HARD REJECT (Phase 4x terminal; preserved)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : project-level locks preserved
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4j §11                : metrics OI-subset partial-eligibility rule (preserved;
                              not invoked by 4ae)
Phase 4k                    : V2 backtest-plan methodology (preserved)
Phase 4p                    : G1 strategy spec (preserved)
Phase 4q                    : G1 backtest-plan methodology (preserved)
Phase 4v                    : C1 strategy spec (preserved)
Phase 4w                    : C1 backtest-plan methodology (preserved)
Phase 4z recommendations    : remain recommendations only; NOT adopted by 4ae
Phase 4aa admissibility framework : remain recommendation only; NOT adopted by 4ae
Phase 4ab recommendations   : remain recommendations only; NOT adopted by 4ae
Phase 4ac results           : data / integrity evidence only
Phase 4ad Rules A / B / C   : prospective future-use scope rules only;
                              Phase 4ae used Rule B1 verbatim as default
                              cross-symbol scope; Rule A not invoked
                              (mark-price deferred); Rule C-style PASS-only
                              cells included alongside Rule B1-governed cells.
                              No flag flipped. No manifest modified. Rules
                              not broadened beyond prospective scope.
Phase 4ae                   : Alt-symbol substrate-feasibility analysis memo
                              (this phase; new; analysis-and-docs only;
                              feature-branch only; not merged)
Recommended state           : remain paused (primary; Option A);
                              future docs-only narrower follow-up feasibility
                              memo (conditional secondary; not authorized
                              by Phase 4ae)
```

## Next authorization status

```text
Phase 4af / Phase 5 / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
Public endpoint calls in code      : NOT authorized
User stream / WebSocket            : NOT authorized
Exchange-write capability          : NOT authorized
MCP / Graphify                     : NOT authorized
.mcp.json / credentials            : NOT authorized
C1 / V2 / G1 / R2 / F1 / D1-A rescue : NOT authorized; FORBIDDEN
C1-prime / V2-prime / G1-prime /
  R2-prime / F1-prime / D1-A-prime  : NOT authorized; FORBIDDEN
Old-strategy alt-symbol re-run     : NOT authorized; FORBIDDEN (retrospective rescue)
Adoption of Phase 4z recommendations
  as binding governance            : NOT authorized
Adoption of Phase 4aa admissibility
  framework as binding governance  : NOT authorized
Adoption of Phase 4ab recommendations
  as binding governance            : NOT authorized
Broadening of Phase 4ac results
  beyond data / integrity evidence : NOT authorized
Broadening of Phase 4ad Rules
  beyond prospective scope         : NOT authorized
Alt-symbol fresh-hypothesis memo   : NOT authorized
Alt-symbol strategy-spec memo      : NOT authorized
Alt-symbol backtest-plan memo      : NOT authorized
Alt-symbol backtest execution      : NOT authorized
Mark-price stop-domain feasibility
  memo (Phase 4ad Rule A applied)  : NOT authorized; conditional alternative
Future narrower follow-up
  substrate-feasibility memo       : NOT authorized; conditional secondary
Spot / COIN-M / options / cross-
  venue expansion                  : NOT authorized; not recommended
Phase 4ae merge to main            : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4ae to main, or take some other action. Until then, the project remains at the post-Phase-4ad merge boundary on `main` with Phase 4ae preserved on its feature branch.

---

**Phase 4ae is analysis-and-docs only. main remains unchanged at `10f122e7be70a4080b181573e07a73c88227b0bb`. Phase 4ae added one standalone analysis script, two report markdown files, and a narrow `current-project-state.md` update; local analysis outputs under gitignored `data/research/phase4ae/` are NOT committed. Phase 4ae did NOT modify Phase 4ac manifests, did NOT flip any `research_eligible` flag, did NOT broaden Phase 4ac results into binding cross-project governance, and did NOT broaden Phase 4ad Rules beyond their prospective analysis-time scope. Phase 4z, Phase 4aa, Phase 4ab recommendations all remain recommendations only — not binding governance. C1 / V2 / G1 first-specs remain terminally HARD REJECTED. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. Recommended state: remain paused (primary; Option A). No next phase authorized.**
