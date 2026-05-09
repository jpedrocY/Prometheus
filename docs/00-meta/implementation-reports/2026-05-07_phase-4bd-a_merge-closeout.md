# Phase 4bd-A — Merge Closeout

**Phase identity:** Phase 4bd-A — AggTrades Normalization Implementation Plan Memo.
**Type:** docs-only implementation-plan memo.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4bd-A AggTrades Normalization Implementation Plan Memo from the Phase 4bd-A feature branch into `main`. Phase 4bd-A is text-only. It translates the Phase 4bc normalization design into a precise file-by-file, function-by-function plan for a future Phase 4bd AggTrades Normalization Implementation.

The merge brings forward only the three Phase 4bd-A tracked-doc changes. It does **not** modify source code, tests, scripts, configs, `pyproject.toml`, `README.md`, `.gitignore`, M0 governance, strategy specs, validation checklists, phase-gates, runtime docs, or MCP files; it does **not** implement a normalizer, run a normalizer, generate a normalized derived dataset, create a derived manifest, or modify any file under `data/microstructure/`; it does **not** rerun the gate, generate a new gate report, or modify the existing Phase 4bb-D gate report or its sidecar; it does **not** acquire data, call any Binance / public / private endpoint, open any WebSocket, use any credential, read or create `.env`, create or read `.mcp.json`, or enable MCP / Graphify; it does **not** flip `research_eligible` or transition the actual manifest's `eligibility_gate_status`; it does **not** authorize any successor phase. The actual on-disk Phase 4az manifest still has `research_eligible=false` and `eligibility_gate_status=pending`; the dataset remains **infrastructure evidence only**.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4bd-a/aggtrades-normalization-implementation-plan` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `53914b88dfaf3459a9fc56c4c7fd31a40e6d5b3e` |
| Phase 4bd-A commit | `5306b3550be9371973cbbfb8fbe87f7a221cdaef` (`docs(phase-4bd-a): plan aggtrades normalization implementation`) |
| Source branch HEAD | `5306b3550be9371973cbbfb8fbe87f7a221cdaef` |
| Source / origin in sync at start | yes (`main == origin/main == 53914b88`) |
| Phase 4bc merge commit ancestry | `07729df9f378452c6d1049172747dcd3e3e34a9d` confirmed ancestor of `main` (`git merge-base --is-ancestor` returns 0) |
| Phase 4bc merge-closeout file present on `main` before merge | yes — `docs/00-meta/implementation-reports/2026-05-07_phase-4bc_merge-closeout.md` |
| Merge method | `git merge --no-ff` (ort strategy) |
| Merge commit SHA | `f075e8879240cdfc4640c41610bda241179e70f9` (`docs(phase-4bd-a): merge aggtrades normalization implementation plan`, `Merge: 53914b8 5306b35`) |
| Final `main` SHA after push | `f075e8879240cdfc4640c41610bda241179e70f9` |
| Final `origin/main` SHA after push | `f075e8879240cdfc4640c41610bda241179e70f9` |
| Local / origin sync after push | in sync |

The Phase 4bd-A merge-closeout commit (this file) is added on top of the merge commit on `main`. Its SHA appears in the operator report after this file is committed.

---

## 4. Files brought forward by the merge

The merge brought forward exactly three tracked file changes from the Phase 4bd-A source branch:

| File | Change | Lines |
| ---- | ------ | -----:|
| `docs/00-meta/implementation-reports/2026-05-07_phase-4bd-a_aggtrades-normalization-implementation-plan.md` | added | +820 |
| `docs/00-meta/implementation-reports/2026-05-07_phase-4bd-a_closeout.md` | added | +193 |
| `docs/00-meta/current-project-state.md` | modified | +427 |

Total diff summary: **3 files changed, 1440 insertions(+)**.

No code under `src/prometheus/` modified. No test under `tests/` modified. No file under `scripts/` modified. No `pyproject.toml` change. No `README.md` change. No `.gitignore` change. No file under `data/`, `data/manifests/`, `data/research/`, `data/derived/`, `data/raw/`, `data/normalized/`, `data/microstructure/manifests/`, `data/microstructure/raw/`, `data/microstructure/normalized/`, or `data/microstructure/gate-reports/` modified. No M0 governance amendment. No phase-gate, strategy-spec, validation-checklist, runtime-doc, or MCP file modified.

---

## 5. Plan conclusions (recorded by Phase 4bd-A)

