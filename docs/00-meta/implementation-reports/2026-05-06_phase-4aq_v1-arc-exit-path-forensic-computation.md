# Phase 4aq — V1-Arc Exit-Path Forensic Computation

## 1. Executive summary

Phase 4aq is the docs-and-code execution of the Phase 4ap V1-Arc
Exit-Path Forensic Plan. It adds the standalone forensic script
[`scripts/phase4aq_v1_arc_exit_path_forensics.py`](../../../scripts/phase4aq_v1_arc_exit_path_forensics.py),
loads every Phase 4ap-allowlisted V1-arc trade-log artefact under
`data/derived/backtests/phase-2*`, and computes the predeclared Phase
4ap §12 descriptive metrics across the included populations (H0, R3,
R1a, R1b-narrow, R2). The Phase 4aq script writes its outputs to a
local research directory, `data/research/phase4aq/`, that follows the
established Phase 4ai / 4l / 4r / 4x convention of remaining a local,
non-committed research artefact.

**Computation status: `SUCCESSFUL_COMPUTATION`.**

- **Loaded artefacts:** 23 allowlisted directories × 2 symbols
  (BTCUSDT, ETHUSDT) = 46 (directory, symbol) pairs.
- **Total trades loaded:** 973 across all populations, windows, cost
  cells, stop-domain variants, and fill variants.
- **Schema validation:** 100% pass. Every loaded ledger contained the
  full Phase 4ap §11 required-field set. Optional fields `quantity`
  and `notional_usdt` are present in every loaded ledger.
- **Stop-trigger-domain inference:** uniform `trade_price_backtest`
  for every loaded V1-arc historical artefact (Phase 4ap §15 inference;
  recorded in `schema_validation_report.csv`).
- **Forbidden questions answered:** zero. All Phase 4ap §9 forbidden
  question forms (F1–F10) are recorded `NOT_PERFORMED` in
  `forbidden_interpretation_checklist.md`.
- **Stop conditions:** Phase 4ap SC-1 through SC-11 all `PASS`.

This memo follows Phase 4ap §10–§17 verbatim and is descriptive only.
No verdict is revised. No project lock is changed. No M0 governance is
modified. No successor phase is authorized.

## 2. Scope and explicit non-scope

### 2.1 Scope

- Read-only access to existing local V1-arc trade-log artefacts under
  `data/derived/backtests/phase-2e-baseline`,
  `data/derived/backtests/phase-2g-wave1-h0-r`,
  `data/derived/backtests/phase-2l-r3-*`,
  `data/derived/backtests/phase-2m-r1a-*`,
  `data/derived/backtests/phase-2s-r1b-*`, and
  `data/derived/backtests/phase-2w-r2-*` (Phase 4ap §10 allowlist).
- Computation of Phase 4ap §12 descriptive metrics:
  MFE_R, MAE_R, net_R, gross_R, cost_in_R, fee_in_R, funding_in_R,
  estimated_slippage_in_R (descriptive), reached_+1R / +2R / +3R
  flags, mfe_capture_ratio, giveback_from_mfe,
  favorable_excursion_before_stop_proxy (proxy),
  adverse_before_favorable_flag (NOT_AUDITABLE),
  bar_resolution_ambiguity_flag.
- Aggregations grouped by `(population, window_type, cost_cell,
  stop_domain_variant, fill_variant, symbol)`.
- Writing local outputs under `data/research/phase4aq/`.
- Authoring this memo and the Phase 4aq closeout.
- Narrow update to `docs/00-meta/current-project-state.md`.

### 2.2 Explicit non-scope (forbidden by Phase 4ap and Phase 4aq brief)

- No new strategy, exit system, or candidate is proposed.
- No R3 optimization. No R3-prime / R3 next-spec / R3 successor.
- No R3 rescue framing. No baseline-of-record revision.
- No R1a-prime / R1b-narrow-prime promotion.
- No R2 cost-fragility relaxation. R2 verdict (FAILED — §11.6) is
  preserved verbatim.
- No H0 framework-anchor revision.
- No F1 / D1-A / V2 / G1 / C1 / 5m population is loaded or
  referenced as input.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h / mark-price
  5m / mark-price 15m data is used.
- No backtest is run.
- No historical strategy script is executed.
- No data acquisition. No data file is modified. No manifest is
  modified. No existing trade-log is modified.
- No `src/prometheus/` modification. No test modification. No
  existing-script modification.
- No `.gitignore` modification.
- No M0 governance modification. No retained verdict revision. No
  project lock change.
- No successor phase is authorized. No 5m research thread is
  reopened.

## 3. Repository verification summary

