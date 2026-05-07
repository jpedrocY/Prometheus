# Phase 4ar — V1-Arc Exit-Path Forensic Interpretation Memo

## 1. Executive summary

Phase 4ar is a docs-only interpretation memo that consolidates the
already-merged Phase 4aq descriptive forensic evidence into
plain-English research and governance interpretation. Phase 4ar
performs **no computation**. It does not rerun
`scripts/phase4aq_v1_arc_exit_path_forensics.py`. It does not run any
historical strategy script. It does not run a backtest. It does not
acquire data. It does not modify data, manifests, existing trade
logs, source under `src/prometheus/`, tests, governance docs,
verdicts, locks, strategy specs, or thresholds. It does not commit
the local Phase 4aq output bundle under `data/research/phase4aq/`.

**Central interpretation:** Phase 4aq produced a complete descriptive
forensic snapshot of V1-arc trade populations (H0, R3, R1a,
R1b-narrow, R2) on 15m trade-price-backtest artefacts. The snapshot
documents that V1-arc trades **had favorable excursion** (non-trivial
MFE_R distributions) but **did not, on average, translate that
favorable excursion into positive realized net_R** in the primary
R-window default cell on either BTCUSDT or ETHUSDT. The snapshot also
documents structural limits of 15m descriptive forensics: intrabar
event ordering is `NOT_AUDITABLE_FROM_EXISTING_FIELDS`, and the
favorable-before-stop signal is a labelled proxy. Phase 4aq passed
all eleven Phase 4ap §17 stop conditions, performed zero of the ten
Phase 4ap §9 forbidden questions, and produced 11 local output
artefacts (not committed; reproducible from the committed standalone
script).

**What this means.** The Phase 4aq evidence is **descriptive
research evidence about how V1-arc trades unfolded under the locked
research methodology**, nothing more. It does not prove a recoverable
edge. It does not prove R3 can be improved by exit redesign. It does
not prove R2's failure was cost-only. It does not prove R1a or
R1b-narrow should be promoted. It does not prove H0 should be
revised. It does not prove that 5m, 1m, aggTrades, tick, or
mark-price 30m / 4h data acquisition is justified. It does not
authorize any successor phase.

**What Phase 4ar does not do.** Phase 4ar does not design exits.
Phase 4ar does not optimize R3. Phase 4ar does not create R3-prime,
R2-prime, R1a-prime, R1b-narrow-prime, H0-prime, or any successor
strategy candidate. Phase 4ar does not propose strategy changes.
Phase 4ar does not authorize Phase 4as or any successor phase. Phase
4ar does not authorize 5m / 1m / aggTrades / tick / mark-price 30m /
4h data acquisition. Phase 4ar does not reopen the 5m research
thread. Phase 4ar does not amend M0 governance. Phase 4ar does not
revise any retained verdict or project lock.

## 2. Scope and explicit non-scope

### 2.1 Scope

- Plain-English interpretation of the already-computed Phase 4aq
  descriptive forensic evidence.
- Per-population interpretation (H0, R3, R1a, R1b-narrow, R2).
- Per-evidence-theme interpretation (MFE_R / MAE_R; threshold-touch
  rates; giveback-from-MFE; favorable-before-stop proxy;
  adverse-before-favorable non-auditability; cost / fee / funding /
  estimated-slippage decomposition; bar-resolution ambiguity;
  R-window vs sensitivity / validation variant caution).
- Exit-architecture interpretation boundary.
- Lower-timeframe interpretation boundary.
- Governance interpretation.
- Forbidden-interpretation rejection list.
- Allowed-interpretation list.
- Recommendation derived from the interpretation result.
- Narrow update to `docs/00-meta/current-project-state.md`.
- Authoring this memo and the Phase 4ar closeout.

### 2.2 Explicit non-scope

- No new computation.
- No re-execution of `scripts/phase4aq_v1_arc_exit_path_forensics.py`.
- No re-execution of any historical strategy / research / data-
  acquisition script.
- No backtest.
- No data acquisition.
- No data file modification.
- No manifest creation or modification.
- No `research_eligible` flag flip.
- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification.
- No `.gitignore` modification.
- No commit of any `data/research/phase4aq/` output.
- No exit design.
- No R3 optimization.
- No R3-prime / R2-prime / R1a-prime / R1b-narrow-prime / H0-prime /
  any V1-arc successor strategy candidate.
- No V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime /
  G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow /
  C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy
  hybrid.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h / mark-price
  5m / mark-price 15m data work.
- No reopening of the 5m research thread.
- No verdict revision.
- No project-lock revision.
- No M0 governance amendment.
- No paper / shadow / live-readiness / deployment / exchange-write /
  production-key / authenticated APIs / private endpoints /
  public-endpoint calls in code / user stream / WebSocket / MCP /
  Graphify / `.mcp.json` / credentials.
- No successor phase authorization.

## 3. Repository verification summary

```
Pre-branch state (main):
  main         = bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b
  origin/main  = bcc4c8562a3870df11ffb50ec7ae4f940d56ab3b
  branch       = main (clean working tree;
                       .claude/scheduled_tasks.lock and data/research/
                       shown as untracked transient/local-only)

Required Phase 4aq files present on main:
  docs/00-meta/implementation-reports/2026-05-06_phase-4aq_v1-arc-exit-path-forensic-computation.md
  docs/00-meta/implementation-reports/2026-05-06_phase-4aq_closeout.md
  docs/00-meta/implementation-reports/2026-05-06_phase-4aq_merge-closeout.md
  scripts/phase4aq_v1_arc_exit_path_forensics.py

Branch created:
  phase-4ar/v1-arc-exit-path-forensic-interpretation
```

## 4. Methodology

Phase 4ar uses **static inspection of committed docs and committed
script only**.

- Docs-only: Phase 4ar adds two markdown files (this memo and the
  Phase 4ar closeout) plus a narrow update to
  `docs/00-meta/current-project-state.md`.
- No computation. The Phase 4aq evidence is taken as given from the
  Phase 4aq main memo, Phase 4aq closeout, and Phase 4aq
  merge-closeout.
- No script execution. `scripts/phase4aq_v1_arc_exit_path_forensics.py`
  is not run by Phase 4ar. No other historical script is run.
- No backtest.
- No data acquisition.
- No local Phase 4aq output is committed.
- Where the interpretation must reference a numeric Phase 4aq
  finding, it cites the value already documented in the Phase 4aq
  main memo on `main` rather than recomputing it.

