# Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo

**Phase identity:** Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo (docs-only).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-e/multi-day-derived-family-research-eligibility-decision-memo`.
**Base:** `main` at `8234375f927f029211747eeae4ef493c612b2df3` (Phase 4bm-D-P1 merge-closeout commit; pre-branch `main == origin/main` in sync).
**Tier:** Tier 1 (docs-only Full Phase; governance / research-eligibility decision; multi-day analogue of Phase 4bg-A).
**Phase type:** docs-only research-eligibility decision / governance memo — no source / test / script / config / data mutation; no manifest mutation; no successor-state artefact creation; no gate rerun; no acquisition; no successor authorization.
**Status:** drafted; pending operator review.

---

## 1. Phase header

This memo answers a single question:

> Given the Phase 4bm-A → Phase 4bm-B Stage-0 multi-day v002 derived artefacts, the Phase 4bm-C 56 / 56 structural QA PASS, and the Phase 4bm-D 60 / 60 derived-family eligibility gate PASS at report level (`overall_status = pass`; `gate_verdict = DERIVED_GATE_PASS`; gate-report SHA256 `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a`), should the project authorize a future Stage-3 research-eligibility transition **in principle** for the multi-day v002 derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events), and under what exact constraints?

The memo is **docs-only**. It records a policy-level decision. It does not mutate any manifest, flip any `research_eligible` flag, transition any `eligibility_gate_status`, run any gate, modify any data file, compute any feature, label, signal, proxy, ML, strategy, or backtest output, acquire any data, or authorize any successor implementation.

The memo preserves every retained verdict, every project lock, the Phase 4ak twelve-clause M0 admissibility gate (including the post-null cooldown rule and cooled-down families list), the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant, the Phase 4bb-F canonical path policy, the Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks, the Phase 4bm-A-P1 thin-prompt context-management standard, and the Phase 4bm-D-P1 lightweight Claude Code workspace standard.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bm-D-P1 merge-closeout commit (pre-branch `main` SHA) | `8234375f927f029211747eeae4ef493c612b2df3` |
| Phase 4bm-D merge commit | `a80b8a050c66397c8a4a51a9a6e87b7f8c785dbc` |
| Phase 4bm-D implementation commit (`code_commit_sha` recorded inside the gate report) | `57e1c97e6e938797d448b331cdc27b50b8e935dd` |
| Phase 4bm-D merge-closeout (on `main`) | `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-d_merge-closeout.md` |
| Phase 4bm-D-P1 merge-closeout (on `main`) | `docs/00-meta/implementation-reports/2026-05-17_phase-4bm-d-p1_merge-closeout.md` |
| Multi-day v002 derived family | `microstructure_normalized_aggtrades_v001`, `dataset_version = v002`, `research_eligible = false`, `eligibility_gate_status = "pending"` (verified on disk) |
| Multi-day v002 raw family | `microstructure_raw_aggtrades_v001`, `dataset_version = v002`, `research_eligible = false`, `eligibility_gate_status = "pending"` (verified on disk) |
| Single-day v001 derived family (Phase 4bd) | `microstructure_normalized_aggtrades_v001`, `dataset_version = v001`, `research_eligible = false`, `eligibility_gate_status = "pending"` (verified on disk) |
| Symbol scope (v002) | BTCUSDT only |
| UTC date scope (v002) | 2024-12-01 .. 2025-02-28 (90 contiguous UTC dates) |
| Event count (v002) | 155,153,449 events across the 90 days |
| Approx. parquet footprint (v002) | ~1.40 GiB across the 90 per-day Parquets |
| Phase 4bm-D authoritative gate report path | `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` |
| Phase 4bm-D authoritative gate report SHA256 | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (recomputed on disk; matches) |
| Phase 4bm-D authoritative sidecar SHA256 | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` (recomputed on disk; matches) |
| Phase 4bm-D `overall_status` | `pass` |
| Phase 4bm-D `gate_verdict` | `DERIVED_GATE_PASS` |
| Phase 4bm-D checks | 60 / 60 PASS (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE) |
| Phase 4bm-D `research_eligible_after` | `False` (hard invariant; report-level) |
| Phase 4bm-D `eligibility_gate_status_after` | `"pass"` (report-level recommendation only; not written back to any manifest) |
| Phase 4bm-D `no_successor_authorization` | `True` (hard invariant) |
| Phase 4bm-D boundary confirmations | 19 / 19 `True` |
| v002 derived multi-day index manifest SHA256 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 raw manifest SHA256 | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v001 derived manifest SHA256 | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| `data/microstructure/` git status | gitignored at `.gitignore:85: data/microstructure/` (covers `gate-reports/`, `manifests/`, `successor-state/`, `normalized/`, `raw/`) |

---

## 3. Inputs reviewed

Phase 4bm-E is grounded in the full v002 multi-day evidence chain plus the v001 single-day precedent:

- Phase 4bl-A multi-day expansion requirements memo;
- Phase 4bl-B multi-day acquisition authorization / design memo;
- Phase 4bl-C multi-day aggTrades acquisition execution (90 daily raw zips + 90 canonical Phase 4bb-F sidecars; 90 dates 2024-12-01 .. 2025-02-28);
- Phase 4bl-D multi-day raw manifest eligibility gate (failed at first attempt — preserved as research evidence);
- Phase 4bl-D-S1 sidecar canonicalization governance memo;
- Phase 4bl-D-S2 controlled sidecar canonicalization execution;
- Phase 4bl-D-R multi-day raw manifest eligibility gate rerun (`RAW_MULTIDAY_GATE_PASS`);
- Phase 4bl-E multi-day raw manifest successor-state recording;
- Phase 4bl-F phase risk-tiering and controlled remediation standard (Tier 1 / Tier 2 / Tier 3 / Tier 4; R-SIDECAR-CRLF; nine reusable non-authorization blocks);
- Phase 4bm-A multi-day normalization design memo;
- Phase 4bm-A-P1 thin-prompt Claude Code context-management standard;
- Phase 4bm-B multi-day normalization implementation (90 per-day v002 derived Parquets + 90 sidecars + v002 multi-day index manifest);
- Phase 4bm-C multi-day normalized structural QA memo (56 / 56 PASS read-only structural QA);
- Phase 4bm-D multi-day derived-family eligibility gate implementation and execution (60 / 60 PASS; `DERIVED_GATE_PASS`; report SHA `3b45e70b…`);
- Phase 4bm-D-P1 lightweight Claude Code workspace execution standard;
- Phase 4bg-A single-day v001 derived-family research-eligibility decision memo (the direct v001 precedent; Option B / Decision form 2);
- Phase 4bg-B single-day v001 derived-family research-eligibility successor-state policy / recording memo (the direct v001 successor-state precedent; sibling successor-state JSON, original manifest preserved byte-identically).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified.

---

## 4. Scope

In scope for this memo:

- evaluating the question: is Stage-3 research-eligibility admissible **in principle** for the multi-day v002 normalized derived family at this point in the project record?
- selecting one of five docs-only decision options (A–E) and justifying the choice;
- defining the 15 minimum Stage-3 admissibility criteria for the multi-day v002 derived family;
- mapping the available evidence (Stages 0, 1, and report-level Stage 2) onto those criteria;
- recording the residual risks, the raw-family permanence rule, the derived-manifest immutability rule for this phase, the multi-day-specific limitations, the feature-boundary policy, and the ML / strategy boundary;
- recommending the conservative successor sequence without authorizing any successor.

---

## 5. Non-scope

This memo does **not**:

- modify any source code, test, script, configuration, dataset, manifest, sidecar, gate report, successor-state JSON, or any tracked file beyond this memo, its closeout, and a narrow `current-project-state.md` paragraph + new "Current phase:" block (with the prior Phase 4bm-D-P1 block preserved as labelled historical context);
- run the multi-day normalizer, the multi-day raw eligibility gate, or the multi-day derived-family gate;
- generate a new gate report, regenerate the Phase 4bm-D authoritative gate report, or modify the Phase 4bm-D authoritative gate report;
- create or modify any `data/microstructure/` artefact;
- create JSONL, Parquet, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position-state, or any column beyond the 19-column Phase 4bc / Phase 4bm-A canonical normalized schema;
- train ML, create strategy logic, run backtests, run simulations, or compute any prediction / model-score / decision-score;
- flip `research_eligible` on any family;
- transition `eligibility_gate_status` on any actual on-disk manifest;
- change `chronological_split_policy` on any actual on-disk manifest;
- authorize Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests;
- revise retained verdicts, change project locks, or amend M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1;
- authorize Phase 4bm-F (multi-day v002 derived-family successor-state recording), Phase 4bm-G, Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 that apply to this memo: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

---

## 6. Stage-0 evidence review (multi-day v002)

**Stage 0 — acquired and normalized** (Phase 4ba ladder, multi-day analogue): the multi-day v002 derived artefacts have been produced by Phase 4bm-B and exist locally in the gitignored `data/microstructure/` namespace.

| Stage-0 artefact (multi-day v002) | Path | SHA256 |
| --------------------------------- | ---- | ------ |
| 90 per-day normalized Parquets | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/<YYYY>/<MM>/BTCUSDT-aggTrades-<YYYY>-<MM>-<DD>.parquet` for each of the 90 dates 2024-12-01 .. 2025-02-28 | recorded in the Phase 4bm-B implementation report and preserved byte-identically through Phase 4bm-C and Phase 4bm-D (per Phase 4bm-D `no_per_file_parquet_mutation = True` and `no_per_file_sidecar_mutation = True`) |
| 90 paired `.sha256` sidecars | same paths + `.sha256` suffix | canonical Phase 4bb-F format; pre/post identical |
| v002 derived multi-day index manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` |
| v002 derived manifest sidecar | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256` | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` |

The v002 derived index manifest carries:

- `dataset_family = microstructure_normalized_aggtrades_v001`,
- `dataset_version = v002`,
- 90 daily entries covering 2024-12-01 .. 2025-02-28 inclusive,
- per-day `event_count` sum totalling 155,153,449 events,
- `research_eligible = false` (verified on disk),
- `eligibility_gate_status = "pending"` (verified on disk),
- governance labels referencing the v002 raw lineage (raw manifest SHA `016967865c97…`, raw zip SHAs per day, acquisition log SHA `52f6d7fb…`, Phase 4bl-D-R `RAW_MULTIDAY_GATE_PASS` report SHA `f9493fd1…`, Phase 4bl-E successor-state SHA `a0576ca6…`),
- `feature_computation = forbidden`,
- `strategy_use = forbidden`.

The multi-day v002 derived family is **reproducible locally** from the 90 raw archives plus the Phase 4bm-B normalizer (which is now project-complete on `main`). It is gitignored, not committed.

**Stage-0 verdict (multi-day v002):** evidence-positive.

---

## 7. Stage-1 evidence review (multi-day v002)

**Stage 1 — inspected** (Phase 4ba ladder, multi-day analogue): the multi-day v002 Stage-0 artefacts have been structurally inspected.

Phase 4bm-C ran the multi-day structural QA memo over the v002 derived family and recorded **56 / 56 PASS** with no FAIL, no ERROR, and no NOT_APPLICABLE (the Phase 4bm-C scope is the multi-day analogue of the Phase 4be single-day 60 / 60 PASS).

Phase 4bm-C confirmed at the multi-day level:

- the 90 per-day Parquet schemas are exactly the 19 Phase 4bc / Phase 4bm-A canonical columns in canonical order;
- the schemas contain no feature, label, signal, proxy, ML, or strategy column;
- per-day `row_count` matches each day's manifest `event_count`;
- per-day `row_index` is contiguous `0..n−1` with no duplicates;
- per-day `agg_trade_id` is non-decreasing within each day and contains the per-day unique-count published in the manifest;
- per-day first / last `transact_time_ms` lie inside each day's half-open UTC window;
- `price` and `quantity` are stored as Decimal-as-string (lossless; no float storage) across every per-day Parquet;
- `is_buyer_maker` is strict bool across every per-day Parquet;
- per-row lineage columns are constant and reference the correct upstream evidence per day (correct `symbol`, `utc_date`, `dataset_family`, `dataset_version`, `source_manifest_sha256`, etc.);
- the multi-day index manifest's per-day entries are mutually consistent with the per-day Parquet contents;
- the v002 raw manifest, v002 raw zips, v002 acquisition log, v002 derived index manifest, v002 derived sidecar, and the Phase 4bl-D-R gate report / sidecar / Phase 4bl-E successor-state are byte-identical pre vs post the Phase 4bm-C inspection;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved.

**Stage-1 verdict (multi-day v002):** evidence-positive.

---

## 8. Stage-2 report-level evidence review (multi-day v002)

**Stage 2 — gate-passed at report level** (Phase 4ba ladder, multi-day analogue; Phase 4bb-E / Phase 4bf precedent): the Stage-1-inspected multi-day v002 artefacts have been put through the separately authorized Phase 4bm-D 60-check multi-day derived-family eligibility gate and the gate emitted a PASS report. The actual manifest fields have not been transitioned (this is exactly the Phase 4bb-E / Phase 4bf precedent, scaled to the multi-day level).

Phase 4bm-D executed the 60-check multi-day derived-family eligibility gate **exactly once** read-only from the implementation commit `57e1c97e6e938797d448b331cdc27b50b8e935dd`, and recorded:

- `overall_status = pass`;
- `gate_verdict = DERIVED_GATE_PASS`;
- `len(checks) = 60`;
- PASS / FAIL / NOT_APPLICABLE / ERROR = **60 / 0 / 0 / 0**;
- `research_eligible_after = False` (hard invariant for raw and derived raw-lineage families);
- `eligibility_gate_status_after = "pass"` (report-level recommendation only; **not** written to any actual on-disk manifest);
- `no_successor_authorization = True` (hard invariant);
- 19 / 19 boundary confirmations `True` (verified on disk this phase):
  - `no_manifest_mutation`,
  - `no_per_file_parquet_mutation`,
  - `no_per_file_sidecar_mutation`,
  - `no_raw_zip_mutation`,
  - `no_normalization_written_outside_namespace`,
  - `no_data_microstructure_write_outside_gate_reports`,
  - `no_feature_computed`,
  - `no_label_computed`,
  - `no_signal_computed`,
  - `no_ml_trained`,
  - `no_strategy_created`,
  - `no_backtest_run`,
  - `no_network_io`,
  - `no_websocket`,
  - `no_credential_read`,
  - `no_env_read`,
  - `no_mcp_or_graphify`,
  - `research_eligible_after_is_false_for_derived_family`,
  - `no_successor_authorization`.

The Phase 4bm-D gate report file is `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v002__phase-4bm-d__1779056065059__57e1c97e6e93.json` with SHA256 `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` (paired `.sha256` sidecar SHA256 `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711`; canonical Phase 4bb-F format `<sha256_lowercase_hex>  <basename>\n`; matches verbatim). Both files are gitignored, not committed. The `code_commit_sha` recorded inside the report is the Phase 4bm-D implementation commit `57e1c97e6e938797d448b331cdc27b50b8e935dd`.

