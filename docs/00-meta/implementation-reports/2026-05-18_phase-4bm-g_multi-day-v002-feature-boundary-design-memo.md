# Phase 4bm-G — Multi-Day V002 Feature-Boundary Design Memo

**Phase identity:** Phase 4bm-G — Multi-Day V002 Feature-Boundary Design Memo (docs-only).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-g/multi-day-v002-feature-boundary-design-memo`.
**Base:** `main` at `bc7fa817ec712d296f9cd88dec89136b818edcbd` (Phase 4bm-F merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** Tier 1 (docs-only Full Phase; governance / boundary-design memo; multi-day v002 analogue of Phase 4bh-A and the Phase 4bh-B schema-finalization layer it eventually fed).
**Phase type:** docs-only feature-boundary design memo — adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`. No source / test / script / configuration / data / manifest / sidecar / gate-report / successor-state file is modified. No feature artefact is created.
**Status:** drafted; pending operator review.

---

## 1. Phase identity and scope

This memo defines the feature boundary that any future multi-day v002 feature work on the Stage-3 successor-state-marked normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events) must respect before any v002 feature-computation phase is authorized. It is **docs-only**: no feature is computed, no feature dataset is written, no feature manifest is created, no feature successor-state artefact is created, no source code or test or script is added or modified, no data is acquired, no endpoint is contacted, no credential is read, and no successor phase is authorized.

**Feature-boundary design is not feature computation.** **Stage-4 is not authorized by Phase 4bm-G.** **Phase 4bm-H is not authorized by Phase 4bm-G.** **No v002 feature artefact exists after Phase 4bm-G.**

The memo is the multi-day v002 analogue of the Phase 4bh-A v001 feature-boundary design memo (and, where appropriate, of the Phase 4bh-B v001 feature schema finalization memo). It records the canonical v002 input, the forbidden inputs, the proposed v002 feature-family naming, the v002 feature-stage model, definitions of feature / label / signal / feature-computation, the allowed and forbidden v002 feature classes, the temporal-leakage boundary, the windowing / aggregation / precision / type / missing-window / multi-day-partition policies, the proposed v002 output namespace and feature manifest schema, the future validation gate sequence, the M0 admissibility boundary, the cooled-down lane boundary, the ML / strategy / backtest boundary, the acquisition boundary, the acceptance criteria for any future v002 feature implementation phase (Phase 4bm-H), and the fail-closed rules.

The Phase 4ak twelve-clause M0 mechanism-admissibility gate, the post-null cooldown rule, the cooled-down families list, the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant, the Phase 4bb-F canonical path policy, the Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks, the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard, every retained verdict, and every project lock are preserved verbatim by this phase.

---

## 2. Current v002 lifecycle state through Stage-3

The multi-day v002 derived family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3:

| Stage | Name | v002 phase | Verdict / Output |
| ----- | ---- | ---------- | ---------------- |
| Stage-0 | acquired + normalized | Phase 4bm-B Multi-Day Normalization Implementation | 90 per-day Parquets + 90 sidecars + v002 multi-day index manifest (gitignored; not committed) |
| Stage-1 | inspected | Phase 4bm-C Multi-Day Normalized Structural QA Memo | 56 / 56 PASS (read-only structural QA) |
| Stage-2 | gate-passed at report level | Phase 4bm-D Multi-Day Derived-Family Eligibility Gate | 60 / 60 PASS; `gate_verdict = DERIVED_GATE_PASS`; 19 / 19 boundary confirmations `True`; `research_eligible_after = False`; `eligibility_gate_status_after = "pass"` (report-level only); `no_successor_authorization = True` |
| Stage-2-decision | policy-level Stage-3 admissibility | Phase 4bm-E Multi-Day Derived-Family Research-Eligibility Decision Memo | Option B / Decision form 2: Stage-3 admissible in principle at policy level; no manifest mutation |
| Stage-3 | machine-readable successor-state marker | Phase 4bm-F Multi-Day Derived-Family Successor-State Recording | sibling successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (SHA `72b6edd4…`) + paired canonical Phase 4bb-F sidecar (SHA `1e9ffb23…`); both gitignored; not committed |

The actual on-disk v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (SHA `01c5fa53…`) **still carries `research_eligible = false` and `eligibility_gate_status = "pending"`** byte-identically. The actual on-disk v002 raw manifest, the v001 derived manifest, and the v001 raw manifest are all also unchanged with `research_eligible=false / eligibility_gate_status="pending"`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end and has never been invoked.

The successor-state JSON's `successor_research_eligible: true` is the **only** machine-readable Stage-3 marker for the v002 derived family. Any future tool that wishes to interpret the v002 derived family as Stage-3 must read this successor-state artefact, not the original manifest.

---

## 3. Stage-4 remains unauthorized

Stage-4 (feature-cleared) is **not** authorized by Phase 4bm-G for the v002 derived family. Phase 4bm-G reaches **v002 Feature Stage-0** only (feature schema designed on paper; no code, no data, no artefact). The transition from v002 Stage-3 (Phase 4bm-F machine-readable successor-state marker) to v002 Stage-4 (feature-cleared) requires, in this order:

1. a separately authorized future multi-day v002 feature schema finalization memo (if separately required by the operator; the multi-day analogue of Phase 4bh-B; not authorized by Phase 4bm-G);
2. a separately authorized future multi-day v002 feature implementation phase (**Phase 4bm-H**; multi-day analogue of Phase 4bh; not authorized by Phase 4bm-G);
3. a separately authorized future multi-day v002 feature artefact structural QA memo (multi-day analogue of Phase 4bi-A; not authorized);
4. a separately authorized future multi-day v002 feature-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bi-B; not authorized);
5. a separately authorized future multi-day v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C; not authorized);
6. a separately authorized future multi-day v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D; not authorized).

Each transition requires its own operator authorization under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

---

## 4. Linkage to Phase 4bm-F successor-state JSON

Phase 4bm-G treats the multi-day v002 derived family as Stage-3 **only** via the Phase 4bm-F successor-state artefact at:

```text
data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
```

with the following authoritative properties (verified locally at the start of Phase 4bm-G):

