# Phase 4bj-F — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-F — Label-Family Research / ML-Use Decision
  Memo
- **Type:** docs-only research-use / ML-use decision memo
- **Action:** merge into `main`
- **Merge purpose:** bring the Phase 4bj-F docs-only research-use /
  ML-use decision memo into `main`, recording the policy-level
  Option B selection: label-family research / ML-use admissibility
  is admissible in principle at policy / governance level for
  `microstructure_labels_aggtrades_v001`, with no manifest
  mutation. A separately authorized future Phase 4bj-G sibling
  successor-state recording phase would be required before any
  machine-readable label admissibility marker exists. The merge
  brings governance text only; it does not modify source, tests,
  scripts, data, manifests, sidecars, gate reports, or runtime
  artefacts, and it does not authorize any successor phase.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-f/label-family-research-ml-use-decision-memo`

## 2. SHAs

- **`main` SHA before merge:**
  `7a860d2e2e0e1ce60f140f515b40e0d0cdb3b3db`
  (post-Phase-4bj-E merge-closeout + SHA-chain-fixup state; the
  Phase 4bj-E merge-closeout commit `ef37b0f` plus the one-commit
  SHA-chain fixup `7a860d2` recording `ef37b0f` into §16 of the
  Phase 4bj-E merge-closeout)
- **Phase 4bj-F branch commit SHA (branch HEAD):**
  `251d99f3f184e72d597b9c91188fb60c5c298f81`
- **Phase 4bj-F merge commit SHA:**
  `aa77c301c6fe1c21e67e81fbf564fe4056997259`
- **Final `main` / `origin/main` SHA after merge push:**
  `aa77c301c6fe1c21e67e81fbf564fe4056997259`
- **Final `main` / `origin/main` SHA after merge-closeout commit +
  push:** (recorded in §16 below after the merge-closeout commit +
  push)
- **Phase 4bj-E merge commit (verified ancestor of `main` at
  branch start):** `e06dbbd973f02352f61479918267a619b78a4c7b`
- **Phase 4bj-E merge-closeout commit (verified ancestor of `main`
  at branch start):** `ef37b0fa3c4f91565b96d0f7da74885704d014b3`
- **Phase 4bj-F branch base (`main` at branch start; merge-base):**
  `7a860d2e2e0e1ce60f140f515b40e0d0cdb3b3db`

## 3. Merge method

- `git merge --no-ff` with `ort` strategy (no fast-forward; merge
  commit created).
- Merge commit message:
  `docs(phase-4bj-f): merge label-family research / ML-use decision memo`.
- Pushed to `origin/main` with no force, no skip-hooks, no
  skip-signing.

## 4. Files brought forward by the merge

Implementation docs (1 added):

- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-f_label-family-research-ml-use-decision-memo.md`

Project state (1 narrowly updated):

- `docs/00-meta/current-project-state.md` (Phase 4bj-F narrative
  paragraph inserted above the Phase 4bj-E narrative paragraph;
  "Current phase:" block replaced with a Phase 4bj-F version; prior
  Phase 4bj-E "Current phase:" block demoted to historical context
  with content preserved verbatim)

No source code, no tests, no scripts, no `.gitignore`, no
`pyproject.toml`, no `README.md`, no MCP files, no governance
memos beyond the narrow `current-project-state.md` Phase 4bj-F
paragraph addition, and no `data/microstructure/` artefacts were
modified by the merge.

## 5. Total diff summary

From the Phase 4bj-F merge:

```text
2 files changed, 1197 insertions(+), 0 deletions
```

The diff matches the expected change set from the authorization
prompt exactly (1 new memo file + 1 narrowly updated
`current-project-state.md`).

## 6. Verdict

**MEMO RECORDED — technical project state unchanged.**

Phase 4bj-F is the label-family analogue of Phase 4bi-C
(feature-family research-use / ML-use decision memo). The memo
records **Option B** at policy / governance level only:
label-family research / ML-use admissibility is admissible **in
principle** for `microstructure_labels_aggtrades_v001`, but no
manifest mutation occurs in this phase. A separately authorized
future Phase 4bj-G sibling successor-state recording phase would
be required before any machine-readable label admissibility marker
exists. Phase 4bj-F does **not** authorize Phase 4bj-G. All eight
deciding criteria PASS (Phase 4bj-E gate report present and SHA
matches `b0b5405b…`; gate `overall_status = pass` with 72 / 72
PASS; all 20 / 20 boundary confirmations true; label parquet SHA
matches `ef50038a…`; label manifest SHA matches `181a799c…`;
manifest state preserved; evidence chain internally consistent;
no-rescue boundaries preserved). The Phase 4bj-E GATE PASS remains
report-level evidence only. The on-disk label manifest remains
`research_eligible=false`, `eligibility_gate_status=pending`, and
`chronological_split_policy=not_yet_defined`. No label
successor-state artefact exists. The Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant is preserved (never invoked). Phase 4bj-F is now
project-complete only with this merge-closeout commit on `main`.
Recommended state: **remain paused unless the operator separately
authorizes Phase 4bj-G.**

