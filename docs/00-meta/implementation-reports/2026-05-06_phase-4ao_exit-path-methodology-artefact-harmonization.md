# Phase 4ao — Exit-Path Methodology / Artefact Harmonization Memo

## 1. Executive Summary

Phase 4ao is a docs-only methodology / artefact harmonization memo. It
defines how any future exit-path forensic phase would have to be
specified before computation. Phase 4ao does NOT perform forensic
analysis, does NOT compute MFE / MAE / realized-R / cost distributions,
does NOT run any backtest or strategy script, does NOT acquire data, does
NOT modify data / manifests / scripts / source / tests / strategy
parameters / thresholds / project locks / retained verdicts / M0
governance, and does NOT authorize any successor phase. It only answers:

```text
What methodology, field definitions, artefact rules, governance
boundaries, and admissibility constraints would be required before any
future exit-path computation could be safely authorized?
```

Phase 4ao is derived from the Phase 4an inventory baseline:

- V1-arc populations (H0, R3, R1a, R1b-narrow, R2):
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS`.
- F1, D1-A:
  `RECONSTRUCTABLE_ONLY_WITH_RERUN` for MFE / MAE;
  `RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS` for non-excursion fields.
- V2, G1, C1:
  `RECONSTRUCTABLE_ONLY_WITH_RERUN`.
- 5m research thread: `CLOSED_CONTEXT_ONLY` (Phase 3t).
- Forbidden-rescue-risk:
  MEDIUM for H0 / R3;
  HIGH for R1a / R1b-narrow;
  CRITICAL for R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread.

Headline harmonization conclusions, in plain language:

1. **Population scope for any future first-pass forensic phase**: V1-arc
   only, with R3 included as baseline-of-record for descriptive context
   and explicitly NOT as an optimization target. F1 / D1-A may be
   admissible later via a strict offline-15m-join route under separate
   authorization. V2 / G1 / C1 rerun-based per-trade forensics is
   conservatively classified as governance-risk-unresolved under the M0
   post-null cooldown rule and is not recommended for first-pass
   forensics.
2. **MFE / MAE definition harmonization**: required to be 15m-bar-extreme-
   based for V1-arc and F1 / D1-A, with bar-resolution caveats explicitly
   recorded; 5m may be referenced as a measurement layer only when an
   ambiguity threshold is exposed (Phase 4al §14 hierarchy); 1m and
   tick / aggTrades remain final escalation and unauthorized.
3. **Realized-R / cost-field harmonization**: V1-arc / F1 / D1-A engine
   accounting and V2 / G1 / C1 standalone-script aggregate accounting
   must be reported under separate labels; cross-population numerical
   comparisons require explicit accounting disclaim. The Phase 4am
   §11.A.10 V2 cost-application DOCUMENTATION_LIMITATION is preserved as
   methodology context. §11.6 = 8 bps per side is preserved verbatim;
   any future fee / slippage / funding decomposition is descriptive only.
4. **Stop-trigger-domain governance** (Phase 3v §8) is binding:
   `trade_price_backtest`, `mark_price_runtime`, and
   `mark_price_backtest_candidate` remain valid; `mixed_or_unknown` fails
   closed; mark-price path forensics for live-readiness remains BLOCKED
   under §1.7.3.
5. **5m boundary** (Phase 3t closure) is binding: existing 5m data may be
   referenced as a forensic measurement layer under strict conditions but
   the 5m strategy thread is NOT reopened. Q1–Q7 outputs are not
   rule-input candidates.
6. **Minimum predeclared-methodology template** for any future forensic
   computation phase is specified in §14 below as the docs-only
   precondition that any successor phase must satisfy before computation.

The recommendation (§16) is **remain paused** as primary, with a
conditional secondary that the operator may later authorize a future
docs-only V1-arc-only exit-path forensic plan if separately sponsored.
Phase 4ao does NOT authorize that plan or any successor phase.

## 2. Scope and Explicit Non-Scope

### 2.1 In scope

- Static repository inspection of Phase 4an inventory result, M0
  governance (`docs/00-meta/m0-mechanism-admissibility-gate.md`), Phase
  4al §9 / §13 / §14, Phase 4am §11.A audit findings, Phase 3v §8 stop-
  trigger-domain governance, Phase 3w §6 / §7 / §8 governance, Phase 4j
  §11 metrics OI-subset rule, Phase 4k / 4q / 4w backtest-plan
  methodologies, and Phase 3t 5m closure.
- Definition of future-forensics terms (§6).
- Cross-population artefact harmonization (§7).
- MFE / MAE methodology harmonization (§8).
- F1 / D1-A reconstruction-route comparison (§9).
- V2 / G1 / C1 rerun admissibility (§10).
- Realized-R / cost-field harmonization (§11).
- Stop-trigger-domain and mark-price boundary (§12).
- 5m boundary (§13).
- Minimum predeclared-methodology template (§14).
- Population eligibility matrix (§15).
- Recommendation (§16).
- Implementation / governance review (§17).
- Research interpretation review (§18).
- Explicit preservation of verdicts, locks, no-rescue (§19).

### 2.2 Explicit non-scope

Phase 4ao does NOT and is NOT authorized to:

- compute MFE / MAE / realized-R / time-to-event / target-before-stop /
  stop-before-target / cost-in-R / fee-in-R / slippage-in-R / funding-in-R
  distributions;
- perform exit-path forensics;
- run backtests;
- execute historical strategy scripts (`scripts/phase2*.py`,
  `scripts/phase3d_F1_execution.py`, `scripts/phase3j_D1A_execution.py`,
  `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`,
  `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`,
  `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`,
  `scripts/phase4ac_alt_symbol_acquisition.py`,
  `scripts/phase4ae_alt_symbol_substrate_feasibility.py`,
  `scripts/phase4af_alt_symbol_regime_persistence.py`,
  `scripts/phase4ai_single_position_cross_sectional_trend.py`);
- run offline MFE / MAE joins;
- acquire data (no 5m / 1m / aggTrades / tick / mark-price 30m / 4h
  acquisition);
- modify any data file under `data/raw/`, `data/normalized/`,
  `data/derived/`, or `data/research/`;
- modify any manifest under `data/manifests/`;
- modify any source file under `src/prometheus/`;
- modify any test under `tests/`;
- modify any strategy specification under `docs/03-strategy-research/`;
- modify any validation document under `docs/05-backtesting-validation/`;
- modify any roadmap document under `docs/12-roadmap/`;
- modify any governance document under `docs/00-meta/`
  (`m0-mechanism-admissibility-gate.md`, `ai-coding-handoff.md`,
  `implementation-ambiguity-log.md`);
- modify any retained verdict;
- modify any project lock (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w);
- propose, name, or pre-design a new strategy or exit system;
- propose a rescue of any rejected or retained-evidence candidate;
- authorize Phase 4ap, Phase 5, Phase 4 canonical, paper / shadow,
  live-readiness, deployment, exchange-write, production-key creation,
  authenticated APIs, private endpoints, public-endpoint calls in code,
  user stream, WebSocket, listenKey, MCP, Graphify, `.mcp.json`, or
  credentials;
- authorize 5m / 1m / aggTrades / tick / mark-price 30m / 4h data
  acquisition;
- amend or override Phase 3t 5m closure;
- amend the Phase 4ak twelve-clause M0 mechanism-admissibility gate, the
  post-null cooldown rule, or the cooled-down families list;
- override Phase 4al §9 refined no-rescue rule, §13 future-Phase-4am-
  style boundary specification, or §14 data-resolution hierarchy.

If a question raised in this memo cannot be answered from static
repository inspection, it is classified explicitly as
**unresolved methodology risk** rather than triggering execution.

## 3. Repository Verification Summary

Verification commands and results, executed at the start of Phase 4ao on
branch `phase-4ao/exit-path-methodology-artefact-harmonization`:

```text
git status                : clean working tree (untracked
                            .claude/scheduled_tasks.lock and
                            data/research/ are gitignored / transient)
