# Phase 4bj-G — Label-Family Successor-State Recording

**Phase identity:** Phase 4bj-G — Label-Family Successor-State Recording (docs + local gitignored successor-state artefact recording).
**Date:** 2026-05-11.
**Branch:** `phase-4bj-g/label-family-successor-state-recording`.
**Base:** `main` at `0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3` (post-Phase-4bj-F SHA-chain-fixup state). Phase 4bj-F merge commit `aa77c301c6fe1c21e67e81fbf564fe4056997259` and merge-closeout commit `9657651cf227527d987d55cb610d9b7ede66a19e` confirmed as ancestors of `main`.
**Status:** drafted; pending operator review.
**Phase type:** docs + local gitignored successor-state artefact recording.

---

## 1. Phase header

Phase 4bj-G converts the Phase 4bj-F policy-level Option B admissibility decision into a single machine-readable sibling successor-state JSON artefact (plus paired SHA256 sidecar) under the gitignored `data/microstructure/successor-state/` namespace for the label family `microstructure_labels_aggtrades_v001`, while preserving the original label manifest, the original label parquet, and the Phase 4bj-E gate report byte-identically.

The phase is deliberately narrow:

- it records label-family research / ML-use admissibility **only** at the sibling successor-state artefact level;
- it must not flip `research_eligible` on the label manifest;
- it must not transition `eligibility_gate_status` on the label manifest;
- it must not change `chronological_split_policy` on the label manifest;
- it must not create ML / strategy / signals / targets / backtests / acquisition / paper-shadow / live / exchange-write capability;
- it must not authorize any successor phase.

This phase mirrors the Phase 4bg-B (derived-family) and Phase 4bi-D (feature-family) precedents exactly, transposed to the label family.

