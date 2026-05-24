# Phase 4bm-L — Multi-Day V002 Feature-Family Research-Use Successor-State Recording

**Phase identity:** Phase 4bm-L — Multi-Day V002 Feature-Family Research-Use Successor-State Recording (docs + local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-l/multi-day-v002-feature-family-research-use-successor-state-recording`.
**Base:** `main` at `121865a26120d5f097fee95c00185ebd4c995703` (Phase 4bm-K merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-D feature-family successor-state recording precedent. First-of-kind multi-day v002 feature-family research-use successor-state recording; any phase that affects machine-readable admissibility for the v002 feature family escalates to Tier 1 (§3).
**Phase type:** docs + local gitignored output — adds two new tracked docs files under `docs/00-meta/implementation-reports/`, narrowly updates `docs/00-meta/current-project-state.md`, and writes exactly one new local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/successor-state/`. **No** source / test / script / configuration / manifest / sidecar / gate-report / prior successor-state mutation; **no** normalized Parquet, raw zip, feature parquet, feature manifest, label parquet, or any other prior `data/microstructure/` artefact touched.
**Status:** drafted; pending operator review.

---

## 1. Phase header

This phase operationalises the Phase 4bm-K Outcome 1 / Decision form 1 (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) outcome:

> v002 Feature Stage-5 research-use admissibility is admissible in principle at policy level for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; 62-column canonical schema; `feature_config_hash = 819cfa7a…`), but no manifest mutation occurs in Phase 4bm-K. A separately authorized Phase 4bm-L successor-state recording phase is required before any machine-readable v002 Feature Stage-5 marker exists.

Phase 4bm-L records that machine-readable v002 Feature Stage-5 successor-state marker as a sibling artefact under `data/microstructure/successor-state/`, while preserving the original v002 feature manifest, the v002 feature manifest sidecar, the Phase 4bm-J feature-family eligibility gate report + sidecar, the v002 derived multi-day index manifest + sidecar, the v002 raw manifest, the v002 acquisition log, the Phase 4bm-D authoritative derived-family gate report + sidecar, the Phase 4bl-D-R raw multi-day PASS gate report, the Phase 4bl-E raw multi-day successor-state JSON, the Phase 4bm-F v002 derived-family Stage-3 successor-state JSON + sidecar, and every other prior `data/microstructure/` artefact byte-identically.

Phase 4bm-L is the **multi-day v002 analogue of Phase 4bi-D** (the v001 feature-family Stage-5 successor-state recording phase) and the **v002 feature-family sibling of Phase 4bm-F** (the v002 derived-family Stage-3 successor-state recording phase).

---

## 2. Why Phase 4bm-L exists

The Phase 4bm-J 50 / 50 PASS `FEATURE_GATE_PASS` result is **report-level only**. Per the Phase 4bb-E / Phase 4bf / Phase 4bg-A / Phase 4bg-B / Phase 4bi-B / Phase 4bi-C / Phase 4bi-D / Phase 4bm-D / Phase 4bm-E / Phase 4bm-F precedent chain (now preserved verbatim across the v002 lifecycle), report-level PASS does not flip any actual on-disk manifest field. The actual v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` continues to carry `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` byte-identically.

Phase 4bm-K (Outcome 1 / Decision form 1; equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`) recorded that v002 Feature Stage-5 research-use admissibility is admissible in principle at policy level for the multi-day v002 feature family, but explicitly required a separately authorized successor-state recording phase before any machine-readable v002 Feature Stage-5 marker exists. Phase 4bm-L is exactly that separately authorized phase.

The successor-state JSON is a **sibling artefact**, not a manifest replacement. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bm-L). Any future tool that wishes to interpret the v002 feature family as Stage-5-admissible must read the successor-state JSON, **not** the original feature manifest.

---

## 3. Scope and boundary

In scope for this phase:

- creating exactly one local gitignored successor-state JSON under `data/microstructure/successor-state/` recording v002 Feature Stage-5 research-use admissibility for the feature family `microstructure_features_aggtrades_v001 @ v002`;
- creating exactly one paired canonical Phase 4bb-F `.sha256` sidecar matching the JSON's bytes;
- citing the Phase 4bm-K decision and its commit chain verbatim;
- citing the Phase 4bm-J gate report id, gate report SHA, gate sidecar SHA, and result invariants verbatim;
- citing the Phase 4bm-I structural QA verdict verbatim;
- citing the Phase 4bm-H feature artefact provenance verbatim;
- citing the Phase 4bm-G feature-boundary design verbatim;
- citing the Phase 4bm-F v002 derived-family Stage-3 successor-state JSON SHA verbatim;
- citing the Phase 4bi-D v001 feature-family successor-state precedent verbatim;
- citing all 14 upstream lineage artefact SHAs verbatim;
- preserving the original v002 feature manifest byte-identically (SHA `512a0a54…`);
- preserving `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` on the original v002 feature manifest;
- documenting the action in this memo and a closeout, plus a narrow `current-project-state.md` paragraph and new "Current phase:" block with the prior Phase 4bm-K block preserved as labelled historical context.

Out of scope (categorical exclusions; this phase honors the Phase 4bl-F reusable non-authorization blocks **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK** — note that **N-SUCCESSOR-STATE** is the only block that does NOT apply, because this phase creates exactly one new sibling successor-state artefact, governed by the Phase 4bi-D / Phase 4bm-F precedent):

- modifying any source code, test, script, configuration, dataset, manifest, sidecar, gate report, or any prior successor-state JSON;
- running the v002 normalizer, raw eligibility gate, derived-family gate, feature kernel, or feature-family eligibility gate;
- generating any new gate report;
- creating any normalized parquet, derived manifest, feature parquet, feature manifest, gate report, label parquet, label manifest, or any other `data/microstructure/` artefact beyond the one new successor-state JSON and its paired sidecar;
- creating labels, targets, signals, ML, strategy, diagnostics, or backtest artefacts;
- computing returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, decision score, or entry / exit signal;
- training ML; designing strategy logic; running backtests or simulations;
- acquiring data; calling public endpoints, Binance APIs, or private endpoints; opening WebSockets; requesting, storing, or using credentials; reading or creating `.env`; creating or reading `.mcp.json`; enabling MCP or Graphify;
- flipping `research_eligible` on any actual manifest; transitioning `eligibility_gate_status` on any actual manifest; marking `stage_4_feature_cleared = true` on any actual manifest; changing `chronological_split_policy` on any actual manifest;
- mutating the feature manifest, any upstream manifest, any prior gate report, or any prior successor-state JSON in any way;
- amending M0; revising any retained verdict; changing any project lock;
- authorizing Phase 4bm-M, multi-day v002 label-family phases, multi-day v002 chronological-split-policy memo, multi-day v002 diagnostics, multi-day v002 ML / strategy / backtest, Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, live WebSocket implementation;
- committing anything under `data/microstructure/`.

---

## 4. Linkage to Phase 4bm-K Outcome 1 / Decision form 1

The Phase 4bm-L successor-state JSON cites the Phase 4bm-K decision verbatim:

- `decision_phase_id`: `"4bm-K"`
- `decision_phase_name`: `"Multi-Day V002 Feature-Family Research-Use Decision Memo"`
- `decision`: `"Outcome 1 / Decision form 1"`
- `decision_equivalent_label`: `"FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE"`
- `phase_4bm_k_branch_commit_sha`: `"ecfb8841a22bac23d0fde7d1b4e32fe69896d178"`
- `phase_4bm_k_merge_commit_sha`: `"a9f09ae7af3bf9a4cf74e6498f38eb092b67ac78"`
- `phase_4bm_k_merge_closeout_commit_sha`: `"feaeff3e557223d122c0383c67cdab6fbd5a2345"`
- `phase_4bm_k_sha_finalization_commit_sha`: `"121865a26120d5f097fee95c00185ebd4c995703"`

Phase 4bm-K recorded the policy-level v002 Feature Stage-5 admissibility decision; Phase 4bm-L records the machine-readable v002 Feature Stage-5 successor-state marker. These two phases together complete the v002 multi-day analogue of the Phase 4bi-C → Phase 4bi-D v001 single-day lifecycle.

