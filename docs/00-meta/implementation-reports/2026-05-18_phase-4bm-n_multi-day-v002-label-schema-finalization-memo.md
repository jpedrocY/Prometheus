# Phase 4bm-N — Multi-Day V002 Label Schema Finalization Memo

**Phase identity:** Phase 4bm-N — Multi-Day V002 Label Schema Finalization Memo (docs-only schema-finalization memo; multi-day v002 analogue of Phase 4bj-B).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-n/multi-day-v002-label-schema-finalization-memo`.
**Base:** `main` at `e74dc13021900a54153cba81eaed8fdb397fb292` (Phase 4bm-M merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bj-B label-schema precedent. First-of-kind multi-day v002 label-schema finalization; locks future target / label semantics for a Stage-5-admissible feature family and therefore can affect downstream ML admissibility under §3 ("creates features / labels / diagnostics" + "affects eligibility / admissibility / downstream authorization").
**Phase type:** docs-only. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`. **No** local gitignored output. **No** source / test / script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** label parquet, label sidecar, label manifest, label gate report, or label successor-state JSON created. **No** `data/microstructure/` file is created, modified, deleted, renamed, or committed.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Phase header

This phase **locks** the exact v002 label schema at memo level only, building on Phase 4bm-M's boundary / design memo and the Phase 4bj-B v001 schema-finalization precedent. It does not compute, validate, implement, or otherwise materialize any label artefact. It locks, at memo level only, the column-by-column, horizon-by-horizon, formula-by-formula, dtype-by-dtype, lineage-by-lineage v002 label schema that any future implementation phase must follow without amendment.

Phase 4bm-N is the **multi-day v002 analogue of Phase 4bj-B** (the v001 label-schema-finalization memo merged on `main`; selected Outcome 1 — label schema finalized, implementation deferred). Phase 4bj-B is the primary structural precedent. Phase 4bm-N adopts the Phase 4bj-B v001 column shape verbatim with three explicit v002-specific adaptations:

1. **multi-day lineage SHAs** — every v002 lineage field replaces its v001 Phase 4bi-* / per-day analogue with the v002 Phase 4bm-* / multi-day-index analogue (Phase 4bm-L successor-state SHA in place of Phase 4bi-D; Phase 4bm-J gate report SHA in place of Phase 4bi-B; v002 feature manifest SHA in place of v001 feature manifest SHA; v002 normalized **manifest** SHA replaces v001 per-day normalized **parquet** SHA);
2. **v002-explicit raw lineage** — adds `source_raw_manifest_sha256` as a fully required lineage column (the v002 raw manifest is the single canonical pointer to all 90 acquired daily zips), where v001 omitted the raw lineage column;
3. **multi-day end-of-sample censoring** — censoring occurs **only** at the 90-day v002 envelope's terminal boundary (2025-02-28 23:59:59.999 UTC) rather than at every per-day boundary; horizons may cross UTC day boundaries within the envelope (v001 did not, because the v001 artefact was single-day-only).

The schema column count rises from v001's 39 columns to v002's 40 columns (delta +1; one lineage field added, one lineage field replaced).

## 2. Scope

Phase 4bm-N finalizes, at memo level only:

- the exact v002 label family identity and naming;
- the exact v002 label schema version (`v001`, mirroring Phase 4bj-B);
- the exact v002 label column list (eight labels);
- the exact v002 horizon list (four horizons);
- the exact v002 anchor-row and anchor-price policy;
- the exact v002 future-reference-row and future-reference-price policy (multi-day cross-day-allowed; envelope-bounded);
- the exact v002 `forward_log_return_<horizon>` formula;
- the exact v002 `forward_direction_<horizon>` derivation policy;
- the exact v002 support / quality column set;
- the exact v002 lineage / identity column set;
- the exact v002 dtype policy;
- the exact v002 null / censoring policy (multi-day, end-of-envelope-only);
- the exact v002 label manifest schema;
- the exact v002 `label_config_hash` policy;
- the exact v002 future label output paths;
- the exact v002 future implementation acceptance criteria;
- the exact v002 future QA / gate expectations;
- the exact v002 chronological-split-policy default;
- the exact v002 no-rescue / M0 boundary.

Phase 4bm-N applies prospectively. It does not authorize implementation work and does not authorize Phase 4bm-O.

## 3. Non-scope

Phase 4bm-N does **not**:

- modify source code, tests, scripts, configurations;
- modify the v002 feature manifest, v002 feature manifest sidecar, v002 per-day feature parquets, v002 per-day feature sidecars;
- modify the Phase 4bm-J v002 feature-family eligibility-gate report or its sidecar;
- modify the Phase 4bm-L v002 feature-family Stage-5 successor-state JSON or its sidecar;
- modify the Phase 4bm-F v002 derived-family Stage-3 successor-state JSON or its sidecar;
- modify the Phase 4bm-D v002 derived-family gate report or its sidecar;
- modify the v002 derived multi-day index manifest or its sidecar;
- modify the v002 raw manifest, v002 acquisition log, Phase 4bl-D-R raw multi-day gate report, or Phase 4bl-E raw multi-day successor-state JSON;
- modify any prior gate report, prior successor-state JSON, or prior manifest;
- create labels, targets, signals, ML, strategy, diagnostics, or backtest artefacts;
- create any label parquet, label sidecar, label manifest, label manifest sidecar, label gate report, or label successor-state JSON;
- compute returns, alpha, edge, predictiveness, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, decision score, entry / exit signal, or any other quantitative output;
- train ML; design strategy logic; run backtests, simulations, or paper / shadow;
- acquire data; call public endpoints, Binance APIs, or private endpoints; open WebSockets; request, store, or use credentials; read or create `.env`; create or read `.mcp.json`; enable MCP or Graphify;
- flip `research_eligible` on any actual manifest; transition `eligibility_gate_status` on any actual manifest; mark `stage_4_feature_cleared = true` on any actual manifest; change `chronological_split_policy` on any actual manifest;
- mutate the v002 feature manifest, any upstream manifest, any prior gate report, or any prior successor-state JSON in any way;
- amend M0; revise any retained verdict; change any project lock;
- authorize Phase 4bm-O, multi-day v002 label-kernel implementation, multi-day v002 label structural QA, multi-day v002 label-family eligibility gate, multi-day v002 label-family research-use decision, multi-day v002 label-family successor-state recording, multi-day v002 chronological-split-policy memo, multi-day v002 diagnostics, multi-day v002 ML / strategy / backtest, Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, live WebSocket implementation;
- commit anything under `data/microstructure/`.

## 4. Linkage to Phase 4bm-M Label Stage-0 boundary / design

Phase 4bm-N finalizes a schema only because Phase 4bm-M established the multi-day v002 label-boundary policy at memo level on `main`. The Phase 4bm-M boundary binds Phase 4bm-N without exception:

- labels are a sibling artefact family of the v002 feature family;
- labels must never feed back into v002 features;
- v002 features must remain causal per the Phase 4bm-G / Phase 4bh contract verbatim;
- labels may use future information only inside the label kernel routine;
- labels must preserve lineage to the v002 feature manifest, the Phase 4bm-L successor-state, the Phase 4bm-J gate report, the v002 derived multi-day index manifest, the v002 raw manifest, the Phase 4bl-E raw successor-state, and the Phase 4bl-D-R raw gate report;
- label manifests default to `research_eligible: false` / `eligibility_gate_status: "pending"` / `label_family_research_use_authorized: false` / `chronological_split_policy: "not_yet_defined"`;
- label design does not prove edge;
- direction accuracy is not profitability;
- cost / RR / WR / expectancy are strategy-evaluation concepts, not label-schema proof;
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + memo template + cooled-down families list remain binding;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy remain binding.

