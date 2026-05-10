# Phase 4bg-B — Derived-Family Research-Eligibility Successor-State Policy / Recording Memo

**Phase identity:** Phase 4bg-B — Derived-Family Research-Eligibility Successor-State Policy / Recording Memo.
**Phase type:** docs-and-local-gitignored-output successor-state recording phase.
**Date:** 2026-05-10.
**Branch:** `phase-4bg-b/derived-family-research-eligibility-successor-state`.
**Base:** `main` at the post-Phase-4bg-A merge-closeout state (`db9742a638e6393f3c5d30d1e94148e727368cbb`); Phase 4bg-A merge commit `f8bfbc16c852c6c93023f80bb28ab70fc0af24e8` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.
**Recorded outcome:** **Outcome 1 — Record successor state now.** One local gitignored successor-state JSON artefact and its paired SHA256 sidecar have been created under `data/microstructure/successor-state/`. Original derived manifest, raw manifest, and all upstream artefacts remain byte-identical. No tracked data file was changed.

---

## 1. Phase header

This memo records the controlled successor-state policy for the normalized derived family `microstructure_normalized_aggtrades_v001` and the creation of one local gitignored successor-state artefact that records the derived family as **Stage-3 research-eligible at successor-state level only**, while preserving the original derived manifest's `research_eligible=false / eligibility_gate_status=pending` state byte-identically and preserving the raw family's permanent `research_eligible=false` policy.

The phase is bounded:

- the original derived manifest is **not mutated**;
- the original raw manifest is **not mutated**;
- the normalized Parquet is **not mutated**;
- the Phase 4bb-D and Phase 4bf gate reports are **not mutated**;
- no source code, test, script, configuration, README, or `.gitignore` is modified;
- no feature, label, signal, proxy, ML, strategy, or backtest artefact is created;
- no data is acquired;
- no public endpoint, Binance API, WebSocket, private endpoint, credential, `.env`, or `.mcp.json` is used;
- Stage-4 (feature-cleared) is **not** authorized;
- no successor phase is authorized.

The recorded successor-state distinguishes between the original-manifest field (`research_eligible=false`, immutable per Phase 4bb-E policy applied to the derived family) and the successor-state field (`successor_research_eligible=true`, recorded only in the sibling successor-state artefact at policy level).

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bg-A merge commit (ancestor of `main`) | `f8bfbc16c852c6c93023f80bb28ab70fc0af24e8` |
| Phase 4bg-A merge-closeout file (on `main`) | `docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_merge-closeout.md` |
| `main == origin/main` (start of Phase 4bg-B) | `db9742a638e6393f3c5d30d1e94148e727368cbb` |
| Raw family | `microstructure_raw_aggtrades_v001` |
| Raw manifest `research_eligible` / `eligibility_gate_status` | `false` / `pending` (immutable; permanent) |
| Derived family | `microstructure_normalized_aggtrades_v001` |
| Derived manifest `research_eligible` / `eligibility_gate_status` (original) | `false` / `pending` (immutable in this phase) |
| Successor-state file (created locally; gitignored) | `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` |
| Successor-state SHA256 | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Successor-state size | `2,679 bytes` |
| Sidecar | `…json.sha256` (158 bytes; matches) |
| `data/microstructure/successor-state/` git status | gitignored at `.gitignore:85` (parent `data/microstructure/` rule) |
| Phase 4bf derived-family gate report SHA256 | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bb-D raw gate report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Derived manifest SHA256 | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Normalized Parquet SHA256 | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Raw manifest SHA256 | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |

---

## 3. Inputs reviewed

- Phase 4az acquisition memo and closeout (one BTCUSDT 2025-01-15 daily archive).
- Phase 4ba 5-stage eligibility ladder (Stage-0 acquired → Stage-1 inspected → Stage-2 gate-passed → Stage-3 research-eligible → Stage-4 feature-cleared).
- Phase 4bb-D raw eligibility-gate execution (45 / 45 PASS; report `96f09159…`).
- Phase 4bb-E successor-state policy (raw family permanently `research_eligible=false`; original raw manifest immutable).
- Phase 4bc normalized-derived family design.
- Phase 4bd-A normalization implementation plan and Phase 4bd implementation + Stage-0 derived artefact production.
- Phase 4be normalized-dataset structural QA (60 / 60 PASS).
- Phase 4bf-A derived-family eligibility-gate design (55-check predeclared catalogue).
- Phase 4bf derived-family eligibility-gate implementation and execution (55 / 55 PASS; report `dd4e0c1c…`; report-level Stage-2 only).
- Phase 4bg-A research-eligibility decision memo (Option B / Decision form 2; Stage-3 admissible at policy level; no manifest mutation).
- Phase 4bg-A merge closeout (records merge into `main`; preserves original manifests).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified other than the new gitignored successor-state JSON + sidecar created by Phase 4bg-B.