---

## 5. Linkage to Phase 4bm-J FEATURE_GATE_PASS

Every Phase 4bm-L upstream-evidence field is grounded in the Phase 4bm-J locked gate report:

- `source_feature_gate_phase_id`: `"4bm-J"`
- `source_feature_gate_verdict`: `"FEATURE_GATE_PASS"`
- `source_feature_gate_overall_status`: `"pass"`
- `source_feature_gate_pass_count`: `50`
- `source_feature_gate_fail_count`: `0`
- `source_feature_gate_error_count`: `0`
- `source_feature_gate_not_applicable_count`: `0`
- `source_feature_gate_blocking_fail_count`: `0`
- `source_feature_gate_report_id`: `"microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd"`
- `source_feature_gate_report_path`: `"data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json"`
- `source_feature_gate_report_sha256`: `"3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242"`
- `source_feature_gate_sidecar_sha256`: `"14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125"`

The Phase 4bm-J gate report is the report-level v002 Feature Stage-4 evidence and remains byte-identical pre- and post-Phase-4bm-L.

---

## 6. Linkage to Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS

The Phase 4bm-L successor-state JSON cites the Phase 4bm-I structural QA verdict verbatim:

- `source_structural_qa_phase_id`: `"4bm-I"`
- `source_structural_qa_phase_name`: `"Multi-Day V002 Feature Artefact Structural QA Memo"`
- `source_structural_qa_verdict`: `"FEATURE_STRUCTURAL_QA_PASS"`

Phase 4bm-I was the read-only structural QA layer over the Phase 4bm-H feature artefacts; its PASS verdict was machine-verified by Phase 4bm-J check A12.

---

## 7. Linkage to Phase 4bm-H feature artefacts

The Phase 4bm-L successor-state JSON records the Phase 4bm-H feature artefact provenance:

- `source_feature_implementation_phase_id`: `"4bm-H"`
- `feature_row_count`: `155153449`
- `feature_parquet_count`: `90`
- `feature_sidecar_count`: `90`
- `feature_schema_column_count`: `62`
- `lineage_column_count`: `17`
- `feature_quality_column_count`: `45`
- `feature_config_hash`: `"819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"`
- `source_feature_manifest_path`: `"data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json"`
- `source_feature_manifest_sha256`: `"512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d"`
- `source_feature_manifest_sidecar_sha256`: `"22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34"`

The 90 per-day v002 feature Parquets and their 90 paired sidecars are not modified by Phase 4bm-L (Phase 4bm-L reads no Parquet and runs no kernel).

---

## 8. Linkage to Phase 4bi-D v001 feature-family successor-state precedent and Phase 4bm-F v002 derived-family sibling

The Phase 4bm-L successor-state JSON cites both precedents verbatim:

- `phase_4bi_d_v001_feature_successor_state_phase`: `"4bi-D"`
- `phase_4bi_d_v001_feature_successor_state_path`: `"data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json"`
- `phase_4bi_d_v001_feature_successor_state_sha256`: `"8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a"`
- `source_derived_successor_state_phase_id`: `"4bm-F"`
- `source_derived_successor_state_path`: `"data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json"`
- `source_derived_successor_state_sha256`: `"72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9"`
- `source_derived_successor_state_sidecar_sha256`: `"1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97"`

The Phase 4bm-L filename pattern adapts the Phase 4bi-D / Phase 4bm-F precedent: `microstructure_features_aggtrades_v001__<version>__stage5_<marker_label>__<phase>.json`. The marker label for v002 uses `stage5_research_use_approved` (rather than the v001 `stage5_research_ml_admissible`) because the Phase 4bm-K decision verdict is `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`, mirroring the Phase 4bm-K phase name "Research-Use Decision Memo" (vs the v001 Phase 4bi-C "Research-Use / ML-Use Decision Memo"). The schema and serialization (`json.dumps(payload, sort_keys=True, indent=2) + "\n"`, ASCII-only, no BOM, LF only) follow the Phase 4bm-F precedent exactly.

---

## 9. Exact successor-state JSON path

```text
data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json
```

