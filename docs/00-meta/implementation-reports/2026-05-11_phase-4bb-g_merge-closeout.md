# Phase 4bb-G — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bb-G — Raw Manifest Successor-State Recording
- **Type:** Docs + local gitignored successor-state artefact recording
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bb-G from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bb-G recorded exactly one sibling raw-family successor-state
  JSON artefact for `microstructure_raw_aggtrades_v001` under the
  gitignored `data/microstructure/successor-state/` namespace (plus a
  paired SHA256 sidecar), completing raw-family governance symmetry
  with the derived (Phase 4bg-B), feature (Phase 4bi-D), and label
  (Phase 4bj-G) successor-state artefacts. The merge brings forward
  the Phase 4bb-G implementation memo, closeout, and narrow
  `current-project-state.md` update. No data file is committed; the
  successor-state JSON and sidecar live locally under the gitignored
  namespace.
- **Target branch:** `main`
- **Source branch:** `phase-4bb-g/raw-manifest-successor-state-recording`

## 2. SHAs

- **`main` SHA before merge:** `07d6ea7c612abbdde370b131af541a9a4c37b969`
  (Phase 4bb-F-implementation SHA-chain-fixup commit on top of the
  Phase 4bb-F-implementation merge-closeout `b1c49a12fd931a64e9c7d46821739432acd94479`).
- **Phase 4bb-G branch commit SHA:** `e101215d1a8763dea31523346aa3747c954d11a4`
  (`docs(phase-4bb-g): record raw-family successor-state artefact`).
- **Merge commit SHA:** `6d14d864a0ac233f19e7ab33116cdae69d2b1c71`.
- **Merge-closeout commit SHA:** (recorded below once committed and
  pushed).
- **Final `main` / `origin/main` SHA after push:** (recorded below
  once the merge-closeout commit is pushed; a one-commit
  SHA-chain-fixup may follow to record the final SHA into §2 of this
  merge-closeout, consistent with Phase 4bb-F /
  Phase 4bb-F-implementation / Phase 4bj-G precedents).

## 3. Merge method

