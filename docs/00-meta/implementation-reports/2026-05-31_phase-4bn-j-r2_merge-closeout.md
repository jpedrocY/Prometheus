# Phase 4bn-J-R2 — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-J-R2 — Revised Acquisition-Only BTCUSDT aggTrades
  Raw Retry.
- **Type:** Acquisition-only / raw-only / local gitignored data-artefact
  generation / integrity-bound execution phase. **Tier 1 — Full Phase**
  (per `docs/00-meta/process/phase-risk-tiering-standard.md` §3).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-J-R2 branch (new bounded
  raw-only 275-day acquisition script + 117 offline tests + the
  implementation report + closeout + the narrow `current-project-state.md`
  update) into `main` and record the canonical merge-closeout that makes
  Phase 4bn-J-R2 project-complete. The acquisition's local gitignored raw
  artefacts (275 zips + sidecars + segment manifest + log) are **not**
  committed and accompany the merge as local data only.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-j-r2/revised-acquisition-only-btcusdt-aggtrades-raw`.

## 2. SHAs

- **`main` SHA before merge:** `03dc876cab9ecd3db982beb0ba51712858cbdf9c`
  (`docs(phase-4bn-j-r1): finalize merge closeout shas`).
- **Branch commit SHA (docs + code):**
  `e714150da36b7fe914d6b9e05caa95d502bebfc9`
  (`data(phase-4bn-j-r2): add bounded raw aggtrades acquisition retry`).
- **Merge commit SHA:** `c80ab68855f0e57fea3cee8b7a7933fac8ea4333`
  (`data(phase-4bn-j-r2): merge revised raw aggtrades acquisition`).
- **Merge-closeout commit SHA:** `26afba74531603b348128c1cee8244b58793614e`
  (`docs(phase-4bn-j-r2): add merge closeout`), recorded by this
  subsequent SHA-finalization commit. Per the repo convention used for
  Phase 4bn-J-R1 / 4bn-I / 4bn-H / 4bn-G / 4bn-F / 4bn-E / 4bn-D / 4bn-C /
  4bn-B / 4bn-A, the merge-closeout commit cannot self-reference its own
  hash inside its own diff; the SHA is filled in by this SHA-finalization
  commit, which can reference the merge-closeout commit hash because that
  hash exists in `git log` before the SHA-finalization commit is created.
- **SHA-finalization commit:** recorded in the final operator report and
  `git log` as `docs(phase-4bn-j-r2): finalize merge closeout shas`. Same
  convention: the SHA-finalization commit cannot self-reference its own
  hash inside its own diff; its SHA is captured in the final operator
  report and `git log`.
- **Final `main` / `origin/main` SHA after push:** after the
  SHA-finalization commit and push, final `main` SHA == final
  `origin/main` SHA == the SHA-finalization commit (recorded in the final
  operator report and `git log`).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message:
  `data(phase-4bn-j-r2): merge revised raw aggtrades acquisition`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No
  force-push.
- Push status: **Pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing** (recorded at SHA-finalization).

## 4. Files brought forward by the merge

**Docs (3):**
- `docs/00-meta/current-project-state.md` (modified; narrow Phase
  4bn-J-R2 paragraph + new `Current phase:` block; prior Phase 4bn-A …
  4bn-J-R1 paragraphs and blocks preserved as labelled historical
  context);
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r2_revised-acquisition-only-btcusdt-aggtrades-raw.md`
  (added; implementation report; 21 sections);
- `docs/00-meta/implementation-reports/2026-05-31_phase-4bn-j-r2_closeout.md`
  (added; branch closeout).

**Scripts (1):**
- `scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py` (added;
  new bounded raw-only 275-day acquisition script).

**Tests (1):**
- `tests/research/microstructure/test_phase4bn_j_r2_acquisition_script.py`
  (added; 117 offline tests).

**Source / config:** none.

No `data/microstructure/` file was modified or committed. No
`data/research/` file was created or committed. No locked prior-phase
script (including `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py`),
source module, existing test, config, `.gitignore`, `pyproject.toml`,
`README.md`, MCP file, published manifest, sidecar, gate report, or
successor-state artefact was modified. No prior governance memo was
modified beyond the narrow `current-project-state.md` paragraph addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  172 ++
 .../2026-05-31_phase-4bn-j-r2_closeout.md          |  149 ++
 ...vised-acquisition-only-btcusdt-aggtrades-raw.md |  358 ++++
 ...e4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py | 2151 ++++++++++++++++++++
 .../test_phase4bn_j_r2_acquisition_script.py       |  812 ++++++++
 5 files changed, 3642 insertions(+)
