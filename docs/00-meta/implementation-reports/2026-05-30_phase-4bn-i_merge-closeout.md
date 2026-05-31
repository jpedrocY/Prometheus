# Phase 4bn-I — Merge Closeout

**Phase 4bn-I is now merge-complete on main.** **Phase 4bn-I is a docs-only
/ design-only / scoping-only acquisition execution plan.** **Phase 4bn-I
does not acquire data.** **Phase 4bn-I does not call public, Binance,
authenticated, or private endpoints.** **Phase 4bn-I does not migrate
storage.** **Phase 4bn-I does not create any database.** **Phase 4bn-I does
not compact Parquet.** **Phase 4bn-I does not create v003.** **Phase 4bn-I
does not authorize acquisition.** **Phase 4bn-I does not authorize any
successor.** **Phase 4bn-I does not read local parquets.** **Phase 4bn-I
does not inspect local data.** **Phase 4bn-I does not open any local
gitignored `data/research/` or `data/microstructure/` artefact.** **Phase
4bn-I does not create or modify any manifest.** **Phase 4bn-I does not run
diagnostics.** **Phase 4bn-I does not run ML.** **Phase 4bn-I does not train
models.** **Phase 4bn-I does not score models.** **Phase 4bn-I does not
generate predictions.** **Phase 4bn-I does not inspect the test holdout.**
**Phase 4bn-I does not use the sealed test split.** **Phase 4bn-I does not
rank features.** **Phase 4bn-I does not select features.** **Phase 4bn-I
does not prune features.** **Phase 4bn-I does not engineer features.**
**Phase 4bn-I does not tune hyperparameters.** **Phase 4bn-I does not tune
thresholds.** **Phase 4bn-I does not fit calibrators.** **Phase 4bn-I does
not run strategy research.** **Phase 4bn-I does not define a strategy.**
**Phase 4bn-I does not generate trade signals.** **Phase 4bn-I does not
simulate PnL.** **Phase 4bn-I does not run backtests.** **Phase 4bn-I does
not modify dataset layout.** **Phase 4bn-I does not open any WebSocket or
user stream.** **Phase 4bn-I does not use credentials, `.env`, `.mcp.json`,
MCP, or Graphify.** **Phase 4bn-I does not mutate any manifest.** **Phase
4bn-I does not mutate any successor-state artefact.** **Phase 4bn-I does not
commit `data/microstructure`.** **Phase 4bn-I does not commit
`data/research`.** **Phase 4bn-I does not authorize Phase 4bn-J, Phase 5,
paper / shadow, live-readiness, deployment, exchange-write, production keys,
or any successor phase.** **Recommended state remains paused.**

## 1. Phase identity

- **Phase:** Phase 4bn-I — Docs-Only Acquisition Execution Plan.
- **Type:** docs-only / design-only / scoping-only governance memo
  (acquisition execution plan). **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because Phase
  4bn-I is adjacent to possible future data acquisition, longer-history
  microstructure planning, future local disk / runtime commitments,
  manifest / sidecar policy, possible future ML-baseline downstream
  admissibility, possible future holdout design, and possible future
  storage workload definition, while explicitly authorizing none of them.
  The separately authorized execution-plan phase that follows the Phase
  4bn-H recommendation
  `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-I acquisition execution plan memo,
  closeout, and narrow `current-project-state.md` Phase 4bn-I paragraph +
  new Current-phase block onto `main`, recording the decision
  `RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  as project state. The phase reads only committed repository Markdown
  reports and committed architecture documents; it opens no test-holdout
  row; it opens no local gitignored `data/research/` or
  `data/microstructure/` artefact; it reads no local parquet / CSV / JSON
  output; it mutates no manifest, sidecar, gate report, or successor-state
  artefact; it creates no local artefact; it runs no diagnostic, ML,
  simulation, backtest, or acquisition kernel.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-i/docs-only-acquisition-execution-plan`.

## 2. SHAs

- **`main` SHA before merge:** `654befd236884c8c47cc062722ac74c794272d12`
  (`docs(phase-4bn-h): finalize merge closeout shas`; `main == origin/main`
  verified pre-merge).
- **Base SHA:** `654befd236884c8c47cc062722ac74c794272d12`.
- **Branch tip SHA before merge:** `a513c4fd24324ccbd9c530c7460b04c77217b0e3`.
- **Branch (docs) commit SHA:** `a513c4fd24324ccbd9c530c7460b04c77217b0e3`
  (`docs(phase-4bn-i): plan acquisition execution`; the acquisition
  execution plan memo + closeout + narrow current-project-state.md
  paragraph + new Current-phase block are a single docs commit, which is
  also the branch tip).
- **Merge commit SHA:** `4733d90ce631cb23d1646329cb202c20103cf5a9`
  (`docs(phase-4bn-i): merge acquisition execution plan`).
- **Merge-closeout commit SHA:** `5aed51052fa841437f13b1173d66b933cd1b485a` (`docs(phase-4bn-i): add merge closeout`), recorded by the subsequent
  SHA-finalization commit. Per the repo convention used for Phase 4bn-H /
  4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B / 4bn-A, the merge-closeout
  commit cannot self-reference its own hash inside its own diff; the SHA is
  filled in by the subsequent SHA-finalization commit, which can reference
  the merge-closeout commit hash because that hash exists in `git log`
  before the SHA-finalization commit is created.
- **SHA-finalization commit:** recorded in the final operator report and
  `git log` as `docs(phase-4bn-i): finalize merge closeout shas`. Same
  convention: the SHA-finalization commit cannot self-reference its own
  hash inside its own diff; its SHA is captured in the final operator
  report and `git log`. After that commit and push, final `main` SHA ==
  final `origin/main` SHA == the SHA-finalization commit.
- **Final `main` / `origin/main` SHA after push:** equals the
  SHA-finalization commit; recorded in the final operator report.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `docs(phase-4bn-i): merge acquisition execution
  plan`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No
  force-push.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Source: none. **No source code added, modified, or deleted.**

Tests: none. **No test added, modified, or deleted.**

Scripts: none. **No committed script added, modified, or deleted.**

Docs (tracked):

- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_docs-only-acquisition-execution-plan.md`
  (added; the phase acquisition execution plan memo; 22 sections + 3
  appendices; 995 lines).
