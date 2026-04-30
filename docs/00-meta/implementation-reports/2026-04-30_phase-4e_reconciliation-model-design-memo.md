# Phase 4e — Reconciliation-Model Design Memo (docs-only)

**Authority:** Phase 4d §16 (operator selection of Option D — docs-only reconciliation-model design memo); Phase 4a (Local Safe Runtime Foundation); Phase 4b/4c (Repository Quality Gate Restoration); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 3x §6 / §10 (Phase 4a strict-subset framing); Phase 2i §1.7.3 project-level locks; `docs/12-roadmap/phase-gates.md`; `docs/12-roadmap/technical-debt-register.md`; `docs/00-meta/ai-coding-handoff.md`; `docs/00-meta/implementation-ambiguity-log.md`; `docs/08-architecture/state-model.md`; `docs/08-architecture/runtime-persistence-spec.md`; `docs/08-architecture/internal-event-contracts.md`; `docs/08-architecture/database-design.md`; `docs/08-architecture/implementation-blueprint.md`; `docs/06-execution-exchange/exchange-adapter-design.md`; `docs/06-execution-exchange/user-stream-reconciliation.md`; `docs/06-execution-exchange/binance-usdm-order-model.md`; `docs/07-risk/kill-switches.md`; `docs/07-risk/exposure-limits.md`; `docs/07-risk/stop-loss-policy.md`; `docs/07-risk/position-sizing-framework.md`; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4e — **Reconciliation-Model Design Memo** (docs-only). Defines the future reconciliation model for the local safe runtime foundation: how a future reconciliation engine would classify and recover from local/fake/exchange state mismatches, how it would interact with `RuntimeMode.RECOVERY_REQUIRED`, runtime control persistence, the fake-exchange adapter, operator-review-required flags, kill switches, and fail-closed behaviour.

**Branch:** `phase-4e/reconciliation-model-design-memo`. **Memo date:** 2026-04-30 UTC.

**Phase 4e does NOT implement reconciliation. Phase 4e does NOT start Phase 4 canonical. Phase 4e does NOT authorize paper/shadow. Phase 4e does NOT authorize live-readiness. Phase 4e does NOT authorize exchange-write. Phase 4e does NOT validate or rescue any strategy. Phase 4e does NOT write implementation code. Phase 4e does NOT modify any source code, tests, scripts, data, manifests, or strategy docs.**

---

## 1. Summary

Phase 4e specifies, in docs-only form, the reconciliation model that a future authorized reconciliation engine would implement. The design covers: state domains to compare, classification taxonomy (13 classifications including the fail-closed `unknown_or_unclassified`), input / output contracts, the binding rules for `RuntimeMode.RECOVERY_REQUIRED` and `operator_review_required`, kill-switch dominance over reconciliation, persistence and audit requirements, a future event-contract family, a future fake-exchange failure-mode taxonomy, a recovery-action taxonomy (10 actions including the explicitly-forbidden `future_real_exchange_action_required_but_forbidden` placeholder), eleven fail-closed boundaries, six future implementation-slice options, and a recommendation.

**Phase 4e recommends Option A (remain paused) as primary**, with **Option B (richer fake-exchange failure matrix scoping) as conditional secondary**. Reconciliation needs richer divergence scenarios to test against; building reconciliation before the fake adapter can simulate the divergence patterns is procedurally premature. Implementing reconciliation against today's bounded fake adapter would either be trivially clean (because the bounded adapter cannot generate the mismatches the engine is designed to find) or require expanding the fake adapter inside the reconciliation phase (mixing scopes). The cleaner ordering is: scope the richer fake-exchange failure matrix first, then scope reconciliation against it, then implement either if the operator authorizes.

**Verification (run on the post-Phase-4d-merge tree, captured by Phase 4e):**

- `ruff check .`: **All checks passed!** (whole-repo Ruff quality gate fully clean).
- `pytest`: **785 passed in 12.81s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

**No retained-evidence verdict revised.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. **No policy locks changed.** **No code, tests, scripts, data, manifests modified by Phase 4e.** **Recommended state remains paused.**

---

## 2. Authority and boundary

Phase 4e operates strictly inside the post-Phase-4d-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11 (Phase 4 / 4a prohibition list); Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a strict-subset framing); Phase 4a's anti-live-readiness statement; Phase 4b's scripts-scope cleanup; Phase 4c's state-package residual cleanup; Phase 4d's review and recommendation.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.**
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md`.

Phase 4e adds *forward-looking design language* — a written specification of what reconciliation would entail if ever implemented — without modifying any prior phase memo, any data, any code, any rule, any threshold, any manifest, any verdict, any lock, or any gate. Phase 4e is *design-only*: every contract, taxonomy, and rule below is normative for any *future* authorized reconciliation phase, but binds no current code.

---

## 3. Starting state

```text
branch:           phase-4e/reconciliation-model-design-memo
parent commit:    2b32a32f85fb369d4039bfff0debeba84e56c4fb (post-Phase-4d-merge housekeeping)
working tree:     clean before review
main:             2b32a32f85fb369d4039bfff0debeba84e56c4fb (unchanged)

Phase 4a foundation: merged.
Phase 4b/4c cleanup: merged.
Phase 4d review:     merged (recommendation: remain paused primary; Option D
                     docs-only reconciliation-model design memo conditional
                     secondary — this phase).
Repository quality gate: fully clean (ruff check . passes; pytest 785 passes;
                          mypy strict 0 issues across 82 source files).
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

## 4. Why this memo exists

Phase 4d §15 ranked seven candidate next moves and recommended Option A (remain paused) primary, with Option D (docs-only reconciliation-model design memo) as conditional secondary. The operator selected Option D for Phase 4e. The memo's purpose is fourfold:

