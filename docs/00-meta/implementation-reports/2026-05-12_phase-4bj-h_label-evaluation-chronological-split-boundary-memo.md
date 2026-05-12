# Phase 4bj-H — Label Evaluation / Chronological Split Boundary Memo

**Phase identity:** Phase 4bj-H — Label Evaluation / Chronological Split Boundary Memo (docs-only).
**Date:** 2026-05-12.
**Branch:** `phase-4bj-h/label-evaluation-chronological-split-boundary-memo`.
**Base:** `main` at `1064d2932ed34bc706a2311139a5431e788ce798` (Phase 4bb-G SHA-chain-fixup commit on top of merge-closeout `3f52176889fdb6ce91b227b2140002e7f44aba6b`).
**Status:** drafted; pending operator review.
**Phase type:** docs-only boundary / governance memo.

A note on the SHA-chain pattern: the Phase 4bb-G merge-closeout itself anchored its §2 final-SHA value at the merge-closeout commit `3f52176`. The one-commit fixup on top of that anchor (commit `1064d29`) only records the final-`main` SHA back into §2 of the Phase 4bb-G merge-closeout; it does not change Phase 4bb-G lifecycle semantics. Phase 4bj-H branches from `1064d29` because that is the post-fixup `main` state; the canonical "Phase 4bb-G project-complete" anchor remains the merge-closeout commit (`3f52176`).

---

## 1. Phase identity

- **Phase name:** Phase 4bj-H — Label Evaluation / Chronological Split Boundary Memo.
- **Phase type:** docs-only boundary / governance memo.
- **Branch:** `phase-4bj-h/label-evaluation-chronological-split-boundary-memo`.
- **Base SHA:** `main` at `1064d2932ed34bc706a2311139a5431e788ce798`.
- **Predecessor anchor:** Phase 4bb-G merge-closeout `3f52176889fdb6ce91b227b2140002e7f44aba6b` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bj-H only.

Phase 4bj-H is **strictly docs-only**. It does **not**:

- evaluate labels;
- read or compute over the label parquet beyond documentation-level references already summarised in prior repo docs;
- create train / validation / test splits;
- create split artefacts;
- create new manifests;
- create new gate reports;
- create new successor-state artefacts;
- rerun any gate;
- run kernels;
- run normalizers;
- modify any manifest;
- modify any sidecar;
- modify any parquet;
- modify any raw zip;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any manifest;
- train ML or design ML architecture;
- rank features or create meta-labeling;
- create a strategy, compute signals, or run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- acquire data (order-book, mark-price, spot, cross-venue, funding, open-interest, additional aggTrades, etc.);
- call public, authenticated, or private endpoints;
- open WebSockets or user streams;
- create or read credentials, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- modify project locks, retained verdicts, or M0 governance;
- authorize Phase 5 or any successor phase.

Tracked changes by Phase 4bj-H are exactly two new docs (this memo + the Phase 4bj-H closeout) plus a narrow paragraph + "Current phase:" block update in `docs/00-meta/current-project-state.md`. No source code, tests, scripts, configuration, `pyproject.toml`, `README.md`, `.gitignore`, MCP files, or governance memos (beyond the narrow `current-project-state.md` update) are modified. No `data/microstructure/` artefact is created, moved, copied, renamed, deleted, or modified.

---

## 2. Current evidence boundary

The microstructure aggTrades lineage now has governed artefacts across four dataset families, with every family showing the same lifecycle shape:

- original manifest preserved with `research_eligible: false` and `eligibility_gate_status: "pending"`;
- sibling successor-state JSON marker recorded under the gitignored `data/microstructure/successor-state/` namespace, with paired `.sha256` sidecar;
- local artefacts preserved byte-identically across the recording phase;
- no manifest transition; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked).

