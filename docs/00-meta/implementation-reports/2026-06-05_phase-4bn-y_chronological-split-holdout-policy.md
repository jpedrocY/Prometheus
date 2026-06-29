# Phase 4bn-Y — Chronological Split / Holdout Policy Memo

## 1. Purpose

This memo records the chronological train / validation / internal-holdout policy
that should govern the **first future ML-baseline path** over the newly-produced,
locally-gated **pre-v002 BTCUSDT aggTrades label segment**
(2024-03-01 .. 2024-11-30 inclusive UTC; 275 dates; 400,001,695 rows), after the
local raw → normalized → feature → label → label-layer-gate sequence
(Phases 4bn-O / 4bn-P / 4bn-S / 4bn-T / 4bn-V / 4bn-W / 4bn-X) has succeeded.

It is a **docs-only** policy memo. It settles the split boundaries, the
purge / embargo rule, sealed-test protection, the v002-terminal handling rule,
the published-v002 label handling rule, censored / invalid-label handling, the
full-envelope reference posture, and the prerequisites that must be satisfied
before any ML-baseline readiness or ML training may be authorized.

It produces **no split file, no research matrix, no manifest, no gate report,
no sidecar, no code, no test, no data**. It reads **no local Parquet, no local
manifest or gate report under `data/`, no v002 terminal window, and no
sealed-test file**. It flips no eligibility, transitions no gate status, sets no
`chronological_split_policy` manifest field, and authorizes no successor.

The memo deliberately defers operationalisation: it states **what** the split
policy is and **why**, so that a later, separately authorized ML-baseline
readiness memo (and only then a code-level pre-v002 split-policy artefact with
offline tests) can implement it without re-deriving the boundary contract.

---

## 2. Authority and repository state

**Active local repo path:** `D:\Prometheus`. **Active Claude Code lightweight
workspace:** `D:\ClaudeRuns\prometheus-light`.

**GitHub remote:** `origin → https://github.com/jpedrocY/Prometheus.git`
(verified intact).

**Branch:** `phase-4bn-y/chronological-split-holdout-policy-memo`.

**Base `main` SHA:** `5d69e679b00783c1a2b37e4d6a80c64c2dd3782a`
(`docs(phase-4bn-x): finalize merge closeout shas`). Pre-branch
`HEAD == main == origin/main == 5d69e679…` verified in sync. Predecessor chain
confirmed present on `main`: Phase 4bn-X SHA-finalization `5d69e67`,
merge-closeout `af6387d`, merge `daee3df`, branch `d272dcd`; Phase 4bn-W
finalization `5bcae53` present as predecessor.

**Tier:** **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3. This docs-only phase
defines an admissibility boundary (the chronological split / holdout contract
that any future ML-baseline work must obey); its error could silently corrupt
downstream scientific meaning, so it is treated as Tier 1.

**Working tree:** only the three tracked Phase 4bn-Y docs files are added; the
sole untracked transient is `.claude/scheduled_tasks.lock`. `data/microstructure/`
(`.gitignore:85`) and `data/research/` (`.gitignore:88`) remain gitignored and
uncommitted. Local Phase 4bn-O/4bn-P/4bn-S/4bn-T/4bn-W/4bn-X artefacts under
`data/microstructure/` remain uncommitted and unread by this phase.

**Phase 4bn-Y is branch-complete only by this work; not merged into main; not
project-complete.** Per the workflow standard it becomes project-complete only
when a separately authorized merge phase records its merge-closeout on `main`.

---

## 3. Phase type and strict scope

**Phase type:** docs-only split-policy / holdout-boundary /
ML-admissibility-precondition / leakage-control memo.

**In scope (this phase):** write the split / holdout policy memo, the closeout,
and a narrow additive `current-project-state.md` paragraph + `Current phase:`
block; read committed docs and committed source/tests read-only for policy
grounding.

**Out of scope / explicitly forbidden (this phase):** create a split file;
create a research matrix; create any `data/research` or `data/microstructure`
output; mutate any manifest; set `chronological_split_policy` in any manifest;
flip `research_eligible`; transition `eligibility_gate_status`; read label /
feature / normalized Parquet; read raw zip; read v002 terminal windows; read
sealed-test files; read any local manifest or gate report under
`data/microstructure/`; run ML, diagnostics, strategy, signals, PnL, backtests,
acquisition, or endpoint calls; create a database; compact Parquet; create v003;
add code / tests / scripts; authorize any successor.