---

## 4. Scope

In scope for this phase:

- recording the controlled successor-state policy for the normalized derived family;
- creating exactly one local gitignored successor-state JSON artefact and its paired SHA256 sidecar;
- documenting the schema of that artefact;
- documenting the immutability boundary that separates the original manifest's fields from the successor-state record's fields;
- preserving all retained verdicts, project locks, M0 admissibility gate, post-null cooldown rule, cooled-down families list, and refined no-rescue rule.

---

## 5. Non-scope

This phase does **not**:

- mutate any manifest's `research_eligible` or `eligibility_gate_status` field;
- create a replacement derived manifest, replacement raw manifest, or any sibling manifest beyond the single successor-state JSON described in §11;
- modify any source code, test, script, configuration, README, `pyproject.toml`, `.gitignore`, or governance memo;
- run the normalizer, the raw eligibility gate, or the derived-family eligibility gate;
- generate a new gate report;
- create JSONL, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquire data; call public endpoints, Binance APIs, authenticated REST, or private endpoints; open WebSockets; use credentials; read or create `.env`; create `.mcp.json`; or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- train ML, create strategy logic, run backtests or simulations;
- authorize Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests;
- revise retained verdicts, change project locks, or amend M0;
- authorize Phase 4bh-A, Phase 4bh, Phase 4bi, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bg-A decision dependency

Phase 4bg-A recorded **Option B / Decision form 2**:

> Stage-3 is admissible in principle at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.

Phase 4bg-B is that separately authorized successor-state recording phase. Phase 4bg-B converts the Phase 4bg-A policy-level admissibility into a single machine-readable gitignored record without mutating the original derived manifest or any upstream artefact. The Phase 4bg-A decision text remains binding on Phase 4bg-B; the original derived manifest stays `research_eligible=false / eligibility_gate_status=pending`.

---

## 7. Successor-state recording objective

- record the Phase 4bg-A admissibility decision in machine-readable form;
- preserve the Phase 4bb-E successor-state pattern (sibling successor-state file; original manifest byte-immutable; raw family permanently `research_eligible=false`);
- ensure that any future tooling that wishes to interpret the derived family as Stage-3 must read the successor-state artefact, not the original manifest;
- preserve the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant for both raw and derived original manifests;
- record sufficient lineage in the successor-state JSON to verify upstream evidence (Phase 4bb-D raw gate, Phase 4be structural QA, Phase 4bf derived gate, Phase 4bg-A decision, Phase 4bg-A merge commit);
- ensure that Stage-4 is **not** implied by this record;
- ensure that no feature computation, ML, strategy, or backtest is licensed by this record.

---

## 8. Original-manifest immutability policy

The original derived manifest `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` is treated as **byte-immutable** by Phase 4bg-B and any successor consuming Phase 4bg-B's output:

- `research_eligible` remains `false`;
- `eligibility_gate_status` remains `pending`;
- the SHA256 `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` is verified before and after the Phase 4bg-B successor-state write;
- the Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved (Phase 4bg-B never invokes that helper);
- no successor-state phase, gate phase, or normalization phase may overwrite the original derived manifest as a Phase 4bg-B-licensed action.

---

## 9. Raw-family permanence policy

Per Phase 4bb-E:

- the raw family `microstructure_raw_aggtrades_v001` is **permanently** `research_eligible=false`;
- the original Phase 4az raw manifest is **immutable**;
- the Phase 4bg-B successor-state JSON records `raw_family_research_eligible=false` and `raw_family_eligibility_gate_status=pending` to preserve this permanence in the machine-readable record.

Phase 4bg-B does not amend the raw-family policy. The raw family remains permanently `research_eligible=false`.

---

## 10. Derived-family successor-state policy

For the normalized derived family `microstructure_normalized_aggtrades_v001`:

- the original derived manifest is byte-immutable per §8;
- a single sibling successor-state artefact may exist under `data/microstructure/successor-state/`;
- the successor-state artefact records the policy-level Stage-3 admissibility decision in machine-readable form;
- the successor-state artefact's `successor_research_eligible=true` field is **not** equivalent to the original manifest's `research_eligible` field; downstream tooling must distinguish the two;
- the successor-state artefact is gitignored, not committed, and reproducible from this memo's schema (§12) plus the upstream lineage SHAs;
- any future overwrite or replacement of the successor-state artefact requires a separately authorized phase (e.g., Phase 4bg-C); Phase 4bg-B itself does not authorize re-writes;
- creation of a *second* successor-state artefact for the same `(dataset_family, dataset_version)` pair is **not** authorized by Phase 4bg-B.

---

## 11. Successor-state artefact path

Created (Outcome 1):

- file: `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`
- size: `2,679 bytes`
- SHA256: `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`
- paired sidecar: `…json.sha256` (158 bytes; same SHA256, matches)
- gitignored under `.gitignore:85: data/microstructure/`
- not committed; not staged

The `data/microstructure/successor-state/` directory is created by this phase as a sibling to `gate-reports/`, `manifests/`, `normalized/`, and `raw/`. It is gitignored under the same parent rule.

---

## 12. Successor-state schema

The created JSON artefact contains, at minimum, the following keys (verbatim per the brief):

| Key | Value |
| --- | ----- |
| `schema_version` | `"v001"` |
| `phase_id` | `"4bg-B"` |
| `dataset_family` | `"microstructure_normalized_aggtrades_v001"` |
| `dataset_version` | `"v001"` |
| `successor_state_kind` | `"research_eligibility_successor_state"` |
| `successor_stage` | `"Stage-3"` |
| `successor_research_eligible` | `true` |
| `successor_eligibility_gate_status` | `"pass"` |
| `original_manifest_path` | `"data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json"` |
| `original_manifest_sha256` | `"f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9"` |
| `original_manifest_research_eligible` | `false` |
| `original_manifest_eligibility_gate_status` | `"pending"` |
| `raw_family` | `"microstructure_raw_aggtrades_v001"` |
| `raw_family_research_eligible` | `false` |
| `raw_family_eligibility_gate_status` | `"pending"` |
| `raw_manifest_sha256` | `"a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201"` |
| `raw_zip_sha256` | `"f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e"` |
| `normalized_parquet_sha256` | `"2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa"` |
| `phase_4bb_d_raw_gate_report_id` | `"microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c"` |
| `phase_4bb_d_raw_gate_report_sha256` | `"96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423"` |
| `phase_4be_structural_qa_result` | `"60/60 PASS"` |
| `phase_4bf_derived_gate_report_id` | `"microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e"` |
| `phase_4bf_derived_gate_report_sha256` | `"dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6"` |
| `phase_4bf_derived_gate_result` | `"55/55 PASS"` |
| `phase_4bg_a_decision` | `"Option B / Decision form 2"` |
| `phase_4bg_a_merge_commit` | `"f8bfbc16c852c6c93023f80bb28ab70fc0af24e8"` |
| `feature_computation` | `"forbidden"` |
| `labels` | `"forbidden"` |
| `ml` | `"forbidden"` |
| `strategy` | `"forbidden"` |
| `backtest` | `"forbidden"` |
| `acquisition` | `"unauthorized"` |
| `stage_4_feature_cleared` | `false` |
| `no_successor_authorization` | `true` |
| `created_at_unix_ms` | `1778372319041` |
| `docs_commit_sha_at_creation` | `"db9742a638e6393f3c5d30d1e94148e727368cbb"` |
| `boundary_confirmations` | nested object — see §14 |

---

## 13. Evidence cited by successor state

The successor-state JSON cites the following upstream evidence verbatim:

- Phase 4bb-D raw gate report (`report_id microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c`; SHA `96f09159…`; 45 / 45 PASS);
- Phase 4be structural QA (60 / 60 PASS);
- Phase 4bf derived-family gate report (`report_id microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e`; SHA `dd4e0c1c…`; 55 / 55 PASS);
- Phase 4bg-A decision (Option B / Decision form 2);
- Phase 4bg-A merge commit `f8bfbc16c852c6c93023f80bb28ab70fc0af24e8`;
- normalized Parquet SHA `2b3d6978…`;
- derived manifest SHA `f6f0d947…`;
- raw manifest SHA `a371edd4…`;
- raw zip SHA `f560c2e5…`.

---

## 14. Boundary confirmations

