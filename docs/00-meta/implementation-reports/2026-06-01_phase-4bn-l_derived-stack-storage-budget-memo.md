# Phase 4bn-L — Derived-Stack Storage-Budget Memo

**Phase 4bn-L is branch-complete only by this work; not merged into main;
not project-complete.** Phase 4bn-L is a docs-only / storage-governance /
derived-stack budgeting / stage-boundary memo (**Tier 1 Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3). It sets
explicit storage caps, stage boundaries, preflight-measurement
requirements, and fail-closed stop conditions that any future
normalization, feature-derivation, or label-derivation phase on the
expanded 12-month BTCUSDT aggTrades envelope must honour **before** it may
run. It authorizes none of those downstream uses.

> **Recording a storage budget does not authorize normalization, feature
> derivation, label derivation, ML, diagnostics, strategy, or any
> successor phase. It does not flip `research_eligible`. It does not
> transition `eligibility_gate_status`. It does not read, create, or
> commit any local data artefact.**

---

## 1. Purpose

The purpose of Phase 4bn-L is to record a **storage-budget contract** for
the future 12-month BTCUSDT Binance USDⓈ-M futures aggTrades **derived
stack** (normalization, feature derivation, label derivation, temporary
working space, and total aggregate footprint), so that explicit caps,
stage boundaries, measurement requirements, and fail-closed stop
conditions exist on `main` **before** any future normalized / feature /
label phase can be separately authorized and executed.

The memo is **governance-only**: it makes no claim about edge,
predictiveness, signal quality, profitability, or readiness, and it does
not move the project toward any derived artefact. It writes a budget that
future phases must obey; it does not spend that budget. The Phase
4bn-J-R1 raw-only acquisition cap (10 GiB warning / 25 GiB hard) governed
raw acquisition only and explicitly did **not** size the derived stack;
this memo supplies the missing derived-stack budget as a separate,
stage-by-stage contract.

---

## 2. Authority and repository state

- **Branch:** `phase-4bn-l/derived-stack-storage-budget-memo`.
- **Base `main` SHA:** `d8d3ba845362e2c1d294522a89e3b90be93ba89f`
  (`docs(phase-4bn-k): finalize merge closeout shas`).
- Pre-branch verification: `HEAD == main == origin/main ==
  d8d3ba845362e2c1d294522a89e3b90be93ba89f`; Phase 4bn-K SHA-finalization
  commit `d8d3ba8`, merge-closeout `63a43cc`, merge `19c6661`, and branch
  `b00a4f3` all present on `main`; GitHub remote `origin` →
  `https://github.com/jpedrocY/Prometheus.git`, verified intact.
- Working tree before branch: only the expected untracked transient
  `.claude/scheduled_tasks.lock`; `data/microstructure/` and
  `data/research/` gitignored under `.gitignore:85` / `.gitignore:88`.
- Active local repo path: `D:\Prometheus`. Active Claude Code lightweight
  workspace: `D:\ClaudeRuns\prometheus-light`.
- Phase 4bn-L creates a branch only; it does **not** merge into `main`
  and does **not** record a merge-closeout.

---

## 3. Phase type and strict scope

Phase 4bn-L is a docs-only / storage-governance / derived-stack budgeting
/ stage-boundary memo, classified **Tier 1 — Full Phase** because it sets
storage caps and stage boundaries adjacent to future normalization,
feature derivation, label derivation, future holdout / split policy,
future ML-baseline admissibility, and future local disk / runtime
commitments — while explicitly authorizing no normalization, no features,
no labels, no ML, no diagnostics, and no downstream use.

**Allowed (and the entirety of what was done):** read committed
repository Markdown reports and committed code / tests; synthesize the
storage implications of the raw acquisition and raw gate; define
stage-by-stage caps for future normalization, feature derivation, and
label derivation; define temporary working-space caps; define total
derived-stack caps; define preflight-measurement requirements; define
per-stage stop conditions; define local-path and gitignore boundaries;
define what future phases must measure and report; define when the
project must stop and require a new storage memo; create tracked
documentation; update `docs/00-meta/current-project-state.md` narrowly.

