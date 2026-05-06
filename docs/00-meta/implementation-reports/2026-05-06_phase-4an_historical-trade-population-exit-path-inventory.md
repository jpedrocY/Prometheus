# Phase 4an — Historical Trade-Population Exit-Path Inventory Memo

## 1. Executive Summary

Phase 4an is a docs-only static inventory of which historical Prometheus
strategy/research populations have sufficient artefacts to support possible
future MFE/MAE, realized-R, exit-path, stop-path, take-profit, and
winner/loser path forensic analysis.

This memo does NOT perform any forensic analysis. It does NOT compute
distributions. It does NOT acquire data. It does NOT modify code, scripts,
data, manifests, retained verdicts, project locks, or governance. It does
NOT authorize any successor phase, including Phase 4ao, Phase 5, Phase 4
canonical, paper / shadow, live-readiness, deployment, exchange-write,
production keys, authenticated APIs, private endpoints, public-endpoint
calls in code, user stream, WebSocket, MCP, Graphify, `.mcp.json`, or
credentials. It does NOT authorize 5m / 1m / aggTrades / tick-data
acquisition. It does NOT reopen the Phase 3t–CLOSED 5m strategy thread.

The populations inventoried are: H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2,
G1, C1, and the 5m research thread (closed historical context only).

Headline result, in plain language:

- **V1-arc populations (H0, R3, R1a, R1b-narrow, R2)**: per-trade trade
  ledgers exist locally with `mfe_r` / `mae_r` already populated from 15m
  bar highs / lows during the trade lifetime, plus all entry / exit
  prices, timestamps, fees, slippage, funding, gross / net PnL, realized R,
  initial stop, and exit-reason fields. **Static MFE/MAE forensics on V1-arc
  populations is feasible from existing artefacts, with bar-resolution
  caveats.**
- **F1 (Phase 3d-B2) and D1-A (Phase 3j)**: per-trade trade ledgers exist
  locally with the same `trade_log_v1` schema as V1-arc, BUT `mfe_r` and
  `mae_r` are systematically populated as `0.0` because F1 and D1-A
  strategies do NOT use the V1 breakout `TradeManagement` excursion-tracking
  module; the engine returns `0.0` when `active.management is None`. All
  other realized-R / cost / timestamp fields are present and usable. **MFE/MAE
  forensics on F1 / D1-A would require either a controlled rerun with
  excursion instrumentation OR offline reconstruction from the existing
  v002 BTCUSDT / ETHUSDT 15m bars over each trade's entry-to-exit window.**
- **V2 (Phase 4l), G1 (Phase 4r), C1 (Phase 4x)**: standalone research
  scripts emit only aggregate variant-level CSV tables. No per-trade ledger
  is persisted. V2 in-memory tracks `mfe_R` (using 30m `bar_high` /
  `bar_low`) but does not track MAE. G1 and C1 do not track MFE or MAE at
  all in memory. **Per-trade exit-path forensics on V2 / G1 / C1 requires
  rerun under script modifications, and MAE / partial-bar resolution
  questions would require either lower-timeframe data or design-stage
  redefinition of what "path" means for these populations.**
- **5m research thread**: operationally CLOSED per Phase 3t. No strategy
  trade ledger was ever produced because the 5m thread was diagnostic
  (Q1–Q7) only, not strategy-running. **No exit-path forensics is allowed
  on the 5m thread except as closed historical context.**

The inventory yields **no rescue-licensed conclusions**. Every retained
verdict (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow
retained — non-leading; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM
PASS / FRAMEWORK FAIL; V2 / G1 / C1 HARD REJECT — terminal first-spec) is
preserved. Every project lock (§11.6 = 8 bps per side; §1.7.3 0.25% / 2× /
one-position / mark-price stops; Phase 3r §8; Phase 3v §8; Phase 3w §6 /
§7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; M0
governance per Phase 4ak) is preserved verbatim.

The recommendation is **remain paused** as primary. A narrower future
docs-only methodology / artefact harmonization memo is acceptable as a
conditional secondary alternative if separately authorized; full exit-path
forensic analysis is acceptable only as a conditional tertiary alternative
if separately authorized after harmonization, and is not preferred over
remain-paused.

## 2. Scope and Explicit Non-Scope

### 2.1 In scope

- Static repository inspection of existing docs, scripts, reports,
  manifests, and existing artefacts.
- Per-population determination of which trade-ledger fields exist.
- Per-population classification of artefact sufficiency for future
  forensics.
- Per-population identification of forbidden rescue-risk pathways.
- Per-population identification of allowed future forensic uses.
- Authoring this docs-only memo and a narrow update to
  `docs/00-meta/current-project-state.md`.

### 2.2 Explicit non-scope

Phase 4an does NOT and is NOT authorized to:

- compute MFE / MAE distributions, time-to-MFE, time-to-stop, target-before-stop
  sequencing, or any other path statistic;
- run any backtest;
- run, modify, or otherwise execute any historical strategy or research script
  (`scripts/phase2*.py`, `scripts/phase3d_F1_execution.py`,
  `scripts/phase3j_D1A_execution.py`, `scripts/phase3q_5m_acquisition.py`,
  `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`,
  `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`,
  `scripts/phase4x_c1_backtest.py`,
  `scripts/phase4ac_alt_symbol_acquisition.py`,
  `scripts/phase4ae_alt_symbol_substrate_feasibility.py`,
  `scripts/phase4af_alt_symbol_regime_persistence.py`,
  `scripts/phase4ai_single_position_cross_sectional_trend.py`);
- run any new research script;
- acquire data;
- modify any data file under `data/raw/`, `data/normalized/`,
  `data/derived/`, or `data/research/`;
- modify any manifest under `data/manifests/`;
- modify any source file under `src/prometheus/`;
- modify any test under `tests/`;
- modify any strategy spec, backtest plan, validation checklist,
  technical-debt register, phase-gates document, ai-coding-handoff document,
  implementation-ambiguity-log, or M0 governance document
  (`docs/00-meta/m0-mechanism-admissibility-gate.md`);
- modify any retained verdict;
- modify any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8, Phase 3w
  §6/§7/§8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w);
- propose, name, or pre-design a new strategy or exit system;
- propose a rescue of any rejected or retained-evidence candidate;
- analyze winners' anatomy, losers' anatomy, exit ambiguity, or stop-path
  divergence;
- authorize Phase 4ao, Phase 5, Phase 4 canonical, paper/shadow,
  live-readiness, deployment, exchange-write, production-key creation,
  authenticated APIs, private endpoints, public-endpoint calls in code,
  user stream, WebSocket, listenKey, MCP, Graphify, `.mcp.json`, or
  credentials;
- authorize acquisition of 5m, 1m, aggTrades, tick, mark-price 30m / 4h, or
  any other data family.

If a question raised in this memo cannot be answered from static repository
inspection, it is classified explicitly as
`RECONSTRUCTABLE_ONLY_WITH_RERUN`, `NEEDS_LOWER_TIMEFRAME_DATA`, or
`NOT_AUDITABLE_FROM_CURRENT_REPO` rather than triggering execution.

## 3. Repository Verification Summary

Verification commands and results, executed at the start of Phase 4an
on branch `phase-4an/historical-trade-population-exit-path-inventory`:

```text
git status                : clean working tree (untracked .claude/scheduled_tasks.lock
                            and data/research/ are gitignored per repo convention)
git branch --show-current : phase-4an/historical-trade-population-exit-path-inventory
git rev-parse main        : dfaa26a4e7f9a21957e0e465c7bb7de2e508a784
git rev-parse origin/main : dfaa26a4e7f9a21957e0e465c7bb7de2e508a784
```

main and origin/main agree at `dfaa26a4e7f9a21957e0e465c7bb7de2e508a784`,
which is the Phase 4am merge-closeout merge commit. Phase 4al was merged at
`f97f850`; Phase 4am was merged at `9c2c7db`; Phase 4am merge-closeout at
`dfaa26a`. Both Phase 4al and Phase 4am are on main.

The branch for this phase (`phase-4an/historical-trade-population-exit-path-inventory`)
was created from clean main.

## 4. Methodology

Phase 4an methodology is **static repository inspection only**. Specifically:

- Read trade-log JSON / Parquet schema fields by inspecting one
  representative file per population and confirming schema versions.
- Read backtest engine source (`src/prometheus/research/backtest/`) to
  determine which strategies populate `mfe_r` / `mae_r` versus which
  default to `0.0`.