- Command: `git merge --no-ff phase-4bb-g/raw-manifest-successor-state-recording`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bb-g): merge raw-family
  successor-state recording`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-g_raw-manifest-successor-state-recording.md`
  (the 15-section Phase 4bb-G implementation memo)
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bb-g_closeout.md`
  (the 12-section Phase 4bb-G closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bb-G narrative
  paragraph; new "Current phase:" Phase 4bb-G block; prior
  Phase 4bb-F-implementation "Current phase:" block preserved as
  historical context per the documented standard)

### Source

- None.

### Tests

- None.

### Scripts

- None.

### Config

- None.

### `data/microstructure/`

- **No `data/microstructure/` file was committed by the merge.**
- The Phase 4bb-G local artefacts (the new sibling raw successor-state
  JSON + sidecar) live under `data/microstructure/successor-state/`
  and remain gitignored under `.gitignore:85: data/microstructure/`.
  See §7 for the artefact inventory.

### Prior governance memos

- No prior governance memo was modified beyond the narrow
  `current-project-state.md` paragraph addition.

### Prior source / test / script

- No prior source, test, or script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              | 319 ++++++++++++++++++++
 .../2026-05-11_phase-4bb-g_closeout.md             | 157 ++++++++++
 ...4bb-g_raw-manifest-successor-state-recording.md | 327 +++++++++++++++++++++
 3 files changed, 803 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bb-G memo + Phase 4bb-G closeout + narrow
`current-project-state.md` update. No source / test / script /
config / `data/microstructure/` files were modified.

## 6. Verdict

**LOCAL ARTEFACT PRODUCED.**

Phase 4bb-G is project-complete after this merge and the
merge-closeout commit. The new sibling raw-family successor-state
JSON artefact (`microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`,
SHA256 `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`,
12,726 bytes) and its paired SHA256 sidecar live locally under the
gitignored `data/microstructure/successor-state/` namespace and were
NOT committed. The artefact records raw-family policy-level
**structural-integrity admissibility only** (Stage-2 marker;
`successor_research_eligible=false`; `raw_family_use_admissible=true`;
`raw_family_research_use_admissible="conditional_future_only"`;
`raw_family_ml_use_admissible=false`). The original raw manifest at
`data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`
remains `research_eligible: false` and `eligibility_gate_status:
pending` — the raw manifest was not modified, and the raw-family
admissibility marker exists **only** in the sibling successor-state
JSON. All six upstream raw-family artefacts (raw manifest, raw zip,
raw zip sidecar, acquisition log, Phase 4bb-D gate report + sidecar)
are byte-for-byte unchanged pre/post. The Phase 4bb-D doubled-path
gate report remains valid at its recorded historical path; it was
not migrated, copied, renamed, or rewritten. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant was preserved (never invoked). No ML, label evaluation,
strategy, signal, backtest, acquisition, paper / shadow,
live-readiness, deployment, exchange-write, production-key,
authenticated-API, private-endpoint, user-stream, MCP, Graphify,
`.mcp.json`, or credential work was authorized or performed.
Recommended state remains **paused**.

## 7. Local gitignored outputs (if any)

Two local artefacts produced by Phase 4bb-G (NOT committed):

### Successor-state JSON

- **Path:** `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`
- **Size:** 12,726 bytes
- **SHA256:** `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`
- **Status:** not committed; gitignored under `.gitignore:85: data/microstructure/`
- **`git check-ignore -v`:** `.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`
- **Predecessor / source references:** raw manifest
  (`a371edd4…`), raw zip (`f560c2e5…`), raw zip sidecar (`b80c2768…`),
  acquisition log (`f88b28b4…`), Phase 4bb-D gate report (`96f09159…`),
  Phase 4bb-D gate report sidecar (`93e68eb6…`).

### Paired SHA256 sidecar

- **Path:** `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`
- **Size:** 147 bytes (= 64 hex chars + 2 spaces + 80-char basename + 1 newline)
- **SHA256:** `8ed0fbc0c31bc7f228ccfb35b92968f99dbbef06ef6b0d07621b14baeb41ef46`
- **Body format:** `<json-sha256>  <basename>\n` (two spaces, trailing newline; canonical `sha256sum` format)
- **Status:** not committed; gitignored under `.gitignore:85: data/microstructure/`
- **`git check-ignore -v`:** `.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`
- **Integrity:** the SHA token parsed from the sidecar body matches
  the recomputed JSON SHA256 bit-for-bit.

The Phase 4bb-G implementation memo and earlier closeout state the
sidecar size as 158 bytes; the actual on-disk size is 147 bytes. The
SHA256 (`8ed0fbc0…`) matches the recorded value exactly and the
sidecar parses correctly, so the integrity-critical fact is
unchanged; the size note in the earlier memo is a transcription
inaccuracy and is corrected here.

## 8. Validation results

- `git diff --check`: **clean** (no whitespace errors).
- `git status` (post-merge, pre-merge-closeout):
  ```text
  On branch main
  Your branch is ahead of 'origin/main' by 2 commits.
  Untracked files:
    .claude/scheduled_tasks.lock
    data/research/
  nothing added to commit but untracked files present
  ```
- `git check-ignore -v data/microstructure/`: `.gitignore:85:data/microstructure/	data/microstructure/`
- `git check-ignore -v data/microstructure/successor-state/`: `.gitignore:85:data/microstructure/	data/microstructure/successor-state/`
- `git check-ignore -v data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`: `.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`
- `git check-ignore -v data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`: `.gitignore:85:data/microstructure/	data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`
- SHA256 recomputation: see §9 (upstream immutability evidence).
- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bb-G modifies no
  source code, no tests, no scripts, no `pyproject.toml`, no
  `README.md`, and no `.gitignore`. The latest authoritative
  whole-repo validation is the Phase 4bb-F-implementation merge:
    - `ruff check .` PASS,
    - `mypy src/prometheus` (strict) Success on 120 source files,
    - `pytest tests/research/microstructure/` 915 passed, 1 skipped
      (pre-existing labelled placeholder),
    - `pytest` (whole repo) 1698 passed, 1 skipped, 2 failed
      (the same pre-existing simulation `KeyError: 'trade_count'`
      failures in `tests/simulation/test_backtest_real_2026_03.py`;
      unchanged from prior phases; not introduced by this merge).

## 9. Upstream immutability evidence (if applicable)

All six upstream raw-family artefacts and both new Phase 4bb-G local
artefacts byte-for-byte identical pre / post merge:

| Artefact | Pre-merge SHA256 | Post-merge SHA256 | Identical? |
| --- | --- | --- | --- |
| Raw manifest (`microstructure_raw_aggtrades_v001__v001.json`) | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` | **IDENTICAL** |
| Raw zip (`BTCUSDT-aggTrades-2025-01-15.zip`) | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` | **IDENTICAL** |
| Raw zip sidecar (`BTCUSDT-aggTrades-2025-01-15.zip.sha256`) | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` | **IDENTICAL** |
| Acquisition log (`microstructure_raw_aggtrades_v001__v001_acquisition_log.json`) | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` | **IDENTICAL** |
| Phase 4bb-D gate report (at doubled `gate-reports/gate-reports/` path) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` | **IDENTICAL** |
| Phase 4bb-D gate report sidecar | `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8` | `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8` | **IDENTICAL** |
| Phase 4bb-G successor-state JSON (new) | `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452` | `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452` | **IDENTICAL** |
| Phase 4bb-G successor-state sidecar (new) | `8ed0fbc0c31bc7f228ccfb35b92968f99dbbef06ef6b0d07621b14baeb41ef46` | `8ed0fbc0c31bc7f228ccfb35b92968f99dbbef06ef6b0d07621b14baeb41ef46` | **IDENTICAL** |