- `docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_closeout.md`
  (added; the phase closeout; 301 lines).
- `docs/00-meta/current-project-state.md`
  (modified — narrow Phase 4bn-I paragraph + new Current-phase block
  inserted immediately after the Phase 4bn-H paragraph and immediately
  before the existing Phase 4bn-H Current-phase block; prior Phase 4bn-A /
  4bn-B / 4bn-C / 4bn-D / 4bn-E / 4bn-F / 4bn-G / 4bn-H paragraphs and prior
  Current-phase blocks preserved as labelled historical context; +209 / −0).

Config: none. **No `pyproject.toml`, `README.md`, `.gitignore`, MCP file,
manifest, sidecar, gate report, successor-state artefact, existing source /
test / script file, or any `data/microstructure/` artefact was modified.**
No prior governance memo was modified beyond the narrow
`current-project-state.md` paragraph addition. **No `data/research/`
artefact was committed.** **No `data/microstructure/` artefact was
modified.** The merge-closeout file (this file) is added by the subsequent
merge-closeout commit on `main`, not by the merge commit itself.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 209 +++++
 .../2026-05-30_phase-4bn-i_closeout.md             | 301 +++++++
 ...e-4bn-i_docs-only-acquisition-execution-plan.md | 995 +++++++++++++++++++++
 3 files changed, 1505 insertions(+)