- Read strategy modules (`src/prometheus/strategy/v1_breakout/management.py`,
  `src/prometheus/strategy/mean_reversion_overextension/`,
  `src/prometheus/strategy/funding_aware_directional/`) to determine
  excursion-tracking presence.
- Read standalone research scripts (`scripts/phase4l_v2_backtest.py`,
  `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`) to
  determine in-memory MFE / MAE tracking and persistence behaviour.
- Read directory listings under `data/derived/backtests/` and
  `data/research/phase4l/`, `data/research/phase4r/`, `data/research/phase4x/`
  to determine which artefacts physically exist locally.
- Read existing phase reports under
  `docs/00-meta/implementation-reports/` for context on dataset coverage,
  governance, retained verdicts, and rejection topology.
- Cross-reference findings with the `m0-mechanism-admissibility-gate.md`
  durable governance document and the Phase 4al / Phase 4am audit results.

No script was run during Phase 4an. No backtest was executed. No data was
read other than schema-inspection of existing JSON/Parquet headers and
sample records via `head` / `Read`. No data modification occurred.

## 5. Population Inventory Table

The table summarizes per-population artefact existence and sufficiency
classification. Detailed per-population findings follow in §6. Local
artefact paths quoted below are gitignored (per repo `.gitignore`
convention) but exist on disk for V1-arc / F1 / D1-A populations.

| Population   | Strategy lineage                            | Trade ledger present locally          | mfe_r / mae_r populated  | Per-cost-cell variants present | Sufficiency classification                |
|--------------|---------------------------------------------|---------------------------------------|--------------------------|--------------------------------|-------------------------------------------|
| H0           | V1 breakout (Phase 2e–2g; framework anchor) | YES (Parquet + JSON)                  | YES (15m bar excursion)  | LOW / MEDIUM / HIGH            | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS   |
| R3           | V1 breakout (Phase 2l/2p; baseline-of-record) | YES (Parquet + JSON)                | YES (15m bar excursion)  | LOW / MEDIUM / HIGH; trade-price stop variant | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS |
| R1a          | V1 breakout (Phase 2m; retained — non-leading) | YES (Parquet + JSON)               | YES (15m bar excursion)  | LOW / MEDIUM / HIGH; trade-price stop variant | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS |
| R1b-narrow   | V1 breakout (Phase 2s; retained — non-leading) | YES (Parquet + JSON)               | YES (15m bar excursion)  | LOW / MEDIUM / HIGH; trade-price stop variant | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS |
| R2           | V1 breakout (Phase 2w; FAILED — §11.6)      | YES (Parquet + JSON)                  | YES (15m bar excursion)  | LOW / MEDIUM / HIGH; trade-price stop variant; limit-at-pullback fill variant | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS |
| F1           | mean-reversion-after-overextension (Phase 3d-B2; HARD REJECT) | YES (Parquet + JSON)  | NO (uniformly 0.0; no excursion module) | LOW / MEDIUM / HIGH; trade-price stop variant | RECONSTRUCTABLE_ONLY_WITH_RERUN (for MFE/MAE); RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS for non-excursion fields |
| D1-A         | funding-aware directional (Phase 3j; MECHANISM PASS / FRAMEWORK FAIL) | YES (Parquet + JSON) | NO (uniformly 0.0; no excursion module) | LOW / MEDIUM / HIGH; trade-price stop variant | RECONSTRUCTABLE_ONLY_WITH_RERUN (for MFE/MAE); RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS for non-excursion fields |
| V2           | participation-confirmed trend continuation (Phase 4l; HARD REJECT — terminal) | NO per-trade ledger; aggregate CSV only | NO (in-memory `mfe_R` only; not persisted; no MAE) | aggregate per-variant per cost cell only | RECONSTRUCTABLE_ONLY_WITH_RERUN |
| G1           | regime-first breakout continuation (Phase 4r; HARD REJECT — terminal) | NO per-trade ledger; aggregate CSV only | NO (no MFE / MAE tracking in script) | aggregate per-variant per cost cell only | RECONSTRUCTABLE_ONLY_WITH_RERUN |
| C1           | volatility-contraction expansion breakout (Phase 4x; HARD REJECT — terminal) | NO per-trade ledger; aggregate CSV only | NO (no MFE / MAE tracking in script) | aggregate per-variant per cost cell only | RECONSTRUCTABLE_ONLY_WITH_RERUN |
| 5m thread    | diagnostic-only (Phase 3o–3t; CLOSED per Phase 3t) | NO trade ledger ever produced | N/A (no strategy)        | N/A                            | CLOSED_CONTEXT_ONLY                       |

`RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` means: existing local trade logs
already contain the field of interest, OR the field can be reconstructed
offline by joining the trade log with the existing v002 / v001-of-5m / Phase
4i datasets without re-running the strategy.

`RECONSTRUCTABLE_ONLY_WITH_RERUN` means: the field is not in any local
artefact, and recovering it would require either rerunning the original
strategy/research script (under separate authorization) OR computing it
offline from raw bar data over each trade's entry-to-exit window if the
trade ledger contains both endpoints.

`CLOSED_CONTEXT_ONLY` means: the population is closed at the project level
(per Phase 3t) and is admissible only as historical context, never as
exit-path forensics input.

## 6. Per-Population Findings

The 26-question per-population checklist from the Phase 4an authorization
brief is answered in compact form per population. Field-presence answers
reference the `trade_log_v1` schema (V1-arc / F1 / D1-A) or the V2/G1/C1
in-memory `TradeRecord` and CSV tables.

### 6.1 H0 (V1 breakout framework anchor; Phase 2e–2g)

1. Trade ledger exists: **YES** (locally; gitignored).
2. Location: `data/derived/backtests/phase-2e-baseline/<run-stamp>/<symbol>/`
   for the Phase 2e baseline; `data/derived/backtests/phase-2g-wave1-h0-r/<run-stamp>/<symbol>/`
   for the wave-1 H0 reference run; v variant suffixes indicate validation
   windows.
3. Entry timestamps: **YES** (`entry_fill_time_ms`, `signal_bar_open_time_ms`).
4. Exit timestamps: **YES** (`exit_fill_time_ms`).
5. Entry prices: **YES** (`entry_fill_price`).
6. Exit prices: **YES** (`exit_fill_price`).
7. Initial stop prices: **YES** (`initial_stop`).
8. Target / take-profit prices: **PARTIAL** (V1 R3+ variants use
   fixed-R take-profit; H0 baseline uses staged management without an
   explicit `take_profit_price` field, but `frozen_target_value` records
   structural target where applicable).
9. Realized R: **YES** (`net_r_multiple`).
10. Gross PnL: **YES** (`gross_pnl`).
11. Net PnL: **YES** (`net_pnl`).
12. Fees: **YES** (`entry_fee`, `exit_fee`, `fee_rate_assumption`).
13. Slippage: **YES** (per-cost-cell variants exist:
    `slippage_bucket` ∈ {LOW, MEDIUM, HIGH}; baseline is MEDIUM unless suffix
    indicates `-slip=LOW`/`-slip=HIGH`).
14. Funding: **YES** (`funding_pnl`).
15. Stop / exit reason fields: **YES** (`exit_reason` ∈ {STOP, TAKE_PROFIT,
    TIME_STOP, ...}; `stop_was_gap_through`).
16. Trade side / symbol / timeframe: **YES** (`direction`, `symbol`;
    timeframe is implicit 15m via the V1-arc dataset reference).
17. MFE reconstructable from existing artefacts: **YES** (`mfe_r` is
    populated; computed from 15m `bar.high` / `bar.low` during trade
    lifetime by `TradeManagement._update_excursions` per
    `src/prometheus/strategy/v1_breakout/management.py`).
18. MAE reconstructable from existing artefacts: **YES** (`mae_r` is
    populated; same source).
19. Reconstruction requires rerunning scripts: **NO** for the existing
    artefacts; **OPTIONAL** if future forensics wants additional fields not
    in the current schema.
20. 15m data sufficient: **YES** (the artefacts are themselves 15m-derived;
    further joins use v002 BTCUSDT / ETHUSDT 15m manifests).
21. 5m supplemental usable: **OPTIONAL** (Phase 3q v001-of-5m manifests
    are research_eligible for trade-price 5m; usable only under Phase 4al
    §14 hierarchy guidance and under Phase 4al §13 boundary; not
    authorized by Phase 4an).
