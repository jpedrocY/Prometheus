# Phase 4bn-J-R2 — Closeout

**Phase 4bn-J-R2 is branch-complete only by this work; not merged into
main; not project-complete.** Phase 4bn-J-R2 is an acquisition-only /
raw-only / local gitignored data-artefact generation / integrity-bound
**Tier 1 Full Phase** (per
`docs/00-meta/process/phase-risk-tiering-standard.md` §3) that executed
the revised acquisition-only retry recommended by Phase 4bn-J-R1: it
acquired the 275 new pre-v002 raw BTCUSDT Binance USDⓈ-M futures
aggTrades daily archives (2024-03-01 .. 2024-11-30 inclusive UTC),
preserving the existing v002 terminal window and the sealed v002 test
split untouched, and authorizing nothing downstream.

**Phase 4bn-J-R2 does not normalize data, derive features, derive
labels, run ML, train or score models, generate predictions, run
diagnostics, run strategy / signals / PnL / backtests, migrate storage,
create a database, compact Parquet, create v003, mutate any existing
manifest / sidecar / gate report / successor-state artefact, read or
touch the sealed v002 test split, transition any manifest eligibility,
use credentials / `.env` / `.mcp.json` / MCP / Graphify, or authorize any
successor phase. Recommended state remains paused.**

## Branch and base

- **Branch:** `phase-4bn-j-r2/revised-acquisition-only-btcusdt-aggtrades-raw`.
- **Base `main` SHA:** `03dc876cab9ecd3db982beb0ba51712858cbdf9c`
  (`docs(phase-4bn-j-r1): finalize merge closeout shas`; pre-branch
  `main == origin/main == HEAD` verified in sync; Phase 4bn-J-R1
  merge-closeout `bbe8b46`, merge `f63ded8`, branch `3f792a6` present on
  `main`).
- **Active local repo path:** `D:\Prometheus`.
- **GitHub remote:** `origin` →
  `https://github.com/jpedrocY/Prometheus.git`, verified intact.
- The stopped Phase 4bn-J branch
  `phase-4bn-j/acquisition-only-btcusdt-aggtrades-12m` was not merged,
  resumed, deleted, or treated as branch-complete.

## Tracked changes

- `scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py`
  (added; new bounded raw-only 275-day acquisition script; reuses the
  proven Phase 4bl-C patterns; adds segment date guard, symbol/family
  guards, scope-token denylist, amended raw-only disk cap + runtime cap,
  HEAD-only preflight, and a phase-scoped segment manifest writer).
- `tests/research/microstructure/test_phase4bn_j_r2_acquisition_script.py`
  (added; offline tests; no network, no local data, no sealed-test read).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r2_revised-acquisition-only-btcusdt-aggtrades-raw.md`
  (added; the implementation report; 21 sections).
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r2_closeout.md`
  (added; this closeout).
- `docs/00-meta/current-project-state.md`
  (narrow update: new Phase 4bn-J-R2 prose paragraph + new
  `Current phase:` block; prior Phase 4bn-A … 4bn-J-R1 paragraphs and
  blocks preserved as labelled historical context).

No locked prior-phase script, source module, existing test, config,
`.gitignore`, `pyproject.toml`, `README.md`, MCP file, manifest, sidecar,
gate report, or successor-state artefact was modified.

## Local gitignored outputs (NOT committed)

- **275 / 275** raw BTCUSDT aggTrades daily zip archives for
  2024-03-01 .. 2024-11-30 under
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/{YYYY}/{MM}/`,
  each with a paired canonical `.sha256` sidecar (275 zips, 275 sidecars).
- One segment manifest + one acquisition log (each with a `.sha256`
  sidecar) under `data/microstructure/manifests/`
  (`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2*`):
  manifest sha256
  `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`;
  log sha256
  `0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`.
- Total raw footprint: **4.788 GiB** (5,140,686,147 bytes; 400,001,695
  rows). Runtime: **2,051 s (≈34 min)** — no warning threshold crossed,
  no hard cap crossed.
- All outputs are gitignored under `data/microstructure/` and remain
  **uncommitted**. The expected untracked transient
  `.claude/scheduled_tasks.lock` was present and not committed. No
  `data/research/` artefact was created.

## Result and decision

- **Result state:
  `ACQUISITION_SUCCEEDED__RAW_ARTEFACTS_LOCAL_GITIGNORED__REMAIN_PAUSED`.**
- **Decision:
  `RECOMMEND_AUTHORIZE_RAW_ARCHIVE_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.**

