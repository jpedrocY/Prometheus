# Phase 4bl-A — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-A — Multi-Day aggTrades Expansion Requirements Memo
- **Type:** docs-only requirements / scope / governance memo
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bl-A from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bl-A authored a docs-only requirements / scope / governance
  memo defining what a future multi-day aggTrades data expansion
  would require before label diagnostics, split policy, ML
  feasibility, or strategy work could become meaningful. The memo
  evaluates seven candidate scopes (A — remain paused; B —
  BTCUSDT-only 30 UTC days; C — BTCUSDT-only 60–90 UTC days; D —
  BTCUSDT + ETHUSDT 30 UTC days; E — BTCUSDT + ETHUSDT + alts 30
  UTC days; F — order-book / mark-price / funding / OI / spot /
  cross-venue expansion; G — ML / strategy / backtest now),
  recommends Option B as the minimum viable expansion with Option
  C as the preferred upper bound, defines date-range / regime
  coverage requirements, symbol-scope requirements, data-source
  requirements, storage / namespace requirements (preserving the
  Phase 4bb-F canonical path policy), raw acquisition requirements,
  repeat pipeline requirements, multi-day manifest / indexing
  requirements, multi-day split policy implications, minimum future
  diagnostic eligibility, relationship to the current one-day cell,
  decision options, the future phase ladder, M0 and no-rescue
  integration, and explicit non-authorizations. The merge brings
  forward the Phase 4bl-A implementation report, closeout, and
  narrow `current-project-state.md` update. No data file is
  committed; no manifest is mutated; no successor phase is
  authorized.
- **Target branch:** `main`
- **Source branch:** `phase-4bl-a/multi-day-aggtrades-expansion-requirements-memo`

## 2. SHAs

- **`main` SHA before merge:** `c120450b87918d104474e6d1bb88b6fa30132f34`
  (Phase 4bj-K SHA-chain-fixup commit on top of the Phase 4bj-K
  merge-closeout `0074f696d5f4e9bd7fccf665d6742c77af2edaa2`).
- **Phase 4bl-A branch commit SHA:** `f2726c2b5561363531e0988196848c9b9ec9c0f2`
  (`docs(phase-4bl-a): multi-day aggtrades expansion requirements memo`).
- **Merge commit SHA:** `faffb40c1d1c4d6c3acb3392224ff701a72ebd78`.
- **Merge-closeout commit SHA:** (recorded below once committed and
  pushed).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bl-A is the merge-closeout
  commit recorded in this section once committed and pushed. A
  subsequent one-commit SHA-chain-fixup on top of that anchor (if
  applied) only records the final-`main` SHA value back into this
  section; it does not change Phase 4bl-A lifecycle semantics,
  consistent with the Phase 4bb-G / Phase 4bb-F-implementation /
  Phase 4bb-F / Phase 4bj-G / Phase 4bj-F / Phase 4bj-H / Phase
  4bj-I / Phase 4bj-J / Phase 4bj-K SHA-chain-fixup precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bl-a/multi-day-aggtrades-expansion-requirements-memo`
- Strategy: `ort` (the default).
- Merge commit message:
  `docs(phase-4bl-a): merge multi-day aggtrades expansion requirements memo`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-a_multi-day-aggtrades-expansion-requirements-memo.md`
  (the Phase 4bl-A main memo)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-a_closeout.md`
  (the Phase 4bl-A closeout)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bl-A narrative
  paragraph prepended above the Phase 4bj-K paragraph; new "Current
  phase:" Phase 4bl-A block; prior Phase 4bj-K "Current phase:"
  block preserved as historical context per the documented
  standard)

### Source / tests / scripts / config

- None.

### `data/microstructure/`

- **No `data/microstructure/` file was modified, created, moved,
  copied, renamed, or deleted by the merge.** All raw / derived /
  feature / label parquets, manifests, sidecars, gate reports, and
  successor-state artefacts (including the Phase 4bj-J no-split
  determination JSON and its paired `.sha256` sidecar) remain
  byte-for-byte unchanged at their recorded paths and SHAs. Phase
  4bl-A is docs-only; it produces no local artefact under
  `data/microstructure/`.

### Prior governance memos

- No prior governance memo was modified beyond the narrow
  `current-project-state.md` paragraph addition.

### Prior source / test / script

- No prior source, test, or script was modified.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  470 ++++++++
 .../2026-05-12_phase-4bl-a_closeout.md             |   94 ++
 ...ti-day-aggtrades-expansion-requirements-memo.md | 1241 ++++++++++++++++++++
 3 files changed, 1805 insertions(+)
```