### Future Phase 4bd source modules

- `src/prometheus/research/microstructure/normalize_io.py` — read-only source-artefact loaders; local path discipline; output-root guard under `data/microstructure/normalized/`; SHA helpers; atomic write helpers; pyarrow Parquet writer boundary.
- `src/prometheus/research/microstructure/normalize_aggtrades.py` — public orchestrator `run_normalize_aggtrades`; per-row Phase 4ax `validate_aggtrade_payload` pipeline; one-to-one row mapping; deterministic `row_index` handling; normalized-row construction; no-feature-column guard via module-level `NORMALIZED_SCHEMA_V001` constant.
- `src/prometheus/research/microstructure/normalize_manifest.py` — derived-manifest builder using the Phase 4aw `MicrostructureManifest` data model; lineage / `governance_labels` construction (14 required keys); per-Parquet-file SHA256 recording; aggregate counts; invalid-window propagation helper; `research_eligible=false` / `eligibility_gate_status=pending` defaults.
- `src/prometheus/research/microstructure/normalize_validation.py` — post-normalization validation runner; implements every Phase 4bc check 4bc.24.1 .. 4bc.24.27 as a typed `NormalizationCheckResult`; raw-artefact immutability checks (pre-run hash vs post-run hash for manifest / raw zip / sidecar / acquisition log).
- `src/prometheus/research/microstructure/__init__.py` — narrow re-export update only (10 new public symbols added; preserve all existing Phase 4aw / 4ax / 4bb-C exports).

### Future Phase 4bd test files

- `tests/research/microstructure/test_normalize_io.py`
- `tests/research/microstructure/test_normalize_aggtrades.py`
- `tests/research/microstructure/test_normalize_manifest.py`
- `tests/research/microstructure/test_normalize_validation.py`
- `tests/research/microstructure/test_normalize_no_network.py`
- Optional `tests/research/microstructure/_normalize_fixtures.py` shared fixture builder if needed (analogous to Phase 4bb-C `_eligibility_fixtures.py`).

### Future public API

- `NormalizeAggTradesInput` (frozen dataclass)
- `NormalizeAggTradesResult` (frozen dataclass)
- `NormalizedAggTradeRow` (frozen dataclass — exactly 19 fields per Phase 4bc §11)
- `NormalizationManifestDraft` (frozen dataclass)
- `NormalizationValidationResult` (frozen dataclass)
- `NormalizationCheckResult` (frozen dataclass)
- `NormalizationCheckStatus` (`StrEnum` — exactly 4 values: `PASS` / `FAIL` / `NOT_APPLICABLE` / `ERROR`)
- `NormalizationIOError` (Exception)
- `NormalizationValidationError` (Exception)
- `run_normalize_aggtrades(inp: NormalizeAggTradesInput) -> NormalizeAggTradesResult` (function)

### Future Phase 4bd 16-step execution flow

