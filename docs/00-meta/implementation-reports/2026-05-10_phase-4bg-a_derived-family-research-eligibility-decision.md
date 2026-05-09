# Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo

**Phase identity:** Phase 4bg-A — Derived-Family Research-Eligibility Decision Memo (docs-only).
**Date:** 2026-05-10.
**Branch:** `phase-4bg-a/derived-family-research-eligibility-decision`.
**Base:** `main` at the post-Phase-4bf state (Phase 4bf merge commit `cad383cd5e85dae6b96fa83650d211842d5e070f`; Phase 4bf merge-closeout commit at the head of `main` at the start of Phase 4bg-A).
**Status:** drafted; pending operator review.
**Phase type:** docs-only research-eligibility decision / governance memo.

---

## 1. Phase header

This memo answers a single question:

> Given the Phase 4bd Stage-0 normalized artefacts, the Phase 4be 60 / 60 structural QA PASS, and the Phase 4bf 55 / 55 derived-family gate PASS report, should the project authorize a future Stage-3 research-eligibility transition for the normalized derived family `microstructure_normalized_aggtrades_v001`, and under what exact constraints?

The memo is **docs-only**. It records a policy-level decision. It does not mutate any manifest, flip any `research_eligible` flag, transition any `eligibility_gate_status`, run any gate, modify any data file, compute any feature, or authorize any successor implementation.

The memo preserves every retained verdict, every project lock, and the Phase 4ak twelve-clause M0 admissibility gate, including the post-null cooldown rule and cooled-down families list.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bf merge commit | `cad383cd5e85dae6b96fa83650d211842d5e070f` |
| Phase 4bf merge-closeout file (on `main`) | `docs/00-meta/implementation-reports/2026-05-10_phase-4bf_merge-closeout.md` |
| Raw family | `microstructure_raw_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Derived family | `microstructure_normalized_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Symbol scope | BTCUSDT only |
| UTC date scope | `2025-01-15` |
| Event count | `1,681,098` |
| Phase 4bb-D raw gate report SHA256 | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bf derived-family gate report SHA256 | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Derived manifest SHA256 | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Normalized Parquet SHA256 | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Raw zip SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| `data/microstructure/` git status | gitignored at `.gitignore:85` (covers `gate-reports/normalized/` as a subpath) |

---

## 3. Inputs reviewed

- Phase 4az acquisition memo and closeout (one BTCUSDT 2025-01-15 daily archive).
- Phase 4ba 5-stage eligibility ladder (Stage-0 acquired → Stage-1 inspected → Stage-2 gate-passed → Stage-3 research-eligible → Stage-4 feature-cleared).
- Phase 4bb-A structural QA on the raw archive.
- Phase 4bb-B raw eligibility-gate execution-plan memo.
- Phase 4bb-C raw eligibility-gate primitive implementation.
- Phase 4bb-D raw eligibility-gate execution (45 / 45 PASS; report `96f09159…`).
- Phase 4bb-E successor-state policy (raw `research_eligible=false` permanent; original raw manifest immutable).
- Phase 4bc normalized-derived family design (19-column trade-record-level schema; no features / labels / signals).
- Phase 4bd-A normalization implementation plan.
- Phase 4bd normalization implementation and run (Stage-0 derived artefacts produced).
- Phase 4be normalized-dataset structural QA (60 / 60 PASS).
- Phase 4bf-A derived-family eligibility-gate design (55-check predeclared catalogue; 14 check groups; 18 fail-closed rules).
- Phase 4bf derived-family eligibility-gate implementation and execution (55 / 55 PASS; report `dd4e0c1c…`).
- Phase 4bf merge closeout (seven input artefacts byte-identical pre/post run; no_successor_authorization=True; research_eligible_after=False).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified.

---

## 4. Scope

In scope for this memo:

- evaluating the question: is Stage-3 research-eligibility admissible **in principle** for the normalized derived family at this point in the project record?
- selecting one of five docs-only decision options (A–E) and justifying the choice;
- defining the 15 minimum admissibility criteria for a Stage-3 transition;
- mapping the available evidence (Stages 0, 1, and report-level Stage 2) onto those criteria;
- recording the residual risks, the raw-family permanence rule, the derived-manifest immutability rule for this phase, the feature-boundary policy, and the ML / strategy boundary;
- recommending the conservative successor sequence without authorizing any successor.