## 7. Local gitignored outputs

**none.** Phase 4bj-F is docs-only; no local artefact was produced
under `data/microstructure/` or anywhere else by Phase 4bj-F. The
existing local gitignored Phase 4bj-E gate report and its paired
sidecar (cited by the Phase 4bj-F memo) are unchanged from prior
phases; they are not artefacts of Phase 4bj-F.

## 8. Validation results

All commands run from `C:\Prometheus` post-merge on `main` at
commit `aa77c301c6fe1c21e67e81fbf564fe4056997259`:

- `git diff --check` — clean (no whitespace errors)
- `git status --short` — only pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`); working tree
  otherwise clean
- `git check-ignore -v data/microstructure/` —
  `.gitignore:85:data/microstructure/	data/microstructure/`
- `git check-ignore -v data/microstructure/labels/` —
  `.gitignore:85:data/microstructure/	data/microstructure/labels/`
- `git check-ignore -v data/microstructure/manifests/` —
  `.gitignore:85:data/microstructure/	data/microstructure/manifests/`
- `git check-ignore -v data/microstructure/gate-reports/` —
  `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/`
- `git check-ignore -v data/microstructure/gate-reports/labels/` —
  `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/labels/`

No ruff / mypy / pytest run by this merge. Phase 4bj-F is
docs-only; no source / test / script / config touched. The Phase
4bj-E merge-closeout recorded the last full validation
(`ruff check src/prometheus/research/microstructure/ tests/research/microstructure/` PASS;
`mypy src` strict `Success: no issues found in 119 source files`;
`pytest tests/research/microstructure/` `823 passed, 1 skipped`);
that state is preserved unchanged. Phase 4bj-F does not modify any
file under `src/`, `tests/`, or `scripts/`, so no behavioural
change on those validation surfaces is expected.

The Phase 4bj-D / Phase 4bj-E merge-closeouts noted two
pre-existing whole-repo simulation failures
(`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
and `::test_real_2026_03_ethusdt`; both `KeyError: 'trade_count'`
in the unrelated `src/prometheus/research/data/storage.py:232`).
Those failures are unchanged from prior phases and are not
introduced by this merge.

## 9. Upstream immutability evidence

All six upstream artefacts that this merge must preserve
bit-for-bit are byte-identical pre/post the Phase 4bj-F merge
(recomputed on `main` post-merge):

| Artefact | Pre-Phase-4bj-F SHA256 | Post-Phase-4bj-F SHA256 | Status |
| --- | --- | --- | --- |
| Label parquet (`data/microstructure/labels/.../BTCUSDT-labels-aggtrades-2025-01-15.parquet`) | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | IDENTICAL |
| Label parquet sidecar (`...parquet.sha256`) | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | IDENTICAL |
| Label manifest (`data/microstructure/manifests/microstructure_labels_aggtrades_v001__v001.json`) | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | IDENTICAL |
| Label manifest sidecar (`...json.sha256`) | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | IDENTICAL |
| Phase 4bj-E gate report (`data/microstructure/gate-reports/labels/...phase-4bj-e__1778531608796__89cde8ad14b5.json`) | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` | IDENTICAL |
| Phase 4bj-E gate report sidecar (`....json.sha256`) | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` | IDENTICAL |

No `data/microstructure/` read or write occurred during Phase
4bj-F; the SHA recomputation in this section is independent
verification only.

## 10. Manifest state preservation

The label manifest (`microstructure_labels_aggtrades_v001__v001.json`):

- `research_eligible` — `false` pre and post (unchanged)
- `eligibility_gate_status` — `"pending"` pre and post (unchanged)
- `chronological_split_policy` — `"not_yet_defined"` pre and post
  (unchanged)
- `governance_labels` — unchanged: `ml=forbidden`,
  `strategy=forbidden`, `backtest=forbidden`,
  `paper_shadow_live=forbidden`, `deployment=forbidden`,
  `exchange_write=forbidden`, `acquisition=unauthorized`
- `boundary_confirmations` — unchanged
- `label_config_hash` —
  `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00`
  pre and post (unchanged)
- `invalid_price_row_count` — `0` pre and post (unchanged)
- `censored_per_horizon` —
  `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` pre and post
  (unchanged)
- `row_count` — `1,681,098` pre and post (unchanged)

Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant preserved (never invoked).

The Phase 4bj-E gate report's invariants
(`research_eligible_after = False`,
`label_manifest_research_eligible_after = False`,
`label_manifest_eligibility_gate_status_after = "pending"`,
`label_manifest_chronological_split_policy_after = "not_yet_defined"`,
`stage_5_authorized = False`,
`stage_5_research_or_ml_use = False`,
`no_successor_authorization = True`) remain intact on the on-disk
gate report.

## 11. Boundary confirmations

The Phase 4bj-F merge honours every boundary below:

- no source code modified
- no test modified
- no script modified
- no `pyproject.toml`, `README.md`, `.gitignore`, or MCP file
  modified
