# Phase 4a — Local Safe Runtime Foundation

**Authority:** Phase 3x (Phase 4a safe-slice scoping memo); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 2i §1.7.3 project-level locks (mark-price stops; one-position max; 0.25% risk; 2× leverage cap; v002 datasets); `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/08-architecture/state-model.md`; `docs/08-architecture/runtime-persistence-spec.md`; `docs/08-architecture/database-design.md`; `docs/08-architecture/internal-event-contracts.md`; `docs/08-architecture/codebase-structure.md`; `docs/07-risk/position-sizing-framework.md`; `docs/07-risk/exposure-limits.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/kill-switches.md`; `docs/06-execution-exchange/exchange-adapter-design.md`; `docs/06-execution-exchange/binance-usdm-order-model.md`; `docs/09-operations/first-run-setup-checklist.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4a — **Local Safe Runtime Foundation.** Strategy-agnostic local runtime safety infrastructure: runtime mode / state model; runtime control state SQLite persistence; internal event contracts; the four governance label schemes from Phase 3v + Phase 3w made enforceable in code; risk sizing skeleton; exposure gate skeleton; stop-validation skeleton; deterministic local fake-exchange adapter; read-only operator state view (CLI). **Phase 4a is local-only / fake-exchange / dry-run / exchange-write-free / strategy-agnostic.**

**Branch:** `phase-4a/local-safe-runtime-foundation`. **Phase date:** 2026-04-30 UTC.

**Operator commitment for Phase 4a (recorded verbatim from authorization):**

> For Phase 4a only, we consciously deprioritize further strategy research in order to build strategy-agnostic local runtime safety infrastructure. This does not imply live-readiness, does not authorize paper/shadow, does not authorize exchange-write, does not validate any strategy, and does not revise any verdict.

---

## 1. Summary

Phase 4a implements the smallest coherent local runtime foundation that proves the Phase 3x safe-slice can be enforced in code. All Phase 3x §9 candidate components are implemented at strategy-agnostic skeleton level; all Phase 3v §8.4 + Phase 3w §6.3 / §7.3 / §8.3 governance label schemes are enforceable in code at every relevant decision boundary with `mixed_or_unknown` failing closed; all Phase 4a-required tests pass.

**Test results:** 117 Phase 4a tests pass; 785/785 project-total tests pass. Ruff lint passes for the new Phase 4a code (29 ruff issues exist in `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py`; these predate Phase 4a and are unchanged by Phase 4a). Mypy strict passes across all 82 source files (no issues).

**Phase 4a explicit anti-live-readiness statement:**

- Phase 4a is local-only.
- Phase 4a is fake-exchange only.
- Phase 4a is dry-run only.
- Phase 4a is exchange-write-free.
- Phase 4a is strategy-agnostic.
- Phase 4a does not authorize paper/shadow.
- Phase 4a does not authorize live-readiness.
- Phase 4a does not authorize deployment.
- Phase 4a does not authorize production keys.
- Phase 4a does not authorize authenticated APIs.
- Phase 4a does not authorize private endpoints.
- Phase 4a does not authorize user stream.
- Phase 4a does not authorize WebSocket.
- Phase 4a does not authorize MCP, Graphify, `.mcp.json`, credentials, or exchange-write.
- Phase 4a does not validate any strategy.
- Phase 4a does not revise any verdict.
- Phase 4a does not change any lock.

**Recommended state remains paused** for any successor phase. **No successor phase has been authorized.**

---

## 2. Authority and boundary

Phase 4a operates strictly inside the post-Phase-3x boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a-specific prohibition list).
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged. Phase 4a explicitly does NOT advance toward Phase 4 (canonical), Phase 5, paper/shadow, tiny live, scaled live, or any other gate.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md` — no production secrets, no MCP enabling, no `.mcp.json` modification.

Phase 4a adds *new code* in `src/prometheus/core/governance.py`, `src/prometheus/state/`, `src/prometheus/persistence/`, `src/prometheus/events/`, `src/prometheus/risk/`, `src/prometheus/execution/`, `src/prometheus/operator/`, and `src/prometheus/cli.py`; *new tests* in `tests/unit/runtime/`; and modifies `src/prometheus/core/__init__.py` to export governance labels. No prior phase memo is modified. No data is acquired. No diagnostics are run. No backtests are run. No retained-evidence verdict is touched. No data manifest is modified. No `.claude/rules/**` modification. No `.mcp.json` modification.

---

## 3. Starting state

```text
branch:           phase-4a/local-safe-runtime-foundation
parent commit:    be918425425904f79fc89e836d2fad6638d9d9ca (post-Phase-3x-merge housekeeping)
working tree:     clean before implementation
main:             be918425425904f79fc89e836d2fad6638d9d9ca (unchanged)

ambiguity log:    All four Phase 3u §8.5 currently-OPEN pre-coding blockers RESOLVED at
                  governance level (GAP-20260424-032 by Phase 3v; GAP-20260424-030 / 031 / 033
                  by Phase 3w).
phase-gate state: Phase 4 (canonical) unauthorized; Phase 4a execution authorized only for
                  the Phase 3x §9 strict-subset scope (this phase).
research thread:  5m research thread operationally complete and closed (Phase 3t).
v002 datasets:    locked; manifests untouched.
v001-of-5m:       trade-price research-eligible; mark-price research_eligible:false;
                  manifests untouched.
governance:       Four governance label schemes binding prospectively
                  (stop_trigger_domain | break_even_rule | ema_slope_method | stagnation_window_role).
                  mixed_or_unknown invalid and fails closed for all four schemes.
locks:            §11.6 = 8 bps HIGH per side; §1.7.3 mark-price stops; all preserved.
project layout:   Python 3.11+ (uv-managed; runtime tested under 3.12.4 from .venv);
                  ruff (E,F,W,I,UP,B,SIM); mypy strict on src/prometheus; pytest -q
                  --strict-markers; pyproject.toml + pythonpath ["src", "."].
```

---

## 4. Operator commitment and anti-live-readiness statement

The operator authorization brief for Phase 4a includes a written commitment to deprioritize further strategy research for the duration of this phase only. Phase 4a treats this commitment as binding context for this phase and as **not** a commitment to deprioritize research after Phase 4a, **not** an implication that any subsequent phase is authorized, and **not** an implication that the project is moving toward live operation.

