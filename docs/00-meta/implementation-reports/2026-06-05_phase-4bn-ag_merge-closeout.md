# Phase 4bn-AG — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-AG — Data-Reading ML Dataset Builder Authorization Memo.
- **Phase type:** docs-only / data-read authorization decision / ML dataset
  builder authorization conditions / leakage-proof and budget-preflight binding /
  no-data-read memo.
- **Action:** merge into `main`.
- **Merge purpose:** bring the branch-complete Phase 4bn-AG work (the
  data-reading builder authorization memo, the closeout, and the narrow additive
  `current-project-state.md` update) onto `main`.
- **Source branch:** `phase-4bn-ag/data-reading-builder-authorization-memo`.
- **Target branch:** `main`.
- **Risk tier:** **Tier 1 — Full Phase** per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3, because this phase
  decides whether the project may move from a code-only synthetic skeleton toward
  a future data-reading ML dataset builder path; an error could authorize local
  data reads, dataset-output creation, leakage-prone builder behaviour,
  budget-unsafe execution, or research-matrix / ML work too early — even though
  the phase itself reads no data and creates no data. The full 16-section
  merge-closeout structure is used.

---

## 2. SHAs

- **Pre-merge `main` / base SHA:** `51263952f2673526dccc39f99dc3b08e1124197a`
  (`docs(phase-4bn-af): finalize merge closeout shas`).
- **Branch / docs commit SHA:** `383a8addf1c8a0de0e8f4c4ceddff11f79843570`
  (`docs(phase-4bn-ag): authorize data-reading builder path`).
- **Merge commit SHA:** `bf1b2d977ad4516cbc4cd8bc7542301e8356e311`
  (`docs(phase-4bn-ag): merge data-reading builder authorization`).
- **Merge-closeout commit SHA:** recorded by the SHA-finalization commit below
  (`docs(phase-4bn-ag): add merge closeout` is this file's commit; its exact SHA
  is filled by the follow-up `docs(phase-4bn-ag): finalize merge closeout shas`).
- **SHA-finalization commit SHA:** `docs(phase-4bn-ag): finalize merge closeout
  shas` — its exact SHA equals the resulting `main` / `origin/main` tip;
  reproduced in the final operator report and `git log`.
- **Final `main` / `origin/main` SHA after push:** equal to the SHA-finalization
  commit SHA above; reproduced in the final operator report and `git log`.

---

## 3. Merge method

`git checkout main` → `git pull --ff-only origin main` (already up to date at
`5126395`) → `git merge --no-ff
phase-4bn-ag/data-reading-builder-authorization-memo -m "docs(phase-4bn-ag):
merge data-reading builder authorization"`. Merge made by the `ort` strategy; no
conflicts. No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no
force-push. Pushed to `origin/main` with no force, no skip-hooks, no skip-signing
(push status recorded in the final operator report).

---

## 4. Files brought forward by the merge

**Docs (3):**

- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ag_data-reading-builder-authorization-memo.md`
  (35 sections).
- **Added:**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-ag_closeout.md`.
- **Modified (additive only):** `docs/00-meta/current-project-state.md`
  (74 insertions, 0 deletions; one new Phase 4bn-AG paragraph after the Phase
  4bn-AF paragraph + one new `Current phase:` block ahead of the Phase 4bn-AF
  block; all prior content preserved verbatim).

**No source, tests, scripts, config, `.gitignore`, `pyproject.toml`, README, MCP
file, manifest, sidecar, gate report, successor-state artefact, split file,
research matrix, ML config, model output, prediction output, or data file was
added or modified.** **No `data/microstructure/` or `data/research/` file was
modified.**

---

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |   74 ++
 .../2026-06-05_phase-4bn-ag_closeout.md            |  254 +++++
 ...n-ag_data-reading-builder-authorization-memo.md | 1004 ++++++++++++++++++++
 3 files changed, 1332 insertions(+)