- no label parquet modified
- no label parquet sidecar modified
- no label manifest modified
- no label manifest sidecar modified
- no feature parquet, feature manifest, normalized parquet,
  original derived manifest, raw manifest, raw zip, Phase 4bb-D
  raw gate report, Phase 4bf derived gate report, Phase 4bg-B
  successor-state, Phase 4bi-B feature-family gate report, Phase
  4bi-D feature-family successor-state, or Phase 4bj-E
  label-family gate report modified
- no `data/microstructure/` write occurred
- no `data/microstructure/` artefact committed
- no label-family successor-state artefact created
- no replacement parquet / manifest / sidecar / gate report /
  successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed on any actual manifest
- no ML model trained
- no ML architecture designed
- no feature ranking performed
- no meta-labeling created
- no strategy created
- no strategy signal computed
- no backtest run
- no data acquired
- no public endpoint called
- no Binance API called
- no WebSocket opened
- no credential read
- no `.env` read or created
- no `.mcp.json` read or created
- no MCP enabled
- no Graphify enabled
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family eligibility gate rerun
- no label kernel rerun
- no label-family eligibility gate rerun
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 12. Retained verdict ledger

All retained verdicts preserved verbatim:

- **H0** — FRAMEWORK ANCHOR
- **R3** — BASELINE-OF-RECORD
- **R1a** — RETAINED — NON-LEADING
- **R1b-narrow** — RETAINED — NON-LEADING
- **R2** — FAILED — §11.6
- **F1** — HARD REJECT
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t
- **V2** — HARD REJECT — terminal for V2 first-spec
- **G1** — HARD REJECT — terminal for G1 first-spec
- **C1** — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 13. Preserved project locks

All locks preserved verbatim:

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

All prior phase results (Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as,
4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D,
4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B,
4bh, 4bi-A, 4bi-B, 4bi-C, 4bi-D, 4bj-A, 4bj-B, 4bj-C, 4bj-D, 4bj-E,
4bk-A) preserved verbatim.

## 14. No-rescue constraints

The Phase 4bj-F merge does not, and cannot, be construed as
authorising:

- ML model training, ML architecture design, model selection,
  feature ranking, meta-labeling, or any conversion of labels into
  signals;
- strategy hypothesis generation, signal construction, strategy
  logic, position state, entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write
  work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL
  labels;
- mark-price / spot / cross-venue / order-book / additional
  aggTrades acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible` from this
  evidence alone;
- transitioning any manifest's `eligibility_gate_status` from this
  evidence alone;
- changing any manifest's `chronological_split_policy` from this
  evidence alone;
- creating a label-family successor-state artefact from this
  evidence alone;
- treating the Phase 4bj-F policy admissibility decision as
  authorisation to design ML, strategy, backtests, or live work;
- treating the Phase 4bj-F memo as authorisation for Phase 4bj-G.

Phase 4bj-F is a policy / governance decision only. It is upstream
of M0 admissibility and cannot bypass M0 for any future
hypothesis, label, target, strategy, or backtest.

## 15. Successor authorization

**None.**

The following candidate successors are NOT authorised by this
merge:

- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book
  data acquisition
- ML implementation
- ML training
- model selection
- feature ranking
- meta-labeling
- strategy implementation
- backtest implementation
- paper / shadow
- live-readiness
- deployment
- exchange-write
- production keys
- authenticated APIs
- private endpoints
- user stream
- live WebSocket implementation
- MCP / Graphify / `.mcp.json` / credentials
- any manifest transition

## 16. Recommended state

**Remain paused unless the operator separately authorizes Phase
4bj-G.**

Phase 4bj-F is project-complete with this merge-closeout commit on
`main`. The Phase 4bj-F policy admissibility decision (Option B)
is now part of the project record. The label-family eligibility
gate primitive remains part of the project record from Phase
4bj-E. The label manifest remains `research_eligible=false /
eligibility_gate_status=pending /
chronological_split_policy=not_yet_defined`. No label
successor-state artefact exists. No machine-readable label
admissibility marker exists. No successor phase is authorized.

**Conditional next, NOT authorised:**

Phase 4bj-G — Label-Family Successor-State Recording is the
cleanest non-paused option per Option B and per the Phase 4bg-B /
Phase 4bi-D precedents. It would, if separately authorised,
produce exactly one sibling successor-state JSON artefact under a
gitignored namespace (e.g.,
`data/microstructure/successor-state/`) with paired `.sha256`
sidecar, preserve the original label manifest byte-identically,
and record a machine-readable admissibility marker on the sibling
artefact only — without flipping `research_eligible`,
transitioning `eligibility_gate_status`, changing
`chronological_split_policy`, training ML, designing ML
architecture, ranking features, creating meta-labeling, creating a
strategy, running backtests, acquiring data, or authorising paper
/ shadow / live / exchange-write. Phase 4bj-G is **not**
authorised by this merge. Per the Phase 4bk-A workflow standard, a
separately authorised authorization prompt is required before any
successor begins.

**Final `main` / `origin/main` SHA after this merge-closeout commit
+ push:** `9657651cf227527d987d55cb610d9b7ede66a19e`
