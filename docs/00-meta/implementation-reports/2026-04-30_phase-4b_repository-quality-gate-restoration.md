# Phase 4b — Repository Quality Gate Restoration

**Authority:** Phase 4a (Local Safe Runtime Foundation) merge closeout's documented quality gap (29 pre-existing ruff issues in Phase 3q / Phase 3s standalone scripts); `pyproject.toml` ruff configuration; `.claude/rules/prometheus-core.md`; `.claude/rules/prometheus-safety.md`; `.claude/rules/prometheus-mcp-and-secrets.md`.

**Phase:** 4b — **Repository Quality Gate Restoration.** Targeted code-hygiene phase to make full-repo Ruff pass by fixing the known pre-existing Ruff issues in the Phase 3q / Phase 3s standalone scripts. **Phase 4b is quality-gate restoration only.**

**Branch:** `phase-4b/repository-quality-gate-restoration`. **Phase date:** 2026-04-30 UTC.

---

## 1. Summary

Phase 4b fixes all 29 known pre-existing ruff issues in `scripts/phase3q_5m_acquisition.py` (16 issues) and `scripts/phase3s_5m_diagnostics.py` (13 issues). All edits are behavior-preserving lint-only changes: removed unused imports, renamed unused loop variables, added `strict=` to `zip()` calls, renamed the ambiguous `l` (lowercase L) variable to `lo`, converted one `if`/`else` block to a ternary expression, and split long lines.

**Test evidence (all required commands ran on the project's `.venv`, Python 3.12.4):**

- `ruff check scripts`: **All checks passed!** (29 known issues fixed).
- `ruff check .`: **2 errors remain** in Phase 4a code (`src/prometheus/state/__init__.py` I001 import-order; `src/prometheus/state/transitions.py:49` SIM103 `return bool(incident_active)`). These two errors are *pre-existing* relative to Phase 4b — they were latent in the Phase 4a merge to main; they are NOT caused by the Phase 4b script edits (verified by `git stash` + `ruff check .` on the unmodified post-Phase-4a-merge tree, which reported 31 errors: 29 in scripts + the same 2 in `state/`). They are explicitly **out of scope for Phase 4b** per the brief's strict constraint *"Do not modify runtime Phase 4a code unless a quality command reveals a direct import/export break caused by the script cleanup, which is not expected"*. Phase 4b documents these 2 residual issues honestly and recommends a separately-authorized follow-up phase to address them; Phase 4b does not fix them.
- `pytest -q`: **785 passed in 13.53s.** No regressions.
- `mypy`: **Success: no issues found in 82 source files.**

**Phase 4b is quality-gate restoration only.** Phase 4b does not expand runtime functionality, does not implement strategy logic, does not run backtests, does not run diagnostics, does not acquire / patch / regenerate / modify data, does not modify data manifests, does not authorize paper/shadow, does not authorize live-readiness, does not authorize deployment, does not authorize production keys, does not authorize authenticated APIs / private endpoints / user stream / WebSocket / MCP / Graphify / `.mcp.json` / credentials / exchange-write, does not validate any strategy, does not revise any verdict, and does not change any lock.

---

## 2. Authority and boundary

Phase 4b operates strictly inside the post-Phase-4a-merge boundary:

- **Predeclaration discipline preserved verbatim.** Phase 3o §5–§10; Phase 3p §4–§8; Phase 3r §8; Phase 3s diagnostic outputs; Phase 3t consolidation; Phase 3u §10 / §11; Phase 3v §8 (stop-trigger-domain governance); Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance); Phase 3x §6 / §10 (Phase 4a prohibition list); Phase 4a's anti-live-readiness statement.
- **Phase-gate governance respected.** `docs/12-roadmap/phase-gates.md` unchanged.
- **Project-level locks preserved verbatim.** §1.7.3 (BTCUSDT primary live; ETHUSDT research/comparison only; one-symbol-only live; one-position max; 0.25% risk; 2× leverage cap; **mark-price stops**; v002 datasets).
- **Phase 2f thresholds preserved verbatim.** §10.3 / §10.4 / §11.3 / §11.4 / §11.6.
- **Retained-evidence verdicts preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other.
- **Safety rules preserved verbatim.** `.claude/rules/prometheus-safety.md`.
- **MCP and secrets rules preserved verbatim.** `.claude/rules/prometheus-mcp-and-secrets.md`.
- **Phase 4a runtime code preserved verbatim.** Phase 4b does not modify any file under `src/prometheus/`, `tests/`, or any runtime artefact.

