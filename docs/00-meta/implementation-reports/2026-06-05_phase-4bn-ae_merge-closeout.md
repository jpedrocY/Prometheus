# Phase 4bn-AE — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-AE — ML Baseline Pre-Registration + Contract Amendment Memo.
- **Phase type:** docs-only / ML baseline pre-registration / contract amendment /
  evaluation design / dependence policy / success-kill criteria / no-data-read
  memo.
- **Action:** merge into `main`.
- **Merge purpose:** bring the branch-complete Phase 4bn-AE work (the
  pre-registration + contract-amendment memo, the closeout, and the narrow
  additive `current-project-state.md` update) onto `main`.
- **Source branch:** `phase-4bn-ae/ml-baseline-preregistration-contract-amendment`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3 (it amends the recorded
  Phase 4bn-AC ML dataset contract before implementation — defining evaluation,
  overlapping-label dependence, success/continue/kill, regime-sliced reporting,
  calibration/cost-realism, economic-interpretation, strategy/PnL boundary, and
  arc-budget rules any later skeleton and builder must obey; an incomplete or
  post-hoc evaluation contract could weaken leakage/interpretation controls or
  license unfalsifiable results, even though the memo performs no data I/O). The
  full 16-section merge-closeout structure is used.

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `925592961c824cd28c1115710f674b0debef753d`
  (`docs(phase-4bn-ad): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `41fb7c1ec39b1ed6e3109b184ac24e6e0982e58e`
  (`docs(phase-4bn-ae): preregister ml baseline evaluation`).
- **Merge commit SHA:** `daae192758a3d7ae6cd6e443895d38a32e55f19b`
  (`docs(phase-4bn-ae): merge ml baseline preregistration`).
- **Merge-closeout commit SHA:** `ee067f161594b8f4d5831e5609416ac9dd890e14`
  (`docs(phase-4bn-ae): add merge closeout`).
- **SHA-finalization commit SHA:** this update
  (`docs(phase-4bn-ae): finalize merge closeout shas`) that fills the exact
  merge-closeout commit SHA above — its exact SHA equals the resulting
  `main` / `origin/main` tip, reproduced in the final operator report and
  `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`9255929`) → `git merge --no-ff
phase-4bn-ae/ml-baseline-preregistration-contract-amendment -m
"docs(phase-4bn-ae): merge ml baseline preregistration"`. Merge made by the `ort`
strategy; no conflicts. No `--no-verify`; no `--no-gpg-sign`; no
`-c commit.gpgsign=false`; no force-push. Pushed to `origin/main` with no force,
no skip-hooks, no skip-signing (push status recorded in the final operator
report).

---

## 4. Files brought forward by the merge

**Docs (3):**

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_ml-baseline-preregistration-contract-amendment.md`
  (31 sections; 1012 insertions).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ae_closeout.md`
  (273 insertions).
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (243 insertions, 0 deletions; new Phase 4bn-AE paragraph after the Phase
  4bn-AD paragraph + new `Current phase:` block ahead of the Phase 4bn-AD block;
  all prior content preserved verbatim).

**Source:** none. **Tests:** none. **Scripts:** none. **Config:** none.

**No** existing source or test was modified; no scripts, config, `.gitignore`,
`pyproject.toml`, README, MCP file, manifest, sidecar, gate report,
successor-state artefact, split file, research matrix, ML config, model output,
prediction output, or data file was added or modified. **No `data/microstructure/`
or `data/research/` file was modified.** No prior governance memo was modified
beyond the narrow additive `current-project-state.md` paragraph.

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  243 +++++
 .../2026-06-05_phase-4bn-ae_closeout.md            |  273 ++++++
 ...-baseline-preregistration-contract-amendment.md | 1012 ++++++++++++++++++++
 3 files changed, 1528 insertions(+)