Absolute path on the local workstation:

```text
C:\Prometheus\data\microstructure\successor-state\microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json
```

Gitignored under `.gitignore:85: data/microstructure/`. **Not committed.**

---

## 10. Exact successor-state JSON SHA256

```text
7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4
```

Size: **13,499 bytes**. UTF-8 (ASCII-only payload; no BOM). LF line endings only. Two-space indent. Sorted keys. Final newline at EOF.

---

## 11. Exact successor-state sidecar path

```text
data/microstructure/successor-state/microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json.sha256
```

Absolute path on the local workstation:

```text
C:\Prometheus\data\microstructure\successor-state\microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json.sha256
```

Gitignored under `.gitignore:85: data/microstructure/`. **Not committed.**

---

## 12. Exact sidecar file SHA256

```text
c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98
```

Size: **159 bytes**. UTF-8 / ASCII content only. Single line with trailing LF. No CRLF; no BOM; canonical Phase 4bb-F format (`<sha256_lowercase_hex><two ASCII spaces><basename><LF>`).

---

## 13. Exact sidecar content

```text
7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4  microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json
```

Byte-by-byte verification (all checks PASS):

- Bytes 0..63: lowercase hex of the JSON SHA256 (`7eccaa8f…35e4`).
- Bytes 64..65: `0x20 0x20` (two ASCII spaces).
- Bytes 66..157: ASCII basename `microstructure_features_aggtrades_v001__v002__stage5_research_use_approved__phase-4bm-l.json` (**92 bytes**).
- Byte 158: `0x0A` (LF terminator).
- Total: 64 + 2 + 92 + 1 = **159 bytes** (matches the on-disk file size).
- No CRLF anywhere; no BOM; ASCII-only.
- The embedded SHA matches the recomputed SHA256 of the JSON byte-for-byte (no drift).

---

## 14. Key successor-state fields

The successor-state JSON records the following critical fields at the top level (full list is in the file itself; this is a curated digest):

| Group | Field | Value |
| --- | --- | --- |
| Schema / phase identity | `schema_version` | `"v001"` |
| | `phase_id` | `"4bm-L"` |
| | `phase_name` | `"Multi-Day V002 Feature-Family Research-Use Successor-State Recording"` |
| Successor-stage semantics | `successor_state_kind` | `"feature_family_research_use_successor_state"` |
| | `successor_state_type` | `"feature_family_research_use"` |
| | `successor_stage` | `"Feature Stage-5"` |
| | `stage_5_policy_admissible` | `true` |
| | `feature_family_research_use_approved_in_principle` | `true` |
| | `machine_readable_stage5_marker_created_by_this_file` | `true` |
| | `research_use_successor_state` | `true` |
| Family identity | `dataset_family` | `"microstructure_features_aggtrades_v001"` |
| | `dataset_version` | `"v002"` |
| | `feature_schema_version` | `"v001"` |
| | `symbol` | `"BTCUSDT"` |
| | `symbol_list` | `["BTCUSDT"]` |
| | `utc_date_start` | `"2024-12-01"` |
| | `utc_date_end` | `"2025-02-28"` |
| | `date_count` | `90` |
| | `feature_row_count` | `155153449` |
| | `feature_parquet_count` | `90` |
| | `feature_sidecar_count` | `90` |
| | `feature_schema_column_count` | `62` |
| | `lineage_column_count` | `17` |
| | `feature_quality_column_count` | `45` |
| | `feature_config_hash` | `"819cfa7a…7d7b5a1d"` |
| Phase 4bm-K decision | `decision` | `"Outcome 1 / Decision form 1"` |
| | `decision_equivalent_label` | `"FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE"` |
| Original feature manifest preservation | `source_feature_manifest_sha256` | `"512a0a54…633343d"` |
| | `original_feature_manifest_byte_identical` | `true` |
| | `original_feature_manifest_research_eligible_after` | `false` |
| | `original_feature_manifest_eligibility_gate_status_after` | `"pending"` |
| | `original_feature_manifest_stage_4_feature_cleared_after` | `false` |
| Governance label fields | `labels` / `diagnostics` / `ml` / `strategy` / `backtest` | `"forbidden"` |
| | `acquisition` | `"unauthorized"` |
| Explicit `*_authorized: false` markers | `labels_authorized` … `successor_phase_authorized_after` | `false` (20 fields total) |
| Negative-action confirmations | `no_manifest_mutation` … `no_successor_authorization` | `true` (20 fields total) |
| Governance preservation | `retained_verdicts_preserved` | `true` |
| | `governance_locks_preserved` | `true` |
| | `phase_4aw_flip_research_eligible_invariant_preserved` | `true` |
| `boundary_confirmations` (50 keys; all `true`) | `no_feature_manifest_mutation` … `normalized_family_research_eligible_remains_false` | `true` (all 50) |
| Creation metadata | `base_commit_sha` | `"121865a26120d5f097fee95c00185ebd4c995703"` |
| | `docs_commit_sha_at_creation` | `"121865a26120d5f097fee95c00185ebd4c995703"` |
| | `created_at_unix_ms` | (recorded at write time; embedded inside the JSON) |
| | `created_at_utc` | (recorded at write time; embedded inside the JSON) |

