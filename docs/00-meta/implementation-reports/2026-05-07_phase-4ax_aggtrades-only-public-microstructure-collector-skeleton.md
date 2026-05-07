# Phase 4ax — AggTrades-Only Public Microstructure Collector Skeleton

**Type:** code-and-docs collector-skeleton implementation phase.
**Status:** drafted on branch `phase-4ax/aggtrades-only-public-microstructure-collector-skeleton`; pending operator review and merge approval.
**Date:** 2026-05-07.

---

## 1. Executive summary

Phase 4ax adds the next inert public-only microstructure implementation layer on top of the Phase 4aw scaffold: an **aggTrades-only collector skeleton** that validates mocked / offline aggTrade payloads, derives the taker side from the `m` (buyer-is-maker) flag, enforces the public-only endpoint allowlist with an aggTrades-shape guard, builds dry-run collection plans, and (when explicitly given a caller-provided path) composes the Phase 4aw `RawWriter` to produce a finalised JSONL file plus paired SHA256 in pytest temp directories.

The skeleton is inert: it does **not** acquire data, contact endpoints, open WebSockets, download archives, write under `data/microstructure/`, create real manifests, run collectors, run features, run strategies, run ML, or authorize any successor phase.

Phase 4ax was derived from Phase 4aw (scaffold + merge-closeout), Phase 4av (implementation plan), Phase 4au (capture design), Phase 4at (data availability / capture feasibility), Phase 4as (mechanism reset), Phase 4ar (V1-arc forensic interpretation), Phase 4ak (M0 governance), Phase 4al (refined no-rescue rule + data-resolution hierarchy), Phase 4j §11 (OI subset governance), Phase 3r §8 (mark-price gap governance), Phase 3v §8 (stop-trigger-domain governance), and Phase 3t (5m thread closure).

Phase 4ax preserves every retained verdict and every project lock. It does not authorize Phase 4ay, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, or any data acquisition (5m, 1m, real aggTrades data, tick, mark-price 30m / 4h, order-book).

---

## 2. Scope and explicit non-scope

### Allowed (and performed) in Phase 4ax

- Add `src/prometheus/research/microstructure/aggtrades.py` (one new source module).
- Add `tests/research/microstructure/test_aggtrades.py` (one new test file, 46 tests).
- Update `src/prometheus/research/microstructure/__init__.py` to re-export the new aggTrades scaffold symbols.
- Update `tests/research/microstructure/test_import_boundaries.py` to (a) reflect Phase 4ax in its module docstring and (b) extend the forbidden-import scan list with `urllib.request` and `socket`. The existing `_scaffold_files()` helper auto-discovers every `*.py` in the package, so `aggtrades.py` is automatically included in every parametrised import-boundary scan.
- Add Phase 4ax memo and closeout under `docs/00-meta/implementation-reports/`.
- Update `docs/00-meta/current-project-state.md` narrowly.

### Forbidden (and not performed) in Phase 4ax

- Acquire real data of any kind.
- Call Binance endpoints.
- Open WebSockets.
- Download public archive files.
- Create the `data/microstructure/` directory.
- Write raw files under any project data path.
- Create real project manifests.
- Implement live REST client behaviour.
- Implement live WebSocket client behaviour.
- Implement order-book reconstruction.
- Implement deterministic replay beyond design references.
- Implement normalizers beyond minimal aggTrades schema validation.
- Implement eligibility-gate execution.
- Implement feature computation.
- Compute predictive statistics.
- Run backtests, historical strategy scripts, Phase 4aq or any prior research script, or simulations.
- Modify existing data, manifests, trade logs, strategy specs, thresholds, governance docs, retained verdicts, project locks, or prior research reports beyond the new Phase 4ax docs and the narrow `current-project-state.md` update.
- Create a strategy candidate, design entries or exits, or create an ML model.
- Authorize any successor phase.

---

## 3. Repository verification summary

Before branching:

- Branch: `main`.
- Working tree: clean (only gitignored `.claude/scheduled_tasks.lock` and `data/research/` untracked).
- `git rev-parse main` and `git rev-parse origin/main` both `6f929d2ce090600c486ecb6e7c571da1ae9ce5d5`.
- All Phase 4aw scaffold files present on main: `__init__.py`, `config.py`, `allowlist.py`, `invalid_window.py`, `manifest.py`, `raw_writer.py`.
- Phase 4aw memo, closeout, and merge-closeout all present under `docs/00-meta/implementation-reports/`.
- `.gitignore` line `data/microstructure/` present.
- `data/microstructure/` does not exist.

