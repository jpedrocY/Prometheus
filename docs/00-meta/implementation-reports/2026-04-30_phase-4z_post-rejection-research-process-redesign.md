# Phase 4z — Post-Rejection Research-Process Redesign Memo

**Authority:** Operator authorization for Phase 4z (Phase 4y §"Operator decision menu" Option B conditional secondary alternative — docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo, only if separately authorized; operator has so chosen). Phase 4y (post-C1 strategy research consolidation memo); Phase 4x (C1 backtest execution; Verdict C HARD REJECT — terminal for C1 first-spec); Phase 4w (C1 backtest-plan methodology); Phase 4v (C1 strategy spec); Phase 4u (C1 hypothesis-spec); Phase 4t (post-G1 fresh-hypothesis discovery memo); Phase 4s (post-G1 strategy research consolidation); Phase 4r (G1 backtest execution; Verdict C HARD REJECT — terminal for G1 first-spec); Phase 4q (G1 backtest-plan methodology); Phase 4p (G1 strategy spec); Phase 4o (G1 hypothesis-spec); Phase 4n (post-V2 fresh-hypothesis discovery memo); Phase 4m (post-V2 consolidation memo; 18-requirement fresh-hypothesis validity gate); Phase 4l (V2 backtest execution; Verdict C HARD REJECT — terminal for V2 first-spec); Phase 4k (V2 backtest-plan methodology); Phase 4j §11 (metrics OI-subset partial-eligibility binding); Phase 4i (V2 acquisition); Phase 4h (V2 data-requirements / feasibility memo); Phase 4g (V2 strategy spec); Phase 4f (external strategy research landscape memo + V2 candidates); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3r §8 (mark-price gap governance); Phase 3t §12 (validity gate for any future research); Phase 3k (post-D1-A consolidation); Phase 3e (post-F1 consolidation); Phase 2p §C.1 (R3 baseline-of-record); Phase 2i §1.7.3 (project-level locks); `docs/03-strategy-research/v1-breakout-strategy-spec.md`; `docs/03-strategy-research/v1-breakout-backtest-plan.md`; `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4z — **Post-Rejection Research-Process Redesign Memo** (docs-only). Examines the project's strategy-research process after six categorically distinct failure modes (R2 / F1 / D1-A / V2 / G1 / C1), separates what worked from what failed in the process, identifies weaknesses in candidate discovery, hypothesis-quality framing, baseline design, mechanism-check framing, opportunity-rate handling, search-space-control, stop-condition design, and no-rescue enforcement, and **proposes** stricter future research-process requirements for any future docs-only fresh-hypothesis discovery cycle. **Phase 4z is text-only.** No new strategy candidate is created or named; no fresh-hypothesis discovery memo is created; no strategy-spec or backtest-plan memo is created; no backtest is run; no Phase 4x rerun is permitted; `scripts/phase4x_c1_backtest.py` is NOT modified; no implementation code is written; no data is acquired or modified; no manifest is modified; no retained verdict is revised; no project lock is changed; no governance file is amended; no successor phase is authorized. Phase 4z's proposed redesigns are **recommendations** for future memos, not adopted governance.

**Branch:** `phase-4z/post-rejection-research-process-redesign`. **Memo date:** 2026-05-04 UTC.

---

## Summary

Phase 4z is the project's first post-rejection research-process redesign memo, authored after the cumulative six-failure-mode rejection ledger (R2 cost-fragility; F1 catastrophic-floor / bad full-population expectancy; D1-A mechanism / framework mismatch; V2 design-stage incompatibility; G1 regime-gate-meets-setup intersection sparseness; C1 fires-and-loses / contraction anti-validation) reached a point where the operator authorized a docs-only examination of the *process itself* rather than another fresh-hypothesis discovery cycle. Phase 4z is the Phase 4y §"Operator decision menu" Option B conditional secondary alternative; Phase 4y did not authorize Phase 4z, but the operator has now separately authorized Phase 4z on the conditional-secondary path.

**The central observation Phase 4z records:** the project's strategy-research process is *procedurally* sound — predeclaration discipline has worked, branch isolation has worked, no governance leakage has occurred across six rejection events — but the process is *substantively* under-constrained at the **discovery and admissibility layer**. The 18-requirement Phase 4m fresh-hypothesis validity gate and the Phase 4t 10-dimension scoring matrix together produced a research arc (Phase 4n → 4o → 4p → 4q → 4r for G1; Phase 4t → 4u → 4v → 4w → 4x for C1) where each candidate was disciplined, predeclared, and tested with §11.6 cost realism, but in which the candidate-discovery process repeatedly produced ideas adjacent to (rather than theoretically distant from) the rejected ledger. Phase 4z does NOT conclude that the gate is wrong; it concludes that the gate's **implicit assumptions about candidate-distinction quality, baseline-superiority predeclaration, opportunity-rate-versus-edge-rate separation, and no-rescue adjacency-mapping** were not strong enough to surface ex-ante what is now visible ex-post: that V2 / G1 / C1 are categorically adjacent in the "mechanical condition + breakout" design family even though each was theoretically distinct from prior rejected forms.

**Phase 4z proposes stricter future requirements** at the discovery, hypothesis-spec, backtest-plan, and execution-report layers. These are *recommendations for any future research-process memo*, not adopted governance changes. Phase 4z does NOT amend the Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, the Phase 4u opportunity-rate principle, the Phase 4w negative-baseline / PBO / DSR / CSCV methodology, the Phase 4j §11 metrics OI-subset partial-eligibility rule, the Phase 4k V2 backtest-plan methodology, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, the Phase 3r §8 mark-price gap governance, §11.6 = 8 bps HIGH per side, or §1.7.3 project-level locks. Each retained verdict (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained-non-leading; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 HARD REJECT; G1 HARD REJECT; C1 HARD REJECT) is preserved verbatim.

**Phase 4z recommendation:** Option A — **remain paused** as primary; Option B — **docs-only documentation-refresh / governance-template update memo** (only if separately authorized) as conditional secondary. Phase 4z does NOT recommend immediate fresh-hypothesis discovery, strategy-spec, backtest-plan, backtest-execution, implementation-readiness work, data acquisition, paper / shadow / live, or Phase 4 canonical. Phase 4z does NOT authorize Phase 5 / Phase 4aa / any successor phase. Phase 4z does NOT authorize paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials.

## Authority and boundary

- **Authority granted:** create the Phase 4z docs-only research-process redesign memo on branch `phase-4z/post-rejection-research-process-redesign`; review the cumulative six-failure-mode rejection ledger; assess the existing research process (Phase 4m gate; Phase 4u opportunity-rate principle; Phase 4w negative-baseline / PBO / DSR / CSCV framework; Phase 4t 10-dimension scoring matrix; Phase 4l / 4r / 4x execution patterns); identify weaknesses; propose stricter future requirements as recommendations for any future research-process memo; create the Phase 4z closeout file; commit on the Phase 4z branch and push; do NOT merge to main unless explicitly instructed after review.
- **Authority NOT granted:** create a new strategy candidate (forbidden); name a new candidate (forbidden); create a fresh-hypothesis discovery memo (forbidden — would itself require separate operator authorization analogous to Phase 4n / 4t); create a strategy-spec memo (forbidden); create a backtest-plan memo (forbidden); run any backtest (forbidden); rerun Phase 4x (forbidden); modify `scripts/phase4x_c1_backtest.py` or any other existing script (forbidden); write implementation code (forbidden); modify `src/prometheus/`, tests, or scripts (forbidden); acquire / download / patch / regenerate / replace data (forbidden); modify `data/raw/`, `data/normalized/`, or `data/manifests/` (forbidden); commit `data/research/` outputs (forbidden); create v003 (forbidden); revise any retained verdict (forbidden); change any project lock (forbidden); amend `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, or any specialist governance file (forbidden); authorize Phase 5 / Phase 4aa / any successor phase (forbidden); authorize paper / shadow / live / exchange-write / production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials (forbidden); merge Phase 4z to main without explicit instruction (forbidden).
- **Hard rule:** Phase 4z is text-only. No code is written. No data is touched. No backtest is run. No new strategy candidate is named or specified. No governance file is amended. The proposed redesigns are **recommendations** that any future research-process memo could choose to adopt, not adopted requirements.

## Starting state

```text
Branch (Phase 4z):    phase-4z/post-rejection-research-process-redesign
main / origin/main:   8e94fb01951e07d428046026750f20197dfe9890 (unchanged)
Phase 4y merge:       69579c15f4ddc15cf79edbf22a67daa84a43f765 (merged)
Phase 4y housekeep:   8e94fb01951e07d428046026750f20197dfe9890 (merged)
Working-tree state:   clean (no tracked modifications); only gitignored
                      transients .claude/scheduled_tasks.lock and
                      data/research/ are untracked and will not be
                      committed.
Quality gates (verified at memo creation):
  ruff check . PASS
  pytest 785 PASS
  mypy strict 0 issues across 82 source files
```

## Why this memo exists

Phase 4y recommended remain-paused as primary and a docs-only post-rejection research-process redesign memo as conditional secondary. The operator has now authorized the conditional-secondary path. Phase 4z exists because:

1. **The cumulative rejection ledger has a structural shape.** Six rejection events with six categorically distinct failure modes is a research-record signal worth examining at the process level, separate from the per-strategy consolidation memos (Phase 3e for F1, Phase 3k for D1-A, Phase 4m for V2, Phase 4s for G1, Phase 4y for C1). Each consolidation memo correctly preserved verdicts and refused rescue, but none of them re-examined the **discovery / admissibility process** that fed candidates into the rejection ledger.
2. **The G1 → C1 sequence revealed a discovery-process gap.** Phase 4n (post-V2 discovery) recommended Candidate B Regime-First Breakout → became G1 → terminated at Verdict C HARD REJECT. Phase 4t (post-G1 discovery) recommended Candidate D Volatility-Contraction Expansion Breakout → became C1 → terminated at Verdict C HARD REJECT. Two disciplined fresh-hypothesis cycles in a row produced rejected hypotheses; the discovery process is *consistent* but its *yield* is insufficient. A research-process redesign is the appropriate response to the pattern.
3. **The C1 result revealed a new evidence layer.** V2 and G1 were zero-trade non-evidence-generating failures; C1 fired plenty of trades and produced strictly-negative differentials against three independent baselines. C1's failure mode (fires-and-loses / contraction anti-validation) cannot be addressed by tightening opportunity-rate floors alone — it requires **explicit pre-data baseline-superiority predeclaration** and an **edge-rate viability gate distinct from the opportunity-rate viability gate**.
4. **A research-process redesign is itself a remain-paused-compatible activity.** Phase 4z does not authorize any successor strategy phase. It captures process learnings into the project record so that *if* the operator ever authorizes a future fresh-hypothesis discovery cycle, that cycle has stricter admissibility constraints to clear. If the operator chooses to remain paused indefinitely, Phase 4z's redesigns simply remain dormant; no harm is done.

