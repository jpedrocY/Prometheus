# Phase 4ax — Merge Closeout

**Phase identity:** Phase 4ax — AggTrades-Only Public Microstructure Collector Skeleton.
**Type:** code-and-docs collector-skeleton implementation phase.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the inert aggTrades-only collector skeleton from the Phase 4ax feature branch into `main`. The skeleton adds the next public-only microstructure implementation layer on top of the Phase 4aw scaffold: it validates mocked / offline aggTrade payloads (REST or stream-shaped), derives the taker side from the `m` (buyer-is-maker) flag, enforces the public-only endpoint allowlist with an additional aggTrades-shape guard, builds dry-run collection plans for archive / REST / WS modes, and (when explicitly given a caller-provided path) composes the Phase 4aw `RawWriter` to produce a finalised JSONL file plus paired SHA256 in pytest temp directories.

The merge does **not** acquire data, contact endpoints, open WebSockets, download archives, implement live REST clients, live WebSocket clients, real collectors, order-book reconstruction, deterministic replay, eligibility-gate execution, feature computation, strategies, or ML. It does **not** create the `data/microstructure/` directory, write under any project data path, or create real project manifests. It does **not** authorize any successor phase.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4ax/aggtrades-only-public-microstructure-collector-skeleton` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `6f929d2ce090600c486ecb6e7c571da1ae9ce5d5` |
| Phase 4ax skeleton commit | `b9f553c03277125f946d788890f0724e8e12b468` |
| Phase 4ax closeout commit | `e4622d4a7e3ab2fc5fb4a79ef7f8d86863720707` |
| Source branch HEAD | `e4622d4a7e3ab2fc5fb4a79ef7f8d86863720707` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff --no-commit` |

The merge commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

7 file changes, 2,008 insertions, 10 deletions.

**Added (4 new files):**

```
src/prometheus/research/microstructure/aggtrades.py
tests/research/microstructure/test_aggtrades.py

docs/00-meta/implementation-reports/2026-05-07_phase-4ax_aggtrades-only-public-microstructure-collector-skeleton.md
docs/00-meta/implementation-reports/2026-05-07_phase-4ax_closeout.md
```

**Modified (3 narrow updates):**

```
src/prometheus/research/microstructure/__init__.py     (re-export aggTrades scaffold symbols; docstring updated to reference Phase 4ax)
tests/research/microstructure/test_import_boundaries.py (Phase 4ax docstring note; +urllib.request and +socket forbidden-import patterns)
docs/00-meta/current-project-state.md                  (Phase 4ax narrative paragraph + new "Current phase:" block; prior Phase 4aw block preserved as historical context)
```

**Files NOT modified by the merge:**

- No file under `src/prometheus/` outside the microstructure package (only `__init__.py` and the new `aggtrades.py`).
- No Phase 4aw scaffold module other than `__init__.py` (re-exports only).
- No existing test outside `tests/research/microstructure/` (only `test_import_boundaries.py` was narrowly updated).
- No existing script under `scripts/` (Phase 3q / 3s / 4i / 4l / 4r / 4x / 4aq scripts all unchanged).
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, runtime doc, or governance memo.
- No `pyproject.toml`, `README.md`, or top-level config.
- No `.gitignore` change (the `data/microstructure/` line was already added by Phase 4aw).

---

## 5. Phase 4ax was collector-skeleton code-and-docs

**Confirmed.** Phase 4ax is a code-and-docs collector-skeleton implementation phase. Its scope was strictly limited to:

- one new inert source module (`aggtrades.py`) layered on top of the Phase 4aw scaffold;
- one new pytest test file (`test_aggtrades.py`, 46 tests) using `tmp_path` only;
- two narrow updates (`__init__.py` re-exports + docstring; `test_import_boundaries.py` docstring + `+urllib.request` + `+socket` forbidden-import patterns);
- two new docs files (memo + closeout);
- one narrow `current-project-state.md` update.

Verified by automated import-boundary and content-scan tests that the new module contains no live endpoint references, no credential paths, and no MCP / Graphify / `.mcp.json` / user stream / listenKey / order / account / position / leverage / margin / `forceOrders` REST references in code (docstrings and comments excluded from the scan are not source-active).

---

## 6. Phase 4ax aggTrades skeleton result summary

The skeleton installs one inert source module:

`aggtrades.py` defines:

- two `StrEnum`s: `TakerSide` (`BUY` / `SELL`), `AggTradeMode` (`ARCHIVE` / `REST` / `WS`);
- three frozen dataclasses: `AggTradePayload` (with `Decimal` price + quantity), `AggTradePlan`, `AggTradeWriteResult`;
- three custom exceptions: `AggTradesError` (base), `AggTradeValidationError`, `AggTradePlanError`;
- four pure functions: `validate_aggtrade_payload(payload)`, `assert_aggtrades_endpoint_allowed(endpoint)`, `build_aggtrades_plan(...)`, `write_validated_aggtrades_to_path(payloads, target_path)`.

