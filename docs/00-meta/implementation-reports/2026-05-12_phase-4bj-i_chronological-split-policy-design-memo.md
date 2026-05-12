# Phase 4bj-I — Chronological Split Policy Design Memo

**Phase identity:** Phase 4bj-I — Chronological Split Policy Design Memo (docs-only).
**Date:** 2026-05-12.
**Branch:** `phase-4bj-i/chronological-split-policy-design-memo`.
**Base:** `main` at `49d60b6e362294541b4f45f49c6e0b389b70b5b9` (Phase 4bj-H SHA-chain-fixup commit on top of merge-closeout `65e9094a46eb6423ac6132ea394a62a7e860c55d`).
**Status:** drafted; pending operator review.
**Phase type:** docs-only design / governance memo.

A note on the SHA-chain pattern: the Phase 4bj-H merge-closeout itself anchored its §2 final-SHA value at the merge-closeout commit `65e9094`. The one-commit fixup on top of that anchor (commit `49d60b6`) only records the final-`main` SHA back into §2 of the Phase 4bj-H merge-closeout; it does not change Phase 4bj-H lifecycle semantics. Phase 4bj-I branches from `49d60b6` because that is the post-fixup `main` state; the canonical "Phase 4bj-H project-complete" anchor remains the merge-closeout commit (`65e9094`).

---

## 1. Phase identity

- **Phase name:** Phase 4bj-I — Chronological Split Policy Design Memo.
- **Phase type:** docs-only design / governance memo.
- **Branch:** `phase-4bj-i/chronological-split-policy-design-memo`.
- **Base SHA:** `main` at `49d60b6e362294541b4f45f49c6e0b389b70b5b9`.
- **Predecessor anchor:** Phase 4bj-H merge-closeout `65e9094a46eb6423ac6132ea394a62a7e860c55d` (project-complete).
- **Authorization:** explicit operator authorization for Phase 4bj-I only.

Phase 4bj-I is **strictly docs-only**. It does **not**:

- create a split artefact of any kind;
- create train / validation / test partitions on disk;
- evaluate labels or compute label statistics;
- read or process the label parquet beyond documentation-level references already recorded in repo docs (Phase 4bj-B / 4bj-C / 4bj-D / 4bj-E / 4bj-G / 4bj-H);
- train ML or design ML architecture;
- rank features or create meta-labeling;
- create a strategy, compute signals, or run backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output;
- acquire data of any kind (order-book, mark-price, spot, cross-venue, funding, open-interest, additional aggTrades);
- call public, authenticated, or private endpoints;
- open WebSockets or user streams;
- create or read credentials, `.env`, or `.mcp.json`;
- enable MCP or Graphify;
- modify any source code, test, script, `pyproject.toml`, `README.md`, `.gitignore`, or MCP file;
- modify any manifest, parquet, sidecar, raw zip, gate report, or successor-state artefact under `data/microstructure/`;
- flip `research_eligible` on any manifest;
- transition `eligibility_gate_status` on any manifest;
- change `chronological_split_policy` on any actual manifest (the label manifest's `chronological_split_policy` must remain `"not_yet_defined"` until a separately authorized successor-state phase records a transition via a sibling artefact);
- modify project locks, retained verdicts, or M0 governance;
- authorize Phase 4bj-J / 4bj-K / 4bj-L, Phase 5, Phase 4 canonical, or any successor phase.

Tracked changes by Phase 4bj-I are exactly two new docs (this memo + the Phase 4bj-I closeout) plus a narrow paragraph + "Current phase:" block update in `docs/00-meta/current-project-state.md`. No `data/microstructure/` artefact, no local gitignored file, no source / test / script / config file is created or modified.

---

## 2. Pre-state and evidence boundary

### 2.1 Phase 4bj-H boundary result (predecessor)

Phase 4bj-H (project-complete at merge-closeout `65e9094`) recorded the **label-evaluation / chronological split boundary** at policy level: label evaluation is a future controlled diagnostic activity, never a strategy or signal; no empirical label evaluation may run before a chronological split policy exists; any future split policy must be recorded as a **sibling artefact** under a gitignored namespace, never as a mutation of the original label manifest. Phase 4bj-H named Phase 4bj-I as the cleanest non-paused successor option but did **not** authorize it. The operator has now separately authorized Phase 4bj-I, narrowly, as docs-only.

### 2.2 Label-family state

| Field | Value |
| --- | --- |
| Family | `microstructure_labels_aggtrades_v001` |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (single UTC day) |
| Row count | `1,681,098` |
| Column count | `39` |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| `invalid_price_row_count` | `0` |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| `research_eligible` | `false` (unchanged) |
| `eligibility_gate_status` | `"pending"` (unchanged) |
| `chronological_split_policy` | `"not_yet_defined"` (unchanged) |
| Phase 4bj-E label-family gate report SHA256 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` (PASS; 72/72) |
| Phase 4bj-G label-family successor-state JSON SHA256 | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |

### 2.3 Governed-artefact chain

Across the four microstructure aggTrades families (raw / derived / feature / label) every family now has:

- a sibling successor-state JSON marker under the gitignored `data/microstructure/successor-state/` namespace;
- an original manifest preserved with `research_eligible: false` and `eligibility_gate_status: "pending"`;
- local artefacts preserved byte-identically through every recording phase;
- no manifest transition; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved.

No empirical label evaluation has been run. No split artefact exists. No ML, strategy, signal, backtest, acquisition, paper / shadow / live work has been authorized at any time during the arc. No data has been acquired beyond the single Phase 4az public archive (BTCUSDT 2025-01-15 aggTrades).

The current research cell is therefore: **one symbol (BTCUSDT), one UTC day (2025-01-15), 1,681,098 rows, 4 forward horizons (1s / 5s / 15s / 60s), 0 invalid-price rows, 676 censored rows total across the 4 horizons**.

---

## 3. Chronological split policy question

The questions Phase 4bj-I must answer at design / policy level:

### 3.1 Can BTCUSDT / 2025-01-15 be safely split into train / validation / test for empirical label evaluation?

**A formal "train / validation / test" split in the statistical-learning sense is NOT safe on this single-day cell.** A train / validation / test split is meaningful when:

- the test partition is representative of out-of-sample conditions the system will encounter in live use;
- repeated evaluation on the test partition is constrained;
- the partitions span enough independent samples that selection bias from repeated diagnostics can be characterised.

The single-day cell fails all three conditions:

- intraday cells are highly dependent on the day's specific regime (volatility, news, exchange events, hour-of-day liquidity profile). A test partition drawn from later hours of 2025-01-15 is not representative of out-of-sample market conditions; it is representative of "the same day, later". This is closer to a within-sample temporal partition than to a held-out generalisation test.
- with only one day, every repeated diagnostic shares the same day-of-data, so cumulative selection bias is concentrated on a single fixture. There is no parallel cell that future diagnostics can move to once this fixture is exhausted.
- statistical generalisation across days, symbols, regimes, or weeks cannot be characterised from a single 24-hour window.

### 3.2 Is a split for descriptive diagnostics only?

**Yes — and this is the only kind of split that is admissible on the single-day cell.** A descriptive within-day temporal segmentation, used purely to characterise label distribution / censoring / alignment / leakage-check behaviour, with explicit acknowledgement that **no segment can be treated as a held-out generalisation test**, is admissible at policy level (subject to a separately authorized successor implementation / recording phase). Such a segmentation must not borrow the train / validation / test vocabulary.

### 3.3 Can the split support ML training?

**No.** The single-day cell is insufficient for ML training of any kind that purports to estimate generalisation. Even a "baseline" classifier or regressor on the single-day cell can only describe how labels relate to features on that day; it cannot estimate out-of-sample performance, and any reported accuracy / AUC / loss number is a descriptive measurement of within-day fit, not a model-quality claim.

### 3.4 Can the split support strategy / backtest claims?

**No.** A split on this cell carries zero strategy-evidence weight under §11.6 cost realism, §1.7.3 sizing locks, and M0 admissibility. Any future strategy derived from the cell would need to clear M0 on its own merits and would need to be evaluated on a different, separately-acquired evidence base.

### 3.5 What are the limitations of single-day splitting?

- **Single-symbol limitation.** BTCUSDT only. ETHUSDT and any alt-symbol generalisation is out of scope of this cell.
- **Single-day limitation.** No multi-day, multi-week, multi-regime, multi-event-day characterisation is possible.
- **Same-day overfitting risk.** Repeated diagnostics on the cell pollute its statistical value over time. The cell has a finite information budget.
- **Intraday regime dependence.** US session, Asia overnight, exchange-event spikes, funding ticks all happen within the day and can dominate any partition's behaviour.
- **Right-edge censoring asymmetry.** 60s-horizon censoring concentrates in the last 60s of the UTC day, biasing the late-day partition.
- **No statistical generalisation claim possible.** Any positive-looking result on this cell must be treated as a "could be interesting on this exact day" observation, not as a generalisation claim.

---

## 4. Candidate split designs

Six policy options are evaluated. Each is described, and each is given a verdict.

### 4.1 Option A — no split; remain paused

Keep `chronological_split_policy: "not_yet_defined"` on the label manifest. No split artefact, no segmentation, no diagnostics. The cell remains structurally available for a separately authorized future expansion phase that brings in additional data before any partitioning is attempted.

Verdict: **maximally conservative**. Avoids selection-bias risk on the cell entirely. Acceptable.

### 4.2 Option B — single-day descriptive split with train / validation / test partitions

Partition the 24-hour day into three temporal segments and label them "train", "validation", "test".

Verdict: **NOT RECOMMENDED.** The vocabulary "train / validation / test" implies a generalisation claim the single-day cell cannot support. Using this vocabulary on a single-day cell is the most likely scope-drift mode and creates lasting confusion in the project record about what the cell can and cannot prove. Even a strict "descriptive only" annotation would be eroded by repeated re-reading; the vocabulary itself signals statistical learning.

### 4.3 Option C — single-day calibration / holdout split without ML permission

Partition the day into two or three segments using neutral vocabulary (e.g. "early", "middle", "late" or "fixture-A", "fixture-B", "fixture-C"). Forbid model fitting. Allow only descriptive comparison of label distributions, censoring, and alignment across segments. Record purge / embargo rules around segment boundaries to control overlapping-horizon leakage.

Verdict: **acceptable if explicitly descriptive-only.** Preserves the ability to inspect within-day stability without implying generalisation. The vocabulary must be neutral; "calibration / holdout" itself shades toward ML and should be avoided in the policy artefact.

### 4.4 Option D — declare single-day cell insufficient for formal train / validation / test; require multi-day expansion before empirical diagnostics

Record the determination that the cell is too small for formal train / validation / test, do not create a split artefact yet, and define what minimum future data expansion (multi-day same-symbol; multi-symbol same-day; both) would be required before any formal generalisation-style partitioning is attempted. Permit a future explicit "no-split determination" recording artefact under the same Phase 4bj-J / equivalent successor pattern.

Verdict: **RECOMMENDED PRIMARY OPTION.** Honest about the cell's evidentiary capacity. Avoids creating an artefact that would later have to be unwound. Permits future descriptive within-day segmentation under a separately authorized phase if and only if the segmentation uses neutral vocabulary, is explicitly descriptive-only, and is recorded as a sibling artefact.

### 4.5 Option E — future split artefact implementation phase after policy selection

A future Phase 4bj-J-equivalent that produces a sibling split artefact (or a sibling no-split determination artefact) under `data/microstructure/splits/` (or analogue), deterministically reproducible from the label artefact + the policy recorded in Phase 4bj-I.

Verdict: **conditional future option only; NOT authorized by Phase 4bj-I.** Phase 4bj-I is design only; implementation requires a separately authorized prompt.

### 4.6 Option F — label diagnostics / ML / strategy / backtest now

Skip the split policy and proceed directly to label diagnostics, ML training, strategy hypothesis generation, or backtesting on the single-day cell.

Verdict: **FORBIDDEN / NOT RECOMMENDED.** Violates M0 admissibility, the Phase 4al refined no-rescue rule, the Phase 4ak post-null cooldown rule, and the project's safety posture. The cumulative six-failure rejection topology (R2 / F1 / D1-A / V2 / G1 / C1 first-specs) was reached precisely because earlier work skipped exactly these kinds of gates.

---

## 5. Recommended split policy

**Primary recommendation: Option D — declare the single-day BTCUSDT 2025-01-15 cell insufficient for formal train / validation / test, and remain unsplit until multi-day data exists.**

This recommendation is recorded with the following specifics.

### 5.1 Why single-day data is insufficient

The cell carries 1,681,098 aggTrades-derived rows on one symbol on one UTC day. Forward horizons are 1s / 5s / 15s / 60s. The cell cannot support:

- a generalisation-style train / validation / test partition (no out-of-sample condition);
- ML training that purports to estimate generalisation (no held-out cell);
- strategy or backtest claims under §11.6 cost realism (no multi-regime evidence);
- repeated independent diagnostics on the same partition (finite information budget).

The cell **can** support, at policy level, future descriptive within-day characterisation under a separately authorized successor phase, provided neutral vocabulary is used, ML permission is withheld, and outputs are explicitly described as "characterisation of this specific cell, not evidence of generalisation".

### 5.2 Minimum future data expansion required for formal partitioning

If, in the future, a separately authorized acquisition phase brings in:

- at least **30 distinct UTC days** of BTCUSDT aggTrades data spanning multiple weekly cycles, multiple exchange-event days (high-volatility spikes), and multiple session profiles; and / or
- at least one **second symbol** (ETHUSDT) on the same set of days for cross-symbol comparison;

then a formal chronological train / validation / test partition could be considered under a separately authorized future policy design memo. The 30-day floor is a heuristic anchor only; the actual minimum depends on stability of label distributions, censoring fractions, and intraday seasonality across the acquired days. **No future acquisition phase is authorized by Phase 4bj-I.**

### 5.3 Temporary descriptive segmentation rules (only if a future Phase 4bj-J-equivalent authorizes it)

If a future separately authorized successor phase elects to permit a temporary within-day descriptive segmentation, it must:

- use **neutral vocabulary** ("fixture-A / fixture-B / fixture-C" or "early-day / mid-day / late-day"; **never** "train / validation / test"; **never** "calibration / holdout");
- declare the segmentation **descriptive-only** in the sibling artefact;
- declare **ML training forbidden** on every segment;
- declare **strategy claims forbidden** on every segment;
- treat any positive-looking result as conditional on this exact cell with no generalisation claim;
- record per-row inclusion / exclusion via masks, never via rewriting the label parquet;
- specify exact UTC time boundaries (preferred over percentage ranges, to avoid implicit row-count assumptions);
- specify a per-horizon embargo / purge rule (§6 below);
- specify the censored-row handling rule (§7 below);
- specify the right-edge handling rule (§8 below).

### 5.4 No split artefact should be created yet

Phase 4bj-I does not authorize any split artefact. A future Phase 4bj-J-equivalent — which may record either a sibling split artefact (under §5.3 rules) or a sibling no-split determination artefact (under §5.1) — is the appropriate next step. Phase 4bj-I records the **policy**; Phase 4bj-J-equivalent would record the **artefact**.

### 5.5 Partition definitions (recorded for the future Phase 4bj-J-equivalent's reference; NOT authorized by Phase 4bj-I)

If the operator later authorizes a within-day descriptive segmentation under §5.3 rules, the recommended structure (subject to revision by the future authorizing prompt) would be:

| Segment | UTC time range | Approx. row share | Permitted use |
| --- | --- | --- | --- |
| `fixture-A` | `[2025-01-15 00:00:00, 2025-01-15 08:00:00)` | ~ Asia / early-EU session band | descriptive-only |
| `fixture-B` | `[2025-01-15 08:00:00, 2025-01-15 16:00:00)` | ~ EU / pre-US-open band | descriptive-only |
| `fixture-C` | `[2025-01-15 16:00:00, 2025-01-15 23:59:00)` *(last 60s reserved as right-edge zone)* | ~ US / late-day band | descriptive-only |

These boundaries are **suggestive only**. The actual segmentation boundaries (if any future phase records them) must be predeclared in the Phase 4bj-J-equivalent authorization prompt, must be deterministic given the label parquet and the policy, and must not be chosen by inspecting the data first. Row counts in the table above are session-band heuristics; the future implementation must enforce the time ranges, not the row shares.

### 5.6 Allowed and forbidden uses (binding)

- **Allowed under future Phase 4bj-J-equivalent (if separately authorized):** descriptive label distribution per segment; descriptive censoring behaviour per segment; descriptive feature-label alignment per segment; descriptive temporal-stability comparison across segments; descriptive leakage checks across segment boundaries.
- **Forbidden under any future authorization scheme:** training any model on any segment; selecting models / hyperparameters based on any segment; reporting a result on one segment as a generalisation claim about another segment; treating any segment as evidence for a strategy or signal; computing PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output on any segment; using the cell to bypass M0 admissibility.

---

## 6. Embargo / purge policy

The labels have overlapping forward horizons: 1s, 5s, 15s, 60s. The longest horizon is 60s. Without an embargo / purge rule, a partition boundary at timestamp `T` allows leakage: a label for an anchor row at `T - 30s` covers the 60s horizon `[T - 30s, T + 30s]`, which crosses into the partition that begins at `T`.

### 6.1 Required policy (binding on any future Phase 4bj-J-equivalent that records a within-day segmentation)

- **Embargo zone after a boundary:** rows with anchor timestamps in the interval `[T, T + 60s)` (after a boundary at `T`) must be excluded from the next segment for purposes of any cross-segment comparison whose label horizon could reach back into the prior segment. The 60s embargo applies because 60s is the maximum forward horizon in the locked label set.
- **Purge zone before a boundary:** rows with anchor timestamps in the interval `[T - 60s, T)` (before a boundary at `T`) must be either purged from the prior segment or labelled "boundary-overlap" if kept, because their label horizons cross into the next segment. The 60s purge applies for the same reason.
- **Per-horizon variation:** the simplest and recommended policy is to use the maximum-horizon-based 60s purge / embargo for every comparison. A more granular policy (1s embargo for 1s-horizon analyses; 5s for 5s; 15s for 15s; 60s for 60s) is admissible but adds complexity; it should be considered only if a future authorized phase records the trade-off explicitly. Phase 4bj-I recommends the **uniform 60s purge / embargo** as the default.
- **Random splits are forbidden.** Under no circumstances may any future split artefact randomly partition rows. Every partition must be deterministic, chronological, and respect UTC time order.
- **Per-row inclusion / exclusion mask:** the future split artefact must record per-row inclusion masks (one mask per segment, one mask per "boundary-overlap" region per horizon if a per-horizon scheme is adopted), never by rewriting the label parquet. The parquet remains byte-identical.

### 6.2 Embargo / purge artefact shape (recommendation only)

The future split artefact's per-row mask should be expressible as: for each `row_index` in `[0, 1681097]`, an integer or label indicating segment membership and a horizon-eligibility bitmask indicating which of the 4 horizons (1s / 5s / 15s / 60s) the row is eligible for in the segment-comparison context. Rows in a boundary embargo / purge zone are marked excluded for the affected horizons but remain present in the parquet.

---

## 7. Censoring policy

The locked label artefact records:

```text
censored_per_horizon = {"1s": 9, "5s": 42, "15s": 118, "60s": 507}
```

This means 9 rows have a censored 1s label, 42 have a censored 5s label, etc. Censoring concentrates at the right edge of the UTC day (rows whose anchor is near the day boundary), because the forward horizon would extend past the day's data window.

### 7.1 Required policy (binding on any future Phase 4bj-J-equivalent)

- **Keep censored rows for non-label diagnostics.** A row with a censored 60s label may still have a valid 1s label, valid features, valid timestamps, and valid metadata. Censored rows must be retained for any diagnostic that does not depend on the censored horizon (e.g. feature-distribution-by-segment, timestamp-alignment checks, censoring-rate-by-segment).
- **Exclude censored rows per-horizon for label diagnostics.** A diagnostic that operates on the 60s-horizon labels must exclude the 507 rows whose 60s label is censored. The same row may be retained for 1s-horizon diagnostics if its 1s label is not censored.
- **Censored-row audit stratum.** The future split artefact should optionally define a dedicated "censored" stratum (per horizon) that allows future diagnostics to characterise the censoring behaviour itself. This stratum is descriptive-only and must not be combined with non-censored strata when computing horizon-specific statistics.
- **Report censored-row handling explicitly.** Every future descriptive diagnostic must report, per horizon, the count of rows excluded due to censoring. Silent exclusion is forbidden.

### 7.2 Treatment in the future split artefact

The per-row mask should record, per horizon, whether the row's label for that horizon is censored. A diagnostic operating on horizon `H` then iterates over rows with non-censored `H` labels.

---

## 8. Single-day limitation

This section restates the limitations recorded in §3.5 and adds policy consequences.

- **BTCUSDT / 2025-01-15 is a single-symbol, single-UTC-day cell.** No multi-day, multi-symbol, multi-regime characterisation is possible from this cell alone.
- **Same-day overfitting risk is high.** Every repeated diagnostic on this cell shares the same day-of-data. Cumulative selection bias accumulates on a single fixture.
- **Intraday regime dependence is unmodelled.** Any positive-looking result may simply reflect the day's specific session profile, exchange events, or news flow.
- **No generalisation claim is possible.** A future diagnostic that produces a positive-looking result must report it as "characterisation of BTCUSDT 2025-01-15 only" and must not claim that the result would hold on any other day, symbol, or regime.
- **Right-edge censoring is asymmetric.** 60s-horizon censoring concentrates in the last 60s of the day. Any segment that includes the last 60s of the day has structurally more 60s-label censoring than earlier segments. Future diagnostics must report this asymmetry.
- **Label diagnostics can be descriptive only.** §6, §7, §8 of this memo, plus the Phase 4bj-H boundary memo's leakage register, constrain any future descriptive label diagnostic. No diagnostic on this cell can produce strategy / signal / ML evidence.
- **Future multi-day / multi-symbol expansion is unauthorized.** If the operator later wishes to expand the cell, a separately authorized data-requirements memo + acquisition memo + acquisition execution phase + family-by-family normalization / gate / successor-state recording sequence is required. Phase 4bj-I does not authorize any of those.

---

## 9. Sibling split-policy / split-artefact design

This section specifies what a future split-policy artefact or split artefact should contain **if** a separately authorized Phase 4bj-J-equivalent is later authorized. Phase 4bj-I does **not** authorize that phase, and does **not** create the artefact.

### 9.1 Required fields (minimum schema)

The future sibling artefact's JSON content should record, at minimum:

- `schema_version` — `"v001"`.
- `phase` — `"4bj-J"` (or whichever phase records it).
- `artefact_type` — `"label_family_split_policy"` or `"label_family_no_split_determination"`.
- `source_label_family` — `"microstructure_labels_aggtrades_v001"`.
- `source_label_version` — `"v001"`.
- `source_symbol` — `"BTCUSDT"`.
- `source_utc_date` — `"2025-01-15"`.
- `source_label_parquet_path` — the canonical path (recorded as the locked path inside the artefact; the parquet itself remains byte-identical and lives at its gitignored on-disk location).
- `source_label_parquet_sha256` — `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26`.
- `source_label_manifest_path` — canonical manifest path.
- `source_label_manifest_sha256` — `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3`.
- `label_config_hash` — `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`.
- `row_count` — `1681098`.
- `column_count` — `39`.
- `horizons` — `["1s", "5s", "15s", "60s"]`.
- `horizon_seconds` — `[1, 5, 15, 60]`.
- `split_policy_name` — neutral name (e.g. `"single_day_descriptive_segmentation_v001"` or `"single_day_no_split_determination_v001"`).
- `split_policy_status` — `"recorded"` (the policy is recorded; the artefact does not authorize empirical diagnostics).
- `partition_definitions` — list of partition records, each with `name`, `utc_start`, `utc_end_exclusive`, `purpose: "descriptive_only"`, `permitted_uses`, `forbidden_uses`. May be the empty list under a no-split determination.
- `purge_embargo_parameters` — record with `policy: "uniform_60s_purge_embargo"` (or `"per_horizon_purge_embargo"` if the future phase elects that), `purge_seconds_before_boundary: 60`, `embargo_seconds_after_boundary: 60`, applicability scope.
- `censored_row_handling` — record matching §7: keep for non-label diagnostics; exclude per-horizon for label diagnostics; censored stratum optional.
- `per_horizon_eligibility_rules` — record matching §6.2: per-row mask per horizon.
- `no_manifest_mutation_confirmation` — `true` (the artefact records the policy at sibling level; the original label manifest is **not** mutated).
- `non_authorizations` — list mirroring §14 (no ML, no strategy, no signal, no backtest, no acquisition, no paper / shadow / live, no exchange-write, etc.).
- `recommended_state` — `"remain_paused"`.
- `created_at_utc` — ISO-8601 UTC timestamp.
- `created_at_unix_ms` — integer.
- `code_commit_sha` — the SHA at which the artefact was generated.
- `base_commit_sha` — the predecessor `main` SHA.
- `boundary_confirmations` — full enumerated list of preserved boundaries.

### 9.2 File layout (recommendation)

- **Path:** `data/microstructure/splits/microstructure_labels_aggtrades_v001__v001__{policy_name}__phase-4bj-j.json` (or analogue).
- **Paired SHA256 sidecar:** same path + `.sha256`, body format `<sha>  <basename>\n` (two spaces, trailing newline), per the Phase 4bb-F canonical-path / sidecar policy.
- **Gitignored** under `.gitignore:85: data/microstructure/`.
- **Not committed.**
- **Original label parquet, label manifest, both sidecars, Phase 4bj-E gate report + sidecar, Phase 4bj-G successor-state JSON + sidecar all remain byte-identical** across the future Phase 4bj-J-equivalent.
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved** (never invoked).

### 9.3 Critical interpretation

If and when the future Phase 4bj-J-equivalent records the artefact:

- The label manifest's `chronological_split_policy` field remains `"not_yet_defined"`. The future artefact records the policy at the **sibling** level only.
- Any tool that wishes to interpret the cell as having a split policy must read the sibling artefact, not the label manifest, and must not assume that `chronological_split_policy` should be mutated.
- The artefact records governance; it does not record empirical edge, model fit, signal quality, or strategy approval.

---

## 10. Label evaluation gating

Before any future Phase 4bj-K / Phase 4bj-L-equivalent (label diagnostic plan / execution), the following must exist on `main`:

| Prerequisite | Status |
| --- | --- |
| Phase 4bj-I (this memo) merged to `main` with merge-closeout | **NOT yet** (per operator instruction: stop at branch-complete) |
| Future Phase 4bj-J-equivalent split-policy artefact or no-split determination artefact recorded under a sibling gitignored namespace | **NOT yet** (not authorized by Phase 4bj-I) |
| Predeclared diagnostics list (per-horizon distributions; censoring tables; alignment cross-checks; leakage checks; per-segment temporal stability if a segmentation exists) | **NOT yet** |
| Predeclared leakage checks (timestamp alignment; horizon-boundary crossing; cross-segment information flow if applicable) | **NOT yet** |
| Predeclared output paths under a gitignored namespace | **NOT yet** |
| Predeclared stop conditions | **NOT yet** |
| Predeclared statement that outputs are descriptive only, never strategy / signal / ML evidence | **NOT yet** |
| No strategy / signal / ML authorization | **NOT yet — and any such authorization must come from a separate prompt under M0** |

All of these gating items remain **unauthorized** by Phase 4bj-I.

---

## 11. Decision options and recommendation

| Option | Description | Verdict |
| --- | --- | --- |
| A | No split; remain paused | acceptable; maximally conservative |
| B | Single-day descriptive split using `train / validation / test` vocabulary | **NOT RECOMMENDED** — implies generalisation the cell cannot support |
| C | Single-day descriptive split using neutral vocabulary (no ML permission) | acceptable only under a separately authorized Phase 4bj-J-equivalent; not selected as primary |
| D | **Declare single-day cell insufficient for formal train / validation / test; require multi-day expansion before empirical diagnostics** | **PRIMARY RECOMMENDATION** |
| E | Future split artefact implementation phase after policy selection | conditional future option only; NOT authorized |
| F | Label diagnostics / ML / strategy / backtest now | **FORBIDDEN / NOT RECOMMENDED** |

**Selected:** Option D.

**Not selected / not authorized:** Options A (acceptable but does not record the determination), B (vocabulary unsafe), C (acceptable only under a separate future phase), E (future, requires separate authorization), F (forbidden).

---

## 12. Future phase ladder

The safe future sequence, **none of which is authorized by Phase 4bj-I**, is:

| Hypothetical phase id | Type | Scope | Status |
| --- | --- | --- | --- |
| Phase 4bj-J (or equivalent) | docs + local gitignored output | Split Artefact Implementation / Recording **or** No-Split Determination Recording: deterministically records the Phase 4bj-I-recommended policy as a sibling artefact under `data/microstructure/splits/` (or analogue) with paired SHA256 sidecar; preserves the label manifest byte-identically. | **NOT authorized** |
| Phase 4bj-K (or equivalent) | docs-only | Label Diagnostic Study Plan: predeclared diagnostics list; predeclared leakage checks; predeclared outputs; predeclared stop conditions. | **NOT authorized** |
| Phase 4bj-L (or equivalent) | docs + local gitignored output | Label Diagnostic Study Execution: runs only the predeclared diagnostics; outputs descriptive results to a gitignored namespace; does not produce strategy or ML output. | **NOT authorized** |
| Later — ML feasibility memo | docs-only | Whether and under what M0 admissibility a future baseline ML diagnostic could be considered. | **NOT authorized** |
| Later — baseline ML diagnostic | docs + local gitignored output | A predeclared baseline classifier / regressor on the labels (only if multi-day data is acquired separately); produces descriptive evaluation only. | **NOT authorized** |
| Later — failure-interpretation / fallback-selection memo | docs-only | If diagnostics return null / near-null. | **NOT authorized** |
| Later — strategy hypothesis under M0 | docs-only | Only after a positive, M0-admissible, mechanism-grounded hypothesis emerges from upstream evidence. | **NOT authorized** |
| Later — strategy spec | docs-only | Full ex-ante strategy specification, mirroring the Phase 4g / Phase 4p / Phase 4v pattern. | **NOT authorized** |
| Later — backtest plan | docs-only | Methodology memo mirroring Phase 4k / Phase 4q / Phase 4w. | **NOT authorized** |
| Later — backtest execution | docs + code | Standalone research script execution mirroring Phase 4l / Phase 4r / Phase 4x. | **NOT authorized** |
| Paper / shadow / live | many phases | Only much later, under separate authorization. | **NOT authorized** |

Each step is its own phase, each requires its own operator authorization, and each is subject to the Phase 4ak M0 twelve-clause gate plus the Phase 4al refined no-rescue rule.

---

## 13. M0 and no-rescue integration

- **Split policy is upstream of label diagnostics.** Without a recorded split policy (or a recorded no-split determination), no label diagnostic is admissible.
- **Label diagnostics are upstream of ML feasibility.** Without descriptive evidence that the cell is even worth modelling, no ML feasibility memo is admissible.
- **ML diagnostics are upstream of M0 strategy admission.** A baseline classifier's accuracy / AUC / loss number is not a strategy; it is a measurement. Producing such numbers does not by itself satisfy the Phase 4ak twelve-clause M0 admissibility gate.
- **Split policy does not bypass M0.** A within-day segmentation does not become a regime model; segments are not strategy regimes.
- **Labels are not signals.** A label is a forward observation by construction; calling its value at row `t` a "signal" is a category error.
- **Split partitions are not strategy regimes.** Segments are administrative partitions for descriptive evaluation; they are not market regimes for which different rules apply.
- **Retained failed strategy families remain closed.** R2 cost-fragility, F1 catastrophic floor, D1-A mechanism / framework mismatch, V2 design-stage incompatibility, G1 regime-gate sparseness, C1 fires-and-loses anti-validation — all remain terminal for their first specs. No rescue path is implied or authorized by Phase 4bj-I.
- **5m research thread remains operationally closed** per Phase 3t.

---

## 14. Explicit non-authorizations

Phase 4bj-I **does not authorize** any of the following:

- Phase 4bj-J (or any future split-artefact / no-split-determination recording phase);
- Phase 4bj-K / Phase 4bj-L (or any future diagnostic-plan / diagnostic-execution phase);
- any Phase 5, Phase 4 canonical, or any other successor phase;
- chronological split artefact creation;
- no-split determination artefact creation;
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
- additional aggTrades acquisition;
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
- mutating `chronological_split_policy` on the original label manifest;
- revising any retained verdict;
- loosening any project lock;
- amending M0 governance.

---

## 15. Retained verdict ledger

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

## 16. Preserved locks

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

## 17. Current-project-state update

`docs/00-meta/current-project-state.md` is updated narrowly to record Phase 4bj-I:

- A new Phase 4bj-I narrative paragraph is added above the existing Phase 4bj-H paragraph.
- The "Current phase:" block is replaced with a Phase 4bj-I block whose content mirrors this memo's headline guarantees:
  - Phase 4bj-I is docs-only;
  - it authorizes no split artefact;
  - it authorizes no empirical label evaluation;
  - it authorizes no new data acquisition;
  - it authorizes no ML / strategy / backtest / acquisition / paper-shadow / live / exchange-write;
  - recommended state remains paused unless the operator separately authorizes a future split-artefact implementation / no-split determination recording phase.
- The prior Phase 4bj-H "Current phase:" block is preserved as historical context under a section heading consistent with prior phases.

No other tracked file in `docs/00-meta/current-project-state.md` is reorganised or rewritten. The retained verdict ledger, project locks, and prior narrative paragraphs are unchanged.

---

## 18. Validation

This phase is docs-only. Validation gates applied:

- `git diff --check` — clean.
- `git status` — clean except always-untracked `.claude/scheduled_tasks.lock` + gitignored `data/research/`.
- `ruff` / `mypy` / `pytest` — **not rerun**. Phase 4bj-I modifies no source code, no tests, no scripts, no `pyproject.toml`, no `README.md`, and no `.gitignore`. The latest authoritative whole-repo validation remains the Phase 4bb-F-implementation merge: `ruff check .` PASS, `mypy strict 120 source files` PASS, `pytest tests/research/microstructure/` 915 passed + 1 pre-existing labelled skip, whole-repo pytest 1698 passed + 1 skipped + 2 pre-existing simulation `KeyError: 'trade_count'` failures (unchanged from prior phases; not introduced by this phase).

---

## Final note

Phase 4bj-I is **branch-complete only** after this work. Per the Phase 4bk-A workflow standard, Phase 4bj-I is **NOT project-complete** until a separately authorized merge phase records its merge-closeout on `main`. No merge is performed by this phase. No successor is authorized.

The recommended state is **remain paused** unless and until the operator separately authorizes a future Phase 4bj-J-equivalent split-artefact implementation / no-split determination recording phase.
