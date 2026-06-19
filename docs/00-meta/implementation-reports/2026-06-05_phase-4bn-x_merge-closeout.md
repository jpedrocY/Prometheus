# Phase 4bn-X — Merge Closeout

## 1. Phase identity

- **Phase:** 4bn-X — Label-Layer Eligibility Gate for the Pre-V002 BTCUSDT
  aggTrades Label Segment.
- **Type:** code + tests + docs + local gitignored read-only gate-report
  generation phase (Tier 1 — Full Phase per `phase-risk-tiering-standard` §3).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-X bounded read-only label-layer gate
  runner, its offline test module, its implementation report, its branch
  closeout, and the narrow `current-project-state.md` update onto `main`,
  recording that the read-only gate over the Phase 4bn-W non-eligible pre-v002
  label segment PASSED (40/40 checks) and that the segment remains non-eligible
  / paused with no successor authorized.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-x/label-layer-eligibility-gate`.

## 2. SHAs

- **`main` SHA before merge:** `5bcae53ee843759a6c81c14d71a66dc241023e31`
  (`docs(phase-4bn-w): finalize merge closeout shas`).
- **Branch commit SHA (code + tests + docs):**
  `d272dcd0fd7ade569f8e638bee7303e4fea26717`
  (`data(phase-4bn-x): gate pre-v002 label segment`).
- **Merge commit SHA:** `daee3df628c3e03df58e3d6f11a399c0ae5b8097`
  (`data(phase-4bn-x): merge label-layer eligibility gate`).
- **Merge-closeout commit SHA:** `af6387d118ffda5c7f9a3e307f6de1a6f4c081a0`
  (`docs(phase-4bn-x): add merge closeout`).
- **SHA-finalization commit SHA:** the subsequent
  `docs(phase-4bn-x): finalize merge closeout shas` commit — its own hash
  becomes the new `main` tip; recorded in the final operator report after the
  commit and push.
- **Final `main` / `origin/main` SHA after push:** the SHA-finalization commit
  hash above; recorded in the final operator report after `git push origin main`.

## 3. Merge method

- `git merge --no-ff` with the `ort` strategy.
- Merge commit message: `data(phase-4bn-x): merge label-layer eligibility gate`.
- No `--no-verify`; no `--no-gpg-sign`; no `-c commit.gpgsign=false`; no force.
- Push status: pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing (recorded at SHA-finalization).

## 4. Files brought forward by the merge

- **docs (3):**
  `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-x_label-layer-eligibility-gate.md`
  (added), `docs/00-meta/implementation-reports/2026-06-05_phase-4bn-x_closeout.md`
  (added), `docs/00-meta/current-project-state.md` (modified — narrow Phase
  4bn-X paragraph + new active `Current phase:` block; prior paragraphs/blocks
  preserved verbatim).
- **scripts (1):** `scripts/phase4bn_x_validate_label_pre_v002_gate.py` (added).
- **tests (1):**
  `tests/research/microstructure/test_phase4bn_x_label_layer_gate.py` (added).
- **source / config:** none.
- **`data/microstructure/` files modified:** none. No
  `data/microstructure/` or `data/research/` artefact was added, modified, or
  committed. No prior source / test / script / config / `.gitignore` /
  `pyproject.toml` / README / MCP file / committed manifest / sidecar / gate
  report / successor-state artefact was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  100 ++
 .../2026-06-05_phase-4bn-x_closeout.md             |  140 ++
 ...-05_phase-4bn-x_label-layer-eligibility-gate.md |  401 ++++++
 scripts/phase4bn_x_validate_label_pre_v002_gate.py | 1500 ++++++++++++++++++++
 .../test_phase4bn_x_label_layer_gate.py            |  903 ++++++++++++
 5 files changed, 3044 insertions(+)
```

The diff matches the expected change set from the authorization prompt exactly
(one script added, one test module added, two implementation docs added, one
narrow `current-project-state.md` modification).

## 6. Verdict

