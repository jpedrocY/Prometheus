# Phase 4bb-A — AggTrades Structural Data-Quality Interpretation Memo

**Type:** docs-only data-quality interpretation memo.
**Status:** drafted on branch `phase-4bb-a/aggtrades-structural-data-quality-interpretation`; pending operator review.
**Date:** 2026-05-07.

---

## 1. Phase header

Phase 4bb-A is a docs-only structural QA interpretation memo. It inspects the single Phase 4az BTCUSDT 2025-01-15 aggTrades archive **for structural data quality only**, with no trading research, no descriptive trading statistics, no microstructure features, no normalization, no derived dataset, no flag flip, no successor authorization. The goal is to record — in writing, before any future eligibility-gate execution-plan or implementation phase — whether the one acquired archive is structurally clean, what its observed structural shape is, and what a future eligibility-gate primitive should be careful to test.

Phase 4bb-A is the first activity in the Phase 4ba §16 Option B / Phase 4bb branch family. It does **not** activate Phase 4bb-B (eligibility-gate execution-plan) or Phase 4bb-C (eligibility-gate primitive implementation).

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Branch | `phase-4bb-a/aggtrades-structural-data-quality-interpretation` |
| Base SHA (`main`) | `96d07fd39eafa0a9a39ad790e4a9dce4fe608979` |
| Base parent | `docs(phase-4ba): add merge closeout` |
| Type | docs-only |
| Touches source / tests / scripts? | **No** |
| Touches data / manifests? | **No** (read-only inspection of Phase 4az artefacts only) |
| Touches `data/microstructure/`? | **No write** (`.gitignore:85` continues to apply; nothing under that subtree was modified) |
| Touches retained verdicts? | **No** |
| Touches project locks? | **No** |
| Touches M0 governance? | **No** |
| Authorizes any successor? | **No** |
| Acquires data? | **No** |
| Calls Binance endpoints / opens WebSockets / uses credentials? | **No** |

---

## 3. Inputs reviewed

Phase 4bb-A inspected exactly the four Phase 4az artefacts under the gitignored `data/microstructure/` tree, read-only:

```
data/microstructure/
├── raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/
│   ├── BTCUSDT-aggTrades-2025-01-15.zip
│   └── BTCUSDT-aggTrades-2025-01-15.zip.sha256
└── manifests/
    ├── microstructure_raw_aggtrades_v001__v001.json
    └── microstructure_raw_aggtrades_v001__v001_acquisition_log.json
```

Plus the following committed sources (read-only):

- The Phase 4ba memo and closeout, especially the §10 forty-five-check enumeration and the §15 fail-closed rule list.
- The Phase 4ay authorization memo, especially §10 (19-check integrity gate) and §12 (manifest field contract).
- The Phase 4az acquisition memo, especially §11 (acquisition flow) and §12 (integrity-gate checklist with 18 PASS + 1 NOT_APPLICABLE).
- The Phase 4aw `MicrostructureManifest` data model (`src/prometheus/research/microstructure/manifest.py`).
- The Phase 4ax `validate_aggtrade_payload` validator (`src/prometheus/research/microstructure/aggtrades.py`).

---

## 4. Scope

Phase 4bb-A is **docs-only**. The allowed activities, all of which are structural QA only, are:

- Verify existence of the four Phase 4az artefacts.
- Recompute the on-disk archive SHA256 and compare to the manifest's `files[0].sha256` and the paired `.sha256` sidecar.
- Open the ZIP read-only and confirm it contains exactly one CSV member.
- Decompress in memory only; **no normalised dataset is produced; no derived file is written; no JSONL / Parquet / DuckDB output is created**.
- Iterate the CSV rows once, recording: row count; first / last `T` (`transact_time` ms); count of rows whose `T` falls in `[2025-01-15 00:00:00.000 UTC, 2025-01-16 00:00:00.000 UTC)`; count of rows outside that range; per-UTC-hour row count (structural coverage table only); aggregate trade ID min / max / monotonicity / duplicates / out-of-order count / largest consecutive-ID gap; observed `m` (`is_buyer_maker`) value parity; per-row Phase 4ax `validate_aggtrade_payload` pass/fail count.
- Author this memo and the Phase 4bb-A closeout.
- Apply a narrow `current-project-state.md` update.