| Family | Successor-state marker recorded by | Marker filename (gitignored) | Original manifest state |
| --- | --- | --- | --- |
| Raw (`microstructure_raw_aggtrades_v001`) | Phase 4bb-G | `…__stage2_raw_admissible__phase-4bb-g.json` | `research_eligible=false`, `eligibility_gate_status="pending"` |
| Derived / normalized (`microstructure_normalized_aggtrades_v001`) | Phase 4bg-B | `…__stage3_research_eligible__phase-4bg-b.json` | `research_eligible=false`, `eligibility_gate_status="pending"` |
| Feature (`microstructure_features_aggtrades_v001`) | Phase 4bi-D | `…__stage5_research_ml_admissible__phase-4bi-d.json` | `research_eligible=false`, `eligibility_gate_status="pending"` |
| Label (`microstructure_labels_aggtrades_v001`) | Phase 4bj-G | `…__stage5_research_ml_admissible__phase-4bj-g.json` | `research_eligible=false`, `eligibility_gate_status="pending"`, `chronological_split_policy="not_yet_defined"` |

The label family in particular carries the following evidence on the original manifest (per Phase 4bj-C / Phase 4bj-D / Phase 4bj-E):

- symbol: `BTCUSDT`;
- date: `2025-01-15` (single UTC day);
- row count: `1,681,098`;
- column count: `39`;
- label parquet SHA256: `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26`;
- label manifest SHA256: `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3`;
- `label_config_hash`: `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`;
- `invalid_price_row_count`: `0`;
- `censored_per_horizon`: `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}`;
- Phase 4bj-E label-family eligibility gate report: `overall_status=pass`, `72/72 PASS`, `0 FAIL / 0 ERROR / 0 NOT_APPLICABLE`, SHA256 `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`.

Across the four-family arc:

- **no ML has been trained**;
- **no strategy has been created or evaluated**;
- **no signal has been computed**;
- **no backtest has been run**;
- **no acquisition has occurred** beyond the Phase 4az single-day public archive (BTCUSDT 2025-01-15);
- **no paper / shadow / live / exchange-write has been authorized**;
- **no Phase 5 / Phase 4 canonical authorization exists**.

The arc has produced **structural admissibility evidence and governance markers**, not empirical edge evidence. Successor-state markers say "this artefact has cleared the governance gate at the stated stage"; they do not say "this artefact predicts price", "this artefact carries alpha", or "this is a strategy".

---

## 3. Definition of label evaluation

For the purposes of Prometheus, "label evaluation" is defined as a **future controlled diagnostic activity**, conducted only under a separately authorized successor phase, whose purpose is to characterise the existing label artefact as a measurement object — not as a tradable signal.

### 3.1 What label evaluation may include (future, NOT authorized by Phase 4bj-H)

In a future, separately authorized label evaluation phase, the following kinds of activity may be considered:

- **Label distribution analysis** — empirical class balance per horizon (1s, 5s, 15s, 60s), per side (long / short / neutral if applicable), and per UTC hour bucket within the locked single-day cell.
- **Horizon-level class balance** — comparison of distributions across the four locked horizons; identification of horizons where censoring or invalidity meaningfully shifts the empirical balance.
- **Censoring behaviour review** — empirical confirmation that `censored_per_horizon` values match the labels' actual null / nan / sentinel distribution, and characterisation of where censoring concentrates (e.g. last-N seconds of UTC day vs distributed across the day).
- **Null / invalid / edge-case review** — confirmation that `invalid_price_row_count` and any sentinel-row count match the on-disk artefact and that the artefact has no silent NaNs.
- **Feature-label alignment diagnostics** — joint inspection of the feature parquet (per Phase 4bi-D) and the label parquet on the same row index / timestamp axis, to confirm one-to-one alignment and detect any timestamp drift.
- **Temporal stability diagnostics** — descriptive analysis of how label distributions change within the single-day window (e.g. UTC hour bucket vs UTC hour bucket).
- **Naive baseline comparisons** — purely descriptive baselines (e.g. constant-prediction baselines, last-value baselines, sign-of-last-return baselines) reported as descriptive frequencies; these are baseline characterisations of the label, **not** strategies.
- **Leakage checks** — formal verification that label construction did not import future information; checks that feature rows used for joint inspection do not silently leak label-time data.
- **Split-readiness checks** — confirmation that the artefact is structurally compatible with a future train / validation / test split scheme, e.g. confirmation that row ordering matches strictly monotonic timestamps, no row interleaving exists, no duplicate timestamps that would break chronological partitioning, etc.