The serialization is deterministic: `json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True) + "\n"`. Any byte-level reproduction of the same payload yields SHA256 `7eccaa8f…35e4`.

---

## 15. Evidence SHA table

| Artefact | SHA256 | Status (pre/post Phase 4bm-L) |
| --- | --- | --- |
| v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | IDENTICAL |
| v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | IDENTICAL |
| Phase 4bm-J v002 feature-family gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | IDENTICAL |
| Phase 4bm-J v002 feature-family gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | IDENTICAL |
| v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | IDENTICAL |
| v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | IDENTICAL |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | IDENTICAL |
| Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | IDENTICAL |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | IDENTICAL |
| Phase 4bm-F v002 derived-family Stage-3 successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | IDENTICAL |
| Phase 4bm-F v002 derived-family Stage-3 successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | IDENTICAL |
| **NEW** Phase 4bm-L v002 feature-family Stage-5 successor-state JSON | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` | NEW (gitignored) |
| **NEW** Phase 4bm-L v002 feature-family Stage-5 successor-state sidecar | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` | NEW (gitignored) |

The 90 v002 per-day feature Parquets, 90 v002 feature sidecars, 90 v002 normalized per-day Parquets, 90 v002 normalized sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are byte-identical pre- and post-Phase-4bm-L by construction (Phase 4bm-L reads no Parquet, runs no kernel, and writes nothing outside `data/microstructure/successor-state/`).

---

## 16. Pre/post SHA immutability table

The 14 upstream lineage artefacts in §15 were SHA-recomputed both at the start of this phase and after the successor-state JSON + sidecar were written. Every SHA matched its expected value byte-for-byte both times. The only new artefacts on disk after Phase 4bm-L are the two gitignored Phase 4bm-L outputs (JSON + sidecar). No existing artefact's `mtime` was updated by Phase 4bm-L.

---

## 17. Original v002 feature manifest preservation

The original v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json`:

- SHA256 (pre and post Phase 4bm-L): `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` (byte-identical).
- `research_eligible`: `false` (re-read on disk by Phase 4bm-L; unchanged).
- `eligibility_gate_status`: `"pending"` (re-read on disk by Phase 4bm-L; unchanged).
- `stage_4_feature_cleared`: `false` (re-read on disk by Phase 4bm-L; unchanged).
- `feature_config_hash`: `"819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d"`.
- `actual_feature_row_count`: `155153449`.
- `symbol`: `"BTCUSDT"`.
- `per_day_outputs` length: `90`.

The successor-state JSON's `feature_family_research_use_approved_in_principle: true` is **not equivalent** to the original manifest's `research_eligible` field. The original manifest's byte-immutability is preserved; the v002 Feature Stage-5 marker lives in the sibling successor-state JSON only.

---

## 18. Phase 4bm-J gate report preservation

The Phase 4bm-J gate report at `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json`:

- SHA256 (pre and post Phase 4bm-L): `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (byte-identical).
- Paired sidecar SHA256 (pre and post Phase 4bm-L): `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` (byte-identical).
- Records `gate_verdict = "FEATURE_GATE_PASS"`, `overall_status = "pass"`, `pass_count = 50`, `fail_count = 0`, `error_count = 0`, `not_applicable_count = 0`, `blocking_fail_count = 0` (unchanged).