The Phase 4bm-L successor-state JSON's `feature_family_research_use_approved_in_principle: true` field is sibling-artefact-only and does not flip `research_eligible` on the v002 feature manifest. Phase 4bm-N reads it as policy-level v002 Feature Stage-5 admissibility and finalizes a v002 label schema consistent with that admissibility, **not** as authorization to implement.

## 5. Linkage to Phase 4bm-L machine-readable v002 Feature Stage-5 marker

Phase 4bm-L is the canonical v002 Feature Stage-5 admissibility evidence:

- successor-state JSON path: `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json`;
- successor-state JSON SHA256: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (recomputed on disk at the start of this phase; MATCH);
- successor-state sidecar SHA256: `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98`;
- `feature_family_research_use_approved_in_principle = true`;
- `machine_readable_stage5_marker_created_by_this_file = true`;
- `successor_stage = "Feature Stage-5"`.

The v002 feature manifest remains byte-identical at SHA256 `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` and still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved (never invoked by Phase 4bm-N).

## 6. Linkage to Phase 4bm-K research-use decision

Phase 4bm-K Outcome 1 / Decision form 1 (equivalent label `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`; SHA-finalization commit `121865a26120d5f097fee95c00185ebd4c995703`) is the v002 Feature Stage-5 admissibility decision in writing. It is the policy gate that allows Phase 4bm-M to design a future v002 label-family boundary and allows Phase 4bm-N (this phase) to finalize the v002 label schema.

## 7. Linkage to Phase 4bm-J `FEATURE_GATE_PASS`

Phase 4bm-J is the report-level v002 Feature Stage-4 evidence:

- gate verdict: `FEATURE_GATE_PASS`;
- `overall_status`: `pass`;
- 50 / 50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE; 0 blocking failures;
- gate report SHA256: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (recomputed on disk at the start of this phase; MATCH);
- gate sidecar SHA256: `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`.

## 8. Linkage to Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`

Phase 4bm-I produced verdict `FEATURE_STRUCTURAL_QA_PASS` over the Phase 4bm-H feature artefacts (read-only structural QA layer). Verdict machine-verified by Phase 4bm-J check A12 PASS.

## 9. Linkage to Phase 4bm-H feature artefacts

The v002 feature artefacts are the upstream lineage for any future v002 label artefact:

- feature manifest path: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`;
- feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (recomputed on disk at the start of this phase; MATCH);
- feature manifest sidecar SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`;
- `feature_config_hash`: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`;
- feature parquet count: 90;
- feature sidecar count: 90;
- total feature row count: 155,153,449;
- feature date range: 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days);
- symbol scope: BTCUSDT (one symbol);
- feature schema column count: 62 (17 lineage / identity / metadata + 45 feature / quality).

## 10. Linkage to Phase 4bj-B v001 label-schema-finalization precedent

Phase 4bj-B is the primary structural precedent for Phase 4bm-N (selected Outcome 1 in Phase 4bj-B verbatim: "Label schema finalized, implementation deferred"). Phase 4bm-N adopts the Phase 4bj-B 39-column shape verbatim with the three v002-specific adaptations listed in §1. Specifically:

- Phase 4bj-B selected horizons `{1s, 5s, 15s, 60s}` → Phase 4bm-N **mirrors** verbatim (no widening, no narrowing).
- Phase 4bj-B selected forward-return formula `ln(reference_trade_price_H / anchor_trade_price)` → Phase 4bm-N **mirrors** verbatim.
- Phase 4bj-B selected direction policy `strict sign threshold at 0.0 log-return; no dead-band; values in {-1, 0, 1, null}` → Phase 4bm-N **mirrors** verbatim.
- Phase 4bj-B selected per-horizon support columns `reference_row_index_H`, `reference_timestamp_ms_H`, `horizon_censored_flag_H` → Phase 4bm-N **mirrors** verbatim.
- Phase 4bj-B selected global support columns `label_invalid_price_flag`, `label_any_censored_flag` → Phase 4bm-N **mirrors** verbatim.
- Phase 4bj-B selected null / censoring policy "keep all feature rows; censor right-edge horizons; no row dropping; no `NaN`; no `inf`" → Phase 4bm-N **mirrors** the row-preservation rule verbatim, **adapts** the right-edge boundary from "end of single UTC day" (v001) to "end of 90-day v002 envelope" (v002).
- Phase 4bj-B forbade barrier / MFE / MAE / R-multiple / strategy / model / mark-price / order-book / external-data columns → Phase 4bm-N **mirrors** the forbidden-column list verbatim.

v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation. v002 label computation requires a separately authorized future phase (multi-day analogue of Phase 4bj-C).

## 11. Evidence table

| # | Evidence item | Value |
| - | ------------- | ----- |
|  1 | Phase 4bm-L successor-state JSON SHA256 | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (recomputed; MATCH) |
|  2 | Phase 4bm-L successor-state sidecar SHA256 | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` |
|  3 | Phase 4bm-K decision | **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) |
|  4 | Phase 4bm-K SHA-finalization commit | `121865a26120d5f097fee95c00185ebd4c995703` |
|  5 | Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` (`overall_status = pass`) |
|  6 | Phase 4bm-J gate report SHA256 | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (recomputed; MATCH) |
|  7 | Phase 4bm-J gate sidecar SHA256 | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` |
|  8 | Phase 4bm-J check totals | 50 / 50 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking |
|  9 | Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` |
| 10 | v002 feature manifest SHA256 | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (recomputed; MATCH; unchanged) |
| 11 | v002 feature manifest sidecar SHA256 | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` (unchanged) |
| 12 | `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| 13 | Feature parquet count | 90 |
| 14 | Feature sidecar count | 90 |
| 15 | Total feature row count | 155,153,449 |
| 16 | Feature date range | 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days) |
| 17 | Symbol scope | BTCUSDT (one symbol) |
| 18 | Feature schema column count | 62 (17 lineage / identity / metadata + 45 feature / quality) |
| 19 | v002 derived multi-day index manifest SHA256 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (recomputed; MATCH; unchanged) |
| 20 | v002 derived manifest sidecar SHA256 | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` (unchanged) |
| 21 | v002 raw manifest SHA256 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (unchanged) |
| 22 | v002 acquisition log SHA256 | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` (unchanged) |
| 23 | Phase 4bl-D-R raw multi-day PASS gate report SHA256 | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` (unchanged) |
| 24 | Phase 4bl-E raw multi-day successor-state JSON SHA256 | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` (unchanged) |
| 25 | Phase 4bm-D authoritative derived-family gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (unchanged) |
| 26 | Phase 4bm-D authoritative gate sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` (unchanged) |
| 27 | Phase 4bm-F v002 derived-family Stage-3 successor-state JSON SHA256 | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (unchanged) |
| 28 | Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar SHA256 | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` (unchanged) |
| 29 | Phase 4bm-M boundary / design status | docs-only memo merged on main at `cc67ad4`; SHA-finalization at `e74dc13`; no label artefact exists |
| 30 | On-disk v002 feature manifest invariants (verified) | `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false`; `actual_feature_row_count = 155153449`; `symbol = "BTCUSDT"`; `per_day_outputs` length = 90 |

## 12. Finalized label family identity

Locked by Phase 4bm-N:

| field | value |
| ----- | ----- |
| `dataset_family` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v002` |
| `label_schema_version` | `v001` |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v002` |
| `source_normalized_dataset_family` | `microstructure_normalized_aggtrades_v001` |
| `source_normalized_dataset_version` | `v002` |
| `source_raw_dataset_family` | `microstructure_raw_aggtrades_v001` |
| `source_raw_dataset_version` | `v002` |
| `symbol` | `BTCUSDT` (one symbol) |
| `symbol_list` | `["BTCUSDT"]` |
| `utc_date_start` | `2024-12-01` |
| `utc_date_end` | `2025-02-28` (inclusive; envelope-terminal day) |
| `date_count` | `90` |

## 13. Finalized row model

Event-aligned to v002 feature rows, per UTC day:

- **One label row per feature row, per UTC day.**
- For each of the 90 UTC dates `D` in `[2024-12-01, 2025-02-28]`, the per-day label parquet `D.parquet` has exactly the same row count as the per-day feature parquet for date `D`.
- Total label `row_count` across all 90 per-day label parquets is expected to equal the total v002 feature row count `155,153,449` (the future implementation must verify this exactly).
- `row_index` matches the corresponding per-day feature parquet's `row_index` row-by-row.
- No row dropping.
- No resampling.
- No synthetic timestamps.
- No upsampling.
- No downsampling.
- **Cross-day horizon lookahead is allowed inside the label kernel routine only** (Phase 4bm-M boundary §22); features remain causal per Phase 4bm-G / Phase 4bh contract verbatim.
- Right-edge horizon values at the 90-day envelope's terminal boundary are **nullable / censored**, not removed (see §16 multi-day censoring policy).
- Row ordering within each per-day parquet uses `(source_transact_time_ms ASC, row_index ASC)`, matching Phase 4bm-G / Phase 4bh row contract verbatim.

## 14. Finalized column schema

The future v002 label parquet must contain **exactly** the following 40 columns in canonical order. The enumerated column list below is authoritative.

**Lineage / identity / metadata columns (17):**

1. `dataset_family` — string — constant across all 90 per-day label parquets: `"microstructure_labels_aggtrades_v001"`
2. `dataset_version` — string — constant: `"v002"`
3. `label_schema_version` — string — constant: `"v001"`
4. `source_feature_dataset_family` — string — constant: `"microstructure_features_aggtrades_v001"`
5. `source_feature_dataset_version` — string — constant: `"v002"`
6. `source_feature_manifest_sha256` — string — constant across all 90 per-day label parquets; points to the v002 feature manifest (`512a0a54…633343d`)
7. `source_feature_parquet_sha256` — string — **per-day-constant** within each per-day label parquet; varies across the 90 per-day label parquets; points to that day's v002 feature parquet (read from the v002 feature manifest's `per_day_outputs` entry for that day)
8. `source_feature_successor_state_sha256` — string — constant; points to the Phase 4bm-L successor-state JSON (`7eccaa8f…35e4`)
9. `source_phase_4bm_j_gate_report_sha256` — string — constant; points to the Phase 4bm-J gate report (`3c59dfae…898242`)
10. `source_normalized_manifest_sha256` — string — constant; points to the v002 derived multi-day index manifest (`01c5fa53…1a2554a`); **v002-specific replacement** of v001's per-day `source_normalized_parquet_sha256` (since the v002 normalized family is indexed by a multi-day manifest, not a single per-day parquet)
11. `source_raw_manifest_sha256` — string — constant; points to the v002 raw manifest (`01696786…d87485`); **v002-new** lineage column (v001 omitted this)
12. `symbol` — string — constant: `"BTCUSDT"`
13. `utc_date` — string — **per-day-constant** within each per-day label parquet; equals the anchor row's UTC date in `YYYY-MM-DD` format (not the future reference's date, even when a horizon crosses day boundaries)
14. `row_index` — int64 — per-row; matches the corresponding feature parquet's `row_index` row-by-row
15. `agg_trade_id` — int64 — per-row; matches the corresponding feature parquet's `agg_trade_id` row-by-row
16. `feature_timestamp_ms` — int64 — per-row; UTC ms; matches the corresponding feature parquet's `feature_timestamp_ms` row-by-row
17. `source_transact_time_ms` — int64 — per-row; UTC ms; matches the corresponding feature parquet's `source_transact_time_ms` row-by-row

**Label config hash column (1):**

18. `label_config_hash` — string — constant across all 90 per-day label parquets; deterministic SHA256 over the canonical-JSON encoding of the schema-locking fields (see §20)

**Regression label columns (4):**

19. `forward_log_return_1s` — nullable float64
20. `forward_log_return_5s` — nullable float64
21. `forward_log_return_15s` — nullable float64
22. `forward_log_return_60s` — nullable float64

**Classification label columns (4):**

23. `forward_direction_1s` — nullable int8 in `{-1, 0, 1, null}`
24. `forward_direction_5s` — nullable int8 in `{-1, 0, 1, null}`
25. `forward_direction_15s` — nullable int8 in `{-1, 0, 1, null}`
26. `forward_direction_60s` — nullable int8 in `{-1, 0, 1, null}`

**Per-horizon support columns (12 = 4 × 3):**

27. `reference_row_index_1s` — nullable int64
28. `reference_timestamp_ms_1s` — nullable int64 (UTC ms)
29. `horizon_censored_flag_1s` — non-nullable bool
30. `reference_row_index_5s` — nullable int64
31. `reference_timestamp_ms_5s` — nullable int64 (UTC ms)
32. `horizon_censored_flag_5s` — non-nullable bool
33. `reference_row_index_15s` — nullable int64
34. `reference_timestamp_ms_15s` — nullable int64 (UTC ms)
35. `horizon_censored_flag_15s` — non-nullable bool
36. `reference_row_index_60s` — nullable int64
37. `reference_timestamp_ms_60s` — nullable int64 (UTC ms)
38. `horizon_censored_flag_60s` — non-nullable bool

**Global support / QA columns (2):**

39. `label_invalid_price_flag` — non-nullable bool
40. `label_any_censored_flag` — non-nullable bool

**Total finalized v002 columns: 40** (v001 was 39; v002 delta = +1; added `source_raw_manifest_sha256`; replaced v001's optional `source_normalized_parquet_sha256` with the v002-required `source_normalized_manifest_sha256`).

Phase 4bj-B Section-10 column-#16 (v001 `source_normalized_parquet_sha256`) is replaced in v002 by required column #10 `source_normalized_manifest_sha256`, **because** the v002 normalized family is multi-day-indexed (Phase 4bm-B + Phase 4bm-D / 4bm-E / 4bm-F), not single-day. The v002 normalized manifest SHA pins the entire 90-day normalized envelope deterministically.

## 15. Finalized label list

The future v002 label parquet must include **exactly** these eight label columns and no others:

- `forward_log_return_1s`
- `forward_log_return_5s`
- `forward_log_return_15s`
- `forward_log_return_60s`
- `forward_direction_1s`
- `forward_direction_5s`
- `forward_direction_15s`
- `forward_direction_60s`

The following label classes are **forbidden** at v002 first pass (verbatim from Phase 4bj-B §11; preserved in Phase 4bm-M §20 forbidden list):

- barrier labels;
- target-before-stop labels;
- MFE labels;
- MAE labels;
- R-multiple labels;
- PnL labels;
- equity labels;
- drawdown labels;
- strategy-action labels;
- position-state labels;
- entry / exit labels;
- model prediction / probability / score labels;
- alpha / edge / decision-score labels;
- execution-quality labels;
- cross-symbol labels;
- cross-sectional labels;
- exchange-write outcome labels;
- mark-price / index-price / bid-ask / order-book / funding / OI / liquidation / external-data-derived labels;
- post-hoc optimized-threshold labels.

## 16. Finalized horizon list

Locked exactly (mirror of Phase 4bj-B §12):

- `1s` = `1000` ms
- `5s` = `5000` ms
- `15s` = `15000` ms
- `60s` = `60000` ms

`horizon_list = ["1s", "5s", "15s", "60s"]`
`horizon_ms_list = [1000, 5000, 15000, 60000]`

Explicitly deferred at v002 first pass (mirror of Phase 4bj-B v001 deferral):

- `30s`
- `5m`, `15m`, `30m`, `1h`, `4h`
- day-end and multi-day horizons (e.g., `1d`, `7d`)

A future amendment memo would be required to widen the horizon list; silent widening at v002 implementation time is forbidden.

## 17. Finalized forward-reference price policy (multi-day, envelope-bounded)

For every feature row `R` (in per-day label parquet for date `D`) with anchor timestamp `T = feature_timestamp_ms` and per horizon `H` in `{1s, 5s, 15s, 60s}` with `H_ms` in `{1000, 5000, 15000, 60000}`:

- **target_timestamp_ms** = `T + H_ms`.
- **envelope_terminal_unix_ms** = the maximum `source_transact_time_ms` across the entire v002 90-day envelope (i.e., across all 90 normalized aggTrades per-day parquets `2024-12-01.parquet` .. `2025-02-28.parquet`), discoverable via the v002 derived multi-day index manifest at SHA `01c5fa53…1a2554a`.
- If `target_timestamp_ms > envelope_terminal_unix_ms`, then:
  - `horizon_censored_flag_H = true`,
  - `forward_log_return_H = null`,
  - `forward_direction_H = null`,
  - `reference_row_index_H = null`,
  - `reference_timestamp_ms_H = null`.
- Otherwise:
  - `reference_row_index_H` = the row_index of the **largest-row-index normalized aggTrades row across the v002 90-day envelope** such that `transact_time_ms <= target_timestamp_ms`. This may be in the same day `D` as the anchor, or in a future day `D' > D` within the envelope. The kernel resolves the destination per-day normalized parquet by walking the v002 multi-day index manifest in chronological order.
  - When multiple rows share the same maximum `transact_time_ms <= target_timestamp_ms`, choose the largest `row_index` at that timestamp inside its per-day source parquet (this is the Phase 4bm-G / Phase 4bh same-timestamp tie-break, applied inside the label routine only).
  - `reference_timestamp_ms_H` = the `transact_time_ms` of that chosen normalized aggTrades row.
  - `reference_trade_price_H` = the trade price of that chosen normalized aggTrades row, parsed from the Decimal-as-string column.