---

## 5. Non-scope

This memo does **not**:

- modify any source code, test, script, configuration, dataset, manifest, or Phase 4bf gate report;
- run the normalizer, the raw eligibility gate, or the derived-family gate;
- generate a new gate report;
- create or modify any `data/microstructure/` artefact;
- create JSONL, Parquet, DuckDB, feature, label, signal, proxy, ML, or strategy artefacts;
- acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, or position-state columns;
- train ML, create strategy logic, run backtests or simulations;
- flip `research_eligible` on any family;
- transition `eligibility_gate_status` on any actual manifest;
- authorize Stage-4 feature-cleared status, feature computation, ML, strategy, or backtests;
- revise retained verdicts, change project locks, or amend M0;
- authorize Phase 4bg, Phase 4bh, Phase 4bi, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Stage-0 evidence review

**Stage 0 — acquired** (Phase 4ba ladder): the artefact has been produced and exists locally in the gitignored `data/microstructure/` namespace.

| Stage-0 artefact | Path | SHA256 |
| ---------------- | ---- | ------ |
| Normalized Parquet | `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Derived manifest | `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |

The derived manifest carries:

- `dataset_family = microstructure_normalized_aggtrades_v001`,
- `dataset_version = v001`,
- `symbol = BTCUSDT`,
- `utc_date = 2025-01-15`,
- `event_count = 1,681,098`,
- `research_eligible = false`,
- `eligibility_gate_status = pending`,
- governance labels including the raw lineage references (raw manifest SHA, raw zip SHA, Phase 4bb-D `report_id` and `report_sha256`),
- `feature_computation = forbidden`,
- `strategy_use = forbidden`.

The derived family is **reproducible locally** from the raw archive plus the Phase 4bd normalizer. It is gitignored, not committed.

**Stage-0 verdict:** evidence-positive.

---

## 7. Stage-1 evidence review

**Stage 1 — inspected** (Phase 4ba ladder): the Stage-0 artefact has been structurally inspected.

Phase 4be ran a 60-check structural QA inspection on the Stage-0 derived artefacts and recorded **60 / 60 PASS** with no FAIL, no ERROR, and no NOT_APPLICABLE.

Phase 4be confirmed:

- the normalized Parquet schema is exactly the 19 Phase 4bc canonical columns in canonical order;
- the schema contains no feature, label, signal, proxy, ML, or strategy column;
- row count = `1,681,098` = derived manifest `event_count`;
- `row_index` is contiguous `0..1,681,097` with no duplicates;
- `agg_trade_id` is non-decreasing and contains 1,681,098 unique values;
- first and last rows match the Phase 4bb-A structural QA bit-for-bit;
- first `transact_time_ms` = raw `start_time_ms` = `1,736,899,205,109`;
- last `transact_time_ms` = raw `end_time_ms` = `1,736,985,599,991`;
- all `transact_time_ms` lie inside the half-open UTC day `[2025-01-15T00:00:00.000Z, 2025-01-16T00:00:00.000Z)`;
- `price` and `quantity` are stored as Decimal-as-string (lossless; no float storage);
- `is_buyer_maker` is strict bool;
- per-row lineage columns are constant and reference the correct upstream evidence;
- the raw artefacts (raw manifest, raw zip, sidecar, acquisition log, Phase 4bb-D gate report) are byte-identical pre vs post inspection;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains in place.

**Stage-1 verdict:** evidence-positive.

---

## 8. Stage-2 report-level evidence review

**Stage 2 — gate-passed at report level** (Phase 4ba ladder; Phase 4bb-E policy): the Stage-1-inspected artefact has been put through a separately authorized eligibility-gate primitive and the gate emitted a PASS report. The actual manifest field has not been transitioned (this is exactly the Phase 4bb-E policy).

Phase 4bf executed the 55-check derived-family eligibility gate exactly under the Phase 4bf-A design and recorded:

- `overall_status = pass`;
- `len(checks) = 55`;
- PASS / FAIL / NOT_APPLICABLE / ERROR = 55 / 0 / 0 / 0;
- `len(invalid_window_candidates) = 0`;
- `research_eligible_after = False` (invariant for raw and derived raw-lineage families);
- `eligibility_gate_status_after = pass` (recommendation only; not written to any actual manifest);
- `no_successor_authorization = True` (invariant);
- 15 / 15 boundary confirmations `True`:
  - `no_backtest_run`
  - `no_credential_read`
  - `no_data_microstructure_write_outside_gate_reports`
  - `no_env_read`
  - `no_feature_computed`
  - `no_label_computed`
  - `no_manifest_mutation`
  - `no_mcp_or_graphify`
  - `no_ml_trained`
  - `no_network_io`
  - `no_normalization_written_outside_namespace`
  - `no_signal_computed`
  - `no_strategy_created`
  - `no_websocket`
  - `research_eligible_after_is_false_for_derived_family`.

The Phase 4bf gate report file is `data/microstructure/gate-reports/normalized/microstructure_normalized_aggtrades_v001__v001__1778368468053__29e3f550e28e.json` with SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` (paired `.sha256` sidecar present and matching). Both files are gitignored, not committed.

**Pre/post immutability evidence (Phase 4bf merge closeout, §4):** all seven input artefacts (derived manifest, normalized Parquet, raw manifest, raw zip, raw sidecar, acquisition log, Phase 4bb-D gate report) were byte-identical pre and post the Phase 4bf gate run.

**Stage-2 verdict:** evidence-positive at report level. The actual derived manifest's `eligibility_gate_status` remains `pending`; per Phase 4bb-E, the report-level PASS is governance evidence and does not by itself flip the manifest field.

---

## 9. Research-eligibility decision framework

The Phase 4ba ladder defines the asymmetry that controls this decision:

- `research_eligible = true` is permitted **only at Stage-3 and only on the derived family** (never on the raw family);
- the raw family `microstructure_raw_aggtrades_v001` remains permanently `research_eligible = false`;
- Stage-3 status is downstream of Stage-2 (gate-passed at the manifest level, recorded by a separately authorized successor-state phase);
- Stage-4 (feature-cleared) is downstream of Stage-3 and is required before any feature computation, ML training, strategy work, or backtest;
- every stage transition requires its own separately authorized phase.

The decision in this memo therefore distinguishes three orthogonal axes:

1. **Policy admissibility:** does the project record contain enough evidence to consider Stage-3 admissible *in principle* for the normalized derived family?
2. **Manifest mutation:** should this phase mutate the actual derived manifest's `research_eligible` and `eligibility_gate_status` fields?
3. **Practical research use:** does Stage-3 (if admissible) authorize feature computation, ML, or strategy work?

Phase 4bg-A is bounded to docs-only output. Axes 2 and 3 are categorically out of scope for this phase regardless of the answer to axis 1. Any "yes" on axis 1 is a recommendation for a future separately authorized phase, not a self-executing instruction.

---

## 10. Stage-3 admissibility criteria

To consider the normalized derived family research-eligible, the following 15 minimum criteria must hold (each must be verifiable from the project record):

| # | Criterion | Status |
| - | --------- | ------ |
| 1 | Stage-0 derived artefacts exist and are reproducible locally. | satisfied |
| 2 | Derived manifest exists and references raw lineage. | satisfied |
| 3 | Phase 4be structural QA passed 60 / 60. | satisfied |
| 4 | Phase 4bf derived-family gate passed 55 / 55. | satisfied |
| 5 | Phase 4bf report SHA256 is recorded and available locally: `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`. | satisfied |
| 6 | Derived manifest currently remains `research_eligible=false` and `eligibility_gate_status=pending`. | satisfied |
| 7 | Raw manifest currently remains `research_eligible=false` and `eligibility_gate_status=pending`. | satisfied |
| 8 | Raw family remains permanently ineligible for research use. | satisfied (Phase 4bb-E policy) |
| 9 | Invalid windows are empty or governed. Current value: `[]`. | satisfied |
| 10 | No features, labels, signals, proxies, ML, strategy, or backtest artefacts exist. | satisfied |
| 11 | No project lock would be loosened by Stage-3. | satisfied |
| 12 | No retained verdict would be revised by Stage-3. | satisfied |
| 13 | M0 remains binding prospectively. | satisfied (Phase 4ak adoption) |
| 14 | Stage-4 feature-boundary design is still required before feature computation. | satisfied (Stage-4 not authorized) |
| 15 | Any machine-readable manifest transition requires a separately authorized successor-state recording phase. | satisfied (Phase 4bb-E policy) |

All 15 admissibility criteria are satisfied at the policy level for the normalized derived family.

---

## 11. Evidence-to-criteria mapping

| Criterion | Evidence source | Specific record |
| --------- | --------------- | --------------- |
| 1 | Phase 4bd implementation report; Phase 4bd merge closeout; Phase 4bf merge closeout §4 | normalized Parquet `2b3d6978…`; derived manifest `f6f0d947…`; raw zip `f560c2e5…`; gitignored `data/microstructure/` |
| 2 | Phase 4bd derived manifest `governance_labels` | `source_dataset_family`, `source_dataset_version`, `source_manifest_sha256`, `source_raw_zip_sha256`, `source_gate_report_id`, `source_gate_report_sha256`, `source_gate_report_code_commit_sha`, `validator`, `stop_trigger_domain`, `feature_computation=forbidden`, `strategy_use=forbidden` |
| 3 | Phase 4be memo + closeout | 60 / 60 PASS, 0 FAIL, 0 ERROR, 0 NOT_APPLICABLE |
| 4 | Phase 4bf memo + closeout + merge closeout §7 | 55 / 55 PASS; check IDs `4bf.13.1` .. `4bf.13.55` |
| 5 | Phase 4bf real-run record; Phase 4bf merge closeout §7 | report SHA256 + paired sidecar match |
| 6 | live `git`-tracked status of `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` (gitignored locally) | `research_eligible=false`, `eligibility_gate_status=pending` |
| 7 | live `git`-tracked status of `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (gitignored locally) | `research_eligible=false`, `eligibility_gate_status=pending` |
| 8 | Phase 4bb-E §"Headline policy conclusions" | raw-family `research_eligible=false` permanent |
| 9 | Phase 4bf real-run summary; Phase 4bf merge closeout §7 | `len(invalid_window_candidates) = 0` |
| 10 | Phase 4bd-A scope; Phase 4bd implementation; Phase 4be schema check; Phase 4bf check 4bf.13.* feature-absence subgroup | no feature / label / signal / proxy column anywhere |
| 11 | Project locks listed in `current-project-state.md` | §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w preserved |
| 12 | Retained verdict ledger | H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 unchanged |
| 13 | Phase 4ak M0 governance adoption | M0 binding prospectively; post-null cooldown rule binding |
| 14 | Phase 4ba ladder | Stage-4 feature-cleared not yet reachable; not authorized |
| 15 | Phase 4bb-E policy | sibling successor-state manifest required for any machine-readable transition |