Phase 4ax branch `phase-4ax/aggtrades-only-public-microstructure-collector-skeleton` was created from this clean base.

---

## 4. Methodology

Phase 4ax is a collector-skeleton implementation. It was constructed under the following methodology:

- **Mocked / offline payload validation only.** Tests construct REST-shaped and stream-shaped Binance aggTrade payloads as plain Python `dict`s and feed them to the validator.
- **No endpoint calls.** No source file imports `httpx`, `requests`, `aiohttp`, `websockets`, `urllib.request`, `socket`, or any Binance SDK.
- **No WebSockets.** No WebSocket client is implemented.
- **No archive downloads.** No code path retrieves public bulk archives.
- **No real data acquisition.** No code path writes raw event data under any project data path.
- **No project data writes.** Tests use pytest `tmp_path` only. The Phase 4aw `RawWriter` enforces the project-data-path refusal.
- **No real manifests.** The `AggTradeWriteResult` summary is the explicit handoff contract for a future caller; manifest translation is **not** implemented in Phase 4ax.
- **Dry-run planning only.** `build_aggtrades_plan(...)` returns a frozen `AggTradePlan` describing the future plan without creating directories or touching the network.
- **No strategies.** No strategy logic exists.
- **No ML.** No machine-learning code exists.
- **No successor authorization.** Phase 4ax does not authorize Phase 4ay or any other successor phase.

---

## 5. Phase 4aw baseline preserved

The Phase 4ax skeleton is layered on top of (and reuses) the Phase 4aw scaffold:

- `allowlist.py` — `assert_endpoint_allowed`, `is_endpoint_denied`, `is_endpoint_allowed`, `EndpointNotAllowedError` are reused unchanged. The aggTrades-specific guard `assert_aggtrades_endpoint_allowed` first defers to the Phase 4aw allowlist and then enforces the additional constraint that the endpoint must contain an aggTrades-shaped fragment (`/fapi/v1/aggTrades`, `@aggTrade`, or `aggtrade_ws`).
- `config.py` — `DEFAULT_SYMBOL_ALLOWLIST` is reused as the default symbol set for `build_aggtrades_plan`. Alt symbols still require explicit caller admission.
- `invalid_window.py` — referenced as the design taxonomy for any future failure that the collector encounters; not exercised in Phase 4ax (no live capture exists yet).
- `manifest.py` — `MicrostructureManifest` is **not** mutated by Phase 4ax. The `research_eligible=False` default and the always-raises `flip_research_eligible` are preserved verbatim.
- `raw_writer.py` — `RawWriter` is composed by `write_validated_aggtrades_to_path(...)`. Path refusals (project `data/microstructure/`, no overwrite, stale `.tmp` companion, directory, non-`Path`) are inherited unchanged.
- `.gitignore` line `data/microstructure/` is preserved.

---

## 6. Files added / modified

### Added (new)

```
src/prometheus/research/microstructure/aggtrades.py
tests/research/microstructure/test_aggtrades.py

docs/00-meta/implementation-reports/2026-05-07_phase-4ax_aggtrades-only-public-microstructure-collector-skeleton.md
docs/00-meta/implementation-reports/2026-05-07_phase-4ax_closeout.md
```

### Modified

```
src/prometheus/research/microstructure/__init__.py     (re-export aggTrades scaffold symbols; docstring updated)
tests/research/microstructure/test_import_boundaries.py (Phase 4ax docstring note; +urllib.request and +socket forbidden-import patterns)
docs/00-meta/current-project-state.md                  (Phase 4ax narrative paragraph + "Current phase:" block update)
```

`.gitignore` is unchanged (the `data/microstructure/` line was already added by Phase 4aw).

### Not modified

- No file under `src/prometheus/` outside the microstructure package (`aggtrades.py` is new; `__init__.py` is the only modified existing file).
- No Phase 4aw scaffold module other than `__init__.py` (re-exports only).
- No existing test outside `tests/research/microstructure/` (only the existing `test_import_boundaries.py` was narrowly updated).
- No existing script under `scripts/`.
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, or governance memo.
- No `pyproject.toml`, `README.md`, or top-level config.
- The `data/microstructure/` directory does not exist after Phase 4ax.