---

## 19. Phase 4bm-F derived-family successor-state preservation

The Phase 4bm-F v002 derived-family Stage-3 successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json`:

- SHA256 (pre and post Phase 4bm-L): `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (byte-identical).
- Paired sidecar SHA256 (pre and post Phase 4bm-L): `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` (byte-identical).

Phase 4bm-F remains the canonical v002 Stage-3 (derived-family research-eligibility) marker. Phase 4bm-L is the new canonical v002 Feature Stage-5 (feature-family research-use admissibility) marker. The two artefacts are siblings; neither modifies the other.

---

## 20. No source / test / script / config modified

- No file under `src/prometheus/` modified.
- No file under `tests/` modified.
- No file under `scripts/` modified.
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, `.mcp.json` (absent), `.claude/`, MCP file, or credential file modified.
- The only tracked changes are the three docs files listed in §22 (this implementation report + closeout + narrow `current-project-state.md` update).

---

## 21. No labels / diagnostics / ML / strategy / backtests authorized or performed

- No label kernel run; no label parquet created; no label manifest created.
- No diagnostics run; no diagnostic output created.
- No ML training, model selection, feature ranking, meta-labeling, or hyperparameter search performed.
- No strategy specification, signal construction, or strategy-spec memo created.
- No backtest specification, plan, or execution performed.
- No simulation run; no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output computed.

The successor-state JSON records every `*_authorized` flag as `false` (20 fields) and every corresponding `no_*` negative-action flag as `true` (20 fields).

---

## 22. No endpoint / credential / MCP / Graphify / exchange-write surface touched

Phase 4bm-L touched no network surface. The successor-state JSON records this explicitly:

- `no_network_io: true`
- `no_websocket: true`
- `no_credential_read: true`
- `no_env_read: true`
- `no_mcp_or_graphify: true`
- `no_exchange_write: true`

No Binance endpoint (public, authenticated, or private) was called. No `data.binance.vision`, `fapi.binance.com`, or `api.binance.com` was contacted. No WebSocket was opened. No `.env` was read or created. No `.mcp.json` was read or created. MCP / Graphify was not enabled. No order was placed. No exchange-write surface was contacted.

---

## 23. Validation commands and results