Phase 4ar makes no governance, verdict, lock, source, test, data,
manifest, strategy, or threshold change.

## 5. Phase 4aq evidence baseline

The interpretation in Phase 4ar is derived from the following Phase
4aq result, recorded verbatim from the merged Phase 4aq main memo
and merge-closeout:

- **Computation status:** `SUCCESSFUL_COMPUTATION`.
- **Loaded artefacts:** 23 allowlisted V1-arc Phase-2 directories ×
  2 symbols (BTCUSDT, ETHUSDT) = **46 (directory, symbol) artefact
  pairs**, latest run per directory, Parquet preferred (Parquet
  selected in every loaded pair; JSON fallback not exercised).
- **Total trades loaded:** **973** (H0=154; R3=392; R1a=110;
  R1b-narrow=88; R2=229).
- **Schema validation:** **100% pass**. Every loaded ledger contained
  the full Phase 4ap §11 required-field set. Optional fields
  `quantity` and `notional_usdt` are present in every ledger. No
  fail-closed condition was triggered.
- **Phase 4ap §17 stop conditions:** **SC-1 through SC-11 all PASS**.
- **Phase 4ap §9 forbidden questions F1–F10:** **zero performed**;
  recorded as `NOT_PERFORMED` in
  `forbidden_interpretation_checklist.md`.
- **Phase 4ap §15 stop-trigger-domain inference:** every loaded
  V1-arc historical artefact tagged
  `stop_trigger_domain = trade_price_backtest`. `mixed_or_unknown`
  was never assigned.
- **Phase 4ap §13 timeframe rule:** 15m bar-extreme only. No 5m /
  1m / aggTrades / tick / mark-price 30m / 4h / mark-price 5m /
  mark-price 15m data was used or referenced.
- **Phase 4ap §14 cost rule:** §11.6 = 8 bps slippage per side
  preserved verbatim. `cost_in_R / fee_in_R / funding_in_R` are
  exact-from-fields. `estimated_slippage_in_R` is descriptive only.
  The identity `cost_in_R == fee_in_R + estimated_slippage_in_R +
  funding_in_R` is **not asserted**.
- **Outputs generated:** 11 artefacts under `data/research/phase4aq/`
  (`loaded_artifacts_manifest.csv`, `schema_validation_report.csv`,
  `population_summary.csv`, `mfe_mae_distribution_by_population.csv`,
  `realized_r_by_population.csv`, `cost_in_r_by_population.csv`,
  `exit_reason_breakdown.csv`,
  `excursion_threshold_touch_rates.csv`, `ambiguity_report.csv`,
  `forbidden_interpretation_checklist.md`,
  `v1_arc_forensic_report.md`).
- **Outputs committed:** **none**. The local outputs are reproducible
  from the committed standalone script + existing local V1-arc
  trade-log artefacts. Convention follows Phase 4ai / 4l / 4r / 4x
  precedent.

## 6. What Phase 4aq showed, in plain English

Phase 4aq's findings, interpreted **only at the descriptive level**,
say the following.

### 6.1 Negative mean net_R across V1-arc populations

In the **primary R-window default cell** (R-window, default cost
cell, default stop_domain_variant, default fill_variant), all five
included V1-arc populations had **negative `net_R_mean`** on both
BTCUSDT and ETHUSDT. The mean values cluster between approximately
−0.114R and −0.443R. This is the headline Phase 4aq descriptive
finding for the primary cell.

The plain-English reading is simple: under the locked Phase 4ap
methodology and on the existing committed V1-arc trade-log
artefacts, V1-arc trades in the primary cell had a negative average
realized return per unit of risk. **This is descriptive only.** It
does not prove a recoverable edge exists, and it does not prove no
recoverable edge can ever exist for any future ex-ante hypothesis
that satisfies M0 / no-rescue / cost-realism gates.

### 6.2 Favorable excursion did exist

MFE_R medians on the primary cell range approximately 0.366R to
1.036R, with several cells sitting above 0.8R. MAE_R medians range
approximately 0.514R to 0.844R. Many trades reached positive
unrealized excursion before exit. **Favorable excursion existed**.

### 6.3 Favorable excursion did NOT translate into positive realized net_R

Despite favorable MFE_R, the realized net_R distributions on the
primary cell are negative on average. The plain-English reading is
that the V1-arc trade populations, taken as a whole, did not capture
their own favorable excursion as net realized return. **This is a
descriptive observation, not a strategy verdict.** It does not
authorize redesigning exits. It does not authorize choosing a
take-profit multiple from observed MFE. It does not authorize any
parameter change. Phase 4ap §9 forbidden questions F1–F4 explicitly
forbid converting this observation into an exit-design rationale.

### 6.4 Threshold-touch rates exist but are not TP recommendations

`frac_reached_+1R` ranges approximately 0.18 to 0.57 across primary
cells. `frac_reached_+3R` ranges approximately 0.00 to 0.08. These
are descriptive frequencies of how often `mfe_r` crossed those
thresholds. **They are not take-profit-multiple recommendations**.
Phase 4ap §9 F3 explicitly forbids choosing the best take-profit
multiple from observed MFE distribution. Phase 4ar reaffirms that
forbidden status here.

### 6.5 Cost / fee / funding / estimated-slippage are descriptive context only

Phase 4aq emits exact-from-fields `cost_in_R`, `fee_in_R`, and
`funding_in_R`, plus a descriptive `estimated_slippage_in_R` derived
from `slippage_bucket` mapped to per-side bps and notional from
`notional_usdt` (or the `abs(quantity) * entry_fill_price`
fallback). The cost decomposition is **descriptive only**. The
identity `cost_in_R == fee_in_R + estimated_slippage_in_R +
funding_in_R` is **not asserted**. Any divergence is explanatory
context, not a finding requiring a fee, slippage, or funding-model
revision. **§11.6 = 8 bps slippage per side remains preserved
verbatim.** The locked project-level cost reference is unchanged by
Phase 4aq, and Phase 4ar makes no contrary recommendation.

### 6.6 Bar-resolution ambiguity is bounded but real at 15m

The Phase 4aq script flags `bars_in_trade == 0` as entry/exit
same-bar ambiguity. On the primary R-window default cell:

- **BTCUSDT cells** fall into the Phase 4al §14.C `2-10%` band.
- **ETHUSDT cells** fall into the Phase 4al §14.C `10-20%` band.