**Multi-day adaptation versus v001:** v001 censored at every UTC day's end (single-day-only artefact); v002 censors **only** at the envelope-terminal boundary (2025-02-28 23:59:59.999 UTC, expressed as `envelope_terminal_unix_ms`). Horizons may cross UTC day boundaries within the 90-day v002 envelope, but **never** beyond `envelope_terminal_unix_ms`. The anchor row's `utc_date` column records the anchor's UTC date only (not the future reference's date, even when the horizon crosses a day boundary).

**Anchor price** for row `R`:

- `anchor_trade_price` = the trade price of the normalized aggTrades row identified by `(agg_trade_id, row_index)` for feature row `R` within its day `D`.
- The anchor price domain is the same trade-price domain as the v002 feature parquet's price-related Decimal columns (Phase 4bm-G / Phase 4bh contract verbatim).

**Forbidden:**

- using mark price for any anchor or reference;
- using index price;
- using bid / ask / book midpoint;
- using order-book data;
- using external data;
- using the first trade **after** `target_timestamp_ms`;
- looking past `target_timestamp_ms` for any horizon;
- using future v002 feature columns to compute v002 label values;
- using any future v002 label column to compute another v002 label;
- looking past `envelope_terminal_unix_ms` for any reason whatsoever (no synthetic extrapolation; no zero-padding; no fabricated rows; no acquisition beyond the locked 90-day envelope).

Rationale (recorded):

> This policy measures the last observed trade price at or before the future horizon timestamp without peeking past the horizon, and without ever fabricating data beyond the locked 90-day v002 envelope. It avoids forward-trade bias, mark-price domain mixing, and book-data dependence. Allowing cross-day reference resolution (within the envelope) keeps the v002 label set dense at the per-day boundary without leaking outside the v002 lifecycle.

## 18. Finalized `forward_log_return` formula

For every (row `R`, horizon `H`) where the horizon is **not** censored and both anchor and reference prices are valid:

```
forward_log_return_H = ln(reference_trade_price_H / anchor_trade_price)
```

Rules (mirror of Phase 4bj-B §14):

- Use natural logarithm (`math.log` or `numpy.log`).
- Parse `anchor_trade_price` and `reference_trade_price_H` from the Decimal-as-string source column to `Decimal` exactly, then cast the ratio to deterministic `float64` only at the log step.
- If `anchor_trade_price <= 0`:
  - `forward_log_return_H = null` for all `H`,
  - `forward_direction_H = null` for all `H`,
  - `label_invalid_price_flag = true`.
- If `reference_trade_price_H <= 0`:
  - that horizon's `forward_log_return_H = null`,
  - that horizon's `forward_direction_H = null`,
  - `label_invalid_price_flag = true`.
- If the horizon is censored:
  - that horizon's `forward_log_return_H = null` (regardless of `label_invalid_price_flag`).
- `forward_log_return_H` columns must never contain `NaN` or `inf`. Any case that would produce `NaN` or `inf` must instead be represented as a null with the appropriate flag set.
- Null is allowed only under explicit censoring or invalid-price conditions defined above.

**Implementation contract (binding on future v002 label-kernel implementation):**

- the Decimal → float64 cast must occur **after** the ratio is formed in `Decimal`, not before;
- the natural-log step is allowed to lose precision below `float64` epsilon; this is acceptable for v002 because labels are descriptive, not strategy-grade;
- the future implementation must not switch to `log10`, `log2`, simple return `(R/A - 1)`, percentage return `(R/A - 1) * 100`, or any other base / scaling without a separately authorized v002 schema-amendment memo.

## 19. Finalized `forward_direction` policy

For every (row `R`, horizon `H`) (mirror of Phase 4bj-B §15):

- `forward_direction_H` is derived **only** from `forward_log_return_H`.
- Values:
  - `+1` if `forward_log_return_H > 0`
  - `0` if `forward_log_return_H == 0`
  - `-1` if `forward_log_return_H < 0`
  - `null` if `forward_log_return_H` is null
- Threshold policy at v002: **strict sign threshold**, threshold = `0.0` log-return.
- **No deadband** at v002.
- **No bp threshold** at v002.
- **No threshold optimization** at v002 or in any future v002 label-kernel implementation.
- **No evaluation-window fitting** at v002.
- **No cost-based threshold** at the label-schema level.

Rationale (recorded):

> The v002 direction labels are descriptive sign labels, not profitability labels and not strategy labels. They are not safe to read as "predicted direction"; they are the realized sign of the measured forward log return at the labeled horizon. A future deadband, bp-threshold, or cost-based threshold variant requires a separately authorized v002 schema-amendment memo.

## 20. Finalized null / censoring policy (multi-day, envelope-bounded)

- **Keep all feature rows** in the label artefact. Per per-day label parquet, the `row_count` equals the corresponding per-day feature parquet's `row_count`. The aggregate `row_count` across all 90 per-day label parquets is expected to equal `155,153,449`.
- **Do not drop** right-edge rows.
- For each horizon `H` independently:
  - if `target_timestamp_ms > envelope_terminal_unix_ms` (the maximum `source_transact_time_ms` across the entire v002 90-day envelope), set `horizon_censored_flag_H = true` and all that horizon's label columns (regression + classification + reference row + reference timestamp) to `null`.
- `label_any_censored_flag = true` if **any** horizon is censored for that row.
- If invalid price is encountered:
  - set affected label columns to `null`,
  - set `label_invalid_price_flag = true`.
- Invalid price must be unexpected for this artefact (the Phase 4bb-D raw gate and Phase 4bl-D-R raw multi-day gate confirmed all rows passed `validate_aggtrade_payload` with positive price and quantity; the Phase 4bm-B normalization preserves rows 1-for-1 in Decimal-as-string form). The future label implementation must record invalid-price counts in the label manifest and the structural QA report.
- **No forward-fill of censored labels** beyond the envelope-terminal `source_transact_time_ms`.
- **No cross-envelope stitching.** Horizons may cross UTC day boundaries within the v002 90-day envelope; they may **never** cross the envelope-terminal boundary (2025-02-28 23:59:59.999 UTC). v001's per-day censoring policy is **replaced** in v002 by envelope-terminal censoring; this is the only v002-specific deviation from Phase 4bj-B §16.