```

1528 insertions, 0 deletions. The diff matches the expected change set from the
merge prompt exactly (add memo, add closeout, modify `current-project-state.md`).

---

## 6. Result / verdict

**PRE-REGISTRATION RECORDED — CONTRACT AMENDED — MERGE COMPLETE.** Phase 4bn-AE
is a docs-only ML baseline pre-registration / contract amendment / evaluation
design / dependence policy / success-kill criteria / no-data-read memo. It does
**not** replace Phase 4bn-AC; it carries the Phase 4bn-AC contract
(`microstructure_ml_dataset_aggtrades_pre_v002_contract_v001`) forward verbatim
as the source contract and adds **amendment 001** — the pre-registered
evaluation / interpretation / decision layer (evaluation claim scope, target
interpretation, overlapping-label dependence policy, date/month-block + regime
reporting, metric registry, calibration/confidence-tail policy, cost-realism
descriptive policy, success/continue/kill criteria, ambiguous-result handling,
finite arc-budget, strategy/PnL hard boundary, and skeleton amendment
obligations). It created no dataset, no dataset config, no manifest, no gate
report, no sidecar, no split file, no research matrix, no model output, no
prediction output, and no data file; it read no local data; it created no local
data; it added no code, tests, or scripts; it mutated no manifest; it set no
`chronological_split_policy`; it flipped no `research_eligible`; it transitioned
no `eligibility_gate_status`; it invoked no Phase 4aw eligibility function; it
created no future output namespace; it authorized no successor. With this merge,
Phase 4bn-AE is **merge-complete on `main`**.

- **Result state:**
  `ML_BASELINE_PREREGISTRATION_RECORDED__CONTRACT_AMENDED__SKELETON_NEXT__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per the project convention, project completion also requires the SHA-finalization
commit (`docs(phase-4bn-ae): finalize merge closeout shas`) that fills the exact
post-merge SHAs in §2; that commit is recorded below and in the final operator
report.

---

## 7. Local gitignored outputs (if any)

**None.** This phase created no `data/microstructure/` or `data/research/` output
and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed). No
`data/microstructure` or `data/research` artefact was staged or committed. The
future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was **not**
created.

---

## 8. Validation results

- `git diff --check` → clean (no whitespace / conflict markers), pre- and
  post-merge.
- `git diff --name-status main..phase-4bn-ae/ml-baseline-preregistration-contract-amendment`
  (pre-merge) → `M current-project-state.md`, `A …_closeout.md`,
  `A …_ml-baseline-preregistration-contract-amendment.md`.
- `git diff --stat` (merge, `9255929..HEAD`) → 3 files, 1528 insertions, 0
  deletions.
- `git diff --numstat -- docs/00-meta/current-project-state.md` → `243 0`
  (additive only).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` (post-merge) → only `?? .claude/scheduled_tasks.lock`.
- No repo-standard markdown lint tooling exists, so none was run; ruff / mypy /
  pytest omitted because Phase 4bn-AE is docs-only with no code surface.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read or created.
- Git emitted the standard LF→CRLF advisory for the two new files at branch
  commit time (`.gitattributes` / `core.autocrlf`, Windows convention);
  cosmetic; committed blobs are correct.

---

## 9. Upstream immutability evidence (if applicable)

**n/a — phase did not access any local artefact.** Phase 4bn-AE reads and mutates
no manifest, sidecar, gate report, successor-state, or published dataset. The
published `__v002` raw / normalized / feature / label families and the local
gated pre-v002 normalized (4bn-O) / feature (4bn-S) / label (4bn-W) segments and
their gate reports (4bn-P / 4bn-T / 4bn-X) remain byte-for-byte immutable and
unread.

---

## 10. Manifest state preservation (if applicable)

No manifest in scope was created, read, or mutated. Byte-identically before and
after this phase, at every pre-v002 layer (normalized `0e96ae37…`, feature
`4881eb87…`, label `69746c88…`):

- `research_eligible` — **false** (not flipped).
- `eligibility_gate_status` — **pending** (not transitioned).
- `chronological_split_policy` — **not set / not transitioned** in any manifest.
- `diagnostics_authorized` / `ml_authorized` — **false** (not transitioned).
- `no_successor_authorization` — **true** (preserved).
- Governance label state — **unchanged**.

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant preserved (never invoked).

---

## 11. Boundary confirmations

- No local data read; no local data created.
- No code, tests, scripts, or data files added; no existing source / test /
  script / config / `.gitignore` / `pyproject.toml` / README / MCP file modified.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, successor-state artefact, model, score, or prediction created.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar under `data/microstructure/` read or inspected.
- No v002 terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No ML trained; no ML dataset created; no research matrix created; no model
  scored; no prediction generated; no diagnostics run; no strategy / signals /
  PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight; no
  acquisition / raw / normalization / feature / label execution or layer-gate
  re-run.
- No storage migration; no database; no Parquet compaction; no v003.
- No `research_eligible` flipped on any actual manifest; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy` changed.
- No `data/microstructure` or `data/research` artefact staged or committed; the
  future output namespace
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was not
  created.