**Pre/post immutability evidence (Phase 4bm-D merge-closeout, §9, restated and re-verified locally by this memo):** the v002 raw manifest (`016967865c97…`), the v002 acquisition log (`52f6d7fb…`), the Phase 4bl-D-R raw multi-day gate report (`f9493fd1…`), the Phase 4bl-E raw successor-state JSON (`a0576ca6…`), the v002 derived multi-day index manifest (`01c5fa53…`), and the v002 derived sidecar (`d96f31ae…`) were byte-identical pre and post the Phase 4bm-D gate run. The 90 v002 raw zips and 90 v002 raw zip sidecars (Phase 4bl-C outputs) are unchanged. The 90 v002 per-day Parquets and 90 paired sidecars (Phase 4bm-B outputs) are unchanged. The Phase 4bd v001 single-day Parquet (`2b3d6978…`) and Phase 4bd v001 derived manifest (`f6f0d947…`) are unchanged. The pre-existing Phase 4bf v001 single-day derived gate report (`microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json`) is unchanged.

**Stage-2 verdict (multi-day v002):** evidence-positive at report level. The actual v002 derived multi-day index manifest's `eligibility_gate_status` remains `"pending"`; per the Phase 4bb-E / Phase 4bf precedent (preserved in Phase 4bm-D's design), the report-level PASS is governance evidence and does not by itself flip the manifest field.

---

## 9. Research-eligibility decision framework

The Phase 4ba 5-stage data-eligibility ladder (Stage-0 acquired → Stage-1 inspected → Stage-2 gate-passed → Stage-3 research-eligible → Stage-4 feature-cleared) defines the asymmetry that controls this decision:

- `research_eligible = true` is permitted **only at Stage-3 and only on the derived family** (never on the raw family);
- the raw family `microstructure_raw_aggtrades_v001` (both v001 and v002 versions) remains permanently `research_eligible = false`;
- Stage-3 is downstream of Stage-2 at the manifest level, and any machine-readable Stage-3 marker is recorded by a separately authorized successor-state recording phase (Phase 4bg-B precedent for v001; would be Phase 4bm-F for v002 if ever authorized);
- Stage-4 (feature-cleared) is downstream of Stage-3 and is required before any feature computation, ML training, strategy work, or backtest;
- every stage transition requires its own separately authorized phase.

The decision in this memo therefore distinguishes three orthogonal axes:

1. **Policy admissibility (multi-day v002):** does the project record contain enough evidence to consider Stage-3 admissible **in principle** at policy level for the multi-day v002 normalized derived family?
2. **Manifest mutation (multi-day v002):** should this phase mutate the actual v002 derived multi-day index manifest's `research_eligible` and `eligibility_gate_status` fields, or create any successor-state artefact for the v002 derived family?
3. **Practical research use (multi-day v002):** does Stage-3 (if admissible in principle) authorize feature computation, ML, strategy work, or backtests on the v002 derived family?

Phase 4bm-E is bounded to docs-only output. Axes 2 and 3 are categorically out of scope for this phase regardless of the answer to axis 1. Any "yes" on axis 1 is a recommendation for a future separately authorized phase, not a self-executing instruction.

---

## 10. Stage-3 admissibility criteria (multi-day v002)

To consider the multi-day v002 normalized derived family research-eligible **in principle at policy level**, the following 15 minimum criteria must hold (each must be verifiable from the project record). The criteria mirror the Phase 4bg-A v001 criteria, scaled to the multi-day v002 evidence chain.

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | v002 Stage-0 derived artefacts (90 per-day Parquets + 90 sidecars + v002 multi-day index manifest + v002 sidecar) exist locally and are reproducible from the 90 v002 raw archives plus the Phase 4bm-B normalizer (now on `main`). | satisfied |
| 2 | v002 derived multi-day index manifest exists and references the v002 raw lineage (v002 raw manifest SHA `016967865c97…`, v002 acquisition log SHA `52f6d7fb…`, Phase 4bl-D-R raw multi-day gate report SHA `f9493fd1…`, Phase 4bl-E raw successor-state SHA `a0576ca6…`). | satisfied |
| 3 | Phase 4bm-C multi-day structural QA passed 56 / 56 (read-only) over the v002 derived family. | satisfied |
| 4 | Phase 4bm-D multi-day derived-family eligibility gate passed 60 / 60 against the v002 derived family with `gate_verdict = DERIVED_GATE_PASS`. | satisfied |
| 5 | Phase 4bm-D authoritative gate report SHA256 is recorded and available locally: `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a`; paired sidecar SHA256 `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711`. | satisfied (recomputed on disk in this memo) |
| 6 | v002 derived multi-day index manifest currently remains `research_eligible = false` and `eligibility_gate_status = "pending"`. | satisfied (verified on disk) |
| 7 | v002 raw manifest currently remains `research_eligible = false` and `eligibility_gate_status = "pending"`. | satisfied (verified on disk) |
| 8 | Raw family `microstructure_raw_aggtrades_v001` (both v001 and v002 versions) remains permanently ineligible for research use. | satisfied (Phase 4bb-E policy; Phase 4bl-E successor-state recording of the v002 raw side) |
| 9 | Invalid windows are empty or explicitly governed across all 90 v002 derived days. | satisfied (Phase 4bm-D reports zero invalid-window candidates over the 90 days; per-day `invalid_windows = []` propagated from the v002 raw side) |
| 10 | No features, labels, signals, proxies, ML, strategy, or backtest artefacts derived from the v002 family exist. | satisfied (no feature kernel run; no label kernel run; no `data/microstructure/features/` namespace exists for v002; no `data/microstructure/labels/` artefact exists for v002) |
| 11 | No project lock would be loosened by a future v002 Stage-3 transition. | satisfied (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0, Phase 4al, Phase 4aw, Phase 4bb-F, Phase 4bl-F all unaffected) |
| 12 | No retained verdict would be revised by a future v002 Stage-3 transition. | satisfied (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure all unaffected) |
| 13 | M0 remains binding prospectively for any future strategy hypothesis that ever consumes v002 microstructure evidence. | satisfied (Phase 4ak adoption preserved; microstructure / order-flow / liquidity-timing lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption) |
| 14 | Stage-4 feature-boundary design is still required before any feature computation on v002. | satisfied (Stage-4 not authorized; Phase 4bh-A / 4bh-B v001 feature-boundary design memos are v001-only and do not extend to v002 without a separately authorized multi-day analogue) |
| 15 | Any machine-readable manifest transition for the v002 derived family requires a separately authorized successor-state recording phase. | satisfied (Phase 4bb-E policy preserved; Phase 4bg-B v001 successor-state precedent applies pattern-only — the v002 case requires its own separately authorized Phase 4bm-F if and when the operator chooses to proceed) |

**All 15 admissibility criteria are satisfied at the policy level for the multi-day v002 normalized derived family.**

---

## 11. Evidence-to-criteria mapping