git branch --show-current : phase-4ao/exit-path-methodology-artefact-harmonization
git rev-parse main        : a73c00b1de878ca9ee020a7942bd9af7ebb831ed
git rev-parse origin/main : a73c00b1de878ca9ee020a7942bd9af7ebb831ed
```

main and origin/main agree at `a73c00b` (the live Phase 4an merge tip on
both local and remote). The Phase 4an merge-closeout file at
`docs/00-meta/implementation-reports/2026-05-06_phase-4an_merge-closeout.md`
records merge commit `bf3643c` per the documented git self-reference
artifact (every amend produces a new SHA, so the recorded SHA is one
amend cycle behind the actual HEAD `a73c00b`); both `7ea264a` and
`bf3643c` are intermediate amend artefacts and are not in any branch's
live history. The live Phase 4an merge commit on main is `a73c00b`. This
does not change Phase 4an's content (memo, closeout, merge-closeout,
narrow `current-project-state.md` update); the difference is purely
SHA bookkeeping for the amend chain.

The branch for this phase
(`phase-4ao/exit-path-methodology-artefact-harmonization`) was created
from clean main.

## 4. Methodology

Phase 4ao methodology is **static repository inspection only**.
Specifically:

- Read `docs/00-meta/implementation-reports/2026-05-06_phase-4an_historical-trade-population-exit-path-inventory.md`
  for the per-population artefact / classification baseline.
- Read `docs/00-meta/m0-mechanism-admissibility-gate.md` for the
  Phase 4ak twelve-clause M0 gate, the post-null cooldown rule, and the
  cooled-down families list.
- Read Phase 4al main memo for the §9 refined no-rescue rule, §13
  future-Phase-4am-style boundary specification, §14 data-resolution
  hierarchy, and the §14.C ambiguity-rate concept.
- Read Phase 4am main audit report for the §11.A subjects, F-1 / F-2 /
  F-3 / F-4 findings, and materiality reasoning.
- Cross-reference Phase 3t 5m closure, Phase 3r §8 mark-price gap
  governance, Phase 3v §8 stop-trigger-domain governance, Phase 3w §6 /
  §7 / §8 break-even / EMA-slope / stagnation governance, Phase 4j §11
  metrics OI-subset partial-eligibility rule, Phase 4k / 4q / 4w
  backtest-plan methodologies, and Phase 4p / 4v strategy-spec memos.

No script was run during Phase 4ao. No backtest was executed. No data was
read other than that already loaded into the documentation reading
context. No data file was modified. No manifest was modified.

## 5. Phase 4an Inventory Baseline Being Harmonized

Phase 4ao harmonizes the Phase 4an inventory baseline. The baseline is
preserved verbatim and unchanged. For convenience:

| Population   | Phase 4an classification                                                                       |
|--------------|------------------------------------------------------------------------------------------------|
| H0           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                                        |
| R3           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                                        |
| R1a          | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                                        |
| R1b-narrow   | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                                        |
| R2           | RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS                                                        |
| F1           | RECONSTRUCTABLE_ONLY_WITH_RERUN (MFE/MAE) / RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS (other)    |
| D1-A         | RECONSTRUCTABLE_ONLY_WITH_RERUN (MFE/MAE) / RECONSTRUCTABLE_WITH_EXISTING_ARTIFACTS (other)    |
| V2           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                                |
| G1           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                                |
| C1           | RECONSTRUCTABLE_ONLY_WITH_RERUN                                                                |
| 5m thread    | CLOSED_CONTEXT_ONLY                                                                             |

Forbidden-rescue-risk per Phase 4an: MEDIUM for H0 / R3; HIGH for R1a /
R1b-narrow; CRITICAL for R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread. Phase
4ao does not change this risk profile.

## 6. Definitions

Future-forensics terms used by any successor computation phase, defined
once here so future memos do not re-derive them:

- **MFE (Maximum Favorable Excursion)**: maximum price movement in the
  trade's favorable direction during the trade lifetime, expressed as a
  positive price difference relative to entry.
- **MAE (Maximum Adverse Excursion)**: maximum price movement in the
  trade's adverse direction during the trade lifetime, expressed as a
  positive price difference relative to entry.
- **MFE_R**: MFE divided by the trade's per-R risk magnitude (initial
  stop-distance); reported as a non-negative R-multiple.
- **MAE_R**: MAE divided by the trade's per-R risk magnitude; reported as
  a non-negative R-multiple.
- **Realized R (`net_r_multiple` in V1-arc / F1 / D1-A `trade_log_v1`
  schema)**: realized profit / loss expressed as an R-multiple of the
  per-trade risk, after fees and slippage and funding accounting per
  the engine that produced it.
- **Gross R**: trade outcome before fees / slippage / funding, as an
  R-multiple. Distinct from `gross_pnl` (which is a USDT amount); future
  forensics may compute `gross_R = gross_pnl / realized_risk_usdt` for
  V1-arc / F1 / D1-A from `trade_log_v1` fields.
- **Net R**: trade outcome after fees / slippage / funding, as an
  R-multiple. Equivalent to `net_r_multiple` in the V1-arc / F1 / D1-A
  schema.
- **Cost-in-R**: `gross_R - net_R`. For V1-arc / F1 / D1-A computable as
  `(gross_pnl - net_pnl) / realized_risk_usdt`.
- **Fee-in-R**: `(entry_fee + exit_fee) / realized_risk_usdt` for V1-arc /
  F1 / D1-A.
- **Slippage-in-R**: cost component attributable to the slippage cost
  cell (`slippage_bucket` ∈ {LOW, MEDIUM, HIGH}). For V1-arc / F1 / D1-A,
  computable as the difference between the gross PnL evaluated at signal-
  bar-close and the gross PnL evaluated at the realized fill price; the
  exact formula must be predeclared in any future computation phase.
- **Funding-in-R**: `funding_pnl / realized_risk_usdt` for V1-arc / F1 /
  D1-A. (Note: per Phase 4am §11.A.3, F1 funding handling is PASS in
  V1-arc / F1 / D1-A engine path; V2 funding handling is PASS-with-
  DEFECT_NON_MATERIAL F-1; G1 PASS; C1 funding excluded per Phase 4w.)
- **Time-to-MFE**: number of bars from entry until MFE_R was last
  updated (i.e., reached). Bar-resolution defined per population
  (15m for V1-arc / F1 / D1-A; 30m for V2; not tracked for G1 / C1).
- **Time-to-MAE**: number of bars from entry until MAE_R was last
  updated. Bar-resolution as for time-to-MFE.
- **Target-before-stop sequencing**: descriptive frequency of trades
  whose intra-trade path crossed `entry + N_R × R_distance` before
  crossing the initial stop. Defined per-trade as a binary indicator
  with a population-level frequency.
- **Stop-before-target sequencing**: complement of target-before-stop;
  binary indicator with population-level frequency.
- **Bar-resolution ambiguity**: a same-bar event in which both the stop
  and the target (or another exit condition) are inside the bar's high-
  low envelope and the bar's open / close ordering does not unambiguously
  determine which fired first. Phase 4al §11.A.11 / Phase 4am §11.A.11
  preserved.
- **Lower-timeframe escalation**: per Phase 4al §14, the recommended
  hierarchy 15m / 30m / 1h / 4h → 5m → 1m → aggTrades / tick. Escalation
  occurs only when bar-resolution ambiguity exceeds the §14.C bands
  (<2% / 2–10% / >10% / >20%). Escalation is NOT authorized by Phase 4ao.
- **Trade-price path**: the kline-based trade-price OHLC sequence
  (the existing v002 BTCUSDT / ETHUSDT 15m / 1h-derived / Phase 4i
  30m / 4h klines). Used by all V1-arc / F1 / D1-A / V2 / G1 / C1
  backtests for stop hits, target hits, and exits. Stop-trigger-domain
  label = `trade_price_backtest`.
- **Mark-price path**: the kline-based mark-price OHLC sequence (Phase
  3q v001-of-5m mark-price 5m / Phase 4i mark-price 30m / 4h, where
  research-eligible). Used only as descriptive context (Phase 3s Q6) or
  in mark-price-backtest-candidate evaluation under Phase 3v §8. Stop-
  trigger-domain label = `mark_price_runtime` for live, or
  `mark_price_backtest_candidate` for research.
- **Artefact-ready population**: a population whose trade ledger and
  all required forensic fields exist locally without rerun and without
  offline reconstruction.
- **Reconstructable population**: a population whose required forensic
  fields can be computed from existing local artefacts (trade ledger +
  bar data) via a one-shot offline join, without re-running the
  strategy script.
- **Rerun-required population**: a population whose required forensic
  fields cannot be obtained without re-running the strategy / research
  script under modification.
- **Governance-blocked-for-rescue-use**: a population whose forensic
  result, even if technically computable, is governance-bounded to
  forbid rescue interpretation under M0 / Phase 4al §9 / cumulative
  rejection-topology forbidden-rescue lists.

## 7. Cross-Population Artefact Harmonization

### 7.1 V1-arc (H0 / R3 / R1a / R1b-narrow / R2)

**Fields that exist** (per `trade_log_v1` schema, populated):
`schema_version`, `trade_count`, per-trade `trade_id`, `direction`,
`symbol`, `signal_bar_open_time_ms`, `entry_fill_time_ms`,
`exit_fill_time_ms`, `entry_fill_price`, `exit_fill_price`, `quantity`,
`notional_usdt`, `initial_stop`, `stop_distance`, `realized_risk_usdt`,
`entry_fee`, `exit_fee`, `fee_rate_assumption`, `funding_pnl`,
`gross_pnl`, `net_pnl`, `net_r_multiple`, `bars_in_trade`,
`exit_reason`, `slippage_bucket`, `mfe_r`, `mae_r`, `stop_was_gap_through`.

**Fields that exist conditionally** (some are populated for some V1-arc
runs and `NaN` for others, depending on whether the strategy variant
used them): `atr_at_signal`, `entry_to_target_distance_atr`,
`stop_distance_at_signal_atr`, `frozen_target_value`,
`overextension_magnitude_at_signal`, `pullback_level_at_registration`,
`structural_stop_level_at_registration`, `funding_event_id_at_signal`,
`funding_rate_at_signal`, `funding_z_score_at_signal`,
`bars_since_funding_event_at_signal`. These are not required for
first-pass V1-arc forensics but should be preserved if present.

**Comparable fields across all V1-arc populations**: `mfe_r`, `mae_r`,
`net_r_multiple`, `direction`, `symbol`, `slippage_bucket`,
`fee_rate_assumption`, `entry_fill_time_ms`, `exit_fill_time_ms`,
`bars_in_trade`, `exit_reason`. Comparable means: same definition, same
units, same units of risk normalization (R is per-trade
`realized_risk_usdt`).

**Not directly comparable across V1-arc populations without disclaim**:
`stop_distance` (in price units; depends on symbol and date), `gross_pnl`
and `net_pnl` (USDT amounts; depend on quantity and realized risk),
`notional_usdt` (depends on quantity and realized risk). For cross-
population comparison, these must be normalized to R or to relative
units.

**Allowed future forensic uses**:
descriptive MFE / MAE / time-to-event / target-before-stop / realized-R /
cost-in-R / fee-in-R / slippage-in-R / funding-in-R distributions
predeclared per §14 template; cross-population descriptive comparison
under explicit accounting-equivalence disclaim; per-cost-cell variant
comparison; per-stop-domain variant comparison (where local trade-price
stop-domain variants exist).

**Forbidden future uses**:
parameter selection on any V1-arc population; R3-prime / R1a-prime /
R1b-narrow-prime / R2-prime; conversion of forensic patterns into
strategy candidates; verdict revision; project-lock revision;
§11.6 relaxation; mining LOW-slip variant outperformance as license
to revise §11.6.

**Rerun governance-admissibility**: V1-arc populations do not require
rerun for first-pass forensics; rerun is therefore NOT a governance
question for V1-arc. Any future V1-arc rerun (e.g., for a forensic
question requiring fields not in the current schema) would be
governance-bounded by M0 post-null cooldown / Phase 4al §9 and would
require separate authorization.

### 7.2 F1 / D1-A

**Fields that exist** (per `trade_log_v1` schema): same set as V1-arc,
populated. Plus D1-A-specific funding-context fields:
`funding_event_id_at_signal`, `funding_rate_at_signal`,
`funding_z_score_at_signal`, `bars_since_funding_event_at_signal`,
`overextension_magnitude_at_signal`. F1 has `frozen_target_value`
populated for the SMA(8)-frozen target.

**Fields uniformly zero (artefact gap)**: `mfe_r = 0.0` and
`mae_r = 0.0`, because F1 (`src/prometheus/strategy/mean_reversion_overextension/`)
and D1-A (`src/prometheus/strategy/funding_aware_directional/`) strategy
modules contain no excursion tracker; engine
`src/prometheus/research/backtest/engine.py:1139–1140` returns `0.0`
defaults when `active.management is None`. This is an artefact gap, NOT
a real zero excursion. Any future MFE / MAE forensic on F1 / D1-A must
recover excursion via Route A or Route B (see §9).

**Comparable fields across F1 / D1-A and V1-arc**: `net_r_multiple`,
`direction`, `symbol`, `slippage_bucket`, `fee_rate_assumption`,
`entry_fill_time_ms`, `exit_fill_time_ms`, `bars_in_trade`,
`exit_reason`. Comparable means same definition.

**Not directly comparable across F1 / D1-A and V1-arc without disclaim**:
`mfe_r` and `mae_r` (artefact gap on F1 / D1-A); the same caveats as
V1-arc for `stop_distance` / `gross_pnl` / `net_pnl` / `notional_usdt`.

**Allowed future forensic uses (under separate authorization)**:
descriptive realized-R / cost-in-R / fee-in-R / slippage-in-R /
funding-in-R distributions on F1 / D1-A using existing trade ledger
fields; descriptive exit-reason composition forensics; cross-population
comparison vs V1-arc under explicit accounting-equivalence disclaim;
MFE / MAE only after Route A or Route B reconstruction (Route B
preferred per §9), and only under separately authorized computation.

**Forbidden future uses**:
F1-prime / F1 with extra filters / F1 hybrid / profitable-subset
extraction; D1-A-prime / D1-B / V1-D1 / F1-D1 hybrid / funding-Z-score
threshold tuning from D1-A forensic numbers; Phase 3s Q6 D1-A finding
as rule input; verdict revision; project-lock revision.

**Rerun governance-admissibility**: F1 / D1-A rerun is governance-
bounded by Phase 3e (post-F1 consolidation) / Phase 3k (post-D1-A
consolidation) / Phase 4z (post-rejection-research-process redesign) /
Phase 4m (V2 consolidation insights) / Phase 4y (post-C1 consolidation).
Rerun would not by itself constitute rescue, but it is not authorized by
Phase 4ao. Route B (offline 15m-join, see §9) is preferred on rescue-
risk grounds because it does not modify or re-execute strategy code.

### 7.3 V2 / G1 / C1

**Fields that exist on disk** (per `data/research/phase4l/tables/`,
`data/research/phase4r/tables/`, `data/research/phase4x/tables/`):
aggregate variant-level CSV tables only; e.g.,
`btc_train_variants.csv`, `btc_oos_variants.csv`,
`btc_train_best_variant.csv`, `cost_sensitivity.csv`,
`m1_m2_m3*_summary.csv`, `parameter_grid.csv`, `pbo_summary.csv`,
`deflated_sharpe_summary.csv`, `cscv_rankings.csv`,
`catastrophic_floor_predicates.csv`, `verdict_declaration.csv`,
`forbidden_work_confirmation.csv`. Plus V2 / G1 / C1-specific aggregate
diagnostics (e.g., regime-state transitions for G1; compression-box
diagnostics for C1).

**Fields that exist in memory only during a run** (per
`scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`,
`scripts/phase4x_c1_backtest.py`): per-trade `TradeRecord` instances
including `entry_time_ms`, `exit_time_ms`, `entry_price`, `exit_price`,
`stop_price`, `tp_price`, `realized_R`, `exit_reason`, etc. V2's
`TradeRecord` additionally has `mfe_R` (computed from 30m bar high /
low at `phase4l_v2_backtest.py:1224–1226`); V2 does NOT track MAE; G1
and C1 do NOT track MFE or MAE.

**Comparable fields across V2 / G1 / C1**: aggregate variant-level
metrics (`mean_R`, `total_R`, `trade_count`, `pf`, `sharpe`,
`max_dd_R`) are comparable per cost cell per window with strict
disclaim that V2 cost-application uses a flat-`entry_price`
approximation per Phase 4am §11.A.10 F-2 (DOCUMENTATION_LIMITATION).

**Not directly comparable across V2 / G1 / C1 and V1-arc / F1 / D1-A
without strong disclaim**: aggregate-only V2 / G1 / C1 metrics vs
per-trade V1-arc / F1 / D1-A `net_r_multiple` distributions; V2 uses
30m bar excursion, V1-arc / F1 / D1-A use 15m; V2 cost application
differs from V1-arc / F1 / D1-A per Phase 4am §11.A.10 F-2; V2 funding
handling boundary differs per Phase 4am §11.A.3 F-1.

**Allowed future forensic uses (governance-risk-unresolved per §10)**:
documenting the V2 / G1 / C1 zero-trade or fires-and-loses outcomes as
historical context (already in Phase 4l / 4r / 4x outputs); citing the
in-memory V2 `mfe_R` distribution as already reported in Phase 4l
outputs (already aggregated in M1 calculation; not per-trade visible);
documenting the always-active baseline result (G1) and the
non-contraction / always-active-same-geometry / delayed-breakout
baselines (C1) as historical context.

**Forbidden future uses**:
V2-prime / V2-narrow / V2-relaxed / V2 hybrid / V2 stop-distance
widening / V2 N1 amendment; G1-prime / G1-narrow / G1-extension / G1
hybrid / classifier relaxation / K_confirm / ATR-band / V_liq_min /
funding-band / E_min amendment; C1-prime / C1-narrow / C1-extension /
C1 hybrid / volume / funding / HTF / mark-price overlay / threshold
tuning from Phase 4x forensic numbers; any rerun under script
modification that introduces relaxed parameters; any rerun whose intent
is to find a "would-have-worked" rescue scenario.

**Rerun governance-admissibility**: per §10 below, conservatively
classified as **governance-risk-unresolved** under the M0 post-null
cooldown rule. Phase 4ao does NOT recommend rerun. Phase 4ao does NOT
authorize rerun. Phase 4ao recommends that any future authorization
discussion of V2 / G1 / C1 rerun first satisfy a separately authorized
docs-only memo addressing OQ-B explicitly.

### 7.4 5m research thread

**Fields that exist**: Phase 3s Q1–Q7 diagnostic outputs (descriptive
diagnostic numbers and tables); no strategy trade ledger.

**Comparable fields**: NONE for strategy-population comparison purposes.
Q1–Q7 are descriptive diagnostics, not trade-ledger fields, and per
Phase 3o §6 forbidden question forms cannot be reused as rule inputs.

**Allowed future forensic uses**: citing Phase 3s Q1–Q7 findings as
descriptive historical context. Citing Phase 3q v001-of-5m manifests
where research-eligible (BTC / ETH 5m trade-price). Referencing 5m as
a path-resolution measurement layer for V1-arc or F1 / D1-A forensics
only under Phase 4al §14 hierarchy and only when an ambiguity threshold
is exposed (§14.C bands).

**Forbidden future uses**: any 5m strategy; reopening of the 5m strategy
thread; conversion of Q1–Q7 findings into rule inputs; new 5m diagnostic
thread without separate authorization; treating 5m mark-price datasets
as research-eligible without Phase 3r §8 governance application
(mark-price 5m manifests remain `research_eligible: false`).

**Rerun governance-admissibility**: N/A — no strategy script to rerun.

## 8. MFE / MAE Methodology Harmonization

Any future forensic computation phase must define MFE / MAE consistently.
Phase 4ao specifies the harmonization rule:

### 8.1 V1-arc (H0 / R3 / R1a / R1b-narrow / R2)

- MFE / MAE definition: 15m bar-extreme based.
- Computation source: existing `mfe_r` / `mae_r` fields populated in
  `trade_log_v1` by `src/prometheus/strategy/v1_breakout/management.py::TradeManagement._update_excursions`
  using 15m `bar.high` / `bar.low` over the trade lifetime including
  the entry bar.
- Bar-resolution caveat: intra-15m-bar stop-vs-MFE sequencing remains
  ambiguous (Phase 4am §11.A.11). Future forensics must disclaim this.
- Single-bar trades (`bars_in_trade = 0`): MFE / MAE come from the
  entry bar's high / low envelope only. Not zero by default; computed
  from `_update_excursions(entry_bar_high, entry_bar_low)` at entry.
- Entry-bar excursion tracked: yes (the V1 management module updates on
  entry bar).
- Exit-bar excursion tracked: yes through the exit event but bounded
  by exit timing within the bar.
- No-trade / zero-qualifying-trade populations: N/A for V1-arc.

### 8.2 F1 / D1-A

- MFE / MAE definition: must be 15m bar-extreme based for harmonization
  with V1-arc.
- Computation source (artefact gap): existing `mfe_r` / `mae_r` fields
  in `trade_log_v1` are uniformly `0.0` due to absent excursion tracker.
- Reconstruction route (under separate authorization): see §9.
- Bar-resolution caveat: same as V1-arc. Disclaim required.
- Single-bar trades: same definition as V1-arc; entry-bar high / low
  envelope.
- No-trade / zero-qualifying-trade populations: N/A for F1 / D1-A.

### 8.3 V2 / G1 / C1

- V2 in-memory MFE: 30m bar-extreme based (existing
  `phase4l_v2_backtest.py:1224–1226`). NOT per-trade persisted; NOT
  available for cross-population cross-resolution comparison without
  rerun.
- V2 MAE: not tracked. No comparable artefact.
- G1 / C1 MFE / MAE: not tracked. No comparable artefact.
- 30m bar-resolution caveat: V2's 30m granularity is coarser than V1-arc
  / F1 / D1-A's 15m. Cross-resolution comparison is methodologically
  fragile and must be disclaimed.
- No-trade populations (V2 zero-trade BTC OOS HIGH; G1 zero-qualifying-
  trade BTC OOS HIGH for train-best; G1 always-active baseline 124
  trades; C1 149 BTC OOS HIGH trades fires-and-loses): forensic
  computation has no per-trade ledger to draw from for V2 / G1; C1's
  149 trades are in-memory only and not persisted.

### 8.4 Lower-timeframe escalation (Phase 4al §14 hierarchy)

- **15m / 30m / 1h / 4h**: signal / event context. Already acquired.
  Sufficient for first-pass MFE / MAE forensics on V1-arc and (via
  reconstruction) on F1 / D1-A.
- **5m**: recommended first lower-timeframe path-resolution layer when
  bar-resolution ambiguity is exposed. Phase 3q v001-of-5m BTCUSDT /
  ETHUSDT trade-price manifests are research-eligible and cover the
  V1-arc / F1 / D1-A OOS windows. Mark-price 5m manifests remain
  `research_eligible: false` per Phase 3q + Phase 3r §8.
- **1m**: escalation only when 5m ambiguity exceeds Phase 4al §14.C
  >10% / >20% bands. NOT acquired. NOT authorized.
- **aggTrades / tick**: final escalation. NOT acquired. NOT
  authorized. Phase 4ao explicitly preserves this boundary.

### 8.5 Bar-ambiguity handling

For any future forensic computation phase:

- Same-bar stop / target ambiguity: stop-first conservative tie-break
  (Phase 4am §11.A.11) is the binding default. Future forensics must
  not retroactively reverse this.
- Same-bar entry / exit (`bars_in_trade = 0`): use entry-bar high / low
  envelope. Phase 4am §11.A.11 F-4 is preserved as documentation; V2
  guards with `if i > entry_idx:` and cannot exit on entry bar; G1 / C1
  lack the guard. For future cross-population forensics this divergence
  must be reported, not silently harmonized.
- Same-bar TP / time-stop ambiguity: target-before-time-stop
  precedence is the binding default (stop > target > time-stop;
  Phase 4l / 4r / 4w specs).
- Same-bar funding event boundary: V2 uses `(entry_ms, exit_ms]`
  (right-inclusive); G1 uses strictly between `(entry_ms, exit_ms)`;
  C1 excludes funding from first-spec. Phase 4am §11.A.3 F-1 is
  preserved as documentation (DEFECT_NON_MATERIAL). Future forensics
  should use the strictly-between convention for harmonization with
  G1 and document the convention explicitly.

## 9. F1 / D1-A Reconstruction Route Decision

The Phase 4an inventory identifies two routes for recovering MFE / MAE
on F1 / D1-A:

### 9.1 Route A — controlled rerun with excursion instrumentation

Modify `src/prometheus/strategy/mean_reversion_overextension/strategy.py`
and `src/prometheus/strategy/funding_aware_directional/strategy.py` to
provide an excursion tracker analogous to V1's
`TradeManagement._update_excursions`. Rerun
`scripts/phase3d_F1_execution.py` and `scripts/phase3j_D1A_execution.py`
under the modified strategy code. Compare new outputs to existing trade
ledgers field-by-field to confirm only `mfe_r` / `mae_r` differ (all
other fields preserved verbatim).

**Pros**: produces native engine-computed MFE / MAE consistent with
V1-arc methodology.

**Cons**:
- requires modifying source code under `src/prometheus/strategy/`;
- requires rerunning historical strategy scripts;
- introduces re-execution risk (e.g., RNG, ordering, dataset hashing
  differences);
- creates surface area for unintended drift in non-excursion fields;
- requires governance review of strategy-code modification under M0 /
  Phase 4al §9 (modifying strategy code, even for excursion-only,
  approaches the boundary between "instrumentation" and "modification");
- harder to validate as no-rescue.

### 9.2 Route B — offline 15m-join reconstruction

Read existing F1 / D1-A trade ledgers; for each trade, compute
MFE / MAE offline by joining `entry_fill_time_ms` →
`exit_fill_time_ms` window with v002 BTCUSDT / ETHUSDT 15m bars and
computing the per-trade MFE / MAE from `bar.high` / `bar.low` over
the join window. Store as a derived artefact under
`data/derived/forensics/<phase>/<symbol>/` (or equivalent) WITHOUT
touching the existing trade ledger or strategy code.

**Pros**:
- does NOT modify any strategy source code;
- does NOT re-execute strategy scripts;
- does NOT regenerate any existing trade ledger;
- can be implemented as a one-shot read-only script under separate
  authorization;
- easier to validate as no-rescue (the script reads ledgers, reads
  bars, writes derived MFE / MAE only);
- preserves Phase 3v §8 stop-trigger-domain governance trivially
  (only trade-price 15m bars are joined; no mark-price domain crossing).

**Cons**:
- bar-resolution caveat at 15m is the same as for V1-arc; further
  resolution requires Phase 4al §14 escalation;
- the join must include or exclude the entry bar consistently with
  V1-arc convention (V1 management's `_update_excursions` is called on
  entry bar; Route B should match);
- the join must match V1-arc on whether the exit bar's full envelope
  is included or only up to the exit fill time (V1 management updates
  through the exit event); Route B should match.

### 9.3 Phase 4ao recommendation (under separate authorization only)

If a future computation phase is ever authorized for F1 / D1-A MFE / MAE
reconstruction, **Route B is preferred** on rescue-risk grounds because
it does not modify or re-execute strategy code. Route A is acceptable as
a backup methodology only after Route B is shown to be insufficient.

**Phase 4ao does NOT authorize either route.** Either route requires a
separately authorized successor phase whose preconditions include the
§14 minimum predeclared-methodology template.

## 10. V2 / G1 / C1 Rerun Admissibility

V2 / G1 / C1 are HARD REJECT — terminal first-spec. Per Phase 4z
(post-rejection-research-process redesign) / Phase 4m (V2 consolidation) /
Phase 4s (G1 consolidation) / Phase 4y (C1 consolidation), the rejection
verdicts are terminal for the first specs and the cooled-down families
list (Phase 4ak post-null cooldown rule + Phase 4ah / 4ai cooled-down
families records) governs.

The OQ-B governance question is:

```text
For V2/G1/C1, does the M0 post-null cooldown rule fully prohibit
rerun-based per-trade forensics, or only forbid forensics that could
be misread as rescue?
```

Phase 4ao provides a **conservative methodology interpretation only**
and does NOT amend M0:

- **V2 / G1 / C1 rerun is conservatively classified as
  governance-risk-unresolved.** The M0 post-null cooldown rule was
  drafted at Phase 4aj / 4ak primarily to prevent rescue-shaped
  re-opening of failed families through descriptor / threshold /
  symbol-universe / interval / forward-horizon / filter / composite-
  weight / rebalance-frequency tweaks. A rerun whose only purpose is
  audit-instrumentation (e.g., persisting per-trade rows from the
  existing in-memory `TradeRecord` lists, without changing any
  parameter, threshold, classifier, or input) is structurally distinct
  from a rescue rerun.
- **However**, Phase 4ao does not have authority to declare audit-only
  rerun admissible under M0. Such a declaration would amend M0 by
  interpretation, which is forbidden by the Phase 4ao non-scope (§2).
- **Therefore Phase 4ao recommends**: any future V2 / G1 / C1 rerun
  authorization discussion must first occur in a separately authorized
  docs-only memo whose scope is explicitly OQ-B resolution; that memo
  must clarify whether the M0 post-null cooldown rule applies only to
  rescue-shaped re-opening or also to audit-only re-execution; and
  that memo must not by itself authorize rerun.
- **Until OQ-B is resolved**, Phase 4ao's conservative recommendation
  is to **defer** V2 / G1 / C1 rerun-based per-trade forensics. V2 / G1 /
  C1 forensics, if any, should be limited to documenting outcomes
  already in Phase 4l / 4r / 4x reports (already aggregated; nothing
  new computed).

**Phase 4ao does NOT authorize V2 / G1 / C1 rerun.** Phase 4ao does NOT
authorize V2 / G1 / C1 script modification. Phase 4ao does NOT authorize
any V2 / G1 / C1 per-trade computation.

## 11. Realized-R / Cost-Field Harmonization

Phase 4am §11.A.10 recorded the V2 cost-application formula
DOCUMENTATION_LIMITATION (V2 uses `cost_R = round_trip_frac × entry_price /
initial_R` flat-`entry_price` approximation rather than the executed-
price-shifting formula used by G1 / C1 per Phase 4q / 4w).

The OQ-C governance question is:

```text
Do Phase 4am V2 cost-application limitations imply that future cross-
population realized-R comparisons need a prospective harmonization spec
before being meaningful?
```

Phase 4ao answer: **YES, with strict separation between V1-arc / F1 /
D1-A engine accounting and V2 / G1 / C1 standalone-script accounting.**

Any future cross-population realized-R comparison must distinguish the
following accounting axes per population:

1. **Engine path**:
   - V1-arc / F1 / D1-A: backtest engine
     (`src/prometheus/research/backtest/`) accounting.
   - V2 / G1 / C1: standalone research script accounting (each script
     implements its own cost / fee / funding accounting; V2 differs from
     G1 / C1 per Phase 4am §11.A.10 F-2).

2. **Fee assumption**:
   - V1-arc / F1 / D1-A: `fee_rate_assumption = 0.0005` (5 bps; per
     `trade_log_v1` field). Total fee per round-trip = 10 bps.
   - V2 / G1 / C1: `TAKER_FEE_PER_SIDE_BPS = 4` per side; total fee per
     round-trip = 8 bps.
   - Cross-population fee comparison MUST disclaim this 5 bps vs 4 bps
     per-side difference and the resulting 10 bps vs 8 bps round-trip
     difference. Both are valid research conventions but they are
     different. §11.6 = 8 bps slippage per side is the LOCK; the 5 bps
     vs 4 bps fee is research-convention, not §11.6.
   - A future harmonization spec MAY report a normalized `fee-in-R`
     under either convention but MUST NOT silently substitute one for
     the other in cross-population comparison.

3. **Slippage assumption**:
   - V1-arc / F1 / D1-A: `slippage_bucket` ∈ {LOW, MEDIUM, HIGH} per
     trade; cost cell variants exist on disk.
   - V2 / G1 / C1: per-cost-cell evaluation at variant aggregate level
     (LOW = 1 bp, MEDIUM = 4 bps, HIGH = 8 bps slippage per side per
     Phase 4k / 4q / 4w).
   - Cross-population slippage comparison should align cost cells
     by per-side bps. The HIGH cell at 8 bps per side matches §11.6
     verbatim across all populations.
   - LOW-slip / MEDIUM-slip variants exist as research evidence on V1-
     arc / F1 / D1-A; they are NOT a license to relax §11.6.

4. **Funding assumption**:
   - V1-arc / F1 / D1-A: funding included via `funding_pnl` field per
     trade.
   - V2: funding included via `searchsorted side="right"` (Phase 4am
     §11.A.3 F-1 DEFECT_NON_MATERIAL).
   - G1: funding strictly between `(entry_ms, exit_ms)`.
   - C1: funding excluded from first-spec per Phase 4w.
   - Cross-population funding comparison MUST disclaim: V2 vs G1 funding
     boundary inclusivity differ (F-1 documented); C1 has no funding
     component (first-spec exclusion).

5. **Cost-cell label**:
   - All populations: LOW / MEDIUM / HIGH per-side bps consistent across
     research conventions; HIGH = 8 bps per side preserved verbatim per
     §11.6.

6. **Stop-trigger-domain label** (Phase 3v §8):
   - V1-arc / F1 / D1-A: `stop_trigger_domain = trade_price_backtest`
     (research backtests use kline trade-price domain).
   - V2 / G1 / C1: behaviour matches `trade_price_backtest` (Phase 4am
     §11.A.5); V2 / G1 do NOT record the four governance labels in
     `run_metadata.json` (Phase 4am F-3 DOCUMENTATION_LIMITATION); C1
     records all four.
   - Cross-population label comparison should treat all six populations
     as `trade_price_backtest` for research purposes; no live-readiness
     interpretation is implied.

7. **Whether reported R is per-trade or aggregate**:
   - V1-arc / F1 / D1-A: per-trade `net_r_multiple` available.
   - V2 / G1 / C1: aggregate `mean_R` per variant per cost cell only;
     per-trade R IN-MEMORY ONLY at run time (not persisted; see
     Phase 4an §6.8 / §6.9 / §6.10).
   - Cross-population aggregation methodology must distinguish these.

**Phase 4ao does NOT revise §11.6.** Any future fee / slippage / funding
decomposition is descriptive only and does not change the locked
project-level cost reference. Historical results are not revised.

**Phase 4ao does NOT propose a unified accounting layer.** Any future
harmonization spec that proposes a unified accounting layer would
require a separately authorized successor phase under M0 / Phase 4al
§9.

## 12. Stop-Trigger-Domain and Mark-Price Boundary

Phase 3v §8 stop-trigger-domain governance is preserved verbatim:

- `trade_price_backtest`: research backtests using kline trade-price
  domain. All V1-arc / F1 / D1-A / V2 / G1 / C1 historical backtests
  carry this label semantically (Phase 4am §11.A.5 confirms). No
  live-readiness implication.
- `mark_price_runtime`: the §1.7.3 lock for any future runtime / paper /
  live operation. Not relevant to docs-only forensics.
- `mark_price_backtest_candidate`: a research label for any future
  backtest that explicitly models mark-price stop-domain. Historically,
  the only mark-price-domain analysis on record is Phase 3s Q6 (D1-A
  mark-stop lag, descriptive-only); no `mark_price_backtest_candidate`
  research run exists.
- `mixed_or_unknown`: invalid; fails closed at any decision boundary.

**Mark-price path forensics is BLOCKED for live-readiness** under
§1.7.3 stop-trigger-domain governance and Phase 3v §8. Any future
mark-price-domain forensics would require a separately authorized
docs-only memo addressing OQ-D and the mark-price-domain admissibility
question explicitly, plus Phase 3r §8 mark-price gap exclusion governance
application (mark-price 5m / 30m / 4h manifests with known invalid
windows).

**Phase 4ao does NOT amend** Phase 3v §8 governance. Phase 4ao does
NOT amend Phase 3r §8 mark-price gap governance. Phase 4ao does NOT
authorize mark-price-domain forensics.

## 13. 5m Boundary

Phase 3t closes the 5m research thread. Phase 4al §14 records the data-
resolution hierarchy and the explicit non-reopening of the 5m strategy
thread.

The OQ-E governance question is:

```text
Where is the boundary between using existing 5m data as a forensic
measurement layer and reopening the closed 5m research thread?
```

Phase 4ao answer (conservative interpretation; does NOT amend Phase 3t):

### 13.1 Allowed conservative uses (under separate authorization)

- **Forensic measurement layer**: referencing existing Phase 3q
  v001-of-5m BTCUSDT / ETHUSDT trade-price 5m manifests
  (`research_eligible: true`) as a finer-resolution measurement layer
  for V1-arc or F1 / D1-A intra-15m bar-resolution ambiguity, only when
  the Phase 4al §14.C ambiguity-rate threshold is exposed (>10%) for
  a specific predeclared forensic question.
- **Citing Q1–Q7 findings** as descriptive historical context (not as
  rule inputs).
- **Documenting the 5m thread closure** as historical context.

### 13.2 Forbidden uses

- **No 5m strategy** (any timeframe-based strategy candidate that uses
  5m as a primary signal timeframe).
- **No Q1–Q7 rule extraction** (Phase 3o §6 forbidden question forms
  remain binding).
- **No lower-timeframe rescue** (using 5m to rescue any V1-arc / F1 /
  D1-A / V2 / G1 / C1 strategy that failed at 15m / 30m / 1h / 4h).
- **No new 5m diagnostic thread unless separately authorized.**
- **No mark-price 5m** unless Phase 3r §8 governance applies and
  separate authorization exists (Phase 3q mark-price 5m manifests
  remain `research_eligible: false`).

### 13.3 Boundary criterion

The boundary criterion that distinguishes "forensic measurement layer"
from "reopened thread":

- **Forensic measurement layer** is allowed if and only if:
  1. the 5m data is used to resolve a specific predeclared bar-
     resolution ambiguity for an existing strategy population's trade
     ledger;
  2. no new 5m strategy or rule is derived;
  3. no Q1–Q7 finding is converted into a rule input;
  4. the 5m data use is documented in the predeclared forensic
     methodology before computation;
  5. the 5m data use is separately authorized by a successor phase.
- **Reopened thread** is what occurs if any of the above conditions is
  violated, OR if the use exceeds passive measurement (e.g., generates
  new 5m diagnostic outputs, derives new rules, or proposes a 5m
  strategy candidate).

**Phase 4ao does NOT authorize** any 5m use, even as a forensic
measurement layer. Any such use requires a separately authorized
successor phase and the §14 minimum predeclared-methodology template.

## 14. Minimum Predeclared-Methodology Template

Any future forensic computation phase MUST satisfy the Phase 4al §9.C
predeclaration discipline AND the Phase 4ak twelve-clause M0 gate AND
the Phase 4al §13 maximum-allowable-Phase-4am-style boundary
specification.

Phase 4ao specifies the minimum template the predeclared methodology
must include. Any successor phase whose predeclaration omits any of
these required headings is not admissible.

### 14.1 Required headings

```text
1. Population(s) included
2. Population(s) excluded
3. Reason for inclusion (one paragraph per population)
4. Artefact source (file paths; manifest references where applicable)
5. Field definitions (referencing Phase 4ao §6 verbatim)
6. Cost assumptions (referencing Phase 4ao §11 axes verbatim)
7. Stop-trigger-domain label (one of: trade_price_backtest |
   mark_price_runtime | mark_price_backtest_candidate; never
   mixed_or_unknown)