- SHA256: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9`
- Paired Phase 4bb-F sidecar at `<json>.sha256`; sidecar SHA256: `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97`
- `successor_state_kind: "research_eligibility_successor_state"`
- `successor_stage: "Stage-3"`
- `successor_research_eligible: true`
- `successor_eligibility_gate_status: "pass"`
- `stage_3_policy_admissible: true`
- `research_eligible_successor_state: true`
- `original_manifest_research_eligible: false`
- `original_manifest_eligibility_gate_status: "pending"`
- `original_manifest_byte_identical: true`
- `phase_4bm_e_decision: "Option B / Decision form 2"`
- `stage_4_feature_cleared: false`
- `no_successor_authorization: true`
- All 43 fields in `boundary_confirmations` block: `true`

Any future v002 feature implementation phase (the hypothetical Phase 4bm-H) **must** cite this Phase 4bm-F successor-state JSON SHA `72b6edd4…` verbatim inside its future v002 feature manifest, **must** refuse to interpret the original v002 derived multi-day index manifest alone as Stage-3, and **must** preserve the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.

---

## 5. Upstream lineage table — required v002 SHAs

Any future v002 feature-implementation phase must cite, by SHA256, the following upstream lineage artefacts. Each SHA was verified on disk at the start of Phase 4bm-G against the values recorded in the Phase 4bm-D / Phase 4bm-D-P1 / Phase 4bm-E / Phase 4bm-F merge-closeouts.

| Artefact | Path | SHA256 |
| -------- | ---- | ------ |
| v002 derived multi-day index manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| v002 raw manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D-R raw multi-day PASS gate report | `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| Phase 4bl-E raw multi-day successor-state JSON | `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| Phase 4bm-D authoritative derived-family gate report | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| Phase 4bm-D authoritative sidecar | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json.sha256` | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` |
| **Phase 4bm-F v002 successor-state JSON (Stage-3 marker)** | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| Phase 4bm-F v002 successor-state sidecar | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256` | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` |

v002 scope details (recorded for downstream feature-implementation phases):

- `dataset_family`: `microstructure_normalized_aggtrades_v001`
- `dataset_version`: `v002`
- Symbol scope: BTCUSDT (single symbol).
- UTC date scope: 90 contiguous UTC dates `2024-12-01 .. 2025-02-28` inclusive.
- Total event count across the 90 days: **155,153,449** events.
- Approximate total per-day Parquet footprint: ~1.40 GiB across 90 per-day Parquet files.
- v002 derived multi-day index manifest's `research_eligible` / `eligibility_gate_status`: `false` / `"pending"` (immutable; the original manifest is preserved byte-identically across Phase 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F).

v001 cross-reference (for historical-precedent reasoning only; does **not** transitively authorize v002 work):

- v001 derived manifest: `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`, SHA256 `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`; `research_eligible=false`; `eligibility_gate_status="pending"`.
- Phase 4bg-B v001 derived successor-state JSON: SHA256 `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`.

---

## 6. Comparison to Phase 4bh-A / Phase 4bh-B v001 feature-boundary precedent

Phase 4bm-G is the multi-day v002 analogue of the Phase 4bh-A v001 feature-boundary design memo (with elements of Phase 4bh-B v001 feature schema finalization included for completeness in a single docs phase). The two precedents differ along the following dimensions that materially affect the v002 boundary:

| Dimension | Phase 4bh-A / Phase 4bh-B (v001 precedent) | Phase 4bm-G (this memo; v002) |
| --------- | ------------------------------------------- | ------------------------------ |
| `dataset_version` of canonical input | `v001` | `v002` |
| Symbol scope | BTCUSDT (single symbol) | BTCUSDT (single symbol) |
| Date scope | 1 UTC day (`2025-01-15`) | **90 contiguous UTC days (`2024-12-01 .. 2025-02-28`)** |
| Event count | 1,681,098 | **155,153,449 (~92× scale-up)** |
| Stage-3 marker SHA cited | Phase 4bg-B (`8bcc7d01…`) | **Phase 4bm-F (`72b6edd4…`)** |
| Source manifest SHA cited | v001 derived (`f6f0d947…`) | **v002 derived multi-day index (`01c5fa53…`)** |
| Source derived gate report SHA cited | Phase 4bf v001 (`dd4e0c1c…`) | **Phase 4bm-D v002 (`3b45e70b…`)** |
| Source raw lineage | Phase 4bb-D v001 raw gate (`96f09159…`) + v001 raw manifest (`a371edd4…`) | **Phase 4bl-D-R v002 multi-day raw gate (`f9493fd1…`) + Phase 4bl-E v002 raw successor-state (`a0576ca6…`) + v002 raw manifest (`01696786…`) + v002 acquisition log (`52f6d7fb…`)** |
| Per-day partitioning required | not applicable (one day) | **mandatory (90 per-day Parquets; cross-day window handling required)** |
| Boundary windows that may need prior-day lookback | not applicable | **must be handled explicitly; see §16** |
| Per-day warm-up / incomplete-window handling | not applicable | **must be handled explicitly; see §16** |
| Per-day `invalid_windows` propagation | one day | **across all 90 days, each per-day Parquet must propagate its own invalid-window state if any (currently all `[]` per Phase 4bm-D)** |
| Cross-symbol coverage | none | **none (unchanged from v001; closing this gap requires separately authorized acquisition)** |

The v002 evidence base is strictly broader and stronger than v001 along every dimension v002 measured; nothing v002 measured is weaker than v001. The cross-symbol gap is unchanged.

---

## 7. Phase 4bh-A / Phase 4bh-B v001 feature-boundary does NOT transitively authorize v002

The Phase 4bh-A v001 Feature-Boundary Design Memo and the Phase 4bh-B v001 Feature Schema Finalization Memo are **v001-specific**:

- They cite the Phase 4bd v001 normalized Parquet SHA `2b3d6978…` verbatim.
- They cite the Phase 4bg-B v001 successor-state JSON SHA `8bcc7d01…` verbatim.
- They cite the Phase 4bf v001 derived gate report SHA `dd4e0c1c…` verbatim.
- They predeclare a v001-only future feature family `microstructure_features_aggtrades_v001` `dataset_version = v001`.
- They were authored before the Phase 4bm-* multi-day v002 evidence chain existed.

These v001 feature-boundary memos do **not** transitively cover v002. Any future v002 feature work requires this Phase 4bm-G memo (the multi-day v002 analogue) and a separately authorized v002 feature implementation phase (Phase 4bm-H or equivalent). Authorisation for v001 feature work, if ever granted, would not by itself authorise v002 feature work.

---

## 8. Proposed future v002 feature family name and versioning convention

Proposed (NOT created by this memo):

- **Feature family name:** `microstructure_features_aggtrades_v001`
- **Feature dataset version (for v002 inputs):** `v002` (matches the convention used by the Phase 4bm-B / 4bm-C / 4bm-D / 4bm-E / 4bm-F v002 chain — i.e., the `dataset_family` is preserved across input versions; only `dataset_version` changes).
- **Relationship to input:** **sibling derived family**, not a mutation of `microstructure_normalized_aggtrades_v001` / `v002`. The normalized derived family is never overwritten by feature work.
- **Schema versioning:** an explicit `feature_schema_version` field (initial value `v001`) must be carried inside any future v002 feature manifest. A future schema change requires an explicit `feature_schema_version` bump.
- **Config versioning:** an explicit `feature_config_hash` (deterministic SHA256 over the canonical-JSON serialization of the feature config) must be carried inside any future v002 feature manifest. Feature manifest entries that differ only in `feature_config_hash` are distinct.

The full proposed identity for the future v002 feature family is:

- `dataset_family = "microstructure_features_aggtrades_v001"`
- `dataset_version = "v002"`
- `feature_schema_version = "v001"` (default; bump on any schema change)

No directory, manifest, or file is created by Phase 4bm-G. The naming convention is design-only.

---

## 9. Proposed future v002 feature manifest naming convention

Proposed (NOT created by Phase 4bm-G):

- **Path:** `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`
- **Paired Phase 4bb-F sidecar:** `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json.sha256`
- **Format of the sidecar (canonical Phase 4bb-F):** `<sha256_lowercase_hex><two ASCII spaces><basename><LF>`

Neither the future v002 feature manifest nor its sidecar exists. Phase 4bm-G does not create either. Verified on disk: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` does not exist (no file is present at that path; this memo does not create one).