- `.claude/scheduled_tasks.lock` remains untracked and uncommitted.
- No credential / `.env` / `.mcp.json` / MCP / Graphify used.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- No retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

---

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

---

## 13. Preserved project locks

All preserved verbatim: §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 =
0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13
boundary + §14 hierarchy; Phase 4aw `flip_research_eligible(...)` always-raises
invariant (never invoked); Phase 4bb-F canonical path + sidecar policy;
Phase 4bl-F risk tiers; Phase 4bm-U / 4bm-W v002 split policy; Phase 4bn-J-R1
raw-only cap amendment; Phase 4bn-L derived-stack storage budget; Phase 4bn-N
normalization manifest/versioning; Phase 4bn-R feature manifest/versioning;
Phase 4bn-V label manifest/versioning; Phase 4bn-Y chronological split/holdout
policy; Phase 4bn-Z ML-baseline readiness memo; Phase 4bn-AA pre-v002
split-policy artefact; Phase 4bn-AB source-admissibility posture; Phase 4bn-AC ML
dataset contract; Phase 4bn-AD ML dataset builder readiness verdict. All prior
phase results preserved verbatim.

---

## 14. No-rescue constraints

The Phase 4bn-AE merge does not, and cannot, be construed as authorising:

- a code-only ML dataset builder skeleton (Phase 4bn-AF); a current-state
  consolidation memo; an additional evaluation-design memo; a
  source-admissibility gate artefact; a data-reading ML dataset builder; a
  research matrix;
- ML model training, model selection, scoring, predictions, strategy hypothesis
  generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry / exit
  rules, backtest design, PnL, or diagnostics;
- any actual data read of the pre-v002 normalized / feature / label segments;
- reading the v002 terminal window or touching the sealed test
  (`test_rows_loaded = 0` preserved);
- relaxing any pre-registered success / continue / kill threshold post-result;
- adopting a decimation / stride (reserved-not-adopted), or introducing per-row
  significance / p-value inference, without a separately authorized
  dependence-aware method;
- converting the `forward_direction_15s` diagnostic target into an economic /
  strategy / PnL claim, or authorizing any economically anchored / deadband /
  mid-price / triple-barrier / longer-horizon / volatility-scaled / MFE / MAE /
  R-multiple / PnL label;
- full-envelope assembly or a holdout-boundary memo;
- creating the future output namespace
  `data/research/microstructure/ml_datasets/pre_v002_contract_v001/`;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- mark-price / spot / cross-venue / order-book / bookTicker / additional
  aggTrades acquisition;