---

## 4. Evidence base and input boundary

This memo is derived **only** from:

- committed process standards: `merge-closeout-standard.md`,
  `phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
  `phase-prompt-template.md`, `operator-report-standard.md`;
- committed implementation reports for Phases 4bn-O … 4bn-X (and 4bn-L);
- committed data specs: `docs/04-data/data-requirements.md`,
  `historical-data-spec.md`, `timestamp-policy.md`, `dataset-versioning.md`,
  `docs/08-architecture/database-design.md`;
- committed source read-only for policy grounding, in particular
  `src/prometheus/research/microstructure/diagnostics_split_policy_v002.py`
  (the **already-recorded** v002 split policy), `labels_schema_v002.py`,
  `labels_compute_v002.py`, `labels_validation.py`,
  `ml_baseline_dataset_v002.py`, `ml_baseline_splits.py`,
  `ml_baseline_train.py`, and their tests.

**No local Parquet, manifest, gate report, sidecar, v002 terminal window, or
sealed-test file was read.** All quantitative evidence below is carried forward
verbatim from the committed predecessor reports and from the committed source
constants; none of it was recomputed from local data in this phase.

`README` was treated as potentially stale and was **not** used as a
current-state authority.

---

## 5. Phase 4bn-X label-layer gate carried forward

Phase 4bn-X executed a bounded read-only label-layer eligibility gate over the
Phase 4bn-W pre-v002 label segment and **PASSED 40/40** with result state
`LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`:

- gate report SHA256
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`;
  sidecar SHA256
  `68dd5b5709bb523003ed183ac776e95ad1c82a40deb65e3cda51b2e10e51997c`;
- all 275 label Parquets + 275 sidecars validated; all 400,001,695 label rows
  scanned (no sampling);
- **no v002 terminal read; no sealed-test read; no label artefact mutation; no
  eligibility transition**;
- posture preserved: `research_eligible=false`, `eligibility_gate_status=pending`,
  `no_successor_authorization=true`; Phase 4aw `flip_research_eligible(...)`
  always-raises invariant never invoked.

The pre-v002 segment is therefore **locally produced and locally gated, but not
admitted**: it remains non-eligible and pending. This memo does not change that
posture; it defines the split contract that a *future* admissible path would use.

---

## 6. Available gated pre-v002 envelope

Carried forward from Phases 4bn-O / 4bn-S / 4bn-W / 4bn-X (data family
`microstructure_labels_aggtrades_v001 @ v002`, **pre-v002 backward segment**):

- **Data family / symbol scope:** BTCUSDT / Binance USDⓈ-M futures / aggTrades.
- **Available local gated pre-v002 span:** 2024-03-01 .. 2024-11-30 inclusive
  UTC; **275 contiguous UTC dates**; 400,001,695 rows.
- Normalized layer: 275 Parquet; manifest SHA256 `0e96ae37…d9fa`;
  normalized-layer gate PASS 25/25 (`3452fd9d…f134`).
- Feature layer: 275 Parquet; manifest SHA256 `4881eb87…9b52`;
  `feature_config_hash 0726b41d…114c`; feature-layer gate PASS 27/27
  (`db731d1b…6a08`).
- Label layer: 275 Parquet + 275 sidecars; manifest SHA256 `69746c88…b161`;
  manifest sidecar `636a4c1a…8239`; `label_config_hash b3bd5d2b…8970`;
  `envelope_terminal_unix_ms 1733011199331` (`envelope_terminal_utc_date
  2024-11-30`); horizons 1s/5s/15s/60s; censored counts 1s=3, 5s=20, 15s=42,
  60s=216; invalid-price rows 0.
- Eligibility: `research_eligible=false`; `eligibility_gate_status=pending`.

This 275-date span is the **only** data this memo treats as candidate
train/validation/internal-holdout material for the first ML-baseline path.

---

## 7. Published v002 terminal and sealed-test boundary

The published terminal family and its sealed test are governed by an
**already-recorded** chronological split policy that this memo must preserve and
must not contradict or mutate:
`diagnostics_split_policy_v002.py` →
`SPLIT_POLICY_NAME = "CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO"`
(Phase 4bm-U recorded; Phase 4bm-W helpers):