The validator enforces required fields `a` / `p` / `q` / `f` / `l` / `T` / `m`, accepts optional stream `E`, requires `a` ≥ 0, requires `p` and `q` decimal-positive, requires `l` ≥ `f`, requires `T` > 0, requires strict `bool` for `m`, requires `E` > 0 if present, preserves unknown extra fields verbatim in `extra_fields`, and accepts int-shaped strings for integer-typed fields. Taker side is derived as `BUY` when `m=False` (seller is maker) and `SELL` when `m=True` (buyer is maker). The aggTrades-shape guard layers on top of the Phase 4aw `assert_endpoint_allowed`, requiring the endpoint to contain at least one of `/fapi/v1/aggTrades`, `@aggTrade`, or `aggtrade_ws`. The dry-run plan builder validates symbol (default `("BTCUSDT", "ETHUSDT")` or admitted via `explicit_extra_symbols`), validates mode, validates time range, validates dataset family, runs the aggTrades-shape guard on REST and WS endpoint references, creates no directories, contacts no endpoints, opens no streams, and returns a frozen `AggTradePlan`. The temp-path writer composes the Phase 4aw `RawWriter` (which refuses paths under `data/microstructure/` regardless of OS separator) to produce JSONL with `event_time_ms_source` label and derived `taker_side`, finalises atomically with paired SHA256, and returns an `AggTradeWriteResult` summary. On validation failure mid-stream, `AggTradeValidationError` is raised with the offending index and the `RawWriter.__exit__` cleanup releases the file handle without finalising — the final file is not produced.

### Source files added / modified

```
ADDED:    src/prometheus/research/microstructure/aggtrades.py
MODIFIED: src/prometheus/research/microstructure/__init__.py  (re-exports + docstring)
```

### Tests added / modified

```
ADDED:    tests/research/microstructure/test_aggtrades.py      (46 tests)
MODIFIED: tests/research/microstructure/test_import_boundaries.py  (+urllib.request +socket; Phase 4ax docstring)
```

The 46 tests cover: payload validation (REST + stream shapes; missing / invalid fields; extra fields preserved; payload type guard; int-shaped strings); taker-side derivation (both directions); allowlist + denylist dominance + aggTrades-shape guard (12 parametrised denylist + 3 explicit accept + 1 non-aggTrades-public reject); dry-run plans (archive / REST / WS modes; invalid mode / time range / unknown symbol / explicit extras / lowercase symbol / non-aggTrades dataset family); temp-path writer behaviour (JSONL + SHA256; stream `E` source label; project-data-path refusal; validation-error mid-stream produces no final file; non-Sequence rejected; no manifest creation; project-tree regression check). The existing parametrised `test_no_forbidden_imports` automatically scans `aggtrades.py` via `_scaffold_files()`.

### `.gitignore` unchanged

**Confirmed.** The `data/microstructure/` ignore line was already added by Phase 4aw; Phase 4ax did not modify `.gitignore`.

---

## 7. Boundary confirmations

The Phase 4ax merge confirms verbatim:

- **`data/microstructure/` was not created.** The directory did not exist before the merge, was not created during the merge, and does not exist after the merge. The Phase 4aw `.gitignore` line continues to protect against accidental future commits.
- **No project data writes occurred.** Tests use pytest `tmp_path` only. The Phase 4aw `RawWriter` enforces the project-data-path refusal across all OS separators.
- **No real manifests were created.** No file was written under `data/manifests/` or any project data tree. The `AggTradeWriteResult` summary is the explicit handoff contract for a future caller; manifest translation is **not** implemented.
- **No endpoint calls occurred.** No source file imports `httpx`, `requests`, `aiohttp`, `websockets`, `urllib.request`, `socket`, `binance`, `dotenv`, `python_dotenv`, or any signed-request helper. The import-boundary test enforces this.
- **No WebSockets were opened.** No WebSocket client is implemented.
- **No archive downloads occurred.** No code path retrieves public bulk archives.
- **No live REST clients, live WebSocket clients, real collectors, order-book reconstruction, deterministic replay, eligibility-gate execution, feature computation, strategy, or ML were implemented.** None of `public_rest.py`, `public_ws.py`, additional collector modules, normalizer modules, replay modules, eligibility-gate execution, healthcheck, dashboard hook, feature, strategy, or ML code exists.

---

## 8. Validation summary

Validation was performed on the Phase 4ax branch immediately before merge.

