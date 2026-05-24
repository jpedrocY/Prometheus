# Phase 4bm-M — Multi-Day V002 Label-Family Boundary / Design Memo

**Phase identity:** Phase 4bm-M — Multi-Day V002 Label-Family Boundary / Design Memo (docs-only label-boundary / design memo; multi-day v002 analogue of Phase 4bj-A).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-m/multi-day-v002-label-family-boundary-design-memo`.
**Base:** `main` at `38cf6693425f91e85e2d5a295800aa5ee2287db3` (Phase 4bm-L merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bj-A label-boundary precedent. First-of-kind multi-day v002 label-family boundary memo; any phase that defines future target / label semantics for a Stage-5-admissible feature family can affect downstream ML admissibility and therefore escalates to Tier 1 under §3 ("creates features / labels / diagnostics" / "affects eligibility / admissibility / downstream authorization").
**Phase type:** docs-only boundary / design memo. Adds two new tracked docs files under `docs/00-meta/implementation-reports/` and narrowly updates `docs/00-meta/current-project-state.md`. **No** local gitignored output is created. **No** source / test / script / configuration / manifest / sidecar / gate-report / successor-state mutation. **No** label parquet, label sidecar, label manifest, label gate report, or label successor-state JSON created. **No** `data/microstructure/` file is created, modified, deleted, renamed, or committed.
**Status:** drafted; pending operator review. Branch-complete only by this work; not merged into `main`; not project-complete.

---

## 1. Phase header

This phase records the **future label-family boundary** for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002`, given the Phase 4bm-L machine-readable v002 Feature Stage-5 research-use admissibility marker (sibling successor-state JSON SHA `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4`). It does not compute, validate, schema-finalize, or otherwise materialize any label artefact. It defines, at policy level only, the future label-family boundary that any future label phase must respect.

Phase 4bm-M is the **multi-day v002 analogue of Phase 4bj-A** (the v001 label-boundary / target-definition memo merged on `main`). Phase 4bj-A is the primary structural precedent. Where v001 Phase 4bj-* lifecycle has progressed beyond the boundary memo (Phase 4bj-B schema finalization, Phase 4bj-C implementation, Phase 4bj-D structural QA, Phase 4bj-E eligibility gate, Phase 4bj-F research-use decision, Phase 4bj-G successor-state recording, Phase 4bj-H / 4bj-I chronological split policy, Phase 4bj-J split-policy successor-state, Phase 4bj-K closeout), Phase 4bm-M cites those later phases only to avoid designing a boundary that would conflict with their established label lifecycle requirements; Phase 4bm-M does **not** authorize a multi-day v002 equivalent of any of them.

## 2. Scope

Phase 4bm-M defines, at policy level only:

- the future multi-day v002 label-family identity (proposed dataset family, dataset version, label schema version, source feature / source normalized / source raw lineage anchor fields);
- the proposed future label manifest path convention;
- the proposed future label parquet path convention;
- the proposed future label sidecar convention (Phase 4bb-F canonical format);
- the allowed future label categories (forward returns, horizon-validity flags, etc., subject to v001 Phase 4bj-A / 4bj-B precedent);
- the forbidden future label categories (strategy entry / exit decisions, PnL, equity, model predictions / scores, post-model labels, mark-price stop labels at v001 scope, cross-venue / external data labels, etc.);
- the future-data access policy (features must remain causal; labels may use future information **only** inside label generation; labels must live in a separate artefact family; future-looking fields are forbidden from feature columns);
- the timestamp / leakage policy (UTC only; deterministic event ordering; same-timestamp tie handling; end-of-sample censoring; multi-day horizon handling);
- the multi-day horizon / boundary policy (90 contiguous UTC days 2024-12-01 .. 2025-02-28 inclusive; end-of-dataset rows with insufficient future horizon must be censored / null / invalid; no acquisition beyond the 90 locked v002 dates is authorized by this phase);
- the proposed future label lineage fields;
- the proposed future label timestamp fields;
- the proposed future label manifest required fields and default governance values;
- the future label implementation gate prerequisites (which separately authorized phases must occur before any label artefact may exist);
- what this memo proves and what it does not prove;
- explicit non-authorization for every successor phase and every downstream activity.

## 3. Non-scope

Phase 4bm-M does **not**:

- modify source code, tests, scripts, configurations;
- modify the v002 feature manifest, v002 feature manifest sidecar, v002 per-day feature Parquets, v002 per-day feature sidecars;
- modify the Phase 4bm-J v002 feature-family eligibility-gate report or its sidecar;
- modify the Phase 4bm-L v002 feature-family Stage-5 successor-state JSON or its sidecar;
- modify the Phase 4bm-F v002 derived-family Stage-3 successor-state JSON or its sidecar;
- modify the Phase 4bm-D v002 derived-family gate report or its sidecar;
- modify the v002 derived multi-day index manifest or its sidecar;
- modify the v002 raw manifest, v002 acquisition log, Phase 4bl-D-R raw multi-day gate report, or Phase 4bl-E raw multi-day successor-state JSON;
- modify any prior gate report, prior successor-state JSON, or prior manifest;
- create labels, targets, signals, ML, strategy, diagnostics, or backtest artefacts;
- create any label parquet, label sidecar, label manifest, label manifest sidecar, label gate report, or label successor-state JSON;
- compute returns, alpha, edge, predictiveness, opportunity rate, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, decision score, entry / exit signal, taker imbalance, sweep detection, aggressive-flow score, spread / depth / liquidity / slippage / order-flow / execution-quality proxies, or any other quantitative output;
- train ML; design strategy logic; run backtests, simulations, or paper / shadow;
- acquire data; call public endpoints, Binance APIs, or private endpoints; open WebSockets; request, store, or use credentials; read or create `.env`; create or read `.mcp.json`; enable MCP or Graphify;
- flip `research_eligible` on any actual manifest; transition `eligibility_gate_status` on any actual manifest; mark `stage_4_feature_cleared = true` on any actual manifest; change `chronological_split_policy` on any actual manifest;
- mutate the v002 feature manifest, any upstream manifest, any prior gate report, or any prior successor-state JSON in any way;
- amend M0; revise any retained verdict; change any project lock;
- authorize Phase 4bm-N, multi-day v002 label-family schema, multi-day v002 label-kernel implementation, multi-day v002 label structural QA, multi-day v002 label-family eligibility gate, multi-day v002 label-family research-use decision, multi-day v002 label-family successor-state recording, multi-day v002 chronological-split-policy memo, multi-day v002 diagnostics, multi-day v002 ML / strategy / backtest, Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, live WebSocket implementation;
- commit anything under `data/microstructure/`.