A small detail on the SHA-chain pattern: the Phase 4bj-F merge-closeout itself anchored its §16 final SHA at `9657651cf227527d987d55cb610d9b7ede66a19e`. The one-commit fixup on top of `9657651` (commit `0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3`) only records that final-SHA value into the §16 placeholder; it does not change Phase 4bj-F lifecycle semantics. Phase 4bj-G branches from `0a069e2` because that is the post-fixup `main` state; the underlying merge-closeout commit (`9657651`) remains the canonical "Phase 4bj-F project-complete" anchor and is cited as such inside the successor-state JSON.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bj-E merge commit | `e06dbbd973f02352f61479918267a619b78a4c7b` |
| Phase 4bj-E merge-closeout commit | `ef37b0fa3c4f91565b96d0f7da74885704d014b3` |
| Phase 4bj-E SHA-chain-fixup commit | `7a860d2` |
| Phase 4bj-F merge commit | `aa77c301c6fe1c21e67e81fbf564fe4056997259` |
| Phase 4bj-F merge-closeout commit | `9657651cf227527d987d55cb610d9b7ede66a19e` |
| Phase 4bj-F SHA-chain-fixup commit | `0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3` |
| `main` HEAD at start of Phase 4bj-G | `0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3` |
| Raw family | `microstructure_raw_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Derived family | `microstructure_normalized_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Feature family | `microstructure_features_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Label family | `microstructure_labels_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending`, `chronological_split_policy=not_yet_defined` |
| Symbol scope | BTCUSDT only |
| UTC date scope | `2025-01-15` |
| Label row count | `1 681 098` |
| Label schema columns | 39 |
| `label_config_hash` | `fe4633af77c8dd6a56c381031a6f5c255a277777b1bc7f6ea54863c014286f00` |
| Phase 4bj-E gate report SHA256 | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` |
| Phase 4bj-E gate report sidecar SHA256 | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` |
| Label parquet SHA256 | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` |
| Label parquet sidecar SHA256 | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` |
| Label manifest SHA256 | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` |
| Label manifest sidecar SHA256 | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` |
| `data/microstructure/` gitignore | `.gitignore:85` (covers `successor-state/` as a subpath) |

---

## 3. Inputs reviewed

- Phase 4az raw aggTrades acquisition + Phase 4bb-D raw eligibility gate.
- Phase 4bd normalization + Phase 4be structural QA + Phase 4bf derived-family eligibility gate.
- Phase 4bg-A derived-family research-eligibility decision + Phase 4bg-B derived-family successor-state JSON.
- Phase 4bh-A feature-boundary design + Phase 4bh-B feature schema finalization + Phase 4bh feature kernel implementation.
- Phase 4bi-A feature-artefact structural QA + Phase 4bi-B feature-family eligibility gate (70 / 70 PASS).
- Phase 4bi-C feature-family research-use / ML-use decision (Outcome 1 / Decision form 1) + Phase 4bi-D feature-family successor-state recording.
- Phase 4bj-A label boundary / target definition memo.
- Phase 4bj-B label schema finalization memo.
- Phase 4bj-C label kernel implementation + label artefact production.
- Phase 4bj-D label artefact structural QA memo (21 / 21 PASS).
- Phase 4bj-E label-family eligibility gate design + implementation + execution (72 / 72 PASS, report SHA `b0b5405b…`).
- Phase 4bj-E merge-closeout (six upstream artefacts byte-identical pre/post).
- Phase 4bj-F label-family research / ML-use decision memo (Option B — admissible in principle at policy level only; no manifest mutation; sibling successor-state required for any machine-readable marker).
- Phase 4bj-F merge-closeout (six upstream artefacts byte-identical pre/post; MEMO RECORDED verdict).

No prior memo's text was modified by Phase 4bj-G. No prior `data/microstructure/` artefact was modified.

---

## 4. Scope

In scope for this phase:

- creating exactly one local gitignored successor-state JSON under `data/microstructure/successor-state/` recording the Phase 4bj-F Option B admissibility decision for the label family `microstructure_labels_aggtrades_v001`;
- creating exactly one paired `.sha256` sidecar file matching the JSON's bytes;
- citing the Phase 4bj-E gate report id, gate report SHA, gate report sidecar SHA, label parquet SHA, label parquet sidecar SHA, label manifest SHA, label manifest sidecar SHA, `label_config_hash`, row count, column count, `invalid_price_row_count`, and `censored_per_horizon` verbatim;
- citing the Phase 4bj-F memo path, merge commit SHA, and merge-closeout commit SHA verbatim;
- preserving the original label manifest byte-identically (SHA `181a799c…`);
- preserving the original label parquet byte-identically (SHA `ef50038a…`);
- preserving the original sidecars byte-identically;
- preserving the original Phase 4bj-E gate report and its sidecar byte-identically;
- preserving `research_eligible=false`, `eligibility_gate_status=pending`, and `chronological_split_policy=not_yet_defined` on the original label manifest;
- documenting the action in this memo, a closeout, and a narrow `current-project-state.md` paragraph plus updated "Current phase:" block (prior Phase 4bj-F block preserved).

---

## 5. Non-scope

This phase does **not**:

- modify any source code, test, script, configuration, dataset, manifest, sidecar, Phase 4bj-E gate report, feature parquet, feature manifest, Phase 4bi-D successor-state, normalized parquet, derived manifest, raw manifest, raw zip, Phase 4bb-D raw gate report, Phase 4bf derived gate report, or Phase 4bg-B successor-state;
- run the label-family gate, label kernel, feature-family gate, feature kernel, derived-family gate, normalizer, or raw eligibility gate;
- generate any new gate report;
- create labels, targets, signals, ML, strategy, or backtest artefacts;
- compute PnL / MFE / MAE / R-multiple / equity / position state / alpha / edge / prediction / model score / decision score / entry / exit / strategy output;
- train ML;
- design ML architecture;
- rank features;
- create meta-labeling;
- design strategy logic;
- run backtests or simulations;
- acquire data;
- call public endpoints, Binance APIs, or private endpoints;
- open WebSockets;
- request, store, or use credentials;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- change `chronological_split_policy` on any actual manifest;
- mutate the label manifest, label parquet, or any prior manifest in any way;
- amend M0;
- revise any retained verdict;
- change any project lock;
- authorize Phase 5 / Phase 4 canonical / paper / shadow / live-readiness / deployment / exchange-write / production keys / authenticated APIs / private endpoints / user stream / live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bj-F dependency

This phase depends entirely on Phase 4bj-F's locked outputs:

- Phase 4bj-F is merged into `main` at merge commit `aa77c301c6fe1c21e67e81fbf564fe4056997259` with merge-closeout commit `9657651cf227527d987d55cb610d9b7ede66a19e`.
- Phase 4bj-F selected **Option B**: *Label-family research / ML-use admissibility is admissible in principle at policy / governance level for `microstructure_labels_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized future Phase 4bj-G sibling successor-state recording phase is required before any machine-readable label admissibility marker exists.*
- Phase 4bj-F explicitly named Phase 4bj-G as the conditional next step ("the cleanest non-paused option"), subject to separate operator authorization. This memo and its successor-state artefact are the recorded execution of that step.

