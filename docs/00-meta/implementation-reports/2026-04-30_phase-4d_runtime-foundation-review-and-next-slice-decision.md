# Phase 4d — Post-4a/4b/4c Runtime Foundation Review and Next-Slice Decision

**Authority:** Phase 4a (Local Safe Runtime Foundation); Phase 4b (Repository Quality Gate Restoration — scripts); Phase 4c (State Package Ruff Residual Cleanup); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 3x §6 / §10 (Phase 4a strict-subset framing); Phase 2i §1.7.3 project-level locks; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/08-architecture/state-model.md`; `docs/08-architecture/runtime-persistence-spec.md`; `docs/08-architecture/database-design.md`; `docs/08-architecture/internal-event-contracts.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/kill-switches.md`; `docs/06-execution-exchange/exchange-adapter-design.md`; `docs/09-operations/first-run-setup-checklist.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4d — **Post-4a/4b/4c Runtime Foundation Review and Next-Slice Decision** (docs-only). Reviews the merged Phase 4a local safe runtime foundation, the Phase 4b/4c quality-gate restoration, and the current post-Phase-4c boundary; decides whether the next safe project step should be another local-only implementation slice, a docs-only design memo, a return-to-research pause, or no action.

**Branch:** `phase-4d/runtime-foundation-review-and-next-slice-decision`. **Memo date:** 2026-04-30 UTC.

**Phase 4d does NOT start Phase 4 canonical. Phase 4d does NOT authorize paper/shadow. Phase 4d does NOT authorize live-readiness. Phase 4d does NOT authorize exchange-write. Phase 4d does NOT validate or rescue any strategy. Phase 4d does NOT write implementation code. Phase 4d does NOT modify any source code, tests, scripts, data, manifests, or strategy docs.**

---

## 1. Summary

Three implementation phases (4a, 4b, 4c) have shipped a strategy-agnostic local safe runtime foundation with a fully clean repository quality gate. Phase 4d evaluates whether to keep building or pause.

**Phase 4d recommends Option A (remain paused) as primary** — the runtime foundation is intentionally bounded and any next slice expands surface area without expanding optionality. **Option D (docs-only reconciliation-model design memo) is acceptable as conditional secondary** if the operator wishes to keep moving while staying inside docs-only discipline; among the implementation slices Option C (richer fake-exchange lifecycle / failure-mode tests) and Option B (structured runtime logging / audit export) are the safest *if* the operator authorizes implementation work, but neither is endorsed over the primary recommendation.

**Verification (run on the post-Phase-4c-merge tree):**

- `ruff check .` (whole repo): **All checks passed!**
- `pytest`: **785 passed in 12.89s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

**No retained-evidence verdict revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim. **No policy locks changed.** **No code, tests, scripts, data, manifests, strategy docs modified by Phase 4d.** **Recommended state remains paused.**

---

## 2. Authority and boundary

Phase 4d operates strictly inside the post-Phase-4c-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a strict-subset framing); Phase 4a's anti-live-readiness statement; Phase 4b's scripts-scope cleanup; Phase 4c's state-package residual cleanup.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.**
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md`.

Phase 4d adds *forward-looking review language* — a written assessment of the runtime foundation and a structured next-slice decision — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate.

---

## 3. Starting state

```text
branch:           phase-4d/runtime-foundation-review-and-next-slice-decision
parent commit:    582a1f7e86f40efff0a2a27e914ae4e38e12ab14 (post-Phase-4c-merge housekeeping)
working tree:     clean before review
main:             582a1f7e86f40efff0a2a27e914ae4e38e12ab14 (unchanged)

Phase 4a foundation: merged (Phase 4a merge commit 3c368fa; housekeeping 829c25a).
Phase 4b cleanup:    merged (Phase 4b merge commit f099a94; housekeeping 5c79cea).
Phase 4c cleanup:    merged (Phase 4c merge commit 4460b2f; housekeeping 582a1f7).
Repository quality gate: fully clean (ruff check . passes; pytest 785 passes;
                          mypy strict 0 issues across 82 source files).
phase-gate state:    Phase 4 (canonical) unauthorized; Phase 4d execution authorized
                     only as a docs-only review (this phase).
research thread:     5m research thread operationally complete (Phase 3t).
v002 datasets:       locked; manifests untouched.
v001-of-5m:          trade-price research-eligible; mark-price research_eligible:false.
governance:          Four governance label schemes binding prospectively
                     (stop_trigger_domain | break_even_rule | ema_slope_method
                     | stagnation_window_role); enforced in code at the Phase 4a
                     layer; mixed_or_unknown invalid and fails closed.
