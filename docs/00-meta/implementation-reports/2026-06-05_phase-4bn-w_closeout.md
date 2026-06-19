# Phase 4bn-W — Branch Closeout

## Branch and base

- **Branch:** `phase-4bn-w/label-only-pre-v002-segment`.
- **Base `main` SHA:** `e53652a11e8586d26803aebb616a87fccd571353`
  (`docs(phase-4bn-v): finalize merge closeout shas`); pre-branch
  `HEAD == main == origin/main` verified in sync.
- **Commit SHA:** recorded in the final operator report after the single
  Phase 4bn-W commit (`data(phase-4bn-w): compute pre-v002 label segment`).
- **Branch-complete only.** Not merged into `main`; not project-complete.
  No merge-closeout created. Not pushed.

## Phase type

Code + tests + docs + local gitignored label artefact generation. Tier 1 —
Full Phase per `phase-risk-tiering-standard` §3.

## Files created (tracked)

- `scripts/phase4bn_w_compute_pre_v002_labels.py` — bounded label-only
  execution wrapper.
- `tests/research/microstructure/test_phase4bn_w_label_pre_v002.py` — 36
  offline tests.
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-w_label-only-pre-v002-segment.md`
  — implementation report (26 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-w_closeout.md` —
  this closeout.

## Files modified (tracked)

- `docs/00-meta/current-project-state.md` — narrow update: new Phase 4bn-W
  paragraph + new `Current phase:` block ahead of the Phase 4bn-V block;
  prior paragraphs/blocks preserved verbatim.

## Code / tooling / tests added

- **Code/tooling added:** one new bounded `scripts/` wrapper (no
  `src/prometheus` module created or modified).
- **Tests added:** one new offline test module (36 tests).
- **`src/prometheus` modified:** **no** — the locked v002 label primitives
  were reused unchanged; the segment-scoped path helper, config-hash
  builder, lineage re-mapping, and manifest builder live in the phase
  wrapper script.

## Local data read

Approved inputs only (read-only, SHA-verified): Phase 4bn-S feature segment
manifest + sidecar (`4881eb87…` / `f2ca2f48…`); 275 feature Parquet (four
anchor columns) + per-day SHA; Phase 4bn-T feature-layer gate report
(`db731d1b…`); Phase 4bn-O normalized segment manifest + sidecar
(`0e96ae37…` / `5d7dcbef…`); 275 normalized Parquet (price + anchor
columns) + per-day SHA; Phase 4bn-P normalized-layer gate report
(`3452fd9d…`). No published `__v002` content; no v002 terminal window; no
sealed-test date; no `data/research` artefact.

## Local data created

275 label Parquet + 275 sidecars + 1 label segment manifest + 1 sidecar
under the gitignored segment directory / manifests root — all non-eligible
and **uncommitted**.

## Output summary

- **Label output directory:**
  `data/microstructure/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w/BTCUSDT/<YYYY>/<MM>/`.
- **Label manifest path:**
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`.
- **Label manifest SHA256:**
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`.
- **Label manifest sidecar SHA256:**
  `636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239`.
- **Label Parquet count:** 275. **Label sidecar count:** 275.
- **Total label rows:** 400,001,695 (== source rows).
- **Total label footprint:** 15,654,082,679 bytes (≈14.58 GiB).
- **`label_config_hash`:**
  `b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`.
- **`envelope_terminal_unix_ms`:** `1733011199331`;
  **`envelope_terminal_utc_date`:** 2024-11-30.
- **Per-horizon censored counts:** 1s = 3, 5s = 20, 15s = 42, 60s = 216
  (total 281 — the last ≤60 s of 2024-11-30).
- **Invalid-price row count:** 0.
- **Runtime:** 4,217.80 s (≈1.17 h) — below the 4 h warn / 8 h hard cap.
- **`D:` free before / min-observed / after:** 1,278,562,484,224 B
  (≈1190.7 GiB) / 1,262,907,052,032 B (≈1176.2 GiB) /
  1,262,907,052,032 B (≈1176.2 GiB).
- **Budget warning thresholds crossed:** none.
- **Hard caps crossed:** none.

## Validation commands run

- `ruff check` (wrapper + test) → All checks passed.
- `pytest test_phase4bn_w_label_pre_v002.py` (+ predecessor regression
  suites) → **155 passed** (36 new + 119 predecessor), 0 failed.
- `mypy src/prometheus` → not run (no `src/prometheus` change; wrapper lives
  under `scripts/`, outside repo-standard mypy scope).
- `git diff --check` → clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85` (label
  Parquet + manifest both resolve to `.gitignore:85`);
  `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → 5 tracked files + expected untracked
  `.claude/scheduled_tasks.lock`; no `data/` artefact staged/committed.

## Result / decision

- **Result state:**
  `LABEL_EXECUTION_SUCCEEDED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_LABEL_LAYER_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused. No successor authorized from inside
  Phase 4bn-W.

## Explicit non-actions

No label-layer gate run; no v002 terminal raw/normalized/feature/label read;
no sealed-test read; no published label `__v002` mutation; no ML training /
model scoring / predictions / diagnostics / strategy / signal / PnL /
backtests; no acquisition / endpoint / archive / HEAD preflight; no feature
/ feature-gate / normalization / normalized-gate / raw rerun; no storage
migration; no database; no Parquet compaction; no v003; no manifest
eligibility transition; no `data/research` artefact; no `data/microstructure`
or `data/research` commit; no paper / shadow / live / exchange-write /
credentials / MCP / Graphify work. `.claude/scheduled_tasks.lock` remained
untracked. Phase 4aw `flip_research_eligible(...)` always-raises invariant
preserved (never invoked).

## Final git state

Final `git status --short`, `git log --oneline -8 --decorate`, and
`git rev-parse HEAD` / `main` / `origin/main` are reported in the final
operator report. `main` and `origin/main` remain at
`e53652a11e8586d26803aebb616a87fccd571353`; the Phase 4bn-W commit exists
only on the `phase-4bn-w/label-only-pre-v002-segment` branch (not pushed).
