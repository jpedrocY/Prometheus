# Phase 4bn-AA — Pre-V002 Split-Policy Artefact + Offline Tests

## 1. Purpose

This phase operationalises the Phase 4bn-Y **Candidate A** chronological split /
holdout policy as a **code-level artefact with offline tests**. It implements the
recorded pre-v002 split contract
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO` as **pure
date / window arithmetic with no data I/O**, so that future ML-dataset tooling has
a single, machine-checkable split-policy module to depend on — exactly the
narrow, low-risk next step recommended by the Phase 4bn-Z ML-baseline readiness
memo (`RECOMMEND_AUTHORIZE_PRE_V002_SPLIT_POLICY_ARTEFACT`).

It is a **code + tests + docs** phase. It builds **no ML dataset, no research
matrix, no manifest, no gate report, no sidecar, no split file**; it reads **no
local data**; it creates **no local data**; it trains / scores / predicts
nothing; it runs no diagnostics, strategy, signals, PnL, or backtests; it sets no
manifest `chronological_split_policy` field; it flips no eligibility; it
transitions no `eligibility_gate_status`; and it authorizes **no successor**.

---

## 2. Authority and repository state

- **Phase:** 4bn-AA — Pre-V002 Split-Policy Artefact + Offline Tests.
- **Authorization:** separately authorized by the operator following the Phase
  4bn-Z decision `RECOMMEND_AUTHORIZE_PRE_V002_SPLIT_POLICY_ARTEFACT`.
- **Active local repo:** `D:\Prometheus`. **Lightweight workspace:**
  `D:\ClaudeRuns\prometheus-light`.
- **Remote:** `origin → https://github.com/jpedrocY/Prometheus.git` (verified).
- **Branch:** `phase-4bn-aa/pre-v002-split-policy-artefact`.
- **Base `main` SHA:** `d9e699ea07d41a8d5492efdab8f6a1f74aae54e2`
  (`docs(phase-4bn-z): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == d9e699ea…` verified.
- **Predecessors present on `main`:** Phase 4bn-Z SHA-finalization `d9e699e`,
  merge-closeout `268020a`, merge `12e50e8`, branch `bce8fb4`; Phase 4bn-Y
  finalization `896f5fa` present as predecessor.
- **Gitignored data namespaces:** `data/microstructure/` (`.gitignore:85`) and
  `data/research/` (`.gitignore:88`) — both confirmed; both remain uncommitted.

This phase is **branch-complete only** by its own work; it is **not merged into
`main`** and is **not project-complete**. It becomes project-complete only when a
separately authorized merge phase records its merge-closeout on `main`.

**Tier:** **Tier 1 — Full Phase** per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3. Although it performs no
data I/O, the module operationalises an admissibility boundary (the split /
holdout / embargo contract that any future ML-baseline work must obey); an error
here could silently corrupt downstream scientific meaning, so it is Tier 1.

---

## 3. Phase type and strict scope

**Phase type:** pure-source split-policy artefact + offline unit tests + docs.

**In scope (this phase):** add one pure split-policy source module; add one
offline unit-test module; write this implementation report; write the closeout;
make a narrow additive `current-project-state.md` update.

**Strictly out of scope / forbidden (this phase does none):** build an ML
dataset; create a research matrix; create a manifest / gate report / sidecar /
split file / ML config; train, score, or predict; run diagnostics, strategy,
signals, PnL, or backtests; read local data; create local data; inspect any file
under `data/microstructure/` or `data/research/`; inspect raw zip / normalized /
feature / label Parquet; inspect any manifest or gate report under `data/`;
inspect any v002-terminal or sealed-test file; mutate any manifest; set
`chronological_split_policy`; flip `research_eligible`; transition
`eligibility_gate_status`; add scripts or data files; or authorize any successor.

---

## 4. Evidence base and input boundary

**Admissible evidence (read-only) used:**

- Committed process standards (`merge-closeout-standard`,
  `phase-risk-tiering-standard`, `phase-workflow-standard`,
  `phase-prompt-template`, `operator-report-standard`) and
  `current-project-state.md`.
- Committed Phase 4bn-O … 4bn-Z implementation reports, merge-closeouts, and
  closeouts (the source of every figure carried forward), in particular the
  Phase 4bn-Y chronological split / holdout policy memo and the Phase 4bn-Z
  ML-baseline readiness memo.
- Committed source, read-only, for implementation precedent:
  `diagnostics_split_policy_v002.py` (the already-recorded v002 split policy),
  `ml_baseline_design_v002.py` (the `NON_AUTHORIZATION_FLAGS` evidence-block
  pattern), and the committed test
  `tests/research/microstructure/test_diagnostics_split_policy_v002.py`.

**Input boundary (not read):** no local Parquet (raw / normalized / feature /
label); no local raw zip; no local manifest or gate report under
`data/microstructure/`; no `data/research/` output; no v002-terminal window; no
sealed-test file. `README` is treated as potentially stale and was **not** used as
a current-state authority. Every quantitative figure below is carried forward
verbatim from committed reports / committed source constants; none was recomputed
from local data.

---

## 5. Phase 4bn-Z readiness conclusion carried forward

Phase 4bn-Z concluded the project is **policy-ready but NOT implementation-ready**
for ML on the conservative pre-v002-only path, with result state
`ML_BASELINE_READINESS_RECORDED__PRE_V002_PATH_READY_FOR_SPLIT_POLICY_ARTEFACT__REMAIN_PAUSED`.
It identified six prerequisites before ML training (split-policy artefact;
source admissibility; ML dataset contract / builder; leakage / split-integrity
proof; budget preflight; per-task target / horizon / filtering decision) and
recommended the **pure-code split-policy artefact** as the next safe step,
because it touches no data and confers no eligibility. **This phase implements
exactly that artefact** and nothing further; the remaining five prerequisites
stay open and unauthorized.

---

## 6. Phase 4bn-Y split policy carried forward

The Phase 4bn-Y memo selected **Candidate A**, working name
`CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`, over the 275 gated
pre-v002 dates (2024-03-01 .. 2024-11-30):

| Split | UTC date range (inclusive) | Dates | Role |
|---|---|---|---|
| **Train** | 2024-03-01 .. 2024-09-30 | 214 | Model + train-only transform fitting |
| Embargo | 2024-10-01 | 1 | Dropped (boundary purge) |
| **Validation** | 2024-10-02 .. 2024-11-15 | 45 | Model selection / tuning |
| Embargo | 2024-11-16 | 1 | Dropped (boundary purge) |
| **Internal holdout (dry-run)** | 2024-11-17 .. 2024-11-30 | 14 | One-time dry-run only; **not** the sealed test |
| **Total** | 2024-03-01 .. 2024-11-30 | **275** | = full gated pre-v002 segment |

Arithmetic: 214 + 1 + 45 + 1 + 14 = **275**. Assignment by
`source_transact_time_ms` UTC date; chronological-only; no shuffle / random /
k-fold-over-time / bootstrap / post-hoc temporal resampling. Embargo: one full
UTC date dropped at each internal boundary (operational rule), over a formal
≥ 60 s row-level earlier-split floor; the 1-day purge (86,400 s) strictly
dominates the 60 s maximum label horizon. The v002 terminal
(2024-12-01 .. 2025-02-28) and the sealed test (2025-02-14 .. 2025-02-28) are
out of scope, by reference only, and unread. **This module encodes Candidate A
exactly and changes nothing about it.**

---

## 7. Existing v002 split-policy precedent

`src/prometheus/research/microstructure/diagnostics_split_policy_v002.py`
(Phase 4bm-W) encodes the **published v002 terminal** policy
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO`: train 2024-12-01 ..
2025-01-14 (45) / validation 2025-01-15 .. 2025-02-13 (30) / test 2025-02-14 ..
2025-02-28 (15); boundaries `1736899200000` / `1739491200000`;
`MIN_BOUNDARY_EMBARGO_SECONDS = 60`; assignment by `source_transact_time_ms` UTC
date; earlier-split-only embargo (`test → None`); `split_for_date()` **raises**
for any date outside the 90-day v002 envelope. The new pre-v002 module is
deliberately modelled on this precedent (same idioms: ISO-date helpers,
`split_for_date` / `split_for_source_transact_time_ms` analogues,
`earlier_split_embargo_window_ms`, `boundary_crossing_window_ms`, a serialisable
policy snapshot), re-bound to the pre-v002 segment and made strictly more
conservative at the boundaries. **`diagnostics_split_policy_v002.py` was not
modified**; the recorded v002 policy is preserved verbatim.

---

## 8. Implemented pre-v002 split-policy artefact

**Module created:**
`src/prometheus/research/microstructure/pre_v002_split_policy.py` (chosen name —
clearly pre-v002, not v002-terminal; consistent with the
`diagnostics_split_policy_v002.py` neighbour). It is pure date / window
arithmetic: its only import is `datetime` (plus `from __future__ import
annotations`). It performs **no file I/O, no network, no RNG**, declares **no
local data-path constants**, and imports **no pandas / pyarrow / polars / numpy**.

The module encodes: the policy name; the segment / train / validation / holdout /
embargo date constants; the two internal boundary timestamps; the ≥ 60 s embargo
floor and 60 s max horizon; the allowed horizons; the v002-terminal / sealed-test
exclusion windows; per-date and per-timestamp split assignment with hard raises
out of segment; the earlier-split embargo and boundary-crossing arithmetic; an
arithmetic self-check; a date inventory; and a serialisable policy contract.

---

## 9. Public API and constants

**Exception:** `PreV002SplitPolicyError(ValueError)`.

**Split labels:** `TRAIN`, `VALIDATION`, `HOLDOUT`, `EMBARGO`;
`MODEL_ELIGIBLE_SPLITS = (TRAIN, VALIDATION, HOLDOUT)`; `ALL_SPLITS`.

**Constants:** `SPLIT_POLICY_NAME`; `PRE_V002_START_DATE` / `PRE_V002_END_DATE`;
`TRAIN_START_DATE` / `TRAIN_END_DATE`; `TRAIN_VALIDATION_EMBARGO_DATE`;
`VALIDATION_START_DATE` / `VALIDATION_END_DATE`;
`VALIDATION_HOLDOUT_EMBARGO_DATE`; `HOLDOUT_START_DATE` / `HOLDOUT_END_DATE`;
`EXPECTED_TRAIN_DATE_COUNT` (214), `EXPECTED_VALIDATION_DATE_COUNT` (45),
`EXPECTED_HOLDOUT_DATE_COUNT` (14), `EXPECTED_EMBARGO_DATE_COUNT` (2),
`EXPECTED_TOTAL_DATE_COUNT` (275); `BOUNDARY_TRAIN_VALIDATION_MS`
(1727827200000 = 2024-10-02T00:00:00Z), `BOUNDARY_VALIDATION_HOLDOUT_MS`
(1731801600000 = 2024-11-17T00:00:00Z); `MIN_BOUNDARY_EMBARGO_SECONDS` /
`MIN_BOUNDARY_EMBARGO_MS` (60 / 60000); `MAX_LABEL_HORIZON_SECONDS` /
`MAX_LABEL_HORIZON_MS` (60 / 60000); `ONE_DAY_PURGE_SECONDS` / `ONE_DAY_PURGE_MS`;
`ALLOWED_HORIZONS_MS` (1000 / 5000 / 15000 / 60000); `UTC_DAY_MS`;
`V002_TERMINAL_START_DATE` / `V002_TERMINAL_END_DATE`; `SEALED_TEST_START_DATE` /
`SEALED_TEST_END_DATE`.

**Functions:** `train_dates()`, `validation_dates()`, `holdout_dates()`,
`embargo_dates()`, `segment_dates()`; `utc_date_start_ms()`,
`utc_date_for_timestamp_ms()`; `split_for_date()`, `split_for_timestamp_ms()`;
`is_train_date()`, `is_validation_date()`, `is_holdout_date()`,
`is_embargo_date()`, `is_model_eligible_split()`; `policy_date_inventory()`;
`validate_horizon_ms()`; `earlier_split_embargo_window_ms()`, `is_embargoed()`,
`is_earlier_split_boundary_crossing()`, `boundary_crossing_window_ms()`;
`validate_policy_arithmetic()`; `build_split_policy_contract()`. A stable
`__all__` lists the public surface.

---

## 10. Date assignment semantics

`split_for_date(date_like)` accepts an ISO date string or a `datetime.date`,
rejects bare `datetime` objects (to avoid timezone ambiguity), and:

- returns `TRAIN` for 2024-03-01 .. 2024-09-30;
- returns `EMBARGO` for 2024-10-01 and 2024-11-16;
- returns `VALIDATION` for 2024-10-02 .. 2024-11-15;
- returns `HOLDOUT` for 2024-11-17 .. 2024-11-30;
- **raises `PreV002SplitPolicyError`** for any date before 2024-03-01 or after
  2024-11-30.

`split_for_timestamp_ms(source_transact_time_ms)` assigns by the **UTC** calendar
date of the epoch-ms timestamp (`datetime.fromtimestamp(..., tz=UTC)`), so the
local machine timezone cannot affect the split. The instant
2024-10-01T23:59:59.999Z resolves to `EMBARGO`; 2024-10-02T00:00:00.000Z (exactly
`BOUNDARY_TRAIN_VALIDATION_MS`) resolves to `VALIDATION`.

---

## 11. Embargo and boundary-crossing semantics

`earlier_split_embargo_window_ms(split)` returns the `[boundary − 60000,
boundary)` earlier-split embargo window for `TRAIN` (at the validation boundary)
and `VALIDATION` (at the holdout boundary), `None` for `HOLDOUT` (the latest
split — never an earlier split, mirroring the v002 `test → None` rule), and
raises for `EMBARGO` / unknown.

`is_earlier_split_boundary_crossing(source_transact_time_ms, horizon_ms, split)`
implements the pure leakage-proof hook. For a row at `T` with horizon `H`:

- `TRAIN`: crossing iff `T + H ≥ BOUNDARY_TRAIN_VALIDATION_MS`
  (2024-10-02T00:00:00Z);
- `VALIDATION`: crossing iff `T + H ≥ BOUNDARY_VALIDATION_HOLDOUT_MS`
  (2024-11-17T00:00:00Z);
- `HOLDOUT`: always `False` (no later pre-v002 split; envelope-terminal label
  censoring is a label concern outside this artefact);
- `EMBARGO`: **raises** (embargo rows are dropped; crossing is undefined);
- out-of-segment `T`: **raises**;
- `horizon_ms ∉ {1000, 5000, 15000, 60000}`: **raises**.

Because the policy drops the full UTC date before each boundary, **no real
earlier-split row can cross**: the latest train instant 2024-09-30T23:59:59.999Z
plus the 60 s max horizon lands on 2024-10-01 (the embargo date), well short of
the 2024-10-02 boundary — the 1-day purge dominates the 60 s floor with margin.
The helper exists so future tooling has a machine-checkable proof even below day
granularity. `is_model_eligible_split()` reports `EMBARGO → False` so dropped
rows are explicitly non-eligible.

---

## 12. v002 terminal and sealed-test exclusion

Every v002-terminal date (2024-12-01 .. 2025-02-28) and every sealed-test date
(2025-02-14 .. 2025-02-28) lies outside the pre-v002 segment, so `split_for_date`
and `split_for_timestamp_ms` **raise** on all of them (verified by tests over the
full v002-terminal and sealed-test ranges). The module assigns those dates to no
split and reads nothing about them; their windows appear in the contract only as
recorded **exclusions** (`v002_terminal_window_read = False`,
`sealed_test_split_touched = False`, `test_rows_loaded = 0`). The internal
holdout is recorded as `holdout_is_sealed_test = False` /
`holdout_role = "internal_dry_run_only"`.

---

## 13. No-data-I/O design

The module opens no file, touches no path, and imports nothing capable of I/O
(`datetime` only). It declares no `data/microstructure` or `data/research` path
string. `build_split_policy_contract()` returns an in-memory dict (records
`no_data_io = True`) and writes nothing. An offline test reads the module's own
source text and asserts the absence of `import random` / `random` / `numpy` /
`socket` / `urllib` / `requests` / `http` / `pandas` / `pyarrow` / `polars`,
`open(`, `Path(`, and any `data/microstructure` / `data/research` path token — so
the no-I/O, no-RNG, no-data-path posture is itself test-enforced.

---

## 14. Offline test coverage

`tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py` (70
tests, all offline / synthetic) covers the 40 required checks and a few extras:
exact policy name; all date constants and counts (214 / 45 / 14 / 2 / 275); the
214 + 1 + 45 + 1 + 14 = 275 arithmetic and `validate_policy_arithmetic()`; the
eight `split_for_date` boundary cases (5–12); out-of-segment raises incl. the
**entire** v002-terminal and sealed-test ranges (13–17); UTC-date timestamp
assignment at the 2024-10-01T23:59:59.999Z / 2024-10-02T00:00:00.000Z boundary
(18); timezone-independence via `TZ` perturbation + `time.tzset()` (19); exact
boundary-timestamp constants (20); horizon acceptance / rejection incl. bool
(21–22); boundary-crossing catches for train→validation and validation→holdout
(23–24); interior-row and full-date-purge non-crossing (25–26); holdout
no-next-split + embargo/out-of-segment raises (27); embargo rows not
model-eligible (28); inventory no-duplicate / no-missing / disjoint splits /
non-assignable embargo (29–32); source-token hygiene for RNG / network / heavy
data deps / data paths (33–36); contract non-authorization flags, counts /
embargo settings, pre-v002-only source scope, and JSON-serialisability (37–39);
stable `__all__` exports (40); plus embargo-window and per-horizon
boundary-window arithmetic.

---

## 15. Validation

- `ruff check` on the new module + test → **All checks passed**.
- `pytest tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`
  → **70 passed**.
- `mypy src/prometheus/research/microstructure/pre_v002_split_policy.py` → the new
  module reports **0 errors**. mypy surfaced 29 **pre-existing, unrelated** errors
  in sibling committed modules (`labels_compute.py`, `features_compute.py`,
  `features_compute_v002.py`, `labels_manifest_v002.py`,
  `multiday_feature_gate_checks.py`) reached transitively through the package;
  checking `labels_compute.py` alone reproduces the same 29, confirming they
  pre-date and are independent of this phase. **The new module introduced no
  mypy error.**
- `git diff --check` → clean.
- `git status --short` → only the new module, the new test, the three additive
  docs, and the pre-existing untracked `.claude/scheduled_tasks.lock`.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`;
  `git check-ignore -v data/research/` → `.gitignore:88`.

---

## 16. Future use boundary

The module is a **pure split contract**. A future, separately-authorized ML
dataset builder may import it to assign rows by `source_transact_time_ms` UTC
date, drop embargo dates, and emit the leakage / split-integrity proof
(`is_earlier_split_boundary_crossing` per horizon; `policy_date_inventory` for
assignment completeness; `build_split_policy_contract` for the recorded
non-authorization evidence). It must still re-bind to the pre-v002
family / hashes / partition count and resolve source admissibility **before**
reading any data; this artefact neither reads data nor confers eligibility.

---

## 17. Remaining blockers before ML dataset creation

Unchanged from Phase 4bn-Z §20, minus the now-satisfied split-policy artefact:
(1) **source admissibility** resolved (segment remains `research_eligible=false` /
`eligibility_gate_status=pending`); (2) an **ML dataset contract / builder** with
its **leakage / split-integrity proof**; (3) a **budget preflight** within the
Phase 4bn-L caps; (4) a **per-task target / horizon / filtering decision**. A
committed end-to-end trainer still does not exist and would be a later,
separately-authorized phase even after (1)–(4). The recommended next blocker is
**source admissibility** (see §21).

---

## 18. Explicit non-authorizations

Phase 4bn-AA did **NOT**, and does **NOT**, authorize: building an ML dataset;
creating a research matrix; creating any manifest / gate report / sidecar / split
file / ML config; training / scoring / predicting; running diagnostics, strategy,
signals, PnL, or backtests; reading or creating any local data; inspecting any
file under `data/microstructure/` or `data/research/`; inspecting raw zip /
normalized / feature / label Parquet; inspecting any manifest or gate report
under `data/`; inspecting any v002-terminal or sealed-test file; mutating any
manifest; setting `chronological_split_policy`; flipping `research_eligible`;
transitioning `eligibility_gate_status` / `diagnostics_authorized` /
`ml_authorized`; acquisition / endpoint calls / archive download / HEAD
preflight; storage migration / database / Parquet compaction / v003; committing
`data/microstructure` or `data/research`; adding scripts or data files; or
authorizing any successor. The Phase 4aw `flip_research_eligible(...)`
always-raises invariant is preserved and never invoked. The recorded v002
`CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` policy and the Phase 4bn-Y
Candidate A policy are preserved verbatim. **Every retained verdict and project
lock is preserved verbatim** (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1; §11.6 = 8 bps per side / round-trip 16 bps; §1.7.3;
Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11;
Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al refined
no-rescue; Phase 4aw always-raises invariant; Phase 4bb-F canonical path policy;
Phase 4bl-F risk tiers; Phase 4bm-U/4bm-W v002 split policy; Phase 4bn-L budgets;
Phase 4bn-N / 4bn-R / 4bn-V manifest/versioning; Phase 4bn-Y chronological split
policy; Phase 4am .. Phase 4bn-Z results — all preserved verbatim).

---

## 19. Result state

`PRE_V002_SPLIT_POLICY_ARTEFACT_IMPLEMENTED__NO_DATA_IO__REMAIN_PAUSED`.

The artefact and its offline tests are implemented and pass; no data was read or
created; no eligibility / manifest state changed; no successor authorized.

---

## 20. Decision

`RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.

Rationale: with the split policy now operationalised in code, the next blocker
before **any** data use is **source admissibility** — the pre-v002 segment is
`research_eligible=false` / `eligibility_gate_status=pending` at every layer, and
no ML dataset builder may read data until that is explicitly resolved. Dataset
contract / builder work should remain blocked until admissibility is resolved,
unless a later operator deliberately chooses a different sequence.

---

## 21. Recommended state and successor options

**Recommended state: remain paused.** No next phase is authorized from inside
Phase 4bn-AA. Successor options (each requiring **separate** operator
authorization after this branch is merged):

- request a merge prompt for Phase 4bn-AA;
- authorize a docs-only **source-admissibility memo** (recommended);
- authorize a docs-only **ML dataset contract memo**;
- authorize a docs-only **ML dataset builder readiness memo**;
- authorize a docs-only **full-envelope reference / assembly memo** (only if a
  future path combines pre-v002 + v002 data);
- authorize a docs-only **holdout-boundary memo** (only if a future scope touches
  the v002 terminal or sealed-test dates);
- authorize a **source-policy documentation memo**;
- authorize a **process-doc `D:` path-string update**;
- **reject** further ML-baseline successors and close the ML arc;
- remain paused.

No ML / diagnostics / strategy / PnL / backtest / storage-migration / paper /
shadow / live / exchange-write option is valid from this state unless separately
authorized after this branch is merged.

---

## 22. Current-project-state update summary

`docs/00-meta/current-project-state.md` is amended **additively only**: one new
Phase 4bn-AA paragraph (after the Phase 4bn-Z paragraph) recording the phase
type, tier, branch, base SHA, the implemented module / test paths, the encoded
Candidate A split, the embargo and boundary semantics, the no-data-I/O posture,
the validation results, the result state
`PRE_V002_SPLIT_POLICY_ARTEFACT_IMPLEMENTED__NO_DATA_IO__REMAIN_PAUSED`, the
decision
`RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`,
and the full non-authorization list; plus one new `Current phase:` block prepended
above the Phase 4bn-Z block. All prior Phase 4bn-A … 4bn-Z paragraphs and blocks,
every retained verdict, and every project lock are preserved verbatim. No table
value, manifest field, or eligibility flag is mutated.