## 21. Finalized dtype policy

(mirror of Phase 4bj-B §17)

- `row_index`: `int64`.
- `agg_trade_id`: `int64`.
- All timestamp columns (`feature_timestamp_ms`, `source_transact_time_ms`, `reference_timestamp_ms_*`): `int64` representing UTC milliseconds.
- Hashes, dataset IDs, dataset / schema versions, symbol, `utc_date`: `string`.
- `forward_log_return_*`: nullable `float64`.
- `forward_direction_*`: nullable `int8` with values `{-1, 0, 1, null}`.
- `reference_row_index_*`: nullable `int64`.
- `horizon_censored_flag_*`: non-nullable `bool`.
- `label_invalid_price_flag`: non-nullable `bool`.
- `label_any_censored_flag`: non-nullable `bool`.
- `label_config_hash`: `string`.
- **No NaN values** in any column (including float columns).
- **No inf values** in any column.
- **Null is allowed only** in the columns explicitly typed as nullable above and only under the censoring / invalid-price conditions defined in §20.

## 22. Finalized lineage / identity policy

Lineage / identity columns must be present in **every** v002 label row (constant or per-day-constant within each per-day label parquet, as marked in §14). The pinned values are:

- `dataset_family` = `"microstructure_labels_aggtrades_v001"`
- `dataset_version` = `"v002"`
- `label_schema_version` = `"v001"`
- `source_feature_dataset_family` = `"microstructure_features_aggtrades_v001"`
- `source_feature_dataset_version` = `"v002"`
- `source_feature_manifest_sha256` = `"512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"`
- `source_feature_parquet_sha256` = (per-day-constant) read from the v002 feature manifest's `per_day_outputs` entry for that day
- `source_feature_successor_state_sha256` = `"7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4"` (Phase 4bm-L)
- `source_phase_4bm_j_gate_report_sha256` = `"3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"`
- `source_normalized_manifest_sha256` = `"01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"`
- `source_raw_manifest_sha256` = `"016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"`
- `symbol` = `"BTCUSDT"`
- `utc_date` = per-day-constant (one of `["2024-12-01", "2024-12-02", ..., "2025-02-28"]`; 90 distinct values across 90 per-day parquets)

Per-row identity columns:

- `row_index`: matches per-day feature parquet row by row.
- `agg_trade_id`: matches per-day feature parquet row by row.
- `feature_timestamp_ms`: matches per-day feature parquet `feature_timestamp_ms` row by row.
- `source_transact_time_ms`: matches per-day feature parquet `source_transact_time_ms` row by row.

## 23. Finalized label manifest schema

The future v002 label manifest, if later implemented by a separately authorized phase, must include at minimum:

| field | value |
| ----- | ----- |
| `dataset_family` | `microstructure_labels_aggtrades_v001` |
| `dataset_version` | `v002` |
| `label_schema_version` | `v001` |
| `source_feature_dataset_family` | `microstructure_features_aggtrades_v001` |
| `source_feature_dataset_version` | `v002` |
| `source_feature_manifest_sha256` | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` |
| `source_feature_manifest_sidecar_sha256` | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` |
| `source_feature_successor_state_sha256` | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (Phase 4bm-L) |
| `source_feature_successor_state_sidecar_sha256` | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` |
| `source_phase_4bm_j_gate_report_sha256` | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` |
| `source_phase_4bm_j_gate_sidecar_sha256` | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` |
| `source_normalized_manifest_sha256` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| `source_normalized_manifest_sidecar_sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |
| `source_phase_4bm_f_derived_successor_state_sha256` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` |
| `source_phase_4bm_d_derived_gate_report_sha256` | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` |
| `source_raw_manifest_sha256` | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| `source_acquisition_log_sha256` | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| `source_phase_4bl_e_raw_successor_state_sha256` | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` |
| `source_phase_4bl_d_r_raw_gate_report_sha256` | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| `symbol` | `BTCUSDT` |
| `symbol_list` | `["BTCUSDT"]` |
| `utc_date_start` | `2024-12-01` |
| `utc_date_end` | `2025-02-28` |
| `date_count` | `90` |
| `row_count` | aggregate across all 90 per-day label parquets; expected `155153449` |
| `column_count` | `40` |
| `label_list` | the eight finalized labels in canonical order |
| `support_column_list` | the 12 per-horizon support columns + 2 global support columns in canonical order |
| `lineage_column_list` | the 17 lineage / identity / metadata columns in canonical order |
| `horizon_list` | `["1s", "5s", "15s", "60s"]` |
| `horizon_ms_list` | `[1000, 5000, 15000, 60000]` |
| `envelope_terminal_unix_ms` | the maximum `source_transact_time_ms` across the v002 90-day envelope (computed deterministically by the future kernel) |
| `nullable_tail_policy` | text description of §20 (envelope-terminal censoring) |
| `reference_price_policy` | text description of §17 (multi-day cross-day-allowed; envelope-bounded) |
| `direction_threshold_policy` | text description of §19 (strict sign; threshold = `0.0`; no dead-band) |
| `label_config_hash` | deterministic SHA256 over canonical JSON of all schema-locking fields (see §25) |
| `chronological_split_policy` | `not_yet_defined` |
| `governance_labels.labels` | `allowed_by_future_phase_only` |
| `governance_labels.targets` | `allowed_by_future_phase_only` |
| `governance_labels.ml` | `forbidden` |
| `governance_labels.strategy` | `forbidden` |
| `governance_labels.backtest` | `forbidden` |
| `governance_labels.acquisition` | `unauthorized` |
| `governance_labels.paper_shadow_live` | `forbidden` |
| `governance_labels.deployment` | `forbidden` |
| `governance_labels.exchange_write` | `forbidden` |
| `governance_labels.phase_id` | `4bm-O` (prospective; future, not authorized by this memo) |
| `research_eligible` | `false` |
| `eligibility_gate_status` | `pending` |
| `label_family_research_use_authorized` | `false` |
| `stage_5_label_cleared` | `false` |
| `code_commit_sha` | recorded by the future implementation phase at run time |
| `created_at_unix_ms` | recorded by the future implementation phase at run time |
| `invalid_price_row_count` | int (expected `0` for the v002 envelope, given Phase 4bl-D-R / Phase 4bm-D PASS evidence) |
| `censored_per_horizon` | object mapping horizon → row count (counts of `horizon_censored_flag_H = true` aggregated across all 90 per-day label parquets) |
| `per_day_outputs` | ordered list of 90 per-day label parquet entries, each with: `utc_date`, label parquet path, label parquet SHA256, label sidecar SHA256, byte size, row count, per-horizon censored counts, invalid-price row count |
| `files[]` | flat list of all 90 label-parquet file entries with sha256, byte size, row count (alternative to `per_day_outputs` if v002 manifest schema prefers a flat list — future implementation must pick one and document the choice) |

The future v002 label manifest must:

- be governed by the same Phase 4aw `MicrostructureManifest` model, unless a separately authorized memo amends that model;
- preserve the Phase 4aw `flip_research_eligible(...)` always-raises invariant — the manifest's `research_eligible` flag may only be flipped to `true` by a separately authorized successor phase, and this v002 schema does **not** authorize it.

## 24. Finalized label parquet path convention

Proposed and finalized for future implementation only, **not created now**:

- per-day label parquet: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet`
- per-day label parquet paired sidecar: same path with `.sha256` suffix
- label manifest: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`
- label manifest paired sidecar: same path with `.sha256` suffix
- future label gate-report directory: `data/microstructure/gate-reports/labels/`
- future label successor-state directory: `data/microstructure/successor-state/` (sibling label successor-state files only; feature / derived / raw successor-state files must not be modified)

For each of the 90 v002 dates `D` in `[2024-12-01, 2025-02-28]`, the per-day label parquet path expands as:

```text
data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet
```

(e.g., `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/2024/12/BTCUSDT-labels-aggtrades-2024-12-01.parquet` through `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/2025/02/BTCUSDT-labels-aggtrades-2025-02-28.parquet`).

The entire `data/microstructure/` tree remains gitignored under `.gitignore:85`, so any future v002 label implementation must write only inside that gitignored namespace and must not produce tracked files under `data/microstructure/`.

Phase 4bm-N does not create any of the above paths.

## 25. Finalized `label_config_hash` policy

The future v002 label-kernel implementation must compute a deterministic `label_config_hash` as follows (mirror of Phase 4bj-B §20 with v002 lineage substitutions):

- Build a canonical-JSON object with **sorted keys** containing the following fields **and only these fields**:
  - `dataset_family`
  - `dataset_version`
  - `label_schema_version`
  - `label_list` (canonical order from §15)
  - `support_column_list` (canonical order from §14)
  - `lineage_column_list` (canonical order from §14)
  - `horizon_list` (canonical order from §16)
  - `horizon_ms_list` (canonical order from §16)
  - `anchor_policy` (sectioned text from §17)
  - `future_reference_policy` (sectioned text from §17)
  - `direction_threshold_policy` (sectioned text from §19)
  - `null_censoring_policy` (sectioned text from §20)
  - `dtype_policy` (sectioned text from §21)
  - `source_feature_manifest_sha256` (§22)
  - `source_feature_successor_state_sha256` (§22)
  - `source_phase_4bm_j_gate_report_sha256` (§22)
  - `source_normalized_manifest_sha256` (§22)
  - `source_raw_manifest_sha256` (§22)
  - `feature_config_hash` (§22)
- Compute `sha256(canonical_json(config_object))`.
- Record the result as:
  - the value of the `label_config_hash` column in every v002 label-parquet row (constant across all 90 per-day label parquets), and
  - the value of `label_config_hash` in the v002 label manifest.
- The hash must be deterministic across reruns. Reordering keys, re-spacing JSON, or altering any of the above fields must change the hash. Any future v002 schema-amendment memo must record the new hash explicitly.

## 26. Finalized future validation and QA requirements

A future v002 label structural QA memo (multi-day analogue of Phase 4bj-D) must verify the v002 label artefacts against this section verbatim:

1. each of the 90 per-day label parquets exists at the canonical path;
2. each per-day label sidecar exists and matches recomputed SHA256;
3. v002 label manifest exists at the canonical path;
4. v002 label manifest sidecar exists and matches recomputed SHA256;
5. per-day label-parquet `row_count` equals corresponding per-day feature-parquet `row_count` for each of the 90 days;
6. aggregate label `row_count` across all 90 per-day label parquets equals `155153449`;
7. per-day label-parquet `row_index` parity with feature parquet row by row;
8. per-day label-parquet `agg_trade_id` parity with feature parquet row by row;
9. per-day label-parquet `feature_timestamp_ms` parity with feature parquet row by row;
10. per-day label-parquet `source_transact_time_ms` parity with feature parquet row by row;
11. lineage hashes (`source_feature_manifest_sha256`, `source_feature_parquet_sha256`, `source_feature_successor_state_sha256`, `source_phase_4bm_j_gate_report_sha256`, `source_normalized_manifest_sha256`, `source_raw_manifest_sha256`) match expected values across all 90 per-day label parquets;
12. `label_config_hash` is constant across all label rows (90 parquets × per-day rows);
13. `label_config_hash` matches the v002 label-manifest `label_config_hash`;
14. `forward_log_return_H` values reproduce the §18 formula on a predeclared sample of rows;
15. `reference_row_index_H` and `reference_timestamp_ms_H` reproduce the §17 future-reference policy on the same sample (including cross-day reference resolution where applicable);
16. no `NaN` or `inf` in any float column;
17. all `forward_direction_H` values are in `{-1, 0, 1, null}`;
18. horizon-censored flags match the predicate `target_timestamp_ms > envelope_terminal_unix_ms` for the v002 envelope (rather than v001's per-day-boundary predicate);
19. support columns (`reference_row_index_H`, `reference_timestamp_ms_H`, `horizon_censored_flag_H`, `label_invalid_price_flag`, `label_any_censored_flag`) are not interpreted as signals;
20. upstream artefact SHAs (v002 feature manifest + sidecar, all 90 per-day feature parquets + sidecars, Phase 4bm-J gate report + sidecar, Phase 4bm-L successor-state JSON + sidecar, Phase 4bm-F successor-state JSON + sidecar, Phase 4bm-D gate report + sidecar, v002 derived multi-day index manifest + sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-E raw successor-state JSON, Phase 4bl-D-R raw gate report) remain byte-identical pre/post run;
21. no `data/microstructure/` file outside the gitignored v002 label namespace was modified;
22. v002 feature manifest still reads `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false` on disk after the run.

A future v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E) must:

- be offline;
- be deterministic;
- write exactly one local gitignored v002 label gate report and paired sidecar under `data/microstructure/gate-reports/labels/`;
- **never** flip the v002 label manifest's `research_eligible` flag to `true`;
- **never** transition the v002 label manifest's `eligibility_gate_status` to `pass` on the actual manifest (gate-report-level recommendation only, mirroring the Phase 4bf / 4bi-B / 4bm-D / 4bm-J precedent);
- not authorize ML, strategy, backtest, or acquisition;
- preserve the Phase 4al refined no-rescue rule and the Phase 4ak M0 twelve-clause gate.

## 27. Finalized forbidden outputs

A future v002 label-kernel implementation must **not** create:

- any column named anything that contains the substring `pnl`, `profit`, `loss`, `mfe`, `mae`, `r_multiple`, `equity`, `position`, `alpha`, `edge`, `prediction`, `model`, `score`, `decision`, `strategy`, `entry`, `exit`, `signal`, `target`, `barrier`, or `liquidation` (forbidden-substring detector applied per Phase 4bh-A / Phase 4bh-B / Phase 4bj-B precedent);
- any column derived from mark price, index price, bid / ask, book data, order-book imbalance, funding, OI, liquidation, or other external data;
- any column that uses future v002 feature values to alter v002 feature semantics;
- any centered-window derivation;
- any train / validation / test split assignment column;
- any ML model artefact;
- any backtest artefact;
- any strategy logic;
- any paper / shadow / live runtime artefact;
- any modification to the v002 feature manifest, v002 feature manifest sidecar, any of the 90 v002 per-day feature parquets, any of the 90 v002 per-day feature sidecars, Phase 4bm-L successor-state JSON or sidecar, Phase 4bm-J gate report or sidecar, Phase 4bm-F successor-state JSON or sidecar, Phase 4bm-D gate report or sidecar, v002 derived multi-day index manifest or sidecar, v002 raw manifest, v002 acquisition log, Phase 4bl-E successor-state JSON, or Phase 4bl-D-R gate report;
- any flip of `research_eligible` on the v002 raw manifest, v002 derived manifest, or v002 feature manifest (the Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved);
- any transition of `eligibility_gate_status` on the v002 raw manifest, v002 derived manifest, or v002 feature manifest;
- any mark of `stage_4_feature_cleared = true` on the v002 feature manifest;
- any v001 label artefact mutation (the Phase 4bj-G v001 label successor-state, the v001 label manifest, the v001 label parquet, and v001 label sidecars must remain byte-identical pre/post any v002 label work).

## 28. Finalized chronological split policy

`chronological_split_policy = "not_yet_defined"` at v002 (mirror of Phase 4bj-B §24).

- No train / validation / test split is finalized by Phase 4bm-N.
- A future v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) must be separately authorized and must occur before any ML training or strategy evaluation.
- Any future v002 split policy must be **chronological only**, predeclared before evaluation, locked in the v002 label manifest, and lineage-bound to the v002 feature manifest, the Phase 4bm-L successor-state, the Phase 4bm-J gate report, and the v002 derived / raw manifests.

## 29. Finalized no-rescue / M0 policy

(mirror of Phase 4bj-B §25)

The Phase 4al refined no-rescue rule applies verbatim:

> No future memo, no future label, no future evaluation, and no future ML training may, in effect, restate or rescue R2 / F1 / D1-A / V2 / G1 / C1 / 5m-thread rules under a different name.

The Phase 4ak M0 twelve-clause gate applies prospectively:

> v002 Feature Stage-5 admissibility is upstream of M0. M0 still applies to any future hypothesis, label, target, strategy, or backtest. v002 Feature Stage-5 admissibility does not bypass M0.

Operational consequences for v002:

- labels are **not** signals;
- labels are **not** strategies;
- forward returns are **not** strategy returns;
- direction accuracy is **not** profitability;
- MFE / MAE / R-multiple labels remain forbidden at v002;
- cost-adjusted expectancy requires a later separately authorized strategy / backtest phase that applies §11.6 = 8 bps HIGH per side verbatim;
- a future v002 label kernel implementation / v002 label structural QA / v002 label-family eligibility gate / v002 label-family research-use decision / v002 label-family successor-state recording memo or implementation must clear M0 for any interpretation, decision, or admissibility transition it proposes;
- no v002 label memo may interpret Phase 4bm-L Stage-5 admissibility as Stage-6 research-eligibility or as strategy authorization;
- the actual v002 raw manifest, v002 derived manifest, and v002 feature manifest must remain `research_eligible: false / eligibility_gate_status: "pending"` for the lifetime of v002 unless a separately authorized phase changes that explicitly under M0 and no-rescue;
- v001 label decisions (Phase 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K) do **not** transitively authorize any v002 label computation.

## 30. Future implementation acceptance criteria (Phase 4bm-O or equivalent)

A future v002 label-kernel implementation phase may be acceptable only if **all** of the following are satisfied:

1. it is **separately authorized** by an explicit operator decision;
2. it implements **exactly** this Phase 4bm-N schema (column names, horizons, formulas, dtypes, lineage, support columns, manifest fields, paths) without amendment;
3. it writes only **gitignored** label artefacts under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/`, `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002*`, `data/microstructure/gate-reports/labels/`, and `data/microstructure/successor-state/` (the latter only for sibling v002 label successor-states; v002 feature / derived / raw successor-states must not be touched);
4. it refuses to overwrite any existing local artefact under the same names;
5. it preserves all 90 v002 feature parquet SHAs byte-identically;
6. it preserves the v002 feature manifest byte-identically (no field flip; no reordering; no whitespace change);
7. it preserves the Phase 4bm-L successor-state JSON byte-identically;
8. it preserves the Phase 4bm-J gate report byte-identically;
9. it preserves the Phase 4bm-F successor-state JSON byte-identically;
10. it preserves the Phase 4bm-D gate report byte-identically;
11. it preserves the v002 derived multi-day index manifest byte-identically;
12. it preserves the v002 raw manifest byte-identically;
13. it preserves the v002 acquisition log byte-identically;
14. it preserves the Phase 4bl-E raw successor-state JSON byte-identically;
15. it preserves the Phase 4bl-D-R raw gate report byte-identically;
16. it creates **no** ML models;
17. it creates **no** strategy signals;
18. it creates **no** backtests;
19. it creates **no** column whose name matches any forbidden-substring listed in §27;
20. it keeps the v002 label manifest `research_eligible: false / eligibility_gate_status: "pending" / label_family_research_use_authorized: false / chronological_split_policy: "not_yet_defined"`;
21. it records `label_config_hash` per §25;
22. it records horizon-censoring counts in the v002 label manifest, both aggregate across the 90 days and per-day;
23. it records invalid-price row count in the v002 label manifest (expected `0` for the v002 envelope given upstream gate evidence);
24. it records `envelope_terminal_unix_ms` deterministically in the v002 label manifest;
25. it passes label-specific tests, microstructure tests, `ruff`, `mypy`, and whole-repo `pytest` with no new failures beyond the documented Phase 4bm-J / Phase 4bm-H baseline;
26. it produces a closeout report under `docs/00-meta/implementation-reports/` recording the same discipline as Phase 4bm-H / Phase 4bm-J / Phase 4bm-L / Phase 4bm-M;
27. it does not authorize any v002 label structural QA, v002 label-family eligibility gate, v002 label-family research-use decision, v002 label-family successor-state recording, v002 chronological-split-policy memo, Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow / live, exchange-write, production keys, authenticated APIs, private endpoints, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, or credentials.