---

## 10. Proposed future v002 feature parquet path convention

Proposed (NOT created by Phase 4bm-G):

- **Output namespace:** `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`
- **Per-day file pattern:** `<SYMBOL>-features-aggtrades-<YYYY>-<MM>-<DD>.parquet`
- **Example future per-day file (NOT created):** `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2024/12/BTCUSDT-features-aggtrades-2024-12-01.parquet`
- **Paired Phase 4bb-F sidecar (NOT created):** same path + `.sha256` suffix; canonical sidecar format.

For the v002 input scope (90 contiguous UTC dates 2024-12-01 .. 2025-02-28 inclusive, single symbol BTCUSDT), the future implementation phase would emit **exactly 90 per-day feature Parquets + 90 paired Phase 4bb-F sidecars**, one per `(symbol, utc_date)` partition, mirroring the v002 Phase 4bm-B per-day normalized Parquet partitioning. The `data/microstructure/features/` namespace does **not** exist as of Phase 4bm-G; no directory is created.

---

## 11. Proposed feature schema design

Proposed (NOT created by Phase 4bm-G). The future v002 feature schema, if ever implemented, must include the following column roles. Exact column names, dtypes, and final feature counts are deferred to a future schema-finalization step (or fixed within the Phase 4bm-H implementation memo if the operator chooses to collapse).

### 11.1 Lineage columns (required on every future feature row)

- `dataset_family` (string, constant: `"microstructure_features_aggtrades_v001"`)
- `dataset_version` (string, constant: `"v002"`)
- `feature_schema_version` (string, e.g. `"v001"`)
- `source_dataset_family` (string, constant: `"microstructure_normalized_aggtrades_v001"`)
- `source_dataset_version` (string, constant: `"v002"`)
- `source_normalized_manifest_sha256` (string, constant: `"01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"`)
- `source_normalized_parquet_per_day_sha256` (string, the SHA256 of the specific Phase 4bm-B per-day Parquet that this feature row is derived from; varies by `utc_date`)
- `source_successor_state_sha256` (string, constant: `"72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"` — the Phase 4bm-F successor-state JSON SHA)
- `source_phase_4bm_d_gate_report_sha256` (string, constant: `"3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a"`)
- `source_phase_4bm_e_decision` (string, constant: `"Option B / Decision form 2"`)
- `feature_config_hash` (string; deterministic SHA256 over canonical-JSON serialization of the feature config used to produce the row)

### 11.2 Timestamp columns