- v002 envelope: 2024-12-01 .. 2025-02-28 inclusive UTC; 90 dates;
  155,153,449 rows.
- Train 2024-12-01 .. 2025-01-14 (45 dates); Validation 2025-01-15 ..
  2025-02-13 (30 dates); **Test / final holdout 2025-02-14 .. 2025-02-28
  (15 dates)**.
- Assignment by `source_transact_time_ms` UTC date.
- Boundaries `T_TV = 1736899200000` (2025-01-15T00:00:00Z) and
  `T_VT = 1739491200000` (2025-02-14T00:00:00Z).
- **60-second boundary embargo**, earlier-split exclusion only
  (`MIN_BOUNDARY_EMBARGO_SECONDS = 60`); rows never reassigned forward.
- No random / shuffled / k-fold-over-time / bootstrap / post-hoc resampling.
- Test is **single-use**; seven prohibited uses recorded:
  `feature_selection`, `model_selection`, `hyperparameter_selection`,
  `threshold_tuning`, `strategy_design`, `diagnostic_iteration`,
  `eligibility_rescue`.

**Sealed-test span (locked, untouched):** 2025-02-14 .. 2025-02-28;
`test_rows_loaded = 0`. The v002 terminal window
(2024-12-01 .. 2025-02-28, all of raw / normalized / feature / label) was **not
read** by Phases 4bn-O … 4bn-X and is **not read** here; it is carried forward
**by reference only**.

---

## 8. Leakage risks being controlled

The forward-looking labels look ahead up to **60 seconds** (1s/5s/15s/60s →
1000/5000/15000/60000 ms). The risks this policy must neutralise:

1. **Forward-horizon boundary crossing.** A row near the end of an earlier split
   whose target timestamp `T + H_ms` falls into a later split would let a
   later-split observation leak into the earlier split. Controlled by the
   embargo (§12).
2. **Random / shuffled splitting.** Any random, shuffled, k-fold-over-time, or
   bootstrap row-level split would mix future and past rows. Forbidden
   (chronological-only; §18).
3. **Future-feature / look-past leakage.** Features must be causal-only
   (`LEAKAGE_POLICY_V002 = "causal_only_no_future_lookahead"`); labels must not
   look past their target nor past the envelope terminal. Preserved (§18).
4. **Sealed-test contamination.** Any read of the v002 sealed test for fitting,
   selection, tuning, or design would burn the final holdout. Forbidden (§15).
5. **v002-terminal contamination.** Pulling any 2024-12-01+ v002-terminal row
   into a pre-v002 train/validation/holdout stream before a later authorized
   full-envelope path would leak across the segment boundary. Forbidden (§14,
   §16).
6. **Censored / invalid-label silent imputation.** Filling null censored labels
   or imputing invalid-price rows would fabricate targets. Forbidden (§13).
7. **Multiple-testing / holdout reuse.** Repeated tuning against validation or
   the internal holdout inflates apparent performance. Controlled (§19).

---

## 9. Candidate split policies considered

- **A — Conservative pre-v002-only split with internal dry-run holdout.**
  Train 2024-03-01 .. 2024-09-30; embargo date 2024-10-01; Validation
  2024-10-02 .. 2024-11-15; embargo date 2024-11-16; internal holdout / dry-run
  (not sealed test) 2024-11-17 .. 2024-11-30. v002 terminal by reference only;
  sealed test untouched.
- **B — Pre-v002 train/validation only, no internal test.** Train
  2024-03-01 .. 2024-09-30; embargo 2024-10-01; Validation 2024-10-02 ..
  2024-11-30. v002 terminal / sealed test unavailable.
- **C — Full-envelope staged policy.** Pre-v002 train/validation; v002-terminal
  non-sealed dates 2024-12-01 .. 2025-02-13 reserved for later out-of-time
  validation; sealed test 2025-02-14 .. 2025-02-28 locked. **Rejected for now:**
  C requires reading / admitting the v002 terminal window, which this phase must
  not do, and which the pre-v002 segment’s non-eligible / pending posture does
  not yet license.
- **D — Other.** No committed repository evidence supports a different policy.

**Decisive arithmetic for A.** Candidate A partitions the 275 gated pre-v002
dates **exactly**: 214 (train, Mar 1 – Sep 30) + 1 (embargo, Oct 1) + 45
(validation, Oct 2 – Nov 15) + 1 (embargo, Nov 16) + 14 (internal holdout,
Nov 17 – Nov 30) = **275**. No date is unused and none is double-counted.

