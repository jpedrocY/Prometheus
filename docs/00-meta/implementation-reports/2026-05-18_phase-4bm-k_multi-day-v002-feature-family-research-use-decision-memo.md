# Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo

**Phase identity:** Phase 4bm-K — Multi-Day V002 Feature-Family Research-Use Decision Memo (docs-only).
**Date:** 2026-05-18.
**Branch:** `phase-4bm-k/multi-day-v002-feature-family-research-use-decision-memo`.
**Base:** `main` at `89bf2cfb45b7c46f77e23669570e9f380c6a2e91` (Phase 4bm-J merge-closeout SHA-finalization commit; pre-branch `main == origin/main` verified).
**Tier:** **Tier 1 — Full Phase** per `docs/00-meta/process/phase-risk-tiering-standard.md` §3 escalation rules and the v001 Phase 4bi-C v001 feature-family research-use / ML-use decision memo precedent. First-of-kind multi-day v002 feature-family research-use governance / admissibility decision.
**Phase type:** docs-only research-use decision / governance memo — no source / test / script / config / data mutation; no manifest mutation; no successor-state artefact creation; no gate rerun; no acquisition; no successor authorization.
**Status:** drafted; pending operator review.

---

## 1. Phase identity, branch, base SHA, risk tier

This memo answers a single question:

