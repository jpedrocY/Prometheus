# Phase 4bn-AE — Closeout

## 1. Phase identity

- **Phase:** 4bn-AE — ML Baseline Pre-Registration + Contract Amendment Memo.
- **Phase type:** docs-only / ML baseline pre-registration / contract amendment /
  evaluation design / dependence policy / success-kill criteria / no-data-read
  memo.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it amends the recorded
  Phase 4bn-AC contract before implementation; an incomplete or post-hoc
  evaluation contract could weaken later leakage/interpretation controls).
- **Status:** **branch-complete only.** Not merged into `main`; not
  project-complete. Per the workflow standard, project completion requires a
  separately authorized merge phase and merge-closeout.

---

## 2. SHAs

- **Branch:** `phase-4bn-ae/ml-baseline-preregistration-contract-amendment`.
- **Base `main` SHA:** `925592961c824cd28c1115710f674b0debef753d`
  (`docs(phase-4bn-ad): finalize merge closeout shas`).
- **Commit SHA:** recorded in the final operator report and `git log` after the
  single `docs(phase-4bn-ae): preregister ml baseline evaluation` commit.
- Pre-branch sync verified: `HEAD == main == origin/main == 92559296…`.

---

## 3. Files created

- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (31 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_closeout.md`
  (this file).

## 4. Files modified

- `docs/00-meta/current-project-state.md` — additive only: one new Phase 4bn-AE
  paragraph after the Phase 4bn-AD paragraph, and one new `Current phase:` block
  ahead of the Phase 4bn-AD block. No prior content altered or deleted.

**No** source / test / script / config / `.gitignore` / `pyproject.toml` /
`README.md` / MCP file / manifest / sidecar / gate report / successor-state /
split file / research matrix / ML config / data file was created or modified. No
`data/microstructure/` or `data/research/` file was created, modified, or read.

---

## 5. Validation commands run

- `git status --short` → only the three tracked Phase 4bn-AE docs files plus the
  expected untracked `.claude/scheduled_tasks.lock`.
- `git diff --check` → clean (no whitespace / conflict markers).
- `git diff` over the three named docs → only the intended additive changes.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- No repo-standard markdown lint tooling exists, so none was run. ruff / mypy /
  pytest omitted: Phase 4bn-AE is docs-only with no code surface.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read or created.

---

## 6. Pre-registration verdict

**Recorded.** The ML-baseline evaluation / interpretation / decision layer is
pre-registered before any pre-v002 result exists.

## 7. Contract-amendment verdict

**Amended.** The Phase 4bn-AC contract
(`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`) is carried forward
verbatim as the source contract and extended by amendment 001 (the §8–§20
evaluation / dependence / success-kill / cost-realism / strategy-boundary /
skeleton-obligation layer). No source-contract field was changed; the amendment
is additive.

## 8. Target interpretation amendment

`forward_direction_15s` retained as the first-baseline target, **reframed
explicitly as a non-economic information / pipeline diagnostic**: not a strategy
label, not a PnL label; may contain last-trade-to-last-trade / bid-ask-bounce
artifacts (aggTrades-only, no mid-price); strict-sign / no-deadband retained as
anti-tuning discipline but acknowledged noise-dominated. Any economically
anchored / deadband / mid-price / triple-barrier / longer-horizon label requires
a separate future contract revision and likely new data or labels.

## 9. Overlapping-label dependence policy

**Option 1 selected:** row-level metrics descriptive-only; decision evidence is
the UTC date / month block; continue/kill requires cross-block agreement; no
per-row significance / p-value / confidence-interval language until a future
phase defines a block bootstrap / date-level jackknife. Fixed decimation/stride
(Option 2) **reserved, not adopted** (would require a pre-registered, justified
constant from committed evidence, e.g. from the Phase 4bn-AH descriptive
diagnostics).

## 10. Date/month-block reporting policy

Every metric emitted at aggregate / per-UTC-month / per-UTC-date granularity
within each split; row and date counts before/after filtering; date inventory per
split; no single aggregate metric governs a decision; effective-sample caveat
adjacent to every aggregate metric. Recorded limitation: validation and holdout
both fall in the Oct–Nov 2024 regime, so decision-window monthly slicing is
regime-narrow; descriptive train-split monthly metrics (Mar–Sep 2024) are also
required as regime-stability context (train is not a generalization test).

## 11. Metric registry

Mandatory: majority-class accuracy / balanced-accuracy / macro-F1 floors;
persistence baseline; accuracy; balanced accuracy; macro-F1; per-class P/R/F1;
confusion matrix; predicted-class distribution; zero-class prevalence and
predicted-zero rate; log loss; Brier; calibration/reliability table;
high-confidence-tail size and accuracy; train−validation and
validation−holdout deltas; filtered row/date counts by split and month;
dropped-row counts by split and reason. No cherry-picking; floors reported beside
model metrics.

## 12. Calibration / confidence-tail policy

Carries the v002 finding (high-confidence tail no better than majority floor).
Mandatory: confidence bins, empirical accuracy per bin, reliability curve per
split/month, high-confidence-tail (≥0.8) size and accuracy, beats-majority
boolean per bin, and a usable / ranking-only / unusable verdict. Pre-registered
rule: if the ≥0.8 tail does not beat the majority floor, probabilities are
declared unusable for confidence-gated interpretation and "trade only when
confident" is pre-emptively rejected.

## 13. Cost-realism descriptive policy

Descriptive only; authorizes no trading rule / label / PnL / backtest. Mandatory:
`forward_log_return_15s` distribution by split/month; share of rows with
`|forward_log_return_15s| > 16 bps` (round-trip lock); optional share > 8 bps.
Pre-registered interpretation: a very small >16 bps share means 15s is almost
never economically relevant, confining the baseline's value to the
information-diagnostic claims.

## 14. Success / continue / kill criteria

Pre-registered on the pre-v002 validation split, corroborated by holdout and
block agreement. **Kill/close** if any: fails to beat both majority and
persistence floors by +2.0 pp accuracy; fails +1.0 pp balanced accuracy and
+0.03 macro-F1 together; improvement concentrated in a single month / minority of
blocks; holdout reverses the uplift sign; calibration unusable AND classification
lift also fails; cost stats show near-zero economic relevance AND diagnostic lift
also fails. **Continue to exactly one bounded follow-up** only if all: +2.0 pp
accuracy over both floors AND +0.03 macro-F1; holdout no sign reversal;
improvement in a majority of validation date-blocks AND months; calibration at
least directionally usable/fixable; cost stats acknowledged (not tradable, but
diagnostic). Thresholds may not be relaxed post-result.

## 15. Ambiguous-result handling

`INVESTIGATE_AMBIGUOUS` (authorizes only one further docs-only decision memo) if:
aggregate clears margins but block evidence mixed; validation improves but holdout
does not (without full reversal); classification improves but calibration fails;
or information suggested but not clean enough to continue. Default on ambiguity:
remain paused; no silent promotion to continue.

## 16. Arc-budget posture

Finite: Phase 4bn-AF (code-only skeleton, no data) → 4bn-AG (data-reading builder
authorization + single run) → 4bn-AH (descriptive dataset diagnostics, no models)
→ 4bn-AI (fixed baseline run + verdict) → 4bn-AJ (arc-decision: close or one
bounded follow-up). Stopping rule: after 4bn-AJ, close or authorize exactly one
bounded follow-up; no open-ended memo sequence. Letters indicative; each phase
separately authorized; posture is not an authorization. (Naming note: the
skeleton is now Phase 4bn-AF because 4bn-AE consumed the slot the 4bn-AD memo
tentatively reserved.)

## 17. Strategy / PnL hard boundary

No baseline result, however strong, authorizes strategy / signals / threshold
trading / backtest / PnL / position sizing / execution / live-readiness /
paper-shadow / exchange-write. Any such path requires a separate future M0-style
memo clearing cost realism (M0.5, never deferred), execution feasibility,
slippage/spread, label economic relevance, strategy admissibility vs retained
rejections + the M0 §7.D microstructure `NOT_RECOMMENDED_NOW` posture, and the
no-rescue constraints.

## 18. Skeleton amendment obligations

A future skeleton (Phase 4bn-AF) must encode/reserve inert interfaces for: metric
registry; date/month-block reporting schema; dependence-caveat fields (incl. an
unset decimation-stride field defaulting to "none"); frozen success/kill/investigate
bucket constants; calibration output schema; descriptive cost fields;
non-authorization flags; a no-strategy-boundary constant; proof fields for
row/date/month counts; and the Phase 4bn-AD no-data-I/O + fail-closed controls.
Synthetic fixtures only; reads no data.

## 19. Remaining blockers

- **Before code-only skeleton:** this amendment (done) + separate skeleton
  authorization. Not blocked by admissibility flags (reads no data).
- **Before data reads:** code-level builder bound to gates/manifests/hashes +
  split artefact; leakage proof + budget preflight in the builder; separate
  data-read authorization (`source_admissible_for_data_read = false`).
- **Before real dataset builder:** contract + amendment; readiness decision
  (done); passing code-only skeleton encoding this amendment; leakage proof +
  budget preflight in the builder; separate builder authorization
  (`source_admissible_for_dataset_builder = false`).
- **Before ML training:** all data-read + builder blockers; target/horizon/filtering
  locked (done) + evaluation layer pre-registered (done); committed end-to-end
  pre-v002 trainer (does not exist); separate ML authorization
  (`ml_authorized = false`).

## 20. Selected next recommendation

A code-only ML dataset builder skeleton (Phase 4bn-AF) encoding the amended
contract, subject to separate operator authorization. A current-state
consolidation memo is separately recommended as a near-term parallel docs-only
option (not a blocker).

---

## 21. Result / decision

- **Result state:**
  `ML_BASELINE_PREREGISTRATION_RECORDED__CONTRACT_AMENDED__SKELETON_NEXT__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

---

## 22. Boundary confirmations

- No local data read; no local data created.
- No code, tests, scripts, or data files added; no existing source / test /
  script / config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, or successor-state artefact created or mutated.
- No file under `data/microstructure/` or `data/research/` read or inspected
  (raw zip / normalized / feature / label Parquet / manifest / gate report /
  sidecar / v002-terminal / sealed-test).
- No v002 terminal window read; no sealed test touched (`test_rows_loaded = 0`).
- No ML trained / scored / predicted; no diagnostics; no strategy / signals /
  PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight; no layer
  re-run.
- No storage migration; no database; no Parquet compaction; no v003.
- No `research_eligible` flip; no `eligibility_gate_status` /
  `chronological_split_policy` / `diagnostics_authorized` / `ml_authorized`
  transition.
- No `data/microstructure` or `data/research` artefact staged or committed; the
  future output namespace
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was not
  created.
- `.claude/scheduled_tasks.lock` remains untracked and uncommitted.
- No credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread
  / V2 / G1 / C1) and every project lock preserved verbatim; no lock loosened; no
  M0 amendment; no successor authorized.

---

## 23. Recommended state

**Remain paused.** No next phase authorized. A code-only skeleton (Phase 4bn-AF)
is recommended but requires separate operator authorization; a current-state
consolidation memo is a recommended near-term parallel docs-only option.

---

## 24. Successor authorization

**None.** No successor is authorized by this branch. Phase 4bn-AE is
branch-complete only; project completion requires a separately authorized merge
phase and merge-closeout on `main`.