## 4. Linkage to Phase 4bm-L machine-readable v002 Feature Stage-5 marker

Phase 4bm-M is admissible **only because** Phase 4bm-L recorded a machine-readable v002 Feature Stage-5 research-use admissibility marker as a sibling successor-state artefact while preserving the original v002 feature manifest byte-identically.

Phase 4bm-L's marker is interpreted as follows:

- the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002` is **admissible in principle at policy level** for research-use, equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`;
- the **actual** v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` remains `research_eligible: false`, `eligibility_gate_status: "pending"`, `stage_4_feature_cleared: false` byte-identically;
- any tool that interprets the v002 feature family as Stage-5-admissible must read the Phase 4bm-L successor-state JSON, never the feature manifest;
- labels, targets, ML, strategy, backtests, diagnostics, and acquisition remain governance-forbidden / governance-unauthorized;
- Stage-5 admissibility is upstream of M0; the Phase 4ak twelve-clause M0 gate still applies prospectively to any future label, target, hypothesis, strategy, or backtest.

If at any future time the Phase 4bm-L successor-state SHA stops matching `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4`, Phase 4bm-M boundary content must be re-validated before any future label phase proceeds.

## 5. Linkage to Phase 4bm-K research-use decision

Phase 4bm-K recorded the policy-level v002 Feature Stage-5 research-use admissibility decision (Outcome 1 / Decision form 1; equivalent label `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) but explicitly required a separately authorized Phase 4bm-L successor-state recording phase before any machine-readable v002 Feature Stage-5 marker exists. Phase 4bm-L is that successor-state phase; Phase 4bm-M is now the next docs-only phase that defines the future multi-day v002 label-family boundary on top of that admissibility chain. Phase 4bm-K SHA-finalization commit `121865a26120d5f097fee95c00185ebd4c995703` is cited for traceability.

## 6. Linkage to Phase 4bm-J `FEATURE_GATE_PASS`

Phase 4bm-J is the report-level v002 Feature Stage-4 evidence:

- gate verdict: `FEATURE_GATE_PASS`;
- `overall_status`: `pass`;
- 50 / 50 PASS; 0 FAIL; 0 ERROR; 0 NOT_APPLICABLE; 0 blocking failures;
- gate report path: `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json`;
- gate report SHA256: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`;
- gate sidecar SHA256: `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`.

The Phase 4bm-J gate report is the report-level evidence cited by Phase 4bm-K and locked into the Phase 4bm-L successor-state JSON. Phase 4bm-M relies on it as the upstream lineage anchor for any future label manifest.

## 7. Linkage to Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`

Phase 4bm-I performed read-only structural QA over the Phase 4bm-H v002 feature artefacts and recorded verdict `FEATURE_STRUCTURAL_QA_PASS`. This verdict was machine-verified by Phase 4bm-J check A12 and is cited verbatim in the Phase 4bm-L successor-state JSON. Phase 4bm-M cites it as the structural QA anchor.

## 8. Linkage to Phase 4bm-H feature artefacts

The Phase 4bm-H v002 feature artefact provenance is the upstream lineage for any future v002 label artefact:

- feature manifest path: `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`;
- feature manifest SHA256: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`;
- feature manifest sidecar SHA256: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`;
- `feature_config_hash`: `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`;
- feature parquet count: 90;
- feature sidecar count: 90;
- total feature row count: 155,153,449;
- feature date range: 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days);
- symbol scope: BTCUSDT (one symbol);
- feature schema column count: 62 (17 lineage / identity / metadata + 45 feature / quality).

These values are read-only inputs to Phase 4bm-M. The 90 per-day v002 feature Parquets and 90 paired sidecars are not read, not opened, and not modified by this phase.

## 9. Linkage to Phase 4bj-A v001 label-family boundary precedent

Phase 4bj-A is the **primary structural precedent** for Phase 4bm-M:

- Phase 4bj-A is the v001 label-boundary / target-definition memo merged into `main`;
- it selected Outcome 1 — "Label boundary admissible in principle, implementation deferred";
- it defined allowed / forbidden future label classes, causal-separation rule, timestamp-anchoring rule, horizon policy, stop / risk-domain boundary, MFE / MAE / R-multiple boundary, forward-return boundary, classification vs regression boundary, multi-horizon boundary, cost / RR / WR / expectancy boundary, chronological-validation requirements, train / validation / test split boundary, symbol / date expansion boundary, no-rescue / M0 boundary, future label artefact namespace, future label manifest schema, future implementation acceptance criteria, and the future label QA / gate sequence;
- it recommended a conservative initial label family `microstructure_labels_aggtrades_v001` with forward-log-return and forward-direction columns at horizons {1s, 5s, 15s, 60s}.

Phase 4bm-M adopts the Phase 4bj-A structural precedent verbatim, transposed to the multi-day v002 feature family, with three deliberate v002-specific extensions:

1. **multi-day end-of-sample censoring** must be defined explicitly for horizons that exceed the 2025-02-28 boundary (rather than the v001 single-day 2025-01-15 boundary);
2. **multi-day chronological ordering** must be enforced across day boundaries (not just within a single UTC day);
3. **multi-day lineage fields** must reference all 90 per-day feature Parquets (not a single feature Parquet) and must anchor to the Phase 4bm-L successor-state SHA, the Phase 4bm-J gate report SHA, the v002 feature manifest SHA, the Phase 4bm-F derived-family successor-state SHA, the v002 derived multi-day index manifest SHA, the v002 raw manifest SHA, the Phase 4bl-E raw multi-day successor-state SHA, and the Phase 4bl-D-R raw multi-day gate report SHA.

Phase 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K are cited only to avoid designing a v002 boundary that would conflict with already-established label lifecycle requirements. **Phase 4bm-M does not transitively inherit any of those v001 phases' authorizations.** v001 label decisions do **not** automatically authorize v002 label computation.

## 10. Evidence SHA table (read-only; SHAs recomputed on disk at the start of this phase)

