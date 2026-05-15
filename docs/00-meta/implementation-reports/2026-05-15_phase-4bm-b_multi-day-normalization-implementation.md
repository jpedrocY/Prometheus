# Phase 4bm-B — Multi-Day Normalization Implementation

**Phase identity:** Phase 4bm-B — Multi-Day Normalization Implementation.
**Type:** docs-and-code Tier 1 implementation phase (per Phase 4bl-F risk-tiering standard).
**Date:** 2026-05-15.
**Branch:** `phase-4bm-b/multi-day-normalization-implementation`.
**Status:** branch-complete; not merged into `main`; not project-complete.

---

## 1. Phase header

Phase 4bm-B operationalises the Phase 4bm-A locked design memo by implementing an offline orchestrator that normalises the v002 multi-day BTCUSDT aggTrades raw archive (90 contiguous UTC dates 2024-12-01 through 2025-02-28; 155,153,449 events; 1,943,823,208 bytes) acquired by Phase 4bl-C and admitted by the Phase 4bl-D-R PASS gate report and the Phase 4bl-E Stage-2 raw successor-state, into a future normalized derived dataset family with identity:

- `dataset_family = microstructure_normalized_aggtrades_v001` (reused; schema byte-identical to Phase 4bd);
- `dataset_version = v002` (new; bounded source-dataset discriminator);
- `schema_version = v001` (unchanged).

Phase 4bm-B does **not**:

- mutate any source raw artefact (v002 raw manifest, v002 raw manifest sidecar, v002 acquisition log, v002 acquisition log sidecar, any of the 90 v002 raw zips, any of the 90 v002 raw zip sidecars, Phase 4bl-D-R PASS gate report, Phase 4bl-D-R gate report sidecar, Phase 4bl-E successor-state, Phase 4bl-E successor-state sidecar) — verified bit-for-bit by pre/post SHA256 capture across **188 immutability witnesses** (4 governance artefacts + 4 governance sidecars + 90 raw zips + 90 raw zip sidecars);
- mutate the Phase 4bd v001 derived parquet, the Phase 4bd v001 derived manifest, the Phase 4bf v001 derived gate report, the Phase 4bg-B v001 successor-state, the Phase 4bh feature parquet, the Phase 4bj-C label parquet, or any other prior derived artefact;
- flip `research_eligible` to `True` on any raw, derived, feature, or label family — the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains intact; the new multi-day index manifest is a sibling shape (mirroring the Phase 4bl-C raw v002 manifest layout) and does NOT use the single-file `MicrostructureManifest` data class; it carries `research_eligible=False` and `eligibility_gate_status="pending"` as locked values;
- compute features, labels, signals, proxies, or strategy artefacts;
- contact any Binance endpoint, public endpoint, or private endpoint;
- open any WebSocket;
- use any credential, `.env`, `.mcp.json`, MCP, or Graphify;
- authorize Phase 4bm-C / 4bm-D / 4bm-E / 4bm-F or any successor.

