# Phase 4bn-K — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bn-K — Expanded Raw Archive Eligibility Gate.
- **Type:** Raw archive eligibility gate / local gitignored
  data-validation / docs + gate-report phase. **Tier 1 — Full Phase**
  (per `docs/00-meta/process/phase-risk-tiering-standard.md` §3; a first
  execution of a gate over the newly acquired pre-v002 raw segment,
  adjacent to future normalization / feature / label / eligibility
  state, authorizing none of it).
- **Action:** merge into `main`.
- **Merge purpose:** bring the Phase 4bn-K branch (new bounded standalone
  pre-v002 raw archive eligibility gate script + offline tests + the
  implementation report + closeout + the narrow `current-project-state.md`
  update) into `main` and record the canonical merge-closeout that makes
  Phase 4bn-K project-complete. The gate's local gitignored output (one
  gate report + its `.sha256` sidecar under
  `data/microstructure/gate-reports/raw/`) is **not** committed and
  accompanies the merge as local data only.
- **Target branch:** `main`.
- **Source branch:** `phase-4bn-k/expanded-raw-archive-eligibility-gate`.

## 2. SHAs

- **`main` SHA before merge:** `cf7dc4f7e663d6f17610e775a9e5061de0b523ce`
  (`docs(phase-4bn-j-r2): finalize merge closeout shas`; pre-merge
  `main == origin/main == cf7dc4f7e663…` verified in sync).
- **Branch commit SHA (docs + code):**
  `b00a4f330eb704b4dea9c1a729d4ac8433383342`
  (`data(phase-4bn-k): add expanded raw archive eligibility gate`).
- **Merge commit SHA:** `19c6661ad4e4173dd0277bc34b1b1684be6d20f7`
  (`data(phase-4bn-k): merge expanded raw archive eligibility gate`).
- **Merge-closeout commit SHA:** `<MERGE_CLOSEOUT_COMMIT_SHA>`
  (`docs(phase-4bn-k): add merge closeout`), recorded by the subsequent
  SHA-finalization commit. Per the repo convention used for Phase
  4bn-J-R2 / 4bn-J-R1 / 4bn-I / 4bn-H / 4bn-G / 4bn-F / 4bn-E / 4bn-D /
  4bn-C / 4bn-B / 4bn-A, the merge-closeout commit cannot self-reference
  its own hash inside its own diff; the SHA is filled in by the
  SHA-finalization commit, which can reference the merge-closeout commit
  hash because that hash exists in `git log` before the SHA-finalization
  commit is created.
- **SHA-finalization commit:** `<SHA_FINALIZATION_COMMIT_SHA>`
  (`docs(phase-4bn-k): finalize merge closeout shas`). Same convention:
  the SHA-finalization commit cannot self-reference its own hash inside
  its own diff; its SHA is captured in the final operator report and
  `git log`.
- **Final `main` / `origin/main` SHA after push:**
  `<FINAL_MAIN_SHA>` — after the SHA-finalization commit and push, final
  `main` SHA == final `origin/main` SHA == the SHA-finalization commit
  (recorded in the final operator report and `git log`).

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message:
  `data(phase-4bn-k): merge expanded raw archive eligibility gate`.
- No `--no-verify`. No `--no-gpg-sign`. No `-c commit.gpgsign=false`. No
  force-push.
- Push status: **Pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing** (recorded at SHA-finalization).

## 4. Files brought forward by the merge

**Docs (3):**
- `docs/00-meta/current-project-state.md` (modified; narrow Phase 4bn-K
  paragraph + new `Current phase:` block; prior Phase 4bn-A … 4bn-J-R2
  paragraphs and blocks preserved verbatim as labelled historical
  context);
- `docs/00-meta/implementation-reports/2026-06-01_phase-4bn-k_expanded-raw-archive-eligibility-gate.md`
  (added; implementation report; 23 sections);
- `docs/00-meta/implementation-reports/2026-06-01_phase-4bn-k_closeout.md`
  (added; branch closeout).

**Scripts (1):**
- `scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py` (added; new
  bounded standalone pre-v002 raw archive eligibility gate; modelled on
  the locked Phase 4bl-D gate but scoped to the Phase 4bn-J-R2 segment
  manifest with a hard `>= 2024-12-01` boundary guard; imports only the
  Phase 4ax validator + Phase 4bb-F canonical-path helpers).

**Tests (1):**
- `tests/research/microstructure/test_phase4bn_k_raw_archive_gate.py`
  (added; 53 offline tests incl. a denylist regression test; no network,
  no local-data read, no sealed-test read).

**Source / config:** none.