```
Pre-branch state (main):
  main             = 4cad1f6444605f10366f86d448e77bfd401771db
  origin/main      = 4cad1f6444605f10366f86d448e77bfd401771db
  branch           = main (clean working tree;
                          .claude/scheduled_tasks.lock and data/research/
                          shown as untracked transient/local-only)

Required Phase 4ap files present on main:
  docs/00-meta/implementation-reports/2026-05-06_phase-4ap_v1-arc-exit-path-forensic-plan.md
  docs/00-meta/implementation-reports/2026-05-06_phase-4ap_closeout.md
  docs/00-meta/implementation-reports/2026-05-06_phase-4ap_merge-closeout.md

Branch created:
  phase-4aq/v1-arc-exit-path-forensic-computation
```

Allowlisted V1-arc directory presence verified before script
execution: 23 of 23 directories present locally; both `BTCUSDT` and
`ETHUSDT` symbol subdirectories present in every directory's latest
timestamped run subdirectory.

## 4. Methodology

### 4.1 Phase 4ap plan adherence

The Phase 4aq script implements the Phase 4ap §6–§17 plan verbatim.

- Population scope: H0, R3, R1a, R1b-narrow, R2 (Phase 4ap §6).
- Excluded: F1, D1-A, V2, G1, C1, 5m research thread (Phase 4ap §6).
- Predeclared questions Q1–Q14: answered descriptively only (Phase
  4ap §8).
- Forbidden questions F1–F10: recorded as `NOT_PERFORMED` in
  `forbidden_interpretation_checklist.md` (Phase 4ap §9).
- Required field schema: enforced as fail-closed (Phase 4ap §11).
- Metric definitions: Phase 4ap §12.
- Timeframe rule: 15m bar-extreme only; no lower-timeframe data
  (Phase 4ap §13).
- Cost rule: §11.6 = 8 bps slippage per side preserved; cost-cell
  comparisons descriptive only (Phase 4ap §14).
- Stop-trigger-domain rule: V1-arc historical artefacts inferred to
  `trade_price_backtest`; `mixed_or_unknown` would be a fail-closed
  condition (Phase 4ap §15).
- Output specification: 11 artefacts under `data/research/phase4aq/`
  (Phase 4ap §16).
- Stop conditions: Phase 4ap SC-1 through SC-11 (Phase 4ap §17).

### 4.2 Standalone-script boundary

The Phase 4aq script is a standalone research script. It is not part
of the Prometheus runtime. It does not import from
`prometheus.runtime`, `prometheus.execution`, or
`prometheus.persistence`. It does not perform any network I/O, does
not call any Binance or `data.binance.vision` endpoint, does not load
credentials or `.env`, does not read any private endpoint, user
stream, WebSocket, or listenKey. It does not execute any historical
backtest script. It does not modify any existing artefact.

### 4.3 Artefact discovery and loading

For each Phase 4ap §10 allowlisted directory, the script selects the
lexicographically-largest immediate timestamped subdirectory as the
canonical run. Within each `<run>/<symbol>/` directory, the script
loads exactly one canonical trade ledger:

- Parquet preferred (`trade_log.parquet`).
- JSON fallback (`trade_log.json`) if Parquet is absent.
- Both files are present in every loaded V1-arc directory; the
  Parquet file is selected in every case.

The script never loads both formats from the same directory. The
selected source format is recorded in
`loaded_artifacts_manifest.csv`.

### 4.4 Schema validation

For each loaded ledger, the script validates the Phase 4ap §11
required-field schema. A required-field-missing condition would
trigger Phase 4ap SC-2 fail-closed and halt computation. No required
field was missing across the 46 loaded (directory, symbol) pairs.
Optional fields `quantity`, `notional_usdt`, and `schema_version`
are present in every loaded ledger.

### 4.5 Label assignment

Each loaded trade is tagged with seven explicit labels (Phase 4ap
§10 / §11):

- `population` ∈ {H0, R3, R1a, R1b-narrow, R2}.
- `run_family` (= directory name; e.g. `phase-2l-r3-r-slip=LOW`).
- `window_type` ∈ {R, V}.
- `cost_cell` ∈ {default, LOW, HIGH}.
- `stop_domain_variant` ∈ {default, TRADE_PRICE}.
- `fill_variant` ∈ {default, limit-at-pullback}.
- `symbol` ∈ {BTCUSDT, ETHUSDT}.

The directory-level `cost_cell=default` represents the
non-`slip=`-suffixed run (which uses the engine default cost cell —
typically MEDIUM, as recorded by the per-trade `slippage_bucket`
field). The per-trade `slippage_bucket` field is preserved through
to the output as the ground-truth per-trade cost-cell value.

Each loaded trade also carries the inferred
`stop_trigger_domain = trade_price_backtest` and the fixed
`timeframe = 15m`.

### 4.6 Metric computation

The Phase 4aq script computes Phase 4ap §12 metrics per trade. Of
particular note:

- `cost_in_R`, `fee_in_R`, and `funding_in_R` are exact-from-fields,
  derived directly from `gross_pnl`, `net_pnl`, `entry_fee`,
  `exit_fee`, `funding_pnl`, and `realized_risk_usdt`.
- `estimated_slippage_in_R` is a **descriptive estimate** only,
  derived from `slippage_bucket` mapped to per-side bps
  (`{LOW: 1, MEDIUM: 4, HIGH: 8}`) with round-trip = `2 *
  per_side_bps` and notional taken from `notional_usdt` (or
  `abs(quantity) * entry_fill_price` fallback). The identity
  `cost_in_R == fee_in_R + estimated_slippage_in_R + funding_in_R`
  is **not asserted**. A `cost_reconciliation_note` accompanies
  every per-trade record.
- `mfe_capture_ratio = net_R / MFE_R` is reported only where
  `MFE_R > 0`; otherwise NA.
- `giveback_from_mfe = MFE_R - net_R` is reported descriptively
  with no clamping; negative values are preserved as descriptive
  edge-case context, not forced to zero, and are not interpreted as
  rescue framing.
- `favorable_excursion_before_stop_proxy` is computed for STOP
  exits only as `mfe_r > 0`. It is labelled **proxy** because the
  existing 15m schema does not preserve intrabar event order.
- `adverse_before_favorable_flag` is set to
  `NOT_AUDITABLE_FROM_EXISTING_FIELDS` for every trade, per Phase
  4ap §12. No lower-timeframe data is consulted.
- `bar_resolution_ambiguity_flag` is set to `True` only when
  `bars_in_trade == 0` (entry/exit same-bar). No lower-timeframe
  data is consulted; per Phase 4ap §13 the script does not infer
  intrabar sequencing.

### 4.7 Aggregation

The script aggregates per-trade metrics by the seven-label group key.
Each output table reports counts plus mean/median (and, where
relevant, additional quantiles) for the metric of interest. No metric
attempts to rank populations for promotion. No metric is converted
into a parameter selection. No metric is interpreted as strategy
evidence.

## 5. Computation status

`SUCCESSFUL_COMPUTATION`.

- Discovery: 46 (directory, symbol) artefact pairs across 23 unique
  run directories.
- Loading: 973 trades loaded successfully.
- Schema validation: 100% pass.
- Stop conditions: SC-1 through SC-11 all `PASS`.
- Forbidden-input audit: no excluded population (F1, D1-A, V2, G1,
  C1, 5m) was loaded or referenced.
- Output bundle: 11 artefacts written under `data/research/phase4aq/`.

## 6. Artefact loading summary

### 6.1 Per-population totals (all variants and windows)

| population | total trades loaded |
|------------|---------------------|
| H0         | 154                 |
| R3         | 392                 |
| R1a        | 110                 |
| R1b-narrow | 88                  |
| R2         | 229                 |
| **Total**  | **973**             |

### 6.2 Loaded directories (23 distinct, latest run each)

H0 (2 directories): `phase-2e-baseline`, `phase-2g-wave1-h0-r`.

R3 (5 directories): `phase-2l-r3-r`, `phase-2l-r3-r-slip=LOW`,
`phase-2l-r3-r-slip=HIGH`, `phase-2l-r3-r-stop=TRADE_PRICE`,
`phase-2l-r3-v`.

R1a (5 directories): `phase-2m-r1a-r1a_plus_r3-r`,
`phase-2m-r1a-r1a_plus_r3-r-slip=LOW`,
`phase-2m-r1a-r1a_plus_r3-r-slip=HIGH`,
`phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE`,
`phase-2m-r1a-r1a_plus_r3-v`.

R1b-narrow (5 directories): `phase-2s-r1b-r1b_narrow-r`,
`phase-2s-r1b-r1b_narrow-r-slip=LOW`,
`phase-2s-r1b-r1b_narrow-r-slip=HIGH`,
`phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE`,
`phase-2s-r1b-r1b_narrow-v`.

R2 (6 directories): `phase-2w-r2-r2_r3-r`,
`phase-2w-r2-r2_r3-r-slip=LOW`,
`phase-2w-r2-r2_r3-r-slip=HIGH`,
`phase-2w-r2-r2_r3-r-stop=TRADE_PRICE`,
`phase-2w-r2-r2_r3-r-fill=limit-at-pullback`,
`phase-2w-r2-r2_r3-v`.

### 6.3 Selected canonical ledger format

For all 46 (directory, symbol) pairs, the canonical ledger is the
Parquet file `trade_log.parquet`. JSON fallback was not exercised.
See `data/research/phase4aq/loaded_artifacts_manifest.csv` for the
full per-(directory, symbol) inventory with paths, run_id, and
labels.

### 6.4 Inferred fields

Every loaded V1-arc trade record carries:

- `stop_trigger_domain = trade_price_backtest` (Phase 4ap §15
  inference for V1-arc historical artefacts);
- `timeframe = 15m` (Phase 4ap §13 fixed value).

These are the only inferred labels. All other Phase 4ap §11 required
fields are present as direct values in the loaded ledgers. The
inference is recorded explicitly in
`schema_validation_report.csv`.

## 7. Schema validation summary

All 46 loaded (directory, symbol) pairs passed Phase 4ap §11 required-
field validation. None triggered Phase 4ap SC-2 fail-closed.

- Required fields present (23 fields): `trade_id`, `direction`,
  `symbol`, `entry_fill_time_ms`, `exit_fill_time_ms`,
  `entry_fill_price`, `exit_fill_price`, `initial_stop`,
  `stop_distance`, `realized_risk_usdt`, `gross_pnl`, `net_pnl`,
  `net_r_multiple`, `entry_fee`, `exit_fee`, `funding_pnl`,
  `fee_rate_assumption`, `slippage_bucket`, `exit_reason`,
  `bars_in_trade`, `mfe_r`, `mae_r`, `stop_was_gap_through`.
- Optional fields present (every loaded ledger): `quantity`,
  `notional_usdt`. `schema_version` is present in the JSON wrappers
  (where read).

## 8. Output artefact summary

All Phase 4aq outputs were written under `data/research/phase4aq/`:

- `loaded_artifacts_manifest.csv` — per-(directory, symbol) inventory
  with 46 rows, including selected canonical-ledger paths, run_id,
  population, window_type, cost_cell, stop_domain_variant,
  fill_variant, symbol, inferred stop_trigger_domain, and timeframe.
- `schema_validation_report.csv` — per-(directory, symbol) schema
  validation result with 46 rows; required-fields-missing column is
  empty for every row; fail_closed = "no" for every row.
- `population_summary.csv` — per-group counts and net_R / MFE_R /
  MAE_R summary metrics across all loaded variants.
- `mfe_mae_distribution_by_population.csv` — per-group MFE_R and
  MAE_R quantiles (mean, median, p25, p75, p90, p95, max), plus
  `giveback_from_mfe_mean / p50` and
  `mfe_capture_ratio_mean / p50 / n`.
- `realized_r_by_population.csv` — per-group net_R distribution
  (mean, stdev, min, p10, p25, p50, p75, p90, p95, p99, max).
- `cost_in_r_by_population.csv` — per-group descriptive cost
  decomposition (cost_in_R, fee_in_R, funding_in_R,
  estimated_slippage_in_R) with reconciliation note.
- `exit_reason_breakdown.csv` — per-group exit-reason counts.
- `excursion_threshold_touch_rates.csv` — per-group fraction reaching
  `+1R / +2R / +3R`.
- `ambiguity_report.csv` — per-group bar-resolution ambiguity rate,
  Phase 4al §14.C descriptive band, and an explicit
  Phase-4aq-does-not-authorize-lower-timeframe-acquisition note.
- `forbidden_interpretation_checklist.md` — Phase 4ap §9 F1–F10
  recorded as NOT_PERFORMED.
- `v1_arc_forensic_report.md` — full human-readable forensic report.

These files are local research outputs, generated reproducibly by
`scripts/phase4aq_v1_arc_exit_path_forensics.py` from the existing
local V1-arc trade-log artefacts. They are not committed to git.
The convention follows Phase 4ai / 4l / 4r / 4x precedent
(`data/research/<phase>/` outputs remain local-only).

## 9. Results — Phase 4ap Q1–Q14

### 9.1 Q1–Q3 distributional findings (R-window, default cell)

Cell scope: R-window, default cost cell, default stop_domain_variant,
default fill_variant. Descriptive only.

| population | symbol | n | net_R_mean | net_R_p50 | MFE_R_mean | MFE_R_p50 | MAE_R_mean | MAE_R_p50 |
|------------|--------|---|-----------:|----------:|-----------:|----------:|-----------:|----------:|
| H0         | BTC    | 74| -0.443     | -0.545    | 0.874      | 0.553     | 0.619      | 0.562     |
| H0         | ETH    | 80| -0.422     | -0.530    | 1.150      | 0.846     | 0.523      | 0.521     |
| R1a        | BTC    | 22| -0.420     | -0.640    | 0.622      | 0.366     | 0.710      | 0.695     |
| R1a        | ETH    | 23| -0.114     | -0.654    | 1.418      | 1.036     | 0.529      | 0.514     |
| R1b-narrow | BTC    | 10| -0.263     | -0.499    | 0.861      | 0.570     | 0.720      | 0.844     |
| R1b-narrow | ETH    | 12| -0.224     | -0.433    | 0.956      | 0.831     | 0.599      | 0.640     |
| R2         | BTC    | 23| -0.275     | -0.480    | 1.102      | 0.772     | 0.594      | 0.626     |
| R2         | ETH    | 19| -0.432     | -1.151    | 1.128      | 0.858     | 0.637      | 0.587     |
| R3         | BTC    | 33| -0.240     | -0.350    | 0.792      | 0.531     | 0.635      | 0.564     |
| R3         | ETH    | 33| -0.351     | -0.654    | 1.060      | 0.849     | 0.519      | 0.514     |

