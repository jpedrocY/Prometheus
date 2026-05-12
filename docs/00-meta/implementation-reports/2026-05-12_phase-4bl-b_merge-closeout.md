# Phase 4bl-B — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-B — Multi-Day aggTrades Acquisition Authorization / Design Memo
- **Type:** docs-only design / authorization-gate memo
- **Action:** merge into `main`
- **Merge purpose:** Bring Phase 4bl-B from branch-complete to
  project-complete status per the Phase 4bk-A workflow standard.
  Phase 4bl-B authored a docs-only design / authorization-gate memo
  that converts the Phase 4bl-A multi-day expansion requirements into
  a precise locked acquisition design for any future Phase 4bl-C
  execution phase. Phase 4bl-B selected the Phase 4bl-A preferred
  upper-bound path per the operator's authorization (storage and disk
  space declared not a practical constraint): BTCUSDT only, 90
  contiguous UTC days, exact date range 2024-12-01 through 2025-02-28
  inclusive, sourced exclusively from `data.binance.vision` public
  daily aggTrades archives. The memo locks the exact 90-element date
  list, the symbol list, the canonical URL pattern with `.CHECKSUM`
  companion-first acquisition, the future local path layout, the
  future multi-day manifest schema (new sibling
  `microstructure_raw_aggtrades_v001__v002.json` distinct from the
  existing one-day `__v001.json`), the future acquisition log schema,
  SHA256 and Phase 4bb-F canonical sidecar rules, the future
  Phase 4bl-C execution boundaries (allowed surface, forbidden
  surface, stop conditions, re-run policy, row-sample validation
  policy, determinism requirements), the failure / retry /
  missing-file policy (3 retries with exponential backoff, 5-min
  per-date budget, HTTP 404 / 5xx / checksum-mismatch / decompression
  failure / row-sample failure handling, no silent skipping, no
  replacement dates, no fallback to APIs), the gitignore and commit
  policy, the existing one-day Phase 4az fixture preservation rule
  (byte-identical; reuse in place; never overwrite), the future
  phase ladder (Phase 4bl-C → 4bl-D → 4bl-E → 4bm-* → 4bn-* →
  4bo-* → 4bp-* → 4bq-* → later ML / strategy / backtest / paper /
  shadow / live; all NOT authorized), M0 and no-rescue integration,
  explicit non-authorizations, the retained verdict ledger preserved
  verbatim (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / 5m thread /
  V2 / G1 / C1), and the project locks preserved verbatim. The merge
  brings forward the Phase 4bl-B implementation report, closeout,
  and narrow `current-project-state.md` update. No data file is
  committed; no manifest is mutated; no successor phase is
  authorized.
- **Target branch:** `main`
- **Source branch:** `phase-4bl-b/multi-day-aggtrades-acquisition-design-memo`

## 2. SHAs

- **`main` SHA before merge:** `dc2240e7a43047823c8b964d52112432b7a61c79`
  (Phase 4bl-A SHA-chain-fixup commit on top of the Phase 4bl-A
  merge-closeout `b9adf68c2662849e344859ec2d7810b9b813ff63`).
- **Phase 4bl-B branch commit SHA:** `e5eb8caa6445dd011c4db253ca12cd8ec0cbfb15`
  (`docs(phase-4bl-b): multi-day aggtrades acquisition authorization / design memo`).
- **Merge commit SHA:** `1e9051e82b37a13042fc44fcc06702304bff2c97`.
- **Merge-closeout commit SHA:** to be recorded in a follow-up commit
  on `main` once this file is committed (the merge-closeout commit
  is the canonical project-complete anchor for Phase 4bl-B).
- **Final `main` / `origin/main` SHA after push:** the canonical
  project-complete anchor for Phase 4bl-B is the merge-closeout
  commit itself (set by the upcoming commit of this file). A
  subsequent one-commit SHA-chain-fixup may record the final-`main`
  SHA value back into this §2 placeholder; that fixup, when it
  exists, does not change Phase 4bl-B lifecycle semantics,
  consistent with the Phase 4bb-G / Phase 4bb-F-implementation /
  Phase 4bb-F / Phase 4bj-G / Phase 4bj-F / Phase 4bj-H / Phase 4bj-I /
  Phase 4bj-J / Phase 4bj-K / Phase 4bl-A SHA-chain-fixup
  precedents.