Phase 4z is **not** a fresh-hypothesis discovery memo, **not** an implementation-readiness scoping memo, and **not** a documentation-refresh memo. It is specifically a **process-redesign memo** focused on the research process upstream of any future hypothesis spec.

## Relationship to Phase 4y

- Phase 4y merged the Post-C1 Strategy Research Consolidation Memo into `main` at SHA `69579c15f4ddc15cf79edbf22a67daa84a43f765` with housekeeping at SHA `8e94fb01951e07d428046026750f20197dfe9890`.
- Phase 4y recommended **Option A — remain paused (primary)** and recorded **Option B — docs-only post-rejection research-process redesign / hypothesis-discovery process redesign memo (conditional secondary; only if separately authorized; not started by Phase 4y)**.
- The operator has now separately authorized Phase 4z on the conditional-secondary path.
- Phase 4z is **docs-only** and inherits all Phase 4y constraints verbatim:
  - No new strategy candidate is created or named.
  - No fresh-hypothesis discovery memo is created.
  - No strategy-spec or backtest-plan memo is created.
  - No backtest is run.
  - No Phase 4x rerun.
  - `scripts/phase4x_c1_backtest.py` is NOT modified.
  - No implementation code is written.
  - No data is acquired or modified.
  - No manifest is modified.
  - No retained verdict is revised.
  - No project lock is changed.
  - No governance file is amended.
  - No successor phase is authorized.

Phase 4z explicitly does NOT amend the Phase 4m 18-requirement validity gate, Phase 4t 10-dimension scoring matrix, Phase 4u opportunity-rate principle, Phase 4w negative-baseline / PBO / DSR / CSCV methodology, Phase 4v C1 strategy spec, Phase 4j §11 metrics OI-subset partial-eligibility rule, Phase 4k V2 backtest-plan methodology, Phase 3v §8 stop-trigger-domain governance, Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, Phase 3r §8 mark-price gap governance, §11.6 = 8 bps HIGH per side, or §1.7.3 project-level locks. The redesigns proposed below are **recommendations** that a future research-process memo (if ever authorized) could choose to adopt; they are not adopted governance.

## Full retained-verdict ledger

```text
H0           : FRAMEWORK ANCHOR (preserved)
R3           : BASELINE-OF-RECORD (preserved)
R1a          : RETAINED — NON-LEADING (preserved)
R1b-narrow   : RETAINED — NON-LEADING (preserved)
R2           : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1           : HARD REJECT (preserved)
D1-A         : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
5m thread    : OPERATIONALLY CLOSED (Phase 3t; preserved)
V2           : HARD REJECT — terminal for V2 first-spec
                (Phase 4l — Verdict C; CFP-1 critical;
                preserved)
G1           : HARD REJECT — terminal for G1 first-spec
                (Phase 4r — Verdict C; CFP-1 critical binding;
                CFP-9 independent; preserved)
C1           : HARD REJECT — terminal for C1 first-spec
                (Phase 4x — Verdict C; CFP-2 binding;
                CFP-3 / CFP-6 co-binding; CFP-1 / CFP-9
                explicitly did NOT trigger; preserved)

§11.6        : 8 bps HIGH per side (preserved verbatim)
§1.7.3       : 0.25% risk / 2× leverage / 1 position / mark-price stops
                (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x / 4y
                            : all preserved verbatim
Phase 4z                    : Post-rejection research-process redesign memo
                              (this phase; new; docs-only; not merged;
                              proposes recommendations only — does NOT
                              amend any prior governance)
```

**No verdict is revised by Phase 4z. No project lock is changed by Phase 4z. No governance file is amended by Phase 4z.**

## Six-failure topology recap

| # | Strategy | Failure mode | Evidence layer | Process requirement Phase 4z observes |
| --- | --- | --- | --- | --- |
| 1 | **R2** (pullback-retest entry) | **Cost-fragility** | Mechanism generated; cost survival failed (§11.6 HIGH blocks) | Future hypotheses must demonstrate first-principles cost-survival plausibility under §11.6 = 8 bps HIGH *before* spec-promotion, not as a retrospective check. Cost is not an afterthought; it is a primary-design constraint. |
| 2 | **F1** (mean-reversion-after-overextension) | **Catastrophic-floor / bad full-population expectancy** | Mechanism generated; full framework failed (M1 PARTIAL; M2 FAIL/weak; M3 PASS-isolated; CFP-1-equivalent triggered 5×) | Mechanism-isolated PASS (TARGET-subset profitability) is research evidence, not promotion evidence. Future specs must explicitly distinguish "mechanism subset positive" from "full population positive" and treat the latter as the binding criterion. |
| 3 | **D1-A** (funding-Z-score contrarian) | **Mechanism / framework mismatch** | Partial mechanism PASS (M1 BTC h=32 ✓); framework FAIL (cond_i / cond_iv) | Mechanism PASS does not imply framework PASS. Future specs must predeclare *both* a mechanism-check pass criterion *and* a framework-promotion pass criterion, and a mechanism-only positive result must be explicitly classified as research-evidence-only with no successor authorization. |
| 4 | **V2** (participation-confirmed trend continuation) | **Design-stage incompatibility** | Zero trades (CFP-1 critical: 512/512 variants below 30 OOS trades; train-best 0 OOS trades) | Setup geometry / structural stop / target / sizing / cost / timeframe / exit must be co-designed from first principles in a single integrated step. V1-inherited filters (such as the 0.60–1.80 × ATR stop-distance bound) cannot be passively re-imposed on a new strategy without first confirming compatibility with the new setup geometry. The Phase 4m 18-requirement gate's requirement #4 already says this; the V2 lesson is that requirement #4 must be enforced *operationally* during spec-review, not merely listed. |
| 5 | **G1** (regime-first breakout continuation) | **Regime-gate-meets-setup intersection sparseness** | Zero qualifying trades (CFP-1 critical; CFP-9 independent; regime active fraction 2.03%) | Multi-condition AND classifiers naturally produce sparse intersections with downstream entry rules. Future specs that compose multiple conditions must predeclare *the joint event rate* (regime_active AND setup AND stop_distance_passes) before any data is touched, derived from first-principles intrinsic frequency expectations rather than from observed forensic numbers. |
| 6 | **C1** (volatility-contraction expansion breakout) | **Fires-and-loses / contraction anti-validation** | Plenty of trades (149 BTC OOS HIGH; rate 3.33 / 480 bars; 100% of variants ≥ 30 trades); strictly-negative differentials vs three baselines (M1 -0.244R CI [-0.41, -0.08]; M2.a -0.220R CI [-0.39, -0.06]; M2.b -0.293R) | Opportunity-rate viability ≠ edge-rate viability. Future specs must predeclare an explicit **expected baseline-differential** before any data is touched, with bootstrap-CI-based pass/fail, and treat an empirically-negative baseline differential as terminal evidence against the hypothesis (not a tuning input). The C1 lesson is that "the strategy fired enough trades" can coexist with "the strategy is anti-predictive" and the project must have a process that surfaces this distinction ex-ante. |

The six modes are **categorically distinct** (no two are reducible to a common cause), but they share a process-level pattern: **each was caught by the existing predeclaration discipline and CFP framework, but each emerged from a discovery process that did not adequately surface its specific failure-shape ex-ante**. Phase 4z's redesigns target this discovery-and-admissibility gap.

## Assessment of the current research process

Phase 4z separates the research process into ten functional layers and assesses each.

### Layer A — Authorization and branch isolation

**Worked.** Every research phase from Phase 4f onward was operator-authorized as a discrete docs-only or docs-and-code unit, branched, scoped, executed, reported, and either merged or paused. No phase has been authorized "by default"; no phase has bypassed the authorization gate; no branch has merged without explicit operator instruction. **No process redesign needed.**

### Layer B — Predeclaration discipline

**Worked.** Every strategy spec (Phase 4g for V2; Phase 4p for G1; Phase 4v for C1) predeclared timeframes, signal rules, structural stop, target, sizing, cost cells, threshold grid, and validation windows *before* data was touched. Every backtest plan (Phase 4k for V2; Phase 4q for G1; Phase 4w for C1) predeclared methodology, mechanism checks, CFPs, reporting tables, plots, stop conditions, and reproducibility requirements *before* the script was written. No backtest reused thresholds chosen from prior failure forensic numbers. Bailey et al. 2014 anti-data-snooping discipline has been honored. **No process redesign needed.**

### Layer C — Forbidden-input enforcement

**Worked.** Every backtest reported audit-zero CFP-10 / CFP-11 / CFP-12 (forbidden-input access counts; lookahead violations; data governance violations all 0). Phase 4l (V2), Phase 4r (G1), and Phase 4x (C1) each had standalone-script boundaries with no `prometheus.runtime` / `execution` / `persistence` imports, no exchange adapters, no `requests` / `httpx` / `aiohttp` / `urllib3` / `urllib.request` / `websockets` / `websocket`, no `.env`, no credentials, no Binance API, no network I/O. **No process redesign needed.**

### Layer D — Cost realism

**Worked.** §11.6 = 8 bps HIGH per side has been preserved verbatim across V2, G1, C1; Phase 3l "B — conservative but defensible" cost-model assessment has not been amended; no candidate has been allowed to relax cost realism. **No process redesign needed.**

### Layer E — Variant-grid / DSR / PBO / CSCV discipline