## 31. Future v002 label QA / gate sequence (none authorized)

Phase 4bm-N recommends the following future v002 phase sequence (none authorized here):

- **Phase 4bm-O** (provisional name) — Multi-Day V002 Label Kernel Implementation + Local Label Artefact Generation. Implements exactly this Phase 4bm-N schema; produces 90 per-day label parquets, v002 label manifest, paired canonical Phase 4bb-F sidecars locally under the gitignored namespace.
- **Phase 4bm-P** (provisional name) — Multi-Day V002 Label Artefact Structural QA Memo (analysis-and-docs only; read-only). Verifies the v002 label artefacts against §26 verbatim.
- **Phase 4bm-Q** (provisional name) — Multi-Day V002 Label-Family Eligibility Gate Design + Implementation + Execution. Mirrors Phase 4bm-J for the v002 label family; emits a v002 label gate report; never flips the v002 label manifest's `research_eligible` to `true`.
- **Phase 4bm-R** (provisional name) — Multi-Day V002 Label-Family Research-Use Decision Memo (docs-only). Decides whether the v002 label family is admissible in principle for research-use at policy level (mirror of Phase 4bm-K for v002 labels).
- **Phase 4bm-S** (provisional name) — Multi-Day V002 Label-Family Successor-State Recording (docs + local gitignored output). Mirrors Phase 4bm-L for v002 labels; records the policy decision in a sibling successor-state artefact while preserving the v002 label manifest byte-identically.
- (Provisional) — Multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I).
- (Provisional) — Multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J).

**No phase in the above sequence is authorized by Phase 4bm-N.** Future phase IDs (`4bm-O`, `4bm-P`, etc.) are provisional names; the operator may rename or re-letter them at authorization time. v001 label decisions (Phase 4bj-A through Phase 4bj-K) do **not** transitively authorize any v002 label computation.

## 32. What this phase proves

Phase 4bm-N proves only the following:

- a fully specified, leakage-safe, deterministic v002 label schema exists at memo level for the future v002 label family `microstructure_labels_aggtrades_v001 @ v002`;
- the schema preserves all upstream v002 artefact SHAs and the byte-immutability discipline of Phase 4bm-H / Phase 4bm-J / Phase 4bm-L / Phase 4bm-M;
- the schema is compatible with the Phase 4aw `MicrostructureManifest` model and with the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- the schema extends Phase 4bj-B's v001 column shape cleanly to multi-day v002 envelope with three explicit v002-specific adaptations (multi-day lineage SHAs; v002-explicit raw lineage; multi-day end-of-envelope censoring);
- a future v002 label-kernel implementation is **possible** if separately authorized, and **bounded** by sections 12–30 of this memo;
- the no-rescue, no-leakage, no-shuffling, cost-aware, M0-bound, Phase 4al-bound interpretation of v002 labels is locked.

