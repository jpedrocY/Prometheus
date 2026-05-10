# Phase 4bi-C — Feature-Family Research-Use / ML-Use Decision Memo

**Phase identity:** Phase 4bi-C — Feature-Family Research-Use / ML-Use Decision Memo (docs-only).
**Date:** 2026-05-10.
**Branch:** `phase-4bi-c/feature-family-research-ml-use-decision`.
**Base:** `main` at the post-Phase-4bi-B merge-closeout state. Phase 4bi-B merge commit `046ec90ddfefb3c59164740eaf572ce104fb060f` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.
**Phase type:** docs-only research-use / ML-use decision memo.

---

## 1. Phase header

This memo answers a single question:

> Given the Phase 4bh feature-family implementation, the Phase 4bi-A 67/67 + 18/18 structural QA PASS, and the Phase 4bi-B 70/70 feature-family eligibility gate PASS report, should the project authorize a future Stage-5 research-use / ML-use admissibility recording for the feature family `microstructure_features_aggtrades_v001`, and under what exact constraints?

The memo is **docs-only**. It records a Stage-5 policy decision. It does not mutate the feature manifest, flip any `research_eligible` flag, transition any `eligibility_gate_status`, run any gate, modify any data file, compute any feature, create any label, train any model, generate any signal, or authorize any successor implementation.