| Criterion | Evidence source | Specific record |
| --------- | --------------- | --------------- |
| 1 | Phase 4bm-B implementation report; Phase 4bm-B merge-closeout; Phase 4bm-D merge-closeout §9 | 90 v002 per-day Parquets + 90 sidecars + v002 index manifest `01c5fa53…` + v002 sidecar `d96f31ae…`; gitignored under `.gitignore:85` |
| 2 | v002 derived multi-day index manifest `governance_labels` (read by Phase 4bm-D check suite check group 4bm-d.X) | v002 raw manifest SHA `016967865c97…`; Phase 4bl-D-R gate report SHA `f9493fd1…`; Phase 4bl-E successor-state SHA `a0576ca6…`; Phase 4bm-A `dataset_version=v002` predeclared; `feature_computation=forbidden`; `strategy_use=forbidden` |
| 3 | Phase 4bm-C memo + closeout + merge-closeout | 56 / 56 PASS, 0 FAIL, 0 ERROR, 0 NOT_APPLICABLE across the 90 v002 days |
| 4 | Phase 4bm-D implementation report + closeout + merge-closeout §6 / §8 / §11 | 60 / 60 PASS; `gate_verdict = DERIVED_GATE_PASS`; check IDs `4bm-d.X.Y` per the Phase 4bm-D check catalogue (60 checks total spread across the v001-equivalent groups extended by the 5 multi-day-specific groups) |
| 5 | Phase 4bm-D real-run record; Phase 4bm-D merge-closeout §7 / §8; recomputed locally in this memo's §2 | gate report SHA256 `3b45e70b…`; sidecar SHA256 `8e74261c…`; both files gitignored under `.gitignore:85` |
| 6 | live filesystem status of `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` (gitignored locally) read in this memo's §2 | `research_eligible=false`, `eligibility_gate_status=pending` |
| 7 | live filesystem status of `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json` (gitignored locally) read in this memo's §2 | `research_eligible=false`, `eligibility_gate_status=pending` |
| 8 | Phase 4bb-E §"Headline policy conclusions"; Phase 4bl-E multi-day raw successor-state recording (gitignored successor-state JSON SHA `a0576ca6…`) | raw-family `research_eligible=false` permanent (v001 and v002) |
| 9 | Phase 4bm-D real-run summary; Phase 4bm-D merge-closeout §6; Phase 4bm-D check suite (invalid-window subgroup) | per-day `invalid_windows = []` propagated from v002 raw side; 0 multi-day invalid-window candidates |
| 10 | Phase 4bm-A scope; Phase 4bm-B implementation; Phase 4bm-C schema check; Phase 4bm-D feature-absence subgroup; live filesystem walk under `data/microstructure/features/` and `data/microstructure/labels/` (no v002 feature / label artefacts exist) | no feature / label / signal / proxy column anywhere in v002; no v002 feature parquet; no v002 label parquet |
| 11 | Project locks listed in `current-project-state.md` and the Phase 4bm-D / Phase 4bm-D-P1 merge-closeouts | §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0, Phase 4al, Phase 4aw, Phase 4bb-F, Phase 4bl-F all preserved |
| 12 | Retained verdict ledger | H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure unchanged |
| 13 | Phase 4ak M0 governance adoption | M0 binding prospectively; post-null cooldown rule binding; microstructure / order-flow / liquidity-timing lane remains `NOT_RECOMMENDED_NOW` |
| 14 | Phase 4ba ladder; Phase 4bh-A / 4bh-B v001 design memos (v001-only) | Stage-4 feature-cleared not yet reachable for v002; not authorized; v001 feature-boundary design does not transitively authorize v002 |
| 15 | Phase 4bb-E policy; Phase 4bg-B v001 successor-state recording precedent | sibling successor-state manifest required for any machine-readable transition on v002; the v002 successor-state phase would be Phase 4bm-F (not authorized) |

---

## 12. What additional evidence does v002 carry that v001 did not?

The Phase 4bg-A v001 decision was based on a single-day single-symbol artefact (BTCUSDT 2025-01-15; 1,681,098 events). The v002 evidence chain materially strengthens the underlying artefact integrity story along several dimensions while leaving the cross-symbol gap unchanged:

| Dimension | v001 (Phase 4bg-A) | v002 (this memo) | Delta |
| --------- | ------------------ | ----------------- | ----- |
| Symbol coverage | BTCUSDT (one symbol) | BTCUSDT (one symbol) | unchanged — no cross-symbol robustness gained |
| Date coverage | 1 UTC day (2025-01-15) | 90 contiguous UTC days (2024-12-01 .. 2025-02-28) | **+89 days** — multi-day robustness materially gained |
| Event count | 1,681,098 events | 155,153,449 events | **~92× scale-up** |
| Raw-gate scope | Phase 4bb-D single-day 45 / 45 PASS | Phase 4bl-D-R multi-day `RAW_MULTIDAY_GATE_PASS` (covering all 90 raw zips + 90 sidecars + raw manifest + acquisition log) | multi-day raw integrity established |
| Raw successor-state | Phase 4bb-E policy only (no v001 raw successor-state JSON) | Phase 4bl-E raw successor-state JSON recorded (gitignored SHA `a0576ca6…`) | raw-side machine-readable boundary recorded |
| Structural QA scope | Phase 4be single-day 60 / 60 PASS | Phase 4bm-C multi-day 56 / 56 PASS over 90 days | structural QA scaled cleanly to 90 days |
| Derived-gate scope | Phase 4bf single-day 55 / 55 PASS | Phase 4bm-D multi-day 60 / 60 PASS (5 additional multi-day-specific check groups) | derived gate scaled cleanly to 90 days with additional multi-day invariants |
| Boundary confirmations | 15 / 15 `True` (Phase 4bf) | **19 / 19 `True`** (Phase 4bm-D adds `no_per_file_parquet_mutation`, `no_per_file_sidecar_mutation`, `no_raw_zip_mutation`, and the multi-day analogue of `no_normalization_written_outside_namespace`) | broader mutation-class evidence |
| Days with non-empty `invalid_windows` | 0 / 1 | **0 / 90** | multi-day invalid-window negative confirmation |
| Phase 4ba ladder Stages reached | Stage-0 ✓, Stage-1 ✓, Stage-2 ✓ (report-level) | Stage-0 ✓, Stage-1 ✓, Stage-2 ✓ (report-level) | parity; Stage-3 manifest-level still requires a separately authorized successor-state phase |

Phase 4bm-D therefore strengthens the *artefact-integrity* evidence base for the derived family while not changing the *cross-symbol* evidence gap. The multi-day v002 evidence is strictly broader and stronger than the single-day v001 evidence along every dimension that v002 measured; nothing the v002 chain measured was weaker than v001.

The remaining open scientific questions (cross-symbol robustness; feature design; label design; leakage controls; ML split design; strategy hypothesis under M0; costed backtest; live / paper / shadow readiness) are unchanged from Phase 4bg-A — they belong to later separately authorized governance phases, not to this policy-level admissibility decision.

---

## 13. Remaining risks and limitations

The 15 admissibility criteria address artefact integrity and governance bookkeeping. They do **not** address statistical sufficiency for strategy research. The following limitations remain after Phase 4bm-E (most are unchanged from Phase 4bg-A; the date-coverage limitation is materially reduced but not eliminated):

- **Symbol scope is one symbol** (BTCUSDT only). No cross-symbol coverage exists in v002.
- **Date scope is 90 contiguous UTC days** (2024-12-01 .. 2025-02-28). 90 days is meaningfully better than the 1-day v001 sample but is still a bounded window. No multi-quarter or multi-year coverage exists yet.
- **Day-type distribution within the 90 days is not yet diagnosed.** The memo records no claim about whether the 90 days are dominated by quiet vs volatile sessions, trend vs range regimes, or any other regime classification. Any future research framing must carry this disclaim.
- **Research eligibility of the v002 artefact is not the same as statistical sufficiency** for any specific research question.
- **No multi-day robustness analysis has been performed** beyond structural QA and the eligibility gate. The Phase 4bm-C / 4bm-D evidence is integrity-shaped, not distribution-shaped.
- **No cross-symbol robustness exists.** A one-symbol sample cannot generalize.
- **No feature set is authorized on v002** (Stage-4 not authorized; Phase 4bh-A / 4bh-B feature-boundary designs are v001-only).
- **No label design exists for v002** (no future-return scheme has been predeclared for the v002 family; Phase 4bj-A / 4bj-B / 4bj-C label work is v001-only).
- **No leakage control design exists for v002** (no temporal-leakage barrier has been specified for future feature work on v002).
- **No ML split design exists for v002** (no train / validation / OOS partitioning policy has been authored for v002 microstructure-driven research; Phase 4bj-H / 4bj-I / 4bj-J chronological-split policy memos are v001-only).
- **No strategy hypothesis exists under the Phase 4ak M0 admissibility gate** that would consume the v002 dataset.
- **No costed backtest exists** for any microstructure-driven hypothesis (the §11.6 8 bps cost lock applies regardless).
- **No live / paper / shadow readiness exists.** None is approached by Stage-3 admissibility.
- **Stage-3, if recommended, only permits governed research use of the clean v002 artefact.** It does not license any claim of edge.