These are descriptive distributional values for the primary R-window
default cell. They do not constitute a strategy ranking. They do not
authorize parameter changes. They do not justify verdict revision.
See `population_summary.csv`,
`mfe_mae_distribution_by_population.csv`, and
`realized_r_by_population.csv` for full per-cell quantile detail
including LOW / HIGH cost cells, TRADE_PRICE stop variant,
limit-at-pullback fill variant, and validation-window cells.

### 9.2 Q4–Q5 relationship findings

`mfe_capture_ratio = net_R / MFE_R` and
`giveback_from_mfe = MFE_R - net_R` distributions per group are
recorded in `mfe_mae_distribution_by_population.csv`. They are
descriptive context. Phase 4aq does not interpret them as strategy
evidence.

### 9.3 Q6 threshold-touch findings (R-window, default cell)

| population | symbol | n | frac_+1R | frac_+2R | frac_+3R |
|------------|--------|---|---------:|---------:|---------:|
| H0         | BTC    | 74| 0.270    | 0.135    | 0.081    |
| H0         | ETH    | 80| 0.400    | 0.175    | 0.075    |
| R1a        | BTC    | 22| 0.182    | 0.136    | 0.000    |
| R1a        | ETH    | 23| 0.565    | 0.174    | 0.043    |
| R1b-narrow | BTC    | 10| 0.300    | 0.200    | 0.000    |
| R1b-narrow | ETH    | 12| 0.417    | 0.167    | 0.000    |
| R2         | BTC    | 23| 0.478    | 0.130    | 0.043    |
| R2         | ETH    | 19| 0.474    | 0.158    | 0.053    |
| R3         | BTC    | 33| 0.273    | 0.121    | 0.030    |
| R3         | ETH    | 33| 0.424    | 0.182    | 0.030    |

Full table is in `excursion_threshold_touch_rates.csv`. These are
descriptive frequencies. They are not parameter selections.
They are not take-profit recommendations.

### 9.4 Q7 favorable-before-stop proxy

For STOP-exit trades, `favorable_excursion_before_stop_proxy` is set
to `mfe_r > 0`. The flag is **proxy** only because the existing 15m
schema does not preserve intrabar event order. Per-trade values are
preserved internally; population-level summaries are not interpreted
as sequencing evidence.

### 9.5 Q8 giveback-from-MFE distribution

See `mfe_mae_distribution_by_population.csv` columns
`giveback_from_mfe_mean` and `giveback_from_mfe_p50`. No clamping
applied. Negative values, where present, are descriptive context.

### 9.6 Q9 adverse-before-favorable

`NOT_AUDITABLE_FROM_EXISTING_FIELDS` for every trade. Phase 4ap §12 /
§13 explicitly forbid inferring this from final MFE / MAE alone or
from lower-timeframe data not authorized by Phase 4ap.

### 9.7 Q10 favorable-before-stop fraction

Population-level fraction of STOP-exit trades whose `mfe_r > 0`.
Population-level summaries are reported through the aggregate output
artefacts; per-trade proxy values are computed internally by the
Phase 4aq script but are not emitted as a separate named per-trade
output file. See `exit_reason_breakdown.csv` for STOP-exit counts
per cell.

### 9.8 Q11–Q12 cost decomposition (descriptive only)

See `cost_in_r_by_population.csv`. The per-group descriptive cost
decomposition reports `cost_in_R`, `fee_in_R`, `funding_in_R`, and
`estimated_slippage_in_R`. The identity
`cost_in_R == fee_in_R + estimated_slippage_in_R + funding_in_R` is
not asserted.

R2 cost-cell columns are descriptive evidence only. They do not
relax §11.6, do not justify R2 rescue, and do not authorize a
cost-model revision.

### 9.9 Q13 cross-population descriptive comparison

The Q1 and Q6 tables above implicitly compare populations on the
primary R-window default cell. No promotion ranking is implied.
- H0 remains the framework anchor.
- R3 remains baseline-of-record.
- R1a / R1b-narrow remain retained — non-leading.
- R2 remains FAILED — §11.6.

### 9.10 Q14 bar-resolution ambiguity

Phase 4al §14.C descriptive bands (heuristic only):

- `<2%`   : 5m would likely be sufficient if separately authorized.
- `2-10%` : 5m would be usable with conservative stop-first
  assumptions.
