# Phase 4bj-F — Label-Family Research / ML-Use Decision Memo

## 1. Phase identity

- **Phase:** Phase 4bj-F — Label-Family Research / ML-Use Decision
  Memo
- **Type:** docs-only research-use / ML-use decision memo
- **Branch:** `phase-4bj-f/label-family-research-ml-use-decision-memo`
- **Base:** `main` at `7a860d2e2e0e1ce60f140f515b40e0d0cdb3b3db`
  (post-Phase-4bj-E merge-closeout + SHA-chain-fixup state). The
  Phase 4bj-E merge-closeout itself anchored its §16 final SHA at
  `ef37b0fa3c4f91565b96d0f7da74885704d014b3` (the merge-closeout
  commit). The one-commit fixup on top of `ef37b0f` (commit
  `7a860d2`) only records that final-SHA value into the §16
  placeholder; it does not change Phase 4bj-E lifecycle semantics.
- **Date:** 2026-05-11
- **Status:** drafted; pending operator review.
- **Action:** branch-complete (not merged by this work).

**Phase 4bj-F is docs-only.** No source code, tests, scripts,
configs, MCP files, data files, manifests, sidecars, gate reports,
successor-state artefacts, or other local artefacts have been or
will be modified by this phase. The only files changed by Phase
4bj-F are:

- this memo file (new), and
- a narrow paragraph addition and "Current phase:" block update
  in `docs/00-meta/current-project-state.md`.

No code, no tests, no data, no manifests, no gate reports, and no
local artefacts are modified.

## 2. Purpose

This memo answers a single question:

> Given the Phase 4bj-E label-family eligibility gate PASS (72 / 72
> PASS report at the report level), should the project authorize a
> future Stage-5-equivalent successor-state recording for the label
> family `microstructure_labels_aggtrades_v001`, and under what
> exact constraints?

Phase 4bj-F is **docs-only**. It records a policy decision. It does
not mutate the label manifest, flip any `research_eligible` flag,
transition any `eligibility_gate_status`, change any
`chronological_split_policy`, run any gate, modify any data file,
compute any feature, design any label, define any target, train any
model, generate any signal, run any backtest, acquire any data, or
authorize any successor implementation.

Phase 4bj-F preserves every retained verdict, every project lock,
the Phase 4ak twelve-clause M0 admissibility gate (post-null
cooldown rule + cooled-down families list + memo template), the
Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy,
the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 /
§7 / §8 break-even / EMA slope / stagnation governance, the Phase
4j §11 metrics OI-subset partial-eligibility rule, the Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant, and every prior phase outcome.

Phase 4bj-F is the label-family analogue of Phase 4bi-C
(feature-family Stage-5 research-use / ML-use decision memo).

## 3. Evidence reviewed

### 3.1 Project state and SHAs

| Item | Value |
| ---- | ----- |
| Phase 4bj-E merge commit | `e06dbbd973f02352f61479918267a619b78a4c7b` |
| Phase 4bj-E merge-closeout commit | `ef37b0fa3c4f91565b96d0f7da74885704d014b3` |
| `main` SHA at Phase 4bj-F branch start | `7a860d2e2e0e1ce60f140f515b40e0d0cdb3b3db` |
| Phase 4bj-E gate report path | `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5.json` |
| Phase 4bj-E gate report SHA256 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| Phase 4bj-E gate report sidecar SHA256 | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` |
| Phase 4bj-E gate result | `overall_status = pass`; 72 / 72 PASS; 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE |

### 3.2 Label-family artefact state (verified at branch start)

| Item | Value |
| ---- | ----- |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar SHA256 | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar SHA256 | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` |
| Label row count | 1,681,098 |
| Label `research_eligible` | `false` |
| Label `eligibility_gate_status` | `"pending"` |
| Label `chronological_split_policy` | `"not_yet_defined"` |
| Label `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| Label `invalid_price_row_count` | 0 |
| Label `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| Label `governance_labels.ml` | `forbidden` |
| Label `governance_labels.strategy` | `forbidden` |
| Label `governance_labels.backtest` | `forbidden` |
| Label `governance_labels.paper_shadow_live` | `forbidden` |
| Label `governance_labels.deployment` | `forbidden` |
| Label `governance_labels.exchange_write` | `forbidden` |
| Label `governance_labels.acquisition` | `unauthorized` |

### 3.3 Relevant prior analogue phases

- **Phase 4bb-D** — raw aggTrades eligibility gate (45 / 45 PASS;
  report SHA `96f09159…`). Established the report-level gate
  pattern at Stage-2.
- **Phase 4bb-E** — raw successor-state policy memo. Established
  that raw-family `research_eligible=false` is permanent and that
  any later admissibility marker must live in a sibling
  successor-state artefact, never on the original manifest.
- **Phase 4bf** — derived-family eligibility gate (55 / 55 PASS;
  report SHA `dd4e0c1c…`). Established the derived-family gate
  pattern.