| Item | Result |
| ---- | ------ |
| `compileall src/prometheus/research/microstructure` | pass (7 modules) |
| `compileall tests/research/microstructure` | pass |
| Targeted ruff (`src/...microstructure tests/research/microstructure`) | `All checks passed!` |
| Whole-repo ruff | `All checks passed!` |
| Targeted microstructure tests (`pytest tests/research/microstructure`) | **161 passed** (Phase 4aw 114 + Phase 4ax 47 effective) |
| AggTrades tests (`pytest tests/research/microstructure/test_aggtrades.py`) | **46 passed** |
| Whole-repo pytest | **944 passed, 2 failed** (verified pre-existing on `main` before Phase 4ax — see below); **zero new regressions** from Phase 4ax |
| Targeted mypy (`mypy src/prometheus/research/microstructure`) | `Success: no issues found in 7 source files` |
| Whole-repo mypy strict | `Success: no issues found in 89 source files` (was 88 on main; +1 for `aggtrades.py`) |
| `git diff --check` | clean |
| `data/microstructure/` directory check | **DOES NOT EXIST** |

### Pre-existing whole-repo pytest failures

**Whole-repo pytest has 2 failures, both reproduced on main before Phase 4ax and unrelated to the aggTrades skeleton; Phase 4ax introduced zero new regressions.**

Both failures are in `tests/simulation/test_backtest_real_2026_03.py`:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`

Both fail with `KeyError: 'trade_count'` raised in the unrelated `src/prometheus/research/data/storage.py:232`. The failures were verified as pre-existing on `main` directly before Phase 4ax; they are also still present on `main` after the Phase 4aw merge. The Phase 4ax skeleton does not touch `src/prometheus/research/data/storage.py`, the simulation tests, or any related path.

---

## 9. Implementation / governance review

### What changed?

- One new source module (`aggtrades.py`), mypy strict clean (89 source files now in scope; +1 over Phase 4aw).
- One new test file (`test_aggtrades.py`, 46 tests).
- Two narrow updates: `__init__.py` re-exports + docstring; `test_import_boundaries.py` docstring + 2 additional forbidden-import patterns (`urllib.request`, `socket`).
- Two new docs files (memo + closeout).
- One narrow `current-project-state.md` update.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).
- No Phase 4ak / 4al / 4j / 3r / 3v / 3w governance.
- No Phase 4aw scaffold module beyond `__init__.py` re-exports.
- No data manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/`.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing test or script outside the narrowly-updated `test_import_boundaries.py`.
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Were any locks, verdicts, or safety boundaries affected?

No. The collector skeleton is inert. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4ax paragraph addition.

### Mergeability

The phase introduces only code that is verifiably inert (no network, no project data writes, no live endpoint calls, no successor authorisation), is fully covered by 46 new tests (161 total in the package), passes whole-repo ruff and mypy strict, and introduces zero new test regressions. The merge is a clean automatic merge (no conflicts) with `--no-ff` to preserve the Phase 4ax commit history.

---

## 10. Research interpretation review

### What did this phase prove?

That an aggTrades-only collector skeleton can be added on top of the Phase 4aw scaffold while preserving every safety boundary. Mocked / offline payload validation works for both REST-shaped and stream-shaped Binance aggTrade payloads. Taker-side derivation matches the Binance convention in both directions. The aggTrades-shape guard layered on top of the Phase 4aw allowlist correctly rejects every public-only-but-non-aggTrades endpoint (e.g. `@bookTicker`) and every private / authenticated / user-stream / listenKey / order / account / leverage / margin / `forceOrders` REST / credential-shaped reference. The dry-run plan returns a descriptive `AggTradePlan` without creating directories or touching the network. The temp-path writer atomically produces a JSONL file with paired SHA256 in pytest temporary directories while refusing project `data/microstructure/` paths and failing closed on validation errors mid-stream without leaving a finalised file behind.

### What did this phase NOT prove?

Anything about Binance microstructure data quality, edge, opportunity rate, or strategy viability. No specific endpoint behaviour was verified against the live exchange. Local order-book reconstruction was not implemented. The eligibility gate was not implemented. No historical strategy verdict changed. No project lock changed. Nothing about live readiness was demonstrated. The skeleton does not prove that real aggTrades acquisition will satisfy `Phase 3p §4.7` strict integrity gating (no acquisition was performed).

### What does this mean for strategy research?

The project now has tested aggTrades-shaped payload validation and a tested dry-run / temp-path writer composition. It does **not** create a strategy candidate, does **not** open any rescue path for cooled-down candidates (R2 / F1 / D1-A / V2 / G1 / C1), and does **not** authorize any feature derivation from aggTrades data. Phase 4ax is plumbing; strategy research stays under the binding M0 admissibility gate and the post-null cooldown rule.

