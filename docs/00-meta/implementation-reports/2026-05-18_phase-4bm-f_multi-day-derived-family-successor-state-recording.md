# Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording

**Phase identity:** Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording (docs + local gitignored successor-state JSON + paired Phase 4bb-F sidecar).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-f/multi-day-derived-family-successor-state-recording`.
**Base:** `main` at `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` (Phase 4bm-E merge-closeout SHA-finalization commit; pre-branch `main == origin/main` in sync).
**Tier:** Tier 1 (docs + local gitignored output; governance / successor-state recording; multi-day analogue of Phase 4bg-B for the v002 derived family).
**Phase type:** docs + local gitignored output — adds two new tracked docs files under `docs/00-meta/implementation-reports/`, narrowly updates `docs/00-meta/current-project-state.md`, and writes exactly one new local gitignored successor-state JSON + paired canonical Phase 4bb-F sidecar under `data/microstructure/successor-state/`. No source / test / script / configuration / manifest / sidecar / gate-report mutation; no normalized Parquet, raw zip, feature parquet, label parquet, or any other prior `data/microstructure/` artefact touched.
**Status:** drafted; pending operator review.

---

## 1. Phase header

This phase operationalises the Phase 4bm-E Option B / Decision form 2 outcome:

> Stage-3 is admissible in principle at policy level for the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events), but no manifest mutation occurs in Phase 4bm-E. A separately authorized successor-state recording phase, Phase 4bm-F, is required before any machine-readable `research_eligible = true` marker exists for the v002 derived family.

Phase 4bm-F records that machine-readable Stage-3 successor-state marker as a sibling artefact under `data/microstructure/successor-state/`, while preserving the original v002 derived multi-day index manifest, the v002 raw manifest, all v001 manifests, the 90 v002 per-day Parquets and sidecars, the 90 v002 raw zips and sidecars, the Phase 4bm-D authoritative gate report, the Phase 4bl-D-R raw multi-day PASS gate report, the Phase 4bl-E raw successor-state JSON, the Phase 4bg-B v001 derived successor-state JSON, and every other prior `data/microstructure/` artefact byte-identically.

Phase 4bm-F is the **multi-day analogue of Phase 4bg-B** (the v001 derived-family Stage-3 successor-state recording phase). The Phase 4bg-B v001 successor-state JSON (SHA `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`) remains the canonical Stage-3 marker for v001; the new Phase 4bm-F v002 successor-state JSON is the canonical Stage-3 marker for v002.

---

## 2. Why Phase 4bm-F exists

The Phase 4bm-D 60 / 60 PASS `DERIVED_GATE_PASS` result is **report-level only**. Per the Phase 4bb-E / Phase 4bf / Phase 4bg-A / Phase 4bg-B precedent (now preserved verbatim across the v002 lifecycle), report-level PASS does not flip any actual on-disk manifest field. The actual v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` continues to carry `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically.

Phase 4bm-E (Option B / Decision form 2) recorded that Stage-3 is admissible in principle at policy level for the multi-day v002 derived family, but explicitly required a separately authorized successor-state recording phase before any machine-readable `research_eligible = true` marker exists. Phase 4bm-F is exactly that separately authorized phase.

The successor-state JSON is a **sibling artefact**, not a manifest replacement. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked by Phase 4bm-F). Any future tool that wishes to interpret the v002 derived family as Stage-3 must read the successor-state JSON, not the original manifest.

---

## 3. Linkage to Phase 4bm-E Option B / Decision form 2

The Phase 4bm-F successor-state JSON cites the Phase 4bm-E decision verbatim:

- `phase_4bm_e_decision: "Option B / Decision form 2"`
- `phase_4bm_e_decision_phase_id: "4bm-E"`
- `phase_4bm_e_branch_commit_sha: "1715a8adaa6eeeb478c7af363ed39af311783773"`
- `phase_4bm_e_merge_commit_sha: "fcc1bd044d274c99520b4ab15282046e1428b3d0"`
- `phase_4bm_e_merge_closeout_commit_sha: "d6acae535fee19a074096e3d7fa3590f4a0dd9ec"`

Phase 4bm-E recorded the policy-level Stage-3 admissibility decision; Phase 4bm-F records the machine-readable Stage-3 successor-state marker. These two phases together complete the v002 multi-day analogue of the Phase 4bg-A → Phase 4bg-B v001 single-day lifecycle.

---

## 4. Linkage to Phase 4bg-B v001 successor-state precedent

The Phase 4bm-F successor-state JSON cites the direct v001 precedent:

- `phase_4bg_b_v001_derived_successor_state_phase: "4bg-B"`
- `phase_4bg_b_v001_derived_successor_state_path: "data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json"`
- `phase_4bg_b_v001_derived_successor_state_sha256: "8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e"`

The Phase 4bm-F filename mirrors the Phase 4bg-B v001 filename pattern exactly: `microstructure_normalized_aggtrades_v001__<version>__stage3_research_eligible__<phase>.json`. The schema is a compact extension of the Phase 4bg-B v001 schema, augmented with multi-day-specific fields (90-date range, total event count, v002 raw lineage, Phase 4bl-D-R / Phase 4bl-E raw multi-day evidence, Phase 4bm-B / 4bm-C / 4bm-D pipeline, Phase 4bm-E decision linkage) and an expanded `boundary_confirmations` block.

---

## 5. Schema design

The Phase 4bm-F successor-state JSON follows the Phase 4bg-B compact schema as its primary precedent, expanded with multi-day-specific fields and the prompt-required non-authorization markers. The top-level field grouping is:

1. **Schema & phase identity** — `schema_version`, `phase_id`, `phase_name`, `dataset_family`, `dataset_version`.
2. **Successor stage semantics** — `successor_state_kind`, `successor_stage`, `successor_state_type`, `successor_research_eligible`, `successor_eligibility_gate_status`, `stage_3_policy_admissible`, `research_eligible_successor_state`.
3. **Multi-day v002 family identity** — `symbol`, `symbol_list`, `utc_date_start`, `utc_date_end`, `date_count`, `event_count`.
4. **Original v002 derived manifest preservation** — path, SHAs, original states, byte-identical confirmation.
5. **v002 raw family lineage** — path, SHAs, gate report, raw successor-state JSON SHA.
6. **Phase 4bm-B / 4bm-C / 4bm-D pipeline evidence** — predecessor phases, gate report ID / SHA / verdict / result / boundary confirmations / commit SHAs.
7. **Phase 4bm-E decision linkage** — decision, branch commit, merge commit, merge-closeout commit.
8. **Phase 4bg-B v001 precedent cross-reference** — phase, path, SHA.
9. **v001 derived manifest cross-reference** — path, SHA, original states.
10. **Non-authorization & governance label fields** — `feature_computation`, `labels`, `ml`, `strategy`, `backtest`, `diagnostics`, `acquisition`, and the explicit `*_authorized: false` markers required by the operator prompt.
11. **Negative-action confirmations** — `no_manifest_mutation`, `no_data_mutation_except_this_successor_state`, `no_feature_computed`, etc.
12. **Governance preservation** — `governance_locks_preserved`, `retained_verdicts_preserved`, `phase_4aw_invariant` statement.
13. **Creation metadata** — `base_commit_sha`, `docs_commit_sha_at_creation`, `created_at_unix_ms`, `created_at_utc`.
14. **Notes** — plain-English explanation of the machine-readable Stage-3 marker semantics.
15. **`boundary_confirmations` object** — 43 explicit `true` markers covering every preservation and non-action guarantee.

---

## 6. Exact successor-state JSON path

```text
data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
```

Absolute path on the local workstation:

```text
C:\Prometheus\data\microstructure\successor-state\microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
```

The filename mirrors the Phase 4bg-B v001 precedent (`microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`) exactly, with `v001 → v002` and `phase-4bg-b → phase-4bm-f`.

---

## 7. Exact successor-state JSON SHA256

```text
72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9
```

Size: 9,963 bytes. UTF-8 (no BOM). LF line endings only. Two-space indent. Final newline at EOF.

---

## 8. Exact successor-state sidecar path

```text
data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256
```

Absolute path on the local workstation:

```text
C:\Prometheus\data\microstructure\successor-state\microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json.sha256
```

---

## 9. Exact sidecar file SHA256

```text
1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97
```

Size: 157 bytes. UTF-8 (no BOM, ASCII content only). Single line with trailing LF.

---

## 10. Exact sidecar content

Canonical Phase 4bb-F sidecar format (`<sha256_lowercase_hex><two ASCII spaces><basename><LF>`):

```text
72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9  microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json
```

Byte-by-byte verification (all checks PASS):

- Bytes 0..63: lowercase hex of the JSON SHA256 (`72b6edd4...309ea9`).
- Bytes 64..65: `0x20 0x20` (two ASCII spaces).
- Bytes 66..155: ASCII basename `microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (90 bytes).
- Byte 156: `0x0A` (LF terminator).
- Total: 64 + 2 + 90 + 1 = **157 bytes** (matches `Get-Item.Length`).
- The embedded SHA matches the recomputed `Get-FileHash` of the JSON byte-for-byte (no drift).

