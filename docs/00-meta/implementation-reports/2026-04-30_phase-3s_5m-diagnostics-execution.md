# Phase 3s — 5m Diagnostics Execution

## Summary

Phase 3s (diagnostics-and-reporting) executed the predeclared Phase 3o / Phase 3p Q1–Q7 diagnostic question set exactly once, on the v002-locked retained-evidence trade populations (R3, R2, F1, D1-A; R-window MEDIUM-slip canonical runs), using the Phase 3q v001-of-5m supplemental datasets, and applying the Phase 3r §8 Q6 invalid-window exclusion rule. **All seven predeclared questions were answered. The Phase 3p §8 outcome-interpretation rules — predeclared and immutable since the Phase 3p commit on `main` — were applied verbatim to classify each question.**

**Q1–Q7 verdict summary:**

| Q | Verdict | Headline finding |
|---|---|---|
| **Q1** — IAE/IFE first 5–15 min after entry | **Informative** | Across all four candidates × both symbols, IAE > IFE in 7 of 8 cells (mean IAE_1 > mean IFE_1). F1 most adverse: ~0.5 R consumed within first 5 min. R3, R2, D1A also show adverse path bias. |
| **Q2** — Wick-stop vs sustained-stop | **Informative** | Clean cross-candidate differential: V1-family (R3, R2) shows **wick-dominated** stop pathology (R3 BTC 83.3%, R3 ETH 63.6%, R2 BTC 100%, R2 ETH 57.1%); F1 + D1-A show **sustained-dominated** stop pathology (F1 BTC 34.7%, F1 ETH 34.4%, D1-A BTC 32.4%, D1-A ETH 26.9%). |
| **Q3** — Intrabar +1R / +2R target touches before adverse exit | **Informative for +1R**; ambiguous for +2R | +1R intrabar-touch fraction in adverse-exit trades: R3 BTC 27.3% / ETH 45.5%; R2 BTC 47.8% / ETH 47.4%; F1 BTC 23.6% / ETH 24.0% (both just below 25% threshold); D1-A BTC 35.6% / ETH 34.6%. Six of eight cells ≥ 25%. **Critical: Phase 3p §8.3 explicitly forbids using this finding as rule revision; Phase 3o §6.3 forbids the maximize-R rule form.** |
| **Q4** — D1-A funding-extreme decay 5/10/15/30/60 min | **Non-informative** | No monotone decay shape. SEM bands wider than displacement magnitudes (BTC mean=-0.041R / sem=0.039R at 5min — ratio ~1.05; ETH mean=-0.088R / sem=0.060R at 5min — ratio ~0.68). Phase 3p §8.4 noise-floor predicate fails on both symbols. |
| **Q5** — Next-15m-open fill realism | **Non-informative** | No cell has |mean signed slippage| > 8 bps. F1 (-3.7 / -4.2 bps signed) and D1-A (-2.9 / -2.9 bps signed) tilt slightly toward 15m assumption being unfavorable, but magnitudes well below threshold. Unsigned means show high cross-trade variance. **Consistent with Phase 3l "B — conservative but defensible" finding at 5m granularity.** |
| **Q6** — Mark-vs-trade stop-trigger sensitivity (§8 exclusion rule) | **Informative for D1-A only**; non-informative for R3 / R2 / F1 | D1-A: BTC mean +1.25 5m-bars (mark lags trade); ETH mean +1.78 5m-bars; both exceed 1-bar threshold with consistent sign — D1-A's mark-stops trigger systematically later than trade-stops would. R3 / R2 / F1: ≤ 0.4 bars mean lag, 89–100% simultaneous-trigger fraction. **Zero trades excluded by Phase 3r §8** across all populations because retained-evidence trade lifetimes (≤ 8 hours) are too short to straddle the four ≥ 30-min mark-price gap windows. |
| **Q7** — Meta-classification | **Informative** | 4 of 6 Q1–Q6 classifications are informative (Q1, Q2, Q3, Q6). Phase 3p §8.7 threshold (≥ 3 informative) met. The diagnostic-phase as a whole produced a coherent body of informative findings, not just isolated signals. |

**Importantly: an informative Q7 result *cannot* by itself license verdict revision, parameter change, strategy rescue, or live-readiness implication.** Phase 3p §8 critical reminders, Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, and Phase 3r §8 Q6 exclusion rule all remain binding. **R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks all preserved verbatim.**

Phase 3s recommends **remain paused** as primary, with a **single optional conditional secondary alternative**: a docs-only post-Phase-3s consolidation memo that integrates the Q1 / Q2 / Q6 mechanism-level findings into the project's framework-discipline knowledge base. Phase 3s explicitly does NOT recommend implementation, strategy rescue, parameter changes, threshold revision, project-lock revision, ML feasibility, regime-first formal spec, paper/shadow planning, Phase 4, live-readiness, deployment, or any successor-strategy proposal (D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid).

## Authority and boundary

**Authority:** Phase 3o §5 (Q1–Q7 question set), §6 (forbidden question forms), §7 (diagnostic-term definitions), §10 (analysis boundary); Phase 3p §4–§8 (data requirements, dataset versioning, manifest specification, per-question outputs, outcome-interpretation rules), §10 (decision menu); Phase 3q acquisition + integrity-validation (`docs/00-meta/implementation-reports/2026-04-30_phase-3q_5m-data-acquisition-and-integrity-validation.md`); Phase 3r §8 Q6 invalid-window exclusion rule (`docs/00-meta/implementation-reports/2026-04-30_phase-3r_mark-price-gap-governance-memo.md`). All preserved verbatim.

**Boundary preserved:** Phase 3s is diagnostics-and-reporting only. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. v002 datasets and manifests untouched. Phase 3q v001-of-5m manifests untouched (mark-price still `research_eligible: false`). No backtest run. No retained-evidence trade population regenerated. No `data/` artefact modified. No 5m strategy / hybrid / variant created. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work.

## Starting git state

```text
branch:           phase-3s/5m-diagnostics-execution
created from:     main @ f20c0edb9a80b4bfdd0863687416939427ad1184
working tree:     clean
v002 manifests:   8 files, untouched
v002 partitions:  data/raw/binance_usdm/{klines,markPriceKlines}/symbol=*/interval=15m/...  untouched
                  data/normalized/{klines,mark_price_klines}/symbol=*/interval=15m/...      untouched
v002 trade pops:  data/derived/backtests/* untouched
phase-3q 5m:      data/raw/binance_usdm/{klines,markPriceKlines}/symbol=*/interval=5m/...   untouched
                  data/normalized/{klines,mark_price_klines}/symbol=*/interval=5m/...       untouched
phase-3q manif.:  4 files, untouched (mark-price `research_eligible: false` preserved)
```

