# Phase 4bn-AA — Closeout

## 1. Phase identity

- **Phase:** 4bn-AA — Pre-V002 Split-Policy Artefact + Offline Tests.
- **Phase type:** pure-source split-policy artefact + offline unit tests + docs.
- **Tier:** Tier 1 — Full Phase per
  `docs/00-meta/process/phase-risk-tiering-standard.md` §3.
- **Branch-complete only:** not merged into `main`; not project-complete.
  Becomes project-complete only when a separately authorized merge phase records
  its merge-closeout on `main`.

---

## 2. SHAs

- **Branch:** `phase-4bn-aa/pre-v002-split-policy-artefact`.
- **Base `main` SHA:** `d9e699ea07d41a8d5492efdab8f6a1f74aae54e2`
  (`docs(phase-4bn-z): finalize merge closeout shas`).
- **Pre-branch sync:** `HEAD == main == origin/main == d9e699ea…` verified.
- **Predecessors present on `main`:** Phase 4bn-Z `d9e699e` / `268020a` /
  `12e50e8` / `bce8fb4`; Phase 4bn-Y `896f5fa`.
- **Branch commit SHA:** recorded in the final operator report (this closeout is
  committed in the same single commit
  `code(phase-4bn-aa): add pre-v002 split policy artefact`).

---

## 3. Files created / modified

**Created (4):**

- `src/prometheus/research/microstructure/pre_v002_split_policy.py` — the pure
  pre-v002 split-policy source module (no data I/O).