> Given the Phase 4bm-G feature-boundary design memo, the Phase 4bm-H computed v002 feature artefacts, the Phase 4bm-I 50+ check `FEATURE_STRUCTURAL_QA_PASS`, and the Phase 4bm-J 50 / 50 `FEATURE_GATE_PASS` at report level (gate report SHA256 `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242`), should the project authorize a future v002 Feature Stage-5 research-use admissibility recording for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002` (BTCUSDT × 90 contiguous UTC dates 2024-12-01 .. 2025-02-28; 155,153,449 rows; feature_config_hash `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d`), and under what exact constraints?

The memo is **docs-only**. It records a policy-level admissibility decision. It does not mutate any manifest, flip any `research_eligible` flag, transition any `eligibility_gate_status`, mark `stage_4_feature_cleared = true`, run any gate, modify any data file, compute any feature, label, signal, proxy, ML, strategy, or backtest output, acquire any data, or authorize any successor implementation.

The memo preserves every retained verdict, every project lock, the Phase 4ak twelve-clause M0 admissibility gate (including the post-null cooldown rule and cooled-down families list), the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant, the Phase 4bb-F canonical path policy, the Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the Phase 4bm-E Option B / Decision form 2 v002 derived-family policy decision, the Phase 4bm-F v002 derived-family Stage-3 successor-state semantics, the Phase 4bm-G v002 feature-boundary design, the Phase 4bm-H v002 feature computation result, the Phase 4bm-I v002 feature-artefact structural QA verdict, and the Phase 4bm-J v002 feature-family eligibility-gate verdict.

---

## 2. Scope and boundary

In scope for this memo:

- evaluating the question: is v002 Feature Stage-5 research-use admissible **in principle at policy level** for the multi-day v002 feature family at this point in the project record?
- selecting one decision outcome and justifying the choice using the Phase 4bi-C decision framework;
- defining the Stage-5 policy meaning and its strict boundaries;
- mapping the available evidence (v002 Feature Stages 0, 2, 3, and report-level Stage 4) onto policy admissibility;
- recording the residual risks, the feature-manifest immutability rule for this phase, the label boundary, the strategy / backtest boundary, the acquisition boundary, and the M0 / no-rescue boundary;
- recommending the conservative successor sequence without authorizing any successor.

Reusable non-authorization blocks from `docs/00-meta/process/phase-risk-tiering-standard.md` §7 that apply to this memo: **N-ACQUISITION**, **N-ENDPOINT**, **N-CREDENTIALS**, **N-MANIFEST**, **N-GATE-RERUN**, **N-SUCCESSOR-STATE**, **N-DERIVATION**, **N-DIAGNOSTICS-ML-STRATEGY**, **N-PHASE-5**, **N-VERDICT-LOCK**.

Out of scope for this memo (categorical exclusions):

- modifying any source code, test, script, configuration, dataset, manifest, sidecar, gate report, successor-state JSON, or any tracked file beyond this memo, its closeout, and a narrow `current-project-state.md` paragraph + new "Current phase:" block (with the prior Phase 4bm-J block preserved as labelled historical context);
- running the v002 normalizer, v002 raw eligibility gate, v002 derived-family gate, v002 feature kernel, or v002 feature-family eligibility gate;
- generating a new gate report or regenerating any prior gate report;
- creating or modifying any `data/microstructure/` artefact;
- creating JSONL, Parquet, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquiring data, calling public endpoints, calling Binance APIs, opening WebSockets, using private endpoints, requesting credentials, reading or creating `.env`, creating `.mcp.json`, or enabling MCP / Graphify;
- computing returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position-state, or any column beyond the 62-column Phase 4bm-G / Phase 4bm-H canonical v002 feature schema (17 lineage + 45 feature/quality);
- training ML, creating labels or targets, designing strategy logic, running backtests, running simulations, or computing any prediction / model-score / decision-score;
- flipping `research_eligible` on any family;
- transitioning `eligibility_gate_status` on any actual on-disk manifest;
- marking `stage_4_feature_cleared = true` on the v002 feature manifest;
- changing `chronological_split_policy` on any actual on-disk manifest;
- creating any successor-state artefact (multi-day v002 feature-family or otherwise);
- authorizing v002 Feature Stage-5 successor-state recording, label-family work, diagnostics, ML, strategy, or backtests;
- revising retained verdicts, changing project locks, or amending M0 / Phase 4al / Phase 4aw / Phase 4bb-F / Phase 4bl-F / Phase 4bm-A-P1 / Phase 4bm-D-P1 / Phase 4bm-E / Phase 4bm-F / Phase 4bm-G / Phase 4bm-H / Phase 4bm-I / Phase 4bm-J;
- authorizing Phase 4bm-L (multi-day v002 feature-family successor-state recording), Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- committing anything under `data/microstructure/`.

---

## 3. Linkage to Phase 4bm-J FEATURE_GATE_PASS

Phase 4bm-K depends entirely on the locked outputs of Phase 4bm-J:

- Phase 4bm-J is project-complete on `main` (merge commit `2fe5e5949ddd7aedf8e2ba60f5dc88f2afc550ec`; merge-closeout commit `9af355c3f3f7d93c84ba23e93819a7e1ced74db5`; SHA-finalization commit `89bf2cfb45b7c46f77e23669570e9f380c6a2e91`).
- The Phase 4bm-J gate report at `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json` exists locally with SHA256 `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` (gitignored under `.gitignore:85: data/microstructure/`; not committed). Recomputed on disk in Phase 4bm-K: matches byte-for-byte.
- The paired canonical Phase 4bb-F sidecar at `<report>.json.sha256` exists locally with SHA256 `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125`; recomputed on disk in Phase 4bm-K: matches byte-for-byte.
- The Phase 4bm-J gate report records `overall_status = "pass"`, `gate_verdict = "FEATURE_GATE_PASS"`, 50 / 50 PASS (0 FAIL / 0 ERROR / 0 NOT_APPLICABLE / 0 blocking failures), across 7 check groups (A: 12 locked-precondition; B: 10 inventory/sidecar/gitignore; C: 10 schema/lineage/forbidden-substring; D: 6 row-count/partition/timestamp; E: 3 quality-flag/cross-day-boundary; F: 3 upstream-immutability; G: 6 non-authorization-invariant).
- The Phase 4bm-J gate report records the result invariants `research_eligible_after = false`, `feature_manifest_research_eligible_after = false`, `feature_manifest_eligibility_gate_status_after = "pending"`, `stage_4_feature_cleared_after = false`, all 8 non-authorization flags `false`, all 14 immutability flags `true`, and 21 boundary_confirmations all `True`.
- The Phase 4bm-J merge-closeout records every required boundary phrase verbatim (`Phase 4bm-J is a feature-family eligibility gate phase only.` / `Gate verdict: FEATURE_GATE_PASS.` / `FEATURE_GATE_PASS is report-level only.` / `Phase 4bm-K is not authorized by Phase 4bm-J.` / `Feature-family research-use is not authorized by Phase 4bm-J.` / `Feature-family successor-state recording is not authorized by Phase 4bm-J.` / `Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-J.` / `No feature artefact was modified.` / `No upstream artefact was mutated.` / `No data/microstructure file was committed.`).

This memo does not re-derive that evidence; it cites it as locked input.

---

## 4. Linkage to Phase 4bm-I FEATURE_STRUCTURAL_QA_PASS

Phase 4bm-I is the immediate predecessor of Phase 4bm-J and the v002 Feature Stage-3 structural QA evidence layer:

- read-only structural QA of all 90 v002 per-day feature Parquets + 90 paired canonical Phase 4bb-F sidecars + 1 feature manifest + 1 manifest sidecar;
- verdict: `FEATURE_STRUCTURAL_QA_PASS`;
- inspected on-disk values matched the Phase 4bm-H recorded values byte-for-byte (90 / 90 per-day Parquet SHAs; 62-column canonical schema across all 90 days; total row count 155,153,449; per-day feature row counts == source normalized event counts byte-for-byte across all 90 days; 0 forbidden-substring hits; safe `source_phase_4bm_e_outcome` present; unsafe `source_phase_4bm_e_decision` absent);
- no upstream artefact mutated;
- no manifest mutated;
- no `data/microstructure/` write occurred;
- the Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked).

Phase 4bm-J's check A12 asserted `structural_qa_verdict == "FEATURE_STRUCTURAL_QA_PASS"` as a hard precondition; A12 PASS in the Phase 4bm-J gate report is the machine-readable evidence that Phase 4bm-I PASS is locked into the v002 Feature Stage-4 report-level evidence. Phase 4bm-K cites Phase 4bm-I PASS via the Phase 4bm-J gate-report record without re-running structural QA.

---

## 5. Linkage to Phase 4bm-H feature artefacts

Phase 4bm-H produced the locked v002 feature artefacts that Phase 4bm-I structurally QA-passed and Phase 4bm-J gate-passed:

- Feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` (SHA `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d`; size 85,929 bytes). Recomputed on disk in Phase 4bm-K: matches byte-for-byte.
- Feature manifest sidecar at `<manifest>.sha256` (SHA `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34`; size 116 bytes; canonical Phase 4bb-F format). Recomputed on disk in Phase 4bm-K: matches byte-for-byte.
- 90 per-day v002 feature Parquets under `data/microstructure/features/microstructure_features_aggtrades_v001__v002/BTCUSDT/<YYYY>/<MM>/BTCUSDT-features-aggtrades-<YYYY-MM-DD>.parquet` (90 / 90 SHAs match manifest's `per_day_outputs[i].feature_parquet_sha256` per Phase 4bm-J check B10).
- 90 paired canonical Phase 4bb-F sidecars under the same tree (90 / 90 canonical-format and SHA-consistent per Phase 4bm-J check B9).
- `feature_config_hash = 819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` (Phase 4bm-H locked value; Phase 4bm-J check C8 PASS).
- Total feature row count = `155,153,449` (1:1 parity with the Phase 4bm-B v002 normalized event count; Phase 4bm-J checks D1–D5 PASS).
- Feature date range = `2024-12-01` through `2025-02-28` inclusive (90 contiguous UTC days; Phase 4bm-J checks B3–B6 PASS).
- Symbol scope = BTCUSDT (Phase 4bm-J check B4 PASS).
- Feature schema = 62 columns total = 17 lineage / identity / metadata + 45 feature / quality columns (Phase 4bm-J checks C1–C4 + C9 + C10 PASS).
- Feature manifest still carries `research_eligible = false`, `eligibility_gate_status = "pending"`, `stage_4_feature_cleared = false` byte-identically (Phase 4bm-J checks G1–G3 PASS; verified directly on disk in this memo).

Phase 4bm-K reads each of these as locked evidence and does not recompute features, does not rerun the feature kernel, does not regenerate the manifest, and does not modify any per-day Parquet or sidecar.

---

## 6. Linkage to Phase 4bm-G feature-boundary design

Phase 4bm-G is the v002 Feature Stage-0 design layer. Its binding rules are the policy substrate over which Phase 4bm-H computed, Phase 4bm-I structurally QA'd, and Phase 4bm-J gate-checked the v002 feature family. Phase 4bm-G binding rules cited by the Phase 4bm-J check suite (and therefore by this memo):

- §13 forbidden-substring detector across the 62-column schema: 0 hits (Phase 4bm-J check C7 PASS).
- §14 leakage / timestamp policy: `feature_timestamp_ms == source_transact_time_ms` on every sampled row; `(feature_timestamp_ms, row_index)` monotonic per day (Phase 4bm-J check D6 PASS).
- §16 multi-day rolling-window / cross-day lookback: day-1 `rolling_missing_window_flag` rule confirmed against `(T - 60_000) < day_start_ms` (Phase 4bm-J check E1 PASS); days 2..90 sampled `rolling_missing_window_flag = false` (E2 PASS); per-event `invalid_window_flag = false` everywhere (E3 PASS).
- §18 fail-closed rules (missing/SHA-mismatched lineage artefact, manifest mutation attempt, non-monotonic timestamp, forbidden column, network/credential surface) each surface as a Phase 4bm-J A/B/C/D/F group check — all PASS.
- §13 / §16 safe lineage column `source_phase_4bm_e_outcome` present (Phase 4bm-J check C5 PASS); §13 unsafe lineage column `source_phase_4bm_e_decision` absent (C6 PASS).

Phase 4bm-K does not weaken, expand, or reinterpret any Phase 4bm-G rule.

---

## 7. Linkage to Phase 4bm-F v002 Stage-3 successor-state marker

Phase 4bm-F recorded the v002 derived-family Stage-3 research-eligibility successor-state marker as a sibling artefact while preserving the original v002 derived multi-day index manifest byte-identically:

- successor-state JSON at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v002__stage3_research_eligible__phase-4bm-f.json` SHA256 `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9`. Recomputed on disk in Phase 4bm-K: matches.
- paired sidecar SHA256 `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97`. Recomputed on disk in Phase 4bm-K: matches.
- the original v002 derived multi-day index manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` SHA256 `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` is preserved byte-identically and continues to carry `research_eligible = false`, `eligibility_gate_status = "pending"`.

The Phase 4bm-F successor-state JSON is the precedent for any future v002 feature-family successor-state recording phase: a sibling artefact is recorded, the original manifest stays byte-identical, and the original `research_eligible / eligibility_gate_status` fields remain unchanged. If Phase 4bm-L is ever separately authorized, it must follow the same pattern at the v002 feature-family level.

Phase 4bm-K does not modify the Phase 4bm-F successor-state JSON or its sidecar.

---

## 8. Linkage to Phase 4bi-C v001 precedent

Phase 4bi-C is the structural precedent for this memo. The v001 / v002 mapping is exact:

| v001 layer | v001 phase | v002 layer | v002 phase |
| ---------- | ---------- | ---------- | ---------- |
| Feature boundary | Phase 4bh-A / 4bh-B | Feature boundary | Phase 4bm-G |
| Feature implementation | Phase 4bh | Feature computation | Phase 4bm-H |
| Feature artefact structural QA | Phase 4bi-A | Feature artefact structural QA | Phase 4bm-I |
| Feature-family eligibility gate | Phase 4bi-B (70 / 70 PASS) | Feature-family eligibility gate | Phase 4bm-J (50 / 50 PASS) |
| Feature research-use decision | **Phase 4bi-C (Outcome 1 / Decision form 1)** | Feature research-use decision | **Phase 4bm-K (this memo)** |
| Feature successor-state recording | Phase 4bi-D | Feature successor-state recording (conditional) | Phase 4bm-L (NOT authorized) |

Phase 4bi-C selected **Outcome 1 / Decision form 1**:

> Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for the feature family `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.

Phase 4bi-C's three docs-only outcome labels (its decision framework):

- **Outcome 1 — Stage-5 admissible in principle at policy level, successor-state required.**
- **Outcome 2 — Stage-5 deferred.**
- **Outcome 3 — Stage-5 rejected.**

These labels are reused verbatim in this memo's §11. The brief's alternative labels (`FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE` / `FEATURE_RESEARCH_USE_REJECTED` / `FEATURE_RESEARCH_USE_INDETERMINATE`) are recorded as equivalent designators in §13 to satisfy the operator-report standard; the memo records both the precedent label and the alternative label for the chosen outcome.

The v001 → v002 evidence delta is summarized in §10 (scale-up: 1 day → 90 days; 1.68 M rows → 155.15 M rows; 1 symbol → 1 symbol — cross-symbol coverage unchanged; v001 70-check gate → v002 50-check gate spanning the multi-day scope).

---

## 9. Evidence table

| # | Evidence item | Value | Status |
| - | ------------- | ----- | ------ |
| 1 | Feature manifest path | `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` | exists; gitignored |
| 2 | Feature manifest SHA256 | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | recomputed in Phase 4bm-K; matches Phase 4bm-H / 4bm-I / 4bm-J recorded value |
| 3 | Feature manifest size | 85,929 bytes | recorded |
| 4 | Feature manifest sidecar path | `<manifest>.sha256` | exists; gitignored; canonical Phase 4bb-F format |
| 5 | Feature manifest sidecar SHA256 | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | recomputed in Phase 4bm-K; matches |
| 6 | Phase 4bm-J gate report path | `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v002__phase-4bm-j__1779475950843__3212722a7ffd.json` | exists; gitignored |
| 7 | Phase 4bm-J gate report SHA256 | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | recomputed in Phase 4bm-K; matches Phase 4bm-J recorded value |
| 8 | Phase 4bm-J gate report size | 16,176 bytes | recorded |
| 9 | Phase 4bm-J gate sidecar path | `<report>.json.sha256` | exists; gitignored; canonical Phase 4bb-F format byte-verified |
| 10 | Phase 4bm-J gate sidecar SHA256 | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | recomputed in Phase 4bm-K; matches |
| 11 | `feature_config_hash` | `819cfa7a9b3a813333ce163074dfe31b5b2886253c0835c4646bc3797d7b5a1d` | Phase 4bm-H locked; Phase 4bm-J check C8 PASS |
| 12 | Total feature row count | `155,153,449` | Phase 4bm-J check D1 PASS; 1:1 parity with v002 normalized event count |
| 13 | Feature date range | `2024-12-01` .. `2025-02-28` inclusive (90 contiguous UTC days) | Phase 4bm-J checks B3–B6 PASS |
| 14 | Symbol scope | BTCUSDT (one symbol) | Phase 4bm-J check B4 PASS |
| 15 | Feature schema column count | 62 (= 17 lineage / identity / metadata + 45 feature / quality) | Phase 4bm-J checks C1–C4 + C9 + C10 PASS |
| 16 | Phase 4bm-I structural QA verdict | `FEATURE_STRUCTURAL_QA_PASS` | confirmed by Phase 4bm-J check A12 PASS |
| 17 | Phase 4bm-J gate verdict | `FEATURE_GATE_PASS` | recorded `gate_verdict` field in the gate report |
| 18 | Phase 4bm-J overall_status | `pass` | recorded `overall_status` field |
| 19 | Phase 4bm-J check totals | total 50; PASS 50; FAIL 0; ERROR 0; NOT_APPLICABLE 0; blocking failures 0 | recorded `pass_count` / `fail_count` / `error_count` / `not_applicable_count` / `blocking_fail_count` |
| 20 | Phase 4bm-J boundary confirmations | 21 / 21 `True` | recorded |
| 21 | Phase 4bm-J immutability flags | 14 / 14 `true` | recorded |
| 22 | Phase 4bm-J non-authorization flags | 8 / 8 `false` | recorded |
| 23 | Feature manifest `research_eligible` | `false` | verified on disk in Phase 4bm-K; Phase 4bm-J check G1 PASS |
| 24 | Feature manifest `eligibility_gate_status` | `"pending"` | verified on disk in Phase 4bm-K; Phase 4bm-J check G2 PASS |
| 25 | Feature manifest `stage_4_feature_cleared` | `false` | verified on disk in Phase 4bm-K; Phase 4bm-J check G3 PASS |

All 25 evidence items are internally consistent. No verdict has been revised. No project lock has been loosened. No upstream artefact has been mutated.

---

## 10. Upstream lineage SHA table

Recomputed on disk in Phase 4bm-K at memo-write time; every SHA matches the Phase 4bm-G / Phase 4bm-H / Phase 4bm-I / Phase 4bm-J recorded values byte-for-byte.

| # | Artefact | SHA256 | Status |
| - | -------- | ------ | ------ |
| 1 | v002 derived multi-day index manifest | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | unchanged |
| 2 | v002 derived manifest sidecar | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | unchanged |
| 3 | v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` | unchanged |
| 4 | v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` | unchanged |
| 5 | Phase 4bl-D-R raw multi-day PASS gate report | `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46` | unchanged |
| 6 | Phase 4bl-E raw multi-day successor-state JSON | `a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d` | unchanged |
| 7 | Phase 4bm-D authoritative derived-family gate report | `3b45e70bbe45d25bb5b3d0dc164ad2903577dfc3e692f35433014179d8ef781a` | unchanged |
| 8 | Phase 4bm-D authoritative sidecar | `8e74261c0b0bf2dedb75691e14d100e0ff1368b094ff1e5984a2dc36da53d711` | unchanged |
| 9 | Phase 4bm-F v002 derived-family successor-state JSON | `72b6edd42d42cb4451108ea7adeb859c0d693b58c9c33c522285f7c2ba309ea9` | unchanged |
| 10 | Phase 4bm-F v002 derived-family successor-state sidecar | `1e9ffb23770fc92c20be07851b9edbb66459f6bb1bddc58dae208d5995ebcb97` | unchanged |
| 11 | v002 feature manifest | `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` | unchanged |
| 12 | v002 feature manifest sidecar | `22e2fb77e75071f032935a971b691e851ac396a266946a8d9b6862e70b2c4c34` | unchanged |
| 13 | Phase 4bm-J v002 feature-family eligibility gate report | `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` | unchanged |
| 14 | Phase 4bm-J v002 feature-family gate sidecar | `14a17764cd5798f8df7d59203079b5e29823e1804ed8626d41ccd87b84166125` | unchanged |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved in this phase (never invoked).

V001 → V002 evidence delta (orientation only; v001 evidence not modified by this memo):

| Dimension | v001 (Phase 4bi-C) | v002 (this memo) | Delta |
| --------- | ------------------ | ----------------- | ----- |
| Symbol coverage | BTCUSDT (one symbol) | BTCUSDT (one symbol) | unchanged — no cross-symbol robustness gained |
| Date coverage | 1 UTC day (2025-01-15) | 90 contiguous UTC days (2024-12-01 .. 2025-02-28) | **+89 days** |
| Feature row count | 1,681,098 | 155,153,449 | **~92× scale-up** |
| Feature schema | 61 columns (45 features + 16 lineage; v001 Phase 4bh-B) | 62 columns (45 features/quality + 17 lineage/identity/metadata; v002 Phase 4bm-G / 4bm-H) | +1 lineage column (`source_phase_4bm_e_outcome` introduced by Phase 4bm-G §13 / §14 and verified present by Phase 4bm-J check C5; unsafe `source_phase_4bm_e_decision` verified absent by C6) |
| Feature-family gate scope | Phase 4bi-B (70 / 70 PASS; single-day; v001) | Phase 4bm-J (50 / 50 PASS; 90-day; v002) | multi-day evidence; tighter check count but broader per-check scope (each check covers all 90 days) |
| Phase 4ba Feature Stages reached | Stage-0 ✓, Stage-2 ✓, Stage-3 ✓, Stage-4 ✓ (report-level) | Stage-0 ✓, Stage-2 ✓, Stage-3 ✓, Stage-4 ✓ (report-level) | parity at this layer; Stage-5 manifest-level still requires a separately authorized successor-state recording phase (Phase 4bi-D for v001 was authorized after Phase 4bi-C; Phase 4bm-L for v002 is **not** authorized by Phase 4bm-K) |

---

## 11. Decision criteria

The Phase 4ba ladder, extended by the Phase 4bh-A v001 design and the Phase 4bm-G v002 multi-day design, defines a feature-family ladder applied here at the v002 level:

- **v002 Feature Stage-0** — feature-boundary design memo (Phase 4bm-G).
- **v002 Feature Stage-2** — local feature artefacts exist with manifest (Phase 4bm-H).
- **v002 Feature Stage-3** — structurally QA-passed at memo level (Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS`).
- **v002 Feature Stage-4** — feature-family eligibility gate PASS at report level (Phase 4bm-J `FEATURE_GATE_PASS`).
- **v002 Feature Stage-5** — research-use admissibility decision (this memo; Phase 4bm-K).
- **v002 Feature Stage-6** (or successor-state recording) — sibling successor-state artefact, only by separate authorization (Phase 4bm-L; NOT authorized by Phase 4bm-K).