### What does this mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, Phase 4j §11 OI subset governance, Phase 3r §8 mark-price gap governance, and Phase 3v §8 stop-trigger-domain governance all remain verbatim.

### Clean next step

After the merge, **remain paused**. The aggTrades-only collector skeleton is in place; no successor phase is authorized. If the operator separately wishes to advance, the most natural separately-authorized next step would be either (a) a docs-only Phase 4ay data-acquisition authorization memo or (b) a docs-and-code Phase 4ay public aggTrades archive acquisition under the strict integrity gate. None of these is authorized by this merge.

---

## 11. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other.
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

No verdict is revised by this merge.

---

## 12. Preserved project locks

- M0 governance remains binding prospectively only.
- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance).
- Phase 4j §11 (OI subset governance).
- Phase 4k V2 backtest-plan methodology.
- Phase 4p G1 strategy spec.
- Phase 4q G1 backtest-plan methodology.
- Phase 4v C1 strategy spec.
- Phase 4w C1 backtest-plan methodology.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am §11.A audit findings.
- Phase 4an inventory result.
- Phase 4ao harmonization result.
- Phase 4ap forensic plan.
- Phase 4aq computation result preserved as descriptive evidence only.
- Phase 4ar interpretation result preserved as descriptive interpretation only.
- Phase 4as mechanism-map result preserved as docs-only reset evidence only.
- Phase 4at availability / capture-feasibility result preserved as docs-only feasibility evidence only.
- Phase 4au capture-design result preserved as docs-only design evidence only.
- Phase 4av implementation-plan result preserved as docs-only planning evidence only.
- Phase 4aw scaffold result preserved as scaffold-only infrastructure evidence only.
- Phase 4ax aggTrades skeleton result preserved as collector-skeleton infrastructure evidence only.

No new lock is introduced. No existing lock is loosened.

---

## 13. No-rescue constraints (preserved)

- No R3-prime / R3 next-spec / R3 rescue / baseline-of-record revision.
- No R1a-prime / R1a promotion to leading.
- No R1b-narrow-prime / R1b-narrow promotion to leading.
- No R2-prime / R2 rescue / R2 cheaper-cost rerun.
- No H0-prime / framework-anchor revision.
- No F1-prime / F1 rescue / F1 profitable-subset rescue.
- No D1-A-prime / D1-A extra-filter / D1-B / V1-D1 hybrid / F1-D1 hybrid.
- No V2-prime / V2-narrow / V2-relaxed / V2 hybrid.
- No G1-prime / G1-narrow / G1-extension / G1 hybrid / G1 classifier relaxation.
- No C1-prime / C1-narrow / C1-extension / C1 hybrid.
- No cross-strategy hybrid of any kind.
- No 5m thread reopening.
- No 5m strategy / hybrid / retained-evidence successor.
- No conversion of Phase 4aq forensic numbers, Phase 4l V2 forensic numbers, Phase 4r G1 active-fraction numbers, or Phase 4x C1 forensic numbers into parameter-selection inputs.
- No M0 amendment derived from Phase 4ax reasoning.

---

## 14. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4ay,
- Phase 5,
- Phase 4 canonical,
- data acquisition (real aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book),
- Binance endpoint calls,
- public-archive downloads,
- WebSocket connections,
- live REST implementation,
- live WebSocket implementation,
- data-capture implementation,
- order-book reconstruction implementation,
- replay implementation,
- eligibility-gate execution,
- feature implementation,
- ML model creation,
- strategy candidate creation,
- entry / exit design,
- old-strategy alt-symbol reruns,
- R3 / R2 / V1-arc rescue,
- 5m research thread reopening,
- paper / shadow,
- live-readiness,
- deployment,
- exchange-write,
- production keys,
- authenticated APIs,
- private endpoints,
- user stream,
- MCP, Graphify, `.mcp.json`,
- credentials.

Any successor phase requires a separate operator authorization brief. Phase 4ay (whether docs-only data-acquisition authorization memo or docs-and-code public aggTrades archive acquisition under the strict integrity gate) is documented as a possible future path but is **not** activated by this merge.

---

## 15. Recommended state

**Recommended state remains paused.** The Phase 4ax aggTrades-only collector skeleton is now available on `main` for any future separately-authorized phase to build upon. No further work should occur until the operator separately authorizes a future phase.

---

## 16. Final note

This merge-closeout is preserved alongside the Phase 4ax memo and the Phase 4ax closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4ax commit history is preserved and the boundary between Phase 4aw (scaffold) and Phase 4ax (aggTrades skeleton) remains visible in `git log`.

**Phase 4ax is now merged into `main`. No next phase is authorized.**