This is descriptive limitation, not an action item. Phase 4ar
documents the limitation and **does not authorize lower-timeframe
acquisition**. See §11 for the full lower-timeframe interpretation
boundary.

### 6.7 Existing fields cannot answer true event-order questions

`adverse_before_favorable_flag` is set to
`NOT_AUDITABLE_FROM_EXISTING_FIELDS` for every loaded trade. The
existing 15m schema records final MFE_R and MAE_R per trade but does
not preserve the intrabar order of those events.
`favorable_excursion_before_stop_proxy` is a **labelled proxy** for
STOP exits and is not asserted as sequencing evidence. Phase 4ap §13
explicitly forbids consulting lower-timeframe data in this phase, so
the result is recorded as `NOT_AUDITABLE` rather than inferred.

### 6.8 15m is sufficient for descriptive V1-arc interpretation, but not for intrabar sequencing certainty

Phase 4aq's 15m-only methodology is sufficient for the descriptive
questions in Phase 4ap §8 (Q1–Q14) under the limits documented in
Phase 4al §13, Phase 4ao §6, and Phase 4ap §13. It is not sufficient
for true intrabar sequencing. This is a **structural limit of the
existing fields**, not an artefact of insufficient effort.

## 7. What Phase 4aq did NOT show

Phase 4aq did not show, and Phase 4ar does not interpret it as
showing:

- **No proof of recoverable edge.** Negative mean net_R on the
  primary cell does not imply any future hypothesis can recover
  positive net_R, and favorable MFE_R does not imply that any
  take-profit, trailing stop, partial-exit, or break-even rule could
  recover net_R in this trade population.
- **No proof that R3 can be improved.** R3 forensic findings are
  descriptive context for the V1-arc baseline-of-record. They are
  not evidence for R3 optimization or R3-prime.
- **No proof that R2 can be rescued.** R2 cost-cell and net_R
  descriptive findings preserve R2's verdict (FAILED — §11.6) as
  retained-research evidence; they do not justify §11.6 relaxation
  or R2 rescue.
- **No proof that R1a or R1b-narrow should become leading.** Their
  retained-non-leading status is preserved; their descriptive
  findings do not authorize promotion or R1a-prime / R1b-narrow-
  prime.
- **No proof that H0 should be revised.** H0's framework-anchor
  status is preserved; its descriptive findings do not authorize
  H0-prime or framework-anchor revision.
- **No proof that any exit rule, TP, SL, trailing stop, break-even
  rule, time stop, or partial-exit system should be adopted.** Phase
  4ap §9 F1–F10 forbid extracting such rules from the descriptive
  evidence; Phase 4ar reaffirms that prohibition.
- **No proof that 5m or 1m escalation is justified.** Bar-resolution
  ambiguity in the `2-10%` and `10-20%` Phase 4al §14.C bands is
  documented as descriptive limitation, not as authorization for
  lower-timeframe data acquisition or the 5m research thread
  reopening.
- **No basis for verdict revision.** All retained verdicts remain
  preserved verbatim.
- **No basis for lock revision.** All project locks remain preserved
  verbatim.

## 8. Interpretation by population

Each subsection states the population's retained status, what the
Phase 4aq descriptive evidence says, what it does not say, allowed
interpretation, and forbidden interpretation. None of these
subsections proposes or interprets a successor candidate.

### 8.1 H0 — Framework Anchor

**Retained status:** H0 remains FRAMEWORK ANCHOR.

**What the Phase 4aq descriptive evidence says about H0.** H0 is
loaded from `phase-2e-baseline` and `phase-2g-wave1-h0-r` (latest
run per directory; Parquet preferred). The H0 R-window default cell
shows mean net_R approximately −0.443R on BTCUSDT and approximately
−0.422R on ETHUSDT, with MFE_R medians approximately 0.553R (BTC)
and 0.846R (ETH) and MAE_R medians approximately 0.562R (BTC) and
0.521R (ETH). H0 trades had favorable excursion but did not, on
average, capture it as positive realized net_R.

**What it does not say about H0.** It does not say H0 is "broken
under exits" or that H0 can be made profitable through a different
exit architecture. The H0 framework-anchor role is structural, not
performative. H0 trades exist as a baseline reference for V1-arc
research evidence, not as a candidate for promotion or rescue.

**Allowed interpretation.** H0 forensic findings are baseline
descriptive context for the V1-arc family. They support the
plain-English statement that V1-arc trade paths under the H0
configuration produced favorable excursion that was not captured as
realized net_R on the primary cell.

**Forbidden interpretation.** No H0-prime. No framework-anchor
revision. No claim that H0 should be retroactively reframed as a
candidate. No conversion of H0 forensic numbers into an entry rule,
exit rule, threshold, or parameter for any future hypothesis. No
extraction of H0 forensic findings as inputs to a fresh-hypothesis
discovery memo without first satisfying the Phase 4m 18-requirement
validity gate AND the Phase 4ak twelve-clause M0 gate AND the Phase
4al §9 refined no-rescue rule.

### 8.2 R3 — Baseline of Record

**Retained status:** R3 remains BASELINE-OF-RECORD.

**What the Phase 4aq descriptive evidence says about R3.** R3 is
loaded from `phase-2l-r3-r`, `phase-2l-r3-r-slip=LOW`,
`phase-2l-r3-r-slip=HIGH`, `phase-2l-r3-r-stop=TRADE_PRICE`, and
`phase-2l-r3-v` (latest run per directory; Parquet preferred). The
R3 R-window default cell shows mean net_R approximately −0.240R on
BTCUSDT and approximately −0.351R on ETHUSDT, with MFE_R medians
approximately 0.531R (BTC) and 0.849R (ETH) and MAE_R medians
approximately 0.564R (BTC) and 0.514R (ETH). R3 trades had favorable
excursion but did not, on average, capture it as positive realized
net_R on the primary cell.

**What it does not say about R3.** It does not say R3 can be
"fixed" by a different take-profit multiple, a different time-stop,
a trailing-stop policy, a break-even move, a partial-exit policy, or
a wider/narrower stop. It does not say R3 is approaching breakeven
under any cost cell. It does not say R3's threshold-touch rates
(BTC: `frac_+1R ≈ 0.273`, `frac_+2R ≈ 0.121`, `frac_+3R ≈ 0.030`;
ETH: `frac_+1R ≈ 0.424`, `frac_+2R ≈ 0.182`, `frac_+3R ≈ 0.030`)
imply an optimal take-profit selection.

