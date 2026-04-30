# Phase 4c — State Package Ruff Residual Cleanup

**Authority:** Phase 4b (Repository Quality Gate Restoration) merge closeout's documented residual quality gap (2 latent ruff issues in `src/prometheus/state/__init__.py` and `src/prometheus/state/transitions.py:49`); `pyproject.toml` ruff configuration; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4c — **State Package Ruff Residual Cleanup.** Tiny code-hygiene phase to fix exactly the two residual ruff issues documented by Phase 4b: (1) `src/prometheus/state/__init__.py:20:1` I001 import-order; (2) `src/prometheus/state/transitions.py:49:5` SIM103 simplify-return. **Phase 4c is lint-only quality-gate restoration.**

**Branch:** `phase-4c/state-package-ruff-residual-cleanup`. **Phase date:** 2026-04-30 UTC.

---

## 1. Summary

Phase 4c fixes exactly two residual ruff issues in the Phase 4a state package via behavior-preserving lint-only edits:

1. **`src/prometheus/state/__init__.py`** — reordered the relative imports alphabetically (`.control` before `.errors`, `.errors` before `.mode`, `.mode` before `.transitions`). The exported names in `__all__` are unchanged; the package's public API is unchanged.
2. **`src/prometheus/state/transitions.py`** — collapsed the final `if incident_active: return True; return False` block in `_derive_entries_blocked` to `return bool(incident_active)`. The function's signature, type, and computed value are unchanged for every input.

**Test evidence (all required commands ran on the project's `.venv`, Python 3.12.4):**

- `ruff check src/prometheus/state`: **All checks passed!**
- `ruff check .` (whole repo): **All checks passed!** (whole-repo quality gate fully restored).
- `pytest`: **785 passed in 12.59s.** No regressions; identical pass count to pre-Phase-4c.
- `mypy` strict: **Success: no issues found in 82 source files.**

**Phase 4c is lint-only quality-gate restoration.** Phase 4c fixes exactly two residual ruff issues. Phase 4c does not expand runtime functionality, does not implement strategy logic, does not run backtests, does not run diagnostics, does not run scripts, does not acquire / patch / regenerate / modify data, does not modify data manifests, does not authorize paper/shadow, does not authorize live-readiness, does not authorize deployment, does not authorize production keys, does not authorize authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write, does not validate any strategy, does not revise any verdict, and does not change any lock.

---

## 2. Authority and boundary

Phase 4c operates strictly inside the post-Phase-4b-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a prohibition list); Phase 4a's anti-live-readiness statement; Phase 4b's quality-gate-restoration scope.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md`.
- **Phase 4a public API preserved verbatim.** The `prometheus.state` package re-exports the same names in `__all__`; the `_derive_entries_blocked` helper (a private function) returns the same value for every input.

Phase 4c modifies *only* the two state-package files (lint-only) plus the two documentation artefacts (this report + the closeout).

---

## 3. Starting state

```text
branch:           phase-4c/state-package-ruff-residual-cleanup
parent commit:    5c79cea4a19f71a42600fdbb49e38a7a1c2cd3ae (post-Phase-4b-merge housekeeping)
working tree:     clean before implementation
main:             5c79cea4a19f71a42600fdbb49e38a7a1c2cd3ae (unchanged)

ruff (pre-edit, full repo): exactly 2 errors
  - src/prometheus/state/__init__.py:20:1 I001 (import block un-sorted).
  - src/prometheus/state/transitions.py:49:5 SIM103 (collapse to return bool).
mypy:             pre-edit clean (82 source files, 0 issues).
pytest:           pre-edit 785/785 passing.
```

---

## 4. Residual Ruff issues being addressed

The Phase 4b merge closeout documented two residual ruff issues in `src/prometheus/state/`. Phase 4c fixes exactly those two:

### 4.1 `src/prometheus/state/__init__.py:20:1` — I001

*Import block is un-sorted or un-formatted.* The pre-Phase-4c block ordered the relative imports as `.errors`, `.mode`, `.control`, `.transitions`. Ruff's I001 rule wants alphabetical order; the correct order is `.control`, `.errors`, `.mode`, `.transitions`.

### 4.2 `src/prometheus/state/transitions.py:49:5` — SIM103

*Return the condition `bool(incident_active)` directly.* The pre-Phase-4c `_derive_entries_blocked` function ended with `if incident_active: return True; return False`. SIM103 wants this collapsed to `return bool(incident_active)`.

---

## 5. Changes made

### 5.1 `src/prometheus/state/__init__.py`

Reordered the relative-imports block. **Before:**

```python
from .errors import (
    EntriesBlockedError,
    KillSwitchActiveError,
    RuntimeStateError,
    UnknownStateError,
)
from .mode import RuntimeMode
from .control import RuntimeControlState, fresh_control_state
from .transitions import (
    activate_kill_switch,
    ...
)
```

**After:**

```python
from .control import RuntimeControlState, fresh_control_state
from .errors import (
    EntriesBlockedError,
    KillSwitchActiveError,
    RuntimeStateError,
    UnknownStateError,
)
from .mode import RuntimeMode
from .transitions import (
    activate_kill_switch,
    ...
)
```

The four relative-import groups are now alphabetical: `.control` → `.errors` → `.mode` → `.transitions`. The set of imported names is identical; the `__all__` list is unchanged; the package's public API is unchanged.

### 5.2 `src/prometheus/state/transitions.py`

Collapsed the final two lines of `_derive_entries_blocked`. **Before:**

```python
    if operator_review_required:
        return True
    if incident_active:
        return True
    return False