The diff matches the expected change set from the authorization
prompt exactly: Phase 4bl-A main memo + Phase 4bl-A closeout +
narrow `current-project-state.md` update. No source / test /
script / config / `data/microstructure/` files were modified.

## 6. Verdict

**MEMO RECORDED.**

Phase 4bl-A is project-complete after this merge and the
merge-closeout commit. The phase records a docs-only requirements /
scope / governance memo for a future multi-day aggTrades data
expansion. The memo:

- evaluates seven candidate scopes (Option A — remain paused;
  Option B — BTCUSDT-only, 30 UTC days; Option C — BTCUSDT-only,
  60–90 UTC days; Option D — BTCUSDT + ETHUSDT, 30 UTC days;
  Option E — BTCUSDT + ETHUSDT + alts, 30 UTC days; Option F —
  order-book / mark-price / funding / OI / spot / cross-venue
  expansion; Option G — ML / strategy / backtest now);
- recommends **Option B (BTCUSDT-only, at least 30 distinct UTC
  days of public USDⓈ-M Futures aggTrades) as the minimum viable
  first expansion**;
- records **Option C (BTCUSDT-only, 60–90 distinct UTC days) as
  the preferred upper bound** if storage / runtime permit;
- rejects immediate ETHUSDT / alt-symbol expansion (Options D / E)
  for the first expansion;
- rejects order-book / mark-price / spot / cross-venue / funding /
  OI expansion (Option F) for the first expansion;
- rejects ML / strategy / backtest now (Option G) as **FORBIDDEN**;
- defines date-range / regime coverage requirements (contiguous
  preferred; minimum 30 distinct UTC days; multi-weekday + weekend
  coverage; deterministic predeclared date list before any
  download; no post-hoc date selection; missing-file explicit
  recording per Phase 4ay §10 strict integrity gate);
- defines symbol-scope requirements (BTCUSDT mandatory first;
  ETHUSDT likely second later; alts much later under separate
  authorization; no cross-symbol generalisation claims from few
  symbols; no alt-symbol rescue of failed strategy families);
- defines data-source requirements (public daily aggTrades archive
  only via `data.binance.vision`; no authenticated APIs; no
  private endpoints; no user streams; no WebSockets; no production
  keys; no credentials; no `.env`; no `.mcp.json`; no public
  endpoint calls during Phase 4bl-A);
- defines storage / namespace requirements (preserving the Phase
  4bb-F canonical path policy; raw zips, raw manifests, acquisition
  logs, normalized parquets, derived manifests, feature parquets,
  feature manifests, label parquets, label manifests, gate reports
  under `gate-reports/<family-subdir>/`, successor-state under
  flat `successor-state/`, diagnostics under `diagnostics/labels/`,
  split artefacts under `successor-state/`, all gitignored under
  `.gitignore:85: data/microstructure/`, paired `.sha256` sidecars
  in canonical Phase 4bb-F format; no mutation of historical
  one-day artefacts);
- defines raw acquisition requirements (predeclared symbols /
  date list / source URL / hash rules / sidecar format /
  acquisition log schema / failure-retry-missing-file policy / no
  partial silent success);
- defines repeat pipeline requirements (multi-day expansion is not
  "download more data"; it requires Phase 4bl-C / 4bl-D / 4bl-E /
  4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* equivalents, each
  separately authorized);
- defines multi-day manifest / indexing requirements;
- defines multi-day split policy implications (train / validation
  / test vocabulary becomes admissible **only after** multi-day
  data exists; strictly chronological; no random split; uniform
  60s purge / embargo at the maximum label horizon — Phase 4bj-I
  §5 preserved; walk-forward acceptable; no symbol-leakage
  claims);
- defines minimum future diagnostic eligibility;
- records the relationship to the current one-day cell (preserved
  as pipeline-proving fixture; not research-grade for ML or
  strategy; inclusion / exclusion decision deferred to future
  Phase 4bl-B-equivalent acquisition design memo);
- records decision options and primary recommendation;
- defines the future phase ladder (Phase 4bl-B / 4bl-C / 4bl-D /
  4bl-E / 4bm-* / 4bn-* / 4bo-* / 4bp-* / 4bq-* / later ML
  feasibility / baseline ML diagnostic / failure interpretation /
  strategy hypothesis under M0 / strategy spec / backtest plan /
  backtest execution / paper / shadow / live), all marked NOT
  authorized;
- records M0 and no-rescue integration (data expansion is
  upstream of label diagnostics; label diagnostics are upstream
  of ML feasibility; ML diagnostics are upstream of M0 strategy
  admission; data expansion does not bypass M0; more data does
  not rescue failed strategy families; labels and features remain
  not signals; old failed strategy families remain closed; 5m
  thread remains operationally closed);
