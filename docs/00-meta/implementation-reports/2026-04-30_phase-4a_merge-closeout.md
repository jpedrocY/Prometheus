# Phase 4a Merge Closeout

## Summary

Phase 4a — **Local Safe Runtime Foundation** — has been merged to `main` and pushed to `origin/main`. The merge brings strategy-agnostic local runtime safety infrastructure onto main: in-process runtime state machine; SQLite-backed runtime control persistence; typed internal event contracts; the four Phase 3v + Phase 3w governance label schemes enforceable in code at every relevant decision boundary with `mixed_or_unknown` failing closed; risk sizing / exposure / stop-validation skeletons; deterministic local fake-exchange adapter; read-only operator state view + minimal CLI; and a comprehensive Phase 4a test harness.

**Phase 4a is local-only / fake-exchange / dry-run / exchange-write-free / strategy-agnostic.** The merge does NOT authorize paper/shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, user stream, WebSocket, MCP, Graphify, `.mcp.json`, credentials, or exchange-write capability. The merge does NOT validate any strategy and does NOT revise any verdict. The merge does NOT change any project lock.

**No retained-evidence verdict revised.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other — all preserved verbatim. **No policy locks changed.** §11.6 = 8 bps HIGH per side preserved. §1.7.3 mark-price-stops preserved. Phase 3v §8 stop-trigger-domain governance preserved. Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance preserved.

**No code, tests, scripts, data, manifests modified by the Phase 4a merge or by the housekeeping commit beyond the merge contents themselves.** No diagnostics rerun. No Q1–Q7 rerun. No backtests. No data acquisition / patching / regeneration / modification. No `data/manifests/*.manifest.json` modification. No spec / backtest-plan / validation-checklist / stop-loss-policy / runtime-doc / phase-gates / technical-debt-register / ai-coding-handoff / first-run-setup-checklist substantive edit. No `docs/00-meta/implementation-ambiguity-log.md` modification. No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private Binance endpoints / user stream / WebSocket / public endpoints consulted. No secrets requested or stored. **Recommended state remains paused.** **No successor phase has been authorized.**

## Files changed

The Phase 4a merge into `main` brought in 35 file changes (33 new files + 2 modified files):

**Modified (2 files):**

- `src/prometheus/core/__init__.py` — added exports for the four governance label types, `GovernanceLabel`, `GovernanceLabelError`, `is_fail_closed`, `require_valid`, and the four `parse_*` helpers.
- `.gitignore` — narrow root-anchoring fix (changed `state/`, `runtime/`, `cache/` to `/state/`, `/runtime/`, `/cache/`) so source-code packages and test directories named `state` or `runtime` are not accidentally ignored. No secret/credential ignore rule weakened.

**Added — production code (20 files):**

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

**Added — documentation (2 files in the merge; this file is added in the housekeeping commit):**

- `docs/00-meta/implementation-reports/2026-04-30_phase-4a_local-safe-runtime-foundation.md` — Phase 4a implementation report.
- `docs/00-meta/implementation-reports/2026-04-30_phase-4a_closeout.md` — Phase 4a closeout artefact.

