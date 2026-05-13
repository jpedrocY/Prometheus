# Phase 4bl-D-S1 — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-D-S1 — Sidecar Canonicalization Governance
  Memo
- **Type:** docs-only governance / remediation-decision memo
- **Action:** merge into `main`
- **Merge purpose:** record on `main` the Phase 4bl-D-S1 governance
  memo that evaluates remediation options for the
  `RAW_MULTIDAY_GATE_FAIL` recorded by Phase 4bl-D, recommends
  Option B1 (normalize the Phase 4az 2025-01-15 sidecar from CRLF
  to canonical Phase 4bb-F LF) as the cleanest practical
  remediation, predeclares the binding requirements of any future
  Phase 4bl-D-S2 controlled-execution successor and any future
  Phase 4bl-D-R gate rerun, and preserves the Phase 4bl-D gate
  FAIL as descriptive evidence only. The merge does **not**
  authorize any execution, remediation, gate rerun, manifest
  mutation, or successor-state recording.
- **Target branch:** `main`
- **Source branch:** `phase-4bl-d-s1/sidecar-canonicalization-governance-memo`

## 2. SHAs

- **`main` SHA before merge:** `01ca1d0`
  (`01ca1d07c601655e3c66b6349038ea4385d4e281`; Phase 4bl-D
  merge-closeout commit `docs(phase-4bl-d): add merge closeout`).
- **Branch commit SHAs (Phase 4bl-D-S1):**
  - `d4e2315` — `docs(phase-4bl-d-s1): sidecar canonicalization
    governance memo` (single tracked commit on the branch; adds
    governance memo + closeout, modifies
    `docs/00-meta/current-project-state.md`).
- **Merge commit SHA:**
  `ffe50d333e6038f154aa6f41e44129e387edc19a`
  (`docs(phase-4bl-d-s1): merge sidecar canonicalization
  governance memo`; created by `git merge --no-ff` with the `ort`
  strategy).
- **Final `main` / `origin/main` SHA after merge-closeout commit
  and push:** to be filled at commit time of this merge-closeout
  file. The canonical `main` anchor for Phase 4bl-D-S1
  project-completion is the merge-closeout commit (this file's
  commit) on `main`, recorded after push. Per Phase 4bk-A
  workflow-standard convention, any future one-commit SHA-chain
  fixup that records the final-`main` SHA value into this §2
  placeholder is optional, separately authorized, and does not
  change Phase 4bl-D-S1 lifecycle semantics.

## 3. Merge method

- `git merge --no-ff` with the default `ort` strategy.
- Merge commit message header:
  `docs(phase-4bl-d-s1): merge sidecar canonicalization governance memo`
- Body explicitly records: docs-only scope; recommendation =
  Option B1; no Phase 4az sidecar rewrite; no v002 manifest
  mutation; no Phase 4bl-D gate report modification; no source /
  test / script change; no prior-memo modification beyond the
  narrow `current-project-state.md` paragraph addition; Phase
  4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked); Phase 4bb-F
  canonical path policy preserved; Phase 4bl-D gate FAIL
  preserved as research evidence only; no remediation
  authorized; no successor phase authorized.
- No `--no-verify`. No `--no-gpg-sign`. No
  `-c commit.gpgsign=false`. No force-push.
- Push status: pushed to `origin/main` with no force, no
  skip-hooks, no skip-signing (recorded once the merge-closeout
  commit is pushed; see §16).

## 4. Files brought forward by the merge

### Docs (tracked)

- `docs/00-meta/current-project-state.md` — narrow update:
  inserted a new Phase 4bl-D-S1 narrative paragraph immediately
  before the existing Phase 4bl-D paragraph and replaced the
  prior "Current phase:" block with a new Phase 4bl-D-S1 block,
  preserving the prior Phase 4bl-D "Current phase:" block as
  historical context.
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-s1_sidecar-canonicalization-governance-memo.md`
  (new) — the 18-section Phase 4bl-D-S1 governance memo.
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-s1_closeout.md`
  (new) — the Phase 4bl-D-S1 branch closeout.

