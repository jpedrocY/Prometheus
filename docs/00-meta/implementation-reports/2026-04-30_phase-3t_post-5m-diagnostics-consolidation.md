# Phase 3t — Post-5m Diagnostics Consolidation and Research Thread Closure Memo (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); Phase 2x family-review memo; Phase 2y slippage / cost-policy review; Phase 2w §16.1 (R2 FAILED — §11.6 cost-sensitivity blocks); Phase 3d-B2 (F1 HARD REJECT); Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3k post-D1-A research consolidation; Phase 3l external execution-cost evidence review; Phase 3m regime-first research framework memo; Phase 3n 5m timeframe feasibility memo; **Phase 3o 5m diagnostics-spec memo (Q1–Q7 predeclared); Phase 3p 5m diagnostics data-requirements + execution-plan memo; Phase 3q 5m data acquisition + integrity validation; Phase 3r mark-price gap governance memo (§8 Q6 invalid-window exclusion rule); Phase 3s 5m diagnostics execution (Q1–Q7 once)**; `docs/04-data/data-requirements.md`; `docs/04-data/timestamp-policy.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/12-roadmap/phase-gates.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 3t — Docs-only **post-5m-diagnostics consolidation and research-thread closure memo.** Records what the 5m research thread (Phases 3o → 3p → 3q → 3r → 3s) taught the project, what it explicitly did not teach, and why the correct project state remains paused. **No diagnostics. No backtests. No strategy rescue. No implementation. No data acquisition. No data modification. No manifest modification. No verdict revision. No threshold revision. No project-lock revision. No 5m strategy / hybrid / variant proposal. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work.**

**Branch:** `phase-3t/post-5m-diagnostics-consolidation`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim. Recommendation is provisional and evidence-based; the operator decides.

---

## 1. Summary

The 5m research thread (Phases 3o → 3p → 3q → 3r → 3s) is **operationally complete**. Across the five phases, the project:

1. **Phase 3o** — predeclared the diagnostic question set Q1–Q7, the forbidden rescue-shaped question forms, the diagnostic-term definitions, the data-boundary rules, the timestamp / leakage guardrails, the allowed-vs-forbidden analysis boundary, the per-strategy diagnostic mapping, the required outputs, and the stop conditions, **before any 5m data existed in the repository**.
2. **Phase 3p** — converted the predeclared question set into a concrete *future* diagnostics plan: exact 5m data requirements (BTC + ETH 5m trade-price klines, 5m mark-price klines; strict v002 date-range superset coverage; UTC ms timestamps; canonical schema; public Binance endpoints, no credentials); recommended supplemental v001-of-5m versioning over a v003 family bump; specified the manifest + integrity-check evidence required; specified per-question diagnostic outputs; and **predeclared per-question outcome-interpretation rules (informative / non-informative / ambiguous thresholds)** before any 5m data existed.
3. **Phase 3q** — physically acquired the four supplemental v001-of-5m dataset families (51 monthly archives × 4 families = 204 archives) from public unauthenticated `data.binance.vision` bulk endpoints, with strict superset coverage of the v002 retained-evidence trade range. **Verdict — partial pass:** trade-price 5m datasets PASS Phase 3p §4.7 strict integrity gate (446 688 bars each; 0 gaps); mark-price 5m datasets FAIL strict gate due to 4 known upstream Binance maintenance-window gaps each (the same gap pattern verified to be present in locked v002 mark-price 15m datasets). No forward-fill, interpolation, imputation, or §4.7 relaxation applied. Mark-price manifests record `research_eligible: false` and `invalid_windows` verbatim.
4. **Phase 3r** — formalized the mark-price gap governance: Phase 3p §4.7 strict integrity gate stays unchanged; mark-price 5m datasets remain `research_eligible: false`; Phase 3q manifests are not modified. **Phase 3r §8 Q6 invalid-window exclusion rule** specified: known invalid windows are exclusion zones, not patch zones; per-trade exclusion test based on Q6 analysis-window intersection; excluded counts reported; Q6 conclusions labeled "conditional on valid mark-price coverage"; no automatic prior-verdict revision; no strategy rescue, parameter change, or live-readiness implication; no silent §8 rule revision.
5. **Phase 3s** — executed the predeclared Q1–Q7 question set **exactly once** on the v002-locked retained-evidence trade populations (R3, R2, F1, D1-A; R-window MEDIUM-slip canonical runs; 10 031 trades total: 4 974 BTC + 5 057 ETH), using the Phase 3q v001-of-5m supplemental datasets, applying the Phase 3r §8 Q6 invalid-window exclusion rule verbatim. Q1, Q2, Q3 (+1R), Q6 (D1-A only), and Q7 meta classified informative; Q4 and Q5 classified non-informative; Q3 +2R ambiguous. Phase 3r §8 zero exclusions empirically.

The thread produced four informative descriptive findings (Q1 universal entry-path adverse bias; Q2 V1-family-vs-F1/D1A stop pathology differentiation; Q3 +1R intrabar-touch frequency in adverse-exit trades; Q6 D1-A mark-stop lag) and two non-informative findings (Q4 D1-A funding-decay non-monotone with SEM > magnitude; Q5 fill realism within ±8 bps of cost assumption). **All four informative findings are descriptive only** and bound by Phase 3o §6 forbidden question forms, Phase 3o §10 analysis boundary, Phase 3p §8 critical reminders, and Phase 3r §8 binding constraints. **None licenses verdict revision, parameter change, threshold revision, project-lock revision, strategy rescue, 5m strategy / hybrid / variant proposal, paper/shadow planning, Phase 4, live-readiness, deployment, or any successor authorization.**

**Phase 3t recommends remain paused as primary.** The 5m research thread has reached its operational endpoint. No actionable strategy candidate emerged. No new implementation-grade hypothesis emerged. No path to rescue R2 / F1 / D1-A emerged. No path to revise §11.6 emerged. No path to revise mark-price stop policy emerged. No path to authorize a 5m strategy layer emerged. The project's correct state is paused; running anything further would either repeat existing diagnostics on alternative populations (low marginal value) or extend into territory forbidden by predeclared rules (high risk).

---

## 2. Authority and boundary