22. 1m may be required later: **NO** for V1-arc baseline questions; would
    only be relevant if intra-15m-bar stop / TP sequencing ambiguity
    became material — Phase 4al §14.C bands suggest 5m is the recommended
    first lower-timeframe layer if any escalation is ever authorized.
23. Mark-price path reconstruction: **BLOCKED** under §1.7.3 stop-trigger
    domain governance — V1-arc backtests carry
    `stop_trigger_domain = trade_price_backtest`; mark-price stop-domain
    forensics requires separately authorized work under Phase 3v §8 and
    Phase 4al §14.D, and is NOT authorized by Phase 4an.
24. Forbidden rescue-risk in including: **MEDIUM** — H0 is the framework
    anchor and a path-pattern reading on H0 could easily be misread as
    license to rewrite §11.6 cost assumptions or §1.7.3 locks; refined
    no-rescue rule (Phase 4al §9) applies.
25. Allowed future forensic use: descriptive MFE / MAE / time-to-event
    distributions for H0 only under predeclared methodology; no
    parameter optimization on the H0 trade population; no structural
    feature change to H0; no verdict revision.
26. Forbidden future use: any change to H0 framework anchor; any conversion
    of observed H0 path patterns into a strategy candidate; any
    parameter tuning; any verdict revision; any cost-lock revision.

### 6.2 R3 (V1 breakout baseline-of-record; Phase 2l / 2p)

1–16. Trade ledger and field availability identical to H0 (§6.1). Local
location is `data/derived/backtests/phase-2l-r3-r/<run-stamp>/<symbol>/`
plus per-cost-cell variants
(`phase-2l-r3-r-slip=LOW`, `phase-2l-r3-r-slip=HIGH`) and
`phase-2l-r3-r-stop=TRADE_PRICE`. Validation-window variants are
`phase-2l-r3-v`.
17–18. MFE / MAE: **YES** (15m bar excursion via V1 management module).
19. Reconstruction without rerun: **YES** for MFE/MAE; OPTIONAL rerun for
fields not in current schema.
20. 15m sufficient: **YES**.
21. 5m supplemental usable: **OPTIONAL**, not authorized.
22. 1m may be required later: **NO** for baseline forensics.
23. Mark-price path: **BLOCKED**, see §6.1.
24. Forbidden rescue-risk: **MEDIUM** — R3 is baseline-of-record; any
path-pattern reading on R3 must be guarded against the V2 / G1 / C1
forbidden-rescue list (no V2-prime / G1-prime / C1-prime / R2-prime / etc.;
no R3 rule-set widening).
25. Allowed: descriptive MFE / MAE / time-to-event / target-before-stop
sequencing on R3 trade population only under predeclared methodology and
Phase 4al §11.A audit-hardened cost arithmetic.
26. Forbidden: parameter tuning on R3; introducing a "next-spec-after-R3"
based on R3 forensic numbers; lock revision; verdict revision; conversion
to live-readiness implication.

### 6.3 R1a (V1 breakout retained — non-leading; Phase 2m)

Identical to R3 in artefact availability except local dir is
`phase-2m-r1a-r1a_plus_r3-r/...` plus per-cost-cell and per-stop variants.
R1a is RETAINED — NON-LEADING. Forbidden rescue-risk is **HIGH** here:
R1a is precisely the kind of "per-bar bolt-on filter" the Phase 4n / Phase
4z / Phase 4ak rejection-topology lessons forbid as future rescue scaffold.
Allowed future forensic use is descriptive only and must NOT compare R1a
forensic patterns favourably as license for reactivating R1a. Forbidden:
R1a-prime / R1a-extension / R1a as-cost-relaxed; using R1a forensic
patterns as G1 / V2 / C1 rescue input; per-bar volatility-percentile
filter rescue.

### 6.4 R1b-narrow (V1 breakout retained — non-leading; Phase 2s)

Identical artefact availability to R1a. Local dir is
`phase-2s-r1b-r1b_narrow-r/...`. R1b-narrow is RETAINED — NON-LEADING.
Forbidden rescue-risk is **HIGH** for the same reasons as R1a (bolt-on
bias-strength filter). Allowed: descriptive forensics only. Forbidden:
R1b-narrow-prime / R1b-narrow widening / R1b-narrow as scaffold for V2 /
G1 / C1 rescue.

### 6.5 R2 (V1 breakout FAILED — §11.6; Phase 2w)

1–16. Trade ledger present at `phase-2w-r2-r2_r3-r/...` plus per-cost
variants (`-slip=LOW`, `-slip=HIGH`), per-stop variants
(`-stop=TRADE_PRICE`), per-fill variants (`-fill=limit-at-pullback`).
17–18. MFE / MAE present and populated (15m bar excursion).
19–22. Same as R3.
23. Mark-price path BLOCKED, see §6.1.
24. Forbidden rescue-risk: **CRITICAL**. R2 is the project's clearest cost-
fragility failure (cond_iv §11.6 HIGH cost-resilience FAILED). Any forensic
reading on R2 must be guarded against the explicit Phase 4z / Phase 4m / Phase
4y / Phase 4ak forbidden-rescue list (no R2-prime / R2 with cheaper costs /
R2 with §11.6 relaxation / R2 hybrid). The presence of `-slip=LOW` variants
in the local artefact set heightens this risk.
25. Allowed: descriptive MFE / MAE / time-to-MFE / target-before-stop /
realized-R-after-costs / cost-in-R / fee-in-R / slippage-in-R / funding-in-R
distributions over the R2 trade population only under predeclared
methodology that explicitly disclaims any cost-lock revision and refuses
to interpret LOW-slip variant outperformance as license to relax §11.6.
26. Forbidden: any §11.6 relaxation; any pullback-retest entry-rule
revival; any new strategy named "R2-prime"; any cost-curve forensics that
crosses into parameter selection; any framing that treats R2 as a "would
have worked at cheaper cost" candidate.

### 6.6 F1 (mean-reversion-after-overextension; Phase 3d-B2; HARD REJECT)

1. Trade ledger exists: **YES** (`data/derived/backtests/phase-3d-f1-window=r-slip=*/...`).
2. Location: per-cost-cell variants `phase-3d-f1-window=r-slip=high`,
   `-slip=low`, `-slip=medium`, plus `-stop=trade_price`.
3–7, 9–16. Field availability identical to V1-arc trade_log_v1 schema:
entry/exit timestamps, prices, initial stop, fees, slippage_bucket, funding,
realized R (`net_r_multiple`), gross / net PnL, exit_reason, side, symbol all
**PRESENT**.
8. Target / take-profit: F1 uses an SMA(8)-frozen target —
   `frozen_target_value` is populated; explicit `take_profit_price` field
   is not separate, but the target value is recorded.
17. **MFE reconstructable from existing artefacts: NO.** Inspection of
   `src/prometheus/strategy/mean_reversion_overextension/` shows no
   excursion-tracking module. Engine line 1139 returns `mfe_r=0.0` when
   `mgmt is None`. Spot-check of `phase-3d-f1-window=r-slip=high/.../trade_log.json`
   confirms `mfe_r=0.0` and `mae_r=0.0` on the inspected first records.
18. **MAE reconstructable from existing artefacts: NO**, same reason as
   §6.6.17.
19. **Reconstruction requires rerunning script** OR offline computation
   from v002 BTCUSDT / ETHUSDT 15m bars over each trade's
   `entry_fill_time_ms` → `exit_fill_time_ms` window.
20. 15m sufficient for offline reconstruction: **YES**, because trade
   ledger preserves both endpoints. Bar-resolution caveats apply:
   intra-bar stop-vs-MFE sequencing remains ambiguous at 15m, exactly as
   audited in Phase 4am §11.A.11.
21. 5m supplemental usable: **OPTIONAL / would improve resolution under
   Phase 4al §14 hierarchy**. Phase 3q v001-of-5m trade-price 5m for
   BTCUSDT / ETHUSDT covers the F1 OOS window. Not authorized by Phase 4an.
22. 1m may be required later: **NO for first-pass forensics**; only if
   the 5m ambiguity rate (Phase 4al §14.C) exceeded the 10–20% band on
   F1's stop pathology.