**Allowed interpretation.** R3 forensic findings are descriptive
context for the V1-arc baseline-of-record. They support the
plain-English statement that R3 trades exhibited favorable excursion
that was, on average, given back before exit, and that R3's net_R
distribution remained negative on the primary cell.

**Forbidden interpretation.** No R3 optimization. No R3-prime. No
R3 rescue framing. No baseline-of-record revision. No conversion of
R3 forensic numbers into entry rules, exit rules, parameters,
thresholds, take-profit multiples, trailing-stop policies,
break-even rules, partial-exit policies, time-stop changes, or any
new V1-arc strategy candidate. **R3 is included in this report
strictly as descriptive context for the V1-arc family; its inclusion
does NOT make any forensic finding authorization for change.**

### 8.3 R1a — Retained, Non-Leading

**Retained status:** R1a remains RETAINED — NON-LEADING.

**What the Phase 4aq descriptive evidence says about R1a.** R1a is
loaded from `phase-2m-r1a-r1a_plus_r3-r`,
`phase-2m-r1a-r1a_plus_r3-r-slip=LOW`,
`phase-2m-r1a-r1a_plus_r3-r-slip=HIGH`,
`phase-2m-r1a-r1a_plus_r3-r-stop=TRADE_PRICE`, and
`phase-2m-r1a-r1a_plus_r3-v`. The R1a R-window default cell shows
mean net_R approximately −0.420R on BTCUSDT and approximately
−0.114R on ETHUSDT, with MFE_R medians approximately 0.366R (BTC)
and 1.036R (ETH) and MAE_R medians approximately 0.695R (BTC) and
0.514R (ETH).

**What it does not say about R1a.** It does not say R1a should be
promoted to leading status. It does not say the per-bar
volatility-percentile filter that distinguishes R1a from R3 was
"validated" by Phase 4aq. The per-bar filter is a research feature;
its retained-non-leading status is a research verdict, not a
performance claim that Phase 4aq could revisit.

**Allowed interpretation.** R1a forensic findings are descriptive
context for the V1-arc retained-non-leading evidence. They support
the plain-English statement that the R1a trade subset on the primary
cell had negative mean net_R and favorable MFE_R that was not
captured as realized net_R.

**Forbidden interpretation.** No R1a-prime. No promotion to leading
status. No per-bar filter "redesign". No conversion of R1a forensic
numbers into a new V1-arc candidate. No mining of R1a's threshold-
touch rates as TP candidates.

### 8.4 R1b-narrow — Retained, Non-Leading

**Retained status:** R1b-narrow remains RETAINED — NON-LEADING.

**What the Phase 4aq descriptive evidence says about R1b-narrow.**
R1b-narrow is loaded from `phase-2s-r1b-r1b_narrow-r`,
`phase-2s-r1b-r1b_narrow-r-slip=LOW`,
`phase-2s-r1b-r1b_narrow-r-slip=HIGH`,
`phase-2s-r1b-r1b_narrow-r-stop=TRADE_PRICE`, and
`phase-2s-r1b-r1b_narrow-v`. The R1b-narrow R-window default cell
shows mean net_R approximately −0.263R on BTCUSDT and approximately
−0.224R on ETHUSDT, with MFE_R medians approximately 0.570R (BTC)
and 0.831R (ETH) and MAE_R medians approximately 0.844R (BTC) and
0.640R (ETH). R1b-narrow's BTCUSDT primary cell has the smallest
trade count among V1-arc populations (n=10 in the primary cell,
n=12 ETH).

**What it does not say about R1b-narrow.** It does not say
R1b-narrow's bias-strength threshold was "validated" by Phase 4aq.
It does not say the small-n primary cell on BTCUSDT supports any
inference about edge. **Small-n descriptive results require extra
caution and are not promoted to leading status by Phase 4ar**.

**Allowed interpretation.** R1b-narrow forensic findings are
descriptive context for the V1-arc retained-non-leading evidence,
under the additional caveat that primary-cell sample sizes are
small.

**Forbidden interpretation.** No R1b-narrow-prime. No promotion to
leading status. No conversion of R1b-narrow forensic numbers into a
new V1-arc candidate. No bias-strength threshold "tuning" from
Phase 4aq numbers.

### 8.5 R2 — Failed (§11.6)

**Retained status:** R2 remains FAILED — §11.6.

**What the Phase 4aq descriptive evidence says about R2.** R2 is
loaded from `phase-2w-r2-r2_r3-r`, `phase-2w-r2-r2_r3-r-slip=LOW`,
`phase-2w-r2-r2_r3-r-slip=HIGH`,
`phase-2w-r2-r2_r3-r-stop=TRADE_PRICE`,
`phase-2w-r2-r2_r3-r-fill=limit-at-pullback`, and
`phase-2w-r2-r2_r3-v`. The R2 R-window default cell shows mean net_R
approximately −0.275R on BTCUSDT and approximately −0.432R on
ETHUSDT, with MFE_R medians approximately 0.772R (BTC) and 0.858R
(ETH) and MAE_R medians approximately 0.626R (BTC) and 0.587R (ETH).
R2 has variants for LOW / HIGH cost cells, a TRADE_PRICE
stop-domain variant, and a limit-at-pullback fill variant — these
are sensitivity / methodology variants and are reported in the Phase
4aq sensitivity section.

**What it does not say about R2.** It does not say R2's failure was
"only because of costs". It does not say R2 becomes positive at LOW
cost. **Even if a particular cell shifted with cost-cell choice, the
R2 verdict (FAILED — §11.6) is locked at §11.6 = 8 bps per side.**
Any cost-cell descriptive comparison is retained-research-evidence
context and does not authorize §11.6 relaxation.

**Allowed interpretation.** R2 forensic findings are descriptive
retained-research-evidence context. They support the plain-English
statement that the R2 pullback-retest entry rule's trade population
had negative mean net_R on the primary cell and that descriptive
cost-cell variation across LOW / default / HIGH does not change the
locked §11.6 cost reference.

**Forbidden interpretation.** No R2 rescue. No R2-prime. No §11.6
relaxation. No claim that R2 is "viable at LOW cost." No conversion
of R2's TRADE_PRICE stop-domain or limit-at-pullback fill variant
findings into a new V1-arc candidate.

## 9. Interpretation by evidence theme