**Design consistency for A.** A mirrors the locked v002 policy’s principles
(chronological-only; assignment by `source_transact_time_ms` UTC date;
earlier-split embargo; single-use holdout; no shuffle / random / bootstrap),
extended to the pre-v002 segment, and is **strictly more conservative** at the
boundaries (full-date embargo ≫ 60 s). It requires **no** v002-terminal or
sealed-test read.

---

## 10. Selected chronological split policy

**Selected: Candidate A — conservative pre-v002-only chronological split with an
internal dry-run holdout.** Working name (for a future code-level artefact, not
created here):
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`.

Binding rules:

- **Scope:** only the 275 gated pre-v002 dates (2024-03-01 .. 2024-11-30). The
  v002 terminal (2024-12-01 .. 2025-02-28) and the sealed test
  (2025-02-14 .. 2025-02-28) are **out of scope** and remain by reference only.
- **Assignment clock:** rows assigned by `source_transact_time_ms` UTC date
  (identical rule to the locked v002 policy).
- **Ordering:** chronological-only. No random / shuffled / k-fold-over-time /
  bootstrap / post-hoc temporal resampling, ever.
- **Embargo:** full-UTC-date embargo at each internal boundary (§12), which
  strictly dominates and satisfies the locked **≥60 s** row-level floor.
- **Internal holdout is not the sealed test:** the 2024-11-17 .. 2024-11-30
  window is an internal dry-run only and **cannot** be used for final claims,
  strategy claims, production claims, or eligibility rescue. The project’s
  single-use final sealed test remains the v002 TEST split
  2025-02-14 .. 2025-02-28, which stays unread.
- **Non-mutating:** this is a recorded *policy*; it sets no manifest field,
  creates no artefact, and does not admit the segment.

---

## 11. Train / validation / internal holdout ranges

| Split | UTC date range (inclusive) | Dates | Role |
|---|---|---|---|
| **Train** | 2024-03-01 .. 2024-09-30 | 214 | Model fitting + train-only transform fitting |
| Embargo | 2024-10-01 | 1 | Dropped (boundary purge) |
| **Validation** | 2024-10-02 .. 2024-11-15 | 45 | Model selection / hyperparameter / threshold tuning |
| Embargo | 2024-11-16 | 1 | Dropped (boundary purge) |
| **Internal holdout (dry-run)** | 2024-11-17 .. 2024-11-30 | 14 | One-time dry-run evaluation only; **not** the sealed test |
| **Total** | 2024-03-01 .. 2024-11-30 | **275** | = full gated pre-v002 segment |

- **Training allowed rows:** only rows whose `source_transact_time_ms` UTC date
  ∈ Train dates, after applying the embargo exclusion.
- **Validation allowed rows:** only rows whose UTC date ∈ Validation dates,
  after applying the embargo exclusion.
- **Internal-holdout allowed rows:** only rows whose UTC date ∈ holdout dates
  (single-use dry-run only).
- **Disallowed rows:** all v002-terminal rows (2024-12-01+) and all sealed-test
  rows, unless a future phase separately authorizes them.

Boundary timestamps (carried forward for a future code-level artefact; **not**
emitted here): `T_TV(pre-v002) = 2024-10-02T00:00:00Z`;
`T_VH(pre-v002) = 2024-11-17T00:00:00Z`. The embargo dates 2024-10-01 and
2024-11-16 sit immediately before each boundary and are dropped in full.

---

## 12. Purge / embargo policy

**Why required.** Labels look forward up to 60 s. A row at time `T` in an
earlier split whose target `T + H_ms` crosses into the next split would leak
later-split information backward. The maximum horizon (60 s) sets the minimum
purge width.

**Selected embargo:**

- **Primary operational rule — 1 full UTC date (date-level purge).** Drop the
  entire boundary date from *both* adjacent splits: 2024-10-01 between
  train/validation, and 2024-11-16 between validation/internal-holdout. This is
  trivially enforceable with the segment’s daily Parquet partitioning.
- **Formal floor — ≥ 60 s row-level embargo (earlier-split exclusion).** The
  1-day purge is **explicitly more conservative than** the 60-second label
  horizon (86,400 s ≫ 60 s) and **subsumes** the locked v002 floor
  `MIN_BOUNDARY_EMBARGO_SECONDS = 60`. Future tooling that ever operates below
  day granularity must still enforce the row-level ≥ 60 s earlier-split embargo
  (`exclude_from_earlier_split`; rows never reassigned forward), so the
  invariant holds even if the date-level purge is relaxed.

**Enforcement units:** date-level for the recommended operational split, with
the row-level 60 s rule retained as the binding minimum. Embargo applies to the
**earlier** split at each boundary only; the internal holdout, being the latest
pre-v002 split, never embargoes itself (mirroring the v002 policy’s `test →
None` rule).

This choice is consistent with — and strictly stronger than — the recorded v002
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` boundary embargo.