## Input datasets and manifests

### 5m datasets (Phase 3q v001-of-5m, used read-only)

| Dataset version | Bars | `research_eligible` | Used by |
|---|---|---|---|
| `binance_usdm_btcusdt_5m__v001` | 446 688 | true | Q1, Q2, Q3, Q4 (BTC), Q5, Q6 (trade-side) |
| `binance_usdm_ethusdt_5m__v001` | 446 688 | true | Q1, Q2, Q3, Q4 (ETH), Q5, Q6 (trade-side) |
| `binance_usdm_btcusdt_markprice_5m__v001` | 445 819 | **false** | Q6 (mark-side, with §8 exclusion) |
| `binance_usdm_ethusdt_markprice_5m__v001` | 446 106 | **false** | Q6 (mark-side, with §8 exclusion) |

### v002 funding-event tables (used for Q4 D1-A funding events)

D1-A trade-log column `funding_event_id_at_signal` maps trades to v002 funding events. Q4 was implemented by sampling the 5m sub-bar at `entry_fill_time + N×60s` for N ∈ {5, 10, 15, 30, 60}, which is operationally equivalent for D1-A entries (which align to the 15m bar following the funding-settlement timestamp).

### v002 retained-evidence trade populations (read-only)

Canonical run per candidate × symbol selected as the latest dated run under the relevant backtest directory:

| Candidate | Run path | BTC trades | ETH trades |
|---|---|---|---|
| **R3** (V1 breakout, baseline-of-record) | `phase-2l-r3-r/2026-04-29T03-11-42Z/{BTCUSDT,ETHUSDT}/trade_log.parquet` | 33 | 33 |
| **R2** (V1 breakout pullback-retest) | `phase-2w-r2-r2_r3-r/2026-04-27T11-25-07Z/{BTCUSDT,ETHUSDT}/trade_log.parquet` | 23 | 19 |
| **F1** (mean-reversion) | `phase-3d-f1-window=r-slip=medium/2026-04-29T03-12-14Z/{BTCUSDT,ETHUSDT}/trade_log.parquet` | 4 720 | 4 826 |
| **D1-A** (funding-aware contrarian) | `phase-3j-d1a-window=r-slip=medium/2026-04-29T03-22-26Z/{BTCUSDT,ETHUSDT}/trade_log.parquet` | 198 | 179 |

R-window MEDIUM-slip canonical runs were chosen because (a) MEDIUM is the canonical Phase 2y reference slip used for primary verdicts, (b) R-window is the predeclared evaluation window for Phase 2f Gate 1 and all retained-evidence verdicts, (c) the 5m-resolution path observations Q1 / Q2 / Q3 / Q4 / Q6 depend on the trade trajectory, not the slip-adjusted fill price (slip only affects entry/exit fill, not the post-entry market path).

## Retained-evidence trade populations used

```text
R3:    66 trades total  (33 BTC + 33 ETH)
R2:    42 trades total  (23 BTC + 19 ETH)
F1:    9 546 trades total  (4 720 BTC + 4 826 ETH)
D1-A:  377 trades total  (198 BTC + 179 ETH)
TOTAL: 10 031 trades
```

Across all populations, 10 031 trades were augmented with 5m-resolution path attributes (Q1 / Q2 / Q3 / Q4 (D1-A only) / Q5 / Q6). No trade population was regenerated. No backtest was run.

## Q6 invalid-window rule implementation

### Q6 analysis-window predeclaration (Phase 3r §8 / Phase 3p §6.1)

The Q6 analysis window for each STOP-exited trade is predeclared as the closed interval `[entry_ot, exit_ot]` where `entry_ot = bar_open_time_for(entry_fill_time_ms)` and `exit_ot = bar_open_time_for(exit_fill_time_ms)` — i.e., the 5m bars from entry through exit, inclusive. This is the smallest interval that contains all 5m sub-bars relevant to comparing mark-price stop-trigger and trade-price stop-trigger timing.

### Phase 3r §8 exclusion test

For each STOP-exited trade, the Phase 3s implementation:
1. Reads the four mark-price 5m invalid-window pairs from each symbol's manifest `invalid_windows` field.
2. Tests whether `[entry_ot, exit_ot]` intersects any invalid window using the predicate `not (window_end < gap_start or window_start > gap_end)`.
3. Independently tests whether any 5m bar `open_time` in `[entry_ot, exit_ot]` is missing from the mark-price 5m dataset (defensive — both checks would catch the gap, but the dataset-presence check also catches any future gap not yet recorded as an invalid window).
4. If either test triggers, the trade is **excluded** from Q6 and recorded in the exclusion-counts table (§Q6 results).
5. If neither test triggers, the trade proceeds to mark-vs-trade stop-trigger timing comparison.

**No forward-fill, interpolation, imputation, replacement, synthetic mark-price, or mark-price reconstruction from trade-price is applied at any step.**

### Exclusion-counts result

**Zero trades were excluded** across all populations × symbols. This is consistent with retained-evidence trade lifetimes being short relative to the four mark-price gap windows:
- R3 trades: typically ≤ 8 × 15m = 2h (Fixed-R + 8-bar time-stop per Phase 2p §C.1).
- R2 trades: similar V1-breakout time-stop horizon.
- F1 trades: 8 × 15m = 2h time-stop (Phase 3c).
- D1-A trades: 32 × 15m = 8h time-stop (Phase 3h).

The four mark-price gap windows total 4 425 minutes (BTC) / 2 990 minutes (ETH), but they are concentrated in 4 distinct calendar windows (3 × ~24h + 1 × 30min for BTC; 1 × 10min + 2 × ~24h + 1 × 30min for ETH). For a trade lifetime of ≤ 8h to *intersect* a gap window requires entry timing within ~8h of the gap window. Across the three retained-evidence candidates' total trade populations × the four gap windows × the date range, statistically a small but non-zero number of trades could in principle intersect; the empirical observation is that no actual retained-evidence trade did.

The Phase 3r §8 rule is therefore preserved verbatim and verified to not exclude any current trade — the rule is binding for any future Q6-running phase (e.g. on different backtest populations or windows) where intersection might occur.