## 33. What this phase does not prove

Phase 4bm-N does **not** prove:

- that any v002 label has predictive value;
- that forward log returns at any v002 horizon are forecastable;
- that direction classification at any v002 horizon is forecastable;
- that any v002 label-based ML model would generalize;
- that any v002 label-based strategy would be edge-positive;
- that the v002 label schema is the **right** schema (only that it is the **finalized** schema for this lifecycle pass);
- that mark-price stop-domain forensics is admissible at v002;
- that aggTrades-domain barrier labels are admissible at v002 first pass;
- that ETHUSDT or any other symbol is admissible at v002;
- that horizons beyond `{1s, 5s, 15s, 60s}` are admissible at v002 first pass;
- that ML training is authorized at v002;
- that strategy work is authorized at v002;
- that backtest work is authorized at v002;
- that paper / shadow / live work is authorized at v002;
- that v001 label decisions transitively authorize v002 label computation;
- that any future v002 label phase is authorized.

## 34. Non-authorization

Phase 4bm-N does **not**, and **cannot**, authorize:

- Phase 4bm-O (any provisional successor; not authorized);
- multi-day v002 label-kernel implementation (multi-day analogue of Phase 4bj-C);
- multi-day v002 label artefact generation;
- multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D);
- multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E);
- multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F);
- multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G);
- multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I);
- multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J);
- multi-day v002 diagnostics;
- multi-day v002 ML training, model selection, feature ranking, meta-labeling;
- multi-day v002 strategy specification, implementation, signal construction;
- multi-day v002 backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price / order-book / funding / OI / liquidation / cross-venue data, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*;
- Phase 5;
- Phase 4 canonical;
- paper / shadow;
- live-readiness;
- deployment;
- exchange-write;
- production-key creation;
- authenticated APIs;
- private endpoints;
- public-endpoint calls in code;
- user-stream / live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1, Phase 4bm-D-P1, Phase 4bm-E, Phase 4bm-F, Phase 4bm-G, Phase 4bm-H, Phase 4bm-I, Phase 4bm-J, Phase 4bm-K, Phase 4bm-L, or Phase 4bm-M;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (Phase 4bm-N creates **no** new successor-state artefact).

## 35. Recommended state

**Remain paused.**

Phase 4bm-N is docs-only. It is branch-complete only by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-N is **not** project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived / feature / label-design family now has a complete ladder of evidence through **v002 Label Stage-1 (schema finalized at memo level)**, plus the Phase 4bm-L machine-readable v002 Feature Stage-5 marker, plus the Phase 4bm-M v002 Label Stage-0 boundary / design memo. No label artefact, label manifest, label gate report, or label successor-state exists or is authorized to exist by this phase.

## 36. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 label lifecycle ladder** — Phase 4bm-O (multi-day v002 label-kernel implementation + local label artefact generation; multi-day analogue of Phase 4bj-C) | code + docs + local gitignored output | **NOT authorized by this memo** |
| **Conditional later** — multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D) | docs + read-only analysis | **NOT authorized** |
| **Conditional later** — multi-day v002 label-family eligibility gate (multi-day analogue of Phase 4bj-E) | code + docs + local gitignored gate report | **NOT authorized** |
| **Conditional later** — multi-day v002 label-family research-use decision memo (multi-day analogue of Phase 4bj-F) | docs-only | **NOT authorized** |
| **Conditional later** — multi-day v002 label-family successor-state recording (multi-day analogue of Phase 4bj-G) | docs + local gitignored successor-state JSON | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized** |
| **Conditional later** — future multi-day v002 chronological-split-policy successor-state recording (multi-day analogue of Phase 4bj-J) | docs + local gitignored successor-state JSON | **NOT authorized** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-N** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-N** |

## 37. Preserved boundaries

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-N).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L / 4bm-M results — all preserved verbatim.

## 38. Validation commands and results

### Initial verification (pre-edit)

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-n/multi-day-v002-label-schema-finalization-memo` |
| `git rev-parse main` | `e74dc13021900a54153cba81eaed8fdb397fb292` |
| `git rev-parse origin/main` | `e74dc13021900a54153cba81eaed8fdb397fb292` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `e74dc13 docs(phase-4bm-m): finalize merge closeout shas` (matches expectation) |

### Read-only SHA verification (recomputed on disk at the start of this phase)

| Artefact | SHA256 (recomputed) | Expected | Match |
| -------- | ------------------- | -------- | ----- |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | same | ✓ |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | same | ✓ |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | ✓ |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | same | ✓ |

### Post-edit validation

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock`, `data/research/` (untracked, expected), plus the three tracked Phase 4bm-N docs files |
| `git diff --check` | clean (no whitespace errors; exit 0) |
| `git diff --name-only` | exactly three tracked docs paths: this memo, the closeout, and the narrow `docs/00-meta/current-project-state.md` update |

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by Phase 4bm-N. Per the standing precedent for Tier 1 docs-only schema-finalization memos (Phase 4bj-B v001 label schema finalization, Phase 4bh-B v001 feature schema finalization, Phase 4bj-A v001 label-boundary, Phase 4bg-A v001 derived-family research-eligibility, Phase 4bi-C v001 feature-family research-use, Phase 4bm-A multi-day normalization design, Phase 4bm-E multi-day derived-family research-eligibility decision, Phase 4bm-G v002 feature-boundary design, Phase 4bm-K v002 feature-family research-use decision, Phase 4bm-M v002 label-family boundary / design — each of which deliberately skipped these gates for the same reason), the code / type / test gate subset is not invoked here. No source / test / script / configuration file is modified. The Phase 4bm-J branch quality gates (Phase 4bm-J surface `ruff check` PASS, whole-repo `ruff check .` PASS, targeted gate pytest 53 PASS) and the Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files; whole-repo `pytest`: 15 collection errors + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures, both env baseline) remain unchanged by construction because Phase 4bm-N modifies no existing source / test / script.

## 39. Quality gate results / skipped-check rationale

- `git diff --check`: clean (exit 0).
- Repo-standard markdown lint or check: no project-specific lightweight markdown gate exists in this repository; therefore none is run.
- `ruff check`, `mypy src/prometheus`, `pytest` — see §38 "Tools deliberately not run".

## 40. No source / test / script / config modified

- No file under `src/prometheus/` modified.
- No file under `tests/` modified.
- No file under `scripts/` modified.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, MCP file, or credential file modified.
- The only tracked changes are the three docs files (this implementation report + the closeout + a narrow `current-project-state.md` paragraph addition + new "Current phase:" block update).

## 41. No labels / diagnostics / ML / strategy / backtests authorized or performed

- No label kernel designed at code level; no label kernel run; no label parquet created; no label manifest created; no label sidecar created; no label gate report created; no label successor-state JSON created.
- No diagnostics run; no diagnostic output created.
- No ML training, model selection, feature ranking, meta-labeling, or hyperparameter search performed.
- No strategy specification, signal construction, or strategy-spec memo created.
- No backtest specification, plan, or execution performed.
- No simulation run; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output computed.

## 42. No endpoint / credential / MCP / Graphify / exchange-write surface touched

Phase 4bm-N touched no network surface. No Binance endpoint (public, authenticated, or private) was called. No `data.binance.vision`, `fapi.binance.com`, or `api.binance.com` was contacted. No WebSocket was opened. No `.env` was read or created. No `.mcp.json` was read or created. MCP / Graphify was not enabled. No order was placed. No exchange-write surface was contacted.

## 43. Required exact phrases (verbatim, per task brief)

- **Phase 4bm-N is label schema finalization only.**
- **No label artefact exists after Phase 4bm-N.**
- **Phase 4bm-O is not authorized by Phase 4bm-N.**
- **Label computation is not authorized by Phase 4bm-N.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-N.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