Phase 3t operates strictly inside the post-Phase-3s boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5 (Q1–Q7 question set), §6 (forbidden question forms), §7 (diagnostic-term definitions), §10 (allowed-vs-forbidden analysis boundary). Phase 3p §4–§8 (data requirements, dataset versioning, manifest specification, per-question outputs, outcome-interpretation rules). Phase 3r §8 (Q6 invalid-window exclusion rule).
- **Phase 3s diagnostic outputs preserved verbatim.** Q1, Q2, Q3 (+1R), Q6 (D1-A only), Q7 informative; Q4, Q5 non-informative; Q3 +2R ambiguous. Phase 3r §8 zero exclusions. The Phase 3s report and JSON tables are committed and immutable.
- **Project-level locks preserved verbatim.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 (Δexp ≥ +0.10 R), §10.4 (absolute floors), §11.3 (V-window no-peeking), §11.4 (ETH non-catastrophic), §11.6 (8 bps HIGH per side cost-resilience).
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **v002 dataset provenance preserved.** v002 partitions and manifests untouched.
- **Phase 3q v001-of-5m manifest provenance preserved.** Mark-price 5m datasets remain `research_eligible: false`. Trade-price 5m datasets remain `research_eligible: true`.

Phase 3t adds *consolidation language* — a closure narrative that integrates the five-phase thread into a single readable record — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, or any lock.

---

## 3. Starting state

```text
branch:           phase-3t/post-5m-diagnostics-consolidation
parent commit:    4f96c81e824bc268b6d32783c295f6320e60fb99 (post-Phase-3s housekeeping)
working tree:     clean
main:             4f96c81e824bc268b6d32783c295f6320e60fb99 (unchanged)
Phase 3s branch:  pushed to origin at a93695f (Phase 3s closeout); commits already on main via Phase 3s merge
Phase 3r branch:  pushed at 0611195; commits on main via Phase 3r merge
Phase 3q branch:  pushed at 3078b44; commits on main via Phase 3r merge
```

No code under `src/prometheus/` modified by Phase 3t. No script under `scripts/` modified by Phase 3t. No `data/` artefact modified by Phase 3t. No prior-phase report modified by Phase 3t.

---

## 4. Why this memo exists

Phase 3t exists for **four** reasons:

1. **Closure.** The 5m research thread spans five phases (Phases 3o → 3p → 3q → 3r → 3s). Without a single consolidation memo, the closure narrative is fragmented across five separate closeouts. Phase 3t produces the unified record.
2. **Anti-rescue procedural fortification.** The Phase 3s findings are *informative-but-not-actionable* by predeclared rule. The risk of "informative findings drifting into action" is real and well-documented in Phase 3o §6 / Phase 3p §8 / Phase 3r §8. Phase 3t reaffirms the non-actionability discipline in a single readable place — both for the current operator and for any future operator who reads the project record without the recent context.
3. **Pre-emption of rescue narratives.** Phase 3o §6 forbidden question forms include "Which 5m entry offset would have made F1 profitable?", "Which 5m exit rule rescues D1-A?", "Which intrabar target touch rule maximizes R?", "Which 5m threshold makes R2 pass §11.6?", "Which 5m filter makes losing trades disappear?". The Phase 3s findings (especially Q3 +1R intrabar touches at 25–48% in adverse-exit trades, and Q1 universal IAE > IFE) are exactly the kind of evidence that *could* be misread as rescue licence. Phase 3t pre-empts that misreading by stating the non-actionability discipline forcefully and in one place.
4. **Future-research-validity criteria.** When the operator eventually decides whether to authorize any further research, they will need a clear written record of what would constitute a *valid* future research path versus a *forbidden* post-hoc loosening. Phase 3t records those criteria.

---

## 5. 5m thread recap

### 5.1 Phase 3o — Diagnostics-spec memo (predeclaration)

Predeclared:

- **Q1–Q7 question set** with per-question definitions of what would count as informative vs non-informative.
- **Five forbidden rescue-shaped question forms** (entry-offset rescue; exit-rule rescue; target-touch maximize-R; §11.6 threshold rescue; filter-out-losers).
- **13 diagnostic-term definitions** (immediate adverse / favorable excursion; first-5m return; max excursion; wick-stop / sustained-stop event; intrabar / confirmed target touch; target-touch-then-stop; funding decay curve; fill-assumption slippage proxy; mark/trade stop divergence).
- **Data-boundary rules** (no 5m data exists in v002; no v003 created; no diagnostics execution authorized).
- **Timestamp / leakage guardrails** (UTC ms canonical; no partial bars; explicit 5m / 15m alignment; no using 5m data before 15m decision timestamp; no target/stop path facts used to define entry filters; no lookahead from future 5m sub-bars into entry decisions).
- **Allowed-vs-forbidden analysis boundary** (allowed: descriptive Q-answers and tables, predeclared interpretations, classification per Phase 3p §8; forbidden: strategy evaluation, parameter tuning, threshold revision, candidate rescue, prior-verdict revision).

Recommendation: remain paused. No data acquisition, no diagnostics execution authorized.

### 5.2 Phase 3p — Data-requirements and execution-plan memo

Built on Phase 3o by predeclaring the operational specification:

- **Data requirements:** BTC + ETH 5m trade-price klines, 5m mark-price klines; strict v002 date-range superset coverage; UTC ms timestamps; canonical schema; public Binance endpoints; no credentials.
- **Versioning approach:** Phase 3p Option B — supplemental v001-of-5m alongside v002 (recommended over a v003 family bump for cleanest v002 verdict-provenance preservation).
- **Manifest + integrity-check evidence specification:** required fields per `dataset-versioning.md`; required `quality_checks` fields including `gaps_detected`, `gap_locations`, `monotone_timestamps`, `boundary_alignment_violations`, `close_time_consistency_violations`, `ohlc_sanity_violations`, `volume_sanity_violations`, `symbol_consistency_violations`, `interval_consistency_violations`, `date_range_coverage`, `coverage_required_first_open_time_ms`, `coverage_required_last_open_time_ms`, `research_eligible`.
- **Per-question diagnostic outputs:** Q1 IAE / IFE distributions; Q2 wick / sustained / indeterminate counts; Q3 intrabar / confirmed target-touch flags + adverse-exit context; Q4 D1-A funding-decay curve at {5, 10, 15, 30, 60} min; Q5 fill-realism distribution; Q6 mark-vs-trade timing differences; Q7 meta classification.
- **Per-question outcome-interpretation rules** (predeclared *before* any 5m data existed): Q4 informative requires monotone decay with SEM tighter than displacement; Q5 informative requires |signed mean| > 8 bps with replicability; Q3 critical reminder that even informative outcome cannot license rule revision; Q7 meta requires ≥ 3 of Q1–Q6 informative, and a non-informative Q7 *strengthens* remain-paused.

Recommendation: remain paused. No data acquisition, no diagnostics execution authorized.

### 5.3 Phase 3q — 5m data acquisition + integrity validation