```

1332 insertions, 0 deletions. The diff matches the expected change set from the
merge prompt exactly (add the authorization memo, add the closeout, modify
`current-project-state.md` additively).

---

## 6. Result / verdict

**MEMO RECORDED — DATA-READING BUILDER PATH AUTHORIZED (RECOMMENDED, NOT GRANTED)
— MERGE COMPLETE.** Phase 4bn-AG is a docs-only authorization memo that decides
the project is ready to **recommend** a future, separately-authorized phase that
implements and runs a real data-reading pre-v002 ML dataset builder (re-lettered
Phase 4bn-AH), using the Phase 4bn-AF code-only skeleton as the contract surface,
and records the exact pre-read / pre-write / budget-preflight / leakage-proof /
sidecar / output-namespace / forbidden-output / one-time-run / validation
conditions that future phase must obey. It read no local data, created no local
data, created no output namespace, implemented no builder, ran no builder,
created no ML dataset / research matrix, trained no ML, ran no diagnostics /
strategy / signals / PnL / backtests, mutated no manifest, set no manifest field,
and authorized no successor. With this merge, Phase 4bn-AG is **merge-complete on
`main`**.

- **Result state:**
  `DATA_READING_BUILDER_AUTHORIZATION_MEMO_RECORDED__BUILDER_RUN_RECOMMENDED__NO_DATA_READ__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_DATA_READING_ML_DATASET_BUILDER_IMPLEMENTATION_AND_SINGLE_RUN__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Per project convention, project completion also requires the SHA-finalization
commit (`docs(phase-4bn-ag): finalize merge closeout shas`) that fills the exact
post-merge SHAs in §2; that commit is recorded below and in the final operator
report.

---

## 7. Local gitignored outputs (if any)

**None.** This phase created no `data/microstructure/` or `data/research/` output
and read none. `git check-ignore -v data/microstructure/` → `.gitignore:85`;
`git check-ignore -v data/research/` → `.gitignore:88`. The sole untracked entry
is the expected transient `.claude/scheduled_tasks.lock` (not committed). The
future output namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/` was **not**
created.

---

## 8. Validation results

- `git status --short` (pre- and post-merge) → only `?? .claude/scheduled_tasks.lock`.
- `git diff --check` → clean (no whitespace errors).
- `git diff --stat main..phase-4bn-ag/data-reading-builder-authorization-memo`
  (pre-merge) → 3 files, 1332 insertions, 0 deletions.
- `git diff --name-status main..phase-4bn-ag/…` → `M current-project-state.md`,
  `A …_data-reading-builder-authorization-memo.md`, `A …_closeout.md`.
- `git diff --numstat -- docs/00-meta/current-project-state.md` → `74 0`
  (additive only).
- `git diff --stat` (merge, `5126395..bf1b2d9`) → 3 files, 1332 insertions, 0
  deletions.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.
- No ruff / mypy / pytest run: docs-only phase; no code validation needed; the
  committed code state is unchanged and was read read-only for authorization
  grounding only in the branch phase. No repo-standard markdown linter exists;
  none run.
- No acquisition / raw / normalization / feature / label / gate / ML /
  diagnostics / backtest / strategy script was run; no endpoint called; no
  archive downloaded; no HEAD preflight; no local data read or created.
- Git emitted the standard LF→CRLF advisory for the two new docs files at branch
  commit time (Windows `.gitattributes` / `core.autocrlf` convention); cosmetic;
  committed blobs are correct.

---

## 9. Upstream immutability evidence (if applicable)

**n/a — phase accessed no local artefact.** Phase 4bn-AG reads and mutates no
manifest, sidecar, gate report, successor-state, or published dataset. The
published `__v002` families and the local gated pre-v002 normalized (4bn-O) /
feature (4bn-S) / label (4bn-W) segments and their gate reports (4bn-P / 4bn-T /
4bn-X) remain byte-for-byte immutable and unread. The Phase 4bn-AF skeleton
modules and the Phase 4bn-AA split artefact are unchanged. This merge adds only
three docs files.

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

The memo-level governance concepts `source_admissible_for_data_read` and
`source_admissible_for_dataset_builder` remain **false** (they are documentation
concepts per Phase 4bn-AB §9, not manifest fields, and appear in no manifest).
The docs-level posture `data_read_authorization_recommended = true` /
`builder_implementation_run_recommended = true` is a recommendation recorded in
documentation only — never a manifest field. Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
preserved (never invoked; this phase imports no manifest reader). No manifest
mutation was invented.

---

## 11. Boundary confirmations

- No local data read; no local data created.
- Two docs files added + one docs file modified additively; no source / test /
  script / config / `.gitignore` / `pyproject.toml` / README / MCP file modified.
- No split file, research matrix, ML dataset, ML config, manifest, gate report,
  sidecar, successor-state artefact, model, score, or prediction created.
- No file under `data/microstructure/` or `data/research/` read or inspected
  (raw zip / normalized / feature / label Parquet / manifest / gate report /
  sidecar / v002-terminal / sealed-test).
- No v002 terminal window read; no sealed test touched (`test_rows_loaded = 0`).
- No ML trained / scored / predicted; no diagnostics; no strategy / signals /
  PnL / backtests.
- No acquisition, endpoint call, archive download, or HEAD preflight; no
  layer-gate re-run.
- No storage migration; no database; no Parquet compaction; no v003.
- No `research_eligible` flipped; no `eligibility_gate_status` /
  `chronological_split_policy` transitioned; no `source_admissible_for_data_read`
  / `source_admissible_for_dataset_builder` transitioned.
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
dataset contract; Phase 4bn-AD ML dataset builder readiness verdict; Phase 4bn-AE
pre-registration amendment; Phase 4bn-AF code-only skeleton. All prior phase
results preserved verbatim.

---

## 14. No-rescue constraints

The Phase 4bn-AG merge does not, and cannot, be construed as authorising:

- the future data-reading ML dataset builder implementation + single run
  (Phase 4bn-AH); a current-state consolidation memo; additional skeleton
  hardening; a source-admissibility gate artefact; a budget-preflight design
  memo; a full-envelope reference-assembly memo; a holdout-boundary memo;
- any actual data read of the pre-v002 normalized / feature / label segments;
  creating the future output namespace; writing any Parquet / sidecar / manifest
  / gate report / proof;
- a research matrix; an ML dataset; ML model training, model selection, scoring,
  predictions, or any conversion of labels into signals;
- strategy signal construction, position state, entry / exit rules, backtest
  design, PnL, or diagnostics;
- reading the v002 terminal window or touching the sealed test
  (`test_rows_loaded = 0` preserved);
- relaxing any pre-registered success / continue / kill threshold, adopting a
  decimation stride, or introducing per-row significance inference;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- additional aggTrades / bookTicker / mid-price / mark-price / order-book
  acquisition;
- storage migration / database creation / Parquet compaction / v003;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`,
  or `chronological_split_policy`, or the memo-level
  `source_admissible_for_data_read` / `source_admissible_for_dataset_builder`,
  from this phase alone.