Phase 4b modifies *only* the two scripts (lint-only) plus the two documentation artefacts (this report + the closeout).

---

## 3. Starting state

```text
branch:           phase-4b/repository-quality-gate-restoration
parent commit:    829c25ab9f90e8103ed966a8b07f9fc4d2d5312c (post-Phase-4a-merge housekeeping)
working tree:     clean before implementation
main:             829c25ab9f90e8103ed966a8b07f9fc4d2d5312c (unchanged)

ruff (pre-edit, full repo): 31 errors
  - 29 in scripts/phase3q_5m_acquisition.py + scripts/phase3s_5m_diagnostics.py
    (the explicitly-named Phase 4b target).
  - 2 latent in src/prometheus/state/ (state/__init__.py I001 import order;
    state/transitions.py:49 SIM103 return bool). NOT named in the Phase 4b
    brief; out of scope per brief's strict constraint on Phase 4a code.
mypy:             pre-edit clean (82 source files, 0 issues).
pytest:           pre-edit 785/785 passing.
```

---

## 4. Quality gap being addressed

The Phase 4a merge closeout documented that `ruff check .` reported 29 errors in the Phase 3q + Phase 3s standalone orchestrator scripts. Phase 4a's report categorized these as pre-existing issues unchanged by Phase 4a; the Phase 4b brief authorized a targeted clean-up.

The 29 known issues by rule category (verified by `ruff check scripts --output-format=concise` at Phase 4b start):

| Rule | Count | Notes |
|---|---|---|
| E501 (line too long > 100) | 18 | 7 in phase3q + 11 in phase3s. |
| F401 (unused import) | 3 | `datetime.datetime`, `datetime.timezone` (phase3q); `dataclasses` (phase3s). |
| B905 (`zip()` without `strict=`) | 3 | All in phase3q OHLC / volume sanity loops. |
| B007 (unused loop control variable) | 2 | `attempt` (phase3q backoff loop); `ot` (phase3s 5m bar iter). |
| E741 (ambiguous variable name `l`) | 2 | One in each script's OHLC loop. |
| SIM108 (use ternary instead of if/else) | 1 | phase3q `family == "klines"` branch. |
| **Total** | **29** | All confirmed fixable with behavior-preserving edits. |

---

## 5. Files inspected

- `scripts/phase3q_5m_acquisition.py` — full-file scan; identified 16 issue locations (lines 15, 16, 36, 36, 104, 225, 277, 437, 544, 562, 562, 576, 652, 723, 757, plus column-shifts after each edit).
- `scripts/phase3s_5m_diagnostics.py` — full-file scan; identified 13 issue locations (lines 25, 88, 252, 489, 552, 562, 600, 601, 630, 639, 640, 641, 657, 658).
- `pyproject.toml` — ruff configuration (`select = ["E", "F", "W", "I", "UP", "B", "SIM"]`, `line-length = 100`, `target-version = "py311"`, `extend-exclude = [".venv", "research/data", "configs", "docs", "infra", "notebooks"]`). No per-file-ignores; rules apply uniformly.
- `.claude/rules/prometheus-core.md`, `prometheus-safety.md`, `prometheus-mcp-and-secrets.md` — read for boundary preservation.

---

## 6. Changes made

### 6.1 `scripts/phase3q_5m_acquisition.py`

