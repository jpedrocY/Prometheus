# Phase 3o — 5m Diagnostics-Spec Memo (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11 (no post-hoc loosening per §11.3.5); Phase 2i §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets); Phase 2p §C.1 (R3 baseline-of-record); Phase 2x family-review memo (V1 breakout family at useful ceiling under current framework); Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved); Phase 2w §16.1 (R2 FAILED — §11.6 cost-sensitivity blocks); Phase 3d-B2 (F1 HARD REJECT); Phase 3e post-F1 research consolidation memo; Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3j terminal for D1-A under current locked spec); Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation); Phase 3l external execution-cost evidence review (primary assessment B — current cost model conservative but defensible; §11.6 unchanged pending stronger evidence); Phase 3m regime-first research framework memo (remain-paused primary recommendation); Phase 3n 5m timeframe feasibility / execution-timing memo (remain-paused primary recommendation; 5m framed as possible future execution / timing diagnostics layer only, not signal layer); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/05-backtesting-validation/backtesting-principles.md`; `docs/05-backtesting-validation/cost-modeling.md`; `docs/04-data/data-requirements.md`; `docs/04-data/dataset-versioning.md`; `docs/04-data/timestamp-policy.md`; `.claude/rules/prometheus-core.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`.

**Phase:** 3o — Docs-only **5m diagnostics-spec memo.** Predeclares the *exact* diagnostic questions, definitions, evidence boundaries, and anti-overfitting guardrails that would govern any future 5m execution / timing diagnostics phase. **Predeclaration is the entire output.** No data acquired, no v003 created, no analysis run, no backtest run, no code written, no implementation initiated, no successor authorized.

**Branch:** `phase-3o/5m-diagnostics-spec`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. **No code change. No backtest. No 5m analysis. No 5m data downloaded. No v003 dataset created. No supplemental 5m dataset created. No variant created. No parameter tuned. No threshold changed. No project-level lock changed. No prior verdict revised.** R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence. R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. §11.6 = 8 bps HIGH per side preserved. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write proposal. **Mindset principle:** *Paused means "pause strategy execution," not "pause learning." Phase 3o makes future 5m work safer by defining the questions before any 5m data exists in the project.* Recommendation is **provisional and evidence-based, not definitive**; the operator decides.

---

## 1. Plain-English explanation of what Phase 3o is deciding

Phase 3o is a docs-only *predeclaration* memo. Its purpose is purely procedural:

> **Write down — *now, before any 5m data exists in the repository* — exactly which diagnostic questions a future 5m diagnostics-execution phase would answer, exactly which questions it would *not* answer, exactly how each diagnostic term would be defined, and exactly which guardrails would govern the analysis.**

Phase 3o is *not* a strategy memo, *not* a data-acquisition memo, *not* a regime memo, *not* an implementation memo, and *not* an analysis memo. The deliverable is a written specification of *what would be measured if measurement were ever authorized*, plus a written specification of *what would deliberately not be measured even then*.

The motivating insight (from Phase 3n §9.1) is:

> *Predeclaration is the only defense against post-hoc loosening, target-touch rescue framing, parameter tuning from path data, and the slippery slope from "diagnostics" to "5m strategy variant." Predeclaring questions before any data exists is unambiguously safer than waiting until data exists to decide what to ask.*

The Phase 3n decision menu listed Phase 3o (5m diagnostics-spec memo, docs-only) as Option C — a conditional tertiary alternative. The operator selected it. Phase 3o therefore inherits the same Phase 3n discipline: predeclare, do not execute; specify, do not run; document the rules, do not produce results.

Phase 3o is **NOT**:

- Authorizing 5m data download.
- Authorizing v003 or supplemental 5m dataset creation.
- Authorizing 5m diagnostics-execution work.
- Authorizing 5m strategy signals or any 5m strategy family.
- Authorizing rerun of H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A or any controls.
- Authorizing reclassification or rescue of R2, F1, or D1-A.
- Authorizing parameter tuning, threshold revision, project-lock revision, or prior-verdict revision.
- Authorizing regime-first implementation, ML feasibility memo, formal cost-model revision, hybrid spec, or new strategy-family discovery.
- Authorizing paper/shadow planning, Phase 4 runtime / state / persistence work, live-readiness, deployment, production-key creation, or exchange-write capability.
- Enabling MCP, Graphify, `.mcp.json`, credentials, authenticated Binance APIs, or any data/ commits.

Phase 3o **IS**:

- A docs-only memo that documents (a) why predeclaration must precede any 5m data work; (b) explicit non-goals; (c) a predeclared diagnostic question set (Q1–Q7) with strict per-question definitions of what counts as informative versus non-informative; (d) explicitly forbidden diagnostic questions, with reasoning; (e) proposed diagnostic-term definitions without computing them; (f) data-boundary rules; (g) timestamp / leakage guardrails; (h) the strict analysis boundary that separates allowed diagnostics from forbidden strategy evaluation; (i) per-strategy diagnostic mapping (R3 / R2 / F1 / D1-A); (j) required outputs and stop conditions for any future diagnostics-execution phase; (k) a single recommended next operator decision.

The output is a consolidated 5m-diagnostics predeclaration record + a single forward-looking operator decision recommendation. **Phase 3o produces a memo; the operator decides whether to authorize anything downstream.**

---

## 2. Current project-state restatement

| Item | State |
|------|-------|
| **R3** | V1 breakout baseline-of-record per Phase 2p §C.1; locked sub-parameters preserved. |
| **H0** | V1 breakout framework anchor per Phase 2i §1.7.3. |
| **R1a / R1b-narrow** | Retained research evidence only; non-leading. |
| **R2** | Retained research evidence only; **framework FAILED — §11.6 cost-sensitivity blocks**. |
| **F1** | Retained research evidence only; **HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 terminal for F1. |
| **D1-A** | Retained research evidence only; **MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2; Phase 3j terminal for D1-A under current locked spec. |
| **Phase 3k consolidation** | Merged; primary recommendation: **remain paused**. |
| **Phase 3l external cost-evidence review** | Merged; primary assessment **B — current cost model conservative but defensible**; §11.6 = 8 bps HIGH per side **preserved unchanged pending stronger evidence**. |
| **Phase 3m regime-first framework memo** | Merged; primary recommendation: **remain paused**; formal regime-first spec / planning memo *not* started. |
| **Phase 3n 5m timeframe feasibility memo** | Merged; primary recommendation: **remain paused**; 5m framed as possible future execution / timing diagnostics layer only, not signal layer; no 5m data downloaded; no v003 created. |
| **§1.7.3 project-level locks** | Preserved verbatim. |
| **Phase 2f thresholds (incl. §11.6 = 8 bps HIGH per side)** | Preserved verbatim. |
| **v002 datasets** | Locked. 15m + 1h-derived + 15m mark-price + funding-event tables for BTCUSDT and ETHUSDT. **No 5m datasets exist; no v003 created.** |
| **Paper/shadow planning** | Not authorized. |
| **Phase 4 work** | Not authorized. |
| **Live-readiness / deployment / production-key / exchange-write work** | Not authorized. |
| **MCP / Graphify / `.mcp.json` / credentials** | Not activated; not requested; not used. |

The next operator decision is operator-driven only. Phase 3o does not pre-empt that decision; this section records the state on which any future decision must build.

---

## 3. Why a diagnostics-spec memo comes before any 5m data work

Predeclaration of the diagnostic question set must precede any 5m data acquisition for *six concrete reasons*:

### 3.1 Prevents data dredging

Once 5m data exists, the temptation to ask "what does the data show?" without a predeclared question is overwhelming. Open-ended exploration on a sufficiently rich dataset will find statistically significant-looking patterns by chance. Predeclaration narrows the search space *before* the search begins, sharply reducing false-discovery rate.

### 3.2 Prevents post-hoc target-touch rescue

