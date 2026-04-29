# Phase 3g — Methodology Sanity Audit

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (pre-declared promotion / disqualification thresholds; **no post-hoc loosening per §11.3.5**); Phase 2i §1.7.3 project-level locks; Phase 2p consolidation memo §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved verbatim); Phase 3a new-strategy-family discovery memo; Phase 3b F1 spec memo; Phase 3c F1 execution-planning memo; Phase 3d-A / 3d-B1 / 3d-B2 reports (F1 HARD REJECT); Phase 3e post-F1 research consolidation memo; Phase 3f next research-direction discovery memo (D1 ranked rank-1); Phase 3g D1 funding-aware spec memo with first amendment (five spec-consistency corrections) and second amendment (RR/target sanity review — Option A: target revised to +2.0R); `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`.

**Phase:** 3g — Docs-only **methodology sanity audit** ahead of Phase 3g merge. Retrospective methodological review of all V1-family + F1 candidates and the amended D1-A spec to identify any structural oversights (analogous to the +1.0R RR concern that triggered the second amendment).

**Branch:** `phase-3g/d1-funding-aware-spec`. **Audit date:** 2026-04-28 UTC.

**Status:** Audit drafted. **No code change. No backtest. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal.** The audit is **read-only retrospective + amended-D1-A confirmation**; no spec is altered by this audit beyond closeout-report updates.

---

## 1. Plain-English explanation of why this audit exists

Operator review of the original Phase 3g spec caught a structural risk-reward concern: the +1.0R / −1.0R target/stop pairing produced a 76–93% required win-rate burden after costs and uncertain funding accrual, which is impractical given empirical V1 / R3 / F1 win rates of 21–42%. The Phase 3g spec was amended via Option A: target revised to +2.0R using R3's established non-fitting project convention.

**This audit asks:** were similar structural oversights present in prior strategy phases or in the amended D1-A spec, and if so, are they already safely contained by prior verdicts, or do they require docs-only clarification before Phase 3g merges?

The audit is **retrospective and forward-looking**, not corrective. It does not authorize any threshold, parameter, project-lock, paper/shadow, Phase 4, live-readiness, deployment, code, test, or script change. Its output is a structured cross-strategy matrix, a per-candidate methodological assessment, retrospective concern triage, an amended-D1-A confirmation, a future-spec checklist, and a final merge-readiness recommendation.

The audit operates within Phase 3e's pause posture (no next phase started; D8 default-primary recommendation preserved; Phase 3h not authorized).

---

## 2. Cross-strategy matrix

R-window evidence: 2022-01-01 → 2025-01-01, MEDIUM slippage, MARK_PRICE stop-trigger, locked Phase 2e v002 datasets, BTCUSDT primary, ETHUSDT comparison.

Cost-stack reference (BTC, stop-distance ≈ 30 bps notional ≈ 1.0 × ATR price-fraction):

- Round-trip taker fee: 10 bps ≈ 0.33 R per trade.
- LOW slippage round-trip: 2 bps ≈ 0.07 R per trade.
- MED slippage round-trip: 6 bps ≈ 0.20 R per trade.
- HIGH slippage round-trip: 16 bps ≈ 0.53 R per trade.
- Total cost-stack at MED ≈ 0.53 R per trade.
- Total cost-stack at HIGH ≈ 0.86 R per trade.

| Candidate | Target / stop | Gross BE WR | Net BE WR (MED) | Net BE WR (HIGH) | Empirical R-WR | Trade count (R-window per symbol) | Cost-dominance risk | Final verdict |
|-----------|---------------|------------:|----------------:|-----------------:|----------------|----------------------------------:|---------------------|---------------|
| **H0** | Staged trailing (no fixed RR); STAGNATION at 8 bars w/o +1.0 R MFE | undefined (variable) | n/a | n/a | BTC 30.30% / ETH 21.21% | 33 / 33 | **HIGH** — staged-trailing destroys upside; mostly STAGNATION + STOP exits | Locked anchor (Phase 2i §1.7.3); not a candidate. |
| **R3** | +2.0R / −1.0R (Fixed-R + 8-bar TIME_STOP) | 33% | ~51% | ~62% | BTC 42.42% / ETH 33.33% | 33 / 33 | LOW (structurally) | PROMOTE — baseline-of-record (Phase 2p §C.1). Aggregate expR still negative (BTC −0.240 / ETH −0.351); R3 is "less negative than H0", not break-even. |
| **R1a + R3** | +2.0R / −1.0R (R3 exit; R1a-only setup change) | 33% | ~51% | ~62% | BTC 27.27% / ETH 34.78% | 22 / 23 | LOW (same RR as R3) | mixed-PROMOTE; non-leading; retained-research-evidence (Phase 2p §D). Symbol-asymmetric (ETH-favorable / BTC-degrading); ineligible under §1.7.3 BTCUSDT-primary lock. |
| **R1b-narrow + R3** | +2.0R / −1.0R (R3 exit; R1b-only bias change) | 33% | ~51% | ~62% | BTC 50.00% / ETH 33.33% | 10 / 12 | LOW (same RR as R3) | PROMOTE-with-caveats; non-leading; retained-research-evidence (Phase 2s §13). Trade-count drops 65–70%; per-fold n=0–3 sample-fragile. |
| **R2 + R3** | +2.0R / smaller R-distance (R3 exit + R2 pullback-retest entry; effective R-multiple ~85% of R3 due to pullback geometry) | ~33% | ~55% (cost a larger fraction of smaller R) | ~80%+ (HIGH) | BTC 35% / ETH 32% | 23 / 19 | **HIGH** — small post-pullback R-distance amplifies cost (Phase 2w §11.6 failure mechanism) | FRAMEWORK FAILED — §11.6 cost-sensitivity blocks (Phase 2w §16.3). M1 + M3 PASS but slippage-fragile. |
| **F1** | SMA(8) frozen target / −1.0 × ATR(20) stop − 0.10 × ATR buffer (effective R-multiples ~0.3–1.0R) | ~50–60% | ~70%+ (target small, cost a large fraction) | ~80–90% | BTC 33.05% / ETH 33.36% | 4720 / 4826 | **CATASTROPHIC** — high frequency × tight target × per-trade negative expR aggregates to −546% total return at MED on BTC | HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate; 5 violations across BTC/ETH × MED/HIGH); retained-research-evidence; Phase 3d-B2 terminal for F1. |
| **D1-A original (+1.0R)** | +1.0R / −1.0R | 50% | **76.5%** | **93.0%** | not run | est. 60–180 / 60–180 (R-window per symbol) | **HIGH** — required win-rate burden impractical given empirical V1/R3/F1 win rates of 21–42% | Caught by Phase 3g RR/target sanity review; **revised to +2.0R per Option A** before merge. |
| **D1-A amended (+2.0R)** | +2.0R / −1.0R (R3 convention reused) | 33% | ~51% (no funding) / ~45% (with one-cycle ~0.17R funding accrual) | ~62% (no funding) / ~56% (with funding) | not run | est. 60–180 / 60–180 (R-window per symbol) | LOW (structurally; same RR as R3) | Spec only; first-execution gate proposed; not yet executed. Phase 3g recommends GO (provisional) for future Phase 3h, contingent on operator authorization. |