**GATE PASS.** The Phase 4bn-X bounded read-only label-layer eligibility gate
ran once over the Phase 4bn-W local, non-eligible, gitignored pre-v002 BTCUSDT
aggTrades label segment (Binance USDⓈ-M futures; 2024-03-01 .. 2024-11-30
inclusive UTC; 275 dates) and produced the result state
`LABEL_LAYER_GATE_PASSED__LOCAL_LABEL_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED` with
**40/40 checks PASS** in 205.6 s, performing a full per-row scan of all 275
label Parquets (no sampling). The decision is
`RECOMMEND_AUTHORIZE_CHRONOLOGICAL_SPLIT_AND_HOLDOUT_POLICY_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
Phase 4bn-X is **merge-complete on `main`** after this merge and the
merge-closeout / SHA-finalization commits. A passing gate authorizes nothing:
the label segment remains `research_eligible=false`,
`eligibility_gate_status=pending`, `no_successor_authorization=true`,
`chronological_split_policy=not_yet_defined`. Recommended state: remain paused.

## 7. Local gitignored outputs

One local gitignored gate report + canonical sidecar were produced by the
Phase 4bn-X branch run; **neither is committed**:

- **Gate report path:**
  `data/microstructure/gate-reports/labels/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w__phase-4bn-x__1781897304431__5bcae53ee843.json`
- **Gate report SHA256:**
  `ffb5b09215d6efd9b34c3a625421a367c9587b63027c59f2fc9d5c59797a8984`
- **Gate report sidecar SHA256:**
  `68dd5b5709bb523003ed183ac776e95ad1c82a40deb65e3cda51b2e10e51997c`
- **Status:** not committed; gitignored via `.gitignore:85`
  (`git check-ignore -v` confirmation in §8).
- **Input label segment validated (source):**
  manifest
  `data/microstructure/manifests/microstructure_labels_aggtrades_v001__v002_pre_v002_segment_4bn_w.json`
  SHA256 `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161`;
  275 label Parquet + 275 sidecars; total rows **400,001,695**; total footprint
  **15,654,082,679 bytes**; `label_config_hash =
  b3bd5d2b332e9f4b4a6bbf76de533f48993b4d0500e4aab90087404b51558970`;
  `envelope_terminal_unix_ms = 1733011199331`; `envelope_terminal_utc_date =
  2024-11-30`; per-horizon censored counts 1s=3 / 5s=20 / 15s=42 / 60s=216;
  invalid-price row count 0. Checks passed/failed: **40 / 0**. Runtime: 205.6 s.
  D: free-space before: 1,259,694,313,472 bytes; after: 1,259,694,301,184 bytes.

## 8. Validation results

- `ruff check scripts/phase4bn_x_validate_label_pre_v002_gate.py tests/research/microstructure/test_phase4bn_x_label_layer_gate.py`
  → **All checks passed**.
- `pytest tests/research/microstructure/test_phase4bn_x_label_layer_gate.py`
  → **48 passed**.
- `pytest` predecessor suites (4bn-W / 4bn-T / 4bn-S / 4bn-P / 4bn-O) →
  **155 passed** (203 total with the new module).
- `mypy src/prometheus` → 96 pre-existing errors in 12 unrelated modules
  (`ml_baseline_dataset_v002.py`, `feature_drift_v002.py`, …); Phase 4bn-X added
  **no `src/prometheus` change** (the wrapper lives under `scripts/`, outside
  the repo-standard mypy scope), so these errors are not introduced by this
  merge.
- `git diff --check` → clean.
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/microstructure/gate-reports/labels/…__phase-4bn-x__…json`
  → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only the expected untracked `.claude/scheduled_tasks.lock`.

The real label-layer gate was **not** rerun during merge review (evidence
already recorded on the branch); no predecessor execution or gate was rerun.

## 9. Upstream immutability evidence

Phase 4bn-X is read-only on all data; the gate re-hashed every input artefact
and mutated none. The following were validated and left bit-for-bit unchanged:

- Phase 4bn-W label segment manifest SHA256
  `69746c88860bff2de197dca0841dc2c6e439a93b06ba4dac9f58312b95e1b161` + sidecar
  `636a4c1a0159364e7d67f502dda48664f18fc16545c993935e6429ccdf868239` —
  IDENTICAL pre/post.
- 275 Phase 4bn-W label Parquets + 275 sidecars — every SHA256 matched its
  sidecar and the manifest inventory; IDENTICAL pre/post.
- Phase 4bn-S feature segment manifest
  `4881eb874b132d5952e34c9d1d3e8191dd32d89a3bc2a02e65a02eebc4599b52` + sidecar
  `f2ca2f48a5ac8ccfb892d0460cdfbbbb891451b9d94135adb3bff0936c8592e5` —
  IDENTICAL.
- Phase 4bn-T feature-layer gate report
  `db731d1be06295404ef195d9b5b5bad8010ce6ae6efef43ece90c29653d6ab08` —
  IDENTICAL.
- Phase 4bn-O normalized segment manifest
  `0e96ae37ff3a02a940724187d973bd0af1ef83585c8427494d33ab32d6bdd9fa` + sidecar
  `5d7dcbefbafcc81f2fcb1977ff9f35b08d58684542608317368c1f60f11e6402` —
  IDENTICAL.