---

## 12. Remaining risks and limitations

The 15 admissibility criteria address artefact integrity and governance bookkeeping. They do **not** address statistical sufficiency for strategy research. The following limitations remain:

- **Symbol scope is one symbol** (BTCUSDT only). No cross-symbol coverage exists yet.
- **Date scope is one UTC day** (`2025-01-15`). No multi-day coverage exists yet. No multi-month or multi-year coverage exists.
- **Day type unknown.** The memo records no claim about whether `2025-01-15` was a typical, quiet, or volatile session. Any future research framing must carry this disclaim.
- **Research eligibility of the artefact is not the same as statistical sufficiency** for any specific research question.
- **No multi-day robustness exists.** A one-day sample cannot demonstrate stability or distributional properties that any future feature would depend on.
- **No cross-symbol robustness exists.** A one-symbol sample cannot generalize.
- **No feature set is authorized** (Stage-4 not authorized).
- **No label design exists** (no future-return scheme has been predeclared).
- **No leakage control design exists** (no temporal-leakage barrier has been specified for future feature work).
- **No ML split design exists** (no train / validation / OOS partitioning policy has been authored for microstructure-driven research).
- **No strategy hypothesis exists** under the Phase 4ak M0 admissibility gate that would consume this dataset.
- **No costed backtest exists** for any microstructure-driven hypothesis (the §11.6 8 bps cost lock applies regardless).
- **No live / paper / shadow readiness exists.** None is approached by Stage-3.
- **Stage-3, if recommended, only permits governed research use of this clean artefact.** It does not license any claim of edge.

