# Phase 3x — Phase 4a Safe-Slice Scoping Memo (docs-only)

**Authority:** Phase 2i §1.7.3 project-level locks (mark-price stops; one-position max; 0.25% risk; 2× leverage cap; v002 datasets); Phase 2y §11.3.5 (no post-hoc loosening); Phase 2p §C.1 (R3 baseline-of-record); Phase 2w §16.1 (R2 FAILED — §11.6); Phase 3d-B2 (F1 HARD REJECT); Phase 3j §11.2 (D1-A MECHANISM PASS / FRAMEWORK FAIL — other); Phase 3t (5m research thread closure); Phase 3u §10 / §11 (Phase 4 / Phase 4a prohibition list and candidate-scope outline); Phase 3v §8 (stop-trigger-domain governance — `stop_trigger_domain` label scheme); Phase 3w §6 / §7 / §8 (`break_even_rule`, `ema_slope_method`, `stagnation_window_role` label schemes); `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/08-architecture/state-model.md`; `docs/08-architecture/runtime-persistence-spec.md`; `docs/08-architecture/database-design.md`; `docs/08-architecture/internal-event-contracts.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/kill-switches.md`; `docs/06-execution-exchange/exchange-adapter-design.md`; `docs/06-execution-exchange/binance-usdm-order-model.md`; `docs/09-operations/first-run-setup-checklist.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 3x — Docs-only **Phase 4a safe-slice scoping memo.** Defines what a possible future Phase 4a execution phase would be — a strictly local-only, fake-exchange, dry-run, exchange-write-free implementation scope — and what it must categorically not be. **Phase 3x writes no implementation code. Phase 3x does not start Phase 4a execution.** Phase 3x modifies no runtime / strategy / execution / risk-engine / database / dashboard / exchange code; runs no diagnostics; runs no Q1–Q7 rerun; runs no backtests; acquires no data; modifies no manifests; modifies no v002 datasets / manifests; modifies no Phase 3q v001-of-5m manifests; revises no retained-evidence verdict; modifies no §11.6 / §1.7.3 lock; modifies no Phase 3v §8 stop-trigger-domain governance; modifies no Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance; proposes no strategy rescue; proposes no new strategy candidate; proposes no 5m strategy / hybrid / retained-evidence successor / new variant; authorizes no Phase 4 / 4a execution / paper-shadow / live-readiness / deployment / production-key / credentials / MCP / Graphify / `.mcp.json` / exchange-write capability.

**Branch:** `phase-3x/phase-4a-safe-slice-scoping`. **Memo date:** 2026-04-30 UTC.

**Status:** Recommendation drafted. R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`; Phase 3v §8 stop-trigger-domain governance; Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance — all preserved verbatim. Recommendation is provisional and evidence-based; the operator decides.

---

## 1. Summary

Phase 3x is the docs-only **Phase 4a safe-slice scoping memo** authorized as the conditional tertiary alternative from Phase 3u §16.3 (and the conditional secondary alternative from Phase 3w §17.2 once GAP-20260424-030 / 031 / 033 were resolved). Its purpose is to write into the project record a precise definition of what a possible future Phase 4a execution phase would be — a *strictly local-only, fake-exchange, dry-run, exchange-write-free* implementation scope — and what it must categorically not be.

**Phase 3x does NOT authorize Phase 4a execution.** Phase 3x is a scoping memo only. Authorizing Phase 4a execution would require a separate, explicit operator decision after Phase 3x is reviewed.

The core conclusions of the scoping exercise:

1. **All four Phase 3u §8.5 currently-OPEN pre-coding governance blockers are now RESOLVED at the governance level.** GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w. The procedural ground for *any* coding work is therefore cleaner than it was at Phase 3u. This does NOT itself authorize coding; it only removes the governance-level pre-coding blockers that Phase 3u flagged.

2. **Phase 4a, if ever authorized for execution, must be a strict subset of canonical Phase 4** that builds *strategy-agnostic runtime infrastructure* with no live-readiness implication, no exchange-write capability, no production keys, no authenticated APIs, no user-stream subscriptions, no WebSocket subscriptions, no paper/shadow commitment, no deployment, no strategy commitment, no strategy rescue, no new strategy candidate, no verdict revision, no parameter / threshold / project-lock revision, no MCP / Graphify / `.mcp.json` / credentials.

3. **Ten candidate Phase 4a components** are evaluated in §9. Each is assessed against the §6 prohibition list and §7 / §8 precondition tests. The components form a coherent strategy-agnostic runtime infrastructure scope: in-process state machine; runtime control state persistence; internal event contracts; risk sizing skeleton; exposure gate skeleton; stop-validation skeleton; break-even / EMA / stagnation governance label plumbing; fake-exchange adapter; read-only operator state view; test harness.

4. **The four governance label schemes from Phase 3v §8 + Phase 3w §6 / §7 / §8 (`stop_trigger_domain`, `break_even_rule`, `ema_slope_method`, `stagnation_window_role`) become enforceable in code at the Phase 4a layer** if Phase 4a is ever authorized. `mixed_or_unknown` must fail closed at any decision boundary in code, not only in policy text.

5. **Phase 4a scoping does not mean the project is moving to live.** Phase 4a execution, if later authorized, would NOT produce live-readiness; would NOT authorize paper/shadow; would NOT authorize production keys; would NOT authorize exchange-write capability; would NOT create or validate a strategy; would NOT revise any verdict; would NOT change any lock. These are binding constraints, not aspirational language.

**Phase 3x recommends Option A (remain paused) as primary**, while acknowledging that Option B (authorize future Phase 4a execution as local-only safe-slice, subject to a separate operator authorization brief that reaffirms the §6 prohibition list verbatim) is now procedurally well-grounded given that all four Phase 3u §8.5 pre-coding governance blockers are resolved. Option C (more docs-only preparation first) remains acceptable as conditional tertiary. Option D (return to research / sensitivity analysis) is not recommended now. Option E (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) is forbidden / not recommended.

**No subsequent phase is authorized by Phase 3x.** The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v / Phase 3w). **Recommended state remains paused.**

---

## 2. Authority and boundary