Acquired the four supplemental v001-of-5m dataset families (Phase 3p Option B) from public unauthenticated `data.binance.vision` bulk endpoints. 51 monthly archives × 4 families = 204 archives, all SHA-256 verified, all written to canonical Parquet partitions matching v002 conventions.

**Integrity-check verdict:**

| Dataset | Bars | Gaps | Other checks | `research_eligible` |
|---|---|---|---|---|
| `binance_usdm_btcusdt_5m__v001` | 446 688 | 0 | all PASS | **true** |
| `binance_usdm_ethusdt_5m__v001` | 446 688 | 0 | all PASS | **true** |
| `binance_usdm_btcusdt_markprice_5m__v001` | 445 819 | **4** | all PASS | **false** |
| `binance_usdm_ethusdt_markprice_5m__v001` | 446 106 | **4** | all PASS | **false** |

The four mark-price gap windows are upstream Binance maintenance-window characteristics; the same four windows are verified to be present in the locked v002 mark-price 15m datasets. No forward-fill, no interpolation, no imputation, no §4.7 relaxation. Mark-price manifests honestly record `research_eligible: false` and `invalid_windows` verbatim.

Recommendation: stop for operator review (per Phase 3q brief failure path).

### 5.4 Phase 3r — Mark-price gap governance memo

Adopted **Option B (known-invalid-window exclusion for Q6 only)** as the formally adopted governance posture:

- Phase 3p §4.7 strict integrity gate stays unchanged.
- Mark-price 5m datasets remain `research_eligible: false`.
- No data is patched, forward-filled, interpolated, imputed, or replaced.
- Phase 3q manifests are not modified.

**Phase 3r §8 Q6 invalid-window exclusion rule** specified the full normative rule that any future Q6-running phase must obey:

1. Known invalid windows are exclusion zones, not patch zones.
2. No forward-fill, interpolation, imputation, replacement, synthetic mark-price, or mark-price reconstruction from trade-price.
3. Per-trade exclusion test based on Q6 analysis-window intersection.
4. Excluded trades counted and reported by candidate / symbol / side / exit-type / gap-window.
5. Q6 conclusions labeled "conditional on valid mark-price coverage."
6. No automatic prior-verdict revision.
7. No strategy rescue, parameter change, or live-readiness implication.
8. No silent §8 rule revision.
9. Per-trade exclusion algorithm must be predeclared in the diagnostics-execution phase brief.

Q6 disposition: bounded-conditional optionality. Q6 stays on the menu but only as a §8-bounded option. Q6 not currently authorized.

Recommendation: remain paused.

### 5.5 Phase 3s — Q1–Q7 execution

Executed the predeclared question set exactly once on the v002-locked retained-evidence trade populations:

| Population | Run | BTC trades | ETH trades |
|---|---|---|---|
| R3 | `phase-2l-r3-r/2026-04-29T03-11-42Z` | 33 | 33 |
| R2 | `phase-2w-r2-r2_r3-r/2026-04-27T11-25-07Z` | 23 | 19 |
| F1 | `phase-3d-f1-window=r-slip=medium/2026-04-29T03-12-14Z` | 4 720 | 4 826 |
| D1-A | `phase-3j-d1a-window=r-slip=medium/2026-04-29T03-22-26Z` | 198 | 179 |
| **TOTAL** | | **4 974** | **5 057** |

10 031 retained-evidence trades augmented with 5m-resolution path attributes. No backtest run. No retained-evidence trade population regenerated. Phase 3r §8 exclusion rule applied verbatim — zero trades excluded empirically.

**Q1–Q7 verdicts:**

| Q | Verdict | Headline |
|---|---|---|
| Q1 | Informative | IAE > IFE in 7 of 8 cells; F1 ~0.5 R adverse in first 5 min. |
| Q2 | Informative | V1-family wick-fraction 0.571–1.000 vs F1/D1-A 0.269–0.347. |
| Q3 (+1R) | Informative | 6 of 8 cells ≥ 25%; **descriptive-only** per §8.3 / §6.3. |
| Q3 (+2R) | Ambiguous | All cells well below typical informativeness. |
| Q4 | Non-informative | No monotone decay; SEM > magnitude. |
| Q5 | Non-informative | No |signed| > 8 bps cell. §11.6 unchanged. |
| Q6 | Informative for D1-A only | D1-A mark lags trade by ~1.3–1.8 5m bars. |
| Q7 | Informative | 4 of 6 ≥ 3-threshold met. |

Recommendation: remain paused.

---

## 6. What Phase 3s answered

The four originally-unresolved strategic questions (per Phase 3n §3 framing) now have Phase-3p-§8-bounded answers:

### 6.1 Are we missing useful timing information inside 15m bars?

**Answer: yes, descriptively.**

- **Q1** confirmed: completed-15m-bar entries hide a consistent first-5min adverse path bias across all four candidates. F1 most pronounced (~0.5 R consumed in first 5 min). The pattern increases monotonically through IAE_2 (~0.6–0.7 R) and IAE_3 (~0.7–0.8 R) for F1; smaller magnitude but same direction for R3, R2, D1-A.
- **Q2** confirmed: stop-trigger pathology differentiates V1-family (wick-dominated) from F1 / D1-A (sustained-dominated). The differential is mechanistically meaningful — V1-family stops sit in a wick-vulnerable zone; F1 / D1-A stops trigger because the contrarian thesis didn't materialize in time.
- **Q3** confirmed: +1R intrabar touches occur in 25–48% of adverse-exit trades across 6 of 8 cells. The +2R touch rate is uniformly low. Path richness exists at 5m granularity that is invisible at 15m granularity.

**Critical: the timing information is descriptive only.** It cannot be acted on as a strategy signal layer (Phase 3o §4.1 / Phase 3p §10 prohibition); it cannot license entry-rule modification, exit-rule modification, stop-rule modification, or any retained-evidence candidate revision (Phase 3p §8 critical reminders); it cannot license a 5m strategy or hybrid (Phase 3o §6 forbidden question forms). It updates *operator understanding* of the post-15m-entry market behavior; it does not update *action*.

### 6.2 Can regimes be defined cleanly before testing?

**Answer: not answered by Phase 3s; still risky.**

Phase 3s did not test regime-classification questions — they were not part of the predeclared Q1–Q7 question set. The Q2 stop-pathology differential (V1-family wick vs F1/D1-A sustained) suggests a *candidate-family-conditional* structural pattern, but this is descriptive at the candidate level, not at a regime level.