The memo preserves every retained verdict, every project lock, the Phase 4ak twelve-clause M0 admissibility gate (post-null cooldown rule + cooled-down families list + memo template), the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, the Phase 4j §11 metrics OI-subset partial-eligibility rule, and every prior phase outcome.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bi-B merge commit | `046ec90ddfefb3c59164740eaf572ce104fb060f` |
| Phase 4bi-B merge-closeout file (on `main`) | `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-b_merge-closeout.md` |
| Raw family | `microstructure_raw_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Derived family | `microstructure_normalized_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Feature family | `microstructure_features_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Symbol scope | BTCUSDT only |
| UTC date scope | `2025-01-15` |
| Feature row count | `1,681,098` |
| Schema columns | 61 (45 features + 16 lineage) |
| Feature config hash | `49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77` |
| Phase 4bi-B feature-gate report SHA256 | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Feature parquet SHA256 | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest SHA256 | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| `data/microstructure/` git status | gitignored at `.gitignore:85` (covers `gate-reports/features/` as a subpath) |

---

## 3. Inputs reviewed

- Phase 4az acquisition memo and closeout (one BTCUSDT 2025-01-15 daily archive).
- Phase 4ba 5-stage data-eligibility ladder.
- Phase 4bb-A through 4bb-E raw eligibility-gate design, execution, and successor-state governance.
- Phase 4bc derived-family schema design.
- Phase 4bd-A normalization implementation plan.
- Phase 4bd normalization implementation and run.
- Phase 4be normalized-dataset structural QA.
- Phase 4bf-A derived-family eligibility-gate design.
- Phase 4bf derived-family eligibility-gate execution (55 / 55 PASS).
- Phase 4bg-A derived-family research-eligibility decision (Stage-3 admissible in principle at policy level only; no manifest mutation).
- Phase 4bg-B derived-family research-eligibility successor-state policy / recording memo.
- Phase 4bh-A feature-boundary design memo.
- Phase 4bh-B feature schema finalization memo (61-column schema; 4-window matrix; deferred 30s/5m).
- Phase 4bh feature schema / feature computation implementation (135 / 135 validation PASS).
- Phase 4bi-A feature artefact structural QA (67 / 67 explicit PASS; 18 / 18 spot-check PASS; same-T tie-break PASS; `validate_feature_dataset` 135 / 135 PASS).
- Phase 4bi-B feature-family eligibility-gate implementation and execution (70 / 70 PASS; report SHA `aa5d29c2…`; `validate_feature_dataset` re-run `overall_status=pass`; `failed_checks=[]`).
- Phase 4bi-B merge closeout (nine input artefacts byte-identical pre/post run; `no_successor_authorization=True`; `research_eligible_after=False`; `feature_manifest_research_eligible_after=False`; `feature_manifest_eligibility_gate_status_after=pending`; `stage_5_authorized=False`; `stage_5_research_or_ml_use=False`).

No prior memo's text was modified. No artefact under `data/microstructure/` was modified.

---

## 4. Scope

In scope for this memo:

- evaluating the question: is Stage-5 research-use / ML-use admissibility admissible **in principle** for the feature family at this point in the project record?
- selecting one of three docs-only decision outcomes (1, 2, 3) and justifying the choice;
- defining the Stage-5 policy meaning and its strict boundaries;
- mapping the available evidence (Stages 1, 2, 3, and report-level Stage-4) onto policy admissibility;
- recording the residual risks, the feature-manifest immutability rule for this phase, the label boundary, the strategy / backtest boundary, the acquisition boundary, and the M0 / no-rescue boundary;
- recommending the conservative successor sequence without authorizing any successor.

---

## 5. Non-scope

This memo does **not**:

- modify any source code, test, script, configuration, dataset, manifest, or Phase 4bi-B gate report;
- run the normalizer, the raw eligibility gate, the derived-family gate, the feature kernel, or the feature-family eligibility gate;
- generate a new gate report;
- create or modify any `data/microstructure/` artefact;
- create JSONL, Parquet, DuckDB, feature, label, target, signal, proxy, ML, or strategy artefacts;
- acquire data, call public endpoints, call Binance APIs, open WebSockets, use private endpoints, request credentials, read or create `.env`, create `.mcp.json`, or enable MCP / Graphify;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, decision score, or entry / exit signal;
- train ML, create label or target, design strategy logic, or run backtests / simulations;
- flip `research_eligible` on any family;
- transition `eligibility_gate_status` on any actual manifest;
- create a successor-state artefact;
- authorize Stage-5 implementation (a separately authorized Phase 4bi-D would be required);
- revise retained verdicts, change project locks, or amend M0;
- authorize Phase 4bi-D, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 4 canonical, Phase 5, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bi-B dependency

This memo depends entirely on Phase 4bi-B's locked outputs:

- Phase 4bi-B is merged into `main` at merge commit `046ec90ddfefb3c59164740eaf572ce104fb060f`.
- The Phase 4bi-B gate report at `data/microstructure/gate-reports/features/microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json` exists locally with SHA256 `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` (gitignored; not committed).
- The Phase 4bi-B gate report records `overall_status=pass`, 70 / 70 PASS, 0 FAIL, 0 ERROR, 0 NOT_APPLICABLE, with all 17 boundary confirmations true and `validate_feature_dataset` re-run also `overall_status=pass` with `failed_checks=[]`.
- The Phase 4bi-B gate report records the result invariants `research_eligible_after=False`, `feature_manifest_research_eligible_after=False`, `feature_manifest_eligibility_gate_status_after=pending`, `stage_5_authorized=False`, `stage_5_research_or_ml_use=False`, `no_successor_authorization=True`.
- The Phase 4bi-B merge-closeout file is present on `main`.

This memo does not re-derive that evidence; it cites it as locked input.

---

## 7. Stage-5 decision objective

The Phase 4ba ladder, as extended by Phase 4bh-A, defines a feature-family ladder:

- **Feature Stage-1** — implementation merged (Phase 4bh).
- **Feature Stage-2** — local feature artefacts exist with manifest (Phase 4bh).
- **Feature Stage-3** — structurally QA-passed at memo level (Phase 4bi-A).
- **Feature Stage-4** — feature-family eligibility gate PASS at report level (Phase 4bi-B).
- **Feature Stage-5** — research-use / ML-use admissibility decision (this phase).
- **Feature Stage-6** (or successor-state recording) — sibling successor-state artefact, only by separate authorization.

This memo's task is to decide whether Stage-5 is admissible **in principle at policy level**, given the evidence on record. The memo does not produce a machine-readable Stage-5 marker; it answers the policy question only.

---

## 8. Evidence table

| Evidence layer | Phase | Result | Status |
| -------------- | ----- | ------ | ------ |
| Stage-0 raw acquisition | 4az | one BTCUSDT 2025-01-15 daily archive | strict integrity gate PASS |
| Stage-1 raw inspection | 4bb-A | structural QA on raw archive | PASS |
| Stage-2 raw eligibility gate | 4bb-D | 45 / 45 PASS | report SHA `96f09159…` |
| Stage-2 raw policy | 4bb-E | raw `research_eligible=false` permanent | governance binding |
| Derived schema | 4bc | trade-record-level only; no features | governance binding |
| Derived implementation | 4bd-A / 4bd | normalized parquet produced | 27 / 27 PASS |
| Derived structural QA | 4be | 60 / 60 PASS | structural QA |
| Derived eligibility gate | 4bf-A / 4bf | 55 / 55 PASS | report SHA `dd4e0c1c…` |
| Derived research-eligibility decision | 4bg-A | Stage-3 admissible at policy level | policy decision |
| Derived successor-state | 4bg-B | sibling successor-state JSON SHA `8bcc7d01…` | recorded |
| Feature boundary | 4bh-A | feature classes & forbidden lists | governance binding |
| Feature schema | 4bh-B | 61-column schema; 4 windows; deferred 30s/5m | governance binding |
| Feature implementation | 4bh | feature kernel run; 135 / 135 validation PASS | feature artefacts produced |
| Feature artefact structural QA | 4bi-A | 67 / 67 + 18 / 18 PASS; same-T PASS; validate 135 / 135 | structural QA |
| Feature-family eligibility gate | 4bi-B | 70 / 70 PASS; validate 0 failed | report SHA `aa5d29c2…` |

All evidence is internally consistent. No verdict has been revised. No project lock has been loosened.

---

## 9. Feature artefact state

- **Feature parquet:** `data/microstructure/features/microstructure_features_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet` SHA256 `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`. Verified at the start of Phase 4bi-C.
- **Feature manifest:** `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` SHA256 `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`. Verified at the start of Phase 4bi-C.
- **Phase 4bi-B feature-family eligibility gate report:** SHA256 `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`; size 30 696 bytes; paired `.sha256` sidecar matches.
- **Coverage:** 1 681 098 rows; one symbol; one UTC date; 61 columns in canonical schema order; deferred 30s and 5m windows absent.

---

## 10. Feature manifest state

The feature manifest's on-disk state is identical to the Phase 4bh-recorded state:

- `dataset_family = microstructure_features_aggtrades_v001`
- `dataset_version = v001`
- `feature_schema_version = v001`
- `symbol = BTCUSDT`
- `utc_date = 2025-01-15`
- `row_count = 1681098`
- `invalid_windows = []`
- `research_eligible = false`
- `eligibility_gate_status = pending`
- `governance_labels.phase_id = 4bh`
- `governance_labels.feature_computation = allowed_by_phase_4bh`
- `governance_labels.labels = forbidden`
- `governance_labels.ml = forbidden`
- `governance_labels.strategy = forbidden`
- `governance_labels.backtest = forbidden`
- `governance_labels.acquisition = unauthorized`
- `governance_labels.stop_trigger_domain = trade_price_backtest_candidate`

Phase 4bi-C does not modify this file. Phase 4bi-C does not transition `eligibility_gate_status`. Phase 4bi-C does not flip `research_eligible`. The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved.

---

## 11. Eligibility-gate state

The Phase 4bi-B feature-family eligibility gate is the authoritative report-level evidence:

- `overall_status = pass`
- `checks_total = 70`, `checks_pass = 70`, `checks_fail = 0`, `checks_error = 0`, `checks_not_applicable = 0`
- `validate_feature_dataset.overall_status = pass`; `validate_feature_dataset.failed_checks = []`
- 17 / 17 boundary confirmations true
- `research_eligible_after = false`
- `feature_manifest_research_eligible_after = false`
- `feature_manifest_eligibility_gate_status_after = pending`
- `stage_5_authorized = false`
- `stage_5_research_or_ml_use = false`
- `no_successor_authorization = true`

The gate report intentionally encodes Stage-5 as not-yet-authorized. That is consistent with this phase's role: the gate report carries the Stage-4 PASS evidence but explicitly defers Stage-5 to a separately authorized successor.

---

## 12. Research-use interpretation

"Research-use admissible in principle at policy level" means:

- the feature family has cleared every prior gate at every prior layer of evidence;
- the feature family's lineage to public, integrity-gated raw data is byte-verifiable on the local machine;
- the feature family's schema, semantics, and quality flags are consistent with the Phase 4bh-B locked contract;
- the feature family is therefore admissible to be considered as the input substrate of a future research workflow whose first step would be label-boundary design followed by Stage-5 successor-state recording.

Crucially, this **does not** mean any of the following:

- the feature family has predictive validity;
- the feature family produces a tradable signal;
- the feature family will pass an out-of-sample evaluation;
- the feature family covers more than one symbol or more than one UTC date;
- the feature family carries a strategy hypothesis;
- a backtest is permitted;
- a simulation is permitted;
- a retained verdict is revised;
- a project lock is loosened;
- M0 admissibility is bypassed.

The feature family's research-use admissibility at policy level is a governance state, not an empirical claim about edge.

---

## 13. ML-use interpretation

"ML-use admissible in principle at policy level" means:

- if a future Phase 4bi-D records the Stage-5 successor-state marker (separately authorized), and
- if a future Phase 4bj-A records a Label Boundary / Target Definition memo (separately authorized),
- then a separately authorized future ML-experimentation phase could be considered.

Crucially, this **does not** mean any of the following at this time:

- no model may be trained;
- no label may be created;
- no target may be created;
- no train / validation / test split may be created;
- no strategy may be derived from the features;
- no backtest may be run;
- no symbol or date expansion may occur;
- no ML hyperparameter search may run;
- no ML metric may be reported;
- no ML output may be persisted under `data/microstructure/` or anywhere else in the repository.

ML-use policy admissibility is upstream of any ML implementation. The forbidden state remains: `governance_labels.ml = forbidden` on the feature manifest.

---

## 14. Label boundary

Label design requires a separate future phase. Labels remain forbidden in Phase 4bi-C.

The locked label boundary, preserved verbatim from Phase 4bh-A:

- forbidden classes: future returns, next-window movement, future high / low, future realized volatility, future volume, label columns, target columns, strategy signals, entry-exit flags, PnL, MFE, MAE, R-multiple, equity curve, position state, alpha, edge, prediction, model embeddings, learned representations, post-hoc-fitted thresholds;
- forbidden rule: any feature row may use only `transact_time_ms <= T`;
- forbidden rule: no centered windows, no full-day-distribution normalization unless explicitly causal, no z-scores using future data;
- forbidden rule: any future labels must obey chronological validation, no leakage, no strategy rescue;
- forbidden rule: any conversion of MFE / MAE / time-to-event / target-before-stop / realized-R into rule candidates without a fresh ex-ante hypothesis and a separately authorized strategy-spec memo.

Phase 4bi-C does not weaken any of these constraints.

A future Label Boundary / Target Definition memo (provisional name **Phase 4bj-A**) would be the only path to even consider label structure, and only after Stage-5 successor-state recording is in place.

---

## 15. Strategy / backtest boundary

Strategy logic and backtests remain forbidden. The locked strategy / backtest boundary:

- no strategy hypothesis may be derived from feature inspection;
- no rule may be conditioned on Phase 4r / Phase 4l / Phase 4x forensic numbers;
- no backtest may be run;
- no simulated trade lifecycle may be produced;
- no entry / exit logic may be designed;
- no PnL, MFE, MAE, R-multiple, equity, position state, alpha, edge, prediction, model score, decision score, or strategy output may be computed;
- no microstructure-flavoured rule may bypass the M0 admissibility gate (`Phase 4ak`);
- no rescue of a cooled-down family (`G1`, `V2`, `C1`, `R2`, `F1`, `D1-A`, regime-first lane, microstructure / order-flow / liquidity-timing lane, mark-price stop-domain lane) is implied or authorized;
- the Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy remain binding.

Phase 4bi-C is governance, not strategy. Stage-5 admissibility at policy level cannot be repurposed as a strategy permission slip.

---

## 16. Acquisition boundary

Acquisition remains unauthorized.

- no additional days, no additional symbols, no mark-price 30m / 4h / 5m, no aggTrades acquisition beyond the existing locked one-day archive;
- no public endpoint calls, no Binance API calls, no WebSocket, no private endpoints, no user stream, no listenKey, no credentials, no `.env`, no `.mcp.json`, no MCP, no Graphify;
- no scripted re-download;
- no rerun of the normalizer, the raw eligibility gate, the derived-family gate, the feature kernel, or the feature-family eligibility gate;
- no replacement parquet, no replacement manifest, no replacement gate report, no replacement successor-state artefact;
- no creation of new dataset versions.

The acquisition envelope on the project's record remains exactly: BTCUSDT 2025-01-15 raw aggTrades archive (Phase 4az), normalized parquet (Phase 4bd), feature parquet (Phase 4bh), and the three gate reports (Phase 4bb-D raw; Phase 4bf derived; Phase 4bi-B feature). Nothing else is authorized.

---

## 17. M0 / no-rescue boundary

The Phase 4ak twelve-clause M0 mechanism-admissibility gate remains binding:

- M0.1 — mechanism source declared;
- M0.2 — non-price-only / structurally distinct source requirement;
- M0.3 — baseline-superiority theory vs H0 and R3;
- M0.4 — rejection-topology distance (R2 / F1 / D1-A / V2 / G1 / C1) with closest-prior-failure trap structurally distinguished;
- M0.5 — cost-realism plausibility under §11.6 = 8 bps per side;
- M0.6 — opportunity-rate plausibility derived from theoretical content;
- M0.7 — edge-rate plausibility separate from opportunity-rate;
- M0.8 — data availability and integrity feasibility;
- M0.9 — governance compatibility with all binding locks;
- M0.10 — forbidden-rescue and anti-reduction check;
- M0.11 — pre-backtest falsification criteria;
- M0.12 — post-null cooldown check + non-authorization clause.

The post-null cooldown rule remains binding. The cooled-down families list (price-only single-symbol directional continuation; cross-sectional trend / relative-strength symbol-selection under Phase 4ai descriptors; derivatives-context directional lane; microstructure / order-flow / liquidity-timing lane; mark-price stop-domain / execution-realism lane) remains binding.

The Phase 4al refined no-rescue rule (§9 distinguishes forbidden parameter tuning / threshold retrofitting from allowed predeclared forensic audits + §13 future scope boundary + §14 lower-timeframe hierarchy) remains binding.

Stage-5 policy admissibility is **upstream** of M0. M0 still applies to any future hypothesis, label, target, strategy, or backtest. Stage-5 admissibility does not bypass M0.

---

## 18. Decision options considered

Three docs-only outcomes were defined:

- **Outcome 1 — Stage-5 admissible in principle at policy level, successor-state required.** Recognises that the evidence chain (Phase 4az → 4bb-D → 4bd → 4be → 4bf → 4bg-A → 4bg-B → 4bh-A → 4bh-B → 4bh → 4bi-A → 4bi-B) is complete and consistent at policy level, while preserving the feature manifest's `research_eligible=false` and `eligibility_gate_status=pending` until a separately authorized Phase 4bi-D records a sibling successor-state marker.
- **Outcome 2 — Stage-5 deferred.** Selected only if there is a missing evidence link or an unresolved risk that prevents Stage-5 admissibility at this time.
- **Outcome 3 — Stage-5 rejected.** Selected only if there is a structural reason the feature family is not admissible at all (e.g., schema violation, lineage break, governance violation, leakage, label leakage, ungoverned ratio-column access, etc.).

The deciding criteria were:

1. Phase 4bi-B gate report present and SHA matches recorded value — **PASS** (`aa5d29c2…`).
2. Gate report `overall_status=pass` with 70 / 70 PASS — **PASS**.
3. `validate_feature_dataset` re-run `overall_status=pass`; `failed_checks=[]` — **PASS**.
4. Feature parquet SHA matches recorded value — **PASS** (`618d9b86…`).
5. Feature manifest SHA matches recorded value — **PASS** (`624e8c5e…`).
6. Feature manifest remains `research_eligible=false` and `eligibility_gate_status=pending` — **PASS**.
7. Phase 4bh / 4bi-A / 4bi-B evidence is internally consistent — **PASS**.
8. All non-scope and no-rescue boundaries remain preserved — **PASS**.

All eight criteria are satisfied. There is no missing evidence link and no unresolved structural risk.

---

## 19. Selected outcome

**Outcome 1 (Decision form 1):**

> **Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for the feature family `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.**