## Q1 results

For each retained-evidence candidate × symbol, the table below reports IAE_N (immediate adverse excursion in R units across first N 5m bars) and IFE_N (immediate favorable excursion) for N ∈ {1, 2, 3}. Mean / median / 90th-percentile reported.

### R3 (V1 breakout baseline-of-record)

| Cell | IAE_1 mean | IAE_3 mean | IFE_1 mean | IFE_3 mean | n |
|---|---|---|---|---|---|
| BTC | 0.250 | 0.418 | 0.091 | 0.250 | 33 |
| ETH | 0.221 | 0.341 | 0.259 | 0.515 | 33 |

### R2 (V1 breakout pullback-retest)

| Cell | IAE_1 mean | IAE_3 mean | IFE_1 mean | IFE_3 mean | n |
|---|---|---|---|---|---|
| BTC | 0.201 | 0.255 | 0.172 | 0.440 | 23 |
| ETH | 0.326 | 0.440 | 0.076 | 0.295 | 19 |

### F1 (mean-reversion-after-overextension)

| Cell | IAE_1 mean | IAE_3 mean | IFE_1 mean | IFE_3 mean | n |
|---|---|---|---|---|---|
| BTC | 0.506 | 0.797 | 0.252 | 0.462 | 4 720 |
| ETH | 0.496 | 0.785 | 0.264 | 0.473 | 4 826 |

### D1-A (funding-aware contrarian)

| Cell | IAE_1 mean | IAE_3 mean | IFE_1 mean | IFE_3 mean | n |
|---|---|---|---|---|---|
| BTC | 0.358 | 0.547 | 0.225 | 0.489 | 198 |
| ETH | 0.398 | 0.660 | 0.278 | 0.553 | 179 |

### Q1 interpretation (Phase 3p §8.1)

**Verdict: Informative.**

- **Cross-candidate consistency:** IAE_1 mean > IFE_1 mean in 7 of 8 candidate × symbol cells (only ETH R3 has IFE_1 > IAE_1, marginally: 0.259 vs 0.221). The cross-cell IAE-dominance pattern is replicable.
- **Cross-symbol replicability:** Within each candidate, BTC and ETH IAE_1 means are within ±0.10 R for R3, F1, D1-A; R2 has BTC=0.201 vs ETH=0.326 (0.125 R apart), slightly outside the predeclared ±0.10 R band but directionally consistent (both adverse).
- **Mechanism reasoning:** F1's IAE_1 ≈ 0.5 R is striking — half of the stop distance is consumed in the first 5 minutes after entry, before any mean-reversion of the supposed overextension materializes. D1-A's IAE_1 ≈ 0.36–0.40 R is also substantial, given the funding-extreme contrarian setup ostensibly anticipates immediate mean-reversion. R3 / R2 IAE_1 ≈ 0.20–0.33 R is smaller in magnitude but still adverse-leaning. *All four mechanism stories are challenged by the empirical adverse-bias finding.*
- **Replicability across sub-periods:** Not formally tested (a sub-period split would require a separate predeclared methodology). The within-population variance bands (p25–p75) are reported in the JSON output and show fairly stable centrality estimates.

**Phase 3p §8.1 critical reminder verbatim:** *"R2's §11.6 verdict, F1's HARD REJECT verdict, and D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict are terminal under current locked spec. Q1 produces path evidence, not threshold evidence. The §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gates are not Q1's domain. Verdict revision would require a separately authorized formal reclassification phase with predeclared evidence thresholds, which Phase 3o does not propose."*

Phase 3s adds: nor does Phase 3s. The Q1 finding is descriptive only.

## Q2 results

Wick-stop / sustained-stop / indeterminate counts for STOP-exited trades, per candidate × symbol. Wick-fraction = wick / (wick + sustained + indeterminate).

| Candidate | Symbol | Wick | Sustained | Indeterminate | Total | Wick-fraction |
|---|---|---|---|---|---|---|
| R3 | BTC | 5 | 0 | 1 | 6 | **0.833** |
| R3 | ETH | 7 | 4 | 0 | 11 | **0.636** |
| R2 | BTC | 4 | 0 | 0 | 4 | **1.000** |
| R2 | ETH | 4 | 3 | 0 | 7 | **0.571** |
| F1 | BTC | 599 | 809 | 317 | 1 725 | **0.347** |
| F1 | ETH | 599 | 868 | 273 | 1 740 | **0.344** |
| D1-A | BTC | 33 | 48 | 21 | 102 | **0.324** |
| D1-A | ETH | 25 | 48 | 20 | 93 | **0.269** |

### Q2 interpretation (Phase 3p §8.2)

**Verdict: Informative.**

The wick-fraction differential between the V1-family (R3, R2) and the F1/D1-A families is **the largest mechanism-level pattern in the entire Phase 3s output:**

- **V1-family (R3, R2):** Wick-fraction 0.571–1.000 across all four cells. Stops are predominantly triggered by short-lived wicks that close back inside. **Wick-dominated stop pathology.**
- **F1 + D1-A:** Wick-fraction 0.269–0.347 across all four cells. Stops are predominantly triggered by sustained 3+ bar invalidation. **Sustained-dominated stop pathology.**

This is a clean cross-family differentiation, replicable across BTC and ETH within each family. Phase 3p §8.2 informative threshold (wick-fraction ≥ 60% or ≤ 40% in at least one cell, replicable) is met by *both* directions: V1-family ≥ 60% in R3 BTC / R3 ETH / R2 BTC; F1 + D1-A ≤ 40% in all four cells.

### Mechanism reasoning

- **V1-family wick-stops** are consistent with stops being placed at structural+ATR levels that lie *just beyond* recent volatility wicks. The breakouts trigger on completed-bar confirmation, the entry happens on next-bar open, and structural stops sit at a level that 5m wicks frequently penetrate without sustained follow-through. This finding does NOT license stop widening (forbidden by `.claude/rules/prometheus-safety.md`); it does suggest that the V1 structural-stop placement is operating in a wick-vulnerable zone.
- **F1 + D1-A sustained-stops** are consistent with the contrarian / mean-reversion positions being on the wrong side of sustained directional moves. When F1 / D1-A stops trigger, they typically trigger because the underlying impulse continued in the entry-adverse direction for ≥ 3 × 5m bars (≥ 15 min). The mean-reversion thesis didn't materialize in time, and the position invalidated cleanly on close. **This is a *signal-failure* signature, not a *timing-failure* signature.**