- `feature_timestamp_ms` (`int64`; UTC ms; the feature row's evaluation timestamp `T`)
- `source_transact_time_ms` (`int64`; UTC ms; copied from the source aggTrade row when feature rows are event-aligned)

The exact rule mapping source rows to feature timestamps is fixed by the timestamp / leakage policy in §14.

### 11.3 Source row identity columns (required for traceability)

- `symbol` (string, e.g. `"BTCUSDT"`)
- `utc_date` (string, ISO `YYYY-MM-DD`; matches the per-day partition)
- `agg_trade_id` (`int64`; copied from source when event-aligned)
- `row_index` (`int64`; per-day source row index; copied from source when event-aligned)

### 11.4 Non-feature normalized columns retained or referenced

The future v002 feature schema **must not** silently overwrite or drop information from the 19-column Phase 4bc / Phase 4bm-A canonical normalized schema. Either: (a) the future feature row carries the lineage columns above plus computed feature columns and references the source per-day Parquet via `source_normalized_parquet_per_day_sha256` (the recommended approach; smaller feature files); or (b) the future feature row carries enough columns of the source row to be self-traceable. The exact choice is fixed in the future v002 feature schema finalization step. **No source column may be silently lossily-transformed (e.g., `price` Decimal-as-string → float) in the feature output.**

### 11.5 Allowed computed feature columns (design candidates)

See §12 for the allowed feature categories. Exact column names and counts are deferred. As a design heuristic (drawing on the Phase 4bh-B v001 precedent of ~45 windowed features × 4 windows = 40 columns + ~5 context / data-quality columns = ~45 feature columns), the future v002 schema is expected to expose roughly the same order of magnitude of features per row. The exact count, window list, and column list are deferred to the future v002 schema-finalization step.

### 11.6 Forbidden columns (binding)

See §13 for the full forbidden list. The future v002 feature schema **must** include a static substring-detector validator that fails closed if any computed column name (lowercased) contains any of the forbidden tokens listed in §13.

---

## 12. Allowed future v002 feature categories

The memo proposes the following first-pass feature *categories* as design candidates for the future v002 feature implementation. **No feature is approved for computation by Phase 4bm-G.** Each category is bounded to microstructure-descriptive features computed only from data at or before the feature timestamp `T`.

### A. Event count / trade count aggregates over predeclared trailing windows

- Rolling aggTrade count: count of source aggTrade rows whose `transact_time_ms` falls inside a predeclared trailing window `(T - window_ms, T]`.
- Rolling unique aggTrade ID span (`last_trade_id - first_trade_id` summed across the window; proxy for the raw-tape trade count subsumed by aggregation).
- Rolling event rate: `rolling_aggtrade_count / window_seconds`.

### B. Buy/sell aggressor imbalance derived only from past and current rows

- Rolling aggressive-buy quantity: sum of `quantity` over source events with `is_buyer_maker = false` in the trailing window.
- Rolling aggressive-sell quantity: sum of `quantity` over source events with `is_buyer_maker = true` in the trailing window.
- Rolling aggressive-buy count / rolling aggressive-sell count: count variants.
- Rolling aggressive-flow ratio: `rolling_aggressive_buy_quantity / (rolling_aggressive_buy_quantity + rolling_aggressive_sell_quantity)`; explicit divide-by-zero handling (proposed default: NaN if denominator == 0; never imputed).
- Rolling aggressive quantity imbalance: `rolling_aggressive_buy_quantity − rolling_aggressive_sell_quantity`.

Per the Phase 4bc canonical schema, the Binance aggTrades aggressor-side rule is: `is_buyer_maker = false` ⇒ aggressive BUY; `is_buyer_maker = true` ⇒ aggressive SELL.

### C. Volume / notional aggregates

- Rolling quantity sum: sum of `quantity` (Decimal-as-string parsed to Decimal) over the trailing window.
- Rolling quantity mean / rolling quantity median: descriptive central-tendency metrics over the trailing window.
- Rolling notional sum: sum of `quantity * price` over the trailing window (Decimal arithmetic; explicit precision policy in §15).
- Rolling large-trade count: count of source aggTrades whose `quantity` exceeds **predeclared** size thresholds. Thresholds must be predeclared and **not** fitted on the same dataset / evaluation period.

### D. Price movement / signed-price-change descriptors computed without future leakage

- Rolling log-return over the trailing window: `log(price_at_T / price_at_T_minus_window)` using only the last source row with `transact_time_ms <= T` and the last source row with `transact_time_ms <= T - window_ms`. Null if no prior reference price.
- Rolling realized volatility: estimator (e.g., sum of squared log returns) computed only from past / current observations within the trailing window.
- Rolling open / high / low / close over the trailing window: descriptive OHLC-like rollups computed only from rows in the trailing window. No carry of future prices; no resampling that synthesizes prices outside observed events.
- Rolling signed-price-change indicators: ratios / differences of `price` between past observations within the window.

### E. Inter-arrival / activity-rate descriptors

- Rolling mean inter-arrival time: mean of `transact_time_ms` differences between consecutive source events within the trailing window.
- Rolling inter-arrival standard deviation: standard deviation of inter-arrival times within the window.
- Rolling activity-burst indicator: ratio of events in the latest sub-window to events in the trailing window.

### F. Rolling-window descriptive features using only data at or before the row timestamp

- All of the above are rolling-window descriptive features. No centered or future-looking window is allowed.

### G. Time-of-day context (deterministic from `transact_time_ms`)

- `utc_hour` (`int8`, 0..23) derived from `transact_time_ms`.
- `utc_minute` (`int8`, 0..59).
- `milliseconds_since_day_start` (`int32`, non-negative).

### H. Data-quality / coverage features

- `invalid_window_flag` (`bool`) propagated from the per-event invalid-window propagation (all `false` across the 90 v002 days per Phase 4bm-D's `len(invalid_window_candidates) = 0`; this flag becomes meaningful only if a future acquisition produces non-empty invalid windows).
- `rolling_missing_window_flag` (`bool`) — `true` if any trailing window of any size intersects an invalid window.
- `rolling_event_count_coverage_ratio` — `actual_events_in_window / expected_events_in_window` if "expected" can be deterministically defined; otherwise omitted.

**No category outside A–H is approved by Phase 4bm-G.** Any future category requires a separately authorized future memo.

---

## 13. Forbidden feature categories

The future v002 feature implementation phase **must** forbid the following, regardless of how the feature is named:

- future returns (any feature using `transact_time_ms > T`);
- next-window price movement (forward-looking);
- future high / low / close;
- future realized volatility;
- future volume;
- labels (target columns for evaluation or ML training);
- targets;
- strategy signal columns;
- entry / exit decisions;
- backtest outputs;
- PnL;
- MFE / MAE;
- R-multiple;
- equity curve;
- position state;
- predictions / probabilities / model scores;
- decision scores;
- mark-price-derived columns unless separately authorized;
- order-book / funding / OI / liquidation / cross-venue features unless separately authorized;
- ML embeddings;
- learned representations;
- any column requiring future data;
- features that use the full-day distribution to normalize intraday points unless the normalization is explicitly causal (uses only past / current data);
- z-scores using future data;
- thresholds fitted on the same evaluation period without an explicit train-only fitting policy;
- any feature whose explicit purpose is to revise or rescue a previously rejected strategy verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1, or any other retained verdict).

**Forbidden-substring detector (binding on the future implementation):** the future v002 feature implementation **must** fail closed at validation time if any output column name (lowercased) contains any of the following tokens:

```text
label, target, future, signal, entry, exit, pnl, profit, loss, mfe, mae,
r_multiple, equity, position, alpha, edge, prediction, model, score,
decision, strategy, liquidation, funding, open_interest, order_book,
mark_price
```

This list is a defensive name-based guardrail and is not exhaustive of semantic forbidden cases; semantic forbiddance per the categories above is the binding contract.

---

## 14. Timestamp and leakage policy

Binding on any future v002 feature implementation:

- **UTC only.** Every timestamp is UTC ms `int64`. No local timezone; no DST; no clock drift; no rounding to local time.
- **No future-looking windows.** A feature row at time `T` may use **only** source aggTrade rows with `transact_time_ms <= T`.
- **Explicit closed / open interval convention.** Trailing windows are defined as `(T - window_ms, T]` — left-open, right-closed at `T`. The single-point window at `T` includes the row(s) whose `transact_time_ms == T`.
- **Row timestamp availability.** The feature timestamp `T` of each feature row is `source_transact_time_ms` (i.e., event-aligned by default). Alternative cadences (e.g., fixed 1-second offsets) may be defined in a future schema-finalization step but must remain deterministic, reproducible from inputs alone, and free of future information.
- **Deterministic sorting.** Source rows must be sorted by `(transact_time_ms ASC, row_index ASC)` before any windowing computation. The Phase 4bm-B per-day Parquets already carry contiguous per-day `row_index` starting at 0; this is the canonical ordering key.
- **Same-timestamp handling rule.** When multiple source rows share the same `transact_time_ms`, the tie is broken by `row_index ASC`. This rule **must** be covered by future tests.
- **Per-day boundary handling.** Each per-day output Parquet covers exactly one UTC day; rows are restricted to `transact_time_ms ∈ [day_start_ms, day_end_ms)` where `day_end_ms = day_start_ms + 86_400_000`. The half-open UTC day convention from Phase 4bm-A / Phase 4bm-B / Phase 4bm-D is honoured.
- **Multi-day rolling-window boundary handling.** A trailing window at `T` whose left endpoint `T - window_ms` falls before `day_start_ms` may require **prior-day lookback**. Three policies are admissible (the future v002 schema finalization step must select exactly one and freeze it):
  1. **Causal cross-day lookback.** Load the trailing tail of the prior day's Parquet sufficient to cover the maximum window; emit fully populated feature rows for every event in the current day except where the prior day is missing (e.g., day 1, the first day of the v002 range, has no prior day — feature rows whose window crosses the day boundary must carry `rolling_missing_window_flag = true` and the affected aggregates must be null or zero per the null policy in §15).
  2. **Per-day-only computation with warm-up flagging.** Compute features using only the current-day Parquet; rows in the early portion of the day whose trailing window would have extended into the prior day carry `rolling_missing_window_flag = true` and the affected aggregates are null per the null policy. This is simpler and avoids cross-day I/O but produces fewer fully-populated feature rows near each day boundary.
  3. **Hybrid.** Compute per-day-only for short windows (e.g., ≤ 60 s); use causal cross-day lookback for longer windows (e.g., > 60 s).
  The recommended default is policy (1) — causal cross-day lookback — for maximum coverage with no future leakage, but the choice is deferred to the future schema-finalization step.
- **No centered windows.** Centered windows that look both backward and forward in time are **forbidden**.
- **No full-day distribution-based normalization** unless explicitly causal (uses only past / current data).
- **All train / validation / OOS / evaluation splits are future work** — not part of Phase 4bm-G, not part of any future Phase 4bm-H implementation, and not part of any future v002 feature schema-finalization memo (see §17).
- **Label construction is forbidden** and must be a later separately authorized phase under M0 admissibility.

---

## 15. Decimal / precision policy

Binding on any future v002 feature implementation:

- `price` and `quantity` in the source Phase 4bc canonical schema are Decimal-as-string. The future v002 feature implementation **must** parse these using Python `Decimal` for intermediate exactness wherever feasible.
- **Raw price** and **raw quantity** must never be stored as float in the future v002 feature output. If a future feature row carries `price` or `quantity` directly (e.g., a copied source column for traceability), it must remain Decimal-as-string.
- **Quantity-derived sums / aggressive-side quantities / quantity means / quantity imbalances** must be stored as Decimal-as-string in the future v002 feature Parquet.
- **Notional sums** (e.g., rolling notional = sum of `quantity * price`) must be computed in Decimal and stored as Decimal-as-string.
- **Aggressive flow ratios** (dimensionless fractions in [0, 1]) may be stored as `float64` (nullable), since the precision drift is bounded and the natural representation is a fraction.
- **Log returns** may be stored as `float64` (nullable), since the natural representation includes negative values and is dimensionless.
- **Float features must be explicitly justified in writing** in the future v002 feature schema-finalization step. The default for new derived numeric columns is Decimal-as-string unless an explicit float justification is recorded.
- The future v002 feature implementation **must declare** the Python `Decimal` context (precision, rounding mode) used for intermediate arithmetic, and **must include** that context in the deterministic `feature_config_hash`.
- Timestamps remain `int64` UTC ms.
- `is_buyer_maker` and `bool` features are strict `bool`.
- `agg_trade_id`, `row_index`, and integer count columns remain `int64`.
- Every numeric column has an explicit dtype declaration in the future v002 feature manifest.

---

## 16. Multi-day partitioning policy

Binding on any future v002 feature implementation:

- **Per-day output partitioning.** Exactly one per-day feature Parquet per `(symbol, utc_date)` partition, mirroring the Phase 4bm-B v002 per-day normalized Parquet partitioning. For the locked v002 scope (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28), exactly 90 per-day feature Parquets are produced by the future implementation, plus 90 paired Phase 4bb-F sidecars.
- **Boundary windows that may need prior-day lookback.** Per §14, trailing windows that cross a day boundary must be handled by the chosen cross-day policy. The chosen policy must be declared in the future v002 feature schema-finalization step, included in the `feature_config_hash`, and tested.
- **Warm-up / incomplete-window handling.** For day 1 of the v002 range (`2024-12-01`), there is no prior day in scope; feature rows whose trailing window would extend into a missing prior day must carry `rolling_missing_window_flag = true` and the affected aggregates must follow the null policy. Similarly for any window-size policy choice where the warm-up region is incomplete.
- **Invalid-window handling.** The Phase 4bm-B v002 per-day Parquets currently carry `invalid_windows = []` for every day (per Phase 4bm-D's `len(invalid_window_candidates) = 0` across all 90 days). The future v002 feature implementation **must** propagate `invalid_windows` from the v002 derived multi-day index manifest verbatim into the future v002 feature manifest, and **must** propagate per-event `invalid_window_flag` into per-feature-row `invalid_window_flag`. If any future acquisition ever produces non-empty invalid windows, the future feature row whose trailing window intersects an invalid window must carry `rolling_missing_window_flag = true` and its window-aggregates must be null per the null policy. **No silent imputation is permitted across invalid windows. No forward-fill across invalid windows is permitted.**
- **Atomic per-file output discipline.** Each per-day feature Parquet must be written via atomic write-then-rename (`os.replace` or equivalent), paired with its canonical Phase 4bb-F sidecar, and refuse-to-overwrite at the writer level. This matches the Phase 4bm-B / Phase 4bm-D / Phase 4bm-F output discipline.
- **Determinism across reruns.** Two independent reruns of the future v002 feature implementation on the same v002 inputs must produce byte-identical per-day feature Parquets (subject to the deterministic ordering and Decimal-arithmetic guarantees above). The `feature_config_hash` must be byte-stable.

---

## 17. Chronological split / research-split readiness

Binding on any future v002 feature implementation:

- **No split is assigned by Phase 4bm-G.** Phase 4bm-G does **not** define a train / validation / out-of-sample / evaluation split for the v002 feature family or for any downstream ML / strategy / backtest work.
- **A future split-policy memo is required** before any v002 feature artefact is used for ML / backtest / strategy evaluation. The future split-policy memo is the multi-day v002 analogue of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J (the v001 label evaluation / chronological split policy + recording chain). **It is not authorized by Phase 4bm-G.**
- **No random shuffle.** Any future v002 split must be **strictly chronological**. No random shuffle, no stratified shuffle, no symbol shuffle.
- **No leakage across train / validation / test boundaries.** Any future v002 split-policy memo **must** specify exact UTC date / time boundaries with no overlap and no leakage. Feature rows whose trailing window crosses a split boundary must be either: (a) excluded from the second split (the recommended default; preserves no-leakage at the cost of fewer rows near boundaries); or (b) explicitly handled with a warm-up policy declared in the split-policy memo.
- **Feature-implementation-time split-anchoring is forbidden.** The future v002 feature implementation phase (Phase 4bm-H) **must not** embed a hard-coded split in the feature artefact. Splits are declared in a separate phase and applied at downstream consumption time.

---

## 18. Feature-boundary fail-closed rules

The following are binding on any future phase that consumes Phase 4bm-G as input. Each rule, if violated, **must** cause the future implementation to fail closed (refuse to run; refuse to write any artefact; refuse to authorize any successor).

1. **Missing Phase 4bm-F successor-state JSON fails closed.** If the future v002 feature implementation cannot locate `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json`, the implementation must fail closed.
2. **Phase 4bm-F successor-state JSON SHA mismatch fails closed.** If the recomputed SHA256 of the successor-state JSON does not equal `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9`, the implementation must fail closed. The paired sidecar's embedded SHA must match.
3. **v002 derived multi-day index manifest SHA mismatch fails closed.** If the recomputed SHA256 of `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` does not equal `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a`, the implementation must fail closed. The paired sidecar's embedded SHA must match.
4. **v002 raw manifest SHA mismatch fails closed.** If the recomputed SHA256 of `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` does not equal `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`, the implementation must fail closed.
5. **Phase 4bm-D derived gate report SHA mismatch fails closed.** If the recomputed SHA256 of `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` does not equal `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a`, the implementation must fail closed.
6. **Phase 4bl-D-R raw multi-day gate report SHA mismatch fails closed.** If the recomputed SHA256 of `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json` does not equal `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`, the implementation must fail closed.
7. **Phase 4bl-E raw multi-day successor-state JSON SHA mismatch fails closed.** If the recomputed SHA256 of the Phase 4bl-E raw successor-state JSON does not equal `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`, the implementation must fail closed.
8. **Any missing lineage field fails closed.** If any required lineage column (per §11.1) is missing from a feature row or from the future v002 feature manifest, the implementation must fail closed.
9. **Any future-looking feature fails closed.** Any computed feature value that depends on `transact_time_ms > T` is a hard failure. The implementation must fail closed.
10. **Any forbidden column fails closed.** Any output column whose name (lowercased) contains a token from the §13 forbidden-substring list — or whose semantics fall into a §13 forbidden category — is a hard failure. The implementation must fail closed.
11. **Non-monotonic timestamp / row_index violation fails closed.** Within any per-day source Parquet, `(transact_time_ms ASC, row_index ASC)` must be monotone non-decreasing. Any violation is a hard failure; the implementation must fail closed.
12. **Manifest mutation attempt fails closed.** The implementation must **not** attempt to mutate the v002 derived multi-day index manifest, the v002 raw manifest, the v001 derived manifest, the v001 raw manifest, the Phase 4bm-D gate report, the Phase 4bl-D-R gate report, the Phase 4bl-E successor-state JSON, the Phase 4bg-B v001 successor-state JSON, the Phase 4bm-F v002 successor-state JSON, or any other prior `data/microstructure/` artefact. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant must remain in force and must never be invoked. Any attempt is a hard failure; the implementation must fail closed.
13. **Network / credential discipline.** No public endpoint, no Binance API, no authenticated REST, no private endpoint, no WebSocket, no user-stream, no listenKey, no `.env` read, no `.mcp.json` read, and no MCP / Graphify must be touched. Any attempt is a hard failure; the implementation must fail closed.
14. **Path discipline.** All future v002 feature writes must occur under `data/microstructure/features/microstructure_features_aggtrades_v001/...` only. Writes outside that namespace are hard failures.
15. **Refuse-to-overwrite.** Each per-day feature Parquet must refuse to overwrite an existing file. Each paired sidecar must refuse to overwrite. Any attempt is a hard failure.
16. **Static-import discipline.** The future v002 feature implementation modules must remain free of forbidden imports (`prometheus.runtime`, `prometheus.execution`, `prometheus.persistence`, `requests`, `httpx`, `aiohttp`, `urllib.request`, `urllib3`, `socket`, `websockets`, `binance`, `dotenv`, `python_dotenv`, `os.environ`, `getenv`). Violations are hard failures; tests must enforce this.

---

## 19. Proposed future implementation gates

A future v002 feature implementation phase (the hypothetical **Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation**), if ever separately authorized by the operator, **must** satisfy at minimum:

1. **Local gitignored output only.** Phase 4bm-H must produce only local gitignored feature artefacts under `data/microstructure/features/microstructure_features_aggtrades_v001/<SYMBOL>/<YYYY>/<MM>/`. Nothing under `data/microstructure/` may be committed.
2. **Canonical Phase 4bb-F sidecars.** Each per-day feature Parquet must be paired with a canonical Phase 4bb-F sidecar (`<sha256_lowercase_hex><two ASCII spaces><basename><LF>`).
3. **Future v002 feature manifest must cite the Phase 4bm-F successor-state SHA verbatim.** The future v002 feature manifest **must** carry `source_successor_state_sha256 = "72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"` verbatim, and **must** refuse to interpret the original v002 derived multi-day index manifest alone as Stage-3.
4. **Future v002 feature manifest must cite all upstream SHAs from §5.** Every lineage SHA listed in §5 must appear in the future v002 feature manifest's lineage block.
5. **`research_eligible = false` / `eligibility_gate_status = "pending"` default.** The future v002 feature manifest defaults to `research_eligible = false` and `eligibility_gate_status = "pending"`. No Stage-4 transition may occur in Phase 4bm-H.
6. **Forbidden-substring detector enforced.** Phase 4bm-H must include a static substring-detector validator that fails closed on any forbidden column name per §13.
7. **No labels / ML / strategy / backtest.** Phase 4bm-H must not create labels, signals, ML models, strategies, or backtests.
8. **No `prometheus.runtime` / `prometheus.execution` / `prometheus.persistence` imports** and no exchange-adapter imports. Phase 4bm-H runs as a standalone offline phase.
9. **No network I/O / no credentials / no MCP / no Graphify / no `.env` / no `.mcp.json`.**
10. **Standalone test surface.** Per-feature unit tests, per-feature golden-fixture tests on synthetic edge cases (single event; all-buyer-maker; all-seller-maker; mixed; empty trailing window; window-with-no-events; day-boundary; multi-day boundary), one-symbol/multi-day end-to-end run on the existing v002 normalized Parquets, static no-network / no-credential / no-MCP / no-Graphify import-boundary tests, static no-overwrite test, static schema-equality test asserting the feature column set matches a module-level constant (`FEATURE_SCHEMA_V001` or equivalent).
11. **Whole-repo `ruff check .` clean.**
12. **Whole-repo `mypy src/prometheus` strict clean.**
13. **Whole-repo `pytest` clean** except for the unchanged pre-existing `KeyError: 'trade_count'` simulation failures preserved as the Phase 4bm-B baseline.
14. **Determinism.** Two independent reruns of Phase 4bm-H on the same v002 inputs must produce byte-identical per-day feature Parquets and byte-identical sidecars.
15. **Atomic write-then-rename** and **refuse-to-overwrite** at the writer level.
16. **Followed by a separately authorized future v002 feature artefact structural QA memo** (multi-day analogue of Phase 4bi-A). Phase 4bm-H must not collapse later gates; Phase 4bm-H must not authorize any successor.
17. **Preserves every retained verdict and project lock verbatim.**

A future v002 feature schema finalization step may be inserted between Phase 4bm-G and Phase 4bm-H (the multi-day analogue of Phase 4bh-B), if the operator chooses to split the design and finalization work into two memos. Alternatively, Phase 4bm-H may be authorized directly with all schema choices fixed in its authorization prompt. **Either choice is at operator discretion and is not authorized by Phase 4bm-G.**

---

## 20. What this phase proves

- that the project record contains a complete feature-boundary design for a future v002 feature-implementation phase on the multi-day v002 Stage-3-marked normalized derived family;
- that the canonical v002 input, forbidden v002 inputs, future v002 feature-stage model, leakage / windowing / aggregation / precision / type / missing-window / multi-day-partition policies, future v002 output / manifest schemas, future v002 validation gate sequence, and future v002 acceptance criteria are predeclared **before** any feature implementation exists for v002;
- that the original v002 derived multi-day index manifest, the original v002 raw manifest, the v001 derived manifest, the v001 raw manifest, the 90 v002 per-day Parquets, the 90 v002 raw zips, the Phase 4bm-D authoritative gate report, the Phase 4bl-D-R raw multi-day PASS gate report, the Phase 4bl-E raw successor-state JSON, the Phase 4bm-F v002 derived successor-state JSON, the Phase 4bg-B v001 derived successor-state JSON, and every other prior `data/microstructure/` artefact remain byte-immutable;
- that the Phase 4bm-F successor-state JSON SHA `72b6edd4…` is cited as the **only** Stage-3 marker for the multi-day v002 derived family;
- that Phase 4bm-G reaches **v002 Feature Stage-0** design only and does not authorize any successor;
- that the v001 Phase 4bh-A / Phase 4bh-B feature-boundary work does **not** transitively authorize v002 feature work.

---

## 21. What this phase does not prove

- that any v002 feature is statistically meaningful for any specific research question;
- that any future v002 feature implementation will produce a Stage-2 feature artefact that passes structural QA;
- that any future v002 feature-family eligibility gate will pass;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that any retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure) may be revisited;
- that any project lock may be loosened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible;
- that any additional acquisition (cross-symbol, multi-quarter, mark-price, order-book, funding, OI, liquidation, cross-venue) is admissible.

---

## 22. Non-authorization

Phase 4bm-G does **not**, and **cannot**, be construed as authorising:

- **Phase 4bm-H — Multi-Day V002 Feature Schema / Feature Computation Implementation** (the canonical successor; not authorized);
- any multi-day v002 feature schema finalization memo, if the operator chooses to split design and finalization;
- any multi-day v002 feature artefact structural QA memo (multi-day analogue of Phase 4bi-A);
- any multi-day v002 feature-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bi-B);
- any multi-day v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C);
- any multi-day v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D);
- any multi-day v002 label-family phase (multi-day analogues of Phase 4bj-A through Phase 4bj-K);
- any multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / Phase 4bj-I / Phase 4bj-J);
- Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / Phase 5 / Phase 4 canonical / any other successor;
- feature computation on v002 (or on v001);
- label computation on v002 (or on v001);
- signal computation;
- diagnostics rerun (Phase 3s Q1–Q7 closure preserved);
- ML training, model selection, feature ranking, meta-labeling;
- strategy implementation, signal construction, backtest implementation;
- additional acquisition (beyond the 90 locked v002 BTCUSDT UTC dates 2024-12-01 .. 2025-02-28);
- cross-symbol acquisition;
- mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated API / private endpoint acquisition;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- user-stream / live WebSocket implementation;
- public-endpoint calls in code;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any actual on-disk manifest;
- any further successor-state JSON creation;
- amending the Phase 4ak M0 admissibility gate / post-null cooldown rule / cooled-down families list / memo template;
- amending the Phase 4al refined no-rescue rule / §13 boundary / §14 hierarchy;
- amending the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- amending the Phase 4bb-F canonical path policy;
- amending the Phase 4bl-F four-tier risk model / R-SIDECAR-CRLF / nine reusable non-authorization blocks;
- amending the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard;
- amending the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard;
- amending the Phase 4bm-E decision (Option B / Decision form 2 preserved verbatim);
- agents-by-default for heavy Claude Code execution sessions;
- copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`;
- committing local hook files from the lightweight workspace into `C:\Prometheus` without a separately authorized process phase;
- committing anything under `data/microstructure/`.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the merge-closeout standard.

**Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 honoured by this phase**: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

## 23. Recommended next state

**Remain paused.**

Phase 4bm-G is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived family now carries a complete Phase 4ba 5-stage ladder of evidence through Stage-3 and a complete v002 Feature Stage-0 boundary design:

- Stage-0: Phase 4bm-B normalization.
- Stage-1: Phase 4bm-C 56/56 structural QA PASS.
- Stage-2: Phase 4bm-D 60/60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2 (policy-level admissibility).
- Stage-3: Phase 4bm-F successor-state JSON SHA `72b6edd4…` (machine-readable marker).
- v002 Feature Stage-0: **Phase 4bm-G this memo** (feature schema designed on paper; no code, no data, no artefact).

Stage-4 (feature-cleared) and v002 Feature Stages 1 through 5 remain unauthorized.

The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). The operator's broader pause decision continues to apply.

---

## 24. Conditional next options, none authorized

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 lifecycle ladder** — future Phase 4bm-H Multi-Day V002 Feature Schema / Feature Computation Implementation (multi-day analogue of Phase 4bh; would compute features locally under `data/microstructure/features/...` and produce gitignored per-day feature Parquets + sidecars + future v002 feature manifest; would not authorize ML, strategy, label, diagnostics, or backtest work) | code + docs + local gitignored feature artefacts only | **NOT authorized by this memo** |
| **Conditional alternative, if separating design from implementation** — future docs-only multi-day v002 feature schema finalization memo (multi-day analogue of Phase 4bh-B) | docs-only; no computation | **NOT authorized by this memo** |
| **Conditional after future v002 feature implementation** — future Phase 4bm-* v002 feature artefact structural QA memo (multi-day analogue of Phase 4bi-A) | analysis + docs | **NOT authorized by this memo** |
| **Conditional after future v002 feature QA** — future Phase 4bm-* v002 feature-family eligibility-gate design + implementation + execution (multi-day analogue of Phase 4bi-B) | code + docs + local gitignored gate-report | **NOT authorized by this memo** |
| **Conditional after future v002 feature-family gate** — future Phase 4bm-* v002 feature-family research-use decision memo (multi-day analogue of Phase 4bi-C) | docs-only | **NOT authorized by this memo** |
| **Conditional after future v002 feature-family research-use decision** — future Phase 4bm-* v002 feature-family successor-state recording (multi-day analogue of Phase 4bi-D) | docs + local gitignored successor-state JSON | **NOT authorized by this memo** |
| **Conditional further down the ladder** — future multi-day v002 label-family phases (multi-day analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by this memo** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope of Phase 4bm-G** |
| Feature computation on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-G** |
| Label computation on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-G** |
| Diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by Phase 4bm-G** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-G** |

**No successor phase is authorized by Phase 4bm-G.**

---

## Preserved boundaries

- H0 — FRAMEWORK ANCHOR.
- R3 — BASELINE-OF-RECORD.
- R1a / R1b-narrow — RETAINED — NON-LEADING.
- R2 — FAILED — §11.6.
- F1 — HARD REJECT.
- D1-A — MECHANISM PASS / FRAMEWORK FAIL.
- 5m thread — OPERATIONALLY CLOSED (Phase 3t).
- V2 — HARD REJECT — terminal for V2 first-spec.
- G1 — HARD REJECT — terminal for G1 first-spec.
- C1 — HARD REJECT — terminal for C1 first-spec.
- §11.6 = 8 bps per side; round-trip = 16 bps.
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops.
- Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8.
- Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w.
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; never invoked).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F results — all preserved verbatim.

---

**Final reminders, recorded verbatim:**

- **Feature-boundary design is not feature computation.**
- **Stage-4 is not authorized by Phase 4bm-G.**
- **Phase 4bm-H is not authorized by Phase 4bm-G.**
- **No v002 feature artefact exists after Phase 4bm-G.**

**Recommended state: remain paused.**