Specifically:

- the feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` remains `research_eligible=false` and `eligibility_gate_status=pending` throughout Phase 4bi-C and after;
- no machine-readable Stage-5 marker exists yet;
- a future Phase 4bi-D would be required to create a sibling successor-state artefact (analogous to Phase 4bg-B's derived-family successor-state JSON), without overwriting or mutating the feature manifest;
- the original feature manifest must remain byte-identical at SHA `624e8c5e…` until separate authorisation;
- labels remain forbidden;
- targets remain forbidden;
- ML remains forbidden (`governance_labels.ml = forbidden`);
- strategy remains forbidden (`governance_labels.strategy = forbidden`);
- backtests remain forbidden (`governance_labels.backtest = forbidden`);
- acquisition remains unauthorized (`governance_labels.acquisition = unauthorized`);
- stage_5 policy admissibility is **not** a strategy hypothesis, **not** a predictive claim, **not** an edge claim, **not** a backtest permission, **not** an M0 bypass, **not** a successor authorization, and **not** a permission to acquire more data.

This is the conservative outcome and the correct outcome given that all eight deciding criteria are satisfied.

---

## 20. Machine-readable state interpretation

After Phase 4bi-C, the on-disk machine-readable state is unchanged from immediately before Phase 4bi-C:

| Object | Field | Value |
| ------ | ----- | ----- |
| feature manifest | `research_eligible` | `false` |
| feature manifest | `eligibility_gate_status` | `pending` |
| feature manifest | `governance_labels.labels` | `forbidden` |
| feature manifest | `governance_labels.ml` | `forbidden` |
| feature manifest | `governance_labels.strategy` | `forbidden` |
| feature manifest | `governance_labels.backtest` | `forbidden` |
| feature manifest | `governance_labels.acquisition` | `unauthorized` |
| derived manifest | `research_eligible` | `false` |
| derived manifest | `eligibility_gate_status` | `pending` |
| raw manifest | `research_eligible` | `false` |
| raw manifest | `eligibility_gate_status` | `pending` |
| Phase 4bi-B gate report | `research_eligible_after` | `false` |
| Phase 4bi-B gate report | `feature_manifest_research_eligible_after` | `false` |
| Phase 4bi-B gate report | `feature_manifest_eligibility_gate_status_after` | `pending` |
| Phase 4bi-B gate report | `stage_5_authorized` | `false` |
| Phase 4bi-B gate report | `stage_5_research_or_ml_use` | `false` |
| Phase 4bi-B gate report | `no_successor_authorization` | `true` |

The policy-level Stage-5 admissibility decision recorded by this memo is text-only. Any tool that wishes to interpret the feature family as Stage-5-admissible must read this memo's selected outcome explicitly. No automatic flag flip is permitted.

---

## 21. Required successor-state policy

If the operator later authorises a Stage-5 successor-state recording phase (provisional name **Phase 4bi-D**), it must obey the following constraints, mirroring the Phase 4bg-B precedent:

- it must be docs-and-local-gitignored-output only;
- it must produce **exactly one** sibling successor-state JSON artefact under a gitignored namespace such as `data/microstructure/successor-state/` (path subject to Phase 4bb-F output-path-hygiene resolution if that phase is ever authorised);
- it must produce a paired `.sha256` sidecar matching the artefact's bytes;
- it must cite the Phase 4bi-B gate report id and SHA verbatim;
- it must cite the feature parquet, feature manifest, normalized parquet, derived manifest, raw manifest, and raw zip SHAs verbatim;
- it must cite this Phase 4bi-C memo as the policy-decision evidence;
- it must record `successor_research_eligible=true` and `successor_eligibility_gate_status=pass` only on the sibling successor-state artefact, not on the feature manifest;
- it must explicitly preserve the original feature manifest byte-identically (SHA `624e8c5e…`);
- it must explicitly preserve `research_eligible=false` and `eligibility_gate_status=pending` on the original feature manifest;
- it must explicitly record `stage_5_research_or_ml_use_authorized = true` (label name subject to Phase 4bi-D design) **only at the successor-state artefact level**, not at the manifest level;
- it must record `labels=forbidden`, `targets=forbidden`, `ml=forbidden`, `strategy=forbidden`, `backtest=forbidden`, `acquisition=unauthorized` until a further separately authorized phase changes those;
- it must not flip `research_eligible` on the feature manifest or any prior manifest;
- it must not transition `eligibility_gate_status` on any actual manifest;
- it must not authorize labels, targets, signals, ML, strategy, backtests, or acquisition;
- it must not authorize Phase 4bj-A label boundary memo by itself;
- it must not amend M0;
- it must not bypass the Phase 4al refined no-rescue rule;
- it must preserve every retained verdict and project lock verbatim;
- it must not authorize any further successor by itself.

Stage-5 successor-state recording is **machine-readable evidence of policy admissibility**, not a label-design or strategy authorization.

---

## 22. What this phase proves

- the Phase 4bh / 4bi-A / 4bi-B evidence chain is internally consistent at policy level;
- Phase 4bi-B's 70 / 70 PASS is sufficient evidence for the policy-level admissibility question this memo answers;
- the feature family is structurally suitable for future research-use / ML-use admissibility consideration;
- a future Stage-5 successor-state recording is governance-supportable;
- no upstream artefact has changed; nine-artefact byte-identical immutability is preserved across the entire arc;
- the M0 admissibility gate, post-null cooldown rule, refined no-rescue rule, and feature-family boundary all remain binding.

---

## 23. What this phase does not prove

- the feature family is **not** proven to have predictive validity;
- the feature family is **not** proven to produce a tradable signal;
- the feature family's evidence chain is **not** generalised to additional symbols or additional UTC dates beyond the one-day BTCUSDT 2025-01-15 cell;
- no label has been designed;
- no target has been defined;
- no train / validation / test split has been designed;
- no strategy hypothesis has been admitted under M0;
- no backtest has been run;
- no edge claim is made;
- no baseline-superiority claim is made;
- no out-of-sample evaluation is implied;
- no successor authorization is granted by Phase 4bi-C alone.

The Phase 4bi-C decision is policy admissibility only.

---

## 24. Preserved boundaries

- **Retained verdict ledger** (preserved verbatim): H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.
- **Project locks** (preserved verbatim): §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B, 4bh, 4bi-A, 4bi-B preserved verbatim.
- **No-rescue boundary**: Phase 4bi-C does not authorise any rescue of `G1`, `V2`, `C1`, `R2`, `F1`, `D1-A`, the regime-first lane, the microstructure / order-flow / liquidity-timing lane, the mark-price stop-domain lane, or any cooled-down family. Stage-5 admissibility is upstream of any hypothesis or strategy candidacy.
- **Feature-manifest immutability**: feature manifest SHA `624e8c5e…` must remain unchanged.
- **Feature-parquet immutability**: feature parquet SHA `618d9b86…` must remain unchanged.
- **Phase 4bi-B gate-report immutability**: Phase 4bi-B gate report SHA `aa5d29c2…` must remain unchanged.
- **Cross-artefact immutability**: nine upstream artefacts (raw manifest, raw zip, derived manifest, normalized parquet, Phase 4bb-D gate report, Phase 4bf gate report, Phase 4bg-B successor-state, feature parquet, feature manifest) must remain byte-identical.
- **Phase 4aw flip-invariant**: `MicrostructureManifest.flip_research_eligible(...)` must continue to always raise.

---

## 25. Recommended future options

- **Primary**: remain paused.
- **Conditional next** (Outcome 1 implies; NOT authorised by Phase 4bi-C): future docs-and-local-gitignored-output **Phase 4bi-D** — Feature-Family Successor-State Recording (records Stage-5 research/ML admissibility in a sibling successor-state artefact while preserving the feature manifest byte-identically).
- **Conditional later, after Stage-5 successor-state** (NOT authorised by Phase 4bi-C): future docs-only **Phase 4bj-A** — Label Boundary / Target Definition Memo. This is the next admissibility layer upstream of any ML-use implementation.
- **Conditional cleanup** (NOT authorised by Phase 4bi-C): future code-and-docs **Phase 4bb-F** — Gate Report Output Path Hygiene (only before any future repeated raw or feature-family gate execution).
- **Conditional raw-policy marker** (NOT authorised by Phase 4bi-C): future docs-only or docs-and-local-gitignored-output **Phase 4bb-G** — Raw Manifest Successor-State Recording (preserves the raw manifest byte-identically and preserves `research_eligible=false`).

**FORBIDDEN** options:

- verdict revision;
- lock revision;
- parameter optimization;
- strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid);
- M0 amendment derived from Phase 4bi-C reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any actual manifest from this phase alone;
- transitioning `eligibility_gate_status` on any actual manifest from this phase alone;
- creating labels / targets / signals / ML / strategy / backtests from this phase alone;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

Phase 4 (canonical) remains unauthorized. Phase 4bi-D / Phase 4bj / Phase 4bj-A / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized.

---

## 26. Closeout / lock preservation

Phase 4bi-C is docs-only. No source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, raw artefacts, derived artefacts, feature artefacts, manifests, sidecars, gate reports, or successor-state artefacts have been or will be modified by this phase. The policy-level Stage-5 admissibility decision recorded above is text-only.

Phase 4bi-C preserves verbatim:

- the retained verdict ledger;
- the project locks;
- the M0 twelve-clause gate;
- the post-null cooldown rule;
- the cooled-down families list;
- the Phase 4al refined no-rescue rule;
- the Phase 4al §13 boundary and §14 hierarchy;
- the Phase 3v §8 stop-trigger-domain governance;
- the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- the Phase 4j §11 metrics OI-subset partial-eligibility rule;
- every prior phase's recorded outcomes.

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bi-C.**