The Phase 4bi-C decision framework provides three docs-only outcomes:

- **Outcome 1 — Stage-5 admissible in principle at policy level, successor-state required** (equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`). Selected when the evidence chain is complete and consistent and no structural blocker exists.
- **Outcome 2 — Stage-5 deferred** (equivalent to `FEATURE_RESEARCH_USE_INDETERMINATE`). Selected when there is a missing evidence link or an unresolved structural risk that prevents Stage-5 admissibility at this time.
- **Outcome 3 — Stage-5 rejected** (equivalent to `FEATURE_RESEARCH_USE_REJECTED`). Selected when there is a structural reason the feature family is not admissible at all (e.g., schema violation, lineage break, governance violation, leakage, label leakage, ungoverned ratio-column access).

The eight deciding criteria are restated from Phase 4bi-C and adapted to the multi-day v002 evidence:

1. Phase 4bm-J gate report present and SHA matches recorded value — **PASS** (`3c59dfae…`; recomputed in §9 / §10).
2. Phase 4bm-J gate report `overall_status = "pass"` with 50 / 50 PASS — **PASS**.
3. Phase 4bm-J check totals match recorded (50 / 50 / 0 / 0 / 0 / 0) — **PASS**.
4. Phase 4bm-J feature-manifest SHA matches recorded value — **PASS** (`512a0a54…`).
5. Phase 4bm-J feature-manifest sidecar SHA matches recorded value — **PASS** (`22e2fb77…`).
6. Feature manifest remains `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` — **PASS** (verified on disk).
7. Phase 4bm-G / 4bm-H / 4bm-I / 4bm-J evidence is internally consistent — **PASS** (every check group; Phase 4bm-J 21 / 21 boundary_confirmations all True; cross-artefact lineage SHAs unchanged per Phase 4bm-K §10).
8. All non-scope and no-rescue boundaries remain preserved — **PASS** (M0 binding prospectively; Phase 4al refined no-rescue rule + §13 + §14 preserved; Phase 4aw flip-invariant preserved; Phase 4bb-F canonical path policy preserved; Phase 4bl-F four-tier risk model preserved; nine N-blocks honored per §2).

All eight deciding criteria are satisfied. There is no missing evidence link and no unresolved structural risk.

---

## 12. Decision analysis

The Phase 4bm-J `FEATURE_GATE_PASS` is the deepest report-level evidence the project has for the v002 feature family. Its 50-check suite is structurally tighter than the v001 70-check suite (because per-check scope is broader: each B / C / D / E / F group check spans all 90 days rather than one day), and its A-group locked preconditions explicitly chain back to:

- the Phase 4bm-I `FEATURE_STRUCTURAL_QA_PASS` precondition (A12);
- the Phase 4bm-H feature manifest + sidecar SHAs (A1 / A2);
- the Phase 4bm-D derived-family gate report + sidecar SHAs (A4 / A5);
- the Phase 4bm-F derived-family successor-state JSON + sidecar SHAs (A6 / A7);
- the Phase 4bl-D-R raw multi-day PASS gate report + Phase 4bl-E raw multi-day successor-state SHAs (A8 / A9);
- the v002 derived multi-day index manifest + v002 raw manifest SHAs (A10 / A11).

This chains the v002 Feature Stage-4 report-level evidence back through every upstream layer: Phase 4bl-C raw acquisition → Phase 4bl-D-R raw eligibility gate → Phase 4bl-E raw successor-state → Phase 4bm-B derived normalization → Phase 4bm-C structural QA → Phase 4bm-D derived-family eligibility gate → Phase 4bm-E v002 derived-family policy decision (Option B / Decision form 2) → Phase 4bm-F v002 derived-family Stage-3 successor-state recording → Phase 4bm-G v002 feature-boundary design → Phase 4bm-H v002 feature computation → Phase 4bm-I v002 feature artefact structural QA → Phase 4bm-J v002 feature-family eligibility gate. Every link is SHA-verifiable on the local machine; every upstream artefact is byte-identical pre- and post- every successor phase (Phase 4bm-J merge-closeout §11 confirms 12 / 12 byte-identical at gate-run time; Phase 4bm-K §10 reconfirms the same set on the local machine at memo-write time).

The Phase 4bm-G design explicitly forbids label / target / signal / ML / strategy / backtest semantics inside the feature schema (§13 forbidden-substring list — 26 tokens scanned by Phase 4bm-J check C7 with 0 hits). The Phase 4bm-G §14 timestamp / leakage policy is enforced by Phase 4bm-J check D6. The Phase 4bm-G §16 multi-day cross-day-lookback policy is enforced by Phase 4bm-J checks E1 / E2 / E3 (per-event `invalid_window_flag = false` everywhere; day-1 `rolling_missing_window_flag` rule matches `(T - 60_000) < day_start_ms`; days 2..90 sampled `rolling_missing_window_flag = false`). No leakage is structurally possible under this design.

The 90-day scope materially strengthens the v002 artefact-integrity story relative to the v001 single-day evidence (92× scale-up; 89 additional contiguous UTC days; multi-day cross-day boundary verified by Phase 4bm-J E-group; upstream immutability across 12 governance artefacts and 90 derived per-day Parquets verified by Phase 4bm-J F-group). The 90-day scope does not address the cross-symbol gap (one symbol only; BTCUSDT) and does not address the regime / day-type distribution within the 90-day window. Those limitations are recorded explicitly in §14 (residual risks) and do not block a policy-level admissibility decision, but they shape what such a decision means (it is a governance state about clean, lineage-verifiable feature artefacts; it is not an empirical claim about edge).

There is no missing evidence link, no unresolved structural risk, and no governance violation. The eight Phase 4bi-C deciding criteria are satisfied (§11). The evidence supports **Outcome 1** under the Phase 4bi-C framework, i.e., admissible in principle at policy level with successor-state recording required before any machine-readable Stage-5 marker exists.

---

## 13. Final research-use decision

**Outcome 1 (Decision form 1) — equivalent to `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`:**

> **v002 Feature Stage-5 research-use admissibility is admissible in principle at policy level for the multi-day v002 feature family `microstructure_features_aggtrades_v001 @ v002`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bm-L successor-state recording phase is required before any machine-readable v002 Feature Stage-5 marker exists.**

Specifically:

- the v002 feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v002.json` remains `research_eligible = false`, `eligibility_gate_status = "pending"`, and `stage_4_feature_cleared = false` throughout Phase 4bm-K and after;
- no machine-readable v002 Feature Stage-5 marker exists yet;
- a future Phase 4bm-L would be required to create a sibling successor-state artefact (the v002 feature-family analogue of Phase 4bi-D for v001 features and Phase 4bm-F for v002 derived), without overwriting or mutating the v002 feature manifest;
- the original v002 feature manifest must remain byte-identical at SHA `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` until any such separate authorisation;
- the Phase 4bm-F v002 derived-family successor-state JSON (`72b6edd4…`) is the only v002 Stage-3 machine-readable marker on record; it does not transitively extend to the v002 feature family;
- labels remain forbidden (no v002 label kernel; no v002 label parquet; no v002 label manifest);
- targets remain forbidden;
- ML remains forbidden (`ml_authorized = false` in the Phase 4bm-J gate report);
- strategy remains forbidden (`strategy_authorized = false` in the Phase 4bm-J gate report);
- backtests remain forbidden (`backtest_authorized = false` in the Phase 4bm-J gate report);
- diagnostics remain forbidden (`diagnostics_authorized = false`);
- additional acquisition remains unauthorized (`acquisition_authorized = false`);
- v002 Feature Stage-5 policy admissibility is **not** a strategy hypothesis, **not** a predictive claim, **not** an edge claim, **not** a backtest permission, **not** an M0 bypass, **not** a successor authorization, and **not** a permission to acquire more data.

This is the conservative outcome and the correct outcome given that all eight Phase 4bi-C deciding criteria are satisfied at the v002 evidence layer.

---

## 14. Affirmative-decision required exact phrases

Because the decision is affirmative (Outcome 1; `FEATURE_RESEARCH_USE_APPROVED_IN_PRINCIPLE`), the following exact phrases are recorded verbatim, per the brief:

- **Feature-family research-use is approved in principle at policy level only.**
- **No machine-readable research-use marker exists after Phase 4bm-K.**
- **Phase 4bm-L is not authorized by Phase 4bm-K.**
- **Successor-state recording is not authorized by Phase 4bm-K.**
- **Labels / diagnostics / ML / strategy / backtests are not authorized by Phase 4bm-K.**
- **No feature artefact was modified.**
- **No upstream artefact was mutated.**
- **No data/microstructure file was committed.**

---

## 15. Residual risks and limitations

The eight deciding criteria address artefact integrity and governance bookkeeping. They do **not** address statistical sufficiency for any research question. The following limitations remain after Phase 4bm-K (most are unchanged from Phase 4bi-C; the date-coverage limitation is materially reduced but not eliminated):

- **Symbol scope is one symbol** (BTCUSDT only). No cross-symbol coverage exists in v002.
- **Date scope is 90 contiguous UTC days** (2024-12-01 .. 2025-02-28). 90 days is meaningfully better than the 1-day v001 sample but is still a bounded window. No multi-quarter or multi-year coverage exists.
- **Day-type distribution within the 90 days is not yet diagnosed.** This memo records no claim about whether the 90 days are dominated by quiet vs volatile sessions, trend vs range regimes, or any other classification.
- **Research-use admissibility of the v002 feature family is not the same as statistical sufficiency** for any specific research question, signal, model, or strategy.
- **No multi-day robustness analysis has been performed** beyond structural QA and the eligibility gate. The Phase 4bm-I / 4bm-J evidence is integrity-shaped, not distribution-shaped.
- **No cross-symbol robustness exists.** A one-symbol sample cannot generalize.
- **No label set is authorized on v002** (no v002 label-family phase exists; Phase 4bj-A..K label work is v001-only and does not transitively extend to v002).
- **No leakage control design exists for v002 labels** (no temporal-leakage barrier has been specified for future v002 label work — the Phase 4bm-G §14 timestamp policy governs features only).
- **No ML split design exists for v002** (no train / validation / OOS partitioning policy for v002 microstructure-driven research has been authored; Phase 4bj-H / 4bj-I / 4bj-J chronological-split policy memos are v001-only).
- **No strategy hypothesis exists under the Phase 4ak M0 admissibility gate** that would consume the v002 dataset. The microstructure / order-flow / liquidity-timing lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption.
- **No costed backtest exists** for any microstructure-driven hypothesis (the §11.6 8 bps per-side cost lock applies regardless).
- **No live / paper / shadow readiness exists.** None is approached by Stage-5 admissibility.
- **Stage-5, even if affirmative at policy level, only permits governed research use of the clean v002 feature artefact.** It does not license any claim of edge.

These limitations are not blockers to a policy-level Stage-5 admissibility decision for v002. They are explicit constraints on what such a decision means.

---

## 16. What the decision proves

- The Phase 4bm-G / 4bm-H / 4bm-I / 4bm-J evidence chain is internally consistent at policy level.
- Phase 4bm-J's 50 / 50 PASS at report level is sufficient evidence for the policy-level admissibility question this memo answers.
- The v002 feature family is structurally suitable for future research-use admissibility consideration.
- A future v002 Feature Stage-5 successor-state recording is governance-supportable.
- No upstream artefact has changed; 14-artefact byte-identical immutability is preserved across the entire arc by Phase 4bm-K (§10).
- The M0 admissibility gate, post-null cooldown rule, refined no-rescue rule, Phase 4aw flip-invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model, and the feature-family boundary all remain binding.

---

## 17. What the decision does not prove

- The v002 feature family is **not** proven to have predictive validity.
- The v002 feature family is **not** proven to produce a tradable signal.
- The v002 feature family's evidence chain is **not** generalised to additional symbols beyond BTCUSDT.
- The v002 evidence chain is **not** generalised to additional UTC dates beyond the 90 contiguous days `2024-12-01 .. 2025-02-28`.
- No label has been designed for v002.
- No target has been defined for v002.
- No train / validation / test split has been designed for v002.
- No strategy hypothesis has been admitted under M0 that would consume v002.
- No backtest has been run on v002.
- No edge claim is made.
- No baseline-superiority claim is made.
- No out-of-sample evaluation is implied.
- No successor authorization is granted by Phase 4bm-K alone.

The Phase 4bm-K decision is policy admissibility only.

---

## 18. Non-authorization

Phase 4bm-K does **not**, and **cannot**, authorize:

- Phase 4bm-L — Multi-Day V002 Feature-Family Research-Use Successor-State Recording (the conditional successor; v002 analogue of Phase 4bi-D);
- v002 feature-family successor-state recording (any form);
- multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K);
- multi-day v002 chronological-split-policy memo;
- diagnostics;
- ML training, model selection, feature ranking, meta-labeling;
- strategy specification, implementation, signal construction;
- backtest specification, plan, or execution;
- additional acquisition (no additional days; no additional symbols; no mark-price 30m / 4h / 5m; no aggTrades acquisition beyond the existing locked v002 90-day envelope);
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
- amending Phase 4ak M0, Phase 4al refined no-rescue rule, Phase 4aw `flip_research_eligible(...)` invariant, Phase 4bb-F canonical path policy, Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks, Phase 4bm-A-P1 thin-prompt context-management standard, Phase 4bm-D-P1 lightweight Claude Code workspace standard, Phase 4bm-E v002 derived-family decision, Phase 4bm-F v002 derived-family successor-state semantics, Phase 4bm-G v002 feature-boundary design, Phase 4bm-H v002 feature computation, Phase 4bm-I v002 feature-artefact structural QA, or Phase 4bm-J v002 feature-family eligibility-gate verdict;
- any successor phase whatsoever.