### Source / tests / scripts / config / runtime

None. No file under `src/`, `tests/`, `scripts/`,
`pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`,
MCP files, or runtime configuration was modified by this merge.

### `data/microstructure/`

None. **No `data/microstructure/` file was modified by this
merge.** No raw zip, no raw sidecar, no manifest, no gate report,
no successor-state file, no normalized parquet, no derived
manifest, no feature parquet, no feature manifest, no label
parquet, no label manifest, no diagnostic, no split artefact was
modified.

### Prior governance memos

None. No prior governance memo (Phase 3p §4.7; Phase 3r §8;
Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k;
Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0; Phase 4al
no-rescue; Phase 4aw `flip_research_eligible(...)` invariant;
Phase 4bb-F canonical path policy; Phase 4bl-A; Phase 4bl-B;
Phase 4bl-C; Phase 4bl-D) was modified beyond the narrow
`current-project-state.md` paragraph addition.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  354 ++++++
 .../2026-05-13_phase-4bl-d-s1_closeout.md          |  213 ++++
 ...-s1_sidecar-canonicalization-governance-memo.md | 1285 ++++++++++++++++++++
 3 files changed, 1852 insertions(+)
```

The diff matches the expected change set from the Phase 4bl-D-S1
authorization prompt exactly: three tracked files (one narrow
modification + two new docs), zero deletions, 1,852 insertions
total. No file outside the three documented files is in the
diff. No `data/microstructure/` file appears.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bl-D-S1 is project-complete on `main`. The recommended
remediation policy for the Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL`
is now recorded as: **Option B1 — normalize the Phase 4az
2025-01-15 sidecar from Windows CRLF to canonical Phase 4bb-F
LF in a separately authorized Phase 4bl-D-S2 controlled
execution phase, followed by a separately authorized Phase
4bl-D-R gate rerun.** The Phase 4bl-D gate FAIL remains the
authoritative research-evidence record; the v002 raw manifest
remains `research_eligible: false` and
`eligibility_gate_status: "pending"`; the Phase 4az 2025-01-15
sidecar remains unchanged at 100 bytes with CRLF terminator;
the Phase 4bl-D gate report and its sidecar remain
byte-identical at their recorded SHAs; Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked); Phase 4bb-F
canonical path policy preserved verbatim. No remediation is
authorized by this merge. The natural conditional successor
chain (Phase 4bl-D-S2 → Phase 4bl-D-R → Phase 4bl-E) is
**NOT** authorized by Phase 4bl-D-S1 and remains unauthorized
after this merge.

## 7. Local gitignored outputs (if any)

**None.**

Phase 4bl-D-S1 is docs-only and produced **no** local
gitignored artefact under `data/microstructure/`. No gate
report. No canonicalization report. No successor-state JSON.
No new manifest. No new sidecar. No new parquet. No new
diagnostic artefact. No new split artefact.

## 8. Validation results

- `git diff --check`: clean (no whitespace errors).
- `git diff --name-status main..phase-4bl-d-s1/sidecar-canonicalization-governance-memo`:
  exactly three files (one `M`, two `A`); matches §4.
- `git diff --stat main..phase-4bl-d-s1/sidecar-canonicalization-governance-memo`:
  3 files changed, 1,852 insertions(+); matches §5.
- `git status --short` after merge: only the pre-existing
  untracked entries `.claude/scheduled_tasks.lock` and
  `data/research/` (both unrelated to Phase 4bl-D-S1 and
  ignored / out-of-scope).
- `git ls-files data/microstructure/`: empty (no
  `data/microstructure/` file is tracked).
- `git check-ignore -v data/microstructure/`:
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/manifests/`:
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/raw/`:
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/`:
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/gate-reports/raw/`:
  `.gitignore:85: data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/`:
  `.gitignore:85: data/microstructure/`.