---

## 7. AggTrades skeleton description

### Payload validation

`validate_aggtrade_payload(payload: Mapping[str, object]) -> AggTradePayload` accepts both REST-shaped payloads (no `E` event-time field) and stream-shaped payloads (with `E`). It enforces:

- required fields `a`, `p`, `q`, `f`, `l`, `T`, `m` present;
- `a` integer-like and ≥ 0;
- `p` decimal-compatible and > 0 (Decimal-based, no float surprises);
- `q` decimal-compatible and > 0;
- `f` integer-like and ≥ 0;
- `l` integer-like and ≥ `f`;
- `T` integer-like and > 0;
- `m` strictly `bool` (rejects `1`, `"true"`, etc.);
- optional `E` integer-like and > 0 if present;
- unknown extra fields preserved verbatim in `extra_fields` and do not affect validation.

Returns a frozen `AggTradePayload` dataclass with `Decimal` price and quantity.

### Taker-side derivation

`TakerSide` is a `StrEnum` (`BUY` / `SELL`). The convention is: `m` is the buyer-is-maker flag in Binance aggTrade payloads. If `m` is true, the buyer was the maker, so the taker side is `SELL`; if `m` is false, the seller was the maker, so the taker side is `BUY`. Both branches are tested.

### Endpoint allowlist enforcement

`assert_aggtrades_endpoint_allowed(endpoint)` first defers to the Phase 4aw `assert_endpoint_allowed`, which enforces public-only allowlist + denylist dominance (so private / authenticated / user stream / listenKey / order / account / position / leverage / margin / forceOrders REST / credential-shaped / `MCP` / `Graphify` / `.mcp.json` references are denied). It then requires the endpoint to contain at least one aggTrades-shaped fragment (`/fapi/v1/aggTrades`, `@aggTrade`, or `aggtrade_ws`) so that public-only-but-non-aggTrades endpoints (e.g. `@bookTicker`) are also rejected at this layer.

### Dry-run plan

`build_aggtrades_plan(*, symbol, mode, start_time_ms=None, end_time_ms=None, output_root=None, dataset_family="microstructure_raw_aggtrades_v001", explicit_extra_symbols=None) -> AggTradePlan`:

- accepts `symbol` (must be uppercase alphanumeric, must be in the default `("BTCUSDT", "ETHUSDT")` allowlist or admitted via `explicit_extra_symbols`);
- accepts `mode` as `AggTradeMode.ARCHIVE`, `AggTradeMode.REST`, `AggTradeMode.WS`, or the equivalent string;
- enforces `start_time_ms <= end_time_ms` if both provided, both ≥ 0;
- accepts `dataset_family` only if it begins with `microstructure_raw_aggtrades`;
- runs `assert_aggtrades_endpoint_allowed` on the live REST / WS endpoint references (the archive label is a separate bulk-archive descriptor reserved for a future archive-acquisition phase and is not allowlist-checked at this layer);
- creates **no directories**, contacts **no endpoints**, opens **no streams**;
- returns a frozen `AggTradePlan` containing `symbol`, `mode`, `dataset_family`, `endpoint_reference`, `capture_mode_label`, `planned_output_root`, `planned_path_label`, `start_time_ms`, `end_time_ms`.

### Temp-path writer composition

`write_validated_aggtrades_to_path(payloads, target_path) -> AggTradeWriteResult`:

- validates each payload via `validate_aggtrade_payload`;
- uses the Phase 4aw `RawWriter` (which refuses paths under `data/microstructure/`, refuses to overwrite existing finals, refuses stale `.tmp` companions);
- writes one JSONL record per validated payload, including the derived `taker_side`, the original `trade_time_ms`, and an `event_time_ms` field (sourced from `E` for stream-shaped payloads or from `T` otherwise);
- finalises atomically with paired SHA256;
- returns an `AggTradeWriteResult` summary including buy / sell taker-side counts;
- on validation failure mid-stream, raises an `AggTradeValidationError` with the offending index and lets the `RawWriter.__exit__` cleanup release the file handle without finalising; the final file is not produced.

The summary is the explicit handoff contract for a future caller that may translate it into a manifest entry. Manifest translation is **not** implemented in Phase 4ax.

### No capture capability