Phase 3m's regime-first framework memo discipline (regimes defined first from first principles; no rescue framing; no winning-fold-derived regimes; no TARGET-exit-conditional labels; falsifiable + stable) was not exercised in Phase 3s. The risk of "let's define a regime that retroactively fits the Q2 differential" is exactly the kind of post-hoc loosening Phase 2y §11.3.5 forbids — and Phase 3m §11.3.5-style discipline forbids in the regime-first context.

**Phase 3t recommends remain paused on regime-first work.** Any future regime-first phase would need the operator to re-evaluate Phase 3m's "remain paused" recommendation with full awareness of Phase 3s findings — and would still be subject to the anti-circular-reasoning preconditions Phase 3m specified.

### 6.3 Would more granular data help diagnostics, or just increase noise/cost?

**Answer: 5m helped diagnostically; finer-than-5m is not justified.**

Phase 3s produced 4 informative classifications out of 6 (Q1 / Q2 / Q3 / Q6) plus an informative Q7 meta-classification. That is a non-trivial information yield from a single 5m diagnostics-execution pass.

However, two of the six (Q4 / Q5) failed informative thresholds despite being mechanism-relevant. Q4's failure (no monotone D1-A funding-decay shape with SEM-vs-magnitude failure) is consistent with funding-extreme effects being either too small to detect at 5m granularity or too heterogeneous across events. Q5's failure (no |signed| > 8 bps cell) is consistent with Phase 3l's "B — conservative but defensible" assessment.

Sub-minute or tick data would likely:
- Add noise to Q4 (more bars per event but no additional signal-to-noise ratio gain).
- Add noise to Q5 (sub-5m fill simulation introduces more cross-trade variance without changing the 8-bps-bound mean).
- Not improve Q1 / Q2 / Q3 / Q6 materially — those findings are robust at 5m granularity.
- Add operational overhead (data acquisition complexity; storage; integrity-check governance) without offsetting analytical benefit.

**Phase 3t does NOT recommend authorizing finer-than-5m data acquisition.** The 5m data already in the repository is sufficient for any plausible future diagnostic question, subject to that question being independently authorized and bound by Phase 3o / 3p / 3r predeclaration discipline.

### 6.4 Is there a truly new hypothesis strong enough to deserve implementation?

**Answer: no.**

The four informative findings are *mechanism-informative descriptive* evidence:

- **Q1:** Universal entry-path adverse bias. Tells us *what happens* but not *what to do* — the prohibition on 5m strategy layer (Phase 3o §4.1) and the prohibition on entry-rule modification (Phase 3o §6 / §10) prevent action.
- **Q2:** Stop-pathology differentiation. Tells us *why* each candidate failed but does not provide a *fix* — stop widening is forbidden categorically (`.claude/rules/prometheus-safety.md`); mark-price stop policy is locked (§1.7.3); changing stop placement would require a new strategy spec with predeclared evidence thresholds (which Phase 3s does not contemplate).
- **Q3:** +1R intrabar touches. Tells us *some adverse-exit trades briefly reached profit levels* but cannot become an exit rule (Phase 3o §6.3 forbidden question form; Phase 3p §8.3 critical reminder).
- **Q6 (D1-A):** Mark-stop lag. Tells us *mark-price triggers later than trade-price* for D1-A but cannot license stop-policy revision (§1.7.3 locked; mark-price stops mandatory).

A *strategy candidate* requires a complete entry / target / stop / time-stop / cooldown specification *plus* predeclared evidence thresholds *plus* walk-forward validation *plus* §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gate compliance. None of the four informative findings constitutes such a candidate, and Phase 3o §6 explicitly forbids attempting to convert any of them into one through post-hoc analysis.

**Phase 3t does NOT recommend any new strategy candidate, hybrid, variant, or successor proposal.**

---

## 7. What Phase 3s did not answer

For completeness, this section records the questions Phase 3s explicitly *did not* address:

- **Regime classification.** Out of scope for Q1–Q7. Phase 3m's remain-paused recommendation stands.
- **ML feasibility.** Out of scope. Phase 3k / Phase 3m / Phase 3n / Phase 3o all left ML feasibility unauthorized; Phase 3s did not change that.
- **Cost-model revision (§11.6 amendment).** Out of scope for Phase 3s; Phase 3l's "B — conservative but defensible" assessment stands. Q5 confirmed §11.6 holds at 5m granularity.
- **D1-A successor specification.** Phase 3o / 3p / 3r explicitly did not contemplate D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid. Phase 3s did not propose any.
- **Sub-period stability of the Q1–Q7 findings.** Phase 3s computed each statistic on the full retained-evidence trade population. A formal sub-period split would require a separately authorized phase with predeclared methodology.
- **Walk-forward stability of any potential rule derivable from the findings.** Phase 3o §6 and Phase 3p §8 forbidden question forms / critical reminders explicitly preclude attempting to derive any rule from the findings, so walk-forward stability is moot — the rule cannot be derived, so its stability cannot be tested.
- **Cross-slip-variant Q1 / Q2 / Q3 stability.** Phase 3s used MEDIUM-slip canonical runs. R-window LOW and HIGH slip variants were not exercised. The trade *paths* are the same regardless of slip (slip only affects fill price); the per-trade Q1 / Q2 / Q3 / Q4 / Q6 statistics would be very similar across slip variants. Q5 differs by slip definitionally. A cross-slip Q5 analysis was not performed.
- **V-window Q1–Q7.** Phase 3s used R-window canonical runs. V-window populations are smaller and serve a different validation purpose (Phase 2f Gate 1 §11.3 V-window no-peeking discipline). A V-window Q1–Q7 run was not performed.

**None of these gaps justifies a follow-up phase by themselves.** Each gap exists by design — Phase 3s ran exactly the predeclared question set on exactly the predeclared population, and stopped. The integrity of the predeclaration discipline depends on not extending Q1–Q7 silently.

---

## 8. Mechanism lessons learned

Integrating Phase 3s findings into the project's mechanism-level understanding:

### 8.1 Q1 lesson — Completed-15m entries hide first-5m adverse path bias

All four retained-evidence candidates exhibit IAE > IFE in the first 5 minutes after the 15m next-bar-open fill. The pattern is universal (7 of 8 cells), consistent across BTC and ETH within each candidate, and strongest for F1 (~0.5 R adverse in first 5 min).

**Mechanism interpretation:** The completed-15m-bar signal-confirmation timing is structurally late relative to the post-signal market impulse. Whether the impulse is breakout-continuation (R3 / R2), mean-reversion-after-overextension (F1), or funding-extreme contrarian (D1-A), the first 5 minutes after entry typically move adverse before any thesis-confirming move materializes.

**Why this is not actionable:**