The memo and closeout are the only committed deliverables. The structural QA was performed via inline shell commands and Python expressions; no scratch file was committed.

---

## 5. Non-scope

The following are **forbidden** and **not performed** in Phase 4bb-A:

- Compute microstructure features (taker imbalance, sweep detection, aggressive-flow score, spread / depth proxies, slippage proxies, order-flow / execution-quality proxies).
- Compute price returns, alpha, edge, predictiveness, signal quality, profitability, opportunity rate, or any descriptive trading statistic.
- Normalize the dataset. No JSONL, Parquet, DuckDB, feature table, label, or derived dataset.
- Train ML.
- Create a strategy.
- Run backtests.
- Acquire more data (additional UTC days, ETHUSDT, alt symbols, monthly archives, REST polling, WebSocket capture, order-book snapshots, mark-price data).
- Call public endpoints / Binance APIs / private endpoints / WebSockets.
- Use or request credentials.
- Create `.env`, `.mcp.json`, MCP, Graphify.
- Modify `data/microstructure/`, any manifest, or `.gitignore`.
- Flip `research_eligible`. Transition `eligibility_gate_status` out of `pending`.
- Revise retained verdicts.
- Change project locks.
- Amend M0.
- Authorize Phase 4bb-B, Phase 4bb-C, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, or production keys.

---

## 6. Methodology

The structural QA used local read-only access only. It ran inside the project's existing virtual environment. No network call. No credential. No write to `data/microstructure/`.

The on-disk file content was read by Python's standard library (`hashlib`, `zipfile`, `csv`, `json`). Per-row validation imported the existing `prometheus.research.microstructure.aggtrades.validate_aggtrade_payload` from the Phase 4ax skeleton.

The CSV header detection used the same heuristic as the Phase 4az acquisition script: if the first cell of the first row parses as `int`, the file is treated as headerless; otherwise the first row is the header. The Phase 4az acquisition wrote the manifest based on this same heuristic, so re-applying it here is consistent with the acquisition path.

UTC hour bucketing used `(T - UTC_DAY_START) // (3600 * 1000)` against `UTC_DAY_START = 1736899200000` (`2025-01-15 00:00:00.000 UTC`) and `UTC_DAY_END = 1736985600000` (`2025-01-16 00:00:00.000 UTC`).

The aggregate-trade-ID continuity statistics (monotonicity, duplicates, out-of-order, min / max, largest consecutive gap) are structural-only continuity checks. They are not microstructure features and are not used to compute predictive content. The largest consecutive-ID gap is reported as a structural shape observation, not as evidence about market activity.

---

## 7. Structural checks performed