**Forbidden (and not done):** no normalization; no feature derivation; no
label derivation; no raw acquisition; no endpoint / public endpoint /
Binance / `data.binance.vision` contact; no archive or CHECKSUM download;
no HEAD preflight; no local raw zip read; no v002 terminal-window read; no
sealed test-split read; no local `data/research` read; no local
`data/microstructure` artefact read; no diagnostics; no ML training /
scoring / prediction; no feature ranking / selection / pruning /
engineering; no hyperparameter / threshold tuning; no calibration
fitting; no strategy / signal / PnL / backtest; no manifest mutation; no
successor-state mutation; no gate-report mutation; no `research_eligible`
flip; no `eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized` transition; no `data/research`
or `data/microstructure` artefact creation or commit; no storage
migration; no DuckDB / SQLite database; no `.duckdb` / `.sqlite`; no
Parquet compaction; no v003; no ETHUSDT; no extra horizons; no mark-price
/ spot / cross-venue / order-book / tick data; no paper / shadow / live /
exchange-write / production keys; no credentials / `.env` / `.mcp.json` /
MCP / Graphify; no successor authorization.

---

## 4. Evidence base and input boundary

**Committed evidence read:** `docs/00-meta/current-project-state.md`; the
process standards (`merge-closeout-standard.md`,
`phase-risk-tiering-standard.md`, `phase-workflow-standard.md`,
`phase-prompt-template.md`, `operator-report-standard.md`); the Phase
4bn-K implementation report, merge-closeout, and closeout; the Phase
4bn-J-R2, 4bn-J-R1, 4bn-J, 4bn-I, and 4bn-G implementation reports,
merge-closeouts, and closeouts; the data specs (`data-requirements.md`,
`historical-data-spec.md`, `timestamp-policy.md`, `dataset-versioning.md`)
and `database-design.md`; the committed tooling
`scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py`,
`scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py`,
`scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`,
`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py`, and their
test modules. README is treated as potentially stale and is **not** used
as current-state authority.

**Input boundary (hard, fail-closed for this phase):** the memo uses only
committed repository Markdown and committed code / tests as evidence. It
does **not** open any local raw zip, normalized parquet, feature file,
label file, gate report, manifest, sidecar, or any `data/research` /
`data/microstructure` artefact; it does not hash, count, or inspect any
local gitignored data; it makes no endpoint call and uses no credentials,
`.env`, `.mcp.json`, MCP, or Graphify. Every numeric figure carried
forward (footprint, row count, runtime, prior caps, the ~150–250 / ~300
GiB derived-stack planning estimate) is quoted from committed reports, not
recomputed from local data.

---

## 5. Phase 4bn-K result carried forward

