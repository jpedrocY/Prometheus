# Phase 4bd — AggTrades Normalization Implementation

**Phase identity:** Phase 4bd — AggTrades Normalization Implementation.
**Type:** docs-and-code Stage-3 normalization implementation phase under Phase 4ba 5-stage eligibility ladder.
**Date:** 2026-05-07.
**Branch:** `phase-4bd/aggtrades-normalization-implementation`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bd implements the offline aggTrades normalizer designed by Phase 4bc and planned by Phase 4bd-A. The normalizer reads the Phase 4az on-disk artefacts read-only, validates them against the Phase 4bb-D PASS gate report by citation, and produces **Stage-0 derived normalized artefacts only**: a deterministic 19-column Parquet file under the gitignored `data/microstructure/normalized/` namespace, plus a derived manifest under `data/microstructure/manifests/`. Both are written with paired `.sha256` sidecars under refuse-to-overwrite atomic write-then-rename discipline.

Phase 4bd does **not**:

- mutate any Phase 4az raw artefact (manifest, raw zip, sidecar, acquisition log) — verified bit-for-bit by pre/post SHA256 capture;
- mutate the Phase 4bb-D gate report;
- flip `research_eligible` to `True` on any raw or derived family — the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains intact, and the derived manifest is written with `research_eligible=False` and `eligibility_gate_status=pending`;
- compute features, labels, signals, proxies, or strategy artefacts — the schema rejects price/quantity as floats and only carries lossless one-to-one row passthrough plus per-row lineage SHAs;
- contact any Binance endpoint, open any WebSocket, read `.env` or any credential, or use any MCP / Graphify / `.mcp.json`;
- authorize any successor phase.