### 3.2 What label evaluation must explicitly NOT include (regardless of authorization)

The following are **out-of-scope for label evaluation under any future authorization scheme**, and any attempt to slip them in must be rejected as scope drift:

- trading **signals** of any kind (label-to-signal conversion is forbidden);
- **entry / exit rules**;
- **strategy logic**, even in pseudocode form, derived from the labels;
- **ML training**, model fitting, fine-tuning, or weight updates;
- **model selection** based on label statistics;
- **feature ranking** based on label correlations;
- **meta-labeling** (signals about signals);
- **backtesting** of any kind;
- **PnL** computation;
- **MFE / MAE / R-multiple** computation;
- **equity curves**;
- **position state** simulation;
- **alpha / edge claims**;
- **paper / shadow / live readiness** evaluation.

The rule is simple: label evaluation describes a measurement object; it never produces a trading rule. If a result of a label evaluation looks like a tradable rule, the rule must be discarded; admissibility for any such rule belongs upstream of the Phase 4ak M0 gate.

---

## 4. Chronological split boundary

No empirical label evaluation should run before a chronological split policy has been recorded, because every diagnostic that touches both features and labels is one step away from accidentally creating an in-sample / out-of-sample structure that later cannot be defended.

### 4.1 Why the boundary exists

The current label artefact spans a single UTC day (`2025-01-15`, BTCUSDT). Within that day, every row has a strictly monotonic `transact_time_ms` timestamp and a row index inherited from the source aggTrades. There is no train / validation / test partition declared on disk; the manifest carries `chronological_split_policy: "not_yet_defined"`. Any diagnostic that even silently treats two row-ranges as comparable (e.g. "early-day vs late-day distribution") is an implicit partitioning. Without a declared policy, repeated diagnostics will pollute any future formal split.

### 4.2 Required future policy dimensions

Any future chronological split policy design phase (referenced in §10 below as Phase 4bj-I or equivalent, **NOT authorized by Phase 4bj-H**) must, at minimum, decide and record:

- **Train / validation / test separation.** Whether the locked single-day cell can host any meaningful train / validation / test partition at all, or whether the day is too short for partitioning and instead must be treated as one block whose evaluation requires future multi-day acquisition.
- **Strictly forward-in-time evaluation.** Any partition must be **temporal**, never random; the test partition must contain only rows whose timestamps strictly post-date every row in the validation partition, which in turn must strictly post-date every row in the train partition.
- **No leakage from future labels into feature construction.** Confirmation that every feature row used jointly with labels uses only information available at or before that row's `transact_time_ms`. This was a Phase 4bh contract; any future label-evaluation phase must re-verify it on the joint dataset.
- **No same-day-only over-claiming.** The single-day cell may be insufficient for any statistical claim about generalisation; the policy must record this limitation and prevent over-claiming.
- **Single-day limitation of BTCUSDT / 2025-01-15.** The split policy must state that the locked cell is one UTC day, one symbol, and that any conclusion is conditional on that cell. Multi-day expansion is not authorized.
- **Embargo / purge consideration if overlapping horizons create leakage.** Labels carry horizons of 1 s / 5 s / 15 s / 60 s. A naive partition at timestamp `T` would let the train side end at `T` while a label for a train row whose anchor is at `T - 30 s` covers a 60-second horizon that overlaps the test side. The policy must specify whether an embargo (gap rows excluded near partition boundaries) or purge (rows whose label horizon crosses the boundary excluded) is required, and how long.
- **Treatment of censored rows.** The 9 / 42 / 118 / 507 censored rows per horizon must be classified explicitly: kept-with-null-label, excluded, or treated as a separate diagnostic stratum. The policy must record this choice before any diagnostic uses it.
- **Treatment of rows near UTC day boundaries.** Rows in the last 60 seconds of the day have horizons that would extend beyond the day; how this is treated must be predeclared (currently these are part of the censored counts).
- **Reproducible split artefact requirements.** Any future split must be deterministic, reproducible from the label artefact + a declared policy, and must produce an artefact whose path, size, and SHA256 are recorded.
- **Sibling artefact, not manifest mutation.** Following the Phase 4bg-B / 4bi-D / 4bj-G pattern, any split must be recorded as a sibling artefact under a gitignored namespace (e.g. `data/microstructure/splits/`) rather than by mutating `chronological_split_policy` on the original label manifest. The original label manifest must remain `chronological_split_policy: "not_yet_defined"` until a separately authorized phase elects to record an explicit policy transition.