These limitations are not blockers to a policy-level Stage-3 admissibility decision for v002. They are explicit constraints on what such a decision means.

---

## 14. Invalid-window status (multi-day v002)

`invalid_windows` for every per-day Parquet in the v002 derived family: `[]`.
`invalid_windows` for the v002 raw manifest (and all 90 per-day raw entries): `[]`.
`invalid_windows` for the v001 derived manifest (single-day; unchanged): `[]`.
`invalid_windows` for the v001 raw manifest (single-day; unchanged): `[]`.

Phase 4bm-D real-run produced zero invalid-window candidates across the 90 v002 days. No invalid windows are governed-but-excluded; none exist for the v002 archive set.

If any future v002 extension acquisition produces non-empty invalid windows, those windows must be enumerated explicitly in the affected manifest, governed by the Phase 3r §8 / Phase 4j §11 precedent (and the Phase 4bm-A / Phase 4bm-B multi-day propagation pattern), and propagated by the Phase 4bm-B normalizer's invalid-window helper. **Phase 4bm-E does not amend invalid-window governance.**

---

## 15. Raw-family policy (multi-day v002)

Per Phase 4bb-E (raw v001) and Phase 4bl-E (raw v002):

- the raw family `microstructure_raw_aggtrades_v001` is **permanently** `research_eligible = false` across both versions (v001 single-day and v002 multi-day);
- the original Phase 4az raw v001 manifest is **immutable**;
- the original Phase 4bl-C raw v002 manifest is **immutable**;
- raw-family gate PASS reports (Phase 4bb-D for v001, Phase 4bl-D-R for v002) are report-level governance evidence, not manifest mutations;
- the Phase 4bl-E v002 raw successor-state JSON records a *sibling* successor-state marker preserving the original v002 raw manifest byte-identically and preserving raw `research_eligible = false`.

**Phase 4bm-E does not amend the raw-family policy.** The raw family remains permanently `research_eligible = false` across both v001 and v002. No raw-side modification is implied or authorized.

---

## 16. Derived-family manifest policy (multi-day v002)

For the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`):

- the actual v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` **must remain unchanged in Phase 4bm-E**;
- Phase 4bm-E does not flip `research_eligible`; the field remains `false`;
- Phase 4bm-E does not transition `eligibility_gate_status`; the field remains `"pending"`;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains in place;
- any machine-readable transition of these fields (whether on the original v002 derived multi-day index manifest, a successor-state sibling, a per-day successor record, or an external registry) requires a separately authorized successor-state recording phase (the multi-day analogue of Phase 4bg-B; if ever authorized, that phase would be **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording**).

If a future Phase 4bm-F is separately authorized, that phase would specify the exact record format (sibling successor-state manifest preserving the original byte-identically vs. a per-day successor-state array vs. an external registry vs. a new pinned `v003`), and it would still not authorize feature computation, ML, strategy, or backtests on v002. Phase 4bm-F is **not** authorized by Phase 4bm-E.

The v001 derived manifest (Phase 4bd output) also remains unchanged; the Phase 4bg-B v001 successor-state JSON SHA `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` continues to be the only Stage-3 machine-readable marker for v001, and it explicitly does not transitively cover v002.

---

## 17. Feature-boundary policy (multi-day v002)

Stage-4 (feature-cleared) is **not** authorized by Phase 4bm-E for v002 and is not implied by any policy-level Stage-3 admissibility decision in this memo.

The Phase 4bh-A v001 Feature-Boundary Design Memo and the Phase 4bh-B v001 Feature Schema Finalization Memo are v001-specific: they cite the Phase 4bd v001 normalized Parquet SHA, the Phase 4bg-B v001 successor-state JSON SHA, and Phase 4bf gate report SHA verbatim, and they predeclare a v001-only future feature family `microstructure_features_aggtrades_v001` (`v001` version). Those v001 feature-boundary memos do **not** transitively cover v002. Any feature work that ever consumes v002 microstructure evidence requires a separately authorized multi-day analogue (a future Phase 4bm-H-A or equivalent, not authorized).

Specifically, the following remain forbidden until a separately authorized multi-day v002 feature-boundary design memo and a separately authorized v002 feature implementation phase:

- computing returns, alpha, edge, opportunity rate on v002;
- computing taker imbalance, sweep detection, aggressive-flow score on v002;
- computing spread, depth, liquidity, slippage, order-flow, execution-quality proxies on v002;
- computing regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position-state columns on v002;
- creating any column outside the 19-column Phase 4bc / Phase 4bm-A canonical normalized schema in the v002 derived family;
- creating any sibling derived family that contains feature columns and consumes v002 inputs;
- writing any feature, label, signal, or proxy under `data/microstructure/features/` or `data/microstructure/labels/` that consumes v002 inputs;
- writing JSONL, DuckDB, feature tables, labels, signals, or analytical datasets that are derived from the v002 artefact.

The feature-boundary policy is downstream governance. Phase 4bm-E only confirms it is the next governance step that must precede any feature computation on v002 if the project ever proceeds further on this lane.

---

## 18. ML / strategy boundary (multi-day v002)

Phase 4bm-E does **not** authorize:

- creating ML models that consume v002;
- training ML on the multi-day v002 derived family;
- creating any strategy candidate (named or otherwise) that consumes v002;
- creating any hypothesis-spec memo, strategy-spec memo, backtest-plan memo, or backtest-execution phase that consumes v002;
- running any backtest;
- running any simulation that uses v002 as input;
- running any paper / shadow / live / exchange-write workflow.

The Phase 4ak M0 admissibility gate (twelve clauses) and the post-null cooldown rule remain binding for any future strategy hypothesis. M0.7 (edge-rate plausibility separate from opportunity-rate) and M0.10 (forbidden-rescue / anti-reduction check with named closest rescue trap) are particularly binding for any microstructure-driven candidate.

Cooled-down families (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane) remain cooled down. Phase 4bm-E neither reopens nor amends any cooled-down family classification.

---

## 19. Research-use permission boundary (multi-day v002)

Even at policy-level Stage-3 (in principle), "research use" of v002 is bounded:

- governed offline inspection of the 90 v002 per-day Parquets for descriptive understanding of the dataset itself (per-day row distributions, agg-trade-id ranges, timestamp coverage, multi-day continuity) is allowed;
- writing those inspection results into a future docs-only memo, with cited SHAs, is allowed;
- producing any derivative dataset, feature, label, signal, proxy, return, or backtest from the v002 artefact is **not** allowed under Phase 4bm-E;
- producing any derivative that would imply a strategy claim is **not** allowed under Phase 4bm-E;
- producing any derivative dataset that would carry `feature_computation` or `strategy_use` outside `forbidden` is **not** allowed under Phase 4bm-E.

This boundary mirrors the Phase 4bb-A (raw structural QA), Phase 4bm-C (multi-day Stage-1 structural QA), and Phase 4bm-D (multi-day Stage-2 gate execution) precedents — each of which inspected the artefact and produced docs without computing features.

---

## 20. Decision options considered