### Pre-write validation

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-l/multi-day-v002-feature-family-research-use-successor-state-recording` |
| `git rev-parse main` | `121865a26120d5f097fee95c00185ebd4c995703` |
| `git rev-parse origin/main` | `121865a26120d5f097fee95c00185ebd4c995703` (in sync) |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| Target JSON pre-existence check | `os.path.exists(target_json)` returned `False` (no overwrite risk) |
| Target sidecar pre-existence check | `os.path.exists(target_sidecar)` returned `False` |
| Pre-write SHA recomputation of all 14 upstream evidence artefacts | all match the SHAs recorded in §15 and the prompt |
| v002 feature manifest re-read on disk | `research_eligible=False`, `eligibility_gate_status="pending"`, `stage_4_feature_cleared=False` (verified) |
| Phase 4bm-J gate report parse + invariant check | `gate_verdict="FEATURE_GATE_PASS"`, `overall_status="pass"`, `pass_count=50`, `blocking_fail_count=0` (verified) |

### Post-write validation

| Command | Result |
| ------- | ------ |
| `sha256sum <json>` | `7eccaa8f5d9dda9baab08da6914a449e163dda55619d9d734d119d378b5435e4` (size 13,499 bytes) |
| `sha256sum <sidecar>` | `c2b7333055e9c524b22fe49cb27a727efd7ff0caed6c185eed8dfe0f4aa7ab98` (size 159 bytes) |
| Sidecar byte-by-byte verification | bytes 0..63 = JSON SHA lowercase hex; bytes 64..65 = `0x20 0x20`; bytes 66..157 = ASCII basename (92 bytes); byte 158 = `0x0A`; total = 159; no CRLF, no BOM ✓ |
| `git check-ignore -v <json>` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v <sidecar>` | `.gitignore:85: data/microstructure/` |
| `git status --short` (post-write, pre-tracked-commit) | only the two pre-existing untracked entries (new files are gitignored; do not appear) |
| `git diff --check` (post-write) | clean (no whitespace errors; exit 0) |
| Post-write SHA recomputation of all 14 upstream evidence artefacts | all match pre-write values byte-identically (see §15) |
| v002 feature manifest re-read on disk | `research_eligible=False`, `eligibility_gate_status="pending"`, `stage_4_feature_cleared=False` (unchanged) |

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by Phase 4bm-L. Per the Phase 4bk-A workflow standard, the Phase 4bl-F risk-tiering standard, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight-workspace standard, and the established Tier 1 docs + local gitignored successor-state-recording precedent (Phase 4bg-B v001 derived successor-state, Phase 4bb-G v001 raw successor-state, Phase 4bl-E v002 raw successor-state, Phase 4bi-D v001 feature successor-state, Phase 4bj-G v001 label successor-state, Phase 4bj-J v001 label split-policy successor-state, Phase 4bm-F v002 derived successor-state — each of which deliberately skipped these gates for the same reason), the code / type / test gate subset is not invoked here. No source / test / script / configuration file is modified. The Phase 4bm-J branch quality gates (Phase 4bm-J surface `ruff check` PASS, whole-repo `ruff check .` PASS, targeted gate pytest 53 PASS) and the Phase 4bm-H baseline (`mypy src/prometheus`: 29 errors in 5 files; whole-repo `pytest`: 15 collection errors + 2 pre-existing `test_engine_d1a_dispatch.py` subprocess failures, both env baseline) remain unchanged by construction because Phase 4bm-L modifies no existing source / test / script.

---

## 24. Quality gate results / skipped-check rationale

- `git diff --check`: clean (exit 0).
- Repo-standard markdown lint or check: **no project-specific lightweight markdown gate exists** in this repository; therefore none is run.
- `ruff check`, `mypy src/prometheus`, `pytest` — see §23 "Tools deliberately not run".

---

## 25. What the successor-state proves

- a machine-readable v002 Feature Stage-5 research-use admissibility marker now exists for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002`;
- the marker exists only as a sibling gitignored successor-state JSON, never on the feature manifest itself;
- the original v002 feature manifest is byte-identical pre/post Phase 4bm-L (SHA `512a0a54…` unchanged);
- the entire upstream evidence chain (14 artefacts) is byte-identical pre/post Phase 4bm-L;
- the Phase 4bg-B / Phase 4bi-D / Phase 4bm-F precedent pattern (sibling-only, manifest-immutable) is correctly reproduced for the v002 feature family;
- the M0 admissibility gate, post-null cooldown rule, refined no-rescue rule, Phase 4aw flip-invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight-workspace standard, and the v002 feature-family boundary all remain binding.

---

## 26. What this phase does not prove

- the v002 feature family is **not** proven to have predictive validity;
- the v002 feature family is **not** proven to produce a tradable signal;
- the v002 evidence chain is **not** generalised to additional symbols beyond BTCUSDT;
- the v002 evidence chain is **not** generalised to additional UTC dates beyond the 90 contiguous days 2024-12-01 .. 2025-02-28;
- no label has been designed;
- no target has been defined;
- no train / validation / test split has been designed;
- no chronological split policy has been authored;
- no diagnostic question has been answered;
- no strategy hypothesis has been admitted under M0;
- no backtest has been run;
- no edge claim is made;
- no baseline-superiority claim is made;
- no out-of-sample evaluation is implied;
- no successor authorization is granted by Phase 4bm-L.

v002 Feature Stage-5 admissibility (machine-readable) is a governance state, not an empirical claim about edge.

---

## 27. Non-authorization

Phase 4bm-L does **not**, and **cannot**, authorize:

- Phase 4bm-M (any provisional successor; not authorized);
- multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K);
- multi-day v002 chronological-split-policy memo;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition (no additional days, no additional symbols, no mark-price 30m / 4h / 5m, no aggTrades acquisition beyond the existing locked v002 90-day envelope);
- Phase 5;
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
- any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` / `stage_4_feature_cleared` on any actual on-disk manifest;
- any committed `data/microstructure/` artefact;
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, Phase 4bm-E v002 derived-family decision, Phase 4bm-F v002 derived-family successor-state semantics, Phase 4bm-G v002 feature-boundary design, Phase 4bm-H v002 feature computation, Phase 4bm-I v002 feature-artefact structural QA, Phase 4bm-J v002 feature-family eligibility-gate verdict, or Phase 4bm-K v002 feature-family research-use decision;
- any further successor-state JSON creation;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