| Issue | Rule | Fix |
|---|---|---|
| Module docstring URL examples (lines 15–16) | E501 | Split the two long URL example lines onto separate `Outputs:` bullets. The URLs are documentation-only; layout change does not affect behavior. |
| `from datetime import datetime, timezone` (line 36) | F401 (×2) | Removed the `datetime` import line entirely. Neither symbol was used elsewhere in the script; verified by `grep -n datetime scripts/phase3q_5m_acquisition.py`. |
| `for attempt in range(...)` in `http_get` (line 104) | B007 | Renamed loop variable to `_attempt`. The variable was not used inside the loop body; the underscore prefix is the conventional "unused" marker. |
| `f"{zip_path} line {index}: expected {KLINE_COLUMNS_EXPECTED} cols, got {len(parts)}"` (lines 225 + 277, two identical occurrences in `parse_kline_zip` and `parse_markprice_zip`) | E501 (×2) | Split each `f"..."` literal onto two adjacent string literals (Python concatenates adjacent string literals at parse time). The runtime message is identical. |
| `if family == "klines": rows = parse_kline_zip(rp)` else `parse_markprice_zip(rp)` (line 437) | SIM108 | Converted to single-line ternary: `rows = parse_kline_zip(rp) if family == "klines" else parse_markprice_zip(rp)`. Behavior identical; both branches return `list[dict[str, Any]]`. |
| `zip(open_times, close_times)` (line 544) | B905 | Added `strict=True`. The two lists are guaranteed equal-length by construction (both come from the same parsed-row sequence in `integrity_check_dataset`). Adding `strict=True` makes the contract explicit and is safer (raises if invariant breaks); no behavior change in valid input. |
| `for o, h, l, c in zip(opens, highs, lows, closes)` (line 562) | E741 + B905 | Renamed `l` → `lo` throughout the OHLC sanity loop (4 references inside the loop body). Added `strict=True` to the `zip(...)`. The semantics are identical: `lo` still references the low values. |
| `for v, qv, tc in zip(volumes, qvols, tcounts)` (line 576) | B905 | Added `strict=True`. Same equal-length-by-construction guarantee as line 544. |
| Manifest `notes` f-string `Months: ...` (line 652) | E501 | Split the long line into two adjacent f-string literals. Manifest output text is unchanged. |
| Progress print `f"[{n_done}/{n_total}] {family} {symbol} ..."` (line 723) | E501 | Split into three adjacent f-string literals. Output text is unchanged. |
| Final print `f"Phase 3q acquisition + integrity validation complete. {len(manifest_paths)} manifests written."` (line 757) | E501 | Split into a multi-line `print(...)` call with two adjacent f-string literals. Output text is unchanged. |

**Total phase3q edits:** 11 distinct edits covering 16 ruff diagnostics (some edits address multiple diagnostics at once — e.g., the OHLC-loop edit fixed both E741 and B905; the docstring-URL edit fixed two adjacent E501s).

### 6.2 `scripts/phase3s_5m_diagnostics.py`

| Issue | Rule | Fix |
|---|---|---|
| `import dataclasses` (line 25) | F401 | Removed. Verified by `grep` that `dataclasses.` is not referenced elsewhere in the script. |
| `l = combined.column("low").to_pylist()` (line 88) | E741 | Renamed `l` → `lo`. Updated the one downstream reference at the original line 99 (`"low": float(l[i])` → `"low": float(lo[i])`). Verified no other references via `grep -nE "\\bl\\b"`. |
| `for ot, b in iter_5m_bars(...)` (line 252) | B007 | Renamed loop variable to `_ot`. The `ot` was not used inside the loop body. |
| Long `print(f"loaded {sym}: ...")` line (line 489) | E501 | Split into a multi-line `print(...)` call with two adjacent f-string literals. Output text unchanged. |
| `q6_results.append({"sym": sym, "direction": tr["direction"], "exit_reason": tr["exit_reason"], **q6})` (line 552) | E501 | Reformatted to a multi-line dict literal. Behavior identical. |
| `"n_trades_by_symbol": {sym: sum(1 for tr in trades if tr["symbol"] == sym) for sym in SYMBOLS}` (line 562) | E501 | Reformatted dict-comprehension onto multiple lines. Behavior identical. |
| `"intrabar_1r_fraction" / "intrabar_2r_fraction"` ternaries (lines 600 + 601) | E501 (×2) | Reformatted each ternary across multiple lines. Behavior identical. |
| `included = [r for r in applicable if not r["excluded"] and r["mark_minus_trade_5m_bars"] is not None]` (line 630) | E501 | Reformatted list-comprehension across multiple lines. Behavior identical. |
| Q6 fraction ternaries `fraction_simultaneous_trigger / fraction_mark_lags_trade / fraction_mark_leads_trade` (lines 639–641) | E501 (×3) | Reformatted each ternary onto multiple lines. Behavior identical. |
| `"n_inconclusive_5m_trigger": len(applicable) - len(excluded) - len(included)` (this line was originally short but became a sibling in the same dict; included for consistency in the multi-line block) | — | Reformatted across multiple lines as part of the surrounding dict-literal reflow. No ruff diagnostic; cosmetic consistency. |
| Final `(OUT / "...").write_text(json.dumps(..., default=str), encoding="utf-8")` lines (lines 657 + 658) | E501 (×2) | Reformatted each `write_text(...)` call across multiple lines. Behavior identical. |