- 5m as a strategy signal layer is forbidden (Phase 3o §4.1 / Phase 3p §10).
- Entry-rule modification is forbidden (Phase 3o §6 / §10 — including questions of the form "which entry offset would avoid the IAE_1 hit?").
- The pattern is descriptive of *what 15m completed-bar entries look like*, not prescriptive about *how to enter differently*.

### 8.2 Q2 lesson — V1-family stops are wick-vulnerable; F1 / D1-A stops trigger on sustained invalidation

The cleanest cross-family mechanism finding from Phase 3s. V1-family (R3, R2) shows wick-fraction 0.571–1.000 across all four cells; F1 + D1-A show wick-fraction 0.269–0.347 across all four cells. The differential is large, replicable across symbols within each family, and mechanism-coherent.

**V1-family wick-stop interpretation:** Structural+ATR stops sit at levels that 5m wicks frequently penetrate without sustained follow-through. Stops trigger on transient market noise rather than invalidation of the breakout-continuation thesis. This is consistent with V1-family aggregate-negative R-window expR despite some PROMOTE-level mechanism support (R3 baseline-of-record per Phase 2p §C.1) — the strategy is in a stop-vulnerable zone but the broader thesis is not categorically refuted.

**F1 / D1-A sustained-stop interpretation:** Stops trigger because the underlying impulse continued in the entry-adverse direction for ≥ 3 × 5m bars. The mean-reversion / contrarian thesis didn't materialize in time. This is a *signal-failure* signature: the thesis itself doesn't hold often enough.

**Why this is not actionable:**

- Stop widening is forbidden categorically (`.claude/rules/prometheus-safety.md`).
- Mark-price stop policy is locked (§1.7.3).
- Changing stop placement would require a new strategy spec with predeclared evidence thresholds and full walk-forward validation — not contemplated by Phase 3o / 3p / 3r / 3s.
- The finding *explains* failure modes but does not *fix* them.

### 8.3 Q3 lesson — +1R intrabar touches exist but are descriptive only

In 6 of 8 candidate × symbol cells, ≥ 25% of adverse-exit trades temporarily reached +1R intrabar before reversing. The pattern is robust (cross-symbol replicable for R2 and D1-A; just-below-threshold for F1 with consistent BTC/ETH values).

**Why this is critically not actionable:**

- Phase 3o §6.3 explicitly forbids the question form "Which intrabar target touch rule maximizes R?".
- Phase 3p §8.3 explicitly states: *"This question is the highest-risk predeclared question in the entire spec. No intrabar target-touch finding may be converted into a '5m exit rule' or 'intrabar target rule' without separately authorized formal reclassification phase with predeclared evidence thresholds. The mere existence of intrabar target touches does not prove that an intrabar-target exit rule would be profitable in walk-forward cross-validation, does not prove the touch is exploitable in real execution (mark-price / trade-price divergence may make the touch unfillable in practice), and does not prove the resulting rule would survive the §11.6 cost-resilience gate."*
- The touch is observed in retrospect on the *same* 5m bars that subsequently reversed against the trade; the touch is not necessarily fillable in real execution.

**Phase 3t reaffirms:** The Q3 +1R finding is descriptive evidence that intrabar path richness exists. It is *not* a license to derive an exit rule.

### 8.4 Q4 lesson — D1-A funding-decay timing was non-informative

The D1-A funding-decay curve at {5, 10, 15, 30, 60} min from entry shows no monotone shape. SEM bands at the 60-min milestone are wider than the 5-min displacement magnitude on both BTC and ETH.

**Mechanism interpretation:** Funding-extreme contrarian effects, if they exist, are either too small to detect at 5m granularity or too heterogeneous across events to characterize cleanly. The predeclared SEM-vs-magnitude test was the right rigorous criterion; both symbols failed it.

**Why this is consistent with D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict:**

- D1-A's M2 mechanism check (funding-cost benefit) was already FAIL on both symbols at Phase 3j (~21× / ~11× below threshold).
- The non-informative Q4 finding is *consistent* with that prior M2 failure: if the funding effect were strong enough to dominate, it should be visible in the decay curve.
- Q4 does *not* identify a successor specification for D1-A. No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid is proposed.

### 8.5 Q5 lesson — 15m fill assumption is conservative-but-defensible at 5m granularity

No cell has |signed slippage mean| > 8 bps. F1 (-3.71 / -4.18 bps signed) and D1-A (-2.91 / -2.91 bps signed) tilt slightly toward the 15m next-open assumption being unfavorable, but well below the §11.6 = 8 bps HIGH per side threshold.

**Strong consistency with Phase 3l:** Phase 3l's external execution-cost evidence review primary assessment was "B — current cost model appears conservative but defensible; §11.6 remains unchanged pending stronger evidence." Q5 at 5m granularity does not provide stronger evidence to revise §11.6.

**Action:** §11.6 remains 8 bps HIGH per side. No cost-model revision phase is proposed.

### 8.6 Q6 lesson — D1-A mark-stops lag trade-stops by ~1.3–1.8 5m bars

For D1-A STOP-exited trades, mark-price stops trigger ~6–9 minutes after trade-price stops would have triggered. The pattern is robust (n=135 BTC, n=120 ETH after Phase 3r §8 zero exclusions), cross-symbol consistent, and exceeds the predeclared 1-bar threshold on both symbols.

**Mechanism interpretation:** Binance USDⓈ-M futures mark price is computed from a weighted average and is intentionally smoothed relative to the trade tape. D1-A's contrarian funding-extreme entries cluster at moments of unusual funding stress — precisely when trade-price tape diverges most from mark-price reference. The lag is consistent with mark-price's design philosophy (resistance to trade-tape manipulation).

**Why this is not actionable:**

- Mark-price stops are locked by §1.7.3 (`docs/07-risk/stop-loss-policy.md`).
- Phase 3r §8 explicitly forbids using Q6 to license stop-policy revision.
- The finding informs operator *understanding* of the mechanism only.
- D1-A's verdict (MECHANISM PASS / FRAMEWORK FAIL — other) is unaffected.

### 8.7 Q7 lesson — Diagnostic phase produced coherent informative output

Q7 informative (4 of 6 ≥ 3-threshold) means the diagnostic phase as a whole produced a coherent body of informative findings, not just isolated signals. The findings span multiple mechanism axes (entry-path asymmetry, stop pathology, intrabar target-touch frequency, mark-vs-trade timing).

