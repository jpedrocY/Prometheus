# Phase 3u — Implementation-Readiness and Phase-4 Boundary Review (docs-only)

**Authority:** Phase 2f Gate 1 plan §§ 8–11; Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); Phase 2y §11.3.5 (no post-hoc loosening); Phase 2w §16.1 (R2 FAILED — §11.6); Phase 3d-B2 (F1 HARD REJECT); Phase 3j (D1-A MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3k post-D1-A research consolidation; Phase 3l external execution-cost evidence review; Phase 3m regime-first research framework memo; Phase 3n 5m timeframe feasibility memo; Phase 3o 5m diagnostics-spec memo; Phase 3p 5m diagnostics data-requirements + execution-plan memo; Phase 3q 5m data acquisition + integrity validation; Phase 3r mark-price gap governance memo (§8 Q6 invalid-window exclusion rule); Phase 3s 5m diagnostics execution; **Phase 3t post-5m diagnostics consolidation and research-thread closure memo (5m research thread operationally complete and closed)**; `docs/00-meta/ai-coding-handoff.md`; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/implementation-ambiguity-log.md`; `docs/09-operations/first-run-setup-checklist.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/08-architecture/state-model.md`; `docs/08-architecture/runtime-persistence-spec.md`; `docs/08-architecture/database-design.md`; `docs/08-architecture/internal-event-contracts.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/kill-switches.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 3u — Docs-only **implementation-readiness and Phase-4 boundary review.** Determines whether the project should later move toward implementation-readiness / Phase-4 boundary work or remain paused. **Phase 3u must not start Phase 4.** Phase 3u writes no implementation code; modifies no runtime, strategy, execution, risk, database, dashboard, or exchange code; runs no diagnostics; runs no backtests; acquires no data; modifies no manifests; modifies no strategy specs / thresholds / project-locks / prior verdicts; proposes no strategy rescue; proposes no new strategy candidate; authorizes no paper/shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write capability.

**Branch:** `phase-3u/implementation-readiness-and-phase-4-boundary-review`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false` — all preserved verbatim. Recommendation is provisional and evidence-based; the operator decides.

---

## 1. Summary

Phase 3u answers a forward-looking strategic question that the project record has not yet addressed explicitly: **now that the V1 / F1 / D1-A research arcs and the entire 5m research thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) have closed without producing an actionable strategy candidate, should the project consider moving toward Phase-4 implementation-readiness work, or should it remain paused?**

**Phase 3u recommends remain paused as primary.** A carefully-bounded conditional secondary alternative (a future docs-only **Phase 4a safe-slice scoping memo** evaluating which runtime-infrastructure components are buildable today *without* committing to any live strategy and *without* exchange-write capability) is acceptable but not endorsed over remain-paused. Full Phase 4 (runtime / state / persistence / risk-runtime as a coherent live-capable system) is **not** authorized; per `phase-gates.md`, Phase 4 requires Phase 3 strategy evidence which the project has not produced.

The reasoning rests on three parallel observations:

1. **No strategy is ready.** All retained-evidence candidates failed framework discipline. R3 baseline-of-record is V1's strongest result but is aggregate-negative on R-window expR. R2 / F1 / D1-A are terminal under current locked spec. Phase 3s findings are descriptive only and explicitly forbidden from authorizing strategy rescue (Phase 3o §6 / Phase 3p §8 / Phase 3r §8 / Phase 3t §9). **Building a live runtime *for which strategy* is the missing premise.**
2. **Documentation is mature but has a small number of resolvable pre-coding blockers.** The architecture / risk / runtime / dashboard / operations / security / interface documentation is substantially complete (per `current-project-state.md` "Completed / Substantially Defined Documentation"). However, the implementation-ambiguity log (`docs/00-meta/implementation-ambiguity-log.md`) contains four currently OPEN items — including **GAP-20260424-032 (backtest trade-price stops vs live MARK_PRICE stops)**, which is a real pre-coding blocker for any future runtime that handles stop placement. These should be resolved before any coding phase, regardless of whether that phase is Phase 4a safe-slice or full Phase 4.
3. **Implementation-readiness work has independent value if and only if it is strictly local-only and exchange-write-free.** Building runtime infrastructure (in-process state machine; persistence schemas; fake-exchange dry-run; dashboard-state read model; restart / kill-switch behavior) does not require a strategy to be ready and does not commit the project to any specific strategy. Such work is "common runtime ground" that any future strategy would need. **But it must not be allowed to drift into "Phase 4 means we're getting ready for live trading"** — the project has no live strategy and no path to one. Phase 4a, if ever authorized, must be procedurally and rhetorically separated from live-readiness, paper/shadow planning, deployment, production-key creation, and exchange-write capability.

**Phase 3u explicitly does not authorize Phase 4 or Phase 4a.** Phase 3u is a forward-looking review that the operator can use to decide what to consider next — either "remain paused indefinitely" (Option A primary) or "authorize a docs-only Phase 4a scoping memo" (Option B conditional secondary) — or to set aside both options and return to the strategic-pause posture.

The four currently-OPEN ambiguity-log items are **pre-coding blockers** regardless of which option the operator selects; if either Phase 4a or fresh-hypothesis research is ever authorized, those items should be resolved first.

---

## 2. Authority and boundary

Phase 3u operates strictly inside the post-Phase-3t boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5 / §6 / §7 / §10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation conclusions. Nothing is revised.
- **Phase-gate governance respected.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 follows Phase 3 strategy evidence. Phase 3u explicitly does not authorize Phase 4 — only evaluates whether and how a future Phase 4a-style scoping decision could be made consistent with the phase-gate model.
- **Project-level locks preserved verbatim.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; mark-price stops; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md` — including stop widening forbidden, exchange-write before approved gate forbidden, production keys during early phases forbidden, blind retry forbidden, etc.

Phase 3u adds *forward-looking review language* — a written assessment of where the project stands and what choices the operator faces — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate.

---

## 3. Starting state

```text
branch:           phase-3u/implementation-readiness-and-phase-4-boundary-review
parent commit:    e982d9c2c18224584894d3501cf60ee79458dbc0 (post-Phase-3t-merge housekeeping)
working tree:     clean
main:             e982d9c2c18224584894d3501cf60ee79458dbc0 (unchanged)

5m research thread:  operationally complete and closed (Phase 3t).
v002 datasets:       locked; manifests untouched.
v001-of-5m datasets: trade-price research-eligible; mark-price research_eligible:false.
Source code:         no src/prometheus modification by Phase 3o-3t; intervals.py reverted to baseline.
Scripts:             scripts/phase3q_5m_acquisition.py and scripts/phase3s_5m_diagnostics.py exist on main; both standalone, read-only on existing data, no exchange-write.
```

No code under `src/prometheus/` modified by Phase 3u. No script modified by Phase 3u. No `data/` artefact modified by Phase 3u. No prior-phase report modified by Phase 3u.

---

## 4. Why this review exists

Phase 3u exists for **four** reasons:

1. **Strategic-direction question after research-thread closure.** Phase 3t closed the 5m research thread without producing an actionable strategy candidate. The natural next operator question is: *given that all three strategy arcs failed framework discipline and the 5m diagnostics produced descriptive-only findings, where does the project go from here?* The two non-rescue answer-shapes are: (a) remain paused indefinitely, accepting that the current framework discipline has not surfaced a live-eligible strategy; (b) prepare implementation infrastructure that any future strategy would need, while keeping framework discipline and exchange-write prohibition intact. Phase 3u evaluates both.
2. **Phase-gate clarity on what "Phase 4" actually means.** `docs/12-roadmap/phase-gates.md` §Phase 4 names "Risk, State, and Persistence Runtime" as the goal of that phase, with strategy evidence as the prerequisite. The phase-gate doc also describes Phase 6 ("Dry-Run Exchange Simulation") and Phase 7 ("Paper / Shadow Operation") as later stages. The semantic question for Phase 3u is: *is the runtime-infrastructure work that is described in §Phase 4 actually contingent on having a ready strategy, or could a strict subset of it be done as a "common runtime ground" exercise?* Phase 3u answers that question while respecting the phase-gate model.
3. **Pre-coding blocker review.** The implementation-ambiguity log (`docs/00-meta/implementation-ambiguity-log.md`) currently has four OPEN items, plus several ACCEPTED_LIMITATION and DEFERRED items. Some of these are genuinely pre-coding blockers (most importantly **GAP-20260424-032 — backtest uses trade-price stops; live uses MARK_PRICE stops**, which directly affects how any future runtime stop-handling must be specified). Phase 3u surfaces these as items that must be resolved before *any* coding phase regardless of which path the operator chooses.
4. **Anti-rescue procedural fortification.** Phase 3t §9 (non-actionability guardrails) and Phase 3t §13 (forbidden paths) preserve the prohibition on using Phase 3s findings to revise verdicts, change parameters, rescue strategies, or imply live-readiness. Phase 3u operates in a similar spirit: any future implementation-readiness work must not become a backdoor for "we're getting ready for live trading even though no strategy is ready." Phase 3u writes that prohibition into the project record explicitly.

---

## 5. Post-Phase-3t research state

### 5.1 What the project has

- **Three completed strategy-research arcs** (V1 / F1 / D1-A) with full predeclaration discipline, Phase 2f Gate 1 framework gate evaluations, and final verdicts:
  - **R3** — V1 breakout baseline-of-record per Phase 2p §C.1; aggregate-negative R-window expR but the strongest single candidate the project has produced.
  - **R1a, R1b-narrow** — V1 retained research evidence only; non-leading.
  - **R2** — V1 retained research evidence only; framework FAILED — §11.6 cost-sensitivity blocks.
  - **F1** — Mean-reversion retained research evidence only; HARD REJECT per Phase 3c §7.3 catastrophic-floor predicate.
  - **D1-A** — Funding-aware contrarian retained research evidence only; MECHANISM PASS / FRAMEWORK FAIL — other per Phase 3h §11.2.
- **Complete 5m research thread** (Phases 3o → 3p → 3q → 3r → 3s → 3t) with predeclaration discipline, supplemental v001-of-5m data, governance memo, executed Q1–Q7 diagnostics, and closure memo. Phase 3s informative findings (Q1, Q2, Q3 (+1R), Q6 (D1-A), Q7) are descriptive only and explicitly bound from authorizing any strategy / verdict / parameter / threshold / lock / live-readiness change.
- **Substantially complete project documentation** across all 11 documentation areas (per `current-project-state.md` "Completed / Substantially Defined Documentation"): Meta + Setup + Handoff; Strategy and Research; Data Layer; Backtesting and Validation; Execution and Exchange; Risk; Runtime Architecture; Operations; Security; Operator Interface; Roadmap / Governance.
- **Phase 1 local-development foundation** (Python project scaffold, dependency manager, test runner, lint / format / type-check tooling, configuration loader, logging, CLI entry point, fake / no-op runtime foundation). Per `current-project-state.md` "Implementation Readiness Status".
- **Phase 2 historical-data foundation** (BTCUSDT + ETHUSDT v002 15m + 1h-derived + 15m mark-price + funding-event datasets; manifested; locked). Plus Phase 3q v001-of-5m supplemental datasets (trade-price research-eligible; mark-price `research_eligible: false`).
- **Phase 3 strategy / backtesting research arc completed** (per the three terminal verdicts above).

### 5.2 What the project does not have

- **No live-eligible strategy candidate.** No strategy has passed framework gate evaluation in a way that would justify live exposure. R3 baseline-of-record is the strongest evidence but the V1 family is at its useful ceiling per Phase 2x; further framework-discipline-respecting work on V1 is not contemplated.
- **No fresh-hypothesis discovery in progress.** Phase 3a / Phase 3f produced F1 and D1-A respectively. A potential Phase 4th-strategy-arc-discovery has not been authorized; Phase 3t §14.2 explicitly lists this as "not recommended now".
- **No regime-first formal spec in progress.** Phase 3m's regime-first framework memo recommended remain paused; Phase 3s did not test regime classification; Phase 3t §14.3 explicitly lists this as "not recommended now".
- **No ML feasibility memo in progress.** Phase 3k / 3m / 3n / 3o all left ML feasibility unauthorized; no later phase changed that.
- **No formal cost-model revision in progress.** Phase 3l found "B — conservative but defensible"; Phase 3s Q5 confirmed this at 5m granularity; §11.6 = 8 bps HIGH per side stands.
- **No paper/shadow planning in progress.** Per `phase-gates.md`, paper/shadow follows Phase 4 + Phase 5 + Phase 6 readiness. None of those is authorized.
- **No live-readiness / deployment / production-key work in progress.** Per `phase-gates.md`, these follow paper/shadow + tiny-live evidence. Not authorized.

### 5.3 Pause posture

The project is in a deliberate strategic pause: research framework intact, retained-evidence verdicts locked, locks and thresholds preserved, no implementation-readiness work in progress, no exchange-write capability, no production keys. The pause is *not* a failure state — it is the correct response to the empirical pattern that three strategy arcs have framework-failed under unchanged discipline. Pausing preserves operator optionality while preventing post-hoc loosening that could compromise future research validity.

---

## 6. Phase-gate assessment

`docs/12-roadmap/phase-gates.md` defines the canonical phase sequence:

```text
PHASE 0 — Documentation and implementation planning
PHASE 1 — Local development foundation
PHASE 2 — Historical data and validation foundation
PHASE 3 — Backtesting and strategy conformance
PHASE 4 — Risk, state, and persistence runtime
PHASE 5 — Dashboard, observability, and alerts
PHASE 6 — Dry-run exchange simulation
PHASE 7 — Paper / shadow operation
PHASE 8 — Tiny live
PHASE 9 — Scaled live
```

### 6.1 Project's actual phase position

| Phase | Status | Notes |
|---|---|---|
| Phase 0 | **Complete.** | `current-project-state.md` documents Phase 0 audit completion. |
| Phase 1 | **Complete.** | Local-development foundation in place; tests / lint / mypy / pyproject set; standalone scripts proven. |
| Phase 2 | **Complete.** | v002 datasets locked; manifests; integrity-checked; reproducible. |
| Phase 3 | **Research arc closed without an actionable candidate.** | V1 / F1 / D1-A all terminal. 5m research thread closed (Phase 3t). |
| Phase 4 | **Not authorized.** | Per phase-gate doc, Phase 4 requires Phase 3 strategy evidence. The project does not have it. |
| Phase 5–9 | **Not authorized.** | Each is gated by the prior phase. |

### 6.2 Phase 4 gate analysis

`phase-gates.md` §Phase 4 lists Phase 4 entry criteria:

> - Phase 3 complete.
> - Risk docs stable.
> - Runtime architecture docs stable.

And exit criteria include:

> - runtime can represent safe/blocked/recovery states
> - persistence supports restart safety
> - risk gates fail closed
> - no exchange-write behavior exists

The Phase 4 entry criterion "Phase 3 complete" is technically satisfied in the sense that the Phase 3 *research arc* is closed — but it is *not* satisfied in the implicit sense of "strategy evidence sufficient to justify live exposure." The phase-gate doc was written under the assumption that Phase 3 produces a live-eligible candidate; the project's empirical reality is that Phase 3 produced *retained research evidence with terminal verdicts* and a baseline-of-record (R3) that is aggregate-negative net-of-cost.

**Phase 3u's interpretation of the phase-gate doc:** "Phase 3 complete" should be read as "Phase 3 work has reached a stable, documented endpoint" — which the project has — not as "Phase 3 has produced a live-eligible strategy" — which the project has not. Under this reading, **Phase 4 entry is technically permissible but Phase 4 *purpose* (preparing for live runtime) is not yet justified by strategy evidence.**

This tension is exactly what the Phase 4a safe-slice concept (§9 below) exists to address: build only the parts of Phase 4 that any future strategy would need, without committing to a specific strategy or to live-readiness.

### 6.3 Risk and runtime documentation stability

Per the required-reading list:

- `docs/08-architecture/implementation-blueprint.md` — exists; substantially defined.
- `docs/08-architecture/state-model.md` — exists; substantially defined per `current-project-state.md`.
- `docs/08-architecture/runtime-persistence-spec.md` — exists; substantially defined.
- `docs/08-architecture/database-design.md` — exists; substantially defined.
- `docs/08-architecture/internal-event-contracts.md` — exists; substantially defined.
- `docs/07-risk/position-sizing-framework.md` — exists; substantially defined.
- `docs/07-risk/exposure-limits.md` — exists; substantially defined.
- `docs/07-risk/stop-loss-policy.md` — exists; substantially defined.
- `docs/07-risk/kill-switches.md` — exists; substantially defined.

These are sufficient documentation to begin local-only Phase 4a-style scoping work — but the four currently-OPEN ambiguity-log items (§8 below) should be resolved first to avoid silent decisions during implementation.

---

## 7. Current documentation readiness

### 7.1 Documentation completeness

Per `current-project-state.md`, the following documentation areas are substantially defined:

1. Meta, Setup, and Handoff (5 docs).
2. Strategy and Research (3 docs + Phase 2 / Phase 3 implementation reports).
3. Data Layer (5 docs).
4. Backtesting and Validation (1 doc + framework checklist).
5. Execution and Exchange (6 docs).
6. Risk (6 docs).
7. Runtime Architecture (9 docs).
8. Operations (7 docs).
9. Security (6 docs).
10. Operator Interface (5 docs).
11. Roadmap / Governance (2 docs).

Plus the post-Phase-2 implementation-report record (Phase 2e through Phase 3t merge closeouts).

### 7.2 Currently-synchronized state

Per the post-Phase-3t-merge housekeeping commit, `docs/00-meta/current-project-state.md` records the post-Phase-3t boundary correctly. All Phase 3o → 3p → 3q → 3r → 3s → 3t paragraphs are present. The "Current phase" code block points at Phase 3t merge. The "Most recent merge" code block points at Phase 3t merge. This is sufficient synchronization for Phase 3u purposes.

### 7.3 Documentation areas that may need refresh before any coding phase

If the operator ever authorizes Phase 4a or fresh-hypothesis research, these documentation refreshes would be in scope but **out of scope for Phase 3u**:

- `docs/08-architecture/implementation-blueprint.md` may need a "Phase 4a safe slice" sub-scope definition if Phase 4a is ever briefed.
- `docs/00-meta/ai-coding-handoff.md` Phase 4 section may need clarifying language about "what 'Phase 4' means in the absence of strategy evidence."
- `docs/12-roadmap/phase-gates.md` may need a clarifying paragraph about Phase 4a as a strict subset of Phase 4 with explicit exchange-write prohibition.

These are *potential* future doc refreshes if and only if the operator authorizes the relevant successor phase. **Phase 3u does not write any of them.**

---

## 8. Technical-debt and blocker review

### 8.1 Currently-OPEN ambiguity-log items

Per `docs/00-meta/implementation-ambiguity-log.md`, four items are currently **OPEN**:

- **GAP-20260424-030 — Break-even rule text conflicts with spec Open Question #8.** Phase 3u characterization: documentation-level conflict in the V1 strategy spec. Resolution requires operator decision on the canonical break-even rule. Pre-coding blocker for any future runtime that implements break-even logic. **Risk: MEDIUM.**
- **GAP-20260424-031 — EMA slope wording ambiguous: discrete comparison vs. fitted slope.** Phase 3u characterization: documentation-level ambiguity. Already resolved at implementation level (the executed backtests use one specific definition) but the spec text is unclear. Pre-coding blocker for any future runtime that re-implements EMA bias. **Risk: LOW-MEDIUM.**
- **GAP-20260424-032 — Backtest uses trade-price stops; live uses MARK_PRICE stops.** Phase 3u characterization: **the most operationally significant OPEN item.** Backtest verdicts were produced under one stop-trigger model; live operation will use a different model (per §1.7.3 mark-price stops lock). The Phase 3s Q6 finding (D1-A mark-stop lag ~1.3–1.8 5m bars) directly characterizes this gap. Pre-coding blocker for any future runtime; pre-paper-shadow blocker for any live work. **Risk: HIGH.**
- **GAP-20260424-033 — Stagnation window not in Open Questions but discussed as metric.** Phase 3u characterization: documentation hygiene item. Pre-coding-blocker classification weak. **Risk: LOW.**

### 8.2 ACCEPTED_LIMITATION items

Several items are recorded as ACCEPTED_LIMITATION (e.g., GAP-20260419-018 taker commission rate parameterization; GAP-20260419-020 ExchangeInfo snapshot proxy; GAP-20260419-024 leverageBracket placeholder limitation). These are not pre-coding blockers in the strict sense but should be reviewed before any tiny-live transition (already documented as such in the technical-debt register).

### 8.3 DEFERRED items

GAP-20260419-025 (Phase 2e wider historical backfill proposed; Phase 3 completes on 2026-03 only) is DEFERRED. Not pre-coding-blocker for Phase 4a; pre-paper-shadow for any longer-history requirement.

### 8.4 Technical-debt register cross-reference

`docs/12-roadmap/technical-debt-register.md` defines blocker classifications including:
- TD-006 (exact Binance endpoint behavior verification) — partially resolved at coding time for bulk klines + mark-price; remains open for REST-write paths and user-stream behavior.
- TD-017 (exact public-IP solution for local NUC) — pre-tiny-live; not Phase-4a blocker.
- TD-018 (first live notional cap value) — pre-tiny-live; not Phase-4a blocker.
- TD-019 (production alert route selection) — pre-tiny-live; not Phase-4a blocker.
- TD-020 (backup schedule and retention) — pre-tiny-live; not Phase-4a blocker.

### 8.5 Pre-coding-blocker summary

Phase 3u identifies the following items that should be resolved **before any coding phase** (whether Phase 4a safe-slice or fresh-hypothesis-research successor):

1. **GAP-20260424-032** (mark-price-vs-trade-price stop policy) — HIGH risk. Should be resolved by a separately authorized docs-only memo that specifies the canonical stop-trigger model for any future runtime, given that the §1.7.3 mark-price-stops lock and the Phase 3s Q6 D1-A finding are now both on record.
2. **GAP-20260424-030** (break-even rule conflict) — MEDIUM risk. Should be resolved by a docs-only spec-clarification memo.
3. **GAP-20260424-031** (EMA slope wording) — LOW-MEDIUM risk. Should be resolved by a docs-only spec-clarification memo.
4. **GAP-20260424-033** (stagnation window) — LOW risk. May be resolved as part of broader documentation hygiene.

**Phase 3u recommends that any operator decision to move toward implementation work be preceded by a docs-only ambiguity-resolution phase** that resolves at minimum GAP-20260424-032 (and ideally the other three). Phase 3u does not authorize that ambiguity-resolution phase; it recommends it.

---

## 9. What Phase 4 would mean

Per `docs/12-roadmap/phase-gates.md` §Phase 4:

- **Purpose:** Implement the runtime safety foundation before live execution.
- **Required build outputs:** risk sizing engine; exposure gate engine; stop validation; daily loss state; drawdown state; runtime state model; internal event/message contracts; runtime database schema; migrations; audit/runtime event storage; restart-critical persistence; safe-mode startup.
- **Required tests/evidence:** risk sizing tests pass; below-minimum quantity rejects; leverage/notional cap tests pass; missing metadata fails closed; one-position/no-pyramiding/no-reversal gates pass; kill switch persists across restart; runtime starts in safe mode; runtime DB backup/restore smoke test passes; state transition and event log transaction tests pass.
- **Exit criteria:** runtime can represent safe/blocked/recovery states; persistence supports restart safety; risk gates fail closed; no exchange write capability required.

**Phase 4 in the canonical phase-gate model is therefore "build the runtime that any strategy would flow through, with no exchange-write capability."** This is a *strategy-agnostic infrastructure* phase. The phase does not require a specific live strategy; it requires the runtime to be representable in safe / blocked / recovery states and to handle restart-safety.

### 9.1 Phase 4 dependencies that ARE met today

- Phase 1 local-development foundation: complete.
- Phase 2 historical-data foundation: complete; v002 datasets locked.
- Phase 3 research arc closed (in the "research has reached an endpoint" sense).
- Risk documentation stable: complete (per §7.1).
- Runtime architecture documentation stable: complete (per §7.1).
- Internal event contracts documented: complete.
- Database design documented: complete.
- Runtime persistence spec documented: complete.

### 9.2 Phase 4 dependencies that are NOT met today

- **Strategy evidence sufficient to justify live exposure: NOT MET.** The implicit dependency in the phase-gate doc — that Phase 3 produces a live-eligible candidate — is not satisfied empirically. R3 is aggregate-negative; R2 / F1 / D1-A are terminal under current spec.
- **Operator-explicit strategic decision that the project should move toward live operation: NOT GIVEN.** The cumulative pattern across nine phases (Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r / 3s) is "remain paused"; Phase 3t reinforced this.
- **GAP-20260424-032 (mark-price vs trade-price stop) resolution: NOT DONE.** Real pre-coding blocker.

### 9.3 Phase 4 is therefore not appropriate as currently framed

The honest position is: **the canonical Phase 4 framing assumes a strategy is forthcoming, and the project's empirical reality is that no strategy is forthcoming under current framework discipline.** Authorizing canonical Phase 4 now would create rhetorical pressure to "have a strategy ready by the end of Phase 4" — exactly the kind of pressure that compromises framework discipline.

The correct response is one of:
- **Remain paused** (Option A primary).
- **Authorize a docs-only Phase 4a safe-slice scoping memo** that explicitly redefines Phase 4 as a *strategy-agnostic infrastructure* phase with no live-readiness implication, no exchange-write capability, no paper/shadow commitment, and no commitment to a specific strategy (Option B conditional secondary).
- **Continue research-paused indefinitely until either a fresh-hypothesis idea emerges from external sources or the operator decides to retire the project altogether** (Option C tertiary).

---

## 10. What Phase 4 must not mean

If Phase 4 (in any form, including a hypothetical Phase 4a safe-slice) is ever authorized, it must NOT mean:

- **It must NOT mean live-readiness.** Phase 4 produces no live-capable code; it produces strategy-agnostic infrastructure that any future authorized strategy would need.
- **It must NOT enable exchange-write capability.** Per `phase-gates.md` Phase 4 exit criterion: "no exchange write capability required." Phase 4 code paths must categorically exclude live order placement, live cancellation, live state mutation. Fake-exchange / dry-run only.
- **It must NOT require production Binance keys.** Per `.claude/rules/prometheus-mcp-and-secrets.md` and `phase-gates.md`, production keys are forbidden until the appropriate phase gate (Phase 8 territory). Phase 4a / 4 must not request, store, or use production keys.
- **It must NOT skip strategy evidence.** Phase 4 cannot be used as a backdoor to declare the system "almost ready" when no strategy is ready. The phase output must explicitly state that no strategy is authorized for live operation.
- **It must NOT silently enable paper/shadow.** Paper/shadow is Phase 7 territory and requires its own authorization. Phase 4 / 4a output must not initiate paper/shadow.
- **It must NOT relax §1.7.3, §10.3 / §10.4 / §11.3 / §11.4 / §11.6, mark-price stops, or any other lock.** All locks remain preserved.
- **It must NOT modify v002 datasets / manifests, Phase 3q v001-of-5m manifests, or Phase 3s diagnostic outputs.** All evidence preserved verbatim.
- **It must NOT propose strategy rescue or new strategy candidates.** Strategy work is research; runtime work is infrastructure. They must not blur.
- **It must NOT activate MCP / Graphify / `.mcp.json` / credentials.** Per project rules.
- **It must NOT use private Binance endpoints, user stream, or WebSocket subscriptions.** Public bulk-archive only for any data work; fake-exchange for any execution work.
- **It must NOT request or store secrets.**

These prohibitions are not aspirational — they are binding constraints that any future Phase 4 / 4a brief must reaffirm explicitly.

---

## 11. Candidate Phase 4a safe slice

If the operator ever authorizes a docs-only Phase 4a safe-slice scoping memo, the following categories of work would be candidates for the slice. **Phase 3u does not authorize any of this work.** Phase 3u lists candidates only so that the operator's eventual scoping decision has a starting framework.

### 11.1 In-scope candidates for Phase 4a (subject to operator authorization)

- **In-process state machine for runtime modes** (`SAFE_MODE`, `RUNNING`, `BLOCKED`, `EMERGENCY`, etc.) per `docs/08-architecture/state-model.md`.
- **Persistence schemas** (SQLite / WAL / `runtime.db` per `docs/08-architecture/runtime-persistence-spec.md` and `docs/08-architecture/database-design.md`).
- **Internal event contracts** (typed events per `docs/08-architecture/internal-event-contracts.md`).
- **Risk sizing engine** (per `docs/07-risk/position-sizing-framework.md`); fail-closed; no order placement.
- **Exposure-limit gate engine** (per `docs/07-risk/exposure-limits.md`); fail-closed.
- **Kill-switch state machine** (per `docs/07-risk/kill-switches.md`); persistent across restart; never auto-clears.
- **Stop-validation engine** (per `docs/07-risk/stop-loss-policy.md`); validates that any proposed stop satisfies project locks; never places orders.
- **Fake-exchange dry-run adapter** (per `docs/06-execution-exchange/exchange-adapter-design.md`); used for end-to-end runtime testing without exchange-write capability.
- **Dashboard read model** (per `docs/11-interface/operator-dashboard-requirements.md`); read-only state visualization.
- **Restart / safe-mode-first behavior** (per `docs/09-operations/restart-procedure.md`); kill-switch persistence; reconciliation-required-on-startup gates.

### 11.2 Out-of-scope categories for Phase 4a (forbidden in any form)

- **Live exchange-write code paths.**
- **Production Binance keys.**
- **Authenticated REST or WebSocket calls.**
- **User-stream subscriptions (real or simulated as stand-in for live).**
- **Paper/shadow execution.**
- **Live runtime deployment.**
- **Tiny-live or any real-capital exposure.**
- **Strategy commitment** (Phase 4a must accept any future authorized strategy, not commit to one).
- **Verdict revision, parameter change, threshold revision, project-lock revision, strategy rescue.**
- **MCP / Graphify / `.mcp.json` / credentials.**

### 11.3 Phase 4a's framing requirement

Phase 4a, if ever authorized, must be framed as: *"Build strategy-agnostic runtime infrastructure that any future authorized strategy would need, using only fake-exchange / local / dry-run execution paths, with explicit prohibition on live exchange-write capability and on any live-readiness implication."* The operator authorization brief for Phase 4a should reaffirm this framing in writing before any code is written.

### 11.4 Phase 4a's success criteria

If Phase 4a were ever to complete successfully, the success criterion would be: *"The project has a working strategy-agnostic runtime that can represent SAFE_MODE / BLOCKED / RUNNING / EMERGENCY states, persist runtime control state across restart, fail closed on unknown state, drive a fake-exchange dry-run end-to-end, and surface state via a read-only dashboard — without ever placing a real order or holding a real-capital position."*

This success would *not* by itself justify any subsequent phase. Paper/shadow (Phase 7), tiny-live (Phase 8), scaled live (Phase 9) would each require separate operator authorization with their own evidence.

---

## 12. Risks of moving too early

Phase 3u identifies the following risks if the operator authorizes Phase 4a or any other implementation-readiness phase **prematurely** (i.e., without addressing the pre-coding blockers and without explicit anti-rescue / anti-live-readiness framing):

### 12.1 Live-readiness rhetoric drift

The phrase "Phase 4" carries implicit "we're getting closer to live" connotation. Even if Phase 4a is technically strategy-agnostic infrastructure, the rhetorical drift toward "we're almost ready for live operation" is a real risk. **Mitigation:** Phase 4a brief must explicitly disclaim live-readiness, paper/shadow, deployment, and exchange-write capability.

### 12.2 Implicit strategy commitment

Building a runtime without naming a strategy creates pressure to "have a strategy by the time the runtime is ready." That pressure is exactly the kind that compromises framework discipline (post-hoc loosening of evidence thresholds; rescue framing for retained-evidence candidates). **Mitigation:** Phase 4a brief must explicitly state that runtime infrastructure does not constitute or imply strategy authorization.

### 12.3 Scope creep into exchange-write paths

A common failure mode in trading-system implementation is: "the runtime is ready, let's just *test* the exchange adapter with a real (small) order." That is exactly what `phase-gates.md` Phase 8 / Phase 9 prohibit. **Mitigation:** Phase 4a code must architecturally prohibit exchange-write capability — not just by configuration but by code structure (e.g., the live exchange adapter is simply not implemented; only the fake adapter exists).

### 12.4 Premature dependency on unresolved pre-coding blockers

If GAP-20260424-032 (mark-price vs trade-price stop) is not resolved before runtime stop-handling is coded, the runtime will encode one model and the eventual paper/shadow / live work will need to encode another. **Mitigation:** resolve all four currently-OPEN ambiguity-log items before any coding phase.

### 12.5 Misrepresentation of project status

If Phase 4a is authorized but treated externally (in any context — internal docs, PRs, commits, future audits) as "Phase 4 is in progress, getting ready for live", the project record becomes misleading. **Mitigation:** every Phase 4a-related artefact must include a "no live-readiness, no exchange-write, no strategy commitment" disclaimer, analogous to how Phase 3o–3t artefacts include "descriptive only, not actionable" disclaimers.

### 12.6 Distraction from research

If the operator authorizes Phase 4a now, attention naturally moves from research to implementation. Without a clear research direction (which the project does not currently have), this could mean implementation work continues indefinitely while research stalls. **Mitigation:** Phase 4a should be authorized only if the operator has consciously chosen to deprioritize research for a defined period — not as a default response to research stalling.

---

## 13. Benefits of implementation-readiness work

If implementation-readiness work is ever authorized (under the bounded conditions above), it could deliver the following benefits:

### 13.1 Common ground for any future strategy

Runtime infrastructure (state machine; persistence; risk gates; fake-exchange dry-run) is required by any future strategy. Building it once, in a strategy-agnostic way, avoids duplicating the work later when a specific strategy is authorized.

### 13.2 Forces precise specification of risk / state / exposure / kill-switch behavior

Documentation describes intended behavior; implementation forces precise specification. The act of writing code surfaces specification ambiguities that documentation alone does not. (Phase 3u §8 already identified four such items in the ambiguity log; implementation work would surface more.) This forcing function is itself valuable — but only if the surfaced items are added to the ambiguity log and resolved through proper governance, not silently coded around.

### 13.3 Provides safety-rule enforcement infrastructure for any future strategy

`.claude/rules/prometheus-safety.md` lists prohibitions (no exchange-write before approved gate; no production keys early; no blind retry; restart in SAFE_MODE; kill switch never auto-clears; etc.). Implementing these as code-level constraints (not just policy text) is concrete safety value.

### 13.4 Enables fake-exchange dry-run end-to-end testing

A working fake-exchange dry-run is a testbed for any future strategy. Without it, future strategy authorization decisions are made on backtest evidence alone (which is what produced the V1 / F1 / D1-A terminal verdicts). With it, future strategies could be vetted in a fake-runtime context before any live consideration.

### 13.5 Provides operator visibility infrastructure

A read-only dashboard backed by runtime state is operator value regardless of whether any strategy is live. The operator can monitor system state, kill-switch state, persistence state, fake-exchange state — and have the same observability infrastructure ready for any future authorized strategy.

### 13.6 Reduces future technical-debt accumulation

The longer documentation sits without implementation, the more likely it is to drift from what implementation eventually does. Implementation-readiness work — done carefully — closes this drift while it is still small.

### 13.7 Phase 3u's overall benefits-vs-risks assessment

The benefits in §13.1–13.6 are real but bounded. The risks in §12.1–12.6 are also real and well-documented from prior trading-system experience. **Phase 3u's net assessment is that the benefits do not by themselves justify authorizing Phase 4a now**, given that:

- The pre-coding blockers (§8) are not yet resolved.
- The 5m research thread closure (Phase 3t) is recent; the operator's strategic posture has not been re-evaluated since.
- Remain-paused has been the cumulative pattern across nine prior phases; reversing that pattern should be deliberate, not reactive.
- The operator has not signaled an intent to deprioritize research in favor of implementation; without that signal, authorizing implementation work risks the "distraction from research" failure mode in §12.6.

If the operator has not consciously decided to deprioritize research, the correct posture is remain paused.

---

## 14. Fresh-hypothesis research alternative

An alternative to Phase 4a (and to remain paused) is **fresh-hypothesis research**: authorize a Phase 3a / Phase 3f-style new-strategy-discovery memo that proposes an entirely new strategy family from first principles, *not* derived from any retained-evidence candidate or from Phase 3s findings.

Phase 3t §14.2 evaluated this option and recommended **not now**, citing:

- Three strategy-research arcs have framework-failed under unchanged discipline; starting a fourth without first addressing *why* the first three failed (which Phase 3m's regime-first thinking and Phase 3s's mechanism findings could in principle inform) is procedurally premature.
- A fresh-hypothesis discovery would be subject to Phase 3a / 3f rigour: predeclared evidence thresholds; M1 / M2 / M3 mechanism check; framework discipline. The likelihood of a clean fourth arc passing where three previous arcs failed is bounded.

**Phase 3u reaffirms Phase 3t's recommendation: fresh-hypothesis research should remain paused for now.** The Phase 3s mechanism findings (Q1 universal entry-path adverse bias; Q2 stop-pathology differentiation) could in principle inform a future first-principles hypothesis design — but the discipline that would protect such a hypothesis from being a covert post-hoc rescue requires separately authorized framing memos, not direct conversion of Q3 / Q6 findings into rule design (forbidden by Phase 3o §6).

If the operator ever wishes to authorize fresh-hypothesis research, it should be with explicit anti-rescue / anti-circular-reasoning preconditions, predeclared evidence thresholds, and a clear separation from the Phase 3s findings.

---

## 15. Recommendation

**Phase 3u recommends Option A (remain paused) as primary.**

The reasoning, in compact form:

1. **No strategy is ready** (Phase 3 research arc closed; R3 baseline-of-record but aggregate-negative; R2 / F1 / D1-A terminal). Building runtime infrastructure for "no specific strategy" carries real risks (§12.1–12.6) without offsetting urgency.
2. **Pre-coding blockers exist** (§8.5). At minimum GAP-20260424-032 (mark-price vs trade-price stop) should be resolved by a separate docs-only memo before any coding phase.
3. **Cumulative pattern is "remain paused"** across Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r / 3s / 3t (ten phases including Phase 3u itself if Phase 3u also recommends remain paused). Reversing that pattern should be a deliberate strategic decision, not a reactive response to research stalling.
4. **Documentation is sufficient** for Phase 3u purposes; refresh of doc set is *not* a precondition for remain paused; a partial refresh could become useful if and only if Phase 4a is ever authorized.
5. **Fresh-hypothesis research** also remains paused per Phase 3t §14.2 and Phase 3u §14.

Phase 3u explicitly does NOT recommend:

- Phase 4 (canonical) — not authorized by any precondition.
- Phase 4a (safe slice) — not recommended now; conditional secondary alternative only if the operator has consciously decided to deprioritize research and is willing to commit to the §10 prohibitions.
- Fresh-hypothesis research — not recommended now; preserves Phase 3t §14.2 recommendation.
- Paper/shadow / live-readiness / deployment / production-key / exchange-write — forbidden by phase-gate model.
- ML feasibility, regime-first formal spec, formal cost-model revision — preserved as not-recommended-now per prior phase recommendations.
- Strategy rescue (R2 / F1 / D1-A successor / D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / 5m-on-X) — preserved as forbidden per Phase 3o §6 / Phase 3p §8 / Phase 3r §8 / Phase 3t §13.

Phase 3u answers the originally-asked questions:

| Question | Phase 3u answer |
|---|---|
| Whether implementation-readiness work can help future strategy discovery without pretending current strategies work | **Yes — but only under strict §10 prohibitions, only after pre-coding blockers (§8) are resolved, and only if the operator has consciously chosen to deprioritize research.** Not recommended now. |
| Whether Phase 4 should remain unauthorized | **Yes.** Canonical Phase 4 framing assumes strategy evidence; the project does not have it. |
| Whether a future Phase 4a, if later authorized, must be local-only and exchange-write-free | **Yes — categorically.** Phase 4a must be local / fake-exchange / dry-run only, with no production keys, no exchange-write, no live-readiness implication, no paper/shadow commitment. (§10, §11.) |
| Whether fresh-hypothesis research should remain paused for now | **Yes.** Per Phase 3t §14.2 and Phase 3u §14. |
| Whether current documentation is sufficiently synchronized after Phase 3t | **Yes for Phase 3u purposes.** Possible refreshes (§7.3) are out of scope unless Phase 4a is ever authorized. |
| Whether any stale docs, technical debt, ambiguity, or blockers should be resolved before any coding phase | **Yes — at minimum the four currently-OPEN ambiguity-log items should be resolved by separately authorized docs-only memos before any Phase 4a or fresh-hypothesis-research coding work begins. Most importantly GAP-20260424-032 (mark-price vs trade-price stop) — HIGH risk.** |

---

## 16. Operator decision menu

The operator now has a forward-looking review of the implementation-readiness boundary. The next operator decision is operator-driven only.

### 16.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategic pause continues. Phase 3u joins Phase 3k / 3l / 3m / 3n / 3o / 3p / 3q / 3r / 3s / 3t as the running record of the post-V1 / post-F1 / post-D1-A / post-5m-research-thread / post-implementation-readiness-review pause. No subsequent phase authorized.

**Reasoning:**
- §15 reasoning applies in full.
- Pausing preserves operator optionality for any future strategic-direction decision (research-resume, implementation-resume, project-retirement, etc.).
- All locks preserved verbatim.
- Phase 3u's review value is realized by the memo itself — whether or not any Option B / C / D follows.

**What this preserves:** Everything in §10, §13.7, and §15.

**What this rules out:** No Phase 4 / Phase 4a / fresh-hypothesis research / implementation work / paper-shadow / live-readiness / deployment / production-key / exchange-write activity.

### 16.2 Option B — Authorize a docs-only ambiguity-resolution memo (CONDITIONAL secondary alternative; arguably useful regardless of any subsequent phase)

**Description:** Authorize a future docs-only memo that resolves at minimum GAP-20260424-032 (and ideally also GAP-20260424-030 / 031 / 033). The memo would specify the canonical mark-price vs trade-price stop policy for any future runtime, given that the §1.7.3 mark-price-stops lock and the Phase 3s Q6 D1-A finding are now both on record.

**Reasoning if selected:**
- The four OPEN ambiguity-log items are pre-coding blockers regardless of which path the operator eventually selects (Phase 4a, fresh-hypothesis research, or even continued pause). Resolving them now is unconditionally useful.
- This is a low-risk docs-only step. It does not commit the project to any subsequent phase.
- It produces concrete documentation value that any future implementation work would inherit.

**Pre-conditions if selected:**
- Operator commits ex-ante that the ambiguity-resolution memo cannot license verdict revision, parameter change, threshold revision, or project-lock revision.
- Operator commits ex-ante that resolving the items does not authorize any subsequent phase.

**Risks if selected:**
- Procedural escalation: another docs-only memo on the running thread. Marginal value bounded.
- The resolution of GAP-20260424-032 may itself surface further questions (e.g., backtest re-running with mark-price stops to validate the magnitude of the gap) that would need separate authorization. The memo should explicitly state that it produces only documentation, not analysis.

**Phase 3u view:** Acceptable as conditional secondary. Not endorsed over Option A purely because it is incremental docs work and the operator may equally validly stay paused indefinitely.

### 16.3 Option C — Authorize a docs-only Phase 4a safe-slice scoping memo (CONDITIONAL tertiary alternative)

**Description:** Authorize a future docs-only memo that defines Phase 4a as a strict subset of Phase 4: strategy-agnostic runtime infrastructure, local / fake-exchange / dry-run only, with explicit §10 prohibitions in writing.

**Pre-conditions if selected:**
- Operator commits ex-ante that the scoping memo cannot license live-readiness, paper/shadow, deployment, production-key creation, exchange-write capability, MCP / Graphify / `.mcp.json` / credentials work.
- Operator commits ex-ante that the scoping memo does not authorize Phase 4a *execution*; it only specifies what Phase 4a would entail if ever authorized.
- Operator commits ex-ante that pre-coding blockers (§8.5) must be resolved before any Phase 4a execution authorization.
- Operator commits ex-ante that authorizing the scoping memo does not commit the project to deprioritizing research.

**Risks if selected:**
- "Live-readiness rhetoric drift" (§12.1) is real — the very phrase "Phase 4" carries connotation. The scoping memo must be explicit and forceful in disclaiming live-readiness.
- Procedural escalation toward implementation. Once a scoping memo exists, the next operator decision becomes whether to authorize execution. The slope is real.

**Phase 3u view:** Acceptable as conditional tertiary. Not endorsed over Option A or Option B. Should be pursued only if the operator has consciously decided to deprioritize research for a defined period.

### 16.4 Option D — Authorize fresh-hypothesis research (NOT RECOMMENDED NOW)

**Description:** Authorize a Phase 3a / Phase 3f-style new-strategy-discovery memo proposing an entirely new strategy family from first principles, not derived from any retained-evidence candidate or Phase 3s findings.

**Phase 3u view:** **Not recommended now.** Per Phase 3t §14.2 and Phase 3u §14.

### 16.5 Option E — Phase 4 (canonical), paper/shadow, live-readiness, deployment, production-key creation, exchange-write capability (FORBIDDEN / NOT RECOMMENDED)

**Phase 3u view:** **Forbidden / not recommended.** Per `phase-gates.md`, none of these gates is met. Strongly not recommended. (Same posture as Phase 3t §14.4.)

### 16.6 Recommendation

**Phase 3u recommends Option A (remain paused) as primary.** Option B (docs-only ambiguity-resolution memo, especially GAP-20260424-032) is a reasonable conditional secondary that produces unconditional documentation value but is not endorsed over remain-paused. Option C (docs-only Phase 4a safe-slice scoping memo) is a conditional tertiary that should be selected only with explicit anti-live-readiness preconditions and explicit operator commitment to deprioritize research for a defined period. Options D and E are not recommended.

---

## 17. Next authorization status

**No next phase has been authorized.** Phase 3u authorizes nothing other than producing this review memo and the accompanying closeout artefact. The operator's decision after Phase 3u is operator-driven only.

Selection of any subsequent phase (ambiguity-resolution memo per Option B; Phase 4a safe-slice scoping memo per Option C; fresh-hypothesis research per Option D; Phase 4 / paper-shadow / live-readiness / deployment / production-key / exchange-write per Option E) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread (Phases 3o → 3p → 3q → 3r → 3s → 3t) remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary (Phase 3u) has now been written into the project record. **Recommended state remains paused.**