This phase does not re-derive Phase 4bj-F's evidence; it cites it as locked input.

---

## 7. Successor-state recording objective

The Phase 4bg-B precedent (derived family) and Phase 4bi-D precedent (feature family) established a sibling successor-state JSON pattern under the gitignored `data/microstructure/successor-state/` namespace. Phase 4bj-G applies the same pattern to the label family:

- one JSON file at a deterministic path under `data/microstructure/successor-state/`;
- one paired `.sha256` sidecar with the format `<sha256>  <filename>\n`;
- canonical sorted-key, indent-2 JSON serialization, with trailing newline;
- atomic write-then-rename via `os.replace`;
- refuse-overwrite on either file;
- byte-for-byte preservation of every upstream artefact, including the original label manifest, the original label parquet, both sidecars, and the Phase 4bj-E gate report and its sidecar.

The successor-state JSON is the **only** machine-readable place where Phase 4bj-F Option B admissibility is recorded for the label family. The original label manifest's `research_eligible`, `eligibility_gate_status`, and `chronological_split_policy` fields **must not** be flipped, transitioned, or changed by this phase or by any tooling that relies on this artefact.

---

## 8. Successor-state artefact path

| Item | Value |
| ---- | ----- |
| JSON path | `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g.json` |
| Sidecar path | `data/microstructure/successor-state/microstructure_labels_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bj-g.json.sha256` |
| JSON SHA256 | `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5` |
| JSON size | 9 086 bytes |
| Sidecar size | 158 bytes |
| Sidecar self-SHA256 | `c6fe4fa1133d788976a7ecc7883b87e7cf04eb16ec76ec77e0467025e888a2fb` |
| Sidecar parses to recomputed JSON SHA | yes (matches `ce7d3917…`) |
| Gitignore coverage | `.gitignore:85` (covers both files under `data/microstructure/`) |
| Tracked in git | **NO** — both files are gitignored and are **NOT** committed |

The path scheme follows the established convention used by Phase 4bg-B (`microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`) and Phase 4bi-D (`microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json`) exactly. The naming convention `<family>__<version>__<stage_marker>__<phase>.json` is preserved across all three successor-state precedents; the namespace is flat (no `labels/` subdirectory) to mirror the prior two precedents.

The `stage5_research_ml_admissible` stage marker mirrors Phase 4bi-D's marker, recognising that label-family research / ML-use admissibility is a Stage-5-equivalent state at the label-family layer. Phase 4bj-F established that the label family is admissible in principle at policy level only (Option B); the successor-state JSON records that admissibility while leaving the label manifest itself untouched.

---

## 9. Successor-state schema

The JSON payload is deterministic (`json.dumps(payload, sort_keys=True, indent=2) + "\n"`) and contains, at minimum, the following fields. The exhaustive enumeration in §10 verifies that every field required by the Phase 4bj-G authorization prompt is present.

Top-level identity:

- `schema_version = "v001"`
- `phase = "Phase 4bj-G"`
- `phase_id = "4bj-G"`
- `artefact_type = "label_family_successor_state"`
- `successor_state_family = "microstructure_labels_aggtrades_v001"`
- `successor_state_version = "v001"`
- `successor_state_type = "label_family_stage5_equivalent_research_ml_admissibility"`
- `successor_stage = "stage_5_equivalent_successor_state_recorded"`

Source label-family identity (locked from Phase 4bj-C and Phase 4bj-D, verified by Phase 4bj-E):

- `source_label_family`, `source_label_family_version`, `source_symbol`, `source_utc_date`
- `source_label_parquet_path`, `source_label_parquet_sha256`, `source_label_parquet_sidecar_sha256`
- `source_label_manifest_path`, `source_label_manifest_sha256`, `source_label_manifest_sidecar_sha256`
- `label_config_hash`, `row_count`, `column_count`, `invalid_price_row_count`, `censored_per_horizon`

Phase 4bj-E gate report citation (verbatim):

