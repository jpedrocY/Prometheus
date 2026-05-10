# Phase 4bj-A — Label Boundary / Target Definition Memo

Date: 2026-05-10
Phase: 4bj-A
Phase type: docs-only label-boundary / target-definition memo
Branch: phase-4bj-a/label-boundary-target-definition
Base: main at the post-Phase-4bi-D merge-closeout state (`bddc84dd8219295f9f0b809e248c13af66fb0d66`)
Author: Prometheus operator-supervised implementation, dual-AI workflow
Status: draft (docs-only; text-only)

---

## 1. Current state

Phase 4bi-D is merged to main and recorded a machine-readable Stage-5
admissibility marker as a sibling successor-state artefact under
`data/microstructure/successor-state/`. The actual feature manifest at
`data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`
continues to carry `research_eligible: false` and
`eligibility_gate_status: pending`. The successor-state artefact's
`successor_research_ml_admissible: true` and `successor_research_eligible: true`
fields apply only to the sibling artefact, not to any actual manifest.

No labels exist. No targets exist. No label namespace exists. No label
manifest exists. No ML model exists. No strategy exists. No backtest has
been authorized or run on this feature family.

Phase 4bj-A is the first phase in the Phase 4bj family. It defines the
**label boundary** and the **future target-definition policy** for the
Stage-5-admissible feature family, **without implementing anything**.

## 2. Inputs reviewed

The following artefacts were inspected read-only:

- Phase 4bi-D successor-state JSON
  - path:
    `data/microstructure/successor-state/`
    `microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json`
  - SHA256:
    `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
  - paired `.sha256` sidecar: matches
  - selected outcome: Outcome 1 / Decision form 1 (Phase 4bi-C)
- Phase 4bi-B feature-family gate report
  - path:
    `data/microstructure/gate-reports/features/`
    `microstructure_features_aggtrades_v001__v001__phase-4bi-b__1778436978312__2bc026b4e0d9.json`
  - SHA256:
    `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
  - overall_status: `pass`; 70 / 70 PASS; 0 FAIL; 0 ERROR; 0 NA
- Feature parquet
  - path:
    `data/microstructure/features/microstructure_features_aggtrades_v001/`
    `BTCUSDT/2025/01/BTCUSDT-features-aggtrades-2025-01-15.parquet`
  - SHA256:
    `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
  - rows: 1 681 098; schema columns: 61; feature / quality columns: 45;
    lineage / identity / metadata columns: 16
- Feature manifest
  - path:
    `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json`
  - SHA256:
    `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
  - `research_eligible`: `false`
  - `eligibility_gate_status`: `pending`
  - governance labels: `labels=forbidden`, `ml=forbidden`,
    `strategy=forbidden`, `backtest=forbidden`,
    `acquisition=unauthorized`,
    `feature_computation=allowed_by_phase_4bh`,
    `stop_trigger_domain=trade_price_backtest_candidate`,
    `phase_id=4bh`
