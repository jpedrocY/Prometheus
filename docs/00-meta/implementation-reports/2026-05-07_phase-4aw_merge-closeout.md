# Phase 4aw — Merge Closeout

**Phase identity:** Phase 4aw — Public-Only Microstructure Capture Scaffold Implementation.
**Type:** code-and-docs scaffold-only implementation phase.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the inert public-only microstructure research scaffold from the Phase 4aw feature branch into `main`. The scaffold realises the Phase 4av implementation plan at scaffold-only scope: six source modules under `src/prometheus/research/microstructure/`, seven test files under `tests/research/microstructure/`, one new `.gitignore` line for `data/microstructure/`, the Phase 4aw memo, the Phase 4aw closeout, and a narrow `current-project-state.md` update.

The merge does **not** acquire data, contact endpoints, open WebSockets, download archives, implement collectors, REST clients, WebSocket clients, order-book reconstruction, deterministic replay, normalizers, eligibility-gate execution, feature computation, strategies, or ML. It does **not** create the `data/microstructure/` directory, write under any project data path, or create real project manifests. It does **not** authorize any successor phase.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4aw/public-only-microstructure-capture-scaffold-implementation` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `46314be989990f33821a67199921ebec2a3aef55` |
| Phase 4aw scaffold commit (source branch) | `6f65000844187886c8fd019853c88b4c1bbe5b8b` |
| Phase 4aw closeout commit (source branch) | `59f4fdf8da9c2cdd009292d8165224460dd2f77c` |
| Source branch HEAD | `59f4fdf8da9c2cdd009292d8165224460dd2f77c` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff --no-commit` |

The merge commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

Phase 4aw introduces 18 file changes (3,057 insertions, 0 deletions).

**Added (16 new files):**

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

**Modified (2 files, narrow):**

```
.gitignore                              (one new line: data/microstructure/)
docs/00-meta/current-project-state.md   (Phase 4aw narrative paragraph + new "Current phase:" block; prior Phase 4av block preserved as historical context)
```

**Files NOT modified by the merge:**

- No file under `src/prometheus/` outside the new microstructure package.
- No existing test under `tests/unit/`, `tests/integration/`, `tests/simulation/`, or `tests/fixtures/`.
- No existing script under `scripts/` (Phase 3q / Phase 3s / Phase 4i / Phase 4l / Phase 4r / Phase 4x / Phase 4aq scripts all unchanged).
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, runtime doc, or governance memo.
- No `pyproject.toml`, `README.md`, or top-level config.

---

## 5. Phase 4aw was scaffold-only code-and-docs

**Confirmed.** Phase 4aw is a scaffold-only code-and-docs phase. Its scope is strictly limited to:

- inert source modules (no imports from `prometheus.runtime`/`execution`/`persistence`; no `requests`/`httpx`/`aiohttp`/`websockets`/`binance`/`dotenv`; no `os.environ`/`getenv`);
- pytest test files using `tmp_path` only;
- one `.gitignore` line;
- two new docs files;
- one narrow `current-project-state.md` update.

It is verified by automated import-boundary and content-scan tests that the scaffold contains no live endpoint references, no credential paths, and no MCP / Graphify / `.mcp.json` / user stream / listenKey / order / account / position / leverage / margin references in code (docstrings and comments excluded from the scan are not source-active).

---

## 6. Phase 4aw scaffold result summary

The scaffold installs six inert source modules:

- **`__init__.py`** — pure package marker re-exporting `__all__`.
- **`config.py`** — frozen `MicrostructureConfig` dataclass (`endpoint_allowlist`, `endpoint_denylist`, `symbol_allowlist`, `storage_root`, `dataset_family_config`, `invalid_window_thresholds`, `eligibility_gate_thresholds`) plus `DatasetFamilyConfig`, `InvalidWindowThresholds`, `EligibilityGateThresholds`, and a pure `validate_config(...)` function with `ConfigValidationError`. Default symbols `("BTCUSDT", "ETHUSDT")` only; alt symbols require explicit caller admission.
- **`allowlist.py`** — immutable `ALLOWLIST_PATTERNS` and `DENYLIST_TOKENS` plus pure `is_endpoint_allowed`/`is_endpoint_denied`/`assert_endpoint_allowed` and `EndpointNotAllowedError`. Denylist dominates allowlist (so `@forceOrder` WS pattern is admitted but `/fapi/v1/forceOrders` user-scope authenticated REST is denied).
- **`invalid_window.py`** — `InvalidWindowReason` `StrEnum` with **exactly seventeen** values matching Phase 4au §23 (`MISSING_SEQUENCE`, `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `GAP_AFTER_RECONNECT`, `SNAPSHOT_MISMATCH`, `CLOCK_SKEW`, `SYMBOL_MISMATCH`, `STALE_STREAM`, `STALE_BOOK`, `IMPOSSIBLE_SPREAD`, `NEGATIVE_SIZE`, `ZERO_OR_INVALID_PRICE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP`, `FORCE_ORDER_PROXY_INCOMPLETENESS`, `FAILED_ATOMIC_WRITE`, `PARTIAL_FILE_RECOVERY_EVENT`); `InvalidWindowSeverity` (`INFO`, `WARN`, `ERROR`); `DownstreamEligibilityAction` (`FLAG`, `EXCLUDE`, `PROXY_ONLY`); frozen `InvalidWindow` dataclass with full round-trip serialisation.
- **`manifest.py`** — `MicrostructureManifest` with `research_eligible` defaulting `False` and `eligibility_gate_status` defaulting `EligibilityGateStatus.PENDING`. **`flip_research_eligible(...)` always raises `ManifestImmutableError`** — only the future eligibility gate (separately authorized) may flip the flag. Append-only mutation; caller-controlled `save(path)` / `load(path)` that refuse to overwrite.
- **`raw_writer.py`** — `RawWriter` primitive with atomic write-then-rename, paired SHA256 finalisation, no overwrite, refuses paths under `data/microstructure/` regardless of OS separator, refuses stale `.tmp` companions, refuses directories or non-`Path`. Tests use pytest `tmp_path` only.

### Scaffold modules added

```
src/prometheus/research/microstructure/__init__.py
src/prometheus/research/microstructure/config.py
src/prometheus/research/microstructure/allowlist.py
src/prometheus/research/microstructure/invalid_window.py
src/prometheus/research/microstructure/manifest.py
src/prometheus/research/microstructure/raw_writer.py
```

### Tests added

```
tests/research/__init__.py
tests/research/microstructure/__init__.py
tests/research/microstructure/test_config.py
tests/research/microstructure/test_allowlist.py
tests/research/microstructure/test_invalid_window.py
tests/research/microstructure/test_manifest.py
tests/research/microstructure/test_raw_writer.py
tests/research/microstructure/test_import_boundaries.py
```

114 microstructure tests pass, covering: config validation; allowlist / denylist behaviour including denylist dominance; the seventeen-trigger invalid-window taxonomy and its round-trip; manifest defaults and the `flip_research_eligible` always-raises invariant; raw-writer atomicity, no-overwrite, stale-`.tmp` rejection, project-data-path rejection, and SHA256 correctness; and a static import-boundary scan plus a code-content denylist scan against every scaffold source file.

### `.gitignore` line added

```
data/microstructure/
```

The line is added at line 85 of `.gitignore`, immediately after the `private/`, `data/secrets/`, and `data/runtime/` entries in the "Private / local data zones not covered by runtime/" section.

---

## 7. Boundary confirmations

The Phase 4aw merge confirms verbatim:

- **`data/microstructure/` was not created.** The directory does not exist before, during, or after the merge. The new `.gitignore` line protects against accidental future commits.
- **No project data writes occurred.** Tests use pytest `tmp_path` only. The raw-writer primitive explicitly rejects any path resolving under `data/microstructure/` regardless of OS separator.
- **No real manifests were created.** The manifest data model is inert. No file was written under `data/manifests/` or any project data tree.
- **No endpoint calls occurred.** No source file imports `httpx`, `requests`, `aiohttp`, `websockets`, or any Binance SDK. The import-boundary test enforces this on every scaffold module.
- **No WebSockets were opened.** No WebSocket client is implemented.
- **No archive downloads occurred.** No code path retrieves public bulk archives.
- **No collectors, REST clients, WebSocket clients, order-book reconstruction, deterministic replay, normalizers, eligibility-gate execution, feature computation, strategy, or ML were implemented.** None of `public_rest.py`, `public_ws.py`, collector modules, normalizer modules, replay modules, eligibility-gate execution, healthcheck, or dashboard hook exists in the scaffold.

---

## 8. Validation summary

Validation was performed on the Phase 4aw branch immediately before merge.

| Command | Result |
| ------- | ------ |
| `python -m compileall src/prometheus/research/microstructure` | pass |
| `python -m compileall tests/research/microstructure` | pass |
| `ruff check src/prometheus/research/microstructure tests/research/microstructure` | `All checks passed!` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest tests/research/microstructure` | **114 passed** |
| `pytest` (whole repo) | 897 passed, **2 failed** (verified pre-existing on `main` and unrelated to Phase 4aw — see below); **zero new regressions** from Phase 4aw |
| `mypy src/prometheus/research/microstructure` | `Success: no issues found in 6 source files` |
| `mypy` (whole repo) | `Success: no issues found in 88 source files` (was 82 on main; 6 new microstructure modules now pass mypy strict) |
| `git diff --check` | clean |
| `data/microstructure/` directory check | **DOES NOT EXIST** |

### Pre-existing whole-repo pytest failures

**Whole-repo pytest has 2 failures, both reproduced on main before Phase 4aw and unrelated to the new scaffold; Phase 4aw introduced zero new regressions.**

Both failures are in `tests/simulation/test_backtest_real_2026_03.py`:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`

Both fail with `KeyError: 'trade_count'` raised in the unrelated `src/prometheus/research/data/storage.py:232`. The failures were verified as pre-existing on `main` directly via `git checkout main && pytest tests/simulation/test_backtest_real_2026_03.py`, which produced the same two failures with identical traces. The new Phase 4aw scaffold does not touch `src/prometheus/research/data/storage.py`, the simulation tests, or any related path.

---

## 9. Implementation / governance review

### What changed?

- One new package under `src/prometheus/research/microstructure/`, 6 source files, mypy strict clean.
- One new test tree under `tests/research/microstructure/`, 7 test files, 114 passing tests.
- One new `.gitignore` line (`data/microstructure/`).
- Two new docs files (memo + closeout) under `docs/00-meta/implementation-reports/`.
- One narrow update to `docs/00-meta/current-project-state.md`.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).
- No Phase 4ak / 4al / 4j / 3r / 3v / 3w governance.
- No data manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/` (all gitignored or untouched).
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing test or script.

### Were any locks, verdicts, or safety boundaries affected?

No. The scaffold is inert. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4aw paragraph addition.

### Mergeability

The phase introduces only code that is verifiably inert (no network, no project data writes, no live endpoint calls, no successor authorisation), is fully covered by 114 tests, passes whole-repo ruff and mypy strict, and introduces zero new test regressions. The merge is a clean automatic merge (no conflicts) with `--no-ff` to preserve the Phase 4aw commit history.

---

## 10. Research interpretation review

### What did this phase prove?

That an inert public-only microstructure scaffold can be added to the Prometheus repository without acquiring data, contacting endpoints, opening WebSockets, downloading archives, writing project data, or coupling to runtime / execution / persistence. The public endpoint allowlist with denylist dominance was encoded as pure data and verified by tests. The seventeen-trigger invalid-window taxonomy from Phase 4au §23 was expressed as a frozen Python data model with full round-trip serialisation. The manifest data model defaults `research_eligible` to `False` and refuses all flip attempts at the scaffold layer. An atomic raw-writer primitive was implemented and rigorously tested entirely within pytest temporary directories.

### What did this phase NOT prove?

Anything about Binance microstructure data quality, edge, opportunity rate, or strategy viability. No specific endpoint behaviour was verified. Local order-book reconstruction was not implemented. The eligibility gate was not implemented. No historical strategy verdict changed. No project lock changed. Nothing about live readiness was demonstrated.

### What does this mean for strategy research?

The project now has a tested public-only research-infrastructure base. It does **not** create a strategy candidate, does **not** open any rescue path for cooled-down candidates (R2 / F1 / D1-A / V2 / G1 / C1), and does **not** authorize any feature derivation from microstructure data. Phase 4aw is plumbing; strategy research remains under the binding M0 admissibility gate and the post-null cooldown rule.

### What does this mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4m 18-requirement validity gate, the Phase 4t 10-dimension scoring matrix, Phase 4j §11 OI subset governance, Phase 3r §8 mark-price gap governance, and Phase 3v §8 stop-trigger-domain governance all remain verbatim.

### Clean next step

After the merge, **remain paused**. The scaffold is in place; no successor phase is authorized. If the operator separately wishes to advance, the most natural separately-authorized next step would be a future Phase 4ax (or equivalent) — for example, an aggTrades-only collector skeleton phase per Phase 4av's recommended branch strategy. None of these is authorized by this merge.

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
- No M0 amendment derived from Phase 4aw reasoning.

---

## 14. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4ax,
- Phase 5,
- Phase 4 canonical,
- data acquisition (5m / 1m / aggTrades / tick / mark-price 30m / 4h / order-book),
- Binance endpoint calls,
- public-archive downloads,
- WebSocket connections,
- endpoint implementation,
- data-capture implementation,
- order-book reconstruction implementation,
- replay implementation,
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
- live WebSocket implementation,
- MCP, Graphify, `.mcp.json`,
- credentials.

Any successor phase requires a separate operator authorization brief. The Phase 4av §"Operator decision menu" Phase 4aw branch strategy (Phase 4ax aggTrades-only collector skeleton; Phase 4ay manifest / eligibility integration; Phase 4az depth / LOB replay; Phase 4ba forceOrder / OI context) is documented as a possible future path but is **not** activated by this merge.

---

## 15. Recommended state

**Recommended state remains paused.** The Phase 4aw scaffold is now available on `main` for any future separately-authorized phase to build upon. No further work should occur until the operator separately authorizes a future phase.

---

## 16. Final note

This merge-closeout is preserved alongside the Phase 4aw memo and the Phase 4aw closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4aw commit history is preserved and the boundary between Phase 4av (implementation plan) and Phase 4aw (scaffold realisation) remains visible in `git log`.

**Phase 4aw is now merged into `main`. No next phase is authorized.**