- `phase_4bj_e_gate_report_id`, `phase_4bj_e_gate_report_path`, `phase_4bj_e_gate_report_sha256`, `phase_4bj_e_gate_report_sidecar_sha256`
- `phase_4bj_e_gate_overall_status = "pass"`
- `phase_4bj_e_gate_checks_total = 72`, `phase_4bj_e_gate_checks_pass = 72`, `phase_4bj_e_gate_checks_fail = 0`, `phase_4bj_e_gate_checks_error = 0`, `phase_4bj_e_gate_checks_not_applicable = 0`
- `phase_4bj_e_merge_commit_sha`, `phase_4bj_e_merge_closeout_commit_sha`, `phase_4bj_e_merge_closeout_path`

Phase 4bj-F policy decision citation (verbatim):

- `phase_4bj_f_policy_decision = "option_b_admissible_in_principle_successor_state_required"`
- `phase_4bj_f_decision_summary` (Option B language verbatim)
- `phase_4bj_f_memo_path`, `phase_4bj_f_merge_commit_sha`, `phase_4bj_f_merge_closeout_commit_sha`, `phase_4bj_f_merge_closeout_path`

Successor admissibility state — policy level only:

- `successor_admissibility_status = "admissible_in_principle_policy_level_only"`
- `successor_research_use_admissible = true`
- `successor_ml_use_admissible = "conditional_future_only"`

Original-manifest preservation invariants:

- `original_manifest_mutated = false`
- `original_label_parquet_mutated = false`
- `original_sidecars_mutated = false`
- `original_label_manifest_research_eligible = false`
- `original_label_manifest_eligibility_gate_status = "pending"`
- `original_label_manifest_chronological_split_policy = "not_yet_defined"`
- `original_label_manifest_must_remain_byte_identical = true`
- `manifest_mutation_permitted = false`
- `manifest_research_eligible_after = false`
- `manifest_eligibility_gate_status_after = "pending"`
- `manifest_chronological_split_policy_after = "not_yet_defined"`

Non-authorizations (every relevant flag is `false` or `"unauthorized"`):

- `ml_training_authorized`, `ml_architecture_authorized`, `feature_ranking_authorized`, `meta_labeling_authorized`
- `strategy_authorized`, `backtest_authorized`, `acquisition_authorized`
- `paper_shadow_authorized`, `live_readiness_authorized`, `deployment_authorized`, `exchange_write_authorized`
- `production_keys_authorized`, `authenticated_apis_authorized`, `private_endpoints_authorized`, `user_stream_authorized`, `websocket_authorized`
- `mcp_authorized`, `graphify_authorized`, `credentials_authorized`
- `successor_authorizes_next_phase = false`, `next_phase_authorized = false`
- `recommended_state = "remain_paused"`

`governance_labels` (mirrors actual on-disk label-manifest values; all forbidden / unauthorized).

`boundary_confirmations` (28 keys, all `true`; see §11 below for the complete enumeration).

`retained_verdict_ledger` (preserved verbatim).

`preserved_project_locks` (preserved verbatim).

`no_rescue_statement` (explicit no-rescue language).

Provenance metadata:

- `created_at_unix_ms = 1778539948399`
- `created_at_utc = "2026-05-11T22:52:28.399104Z"`
- `code_commit_sha = "0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3"` (current branch HEAD at write time, i.e. the base `main` SHA before any Phase 4bj-G commit)
- `base_main_commit_sha = "0a069e24b5aeb15229bbf16f0e0dc9542a7d02b3"`
- `predecessor_merge_closeout_commit_sha = "9657651cf227527d987d55cb610d9b7ede66a19e"`
- `precedent_phases` (Phase 4bg-B, Phase 4bi-D)

---

## 10. Required-field coverage

The Phase 4bj-G authorization prompt enumerated a minimum required field list. Every required field is present in the on-disk JSON and is exactly as specified:

| Required field | Recorded value |
| -------------- | -------------- |
| `successor_state_family` | `microstructure_labels_aggtrades_v001` |
| `successor_state_version` | `v001` |
| `phase` | `Phase 4bj-G` |
| `artefact_type` | `label_family_successor_state` |
| `source_label_family` | `microstructure_labels_aggtrades_v001` |
| `source_symbol` | `BTCUSDT` |
| `source_utc_date` | `2025-01-15` |
| `source_label_parquet_path` | (locked path; see §2) |
| `source_label_parquet_sha256` | `ef50038a…` |
| `source_label_parquet_sidecar_sha256` | `b9681e6b…` |
| `source_label_manifest_path` | (locked path; see §2) |
| `source_label_manifest_sha256` | `181a799c…` |
| `source_label_manifest_sidecar_sha256` | `3392a336…` |
| `label_config_hash` | `fe4633af…` |
| `row_count` | `1681098` |
| `column_count` | `39` |
| `invalid_price_row_count` | `0` |
| `censored_per_horizon` | `{"1s": 9, "5s": 42, "15s": 118, "60s": 507}` |
| `phase_4bj_e_gate_report_id` | (locked id; see §2) |
| `phase_4bj_e_gate_report_path` | (locked path; see §2) |
| `phase_4bj_e_gate_report_sha256` | `b0b5405b…` |
| `phase_4bj_e_gate_report_sidecar_sha256` | `2f24ad3e…` |
| `phase_4bj_e_gate_overall_status` | `pass` |
| `phase_4bj_e_gate_checks_total` | `72` |
| `phase_4bj_e_gate_checks_pass` | `72` |
| `phase_4bj_e_gate_checks_fail` | `0` |
| `phase_4bj_e_gate_checks_error` | `0` |
| `phase_4bj_e_gate_checks_not_applicable` | `0` |
| `phase_4bj_f_policy_decision` | `option_b_admissible_in_principle_successor_state_required` |
| `phase_4bj_f_memo_path` | `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-f_label-family-research-ml-use-decision-memo.md` |
| `phase_4bj_f_merge_closeout_path` | `docs/00-meta/implementation-reports/2026-05-11_phase-4bj-f_merge-closeout.md` |
| `successor_admissibility_status` | `admissible_in_principle_policy_level_only` |
| `successor_research_use_admissible` | `true` |
| `successor_ml_use_admissible` | `conditional_future_only` |
| `successor_stage` | `stage_5_equivalent_successor_state_recorded` |
| `manifest_research_eligible_after` | `false` |
| `manifest_eligibility_gate_status_after` | `pending` |
| `manifest_chronological_split_policy_after` | `not_yet_defined` |
| `original_manifest_mutated` | `false` |
| `original_label_parquet_mutated` | `false` |
| `original_sidecars_mutated` | `false` |
| `ml_training_authorized` | `false` |
| `ml_architecture_authorized` | `false` |
| `feature_ranking_authorized` | `false` |
| `meta_labeling_authorized` | `false` |
| `strategy_authorized` | `false` |
| `backtest_authorized` | `false` |
| `acquisition_authorized` | `false` |
| `paper_shadow_authorized` | `false` |
| `live_readiness_authorized` | `false` |
| `deployment_authorized` | `false` |
| `exchange_write_authorized` | `false` |
| `production_keys_authorized` | `false` |
| `authenticated_apis_authorized` | `false` |
| `private_endpoints_authorized` | `false` |
| `user_stream_authorized` | `false` |
| `websocket_authorized` | `false` |
| `mcp_authorized` | `false` |
| `graphify_authorized` | `false` |
| `credentials_authorized` | `false` |
| `successor_authorizes_next_phase` | `false` |
| `recommended_state` | `remain_paused` |

Additional fields beyond the required minimum that strengthen the record:

- `phase_4bj_e_merge_commit_sha`, `phase_4bj_e_merge_closeout_commit_sha`, `phase_4bj_e_merge_closeout_path`
- `phase_4bj_f_decision_summary`, `phase_4bj_f_merge_commit_sha`, `phase_4bj_f_merge_closeout_commit_sha`
- `manifest_mutation_permitted`, `original_label_manifest_research_eligible`, `original_label_manifest_eligibility_gate_status`, `original_label_manifest_chronological_split_policy`, `original_label_manifest_must_remain_byte_identical`
- `next_phase_authorized` (redundant with `successor_authorizes_next_phase`; both recorded as `false` for defensive clarity)
- `governance_labels` (full mapping)
- `boundary_confirmations` (28-key block; see §11)
- `retained_verdict_ledger` (verbatim ledger)
- `preserved_project_locks` (verbatim list)
- `no_rescue_statement` (explicit no-rescue paragraph)
- `created_at_unix_ms`, `created_at_utc`, `code_commit_sha`, `base_main_commit_sha`, `predecessor_merge_closeout_commit_sha`, `precedent_phases`

---

## 11. Boundary confirmations (28 keys; all `true`)