### 9.1 MFE_R / MAE_R interpretation

MFE_R and MAE_R distributions describe the favorable and adverse
excursion experienced by V1-arc trades during their lifecycle, as
recorded by `TradeManagement._update_excursions` in
`src/prometheus/strategy/v1_breakout/management.py` from 15m bar
extremes. MFE_R medians approximately 0.366R–1.036R and MAE_R
medians approximately 0.514R–0.844R across primary cells indicate
that V1-arc trades **moved**, both favorably and adversely, before
exit. **The fact that MFE_R was non-trivial does not imply edge.**
The fact that MAE_R was non-trivial does not imply the structural
stop was poorly placed. These are descriptive distributions of
trade-path behaviour, not strategy verdicts.

### 9.2 Threshold-touch interpretation

`frac_reached_+1R / +2R / +3R` reports the population fraction of
trades whose `mfe_r` crossed each threshold. The fact that R3 ETH
hit +1R about 42% of the time and +2R about 18% of the time
**does not authorize a take-profit-multiple selection**. A higher
touch rate at +1R does not mean a +1R take-profit "would have
worked", because Phase 4ap §9 F3 explicitly forbids the implied
counterfactual. Phase 4ap §9 F1 also forbids the related
counterfactual of "which exit rule would have made R3 profitable."
Phase 4ar **reaffirms both prohibitions** as binding interpretation
constraints.

### 9.3 Giveback-from-MFE interpretation

`giveback_from_mfe = MFE_R - net_R` is reported descriptively, with
no clamping. Negative values, where they appear, are not forced to
zero. They indicate edge cases where realized net_R exceeded the
final MFE_R recorded in the trade log — possible explanations
include fill-vs-mark-extreme differences, cost / sign / schema edge
cases, or descriptive-reconstruction artefacts. **Phase 4ar treats
all such values as descriptive context, not as findings requiring
fee / slippage / fill-model revision.**

### 9.4 Favorable-before-stop proxy interpretation

`favorable_excursion_before_stop_proxy` is computed for STOP exits
only as `mfe_r > 0`. It is **proxy** because the existing 15m
schema does not preserve intrabar event order. The proxy says
nothing about whether the favorable excursion happened before or
after the adverse excursion that hit the stop. **It is not evidence
for any "stop hit before target" or "target reached before stop"
counterfactual at intrabar resolution.** Phase 4ar treats this
proxy as a descriptive-only summary statistic.

### 9.5 Adverse-before-favorable non-auditability

`adverse_before_favorable_flag = NOT_AUDITABLE_FROM_EXISTING_FIELDS`
on every loaded trade. This is a **structural limit of the existing
trade-log schema**: the schema records final MFE_R and MAE_R but
does not record the intrabar order of those events. Phase 4ap §12
and §13 explicitly forbid inferring the order from MFE / MAE alone
and forbid consulting lower-timeframe data in this phase. Phase 4ar
treats this `NOT_AUDITABLE` finding as a documented limitation, not
as an action item for lower-timeframe escalation.

### 9.6 Cost / fee / funding / estimated-slippage interpretation

- `cost_in_R = (gross_pnl - net_pnl) / realized_risk_usdt` —
  exact-from-fields.
- `fee_in_R = (entry_fee + exit_fee) / realized_risk_usdt` —
  exact-from-fields.
- `funding_in_R = funding_pnl / realized_risk_usdt` —
  exact-from-fields.
- `estimated_slippage_in_R` — descriptive only. Derived from
  `slippage_bucket` mapped to per-side bps {LOW: 1, MEDIUM: 4,
  HIGH: 8}, round-trip = 2 × per-side, with notional from
  `notional_usdt` (or `abs(quantity) * entry_fill_price`
  fallback).

The identity `cost_in_R == fee_in_R + estimated_slippage_in_R +
funding_in_R` is **not asserted**. Any divergence is descriptive
context, not an action item. **§11.6 = 8 bps slippage per side
remains preserved verbatim.** The locked project-level cost
reference is unchanged. R2's cost-cell sensitivity descriptive
findings are retained-research evidence and do not authorize §11.6
relaxation.

### 9.7 Bar-resolution ambiguity interpretation

`bars_in_trade == 0` flags entry/exit same-bar trades. The Phase 4al
§14.C descriptive bands are heuristic only and are not gates:

- `<2%` : 5m would likely be sufficient if separately authorized.
- `2-10%` : 5m would be usable with conservative stop-first
  assumptions.
- `10-20%` : 1m escalation may be considered if separately
  authorized.
- `>20%` : 5m would likely be too coarse if separately authorized.

Phase 4aq's primary cells fall in `2-10%` (BTCUSDT) and `10-20%`
(ETHUSDT). Phase 4ar treats this as a documented limitation only.
**Phase 4ar does NOT authorize 5m, 1m, aggTrades, tick, mark-price
30m, mark-price 4h, mark-price 5m, or mark-price 15m data
acquisition.** See §11 for the full lower-timeframe interpretation
boundary.

### 9.8 R-window vs sensitivity / validation variant caution

Phase 4aq separates R-window default-cell results from sensitivity
(LOW / HIGH cost cells, TRADE_PRICE stop-domain variant,
limit-at-pullback fill variant) and validation-window (V) cells.
Sensitivity and V cells are descriptive context only and **must not
be pooled with primary-cell results**. Promotion of any V-window or
sensitivity finding to "headline status" is forbidden. Phase 4ar
preserves this separation as binding interpretation discipline.

## 10. Exit-architecture interpretation boundary

Phase 4aq enables the following **descriptive** statement, recorded
here for the record:

> Exit architecture has now been **descriptively audited** for
> V1-arc populations on 15m trade-price-backtest artefacts within
> the Phase 4ap-locked methodology.

Phase 4aq does **NOT** support any of the following:

- exit design;
- TP / SL selection;
- inference of optimal winner management;
- justification of trailing stops, break-even moves, partial exits,
  or time-stop changes;
- rescue of failed entries.

A bad exit architecture can destroy a usable signal, but Phase 4aq
**did not prove a usable signal exists**. The cumulative
six-failure-mode rejection topology (R2 / F1 / D1-A / V2 / G1 / C1)
remains preserved verbatim, and Phase 4aq does not introduce a new
candidate. Phase 4ar reaffirms this boundary explicitly.

## 11. Lower-timeframe interpretation boundary