- **Phase 4bg-A** — derived-family research-eligibility decision
  memo. Selected "admissible in principle at policy level only;
  no manifest mutation; sibling successor-state required."
- **Phase 4bg-B** — derived-family research-eligibility
  successor-state recording (sibling successor-state JSON SHA
  `8bcc7d01…`). Established the successor-state recording pattern
  that preserves the original manifest byte-identically.
- **Phase 4bi-A** — feature artefact structural QA (67 / 67 + 18 /
  18 PASS).
- **Phase 4bi-B** — feature-family eligibility gate (70 / 70 PASS;
  report SHA `aa5d29c2…`).
- **Phase 4bi-C** — feature-family Stage-5 research-use / ML-use
  decision memo. **Directly analogous to Phase 4bj-F.** Selected
  Outcome 1: "Stage-5 admissible in principle at policy level;
  successor-state required; no manifest mutation; no ML / strategy
  / backtest / acquisition authorization."
- **Phase 4bi-D** — feature-family successor-state recording
  (sibling successor-state JSON SHA `8176aa3f…`). The direct
  Phase 4bj-G analogue.
- **Phase 4aw** — `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant. Binding across every subsequent phase.
  Phase 4bj-E preserved this invariant (never invoked).
- **Phase 4al** — refined no-rescue rule + §13 boundary + §14
  hierarchy. Binding prospectively.
- **Phase 4ak** — M0 twelve-clause mechanism-admissibility gate +
  post-null cooldown rule + cooled-down families list + memo
  template. Binding prospectively.

No prior memo's text was modified by Phase 4bj-F. No artefact
under `data/microstructure/` was modified by Phase 4bj-F.

## 4. Interpretation of the Phase 4bj-E PASS

The Phase 4bj-E label-family eligibility gate produced
`overall_status = pass` with 72 / 72 PASS, 0 FAIL, 0 ERROR, 0
NOT_APPLICABLE, and all 20 boundary confirmations true. The gate
report is on the local filesystem at the path recorded in §3.1, is
gitignored, and was not committed.

### 4.1 What the PASS means

The PASS is evidence — at the report level — that the on-disk
Phase 4bj-C label artefacts satisfy the 72 stable label-family
gate checks defined in `label_gate_checks.py`. Specifically the
PASS records:

1. **Artefact integrity.** The four upstream artefacts (label
   parquet, label parquet sidecar, label manifest, label manifest
   sidecar) exist on disk under the expected paths, and the
   parquet SHA256 and manifest SHA256 match their paired `.sha256`
   sidecars and match the expected values recorded inside the
   label manifest itself.
2. **Schema conformance.** The on-disk label parquet matches the
   Phase 4bj-B v001 schema bit-for-bit: 39 columns in
   `LABEL_SCHEMA_V001` canonical order; 18 label / support /
   lineage / quality columns counted correctly; `label_list`,
   `horizon_list`, and `horizon_ms_list` match the locked
   schema; no forbidden-substring column name appears.
3. **Lineage consistency.** The label manifest's
   `source_feature_parquet_sha256`,
   `source_feature_manifest_sha256`,
   `source_feature_successor_state_sha256`,
   `source_phase_4bi_b_gate_report_sha256`, and
   `source_normalized_parquet_sha256` all match the byte-identical
   upstream artefacts that the label kernel cited at Phase 4bj-C
   run-time.
4. **Hash stability.** `label_config_hash` matches
   `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`
   as recorded by Phase 4bj-C, indicating the deterministic-config
   hash chain has not drifted.
5. **Row-count and feature-row parity.** The label parquet
   contains exactly 1,681,098 rows, matching the manifest's
   `row_count` and matching the Phase 4bh feature-row count from
   the upstream feature parquet. `row_index` is contiguous
   `0..1,681,097`.
6. **Censorship counts.** The per-horizon censored counts
   (`{"1s": 9, "5s": 42, "15s": 118, "60s": 507}`) match the
   manifest's `censored_per_horizon` exactly, and the
   `horizon_censored_flag_*` true-count for each horizon matches.
   Nested censoring is correct: 1s ⊆ 5s ⊆ 15s ⊆ 60s, and
   `label_any_censored_flag` true-count equals
   `censored_per_horizon["60s"]` = 507.
7. **Invalid-price row count.** `invalid_price_row_count = 0`.
8. **Governance-preserving state.** The label manifest's
   `research_eligible`, `eligibility_gate_status`, and
   `chronological_split_policy` are all in their pre-decision
   state. The `governance_labels` block records `ml=forbidden`,
   `strategy=forbidden`, `backtest=forbidden`,
   `paper_shadow_live=forbidden`, `deployment=forbidden`,
   `exchange_write=forbidden`, and `acquisition=unauthorized`.
9. **Upstream immutability.** The four upstream Phase 4bj-C
   artefact SHAs are byte-identical pre/post the gate run.
10. **Phase 4aw invariant preserved.** The gate never invokes
    `MicrostructureManifest.flip_research_eligible(...)`; the
    always-raises invariant remains intact.
11. **Report-level invariants enforced.** The gate report's
    `research_eligible_after = False`,
    `label_manifest_research_eligible_after = False`,
    `label_manifest_eligibility_gate_status_after = "pending"`,
    `label_manifest_chronological_split_policy_after =
    "not_yet_defined"`, `stage_5_authorized = False`,
    `stage_5_research_or_ml_use = False`, and
    `no_successor_authorization = True` are all written-time
    invariants enforced by `write_label_gate_report` before the
    atomic write.

### 4.2 What the PASS does **not** mean

The PASS is **report-level evidence only**. It does **not**, in any
combination, mean any of the following:

- **It does not transition the manifest.** The label manifest at
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
  remains `research_eligible=false`,
  `eligibility_gate_status="pending"`, and
  `chronological_split_policy="not_yet_defined"`. No write to that
  file occurred during Phase 4bj-E or Phase 4bj-F.
- **It does not create a successor-state.** No sibling
  successor-state JSON for the label family exists. The label
  family has no machine-readable Stage-5 marker.
- **It does not authorize ML.** No ML model training, model
  selection, hyperparameter search, feature ranking, or
  meta-labeling is authorized. `governance_labels.ml = forbidden`
  remains binding on the label manifest.
- **It does not authorize strategy.** No strategy hypothesis,
  signal construction, position state, entry / exit rule, or
  trading-rule conditioning on label values is authorized.
  `governance_labels.strategy = forbidden` remains binding.
- **It does not authorize backtesting.** No backtest may be run.
  `governance_labels.backtest = forbidden` remains binding.
- **It does not authorize acquisition.** No additional aggTrades /
  5m / 1m / tick / mark-price / order-book / spot / cross-venue
  data acquisition is authorized.
  `governance_labels.acquisition = unauthorized` remains binding.
- **It does not authorize paper / shadow.** No paper / shadow
  runtime work is authorized.
- **It does not authorize live.** No live-readiness, no
  deployment, no exchange-write capability, no production keys, no
  authenticated APIs, no private endpoints, no user stream, no
  live WebSocket implementation is authorized.
- **It does not authorize MCP, Graphify, `.mcp.json`, or
  credentials.** None of these is authorized.
- **It does not predict.** The PASS makes no claim about
  predictive validity, signal quality, edge, profitability, or
  out-of-sample generalization.
- **It does not generalize.** The PASS covers exactly one symbol
  (BTCUSDT) and one UTC date (2025-01-15). The PASS does not
  generalize to additional symbols, additional dates, or
  additional horizons.
- **It does not amend M0.** The Phase 4ak twelve-clause M0
  admissibility gate, post-null cooldown rule, and cooled-down
  families list all remain binding.
- **It does not bypass no-rescue.** The Phase 4al refined
  no-rescue rule remains binding. Stage-5 admissibility is
  upstream of M0 and cannot be repurposed as a rescue lever for
  any cooled-down family (`G1`, `V2`, `C1`, `R2`, `F1`, `D1-A`,
  regime-first lane, microstructure / order-flow / liquidity-timing
  lane, mark-price stop-domain lane).

The PASS is a governance signal about local artefact integrity,
not an empirical claim about edge or live readiness.

## 5. Research / ML-use decision analysis

### 5.1 Evidence chain

The label-family evidence chain on the project record is:

```text
Phase 4az  raw acquisition           → strict integrity gate PASS
Phase 4bb-D raw eligibility gate     → 45 / 45 PASS (report SHA 96f09159…)
Phase 4bb-E raw successor-state policy → raw research_eligible=false permanent
Phase 4bd  normalization run         → 27 / 27 PASS
Phase 4be  normalized structural QA  → 60 / 60 PASS
Phase 4bf  derived-family gate       → 55 / 55 PASS (report SHA dd4e0c1c…)
Phase 4bg-A derived research-elig.   → admissible at policy level only
Phase 4bg-B derived successor-state  → sibling SHA 8bcc7d01…
Phase 4bh  feature kernel run        → 135 / 135 validation PASS
Phase 4bi-A feature structural QA    → 67 / 67 + 18 / 18 PASS
Phase 4bi-B feature-family gate      → 70 / 70 PASS (report SHA aa5d29c2…)
Phase 4bi-C feature research-elig.   → Stage-5 admissible at policy level
Phase 4bi-D feature successor-state  → sibling SHA 8176aa3f…
Phase 4bj-A label boundary memo      → label boundary defined
Phase 4bj-B label schema finalization → label schema locked
Phase 4bj-C label implementation     → label parquet + manifest written
Phase 4bj-D label structural QA      → 21 / 21 PASS
Phase 4bj-E label-family gate        → 72 / 72 PASS (report SHA b0b5405b…)
```

The chain is internally consistent. Each phase preserves the
upstream artefacts byte-identically. No verdict has been revised.
No project lock has been loosened.

### 5.2 Evidence layer evaluation

The following layers of evidence are now on the project record for
the label family:

1. **Label artefact integrity.** Confirmed by Phase 4bj-E gate
   §3.1 of this memo records the four upstream SHAs that the gate
   verified.
2. **Schema finality.** The label parquet matches `LABEL_SCHEMA_V001`
   bit-for-bit. 39 columns; canonical order; no forbidden-substring
   column names. Confirmed by Phase 4bj-E gate group D (checks
   D01–D10).
3. **Row-count and feature-row parity.** 1,681,098 rows in the
   label parquet; identical to the upstream Phase 4bh feature
   parquet row count; `row_index` contiguous `0..1,681,097`.
   Confirmed by Phase 4bj-E gate group E (checks E01–E04).
4. **Censorship counts.** Per-horizon censored counts match the
   manifest exactly; nested censoring is correct; 1s ⊆ 5s ⊆ 15s
   ⊆ 60s. Confirmed by Phase 4bj-E gate groups G (G01–G02) and H
   (H01–H04).
5. **Invalid price row count.** `invalid_price_row_count = 0`.
   Confirmed by Phase 4bj-E gate group G (G01).
6. **Source feature lineage.** The label manifest's
   `source_feature_parquet_sha256`,
   `source_feature_manifest_sha256`,
   `source_feature_successor_state_sha256`,
   `source_phase_4bi_b_gate_report_sha256`, and
   `source_normalized_parquet_sha256` all match upstream
   byte-identical artefacts. Confirmed by Phase 4bj-E gate group
   F (F01–F11).
7. **Manifest governance labels.** All seven governance labels
   are in their forbidden / unauthorized state. Confirmed by
   Phase 4bj-E gate group C (C01–C10).
8. **`chronological_split_policy` remains `"not_yet_defined"`.**
   Confirmed by Phase 4bj-E gate group O (O01).
9. **`research_eligible` remains `false`.** Confirmed.
10. **`eligibility_gate_status` remains `"pending"`.** Confirmed.
11. **No successor-state artefact exists.** No file under any
    plausible label successor-state path exists on disk. The
    Phase 4bj-E gate did not create one and is structurally
    incapable of creating one (the writer's path discipline
    forbids any write outside `data/microstructure/gate-reports/labels/`).

### 5.3 Sufficiency analysis

The eight Phase 4bi-C deciding criteria, adapted to the label
family for Phase 4bj-F:

1. Phase 4bj-E gate report present and SHA matches recorded value
   (`b0b5405b…`) — **PASS**.
2. Gate report `overall_status = pass` with 72 / 72 PASS — **PASS**.
3. All 20 / 20 boundary confirmations true in the gate report —
   **PASS**.
4. Label parquet SHA matches recorded value (`ef50038a…`) —
   **PASS**.
5. Label manifest SHA matches recorded value (`181a799c…`) —
   **PASS**.
6. Label manifest remains `research_eligible=false`,
   `eligibility_gate_status="pending"`, and
   `chronological_split_policy="not_yet_defined"` — **PASS**.
7. Phase 4bh / 4bi-A / 4bi-B / 4bi-D / 4bj-A / 4bj-B / 4bj-C /
   4bj-D / 4bj-E evidence is internally consistent — **PASS**.
8. All non-scope and no-rescue boundaries remain preserved —
   **PASS**.

All eight criteria are satisfied. There is no missing evidence
link and no unresolved structural risk for the label family at the
policy / governance layer.

### 5.4 Critical reminders that bound the decision

- **Labels alone are not signals.** A label column is a measurement
  of future-relative behaviour, not a trading decision. Converting
  labels into signals requires a separate, fresh, ex-ante strategy
  hypothesis that clears the Phase 4ak M0 twelve-clause
  admissibility gate.
- **Labels alone are not strategy evidence.** The label family has
  not been evaluated for predictive validity, baseline-superiority
  over H0 / R3, or out-of-sample generalization. Any conversion of
  label inspection into strategy candidacy is forbidden and would
  trigger the Phase 4al refined no-rescue rule.
- **Labels alone are not live-readiness evidence.** No live-trading
  authorization can be derived from label-family admissibility.
  Live-readiness requires the full §1.7.3 / §11.6 / Phase 3v §8 /
  Phase 3w stack plus separately authorized paper / shadow / tiny-
  live phases.
- **ML would require further safeguards before any model
  training.** ML training requires at minimum: (i) Stage-5
  successor-state recording for the label family (a future Phase
  4bj-G); (ii) a separately authorized ML-experimentation phase
  with predeclared validation, leakage controls, and reporting;
  (iii) Phase 4ak M0 admissibility for the underlying hypothesis;
  (iv) Phase 4al refined no-rescue compliance.
- **Single-symbol single-day scope.** The label artefact covers
  exactly BTCUSDT on 2025-01-15 (1,681,098 rows). Any
  generalization claim is out of scope until additional days
  and / or symbols are separately authorized.

## 6. Decision options

The following docs-only outcomes were defined and evaluated:

### 6.1 Option A — remain paused, no successor-state yet

The most conservative outcome. Phase 4bj-F simply records the
Phase 4bj-E PASS as report-level evidence, makes no policy
admissibility statement, and recommends remaining paused. Under
Option A, the label family remains at Stage-0 (acquired);
research-eligible flags remain `false`; no successor-state is ever
authorized; no future Phase 4bj-G is implied.

**Tradeoffs.** Conservative and safe, but does not utilise the
evidence already on record. Forecloses on later analytic use of
the label family without a future docs-only memo.

### 6.2 Option B — authorize a future Phase 4bj-G sibling successor-state recording phase under strict constraints

Recognise that the Phase 4bj-E PASS is sufficient evidence at the
policy / governance level to admit a future Phase 4bj-G
successor-state recording phase, mirroring the Phase 4bg-B
(derived-family) and Phase 4bi-D (feature-family) precedents. The
future Phase 4bj-G would be **separately authorized**, would
produce **exactly one** sibling successor-state JSON under
`data/microstructure/successor-state/` (or whatever path the
output-path-hygiene phase ultimately establishes), would preserve
the original label manifest byte-identically, and would not flip
`research_eligible`, transition `eligibility_gate_status`, or
change `chronological_split_policy`. Under Option B, Phase 4bj-F
**does not authorize Phase 4bj-G**; it only states that Phase
4bj-G is admissible in principle at policy level.

**Tradeoffs.** Matches the proven Phase 4bg-A → Phase 4bg-B and
Phase 4bi-C → Phase 4bi-D pattern. Preserves manifest immutability
and Phase 4aw invariant. Does not unlock ML, strategy, or
acquisition. Records a coherent policy admissibility decision.

### 6.3 Option C — require additional docs-only policy before successor-state

Defer admissibility until additional docs-only policy work is
completed (e.g., explicit label-research-use scope memo, label-ML-
use scope memo, or multi-symbol generalization memo). Under
Option C, Phase 4bj-G remains both unauthorized and not-yet-
admissible-in-principle.

**Tradeoffs.** Conservative but adds policy debt. Possibly
appropriate if there were a missing evidence link in the chain;
there is not. The Phase 4bi-C precedent did not require additional
upstream policy work, and the label-family evidence chain is
analogous in completeness.

### 6.4 Option D — reject label-family research / ML-use admissibility for now

Selected only if there is a structural reason the label family is
not admissible at all (e.g., schema violation, lineage break,
governance violation, leakage, label leakage, ungoverned column
access, etc.). No such reason has been observed: the Phase 4bj-E
gate's group F (lineage, 11 checks), group D (schema, 10 checks),
group C (governance, 10 checks), and group L (no-rescue, 4 checks)
all PASS.

**Tradeoffs.** Would only be appropriate if a structural defect
were found, which is not the case.

### 6.5 Option E — ML / strategy / backtest / acquisition / paper-shadow / live work

**FORBIDDEN — NOT RECOMMENDED.** Phase 4bj-F does not, and cannot,
authorize any of these. The label family's `governance_labels.ml`,
`strategy`, `backtest`, `paper_shadow_live`, `deployment`,
`exchange_write`, and `acquisition` fields remain in their
forbidden / unauthorized state. The Phase 4ak M0 gate, post-null
cooldown rule, cooled-down families list, and Phase 4al refined
no-rescue rule all remain binding.

## 7. Recommendation

### 7.1 Selected outcome

**Option B (Decision form):**

> **Label-family research / ML-use admissibility is admissible in
> principle at policy / governance level for
> `microstructure_labels_aggtrades_v001`, but no manifest mutation
> occurs in this phase. A separately authorized future Phase
> 4bj-G sibling successor-state recording phase is required before
> any machine-readable label admissibility marker exists. Phase
> 4bj-F does not authorize Phase 4bj-G. Phase 4bj-F does not
> authorize ML, strategy, backtests, acquisition, paper / shadow,
> live-readiness, deployment, exchange-write, production keys,
> authenticated APIs, private endpoints, user stream, live
> WebSocket implementation, MCP, Graphify, `.mcp.json`, or
> credentials. Recommended state: remain paused unless the
> operator separately authorizes Phase 4bj-G.**

This outcome matches the Phase 4bg-A → Phase 4bg-B (derived-family)
and Phase 4bi-C → Phase 4bi-D (feature-family) precedents. The
Phase 4bj-E evidence chain is internally consistent at the policy
layer. All eight deciding criteria are satisfied. There is no
missing evidence link and no unresolved structural risk.

### 7.2 What this recommendation does not change

- The label manifest at
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`
  remains `research_eligible=false`,
  `eligibility_gate_status="pending"`, and
  `chronological_split_policy="not_yet_defined"`.