23. Mark-price path: **BLOCKED**, see §6.1.
24. Forbidden rescue-risk: **CRITICAL**. F1 is HARD REJECT under the Phase
   3c §7.3 catastrophic-floor predicate. Any MFE / MAE forensic reading on
   F1 must be guarded against the explicit Phase 3e / Phase 4z / Phase 4m
   forbidden-rescue list (no F1-prime / F1 with extra filters / F1 with
   profitable-subset extraction / F1 hybrid / F1 as substrate-relaxed).
   Phase 3d-B2 is terminal for F1.
25. Allowed: descriptive MFE / MAE / time-to-event distributions per
   predeclared methodology, requiring either rerun or offline 15m
   reconstruction; explicit disclaim that informative findings cannot
   license rescue; STOP / TARGET / TIME_STOP exit-reason composition
   forensics.
26. Forbidden: any F1-prime / F1-extended / F1-narrowed; any
   profitable-subset extraction that licenses a new strategy; using F1
   forensic numbers as parameter inputs; any verdict revision.

### 6.7 D1-A (funding-aware directional; Phase 3j; MECHANISM PASS / FRAMEWORK FAIL)

1. Trade ledger exists: **YES** (`data/derived/backtests/phase-3j-d1a-window=r-slip=*/...`).
2. Location: per-cost-cell variants `phase-3j-d1a-window=r-slip=high`,
   `-slip=low`, `-slip=medium`, plus `-stop=trade_price`.
3–7, 9–16. Field availability identical to V1-arc trade_log_v1 schema, plus
D1-A-specific funding-context fields:
`funding_event_id_at_signal`, `funding_rate_at_signal`,
`funding_z_score_at_signal`, `bars_since_funding_event_at_signal`,
`overextension_magnitude_at_signal`. All present.
8. Target / take-profit: D1-A uses fixed +2.0R target —
   `frozen_target_value` populated.
17. **MFE reconstructable from existing artefacts: NO**, same reason as
   F1 (`src/prometheus/strategy/funding_aware_directional/` has no
   excursion-tracking module; engine returns `mfe_r=0.0` for `mgmt is None`).
   Spot-check of `phase-3j-d1a-window=r-slip=high/.../trade_log.json`
   confirms `mfe_r=0.0` and `mae_r=0.0`.
18. **MAE reconstructable from existing artefacts: NO**, same reason as
   §6.7.17.
19. Reconstruction requires rerun OR offline 15m reconstruction.
20. 15m sufficient for offline reconstruction: **YES** under same
   bar-resolution caveats as F1.
21. 5m supplemental usable: **OPTIONAL** under Phase 4al §14, Phase 3q
   v001-of-5m coverage; **also relevant** to the Phase 3s Q6 D1-A
   mark-price stop-domain finding (~1.3–1.8 5m bars lag), but Q6-style
   work would require Phase 3r §8 mark-price-gap exclusion governance and
   is NOT authorized by Phase 4an.
22. 1m may be required later: **NO for first-pass forensics**; only if 5m
   resolution insufficient.
23. Mark-price path: **BLOCKED** under Phase 3v §8 stop-trigger-domain
   governance for the live-readiness path; the Phase 3s Q6 finding is
   descriptive-only and cannot revise verdicts; not authorized by Phase 4an.
24. Forbidden rescue-risk: **CRITICAL**. D1-A is MECHANISM PASS / FRAMEWORK
   FAIL — other. Forensic reading must be guarded against the Phase 3k /
   Phase 4z / Phase 4m forbidden-rescue list (no D1-A-prime / D1-B / V1-D1
   hybrid / F1-D1 hybrid; no funding as directional trigger). The
   funding-context fields are particularly tempting for post-hoc
   threshold tuning and must NOT be used that way.
25. Allowed: descriptive MFE / MAE / time-to-event / cost-in-R distributions
   under predeclared methodology with explicit no-rescue and no-tuning
   disclaim. Funding-context fields may be analyzed descriptively but
   must NOT be used to derive new threshold candidates.
26. Forbidden: any D1-A-prime / D1-B / V1-D1 / F1-D1 hybrid; any new
   funding-Z-score threshold derived from D1-A forensic numbers; any
   conversion of Phase 3s Q6 finding into rule logic; any verdict revision.

### 6.8 V2 (participation-confirmed trend continuation; Phase 4l; HARD REJECT — terminal)

1. **Trade ledger exists: NO**. `scripts/phase4l_v2_backtest.py` builds
   `trades[symbol][cost_cell][variant_id] = list[TradeRecord]` in memory
   but never persists per-trade rows to disk.
2. Location: only aggregate variant-level CSV tables under
   `data/research/phase4l/tables/`
   (`btc_train_variants.csv`, `btc_oos_variants.csv`,
   `cost_sensitivity.csv`, `m1_m2_m3_mechanism_checks.csv`,
   `parameter_grid.csv`, etc.).
3–6. Per-trade timestamps and prices: **IN-MEMORY ONLY** during run; not
   persisted; classification `RECONSTRUCTABLE_ONLY_WITH_RERUN`.
7. Initial stop prices: same.
8. Target / take-profit: same.
9. Realized R: aggregate `mean_R`, `total_R` are persisted at variant
   level; per-trade R not persisted.
10–14. Aggregate gross / net PnL, fees, slippage, funding: only at
   aggregate cost-cell level; per-trade not persisted.
15. Stop / exit-reason fields: not persisted; in-memory only.
16. Trade side / symbol / timeframe: per-variant persisted; per-trade only
   in memory (`TradeRecord` dataclass at line 204).
17. **MFE reconstructable: PARTIAL UPON RERUN**. V2 in-memory tracks
   `mfe_R` at line 221 of the script using 30m `bar_high` / `bar_low`
   (lines 1224–1226), but this value is not persisted per-trade; M1
   uses the in-memory distribution. Rerun under script modification
   would persist it.
18. **MAE reconstructable: NO from existing artefacts; NOT in V2 code at
   all**. V2 `TradeRecord` does not have an MAE field; rerun would require
   adding a `mae_R` running tracker analogous to `mfe_R_running`. NOT
   authorized by Phase 4an.
19. **Reconstruction requires rerunning the V2 script under modification.**
   The existing aggregate tables cannot answer per-trade questions.
20. 30m sufficient for V2 path forensics: **NO usable answer because
   V2 produced 0 BTC OOS HIGH trades** (Phase 4l Verdict C; CFP-1 critical
   binding driver). The trade population is empty for the train-best
   variant; per-trade forensics on V2 first-spec is fundamentally limited
   to the descriptive observation that no trades survived the 0.60–1.80 ×
   ATR(20) stop-distance gate. This is recorded in Phase 4l outputs.
21. 5m supplemental usable: **OPTIONAL** for any future redesign-stage
   path-resolution work, but Phase 4u / Phase 4z / Phase 4m / Phase 4y
   forbid V2 first-spec rerun and forbid V2-prime; not authorized.
22. 1m may be required later: **NO**.
23. Mark-price path: **BLOCKED** under §1.7.3.
24. Forbidden rescue-risk: **CRITICAL**. V2 is HARD REJECT — terminal.
   Phase 4m forbidden-rescue list explicitly bans V2-prime / V2-narrow /
   V2-relaxed / V2 hybrid / V2 stop-distance widening / V2 N1 amendment.
   Forensic reading on V2 must NOT cross into design-stage redesign.
25. Allowed: documenting the zero-trade outcome and the Phase 4l forensic
   observation as historical context. Documenting the 30m `mfe_R`
   distribution from V2's in-memory M1 calculation (already in Phase 4l
   outputs) descriptively.
26. Forbidden: any V2 rerun under modified stop-distance bounds; any
   V2-prime / V2-narrow / V2-relaxed / V2 hybrid; any conversion of V2 in-memory
   `mfe_R` distribution into a "what would have happened with a wider
   stop" rescue narrative; any verdict revision; any framework lock
   revision.

### 6.9 G1 (regime-first breakout continuation; Phase 4r; HARD REJECT — terminal)

1. **Trade ledger exists: NO**. `scripts/phase4r_g1_backtest.py` builds
   `trades` lists in memory and persists only aggregate CSV tables under
   `data/research/phase4r/tables/`.
2. Location: aggregate variant-level CSVs only.
3–16. Same as V2 (§6.8): per-trade fields IN-MEMORY ONLY during run; not
   persisted; aggregate-only on disk.
17. **MFE reconstructable: NO from existing artefacts; NOT in G1 code at
   all**. `grep mfe scripts/phase4r_g1_backtest.py` returns no matches.
   Reconstruction requires script modification + rerun. NOT authorized
   by Phase 4an.