- `10-20%`: 1m escalation may be considered if separately authorized.
- `>20%`  : 5m would likely be too coarse if separately authorized.

Per primary R-window default cell, ambiguity rates fall in the
`2-10%` and `10-20%` bands across the included populations and
symbols (BTCUSDT cells `2-10%`; ETHUSDT cells `10-20%`). These are
descriptive only. **Phase 4aq does NOT authorize 5m / 1m /
aggTrades / tick / mark-price acquisition or use.** Any future
forensic-measurement-layer decision requires separate operator
authorization under Phase 4al §14 and Phase 4ao §13.3.

See `ambiguity_report.csv` for the full per-cell breakdown.

## 10. R3 baseline boundary (Phase 4ap §7)

R3 is included in this Phase 4aq computation strictly as the V1-arc
baseline-of-record for descriptive context. R3 forensic findings in
this report do not authorize:

- R3 optimization;
- R3-prime / R3 next-spec / R3 successor;
- R3 rescue framing;
- baseline-of-record revision;
- conversion of R3 forensic numbers into entry rules, exit rules,
  parameters, or thresholds;
- introducing a new V1-arc strategy candidate based on R3
  observations.

R3 retains BASELINE-OF-RECORD verdict. No aspect of Phase 4aq
modifies that status.

## 11. R2 cost-fragility boundary

R2 retains FAILED — §11.6. The Phase 4aq cost-cell descriptive
findings on R2 (across LOW / default / HIGH cost cells, TRADE_PRICE
stop variant, limit-at-pullback fill variant, R-window and V-window)
are retained-research-evidence context only. They do not justify
§11.6 relaxation. They do not authorize R2 rescue. They do not
produce R2-prime.

## 12. R1a / R1b-narrow boundary

R1a and R1b-narrow retain RETAINED — NON-LEADING. Phase 4aq
descriptive findings do not authorize:

- R1a-prime;
- R1b-narrow-prime;
- promotion to leading status;
- conversion to a new ex-ante hypothesis without satisfying the
  Phase 4m 18-requirement validity gate AND the Phase 4ak twelve-
  clause M0 gate AND the Phase 4al §9 refined no-rescue rule.

## 13. H0 boundary

H0 retains FRAMEWORK ANCHOR. Phase 4aq descriptive findings do not
authorize:

- H0-prime;
- framework-anchor revision;
- hybrid candidates with H0 as a structural lineage source.

## 14. Cost decomposition limitation

`estimated_slippage_in_R` is descriptive and estimated, not exact.
The Phase 4aq script does not assert
`cost_in_R == fee_in_R + estimated_slippage_in_R + funding_in_R`.
Each per-trade record carries a `cost_reconciliation_note` documenting
this. Any divergence between `cost_in_R` and the sum of `fee_in_R +
estimated_slippage_in_R + funding_in_R` is descriptive context, not
a finding requiring fee / slippage / funding-model revision.

§11.6 = 8 bps slippage per side is preserved verbatim. The
historical cost reference is unchanged by Phase 4aq.

## 15. Sequence-claim limitation

Phase 4ap §14: the Phase 4aq script does not infer event order from
final MFE_R and MAE_R alone.

- `adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`
  for every trade.
- `favorable_excursion_before_stop_proxy` is labelled **proxy** for
  STOP exits.
- No lower-timeframe data is consulted.
- The 15m bar is the only resolution used.

## 16. Bar-resolution ambiguity section

Bar-resolution ambiguity is computed from `bars_in_trade == 0` only,
the only signal recoverable from existing 15m fields. Per primary
R-window default cell, the ambiguity rates fall in the Phase 4al
§14.C `2-10%` (BTC) and `10-20%` (ETH) bands. This is descriptive
context only. Phase 4aq does not authorize 5m / 1m escalation. Any
future forensic-measurement-layer decision requires separate operator
authorization.

## 17. Forbidden interpretation checklist

See `forbidden_interpretation_checklist.md`. All Phase 4ap §9
forbidden question forms (F1–F10) are recorded as `NOT_PERFORMED`.
Phase 4aq did not address any forbidden question form.

## 18. Stop-condition review (Phase 4ap §17)

| ID    | Condition                                | Result |
|-------|------------------------------------------|--------|
| SC-1  | Required artefact missing                | PASS — no artefact missing |
| SC-2  | Required field missing                   | PASS — all required fields present |
| SC-3  | mixed_or_unknown stop_trigger_domain     | PASS — inferred trade_price_backtest only |
| SC-4  | Schema mismatch                          | PASS — Parquet/JSON parsed cleanly |
| SC-5  | Excluded population detected             | PASS — allowlist enforces inclusion-only |
| SC-6  | 5m/1m/tick/mark-price use w/o auth       | PASS — none used |
| SC-7  | Promotion ranking attempted              | PASS — none attempted |
| SC-8  | Parameter-change proposal                | PASS — none made |
| SC-9  | Verdict / lock revision                  | PASS — none made |
| SC-10 | Strategy interpretation                  | PASS — descriptive reporting only |
| SC-11 | Quality-gate failure                     | PASS — `ruff check` and `python -m compileall` clean |