```

The diff matches the expected change set from the authorization prompt
exactly: two added docs files (memo + closeout) plus one narrow
modification to `current-project-state.md` (Phase 4bn-I paragraph + new
Current-phase block). No source / test / script / config / data / manifest
/ sidecar / gate-report / successor-state change beyond the three named
files.

## 6. Verdict

**MEMO RECORDED —
`RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Phase 4bn-I is the separately authorized docs-only / design-only /
scoping-only acquisition execution plan that takes the Phase 4bn-H
acquisition-readiness recommendation one level lower of abstraction by
pre-declaring the **exact** future acquisition envelope (Option C —
12-month continuous BTCUSDT Binance USDⓈ-M futures aggTrades history), the
exact UTC calendar range (2024-03-01 through 2025-02-28 inclusive UTC), the
exact canonical `data/microstructure/<family>/` path layout, the exact
source-endpoint policy confirmation requirement (public Binance USDⓈ-M bulk
archives only; fail-closed on any divergence; source-policy memo required if
ambiguous — and the committed `historical-data-spec.md` aggTrades-bulk-archive
source-policy gap flagged for the future phase to resolve), the exact
disk-footprint cap (5 GiB hard / 3 GiB warning), the exact derivation-time
cap (4 hours hard / 2 hours warning), the exact Phase 4bb-F sidecar policy
and manifest-immutability / `__vNNN` / non-eligible manifest-start policy,
the exact sealed-test preservation and new-holdout policy (existing v002
test split 2025-02-14 through 2025-02-28 remains sealed and terminal), the
exact 25 fail-closed stop conditions, the exact acquisition-phase
non-authorization envelope, and the exact post-acquisition successor chain.
**The recommended acquisition-only successor is recommended only and is not
authorized.** **The operator may equivalently remain paused, reject the
successor and close the ML arc, separately authorize a docs-only
storage-architecture decision memo, or separately authorize a docs-only
holdout and split-policy memo.** It preserves the Phase 4bn-H decision
verbatim
(`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`),
the Phase 4bn-G decision verbatim
(`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`),
the Phase 4bn-F decision verbatim
(`RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`),
the Phase 4bn-E decision verbatim
(`RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED`), the Phase 4bn-D
scoping decision verbatim
(`RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`),
the Phase 4bn-C interpretation verbatim
(`RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING`), and the Phase
4bn-B decision verbatim (`RECORD_EVIDENCE_ONLY`). It creates no local
artefact, mutates no manifest or successor-state artefact, acquires no data,
migrates no storage, creates no database, compacts no Parquet, modifies no
dataset layout, creates no v003 dataset, and authorizes no execution.
**Phase 4bn-I is a docs-only / design-only / scoping-only memo and
authorizes nothing.** The v002 label and feature manifests remain
`research_eligible = false` / `eligibility_gate_status = "pending"`; the
label manifest's `chronological_split_policy` remains `"not_yet_defined"` on
disk. The lifecycle state is **remain paused**.

After this merge commit, the merge-closeout commit, and the SHA-finalization
commit are pushed, Phase 4bn-I is project-complete on `main`. **Project
completion still requires the SHA-finalization commit below per the repo's
current Phase 4bn-H / 4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B / 4bn-A
SHA-finalization convention.**

### 6.1 Phase 4bn-H decision carried forward

`RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(Phase 4bn-H; merge-complete, SHA-finalized, project-complete on `main`).
Phase 4bn-H selected Option B as the candidate expansion shape, compared
calendar-coverage options A / B / C / D / E at design level only,
recommended Option C (12-month continuous BTCUSDT) as the cleanest
first-expansion coverage, preserved the Phase 4bn-G `A + F + C` storage
posture verbatim, defined 14 pre-acquisition gates and 13 stop conditions,
and recommended this docs-only acquisition execution plan. Phase 4bn-I is
the chosen acquisition execution plan and inherits the Phase 4bn-H
recommendation boundary verbatim.

### 6.2 Phase 4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C / 4bn-B decisions carried forward

- `RECOMMEND_AUTHORIZE_DOCS_ONLY_ACQUISITION_READINESS_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  (Phase 4bn-G; project-complete on `main`) — defined the combined
  data-expansion + storage-scaling scoping framework.
- `RECOMMEND_AUTHORIZE_COMBINED_DATA_EXPANSION_AND_STORAGE_SCOPING_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  (Phase 4bn-F; project-complete on `main`) — concluded the 90-day window
  is useful but not enough to prove broad sufficiency, insufficiency,
  representativeness, or outlier status; treated "outlier" as an unresolved
  risk, not a conclusion.
- `RECORD_FEATURE_DRIFT_EVIDENCE_ONLY__REMAIN_PAUSED` (Phase 4bn-E;
  project-complete on `main`) — partially ruled out gross
  train-vs-validation feature-distribution drift at the measurement-frame
  level only.
- `RECOMMEND_BOUNDED_ML_BASELINE_EXPANSION_PHASE_4BN_E_DESIGN_LEVEL_SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
  (Phase 4bn-D; project-complete on `main`) — scoped bounded expansion
  options but authorized nothing.
- `RECOMMEND_AUTHORIZE_BOUNDED_ML_BASELINE_EXPANSION_SCOPING` (Phase 4bn-C;
  project-complete on `main`) — interpreted Phase 4bn-B evidence as small
  descriptive lift, not edge.
- `RECORD_EVIDENCE_ONLY` (Phase 4bn-B; project-complete on `main`) —
  descriptive ML-baseline evidence on train / validation only; test holdout
  sealed (`test_rows_loaded: 0`).

Phase 4bn-I inherits all six decisions verbatim and softens none of them.

### 6.3 Phase 4bn-I is a docs-only / design-only / scoping-only memo