The single most dangerous 5m diagnostic finding (per Phase 3n §6 question Q4 in the memo's interim list) is the observation that "X% of losing 15m trades touched +1R or +2R intrabar before reversing to stop." This finding is *empirically true in any dataset* (some trades always touch some level intrabar) and is *useless as evidence of an exploitable rule* unless the touch-frequency is high enough, the reversal pattern is asymmetric enough, and the implied exit-rule survives walk-forward cross-validation. Without predeclared anti-rescue language, this finding becomes a target-touch-based "improved exit rule" — exactly the post-hoc loosening Phase 2y §11.3.5 forbids.

### 3.3 Defines questions before data exists

Defining questions *before* the data exists is unambiguously stronger evidence than defining them after. Predeclaration timestamped to a commit on `main` is auditable and immutable. Questions defined after data exists are vulnerable to selection bias even with the best intentions.

### 3.4 Separates diagnostics from strategy evaluation

Phase 3n §9.5 articulated this principle: diagnostics work answers "what happened inside losing trades?" Strategy evaluation answers "does this candidate pass §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds?" These are *different questions*. Predeclaring the diagnostic question set forces this distinction up-front and prevents drift toward strategy-evaluation framing during the analysis.

### 3.5 Preserves prior verdicts

R2's FAILED verdict, F1's HARD REJECT verdict, and D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict are *terminal under current locked spec*. Predeclaring that no diagnostic finding can revise any of these verdicts (§5 of this memo, per question; §10 of this memo, in the analysis-boundary section) prevents 5m findings from being treated as verdict-revising evidence.

### 3.6 Prevents "5m as strategy signal" drift

Phase 3n §4.1 articulated that 5m as a strategy signal layer is "Dangerous now. Not authorized. Strongly discouraged." Without predeclared procedural separation, 5m diagnostic findings become inputs to "5m candidate" thinking — exactly the slippery slope §7.10 of the Phase 3n memo identified. Predeclaration enforces that 5m findings are descriptive only, not prescriptive.

---

## 4. Explicit non-goals

Phase 3o explicitly does **not** authorize, propose, or initiate any of the following:

- **No 5m strategy.** No 5m breakout, 5m mean-reversion, 5m funding-aware, 5m hybrid, or any 5m signal generation.
- **No 5m variant of V1, R2, F1, or D1-A.** No reformulation of any retained-evidence candidate at 5m granularity. No "F1-on-5m" experiment. No "D1-A-on-5m" experiment.
- **No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid.** No successor candidate authorized.
- **No data acquisition.** No 5m kline download, no 5m mark-price download, no 5m funding-rate work, no third-party 5m dataset import, no data refresh, no manifest regeneration.
- **No v003 creation.** v002 remains canonical. No supplemental 5m dataset created (whether named v003 or v001-of-5m).
- **No diagnostics execution.** Phase 3o predeclares the diagnostic spec; it does *not* run any diagnostic. No diagnostic table, plot, or summary statistic is produced.
- **No prior-verdict revision.** R2 remains FAILED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other. R3 remains baseline-of-record. H0 remains framework anchor.
- **No paper/shadow or Phase 4.** No paper/shadow planning. No Phase 4 runtime / state / persistence / risk-runtime work. No live-readiness. No deployment. No production-key creation. No exchange-write capability.

---

## 5. Predeclared diagnostic question set

The following seven questions (Q1–Q7) are the **complete predeclared question set** for any future 5m diagnostics-execution phase. Future 5m diagnostics work must operate strictly within this question set and may not silently extend it. Adding a new question requires a separately authorized phase.

Each question records:
- **What it measures** — the descriptive fact extracted from 5m data, expressed without computing it.
- **Why it matters** — what mechanism-level understanding it would inform.
- **Which prior strategy failure it informs** — the retained-evidence candidate(s) for which the question is most relevant.
- **What would count as informative** — the qualitative pattern that would justify writing the finding into a future docs-only diagnostics report.
- **What would count as non-informative** — the pattern that would lead to "no useful information" classification.
- **Why it cannot revise a prior verdict by itself** — the procedural reason any answer must remain descriptive.

### 5.1 Q1 — Immediate adverse excursion in the first 5–15 minutes after 15m entry

- **What it measures:** For each completed 15m trade in the v002-locked retained-evidence backtests (R3, R2, F1, D1-A, plus controls), the realized price path inside the *first* 1, 2, 3 5m sub-bars after entry — specifically the *adverse* excursion (the worst-case unrealized R the trade reaches, in the direction *opposite* to the entry).
- **Why it matters:** Distinguishes "bad entry timing" failure (immediate adverse path) from "bad signal" failure (initial favorable path that later reverses). The former is consistent with structural 15m-completed-bar entry timing being mismatched to the underlying impulse; the latter is consistent with the signal itself being non-predictive.
- **Which prior strategy failure it informs:** Most relevant to **R3** (where V1 breakout entries may be systematically front-run), **R2** (whose pullback-retest entry depends critically on fill timing), and **D1-A** (where the funding-extreme contrarian entry may happen too late in the impulse cycle).
- **What would count as informative:** Either uniformly-hostile first-5m-bar adverse excursion across candidates (suggesting a *structural* 15m-entry-timing problem common to all rules-based completed-bar entries), or candidate-specific patterns (suggesting individual mechanism-level explanations).
- **What would count as non-informative:** Symmetric distributions of first-5m-bar adverse and favorable excursions across all candidates. This pattern would be consistent with no meaningful entry-timing structure on the 5m horizon.
- **Why it cannot revise a prior verdict by itself:** R2's §11.6 verdict, F1's HARD REJECT verdict, and D1-A's MECHANISM PASS / FRAMEWORK FAIL — other verdict are *terminal under current locked spec*. Q1 produces *path evidence*, not *threshold evidence*. The §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gates are not Q1's domain. Verdict revision would require a separately authorized formal reclassification phase with predeclared evidence thresholds, which Phase 3o does not propose.

### 5.2 Q2 — Stop-trigger path: short-lived 5m wick versus sustained invalidation

- **What it measures:** For each STOP-exited trade in the v002-locked retained-evidence backtests, the *path* of the price relative to the stop level in the 5m sub-bars surrounding the stop event. Specifically: was the stop violated by a single 5m wick whose subsequent close was back inside the position-favorable zone (a "wick-stop event"), or was the stop violated by sustained price action persisting beyond the stop level for ≥3 consecutive 5m bars (a "sustained-stop event")?
- **Why it matters:** Distinguishes stop-trigger pathology (5m noise wicking through stops that would not have been hit on close-confirmation) from sustained-invalidation stop-out (5m close-aligned with stop direction). The two pathologies have different mechanism implications (and *neither* licenses stop widening, which is forbidden by `.claude/rules/prometheus-safety.md`).
- **Which prior strategy failure it informs:** Most relevant to **R3** (where structural+ATR stops may be wick-vulnerable in V1 breakout setups), **F1** (whose 53–54% STOP exits at −1.30 / −1.24 R mean dominate the failure), and **D1-A** (whose 67–68% STOP exits at −1.24 / −1.30 R mean drove the FRAMEWORK FAIL).
- **What would count as informative:** A meaningful skew toward wick-stops in any candidate (suggesting stop-trigger sensitivity to short-lived noise) or toward sustained-stops (suggesting stops are invalidated by genuine directional shifts). Strong differential between candidates would also be informative.
- **What would count as non-informative:** A roughly uniform mix of wick-stops and sustained-stops with no clear candidate-level differentiation. This pattern would be consistent with stops behaving as designed within the 5m noise floor.
- **Why it cannot revise a prior verdict by itself:** Stop pathology evidence cannot license stop widening (forbidden), cannot revise the §11.6 cost-resilience gate, and cannot revise prior verdicts. Mark-price stop discipline (`docs/07-risk/stop-loss-policy.md`) is preserved verbatim regardless of any Q2 finding.

### 5.3 Q3 — Intrabar +1R / +2R target touches before adverse exit

- **What it measures:** For STOP-exited or unrealized-target-exited trades in the v002-locked retained-evidence backtests, the count and timing of intrabar 5m sub-bar moments where the trade's unrealized profit touched +1R or +2R *before* the trade subsequently exited adversely. Distinguishes "target-touch-then-stop" events from "no-touch-then-stop" events. Distinguishes "intrabar target touch" (any 5m sub-bar high/low for long/short trades respectively reaches the level) from "confirmed target touch" (a 5m sub-bar *closes* beyond the level).
- **Why it matters:** Provides path evidence about whether the 15m exit rule systematically misses trades that *temporarily* reached profit levels. This is the *most rescue-shaped* of the predeclared questions and therefore the most procedurally constrained.
- **Which prior strategy failure it informs:** Most relevant to **R3** (whose Fixed-R target may be intrabar-touched but close-aligned at adverse levels), **F1** (whose TARGET subset shows +1.86 R per trade when isolated, suggesting some intrabar reach toward target), and **D1-A** (whose TARGET subset shows +2.143 / +2.447 R per trade when isolated).
- **What would count as informative:** A coherent pattern in which a meaningful fraction of STOP-exited trades reached +1R or +2R intrabar across multiple candidates and date ranges. This finding would be *descriptive evidence* of intrabar path richness.
- **What would count as non-informative:** Few or no intrabar target touches in STOP-exited trades, or intrabar touches that occur in a small minority and are equally distributed across all candidates with no temporal clustering.
- **Why it cannot revise a prior verdict by itself:** **This question is the highest-risk predeclared question in the entire spec.** No intrabar target-touch finding may be converted into a "5m exit rule" or "intrabar target rule" without separately authorized formal reclassification phase with predeclared evidence thresholds. The mere existence of intrabar target touches *does not prove* that an intrabar-target exit rule would be profitable in walk-forward cross-validation, *does not prove* the touch is exploitable in real execution (mark-price / trade-price divergence may make the touch unfillable in practice), and *does not prove* the resulting rule would survive the §11.6 cost-resilience gate. Prior verdicts (R3 baseline-of-record; R2 FAILED; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other) are unaffected by any Q3 answer.

### 5.4 Q4 — D1-A funding-extreme decay over 5 / 10 / 15 / 30 / 60 minutes

- **What it measures:** For trades in the v002-locked D1-A backtest, the realized price-path response across the first 5, 10, 15, 30, and 60 minutes after the funding-settlement event that triggered the entry — specifically, the cumulative direction of the contrarian impulse. Diagnostic curve: mean cumulative price displacement (in ATR(20) units) at 5 / 10 / 15 / 30 / 60 minute milestones, separately for BTC and ETH.
- **Why it matters:** D1-A's locked spec uses a 32-bar (8-hour) holding period with 1.0 × ATR(20) stop and +2.0 R target. If the funding-extreme contrarian impulse decays substantially within minutes (rather than hours), the 32-bar holding period assumption is fundamentally mismatched to the underlying mechanism — explaining why D1-A's WR (~30–31%) is so far below the +51% breakeven implied by the +2.0 R target / 1.0 R stop ratio.
- **Which prior strategy failure it informs:** Specifically and exclusively **D1-A**. This question has the highest *information value* of the predeclared seven for D1-A's diagnostic story.
- **What would count as informative:** A monotonic decay curve where most of the contrarian impulse is realized within 5–15 minutes (suggesting the 32-bar holding-period assumption is mismatched), *or* a flat / stable curve over the full 60-minute window (suggesting decay is slow and the 32-bar assumption is reasonable but other failure modes dominate).
- **What would count as non-informative:** Noisy curves with high variance across funding events such that no coherent decay timescale can be identified — consistent with funding-extreme effects being either too small to detect at 5m granularity or highly heterogeneous across events.
- **Why it cannot revise a prior verdict by itself:** D1-A is **MECHANISM PASS / FRAMEWORK FAIL — other** under current locked spec. **Phase 3j is terminal for D1-A.** Q4 findings *may inform* a possible future operator decision about whether to authorize a D1-A-prime / D1-B / hybrid spec — but Phase 3o does *not* contemplate any such authorization. The existence of a fast funding-decay curve does not by itself constitute a FRAMEWORK PASS for any successor; it is one piece of mechanism evidence among many that any future successor proposal would have to integrate.

### 5.5 Q5 — Next-15m-open fill assumption realism when decomposed into 5m sub-bars

- **What it measures:** For each trade in the v002-locked retained-evidence backtests, the price path of the *first* 5m sub-bar after the 15m signal close (i.e., the 5m bar that would contain the trade's actual fill in a real execution scenario). Specifically: the difference between the 15m bar's open (the next-bar-open assumption used by all v002 backtests per `docs/05-backtesting-validation/backtesting-principles.md`) and a probability-weighted 5m fill simulation across that 5m sub-bar's range.
- **Why it matters:** Phase 3l found the cost model "B — conservative but defensible" at 15m granularity (8 bps HIGH per side). Q5 provides 5m-resolution evidence about whether the 15m next-open assumption is systematically optimistic (real fills inside the 5m sub-bar are worse than the 15m open print) or systematically conservative (real fills are better). Either direction would be diagnostically relevant; neither would by itself revise §11.6.
- **Which prior strategy failure it informs:** Most relevant to **R3** and **R2** (both of which depend on V1 breakout signal-bar-close entry timing) and **D1-A** (which depends on funding-event-timestamp-aligned next-bar-open).
- **What would count as informative:** A systematic skew (in either direction) larger than the existing 8 bps HIGH cost assumption. Either direction would be evidence about cost-model realism — though Phase 3o reminds that *changing* §11.6 requires a separately authorized formal cost-model revision phase.
- **What would count as non-informative:** A skew within or smaller than the 8 bps HIGH bound, with high variance and no candidate-level differentiation. This pattern would be consistent with the 15m next-open assumption being well-calibrated to the 5m intrabar reality at the cost-tolerance level §11.6 is built around.
- **Why it cannot revise a prior verdict by itself:** §11.6 = 8 bps HIGH per side is preserved verbatim and is revisable only through a separately authorized formal cost-model revision phase. Phase 3l found the current cost model "B — conservative but defensible" and explicitly recommended "§11.6 remains unchanged pending stronger evidence." Q5 produces *one piece* of fill-realism evidence, not a §11.6 revision input; it would inform a future docs-only cost-model revision memo if the operator separately authorized one, but cannot itself revise §11.6.

### 5.6 Q6 — Mark-price versus trade-price stop-trigger sensitivity at 5m granularity

- **What it measures:** For STOP-exited trades in the v002-locked retained-evidence backtests, the difference between the 5m sub-bar at which a *mark-price-driven* stop would have triggered versus a *trade-price-driven* stop would have triggered. The v002 datasets include both `binance_usdm_btcusdt_markprice_15m__v002` and `binance_usdm_btcusdt_15m__v002` (trade-price klines) for BTCUSDT (and equivalents for ETHUSDT); a future 5m phase would require analogous 5m-resolution data.
- **Why it matters:** §1.7.3 project locks specify mark-price stops (per `.claude/rules/prometheus-safety.md`: `workingType=MARK_PRICE`, `priceProtect=TRUE`). The v002 backtests are calibrated to mark-price stop triggering. Q6 provides 5m-resolution evidence about whether mark-price and trade-price diverge meaningfully at 5m granularity in stop-relevant moments — informing operator understanding of the stop-trigger mechanism in real-execution conditions, *not* informing any change to mark-price stop policy.
- **Which prior strategy failure it informs:** Most relevant to all retained-evidence candidates (R3 / R2 / F1 / D1-A) for the subset of trades that exited via STOP, since stop-trigger sensitivity is mechanism-relevant for all of them.
- **What would count as informative:** Systematic divergence between mark-price and trade-price stop-trigger timing larger than typical 5m bar variance, especially in volatile market conditions. Either direction (mark-price triggers earlier or later) would be informative.
- **What would count as non-informative:** Mark-price and trade-price stop-trigger timings tracking within 1 5m bar with no systematic skew. This pattern would be consistent with mark-price and trade-price being effectively synonymous at the 5m horizon for stop-trigger purposes.
- **Why it cannot revise a prior verdict by itself:** Mark-price stop discipline is a `.claude/rules/prometheus-safety.md` lock and is preserved verbatim regardless of any Q6 finding. Q6 provides *understanding*, not *policy revision*. Verdicts and stop policies remain unchanged.

### 5.7 Q7 — Whether 5m evidence adds useful signal-path insight or mostly false precision

- **What it measures:** A meta-question to be evaluated *after* Q1–Q6 are completed (in a hypothetical future diagnostics-execution phase): does the aggregate of Q1–Q6 findings produce coherent, replicable, mechanism-informing evidence, or does it produce noisy, incoherent, hard-to-replicate patterns that look meaningful in-sample but do not generalize?
- **Why it matters:** Phase 3n §7.4 and §7.9 articulated that 5m carries lower signal-to-noise ratio and induces false-confidence-from-intrabar-hindsight. Q7 forces an explicit, predeclared, post-hoc-but-honest assessment of whether 5m diagnostics actually delivered information value — *or* whether the analysis primarily produced false-precision artifacts.
- **Which prior strategy failure it informs:** Q7 is meta and applies to all candidates simultaneously.
- **What would count as informative:** Q7 self-reports "informative" only if Q1–Q6 produced findings that are (a) replicable across BTC and ETH, (b) replicable across multiple non-overlapping date sub-ranges within v002, (c) consistent with mechanism-level reasoning, and (d) not heavily dependent on a small number of outlier trades or a narrow time window.
- **What would count as non-informative:** Q7 self-reports "non-informative" if Q1–Q6 produced findings that are (a) BTC-only or ETH-only without corroboration, (b) heavily concentrated in narrow date sub-ranges, (c) sensitive to small parameter or window-definition choices, or (d) inconsistent with any coherent mechanism-level explanation.
- **Why it cannot revise a prior verdict by itself:** Q7 is a meta-assessment of the *information value* of the diagnostics phase itself, not a strategy-evaluation question. A "non-informative" Q7 result is a valid output of a future diagnostics phase and should *not* trigger framing pressure to find rescue narratives. A "non-informative" Q7 result *strengthens* the existing remain-paused recommendation rather than weakening it.

### 5.8 Question-set scope discipline

The seven questions Q1–Q7 are the **complete** predeclared question set. Future 5m diagnostics-execution work must operate strictly within this set. Questions that *appear* during data exploration must be deferred to a separately authorized phase. The diagnostics-execution phase, if ever authorized, *may not* silently extend the question set — silent extension is data dredging.

---

## 6. Forbidden diagnostic questions

The following question forms are *explicitly forbidden* from any future 5m diagnostics-execution phase. These forms are forbidden regardless of how the phase is briefed, regardless of operator pressure, and regardless of any in-sample evidence that suggests they would be informative. The procedural prohibition is designed to be hard.

### 6.1 "Which 5m entry offset would have made F1 profitable?"

**Why forbidden:** This is a strategy-design question disguised as a diagnostic question. It searches for a parameter (entry offset) that retroactively rescues a HARD-REJECTED candidate. The answer is *guaranteed* to exist in any sufficiently rich dataset (some offset always exists that improves in-sample performance) and is *guaranteed* to be a post-hoc loosening of the F1 spec. Phase 2y §11.3.5 forbids post-hoc loosening. Phase 3d-B2 is *terminal* for F1.

### 6.2 "Which 5m exit rule rescues D1-A?"

**Why forbidden:** Same form as 6.1, applied to D1-A's exit logic. The +2.0 R target / 1.0 R stop / 32-bar time-stop combination is locked. Searching 5m sub-bar paths for a rescue exit rule is post-hoc loosening of D1-A's spec. **Phase 3j is terminal for D1-A under current locked spec.** Any successor proposal (D1-A-prime, D1-B, hybrid) requires separate operator authorization not contemplated here.

### 6.3 "Which intrabar target touch rule maximizes R?"

**Why forbidden:** Q3 in §5.3 above is the *only* permitted form of intrabar-target-touch question, and is explicitly bounded as descriptive-only. The maximize-R form converts a descriptive observation into a parameter search — exactly the post-hoc target-touch rescue pattern §3.2 of this memo, Phase 3n §6 "highest-risk question," and Phase 2y §11.3.5 all forbid.

### 6.4 "Which 5m threshold makes R2 pass §11.6?"

**Why forbidden:** This is a §11.6-rescue question. R2's verdict is FAILED — §11.6 cost-sensitivity blocks. §11.6 is preserved verbatim. Any "5m threshold that makes R2 pass §11.6" would be either (a) a §11.6 revision (forbidden without separately authorized formal cost-model revision phase) or (b) an R2 spec revision (forbidden without separately authorized formal R2 successor phase). Phase 3l found the cost model "B — conservative but defensible"; this question form attempts to circumvent that finding.

### 6.5 "Which 5m filter makes losing trades disappear?"

**Why forbidden:** Generic post-hoc rescue. Any sufficiently rich dataset contains *some* filter that retroactively excludes most losers in-sample. The exclusion rule is essentially guaranteed not to generalize and is essentially guaranteed to be a post-hoc loosening of whatever candidate it is applied to. Forbidden categorically.

### 6.6 General principle

Forbidden questions share a common structure: they search for a 5m parameter, threshold, filter, or rule that *retroactively improves* the in-sample performance of a retained-evidence candidate. All such questions are post-hoc loosening per Phase 2y §11.3.5 and are forbidden. Permitted questions (Q1–Q7) are *descriptive* — they characterize what happened in the 5m path of completed v002 trades — and produce findings that *cannot* by themselves authorize any retained-evidence candidate revision.

---

## 7. Diagnostic definitions (proposed; not computed)

The following diagnostic terms would be required by any future 5m diagnostics-execution phase. Each is defined here at the specification level. **No values are computed. No examples are computed. No dataset is queried.** The definitions themselves are part of Phase 3o's predeclaration discipline.

### 7.1 Immediate adverse excursion (IAE)

For a trade with entry at 15m bar `t_entry` (next-bar-open of the bar immediately after the signal-confirmation bar) and over a window of `N` 5m sub-bars (N = 1, 2, 3 typically), IAE is the maximum unrealized R *against* the trade direction across the N 5m sub-bars. Long-trade IAE: `(entry_price − min(low_t_entry+1, low_t_entry+2, ..., low_t_entry+N)) / R`. Short-trade IAE: `(max(high_t_entry+1, ..., high_t_entry+N) − entry_price) / R`. Reported per-trade and aggregated as distribution / mean / median.

### 7.2 Immediate favorable excursion (IFE)

Symmetric to IAE in the favorable direction. Long-trade IFE: `(max(high_t_entry+1, ..., high_t_entry+N) − entry_price) / R`. Short-trade IFE: `(entry_price − min(low_t_entry+1, ..., low_t_entry+N)) / R`.

### 7.3 First-5m-bar return

For a 15m trade entered at `t_entry`, the close-to-close (or open-to-close) return of the *first* 5m sub-bar after entry, in trade-direction-signed R units. Sign convention: positive when the 5m bar moved in the trade-favorable direction.

### 7.4 Max adverse excursion (MAE) over first N 5m bars

Same as IAE for N = 1, 2, 3, ..., extended to the trade's full holding-period. Generalization of IAE for path analysis across the full trade horizon.

### 7.5 Max favorable excursion (MFE) over first N 5m bars

Symmetric to MAE in the favorable direction.

### 7.6 Wick-stop event

A stop-violation event in which the 5m sub-bar containing the stop-trigger has its stop-violating extreme (low for long stops; high for short stops) beyond the stop level, *but* the same 5m sub-bar's close is back inside the position-favorable side of the stop level. The stop is triggered intrabar by the wick, not by sustained close-aligned action.

### 7.7 Sustained-stop event

A stop-violation event in which the 5m sub-bar containing the stop-trigger and *at least the next two consecutive 5m sub-bars* all close on the position-adverse side of the stop level. The stop is triggered by sustained price action, not by a transient wick.

### 7.8 Intrabar target touch

A 5m sub-bar within a trade's holding period whose extreme (high for long target; low for short target) reaches or exceeds the target level, *but* the trade was not actually exited at the target (because v002 backtests use bar-close confirmation rules and do not assume intrabar target fills unless the bar's *close* is also beyond the target).

### 7.9 Confirmed target touch

A 5m sub-bar within a trade's holding period whose *close* is beyond the target level. This is a stronger signal than intrabar target touch; the trade reached the target on a closed-bar basis.

### 7.10 Target-touch-then-stop

A trade whose holding period contains at least one intrabar or confirmed target touch but ultimately exits via STOP. The combination is the most diagnostically suggestive of "missed-target-then-reversed" path patterns *and* the most rescue-shaped (per §6.3 forbidden question form). The *count* and *distribution* of target-touch-then-stop events is permitted under Q3; *deriving an exit rule from them* is forbidden under §6.3.

### 7.11 Funding decay curve

For D1-A trades (Q4), a mean-cumulative-displacement curve at the 5, 10, 15, 30, 60-minute horizons after the funding-settlement event that triggered the entry. Displacement is measured in ATR(20) units, signed by the contrarian-direction the trade entered. A "fast-decay" curve has most of the displacement realized in the first 5–15 minutes; a "slow-decay" curve has displacement spread over the full 60 minutes or beyond.

### 7.12 Fill-assumption slippage proxy

For Q5, the difference between the 15m bar-open price (used by all v002 backtests as the next-bar-open fill assumption) and a probability-weighted 5m intrabar fill simulation. The probability weights for the 5m simulation are intentionally *not* defined here; that definition belongs in a future docs-only data-requirements / v003 planning memo (Option B in §14, *not started by Phase 3o*).

### 7.13 Mark/trade stop divergence

For Q6, the time difference (in 5m sub-bars) between the 5m sub-bar at which a mark-price-driven stop would have triggered and the 5m sub-bar at which a trade-price-driven stop would have triggered. Reported as a distribution; signed (mark-earlier vs trade-earlier).

### 7.14 Definition discipline

The above definitions are *proposed* and *predeclared*. Any future 5m diagnostics-execution phase, if ever authorized, may refine these definitions for computational specificity (e.g., handling of weekends, gaps, missing 5m bars) but may *not* fundamentally alter the conceptual content of any definition without amending Phase 3o through a separately authorized phase. Silent definitional drift is data dredging.

---

## 8. Data boundary

Phase 3o is a docs-only predeclaration memo. **No data is acquired by Phase 3o.** The following statements bound any future 5m diagnostics work:

### 8.1 No 5m data exists in current canonical v002 datasets

The current v002 dataset family (per `data/manifests/`) consists of 15m + 1h-derived + 15m mark-price + funding-event tables for BTCUSDT and ETHUSDT — *no 5m datasets*. The repository is unable to perform any 5m diagnostic computation today, and Phase 3o does not change that.

### 8.2 v002 verdicts must remain uncontaminated

R3 baseline-of-record, R2 FAILED, F1 HARD REJECT, and D1-A MECHANISM PASS / FRAMEWORK FAIL — other are all dataset-version-locked to v002. Any 5m-augmented re-analysis would constitute a *new* analysis under a *new* dataset version (or dataset-family extension) and a *new* phase authorization, *not* a reclassification of prior verdicts. Phase 3o reaffirms this principle from Phase 3n §8.5.

### 8.3 Any 5m data would need versioning

Per `docs/04-data/dataset-versioning.md`, adding a new interval set is a mandatory version bump for the affected dataset family. Any future 5m datasets must:
- Have explicit version IDs (`__vNNN`).
- Have manifest files describing source endpoint, symbol, interval, schema version, generation timestamp, predecessor-linkage to v002, and quality checks.
- Be immutable once published.
- Be linked to any future diagnostics report by version ID.

### 8.4 No v003 is created here

Phase 3o does *not* create v003. Phase 3o does *not* create supplemental v001-of-5m. Phase 3o does *not* generate or stage any new manifest. The v002 manifest set is untouched.

### 8.5 No data acquisition is authorized here

Phase 3o does *not* authorize 5m data download, 5m data fetch, 5m HTTP requests, 5m REST calls, 5m WebSocket subscriptions, archive imports, third-party dataset purchases, or any other form of data acquisition. The next operator decision menu (§14) lists 5m data-requirements / v003 planning memo as Option B (a docs-only successor). Selection of Option B would still not authorize data acquisition; data acquisition would require a *further* separately authorized phase beyond Option B.

---

## 9. Timestamp and leakage guardrails

Any future 5m diagnostics-execution phase, if ever authorized, must respect the following guardrails. These are guardrails for *any future authorization*, not Phase 3o requirements.

### 9.1 All timestamps UTC

Per `docs/04-data/timestamp-policy.md`, all canonical timestamps use UTC Unix milliseconds. 5m bars must use the same convention. No local-timezone storage. No daylight-saving-time-dependent logic.

### 9.2 5m bars must be completed before use

Per `docs/04-data/data-requirements.md` core principle 1, completed bars only. 5m partial bars must not be used for any diagnostic purpose. The same "completed bars only" rule that governs strategy decisions also governs diagnostic analysis.

### 9.3 No partial bars

Reaffirmation of 9.2. Specifically: a 5m bar's `close_time` (or `open_time + 5 × 60 × 1000 − 1`) must have passed before the bar is eligible for inclusion in any diagnostic computation.

### 9.4 5m / 15m alignment must be explicit

Per Phase 3n §7.6, mixing 5m and 15m introduces alignment risk. 15m `open_time` values are a strict subset of 5m `open_time` values (every third 5m boundary, where `open_time mod 900000 = 0` in milliseconds). Any join between 5m and 15m must use explicit point-in-time alignment logic. Implicit joins are forbidden.

### 9.5 No using 5m data before the 15m decision timestamp

This is the central no-leakage rule. For any 15m trade entered at `t_entry`, all diagnostic computation must use only 5m data with `open_time ≥ t_entry`. 5m data from *before* the 15m decision timestamp may not be used to retroactively redefine the trade entry, target, stop, or filter. Specifically: the 15m signal-confirmation bar, the 15m next-bar-open fill, and the 15m higher-timeframe-bias must all use the *same* point-in-time-valid logic that v002 backtests already use.

### 9.6 No target/stop path facts used to define entry filters

If a trade's 5m path (e.g., its intrabar target touch or wick-stop pattern) is observed, that observation must not be back-propagated into an entry filter. "Trades with 5m path X were unprofitable, so we will filter them at entry" is a form of look-ahead leakage even if the filter is technically computable from pre-entry 5m data, because the *filter definition* was derived from post-entry path observation.

### 9.7 No lookahead from future 5m sub-bars into entry decisions

Reaffirmation of 9.6. Specifically: 5m sub-bars *after* `t_entry` must not influence the *decision* to enter at `t_entry`. That decision is locked to v002 logic and must not be retroactively conditioned by post-entry 5m observations.

---

## 10. Analysis boundary

The following boundary is the *single most procedurally important* aspect of Phase 3o. Any future 5m diagnostics-execution phase must respect this boundary.

### 10.1 Allowed future diagnostics

A future 5m diagnostics-execution phase is *allowed* to:

- Compute the predeclared diagnostic terms (§7) on a separately authorized 5m dataset.
- Answer the predeclared questions Q1–Q7 (§5) using those computations.
- Classify each predeclared question's outcome as **informative**, **non-informative**, or **ambiguous** (§12).
- Produce diagnostic tables, distributions, and per-candidate summaries.
- Discuss what each finding *might* inform about future research direction.

### 10.2 Forbidden strategy evaluation

A future 5m diagnostics-execution phase is *forbidden* from:

- Computing §10.3 / §10.4 / §11.3 / §11.4 / §11.6 gate metrics on any 5m-augmented or 5m-derived dataset.
- Producing PROMOTE / FAIL / HARD REJECT verdicts of any kind.
- Recomputing aggregate metrics for any retained-evidence candidate.
- Re-running H0, R3, R1a, R1b-narrow, R2, F1, D1-A, or any controls.
- Treating diagnostic findings as strategy-evaluation evidence.

### 10.3 Forbidden parameter tuning

A future 5m diagnostics-execution phase is *forbidden* from:

- Searching parameter spaces (entry offsets, stop multipliers, target multipliers, time-stop bar counts, threshold values) for any retained-evidence candidate.
- Reporting "best parameter" values for any candidate.
- Reporting parameter-sensitivity surfaces for any candidate.

### 10.4 Forbidden threshold revision

A future 5m diagnostics-execution phase is *forbidden* from:

- Recommending any change to §10.3, §10.4, §11.3, §11.4, or §11.6.
- Recommending any change to catastrophic-floor predicate thresholds.
- Recommending any change to project-level locks (§1.7.3).

### 10.5 Forbidden candidate rescue

A future 5m diagnostics-execution phase is *forbidden* from:

- Producing a "rescue" framing for R2, F1, or D1-A.
- Producing a target-touch-based "improved exit rule" for any candidate.
- Producing a wick-stop-based "improved stop rule" for any candidate.
- Producing a funding-decay-based "improved holding period" for D1-A.
- Producing a fill-assumption-based "improved cost model" for any candidate.

### 10.6 Forbidden prior-verdict revision

A future 5m diagnostics-execution phase is *forbidden* from:

- Revising R3's baseline-of-record status.
- Revising R2's FAILED — §11.6 cost-sensitivity blocks status.
- Revising F1's HARD REJECT status.
- Revising D1-A's MECHANISM PASS / FRAMEWORK FAIL — other status.
- Revising H0's framework-anchor status.
- Producing any reclassification of any retained-evidence candidate.

### 10.7 Procedural enforcement

The above boundary is enforced procedurally by: (a) the Phase 3o predeclaration of the question set Q1–Q7, (b) the Phase 3o predeclaration of forbidden question forms (§6), and (c) the requirement that any subsequent verdict revision, parameter tuning, threshold revision, or candidate rescue be performed only through a separately authorized formal phase with predeclared evidence thresholds. *No 5m diagnostic finding by itself can trigger such authorization.* The trigger is operator-strategic, not data-driven.

---

## 11. Strategy-by-strategy diagnostic mapping

For each retained-evidence candidate, the following table maps the predeclared questions Q1–Q7 to the candidate's known failure mode, with explicit preservation of the candidate's terminal verdict.

### 11.1 R3 (V1 breakout, baseline-of-record)

| Question | Relevance to R3 | Reason |
|----------|-----------------|--------|
| Q1 | High | R3 entries may suffer immediate adverse excursion ("breakout front-running"). |
| Q2 | High | R3 stops are structural+ATR; wick-vulnerable in V1 breakout setups. |
| Q3 | Medium | R3 uses Fixed-R target; intrabar touches may exist but cannot license rescue. |
| Q4 | None | Q4 is D1-A-specific. |
| Q5 | High | R3's next-bar-open fill realism is directly relevant to its aggregate-negative net-of-cost expR. |
| Q6 | Medium | Mark/trade stop divergence is mechanism-relevant for R3's STOP-exit population. |
| Q7 | Applies | Meta. |

**Preserved status:** R3 remains V1 breakout baseline-of-record per Phase 2p §C.1 *regardless* of any Q1–Q7 finding.

### 11.2 R2 (V1 breakout pullback-retest entry)

| Question | Relevance to R2 | Reason |
|----------|-----------------|--------|
| Q1 | High | R2's pullback-retest entry depends critically on fill timing; first-5m-bar IAE is highly diagnostic. |
| Q2 | High | R2 stops at HIGH slippage are disproportionately sensitive (per Phase 2w §16.1). |
| Q3 | Medium | R2's M3 mechanism-support is target-related; intrabar touches may exist but cannot license rescue. |
| Q4 | None | Q4 is D1-A-specific. |
| Q5 | High | R2's §11.6 cost-fragility is directly downstream of fill realism. |
| Q6 | Medium | Mark/trade stop divergence is mechanism-relevant for R2's HIGH-slippage stop-trigger population. |
| Q7 | Applies | Meta. |

**Preserved status:** R2 remains FAILED — §11.6 cost-sensitivity blocks per Phase 2w §16.1 *regardless* of any Q1–Q7 finding. Q5 findings *cannot* by themselves revise §11.6; that requires a separately authorized formal cost-model revision phase.

### 11.3 F1 (mean-reversion-after-overextension)

| Question | Relevance to F1 | Reason |
|----------|-----------------|--------|
| Q1 | Medium | F1 STOP-exit immediate adverse excursion is informative but cannot revive F1. |
| Q2 | High | F1's 53–54% STOP exits at −1.30 / −1.24 R mean dominate the failure; wick vs sustained classification is directly relevant. |
| Q3 | Medium | F1's TARGET subset shows +1.86 R per trade when isolated; intrabar touches may exist but cannot license rescue. |
| Q4 | None | Q4 is D1-A-specific. |
| Q5 | Low | F1 fill realism is downstream of its catastrophic-floor failure mode. |
| Q6 | Medium | Mark/trade stop divergence is mechanism-relevant for F1's STOP-exit population. |
| Q7 | Applies | Meta. |

**Preserved status:** F1 remains HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate; Phase 3d-B2 is *terminal* for F1 *regardless* of any Q1–Q7 finding.

### 11.4 D1-A (funding-aware directional / carry-aware contrarian)

| Question | Relevance to D1-A | Reason |
|----------|-------------------|--------|
| Q1 | High | D1-A's 67–68% STOP exits at −1.24 / −1.30 R mean drove the FRAMEWORK FAIL; immediate adverse excursion is highly diagnostic. |
| Q2 | High | D1-A's STOP-exit population is mechanism-relevant; wick vs sustained classification informs the 32-bar holding-period mismatch hypothesis. |
| Q3 | Medium | D1-A's TARGET subset shows +2.143 / +2.447 R per trade when isolated; intrabar touches may exist but cannot license rescue. |
| Q4 | **Highest** | Q4 is D1-A-specific and is the highest-information-value question in the entire spec for D1-A. |
| Q5 | Medium | D1-A's funding-event-aligned next-bar-open is mechanism-relevant. |
| Q6 | Medium | Mark/trade stop divergence is mechanism-relevant for D1-A's STOP-exit population. |
| Q7 | Applies | Meta. |

**Preserved status:** D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2; Phase 3j is *terminal* for D1-A under current locked spec *regardless* of any Q1–Q7 finding. Q4 findings *may inform* a possible future operator decision about whether to authorize a D1-A-prime / D1-B / hybrid spec, but Phase 3o does *not* contemplate any such authorization.

### 11.5 Cross-candidate principle

The single highest-value 5m diagnostic question across all four candidates is Q1 (immediate adverse excursion). The single highest-information-value question for any specific candidate is Q4 (D1-A funding decay). The single highest-risk question is Q3 (intrabar target touches). *None* of the questions, including Q1 and Q4, can revise any prior verdict.

---

## 12. Required outputs of any future diagnostics phase

If a future 5m diagnostics-execution phase is ever authorized (separately from Phase 3o), it should produce *only* the following outputs:

### 12.1 Diagnostic tables only

Per-candidate tables of Q1–Q7 metrics across the v002-locked retained-evidence trade populations, with appropriate aggregations (mean / median / distribution by sub-period / by symbol / by exit-type). Tables, not interpretations.

### 12.2 No strategy verdicts

The output must not contain PROMOTE / FAIL / HARD REJECT / PASS / MECHANISM PASS classifications for any candidate. These classifications are forbidden in diagnostic outputs.

### 12.3 No parameter recommendations

The output must not recommend any change to entry offsets, stop multipliers, target multipliers, time-stop bar counts, threshold values, regime filters, cooldown rules, or any other strategy parameter.

### 12.4 No revised candidate labels

The output must not propose any reclassification of R3 / R2 / F1 / D1-A. The terminal verdicts remain.

### 12.5 No "rescue" conclusion

The output must not contain the words "rescue," "resurrect," "revive," "salvage," or any synonym applied to R2, F1, or D1-A. Diagnostic tables describe what happened; they do not advocate for action on the affected candidate.

### 12.6 Informative / non-informative / ambiguous classification

Each predeclared question Q1–Q7 must receive exactly one classification:

- **Informative** — the diagnostic produced a coherent, replicable, mechanism-relevant finding. Replicability requires consistency across BTC and ETH where applicable, across multiple non-overlapping date sub-ranges, and consistency with prior mechanism reasoning.
- **Non-informative** — the diagnostic produced patterns that are not coherent, not replicable, or not mechanism-relevant. A non-informative result is a *valid* output and should not trigger pressure to find rescue framings.
- **Ambiguous** — the diagnostic produced a result that is partially informative but inconclusive on the key mechanism question. Ambiguous results should be reported honestly, not interpreted toward action.

### 12.7 Output discipline

The output of a future 5m diagnostics-execution phase is a **memo plus tables**, *not* a memo plus tables plus recommendations. Recommendations belong in subsequent operator-driven decisions, not in the diagnostic output itself.

---

## 13. Stop conditions for any future diagnostics phase

The following stop conditions must apply to any future 5m diagnostics-execution phase. If any condition is met, the phase must stop, document the reason, and not produce diagnostic outputs.

### 13.1 Missing or incomplete 5m data

If the 5m dataset (whatever its version identity) has missing bars, gaps, or coverage shorter than the v002 backtest date range that is being analyzed, the phase must stop. Forward-fill, interpolation, and similar gap-handling are *not* acceptable for diagnostic analysis (per `docs/04-data/data-requirements.md` forbidden patterns).

### 13.2 Timestamp mismatch

If 5m and 15m timestamps cannot be aligned to UTC Unix millisecond precision, the phase must stop. Any 5m bar whose `open_time` does not satisfy `open_time mod 300000 = 0` is malformed; any 15m bar whose `open_time` does not satisfy `open_time mod 900000 = 0` is malformed.

### 13.3 Inability to align 5m and 15m bars safely

If the alignment logic between 5m and 15m bars cannot be tested for point-in-time validity (e.g., due to dataset versioning gaps, manifest inconsistencies, or schema drift), the phase must stop.

### 13.4 Insufficient trade coverage

If the 5m diagnostic computation cannot be performed on a meaningful fraction of the v002-locked retained-evidence trade population (e.g., due to gaps that systematically exclude specific exit-types or sub-periods), the phase must stop. "Meaningful fraction" should be defined in the docs-only diagnostics-execution plan, but cannot be lower than ≥80% of trades by count for any candidate.

### 13.5 Any temptation to alter candidate rules

If during the analysis the analyst (Claude Code, ChatGPT, or operator) experiences pressure to alter any retained-evidence candidate's rules, parameters, or thresholds, the phase must stop and escalate to the operator. Phase 3o's predeclaration discipline is meant to prevent this temptation from arising in the first place; if it arises anyway, that is itself a procedural failure mode.

### 13.6 Any data-quality concern that could create lookahead or survivorship bias

If during the analysis any data-quality concern emerges that could create lookahead leakage (e.g., 5m data containing future-aware features) or survivorship bias (e.g., 5m data missing for failed trades but present for successful trades), the phase must stop.

---

## 14. Operator decision menu after Phase 3o

The operator now has a docs-only diagnostics-spec memo predeclaring Q1–Q7 plus their definitions, guardrails, forbidden forms, and analysis boundary. The next operator decision is operator-driven only. The following paths are *possible*; Phase 3o recommends exactly one.

### 14.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategy-execution pause continues. Phase 3o joins Phase 3k / 3l / 3m / 3n as docs-only research-consolidation evidence. No 5m data acquired. No v003 created. No diagnostics executed.

**Reasoning:**

- Phase 3o has now realized its full *predeclaration* value: the question set, definitions, forbidden forms, analysis boundary, and stop conditions are all written down, immutable, and auditable on `main`. That value is realized whether or not any successor phase is authorized.
- The case for *running* the predeclared diagnostics is non-zero but provisional. The strongest single case (Q4 D1-A funding-decay curve) has high information value, but D1-A is already terminal under current spec; even an informative Q4 result could only inform a possible future operator decision, not authorize one.
- The procedural overhead of any 5m diagnostics-execution phase is significant: dataset-versioning work, data-acquisition authorization, predeclared-question discipline enforcement, anti-overfitting guardrails, and separation from prior verdicts. None of this overhead is justified without a specific operator-driven motivation that Phase 3o does not currently produce.
- The cumulative pattern across Phase 3k / 3l / 3m / 3n has been "remain paused" four times. Phase 3o adds another piece of *predeclaration*, not a piece of *evidence demanding action*.
- The forbidden-question discipline (§6) and analysis-boundary discipline (§10) are the most important Phase 3o outputs. They protect any future phase from the most dangerous post-hoc loosening patterns. That protection is realized now and persists indefinitely.

**What this preserves:** R3 baseline-of-record; H0 anchor; all retained-evidence verdicts; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; v002 dataset version; no paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write commitment.

**What this rules out:** No 5m data acquired. No v003 created. No diagnostics executed. No prior verdict revised. No successor authorized.

### 14.2 Option B — 5m data-requirements / v003 planning memo, docs-only (CONDITIONAL secondary alternative)

**Description:** Authorize a future docs-only memo that defines (a) which 5m datasets would be required to answer the predeclared Q1–Q7, (b) versioning options (v003 bump vs supplemental v001-of-5m), (c) timestamp-policy specifics for 5m, (d) data-quality checks, (e) a written decision about whether to actually proceed with 5m data acquisition. Still no data download, still no v003 created, still no analysis.

**Reasoning if selected:** Phase 3o §8 establishes the data boundary; a deeper docs-only data-requirements / v003 planning memo would be the *next-most-conservative* step beyond Phase 3o. It would still produce only documentation, not data, and not analysis. It would close the data-requirements gap before any data acquisition is even contemplated.

**Pre-conditions if selected:** Operator commits ex-ante to symmetric-outcome / anti-circular-reasoning discipline. Operator commits ex-ante that the data-requirements / v003 planning memo cannot itself authorize 5m data acquisition or analysis — a further phase would be required for that.

**Risks if selected:** Procedural escalation. Each successive docs-only memo creates institutional pressure to "do something with this," even if "remain paused" remains the right answer. Five docs-only memos already exist (3k / 3l / 3m / 3n / 3o); a sixth on essentially the same theme should be selected only if the operator has a specific motivating question that Phase 3o does not already address.

### 14.3 Option C — 5m diagnostics-execution plan, docs-only (CONDITIONAL tertiary alternative)

**Description:** Authorize a future docs-only memo that defines the *execution plan* for running Q1–Q7 against a (still-not-yet-acquired) 5m dataset. This memo would cover: methodology specifics (statistical aggregation choices, sub-period boundaries, BTC/ETH handling), output-format specifics (table schemas, classification logic), and stop-condition specifics. Still no data download, still no diagnostics executed.

**Reasoning if selected:** Phase 3o §10 / §12 / §13 establish the execution-discipline framework; a deeper docs-only diagnostics-execution plan would specify the *how* once the *what* (Q1–Q7) and *guardrails* are predeclared.

**Pre-conditions if selected:** Same as Option B. Plus: operator commitment that the diagnostics-execution plan memo cannot itself authorize 5m data acquisition or analysis.

**Risks if selected:** Same as Option B, with the additional risk that detailed execution planning creates institutional momentum toward execution. A predeclared execution plan is *not* a commitment to execute; this must be made explicit.

### 14.4 Option D — Regime-first formal spec memo, docs-only (LATERAL alternative)

**Description:** Authorize the docs-only formal regime-first spec memo that Phase 3m discussed but did not start.

**Reasoning if selected:** Independent of 5m. Some operators may decide that regime-first is a more promising direction than 5m diagnostics-spec follow-through.

**Phase 3o's view:** 5m and regime-first are different research tracks; choosing between them is an operator-strategic question, not a Phase 3o technical question. Phase 3m's recommendation was "remain paused" with regime-first formal spec as a possible future option. Phase 3o does not endorse or oppose this option relative to Option A; it is mentioned for completeness.

### 14.5 Option E — ML feasibility memo, docs-only (CONDITIONAL alternative)

**Description:** Authorize a docs-only memo evaluating whether ML feasibility work is appropriate.

**Reasoning if selected:** Independent of 5m. Phase 3k's decision menu listed ML feasibility as an option; it remains so.

**Phase 3o's view:** ML feasibility is a separate and significantly more complex question than 5m diagnostics. Phase 3o does not endorse this option as a near-term direction; it is mentioned for completeness.

### 14.6 Option F — New strategy-family discovery (NOT RECOMMENDED)

**Description:** Authorize a new strategy-family discovery phase analogous to Phase 3a (F1 family) or Phase 3f (D1-A family).

**Phase 3o's view:** Three strategy-research arcs have framework-failed under unchanged discipline. Starting a fourth without addressing *why* the first three failed (which 5m diagnostics or regime-first work might inform) is procedurally premature. Not recommended.

### 14.7 Option G — Paper/shadow planning, Phase 4, live-readiness, deployment, or strategy rescue (NOT RECOMMENDED)

**Description:** Authorize any phase beyond docs-only research consolidation.

**Phase 3o's view:** None of these are appropriate from the current state. R3 remains the strongest evidence the project has produced, but R3 alone does not constitute live-readiness evidence under `phase-gates.md` Phase 8 criteria. Strongly not recommended.

### 14.8 Recommendation

**Phase 3o recommends Option A (remain paused) as primary.**

Phase 3o's *predeclaration* value is fully realized by this memo itself. The forbidden-question discipline and the analysis-boundary discipline are the most procedurally important outputs and are realized now, regardless of any successor phase.

The case for *acting on* the predeclaration (even at the docs-only level of Option B or C) is weak in the absence of a specific operator-driven motivation that Phase 3o does not currently identify. The procedural escalation risk (each successive docs-only memo creating institutional pressure to act) is real and worth respecting.

Phase 3o explicitly does **NOT** recommend:

- Implementation of any kind.
- Backtesting of any kind.
- 5m data acquisition.
- v003 creation.
- 5m diagnostics execution.
- 5m strategy.
- Paper/shadow planning.
- Phase 4 runtime work.
- Live-readiness work.
- Deployment work.
- Strategy rescue (R2 / F1 / D1-A successor / D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / target-subset rescue / regime-conditioned rescue).
- ML feasibility.
- Cost-model revision.
- New strategy-family discovery.
- Project-lock revision.
- Threshold revision.

If the operator selects Option A, Phase 3o is closed and the project remains at the post-Phase-3o consolidated boundary.

If the operator selects Option B (5m data-requirements / v003 planning memo) or Option C (5m diagnostics-execution plan), each is conditional on explicit ex-ante operator commitment to symmetric-outcome / anti-circular-reasoning discipline and explicit ex-ante commitment that the docs-only memo cannot itself authorize data acquisition, diagnostics execution, or any prior-verdict revision. Selecting B or C does not authorize anything beyond the named docs-only memo.

Options D, E, F, and G are not recommended by Phase 3o.

---

## 15. Explicit preservation

This memo preserves the following items unchanged:

- **No threshold changes.** §10.3 (Δexp ≥ +0.10 R), §10.4 (absolute floors expR > −0.50 AND PF > 0.30), §11.3 (V-window no-peeking), §11.4 (ETH non-catastrophic), §11.6 (8 bps HIGH per side cost-resilience) preserved verbatim.
- **No strategy-parameter changes.** R3 sub-parameters preserved. F1 parameters preserved (8-bar cumulative displacement > 1.75 × ATR(20); SMA(8) target; structural stop with 0.10 × ATR buffer; 8-bar time-stop; same-direction cooldown until unwind). D1-A parameters preserved (|Z_F| ≥ 2.0 / 270 events / 1.0 × ATR(20) stop / +2.0 R target / 32-bar (8-hour) time-stop / per-funding-event cooldown / band [0.60, 1.80] × ATR / contrarian / no regime filter).
- **No project-lock changes.** §1.7.3 project-level locks (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets) preserved verbatim.
- **No prior verdict changes.** R3 remains V1 breakout baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 / F1 / D1-A remain retained research evidence only. R2 remains FAILED — §11.6 cost-sensitivity blocks. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other.
- **No backtests.** No backtest run by Phase 3o.
- **No data download.** No data fetched from any source by Phase 3o.
- **No v003 creation.** v002 datasets remain canonical; no v003 dataset created or staged.
- **No supplemental 5m dataset created.**
- **No derived 5m-resolution tables created.**
- **No 5m analysis.** No diagnostic computation performed. No diagnostic table produced. No diagnostic plot produced.
- **No timestamp-policy changes.**
- **No dataset-versioning policy changes.**
- **No cost-model revision.** Phase 3l's "B — current cost model conservative but defensible" assessment stands. §11.6 unchanged.
- **No regime-first authorization.** Phase 3m's "remain paused" recommendation stands.
- **No 5m timeframe authorization.** Phase 3n's "remain paused" recommendation stands.
- **No ML feasibility authorization.**
- **No new strategy-family discovery authorization.**
- **No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid authorization.**
- **No paper/shadow planning authorization.**
- **No Phase 4 runtime / state / persistence authorization.**
- **No live-readiness authorization.**
- **No deployment authorization.**
- **No production-key creation authorization.**
- **No exchange-write capability authorization.**
- **No MCP / Graphify / `.mcp.json` activation.** Project rules `.claude/rules/prometheus-mcp-and-secrets.md` preserved.
- **No credentials requested or used.**
- **No authenticated / private Binance API calls made.**
- **No data/ commits.** v002 manifests untouched. No new data files staged or committed.
- **No next phase started.**

The output of Phase 3o is this memo and the closeout report. No code, no tests, no scripts, no data, no thresholds, no strategy parameters, no project locks, no paper/shadow, no Phase 4, no live-readiness, no deployment, no credentials, no MCP, no Graphify, no `.mcp.json`, and no exchange-write work has changed.

Phase 3o is a docs-only diagnostics-spec memo. The operator decides what (if anything) follows.