## 3. Merge method

- Command: `git merge --no-ff phase-4bl-b/multi-day-aggtrades-acquisition-design-memo`
- Strategy: `ort` (the default).
- Merge commit message: `docs(phase-4bl-b): merge multi-day aggtrades acquisition design memo`.
- Push status: pushed to `origin/main` with no force, no skip-hooks,
  no skip-signing.

## 4. Files brought forward by the merge

### Docs (added)

- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_multi-day-aggtrades-acquisition-design-memo.md`
  (the Phase 4bl-B main memo, 21 sections, 1,267 lines)
- `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_closeout.md`
  (the Phase 4bl-B closeout, 9 sections, 127 lines)

### Docs (modified narrowly)

- `docs/00-meta/current-project-state.md` (new Phase 4bl-B narrative
  paragraph prepended above the Phase 4bl-A paragraph; new "Current
  phase:" Phase 4bl-B block; prior Phase 4bl-A "Current phase:"
  block preserved as historical context per the documented
  standard; +511 lines)

### Source / tests / scripts / config / data

- None modified. None added. None removed.
- No source code changes.
- No test changes.
- No script changes (no `scripts/...` entry created or modified).
- No `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`,
  or MCP file change.
- No `data/microstructure/` change (no raw zip, no manifest, no
  sidecar, no acquisition log, no gate report, no successor-state,
  no normalized parquet, no feature parquet, no label parquet, no
  diagnostic artefact, no split artefact created or modified).
- No artefact under `data/raw/`, `data/normalized/`,
  `data/manifests/`, `data/derived/`, or any other project data
  path created or modified.

## 5. Diff summary

- Three tracked files: 1,905 insertions, 0 deletions.
  - `docs/00-meta/current-project-state.md`: +511 lines (narrative
    paragraph + new "Current phase:" block; prior Phase 4bl-A
    "Current phase:" block preserved as historical context).
  - `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_closeout.md`:
    +127 lines (added).
  - `docs/00-meta/implementation-reports/2026-05-12_phase-4bl-b_multi-day-aggtrades-acquisition-design-memo.md`:
    +1,267 lines (added).
- No file deletions.
- No file renames.
- No file moves.
- No binary file changes.

## 6. Result / verdict

- **Status:** SUCCESSFUL_MERGE.
- **Verdict:** MEMO RECORDED — the Phase 4bl-B multi-day aggTrades
  acquisition authorization / design memo is now part of the
  canonical project history on `main`. Phase 4bl-B is
  project-complete only after this merge-closeout commit is
  recorded on `main`.

## 7. Local gitignored outputs

- None. Phase 4bl-B is strictly docs-only. The merge itself
  produces no `data/microstructure/` artefact. The future Phase 4bl-C
  execution phase (NOT authorized by Phase 4bl-B and NOT authorized
  by this merge) would produce the locked gitignored outputs
  described in the Phase 4bl-B memo §7 and §8.

## 8. Validation results

- `git diff --check` (post-merge): clean.
- `git status` (post-merge, pre-merge-closeout-commit): `On branch
  main`; `Your branch is ahead of 'origin/main' by 2 commits`; no
  staged changes; only the pre-existing untracked entries
  (`.claude/scheduled_tasks.lock`, `data/research/`).
- `git log --oneline -6 --decorate` (post-merge,
  pre-merge-closeout-commit):
  ```
  1e9051e (HEAD -> main) docs(phase-4bl-b): merge multi-day aggtrades acquisition design memo
  e5eb8ca (origin/phase-4bl-b/..., phase-4bl-b/...) docs(phase-4bl-b): multi-day aggtrades acquisition authorization / design memo
  dc2240e (origin/main, origin/HEAD) docs(phase-4bl-a): record final main SHA in merge closeout
  b9adf68 docs(phase-4bl-a): add merge closeout
  faffb40 docs(phase-4bl-a): merge multi-day aggtrades expansion requirements memo
  f2726c2 docs(phase-4bl-a): multi-day aggtrades expansion requirements memo
  ```
- `ruff` / `mypy` / `pytest`: not rerun (Phase 4bl-B modifies no
  source code, no tests, no scripts). The most recent authoritative
  whole-repo validation remains the Phase 4bb-F-implementation
  merge: `ruff check .` PASS, `mypy` strict 120 source files PASS,
  `pytest tests/research/microstructure/` 915 passed + 1
  pre-existing labelled skip, whole-repo `pytest` 1698 passed + 1
  skipped + 2 pre-existing simulation failures.

## 9. Upstream immutability evidence

Phase 4bl-B is docs-only. No upstream artefact under
`data/microstructure/` exists in the diff. Specifically, the
following existing local gitignored artefacts remain byte-identical
before and after the Phase 4bl-B merge (no Phase 4bl-B operation
touches them):

- Phase 4az raw zip `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`
  (`data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`).
- Phase 4az raw zip sidecar.
- Phase 4az raw manifest `microstructure_raw_aggtrades_v001__v001.json`
  (recorded SHA256, `research_eligible: false`,
  `eligibility_gate_status: "pending"` preserved).
- Phase 4az raw manifest sidecar.
- Phase 4az acquisition log `microstructure_raw_aggtrades_v001__v001_acquisition_log.json`.
- Phase 4bb-D raw gate report
  `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`
  and paired sidecar.
- Phase 4bd derived parquet
  `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa`
  + derived manifest
  `f6f0d9476ab3fbdb83f58bd4b38e2c6e2386110b371f77d7badcb21897b8e9b9`
  + paired sidecars.
- Phase 4bf derived-family gate report
  `dd4e0c1c32b966378e4ac9b8db4803221ea4d735bdc62a0e0a7be9f710bd4ae6`
  and paired sidecar.
- Phase 4bg-B derived-family successor-state
  `8bcc7d0126128dd855ec67edf450bda088ba7d8d4e2087f339a0446dddedb39e`
  and paired sidecar.
- Phase 4bh feature parquet
  `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f`
  + feature manifest
  `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718`
  + paired sidecars.
- Phase 4bi-B feature-family gate report
  `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988`
  and paired sidecar.
- Phase 4bi-D feature-family successor-state
  `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`
  and paired sidecar.
- Phase 4bj-C label parquet
  `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26`
  + label manifest
  `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3`
  + paired sidecars.
- Phase 4bj-E label-family gate report
  `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0`
  and paired sidecar.
- Phase 4bj-G label-family successor-state
  `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5`
  and paired sidecar.
- Phase 4bj-J no-split-determination JSON
  `7e461eb5508affa9ecd8f9a8127a5528082567a9b7492dd94648002ed37c4fa6`
  and paired sidecar.
- Phase 4bb-G raw-family successor-state
  `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`
  and paired sidecar.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant is preserved (never invoked by Phase 4bl-B
or by the merge).

## 10. Manifest state preservation

- Phase 4az raw manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bd derived manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bh feature manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`: preserved.
- Phase 4bj-C label manifest `research_eligible: false`,
  `eligibility_gate_status: "pending"`,
  `chronological_split_policy: "not_yet_defined"`: preserved.