- enumerates explicit non-authorizations.

Phase 4bl-A does **not**: acquire data; download files; call
public endpoints; call Binance APIs; call authenticated APIs;
call private endpoints; open user streams or WebSockets; create
or read credentials, `.env`, or `.mcp.json`; enable MCP or
Graphify; create raw / manifest / sidecar / gate-report /
successor-state / normalized / derived / feature / label / split
/ diagnostic artefacts; modify any existing local artefact; run
any kernel, normalizer, or gate; compute label statistics;
execute diagnostics; train ML; design ML architecture; rank
features; create meta-labeling; create a strategy; compute
signals; run backtests; compute PnL / MFE / MAE / R-multiple /
equity / position / alpha / edge / prediction / model-score /
decision-score / entry-exit / strategy output; modify source
code, tests, scripts, configs, `pyproject.toml`, `README.md`,
`.gitignore`, MCP files, or any prior governance memo beyond
the narrow `current-project-state.md` update; flip
`research_eligible` on any actual manifest; transition
`eligibility_gate_status` on any actual manifest; change
`chronological_split_policy` on any actual manifest; revise any
retained verdict; change any project lock; amend M0; or
authorize Phase 4bl-B / 4bl-C / 4bl-D / 4bl-E / 4bm-* / 4bn-* /
4bo-* / 4bp-* / 4bq-* / Phase 5 / Phase 4 canonical / paper /
shadow / live-readiness / deployment / exchange-write /
production-key creation / authenticated APIs / private endpoints
/ user stream / live WebSocket implementation.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. The Phase 4bj-J Option D no-split
determination remains encoded ONLY in the Phase 4bj-J sibling
JSON at the gitignored path
`data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__split_policy__phase-4bj-j.json`;
Phase 4bl-A does not write to that artefact, does not duplicate
it, and does not broaden its scope. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant was preserved (never invoked). Recommended state remains
**paused**.

## 7. Local gitignored outputs (if any)

**None.**

Phase 4bl-A is docs-only and produced no local artefact under
`data/microstructure/`. The Phase 4bj-J no-split determination
JSON and its paired `.sha256` sidecar remain at their recorded
gitignored paths (SHA256
`7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`
for the JSON and
`9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8`
for the sidecar), byte-identical pre/post-merge. They remain
local gitignored output only; the merge does not touch them.

## 8. Validation results

- `git diff --check` (post-merge): **clean** (no whitespace errors).
- `git status` (post-merge, pre-merge-closeout):

  ```text
  On branch main
  Your branch is ahead of 'origin/main' by 1 commits.
  Untracked files:
    .claude/scheduled_tasks.lock
    data/research/
  nothing added to commit but untracked files present
  ```

- `ruff` / `mypy` / `pytest`: **not rerun**. Phase 4bl-A modifies
  no source code, no tests, no scripts, no `pyproject.toml`, no
  `README.md`, and no `.gitignore`. The latest authoritative
  whole-repo validation remains the Phase 4bb-F-implementation
  merge: `ruff check .` PASS, `mypy src/prometheus` (strict)
  Success on 120 source files, `pytest tests/research/microstructure/`
  915 passed + 1 skipped (pre-existing labelled placeholder),
  `pytest` (whole repo) 1698 passed + 1 skipped + 2 failed (the
  same pre-existing simulation `KeyError: 'trade_count'` failures
  in `tests/simulation/test_backtest_real_2026_03.py`; unchanged
  from prior phases; not introduced by this merge).

## 9. Upstream immutability evidence (if applicable)

For every prior `data/microstructure/` artefact, pre-merge vs
post-merge SHA256 is IDENTICAL:

| Artefact | SHA256 |
| --- | --- |
| Raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| Raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Raw zip sidecar | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| Acquisition log | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` |
| Phase 4bb-D raw gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bb-D raw gate report sidecar | `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8` |
| Phase 4bb-G raw successor-state | `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452` |
| Normalized parquet | `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` |
| Original derived manifest | `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9` |
| Phase 4bf derived gate report | `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6` |
| Phase 4bg-B derived successor-state | `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e` |
| Feature parquet | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| Phase 4bi-B feature gate report | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Phase 4bi-D feature successor-state | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| Label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` |
| Label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` |
| Phase 4bj-E label gate report | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| Phase 4bj-G label successor-state | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |
| Phase 4bj-J no-split determination JSON | `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6` |
| Phase 4bj-J no-split determination sidecar | `9014c5d0c4f0bb4a74b83fff11aa95315f26816cd45fd2ccdd92047c9f4b6af8` |

All twenty-three prior artefacts byte-for-byte unchanged across
the merge. Phase 4bl-A produces no new local artefact under
`data/microstructure/`. The Phase 4bb-D doubled-path gate report
remains valid at its recorded historical path; it was not
migrated, copied, renamed, deleted, or rewritten.

## 10. Manifest state preservation (if applicable)

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Governance labels |
| --- | --- | --- | --- | --- |
| Raw aggTrades (`microstructure_raw_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Derived normalized aggTrades (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Feature aggTrades (`microstructure_features_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | n/a | unchanged |
| Label aggTrades (`microstructure_labels_aggtrades_v001__v001.json`) | `false` (unchanged) | `"pending"` (unchanged) | `"not_yet_defined"` (unchanged) | unchanged |

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant **preserved (never invoked)** by Phase
4bl-A or by the merge.

The label manifest's `chronological_split_policy` remains
`"not_yet_defined"`. Phase 4bl-A explicitly **does not** mutate
this field on the original manifest. The Phase 4bj-J Option D
no-split determination remains encoded ONLY in the Phase 4bj-J
sibling JSON.

## 11. Boundary confirmations

- No source code modified.
- No test modified.
- No script modified.
- No `pyproject.toml` modified.
- No `README.md` modified.
- No `.gitignore` modified.
- No MCP file modified.
- No prior governance memo modified (beyond the narrow
  `current-project-state.md` paragraph addition + Current-phase
  block update).
- No `data/microstructure/` file modified, created, moved, copied,
  renamed, or deleted by the merge.
- No `data/microstructure/` file committed.
- No data acquired.
- No file downloaded.
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
- No raw artefact created.
- No new manifest created.
- No new gate report created.
- No new successor-state artefact created.
- No normalized / derived artefact created.
- No feature artefact created.
- No label artefact created.
- No split artefact created.
- No segmentation artefact created.
- No diagnostic artefact created.
- No raw / derived / feature / label eligibility gate rerun.
- No normalizer, kernel, or processing script run.
- No label parquet read for computation, modification, or
  recomputation.
- No label statistics computed.
- No diagnostic execution.
- No ML model trained.
- No ML architecture designed.
- No feature ranked.
- No meta-labeling created.
- No strategy created.
- No signal computed.
- No backtest run.
- No PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output computed.
- No `research_eligible` flipped on any actual manifest.
- No `eligibility_gate_status` transitioned on any actual manifest.
- No `chronological_split_policy` changed on any actual manifest
  (label manifest remains `"not_yet_defined"`).
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).
- No retained verdict revised.
- No project lock changed.
- No M0 amendment.
- No successor phase authorized.

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

The Phase 4bl-A merge does NOT, and cannot, be construed as
authorising:

- any data acquisition, download, or public endpoint call (the
  memo records the requirements for a future acquisition phase;
  it does not authorize the acquisition);
- any Binance API call, authenticated API call, private endpoint
  call, user stream, WebSocket, or listenKey lifecycle;
- creation or use of any credential, `.env`, `.mcp.json`, MCP, or
  Graphify;
- creation of any raw / manifest / sidecar / gate-report /
  successor-state / normalized / derived / feature / label /
  split / segmentation / diagnostic artefact;
- mutation of any existing local artefact;
- any kernel, normalizer, or gate execution;
- label statistics computation, diagnostic execution, or any
  reading of the label parquet for analysis;
- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels / features into trading
  signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- transitioning any manifest's `research_eligible` from `false`
  to `true`;
- transitioning any manifest's `eligibility_gate_status` from
  `pending` to `pass` or `fail`;
- mutating the label manifest's `chronological_split_policy`
  from `"not_yet_defined"` to any value;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- Phase 4 canonical or Phase 5 authorisation;
- Phase 4bl-B (multi-day aggTrades acquisition authorization /
  design memo), Phase 4bl-C (multi-day acquisition execution),
  Phase 4bl-D (multi-day raw QA / raw gate), Phase 4bl-E
  (multi-day raw successor-state), Phase 4bm-* (multi-day
  normalization), Phase 4bn-* (multi-day features), Phase 4bo-*
  (multi-day labels), Phase 4bp-* (multi-day split policy), Phase
  4bq-* (multi-day diagnostics), or any successor in the
  multi-day arc;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades / 5m / 1m / tick / funding / open-interest data
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening
  (R2 cost-fragility, F1 catastrophic floor, D1-A mechanism /
  framework mismatch, V2 design-stage incompatibility, G1
  regime-gate sparseness, C1 fires-and-loses anti-validation —
  all remain terminal for their first specs);
- 5m research-thread reopening (Phase 3t closure preserved);
- any rescue of R2 / F1 / D1-A / V2 / G1 / C1 / 5m thread;
- creation of R3-prime / R1a-prime / R1b-narrow-prime / R2-prime
  / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime /
  V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow /
  G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension
  / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bl-A reasoning;
- broadening Phase 4bl-A requirements language into binding
  cross-project governance beyond its docs-only scope.

## 15. Successor authorization

**None.**

The following candidate successors are **NOT authorized** by this
merge:

- Phase 4bl-B (or any equivalent Multi-Day aggTrades Acquisition
  Authorization / Design Memo)
- Phase 4bl-C (or any equivalent Multi-Day Public Archive
  Acquisition Execution)
- Phase 4bl-D (or any equivalent Multi-Day Raw Artefact QA / Raw
  Gate)
- Phase 4bl-E (or any equivalent Multi-Day Raw Successor-State
  Recording)
- Phase 4bm-* (Multi-Day Normalization / Derived Artefact Arc)
- Phase 4bn-* (Multi-Day Feature Generation / Gate Arc)
- Phase 4bo-* (Multi-Day Label Generation / Gate Arc)
- Phase 4bp-* (Multi-Day Split Policy Design / Artefact
  Recording)
- Phase 4bq-* (Multi-Day Label Diagnostic Plan / Execution)
- any future ML feasibility memo
- any future baseline ML diagnostic
- any future failure-interpretation / fallback-selection memo
- any future strategy hypothesis memo under M0
- any future strategy spec memo
- any future backtest plan memo
- any future backtest execution phase
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book
  / spot / cross-venue / funding / open-interest data acquisition
- ML implementation, ML training, model selection, feature
  ranking, meta-labeling
- strategy implementation, signal computation, backtest
  implementation
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

Phase 4bl-A is now project-complete on `main` after this merge
and the merge-closeout commit. The project record now contains a
docs-only requirements memo for a future multi-day aggTrades
expansion that recommends Option B (BTCUSDT-only, at least 30
distinct UTC days) as the minimum viable first expansion, with
Option C (BTCUSDT-only, 60–90 distinct UTC days) as the preferred
upper bound. The memo defines the date-range, symbol-scope,
data-source, storage / namespace, raw acquisition, repeat
pipeline, manifest, split policy, diagnostic eligibility, and
non-authorization requirements that any future Phase 4bl-B-
equivalent acquisition design memo (and its downstream phases)
would have to satisfy.

The microstructure aggTrades lineage arc remains in its post-
Phase-4bj-K state with respect to artefacts: every dataset family
(raw / derived / feature / label) has a machine-readable sibling
successor-state marker recorded as a gitignored JSON artefact
under `data/microstructure/successor-state/`, every original
manifest remains byte-identical with `research_eligible: false`
and `eligibility_gate_status: "pending"`, the label manifest's
`chronological_split_policy` remains `"not_yet_defined"`, and the
Phase 4bj-J Option D no-split determination remains encoded ONLY
in the Phase 4bj-J sibling JSON. Phase 4bl-A adds no artefact; it
adds a docs-only requirements memo defining what a future
multi-day expansion would have to look like, what it would be
forbidden to do, and what the predeclared requirements would be.
The memo is governance, not execution.

Per the operator's instruction, the project remains paused; any
future phase requires a separately authorized prompt that
satisfies the Phase 4bk-A workflow standard, the Phase 4ak M0
twelve-clause gate, and the Phase 4al refined no-rescue rule.

**Conditional next, NOT authorized:** **Phase 4bl-B — Multi-Day
aggTrades Acquisition Authorization / Design Memo** (docs-only) is
the cleanest non-paused option. It would lock the exact date list
(per Phase 4bl-A §6: contiguous; deterministic; predeclared
before download), the exact symbol list (per Phase 4bl-A §7:
BTCUSDT-only first), the exact source URL pattern (per Phase
4bl-A §8: public `data.binance.vision` archive), the future
local path layout (per Phase 4bl-A §9: Phase 4bb-F canonical),
the manifest schema (per Phase 4bl-A §12), the integrity-gate
plan (per Phase 4ay §10 precedent), the failure / retry /
missing-file policy (per Phase 4bl-A §10), the acquisition log
schema (per Phase 4bl-A §10), and predeclare the future Phase
4bl-C-equivalent acquisition execution — without authorizing the
acquisition itself or any downstream phase. Phase 4bl-B is **not**
authorised by this merge.