`aggtrades.py` does not import `httpx`, `requests`, `aiohttp`, `websockets`, `binance`, `urllib.request`, `socket`, `dotenv`, `python_dotenv`, or any `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` module. The new import-boundary scan extensions (`urllib.request`, `socket`) enforce this.

---

## 8. Tests implemented

46 new tests in `test_aggtrades.py`; targeted-package total now 161 (Phase 4aw 114 + Phase 4ax 47 effective tests including the +1 parametrised import-boundary scan slot for `aggtrades.py`).

### Payload validation tests

- valid REST-shaped payload validates;
- valid stream-shaped payload validates with optional `E`;
- missing required field rejected;
- invalid price rejected (negative, zero, non-numeric, empty);
- invalid quantity rejected (zero, negative, non-numeric);
- invalid trade-id ordering rejected (`l < f`);
- invalid trade time rejected (zero, negative);
- invalid `m` type rejected (string, int);
- invalid `E` rejected when present (zero, negative);
- extra fields preserved;
- payload must be a Mapping;
- int-shaped strings accepted for `a`, `f`, `l`, `T`.

### Taker-side derivation tests

- `m=False` → `taker_side=BUY`;
- `m=True` → `taker_side=SELL`.

### Allowlist tests

- `/fapi/v1/aggTrades` accepted;
- `@aggTrade` WS accepted;
- `aggtrade_ws` logical label accepted;
- 12 parametrised denylist references rejected (private REST, authenticated REST, user stream, listenKey, credential-shaped, `.mcp.json`);
- public-only-but-non-aggTrades endpoint (`@bookTicker`) rejected by the aggTrades-shape guard.

### Dry-run plan tests

- archive plan does not create directories;
- REST plan does not call endpoints;
- WS plan does not open WebSockets;
- invalid mode rejected;
- invalid time range rejected (start > end, negative start, negative end);
- unknown symbol rejected without explicit extras;
- unknown symbol admitted via explicit extras;
- lowercase symbol rejected;
- non-aggTrades dataset family rejected.

### Temp-path writer tests

- writes JSONL to pytest `tmp_path`, finalises SHA256, returns summary with correct buy / sell counts;
- preserves stream `E` event-time and labels source `stream` vs `trade_time`;
- rejects project `data/microstructure/...` path;
- rejects invalid payload before final-file creation (no final file or SHA file written);
- rejects non-Sequence `payloads`;
- does not create any manifest;
- regression check: project `data/microstructure/` directory still does not exist.

### Import-boundary tests

The existing parametrised `test_no_forbidden_imports` automatically scans the new `aggtrades.py` (the `_scaffold_files()` helper globs every `*.py` in the package). The scan list now includes `urllib.request` and `socket` in addition to the Phase 4aw set. The strict-deny and allowlist-deny content scans likewise auto-cover the new module.

---

## 9. Validation results

| Command | Result |
| ------- | ------ |
| `python -m compileall src/prometheus/research/microstructure` | pass (7 modules) |
| `python -m compileall tests/research/microstructure` | pass |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | `All checks passed!` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest tests/research/microstructure` | **161 passed** (114 Phase 4aw + 47 Phase 4ax effective) |
| `pytest tests/research/microstructure/test_aggtrades.py` | **46 passed** |
| `pytest` (whole repo) | **944 passed, 2 failed**; both 2 failures are the same pre-existing simulation failures verified on `main` before Phase 4ax: `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in the unrelated `src/prometheus/research/data/storage.py:232`; **Phase 4ax introduced zero new test regressions** |
| `mypy src/prometheus/research/microstructure` | `Success: no issues found in 7 source files` |
| `mypy` (whole repo) | `Success: no issues found in 89 source files` (was 88 on main; +1 for `aggtrades.py`) |
| `git diff --check` | clean |
| `data/microstructure/` directory check | **DOES NOT EXIST** |

---

## 10. Security / credential boundary

`aggtrades.py` does not:

- read `.env` files;
- accept API keys;
- handle signed requests;
- reference private endpoints;
- reference user stream or listenKey lifecycle;
- reference order / account / position / leverage / margin endpoints;
- reference MCP, Graphify, or `.mcp.json`;
- use `os.environ` or `getenv()`.

These constraints are enforced by `tests/research/microstructure/test_import_boundaries.py`, which scans every microstructure source file (excluding docstrings and comments) for forbidden import patterns and forbidden token strings.

---

## 11. Runtime separation