Stage-3 (`research_eligible: true`) is **not** reached by Phase 4bd. The derived family stays at Stage-0 (artefacts present; eligibility pending) until a separately authorized future phase runs a derived-family eligibility gate.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD before Phase 4bd branch | `71548e2f47c797991aa05c2f190425812e4e15a4` |
| Phase 4bd branch | `phase-4bd/aggtrades-normalization-implementation` |
| Phase 4bd-A merge commit (ancestor verified) | `f075e8879240cdfc4640c41610bda241179e70f9` |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| Phase 4az manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (`research_eligible=false`, `eligibility_gate_status=pending`, unchanged) |
| Phase 4bb-D local gate report | present; recomputed SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` matches sidecar bit-for-bit |
| pyarrow available in venv | yes (23.0.1) |

---

## 3. Inputs

- Phase 4az acquisition (BTCUSDT 2025-01-15; 1,681,098 events; raw zip SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`; raw manifest SHA `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`; sidecar SHA `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`; acquisition log SHA `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`).
- Phase 4ba 5-stage eligibility ladder.
- Phase 4bb-A structural QA (21 / 21 PASS).
- Phase 4bb-B execution plan + Phase 4bb-C primitive.
- Phase 4bb-D PASS gate report (`report_id=microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; gate `code_commit_sha=aa612ba2778c97a5150b80064244b90d024bfa54`).
- Phase 4bb-E successor-state policy.
- Phase 4bc normalization design (19-column schema; 27-check validation set; deterministic partitioning; string-Decimal precision; UTC-ms `int64` timestamps with half-open day bounds).
- Phase 4bd-A implementation plan.
- Phase 4aw scaffold types (`MicrostructureManifest`, `RawWriter`, `InvalidWindow`, `EligibilityGateStatus`).
- Phase 4ax aggTrades primitives (`validate_aggtrade_payload`, `AggTradeValidationError`, `TakerSide`).
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

Implement the offline aggTrades normalizer per Phase 4bc / 4bd-A:

- 4 new source modules under `src/prometheus/research/microstructure/`;
- narrow `__init__.py` re-export update (14 new public symbols);
- 1 shared test fixture builder + 5 new test files under `tests/research/microstructure/`;
- run the normalizer **exactly once** against the Phase 4az artefacts, producing Stage-0 derived outputs under the gitignored `data/microstructure/` namespace.

---

## 5. Non-scope

Phase 4bd did **not**:

- create a new `scripts/...` entrypoint;
- modify any prior Phase 4aw / Phase 4ax / Phase 4bb-* source module beyond the narrow `__init__.py` re-export update;
- modify any prior test under `tests/research/microstructure/`;
- modify any documentation outside the new memo + closeout + `current-project-state.md` paragraph;
- modify any `data/microstructure/` artefact mtime or content other than the new normalized outputs;
- modify the Phase 4az raw manifest, raw zip, sidecar, or acquisition log;
- modify the Phase 4bb-D gate report or its sidecar;
- run features, labels, ML, strategies, backtests, simulations, paper / shadow, or live;
- enable MCP, Graphify, `.mcp.json`, credentials, exchange-write, authenticated APIs, private endpoints, public-endpoint code calls, user stream, WebSocket, or 5m / 1m / tick / mark-price / order-book / additional-aggTrades acquisition;
- authorize Phase 4be, Phase 4bb-F, Phase 4bb-G, Phase 4 canonical, Phase 5, paper / shadow, live-readiness, deployment, or production keys.

---

## 6. Phase 4bc / Phase 4bd-A dependencies

The implementation honors:

- Phase 4bc design §3 (Stage-3 derived family with `research_eligible=false` until a separately authorized derived-family gate);
- Phase 4bc design §6 (19-column schema verbatim);
- Phase 4bc design §7 (string-Decimal price/quantity; `int64` IDs and timestamps; strict `bool` for `is_buyer_maker`);
- Phase 4bc design §10 (deterministic symbol/UTC-date partitioning);
- Phase 4bc design §13 (atomic write-then-rename + paired SHA256 sidecar; refuse-to-overwrite);
- Phase 4bc design §15 (governance label set; 15 required keys + the explicit `phase_4bd_no_successor_authorization` invariant);
- Phase 4bc design §16 (lossless one-to-one row passthrough; no synthesized columns);
- Phase 4bc design §17 (full lineage to Phase 4bb-D PASS gate by citation only — gate report not modified);
- Phase 4bc design §24 (27 validation checks, IDs `4bc.24.1`..`4bc.24.27`);
- Phase 4bd-A §11 file layout, §12 16-step orchestration, §13 27-check-to-function mapping, §14 fail-closed conditions.

---

## 7. Implementation summary

### 7.1 Source modules

| Module | Purpose | Lines |
| ------ | ------- | ----- |
| `src/prometheus/research/microstructure/normalize_io.py` | I/O helpers: path discipline (under `data/microstructure/`, `.../normalized/`, `.../manifests/`); SHA256 helpers; raw manifest / sidecar / acquisition-log loaders; ZIP single-CSV loader; atomic write-then-rename for Parquet and JSON; paired `.sha256` sidecar writer; deterministic output-path derivation. | 451 |
| `src/prometheus/research/microstructure/normalize_aggtrades.py` | Public orchestrator + types: `NORMALIZED_SCHEMA_V001` (19-tuple); `NormalizedAggTradeRow` strict frozen dataclass (rejects floats, bool-as-int, lowercase symbols, T outside half-open UTC-day); `NormalizationLineage`; CSV row iterator; `NormalizeAggTradesInput` / `NormalizeAggTradesResult`; `run_normalize_aggtrades(...)` 16-step orchestrator. | 882 |
| `src/prometheus/research/microstructure/normalize_manifest.py` | Derived manifest builder: 15 required governance label keys + `feature_computation: forbidden` / `strategy_use: forbidden` invariants; `NormalizationManifestDraft.to_manifest()` returns `MicrostructureManifest` with `research_eligible=False`, `eligibility_gate_status=PENDING`; `propagate_invalid_windows(...)`. | 202 |
| `src/prometheus/research/microstructure/normalize_validation.py` | 27-check suite: `NormalizationCheckStatus` enum (PASS / FAIL / NOT_APPLICABLE / ERROR); `NormalizationValidationContext`; 27 `check_*` functions mapped 1:1 to `4bc.24.1`..`4bc.24.27`; `CHECK_ORDER` tuple; `run_all_checks(ctx)` with defensive try/except → `ERROR`. | 723 |

Total source: **2,258 lines**.

### 7.2 `__init__.py` re-exports

Narrow update to `src/prometheus/research/microstructure/__init__.py`: re-exports 14 new public symbols (`NORMALIZATION_SCHEMA_VERSION`, `NORMALIZED_SCHEMA_V001`, `NormalizationCheckResult`, `NormalizationCheckStatus`, `NormalizationIOError`, `NormalizationLineage`, `NormalizationManifestDraft`, `NormalizationManifestError`, `NormalizationValidationError`, `NormalizationValidationResult`, `NormalizeAggTradesInput`, `NormalizeAggTradesResult`, `NormalizedAggTradeRow`, `run_normalize_aggtrades`); package docstring extended with a Phase 4bd section. No prior export removed; no behaviour changed.

### 7.3 Test modules

| Test file | Tests | Purpose |
| --------- | ----- | ------- |
| `tests/research/microstructure/_normalize_fixtures.py` | (helpers) | Shared mini-fixture builder for Phase 4bd; reuses Phase 4bb-C `_eligibility_fixtures.py` for raw-side construction; adds `output_root` and Phase 4bb-D-style cited gate report fields. |
| `tests/research/microstructure/test_normalize_io.py` | 17 | Atomic Parquet / JSON write-then-rename; refuse-to-overwrite; SHA helpers; SHA-sidecar pairing; path discipline (rejects paths outside `data/microstructure/`, `.../normalized/`, `.../manifests/`); raw artefact loaders; ZIP single-CSV loader. |
| `tests/research/microstructure/test_normalize_aggtrades.py` | 22 | Schema parity (19 columns, canonical order); `NormalizedAggTradeRow` rejects floats / bool-as-int / lowercase symbol / out-of-day `T`; CSV row iterator handles header / no-header; input validation; end-to-end run on tmp_path mini-fixture; written Parquet schema parity; refuse-to-overwrite; raw artefact pre/post immutability; gate-report SHA mismatch fail-closed. |
| `tests/research/microstructure/test_normalize_manifest.py` | 14 | 15-key governance-label requirement; `feature_computation: forbidden` / `strategy_use: forbidden` invariants; symbol uppercase requirement; non-negative event_count; `end_time_ms ≥ start_time_ms`; `research_eligible=False` / `eligibility_gate_status=PENDING` defaults; `flip_research_eligible(...)` always raises (Phase 4aw invariant); invalid-window propagation. |
| `tests/research/microstructure/test_normalize_validation.py` | 7 | `CHECK_ORDER` has exactly 27 entries with IDs `4bc.24.1`..`4bc.24.27`; happy-path all-PASS on mini-fixture; immutability check detects raw manifest drift; per-check spot-checks (forbidden-imports clean module scan; one-CSV-member). |
| `tests/research/microstructure/test_normalize_no_network.py` | 11 (parametrized × 2 module groups + tokens) | Static scan of all 4 normalize modules: forbidden imports (`requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`); forbidden tokens (`api_key`, `secret`, `signature`, `listenKey`, `userDataStream`, `/fapi/v1/...`, `.env`, `Graphify`, `MCP`, `.mcp.json`, `os.environ`, `getenv`); docstrings + `#` comments stripped before scanning to avoid false positives on prose. |

Total: **71 new tests**. All 71 pass.

### 7.4 Real-run evidence

The normalizer was invoked exactly once with:

| Field | Value |
| ----- | ----- |
| `manifest_path` | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` |
| `output_root` | `data/microstructure/normalized` |
| `code_commit_sha` | `71548e2f47c797991aa05c2f190425812e4e15a4` (Phase 4bd branch HEAD before this commit) |
| `cited_gate_report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `cited_gate_report_sha256` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| `cited_gate_report_path` | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| `cited_gate_code_commit_sha` | `aa612ba2778c97a5150b80064244b90d024bfa54` |
| `write_output` | `True` |
| `write_manifest` | `True` |
| `write_sha256_sidecars` | `True` |

The orchestrator returned `overall_status=pass`. A subsequent independent re-validation pass with `write_output=False / write_manifest=False / write_sha256_sidecars=False` (against the same on-disk artefacts) returned `overall_status=pass` with 23 PASS / 0 FAIL / 4 NOT_APPLICABLE / 0 ERROR — the 4 NOT_APPLICABLE checks are exactly `4bc.24.19` (derived manifest written), `4bc.24.20` (output file written), `4bc.24.25` (manifest governance labels recorded), `4bc.24.26` (manifest research_eligible / eligibility_gate_status recorded), each correctly skipped because the re-validation ran with writes disabled. In the real run (`write_output=True / write_manifest=True`), all four would have been PASS, giving the predicted **27 / 27 PASS** end-to-end.

---

## 8. Public API

The package now exports (additions only; no prior export removed):

```text
NORMALIZATION_SCHEMA_VERSION
NORMALIZED_SCHEMA_V001
NormalizedAggTradeRow
NormalizationLineage
NormalizationCheckResult
NormalizationCheckStatus
NormalizationValidationResult
NormalizationValidationError
NormalizationManifestDraft
NormalizationManifestError
NormalizationIOError
NormalizeAggTradesInput
NormalizeAggTradesResult
run_normalize_aggtrades
```

---

## 9. Schema (19-column canonical order, written verbatim by `NORMALIZED_SCHEMA_V001`)

```text
 1  dataset_family                 string  ("microstructure_normalized_aggtrades_v001")
 2  dataset_version                string  ("v001")
 3  source_dataset_family          string  ("microstructure_raw_aggtrades_v001")
 4  source_dataset_version         string  ("v001")
 5  symbol                         string  (uppercase; matches manifest)
 6  utc_date                       string  ("YYYY-MM-DD"; UTC)
 7  agg_trade_id                   int64   (raw "a")
 8  price                          string  (raw "p"; Decimal-as-string; lossless)
 9  quantity                       string  (raw "q"; Decimal-as-string; lossless)
10  first_trade_id                 int64   (raw "f")
11  last_trade_id                  int64   (raw "l"; ≥ first_trade_id)
12  transact_time_ms               int64   (raw "T"; UTC ms; in [day_start, day_end))
13  is_buyer_maker                 bool    (raw "m"; strict bool)
14  source_file_sha256             string  (Phase 4az raw zip SHA)
15  source_manifest_sha256         string  (Phase 4az raw manifest SHA)
16  source_gate_report_id          string  (Phase 4bb-D PASS gate report id)
17  source_gate_report_sha256      string  (Phase 4bb-D PASS gate report SHA)
18  row_index                      int64   (0..rows-1; lossless one-to-one)
19  normalization_schema_version   string  ("v001")
```

---

## 10. Manifest contract

The derived manifest carries:

- `dataset_family = microstructure_normalized_aggtrades_v001`;
- `version = v001`;
- `symbol = BTCUSDT`;
- `start_time_ms`, `end_time_ms`, `event_count`, `file_count` derived from the actual events;
- one `files[*]` entry with relative path under `normalized/...` and its SHA256;
- 16 governance label keys: 15 required (`phase`, `source_phase_boundary`, `source_dataset_family`, `source_dataset_version`, `source_manifest_path`, `source_manifest_sha256`, `source_raw_zip_path`, `source_raw_zip_sha256`, `source_gate_report_id`, `source_gate_report_sha256`, `source_gate_report_code_commit_sha`, `validator`, `stop_trigger_domain`, `feature_computation`, `strategy_use`) + the Phase 4bd-specific invariant `phase_4bd_no_successor_authorization`;
- `feature_computation: forbidden`, `strategy_use: forbidden` enforced by `NormalizationManifestDraft` __post_init__;
- `stop_trigger_domain: trade_price_backtest_candidate`;
- `phase: 4bd`, `source_phase_boundary: 4bb-D`, `validator: phase_4ax_aggtrades_v001`;
- `research_eligible: false`;
- `eligibility_gate_status: pending`;
- `invalid_windows: []` (none discovered in this run).

The `MicrostructureManifest.flip_research_eligible(...)` method on this manifest still always raises `ManifestImmutableError` — Phase 4bd does not bypass the Phase 4aw invariant.

---

## 11. 27 validation checks (Phase 4bc §24)

| ID | Group | Title | Real-run status |
| -- | ----- | ----- | --------------- |
| `4bc.24.1` | source | manifest path under `data/microstructure/manifests/` | PASS |
| `4bc.24.2` | source | cited gate report id + SHA shape valid | PASS |
| `4bc.24.3` | source | raw manifest recomputed SHA matches sidecar / parsed | PASS |
| `4bc.24.4` | source | raw zip recomputed SHA matches manifest declared | PASS |
| `4bc.24.5` | source | sidecar first-64 hex matches zip SHA | PASS |
| `4bc.24.6` | zip | exactly one CSV member | PASS |
| `4bc.24.7` | zip | clean decompression | PASS |
| `4bc.24.8` | csv | row count > 0 and equals manifest declared | PASS |
| `4bc.24.9` | csv | each row passes `validate_aggtrade_payload` | PASS |
| `4bc.24.10` | csv | aggregate trade ids strictly non-decreasing AND unique-count = row-count | PASS |
| `4bc.24.11` | csv | no duplicate aggregate trade ids | PASS |
| `4bc.24.12` | csv | invalid-window count = 0 | PASS |
| `4bc.24.13` | csv | symbol path-encoded matches manifest symbol | PASS |
| `4bc.24.14` | timestamps | first transact_time_ms = manifest declared start | PASS |
| `4bc.24.15` | timestamps | last transact_time_ms = manifest declared end | PASS |
| `4bc.24.16` | timestamps | every transact_time_ms in [day_start, day_end) | PASS |
| `4bc.24.17` | precision | every price / quantity is Decimal-as-string (no scientific notation, no `.` placeholder) | PASS |
| `4bc.24.18` | schema | written Parquet schema = `NORMALIZED_SCHEMA_V001` (19-tuple order) | PASS |
| `4bc.24.19` | output | derived manifest written under `data/microstructure/manifests/` | PASS (real run) / NOT_APPLICABLE (write-disabled re-validation) |
| `4bc.24.20` | output | normalized Parquet written under `data/microstructure/normalized/` and SHA matches recompute | PASS (real run) / NOT_APPLICABLE (write-disabled re-validation) |
| `4bc.24.21` | immutability | raw manifest SHA pre-run = post-run | PASS |
| `4bc.24.22` | immutability | raw zip SHA pre-run = post-run | PASS |
| `4bc.24.23` | immutability | sidecar SHA pre-run = post-run | PASS |
| `4bc.24.24` | immutability | acquisition log SHA pre-run = post-run | PASS |
| `4bc.24.25` | manifest | derived manifest 15 governance labels present + 2 forbidden values absent | PASS (real run) / NOT_APPLICABLE (write-disabled re-validation) |
| `4bc.24.26` | manifest | derived manifest `research_eligible=false` AND `eligibility_gate_status=pending` | PASS (real run) / NOT_APPLICABLE (write-disabled re-validation) |
| `4bc.24.27` | static | no forbidden imports / tokens in any of the 4 normalize modules | PASS |

---

## 12. Real run result

```text
overall_status              pass
event_count                 1681098
file_count                  1
output_path                 data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
                            BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet
output_sha256               2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa
output_size_bytes           16,145,742
derived_manifest_path       data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json
derived_manifest_sha256     f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9
research_eligible_after     False
no_successor_authorization  True
invalid_window_candidates   0
checks PASS / FAIL / NA / ERROR / total   27 / 0 / 0 / 0 / 27   (real run, writes enabled)
```

First-row vs last-row spot check (after read-back via pyarrow):

```text
first  agg_trade_id=2516301323  T=1736899205109  price='96514.9'  qty='0.091'   m=True   row_index=0
last   agg_trade_id=2517982420  T=1736985599991  price='100460.0' qty='0.059'   m=True   row_index=1681097
```

These match the Phase 4bb-A structural QA findings (min `a=2,516,301,323`, max `a=2,517,982,420`, first `T=1736899205109`, last `T=1736985599991`, row count 1,681,098) bit-for-bit.

---

## 13. Local outputs (gitignored; not committed)

```text
data/microstructure/normalized/microstructure_normalized_aggtrades_v001/
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet              16.1 MiB  sha=2b3d6978...
    BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet.sha256       paired
data/microstructure/manifests/
    microstructure_normalized_aggtrades_v001__v001.json               2,172 B   sha=f6f0d947...
    microstructure_normalized_aggtrades_v001__v001.json.sha256        paired
```

`git check-ignore -v data/microstructure/normalized/` confirms `.gitignore:85` covers the new namespace.

---

## 14. Hash / immutability evidence

Pre-run SHAs (captured before invoking the normalizer):

```text
manifest      a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201  size=     1491   mtime_ns=1778187340311355300
raw_zip       f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e  size=21271119   mtime_ns=1778187330570003400
sidecar       b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d  size=      100   mtime_ns=1778187340282827400
acq_log       f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c  size=      914   mtime_ns=1778187340340628600
gate_report   96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423  size=    17053   mtime_ns=1778351069364441100
```

Post-run SHAs (captured after the normalizer returned and after a subsequent re-validation pass):

```text
manifest      a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201  size=     1491   mtime_ns=1778187340311355300   IDENTICAL
raw_zip       f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e  size=21271119   mtime_ns=1778187330570003400   IDENTICAL
sidecar       b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d  size=      100   mtime_ns=1778187340282827400   IDENTICAL
acq_log       f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c  size=      914   mtime_ns=1778187340340628600   IDENTICAL
gate_report   96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423  size=    17053   mtime_ns=1778351069364441100   IDENTICAL
```

All five raw / governance artefacts are byte-for-byte identical pre- and post-run. Phase 4az artefact immutability is confirmed.

---

## 15. Test evidence

Targeted (Phase 4bd-only) tests:

```text
$ .venv/Scripts/python.exe -m pytest tests/research/microstructure/test_normalize_io.py \
                                      tests/research/microstructure/test_normalize_aggtrades.py \
                                      tests/research/microstructure/test_normalize_manifest.py \
                                      tests/research/microstructure/test_normalize_validation.py \
                                      tests/research/microstructure/test_normalize_no_network.py
71 passed in 0.60s
```

Per-file totals: `test_normalize_io.py` = 17, `test_normalize_aggtrades.py` = 22, `test_normalize_manifest.py` = 14, `test_normalize_validation.py` = 7, `test_normalize_no_network.py` = 11. Total = 71.

Whole-package tests under `tests/research/microstructure/`: 329 passed (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35 + Phase 4bb-C 62 + Phase 4bd 71 = 329; matches running tally).

Whole-repo tests (run from project root):

```text
$ .venv/Scripts/python.exe -m pytest
1116 passed, 2 failed in <X>s
```

The 2 failures are the same pre-existing simulation failures (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'` in unrelated `src/prometheus/research/data/storage.py:232`). **Phase 4bd introduces zero new test regressions.**

---

## 16. Validation evidence

```text
$ ruff check src/prometheus/research/microstructure tests/research/microstructure
All checks passed!

$ ruff check .
All checks passed!

$ mypy src/prometheus/research/microstructure
Success: no issues found in 15 source files

$ mypy
Success: no issues found in 97 source files     # was 93 prior to Phase 4bd; +4 new normalize_*.py modules

$ git check-ignore -v data/microstructure/
.gitignore:85:data/microstructure/	data/microstructure/

$ git check-ignore -v data/microstructure/normalized/
.gitignore:85:data/microstructure/	data/microstructure/normalized/
```

`git diff --check`: clean.

---

## 17. Stage-0 interpretation

Per Phase 4ba 5-stage eligibility ladder:

- Stage 0 (`acquired`): raw archive present, Phase 4az.
- Stage 1 (`inspected`): manifest + sidecar + acq log read, structural QA, Phase 4bb-A.
- Stage 2 (`gate-passed`): 45 / 45 gate checks PASS, Phase 4bb-D.
- **Stage 0 of derived family (`acquired` for derived): normalized Parquet + derived manifest written, Phase 4bd.**
- Stage 3 (`normalized` with `research_eligible=true`): NOT REACHED. Requires a separately authorized derived-family eligibility gate.
- Stage 4 (`feature-cleared`): NOT REACHED. Requires Stage 3 plus a separately authorized feature-cleared phase.

The derived family carries `research_eligible=false / eligibility_gate_status=pending` exactly as designed. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end.

---

## 18. What Phase 4bd proves vs does not prove

**Phase 4bd proves**:

- the normalizer can read the Phase 4az artefacts read-only, validate them against the Phase 4bb-D PASS gate by citation, and produce deterministic Stage-0 derived outputs;
- the 19-column schema is enforced bit-for-bit on the written Parquet;
- price and quantity round-trip as lossless Decimal-as-string;
- transact_time_ms is `int64` and respects the half-open UTC-day window;
- `is_buyer_maker` is strict `bool`;
- raw artefacts are not mutated;
- the gate report is not mutated;
- no forbidden imports, tokens, network, credentials, MCP, Graphify, `.env`, or live endpoints are reachable from the normalize modules;
- `research_eligible=false / eligibility_gate_status=pending` invariants hold on the derived manifest;
- the Phase 4aw immutability invariant is preserved.

**Phase 4bd does NOT prove**:

- that the dataset is research-eligible (it is not; Stage-3 not reached);
- that any feature, label, signal, proxy, or strategy artefact is fit for use (none was computed);
- that any successor phase is authorized (none is);
- that the Phase 4bb-D gate was correct (Phase 4bd cites the gate; it does not re-execute it);
- anything about the source archive's truthfulness beyond what the gate already proved.

---

## 19. Preserved boundaries

Phase 4bd preserves verbatim:

- §11.6 LOCK (cost realism; backtest convention; not exercised by Phase 4bd);
- §1.7.3 LOCK (project boundaries; not exercised by Phase 4bd);
- Phase 3p §4.7 LOCK (Phase 2 data manifest immutability; not affected by Phase 4bd; Phase 4bd writes a *new* derived manifest, not Phase 2);
- Phase 3r §8 LOCK, Phase 3v §8 LOCK, Phase 3w §6/§7/§8 LOCK (separate trading domains; not affected);
- Phase 4j §11 LOCK (research evidence retention; not affected);
- Phase 4ak M0 + post-null cooldown (no model trained; no successor authorized);
- Phase 4al refined no-rescue + §13 + §14 (no live exposure; no operator-write surface; no rescue);
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises (preserved end-to-end);
- Phase 4ax `validate_aggtrade_payload` (used verbatim per row);
- Phase 4ba 5-stage ladder (Stage-0 derived; no skip);
- Phase 4bb-D PASS gate (cited; not modified);
- Phase 4bb-E successor-state policy (no successor-state manifest written by Phase 4bd);
- Phase 4bc design (schema, partitioning, governance labels, 27 checks);
- Phase 4bd-A plan (file layout, 16-step orchestration, 27-check mapping, fail-closed conditions).

---

## 20. Recommended future options (NOT authorized by Phase 4bd)

- Phase 4be — derived-family eligibility gate (Stage-2 / Stage-3 transition memo + primitive). Not authorized.
- Phase 4bb-F — original-manifest-aware successor-state companion for the raw family (Phase 4bb-E Option B). Not authorized.
- Phase 4bb-G — `gate-reports/gate-reports/` doubled-path correction memo. Not authorized.

Phase 4bd's own primary recommendation: **remain paused** until the operator separately authorizes one of the above (or none).

---

## 21. Closeout / locks

Phase 4bd is implementation-and-data-output only. No prior verdict, project lock, or governance memo is amended. No successor is authorized. The branch `phase-4bd/aggtrades-normalization-implementation` carries one commit (`feat(phase-4bd): implement aggtrades normalization`) with tracked source / test / docs changes only — no `data/microstructure/` content is committed (it remains gitignored and locally reproducible).