### Sample-size caveats

- R3 BTC has only 6 stop events (5 wick, 1 indeterminate). R3 ETH has 11. R2 BTC has 4. R2 ETH has 7. The V1-family wick fractions are computed on small samples and should be interpreted with care (point estimates are extreme but standard errors are large at n=4–11).
- F1 has 1725 / 1740 stop events per symbol — very robust.
- D1-A has 102 / 93 stop events per symbol — robust.

The cross-family pattern (V1 wick vs F1/D1-A sustained) is robust because the F1 and D1-A samples are large; the R3 / R2 point estimates are noisy but the directional contrast remains clear.

**Phase 3p §8.2 critical reminder verbatim:** *"Stop pathology evidence cannot license stop widening (forbidden), cannot revise the §11.6 cost-resilience gate, and cannot revise prior verdicts. Mark-price stop discipline (`docs/07-risk/stop-loss-policy.md`) is preserved verbatim regardless of any Q2 finding."*

## Q3 results

Intrabar / confirmed +1R / +2R target-touch fractions in adverse-exit (STOP / TIME_STOP) trades, per candidate × symbol.

| Candidate | Symbol | Adverse exits | Intrabar 1R frac | Intrabar 2R frac | Confirmed 1R frac | Confirmed 2R frac |
|---|---|---|---|---|---|---|
| R3 | BTC | 33 | **0.273** | 0.151 | (low) | (low) |
| R3 | ETH | 33 | **0.455** | 0.181 | (low) | (low) |
| R2 | BTC | 23 | **0.478** | 0.130 | (low) | (low) |
| R2 | ETH | 19 | **0.474** | 0.158 | (low) | (low) |
| F1 | BTC | 3 184 | 0.236 | 0.048 | (low) | (low) |
| F1 | ETH | 3 216 | 0.240 | 0.052 | (low) | (low) |
| D1-A | BTC | 146 | **0.356** | 0.103 | (low) | (low) |
| D1-A | ETH | 130 | **0.346** | 0.100 | (low) | (low) |

(Confirmed-touch fractions are uniformly low across all populations and not material; full counts available in `docs/00-meta/implementation-reports/phase-3s/q1_q5_results.json`.)

### Q3 interpretation (Phase 3p §8.3)

**Verdict: Informative for +1R; ambiguous for +2R.**

#### +1R touches

- **Above 25% threshold:** R3 ETH (45.5%), R2 BTC (47.8%), R2 ETH (47.4%), D1-A BTC (35.6%), D1-A ETH (34.6%). Five of eight cells.
- **Just below 25% threshold:** F1 BTC (23.6%), F1 ETH (24.0%) — consistent across symbols.
- **Marginal:** R3 BTC (27.3%) — just above threshold.

Six of eight cells ≥ 25%. R2 and D1-A show ≥ 25% on both symbols (cross-symbol replicability confirmed). The Phase 3p §8.3 informative threshold is met for those candidates.

#### +2R touches

- All cells well below typical informativeness threshold (3.6–18.1%).
- F1 strikingly low (4.8% / 5.2%) — consistent with F1's signal-failure pattern (price moves against entry, doesn't reach +1R let alone +2R).
- R3 / R2 / D1-A in the 10–18% range.

**Verdict: ambiguous for +2R.** No coherent informativeness signal at the +2R level.

### Mechanism reasoning

The +1R intrabar-touch finding indicates that a meaningful fraction of adverse-exit trades did *temporarily* reach +1R during their lifetime before reversing. **This is the Phase 3o §6.3 / Phase 3p §8.3 highest-risk finding** — it is *purely descriptive* and *cannot* license any rule revision. Specifically:

- It does **not** prove that an "exit at +1R touch" rule would be profitable (the bars that touch +1R may also be the bars that immediately reverse, making real execution lossy).
- It does **not** prove the touches survive cost-modeling (the §11.6 cost gate already rules out R2 and similar fragile-edge candidates).
- It does **not** prove walk-forward stability (in-sample touches are guaranteed to exist in any sufficiently rich dataset).
- It does **not** prove Q3 results would replicate in OOS or future data.

Phase 3o §6 explicitly forbids the question forms "Which intrabar target touch rule maximizes R?" and "Which 5m exit rule rescues D1-A?" Phase 3s preserves both prohibitions. Phase 3p §8.3 explicitly preserved this discipline.

**Phase 3p §8.3 critical reminder verbatim:** *"This question is the highest-risk predeclared question in the entire spec. No intrabar target-touch finding may be converted into a '5m exit rule' or 'intrabar target rule' without separately authorized formal reclassification phase with predeclared evidence thresholds. The mere existence of intrabar target touches does not prove that an intrabar-target exit rule would be profitable in walk-forward cross-validation, does not prove the touch is exploitable in real execution (mark-price / trade-price divergence may make the touch unfillable in practice), and does not prove the resulting rule would survive the §11.6 cost-resilience gate. Prior verdicts (R3 baseline-of-record; R2 FAILED; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other) are unaffected by any Q3 answer."*

## Q4 results

D1-A funding-extreme decay curve at 5 / 10 / 15 / 30 / 60 minutes after entry (in R-units, contrarian-direction-signed, BTC and ETH separately).

| Symbol | +5min mean R | +10min | +15min | +30min | +60min | sem at +60min |
|---|---|---|---|---|---|---|
| BTC | -0.041 | -0.038 | -0.035 | +0.058 | -0.017 | 0.091 |
| ETH | -0.088 | -0.105 | -0.124 | -0.021 | -0.075 | 0.135 |

(Full sem profile available in JSON output; n=198 BTC, n=179 ETH; +60min n equal because all decays computed.)

### Q4 interpretation (Phase 3p §8.4)

**Verdict: Non-informative.**

Phase 3p §8.4 informative criterion required:
- A coherent decay shape: monotone (or near-monotone) cumulative-displacement curve.
- Replicability across BTC and ETH at the qualitative shape level.
- Standard-error bands tighter than displacement magnitude (specifically: SEM at the 60-minute milestone tighter than the 5-minute-milestone displacement magnitude in at least one symbol).

**Failures:**