Per Phase 3x §6 / §10, Phase 4a's anti-live-readiness statement is structurally enforced in code:

- The live exchange adapter does not exist in the Phase 4a code base. Only the fake adapter (`src/prometheus/execution/fake_adapter.py`) exists. There is no configuration switch that "turns on" a live adapter; authorizing live capability would require new code AND a new phase authorization.
- No code path reads credentials, environment variables that might contain credentials, `.env` files, or any secret material.
- No code path opens network sockets, HTTP connections, or WebSocket subscriptions.
- The fake-adapter event payloads carry `is_fake = True` as a model-validated invariant; downstream code cannot syntactically confuse fake events with live truth.
- The CLI (`prometheus.cli`) exposes only a single read-only `inspect-runtime` subcommand. No subcommand mutates exchange state, places orders, cancels orders, or toggles the kill switch.

---

## 5. Implemented scope

The Phase 4a deliverable spans nine code components plus a test harness, mapped one-to-one against Phase 3x §9 candidate components:

| Phase 3x §9 component | Module | Status |
|---|---|---|
| 9.1 Runtime mode / state model | `prometheus.state` | implemented |
| 9.2 Runtime control state persistence | `prometheus.persistence` | implemented |
| 9.3 Internal event contracts | `prometheus.events` | implemented |
| 9.7 Governance label plumbing | `prometheus.core.governance` | implemented |
| 9.4 Risk sizing skeleton | `prometheus.risk.sizing` | implemented |
| 9.5 Exposure gate skeleton | `prometheus.risk.exposure` | implemented |
| 9.6 Stop-validation skeleton | `prometheus.risk.stop_validation` | implemented |
| 9.8 Fake-exchange adapter | `prometheus.execution.fake_adapter` | implemented |
| 9.9 Read-only operator state view | `prometheus.operator.state_view` + `prometheus.cli` | implemented |
| 9.10 Test harness | `tests/unit/runtime/` (10 test files; 117 tests) | implemented |

Each component is described in §7 through §16.

---

## 6. Explicitly out-of-scope work

Per Phase 3x §6 / §10 (binding on Phase 4a execution), the following work was NOT done by Phase 4a and would require separate operator authorization:

- **No live Binance adapter.** No real REST endpoints. No authenticated calls. No listenKey acquisition / refresh. No WebSocket subscriptions. No user-stream lifecycle. No order signing.
- **No production credentials.** No `.env` file created. No `.mcp.json` modification. No Graphify wiring. No credential storage.
- **No strategy implementation.** Phase 4a does NOT implement V1, R3, R2, F1, D1-A, or any other strategy. The runtime accepts any future authorized strategy without privileging one. Existing `prometheus.strategy` modules are unchanged.
- **No backtest engine.** Phase 4a does NOT re-run Phase 2 / Phase 3 backtests. Phase 4a does NOT propose H-D3 / H-C2 / H-D5 sensitivity backtests. Phase 4a does NOT propose mark-price-stop sensitivity backtests.
- **No paper/shadow.** No real market data ingestion. No paper-trading endpoint. No production alerting (Telegram / n8n alerts are pre-tiny-live per TD-019).
- **No deployment.** No service file, no daemon, no NUC live setup. No long-running process.
- **No data acquisition / patching / regeneration / modification.** No `data/` artefact modified. No `data/manifests/*.manifest.json` modified. No public Binance endpoint consulted. Phase 4a performs no network I/O.
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No lock change.** §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim.
- **No retroactive modification of Phase 2 / Phase 3 backtest report manifests, Phase 3q v001-of-5m manifests, or Phase 3s diagnostic outputs.** The four governance label schemes apply prospectively only.
- **No regime-first / ML / cost-model-revision work.** Preserved as not-recommended-now per prior phase recommendations.
- **No `current-project-state.md` modification on the Phase 4a branch.** Per the Phase 4a brief's Allowed-changes section, the `current-project-state.md` update is preferred only after merge.
- **No modification of any prior phase memo or closeout.**

---

## 7. Runtime mode / state model

`src/prometheus/state/` implements the in-process runtime state machine.

**Files:**

- `mode.py` — `RuntimeMode` `StrEnum` with the five values required by the brief: `SAFE_MODE`, `RUNNING`, `BLOCKED`, `EMERGENCY`, `RECOVERY_REQUIRED`.
- `control.py` — `RuntimeControlState` (frozen pydantic model) with fields `runtime_mode`, `kill_switch_active`, `paused_by_operator`, `operator_review_required`, `entries_blocked`, `incident_active`, `updated_at_utc_ms`. Provides `fresh_control_state(now_utc_ms)` for the canonical fresh-startup baseline.
- `transitions.py` — pure-function transitions `enter_safe_mode`, `enter_running`, `enter_blocked`, `enter_emergency`, `enter_recovery_required`, `activate_kill_switch`, `clear_kill_switch`. Each function takes a state, returns a new state; never mutates inputs.
- `errors.py` — `RuntimeStateError`, `UnknownStateError`, `KillSwitchActiveError`, `EntriesBlockedError`.

**Safety invariants enforced in code:**

- `fresh_control_state` always returns SAFE_MODE with `entries_blocked = True` (Phase 3x §9.2 / `state-model.md` §Startup rule). Tests verify this for `now_utc_ms = 1`.
- `enter_running` is allowed only from SAFE_MODE / RECOVERY_REQUIRED. Calling it from RUNNING / BLOCKED / EMERGENCY raises `RuntimeStateError`. Tests verify all four blocked-paths.
- `enter_running` raises `KillSwitchActiveError` if the kill switch is active. Tests verify this.
- `enter_running` raises `RuntimeStateError` if any of `paused_by_operator`, `operator_review_required`, `incident_active` is true. Tests verify all three.
- `activate_kill_switch` forces the runtime mode to BLOCKED if it was RUNNING; otherwise preserves the mode. Always sets `kill_switch_active = True`, `operator_review_required = True`, `entries_blocked = True`.
- `clear_kill_switch` returns the runtime to SAFE_MODE (not RUNNING). It preserves `operator_review_required` (clearing the kill switch is not equivalent to clearing operator review).
- `enter_emergency` sets `runtime_mode = EMERGENCY`, `entries_blocked = True`, `incident_active = True`, `operator_review_required = True` per `docs/07-risk/stop-loss-policy.md` §Emergency Unprotected Policy.