- No machine-readable label admissibility marker exists yet.
- The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant remains binding (never invoked by Phase
  4bj-F).
- The Phase 4al refined no-rescue rule remains binding.
- The Phase 4ak twelve-clause M0 admissibility gate, post-null
  cooldown rule, and cooled-down families list all remain binding.
- All retained verdicts (H0, R3, R1a, R1b-narrow, R2, F1, D1-A, 5m
  thread, V2, G1, C1) remain preserved verbatim.
- All project locks (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8,
  Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4k,
  Phase 4p, Phase 4q, Phase 4v, Phase 4w) remain preserved
  verbatim.

### 7.3 Why Option B and not Option A

Option A (remain paused with no policy statement) is also a
defensible choice. Option B is preferred because:

1. **Evidence is complete.** All eight deciding criteria are
   satisfied. There is no missing structural evidence at the
   policy / governance layer.
2. **Precedent.** The Phase 4bi-C → Phase 4bi-D pattern
   established that a passing gate report is sufficient evidence
   to admit (in principle, at policy level) a sibling successor-
   state recording phase. The label-family evidence chain is
   analogous in completeness and quality.
3. **No new permissions.** Option B does not unlock ML, strategy,
   backtests, acquisition, or live work. The forbidden /
   unauthorized state of the label manifest's governance labels
   remains intact.