| Option | Description | Evaluation |
| ------ | ----------- | ---------- |
| A | Do not authorize Stage-3 admissibility for v002 even in principle yet; require more evidence (cross-symbol, multi-quarter, additional acquisition) first. | Defensible but conservative beyond the evidence. The 15 admissibility criteria are satisfied at the policy level. The remaining open questions (cross-symbol robustness; feature design; label design; leakage controls; ML split; strategy hypothesis under M0; costed backtest) belong to *later* governance phases (a separately authorized multi-day feature-boundary design memo and/or further acquisition phases), not to a policy-level Stage-3 admissibility decision. Choosing A would be an under-recognition of the available evidence and would also be inconsistent with the Phase 4bg-A v001 precedent (which chose B on strictly weaker single-day evidence). |
| B | Authorize Stage-3 admissibility **in principle at policy level** for the multi-day v002 derived family, but do not mutate the manifest in this phase; require a separately authorized successor-state recording phase (Phase 4bm-F) before any machine-readable `research_eligible` transition. | Matches the Phase 4ba ladder, the Phase 4bb-E successor-state policy, the Phase 4bg-A v001 precedent verbatim, and the Phase 4bm-E non-scope. Records a precise governance position without overstepping. **Selected.** |
| C | Authorize a limited, docs-only research-use policy on v002 while keeping the v002 manifest false; require Stage-4 feature-boundary design before any feature computation. | Functionally consistent with B (which already implies the Stage-4 prerequisite). C is admissible as a wording variant; B is more precise about the manifest boundary, so B is preferred (consistent with Phase 4bg-A's reasoning). |
| D | Reject immediate v002 Stage-3 and proceed instead to additional acquisition planning (cross-symbol, multi-quarter). | Out of scope: Phase 4bm-E is not an acquisition phase. Any acquisition would require a separately authorized acquisition memo. Additional acquisition does not invalidate the existing v002 evidence and is not a prerequisite for *policy-level* Stage-3 admissibility — it is a prerequisite for broader scientific applicability, which is a different question. |
| E | Mutate the v002 derived multi-day index manifest now (flip `research_eligible` to `true` and/or transition `eligibility_gate_status` from `"pending"` to `"pass"` on disk). | **Forbidden.** Phase 4bm-E is docs-only. Mutation requires a separately authorized successor-state recording phase (Phase 4bm-F, not authorized). The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains in force and would refuse any direct mutation attempt; the multi-day index manifest is a sibling shape but the policy intent is identical. |

---

## 21. Recommended decision

**Option B.** Decision form 2 wording (the Phase 4bg-A v001 wording, scaled to v002):

> **Stage-3 is admissible in principle at policy level for the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`; 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 events), but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase (Phase 4bm-F) is required before any machine-readable `research_eligible = true` marker exists for the v002 derived family.**

Specifically:

- the **raw family `microstructure_raw_aggtrades_v001` remains `research_eligible = false` permanently** across both v001 and v002 versions (Phase 4bb-E + Phase 4bl-E preserved verbatim);
- the **actual v002 derived multi-day index manifest remains `research_eligible = false`** in Phase 4bm-E, and the **actual `eligibility_gate_status` remains `"pending"`** on disk;
- the **actual v002 raw manifest remains `research_eligible = false` and `eligibility_gate_status = "pending"`** on disk (untouched);
- the **actual v001 derived manifest remains `research_eligible = false` and `eligibility_gate_status = "pending"`** on disk (untouched; Phase 4bg-B v001 successor-state JSON remains the only v001 machine-readable Stage-3 marker);
- **no data, feature, label, ML, strategy, or backtest work on v002 is authorized** by Phase 4bm-E;
- **the next safe phase is one of: a multi-day successor-state policy / recording memo (a future Phase 4bm-F), or a multi-day feature-boundary design memo (a future Phase 4bm-H-A or equivalent), or remain paused**; no immediate feature computation on v002 is authorized;
- this admissibility is policy-level only and bounded by the Phase 4ba ladder; Stage-4 (feature-cleared) remains unauthorized for v002 and Stage-4 admissibility is not predetermined by Phase 4bm-E.

The Phase 4ak M0 admissibility gate, post-null cooldown rule, cooled-down families list, refined no-rescue rule (Phase 4al §13 / §14), the Phase 4aw `flip_research_eligible(...)` always-raises invariant, the Phase 4bb-F canonical path policy, the Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, the Phase 4bm-A-P1 thin-prompt context-management standard, and the Phase 4bm-D-P1 lightweight Claude Code workspace standard all remain binding.

---

## 22. Exact authority path required before any future v002 manifest mutation

Before any tracked or on-disk change to `research_eligible` or `eligibility_gate_status` on the v002 derived multi-day index manifest, the following authority steps must occur **in order**:

1. **Operator review of this memo** in ChatGPT (Phase 4bm-E review step per the Phase 4bk-A / Phase 4bm-A-P1 / Phase 4bm-D-P1 workflow standards).
2. **Operator-authored merge prompt** to merge this branch into `main` per `merge-closeout-standard.md` (a Tier 1 16-section merge-closeout for Phase 4bm-E).
3. **Phase 4bm-E merge-closeout on `main`** recording this memo as project-complete (Phase 4bm-E becomes project-complete only at this step).
4. **Operator post-merge plain-English summary** in ChatGPT (Phase 4bm-E step 9 per `phase-workflow-standard.md`).
5. **Operator-authored authorization prompt for Phase 4bm-F** — a separately authorized successor-state recording phase that names exactly Phase 4bm-F, the v002 derived multi-day index manifest, the exact successor-state JSON format (sibling artefact preserving the original byte-identically vs. per-day successor-state array; the operator chooses the form), the allowed tracked files, the allowed local gitignored outputs under `data/microstructure/successor-state/`, the strict non-scope, the validation commands, and the fail-closed conditions.
6. **Phase 4bm-F branch execution** by Claude Code: writes the v002 successor-state JSON + paired Phase 4bb-F sidecar under `data/microstructure/successor-state/` (gitignored; not committed); preserves the original v002 derived multi-day index manifest byte-identically; preserves the original v002 raw manifest byte-identically; preserves every other `data/microstructure/` artefact byte-identically; preserves the Phase 4aw always-raises invariant (never invoked); records pre/post SHAs.
7. **Phase 4bm-F implementation report + closeout** on the branch.
8. **Operator review** of Phase 4bm-F branch.
9. **Phase 4bm-F merge prompt** to merge into `main`.
10. **Phase 4bm-F merge-closeout on `main`** recording the successor-state JSON SHA verbatim as the v002 Stage-3 machine-readable marker.

Only after step 10 does any machine-readable Stage-3 marker exist for v002. Even then, the **actual on-disk v002 derived multi-day index manifest still carries `research_eligible = false` / `eligibility_gate_status = "pending"`**; the Stage-3 marker lives only in the sibling successor-state JSON (the Phase 4bg-B v001 pattern; the original manifest is preserved byte-identically). Phase 4aw's `flip_research_eligible(...)` always-raises invariant is preserved end-to-end and is never invoked.

Any deviation from this authority path is forbidden. In particular:

- Phase 4bm-E does not authorize Phase 4bm-F.
- Phase 4bm-E does not collapse Phase 4bm-F and any feature-boundary phase into one phase.
- Phase 4bm-E does not authorize feature computation, ML, strategy, or backtest on v002 even after a hypothetical Phase 4bm-F merge-closeout.

---

## 23. Recommended successor phase

The recommended successor phase is **none — remain paused**. The operator may, at their discretion and on their own timeline, separately authorize:

- **Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording** (docs + local gitignored sibling successor-state JSON; would record a single v002 successor-state JSON marker + paired SHA256 sidecar under `data/microstructure/successor-state/`; would preserve the original v002 derived multi-day index manifest byte-identically; would preserve the original v002 raw manifest byte-identically; would not authorize feature computation, ML, strategy, or backtest). This is the natural multi-day analogue of Phase 4bg-B for v001. **Phase 4bm-F is NOT authorized by this memo.**

- **A future multi-day feature-boundary design memo** (e.g. Phase 4bm-H-A; docs-only; would extend the Phase 4bh-A / Phase 4bh-B v001 feature-boundary design to v002 inputs; would predeclare future v002-specific feature schema, lineage SHAs including the Phase 4bm-F successor-state JSON SHA, manifest, governance labels, and 17+ fail-closed rules; would not authorize feature computation). This memo is **NOT authorized** by Phase 4bm-E and would not be reachable until Phase 4bm-F is project-complete on `main`.

- **Remain paused.** The default Prometheus recommendation after every merge-closeout is *remain paused*. Phase 4bm-E does not change that default.

---

## 24. What remains forbidden after Phase 4bm-E

Phase 4bm-E does not, and cannot, be construed as authorising:

- any change to the v002 derived multi-day index manifest's `research_eligible` field (remains `false` on disk);
- any change to the v002 derived multi-day index manifest's `eligibility_gate_status` field (remains `"pending"` on disk);
- any change to the v002 derived multi-day index manifest's `chronological_split_policy` field (the v002 manifest does not yet carry a chronological-split-policy field; any future addition requires a separately authorized phase under the Phase 4bj-I / 4bj-J chronological-split-policy precedent extended to v002);
- any change to the v002 raw manifest, v002 raw zips, v002 acquisition log, Phase 4bl-D-R raw multi-day gate report, Phase 4bl-E raw successor-state JSON, or Phase 4bm-D authoritative gate report;
- any change to the v001 derived manifest, v001 normalized Parquet, v001 raw manifest, v001 raw zip, v001 acquisition log, Phase 4bb-D v001 raw gate report, Phase 4bf v001 derived gate report, or Phase 4bg-B v001 successor-state JSON;
- any creation of a v002 successor-state JSON (only Phase 4bm-F, if separately authorized, may create that artefact);
- any rerun of the Phase 4bm-D gate, the Phase 4bm-C structural QA, the Phase 4bm-B normalizer, the Phase 4bl-D-R raw gate, or any other prior gate / normalizer / QA;
- any new acquisition (no extension beyond the 90 locked v002 dates; no cross-symbol acquisition; no 5m / 1m / tick / mark-price 30m / 4h / order-book / liquidation / funding / open-interest / cross-venue acquisition);
- any feature computation on v002 (or on v001);
- any label computation on v002;
- any diagnostics rerun (Phase 3s Q1–Q7 closure preserved);
- any ML training, model selection, feature ranking, or meta-labeling on v002 (or on v001);
- any strategy creation, signal computation, or backtest implementation that consumes v002 (or v001);
- any paper / shadow, live-readiness, deployment, exchange-write, production-key creation, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- any MCP, Graphify, `.mcp.json`, or credential work;
- any modification of source code, tests, scripts, configuration, `.gitignore`, `pyproject.toml`, `README.md`, `.claude/settings.json`, `.claude/settings.local.json`, `.claude/hooks/`, or `.claude/agents/`;
- any revision of any retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure all preserved verbatim);
- any change to any project lock (§11.6, round-trip = 16 bps, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy);
- any amendment to the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- any amendment to the Phase 4bb-F canonical path policy;
- any amendment to the Phase 4bl-F four-tier risk model, R-SIDECAR-CRLF standing rule, or nine reusable non-authorization blocks;
- any amendment to the Phase 4bm-A-P1 thin-prompt Claude Code context-management standard;
- any amendment to the Phase 4bm-D-P1 lightweight Claude Code workspace execution standard;
- any reopening of cooled-down families (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane);
- any cross-strategy hybrid (V1-D1, F1-D1, V2-G1, G1-C1, or any other combination);
- any -prime, -narrow, -extension, or -hybrid variant of any historical candidate;
- any reopening of the 5m research thread (Phase 3t closure preserved);
- any use of Phase 4l V2 forensic numbers, Phase 4r G1 forensic numbers, or Phase 4x C1 forensic numbers as parameter-selection inputs;
- any use of Phase 3s Q1–Q7 diagnostic outputs as rule-input candidates;
- copying Prometheus agent packs or agent memory into `C:\ClaudeRuns\prometheus-light` (Phase 4bm-D-P1 default preserved);
- enabling agents-by-default for heavy execution sessions;
- committing any file under `data/microstructure/`.

---

## 25. What project state should remain after Phase 4bm-E

After Phase 4bm-E (post-merge-closeout):

- `main` advances by exactly three docs files: this memo, the Phase 4bm-E closeout, and a narrow `current-project-state.md` update; plus one further docs file in the Phase 4bm-E merge-closeout commit (Phase 4bm-E merge-closeout report) if and when a separately authorized merge phase occurs.
- No file under `src/prometheus/`, `tests/`, `scripts/`, `data/`, `.claude/`, or any non-`docs/` location changes.
- The v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` remains `research_eligible = false`, `eligibility_gate_status = "pending"`, SHA256 `01c5fa53…` byte-identical.
- The v002 raw manifest remains `research_eligible = false`, `eligibility_gate_status = "pending"`, SHA256 `01696786…` byte-identical.
- The v001 derived manifest remains `research_eligible = false`, `eligibility_gate_status = "pending"`, SHA256 `f6f0d947…` byte-identical.
- The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, 90 v002 raw zip sidecars, v002 acquisition log, Phase 4bl-D-R gate report and sidecar, Phase 4bl-E raw successor-state JSON and sidecar, Phase 4bm-D gate report (`3b45e70b…`) and sidecar (`8e74261c…`), v001 derived Parquet (`2b3d6978…`), Phase 4bf v001 derived gate report (`dd4e0c1c…`), Phase 4bg-B v001 successor-state JSON (`8bcc7d01…`), Phase 4bh v001 feature parquet and manifest (if present locally), Phase 4bj-C v001 label parquet and manifest (if present locally) all remain byte-identical.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains in place (never invoked).
- The retained verdict ledger (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread closure) is preserved verbatim.
- Every project lock (§11.6, round-trip, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w, Phase 4ak M0 + post-null cooldown + cooled-down families list + memo template, Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, Phase 4aw, Phase 4bb-F, Phase 4bl-F, Phase 4bm-A-P1, Phase 4bm-D-P1) is preserved verbatim.
- The recommended state is **remain paused** unless and until the operator separately authorizes Phase 4bm-F or another successor.

---

## 26. Fail-closed rules

The following are binding on any future phase that consumes Phase 4bm-E as input:

1. **Path discipline.** No write may occur outside `data/microstructure/`. The Phase 4bm-B per-day Parquet paths, the v002 derived multi-day index manifest path, the v002 raw manifest path, the Phase 4bl-D-R gate report path, the Phase 4bl-E successor-state path, and the Phase 4bm-D gate report path must remain byte-immutable unless a separately authorized phase reproduces the artefact deterministically with documented evidence (Phase 4bb-F canonical path policy preserved).
2. **Manifest-mutation discipline.** The original v002 derived multi-day index manifest, the original v002 raw manifest, and the v001 single-day manifests must not be mutated. Any successor state for v002 must be recorded in a sibling artefact preserving the original byte-identically (the Phase 4bg-B v001 pattern, applied to v002 if and when Phase 4bm-F is separately authorized).
3. **Raw-family discipline.** The raw family `microstructure_raw_aggtrades_v001` remains `research_eligible = false` permanently across both v001 and v002. No phase may flip it.
4. **Stage-3 discipline (v002).** Stage-3 admissibility at policy level for v002 is *not* a license for feature computation, ML, strategy, or backtests on v002. Stage-4 authorization is required for those.
5. **Stage-4 discipline (v002).** Stage-4 authorization is not implied by Stage-3 admissibility. A separately authorized multi-day feature-boundary memo is required before Stage-4 even becomes a candidate for v002. The Phase 4bh-A / Phase 4bh-B v001 feature-boundary designs do not transitively cover v002.
6. **Network discipline.** No phase consuming Phase 4bm-E as input may call public endpoints, Binance APIs, authenticated REST, private endpoints, user stream, WebSocket, or read `.env` / credentials / `.mcp.json` without separately authorized scope.
7. **Static-import discipline.** The Phase 4bm-D static-scan policy on `multiday_derived_gate_*` modules and the Phase 4bf static-scan policy on `derived_gate_*` modules continue. Future microstructure modules must remain free of forbidden imports and tokens.
8. **Cooldown discipline.** Post-null cooldown classifications for cooled-down families are not loosened by any policy-level Stage-3 admissibility decision in this memo.
9. **Cost-realism discipline.** §11.6 = 8 bps per side and round-trip = 16 bps remain binding for any future strategy candidate that ever consumes v002 microstructure-derived features.
10. **No-rescue discipline.** Phase 4al refined no-rescue rule remains binding. No retained verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1) may be revisited, rescued, or relabelled on the basis of Phase 4bm-E.
11. **Tier discipline (Phase 4bl-F).** Phase 4bm-E is itself a Tier 1 docs-only governance phase. Any future v002 successor-state recording phase (Phase 4bm-F) is Tier 1. Any future v002 feature-boundary design memo is Tier 1. None of these may be batched or collapsed.
12. **Thin-prompt discipline (Phase 4bm-A-P1).** Any future v002 successor or feature-boundary authorization prompt must follow the Phase 4bm-A-P1 thin-prompt context-management standard.
13. **Lightweight-workspace discipline (Phase 4bm-D-P1).** Any future heavy-execution Claude Code session that consumes v002 inputs must launch from the lightweight workspace at `C:\ClaudeRuns\prometheus-light` and access `C:\Prometheus` explicitly per the Phase 4bm-D-P1 standard.

