# Phase 4aw — Public-Only Microstructure Capture Scaffold Implementation

**Type:** code-and-docs scaffold-only implementation phase.
**Status:** drafted; pending operator review and merge approval.
**Date:** 2026-05-07.

---

## 1. Executive summary

Phase 4aw adds the first inert public-only microstructure research scaffold to the Prometheus repository. It introduces a new package `src/prometheus/research/microstructure/` containing five small, narrowly-scoped modules — `config`, `allowlist`, `invalid_window`, `manifest`, `raw_writer` — plus a paired test tree under `tests/research/microstructure/`. It adds a single `.gitignore` line for `data/microstructure/`. It does **not** create the `data/microstructure/` directory, write any project data, call any endpoint, open any WebSocket, download any archive, run any collector, normalizer, replay, or eligibility gate, or authorize any successor phase.

The scaffold answers a narrow question: *Can the project safely add the foundational microstructure research scaffold — config model, endpoint allowlist / denylist, invalid-window taxonomy, manifest data model, raw-writer primitive, `.gitignore` protection, and tests — without creating any data-capture capability or trading capability?* The answer demonstrated by Phase 4aw is **yes**.

Phase 4aw was derived from Phase 4av (implementation plan), Phase 4au (capture design specification), Phase 4at (data availability / capture feasibility memo), Phase 4as (mechanism reset), Phase 4ar (V1-arc forensic interpretation), Phase 4ak (M0 governance), Phase 4al (refined no-rescue rule and data-resolution hierarchy), Phase 4j §11 (OI subset governance), Phase 3r §8 (mark-price gap governance), Phase 3v §8 (stop-trigger-domain governance), and Phase 3t (5m thread closure).

Phase 4aw preserves every retained verdict and every project lock. It does not authorize Phase 4ax, Phase 5, Phase 4 canonical, paper/shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, or any data acquisition (5m, 1m, aggTrades, tick, mark-price 30m / 4h, order-book).

---

## 2. Scope and explicit non-scope

### Allowed (and performed) in Phase 4aw

- Add inert scaffold modules under `src/prometheus/research/microstructure/`:
  - `__init__.py`
  - `config.py`
  - `allowlist.py`
  - `invalid_window.py`
  - `manifest.py`
  - `raw_writer.py`
- Add tests under `tests/research/microstructure/`:
  - `__init__.py`
  - `test_config.py`
  - `test_allowlist.py`
  - `test_invalid_window.py`
  - `test_manifest.py`
  - `test_raw_writer.py`
  - `test_import_boundaries.py`
- Add `data/microstructure/` to `.gitignore` (one line).
- Add Phase 4aw memo and closeout under `docs/00-meta/implementation-reports/`.
- Update `docs/00-meta/current-project-state.md` narrowly.

### Forbidden (and not performed) in Phase 4aw

- Acquire data of any kind.
- Call Binance endpoints.
- Open WebSockets.
- Download public archive files.
- Implement collectors.
- Implement public REST client logic.
- Implement public WebSocket client logic.
- Implement order-book reconstruction.
- Implement deterministic replay.
- Implement normalizers.
- Implement eligibility-gate execution.
- Implement feature computation.
- Create real dataset manifests under project paths.
- Create the `data/microstructure/` directory.
- Write raw files under project data paths.
- Run backtests.
- Run historical strategy scripts.
- Run Phase 4aq or any prior research script.
- Run simulations.
- Compute predictive statistics.
- Modify existing data, manifests, trade logs, strategy specs, thresholds, governance docs, retained verdicts, project locks, or prior research reports — except for the new Phase 4aw docs and the narrow `current-project-state.md` update.
- Create a strategy candidate.
- Design entries or exits.
- Create an ML model.
- Authorize any successor phase.

---

## 3. Repository verification summary

Before branching:

- Branch: `main`.
- Working tree: clean (only gitignored `.claude/scheduled_tasks.lock` and `data/research/` untracked).
- `git rev-parse main` and `git rev-parse origin/main` both `46314be989990f33821a67199921ebec2a3aef55`.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_public-only-microstructure-capture-implementation-plan.md` present on main.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_closeout.md` present on main.
- `docs/00-meta/implementation-reports/2026-05-07_phase-4av_merge-closeout.md` present on main.
- `data/microstructure/` did not exist (and still does not).

Phase 4aw branch `phase-4aw/public-only-microstructure-capture-scaffold-implementation` was created from this clean base.