Phase 4bl-B does NOT flip `research_eligible` on any manifest.
Phase 4bl-B does NOT transition `eligibility_gate_status` on any
manifest. Phase 4bl-B does NOT change `chronological_split_policy`
on any manifest.

## 11. Boundary confirmations (all true)

- `no_data_acquisition`: true (no download, no API call, no
  endpoint call, no WebSocket).
- `no_data_microstructure_modification`: true.
- `no_source_code_modification`: true.
- `no_test_modification`: true.
- `no_script_creation_or_modification`: true.
- `no_pyproject_modification`: true.
- `no_readme_modification`: true.
- `no_gitignore_modification`: true.
- `no_gitattributes_modification`: true.
- `no_mcp_file_modification`: true.
- `no_credential_creation_or_read`: true (no `.env`, no API key,
  no signed request).
- `no_mcp_or_graphify_enabled`: true.
- `no_kernel_or_normalizer_or_gate_run`: true.
- `no_label_statistic_computed`: true.
- `no_diagnostic_executed`: true.
- `no_ml_training_or_architecture`: true.
- `no_feature_ranking_or_meta_labeling`: true.
- `no_strategy_created`: true.
- `no_signal_computed`: true.
- `no_backtest_run`: true.
- `no_pnl_mfe_mae_r_multiple_equity_position_alpha_edge_prediction_modelscore_decisionscore_entryexit_strategyoutput`:
  true.