| # | Check | Allowed by brief? | Result |
| - | ----- | ------------------ | ------ |
| 1 | Raw `.zip` path exists | ✓ | PASS |
| 2 | Paired `.sha256` sidecar exists | ✓ | PASS |
| 3 | Manifest exists | ✓ | PASS |
| 4 | Acquisition log exists | ✓ | PASS |
| 5 | `data/microstructure/` gitignored | ✓ | PASS — `.gitignore:85` continues to apply |
| 6 | Recompute on-disk archive SHA256 | ✓ | PASS |
| 7 | Recomputed SHA matches manifest `files[0].sha256` | ✓ | PASS |
| 8 | Recomputed SHA matches sidecar `.sha256` | ✓ | PASS |
| 9 | ZIP contains exactly one CSV member | ✓ | PASS — `BTCUSDT-aggTrades-2025-01-15.csv` |
| 10 | CSV row count equals manifest `event_count` | ✓ | PASS — 1,681,098 / 1,681,098 |
| 11 | First `T` matches manifest `start_time_ms` | ✓ | PASS — 1,736,899,205,109 |
| 12 | Last `T` matches manifest `end_time_ms` | ✓ | PASS — 1,736,985,599,991 |
| 13 | All `T` fall within 2025-01-15 UTC | ✓ | PASS — 1,681,098 in-day; 0 out-of-day |
| 14 | UTC-hour coverage table | ✓ | PASS — see §9 |
| 15 | Aggregate trade IDs monotone non-decreasing | ✓ | PASS — 0 out-of-order events |
| 16 | Aggregate trade ID duplicates | ✓ | PASS — 0 duplicates |
| 17 | Aggregate trade ID min / max | ✓ | PASS — min = 2,516,301,323 / max = 2,517,982,420 |
| 18 | Largest consecutive aggregate-ID gap | ✓ | PASS — gap_max = 1 (perfectly contiguous IDs) |
| 19 | `m` (`is_buyer_maker`) value parity | ✓ | PASS — true: 840,378; false: 840,720; unparsed: 0 |
| 20 | Per-row Phase 4ax `validate_aggtrade_payload` | ✓ | PASS — 1,681,098 / 1,681,098 |
| 21 | Invalid-window discovery | ✓ | PASS — 0 new invalid windows discovered |

**All 21 structural checks PASS.** No anomaly was discovered.

---

## 8. Structural QA findings

The single Phase 4az BTCUSDT 2025-01-15 aggTrades archive is structurally **clean**.

- **Existence and integrity:** all four artefacts (raw `.zip`, paired `.sha256`, manifest, acquisition log) exist on disk under the gitignored `data/microstructure/` tree. The recomputed archive SHA256 matches both the manifest's `files[0].sha256` and the paired `.sha256` sidecar bit-for-bit (`f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`).
- **Single-member ZIP:** the archive contains exactly one CSV member (`BTCUSDT-aggTrades-2025-01-15.csv`, ~111.7 MiB uncompressed).
- **Header form:** the CSV is in *header-row* form (`agg_trade_id,price,quantity,first_trade_id,last_trade_id,transact_time,is_buyer_maker`). The Phase 4az acquisition path's header detection heuristic (numeric-first-cell ⇒ headerless) classifies this archive correctly as headered.
- **Row count parity:** the CSV body row count is exactly `1,681,098`, identical to the manifest's `event_count` and `files[0].event_count`.
- **Timestamp parity:** `first_T = 1,736,899,205,109` (2025-01-15 00:00:05.109 UTC) and `last_T = 1,736,985,599,991` (2025-01-15 23:59:59.991 UTC) match the manifest's `start_time_ms` and `end_time_ms` exactly. Every observed `T` falls within `[2025-01-15 00:00:00.000 UTC, 2025-01-16 00:00:00.000 UTC)`. Zero out-of-day rows.
- **Aggregate trade IDs:** strictly monotone non-decreasing across the file (0 out-of-order events). Zero duplicate IDs. The unique-ID count equals the row count (1,681,098). The ID range `[2,516,301,323, 2,517,982,420]` spans exactly `1,681,097`, and there are `1,681,098` unique IDs, so the file represents a **perfectly contiguous** sequence of aggregate trade IDs (largest consecutive gap = 1). This is reported as a structural shape observation; it is not a microstructure feature and is not used to compute any predictive content.
- **`m` parity:** 840,378 rows have `is_buyer_maker = true`; 840,720 rows have `is_buyer_maker = false`; 0 rows have unparsed `m`. The split is approximately balanced (49.99% true / 50.01% false). This is reported as a structural shape observation; it is not interpreted as evidence about taker imbalance, aggressive flow, or directional bias, and no such feature is computed.
- **Validator pass rate:** 1,681,098 / 1,681,098 rows pass the existing Phase 4ax `validate_aggtrade_payload` (REST-shaped, with the same bool-coercion rules the Phase 4az acquisition uses).
- **No new invalid windows discovered.** No row required `OUT_OF_ORDER_EVENT`, `DUPLICATE_EVENT`, `SYMBOL_MISMATCH`, `ZERO_OR_INVALID_PRICE`, `NEGATIVE_SIZE`, `ARCHIVE_CHECKSUM_MISMATCH`, or any other Phase 4aw `InvalidWindowReason`. The manifest's `invalid_windows` list (`[]`) remains accurate.