- `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py` — the
  offline unit-test module (70 tests).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-aa_pre-v002-split-policy-artefact.md`
  (22 sections).
- `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-aa_closeout.md` (this
  file).

**Modified narrowly (1):**

- `docs/00-meta/current-project-state.md` — additive only: one new Phase 4bn-AA
  paragraph + one new `Current phase:` block; all prior content preserved
  verbatim.

**No** scripts, config, manifests, gate reports, sidecars, split files, research
matrices, ML configs, or data files were created or modified. No existing source
or test was modified (`diagnostics_split_policy_v002.py` preserved verbatim).

---

## 4. Code / tooling added

- **Module path:** `src/prometheus/research/microstructure/pre_v002_split_policy.py`.
- Pure date / window arithmetic; only import is `datetime`. No file I/O, no
  network, no RNG, no pandas / pyarrow / polars / numpy, no local data-path
  constants.
- **Public surface (via `__all__`):** `PreV002SplitPolicyError`; split labels
  `TRAIN` / `VALIDATION` / `HOLDOUT` / `EMBARGO`; the policy / date / boundary /
  embargo / horizon constants; `split_for_date()`, `split_for_timestamp_ms()`,
  the `is_*_date()` predicates, `is_model_eligible_split()`,
  `policy_date_inventory()`, `validate_horizon_ms()`,
  `earlier_split_embargo_window_ms()`, `is_embargoed()`,
  `is_earlier_split_boundary_crossing()`, `boundary_crossing_window_ms()`,
  `validate_policy_arithmetic()`, `build_split_policy_contract()`.

---

## 5. Tests added

- **Test path:** `tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`.
- **70 offline / synthetic tests**, covering the 40 required checks plus extras
  (see report §14). No production data, no `data/microstructure`, no
  `data/research`, no Parquet, no network, no RNG, no machine-timezone
  dependence, no file writes.

---

## 6. Validation commands run

- `ruff check src/prometheus/research/microstructure/pre_v002_split_policy.py tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py`
  → **All checks passed** (after fixing 3 `SIM300` yoda-condition lints).
- `python -m pytest tests/research/microstructure/test_phase4bn_aa_pre_v002_split_policy.py -q`
  → **70 passed**.
- `python -m mypy src/prometheus/research/microstructure/pre_v002_split_policy.py`
  → **0 errors in the new module**; 29 pre-existing, unrelated errors surfaced
  transitively from sibling committed modules (`labels_compute.py`,
  `features_compute.py`, `features_compute_v002.py`, `labels_manifest_v002.py`,
  `multiday_feature_gate_checks.py`). Checking `labels_compute.py` alone
  reproduces the same 29, confirming they pre-date this phase. The new module
  introduced none.
- `git diff --check` → clean.
- `git status --short`, `git check-ignore -v data/microstructure/`
  (`.gitignore:85`), `git check-ignore -v data/research/` (`.gitignore:88`).

Exact command outputs are reproduced in the final operator report.

---

## 7. Encoded policy

- **Policy name:** `CHRONO_SPLIT_PRE_V002_214D_45D_14D_WITH_1D_BOUNDARY_EMBARGO`.
- **Selected split (Phase 4bn-Y Candidate A, exact):**
  - **Train:** 2024-03-01 .. 2024-09-30 — **214** dates.
  - **Embargo:** 2024-10-01 (dropped).
  - **Validation:** 2024-10-02 .. 2024-11-15 — **45** dates.
  - **Embargo:** 2024-11-16 (dropped).
  - **Internal holdout / dry-run (NOT sealed test):** 2024-11-17 .. 2024-11-30 —
    **14** dates.
  - **Total:** 214 + 1 + 45 + 1 + 14 = **275** = full gated pre-v002 segment.
- **Date counts:** train 214 / validation 45 / holdout 14 / embargo 2 /
  total 275.
- **Embargo dates:** 2024-10-01 and 2024-11-16 (each one full UTC date; over a
  formal ≥ 60 s row-level earlier-split floor; 1-day purge dominates the 60 s max
  horizon).

---

## 8. Boundary timestamp handling

- `BOUNDARY_TRAIN_VALIDATION_MS = 1727827200000` = 2024-10-02T00:00:00Z
  (validation start).
- `BOUNDARY_VALIDATION_HOLDOUT_MS = 1731801600000` = 2024-11-17T00:00:00Z
  (holdout start).
- Assignment is by **UTC** date of `source_transact_time_ms`; the local timezone
  cannot affect it (verified by `TZ`-perturbation tests). 2024-10-01T23:59:59.999Z
  → `EMBARGO`; 2024-10-02T00:00:00.000Z → `VALIDATION`.
- Boundary-crossing helper: `TRAIN` crosses iff `T + H ≥` the validation
  boundary; `VALIDATION` crosses iff `T + H ≥` the holdout boundary; `HOLDOUT`
  never crosses (no later pre-v002 split); `EMBARGO` and out-of-segment `T` raise;
  invalid horizon raises.

---

## 9. Boundary / data confirmations

- **No-data-I/O confirmation:** the module performs no file I/O, opens no path,
  and imports nothing capable of I/O (`datetime` only); a test asserts the source
  contains no RNG / network / pandas / pyarrow / polars / `open(` / `Path(` /
  `data/microstructure` / `data/research` token.
- **No local data read** (no raw zip, normalized / feature / label Parquet,
  manifest, gate report, sidecar, v002-terminal window, or sealed-test file).
- **No local data created** (no `data/microstructure` or `data/research` output).
- **No ML / dataset / research matrix / training / scoring / prediction /
  diagnostics / strategy / signals / PnL / backtests.**

---

## 10. Result / decision

- **Result state:**
  `PRE_V002_SPLIT_POLICY_ARTEFACT_IMPLEMENTED__NO_DATA_IO__REMAIN_PAUSED`.
- **Decision:**
  `RECOMMEND_AUTHORIZE_SOURCE_ADMISSIBILITY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
- **Recommended state:** remain paused.
- **ARTEFACT IMPLEMENTED; NO DATA I/O.**

---

## 11. Boundary confirmations (non-authorizations)

- No acquisition, endpoint call, archive download, or HEAD preflight.
- No raw / normalization / feature / label execution or any layer gate re-run.
- No local raw zip, normalized / feature / label Parquet, manifest, gate report,
  or sidecar read or inspected.
- No v002-terminal window read; no sealed-test read or touch
  (`test_rows_loaded = 0`).
- No storage migration; no database; no Parquet compaction; no v003.
- No manifest mutation; no `chronological_split_policy` set; no
  `research_eligible` flip; no `eligibility_gate_status` transition.
- No `data/research` or `data/microstructure` artefact created or committed.
- No scripts or data files added; no existing source/test modified.
- No successor authorized.
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked).
- Recorded v002 `CHRONO_SPLIT_45D_30D_15D_WITH_60S_BOUNDARY_EMBARGO` and Phase
  4bn-Y Candidate A policy preserved verbatim.

---

## 12. Successor authorization

**None.** Not authorized by this phase: any merge phase; a source-admissibility
memo / gate; an ML dataset contract memo; an ML dataset builder readiness memo;
an ML dataset builder; a research matrix; any model / scoring / prediction; any
diagnostics; any strategy / signals / PnL / backtest; a full-envelope reference /
assembly memo; a holdout-boundary memo; a source-policy documentation memo; a
process-doc path update; any acquisition; any paper / shadow / live /
exchange-write / production-key; any Phase 5; any other successor.

---

## 13. Recommended state

**Remain paused.** No next phase authorized.

---

## 14. Final git state

Reproduced in the final operator report (`git status --short`,
`git log --oneline -8 --decorate`, `git rev-parse HEAD`, `git rev-parse main`,
`git rev-parse origin/main`) so the operator need not run a separate status / SHA
check manually.