### 4.3 Why split policy must precede empirical evaluation

Repeated diagnostics on the same artefact without a fixed split create cumulative selection bias. Each time a researcher inspects the data and decides to "try a slightly different cut", the next analysis is implicitly informed by the previous. By recording the split policy in a sibling artefact **before** running diagnostics, the project creates a fixed reference frame: every later diagnostic either complies with the recorded policy or is explicitly out-of-policy and labelled as such.

This rule is **upstream of M0**. M0 admissibility cannot be evaluated on results that came from a moving partition. A split policy is a prerequisite for any later M0-cleared hypothesis study.

---

## 5. Leakage risk register

This register enumerates leakage risks any future label evaluation phase must control. Phase 4bj-H does not run any of these checks; it only records the register.

1. **Lookahead leakage.** Any computation that uses information from `t_future` to label a row at time `t` is forbidden. Phase 4bh's feature contract bars this for feature rows; Phase 4bj-C records that labels use forward windows by design, but every joint diagnostic must verify that no feature row used in a diagnostic at time `t` was computed using information at `t_future`.
2. **Feature-label timestamp misalignment.** Labels and features must be joined on a strictly aligned row index / timestamp axis. Off-by-one row alignment is a silent leakage source. Any future diagnostic must include an explicit alignment check.
3. **Overlapping horizon leakage.** Labels with horizons of 1 s, 5 s, 15 s, 60 s cover overlapping forward windows. If a partition boundary is set at timestamp `T`, a 60 s-horizon label for an anchor at `T - 30 s` reaches into the post-`T` side. An embargo or purge is required.
4. **Right-edge censoring leakage.** Censored rows near the end of the day (per `censored_per_horizon`) are not missing-at-random; they are missing because the horizon falls outside the data window. Any diagnostic that conditions on censoring without acknowledging this asymmetry is biased.
5. **Same-day overfitting.** With one UTC day, repeated analyses will overfit the day-level dynamics (intraday seasonality, exchange-event idiosyncrasies, etc.). No generalisation claim can be made from a single day. Any conclusion is conditional on this exact cell.
6. **Hyperparameter / model-selection leakage.** Even before training, the act of selecting which diagnostic to run based on prior diagnostics' outcomes leaks information across the split. The future policy must include a "diagnostics budget" or pre-registered checklist.
7. **Repeated-analysis leakage.** Each repeated read of the data informs implicit selection. The future policy should record how many distinct analyses are permitted before the partition is "burned" and must be replaced with a new cell (e.g. a future second-day acquisition under a separately authorized phase).
8. **Strategy resurrection via labels.** Any label or label-statistic must not be interpreted as a strategy. The Phase 4al refined no-rescue rule remains binding: no V2 / G1 / C1 / R2 / F1 / D1-A rescue, no V3 / V4 cross-strategy hybrid, no "let's just look at the labels' direction and trade it".
9. **Cost-blind interpretation.** Any future result that ignores §11.6 (8 bps slippage per side; 16 bps round-trip) and §1.7.3 (0.25% risk, 2× leverage cap, one-position max, mark-price stops) is incomplete. Even descriptive label statistics must be reported with cost realism in mind; cost realism is the floor of any later edge claim.
10. **Confusing labels with signals.** The most common failure mode in label evaluation work is interpretive: "the label is positive 51% of the time, so we have a 51% signal". This is wrong on two counts: (a) the label is a forward observation, not a forecast, and (b) 51% with realistic costs is not edge. The register flags this as the single most likely scope-drift mode.