Phase 4bn-I adds two new tracked docs files under
`docs/00-meta/implementation-reports/` plus narrowly updates
`docs/00-meta/current-project-state.md`. **No** existing source / test /
committed-script / configuration / manifest / sidecar / gate-report /
successor-state mutation. **No** local data artefact created, read, hashed,
or mutated. **No** local parquet / CSV / JSON output read or inspected.
**No** diagnostic rerun. **No** ML rerun. **No** ML artefact, model binary,
row-level prediction, or reusable split mask created or persisted. **No**
acquisition, endpoint call, WebSocket / user stream, or credential /
`.env` / `.mcp.json` / MCP / Graphify use. **No** storage migration. **No**
database creation. **No** Parquet compaction. **No** dataset-layout
modification. **No** v003 dataset creation. **No** successor authorization.

### 6.4 Core interpretation preserved verbatim

- The current v002 microstructure ML-baseline window is **90 calendar
  days**.
- The split structure is **45 train days, 30 validation days, and 15 sealed
  test days**.
- The sealed test split remains sealed and was not inspected
  (`test_rows_loaded: 0`).
- Phase 4bn-B produced descriptive ML-baseline evidence only.
- Phase 4bn-C interpreted that evidence as small descriptive lift, not edge.
- Phase 4bn-D scoped bounded expansion options but authorized nothing.
- Phase 4bn-E partially ruled out gross train-vs-validation
  feature-distribution drift at the measurement-frame level only.
- Phase 4bn-F concluded the 90-day window is useful but not enough to prove
  broad sufficiency, insufficiency, representativeness, or outlier status.
- Phase 4bn-G defined a concrete data-expansion requirements framework and a
  concrete storage-scaling architecture comparison at design level only.
- Phase 4bn-H recommended a docs-only acquisition execution plan for a
  12-month continuous BTCUSDT expansion at design level only.
- Phase 4bn-I records the exact acquisition execution plan for that Option C
  envelope at design level only.
- Parquet remains canonical (Storage A). DuckDB querying Parquet in place
  remains the preferred non-invasive query-layer posture if needed (Storage
  C). DuckDB database cache remains deferred (Storage D). Parquet compaction
  remains deferred (Storage B). SQLite remains runtime / control metadata
  only, not research matrices (Storage E runtime-only).
- ETHUSDT remains deferred. v003 remains deferred / not created. Future
  acquisition remains not authorized. Future storage migration remains not
  authorized. Future v003 creation remains not authorized.
- None of the Phase 4bn-A through Phase 4bn-I evidence establishes edge,
  profitability, tradability, strategy-readiness, signal-readiness, paper /
  shadow readiness, or live-readiness.

### 6.5 Exact future acquisition plan recorded (design level only)

- **Symbol:** BTCUSDT only. **Market:** Binance USDⓈ-M futures. **Data
  family:** aggTrades only. **Shape:** 12-month continuous history.
- **Exact UTC range:** 2024-03-01 through 2025-02-28 inclusive UTC (365
  calendar days; extends the existing 90-day v002 window backward).
- **Existing v002 envelope included as terminal 90-day portion:** 2024-12-01
  through 2025-02-28.
- **Existing v002 sealed test split preserved untouched and terminal:**
  2025-02-14 through 2025-02-28.
- **New acquisition adds only pre-v002 history:** 2024-03-01 through
  2024-11-30. **No post-v002 dates.**
- **No** ETHUSDT; **no** extra horizons; **no** mark-price; **no** spot;
  **no** cross-venue; **no** order book; **no** tick data; **no** v003;
  **no** storage migration; **no** database creation; **no** Parquet
  compaction; **no** ML / diagnostics / strategy / signals / PnL / backtests.
- **v002 feature semantics preserved** (45 feature columns). **v002 label
  semantics preserved** (3-class strict-sign at 15s and 60s). **v002
  horizons 15s and 60s preserved.** Parquet remains canonical; DuckDB
  querying Parquet in place permitted only as a non-invasive query layer;
  no DuckDB database cache; no SQLite research matrices.
- **Disk-footprint cap:** 5 GiB hard / 3 GiB warning additional local
  footprint; fail-closed on preflight estimate over the cap and on actual
  footprint crossing the cap. **Derivation-time cap:** 4 hours hard / 2
  hours warning total wall-clock; fail-closed on preflight estimate over the
  cap and on actual runtime crossing the cap.