Phase 4aq documents bar-resolution ambiguity in two bands on the
primary R-window default cell:

- BTCUSDT cells: `2-10%` band.
- ETHUSDT cells: `10-20%` band.

Phase 4ar treats these as **documented limitations**, not as action
items.

This documentation does **NOT**:

- authorize 5m / 1m / aggTrades / tick / mark-price 30m / 4h /
  mark-price 5m / mark-price 15m data acquisition;
- reopen the 5m research thread (Phase 3t closure preserved);
- imply that lower-timeframe escalation is necessary;
- imply that lower-timeframe escalation would alter any retained
  verdict;
- imply that lower-timeframe escalation would alter §11.6, §1.7.3,
  Phase 3v §8, or any other lock.

Any future lower-timeframe measurement-layer discussion would
require **separate operator authorization** and would have to
satisfy Phase 4al §14 (data-resolution hierarchy with conservative
stop-first assumptions where ambiguity falls in the `2-10%` band)
and Phase 4ao §13.3 (conservative criterion for forensic-
measurement-layer use of existing 5m data only when an ambiguity
threshold is exposed). Phase 4ar does not start any such
discussion; it documents the boundary and stops.

## 12. Governance interpretation

### 12.1 Phase 4aq is descriptive evidence only

Phase 4aq's outputs are **descriptive evidence** about V1-arc trade
behaviour under the locked methodology. They are not strategy
evidence, not promotion evidence, not rescue evidence, and not
authorization evidence. Phase 4ar preserves this status.

### 12.2 M0 remains binding prospectively

Phase 4ak adopted the twelve-clause M0 mechanism-admissibility gate
and the post-null cooldown rule as binding prospective governance.
Phase 4aq did not amend M0. Phase 4ar does not amend M0. Any future
admissibility decision must satisfy the M0 gate and the post-null
cooldown rule.

### 12.3 Post-null cooldown remains unchanged

Phase 4z's post-null cooldown rule (now binding under Phase 4ak)
applies to feasibility families that returned `NOT_SUPPORTED`. No
cooled-down family is reopened by Phase 4aq or Phase 4ar.

### 12.4 §11.6 remains locked

§11.6 = 8 bps slippage per side; round-trip = 16 bps. Phase 4aq's
descriptive cost decomposition does not modify this lock. Phase 4ar
makes no recommendation that would.

### 12.5 §1.7.3 remains locked

§1.7.3 project-level locks remain: 0.25% risk per trade; 2× leverage
cap; one position max; mark-price stops where applicable.

### 12.6 Phase 3t 5m closure remains binding

The 5m research thread is operationally CLOSED per Phase 3t. Phase
4aq did not reopen it. Phase 4ar does not reopen it. No 5m strategy
work, no 5m signal, no 5m-as-rule-input, no Q1–Q7 rule extraction.
Existing 5m data may, at most, be referenced as a forensic
measurement layer under the conservative §13.3 criterion **and only
if separately authorized in a future phase**. Phase 4ar does not
start that authorization.

### 12.7 Phase 3v stop-trigger-domain governance remains binding

`stop_trigger_domain` ∈ `{trade_price_backtest, mark_price_runtime,
mark_price_backtest_candidate}`. `mixed_or_unknown` fails closed at
any decision boundary. Phase 4aq inferred V1-arc historical
artefacts as `trade_price_backtest`. Phase 4ar preserves this.

### 12.8 Retained verdict ledger remains unchanged

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow
RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A
MECHANISM PASS / FRAMEWORK FAIL; 5m thread CLOSED; V2 / G1 / C1
HARD REJECT — terminal. All preserved verbatim.

## 13. Forbidden interpretations

Phase 4ar **explicitly rejects** each of the following statements
about Phase 4aq evidence. None of them is a legitimate interpretation
of Phase 4aq descriptive findings.

- **REJECTED:** "R3 would work with better exits."
  Phase 4aq did not prove a usable signal in R3, did not test exit
  alternatives, and did not authorize counterfactual exit-design
  reasoning. Phase 4ap §9 F1 forbids "which exit rule would have
  made R3 profitable."

- **REJECTED:** "R3 should be optimized."
  Phase 4aq is descriptive, not optimization evidence. R3 remains
  BASELINE-OF-RECORD descriptive context only. Phase 4ap §9 F4
  forbids parameter tuning from forensic findings.

- **REJECTED:** "R2 failed only because of costs."
  Phase 4aq's cost-cell descriptive findings do not justify §11.6
  relaxation or R2 rescue. R2 verdict (FAILED — §11.6) is locked at
  §11.6 = 8 bps per side. Phase 4ap §9 F5 forbids "can R2 be
  rescued if costs are lower."

- **REJECTED:** "R1a / R1b-narrow should be promoted."
  R1a and R1b-narrow remain RETAINED — NON-LEADING. Their primary-
  cell descriptive findings do not authorize promotion. Phase 4ap
  §9 F6 forbids "can R1a / R1b-narrow become leading."

- **REJECTED:** "+2R or +3R touch rates imply TP selection."
  Threshold-touch rates are descriptive frequencies, not take-
  profit-multiple recommendations. Phase 4ap §9 F3 forbids
  "choose the best take-profit multiple from observed MFE
  distribution."

- **REJECTED:** "5m / 1m is now required."
  Bar-resolution ambiguity in `2-10%` (BTC) and `10-20%` (ETH) bands
  is documented as a limitation. It does not authorize lower-
  timeframe acquisition or reopen the 5m research thread.

- **REJECTED:** "V1-arc can be rescued."
  No V1-arc rescue is supported by the descriptive evidence. The
  cumulative rejection topology and the Phase 4ak post-null cooldown
  rule remain binding. Phase 4ap §9 F8 forbids cross-strategy
  hybridization. Phase 4ap §9 F10 forbids converting any descriptive
  finding into a strategy candidate.

- **REJECTED:** "A new V1-arc exit system should be designed."
  Phase 4aq did not authorize exit design, did not select TP / SL,
  did not infer optimal winner management, and did not justify
  trailing stops, break-even moves, partial exits, or time-stop
  changes. Phase 4ar reaffirms this boundary.

- **REJECTED:** "Verdicts should be revised."
  No retained verdict is revised by Phase 4aq or Phase 4ar.

- **REJECTED:** "Locks should be revised."
  No project lock is revised by Phase 4aq or Phase 4ar.

## 14. Allowed interpretations