Phase 4bn-K result:
`RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`;
**33 / 33** checks PASS / 0 FAIL / 0 ERROR over the Phase 4bn-J-R2
pre-v002 raw segment (BTCUSDT / Binance USDⓈ-M futures / aggTrades;
2024-03-01 .. 2024-11-30 inclusive UTC; 275 daily archives). The gate
recomputed and matched the recorded aggregates exactly (275 archives, 275
sidecars, **5,140,686,147 bytes**, **400,001,695** rows); verified segment
manifest SHA256
`1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1` and
acquisition-log SHA256
`0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`;
wall-clock 496.2 s; 281,600 sampled rows validated. The segment remains
**non-eligible** in the research sense (`research_eligible` stays
`false`); `eligibility_gate_status` stays `pending`; no manifest
eligibility transition occurred; the v002 terminal window
(2024-12-01 .. 2025-02-28) was treated by reference only and not read; the
sealed v002 test split (2025-02-14 .. 2025-02-28) was untouched. Phase
4bn-K's decision was
`RECOMMEND_AUTHORIZE_DOCS_ONLY_DERIVED_STACK_STORAGE_BUDGET_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
— i.e. it recommended exactly this memo. Phase 4bn-L is that memo.

---

## 6. Raw layer status

The existing raw layer is **already acquired and gate-passed** for the
pre-v002 segment, and is **not** re-budgeted, revalidated, or read by this
memo:

- **Already-measured local raw pre-v002 segment:** 5,140,686,147 bytes /
  **4.788 GiB** (275 daily archives + 275 sidecars + one segment manifest
  + one acquisition log), 400,001,695 rows inventoried.
- **Status:** local, gitignored under `.gitignore:85`, **non-eligible**
  (`research_eligible: false`, `eligibility_gate_status: "pending"`),
  **not to be committed**, and **not** revalidated or read by this memo.
- **Raw-only acquisition cap (carried forward unchanged from Phase
  4bn-J-R1):** **10 GiB warning / 25 GiB hard** additional local raw
  acquisition footprint. This cap governs raw acquisition only and is
  **not** reused for the derived stack.
- **No new raw acquisition is authorized** by this memo. The existing v002
  terminal raw window and the sealed v002 test split remain untouched and,
  for any future derived phase, structurally off the segment.

---

## 7. Derived-stack risk being budgeted

The risk this memo budgets is that a future normalization / feature /
label phase, run on the full 12-month BTCUSDT aggTrades envelope, expands
local disk footprint and runtime **without an explicit, stage-separated,
fail-closed cap** and silently fills the working drive `D:` or runs
unbounded to "finish the run." The committed planning context (Phase
4bn-G combined data-expansion + storage-scaling architecture scoping memo,
carried forward verbatim in the Phase 4bn-J-R1 paragraph and reaffirmed in
the Phase 4bn-K implementation report §20) estimated that the full
ML-ready 12-month derived stack may plausibly require **~150–250 GiB**
with **~300 GiB comfortable working headroom**, and classified every
derived-stack-expanding storage option as "compatible but deferred"
pending explicit storage governance. This memo supplies that governance as
a stage-by-stage budget. It is grounded in the raw footprint already
measured (4.788 GiB raw → normalized aggTrades and v002-compatible feature
/ label artefacts are materially larger per the planning estimate) and in
the recorded ~150–250 / ~300 GiB envelope; the draft budget values below
are adopted because they are consistent with that committed evidence.

---

## 8. Normalized layer budget

Applies **only** to future normalized aggTrades outputs for the expanded
envelope. **No authorization in this phase.**

- **Warning threshold:** **100 GiB** additional normalized-artefact
  footprint.
- **Hard cap:** **150 GiB** additional normalized-artefact footprint.
- **Runtime warning threshold:** **4 hours**.
- **Runtime hard cap:** **8 hours**.
- The future normalization phase **must preflight-estimate** output
  footprint and runtime before writing.
- The future normalization phase **must measure at day / month
  boundaries** during execution.
- The future normalization phase **must fail closed** on any cap breach
  (footprint warning crossed → log and continue toward hard cap with
  intensified measurement; footprint hard cap or runtime hard cap exceeded
  → stop, report partial outputs, leave all outputs non-eligible).
- Future normalized manifests must start `research_eligible: false`,
  `eligibility_gate_status: "pending"`; normalization must not flip
  eligibility.

---

## 9. Feature layer budget

Applies **only** to future v002-compatible feature outputs. **No
authorization in this phase.** Feature derivation must not run until
normalization completes and passes its own gate.

- **Warning threshold:** **50 GiB** additional feature-artefact footprint.
- **Hard cap:** **100 GiB** additional feature-artefact footprint.
- **Runtime warning threshold:** **4 hours**.
- **Runtime hard cap:** **8 hours**.
- The future feature phase **must preflight-estimate** before writing and
  **must fail closed** on cap breach (partial outputs reported and left
  non-eligible).
- Future feature manifests must start `research_eligible: false`,
  `eligibility_gate_status: "pending"`.

---

## 10. Label layer budget

Applies **only** to future v002-compatible label outputs. **No
authorization in this phase.** Label derivation must not run until the
required normalized / feature prerequisites are complete and separately
authorized.

- **Warning threshold:** **75 GiB** additional label-artefact footprint.
- **Hard cap:** **125 GiB** additional label-artefact footprint.
- **Runtime warning threshold:** **4 hours**.
- **Runtime hard cap:** **8 hours**.
- The future label phase **must preflight-estimate** before writing and
  **must fail closed** on cap breach (partial outputs reported and left
  non-eligible).
- Future label manifests must start `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`.

---

## 11. Temporary workspace budget

Applies to transient working files produced while any future derived stage
runs (decompression scratch, intermediate parquet, sort spill, etc.).

- **Warning threshold:** **50 GiB** temporary working footprint.
- **Hard cap:** **100 GiB** temporary working footprint.
- Temporary files **must be cleaned on success or on fail-closed stop**.
- Temporary files **must live under an explicit gitignored path** (under
  the existing `data/microstructure/` conventions, e.g. a dedicated
  gitignored `tmp/` subtree; never committed; never under a tracked path).
- Future phases **must report pre-cleanup and post-cleanup footprint**.

---

## 12. Total derived-stack budget

This is the **binding aggregate cap**. It includes normalized + feature +
label + temporary files **while running**, measured as additional
footprint **beyond** the raw archives.

- **Warning threshold:** **250 GiB** total additional derived-stack
  footprint beyond raw archives.
- **Hard cap:** **300 GiB** total additional derived-stack footprint
  beyond raw archives.
- If any future preflight estimates total derived-stack footprint **above
  300 GiB**, the phase must **stop and require a new storage memo** before
  execution.
- If actual footprint crosses **300 GiB** during execution, the phase must
  **fail closed**.

**Relationship to per-stage caps (binding interpretation).** The
per-stage hard caps (normalized 150 + feature 100 + label 125 + temporary
100 = 475 GiB) are **individual ceilings** for each stage in isolation;
they are deliberately not additive into a single permitted total. The
**total derived-stack hard cap of 300 GiB is lower than the sum of the
per-stage caps and governs the aggregate**: no combination of stages may
exceed 300 GiB of concurrent additional footprint regardless of remaining
per-stage headroom. The per-stage caps prevent any single stage from
running away; the total cap prevents the stack as a whole from exceeding
the ~300 GiB comfortable-headroom envelope recorded in the Phase 4bn-G
planning context. When the per-stage and total caps disagree, the total
cap binds.

---

## 13. Free-space floor and D: drive rule

The working drive for all derived artefacts is `D:` (active repo path
`D:\Prometheus`, active workspace `D:\ClaudeRuns\prometheus-light`).

- **Before** any future derived-stage execution, require **at least 500
  GiB free on `D:`** at preflight. If `D:` free space is below 500 GiB at
  preflight, **fail closed** and require an operator decision.
- **During** execution, if `D:` free space falls below **350 GiB**, **fail
  closed before proceeding** to the next stage / day / month.
- This floor is **not** an expectation that 500 GiB will be consumed (the
  total derived-stack hard cap is 300 GiB). It preserves working headroom,
  absorbs temporary working files, and prevents `D:` from becoming
  dangerously full mid-run. The floor and the cap are independent
  fail-closed conditions; either alone is sufficient to stop a future
  phase.

---

## 14. Stage-boundary rules

The memo records the following binding stage-boundary rules for all future
derived work:

1. **Normalization must be separately authorized** after Phase 4bn-L is
   merged. It is not authorized here.
2. **Feature derivation must not run** until normalization completes and
   passes its own gate.
3. **Label derivation must not run** until the required normalized /
   feature prerequisites are complete and separately authorized.
4. **ML must not run** until raw, normalized, feature, and label gates
   pass **and** a separate chronological-split / holdout policy is
   authorized.
5. **Diagnostics must not run** until separately authorized.
6. **Strategy / signals / PnL / backtests must not run.**
7. **No phase may silently exceed its budget to "finish the run."**
8. If any cap is exceeded, the phase must **fail closed, report partial
   outputs, and leave all outputs non-eligible**.
9. Any future partial outputs must remain **gitignored and uncommitted**.
10. Any future manifests must start `research_eligible: false` and
    `eligibility_gate_status: "pending"` (label manifests additionally
    `chronological_split_policy: "not_yet_defined"`).
11. **No future execution phase may flip eligibility as part of
    generation.** The Phase 4aw
    `MicrostructureManifest.flip_research_eligible(...)` always-raises
    invariant is preserved and must never be invoked by a generation
    phase.

---

## 15. Path and storage posture

Preserved verbatim from the committed storage posture (Phase 4bn-G /
4bn-I / 4bn-J-R1 / 4bn-K):

- **Active repo path:** `D:\Prometheus`. **Active Claude workspace:**
  `D:\ClaudeRuns\prometheus-light`.
- Raw / normalized / feature / label outputs under the existing
  `data/microstructure/` conventions (raw under
  `data/microstructure/raw/`, normalized under
  `data/microstructure/normalized/`, features under
  `data/microstructure/features/`, labels under
  `data/microstructure/labels/`, manifests under
  `data/microstructure/manifests/`, gate reports under
  `data/microstructure/gate-reports/`).
- Research outputs, **if ever authorized later**, under `data/research/`;
  `data/research/` remains off-limits to all derived-stack execution
  phases.
- **No `data/microstructure` commits. No `data/research` commits.**
- **Parquet remains canonical** for future normalized / feature / label
  artefacts.
- **No DuckDB database cache.** DuckDB **in-place querying of Parquet** is
  allowed only if separately needed and non-invasive (Storage C). **No
  `.duckdb` files.**
- **No SQLite research matrices. No `.sqlite` files.** (SQLite remains
  runtime / control-metadata only, per Storage E, preserved verbatim.)
- **No Parquet compaction** unless separately authorized by a
  storage-architecture phase (Storage B deferred).
- **No storage migration. No v003.**

---

## 16. Future preflight measurement requirements

Every future derived stage (normalization, feature, label) must, before
writing any artefact, measure and record:

1. A **preflight footprint estimate** for the stage's outputs (GiB).
2. A **preflight runtime estimate** for the stage (hours).
3. A **preflight total derived-stack footprint estimate** (this stage's
   estimate + already-written derived footprint), checked against the 300
   GiB total hard cap.
4. **`D:` free space** at preflight, checked against the 500 GiB floor.
5. The **per-stage cap and total cap** it is operating under, recorded in
   the run log.

During execution every future derived stage must measure and report:

6. **Footprint at day / month boundaries**, checked against the per-stage
   and total caps.
7. **Elapsed runtime**, checked against the per-stage runtime caps.
8. **`D:` free space**, checked against the 350 GiB in-execution floor
   before proceeding to the next stage / day / month.
9. **Temporary workspace footprint** (pre-cleanup) and **post-cleanup
   footprint**.

If a stage **cannot produce a preflight estimate**, it must **fail
closed** before writing (see §17).

---

## 17. Future fail-closed stop conditions

Any future derived-stack phase must **fail closed** (stop, report partial
outputs, leave all outputs non-eligible and uncommitted) on any of the
following:

1. Preflight cannot estimate output footprint.
2. Preflight estimate exceeds the per-stage hard cap.
3. Preflight estimate exceeds the total derived-stack hard cap (300 GiB) —
   stop and require a **new storage memo** before execution.
4. `D:` free-space floor below 500 GiB before execution.
5. `D:` free space falls below 350 GiB during execution.
6. Any temporary workspace exceeds 100 GiB.
7. Any stage runtime exceeds its hard cap (8 hours per stage).
8. Any attempt to read sealed test data.
9. Any attempt to flip `research_eligible`.
10. Any attempt to transition `eligibility_gate_status` to eligible.
11. Any attempt to create v003.
12. Any attempt to create DuckDB / SQLite / database files.
13. Any attempt to compact Parquet.
14. Any attempt to write outside the approved gitignored data paths.
15. Any attempt to commit `data/microstructure` or `data/research`.
16. Any attempt to run ML, diagnostics, strategy, PnL, or backtests.
17. Any need for ETHUSDT, mark-price, spot, cross-venue, order-book, tick,
    or extra-horizon data.
18. Any deviation from BTCUSDT / Binance USDⓈ-M futures / aggTrades /
    v002-compatible semantics.
19. Any missing prerequisite gate (raw / normalized / feature gate not
    passed before the dependent stage).
20. Any ambiguity about whether a future output is raw, normalized,
    feature, label, or research.

---

## 18. Decision

**`RECOMMEND_AUTHORIZE_NORMALIZATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`**

Rationale (repository-evidence-grounded): the raw segment has been
acquired (Phase 4bn-J-R2) and has passed the raw archive gate (Phase
4bn-K, 33 / 33 PASS), and this memo now records explicit, stage-separated,
fail-closed derived-stack storage caps grounded in the committed ~150–250
/ ~300 GiB planning envelope. No repository evidence blocks progress and
the draft budget values are consistent with the committed planning
estimate, so the next clean non-paused technical step is a **separately
authorized normalization-readiness or normalization execution plan**. That
future step must still not derive features, labels, ML, diagnostics,
strategy, or research outputs, and must honour the budget recorded here.
**Phase 4bn-L authorizes nothing executable and authorizes no successor.**

The full set of admissible Phase 4bn-L decision options was:
`RECORD_DERIVED_STACK_STORAGE_BUDGET__REMAIN_PAUSED`;
`RECOMMEND_AUTHORIZE_NORMALIZATION_READINESS_OR_EXECUTION_PLAN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`
(selected);
`RECOMMEND_AUTHORIZE_SOURCE_POLICY_DOCUMENTATION_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_AUTHORIZE_PROCESS_DOC_PATH_UPDATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`;
`RECOMMEND_CLOSE_ML_BASELINE_ARC__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