- **Source-policy caveat preserved:** the committed `historical-data-spec.md`
  does not explicitly enumerate the aggTrades bulk historical archive source
  at the same level of detail as some other Binance USDⓈ-M historical source
  policies. Phase 4bn-I does not resolve this gap and does not call
  endpoints. The future acquisition-only phase must confirm the exact source
  policy before fetching anything and must fail closed if source policy is
  insufficient or ambiguous, requiring a separately authorized source-policy
  memo before acquisition.
- **25 fail-closed stop conditions** recorded (memo §16): source / archive
  naming mismatch; public source unavailable; archive missing for any
  expected day; duplicate archive / overwrite attempt; unexpected schema;
  timestamp monotonicity violation; unexpected timestamp gap; unexpected
  duplicate aggTrade primary key; sidecar format mismatch; SHA256 hash
  mismatch; manifest validation failure; disk-footprint warning crossed;
  disk-footprint hard cap exceeded; derivation-time warning crossed;
  derivation-time hard cap exceeded; any v002 test-holdout read attempt; any
  new-ML-split attempt without authorization; any ML / diagnostics / strategy
  / PnL / backtest attempt; any DuckDB / SQLite / database creation attempt;
  any Parquet-compaction attempt; any `data/microstructure` or
  `data/research` commit attempt; any credential / private-endpoint /
  WebSocket / user-stream / `.env` / `.mcp.json` / MCP / Graphify usage; any
  manifest eligibility transition; any deviation from the exact UTC range;
  any requirement to add ETHUSDT / v003 / mark-price / spot / cross-venue /
  order-book / extra-horizon data.

### 6.6 Post-acquisition successor chain recorded (NONE authorized)

If a future acquisition-only phase is separately authorized and completed,
the project still requires separate successor phases before research use
(memo §18): (1) acquisition merge-closeout on main; (2) raw archive
eligibility validation / gate; (3) normalized artefact eligibility
validation / gate; (4) feature-family derivation and eligibility gate; (5)
label-family derivation and eligibility gate; (6) successor-state recording
if required by repo convention; (7) new chronological split / holdout policy
memo before any ML or diagnostics; (8) separate descriptive ML-baseline
implementation plan before any ML rerun; (9) separate diagnostics plan
before any diagnostics rerun; (10) no test-holdout use until a future
explicitly authorized terminal-holdout phase, if ever. **Each requires a
separate operator authorization; Phase 4bn-I authorizes none of them.**

### 6.7 Recommended successor (NOT authorized)

**Conditional next, NOT authorized.** Phase 4bn-I recommends a future
separately authorized **acquisition-only phase** (provisional Phase 4bn-J;
*not* authorized) bounded exactly by this plan (BTCUSDT aggTrades;
2024-03-01 through 2025-02-28; 5 GiB / 4 h caps; v002 semantics preserved;
Parquet canonical; DuckDB-in-place; no ETHUSDT / v003 / compaction /
database; sealed v002 test split untouched; 25 fail-closed stop conditions;
acquisition-only). The operator may equivalently:

- **remain paused** (no successor authorized);
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence);
- **separately authorize a docs-only storage-architecture decision memo**
  (must remain docs-only; must not authorize any storage migration);
- **separately authorize a docs-only holdout and split-policy memo** (must
  remain docs-only; must not transition `chronological_split_policy`).

Phase 4bn-I does **not** recommend acquisition as edge-search. Phase 4bn-I
does **not** recommend storage migration directly. Phase 4bn-I does **not**
recommend model tuning, threshold tuning, calibrator fitting, strategy /
signal work, or paper / shadow / live-readiness / deployment / exchange-write
/ production-key work.

## 7. Local gitignored outputs

**None.** Phase 4bn-I is a docs-only / design-only / scoping-only phase and
produced no local artefact under `data/microstructure/` or `data/research/`.
No CSV, no JSON, no parquet, no manifest, no sidecar, no gate report, no
successor-state file, and no database file was created. No diagnostic, ML,
simulation, backtest, or acquisition kernel was invoked. Phase 4bn-I never
opened, read, or hashed any predecessor local gitignored artefact (Phase
4bn-B / 4bn-E ML-baseline and diagnostics outputs; Phase 4bm-* artefacts;
v002 raw / normalized / feature / label parquets, manifests, sidecars, gate
reports, and successor-state JSONs all remain bit-for-bit unchanged because
Phase 4bn-I did not touch them).

## 8. Validation results

- `git diff --check main..phase-4bn-i/docs-only-acquisition-execution-plan`
  (pre-merge) → clean (no whitespace errors).