- `ruff` / `mypy` / `pytest` were **not** rerun by Phase
  4bl-D-S1 because this is a docs-only phase that modifies no
  source, no tests, no scripts, no configs, no `pyproject.toml`,
  no `.gitignore`, and no `.gitattributes`. The latest
  authoritative whole-repo validation remains the Phase
  4bb-F-implementation merge baseline (`ruff` PASS, `mypy`
  strict 120 source files PASS, microstructure `pytest`
  915 passed + 1 pre-existing labelled skip, whole-repo
  `pytest` 1698 passed + 1 skipped + 2 pre-existing simulation
  failures unchanged from prior phases).

## 9. Upstream immutability evidence (if applicable)

Phase 4bl-D-S1 did **not** access any local
`data/microstructure/` artefact. No per-artefact pre-merge vs
post-merge SHA256 comparison was performed because the merge
modifies only `docs/`. Every prior local gitignored
`data/microstructure/` artefact remains at its previously
recorded location and SHA256, including (without limitation):

- v002 raw manifest
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002.json`
  (recorded SHA `016967865c97...d87485`);
- v002 acquisition log
  `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v002_acquisition_log.json`
  (recorded SHA `52f6d7fb3cb0...c6b314`);
- Phase 4az 2025-01-15 raw zip
  `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
  (recorded SHA `f560c2e529e9...852b3e`);
- Phase 4az 2025-01-15 raw zip sidecar (100 bytes; CRLF
  terminator; preserved verbatim; the central finding of Phase
  4bl-D-S1 is recommending its future canonicalization, **not**
  executing it);
- Phase 4bl-D gate report
  `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d__1778627360966__2576a004c18a.json`
  (recorded SHA
  `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7`);
- Phase 4bl-D gate report sidecar (recorded SHA
  `b201dcd977ea2ef370b502f3840d90d6efd28b10354ca30eafcf155838c7a9c6`);
- every prior Phase 4az / 4bb / 4bd / 4be / 4bf / 4bg-B /
  4bh / 4bi-B / 4bi-D / 4bj-C / 4bj-E / 4bj-G / 4bj-J / 4bb-G
  artefact.

n/a in spirit: Phase 4bl-D-S1 is a docs-only governance memo
and did not access local artefacts beyond reading the public
SHA references recorded in prior memos.

## 10. Manifest state preservation (if applicable)

Every manifest in scope of Phase 4bl-D-S1 is preserved
verbatim:

- **v002 raw manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`, governance labels
  unchanged from the Phase 4bl-C state; not modified by Phase
  4bl-D-S1.
- **v001 raw manifest (Phase 4az):** `research_eligible:
  false`, `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bd derived manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bh feature manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`; not modified.
- **Phase 4bj-C label manifest:** `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`; not
  modified.
- Every successor-state sibling artefact (Phase 4bb-G raw;
  Phase 4bg-B derived; Phase 4bi-D feature; Phase 4bj-G label;
  Phase 4bj-J label no-split) preserved verbatim.

**Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).** Phase
4bl-D-S1 records a recommended remediation policy at the
governance level only; it does not transition any flag, perform
any mutation, or invoke any helper that would change manifest
state.

## 11. Boundary confirmations

The Phase 4bl-D-S1 merge honours every boundary required by the
authorization prompt and the Phase 4bk-A workflow standard:

- no Phase 4az 2025-01-15 sidecar rewrite, normalization, or
  modification;
- no `data/microstructure/` write or modification;
- no `data/microstructure/` artefact committed;
- no v002 raw manifest mutation;
- no v002 raw acquisition log mutation;
- no Phase 4bl-D gate report or sidecar mutation;
- no prior gate report, normalized parquet, feature parquet,
  label parquet, derived manifest, feature manifest, label
  manifest, sidecar, successor-state, diagnostic, or split
  artefact mutation;
- no normalizer / gate / kernel / diagnostic / ML / strategy
  / backtest script rerun;
- no source code, test, script, configuration,
  `pyproject.toml`, `README.md`, `.gitignore`,
  `.gitattributes`, or MCP-file modification;
- no `research_eligible` flipped on any actual manifest;
- no `eligibility_gate_status` transitioned on any actual
  manifest;
- no `chronological_split_policy` changed on any actual
  manifest;
- no ML model trained, designed, selected, or feature-ranked;
- no strategy created, implemented, or rescued;
- no signal computed; no PnL / MFE / MAE / R-multiple /
  equity / position / alpha / edge / prediction /
  model-score / decision-score / entry-exit output computed;
- no backtest run;
- no data acquired, downloaded, or normalized;
- no public endpoint called; no Binance API called; no
  WebSocket opened; no user stream contacted; no listenKey
  lifecycle invoked; no authenticated REST contacted; no
  private endpoint contacted;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used,
  read, written, or referenced;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked);
- Phase 4bb-F canonical path policy preserved (Phase 4bl-D-S1
  documents the CRLF deviation of the Phase 4az 2025-01-15
  sidecar as a finding under existing Phase 4bb-F policy; it
  does **not** amend Phase 4bb-F);
- Phase 4bl-D gate FAIL preserved as descriptive evidence only;
- Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, and memo template preserved;
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy preserved;
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized;
- no remediation executed.

## 12. Retained verdict ledger

Every retained verdict is preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

Every preserved lock is recorded verbatim:

- §11.6 = 8 bps per side;
- round-trip = 16 bps;
- §1.7.3 = 0.25% risk per trade / 2× leverage cap /
  one-position max / mark-price stops;
- Phase 3p §4.7 strict integrity gate (multi-day extension
  applied verbatim by Phase 4bl-D);
- Phase 3r §8 mark-price gap governance;
- Phase 3v §8 stop-trigger-domain governance;
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance;
- Phase 4j §11 metrics OI-subset partial-eligibility rule;
- Phase 4k V2 backtest-plan methodology;
- Phase 4p G1 strategy-spec memo;
- Phase 4q G1 backtest-plan methodology;
- Phase 4v C1 strategy-spec memo;
- Phase 4w C1 backtest-plan methodology;
- Phase 4ak M0 twelve-clause mechanism-admissibility gate +
  post-null cooldown rule + cooled-down families list + memo
  template;
- Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant;
- Phase 4bb-F canonical path policy.

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bl-D-S1 merge does **not**, and cannot be construed
as authorising:

- modification, normalization, replacement, or rewrite of the
  Phase 4az 2025-01-15 sidecar;
- any `data/microstructure/` write or modification;
- the Phase 4bl-D-S2 controlled sidecar canonicalization
  execution phase;
- the Phase 4bl-D-R gate rerun;
- Phase 4bl-E multi-day raw successor-state recording;
- successor-state recording for any other family;
- v002 raw manifest mutation, including any
  `research_eligible` flip, `eligibility_gate_status`
  transition, or governance-label change;
- v002 acquisition log mutation;
- any prior gate report, normalized parquet, feature parquet,
  label parquet, derived manifest, feature manifest, label
  manifest, sidecar, successor-state, diagnostic, or split
  artefact modification;
- normalization, derived parquet, features, labels, label
  diagnostics, label statistics, ML, strategy, signals, or
  backtest work;
- additional aggTrades / 5m / 1m / tick / mark-price 30m /
  4h / order-book / spot / cross-venue / funding /
  open-interest data acquisition;
- paper / shadow / live-readiness / deployment / exchange-write
  / production-key creation / authenticated APIs / private
  endpoints / public-endpoint calls in code / user stream /
  live WebSocket implementation;
- MCP / Graphify / `.mcp.json` / credentials;
- flipping `research_eligible` on any actual manifest;
- transitioning `eligibility_gate_status` on any actual
  manifest;
- changing `chronological_split_policy` on any actual
  manifest;
- amending Phase 4bb-F canonical path policy;
- amending the Phase 4bl-D gate;
- old-strategy alt-symbol rerun or cooled-down-family
  reopening (R2 / F1 / D1-A / V2 / G1 / C1 first-spec
  rejections remain terminal; the 5m research thread remains
  operationally closed per Phase 3t);
- transitioning any manifest state from this docs-only
  governance memo alone;
- Phase 4 canonical;
- Phase 5;
- any other successor phase.

## 15. Successor authorization

**None.**

Phase 4bl-D-S1 does **not** authorize any successor phase. The
natural conditional successor chain implied by the
recommendation (Option B1) requires three separately authorized
operator prompts and is **NOT** authorized by this merge:

- **Phase 4bl-D-S2 — Sidecar Canonicalization Execution**
  (NOT authorized): would perform the controlled CRLF → LF
  normalization of the Phase 4az 2025-01-15 sidecar exactly
  under the binding requirements predeclared in §7 of the
  Phase 4bl-D-S1 memo (preserve raw zip byte-identically;
  preserve embedded SHA256 byte-identically; change only line
  terminator from CRLF to LF; record pre/post sidecar SHA256,
  size, line-ending, byte delta, raw-zip SHA256, manifest SHA,
  log SHA, and gate-report SHA; no v002 manifest mutation; no
  successor authorization).
- **Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun** (NOT authorized): would re-run the Phase 4bl-D
  33-check gate against the Phase 4bl-D-S2-canonicalized
  sidecar and the unchanged Phase 4bl-C raw fileset. PASS is
  likely but not guaranteed.
- **Phase 4bl-E — Multi-Day Raw Manifest Successor-State
  Recording** (NOT authorized): would record a sibling
  successor-state JSON only after Phase 4bl-D-R produces PASS,
  per the Phase 4bb-G raw-family successor-state precedent.

Also **NOT** authorized:

- Phase 4bm-* (multi-day derived arc);
- Phase 4bn-* (multi-day feature arc);
- Phase 4bo-* (multi-day label arc);
- Phase 4bp-* (multi-day diagnostics);
- Phase 4bq-* (multi-day chronological split);
- Phase 5;
- Phase 4 canonical;
- paper / shadow / live-readiness / deployment / production
  keys / authenticated APIs / private endpoints / user stream
  / live WebSocket implementation / MCP / Graphify /
  `.mcp.json` / credentials / exchange-write;
- additional aggTrades / 5m / 1m / tick / mark-price 30m /
  4h / order-book / spot / cross-venue / funding /
  open-interest data acquisition;
- ML implementation, ML training, model selection, feature
  ranking, meta-labeling, strategy implementation, backtest
  implementation.

Each step of the conditional successor chain requires a
separately authorized operator prompt. Phase 4bl-D-S1 makes no
claim about expected execution sequencing beyond recording the
recommended policy and the binding requirements for each future
step.

## 16. Recommended state

**Remain paused.**

The Phase 4bl-D `RAW_MULTIDAY_GATE_FAIL` is preserved as
descriptive research evidence on `main`. The Phase 4bl-D-S1
governance memo's Option B1 recommendation is now recorded on
`main` as the cleanest practical remediation path. No
remediation has been authorized. No execution has occurred.

**Conditional next, NOT authorized:** A future separately
authorized Phase 4bl-D-S2 controlled sidecar canonicalization
execution phase would be the cleanest non-paused option. Per
the Phase 4bk-A workflow standard, a separately authorized
operator prompt is required before any Phase 4bl-D-S2 work may
begin; before any Phase 4bl-D-R gate rerun; and before any
Phase 4bl-E successor-state recording. Phase 4bl-D-S1 does
**not** authorize any of these.

Push status (recorded after merge-closeout commit is committed
and pushed): pushed to `origin/main` with no force, no
skip-hooks, no skip-signing.