Notes on the matrix:

- **Net BE WR estimates** assume the simple `WR × winner_net + (1−WR) × loser_net = 0` solution. Real distributions include TIME_STOP exits at intermediate R-multiples that soften both extremes; the headline figures are conservative upper bounds.
- **Empirical R-WR for V1 candidates** is from the Phase 2l / 2m / 2s / 2w R-window comparison reports.
- **F1 empirical R-WR** is from Phase 3d-B2 §7.1 (BTC 33.05% / ETH 33.36%).
- **D1-A empirical R-WR** is not yet observed (no D1-A backtest has been run; the spec has not been executed).

---

## 3. Per-candidate methodological assessment

For each candidate, the audit assesses 11 attributes per the brief.

### 3.1 H0 (Phase 2e locked baseline)

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | Staged trailing (Stage 3 risk-reduction at +1.0R; Stage 4 break-even at +1.5R; Stage 5 trailing at +2.0R) plus STAGNATION exit at 8 bars without +1.0R MFE. The R-multiple distribution is structurally adverse: most trades exit at slight loss (STAGNATION) or full stop; the few winners are capped by trailing. |
| **Gross BE WR** | Undefined (variable). Effective average winner is small-positive (~+0.5 to +1.0R) and average loser is full stop (−1.0R). |
| **Net BE burden** | Very high — staged-trailing systematically converts potential winners into breakevens or losses. |
| **Costs structurally dominate?** | Indirectly yes — the staged-trailing destroys edge that exists in a way costs cannot fully explain, but the cost-stack on small winners is also unfavorable. |
| **Sample-size risk** | LOW — 33 trades per symbol per R-window is tight but consistent across candidates. |
| **Target/stop/time-stop coherence** | LOW coherence — the multi-stage trailing + STAGNATION machinery has many ways to exit early; documented as the failure mode R3 was designed to fix. |
| **Fill timing / same-bar priority** | Standard V1 next-bar-open fill; STOP > TAKE_PROFIT > TRAILING > STAGNATION same-bar precedence. |
| **Timestamp / lookahead leakage risk** | LOW — completed-bar-only; 1h bias uses most recent completed 1h bar; bit-for-bit reproducible across all phases. |
| **Target-subset evidence misleading?** | N/A — H0 is the locked anchor, not a promotion candidate. |
| **Descriptive vs governing separation** | N/A — H0 is the governing anchor for V1-family per Phase 2i §1.7.3. |
| **Final verdict handled correctly?** | **YES** — H0 is locked as anchor, not promoted; aggregate negative expR is the framework's *baseline*, not a failure to recover. |

### 3.2 R3 (Phase 2j §D — Fixed-R + 8-bar TIME_STOP, no trailing)

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | +2.0R / −1.0R clean. Same-bar priority STOP > TAKE_PROFIT > TIME_STOP. Protective stop never moved intra-trade. |
| **Gross BE WR** | 33%. Project's strongest natural R/R configuration. |
| **Net BE burden** | ~51% MED / ~62% HIGH (without funding considerations). Within plausible WR range. |
| **Costs structurally dominate?** | NO — +2.0R target provides meaningful R-multiple room for cost absorption. R3 is cost-robust at HIGH on both symbols (Phase 2l verified). |
| **Sample-size risk** | LOW — 33 trades per symbol per R-window. |
| **Target/stop/time-stop coherence** | HIGH — three exit reasons (STOP / TAKE_PROFIT / TIME_STOP) with clean priority; no overlapping exit machinery. |
| **Fill timing / same-bar priority** | Standard V1 next-bar-open fill; clean STOP > TAKE_PROFIT > TIME_STOP precedence. |
| **Timestamp / lookahead leakage risk** | LOW — bit-for-bit reproducible across all phases including Phase 3d-B2. |
| **Target-subset evidence misleading?** | N/A — R3's broad-based PROMOTE is across all 6 regime-symbol cells; no need for subset rescue. |
| **Descriptive vs governing separation** | Clean — Phase 2l / 2m / 2s / 2w consistently treat H0 anchor as governing and R3-anchor view as descriptive when applicable. |
| **Final verdict handled correctly?** | **YES** — R3 PROMOTE, baseline-of-record per Phase 2p §C.1. The honest "less negative than H0, not break-even" framing has been preserved through subsequent phases. |