---

## 9. UTC-hour coverage table

Per-UTC-hour row count for 2025-01-15. Reported as a structural coverage check only.

| UTC hour | Row count |
| -------- | --------- |
| 00       | 54,706    |
| 01       | 61,632    |
| 02       | 47,890    |
| 03       | 40,807    |
| 04       | 61,602    |
| 05       | 36,182    |
| 06       | 24,297    |
| 07       | 39,536    |
| 08       | 34,011    |
| 09       | 43,697    |
| 10       | 32,415    |
| 11       | 45,092    |
| 12       | 47,996    |
| 13       | 237,550   |
| 14       | 203,987   |
| 15       | 168,756   |
| 16       | 99,087    |
| 17       | 65,110    |
| 18       | 48,357    |
| 19       | 67,375    |
| 20       | 117,212   |
| 21       | 33,762    |
| 22       | 22,490   |
| 23       | 47,549    |

**Structural coverage check only.** Every UTC hour has a non-zero row count; no UTC hour is missing. The peaks at hours 13 / 14 / 15 / 20 are noted as structural shape observations (consistent with US-session trading windows) and are **not** interpreted as evidence about volume regimes, directional bias, microstructure activity, or predictive content. No volume-regime, intraday-pattern, or activity feature is computed from this table.

---

## 10. Aggregate-trade-ID continuity findings

| Item | Value |
| ---- | ----- |
| Row count | 1,681,098 |
| Unique aggregate trade IDs | 1,681,098 |
| Duplicates | 0 |
| Out-of-order events | 0 |
| Monotone non-decreasing | TRUE |
| Min aggregate trade ID | 2,516,301,323 |
| Max aggregate trade ID | 2,517,982,420 |
| ID range span (max − min) | 1,681,097 |
| Largest consecutive-ID gap | 1 |

**Structural continuity is perfect.** The aggregate trade IDs form a contiguous run of 1,681,098 unique values. No `OUT_OF_ORDER_EVENT` is required. No `DUPLICATE_EVENT` is required. The largest consecutive-ID gap is 1, meaning every ID in the inclusive range `[2,516,301,323, 2,517,982,420]` is present in the file exactly once.

**This is a structural observation only.** It is not a microstructure feature, not evidence about exchange engine behaviour, not evidence about volume / liquidity / activity. Any future eligibility-gate primitive can rely on the continuity check as a structural pass; no feature work is licensed by this finding.

---

## 11. Manifest / checksum / sidecar consistency findings