---

## 27. What this phase proves

- that the project record contains enough evidence to consider Stage-3 admissibility **in principle at policy level** for the multi-day v002 normalized derived family `microstructure_normalized_aggtrades_v001` (`dataset_version = v002`);
- that the 15 minimum admissibility criteria are satisfied at the policy level for v002;
- that the v002 evidence chain is strictly broader and stronger than the v001 evidence chain along every dimension v002 measured (90 days vs. 1 day; 155,153,449 events vs. 1,681,098 events; 19 / 19 boundary confirmations vs. 15 / 15; multi-day raw integrity established by Phase 4bl-D-R; raw successor-state recorded by Phase 4bl-E);
- that the actual v002 derived multi-day index manifest remains `research_eligible = false` and `eligibility_gate_status = "pending"` throughout Phase 4bm-E;
- that the v002 raw manifest remains `research_eligible = false` and `eligibility_gate_status = "pending"` throughout Phase 4bm-E;
- that the v001 derived and v001 raw manifests remain unchanged throughout Phase 4bm-E;
- that the raw family `microstructure_raw_aggtrades_v001` remains `research_eligible = false` permanently across both v001 and v002;
- that no manifest, dataset, gate report, sidecar, successor-state JSON, or governance memo was mutated by Phase 4bm-E;
- that no successor phase is authorized.