18. **MAE reconstructable: NO**, same reason as §6.9.17.
19. **Reconstruction requires rerun under script modification.**
20. 30m sufficient for any future G1 path question: **N/A — G1 produced 0
   qualifying BTC OOS HIGH trades** (Phase 4r Verdict C; CFP-1 critical;
   CFP-9 independent regime-active-fraction collapse 2.03%). The trade
   population is empty.
21. 5m supplemental usable: **NOT meaningful** because G1's failure mode is
   regime-gate-meets-setup intersection sparseness — adding lower-timeframe
   data does not change the rate at which 30m breakout triggers fire
   inside an active regime.
22. 1m may be required later: **NO**.
23. Mark-price path: **BLOCKED** under §1.7.3.
24. Forbidden rescue-risk: **CRITICAL**. G1 is HARD REJECT — terminal.
   Phase 4s forbidden-rescue list explicitly bans G1-prime / G1-narrow /
   G1-extension / G1 hybrid; classifier relaxation; any K_confirm,
   ATR-band, V_liq_min, funding-band, E_min, breakout-rule, or
   stop-distance-bound amendment based on Phase 4r forensic numbers.
25. Allowed: documenting the zero-trade-and-regime-sparse outcome and
   the always-active baseline result (124 BTC OOS HIGH trades, mean_R =
   −0.34) as historical context. Already recorded in Phase 4r outputs.
26. Forbidden: any G1 rerun under relaxed classifier; any G1-prime / G1
   hybrid; any conversion of always-active baseline numbers into a
   strategy candidate; any verdict revision; any lock revision.

### 6.10 C1 (volatility-contraction expansion breakout; Phase 4x; HARD REJECT — terminal)

1. **Trade ledger exists: NO**. `scripts/phase4x_c1_backtest.py` builds
   `trades[sym][cell][population][variant_id] = list[TradeRecord]` lists
   in memory and persists only aggregate CSV tables under
   `data/research/phase4x/tables/`.
2. Location: aggregate variant-level CSVs only.
3–16. Same as V2 / G1 (§6.8 / §6.9): per-trade fields IN-MEMORY ONLY during
   run; not persisted; aggregate-only on disk.
17. **MFE reconstructable: NO from existing artefacts; NOT in C1 code at
   all**. `grep mfe scripts/phase4x_c1_backtest.py` returns no matches.
   Reconstruction requires script modification + rerun. NOT authorized.
18. **MAE reconstructable: NO**, same reason as §6.10.17.
19. **Reconstruction requires rerun under script modification.**
20. 30m sufficient for path questions: **C1 produced 149 BTC OOS HIGH
   trades** (Phase 4x; mean_R = −0.36). C1 is the only V2/G1/C1
   population whose per-trade pathway is non-empty in principle, BUT no
   per-trade ledger was persisted. Reconstruction would require rerun.
21. 5m supplemental usable: **OPTIONAL** for resolving intra-30m stop /
   target sequencing under Phase 4al §14 hierarchy if path forensics on
   C1 were ever authorized — but Phase 4y forbidden-rescue list bans
   C1-prime / C1-narrow / C1-extension / C1 hybrid; not authorized.
22. 1m may be required later: **NO** for first-pass forensics; only if
   the 5m ambiguity rate exceeded 10–20%.
23. Mark-price path: **BLOCKED** under §1.7.3.
24. Forbidden rescue-risk: **CRITICAL**. C1 is HARD REJECT — terminal.
   Phase 4y forbidden-rescue list explicitly bans C1-prime /
   C1-extension / C1-narrow / C1 hybrid; any threshold tuning from Phase
   4x; any volume / funding / HTF / ATR stop-distance gate added post hoc.
   The "fires-and-loses" failure mode (Phase 4y categorical insight #5
   "not zero trades is not success") makes C1 forensics particularly
   tempting and particularly forbidden as rescue input.
25. Allowed: documenting the 149-trade fires-and-loses outcome and the
   non-contraction / always-active / delayed-breakout baseline differentials
   as historical context. Already recorded in Phase 4x outputs.
26. Forbidden: any C1 rerun under different N_comp / C_width / B_width /
   S_buffer / T_mult; any C1-prime / C1-extension / C1-narrow / C1 hybrid;
   any volume / funding / HTF / mark-price overlay; any conversion of Phase
   4x forensic numbers into tuning targets; any verdict revision; any
   lock revision.

### 6.11 5m research thread (CLOSED per Phase 3t)

The 5m research thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) was diagnostic
only (Q1–Q7) and did NOT produce a strategy trade ledger. Per the Phase 3t
post-5m-diagnostics consolidation memo, the 5m thread is operationally
CLOSED. Its ONLY admissible Phase 4an-era role is **closed historical
context**.

1–16. **N/A** (no strategy population, no trade ledger).
17–22. **N/A** (no excursion data because no trades).
23. Mark-price path: Phase 3r §8 governance applies to any future
   mark-price-domain analysis but **the 5m thread is not the right place to
   open such analysis**.
24. Forbidden rescue-risk: **CRITICAL**. Phase 4al §14 explicitly says the
   5m research thread remains closed and is NOT reopened by lower-timeframe
   data-resolution discussion. Phase 3o §6 forbidden question forms remain
   binding.
25. Allowed: citing Q1–Q7 findings as descriptive context only. NOT
   citing Q1–Q7 outputs as rule-input candidates.
26. Forbidden: any 5m strategy; any reuse of Q1–Q7 findings as rule
   input; any reopening of the 5m strategy thread; any conversion of 5m
   diagnostic outputs into strategy candidates.

## 7. Artifact Sufficiency Classification

Using the Phase 4an authorization-brief classification taxonomy:

```text
READY_FOR_STATIC_FORENSICS              :   (none)
RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS :   H0, R3, R1a, R1b-narrow, R2
                                            (for MFE/MAE/realized-R/cost
                                            forensics; rerun NOT required)
RECONSTRUCTABLE_ONLY_WITH_RERUN         :   F1, D1-A (for MFE/MAE);
                                            V2, G1, C1 (for any per-trade
                                            forensics)
NEEDS_LOWER_TIMEFRAME_DATA              :   (conditional only) — applies
                                            only to questions requiring
                                            intra-15m or intra-30m
                                            stop / target sequencing where
                                            5m would help; not required
                                            for first-pass forensics on
                                            any population
NOT_AUDITABLE_FROM_CURRENT_REPO         :   (none) — every population's
                                            artefact state is determinable
                                            from static inspection
CLOSED_CONTEXT_ONLY                     :   5m research thread
GOVERNANCE_BLOCKED_FOR_RESCUE_USE       :   F1, D1-A, V2, G1, C1, R2
                                            (for any forensics whose
                                            shape would license rescue);
                                            R1a, R1b-narrow are also
                                            governance-bounded as
                                            non-leading
```

The classification is **artefact-availability-only**. It says NOTHING
about whether forensics on a population is allowed — that is a separate
governance question (§11) gated by the M0 / Phase 4al refined-no-rescue
rule and Phase 4ak post-null cooldown.

## 8. MFE / MAE Reconstruction Feasibility

### 8.1 V1-arc populations (H0, R3, R1a, R1b-narrow, R2)

`mfe_r` and `mae_r` are already populated in `trade_log_v1`. Computation
source is `src/prometheus/strategy/v1_breakout/management.py::TradeManagement._update_excursions`,
which uses 15m `bar.high` / `bar.low` over the trade lifetime. **No rerun
is required for these fields**, but bar-resolution caveats apply:

- intra-15m-bar stop-vs-MFE sequencing remains ambiguous (the same Phase
  4am §11.A.11 ambiguity);
- the MFE / MAE values are 15m-bar-extreme-based, not tick-based;
- entry-bar excursions are captured (`_update_excursions` is called on
  entry per `phase-2l-r3-r/.../trade_log.json` showing non-zero MFE/MAE on
  multi-bar trades like the one with `bars_in_trade=3`);
- single-bar trades (`bars_in_trade=0`) have meaningful but bounded MFE /
  MAE (the entry-bar high-low envelope).

### 8.2 F1 and D1-A populations (Phase 3d-B2 / Phase 3j)

`mfe_r=0.0` and `mae_r=0.0` are systematic. The `mean_reversion_overextension`
and `funding_aware_directional` strategy modules do not include a
`TradeManagement`-equivalent excursion tracker; engine line 1139–1140
returns `0.0` defaults. **MFE/MAE forensics on F1 / D1-A is therefore
RECONSTRUCTABLE_ONLY_WITH_RERUN**.