No `data/microstructure/` file was modified or committed. No
`data/research/` file was created or committed. No locked prior-phase
script (including the locked Phase 4bl-D gate
`scripts/phase4bl_d_validate_multiday_raw_manifest_gate.py` and the
locked acquisition scripts), source module, existing test, config,
`.gitignore`, `pyproject.toml`, `README.md`, MCP file, published
manifest, sidecar, prior gate report, or successor-state artefact was
modified. No prior governance memo was modified beyond the narrow
`current-project-state.md` paragraph addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  154 ++
 .../2026-06-01_phase-4bn-k_closeout.md             |  143 ++
 ...-4bn-k_expanded-raw-archive-eligibility-gate.md |  524 +++++
 ...hase4bn_k_validate_pre_v002_raw_archive_gate.py | 2272 ++++++++++++++++++++
 .../test_phase4bn_k_raw_archive_gate.py            |  413 ++++
 5 files changed, 3506 insertions(+)
```

The diff matches the expected change set from the authorization prompt
exactly: 1 modified doc + 2 added docs + 1 added script + 1 added test;
no deletions; no data artefacts.

## 6. Verdict

**GATE PASS — local raw segment structurally eligible; remains
non-eligible in the research sense; remain paused.**

Phase 4bn-K executed the raw archive eligibility gate recommended (only)
by Phase 4bn-J-R2. The new bounded standalone gate evaluated the local
Phase 4bn-J-R2 pre-v002 raw segment — BTCUSDT, Binance USDⓈ-M futures,
aggTrades only, **2024-03-01 .. 2024-11-30 inclusive UTC** — for
**structural** eligibility only. The gate ran **33 / 33 checks PASS**
(0 FAIL, 0 ERROR) in **496.2 s** wall-clock: 275 inventory dates
(contiguous, no missing, no duplicate, none `>= 2024-12-01`); 275 raw
archives and 275 `.sha256` sidecars; recomputed total footprint
**5,140,686,147 bytes**; recomputed total row count **400,001,695**;
segment manifest SHA256
`1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1` and
acquisition-log SHA256
`0266210f23cae53ceda83270fd3466f15ffafdd7ded22bca828fc0cb788bcf93`
matched the Phase 4bn-J-R2 recorded values; every raw zip SHA256 matched
both the manifest hash and its canonical sidecar; `zipfile.testzip()`
reported no corruption; each archive contained exactly one CSV member; a
full streaming structural scan independently recomputed the aggregate
row count and footprint; and bounded Phase 4ax validation was run on
head+tail samples totalling **281,600** sampled rows across the 275
archives. The gate is **structural only** — a passing raw archive gate
does **not** establish edge, profitability, tradability,
strategy-readiness, signal-readiness, paper/shadow readiness, or
live-readiness. The local raw segment **remains non-eligible** in the
research sense: `research_eligible` stays `false`,
`eligibility_gate_status` stays `pending`, no manifest eligibility
transition occurred, no `chronological_split_policy` transition occurred,
no `diagnostics_authorized` / `ml_authorized` transition occurred, and no
successor was authorized. The existing v002 terminal raw window
(2024-12-01 .. 2025-02-28) was treated **by reference only** — not read,
hashed, counted, sampled, summarized, inspected, or mutated — and the
sealed v002 test split (2025-02-14 .. 2025-02-28) was **untouched**. The
published v002 raw manifest was not opened or mutated. **Result state:**
`RAW_ARCHIVE_GATE_PASSED__LOCAL_RAW_SEGMENT_NON_ELIGIBLE__REMAIN_PAUSED`.
**Decision:**
`RECOMMEND_AUTHORIZE_DOCS_ONLY_DERIVED_STACK_STORAGE_BUDGET_MEMO__SUBJECT_TO_SEPARATE_OPERATOR_AUTHORIZATION`.
**Phase 4bn-K is now merge-complete on `main` after this merge** (with
the merge-closeout + SHA-finalization commits recorded per the
repository convention). Project completion is recorded by this
merge-closeout plus its SHA-finalization commit per the repo's
established convention. The recommended docs-only derived-stack
storage-budget memo is itself **only a recommendation** and is **not**
authorized by Phase 4bn-K; normalization-readiness and any successor are
**not** authorized. **Recommended state: remain paused.**

## 7. Local gitignored outputs

Produced by the gate and **not committed** (gitignored under
`data/microstructure/`; confirmed by `git check-ignore -v` →
`.gitignore:85`):

- **Gate report:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1780436389489__cf7dc4f7e663.json`
  — SHA256
  `051bed7b3a146278e389bd8e265243d30fd541b5f36061d0573f3522920f9c24`.