`aggtrades.py` does not import from `prometheus.runtime`, `prometheus.execution`, or `prometheus.persistence`. None of the scaffold code:

- mutates runtime state;
- writes to a runtime database;
- contacts an order router;
- touches the safety-state machine;
- reads or writes `state.db`;
- emits runtime events.

The collector skeleton is research infrastructure. It does not couple to live operation in any direction.

---

## 12. Data boundary

- `.gitignore` already contains `data/microstructure/` (added by Phase 4aw); Phase 4ax did not modify `.gitignore`.
- The directory `data/microstructure/` was not created by Phase 4ax.
- No raw file is written under any project path.
- Tests use pytest `tmp_path` exclusively for file I/O.
- The Phase 4aw `RawWriter` primitive composed by `write_validated_aggtrades_to_path` rejects any caller-provided path that resolves under `data/microstructure/`.
- No existing dataset manifest under `data/manifests/` is modified.
- No `__v002`, `__v003`, or other dataset version is created.
- Phase 4i, Phase 4ac, Phase 3q, Phase 2 manifests are unchanged.

---

## 13. What Phase 4ax enables

A future, separately authorized phase can build:

- archive acquisition (downloading public Binance bulk aggTrades archives) by composing `assert_aggtrades_endpoint_allowed` and `validate_aggtrade_payload` with an HTTP fetch layer not yet implemented;
- REST polling (calling `/fapi/v1/aggTrades`) by composing the same validation logic with a future REST client;
- live WebSocket capture (subscribing to `<symbol>@aggTrade`) by composing the same validation logic with a future WS client;
- manifest construction by translating `AggTradeWriteResult` summaries into `MicrostructureManifest.append_file(...)` entries.

None of these is authorized by Phase 4ax.

---

## 14. What Phase 4ax does not enable

- No real capture.
- No endpoints.
- No WebSockets.
- No archive downloads.
- No data acquisition.
- No feature computation.
- No ML model.
- No strategy.
- No paper / shadow.
- No live readiness.
- No deployment.
- No exchange-write.
- No production keys.
- No authenticated APIs.
- No private endpoints.
- No user stream.
- No live WebSocket implementation.
- No MCP, Graphify, or `.mcp.json`.
- No 5m, 1m, real aggTrades data, tick, mark-price 30m / 4h, or order-book data acquisition.

---

## 15. Implementation / governance review

### What changed?