Two reconstruction routes exist (neither authorized by Phase 4an):

- **Route A — controlled rerun**: rerun F1 / D1-A under script modification
  that adds excursion tracking analogous to V1 `_update_excursions`. This
  would require script modification + rerun under separate authorization.
- **Route B — offline reconstruction**: join each trade's
  `entry_fill_time_ms` → `exit_fill_time_ms` window with the v002 BTCUSDT /
  ETHUSDT 15m bars, compute per-trade MFE / MAE from bar.high / bar.low,
  and store as a derived artefact. This route does NOT require running the
  strategy script but DOES require a one-shot offline computation under a
  predeclared methodology and separate authorization.

Route B is preferable on rescue-risk grounds because it does not modify the
strategy code, but both routes are NOT authorized by Phase 4an.

### 8.3 V2 / G1 / C1 (Phase 4l / Phase 4r / Phase 4x)

- **V2**: in-memory `mfe_R` exists (computed from 30m bar high/low at
  `phase4l_v2_backtest.py:1224–1226`) but is NOT persisted per-trade. M1
  uses the in-memory distribution. No MAE tracking. Reconstruction
  requires rerun + script modification (to persist per-trade rows and add
  MAE).
- **G1**: no MFE / MAE tracking at all. Full reconstruction requires
  rerun + script modification.
- **C1**: no MFE / MAE tracking at all. Full reconstruction requires
  rerun + script modification.

Phase 4an does NOT authorize any V2 / G1 / C1 rerun. All three are HARD
REJECT terminal first-spec; Phase 4z / Phase 4m / Phase 4s / Phase 4y
forbidden-rescue lists apply.

### 8.4 5m thread

N/A — no strategy population.

## 9. Realized-R / Cost-Field Feasibility

### 9.1 V1-arc / F1 / D1-A populations

Realized R (`net_r_multiple`), gross PnL (`gross_pnl`), net PnL
(`net_pnl`), entry / exit fees (`entry_fee`, `exit_fee`,
`fee_rate_assumption`), slippage cost cell (`slippage_bucket`), and funding
PnL (`funding_pnl`) are all **PRESENT** in `trade_log_v1` schema. Cost
decomposition forensics (fee-in-R, slippage-in-R, funding-in-R) is
**RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS** for all V1-arc populations,
F1, and D1-A.

Phase 4am §11.A.10 audit recorded the V2 cost-application formula
DOCUMENTATION_LIMITATION (V2 uses flat-`entry_price` round-trip
approximation rather than executed-price-shifting); V1-arc / F1 / D1-A
backtest engine cost-application semantics are inherited from
`src/prometheus/research/backtest/accounting.py` and are NOT subject to
the V2-specific approximation. The V1-arc / F1 / D1-A `net_pnl` values
already reflect the engine's chosen accounting; cross-population
methodology-harmonization questions are recorded in §16.

### 9.2 V2 / G1 / C1

Realized R is recorded only at aggregate variant level
(`btc_train_variants.csv`, `btc_oos_variants.csv`, `cost_sensitivity.csv`).
Per-trade realized R, gross / net PnL, fees, and funding-PnL components
are **NOT PERSISTED** and require rerun.

### 9.3 Cost-cell coverage

- V1-arc: per-cost-cell variants exist on disk (`-slip=LOW`,
  `-slip=HIGH`; baseline = MEDIUM). Trade-price stop-domain variant exists
  for retained-evidence runs.
- F1 / D1-A: per-cost-cell variants exist (LOW / MEDIUM / HIGH) plus
  trade-price stop-domain variant.
- V2 / G1 / C1: per-cost-cell evaluation exists at variant aggregate
  level only.

## 10. 15m vs 5m vs Possible 1m Data Sufficiency

Following Phase 4al §14 hierarchy guidance:

- **15m / 30m / 1h / 4h**: signal / event context. ALREADY ACQUIRED.
  Sufficient for first-pass MFE / MAE / time-to-event / cost-decomposition
  forensics on V1-arc populations and (via offline reconstruction or rerun)
  on F1 / D1-A.
- **5m**: recommended first lower-timeframe path-resolution layer for any
  exit-path forensics that exposes intra-15m / intra-30m sequencing
  ambiguity. Phase 3q v001-of-5m datasets cover BTCUSDT / ETHUSDT
  trade-price 5m. Mark-price 5m datasets remain `research_eligible: false`
  (Phase 3q) and would be governed by Phase 3r §8 if ever activated.
  **Not authorized by Phase 4an.**
- **1m**: escalation layer only if 5m ambiguity exceeds the Phase 4al
  §14.C >10% / >20% bands. **Not authorized by Phase 4an** and not
  acquired.
- **aggTrades / tick**: final escalation. NOT acquired and NOT authorized.

For each population, the Phase 4al §14.D resolution-coverage-by-question
guidance applies:

- MFE / MAE magnitude: probably resolvable at 15m for V1-arc; at 30m for
  V2; first-pass adequate.
- Exact stop-vs-target sequencing: ambiguous at 15m / 30m. Would benefit
  from 5m only if explicit forensic question requires it.
- Mark-price stops: requires both trade-price and mark-price candles AND
  Phase 3r §8 mark-price-gap exclusion governance. Blocked under §1.7.3
  for live-readiness; not authorized for forensics by Phase 4an.

The **only** populations whose first-pass forensic questions are
plausibly answerable from existing locally-present artefacts (without
rerun, without acquisition, without script modification) are V1-arc:
H0, R3, R1a, R1b-narrow, R2.

## 11. Forbidden Rescue-Risk Assessment

The forbidden-rescue-risk profile per population follows the Phase 4al §9
refined no-rescue rule and the cumulative Phase 4z / Phase 4m / Phase 4s /
Phase 4y forbidden-rescue lists:

| Population   | Forbidden rescue-risk | Specific forbidden patterns                                                                                           |
|--------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------|
| H0           | MEDIUM                | reframe as cost-relaxed; discount §11.6                                                                               |
| R3           | MEDIUM                | reframe as next-spec-after-R3; new-strategy spawn from R3 path                                                        |
| R1a          | HIGH                  | per-bar volatility-percentile filter rescue; R1a-prime; bolt-on as scaffold                                           |
| R1b-narrow   | HIGH                  | bias-strength magnitude filter rescue; R1b-narrow-prime; bolt-on as scaffold                                          |
| R2           | CRITICAL              | §11.6 relaxation; pullback-retest rescue; R2-prime; cost-curve mining                                                 |
| F1           | CRITICAL              | F1-prime; profitable-subset extraction; F1 hybrid; F1 with extra filters                                              |
| D1-A         | CRITICAL              | D1-A-prime; D1-B; V1-D1 hybrid; F1-D1 hybrid; funding-Z-score tuning; Phase 3s Q6 finding as rule input               |
| V2           | CRITICAL              | V2-prime; V2-narrow; V2-relaxed; V2 hybrid; stop-distance widening; setup-window amendment                            |
| G1           | CRITICAL              | G1-prime; G1-narrow; G1-extension; classifier relaxation; K_confirm/ATR-band/V_liq_min/funding-band/E_min amendment   |
| C1           | CRITICAL              | C1-prime; C1-narrow; C1-extension; C1 hybrid; volume / funding / HTF / mark-price overlay; threshold tuning           |
| 5m thread    | CRITICAL              | reopening 5m strategy thread; Q1–Q7 outputs as rule input                                                              |

Cross-cutting forbidden patterns (apply to ALL populations):