| # | Artefact | SHA256 | Status |
| - | -------- | ------ | ------ |
|  1 | v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL (verified) |
|  2 | v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |
|  3 | Phase 4bm-J v002 feature-family gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | IDENTICAL (verified) |
|  4 | Phase 4bm-J v002 feature-family gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | IDENTICAL |
|  5 | v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | IDENTICAL (verified) |
|  6 | v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | IDENTICAL |
|  7 | v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
|  8 | v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
|  9 | Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| 10 | Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | IDENTICAL |
| 11 | Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | IDENTICAL |
| 12 | Phase 4bm-D authoritative gate sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | IDENTICAL |
| 13 | Phase 4bm-F v002 derived-family Stage-3 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | IDENTICAL |
| 14 | Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | IDENTICAL |
| 15 | Phase 4bm-L v002 feature-family Stage-5 successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | IDENTICAL (verified) |
| 16 | Phase 4bm-L v002 feature-family Stage-5 successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | IDENTICAL |
| 17 | Phase 4bi-D v001 feature-family Stage-5 successor-state JSON (reference precedent only) | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` | IDENTICAL |

Read-only verification — Phase 4bm-M recomputed SHA256 for artefacts #1, #3, #5, #15 directly from disk and matched the recorded values byte-for-byte. The remaining artefact SHAs are taken verbatim from the Phase 4bm-L successor-state JSON `boundary_confirmations` block and the Phase 4bm-L implementation report Evidence Table §15.

| Other key facts | Value |
| --------------- | ----- |
| Phase 4bm-K decision | **Outcome 1 / Decision form 1** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) |
| Phase 4bm-K SHA-finalization commit | `121865a26120d5f097fee95c00185ebd4c995703` |
| Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` (`overall_status = pass`) |
| Phase 4bm-J check totals | 50 / 50 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking |
| Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` |
| Feature parquet count | 90 |
| Feature sidecar count | 90 |
| Total feature row count | 155,153,449 |
| Feature date range | 2024-12-01 .. 2025-02-28 inclusive (90 contiguous UTC days) |
| Symbol scope | BTCUSDT (one symbol) |
| Feature schema column count | 62 (17 lineage / identity / metadata + 45 feature / quality) |
| `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` |
| v002 feature manifest on-disk invariants | `research_eligible = false`; `eligibility_gate_status = "pending"`; `stage_4_feature_cleared = false` |

## 11. Proposed future label family name and versioning convention

If a future operator-authorized phase (e.g., a future Phase 4bm-N — Multi-Day V002 Label Schema Finalization Memo, or whatever name the operator chooses) lands, the proposed identity for the multi-day v002 label family is:

- `dataset_family`: `microstructure_labels_aggtrades_v001`
- `dataset_version`: `v002`
- `label_schema_version`: `v001`
- `source_feature_dataset_family`: `microstructure_features_aggtrades_v001`
- `source_feature_dataset_version`: `v002`
- `source_normalized_dataset_family`: `microstructure_normalized_aggtrades_v001`
- `source_normalized_dataset_version`: `v002`
- `source_raw_dataset_family`: `microstructure_raw_aggtrades_v001`
- `source_raw_dataset_version`: `v002`

Rationale: the family name is shared with the v001 label-family precedent (`microstructure_labels_aggtrades_v001`); the version `v002` is the multi-day v002 sibling of the v001 single-day labels (`v001`), exactly mirroring the v002 / v001 versioning pattern for raw, normalized, and feature families. The `label_schema_version` field is intentionally a separate identifier so that the schema can evolve independently of the dataset version if a future memo authorizes a schema change.

## 12. Proposed future label manifest naming convention

Proposed future label manifest path:

```text
data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json
```

Paired canonical Phase 4bb-F sidecar:

```text
data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json.sha256
```

Phase 4bm-M does not create either file. The entire `data/microstructure/` tree is gitignored under `.gitignore:85`, so any future implementation phase that produces a real label manifest must respect that gitignore rule and **must not** commit anything under `data/microstructure/`.

The proposed manifest naming follows the v002 feature manifest precedent at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` and the v002 derived multi-day index manifest precedent at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`.

## 13. Proposed future label parquet path convention

Proposed future per-day label parquet path:

```text
data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet
```

For the 90 locked v002 dates 2024-12-01 .. 2025-02-28, this would yield 90 per-day label Parquets (one per UTC date), each paired with a canonical Phase 4bb-F sidecar at the same path with a `.sha256` suffix.

This mirrors the Phase 4bm-H v002 feature parquet layout (`data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...`) and the Phase 4bm-B v002 normalized parquet layout (`data/microstructure/derived/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/...`).

Phase 4bm-M does **not** create any label parquet, sidecar, or directory.

## 14. Proposed future label sidecar convention

Every future per-day label parquet must be paired with a canonical Phase 4bb-F sidecar in the same directory with a `.sha256` suffix.

Canonical sidecar bytes (Phase 4bb-F):

```text
<sha256_lowercase_hex>  <basename_of_target_file><LF>
```

- 64-byte lowercase hex of the target file's recomputed SHA256;
- exactly two ASCII spaces (`0x20 0x20`);
- ASCII basename of the target file;
- single `0x0A` (LF) terminator;
- no CRLF anywhere; no BOM; ASCII only.

The same canonical-sidecar convention also applies to the future label manifest sidecar, the future label gate report sidecar (if any), and any future label successor-state JSON sidecar. Phase 4bb-F canonical path policy is preserved verbatim across all v002 label artefacts.

Phase 4bm-M does **not** create any sidecar.

## 15. Proposed future label lineage fields

Any future v002 label parquet must include lineage / identity / metadata columns that bind each label row to its v002 feature row provenance. The proposed minimum set (subject to a future schema-finalization phase locking exact column names, dtypes, and order):

- `row_index` (label row position; integer)
- `agg_trade_id` (carried verbatim from the v002 feature row)
- `symbol` (e.g., `"BTCUSDT"`)
- `utc_date` (label-row UTC date; `YYYY-MM-DD`)
- `feature_dataset_family` (= `"microstructure_features_aggtrades_v001"`)
- `feature_dataset_version` (= `"v002"`)
- `feature_config_hash` (= `"819cfa7a…7d7b5a1d"`)
- `feature_successor_state_sha256` (= `"7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4"`)
- `feature_gate_report_sha256` (= `"3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"`)
- `feature_manifest_sha256` (= `"512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"`)
- `normalized_manifest_sha256` (= `"01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"`)
- `raw_manifest_sha256` (= `"016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"`)
- `label_dataset_family` (= `"microstructure_labels_aggtrades_v001"`)
- `label_dataset_version` (= `"v002"`)
- `label_schema_version` (= `"v001"`)
- `label_config_hash` (computed by the future label kernel)
- `code_commit_sha` (the future label kernel's commit SHA)
- `created_at_unix_ms` (the label kernel's run timestamp)

A label parquet that cannot identify its feature lineage by the four SHAs above (`feature_manifest_sha256`, `feature_successor_state_sha256`, `feature_gate_report_sha256`, `normalized_manifest_sha256`) is invalid. The exact column list, order, dtypes, and validation rules are subject to a future schema-finalization phase.

## 16. Proposed future label timestamp fields

Each future v002 label row must carry the following timestamp / horizon fields (subject to schema finalization):

- `feature_timestamp_ms` (= the v002 feature row's `source_transact_time_ms`; integer, UTC milliseconds);
- `source_transact_time_ms` (carried verbatim from v002 feature row);
- one column per horizon recording the target reference timestamp (e.g., `forward_ref_ts_ms_<horizon>`), recorded only when the future horizon can be evaluated within the 90-day window;
- a censoring flag column per horizon (e.g., `forward_valid_<horizon>` or `forward_censored_<horizon>`) that is `true` when the future horizon falls beyond 2025-02-28 23:59:59 UTC (end of the locked v002 envelope) or otherwise cannot be evaluated; null label values must accompany the censoring flag.

All timestamps must be UTC. No local time zone. No synthetic timestamps. No resampling. Deterministic event ordering on `(feature_timestamp_ms, agg_trade_id, row_index)` is mandatory.

## 17. Proposed future source feature / source normalized lineage requirements

Any future v002 label manifest must cite the full upstream lineage chain verbatim:

- Phase 4bm-L v002 feature-family Stage-5 successor-state SHA: `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4`;
- Phase 4bm-J v002 feature-family gate report SHA: `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`;
- v002 feature manifest SHA: `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`;
- v002 feature manifest sidecar SHA: `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`;
- Phase 4bm-F v002 derived-family Stage-3 successor-state SHA: `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9`;
- Phase 4bm-D v002 derived-family gate report SHA: `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a`;
- v002 derived multi-day index manifest SHA: `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a`;
- v002 raw manifest SHA: `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`;
- Phase 4bl-E raw multi-day successor-state SHA: `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`;
- Phase 4bl-D-R raw multi-day gate report SHA: `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`;
- v002 acquisition log SHA: `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`.

A label manifest that does not record this full upstream lineage is invalid. The future label kernel's `code_commit_sha`, `label_config_hash`, and `created_at_unix_ms` must also be recorded.

## 18. Proposed future label schema categories (Phase 4bj-A / Phase 4bj-B precedent, transposed to v002)

The Phase 4bj-A v001 boundary memo defined five admissible-in-principle label classes; the Phase 4bj-B v001 schema-finalization memo selected and locked the actual v001 schema. Phase 4bm-M adopts the Phase 4bj-A class shape verbatim for v002, with no schema selection (schema selection is deferred to a future v002 schema-finalization phase, if and when separately authorized):

**Class A — `forward_log_return_<horizon>`** (numeric / regression-style).
Future realized log return from the v002 feature row timestamp `T` to a future reference timestamp at `T + horizon`. Anchor: the v002 feature row's price (carried from upstream feature lineage). Future prices are used only inside the label routine. Nullable / censored when no valid future reference price exists within the 90-day v002 window.

**Class B — `forward_direction_<horizon>`** (categorical / classification).
Derived from class A. Requires predeclared thresholds, locked in the label manifest's `label_threshold_metadata`. Typical variants: strict-sign, dead-band with predeclared bp width, ternary (up / flat / down) with predeclared cut-points. Threshold choices must be locked before any evaluation pass; never optimized on the evaluation window.

**Class C — `barrier_outcome_<horizon>` / `target_before_stop_<horizon>`** (categorical event label).
Records whether an upper barrier or lower barrier is touched first within a future horizon. Must be defined as a **label only**, never as a strategy rule. Requires separately defined barriers and explicit tie rules (same-record / simultaneous-barrier handling). Must use the same trade-price domain as features at v002 scope. Mixing mark-price and trade-price barriers in one label family is forbidden unless a separately authorized memo reconciles Phase 3v §8 stop-trigger-domain governance with label semantics.

**Class D — `mfe_mae_r_path_<horizon>`** (forensic / evaluation only).
Forensic outcome label family that records future MFE / MAE in R terms relative to a predeclared structural-risk anchor. Treated strictly as evaluation / forensic evidence; never converted into strategy rules without a fresh M0-admissible strategy-spec memo. Phase 4al refined no-rescue rule applies verbatim: no tuning, threshold selection, exit-rule retrofit on any rejected or retained-evidence candidate's future trade population may piggyback on class D labels.

**Class E — `time_to_event_<horizon>`** (optional future event-timing label).
Records time until first threshold touch, time until barrier outcome, or time until label B flips. Must support null / censored values when no event occurs within the horizon. Must be explicitly separated from strategy entry / exit logic. A label that records "how long until X happens" is not a rule that says "enter / exit when X happens."

**Class F (v002-only addition) — `horizon_valid_<horizon>` / `forward_censored_<horizon>` / `future_path_available_<horizon>`** (validity / censoring flags).
Per-horizon boolean flags marking whether the future horizon falls within the 90-day v002 envelope (2024-12-01 .. 2025-02-28 inclusive) and whether sufficient future feature rows exist to evaluate the horizon. Required for any label parquet that includes class A / B / C / D / E columns. Censoring flags must be explicit (boolean column), not implicit (only via null label value).

## 19. Allowed future label categories (admissible in principle; not authorized for computation)

Phase 4bm-M records the following label categories as **admissible in principle** for any future schema-finalization phase:

- forward return labels over predeclared horizons (class A);
- forward direction labels over predeclared horizons (class B; classification with predeclared thresholds);
- horizon-validity / censoring flags (class F; **required** for any label parquet that mixes horizons or spans the 2025-02-28 end-of-envelope boundary);
- future path availability flags (class F variant);
- neutral / no-event class (class B ternary variant), if v001 precedent permits;
- label-quality / label-validity flags (class F);
- strictly deterministic labels derived from the locked v002 BTCUSDT time / event series (the 155,153,449-row, 90-day, 62-column v002 feature artefact lineage).

Specifically deferred at v002 (not authorized; **not** part of Phase 4bm-M scope):

- barrier labels (class C) and target-before-stop labels — admissible **in principle**, but deferred at v002 first pass to mirror v001 Phase 4bj-A deferral;
- MFE / MAE labels and R-multiple labels (class D) — admissible **in principle as forensic only**, but deferred at v002 first pass;
- time-to-event labels (class E) — admissible **in principle**, but deferred at v002 first pass;
- multi-symbol label families (no ETHUSDT or alt label data is authorized; the symbol scope is locked at BTCUSDT-only by Phase 4bm-L);
- horizons beyond a conservative initial set (no 5m, 30m, 1h, 4h, 1d, multi-day label horizons authorized at v002 first pass);
- cross-day chronological-split-policy labels (a future separately authorized chronological-split-policy memo must precede any split definition; Phase 4bj-H / 4bj-I precedent applies);
- any other label family not explicitly listed in this memo or in the Phase 4bj-A v001 precedent.

A future v002 schema-finalization phase may keep, narrow, or further defer this list, but **must not silently widen it**.

## 20. Forbidden future label categories

The following label / target families are **forbidden** under the Phase 4bm-M boundary, both at v002 and at any future version, unless a separately authorized governance memo materially changes Phase 4al's refined no-rescue rule, the Phase 4m 18-requirement validity gate, and the Phase 4ak M0 twelve-clause gate:

- any label that **directly encodes** strategy entry decisions;
- any label that **directly encodes** strategy exit decisions;
- any label that records production order outcomes (live or paper);
- any label that records realized PnL of a hypothetical trade;
- any label that records realized profit / loss as a target;
- any label that records equity curves;
- any "alpha score" target derived from a trained model;
- any "edge score" target derived from a trained model;
- any "model prediction", "model probability", "model score", "decision score", or other post-model label;
- any label that depends on **future feature values that have been re-computed using future windows** (centered windows, future normalization, future z-scoring); features must remain causal as defined by Phase 4bm-G;
- any label that depends on external data not already governed at the same eligibility level (no spot data, no cross-venue data, no order-book data, no mark-price 30m / 4h / 5m / 15m data, no `aggTrades` beyond the locked v002 90-day envelope, no `metrics` beyond the Phase 4j §11 OI subset, no funding data, no liquidation data, no open-interest data unless separately authorized);
- any label that requires Phase 3v §8 stop-trigger-domain governance to be bypassed or relabeled to `mixed_or_unknown`;
- any label that uses the live exchange's own decision boundaries as targets (e.g., labeling exchange-side stop triggers, exchange-side liquidation events, exchange-side ADL events) until a separately authorized governance memo addresses mark-price domain, liquidation-proxy completeness, and forbidden-input scope;
- any label that requires public or private endpoint calls in code;
- any label that mutates the v002 feature manifest, the v002 derived manifest, the v002 raw manifest, the Phase 4bm-J gate report, the Phase 4bm-L successor-state JSON, the Phase 4bm-F successor-state JSON, the Phase 4bm-D gate report, the Phase 4bl-E successor-state JSON, the Phase 4bl-D-R gate report, or any other prior `data/microstructure/` artefact;
- any "post-hoc optimized threshold" target where thresholds were fitted to the evaluation cell rather than predeclared;
- any **rescue-shaped** label family that, when restated, reproduces a retained-evidence or HARD-REJECT candidate's entry / exit rules under a new name. This includes, but is not limited to: R2 pullback-retest reconstruction, F1 mean-reversion-after-overextension reconstruction, D1-A funding-Z-score directional reconstruction, V2 8-feature AND chain reconstruction, G1 multi-dimension regime-AND classifier reconstruction, C1 compression-box transition reconstruction, and any 5m strategy reconstruction from the Phase 3o / 3p Q1–Q7 outputs.

## 21. Future-data access policy

The causal-separation rule is binding:

- **features must remain causal.** A v002 feature value at row `R` with timestamp `T` may use only information from rows with `transact_time_ms <= T` and same-timestamp tie-break `row_index <= R` (this is the Phase 4bm-G / Phase 4bh contract preserved verbatim for v002).
- **labels may use future information only inside label generation.** A v002 label value at the same row `R` may use information after `T`, but **only inside the label kernel routine**. Features must not be modified by label computation.
- **labels must be stored in a separate label artefact family.** Label parquets must live under `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/...`, never inside the feature parquet directory. Label manifests must live under `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`, never inside the feature manifest.
- **label columns must never be placed inside feature parquets.** The 90 v002 feature parquets must remain at exactly 62 columns (17 lineage + 45 feature / quality). Adding a label column to a feature parquet is forbidden under Phase 4bm-G / Phase 4bh-A boundary.
- **all future-looking label fields must be explicitly marked as labels / targets and forbidden from feature computation.** Future label-schema-finalization code must declare each label column's `column_role = "label"` (or `"target"`) so that any feature-recompute routine refuses to read label columns as feature inputs.
- **labels must never be used to normalize, z-score, rank, bucket, filter, or mask feature rows before any train / validation / test split definition.**
- **labels must never be used to select which feature rows are kept before split definition.**
- **label code must be importable independently of feature code.** Cross-imports that let label results feed back into feature computation are forbidden.
- **any future label-kernel implementation must include a static and runtime test that asserts no label value flows back into any feature column for any v002 row.**

## 22. Timestamp / leakage policy

All future v002 label artefacts must enforce:

- **UTC only.** No local time zone. All timestamps are integer UTC milliseconds.
- **Deterministic event ordering.** Sort order `(feature_timestamp_ms, agg_trade_id, row_index)` is the canonical event order. No random shuffle is permitted at label-generation time, label-storage time, or label-evaluation time.
- **Feature row timestamp alignment.** Each label row anchors to exactly one v002 feature row (one label row per feature row, per horizon column, per UTC date).
- **Future horizon interval convention.** A horizon `<H>s` means the future reference timestamp is `feature_timestamp_ms + H*1000`. Inclusive / exclusive boundary at `T+H` must be predeclared in the future schema-finalization memo.
- **Same-timestamp tie handling.** Within a UTC day, multiple feature rows may share `transact_time_ms`. Labels must use the canonical tie-break `row_index` and must record the exact tie-handling convention in `label_threshold_metadata`.
- **End-of-sample censoring.** For any feature row whose `feature_timestamp_ms + H*1000` exceeds the 2025-02-28 23:59:59.999 UTC envelope, the label value must be `null` and the corresponding `forward_censored_<horizon>` flag must be `true`. No label value may be synthesized from non-existent future data.
- **Day-boundary handling.** For multi-day horizons, label generation may cross UTC day boundaries inside the 90-day v002 envelope (2024-12-01 .. 2025-02-28). Each label row must record the `utc_date` of its anchor feature row (not the future reference timestamp's date).
- **No random shuffle.** Label-evaluation, label-validation, and any future label-based research must use chronological splits only.
- **No train / validation / test split assignment in this phase.** Phase 4bm-M does not define any split. A future chronological-split-policy memo (multi-day v002 analogue of Phase 4bj-H / 4bj-I) must separately define any v002 split, and that memo is **not authorized** by Phase 4bm-M.

## 23. Multi-day label boundary policy

- **Labels may require future-day lookahead** (for horizons that exceed the anchor row's UTC date). This is allowed inside the label kernel only; feature computation must never lookahead.
- **End-of-dataset rows with insufficient future horizon must be censored** (null label + explicit `forward_censored_<horizon> = true` flag) according to the future schema.
- **No data beyond 2025-02-28 23:59:59.999 UTC may be acquired by this phase, by any future label phase, or by any successor phase, unless an explicit, separately authorized acquisition phase is approved.** The 90-day v002 envelope is locked.
- **Any future label-computation phase must either restrict horizons to available data or explicitly mark censoring.** Silent extrapolation, synthetic future fills, or "zero-padding" beyond 2025-02-28 is forbidden.
- **Day-boundary labels must preserve the v002 acquisition log / raw manifest / derived manifest / feature manifest immutability.** Crossing a day boundary inside the label kernel does not authorize any modification of the underlying day's data.

## 24. Proposed future label family identity (consolidated)

For convenience, the proposed future label family identity is:

- `dataset_family` = `"microstructure_labels_aggtrades_v001"`
- `dataset_version` = `"v002"`
- `label_schema_version` = `"v001"`
- `source_feature_dataset_family` = `"microstructure_features_aggtrades_v001"`
- `source_feature_dataset_version` = `"v002"`
- `source_normalized_dataset_family` = `"microstructure_normalized_aggtrades_v001"`
- `source_normalized_dataset_version` = `"v002"`
- `source_raw_dataset_family` = `"microstructure_raw_aggtrades_v001"`
- `source_raw_dataset_version` = `"v002"`
- `symbol_list` = `["BTCUSDT"]`
- `utc_date_start` = `"2024-12-01"`
- `utc_date_end` = `"2025-02-28"`
- `date_count` = `90`

## 25. Proposed future output namespace (consolidated)

Proposed (not created):

- per-day label parquet: `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-labels-aggtrades-<YYYY>-<MM>-<DD>.parquet`;
- per-day label sidecar: same path with `.sha256` suffix;
- label manifest: `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002.json`;
- label manifest sidecar: same path with `.sha256` suffix;
- label gate-report directory: `data/microstructure/gate-reports/labels/`;
- label successor-state directory: `data/microstructure/successor-state/` (sibling files only; feature / derived / raw successor-state JSONs must not be modified).

If a future v001 Phase 4bj precedent uses different filenames, the future v002 schema-finalization phase must reconcile the difference explicitly. The exact label parquet naming pattern is subject to schema-finalization confirmation.

## 26. Future label manifest required fields

If a future phase separately authorizes a label manifest, that manifest must include at minimum:

- `dataset_family` = `"microstructure_labels_aggtrades_v001"`
- `dataset_version` = `"v002"`
- `label_schema_version` = `"v001"`
- `source_feature_dataset_family` = `"microstructure_features_aggtrades_v001"`
- `source_feature_dataset_version` = `"v002"`
- `source_feature_manifest_sha256` = `"512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"`
- `source_feature_manifest_sidecar_sha256` = `"22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34"`
- `source_feature_successor_state_sha256` = `"7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4"` (Phase 4bm-L)
- `source_feature_successor_state_sidecar_sha256` = `"c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98"`
- `source_phase_4bm_j_gate_report_sha256` = `"3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"`
- `source_normalized_manifest_sha256` = `"01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a"`
- `source_phase_4bm_f_successor_state_sha256` = `"72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"`
- `source_phase_4bm_d_gate_report_sha256` = `"3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a"`
- `source_raw_manifest_sha256` = `"016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485"`
- `source_phase_4bl_e_raw_successor_state_sha256` = `"a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d"`
- `source_phase_4bl_d_r_raw_gate_report_sha256` = `"f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46"`
- `source_acquisition_log_sha256` = `"52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314"`
- `feature_config_hash` = `"819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"`
- `label_config_hash`: deterministic hash of the future label kernel configuration (computed by the kernel);
- `label_list`: ordered list of label column names (no forbidden substrings per the Phase 4bh-A / Phase 4bh-B substring-enforcement precedent; see also the forbidden categories in §20);
- `horizon_list`: ordered list of future horizons (subject to schema finalization);
- `symbol_list` = `["BTCUSDT"]`
- `utc_date_start` = `"2024-12-01"`
- `utc_date_end` = `"2025-02-28"`
- `date_count` = `90`
- `row_count`: total label rows (may equal feature row count = 155,153,449 or be lower if right-edge censoring removes rows, depending on null-tail policy);
- `per_day_outputs`: ordered list of 90 per-day label parquet entries (path + SHA256 + sidecar SHA256 + row count);
- `nullable_tail_policy`: explicit description of how horizon-censored rows are represented (null label + explicit boolean censoring flag);
- `chronological_split_policy` = `"not_yet_defined"` (until a separately authorized split-policy memo locks it);
- `governance_labels` (default values):
  - `labels` = `"allowed_by_future_phase_only"`;
  - `targets` = `"allowed_by_future_phase_only"`;
  - `ml` = `"forbidden"`;
  - `strategy` = `"forbidden"`;
  - `backtest` = `"forbidden"`;
  - `acquisition` = `"unauthorized"`;
  - `paper_shadow_live` = `"forbidden"`;
  - `deployment` = `"forbidden"`;
  - `exchange_write` = `"forbidden"`;
- `research_eligible` = `false` (default; must remain `false` until a separately authorized label-family research-use admissibility phase records otherwise);
- `eligibility_gate_status` = `"pending"` (default);
- `label_family_research_use_authorized` = `false` (default);
- `code_commit_sha`: the implementation phase's commit SHA at run time;
- `created_at_unix_ms`: the implementation phase's creation time.

These fields are policy-level only at Phase 4bm-M. Their exact JSON shape must be finalized by a future schema-finalization memo, not by implementation drift.

## 27. Future label implementation gate prerequisites

Before any future v002 label artefact may exist (Parquet, sidecar, manifest, manifest sidecar, gate report, or successor-state JSON), all of the following must hold:

1. Phase 4bm-M (this memo) **must be merged into `main` and project-complete** per the merge-closeout standard. Phase 4bm-M is currently branch-complete only by this work; merge is a separately authorized future phase.
2. A future Phase 4bm-N (or equivalent) **Multi-Day V002 Label Schema Finalization Memo** must be separately authorized by an explicit operator decision, must finalize the exact label list, horizon list, classification / regression policy, threshold policy, null-tail / censoring policy, lineage policy, manifest schema, and acceptance criteria, and must clear M0 for the label family it finalizes. (If a future operator combines boundary and schema finalization into one phase, that combined phase must be separately authorized; Phase 4bm-M does not authorize such a combination.)
3. A future label-kernel implementation phase (multi-day v002 analogue of Phase 4bj-C) must be separately authorized by an explicit operator decision.
4. The future label-kernel implementation must implement **exactly** the schema finalized by the immediately prior schema-finalization phase (no widening, no narrowing, no implicit drift).
5. The future label-kernel implementation must write only **gitignored** label artefacts under `data/microstructure/labels/`, `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002*`, `data/microstructure/gate-reports/labels/`, and `data/microstructure/successor-state/` (the latter only for sibling label successor-states; feature / derived / raw successor-states must remain byte-identical).
6. The future label-kernel implementation must refuse to overwrite any existing local artefact under the same names.
7. The future label-kernel implementation must preserve the v002 feature manifest, v002 feature manifest sidecar, every v002 per-day feature parquet, every v002 per-day feature sidecar, the Phase 4bm-J gate report, the Phase 4bm-J gate sidecar, the Phase 4bm-L successor-state JSON, the Phase 4bm-L successor-state sidecar, the Phase 4bm-F successor-state JSON, the Phase 4bm-F successor-state sidecar, the Phase 4bm-D gate report, the Phase 4bm-D gate sidecar, the v002 derived multi-day index manifest, the v002 derived manifest sidecar, the v002 raw manifest, the v002 acquisition log, the Phase 4bl-E successor-state JSON, and the Phase 4bl-D-R gate report **byte-identically**.
8. The future label-kernel implementation must create **no** ML models, **no** strategy signals, **no** backtests, **no** PnL / MFE / MAE / R-multiple / equity / position-state / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy-output columns.
9. The future label manifest must record `research_eligible = false` and `eligibility_gate_status = "pending"` by default; flipping is forbidden by the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant.
10. The future label-kernel implementation must record the null / censoring policy explicitly in the manifest.
11. The future label-kernel implementation must record the horizon policy explicitly in the manifest.
12. The future label-kernel implementation must record `chronological_split_policy = "not_yet_defined"` unless a separately authorized memo locks it.
13. The future label-kernel implementation must pass label-specific tests, microstructure tests, `ruff`, `mypy`, and `pytest` with no new failures beyond the documented Phase 4bm-H baseline.
14. The future label-kernel implementation must produce a closeout report under `docs/00-meta/implementation-reports/` recording the same discipline as Phase 4bm-H / Phase 4bm-J / Phase 4bm-L.

Subsequent phases (multi-day v002 analogues of Phase 4bj-D structural QA, Phase 4bj-E eligibility gate, Phase 4bj-F research-use decision, Phase 4bj-G successor-state recording, Phase 4bj-H / 4bj-I chronological-split-policy memo, Phase 4bj-J split-policy successor-state recording) must each be separately authorized by explicit operator decisions. **None of those phases is authorized by Phase 4bm-M.**

## 28. What this memo proves

Phase 4bm-M proves only the following:

- a leakage-safe multi-day v002 label-family boundary can be specified at policy level for the Stage-5-admissible multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 62-column canonical schema; `feature_config_hash 819cfa7a…7d7b5a1d`);
- a conservative initial label family (`microstructure_labels_aggtrades_v001 @ v002`) is admissible **in principle** for a future separately authorized schema-finalization phase and a future separately authorized implementation phase, subject to all 14 acceptance criteria in §27;
- the no-rescue, no-leakage, no-shuffling, cost-aware, M0-bound, Phase 4al-bound interpretation of v002 labels is recorded as policy;
- the boundary between v002 labels and v002 stops / risks / strategies / backtests / ML is recorded explicitly so that future v002 label phases cannot silently widen scope;
- the Phase 4bj-A v001 boundary precedent extends cleanly to the multi-day v002 envelope, with three explicit v002-specific extensions (multi-day end-of-sample censoring; multi-day chronological ordering; multi-day lineage anchored to all 90 per-day feature Parquets and the Phase 4bm-L successor-state).

## 29. What this memo does not prove

Phase 4bm-M does **not** prove:

- that any v002 label has predictive value;
- that forward returns at any v002 horizon are forecastable;
- that direction classification at any v002 horizon is forecastable;
- that any v002 label-based ML model would generalize;
- that any v002 label-based strategy would be edge-positive;
- that any specific v002 label schema is the right one;
- that mark-price stop-domain forensics is admissible at v002;
- that aggTrades-domain barrier labels are admissible at v002 first pass;
- that ETHUSDT or any other symbol is admissible at v002;
- that any v002 horizons beyond a conservative initial set are admissible;
- that any v002 label phase is authorized;
- that ML training on v002 labels is authorized;
- that strategy work on v002 labels is authorized;
- that backtest work on v002 labels is authorized;
- that paper / shadow / live work on v002 labels is authorized;
- that any v001 label decision transitively authorizes any v002 label computation;
- that the v002 feature family is itself an empirical claim of edge (Phase 4bm-L Stage-5 admissibility is a governance state, not an empirical claim);
- that any successor phase is authorized.

## 30. Non-authorization

Phase 4bm-M does **not**, and **cannot**, authorize:

- Phase 4bm-N (any provisional successor; not authorized);
- multi-day v002 label-family schema finalization (multi-day analogue of Phase 4bj-B);
- multi-day v002 label-kernel implementation (multi-day analogue of Phase 4bj-C);
- multi-day v002 label artefact structural QA (multi-day analogue of Phase 4bj-D);
- multi-day v002 label-family eligibility gate design / implementation / execution (multi-day analogue of Phase 4bj-E);
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, Phase 4bm-E v002 derived-family decision, Phase 4bm-F v002 derived-family successor-state semantics, Phase 4bm-G v002 feature-boundary design, Phase 4bm-H v002 feature computation, Phase 4bm-I v002 feature-artefact structural QA, Phase 4bm-J v002 feature-family eligibility-gate verdict, Phase 4bm-K v002 feature-family research-use decision, or Phase 4bm-L v002 feature-family Stage-5 successor-state recording;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**, **N-SUCCESSOR-STATE** (Phase 4bm-M creates **no** new successor-state artefact).

## 31. Recommended state

**Remain paused.**

Phase 4bm-M is docs-only. It is branch-complete only by this work. Per the Phase 4bk-A workflow standard, Phase 4bm-M is **not** project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived / feature family now has a complete ladder of evidence through **v002 Feature Stage-5 (machine-readable research-use admissibility, Phase 4bm-L)** plus a **v002 Label-Family Boundary / Design memo at policy level (Phase 4bm-M, this phase, branch-complete only)**. No label artefact, label manifest, label gate report, or label successor-state exists or is authorized to exist by this phase.

## 32. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 label lifecycle ladder** — Phase 4bm-N (multi-day v002 label schema finalization memo; multi-day analogue of Phase 4bj-B) | docs-only; no computation | **NOT authorized by this memo** |
| **Conditional later** — future docs-only multi-day v002 chronological-split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized by this memo** |
| **Conditional further along** — multi-day v002 label-kernel implementation + local label artefact generation, structural QA, eligibility gate, research-use decision, successor-state recording (multi-day analogues of Phase 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G) | code + docs + local gitignored output | **NOT authorized by this memo** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-M** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-M** |

## 33. Preserved boundaries

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-M).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K / 4bm-L results — all preserved verbatim.

## 34. Validation commands and results

### Initial verification (pre-edit)

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-m/multi-day-v002-label-family-boundary-design-memo` |
| `git rev-parse main` | `38cf6693425f91e85e2d5a295800aa5ee2287db3` |
| `git rev-parse origin/main` | `38cf6693425f91e85e2d5a295800aa5ee2287db3` (in sync) |
| `git log --oneline -12 --decorate` | latest main commit is `38cf669 docs(phase-4bm-l): finalize merge closeout shas` (matches expectation) |