1. **Bridge the static-state vs workflow-state gap.** Phase 4a's `RuntimeMode.RECOVERY_REQUIRED` is a *state* without a defined *workflow*. Reconciliation is the workflow that would consume that state. Phase 4e specifies the reconciliation contract before any code is written, so that any future authorized reconciliation phase has a precise specification to implement against.
2. **Make the fail-closed semantics explicit at the workflow layer.** Phase 4a establishes fail-closed at six independent decision boundaries (persistence, initial-stop validation, stop-update validation at construction, fake-lifecycle event construction, governance-label event construction, fake-adapter stop submission). A future reconciliation engine adds an *eleven-boundary* fail-closed contract (per §17 below) — one of the largest fail-closed surfaces the project will ever specify. Writing this surface down explicitly, before code, is risk-reducing.
3. **Force the fake-exchange dependency to surface.** A reconciliation engine cannot be tested without a fake adapter that can produce the divergence scenarios the engine is designed to find. Today's fake adapter can produce a small subset (entry-unknown-outcome; stop-submission-failure; basic happy path); it cannot produce most of the failure modes a real reconciliation engine would need (partial fills; orphaned stops; multiple stops; side / size mismatch; stale observation; mark-price-vs-trade-price reference divergence). Phase 4e enumerates this dependency explicitly so the operator's eventual implementation ordering decision is informed.
4. **Anti-live-readiness fortification.** A reconciliation engine in a real-exchange context is the bridge between local intent and exchange truth — exactly the bridge that any "live-readiness" framing needs. Phase 4e writes anti-live-readiness language into the reconciliation design so that any future authorized reconciliation phase cannot drift from "local/fake reconciliation" to "live reconciliation" without a separate explicit operator authorization with new evidence.

---

## 5. Reconciliation problem statement

A future reconciliation process is **a local/runtime workflow that compares internal runtime state against an observed external (or fake) exchange state representation, classifies mismatches into a closed taxonomy, and chooses safe local actions that preserve the project's safety invariants**.

**Inputs:**

- The runtime's *internal* belief about position, orders, stops, mode, kill-switch, governance labels, operator-review-required, recovery-required.
- An *observed* representation of "exchange truth" — provided either by the fake adapter (in any future Phase-4a-aligned reconciliation phase) or, in some hypothetical far-future paper/shadow / tiny-live phase, by an authorized real exchange adapter.
- A timestamp of the observation, so staleness can be evaluated.

**Outputs:**

- A classification (`clean_consistent` ... `unknown_or_unclassified`) per §13.
- A recommended local action per §19.
- An audit event recording the run (§16 / §17).
- Optionally, a state transition (e.g., into `RuntimeMode.RECOVERY_REQUIRED`) and/or flag mutation (e.g., `operator_review_required = True`) per §15 / §16.

**Constraints:**

- **Local-only first.** Phase 4e's reconciliation design assumes the *fake* adapter as the observation source; a *real* adapter is design-placeholder only and forbidden.
- **Strategy-agnostic.** The reconciliation engine accepts any future authorized strategy without privileging one.
- **Fail-closed by default.** Eleven fail-closed boundaries (§17). Unknown classifications, missing inputs, stale observations, unprotected positions, governance-label mismatches, operator-review-required state, and persistence/event failures all force conservative behaviour.

**Phase 4e specifies but does NOT implement** any of the above. The implementation is a *future* phase decision.

---

## 6. Existing Phase 4a runtime foundation relevant to reconciliation

Phase 4a's runtime foundation provides the substrate a future reconciliation engine would consume:

| Phase 4a artefact | Reconciliation use |
|---|---|
| `prometheus.state.RuntimeMode` (`SAFE_MODE`, `RUNNING`, `BLOCKED`, `EMERGENCY`, `RECOVERY_REQUIRED`) | Reconciliation reads / writes the runtime mode; `RECOVERY_REQUIRED` is the canonical "reconciliation must complete" state. |
| `prometheus.state.RuntimeControlState` | Reconciliation reads the current control state (kill-switch, paused, operator-review-required, incident-active, entries-blocked, last-updated) and produces a new state via `with_changes` if a transition is recommended. |
| `prometheus.state.transitions.enter_recovery_required`, `enter_emergency`, `activate_kill_switch` | Reconciliation calls these (in design-only terms — Phase 4e does NOT implement) to apply state transitions. |
| `prometheus.persistence.RuntimeStore` | Reconciliation reads `load_persisted()` for the prior local state, writes via `save()`, appends to `runtime_mode_event` and `governance_label_audit`. A future reconciliation phase would add a new `reconciliation_event` table (design only — §16). |
| `prometheus.events` (`MessageEnvelope`, `MessageClass`, `RuntimeModeChangedEvent`, `KillSwitchEvent`, `FakeExchangeLifecycleEvent`, `GovernanceLabelEvent`) | Reconciliation emits a new event family (`ReconciliationStarted`, `ReconciliationCompleted`, etc. — §17). All envelope rules apply. |
| `prometheus.core.governance` (4 label schemes; `is_fail_closed`; `require_valid`) | Reconciliation calls `require_valid` on every governed label it consumes; `mixed_or_unknown` fails closed at the reconciliation boundary. |
| `prometheus.execution.fake_adapter.FakeExchangeAdapter` | Reconciliation reads `position_state`, `stop_state`, `is_entry_in_flight`, `emitted_events` to build the "observed exchange state" representation. The fake adapter today is bounded; a richer adapter would be needed for full coverage (see §18). |
| `prometheus.risk.exposure.evaluate_entry_candidate` | Reconciliation does NOT call this directly — its job is comparison, not gating; but the gates' invariants (one-symbol-only, no-pyramiding, no-reversal, no-unprotected-position-allows-new-entry) define what the reconciliation classification must protect. |
| `prometheus.risk.stop_validation.validate_initial_stop` and `validate_stop_update` | Reconciliation calls these (design only) when checking a recovered stop against the project's stop-trigger-domain governance. `mixed_or_unknown` fails closed. |
| `prometheus.operator.state_view.format_state_view` | Reconciliation outputs (classification; recommended action; operator-review-required flag) feed the state view. The state view remains read-only. |

The foundation is therefore largely *sufficient* for reconciliation's reads and writes; what is missing is (a) a richer fake adapter that can simulate the failure modes the engine is designed to detect (§18), and (b) the reconciliation engine itself (§19, §20).

---

## 7. Reconciliation model goals

The future reconciliation model must:

1. **Preserve all 15 safety properties from Phase 4a §8** (per Phase 4d §8): startup-in-SAFE_MODE; persisted-RUNNING-does-not-auto-resume; kill-switch-persists-across-restart; kill-switch-never-auto-clears; kill-switch-blocks-entries; `mixed_or_unknown` fail-closed at every governance boundary; stop-widening-rejected; exposure-gates-enforced; position-without-confirmed-protection-forces-EMERGENCY; fake-events-syntactically-distinguishable; read-only-operator-surface; persistence-rejects-corrupt-runtime-modes; no-network-IO; no-secrets; single-source-of-truth-for-governance-labels.
2. **Add a single new safety property: reconciliation must be conservative.** A reconciliation run that cannot prove safety must transition the runtime into `RECOVERY_REQUIRED` (or stronger), set `operator_review_required = True`, emit an audit event, and refuse to advance. This is the **conservative-on-uncertainty** rule.
3. **Remain strategy-agnostic.** The engine accepts any future authorized strategy without privileging one; reconciliation rules apply uniformly.
4. **Remain local-only.** Phase 4e specifies reconciliation against the fake adapter; any real-exchange reconciliation requires a separately authorized future phase.
5. **Be deterministic and tested.** Like Phase 4a, the engine must run offline, with deterministic results given fixed inputs; tests must cover every classification + recommended-action combination plus every fail-closed boundary.
6. **Be idempotent on clean inputs.** A reconciliation run on a clean state must produce `clean_consistent` and recommend `no_action_clean` regardless of how many times it runs.
7. **Be auditable.** Every run produces an append-only audit row (§16) with classification, observed-state summary, local-state summary, recommended action, applied action (if any), operator-review status, and UTC timestamp. No secrets in the audit.

---

## 8. Reconciliation model non-goals

The future reconciliation model must NOT:

1. **Place orders.** Reconciliation is a comparison + recommend + state-transition workflow. It never places, cancels, or modifies real orders. The `future_real_exchange_action_required_but_forbidden` recovery-action category (§19) is a design placeholder; until a separately authorized live phase exists, reconciliation never actually performs an exchange-write action.
2. **Auto-clear the kill switch.** Per Phase 4a's safety properties, the kill switch never auto-clears; reconciliation cannot clear it. Reconciliation may *recommend* operator review, but the operator clears the kill switch.
3. **Auto-clear `operator_review_required`.** Similarly, this flag persists across restart and never auto-clears. Reconciliation may set it; only an explicit operator action clears it.
4. **Auto-resume `RUNNING` from `RECOVERY_REQUIRED`.** A clean reconciliation result returns the runtime to `SAFE_MODE`, not `RUNNING`. Operator action plus a separate `enter_running` transition then advances to `RUNNING` if all gates pass.
5. **Modify governance labels.** The four label schemes are project-level governance (Phase 3v §8 + Phase 3w §6 / §7 / §8); reconciliation reads them, validates them against `mixed_or_unknown` fail-closed, and reports mismatches — but never edits a label scheme or substitutes a value.
6. **Modify retained-evidence verdicts.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A are preserved verbatim across all phases.
7. **Imply live-readiness.** Reconciliation in a fake / local context produces no live-readiness evidence and confers no live-capability. The architectural prohibition from Phase 4a (no real adapter exists in code) is preserved.
8. **Replace operator review.** Reconciliation produces *recommendations*; operator review remains the authoritative human-in-the-loop step for any state where automated recovery is not safe.

---

## 9. State domains to reconcile

A future reconciliation engine compares state across these domains:

### 9.1 Runtime control state

The single-row `runtime_control` record from `prometheus.persistence`. Fields: `runtime_mode`, `kill_switch_active`, `paused_by_operator`, `operator_review_required`, `entries_blocked`, `incident_active`, `updated_at_utc_ms`. Reconciliation reads this as the runtime's internal belief.

### 9.2 Persisted runtime state (audit history)

The append-only `runtime_mode_event` and `governance_label_audit` tables. Reconciliation may consult these for context (e.g., when did the kill switch last activate; what labels were last observed) but does not edit them.

### 9.3 Fake-exchange position state

`FakeExchangeAdapter.position_state` (`FakePositionState`: `symbol`, `has_position`, `side`, `quantity`, `entry_price`). Reconciliation reads this as the "observed exchange truth" in a fake context.

### 9.4 Fake-exchange order/stop state

`FakeExchangeAdapter.stop_state` (`FakeStopState`: `has_stop`, `stop_price`, `confirmed`, `submission_failed`); `FakeExchangeAdapter.is_entry_in_flight`; `FakeExchangeAdapter.emitted_events`. Reconciliation evaluates protection coverage and outstanding entry-in-flight status.

### 9.5 Future exchange snapshot state, if ever authorized

Reserved as a *design placeholder*. A future authorized real-exchange reconciliation phase would consume a `RealExchangeSnapshot` (position; open orders; open algo orders; account state) sourced from an authenticated adapter. **Phase 4e does NOT authorize a real adapter and does NOT design its snapshot in detail.**

### 9.6 Operator state view

`prometheus.operator.state_view.format_state_view(...)` is read-only and consumes the runtime control state + fake position/stop state + governance labels. Reconciliation does not write to the operator view; the view's contents are derived from the upstream domains.

### 9.7 Governance labels

The four label schemes from `prometheus.core.governance`: `StopTriggerDomain`, `BreakEvenRule`, `EmaSlopeMethod`, `StagnationWindowRole`. Reconciliation calls `require_valid` on every label it consumes; any `mixed_or_unknown` causes a `governance_label_mismatch` classification per §13.

### 9.8 Kill-switch state

`runtime_control.kill_switch_active`. Reconciliation reads but does not write this. Active kill-switch dominates reconciliation per §15.

### 9.9 Operator-review-required flag

`runtime_control.operator_review_required`. Reconciliation may *set* this flag (when classification is anything other than `clean_consistent` or a small set of clean-recoverable classifications) but never *clears* it.

### 9.10 Recovery-required status

The runtime mode being `RECOVERY_REQUIRED`. Reconciliation may *enter* this mode (via `enter_recovery_required`) but only the explicit operator workflow exits it.

---

## 10. Reconciliation input model

A future reconciliation engine accepts a frozen `ReconciliationInput` value object (design only):

```text
ReconciliationInput {
    run_id: str                                     # deterministic per run; e.g. UUIDv7 or counter+UTC
    started_at_utc_ms: int (gt=0)
    runtime_control: RuntimeControlState
    fake_position: FakePositionState | None
    fake_stop: FakeStopState | None
    fake_entry_in_flight: bool
    observed_at_utc_ms: int (gt=0)
    staleness_threshold_ms: int (gt=0)              # caller-supplied
    governance_labels: dict[scheme, label]          # current labels in use
    expected_symbol: Symbol                         # BTCUSDT in v1
}
```

Notes:

- All four fake-state fields are present as `None` if no fake state exists (i.e., adapter says "no position, no stop"). The engine treats `None` as "observed flat" — but only after staleness check passes.
- `governance_labels` carries whichever of the four schemes the runtime currently has bound. `require_valid` is called on each label individually; any `mixed_or_unknown` triggers `governance_label_mismatch`.
- The input is a *snapshot*; the engine does not subscribe to live updates. A future implementation passes one snapshot per reconciliation run.

A future implementation MUST NOT introduce real-exchange snapshot fields in this input model without a separate operator authorization (per §22).

---

## 11. Reconciliation classification model

A future reconciliation run produces exactly one classification from this closed taxonomy:

| Classification | Definition | Severity hint |
|---|---|---|
| `clean_consistent` | Local belief matches observation; no flags asserted; observation fresh; governance labels valid. | clean |
| `local_only_no_external_exposure` | Local says flat; observation says flat; no entry in flight; no stop. | clean |
| `fake_exchange_unknown_outcome` | Adapter has marked an entry as `FakeOrderOutcome.UNKNOWN`. | severe; treat as exposure may exist |
| `unprotected_position` | Observation has `has_position = True` but `stop_state.has_stop = False` or `confirmed = False`. | emergency |
| `stop_missing` | Local belief says stop is confirmed; observation says no stop. | emergency |
| `stop_orphaned` | Observation has `has_stop = True` but `has_position = False`. | severe |
| `multiple_stops` | Observation reports more than one protective stop (extension to fake adapter; not currently representable but reserved). | severe |
| `position_size_mismatch` | Local belief and observation disagree on `quantity`. | severe |
| `side_mismatch` | Local belief and observation disagree on `side` (`LONG` vs `SHORT`). | severe |
| `symbol_mismatch` | Observation's `symbol` is not the expected `BTCUSDT`. | emergency |
| `stale_observation` | `started_at_utc_ms - observed_at_utc_ms > staleness_threshold_ms`. | severe |
| `governance_label_mismatch` | Any governance label is `mixed_or_unknown` or invalid. | emergency |
| `unknown_or_unclassified` | The engine cannot assign any of the above. **Fails closed.** | emergency |

**`unknown_or_unclassified` MUST fail closed.** The engine MUST treat this classification as if it were `unprotected_position` for the purposes of state transition: enter `RECOVERY_REQUIRED`, set `operator_review_required = True`, block all entries, emit `ReconciliationRecoveryRequired` event. This rule is non-overridable.

---

## 12. Reconciliation output model

A future reconciliation engine emits a frozen `ReconciliationResult` value object (design only):

```text
ReconciliationResult {
    run_id: str                                  # matches input
    completed_at_utc_ms: int (gt=0)
    classification: Classification               # one of §13
    severity_hint: Literal["clean", "severe", "emergency"]
    recommended_action: RecoveryAction           # one of §19
    state_transition: RuntimeMode | None         # if a transition is recommended
    operator_review_required: bool               # whether the engine recommends setting this flag
    audit_summary: ReconciliationAuditSummary    # observed/local/expected/diff
    applied_action: RecoveryAction | None        # what the runtime actually applied (filled by caller)
}
```

The caller (a future runtime orchestrator) is responsible for *applying* the `recommended_action`. The engine itself produces *recommendations*; mutation is the caller's concern and is bounded by the `recovery_action` taxonomy (§19).

---

## 13. RuntimeMode.RECOVERY_REQUIRED contract

A future reconciliation run MUST transition the runtime to (or keep it in) `RECOVERY_REQUIRED` when ANY of the following holds:

1. The classification is `fake_exchange_unknown_outcome`.
2. The classification is `stale_observation`.
3. The classification is `unprotected_position`.
4. The classification is `stop_missing`, `stop_orphaned`, `multiple_stops`, `position_size_mismatch`, `side_mismatch`, or `symbol_mismatch`.
5. The classification is `governance_label_mismatch`.
6. The classification is `unknown_or_unclassified`.
7. Any reconciliation precondition failed (e.g., the engine's input snapshot itself was missing required fields, or the persistence layer rejected a write).

Rules:

- **`RECOVERY_REQUIRED` MUST require explicit operator review before any return to `SAFE_MODE` or `RUNNING`.** The engine cannot exit `RECOVERY_REQUIRED` autonomously; only an operator action plus a fresh reconciliation run that yields `clean_consistent` (or a small clean-recoverable set) can authorise a return to `SAFE_MODE`. From `SAFE_MODE`, the operator's separate `enter_running` action then advances to `RUNNING` only if all gates pass.
- **`RECOVERY_REQUIRED` does NOT auto-clear `operator_review_required`.** Setting one flag does not clear the other.
- **The `entries_blocked` flag remains derived; in `RECOVERY_REQUIRED` it is always `True`.**

This contract is normative for any future authorized reconciliation phase.

---

## 14. Operator-review-required contract

A future reconciliation engine MUST set `operator_review_required = True` when the classification is anything other than `clean_consistent` or `local_only_no_external_exposure`. It MUST NOT clear the flag under any circumstance.

Rules:

- **The flag MUST persist across restart.** Phase 4a's `RuntimeStore` already preserves this field in the `runtime_control` row; reconciliation honours this.
- **The flag MUST NOT auto-clear.** Even a subsequent `clean_consistent` reconciliation does not clear it; only explicit operator action does.
- **Clearing the flag MUST NOT auto-resume `RUNNING`.** Clearing returns the runtime to `SAFE_MODE` (or wherever it was, if not `RECOVERY_REQUIRED`); the explicit `enter_running` transition then applies its own gates.
- **The operator state view MUST surface this flag prominently.** Phase 4a's `format_state_view` already renders it. A future reconciliation phase adds the most-recent classification + summary to the view (read-only).

---

## 15. Kill-switch interaction

A future reconciliation engine MUST NOT clear or weaken the kill switch. Specifically:

- **Kill-switch dominates reconciliation.** When `kill_switch_active = True`:
  - All future entry attempts are blocked regardless of reconciliation outcome.
  - Reconciliation MAY run (kill-switch allows safety-action reads per `docs/07-risk/kill-switches.md` §Actions allowed while active) but its only valid recommendations are `no_action_clean`, `block_entries`, `enter_recovery_required`, `record_audit_event`, `require_operator_review`, and `mark_fake_*_unknown`. Other actions are implicitly suppressed.
  - The runtime mode is forced to `BLOCKED` if it was `RUNNING`; reconciliation may also set it to `RECOVERY_REQUIRED` or `EMERGENCY`. Reconciliation MUST NOT transition out of `BLOCKED` to `RUNNING`.
- **Reconciliation MAY recommend operator review** (and SHOULD, on any non-clean classification) but MUST NOT auto-clear the kill switch.
- **Reconciliation MAY NOT auto-clear `EMERGENCY`** state; per Phase 4a `transitions.enter_emergency` sets `incident_active = True` and `operator_review_required = True`, both of which only the operator clears. Reconciliation may *transition into* `EMERGENCY` (e.g., on `unprotected_position`); it cannot transition *out*.
- **Kill-switch persistence remains mandatory.** Phase 4a's contract preserves this; reconciliation honours it.

If reconciliation is invoked while the kill switch is active, the engine emits its result, sets `operator_review_required = True` if not already, and the runtime remains blocked.

---

## 16. Persistence and audit requirements

A future authorized reconciliation phase MUST add an append-only `reconciliation_event` table to the SQLite runtime store. Required columns:

```text
reconciliation_event (
    rowid_pk INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    started_at_utc_ms INTEGER NOT NULL CHECK (started_at_utc_ms > 0),
    completed_at_utc_ms INTEGER NOT NULL CHECK (completed_at_utc_ms > 0),
    classification TEXT NOT NULL,
    severity_hint TEXT NOT NULL CHECK (severity_hint IN ('clean','severe','emergency')),
    observed_state_summary_json TEXT NOT NULL,
    local_state_summary_json TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    applied_action TEXT,                              -- nullable; filled by caller
    operator_review_required INTEGER NOT NULL CHECK (operator_review_required IN (0,1)),
    runtime_mode_after TEXT NOT NULL,                 -- mode after the engine's recommendation
    recorded_at_utc_ms INTEGER NOT NULL CHECK (recorded_at_utc_ms > 0)
);
```

Rules:

- **Append-only.** No `UPDATE` statements on this table. The `applied_action` column is filled at insert-time by the caller; if the caller cannot determine it pre-insert, it is `NULL` and a separate row records the actual application.
- **No secrets in audit.** No API keys, no signing material, no credentials, no exchange-write tokens, no `.env` content. Phase 4a's persistence layer already excludes these; reconciliation honours the same exclusion.
- **`run_id` is deterministic per run.** Recommendation: a counter + UTC ms timestamp, formatted as `recon-{counter:08d}-{utc_ms}`, analogous to `prometheus.events.envelope.new_message_id`. UUIDs are also acceptable but offer no benefit over the counter-based scheme.
- **JSON summaries are bounded.** A schema file (or pydantic model) constrains the keys; arbitrary extension is rejected by the validator.
- **Persistence write failure fails closed.** If the DB write fails, the runtime MUST NOT proceed past the reconciliation run — it transitions to `RECOVERY_REQUIRED` with `operator_review_required = True` and the failure is logged via the structured-logging slice (Phase 4d Option B) if that slice exists, or via stderr otherwise.
- **Backfill of historical reconciliation events is forbidden.** The table is forward-only; pre-implementation runs do not exist and cannot be retroactively inserted.

---

## 17. Event-contract requirements

A future authorized reconciliation phase MUST add the following event types to `prometheus.events.runtime_events` (design only — Phase 4e does NOT implement these):

| Event | Trigger | Payload (minimum) |
|---|---|---|
| `ReconciliationStarted` | Reconciliation engine begins a run | `run_id`, `started_at_utc_ms`, `observed_at_utc_ms`, `staleness_threshold_ms` |
| `ReconciliationCompleted` | Run finishes (any outcome) | `run_id`, `completed_at_utc_ms`, `classification`, `severity_hint` |
| `ReconciliationMismatchDetected` | Classification is anything other than `clean_consistent` / `local_only_no_external_exposure` | `run_id`, `classification`, `observed_summary`, `local_summary`, `diff_summary` |
| `ReconciliationActionRecommended` | Engine recommends a recovery action | `run_id`, `recommended_action`, `recommended_state_transition`, `recommended_operator_review_required` |
| `ReconciliationRecoveryRequired` | Engine forces `RECOVERY_REQUIRED` | `run_id`, `prior_runtime_mode`, `reason` |
| `OperatorReviewRequired` | Engine sets `operator_review_required = True` | `run_id`, `reason`, `prior_value` |
| `ReconciliationAuditRecorded` | Audit row written successfully | `run_id`, `audit_rowid`, `recorded_at_utc_ms` |

Rules:

- All envelope rules from `prometheus.events.envelope.MessageEnvelope` apply (`message_type`, `message_class = event`, `message_id`, `correlation_id`, `causation_id`, `occurred_at_utc_ms`, `source_component = "reconciliation"`, `payload`).
- **Validators MUST call `prometheus.core.governance.require_valid` on any governance label in the payload.** `mixed_or_unknown` fails closed.
- **No secrets in payload.**
- **`correlation_id` is the `run_id`** for events emitted within one reconciliation run.

Phase 4e does NOT implement these events.

---

## 18. Fake-exchange requirements for future testing

A reconciliation engine cannot be tested without a fake adapter that can produce the divergence scenarios it is designed to detect. A future "richer fake-exchange failure matrix" slice (Phase 4d §15.3 Option C) MUST be able to simulate at minimum:

| Failure mode | What the adapter produces |
|---|---|
| Partial fills | Entry filled with `quantity < requested_quantity`; `FakePositionState.quantity < pending_entry.requested_quantity`. |
| Unknown entry outcome | `FakeOrderOutcome.UNKNOWN`; existing in Phase 4a; preserved. |
| Missing protective stop | `has_position = True` AND `has_stop = False`; existing in Phase 4a. |
| Stop submission timeout | `stop_state.submission_failed = True`; existing in Phase 4a. |
| Stop confirmation delay | `stop_state.has_stop = True, confirmed = False` for an extended period (configurable threshold). |
| Orphaned stop | `has_position = False` AND `has_stop = True`. |
| Multiple stops | Adapter extension: list of stops rather than single `stop_state`; reconciliation classifies as `multiple_stops`. |
| Stale observation | Adapter exposes `last_observed_at_utc_ms`; if older than threshold, classification is `stale_observation`. |
| Position side mismatch | Adapter reports `side` differing from local belief. |
| Position size mismatch | Adapter reports `quantity` differing from local belief. |
| Mark-price vs trade-price reference divergence | Adapter exposes both reference prices; reconciliation flags any stop event whose `stop_trigger_domain` doesn't match the runtime's expected reference. |
| Cancel-and-replace lifecycle | Adapter supports a `replace_protective_stop` method; reconciliation tracks the transitional state where the old stop is canceled but new stop is unconfirmed. |
| Local/fake state divergence | Adapter exposes a "what the runtime thinks" channel separate from "what the adapter knows", so divergence can be injected for testing. |

These additions are *design requirements* for the richer fake-exchange slice (Phase 4d §15.3 Option C). Phase 4e does NOT authorise that slice; it merely enumerates what the slice would need to deliver to be useful to a future reconciliation implementation.

---

## 19. Failure-mode taxonomy

The following failure modes are the *causes* that produce the §13 classifications. Listed for completeness; each is observable through the §18 fake-adapter additions.

| Failure mode | Resulting classification |
|---|---|
| Submission timeout | `fake_exchange_unknown_outcome` |
| Partial fill ambiguity | `position_size_mismatch` (or `fake_exchange_unknown_outcome` if outcome unknown) |
| Stop rejection | `stop_missing` (if no position) or `unprotected_position` (if position) |
| Stop confirmation timeout | `unprotected_position` (after threshold) or `stop_missing` |
| Stop replacement ambiguity | `unprotected_position` (during transitional window) |
| Multiple-stops detection | `multiple_stops` |
| Orphaned-stop detection | `stop_orphaned` |
| Stream stale | `stale_observation` |
| Manual / non-bot exposure | `unknown_or_unclassified` (because the runtime cannot vouch for non-bot orders) → fails closed |
| Mark-price-vs-trade-price divergence at stop trigger | `governance_label_mismatch` (if label declared) or `unknown_or_unclassified` |
| Local state lost | `unknown_or_unclassified` → fails closed |
| Persistence write failure | (not a classification per se; engine forces `RECOVERY_REQUIRED` per §16) |

---

## 20. Recovery action taxonomy

A future reconciliation engine recommends one action from this closed taxonomy:

| Action | Meaning |
|---|---|
| `no_action_clean` | Classification is `clean_consistent` or `local_only_no_external_exposure`; runtime can proceed. |
| `block_entries` | Set `entries_blocked = True` (caller derives via state model); typically pairs with another action. |
| `enter_safe_mode` | Transition runtime to `SAFE_MODE` (e.g., from `RUNNING` after a non-emergency mismatch). |
| `enter_emergency` | Transition runtime to `EMERGENCY` (e.g., on `unprotected_position`); sets `incident_active = True`, `operator_review_required = True`. |
| `enter_recovery_required` | Transition runtime to `RECOVERY_REQUIRED`; the canonical "reconciliation must complete" state. |
| `require_operator_review` | Set `operator_review_required = True` without changing mode. |
| `record_audit_event` | Write `reconciliation_event` row only; no state mutation. |
| `mark_fake_order_unknown` | Tell the fake adapter to mark the pending entry as `FakeOrderOutcome.UNKNOWN` (caller handles). |
| `mark_fake_stop_unknown` | Tell the fake adapter to mark the protective stop as submission-failed (caller handles). |
| `future_real_exchange_action_required_but_forbidden` | Design placeholder. Indicates that, in some hypothetical far-future paper/shadow / tiny-live phase, a real-exchange action (place stop; cancel order; flatten position) would be recommended. **Until a separately authorized live phase exists, this category MUST cause the engine to fall back to `enter_recovery_required` + `require_operator_review` + `record_audit_event`** — i.e., the placeholder is non-actionable in any non-live context. |

The last category is *explicit* in the design so that future implementers cannot accidentally introduce real-exchange capability through reconciliation. Phase 4e MUST NOT authorize the `future_real_exchange_action_required_but_forbidden` action's actual real-exchange implementation; that requires a separate operator authorization with new evidence (paper/shadow / tiny-live preconditions per `docs/12-roadmap/phase-gates.md`).

---

## 21. Fail-closed requirements

A future reconciliation engine MUST fail closed at the following eleven boundaries:

1. **Missing local state.** `runtime_control` row is `NULL` or fails to deserialize → `unknown_or_unclassified` + `enter_recovery_required` + `require_operator_review`.
2. **Missing fake/external observation.** `fake_position` and `fake_stop` are both `None` AND the input does not assert "observed flat" (e.g., adapter raised an error fetching state) → fails closed.
3. **Stale observation.** `started_at_utc_ms - observed_at_utc_ms > staleness_threshold_ms` → `stale_observation` + `enter_recovery_required` + `require_operator_review`.
4. **Unknown runtime mode.** `runtime_control.runtime_mode` deserializes to a value outside the `RuntimeMode` enum (e.g., schema corruption per Phase 4a's `RuntimeStoreError` test) → `unknown_or_unclassified` + `enter_recovery_required`.
5. **Unknown classification.** Engine cannot assign a classification → `unknown_or_unclassified` (which itself fails closed).
6. **`mixed_or_unknown` governance label.** `require_valid` raises → `governance_label_mismatch` + `enter_recovery_required` + `require_operator_review`.
7. **Missing stop-trigger-domain.** A stop-bearing event in the audit history lacks `stop_trigger_domain` (which is impossible by Phase 4a's event-construction validators, but defensively re-checked) → `governance_label_mismatch`.
8. **Unprotected position.** `has_position = True` AND `confirmed_stop = False` → `unprotected_position` + `enter_emergency` + `require_operator_review`. This is the strictest case in the taxonomy.
9. **Operator-review-required state.** If the engine is invoked while `operator_review_required = True` and the new classification is not strictly clean, the operator-review-required flag MUST stay set; the engine MUST NOT overwrite it to `False`.
10. **Persistence write failure.** Audit write or state write fails → engine returns `recommended_action = enter_recovery_required` + `require_operator_review` even if the underlying classification was clean; the failure to persist itself is unsafe.
11. **Event-validation failure.** Pydantic validation of any emitted event fails → engine treats the run as failed (`unknown_or_unclassified`) and forces `RECOVERY_REQUIRED`; the un-emitted event is logged and the operator is notified.

These eleven boundaries form one of the largest fail-closed surfaces the project will ever specify. Any future authorized reconciliation phase MUST implement all eleven in code with at least one test per boundary.

---

## 22. Persistence and audit requirements (cross-reference)

See §16 for the full audit-table specification. Key invariants restated for prominence:

- Append-only, no UPDATE.
- No secrets / credentials / API keys.
- Bounded JSON summaries via schema validation.
- Persistence write failure fails closed (boundary 10 of §17).
- Forward-only; no backfill.

---

## 23. Event-contract requirements (cross-reference)

See §17 for the full event family. Key invariants restated:

- Seven event types in design only; Phase 4e does NOT implement them.
- All envelope rules from `prometheus.events.envelope.MessageEnvelope` apply.
- Validators call `require_valid` on any governance label in payload.
- No secrets in payload.
- `correlation_id = run_id` within a reconciliation run.

---

## 24. Open questions and deferred items

Phase 4e flags the following design questions for resolution by a future reconciliation-implementation phase, NOT by Phase 4e:

1. **Staleness threshold value.** Per `docs/06-execution-exchange/user-stream-reconciliation.md`, this is implementation-time. Phase 4e does not set a numeric value.
2. **Reconciliation invocation cadence.** Per the user-stream-reconciliation doc, reconciliation is invoked on confidence loss or restart; in a future fake-only context, on demand by the operator or test fixture. Phase 4e does not specify a cadence beyond "on demand by caller".
3. **Diff format inside `audit_summary`.** A bounded JSON schema is required; the exact field layout is implementation-time.
4. **State-transition idempotence.** A transition into `RECOVERY_REQUIRED` from an already-`RECOVERY_REQUIRED` mode is a no-op for runtime mode but should still produce an audit row recording the new run. Phase 4e specifies the "audit always" rule; it does not specify whether the persistence layer de-duplicates audit rows.
5. **Multiple-stops representation in fake adapter.** Phase 4a's adapter has at most one stop. The richer-adapter slice (Phase 4d §15.3) must extend to a list of stops; Phase 4e does not authorise that extension.
6. **Reconciliation-vs-strategy ordering.** A future authorized strategy MAY produce its own consistency-check semantics (e.g., a stop-update intent that the strategy emits but the runtime has not yet acted on). The interaction is out of Phase 4e scope; design only.
7. **Operator-action vocabulary.** The operator's tools to *clear* `operator_review_required` and exit `RECOVERY_REQUIRED` are not specified by Phase 4e. The Phase 4a CLI is read-only; an operator-write CLI would be a separately authorized phase.

These items are pre-coding-blockers for any future authorized reconciliation phase.

---

## 25. Future implementation-slice options

Phase 4e evaluates six candidate next moves (the design-only memo subset of Phase 4d's seven options, excluding the docs-only memo itself which is this phase). **Phase 4e does NOT authorize any of them.**

### 25.1 Option A — Remain paused (PRIMARY recommendation)

Take no further action. The reconciliation design is recorded in the project's main branch (after Phase 4e merge); future authorized phases inherit it. Pausing preserves operator optionality fully.

### 25.2 Option B — Richer fake-exchange failure matrix scoping (CONDITIONAL secondary)

Authorize a docs-only scoping memo for the richer fake-exchange failure matrix (Phase 4d §15.3 Option C). The scoping memo would specify the §18 additions in implementation-grade detail (exact method signatures, exact event payloads, exact state-machine extensions) but would not implement them.

**Why this is the right next step if implementation continues:** A reconciliation engine cannot be tested without divergence scenarios; the richer fake adapter is the source of those scenarios. Building reconciliation against today's bounded adapter would be either trivially clean (the adapter cannot generate the mismatches the engine is designed to find) or would require extending the adapter inside the reconciliation phase (mixing scopes). The cleanest ordering is: scope the richer fake adapter first, then scope reconciliation against it, then implement either if the operator authorizes.

### 25.3 Option C — Implement local-only reconciliation engine against fake exchange only (CONDITIONAL alternative)

Authorize an implementation slice that builds the reconciliation engine described in this memo (§7–§21) against the *current* fake adapter, accepting that test coverage will be limited to the failure modes the bounded adapter can produce.

**Phase 4e view:** Acceptable but suboptimal. The engine would be useful but under-tested; later expansion of the fake adapter would require revisiting the engine's tests. The richer-adapter-first ordering (Option B → richer adapter → reconciliation) avoids this rework.

### 25.4 Option D — Implement structured runtime logging / audit export first (CONDITIONAL alternative)

Authorize the Phase 4d §15.4 Option B implementation slice (structured runtime logging / audit export) before reconciliation work. This produces operator-visible value (audit-trail export) that is directly useful regardless of whether reconciliation is ever implemented, and provides the structured-logging substrate that reconciliation's audit events would benefit from.

**Phase 4e view:** Acceptable as a parallel track. Phase 4d preferred Option C (richer fake adapter) over Option B (structured logging) among implementation slices; Phase 4e's reconciliation analysis reinforces that preference because reconciliation depends on the richer adapter while structured logging is independent of reconciliation.

### 25.5 Option E — Strategy-readiness gate (NOT RECOMMENDED NOW)

Per Phase 4d §15.5: defer until a strategy is on the operator's authorization horizon. Designing for a strategy that does not exist creates rhetorical drift toward strategy work.

### 25.6 Option F — Phase 4 canonical / paper-shadow / live-readiness / exchange-write (FORBIDDEN / NOT RECOMMENDED)

Per Phase 4d §15.7 + cumulative Phase 3u §16.5 + Phase 3v §17.5 + Phase 3w §17.5 + Phase 3x §18.5 + Phase 4a §22. Forbidden.

---

## 26. Recommendation

**Phase 4e recommends Option A (remain paused) as primary.** Option B (docs-only richer-fake-exchange scoping memo) is acceptable as conditional secondary if the operator wishes to keep moving while staying inside docs-only discipline.

The recommendation preserves:

- **No real exchange adapter.** Architectural prohibition unchanged.
- **No live-readiness.** Design-only memo confers no live capability.
- **No paper/shadow.** Phase 7 territory; not authorized.
- **No strategy work.** Phase 4e is strategy-agnostic by construction.
- **No exchange-write.** Architectural prohibition unchanged.
- **No credentials.** No `.env`, no `.mcp.json` modification, no MCP enablement, no Graphify.
- **No verdict revision.** Retained-evidence verdicts preserved verbatim.
- **No lock change.** Project-level locks preserved verbatim.

The recommendation rejects:

- **Option C (reconciliation against current bounded adapter).** Sub-optimal ordering; would require rework when adapter is later extended.
- **Option E (strategy-readiness gate).** Defer per Phase 4d.
- **Option F (Phase 4 canonical / paper-shadow / live-readiness / exchange-write).** Forbidden.

The recommendation conditionally accepts (in order of preference):

- **Option B (docs-only richer-fake-exchange scoping memo).** Lowest-risk move that produces concrete documentation value and unblocks reconciliation implementation when ever authorized.
- **Option D (structured runtime logging / audit export — implementation slice, preceded by docs-only scoping).** Acceptable as a parallel track; produces operator value independent of reconciliation.

---

## 27. Operator decision menu

The operator now has a structured reconciliation-model design specification.

### 27.1 Option A — Remain paused (PRIMARY)

Take no further action. Phase 4e's design value is realized by the memo itself; future runtime / reconciliation work, if ever authorized, would inherit the contracts (§9–§21) regardless. Pausing preserves operator optionality.

### 27.2 Option B — Docs-only richer-fake-exchange scoping memo (CONDITIONAL secondary)

Authorize a future docs-only scoping memo for the richer fake-exchange failure matrix per §18. The memo would NOT authorize implementation; that would be a separate decision.

### 27.3 Option C — Reconciliation engine against current bounded adapter (CONDITIONAL alternative)

Authorize an implementation slice that builds the reconciliation engine of §7–§21 against today's fake adapter. Should be preceded by a docs-only execution-plan memo (analogous to Phase 3x → Phase 4a). **Phase 4e view: Acceptable but suboptimal; Option B richer-adapter-first ordering is preferred.**

### 27.4 Option D — Structured runtime logging / audit export (CONDITIONAL alternative)

Authorize the Phase 4d §15.4 Option B slice. Independent of reconciliation; operator-visible value. Should be preceded by a docs-only scoping memo.

### 27.5 Option E — Strategy-readiness gate (NOT RECOMMENDED NOW)

Defer until a strategy is on the authorization horizon.

### 27.6 Option F — Phase 4 canonical / paper-shadow / live-readiness / exchange-write (FORBIDDEN / NOT RECOMMENDED)

Per `docs/12-roadmap/phase-gates.md`.

### 27.7 Recommendation

**Phase 4e recommends Option A (remain paused) as primary.** Option B (docs-only richer-fake-exchange scoping memo) is acceptable as conditional secondary. Options C / D are acceptable conditional alternatives if the operator authorizes implementation work, with Option B richer-adapter-first preferred over Option C reconciliation-first. Options E / F are not recommended now (E) or forbidden (F).

---

## 28. What this does not authorize

Phase 4e explicitly does NOT authorize, propose, or initiate any of the following:

- **Reconciliation implementation.** No code is written.
- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 (canonical) requires Phase 3 strategy evidence which the project does not have.
- **Phase 4f or any successor phase.** Phase 4e is a docs-only memo; the operator must explicitly authorize any successor.
- **Live exchange-write capability.** The architectural prohibition from Phase 4a remains: only the fake adapter exists in code; no real Binance code.
- **Production Binance keys, authenticated APIs, private endpoints, user stream, WebSocket, listenKey lifecycle, production alerting, Telegram / n8n production routes, MCP, Graphify, `.mcp.json`, credentials, exchange-write capability.** None of these is touched, enabled, or implied.
- **Strategy implementation / rescue / new candidate.** No strategy code added or modified.
- **Verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **Lock change.** §1.7.3 / §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / mark-price-stop lock all preserved verbatim.
- **Data acquisition / patching / regeneration / modification.** `data/` artefacts preserved verbatim.
- **Diagnostics / Q1–Q7 rerun / backtests.** None run.
- **Phase 3v stop-trigger-domain governance modification.** Preserved verbatim.
- **Phase 3w break-even / EMA slope / stagnation governance modification.** Preserved verbatim.
- **Paper/shadow / live-readiness / deployment.** Not authorized.

Phase 4e is *docs-only design memo* and limited to producing this memo and the accompanying closeout artefact.

---

## 29. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4f / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No reconciliation implementation.**
- **No implementation code written.**
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4e performs no network I/O.
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
- **No `docs/06-execution-exchange/exchange-adapter-design.md` substantive change.**
- **No `docs/06-execution-exchange/user-stream-reconciliation.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4e branch.** Per the Phase 4e brief.
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

## 30. Remaining boundary

- **Recommended state:** **paused.**
- **Phase 4e output:** docs-only design memo + closeout artefact on the Phase 4e branch.
- **Repository quality gate state:** **fully clean.** Whole-repo `ruff check .` passes; pytest 785 passed; mypy strict 0 issues across 82 source files (verified during Phase 4e startup).
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged. Phase 4b and Phase 4c quality cleanups merged. Phase 4d review merged. Phase 4e design memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by 4b / 4c / 4d / 4e).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved).
- **Reconciliation governance:** Defined by Phase 4e (this memo) but NOT yet enforced in code; enforcement awaits a separately authorized future implementation phase.
- **OPEN ambiguity-log items after Phase 4e:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.**
- **Branch state:** `phase-4e/reconciliation-model-design-memo` exists locally and (after push) on `origin/phase-4e/reconciliation-model-design-memo`. NOT merged to main.

---

## 31. Next authorization status

**No next phase has been authorized.** Phase 4e's recommendation is Option A (remain paused) as primary, with Option B (docs-only richer-fake-exchange scoping memo) as conditional secondary, Options C / D (implementation slices, each preceded by a docs-only scoping memo) as acceptable conditional alternatives if the operator wishes to keep building (with Option B richer-adapter-first preferred over Option C reconciliation-first), Option E (strategy-readiness gate) as not recommended now, and Option F (Phase 4 canonical / paper-shadow / live-readiness / exchange-write) as forbidden / not recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase 4a). The Phase 4b script-scope quality-gate restoration is complete (per Phase 4b). The Phase 4c state-package quality-gate residual cleanup is complete (per Phase 4c). The Phase 4d post-4a/4b/4c review is complete (per Phase 4d). The Phase 4e reconciliation-model design memo is complete on the Phase 4e branch (this phase). **Recommended state remains paused.**