---

## 4. Methodology

Phase 4aw is a scaffold-only implementation. It was constructed under the following methodology:

- **No endpoint calls.** No module imports `httpx`, `requests`, `aiohttp`, `websockets`, or any Binance SDK.
- **No WebSockets.** No WebSocket client is implemented.
- **No archive downloads.** No code path retrieves public bulk archives.
- **No data acquisition.** No code path writes raw event data.
- **No collectors.** No `aggtrade.py`, `bookticker.py`, `depthdiff.py`, `forceorder_proxy.py`, `oi_funding.py` is created.
- **No REST / WS client modules.** No `public_rest.py` or `public_ws.py` is created.
- **No real manifests.** No manifest is written under project data paths.
- **No project data writes.** Tests use `pytest` `tmp_path` only. The raw-writer primitive explicitly rejects any path resolving under `data/microstructure/` (regardless of separator).
- **No strategies.** No strategy logic exists in the scaffold.
- **No ML.** No machine-learning code exists in the scaffold.
- **No successor authorization.** Phase 4aw does not authorize Phase 4ax or any other successor phase.

The scaffold is intentionally narrow. Its purpose is to lock the public-only boundary and the inert manifest / raw-writer / invalid-window data shapes. Any future phase that adds collectors, clients, or capture must be separately authorized.

---

## 5. Phase 4av baseline

Phase 4av was the implementation-plan memo that defined the file-by-file design Phase 4aw partially realises. Phase 4aw's scaffold-only realisation honours the Phase 4av-recommended Phase 4aw scope:

- scaffold (`__init__.py`, `config.py`, `allowlist.py`, `invalid_window.py`, `manifest.py` with no live writes, `raw_writer.py` with no live writes);
- test scaffolding;
- import-boundary tests;
- `.gitignore` line for `data/microstructure/`;
- no live endpoint calls;
- no archive downloads;
- no WebSockets;
- no data acquisition;
- no actual manifest creation under project paths;
- no actual raw file writes under project paths.

---

## 6. Files added / modified

### Added (new)

```
src/prometheus/research/microstructure/__init__.py
src/prometheus/research/microstructure/config.py
src/prometheus/research/microstructure/allowlist.py
src/prometheus/research/microstructure/invalid_window.py
src/prometheus/research/microstructure/manifest.py
src/prometheus/research/microstructure/raw_writer.py

tests/research/__init__.py
tests/research/microstructure/__init__.py
tests/research/microstructure/test_config.py
tests/research/microstructure/test_allowlist.py
tests/research/microstructure/test_invalid_window.py
tests/research/microstructure/test_manifest.py
tests/research/microstructure/test_raw_writer.py
tests/research/microstructure/test_import_boundaries.py

docs/00-meta/implementation-reports/2026-05-07_phase-4aw_public-only-microstructure-capture-scaffold-implementation.md
docs/00-meta/implementation-reports/2026-05-07_phase-4aw_closeout.md
```

### Modified

```
.gitignore                          (one new line: data/microstructure/)
docs/00-meta/current-project-state.md   (Phase 4aw narrative paragraph + "Current phase:" block; preserves prior content)
```

### Not modified

- No file under `src/prometheus/` other than the new package.
- No existing test file.
- No existing script under `scripts/`.
- No existing dataset manifest under `data/manifests/`.
- No existing trade log, backtest report, validation checklist, governance memo, or strategy spec.
- No `pyproject.toml` change.
- No `README.md` change.
- The `data/microstructure/` directory does not exist after Phase 4aw.

---

## 7. Scaffold module descriptions

### `__init__.py`

Package marker that re-exports the public scaffold surface as `__all__`. No side effects, no I/O, no network imports, no runtime / execution / persistence imports. Module docstring describes the package boundary in abstract terms (no literal denylist tokens in code; the test scanner verifies this).

### `config.py`

Pure data model for the future capture configuration:

- `MicrostructureConfig` (frozen dataclass) — `endpoint_allowlist`, `endpoint_denylist`, `symbol_allowlist`, `storage_root`, `dataset_family_config`, `invalid_window_thresholds`, `eligibility_gate_thresholds`.
- `DatasetFamilyConfig` (frozen dataclass) — per-family scaffold config entry; layer is one of `raw|normalized|derived`; capture-mode is one of `rest_polling|ws_live_capture_required|historical_archive`.
- `InvalidWindowThresholds` and `EligibilityGateThresholds` (frozen dataclasses) — bounds for future detection / gating.
- `validate_config(config, *, explicit_extra_symbols=None)` — pure function. Verifies that every allowlist endpoint is on the public-only allowlist and not denied. Refuses any unknown endpoint, denylisted endpoint, unknown symbol (unless explicitly admitted via `explicit_extra_symbols`), credential-shaped fields, `.env` references, private endpoint references, user-stream / listenKey references, order / account / position / leverage / margin endpoint references, and `.mcp.json` / `Graphify` / `MCP` references.
- `ConfigValidationError` — raised on rejection.

The default symbol allowlist is `("BTCUSDT", "ETHUSDT")` only. Phase 4ac core symbol set extension is allowed only via the explicit caller-passed `explicit_extra_symbols` mapping.

### `allowlist.py`

Immutable public endpoint allowlist + explicit denylist + lookups:

- `ALLOWLIST_PATTERNS` — tuple of public-only patterns: `@aggTrade`, `@bookTicker`, `@depth`, `@depth5/10/20`, `@forceOrder`, `@markPrice`, `@indexPrice` WS subscription substrings; `/fapi/v1/aggTrades`, `/fapi/v1/depth`, `/fapi/v1/klines`, `/fapi/v1/markPriceKlines`, `/fapi/v1/indexPriceKlines`, `/fapi/v1/premiumIndexKlines`, `/fapi/v1/fundingRate`, `/fapi/v1/fundingInfo`, `/fapi/v1/openInterest`, `/futures/data/openInterestHist`, `/futures/data/topLongShortAccountRatio`, `/futures/data/topLongShortPositionRatio`, `/futures/data/globalLongShortAccountRatio`, `/futures/data/takerlongshortRatio` REST paths; plus logical labels for the future capture stack.
- `DENYLIST_TOKENS` — tuple of forbidden patterns: private / authenticated REST paths, user-stream / listenKey, credential-shaped strings, `.mcp.json`, `MCP`, `Graphify`, `.env`.
- `is_endpoint_allowed(value)`, `is_endpoint_denied(value)`, `assert_endpoint_allowed(value)` — pure functions.
- `EndpointNotAllowedError` — raised on assertion failure.

Denylist dominates allowlist: any value matching a denylist token is denied even if it also matches an allowlist pattern. This protects the legitimate `@forceOrder` WebSocket pattern from accidentally promoting the `/fapi/v1/forceOrders` user-scope authenticated REST endpoint.

No HTTP / WebSocket / URL opening. No `.env` reads. No credential lookup. Pure data + pure functions only.

### `invalid_window.py`

Microstructure-specific invalid-window taxonomy. Coexists with the historical-kline `InvalidWindow` in `prometheus.research.data.manifests` — they are different concepts in different packages.