```

**After:**

```python
    if operator_review_required:
        return True
    return bool(incident_active)
```

The function semantics are identical: when `incident_active` is `True`, the function returns `True` (matching the prior `if incident_active: return True` branch); when `incident_active` is `False`, the function returns `False` (matching the prior `return False`). The function signature declares `incident_active: bool`, so `bool(incident_active)` is an identity wrapper that satisfies the SIM103 rule's preferred form. No semantic change.

The four other if-blocks (`runtime_mode`, `kill_switch_active`, `paused_by_operator`, `operator_review_required`) remain unchanged because SIM103 only applies to the *final* if-block of an early-return chain; ruff did not flag those.

---

## 6. Behavior-preservation notes

Both edits are behavior-preserving by construction:

1. **Import-order reorder in `__init__.py`** — Python's import semantics treat `from X import Y` as order-independent within a single module's import-block (apart from edge cases involving circular imports, which do not apply here because all four modules are under the same `prometheus.state` namespace and import only from each other in a non-circular DAG: `errors` is a leaf; `mode` is a leaf; `control` imports from `mode`; `transitions` imports from `control`, `errors`, `mode`). Reordering `from .X import` lines does not change which names are bound or which side effects fire. The `__all__` list and the set of exported names are identical pre- and post-edit. No downstream import will resolve differently.

2. **`return bool(incident_active)` collapse** — for any `bool` input (which the type signature guarantees), `bool(incident_active)` is the identity function. The two formulations produce identical return values for every possible input; the function's truth table is unchanged. Bytecode-level the new form is shorter (no conditional jump) but the behavioral output is identical. Test coverage for `_derive_entries_blocked` flows through every public transition (`enter_running`, `enter_blocked`, `enter_emergency`, etc.); all 117 Phase 4a runtime tests + 785 project-total tests pass post-edit, confirming behavior preservation.

No runtime functionality is added, removed, or moved. No public API symbol is added, removed, or renamed. No tests are modified. No data is touched. No script is run. No network I/O is performed.

---

## 7. Commands run

All commands run from `c:\Prometheus` against the project's `.venv` (Python 3.12.4):

```text
git status
git rev-parse HEAD
git rev-parse origin/main
git checkout -b phase-4c/state-package-ruff-residual-cleanup
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check src/prometheus/state
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m pytest
.venv/Scripts/python -m mypy
git diff --stat
git add src/prometheus/state/__init__.py src/prometheus/state/transitions.py docs/00-meta/implementation-reports/2026-04-30_phase-4c_state-package-ruff-residual-cleanup.md
git commit -m "phase-4c: state package ruff residual cleanup"
git push -u origin phase-4c/state-package-ruff-residual-cleanup
```

No format-check command is configured separately by the project (`tool.ruff.format` exists but `ruff format --check` is not part of the documented project workflow). Phase 4c does not invent a format step. No script (`scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`) was run. No data was acquired / downloaded / patched / regenerated / modified. No network I/O was performed.

---

## 8. Test results

**`pytest`:**

```text
785 passed in 12.59s
```

No regressions; identical pass count to pre-Phase-4c (785/785). The two state-package edits are exercised by the Phase 4a runtime test suite (`tests/unit/runtime/`), specifically by tests that import from `prometheus.state` (verifying the reordered `__init__.py`) and tests that exercise `_derive_entries_blocked` indirectly via the `enter_*` transitions (verifying the SIM103 collapse).

---

## 9. Ruff results

**`ruff check src/prometheus/state`:**

```text
All checks passed!
```

**`ruff check .` (whole repo):**

```text
All checks passed!
```

**The whole-repo Ruff quality gate is now fully restored.** After Phase 4b cleaned the 29 known issues in `scripts/`, and Phase 4c cleaned the 2 residual issues in `src/prometheus/state/`, the entire repository passes ruff with zero errors. This closes the quality-gate restoration that Phase 4b began.

---

## 10. Mypy results

```text
Success: no issues found in 82 source files
```

Mypy strict (per `tool.mypy.strict = true`, `files = ["src/prometheus"]`) passes with no issues across all 82 source files. The Phase 4c edits to `state/__init__.py` and `state/transitions.py` preserve all type signatures; mypy result is identical to pre-Phase-4c.

---

## 11. Files changed

**Modified (2 files):**

- `src/prometheus/state/__init__.py` — reordered four relative-import lines alphabetically. Behavior preserved.
- `src/prometheus/state/transitions.py` — collapsed final `if incident_active: return True; return False` block to `return bool(incident_active)` in `_derive_entries_blocked`. Behavior preserved.

**Added (2 files; the closeout file is added in the next commit):**

- `docs/00-meta/implementation-reports/2026-04-30_phase-4c_state-package-ruff-residual-cleanup.md` (this report).
- `docs/00-meta/implementation-reports/2026-04-30_phase-4c_closeout.md` (Phase 4c closeout; added in the closeout commit).

**NOT modified:**

- All other `src/prometheus/**` source code (Phase 4a / Phase 4b deliverables preserved verbatim).
- All `tests/**`.
- All `scripts/**` (Phase 4b deliverables preserved verbatim).
- All `data/**` and `data/manifests/**`.
- All `docs/**` other than the two new Phase 4c artefacts.
- All `.claude/rules/**`.
- `pyproject.toml`.
- `.gitignore`.
- `.mcp.json`.
- `uv.lock`.
- `docs/00-meta/current-project-state.md` (preferred update only after merge per the Phase 4c brief).
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w / 3x / 4a / 4b reports / closeouts / merge-closeouts.

---

## 12. What this does not authorize

Phase 4c explicitly does NOT authorize, propose, or initiate any of the following:

- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 (canonical) requires Phase 3 strategy evidence which the project does not have.
- **Phase 4d or any successor phase.** Phase 4c is a tiny lint-only follow-up; the operator must explicitly authorize any successor.
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

Phase 4c is *lint-only quality-gate restoration* and limited to behavior-preserving edits in two specific files.

---

## 13. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4d / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement, no order cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4c performs no network I/O.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP / Graphify / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.** Existing `prometheus.strategy` modules untouched.
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
- **No threshold / parameter / project-lock modifications.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6 / §1.7.3 preserved verbatim.
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
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4c branch.** Per the Phase 4c brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No other `src/prometheus/**` modification beyond the two state-package files.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 14. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4c deliverables exist as branch-only artefacts pending operator review.
- **Phase 4c objective state:** narrowly-scoped objective (fix the 2 residual ruff issues in `src/prometheus/state/`) is **MET**; `ruff check .` (whole repo) now passes cleanly.
- **Repository quality gate state:** **fully restored.** Whole-repo `ruff check .` passes; pytest 785 passed; mypy strict 0 issues across 82 source files. The quality-gate restoration that Phase 4b began (scripts) is now completed by Phase 4c (state package).
- **5m research thread state:** Operationally complete and closed (Phase 3t). Unaffected.
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by Phase 4b and Phase 4c).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved by Phase 4b and Phase 4c).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved by Phase 4b and Phase 4c).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved by Phase 4b and Phase 4c).
- **OPEN ambiguity-log items after Phase 4c:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4c/state-package-ruff-residual-cleanup` exists locally and (after push) on `origin/phase-4c/state-package-ruff-residual-cleanup`. NOT merged to main.

---

## 15. Operator decision menu

The operator now has a Phase 4c branch with the 2 residual ruff issues in `src/prometheus/state/` cleaned up.

### 15.1 Option A — Merge Phase 4c to main and remain paused (PRIMARY recommendation)

Authorize a Phase 4c merge into main (analogous to the Phase 4b merge). After merge, the repository quality gate is fully clean: `ruff check .` passes cleanly across the whole repo. The project remains paused.

### 15.2 Option B — Defer the merge / leave Phase 4c on its branch (CONDITIONAL secondary; NOT RECOMMENDED)

Leave Phase 4c on its branch indefinitely. The 2 residual ruff issues remain on main as known technical debt. **Not recommended** because the fix is trivial and the gate is otherwise fully restorable.

### 15.3 Option C — Authorize unrelated runtime / strategy / live-readiness work (FORBIDDEN / NOT RECOMMENDED)

Out of Phase 4c's scope. Per `docs/12-roadmap/phase-gates.md` and the cumulative recommendation across Phase 3o → Phase 4b, these are not appropriate now.

### 15.4 Recommendation

**Phase 4c recommends Option A (merge to main and remain paused) as primary.** Option B is not recommended (the trivial gate-closing fix should not sit dormant). Option C is not recommended now.

---

## 16. Next authorization status

**No next phase has been authorized.** Phase 4c authorizes nothing other than producing this implementation report and the accompanying closeout artefact. Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase 4a). The Phase 4b script-scope quality-gate restoration is complete (per Phase 4b). The Phase 4c state-package quality-gate residual cleanup is complete on the Phase 4c branch (this phase). **Recommended state remains paused.**