4. **Conservative successor.** A future Phase 4bj-G, if separately
   authorized, would be docs + local-gitignored-output only, would
   preserve the original label manifest byte-identically, and
   would not lift any forbidden flag on the manifest. The
   sibling successor-state JSON would be the only machine-readable
   indicator of admissibility, and it would live outside the
   manifest.

## 8. Strict constraints for a future Phase 4bj-G (if separately authorized)

A future Phase 4bj-G label-family successor-state recording phase,
**if separately authorized by the operator and only under explicit
ex-ante authorization**, must obey the following constraints,
mirroring the Phase 4bg-B and Phase 4bi-D precedents:

### 8.1 Scope and outputs

- Phase 4bj-G must be docs-and-local-gitignored-output (or docs-
  only if no successor-state artefact is needed) — exactly the
  same pattern as Phase 4bg-B and Phase 4bi-D.
- Phase 4bj-G must produce **exactly one** sibling successor-state
  JSON artefact under a gitignored namespace such as
  `data/microstructure/successor-state/`. The exact subdirectory
  layout (e.g., `successor-state/labels/`) is subject to a future
  Phase 4bb-F output-path-hygiene memo if one is ever authorized;
  otherwise Phase 4bj-G should mirror Phase 4bi-D's path layout.
- Phase 4bj-G must produce a paired `.sha256` sidecar matching the
  artefact's bytes.