Each future phase requires its own separately authorized operator prompt under the Phase 4bk-A workflow standard, the Phase 4bl-F four-tier risk model, the Phase 4bm-A-P1 thin-prompt context-management standard, the Phase 4bm-D-P1 lightweight Claude Code workspace standard, the operator-report standard, and the merge-closeout standard.

---

## 19. Recommended state

**Remain paused.**

Phase 4bm-K records a policy-level admissibility decision and adds no new machine-readable marker. The operator's broader pause decision continues to apply. The recommended next state is remain paused.

---

## 20. Conditional next options (none authorized)

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | n/a | **recommended** |
| Future docs-and-local-gitignored-output **Phase 4bm-L — Multi-Day V002 Feature-Family Research-Use Successor-State Recording** (v002 analogue of Phase 4bi-D; would record a sibling successor-state JSON marking v002 Feature Stage-5 admissibility while preserving the v002 feature manifest byte-identically at SHA `512a0a54…`) | docs + local gitignored successor-state JSON | **NOT authorized by Phase 4bm-K** |
| Future multi-day v002 label-family phases (analogues of Phase 4bj-A through Phase 4bj-K) | docs + code + local gitignored output | **NOT authorized by Phase 4bm-K** |
| Future multi-day v002 chronological-split-policy memo | docs-only | **NOT authorized by Phase 4bm-K** |
| Additional acquisition / cross-symbol / mark-price / order-book / funding / OI / liquidation / cross-venue / authenticated APIs / private endpoints | docs + data | **NOT authorized by Phase 4bm-K** |
| Label computation, diagnostics, ML, strategy, backtests | code + data | **FORBIDDEN by Phase 4bm-K** |
| Paper / shadow / live / exchange-write / production keys | runtime | **FORBIDDEN by Phase 4bm-K** |