Phase 3x operates strictly inside the post-Phase-3w boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11 (Phase 4 / 4a prohibition list and candidate-scope outline); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance). Nothing is revised.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged. Phase 3x explicitly does NOT authorize Phase 4 (canonical), Phase 4a execution, paper/shadow, tiny live, scaled live, or any other gate.
- **Project-level locks preserved verbatim.** §1.7.3 (H0 anchor; BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md` — including stop widening forbidden, exchange-write before approved gate forbidden, production keys during early phases forbidden, blind retry forbidden, restart-in-SAFE_MODE, kill-switch never auto-clears.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md` — no production secrets, no MCP enabling without operator review, no Binance production account / exchange-write MCP, no `.mcp.json` modifications by Phase 3x.
- **Four governance label schemes binding prospectively.** Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3. `mixed_or_unknown` invalid and fails closed at any decision boundary for all four schemes.

Phase 3x adds *forward-looking scoping language* — a written specification of what Phase 4a execution would entail if ever authorized — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate.

---

## 3. Starting state

```text
branch:           phase-3x/phase-4a-safe-slice-scoping
parent commit:    75e5029b11620d9540106137c7449b20df1aedc1 (post-Phase-3w-merge housekeeping)
working tree:     clean
main:             75e5029b11620d9540106137c7449b20df1aedc1 (unchanged)

ambiguity log:    All four Phase 3u §8.5 currently-OPEN pre-coding blockers RESOLVED at
                  governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033
                  by Phase 3w). Pre-tiny-live ACCEPTED_LIMITATION / DEFERRED items remain
                  documented but are not pre-coding blockers per Phase 3u §8.2 / §8.3.
phase-gate state: Phase 4 (canonical) unauthorized; Phase 4a execution unauthorized.
research thread:  5m research thread operationally complete and closed (Phase 3t).
v002 datasets:    locked; manifests untouched.
v001-of-5m:       trade-price research-eligible; mark-price research_eligible:false; manifests untouched.
governance:       Four governance label schemes binding prospectively
                  (stop_trigger_domain | break_even_rule | ema_slope_method | stagnation_window_role).
                  mixed_or_unknown invalid and fails closed for all four schemes.
locks:            §11.6 = 8 bps HIGH per side; §1.7.3 mark-price stops; all preserved.
```

No code under `src/prometheus/` modified by Phase 3x. No script modified. No `data/` artefact modified. No prior-phase report modified. No strategy spec / threshold / project-lock / prior verdict modified. No `data/manifests/*.manifest.json` modified.

---

## 4. Why this memo exists

Phase 3x exists for **four** reasons:

### 4.1 Phase 3u §16.3 conditional tertiary alternative; Phase 3w §17.2 conditional secondary alternative

Phase 3u recommended Option A (remain paused) as primary, Option B (docs-only ambiguity-resolution memo) as conditional secondary, and Option C (docs-only Phase 4a safe-slice scoping memo) as conditional tertiary. Phase 3v resolved GAP-20260424-032 (the Option B priority-one item). Phase 3w resolved GAP-20260424-030 / 031 / 033 (the remaining Option B items). Once all four pre-coding governance blockers are RESOLVED, Phase 3w §17.2 noted that "Option B (Phase 4a safe-slice scoping memo) becomes more procedurally well-grounded after Phase 3w."

The operator authorization for Phase 3x is the natural execution of that conditional alternative now that the governance preconditions Phase 3u flagged are resolved.

### 4.2 Concrete specification before any execution authorization

A scoping memo exists *before* an execution memo so that the operator's eventual decision (whether to authorize Phase 4a execution) is informed by a precise written specification of what would be built, what would be excluded, what governance labels would be enforced, what tests would be written, what evidence would be produced, and what risks would be borne.

Without a scoping memo, an execution authorization would either (a) leave too many decisions to coding-time interpretation (drift risk), or (b) be impossibly broad to authorize in one step. Splitting scope (this memo) from execution (a separate authorization, if ever issued) is the correct discipline.

### 4.3 Anti-live-readiness fortification

Phase 3u §10 / §12.1 identified "live-readiness rhetoric drift" as a real risk: the phrase "Phase 4" carries implicit "we're getting closer to live" connotation even when the actual scope is strategy-agnostic infrastructure. Phase 3x writes the anti-live-readiness disclaimers into the project record with the same procedural weight as the Phase 3v §8 and Phase 3w §6 / §7 / §8 governance rules — making them binding on any future Phase 4a execution brief, not merely aspirational.

### 4.4 Governance label code-enforcement scoping

The four governance label schemes from Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3 are currently policy text. They are not yet enforced in code because no runtime code currently exists that touches stop-trigger logic, break-even logic, EMA-bias logic, or stagnation logic at the runtime layer. If Phase 4a is ever authorized for execution, the four schemes become enforceable in code — but the *form* of that enforcement (where the labels live in the persistence schema, the event-contract layer, the risk-engine validation layer, the dashboard layer) needs to be scoped before it can be implemented. Phase 3x specifies that form.

---

## 5. What Phase 4a would be

If Phase 4a execution is ever authorized (and Phase 3x does NOT authorize it), Phase 4a would be a **strict subset of canonical Phase 4** that builds strategy-agnostic runtime infrastructure with no live-readiness implication and no exchange-write capability.

### 5.1 Strict subset framing

Per `docs/12-roadmap/phase-gates.md` §Phase 4, canonical Phase 4 builds:

- risk sizing engine; exposure gate engine; stop validation; daily loss state; drawdown state; runtime state model; internal event/message contracts; runtime database schema; migrations; audit/runtime event storage; restart-critical persistence; safe-mode startup.

Phase 4a is *not* "Phase 4 with smaller scope." Phase 4a is "the parts of Phase 4 that any future strategy would need, *built without committing to any specific strategy* and *without exchange-write capability*." The framing distinction matters — see §6.

### 5.2 Strategy-agnostic infrastructure

Phase 4a would build the runtime infrastructure that *any* future authorized strategy would flow through. This includes:

- a runtime state machine that can represent SAFE_MODE / RUNNING / BLOCKED / EMERGENCY / RECOVERY_REQUIRED states (per `docs/08-architecture/state-model.md`);
- runtime control state persistence (per `docs/08-architecture/runtime-persistence-spec.md`);
- internal event contracts (per `docs/08-architecture/internal-event-contracts.md`);
- risk sizing and exposure gate skeletons (per `docs/07-risk/position-sizing-framework.md` and `docs/07-risk/exposure-limits.md`);
- stop-validation skeleton (per `docs/07-risk/stop-loss-policy.md`);
- governance label plumbing (per Phase 3v §8 + Phase 3w §6 / §7 / §8);
- a fake-exchange adapter (per `docs/06-execution-exchange/exchange-adapter-design.md` for the adapter boundary; no real Binance code);
- a read-only operator state view (per `docs/11-interface/operator-dashboard-requirements.md`, restricted to read-only for Phase 4a);
- a test harness covering fail-closed behavior, restart safety, kill-switch persistence, label validation, and fake-exchange lifecycle.

Phase 4a would *not* implement any strategy logic, any backtest engine, any real exchange code, any user-stream code, any WebSocket code, any authenticated REST code, any production credential handling, any paper/shadow runtime, any deployment artifact, or any code that could place a real order.

### 5.3 Local-only, fake-exchange, dry-run, exchange-write-free

Phase 4a would be strictly:

- **Local-only.** All Phase 4a code runs on the operator's local development machine (or a future NUC / mini PC, per `docs/09-operations/first-run-setup-checklist.md`, but Phase 4a would not require NUC deployment). No remote services. No cloud. No production environment.
- **Fake-exchange only.** All Phase 4a interactions with the "exchange" go through a deterministic local fake adapter. The fake adapter accepts simulated orders, simulates fills, simulates protective-stop placement, simulates user-stream events. No real Binance code is invoked.
- **Dry-run only.** All Phase 4a execution is dry-run. No real-capital orders. No real-capital exposure. No paper/shadow. No tiny live.
- **Exchange-write-free.** Phase 4a code paths must categorically exclude live order placement, live order cancellation, live position mutation, live account state mutation. The architectural prohibition is not "configuration disables exchange-write" but "the live exchange adapter is simply not implemented; only the fake adapter exists in code." This is a code-structure prohibition, not a runtime configuration.

### 5.4 Strategy-commitment-free

Phase 4a would *not* commit the project to any specific strategy. The runtime infrastructure must accept any future authorized strategy — V1, F1, D1-A, or any new family — without privileging one over another. The runtime must not encode strategy-specific logic that would prefer V1 over F1 or vice versa.

This is important because the project's empirical reality is that no strategy has passed framework gate evaluation in a way that justifies live exposure. R3 is V1 breakout baseline-of-record but is aggregate-negative. R2 / F1 / D1-A are terminal under current locked spec. Building runtime infrastructure for "no specific strategy" is the only honest framing; building it for "the eventual strategy we will authorize later" creates rhetorical pressure to authorize a strategy by the time the runtime is ready, which is exactly the failure mode Phase 3u §12.2 identified.

### 5.5 Anti-live-readiness framing

Phase 4a's success would *not* by itself justify any subsequent phase. Per Phase 3u §11.4 (preserved verbatim by Phase 3x):

> If Phase 4a were ever to complete successfully, the success criterion would be: *"The project has a working strategy-agnostic runtime that can represent SAFE_MODE / BLOCKED / RUNNING / EMERGENCY states, persist runtime control state across restart, fail closed on unknown state, drive a fake-exchange dry-run end-to-end, and surface state via a read-only dashboard — without ever placing a real order or holding a real-capital position."*
>
> This success would *not* by itself justify any subsequent phase. Paper/shadow (Phase 7), tiny-live (Phase 8), scaled live (Phase 9) would each require separate operator authorization with their own evidence.

Phase 4a is therefore a *bounded* infrastructure phase, not a *staging* phase for live readiness. The operator's eventual decision to authorize paper/shadow or live work, if ever made, would not be implied by Phase 4a success.

---

## 6. What Phase 4a must not be

Phase 4a, if ever authorized, must NOT be (these are binding prohibitions, not aspirational language):

### 6.1 No live exchange-write capability

Phase 4a must NOT place orders on Binance or any other exchange. Phase 4a must NOT cancel orders. Phase 4a must NOT modify position state on the exchange. Phase 4a must NOT touch any authenticated REST endpoint. Phase 4a must NOT subscribe to any user stream or any private WebSocket channel.

The architectural enforcement: Phase 4a code does not contain a live exchange adapter. Only the fake adapter exists in code. There is no configuration switch that "turns on" live exchange-write. The capability is absent by code structure.

### 6.2 No production Binance keys

Phase 4a must NOT request, store, configure, or use production Binance trade-capable API keys. Phase 4a must NOT store any real credential of any kind. Phase 4a must NOT introduce a `.env` file with real secrets. Phase 4a must NOT modify `.gitignore` in a way that would silently un-ignore credential files.

Per `phase-gates.md`, production trade-capable Binance keys must not be created until the appropriate phase gate (Phase 8 territory). Phase 4a is not that gate.

### 6.3 No authenticated APIs / private endpoints / user stream / WebSocket

Phase 4a code paths must not include any calls to Binance's authenticated REST endpoints (account-state queries, order placement, order cancellation, listenKey acquisition, account-info). Phase 4a code paths must not include any WebSocket subscriptions. Phase 4a code paths must not include any user-stream lifecycle code. Public-endpoint code (such as bulk-archive download from `data.binance.vision`) is permissible only if explicitly required for Phase 4a's stated infrastructure scope; Phase 4a does not require new public-endpoint code, since data acquisition is out of scope (see §10).

### 6.4 No paper/shadow

Phase 4a must NOT run paper/shadow operations. Per `phase-gates.md` Phase 7 is paper/shadow; Phase 4a is not Phase 7 and does not authorize Phase 7. Phase 4a must NOT log into paper-trading endpoints. Phase 4a must NOT consume real market data in any operational sense (research data already exists at v002 and Phase 3q v001-of-5m; Phase 4a does not need new market data).

### 6.5 No live-readiness implication

Phase 4a's existence, completion, success, or output must NOT be cited as live-readiness evidence anywhere — in commit messages, PR descriptions, code comments, doc text, dashboard text, or operator-facing reports. Per Phase 3u §12.5: every Phase 4a-related artefact must include a "no live-readiness, no exchange-write, no strategy commitment" disclaimer.

### 6.6 No deployment

Phase 4a must NOT produce a deployment artefact. Phase 4a must NOT run as a long-lived service. Phase 4a must NOT be installed on a NUC for live operation. Phase 4a may run on an NUC for testing purposes, but must not be configured for live capability.

### 6.7 No strategy commitment / rescue / new candidate

Phase 4a must NOT commit the project to any strategy. Phase 4a must NOT re-classify any retained-evidence verdict (R3 baseline-of-record; R2 FAILED; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; H0 framework anchor; R1a / R1b-narrow retained research evidence only — all preserved verbatim). Phase 4a must NOT propose a strategy successor (no D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, 5m-on-X variant). Phase 4a must NOT propose a fresh-hypothesis candidate.

Phase 4a's exposure to strategy specifications is read-only: the runtime infrastructure must be able to *accept* any future authorized strategy specification, but must not *propose* or *modify* one.

### 6.8 No verdict revision

Phase 4a must NOT revise R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A verdicts. Phase 4a must NOT re-run Phase 2 / Phase 3 backtests. Phase 4a must NOT re-run Phase 3s Q1–Q7 diagnostics. Phase 4a must NOT regenerate retained-evidence trade populations.

### 6.9 No lock change

Phase 4a must NOT change §1.7.3, §10.3 / §10.4 / §11.3 / §11.4 / §11.6. Phase 4a must NOT modify the mark-price-stop lock. Phase 4a must NOT modify v002 datasets / manifests. Phase 4a must NOT modify Phase 3q v001-of-5m manifests. Phase 4a must NOT modify Phase 3v §8 stop-trigger-domain governance. Phase 4a must NOT modify Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance.

### 6.10 No MCP / Graphify / `.mcp.json` / credentials

Phase 4a must NOT enable any new MCP server. Phase 4a must NOT modify `.mcp.json`. Phase 4a must NOT install Graphify or any other repo-graph tool with secret access. Phase 4a must NOT request, store, or configure any credentials of any kind. Phase 4a must NOT introduce code that would later be wired to read credentials.

### 6.11 No data acquisition / patching / regeneration / modification

Phase 4a must NOT download new data. Phase 4a must NOT patch existing data (no forward-fill, no interpolation, no imputation, no replacement, no §4.7 relaxation). Phase 4a must NOT regenerate v002 / v001-of-5m datasets. Phase 4a must NOT create v003. Phase 4a must NOT modify any `data/manifests/*.manifest.json` file.

### 6.12 No regime-first / ML / cost-model-revision work

Phase 4a must NOT begin regime-first formal spec work (preserved as not-recommended-now per Phase 3m + Phase 3t §14.3). Phase 4a must NOT begin ML feasibility work (preserved as not-authorized per Phase 3k / 3m / 3n / 3o). Phase 4a must NOT begin formal cost-model revision (preserved per Phase 3l).

These prohibitions are exhaustive within Phase 3x's evaluation scope. Any future Phase 4a execution brief must reaffirm these prohibitions verbatim before any code is written.

---

## 7. Preconditions satisfied

The following preconditions for considering Phase 4a execution are SATISFIED at the post-Phase-3w boundary:

### 7.1 Documentation maturity

Per `current-project-state.md` "Completed / Substantially Defined Documentation" and Phase 3u §7.1, the project has substantially complete documentation across all 11 documentation areas:

- Meta + Setup + Handoff (5 docs).
- Strategy and Research (3 docs + Phase 2 / Phase 3 implementation reports).
- Data Layer (5 docs).
- Backtesting and Validation (1 doc + framework checklist).
- Execution and Exchange (6 docs).
- Risk (6 docs).
- Runtime Architecture (9 docs).
- Operations (7 docs).
- Security (6 docs).
- Operator Interface (5 docs).
- Roadmap / Governance (2 docs).

This documentation is sufficient to ground a Phase 4a execution brief.

### 7.2 Pre-coding governance blockers resolved

All four Phase 3u §8.5 currently-OPEN pre-coding governance blockers are RESOLVED at the governance level:

- **GAP-20260424-032** (Backtest uses trade-price stops; live uses MARK_PRICE stops) — RESOLVED by Phase 3v governance memo. `stop_trigger_domain` label scheme binding prospectively.
- **GAP-20260424-030** (Break-even rule conflict) — RESOLVED by Phase 3w governance memo. `break_even_rule` label scheme binding prospectively.
- **GAP-20260424-031** (EMA slope wording) — RESOLVED by Phase 3w governance memo. `ema_slope_method` label scheme binding prospectively.
- **GAP-20260424-033** (Stagnation window) — RESOLVED by Phase 3w governance memo. `stagnation_window_role` label scheme binding prospectively.

These were the procedural blockers Phase 3u flagged. They are resolved.

### 7.3 Phase 1 local-development foundation intact

Per `current-project-state.md` Implementation Readiness Status, Phase 1 (local development foundation) is complete: Python project structure, dependency manager, test runner, lint / format / type-check tooling, configuration loader, logging foundation, basic CLI/runtime entrypoint, fake/no-op runtime foundation. Phase 4a execution would build *on top of* this foundation rather than re-creating it.

### 7.4 Phase 2 historical data foundation intact

Per `current-project-state.md`, Phase 2 (v002 historical-data foundation) is complete: BTCUSDT + ETHUSDT 15m + 1h-derived + 15m mark-price + funding-event datasets are manifested and locked. Phase 3q (v001-of-5m supplemental datasets) is complete with trade-price `research_eligible: true` and mark-price `research_eligible: false`. Phase 4a execution would consume these existing datasets read-only (or, more accurately, would not consume them at all because data work is out of scope per §6.11; the data foundation simply *exists* and can be referenced if needed).

### 7.5 Architecture / risk / runtime / dashboard / execution / operations / security / interface documentation stable

Per Phase 3u §6.3 + §7.1, the architecture / risk / runtime / dashboard / execution / operations / security / interface documentation is stable and substantially complete. The candidate Phase 4a components in §9 below all derive directly from these existing specifications. No documentation refresh is required as a precondition for Phase 4a *scoping* (this memo); a partial documentation refresh might become useful if Phase 4a *execution* is ever authorized (see §15).

### 7.6 Standalone scripts proven

Per `current-project-state.md`, Phase 3q's standalone orchestrator (`scripts/phase3q_5m_acquisition.py`) and Phase 3s's standalone diagnostics (`scripts/phase3s_5m_diagnostics.py`) are proven on the existing data foundation. This does not directly affect Phase 4a (data work is out of scope) but it confirms that the project's coding capability for non-trivial standalone work exists.

---

## 8. Preconditions still not satisfied

The following preconditions for *executing* Phase 4a (as distinct from *scoping* it) are NOT yet satisfied:

### 8.1 Operator has not authorized Phase 4a execution

Phase 3x is a scoping memo only. Phase 3x explicitly does NOT authorize Phase 4a execution. Authorizing Phase 4a execution would require a separate operator decision after Phase 3x is reviewed. Specifically, the operator authorization brief for Phase 4a execution would need to:

- explicitly reaffirm the §6 prohibition list verbatim;
- explicitly state that authorizing execution does not commit the project to live readiness;
- explicitly state that Phase 4a success does not authorize paper/shadow, tiny live, or any subsequent phase;
- explicitly authorize the execution scope (one or more of the §9 candidate components, or all of them, or a stricter subset);
- explicitly authorize the test scope per §14;
- explicitly authorize the documentation update scope per §15;
- explicitly state that pre-tiny-live items (`ACCEPTED_LIMITATION` / `DEFERRED` per the ambiguity log and the technical-debt register) remain pre-tiny-live concerns and are not Phase 4a blockers.

No such authorization has been issued.

### 8.2 Operator has not committed to deprioritizing research

Phase 3u §12.6 + §13.7 + §16.3 + §16.6 noted that Phase 4a should be authorized only if the operator has consciously decided to deprioritize research for a defined period. The reasoning: building runtime infrastructure naturally moves attention from research to implementation; without a clear research direction (which the project does not currently have given the V1 / F1 / D1-A terminal verdicts and the Phase 3t research-thread closure), authorizing Phase 4a now could mean implementation work continues indefinitely while research stalls.

The operator has not signaled an intent to deprioritize research. Phase 3x does not interpret the operator's authorization for Phase 3x (the scoping memo) as a commitment to deprioritize research; the scoping memo is independently useful as documentation and does not require a research-deprioritization commitment.

### 8.3 Phase 3v / 3w label-enforcement design not yet specified at code level

The four governance label schemes from Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3 are currently policy text. Phase 3x §11 below specifies *which artefacts* must carry the labels and *what fail-closed semantics* must be enforced — but does not yet specify the *code-level form* (exact field names, exact validation paths, exact persistence schema columns, exact event-contract field definitions). A Phase 4a execution brief would need to specify those code-level forms before any code is written.

### 8.4 Pre-tiny-live items remain (not pre-coding blockers)

Per Phase 3u §8.2 + Phase 3w §16, the following pre-tiny-live items remain documented but are NOT pre-coding blockers:

- GAP-20260419-018 — Taker commission rate parameterization (`ACCEPTED_LIMITATION`).
- GAP-20260419-020 — ExchangeInfo snapshot proxy (`ACCEPTED_LIMITATION`).
- GAP-20260419-024 — leverageBracket placeholder (`ACCEPTED_LIMITATION`).
- GAP-20260419-025 — Wider historical backfill (`DEFERRED`).
- TD-006 (`docs/12-roadmap/technical-debt-register.md`) — Exact Binance endpoint behavior verification (partially resolved at coding time for bulk klines + mark-price; remains open for REST-write paths and user-stream behavior).
- TD-017 — Public-IP solution for local NUC (pre-tiny-live).
- TD-018 — First live notional cap value (pre-tiny-live).
- TD-019 — Production alert route selection (pre-tiny-live).
- TD-020 — Backup schedule and retention (pre-tiny-live).

These items are pre-tiny-live concerns. Phase 4a's strict subset framing (§5.1 / §5.3) ensures these items are NOT in scope: Phase 4a does not touch live exchange capability, production keys, NUC deployment for live operation, alert routing for production, backup for production, or any other pre-tiny-live concern. The pre-tiny-live items remain pre-tiny-live; they would be addressed by a separately authorized pre-tiny-live readiness phase if and when paper/shadow / Phase 7 / Phase 8 work is ever authorized.

The fact that pre-tiny-live items remain unresolved is **not** a blocker for Phase 4a, because Phase 4a's scope explicitly excludes anything that would require those items to be resolved.

---

## 9. Safe-slice candidate scope

This section evaluates ten candidate Phase 4a components against the §6 prohibition list. Each candidate is described, scoped, and tested against the §6 / §7 / §8 boundaries. Phase 3x does NOT authorize any of these components; it only specifies what they would entail if Phase 4a execution were authorized.

### 9.1 Runtime mode / state model

**Component:** In-process state machine implementing the runtime modes from `docs/08-architecture/state-model.md` Top-Level Runtime Modes section.

**Specification:** valid states `SAFE_MODE`, `RUNNING_HEALTHY` (or `RUNNING` for Phase 4a's strategy-agnostic framing — the runtime can be "running" without any live trading because no strategy is wired in), `BLOCKED_AWAITING_OPERATOR`, `RECOVERING`, `EMERGENCY`, `RECOVERY_REQUIRED`. Transitions follow the rules in `state-model.md` §Runtime Mode Rules and §Recommended Transition Rules.

**Required behavior:**
- Startup defaults to `SAFE_MODE` per `state-model.md` §Startup rule and `.claude/rules/prometheus-safety.md`.
- Unknown state must fail closed (block trade / block verdict / block persist / block evidence-promotion).
- State transitions must be driven by explicit event classes (per `internal-event-contracts.md`); no hidden cross-module mutation.

**Out of scope:** Phase 4a does NOT implement strategy-driven state transitions (because no strategy is wired in). Phase 4a does NOT implement live-exchange-driven state transitions (because no live exchange code exists). The state machine accepts events from the test harness (§9.10) and from internal control commands (§9.4). Real-world strategy or exchange integration would be a *future* phase, not Phase 4a.

**Phase 4a appropriateness:** APPROPRIATE. This is the foundation of the runtime; it is strategy-agnostic; it does not require exchange-write capability. The §6 prohibitions are preserved.

### 9.2 Runtime control state persistence

**Component:** SQLite (or local equivalent) persistence layer for restart-critical runtime control state, per `docs/08-architecture/runtime-persistence-spec.md` and `docs/08-architecture/database-design.md`.

**Specification:** A local SQLite database (path `runtime/runtime.db` or equivalent per the runtime-persistence spec) with WAL journal mode, foreign-keys on, busy-timeout configured. Tables for: runtime control state (current mode, kill-switch state, pause state, operator-review-required flag, entries-blocked flag); incident records; reconciliation records; operator action audit; runtime events; exchange events (placeholder schema; no real exchange events written by Phase 4a because no live exchange code exists). Migrations.

**Required behavior:**
- Startup loads persisted state and enters `SAFE_MODE` regardless of last persisted mode.
- Kill-switch state persists across restart (per `kill-switches.md` §6 and §Persistence Requirements).
- Kill switch never auto-clears.
- Operator review required state persists across restart.
- Unknown execution outcome state persists across restart.
- Persistence must be durable for restart-critical transitions (per `internal-event-contracts.md` §Durable-Write and Persistence Trigger Rules).

**Out of scope:** Phase 4a does NOT persist live trade lifecycle records (because no live trades occur). Phase 4a does NOT persist real exchange events (only fake-adapter-emitted simulated events for test purposes). Phase 4a does NOT persist secrets, credentials, or any sensitive data. Phase 4a does NOT introduce a remote database or any distributed persistence.

**Phase 4a appropriateness:** APPROPRIATE. The persistence layer is part of the runtime safety foundation; SQLite + local files are the minimum viable persistence; the schema can accept future strategy / exchange integration without re-design. The §6 prohibitions are preserved (no exchange-write because no exchange code exists; no production credentials because no credentials are stored).

### 9.3 Internal event contracts

**Component:** Typed local event-bus and message-envelope implementation per `docs/08-architecture/internal-event-contracts.md`.

**Specification:** In-process event bus implementing the message envelope (`message_type`, `message_class`, `message_id`, `correlation_id`, `causation_id`, `occurred_at_utc_ms`, `source_component`, `symbol`, `strategy_id`, `payload`). Command / event / query semantic distinction. Module ownership rules (per §Component Ownership and Allowed Emissions). Durable-write trigger rules for runtime / control / lifecycle / protection / reconciliation / operator-action / incident events.

**Required behavior:**
- Commands and events are semantically distinct (commands are intentions; events are confirmed facts).
- Module ownership rules are enforced (e.g., the strategy engine emits no exchange-truth events; the operator control layer emits no exchange-truth events).
- Persistence-critical messages (per `internal-event-contracts.md` §Durable-Write and Persistence Trigger Rules) trigger durable persistence before the runtime proceeds.
- Event schema carries required governance labels per §11 below where relevant.

**Out of scope:** Phase 4a does NOT implement exchange-write events (only fake-adapter-emitted simulated equivalents for test purposes). Phase 4a does NOT implement authenticated-exchange events (no live user stream, no live REST). Phase 4a does NOT implement strategy-signal events for any live strategy (no strategy is wired in).

**Phase 4a appropriateness:** APPROPRIATE. Internal event contracts are foundational; they define the wiring that all later strategy / exchange / dashboard work would use; they do not require live capability. The §6 prohibitions are preserved.

### 9.4 Risk sizing skeleton

**Component:** Risk-engine implementation per `docs/07-risk/position-sizing-framework.md`, restricted to local calculation only.

**Specification:** Functions / classes implementing the risk-sizing computation: stop-distance-based sizing; equity reference; risk fraction (default 0.25% per §1.7.3); leverage cap (default 2× per §1.7.3); internal notional cap (placeholder; the actual value remains pre-tiny-live per TD-018). Inputs: strategy-decision proxies (test fixtures, not real strategy output); equity reference (test fixture); stop distance; symbol metadata (placeholder; the leverageBracket / ExchangeInfo proxies remain pre-tiny-live per TD-020 / TD-024). Outputs: approved or rejected sizing decision with explicit rejection reason.

**Required behavior:**
- Fail closed on missing metadata.
- Fail closed on missing equity reference.
- Below-minimum quantity rejects.
- Notional cap rejects when exceeded.
- Leverage cap rejects when exceeded.
- Locked constants (0.25% risk, 2× leverage cap) referenced as configuration with explicit defaults; any deviation is a configuration change, not a code-level decision.

**Out of scope:** Phase 4a does NOT place orders. Phase 4a does NOT make live notional decisions (no real account equity is consulted). Phase 4a does NOT optimize sizing parameters (no parameter tuning). Phase 4a does NOT propose new risk thresholds (project-level locks preserved).

**Phase 4a appropriateness:** APPROPRIATE. Risk sizing is a local calculation; it does not require live capability. The §6 prohibitions are preserved (no exchange-write; no production credentials; no live notional).

### 9.5 Exposure gate skeleton

**Component:** Exposure-limit gate implementation per `docs/07-risk/exposure-limits.md`, restricted to fake-position state only.

**Specification:** Functions / classes implementing the exposure gates: one-symbol-only live lock (per §1.7.3 BTCUSDT only); one-position-maximum gate (per §1.7.3); no-pyramiding guardrail; no-reversal-while-positioned guardrail; manual-exposure-block guardrail. Inputs: fake-position state (from the §9.8 fake-exchange adapter); proposed entry candidate (from the §9.10 test harness). Outputs: allow or block decision with explicit reason.

**Required behavior:**
- Multiple positions block.
- Pyramiding (same-symbol same-side scale-in) blocks.
- Reversal (same-symbol opposite-side entry while positioned) blocks.
- Manual / non-bot exposure detection (when the fake-adapter simulates external order placement) blocks new bot entries.
- Symbol other than the configured live symbol blocks.

**Out of scope:** Phase 4a does NOT manage real positions. Phase 4a does NOT detect real manual exposure. Phase 4a does NOT cancel real orders. Phase 4a does NOT authorize multi-symbol live or hedge-mode behavior (preserved per §1.7.3).

**Phase 4a appropriateness:** APPROPRIATE. Exposure gates are local checks against simulated state; they do not require live capability. The §6 prohibitions are preserved.

### 9.6 Stop-validation skeleton

**Component:** Stop-validation implementation per `docs/07-risk/stop-loss-policy.md`, with mandatory enforcement of the Phase 3v `stop_trigger_domain` governance.

**Specification:** Functions / classes implementing the stop validation: long-stop-below-entry / short-stop-above-entry side check; positive stop-distance check; ATR filter `0.60 * ATR <= stop_distance <= 1.80 * ATR`; metadata validation (price precision, tick size, trigger order support, `MARK_PRICE` working type support, `priceProtect` support); stop-direction-of-update check (cannot widen risk); `stop_trigger_domain` label validation (per §11 below).

**Required behavior:**
- Reject stops that violate the side check.
- Reject stops that violate the distance check.
- Reject stops that violate the ATR filter.
- Reject stops with missing or stale metadata.
- Reject stop-update intents that would widen risk.
- Reject stops with `stop_trigger_domain = mixed_or_unknown` (fail closed).
- For any future live / paper / runtime path, require `stop_trigger_domain = mark_price_runtime` per Phase 3v §8.3.
- For any future research backtest path, require `stop_trigger_domain = trade_price_backtest` or `mark_price_backtest_candidate` per Phase 3v §8.4.

**Out of scope:** Phase 4a does NOT place stops on a real exchange. Phase 4a does NOT cancel real stops. Phase 4a does NOT widen stops (per §1.7.3 + `stop-loss-policy.md` Core Principle 7). Phase 4a does NOT propose mark-price-stop sensitivity backtests on retained-evidence populations (preserved as not-recommended-now per Phase 3v §17.4).

**Phase 4a appropriateness:** APPROPRIATE. Stop validation is a local check; it does not require live capability. The Phase 3v §8 stop-trigger-domain governance becomes enforceable in code at this layer. The §6 prohibitions are preserved.

### 9.7 Break-even / EMA / stagnation governance label plumbing

**Component:** Code-level enforcement of Phase 3w §6.3 / §7.3 / §8.3 governance label schemes — `break_even_rule`, `ema_slope_method`, `stagnation_window_role` — across persistence, event contracts, and validation paths.

**Specification:** First-class fields in the runtime control persistence schema, the internal event contract schema (where relevant), and the validation interfaces. Valid values per Phase 3w. `mixed_or_unknown` invalid and fails closed. The label values are *configured* (not hardcoded by strategy) so that any future authorized strategy specification can declare its own value set.

**Required behavior:**
- Persistence schema includes `break_even_rule`, `ema_slope_method`, `stagnation_window_role` columns (or equivalent NoSQL fields if SQLite is chosen and these go on a configuration table).
- Event-contract messages that touch break-even / EMA / stagnation logic carry the appropriate label.
- Validation paths reject `mixed_or_unknown` (block trade / block verdict / block persist).
- The label values are *recorded*, not *applied*: Phase 4a does not implement break-even or stagnation rule logic (because no strategy is wired in). Phase 4a only enforces that *if* a future strategy specifies one of these schemes, the label must be valid.

**Out of scope:** Phase 4a does NOT implement break-even rule behavior (no Stage-4 stop transition logic). Phase 4a does NOT implement EMA slope behavior (no 1h-bias-bar comparison logic). Phase 4a does NOT implement stagnation rule behavior (no 8-bar / +1.0R stagnation exit logic). Phase 4a does NOT propose H-D3 / H-C2 / H-D5 sensitivity analyses (preserved per Phase 3w §17.3).

**Phase 4a appropriateness:** APPROPRIATE. Label plumbing is a code-level governance enforcement; it does not require any strategy logic to exist (because the labels are declarative, not behavioral). The Phase 3w §6 / §7 / §8 governance becomes enforceable in code at this layer. The §6 prohibitions are preserved.

### 9.8 Fake-exchange adapter

**Component:** Local deterministic fake-exchange adapter per `docs/06-execution-exchange/exchange-adapter-design.md` adapter boundary, with no Binance credentials, no private endpoints, no WebSocket, no real order placement.

**Specification:** A Python class implementing the adapter interface defined in `exchange-adapter-design.md`, but backed entirely by an in-memory simulated state machine. Methods: `submit_entry_order`, `submit_protective_stop`, `replace_protective_stop`, `submit_exit_order`, `query_position`, `query_open_orders`, `query_open_algo_orders`. All methods operate on simulated state. The adapter emits simulated user-stream events into the §9.3 event bus.

**Required behavior:**
- All methods are deterministic given the test fixture inputs.
- No HTTP requests to Binance.
- No WebSocket connections.
- No credential reads.
- No `.env` file reads (other than test fixtures explicitly configured for the fake adapter).
- Fake-fill simulation respects the lifecycle in `state-model.md` §Trade Lifecycle State Model.
- Fake protective-stop simulation respects the lifecycle in `stop-loss-policy.md` §Protective Stop Timing.
- Fake user-stream events tagged with appropriate `stop_trigger_domain` labels (per Phase 3v §8.4) — e.g., a fake stop-trigger event in a runtime context carries `stop_trigger_domain = mark_price_runtime` (because the fake adapter is simulating runtime, not backtest).

**Out of scope:** Phase 4a does NOT implement a real Binance adapter. Phase 4a does NOT implement authenticated REST. Phase 4a does NOT implement WebSocket subscriptions. Phase 4a does NOT implement listenKey acquisition / refresh. Phase 4a does NOT implement any code that could be repointed at production Binance via configuration alone.

**Phase 4a appropriateness:** APPROPRIATE. The fake adapter is foundational for end-to-end runtime testing without exchange-write capability; it does not require any live capability. The §6 prohibitions are preserved by construction (no real Binance code exists).

### 9.9 Read-only operator state view

**Component:** Local read-only operator state surface (text or simple HTTP/WebUI) per `docs/11-interface/operator-dashboard-requirements.md`, restricted to read-only.

**Specification:** A local read model that exposes runtime control state, fake-position state, fake-order state, fake-protective-stop state, kill-switch state, pause state, operator-review-required state, incident state, recent runtime events. Implementation may be a CLI command, a simple HTTP endpoint, or a minimal web UI — whichever is least complex to build given the runtime infrastructure.

**Required behavior:**
- Read-only. No buttons or controls that would imply live execution.
- No exchange actions exposed.
- No production alerting (Telegram / n8n alerts are pre-tiny-live per TD-019; Phase 4a does not implement them).
- Secrets must not leak into the view.
- Display includes the four governance labels per §11 below where applicable.

**Out of scope:** Phase 4a does NOT implement operator control buttons that could place orders, cancel orders, widen stops, or change risk. Phase 4a does NOT implement Telegram / n8n alert routing for production purposes. Phase 4a does NOT implement TradingView-like chart rendering (per `current-project-state.md` Forbidden in v1: no click-to-trade, no chart trading).

**Phase 4a appropriateness:** APPROPRIATE if the read-only constraint is enforced by code structure (no controls exist; the surface only renders state). The §6 prohibitions are preserved.

### 9.10 Test harness

**Component:** Comprehensive test suite for §9.1 through §9.9, including unit tests, integration tests, and end-to-end fake-runtime tests.

**Specification:** Tests covering:
- Fail-closed behavior on unknown state, missing metadata, ambiguous label values.
- Restart safety: kill-switch state persists across simulated restart; operator-review-required state persists; reconciliation-required state persists.
- Kill-switch persistence: kill switch never auto-clears; kill switch survives simulated restart; kill switch blocks new entries.
- Label validation: each of the four governance labels rejects `mixed_or_unknown`; each label rejects values outside its scheme.
- Fake-exchange lifecycle: entry submission → fake fill → fake position confirmed → fake protective stop submitted → fake stop confirmed → fake position protected; failure-injection paths (submission timeout / unknown outcome → fail closed; missing protection → emergency unprotected branch).

**Required behavior:**
- All tests are local; no network access required for any test.
- All tests are deterministic; no flakiness tolerance.
- Tests run as part of the existing pytest harness (per Phase 1 local-development foundation).

**Out of scope:** Phase 4a does NOT include live integration tests against Binance (no live integration). Phase 4a does NOT include paper/shadow tests (no paper/shadow). Phase 4a does NOT include performance / load / chaos tests at production scale (those are pre-tiny-live concerns).

**Phase 4a appropriateness:** APPROPRIATE. Test harness is a code-level discipline; it does not require any live capability. The §6 prohibitions are preserved.

### 9.11 Component-scope summary

All ten candidate components are appropriate for a future Phase 4a execution scope under the §6 prohibition list. Each component is local-only, fake-exchange or fake-state-only, dry-run, exchange-write-free, strategy-agnostic, and lock-preserving. The components form a coherent strategy-agnostic runtime infrastructure that any future authorized strategy would flow through.

A future Phase 4a execution brief would explicitly authorize one or more of these components (or all of them, or a stricter subset). Phase 3x does NOT authorize any of them.

---

## 10. Explicitly out-of-scope work

The following work is categorically OUT OF SCOPE for any future Phase 4a execution. This list complements the §6 prohibition list and is binding:

### 10.1 No strategy implementation

Phase 4a does NOT implement V1 breakout strategy logic. Phase 4a does NOT implement F1 mean-reversion strategy logic. Phase 4a does NOT implement D1-A funding-aware strategy logic. Phase 4a does NOT implement any strategy. The runtime infrastructure must accept any future authorized strategy specification, but Phase 4a does not contain a strategy.

### 10.2 No backtest engine

Phase 4a does NOT implement a backtest engine. Phase 4a does NOT re-run Phase 2 / Phase 3 backtests. Phase 4a does NOT implement walk-forward / cross-validation / out-of-sample / holdout-evaluation frameworks. Phase 4a does NOT propose H-D3 / H-C2 / H-D5 sensitivity backtests. Phase 4a does NOT propose mark-price-stop sensitivity backtests.

### 10.3 No live exchange code

Phase 4a does NOT implement a real Binance adapter. Phase 4a does NOT implement authenticated REST. Phase 4a does NOT implement WebSocket subscriptions. Phase 4a does NOT implement user-stream code. Phase 4a does NOT implement listenKey lifecycle. Phase 4a does NOT implement order signing.

### 10.4 No production credentials / MCP / Graphify / `.mcp.json`

Phase 4a does NOT request, store, configure, or use production credentials of any kind. Phase 4a does NOT enable any new MCP server. Phase 4a does NOT modify `.mcp.json`. Phase 4a does NOT install Graphify or any other repo-graph tool with secret access.

### 10.5 No deployment / NUC live setup / Telegram / n8n / production alerting

Phase 4a does NOT produce a deployment artefact for live operation. Phase 4a does NOT install on NUC for live operation. Phase 4a does NOT configure Telegram alerts for production. Phase 4a does NOT configure n8n for production. These are all pre-tiny-live concerns per Phase 3u §8 + TD-017 / TD-018 / TD-019 / TD-020.

### 10.6 No paper / shadow / tiny-live / scaled-live

Phase 4a does NOT run paper/shadow. Phase 4a does NOT run tiny-live. Phase 4a does NOT run scaled-live. Per `phase-gates.md`, these are Phase 7 / 8 / 9 territory; Phase 4a is Phase 4-territory subset, not Phase 7+.

### 10.7 No data acquisition / patching / regeneration / modification

Phase 4a does NOT download new data. Phase 4a does NOT patch existing data. Phase 4a does NOT regenerate v002 / v001-of-5m datasets. Phase 4a does NOT create v003. Phase 4a does NOT modify any `data/manifests/*.manifest.json` file. Phase 4a does NOT consult Binance public endpoints for fresh data (the existing v002 + v001-of-5m datasets are sufficient if any data is needed for testing, and even those are likely not needed because Phase 4a does not implement strategy or backtest logic).

### 10.8 No verdict revision / strategy rescue / new strategy candidate / regime-first / ML / cost-model revision

These are exhaustively prohibited per Phase 3u §10 + Phase 3v §13 + Phase 3w §14. Phase 4a inherits these prohibitions verbatim.

### 10.9 No retroactive modification

Phase 4a does NOT retroactively modify Phase 2 / Phase 3 backtest report manifests. Phase 4a does NOT retroactively modify Phase 3q v001-of-5m manifests. Phase 4a does NOT retroactively modify Phase 3s diagnostic outputs. The four governance label schemes (per Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3) apply *prospectively* per Phase 3v §9 + Phase 3w §9; existing artefacts are treated as having implicit labels for audit purposes only.

---

## 11. Required governance labels

Any future Phase 4a execution must enforce the four governance label schemes from Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3 in code, not only in policy text. The compact form (preserved verbatim from Phase 3w §9):

| Label | Source | Valid values | Fail-closed value |
|---|---|---|---|
| `stop_trigger_domain` | Phase 3v §8.4 | `trade_price_backtest` \| `mark_price_runtime` \| `mark_price_backtest_candidate` | `mixed_or_unknown` |
| `break_even_rule` | Phase 3w §6.3 | `disabled` \| `enabled_plus_1_5R_mfe` \| `enabled_plus_2_0R_mfe` \| `enabled_<other_predeclared>` | `mixed_or_unknown` |
| `ema_slope_method` | Phase 3w §7.3 | `discrete_comparison` \| `fitted_slope` \| `other_predeclared` \| `not_applicable` | `mixed_or_unknown` |
| `stagnation_window_role` | Phase 3w §8.3 | `not_active` \| `metric_only` \| `active_rule_predeclared` | `mixed_or_unknown` |

### 11.1 Where the labels live in Phase 4a code

A future Phase 4a execution must place these labels as first-class fields in:

- **Runtime control persistence schema** (per `docs/08-architecture/runtime-persistence-spec.md` and `docs/08-architecture/database-design.md`). The labels appear on the runtime control state row (or on a dedicated configuration table referenced by the runtime control state row).
- **Internal event contract messages** (per `docs/08-architecture/internal-event-contracts.md`). Messages that touch stop-trigger logic, break-even logic, EMA-bias logic, or stagnation logic carry the appropriate label in the envelope or payload.
- **Risk-engine validation paths** (per `docs/07-risk/stop-loss-policy.md` for `stop_trigger_domain`; per equivalent risk-engine validation for the other three). Validation paths reject `mixed_or_unknown` and reject values outside the scheme.
- **Read-only operator state view** (per `docs/11-interface/operator-dashboard-requirements.md`). The dashboard renders the current label values for operator visibility.
- **Trade-execution decisions** (in Phase 4a context, fake trade-execution decisions only). Decisions cannot proceed with `mixed_or_unknown` labels.

### 11.2 Why these labels are enforceable at the Phase 4a layer

The four governance label schemes were defined as policy text in Phase 3v / Phase 3w. They become *enforceable in code* once a runtime exists that touches the relevant logic. Phase 4a is the first point in the project where such a runtime would exist. Therefore Phase 4a is the natural code-enforcement layer for these labels.

The enforcement is governance, not strategy: Phase 4a does not implement break-even / EMA / stagnation rule behavior (because no strategy is wired in). It only enforces that any future strategy specification *declare* its label values explicitly, and rejects ambiguous declarations.

### 11.3 What Phase 4a does not do with the labels

- Phase 4a does NOT change any label scheme value set.
- Phase 4a does NOT add new label schemes beyond the four.
- Phase 4a does NOT silently retro-modify existing artefacts to add labels.
- Phase 4a does NOT use the labels to revise any retained-evidence verdict.
- Phase 4a does NOT use the labels to authorize strategy rescue.

---

## 12. Fail-closed requirements

Any future Phase 4a execution must implement fail-closed semantics across the following decision boundaries (per Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3):

### 12.1 Fail-closed at the trade-execution boundary

A trade-execution decision under `mixed_or_unknown` (any of the four labels) must block the trade. This applies to fake trades in Phase 4a context (because no real trades exist in Phase 4a).

### 12.2 Fail-closed at the verdict boundary

A verdict decision under `mixed_or_unknown` must block the verdict. In Phase 4a, this applies to any verdict-shaped output the runtime might emit (e.g., a future strategy-readiness gate; in Phase 4a context this is conceptual only because no strategy is wired in).

### 12.3 Fail-closed at the persistence boundary

A persistence write under `mixed_or_unknown` must block the persist. The runtime must not silently store ambiguous label values; the write fails and the operator is notified.

### 12.4 Fail-closed at the evidence-promotion boundary

An evidence-promotion decision under `mixed_or_unknown` must block the promotion. In Phase 4a context this is conceptual (because no evidence is being promoted). The boundary becomes operationally relevant if and when a future research backtest phase consumes Phase 4a's runtime; it must be code-enforceable from Phase 4a forward.

### 12.5 Fail-closed at the unknown state boundary

Per `docs/08-architecture/state-model.md` §State-Model Principles 4: "Normal operation requires state certainty." Per `.claude/rules/prometheus-safety.md`: "Unknown execution outcomes fail closed." Per Phase 4a's strategy-agnostic framing: any state the runtime cannot trust must block normal progression. The runtime must enter `SAFE_MODE` or equivalent emergency-handling on unknown state.

### 12.6 Fail-closed at the missing-metadata boundary

Per `docs/07-risk/stop-loss-policy.md` §Initial Stop Validation: stops with missing metadata reject. Per `docs/07-risk/position-sizing-framework.md`: missing risk state, metadata, or exchange-state confidence fails closed. Phase 4a's risk sizing skeleton (§9.4), exposure gate skeleton (§9.5), and stop-validation skeleton (§9.6) must enforce these prohibitions in code.

### 12.7 Fail-closed at the kill-switch boundary

Per `docs/07-risk/kill-switches.md` §Persistence Requirements: kill-switch state is restart-critical; kill switch never auto-clears. Phase 4a's runtime control state persistence (§9.2) must enforce kill-switch persistence. Phase 4a's runtime mode / state model (§9.1) must enforce kill-switch-blocks-new-entries semantics.

---

## 13. Required implementation evidence if later authorized

If Phase 4a execution is ever authorized (and Phase 3x does NOT authorize it), the resulting implementation phase must produce the following evidence as part of its checkpoint report (per `docs/00-meta/ai-coding-handoff.md` §Runnable Checkpoint Review Protocol):

### 13.1 Code artefacts

- Modified files under `src/prometheus/` covering the in-scope §9 components.
- Migration file(s) for the SQLite runtime database.
- Test files under `tests/` covering the §14 test scope.
- Updated `pyproject.toml` if new development dependencies are introduced (e.g., for the read-only operator state view if it requires a web framework).
- No `.env` / credential / secret files; no MCP config changes; no production-deployment artefacts.

### 13.2 Verification outputs

- `pytest` output showing all tests pass.
- `ruff` / `black` / `mypy` output showing lint / format / type-check pass.
- A runnable demo: a CLI command (or equivalent) that starts the runtime in `SAFE_MODE`, drives a fake-exchange dry-run signal-to-protected-position lifecycle, demonstrates fail-closed on a deliberately ambiguous label, demonstrates kill-switch activation and persistence across simulated restart, and prints the read-only operator state view.

### 13.3 Documentation artefacts

- Phase 4a memo (the equivalent of this Phase 3x memo, for the execution phase).
- Phase 4a closeout report (per the Phase 3o–3w pattern).
- Phase 4a merge closeout (per the Phase 3o–3w pattern).
- Updated `current-project-state.md` recording Phase 4a execution merged.
- Updated `docs/00-meta/implementation-ambiguity-log.md` if any new pre-coding ambiguities are surfaced during Phase 4a execution (Phase 3u §13.2 noted that implementation work surfaces ambiguities documentation alone does not).

### 13.4 Evidence that prohibitions were preserved

- Evidence that no real Binance code was added (e.g., grep for any reference to authenticated REST endpoints, WebSocket URLs, or production credential paths returns zero hits).
- Evidence that no `.mcp.json` was modified.
- Evidence that no `data/manifests/*.manifest.json` was modified.
- Evidence that no v002 / v001-of-5m dataset was modified.
- Evidence that no retained-evidence verdict was revised (Phase 4a does not touch Phase 2 / Phase 3 reports).
- Evidence that no strategy spec / backtest plan / validation checklist substantive content was modified.
- Evidence that the Phase 3v §8 stop-trigger-domain governance and Phase 3w §6 / §7 / §8 governance were not modified.
- Evidence that the §6 prohibition list was reaffirmed verbatim in the Phase 4a authorization brief and that no item in the prohibition list was violated by the implementation.

---

## 14. Required tests if later authorized

If Phase 4a execution is ever authorized, the resulting implementation phase must include tests covering at minimum:

### 14.1 Fail-closed behavior tests

- Each of the four governance labels rejects `mixed_or_unknown`.
- Each of the four governance labels rejects values outside its scheme.
- Risk sizing fails closed on missing metadata.
- Risk sizing fails closed on missing equity reference.
- Stop validation fails closed on missing metadata.
- Stop validation fails closed on stops that violate side / distance / ATR-filter checks.
- Exposure gate fails closed on multiple positions / pyramiding / reversal / non-bot exposure.

### 14.2 Restart safety tests

- Process start enters `SAFE_MODE`.
- Persisted runtime control state loads as provisional (does not assume `RUNNING_HEALTHY`).
- Reconciliation-required state persists across simulated restart.
- Operator-review-required state persists across simulated restart.
- Unknown execution outcome state persists across simulated restart.

### 14.3 Kill-switch persistence tests

- Operator activation sets kill-switch active and persists.
- Automatic safety activation sets kill-switch active and persists (e.g., simulated emergency unprotected condition).
- Restart preserves active kill switch.
- Kill switch never auto-clears.
- Kill-switch active blocks new entries (fake entry attempts in Phase 4a context).
- Kill-switch active blocks normal strategy progression (conceptual in Phase 4a context because no strategy is wired in).
- Kill-switch clearance requires explicit operator action.
- Kill-switch clearance is blocked when reconciliation is required, when fake-position is unprotected, when severe incident is active.

### 14.4 Label validation tests

- Persistence schema rejects writes with `mixed_or_unknown` for any of the four labels.
- Event-contract messages with `mixed_or_unknown` are rejected by validation.
- Risk-engine validation paths reject decisions under `mixed_or_unknown`.
- Read-only operator state view renders label values without modification.

### 14.5 Fake-exchange lifecycle tests

- Fake entry submission → fake fill → fake position confirmed.
- Fake protective stop submission → fake stop confirmed → fake position protected.
- Fake stop replacement (cancel-and-replace) → fake stop replacement confirmed.
- Fake submission timeout → unknown outcome → fail closed.
- Fake fill confirmation followed by missing protective stop → emergency unprotected branch.
- Fake protective stop replacement failure → protection uncertain → fail closed.

### 14.6 Out-of-scope tests

- Phase 4a does NOT include live integration tests against Binance (no live capability).
- Phase 4a does NOT include paper/shadow tests (no paper/shadow).
- Phase 4a does NOT include performance / load / chaos tests at production scale.
- Phase 4a does NOT include end-to-end strategy tests (no strategy is wired in).

---

## 15. Required documentation updates if later authorized

If Phase 4a execution is ever authorized, the resulting implementation phase may need (subject to operator authorization in the execution brief) the following documentation updates. Phase 3x does NOT authorize these updates; they are listed only so the operator's eventual scoping decision is informed.

### 15.1 Possibly in scope for the execution phase

- `docs/08-architecture/implementation-blueprint.md` — possible "Phase 4a safe slice" sub-scope subsection that ties the existing Phase A–G recommended implementation sequence to the §9 candidate components.
- `docs/00-meta/ai-coding-handoff.md` — possible Phase 4 section clarification distinguishing canonical Phase 4 (live-readiness oriented) from Phase 4a (strategy-agnostic infrastructure).
- `docs/12-roadmap/phase-gates.md` — possible Phase 4a paragraph clarifying its strict-subset relationship to Phase 4 with explicit anti-live-readiness preconditions.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 4a execution merged (per the Phase 3o–3w pattern).

### 15.2 Definitely out of scope for the execution phase

- `docs/03-strategy-research/v1-breakout-strategy-spec.md` — substantive content preserved verbatim. Lines 156–172 (EMA slope), 332 (stop-trigger reference), 380 (break-even rule), 415 (stagnation), 564 (Open Question #8) all preserved. Phase 4a does not modify strategy specs.
- `docs/03-strategy-research/v1-breakout-backtest-plan.md` — preserved verbatim.
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` — preserved verbatim.
- `docs/07-risk/stop-loss-policy.md` — substantive content preserved verbatim (per Phase 3v §13 the optional cross-reference back-pointer was permitted but not made; Phase 4a inherits that restraint).
- `docs/06-execution-exchange/binance-usdm-order-model.md` — preserved verbatim.
- `docs/04-data/*` — all data documentation preserved verbatim.
- `docs/10-security/*` — all security documentation preserved verbatim.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w reports and closeouts — preserved verbatim. Phase 4a does not modify prior phase memos.

---

## 16. Risks and mitigations

Phase 3x identifies the following risks specific to Phase 4a execution (extending Phase 3u §12 with code-level concerns):

### 16.1 Live-readiness rhetoric drift

**Risk:** The phrase "Phase 4" carries implicit "we're getting closer to live" connotation. Even if Phase 4a is technically strategy-agnostic infrastructure, drift toward "we're almost ready for live operation" is real (Phase 3u §12.1).

**Mitigation:** The Phase 4a execution authorization brief, the Phase 4a memo, the Phase 4a closeout, the Phase 4a merge closeout, and `current-project-state.md` updates must each include the §6 prohibition list and the "no live-readiness, no exchange-write, no strategy commitment" disclaimer. The disclaimer must appear in commit messages and PR descriptions. The disclaimer is not optional.

### 16.2 Implicit strategy commitment

**Risk:** Building runtime infrastructure naturally creates pressure to "have a strategy by the time the runtime is ready" (Phase 3u §12.2). That pressure compromises framework discipline.

**Mitigation:** Phase 4a's strategy-agnostic framing (§5.4) is binding. The runtime must accept any future authorized strategy without privileging one. The §6.7 prohibition (no strategy commitment / rescue / new candidate) is absolute. Any future strategy authorization is a separate phase requiring separate evidence, separate framework discipline, and separate operator authorization.

### 16.3 Scope creep into exchange-write paths

**Risk:** A common failure mode is "the runtime is ready, let's just *test* the exchange adapter with a real (small) order" (Phase 3u §12.3).

**Mitigation:** Phase 4a's architectural prohibition is structural, not configurational. The live exchange adapter is simply not implemented; only the fake adapter exists in code. There is no configuration switch that "turns on" live exchange-write. A future operator decision to authorize live capability would require *new code* (not configuration) and a *new phase authorization*. The barrier is high by design.

### 16.4 Premature dependency on unresolved pre-tiny-live items

**Risk:** Phase 4a might inadvertently depend on pre-tiny-live items (per §8.4) and code around them in ways that create technical debt.

**Mitigation:** Phase 4a's strict-subset framing (§5.1 / §5.3) excludes anything that requires pre-tiny-live items to be resolved. Specifically: Phase 4a uses placeholder leverageBracket / ExchangeInfo proxies (per TD-024 / TD-020); Phase 4a uses placeholder taker commission rate (per TD-018); Phase 4a uses placeholder notional cap (per TD-018); Phase 4a does not require a public-IP solution (per TD-017); Phase 4a does not require production alert routing (per TD-019); Phase 4a does not require backup schedule (per TD-020). The placeholders are explicit, not implicit; their values are configured rather than hardcoded; their replacement is a pre-tiny-live concern, not a Phase 4a concern.

### 16.5 Misrepresentation of project status

**Risk:** Phase 4a might be cited externally as "Phase 4 is in progress, getting ready for live" (Phase 3u §12.5).

**Mitigation:** Every Phase 4a-related artefact must include the disclaimer (per §16.1 mitigation). `current-project-state.md` updates after Phase 4a execution must explicitly distinguish Phase 4a from canonical Phase 4 and explicitly preserve the recommended-state-paused posture if no subsequent phase is authorized.

### 16.6 Distraction from research

**Risk:** Authorizing Phase 4a moves attention from research to implementation; without a clear research direction, this could mean implementation continues indefinitely while research stalls (Phase 3u §12.6).

**Mitigation:** Phase 4a should be authorized only if the operator has consciously decided to deprioritize research for a defined period, with a clear "implementation-now, research-later" framing. The decision should be explicit in the Phase 4a execution authorization brief. Phase 3x does NOT make that decision; the operator does.

### 16.7 Code-level governance label drift

**Risk:** The four governance label schemes (Phase 3v §8 + Phase 3w §6 / §7 / §8) might be implemented inconsistently across the persistence schema, the event-contract schema, the validation paths, and the dashboard layer — creating opportunities for `mixed_or_unknown` to slip through one decision boundary while being blocked at another.

**Mitigation:** Phase 4a's test harness (§14.4) must include label validation tests at every boundary. The Phase 4a execution brief must require that the four labels be defined as a single shared schema (e.g., a single `LabelScheme` module) used by all artefacts that touch the labels — not as separate copies in each layer. Code review must verify that every label-touching code path uses the single shared schema.

### 16.8 Persistence-layer crash-safety drift

**Risk:** Restart-critical state might not be durably persisted before the runtime proceeds past the associated transition, creating opportunities for restart to lose safety state (per `internal-event-contracts.md` §Durable-Write and Persistence Trigger Rules).

**Mitigation:** Phase 4a's test harness (§14.2 / §14.3) must include simulated-restart tests that verify safety-critical state survives. SQLite WAL mode provides reasonable durability; the Phase 4a execution brief should specify the exact `synchronous` setting (per `database-design.md` Open Question 1) and document the trade-off.

---

## 17. Recommendation

**Phase 3x recommends Option A (remain paused) as primary**, with explicit acknowledgment that Option B (authorize future Phase 4a execution as local-only safe-slice) is now procedurally well-grounded given the post-Phase-3w state.

The reasoning, in compact form:

1. **Phase 3x is itself a successful procedural step.** Authorizing Phase 3x (the scoping memo) is the natural execution of Phase 3u §16.3 + Phase 3w §17.2 conditional alternatives now that GAP-20260424-030 / 031 / 032 / 033 are resolved at the governance level. Phase 3x's value is realized by the memo itself — whether or not any subsequent phase follows.

2. **The cumulative pattern across 12 prior phases (3k → 3w) is "remain paused".** Phase 3x continues that pattern. Reversing it should be deliberate, not automatic.

3. **All four pre-coding governance blockers are resolved.** This is a real procedural improvement, but it does not by itself justify authorizing Phase 4a *execution* — only authorizing Phase 4a *scoping* (which Phase 3x has now done). Whether to authorize Phase 4a execution is a separate operator decision.

4. **Implementation-readiness benefits remain bounded** (Phase 3u §13.7 + Phase 3x §16). The benefits of building strategy-agnostic runtime infrastructure are real but bounded. The risks are also real and well-documented from prior trading-system experience. The benefit-vs-risk balance does not by itself favour authorizing Phase 4a execution unless the operator has a specific motivating reason (e.g., consciously chosen research-deprioritization, or a specific code-enforcement need for the four governance label schemes).

5. **Fresh-hypothesis research remains paused** per Phase 3t §14.2 + Phase 3u §14 + Phase 3v §17 + Phase 3w §17.

Phase 3x does NOT recommend:

- Phase 4 (canonical) — not authorized by any precondition.
- Phase 4a execution — not endorsed over remain-paused. Conditional secondary alternative only if the operator has consciously decided to deprioritize research and is willing to commit to the §6 prohibitions in writing.
- Fresh-hypothesis research — not recommended now.
- Paper/shadow / live-readiness / deployment / production-key / exchange-write — forbidden by phase-gate model.
- ML feasibility / regime-first formal spec / formal cost-model revision — preserved as not-recommended-now per prior phase recommendations.
- Strategy rescue (R2 / F1 / D1-A successor / D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / 5m-on-X) — preserved as forbidden per Phase 3o §6 + Phase 3p §8 + Phase 3r §8 + Phase 3t §13 + Phase 3u §10 + Phase 3v §13 + Phase 3w §14.

Phase 3x answers the originally-asked question:

| Question | Phase 3x answer |
|---|---|
| Whether a future Phase 4a execution phase is now procedurally clean enough to be considered | **Yes — at the governance level.** All four Phase 3u §8.5 pre-coding blockers are RESOLVED. The §6 prohibition list is now codified. The four governance label schemes are now well-defined. Phase 4a execution would be procedurally well-grounded. |
| Whether Phase 4a execution should be authorized now | **Not endorsed over remain-paused.** Acceptable as conditional secondary alternative subject to operator commitment to §6 prohibitions in writing and conscious deprioritization of research. |
| Whether Phase 4a, if ever authorized, must be local-only and exchange-write-free | **Yes — categorically.** Per §5 / §6 / §10. These are binding prohibitions, not aspirational language. |
| Whether fresh-hypothesis research should remain paused | **Yes.** Per Phase 3t §14.2 + Phase 3u §14 + Phase 3v §17 + Phase 3w §17. |
| Whether the four governance label schemes should be enforceable in code | **Yes — at the Phase 4a layer if Phase 4a is ever authorized.** Per §11 / §12. Until then, they remain policy text binding prospectively on any future evidence or runtime artifact. |

---

## 18. Operator decision menu

The operator now has a precise scoping memo for a possible future Phase 4a execution phase. The next operator decision is operator-driven only.

### 18.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. The strategic pause continues. Phase 3x joins the running record. No subsequent phase authorized.

**Reasoning:**
- §17 reasoning applies in full.
- Phase 3x's scoping value is realized by the memo itself; future runtime / paper / live work, if ever authorized, would inherit the §6 prohibition list and the four governance label schemes regardless.
- Pausing preserves operator optionality.

**What this preserves:** Everything in §6, §10, §13.4, and §17.

**What this rules out:** No Phase 4 / Phase 4a execution / fresh-hypothesis research / paper-shadow / live-readiness / deployment / production-key / exchange-write activity.

### 18.2 Option B — Authorize future Phase 4a execution as local-only safe-slice (CONDITIONAL secondary alternative; now procedurally well-grounded)

**Description:** Authorize a separately scoped execution phase that builds the strategy-agnostic runtime infrastructure per §9 candidate components, subject to the §6 prohibition list reaffirmed verbatim in the execution authorization brief.

**Pre-conditions if selected:**
- Operator commits ex-ante to the §6 prohibitions in writing (the execution authorization brief restates §6 verbatim and confirms no item in the prohibition list will be violated).
- Operator commits ex-ante to the §10 out-of-scope list in writing.
- Operator commits ex-ante that authorizing execution does not commit the project to live readiness (§16.1 mitigation).
- Operator commits ex-ante that Phase 4a success does not authorize paper/shadow, tiny live, or any subsequent phase (§16.1 mitigation).
- Operator selects the §9 component scope (one or more of the ten components, or all of them, or a stricter subset) and explicitly authorizes that scope.
- Operator commits ex-ante that the four governance label schemes will be enforced in code at every decision boundary (§16.7 mitigation).
- Operator commits ex-ante that pre-tiny-live items (§8.4) remain pre-tiny-live concerns and are NOT Phase 4a blockers — Phase 4a uses configured placeholders for those items, not hardcoded values.
- Operator commits ex-ante (preferably) to a defined research-deprioritization period (§16.6 mitigation), or alternatively explicitly waives §16.6 with a written rationale.

**Phase 3x view:** Acceptable as conditional secondary. Phase 3x's resolution of the governance-level pre-coding blockers (via Phase 3v + Phase 3w) makes this option more procedurally available than it was at Phase 3u §16.3. **Not endorsed over Option A** purely because Option A also fully realizes Phase 3x's scoping value (the §6 prohibition list and the four governance label schemes are binding prospectively regardless of any subsequent phase). The operator should select Option B only if the §16.6 (research-deprioritization) precondition is met or explicitly waived.

### 18.3 Option C — More docs-only preparation first (CONDITIONAL tertiary alternative)

**Description:** Authorize one or more additional docs-only memos before any Phase 4a execution. Possible candidates (none authorized by Phase 3x):

- A docs-only Phase 4a execution-plan memo that translates the §9 candidate components into a per-commit / per-PR plan with explicit acceptance criteria for each commit. This would be a more granular pre-execution scoping memo than Phase 3x.
- A docs-only label-enforcement design memo that specifies the code-level form of the four governance label schemes (exact field names, exact validation paths, exact persistence schema columns, exact event-contract field definitions) per §8.3 / §11. This would resolve §8.3 at the documentation level before any code is written.
- A docs-only documentation-refresh memo that updates `docs/08-architecture/implementation-blueprint.md` Phase A-G with explicit Phase 4a sub-scope language; updates `docs/00-meta/ai-coding-handoff.md` Phase 4 section; updates `docs/12-roadmap/phase-gates.md` with explicit Phase 4a paragraph (per §15.1).

**Phase 3x view:** Acceptable as conditional tertiary. Each candidate would produce unconditional documentation value. **Not endorsed over Option A or Option B.** If the operator is not ready to commit to Option B's preconditions, Option C is a procedurally safer middle path that produces documentation value without authorizing any code. If the operator is ready to commit to Option B's preconditions, Option C is unnecessary procedural overhead.

### 18.4 Option D — Return to research / sensitivity analysis (NOT RECOMMENDED)

**Description:** Authorize one of: H-D3 break-even +2.0R variant; H-C2 fitted-slope EMA variant; H-D5 stagnation-window 6/10/12 bars; mark-price stop sensitivity on retained-evidence populations; fresh-hypothesis research per Phase 3t §14.2 + Phase 3u §14.

**Phase 3x view:** **Not recommended now.** Same posture as Phase 3v §17.4 + Phase 3w §17.3 + Phase 3w §17.4. Bounded marginal information value. Procedurally heavy. Phase 3t / Phase 3u / Phase 3v / Phase 3w cumulative recommendation has been research-paused. Phase 3x reaffirms that recommendation.

### 18.5 Option E — Phase 4 (canonical) / paper-shadow / live-readiness / deployment / production-key / exchange-write (FORBIDDEN / NOT RECOMMENDED)

**Description:** Authorize one of: Phase 4 canonical (per `phase-gates.md` Phase 4); paper/shadow (Phase 7); tiny live (Phase 8); scaled live (Phase 9); production Binance key creation; exchange-write capability; MCP / Graphify / `.mcp.json` / credentials work.

**Phase 3x view:** **Forbidden / not recommended.** Per `phase-gates.md`, none of these gates is met. Per the cumulative Phase 3o → Phase 3w + Phase 3x pattern, none of these is appropriate. Strongly not recommended. Same posture as Phase 3u §16.5 + Phase 3v §17.5 + Phase 3w §17.5.

### 18.6 Recommendation

**Phase 3x recommends Option A (remain paused) as primary.** Option B (authorize future Phase 4a execution as local-only safe-slice) is acceptable as conditional secondary, now procedurally well-grounded given Phase 3v + Phase 3w resolution of all four pre-coding governance blockers, subject to the §18.2 preconditions. Option C (more docs-only preparation first) is acceptable as conditional tertiary. Option D (return to research / sensitivity analysis) is not recommended now. Option E (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) is forbidden / not recommended.

---

## 19. Next authorization status

**No next phase has been authorized.** Phase 3x authorizes nothing other than producing this scoping memo and the accompanying closeout artefact. The operator's decision after Phase 3x is operator-driven only.

Selection of any subsequent phase (Phase 4a execution per Option B; more docs-only preparation per Option C; return to research per Option D; Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write per Option E) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is now defined in the project record (per Phase 3x — this memo). **Recommended state remains paused.**