These limitations are not blockers to a policy-level Stage-3 admissibility decision. They are explicit constraints on what such a decision means.

---

## 13. Invalid-window status

`invalid_windows` for the normalized derived manifest: `[]`.

`invalid_windows` for the raw manifest: `[]`.

Phase 4bf real-run produced `len(invalid_window_candidates) = 0`. No invalid windows are governed-but-excluded; none exist for this single archive.

If any future acquisition produces non-empty invalid windows, those windows must be enumerated explicitly in the affected manifest, governed by Phase 3r §8 / Phase 4j §11 precedent, and propagated by the Phase 4bd normalizer's `propagate_invalid_windows(...)` helper. **Phase 4bg-A does not amend invalid-window governance.**

---

## 14. Raw-family policy

Per Phase 4bb-E:

- the raw family `microstructure_raw_aggtrades_v001` is **permanently** `research_eligible=false`;
- the original Phase 4az raw manifest is **immutable**;
- raw-family gate PASS reports are report-level governance evidence, not manifest mutations;
- any future raw-state policy marker (Phase 4bb-G, not authorized) would record a *sibling* successor-state manifest preserving the original v001 manifest byte-identically and preserving `research_eligible=false`.

**Phase 4bg-A does not amend the raw-family policy.** The raw family remains permanently `research_eligible=false`.

---

## 15. Derived-family manifest policy

For the normalized derived family `microstructure_normalized_aggtrades_v001`:

- the actual derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` **must remain unchanged in Phase 4bg-A**;
- Phase 4bg-A does not flip `research_eligible`; the field remains `false`;
- Phase 4bg-A does not transition `eligibility_gate_status`; the field remains `pending`;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains in place;
- any machine-readable transition of these fields (whether on the original manifest, a successor-state sibling, or a registry) requires a separately authorized successor-state recording phase.

If a future Phase 4bg-B (Derived-Family Successor-State Policy / Recording memo) is separately authorized, that phase would specify the exact record format (sibling successor-state manifest preserving the original byte-identically vs. an external registry vs. a new pinned version), and it would still not authorize feature computation, ML, strategy, or backtests.

---

## 16. Feature-boundary policy

Stage-4 (feature-cleared) is **not** authorized by Phase 4bg-A and is not implied by any policy-level Stage-3 admissibility decision in this memo.

Specifically, the following remain forbidden until a separately authorized Stage-4 feature-boundary design memo (a future Phase 4bh-A, not authorized) and a separately authorized feature implementation phase (a future Phase 4bh, not authorized):

- computing returns, alpha, edge, opportunity rate;
- computing taker imbalance, sweep detection, aggressive-flow score;
- computing spread, depth, liquidity, slippage, order-flow, execution-quality proxies;
- computing regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position-state columns;
- creating any column outside the 19-column Phase 4bc trade-record-level schema in the canonical normalized family;
- creating any sibling derived family that contains feature columns;
- writing any feature, label, signal, or proxy under `data/microstructure/`;
- writing JSONL, DuckDB, feature tables, labels, signals, or analytical datasets that are derived from this artefact.

The feature-boundary policy is downstream governance. Phase 4bg-A only confirms it is the next governance step that must precede feature computation if the project ever proceeds further on this lane.

---

## 17. ML / strategy boundary

Phase 4bg-A does **not** authorize:

- creating ML models;
- training ML on the normalized derived family;
- creating any strategy candidate (named or otherwise);
- creating any hypothesis-spec memo, strategy-spec memo, backtest-plan memo, or backtest-execution phase that consumes this dataset;
- running any backtest;
- running any simulation that uses this dataset as input;
- running any paper / shadow / live / exchange-write workflow.

The Phase 4ak M0 admissibility gate (twelve clauses) and the post-null cooldown rule remain binding for any future strategy hypothesis. M0.7 (edge-rate plausibility separate from opportunity-rate) and M0.10 (forbidden-rescue / anti-reduction check with named closest rescue trap) are particularly binding for any microstructure-driven candidate.

Cooled-down families (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane) remain cooled down. Phase 4bg-A neither reopens nor amends any cooled-down family classification.

---

## 18. Research-use permission boundary

Even at policy-level Stage-3, "research use" is bounded:

- governed offline inspection of the normalized Parquet for descriptive understanding of the dataset itself (row distributions, agg-trade-id ranges, timestamp coverage) is allowed;
- writing those inspection results into a future docs-only memo, with cited SHAs, is allowed;
- producing any derivative dataset, feature, label, signal, proxy, return, or backtest from this artefact is **not** allowed under Phase 4bg-A;
- producing any derivative that would imply a strategy claim is **not** allowed under Phase 4bg-A;
- producing any derivative dataset that would carry `feature_computation` or `strategy_use` outside `forbidden` is **not** allowed under Phase 4bg-A.

This boundary mirrors Phase 4bb-A (structural QA), Phase 4be (Stage-1 structural QA), and Phase 4bf (Stage-2 gate execution) — each of which inspected the artefact and produced docs without computing features.

---

## 19. Decision options considered

| Option | Description | Evaluation |
| ------ | ----------- | ---------- |
| A | Do not authorize Stage-3 even in principle yet; require more evidence or more data first. | Defensible but conservative beyond the evidence. The 15 admissibility criteria are satisfied at the policy level. The remaining open questions (multi-day, multi-symbol robustness; feature design) belong to *later* governance phases (Stage-4 feature-boundary and / or further acquisition), not to a policy-level Stage-3 admissibility decision. Choosing A would be an under-recognition of the available evidence. |
| B | Authorize Stage-3 in principle for the normalized derived family, but do not mutate the manifest in this phase; require a separately authorized successor-state recording phase before any machine-readable `research_eligible` transition. | Matches the Phase 4ba ladder, the Phase 4bb-E successor-state policy, and the Phase 4bg-A non-scope. Records a precise governance position without overstepping. |
| C | Authorize a limited, docs-only research-use policy while keeping the manifest false; require Stage-4 feature-boundary design before any feature computation. | Functionally consistent with B (which already implies the Stage-4 prerequisite). C is admissible as a wording variant; B is more precise about the manifest boundary, so B is preferred. |
| D | Reject immediate Stage-3 and proceed instead to additional acquisition planning. | Out of scope: Phase 4bg-A is not an acquisition phase. Any acquisition would require a separately authorized acquisition memo. |
| E | Mutate the derived manifest now. | Forbidden: Phase 4bg-A is docs-only. Mutation requires a separately authorized successor-state recording phase. |

---

## 20. Recommended decision

**Option B.** Decision form 2 wording is adopted verbatim:

> **Stage-3 is admissible in principle at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists.**

Specifically:

- the **raw family remains `research_eligible=false` permanently** (Phase 4bb-E policy preserved verbatim);
- the **actual derived manifest remains `research_eligible=false`** in Phase 4bg-A, and the **actual `eligibility_gate_status` remains `pending`**;
- **no data, feature, ML, strategy, or backtest work is authorized** by Phase 4bg-A;
- **the next safe phase is one of: a successor-state policy / recording memo (a future Phase 4bg-B), or a feature-boundary design memo (a future Phase 4bh-A), or remain paused;** no immediate feature computation is authorized;
- this admissibility is policy-level only and bounded by the Phase 4ba ladder; Stage-4 (feature-cleared) remains unauthorized and Stage-4 admissibility is not predetermined by Phase 4bg-A.

The Phase 4ak M0 admissibility gate, post-null cooldown rule, cooled-down families list, and refined no-rescue rule (Phase 4al §13 / §14) remain binding.

---

## 21. Required successor-state handling, if any

If a future Phase 4bg-B is separately authorized, that phase **must**:

1. preserve the original Phase 4bd derived manifest at `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json` byte-identically;
2. preserve the actual `research_eligible` field at `false` on the original manifest;
3. preserve the actual `eligibility_gate_status` field at `pending` on the original manifest;
4. record any successor state via a sibling successor-state manifest (or equivalently disciplined registry), preserving the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant on the original;
5. only transition the derived family's *successor* `eligibility_gate_status` from `pending` to `pass` (recording the Phase 4bf PASS); only the *successor-recorded* `research_eligible` may carry `true` — and even there, only if the successor-state phase is explicitly authorized to do so;
6. cite the Phase 4bf gate report SHA256 `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` and the Phase 4bb-D raw gate report SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` verbatim;
7. preserve the `governance_labels` keys and add a successor-state phase reference;
8. write only under `data/microstructure/`, never to existing tracked paths;
9. be gitignored, never committed under `data/microstructure/`;
10. not authorize Stage-4, feature computation, ML, strategy, backtests, paper / shadow / live, exchange-write, production keys, authenticated APIs, or private endpoints.