---

## 13. Censored-label and invalid-label handling policy

**Censored labels.** In the pre-v002 segment, per-horizon
`horizon_censored_flag_H = true` when the target timestamp crosses
`envelope_terminal_unix_ms = 1733011199331` (2024-11-30); recorded censored
counts are 1s=3, 5s=20, 15s=42, 60s=216, all concentrated at the segment tail —
i.e. inside the internal-holdout window (2024-11-17 .. 2024-11-30). Policy:

- **Do not silently impute** censored labels. Never zero-pad, forward-fill, or
  fabricate a target where `forward_log_return_H` / `forward_direction_H` is
  null.
- Rows may be **retained** with horizon-specific labels null; a per-task ML
  dataset must **drop, per horizon, the rows whose label for that horizon is
  null** (consistent with the existing v002 supervised mask, which includes a
  row iff not-censored ∧ not-embargoed ∧ direction-non-null ∧ return-non-null).
- The **exact per-task filtering must be defined by the future ML-baseline
  readiness memo**, not by this split memo. This memo forbids only silent
  imputation; it does not pre-commit the per-horizon task design.

**Invalid-price labels.** The current pre-v002 label segment has **0**
`label_invalid_price_flag = true` rows. Future policy must nonetheless
**explicitly reject / filter** any `label_invalid_price_flag = true` row from
train / validation / holdout and **never impute** an invalid-price label. The
`label_any_censored_flag` OR-invariant and the
`forward_direction ∈ {-1, 0, 1}` (null iff return null) semantics are preserved.

---

## 14. v002 terminal handling policy

- The v002 terminal window (2024-12-01 .. 2025-02-28; raw / normalized /
  feature / label) is **by reference only** and **unread** in this arc.