---

## 11. Pre/post SHAs for preserved evidence artefacts

The following 10 evidence artefacts were verified byte-identical before and after Phase 4bm-F. Each SHA was recomputed at the start of this phase, then recomputed again after the successor-state JSON + sidecar were written.

| Artefact | SHA256 (pre and post Phase 4bm-F) | Status |
| -------- | ---------------------------------- | ------ |
| v002 derived multi-day index manifest (`microstructure_normalized_aggtrades_v001__v002.json`) | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | IDENTICAL |
| v002 derived manifest sidecar (`...v002.json.sha256`) | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | IDENTICAL |
| v002 raw manifest (`microstructure_raw_aggtrades_v001__v002.json`) | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | IDENTICAL |
| v002 acquisition log (`...v002_acquisition_log.json`) | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | IDENTICAL |
| v001 derived manifest (`microstructure_normalized_aggtrades_v001__v001.json`) | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` | IDENTICAL |
| Phase 4bm-D authoritative derived gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | IDENTICAL |
| Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | IDENTICAL |
| Phase 4bl-D-R raw multi-day `RAW_MULTIDAY_GATE_PASS` report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | IDENTICAL |
| Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | IDENTICAL |
| Phase 4bg-B v001 derived successor-state JSON (precedent) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` | IDENTICAL |