### Read-only SHA verification (recomputed on disk at the start of this phase)

| Artefact | SHA256 (recomputed) | Expected | Match |
| -------- | ------------------- | -------- | ----- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | same | ✓ |
| Phase 4bm-J gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | same | ✓ |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | same | ✓ |
| Phase 4bm-L successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | same | ✓ |

The remaining 13 artefacts in §10 are not re-hashed in this phase because Phase 4bm-M reads no Parquet, runs no kernel, and modifies no `data/microstructure/` file. Their SHAs are taken verbatim from the Phase 4bm-L successor-state JSON and the Phase 4bm-L implementation report Evidence Table §15.

### Post-edit validation

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock`, `data/research/` (untracked, expected), plus the three tracked Phase 4bm-M docs files |
| `git diff --check` | clean (no whitespace errors; exit 0) |
| `git diff --name-only` | exactly three tracked docs paths: this memo, the closeout, and the narrow `docs/00-meta/current-project-state.md` update |

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by Phase 4bm-M. Per the Phase 4bk-A workflow standard, the Phase 4bl-F risk-tiering standard, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, and the established Tier 1 docs-only boundary / design-memo precedent (Phase 4bj-A v001 label-boundary, Phase 4bg-A v001 derived-family research-eligibility, Phase 4bi-C v001 feature-family research-use, Phase 4bm-A multi-day normalization design, Phase 4bm-E multi-day derived-family research-eligibility decision, Phase 4bm-G v002 feature-boundary design, Phase 4bm-K v002 feature-family research-use decision — each of which deliberately skipped these gates for the same reason), the code / type / test gate subset is not invoked here. No source / test / script / configuration file is modified. The Phase 4bm-J branch quality gates (Phase 4bm-J surface `ruff check` PASS, whole-repo `ruff check .` PASS, targeted gate pytest 53 PASS) and the Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files; whole-repo `pytest`: 15 collection errors + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures, both env baseline) remain unchanged by construction because Phase 4bm-M modifies no existing source / test / script.

## 35. Quality gate results / skipped-check rationale

- `git diff --check`: clean (exit 0).
- Repo-standard markdown lint or check: no project-specific lightweight markdown gate exists in this repository; therefore none is run.
- `ruff check`, `mypy src/prometheus`, `pytest` — see §34 "Tools deliberately not run".

## 36. No source / test / script / config modified

- No file under `src/prometheus/` modified.
- No file under `tests/` modified.
- No file under `scripts/` modified.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, MCP file, or credential file modified.
- The only tracked changes are the three docs files (this implementation report + the closeout + a narrow `current-project-state.md` paragraph addition + new "Current phase:" block update).

## 37. No labels / diagnostics / ML / strategy / backtests authorized or performed

- No label kernel designed; no label kernel run; no label parquet created; no label manifest created; no label sidecar created; no label gate report created; no label successor-state JSON created.
- No diagnostics run; no diagnostic output created.
- No ML training, model selection, feature ranking, meta-labeling, or hyperparameter search performed.
- No strategy specification, signal construction, or strategy-spec memo created.
- No backtest specification, plan, or execution performed.
- No simulation run; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output computed.

## 38. No endpoint / credential / MCP / Graphify / exchange-write surface touched

Phase 4bm-M touched no network surface. No Binance endpoint (public, authenticated, or private) was called. No `data.binance.vision`, `fapi.binance.com`, or `api.binance.com` was contacted. No WebSocket was opened. No `.env` was read or created. No `.mcp.json` was read or created. MCP / Graphify was not enabled. No order was placed. No exchange-write surface was contacted.

## 39. Required exact phrases (verbatim, per task brief)

- **Phase 4bm-M is label-boundary design only.**
- **No label artefact exists after Phase 4bm-M.**
- **Phase 4bm-N is not authorized by Phase 4bm-M.**
- **Label computation is not authorized by Phase 4bm-M.**
- **Diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-M.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