Stage-0 (artefacts present; eligibility pending) is reached for the v002 derived family. The Phase 4ba 5-stage eligibility ladder requires separately authorized future phases for Stage-1 / 2 / 3 / 4.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD before Phase 4bm-B branch | `56f96a4c613a3d8c8794905be4c1847fcdac5e58` (Phase 4bm-A-P1 merge-closeout) |
| Phase 4bm-A merge commit (predecessor multi-day-normalization design memo) | `af97285` (merged earlier; intermediate ancestor) |
| Phase 4bm-A-P1 merge commit (most recent predecessor) | `e00e178` (Claude Code Context Management standard) |
| Phase 4bm-B branch | `phase-4bm-b/multi-day-normalization-implementation` |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| pyarrow available in venv | yes |
| Phase 4bd v001 derived family on disk | preserved verbatim; 2025-01-15 parquet SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` re-verified post-run |

---

## 3. Inputs

Cited verbatim from the v002 raw acquisition arc:

- **Phase 4bl-A** — Multi-Day aggTrades Expansion Requirements Memo.
- **Phase 4bl-B** — Multi-Day aggTrades Acquisition Authorization / Design Memo.
- **Phase 4bl-C** — Multi-Day aggTrades Acquisition Execution (SUCCESSFUL_ACQUISITION; 90 dates × 1 symbol = 90 zips; 155,153,449 events).
- **Phase 4bl-D** — Multi-Day Raw Manifest Eligibility Gate (initial FAIL, root cause = single Phase 4az 2025-01-15 sidecar CRLF terminator).
- **Phase 4bl-D-S1** — Sidecar Canonicalization Governance Memo (governance lane for CRLF→LF remediation).
- **Phase 4bl-D-S2** — Controlled Sidecar Canonicalization Execution.
- **Phase 4bl-D-R** — Multi-Day Raw Manifest Eligibility Gate Rerun (PASS, 33/33).
- **Phase 4bl-E** — Multi-Day Raw Manifest Successor-State Recording (Stage-2 admissible).
- **Phase 4bl-F** — Phase Risk-Tiering and Controlled Remediation Standard.
- **Phase 4bm-A** — Multi-Day Normalization Design Memo (Tier 1 locked design).

Locked precondition SHAs (Phase 4bm-A §4 / §12.1 criteria 1-9):

| Artefact | SHA256 |
| -------- | ------ |
| `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| same path with `.sha256` suffix | `adaf97242cfbe922bc9e93a6699e547d1b02fa64a96dd2cdd08df1814ce25e26` |
| `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| same path with `.sha256` suffix | `975bdc544152d1f84f6e700309aad89998e663cb779acc5883bd20652e428958` |
| `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| same path with `.sha256` suffix | `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02` |
| `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| same path with `.sha256` suffix | `63d97bf54e1063f2fd70024d40639db711e9c24d929074cdd63b2db385302b4f` |

Project locks honoured verbatim: §11.6 = 8 bps per side; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

Implement the offline multi-day normalizer exactly per Phase 4bm-A:

- 1 new standalone orchestrator script under `scripts/`;
- 1 new test file under `tests/research/microstructure/`;
- run the orchestrator **exactly once** against the v002 raw artefacts, producing 90 per-day Parquet files + 90 paired canonical Phase 4bb-F sidecars + 1 multi-day index manifest + 1 manifest sidecar — all under the gitignored `data/microstructure/` namespace.

---

## 5. Non-scope

Phase 4bm-B did **not**:

- modify any prior `src/prometheus/` source module (the orchestrator reuses the Phase 4bd primitives in `src/prometheus/research/microstructure/normalize_aggtrades.py` and `normalize_io.py` unchanged);
- modify any prior test;
- modify any prior governance memo beyond the narrow `current-project-state.md` paragraph addition + the new Phase 4bm-B memo + closeout files;
- modify `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or any MCP file;
- modify any data/microstructure/ artefact other than producing the new v002 derived outputs;
- modify the Phase 4az single-day raw manifest, raw zip, sidecars, or acquisition log;
- modify the Phase 4bd v001 single-day derived parquet or its sidecar — the legitimate 2025-01-15 v001 file at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` (SHA `2b3d69787d93...808f6fa`) remains byte-identical;
- modify the Phase 4bb-D / 4bf / 4bg-B / 4bh / 4bi-B / 4bi-D / 4bj-C / 4bj-E / 4bj-G derived / feature / label / gate / successor-state artefacts;
- modify the Phase 4bb-G raw successor-state artefact;
- modify the Phase 4bl-C / 4bl-D / 4bl-D-R / 4bl-E v002 artefacts;
- run features, labels, ML, strategies, backtests, simulations, paper / shadow, or live;
- enable MCP, Graphify, `.mcp.json`, credentials, exchange-write, authenticated APIs, private endpoints, public-endpoint code calls, user stream, WebSocket, or any data acquisition (5m / 1m / aggTrades / tick / mark-price / order-book / spot / cross-venue);
- authorize Phase 4bm-C / Phase 4bm-D / Phase 4bm-E / Phase 4bm-F / Phase 4bn-* / Phase 4 canonical / Phase 5 / paper / shadow / live-readiness / deployment / production keys.

---

## 6. Phase 4bm-A design dependencies honoured

Phase 4bm-B honours the Phase 4bm-A locked design verbatim:

- §4 — eight precondition SHAs encoded as module-level constants (`EXPECTED_SOURCE_MANIFEST_SHA`, `EXPECTED_SOURCE_MANIFEST_SIDECAR_SHA`, `EXPECTED_ACQUISITION_LOG_SHA`, `EXPECTED_ACQUISITION_LOG_SIDECAR_SHA`, `EXPECTED_GATE_REPORT_SHA`, `EXPECTED_GATE_REPORT_SIDECAR_SHA`, `EXPECTED_SUCCESSOR_STATE_SHA`, `EXPECTED_SUCCESSOR_STATE_SIDECAR_SHA`) — verified pre-run by `verify_preconditions`;
- §5 — 90-date `date_list` ordering, length, and `date_start`/`date_end` boundary checks;
- §6 — Phase 4bc 19-column `NORMALIZED_SCHEMA_V001` schema reused verbatim by importing from `prometheus.research.microstructure.normalize_aggtrades`; Decimal-as-string price/quantity, `int64` IDs and timestamps, strict `bool` `is_buyer_maker`;
- §7 — per-day Parquet partition layout (implementation-level deviation from literal directory naming; see §8 below);
- §8 — multi-day index manifest schema (sibling layout mirroring Phase 4bl-C raw v002 manifest; 16-key `governance_labels` block; `research_eligible: false`; `eligibility_gate_status: pending`; `invalid_windows: []`; `per_file_inventory[]` 90 entries; `expected_file_count: 90`; `produced_file_count`; `total_event_count`);
- §9 — `phase_4bm_b_no_successor_authorization` invariant exposed in `governance_labels`;
- §10 — forbidden inputs (no mark-price, no aggTrades-other, no spot, no cross-venue, no order-book, no metrics OI, no optional metrics ratio columns, no 5m, no 1m, no tick, no funding directional trigger) — enforced by the orchestrator's standard-library-only import surface;
- §11 — forbidden outputs (no features, labels, signals, proxies, regression / classification / boundary outputs; no ML; no strategy; no backtests; no paper / shadow / live) — enforced by the 26-substring forbidden-column scan applied to every column in `NORMALIZED_SCHEMA_V001` at write time;
- §12 — 65-criterion strict-fail-closed validation contract (6 groups: precondition / per-day / aggregate / immutability / governance / quality-gate);
- §13 — atomic write-then-rename via `tempfile.mkstemp` + `os.replace`; refuse-overwrite at writer level; paired SHA256 sidecar in canonical Phase 4bb-F format `<sha256_lowercase_hex>  <basename>\n` (two ASCII spaces; single trailing LF);
- §14 — Phase 4ax `validate_aggtrade_payload` for per-row validation, applied via the Phase 4bd `iter_aggtrade_rows_from_csv` iterator;
- §16 — orchestrator architecture (precondition → per-day production → aggregate consistency → immutability witness check → governance / boundary check → atomic manifest write);
- §18 — gitignore discipline: every output path under `data/microstructure/` is covered by `.gitignore:85`; no artefact under `data/microstructure/` is committed.

---

## 7. Implementation summary

### 7.1 Source

| File | Purpose | Lines |
| ---- | ------- | ----- |
| `scripts/phase4bm_b_normalize_multiday_aggtrades.py` | Standalone offline orchestrator. Reads v002 raw manifest + gate report + successor-state read-only; loads each of the 90 raw zips read-only; iterates rows via Phase 4bd `iter_aggtrade_rows_from_csv` and per-row `validate_aggtrade_payload`; constructs the 19-column pyarrow table for each day; writes per-day Parquet + paired sidecar atomically; builds and writes the multi-day index manifest + paired sidecar. Implements the 65-criterion validation contract end-to-end. | ~1,620 |

The orchestrator imports only:

- Python standard library (`hashlib`, `json`, `argparse`, `zipfile`, `csv`, `io`, `os`, `contextlib`, `tempfile`, `re`, `sys`, `time`, `datetime`, `dataclasses`, `collections.abc`, `pathlib`, `typing`);
- `pyarrow` (Apache 2.0; already a project dependency);
- Phase 4ax / 4bd microstructure primitives from `prometheus.research.microstructure.normalize_aggtrades` and `prometheus.research.microstructure.normalize_io`.

The orchestrator does **not** import `requests`, `httpx`, `aiohttp`, `urllib`, `urllib3`, `socket`, `websockets`, `binance`, or `dotenv`. Static no-network and no-credential scans are enforced by tests.

### 7.2 Tests

| File | Purpose | Tests |
| ---- | ------- | ----- |
| `tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` | 33 tests across 9 sections: locked identity constants (11); expected SHA constants (5); schema discipline (4); pure helpers (3); `normalize_one_date` happy path (2); `normalize_one_date` fail-closed paths (5); `build_multiday_manifest` shape (1); CLI surface (1); static no-network / credentials scan (2). | 33 |

All tests use pytest `tmp_path` fixtures rooted at `tmp_path / "data" / "microstructure"` to satisfy the path-discipline guard, plus synthetic raw zips built by `_build_synthetic_inventory_and_zip(...)` to exercise `normalize_one_date` without touching real data.

### 7.3 Phase 4bd primitives reused verbatim

- `NORMALIZED_SCHEMA_V001` — 19-column schema tuple.
- `NORMALIZATION_SCHEMA_VERSION` — `"v001"`.
- `iter_aggtrade_rows_from_csv` — CSV-zip row iterator.
- `atomic_write_parquet` — atomic Parquet write + SHA256.
- `write_sha256_sidecar` — canonical Phase 4bb-F sidecar writer.
- `compute_bytes_sha256` — in-memory SHA256.
- `assert_path_under_microstructure` — path discipline guard.
- `assert_manifest_path_under_manifests` — manifest path discipline guard.
- `NormalizationIOError` — fail-closed I/O exception type.

No Phase 4bd primitive was modified.

---

## 8. Path-layout implementation decision (design-memo clarification)

The Phase 4bm-A design memo §7 specifies that the v002 derived family writes parquets at:

```text
data/microstructure/normalized/
  microstructure_normalized_aggtrades_v001/
    BTCUSDT/<YYYY>/<MM>/
      BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet
```

The same memo §7 further specifies that:

> "The Phase 4bd 2025-01-15 single-day v001 normalized parquet is **not modified, not moved, not renamed, not deleted, not consumed** by Phase 4bm-B. The v001 normalized family remains exactly as it is on the operator's local machine (SHA `2b3d69787d93...808f6fa`, under `microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/`). The v002 normalized family writes a parallel parquet for the same date — `BTCUSDT-aggTrades-2025-01-15.parquet` under the same family / same path tree but with `dataset_version="v002"` recorded inside the parquet's per-row constants and inside the v002 manifest."

These two requirements are internally inconsistent on the literal level: two parquet files with the same absolute path cannot coexist on a single filesystem. The memo's substantive intent (parallel files; coexistence; v001 byte-identical) is unambiguous; the literal path layout is unrealizable.

**Decision (Phase 4bm-B implementation-level):** the v002 family-directory segment is version-suffixed to `microstructure_normalized_aggtrades_v001__v002`. Final v002 layout:

```text
data/microstructure/normalized/
  microstructure_normalized_aggtrades_v001/         (untouched; Phase 4bd v001)
    BTCUSDT/2025/01/
      BTCUSDT-aggTrades-2025-01-15.parquet          (Phase 4bd v001; SHA 2b3d6978...)
      BTCUSDT-aggTrades-2025-01-15.parquet.sha256
  microstructure_normalized_aggtrades_v001__v002/   (new; Phase 4bm-B v002)
    BTCUSDT/2024/12/...
    BTCUSDT/2025/01/...
    BTCUSDT/2025/02/...