The post-merge housekeeping commit additionally adds:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4a_merge-closeout.md` — this file.
- `docs/00-meta/current-project-state.md` — narrow update recording Phase 4a merged, local safe runtime foundation implemented, ten Phase 4a safe-slice components implemented, test evidence (117 Phase 4a tests passed; 785/785 project total; ruff clean for Phase 4a code; mypy strict no issues across 82 source files; 29 pre-existing ruff issues in Phase 3q/3s scripts unchanged), Phase 4 canonical / Phase 4b / paper-shadow / live-readiness / deployment / production-key / authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write all unauthorized, no strategy implemented or validated, no retained verdicts revised, no project locks changed, recommended state paused, no next phase authorized. Stale "Current phase" and "Most recent merge" code blocks refreshed to point at the Phase 4a merge.

NOT modified by this merge or by the housekeeping commit:

- All `data/manifests/*.manifest.json` files (v002 + Phase 3q v001-of-5m). Mark-price 5m `research_eligible: false` preserved.
- All `data/raw/**`, `data/normalized/**`, `data/derived/**` partitions.
- All other `src/prometheus/**` source code (existing strategy modules, research modules, core modules other than `__init__.py` and the new `governance.py`).
- All `scripts/**`.
- All `.claude/rules/**`.
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w / 3x reports / closeouts / merge-closeouts.
- `docs/00-meta/implementation-ambiguity-log.md` — not modified by Phase 4a.
- `docs/03-strategy-research/v1-breakout-strategy-spec.md` — substantive content preserved verbatim. Lines 156–172, 332, 380, 415, 564 unchanged.
- `docs/03-strategy-research/v1-breakout-backtest-plan.md` — preserved verbatim.
- `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` — preserved verbatim.
- `docs/07-risk/stop-loss-policy.md` — preserved verbatim.
- `docs/06-execution-exchange/binance-usdm-order-model.md` — preserved verbatim.
- `docs/12-roadmap/phase-gates.md` — preserved verbatim.
- `docs/12-roadmap/technical-debt-register.md` — preserved verbatim.
- `docs/00-meta/ai-coding-handoff.md` — preserved verbatim.
- `docs/09-operations/first-run-setup-checklist.md` — preserved verbatim.
- All `docs/04-data/*`, `docs/06-execution-exchange/*`, `docs/07-risk/*`, `docs/08-architecture/*`, `docs/09-operations/*`, `docs/10-security/*`, `docs/11-interface/*` (other than the new Phase 4a artefacts) — preserved verbatim.
- `.mcp.json` — preserved (no changes; no new MCP servers enabled).
- `pyproject.toml` — preserved verbatim.
- `uv.lock` — preserved verbatim.

## Phase 4a commits included

| Commit | Subject |
|---|---|
| `b1f6cc1251635ce6e6a0191c467d1d7eac0c0271` | `phase-4a: local safe runtime foundation (strategy-agnostic)` — Phase 4a implementation + report (35 files changed; 4 634 insertions; 4 deletions). |
| `9c10dbd4e80e7daa60ffd77c1830d51d4776b345` | `docs(phase-4a): closeout report (Markdown artefact)` — Phase 4a closeout (256 lines). |

## Merge commit

- **Phase 4a merge commit (`--no-ff`, ort strategy):** `3c368fa4577e22f6e6b558caa2e43b2cad87b1c8`
- **Merge title:** `Merge Phase 4a (local safe runtime foundation: state model, persistence, events, governance, risk, fake-exchange, operator state view, tests) into main`

## Housekeeping commit

The post-merge housekeeping commit adds this Phase 4a merge-closeout file and updates `current-project-state.md` narrowly. Its SHA advances `main` by one further commit beyond the merge commit `3c368fa4` and is reported in the chat closeout block accompanying this commit. Per prior phase pattern, the housekeeping commit's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged.

## Final git status

```text
clean
```

Working tree empty after the post-merge housekeeping commit. No uncommitted changes. No untracked files.

## Final git log --oneline -8

Snapshot at the housekeeping commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this housekeeping commit itself is committed>  docs(phase-4a): merge closeout + current-project-state sync
3c368fa  Merge Phase 4a (local safe runtime foundation: state model, persistence, events, governance, risk, fake-exchange, operator state view, tests) into main
9c10dbd  docs(phase-4a): closeout report (Markdown artefact)
b1f6cc1  phase-4a: local safe runtime foundation (strategy-agnostic)
be91842  docs(phase-3x): merge closeout + current-project-state sync
dca29af  Merge Phase 3x (docs-only Phase 4a safe-slice scoping memo) into main
538e8f1  docs(phase-3x): closeout report (Markdown artefact)
14bfb38  phase-3x: Phase 4a safe-slice scoping memo (docs-only)
```

## Final rev-parse

- **`git rev-parse main`** (after housekeeping commit + push): the housekeeping commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse origin/main`** (after push): same as `main` above.
- **`git rev-parse HEAD`** (on `main`): same as `main` above.
- **`git rev-parse phase-4a/local-safe-runtime-foundation`**: `9c10dbd4e80e7daa60ffd77c1830d51d4776b345` (branch tip preserved).
- **`git rev-parse origin/phase-4a/local-safe-runtime-foundation`**: `9c10dbd4e80e7daa60ffd77c1830d51d4776b345`.
- **`git rev-parse phase-3x/phase-4a-safe-slice-scoping`**: `538e8f1680db083705f8a8b7c08c15906bd2e569` (branch tip preserved).
- **`git rev-parse phase-3w/remaining-ambiguity-log-resolution`**: `85f52dc6dc71437cd8708f9b7c411816e31301be` (branch tip preserved).
- **`git rev-parse phase-3v/gap-20260424-032-stop-trigger-domain-resolution`**: `5be99783f86eb3830cd9814defda3032073de3c7` (branch tip preserved).
- **`git rev-parse phase-3u/implementation-readiness-and-phase-4-boundary-review`**: `f31903af800e4ce0ac25f17d56e7f3fa7cc83822` (branch tip preserved).

## main == origin/main confirmation

After the Phase 4a merge push: local `main` = `origin/main` = `3c368fa4577e22f6e6b558caa2e43b2cad87b1c8`. Synced.

After the post-merge housekeeping commit + push: local `main` = `origin/main` advances to the housekeeping commit's SHA (reported in the chat closeout block accompanying this commit). Synced.

## Implemented scope

The Phase 4a merge brings the following ten Phase 3x §9 candidate components onto `main` as strategy-agnostic skeletons:

1. **Runtime mode / state model** — `prometheus.state` package: `RuntimeMode` `StrEnum` (SAFE_MODE / RUNNING / BLOCKED / EMERGENCY / RECOVERY_REQUIRED); `RuntimeControlState` frozen pydantic record; pure-function transitions (`enter_safe_mode`, `enter_running`, `enter_blocked`, `enter_emergency`, `enter_recovery_required`, `activate_kill_switch`, `clear_kill_switch`); startup defaults to SAFE_MODE; unknown state fails closed via the explicit transition guards.
2. **Runtime control state persistence** — `prometheus.persistence.runtime_store.RuntimeStore`: SQLite WAL mode with `foreign_keys = ON`, `synchronous = FULL`, `busy_timeout = 5000`; single-row `runtime_control` table; append-only `runtime_mode_event` audit table; append-only `governance_label_audit` table with `CHECK scheme IN (...)` constraint; persisted RUNNING does NOT auto-resume RUNNING; kill-switch state persists across restart; never auto-clears.
3. **Internal event contracts** — `prometheus.events`: `MessageEnvelope` with required fields (`message_type`, `message_class`, `message_id`, `correlation_id`, `causation_id`, `occurred_at_utc_ms`, `source_component`, `payload`); `MessageClass` enum (command / event / query); `RuntimeModeChangedEvent`, `KillSwitchEvent`, `FakeExchangeLifecycleEvent` (with `is_fake = True` invariant), `GovernanceLabelEvent`; deterministic `new_message_id(prefix)` counter-backed id generator.
4. **Governance label enforcement** — `prometheus.core.governance`: single source of truth for the four schemes (`StopTriggerDomain`, `BreakEvenRule`, `EmaSlopeMethod`, `StagnationWindowRole`); `is_fail_closed(label)` predicate; `require_valid(label)` raises `GovernanceLabelError` on `mixed_or_unknown`; `parse_<scheme>(value)` strict parsers; `mixed_or_unknown` fails closed at every governance-relevant decision boundary by importing from this single module.
5. **Risk sizing skeleton** — `prometheus.risk.sizing.compute_sizing(SizingInputs) -> SizingResult`: stop-distance-based sizing per `docs/07-risk/position-sizing-framework.md`; locked v1 constants exposed (`LOCKED_LIVE_RISK_FRACTION = 0.0025`, `LOCKED_LIVE_LEVERAGE_CAP = 2.0`); fail-closed on missing/invalid metadata, below-minimum quantity, notional cap violation, leverage cap violation; no live equity fetch; test fixtures only.
6. **Exposure gate skeleton** — `prometheus.risk.exposure.evaluate_entry_candidate(...) -> ExposureDecision`: BTCUSDT-only live lock (Rule 1); one-position max (Rule 2); no pyramiding (Rule 3); no reversal while positioned (Rule 4); entry-in-flight blocks (Rule 7); unprotected-position blocks (Rule 9); manual-or-non-bot exposure blocks; fake-position state only.
7. **Stop-validation skeleton** — `prometheus.risk.stop_validation`: `validate_initial_stop(StopRequest)` enforces `stop_trigger_domain` governance, side-vs-entry, ATR filter (0.60 × ATR ≤ stop_distance ≤ 1.80 × ATR), metadata presence; `validate_stop_update(StopUpdateRequest)` enforces risk-reducing-only direction; `mixed_or_unknown` fails closed at construction time.
8. **Fake-exchange adapter** — `prometheus.execution.fake_adapter.FakeExchangeAdapter`: deterministic local in-memory state machine; injectable clock; methods `submit_entry_order`, `confirm_fake_fill`, `mark_entry_unknown_outcome`, `submit_protective_stop`, `confirm_fake_protective_stop`, `mark_stop_submission_failed`, `trigger_fake_stop`; emits `FakeExchangeLifecycleEvent` with `is_fake = True`; enforces `stop_trigger_domain` on stop-bearing methods; **no Binance code; no network I/O; no credentials**.
9. **Read-only operator state view** — `prometheus.operator.state_view.format_state_view(...)`: pure function returning plain-text rendering of runtime mode + control flags + fake-position state + fake-stop state + governance label values + Phase 4a anti-live-readiness disclaimer; no controls; no exchange actions; no production alerting. Plus `prometheus.cli`: minimal `inspect-runtime --db PATH` subcommand; no mutation subcommand.
10. **Test harness** — `tests/unit/runtime/`: 10 test files, 117 tests, covering all required Phase 4a behaviors plus defensive edge cases; deterministic; no network I/O.

## Test evidence

**Phase 4a runtime tests (`tests/unit/runtime/`):**

```text
117 passed in 0.50s
```

**Project-total tests (`tests/`):**

```text
785 passed in 12.90s
```

**Ruff lint on Phase 4a code (`src/prometheus/`, `tests/unit/runtime/`):**

```text
All checks passed!
```

**Mypy strict (`tool.mypy.strict = true`, `files = ["src/prometheus"]`):**

```text
Success: no issues found in 82 source files
```

**Ruff lint on entire repository:**

```text
Found 29 errors.
```

All 29 are pre-existing in `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py` (Phase 3q + Phase 3s deliverables merged in prior phases). They are unchanged by Phase 4a. They are pre-existing technical debt; addressing them is out of Phase 4a's scope and would be a separately authorized clean-up phase.

## Safety properties proven

The Phase 4a test harness on `main` proves the following safety properties in code:

- **Startup defaults to SAFE_MODE.** `fresh_control_state` always returns SAFE_MODE with `entries_blocked = True`, regardless of previously persisted state. Tested: `test_fresh_control_state_defaults_to_safe_mode`, `test_phase_4a_full_lifecycle_no_real_exchange`.
- **Persisted RUNNING does not auto-resume.** `RuntimeStore.load_persisted` returns the persisted record for inspection only; the runtime layer constructs a fresh SAFE_MODE state and explicitly carries forward only restart-critical flags. Tested: `test_persisted_running_does_not_auto_resume_running`, `test_phase_4a_full_lifecycle_no_real_exchange`.
- **Kill-switch persists across restart.** Persisted `kill_switch_active = True` survives a simulated restart. Tested: `test_kill_switch_persists_across_restart`, `test_phase_4a_full_lifecycle_no_real_exchange`.
- **Kill-switch never auto-clears.** Only an explicit `clear_kill_switch` call clears it, and that returns to SAFE_MODE (not RUNNING). Tested: `test_clear_kill_switch_returns_to_safe_mode_not_running`.
- **Kill-switch blocks fake entries.** With kill-switch active, `enter_running` raises `KillSwitchActiveError`; downstream entry attempts cannot proceed. Tested: `test_enter_running_blocked_by_kill_switch`, `test_phase_4a_full_lifecycle_no_real_exchange`.
- **`mixed_or_unknown` fails closed at governance-relevant boundaries.** Six independent boundaries (persistence; initial-stop validation; stop-update validation at construction; fake-lifecycle event construction; governance-label event construction; fake-adapter stop submission) each tested. Tests: `test_persistence_rejects_mixed_or_unknown_*` (×4), `test_mixed_or_unknown_stop_trigger_domain_fails_closed`, `test_stop_update_mixed_or_unknown_fails_closed_at_construction`, `test_fake_exchange_lifecycle_event_rejects_mixed_or_unknown_stop_trigger`, `test_governance_label_event_rejects_mixed_or_unknown_in_any_slot`, `test_protective_stop_rejects_mixed_or_unknown_label`.
- **Stop widening is rejected.** Both long and short widening attempts raise `StopValidationError`. Tested: `test_stop_update_long_widening_rejected`, `test_stop_update_short_widening_rejected`.
- **Exposure gates enforce one-symbol / one-position / no-pyramiding / no-reversal / no-unprotected-position / no-manual-exposure behavior.** Tested: `test_non_btcusdt_live_entry_rejected_by_rule_1`, `test_pyramiding_rejected_by_rule_3`, `test_reversal_while_positioned_rejected_by_rule_4`, `test_multiple_positions_blocked_via_existing_position`, `test_unprotected_position_blocks_new_entries`, `test_entry_in_flight_blocks_new_entries`, `test_manual_exposure_blocks_new_entries`.
- **Fake exchange has no real exchange path.** Phase 4a contains only `FakeExchangeAdapter`; no real Binance adapter exists in code. There is no configuration switch that "turns on" a live adapter. The architectural prohibition is structural, not configurational. All emitted fake events carry `is_fake = True` as a model-validated invariant.
- **Operator state view is read-only.** `format_state_view` is a pure function returning a string; no controls; no order/cancel/widen-stop language. The CLI exposes only `inspect-runtime` (read-only). Tested: `test_state_view_does_not_expose_exchange_actions`.
- **No network I/O.** Phase 4a code base contains no `httpx`, `socket`, `websockets`, `urllib`, or `requests` imports. All 117 tests run offline in 0.50 seconds with no network round-trips.
- **No credentials.** No `.env` file is read; no credential field is persisted; no test fixture contains a token or key; no environment variable is consulted for credentials.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4b / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No real exchange adapter implemented.** The merge brings only `FakeExchangeAdapter` onto main; no real Binance code. No HTTP / WebSocket / listenKey / signing code added.
- **No exchange-write capability.** No order placement, no order cancellation, no account state mutation; the architectural prohibition is structural (live adapter does not exist in code).
- **No Binance credentials used.** No request for credentials. No credential storage. No `.env` file created. No secret material in commits.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4a performs no network I/O.
- **No production alerting / Telegram / n8n production routes.** None added.
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.** None.
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.** Stated explicitly in the merged Phase 4a report and in disclaimer text inside `format_state_view` output.
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
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **`.gitignore` modified narrowly only** (root-anchoring fix to `state/`/`runtime/`/`cache/` patterns; no secret/credential ignore rule weakened). See merge contents.
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No successor phase started.**

## Remaining boundary

- **main HEAD:** the housekeeping commit (SHA reported in chat closeout). After the merge: `3c368fa4`. Phase 4a implementation + report + closeout consolidated on `main`.
- **Recommended state:** **paused.**
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged; Phase 4b / any successor phase remains unauthorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (now on main).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (now on main).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (now on main).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (now on main).
- **Phase 4a safe-slice scope:** Defined by Phase 3x + implemented by Phase 4a + merged to main.
- **OPEN ambiguity-log items after Phase 4a merge:** zero relevant to runtime / strategy implementation. Pre-tiny-live items remain documented as pre-tiny-live concerns.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-4a/local-safe-runtime-foundation` pushed at `9c10dbd4`. Commits in main via Phase 4a merge.
  - All prior phase branches preserved at their respective tips.

## Next authorization status

**No next phase has been authorized.** Phase 4a's recommendation was Option A (review on branch and remain paused) as primary, with Option B (merge to main and remain paused) as conditional secondary. The operator selected Option B; the merge is now complete and the project remains paused. No further phase authorization flows from Option B.

Selection of any subsequent phase (richer runtime work per the implementation report's Option C; return to research per Option D; Phase 4 canonical / paper-shadow / live-readiness / deployment / production-key / exchange-write per Option E) requires explicit operator authorization for that specific phase. No such authorization has been issued.