8. Timeframe / data-resolution label (one of: 15m | 30m | 1h | 4h |
   5m-measurement-layer-only | 1m-not-authorized | tick-not-authorized)
9. MFE/MAE definition (referencing Phase 4ao §8.1–§8.4 verbatim, or
   a Route B offline-join definition referencing Phase 4ao §9.2
   verbatim)
10. Bar-ambiguity handling (referencing Phase 4ao §8.5 verbatim)
11. Lower-timeframe escalation rule (referencing Phase 4al §14
    hierarchy and §14.C ambiguity-rate bands verbatim)
12. Forbidden interpretations (population-specific list, referencing
    Phase 4ao §7 forbidden-future-uses lists verbatim)
13. Allowed interpretations (population-specific list, referencing
    Phase 4ao §7 allowed-future-forensic-uses lists verbatim)
14. No-rescue statement (verbatim from Phase 4al §9 refined no-rescue
    rule)
15. Verdict / lock preservation statement (verbatim ledger from
    Phase 4ao §19)
16. Outputs to produce (table list, plot list, schema)
17. Stop conditions (M0 / Phase 4al §13 / forbidden-input list)
18. Merge / closeout requirements (per operator phase-branch
    convention recorded in Phase 4an memo)
```

### 14.2 Sample population eligibility under the template

- **V1-arc-only first-pass** (recommended scope if any future computation
  is ever authorized): include H0 / R3 / R1a / R1b-narrow / R2; exclude
  F1 / D1-A / V2 / G1 / C1 / 5m thread; data resolution = 15m;
  artefact source = existing local `trade_log_v1` JSON / Parquet under
  `data/derived/backtests/`; MFE / MAE definition = §8.1; cost
  assumptions = §11 with V1-arc engine path label;
  stop_trigger_domain = trade_price_backtest.
- **F1 / D1-A Route B reconstruction** (if separately authorized
  successor): include F1 and / or D1-A; data resolution = 15m; artefact
  source = existing `trade_log_v1` ledgers + v002 BTCUSDT / ETHUSDT 15m
  bars; MFE / MAE definition = §9.2 (offline 15m-join Route B);
  stop_trigger_domain = trade_price_backtest. Computation script must
  be standalone (no `prometheus.runtime/execution/persistence` imports;
  no network I/O; no credentials).
- **V2 / G1 / C1**: NOT recommended for first-pass forensics. Any
  consideration requires a prior OQ-B-resolution memo (§10).
- **5m thread**: NOT a forensic-population scope; only a measurement-
  layer escalation under §13.3.

### 14.3 Predeclaration timing

The predeclared methodology must be authored and committed BEFORE any
computation script is run, BEFORE any data join is executed, and BEFORE
any output is produced. This is the Phase 4al §9.C discipline applied to
forensic computation.

## 15. Population Eligibility Matrix

| Population   | Artefact status                       | MFE/MAE today                                       | Realized-R today                          | Cost-field today                                    | Rerun needed         | Offline reconstruction                       | Lower TF needed                                | Governance rescue risk | Future forensic eligibility                                                                                                         | Forbidden use                                                                                                                                 |
|--------------|---------------------------------------|-----------------------------------------------------|-------------------------------------------|-----------------------------------------------------|----------------------|----------------------------------------------|------------------------------------------------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| H0           | RECONSTRUCTABLE_WITH_EXISTING         | 15m bar-extreme; populated                          | per-trade                                 | per-trade fees / slippage / funding                 | NO                   | N/A                                          | NO (15m sufficient first-pass)                 | MEDIUM                 | descriptive forensics under §14 template; framework-anchor only                                                                     | reframe as cost-relaxed; reframe baseline; verdict revision                                                                                   |
| R3           | RECONSTRUCTABLE_WITH_EXISTING         | 15m bar-extreme; populated                          | per-trade                                 | per-trade; per-cost-cell variants                   | NO                   | N/A                                          | NO                                             | MEDIUM                 | descriptive forensics; baseline-of-record context; cost-cell sensitivity inspection                                                 | R3-prime; R3 next-spec; parameter tuning; baseline-of-record revision                                                                          |
| R1a          | RECONSTRUCTABLE_WITH_EXISTING         | 15m bar-extreme; populated                          | per-trade                                 | per-trade; per-cost-cell variants                   | NO                   | N/A                                          | NO                                             | HIGH                   | descriptive forensics only; non-leading                                                                                              | R1a-prime; per-bar volatility-percentile filter rescue scaffold                                                                                |
| R1b-narrow   | RECONSTRUCTABLE_WITH_EXISTING         | 15m bar-extreme; populated                          | per-trade                                 | per-trade; per-cost-cell variants                   | NO                   | N/A                                          | NO                                             | HIGH                   | descriptive forensics only; non-leading                                                                                              | R1b-narrow-prime; bias-strength filter rescue scaffold                                                                                          |
| R2           | RECONSTRUCTABLE_WITH_EXISTING         | 15m bar-extreme; populated                          | per-trade                                 | per-trade; per-cost-cell + fill-variant artefacts   | NO                   | N/A                                          | NO                                             | CRITICAL               | descriptive forensics only; cost-fragility evidence                                                                                  | R2-prime; pullback-retest revival; §11.6 relaxation; LOW-slip variant as license                                                              |
| F1           | RECONSTRUCTABLE_WITH_EXISTING (other) | uniformly 0.0 (artefact gap)                        | per-trade                                 | per-trade                                           | YES (for MFE/MAE)    | YES (Route B preferred)                      | NO for first-pass; 5m optional escalation     | CRITICAL               | descriptive realized-R / cost forensics; MFE/MAE only after Route B authorization                                                    | F1-prime; profitable-subset extraction; F1 hybrid; F1 with extra filters                                                                       |
| D1-A         | RECONSTRUCTABLE_WITH_EXISTING (other) | uniformly 0.0 (artefact gap)                        | per-trade                                 | per-trade incl. funding-context fields              | YES (for MFE/MAE)    | YES (Route B preferred)                      | NO for first-pass; 5m optional escalation     | CRITICAL               | descriptive realized-R / cost / funding-context forensics; MFE/MAE only after Route B authorization                                  | D1-A-prime; D1-B; V1-D1; F1-D1; funding-Z-score tuning; Phase 3s Q6 finding as rule input                                                     |
| V2           | RECONSTRUCTABLE_ONLY_WITH_RERUN       | in-memory mfe_R only (30m); no MAE; not persisted   | aggregate variant only                    | aggregate variant only; F-2 cost approximation       | YES                  | NO                                           | NO (30m baseline; coarser than V1-arc 15m)     | CRITICAL               | governance-risk-unresolved per §10; defer until OQ-B resolution                                                                      | V2-prime; V2-narrow; V2-relaxed; V2 hybrid; stop-distance widening; setup-window amendment                                                    |
| G1           | RECONSTRUCTABLE_ONLY_WITH_RERUN       | not tracked in script                               | aggregate variant only                    | aggregate variant only                              | YES                  | NO                                           | NO (30m baseline)                              | CRITICAL               | governance-risk-unresolved per §10; defer until OQ-B resolution                                                                      | G1-prime; classifier relaxation; K_confirm/ATR-band/V_liq_min/funding-band/E_min amendment                                                    |
| C1           | RECONSTRUCTABLE_ONLY_WITH_RERUN       | not tracked in script                               | aggregate variant only                    | aggregate variant only                              | YES                  | NO                                           | NO (30m baseline)                              | CRITICAL               | governance-risk-unresolved per §10; defer until OQ-B resolution                                                                      | C1-prime; volume / funding / HTF / mark-price overlay; threshold tuning from Phase 4x forensic numbers                                       |
| 5m thread    | CLOSED_CONTEXT_ONLY                   | N/A (no strategy)                                   | N/A                                       | N/A                                                 | N/A                  | N/A                                          | itself a measurement-layer escalation only    | CRITICAL               | Q1–Q7 historical context only; 5m measurement-layer use only under §13 conservative criterion + separate authorization              | reopening 5m strategy thread; Q1–Q7 outputs as rule inputs; 5m strategy; new 5m diagnostic thread without separate authorization              |

## 16. Recommendation

### 16.1 Primary

**Remain paused.** Phase 4ao records harmonized methodology and field
definitions on the project record. No computation is required to
proceed; no successor phase is authorized.

### 16.2 Conditional secondary (NOT authorized by Phase 4ao)

The operator may later authorize a future docs-only V1-arc-only
exit-path forensic plan. If so:

- **Population scope**: H0 / R3 / R1a / R1b-narrow / R2.
- **R3 inclusion as baseline-of-record**: R3 is the project's locked
  baseline-of-record. R3 may be included for descriptive forensics
  because:
  - V1-arc R3 already has populated `mfe_r` / `mae_r` / `net_r_multiple`
    fields per `trade_log_v1` schema (no rerun, no offline join, no
    script modification);
  - descriptive R3 forensics is structurally distinct from R3
    optimization, R3-prime, or R3 rescue;
  - R3 cost-cell variants and trade-price stop-domain variants exist
    locally and can be inspected for sensitivity reporting only;
  - R3's role as baseline-of-record is preserved verbatim — no
    descriptive forensic finding licenses revision of this status.
  - Forbidden in any future R3 forensic phase: R3 optimization;
    R3-prime; R3 rescue; R3 next-spec derivation from forensic numbers;
    R3 baseline-of-record revision; conversion of forensic patterns
    into a strategy candidate.
- **Predeclared methodology** must satisfy the §14 template verbatim.
- **Scope**: descriptive only (MFE / MAE / time-to-event / target-
  before-stop / stop-before-target / realized-R / cost-in-R / fee-in-R /
  slippage-in-R / funding-in-R distributions).
- **Forbidden interpretations**: as recorded in §7.1 forbidden-future-
  uses for V1-arc.
- **No-rescue statement**: verbatim from Phase 4al §9.

### 16.3 Conditional tertiary (NOT authorized by Phase 4ao)

The operator may later authorize a future docs-only OQ-B resolution
memo addressing V2 / G1 / C1 rerun admissibility under the M0 post-
null cooldown rule. If authorized, that memo would be a prerequisite
for any future V2 / G1 / C1 rerun consideration, and would itself NOT
authorize rerun.

### 16.4 Conditional quaternary (NOT authorized by Phase 4ao)

The operator may later authorize a future docs-only F1 / D1-A Route B
reconstruction methodology memo (per §9.2 + §14 template). If
authorized, that memo would specify the offline 15m-join script
boundary and predeclared outputs, and would itself NOT authorize
execution.

### 16.5 Not recommended

- Starting any forensic computation without §14 predeclared methodology.
- Treating Phase 4ao's allowed-uses lists as authorization to compute.
- Using Phase 4ao's forbidden-rescue-risk classifications as a
  population-ranking scheme.
- Combining the conditional secondary, tertiary, and quaternary into a
  single successor phase.

### 16.6 Forbidden

- Paper / shadow / live / exchange-write / production-key creation /
  authenticated APIs / private endpoints / public-endpoint calls in
  code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.
- Any strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime /
  R2-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-
  relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1
  hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 /
  F1-D1 / any cross-strategy hybrid).
- Any verdict revision; any project-lock revision; any §11.6 relaxation;
  any §1.7.3 relaxation; any M0 amendment derived from Phase 4ao
  reasoning; any Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 /
  Phase 4j §11 / Phase 4k / 4q / 4w / Phase 4p / 4v amendment;
  reopening the 5m research thread; acquisition of 5m / 1m / aggTrades /
  tick / mark-price 30m / 4h data without separately authorized data-
  requirements memo.

**Phase 4ao does not authorize any successor phase.**

## 17. Implementation / Governance Review

### 17.1 What changed?

Phase 4ao added two new files:

```text
docs/00-meta/implementation-reports/2026-05-06_phase-4ao_exit-path-methodology-artefact-harmonization.md
docs/00-meta/implementation-reports/2026-05-06_phase-4ao_closeout.md
```

and added a narrow paragraph + "Current phase:" block update to:

```text
docs/00-meta/current-project-state.md
```

recording the Phase 4ao harmonization result and reaffirming preserved
verdicts and locks.

### 17.2 What did not change?

- `docs/00-meta/m0-mechanism-admissibility-gate.md` (Phase 4ak governance):
  unchanged.
- All twelve M0 clauses M0.1–M0.12: unchanged.
- The post-null cooldown rule: unchanged.
- The cooled-down families list: unchanged.
- All retained verdicts: unchanged.
- All project locks: unchanged (§11.6, §1.7.3, Phase 3r §8, Phase 3v §8,
  Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q,
  Phase 4v, Phase 4w).
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

### 17.3 Were any locks, verdicts, or safety boundaries affected?

No. All locks, verdicts, and safety boundaries are preserved verbatim.

### 17.4 Were any scripts, source files, data, manifests, or tests modified?

No.

### 17.5 Is the phase mergeable as docs-only?

Yes. Phase 4ao is mergeable as docs-only.

## 18. Research Interpretation Review

### 18.1 What did this phase prove?

Phase 4ao proved, by static repository inspection only, that:

- A single harmonized methodology framework can be defined for any
  future exit-path forensic phase across the ten historical Prometheus
  populations (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, V2, G1, C1) plus
  the 5m thread context, without revising any retained verdict or any
  project lock.
- V1-arc populations require no rerun and no offline reconstruction for
  first-pass MFE / MAE / realized-R / cost-decomposition forensics.
- F1 / D1-A MFE / MAE forensics requires either Route A (rerun with
  excursion instrumentation) or Route B (offline 15m-join). Route B is
  preferred on rescue-risk grounds because it does not modify or re-
  execute strategy code.
- V2 / G1 / C1 rerun-based per-trade forensics is governance-risk-
  unresolved under the M0 post-null cooldown rule and should be
  deferred until a separately authorized OQ-B resolution memo
  clarifies whether audit-only rerun is admissible.
- Cross-population realized-R comparison requires explicit accounting
  separation along seven axes (engine path, fee, slippage, funding,
  cost cell, stop-trigger-domain, per-trade-vs-aggregate); failure to
  separate these would conflate methodologies. §11.6 = 8 bps per side
  is preserved verbatim and is the only axis subject to the project
  lock.
- Stop-trigger-domain governance (Phase 3v §8) and 5m closure (Phase 3t)
  remain binding. Mark-price-domain forensics is BLOCKED for live-
  readiness; 5m may be referenced as a measurement layer only under
  conservative §13.3 criterion and only with separate authorization.
- A minimum predeclared-methodology template (§14) suffices as the
  precondition for any successor computation phase.

### 18.2 What did this phase not prove?

Phase 4ao did NOT prove:

- the actual distributions of MFE / MAE / realized-R / cost-decomposition
  on any population (no computation done);
- whether offline 15m-join Route B reconstruction recovers useful MFE /
  MAE resolution on F1 / D1-A (this is OQ-A; only authorized
  computation can answer);
- whether the M0 post-null cooldown rule formally permits audit-only
  rerun on V2 / G1 / C1 (this is OQ-B; only a separately authorized
  OQ-B-resolution memo can clarify);
- which V1-arc populations are most worth analyzing first
  (no prioritization done);
- any specific numerical claim about cost-cell sensitivity, regime
  fragility, or path patterns.

### 18.3 Which original questions did it answer?

- **OQ-B** (V2 / G1 / C1 rerun under M0): conservatively interpreted
  per §10 as governance-risk-unresolved; Phase 4ao defers to a future
  separately authorized memo.
- **OQ-C** (Phase 4am V2 cost-application limitations and cross-
  population realized-R comparisons): YES, harmonization spec required;
  seven accounting axes specified per §11.
- **OQ-D** (minimum-sufficient predeclared-methodology template):
  specified per §14, with required headings 1–18.
- **OQ-E** (forensic-measurement-layer vs reopened-thread boundary for
  5m): conservative criterion specified per §13.3.

### 18.4 Which original questions remain open?

- **OQ-A** (offline 15m-join MFE / MAE recovery sufficiency for F1 /
  D1-A): cannot be answered without authorized computation; Phase 4ao
  recommends Route B preferred under separate authorization but does
  not authorize.
- The M0-formal-status of audit-only rerun on V2 / G1 / C1 remains
  formally unresolved despite Phase 4ao's conservative interpretation
  in §10. A separately authorized OQ-B resolution memo would be
  required.
- Whether and when the operator wishes to authorize a V1-arc-only
  forensic plan, an F1 / D1-A Route B memo, or an OQ-B resolution memo
  is operator-driven.

### 18.5 What does it mean for strategy research?

It means that any future exit-path forensic phase has a defensible
methodology, definitional, accounting, and governance map already on
the project record. It does NOT mean that any forensic phase is
unblocked. The M0 cooled-down families list is unchanged. No strategy
research is unblocked.

### 18.6 What does it mean for governance?

It means the methodology-harmonization gap identified in Phase 4an is
now closed at the documentation level. Any successor phase has a
single template (§14) to follow, a single per-population eligibility
matrix (§15), and a single set of cross-population accounting axes
(§11). The M0 / Phase 4al §9 / Phase 3v §8 / Phase 3t / Phase 3r §8 /
Phase 4j §11 / Phase 4k / 4q / 4w / Phase 4p / 4v governance is
preserved verbatim.

### 18.7 What is the clean next step?

Remain paused. The harmonization is on record; no successor phase is
authorized; the operator may later authorize a future docs-only V1-
arc-only exit-path forensic plan, an OQ-B resolution memo, or an
F1 / D1-A Route B reconstruction methodology memo, or none of these.

### 18.8 What should we not do yet?

Do not start any forensic computation. Do not rerun any strategy script.
Do not run an offline join. Do not modify any strategy or backtest code.
Do not acquire 5m / 1m / aggTrades / tick / mark-price 30m / 4h data.
Do not reopen the 5m research thread. Do not propose a new strategy. Do
not authorize Phase 4ap / Phase 5 / Phase 4 canonical / paper / shadow /
live / exchange-write / production keys / authenticated APIs / private
endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
credentials. Do not modify the M0 governance document. Do not modify
any retained verdict. Do not modify any project lock.

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

- M0 governance remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- §11.6 HIGH cost remains preserved. Any future fee / slippage / funding
  decomposition may be reported descriptively only and must not change
  the locked project-level cost reference or revise historical results.
- §1.7.3 project-level locks remain:
  - 0.25% risk per trade;
  - 2× leverage cap;
  - one position max;
  - mark-price stops where applicable.
- Phase 3r §8 mark-price gap governance preserved.
- Phase 3v §8 stop-trigger-domain governance preserved.
- Phase 3w §6 / §7 / §8 break-even / EMA-slope / stagnation governance
  preserved.
- Phase 4j §11 metrics OI-subset partial-eligibility rule preserved.
- Phase 4k V2 backtest-plan methodology preserved.
- Phase 4p G1 strategy-spec memo preserved.
- Phase 4q G1 backtest-plan methodology preserved.
- Phase 4v C1 strategy-spec memo preserved.
- Phase 4w C1 backtest-plan methodology preserved.
- Phase 4ak twelve-clause M0 mechanism-admissibility gate preserved.
- Phase 4ak post-null cooldown rule preserved.
- Phase 4ak cooled-down families list preserved.
- Phase 4al refined no-rescue rule preserved.
- Phase 4al §13 future-Phase-4am-style boundary specification preserved.
- Phase 4al §14 data-resolution hierarchy preserved.
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4) preserved.
- Phase 4an inventory result preserved.

**No-rescue constraints (preserved verbatim):**

- No R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / F1-prime /
  D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid /
  G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any
  cross-strategy hybrid.
- No conversion of Phase 4ao methodology / harmonization findings into
  strategy candidates.
- No conversion of Phase 4ao forbidden-rescue-risk classifications into
  parameter-tuning input.
- No reopening of the 5m research thread.
- No M0-governance amendment derived from Phase 4ao reasoning.
- No verdict revision.
- No project-lock revision.

Phase 4 (canonical) remains unauthorized.

Phase 4ap / Phase 5 / any successor phase remains unauthorized.

Paper / shadow, live-readiness, deployment, production keys, authenticated
APIs, private endpoints, public-endpoint calls in code, user stream,
WebSocket, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and
5m / 1m / aggTrades / tick / mark-price 30m / 4h data acquisition all
remain unauthorized.

**Recommended state remains paused.**

**No next phase authorized.**