Step 1 verify paths under `data/microstructure/`; Step 2 read source raw manifest and hash; Step 3 read raw sidecar and raw zip hash; Step 4 read acquisition log and hash; Step 5 verify Phase 4bb-D PASS gate report reference (cited SHA `96f09159...`; gate `code_commit_sha=aa612ba2...`; `report_id=microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`); Step 6 in-memory zip iteration (no on-disk decompression to tracked paths); Step 7 per-row Phase 4ax `validate_aggtrade_payload`; Step 8 one-to-one mapping with deterministic `row_index` counter; Step 9 schema-equality assertion against `NORMALIZED_SCHEMA_V001` module-level constant; Step 10 atomic Parquet write under `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet` (write-then-rename via `os.replace`; refuse-to-overwrite); Step 11 file SHA256 for derived manifest entry; Step 12 derived manifest builder + atomic write at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` (`research_eligible=false`; `eligibility_gate_status=pending`); Step 13 27-check validation suite via `normalize_validation.run_all_checks(...)`; Step 14 pre/post raw-artefact hash equality (manifest, raw zip, sidecar, acquisition log); Step 15 result construction with `research_eligible_after = False` and `no_successor_authorization = True` invariants; Step 16 Stage-0-only documentation in docstring + closeout.

### Phase 4bc 27 validation checks mapped to functions / tests

Every Phase 4bc check ID `4bc.24.1` .. `4bc.24.27` mapped to:

- a `check_*` function in `normalize_validation.py` (e.g. `check_input_raw_manifest_exists`, `check_gate_report_citation_recorded`, `check_raw_manifest_sha_matches`, ..., `check_no_forbidden_imports`);
- one positive test (PASS path on a clean fixture) and one negative test (deliberate fault injection that produces FAIL) in `test_normalize_validation.py`;
- 54+ tests minimum from this mapping alone, plus orchestrator / API / boundary / I/O / manifest / static-scan tests for ~90+ total new tests.

### Future Stage-0-only derived artefact status

A future Phase 4bd run produces Stage-0 derived artefacts only:

- `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet` (gitignored);
- `data/microstructure/normalized/...<SYMBOL>-aggTrades-<YYYY-MM-DD>.parquet.sha256` paired sidecar (gitignored);
- `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` (gitignored).

Stage-1 (inspected), Stage-2 (gate-passed), Stage-3 (research-eligible), and Stage-4 (feature-cleared) transitions each require their own separately authorized phase. None of these is authorized by Phase 4bd-A.

### Future normalized family

- Family name: `microstructure_normalized_aggtrades_v001` (derived; never overwrites the raw family `microstructure_raw_aggtrades_v001`).

### Derived manifest defaults

- `research_eligible = false`
- `eligibility_gate_status = pending`

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant continues to apply for raw families; derived families would need a separately authorized Stage-3 transition phase to relax that invariant via a sibling successor-state mechanism.

### Future Phase 4bd forbidden outputs

- No features, labels, signals, returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, trend, momentum, volatility metrics, MFE / MAE, R-multiples, PnL, equity, position state, or strategy signals.
- No ML training, no strategy implementation, no backtests.

### Future Phase 4bd preservation requirements

- Raw artefact hashes preserved pre/post run (manifest, raw zip, sidecar, acquisition log).
- Normalized output written only under gitignored `data/microstructure/normalized/`.
- Derived manifest written only at the approved manifest path.
- No mutation of any raw artefact or the existing Phase 4bb-D gate report.
- `research_eligible_after = False` and `no_successor_authorization = True` invariants enforced at the framework layer.
- No successor phase authorized by implementation alone.

---

## 6. Local gitignored gate report reference

| Item | Value |
| ---- | ----- |
| Report path | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Sidecar path | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json.sha256` |
| Report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Recomputed SHA256 at merge time | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| SHA match | yes — bit-for-bit identical to sidecar |
| Local presence at merge time | present in this workspace (17,053 bytes report; 140 bytes sidecar) |
| Committed to repository? | no — gitignored under `.gitignore:85: data/microstructure/` |

The Phase 4bb-D gate report is not committed and was not modified by Phase 4bd-A or by this merge. Phase 4bd-A's plan references the report by SHA + path + `report_id` + `code_commit_sha` + status + counts in tracked Markdown only. The doubled `gate-reports/gate-reports/` segment in the report path is observed Phase 4bb-C orchestrator behavior and was not changed by Phase 4bd-A.

---

## 7. Validation results

| Gate | Result |
| ---- | ------ |
| `git diff --stat main...HEAD` (on branch, pre-merge) | exactly the three Phase 4bd-A tracked-doc changes (+1440 lines) |
| `git diff --name-only main...HEAD` | three Phase 4bd-A tracked-doc paths only |
| `ruff check .` | PASS (`All checks passed!`) |
| `pytest tests/research/microstructure/` | PASS (258 passed in ~3 s) |
| `pytest` (whole repo) | 1041 passed, 2 failed |
| The 2 failures | `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`; both pre-existing on `main` before Phase 4bd-A (zero new regressions) |
| `mypy` (whole repo, strict) | `Success: no issues found in 93 source files` |
| `git check-ignore -v data/microstructure/` | `.gitignore:85:data/microstructure/` |
| `git status` post-merge | clean working tree on `main`; only the always-untracked `.claude/scheduled_tasks.lock` and gitignored `data/research/` listed |

Phase 4bd-A introduced zero new regressions.

---

## 8. Boundary confirmations

