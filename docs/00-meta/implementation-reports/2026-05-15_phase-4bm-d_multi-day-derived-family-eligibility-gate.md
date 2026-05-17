# Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate

**Phase identity:** Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate.
**Type:** docs-and-code Tier 1 implementation phase (multi-day analogue of Phase 4bf).
**Date:** 2026-05-15.
**Branch:** `phase-4bm-d/multi-day-derived-family-eligibility-gate`.
**Status:** branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Phase identity

Phase 4bm-D implements the offline multi-day derived-family eligibility gate that read-only inspects the Phase 4bm-B v002 derived family (`dataset_family = microstructure_normalized_aggtrades_v001`, `dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events) and emits a single signed gate report under the canonical `data/microstructure/gate-reports/normalized/` namespace. Phase 4bm-D is the multi-day analogue of the Phase 4bf single-day derived-family eligibility gate, transposed forward to the v002 multi-day inventory and extended with a multi-day three-state verdict (`DERIVED_GATE_PASS` / `DERIVED_GATE_FAIL` / `DERIVED_GATE_INCOMPLETE`).

Phase 4bm-D is **branch-complete only**. Per the Phase 4bk-A workflow standard it is not project-complete until a separately authorized merge phase records its merge-closeout on `main`.

---

## 2. Branch and base SHA

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bm-d/multi-day-derived-family-eligibility-gate` |
| `main` HEAD before Phase 4bm-D branch | `d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (Phase 4bm-C merge-closeout commit) |
| Predecessor on `main` | Phase 4bm-C (Multi-Day Normalized Structural QA Memo, project-complete) |

---

## 3. Implementation commit SHA

| Item | SHA |
| ---- | --- |
| Phase 4bm-D implementation commit | `57e1c97e6e938797d448b331cdc27b50b8e935dd` |
| Commit message | `feat(phase-4bm-d): implement multi-day derived eligibility gate` |
| Files changed | 11 (`+6,786` insertions; `−0` deletions) |

A separate docs commit (this report + the closeout + a narrow `current-project-state.md` update) is appended on the same branch.

---

## 4. Files changed by the implementation commit

Tracked files added (10):

- `src/prometheus/research/microstructure/multiday_derived_gate.py` — orchestrator + frozen input/result types + boundary-confirmation builder.
- `src/prometheus/research/microstructure/multiday_derived_gate_io.py` — streaming SHA / manifest read / atomic JSON write / canonical sidecar write / path-discipline helpers / per-file path resolver.
- `src/prometheus/research/microstructure/multiday_derived_gate_checks.py` — 60-check suite, `CHECK_ORDER` tuple, locked constants (`EXPECTED_*_SHA`, `EXPECTED_GATE_REPORT_ID`, `EXPECTED_TOTAL_EVENT_COUNT = 155,153,449`, `EXPECTED_DATE_COUNT = 90`, `CANONICAL_DATE_START = "2024-12-01"`, `CANONICAL_DATE_END = "2025-02-28"`, Phase 4bm-C documentation-dependency paths, `_PASS_28_RE` 28-question regex), required-field tuples, forbidden-column-token list, sample-date predeclared tuple, normalized schema constant.
- `src/prometheus/research/microstructure/multiday_derived_gate_report.py` — frozen report data model + builder + writer enforcing the two hard safety invariants and the three-state verdict whitelist.
- `tests/research/microstructure/_multiday_derived_gate_fixtures.py` — canonical PASS-shape fixture builders.
- `tests/research/microstructure/test_multiday_derived_gate_checks.py` — per-check PASS / FAIL unit tests.
- `tests/research/microstructure/test_multiday_derived_gate_io.py` — I/O primitive tests.
- `tests/research/microstructure/test_multiday_derived_gate_report.py` — report data-model + writer-refuse-invariant tests.
- `tests/research/microstructure/test_multiday_derived_gate.py` — orchestrator end-to-end tests (12 tests; parser-format `per_file_inventory` keys throughout).
- `tests/research/microstructure/test_multiday_derived_gate_no_network.py` — static no-network / no-credential / `.env` / `dotenv` scan over the four gate modules.

Tracked files modified narrowly (1):

- `src/prometheus/research/microstructure/__init__.py` — added narrow re-exports for the new public surface of the four `multiday_derived_gate*` modules.

No other tracked file modified by the implementation commit.

---

## 5. Purpose and scope of the 60-check multi-day derived-family eligibility gate

The Phase 4bm-D gate is the multi-day analogue of the Phase 4bf 55-check single-day derived-family eligibility gate, transposed forward for the v002 derived inventory (90 dates, 155,153,449 events). It implements 60 ordered checks (`4bm-d.13.1` .. `4bm-d.13.60`) grouped by concern:

- **Group A** — manifest / sidecar / per-file existence (checks 13.1, 13.2, 13.4, 13.5).
- **Group B** — manifest / per-file / raw-zip SHA matches (checks 13.3, 13.6, 13.20).
- **Group C** — manifest scalar conformance: `total_event_count = 155,153,449`, per-file size match, `dataset_family`, `dataset_version = v002`, `symbol_list = ["BTCUSDT"]`, governance-label `feature_computation = "forbidden"` / `strategy_use = "forbidden"` (checks 13.7, 13.9, 13.10–13.16).
- **Group E** — per-file Parquet num-rows vs inventory event_count plus per-row content checks against the 5 predeclared sample dates: row-index `0..n-1` density, no duplicate `agg_trade_id`, monotone `agg_trade_id`, first-row / last-row alignment with inventory (checks 13.8, 13.25–13.30).
- **Group F** — governance lineage: derived manifest cites the Phase 4bl-D-R gate report id + SHA, the v002 raw manifest SHA, and per-row source lineage columns match (checks 13.17, 13.18, 13.19, 13.37).
- **Group G** — timestamp / UTC boundary: all `transact_time_ms` within `[UTC date, UTC date + 1)`, first / last per-file timestamp match inventory (checks 13.31, 13.32, 13.33).
- **Group H** — Arrow dtypes: `price` / `quantity` string Decimal, `is_buyer_maker` strict bool (checks 13.34, 13.35, 13.36).
- **Group K** — Phase 4bm-C documentation dependency: QA memo / closeout / merge-closeout file existence plus 28-question PASS phrase match (checks 13.38, 13.39, 13.40, 13.41).
- **Group L** — raw manifest / acquisition log / Phase 4bl-D-R gate report / Phase 4bl-E successor-state SHA matches (checks 13.42, 13.43, 13.44, 13.45, 13.46, 13.47, 13.48).
- **Group N** — static / structural invariants and no-network discipline (checks 13.49–13.55).
- **Group P** — multi-day envelope: required 34 top-level + 16 governance-label keys present; 90-date contiguous span; adjacent-date temporal monotonicity (89 pairs); adjacent-date `agg_trade_id` non-overlap (89 pairs); cross-totals consistency (checks 13.56, 13.57, 13.58, 13.59, 13.60).

The orchestrator never mutates the derived manifest, any of the 90 per-day Parquets, any sidecar, any raw zip, the raw manifest, the acquisition log, the Phase 4bl-D-R gate report, the Phase 4bl-E successor-state record, or any prior gate report. It only writes the new gate report JSON + paired `.sha256` sidecar under `data/microstructure/gate-reports/normalized/` (and only when `write_report=True`). Per-file row counts come from `pyarrow.parquet.ParquetFile.metadata.num_rows` without materialising row groups; full per-row content checks are bounded to the 5 predeclared `SAMPLE_DATES`; SHA hashing is streamed in 1 MiB chunks. The dataset (~1.4 GiB / ~155 M events) is never loaded fully into memory.

---

## 6. Validation summary

| Tool | Scope | Result |
| ---- | ----- | ------ |
| `ruff check` | 10 Phase 4bm-D source/test files | **PASS** (`All checks passed!`) after minimal in-scope test cleanups (one B007 dead-loop removal in `test_multiday_derived_gate.py`; auto-fixed I001 import order + 3× F401 unused imports + 2× SIM300 Yoda + 2× manual F841 unused-`d`-assignment removals across `test_multiday_derived_gate_checks.py` and `test_multiday_derived_gate_report.py`; the two surgical F841 removals are no-op deletions of dead `d = _PASS_DATES[0]` lines) |
| `mypy --strict` | `src/prometheus` | **PASS** — `Success: no issues found in 124 source files` |
| `pytest` (targeted) | 5 Phase 4bm-D test files | **218 passed in 2.51 s** (60 per-check tests + 12 orchestrator E2E tests + 9 no-network parametrized tests + I/O primitive tests + report-data-model + writer-refuse-invariant tests) |
| `pytest` (orchestrator only) | `test_multiday_derived_gate.py` | **12 passed in 1.76 s** |
| `pytest` (no-network only) | `test_multiday_derived_gate_no_network.py` | **9 passed in 0.06 s** |

Whole-repo `pytest` was not rerun in this implementation phase; the latest authoritative whole-repo baseline remains the Phase 4bm-B merge baseline (`1156 passed, 1 skipped`; the pre-existing 2 simulation failures on `test_backtest_real_2026_03.py` `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232` are unrelated to Phase 4bm-D and are preserved as the baseline; Phase 4bm-D introduces zero new regressions vs that baseline).

---

## 7. Preliminary pre-commit sanity gate result (NON-AUTHORITATIVE)

A preliminary read-only gate run was executed **before** the implementation commit, with `code_commit_sha = d39ffd8aa1fedf3a191f0c8b1a5268f431456fb3` (the predecessor `main` HEAD; the Phase 4bm-D implementation was still uncommitted in the working tree). This run is **a pre-commit sanity PASS witness, not authoritative evidence**.

| Item | Value |
| ---- | ----- |
| Report path | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779055831936__d39ffd8aa1fe.json` |
| Report SHA256 | `ffde54bb7dd96f9df3269915271238b3e3f463fee6af6ce845e95d8713651764` |
| Sidecar SHA256 | `11c952519e16a967f1a916273bff3d64381fe8fa2e2851379b47f4f5a930e99d` |
| Overall status | `pass` |
| Gate verdict | `DERIVED_GATE_PASS` |
| Checks total / PASS / FAIL / ERROR / NA | 60 / 60 / 0 / 0 / 0 |
| `code_commit_sha` recorded | `d39ffd8…` (predecessor `main` HEAD; uncommitted Phase 4bm-D implementation in working tree) |

The preliminary report file remains on disk as a non-authoritative continuity witness; it is not deleted, moved, or renamed by Phase 4bm-D. It is gitignored under `.gitignore:85` and is not committed.

---

## 8. Authoritative post-commit gate result (AUTHORITATIVE EVIDENCE)

After the implementation commit, the gate was rerun once read-only against the same real artefacts with the post-commit SHA recorded as `code_commit_sha`.

| Item | Value |
| ---- | ----- |
| Report path | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` |
| Report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Sidecar path | same path with `.json.sha256` suffix |
| Sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| Sidecar body format | canonical Phase 4bb-F `<sha256_lowercase_hex>  <basename>\n` (two ASCII spaces; trailing LF) |
| Overall status | `pass` |
| Gate verdict | `DERIVED_GATE_PASS` |
| Checks total | 60 |
| Checks PASS | **60** |
| Checks FAIL | 0 |
| Checks ERROR | 0 |
| Checks NOT_APPLICABLE | 0 |
| `research_eligible_after` | `False` (hard invariant) |
| `no_successor_authorization` | `True` (hard invariant) |
| `eligibility_gate_status_after` | `"pass"` (report-level recommendation only; on-disk manifest unchanged) |
| Report id | `microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93` |
| `code_commit_sha` recorded | `57e1c97e6e938797d448b331cdc27b50b8e935dd` (Phase 4bm-D implementation commit) |

Both new files are gitignored under `.gitignore:85: data/microstructure/`; `git check-ignore -v` confirms each path.

Recomputed post-write hashes (via `Get-FileHash … -Algorithm SHA256`) confirm both the report and sidecar SHA256 values byte-identical to the post-write recorded values above.

---

## 9. `4bm-d.13.40` result

**PASS.** Check `4bm-d.13.40` ("Phase 4bm-C merge-closeout file exists") located `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-c_merge-closeout.md` on disk and returned PASS. The stale assumption recorded in the in-progress bounded-session checkpoint (which speculated that 4bm-d.13.40 would FAIL because the Phase 4bm-C merge-closeout file was missing) is **corrected** by this run: the operator-verified state showed the file is present, and the live gate run confirmed the file is present and located by check `4bm-d.13.40`. No source / docs change is needed to address that stale assumption; the corrected expectation simply matches the on-disk reality.

---

## 10. Boundary confirmations

All **19 boundary confirmation keys** returned **`True`** on the authoritative run:

| Key | Value |
| --- | ----- |
| `no_manifest_mutation` | `True` |
| `no_per_file_parquet_mutation` | `True` |
| `no_per_file_sidecar_mutation` | `True` |
| `no_raw_zip_mutation` | `True` |
| `no_normalization_written_outside_namespace` | `True` |
| `no_data_microstructure_write_outside_gate_reports` | `True` |
| `no_feature_computed` | `True` |
| `no_label_computed` | `True` |
| `no_signal_computed` | `True` |
| `no_ml_trained` | `True` |
| `no_strategy_created` | `True` |
| `no_backtest_run` | `True` |
| `no_network_io` | `True` |
| `no_websocket` | `True` |
| `no_credential_read` | `True` |
| `no_env_read` | `True` |
| `no_mcp_or_graphify` | `True` |
| `research_eligible_after_is_false_for_derived_family` | `True` |
| `no_successor_authorization` | `True` |

The four mutation-class confirmations (`no_manifest_mutation`, `no_per_file_parquet_mutation`, `no_per_file_sidecar_mutation`, `no_raw_zip_mutation`) are computed by re-hashing every governance artefact + every per-file Parquet + every sidecar + every raw zip post-checks and comparing each value byte-identically against the pre-check SHA. All matched. The remaining 13 confirmations are static / source-level invariants and report-level hard invariants; the no-network static scan (`test_multiday_derived_gate_no_network.py`) source-level enforces the network / credentials / `.env` / `dotenv` / MCP-related ones.

---

## 11. Hard invariants

| Invariant | Result |
| --------- | ------ |
| `research_eligible_after` | `False` (set unconditionally by the orchestrator; the writer in `multiday_derived_gate_report.py` raises `GateIOError` if any caller attempts to serialise a report with this `True`) |
| `no_successor_authorization` | `True` (set unconditionally; the writer raises `GateIOError` if `False`) |
| `eligibility_gate_status_after` | `"pass"` — report-level recommendation only. **No on-disk manifest mutation occurs.** The v002 derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` continues to read `research_eligible = false` / `eligibility_gate_status = "pending"` byte-for-byte before and after the gate run; the post-check re-hash confirms `no_manifest_mutation = True`. |
| Phase 4aw `flip_research_eligible(...)` always-raises invariant | preserved end-to-end (never invoked; the v002 multi-day index manifest is a sibling shape and does not use the single-file `MicrostructureManifest` data class) |

---

## 12. Local output inventory

All listed files live under the gitignored `data/microstructure/gate-reports/normalized/` namespace (`.gitignore:85`) and are not committed.

**Authoritative (Phase 4bm-D evidence):**

| Path | SHA256 |
| ---- | ------ |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256` | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |

**Preliminary pre-commit sanity (NON-AUTHORITATIVE; retained as continuity witness):**

| Path | SHA256 |
| ---- | ------ |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779055831936__d39ffd8aa1fe.json` | `ffde54bb7dd96f9df3269915271238b3e3f463fee6af6ce845e95d8713651764` |
| `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779055831936__d39ffd8aa1fe.json.sha256` | `11c952519e16a967f1a916273bff3d64381fe8fa2e2851379b47f4f5a930e99d` |

The pre-existing Phase 4bf v001 single-day gate report (different dataset version, recorded in Phase 4bf) at `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` is byte-identical pre/post Phase 4bm-D and is not modified.

---

## 13. Gitignored data policy

All `data/microstructure/` outputs (the v002 derived manifest, the 90 per-day Parquets, the 90 sidecars, the v002 raw zips, the raw manifest, the acquisition log, the Phase 4bl-D-R gate report, the Phase 4bl-E successor-state record, the new Phase 4bm-D report + sidecar, and the preliminary pre-commit report + sidecar) are **local and gitignored** under `.gitignore:85: data/microstructure/`. **No `data/microstructure/` artefact is staged or committed by this branch.** The two commits on the branch (`feat` + `docs`) only touch tracked source / test / docs files.

---

## 14. No successor authorization

Phase 4bm-D does **not** authorize:

- Phase 4bm-D merge phase;
- Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo);
- Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording);
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*;
- Phase 5 / Phase 4 canonical;
- paper / shadow / live-readiness / deployment / exchange-write;
- production-key creation / authenticated APIs / private endpoints;
- user stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any additional acquisition beyond the 90 locked BTCUSDT UTC dates;
- any modification of `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` on any actual manifest;
- feature computation, label computation, signal computation, proxy computation, ML training, model selection, feature ranking, meta-labeling, strategy creation, or backtest execution.

---

## 15. Recommended state

**Branch-complete after this docs/closeout commit. Not project-complete. Remain paused.**

**Conditional next, NOT authorized:**

- future operator-authorized Phase 4bm-D merge phase that merges this branch into `main` and records a Phase 4bm-D merge-closeout per `docs/00-meta/process/merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout);
- after merge, conditional Phase 4bm-E (Multi-Day Derived-Family Research-Eligibility Decision Memo) and downstream Phase 4bm-F (Multi-Day Derived-Family Successor-State Recording), neither authorized by Phase 4bm-D.

The Phase 4bm-D `DERIVED_GATE_PASS` is a **report-level Stage-2 verdict for the v002 derived family**. It does not transition the derived manifest, does not flip `research_eligible`, does not transition `eligibility_gate_status` on the on-disk manifest, and does not license edge claims, feature computation, label computation, ML, strategy work, or backtests.

---

## 16. Retained verdict ledger and project locks preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec; §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked); Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule (cited; not invoked — the Phase 4bm-D writer emits canonical LF natively); Phase 4am .. Phase 4bm-C results — all preserved verbatim.

— end of Phase 4bm-D implementation report —