The Phase 4bb-D doubled-path gate report remains valid at its
recorded historical path:
`data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`.
It was not migrated, copied, renamed, deleted, or rewritten.

`mtime_ns` also unchanged for the raw manifest, raw zip, and
Phase 4bb-D gate report (verified during Phase 4bb-G branch work and
preserved across the merge).

## 10. Manifest state preservation (if applicable)

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Governance labels |
| --- | --- | --- | --- | --- |
| Raw aggTrades (`microstructure_raw_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Derived normalized aggTrades (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Feature aggTrades (`microstructure_features_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Label aggTrades (`microstructure_labels_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | unchanged |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant **preserved (never invoked)** by Phase 4bb-G
or by the merge.

The raw-family admissibility marker recorded by Phase 4bb-G exists
**only** at the sibling successor-state JSON. The raw manifest's
`research_eligible` field remains `false` and **must remain `false`
permanently** per the raw-family governance rule (the raw family is
permanently capped at Stage-2 — gate-passed at report level only;
Stage-3 is not reachable for the raw family by design).

## 11. Boundary confirmations

- No source code modified.
- No test modified.
- No script modified.
- No `pyproject.toml` modified.
- No `README.md` modified.
- No `.gitignore` modified.
- No MCP file modified.
- No prior governance memo modified (beyond the narrow
  `current-project-state.md` paragraph addition).
- No `data/microstructure/` file committed.
- No `data/microstructure/` file outside the gitignored successor-state
  pair created.
- No raw manifest modified.
- No raw zip modified.
- No raw zip sidecar modified.
- No acquisition log modified.
- No Phase 4bb-D gate report modified.
- No Phase 4bb-D gate report sidecar modified.
- No Phase 4bb-D doubled-path gate report migrated, copied, renamed,
  deleted, or rewritten.
- No derived parquet, feature parquet, label parquet, or any other
  derived data file modified.
- No derived manifest, feature manifest, or label manifest modified.
- No prior gate report (Phase 4bf / 4bi-B / 4bj-E) modified.
- No prior successor-state artefact (Phase 4bg-B / 4bi-D / 4bj-G)
  modified.
- No raw / derived-family / feature-family / label-family eligibility
  gate rerun.
- No new gate report created.
- No new manifest created.
- No `research_eligible` flipped on any actual manifest.
- No `eligibility_gate_status` transitioned on any actual manifest.
- No `chronological_split_policy` changed on any actual manifest.
- No ML model trained.
- No ML architecture designed.
- No feature ranked.
- No meta-labeling created.
- No label evaluated.
- No strategy created.
- No signal computed.
- No backtest run.
- No PnL / MFE / MAE / R-multiple / equity / position / alpha / edge /
  prediction / model-score / decision-score / entry-exit / strategy
  output computed.
- No data acquired.
- No public endpoint called.
- No Binance API called.
- No authenticated API called.
- No private endpoint called.
- No user stream used.
- No WebSocket opened.
- No credential created or read.
- No `.env` created or modified.
- No `.mcp.json` created or read.
- No MCP enabled.
- No Graphify enabled.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No successor authorized.

## 12. Retained verdict ledger

All preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED (per Phase 3t)
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

## 13. Preserved project locks

All preserved verbatim:

- §11.6 = 8 bps per side
- round-trip = 16 bps
- §1.7.3 = 0.25% / 2× / one-position / mark-price stops
- Phase 3p §4.7 strict integrity gate
- Phase 3r §8 mark-price gap governance
- Phase 3v §8 stop-trigger-domain governance
- Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance
- Phase 4j §11 metrics OI-subset partial-eligibility rule
- Phase 4k V2 backtest-plan methodology
- Phase 4p G1 strategy-spec
- Phase 4q G1 backtest-plan methodology
- Phase 4v C1 strategy-spec
- Phase 4w C1 backtest-plan methodology
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule +
  cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant
- Phase 4bb-F canonical path policy (raw → `gate-reports/raw/`,
  normalized → `gate-reports/normalized/`, features →
  `gate-reports/features/`, labels → `gate-reports/labels/`,
  successor-state → flat under `successor-state/`)

All prior phase results preserved verbatim.

## 14. No-rescue constraints

The Phase 4bb-G merge does NOT, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis generation,
  or any conversion of labels / features / OI / funding context /
  derivatives flow into signals;
- strategy signal construction, strategy logic, position state, entry
  / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- transitioning the raw manifest's `research_eligible` from `false` to
  `true` (the raw family is permanently capped at Stage-2);
- transitioning any manifest's `eligibility_gate_status` from
  `pending` to `pass` or `fail` on the basis of this successor-state
  artefact alone;
- transitioning the label manifest's `chronological_split_policy` from
  `"not_yet_defined"` to any value on the basis of this
  successor-state artefact alone;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- migration, copy, rename, deletion, or rewriting of the Phase 4bb-D
  doubled-path raw gate report;
- broadening Phase 4bb-G results into binding cross-project governance
  (the successor-state artefact records raw-family policy-level
  structural-integrity admissibility only; it is not strategy
  evidence, not ML approval, and not live-readiness evidence);
- any rescue of R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread;
- creation of R3-prime / R1a-prime / R1b-narrow-prime / R2-prime /
  H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow /
  V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension /
  G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid /
  V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bb-G reasoning.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

- Phase 4bb-H (any future hypothetical raw-family follow-up)
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book /
  spot / cross-venue data acquisition
- new gate-report generation (raw / derived / feature / label)
- new manifest creation
- migration / copy / rename of the Phase 4bb-D doubled-path raw gate
  report
- label evaluation
- ML implementation
- ML training
- model selection
- feature ranking
- meta-labeling
- strategy implementation
- backtest implementation
- signal computation
- PnL / MFE / MAE / R-multiple / equity / position / alpha / edge /
  prediction / model-score / decision-score / entry-exit / strategy
  output computation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- public-endpoint calls in code
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials

## 16. Recommended state

**Remain paused.**

Phase 4bb-G is now project-complete on `main` after this merge and
the merge-closeout commit. The raw-family governance symmetry with
the derived (Phase 4bg-B), feature (Phase 4bi-D), and label
(Phase 4bj-G) successor-state artefacts is complete: every dataset
family in the microstructure aggTrades lineage now has a
machine-readable sibling successor-state marker recorded as a
gitignored JSON artefact, while the original manifests remain
byte-identical and `research_eligible: false / eligibility_gate_status:
pending`. No successor phase is authorized. Per the operator's
instruction, the project remains paused; any future phase requires
a separately authorized prompt that satisfies the Phase 4bk-A
workflow standard, the Phase 4ak M0 twelve-clause gate, and the
Phase 4al refined no-rescue rule.

**Conditional next, NOT authorized:** there is no current
conditional-next candidate. Any future phase — including but not
limited to label evaluation, ML, strategy, backtest, acquisition,
paper / shadow, live-readiness, deployment, exchange-write — would
require a separately authorized prompt and would have to pass the M0
admissibility gate, the post-null cooldown rule, and the refined
no-rescue rule. None of these is authorized here.