- It remains governed by the recorded
  `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy; this memo neither
  mutates nor contradicts it.
- The v002 terminal is **inadmissible** to the first ML-baseline path. It may be
  admitted only by a **later, separately authorized** full-envelope reference /
  assembly phase (and, where it touches the non-sealed 2024-12-01 .. 2025-02-13
  window, a holdout-boundary memo), neither of which is authorized here.
- The published `__v002` label / feature / normalized manifests and directories
  remain **byte-for-byte immutable**; nothing here reads or alters them.

---

## 15. Sealed-test handling policy

- The sealed test **2025-02-14 .. 2025-02-28** remains **fully sealed**:
  `test_rows_loaded = 0`; untouched; unread.
- It is **excluded** from all training, validation, model selection,
  hyperparameter / threshold tuning, feature selection, strategy design,
  diagnostic iteration, and eligibility rescue — the seven prohibited uses
  recorded in the v002 policy.
- It may be used **only** by a future, explicitly authorized sealed-test
  protocol under locked rules, as a **single-use final** evaluation. Until then
  it is unavailable for any purpose.
- The pre-v002 **internal holdout (2024-11-17 .. 2024-11-30) is not a substitute
  for the sealed test** and may not be used for final / strategy / production
  claims.

---

## 16. Full-envelope reference policy

- The full intended label envelope is **2024-03-01 .. 2025-02-28**, currently
  represented **by reference**: the gated pre-v002 segment
  (2024-03-01 .. 2024-11-30) plus the published v002 label reference
  (2024-12-01 .. 2025-02-28).
- **No full-envelope assembly manifest is created by this arc**, and none is
  created here. (If the repository already contains one from prior work, it is
  left untouched.)
- A full-envelope reference / assembly artefact is **NOT a prerequisite** for
  the selected conservative pre-v002-only path (Candidate A), because that path
  uses only the already-gated pre-v002 dates.
- A full-envelope reference / assembly artefact **IS required** before any
  future ML path that combines pre-v002 and v002 data (or that uses any
  v002-terminal row), to reconcile the two manifests, lineages, and envelope
  terminals under a single admissibility contract. That artefact is **deferred
  and unauthorized** here.

---

## 17. Future ML-baseline readiness prerequisites

Before any ML-baseline readiness work, and well before any training, all of the
following must hold (each requires separate operator authorization):

1. **An ML-baseline readiness memo (docs-only)** that, on top of this split
   policy, settles per-task dataset construction: which horizons, which feature
   columns (the frozen v002 computed-feature matrix vs. a pre-v002 analogue),
   per-horizon censored-row filtering, invalid-row rejection, label/target
   definitions, and train-only transform fitting.
2. **A code-level pre-v002 split-policy artefact + offline tests** (analogous to
   `diagnostics_split_policy_v002.py`) implementing
   `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`. **Not created
   here.**
3. **Source admissibility resolved.** The pre-v002 segment is currently
   `research_eligible=false` / `eligibility_gate_status=pending`. An ML-baseline
   path requires the segment to be admissible; resolving that is a **separate,
   unauthorized** eligibility action (Phase 4aw `flip_research_eligible(...)`
   always-raises invariant remains in force and is untouched here).
4. **A leakage / split-integrity proof** (§18) demonstrating that no train /
   validation / holdout row’s forward horizon crosses into another split, that
   no shuffle / random split was used, and that no v002-terminal / sealed-test
   row entered any stream.
5. **Budget preflight** within the carried-forward Phase 4bn-L caps (label
   footprint warn 75 / hard 125 GiB; runtime warn 4 h / hard 8 h; temp warn 50 /
   hard 100 GiB; total derived-stack warn 250 / hard 300 GiB; D: ≥ 500 GiB
   before / fail-closed below 350 GiB during).

The existing committed ML-baseline modules (`ml_baseline_design_v002.py`,
`ml_baseline_dataset_v002.py`, `ml_baseline_splits.py`, `ml_baseline_train.py`)
target the **v002 envelope** and do **not** cover the pre-v002 segment; a
pre-v002 baseline is a new, separately authorized path, not a re-run of those.

---

## 18. Future ML dataset construction rules

Any future ML dataset built under this policy must obey:

- **Chronological-only; no shuffle.** No random row-level train/test split; no
  shuffled CV; no k-fold-over-time; no bootstrap. Order by
  `source_transact_time_ms`.
- **Train-only transform fitting.** Any normalisation / standardisation
  statistic is fit on the train stream only and applied to validation / holdout;
  never refit on validation or holdout.
- **Embargo enforcement.** Apply the §12 embargo; prove no earlier-split row’s
  `T + H_ms` crosses the next boundary (date-level purge satisfies this with
  margin; the ≥ 60 s row-level floor is the formal guarantee).
- **No leakage.** No future feature columns
  (`causal_only_no_future_lookahead`); no look-past-target; no
  look-past-envelope-terminal; no v002 / sealed access; no external data; no
  synthetic extrapolation; no fabricated or zero-padded rows.
- **Censored / invalid handling per §13.** Drop per-horizon nulls; reject
  invalid-price rows; never impute.
- **Purged/embargo validation artefact.** The dataset builder must emit a
  check that, for every retained row, the forward horizon stays within the
  row’s own split (no boundary crossing).

---

## 19. Future model-selection and overfitting controls

- **Validation** (2024-10-02 .. 2024-11-15) may be used for model selection,
  hyperparameter selection, and threshold tuning.
- **Internal holdout** (2024-11-17 .. 2024-11-30) may be used for a **one-time
  dry-run** evaluation only — never for repeated tuning, model selection, or
  any final / strategy / production / eligibility claim.
- **Sealed test** (2025-02-14 .. 2025-02-28) may not be touched until a future
  explicit authorization.
- **Multiple-testing log required.** Future ML-baseline work must record the
  model family, hyperparameter trials, feature columns used, labels/horizons
  used, and each validation / holdout touch. No strategy / PnL / signal claim
  may be drawn from validation or the internal holdout alone.
- **No eligibility rescue.** No diagnostic, model, or metric outcome may be used
  to rescue or flip the eligibility of any segment.

---

## 20. Explicit non-authorizations

Phase 4bn-Y did **NOT**, and does **NOT**, authorize: creating a split file;
creating a research matrix; creating any `data/research` or `data/microstructure`
output; mutating any manifest; setting `chronological_split_policy` in any
manifest; flipping `research_eligible`; transitioning `eligibility_gate_status`,
`diagnostics_authorized`, or `ml_authorized`; reading label / feature /
normalized Parquet; reading raw zip; reading the v002 terminal window; reading
the sealed test; reading any local manifest / gate report under
`data/microstructure/`; running ML / diagnostics / strategy / signals / PnL /
backtests; acquisition or endpoint calls; HEAD preflight; storage migration;
database creation; Parquet compaction; v003 creation; adding code / tests /
scripts; or authorizing any successor.

The Phase 4aw `flip_research_eligible(...)` always-raises invariant is preserved
and never invoked. The recorded v002
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy is preserved verbatim
and unmodified.

**Every retained verdict and project lock is preserved verbatim** (H0 / R3 /
R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread / V2 / G1 / C1; §11.6 = 8 bps per
side / round-trip 16 bps; §1.7.3 0.25% / 2× / one-position / mark-price stops;
Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11;
Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 + post-null
cooldown; Phase 4al refined no-rescue + §13 boundary + §14 hierarchy; Phase 4aw
always-raises invariant; Phase 4bb-F canonical path policy; Phase 4bl-F risk
tiers; Phase 4bm-U/4bm-W v002 split policy; Phase 4bn-L budgets; Phase 4bn-N
normalization manifest/versioning; Phase 4bn-R feature manifest/versioning;
Phase 4bn-V label manifest/versioning; Phase 4am .. Phase 4bn-X results — all
preserved verbatim).

---

## 21. Decision

**Result state:** `RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`.

**Decision:**
`RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale: the memo settles a conservative, repository-grounded pre-v002-only
split policy (Candidate A) that requires **no** v002-terminal or sealed-test
read, partitions the 275 gated pre-v002 dates exactly, and is strictly more
conservative than — and fully consistent with — the locked v002 split policy.
Per the phase prompt, that is the preferred condition for recommending a
docs-only ML-baseline readiness memo as the next (separately authorized) step.
No full-envelope reference/assembly is required for this conservative path, and
no v002/sealed scope must be touched to define the split, so neither the
full-envelope-assembly nor the holdout-boundary recommendation is selected.