- `no_research_eligible_flip`: true.
- `no_eligibility_gate_status_transition`: true.
- `no_chronological_split_policy_change`: true.
- `no_project_lock_modification`: true.
- `no_retained_verdict_revision`: true.
- `no_m0_amendment`: true.
- `no_post_null_cooldown_modification`: true.
- `no_cooled_down_families_list_modification`: true.
- `no_phase_4al_no_rescue_rule_modification`: true.
- `no_phase_4bb_f_canonical_path_policy_modification`: true.
- `no_phase_4aw_flip_research_eligible_invariant_modification`:
  true (the method was not invoked).
- `no_phase_4bl_c_authorization`: true.
- `no_phase_5_authorization`: true.
- `no_paper_shadow_authorization`: true.
- `no_live_readiness_authorization`: true.
- `no_exchange_write_authorization`: true.
- `no_production_key_creation_or_request`: true.
- `no_authenticated_api_usage`: true.
- `no_private_endpoint_usage`: true.
- `no_public_endpoint_call_in_code`: true.
- `no_user_stream_or_websocket_usage`: true.
- `no_listenkey_usage`: true.

## 12. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR (Phase 2i §1.7.3). Preserved verbatim.
- **R3** — BASELINE-OF-RECORD (Phase 2p §C.1). Preserved verbatim.
- **R1a** — RETAINED — NON-LEADING (Phase 2m). Preserved verbatim.
- **R1b-narrow** — RETAINED — NON-LEADING (Phase 2s). Preserved
  verbatim.
- **R2** — FAILED — §11.6 cost-sensitivity blocks (Phase 2w §16.1).
  Preserved verbatim.
- **F1** — HARD REJECT (Phase 3c §7.3 catastrophic-floor
  predicate; Phase 3d-B2 terminal). Preserved verbatim.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other (Phase 3h
  §11.2; Phase 3j terminal). Preserved verbatim.
- **5m thread** — OPERATIONALLY CLOSED (Phase 3t). Preserved
  verbatim.
- **V2** — HARD REJECT — terminal for V2 first-spec (Phase 4l,
  structural CFP-1 critical). Preserved verbatim.
- **G1** — HARD REJECT — terminal for G1 first-spec (Phase 4r,
  CFP-1 critical binding; CFP-9 independent). Preserved verbatim.
- **C1** — HARD REJECT — terminal for C1 first-spec (Phase 4x,
  CFP-2 binding; CFP-3 / CFP-6 co-binding). Preserved verbatim.

No retained verdict is revised by Phase 4bl-B or by this merge.

## 13. Preserved project locks (verbatim)

- **§11.6 cost lock** — HIGH cost = 8 bps slippage per side;
  round-trip = 16 bps slippage. Preserved verbatim.
- **§1.7.3 project-level locks** — 0.25% risk per trade; 2×
  leverage cap; one position max; mark-price stops. Preserved
  verbatim.
- **Phase 3p §4.7 strict integrity gate** — preserved verbatim.
- **Phase 3r §8 mark-price gap governance** — preserved verbatim.
- **Phase 3v §8 stop-trigger-domain governance** — preserved
  verbatim.
- **Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation
  governance** — preserved verbatim.
- **Phase 4j §11 metrics OI-subset partial-eligibility rule** —
  preserved verbatim.
- **Phase 4k V2 backtest-plan methodology** — preserved verbatim.
- **Phase 4p G1 strategy-spec memo** — preserved verbatim.
- **Phase 4q G1 backtest-plan methodology** — preserved verbatim.
- **Phase 4v C1 strategy-spec memo** — preserved verbatim.
- **Phase 4w C1 backtest-plan methodology** — preserved verbatim.
- **Phase 4ak M0 mechanism-admissibility twelve-clause gate** —
  preserved verbatim.