```

The diff matches the expected change set from the authorization prompt
exactly: 1 modified doc + 2 added docs + 1 added script + 1 added test;
no deletions; no data artefacts.

## 6. Verdict

**LOCAL ARTEFACT PRODUCED — acquisition succeeded; remain paused.**

Phase 4bn-J-R2 executed the revised acquisition-only retry authorized by
Phase 4bn-J-R1. It acquired all **275 / 275** new pre-v002 raw BTCUSDT
Binance USDⓈ-M futures aggTrades daily archives for **2024-03-01 ..
2024-11-30 inclusive UTC**, integrity-verified each (CHECKSUM-first →
SHA256 match → `zipfile.testzip()` → bounded Phase 4ax row-sample
validation; 0 failures of any class), totalling **5,140,686,147 bytes ≈
4.788 GiB** and **400,001,695** aggTrade rows in **2,051 s (≈34 min)**,
with **no warning threshold and no hard cap crossed** and **no
fail-closed stop condition triggered**. The full intended envelope
remains 2024-03-01 .. 2025-02-28; the existing v002 terminal window
(2024-12-01 .. 2025-02-28) and the sealed v002 test split (2025-02-14 ..
2025-02-28) were not re-downloaded, overwritten, or read. All raw
artefacts are local gitignored and **not committed**. The segment
manifest is non-eligible (`research_eligible=false`,
`eligibility_gate_status="pending"`, `test_holdout_touched=false`,
`test_rows_loaded=0`). **Result state:**
`ACQUISITION_SUCCEEDED__RAW_ARTEFACTS_LOCAL_GITIGNORED__REMAIN_PAUSED`.
**Decision:**
`RECOMMEND_AUTHORIZE_RAW_ARCHIVE_ELIGIBILITY_GATE__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
**Phase 4bn-J-R2 is now merge-complete on `main` after this merge** (with
the merge-closeout + SHA-finalization commits recorded per the repository
convention). The recommended raw archive eligibility gate and any other
successor are **not** authorized. **Recommended state: remain paused.**

## 7. Local gitignored outputs

Produced by the acquisition and **not committed** (gitignored under
`data/microstructure/`; confirmed by `git check-ignore -v` →
`.gitignore:85`):

- **275 raw daily zip archives** for 2024-03-01 .. 2024-11-30 under
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/{YYYY}/{MM}/`,
  each with a paired canonical `.sha256` sidecar (**275 zips, 275
  sidecars**).
- **Segment manifest:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`
  — SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`
  (with `.sha256` sidecar).
- **Acquisition log:**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2_acquisition_log.json`
  — SHA256 `0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`
  (with `.sha256` sidecar).
- **Total raw footprint:** 5,140,686,147 bytes / **4.788 GiB**.
- **Rows inventoried:** 400,001,695.
- **Runtime:** 2,051 s / ≈34 min.
- **Warning thresholds crossed:** none (4.788 GiB < 10 GiB; 34 min < 2 h).
- **Hard caps crossed:** none (< 25 GiB; < 4 h).
- **Fail-closed stop conditions triggered:** none.
- These derive from public unauthenticated `data.binance.vision` daily
  archives and are reproducible from the committed script; they are
  intentionally uncommitted.

## 8. Validation results

Re-run during merge review (no acquisition rerun; no endpoint contacted;
no archive downloaded; no HEAD preflight; no raw/sealed inspection):

- `ruff check scripts/phase4bn_j_r2_acquire_btcusdt_aggtrades_pre_v002.py tests/research/microstructure/test_phase4bn_j_r2_acquisition_script.py`
  → **All checks passed**.
- `pytest tests/research/microstructure/test_phase4bn_j_r2_acquisition_script.py`
  → **117 passed**.
- `pytest tests/research/microstructure/test_phase4bl_c_acquisition_script.py`
  → **71 passed** (locked Phase 4bl-C script unmodified; no regression).
- `git diff --check` → clean (no whitespace errors).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`
  (transient; not committed) plus the gitignored local data namespaces;
  no data artefact staged or committed.
- **mypy:** the `[tool.mypy]` gate is scoped to `src/prometheus`
  (`pyproject.toml` `files = ["src/prometheus"]`). The new acquisition
  script lives under `scripts/` like the locked Phase 4bl-C script and is
  outside the type-gate; running mypy directly on either `scripts/` file
  yields only `scripts/`-only notes, so mypy is not part of this phase's
  changed-surface gate. This matches the locked Phase 4bl-C precedent.

## 9. Upstream immutability evidence

- **Published v002 raw manifest**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`:
  not read and not mutated by this phase (verified: last-write timestamp
  unchanged from before the phase; the new script writes a distinct
  phase-scoped segment manifest filename and refuses any write to the
  published v002 manifest path).
- **Existing v002 terminal window raw archives** (2024-12-01 ..
  2025-02-28): not re-downloaded, not overwritten, not read — the new
  script's segment date guard makes any date `>= 2024-12-01` unreachable.
- **Sealed v002 test split** (2025-02-14 .. 2025-02-28): untouched — not
  read / counted / sampled / hashed / summarized / inspected.