**Total phase3s edits:** 9 distinct edits covering 13 ruff diagnostics.

---

## 7. Behavior-preservation notes

All Phase 4b edits are behavior-preserving by construction:

1. **Removed unused imports** (`datetime.datetime`, `datetime.timezone`, `dataclasses`) — no callsite uses these symbols, so removal cannot affect runtime behavior. Verified by full-file `grep`.
2. **Renamed unused loop variables** (`attempt` → `_attempt`; `ot` → `_ot`) — the variables were not referenced inside their loops; only the for-loop binding name changes. Identical iteration count; identical loop body.
3. **Added `strict=True` to `zip()`** — Python's `strict=` parameter raises `ValueError` if the iterables have different lengths; otherwise behavior is identical. The three call sites all consume lists that are guaranteed equal-length by construction (they come from the same parsed-row sequence in `integrity_check_dataset`); under valid input the strict check never fires. The change makes the equal-length contract explicit at the type-checker / lint layer.
4. **Renamed `l` → `lo`** (both scripts' OHLC loops + the phase3s `load_5m_klines` low-price array) — same value bound to a different identifier; downstream references updated atomically. No semantic change.
5. **`if`/`else` → ternary** for the `family == "klines"` branch in phase3q `acquire_one_month` — Python evaluates ternary and if/else identically when both branches assign the same target variable. Verified the old and new produce the same `rows: list[dict[str, Any]]`.
6. **Adjacent f-string literal splits and multi-line reformat** — Python's parser concatenates adjacent string literals at compile time; the resulting bytecode is identical for the f-string output text. For the dict-literal / list-comprehension reformats, the AST is structurally identical with only whitespace changes; runtime behavior is identical.

No script is executed during Phase 4b. The brief's forbidden-work list explicitly prohibits running `scripts/phase3q_5m_acquisition.py` and `scripts/phase3s_5m_diagnostics.py`; Phase 4b honours this by relying on `ruff check`, `mypy`, and the existing `pytest` suite (which does not import these standalone orchestrator scripts) for verification. Phase 4b does not download data, does not touch data files, and does not touch manifests.

---

## 8. Commands run

All commands run from `c:\Prometheus` against the project's `.venv` (Python 3.12.4):

```text
git status
git rev-parse HEAD
git rev-parse origin/main
git checkout -b phase-4b/repository-quality-gate-restoration
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check scripts
.venv/Scripts/python -m ruff check scripts/phase3q_5m_acquisition.py
.venv/Scripts/python -m ruff check scripts/phase3s_5m_diagnostics.py
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m pytest
.venv/Scripts/python -m mypy
git stash       # used once to verify the 2 state/ ruff issues exist independent of Phase 4b edits
git stash pop
git diff --stat
```

No format-check command is configured separately by the project (`tool.ruff.format` exists but `ruff format --check` is not part of the documented project workflow). Phase 4b does not invent a format step. No script (`scripts/phase3q_5m_acquisition.py`, `scripts/phase3s_5m_diagnostics.py`) was run. No data was acquired, downloaded, or modified. No network I/O was performed.

---

## 9. Test results

**`pytest -q`:**

```text
785 passed in 13.53s
```

No regressions; identical pass count to the pre-Phase-4b state on main (785/785). The two scripts are not imported by any test (they are standalone orchestrators); the script edits therefore have no test footprint.

---

## 10. Ruff results

**`ruff check scripts`:**

```text
All checks passed!
```

All 29 known pre-existing ruff issues in the two standalone scripts are now resolved. The Phase 4b objective is met for the explicitly-named target.

**`ruff check .` (whole repo):**

```text
Found 2 errors.
```

The 2 residual errors are:

1. **`src/prometheus/state/__init__.py:20:1` — I001** *Import block is un-sorted or un-formatted.* The block imports `from .errors`, `from .mode`, `from .control`, `from .transitions` — ruff's I001 rule wants `.control` before `.errors` (alphabetical order). One-line fix when authorized.
2. **`src/prometheus/state/transitions.py:49:5` — SIM103** *Return the condition `bool(incident_active)` directly.* The `_derive_entries_blocked` function ends with `if incident_active: return True; return False` instead of `return bool(incident_active)`. Two-line collapse when authorized.

**Both errors are pre-existing relative to Phase 4b.** Verification: with the Phase 4b script edits stashed (`git stash`), `ruff check .` on the unmodified post-Phase-4a-merge tree reported **31 errors** (29 in `scripts/` + 2 in `state/`). After the stash was popped (Phase 4b script edits restored), the count became 2 (the same 2 in `state/`).

These 2 errors were latent during Phase 4a's verification: Phase 4a's report ran `ruff check src/prometheus tests/unit/runtime` and `ruff check .` and reported "All checks passed!" for the former and "Found 29 errors" for the latter. The scoped command apparently did not flag the 2 issues; a fresh re-run of the *same* scoped command at Phase 4b start now reports the 2 issues. The most likely root cause is ruff cache state during Phase 4a; the issues are real and present at HEAD.

**Phase 4b does NOT fix these 2 errors.** Per the Phase 4b brief's strict constraint: *"Do not modify runtime Phase 4a code unless a quality command reveals a direct import/export break caused by the script cleanup, which is not expected."* The 2 errors are not import/export breaks and are not caused by the Phase 4b script cleanup; they are pre-existing in Phase 4a code. Phase 4b documents them honestly and recommends a separately-authorized follow-up phase (e.g., `phase-4c/state-package-lint-residual`) to address them. **Phase 4b does NOT invent success.**

---

## 11. Mypy results

```text
Success: no issues found in 82 source files
```

Mypy strict (per `tool.mypy.strict = true`, `files = ["src/prometheus"]`) passes with no issues across all 82 source files. Phase 4b's edits to `scripts/` are not in mypy's scope (the configured `files` is `src/prometheus` only); the mypy result is identical to pre-Phase-4b.

---

## 12. Files changed

**Modified (2 files):**

- `scripts/phase3q_5m_acquisition.py` — 11 distinct lint-only edits covering 16 ruff diagnostics. Behavior preserved.
- `scripts/phase3s_5m_diagnostics.py` — 9 distinct lint-only edits covering 13 ruff diagnostics. Behavior preserved.

**Added (2 files; the closeout file is added in the next commit):**

- `docs/00-meta/implementation-reports/2026-04-30_phase-4b_repository-quality-gate-restoration.md` (this report).
- `docs/00-meta/implementation-reports/2026-04-30_phase-4b_closeout.md` (Phase 4b closeout; added in the closeout commit).

**NOT modified:**

- All `src/prometheus/**` — Phase 4a runtime code preserved verbatim, including the 2 latent ruff issues in `state/__init__.py` and `state/transitions.py` (out of Phase 4b scope).
- All `tests/**`.
- All `data/**` and `data/manifests/**`.
- All `docs/**` other than the two new Phase 4b artefacts.
- All `.claude/rules/**`.
- `pyproject.toml`.
- `.gitignore`.
- `.mcp.json`.
- `uv.lock`.
- `docs/00-meta/current-project-state.md` (not modified on the Phase 4b branch per the brief; preferred update only after merge).
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w / 3x / 4a reports / closeouts / merge-closeouts.

---

## 13. What this does not authorize

Phase 4b explicitly does NOT authorize, propose, or initiate any of the following:

- **Phase 4 (canonical) authorization.** Per `docs/12-roadmap/phase-gates.md`, Phase 4 (canonical) requires Phase 3 strategy evidence which the project does not have. Phase 4b is a quality-gate-restoration phase; it is not Phase 4.
- **Phase 4c or any successor phase.** Phase 4b's discovery of 2 residual ruff issues in Phase 4a code does NOT authorize a follow-up phase by itself; the operator must explicitly authorize any successor.
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

Phase 4b is *quality-gate restoration only* and limited to behavior-preserving lint-only edits in two specific scripts.

---

## 14. Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4c / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement, no order cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4b performs no network I/O.
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
- **No backtests run.** No H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A run executed.
- **`scripts/phase3q_5m_acquisition.py` not run.** Per brief.
- **`scripts/phase3s_5m_diagnostics.py` not run.** Per brief.
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
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4b branch.** Per the Phase 4b brief.
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.** Phase 4a runtime code preserved verbatim. The 2 latent ruff issues in `state/__init__.py` and `state/transitions.py:49` are explicitly NOT fixed by Phase 4b per the brief's strict-constraint clause.
- **No `tests/**` modification.**
- **No merge to main.**
- **No successor phase started.**

---

## 15. Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase 4b deliverables exist as branch-only artefacts pending operator review.
- **Phase 4b objective state:** The narrowly-scoped Phase 4b objective (fix 29 known pre-existing ruff issues in the two standalone scripts) is **MET**; `ruff check scripts` passes cleanly.
- **Repository quality gate state:** `ruff check .` (whole-repo) reports **2 residual errors in Phase 4a code** that were latent at the start of Phase 4b (verified by stash test). These 2 errors are out of Phase 4b's authorized scope. Closing them requires separate operator authorization. The repository quality gate is therefore *partially* restored: the explicitly-named scripts portion is clean; 2 latent errors in Phase 4a code remain.
- **5m research thread state:** Operationally complete and closed (Phase 3t). Unaffected by Phase 4b.
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged; Phase 4b is quality-gate cleanup only.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by Phase 4b).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved by Phase 4b).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved by Phase 4b).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved by Phase 4b).
- **OPEN ambiguity-log items after Phase 4b:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:** `phase-4b/repository-quality-gate-restoration` exists locally and (after push) on `origin/phase-4b/repository-quality-gate-restoration`. NOT merged to main.