---

## 6. Input-family boundary

Any future label evaluation phase must explicitly state which input families are in scope and which are out.

### 6.1 In scope for the current governed arc

- **Existing aggTrades-derived features** (Phase 4bh / Phase 4bi-D). These are the only features the project has formally governed.
- **Existing aggTrades-derived labels** (Phase 4bj-C / Phase 4bj-D / Phase 4bj-E / Phase 4bj-G). Single UTC day, BTCUSDT.

### 6.2 Out of scope for the current governed arc

- **Price / return baselines.** Computing trivial price-based or return-based baselines for comparison may be useful in a future diagnostic, but they are **not authorized for computation by Phase 4bj-H**. Adding such a baseline requires its own scope decision and its own avoidance-of-strategy boundary, because price-return baselines can shade into trivial signal proposals.
- **Volume / trade-flow baselines.** Same status: potentially useful future comparators, **not authorized for computation here**, and they carry the same risk of accidentally becoming "signals".
- **Candle / kline context.** The project has v002 BTCUSDT 15m / 1h-derived klines and Phase 4i 30m / 4h klines, but these are not part of the aggTrades-derived arc. They are **not automatically part of any future label-evaluation phase**. Pulling them in requires their own boundary memo.
- **Order-book / depth data.** **Not acquired in this project arc.** Any order-book lane would require:
  - a data-requirements memo,
  - an acquisition-authorization memo,
  - a public-only acquisition execution phase under the Phase 4ay-style strict integrity gate,
  - a normalization design memo,
  - a normalization implementation phase,
  - a derived-family eligibility-gate design and execution,
  - a feature design and implementation phase,
  - a feature-family eligibility gate,
  - a successor-state recording phase,
  - and a label-family equivalent if labels are derived;
  before any empirical use. None of this is authorized by Phase 4bj-H.
- **Mark-price data.** Not in scope; **not acquired**; would require a separately authorized data acquisition memo and the Phase 3v §8 stop-trigger-domain governance reconciliation.
- **Spot / cross-venue data.** Out of scope and **forbidden** in v1 (one-venue, one-symbol live scope).
- **Funding / open-interest context.** Phase 4i acquired some metrics datasets; Phase 4j §11 governs the OI subset. None of this is automatically part of the aggTrades-derived label arc; merging it in would require an explicit boundary decision and would re-engage the D1-A rescue-risk pattern.

### 6.3 Critical statement

The current governed family is **aggTrades-derived**, not order-book-derived. Any new input family requires separate requirements, acquisition / governance, QA, gate, and successor-state phases before empirical use. The phrase "we already have the data" must be tested against the actual governance state of each family before any cross-family analysis is admitted.

---

## 7. Fallback lane framing

If a future authorized aggTrades-only label diagnostic returns null or near-null results, the temptation will be to "try the next idea". This memo documents, at policy level only, the kinds of fallback lanes that may be considered later — and the rules they must respect.

### 7.1 Lanes available at policy level (none authorized by Phase 4bj-H)

- **Failure interpretation memo.** First response to a null result must be a failure interpretation memo, not "try the next thing". The failure interpretation must record: what was tested, what was held fixed, what the null result actually means, what mechanism it does not prove absent, and what would constitute meaningful new evidence.
- **Price / volume baseline comparison.** If a failure interpretation memo concludes that the existing aggTrades-derived labels carry essentially no information beyond price / volume baselines, a future authorized memo could record the baselines for comparison. This is **diagnostic**, not strategy.
- **Aggressive-flow refinement within existing aggTrades data.** If the failure mode is interpretable, a future authorized phase could refine aggressive-flow features (e.g. taker-side imbalance over different windows) within the **already-acquired** aggTrades cell. No new acquisition. No new manifest. No new strategy.
- **Multi-symbol / multi-day aggTrades expansion.** A separately authorized data acquisition expansion (more days, ETHUSDT etc.) under the Phase 4ay-style integrity gate. Not authorized.
- **Order-book feasibility lane.** A docs-only feasibility memo for a hypothetical order-book lane. Not authorized.
- **Funding / open-interest context lane.** A docs-only feasibility memo, conditional on extreme caution because of the D1-A precedent (funding-as-directional-trigger failed terminally). Not authorized.
- **New label-family / horizon design.** If diagnostics suggest the locked 1 s / 5 s / 15 s / 60 s horizon set is unsuitable, a future authorized memo could propose a new label family with different horizons. Not authorized.