---

## 15. Successor authorization

**None.** No successor is authorized by this merge. A **data-reading ML dataset
builder implementation + single run (Phase 4bn-AH)** is *recommended* as the next
step but requires separate operator authorization. A **current-state
consolidation memo** is *recommended* as a near-term parallel docs-only option
but is not a blocker and is not authorized.

Candidate successors explicitly **NOT** authorized:

- the data-reading ML dataset builder implementation + single run (Phase 4bn-AH;
  recommended; not authorized)
- a current-state consolidation memo (recommended parallel option; not
  authorized)
- additional skeleton hardening
- a source-admissibility gate artefact
- a budget-preflight design memo
- a full-envelope reference-assembly memo
- a holdout-boundary memo
- a real data-reading builder run
- a research matrix; an ML dataset
- ML implementation / model training / scoring / predictions / diagnostics
- strategy / signals / PnL / backtest implementation
- additional aggTrades / bookTicker / mid-price / mark-price / order-book
  acquisition
- Phase 5; Phase 4 canonical
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials

---

## 16. Recommended state

**Remain paused.** No next phase authorized.

**Conditional next, NOT authorized:** a **data-reading ML dataset builder
implementation + single run (Phase 4bn-AH)** is the cleanest non-paused option.
It would be a code + controlled local data read + local gitignored output phase
(single run) that imports the Phase 4bn-AF skeleton, uses the Phase 4bn-AA split
artefact, binds the Phase 4bn-AC contract and Phase 4bn-AE amendment, validates
source scope and manifest/config/gate hashes before reading, runs the Phase
4bn-L budget preflight and fails closed before any write, emits a
machine-checkable leakage/split-integrity proof and Phase 4bb-F sidecars, creates
the single authorized gitignored namespace, writes nothing forbidden, and
preserves `test_rows_loaded = 0` and all non-authorization flags. A
**current-state consolidation memo** is a recommended parallel docs-only option
(the state doc is large / partially stale) but is not a blocker. Neither is
authorised by this merge.

---

## 17. Phase 4bn-AG carry-forward (informational)

Recorded here so the merged project state carries the authorization verdict
without re-reading the report.

**Docs added:** the authorization memo (35 sections) and the closeout. **Docs
modified:** `current-project-state.md` (additive; 74 insertions, 0 deletions).
**Code/tooling added or modified:** none. **Tests added or modified:** none.

**Data-read authorization verdict:** RECOMMENDED, not granted;
`source_admissible_for_data_read` remains false.