| Key | Value |
| --- | ----- |
| `no_label_manifest_mutation` | `true` |
| `no_label_parquet_mutation` | `true` |
| `no_label_sidecar_mutation` | `true` |
| `no_gate_report_mutation` | `true` |
| `no_data_microstructure_write_outside_successor_state_namespace` | `true` |
| `no_data_microstructure_artefact_committed` | `true` |
| `no_research_eligible_manifest_flip` | `true` |
| `no_eligibility_gate_status_manifest_transition` | `true` |
| `no_chronological_split_policy_manifest_change` | `true` |
| `no_ml_training` | `true` |
| `no_ml_architecture_design` | `true` |
| `no_feature_ranking` | `true` |
| `no_meta_labeling` | `true` |
| `no_strategy_creation` | `true` |
| `no_signal_computation` | `true` |
| `no_backtest` | `true` |
| `no_data_acquisition` | `true` |
| `no_public_endpoint_use` | `true` |
| `no_binance_api_use` | `true` |
| `no_websocket` | `true` |
| `no_credentials` | `true` |
| `no_env` | `true` |
| `no_mcp_or_graphify` | `true` |
| `phase_4aw_flip_research_eligible_invariant_preserved` | `true` |
| `no_retained_verdict_revision` | `true` |
| `no_project_lock_change` | `true` |
| `no_m0_amendment` | `true` |
| `no_successor_authorization` | `true` |

---

## 12. Hash / sidecar verification

- The JSON was serialized once with `json.dumps(payload, sort_keys=True, indent=2) + "\n"` and encoded to UTF-8 bytes.
- SHA256 of those bytes: `ce7d391756ef347568374a9ee71e2cfaaa14d4f90ded969ab5771abe3fed2ea5`.
- The bytes were written atomically via `tmp + os.replace` to the target path.
- The on-disk file SHA256 was recomputed and matched the expected SHA exactly.
- The sidecar was written as `<sha>  <filename>\n` (158 bytes) and verified by parsing its first whitespace-separated token, which matches the recomputed JSON SHA.
- No other `data/microstructure/` artefact was created.

The implementation used a temporary, deterministic, gitignored helper file (`_phase4bj_g_writer.py`) that was deleted immediately after a successful write. The helper was at the repository root only during the write and is verified absent below:

```
git status --short | grep _phase4bj_g_writer   # (no output — file not tracked, not present)
```

The helper file is not part of any commit and is not referenced from any tracked file.

---

## 13. Label manifest / parquet / gate report preservation

| Artefact | Recorded SHA (locked) | Recomputed SHA (post-write) | Status |
| -------- | --------------------- | --------------------------- | ------ |
| Label parquet | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | `ef50038a3ff91ec9d42c741562521e2a14e8f5e134831349d7ba08f7580e8d26` | IDENTICAL |
| Label parquet sidecar | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | `b9681e6b029901a7f8379909b4d7bc5a753fa07764104519c3eb10e9fb45c78b` | IDENTICAL |
| Label manifest | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | `181a799c3b17d3365cb912d40fe3ce91b6a09daa94fa5bccf07f9a24f97ee0f3` | IDENTICAL |
| Label manifest sidecar | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | `3392a3364309e1392b8a790954db3ce5f68829911a477dfe825685fda3448a8d` | IDENTICAL |
| Phase 4bj-E gate report | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` | `b0b5405b94b916c2ce182f63b414b83887e4abddf422f18ae36d0bdc7273ead0` | IDENTICAL |
| Phase 4bj-E gate report sidecar | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` | `2f24ad3e378b13e51550dbe1891c43e1e91bc84229c02ea703cc910bd025d191` | IDENTICAL |

`mtime_ns` values for the three primary upstream artefacts (label parquet, label manifest, Phase 4bj-E gate report) are unchanged across the write. The on-disk label manifest still reads `research_eligible: false`, `eligibility_gate_status: "pending"`, `chronological_split_policy: "not_yet_defined"`, and every `governance_labels.*` value unchanged from the Phase 4bj-C output.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved end-to-end and was never invoked by this phase.

Predecessor successor-state artefacts (Phase 4bg-B derived family; Phase 4bi-D feature family) were not touched.

---

## 14. Machine-readable state interpretation

After Phase 4bj-G, the on-disk machine-readable state is:

| Object | Field | Value |
| ------ | ----- | ----- |
| Label manifest | `research_eligible` | `false` (unchanged) |
| Label manifest | `eligibility_gate_status` | `"pending"` (unchanged) |
| Label manifest | `chronological_split_policy` | `"not_yet_defined"` (unchanged) |
| Label manifest | `governance_labels.*` | every value unchanged |
| Phase 4bj-E gate report | `research_eligible_after` | `false` (unchanged) |
| Phase 4bj-E gate report | `eligibility_gate_status_after` | `"pass_report_level_only"` (unchanged; report-level recommendation only) |
| Phase 4bj-E gate report | `no_successor_authorization` | `true` (unchanged) |
| **Phase 4bj-G successor-state JSON (NEW)** | `successor_research_use_admissible` | `true` |
| **Phase 4bj-G successor-state JSON (NEW)** | `successor_ml_use_admissible` | `"conditional_future_only"` |
| **Phase 4bj-G successor-state JSON (NEW)** | `successor_admissibility_status` | `admissible_in_principle_policy_level_only` |
| **Phase 4bj-G successor-state JSON (NEW)** | `manifest_mutation_permitted` | `false` |
| **Phase 4bj-G successor-state JSON (NEW)** | `manifest_research_eligible_after` | `false` |
| **Phase 4bj-G successor-state JSON (NEW)** | `manifest_eligibility_gate_status_after` | `"pending"` |
| **Phase 4bj-G successor-state JSON (NEW)** | `manifest_chronological_split_policy_after` | `"not_yet_defined"` |
| **Phase 4bj-G successor-state JSON (NEW)** | `original_label_manifest_must_remain_byte_identical` | `true` |
| **Phase 4bj-G successor-state JSON (NEW)** | every `governance_labels.*` | forbidden / unauthorized |
| **Phase 4bj-G successor-state JSON (NEW)** | every `boundary_confirmations.*` | `true` |
| **Phase 4bj-G successor-state JSON (NEW)** | every `*_authorized` flag (19 keys) | `false` |
| **Phase 4bj-G successor-state JSON (NEW)** | `successor_authorizes_next_phase` | `false` |
| **Phase 4bj-G successor-state JSON (NEW)** | `recommended_state` | `remain_paused` |

Critical interpretation:

- The label-family research / ML-use admissibility marker exists **only** at the new sibling successor-state JSON (file path documented above).
- Any tool that wishes to interpret the label family as admissible in principle must read the successor-state JSON, never the label manifest, and never assume that `research_eligible=true` should be flipped on the label manifest.
- Label-family admissibility is a **governance state**, not an empirical claim about edge.
- Label-family admissibility is **not** a strategy hypothesis, **not** a predictive claim, **not** an edge claim, **not** a backtest permission, and **not** an M0 bypass.
- ML use is `conditional_future_only` — a future authorized phase must satisfy additional safeguards before any ML training under labels from this family.

---

## 15. Boundary confirmations narrative

This phase honoured every boundary confirmation enumerated in §11:

- no source code modified
- no tests modified
- no scripts modified
- no configs / README / pyproject / `.gitignore` / MCP files modified
- no data acquisition
- no public endpoint calls
- no Binance API calls
- no WebSocket
- no credential / `.env` / `.mcp.json` / MCP / Graphify
- no label kernel rerun
- no label-family eligibility-gate rerun
- no feature kernel rerun
- no feature-family eligibility-gate rerun
- no derived-family eligibility-gate rerun
- no normalizer rerun
- no raw eligibility-gate rerun
- no replacement label parquet / manifest / sidecar
- no replacement gate report
- no replacement feature parquet / manifest / sidecar
- no replacement normalized parquet / derived manifest
- no replacement raw manifest / raw zip
- no labels / targets / signals / ML / strategy / backtest artefacts
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output
- no tracked `data/microstructure/` output
- raw-family `research_eligible` remains `false`
- raw-family `eligibility_gate_status` remains `pending`
- derived manifest `research_eligible` remains `false`
- derived manifest `eligibility_gate_status` remains `pending`
- feature manifest `research_eligible` remains `false`
- feature manifest `eligibility_gate_status` remains `pending`
- label manifest `research_eligible` remains `false`
- label manifest `eligibility_gate_status` remains `pending`
- label manifest `chronological_split_policy` remains `not_yet_defined`
- Phase 4bj-E gate report's invariants preserved
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

---

## 16. What this phase proves