**However, an informative Q7 does not change the non-actionability of any individual finding.** Phase 3p §8.7 explicitly stated: *"A non-informative Q7 outcome is a valid result of a future diagnostics phase and should not trigger framing pressure to find rescue narratives."* By symmetry, an informative Q7 outcome does not trigger framing pressure to find action narratives — the predeclared per-Q rules and forbidden question forms remain binding regardless of Q7's verdict.

---

## 9. Non-actionability guardrails

Phase 3t reaffirms the following guardrails — predeclared in Phase 3o / 3p / 3r and now binding in the post-Phase-3s state:

### 9.1 Informative diagnostics do not equal strategy evidence

A *strategy candidate* requires:
- A complete entry / target / stop / time-stop / cooldown specification.
- Predeclared evidence thresholds (§10.3 / §10.4 / §11.3 / §11.4 / §11.6 gate compliance).
- Walk-forward cross-validation results.
- Cost-sensitivity sweep results.
- Mechanism-check support (M1 / M2 / M3-style framework).

The four Phase 3s informative findings (Q1 / Q2 / Q3 / Q6) provide *none* of these. They are *descriptive characterizations* of the post-entry market path, not strategy candidates. **Equating diagnostic informativeness with strategy evidence is the canonical post-hoc loosening anti-pattern.**

### 9.2 Informative diagnostics do not revise prior verdicts

R3 baseline-of-record; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other. Each verdict is dataset-version-locked to v002 with predeclared evidence thresholds and was decided under the predeclared framework discipline.

Verdict revision requires:
- A separately authorized formal reclassification phase.
- Predeclared evidence thresholds for the reclassification.
- Operator-explicit recognition that the reclassification is happening.
- Compliance with `phase-gates.md` and Phase 2y §11.3.5 (no post-hoc loosening).

The Phase 3s findings do not by themselves authorize any such phase. **Phase 3t explicitly does not propose verdict revision for any retained-evidence candidate.**

### 9.3 Informative diagnostics do not authorize parameter changes

R3 sub-parameters (Fixed-R + 8-bar time-stop per Phase 2p §C.1). F1 parameters (8-bar cumulative displacement > 1.75 × ATR(20); SMA(8) target; structural stop with 0.10 × ATR buffer; 8-bar time-stop; same-direction cooldown until unwind). D1-A parameters (|Z_F| ≥ 2.0; 1.0 × ATR(20) stop; +2.0 R target; 32-bar time-stop; per-funding-event cooldown; band [0.60, 1.80] × ATR; contrarian; no regime filter). All locked.

Parameter changes require a new strategy spec with predeclared evidence thresholds and full validation. The Phase 3s findings do not constitute such a spec. **Phase 3t explicitly does not propose parameter changes.**

### 9.4 Informative diagnostics do not authorize a 5m strategy

Phase 3o §4.1 / Phase 3p §10 explicitly forbid 5m as a strategy signal layer. The Phase 3s findings do not change that prohibition — in fact, Phase 3s §13 / §14 reaffirmed the prohibition explicitly.

**Phase 3t reaffirms: no 5m strategy, no 5m hybrid, no 5m-on-X variant, no 5m-derived signal generation is authorized.**

### 9.5 Informative diagnostics do not authorize Phase 4, paper/shadow, live-readiness, or deployment

Per `phase-gates.md`:
- Phase 4 (runtime / state / persistence) requires Phase 3 strategy evidence to be complete and approved.
- Paper/shadow requires Phase 4 runtime + Phase 7 authorization.
- Live-readiness requires Phase 8 authorization with full readiness checklist.
- Deployment requires Phase 8 / Phase 9 authorization.
- Production-key creation requires Phase 8 / Phase 9 authorization.

The 5m research thread did not produce Phase 3 strategy evidence (it produced descriptive diagnostic evidence about *why retained-evidence candidates failed*, not new candidates). **Phase 3t explicitly does not authorize Phase 4 / paper-shadow / live-readiness / deployment / production-key / exchange-write work.**

---

## 10. Retained verdicts and locks

| Item | Status |
|---|---|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1; locked sub-parameters preserved verbatim. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3; preserved verbatim. |
| **R1a** | Retained research evidence only; non-leading; preserved verbatim. |
| **R1b-narrow** | Retained research evidence only; non-leading; preserved verbatim. |
| **R2** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks**; preserved verbatim. |
| **F1** | Retained research evidence only; **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal; preserved verbatim. |
| **D1-A** | Retained research evidence only; **MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal under current locked spec; preserved verbatim. |
| **§1.7.3 project-level locks** | Preserved verbatim (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets). |
| **§10.3 (Δexp ≥ +0.10 R)** | Preserved verbatim. |
| **§10.4 (absolute floors expR > −0.50 AND PF > 0.30)** | Preserved verbatim. |
| **§11.3 (V-window no-peeking)** | Preserved verbatim. |
| **§11.4 (ETH non-catastrophic)** | Preserved verbatim. |
| **§11.6 (8 bps HIGH per side cost-resilience)** | Preserved verbatim. Q5 confirmed at 5m granularity. |
| **Mark-price stops** | Preserved verbatim. Q6 finding does not license revision. |
| **v002 dataset families and manifests** | Preserved verbatim. NOT modified by Phase 3o / 3p / 3q / 3r / 3s / 3t. |
| **Phase 3q v001-of-5m manifests** | Preserved verbatim. Trade-price `research_eligible: true`; mark-price `research_eligible: false`. NOT modified by Phase 3r / 3s / 3t. |
| **v002 verdict provenance** | Preserved. R3 / R2 / F1 / D1-A trade populations remain dataset-version-attributed to v002. |
| **Phase 3o predeclared question set** | Preserved verbatim. Q1–Q7 set is complete and immutable. |
| **Phase 3o forbidden question forms** | Preserved verbatim. Five forms remain forbidden categorically. |
| **Phase 3o / Phase 3p analysis boundary** | Preserved verbatim. |
| **Phase 3p §4.7 strict integrity gate** | Preserved verbatim. NOT amended. |
| **Phase 3p §8 outcome-interpretation rules** | Preserved verbatim. Applied verbatim by Phase 3s. |
| **Phase 3r §8 Q6 invalid-window exclusion rule** | Preserved verbatim. Applied verbatim by Phase 3s (zero exclusions empirical). Binding for any future Q6-running phase. |
| **Phase 3s diagnostic outputs** | Preserved verbatim. Reports + JSON tables committed and immutable. |

Phase 3t adds no new lock and revises no existing lock. The locks listed above bound any future research, implementation, or operational phase.

---

## 11. Why remain paused

The recommended state remains **paused** for six concrete reasons:

### 11.1 No actionable strategy candidate emerged