The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, and 90 v002 raw zip sidecars are byte-identical pre- and post-Phase-4bm-F by construction (Phase 4bm-F reads no Parquet, runs no kernel, and writes nothing outside `data/microstructure/successor-state/`).

---

## 12. Original v002 derived manifest preservation

The original v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json`:

- SHA256 (pre and post Phase 4bm-F): `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` (byte-identical).
- `research_eligible`: `false` (re-read on disk by Phase 4bm-F; unchanged).
- `eligibility_gate_status`: `"pending"` (re-read on disk by Phase 4bm-F; unchanged).
- `dataset_family`: `microstructure_normalized_aggtrades_v001`.
- `dataset_version`: `v002`.

The successor-state JSON's `successor_research_eligible: true` is **not equivalent** to the original manifest's `research_eligible` field. The original manifest's byte-immutability is preserved; the Stage-3 marker lives in the sibling successor-state JSON only.

---

## 13. v002 raw manifest preservation

The v002 raw manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`:

- SHA256 (pre and post Phase 4bm-F): `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` (byte-identical).
- `research_eligible`: `false` (re-read on disk by Phase 4bm-F; unchanged).
- `eligibility_gate_status`: `"pending"` (re-read on disk by Phase 4bm-F; unchanged).

---

## 14. Raw-family research eligibility — permanently false

The raw family `microstructure_raw_aggtrades_v001` remains **permanently** `research_eligible = false` across both v001 and v002 versions, per the Phase 4bb-E (raw v001) and Phase 4bl-E (raw v002) policy precedents. Phase 4bm-F does not amend the raw-family policy. The Phase 4bl-E raw multi-day successor-state JSON (SHA `a0576ca6…`) is unchanged and remains the canonical raw v002 Stage-2 marker.

The successor-state JSON records this explicitly:

- `raw_family_research_eligible: false`
- `raw_family_eligibility_gate_status: "pending"`
- `raw_family_permanently_ineligible: true`

---

## 15. Machine-readable Stage-3 marker for v002

The Phase 4bm-F successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` (SHA `72b6edd4…`) is the canonical machine-readable Stage-3 marker for the multi-day v002 derived family.

Key fields:

- `successor_state_kind: "research_eligibility_successor_state"`
- `successor_stage: "Stage-3"`
- `successor_state_type: "research_eligibility"`
- `successor_research_eligible: true`
- `successor_eligibility_gate_status: "pass"`
- `stage_3_policy_admissible: true`
- `research_eligible_successor_state: true`

Any future tool that needs to interpret the v002 derived family as Stage-3 must read this successor-state artefact, **not** the original v002 derived multi-day index manifest. The original manifest remains `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically.

---

## 16. Stage-4 remains unauthorized