**No successor phase is authorized by Phase 4bm-K.**

---

## 21. Preserved boundaries

- **Retained verdict ledger** (preserved verbatim): H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.
- **Project locks** (preserved verbatim): §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF + nine reusable non-authorization blocks; Phase 4bm-A-P1 thin-prompt context-management standard; Phase 4bm-D-P1 lightweight Claude Code workspace standard; Phase 4am .. Phase 4bm-J results — all preserved verbatim.
- **No-rescue boundary**: Phase 4bm-K does not authorise any rescue of `G1`, `V2`, `C1`, `R2`, `F1`, `D1-A`, the regime-first lane, the microstructure / order-flow / liquidity-timing lane, the mark-price stop-domain lane, or any cooled-down family. v002 Feature Stage-5 admissibility is upstream of any hypothesis or strategy candidacy.
- **Feature-manifest immutability**: v002 feature manifest SHA `512a0a54be40d9c3a61fe0a032ce0301b7b60de60e3147362fa3a4bce633343d` must remain unchanged.
- **Phase 4bm-J gate-report immutability**: Phase 4bm-J gate report SHA `3c59dfaeb06c14cd1fdf4b589e17ecaa457277637d221bf35c3a69f42a898242` must remain unchanged.
- **Cross-artefact immutability**: all 14 upstream artefacts listed in §10 must remain byte-identical.
- **Phase 4aw flip-invariant**: `MicrostructureManifest.flip_research_eligible(...)` must continue to always raise.