- **Phase 4ak post-null cooldown rule** — preserved verbatim.
- **Phase 4ak cooled-down families list** — preserved verbatim.
- **Phase 4ak future M0 memo template** — preserved verbatim.
- **Phase 4al refined no-rescue rule + §13 boundary + §14
  hierarchy** — preserved verbatim.
- **Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant** — preserved verbatim (not invoked).
- **Phase 4bb-F canonical path policy** — preserved verbatim.

## 14. No-rescue constraints

Phase 4bl-B does NOT rescue or revise any of the six cooled-down
failed strategy families (R2 / F1 / D1-A / V2 / G1 / C1). Phase 4bl-B
does NOT propose a new strategy hypothesis. The Phase 4ak M0
twelve-clause gate is not triggered by Phase 4bl-B because Phase
4bl-B is a data-acquisition-design memo, not a hypothesis admission.

Phase 4bl-B explicitly forbids the future Phase 4bl-C (when
separately authorized) from:

- using the acquired multi-day data to re-tune any of the six
  failed strategies;
- re-fitting any threshold or filter that was previously fit on the
  one-day cell;
- re-evaluating any of the six failed strategies under cherry-picked
  sub-windows of the 90-day range;
- "rescuing" any failed hypothesis by appealing to the larger
  evidence base.

The 90-day acquisition is for forward research only — new
hypotheses, new ML feasibility, new descriptive diagnostics, all
gated by M0 on the forward path.

## 15. Successor authorization

This merge-closeout records Phase 4bl-B as project-complete. It
does **NOT** authorize any successor phase. Specifically:

- Phase 4bl-C (Multi-Day aggTrades Acquisition Execution) is NOT
  authorized. Phase 4bl-C requires its own separate authorization
  prompt.
- Phase 4bl-D (Multi-Day Raw Manifest Eligibility Gate) is NOT
  authorized.
- Phase 4bl-E (Multi-Day Raw Manifest Successor-State Recording) is
  NOT authorized.
- Phase 4bm-* (Multi-Day Derived Family arc) is NOT authorized.
- Phase 4bn-* (Multi-Day Feature arc) is NOT authorized.
- Phase 4bo-* (Multi-Day Label arc) is NOT authorized.
- Phase 4bp-* (Multi-Day Label Diagnostic arc) is NOT authorized.
- Phase 4bq-* (Multi-Day Chronological Split arc) is NOT
  authorized.
- Phase 5 / Phase 4 canonical is NOT authorized.
- ML feasibility memo, baseline ML diagnostic, failure-interpretation
  memo, strategy-hypothesis-under-M0 memo, strategy spec, backtest
  plan, backtest execution: NOT authorized.
- Paper / shadow operation: NOT authorized.
- Live-readiness, deployment, exchange-write, production-key
  creation, authenticated APIs, private endpoints, user stream,
  live WebSocket implementation, MCP, Graphify, `.mcp.json`,
  credentials: all NOT authorized.
- Additional aggTrades acquisition beyond the 90 locked BTCUSDT
  UTC dates: NOT authorized.
- 5m / 1m / tick / mark-price 30m / 4h / order-book / spot /
  cross-venue / funding / open-interest data acquisition: NOT
  authorized.

## 16. Recommended state

**Phase 4bl-C conditional primary; remain-paused conditional
secondary.**

The conditional primary recommendation is that the operator may
authorize a future Phase 4bl-C — Multi-Day aggTrades Acquisition
Execution — as the natural next step after Phase 4bl-B is
project-complete. That authorization requires a separate operator
prompt; it is not implicit in this merge-closeout.

The conditional secondary recommendation is to remain paused —
acceptable if the operator wishes to defer Phase 4bl-C indefinitely
or pivot to a different acquisition design.

Phase 4bl-B itself does not require any immediate follow-up action
beyond this merge-closeout. The project-state is well-defined and
stable as of the post-merge-closeout `main`.

---

**End of Phase 4bl-B merge-closeout.**