- mining V1-D1 / F1-D1 / V1-D1-V2 / V1-D1-G1 / V1-D1-C1 / etc. hybrids;
- mining cost-cell-shaped strategies (e.g., a strategy that "only works at
  LOW cost");
- mining symbol-shaped strategies (e.g., ETH-only forks of BTC-failed
  candidates) — Phase 4aa retroactive-rescue ban applies;
- using forensic numbers from any rejected population as parameter-
  selection input for any future hypothesis;
- using descriptive winner-anatomy patterns as license to weaken the M0
  refined no-rescue rule.

## 12. Allowed Future Forensic Uses

Conditional on separate operator authorization, the **only** future
forensic uses that pass the M0 / Phase 4al §9 / Phase 4ak post-null
cooldown gauntlet are:

1. **Descriptive MFE / MAE / time-to-event / target-before-stop / realized-R
   / cost-in-R distributions on V1-arc populations**, predeclared in
   methodology before computation, with explicit no-rescue and no-tuning
   disclaim.
2. **Methodology-harmonization memo** (docs-only) clarifying:
   - how MFE / MAE should be defined consistently across V1-arc, F1, D1-A,
     V2, G1, C1 if any future forensic phase is ever authorized;
   - whether F1 / D1-A reconstruction should follow the rerun route or
     the offline-15m-join route;
   - whether V2 / G1 / C1 reconstruction is admissible at all under M0,
     given that all three are HARD REJECT terminal first-spec and the M0
     post-null cooldown rule applies to their families.
3. **Backtest-logic methodology-harmonization memo** (docs-only) addressing
   the Phase 4am §11.A.10 V2 cost-application DOCUMENTATION_LIMITATION
   and the §11.A.11 entry-bar exit handling DEFECT_NON_MATERIAL by
   prospectively specifying how future research scripts should account
   for cost and how entry-bar exits should be handled, without modifying
   any existing committed script and without rerunning anything.

Each of (1), (2), (3) requires separate operator authorization. Phase 4an
does NOT authorize any of them.

## 13. Forbidden Future Uses

Forbidden under Phase 4an, regardless of artefact availability:

- any strategy resurrection labelled R3-prime / R1a-prime / R1b-narrow-prime
  / R2-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / G1-prime / G1-narrow / G1-extension / C1-prime / C1-narrow /
  C1-extension / V1-D1 / F1-D1 / any cross-strategy hybrid;
- any conversion of forensic numbers into parameter-selection inputs;
- any verdict revision;
- any project-lock revision (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6/§7/§8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v,
  Phase 4w);
- any M0-governance amendment derived from forensic findings;
- any framework-anchor revision (H0 stays anchor);
- any baseline-of-record revision (R3 stays baseline-of-record);
- any framework promotion of a retained-evidence population;
- any conversion of MFE / MAE / time-to-event findings into a strategy
  candidate without first satisfying the Phase 4m 18-requirement
  fresh-hypothesis validity gate AND the Phase 4ak twelve-clause M0 gate
  AND the Phase 4al §9 refined no-rescue rule;
- any reopening of the 5m research thread;
- any acquisition of 5m / 1m / aggTrades / tick / mark-price 30m / 4h
  data without separately authorized data-requirements memo;
- any paper / shadow / live / exchange-write / production-key creation;
- any MCP / Graphify / `.mcp.json` / credential work.

## 14. Original Questions Answered by Phase 4an

The Phase 4an authorization brief implicitly raised these questions:

- **Q1: Which historical populations have sufficient artefacts for future
  exit-path forensic analysis?**
  Answer: V1-arc (H0, R3, R1a, R1b-narrow, R2) for MFE / MAE / realized-R /
  cost-decomposition forensics from existing artefacts. F1 and D1-A for
  realized-R / cost-decomposition forensics from existing artefacts; for
  MFE / MAE, only via rerun or offline 15m-join reconstruction. V2 / G1 /
  C1: for any per-trade forensics, rerun under script modification is
  required.
- **Q2: Which populations would require lower-timeframe data?**
  Answer: None for first-pass forensics. 5m may be useful only if intra-15m
  / intra-30m sequencing ambiguity is exposed in a future forensic question
  on V1-arc / F1 / D1-A / C1. 1m would only be relevant if 5m ambiguity
  exceeds Phase 4al §14.C bands.
- **Q3: Which populations would require reruns?**
  Answer: V2, G1, C1 (any per-trade forensics). F1, D1-A (MFE/MAE only;
  alternative offline-join route exists).
- **Q4: Which populations are governance-blocked for rescue use?**
  Answer: All ten populations are governance-bounded against rescue use
  per the cumulative forbidden-rescue list, with R1a / R1b-narrow / R2 /
  F1 / D1-A / V2 / G1 / C1 / 5m thread carrying CRITICAL forbidden-rescue
  risk.
- **Q5: What is the clean next step?**
  Answer: remain paused.

## 15. Original Questions Still Open After Phase 4an

- **OQ-A**: For F1 / D1-A, does offline 15m-join reconstruction recover
  enough MFE / MAE resolution to support useful forensics, or does the bar
  resolution wash out the signal? Cannot be determined without computation,
  which is NOT authorized.
- **OQ-B**: For V2 / G1 / C1, does the M0 post-null cooldown rule fully
  prohibit rerun-based per-trade forensics, or only forbid forensics that
  could be misread as rescue? This is a governance interpretation question
  that the methodology-harmonization memo (Phase 4an §12 item 2) would
  need to resolve before any rerun is authorized.
- **OQ-C**: For all populations, does the Phase 4am §11.A audit's
  DOCUMENTATION_LIMITATION classification of V2's cost-application formula
  imply that future cross-population realized-R comparisons need a
  prospective harmonization spec before being meaningful? This is a
  methodology question for the Phase 4an §12 item 3 memo if separately
  authorized.
- **OQ-D**: For any future forensic phase, what is the minimum-sufficient
  "predeclared methodology" template that satisfies the Phase 4al §9.C
  predeclaration discipline plus the Phase 4ak twelve-clause M0 gate? This
  is a template question.
- **OQ-E**: For the 5m thread, are there path-resolution-only uses of the
  Phase 3q v001-of-5m datasets that do NOT count as reopening the 5m
  thread? Phase 4al §14 says yes in principle (forensic-measurement-layer
  use). Phase 3t says the 5m thread itself is closed. The boundary between
  "forensic measurement layer" and "reopened thread" is governance-
  interpretation territory; Phase 4an does not draw it.

These open questions are recorded but **NOT answered** by Phase 4an. They
do not block Phase 4an from being mergeable as docs-only.

## 16. Implementation / Governance Review

### 16.1 What changed?

This phase added two new files:

```text
docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md
```

(this memo) and a narrow paragraph addition to:

```text
docs/00-meta/current-project-state.md
```

recording the Phase 4an inventory result and reaffirming preserved verdicts
and locks.

### 16.2 What did not change?

- `docs/00-meta/m0-mechanism-admissibility-gate.md` (Phase 4ak durable
  governance): unchanged.
- All twelve M0 clauses M0.1–M0.12: unchanged.
- The post-null cooldown rule: unchanged.
- The M0 cooled-down families list: unchanged.
- All retained verdicts: unchanged
  (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread).
- All project locks: unchanged
  (§11.6 = 8 bps per side / 16 bps round-trip; §1.7.3 0.25% / 2× /
  one-position / mark-price stops; Phase 3r §8 mark-price gap governance;
  Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8
  break-even / EMA slope / stagnation governance; Phase 4j §11 metrics
  OI-subset partial-eligibility rule; Phase 4k V2 backtest-plan
  methodology; Phase 4p G1 strategy-spec memo; Phase 4q G1 backtest-plan
  methodology; Phase 4v C1 strategy-spec memo; Phase 4w C1 backtest-plan
  methodology).
- All scripts under `scripts/`: unchanged.
- All source files under `src/prometheus/`: unchanged.
- All tests under `tests/`: unchanged.
- All data files under `data/raw/`, `data/normalized/`, `data/derived/`,
  `data/research/`: unchanged.
- All manifests under `data/manifests/`: unchanged.
- `docs/12-roadmap/phase-gates.md`: unchanged.
- `docs/12-roadmap/technical-debt-register.md`: unchanged.
- `docs/00-meta/ai-coding-handoff.md`: unchanged.
- `docs/00-meta/implementation-ambiguity-log.md`: unchanged.

### 16.3 Were any locks, verdicts, or safety boundaries affected?

No. All locks, verdicts, and safety boundaries are preserved verbatim.
The Phase 4al refined no-rescue rule, the Phase 4ak twelve-clause M0
gate, the Phase 4ak post-null cooldown rule, and the Phase 3v / Phase 3w /
Phase 4j / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w
methodologies are preserved.

### 16.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 16.5 Is the phase mergeable as docs-only?

Yes. The phase is mergeable as docs-only because the only files modified
are the new memo and the narrow paragraph addition to
`docs/00-meta/current-project-state.md`.

## 17. Research Interpretation Review

### 17.1 What did this phase prove?

Phase 4an proved, by static repository inspection, that:

- V1-arc populations (H0, R3, R1a, R1b-narrow, R2) have sufficient locally
  present trade-log artefacts to support future descriptive MFE / MAE /
  realized-R / cost-decomposition forensics WITHOUT rerun, subject to
  15m-bar-resolution caveats and to the refined no-rescue rule.
- F1 and D1-A have trade-log artefacts whose realized-R / cost / timing
  fields are populated, but whose MFE / MAE fields are systematically
  zero because the F1 / D1-A strategy modules do not include excursion
  trackers; MFE / MAE forensics on these populations is therefore
  RECONSTRUCTABLE_ONLY_WITH_RERUN (or via offline 15m-join).
- V2, G1, C1 standalone scripts emit aggregate variant-level CSVs only
  and persist no per-trade ledger; per-trade forensics on these
  populations is RECONSTRUCTABLE_ONLY_WITH_RERUN, and for V2 / G1 / C1
  this is governance-bounded by Phase 4z / Phase 4m / Phase 4s / Phase 4y
  forbidden-rescue lists.
- The 5m research thread is CLOSED_CONTEXT_ONLY and cannot be reopened
  for forensics without separate operator authorization that explicitly
  rejects the Phase 3t closure.
- All ten populations carry forbidden-rescue-risk under M0 / Phase 4al §9;
  the risk is HIGH for R1a / R1b-narrow and CRITICAL for R2 / F1 / D1-A /
  V2 / G1 / C1 / 5m thread.

### 17.2 What did this phase not prove?

Phase 4an did NOT prove anything about:

- the actual distributions of MFE / MAE / realized-R / cost across any
  population (no computation done);
- whether any population's path patterns are "interesting" or "boring"
  (no analysis done);
- whether the V1-arc cost-decomposition is methodologically harmonized
  with V2 / G1 / C1 cost-decomposition (this is OQ-C);
- whether 5m-resolution path forensics on F1 / D1-A would expose
  meaningful intra-bar sequencing (this is OQ-A);
- whether V2 / G1 / C1 rerun under script modification would be
  governance-admissible at all (this is OQ-B);
- which populations are most worth analyzing first (no prioritization done;
  Phase 4an deliberately stops before that).

### 17.3 Which original questions did it answer?

Q1, Q2, Q3, Q4, Q5 above (§14).

### 17.4 Which original questions remain open?

OQ-A, OQ-B, OQ-C, OQ-D, OQ-E above (§15).

### 17.5 What does it mean for strategy research?

It means that the historical strategy-research record now has a clear
inventory of what could be examined later if any future forensic phase is
ever authorized. It does NOT mean any strategy research is unblocked. It
does NOT mean any new candidate is admissible. The M0 cooled-down families
list still cools down price-only single-symbol directional continuation
(DEPLETED), cross-sectional trend / relative-strength symbol selection
under Phase 4ai descriptors (COOLED_DOWN_AFTER_NOT_SUPPORTED), derivatives-
context directional (CONDITIONAL_ONLY / HIGH_D1-A_RESCUE_RISK),
microstructure / order-flow (NOT_RECOMMENDED_NOW), mark-price stop-domain
(NOT_RECOMMENDED_NOW). Phase 4an does not update that list.

### 17.6 What does it mean for governance?

It means that any future forensic phase has a defensible map of what
artefacts exist and what would require rerun, but it also means that the
forbidden-rescue-risk profile of every population is documented in advance
of any computation. The methodology-harmonization gap (V2 cost-application
DOCUMENTATION_LIMITATION; F1 / D1-A missing-MFE/MAE; V2/G1/C1 missing
per-trade ledger) is now explicit. Future forensic work would benefit
from a methodology-harmonization memo BEFORE any computation is done.

### 17.7 What is the clean next step?

The clean next step is **remain paused**. The inventory is complete; no
forensic work is authorized; no successor phase is started. If the
operator later wants to authorize a methodology-harmonization memo (a
narrow docs-only follow-up), that is acceptable as a conditional secondary
alternative.

### 17.8 What should we not do yet?

Do not start any forensic phase. Do not rerun V2 / G1 / C1. Do not rerun
F1 / D1-A. Do not compute offline MFE / MAE joins. Do not acquire 5m / 1m /
aggTrades / tick. Do not reopen the 5m research thread. Do not propose a
new strategy. Do not authorize Phase 4ao / Phase 5 / Phase 4 canonical /
paper / shadow / live / exchange-write / production keys / authenticated
APIs / private endpoints / user stream / WebSocket / MCP / Graphify /
`.mcp.json` / credentials. Do not modify the M0 governance document. Do
not modify any retained verdict. Do not modify any project lock.

## 18. Recommendation

**Primary recommendation**: remain paused. The Phase 4an inventory is on
record; no computation is required to proceed; no successor phase is
authorized.

**Conditional secondary**: a narrower future docs-only methodology /
artefact harmonization memo (Phase 4an §12 items 2–3) is acceptable IF
separately authorized. The harmonization memo would resolve OQ-C and
OQ-D before any computation is contemplated. It would NOT authorize
computation; computation would require a separately authorized successor
phase after harmonization.

**Conditional tertiary**: a future full exit-path forensic plan (per
Phase 4al §13 maximum scope) is acceptable ONLY IF separately authorized
AND ONLY AFTER harmonization. Forensic computation would be restricted to
V1-arc populations under predeclared methodology and the Phase 4al §9
refined no-rescue rule. F1 / D1-A computation, if ever authorized, would
prefer the offline-15m-join route (Route B, §8.2) on rescue-risk grounds.
V2 / G1 / C1 computation is prima facie governance-blocked by the M0
post-null cooldown rule and would require explicit reasoning that does
not currently exist.

**Not recommended**: starting forensic work without harmonization;
treating Phase 4an artefact-availability findings as authorization to
analyze; using Phase 4an forbidden-rescue-risk classifications as a
ranking scheme to "pick the most interesting population"; converting any
Phase 4an section into a strategy candidate.

**Forbidden**: paper / shadow / live / exchange-write / production keys /
authenticated APIs / private endpoints / user stream / WebSocket / MCP /
Graphify / `.mcp.json` / credentials; any strategy resurrection; any
verdict revision; any project-lock revision; any M0-governance amendment
derived from Phase 4an findings; reopening the 5m research thread.

Phase 4an does NOT authorize Phase 4ao or any successor.

## 19. Explicit Preservation of Verdicts, Locks, and No-Rescue Constraints

**Retained verdicts (preserved verbatim):**

- H0 remains FRAMEWORK ANCHOR.
- R3 remains BASELINE-OF-RECORD.
- R1a remains RETAINED — NON-LEADING.
- R1b-narrow remains RETAINED — NON-LEADING.
- R2 remains FAILED — §11.6 cost-sensitivity blocks.
- F1 remains HARD REJECT.
- D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- 5m research thread remains operationally CLOSED per Phase 3t.
- V2 remains HARD REJECT — terminal for V2 first-spec.
- G1 remains HARD REJECT — terminal for G1 first-spec.
- C1 remains HARD REJECT — terminal for C1 first-spec.

**Project locks (preserved verbatim):**

- §11.6 HIGH cost = 8 bps slippage per side; round-trip = 16 bps; taker
  fee = 4 bps per side; no maker rebates; no live fee assumption.
- §1.7.3 project-level locks: 0.25% risk per trade; 2× leverage cap; one
  position max; mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance.
- Phase 3v §8 stop-trigger-domain governance.
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.
- Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy-spec memo.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy-spec memo.
- Phase 4w C1 backtest-plan methodology.
- Phase 4ak twelve-clause M0 mechanism-admissibility gate.
- Phase 4ak post-null cooldown rule.
- Phase 4ak cooled-down families list.
- Phase 4al refined no-rescue rule.
- Phase 4al §13 future-Phase-4am-style boundary specification.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved as
  documentation for future methodology-harmonization scoping.

**No-rescue constraints (preserved verbatim):**

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid.
- No conversion of Phase 4an inventory findings into strategy candidates.
- No conversion of Phase 4an forbidden-rescue-risk classifications into
  parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4an findings.
- No verdict revision.
- No project-lock revision.

Phase 4 (canonical) remains unauthorized.

Phase 4ao / Phase 5 / any successor phase remains unauthorized.

Paper/shadow, live-readiness, deployment, production keys, authenticated
APIs, private endpoints, public-endpoint calls in code, user stream,
WebSocket, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and
5m / 1m / aggTrades / tick-data acquisition all remain unauthorized.

**Recommended state remains paused.**

**No next phase authorized.**