```

This mirrors the existing manifest filename convention `microstructure_normalized_aggtrades_v001__<version>.json` already used by Phase 4bd (for v001) and Phase 4bm-A (for the v002 multi-day index manifest). Both Phase 4bd's `__v001` manifest filename and the new family-directory suffix `__v002` use the same `__<dataset_version>` discriminator pattern.

The `assert_path_under_microstructure` helper imported from `normalize_io.py` enforces the `data/microstructure/normalized/` prefix only and does not constrain the next segment, so the suffixed family directory satisfies path discipline verbatim.

**Per-row content invariants from Phase 4bm-A §7 are honoured:**

- column 2 `dataset_version` records `"v002"` for the v002 parquet;
- column 4 `source_dataset_version` records `"v002"`;
- column 14 `source_file_sha256` cites the same raw zip SHA as Phase 4bd for 2025-01-15;
- column 15 `source_manifest_sha256` cites the v002 raw manifest SHA `016967865c97...d87485`;
- column 16 `source_gate_report_id` cites the Phase 4bl-D-R PASS gate report `microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080`;
- column 17 `source_gate_report_sha256` cites the Phase 4bl-D-R gate report SHA `f9493fd10d1c...6f1c46`;
- column 18 `row_index` is the canonical `0..N-1` sequence for that day;
- column 19 `normalization_schema_version` is `"v001"` (unchanged across both v001 and v002 files).

This is the only deviation from a literal reading of the Phase 4bm-A design memo. The deviation is design-memo-clarifying (not design-memo-amending): it does not change schema, governance, immutability, validation, output count, or coexistence intent.

---

## 9. Real-run result

The orchestrator was run **exactly once** against the real v002 raw artefacts:

```text
python -X utf8 scripts/phase4bm_b_normalize_multiday_aggtrades.py
```

Result:

- **Overall status:** `pass`
- **Produced file count:** 90 (matches expected exactly)
- **Total event count:** 155,153,449 (matches v002 raw manifest `total_row_count` exactly)
- **Wall-clock seconds:** 1460.5 (~24.3 minutes)
- **Multi-day index manifest:** `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (104,094 bytes; SHA256 `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a`)
- **Multi-day index manifest sidecar:** same path with `.sha256` suffix (118 bytes; SHA256 `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888`; canonical body `01c5fa53…554a  microstructure_normalized_aggtrades_v001__v002.json` with two ASCII spaces and trailing LF)
- **Per-day parquet output root:** `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/{2024/12,2025/01,2025/02}/`