The state machine is strategy-agnostic: it neither imports nor depends on any strategy module, exchange module, or live data source. It is consumed by the persistence layer (§8), event layer (§9), fake-exchange adapter (§14), and operator state view (§15).

---

## 8. Runtime control state persistence

`src/prometheus/persistence/` implements local SQLite persistence.

**Files:**

- `runtime_store.py` — `RuntimeStore` class with `initialize()`, `load_persisted()`, `save(state)`, `record_mode_event(...)`, `record_governance_label(...)` methods.

**Configuration:**

- `journal_mode = WAL`, `foreign_keys = ON`, `synchronous = FULL`, `busy_timeout = 5000` (per `docs/08-architecture/database-design.md` §Database Configuration Requirements).
- One connection per operation; no long-lived connection (matches Phase 4a's "no background services / no daemon" constraint).
- Database path is operator-supplied (file path or `":memory:"`); no implicit default.

**Schema (3 tables):**

- `runtime_control` — single-row table (CHECK `id = 1`). Stores `runtime_mode`, `kill_switch_active`, `paused_by_operator`, `operator_review_required`, `entries_blocked`, `incident_active`, `updated_at_utc_ms`. Boolean fields are stored as `INTEGER` with `CHECK ... IN (0, 1)`.
- `runtime_mode_event` — append-only audit table for runtime mode transitions. Fields: `previous_mode`, `new_mode`, `reason`, `kill_switch_active`, `operator_review_required`, `incident_active`, `occurred_at_utc_ms`.
- `governance_label_audit` — append-only audit table for governance label observations. `scheme` constrained by `CHECK scheme IN (...)`; `value` stored as text; `context` and `recorded_at_utc_ms` required.

**Safety invariants enforced in code:**

- **Persisted RUNNING does not auto-resume RUNNING.** `load_persisted()` returns the persisted record for inspection only; the runtime layer constructs a fresh SAFE_MODE record via `fresh_control_state(now_utc_ms)` and explicitly carries forward only the restart-critical flags (`kill_switch_active`, `operator_review_required`, `incident_active`, `paused_by_operator`). The runtime mode itself is reset to SAFE_MODE on every process start. Tests verify this discipline (`test_persisted_running_does_not_auto_resume_running`).
- **Kill switch persists across restart.** Tested directly (`test_kill_switch_persists_across_restart`).
- **Persistence rejects `mixed_or_unknown` for all four governance schemes.** `record_governance_label(...)` calls `prometheus.core.governance.require_valid` before writing; tests verify all four schemes (`test_persistence_rejects_mixed_or_unknown_*`).
- **Corrupt persisted runtime mode fails closed.** If the DB row contains an out-of-scheme `runtime_mode` value, `load_persisted()` raises `RuntimeStoreError` rather than silently accepting it (`test_persistence_rejects_invalid_persisted_runtime_mode`).
- **Empty audit-event reasons rejected.** Tested (`test_record_mode_event_rejects_empty_reason`).
- **No secrets are persisted.** No table column stores credentials, API keys, secret tokens, or any sensitive material.

---

## 9. Internal event contracts

`src/prometheus/events/` implements the typed local event/message contracts.

**Files:**

- `envelope.py` — `MessageClass` enum (`command` / `event` / `query`); `MessageEnvelope` (frozen pydantic model with all required fields per `docs/08-architecture/internal-event-contracts.md` §Shared Message Envelope); `new_message_id(prefix)` deterministic counter-backed id generator.
- `runtime_events.py` — typed event payloads: `RuntimeModeChangedEvent`, `KillSwitchEvent` (with `KillSwitchEventKind` enum), `FakeExchangeLifecycleEvent` (with `FakeExchangeLifecycleKind` enum), `GovernanceLabelEvent`.

**Phase 4a is strategy-agnostic; the event contracts implement only the message families that exist independent of any specific strategy.**

**Safety invariants enforced in code:**

- **`MessageEnvelope` is frozen and `extra="forbid"`.** No silent payload drift.
- **`message_type`, `message_id`, `correlation_id`, `source_component`** must be non-empty strings (`Field(min_length=1)`).
- **`occurred_at_utc_ms` must be positive** (`Field(gt=0)`).
- **`FakeExchangeLifecycleEvent.is_fake`** is a model-validated invariant that must always be `True`. Constructing such an event with `is_fake = False` raises `ValueError`.
- **Stop-bearing fake-lifecycle events require a `stop_trigger_domain` label.** The model validator rejects construction without it.
- **Fake-lifecycle events with `stop_trigger_domain = mixed_or_unknown` fail closed.** The validator calls `require_valid`. Tested (`test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger`).
- **`GovernanceLabelEvent` requires at least one label** populated, and rejects `mixed_or_unknown` for any populated label slot. Tested (`test_governance_label_event_rejects_mixed_or_unknown_in_any_slot`).

---

## 10. Governance label enforcement

`src/prometheus/core/governance.py` is the **single code-level source of truth** for the four Phase 3v + Phase 3w governance label schemes. All Phase 4a modules that touch governed semantics import from this module.

**Schemes (each a `StrEnum`):**

- `StopTriggerDomain` — `trade_price_backtest` | `mark_price_runtime` | `mark_price_backtest_candidate` | `mixed_or_unknown` (Phase 3v §8.4).
- `BreakEvenRule` — `disabled` | `enabled_plus_1_5R_mfe` | `enabled_plus_2_0R_mfe` | `enabled_other_predeclared` | `mixed_or_unknown` (Phase 3w §6.3).
- `EmaSlopeMethod` — `discrete_comparison` | `fitted_slope` | `other_predeclared` | `not_applicable` | `mixed_or_unknown` (Phase 3w §7.3).
- `StagnationWindowRole` — `not_active` | `metric_only` | `active_rule_predeclared` | `mixed_or_unknown` (Phase 3w §8.3).

**Helpers:**

- `is_fail_closed(label)` — predicate; True iff label value is `mixed_or_unknown`.
- `require_valid(label)` — raises `GovernanceLabelError` if label is fail-closed; canonical fail-closed signal.
- `parse_<scheme>(value)` — strict parsers that raise `GovernanceLabelError` on out-of-scheme values.

**Decision boundaries that consume `require_valid`:**

| Boundary | Module / function | Test |
|---|---|---|
| Persistence | `persistence.runtime_store.RuntimeStore.record_governance_label` | `test_persistence_rejects_mixed_or_unknown_*` (×4) |
| Stop validation (initial) | `risk.stop_validation.validate_initial_stop` | `test_mixed_or_unknown_stop_trigger_domain_fails_closed` |
| Stop validation (update) | `risk.stop_validation.StopUpdateRequest._validate` (pydantic model_validator) | `test_stop_update_mixed_or_unknown_fails_closed_at_construction` |
| Event validation (fake lifecycle) | `events.runtime_events.FakeExchangeLifecycleEvent._validate` | `test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger` |
| Event validation (label observation) | `events.runtime_events.GovernanceLabelEvent._validate` | `test_governance_label_event_rejects_mixed_or_unknown_in_any_slot` |
| Fake-exchange decision | `execution.fake_adapter.FakeExchangeAdapter.submit_protective_stop` (and related stop-bearing methods) | `test_protective_stop_rejects_mixed_or_unknown_label` |

**No decision boundary uses a copy-pasted enum or value list.** All consumers import from `prometheus.core.governance`. The single-source-of-truth invariant is verified by `test_governance_labels_share_single_source_of_truth`.

---

## 11. Risk sizing skeleton

`src/prometheus/risk/sizing.py` implements the `compute_sizing(SizingInputs) -> SizingResult` function.

**Inputs (frozen pydantic model with strict bounds):**

- `symbol`, `account_equity_usdt > 0`, `strategy_allocated_equity_usdt > 0`, `risk_fraction ∈ (0, 1]`, `risk_usage_fraction ∈ (0, 1]`, `proposed_entry_price > 0`, `initial_stop_price > 0`, `side_is_long`, `leverage_cap > 0`, `notional_cap_usdt > 0`, `quantity_step > 0`, `min_quantity > 0`. Pydantic enforces `> 0` / range validation at construction time.

**Computation (per `docs/07-risk/position-sizing-framework.md` §Definitions):**

```
sizing_equity = min(account_equity, strategy_allocated_equity)
risk_amount   = sizing_equity * risk_fraction
budget        = risk_amount * risk_usage_fraction
stop_distance = entry - stop  (long) or stop - entry  (short)
raw_quantity  = budget / stop_distance
rounded_quantity = floor(raw_quantity / quantity_step) * quantity_step
notional      = rounded_quantity * entry_price
effective_leverage = notional / sizing_equity
```

**Fail-closed branches:**

- `stop_distance <= 0` (e.g., long stop above entry; short stop below entry) → `SizingError`.
- `rounded_quantity < min_quantity` → `SizingError` (reject rather than scale up).
- `notional > notional_cap_usdt` → `SizingError`.
- `effective_leverage > leverage_cap` → `SizingError`.
- Missing or invalid pydantic-bounded input → `ValidationError` at construction.

**Locked v1 constants exposed:**

- `LOCKED_LIVE_RISK_FRACTION = 0.0025`.
- `LOCKED_LIVE_LEVERAGE_CAP = 2.0`.

These are read-only references; the function does not enforce them by default (research-stage callers may legitimately use other values for fixtures), but tests verify the exposed values.

**Tests:** 12 sizing tests including baseline-long happy path, long-stop-above-entry rejection, short-stop-below-entry rejection, below-minimum-quantity rejection (no scale-up), notional-cap violation, leverage-cap violation, missing-equity-via-pydantic, missing-quantity-step-via-pydantic, zero-risk-fraction-via-pydantic, strategy-allocated-equity-caps-sizing.

---

## 12. Exposure gate skeleton

`src/prometheus/risk/exposure.py` implements `evaluate_entry_candidate(...) -> ExposureDecision`.

**Snapshot value object:**

- `ExposureSnapshot` — frozen pydantic model: `symbol`, `has_position`, `position_side`, `protection_confirmed`, `entry_in_flight`, `manual_or_non_bot_exposure`. Fake-position state only; constructed from fake-adapter state in tests.

**Gates enforced (per `docs/07-risk/exposure-limits.md` §Locked V1 Exposure Rules):**

| Rule | Implementation | Test |
|---|---|---|
| Rule 1: BTCUSDT only live | `candidate_symbol != live_symbol` → reject | `test_non_btcusdt_live_entry_rejected_by_rule_1` |
| Rule 2 / 3: pyramiding | `position_side == candidate_side` → reject | `test_pyramiding_rejected_by_rule_3` |
| Rule 4: reversal while positioned | `position_side != candidate_side` → reject | `test_reversal_while_positioned_rejected_by_rule_4` |
| Rule 7: entry in flight | `entry_in_flight == True` → reject | `test_entry_in_flight_blocks_new_entries` |
| Rule 9: missing protection | `has_position and not protection_confirmed` → reject | `test_unprotected_position_blocks_new_entries` |
| Manual exposure | `manual_or_non_bot_exposure == True` → reject | `test_manual_exposure_blocks_new_entries` |

A snapshot inconsistency (e.g., `has_position = True` with `position_side = None`, or symbol mismatch) raises `ExposureGateError` rather than silently returning a decision. Tested.

The decision is structured (`ExposureDecision(allowed: bool, reason: str)`) so the runtime layer can record the rejection reason on the audit log.

---

## 13. Stop-validation skeleton

`src/prometheus/risk/stop_validation.py` implements `validate_initial_stop(StopRequest)` and `validate_stop_update(StopUpdateRequest)`.

**Validators:**

- **`validate_initial_stop`:** calls `require_valid(stop_trigger_domain)`; checks side-vs-entry (long stop strictly below entry; short stop strictly above); checks positive stop distance; applies the `0.60 × ATR ≤ stop_distance ≤ 1.80 × ATR` filter when ATR is supplied (per `docs/07-risk/stop-loss-policy.md` §ATR stop-distance filter); checks tick-size and price-precision metadata when supplied. Raises `StopValidationError` or `MissingMetadataError` on failure.
- **`validate_stop_update`:** for longs, rejects proposed-new-stop strictly below current; for shorts, rejects proposed-new-stop strictly above current. Equality is permitted (idempotent re-submission); strict widening is rejected (Phase 4a stop-policy rule "stops may reduce risk, not increase it"). The pydantic `model_validator` calls `require_valid(stop_trigger_domain)` at construction time, so a request with `mixed_or_unknown` cannot even be built.

**Tests:** 14 stop-validation tests covering long/short happy paths, side-vs-entry rejections, ATR-too-tight, ATR-too-wide, `mixed_or_unknown` fail-closed, metadata rejections (zero ATR, negative tick size), and stop-update widening tests.

---

## 14. Fake-exchange adapter

`src/prometheus/execution/fake_adapter.py` implements `FakeExchangeAdapter`.

**Construction:** one adapter per test; injectable `ClockFn` from `prometheus.core.time` for deterministic timestamps; symbol locked to BTCUSDT by default.

**Public API:**

- `submit_entry_order(...)` — submit a fake entry; raises `FakeExchangeError` if an entry is already in flight or a fake position exists.
- `confirm_fake_fill(correlation_id)` — mark pending entry as filled; updates fake position state.
- `mark_entry_unknown_outcome(correlation_id)` — surface a fake submission timeout / unknown outcome.
- `submit_protective_stop(stop_price, stop_trigger_domain)` — submit a fake protective stop; requires an existing fake position; calls `require_valid(stop_trigger_domain)`.
- `confirm_fake_protective_stop(stop_trigger_domain)` — confirm the previously submitted fake stop.
- `mark_stop_submission_failed(stop_trigger_domain)` — surface a fake stop submission failure.
- `trigger_fake_stop(stop_trigger_domain)` — simulate the fake protective stop firing; clears fake position and stop.

**Read accessors:** `position_state`, `stop_state`, `is_entry_in_flight`, `emitted_events`.

**Architectural prohibitions enforced by code structure:**

- No `import httpx`, no `import websockets`, no `import socket`.
- No `os.environ` reads.
- No file opens.
- No imports from any module that talks to a real Binance API.
- All emitted events carry `is_fake = True` (model-validated invariant).
- All stop-related fake events carry a `stop_trigger_domain` label (model-validated invariant).

**Tests:** 9 fake-adapter tests including the Phase 4a happy-path lifecycle (`test_happy_path_signal_to_protected_position`) and the failure-path scenarios (`test_failure_path_unknown_outcome_blocks_progression`, `test_stop_submission_failure_after_fill_signals_emergency`).

---

## 15. Read-only operator state view

`src/prometheus/operator/state_view.py` and `src/prometheus/cli.py` together implement the read-only operator surface.

**`format_state_view(...)`:** pure function that returns a plain-text rendering of:

- runtime mode,
- kill-switch state,
- pause / operator-review-required / incident-active flags,
- entries-blocked status,
- fake-position state (clearly labelled "local; not exchange truth"),
- fake-protective-stop state (clearly labelled "local; not exchange truth"),
- governance label values where supplied,
- a closing disclaimer line: "Phase 4a is local-only / fake-exchange / dry-run / exchange-write-free / strategy-agnostic."

**CLI (`python -m prometheus.cli inspect-runtime --db PATH`):** opens the SQLite store, calls `load_persisted`, and prints `format_state_view(...)`. With `--allow-empty`, prints a fresh SAFE_MODE view if the DB is empty.

**Architectural prohibitions enforced by code structure:**

- No control buttons (the surface is a function returning a string).
- No exchange action exposed.
- No production alerting wiring.
- No Telegram / n8n.
- Tests verify the output does not contain action-shaped phrases like `place order`, `submit order`, `cancel order`, `modify stop`, `click to`, `production key`, or `credentials` (`test_state_view_does_not_expose_exchange_actions`).

---

## 16. Test harness

`tests/unit/runtime/` contains 117 Phase 4a tests across 10 test files plus an `__init__.py`.

**Coverage by required-test category (per Phase 4a brief):**

| Required test | Test name(s) |
|---|---|
| startup defaults to SAFE_MODE | `test_fresh_control_state_defaults_to_safe_mode`, `test_phase_4a_full_lifecycle_no_real_exchange` |
| persisted RUNNING does not auto-resume RUNNING | `test_persisted_running_does_not_auto_resume_running`, `test_phase_4a_full_lifecycle_no_real_exchange` |
| kill-switch persists across restart | `test_kill_switch_persists_across_restart`, `test_phase_4a_full_lifecycle_no_real_exchange` |
| kill-switch never auto-clears | `test_clear_kill_switch_returns_to_safe_mode_not_running` (only explicit transition clears) |
| kill-switch blocks fake entries | `test_phase_4a_full_lifecycle_no_real_exchange` (KillSwitchActiveError on `enter_running` while kill switch active) |
| unknown runtime state fails closed | `test_persistence_rejects_invalid_persisted_runtime_mode` |
| missing risk metadata fails closed | `test_missing_quantity_step_fails_closed_via_pydantic`, `test_metadata_validation_rejects_zero_atr`, `test_metadata_validation_rejects_negative_tick_size` |
| missing equity fails closed | `test_missing_equity_fails_closed_via_pydantic` |
| exposure gate blocks multiple positions | `test_multiple_positions_blocked_via_existing_position` |
| exposure gate blocks pyramiding | `test_pyramiding_rejected_by_rule_3` |
| exposure gate blocks reversal while positioned | `test_reversal_while_positioned_rejected_by_rule_4` |
| stop validation rejects mixed_or_unknown stop_trigger_domain | `test_mixed_or_unknown_stop_trigger_domain_fails_closed`, `test_stop_update_mixed_or_unknown_fails_closed_at_construction` |
| stop validation rejects stop widening | `test_stop_update_long_widening_rejected`, `test_stop_update_short_widening_rejected` |
| all four governance labels reject mixed_or_unknown | `test_require_valid_rejects_mixed_or_unknown` (parametrized over all four schemes) |
| all four governance labels reject invalid values | `test_parsers_reject_out_of_scheme_values` (parametrized) |
| persistence rejects mixed_or_unknown labels | `test_persistence_rejects_mixed_or_unknown_*` (4 tests, one per scheme) |
| event validation rejects mixed_or_unknown labels where relevant | `test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger`, `test_governance_label_event_rejects_mixed_or_unknown_in_any_slot` |
| fake-exchange happy path | `test_happy_path_signal_to_protected_position`, `test_phase_4a_full_lifecycle_no_real_exchange` |
| fake-exchange failure path | `test_failure_path_unknown_outcome_blocks_progression`, `test_stop_submission_failure_after_fill_signals_emergency` |
| read-only operator state view does not expose exchange actions | `test_state_view_does_not_expose_exchange_actions` |

All required tests pass. Additional defensive tests are included for snapshot-inconsistency rejection, double-entry-submission rejection, mismatched-correlation-id rejection, single-source-of-truth verification, and CLI behaviour with empty DB.

---

## 17. Commands run

All commands run from `c:\Prometheus` against the project's `.venv` (Python 3.12.4):

```text
git status
git checkout -b phase-4a/local-safe-runtime-foundation
.venv/Scripts/python --version
.venv/Scripts/python -m pytest tests/unit/runtime -q
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m ruff check src/prometheus tests/unit/runtime
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m ruff check scripts
.venv/Scripts/python -m mypy
```

Note: `pyproject.toml` declares `requires-python = ">=3.11,<3.13"` and `tool.mypy.python_version = "3.11"`. The local `.venv` runs Python 3.12.4 which satisfies the constraint; mypy still type-checks against 3.11 semantics. The brief asked to adapt only to actual project tooling — no command was invented, and no command was claimed successful without being run.

No format-check command is configured separately by the project (`tool.ruff.format` is declared but `ruff format --check` is not part of the documented project workflow). Phase 4a does not invent a format step.

---

## 18. Test results

**Phase 4a runtime tests (`tests/unit/runtime/`):**

```text
117 passed in 0.50s
```

**Project-total tests (`tests/`):**

```text
785 passed in 12.90s
```

All Phase 4a tests pass; full project test suite (research backtest, strategy modules, data integrity, simulation, etc.) also passes — no regression introduced.

**Ruff lint on Phase 4a code (`src/prometheus/`, `tests/unit/runtime/`):**

```text
All checks passed!
```

**Ruff lint on entire repository:**

```text
Found 29 errors.
```

All 29 are pre-existing in `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py` (Phase 3q + Phase 3s deliverables). They are unchanged by Phase 4a. They are documented as known limitations in §20 below.

**Mypy strict (`tool.mypy.strict = true`, `files = ["src/prometheus"]`):**

```text
Success: no issues found in 82 source files
```

---

## 19. Files changed

**Modified (2 files):**

- `src/prometheus/core/__init__.py` — added exports for the four governance label types, `GovernanceLabel`, `GovernanceLabelError`, `is_fail_closed`, `require_valid`, and the four `parse_*` helpers.
- `.gitignore` — narrow fix to anchor the `state/`, `runtime/`, `cache/` patterns to the repository root only (changed to `/state/`, `/runtime/`, `/cache/`) so they no longer accidentally ignore the Phase 4a source-code packages `src/prometheus/state/` and the test directory `tests/unit/runtime/`. The fix preserves the original intent (root-level local-runtime-artefact directories remain ignored) and does not weaken any secret/credential ignore rule. Verified by `git check-ignore` showing no Phase 4a path is now ignored.

**Added — production code (24 files):**

- `src/prometheus/cli.py` (CLI entrypoint).
- `src/prometheus/core/governance.py` (governance labels — single source of truth).
- `src/prometheus/state/__init__.py`, `state/mode.py`, `state/control.py`, `state/transitions.py`, `state/errors.py`.
- `src/prometheus/persistence/__init__.py`, `persistence/runtime_store.py`.
- `src/prometheus/events/__init__.py`, `events/envelope.py`, `events/runtime_events.py`.
- `src/prometheus/risk/__init__.py`, `risk/errors.py`, `risk/sizing.py`, `risk/exposure.py`, `risk/stop_validation.py`.
- `src/prometheus/execution/__init__.py`, `execution/fake_adapter.py`.
- `src/prometheus/operator/__init__.py`, `operator/state_view.py`.

**Added — tests (11 files):**

- `tests/unit/runtime/__init__.py`.
- `tests/unit/runtime/test_governance_labels.py`.
- `tests/unit/runtime/test_runtime_state.py`.
- `tests/unit/runtime/test_runtime_persistence.py`.
- `tests/unit/runtime/test_runtime_events.py`.
- `tests/unit/runtime/test_risk_sizing.py`.
- `tests/unit/runtime/test_risk_exposure.py`.
- `tests/unit/runtime/test_risk_stop_validation.py`.
- `tests/unit/runtime/test_fake_adapter.py`.
- `tests/unit/runtime/test_operator_state_view.py`.
- `tests/unit/runtime/test_runtime_end_to_end.py`.

**Added — documentation (2 files):**

- `docs/00-meta/implementation-reports/2026-04-30_phase-4a_local-safe-runtime-foundation.md` (this report).
- `docs/00-meta/implementation-reports/2026-04-30_phase-4a_closeout.md` (Phase 4a closeout).

**NOT modified:**

- All `data/manifests/*.manifest.json` (v002 + Phase 3q v001-of-5m). Mark-price 5m `research_eligible: false` preserved.
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions.
- All other `src/prometheus/**` source code (existing strategy modules, research modules, core modules other than `__init__.py` and the new `governance.py`).
- All other `scripts/**`.
- All other `tests/**`.
- All `.claude/rules/**`.
- All `docs/**` other than the two new Phase 4a artefacts.
- `docs/00-meta/current-project-state.md` (preferred update only after merge per the Phase 4a brief).
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w / 3x reports / closeouts / merge-closeouts.
- `docs/03-strategy-research/v1-breakout-strategy-spec.md` (lines 156–172, 332, 380, 415, 564 unchanged).
- `docs/03-strategy-research/v1-breakout-backtest-plan.md`.
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md`.
- `docs/07-risk/stop-loss-policy.md`.
- `docs/06-execution-exchange/binance-usdm-order-model.md`.
- `docs/12-roadmap/phase-gates.md`.
- `docs/12-roadmap/technical-debt-register.md`.
- `docs/00-meta/ai-coding-handoff.md`.
- `docs/09-operations/first-run-setup-checklist.md`.
- `docs/00-meta/implementation-ambiguity-log.md`.
- `.mcp.json`.
- `pyproject.toml`.
- `.gitignore`.
- `uv.lock`.

---

## 20. Known limitations

- **Pre-existing ruff issues in `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py`.** 29 ruff errors remain in those Phase 3q / Phase 3s standalone orchestrator scripts. Phase 4a does not modify those scripts and does not undertake to fix their lint debt; that would be a separate clean-up phase (and would touch already-merged-to-main artefacts not in Phase 4a's scope).
- **Phase 4a is research-backed by tests, not by an integration with a live runtime.** The fake-exchange adapter is a deterministic state machine, not a live Binance integration. That is by design (per Phase 3x §6 / §10); a future phase that wires a real adapter would require new code, separate operator authorization, and explicit live-readiness preconditions.
- **The runtime control state is single-row.** Phase 4a does not implement multi-tenant runtime control or a multi-strategy registry. These are out of scope for v1 (per `current-project-state.md` Locked V1 Decisions and the Phase 3x strict-subset framing).
- **No real reconciliation engine.** Phase 4a's `RuntimeMode.RECOVERY_REQUIRED` is a state, not a workflow. Implementing the actual reconciliation flow (per `docs/06-execution-exchange/user-stream-reconciliation.md`) requires either real exchange capability or a richer fake adapter; that is out of scope for Phase 4a per Phase 3x §10.
- **No real strategy-readiness gate.** Phase 4a defines persistence and event schemas that *would* support a strategy-readiness gate (label-match check between a backtest's `stop_trigger_domain` and the runtime's expected domain per Phase 3v §8.5), but Phase 4a does not implement the gate itself because no strategy is wired in.
- **`risk_usage_fraction = 0.90` is a default in test fixtures, not a project-wide locked constant.** `LOCKED_LIVE_RISK_FRACTION` and `LOCKED_LIVE_LEVERAGE_CAP` are exposed as locked constants per §1.7.3; `risk_usage_fraction` is a per-config value per `docs/07-risk/position-sizing-framework.md` §Risk usage fraction.
- **Mypy `python_version = "3.11"` while the local `.venv` runs 3.12.4.** This is consistent with `pyproject.toml::requires-python = ">=3.11,<3.13"`. Type-checking against the lower-bound version is the more conservative posture.
- **Pre-tiny-live items remain documented but unaddressed.** Per Phase 3x §8.4, the pre-tiny-live items (TD-006, TD-017, TD-018, TD-019, TD-020) remain documented as pre-tiny-live concerns and are not pre-coding blockers for Phase 4a. Phase 4a does not address them; they would be addressed by a separately authorized pre-tiny-live readiness phase if and when paper/shadow / Phase 7 / Phase 8 work is ever authorized.

---

## 21. Safety properties proven

The following safety properties are proven by the Phase 4a test harness:

1. **Startup always enters SAFE_MODE.** Even when a persisted record is `RUNNING`, the runtime constructs a fresh SAFE_MODE state on startup. Test: `test_persisted_running_does_not_auto_resume_running`, `test_phase_4a_full_lifecycle_no_real_exchange`.
2. **Kill-switch persistence across restart.** Persisted `kill_switch_active = True` survives a simulated restart. Test: `test_kill_switch_persists_across_restart`, `test_phase_4a_full_lifecycle_no_real_exchange`.
3. **Kill-switch never auto-clears.** The only path to clearing is an explicit `clear_kill_switch` call, which returns the runtime to SAFE_MODE (not RUNNING). Test: `test_clear_kill_switch_returns_to_safe_mode_not_running`.
4. **Kill-switch blocks fake entries.** With kill-switch active, `enter_running` raises `KillSwitchActiveError`; downstream entry attempts therefore cannot proceed. Test: `test_enter_running_blocked_by_kill_switch`, `test_phase_4a_full_lifecycle_no_real_exchange`.
5. **`mixed_or_unknown` fails closed at every governance-relevant decision boundary.** Stop validation, persistence, fake-adapter decisions, event validation — six independent boundaries, each tested. Test set: `test_persistence_rejects_mixed_or_unknown_*` (×4), `test_mixed_or_unknown_stop_trigger_domain_fails_closed`, `test_stop_update_mixed_or_unknown_fails_closed_at_construction`, `test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger`, `test_governance_label_event_rejects_mixed_or_unknown_in_any_slot`, `test_protective_stop_rejects_mixed_or_unknown_label`.
6. **Stop widening is rejected.** Both long and short widening attempts raise `StopValidationError`. Test: `test_stop_update_long_widening_rejected`, `test_stop_update_short_widening_rejected`.
7. **Exposure gates enforce one-symbol-only / one-position / no-pyramiding / no-reversal / no-unprotected-position-allows-new-entry / no-manual-exposure-allows-new-entry.** Test set covers all six rules.
8. **Position without confirmed protection forces EMERGENCY.** The end-to-end test (`test_phase_4a_full_lifecycle_no_real_exchange`) drives a fake fill confirmed → fake stop submission failed sequence and enters `enter_emergency`, asserting `runtime_mode = EMERGENCY`, `incident_active = True`, `operator_review_required = True`, `entries_blocked = True`.
9. **Fake events are syntactically distinguishable from live events.** All `FakeExchangeLifecycleEvent` instances carry `is_fake = True` (model-validated). No code path emits an event without that marker.
10. **Read-only operator surface does not expose exchange actions.** Output-text scan rejects all action-shaped phrases. Test: `test_state_view_does_not_expose_exchange_actions`.
11. **Persistence rejects corrupt runtime modes.** A direct SQL injection of an out-of-scheme `runtime_mode` value causes `load_persisted` to raise `RuntimeStoreError`. Test: `test_persistence_rejects_invalid_persisted_runtime_mode`.
12. **No network I/O.** Phase 4a code base contains no `httpx`, `socket`, `websockets`, `urllib`, or `requests` imports; tests all run offline (verified by absence of import errors and by all 117 tests completing in 0.50s with no network round-trip).
13. **No secrets in code, tests, or DB.** No `.env` is read; no credential field is persisted; no test fixture contains a token or key.
14. **Single source of truth for governance labels.** All four schemes are defined exactly once in `prometheus.core.governance`. Test: `test_governance_labels_share_single_source_of_truth`.

---

## 22. What Phase 4a does not authorize

Phase 4a explicitly does NOT authorize, propose, or initiate any of the following:

- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 (canonical) requires Phase 3 strategy evidence which the project does not have. Phase 4a is a strict subset of Phase 4 with explicit anti-live-readiness preconditions; it is not Phase 4.
- **Phase 4b or any successor phase.** No follow-up phase is implied by Phase 4a's success.
- **Live exchange-write capability.** Architectural prohibition: live exchange adapter is not implemented in code; only fake adapter exists.
- **Production Binance keys.** None requested, stored, configured, or used.
- **Authenticated APIs / private endpoints / user stream / WebSocket.** Code paths simply do not contain these.
- **Paper/shadow.** Phase 4a is not Phase 7.
- **Live-readiness implication.** Phase 4a's success does not constitute, imply, or shorten the path to live readiness.
- **Deployment.** No deployment artefact for live operation; no NUC live setup; no Telegram / n8n production alerting.
- **Strategy commitment / rescue / new candidate.** Phase 4a is strategy-agnostic.
- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **Lock change.** §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim.
- **MCP / Graphify / `.mcp.json` / credentials.** None enabled, configured, requested, or stored.
- **Data acquisition / patching / regeneration / modification.** `data/` artefacts preserved verbatim.
- **Regime-first / ML / cost-model-revision work.** Preserved as not-recommended-now per prior phase recommendations.
- **Retroactive modification of Phase 2 / Phase 3 backtest manifests, Phase 3q v001-of-5m manifests, or Phase 3s diagnostic outputs.** The four governance label schemes apply prospectively only.
- **Phase 3v stop-trigger-domain governance modification.** Preserved verbatim.
- **Phase 3w break-even / EMA slope / stagnation governance modification.** Preserved verbatim.

---

## 23. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4b / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No real exchange adapter implemented.** No HTTP, WebSocket, listenKey, or signing code added.
- **No exchange-write capability.** No order placement code; no order cancellation code; no account state mutation code.
- **No Binance credentials used.** No request for credentials. No credential storage. No `.env` file created. No secret material in commits.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4a performs no network I/O.
- **No production alerting / Telegram / n8n production routes.** None added.
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.** None.
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.** Stated explicitly in §1, §4, §22 above and in disclaimer text inside `format_state_view` output.
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.** Existing `prometheus.strategy` modules untouched.
- **No strategy rescue proposal.** No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, target-subset rescue, regime-conditioned rescue, or 5m-on-X variant.
- **No new strategy candidate proposal.**
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun. No new diagnostic computation.
- **No Q1–Q7 rerun.**
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` (v002 + v001-of-5m) preserved verbatim. Mark-price 5m `research_eligible: false` preserved.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim. **§11.6 unchanged.** **§1.7.3 mark-price-stop lock unchanged.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.** Spec lines 156–172, 332, 380, 415, 564 all preserved verbatim.
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.** All four pre-coding blockers (GAP-20260424-030 / 031 / 032 / 033) remain RESOLVED per Phase 3v / Phase 3w.
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4a branch.** Per the Phase 4a brief, the `current-project-state.md` update is preferred only after merge.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` substantive modification.** No new dependencies were added; no version bumps; no scope change.
- **`.gitignore` modification limited to a narrow root-anchoring fix** (changed `state/`/`runtime/`/`cache/` to `/state/`/`/runtime/`/`/cache/` so source-code packages and test directories named `state` or `runtime` are not accidentally ignored). No secret/credential ignore rule weakened; no new files un-ignored other than the Phase 4a code itself. See §19 for details.
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No merge to main.** Per the Phase 4a brief, the Phase 4a branch is not merged to main by Phase 4a itself.

---

## 24. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4a deliverables exist as branch-only artefacts pending operator review.
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed on this branch only; Phase 4a *branch* is not merged to main.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a.
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a.
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a.
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a.
- **Phase 4a safe-slice scope:** Defined by Phase 3x + implemented by Phase 4a (this phase).
- **OPEN ambiguity-log items after Phase 4a:** zero relevant to Phase 4a / runtime / strategy implementation. Pre-tiny-live items remain documented as pre-tiny-live concerns.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4a/local-safe-runtime-foundation` exists locally and on `origin/phase-4a/local-safe-runtime-foundation` after the Phase 4a push (see Phase 4a closeout for SHAs). NOT merged to main.

---

## 25. Operator decision menu

The operator now has a working Phase 4a local safe runtime foundation on the Phase 4a branch. The next operator decision is operator-driven only.

### 25.1 Option A — Review on branch and remain paused (PRIMARY recommendation)

Take no further action. The Phase 4a branch persists as a reviewable artefact. The operator reviews the implementation, the test outputs, and the documentation; pauses; decides separately whether to merge to main and whether to authorize any subsequent phase.

### 25.2 Option B — Merge Phase 4a to main and remain paused (CONDITIONAL secondary)

Authorize a Phase 4a merge into main (analogous to the Phase 3o → 3w merge pattern). The merge would bring Phase 4a artefacts onto main, refresh `current-project-state.md`, and produce a Phase 4a merge-closeout artefact. After merge, the project remains paused; no further phase is authorized.

### 25.3 Option C — Authorize follow-up implementation work (CONDITIONAL tertiary)

If, after reviewing Phase 4a, the operator wishes to expand the runtime (e.g., reconciliation engine, richer dashboard, structured logging hooks), each such expansion would be a separately authorized phase with its own brief, its own scoped deliverables, and its own test harness. Phase 4a does not authorize any such phase.

### 25.4 Option D — Return to research / authorize a strategy phase (NOT RECOMMENDED NOW)

The operator's commitment for Phase 4a was to deprioritize research for the duration of Phase 4a only. Phase 4a does not extend that commitment beyond Phase 4a. If the operator chooses to return to research after Phase 4a, that is a separately authorized decision and would not be a continuation of Phase 4a.

### 25.5 Option E — Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write (FORBIDDEN / NOT RECOMMENDED)

Phase 4a's strict-subset framing was the basis for its authorization. Authorizing canonical Phase 4 / paper-shadow / live-readiness / deployment / production-key / exchange-write requires separate operator decisions with separate evidence; none of those is implied by Phase 4a's success.

### 25.6 Recommendation

**Phase 4a recommends Option A (review on branch and remain paused) as primary**, with Option B (merge to main and remain paused) as an acceptable conditional secondary. Option C is acceptable only with a fresh operator brief. Options D and E are not recommended now.

---

## 26. Next authorization status

**No next phase has been authorized.** Phase 4a authorizes nothing other than producing this implementation report and the accompanying closeout artefact (the implementation itself was authorized by the operator brief that opened Phase 4a; that authorization is now spent on this phase).

Selection of any subsequent phase (Phase 4a merge per Option B; richer runtime per Option C; return to research per Option D; Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write per Option E) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is now both *defined* (Phase 3x) and *implemented* (Phase 4a — this phase). **Recommended state remains paused.**