| Item | Manifest value | Recomputed value | Match? |
| ---- | -------------- | ---------------- | ------ |
| `files[0].sha256` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | **YES** (bit-for-bit) |
| Paired `.sha256` sidecar | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | (same) | **YES** (bit-for-bit) |
| `event_count` | 1,681,098 | 1,681,098 | **YES** |
| `files[0].event_count` | 1,681,098 | 1,681,098 | **YES** |
| `start_time_ms` | 1,736,899,205,109 | 1,736,899,205,109 | **YES** |
| `end_time_ms` | 1,736,985,599,991 | 1,736,985,599,991 | **YES** |
| `files[0].start_time_ms` | 1,736,899,205,109 | 1,736,899,205,109 | **YES** |
| `files[0].end_time_ms` | 1,736,985,599,991 | 1,736,985,599,991 | **YES** |
| `file_count` | 1 | 1 | **YES** |
| `dataset_family` | `microstructure_raw_aggtrades_v001` | (n/a; manifest declarative) | declarative |
| `version` | `v001` | declarative | declarative |
| `symbol` | `BTCUSDT` | declarative | declarative |
| `source` | `binance_data_archive` | declarative | declarative |
| `endpoint` | `data.binance.vision/data/futures/um/daily/aggTrades` | declarative | declarative |
| `endpoint_docs_reference` | `https://github.com/binance/binance-public-data#trades (futures aggTrades daily archive convention)` | declarative | declarative |
| `capture_mode` | `historical_archive` | declarative | declarative |
| `schema_version` | `v001` | declarative | declarative |
| `capture_config_hash` | `d7508638b2184f4754900b6f2c2165a9499d5e79d0494600a62516738368010d` | declarative | declarative |
| `code_commit_sha` | `caaad39e40604571758bc58eaac374344c7852e8` | declarative | declarative |
| `invalid_windows` | `[]` | confirmed empty by direct row scan | **YES** |
| `retention_warning` | `null` | (n/a; review-time policy) | acceptable |
| `proxy_warning` | `null` | (n/a; archive is canonical, not proxy) | acceptable |
| `governance_labels.phase` | `4az` | declarative | declarative |
| `governance_labels.source_phase_boundary` | `4ay` | declarative | declarative |
| `governance_labels.validator` | `phase_4ax_aggtrades_v001` | re-applied successfully against 1,681,098 / 1,681,098 rows | **YES** |
| `governance_labels.stop_trigger_domain` | `trade_price_backtest_candidate` | declarative | declarative |
| `governance_labels.symbol_scope_source` | `archive_path` | declarative; consistent with archive path encoding `BTCUSDT` | **YES** (path-encoded) |
| `governance_labels.feature_computation` | `forbidden` | declarative; respected by Phase 4bb-A | **YES** |
| `governance_labels.strategy_use` | `forbidden` | declarative; respected by Phase 4bb-A | **YES** |
| `research_eligible` | `false` | unchanged | **YES** |
| `eligibility_gate_status` | `pending` | unchanged | **YES** |

**No manifest field was modified by Phase 4bb-A.** All declarative fields are echoed for review; all measurable fields (`event_count`, `start_time_ms`, `end_time_ms`, `files[0].sha256`, `invalid_windows`, `file_count`) recompute to the same values.

---

## 12. Invalid-window assessment

Phase 4bb-A did **not** discover any new invalid windows. The manifest's `invalid_windows: []` is accurate. None of the Phase 4aw `InvalidWindowReason` triggers fires for this archive:

- `MISSING_SEQUENCE` — n/a (per-row aggregate-trade-id monotonicity is perfect; no missing IDs in the inclusive range).
- `OUT_OF_ORDER_EVENT` — 0.
- `DUPLICATE_EVENT` — 0.
- `GAP_AFTER_RECONNECT` — n/a (single-shot archive download, no reconnect).
- `SNAPSHOT_MISMATCH` — n/a.
- `CLOCK_SKEW` — n/a.
- `SYMBOL_MISMATCH` — 0 (every row is the path-encoded `BTCUSDT`; the archive path enforces the symbol).
- `STALE_STREAM` — n/a (archive, not stream).
- `STALE_BOOK` — n/a.
- `IMPOSSIBLE_SPREAD` — n/a (no order book; aggTrades).
- `NEGATIVE_SIZE` — 0 (validator confirms `q > 0` on every row).
- `ZERO_OR_INVALID_PRICE` — 0 (validator confirms `p > 0` on every row).
- `ARCHIVE_CHECKSUM_MISMATCH` — 0 (recomputed SHA matches manifest and sidecar bit-for-bit).
- `REST_RETENTION_GAP` — n/a (archive is well within retention; `retention_warning: null`).
- `FORCE_ORDER_PROXY_INCOMPLETENESS` — n/a (not a proxy dataset; `proxy_warning: null`).
- `FAILED_ATOMIC_WRITE` — 0 (acquisition log records clean atomic move; staging tree was cleaned on success).
- `PARTIAL_FILE_RECOVERY_EVENT` — 0 (no recovery procedure ran).