### 9.1 65-criterion validation contract result

| Group | Checks | PASS | FAIL | NOT_APPLICABLE | ERROR |
| ----- | ------ | ---- | ---- | -------------- | ----- |
| Group 1: Precondition (criteria 1-10) | 10 | 10 | 0 | 0 | 0 |
| Group 2: Per-day (criteria 11-31 ×90 dates) | 90 dates × 21 = 1,890 effective; aggregated as one PASS check | 1 | 0 | 0 | 0 |
| Group 3: Aggregate (criteria 32-39) | 8 | 8 | 0 | 0 | 0 |
| Group 4: Lineage / immutability (criteria 40-51) | 12 (collapsed; verifies 188 witnesses) | 12 | 0 | 0 | 0 |
| Group 5: Governance / boundary (criteria 52-57) | 6 | 6 | 0 | 0 | 0 |
| Group 6: Quality-gate (criteria 58-65) | 8 | 8 | 0 | 0 | 0 |

**All 65 criteria PASS. No FAIL / NOT_APPLICABLE / ERROR. Manifest written. Sidecar written. Per-day parquet inventory recorded in manifest's `per_file_inventory` (90 entries; first date 2024-12-01 with 731,065 events; last date 2025-02-28 with 4,526,219 events).**

The orchestrator collapses certain repeated criteria into a single check when the underlying assertion is run identically across the iteration (per-day criteria 11-31 verified per-day, then summarised; immutability criteria 40-51 collapsed into a single all-witnesses-verified check after pre/post SHA comparison across all 188 artefacts).

### 9.2 Per-day production summary

90 produced records, one per UTC date 2024-12-01 through 2025-02-28. Each record carries:

- `date` (UTC date string),
- `symbol` (`BTCUSDT`),
- `local_parquet_path` (relative to repo root),
- `local_sidecar_path` (relative to repo root),
- `parquet_sha256` (Parquet file SHA256),
- `sidecar_sha256` (sidecar file SHA256),
- `parquet_size_bytes`, `sidecar_size_bytes`,
- `event_count` (rows in this date's Parquet),
- `first_transact_time_ms`, `last_transact_time_ms`,
- `min_agg_trade_id`, `max_agg_trade_id`,
- `source_file_sha256` (the v002 raw zip SHA cited per row),
- `source_zip_path` (relative to `data/microstructure/`),
- `status = produced_verified`.

Headline aggregate (post-run):

- `produced_file_count` = 90,
- `total_event_count` = 155,153,449 (matches v002 raw manifest's `total_row_count` exactly),
- per-day event counts match the v002 raw manifest's `per_file_inventory[i].row_count` exactly,
- per-day `first_transact_time_ms` / `last_transact_time_ms` fall inside the UTC-half-open day-window `[date_start_ms, date_start_ms + 86_400_000)`,
- adjacent-date overlap check passes for all 89 (date, next-date) pairs (each day's `last_transact_time_ms` is strictly less than next day's `first_transact_time_ms`).

---

## 10. Pre/post immutability evidence (188 witnesses)

The orchestrator captures pre-run SHA256 for **188 immutability witnesses** before any output write and re-captures post-run SHA256 after all outputs are committed:

- 4 governance artefacts (v002 raw manifest, v002 acquisition log, Phase 4bl-D-R gate report, Phase 4bl-E successor-state);
- 4 governance sidecars (paired `.sha256` for each of the above);
- 90 v002 raw zips;
- 90 v002 raw zip sidecars.

Every witness is verified byte-identical pre/post. Any drift fails closed (criteria 40-51).

Additionally, the Phase 4bd v001 single-day parquet at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` was re-verified post-cleanup to be byte-identical to the recorded Phase 4bd SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`.

---

## 11. Manifest state preservation

| Manifest | `research_eligible` | `eligibility_gate_status` | Note |
| -------- | ------------------- | -------------------------- | ---- |
| `microstructure_raw_aggtrades_v002` (v002 raw) | `false` | `pending` | unchanged from Phase 4bl-C |
| `microstructure_normalized_aggtrades_v001` v001 (Phase 4bd) | `false` | `pending` | unchanged from Phase 4bd |
| `microstructure_normalized_aggtrades_v001` v002 (NEW, Phase 4bm-B) | `false` | `pending` | locked at Stage-0 |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end: the new multi-day index manifest is a sibling shape and does NOT use the single-file `MicrostructureManifest` data class. No call to `flip_research_eligible(...)` occurs anywhere in Phase 4bm-B code or tests.

---

## 12. Validation evidence

| Command | Result |
| ------- | ------ |
| `ruff check scripts/phase4bm_b_normalize_multiday_aggtrades.py tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` | PASS (`All checks passed!`) |
| `mypy scripts/phase4bm_b_normalize_multiday_aggtrades.py` | PASS (`Success: no issues found`) |
| `pytest tests/research/microstructure/test_phase4bm_b_multiday_normalization.py -q` | `33 passed` |
| `pytest tests/research/microstructure/ -q` | `1156 passed, 1 skipped in 12.64s` (zero regressions; includes the 33 new Phase 4bm-B tests; the 1 skip is a pre-existing labelled placeholder in `test_label_gate_report.py`) |
| `git diff --check` | clean |
| `git check-ignore -v data/microstructure/` | `.gitignore:85` |
| `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` | covered by `.gitignore:85` |

---

## 13. Boundary confirmations

All true at the close of Phase 4bm-B:

- no_data_microstructure_commit;
- no_modification_of_phase_4az_artefacts;
- no_modification_of_phase_4bd_artefacts;
- no_modification_of_phase_4bb_d_gate_report;
- no_modification_of_phase_4bf_gate_report;
- no_modification_of_phase_4bg_b_successor_state;
- no_modification_of_phase_4bh_feature_parquet;
- no_modification_of_phase_4bj_c_label_parquet;
- no_modification_of_phase_4bl_c_v002_artefacts;
- no_modification_of_phase_4bl_d_r_gate_report;
- no_modification_of_phase_4bl_e_successor_state;
- no_features_labels_signals_ml_strategy_backtest_simulation_paper_shadow_live;
- no_data_acquisition;
- no_binance_endpoint_contact;
- no_websocket;
- no_credential_use;
- no_env_read;
- no_mcp_or_graphify;
- no_research_eligible_flip;
- no_eligibility_gate_status_transition_on_any_actual_manifest;
- no_chronological_split_policy_change_on_any_actual_manifest;
- no_retained_verdict_revision;
- no_project_lock_change;
- no_m0_amendment;
- no_successor_authorization;
- no_merge_into_main;
- phase_4aw_flip_research_eligible_always_raises_invariant_preserved.

---

## 14. Retained verdict ledger preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.

---

## 15. Preserved project locks (verbatim)

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule.

---

## 16. Forbidden-rescue / no-rescue statement

Phase 4bm-B is infrastructure (data normalization) only. It does not constitute or imply: any new strategy hypothesis; any retained-strategy promotion or rescue (R3-prime, R2-prime, F1-prime, D1-A-prime, V2-prime, G1-prime, C1-prime, R1a-prime, R1b-narrow-prime, H0-prime, V1-D1, F1-D1, or any cross-strategy hybrid); reopening of the 5m research thread; any change to retained verdicts or project locks; any M0 governance amendment; any feature / label / signal / ML / strategy / backtest authorization; any paper / shadow / live readiness implication; any data acquisition (beyond the already-acquired v002 raw zips, none of which is acquired by Phase 4bm-B itself); any exchange-write capability; any production-key creation; any MCP / Graphify / `.mcp.json` / credentials work.

The Phase 4ak M0 twelve-clause gate, post-null cooldown rule, and cooled-down families list remain binding prospective governance for any future research lane. The Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy remain binding.

---

## 17. Successor authorization

**None.** Phase 4bm-B does not authorize any successor phase. Conditionally, the operator may separately authorize:

- a future Phase 4bm-C — Multi-Day Normalized Structural QA Memo (Tier 1; analysis-and-docs; mirrors Phase 4be);
- a future Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate (Tier 1; docs-and-code; mirrors Phase 4bf);
- a future Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo (Tier 1; docs-only; mirrors Phase 4bg-A);
- a future Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording (Tier 1; docs + local gitignored artefact; mirrors Phase 4bg-B).

Each requires its own separate operator authorization. Phase 4bm-B authorizes none of them.

---

## 18. Recommended state

**Remain paused.**

Per the Phase 4bk-A workflow standard, Phase 4bm-B is branch-complete only by this work; it is **not** project-complete until a separately authorized merge phase records its merge-closeout on `main`. The conditional next-step ladder (merge → discussion → optionally Phase 4bm-C) is operator-driven.

---

## 19. Validation commands and exact output (post-run snippets)

```text
**Orchestrator final stdout line:**

```text
[Phase 4bm-B] PASS — produced 90 parquets totalling 155153449 events in 1460.5s; manifest at C:\Prometheus\data\microstructure\manifests\microstructure_normalized_aggtrades_v001__v002.json (sha256=01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a)
```

**Manifest sidecar parse verification:**

```text
sidecar_path:   data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256
sidecar_size:   118 bytes
sidecar_sha256: d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888
sidecar_body:   01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a  microstructure_normalized_aggtrades_v001__v002.json
parse_check:    embedded SHA matches recomputed manifest SHA bit-for-bit
```

**Immutability spot-check (4 of 188 witnesses; post-run):**

```text
v1_2025-01-15:    2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa  (Phase 4bd; unchanged)
v2_raw_manifest:  016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485  (Phase 4bl-C; unchanged)
v2_gate_report:   f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46  (Phase 4bl-D-R PASS; unchanged)
v2_successor_state: a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d  (Phase 4bl-E Stage-2 admissible; unchanged)
```

**Manifest content spot-check:**

```text
dataset_family:           microstructure_normalized_aggtrades_v001
dataset_version:          v002
schema_version:           v001
research_eligible:        False
eligibility_gate_status:  pending
produced_file_count:      90
total_event_count:        155153449
per_file_inventory_len:   90
first_file:               2024-12-01 with 731,065 events
last_file:                2025-02-28 with 4,526,219 events
governance_labels keys:   feature_computation, multi_day, phase, phase_4bm_b_no_successor_authorization,
                          source_dataset_family, source_dataset_version,
                          source_gate_report_code_commit_sha, source_gate_report_id, source_gate_report_sha256,
                          source_manifest_path, source_manifest_sha256, source_phase_boundary,
                          source_successor_state_sha256, stop_trigger_domain, strategy_use, validator
                          (16 keys)
```

**Whole-microstructure pytest:**

```text
1156 passed, 1 skipped in 12.64s
```
```