The successor-state JSON's `boundary_confirmations` object records the following, all `True`:

```text
original_derived_manifest_preserved              True
original_raw_manifest_preserved                  True
raw_family_research_eligible_remains_false       True
derived_original_research_eligible_remains_false True
no_feature_computation                           True
no_label_computation                             True
no_ml                                            True
no_strategy                                      True
no_backtest                                      True
no_acquisition                                   True
no_network                                       True
no_credentials                                   True
no_mcp_or_graphify                               True
no_project_lock_change                           True
no_retained_verdict_change                       True
```

---

## 15. Stage interpretation

Per the Phase 4ba ladder:

- Stage-0 — acquired (Phase 4bd; satisfied);
- Stage-1 — inspected (Phase 4be; satisfied);
- Stage-2 — gate-passed at report level (Phase 4bf; satisfied);
- **Stage-3 — research-eligible at successor-state level (Phase 4bg-B; recorded only in the gitignored successor-state JSON)**;
- Stage-4 — feature-cleared (NOT authorized; requires separately authorized future Phase 4bh-A feature-boundary design memo and a separate feature implementation phase).

The Stage-3 admissibility recorded by Phase 4bg-B is at successor-state level. The original derived manifest's `eligibility_gate_status` remains `pending`. Any tool that reads only the original manifest must continue to treat the derived family as Stage-1-equivalent (inspected). Tools that consume the successor-state JSON may read the family as Stage-3 for governed research use only (§16).

---

## 16. Research-use interpretation

Even with Stage-3 successor-state recording, "research use" is bounded:

- governed offline inspection of the normalized Parquet for descriptive understanding of the dataset itself (row distributions, agg-trade-id ranges, timestamp coverage) is allowed under future docs-only memos, with cited SHAs and explicit no-feature disclaim;
- producing any derivative dataset, feature, label, signal, proxy, return, or backtest from this artefact is **not** allowed under Phase 4bg-B;
- producing any derivative that would imply a strategy claim is **not** allowed under Phase 4bg-B;
- producing any derivative dataset that would carry `feature_computation` or `strategy_use` outside `forbidden` is **not** allowed under Phase 4bg-B.

---

## 17. Feature-boundary policy

Stage-4 (feature-cleared) is **not** authorized by Phase 4bg-B. Specifically, the following remain forbidden until a separately authorized Stage-4 feature-boundary design memo (a future Phase 4bh-A, not authorized) and a separately authorized feature implementation phase (a future Phase 4bh, not authorized):

- computing returns, alpha, edge, opportunity rate;
- computing taker imbalance, sweep detection, aggressive-flow score;
- computing spread, depth, liquidity, slippage, order-flow, execution-quality proxies;
- computing regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position-state columns;
- creating any column outside the 19-column Phase 4bc trade-record-level schema in the canonical normalized family;
- creating any sibling derived family that contains feature columns;
- writing any feature, label, signal, or proxy under `data/microstructure/`;
- writing JSONL, DuckDB, feature tables, labels, signals, or analytical datasets that are derived from this artefact.

---

## 18. ML / strategy / backtest boundary

Phase 4bg-B does **not** authorize:

- creating ML models;
- training ML on the normalized derived family;
- creating any strategy candidate (named or otherwise);
- creating any hypothesis-spec memo, strategy-spec memo, backtest-plan memo, or backtest-execution phase that consumes this dataset;
- running any backtest;
- running any simulation that uses this dataset as input;
- running any paper / shadow / live / exchange-write workflow.

The Phase 4ak M0 admissibility gate (twelve clauses) and the post-null cooldown rule remain binding for any future strategy hypothesis. Cooled-down families (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane) remain cooled down. Phase 4bg-B neither reopens nor amends any cooled-down family classification.

---

## 19. Validation and immutability evidence