Phase 3s produced four informative descriptive findings. None constitutes a strategy candidate per §9.1 above. The 5m research thread *did* update operator understanding of mechanism-level failure modes for retained-evidence candidates, but it *did not* identify a path to fix any of them or to discover a new candidate.

### 11.2 No path to rescue R2 / F1 / D1-A emerged

- **R2** remains FAILED — §11.6 cost-sensitivity blocks. Q5's "no |signed| > 8 bps cell" finding actively confirms §11.6's calibration; nothing in Phase 3s suggests R2 should be reopened.
- **F1** remains HARD REJECT. Q1 confirms F1 has the most pronounced first-5min adverse path bias (~0.5 R) — the signal failure is empirical, not a measurement artefact. Q2 confirms F1's stops trigger on sustained invalidation, not noise — again, signal failure. Nothing in Phase 3s suggests F1 should be reopened.
- **D1-A** remains MECHANISM PASS / FRAMEWORK FAIL — other. Q4's non-informative funding-decay finding does *not* support a fast-decay or slow-decay D1-A successor narrative. Q6's mark-stop lag finding describes microstructure but does not license stop-policy revision. Nothing in Phase 3s suggests D1-A should be reopened.

### 11.3 No path to revise §11.6 emerged

Q5 confirmed the cost model is conservative but defensible at 5m granularity. Phase 3l's "B — conservative but defensible" assessment is reaffirmed. §11.6 = 8 bps HIGH per side stands.

### 11.4 No path to revise mark-price stop policy emerged

Q6's D1-A mark-stop lag finding is descriptive evidence about Binance USDⓈ-M futures mark-price design philosophy — it does not license stop-policy revision. Mark-price stops remain locked by §1.7.3.

### 11.5 No path to authorize a 5m strategy layer emerged