---

## 16. Operator decision menu

The operator now has a Phase 4b branch with the 29 known pre-existing script ruff issues cleaned up. The next operator decision is operator-driven only.

### 16.1 Option A — Review on branch and merge Phase 4b to main, then remain paused (PRIMARY recommendation)

Authorize a Phase 4b merge into main (analogous to the Phase 3o → 3w / 3x → 4a merge pattern). After merge, the project remains paused. The 2 residual ruff issues in Phase 4a code remain documented as a known quality gap; they are not pre-coding blockers for any specific successor phase, but they are visible debt.

### 16.2 Option B — Merge Phase 4b plus authorize a narrow follow-up `phase-4c/state-package-lint-residual` (CONDITIONAL secondary)

After merging Phase 4b, authorize a *very narrow* follow-up phase to fix the 2 residual ruff issues in `src/prometheus/state/__init__.py` and `src/prometheus/state/transitions.py`. Scope: 2 lint-only behavior-preserving edits, identical pattern to Phase 4b. Estimated effort: < 5 minutes. Output: `ruff check .` reports zero errors.

### 16.3 Option C — Defer the 2 residual issues indefinitely (CONDITIONAL tertiary)

Accept the 2 residual ruff issues as documented technical debt; do not authorize a follow-up phase. The repository quality gate is "partially clean — scripts are clean, Phase 4a state package has 2 known issues."