- `git diff --name-status main..phase-4bn-i/docs-only-acquisition-execution-plan`
  (pre-merge): `M docs/00-meta/current-project-state.md`;
  `A docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_closeout.md`;
  `A docs/00-meta/implementation-reports/2026-05-30_phase-4bn-i_docs-only-acquisition-execution-plan.md`
  (docs only).
- `git diff --stat main..phase-4bn-i/docs-only-acquisition-execution-plan`
  (pre-merge): `3 files changed, 1505 insertions(+)`.
- `git merge --no-ff` output: `Merge made by the 'ort' strategy`;
  `3 files changed, 1505 insertions(+)`; two `create mode 100644` entries
  for the new docs files.
- `git status --short` (pre and post merge) → clean working tree; only
  expected pre-existing untracked entry `.claude/scheduled_tasks.lock` and
  pre-existing gitignored `data/research/` + `data/microstructure/` local
  outputs.
- `git check-ignore -v data/research/` → `.gitignore:88: data/research/`.
- `git check-ignore -v data/microstructure/` →
  `.gitignore:85: data/microstructure/`.
- `git diff --check` (post-merge) → clean.
- `git log --oneline -4 --decorate` post-merge confirmed:
  `4733d90 (HEAD -> main) docs(phase-4bn-i): merge acquisition execution plan`
  above
  `a513c4f (phase-4bn-i/...) docs(phase-4bn-i): plan acquisition execution`
  above
  `654befd (origin/main, origin/HEAD) docs(phase-4bn-h): finalize merge closeout shas`.
- Repository tooling (`ruff` / `mypy` / `pytest`) is **not required** for a
  docs-only / design-only / scoping-only Tier 1 phase that creates no code
  surface, modifies no code, and adds no tests. The relevant validation
  surface for this merge is `git diff --check`, `git diff --stat`,
  `git diff --name-status`, `git status --short`, and `git check-ignore -v`
  on the data namespaces. All passed.
- No ML, diagnostic, backtest, or acquisition kernel was invoked. The Phase
  4bn-E feature-drift runner was not invoked. The Phase 4bn-B ML-baseline
  runner was not invoked. No local gitignored output was inspected. No
  test-holdout row was read. No public, Binance, authenticated, or private
  endpoint was called. No credential, `.env`, `.mcp.json`, MCP, or Graphify
  was used.
- Encoding / line-ending preservation:
  `docs/00-meta/current-project-state.md` remains UTF-8 without BOM, CRLF
  line endings; the two new tracked docs files were authored with the repo's
  prevailing Markdown convention (UTF-8; CRLF in the working tree; line
  endings normalized to LF in the repository by git on commit per the
  existing `.gitattributes` `* text=auto` policy, unchanged by this phase).
  No `.gitattributes` amendment was issued by this phase.

## 9. Upstream immutability evidence

**n/a — phase did not access any local artefact.** Phase 4bn-I is a
docs-only / design-only / scoping-only memo that opens no local data
artefact and reads only committed repository Markdown documents (the Phase
4bn-A through Phase 4bn-H reports and the data / architecture documents
enumerated in the Phase 4bn-I memo §4). It explicitly does **not** read,
hash, or inspect any test-holdout partition, any prior local Phase 4bn-B /
4bn-E / 4bm-* output, any v002 raw / normalized / feature / label parquet,
any manifest / sidecar, or any prior gate report / successor-state artefact.
Per the merge prompt's "do not inspect local data / do not hash local data
artefacts" constraint, this merge does not re-hash predecessor artefacts;
all prior governed artefacts remain bit-for-bit unchanged because the Phase
4bn-I branch brings forward zero changes to any of them (the branch diff is
exactly the three docs files in §4 / §5).

## 10. Manifest state preservation

- **v002 label manifest:** `research_eligible = false`;
  `eligibility_gate_status = "pending"`;
  `chronological_split_policy = "not_yet_defined"`;
  `label_family_research_use_authorized = false`;
  `diagnostics_authorized = false`; `ml_authorized = false` (historical, on
  disk). **No transition occurred** (manifest not accessed).
- **v002 feature manifest:** `research_eligible = false`;
  `eligibility_gate_status = "pending"`. **No transition occurred** (manifest
  not accessed).
- Prior sibling successor-state / gate-report artefacts: not accessed; no
  transition occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no existing source code modified;
- no existing test modified;
- no existing committed script modified;
- no config / `.gitignore` / `pyproject.toml` / `README.md` / MCP file
  modified;