- **Gate report sidecar:**
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bn-k__1780436389489__cf7dc4f7e663.json.sha256`
  — 153 bytes; canonical Phase 4bb-F format `<sha256>␠␠<basename>\n`
  (two spaces, LF, no BOM); embedded token matches the recomputed report
  SHA256 bit-for-bit.
- **Gate run:** `overall_status=pass`; **33 / 33** checks PASS / 0 FAIL /
  0 ERROR; wall-clock **496.2 s**.
- **Archive count:** 275. **Sidecar count:** 275.
- **Recomputed total footprint:** 5,140,686,147 bytes (≈ 4.788 GiB).
- **Recomputed total row count:** 400,001,695.
- **Total bounded sample rows validated:** 281,600 across the 275
  archives.
- The report records `phase-4bn-k`, base main SHA
  `cf7dc4f7e663d6f17610e775a9e5061de0b523ce`, input segment manifest
  SHA256 `1659e6da9ccc1c4a49c2f497e1f4a70f8082cac24142c77ac6d5217197b3a3d1`,
  the gate result state, `segment_non_eligible: true`,
  `research_eligible_after: false`, `no_successor_authorization: true`,
  `v002_terminal_window_read: false`, and `sealed_test_split_touched:
  false`.
- The gate report derives from the byte-identical Phase 4bn-J-R2 local
  raw segment and is reproducible from the committed gate script; it is
  intentionally uncommitted.

**Tooling note (denylist fix + clean re-run).** The first gate execution
fail-closed on a defect in the gate's own scope-token denylist: the token
`"trades-"` is a substring of the in-scope `aggTrades-` family token
(lowercased `aggtrades-`), so it false-positively flagged every
legitimate aggTrades path. This was a **tool defect, not a data defect**
— all other 32 checks passed, including the full recomputed 400,001,695-
row / 5,140,686,147-byte aggregates. The denylist token was corrected to
the hyphen-delimited `"-trades-"` (plus `"/trades/"` and `"/spot/"`); a
regression test was added; the false-failure local gate report and its
sidecar were deleted; and the gate was re-run from a clean state. The
**authoritative final gate report is the 33 / 33 PASS report** recorded
above.

## 8. Validation results

Re-run during merge review (no gate rerun; no endpoint contacted; no
archive downloaded; no HEAD preflight; no raw-zip-content inspection; no
v002 terminal read; no sealed-test touch):

- `ruff check scripts/phase4bn_k_validate_pre_v002_raw_archive_gate.py tests/research/microstructure/test_phase4bn_k_raw_archive_gate.py`
  → **All checks passed!**.
- `pytest tests/research/microstructure/test_phase4bn_k_raw_archive_gate.py`
  → **53 passed** (53 collected; 0 failed; 0 error). (The branch closeout
  recorded `51 passed` at an earlier point in branch development; the
  final committed test surface contains 53 offline tests, all passing.
  This is a count refinement on the same offline test file, not a
  behaviour or scope change.)
- `git diff --check` → clean (no whitespace errors; exit 0).
- `git check-ignore -v data/microstructure/` → `.gitignore:85`.
- `git check-ignore -v data/research/` → `.gitignore:88`.
- `git status --short` → only `?? .claude/scheduled_tasks.lock`
  (transient Claude Code scheduler artefact; not committed) plus the
  gitignored local data namespaces; no data artefact staged or committed.
- **mypy:** the `[tool.mypy]` gate is scoped to `src/prometheus`
  (`pyproject.toml` `files = ["src/prometheus"]`, `strict = true`). The
  new gate script lives under `scripts/` like the locked Phase 4bl-D /
  4bl-C / 4bn-J-R2 scripts and is outside the type-gate, so mypy is not
  part of this phase's changed-surface gate. The new script modifies no
  `src/prometheus` module, so the strict src type-gate is unaffected.
  This matches the established locked-script precedent.

## 9. Upstream immutability evidence

- **Published v002 raw manifest**
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`:
  not opened and not mutated by this phase (the gate targets only the
  Phase 4bn-J-R2 *segment* manifest filename and never opens the
  published v002 manifest path).
- **Existing v002 terminal raw window** (2024-12-01 .. 2025-02-28):
  treated **by reference only** — not read, hashed, counted, sampled,
  summarized, inspected, or mutated. The gate's hard
  `is_within_segment(...)` boundary guard rejects any date `>= 2024-12-01`
  and returns before any filesystem access, making those files
  structurally unreachable.
- **Sealed v002 test split** (2025-02-14 .. 2025-02-28): **untouched** —
  not read / counted / sampled / hashed / summarized / inspected / used
  for continuity checks / used for QA. Phase 4bn-B `test_rows_loaded: 0`
  preserved.