### 16.4 Option D — Do not merge Phase 4b (CONDITIONAL alternative; NOT RECOMMENDED)

Leave Phase 4b on its branch indefinitely without merging. The 29 known script issues remain on main as documented technical debt; the Phase 4b branch sits dormant.

### 16.5 Option E — Authorize unrelated runtime / strategy / live-readiness work (FORBIDDEN / NOT RECOMMENDED)

Out of Phase 4b's scope. Per `docs/12-roadmap/phase-gates.md` and the cumulative Phase 3o → Phase 4a recommendations, these are not appropriate now.

### 16.6 Recommendation

**Phase 4b recommends Option A (merge to main and remain paused) as primary.** Option B (merge plus authorize narrow `phase-4c/state-package-lint-residual` follow-up) is acceptable as conditional secondary if the operator wants to fully close the quality gate. Option C is acceptable as conditional tertiary if the operator considers the 2 residual issues immaterial. Option D is not recommended (the 29-issue debt should not persist on main when Phase 4b has clean fixes ready). Option E is not recommended now.

---

## 17. Next authorization status

**No next phase has been authorized.** Phase 4b authorizes nothing other than producing this implementation report and the accompanying closeout artefact (the implementation itself was authorized by the operator brief that opened Phase 4b; that authorization is now spent on this phase).

Selection of any subsequent phase (Phase 4b merge per Option A; narrow `phase-4c/state-package-lint-residual` follow-up per Option B; defer per Option C; do-not-merge per Option D; runtime / strategy / live-readiness work per Option E) requires explicit operator authorization for that specific phase. No such authorization has been issued.

The 5m research thread remains operationally complete and closed (per Phase 3t). The implementation-readiness boundary remains reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding governance blockers remain RESOLVED at the governance level (per Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented (per Phase 4a). The Phase 4b script-scope quality-gate restoration is complete on the Phase 4b branch (this phase). **Recommended state remains paused.**