- Original derived manifest
  - path:
    `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v001.json`
  - SHA256:
    `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
  - `research_eligible`: `false`; `eligibility_gate_status`: `pending`
- Original raw manifest
  - path:
    `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`
  - SHA256:
    `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`
  - `research_eligible`: `false`; `eligibility_gate_status`: `pending`
- Phase 4bb-D raw gate report
  - SHA256:
    `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`
- Phase 4bf derived gate report
  - SHA256:
    `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`
- Phase 4bg-B successor-state JSON
  - SHA256:
    `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`
- Raw zip
  - SHA256:
    `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`

Phase 4bi-D successor-state JSON content was verified to record:
`successor_stage = "Feature Stage-5"`,
`successor_research_ml_admissible = true`,
`successor_research_eligible = true`,
`successor_eligibility_gate_status = "pass"`,
`manifest_mutation_permitted = false`,
`original_feature_manifest_research_eligible = false`,
`original_feature_manifest_eligibility_gate_status = "pending"`,
all seven governance labels at their locked values
(`labels=forbidden`, `targets=forbidden`, `ml=forbidden`,
`strategy=forbidden`, `backtest=forbidden`, `acquisition=unauthorized`,
`paper_shadow_live=forbidden`, `deployment=forbidden`,
`exchange_write=forbidden`), and
`boundary_confirmations.no_successor_authorization = true`.

No label namespace exists. No label manifest exists. No label gate
report exists. No label successor-state exists.

## 3. Scope

Phase 4bj-A defines, at policy level only:

- the **allowed future label / target families** (in principle),
- the **forbidden label / target families**,
- the **causal-separation rule** between features and labels,
- the **timestamp-anchoring rule** for label rows,
- the **horizon policy** (initial conservative set; deferred set),
- the **stop / risk-domain boundary** for label vs strategy semantics,
- the **MFE / MAE / R-multiple boundary**,
- the **forward-return boundary**,
- the **classification vs regression target boundary**,
- the **multi-horizon boundary**,
- the **cost / RR / WR / expectancy boundary**,
- the **chronological-validation requirements**,
- the **train / validation / test split boundary**,
- the **symbol / date expansion boundary**,
- the **no-rescue and M0 boundary**,
- the **future label artefact namespace** (proposed only; not created),
- the **future label manifest schema** (proposed only; not created),
- the **future implementation acceptance criteria**,
- the **future label QA / gate sequence**,
- and a **selected outcome** for the label boundary itself.

Phase 4bj-A applies prospectively. It does not authorize implementation
work.

## 4. Non-scope

Phase 4bj-A does **not**:

- modify source code;
- modify tests;
- modify scripts;
- create label-computation code;
- create target-computation code;
- create ML code;
- create strategy code;
- create backtest code;
- create analysis scripts;
- rerun the feature-family eligibility gate;
- rerun feature computation;
- regenerate the feature parquet;
- regenerate the feature manifest;
- modify the feature parquet;
- modify the feature manifest;
- modify the Phase 4bi-B gate report;
- modify the Phase 4bi-D successor-state artefact;
- modify any sidecar;
- run the normalizer;
- rerun the raw eligibility gate;
- rerun the derived-family gate;
- generate any new gate report (raw, derived, feature, label, or other);
- create a label manifest;
- create a target manifest;
- create a label successor-state artefact;
- create labels;
- create targets;
- create signals;
- create ML artefacts;
- train ML;
- create strategy logic;
- run backtests or simulations;
- compute PnL, MFE, MAE, R-multiple, equity, position state, alpha,
  edge, prediction, model score, decision score, entry/exit, or
  strategy output;
- acquire data;
- call public or private endpoints;
- call Binance APIs;
- open WebSockets;
- request or use credentials;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- authorize labels or targets beyond policy definition;
- authorize ML implementation;
- authorize strategy;
- authorize backtests;
- authorize acquisition;
- authorize paper / shadow / live or deployment;
- authorize Phase 4bj-B implementation;
- revise retained verdicts;
- change project locks;
- amend M0;
- authorize Phase 5, Phase 4 canonical, exchange-write, production keys,
  authenticated APIs, private endpoints, user stream, or live WebSocket
  implementation;
- commit anything under `data/microstructure/`.

## 5. Phase 4bi-D dependency

Phase 4bj-A is admissible **only because** Phase 4bi-D recorded a
machine-readable Stage-5 admissibility marker in a sibling successor-
state artefact while preserving the original feature manifest byte-
identically.

Phase 4bi-D's marker is interpreted as follows:

- the feature family `microstructure_features_aggtrades_v001` is
  **admissible in principle at policy level** for research and ML use;
- the **actual** feature manifest remains
  `research_eligible: false / eligibility_gate_status: pending` and
  must remain byte-identical;
- any tool that interprets the feature family as Stage-5-admissible
  must read the successor-state artefact, not the manifest;
- labels, targets, ML, strategy, backtests, and acquisition remain
  governance-forbidden / governance-unauthorized;
- Stage-5 admissibility is **upstream of M0**; the M0 admissibility
  gate (Phase 4ak) still applies prospectively to any future label,
  target, hypothesis, strategy, or backtest.

If at any future time the Phase 4bi-D successor-state SHA stops
matching the recorded value, all Phase 4bj-* memo content must be
re-validated before any successor work proceeds.

## 6. Label-boundary objective

The label boundary answers a single question:

> Given a Stage-5-admissible feature family, what future label and target
> definitions are **allowed in principle**, what is **forbidden**, and
> what must any future implementation **prove** before any label
> artefact can exist?

Phase 4bj-A's role is to fix that boundary at policy level so that any
future Phase 4bj-B (schema finalization), Phase 4bj-C (implementation),
Phase 4bj-D (structural QA), Phase 4bj-E (gate), Phase 4bj-F
(research / ML-use decision), and Phase 4bj-G (successor-state
recording) cannot silently widen scope.

## 7. Label / target design principles

Any future label / target family for this feature family must:

1. **Be a sibling derived family**, never a mutation of the feature
   family, the derived family, or the raw family.
2. **Use future information only inside the label**, never to alter
   features. Labels may use information after each row's anchor
   timestamp; features may not.
3. **Be event-aligned** to feature rows by default — one label row
   per feature row, with explicit nullable / censored handling when a
   horizon cannot be evaluated.
4. **Anchor lineage** to the feature parquet SHA, the feature manifest
   SHA, the Phase 4bi-D successor-state SHA, and the Phase 4bi-B gate
   report SHA. A label artefact that cannot identify its feature lineage
   is invalid.
5. **Preserve raw and derived governance** — no label rule may revise
   the raw or derived manifest, and no label rule may flip
   `research_eligible` on either of them.
6. **Preserve the feature manifest byte-identically.** Labels never
   modify the feature manifest.
7. **Be governance-tagged** with `labels=allowed_by_future_phase_only`,
   `targets=allowed_by_future_phase_only`, `ml=forbidden`,
   `strategy=forbidden`, `backtest=forbidden`,
   `acquisition=unauthorized` until separately authorized successor
   phases change individual labels.
8. **Default research_eligible=false / eligibility_gate_status=pending**
   on any future label manifest.
9. **Be deterministic and reproducible** — same inputs, same code
   commit, same config hash must produce byte-identical label parquet
   bytes.
10. **Be cost-realism-aware** — labels do not prove edge by themselves.
    A label that predicts a direction at zero cost is not a strategy.
11. **Be no-rescue safe** — no label family may, in effect, restate
    R2 / F1 / D1-A / V2 / G1 / C1 / 5m-thread rules under a different
    name. Each label class must stand on its own theoretical grounds.
12. **Be M0-clear** — labels are not strategies. A future strategy must
    still pass the Phase 4ak twelve-clause M0 gate independently. The
    existence of labels does not satisfy M0.

## 8. Allowed future label classes (policy-level only)

Phase 4bj-A defines the following label-class shape as **admissible in
principle** for a future schema-finalization phase. Phase 4bj-A does
not implement any of them.

**A. `forward_log_return_<horizon>`**

- Future realized **log return** from feature row timestamp `T` to a
  future reference timestamp at `T + horizon`.
- Numeric (regression-style).
- Computation uses future prices only inside the label routine; the
  feature row's price is the anchor.
- Nullable / censored when no valid future reference price exists
  within the dataset window.

**B. `forward_direction_<horizon>`**

- Classification label derived from `forward_log_return_<horizon>`.
- Requires **predeclared thresholds**. Thresholds must not be optimized
  on the same window used for evaluation.
- Typical predeclared variants: strict-sign, dead-band with predeclared
  bp width, ternary (up / flat / down) with predeclared cut-points.
- Threshold choices must be locked before any evaluation pass.

**C. `barrier_outcome_<horizon>` / `target_before_stop_<horizon>`**

- Classification-style event label indicating whether an upper barrier
  or lower barrier is touched first within a future horizon.
- Must be defined as a **label only**, never as a strategy rule.
- Requires separately defined barriers and explicit tie rules
  (same-bar / same-record / simultaneous-barrier handling).
- **Must not use mark-price stop-domain assumptions** unless explicitly
  authorized by a separately approved memo that reconciles
  Phase 3v §8 stop-trigger-domain governance with label semantics.
- For aggTrade-only inputs at v001 scope, barrier labels must use the
  same trade-price domain as features. Mixing mark-price and trade-
  price barriers in one label family is forbidden.

**D. `mfe_mae_r_path_<horizon>`**

- Forensic outcome label family that records future MFE / MAE in R
  terms relative to a predeclared structural-risk anchor.
- Treated strictly as **evaluation / forensic** evidence.
- May not be converted into strategy rules without a fresh
  M0-admissible strategy-spec memo. The Phase 4al refined no-rescue
  rule applies verbatim: no tuning / parameter selection / threshold
  selection / exit-rule retrofit on any rejected or retained-evidence
  candidate's future trade population may piggyback on
  `mfe_mae_r_path_<horizon>` labels.

**E. `time_to_event_<horizon>`**

- Optional future event-timing label (e.g., time until first
  threshold touch, time until barrier outcome, time until label B
  flips).
- Must support **null / censored** values when no event occurs within
  the horizon.
- Must be explicitly separated from strategy entry / exit logic. A
  label that records "how long until X happens" is not a rule that
  says "enter / exit when X happens."

## 9. Preferred initial future label boundary

Phase 4bj-A recommends, but **does not authorize**, the following
conservative first label family for any future Phase 4bj-B schema
finalization:

**Family name:** `microstructure_labels_aggtrades_v001`

**Initial label list (policy-recommended only):**

- `forward_log_return_1s`
- `forward_log_return_5s`
- `forward_log_return_15s`
- `forward_log_return_60s`
- `forward_direction_1s`
- `forward_direction_5s`
- `forward_direction_15s`
- `forward_direction_60s`

**Rationale (recorded; not strategy guidance):**

- The four horizons mirror the current Phase 4bh feature windows
  (`1s / 5s / 15s / 60s`). This minimizes the "feature-window leakage"
  attack surface and keeps the first label pass aligned with the
  smallest analysis frame already gated.
- Forward log returns and their direction classifications avoid the
  immediate stop / target / position-state semantics that the rejection
  topology (R2 / F1 / D1-A / V2 / G1 / C1) has shown can entangle
  with strategy rescue patterns. A label family that does not encode
  stops, targets, R-multiples, or exit logic is structurally less
  likely to be used as a back-door rescue.
- The same conservative choice keeps the first label gate (a future
  Phase 4bj-E) easier to scope, easier to test, and easier to invalidate.
- Direction labels at multiple horizons preserve the ability to detect
  short-vs-long-horizon disagreement, which is itself diagnostic
  evidence and not a strategy.

**Explicitly deferred at v001:**

- barrier labels;
- target-before-stop labels;
- MFE / MAE labels;
- R-multiple labels;
- PnL labels;
- strategy-action labels;
- position-state labels;
- execution-quality labels;
- multi-symbol labels;
- cross-sectional labels;
- 30s, 5m, and longer horizons.

A future Phase 4bj-B may keep, narrow, or further defer this list, but
must not silently widen it.

## 10. Forbidden future label / target classes

The following label / target families are **forbidden** under
Phase 4bj-A boundary, both at v001 and at any future version, unless a
separately authorized governance memo materially changes Phase 4al's
refined no-rescue rule, the Phase 4m 18-requirement validity gate,
and the Phase 4ak M0 twelve-clause gate:

- any label that **directly encodes** strategy entry decisions;
- any label that **directly encodes** strategy exit decisions;
- any label that records production order outcomes (live or paper);
- any label that records realized PnL of a hypothetical trade;
- any label that records realized profit / loss as a target;
- any label that records equity curves;
- any "alpha score" target derived from a trained model;
- any "edge score" target derived from a trained model;
- any label that depends on **future feature values that have been
  re-computed using future windows** (centered windows, future
  normalization, future z-scoring);
- any label that depends on external data not already governed at the
  same eligibility level (no spot data, no cross-venue data, no order-
  book data, no mark-price 30m / 4h / 5m / 15m data, no `aggTrades`
  beyond the existing raw family, no `metrics` beyond the
  Phase 4j §11 OI subset);
- any label that requires Phase 3v §8 stop-trigger-domain governance
  to be bypassed or relabeled to `mixed_or_unknown`;
- any "post-hoc optimized threshold" target where thresholds were
  fitted to the evaluation cell rather than predeclared;
- any **rescue-shaped** label family that, when restated, reproduces a
  retained-evidence or HARD-REJECT candidate's entry / exit rules under
  a new name. This includes, but is not limited to: R2 pullback-retest
  reconstruction, F1 mean-reversion-after-overextension reconstruction,
  D1-A funding-Z-score directional reconstruction, V2 8-feature AND
  chain reconstruction, G1 multi-dimension regime-AND classifier
  reconstruction, C1 compression-box transition reconstruction, and any
  5m strategy reconstruction from the Phase 3o / 3p Q1–Q7 outputs;
- any label that uses the live exchange's own decision boundaries as
  targets (e.g., labeling exchange-side stop triggers, exchange-side
  liquidation events, exchange-side ADL events) until a separately
  authorized governance memo addresses mark-price domain, liquidation-
  proxy completeness, and forbidden-input scope.

## 11. Causal-separation rule

Causal separation between features and labels is binding:

- A **feature value** at row `R` with timestamp `T = feature_timestamp_ms`
  may use only information from rows with
  `transact_time_ms <= T` and same-timestamp tie-break
  `row_index <= R` (this is the Phase 4bh contract verbatim).
- A **label value** at the same row `R` may use future information after
  `T`, **only inside the label routine**. Features must not be modified
  by label computation.
- Labels must never be merged back into features.
- Labels must never be used to **normalize**, **z-score**, **rank**,
  **bucket**, **filter**, or **mask** feature rows before any train /
  validation / test split definition.
- Labels must never be used to **select** which feature rows are kept
  before split definition.
- Label generation must be a **separate artefact family** from the
  feature family, with its own manifest, its own parquet, its own
  sidecars, its own gate report, and its own successor-state.
- Label code must be importable independently of feature code; mixing
  feature and label modules in a single Python package boundary is
  acceptable, but cross-imports that let label results feed back into
  feature computation are forbidden.
- Any future Phase 4bj-C implementation must include a static and
  runtime test that asserts no label value flows back into any feature
  column for any row.

## 12. Timestamp-anchoring rule

Future label rows must anchor to the following set of feature-row
identifiers (matching Phase 4bh-B / Phase 4bh lineage policy):

- `row_index` (feature row position)
- `agg_trade_id`
- `feature_timestamp_ms` (= `source_transact_time_ms`)
- `source_transact_time_ms`
- `symbol`
- `utc_date`
- `feature_dataset_family` (=`microstructure_features_aggtrades_v001`)
- `feature_dataset_version` (=`v001`)
- `feature_successor_state_sha256`
  (=`8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`)

Row model rules:

- one label row per feature row where the future horizon **can be
  evaluated** within the dataset window;
- nullable / censored label values where the future horizon **cannot be
  evaluated** (right-edge censoring at end of `utc_date` for the v001
  one-day cell, and at end of file for multi-day future extensions);
- no synthetic timestamps;
- no resampling, no upsampling, no downsampling at v001;
- if a future memo authorizes a different row model (e.g., resampled
  to fixed time grid), that memo must explicitly carry the change and
  must not be implicit in implementation.

## 13. Horizon policy

Initial recommended horizons (policy-level only):

- 1 s
- 5 s
- 15 s
- 60 s

Explicitly deferred horizons:

- 30 s
- 5 min
- any 15 min / 30 min / 1 h / 4 h horizon
- any session / day-end horizon
- any multi-day horizon

Deferral rationale:

- horizons strictly shorter than 1 s would require sub-second resolution
  that the existing aggTrade input can provide but that has not been
  gated for label use;
- horizons longer than 1 min cross into rejected-strategy timeframe
  territory (V2 30m, G1 30m+4h, C1 30m) where rescue risk is elevated;
- the rejection topology already provides explicit evidence that
  longer-horizon return / direction labels can become strategy-rescue
  vehicles. Phase 4bj-A keeps the v001 horizon set well below those
  precedents.

A future Phase 4bj-B may keep, narrow, or further defer this set, but
must not silently widen it.

## 14. Stop / risk-domain boundary

Phase 4bj-A separates label semantics from stop / risk-domain semantics:

- **Labels are not stops.** A `barrier_outcome_<horizon>` label that
  records "upper barrier touched first" is descriptive evidence, not a
  trading rule, and not a stop placement specification.
- **Labels do not authorize stop trigger domain changes.** Phase 3v §8
  stop-trigger-domain governance remains binding. Any future barrier-
  family label must specify its barrier construction in the
  `trade_price_backtest` domain to match feature lineage, unless a
  separately authorized memo reconciles barrier construction with
  Phase 3v §8.
- **R-multiple framing is forbidden at v001.** The first label family
  does not use R-multiples as targets. R-multiples re-introduce the
  full V1-arc stop-distance / structural-stop semantics, which would
  re-open the Phase 4ao harmonization seven-axis disclaim. The first
  label pass should not pay that cost.

## 15. MFE / MAE / R-multiple boundary

If a future Phase 4bj-B authorizes class **D** (`mfe_mae_r_path_<horizon>`)
labels, that memo must:

- predeclare the R-anchor (structural-stop method) explicitly;
- forbid the use of those labels for parameter tuning on any rejected
  or retained-evidence candidate's trade population (Phase 4al §9
  refined no-rescue rule applied to labels);
- forbid the use of those labels to select TP / SL / break-even /
  trailing / partial-exit / time-stop parameters retroactively;
- forbid the use of those labels as direct strategy decisions;
- declare them as **evaluation / forensic** labels in
  `governance_labels` rather than `decision` labels;
- pass M0 admissibility independently before any strategy memo can
  cite them.

Phase 4bj-A does not authorize class D at v001.

## 16. Forward-return boundary

Forward-return labels (class A) are the **most conservative** future
label class. They are designed to be:

- structurally distinct from any rejected strategy's primary rule;
- usable for descriptive evaluation, label-feature relationship
  measurement, and downstream ML evaluation;
- **not** sufficient on their own to prove edge.

Cost / RR / WR / expectancy considerations:

- forward returns are gross signals; they do not include §11.6 cost
  realism by themselves;
- any cost-adjusted expectancy claim using forward returns requires a
  separately authorized strategy / backtest phase that applies the
  Phase 4j §11 / Phase 4k / Phase 4w cost conventions verbatim;
- direction-classification accuracy on forward-return labels is **not**
  profitability; the Phase 4y reusable-insight #5 ("not zero trades is
  not success") applies to labels as well: high directional accuracy
  with negative cost-adjusted expectancy is not edge.

## 17. Classification vs regression target boundary

Two structurally different target types are admissible in principle:

- **Regression** targets: numeric label values (e.g., forward log
  return). No threshold is required at label time. Evaluation
  thresholds, if any, must be predeclared in a separately authorized
  evaluation phase.
- **Classification** targets: categorical label values (e.g., direction
  up / flat / down). Thresholds must be predeclared at label-schema
  finalization time, must be locked in the label manifest's
  `label_threshold_metadata`, and must not be optimized on the
  evaluation cell.

Any future schema-finalization phase must clearly state, per label,
whether it is regression or classification, and must record the
threshold policy in the label manifest.

## 18. Multi-horizon boundary

Multi-horizon labels (the same target shape at several horizons) are
admissible in principle.

Constraints:

- each horizon must be its own column; horizons must not be aggregated
  into a single column (no max-over-horizons, no min-over-horizons, no
  meta-targets);
- horizon disagreement is descriptive evidence, not a strategy rule;
- any future evaluation that compares predictability across horizons
  must use chronological splits and predeclared evaluation thresholds.

## 19. Cost / RR / WR / expectancy boundary

The memo records the following clarifications at policy level:

- **label design does not prove edge.**
- **forward returns are not strategy returns.**
- **direction accuracy is not profitability.**
- **RR / WR / expectancy are strategy-evaluation concepts**, not
  feature-schema or label-schema proof.
- Cost-adjusted expectancy requires a later separately authorized
  strategy / backtest phase that applies §11.6 = 8 bps HIGH per side
  verbatim, the Phase 4k / Phase 4q / Phase 4w fee / slippage / funding
  rules verbatim, and the Phase 4al refined no-rescue rule.
- MFE / MAE / R-multiple labels, if ever allowed, are forensic /
  evaluation labels and must not be used to rescue any failed strategy.

## 20. Chronological-validation requirements

Any future label artefact, label gate, or label-based research must
support and require:

- chronological splits only;
- no random shuffling of label rows;
- no threshold fitting on the evaluation window;
- no symbol / date mining;
- split metadata recorded **before** any ML training or strategy work;
- labels generated **before** ML or strategy work, but **after** feature
  eligibility (Phase 4bi-D Stage-5 admissibility marker);
- labels must preserve lineage to the feature parquet and to the
  Phase 4bi-D successor-state.

These constraints are intended to make label-based evaluation safe
against the test-set contamination, threshold-mining, and symbol-
mining patterns that the rejection topology (R2 / F1 / D1-A / V2 /
G1 / C1) has shown the project must avoid.

## 21. Train / validation / test split boundary

Phase 4bj-A does **not** define exact train / validation / test split
boundaries at v001.

It does record the binding rule that any such split, when later
authorized, must:

- be chronological;
- be predeclared in writing (a future Phase 4bj-F or equivalent);
- be locked in the label manifest's `chronological_split_policy`
  field (initially `not_yet_defined`);
- be lineage-bound to the feature parquet SHA;
- be lineage-bound to the Phase 4bi-D successor-state SHA;
- be lineage-bound to the Phase 4bi-B feature-family gate report SHA;
- not be retrofitted to maximize evaluation-set performance.

## 22. Symbol / date expansion boundary

The current Stage-5-admissible feature artefact covers exactly:

- symbol: `BTCUSDT`;
- date: `2025-01-15`.

Any future label work must, by default, stay within this one (symbol,
date) cell. Multi-symbol or multi-date expansion is **not** authorized
by Phase 4bj-A.

Specifically forbidden as silent moves:

- generating labels for additional dates from the same acquired feature
  family without authorizing the data path;
- generating labels for additional symbols (ETH, alts) without re-
  running Phase 4bb-D / Phase 4bf / Phase 4bh / Phase 4bi-A /
  Phase 4bi-B / Phase 4bi-C / Phase 4bi-D for each new (symbol, date)
  cell;
- treating cross-date or cross-symbol label aggregation as a free
  operation.

If at any future time additional days or symbols are authorized in a
separate phase, label coverage must be expanded explicitly, not by
inference from this memo.

## 23. No-rescue and M0 boundary

The Phase 4al refined no-rescue rule applies verbatim:

> No future memo, no future label, no future evaluation, and no future
> ML training may, in effect, restate or rescue R2 / F1 / D1-A / V2 /
> G1 / C1 / 5m-thread rules under a different name.

The Phase 4ak M0 twelve-clause gate applies prospectively:

> Stage-5 admissibility is upstream of M0. M0 still applies to any
> future hypothesis, label, target, strategy, or backtest. Stage-5
> admissibility does not bypass M0.

Operational consequences:

- a future Phase 4bj-B schema-finalization memo must clear M0 for the
  label family it finalizes;
- a future Phase 4bj-F research / ML-use decision memo must clear M0
  before authorizing any ML training or strategy work;
- no Phase 4bj-* memo may interpret Phase 4bi-D Stage-5 admissibility
  as either Stage-6 (research-eligible) or strategy authorization;
- the actual feature manifest, the actual derived manifest, and the
  actual raw manifest must remain `research_eligible: false /
  eligibility_gate_status: pending` for the lifetime of v001 unless a
  separately authorized phase changes that explicitly under M0 and
  no-rescue.

## 24. Future label artefact namespace (proposed only; not created)

Proposed, but **not created** by Phase 4bj-A:

- label family name:
  `microstructure_labels_aggtrades_v001`
- future label parquet path:
  `data/microstructure/labels/microstructure_labels_aggtrades_v001/`
  `BTCUSDT/2025/01/BTCUSDT-labels-aggtrades-2025-01-15.parquet`
- future label sidecar:
  same path with `.sha256` suffix
- future label manifest path:
  `data/microstructure/manifests/`
  `microstructure_labels_aggtrades_v001__v001.json`
- future label gate-report directory:
  `data/microstructure/gate-reports/labels/`
- future label successor-state directory:
  `data/microstructure/successor-state/` (sibling files only;
  feature-family successor-state files must not be modified)

The entire `data/microstructure/` tree is already gitignored under
`.gitignore:85`, so any future Phase 4bj-C-style implementation that
produces real label artefacts must respect that gitignore rule and
must not produce tracked files under `data/microstructure/`.

Phase 4bj-A does not create any of the above paths.

## 25. Future label manifest schema (proposed only)

If a future phase separately authorizes a label manifest, that manifest
must include at minimum:

- `dataset_family`: `microstructure_labels_aggtrades_v001`
- `dataset_version`: `v001`
- `label_schema_version`: `v001`
- `source_feature_dataset_family`:
  `microstructure_features_aggtrades_v001`
- `source_feature_dataset_version`: `v001`
- `source_feature_manifest_sha256`:
  `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