**Dataset-builder authorization verdict:** RECOMMENDED (single controlled run),
not granted; `source_admissible_for_dataset_builder` remains false.

**Manifest-transition posture:** no manifest created / read / mutated; no
manifest field set; docs-level posture only
(`data_read_authorization_recommended = true`,
`builder_implementation_run_recommended = true` — documentation concepts, not
manifest fields). Per Phase 4bn-AB, `source_admissib*` are memo-level governance
concepts appearing in no manifest, transitioning only in the future Phase 4bn-AH
under separate authorization by the Phase 4bn-AB docs-only convention.
`research_eligible=false`, `eligibility_gate_status=pending`,
`chronological_split_policy=not set`, `no_successor_authorization=true` — all
unchanged; Phase 4aw always-raises invariant preserved (never invoked); no
manifest mutation invented.

**Future builder implementation/run scope (Phase 4bn-AH, if separately
authorized):** code + controlled local data read + one local gitignored output
namespace; single run; a new pre-v002-specific data-reading module (not a
wrap/copy/reuse of the v002-terminal loader); imports the Phase 4bn-AF skeleton;
uses the Phase 4bn-AA split artefact; binds the Phase 4bn-AC contract and Phase
4bn-AE amendment. Arc shift: AH builder run → AI descriptive dataset diagnostics
→ AJ fixed baseline run + verdict → AK arc-decision (operator may re-letter).