- Phase 4bj-G must not produce any other artefact under
  `data/microstructure/`.

### 8.2 Citations

- Phase 4bj-G must cite the Phase 4bj-E gate report id verbatim
  (`microstructure_labels_aggtrades_v001__v001__phase-4bj-e__1778531608796__89cde8ad14b5`).
- Phase 4bj-G must cite the Phase 4bj-E gate report SHA verbatim
  (`b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`).
- Phase 4bj-G must cite the Phase 4bj-E gate report sidecar SHA
  verbatim
  (`2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191`).
- Phase 4bj-G must cite the label parquet SHA verbatim
  (`ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26`).
- Phase 4bj-G must cite the label parquet sidecar SHA verbatim
  (`b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b`).
- Phase 4bj-G must cite the label manifest SHA verbatim
  (`181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3`).
- Phase 4bj-G must cite the label manifest sidecar SHA verbatim
  (`3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d`).
- Phase 4bj-G must cite `label_config_hash` verbatim
  (`fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`).
- Phase 4bj-G must cite the upstream feature parquet SHA, feature
  manifest SHA, feature successor-state SHA (Phase 4bi-D), Phase
  4bi-B gate report SHA, normalized parquet SHA, derived manifest
  SHA, derived successor-state SHA (Phase 4bg-B), raw manifest
  SHA, raw zip SHA, and raw gate report SHA (Phase 4bb-D) verbatim.