- **Phase 4bn-J-R2 local raw segment** (275 zips + 275 sidecars + segment
  manifest + acquisition log): read / hashed / decompressed / structurally
  scanned **read-only**; recomputed SHA256s matched the recorded values
  bit-for-bit; no segment artefact was mutated.
- No prior gate report (e.g. `phase-4bl-d`), successor-state JSON, or any
  normalized / feature / label / metrics artefact was accessed for
  mutation.

## 10. Manifest state preservation

- Phase 4bn-J-R2 segment manifest
  (`microstructure_raw_aggtrades_v001__v002_pre_v002_segment_4bn_j_r2.json`):
  `research_eligible: false`; `eligibility_gate_status: "pending"`;
  `test_holdout_touched: false`; governance labels unchanged. Read only;
  **not** mutated.
- No existing manifest's `research_eligible`, `eligibility_gate_status`,
  `chronological_split_policy`, `diagnostics_authorized`, or
  `ml_authorized` was transitioned. No governance label changed on any
  existing manifest. No manifest eligibility transition occurred. No
  `research_eligible` flip occurred.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).

## 11. Boundary confirmations

- no source code (`src/prometheus`) modified;
- no locked prior-phase script modified (the new gate is additive; the
  locked Phase 4bl-D v002 gate and the locked acquisition scripts are
  untouched);
- no existing test modified;
- no `.gitignore`, `pyproject.toml`, `README.md`, or MCP file modified;
- no `data/microstructure/` artefact committed; no `data/research/`
  artefact created or committed;
- existing v002 terminal window treated by reference only — not read /
  hashed / counted / sampled / summarized / inspected / mutated;
- sealed v002 test split untouched — not read / counted / sampled /
  hashed / summarized / inspected / used for continuity / used for QA;
- published v002 manifest not opened or mutated;
- no `research_eligible` flipped; no `eligibility_gate_status`
  transitioned; no `chronological_split_policy` changed; no
  `diagnostics_authorized` / `ml_authorized` changed;
- no manifest eligibility transition; no new holdout / ML split defined;
- no successor-state artefact created or mutated;
- no `.duckdb` / `.sqlite` / database created; no Parquet compaction; no
  normalized / feature / label artefact created; no v003 created;
- no normalization; no feature / label derivation; no feature ranking /
  selection / pruning / engineering;
- no ML trained / scored; no predictions; no diagnostics; no strategy /
  signals / PnL / backtest;
- no acquisition; no endpoint / public endpoint / Binance /
  `data.binance.vision` contact; no archive or CHECKSUM download; no HEAD
  preflight; no acquisition rerun; no gate rerun during merge review;
- no credentials / `.env` / `.mcp.json` / MCP / Graphify; no
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

The Phase 4bn-K merge does not, and cannot, be construed as authorising:

- ML model training, model selection, scoring, prediction, or any
  conversion of raw archives / future labels into signals;
- normalization, feature derivation, label derivation, feature ranking /
  selection / pruning / engineering, or feature/label manifest creation;
- the recommended **docs-only derived-stack storage-budget memo**
  (recommended only; NOT authorized);
- any **normalization-readiness or normalization execution plan**
  (NOT authorized);
- any **source-policy documentation memo** (NOT authorized);
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
  gate evidence alone;
- reading the existing v002 terminal window, touching the sealed v002
  test split, or opening / mutating the published v002 raw manifest.

## 15. Successor authorization

**None.**

Not authorized by this merge:

- docs-only derived-stack storage-budget memo (the Phase 4bn-K
  recommendation; NOT authorized — subject to separate operator
  authorization);
- normalization-readiness or normalization execution plan;
- source-policy documentation memo (backfilling `historical-data-spec.md`
  with the aggTrades archive convention);
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

**Conditional next, NOT authorized:** a future **docs-only derived-stack
storage-budget memo** is the cleanest non-paused option (the Phase 4bn-K
recommendation). It would, under separate operator authorization, set
explicit storage caps and stage boundaries for the prospective ML-ready
derived stack (which Phase 4bn-G scoped at plausibly ~150–250 GiB with
~300 GiB comfortable working headroom) **before** any normalization /
feature / label phase runs — without flipping `research_eligible`,
without normalization / features / labels, and without touching the
sealed test split. The acceptable alternative, if repository convention
is read to expect normalization-readiness next, is a docs-only
normalization-readiness / normalization execution plan only. Both are
**not** authorized by this merge. No ML / diagnostics / normalization /
feature / label / strategy / PnL / backtest / storage-migration /
database / Parquet-compaction / v003 / paper / shadow / live /
exchange-write option is valid from this state unless separately
authorized after this merge.