- **No monotone decay shape:** BTC curve oscillates -0.041 → -0.038 → -0.035 → +0.058 → -0.017 (non-monotone; +30min is positive while neighbors are negative). ETH curve is closer to monotone in -ve direction at early bars but breaks at +30min (-0.021).
- **Cross-symbol shape disagreement:** BTC's +30min positive value (+0.058) versus ETH's persistent negative pattern (-0.021 to -0.124) is qualitative shape disagreement.
- **SEM-vs-magnitude predicate fails on both symbols:**
  - BTC: SEM(+60min) = 0.091 vs |displacement(+5min)| = 0.041 → SEM > magnitude (FAIL).
  - ETH: SEM(+60min) = 0.135 vs |displacement(+5min)| = 0.088 → SEM > magnitude (FAIL).

The Q4 result is consistent with Phase 3p §8.4's predicted non-informative pattern: *"Curve has high variance with no coherent decay shape; standard-error bands wider than the displacement magnitude at all milestones."*

### Mechanism implication

Q4 was the highest-information-value predeclared question for D1-A specifically (Phase 3o §11.4). A non-informative Q4 result means the funding-extreme decay timescale cannot be cleanly identified at 5m granularity from the v002-locked D1-A trade population. It is consistent with funding-extreme effects being either too small to detect at 5m granularity OR too heterogeneous across events (per Phase 3p §8.4 non-informative description). It does **not** distinguish between fast-decay and slow-decay hypotheses for D1-A's mechanism failure.

**Phase 3p §8.4 critical reminder verbatim:** *"D1-A is MECHANISM PASS / FRAMEWORK FAIL — other under current locked spec. Phase 3j is terminal for D1-A. Q4 findings may inform a possible future operator decision about whether to authorize a D1-A-prime / D1-B / hybrid spec — but Phase 3o does not contemplate any such authorization. The existence of a fast funding-decay curve does not by itself constitute a FRAMEWORK PASS for any successor; it is one piece of mechanism evidence among many that any future successor proposal would have to integrate."*

Phase 3s adds: a non-informative Q4 result *strengthens* the existing remain-paused recommendation rather than weakening it. No D1-A successor is contemplated.

## Q5 results

Fill-assumption realism — 15m next-open vs probability-weighted 5m fill simulation (mid-price = (high + low) / 2 of the first 5m sub-bar containing entry). Reported in trade-direction-signed basis points (positive = 15m fill better than 5m mid; negative = 15m fill worse) and unsigned magnitude.

| Candidate | Symbol | Signed bps mean | Unsigned bps mean | n |
|---|---|---|---|---|
| R3 | BTC | -3.97 | 5.73 | 33 |
| R3 | ETH | +0.39 | 9.66 | 33 |
| R2 | BTC | -0.11 | 3.77 | 23 |
| R2 | ETH | -5.80 | 6.65 | 19 |
| F1 | BTC | -3.71 | 9.30 | 4 720 |
| F1 | ETH | -4.18 | 11.06 | 4 826 |
| D1-A | BTC | -2.91 | 9.24 | 198 |
| D1-A | ETH | -2.91 | 13.97 | 179 |

### Q5 interpretation (Phase 3p §8.5)

**Verdict: Non-informative.**

Phase 3p §8.5 informative criterion: |mean signed slippage| > 8 bps in at least one candidate × symbol cell, with replicability across BTC and ETH at the directional level, and replicability across at least two non-overlapping date sub-ranges within v002.

**No cell exceeds 8 bps in absolute signed value.** The largest signed magnitude is R2 ETH at -5.80 bps (still below threshold). F1 and D1-A both show small consistent negative tilts (-3 to -4 bps signed) suggesting the 15m next-open fill assumption is *very mildly* unfavorable to the trade direction at 5m sub-bar resolution, but the magnitude is well below the 8 bps HIGH per side cost threshold that §11.6 enforces.

The unsigned magnitudes (3.8–14.0 bps) reflect cross-trade variance rather than systematic skew — large but symmetric per-trade deviations average to small signed means.

### Cross-Phase-3l consistency

This Q5 finding is **strongly consistent** with Phase 3l's external execution-cost evidence review primary assessment: *"B — current cost model appears conservative but defensible; §11.6 remains unchanged pending stronger evidence."* Q5 at 5m granularity does not provide stronger evidence to revise §11.6.

**Phase 3p §8.5 critical reminder verbatim:** *"§11.6 = 8 bps HIGH per side is preserved verbatim and is revisable only through a separately authorized formal cost-model revision phase. Phase 3l found the current cost model 'B — conservative but defensible' and explicitly recommended '§11.6 remains unchanged pending stronger evidence.' Q5 produces one piece of fill-realism evidence, not a §11.6 revision input."*

§11.6 = 8 bps HIGH per side preserved verbatim by Phase 3s.

## Q6 results conditional on valid mark-price coverage

Mark-vs-trade stop-trigger 5m-bar timing difference for STOP-exited trades, after Phase 3r §8 invalid-window exclusion. **All Q6 conclusions are conditional on valid mark-price coverage per Phase 3r §8.5.**

| Candidate | Symbol | n applicable | n excluded | n included | n inconclusive | Mean (mark − trade) bars | Frac simultaneous |
|---|---|---|---|---|---|---|---|
| R3 | BTC | 8 | 0 | 8 | 0 | +0.125 | 0.875 |
| R3 | ETH | 14 | 0 | 14 | 0 | +0.286 | 0.929 |
| R2 | BTC | 6 | 0 | 6 | 0 | 0.000 | 1.000 |
| R2 | ETH | 10 | 0 | 10 | 0 | +0.400 | 0.900 |
| F1 | BTC | 2 534 | 0 | 2 531 | 3 | +0.373 | 0.893 |
| F1 | ETH | 2 516 | 0 | 2 516 | 0 | +0.353 | 0.895 |
| D1-A | BTC | 135 | 0 | 135 | 0 | **+1.252** | 0.822 |
| D1-A | ETH | 120 | 0 | 120 | 0 | **+1.783** | 0.817 |