---

## 22. Recommended state and successor options

**Recommended state: remain paused.** No next phase is authorized from inside
Phase 4bn-Y.

Successor options (each requiring **separate** operator authorization after this
branch is merged):

- request a merge prompt for Phase 4bn-Y;
- authorize a docs-only **ML-baseline readiness memo** (recommended);
- authorize a docs-only **full-envelope reference / assembly memo** (only if a
  future path must combine pre-v002 + v002 data);
- authorize a docs-only **holdout-boundary memo** (only if a future scope must
  touch the v002 terminal or sealed-test dates);
- authorize a **source-policy documentation** memo;
- authorize a **process-doc `D:` path-string update**;
- **reject** further ML-baseline successors and close the ML-baseline arc;
- remain paused.

No ML / diagnostics / strategy / PnL / backtest / storage-migration / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 23. Current-project-state update summary

The narrow, additive `current-project-state.md` change records: a new Phase
4bn-Y paragraph (after the Phase 4bn-X paragraph) and a new `Current phase:`
block (prepended above the Phase 4bn-X block); all prior paragraphs and blocks
preserved verbatim as labelled historical context. The paragraph records the
phase type, branch, base SHA, the selected Candidate A split (train
2024-03-01 .. 2024-09-30 / validation 2024-10-02 .. 2024-11-15 / internal
holdout 2024-11-17 .. 2024-11-30; embargo dates 2024-10-01 and 2024-11-16; 1-day
purge over a ≥ 60 s floor), the v002-terminal / sealed-test by-reference
posture, the result state `RECORD_CHRONOLOGICAL_SPLIT_POLICY__REMAIN_PAUSED`, the
decision
`RECOMMEND_AUTHORIZE_ML_BASELINE_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`,
the full non-authorization list, the preserved verdict/lock ledger, and
**remain paused / no next phase authorized**. No table value, manifest field, or
eligibility flag is mutated.