### 3.3 R1a + R3

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | Same as R3 (+2.0R / −1.0R); R1a only changes setup-validity predicate. |
| **Gross BE WR** | 33%. Same as R3. |
| **Net BE burden** | ~51% MED / ~62% HIGH. |
| **Costs structurally dominate?** | NO — same R/R profile as R3. R1a's filter further reduces trade count (33 → 22/23), which is descriptive concentration, not cost-dominance. |
| **Sample-size risk** | MODERATE — R-window n=22/23 (vs R3's 33); per-fold n=2–7. Below R3's sample-size band. |
| **Target/stop/time-stop coherence** | HIGH — R3's clean exit machinery preserved. |
| **Fill timing / same-bar priority** | Same as R3. |
| **Timestamp / lookahead leakage risk** | LOW — bit-for-bit H0/R3 control reproduction in Phase 2m. |
| **Target-subset evidence misleading?** | N/A — R1a is a setup-axis predicate, not a target-subset rescue. |
| **Descriptive vs governing separation** | Clean — Phase 2m §6.1 uses H0 as governing anchor; R3-anchor view (descriptive) reveals the BTC degradation that the H0-anchor PROMOTE obscures. |
| **Final verdict handled correctly?** | **YES** — mixed-PROMOTE / non-leading / retained-research-evidence; the symbol-asymmetric BTC degradation under §1.7.3 BTCUSDT-primary lock is correctly recognized and prevents promotion to leading status. |

### 3.4 R1b-narrow + R3

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | Same as R3 (+2.0R / −1.0R); R1b-narrow only changes bias-validity predicate. |
| **Gross BE WR** | 33%. Same as R3. |
| **Net BE burden** | ~51% MED / ~62% HIGH. |
| **Costs structurally dominate?** | NO — same R/R profile as R3. |
| **Sample-size risk** | **HIGH** — R-window n=10/12 (vs R3's 33); per-fold n=0–3; BTC V-window n=1 (uninterpretable). The 65–70% trade-count drop is the binding sample-size concern. |
| **Target/stop/time-stop coherence** | HIGH — R3's clean exit machinery preserved. |
| **Fill timing / same-bar priority** | Same as R3. |
| **Timestamp / lookahead leakage risk** | LOW. |
| **Target-subset evidence misleading?** | N/A — R1b-narrow is a bias-axis predicate, not a target-subset rescue. **However**, the §10.3.a-on-both PROMOTE is dominated by trade-count concentration plus R3 exit-machinery contribution — the *formal* §10.3.a clearance does not imply genuine per-trade-expectancy gain on top of R3 (R3-anchor Δexp_R3 −0.023 BTC is roughly neutral). Phase 2s §13 / Phase 2x §4.3 correctly note this methodological observation. |
| **Descriptive vs governing separation** | Clean — Phase 2s explicitly distinguishes the formal H0-anchor PROMOTE from the R3-anchor near-neutrality. |
| **Final verdict handled correctly?** | **YES** — PROMOTE-with-caveats / non-leading / retained-research-evidence per Phase 2s §13. The framework discipline is preserved (PROMOTE under unchanged §10.3 thresholds) while the strategic interpretation honestly notes that the absolute-edge case is sample-fragile and dominated by R3. The R1b-narrow precedent is the project's clearest example of "comparison-metric clearance can occur via trade-count concentration without genuine per-trade-expectancy gain"; this lesson informs future evaluation discipline. |

### 3.5 R2 + R3

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | +2.0R target preserved from R3, but R2's pullback-retest entry geometry reduces the absolute R-distance: empirical stop-distance ratios 0.844 BTC / 0.815 ETH (R-multiple potential ~85% of R3's). |
| **Gross BE WR** | ~33% (target / stop ratio similar). |
| **Net BE burden** | ~55–65% MED / ~80%+ HIGH — the smaller absolute R-distance means cost-as-fraction-of-R is materially larger than R3's. |
| **Costs structurally dominate?** | **YES** — this is exactly the §11.6 failure mechanism. At HIGH slippage, the per-trade cost increase (~0.06 R) approximately equals R2's M1 per-trade gain (+0.12 R BTC). |
| **Sample-size risk** | MODERATE — R-window n=23/19; comparable to R1a+R3. |
| **Target/stop/time-stop coherence** | MODERATE — R3 exit machinery preserved, but the entry geometry creates a structural cost-fragility that the exit machinery cannot fully compensate. |
| **Fill timing / same-bar priority** | Standard; STRUCTURAL_INVALIDATION cancellation at precedence position 3 (Phase 2v Gate 2 amendment). |
| **Timestamp / lookahead leakage risk** | LOW — bit-for-bit H0/R3 controls in Phase 2w. |
| **Target-subset evidence misleading?** | **YES, but contained.** R2's M1 + M3 PASS produced mechanism-supported evidence; M2 FAILED. Phase 2w §16.3 correctly framed the M3 PASS as *research evidence, not promotion*; F1's later HARD REJECT under analogous framing reinforced this discipline. |
| **Descriptive vs governing separation** | Clean — H0 anchor governing; M1/M2/M3 mechanism PASS/FAIL is descriptive. |
| **Final verdict handled correctly?** | **YES** — FRAMEWORK FAILED — §11.6 cost-sensitivity blocks; retained-research-evidence per Phase 2w §16.3. The slippage-fragility was correctly identified as the binding gate. Phase 3c §7.2(iv) operator-mandated amendment (BTC HIGH expR > 0) was directly motivated by R2's §11.6 failure pattern. |

### 3.6 F1 (mean-reversion-after-overextension)

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | SMA(8) frozen target / −1.0 × ATR(20) − 0.10 × ATR buffer stop; effective R-multiples ~0.3–1.0R per trade (empirical). Target geometrically *closer* to entry than R3's +2.0R. |
| **Gross BE WR** | ~50–60% (target smaller than stop). |
| **Net BE burden** | ~70%+ MED / ~80–90% HIGH — small target × per-trade cost-stack = large cost-as-fraction-of-R. |
| **Costs structurally dominate?** | **CATASTROPHICALLY YES** — at MED, BTC expR=−0.5227 / per-trade cost compounding × 4720 trades = total return −546%. Empirical confirmation of Phase 3a §4.1(g) "moderate-to-high cost sensitivity" warning, but worse than anticipated. |
| **Sample-size risk** | LOW (statistical) — 4720+ trades per symbol → high statistical power. **But trade-frequency × negative expR aggregation is the binding catastrophic-floor mechanism** (different from sample-size risk). |
| **Target/stop/time-stop coherence** | HIGH within the F1 hypothesis — clean STOP > TARGET > TIME_STOP precedence; SMA(8) frozen at signal close. |
| **Fill timing / same-bar priority** | Standard next-bar-open fill; STOP > TARGET > TIME_STOP per Phase 3b §6 / Phase 3d-A. |
| **Timestamp / lookahead leakage risk** | LOW — Phase 3d-B2 §13 P.14 invariants all PASS; H0/R3 controls bit-for-bit. |
| **Target-subset evidence misleading?** | **YES, but contained.** F1's M3 PASS (TARGET-exit subset profitable in isolation: BTC mean +0.75R / aggregate +1149R) is empirically informative but does NOT constitute promotion authority. Phase 3c §7.3 catastrophic-floor predicate correctly took precedence; Phase 3e §5.4 / §8.6 explicitly forbade F1-prime / target-subset rescue. The R2 → F1 → F1-prime treadmill risk is now an established discipline pattern. |
| **Descriptive vs governing separation** | Clean — Phase 3c §7.4 / Phase 3d-B2 §15 explicitly state H0/R3 deltas are descriptive cross-family references only, not §10.3-equivalent governing metrics. The first-execution gate evaluated F1 against self-anchored absolute thresholds. |
| **Final verdict handled correctly?** | **YES** — HARD REJECT (Phase 3c §7.3 catastrophic-floor predicate; 5 violations); retained-research-evidence; Phase 3d-B2 terminal for F1; F1-prime forbidden. The catastrophic-floor predicate correctly triggered HARD REJECT despite M3 PASS-isolated, preventing target-subset rescue. |

### 3.7 D1-A amended (+2.0R after Phase 3g RR sanity review)

| Attribute | Assessment |
|-----------|-----------|
| **Risk/reward profile** | +2.0R / −1.0R (R3 convention reused); recorded exit reason TARGET; STOP > TARGET > TIME_STOP same-bar priority; protective stop never moved intra-trade. |
| **Gross BE WR** | 33% — same as R3. |
| **Net BE burden** | ~51% MED / ~62% HIGH (without funding); ~45% MED / ~56% HIGH (with one-cycle ~0.17R funding accrual). Within empirical V1 / R3 / F1 win-rate band. |
| **Costs structurally dominate?** | NO — +2.0R target provides meaningful R-multiple room for cost absorption (winner net +1.47R at MED, +1.14R at HIGH). The §5.6 RR/target sanity review explicitly addressed this. |
| **Sample-size risk** | MODERATE — estimated R-window n=60–180 per symbol; per-fold n=10–30. Comparable to V1 / R3 / R1b-narrow band; below F1's 4700+. |
| **Target/stop/time-stop coherence** | HIGH — clean STOP > TARGET > TIME_STOP same-bar priority; 32-bar (= one funding cycle) unconditional time-stop with completed-bar discipline; no overlapping exit machinery. |
| **Fill timing / same-bar priority** | Standard next-bar-open fill; TIME_STOP triggers at close of bar `B+1+32` and fills at open of bar `B+1+33` (per first amendment §6.9 clarification). |
| **Timestamp / lookahead leakage risk** | **LOW (by spec)** — funding event used at signal must satisfy `funding_time ≤ bar_close_time`; trailing-90-day Z-score normalization excludes the current event. M1 displacement uses `fill_price` (not `close(B+1)`) per first amendment §10.1 correction. P.14 invariants enforced. **Note:** funding-event timestamp alignment is identified as an expected-failure-mode (§11 item 7); careful implementation will be required at any future Phase 3i-equivalent. |
| **Target-subset evidence misleading?** | **Risk identified and contained.** D1-A spec §10.3 frames M3 as descriptive PASS/FAIL/PARTIAL evidence; §13.3 verdict mapping has HARD REJECT supersede MECHANISM PASS, matching F1 precedent. Phase 3e §5.4 / §8.6 / Phase 3f §5.7 forbid target-subset rescues. The expected lower TARGET-exit fraction at +2.0R (5–20% vs F1's 33%) makes M3 evidence statistically thinner; the audit reinforces that TIME_STOP-subset behavior must be central in future diagnostics. |
| **Descriptive vs governing separation** | Clean — §13.1 explicitly states H0 / R3 are descriptive cross-family references for D1-A; §13.2 self-anchored absolute thresholds govern; M1 / M2 / M3 are descriptive mechanism evidence. |
| **Final verdict handled correctly?** | **N/A — spec only; not yet executed.** First-execution gate proposed (analogous to Phase 3c §7.2 F1 gate); §10.4 absolute floors and §11.6 = 8 bps HIGH per side preserved verbatim; operator-mandated BTC HIGH > 0 strengthening preserved; BTC HIGH PF > 0.30 made explicit at gate level (per first amendment §13). The verdict-handling discipline is structurally aligned with F1 / R2 precedent. |

---

## 4. Retrospective concerns triage

### 4.1 Concerns already safely contained by prior verdicts

These are concerns that the project's research framework has already handled correctly; no further action is needed.

1. **R1a's symbol-asymmetric mixed-PROMOTE.** Phase 2p §D's retained-research-evidence framing correctly prevented R1a from displacing R3 under §1.7.3 BTCUSDT-primary lock. The asymmetry was diagnosed (Phase 2o §C) as market-structure × strategy interaction, not a fixable rule defect.
2. **R1b-narrow's §10.3.a-on-both PROMOTE without genuine per-trade-expectancy gain.** Phase 2s §13 / Phase 2x §4.3 correctly framed the formal §10.3.a clearance vs the R3-anchor near-neutral marginal contribution. The methodological observation ("comparison-metric clearance can occur via trade-count concentration") is preserved in the family-review record.
3. **R2's §11.6 cost-sensitivity failure with M1+M3 mechanism PASS.** Phase 2w §16.3 correctly classified R2 as FRAMEWORK FAILED while preserving M1+M3 mechanism evidence as descriptive research. The "mechanism-supported subset is research evidence, not promotion" framing established the discipline that contained F1's later M3 PASS-isolated finding.
4. **F1's HARD REJECT despite M3 PASS-isolated.** Phase 3c §7.3 catastrophic-floor predicate correctly took precedence over M3 isolated subset evidence. Phase 3e §5.4 / §8.6 + Phase 3f §5.7 explicitly forbade F1-prime / target-subset rescues, closing the treadmill-risk loophole.
5. **R3's "less negative than H0" honest framing.** Phase 2l / 2p / 2x / 3a / 3e / 3f / 3g consistently note that R3's BTC R-window expR=−0.240 is an improvement over H0 but still negative. No phase has misrepresented R3's edge as positive aggregate.
6. **Phase 2y's §11.6 = 8 bps HIGH preservation.** Phase 2y closeout correctly resisted post-hoc threshold revision after R2's failure; preserved verbatim through Phase 3e / Phase 3f / Phase 3g. The framework calibration discipline is intact.

### 4.2 Concerns requiring documentation clarification only

These are concerns whose substance is correctly handled but where the documentation could be strengthened. **None of these block Phase 3g merge**; they are forward-looking observations.

1. **R/R / breakeven WR analysis was historically implicit.** Phase 2l / 2m / 2s / 2w / 3d-B2 reports cite empirical win rates and aggregate expR but do not explicitly compute the gross/net breakeven WR burden vs the empirical WR. The Phase 3g RR/target sanity review (§5.6) is the project's first formal cost-arithmetic-into-RR analysis. This audit's §6 future-spec checklist makes RR/breakeven analysis a mandatory pre-execution discipline.
2. **F1's M3 PASS-isolated arithmetic was descriptively correct but did not include explicit breakeven framing.** Phase 3d-B2 §11.3 reports the TARGET subset's aggregate +1149R BTC / +1398R ETH and means +0.75R / +0.87R, but does not frame these in cost-stack-vs-R-multiple terms. The Phase 3g audit retrospectively notes that F1's TARGET subset means correspond to a +2.0R-equivalent geometry only on a small subset; the wider population's cost-amplification was the binding HARD REJECT mechanism.
3. **Trade-count vs event-count distinction was historically implicit for V1 candidates.** V1 candidates fire on per-bar setup conditions; the per-bar vs per-setup-event count is naturally aligned. F1 used per-bar overextension events; per-bar vs per-event was also naturally aligned (each unique overextension event ≤ one entry). D1-A introduced a clear funding-event-vs-bar distinction (multiple 15m bars reference the same funding event); this was resolved in the first amendment §9.4 / §12 (funding-event-level funnel counters). Future strategy specs that introduce non-bar-level event sources should explicitly distinguish event-count from bar-count from the start.
4. **Time-stop fill discipline was historically implicit.** F1's 8-bar time-stop and R3's 8-bar time-stop both follow completed-bar discipline (close trigger → next-bar open fill) per Phase 3b §6 / Phase 2j §D, but the spec wording was less explicit than D1-A's first-amendment §6.9 update. Future specs should follow the D1-A §6.9 explicit framing.

### 4.3 Concerns that could affect future planning

These observations may inform any future phase but do not require action now.

1. **The cost-sensitivity gate is now the most consistent failure-mode signal.** R2 failed §11.6; F1 failed §10.4 + §11.6 catastrophically. Any future strategy candidate's pre-execution discipline must include explicit cost-resilience analysis before run authorization. The Phase 3g §5.6 RR/target sanity review and this audit's §6 future-spec checklist establish this discipline.
2. **TIME_STOP-subset behavior dominates the framework verdict for time-stop-anchored families.** R3 / F1 / D1-A all use unconditional time-stops; R3's time-stop is 8 bars (V1 framework), F1's is 8 bars, D1-A's is 32 bars (one funding cycle). The TIME_STOP-subset mean R is a primary determinant of per-trade expR for these candidates; future specs should require per-exit-reason expR diagnostics from the start.
3. **The R3 / R1a / R1b-narrow / R2 / F1 candidates all have BTC-and-ETH symmetric specifications.** D1-A is also symmetric. None of the project's candidates currently have BTC-only specifications; this preserves §11.4 ETH-comparison cleanliness and §1.7.3 primary-vs-comparison structure. Future BTC-only or asymmetric specifications would require explicit operator-policy review of §11.4 and §1.7.3 implications.
4. **Trade-frequency × per-trade-expR aggregation is a separate failure mode from sample-size risk.** F1 was statistically powerful (n=4720+) but catastrophically negative aggregate; R1b-narrow was statistically weak (n=10/12) but per-trade clean. These are orthogonal risks that must both be evaluated. The future-spec checklist makes this explicit.
5. **The project has not yet had a candidate that produces positive aggregate net-of-cost expR on BTCUSDT.** R3 is the strongest (BTC R-window expR=−0.240); all others are equal or worse. The aggregate-edge gap remains the binding challenge regardless of any single candidate's framework verdict. Future planning should be prepared for the possibility that the framework + locks + costs + market conditions may not currently support positive-aggregate-edge strategies on BTCUSDT — and that this is operator-strategic territory, not strategy-redesign territory.

---

## 5. Specific audit of the amended D1-A +2.0R spec

### 5.1 Confirm +2.0R is more structurally sane than +1.0R

**CONFIRMED.** Per the Phase 3g §5.6 RR/target sanity review:

- **Required-WR burden moderated meaningfully.** From 76.5% / 93.0% (MED / HIGH without funding) at +1.0R to 51% / 62% (MED / HIGH without funding) at +2.0R. With one-cycle funding accrual (~0.17R), the +2.0R burden moderates further to 45% / 56%.
- **Empirical WR comparison.** R3's BTC R-window WR=42.42% / ETH=33.33% sit just below the +2.0R MED breakeven (~51%); F1's BTC=33.05% / ETH=33.36% sit further below. A WR around 45–55% (the +2.0R MED-with-funding band) is challenging but within the project's empirical range, unlike +1.0R's 70%+ requirement which has never been observed.
- **Cost-stack absorption.** +2.0R produces winner net +1.47R at MED / +1.14R at HIGH; +1.0R produces +0.47R / +0.14R. The +2.0R absorption headroom is roughly 3× larger.
- **Structural alignment with cost-sensitivity thesis.** Phase 3f §3.6 / Phase 3g §3.6 motivated D1-A specifically as a candidate that *should address* R2's §11.6 cost-sensitivity failure. +1.0R sat in R2's failed small-R-multiple regime; +2.0R sits in R3's cost-robust regime. The amendment fixes a structural inconsistency between the spec and its motivation.
- **Non-fitting rationale.** +2.0R reuses R3's established Phase 2j §D / Phase 2p §C.1 convention; not selected on D1-A backtest evidence (no D1-A backtest has been run). The reuse is convention-driven, not fit-driven.

### 5.2 Confirm the 32-bar time-stop remains coherent with +2.0R

**CONFIRMED.** The 32-bar time-stop is not loosened or tightened by the target revision; both axes are preserved as separate non-fitting commitments:

- **32 bars = 1 funding cycle.** Anchored to Binance protocol fact (funding cycles every 8 hours; 8h / 15min = 32). Not fitted to any prior candidate's outcome.
- **+2.0R target is reachable but not certain within 32 bars.** A 2.0 × ATR(20) move in 32 × 15m bars is empirically not trivial; estimated TARGET-exit fraction 5–20% (per Phase 3g §5.6.5 tradeoff analysis; descriptive only). Most trades will exit at TIME_STOP at intermediate R-multiples (~+0.3 to +0.8R reversion).
- **TIME_STOP catches partial reversions; +2.0R catches outsized reversions.** This is the same RR architecture as R3 (whose BTC R3 R-window TARGET fraction was ~12% with ETH ~15%; bulk exits at TIME_STOP). The 32-bar / +2.0R combination produces an analogous distributional shape, scaled to D1-A's funding-cycle horizon.
- **No coherence issue identified.** The hold horizon and target magnitude are independently committed; their interaction (most trades exit at TIME_STOP; few reach TARGET) is the natural framework geometry, not a flaw.

### 5.3 Confirm TIME_STOP outcomes must be central in future diagnostics

**CONFIRMED.** Per §3.7 / §4.3 above, the TIME_STOP-subset mean R is a primary determinant of per-trade expR for time-stop-anchored families. For D1-A specifically:

- **Expected exit-reason mix:** STOP fraction ~50–55% (similar to F1); TARGET fraction ~5–20%; TIME_STOP fraction ~25–45%.
- **Per-exit-reason expR diagnostics are mandatory at any future first execution.** Phase 3g §12 §17 lists "per-exit-reason fractions"; this audit reinforces that **per-exit-reason mean R / aggregate R must also be computed and reported**, not just the fractions.
- **TIME_STOP mean R will likely drive the framework verdict.** If TIME_STOP exits are systematically near-flat or slightly negative (e.g., mean ~0 to −0.3 R), per-trade expR could remain negative even with a clean TARGET subset. This is exactly Phase 3g §11 expected-failure-mode item 13.
- **Recommendation for any future Phase 3h / 3i / 3j:** mandatory diagnostic to include `mean_R_by_exit_reason` and `aggregate_R_by_exit_reason` per symbol, in addition to the existing exit-reason fraction breakdown. This enables the operator to see whether a HARD REJECT verdict is driven by STOP-subset losses, TIME_STOP-subset near-flat exits, or absent TARGET-subset positive contribution — all three failure modes are distinguishable from the per-exit-reason diagnostics.

### 5.4 Confirm no target sweep or D1-prime should be proposed

**CONFIRMED.** The amendment locks +2.0R singularly per Phase 2j §C.6 / §11.3.5 single-spec discipline. Per Phase 3g §14 (overfitting risk):

- **No target sweep authorized.** The +2.0R value is locked; revisiting it post-execution under any outcome is forbidden post-hoc loosening per Phase 2f §11.3.5.
- **No D1-prime authorized.** Any future regime-conditional, asymmetric, or filter-overlay variant of D1-A would require a separately-authorized Phase 3a-style discovery memo + Phase 3b/3g-style spec memo with an independently-developed hypothesis. Phase 3g does not authorize D1-prime.
- **No retroactive TARGET-subset selection rescue.** Phase 3e §5.4 / §8.6 + Phase 3f §5.7 prohibitions on F1-target-subset rescue apply by analogy to D1-A. If D1-A's M3 PASSES while §10.4 / §11.6 fails, the verdict is FRAMEWORK FAIL or HARD REJECT; no D1-A-prime via target-subset selection is automatically authorized.
- **No "let's also test +1.0R for completeness" framing.** A future researcher proposing a sweep across +1.0R / +1.5R / +2.0R / +3.0R targets would be exactly the post-hoc-loosening / parameter-sweep pattern the §11.3.5 binding rule forbids. The §5.6 Option A decision is the pre-declared single-spec target value.

---

## 6. Future spec checklist

This checklist is informed by the V1-family + F1 retrospective and the D1-A RR sanity review. It is forward-looking guidance for any future operator-authorized strategy-family spec memo (Phase 3a-style discovery, Phase 3b / 3g-style spec, etc.). The checklist is **non-binding on existing candidates** (whose verdicts stand) and **does not authorize any future phase** (each phase requires separate operator authorization).

A new strategy-family spec memo should explicitly address each of the following before requesting any execution-planning authorization:

### 6.1 RR / breakeven math before costs

State the conceptual target / stop ratio explicitly (e.g., "+2.0R / −1.0R"). State the gross-breakeven win-rate (1 / (1 + RR)) before any costs. Identify whether the gross BE WR is naturally compatible with the empirical V1 / R3 / F1 win-rate band (21–42%) or whether it requires a substantially higher win rate.

### 6.2 RR / breakeven math after LOW / MED / HIGH costs

Compute the net winner R and net loser R after the project's cost-stack at LOW (1 bps/side slip + 0.0005 fee), MED (3 bps/side), HIGH (8 bps/side per the §11.6 = 8 bps preservation). Compute the net-cost breakeven win-rate at each slippage level. Compare to empirical V1 / R3 / F1 win rates. **If the HIGH net BE WR exceeds 65%, the spec must include an explicit non-fitting argument for why the strategy can plausibly produce that win rate**, or the spec is structurally weak and should reconsider the target/stop design.

### 6.3 Funding-accrual realism if applicable

If the strategy's hypothesis depends on funding accrual (D1-A) or routinely accrues funding due to long hold times, state the expected funding contribution per trade in R-multiples explicitly. Acknowledge funding-accrual uncertainty (partial-cycle holds, sign reversals, regime shifts). State whether the breakeven WR after costs *with* funding is materially different from the breakeven WR after costs *without* funding; if the spec depends on funding to clear breakeven, that dependence must be explicit and falsifiable (an M2-style mechanism check).

### 6.4 Sample-size estimate

State the expected R-window n per symbol and per-fold n at the baseline parameter setting. Compare to V1 / R3's 33-trade R-window n and F1's 4720+ R-window n. Identify whether the sample size is statistically credible for §10.3 / §11.2 fold-consistency evaluation (typical band: 25–200 trades per R-window per symbol; below 15 is fragile, above 1000 raises trade-frequency × per-trade-expR aggregation concerns).

### 6.5 Target reachability estimate

If the spec uses a fixed R-multiple target (e.g., +2.0R) with a finite time-stop, estimate the expected TARGET-exit fraction. Compare to R3 (~12–15%) and F1 (~33% at SMA(8) target). State whether the bulk of exits will be STOP / TARGET / TIME_STOP / END_OF_DATA. **If TARGET-exit fraction is expected below 5%, the M3 mechanism check becomes statistically thin and the spec should reconsider** target / time-stop balance.

### 6.6 Event-count vs bar-count distinction

If the strategy fires on a non-bar-level event source (funding events, news events, on-chain events, etc.), explicitly distinguish event-count from bar-count from the start. Funnel counters must be at the event level, not the bar level. Phase 3g first-amendment §9.4 / §12 funding-event-level funnel counters are the precedent. This avoids inflating "detected" counts when multiple bars reference the same upstream event.

### 6.7 Fill timing

State the entry fill timing convention (e.g., "market entry at next-bar open after confirmed signal close"). Confirm consistency with V1 framework precedent. Identify any fill-timing edge cases (e.g., signal at last bar of session; signal coincident with funding event; signal during data gap) and state how the engine should handle them.

### 6.8 Same-bar priority

State the same-bar exit precedence (e.g., "STOP > TARGET > TIME_STOP" per R3 / F1 / D1-A). Confirm the spec uses TARGET (not TAKE_PROFIT) for non-V1 families to avoid V1-multi-stage exit-reason confusion.

### 6.9 Timestamp leakage

State the timestamp discipline explicitly: signal evaluation at completed bar close; rolling-window features computed up to (not including) current event; higher-timeframe alignment using most recent completed bar. Identify any non-bar-level timestamp dependencies (funding settlement times, exchange announcement times, etc.) and state the no-lookahead invariant.

### 6.10 Target-subset fallacy

Anticipate the M3-style TARGET-subset PASS / FAIL outcomes explicitly. State that M3 PASS-isolated does NOT promote the strategy if §10.4 absolute floors or §11.6 cost-sensitivity gate fails on the wider trade population. Forbid retroactive TARGET-subset rescue in the spec itself (Phase 3e §5.4 / §8.6 / Phase 3f §5.7 / Phase 3g §14 precedent).

### 6.11 Descriptive vs governing evidence

Explicitly identify which metrics govern the first-execution gate (e.g., self-anchored absolute thresholds at MED / HIGH cells) and which metrics are descriptive (M1 / M2 / M3 mechanism PASS/FAIL/PARTIAL; H0 / R3 / F1 cross-family deltas). Phase 3c §7.4 / Phase 3d-B2 §15 / Phase 3g §13 precedent. Mixing descriptive and governing evidence in the verdict mapping is forbidden.

### 6.12 Explicit hard-reject floors

State the §10.4-style absolute floors verbatim: `expR > −0.50 AND PF > 0.30` per symbol per MED / HIGH cell on MARK_PRICE. State that any catastrophic violation triggers HARD REJECT regardless of mechanism evidence (Phase 3c §7.3 catastrophic-floor predicate; F1 / D1-A precedent). If the operator-mandated BTC HIGH expR > 0 strengthening (Phase 3c §7.2(iv)) applies, state it explicitly. If a §10.4-style PF floor at the BTC HIGH gate-level is implied (per Phase 3g first amendment §13.2 explicit framing), state it explicitly.

---

## 7. Final recommendation

### 7.1 Phase 3g safe to merge

**YES.** The Phase 3g spec memo (with both amendments — five spec-consistency corrections + RR/target sanity Option A revision to +2.0R) is methodologically sound. The audit finds:

- The amended D1-A spec is structurally consistent with the Phase 3f / Phase 3g cost-sensitivity thesis (§5.1 confirmed).
- The 32-bar time-stop is coherent with the +2.0R target (§5.2 confirmed).
- TIME_STOP-subset diagnostics are clearly documented as central for future execution (§5.3 confirmed).
- No target sweep or D1-prime is authorized; single-spec discipline is preserved (§5.4 confirmed).
- Retrospective concerns (§4.1) are already safely contained by prior verdicts; documentation-clarification concerns (§4.2) do not block merge.
- Future-spec checklist (§6) provides forward-looking guidance for any subsequent operator-authorized strategy spec; not a Phase 3g blocker.

### 7.2 No additional docs-only amendment required before merge

**CONFIRMED.** The audit identifies no further blocking issue requiring a third Phase 3g amendment. The two existing amendments (`97085d9` five-fix; `5817cbb` RR/target sanity Option A) plus the original spec commit (`2c3a91b`) and closeout-backfill commits (`e439c6b`, `7dfa596`, `01bd227`) constitute the complete Phase 3g delivery.

This methodology sanity audit is itself a docs-only addition. It is a retrospective methodology audit, not a spec amendment; it does not change any locked axis or threshold in the D1-A spec. The audit and the closeout's reference to it are appended to the branch as a separate commit; the spec memo itself is not further modified.

### 7.3 Phase 3h remains only a future operator decision

**CONFIRMED.** Phase 3g recommends GO (provisional) for a future Phase 3h execution-planning memo for D1-A with target +2.0R, contingent on operator authorization. **Phase 3g does not authorize Phase 3h.** Phase 3h requires a separately-authorized operator decision.

The recommended next operator decision after Phase 3g merge remains:

1. Authorize Phase 3h (D1-A execution-planning memo, Phase-3c-style) — Phase 3g primary recommendation.
2. Remain paused per Phase 3e §9 / Phase 3f §8 default.
3. Authorize an alternative direction (D7 external cost-evidence review per Phase 3f §7.7) or any other operator-driven docs-only direction.

Phase 3g — with both amendments and this methodology sanity audit — terminates at the spec memo. No execution, implementation, paper/shadow, Phase 4, live-readiness, or deployment authorization follows automatically.

---

**End of Phase 3g methodology sanity audit.** Cross-strategy matrix produced for H0 / R3 / R1a / R1b-narrow / R2 / F1 / amended-D1-A. Per-candidate methodological assessment confirms all prior verdicts are correctly handled and contain the structural concerns (R1a symbol-asymmetry; R1b-narrow comparison-metric-via-concentration; R2 §11.6 slippage-fragility; F1 catastrophic-floor + target-subset-rescue prohibition). Amended D1-A +2.0R is structurally sane and aligned with R3's non-fitting project convention. Future-spec checklist documents 12 mandatory pre-execution disciplines for any subsequent strategy-family spec. **Phase 3g safe to merge.** No additional docs-only amendment required. Phase 3h remains only a future operator decision. R3 baseline-of-record / H0 framework anchor / R1a-R1b-narrow-R2-F1 retained-research-evidence preserved verbatim. F1 HARD REJECT preserved; Phase 3d-B2 terminal for F1 preserved. §11.6 = 8 bps HIGH per side preserved verbatim. §1.7.3 locks preserved verbatim. No paper/shadow, no Phase 4, no live-readiness, no deployment, no implementation, no execution, no backtest, no parameter tuning, no threshold change, no project-lock change, no MCP / Graphify / `.mcp.json`, no credentials, no `data/` commits, no code change. No next phase started. Awaiting operator review.