locks:               §11.6 = 8 bps HIGH per side; §1.7.3 mark-price stops; preserved.
```

---

## 4. Why this review exists

Phase 4d exists for **four** reasons:

1. **Phase 4a's terminal recommendation was Option A (review on branch and remain paused) primary, with Option B (merge and remain paused) as conditional secondary.** The operator selected Option B for Phase 4a, then authorized two narrow follow-up cleanups (Phase 4b for scripts; Phase 4c for state package) to fully close the quality gate. The original "remain paused after merge" decision was deferred while the gate was being closed; now that the gate is fully clean, the deferred pause-vs-keep-going decision is again on the operator's plate.
2. **Phase 4a's §25 operator decision menu listed Option C (richer runtime work) as conditional tertiary requiring a fresh operator brief.** Phase 4d is that brief — a structured, docs-only review of what such work would or would not look like, given the post-4a/4b/4c boundary.
3. **The runtime foundation's *bounded* nature should be made explicit before any next slice.** Phase 4a built strategy-agnostic infrastructure; the natural next question is which slice (if any) extends infrastructure further without crossing into strategy / live-readiness. Phase 4d enumerates candidate slices and ranks them.
4. **Anti-rhetoric drift.** Phase 3u §12.1 / Phase 3x §16.1 / Phase 4a §16.1 all warned against "live-readiness rhetoric drift" — the slow normalization of "we're getting closer to live" framing as runtime infrastructure grows. Phase 4d writes that warning into the project record once more, while the foundation is still small and the rhetoric is still defensible.

---

## 5. Phase 4a runtime foundation review

Phase 4a implemented ten Phase 3x §9 safe-slice components (per the merged Phase 4a implementation report and merge closeout):

| Component | Scope | Status |
|---|---|---|
| **Runtime mode / state model** (`prometheus.state`) | `RuntimeMode` `StrEnum` (SAFE_MODE / RUNNING / BLOCKED / EMERGENCY / RECOVERY_REQUIRED); `RuntimeControlState` frozen pydantic record; pure-function transitions (`enter_safe_mode`, `enter_running`, `enter_blocked`, `enter_emergency`, `enter_recovery_required`, `activate_kill_switch`, `clear_kill_switch`); startup defaults to SAFE_MODE; unknown state fails closed via explicit transition guards. | Implemented; tests pass; ruff/mypy clean. |
| **Runtime control state persistence** (`prometheus.persistence`) | SQLite WAL with `foreign_keys=ON`, `synchronous=FULL`, `busy_timeout=5000`; single-row `runtime_control` table; append-only `runtime_mode_event` audit table; append-only `governance_label_audit` table; persisted RUNNING does NOT auto-resume RUNNING; kill-switch state persists across restart; never auto-clears. | Implemented; tests pass. |
| **Internal event contracts** (`prometheus.events`) | `MessageEnvelope`, `MessageClass` enum, `RuntimeModeChangedEvent`, `KillSwitchEvent`, `FakeExchangeLifecycleEvent` with `is_fake = True` invariant, `GovernanceLabelEvent`. | Implemented; tests pass. |
| **Governance label enforcement** (`prometheus.core.governance`) | Single source of truth for the four label schemes (`StopTriggerDomain`, `BreakEvenRule`, `EmaSlopeMethod`, `StagnationWindowRole`); `is_fail_closed`, `require_valid`, four `parse_*` strict parsers; `mixed_or_unknown` fails closed at every governance-relevant decision boundary by importing from this single module. | Implemented; tests verify single-source-of-truth invariant; tests pass. |
| **Risk sizing skeleton** (`prometheus.risk.sizing`) | `compute_sizing(SizingInputs) -> SizingResult`; locked v1 constants `LOCKED_LIVE_RISK_FRACTION = 0.0025`, `LOCKED_LIVE_LEVERAGE_CAP = 2.0`; fail-closed on missing/invalid metadata, below-minimum quantity, notional cap, leverage cap. | Implemented; tests pass. |
| **Exposure gate skeleton** (`prometheus.risk.exposure`) | `evaluate_entry_candidate(...) -> ExposureDecision`; BTCUSDT-only (Rule 1); one-position max (Rule 2); no pyramiding (Rule 3); no reversal (Rule 4); entry-in-flight blocks (Rule 7); unprotected-position blocks (Rule 9); manual-exposure blocks; fake-position state only. | Implemented; tests pass. |
| **Stop-validation skeleton** (`prometheus.risk.stop_validation`) | `validate_initial_stop` and `validate_stop_update`; Phase 3v `stop_trigger_domain` governance enforced; side-vs-entry; ATR filter (0.60 ≤ stop_distance/ATR ≤ 1.80); risk-reducing-only direction; `mixed_or_unknown` fails closed at construction. | Implemented; tests pass. |
| **Fake-exchange adapter** (`prometheus.execution.fake_adapter`) | `FakeExchangeAdapter`; deterministic local in-memory state machine; injectable clock; methods `submit_entry_order`, `confirm_fake_fill`, `mark_entry_unknown_outcome`, `submit_protective_stop`, `confirm_fake_protective_stop`, `mark_stop_submission_failed`, `trigger_fake_stop`; emits `FakeExchangeLifecycleEvent` with `is_fake = True`; **no Binance code; no network I/O; no credentials**. | Implemented; tests pass. |
| **Read-only operator state view** (`prometheus.operator.state_view`, `prometheus.cli`) | `format_state_view(...)` pure function; `inspect-runtime --db PATH` CLI; **no controls; no exchange actions; no production alerting**. | Implemented; tests pass. |
| **Test harness** (`tests/unit/runtime/`) | 10 test files; 117 Phase 4a runtime tests; deterministic; offline. | Implemented; all pass. |

### 5.1 What the foundation gives the project

The foundation is **strategy-agnostic runtime safety scaffolding**: a place where a *future* authorized strategy could plug in without each future strategy re-implementing kill-switch persistence, governance-label enforcement, exposure gates, stop validation, fake-adapter testing, or read-only state surface. The four governance label schemes from Phase 3v + Phase 3w are now *enforceable in code at every relevant decision boundary* (persistence, event validation, stop validation, fake-adapter decisions, sizing path), not merely policy text. `mixed_or_unknown` fails closed at six independent boundaries (per Phase 4a §10), each tested.

### 5.2 What the foundation does NOT give the project

The foundation is *bounded by design* — Phase 3x §6 / §10 prohibitions:

- **No live exchange capability.** Architectural prohibition is structural, not configurational; only the fake adapter exists in code.
- **No production credentials, no `.env`, no `.mcp.json` modification, no Graphify, no MCP enabling.**
- **No strategy logic.** No V1 / R3 / R2 / F1 / D1-A code. The runtime *accepts* any future authorized strategy without privileging one.
- **No backtest engine.** No re-run of Phase 2 / Phase 3 backtests; no H-D3 / H-C2 / H-D5 sensitivity analyses; no mark-price-stop sensitivity backtests.
- **No paper/shadow runtime.** Phase 4a is not Phase 7.
- **No deployment artefact.** No service file, no daemon, no NUC live setup.
- **No data acquisition / patching / regeneration / modification.** All `data/` artefacts preserved verbatim.

### 5.3 Architectural posture

The foundation matches `docs/08-architecture/codebase-structure.md` Target Repository Layout for the in-scope subset: `core/`, `state/`, `persistence/`, `events/`, `risk/`, `execution/` (fake adapter only), `operator/`, plus a top-level `cli.py`. Modules outside this subset (`market_data/`, `strategy/` runtime layer, `exchange/` live adapter, `reconciliation/`, `safety/`, `runtime/` orchestrator, `observability/`, `config/`, `secrets/`) are deliberately not implemented in Phase 4a. The strategy-agnostic skeleton can be extended *incrementally* by future authorized phases; nothing in the foundation forces a specific later expansion order.

---

## 6. Phase 4b/4c quality-gate review

The Phase 4a merge to main left a documented quality gap: 31 `ruff check .` errors (29 in `scripts/phase3q_5m_acquisition.py` + `scripts/phase3s_5m_diagnostics.py`; 2 latent in `src/prometheus/state/`).

| Phase | Scope | Outcome |
|---|---|---|
| **Phase 4b** | 29 known ruff issues in the two Phase 3q / 3s standalone orchestrator scripts (E501 × 18; F401 × 3; B905 × 3; B007 × 2; E741 × 2; SIM108 × 1). | All 29 fixed via behavior-preserving lint-only edits: removed unused imports; renamed unused loop variables; added `strict=True` to `zip()` calls; renamed ambiguous `l` → `lo`; converted one if/else to ternary; split long lines via adjacent f-string literals / multi-line reformat. Honest report of 2 residual latent issues in Phase 4a state code (out of Phase 4b scope per the brief). |
| **Phase 4c** | 2 residual ruff issues in `src/prometheus/state/__init__.py:20:1` (I001 import order) and `src/prometheus/state/transitions.py:49:5` (SIM103 simplify return). | Both fixed via behavior-preserving lint-only edits: alphabetized four relative imports (`__all__` unchanged; public API unchanged); collapsed final `if incident_active: return True; return False` to `return bool(incident_active)` (truth table unchanged for every input). |
| **Combined** | 31 → 0 errors. | Whole-repo `ruff check .` passes cleanly; pytest 785 passed; mypy strict 0 issues across 82 source files. |

The discipline pattern across 4b → 4c is worth recording explicitly: *narrow scope, lint-only edits, behavior-preservation by construction, honest reporting of residuals, separately-authorized follow-up*. Phase 4b explicitly refused to fix the 2 state-package issues out-of-scope and recommended `phase-4c/state-package-lint-residual` as a follow-up; the operator authorized exactly that. This pattern is the project's working definition of "small, honest, separable" code-hygiene work, and is the model any future code-hygiene phase should follow.

---

## 7. Current verification state

All required Phase 4d verification commands ran on the project's `.venv` (Python 3.12.4):

```text
=== git status ===
On branch phase-4d/runtime-foundation-review-and-next-slice-decision
nothing to commit, working tree clean