---

## 28. Recommended state

**Remain paused.**

Phase 4bm-L is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main` per `merge-closeout-standard.md` (Tier 1; full 16-section merge-closeout).

The v002 multi-day derived / feature family now has a complete ladder of evidence through **v002 Feature Stage-5 (machine-readable research-use admissibility)**:

- Stage-0 (acquired + normalized): Phase 4bm-B output (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest).
- Stage-1 (inspected): Phase 4bm-C 56 / 56 multi-day structural QA PASS.
- Stage-2 (gate-passed at report level): Phase 4bm-D 60 / 60 `DERIVED_GATE_PASS`.
- Stage-2-decision: Phase 4bm-E Option B / Decision form 2.
- Stage-3 (machine-readable successor-state marker, derived): Phase 4bm-F successor-state JSON SHA `72b6edd4…`.
- v002 Feature Stage-0 (design): Phase 4bm-G feature-boundary design memo.
- v002 Feature Stage-2 (artefacts): Phase 4bm-H computed feature artefacts (155,153,449 rows; 62-column canonical schema).
- v002 Feature Stage-3 (inspected): Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`.
- v002 Feature Stage-4 (gate-passed at report level): Phase 4bm-J 50 / 50 `FEATURE_GATE_PASS`.
- v002 Feature Stage-5 admissibility decision (policy-level only): Phase 4bm-K Outcome 1 / Decision form 1.
- **v002 Feature Stage-5 machine-readable successor-state marker (feature-family research-use admissibility)**: Phase 4bm-L successor-state JSON SHA `7eccaa8f…` (this phase).

The actual v002 feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 29. Conditional next options, none authorized

| Option | Type | Status |
| --- | --- | --- |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 lifecycle ladder** — future docs-only multi-day v002 label-family boundary / design memo (multi-day analogue of Phase 4bj-A) | docs-only; no computation | **NOT authorized by this memo** |
| **Conditional later** — future docs-only multi-day v002 chronological split-policy memo (multi-day analogue of Phase 4bj-H / 4bj-I) | docs-only | **NOT authorized by this memo** |
| **Conditional further along** — multi-day v002 label-family schema, kernel, structural QA, eligibility gate, research-use decision, successor-state recording (multi-day analogues of Phase 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G) | code + docs + local gitignored output | **NOT authorized by this memo** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Diagnostics / ML / strategy / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-L** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-L** |

---

## 30. Preserved boundaries

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
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant (preserved; **never invoked** by Phase 4bm-L).
- Phase 4bb-F canonical path policy.
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks.
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard.
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard.
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A..G / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E / 4bm-F / 4bm-G / 4bm-H / 4bm-I / 4bm-J / 4bm-K results — all preserved verbatim.

Reusable non-authorization blocks honored: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**. **N-SUCCESSOR-STATE** does NOT apply (Phase 4bm-L creates exactly one new sibling successor-state artefact, governed by the Phase 4bi-D / Phase 4bm-F precedent).

---

## 31. Required exact phrases (verbatim, per task brief)

- **This successor-state JSON is the machine-readable v002 Feature Stage-5 research-use marker.**
- **The v002 feature manifest remains byte-identical.**
- **The v002 feature manifest still carries research_eligible=false, eligibility_gate_status="pending", and stage_4_feature_cleared=false.**
- **Phase 4bm-M is not authorized by Phase 4bm-L.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-L.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**