**Conclusion:** the Phase 4az archive carries no integrity events. The `invalid_windows: []` state in the manifest is correct.

---

## 13. What this phase proves

- **The Phase 4az archive is structurally clean.** All 21 structural checks pass. The manifest's measurable fields agree with the on-disk file. The Phase 4ax validator passes on every row. The aggregate-trade-ID sequence is perfectly contiguous. The UTC-hour coverage is non-zero across every hour. Zero new invalid windows were discovered.
- **The Phase 4ay §10 integrity-gate evidence (Phase 4az §12, 18 PASS + 1 NOT_APPLICABLE) survives a re-execution of its measurable subset by an independent process more than 24 hours after the original acquisition run.** Bit-fidelity holds on disk. Manifest and sidecar agree.
- **The Phase 4ba staged eligibility model has at least one structurally-clean candidate to plan against.** Any future Phase 4bb-B execution-plan memo or Phase 4bb-C primitive implementation can use the Phase 4az archive as a worked example for §10 of the Phase 4ba memo.

---

## 14. What this phase does not prove

- **Anything about edge.** No predictive content, no opportunity rate, no microstructure feature viability, no strategy potential, no signal quality, no profitability, no alpha, no opportunity-rate. The acquired dataset remains one symbol's aggregate trades for a single UTC day; no statistical claim is made or licensed.
- **Anything about taker imbalance, sweep activity, aggressive flow, or directional bias.** The 49.99% / 50.01% `m` parity is reported as a structural shape only. It is **not** computed as a feature, **not** interpreted as evidence about market activity, and **not** licensed as input to any future strategy work.
- **Anything about volume regimes or intraday patterns.** The hour-coverage spikes at 13 / 14 / 15 / 20 UTC are reported as structural coverage only. They are **not** computed as a feature and **not** licensed as input to any future strategy work.
- **Reproducibility across re-fetches from the public archive.** Phase 4bb-A did not re-fetch the file; bit-fidelity here means "still on disk after the original acquisition", not "would re-fetch produce the same bytes". Cross-acquisition reproducibility remains an unverified property and is recorded in the Phase 4ba memo §8.
- **Schema parity with the public-data repo across time.** The first row matches a documented header convention; Phase 4bb-A did not audit every published archive variant.
- **Coverage of operational pathologies.** A single quiet day did not exercise: archive splits, vendor outages, exchange maintenance, halts, listing-day partial coverage, late-month archive availability, or `.CHECKSUM` companion absence.
- **The eligibility gate.** No code-level eligibility-gate primitive was implemented. `flip_research_eligible` still always raises. `research_eligible` remains `false`. `eligibility_gate_status` remains `pending`.

---

## 15. Implications for future eligibility-gate planning

A future Phase 4bb-B execution-plan memo and a future Phase 4bb-C primitive implementation, **neither of which is authorized by Phase 4bb-A**, should be careful to test the following — derived from Phase 4ba §10 / §12 / §15 plus the structural QA observations recorded here:

1. **Header detection idempotence.** The Phase 4az acquisition heuristic (numeric first cell ⇒ headerless) classifies this archive as headered. The future eligibility-gate primitive must apply the same heuristic and produce the same result for the same on-disk archive. A primitive that re-reads the archive and *disagrees* with the acquisition path on header form is a fail-closed condition.
2. **Header alias map preservation.** The acquisition path translates `agg_trade_id`, `price`, `quantity`, `first_trade_id`, `last_trade_id`, `transact_time`, `is_buyer_maker` into the Phase 4ax canonical keys `a`, `p`, `q`, `f`, `l`, `T`, `m`. The eligibility-gate primitive must use the same alias map, or fail closed if a new column appears.
3. **Bool coercion contract for `m`.** `true / True / TRUE` ⇒ `True`; `false / False / FALSE` ⇒ `False`. Any other string value is a fail-closed condition. The structural QA observed exactly two distinct string values (`true`, `false`); the primitive must not silently broaden this set.
4. **SHA bit-fidelity.** The recomputed SHA must match both the manifest `files[*].sha256` and the paired `.sha256` sidecar. A two-way agreement is required; sidecar-only or manifest-only is a fail-closed condition.
5. **`.CHECKSUM` companion governance.** The Phase 4az acquisition matched a published `.CHECKSUM` companion; the manifest does not need a `governance_labels.checksum_companion_absent` annotation. Future archives without a published `.CHECKSUM` must either fail closed at the eligibility gate (per Phase 4ba §10.2) or carry the explicit governance label, per a separately authorized governance memo.
6. **Aggregate-trade-ID range and continuity.** The eligibility-gate primitive should verify monotone non-decreasing `a`, zero duplicates, and (optionally) record the largest consecutive-ID gap. The Phase 4az archive shows a `gap_max = 1` (perfect contiguity), which is the structural shape an eligibility gate should *not* require for all future archives — multi-hour quiet windows in alt-symbol or low-volume archives may produce larger consecutive-ID gaps without indicating an integrity event. The check is *monotonicity + uniqueness*, **not** *gap_max == 1*.
7. **UTC-day boundary discipline.** Every observed `T` must fall in `[UTC_DAY_START, UTC_DAY_END)` for a daily archive. The boundary is half-open at the next day's midnight. The Phase 4az archive's `last_T = 1736985599991` (2025-01-15 23:59:59.991 UTC) — 9 ms before the boundary — is acceptable. The primitive should treat any row at exactly `UTC_DAY_END` as a fail-closed condition.
8. **Hour coverage as structural QA, not feature.** The eligibility-gate primitive may *report* per-hour row counts in its gate report, but it must not condition `eligibility_gate_status=pass` on volume-regime-shaped thresholds derived from the counts. Hour-coverage thresholds (e.g. "fail if any hour has zero rows") would conflate structural QA with implicit edge claims.
9. **`m` parity reporting.** The primitive may report the true / false split, but it must not condition pass on a parity range (e.g. "fail if true-fraction outside [0.4, 0.6]"). Such a check would be a hidden feature, not a structural QA. The structural QA on Phase 4az observed approximately 50/50; future archives may legitimately show different ratios for symbol-specific or day-specific reasons that are out of scope for the eligibility gate.
10. **Validator round-trip.** The primitive must re-apply Phase 4ax `validate_aggtrade_payload` on every row, with the bool-coerced `m` value, and require 100% pass. A single failure is a fail-closed condition (Phase 4ba §15.2 mixed-state rule: per-row PASS does not yield manifest-level PASS, and the converse holds: a single per-row FAIL fails the manifest).
11. **Manifest immutability during gate-time.** The gate primitive must not modify the existing manifest file. Per Phase 4ba §15.6, the gate may only append a gate report log under a future `data/microstructure/gate-reports/` namespace. Any manifest modification (including a `research_eligible` flip) requires a separate, separately authorized future eligibility-gate primitive, which Phase 4bb-A does **not** authorize.
12. **Path-encoded symbol enforcement.** The Phase 4az archive's `governance_labels.symbol_scope_source = "archive_path"` records that the symbol is enforced by the archive path (`.../BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`). The gate primitive must verify that the path-encoded symbol matches the manifest's `symbol` field. Phase 4bb-A confirms this match for the Phase 4az archive.
13. **`invalid_windows` post-acquisition discovery.** If the eligibility-gate primitive ever discovers invalid windows post-acquisition that were not in the manifest, the response must be either (a) fail closed and recommend re-acquisition under the same version (per Phase 4ba §13.1) if local-side corruption is suspected, or (b) fail closed and recommend a new dataset version (per Phase 4ba §13.2) if the upstream bytes are believed to have changed. It is **not** acceptable to silently amend the manifest.

These thirteen items are recommendations to Phase 4bb-B / Phase 4bb-C planners; they are not new locks, not new governance, and not amendments to the Phase 4ba §10 forty-five-check enumeration. The Phase 4ba §10 enumeration remains the binding contract; the items above are application-time observations grounded in the Phase 4az archive shape.