---

## 28. What this phase does not prove

- that the v002 artefact is statistically sufficient for any specific research question;
- that any feature, label, signal, or proxy is admissible on v002;
- that Stage-4 is admissible for v002, in principle or otherwise;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible.

---

## 29. Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B / 4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-F / 4bj-G / 4bj-H / 4bj-I / 4bj-J / 4bj-K / 4bk-A / 4bl-A / 4bl-B / 4bl-C / 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R / 4bl-E / 4bl-F / 4bm-A / 4bm-A-P1 / 4bm-B / 4bm-C / 4bm-D / 4bm-D-P1 results — all preserved verbatim.

---

## 30. Recommended future options

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | recommended |
| **Conditional next, if continuing on the v002 lifecycle ladder** — Phase 4bm-F Multi-Day Derived-Family Successor-State Recording (multi-day analogue of Phase 4bg-B) | docs + local gitignored successor-state JSON; no feature computation; no manifest mutation; preserves original v002 derived multi-day index manifest byte-identically | **NOT authorized by this memo** |
| **Conditional later, if keeping manifests false but preparing v002 research** — a future multi-day feature-boundary design memo (e.g. Phase 4bm-H-A or equivalent; multi-day analogue of Phase 4bh-A / Phase 4bh-B) | docs-only; no computation | **NOT authorized by this memo** |
| **Conditional later still** — a future multi-day v002 feature schema / feature computation implementation (e.g. Phase 4bm-H or equivalent; multi-day analogue of Phase 4bh) | code + docs; only after Stage-4 authorization on v002 | **NOT authorized by this memo** |
| Acquisition (additional days / symbols / data families beyond the 90 locked v002 dates) | docs + data | **NOT authorized; not in scope of Phase 4bm-E** |
| Feature computation, ML, strategy, backtests on v002 | code + data | **FORBIDDEN by Phase 4bm-E** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-E** |

---

## 31. Closeout / lock preservation

Phase 4bm-E is docs-only and produces:

- this memo (`docs/00-meta/implementation-reports/2026-05-18_phase-4bm-e_multi-day-derived-family-research-eligibility-decision-memo.md`);
- the Phase 4bm-E closeout (`docs/00-meta/implementation-reports/2026-05-18_phase-4bm-e_closeout.md`);
- a narrow Phase 4bm-E paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md` (prior Phase 4bm-D-P1 "Current phase:" block preserved as labelled historical context).

No source code, tests, scripts, configs, READMEs, MCP files, runtime configuration, manifests, raw artefacts, normalized artefacts, gate reports, successor-state artefacts, or `.gitignore` entries were modified by Phase 4bm-E.

The `data/microstructure/` namespace is untouched by Phase 4bm-E. The 90 v002 per-day Parquets, 90 v002 sidecars, 90 v002 raw zips, 90 v002 raw zip sidecars, v002 acquisition log, v002 raw manifest, v002 derived multi-day index manifest, Phase 4bl-D-R gate report and sidecar, Phase 4bl-E raw successor-state JSON and sidecar, Phase 4bm-D authoritative gate report and sidecar, Phase 4bd v001 normalized Parquet, Phase 4bd v001 derived manifest, Phase 4az v001 raw manifest / zip / sidecar / acquisition log, Phase 4bb-D v001 raw gate report, Phase 4bf v001 derived gate report, Phase 4bg-B v001 successor-state JSON, Phase 4bh v001 feature parquet / manifest (if present), Phase 4bj-C v001 label parquet / manifest (if present), Phase 4bj-G v001 label successor-state JSON (if present), Phase 4bi-D v001 feature successor-state JSON (if present), and every other prior `data/microstructure/` artefact all remain byte-identical pre- and post-Phase-4bm-E.

The decision recorded in §21 is **Option B**: Stage-3 admissibility in principle at policy level for the multi-day v002 normalized derived family, with no manifest mutation in this phase and a separately authorized successor-state recording phase (Phase 4bm-F) required before any machine-readable `research_eligible = true` marker exists for v002. The raw family remains permanently `research_eligible = false` across both v001 and v002. Feature computation on v002 remains forbidden until a separately authorized multi-day feature-boundary design memo and a separately authorized v002 feature implementation phase. ML / strategy / backtest work on v002 remains forbidden under the Phase 4ak M0 admissibility gate, the post-null cooldown rule, and the cooled-down families list.

**Recommended state: remain paused.** No next phase authorized.