| Boundary | Preserved? |
| -------- | :--------: |
| No source code change | yes |
| No test change | yes |
| No script change | yes |
| No config change | yes |
| No `.gitignore` change | yes |
| No M0 governance change | yes |
| No data acquisition | yes |
| No public-endpoint calls | yes |
| No Binance API calls | yes |
| No WebSocket | yes |
| No credential / `.env` / `.mcp.json` / MCP / Graphify | yes |
| No data normalization occurred | yes |
| No derived dataset created | yes |
| No feature computation | yes |
| No ML / strategy / backtest | yes |
| No mutation of `data/microstructure/` | yes |
| Original Phase 4az manifest unchanged | yes |
| Phase 4bb-D gate report unchanged (present this workspace; SHA recomputed identical) | yes |
| `research_eligible` for raw family stays `false` | yes |
| `eligibility_gate_status` stays `pending` | yes |
| No retained verdict revised | yes |
| No project lock loosened | yes |
| No M0 amendment | yes |
| No successor authorized | yes |

---

## 9. Retained verdict ledger (preserved verbatim)

| Family | Status |
| ------ | ------ |
| H0 | FRAMEWORK ANCHOR |
| R3 | BASELINE-OF-RECORD |
| R1a | RETAINED — NON-LEADING |
| R1b-narrow | RETAINED — NON-LEADING |
| R2 | FAILED — §11.6 |
| F1 | HARD REJECT |
| D1-A | MECHANISM PASS / FRAMEWORK FAIL |
| 5m thread | OPERATIONALLY CLOSED (Phase 3t) |
| V2 | HARD REJECT — terminal for V2 first-spec |
| G1 | HARD REJECT — terminal for G1 first-spec |
| C1 | HARD REJECT — terminal for C1 first-spec |

No retained verdicts were revised by Phase 4bd-A or by this merge.

---

## 10. Project locks (preserved verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7 strict integrity gate; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.

No project locks were changed by Phase 4bd-A or by this merge. M0 was not amended.

---

## 11. No-rescue constraints (preserved verbatim)

Phase 4bd-A did not authorize and explicitly forbids:

- R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime;
- F1-prime / D1-A-prime / D1-B;
- V2-prime / V2-narrow / V2-relaxed / V2 hybrid;
- G1-prime / G1-narrow / G1-extension / G1 hybrid;
- C1-prime / C1-narrow / C1-extension / C1 hybrid;
- V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bd-A reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any raw aggTrades family;
- transitioning the raw manifest's `eligibility_gate_status` from `pending` to `pass` without a separately authorized successor-state phase that preserves the original raw manifest byte-identically;
- flipping `research_eligible` to `true` on any derived normalized family without the full Stage-0 → Stage-3 evidence chain;
- normalization implementation, feature computation, ML training, strategy implementation, or backtest based on the Phase 4bd-A plan alone;
- additional data acquisition justified by the Phase 4bd-A plan;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 12. Successor authorization

**No successor phase is authorized by the Phase 4bd-A merge.**

Specifically:

- no Phase 4bd (AggTrades Normalization Implementation);
- no Phase 4be;
- no Phase 4bf;
- no Phase 4bb-F (Gate Report Output Path Hygiene);
- no Phase 4bb-G (Raw Manifest Successor-State Recording);
- no Phase 5;
- no Phase 4 canonical;
- no additional acquisition;
- no normalization implementation;
- no features;
- no ML;
- no strategy;
- no backtest;
- no paper / shadow;
- no live-readiness;
- no deployment;
- no exchange-write;
- no production keys;
- no authenticated APIs;
- no private endpoints;
- no user stream;
- no MCP / Graphify / `.mcp.json` / credentials.

A future docs-and-code Phase 4bd (AggTrades Normalization Implementation) is the conditional next option only if the operator wants to begin moving toward implementation; it must implement the Phase 4bc design per the Phase 4bd-A plan and produce Stage-0 derived artefacts only. A future code-and-docs Phase 4bb-F (gate-report output-path hygiene) is the conditional cleanup option only before any future repeated gate execution. A future docs-and-local-gitignored-output (or docs-and-code) Phase 4bb-G (raw-manifest successor-state recording) is the conditional policy-marker option only if the operator wants a machine-readable Stage-2 marker on the raw manifest. None of these are authorized by Phase 4bd-A or by this merge.

---

## 13. Recommended state

**Recommended state: remain paused. No next phase authorized.**

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible = false`; `eligibility_gate_status = pending`. The Phase 4bb-D PASS gate report exists locally under the gitignored `data/microstructure/gate-reports/` namespace; it is not committed; its SHA256 (`96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`) is the pinning hash recorded in tracked Markdown. Phase 4bd-A does not authorize any further work.

Phase 4 (canonical) remains unauthorized. Phase 4bd / Phase 4be / Phase 4bf / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, exchange-write, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.