- `source_feature_parquet_sha256`:
  `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
- `source_feature_successor_state_sha256`:
  `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
- `source_phase_4bi_b_gate_report_sha256`:
  `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
- `label_list`: ordered list of label column names (no forbidden
  substrings; see Phase 4bh-A / Phase 4bh-B precedent for substring
  enforcement);
- `horizon_list`: `["1s", "5s", "15s", "60s"]` for the recommended
  v001 set;
- `row_count`: total label rows (may equal feature row count or fewer
  if right-edge censoring removes rows; null-tail policy must be
  recorded);
- `nullable_tail_policy`: explicit description of how horizon-
  censored rows are represented;
- `chronological_split_policy`: `not_yet_defined` at v001 unless a
  future memo locks it;
- `governance_labels`:
  - `labels`: `allowed_by_future_phase_only`
  - `targets`: `allowed_by_future_phase_only`
  - `ml`: `forbidden`
  - `strategy`: `forbidden`
  - `backtest`: `forbidden`
  - `acquisition`: `unauthorized`
  - `paper_shadow_live`: `forbidden`
  - `deployment`: `forbidden`
  - `exchange_write`: `forbidden`
- `research_eligible`: `false`
- `eligibility_gate_status`: `pending`
- `code_commit_sha`: implementation phase's commit SHA
- `created_at_unix_ms`: implementation phase's creation time

These fields are policy-level only at Phase 4bj-A. Their exact JSON
shape must be finalized by a future Phase 4bj-B memo, not by
implementation drift.

## 26. Future implementation acceptance criteria

Any future Phase 4bj-C label-implementation phase must satisfy all of
the following before it can be considered acceptable:

1. is **separately authorized** by an explicit operator decision;
2. implements **exactly** the label schema finalized by the immediately
   prior Phase 4bj-B memo (no widening, no narrowing without
   amendment);
3. writes only **gitignored** label artefacts under
   `data/microstructure/labels/`,
   `data/microstructure/manifests/microstructure_labels_aggtrades_v001*`,
   `data/microstructure/gate-reports/labels/`, and
   `data/microstructure/successor-state/` (the latter only for sibling
   label successor-states; feature successor-states must not be
   touched);
4. refuses overwrite of any existing local artefact under the same
   names;
5. preserves the feature parquet SHA byte-identically;
6. preserves the feature manifest byte-identically (no field flip; no
   reordering; no whitespace change);
7. preserves the Phase 4bi-D successor-state artefact byte-identically;
8. preserves the Phase 4bi-B gate report byte-identically;
9. preserves the Phase 4bf gate report byte-identically;
10. preserves the Phase 4bb-D raw gate report byte-identically;
11. preserves the original derived manifest byte-identically;
12. preserves the raw manifest byte-identically;
13. creates **no** ML models;
14. creates **no** strategy signals;
15. creates **no** backtests;
16. creates **no** PnL / MFE / MAE / R-multiple / equity / position-
    state / alpha / edge / prediction / model-score / decision-score /
    entry-exit / strategy-output columns;
17. keeps the label manifest `research_eligible=false /
    eligibility_gate_status=pending`;
18. records the null / censoring policy explicitly in the manifest;
19. records the horizon policy explicitly in the manifest;
20. records the chronological-split-policy field as
    `not_yet_defined` unless a separately authorized memo locks it;
21. passes label-specific tests, microstructure tests, ruff, mypy, and
    whole-repo pytest with only the two known pre-existing simulation
    failures
    (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
    and `::test_real_2026_03_ethusdt`,
    both `KeyError: 'trade_count'` in
    `src/prometheus/research/data/storage.py:232`);
22. produces a Phase 4bj-C closeout report under
    `docs/00-meta/implementation-reports/` recording the same
    discipline as Phase 4bh / Phase 4bi-B / Phase 4bi-D.

## 27. Future label QA / gate sequence

Phase 4bj-A recommends the following future Phase 4bj-* sequence
(none of which is authorized here):

- **Phase 4bj-B** — Label Schema Finalization Memo (docs-only). Locks
  the exact label list, horizon list, classification / regression
  policy, threshold policy, null-tail policy, lineage policy,
  manifest schema, and acceptance criteria.
- **Phase 4bj-C** — Label Implementation + Local Label Artefact
  Generation (code / docs / local gitignored outputs). Implements
  exactly Phase 4bj-B's schema; produces label parquet, label manifest,
  paired sidecars locally under the gitignored namespace.
- **Phase 4bj-D** — Label Artefact Structural QA Memo (analysis-and-
  docs only; read-only). Mirrors Phase 4bi-A's role for the feature
  family.
- **Phase 4bj-E** — Label-Family Eligibility Gate Design + Implementation
  + Execution. Mirrors Phase 4bi-B's role for the feature family; emits
  a label gate report; never flips the manifest's `research_eligible`
  to `true`.
- **Phase 4bj-F** — Label-Family Research / ML-Use Decision Memo
  (docs-only). Decides whether the label family is admissible in
  principle for research / ML use at policy level. Mirrors Phase 4bi-C.
- **Phase 4bj-G** — Label-Family Successor-State Recording (docs +
  local gitignored output). Mirrors Phase 4bi-D; records the policy
  decision in a sibling successor-state artefact while preserving the
  label manifest byte-identically.

No phase in the above sequence is authorized by Phase 4bj-A.

## 28. Decision options considered

Phase 4bj-A considered three label-boundary outcomes:

- **Outcome 1** — Label boundary admissible in principle, implementation
  deferred:
  - admissible in principle at policy level;
  - no labels created;
  - no targets created;
  - no label schema implemented;
  - no ML / strategy authorized;
  - a future Phase 4bj-B is required to finalize an exact label schema
    and implementation plan;
  - preferred outcome if all boundary conditions are satisfied.
- **Outcome 2** — Label boundary deferred:
  - label / target definition is not yet admissible;
  - missing prerequisite or unresolved risk must be recorded;
  - no label implementation phase may be proposed until the risk is
    resolved.
- **Outcome 3** — Label boundary rejected:
  - label / target definition should not proceed from the current
    feature family;
  - the blocking reason must be recorded.

## 29. Selected outcome

**Selected outcome: Outcome 1 — Label boundary admissible in
principle, implementation deferred.**

Justification:

- Phase 4bi-D successor-state exists and its SHA256 matches the
  recorded value
  (`8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`).
- Phase 4bi-D successor-state records Stage-5 admissibility only at
  sibling artefact level; the actual feature manifest remains
  `research_eligible: false / eligibility_gate_status: pending`.
- No labels or targets currently exist.
- No label namespace currently exists.
- This memo defines a leakage-safe future label-boundary policy
  without weakening Phase 4ak M0, Phase 4al refined no-rescue, or
  Phase 4ao harmonization.
- All 10 upstream artefacts (raw manifest, raw zip, derived manifest,
  normalized parquet, Phase 4bb-D gate report, Phase 4bf gate report,
  Phase 4bg-B successor-state, feature parquet, feature manifest,
  Phase 4bi-B gate report) preserve byte-identical SHA256 values.
- All retained verdicts and project locks are preserved verbatim.

Outcome 1 does **not** authorize Phase 4bj-B. Phase 4bj-B remains a
separately authorized future option.

## 30. What this phase proves

Phase 4bj-A proves only the following:

- a leakage-safe label boundary can be specified at policy level for
  the Stage-5-admissible feature family `microstructure_features_aggtrades_v001`;
- a conservative initial label family
  (`microstructure_labels_aggtrades_v001` with four forward-log-return
  and four forward-direction columns at 1s / 5s / 15s / 60s horizons)
  is admissible in principle, subject to a future Phase 4bj-B finalizing
  exact schema and a future Phase 4bj-C implementing it under all
  acceptance criteria;
- the no-rescue, no-leakage, no-shuffling, cost-aware, M0-bound, and
  Phase 4al-bound interpretation of labels is recorded as policy;
- the boundary between labels and stops / risks / strategies /
  backtests / ML is recorded explicitly so that future phases cannot
  silently widen scope.

## 31. What this phase does not prove

Phase 4bj-A does **not** prove:

- that any label has predictive value;
- that forward returns at any horizon are forecastable;
- that direction classification at any horizon is forecastable;
- that any label-based ML model would generalize;
- that any label-based strategy would be edge-positive;
- that any label family is the right one;
- that mark-price stop-domain forensics is admissible;
- that aggTrades-domain barrier labels are admissible at v001;
- that ETHUSDT or any other symbol is admissible at v001;
- that multi-date label coverage is admissible at v001;
- that ML training is authorized;
- that strategy work is authorized;
- that backtest work is authorized;
- that paper / shadow / live work is authorized;
- that any successor phase is authorized.

## 32. Preserved boundaries

Phase 4bj-A preserves every retained verdict and project lock
verbatim:

- H0 → FRAMEWORK ANCHOR;
- R3 → BASELINE-OF-RECORD;
- R1a / R1b-narrow → RETAINED — NON-LEADING;
- R2 → FAILED — §11.6;
- F1 → HARD REJECT;
- D1-A → MECHANISM PASS / FRAMEWORK FAIL — other;
- 5m thread → OPERATIONALLY CLOSED per Phase 3t;
- V2 → HARD REJECT — terminal for V2 first-spec;
- G1 → HARD REJECT — terminal for G1 first-spec;
- C1 → HARD REJECT — terminal for C1 first-spec;
- §11.6 = 8 bps per side preserved verbatim; round-trip = 16 bps;
- §1.7.3 0.25 % / 2× / one-position / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4p G1 strategy-spec memo;
- Phase 4q G1 backtest-plan methodology;
- Phase 4v C1 strategy-spec memo;
- Phase 4w C1 backtest-plan methodology;
- Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4am §11.A audit findings (F-1 / F-2 / F-3 / F-4);
- Phase 4an V1-arc trade-population inventory;
- Phase 4ao harmonization;
- Phase 4ap V1-arc forensic plan;
- Phase 4aq V1-arc forensic computation as descriptive evidence only;
- Phase 4ar V1-arc forensic interpretation as descriptive interpretation
  only;
- Phase 4as mechanism-map memo as docs-only reset evidence only;
- Phase 4at Binance microstructure availability / capture-feasibility
  memo as docs-only feasibility evidence only;
- Phase 4au microstructure capture-design memo as docs-only design
  evidence only;
- Phase 4av public-only capture implementation-plan memo as docs-only
  planning evidence only;
- Phase 4aw scaffold result as scaffold-only infrastructure evidence
  only;
- Phase 4ax aggTrades-only collector skeleton as collector-skeleton
  infrastructure evidence only;
- Phase 4ay aggTrades archive acquisition authorization memo as
  acquisition-boundary evidence only;
- Phase 4az aggTrades archive acquisition (BTCUSDT 2025-01-15) as
  data-acquisition infrastructure evidence only, with
  `research_eligible: false / eligibility_gate_status: pending` on the
  raw manifest;
- Phase 4ba aggTrades dataset eligibility-gate review as docs-only
  governance evidence;
- Phase 4bb-A structural QA, Phase 4bb-B execution-plan, Phase 4bb-C
  primitive implementation, Phase 4bb-D gate-execution PASS,
  Phase 4bb-E successor-state policy memo;
- Phase 4bc normalization design;
- Phase 4bd-A normalization implementation plan;
- Phase 4bd Stage-0 normalization implementation;
- Phase 4be structural QA;
- Phase 4bf-A derived-family gate design;
- Phase 4bf derived-family gate execution PASS;
- Phase 4bg-A derived-family research-eligibility decision (Option B /
  Decision form 2);
- Phase 4bg-B derived-family research-eligibility successor-state
  recording (Outcome 1);
- Phase 4bh-A feature-boundary design;
- Phase 4bh-B feature schema finalization;
- Phase 4bh feature-computation implementation;
- Phase 4bi-A feature artefact structural QA;
- Phase 4bi-B feature-family eligibility gate PASS;
- Phase 4bi-C feature-family research-use / ML-use admissibility
  decision (Outcome 1 / Decision form 1);
- Phase 4bi-D feature-family successor-state recording (Outcome 1);

— all preserved verbatim.

## 33. Recommended future options

- **Primary:** remain paused.
- **Conditional next (NOT authorized):** Phase 4bj-B — Label Schema
  Finalization Memo, docs-only.
- **Conditional cleanup (NOT authorized):** Phase 4bb-F — Gate Report
  Output Path Hygiene.
- **Conditional raw policy marker (NOT authorized):** Phase 4bb-G —
  Raw Manifest Successor-State Recording.

No successor phase is authorized.

## 34. Closeout / lock preservation

Phase 4bj-A is docs-only and text-only. No code, tests, scripts,
configs, manifests, gate reports, successor-state artefacts, feature
parquet, normalized parquet, raw zip, or data files were created or
modified outside the two new docs files and the narrow
`current-project-state.md` update. Whole-repo quality gates remain
clean. No retained verdicts were revised. No project locks changed.
M0 governance and the post-null cooldown rule remain binding
prospective governance for any future research lane.

**Recommended state:** remain paused.

**No next phase authorized.**