**Required pre-read checks:** source-scope validation (BTCUSDT /
binance_usdm_futures / aggTrades / 2024-03-01..2024-11-30 / 275 partitions /
400,001,695 rows / no v002 / no sealed / no full-envelope / no private /
authenticated / external; fail closed on missing critical keys); manifest /
config / gate-report hash binding (normalized `0e96ae37…` + gate `3452fd9d…`;
feature `4881eb87…` + `feature_config_hash 0726b41d…` + gate `db731d1b…`; label
`69746c88…` + `label_config_hash b3bd5d2b…` + gate `ffb5b092…`; reject v002
`819cfa7a…` / `352bad41…` by full value and prefix; fail closed on missing/mismatch);
per-Parquet `.sha256` + manifest-inventory verification before reading rows;
275/275 partition discovery; split-authority binding (import
`pre_v002_split_policy.py`; confirm
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`; record module path
+ commit SHA).

**Required pre-write checks:** all pre-read checks; strict feature/label pairing
by UTC date; strict positional alignment over row_index / agg_trade_id /
feature_timestamp_ms / source_transact_time_ms / symbol / utc_date where present;
split assignment by `source_transact_time_ms` UTC date; embargo drop; per-horizon
earlier-split boundary-crossing exclusion; target filtering (null direction; null
log-return where required; censored; invalid-price; never impute; record drops by
split and reason); model-matrix construction from exactly 45 allowed feature
columns; empty forbidden-column scan; train-only transform planning; Phase 4bn-L
budget preflight must pass; leakage/split-integrity proof assembled and validated
before any output committed to disk.

**Budget preflight requirements (Phase 4bn-L, before any write, fail closed on
breach):** derived footprint warn 75 GiB / hard 125 GiB; total derived-stack warn
250 GiB / hard 300 GiB; runtime warn 4 h / hard 8 h; temp warn 50 GiB / hard 100
GiB; `D:` ≥ 500 GiB free before start; fail closed below 350 GiB free during;
result recorded in the proof / run manifest.

**Leakage / split-integrity proof requirements:** machine-checkable JSON proof +
Phase 4bb-F canonical sidecar covering split-policy name / module path / commit
SHA; date-assignment counts 214 / 1 / 45 / 1 / 14; no missing / duplicate /
multi-assigned in-segment dates; no EMBARGO rows used; zero out-of-segment dates;
`v002_terminal_window_read=false`; `sealed_test_split_touched=false`;
`test_rows_loaded=0`; no random / shuffle / k-fold / bootstrap; deterministic
`source_transact_time_ms` UTC-date assignment; per-horizon zero earlier-split
boundary-crossing rows; strict feature/label key-alignment counts; target null /
censored / invalid drops by split and reason; active 45-column feature-list hash;
empty forbidden-column scan; train-only transform provenance; budget-preflight
result; metric registry present; date/month block reporting schema present;
dependence caveat present; calibration schema present; cost descriptive fields
present; success/kill constants present; non-authorization flags all false (ML /
diagnostics / strategy / signals / PnL / backtest / live / exchange-write);
output namespace created exactly once if authorized; no outputs outside the
authorized namespace. Validated by `validate_dataset_builder_proof`.

**Sidecar / metadata policy:** every future output carries a Phase 4bb-F
canonical two-space `.sha256` sidecar; the proof carries its own sidecar; a local
dataset manifest / metadata only if the future spec defines it; all local +
gitignored under `data/research/`; none committed; none imply eligibility; none
set `chronological_split_policy`; none transition `ml_authorized` /
`diagnostics_authorized`.

**Future output namespace posture:** exactly one local gitignored namespace
`data/research/microstructure/ml_datasets/pre_v002_contract_v001/`, created only
in the future Phase 4bn-AH if separately authorized; not created by this phase.

**Forbidden future outputs:** model files; predictions; diagnostics outputs;
research matrices beyond the authorized dataset unless explicitly authorized;
backtest outputs; strategy outputs; PnL reports; v003 dataset; compacted Parquet;
database files; outputs under `data/microstructure/` unless explicitly
authorized; committed data files; outputs outside the single authorized
namespace; split file / research matrix / ML config / source-manifest / gate
report that mutates or replaces existing published artefacts.

**One-time run / rerun posture:** single controlled run; not open-ended or
scheduled; failure requires a failure-closeout / recovery memo before rerun; any
rerun requires separate authorization unless the future spec defines safe
idempotent rerun behaviour; default one run then stop and report.

**Future validation requirements:** targeted offline tests for new data-reading
builder code; synthetic-fixture tests for the new I/O boundary and fail-closed
guards; the existing 97 Phase 4bn-AF skeleton tests; ruff; mypy (new vs
pre-existing sibling errors distinguished); real budget preflight; hash/gate
validation; no-sealed / no-v002 proof; no-output-outside-namespace proof;
`git status`; `git check-ignore -v data/microstructure/`;
`git check-ignore -v data/research/`.

**Current-state consolidation assessment:** non-blocking; strongly recommended
parallel docs-only option; the state doc (large, partially stale) is a
navigational summary, not the binding source of truth for any hash/gate/split/flag
the future builder binds to, so its staleness does not weaken data-read safety.

**Candidate next phases considered:** (1) Phase 4bn-AH data-reading builder
implementation + single run — selected recommendation; (2) current-state
consolidation memo — recommended parallel, not blocker; (3) additional skeleton
hardening — not required; (4) source-admissibility gate artefact — not required;
(5) budget-preflight design memo — not required; (6) full-envelope
reference-assembly memo — only if pre-v002 + v002; (7) holdout-boundary memo —
only if v002 / sealed dates touched; (8) close ML baseline arc — premature.

**Selected next recommendation:** Phase 4bn-AH — data-reading ML dataset builder
implementation + single run, subject to separate operator authorization;
current-state consolidation memo as a recommended parallel option.

**Remaining blockers before future builder run:** this memo (done); a code-level
data-reading builder importing the skeleton and binding the passed gates
(`3452fd9d…` / `db731d1b…` / `ffb5b09…`) / manifests / hashes / split artefact; a
real leakage/split-integrity proof + real Phase 4bn-L budget preflight bound in
and passing; separate operator authorization (`source_admissible_for_data_read` /
`source_admissible_for_dataset_builder` both false).

**Remaining blockers before ML dataset can be used for diagnostics:** all
builder-run blockers; the dataset must exist under a passing proof / preflight;
separate diagnostics authorization (`diagnostics_authorized=false`); a
descriptive-only diagnostics scope with no models / scoring / predictions.

**Remaining blockers before ML training:** all builder-run + diagnostics
blockers; target/horizon/filtering locked (done) and evaluation/dependence/
success-kill layer pre-registered (done) and encoded (done); a committed
end-to-end pre-v002 trainer (does not exist); separate ML authorization
(`ml_authorized=false`).

**Strategy / PnL / backtest hard boundary (absolute):** no dataset, diagnostic,
baseline, or metric authorizes strategy construction, signal generation,
threshold / confidence-gated trading, backtesting, PnL computation, position
sizing, execution logic, live-readiness, paper / shadow trading, or
exchange-write; any such path requires a future M0-style mechanism-admissibility
memo clearing cost realism at 8 bps/side · 16 bps round-trip, execution
feasibility, slippage / spread assumptions, label economic relevance, strategy
admissibility vs the retained rejections and the M0 §7.D microstructure-lane
`NOT_RECOMMENDED_NOW` posture, and the Phase 4al no-rescue constraints.

Final `git status` / `git log` / SHAs are reproduced in the final operator report
so the operator need not run a separate status/SHA check manually.