## 19. Implementation / governance review

### 19.1 What changed?

- New file: `scripts/phase4aq_v1_arc_exit_path_forensics.py` (standalone
  research script).
- New local research outputs under `data/research/phase4aq/` (not
  committed, follows Phase 4ai / 4l / 4r / 4x convention).
- New file: this Phase 4aq memo at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md`.
- New file: Phase 4aq closeout at
  `docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`.
- Narrow update to `docs/00-meta/current-project-state.md` adding the
  Phase 4aq narrative paragraph and current-phase block.

### 19.2 What did not change?

- No modification to `src/prometheus/`.
- No modification to any test file.
- No modification to any existing script under `scripts/`.
- No modification to any data file under `data/raw/`,
  `data/normalized/`, or `data/derived/`.
- No modification to any manifest under `data/manifests/`.
- No new manifest created.
- No `.gitignore` modification.
- No retained verdict revised.
- No project lock changed.
- No M0 governance modified.
- No data acquisition.
- No backtest run.
- No historical script execution.
- No 5m research thread reopened.

### 19.3 Are any locks, verdicts, or safety boundaries affected?

No. The full retained verdict ledger and all project locks remain
preserved verbatim; see §22.

### 19.4 Mergeable as docs-and-code?

Yes. The Phase 4aq script passes the project's lint (`ruff check`)
and bytecode-compile (`python -m compileall`) gates. The local
research outputs are reproducible from the script and existing
V1-arc trade-log artefacts; the script is the canonical mode of
regenerating them.

## 20. Research interpretation review (plain English)

### 20.1 What did this phase prove?

It produced a reproducible descriptive forensic snapshot of V1-arc
trade populations (H0, R3, R1a, R1b-narrow, R2) on existing local
15m trade-price-backtest artefacts. The snapshot covers MFE / MAE /
net_R distributions, descriptive cost decomposition, exit-reason
breakdown, threshold-touch rates, and bar-resolution ambiguity rates,
all under the Phase 4ap-locked methodology.

### 20.2 What did this phase not prove?

It did not prove that any V1-arc population can be improved, rescued,
promoted, or hybridized. It did not prove that any V1-arc verdict or
project lock should change. It did not prove that lower-timeframe
data acquisition is necessary or justified. It did not produce a new
strategy candidate.

### 20.3 Which original questions did it answer?

The Phase 4ap descriptive questions Q1–Q14, within the limits of the
existing 15m schema. Q9 (`adverse_before_favorable_flag`) was
recorded as `NOT_AUDITABLE_FROM_EXISTING_FIELDS`. Q7 (favorable-
before-stop) was recorded as a **proxy**.

### 20.4 Which original questions remain open?

Phase 4ap forbidden questions F1–F10 are explicitly out of scope and
remain unaddressed. Any deeper sequencing question (true intrabar
event order, intra-15m-bar stop-vs-target sequencing, exact mark-price
trigger time) is unaddressed because it would require lower-timeframe
data not authorized by Phase 4aq.

### 20.5 What does it mean for strategy research?

It provides descriptive context for understanding how V1-arc trades
unfolded relative to their MFE / MAE / cost / exit-reason profile.
It does not motivate strategy work. The cumulative six-failure-mode
rejection topology (R2 / F1 / D1-A / V2 / G1 / C1) remains preserved
verbatim, and Phase 4aq does not introduce any new candidate.

### 20.6 What does it mean for governance?

M0 admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8,
Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
Phase 4q, Phase 4v, Phase 4w, Phase 4ak adoption, and the Phase
4al / 4am / 4an / 4ao / 4ap chain are all preserved.

### 20.7 What is the clean next step?

Operator review of the Phase 4aq descriptive results. No successor
phase is authorized. Future operator-driven options include:

- remain paused (recommended);
- a separately authorized narrower docs-only interpretation memo
  focused on a specific Phase 4aq descriptive finding (only if
  separately authorized and only if the operator wants the
  descriptive findings consolidated);
- a separately authorized future Phase 4ar-class memo that summarizes
  Phase 4aq forensic evidence into a higher-level narrative without
  authorizing strategy work.

### 20.8 What should we not do yet?

- No V1-arc successor candidates (R3-prime / R1a-prime /
  R1b-narrow-prime / R2-prime / H0-prime).
- No exit-rule design from forensic numbers.
- No parameter optimization.
- No verdict revision.
- No project-lock revision.
- No 5m / 1m / aggTrades / tick / mark-price acquisition.
- No reopening of the 5m research thread.
- No paper / shadow / live-readiness / exchange-write.
- No production-key creation.
- No authenticated APIs / private endpoints / public-endpoint calls
  in code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.

## 21. Recommendation

Phase 4aq computation is complete and descriptive only. The recommended
state remains paused.

- **Primary recommendation:** remain paused.
- **Conditional secondary (NOT authorized by Phase 4aq):** a
  separately authorized narrower docs-only interpretation memo on a
  specific Phase 4aq descriptive finding.
- **Conditional tertiary (NOT authorized by Phase 4aq):** a separately
  authorized future memo (Phase 4ar-class) consolidating Phase 4aq
  forensic evidence at a higher level without authorizing strategy
  work.
- **NOT recommended:** authorizing 5m / 1m / aggTrades / tick / mark-
  price acquisition; designing exits from forensic numbers; promoting
  any retained-evidence population; reopening the 5m research thread.
- **FORBIDDEN:** verdict revision; lock revision; parameter
  optimization; strategy resurrection; M0 amendment from Phase 4aq
  reasoning; paper / shadow / live-readiness / deployment / exchange-
  write / production-key creation / authenticated APIs / private
  endpoints / public-endpoint calls in code / user stream / WebSocket /
  MCP / Graphify / `.mcp.json` / credentials.

Phase 4aq does not authorize any successor phase.

## 22. Verdict and lock preservation

### 22.1 Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m research thread** — operationally CLOSED (Phase 3t).
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

### 22.2 Project locks (preserved verbatim)

- **§11.6** = 8 bps slippage per side; round-trip = 16 bps. Any
  fee / slippage / funding decomposition reported by Phase 4aq is
  descriptive only and does not change the locked project-level cost
  reference or revise historical results.
- **§1.7.3** = 0.25% risk per trade; 2× leverage cap; one position
  max; mark-price stops where applicable.
- **Phase 3r §8** mark-price gap governance — preserved.
- **Phase 3v §8** stop-trigger-domain governance — preserved.
- **Phase 3w §6 / §7 / §8** break-even / EMA-slope / stagnation
  governance — preserved.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule —
  preserved (unused by Phase 4aq).
- **Phase 4k** V2 backtest-plan methodology — preserved.
- **Phase 4p** G1 strategy-spec memo — preserved.
- **Phase 4q** G1 backtest-plan methodology — preserved.
- **Phase 4v** C1 strategy-spec memo — preserved.
- **Phase 4w** C1 backtest-plan methodology — preserved.
- **Phase 4ak** M0 mechanism-admissibility gate adoption (twelve
  clauses + post-null cooldown rule + cooled-down families list +
  memo template) — preserved.
- **Phase 4al** refined no-rescue rule (§9.A forbidden / §9.B allowed
  under §9.C predeclaration); §13 future-phase boundary; §14 data-
  resolution hierarchy — preserved.
- **Phase 4am** §11.A audit findings (F-1, F-2, F-3, F-4) — preserved.
- **Phase 4an** historical-trade-population exit-path inventory —
  preserved.
- **Phase 4ao** exit-path methodology / artefact harmonization —
  preserved.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan (§6 population scope;
  §7 R3 baseline boundary; §8 Q1–Q14; §9 F1–F10; §10 directory
  allowlist; §11 required field schema; §12 metric definitions; §13
  timeframe rule; §14 cost rule; §15 stop-trigger-domain rule; §16
  output specification; §17 stop conditions) — preserved.

### 22.3 Boundaries explicitly not altered

- M0 governance is not amended.
- The Phase 4m 18-requirement fresh-hypothesis validity gate is not
  amended.
- The Phase 4t 10-dimension candidate scoring matrix is not amended.
- The Phase 4u opportunity-rate-vs-edge-rate distinction is not
  amended.
- The Phase 4w negative-baseline / PBO / DSR / CSCV methodology is
  not amended.
- The Phase 4z proposed framework remains a recommendation, not
  binding governance.

### 22.4 Phase 4 canonical / successor authorization status

- **Phase 4 canonical**: NOT authorized.
- **Phase 4ar / Phase 5 / any other successor phase**: NOT
  authorized.
- **Paper/shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in
  code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
  credentials**: NOT authorized.
- **5m / 1m / aggTrades / tick / mark-price 30m / 4h data
  acquisition**: NOT authorized.

## 23. End of Phase 4aq main memo

This memo, the Phase 4aq closeout
(`docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md`),
the standalone script
(`scripts/phase4aq_v1_arc_exit_path_forensics.py`), the local research
outputs (`data/research/phase4aq/`, gitignored / not committed), and
the narrow update to `docs/00-meta/current-project-state.md` together
constitute the complete Phase 4aq deliverable. Recommended state
remains paused.