**Worked.** V2 used a 512-variant grid (= 2^9); G1 and C1 used 32-variant grids (= 2^5). DSR (Bailey & López de Prado 2014) was computed with skew/kurtosis correction. PBO (train→validation rank-based, train→OOS rank-based, CSCV) was computed exactly with no silent approximation; CSCV S = 16 with C(16, 8) = 12 870 combinations was honored in all three cases. **No process redesign needed at this layer**, though Phase 4z notes that the C1 result demonstrated PBO low + DSR strongly negative as a useful diagnostic — when the strategy is broadly negative (no "lucky" overfit subset), PBO does not detect overfitting and DSR carries the binding signal. This is a useful observation for any future memo's CFP-6 design.

### Layer F — Negative-baseline framework (Phase 4w)

**Worked, but only at C1.** Phase 4k (V2) did not include explicit negative baselines because V2 produced zero trades (CFP-1 critical), making baseline computation methodologically inert. Phase 4q (G1) included an active-vs-inactive M1 framework (negative test) and an always-active M2 framework, but these too were methodologically inert under G1's 0-active-trade outcome. **Phase 4w (C1) was the first phase where the negative-baseline framework was binding and produced informative evidence.** The C1 result (M1 -0.244R CI strictly negative; M2.a -0.220R CI strictly negative; M2.b -0.293R) is a *new* kind of evidence in the project record: not zero trades, not catastrophic-floor expectancy, but strictly-negative differential vs. three independent baselines. **Phase 4z observes** that the negative-baseline framework should be *binding from the spec-review layer onward* for any future hypothesis, not introduced only at the backtest-plan layer. Future specs should explicitly predeclare **expected baseline differentials** with first-principles justification before backtesting begins.

### Layer G — Opportunity-rate framework (Phase 4u)

**Worked, but with a now-visible gap.** Phase 4u predeclared opportunity-rate viability as intrinsic to the contraction-to-expansion theory (a Phase 4u §6 binding hypothesis clause). Phase 4v / Phase 4w made it a binding gate via CFP-9 with explicit floors (≥1 candidate transition per 480 30m bars; trade_count ≥ 30 for the train-best variant; ≥50% of variants must produce trade_count ≥ 30 on BTC OOS HIGH). Phase 4x demonstrated that the framework was implementable and the gate was meaningful — C1 satisfied CFP-9 (rate 3.33; 100% pass). **The gap Phase 4z observes:** opportunity-rate viability ≠ edge-rate viability, but the existing framework treats them as a single gate. C1's evidence-generating negative result demonstrates that a strategy can satisfy CFP-9 and still be anti-predictive. **Phase 4z proposes** an additional **edge-rate viability gate** distinct from the opportunity-rate viability gate (see §"Opportunity-rate versus edge-rate redesign" below).

### Layer H — Mechanism-check framework

**Worked operationally, but with admissibility-layer weakness.** Phase 4q (G1) and Phase 4w (C1) each predeclared M1 / M2 / M3 / M4 mechanism checks with bootstrap-CI thresholds. The Phase 4w M1 / M2.a / M2.b / M3 / M4 / M5 framework is the project's most mature mechanism-check shape. **The gap Phase 4z observes:** the framework operates correctly during execution, but the project does not have an **M0 theoretical-admissibility gate** *upstream* of the strategy-spec phase. M0 would ask: "Why should this strategy's primary condition outperform an unconditioned baseline before we spend Phase 4u → 4v → 4w → 4x effort on it?" The C1 lesson is that this question, asked seriously and with first-principles answer, would have surfaced a key risk: the C1 hypothesis predicted that contraction releases would be directionally informative, but no first-principles theoretical case was made for **why** contraction-tied transitions should outperform unconditioned same-geometry transitions on BTCUSDT 30m perpetual futures. The hypothesis was *plausible*; it was not *theoretically distinguished from its closest baseline*.

### Layer I — Discovery method (Phase 4n / 4t)

**Worked procedurally, but with substantive distinction-quality weakness.** Phase 4n introduced a four-candidate evaluation; Phase 4t expanded to an eight-candidate evaluation with a 10-dimension scoring matrix (D1–D10). Both memos correctly recommended remain-paused as primary and a single conditional-secondary candidate. The discipline of evaluating multiple candidate spaces against a structured matrix is correct. **The gap Phase 4z observes:** the 10 dimensions emphasize *avoidance* of prior failure modes (D2 distance from forbidden rescue) and *operational feasibility* (D3 opportunity-rate; D5 data feasibility; D6 cost-survival plausibility; D7 mechanism-check designability; D9 implementation complexity), but they do not adequately emphasize **theoretical novelty in a positive sense** — i.e., the candidate's first-principles thesis for why its primary condition is *positively predictive* against an unconditioned baseline. The 10-dimension matrix correctly filters for "is this candidate a hidden rescue?" and "is this candidate operationally implementable?", but it does not strongly filter for "is this candidate's core thesis substantively new and theoretically grounded?" Phase 4z proposes a **theoretical-distinction matrix** (see §"Future hypothesis admissibility framework") to complement D1–D10.

### Layer J — Consolidation-memo discipline

**Worked.** Phase 3e (post-F1), Phase 3k (post-D1-A), Phase 4m (post-V2), Phase 4s (post-G1), and Phase 4y (post-C1) have produced a consistent post-rejection consolidation pattern: preserve verdicts; update the rejection topology; extract reusable insights; explicitly forbid rescue; recommend remain-paused as primary. The consolidation discipline has been the project's strongest defense against rescue-pattern drift. **No process redesign needed at the consolidation layer**, but Phase 4z observes that **consolidation memos themselves are not the place to redesign the discovery process** — that is exactly Phase 4z's role and would be the role of any future research-process memo. Future consolidation memos should continue to focus on verdict preservation and rescue-prevention; process redesign belongs in dedicated process-redesign memos.

## What worked in the research process

Synthesizing across the ten layers above, the following components of the existing process worked and should be preserved:

1. **Strict docs-first sequence.** Every strategy arc moved through hypothesis-spec (Phase 4u for C1; Phase 4o for G1; Phase 4f-4g for V2) → strategy-spec (Phase 4v / 4p / 4g) → backtest-plan (Phase 4w / 4q / 4k) → backtest-execution (Phase 4x / 4r / 4l) → consolidation (Phase 4y / 4s / 4m) → discovery (Phase 4t / 4n) phases, with each phase being a separate operator-authorized unit. The sequence prevented one-shot full-strategy work.
2. **Branch isolation.** Each phase has its own branch; merges to main require separate operator authorization with housekeeping commits.
3. **No premature implementation.** No strategy has been implemented in `src/prometheus/` from research evidence alone; runtime infrastructure (Phase 4a) is strategy-agnostic.
4. **No live path.** No paper / shadow / live operation has been attempted. No production keys have been created. No exchange-write capability exists.
5. **Explicit project locks.** §11.6 = 8 bps HIGH per side; §1.7.3 0.25% / 2× / one-position; mark-price stops; Phase 3v / 3w / 3r / 4j §11 governance — all preserved verbatim across six rejection events with no leakage.
6. **Backtest plans before execution.** Phase 4k / 4q / 4w predeclared methodology before the script was written. No execution phase introduced new methodology.
7. **Forbidden-input enforcement.** Every backtest produced audit-zero CFP-10 / CFP-11 / CFP-12 counters. No execution phase silently consumed forbidden inputs.
8. **Negative baselines were introduced and worked at C1.** Phase 4w's binding negative-test framework produced strictly-negative bootstrap CIs at C1, the first phase where this evidence shape was achievable.
9. **Opportunity-rate floors worked at C1.** CFP-9 was a binding pre-condition; CFP-9 and CFP-1 are independent gates.
10. **PBO / DSR / CSCV discipline worked.** Bailey et al. 2014 / Bailey & López de Prado 2014 corrections were computed exactly at C1; PBO_cscv = 0.094 demonstrated low overfitting; DSR = -20.82 carried the binding signal independently.
11. **Merge closeouts and current-project-state synchronization.** Each merge produced a closeout file recording verdict and project-state delta. `current-project-state.md` is updated narrowly at each merge to preserve historical phase context. The project record is *complete* after Phase 4y.

## What failed in the research process

The following process gaps Phase 4z identifies (these are observations, not corrections to existing governance):

1. **Repeated candidate ideas clustered around breakout / trend continuation variants.** V2 (participation-confirmed trend continuation), G1 (regime-first breakout continuation), and C1 (volatility-contraction expansion breakout) are all variations on a "mechanical condition + breakout" design family. Each was theoretically distinct from the others by some axis, but none represented a substantively orthogonal mechanism (e.g., relative-value, statistical arbitrage, intermarket-relationship, calendar / event, microstructure-derived). The discovery process produced candidates from a narrow cone of design space.
2. **Discovery did not sufficiently penalize "mechanical condition + breakout" designs.** The Phase 4t 10-dimension matrix identified V2 / G1 / R2 / F1 / D1-A as rescue traps to avoid (D2), but did not identify the **shared design family** that V2, G1, and C1 all occupy. A "design-family adjacency" check would have flagged C1 as occupying the same family as V2 and G1 even though it was theoretically distinct from each one individually.
3. **Theory-to-baseline superiority was under-specified before C1.** The Phase 4u C1 hypothesis-spec stated qualitatively that "compression releases improve directional breakout outcomes" but did not require a first-principles **expected baseline differential** with predicted magnitude and CI. The Phase 4v C1 strategy-spec set numeric M1 / M2 thresholds (≥+0.10R, ≥+0.05R) but did not require ex-ante justification of these magnitudes from theory. This left the empirical CI -0.41R to -0.08R as a surprise rather than a confirmation or rejection of a stated prediction.
4. **Fresh-hypothesis gates did not require enough proof that the core condition should outperform a same-geometry unconditioned baseline.** The Phase 4m 18-requirement gate's requirement #6 ("predeclare mechanism checks") and requirement #15 ("distinguish mechanism evidence from framework promotion") are correct but operate at the *backtest-plan layer*, not at the *hypothesis-admissibility layer*. The C1 lesson is that the baseline-superiority case must be argued *before* the hypothesis is admitted, not only validated *after* the backtest.
5. **The process allowed too much effort to be expended on theoretically weak edges.** From Phase 4n (post-V2 discovery) through Phase 4r (G1 execution) was approximately one G1 research arc; from Phase 4t (post-G1 discovery) through Phase 4x (C1 execution) was approximately one C1 research arc. Each arc was procedurally clean but ended in HARD REJECT. Phase 4z observes that an arc-economy view would prefer **fewer, more theoretically grounded candidates** over **more, more disciplined-but-weak candidates**.
6. **Remain-paused was treated as a boundary but not converted into a stronger discovery-process reset until now.** Phase 4m (post-V2) and Phase 4s (post-G1) both recommended remain-paused as primary, both correctly forbade rescue, but neither triggered a *discovery-process redesign*. Phase 4y (post-C1) for the first time identified the conditional-secondary path "docs-only post-rejection research-process redesign memo" and the operator authorized Phase 4z. The lesson is that *consolidation memos do not trigger process redesign*; process redesign requires a separate authorization, which Phase 4z is the first instance of in the project record.