- storage migration / database creation / Parquet compaction / v003;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`,
  or `chronological_split_policy` from this memo alone.

---

## 15. Successor authorization

**None.** No successor is authorized by this merge. A **code-only ML dataset
builder skeleton (Phase 4bn-AF)** encoding this amendment is *recommended* as the
next step but requires separate operator authorization. A **current-state
consolidation memo** is *recommended* as a near-term parallel docs-only option
but is not a blocker and is not authorized.

Candidate successors explicitly **NOT** authorized:

- a code-only ML dataset builder skeleton (Phase 4bn-AF; recommended; not
  authorized)
- a current-state consolidation memo (recommended parallel option; not
  authorized)
- an additional evaluation-design memo
- a source-admissibility gate artefact
- a data-reading ML dataset builder
- a research matrix
- a full-envelope reference-assembly memo
- a holdout-boundary memo
- ML implementation / model training / scoring / predictions / diagnostics
- strategy / signals / PnL / backtest implementation
- additional aggTrades / bookTicker / mid-price / 5m / 1m / tick / mark-price /
  order-book acquisition
- Phase 5; Phase 4 canonical
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials

---

## 16. Recommended state

**Remain paused.** No next phase authorized.

**Conditional next, NOT authorized:** a **code-only ML dataset builder skeleton
(Phase 4bn-AF)** encoding the Phase 4bn-AE amendment is the cleanest non-paused
option. It would encode the amended evaluation contract — metric registry,
date/month-block reporting schema, dependence-caveat fields (unset
decimation-stride defaulting to `none`), frozen success/kill/investigate bucket
constants, calibration output schema, descriptive cost fields, non-authorization
flags, a no-strategy-boundary constant, and row/date/month proof fields — plus
the Phase 4bn-AC/AD builder scope, all exercised **against synthetic in-memory
fixtures only**, reading no local data, creating no output directory, writing no
Parquet, mutating no manifest, producing no `data/research` / `data/microstructure`
artefact, and calling no endpoint. A **current-state consolidation memo** is a
recommended parallel docs-only option (the state doc is now large / partially
stale) but is not a blocker. Neither is authorised by this merge.

---

## 17. Phase 4bn-AE carry-forward (informational)

Recorded here so the merged project state carries the pre-registration verdict
without re-reading the memo.

**Pre-registration verdict:** recorded — the ML-baseline evaluation /
interpretation / decision layer is pre-registered **before** any pre-v002 result
exists.

**Contract-amendment verdict:** amended — Phase 4bn-AC carried forward verbatim
as the source contract; amendment 001 added; no source-contract field changed.

**Evaluation claim scope:** the first pre-v002 baseline may claim only (a) whether
the 45 causal aggTrades features carry short-horizon directional information, (b)
whether the v002 small-lift sign reproduces across the larger pre-v002 regime
span, (c) whether calibration/confidence-tail behaviour is adequate/marginal/fails.
It may **not** claim tradability, profitability, strategy viability, execution
viability, slippage/spread adequacy, live-readiness, paper/shadow readiness, PnL,
backtest validity, production suitability, or economic significance.

**Target interpretation amendment:** `forward_direction_15s` retained but reframed
as a **non-economic information / pipeline diagnostic**; not a strategy label; not
a PnL label; may contain last-trade-to-last-trade / bid-ask-bounce artifacts
(aggTrades-only, no mid-price); strict-sign / no-deadband retained as anti-tuning
discipline but acknowledged noise-dominated; any economically anchored / deadband
/ mid-price / triple-barrier / longer-horizon / volatility-scaled / MFE / MAE /
R-multiple / PnL label requires a separate future contract revision and likely
new data or labels.

**Overlapping-label dependence policy:** Option 1 — row-level metrics
descriptive-only; decision evidence is the UTC date / month block; continue/kill
requires cross-block agreement; no per-row significance / p-value /
confidence-interval / "significant" language until a future separately-authorized
block-bootstrap / date-level jackknife method; fixed decimation/stride reserved,
not adopted (would need a pre-registered justified constant from committed
evidence).

**Date/month-block + regime reporting policy:** every metric at aggregate /
per-UTC-month / per-UTC-date granularity per split; row and date counts
before/after filtering; split date inventories; effective-sample caveat adjacent
to aggregate metrics; no single aggregate metric governs a decision; validation
and holdout recognised as regime-narrow (both in the Oct–Nov 2024 window);
descriptive train-month metrics (Mar–Sep 2024) also required as regime-stability
context (train is not a generalization test and cannot alone govern
continue/kill). Required future report contents: train/validation/internal-holdout
date counts; dropped embargo dates; monthly row counts per split; monthly
target-class distribution; zero-class prevalence per month; monthly
supervised-row counts after filtering; monthly validation and internal-holdout
dry-run metrics; validation and internal-holdout aggregate + monthly metrics;
descriptive train-split monthly metrics.

**Metric registry (mandatory; no cherry-picking):** majority accuracy /
balanced-accuracy / macro-F1 floors; persistence baseline; accuracy; balanced
accuracy; macro-F1; per-class precision/recall/F1 for {-1, 0, +1}; confusion
matrix; predicted-class distribution; zero-class prevalence; predicted-zero rate;
log loss (where probabilities exist); Brier (where probabilities exist);
calibration / reliability table; high-confidence-tail size and accuracy;
train−validation deltas; validation−holdout deltas; filtered row/date counts by
split and month; dropped-row counts by split and reason.

**Calibration / confidence-tail policy:** carries the v002 finding that the
high-confidence tail did not beat the majority floor; mandatory confidence bins,
empirical accuracy per bin, reliability curve per split and month, ≥0.8 tail size
and accuracy, beats-majority boolean per bin, and a usable / ranking-only /
unusable verdict; if the ≥0.8 tail does not exceed the majority accuracy floor by
a positive margin the probabilities are declared **unusable** for confidence-gated
interpretation and "trade only when confident" is pre-emptively rejected;
calibration failure is a kill contributor, not necessarily a standalone full kill.

**Cost-realism descriptive policy:** descriptive only; authorizes no trading rule
/ cost-aware label / PnL / backtest; mandatory `forward_log_return_15s`
distribution by split/month; mandatory share of rows with
`|forward_log_return_15s| > 16 bps` (locked round-trip); optional share > 8 bps; a
tiny >16 bps share means 15s is almost never economically relevant at the locked
cost, confining value to the information diagnostic; does not by itself kill the
arc if information-diagnostic value remains.

**Success / continue / kill criteria (pre-registered before any result):** KILL /
close-arc if any of — model fails to beat both majority and persistence floors on
validation accuracy by ≥ +2.0 pp; balanced accuracy fails ≥ +1.0 pp over the
majority floor and macro-F1 fails ≥ +0.03 absolute (both); improvement
concentrated in one month / a minority of date-blocks; internal-holdout dry-run
reverses the uplift sign on accuracy or macro-F1 materially; calibration unusable
AND classification lift also fails the margins; cost stats show near-zero economic
relevance AND diagnostic lift also fails. CONTINUE to exactly one bounded
follow-up only if all of — beats both floors on validation accuracy by ≥ +2.0 pp
AND macro-F1 by ≥ +0.03 absolute; holdout does not reverse the uplift sign;
improvement in a majority of evaluated validation date-blocks AND months;
calibration at least directionally usable/fixable (or classification lift strong
and stable enough for a ranking-only follow-up); cost stats acknowledged (not
tradable at 15s, possibly information-diagnostic). Allowed bounded follow-up
categories: (1) longer-horizon label memo; (2) bookTicker / mid-price
data-admissibility memo; (3) code-only evaluation-framework extension (e.g.
block-bootstrap inference); (4) one fixed-capacity model-comparison memo.
Thresholds may not be relaxed post-result; only a separately authorized docs-only
amendment before the baseline is run, justified from committed evidence, may
change them — never to rescue a near-miss.

**Ambiguous-result handling:** record `INVESTIGATE_AMBIGUOUS` (authorizes only one
further docs-only decision memo) if aggregate metrics clear margins but
date/month-block evidence is mixed; validation improves but internal holdout does
not (without full sign reversal); classification improves past margins but
calibration fails; or the result suggests information but is not clean enough for
`CONTINUE_ONE_FOLLOWUP`. Ambiguous results must not silently become continue;
default on ambiguity is remain paused.

**Finite arc-budget / stopping-rule posture:** Phase 4bn-AF code-only skeleton
(synthetic fixtures, no data read, encodes this amendment) → Phase 4bn-AG
data-reading builder authorization + a single builder run → Phase 4bn-AH
descriptive dataset diagnostics (no models) → Phase 4bn-AI fixed baseline run +
verdict → Phase 4bn-AJ arc-decision (close or exactly one bounded follow-up).
After Phase 4bn-AJ the arc must either close or authorize exactly one bounded
follow-up; it may not spawn an open-ended sequence of further readiness / contract
/ interpretation memos. Phase letters are indicative and may be re-lettered or
compressed; the finite five-step-then-decide shape is pre-registered. Each step
requires separate operator authorization; the budget is a posture, not an
authorization.

**Strategy / PnL / backtest hard boundary:** no pre-v002 baseline result, however
strong, authorizes strategy construction, signal generation, threshold trading,
confidence-gated trading, backtesting, PnL, position sizing, execution logic,
live-readiness, paper / shadow trading, or exchange-write. Any such path requires
a separate future M0-style mechanism-admissibility memo clearing at minimum M0.5
cost realism at the locked 8 bps/side · 16 bps round-trip (never deferred),
execution feasibility, slippage/spread assumptions, label economic relevance,
strategy admissibility versus the retained rejections and the M0 §7.D
microstructure-lane `NOT_RECOMMENDED_NOW` posture, and the Phase 4al no-rescue
constraints.

**Skeleton amendment obligations:** a future Phase 4bn-AF skeleton must
encode/reserve inert interfaces for the evaluation-metrics registry, the
date/month-block reporting schema, dependence-caveat fields (incl. an unset
decimation-stride field defaulting to `none`), frozen success/kill/investigate
bucket constants, a calibration output schema, descriptive cost fields,
non-authorization flags, a no-strategy-boundary constant, proof fields for
row/date/month counts by split and reason, and the Phase 4bn-AD no-data-I/O and
fail-closed controls — synthetic in-memory fixtures only; reads no data; creates
no output directory; writes no Parquet; mutates no manifest; produces no
`data/research` or `data/microstructure` artefact.

**Remaining blockers before code-only skeleton:** this amendment (done) + separate
skeleton authorization; not blocked by `source_admissible_for_data_read=false` /
`source_admissible_for_dataset_builder=false` (reads no data, creates no output).
**Remaining blockers before data reads:** recorded contract + amendment;
code-level builder bound to the passed gates (`3452fd9d…` / `db731d1b…` /
`ffb5b09…`), manifests, hashes, and the Phase 4bn-AA split artefact; leakage /
split-integrity proof + Phase 4bn-L budget preflight bound into the builder;
separate data-read authorization (`source_admissible_for_data_read=false`).
**Remaining blockers before real dataset builder:** recorded contract +
amendment; the Phase 4bn-AD readiness decision (done — code-only first); a passing
code-only skeleton encoding this amendment with synthetic validation; leakage
proof + budget preflight designed into the builder; separate builder
authorization (`source_admissible_for_dataset_builder=false`). **Remaining
blockers before ML training:** all data-read + dataset-builder blockers;
target/horizon/filtering locked (`forward_direction_15s`, 15s, 3-class signed —
done) and the evaluation / dependence / success-kill layer pre-registered (done);
a committed end-to-end pre-v002 trainer (does **not** exist); separate ML
authorization (`ml_authorized=false`).

**Selected next recommendation:**
`RECOMMEND_AUTHORIZE_CODE_ONLY_ML_DATASET_BUILDER_SKELETON__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— a code-only ML dataset builder skeleton (Phase 4bn-AF) with synthetic fixtures +
offline tests only, encoding this amendment. Do not authorize a data-reading
builder yet. A current-state consolidation memo is a recommended near-term
parallel docs-only option (not a blocker). Final `git status` / `git log` / SHAs
are reproduced in the final operator report so the operator need not run a
separate status/SHA check manually.