**Phase 4bg-A does not authorize Phase 4bg-B.**

---

## 22. Required future feature-boundary phase

Even after a hypothetical Phase 4bg-B records the derived family as Stage-2 / Stage-3 at the successor-state level, **no feature computation may begin until** a separately authorized Phase 4bh-A — Feature-Boundary Design Memo (docs-only, no computation) — has:

1. predeclared the exact future feature schema and its 19+N column layout;
2. predeclared the temporal-leakage barrier (e.g., point-in-time-valid only; no future bars referenced);
3. predeclared the M0 admissibility status of the implied research lane (M0.1 source; M0.7 edge-rate plausibility; M0.10 closest rescue trap and structural distinguishing argument);
4. predeclared the post-null cooldown status of the implied lane (microstructure / order-flow / liquidity-timing is currently `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
5. predeclared the test plan for the future implementation phase (Phase 4bh, not authorized);
6. predeclared the manifest and dataset-family naming for any feature-bearing derived family;
7. predeclared the validator / governance-label policy for any feature-bearing derived family;
8. predeclared the integration with §11.6 cost realism and §1.7.3 project-level locks;
9. preserved the Phase 4aw flip-invariant on every manifest involved;
10. not authorize feature computation by itself.

**Phase 4bg-A does not authorize Phase 4bh-A.**

---

## 23. Fail-closed rules

The following are binding on any future phase that consumes Phase 4bg-A as input:

1. **Path discipline.** No write may occur outside `data/microstructure/`. The Phase 4bd normalized Parquet path, the Phase 4bd derived manifest path, and the Phase 4bf gate report path must remain byte-immutable unless a separately authorized phase reproduces the artefact deterministically with documented evidence.
2. **Manifest-mutation discipline.** The original Phase 4bd derived manifest must not be mutated. Any successor state must be recorded in a sibling artefact preserving the original byte-identically.
3. **Raw-family discipline.** The raw family `microstructure_raw_aggtrades_v001` remains `research_eligible=false` permanently. No phase may flip it.
4. **Stage-3 discipline.** Stage-3 admissibility at policy level is *not* a license for feature computation, ML, strategy, or backtests. Stage-4 authorization is required for those.
5. **Stage-4 discipline.** Stage-4 authorization is not implied by Stage-3 admissibility. A separately authorized feature-boundary memo is required before Stage-4 even becomes a candidate.
6. **Network discipline.** No phase consuming Phase 4bg-A as input may call public endpoints, Binance APIs, authenticated REST, private endpoints, user stream, WebSocket, or read `.env` / credentials / `.mcp.json` without separately authorized scope.
7. **Static-import discipline.** The Phase 4bf static-scan policy on `derived_gate_*` modules continues. Future microstructure modules must remain free of forbidden imports and tokens.
8. **Cooldown discipline.** Post-null cooldown classifications for cooled-down families are not loosened by any policy-level Stage-3 admissibility decision in this memo.
9. **Cost-realism discipline.** §11.6 = 8 bps per side and round-trip = 16 bps remain binding for any future strategy candidate that ever consumes microstructure-derived features.
10. **No-rescue discipline.** Phase 4al refined no-rescue rule remains binding. No retained verdict (R3 / R2 / F1 / D1-A / V2 / G1 / C1) may be revisited, rescued, or relabelled on the basis of Phase 4bg-A.

---

## 24. What this phase proves

- that the project record contains enough evidence to consider Stage-3 admissibility *in principle* at policy level for the normalized derived family `microstructure_normalized_aggtrades_v001`;
- that the 15 minimum admissibility criteria are satisfied at the policy level;
- that the actual derived manifest remains `research_eligible=false` and `eligibility_gate_status=pending` throughout Phase 4bg-A;
- that the raw family remains `research_eligible=false` permanently;
- that no manifest, dataset, gate report, or governance memo was mutated by Phase 4bg-A;
- that no successor phase is authorized.

---

## 25. What this phase does not prove

- that the artefact is statistically sufficient for any specific research question;
- that any feature, label, signal, or proxy is admissible;
- that Stage-4 is admissible, in principle or otherwise;
- that any microstructure / order-flow / liquidity-timing strategy hypothesis is admissible (the lane remains `NOT_RECOMMENDED_NOW` per Phase 4ak adoption);
- that any cooled-down family may be reopened;
- that paper / shadow / live / exchange-write may begin;
- that production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation are admissible.

---

## 26. Preserved boundaries

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
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D / 4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf results — all preserved.

---

## 27. Recommended future options

| Option | Type | Status |
| ------ | ---- | ------ |
| **Primary** — remain paused | docs-only / no work | recommended |
| **Conditional next, if continuing and Stage-3 is recommended in principle** — Phase 4bg-B Derived-Family Research-Eligibility Successor-State Policy / Recording memo | docs-only or docs-and-local-gitignored-output; no feature computation | NOT authorized by this memo |
| **Conditional next, if keeping manifest false but preparing research** — Phase 4bh-A Feature-Boundary Design memo | docs-only; no computation | NOT authorized by this memo |
| **Conditional later** — Phase 4bh Feature Schema / Feature Computation implementation | code + docs; only after Stage-4 authorization | NOT authorized by this memo |
| **Conditional cleanup** — Phase 4bb-F Gate Report Output Path Hygiene | code + docs; before any repeated raw gate execution | NOT authorized by this memo |
| **Conditional raw policy marker** — Phase 4bb-G Raw Manifest Successor-State Recording | docs-only or docs-and-local-gitignored-output | NOT authorized by this memo |
| Acquisition (additional days / symbols / data families) | docs + data | NOT authorized; not in scope of Phase 4bg-A |
| Feature computation, ML, strategy, backtests | code + data | FORBIDDEN by Phase 4bg-A |
| Paper / shadow / live / exchange-write / production keys | runtime | FORBIDDEN by Phase 4bg-A |

---

## 28. Closeout / lock preservation

Phase 4bg-A is docs-only and produces:

- this memo (`docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_derived-family-research-eligibility-decision.md`);
- the Phase 4bg-A closeout (`docs/00-meta/implementation-reports/2026-05-10_phase-4bg-a_closeout.md`);
- a narrow Phase 4bg-A paragraph + new "Current phase:" block in `docs/00-meta/current-project-state.md` (prior Phase 4bf block preserved as historical context).

No source code, tests, scripts, configs, READMEs, MCP files, runtime configuration, manifests, raw artefacts, gate reports, or `.gitignore` entries were modified.

The `data/microstructure/` namespace is untouched. The Phase 4bd derived manifest, the normalized Parquet, the raw manifest, the raw zip, the raw sidecar, the acquisition log, the Phase 4bb-D gate report, and the Phase 4bf gate report all remain byte-identical.

The decision recorded in §20 is **Option B**: Stage-3 is admissible in principle at policy level for the normalized derived family, but no manifest mutation occurs in this phase, and a separately authorized successor-state recording phase is required before any machine-readable `research_eligible=true` marker exists. The raw family remains permanently `research_eligible=false`. Feature computation remains forbidden until a separately authorized Stage-4 feature-boundary design memo and a separately authorized feature implementation phase. ML / strategy / backtest work remains forbidden under the Phase 4ak M0 admissibility gate, the post-null cooldown rule, and the cooled-down families list.

**Recommended state: remain paused.** No next phase authorized.
