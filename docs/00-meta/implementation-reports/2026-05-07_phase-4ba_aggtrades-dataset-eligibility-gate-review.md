# Phase 4ba — AggTrades Dataset Eligibility-Gate Review Memo

**Type:** docs-only governance / eligibility-gate review memo.
**Status:** drafted on branch `phase-4ba/aggtrades-dataset-eligibility-gate-review`; pending operator review and merge approval.
**Date:** 2026-05-07.

---

## 1. Phase header

Phase 4ba is a docs-only memo. It defines exactly what must be true before any aggTrades raw dataset family can become `research_eligible=true` or otherwise usable for downstream research. It is the natural successor to Phase 4ay (authorization-boundary memo) and Phase 4az (first authorized acquisition); it does **not** implement the eligibility gate, does **not** flip any flag on the Phase 4az dataset, does **not** acquire data, does **not** normalize, does **not** compute features, does **not** train models, and does **not** authorize any successor phase.

Phase 4ba's scope is narrow and explicitly bounded: it reviews the existing post-Phase-4az evidence and writes down — *before* a code-level eligibility gate is implemented — the rules that any such future gate would have to obey. The memo answers twelve operator-supplied questions and lays out a proposed staged eligibility model, the minimum gate checks, the manifest-field requirements, the invalid-window policy, the dataset-versioning policy, the downstream-use permissions, and the fail-closed rules. It then ranks the future phase options and stops.

After Phase 4ba merges, the recommended state is **remain paused**. No successor phase is authorized.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Branch | `phase-4ba/aggtrades-dataset-eligibility-gate-review` |
| Base SHA (`main`) | `203d9ae6ef71ca95ff77be70542474983f3292b2` |
| Base parent | `docs: merge README post-4az refresh` |
| Type | docs-only |
| Touches source / tests / scripts? | **No** |
| Touches data / manifests? | **No** |
| Touches `data/microstructure/`? | **No** (`.gitignore:85` continues to apply) |
| Touches retained verdicts? | **No** |
| Touches project locks? | **No** |
| Touches M0 governance? | **No** |
| Authorizes any successor? | **No** |
| Acquires data? | **No** |
| Calls Binance endpoints / opens WebSockets / uses credentials? | **No** |

The Phase 4az dataset (BTCUSDT, 2025-01-15 UTC, `microstructure_raw_aggtrades_v001`, 1,681,098 events, manifest `research_eligible=false`, `eligibility_gate_status=pending`) is on disk locally under the gitignored `data/microstructure/` tree. It is the only acquired aggTrades artefact in the project.

---

## 3. Inputs reviewed

Static repo inspection only. Phase 4ba did not run scripts, run tests, run mypy, run ruff, fetch endpoints, open WebSockets, download archives, or modify any file under `data/microstructure/`. The following committed sources were read:

- The Phase 4az main memo (`docs/00-meta/implementation-reports/2026-05-07_phase-4az_public-aggtrades-archive-acquisition.md`), §10–§14 (integrity-gate evidence, 19-check checklist, manifest review, data boundary).
- The Phase 4az closeout (`...2026-05-07_phase-4az_closeout.md`), §11–§14.
- The Phase 4az merge-closeout (`...2026-05-07_phase-4az_merge-closeout.md`).
- The Phase 4ay authorization memo (`...2026-05-07_phase-4ay_aggtrades-public-archive-acquisition-authorization.md`), §7–§16, especially §10 (19-check integrity gate), §12 (manifest authorization plan), §13 (failure / fail-closed rules), §14 (relationship to Phase 3p §4.7 strict integrity gate), §15 (relationship to §11.6 cost realism), §16 (relationship to M0 / no-rescue).
- The Phase 4ay closeout (`...2026-05-07_phase-4ay_closeout.md`).
- The Phase 4aw scaffold modules: `src/prometheus/research/microstructure/__init__.py`, `config.py`, `allowlist.py`, `invalid_window.py`, `manifest.py`, `raw_writer.py`. Especially:
  - `MicrostructureManifest` (`research_eligible: bool = False`, `eligibility_gate_status: EligibilityGateStatus = EligibilityGateStatus.PENDING`, `flip_research_eligible(...)` always raises `ManifestImmutableError`).
  - `EligibilityGateStatus` (`PENDING`, `PASS`, `FAIL`).
  - `InvalidWindowReason` (seventeen values: `MISSING_SEQUENCE`, `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `GAP_AFTER_RECONNECT`, `SNAPSHOT_MISMATCH`, `CLOCK_SKEW`, `SYMBOL_MISMATCH`, `STALE_STREAM`, `STALE_BOOK`, `IMPOSSIBLE_SPREAD`, `NEGATIVE_SIZE`, `ZERO_OR_INVALID_PRICE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP`, `FORCE_ORDER_PROXY_INCOMPLETENESS`, `FAILED_ATOMIC_WRITE`, `PARTIAL_FILE_RECOVERY_EVENT`).
  - `InvalidWindowSeverity` (`INFO`, `WARN`, `ERROR`).
  - `DownstreamEligibilityAction` (`FLAG`, `EXCLUDE`, `PROXY_ONLY`).
- The Phase 4ax aggTrades skeleton: `src/prometheus/research/microstructure/aggtrades.py` (`validate_aggtrade_payload`, `assert_aggtrades_endpoint_allowed`, `build_aggtrades_plan`, `write_validated_aggtrades_to_path`).
- The Phase 4az script `scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` — only structurally; not executed.
- The Phase 4az manifest `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` — only as JSON evidence; not modified.
- The Phase 4ak M0 governance document `docs/00-meta/m0-mechanism-admissibility-gate.md` (twelve-clause M0 gate, post-null cooldown rule, cooled-down families list, memo template).
- The Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Project locks: `§11.6 = 8 bps slippage per side; round-trip = 16 bps`; `§1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops`.
- Phase 3p §4.7 strict integrity gate (kline lineage; aggTrades equivalent recorded by Phase 4ay §14 and verified by Phase 4az §12).
- Phase 3r §8 (mark-price gap governance), Phase 3v §8 (stop-trigger-domain governance), Phase 3w §6 / §7 / §8 (break-even / EMA-slope / stagnation governance), Phase 4j §11 (OI subset governance).
- The retained-verdict ledger: H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread operationally closed; V2 / G1 / C1 hard reject — terminal for first-spec.

---

## 4. Scope

Phase 4ba is **docs-only**. The allowed activities are:

- Static repository inspection.
- Reasoning derived from the Phase 4aw scaffold, the Phase 4ax aggTrades skeleton, the Phase 4ay authorization framework, and the Phase 4az acquisition evidence.
- Authoring this memo and the Phase 4ba closeout under `docs/00-meta/implementation-reports/`.
- A narrow `docs/00-meta/current-project-state.md` update (Phase 4ba narrative paragraph + new "Current phase:" block; prior Phase 4az block preserved as historical context).

---

## 5. Non-scope

The following are **forbidden** and **not performed** in Phase 4ba:

- Compute features. Compute taker-imbalance, sweep detection, aggressive-flow score, microstructure imbalance, spread / depth proxies, or any other transform of acquired aggTrades.
- Normalize the dataset. Produce JSONL, Parquet, DuckDB, or any normalized table from the Phase 4az archive.
- Parse the raw archive for research analysis. Decompress, scan, summarise, sample, slice, or measure rows beyond what is strictly needed for review-time documentation (and Phase 4ba does not perform any such decompression).
- Produce descriptive trading statistics. No volume profile, no funding-aware overlay, no liquidity heatmap, no slippage estimate, no spread approximation, no microstructure ratio.
- Run backtests, historical strategy scripts, or simulations.
- Create ML labels. No supervised target. No regression target. No classification target.
- Train ML. No model fit, no embedding, no anomaly score, no calibration.
- Create a strategy candidate. No entry, no exit, no signal, no threshold.
- Acquire more data. No additional UTC days, no ETHUSDT, no monthly archive, no REST polling, no WebSocket capture, no order-book snapshot.
- Acquire ETHUSDT. Phase 4ba does not extend the symbol scope.
- Acquire additional BTCUSDT days. Phase 4ba does not extend the date scope.
- Call public endpoints. No live HTTP, no live archive download.
- Use private endpoints. No `fapi.binance.com`, no authenticated REST.
- Use WebSockets.
- Request or use credentials.
- Create `.mcp.json`.
- Enable MCP or Graphify.
- Modify `data/microstructure/`. The Phase 4az artefacts are read-only context for this memo.
- Modify manifests to flip `research_eligible`. Phase 4ba does **not** flip any eligibility flag on any dataset.
- Change project locks.
- Revise retained verdicts.
- Imply paper / shadow, live-readiness, deployment, or exchange-write capability.

---

## 6. Phase 4az evidence summary

Phase 4az is the only acquired aggTrades artefact in the project. The committed Phase 4az documentation states the evidence verbatim; this section restates the salient values for review-time grounding.

**Manifest (committed text, gitignored file):**

| Field | Value |
| ----- | ----- |
| `dataset_family` | `microstructure_raw_aggtrades_v001` |
| `version` | `v001` |
| `symbol` | `BTCUSDT` |
| `source` | `binance_data_archive` |
| `endpoint` | `data.binance.vision/data/futures/um/daily/aggTrades` |
| `endpoint_docs_reference` | `https://github.com/binance/binance-public-data#trades (futures aggTrades daily archive convention)` |
| `capture_mode` | `historical_archive` |
| `schema_version` | `v001` |
| `start_time_ms` | `1736899205109` (2025-01-15 00:00:05.109 UTC) |
| `end_time_ms` | `1736985599991` (2025-01-15 23:59:59.991 UTC) |
| `event_count` | `1,681,098` |
| `file_count` | `1` |
| `files[0].path` | `raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip` |
| `files[0].sha256` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| `files[0].event_count` | `1,681,098` |
| `files[0].start_time_ms` | `1736899205109` |
| `files[0].end_time_ms` | `1736985599991` |
| `invalid_windows` | `[]` |
| `retention_warning` | `null` |
| `proxy_warning` | `null` |
| `capture_config_hash` | `d7508638b2184f4754900b6f2c2165a9499d5e79d0494600a62516738368010d` |
| `code_commit_sha` | `caaad39e40604571758bc58eaac374344c7852e8` |
| `governance_labels` | `{phase=4az, source_phase_boundary=4ay, validator=phase_4ax_aggtrades_v001, stop_trigger_domain=trade_price_backtest_candidate, symbol_scope_source=archive_path, feature_computation=forbidden, strategy_use=forbidden}` |
| `research_eligible` | **`false`** |
| `eligibility_gate_status` | **`pending`** |

**Integrity-gate result:** Phase 4ay §10 19-check checklist: 18 PASS + 1 NOT_APPLICABLE (`invalid_windows` because no integrity events occurred). The `invalid_windows` list is empty.

**Boundary observations:**

- The archive `.zip` (~21 MiB) was downloaded once from the public `data.binance.vision` archive; the SHA256 matched the `.CHECKSUM` companion bit-for-bit on first compare.
- All 1,681,098 rows passed `validate_aggtrade_payload`. Aggregate trade IDs are monotonically non-decreasing with no duplicates. Timestamps are within the requested UTC day exactly.
- The acquisition script wrote four files under the gitignored `data/microstructure/` tree: the raw `.zip`, the paired `.sha256`, the manifest JSON, and an acquisition log JSON. None of these is committed; `git status` does not list them.
- No Binance API endpoint was contacted. No WebSocket was opened. No credential was used.
- The Phase 4aw `flip_research_eligible(...)` method (`ManifestImmutableError`) was **not** bypassed. The manifest is JSON-only and does not round-trip back through the dataclass; the field defaults match Phase 4ay §12 verbatim.

---

## 7. What Phase 4az proves

- **Acquisition discipline works.** A predeclared single-day BTCUSDT public archive can be downloaded, checksum-verified, schema-validated row-by-row, stored under a gitignored namespace, and described by a `MicrostructureManifest`-shaped JSON without contacting any private endpoint, opening any WebSocket, or using any credential.
- **The Phase 4ay strict integrity gate composes cleanly.** All 18 applicable checks pass on a real Binance public-archive day, with the 19th (`invalid_windows`) correctly recorded as `NOT_APPLICABLE` rather than vacuously PASS.
- **The Phase 4ax aggTrades validator handles real Binance archive rows without modification.** No false rejection across 1,681,098 rows; no schema patching required.
- **Atomic staging-then-final movement works.** The download lands in `staging/...` first, integrity gate runs, only then the artefact moves to `raw/...` with paired `.sha256`. Failure preserves staging for inspection and never creates a final file.
- **No-overwrite discipline works.** Pre-existing finals abort the run by default.
- **The `data/microstructure/` boundary holds.** `git check-ignore` confirms `.gitignore:85` covers the entire subtree; no acquired byte was committed.
- **Manifest defaults survive a real run.** `research_eligible=false` and `eligibility_gate_status=pending` remained in place; nothing flipped them.

In short: Phase 4az proves that the project can acquire one tightly scoped aggTrades archive **safely**.

---

## 8. What Phase 4az does not prove

- **Edge.** No predictive content, no opportunity rate, no microstructure feature viability, no strategy potential. The acquired data is one UTC day's worth of one symbol's aggregate trades; no statistical claim is made or licensed.
- **Eligibility.** The dataset is **infrastructure evidence**, not research evidence. `research_eligible=false` is the truthful state, not a placeholder.
- **Reproducibility across runs.** A single SHA256 match against a single `.CHECKSUM` companion at one acquisition time does not establish that re-fetching the same date from the public archive in the future will produce a byte-identical artefact (Phase 4ay §17.A flagged this consideration). This is not currently a blocker; it is an unverified property.
- **Schema parity with the public-data repo.** The Phase 4ax validator passed every row, but Phase 4ba is not a schema audit against `https://github.com/binance/binance-public-data`. A future memo (or the eligibility gate itself) must record the exact archive column names, column order, and any version drift.
- **Coverage of operational pathologies.** A single quiet 24-hour window may not exercise: archive splits, mid-day gaps, vendor outages, exchange maintenance, halts, listing-day partial coverage, late-month archive availability, or `.CHECKSUM` companion absence. Phase 4az encountered none of these.
- **Retention envelope.** The archive's retention behaviour was not stress-tested.
- **Manifest round-trip strictness.** The Phase 4aw `MicrostructureManifest.from_dict(...)` accepts the Phase 4az JSON shape, but Phase 4az writes JSON directly without round-tripping through the dataclass at write time. The dataclass-side strict validation has not been exercised against this manifest.
- **The eligibility gate.** No code-level eligibility-gate primitive exists. `flip_research_eligible` always raises. Until a separately authorized phase implements the gate, the dataset cannot become `research_eligible=true`.

---

## 9. Proposed eligibility model

Phase 4ba recommends a **staged eligibility model**, not a single boolean. The Phase 4aw `EligibilityGateStatus` already provides three values (`PENDING`, `PASS`, `FAIL`), and the Phase 4ba review extends the semantics to a five-stage research-use ladder. The boolean `research_eligible` remains the single authoritative field for downstream code paths; it flips to `true` if and only if the staged ladder reaches the eligible-for-research stage.

### 9.1 Why staged, not boolean

A pure boolean creates a binary "ineligible / eligible for everything" cliff. AggTrades data has at least four distinct downstream uses with distinct safety profiles: (a) inspection / review only; (b) normalization to a derived dataset; (c) feature computation under M0; (d) ML / strategy / backtest input. Treating these as a single yes/no risks either being too conservative (blocking legitimate inspection) or too permissive (a single PASS unlocks ML training).

A staged ladder lets the gate make explicit, separately approvable transitions. The boolean `research_eligible` can still gate downstream code (it must be `true` for any feature / ML / backtest path), but the staged ladder makes clear *what* "research-eligible" means and what evidence supported it.

### 9.2 Proposed five-stage ladder

| Stage | Label | `research_eligible` | `eligibility_gate_status` | Allowed downstream uses |
| ----- | ----- | ------------------- | ------------------------- | ----------------------- |
| 0 | `acquired` | `false` | `pending` | Acquisition logs and manifest review only. No decompression for analysis. (Phase 4az dataset is currently here.) |
| 1 | `inspected` | `false` | `pending` | Operator decompression for hand inspection in a sandbox. No tracked output. No persisted derived artefact. |
| 2 | `gate-passed` | `false` | `pass` | Eligible to be used as input to a separately authorized normalization phase. Still not eligible for features / ML / backtests. |
| 3 | `normalized` | `true` | `pass` | Eligible for feature computation under a separately authorized M0-cleared hypothesis-spec memo. |
| 4 | `feature-cleared` | `true` | `pass` | Eligible for ML / strategy / backtest input under a separately authorized strategy-spec memo that satisfies M0, the Phase 4m 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix. |

**Important asymmetry:** the `research_eligible` boolean flips at Stage 3, not Stage 2. Stage 2 records that the integrity gate has passed, but the actual `research_eligible=true` transition occurs only when a separately authorized normalization phase has produced a derived artefact and recorded its own pass evidence. This protects against the trap of letting "raw integrity passed" silently authorize feature work.

The Phase 4aw `flip_research_eligible(...)` method (`ManifestImmutableError`) remains the only path that could legitimately mutate `research_eligible`; until a code-level eligibility-gate primitive replaces it, the field cannot be flipped.

### 9.3 Cooldown and demotion semantics

A dataset that reaches Stage 2 or Stage 3 must be **demotable**. If a later check (e.g. an eligibility-gate audit, a re-acquisition mismatch, or an integrity event surfaced by a downstream consumer) invalidates the basis for the prior stage, the gate must demote the dataset, set `eligibility_gate_status=fail`, set `research_eligible=false`, and append an `invalid_window` entry recording the reason.

Demotion is not a "rescue path in reverse"; it is a fail-closed primitive. It does not require operator approval to take effect, but it does require an audit log entry and a follow-up operator review.

### 9.4 Per-dataset, not project-wide

The eligibility ladder is per dataset (per `dataset_family` × `version` × `symbol` × file set). It is not a project-wide flag. Phase 4az is the only artefact in the ladder today, currently at Stage 0.

---

## 10. Required gate checks

This section answers operator question 3. The minimum checks any future code-level eligibility gate must enforce before it may set `eligibility_gate_status=pass` (Stage 2) or `research_eligible=true` (Stage 3) are partitioned by category. Phase 4ay §10 specified the **acquisition-time** integrity gate (run once at acquisition); Phase 4ba specifies the **eligibility-time** gate (run by a future eligibility-gate phase against the already-acquired manifest and raw bytes). The two gates compose: acquisition-time gate must have passed, and eligibility-time gate must independently re-verify a subset and add gate-specific checks.

### 10.1 Source

1. **Source label is `binance_data_archive`** or another whitelisted public-only label.
2. **Endpoint label matches a documented archive family** (e.g. `data.binance.vision/data/futures/um/daily/aggTrades`).
3. **`endpoint_docs_reference` is non-empty** and references a documented official source (e.g. `https://github.com/binance/binance-public-data#trades`).
4. **No private-endpoint label** appears in `endpoint`, `source`, or `governance_labels`.
5. **`capture_mode` is `historical_archive`** for archive-acquired data; `live_capture` modes require their own gate spec (out of scope for Phase 4ba).

### 10.2 Checksum

6. **`files[*].sha256` is a 64-character lowercase hex string.** The `MicrostructureManifest.FileEntry.__post_init__` already enforces this on construction.
7. **Bit-for-bit recomputation matches manifest digest.** The eligibility gate must independently re-hash the on-disk `.zip` and verify equality with `files[*].sha256`. The gate must also verify that the paired `<file>.sha256` sidecar (if present) matches.
8. **`.CHECKSUM` companion verification recorded.** Either a `.CHECKSUM` was present at acquisition time and matched, or the absence is recorded in `governance_labels` (e.g. `checksum_companion_absent: "true"`). Acquisition without checksum is a permanent disqualification for `research_eligible=true` unless a separately authorized governance memo amends this rule.

### 10.3 Manifest

9. **Required fields populated.** Every required `MicrostructureManifest` field is non-empty (`dataset_family`, `version`, `symbol`, `source`, `endpoint`, `capture_mode`, `schema_version`, `endpoint_docs_reference`, `capture_config_hash`, `code_commit_sha`).
10. **`research_eligible` is `false` and `eligibility_gate_status` is `pending`** at the time the gate runs. The gate is the only path that may flip these; it does not run on already-PASSed datasets.
11. **`governance_labels` includes minimum keys.** At least: `validator`, `stop_trigger_domain` (with a value from the Phase 3v §8 enum), `feature_computation` (`forbidden` for raw datasets), `strategy_use` (`forbidden` for raw datasets), `phase` (the acquisition phase label, e.g. `4az`), `source_phase_boundary` (the authorization phase label, e.g. `4ay`).
12. **`code_commit_sha` exists in repo history.** Re-running the gate against an unknown commit fails closed (the dataset cannot be tied to a reproducible code state).
13. **`capture_config_hash` is non-empty and matches a deterministic config-hash.** The gate must be able to re-derive the hash from the recorded acquisition config; mismatch fails closed.

### 10.4 Schema

14. **Every row passes `validate_aggtrade_payload` (Phase 4ax)**, with the additional archive-row-shape constraints: required keys `a`, `p`, `q`, `f`, `l`, `T`, `m`; optional `E`; `f ≤ l`; `T > 0`; `m` is a strict bool (string-coerced from `true`/`True`/`TRUE`/`false`/`False`/`FALSE`); price > 0; quantity > 0.
15. **Column order is recorded.** The eligibility gate must record the observed CSV column order verbatim in `governance_labels.csv_column_order` (or in the acquisition log) so future re-runs detect upstream column reordering.
16. **No row has unexpected extra fields beyond the documented archive schema.** Unknown fields are preserved during validation but recorded in a gate report; any unknown field that did not appear in the previous gate run for the same `dataset_family` raises an integrity event.

### 10.5 Timestamps

17. **All `T` values are int milliseconds** within `[start_time_ms, end_time_ms]`.
18. **`start_time_ms` ≤ `end_time_ms`.**
19. **`T` non-decreasing across the file** (i.e. no rewinds). Decreases are recorded as `OUT_OF_ORDER_EVENT` invalid windows and the gate fails closed.
20. **UTC-day match.** For `historical_archive` daily files, every `T` falls within the requested 24-hour UTC day, inclusive of `00:00:00.000` and exclusive of the next day's `00:00:00.000`. Any boundary entries are recorded.

### 10.6 Monotonicity (aggregate trade IDs)

21. **`a` is monotonically non-decreasing across the file.** Decreases are `OUT_OF_ORDER_EVENT` integrity events.
22. **`a` increments are non-negative.** Negative increments fail closed.
23. **No `a` value reappears with a different `(p, q, m, T)` tuple.** This is a post-deduplication consistency check.

### 10.7 Duplicates

24. **No duplicate `(a)` within the file.** Duplicates are `DUPLICATE_EVENT` integrity events.
25. **`f ≤ l` for every row.** First-trade-id ≤ last-trade-id within an aggregate trade.

### 10.8 Row count

26. **`event_count > 0`.**
27. **`event_count` matches the actual row count of the on-disk file.** The gate re-counts; mismatch fails closed.
28. **`event_count` is consistent with `sum(files[*].event_count)`** for multi-file datasets. Phase 4az has `file_count = 1` so this collapses to a tautology, but the rule is binding for any future multi-file family.

### 10.9 Symbol / date

29. **`symbol` is in the project's symbol allowlist** (Phase 4aw `MicrostructureConfig.symbol_allowlist`, which by default is `("BTCUSDT", "ETHUSDT")`). Alt symbols require explicit caller admission.
30. **`symbol_scope_source` recorded.** For archive-acquired data, the symbol is enforced by the archive path (e.g. `archive_path`); the gate verifies the path-encoded symbol matches the manifest `symbol` field exactly.
31. **The file's UTC date matches its archive-path date.** For daily archives (e.g. `BTCUSDT-aggTrades-2025-01-15.zip`), the gate parses the date from the path and verifies that all `T` values fall within that UTC day.
32. **Date is within retention window.** If the date is older than the documented public-archive retention bound, the gate either accepts (with `retention_warning` recorded) or fails closed depending on a separately authorized retention-governance memo. Phase 4ba does not propose such a memo; the conservative default is **fail closed** when retention is unknown.

### 10.10 Archive integrity

33. **Single CSV member per ZIP.** The archive contains exactly one CSV member; any other arrangement fails closed.
34. **CSV decompresses cleanly.** No partial extraction, no truncated trailer, no bad EOF.
35. **File size within bounds.** Greater than 0; less than the predeclared upper bound (Phase 4ay §10 chose 5 GiB; Phase 4ba retains this bound).
36. **Archive byte count recorded.** The gate records the raw byte count and verifies it matches the on-disk file size.

### 10.11 Invalid windows

37. **`invalid_windows` is parseable into Phase 4aw `InvalidWindow` records.** Round-trip via `InvalidWindow.from_dict(...)` and `InvalidWindow.to_dict(...)` must be lossless.
38. **Every `InvalidWindow` has a non-empty `evidence` mapping.** Phase 4aw enforces this on construction; the gate re-verifies after deserialisation.
39. **Severity / action consistency.** An `ERROR`-severity window must have `downstream_eligibility_action` set to `EXCLUDE` or `PROXY_ONLY`; a window with `EXCLUDE` action must have severity `WARN` or `ERROR`. (`INFO` + `EXCLUDE` is inconsistent; gate fails closed.)
40. **No silent omission.** If a row failed any per-row integrity check during acquisition, the corresponding `InvalidWindow` must exist; gate-time row scanning must not rediscover row failures that are not already represented.

### 10.12 Cross-cutting

41. **`governance_labels.feature_computation` is `forbidden`** for any raw dataset family. A normalized dataset family may relax this only after passing its own gate.
42. **`governance_labels.strategy_use` is `forbidden`** for any raw dataset family.
43. **`governance_labels.stop_trigger_domain` is from the Phase 3v §8 enum** (one of the documented values, e.g. `trade_price_backtest_candidate`).
44. **No private-endpoint or credential-shaped string** appears anywhere in the manifest or acquisition log.
45. **Acquisition log is present and self-consistent.** The acquisition-time log file (`<dataset_family>__<version>_acquisition_log.json`) exists, documents the same `start_time_ms` / `end_time_ms` / `event_count` as the manifest, and references the same `code_commit_sha`.

A dataset that passes every check in §10.1 through §10.12 may transition from `eligibility_gate_status=pending` to `pass`. It may **not** automatically flip `research_eligible` to `true`; that flip requires Stage 3 (normalization), per §9.

---

## 11. Required manifest fields

This section consolidates the manifest contract required for any aggTrades raw dataset family seeking eligibility. All fields use the Phase 4aw `MicrostructureManifest` shape verbatim.

### 11.1 Mandatory non-empty strings

- `dataset_family` — must match the canonical family name (e.g. `microstructure_raw_aggtrades_v001`).
- `version` — must match a registered version label (e.g. `v001`).
- `symbol` — must be in the symbol allowlist.
- `source` — must be a whitelisted public-only label.
- `endpoint` — must be a documented archive endpoint family.
- `capture_mode` — must be one of `historical_archive` (or future labels added by separately authorized governance).
- `schema_version` — must match a registered schema label.
- `endpoint_docs_reference` — must reference an official documented source.
- `capture_config_hash` — must be deterministic and re-derivable.
- `code_commit_sha` — must exist in repo history.

### 11.2 Mandatory numerics

- `start_time_ms`, `end_time_ms`, `event_count`, `file_count` — non-negative integers; consistent with `files[*]`.
- Every `files[*].sha256` is a 64-char lowercase hex string; `event_count`, `start_time_ms`, `end_time_ms` non-negative; `end_time_ms ≥ start_time_ms`.

### 11.3 Mandatory governance labels

- `phase` — acquisition phase label (e.g. `4az`).
- `source_phase_boundary` — authorization phase label (e.g. `4ay`).
- `validator` — validator identity label (e.g. `phase_4ax_aggtrades_v001`).
- `stop_trigger_domain` — value from the Phase 3v §8 enum.
- `symbol_scope_source` — how the symbol was enforced (e.g. `archive_path`).
- `feature_computation` — `forbidden` for any raw family.
- `strategy_use` — `forbidden` for any raw family.

### 11.4 Mandatory eligibility fields

- `research_eligible` — `false` until Stage 3 is reached.
- `eligibility_gate_status` — one of `pending`, `pass`, `fail`.

### 11.5 Optional fields with strict semantics

- `retention_warning` — `null` if the dataset is comfortably within retention; a non-null string label if not.
- `proxy_warning` — `null` for canonical archives (`historical_archive`); a non-null string label for proxy-acquired data (e.g. forceOrder proxy).
- `invalid_windows` — `[]` if the integrity gate produced no events; otherwise a list of Phase 4aw `InvalidWindow` records.

### 11.6 Forbidden manifest content

- No API keys, signed payloads, request signatures, or credential-shaped strings anywhere.
- No private-endpoint labels.
- No live capture mode (until separately authorized).
- No `feature_computation: allowed` or `strategy_use: allowed` on any raw family.
- No `research_eligible: true` until Stage 3 is reached.

---

## 12. Required invalid-window policy

This section restates the invalid-window policy and adds the eligibility-time semantics not yet present in earlier phases.

### 12.1 Taxonomy (Phase 4aw verbatim, seventeen reasons)

`MISSING_SEQUENCE`, `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `GAP_AFTER_RECONNECT`, `SNAPSHOT_MISMATCH`, `CLOCK_SKEW`, `SYMBOL_MISMATCH`, `STALE_STREAM`, `STALE_BOOK`, `IMPOSSIBLE_SPREAD`, `NEGATIVE_SIZE`, `ZERO_OR_INVALID_PRICE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP`, `FORCE_ORDER_PROXY_INCOMPLETENESS`, `FAILED_ATOMIC_WRITE`, `PARTIAL_FILE_RECOVERY_EVENT`.

For raw archive-acquired aggTrades, the most common eligibility-time triggers will be: `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `SYMBOL_MISMATCH`, `ZERO_OR_INVALID_PRICE`, `NEGATIVE_SIZE`, `ARCHIVE_CHECKSUM_MISMATCH`, `REST_RETENTION_GAP` (only if the archive falls outside retention), `FAILED_ATOMIC_WRITE` (only if a prior acquisition was interrupted), `PARTIAL_FILE_RECOVERY_EVENT` (only if a recovery procedure ran).

### 12.2 Severity model

- `INFO` — informational; does not block eligibility on its own.
- `WARN` — must be acknowledged in the gate report; `EXCLUDE` or `PROXY_ONLY` action may be required.
- `ERROR` — fails the eligibility gate by default; may require reacquisition or a new dataset version.

### 12.3 Downstream-action model

- `FLAG` — record but allow downstream use (acceptable for `INFO` events that are merely informational).
- `EXCLUDE` — exclude affected rows / time ranges from any downstream use; downstream consumers must respect this.
- `PROXY_ONLY` — the affected portion is acceptable only as a proxy and must not be used as canonical evidence.

### 12.4 Recording requirements

- Every `InvalidWindow` carries non-empty `evidence` (sequence numbers, observed `T` values, expected vs observed checksums, byte offsets, etc.).
- Evidence must be reproducible from the manifest + raw file alone.
- The gate must record, for each window, the originating check from §10 (e.g. "produced by §10.6 monotonicity check").

### 12.5 Aggregation semantics

- Many small contiguous events of the same reason must be coalesced into a single window with `start_time_ms` and `end_time_ms` covering the span and an evidence count.
- Distinct reasons must not be merged.
- Windows must not overlap for the same reason on the same dataset.

### 12.6 No silent omission

- The gate must never drop a row, decompress-and-discard, forward-fill, or impute. Any operation that would change the row count from the on-disk archive's actual row count is forbidden.
- Phase 3p §4.7 forbidden patterns (forward-fill, interpolation, imputation, silent omission) apply per Phase 4ay §14 mapping.

### 12.7 Demotion trigger

- An `ERROR`-severity window appearing on a Stage ≥ 2 dataset triggers demotion (per §9.3). The gate sets `eligibility_gate_status=fail`, sets `research_eligible=false`, and records the demotion reason in `governance_labels.demotion_reason`.

---

## 13. Required dataset-versioning policy

This section answers operator question 7. It records the conditions that determine whether a problem can be addressed by re-acquisition under the same version, requires a new dataset version, or makes the dataset permanently ineligible.

### 13.1 The same-version reacquisition lane

A reacquisition under the same `(dataset_family, version)` is allowed if and only if:

- The acquisition-time integrity gate failed in a way that does not invalidate the archive's authoritative byte content (e.g. a `FAILED_ATOMIC_WRITE` due to local disk error; a `.CHECKSUM` mismatch caused by a bit-flip on the local disk that is detectable by re-fetching).
- The public archive byte content is unchanged across runs (recommended check: `.CHECKSUM` companion is identical between runs; local-side re-hash matches).
- No row content changes; no row count changes; no `T` range changes.

A reacquisition under the same version overwrites the staging area only after the existing finals are explicitly cleared by the operator. The Phase 4az script's `--fail-if-existing` default must remain in place; same-version reacquisition is an explicit operator action, not a script default.

### 13.2 New-version triggers

A new dataset version is **required** (not optional) when any of the following holds:

- The public archive's published byte content changes for the same `(symbol, date)`. (Detectable by `.CHECKSUM` comparison between runs.)
- The archive schema changes (new columns, renamed columns, column reordering, format change).
- The archive endpoint family changes (e.g. Binance restructures the public archive).
- The validator (`phase_4ax_aggtrades_v001`) is replaced by a newer validator with non-equivalent semantics.
- The acquisition methodology changes in a way that affects what is recorded (e.g. a new integrity check is added, a checksum tolerance is introduced — both of which Phase 4ba does not propose, but the rule is binding).
- The `governance_labels` contract changes in a way that is not backwards-compatible.
- A demotion (§9.3) on a Stage ≥ 2 dataset has occurred and a fresh acquisition is required to recover.

A new version is named by incrementing the version suffix (`v001` → `v002`). The previous version's manifest, raw `.zip`, and acquisition log must remain on disk and gitignored; nothing is deleted by a version increment.

### 13.3 Permanent ineligibility

A dataset is **permanently ineligible** (cannot reach Stage 2 or beyond, period) if:

- The `.CHECKSUM` companion is missing **and** the public archive cannot otherwise establish bit-fidelity for the file. (The gate may not "trust the byte content because we hashed it on disk"; the digest must be tied to a published source-of-truth.)
- The archive is corrupt at the bytes level and cannot be re-acquired (e.g. retention has expired and no other public source publishes the same bytes).
- The archive contains data that violates a project lock that is not amendable by the eligibility gate (e.g. a row with `m` not strictly bool — the validator already fails closed; this is recorded for clarity).
- The dataset is found to encode a Binance-private artefact that should not have entered the public archive (extremely unlikely; flagged for completeness).
- A successor governance memo retroactively forbids the dataset family (e.g. a future memo declares `microstructure_raw_aggtrades_v001` retired in favour of `_v002`).

Permanent ineligibility is recorded by setting `eligibility_gate_status=fail` and adding `governance_labels.permanent_ineligibility_reason`. The dataset is preserved on disk as audit evidence; it is not deleted.

### 13.4 Reacquisition vs new version vs ineligibility decision matrix

| Symptom | Outcome |
| ------- | ------- |
| Local `.zip` corrupted; public bytes unchanged | Same-version reacquisition |
| Public archive bytes changed | New version |
| Schema column reordering | New version |
| Validator replaced | New version |
| Governance contract change | New version |
| `.CHECKSUM` permanently absent | Permanent ineligibility |
| Archive expired and unobtainable | Permanent ineligibility |
| Demotion from Stage ≥ 2 | New version (recommended) or same-version reacquisition (only if the underlying bytes are confirmed unchanged) |

---

## 14. Required downstream-use permissions

This section answers operator questions 8, 9, and 10. It defines the minimum evidence required before each downstream-use category becomes allowable. Each prerequisite is **necessary**; none is sufficient on its own.

### 14.1 Before normalization is allowed

- The dataset has reached Stage 2 (`eligibility_gate_status=pass`).
- A separately authorized normalization phase memo exists, predeclaring:
  - the exact derived schema (column names, types, units);
  - the exact transformation (e.g. row passthrough vs aggregation);
  - the new dataset family name and version (e.g. `microstructure_normalized_aggtrades_v001`);
  - the storage layout under `data/microstructure/normalized/...`;
  - the manifest contract for the normalized family;
  - the eligibility-gate behaviour for the normalized family (a separate gate; does not inherit from the raw family).
- The normalization phase produces no feature, no metric, no transform other than the documented ones; it is structurally analogous to Phase 4az for raw acquisition.

### 14.2 Before feature computation is allowed

- The dataset has reached Stage 3 (`research_eligible=true` on a normalized dataset).
- A separately authorized hypothesis-spec memo exists that satisfies the Phase 4ak twelve-clause M0 mechanism-admissibility gate — specifically: a clear mechanism statement; a falsifiable predeclaration; a relevant-time-period commitment; a no-rescue clearance; cooled-down-family non-overlap; data-availability declaration; methodology pre-registration; cost-realism preservation; non-leakage assertion; sample-size predeclaration; baseline-superiority commitment; explicit forbidden-paths enumeration.
- The hypothesis-spec memo also satisfies the Phase 4m 18-requirement validity gate and the Phase 4t 10-dimension scoring matrix.
- The feature implementation produces no implicit edge claim; it is mechanically a transform of the underlying data, with the edge claim deferred to the strategy-spec memo.

### 14.3 Before ML / strategy research / backtesting is allowed

- The dataset has reached Stage 4 (`feature-cleared`) on at least one feature family.
- A separately authorized strategy-spec memo exists and pre-declares:
  - the entry rule;
  - the exit rule;
  - the position sizing and risk budget (subject to §1.7.3 = 0.25% / 2× / one-position max);
  - the cost model preserving §11.6 = 8 bps slippage per side;
  - the no-rescue posture vs cooled-down families (R2 / F1 / D1-A / V2 / G1 / C1);
  - the no-old-strategy-alt-symbol-rerun discipline;
  - the falsification predicate;
  - the success / partial / hard-reject thresholds;
  - the data-resolution boundary (Phase 4al §14 hierarchy preserved).
- The strategy-spec memo passes M0, the Phase 4m 18-requirement validity gate, and the Phase 4t 10-dimension scoring matrix.
- The backtest plan memo additionally pre-declares: the train / validation / OOS split; the variant grid; the deflated-Sharpe / PBO / CSCV discipline; the catastrophic-floor predicate; the verdict taxonomy.
- A separately authorized backtest-execution phase exists (analogous to Phase 4l / 4r / 4x for retired families).

Each of Stages 2 → 3 → 4 requires a separate operator decision and a separate authorization memo. Phase 4ba does not authorize any of these.

---

## 15. Fail-closed rules

This section answers operator question 11. It enumerates fail-closed rules that bind the future code-level eligibility-gate when eligibility status is unknown, mixed, stale, partial, or ambiguous.

### 15.1 Unknown

- **Unknown manifest field** — gate fails closed; cannot pass.
- **Unknown enum value** in `eligibility_gate_status`, `stop_trigger_domain`, `feature_computation`, or `strategy_use` — gate fails closed.
- **Unknown `dataset_family` or `version`** — gate fails closed; the family / version must be registered before the gate runs.
- **Unknown commit SHA in `code_commit_sha`** — gate fails closed.
- **Unknown `capture_config_hash`** — gate fails closed.

### 15.2 Mixed

- **Manifest claims `research_eligible=true` but `eligibility_gate_status=pending` or `fail`** — gate fails closed and demotes to `fail`. (`true / pending` and `true / fail` are inconsistent; the gate refuses to honour the inconsistent state.)
- **Some files PASS, some files FAIL within the same manifest** — gate fails closed for the whole manifest. Per-file PASS does not yield manifest-level PASS.
- **Mixed severities** without a `downstream_eligibility_action` consistent with the highest severity — gate fails closed.

### 15.3 Stale

- **Manifest references a `code_commit_sha` older than the gate's minimum-acceptable-age policy** — gate may fail closed under a separately authorized staleness policy. Phase 4ba does not impose a numeric staleness bound; it records that one is required before any production-grade eligibility gate goes live.
- **`endpoint_docs_reference` points to a documentation page known to be deprecated** — gate fails closed; the reference must be updated and the manifest amended via a new version.
- **Manifest's `start_time_ms` falls outside the public archive's documented retention window** without a `retention_warning` — gate fails closed.

### 15.4 Partial

- **Acquisition log present but truncated or malformed** — gate fails closed.
- **`.CHECKSUM` companion absent and `governance_labels.checksum_companion_absent` not set** — gate fails closed.
- **`files[*]` present but on-disk file missing or unreadable** — gate fails closed.
- **`invalid_windows` non-empty but no per-window evidence** — gate fails closed.

### 15.5 Ambiguous

- **Two manifests for the same `(dataset_family, version, symbol, file)` exist with different content** — gate fails closed for both.
- **The on-disk `.zip` SHA256 matches `files[0].sha256` but the `.sha256` sidecar disagrees** — gate fails closed.
- **`governance_labels.feature_computation` says `allowed` on a raw family** — gate fails closed; raw families always have `feature_computation: forbidden`.
- **`governance_labels.strategy_use` says `allowed` on a raw family** — gate fails closed.

### 15.6 Cross-cutting fail-closed rules

- Any attempt by the gate to skip a §10 check is a programming error; the gate code must not have a "skip" path.
- The gate must never write outside `data/microstructure/`, except for its own gate-report log under `data/microstructure/gate-reports/` (descriptive only; not created by Phase 4ba; reserved for a future gate phase).
- The gate must never modify the raw `.zip`, the paired `.sha256`, the manifest, or the acquisition log of an existing dataset. It may only append a gate report and (if applicable) demote `eligibility_gate_status` and `research_eligible` via a successor manifest write — which itself requires the future eligibility-gate primitive that replaces `flip_research_eligible(...)`.
- The gate must not call any Binance endpoint, open any WebSocket, or use any credential at runtime. The §10.1–§10.3 source / checksum / manifest checks are all offline checks against the local manifest, the local raw `.zip`, the local `.sha256` sidecar, the local `.CHECKSUM` companion (if available), and the local acquisition log.
- The gate must not flip `research_eligible=true` for any raw family, ever. Stage 3 and Stage 4 transitions occur only on derived (normalized / feature) families, each of which has its own gate and its own memo.

---

## 16. Recommended future phase options

Phase 4ba does not authorize any successor. The following are recorded for operator evaluation only.

### Option A — Remain paused

**Status:** **primary recommendation.** Procedurally clean; preserves every retained verdict and every project lock; no further microstructure work happens until a separate operator decision authorizes it.

### Option B — Future docs-only Phase 4bb data-quality interpretation memo

**Status:** allowable; **not authorized** by Phase 4ba.

A future docs-only memo could review the Phase 4az dataset as observational evidence about Binance's public-archive aggTrades quality (without computing strategy features or descriptive trading statistics). Allowed scope: row-count parity vs published archive size; checksum companion availability behaviour across one day's worth of data; `T` distribution by hour as a coverage check; aggregate-trade-id distribution as a continuity check. Forbidden: any aggregation that produces a microstructure feature, a flow ratio, a sweep score, or a slippage proxy.

This is a "what does the data look like, structurally?" memo, not a "what edge does it carry?" memo.

### Option C — Future docs-only Phase 4bb eligibility-gate execution-plan memo

**Status:** allowable; **not authorized** by Phase 4ba.

A future docs-only memo could translate the Phase 4ba eligibility model and check list into an execution plan for a code-level gate primitive (file layout, function signatures, fail-closed branches, gate-report schema, manifest-update primitive, demotion path), without implementing any code.

### Option D — Future docs-and-code Phase 4bb eligibility-gate primitive implementation

**Status:** allowable; **not authorized** by Phase 4ba.

A future docs-and-code phase could implement the eligibility-gate primitive as a standalone offline tool that reads the manifest + raw `.zip` + `.sha256` sidecar + `.CHECKSUM` companion (if present) + acquisition log, runs every §10 check, produces a gate report under `data/microstructure/gate-reports/`, and (optionally) writes a successor manifest with `eligibility_gate_status=pass` or `fail`. This phase would replace `flip_research_eligible(...)` with a real gate-controlled mutation primitive. It must remain offline-only, must not call any Binance endpoint, must not flip `research_eligible=true` for raw families, and must not authorize features / ML / strategy / backtest.

### Option E — Future docs-only Phase 4bb extension to additional dataset families

**Status:** allowable; **not authorized** by Phase 4ba.

A future docs-only memo could extend the Phase 4ba eligibility model to additional dataset families (e.g. `microstructure_raw_bookticker_v001`, `microstructure_raw_depth_v001`, `microstructure_raw_forceorder_proxy_v001`). Each new family has its own §10 check list (bookticker checks differ from aggTrade checks; depth-snapshot checks differ from both; forceOrder is a proxy with its own `proxy_warning` semantics). Phase 4ba's contract is **aggTrades-only**; extension to other families is reserved for a separately authorized memo.

### Option F — Acquire additional aggTrades data

**Status:** **not recommended now.** Phase 4ay's authorization is for one tightly scoped acquisition; Phase 4az consumed that authorization. Any further acquisition (additional UTC days; ETHUSDT; monthly archives; alt symbols; live capture) requires its own separately authorized acquisition memo and is not the right next step before the eligibility gate is reasoned through.

### Option G — Compute features / train ML / build strategy

**Status:** **forbidden.** Phase 4ba forbids this until at least Stage 4 is reached on at least one feature family — which requires Stages 2 (gate-passed), 3 (normalized), and 4 (feature-cleared), each separately authorized.

---

## 17. Final recommendation

After Phase 4ba merges to `main`, **remain paused**.

The eligibility gate is now specified in writing. No flag was flipped. No data was modified. No code was written. No verdict was revised. No lock was loosened.

If the operator chooses to advance, the cleanest sequence is:

1. **Optional Phase 4bb-A:** docs-only data-quality interpretation memo (Option B above). Cheap and unconditionally informative.
2. **Optional Phase 4bb-B:** docs-only eligibility-gate execution-plan memo (Option C above). Translates §10 into a precise file-by-file implementation plan without writing code.
3. **Optional Phase 4bb-C:** docs-and-code eligibility-gate primitive implementation (Option D above). Implements the gate as an offline tool. Even if this phase ever runs, it does not flip `research_eligible=true` for any raw family.

Each step requires a separate operator decision. Phase 4ba does not commit to any of them.

---

## 18. Closeout / preservation of locks

Phase 4ba preserves verbatim:

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
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az results.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane. No retained verdict is revised. The Phase 4az dataset's `research_eligible=false` and `eligibility_gate_status=pending` are unchanged.

**Recommended state:** remain paused. **No successor phase is authorized.**

---

## Appendix A — Operator question-by-question index

The twelve operator-supplied questions and the sections of this memo that answer them:

| # | Question | Section(s) |
| - | -------- | ---------- |
| 1 | What does `research_eligible=true` mean for raw aggTrades? | §9.2 (Stage 3 onwards; flips only on a normalized family, never on a raw family) |
| 2 | Single boolean or staged eligibility model? | §9 (staged five-stage ladder; boolean preserved for downstream code) |
| 3 | Minimum source / checksum / manifest / schema / timestamp / monotonicity / duplicate / row-count / symbol-date / archive-integrity / invalid-window checks | §10 (45 enumerated checks across §10.1–§10.12) |
| 4 | What conditions keep `eligibility_gate_status=pending`? | §9.2 (default until gate runs); §10 (any §10 check unverified leaves pending); §15 (any unknown / mixed / stale / partial / ambiguous condition keeps pending) |
| 5 | What conditions make a dataset permanently ineligible? | §13.3 (`.CHECKSUM` permanently absent, archive expired and unobtainable, retroactive governance retirement, etc.) |
| 6 | What conditions require reacquisition? | §13.1 (same-version reacquisition lane: local-side corruption with public bytes unchanged) |
| 7 | What conditions require a new dataset version? | §13.2 (public bytes changed, schema changed, validator replaced, governance contract changed, post-demotion fresh acquisition) |
| 8 | Evidence required before normalization is allowed? | §14.1 (Stage 2 reached + separately authorized normalization-phase memo) |
| 9 | Evidence required before feature computation is allowed? | §14.2 (Stage 3 reached + M0 + Phase 4m 18-requirement gate + Phase 4t 10-dimension matrix) |
| 10 | Evidence required before ML / strategy / backtest is allowed? | §14.3 (Stage 4 reached + strategy-spec memo + backtest-plan memo + separately authorized backtest-execution phase) |
| 11 | Fail-closed rules when eligibility is unknown / mixed / stale / partial / ambiguous? | §15 (six-category fail-closed rule set) |
| 12 | Whether a future code-level eligibility-gate implementation is needed; what it should enforce | §16 Option C (execution plan) and §16 Option D (implementation); §10 + §15 enumerate exactly what such a gate must enforce; §15.6 records the cross-cutting rules a real gate implementation must obey (offline-only, no `research_eligible=true` flip on raw families, no Binance endpoint contact, no WebSocket, no credential) |