=== python --version ===
Python 3.12.4

=== ruff check . ===
All checks passed!

=== pytest -q ===
785 passed (12.89s)

=== mypy ===
Success: no issues found in 82 source files
```

The repository quality gate is fully clean. No regressions across 4a/4b/4c. No script was run; no data was acquired or modified; no diagnostics or backtests were run.

---

## 8. Safety properties now established

The Phase 4a / 4b / 4c trio establishes the following safety properties in code (each with at least one test in `tests/unit/runtime/`):

1. **Startup always enters SAFE_MODE.** `fresh_control_state` always returns SAFE_MODE with `entries_blocked = True`, regardless of any persisted prior mode.
2. **Persisted RUNNING does not auto-resume RUNNING.** The runtime layer carries forward only restart-critical flags (kill switch, operator review, incident, pause) and resets the runtime mode itself to SAFE_MODE.
3. **Kill-switch persists across restart.** Persisted `kill_switch_active = True` survives a simulated restart.
4. **Kill-switch never auto-clears.** Only an explicit `clear_kill_switch` call clears it, and it returns to SAFE_MODE (not RUNNING).
5. **Kill-switch blocks fake entries.** With kill-switch active, `enter_running` raises `KillSwitchActiveError`.
6. **`mixed_or_unknown` fails closed at six independent decision boundaries.** Persistence; initial-stop validation; stop-update validation at construction; fake-lifecycle event construction; governance-label event construction; fake-adapter stop submission. All tested.
7. **Stop widening is rejected.** Both long and short widening attempts raise `StopValidationError`.
8. **Exposure gates enforce one-symbol / one-position / no-pyramiding / no-reversal / no-unprotected-position-allows-new-entry / no-manual-exposure-allows-new-entry.**
9. **Position without confirmed protection forces EMERGENCY.** End-to-end test drives the EMERGENCY transition explicitly.
10. **Fake events are syntactically distinguishable from live events.** All `FakeExchangeLifecycleEvent` instances carry `is_fake = True` (model-validated invariant); no code path emits an event without that marker.
11. **Read-only operator surface does not expose exchange actions.** Output-text scan rejects all action-shaped phrases.
12. **Persistence rejects corrupt runtime modes.** A direct SQL injection of an out-of-scheme `runtime_mode` value causes `load_persisted` to raise `RuntimeStoreError`.
13. **No network I/O.** Phase 4a code base contains no `httpx`, `socket`, `websockets`, `urllib`, or `requests` imports; tests run offline.
14. **No secrets in code, tests, or DB.** No `.env` is read; no credential field is persisted; no test fixture contains a token or key.
15. **Single source of truth for governance labels.** All four schemes are defined exactly once in `prometheus.core.governance`; the single-source-of-truth invariant is verified by a dedicated test.

These 15 properties are now structural guarantees of the post-4a/4b/4c boundary. Any future phase that breaks them must do so explicitly and with separate operator authorization.

---

## 9. Remaining limitations

The runtime foundation is intentionally limited. Phase 4d evaluates each limitation but does not implement any of them.

### 9.1 No reconciliation engine

`RuntimeMode.RECOVERY_REQUIRED` is a *state*, not a *workflow*. Phase 4a does not implement the reconciliation flow described in `docs/06-execution-exchange/user-stream-reconciliation.md` (compare local vs exchange position; classify clean / recoverable / unsafe; repair-or-escalate; rerun integrity check). Implementing reconciliation would require either a real exchange capability (forbidden in v1 outside paper/shadow gates) or a *richer fake adapter* that can simulate position / order / stop state divergence on demand. The richer-fake-adapter path is local-only and Phase-4a-aligned; the real-exchange path is not.

### 9.2 No structured runtime logging / audit export beyond current persistence

The Phase 4a `RuntimeStore` provides three append-only audit tables (`runtime_mode_event`, `governance_label_audit`, plus the single-row `runtime_control`). It does not provide:

- A structured log format (JSON Lines, OpenTelemetry, or equivalent) for human / machine consumption beyond pytest-driven verification.
- An export pathway (e.g., a CLI subcommand to dump audit rows to a JSON / NDJSON file for archival).
- A redaction layer for any future content that might inadvertently include sensitive material (Phase 4a's content is provably non-sensitive — no credentials, no PII; but a defensive redaction layer is good operational practice).
- A retention / rotation policy.

Adding these is local-only and well-scoped.

### 9.3 No richer fake-exchange failure matrix beyond Phase 4a

The current `FakeExchangeAdapter` covers entry submission, fill confirmation, unknown outcome, protective stop submission, stop confirmation, stop submission failure, stop trigger. It does NOT cover (because Phase 4a was deliberately bounded):

- Partial fills.
- Stop replacement (cancel-and-replace) lifecycle in detail (the runtime currently exposes `submit_protective_stop` but no explicit `replace_protective_stop` method; updates would call submit-then-cancel rather than the cancel-and-replace pattern in `docs/07-risk/stop-loss-policy.md` §Cancel-and-Replace Procedure).
- Multiple-stop detection / orphaned-stop detection at adapter level.
- Stream stale simulation while flat / while exposed.
- Reconciliation-trigger conditions (which is §9.1).
- Rate-limit / IP-ban simulation (relevant only when a real adapter eventually exists).
- Permission / authorization anomaly simulation.
- Mark-price reference vs trade-price reference divergence at the adapter layer (relevant for `stop_trigger_domain = mark_price_runtime` enforcement at the fake-runtime path; Phase 4a handles this only at the validator layer).

Adding these is local-only, valuable for testing the existing risk / state / persistence layers under more failure modes, and Phase-4a-aligned.

### 9.4 No strategy-readiness gate

A "strategy-readiness gate" would be a runtime-internal check that, given a strategy's configuration declaration (e.g., `stop_trigger_domain = mark_price_runtime`, `break_even_rule = enabled_plus_1_5R_mfe`, `ema_slope_method = discrete_comparison`, `stagnation_window_role = active_rule_predeclared`), validates that the runtime's expected label set and the strategy's declared label set match before allowing `enter_running`. Phase 4a does not implement this because no strategy is wired in. Designing the gate is a docs-only exercise; implementing it requires either a real strategy module (forbidden in this scope) or a stub strategy module that the runtime imports.

### 9.5 No market-data ingestion

Phase 4a is strategy-agnostic; it does not import historical or live market data. Implementing market-data ingestion is *not* a strategy-agnostic activity — it requires either consuming v002 datasets (research-side) or consuming live data (forbidden). Phase 4d does NOT recommend market-data ingestion as a next slice.

### 9.6 No live exchange adapter

This is the categorical prohibition that Phase 3x §6 and Phase 4a §22 establish structurally. Phase 4d does NOT propose lifting it.

### 9.7 No paper/shadow path

Per `docs/12-roadmap/phase-gates.md` Phase 7, paper/shadow is its own gate with its own evidence requirements. Phase 4d does NOT propose it.

### 9.8 No deployment path

No service file, no daemon, no NUC live setup, no Telegram / n8n production alerting. These are pre-tiny-live concerns per the technical-debt register (TD-017 / TD-018 / TD-019 / TD-020). Phase 4d does NOT propose them.

### 9.9 No production alerting

Telegram / n8n alerts are pre-tiny-live per TD-019. Phase 4d does NOT propose them.

### 9.10 No strategy edge

R3 baseline-of-record is aggregate-negative on R-window expR. R2 / F1 / D1-A are terminal under current locked spec. The 5m research thread is operationally complete (Phase 3t). Phase 4d does NOT propose strategy work; that boundary is governed by Phase 3t §14.2 + Phase 3u §14 + Phase 3v §17 + Phase 3w §17 + Phase 3x §18 + Phase 4a §22 (all preserved).

---

## 10. Technical-debt review

Per `docs/12-roadmap/technical-debt-register.md`, the following items remain documented as pre-tiny-live concerns and are NOT pre-coding blockers for Phase 4a-aligned implementation slices:

- **TD-006** — Exact Binance endpoint behavior verification. Partially resolved at coding time for bulk klines + mark-price (Phase 3q); remains open for REST-write paths and user-stream behavior. Not relevant to Phase 4a-aligned work.
- **TD-008** — TradingView-like chart implementation. Deferred. Not relevant to Phase 4a-aligned work.
- **TD-009** — Remote approvals through Telegram/n8n. Deferred (POST_MVP). Not relevant.
- **TD-017** — Public-IP solution for local NUC. Pre-tiny-live.
- **TD-018** — First live notional cap value. Pre-tiny-live.
- **TD-019** — Production alert route selection. Pre-tiny-live.
- **TD-020** — Backup schedule and retention. Pre-tiny-live.

The four Phase 3u §8.5 currently-OPEN pre-coding governance blockers are RESOLVED at the governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033 by Phase 3w), and enforced in code at the Phase 4a layer. `docs/00-meta/implementation-ambiguity-log.md` has zero OPEN entries that constitute pre-coding blockers per Phase 3u §8.5; pre-tiny-live items remain documented.

**No new technical debt was introduced by Phase 4a / 4b / 4c.** Phase 4a's report flagged the 29 + 2 latent ruff issues, both of which are now fixed (Phase 4b + Phase 4c). The post-Phase-4c boundary has no known unresolved code-hygiene debt.

---

## 11. Phase-gate assessment

`docs/12-roadmap/phase-gates.md` defines the canonical phase sequence:

```text
PHASE 0 — Documentation and implementation planning
PHASE 1 — Local development foundation
PHASE 2 — Historical data and validation foundation
PHASE 3 — Backtesting and strategy conformance
PHASE 4 — Risk, state, and persistence runtime
PHASE 5 — Dashboard, observability, and alerts
PHASE 6 — Dry-run exchange simulation
PHASE 7 — Paper/shadow operation
PHASE 8 — Tiny live
PHASE 9 — Scaled live
```

### 11.1 Project's actual phase position

| Phase | Status | Notes |
|---|---|---|
| Phase 0 | Complete. | |
| Phase 1 | Complete. | |
| Phase 2 | Complete. | v002 datasets locked. |
| Phase 3 | **Research arc closed without an actionable candidate.** | V1 / F1 / D1-A all terminal. 5m research thread closed. |
| Phase 4 (canonical) | **Not authorized.** | Per phase-gate doc, Phase 4 (canonical) requires Phase 3 strategy evidence; the project does not have it. |
| Phase 4a (safe-slice) | **Implemented and merged** (per Phase 3x scoping + Phase 4a execution + Phase 4b/4c quality cleanup). | Strategy-agnostic infrastructure; not Phase 4 canonical. |
| Phase 4d (this review) | **In progress.** | Docs-only forward-looking review. |
| Phase 5 (dashboard, observability, alerts) | **Not authorized.** | Phase 5 in the canonical gate model is downstream of Phase 4 canonical, not Phase 4a. A *narrow* observability slice (e.g., structured runtime logging — §13 Option B below) is a Phase-4a-aligned candidate and is not the same as canonical Phase 5. |
| Phase 6 (dry-run exchange simulation) | **Partially implemented as the Phase 4a fake adapter.** | The Phase 4a fake adapter is dry-run by construction; richer dry-run *failure modes* are a Phase-4a-aligned candidate (§13 Option C). |
| Phase 7–9 | **Not authorized.** | Each gated by the prior phase. |

### 11.2 Phase-gate interpretation reminder

Phase 3u §6.3 noted that "Phase 3 complete" should be read as "Phase 3 work has reached a stable, documented endpoint" rather than "Phase 3 has produced a live-eligible strategy." Phase 4d preserves this interpretation: Phase 4a was authorized as a *strict subset* of canonical Phase 4 (per Phase 3x §5.1) precisely because canonical Phase 4 framing assumes strategy evidence which the project does not have.

Any next slice the operator authorizes must remain inside the strict-subset framing (no strategy commitment / rescue / new candidate; no live-readiness implication; no exchange-write capability). This rules out ascending the canonical phase ladder past Phase 4a; it does not rule out *widening* Phase 4a-aligned work.

---

## 12. Candidate next slices

Phase 4d evaluates seven candidate next moves. **Phase 4d does NOT authorize any of them.** Phase 4d ranks them and recommends a posture.

### 12.1 Option A — Remain paused (PRIMARY recommendation)

**Description:** Take no further action. Phase 4d joins Phase 4c as a clean documented endpoint. The Phase 4a runtime foundation persists on main; the quality gate is fully clean; the operator may at any time authorize a future phase.

**Pros:**
- Preserves operator optionality fully.
- Runtime foundation's bounded scope is not enlarged; no rhetorical drift toward live-readiness.
- Discipline pattern (cumulative "remain paused" recommendation across Phase 3k → Phase 4a) continues.
- No new code = no new code-hygiene debt = no new test surface = no new mypy / ruff exposure.

**Cons:**
- No incremental progress on infrastructure that any future strategy would need.
- The richer fake-exchange failure matrix (§9.3) and the structured runtime logging (§9.2) remain "easy" wins that could be done at low risk.

**Phase 4d view:** The cons are real but bounded. The pause posture is the correct default; the operator explicitly chooses to widen scope only when there is a concrete reason.

### 12.2 Option B — Local-only structured runtime logging / audit export slice (CONDITIONAL secondary)

**Description:** A Phase 4a-aligned implementation slice that adds: (a) a structured logging format (e.g., JSON Lines) for runtime events; (b) a CLI subcommand to export audit rows from the SQLite database to a JSON / NDJSON file; (c) a defensive redaction layer for any field that might in future contain sensitive material; (d) tests covering the export path, redaction, and a documented retention discipline.

**Pros:**
- Strictly local-only; no exchange touch; no credentials.
- Adds operator-visible value (audit-trail export) that is directly useful in any future operator workflow.
- Forces precise specification of the runtime's *output-side* contracts (event schemas at rest), which is currently implicit.
- Reuses existing `RuntimeStore` audit tables; does not require schema changes.

**Cons:**
- Adds code surface area for low marginal value while no strategy is wired in.
- The "defensive redaction layer" is preventive — it solves a problem that does not yet exist (no sensitive data is currently emitted).
- Risk of drift: a "structured logging" slice could accidentally grow into "production observability" if not strictly scoped.

**Phase 4d view:** Acceptable as conditional secondary, with a docs-only design memo first (preferred). The operator should not authorize implementation without first reviewing a precise scope memo (analogous to Phase 3x being the pre-Phase-4a scoping memo).

### 12.3 Option C — Richer fake-exchange lifecycle and failure-mode test slice (CONDITIONAL alternative)

**Description:** A Phase 4a-aligned implementation slice that extends the `FakeExchangeAdapter` with: (a) cancel-and-replace stop lifecycle; (b) partial fills; (c) multiple-stop detection / orphaned-stop detection; (d) stream-stale simulation; (e) mark-price-vs-trade-price reference divergence; (f) tests covering each new failure mode against the existing risk / state / persistence layers.

**Pros:**
- Strictly local-only; no exchange touch; no credentials.
- Exercises the existing risk / stop-validation / state-machine code under more conditions, which improves confidence in the foundation's safety properties.
- Aligns with `docs/06-execution-exchange/exchange-adapter-design.md` §Public Interface Families (the fake adapter's interface widens toward the documented adapter shape, but stays inside fake state).
- Direct-pre-requisite for any future reconciliation engine (§9.1) — the richer fake adapter is what reconciliation tests would consume.

**Cons:**
- Adds significant code surface area in the fake adapter (Phase 4a's adapter is already 337 lines).
- Tests for each new failure mode multiply the test count, increasing CI time (currently 12.89s; a richer matrix could push pytest into 30–60s territory).
- Risk of drift: the adapter could grow toward "what a real adapter does" without the explicit boundary that distinguishes fake from real.

**Phase 4d view:** Acceptable as conditional alternative. Like Option B, a docs-only design memo first is preferred. Among the implementation slices, Option C is the safest from a discipline standpoint because the architectural prohibition (no real adapter) is enforced by code structure, not configuration; widening the fake adapter does not erode that prohibition.

### 12.4 Option D — Local-only reconciliation-model design memo, docs-only first (CONDITIONAL alternative)

**Description:** A docs-only design memo that specifies how a future reconciliation engine would interact with the existing `RuntimeMode.RECOVERY_REQUIRED` state, the runtime control persistence layer, the fake-exchange adapter (or a future authorized real adapter), and the operator-review-required flag. The memo would NOT authorize implementation.

**Pros:**
- Docs-only; lowest possible risk.
- Forces precise specification of the reconciliation contract before any code is written.
- Documents the bridge between the current static `RECOVERY_REQUIRED` state and a future workflow.
- Could be done with full operator review of each section.

**Cons:**
- Marginal incremental value if reconciliation is far in the future; the memo could become stale.
- The reconciliation contract depends on a richer fake adapter (Option C), so the design memo would either pre-suppose Option C or specify both layers.

**Phase 4d view:** Acceptable as conditional alternative. If the operator wishes to keep moving while staying inside docs-only discipline (matching the Phase 3o → Phase 3w cadence), Option D is the safest move.

### 12.5 Option E — Strategy-readiness gate design memo, docs-only first (CONDITIONAL alternative)

**Description:** A docs-only design memo that specifies how a future strategy-readiness gate would (a) consume a strategy's declared governance labels; (b) compare them against the runtime's expected labels; (c) fail closed on mismatch; (d) interact with `enter_running`. The memo would NOT authorize implementation.

**Pros:**
- Docs-only; lowest possible risk.
- Closes the loop on the four governance label schemes — currently they are *enforced* but not *consumed* by a readiness gate.
- Could be combined with Option D into a single "runtime-readiness contract" memo.

**Cons:**
- A strategy-readiness gate is meaningless without a strategy. The memo would be designing a contract whose other side is forbidden in this project posture.
- Risk of "designing for a strategy" framing that subtly pre-supposes strategy work.

**Phase 4d view:** **Not recommended now.** Strategy-readiness gates are a downstream concern; designing them while no strategy is authorized creates the rhetorical drift Phase 3u §12.1 / Phase 3x §16.1 / Phase 4a §16.1 warned about. Defer until a strategy is on the operator's authorization horizon.

### 12.6 Option F — Return-to-research / fresh hypothesis discovery (NOT RECOMMENDED NOW)

**Description:** Authorize a Phase 3a / Phase 3f-style new-strategy-discovery memo proposing an entirely new strategy family from first principles, not derived from any retained-evidence candidate or Phase 3s findings.

**Phase 4d view:** **Not recommended now.** Per Phase 3t §14.2 + Phase 3u §14 + Phase 3v §17 + Phase 3w §17 + Phase 3x §18 + Phase 4a §22. Three strategy-research arcs have framework-failed under unchanged discipline; starting a fourth without first addressing why the three failed is procedurally premature. Phase 4a's operator commitment to deprioritize research applied for the duration of Phase 4a only; Phase 4d does NOT extend that commitment but also does NOT recommend reversing it without an operator-explicit motivating reason.

### 12.7 Option G — Phase 4 canonical / paper-shadow / live-readiness / exchange-write (FORBIDDEN / NOT RECOMMENDED)

**Description:** Authorize one of: Phase 4 canonical (per `phase-gates.md` Phase 4); paper/shadow (Phase 7); tiny live (Phase 8); scaled live (Phase 9); production Binance key creation; exchange-write capability; MCP / Graphify / `.mcp.json` / credentials work.

**Phase 4d view:** **Forbidden / not recommended.** Per `docs/12-roadmap/phase-gates.md`, none of these gates is met. Per Phase 3u §16.5 + Phase 3v §17.5 + Phase 3w §17.5 + Phase 3x §18.5 + Phase 4a §22 (all preserved). Strongly not recommended.

---

## 13. Rejected next slices

For clarity, Phase 4d explicitly rejects the following candidate slices (the inverse of the recommended posture):

- **Live exchange-adapter implementation.** Architectural prohibition is structural and Phase 3x §6 / §10. Forbidden.
- **Production credential handling / `.env` introduction / `.mcp.json` modification / MCP enablement / Graphify enablement.** Forbidden by `.claude/rules/prometheus-mcp-and-secrets.md` and Phase 3x §6.10 / §10.4.
- **Strategy implementation.** No V1 / R3 / R2 / F1 / D1-A code; no new strategy candidate; no strategy rescue; no 5m strategy / hybrid / retained-evidence successor / new variant. Forbidden by Phase 3o §6 + Phase 3p §8 + Phase 3r §8 + Phase 3t §13 + Phase 3u §10 + Phase 3v §13 + Phase 3w §14 + Phase 3x §6.7 + Phase 4a §22.
- **Backtest re-runs or sensitivity analyses.** No H-D3 / H-C2 / H-D5 / mark-price-stop sensitivity. Forbidden by Phase 3w §17.3 + Phase 3v §17.4.
- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. Forbidden.
- **Lock change.** §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim. Forbidden.
- **Paper/shadow runtime / live-readiness / deployment.** Per `phase-gates.md` Phase 7+, gated by prior phases; not appropriate now. Forbidden.
- **Production alerting / Telegram / n8n production routes.** Pre-tiny-live concerns per TD-019. Not authorized now.
- **Market-data ingestion at runtime.** Couples runtime to specific data shape; out of strategy-agnostic framing. Not recommended.
- **Frontend / dashboard implementation beyond the read-only state view.** Phase 5-territory; would require canonical Phase 4 strategy evidence. Forbidden.
- **Broad refactoring of Phase 4a code.** No surface-area-changing refactor is justified at this scope. Phase 4a code is clean (ruff + mypy strict + 117 tests pass). Refactoring without a concrete next-slice need is rhetorical drift toward "polish for its own sake."

---

## 14. Recommendation

**Phase 4d recommends Option A (remain paused) as primary.** Option D (docs-only reconciliation-model design memo) is acceptable as conditional secondary if the operator wishes to keep moving while staying inside docs-only discipline.

The recommendation preserves:

- **No live path.** Architectural prohibition unchanged.
- **No exchange-write.** Architectural prohibition unchanged.
- **No strategy validation claim.** No strategy is wired in; nothing in the runtime claims to validate a strategy.
- **No strategy rescue.** Retained-evidence verdicts preserved verbatim.
- **No Phase 4 canonical.** Strict-subset framing preserved.
- **No paper/shadow.** Phase 7 territory; not authorized.
- **No deployment.** No service file, no daemon, no NUC live setup.

The recommendation rejects:

- **Option E (strategy-readiness gate design memo).** Designing for a strategy that does not exist creates rhetorical drift toward strategy work; defer until a strategy is on the authorization horizon.
- **Option F (return-to-research).** Per cumulative Phase 3t / 3u / 3v / 3w / 3x / 4a recommendation; not appropriate now without operator-explicit motivating reason.
- **Option G (Phase 4 canonical / paper-shadow / live-readiness / exchange-write).** Forbidden / not recommended.

The recommendation conditionally accepts (in order of preference):

- **Option D (docs-only reconciliation-model design memo).** Lowest-risk move that produces concrete documentation value.
- **Option C (richer fake-exchange lifecycle / failure-mode test slice).** If the operator authorizes implementation work, Option C is the safest implementation slice because the architectural prohibition is enforced by code structure, not configuration.
- **Option B (structured runtime logging / audit export slice).** If the operator authorizes implementation work and prefers operator-visible value over more failure-mode coverage, Option B is acceptable but should be preceded by a docs-only design memo (analogous to Phase 3x preceding Phase 4a).

Among the conditional options, Phase 4d **prefers Option A primary** and **Option D conditional secondary** as the next move. Option C and Option B are *acceptable* implementation slices if the operator wishes to keep building, but neither is *endorsed* over Option A or Option D.

---

## 15. Operator decision menu

The operator now has a structured review of the post-4a/4b/4c boundary and seven candidate next moves. The next operator decision is operator-driven only.

### 15.1 Option A — Remain paused (PRIMARY recommendation)

Take no further action. Phase 4d's review value is realized by the memo itself; future runtime / paper / live work, if ever authorized, would inherit the safety properties (§8) and the four governance label schemes regardless. Pausing preserves operator optionality.

### 15.2 Option D — Docs-only reconciliation-model design memo (CONDITIONAL secondary)

Authorize a future docs-only memo that specifies the reconciliation contract between `RuntimeMode.RECOVERY_REQUIRED`, the runtime control persistence layer, the fake-exchange adapter (or future real adapter), and the operator-review-required flag. The memo would NOT authorize implementation; that would be a separate decision.

### 15.3 Option C — Richer fake-exchange lifecycle / failure-mode test slice (CONDITIONAL alternative)

Authorize an implementation slice that extends the fake adapter with cancel-and-replace stop lifecycle, partial fills, multiple-stop / orphaned-stop detection, stream-stale simulation, mark-price-vs-trade-price reference divergence, plus tests. Should be preceded by a docs-only scoping memo (analogous to Phase 3x → Phase 4a).

### 15.4 Option B — Structured runtime logging / audit export slice (CONDITIONAL alternative)

Authorize an implementation slice that adds JSON-Lines structured logging, a CLI export subcommand, defensive redaction, and tests. Should be preceded by a docs-only scoping memo.

### 15.5 Option E — Strategy-readiness gate design memo (NOT RECOMMENDED NOW)

Defer until a strategy is on the operator's authorization horizon. Designing now creates rhetorical drift toward strategy work.

### 15.6 Option F — Return-to-research / fresh hypothesis (NOT RECOMMENDED NOW)

Per cumulative Phase 3t / 3u / 3v / 3w / 3x / 4a recommendation. Three strategy-research arcs have framework-failed; starting a fourth now is procedurally premature.

### 15.7 Option G — Phase 4 canonical / paper-shadow / live-readiness / exchange-write (FORBIDDEN / NOT RECOMMENDED)

Per `docs/12-roadmap/phase-gates.md`, none of these gates is met. Strongly not recommended.

### 15.8 Recommendation

**Phase 4d recommends Option A (remain paused) as primary.** Option D (docs-only reconciliation-model design memo) is acceptable as conditional secondary. Options C / B are acceptable if the operator authorizes implementation work, with C preferred over B and a docs-only scoping memo required first in either case. Options E / F / G are not recommended now (E and F) or forbidden (G).

---

## 16. What this does not authorize

Phase 4d explicitly does NOT authorize, propose, or initiate any of the following:

- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 (canonical) requires Phase 3 strategy evidence which the project does not have.
- **Phase 4e or any successor phase.** Phase 4d is a docs-only review; the operator must explicitly authorize any successor.
- **Live exchange-write capability.** The architectural prohibition from Phase 4a remains: only the fake adapter exists in code; no real Binance code.
- **Production Binance keys, authenticated APIs, private endpoints, user stream, WebSocket, listenKey lifecycle, production alerting, Telegram / n8n production routes, MCP, Graphify, `.mcp.json`, credentials, exchange-write capability.** None of these is touched, enabled, or implied.
- **Strategy implementation / rescue / new candidate.** No strategy code added or modified by Phase 4d.
- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **Lock change.** §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim.
- **Data acquisition / patching / regeneration / modification.** `data/` artefacts preserved verbatim.
- **Diagnostics / Q1–Q7 rerun / backtests.** None run.
- **Phase 3v stop-trigger-domain governance modification.** Preserved verbatim.
- **Phase 3w break-even / EMA slope / stagnation governance modification.** Preserved verbatim.
- **Paper/shadow / live-readiness / deployment.** Not authorized.

Phase 4d is *docs-only review and next-slice decision* and limited to producing this memo and the accompanying closeout artefact.

---

## 17. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4e / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No implementation code written.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4d performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.**
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4d branch.** Per the Phase 4d brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 18. Remaining boundary

- **Recommended state:** **paused.**
- **Phase 4d output:** docs-only review memo + closeout artefact on the Phase 4d branch.
- **Repository quality gate state:** **fully clean.** `ruff check .` passes; pytest 785 passed; mypy strict 0 issues across 82 source files.
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged. Phase 4b and Phase 4c quality cleanups merged. Phase 4d review complete (this branch).
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by 4b / 4c / 4d).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved).
- **OPEN ambiguity-log items after Phase 4d:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4d/runtime-foundation-review-and-next-slice-decision` exists locally and (after push) on `origin/phase-4d/runtime-foundation-review-and-next-slice-decision`. NOT merged to main.

---

## 19. Next authorization status

**No next phase has been authorized.** Phase 4d's recommendation is Option A (remain paused) as primary, with Option D (docs-only reconciliation-model design memo) as conditional secondary. Options C / B (implementation slices, each preceded by a docs-only scoping memo) are acceptable conditional alternatives if the operator wishes to keep building; Options E / F are not recommended now; Option G is forbidden / not recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase 4a). The Phase 4b script-scope quality-gate restoration is complete (per Phase 4b). The Phase 4c state-package quality-gate residual cleanup is complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete on the Phase 4d branch (this phase). **Recommended state remains paused.**