(Positive mean = mark-price stop triggers later than trade-price stop. "Inconclusive" = no 5m-bar stop trigger detected on either side, indicating the stop level was breached only at intra-5m-bar resolution that bulk-archive 5m bars don't capture; very rare.)

### Q6 interpretation (Phase 3p §8.6)

**Verdict: Informative for D1-A; non-informative for R3 / R2 / F1.**

Phase 3p §8.6 informative threshold: mean |timing difference| > 1 5m sub-bar in at least one candidate × symbol cell, replicable across BTC and ETH.

- **D1-A: BOTH symbols exceed 1-bar threshold.** BTC mean +1.252, ETH mean +1.783. Both positive (mark lags trade) — direction consistent. Cross-symbol replicability confirmed. **Q6 informative for D1-A.**
- **R3: BTC +0.125, ETH +0.286** — both well below 1-bar threshold. Q6 non-informative for R3.
- **R2: BTC 0.000, ETH +0.400** — both well below 1-bar threshold. Q6 non-informative for R2.
- **F1: BTC +0.373, ETH +0.353** — both well below 1-bar threshold; cross-symbol consistent. Q6 non-informative for F1 (consistent simultaneous-trigger pattern).

### Phase 3r §8 exclusion-counts table

| Candidate | Symbol | Direction | Exit type | Exclusion reason | Excluded count |
|---|---|---|---|---|---|
| (no rows — zero exclusions across all populations) |||||| **0** |

Zero retained-evidence trades had a Q6 analysis window that intersected any of the four mark-price 5m gap windows. Phase 3r §8 rule was applied verbatim and preserved; the zero-exclusion outcome is empirical, not procedural.

### Mechanism reasoning for D1-A Q6 finding

D1-A's mark-stops trigger ~1.3–1.8 5m-bars (~6–9 minutes) **after** trade-stops would. Among the four candidates, this is the largest mark-vs-trade divergence. Plausible explanations include:

1. **Mark-price smoothing.** Binance USDⓈ-M futures mark price is computed from a weighted average of multiple price sources and is intentionally smoothed (relative to the trade tape) to reduce manipulation-driven liquidations. D1-A's contrarian funding-extreme entries are taken at moments of unusual funding stress — precisely the moments when trade-price tape diverges most from mark-price reference. The lag is consistent with mark-price's design philosophy.
2. **Funding-extreme regime correlation.** D1-A entries cluster at funding-settlement boundaries where market microstructure is unusual. The mark-vs-trade lag could be a *regime-conditional* property rather than a candidate-specific one.

The Q6 finding is descriptive — it does not by itself license any policy change. **Mark-price stops remain locked by §1.7.3** (`docs/07-risk/stop-loss-policy.md`); Phase 3s does not propose revising mark-price stop policy. The finding informs operator understanding of the mechanism *only*.

**Phase 3p §8.6 critical reminder verbatim:** *"Mark-price stop discipline is a `.claude/rules/prometheus-safety.md` lock and is preserved verbatim regardless of any Q6 finding. Q6 provides understanding, not policy revision. Verdicts and stop policies remain unchanged."*

**Phase 3r §8 critical reminder:** Q6 cannot revise prior verdicts, rescue strategies, change parameters, or imply live-readiness. All four constraints preserved.

## Q7 meta-classification

Phase 3p §8.7: Q7 is informative if ≥ 3 of Q1–Q6 are classified informative.

| Question | Classification | Notes |
|---|---|---|
| Q1 | Informative | Cross-candidate IAE > IFE pattern, BTC/ETH replicable. |
| Q2 | Informative | V1-family wick vs F1/D1-A sustained — strongest mechanism finding. |
| Q3 | Informative (+1R) | Six of eight cells ≥ 25% threshold. **Critical: descriptive-only.** |
| Q4 | Non-informative | No monotone decay; SEM > magnitude. |
| Q5 | Non-informative | No |signed| > 8 bps cell. Consistent with Phase 3l. |
| Q6 | Informative (D1-A only) | D1-A both symbols > 1-bar threshold; R3/R2/F1 below. |

**Count: 4 informative (Q1, Q2, Q3, Q6) of 6 ≥ 3 threshold → Q7 = informative.**

Q7 informative means the diagnostic phase as a whole produced a coherent body of informative findings, not just isolated signals. The findings are mechanism-informative across multiple axes (entry-path asymmetry, stop pathology, intrabar target-touch frequency, mark-vs-trade timing). They are emphatically *not* license to revise verdicts, rescue strategies, or change parameters.

**Phase 3p §8.7 verbatim:** *"A `non-informative` Q7 outcome is a valid result of a future diagnostics phase and should *not* trigger framing pressure to find rescue narratives. A `non-informative` Q7 outcome strengthens the existing remain-paused recommendation rather than weakening it."*

Phase 3s adds: *an informative Q7 outcome equally does not license rescue narratives. The Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, and Phase 3p §8 critical reminders bind regardless of Q7's verdict.*

## Cross-question interpretation

Integrating across Q1–Q7 informative findings:

### Pattern A — Universal entry-path adverse bias (Q1)

All four candidates show IAE_1 > IFE_1 in 7 of 8 cells. This is consistent with **completed-15m-bar entries being structurally late** relative to the post-signal price impulse. Whether the impulse is breakout-continuation (R3 / R2), mean-reversion (F1), or funding-extreme contrarian (D1-A), the first 5 minutes after entry-fill typically move adverse before any thesis-confirming move. The magnitude varies (F1 most pronounced at ~0.5 R; R3 / R2 most modest at ~0.2 R).

**Strategic implication: NONE that Phase 3s authorizes.** This finding does *not* license entry-timing modifications, intrabar entry rules, or any 5m-strategy variant. Phase 3o §4.1 / Phase 3p §10 explicitly prohibit 5m as a strategy signal layer. The finding *does* update operator-level understanding of how completed-bar-confirmed entries interact with the post-signal market.

### Pattern B — Wick-vs-sustained stop pathology differentiation (Q2)

V1-family wick-dominated stops vs F1/D1-A sustained-dominated stops is the cleanest cross-family mechanism finding. It says:

- V1 trades fail because their structural+ATR stops sit in a wick-vulnerable zone — but the broader thesis (post-breakout continuation in some form) is not categorically refuted by Q2.
- F1 / D1-A trades fail because the underlying contrarian / mean-reversion thesis is sustained-direction-against — i.e., the *thesis itself* doesn't hold often enough.

**Strategic implication: NONE that Phase 3s authorizes.** Stop widening is forbidden categorically (`.claude/rules/prometheus-safety.md`). Mark-price stop policy is locked (§1.7.3). The finding *does* update operator-level understanding of why each candidate failed framework discipline.

### Pattern C — Q3 +1R intrabar touches (descriptive-only)

Six of eight cells show ≥ 25% intrabar +1R touch fraction in adverse-exit trades. This is the most rescue-shaped finding and is bound by Phase 3p §8.3 / Phase 3o §6.3 prohibitions. **No exit-rule revision is authorized or implied.**

### Pattern D — Q6 D1-A mark-stop lag (~6–9 minutes)

D1-A's mark-stops trigger systematically later than trade-stops would. The pattern is robust (n=135 BTC, 120 ETH) and consistent in direction across symbols. This is descriptive evidence about market microstructure at funding-event boundaries, NOT a stop-policy revision input.

### Patterns A–D in context of Phase 3p §8 critical reminders

All four informative findings are bound by Phase 3p §8 critical reminders and Phase 3o §6 / §10 prohibitions:

- They cannot license verdict revision (R3 / R2 / F1 / D1-A all preserved).
- They cannot license parameter changes, threshold revisions, or project-lock revisions.
- They cannot license strategy rescue (no 5m strategy, no D1-A-prime, no D1-B, no hybrid).
- They cannot imply live-readiness (no paper/shadow / Phase 4 / deployment).
- They cannot license stop-policy revision (mark-price stops locked).

**The findings update *understanding*; they do not update *action*.**

## Answer to the four unresolved strategic questions

The Phase 3n memo (§3) listed four unresolved questions that motivated the entire 5m research thread. Phase 3s now provides Phase-3p-§8-bounded answers:

| Question | Phase 3s answer |
|---|---|
| **Are we missing useful timing information inside 15m bars?** | **Yes (Q1, Q2 informative; Q3 informative for +1R touches).** Completed-15m-bar entries hide a consistent first-5min adverse path bias (Q1) and stop pathology that differentiates strategy families (Q2). However, this useful information cannot be acted on in a 5m strategy layer (Phase 3o §4.1 / Phase 3p §10 prohibition) and cannot license rule revision for retained-evidence candidates (Phase 3p §8 critical reminders). The information updates operator understanding only. |
| **Can regimes be defined cleanly before testing, without overfitting?** | **Phase 3s does not formally answer — out of scope for predeclared Q1–Q7.** The Q2 stop-pathology differential (V1-family wick vs F1/D1-A sustained) suggests a candidate-family-conditional structural pattern, but this is descriptive at the candidate level, not at a regime level. Phase 3m's regime-first framework memo discipline (defining regimes from first principles, not from winning-fold-derived labels) was not exercised in Phase 3s. **Phase 3s recommends remain paused on regime-first work.** |
| **Would more granular data help diagnostics, or just increase noise/cost?** | **Mostly increases noise/cost.** The 5m diagnostics produced 4 informative classifications out of 6 (Q1 / Q2 / Q3 / Q6), but two of those (Q4 / Q5) failed informative thresholds despite being mechanism-relevant. Sub-minute or tick data would likely add more noise without sharpening the mechanism stories that are already informative at 5m. **Phase 3s does NOT recommend authorizing finer-than-5m data acquisition.** |
| **Is there a truly new hypothesis strong enough to deserve implementation?** | **No.** The four informative findings (entry-path adverse bias; wick-vs-sustained pathology; intrabar +1R touch frequency; D1-A mark-stop lag) are all *mechanism-informative descriptive* evidence. None constitutes a *strategy candidate* — strategy candidates require a complete entry / target / stop / time-stop / cooldown specification *plus* predeclared evidence thresholds *plus* walk-forward validation *plus* §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gate compliance. The Q3 / Q6 findings in particular cannot be converted into strategy variants without violating Phase 3o §6 forbidden question forms. **Phase 3s does NOT recommend any new strategy candidate, hybrid, variant, or successor.** |

### Summary answer matrix

```text
Are we missing useful timing information?    YES (descriptive only; cannot be acted on)
Can regimes be defined cleanly?               OUT OF SCOPE (Phase 3s did not test)
Would more granular data help?                NO (5m suffices; finer = more noise)
Is there a strong new hypothesis?             NO (informative findings ≠ strategy candidates)
```

## What Phase 3s does not authorize

Phase 3s does NOT authorize, propose, or initiate any of the following:

- **Verdict revision.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. All preserved verbatim.
- **Threshold revision.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 = 8 bps HIGH per side. All preserved verbatim.
- **Project-lock revision.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) preserved verbatim.
- **Strategy-parameter changes.** R3 / R2 / F1 / D1-A specs preserved verbatim.
- **Strategy rescue.** No R2 / F1 / D1-A successor authorized. No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or 5m-on-X variant proposed.
- **5m strategy.** Phase 3o §4.1 / Phase 3p §10 prohibition preserved.
- **Stop-policy revision.** Mark-price stop discipline (§1.7.3 + `.claude/rules/prometheus-safety.md`) preserved.
- **Cost-model revision.** §11.6 preserved. Phase 3l "B — conservative but defensible" stands.
- **Manifest re-issue.** Phase 3q v001-of-5m manifests untouched. Mark-price `research_eligible: false` preserved.
- **v002 modification.** v002 datasets and manifests untouched.
- **Phase 3p §4.7 amendment.** Preserved verbatim.
- **Phase 3o / 3p / 3r rule modification.** All predeclared rules preserved verbatim. Phase 3r §8 binding for any future Q6-running phase.
- **Implementation.** No runtime, strategy, execution, risk, persistence, dashboard, observability, or test code changed.
- **Backtests.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed. No control rerun. No retained-evidence trade population regenerated.
- **ML feasibility.** Not authorized; not proposed.
- **Regime-first formal spec.** Not authorized; not proposed.
- **New strategy-family discovery.** Not authorized; not proposed.
- **Paper/shadow planning.** Not authorized.
- **Phase 4.** Not authorized; no runtime / state / persistence / risk-runtime work.
- **Live-readiness.** Not authorized.
- **Deployment.** Not authorized.
- **Production-key creation.** No production keys requested, generated, stored, or referenced.
- **Exchange-write capability.** No exchange-write paths exist or were touched.
- **MCP / Graphify / `.mcp.json`.** Not enabled. Not used.
- **Credentials.** None requested. None used. None stored.
- **Authenticated APIs / private endpoints / user stream / WebSocket.** Not used.
- **Data acquisition / patching / regeneration / modification.** No download. No HTTP request. No `data/` artefact modified.
- **Forward-fill / interpolation / imputation / replacement.** Not applied at any step. Phase 3r §8 prohibition preserved.