- a machine-readable label-family admissibility-in-principle marker now exists for `microstructure_labels_aggtrades_v001`;
- the marker exists only as a sibling gitignored successor-state JSON, never on the label manifest itself;
- the original label manifest is byte-identical pre/post Phase 4bj-G;
- the original label parquet is byte-identical pre/post Phase 4bj-G;
- both label sidecars are byte-identical pre/post Phase 4bj-G;
- the Phase 4bj-E gate report and its sidecar are byte-identical pre/post Phase 4bj-G;
- the Phase 4bg-B / Phase 4bi-D precedent (sibling-only, manifest-immutable) is correctly reproduced for the label family;
- the M0 admissibility gate, post-null cooldown rule, refined no-rescue rule, label-family boundary, and Phase 4aw invariant all remain binding.

---

## 17. What this phase does not prove

- the label family is **not** proven to have predictive validity;
- the label family is **not** proven to produce a tradable signal;
- the label family is **not** proven to be ML-trainable under any specific architecture;
- the label family's evidence chain is **not** generalised to additional symbols or additional UTC dates;
- no target evaluation has been performed;
- no train / validation / test split has been designed;
- no strategy hypothesis has been admitted under M0;
- no backtest has been run;
- no edge claim is made;
- no successor authorization is granted.

Label-family admissibility is a governance state, not an empirical claim about edge.

---

## 18. Preserved boundaries

- **Retained verdict ledger** (preserved verbatim): H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.
- **Project locks** (preserved verbatim): §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4am .. Phase 4bj-F results — all preserved verbatim.
- **No-rescue boundary**: label-family admissibility is upstream of M0 in the same sense as feature-family Stage-5 admissibility. M0 still applies to any future hypothesis, label evaluation, target, strategy, or backtest. Phase 4bj-G does not authorise rescue of any cooled-down family. Labels are not signals; labels are not strategy evidence; labels are not live-readiness evidence.
- **Label manifest immutability**: SHA `181a799c…` unchanged.
- **Label parquet immutability**: SHA `ef50038a…` unchanged.
- **Both label sidecar immutability**: SHA `b9681e6b…` and SHA `3392a336…` unchanged.
- **Phase 4bj-E gate report immutability**: SHA `b0b5405b…` unchanged.
- **Phase 4bj-E gate report sidecar immutability**: SHA `2f24ad3e…` unchanged.
- **Cross-artefact immutability**: six pre-existing upstream artefacts byte-for-byte unchanged; one new sibling successor-state artefact created plus paired sidecar.

---

## 19. Recommended future options

- **Primary**: remain paused.
- **Conditional next** (NOT authorised by Phase 4bj-G): not currently named. If the operator later wants to define a chronological-split or train / validation / test design phase, that would require a separate authorization prompt with explicit scope.
- **Conditional cleanup** (NOT authorised by Phase 4bj-G): future code + docs **Phase 4bb-F** — Gate Report Output Path Hygiene (only before any future repeated raw or feature-family or label-family gate execution).
- **Conditional raw-policy marker** (NOT authorised by Phase 4bj-G): future **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**FORBIDDEN** options:

- verdict revision;
- lock revision;
- parameter optimization;
- strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid);
- M0 amendment derived from Phase 4bj-G reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any actual manifest from this phase alone;
- transitioning `eligibility_gate_status` on any actual manifest from this phase alone;
- changing `chronological_split_policy` on any actual manifest from this phase alone;
- creating labels-as-signals / strategy-from-labels / ML training / backtests from this phase alone;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

Phase 4 (canonical) remains unauthorized. Phase 5 / any successor phase remains unauthorized.

---

## 20. Closeout / lock preservation

Phase 4bj-G is docs + local gitignored successor-state artefact recording. No source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, raw artefacts, derived artefacts, feature artefacts, label artefacts, manifests, sidecars, gate reports, or prior successor-state artefacts have been or will be modified by this phase. The single new successor-state JSON and its paired sidecar exist only under the gitignored `data/microstructure/successor-state/` namespace and are NOT committed to git.

Phase 4bj-G preserves verbatim:

- the retained verdict ledger;
- the project locks;
- the M0 twelve-clause gate;
- the post-null cooldown rule;
- the cooled-down families list;
- the Phase 4al refined no-rescue rule;
- the Phase 4al §13 boundary and §14 hierarchy;
- the Phase 3v §8 stop-trigger-domain governance;
- the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance;
- the Phase 4j §11 metrics OI-subset partial-eligibility rule;
- the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant;
- every prior phase's recorded outcomes.

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bj-G.**