Phase 3o §4.1 / Phase 3p §10 prohibition is preserved. The Phase 3s findings reinforce — not weaken — the case for that prohibition (Q1 universal adverse bias would translate directly into 5m strategy losses; F1's catastrophic floor would be reproduced or amplified at 5m frequency).

### 11.6 The cumulative pattern across nine phases is "remain paused"

Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r / 3s have each, in turn, recommended remain paused. The 5m research thread is now operationally complete and Phase 3t makes that closure explicit. The operator now has the cleanest possible written record of *why* paused is the right state and *what would have to change* for that to be reconsidered (§12 below).

---

## 12. What would be required for any future research to be valid

If, at some future date, the operator considers authorizing additional research, the following preconditions would apply per Phase 2y §11.3.5 / Phase 3o predeclaration discipline / Phase 3p §8 outcome-interpretation rules / Phase 3r §8 invalid-window exclusion discipline:

### 12.1 A genuinely new ex-ante hypothesis

The hypothesis must:
- Be defined *from first principles*, not derived from observed Q1–Q7 patterns.
- Be falsifiable.
- Be specifiable as a complete strategy candidate (entry / target / stop / time-stop / cooldown / cost / risk).
- Not reuse Phase 3s findings as parameter-optimization hints.

Any hypothesis that begins with "what if we used Q3's intrabar +1R touch as an exit rule?" is **forbidden** (Phase 3o §6.3). Any hypothesis that begins with "what if we shifted F1's entry to avoid the IAE_1 hit?" is **forbidden** (Phase 3o §6.1). Any hypothesis that begins with "what if D1-A held only N minutes instead of 32 bars?" derived from Q4 path observation is a post-hoc loosening of D1-A's spec and is **forbidden** under Phase 2y §11.3.5.

### 12.2 Full written specification before testing

The new hypothesis must be:
- Written down as a complete spec memo before any data is examined or computation is run.
- Committed to `main` with predeclared evidence thresholds for the §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gates.
- Reviewed by the operator with explicit recognition that the spec is being predeclared.
- Subject to Phase 2f-style framework discipline.

### 12.3 No conversion of Q3 / Q6 findings into post-hoc rules

The Q3 +1R intrabar-touch finding and the Q6 D1-A mark-stop lag finding are the **two highest-risk Phase 3s outputs** for post-hoc rule derivation. Any future research that even mentions these findings as motivation must explicitly disclaim that:

- The findings are not the source of any rule design.
- The new rule (if any) is derived from independent first-principles reasoning.
- The Phase 3o §6 forbidden question forms remain binding.

### 12.4 No rescue framing

The new research must not be framed as "rescuing" R2, F1, D1-A, or any retained-evidence candidate. R2 remains FAILED; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. A new candidate that happens to share structural similarity with R2 / F1 / D1-A is not a rescue — but it must be specified independently and validated independently.

### 12.5 No reuse of 5m findings as parameter-optimization hints

Specifically:
- Q1 IAE / IFE values cannot inform entry-offset parameters.
- Q2 wick-fraction values cannot inform stop-placement parameters.
- Q3 target-touch fractions cannot inform target / exit parameters.
- Q4 funding-decay milestones cannot inform holding-period parameters.
- Q5 fill realism cannot inform §11.6.
- Q6 mark-stop lag cannot inform stop-policy parameters.

### 12.6 Predeclared evidence thresholds

Following Phase 2f / Phase 2y / Phase 3o / 3p / 3r discipline, any new research phase must predeclare:
- The framework gate criteria (analogous to §10.3 / §10.4 / §11.3 / §11.4 / §11.6).
- The mechanism-check criteria (analogous to M1 / M2 / M3).
- The outcome-interpretation rules (analogous to Phase 3p §8).
- The forbidden question forms.
- The data version provenance.
- The trade-population provenance.

### 12.7 Separate operator authorization

No phase initiates without explicit operator authorization for that specific phase. Phase 3t does not authorize any successor; the operator is the sole source of authorization.

---

## 13. Forbidden paths

Phase 3t explicitly preserves the following forbidden paths:

### 13.1 Strategy rescue

- **R2 rescue.** R2 remains FAILED — §11.6. Any path to "make R2 work" by reframing §11.6, by deriving a new R2 entry rule from Q1 IAE patterns, by deriving a new R2 stop rule from Q2 wick-fraction, or by any post-hoc loosening is forbidden under Phase 2y §11.3.5 + Phase 2w §16.1.
- **F1 rescue.** F1 remains HARD REJECT. Any path to "make F1 work" via 5m entry-offset, 5m exit rule, intrabar target rule, regime filter derived from Q2 sustained-stop pattern, or any post-hoc loosening is forbidden under Phase 3o §6 + Phase 3d-B2 terminal status.
- **D1-A rescue.** D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. Any path to "make D1-A work" via Q4-derived holding-period revision, Q6-derived mark-vs-trade stop adjustment, or any post-hoc parameter optimization is forbidden under Phase 3o §6.2 + Phase 3j terminal status.

### 13.2 5m strategy / hybrid / variant

- 5m as strategy signal layer: forbidden by Phase 3o §4.1.
- D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, V1-on-5m, F1-on-5m, D1-A-on-5m: not authorized; not contemplated by any prior phase; would violate Phase 3o §4.1 / §6 prohibitions.
- Target-subset rescue (e.g., "F1 TARGET trades alone are profitable"): forbidden by Phase 3d-B2 evaluation framing (Phase 3c §7.3 catastrophic-floor predicate applies to the *full* trade population, not subsets).
- Regime-conditioned rescue (e.g., "D1-A is profitable in regime X derived from Q2 patterns"): forbidden by Phase 3m anti-circular-reasoning discipline + Phase 3o §6 forbidden question forms.

### 13.3 Phase 4 / paper-shadow / live-readiness / deployment

- Phase 4 (runtime / state / persistence / risk-runtime): not authorized; requires Phase 3 strategy evidence which Phase 3s did not produce.
- Paper/shadow planning: not authorized; requires Phase 4 + Phase 7 gate.
- Live-readiness: not authorized; requires Phase 8 readiness checklist.
- Deployment: not authorized; requires Phase 8 / Phase 9 gate.
- Production-key creation: forbidden until phase-gate (per `phase-gates.md`).
- Exchange-write capability: forbidden until phase-gate.

### 13.4 MCP / Graphify / `.mcp.json` / credentials

- MCP servers: not enabled; forbidden by `.claude/rules/prometheus-mcp-and-secrets.md` until specifically authorized.
- Graphify: not installed; not used.
- `.mcp.json`: not created; not used.
- Credentials: none requested; none stored; none referenced.
- Authenticated APIs: not used.
- Private Binance endpoints: not used.
- User stream: not used.
- WebSocket: not used.
- Secrets: not requested; not stored.

---

## 14. Operator decision menu

The operator now has the closing memo for the 5m research thread. The next operator decision is operator-driven only.

### 14.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategy-execution pause continues. Phase 3t joins Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r / 3s as the closing entry of the running 5m research thread record. No subsequent phase authorized.

**Reasoning:**

- The 5m research thread is operationally complete (per §1 / §11).
- No actionable strategy candidate emerged.
- All locks preserved verbatim (per §10).
- The closure narrative is now in the project record as a single readable memo (this memo).
- Pausing preserves operator optionality: future authorization decisions can be made cleanly without inheriting any commitments from Phase 3t.
- The cumulative pattern across nine phases ("remain paused" each time) is reinforced by Phase 3t.

**What this preserves:** Everything in §10. Nothing changes.

**What this rules out:** No further research / strategy / implementation / paper-shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write activity.

### 14.2 Option B — Pause and prepare for a future unrelated fresh-hypothesis discovery memo (NOT RECOMMENDED NOW)

**Description:** The operator could in principle, at some future date, authorize a fresh-hypothesis discovery memo — analogous to Phase 3a (F1 discovery) or Phase 3f (D1-A discovery) — that proposes an entirely new strategy family from first principles, *not* derived from any retained-evidence candidate or from Phase 3s findings.

**Phase 3t's view:** **Not recommended now.**

- Three strategy-research arcs have framework-failed under unchanged discipline (V1 breakout family at useful ceiling; F1 HARD REJECT; D1-A FRAMEWORK FAIL). Starting a fourth arc without first addressing *why* the first three failed (which Phase 3m's regime-first thinking and Phase 3s's mechanism findings could in principle inform) is procedurally premature.
- A fresh-hypothesis discovery would also be subject to Phase 3a / Phase 3f rigour: predeclared evidence thresholds; M1 / M2 / M3 mechanism check; framework discipline. The likelihood of a clean fourth arc passing where three previous arcs failed is bounded.
- Phase 3t reaffirms: the operator's correct choice is paused, not "paused but preparing for the next arc."

If the operator later wishes to authorize fresh-hypothesis discovery, it would be a separately briefed phase with explicit anti-rescue / anti-circular-reasoning preconditions.

### 14.3 Option C — Regime-first formal spec (NOT RECOMMENDED NOW)

**Description:** Authorize the docs-only formal regime-first spec memo that Phase 3m discussed but did not start.

**Phase 3t's view:** **Not recommended now.**

- Phase 3m's primary recommendation was remain paused, with regime-first formal spec as a possible (not authorized) future option.
- Phase 3s did not test regime-classification questions; Q2's V1-vs-F1/D1-A pathology differential is candidate-family-conditional, not regime-conditional.
- Authorizing regime-first formal spec now would be premature: Phase 3m specified that any regime-first work must define regimes from first principles, not from winning-fold-derived labels or from rescue framing. Phase 3s findings could easily contaminate that discipline if regime-first work follows immediately.
- If the operator wishes to revisit regime-first, it should be at a strategically-clean later moment, not as a Phase 3t direct successor.

### 14.4 Option D — Implementation / Phase 4 / paper-shadow / live-readiness / deployment (FORBIDDEN / NOT RECOMMENDED)

**Description:** Authorize any phase beyond docs-only research consolidation.

**Phase 3t's view:** **Forbidden / not recommended.** Per `phase-gates.md`:

- Phase 4 requires Phase 3 strategy evidence to be complete and approved. Phase 3s did not produce strategy evidence; it produced descriptive diagnostic evidence.
- Paper/shadow requires Phase 4 + Phase 7 gate.
- Live-readiness requires Phase 8 gate with full readiness checklist.
- Deployment / production-key creation / exchange-write capability require Phase 8 / Phase 9 gate.

None of these gates is met. Strongly not recommended.

### 14.5 Recommendation

**Phase 3t recommends Option A (remain paused) as primary.** The 5m research thread is operationally complete; the closure narrative is now in the project record; no actionable strategy candidate emerged; all locks preserved; the operator's correct state is paused.

Options B, C, D are evaluated above and not recommended.

---

## 15. Next authorization status

**No next phase has been authorized.** Phase 3t authorizes nothing other than producing this consolidation memo and the accompanying closeout artefact. The operator's decision after Phase 3t is operator-driven only.

Selection of any subsequent phase (fresh-hypothesis discovery, regime-first formal spec, ML feasibility, formal cost-model revision, retained-evidence successor, 5m strategy / hybrid / variant, paper/shadow planning, Phase 4 runtime work, live-readiness, deployment, production-key creation, exchange-write capability, MCP / Graphify / `.mcp.json` / credentials activation) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) is **complete**. Recommended state remains **paused**.