## Forbidden-work confirmation

- No backtests run. No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- No retained-evidence trade population regenerated.
- No v002 dataset modification.
- No v002 manifest modification.
- No Phase 3q v001-of-5m manifest modification.
- No v003 created.
- No data acquisition / download / patching / regeneration / modification.
- No forward-fill / interpolation / imputation / replacement / synthetic data.
- No strategy spec / threshold / parameter / project-lock / prior-verdict modification.
- No verdict revision (R3 baseline-of-record; H0 framework anchor; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other all preserved).
- No 5m strategy / hybrid / variant proposal.
- No strategy rescue.
- No Phase 4 / paper-shadow / live-readiness / deployment / production-key / exchange-write paths touched.
- No MCP / Graphify / `.mcp.json` activation.
- No credentials / authenticated APIs / private endpoints / user stream / WebSocket / secrets.
- No merge to main.

## Remaining boundary

- **Recommended state:** **paused.**
- **5m research thread state:** Complete. Phase 3o predeclared questions; Phase 3p added data-requirements + dataset-versioning + manifest specification + per-question outputs + outcome-interpretation rules; Phase 3q acquired data + ran integrity checks; Phase 3r added mark-price gap governance + §8 Q6 invalid-window exclusion rule; Phase 3s executed Q1–Q7 once, classified per Phase 3p §8 verbatim, applied Phase 3r §8 rule (zero exclusions empirically). The thread is operationally finished — running anything further (sub-period splits, alternative slip variants, alternative stop-classification thresholds, etc.) would require a separately authorized phase and would itself be subject to Phase 3o §6 forbidden question forms and Phase 3p §8 outcome-interpretation rules.
- **Trade-price 5m datasets:** locally research-eligible; used by Q1 / Q2 / Q3 / Q4 / Q5 / Q6 (trade-side) and produced informative classifications for Q1 / Q2 / Q3 / Q6.
- **Mark-price 5m datasets:** NOT research-eligible under Phase 3p §4.7 strict gate. Used by Q6 (mark-side) under Phase 3r §8 exclusion rule. Zero exclusions empirically.
- **Project locks preserved verbatim.**
- **Branch state:** `phase-3s/5m-diagnostics-execution` not merged to main. main = origin/main = `f20c0edb9a80b4bfdd0863687416939427ad1184` (unchanged).