- One new source module (`aggtrades.py`, 7 source files in package, mypy-strict-clean).
- One new test file (`test_aggtrades.py`, 46 tests).
- Two narrow updates: `__init__.py` re-exports + docstring; `test_import_boundaries.py` docstring + 2 additional forbidden-import patterns (`urllib.request`, `socket`).
- Two new docs files (memo + closeout).
- One narrow `current-project-state.md` update.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text.
- No Phase 4ak / 4al / 4j / 3r / 3v / 3w governance.
- No Phase 4aw scaffold module beyond `__init__.py` re-exports.
- No data manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/`.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing test or script outside the narrowly-updated `test_import_boundaries.py`.

### Were any locks, verdicts, or safety boundaries affected?

No. The collector skeleton is inert. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4ax paragraph addition.

### Is the phase mergeable as collector-skeleton code-and-docs?

Yes, subject to operator review. The phase introduces only code that is verifiably inert (no network, no project data writes, no live endpoint calls, no successor authorisation), is fully covered by 46 new tests (161 total in the package), passes whole-repo ruff and mypy strict, and introduces zero new test regressions.

---

## 16. Research interpretation review

### 1. What did this phase prove?

That an aggTrades-only collector skeleton can be added on top of the Phase 4aw scaffold while preserving every safety boundary. Mocked / offline payload validation works, taker-side derivation matches the Binance convention in both directions, the Phase 4aw allowlist + denylist + an additional aggTrades-shape guard reject every non-aggTrades public endpoint and every private / authenticated / user-stream / listenKey / order / account / leverage / margin / `forceOrders` / credential-shaped reference, the dry-run plan returns a descriptive `AggTradePlan` without creating directories or touching the network, and the temp-path writer atomically produces a JSONL file with paired SHA256 in pytest temporary directories while refusing project `data/microstructure/` paths and refusing to leave a finalised file behind on validation failure.

### 2. What did this phase not prove?

Anything about Binance microstructure data quality, edge, opportunity rate, or strategy viability. No specific endpoint behaviour was verified against the live exchange. Local order-book reconstruction was not implemented. The eligibility gate was not implemented. No historical strategy verdict was changed. No project lock was changed. Nothing about live readiness was demonstrated. The skeleton does not prove that real aggTrades acquisition will satisfy `Phase 3p §4.7` strict integrity gating (no acquisition was performed).

### 3. Which original questions did it answer?

- "Can the project safely add an aggTrades-only collector skeleton on top of the Phase 4aw scaffold, with schema validation, dry-run behavior, allowlist enforcement, raw-writer composition in temp paths, and tests, while still preventing real data acquisition and endpoint contact?" → **Yes** (verified by 46 new tests, whole-repo ruff and mypy strict pass, zero new regressions, and confirmed-empty `data/microstructure/`).
- "Does Phase 4aw scaffold composition work in practice when reused by a downstream module?" → **Yes** (`allowlist`, `config`, `raw_writer` all compose cleanly).
- "Does the aggTrades payload validator reject malformed REST and stream payloads while preserving extra fields?" → **Yes**.
- "Does the temp-path writer fail closed under validation errors without leaving a finalised file behind?" → **Yes**.

### 4. Which original questions remain open?

- Does Binance actually return aggTrades payloads matching this validator's strict-shape assumptions in practice? (Phase 4ax does not contact the exchange.)
- What rate limits, retention windows, and per-symbol availability constraints apply to the public aggTrades archive? (Documented in Phase 4at; not exercised here.)
- Does any future microstructure feature derived from aggTrades carry edge under §11.6 cost realism? (No analysis performed.)
- Should the JSONL raw format be replaced by `.jsonl.zst`? (Documented as future additive work in Phase 4aw.)

### 5. What does it mean for strategy research?

It means the project now has tested aggTrades-shaped payload validation and a tested dry-run / temp-path writer composition. It does **not** create a strategy candidate, does **not** open any rescue path for cooled-down candidates (R2 / F1 / D1-A / V2 / G1 / C1), and does **not** authorize any feature derivation from aggTrades data. Phase 4ax remains plumbing; strategy research stays under the binding M0 admissibility gate and the post-null cooldown rule.

### 6. What does it mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, Phase 4j §11 OI subset governance, Phase 3r §8 mark-price gap governance, and Phase 3v §8 stop-trigger-domain governance all remain verbatim.

### 7. What is the clean next step?

After operator review and merge of Phase 4ax, **remain paused**. The aggTrades-only collector skeleton is now in place; no successor phase is authorized.

If the operator separately wishes to advance, the most natural separately-authorized next step would be either (a) a docs-only data-acquisition authorization memo establishing the explicit operator decision and §4.7 / §11.6 boundary for aggTrades archive acquisition, or (b) a docs-and-code Phase 4ay implementing the public aggTrades archive download path under the strict integrity gate. Phase 4ax does **not** authorize either.

### 8. What should we not do yet?

- Do not implement REST or WebSocket clients.
- Do not contact any Binance endpoint.
- Do not download any public archive.
- Do not create the `data/microstructure/` directory tree.
- Do not implement order-book reconstruction, deterministic replay, normalizers beyond schema validation, eligibility-gate execution, healthcheck, dashboard hooks, or features.
- Do not start ML, strategies, paper / shadow, live-readiness, deployment, exchange-write, or production keys.
- Do not authorize a successor phase.

---

## 17. Recommendation

- **Primary:** remain paused. After operator review, merge Phase 4ax into `main`, then stop.
- **Conditional secondary (NOT authorized by Phase 4ax):** future docs-only Phase 4ay data-acquisition authorization memo, *or* future docs-and-code Phase 4ay public aggTrades archive acquisition under the strict integrity gate, separately authorized.
- **Not recommended:** implementing live REST / WebSocket clients, capture, archive downloads, eligibility-gate execution, features, ML, or any cooled-down-family rescue.
- **Forbidden:** verdict revision, lock revision, parameter optimization, strategy resurrection, M0 amendment derived from Phase 4ax reasoning, reopening the 5m research thread, real data acquisition, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials.

---

## 18. Explicit preservation of verdicts, locks, and no-rescue constraints

Phase 4ax preserves verbatim:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

Project locks preserved verbatim:

- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w.
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw results.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane.

**Recommended state remains paused. No successor phase is authorized.**