| Check | Result |
| ----- | ------ |
| `git check-ignore -v data/microstructure/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/gate-reports/normalized/` | `.gitignore:85: data/microstructure/` |
| `git check-ignore -v data/microstructure/successor-state/` | `.gitignore:85: data/microstructure/` |
| Pre-write SHA — derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Post-write SHA — derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` (MATCH) |
| Pre-write SHA — raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Post-write SHA — raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` (MATCH) |
| Pre-write SHA — normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Post-write SHA — normalized Parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` (MATCH) |
| Pre-write SHA — Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Post-write SHA — Phase 4bf gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` (MATCH) |
| Pre-write SHA — raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Post-write SHA — raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` (MATCH) |
| Successor-state SHA256 | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Sidecar SHA256 (matches) | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| `ruff check .` (post-write) | All checks passed |
| `pytest tests/research/microstructure/` | 492 passed |
| Whole-repo `pytest` | 1275 passed, 2 failed (only the pre-existing simulation `KeyError: 'trade_count'` failures; identical to pre-Phase-4bg-B baseline) |
| `mypy src/prometheus` (strict) | Success: no issues found in 101 source files |
| `git diff --check` | clean |
| `git status` (tracked) | only the three new docs are staged at commit time; no `data/` change |
| Manifest state (raw, post-write) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Manifest state (derived, post-write) | `research_eligible=false`, `eligibility_gate_status=pending` |
| Phase 4aw `flip_research_eligible(...)` always-raises invariant | preserved (never invoked by Phase 4bg-B) |

Phase 4bg-B introduces zero new test regressions.

---

## 20. What this phase proves

- that the Phase 4bg-A admissibility decision can be recorded in machine-readable form without mutating the original derived manifest or any upstream artefact;
- that the controlled successor-state pattern (sibling artefact preserving original byte-identically) is implementable for the derived family with the same discipline Phase 4bb-E specified for the raw family;
- that the original derived manifest's `research_eligible=false / eligibility_gate_status=pending` state is preserved byte-identically by Phase 4bg-B;
- that the raw family remains permanently `research_eligible=false`;
- that the Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved end-to-end;
- that the local artefact and its sidecar are gitignored, not committed, reproducible from documented inputs, and identifiable by SHA256.

---

## 21. What this phase does not prove

- that the artefact is statistically sufficient for any specific research question;
- that any feature, label, signal, or proxy is admissible;
- that Stage-4 is admissible, in principle or otherwise;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible.

---

## 22. Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A results — all preserved.

---

## 23. Recommended future options

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | recommended |
| **Conditional next, after Outcome 1 (this phase)** — Phase 4bh-A Feature-Boundary Design memo | docs-only; no computation | NOT authorized by this memo |
| **Conditional later** — Phase 4bh Feature Schema / Feature Computation implementation | code + docs; only after Stage-4 authorization | NOT authorized by this memo |
| **Conditional cleanup** — Phase 4bb-F Gate Report Output Path Hygiene | code + docs; before any repeated raw gate execution | NOT authorized by this memo |
| **Conditional raw policy marker** — Phase 4bb-G Raw Manifest Successor-State Recording | docs-only or docs-and-local-gitignored-output | NOT authorized by this memo |
| Acquisition (additional days / symbols / data families) | docs + data | NOT authorized; not in scope |
| Feature computation, ML, strategy, backtests | code + data | FORBIDDEN |
| Paper / shadow / live / exchange-write / production keys | runtime | FORBIDDEN |

---

## 24. Closeout / lock preservation

Phase 4bg-B is docs-and-local-gitignored-output and produces:

- this memo (`docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_derived-family-research-eligibility-successor-state.md`);
- the Phase 4bg-B closeout (`docs/00-meta/implementation-reports/2026-05-10_phase-4bg-b_closeout.md`);
- a narrow Phase 4bg-B paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md` (prior Phase 4bg-A block preserved as historical context);
- one local gitignored successor-state JSON artefact under `data/microstructure/successor-state/` and its paired SHA256 sidecar (NOT committed; reproducible from this memo's schema and the cited input SHAs).

No source code, tests, scripts, configs, READMEs, MCP files, runtime configuration, manifests, raw artefacts, gate reports, or `.gitignore` entries were modified. The `data/microstructure/` namespace is untouched outside the new `data/microstructure/successor-state/` subdirectory.

The original Phase 4bd derived manifest, the normalized Parquet, the raw manifest, the raw zip, the raw sidecar, the acquisition log, the Phase 4bb-D gate report, and the Phase 4bf gate report all remain byte-identical.

The recorded outcome is **Outcome 1**: one local gitignored successor-state JSON + paired SHA256 sidecar created at `data/microstructure/successor-state/microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json` (SHA256 `8bcc7d01…`). Original derived manifest remains `research_eligible=false / eligibility_gate_status=pending`. Raw family remains permanently `research_eligible=false`. Feature computation, ML, strategy, backtests, and acquisition all remain unauthorized. No successor phase is authorized by Phase 4bg-B.

**Recommended state: remain paused.**