- `InvalidWindowReason` (`StrEnum`, exactly 17 values): `MISSING_SEQUENCE`, `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `GAP_AFTER_RECONNECT`, `SNAPSHOT_MISMATCH`, `CLOCK_SKEW`, `SYMBOL_MISMATCH`, `STALE_STREAM`, `STALE_BOOK`, `IMPOSSIBLE_SPREAD`, `NEGATIVE_SIZE`, `ZERO_OR_INVALID_PRICE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP`, `FORCE_ORDER_PROXY_INCOMPLETENESS`, `FAILED_ATOMIC_WRITE`, `PARTIAL_FILE_RECOVERY_EVENT`.
- `InvalidWindowSeverity` (`StrEnum`): `INFO`, `WARN`, `ERROR`.
- `DownstreamEligibilityAction` (`StrEnum`): `FLAG`, `EXCLUDE`, `PROXY_ONLY`.
- `InvalidWindow` (frozen dataclass): `start_time_ms`, `end_time_ms`, `family`, `symbol`, `reason`, `severity`, `downstream_eligibility_action`, `evidence` (non-empty mapping); `to_dict` / `from_dict` for round-trip.

### `manifest.py`

Microstructure manifest data model. Designed to be populated by a future capture phase; not populated by Phase 4aw.

- `MicrostructureManifest` (mutable dataclass) — required fields include `dataset_family`, `version`, `symbol`, `source`, `endpoint`, `capture_mode`, `schema_version`, `endpoint_docs_reference`, `capture_config_hash`, `code_commit_sha`, plus `governance_labels`, `start_time_ms`, `end_time_ms`, `event_count`, `file_count`, `files` (list of `FileEntry`), `invalid_windows` (list of `InvalidWindow`), `retention_warning`, `proxy_warning`, `research_eligible` (default `False`), `eligibility_gate_status` (default `pending`).
- `FileEntry` (frozen dataclass) — `path`, `sha256` (64-char hex), `event_count`, `start_time_ms`, `end_time_ms`.
- `EligibilityGateStatus` (`StrEnum`): `PENDING`, `PASS`, `FAIL`.
- Mutation methods are intentionally narrow: `append_file`, `append_invalid_window`, `to_dict`, `from_dict`, `save(path)`, `load(path)`.
- **`flip_research_eligible(...)` always raises `ManifestImmutableError`.** The Phase 4aw scaffold provides no way to flip `research_eligible` to `True`. Only the future eligibility gate (separately authorized) may do so.
- `save(path)` refuses to overwrite an existing file. `path` is caller-controlled — tests use pytest `tmp_path`. No write under project `data/microstructure/`.

### `raw_writer.py`

Atomic JSONL raw event writer primitive. JSONL was selected over `.jsonl.zst` for the scaffold because zstandard is not in the project's current dependency set; adding zstd later is an additive change and does not affect the scaffold's logical contracts.

- `RawWriter(target_path)` — constructs an open writer. Refuses if `target_path` already exists, if a stale `.tmp` companion exists, if the path is a directory, or if the path resolves under the project `data/microstructure/` tree.
- `append(record)` — appends one JSON-serializable dict; requires integer `event_time_ms`.
- `close()` — finalizes by flushing, optional fsync (suppressed where not supported), computing SHA256 over `.tmp` bytes, atomically renaming `.tmp` → final, and writing `<final>.sha256`. Returns a `RawWriterFileSummary`.
- Exceptions: `RawWriterError` (base), `RawWriterPathError`, `RawWriterAlreadyExistsError`.
- `RawWriterFileSummary` (frozen dataclass) — `path`, `sha256`, `event_count`, `start_time_ms`, `end_time_ms`. Designed to be translated explicitly by callers into a `FileEntry` for the manifest. Phase 4aw deliberately does not couple the writer to manifest mutation.

The forbidden-path check inspects both the literal path string and the resolved absolute form, normalising backslashes to forward slashes and lowercasing before comparison. This catches both `data/microstructure` and `data\microstructure` regardless of OS.

---

## 8. Tests implemented

114 tests, all passing.

- `test_config.py` (15 tests) — valid config passes; default thresholds; empty / duplicate / unknown / denylisted allowlist rejections; denylist block accepts denylist tokens; credential-shaped storage_root rejected; unknown symbol rejected without explicit extras; unknown symbol admitted via explicit extras; lowercase symbol rejected; invalid layer / capture_mode rejected; threshold negative rejected; out-of-range fraction rejected; credential-shaped family rejected.
- `test_allowlist.py` (8 tests + 21 + 23 parametrised cases = 52 effective cases) — non-empty allowlist / denylist; every public endpoint admitted; every denied reference blocked; denylist dominates `@forceOrder` vs `/fapi/v1/forceOrders`; empty / non-string values fail closed; case-insensitive matching.
- `test_invalid_window.py` (12 tests) — exactly 17 reasons; minimum severity / action sets; valid window constructs; end < start rejected; empty family / symbol / evidence rejected; round-trip; string enum values emitted; invalid reason rejected on round trip; frozen-dataclass immutability.
- `test_manifest.py` (11 tests) — `research_eligible` default `False`; `eligibility_gate_status` default `pending`; `flip_research_eligible` always raises; `append_file` updates counters; `append_invalid_window` appends; invalid SHA256 rejected; round-trip; save / load via pytest `tmp_path`; refuses to overwrite; serialised payload defaults; empty required field rejected.
- `test_raw_writer.py` (12 tests + 3 parametrised path cases = 14 effective cases) — append / close atomic; tmp file removed after close; no overwrite; stale tmp blocks construction; record must have `event_time_ms`; `event_time_ms` must be int; record must be dict; double close rejected; append after close rejected; directory path rejected; non-`Path` rejected; project data path rejected (with parametrised forbidden fragments); SHA256 matches finalized bytes.
- `test_import_boundaries.py` (forbidden-import scan parametrised by 6 source files = 6 cases + 2 content-scan tests) — scans every scaffold module for forbidden imports (`prometheus.runtime`, `prometheus.execution`, `prometheus.persistence`, `requests`, `httpx`, `aiohttp`, `websockets`, `binance`, `dotenv`, `python_dotenv`, `os.environ`, `getenv`); strict-deny content scan; allowlist-only-allowed deny content scan. Imports inside docstrings/comments are stripped before scanning so docstrings can describe the boundary.

The scanners use file-level regex / substring tests against repository sources only. They do not import the modules under test and never perform network or filesystem mutation.

---

## 9. Validation results

Run on the Phase 4aw branch with `data/microstructure/` confirmed not present:

- `python -m compileall src/prometheus/research/microstructure` — pass.
- `python -m compileall tests/research/microstructure` — pass.
- `.venv/Scripts/ruff check src/prometheus/research/microstructure tests/research/microstructure` — `All checks passed!`.
- `.venv/Scripts/ruff check .` (whole repo) — `All checks passed!`.
- `.venv/Scripts/pytest tests/research/microstructure` — 114 passed.
- `.venv/Scripts/pytest` (whole repo) — 897 passed, 2 failed. **Both failures are pre-existing on `main`** (verified by `git checkout main && pytest tests/simulation/test_backtest_real_2026_03.py` returning the same 2 failures with identical `KeyError: 'trade_count'` in the unrelated `src/prometheus/research/data/storage.py:232`). Phase 4aw introduces zero new test regressions.
- `.venv/Scripts/mypy src/prometheus/research/microstructure` — `Success: no issues found in 6 source files`.
- `.venv/Scripts/mypy` (whole repo) — `Success: no issues found in 88 source files` (was 82 on main; 6 new microstructure modules now also pass mypy strict).
- `git diff --check` — clean (no whitespace errors).
- `git status` — only the expected scaffold files, the new `.gitignore` change, and the gitignored `.claude/scheduled_tasks.lock` / `data/research/` are present. `data/microstructure/` does not exist.

mypy was run because the project already runs mypy strict on `src/prometheus`, and the new package adds 6 source files to that scope.

---

## 10. Security / credential boundary

No code in the scaffold:

- reads `.env` files,
- accepts API keys,
- handles signed requests,
- references private endpoints,
- references user stream or listenKey lifecycle,
- references order / account / position / leverage / margin endpoints,
- references MCP, Graphify, or `.mcp.json`,
- uses `os.environ` or `getenv()` for credentials.

These constraints are enforced by `tests/research/microstructure/test_import_boundaries.py`, which scans the package source files (excluding docstrings and comments) for forbidden import patterns and forbidden token strings. Any future change to the scaffold that introduces such a reference will fail the test.

---

## 11. Runtime separation

No scaffold module imports from `prometheus.runtime`, `prometheus.execution`, or `prometheus.persistence`. None of the scaffold code:

- mutates runtime state,
- writes to a runtime database,
- contacts an order router,
- touches the safety-state machine,
- reads or writes `state.db`,
- emits runtime events.

The scaffold is research infrastructure. It does not couple to live operation in any direction.

---

## 12. Data boundary

- `.gitignore` now contains a single new line: `data/microstructure/`.
- The directory `data/microstructure/` was not created by Phase 4aw.
- No raw file is written under any project path.
- Tests use pytest `tmp_path` exclusively for file I/O.
- The raw-writer primitive explicitly rejects any caller-provided path that resolves under `data/microstructure/`.
- No existing dataset manifest under `data/manifests/` is modified.
- No `__v002`, `__v003`, or other dataset version is created.
- Phase 4i, Phase 4ac, Phase 3q, Phase 2 manifests are unchanged.

---

## 13. What Phase 4aw enables

A future, separately authorized phase (call it Phase 4ax or any successor) may build collectors, REST clients, WebSocket clients, an LOB replay implementation, normalizers, an eligibility gate, a healthcheck reporter, and a dashboard hook on top of this scaffold without redesigning the scaffold's boundary. The scaffold provides:

- a typed config model that can be extended with concrete loader logic;
- a public-only endpoint allowlist with denylist dominance, ready to be consulted by every future endpoint reference site;
- a frozen invalid-window taxonomy that both collector and replay layers can emit;
- a manifest data model that the future eligibility gate is the only authorized path to flip to `research_eligible=True`;
- a raw-writer primitive that future collectors can compose with, ensuring atomic finalization and refusal to write under the reserved project data tree.

---

## 14. What Phase 4aw does not enable

- No capture.
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
- No 5m, 1m, aggTrades, tick, mark-price 30m / 4h, or order-book data acquisition.

---

## 15. Implementation / governance review

### What changed?

- One new package (`src/prometheus/research/microstructure/`), 6 source files, 6 mypy-strict-clean modules.
- One new test tree (`tests/research/microstructure/`), 7 test files, 114 passing tests.
- One new `.gitignore` line (`data/microstructure/`).
- Two new docs files (this memo and the closeout).
- A narrow update to `current-project-state.md`.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text.
- No Phase 4ak governance.
- No Phase 4al refined no-rescue rule.
- No Phase 4j §11, Phase 3r §8, Phase 3v §8, or Phase 3w §6 / §7 / §8 governance.
- No data manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or anywhere else.
- No existing strategy spec, backtest plan, or validation checklist.
- No existing script under `scripts/`.
- No existing test under `tests/unit/`, `tests/integration/`, `tests/simulation/`, or `tests/fixtures/`.

### Were any locks, verdicts, or safety boundaries affected?

No. The scaffold is inert. Locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) remain verbatim. Verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of:

- `scripts/phase3q_5m_acquisition.py`
- `scripts/phase3s_5m_diagnostics.py`
- `scripts/phase4i_v2_acquisition.py`
- `scripts/phase4l_v2_backtest.py`
- `scripts/phase4r_g1_backtest.py`
- `scripts/phase4x_c1_backtest.py`
- `scripts/phase4aq_v1_arc_exit_path_forensics.py`

was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4aw paragraph addition.

### Is the phase mergeable as scaffold-only code-and-docs?

Yes, subject to operator review. The phase introduces only code that is verifiably inert (no network, no project data writes, no live endpoint calls, no successor authorisation), is fully covered by 114 tests, passes whole-repo ruff and mypy strict, and introduces zero new test regressions. The two pre-existing simulation failures are unrelated to Phase 4aw (verified on `main` directly).

---

## 16. Research interpretation review

> *In plain English, using the required 8-question format.*

### 1. What did this phase prove?

It proved that the project can add an inert public-only microstructure research scaffold without acquiring data, contacting endpoints, opening WebSockets, downloading archives, writing project data, or coupling to runtime / execution / persistence. It proved that the public endpoint allowlist with denylist dominance can be encoded as pure data and verified by automated tests. It proved that the 17-trigger invalid-window taxonomy from Phase 4au §23 can be expressed as a frozen Python data model with full round-trip serialisation. It proved that the manifest data model can default `research_eligible` to `False` and refuse all flip attempts at the scaffold layer. It proved that an atomic raw-writer primitive can be implemented and rigorously tested entirely within pytest temporary directories.

### 2. What did this phase not prove?

It did not prove anything about Binance microstructure data quality, edge, opportunity rate, or strategy viability. It did not prove that any specific endpoint behaves as documented. It did not prove that local order-book reconstruction is feasible. It did not prove that the eligibility gate is correct (the gate is not implemented). It did not prove that any historical strategy verdict is wrong. It did not prove that any project lock should change. It does not prove anything about live readiness.

### 3. Which original questions did it answer?

- "Can the project safely add a foundational microstructure research scaffold without creating data-capture or trading capability?" → **Yes**, demonstrated by the merged code, the 114 passing tests, and the verified-empty `data/microstructure/` directory.
- "Does the public-only endpoint allowlist + denylist dominance pattern work in code?" → **Yes**, verified by `test_allowlist.py`'s parametrised allow / deny tests including the `@forceOrder` vs `/fapi/v1/forceOrders` collision.
- "Can the 17-trigger invalid-window taxonomy be encoded as a tested data model?" → **Yes**, verified by `test_invalid_window.py`.
- "Can the manifest scaffold safely defer the `research_eligible` flip to a future eligibility gate?" → **Yes**, verified by `test_manifest.py::test_flip_research_eligible_always_raises`.
- "Can the raw-writer primitive refuse project data paths and finalize atomically with paired SHA256?" → **Yes**, verified by `test_raw_writer.py`.

### 4. Which original questions remain open?

- Are the documented Binance public endpoint shapes, retention windows, sequence-number conventions, and rate limits accurate at runtime? (Phase 4aw does not contact endpoints.)
- Does local LOB reconstruction from the diff-depth stream + REST snapshot satisfy the `U / u / pu` continuity rule under realistic gap / reconnect conditions? (No reconstruction implementation exists.)
- Does any future microstructure feature actually carry edge under §11.6 cost realism? (No analysis performed.)
- Should the scaffold's JSONL raw format be replaced by `.jsonl.zst`? (Documented as future additive work; zstandard is not currently a project dependency.)

### 5. What does it mean for strategy research?

It means the project now has a tested public-only research-infrastructure base. It does **not** create a strategy candidate, does **not** open any rescue path for cooled-down candidates (R2 / F1 / D1-A / V2 / G1 / C1), and does **not** authorize any feature derivation from microstructure data. Phase 4aw is infrastructure plumbing; strategy research remains under the binding M0 admissibility gate and the post-null cooldown rule for any future hypothesis.

### 6. What does it mean for governance?

Nothing changes. M0 (Phase 4ak) remains binding prospectively. The Phase 4al refined no-rescue rule remains binding. The Phase 4m 18-requirement validity gate remains binding for any future ex-ante hypothesis. The Phase 4t 10-dimension scoring matrix remains binding. The Phase 4j §11 OI subset governance, Phase 3r §8 mark-price gap governance, and Phase 3v §8 stop-trigger-domain governance remain verbatim. No governance file is modified by Phase 4aw beyond the narrow `current-project-state.md` Phase 4aw paragraph addition.

### 7. What is the clean next step?

After operator review and merge of Phase 4aw, the clean next step is **remain paused**. The scaffold is now in place; no successor phase is authorized.

If the operator separately wishes to advance the public-only capture stack toward implementation, the appropriate next step would be a separately authorized Phase 4ax (or equivalent). Phase 4av's recommended branch strategy was: Phase 4ax aggTrades-only collector skeleton; Phase 4ay manifest / eligibility integration; Phase 4az depth / LOB replay; Phase 4ba forceOrder / OI context. None of these is authorized by Phase 4aw.

### 8. What should we not do yet?

- Do not implement collectors.
- Do not implement REST clients.
- Do not implement WebSocket clients.
- Do not download archives.
- Do not call endpoints.
- Do not open the `data/microstructure/` directory tree.
- Do not implement the eligibility gate.
- Do not implement features.
- Do not implement strategies.
- Do not start ML work.
- Do not authorize a successor phase.
- Do not approach paper / shadow, live-readiness, deployment, exchange-write, or production keys.

---

## 17. Recommendation

- **Primary:** remain paused. After operator review of this memo, merge Phase 4aw into `main` so the scaffold becomes available, then stop.
- **Conditional secondary (NOT authorized by Phase 4aw):** future docs-and-code Phase 4ax aggTrades-only collector skeleton phase, separately authorized.
- **Not recommended:** implementing collectors, REST / WS clients, capture, archive downloads, eligibility-gate execution, features, ML, or any cooled-down-family rescue.
- **Forbidden:** verdict revision, lock revision, parameter optimization, strategy resurrection, M0 amendment derived from Phase 4aw reasoning, reopening the 5m research thread, data acquisition, paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials.

---

## 18. Explicit preservation of verdicts, locks, and no-rescue constraints

Phase 4aw preserves verbatim:

- **H0** remains FRAMEWORK ANCHOR.
- **R3** remains BASELINE-OF-RECORD.
- **R1a** remains RETAINED — NON-LEADING.
- **R1b-narrow** remains RETAINED — NON-LEADING.
- **R2** remains FAILED — §11.6.
- **F1** remains HARD REJECT.
- **D1-A** remains MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** remains OPERATIONALLY CLOSED.
- **V2** remains HARD REJECT — terminal for V2 first-spec.
- **G1** remains HARD REJECT — terminal for G1 first-spec.
- **C1** remains HARD REJECT — terminal for C1 first-spec.

Project locks preserved verbatim:

- §11.6 = 8 bps slippage per side.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w.
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am §11.A audit findings.
- Phase 4an inventory result.
- Phase 4ao harmonization result.
- Phase 4ap forensic plan.
- Phase 4aq computation result (descriptive evidence only).
- Phase 4ar interpretation result (descriptive interpretation only).
- Phase 4as mechanism-map result (docs-only reset evidence only).
- Phase 4at availability / capture-feasibility result (docs-only feasibility evidence only).
- Phase 4au capture-design result (docs-only design evidence only).
- Phase 4av implementation-plan result (docs-only planning evidence only).

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane.

**Recommended state remains paused. No successor phase is authorized.**