- Phase 4bj-G must cite this Phase 4bj-F memo as the
  policy-decision evidence.

### 8.3 Manifest immutability

- Phase 4bj-G must not modify the label manifest at
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`.
- Phase 4bj-G must not modify the label parquet.
- Phase 4bj-G must not modify any sidecar.
- Phase 4bj-G must not modify any prior gate report or
  successor-state artefact.
- The original label manifest must remain byte-identical at SHA
  `181a799c…` after Phase 4bj-G.
- The original label parquet must remain byte-identical at SHA
  `ef50038a…` after Phase 4bj-G.

### 8.4 Manifest field invariants

- Phase 4bj-G must not flip `research_eligible` on the label
  manifest. The manifest field remains `false`.
- Phase 4bj-G must not transition `eligibility_gate_status` on the
  label manifest. The manifest field remains `"pending"`.
- Phase 4bj-G must not change `chronological_split_policy` on the
  label manifest. The manifest field remains `"not_yet_defined"`
  unless a separately authorized scope memo explicitly justifies a
  policy definition (and even then, only via a separately
  authorized phase, not Phase 4bj-G).
- Phase 4bj-G must record `successor_research_eligible=true` (or
  whatever final field name is chosen) **only on the sibling
  successor-state artefact**, not on the manifest.
- Phase 4bj-G must record `successor_eligibility_gate_status=pass`
  (or equivalent) **only on the sibling successor-state artefact**.
- Phase 4bj-G must record `labels=forbidden`, `targets=forbidden`,
  `ml=forbidden`, `strategy=forbidden`, `backtest=forbidden`,
  `paper_shadow_live=forbidden`, `deployment=forbidden`,
  `exchange_write=forbidden`, `acquisition=unauthorized` on both
  the manifest (unchanged) and the sibling successor-state
  artefact (until a further separately authorized phase changes
  those).

### 8.5 Forbidden activities

A future Phase 4bj-G must NOT:

- train any ML model;
- design any ML architecture;
- rank any feature;
- create any meta-labeling artefact;
- create any strategy logic;
- run any backtest;
- generate any signal;
- compute any PnL / MFE / MAE / R-multiple / equity / position
  state / alpha / edge / prediction / model score / decision score
  / entry-exit / strategy output;
- acquire additional data of any kind;
- call any public endpoint;
- call any Binance API;
- call any authenticated REST endpoint;
- call any private endpoint;
- open any WebSocket;
- use any credential;
- read or create `.env`;
- read or create `.mcp.json`;
- enable MCP;
- enable Graphify;
- rerun the normalizer, raw eligibility gate, derived-family
  gate, feature kernel, feature-family eligibility gate, label
  kernel, or label-family eligibility gate;
- modify `src/prometheus/`, tests, scripts, `pyproject.toml`,
  `README.md`, `.gitignore`, or MCP files;
- create a label-family eligibility gate report;
- create any label-family artefact other than the single sibling
  successor-state JSON;
- amend M0;
- revise any retained verdict;
- loosen any project lock;
- authorize any further successor by itself (no auto-authorization
  of Phase 5, Phase 4 canonical, ML, strategy, backtest,
  acquisition, paper / shadow / live / exchange-write paths).

### 8.6 Invariant preservation

- Phase 4bj-G must preserve the Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant. The helper must never be invoked.
- Phase 4bj-G must preserve the Phase 4al refined no-rescue rule
  + §13 boundary + §14 hierarchy.
- Phase 4bj-G must preserve the Phase 4ak M0 twelve-clause gate +
  post-null cooldown rule + cooled-down families list + memo
  template.
- Phase 4bj-G must preserve the Phase 3v §8 stop-trigger-domain
  governance.
- Phase 4bj-G must preserve the Phase 3w §6 / §7 / §8 break-even
  / EMA slope / stagnation governance.
- Phase 4bj-G must preserve the Phase 4j §11 metrics OI-subset
  partial-eligibility rule.
- Phase 4bj-G must preserve every retained verdict and project
  lock verbatim.

### 8.7 Authorization boundary

Phase 4bj-F **does not authorize Phase 4bj-G.** Phase 4bj-G
remains unauthorized unless the operator issues a separate
explicit authorization prompt with the exact scope, name,
constraints, and acceptance criteria. Per the Phase 4bk-A workflow
standard, every phase must begin from a separately authorized
operator prompt.

## 9. Explicit non-authorizations

Phase 4bj-F does **NOT** authorize, and cannot be construed as
authorizing, any of the following:

- **Phase 4bj-G** — Label-Family Successor-State Recording.
- **Phase 5** — any successor numbered phase.
- **Phase 4 canonical** — any canonical Phase 4 work.
- **Phase 4bb-F** — Gate Report Output Path Hygiene.
- **Phase 4bb-G** — Raw Manifest Successor-State Recording.
- **ML implementation** — no ML codebase or library introduction.
- **ML training** — no model fit, gradient step, or optimization
  run.
- **Model selection** — no model architecture chosen.
- **Feature ranking** — no SHAP, mutual-information, permutation
  importance, or any feature-importance computation.
- **Meta-labeling** — no triple-barrier, meta-label, or label-
  conditioning artefact.
- **Strategy implementation** — no strategy logic, signal
  generator, entry / exit rule, or position-state machine.
- **Backtest implementation** — no backtest runner, simulator, or
  walk-forward harness.
- **Additional data acquisition** — no aggTrades / 5m / 1m / tick
  / mark-price / order-book / spot / cross-venue / multi-day /
  multi-symbol acquisition.
- **Paper / shadow** — no paper or shadow runtime work.
- **Live-readiness** — no live-runtime preparation.
- **Deployment** — no production deployment work.
- **Production keys** — no production-key creation, storage,
  scoping, or rotation.
- **Authenticated APIs** — no signed REST endpoint calls.
- **Private endpoints** — no private Binance endpoint use.
- **User stream** — no user data stream subscription.
- **WebSockets** — no live WebSocket implementation.
- **MCP** — no MCP enable, configure, or use.
- **Graphify** — no Graphify enable, configure, or use.
- **`.mcp.json`** — no creation, read, or modification.
- **Credentials** — no credential creation, storage, or use.
- **Exchange-write** — no exchange-write capability path.
- **Manifest transition** — no manifest field transition on the
  label manifest, feature manifest, derived manifest, or raw
  manifest.

## 10. Retained verdict ledger

All retained verdicts preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim by Phase 4bj-F.

## 11. Preserved locks

All locks preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position
  max / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant

All prior phase results (Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as,
4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C,
4bb-D, 4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B,
4bh-A, 4bh-B, 4bh, 4bi-A, 4bi-B, 4bi-C, 4bi-D, 4bj-A, 4bj-B,
4bj-C, 4bj-D, 4bj-E, 4bk-A) preserved verbatim.

## 12. Boundary confirmations

Phase 4bj-F honours every boundary below:

- no source code modified
- no test modified
- no script modified
- no `pyproject.toml`, `README.md`, `.gitignore`, or MCP file
  modified
- no label parquet modified
- no label parquet sidecar modified
- no label manifest modified
- no label manifest sidecar modified
- no feature parquet, feature manifest, normalized parquet,
  original derived manifest, raw manifest, raw zip, Phase 4bb-D
  raw gate report, Phase 4bf derived gate report, Phase 4bg-B
  successor-state, Phase 4bi-B feature-family gate report, Phase
  4bi-D feature-family successor-state, or Phase 4bj-E
  label-family gate report modified
- no `data/microstructure/` write occurred
- no `data/microstructure/` artefact committed
- no label-family successor-state artefact created
- no replacement parquet / manifest / sidecar / gate report /
  successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no ML model trained
- no ML architecture designed
- no feature ranking performed
- no meta-labeling created
- no strategy created
- no strategy signal computed
- no backtest run
- no data acquired
- no public endpoint called
- no Binance API called
- no WebSocket opened
- no credential read
- no `.env` read or created
- no `.mcp.json` read or created
- no MCP enabled
- no Graphify enabled
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family eligibility gate rerun
- no label kernel rerun
- no label-family eligibility gate rerun
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 13. Current-project-state update

`docs/00-meta/current-project-state.md` is narrowly updated to:

1. Add a new Phase 4bj-F narrative paragraph above the existing
   Phase 4bj-E narrative paragraph, recording Phase 4bj-F's
   docs-only status, the Option B selected outcome, the
   admissibility-in-principle statement, the no-mutation
   guarantee, the explicit non-authorizations, and the
   recommended-state language.
2. Replace the existing Current-phase code block with a Phase
   4bj-F version that records: phase identity, branch, base SHA,
   docs-only status, scope of decision, the eight deciding-criteria
   PASS results, what the decision means and does not mean, the
   explicit non-authorizations, the strict constraints on a
   future Phase 4bj-G, and the recommended state.
3. Demote the prior Phase 4bj-E "Current phase:" block to
   historical context, preserving its content verbatim.

No other change to `current-project-state.md` is made by Phase
4bj-F.

## 14. Recommended state

**Remain paused unless the operator separately authorizes Phase
4bj-G.**

Phase 4bj-F is docs-only. It records a policy admissibility
decision. It does not authorize Phase 4bj-G. It does not authorize
ML, strategy, backtests, acquisition, paper / shadow,
live-readiness, deployment, exchange-write, production keys,
authenticated APIs, private endpoints, user stream, live WebSocket
implementation, MCP, Graphify, `.mcp.json`, or credentials. No
machine-readable label admissibility marker exists after this
phase. The label manifest remains `research_eligible=false`,
`eligibility_gate_status="pending"`, and
`chronological_split_policy="not_yet_defined"`.

**Conditional next, NOT authorised:**

Phase 4bj-G — Label-Family Successor-State Recording is the
cleanest non-paused option. It would, if separately authorized,
produce exactly one sibling successor-state JSON artefact under a
gitignored namespace, preserve the original label manifest
byte-identically, and record a machine-readable admissibility
marker on the sibling artefact only. Phase 4bj-G is **not**
authorised by Phase 4bj-F. Per the Phase 4bk-A workflow standard,
a separately authorised authorization prompt is required before
any successor begins.

## 15. Closeout / lock preservation

Phase 4bj-F is docs-only. No source code, tests, scripts, configs,
README, pyproject, `.gitignore`, MCP files, raw artefacts, derived
artefacts, feature artefacts, label artefacts, manifests,
sidecars, gate reports, or successor-state artefacts have been or
will be modified by this phase. The policy-level admissibility
decision recorded above is text-only.

Phase 4bj-F preserves verbatim:

- the retained verdict ledger;
- the project locks;
- the Phase 4ak M0 twelve-clause gate;
- the Phase 4ak post-null cooldown rule;
- the Phase 4ak cooled-down families list;
- the Phase 4ak M0 memo template;
- the Phase 4al refined no-rescue rule;
- the Phase 4al §13 boundary and §14 hierarchy;
- the Phase 3v §8 stop-trigger-domain governance;
- the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- the Phase 4j §11 metrics OI-subset partial-eligibility rule;
- the Phase 4aw
  `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant;
- every prior phase's recorded outcomes (Phase 4am .. Phase 4bk-A
  preserved verbatim).

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bj-F.**