- No other prior artefact (normalized / feature / label parquet or
  manifest, gate report, successor-state JSON, sidecar) was accessed for
  mutation. The acquisition wrote only new pre-v002 raw zips + sidecars +
  the new segment manifest/log.

## 10. Manifest state preservation

- New phase-scoped segment manifest
  (`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`):
  `research_eligible: false`; `eligibility_gate_status: "pending"`;
  `test_holdout_touched: false`; `test_rows_loaded: 0`; governance
  labels all `forbidden` for ML / features / labels / strategy.
- No existing manifest's `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` was transitioned. No governance label changed on any
  existing manifest.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code (`src/prometheus`) modified;
- no locked prior-phase script modified (the new script is additive;
  `scripts/phase4bl_c_acquire_btcusdt_aggtrades_multiday.py` untouched);
- no existing test modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no `data/microstructure/` artefact committed; no `data/research/`
  artefact created or committed;
- existing v002 terminal window and sealed v002 test split not read /
  counted / sampled / hashed / summarized / inspected / mutated;
- published v002 manifest not read or mutated;
- no `research_eligible` flipped; no `eligibility_gate_status`
  transitioned; no `chronological_split_policy` changed; no
  `diagnostics_authorized` / `ml_authorized` changed;
- no new holdout / ML split defined;
- no successor-state / gate-report artefact created or mutated;
- no `.duckdb` / `.sqlite` / database created; no Parquet compaction; no
  normalized / feature / label artefact created; no v003 created;
- no ML trained / scored; no predictions; no diagnostics; no strategy /
  signals / PnL / backtest;
- no normalizer / feature kernel / label kernel / raw-gate / derived-gate
  rerun; no acquisition rerun during merge review;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used; no
  authenticated / private endpoint / WebSocket / user stream contacted;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
  preserved (never invoked);
- no retained verdict revised; no project lock loosened; no M0
  amendment; no successor authorized.

## 12. Retained verdict ledger

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

## 13. Preserved project locks

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7
- Phase 3r §8
- Phase 3v §8
- Phase 3w §6 / §7 / §8
- Phase 4j §11
- Phase 4k
- Phase 4p
- Phase 4q
- Phase 4v
- Phase 4w
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bl-F four-tier risk model
- Phase 4bn-J-R1 raw-only disk-cap amendment (10 GiB warning / 25 GiB
  hard; runtime 2 h / 4 h)

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-J-R2 merge does not, and cannot, be construed as
authorising:

- ML model training, model selection, scoring, prediction, or any
  conversion of raw archives / future labels into signals;
- normalization, feature derivation, label derivation, or feature/label
  manifest creation;
- the recommended **raw archive eligibility gate** (recommended only;
  NOT authorized);
- strategy signal construction, strategy logic, position state, entry /
  exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation; barrier /
  target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / tick / additional /
  post-v002 aggTrades acquisition; ETHUSDT or extra-horizon acquisition;
  v003 creation;
- storage migration, database creation, `.duckdb` / `.sqlite` creation,
  or Parquet compaction;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible`,
  `eligibility_gate_status`, or `chronological_split_policy` from this
  evidence alone.

## 15. Successor authorization

**None.**

Not authorized by this merge:

- Raw archive eligibility gate for the expanded raw envelope (the Phase
  4bn-J-R2 recommendation; NOT authorized);
- source-policy documentation memo (backfilling `historical-data-spec.md`
  with the aggTrades archive convention);
- derived-stack storage-budget memo (before any normalization / features
  / labels);
- process-doc `D:` path-string update phase for the
  lightweight-workspace standard;
- normalization / feature / label derivation phases;
- ML / diagnostics / strategy / backtest implementation;
- Phase 5; Phase 4 canonical;
- additional / post-v002 / ETHUSDT / mark-price / spot / cross-venue /
  order-book / tick / 5m / 1m data acquisition;
- v003 dataset creation; storage migration; database creation; Parquet
  compaction;
- paper / shadow; live-readiness; deployment; exchange-write; production
  keys; authenticated APIs; private endpoints; user stream; MCP /
  Graphify / `.mcp.json` / credentials.

## 16. Recommended state

**Remain paused.**

**Conditional next, NOT authorized:** a future **raw archive eligibility
gate** is the cleanest non-paused option. It would, under separate
operator authorization, evaluate the newly acquired pre-v002 raw segment
(plus the existing v002 raw window, by reference) against the raw
eligibility contract and record a gate report + non-eligible
successor-state, **without** flipping `research_eligible`, without
normalization / features / labels, and without touching the sealed test
split. It is **not** authorized by this merge. No ML / diagnostics /
normalization / feature / label / strategy / PnL / backtest /
storage-migration / database / Parquet-compaction / v003 / paper / shadow
/ live / exchange-write option is valid from this state unless separately
authorized after this merge.