---

## 19. Recommended state and successor options

**Recommended state: remain paused.** No next phase is authorized by Phase
4bn-L. The operator may, subject to separate operator authorization:
remain paused (default); request a merge prompt for Phase 4bn-L;
separately authorize a normalization-readiness or normalization execution
plan (the preferred recommendation — see §18), which must derive no
features / labels / ML / diagnostics / strategy / research and must honour
this budget; separately authorize a source-policy documentation memo;
separately authorize a process-doc `D:` path-string update (refreshing the
Phase 4bm-D-P1 lightweight-workspace standard's stale `C:` example paths
under its own §15 change-control); or reject further ML-baseline
successors and close the ML-baseline arc. No normalization / feature /
label / ML / diagnostics / strategy / PnL / backtest / storage-migration /
paper / shadow / live / exchange-write option is valid from this state
unless separately authorized after this branch is merged.

---

## 20. Explicit non-authorizations

Phase 4bn-L does **not** run normalization; does not derive features; does
not derive labels; does not run ML; does not train or score models; does
not generate predictions; does not run diagnostics; does not rank / select
/ prune / engineer features; does not tune hyperparameters / thresholds;
does not fit calibrators; does not run strategy / signals / PnL /
backtests; does not acquire data; does not call any endpoint / public
endpoint / Binance / `data.binance.vision`; does not download any archive
or CHECKSUM; does not run HEAD preflight; does not inspect any local raw
zip; does not read the v002 terminal window; does not touch the sealed
v002 test split; does not read any local `data/microstructure` or
`data/research` artefact; does not create a database / `.duckdb` /
`.sqlite`; does not compact Parquet; does not migrate storage; does not
create v003; does not mutate any manifest / sidecar / gate report /
successor-state artefact; does not flip `research_eligible`; does not
transition `eligibility_gate_status` / `chronological_split_policy` /
`diagnostics_authorized` / `ml_authorized`; does not create or commit any
`data/microstructure` or `data/research` artefact; does not use
credentials / `.env` / `.mcp.json` / MCP / Graphify; does not open any
WebSocket / user stream / private / authenticated endpoint; and does not
authorize Phase 5, paper / shadow, live-readiness, deployment,
exchange-write, production keys, or any successor phase.

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
round-trip = 16 bps; §1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 3v §8;
Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al refined no-rescue rule;
Phase 4aw `flip_research_eligible(...)` always-raises invariant (never
invoked); Phase 4bb-F canonical path + sidecar policy; the Phase 4bn-J-R1
raw-only cap amendment) is preserved verbatim. Phase 4 canonical remains
unauthorized.

---

## 21. Current-project-state update summary

`docs/00-meta/current-project-state.md` was updated narrowly: one new
Phase 4bn-L narrative paragraph and one new `Current phase:` block were
added; all prior paragraphs and `Current phase:` blocks (Phase 4bn-A …
Phase 4bn-K and earlier) are preserved verbatim as labelled historical
context. No other section of that document was changed.