- no `data/microstructure/` artefact committed;
- no `data/research/` artefact committed;
- no `data/microstructure/` artefact created, modified, moved, read, or
  hashed;
- no `data/research/` artefact created, modified, moved, read, or hashed;
- no local parquet / CSV / JSON output read or inspected;
- no manifest mutated; no `research_eligible` flipped; no
  `eligibility_gate_status` transitioned; no `chronological_split_policy`
  changed; no `diagnostics_authorized` / `ml_authorized` changed;
- no successor-state artefact mutated, created, moved, or accessed for
  mutation;
- no prior gate report mutated;
- no prior Phase 4bn-B / 4bn-E / 4bm-* local output mutated, read, or hashed
  by Phase 4bn-I;
- no ML model trained / scored; no prediction generated; no reusable split
  mask materialised; no model binary persisted; no row-level prediction
  persisted;
- no feature ranked, selected, pruned, or engineered;
- no hyperparameter or threshold tuned;
- no calibrator fitted;
- no probability-to-signal conversion;
- no strategy defined or run; no signal generated; no PnL simulated; no
  backtest run; no walk-forward optimization;
- test holdout not used for any reason; the existing v002 sealed test split
  (2025-02-14 through 2025-02-28) `test_rows_loaded: 0` preserved; the
  `iter_partitions(split="test", ...)` raise pattern remains in force;
- no data acquired; no Binance / public / authenticated / private endpoint
  called; no WebSocket / user stream opened; no credential / `.env` /
  `.mcp.json` / MCP / Graphify used;
- no v003 dataset created; no new dataset family created; no new label /
  feature / horizon / symbol acquisition; no longer-history acquisition; no
  multiple-window acquisition; no mark-price / spot / cross-venue /
  order-book / additional-aggTrades / tick acquisition;
- no storage migration; no database created; no Parquet compaction; no
  DuckDB database file created; no SQLite database file created; no
  partitioning policy changed; no compression policy changed; no dataset
  layout changed;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

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

All preserved verbatim. All prior phase results (Phase 4am .. Phase 4bn-H)
preserved verbatim.

## 13. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k / 4p / 4q / 4v / 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant (never invoked)
- Phase 4bb-F canonical sidecar / path policy
- Phase 4bl-F four-tier risk model + R-SIDECAR-CRLF standing rule + nine
  reusable non-authorization blocks
- Phase 4bm-A-P1 thin-prompt context-management standard
- Phase 4bm-D-P1 lightweight Claude Code workspace standard

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-I merge does not, and cannot, be construed as authorizing:

- any data acquisition (no aggTrades acquisition; no additional days /
  symbols / families / horizons beyond the locked 90-day v002 envelope; no
  longer single contiguous BTCUSDT aggTrades history; no multiple separated
  BTCUSDT windows; no ETHUSDT or other comparison-symbol acquisition; no v003
  dataset; no successor dataset family; no mark-price / spot / cross-venue /
  order-book / tick / additional aggTrades; no 30s / 5m / 30m / 1h / 4h /
  longer-horizon label generation; no barrier / target-before-stop / MFE /
  MAE / R-multiple / PnL labels);
- any storage migration (no Parquet → DuckDB / SQLite / other database
  migration; no Parquet compaction; no per-day → per-week / per-month
  partition restructuring; no new compression codec / dictionary / row-group
  policy applied to existing artefacts; no derived `.duckdb` database file
  creation; no SQLite database file creation; no other database file
  creation);
- any ML rerun; any ML implementation execution; any ML model training; any
  model scoring; any prediction generation; any feature ranking / selection /
  pruning / engineering; any hyperparameter tuning; any threshold tuning; any
  probability-to-signal conversion; any calibrator fitting; any model-binary
  or row-level-prediction persistence; any reusable split-mask
  materialisation; any meta-labeling; any ensemble construction;
- any strategy research / design; any signal generation; any trade-signal
  generation; any PnL simulation; any equity-curve construction; any Sharpe /
  Sortino / drawdown / hit-rate / trade-PnL metrics; any backtest; any
  walk-forward optimization;
- any use of the sealed test holdout for training, fitting, calibration,
  evaluation, tuning, design, model selection, threshold selection,
  reporting, or inspection;
- any diagnostics rerun beyond the already-completed Phase 4bn-E
  feature-drift diagnostic; any new diagnostic artefact creation;
- any manifest mutation; any successor-state mutation; any
  `research_eligible` / `eligibility_gate_status` / `chronological_split_policy`
  / `diagnostics_authorized` / `ml_authorized` transition from this evidence
  alone;