Decision rationale: acquisition ran within the amended raw-only contract;
the source-policy preflight passed; the HEAD-only disk preflight measured
~4.79 GiB (below the 10 GiB warning and 25 GiB hard caps); no hard cap
was crossed. If acquisition succeeded and raw artefacts / manifest /
sidecars were created, the recommendation is a future raw archive
eligibility gate only, subject to separate operator authorization. No ML,
diagnostics, model training, strategy, PnL, backtest, storage migration,
database creation, Parquet compaction, v003, or paper / shadow / live is
recommended or authorized. No successor is authorized from inside Phase
4bn-J-R2.

## Validation summary

- `ruff check` on the new script + new test module: pass.
- `pytest` new offline test module: 117 passed.
- Existing `test_phase4bl_c_acquisition_script.py`: passing (no
  regression).
- `mypy` gate scoped to `src/prometheus`; the new `scripts/` file is
  outside the gate, at parity with the locked Phase 4bl-C script.
- `git diff --check`: clean.
- `git check-ignore -v data/microstructure/` and
  `git check-ignore -v data/research/`: both ignored.
- No `data/microstructure/` or `data/research/` artefact staged.
- Every generated raw archive has a canonical sidecar; sidecar format is
  canonical `<sha256>␠␠<basename>\n`; the segment manifest validates as
  sorted-key JSON with a trailing newline and the required non-eligible
  seed (`research_eligible=false`, `eligibility_gate_status="pending"`,
  `test_holdout_touched=false`, `test_rows_loaded=0`).
- No sealed test-holdout file opened; no credentials / private endpoints
  used; no `.duckdb` / `.sqlite` created; no normalized / feature / label
  artefact created.

## Recommended state

**Remain paused.** Phase 4bn-J-R2 is branch-complete only by this work;
not merged into main; not project-complete until a separately authorized
merge phase records its merge-closeout on `main` per
`merge-closeout-standard.md` (Tier 1). **No next phase authorized.** The
operator may equivalently: remain paused (default); request a merge
prompt for Phase 4bn-J-R2; separately authorize a raw archive eligibility
gate (the recommendation, if acquisition succeeded); separately authorize
a docs-only source-policy documentation memo; separately authorize a
docs-only derived-stack storage-budget memo before any normalization /
features / labels; or reject further ML-baseline successors and close the
ML arc.

## Preserved governance

Every retained verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m
thread / V2 / G1 / C1) and every project lock (§11.6 = 8 bps per side;
§1.7.3; Phase 3p §4.7; Phase 3r §8; Phase 4j §11; Phase 4k; Phase 4p;
Phase 4q; Phase 4ak M0; Phase 4aw `flip_research_eligible(...)`
always-raises invariant (never invoked); Phase 4bb-F canonical path +
sidecar policy; Phase 4bl-F four-tier risk model; the Phase 4bn-J-R1
raw-only cap amendment) is preserved verbatim. Phase 4 canonical remains
unauthorized. The Phase 4bn-J-R2 merge phase / any raw archive
eligibility gate / any source-policy documentation memo / any
derived-stack storage-budget memo / any normalization / feature / label /
ML / diagnostics / strategy / signals / PnL / backtest / storage-migration
/ database-creation / Parquet-compaction / v003-creation / paper / shadow
/ live-readiness / deployment / exchange-write / production-key / any
Phase 5 / any successor phase remains unauthorized.