## Operator decision menu

The operator now has Phase 3s's complete diagnostic output: 4 informative classifications, 2 non-informative classifications, Q7 informative (≥ 3 informative threshold met). The next operator decision is operator-driven only.

### Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategy-execution pause continues. Phase 3s joins Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r as the running record of the 5m research thread. No diagnostic output is converted into action. No subsequent phase authorized.

**Reasoning:**

- The Phase 3s diagnostic output is *informative-but-not-actionable* by predeclared rule. Phase 3p §8 critical reminders, Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, Phase 3r §8 Q6 exclusion rule all forbid converting the findings into verdict revision, parameter change, or strategy rescue.
- The 5m research thread has reached its operational endpoint. Further diagnostic runs would either repeat the same questions on alternative populations (low marginal value) or extend into forbidden territory (high risk).
- Phase 3s's strongest finding (Q2 wick-vs-sustained pathology differential) is a *negative* result for any rescue narrative: it identifies that V1-family fails because of stop-vulnerability and F1/D1-A fail because of signal-vulnerability — neither of which has an obvious cleanly-implementable fix that survives Phase 3o / 3p / 3r discipline.
- Q4 non-informative + Q5 non-informative *strengthen* the remain-paused recommendation per Phase 3p §8.4 / §8.7 framing.
- Project locks preserved. No further operator action required to preserve safety state.

### Option B — Authorize a docs-only post-Phase-3s consolidation memo (CONDITIONAL secondary alternative)

**Description:** Authorize a future docs-only memo that integrates the Phase 3s informative findings (Q1 entry-path adverse bias; Q2 wick-vs-sustained pathology; Q3 +1R touch frequency descriptive-only; Q6 D1-A mark-stop lag) into the project's framework-discipline knowledge base. The memo would NOT propose any strategy / verdict / parameter change; it would record the mechanism-level understanding for future framework-design memos.

**Pre-conditions if selected:**

- Operator commits ex-ante that the consolidation memo cannot license verdict revision, parameter change, strategy rescue, or 5m-strategy proposal.
- Operator commits ex-ante that the memo applies only to *understanding* of why retained-evidence candidates failed, not to *action* on them.
- The memo would be subject to all Phase 3o / 3p / 3r prohibitions.

**Risks if selected:**

- Procedural escalation: nine docs-only / docs-and-data phases on the 5m thread would consolidate into an even-longer paper trail. The marginal value is bounded.
- The risk of "consolidation memo becomes implicit rule-revision authorization" is real and would need explicit ex-ante framing to avoid.

**Phase 3s view:** Acceptable as conditional secondary. Not endorsed over Option A.

### Options C–F — NOT recommended

- **C — Authorize any 5m strategy proposal.** Forbidden by Phase 3o §4.1 / Phase 3p §10. Strongly not recommended.
- **D — Authorize D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, or any retained-evidence successor.** Phase 3p §11 explicitly does not contemplate these; Phase 3s preserves that posture. Not recommended.
- **E — Authorize regime-first formal spec, ML feasibility, formal cost-model revision, or new strategy-family discovery.** All independent of Phase 3s findings; Phase 3m / 3n already evaluated and recommended remain paused. Not recommended.
- **F — Authorize paper/shadow, Phase 4, live-readiness, deployment, production-key creation, exchange-write, MCP / Graphify / `.mcp.json` / credentials.** None appropriate from current state. Strongly not recommended.

### Recommendation

**Phase 3s recommends Option A (remain paused) as primary.**

The 5m research thread is operationally complete. Diagnostics produced informative findings *under predeclared rules* but no finding licenses action. The operator's next decision is whether to (a) remain paused (Phase 3s primary), (b) authorize Option B docs-only consolidation if the operator wants the mechanism-level understanding formally captured, or (c) reject Phase 3s and request changes. **No implementation, backtest, paper/shadow, Phase 4, live-readiness, deployment, strategy rescue, or successor strategy is recommended.**

## Next authorization status

**No next phase has been authorized.** Phase 3s authorizes nothing other than producing this report and the closeout artefact. Phase 3s recommends Option A (remain paused) as primary; Option B (docs-only post-Phase-3s consolidation memo) as conditional secondary subject to explicit anti-rescue preconditions; Options C / D / E / F NOT recommended. Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
