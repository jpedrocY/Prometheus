# Phase 4bj-D — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bj-D — Label Artefact Structural QA Memo
- **Type:** docs-only / read-only structural QA
- **Action:** merge into `main`
- **Merge purpose:** bring the Phase 4bj-D read-only structural QA
  inspection of the Phase 4bj-C local Stage-0 label artefacts (label
  parquet, label parquet sidecar, label manifest, label manifest
  sidecar; gitignored under `data/microstructure/`) into `main` so
  the project record carries the structural-QA evidence that the
  locally generated label artefacts conform to the Phase 4bj-B v001
  schema contract, without transitioning any manifest state and
  without creating any label-family eligibility gate report or
  label successor-state artefact.
- **Target branch:** `main`
- **Source branch:** `phase-4bj-d/label-artefact-structural-qa-memo`

## 2. SHAs

- **`main` SHA before merge:** `5fedc0c` (Phase 4bj-C merge closeout)
- **Phase 4bj-D memo commit SHA:** `427ec28e142e48ed6c7055960f30969f20d50759`
- **Phase 4bj-D closeout commit SHA:** `ad245b899c5bbe66d642cae82bbe77b92f370474`
- **Phase 4bj-D merge commit SHA:** `11e25acbf7d33b30f5149b93919594c3ccab9fe2`
- **Final `main` / `origin/main` SHA after push:**
  (recorded in §17 below after the merge-closeout commit + push)

## 3. Merge method

- `git merge --no-ff` with `ort` strategy
- Merge commit message: `docs(phase-4bj-d): merge label artefact structural QA memo`
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing.

## 4. Files brought forward by the merge

Docs (2 added, 1 narrowly updated):

- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_label-artefact-structural-qa-memo.md`
- `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-d_closeout.md`
- `docs/00-meta/current-project-state.md` (Phase 4bj-D narrative
  paragraph + Current phase block; prior Phase 4bj-C block demoted
  to historical context)

Total diff summary from the Phase 4bj-D merge:

```text
3 files changed, 736 insertions(+), 0 deletions
```

No source code, no tests, no scripts, no `.gitignore`, no
`pyproject.toml`, no `README.md`, no MCP files, no governance memos
beyond the narrow `current-project-state.md` Phase 4bj-D paragraph
addition, and no `data/microstructure/` artefacts were modified by
the merge.

## 5. Verdict

**STRUCTURAL QA PASS — label artefact remains not research-eligible.**

The Phase 4bj-D read-only inspection confirms the Phase 4bj-C local
Stage-0 label artefacts conform to the Phase 4bj-B v001 schema
contract bit-for-bit at the descriptive level. The label family
remains `research_eligible = false` and `eligibility_gate_status =
"pending"`. No state was transitioned. No gate report was created.
No successor-state artefact was created. No verdict was revised.

## 6. Evidence summary

| Field | Value |
|---|---|
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar SHA | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` (matches) |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar SHA | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` (matches) |
| `row_count` | 1,681,098 |
| `column_count` | 39 |
| Schema column order | matches `LABEL_SCHEMA_COLUMNS_V001` exactly |
| Per-column dtype | matches `LABEL_SCHEMA_V001` exactly |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| `invalid_price_row_count` | 0 |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| `research_eligible` | `false` |
| `eligibility_gate_status` | `"pending"` |
| `chronological_split_policy` | `"not_yet_defined"` |
| Anomalies discovered | none |

## 7. Validation results

- `ruff check .` (whole repo): **All checks passed**
- `mypy` (whole repo, strict): **Success on 115 source files**
- `pytest tests/research/microstructure/`: **744 passed**
- `git diff --check`: clean
- `git check-ignore -v data/microstructure/`: `.gitignore:85`
- `git check-ignore -v data/microstructure/labels/`: `.gitignore:85`
- `git check-ignore -v data/microstructure/manifests/`: `.gitignore:85`

## 8. Boundary confirmations

- no labels modified
- no label manifest modified
- no label parquet modified
- no label sidecars modified
- no `data/microstructure/` write outside the read-only inspection
- no `data/microstructure/` artefact committed
- no label-family gate report created
- no label-family successor-state artefact created
- no replacement parquet / manifest / sidecar / gate report /
  successor-state created
- no `research_eligible` flipped on any actual manifest
- no `eligibility_gate_status` transitioned on any actual manifest
- no `chronological_split_policy` changed
- no ML model trained
- no strategy created
- no signal computed
- no backtest run
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge
  / prediction / model-score / decision-score / entry-exit / strategy
  output computed
- no data acquired
- no public endpoint called
- no Binance API called
- no WebSocket opened
- no credential / `.env` / `.mcp.json` / MCP / Graphify used
- no normalizer rerun
- no raw eligibility gate rerun
- no derived-family gate rerun
- no feature kernel rerun
- no feature-family eligibility gate rerun
- no source code modified
- no test modified
- no script modified
- no `.gitignore`, `pyproject.toml`, or `README.md` modified
- no MCP file modified
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

## 9. Retained verdict ledger

- H0 — FRAMEWORK ANCHOR
- R3 — BASELINE-OF-RECORD
- R1a — RETAINED — NON-LEADING
- R1b-narrow — RETAINED — NON-LEADING
- R2 — FAILED — §11.6
- F1 — HARD REJECT
- D1-A — MECHANISM PASS / FRAMEWORK FAIL
- 5m thread — OPERATIONALLY CLOSED
- V2 — HARD REJECT — terminal for V2 first-spec
- G1 — HARD REJECT — terminal for G1 first-spec
- C1 — HARD REJECT — terminal for C1 first-spec

All preserved verbatim.

## 10. Preserved project locks

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule
  + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw / 4ax / 4ay / 4az / 4ba / 4bb-A / 4bb-B / 4bb-C / 4bb-D /
  4bb-E / 4bc / 4bd-A / 4bd / 4be / 4bf-A / 4bf / 4bg-A / 4bg-B /
  4bh-A / 4bh-B / 4bh / 4bi-A / 4bi-B / 4bi-C / 4bi-D / 4bj-A / 4bj-B
  / 4bj-C results all preserved verbatim

## 11. No-rescue constraints

The Phase 4bj-D merge does not, and cannot, be construed as
authorising:

- ML model training, model selection, strategy hypothesis
  generation, or any conversion of labels into signals;
- strategy signal construction, strategy logic, position state,
  entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades
  acquisition;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning the label manifest's `research_eligible` or
  `eligibility_gate_status` from this read-only QA evidence alone.

## 12. Recommended state

**Remain paused.**

The Phase 4bj-D structural QA evidence is recorded in the project
record. The label family remains Stage-0, `research_eligible =
false`, `eligibility_gate_status = "pending"`. No further forward
motion is implied by this merge.

## 13. Successor authorization

**None.**

The Phase 4bj-D merge closes the read-only structural QA review of
the Phase 4bj-C local label artefacts. Specifically not authorised
by this merge:

- Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation
  + Execution
- Phase 4bj-F — Label-Family Research / ML-Use Decision
- Phase 4bj-G — Label-Family Successor-State Recording
- Phase 4bj (catch-all)
- Phase 4bb-F — Gate Report Output Path Hygiene
- Phase 4bb-G — Raw Manifest Successor-State Recording
- Phase 5
- Phase 4 canonical
- additional aggTrades / 5m / 1m / tick / mark-price / order-book
  data acquisition
- ML implementation
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
- MCP / Graphify / `.mcp.json` / credentials

## 14. Conditional next, NOT authorized

**Phase 4bj-E — Label-Family Eligibility Gate Design + Implementation
+ Execution** is the cleanest non-paused option. It would design
and implement an offline label-family eligibility gate analogous to
the Phase 4bb-C raw eligibility gate and the Phase 4bf derived-family
gate, then run it exactly once against the Phase 4bj-C local label
artefacts to produce a gitignored gate report under
`data/microstructure/gate-reports/labels/`, while preserving the
label manifest byte-identically and preserving `research_eligible =
false` for the label family at the actual-manifest level.

Phase 4bj-E is **not** authorised by this merge.