Phase 4ar **allows** each of the following statements as legitimate
interpretation of Phase 4aq descriptive findings.

- **ALLOWED:** Phase 4aq improves descriptive understanding of
  V1-arc trade paths under the locked Phase 4ap methodology.
- **ALLOWED:** Phase 4aq documents that favorable excursion existed
  in V1-arc trade populations but was not, on average, sufficient
  to overcome realized net_R behaviour on the primary R-window
  default cell.
- **ALLOWED:** Phase 4aq documents structural limitations of
  intrabar sequencing under the existing 15m schema, including the
  `NOT_AUDITABLE_FROM_EXISTING_FIELDS` adverse-before-favorable
  finding and the proxy-only favorable-before-stop flag.
- **ALLOWED:** Phase 4aq supports governance-safe archival
  interpretation of the V1-arc descriptive forensic snapshot.
- **ALLOWED:** Phase 4aq can inform future meta-learning **about
  research process**, not about strategy design, unless a future
  phase is separately authorized and passes the M0 / no-rescue /
  cost-realism gates.
- **ALLOWED:** Phase 4aq's stop-trigger-domain inference for V1-arc
  historical artefacts (`trade_price_backtest`) is preserved as
  documented research evidence.
- **ALLOWED:** Phase 4aq's bar-resolution ambiguity bands are
  documented as a structural-limit observation, not as
  authorization for lower-timeframe acquisition.

## 15. Recommendation

The Phase 4ar interpretation result supports the following
recommendation hierarchy. None of these is started or authorized by
Phase 4ar.

- **Primary recommendation:** **remain paused**. The Phase 4aq
  descriptive evidence and the Phase 4ar interpretation are now
  part of the project record. No further action is required, and
  no further action is recommended by default.
- **Conditional secondary (NOT authorized by Phase 4ar):** a
  narrower docs-only archival synthesis memo that reorganises the
  combined Phase 4an / 4ao / 4ap / 4aq / 4ar narrative into a
  single archival-friendly summary. This would be docs-only and
  would not authorize computation, strategy work, or governance
  amendment.
- **Conditional tertiary (NOT authorized by Phase 4ar):** a future
  separately authorized governance memo only if a precise
  governance question arises (for example, an explicit operator
  decision about whether to add `data/research/` to `.gitignore`
  formally, or an explicit operator decision about mark-price
  stop-domain forensic admissibility under Phase 3v §8 + Phase 3r
  §8). Any such memo would be docs-only, would not authorize
  computation, and would not amend M0 by default.
- **NOT recommended:** computation by default; 5m / 1m escalation by
  default; exit design; strategy work; verdict / lock revision; M0
  amendment; reopening the 5m research thread; paper / shadow /
  live-readiness / deployment / exchange-write / production-key
  creation / authenticated APIs / private endpoints / public-
  endpoint calls in code / user stream / WebSocket / MCP / Graphify
  / `.mcp.json` / credentials.

If any successor is mentioned above, it is framed as "operator may
later authorize," **not** as started or authorized.

## 16. Implementation / governance review

### 16.1 What changed?