Stage-4 (feature-cleared) is **not** authorized by Phase 4bm-F for the v002 derived family. The successor-state JSON records this explicitly:

- `stage_4_feature_cleared: false`
- `feature_computation_authorized: false`
- `successor_authorization_after: false`
- `no_successor_authorization: true`

Any future v002 feature work requires a separately authorized multi-day v002 feature-boundary design memo (multi-day analogue of Phase 4bh-A / Phase 4bh-B; not authorized by Phase 4bm-F) and a separately authorized v002 feature implementation phase (multi-day analogue of Phase 4bh; not authorized by Phase 4bm-F).

The Phase 4bh-A / Phase 4bh-B v001 feature-boundary designs do **not** transitively cover v002; they are v001-specific and cite the Phase 4bd v001 normalized Parquet SHA, the Phase 4bg-B v001 successor-state JSON SHA, and Phase 4bf gate report SHA verbatim.

---

## 17. Feature / label / diagnostics / ML / strategy / backtest unauthorized

All downstream work on v002 (and on v001) remains forbidden. The successor-state JSON records this explicitly:

- `feature_computation: "forbidden"`
- `labels: "forbidden"`
- `ml: "forbidden"`
- `strategy: "forbidden"`
- `backtest: "forbidden"`
- `diagnostics: "forbidden"`
- `acquisition: "unauthorized"`
- `label_computation_authorized: false`
- `diagnostics_authorized: false`
- `ml_authorized: false`
- `strategy_authorized: false`
- `backtest_authorized: false`
- `acquisition_authorized: false`

The Phase 4ak M0 admissibility gate (twelve clauses) and the post-null cooldown rule remain binding for any future strategy hypothesis. The microstructure / order-flow / liquidity-timing lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption. Cooled-down families (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane) remain cooled down.

---

## 18. Network / credential / MCP / WebSocket / exchange-write — none touched

Phase 4bm-F touched no network surface. The successor-state JSON records this explicitly:

- `no_network_io: true`
- `no_websocket: true`
- `no_credential_read: true`
- `no_env_read: true`
- `no_mcp_or_graphify: true`
- `paper_shadow_authorized: false`
- `live_readiness_authorized: false`
- `exchange_write_authorized: false`
- `phase_5_authorized: false`

No Binance endpoint (public, authenticated, or private) was called. No `data.binance.vision`, `fapi.binance.com`, or `api.binance.com` was contacted. No WebSocket was opened. No `.env` was read or created. No `.mcp.json` was read or created. MCP / Graphify was not enabled. No order was placed. No exchange-write surface was contacted.

---

## 19. Validation commands and results

### Pre-write validation

| Command | Result |
| ------- | ------ |
| `git status --short` | only `.claude/scheduled_tasks.lock` and `data/research/` untracked (expected) |
| `git branch --show-current` | `phase-4bm-f/multi-day-derived-family-successor-state-recording` |
| `git rev-parse main` | `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` |
| `git rev-parse origin/main` | `fb0aa97561702c3c2c91dd1e451ae6fe7bf90ece` (in sync) |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| Target file pre-existence check | `Test-Path …phase-4bm-f.json` returned `False` (no overwrite risk) |
| Target sidecar pre-existence check | `Test-Path …phase-4bm-f.json.sha256` returned `False` |
| Pre-write SHA recomputation of all 10 upstream evidence artefacts | all match the SHAs recorded in §11 and the prompt |

### Post-write validation