### 7.2 Rules governing any future fallback lane choice

- **Failure interpretation must precede "try the next idea".** No fallback may be authorized without a failure interpretation memo.
- **No order-book, mark-price, spot, cross-venue, or additional aggTrades acquisition** is authorized by Phase 4bj-H.
- **Old failed strategy families remain closed.** R2 cost-fragility, F1 catastrophic floor, D1-A mechanism / framework mismatch, V2 design-stage incompatibility, G1 regime-gate sparseness, C1 fires-and-loses anti-validation — all remain terminal for their first specs. No fallback lane may resurrect them under a label-evaluation disguise.
- **5m research thread remains closed** per Phase 3t.
- **M0 admissibility remains the gate** for any future hypothesis arising out of a fallback lane.

---

## 8. Decision options

The standard option set for Phase 4bj-H is enumerated below. Phase 4bj-H authorizes exactly one of them (Option B, the docs-only boundary memo). All other options remain unauthorized.

- **Option A — remain paused, no label evaluation boundary.** Keep the project paused without recording the boundary. Acceptable but loses the opportunity to record a durable in-repo standard for what label evaluation means and how it must be approached.
- **Option B — docs-only label evaluation / chronological split boundary memo (this phase).** Records the boundary, the chronological split policy requirement, the leakage register, the input-family boundary, the fallback-lane framing, and the safe future phase ladder. Authorizes no empirical work. Authorizes no successor.
- **Option C — future chronological split policy design phase.** A future docs-only design phase that records the locked single-day cell's partition rules (or records the determination that the cell is too small to partition). Authorized only by a separate operator prompt; **not authorized by Phase 4bj-H**.
- **Option D — future split artefact implementation phase.** A future docs + local gitignored output phase that produces the split artefact deterministically from the label artefact and the policy. **Not authorized by Phase 4bj-H**.
- **Option E — future label diagnostic study phase after split policy.** A future docs + local gitignored output phase that runs the predeclared label diagnostics under the recorded split. **Not authorized by Phase 4bj-H**.
- **Option F — ML / strategy / backtest / acquisition now.** **Forbidden / not recommended.** Skipping the boundary, the split, and the diagnostics in order to "just train something" violates M0 admissibility, the Phase 4al refined no-rescue rule, the Phase 4ak post-null cooldown rule, and the project's safety posture. Authorizing this would be a regression to a state the cumulative six-failure topology has already disqualified.

---

## 9. Recommendation

Phase 4bj-H recommends:

- **Now:** Option B — record this docs-only boundary memo (Phase 4bj-H) and merge it under the Phase 4bk-A workflow when the operator separately authorizes the merge.
- **Future next, if separately authorized:** Option C — a chronological split policy design phase (referenced below as Phase 4bj-I or equivalent), docs-only, recording the partition rules for the single-day cell or recording the determination that the cell cannot be partitioned.
- **Do not proceed directly** to label diagnostics (Option E), split artefact implementation (Option D), ML, strategy, backtesting, or any acquisition. These remain unauthorized and require their own separately authorized successor phases.

The default state is **remain paused** unless the operator separately authorizes a future Phase 4bj-I-equivalent chronological split policy design phase.

---

## 10. Future phase ladder

The safe future sequence, **none of which is authorized by Phase 4bj-H**, is:

| Hypothetical phase id | Type | Scope | Status |
| --- | --- | --- | --- |
| Phase 4bj-I (or equivalent) | docs-only | Chronological Split Policy Design Memo: enumerates partition options for the locked BTCUSDT 2025-01-15 cell, records embargo / purge requirements, records the recommended sibling-artefact recording approach. | **NOT authorized** |
| Phase 4bj-J (or equivalent) | docs + local gitignored output | Split Artefact Implementation / Recording: deterministically derives the split artefact from the label artefact and the policy; records the artefact under `data/microstructure/splits/` (or analogue) with paired SHA256 sidecar; preserves the label manifest byte-identically. | **NOT authorized** |
| Phase 4bj-K (or equivalent) | docs-only | Label Diagnostic Study Plan: predeclared diagnostics list, predeclared falsification criteria, predeclared diagnostics budget, predeclared stop conditions, predeclared output paths. | **NOT authorized** |
| Phase 4bj-L (or equivalent) | docs + local gitignored output | Label Diagnostic Study Execution: runs only the predeclared diagnostics; records descriptive results under a gitignored namespace; does not produce strategy or ML output. | **NOT authorized** |
| Later — ML feasibility memo | docs-only | Whether and under what M0 admissibility a future baseline ML diagnostic could be considered. | **NOT authorized** |
| Later — baseline ML diagnostic | docs + local gitignored output | A predeclared baseline classifier or regressor on the labels under the recorded split; produces descriptive evaluation metrics only; **not** a strategy. | **NOT authorized** |
| Later — failure interpretation / fallback selection memo | docs-only | If diagnostics return null or near-null, record the interpretation before choosing a fallback lane. | **NOT authorized** |
| Later — strategy hypothesis under M0 | docs-only | Only after a positive, M0-admissible, mechanism-grounded hypothesis emerges from upstream evidence. | **NOT authorized** |
| Later — strategy spec | docs-only | Full ex-ante strategy specification mirroring the Phase 4g / Phase 4p / Phase 4v pattern. | **NOT authorized** |
| Later — backtest plan | docs-only | Methodology memo mirroring Phase 4k / Phase 4q / Phase 4w. | **NOT authorized** |
| Later — backtest execution | docs + code | Standalone research script execution mirroring Phase 4l / Phase 4r / Phase 4x. | **NOT authorized** |
| Paper / shadow / live | many phases | Only much later, under separate authorization, after live-capable runtime work that does not yet exist. | **NOT authorized** |

Each step is its own phase, each requires its own operator authorization, and each is subject to the Phase 4ak M0 twelve-clause gate plus the Phase 4al refined no-rescue rule.

---

## 11. M0 and no-rescue integration

- **Label evaluation is upstream of M0 admissibility.** Diagnostics describe a measurement object; they do not by themselves clear the M0 mechanism-admissibility gate. Any future hypothesis that wants to use label-derived evidence still has to pass M0 on its own merits (mechanism source, baseline-superiority theory, predicted Δ_R derivation, design-family distance from cooled-down families, cost realism, opportunity rate viability separate from edge rate viability, edge rate viability, data feasibility, governance compatibility, forbidden-rescue check, predeclared falsification criteria, post-null cooldown compliance, non-authorization clause).
- **ML diagnostics cannot become a strategy without M0 admission.** A baseline classifier's accuracy or AUC is not a strategy; producing such numbers does not by itself authorize trading. The Phase 4ak twelve-clause M0 gate remains binding.
- **Labels are not signals.** This is restated for emphasis: a label is a forward-looking observation by construction; calling its value at row `t` a "signal" is a category error.
- **Labels are not strategy evidence.** A label distribution is descriptive evidence about the observation; it is not, by itself, evidence that any rule based on observed labels would be profitable under §11.6 cost realism.
- **Successor-state markers are governance markers, not empirical edge claims.** The Phase 4bg-B / 4bi-D / 4bj-G / 4bb-G markers say "this artefact has cleared the structural gate at the stated stage"; they say nothing about market behaviour, edge, predictability, or profitability.
- **Retained failed strategy families remain closed.** R2, F1, D1-A, V2, G1, C1 first-specs are terminal as research evidence; no rescue, no -prime, no narrow / extension / relaxation / hybrid is authorized.
- **5m research thread remains operationally closed** per Phase 3t.