---

## 22. Closeout / lock preservation

Phase 4bm-K is docs-only. No source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, raw artefacts, derived artefacts, feature artefacts, label artefacts, manifests, sidecars, gate reports, or successor-state artefacts have been or will be modified by this phase. The policy-level Stage-5 admissibility decision recorded above is text-only.

Phase 4bm-K preserves verbatim:

- the retained verdict ledger;
- the project locks;
- the M0 twelve-clause gate;
- the post-null cooldown rule;
- the cooled-down families list;
- the Phase 4al refined no-rescue rule;
- the Phase 4al §13 boundary and §14 hierarchy;
- the Phase 4aw `flip_research_eligible(...)` always-raises invariant;
- the Phase 4bb-F canonical path policy;
- the Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine reusable non-authorization blocks;
- the Phase 4bm-A-P1 thin-prompt context-management standard;
- the Phase 4bm-D-P1 lightweight Claude Code workspace standard;
- the Phase 4bm-E v002 derived-family Option B / Decision form 2 decision;
- the Phase 4bm-F v002 derived-family Stage-3 successor-state semantics;
- the Phase 4bm-G v002 feature-boundary design;
- the Phase 4bm-H v002 feature computation result;
- the Phase 4bm-I v002 feature-artefact structural QA verdict;
- the Phase 4bm-J v002 feature-family eligibility-gate verdict;
- every prior phase's recorded outcomes.

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bm-K.**