---

## 16. Preserved boundaries

- **No data was modified.** The four Phase 4az artefacts under `data/microstructure/` are byte-identical to their post-Phase-4az state. The Phase 4az manifest mtime is the original `May 7 21:55`.
- **`data/microstructure/` remains gitignored.** `git check-ignore -v` returns `.gitignore:85:data/microstructure/	data/microstructure/`. Nothing under that subtree is staged or tracked.
- **`research_eligible` remains `false`.** Verified by direct inspection of the manifest after the structural QA.
- **`eligibility_gate_status` remains `pending`.** Same verification.
- **No acquisition.** No HTTP request, no `data.binance.vision` fetch, no Binance API call, no WebSocket, no credential, no `.env`, no `.mcp.json`, no MCP, no Graphify.
- **No normalization.** No JSONL, no Parquet, no DuckDB, no derived dataset.
- **No features.** No metric, no ratio, no transform, no aggregation, no descriptive trading statistic.
- **No ML.** No label, no model, no embedding, no calibration, no fit.
- **No strategy.** No candidate, no entry rule, no exit rule, no threshold, no signal.
- **No backtest.**
- **No source / test / script change.** Phase 4bb-A modifies only `docs/00-meta/...` paths.
- **No retained verdict revised.**
- **No project lock loosened.**
- **No M0 governance amended.**
- **No successor phase authorized.**
- **No scratch script committed.** The structural QA was performed via inline shell + Python; nothing under `scripts/` or any tracked path was added or modified.

---

## 17. Recommended future options

Phase 4bb-A does not authorize any successor. The following are recorded for operator evaluation only.

### Option A — Remain paused (primary)

Procedurally clean. Preserves every retained verdict and every project lock. The Phase 4az archive is structurally clean and the Phase 4ba eligibility-gate model is on record; no further microstructure work is required until the operator separately authorizes it.

### Option B — Future docs-only Phase 4bb-B eligibility-gate execution-plan memo (conditional next)

**Allowable; not authorized.**

A future docs-only memo would translate the Phase 4ba §10 forty-five-check enumeration into a precise file-by-file implementation plan (file layout, function signatures, fail-closed branches, gate-report schema, manifest-update primitive, demotion path) without writing code. The Phase 4bb-A structural QA observations recorded in §15 above can serve as application-time grounding for the Phase 4bb-B memo.

### Option C — Future docs-and-code Phase 4bb-C eligibility-gate primitive implementation (conditional later)

**Allowable; not authorized.**

A future docs-and-code phase would implement the eligibility-gate primitive as a standalone offline tool that reads the manifest + raw `.zip` + `.sha256` sidecar + acquisition log, runs every §10 check, produces a gate report under `data/microstructure/gate-reports/`, and (optionally) writes a successor manifest with `eligibility_gate_status=pass` or `fail`. This phase would replace `flip_research_eligible(...)` with a real gate-controlled mutation primitive on a raw-family manifest. It must remain offline-only, must not call any Binance endpoint, must not flip `research_eligible=true` for raw families, and must not authorize features / ML / strategy / backtest.

### Forbidden

- Acquire additional aggTrades data.
- Compute features / train ML / build strategy.
- Flip `research_eligible` to `true` on any raw family.
- Authorize Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / exchange-write / production keys.

---

## 18. Closeout / lock preservation

Phase 4bb-A preserves verbatim:

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
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az and reaffirmed by Phase 4ba; structural QA confirmed by Phase 4bb-A).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance).
- Phase 4j §11 (OI subset governance).
- Phase 4ak — M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al — refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay, Phase 4az, Phase 4ba results — all preserved verbatim.

No new lock is introduced. No existing lock is loosened. M0 admissibility and the post-null cooldown rule remain binding prospectively for any future research lane. The Phase 4az dataset's `research_eligible=false` and `eligibility_gate_status=pending` are unchanged.

**Recommended state:** remain paused. **No successor phase is authorized.**