---

## 12. Explicit non-authorizations

Phase 4bj-H **does not authorize** any of the following, and this section enumerates them so a future reader cannot misread the boundary as authorization:

- Phase 4bj-I (or any future chronological split policy design phase);
- Phase 4bj-J / Phase 4bj-K / Phase 4bj-L (or any future split-artefact / diagnostic-plan / diagnostic-execution phase);
- any Phase 5, Phase 4 canonical, Phase 4bj-anything, or any other successor phase;
- chronological split artefact creation;
- label diagnostic execution;
- ML implementation;
- ML training;
- model selection;
- feature ranking;
- meta-labeling;
- strategy implementation;
- signal computation;
- backtesting;
- additional data acquisition of any kind;
- order-book acquisition;
- mark-price acquisition;
- spot / cross-venue acquisition;
- funding / open-interest acquisition;
- paper / shadow operation;
- live-readiness work;
- deployment;
- production-key creation;
- authenticated API access;
- private-endpoint access;
- public-endpoint calls in code;
- user-stream subscription;
- WebSocket usage;
- MCP enablement;
- Graphify enablement;
- `.mcp.json` creation or modification;
- credential creation, reading, or storage;
- exchange-write capability of any kind;
- any manifest transition;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual manifest;
- mutating `chronological_split_policy` on the original label manifest (any future split policy must be recorded as a sibling artefact);
- revising any retained verdict;
- loosening any project lock;
- amending M0 governance.

---

## 13. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

---

## 14. Preserved locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% risk per trade / 2× leverage cap / one-position max / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path policy (raw → `gate-reports/raw/`, normalized → `gate-reports/normalized/`, features → `gate-reports/features/`, labels → `gate-reports/labels/`, successor-state → flat under `successor-state/`)

All prior phase results preserved verbatim.

---

## 15. Current-project-state update

`docs/00-meta/current-project-state.md` is updated narrowly to record Phase 4bj-H:

- A new Phase 4bj-H narrative paragraph is added above the existing Phase 4bb-G paragraph.
- The "Current phase:" block is replaced with a Phase 4bj-H block whose content mirrors this memo's headline guarantees:
  - Phase 4bj-H is docs-only;
  - it authorizes no empirical label evaluation;
  - it authorizes no split artefact;
  - it authorizes no new data acquisition;
  - it authorizes no ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write;
  - recommended state remains paused unless the operator separately authorizes a future chronological split policy design phase.
- The prior Phase 4bb-G "Current phase:" block is preserved as historical context under a section heading consistent with prior phases.

No other tracked file in `docs/00-meta/current-project-state.md` is reorganised or rewritten. The retained verdict ledger, project locks, and prior narrative paragraphs are unchanged.

---

## 16. Validation

This phase is docs-only. Validation gates applied:

- `git diff --check` — clean.
- `git status` — clean except always-untracked `.claude/scheduled_tasks.lock` + gitignored `data/research/`.
- `ruff` / `mypy` / `pytest` — **not rerun**. Phase 4bj-H modifies no source code, no tests, no scripts, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the Phase 4bb-F-implementation merge: `ruff check .` PASS, `mypy strict 120 source files` PASS, `pytest tests/research/microstructure/` 915 passed + 1 pre-existing labelled skip, whole-repo pytest 1698 passed + 1 skipped + 2 pre-existing simulation `KeyError: 'trade_count'` failures (unchanged from prior phases; not introduced by this phase).

---

## Final note

Phase 4bj-H is **branch-complete only** after this work. Per the Phase 4bk-A workflow standard, Phase 4bj-H is **NOT project-complete** until a separately authorized merge phase records its merge-closeout on `main`. No merge is performed by this phase. No successor is authorized.

The recommended state is **remain paused** unless and until the operator separately authorizes a future Phase 4bj-I-equivalent chronological split policy design phase.