| Command | Result |
| ------- | ------ |
| `Get-FileHash <json> -Algorithm SHA256` | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` (size 9,963 bytes) |
| `Get-FileHash <sidecar> -Algorithm SHA256` | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` (size 157 bytes) |
| Sidecar byte-by-byte verification | bytes 0..63 = JSON SHA lowercase hex; bytes 64..65 = `0x20 0x20`; bytes 66..155 = ASCII basename; byte 156 = `0x0A`; total = 157 ✓ |
| `git check-ignore -v <json>` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v <sidecar>` | `.gitignore:85: data/microstructure/` |
| `git status --short` (post-write, pre-tracked-commit) | only the two pre-existing untracked entries (new files are gitignored; do not appear) |
| `git diff --check` (post-write) | clean (no whitespace errors) |
| JSON parses cleanly via `ConvertFrom-Json` | `phase_id="4bm-F"`, `successor_stage="Stage-3"`, `successor_research_eligible=True`, `successor_eligibility_gate_status="pass"`, `date_count=90`, `event_count=155153449`, all 43 `boundary_confirmations` fields = `True` |
| Post-write SHA recomputation of all 10 upstream evidence artefacts | all match pre-write values byte-identically (see §11) |
| v002 derived manifest re-read on disk | `research_eligible=False`, `eligibility_gate_status="pending"` (unchanged) |
| v002 raw manifest re-read on disk | `research_eligible=False`, `eligibility_gate_status="pending"` (unchanged) |
| v001 derived manifest re-read on disk | `research_eligible=False`, `eligibility_gate_status="pending"` (unchanged) |

### Tools deliberately not run

`ruff`, `mypy`, and `pytest` were **not** invoked by Phase 4bm-F. Per the Phase 4bk-A workflow standard, the Phase 4bl-F risk-tiering standard, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight-workspace standard, and the established Tier 1 docs-and-local-gitignored-output successor-state-recording precedent (Phase 4bg-B v001 derived successor-state, Phase 4bb-G v001 raw successor-state, Phase 4bl-E v002 raw successor-state, Phase 4bi-D v001 feature successor-state, Phase 4bj-G v001 label successor-state, Phase 4bj-J v001 label split-policy successor-state — each of which deliberately skipped these gates for the same reason), the code / type / test gate subset is not invoked here. No source / test / script / configuration file is modified. The most recent authoritative whole-repo `pytest` baseline (`1156 passed, 1 skipped`; two pre-existing simulation `KeyError: 'trade_count'` failures unrelated to this work) remains unchanged.

---

## 20. Recommended state

**Remain paused.**

Phase 4bm-F is branch-complete only by this work. Per the Phase 4bk-A workflow standard, it is NOT project-complete until a separately authorized merge phase records its merge-closeout on `main`.

The v002 multi-day derived family now has:

- Stage-0 (acquired + normalized): Phase 4bm-B output (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest).
- Stage-1 (inspected): Phase 4bm-C 56 / 56 multi-day structural QA PASS.
- Stage-2 (gate-passed at report level): Phase 4bm-D 60 / 60 PASS with `DERIVED_GATE_PASS`.
- **Stage-3 (machine-readable successor-state marker)**: Phase 4bm-F successor-state JSON (SHA `72b6edd4…`).

The actual v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"` byte-identically. The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

---

## 21. Conditional next options, none authorized

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | **recommended** |
| **Conditional next, if continuing on the v002 lifecycle ladder** — future docs-only multi-day v002 feature-boundary design memo (multi-day analogue of Phase 4bh-A / Phase 4bh-B) | docs-only; no computation | **NOT authorized by this memo** |
| **Conditional later** — future code + docs multi-day v002 feature schema / feature computation implementation (multi-day analogue of Phase 4bh) | code + docs; only after Stage-4 authorization on v002 | **NOT authorized by this memo** |
| **Conditional later still** — multi-day v002 feature-family structural QA / eligibility gate / research-use decision / successor-state recording (multi-day analogues of Phase 4bi-A / Phase 4bi-B / Phase 4bi-C / Phase 4bi-D) | docs + code + local gitignored output | **NOT authorized by this memo** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope** |
| Feature / label / ML / strategy / diagnostics / backtest work on v002 (or v001) | code + data | **FORBIDDEN by Phase 4bm-F** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-F** |

---

## 22. No successor phase is authorized

**Phase 4bm-F does not authorize Phase 4bm-G, any multi-day v002 feature-boundary design memo, any multi-day v002 feature implementation phase, any multi-day v002 feature-family structural QA / eligibility gate / research-use decision / successor-state recording, any multi-day v002 label-family phases, Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-* / Phase 4bq-* / any other Phase 4 successor, Phase 5, Phase 4 canonical, feature computation, label computation, diagnostics rerun, ML training / model selection / feature ranking / meta-labeling, strategy implementation / signal construction / backtest implementation, additional acquisition (beyond the 90 locked v002 BTCUSDT UTC dates), paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, public-endpoint calls in code, user-stream / live WebSocket implementation, MCP / Graphify / `.mcp.json` / credentials, any modification of `research_eligible` / `eligibility_gate_status` / `chronological_split_policy` on any on-disk manifest, any further successor-state JSON creation, agents-by-default for heavy Claude Code execution sessions, or copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light`.**

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, Phase 4bl-F four-tier risk model, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, and merge-closeout standard.

---

## 23. Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 / 4bm-E results — all preserved verbatim.