## Candidate-discovery weakness analysis

V2 / G1 / C1 are theoretically distinct from each other by Phase 4t's D1 measure, but they share a **design-family signature**:

- **Setup mechanism:** all three use a per-bar mechanical condition computed on prior-completed kline data (V2: participation features + trend bias; G1: multi-dimension regime classifier; C1: compression-box state) combined with a breakout-style entry trigger (V2: Donchian breakout; G1: 12-bar Donchian breakout; C1: close-beyond-compression-box-with-buffer).
- **Time horizon:** all three use 30m signal timeframe with optional HTF context.
- **Direction policy:** all three are symmetric long / short with directional confirmation derived from price structure.
- **Stop / target shape:** all three use ATR-derived structural stop and fixed-R or measured-move target with unconditional time-stop.
- **Cost / sizing:** all three use §11.6 = 8 bps HIGH and §1.7.3 0.25% / 2×.

The shared signature is "**mechanical condition (extracted from price-structure features) + breakout-style entry trigger + ATR-derived structural stop + fixed-R or measured-move target + unconditional time-stop, on BTCUSDT 30m perpetual futures, under §11.6 HIGH cost**". Three rejections of strategies from this design family is informative evidence about the family itself, not just about each strategy individually.

**Phase 4z observes** that the discovery process should explicitly track design-family adjacency. Future candidates should be required to declare which design family they belong to and whether prior rejections from the same family constitute *evidence against the family* (in which case the candidate's burden of distinction is higher) or *evidence specific to the prior strategy* (in which case the family is still open). Three rejections in the same family creates a strong prior against the family.

The four large design-family categories most relevant to Prometheus v1's substrate (rules-based, supervised, BTCUSDT futures, 15m/30m signal, 1h/4h HTF context, completed bars only) appear to be:

- **(F-1) Mechanical-condition + breakout** (R3 baseline / R1a / R1b-narrow research evidence; V2 / G1 / C1 all rejected; six total entries; three rejections; family signature now well-explored on the negative side).
- **(F-2) Pullback / mean-reversion** (R2 / F1 both rejected; two entries; two rejections; smaller exploration but two distinct rejection modes — cost-fragility and catastrophic-floor — already on record).
- **(F-3) Funding / derivatives-flow** (D1-A rejected; one entry; one rejection — MECHANISM PASS / FRAMEWORK FAIL; family largely unexplored on the positive side).
- **(F-4) Microstructure / liquidity-timing** (Phase 4t Candidate F rejected at this boundary because of unavailable-data dependency; family unexplored on the project's substrate; Phase 4t cannot authorize acquisition).

A future fresh-hypothesis discovery memo should explicitly evaluate candidates against a **design-family-distance matrix** in addition to the Phase 4t 10-dimension matrix, where the rows are F-1 / F-2 / F-3 / F-4 and the entries describe how distant the candidate is from each rejected mode in the family. The C1 lesson is that "theoretically distinct from V2 and theoretically distinct from G1" was not enough; "theoretically distinct from V2, G1, *and the design family they share*" would have been a higher bar.

## Hypothesis-quality weakness analysis

The Phase 4m 18-requirement validity gate establishes 18 admissibility conditions. Phase 4z observes that a future research-process memo (if ever authorized) could *recommend* the following stronger hypothesis-quality requirements as **additions to a future hypothesis-admissibility framework** (not amendments to the Phase 4m gate, which is preserved verbatim):

1. **Explicit causal / mechanistic thesis.** Not "this condition correlates with future direction"; rather, "this condition causes / mediates / predicts future direction *because* [stated mechanism in language a market structure expert would recognize as plausible]". The mechanism statement must precede any threshold.
2. **Explicit "why this condition beats the unconditioned baseline" statement.** The hypothesis must claim, ex-ante, that the conditioned strategy will outperform the closest unconditioned same-geometry baseline by ≥ Δ_R with bootstrap CI lower > 0, and the magnitude Δ_R must be derived from theoretical expectations (e.g., from microstructural arguments, cross-asset evidence, or published academic results) rather than chosen post-hoc to be just barely passable.
3. **Explicit expected failure mode.** The hypothesis must predict, ex-ante, what the most likely failure mode would look like *if* the hypothesis is wrong. This ex-ante failure-mode prediction can then be cross-checked against the actual backtest outcome at consolidation. C1's failure mode (anti-validation against three baselines) was a surprise; a strong hypothesis would have predicted that "if we are wrong, we will see X" and X would have been a measurable quantity.
4. **Explicit non-hypothesis baseline.** Defined before any data is touched. C1 had three baselines (non-contraction, always-active-same-geometry, delayed-breakout). Future specs should require *at minimum* a same-geometry-unconditioned baseline plus one timing-shift baseline plus one alternative-condition baseline.
5. **Explicit opportunity-rate story.** What is the *first-principles expected frequency* of this candidate's primary event on BTCUSDT 30m? Derived from the candidate's theoretical content (e.g., "compression states arrive ~X% of the time because volatility regimes have characteristic durations of ~Y bars"), not from observed forensic numbers.
6. **Explicit edge-rate story.** What is the *first-principles expected positive expectancy per trade* of this candidate, after costs? Derived from the candidate's theoretical content, not chosen to be just barely passable.
7. **Explicit cost-survival thesis.** Why should this candidate survive §11.6 = 8 bps HIGH per side? Derived from the candidate's theoretical content (e.g., "the hold horizon is long enough that 8 bps round-trip is small relative to typical move size"), not from observed forensic numbers.
8. **Explicit sample-size viability.** What is the expected number of trades on BTCUSDT 30m over a 21-month OOS window? Must be ≥ a predeclared minimum derived from the candidate's theoretical content.
9. **Explicit anti-rescue mapping.** For each rejected strategy in the project record, the hypothesis must declare its closest distance and explain why it is not that strategy in disguise. After C1, this includes V2-prime / G1-prime / R1a / R1b-narrow / R2 / F1 / D1-A / V1-D1 / F1-D1 hybrid distances.
10. **Explicit closest-prior-failure comparison.** Identify the rejected strategy nearest in design family and explain how this candidate's failure mode would differ.

These ten requirements would complement the existing Phase 4m 18-requirement gate; they are not replacements. Phase 4z does NOT amend the Phase 4m gate.

## Baseline-design redesign

Phase 4w introduced a binding negative-baseline framework at the backtest-plan layer (M1 contraction-vs-non-contraction; M2.a vs always-active-same-geometry; M2.b vs delayed-breakout). Phase 4z observes that any future research-process memo could recommend **promoting baseline-design from the backtest-plan layer to the hypothesis-admissibility layer**, requiring future hypotheses to predeclare:

1. **Closest same-geometry unconditioned baseline.** The candidate's setup geometry, stop / target / sizing, cost cells, but with no conditioning predicate. This is the M2.a-style baseline.
2. **Condition-removed baseline.** The candidate's full setup with the primary conditioning predicate removed. Where the primary predicate is the candidate's defining theoretical content, this is the M1-style baseline.
3. **Timing-shift baseline** (where applicable). The candidate's full setup but with the entry timing shifted by an arbitrary lag. This is the M2.b-style baseline; it tests whether the precise timing of the candidate's trigger matters.
4. **Random-condition baseline** (where applicable). The candidate's full setup but with the conditioning predicate replaced by a random Bernoulli with the same activation frequency. This tests whether the candidate's condition carries any signal beyond pure activation rate.
5. **Always-active baseline** (where applicable). For state-machine-style candidates, the same setup with the state machine replaced by always-on. This tests whether the state machine adds value over the unconditioned setup.
6. **Non-event baseline** (where applicable). For event-driven candidates, the same setup but with the event-trigger replaced by a non-event sample. This tests whether the event itself carries signal.

Pass/fail thresholds for baseline differentials should be:

- **Bootstrap-CI-based**: candidate's mean_R minus baseline's mean_R must have bootstrap 95% CI lower > 0 (with B = 10 000 minimum, RNG seed pinned).
- **Magnitude-based**: differential ≥ a predeclared minimum Δ_R derived from the candidate's first-principles theoretical content.
- **Both required** for a baseline-superiority pass; raw mean_R thresholds alone are insufficient.

Phase 4w already implements this at C1; Phase 4z's recommendation is to make it the **default baseline-design pattern** for any future strategy spec, not just a Phase 4w-specific innovation.

## Opportunity-rate versus edge-rate redesign

The Phase 4u opportunity-rate viability principle and the Phase 4v / Phase 4w CFP-9 enrichment are preserved verbatim. Phase 4z does NOT amend them.

Phase 4z observes that **opportunity-rate viability** and **edge-rate viability** should be tracked as **two separate gates** at the hypothesis-admissibility layer:

- **Opportunity-rate viability gate:** "Will this candidate fire enough trades to be statistically informative?" Operationalized as CFP-9 floors (candidate-event rate per N bars; trade_count per OOS window for the train-best variant; variant pass-fraction). Already binding at the backtest-plan layer for any future grid-search strategy. **No redesign needed at this gate.**
- **Edge-rate viability gate (NEW PROPOSED):** "Will this candidate, *when it fires*, produce positive expectancy versus an unconditioned baseline?" Operationalized as a predeclared expected baseline differential with bootstrap-CI-based pass/fail. Currently **implicit** in the Phase 4w M1 / M2 framework but not separated as its own gate.

The C1 result demonstrated that these two gates measure different things. C1 satisfied the opportunity-rate gate (rate 3.33; 100% pass; 149 trades) and failed the edge-rate gate (M1 -0.244R CI strictly negative). A future research-process memo could recommend **explicitly separating the two gates** in any future strategy-spec, hypothesis-admissibility, and backtest-plan template.

This separation also clarifies the earlier failure modes:

| Failure mode | Opportunity-rate gate | Edge-rate gate |
| --- | --- | --- |
| R2 cost-fragility | PASSED | PASSED gross; FAILED net (cost-driven) |
| F1 catastrophic-floor | PASSED at full population | FAILED; subset-isolated PASS only |
| D1-A mechanism / framework | PASSED | PARTIAL PASS at h=32 BTC; FAILED at framework |
| V2 design-stage | FAILED (zero trades) | Not measurable |
| G1 regime-gate sparsity | FAILED (zero qualifying trades) | Not measurable |
| C1 fires-and-loses | PASSED | FAILED (multi-baseline anti-validation) |

This table makes the design intent of the two gates explicit: **opportunity-rate viability is a sample-existence gate; edge-rate viability is a strategy-quality gate**. They must be separable so that a future hypothesis can be described as "this candidate's primary risk is opportunity-rate" or "this candidate's primary risk is edge-rate" *before* the backtest is run.

## Mechanism-check redesign

Phase 4w's M1 / M2 / M3 / M4 / M5 mechanism-check framework is the project's most mature mechanism-check shape. Phase 4z proposes (as recommendations for any future research-process memo) the following additions:

- **M0 — Theoretical admissibility gate.** Predeclared at the hypothesis-admissibility layer (upstream of strategy-spec). M0 requires the hypothesis to argue ex-ante why its primary condition should outperform an unconditioned baseline, deriving a predicted Δ_R from theoretical content, and committing to that prediction as the *expected outcome* of the future M1 / M2 baselines. M0 is not a backtest gate; it is an admissibility check that operates before any strategy spec is authored.
- **M1 — Baseline superiority** (existing Phase 4w form preserved). Candidate's mean_R vs. condition-removed baseline; bootstrap CI lower > 0; magnitude ≥ predeclared Δ_R.
- **M2 — Condition specificity.** Candidate's mean_R vs. always-active-same-geometry baseline AND vs. timing-shift baseline AND vs. random-condition baseline (where applicable). Tests whether the *specific* conditioning predicate adds value over alternative baselines that share the same geometry but differ in conditioning.
- **M3 — Timing / transition value-add** (where applicable). For candidates whose theoretical content depends on transition timing (e.g., contraction-to-expansion), explicit comparison vs. delayed / shifted baselines.
- **M4 — Cost survival.** Candidate's BTC OOS HIGH mean_R > 0 AND trade_count ≥ 30 AND no CFP-1 / CFP-2 / CFP-3 trigger AND opportunity-rate floors satisfied AND CFP-9 not triggered.
- **M5 — Cross-symbol non-contradiction.** ETH OOS HIGH non-negative differential AND directional consistency; ETH cannot rescue BTC.
- **M6 — Robustness / sensitivity.** Sensitivity perturbation of the train-best variant's threshold values; worst-case degradation must be below a predeclared bound.
- **M7 — No-rescue compliance.** Audit confirms no use of prior failure forensic numbers as design inputs; no use of forbidden inputs; no methodology amendment based on observed results.

These are recommendations, not adopted governance. Any future research-process memo would itself need separate operator authorization before any of these became binding requirements for a future hypothesis spec.

## Negative-test redesign

Phase 4w's negative-test framework (non-contraction baseline; always-active-same-geometry baseline; delayed-breakout baseline; active opportunity-rate diagnostic) is the project's most mature negative-test design. Phase 4z observes that any future research-process memo could recommend:

1. **Negative-test predeclaration is mandatory at the hypothesis-admissibility layer**, not optional or introduced at the backtest-plan layer.
2. **At minimum three negative tests** must be predeclared per hypothesis: (a) condition-removed (M1 form); (b) always-active-same-geometry (M2.a form); (c) one of timing-shift / random-condition / non-event depending on candidate (M2.b form).
3. **Each negative test must have a predeclared expected differential** from theoretical content.
4. **Each negative test must have a bootstrap-CI-based pass criterion** (CI lower > 0 for positive differentials).
5. **Empirically negative differentials are terminal evidence** against the hypothesis on the dataset / window / cost cell tested; they are NOT tuning inputs for future variants.
6. **Methodologically inert negative-test outcomes** (e.g., baseline computation failed because of zero-trade conditions in V2 / G1) must not be treated as PASS-by-default; the appropriate verdict is INCOMPLETE or HARD REJECT depending on the cause.

## Search-space-control redesign

Phase 4w's PBO / DSR / CSCV framework with N = 32 variants, B = 10 000 bootstrap, RNG seed 202604300, S = 16 CSCV with C(16, 8) = 12 870 combinations is the project's most mature search-space-control design. Phase 4z observes that any future research-process memo could recommend:

1. **Variant grid cardinality should be the smallest needed to test the hypothesis's primary axes**, not maximized. C1's 32-variant grid (= 2^5 over five binary axes) was a substantial reduction from V2's 512-variant grid (= 2^9 over nine binary axes). Smaller grids reduce search-space-control burden, simplify CSCV computation, and reduce the risk of false-positive overfitting. Future specs should justify grid cardinality from theoretical content.
2. **CFP-6 should preserve both PBO ≤ 0.50 AND DSR > 0** as independent triggers. C1 demonstrated that low PBO + strongly negative DSR is informative ("not overfit AND not edge"); a future spec should treat these as independent signals.
3. **CSCV should remain exact, not approximated.** S = 16 with C(16, 8) = 12 870 combinations is tractable; any future spec that proposes silent approximation is a stop-condition trigger.
4. **The pinned RNG seed convention (`202604300`)** should be preserved across phases for reproducibility unless a separately authorized memo changes it.

## Stop-condition redesign

Phase 4w's 24-item stop-condition list (manifest mismatch; missing data; forbidden inputs; lookahead; transition-dependency violations; data-integrity issues; methodology violations; quality-gate failures; CSCV silent approximation; grid expansion / contraction; non-pinned RNG seed) is comprehensive. Phase 4z observes that any future research-process memo could recommend:

1. **Stop-conditions must be predeclared at the backtest-plan layer**, not introduced during execution. Phase 4w correctly does this.
2. **Stop-conditions must be runtime-enforced**, not only tested at end-of-run. Phase 4l / 4r / 4x scripts implement this via audit counters in `forbidden_work_confirmation.csv` plus runtime guards.
3. **Stop-conditions must include an "unexpected outcome" category** that triggers Verdict D (INCOMPLETE) rather than Verdict C (HARD REJECT) when the cause of an anomalous result is methodological rather than substantive. Phase 4w correctly distinguishes runtime-stop CFPs (CFP-10 / CFP-11 / CFP-12) from post-run-verdict CFPs (CFP-1 through CFP-9).
4. **Adding a new stop-condition mid-execution is a methodology amendment** and is forbidden post-hoc.

## No-rescue enforcement redesign

The Phase 4m §"Forbidden rescue observations" and Phase 4y §"Forbidden cross-strategy rescue interpretations" are comprehensive. Phase 4z observes that any future research-process memo could recommend the following stronger no-rescue language as **process discipline** (not as new governance):

1. **"Forensic numbers cannot become future thresholds" rule.** A future hypothesis must NOT use V2's 3–5 × ATR observed stop distance, V2's zero-trade outcome, G1's 2.03% active fraction, G1's 124 always-active baseline trades, G1's −0.34 mean_R always-active outcome, C1's 149 BTC OOS HIGH trade count, C1's −0.36 mean_R, C1's −0.24R baseline differential, or any other observed forensic number from a rejected strategy as a tuning input or threshold derivation.
2. **"Least-bad variant cannot seed a new spec" rule.** A future hypothesis must NOT identify the least-loss variant from a rejected strategy's threshold grid and propose modifications around that variant. Each rejected strategy's full grid is research evidence, not a spec template.
3. **"Adding a filter after failure is rescue unless justified from external first-principles before data touch" rule.** A future hypothesis that proposes "[rejected strategy] but with [new filter]" must derive the new filter from external theory or evidence (not from observation of the rejected strategy's failure shape) and predeclare the filter before any data is touched.
4. **"Same data + adjacent hypothesis after failure requires elevated approval" rule.** A future hypothesis that proposes a candidate from the same design family as a rejected strategy (e.g., another mechanical-condition + breakout candidate after V2 / G1 / C1 rejection) must clear an elevated discovery-memo approval bar with explicit design-family-distance justification.
5. **"Future research must name the prior failure trap it is closest to and explain why it is not that trap" rule.** Phase 4n / 4t already do this; future memos should continue and strengthen the rescue-trap-naming discipline.

These five rules are recommendations for any future research-process memo, not amendments to existing governance.

## Future hypothesis admissibility framework

Phase 4z proposes a stricter future hypothesis-admissibility checklist with at least 20 requirements. The list is **a recommendation** for any future research-process memo to consider; Phase 4z does NOT adopt it as binding governance. The list complements (does NOT replace) the Phase 4m 18-requirement validity gate.

```text
A1.  Must be named as a new hypothesis (not a rescue label).
     [Phase 4m requirement #1; preserved]
A2.  Must have a distinct name and a distinct conceptual foundation.
     [Phase 4m requirement #1; preserved]
A3.  Must be specified before any data is touched.
     [Phase 4m requirement #2; preserved]
A4.  Must explain why it is new in theory, not just a parameter tweak.
     [Phase 4m requirement #3; preserved]
A5.  Must declare its design family (F-1 / F-2 / F-3 / F-4 or new) and
     argue distance from each prior rejected strategy in that family.
     [NEW; recommended addition]
A6.  Must define entry, stop, target, sizing, cost, timeframe, and exit
     together as a single integrated co-design.
     [Phase 4m requirement #4; preserved]
A7.  Must define regime-gate / entry-rule / sample-size-viability
     together (G1 lesson).
     [Phase 4s observation; recommended addition]
A8.  Must predeclare data requirements (no acquisition implied).
     [Phase 4m requirement #5; preserved]
A9.  Must predeclare an explicit causal / mechanistic thesis with a named
     mechanism (NEW; recommended addition).
A10. Must predeclare expected baseline differential Δ_R derived from
     theoretical content, not chosen to be just barely passable.
     [NEW; recommended addition]
A11. Must predeclare expected opportunity-rate from theoretical content,
     not from observed forensic numbers (Phase 4u principle preserved
     and strengthened).
A12. Must predeclare expected edge-rate from theoretical content
     (NEW; recommended addition; opportunity-rate / edge-rate separation).
A13. Must predeclare expected failure mode if hypothesis is wrong
     (NEW; recommended addition).
A14. Must predeclare cost-survival thesis from theoretical content;
     §11.6 = 8 bps HIGH per side preserved verbatim
     (Phase 4m requirement #11; preserved and strengthened).
A15. Must predeclare sample-size viability from theoretical content
     (NEW; recommended addition).
A16. Must predeclare mechanism checks (M0 / M1 / M2 / M3 / M4 / M5 / M6 / M7)
     (Phase 4m requirement #6; recommended extension to M0–M7).
A17. Must predeclare pass / fail gates including catastrophic-floor
     predicates (Phase 4m requirement #7; preserved).
A18. Must predeclare forbidden comparisons and forbidden rescue
     interpretations (Phase 4m requirement #8; preserved).
A19. Must NOT choose thresholds from prior failed outcomes
     (Phase 4m requirement #9; preserved and strengthened).
A20. Must NOT use Phase 4l / 4r / 4x forensic numbers as direct
     optimization targets (Phase 4m requirement #10 + Phase 4s + Phase 4y;
     preserved and strengthened with C1 forensic numbers added).
A21. Must NOT use Phase 4r G1 active-fraction, 124-trade, or −0.34
     mean_R numbers as tuning targets (Phase 4s observation; preserved).
A22. Must NOT use Phase 4x C1 forensic numbers as tuning targets
     (Phase 4y observation; preserved).
A23. Must preserve §11.6 cost sensitivity (Phase 4m requirement #11;
     preserved).
A24. Must preserve project locks and governance (Phase 4m requirement
     #12; preserved).
A25. Must commit to predeclared chronological train / validation / OOS
     holdout windows before any backtest (Phase 4m requirement #13;
     preserved).
A26. Must commit to deflated Sharpe / PBO / CSCV correction if grid
     search is involved (Phase 4m requirement #14; preserved).
A27. Must distinguish mechanism evidence from framework promotion
     (Phase 4m requirement #15; preserved).
A28. Must preserve BTCUSDT-primary / ETHUSDT-comparison protocol
     (Phase 4m requirement #16; preserved).
A29. Must NOT propose live-readiness or paper / shadow / Phase 4
     canonical as part of its first phase (Phase 4m requirement #17;
     preserved).
A30. Must satisfy separate operator authorization (Phase 4m
     requirement #18; preserved).
A31. Must declare the closest rejected strategy in design family and
     explain how its failure mode would differ (NEW; recommended
     addition).
A32. Must declare a remain-paused-comparison: under what evidence
     would remain-paused dominate this candidate? (NEW; recommended
     addition).
```

The 32 items above include every Phase 4m requirement (preserved verbatim, with strengthening notes only) plus 9 proposed new items (A5, A7 reads, A9, A10, A12, A13, A15, A31, A32). A future research-process memo could choose to adopt the 9 new items as additions to the Phase 4m gate or could choose to leave the gate at 18 items unchanged. Phase 4z recommends *consideration* of the 9 new items but does NOT itself amend the gate.

## Future discovery memo template

For any future fresh-hypothesis discovery memo (analogous to Phase 4n / Phase 4t), Phase 4z proposes the following section template (recommendation only):

```text
1.  Authority and boundary
2.  Starting state
3.  Why this memo exists
4.  Relationship to prior consolidation memo
5.  Full rejection topology recap (six-failure topology, current as of
    the memo date)
6.  Phase 4m + Phase 4z proposed admissibility framework recap
7.  Discovery method (10-dimension matrix + design-family-distance
    matrix)
8.  Candidate pool considered (named candidates only; no implementation
    names)
9.  Per-candidate analysis (one section per candidate; consistent shape)
   - 9.1 Origin
   - 9.2 Core thesis
   - 9.3 Design-family declaration (F-1 / F-2 / F-3 / F-4 / new)
   - 9.4 Distance from prior rejections in same family
   - 9.5 Distance from rejections in other families
   - 9.6 Distance from forbidden rescue traps
   - 9.7 Theoretical mechanism statement
   - 9.8 Predicted baseline differential Δ_R from theory
   - 9.9 Predicted opportunity-rate from theory
   - 9.10 Predicted edge-rate from theory
   - 9.11 Predicted failure mode if hypothesis is wrong
   - 9.12 Cost-survival thesis
   - 9.13 Sample-size viability
   - 9.14 Data feasibility (existing-data only)
   - 9.15 Negative-baseline designability
   - 9.16 Mechanism-check designability
   - 9.17 Implementation complexity later
   - 9.18 Research value if rejected
10. Candidate scoring matrix (Phase 4t 10-dimension form preserved;
    plus design-family-distance matrix)
11. Rescue-risk analysis (per candidate)
12. Opportunity-rate viability analysis (per candidate)
13. Edge-rate viability analysis (per candidate; NEW)
14. Data-readiness implications
15. Cost-sensitivity implications
16. Mechanism-check designability
17. Governance and forbidden-input implications
18. Final discovery recommendation (one primary; at most one
    conditional secondary; or remain-paused if no candidate clearly
    dominates)
19. What this does not authorize
20. Forbidden-work confirmation
21. Remaining boundary
22. Operator decision menu
23. Next authorization status
```

This template is a **recommendation** for any future fresh-hypothesis discovery memo. It is not adopted governance and Phase 4z does NOT itself create such a memo.

## Future strategy-spec template changes

For any future strategy-spec memo (analogous to Phase 4g / 4p / 4v), Phase 4z proposes the following template additions (recommendation only):

1. **Closest baseline definitions required before thresholds.** The strategy spec must define its same-geometry-unconditioned baseline, condition-removed baseline, and timing-shift baseline (where applicable) *before* any threshold value is committed.
2. **Exact "why condition beats baseline" clause.** The strategy spec must state, in a dedicated section, why the chosen conditioning predicate is expected to outperform each baseline. The clause must be derived from theoretical content and must commit to a predicted Δ_R magnitude.
3. **Edge-rate floor separate from trade-count floor.** The strategy spec must declare both an opportunity-rate floor (CFP-9 form) and an edge-rate floor (predicted Δ_R from theory). Both must be predeclared.
4. **Rescue-adjacency table.** The strategy spec must include a table showing this candidate's distance from each of the six rejected strategies (R2 / F1 / D1-A / V2 / G1 / C1) plus any future rejected strategies, with explicit avoidance pattern per row.
5. **Forbidden threshold provenance section.** The strategy spec must declare that no threshold value was derived from prior failure forensic numbers. The declaration must list each threshold and identify its provenance (theoretical content / external evidence / safe inheritance from baseline-of-record).
6. **Expected failure-mode declaration.** The strategy spec must state, in advance, what the most likely failure mode would look like if the hypothesis is wrong, and what observable quantity at the backtest-execution layer would confirm or deny it.

These additions complement (do NOT replace) the existing Phase 4g / 4p / 4v strategy-spec sections.

## Future backtest-plan template changes

For any future backtest-plan memo (analogous to Phase 4k / 4q / 4w), Phase 4z proposes the following template additions (recommendation only):

1. **Baseline tables are binding, not optional.** Every backtest plan must include explicit table specifications for at least three baseline differentials (M1 form; M2.a form; M2.b form where applicable).
2. **Baseline differential CI required.** The backtest plan must specify bootstrap parameters (B = 10 000 minimum; pinned RNG seed) and CI thresholds for each baseline differential.
3. **Strategy can fail even if mean_R positive if baseline outperforms.** The backtest plan must explicitly state that a strategy with positive raw mean_R but a strictly-negative baseline differential is HARD REJECT, not PASS.
4. **Edge-rate gates separate from CFPs.** The backtest plan must include a dedicated "edge-rate viability" section separate from the catastrophic-floor predicate section; the edge-rate gate's pass / fail criteria must be predeclared.
5. **All post-failure tuning prohibited.** The backtest plan must declare that observed results are research evidence only and must NOT be used as inputs to future variants, future thresholds, future filters, or any other tuning channel.
6. **Methodology amendment forbidden mid-execution.** The backtest plan must commit to its methodology before execution; any change discovered during execution is a stop-condition trigger.

These additions complement (do NOT replace) the existing Phase 4k / 4q / 4w backtest-plan sections.

## Future execution-report template changes

For any future backtest-execution report (analogous to Phase 4l / 4r / 4x), Phase 4z proposes the following template additions (recommendation only):

1. **Baseline superiority summary before headline mean_R.** The execution report's leading section should report baseline differentials (M1 / M2.a / M2.b) with bootstrap CI, BEFORE reporting the candidate's raw mean_R. This makes it visually obvious whether the candidate is anti-validated against baselines.
2. **Failure-mode classification section.** The execution report must explicitly classify the failure mode (or pass mode) using the project's six-failure-mode topology (R2 cost-fragility; F1 catastrophic-floor; D1-A mechanism / framework mismatch; V2 design-stage; G1 regime-gate sparsity; C1 fires-and-loses) plus any future modes. New failure modes should be named and added to the topology.
3. **Forensic-number non-reuse warning.** The execution report must include an explicit warning section stating that observed forensic numbers (variant identifiers, threshold values, baseline differentials, opportunity rates, mean_R values) are NOT to be used as tuning inputs or threshold derivations for any future hypothesis.
4. **Rescue-prohibition summary.** The execution report must enumerate the rescue interpretations that are forbidden as a result of this rejection, by name and by category.
5. **Process-lessons section.** The execution report must record any process-level lessons learned during execution that are relevant to future research-process redesign. This section should be brief and factual; deep process redesign belongs in dedicated process-redesign memos (analogous to this Phase 4z).

These additions complement (do NOT replace) the existing Phase 4l / 4r / 4x execution-report sections.

## Process gates before any new strategy candidate

Phase 4z recommends the following process gates before any future fresh-hypothesis discovery cycle is authorized:

1. **No new strategy candidate until a process-redesign memo (this Phase 4z, or a successor) is reviewed by the operator and the operator chooses to either adopt or decline its recommendations.** The current Phase 4z merge into main (if ever authorized) is itself an operator-driven decision; until then, no new strategy candidate work is in progress.
2. **Any future fresh-hypothesis discovery memo requires separate operator authorization** (analogous to Phase 4n / 4t precedent). Phase 4z does NOT authorize one.
3. **A future fresh-hypothesis discovery memo must apply the proposed admissibility framework** (or an explicit subset of it) and must justify any candidate selection against the design-family-distance matrix.
4. **Remain-paused must remain a serious candidate in any future discovery memo**, with explicit articulation of what evidence would dominate it.
5. **Repeated rejection in the same design family** (e.g., a fourth rejection in F-1 mechanical-condition + breakout) should automatically demote that family in the discovery matrix until a substantively new sub-family argument is produced.

## Process gates before any new backtest

Phase 4z recommends the following process gates before any future backtest is run:

1. **Docs-only discovery memo merged.**
2. **Docs-only hypothesis-spec memo merged.**
3. **Docs-only strategy-spec memo merged.**
4. **Docs-only backtest-plan memo merged.**
5. **All explicit negative baselines predeclared at the strategy-spec layer.**
6. **No acquired data unless a separately authorized data-requirements memo has been merged.**
7. **No execution until all four merge gates above have passed.**
8. **Backtest execution remains a separate operator-authorized phase.**

These gates mirror the existing Phase 4u → 4v → 4w → 4x and Phase 4o → 4p → 4q → 4r and Phase 4f → 4g → 4h → 4i → 4j → 4k → 4l sequences. Phase 4z observes that the existing sequence pattern is correct and should be preserved; the redesigns above propose stricter content within each phase, not a different sequence.

## Process gates before any implementation-readiness work

Phase 4z recommends the following process gates before any implementation-readiness work proceeds:

1. **Strategy-agnostic implementation-readiness work** (e.g., Phase 4d Option B structured logging slice; Phase 4e reconciliation-engine implementation; Phase 4d Option C richer fake-exchange test harness) is permitted as separate docs-only scoping followed by separate operator-authorized implementation. **Phase 4z does NOT authorize any of these.**
2. **Strategy-specific implementation** (any code that depends on a particular strategy's signal logic, parameter values, or feature computations) is **forbidden** without validated strategy evidence. No strategy in the project record currently has validated evidence; all six retained strategy entries other than R3 are research-evidence-only or rejected.
3. **No paper / shadow / live until strategy evidence exists.** Phase 4 canonical (paper / shadow / live-readiness gates) is unauthorized; production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, and exchange-write are all unauthorized.

## What remains valid

After Phase 4z, the following remain valid (preserved verbatim from prior governance):

- H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained-non-leading; R2 / F1 / D1-A / V2 / G1 / C1 rejection states.
- §11.6 = 8 bps HIGH per side; §1.7.3 0.25% / 2× / one-position; mark-price stops.
- Phase 3r §8 mark-price gap governance; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; Phase 4j §11 metrics OI-subset partial-eligibility rule.
- Phase 4k V2 backtest-plan methodology; Phase 4q G1 backtest-plan methodology; Phase 4w C1 backtest-plan methodology.
- Phase 4m 18-requirement fresh-hypothesis validity gate.
- Phase 4t 10-dimension scoring matrix (D1–D10).
- Phase 4u opportunity-rate viability principle.
- Phase 4w binding negative-baseline framework (M1 / M2.a / M2.b / M3 / M4 / M5).
- Phase 4l / 4r / 4x execution patterns (standalone-script boundary; gitignored research output; no implementation in `src/prometheus/`).
- Phase 4a runtime foundation (strategy-agnostic).
- Phase 4e reconciliation-model design memo (preserved; not implemented).
- Consolidation-memo discipline (Phase 3e / 3k / 4m / 4s / 4y).

Phase 4z's proposed redesigns are **additions** to consider in future memos, not replacements for what remains valid.

## What remains forbidden

After Phase 4z, the following remain forbidden:

- Any C1 / V2 / G1 / R2 / F1 / D1-A rescue (preserved from Phase 4y).
- C1-prime / C1-narrow / C1-extension / C1 hybrid (preserved from Phase 4y).
- G1-prime / G1-narrow / G1-extension / G1 hybrid (preserved from Phase 4s / 4y).
- V2-prime / V2-narrow / V2-relaxed / V2 hybrid (preserved from Phase 4m / 4y).
- F1 / D1-A / R2 rescue (preserved from Phase 3e / 3k / 4m / 4s / 4y).
- 5m strategy from Q1–Q7 diagnostic findings (preserved from Phase 3t).
- Immediate ML-first black-box forecasting (preserved; project remains rules-based per §1.7.3).
- Immediate market-making / HFT (preserved from Phase 4f).
- Mark-price 30m / 4h / 5m / 15m acquisition; aggTrades; spot; cross-venue; order-book (preserved).
- Optional metrics ratio columns (preserved from Phase 4j §11.3).
- Use of Phase 4l / 4r / 4x forensic numbers as tuning inputs (preserved).
- Phase 4v / 4w / 4j §11 / 4k methodology amendment based on Phase 4l / 4r / 4x results (preserved).
- Paper / shadow / live operation (preserved).
- Phase 4 canonical (preserved).
- Production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write (preserved).
- Phase 5 / Phase 4aa / any successor phase (NOT authorized by Phase 4z).
- Creation of a new strategy candidate or named successor (forbidden by Phase 4z scope).
- Creation of a fresh-hypothesis discovery memo (forbidden by Phase 4z scope).
- Creation of a strategy-spec or backtest-plan memo (forbidden by Phase 4z scope).
- Modification of any existing script, including `scripts/phase4x_c1_backtest.py` (forbidden by Phase 4z scope).
- Modification of `src/prometheus/`, tests, or any source code (forbidden by Phase 4z scope).
- Acquisition / download / patch / regeneration / replacement of data (forbidden by Phase 4z scope).
- Creation of v003 (forbidden by Phase 4z scope).
- Modification of governance files including `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, or any specialist governance document (forbidden by Phase 4z scope).
- Merge of Phase 4z to main without explicit operator instruction (forbidden by Phase 4z scope).

## Recommended next operator choice

- **Option A — primary recommendation: remain paused.** The strongest-evidence position remains unchanged. With six terminal negative strategy outcomes, a research-process redesign memo (this Phase 4z) preserved on a feature branch (or merged later if operator chooses) does not change the binding constraint that no validated strategy candidate exists. Remain-paused dominates any research-forward action at this boundary.
- **Option B — conditional secondary: docs-only documentation-refresh / governance-template update memo (only if separately authorized).** This option would update `docs/00-meta/current-project-state.md`, `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, or `docs/00-meta/ai-coding-handoff.md` to reflect the post-Phase-4z boundary, possibly incorporating a subset of the Phase 4z proposed redesigns as adopted governance. Phase 4z does NOT itself amend these files. Phase 4z does NOT recommend this option as primary because the binding constraint at this boundary remains strategy evidence, not governance text.

NOT recommended:

- **Immediate fresh-hypothesis discovery memo** — REJECTED. The Phase 4z process-redesign analysis indicates that another fresh-hypothesis cycle would likely repeat the V2 / G1 / C1 pattern unless the discovery method is materially redesigned. Phase 4z is the redesign analysis; adoption of its proposed redesigns is a separate operator decision.
- **Immediate new strategy candidate, strategy spec, backtest plan, backtest execution, implementation, data acquisition, paper / shadow / live, Phase 4 canonical, production keys, MCP, Graphify, `.mcp.json`, credentials, or exchange-write** — REJECTED / FORBIDDEN.
- **Strategy-agnostic implementation-readiness scoping memo** — NOT recommended now. Acceptable in principle but not preferred because the binding constraint is strategy evidence, not infrastructure.

## What this does not authorize

Phase 4z does NOT authorize:

- **Phase 5 / Phase 4aa / any successor phase.**
- creation of any new strategy candidate;
- creation of any new strategy candidate name (e.g., V3, H2, G2, C2, R4);
- creation of **C1-prime / C1-extension / C1-narrow / C1 hybrid**;
- creation of **G1-prime / V2-prime / R2-prime / F1-prime / D1-A-prime / D1-B / V1-D1 hybrid / F1-D1 hybrid / any cross-strategy rescue**;
- any **fresh-hypothesis discovery memo** (would require separate operator authorization analogous to Phase 4n / 4t);
- any **strategy-spec memo** or **backtest-plan memo** (would require separate operator authorization analogous to Phase 4o / 4p / 4u / 4v or Phase 4q / 4w);
- any **backtest execution** (would require separate operator authorization analogous to Phase 4r / 4x);
- any **C1 rerun** or amendment of Phase 4v / 4w;
- any amendment of **Phase 4m 18-requirement validity gate**, **Phase 4t 10-dimension scoring matrix**, **Phase 4u opportunity-rate principle**, **Phase 4w negative-baseline / PBO / DSR / CSCV methodology**, **Phase 4j §11 metrics OI-subset partial-eligibility rule**, **Phase 4k V2 backtest-plan methodology**, **Phase 3v §8 stop-trigger-domain governance**, **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance**, **Phase 3r §8 mark-price gap governance**, **§11.6 = 8 bps HIGH per side**, or **§1.7.3 project-level locks**;
- any modification of `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist governance document;
- **implementation** in `src/prometheus/`;
- **data acquisition** (mark-price, aggTrades, spot, cross-venue, or any other source);
- **paper / shadow / live / exchange-write**;
- **production keys / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials**;
- any revision of **retained verdicts** (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1);
- any change to **project locks** (§11.6 / §1.7.3 / mark-price stops / v002 verdict provenance);
- modification of **`scripts/phase4x_c1_backtest.py`** or any other existing script;
- adoption of any of the Phase 4z proposed redesigns as binding governance — they remain recommendations only;
- merge of Phase 4z to main without explicit operator instruction.

## Forbidden-work confirmation

Phase 4z did NOT do any of the following:

- run a backtest (any phase);
- write any code;
- create any script;
- modify any source under `src/prometheus/`;
- modify any test;
- modify any existing script (no edits to `scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`, `scripts/phase4i_v2_acquisition.py`, `scripts/phase4l_v2_backtest.py`, `scripts/phase4r_g1_backtest.py`, `scripts/phase4x_c1_backtest.py`);
- run `scripts/phase4x_c1_backtest.py`;
- run any acquisition / diagnostics / backtest script;
- acquire data;
- download data;
- patch / forward-fill / interpolate / regenerate / replace data;
- modify any manifest;
- create any new manifest;
- create v003;
- modify Phase 4p / Phase 4q / Phase 4j §11 / Phase 4k / Phase 4v / Phase 4w / Phase 3v §8 / Phase 3w §6 / §7 / §8 / Phase 3r §8 governance;
- amend the Phase 4m 18-requirement validity gate;
- amend the Phase 4t 10-dimension scoring matrix;
- amend the Phase 4u opportunity-rate principle;
- amend the Phase 4w negative-baseline / PBO / DSR / CSCV methodology;
- modify `docs/00-meta/current-project-state.md`, `docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/implementation-ambiguity-log.md`, or any specialist governance file;
- revise any retained verdict;
- change any project lock;
- create a new strategy candidate or named successor;
- create C1-prime / C1-narrow / C1-extension / C1 hybrid;
- create G1-prime / G1-narrow / G1-extension / G1 hybrid;
- create V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- create F1 / D1-A / R2 rescue;
- propose a 5m strategy / hybrid / variant;
- start Phase 5 / Phase 4aa / 4 canonical / paper-shadow / live-readiness / deployment / production-key creation / exchange-write capability / authenticated REST / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials work;
- consult any private endpoint / user stream / WebSocket / authenticated REST in code;
- store, request, or display any secret;
- perform web research that collected market data, downloaded archives, called Binance APIs, called `data.binance.vision`, scraped prices, created datasets, or imported online thresholds as adopted project values;
- use Phase 4l / 4r / 4x C1 forensic numbers as tuning input or threshold derivation for any proposed redesign;
- merge Phase 4z to main.

## Remaining boundary

```text
R3                  : V1 breakout baseline-of-record (preserved)
H0                  : framework anchor (preserved)
R1a / R1b-narrow    : retained research evidence; non-leading (preserved)
R2                  : FAILED — §11.6 cost-sensitivity blocks (preserved)
F1                  : HARD REJECT (preserved)
D1-A                : MECHANISM PASS / FRAMEWORK FAIL — other (preserved)
V2                  : HARD REJECT (Phase 4l terminal for first-spec; preserved)
G1                  : HARD REJECT (Phase 4r — Verdict C; CFP-1 critical
                       binding; CFP-9 independent; terminal for G1 first-spec;
                       preserved)
C1                  : HARD REJECT (Phase 4x — Verdict C; CFP-2 binding;
                       CFP-3 / CFP-6 co-binding; CFP-1 / CFP-9 NOT
                       triggered; terminal for C1 first-spec; preserved
                       by Phase 4y consolidation)
5m diagnostic thread : OPERATIONALLY CLOSED (Phase 3t)
§11.6               : 8 bps HIGH per side (preserved verbatim)
§1.7.3              : 0.25% risk / 2× leverage / 1 position / mark-price
                       stops (preserved)
v002 verdict provenance     : preserved
Phase 3q manifests          : research_eligible: false for mark-price 5m
                              (preserved)
Phase 3r §8                 : mark-price gap governance (preserved)
Phase 3v §8                 : stop-trigger-domain governance (preserved)
Phase 3w §6 / §7 / §8       : break-even / EMA slope / stagnation governance
                              (preserved)
Phase 4a runtime            : public API and behavior (preserved;
                              strategy-agnostic)
Phase 4e                    : reconciliation-model design memo (preserved)
Phase 4f / 4g / 4h / 4i / 4j§11 / 4k / 4l / 4m / 4n / 4o / 4p / 4q / 4r / 4s / 4t / 4u / 4v / 4w / 4x / 4y
                            : all preserved verbatim
Phase 4z                    : Post-rejection research-process redesign memo
                              (this phase; new; docs-only; not merged;
                              proposes recommendations only)
Recommended state           : remain paused (primary);
                              docs-only documentation-refresh / governance-
                              template update memo (conditional secondary;
                              not authorized by Phase 4z)
```

## Operator decision menu

- **Option A — primary recommendation: remain paused.** The Phase 4z process-redesign analysis is now on the project record. Whether to merge Phase 4z to main, adopt a subset of its proposed redesigns as governance, or simply preserve it on the branch as research evidence is an operator decision that does not require immediate action.
- **Option B — conditional secondary: docs-only documentation-refresh / governance-template update memo (only if separately authorized; not started by this Phase 4z).** This option would update governance files (`docs/12-roadmap/phase-gates.md`, `docs/12-roadmap/technical-debt-register.md`, `docs/00-meta/ai-coding-handoff.md`, `docs/00-meta/current-project-state.md`) to incorporate a subset of Phase 4z's proposed redesigns as adopted governance. Phase 4z does NOT itself amend these files; an operator-authorized governance-update phase would be required.
- **Option C — NOT recommended: docs-only fresh-hypothesis discovery memo (only if separately authorized).** Acceptable in principle but Phase 4z's analysis indicates that another fresh-hypothesis cycle without first adopting (or explicitly declining) the proposed redesigns would likely repeat the V2 / G1 / C1 pattern. Phase 4z does NOT recommend this option as immediate next.
- **Option D — NOT recommended: docs-only strategy-agnostic implementation-readiness scoping memo (only if separately authorized).** Acceptable in principle but the binding constraint is strategy evidence, not infrastructure.
- **Option E — REJECTED: any C1 / V2 / G1 / R2 / F1 / D1-A rescue.** All forbidden by accumulated governance.
- **Option F — REJECTED: immediate new strategy spec / backtest / implementation / data acquisition.** All rejected.
- **Option G — FORBIDDEN: paper / shadow / live / exchange-write / Phase 4 canonical / production keys / MCP / Graphify / `.mcp.json` / credentials.** All forbidden.
- **Option H — FORBIDDEN: merging Phase 4z to main without explicit operator instruction.** Phase 4z is preserved on its feature branch unless and until the operator separately instructs a merge.

**Phase 5 / Phase 4aa / any successor phase are NOT authorized by Phase 4z.** Each future authorization is operator-driven and would be separately approved.

## Next authorization status

```text
Phase 5 / Phase 4aa / successor    : NOT authorized
Phase 4 (canonical)                : NOT authorized
Paper / shadow                     : NOT authorized
Live-readiness                     : NOT authorized
Deployment                         : NOT authorized
Production-key creation            : NOT authorized
Authenticated REST                 : NOT authorized
Private endpoints                  : NOT authorized
User stream / WebSocket            : NOT authorized
Exchange-write capability          : NOT authorized
MCP / Graphify                     : NOT authorized
.mcp.json / credentials            : NOT authorized
C1 implementation                  : NOT authorized; terminal-rejected
C1 rerun                           : NOT authorized; terminal-rejected
C1 spec amendment                  : NOT authorized; FORBIDDEN
Phase 4w methodology amendment     : NOT authorized; FORBIDDEN
Phase 4m gate amendment            : NOT authorized; recommendations only
Phase 4t matrix amendment          : NOT authorized; recommendations only
Phase 4u opportunity-rate
  principle amendment              : NOT authorized; recommendations only
G1 / V2 / R2 / F1 / D1-A rescue    : NOT authorized; FORBIDDEN
G1-prime / G1-extension axes       : NOT authorized; FORBIDDEN
V2-prime / V2-variant              : NOT authorized; FORBIDDEN
C1-prime / C1-extension            : NOT authorized; FORBIDDEN
Retained-evidence rescue           : NOT authorized; FORBIDDEN
5m strategy / hybrid               : NOT authorized; not proposed
ML feasibility                     : NOT authorized; not proposed
Microstructure / liquidity-timing data acquisition (Phase 4t Candidate F)
                                   : NOT authorized; data unavailable
Mark-price / aggTrades / spot / cross-venue acquisition
                                   : NOT authorized; FORBIDDEN
Fresh-hypothesis discovery memo    : NOT authorized; would require
                                     separate operator authorization
Strategy-spec memo                 : NOT authorized; would require
                                     separate operator authorization
Backtest-plan memo                 : NOT authorized; would require
                                     separate operator authorization
Backtest-execution phase           : NOT authorized; would require
                                     separate operator authorization
Implementation-readiness scoping
  memo                             : NOT authorized; not recommended
Documentation-refresh / governance
  -template update memo            : NOT authorized; conditional
                                     secondary in operator decision menu
Phase 4z merge to main             : NOT authorized; preserved on
                                     feature branch unless separately
                                     instructed
Adoption of Phase 4z proposed
  redesigns as governance          : NOT authorized; recommendations only
```

The next step is operator-driven: the operator decides whether to remain paused, merge Phase 4z to main and adopt a subset of its proposed redesigns through a separately authorized governance-update phase, or take some other action. Until then, the project remains at the post-Phase-4y consolidation boundary on `main` with Phase 4z preserved on its feature branch.

---

**Phase 4z is text-only. No source code, tests, scripts, data, manifests, governance files, retained verdicts, or project locks were created or modified. Phase 4z's proposed redesigns are recommendations for any future research-process memo, not adopted governance. C1 first-spec remains terminally HARD REJECTED. V2 first-spec remains terminally HARD REJECTED. G1 first-spec remains terminally HARD REJECTED. F1 remains HARD REJECT. D1-A remains MECHANISM PASS / FRAMEWORK FAIL. R2 remains FAILED — §11.6. R3 remains BASELINE-OF-RECORD. H0 remains FRAMEWORK ANCHOR. R1a / R1b-narrow remain RETAINED — NON-LEADING. Recommended state: remain paused. No next phase authorized.**