- Phase 4bn-P normalized-layer gate report
  `3452fd9d33e45c3570693919f419e3ca2c9e9f886b1490fe3755d322e27af134` —
  IDENTICAL.
- Phase 4bn raw segment manifest
  `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1` —
  IDENTICAL.

No published label / feature / normalized `__v002` Parquet content was read; no
v002 terminal raw/normalized/feature/label window was read; no sealed-test data
was read.

## 10. Manifest state preservation

The Phase 4bn-W label segment manifest (the only manifest in scope) is preserved
unchanged: `research_eligible = false`; `eligibility_gate_status = "pending"`;
`chronological_split_policy = "not_yet_defined"`; governance labels
(`ml_use`/`diagnostics_use`/`strategy_use`/`backtest_use` = `forbidden`)
unchanged; `no_successor_authorization = true`; `v002_terminal_window_mode =
by_reference`; `sealed_test_split_touched = false`; `test_holdout_touched =
false`; `test_rows_loaded = 0`. No transition occurred. The predecessor feature
(4bn-S) and normalized (4bn-O) manifests remain `research_eligible = false` /
`eligibility_gate_status = pending`. Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
preserved (never invoked).

## 11. Boundary confirmations

- no labels modified; no label manifest / Parquet / sidecar modified;
- no feature / normalized / raw artefact modified; no predecessor gate report
  modified;
- no published label `__v002` read or mutated (by reference only);
- no v002 terminal raw / normalized / feature / label window read;
- no sealed-test data read (`test_rows_loaded = 0`); no test holdout touched;
- no `data/microstructure/` write outside the gitignored gate-report surface;
  no `data/microstructure/` or `data/research/` artefact committed;
- no `data/research` output created;
- no `research_eligible` flipped; no `eligibility_gate_status` transitioned; no
  `chronological_split_policy` changed;
- no label derivation rerun; no feature execution rerun; no normalization rerun;
  no raw / normalized-layer / feature-layer gate rerun;
- no ML trained; no model scoring; no predictions; no scores; no diagnostics; no
  strategy; no signals; no PnL; no backtests;
- no acquisition; no endpoint called; no Binance API; no WebSocket; no archive
  download; no HEAD preflight;
- no database created; no Parquet compaction; no storage migration; no v003;
- no source / test / script / `.gitignore` / `pyproject.toml` / README / MCP
  file modified;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved
  (never invoked);
- no retained verdict revised; no project lock loosened; no M0 amendment; no
  successor authorized.

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down
  families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path + sidecar policy
- Phase 4bn-J-R1 raw-only cap amendment
- Phase 4bn-L derived-stack storage budget
- Phase 4bn-N normalization manifest/versioning convention
- Phase 4bn-R feature manifest/versioning convention
- Phase 4bn-V label manifest/versioning convention

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bn-X merge does not, and cannot, be construed as authorising:

- the chronological split / holdout policy memo itself (recommended only,
  separately authorized);
- ML-baseline readiness, ML model training, model selection, scoring,
  predictions, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state, entry / exit
  rules, or backtest design / execution; PnL;
- diagnostics;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades / ETHUSDT
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening;
- storage migration, database creation, Parquet compaction, or v003 dataset
  creation;
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`,
  or `chronological_split_policy` from this gate-pass evidence alone.

## 15. Successor authorization

**None.**

Not authorized by this merge:

- chronological split / holdout policy memo (docs-only; recommended next, NOT
  authorized);
- ML-baseline readiness memo;
- holdout-boundary memo;
- source-policy documentation memo;
- process-doc `D:` path-string update;
- ML implementation; strategy implementation; backtest implementation;
- diagnostics implementation;
- additional aggTrades / 5m / 1m / tick / mark-price / order-book data
  acquisition;
- paper / shadow; live-readiness; deployment; exchange-write; production keys;
  authenticated APIs; private endpoints; user stream; MCP / Graphify /
  `.mcp.json` / credentials;
- Phase 4 canonical; Phase 5.

## 16. Recommended state

**Remain paused.**

**Conditional next, NOT authorized:** a docs-only chronological split / holdout
policy memo is the cleanest non-paused option. It would define train /
validation / test boundaries, purging / embargo if needed, sealed-test rules,
and admissibility conditions for future ML-baseline work — without running ML,
flipping eligibility, or reading the v002 terminal / sealed-test dates. It is
**not** authorised by this merge.