- New file:
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_v1-arc-exit-path-forensic-interpretation.md`
  (this memo).
- New file:
  `docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`
  (Phase 4ar closeout).
- Narrow update to `docs/00-meta/current-project-state.md` adding
  the Phase 4ar narrative paragraph and updating the "Current
  phase:" block (prior Phase 4aq block preserved as historical
  context).

### 16.2 What did not change?

- No `src/prometheus/` modification.
- No test modification.
- No existing-script modification (no
  `scripts/phase4aq_v1_arc_exit_path_forensics.py` execution; no
  modification to that script or any other historical script).
- No data file modification (no `data/raw/`, `data/normalized/`,
  `data/derived/` change).
- No manifest modification (no `data/manifests/` change; no
  `research_eligible` flag flip).
- No `.gitignore` modification.
- No commit of `data/research/phase4aq/` outputs.
- No Phase 3r §8 / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 4j
  §11 / Phase 4k / Phase 4p / Phase 4q / Phase 4v / Phase 4w /
  Phase 4ak / Phase 4al / 4am / 4an / 4ao / 4ap / 4aq governance
  document modification.
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price 30m / 4h / mark-price
  5m / mark-price 15m data work.
- No reopening of the 5m research thread.
- No backtest run.
- No historical strategy script executed.
- No data acquisition.

### 16.3 Were any locks, verdicts, or safety boundaries affected?

No. The retained verdict ledger and project locks are preserved
verbatim. M0 governance is unchanged. The 5m closure is preserved.
The cost lock is preserved. The position / leverage / risk locks
are preserved. The stop-trigger-domain governance is preserved.

### 16.4 Were any historical scripts, source files, existing data, manifests, or tests modified?

No. Phase 4ar is docs-only.

### 16.5 Is the phase mergeable as docs-only?

Yes. Phase 4ar adds two markdown files under
`docs/00-meta/implementation-reports/` plus a narrow update to
`docs/00-meta/current-project-state.md`. The phase is mergeable as
docs-only.

## 17. Research interpretation review (plain English)

### 17.1 What did this phase prove?

Phase 4ar consolidated the Phase 4aq descriptive forensic evidence
into plain-English research and governance interpretation. It
recorded what the Phase 4aq evidence supports (descriptive V1-arc
trade-path observations, structural-limit observations about
intrabar sequencing under the 15m schema, descriptive cost
decomposition) and what it does not support (recoverable edge,
exit redesign, parameter optimization, R3 / R2 / R1a / R1b-narrow /
H0 promotion or rescue, lower-timeframe escalation, verdict / lock
revision, M0 amendment, successor-phase authorization).

### 17.2 What did this phase not prove?

Phase 4ar did not prove that any V1-arc population can be improved,
rescued, promoted, or hybridized. It did not prove that any V1-arc
verdict or project lock should change. It did not prove that
lower-timeframe data acquisition is necessary or justified. It did
not produce a new strategy candidate. It did not perform any
computation; the interpretation rests on the merged Phase 4aq
evidence.

### 17.3 Which original questions did it answer?

The originally posed Phase 4ar question — *"What does the Phase 4aq
V1-arc descriptive forensic evidence mean, and what does it not
mean, without turning it into exit design, optimization, rescue,
verdict revision, or lock revision?"* — is answered across §6 (what
Phase 4aq showed), §7 (what Phase 4aq did NOT show), §8 (per-
population interpretation), §9 (per-evidence-theme interpretation),
§10 (exit-architecture boundary), §11 (lower-timeframe boundary),
§12 (governance boundary), §13 (forbidden interpretations), and §14
(allowed interpretations).

### 17.4 Which original questions remain open?

Phase 4ap forbidden questions F1–F10 remain explicitly out of scope
and unanswered. Any deeper sequencing question (true intrabar event
order, intra-15m-bar stop-vs-target sequencing, exact mark-price
trigger time) remains structurally unauditable from the existing
15m fields. The question of whether any future ex-ante hypothesis
could clear M0 admissibility and the post-null cooldown rule remains
operator-driven and is not advanced by Phase 4ar.

### 17.5 What does it mean for strategy research?

Phase 4ar's interpretation supports the conclusion that the V1-arc
descriptive forensic snapshot is **complete, internally consistent,
and bounded by the locked methodology**, and that no aspect of it
authorizes V1-arc rescue, promotion, or successor-candidate
creation. The cumulative six-failure-mode rejection topology
(R2 / F1 / D1-A / V2 / G1 / C1) remains preserved. The Phase 4m
18-requirement validity gate, the Phase 4t 10-dimension scoring
matrix, the Phase 4ak twelve-clause M0 gate, the Phase 4ak post-
null cooldown rule, and the Phase 4al refined no-rescue rule remain
the binding admissibility framework for any future hypothesis.

### 17.6 What does it mean for governance?

Phase 4ar reaffirms the binding prospective governance: M0
admissibility, post-null cooldown, §11.6, §1.7.3, Phase 3r §8, Phase
3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p,
Phase 4q, Phase 4v, Phase 4w, Phase 4ak, Phase 4al refined no-rescue
rule + §13 boundary + §14 hierarchy, Phase 4am §11.A audit findings,
Phase 4an inventory, Phase 4ao harmonization, Phase 4ap forensic
plan, and Phase 4aq computation result preserved as descriptive
evidence only. None is amended.

### 17.7 What is the clean next step?

Operator review of the Phase 4ar interpretation. **No successor
phase is authorized.** The clean next step is operator-driven only.
Acceptable separately-authorized future options include remain
paused (recommended), a narrower docs-only archival synthesis memo,
or a future governance memo on a precise governance question. None
is started or authorized by Phase 4ar.

### 17.8 What should we not do yet?

- No V1-arc successor candidates.
- No exit-rule design from forensic numbers.
- No parameter optimization.
- No verdict / lock revision.
- No M0 amendment.
- No 5m / 1m / aggTrades / tick / mark-price acquisition.
- No reopening of the 5m research thread.
- No paper / shadow / live-readiness / deployment / exchange-write
  / production-key creation.
- No authenticated APIs / private endpoints / public-endpoint calls
  in code / user stream / WebSocket / MCP / Graphify / `.mcp.json` /
  credentials.

## 18. Verdict, lock, and no-rescue preservation

### 18.1 Retained verdict ledger (preserved verbatim)

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

### 18.2 Project locks (preserved verbatim)

- **M0 governance** remains binding prospectively only.
- No retained verdict is revised.
- No project lock is changed.
- **§11.6** HIGH cost = 8 bps slippage per side; round-trip = 16 bps.
  Any fee / slippage / funding decomposition reported by Phase 4aq
  remains descriptive only and must not change the locked project-
  level cost reference or revise historical results.
- **§1.7.3** = 0.25% risk per trade; 2× leverage cap; one position
  max; mark-price stops where applicable.
- **Phase 3r §8** mark-price gap governance — preserved.
- **Phase 3v §8** stop-trigger-domain governance — preserved.
- **Phase 3w §6 / §7 / §8** break-even / EMA-slope / stagnation
  governance — preserved.
- **Phase 4j §11** metrics OI-subset partial-eligibility rule —
  preserved (unused by Phase 4aq / 4ar).
- **Phase 4k** V2 backtest-plan methodology — preserved.
- **Phase 4p** G1 strategy-spec memo — preserved.
- **Phase 4q** G1 backtest-plan methodology — preserved.
- **Phase 4v** C1 strategy-spec memo — preserved.
- **Phase 4w** C1 backtest-plan methodology — preserved.
- **Phase 4ak** M0 mechanism-admissibility gate adoption (twelve
  clauses + post-null cooldown + cooled-down families list + memo
  template) — preserved.
- **Phase 4al** refined no-rescue rule (§9.A forbidden / §9.B allowed
  under §9.C predeclaration) + §13 future-phase boundary + §14
  data-resolution hierarchy — preserved.
- **Phase 4am** §11.A audit findings (F-1 / F-2 / F-3 / F-4) —
  preserved.
- **Phase 4an** historical-trade-population exit-path inventory —
  preserved.
- **Phase 4ao** exit-path methodology / artefact harmonization —
  preserved.
- **Phase 4ap** V1-Arc Exit-Path Forensic Plan — preserved.
- **Phase 4aq** computation result preserved as descriptive evidence
  only.

### 18.3 No-rescue constraints

- No V1-arc rescue (R3-prime / R2-prime / R1a-prime / R1b-narrow-
  prime / H0-prime / V2-prime / V2-narrow / V2-relaxed / V2 hybrid
  / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime /
  C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-
  strategy hybrid).
- No 5m research thread reopening.
- No M0 amendment from Phase 4ar reasoning.
- No verdict revision from Phase 4ar reasoning.
- No lock revision from Phase 4ar reasoning.

### 18.4 Phase 4 canonical / successor authorization status

- **Phase 4 canonical:** NOT authorized.
- **Phase 4as / Phase 5 / any other successor phase:** NOT
  authorized.
- **Paper / shadow, live-readiness, deployment, production keys,
  authenticated APIs, private endpoints, public-endpoint calls in
  code, user stream, WebSocket, MCP, Graphify, `.mcp.json`,
  credentials:** NOT authorized.
- **5m / 1m / aggTrades / tick / mark-price 30m / 4h / mark-price
  5m / mark-price 15m data acquisition:** NOT authorized.

## 19. End of Phase 4ar memo

This memo, the Phase 4ar closeout
(`docs/00-meta/implementation-reports/2026-05-06_phase-4ar_closeout.md`),
and the narrow update to `docs/00-meta/current-project-state.md`
together constitute the complete Phase 4ar deliverable. **Recommended
state remains paused.** **No successor phase is authorized.**