- any public / Binance / authenticated / private endpoint call; any WebSocket
  / user stream; any credential / `.env` / `.mcp.json` / MCP / Graphify use;
- Phase 4 canonical; Phase 5; Phase 4bn-J; the recommended acquisition-only
  phase itself; any further Phase 4bn-* successor; Phase 4bo-* / Phase 4bp-*;
- old-strategy alt-symbol rerun, cooled-down-family reopening, or 5m
  research-thread reopening (Phase 3t closure preserved);
- any future docs-only successor memo (storage-architecture decision memo,
  holdout and split-policy memo, regime-conditioning, class-weighting design,
  label / target rework, calibration design) beyond a separately authorized
  phase.

`RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
means only that Phase 4bn-I records the exact acquisition execution plan and
recommends remain-paused with a conditional acquisition-only successor that
must be separately authorized. **Any acquisition phase requires a separately
authorized phase.** **Any storage-migration phase requires a separately
authorized storage-architecture decision memo first.** **Any future
docs-only successor memo requires a separately authorized phase.**

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Phase 4bn-J — the recommended acquisition-only phase (or any phase under
  any name performing the acquisition; or any docs-only storage-architecture
  decision memo; or any docs-only holdout and split-policy memo; or any
  storage-migration phase; or any database-creation phase; or any
  Parquet-compaction phase; or any v003-creation phase);
- any further Phase 4bn-* successor / Phase 4bo-* / Phase 4bp-*; Phase 5;
  Phase 4 canonical;
- any ML implementation execution; any ML model training; any model scoring;
  any prediction generation; any feature ranking / selection / pruning /
  engineering; any model selection through results; any hyperparameter
  tuning; any threshold tuning; any calibrator fitting; any
  probability-to-signal conversion;
- any strategy research / design; any signal generation; any trade-signal
  generation; any PnL simulation; any backtest; any walk-forward
  optimization;
- any diagnostics rerun; any new diagnostic artefact creation; any ML
  artefact creation; any reusable split-mask materialisation; any row-level
  prediction persistence; any model-binary persistence; any test-holdout
  tuning / design / evaluation / inspection;
- any manifest mutation; any successor-state mutation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book / spot /
  cross-venue / longer-history / multi-window data acquisition;
- paper / shadow; live-readiness; deployment; exchange-write; production-key
  creation; authenticated APIs; private endpoints; user stream; live
  WebSocket implementation; MCP; Graphify; `.mcp.json`; credentials.

## 16. Recommended state

**Remain paused.**

Phase 4bn-I is now merge-complete on main and, after the SHA-finalization
commit and push, project-complete. The decision
`RECOMMEND_AUTHORIZE_ACQUISITION_ONLY_PHASE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
authorizes nothing. **Any acquisition phase requires a separately authorized
phase.** **Phase 4bn-J is not authorized by Phase 4bn-I.** **Recommended
state remains paused.**

**Conditional next, NOT authorized:** a Phase 4bn-J acquisition-only phase
bounded exactly by this plan (BTCUSDT aggTrades; 2024-03-01 through
2025-02-28; 5 GiB / 4 h caps; v002 semantics preserved; Parquet canonical;
DuckDB-in-place; no ETHUSDT / v003 / compaction / database; sealed v002 test
split untouched; 25 fail-closed stop conditions; acquisition-only) is the
cleanest non-paused option. It would, if separately authorized later, fetch
only the recommended 12-month BTCUSDT aggTrades history under the fixed
fail-closed contract recorded by Phase 4bn-I, produce only raw / normalized
/ feature / label artefacts and their non-eligible manifests / sidecars, and
authorize no ML / diagnostics / strategy / PnL / backtest / storage
migration / database creation / v003 / manifest eligibility transition.
Phase 4bn-J is **not authorized** by this merge. The operator may
equivalently choose:

- **remain paused** (no successor authorized);
- **reject further ML-baseline successors and close the ML arc**
  (operationally close the v002 ML-baseline family for further bounded
  expansion under current evidence);
- **separately authorize a docs-only storage-architecture decision memo**
  (requires a separate authorization prompt; must remain docs-only; must not
  authorize any storage migration or acquisition);
- **separately authorize a docs-only holdout and split-policy memo**
  (requires a separate authorization prompt; must remain docs-only; must not
  transition `chronological_split_policy`).

**No acquisition / storage migration / paper / shadow / live / exchange-write
/ production-key / credentials / MCP / Graphify option is valid from this
state unless separately authorized after this merge.**
