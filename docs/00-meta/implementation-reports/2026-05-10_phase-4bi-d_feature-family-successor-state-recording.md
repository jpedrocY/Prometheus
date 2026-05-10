# Phase 4bi-D — Feature-Family Successor-State Recording

**Phase identity:** Phase 4bi-D — Feature-Family Successor-State Recording (docs + local gitignored successor-state artefact recording).
**Date:** 2026-05-10.
**Branch:** `phase-4bi-d/feature-family-successor-state-recording`.
**Base:** `main` at the post-Phase-4bi-C merge-closeout state. Phase 4bi-C merge commit `62bba715a08a5b29e31bca125041f51a2a6f9ddc` confirmed as ancestor of `main`.
**Status:** drafted; pending operator review.
**Phase type:** docs + local gitignored successor-state artefact recording.

---

## 1. Phase header

This phase converts the Phase 4bi-C policy-level Stage-5 admissibility decision into a single machine-readable sibling successor-state JSON artefact (plus paired SHA256 sidecar) under the gitignored `data/microstructure/successor-state/` namespace, while preserving the original feature manifest byte-identically and preserving all manifest state, all retained verdicts, and all project locks.

The phase is deliberately narrow:

- it records Stage-5 admissibility **only** at the sibling successor-state artefact level;
- it must not flip `research_eligible` on any actual manifest;
- it must not transition `eligibility_gate_status` on any actual manifest;
- it must not create labels, targets, signals, ML, strategy, backtests, or acquisition;
- it must not authorize any successor.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| Phase 4bi-C merge commit | `62bba715a08a5b29e31bca125041f51a2a6f9ddc` |
| Phase 4bi-C merge-closeout file (on `main`) | `docs/00-meta/implementation-reports/2026-05-10_phase-4bi-c_merge-closeout.md` |
| Phase 4bi-C policy decision | Outcome 1 / Decision form 1 — Stage-5 admissible in principle at policy level |
| Code commit SHA at start of Phase 4bi-D | `b3bb6dbe7dceb097af0346cf0e7318ff48669b28` |
| Raw family | `microstructure_raw_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Derived family | `microstructure_normalized_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Feature family | `microstructure_features_aggtrades_v001`, `research_eligible=false`, `eligibility_gate_status=pending` |
| Symbol scope | BTCUSDT only |
| UTC date scope | `2025-01-15` |
| Feature row count | `1 681 098` |
| Schema columns | 61 (45 features + 16 lineage) |
| Feature config hash | `49b4ec1fd63688cc11d72ea7286af6efe2bad8ac5c29da0438c0f65d571f0c77` |
| Phase 4bi-B feature-family gate report SHA256 | `aa5d29c2bd18755625a95b7c2b59d9199785d1f2f2617b7fb6111e78f64d7988` |
| Feature parquet SHA256 | `618d9b86426df8322a5924392266562dd558cf05e36d0447713b97a2b4c1691f` |
| Feature manifest SHA256 | `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` |
| `data/microstructure/` gitignore | `.gitignore:85` (covers `successor-state/` as a subpath) |

---

## 3. Inputs reviewed

- Phase 4az acquisition + Phase 4bb-D raw eligibility gate.
- Phase 4bd normalization + Phase 4be structural QA + Phase 4bf derived-family eligibility gate.
- Phase 4bg-A derived-family research-eligibility decision + Phase 4bg-B derived-family successor-state JSON.
- Phase 4bh-A feature-boundary design + Phase 4bh-B feature schema finalization + Phase 4bh feature kernel implementation + Phase 4bi-A feature artefact structural QA + Phase 4bi-B feature-family eligibility gate (70/70 PASS).
- Phase 4bi-C policy decision (Outcome 1 / Decision form 1).
- Phase 4bi-C merge closeout (10 upstream artefacts byte-identical pre/post).

No prior memo's text was modified by Phase 4bi-D. No prior `data/microstructure/` artefact was modified.

---

## 4. Scope

In scope for this phase:

- creating exactly one local gitignored successor-state JSON under `data/microstructure/successor-state/` recording Stage-5 research-use / ML-use admissibility for the feature family `microstructure_features_aggtrades_v001`;
- creating exactly one paired `.sha256` sidecar file matching the JSON's bytes;
- citing the Phase 4bi-B gate report id and SHA verbatim;
- citing the Phase 4bi-C policy-decision evidence verbatim;
- citing all upstream artefact SHAs verbatim;
- preserving the original feature manifest byte-identically (SHA `624e8c5e…`);
- preserving `research_eligible=false` and `eligibility_gate_status=pending` on the original feature manifest;
- documenting the action in this memo and a closeout, plus a narrow `current-project-state.md` paragraph and "Current phase:" block update with the prior Phase 4bi-C block preserved.

---

## 5. Non-scope

This phase does **not**:

- modify any source code, test, script, configuration, dataset, manifest, or Phase 4bi-B gate report;
- run the normalizer, raw eligibility gate, derived-family gate, feature kernel, or feature-family eligibility gate;
- generate any new gate report;
- create any normalized parquet, derived manifest, feature parquet, feature manifest, gate report, or any other `data/microstructure/` artefact beyond the one new successor-state JSON and its paired sidecar;
- create labels, targets, signals, ML, strategy, or backtest artefacts;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, execution-quality proxies, regime, momentum, volatility, PnL, MFE, MAE, R-multiple, equity, position state, prediction, model score, decision score, or entry / exit signal;
- train ML;
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
- mutate the feature manifest or any upstream manifest in any way;
- amend M0;
- revise any retained verdict;
- change any project lock;
- authorize Phase 4bj-A, Phase 4bj, Phase 4bb-F, Phase 4bb-G, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation;
- commit anything under `data/microstructure/`.

---

## 6. Phase 4bi-C dependency

This phase depends entirely on Phase 4bi-C's locked outputs:

- Phase 4bi-C is merged into `main` at merge commit `62bba715a08a5b29e31bca125041f51a2a6f9ddc`.
- Phase 4bi-C selected **Outcome 1 / Decision form 1**: *Stage-5 research-use / ML-use admissibility is admissible in principle at policy level for `microstructure_features_aggtrades_v001`, but no manifest mutation occurs in this phase. A separately authorized Phase 4bi-D successor-state recording phase is required before any machine-readable Stage-5 marker exists.*
- Phase 4bi-C explicitly named Phase 4bi-D as the conditional next step. This memo and its successor-state artefact are the recorded execution of that step.

This phase does not re-derive Phase 4bi-C's evidence; it cites it as locked input.

---

## 7. Successor-state recording objective

The Phase 4bg-B precedent established a sibling successor-state JSON pattern for the derived family. Phase 4bi-D applies the same pattern to the feature family:

- one JSON file at a deterministic path under the gitignored `data/microstructure/successor-state/` namespace;
- one paired `.sha256` sidecar with the format `<sha256>  <filename>\n`;
- canonical sorted-key, indent-2 JSON serialization, with trailing newline;
- atomic write-then-rename via `os.replace`;
- refuse-overwrite on either file;
- byte-for-byte preservation of every upstream artefact, including the original feature manifest.

The successor-state JSON is the **only** machine-readable place where Stage-5 admissibility is recorded. The original feature manifest's `research_eligible` and `eligibility_gate_status` fields **must not** be flipped or transitioned by this phase or by any tooling that relies on this artefact.

---

## 8. Successor-state artefact path

| Item | Value |
| ---- | ----- |
| JSON path | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json` |
| Sidecar path | `data/microstructure/successor-state/microstructure_features_aggtrades_v001__v001__stage5_research_ml_admissible__phase-4bi-d.json.sha256` |
| JSON SHA256 | `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a` |
| JSON size | 4 428 bytes |
| Sidecar size | 160 bytes |
| Sidecar match | matches recomputed bytes |
| Gitignore | `.gitignore:85` covers both files (under `data/microstructure/`) |
| Tracked in git | NO — both files are gitignored and are NOT committed |

The path scheme mirrors the Phase 4bg-B precedent (`microstructure_normalized_aggtrades_v001__v001__stage3_research_eligible__phase-4bg-b.json`) and is unique to the feature family Stage-5 marker.

---

## 9. Successor-state schema

The JSON payload contains, at minimum:

- `schema_version = "v001"`
- `phase_id = "4bi-D"`
- `dataset_family`, `dataset_version`, `feature_schema_version`
- `symbol`, `utc_date`
- `successor_state_type = "feature_family_stage5_research_ml_admissibility"`
- `successor_stage = "Feature Stage-5"`
- `successor_research_ml_admissible = true`
- `successor_research_eligible = true`
- `successor_eligibility_gate_status = "pass"`
- `successor_policy_decision`, `successor_policy_decision_phase = "4bi-C"`, `successor_policy_decision_outcome = "Outcome 1 / Decision form 1"`
- `original_feature_manifest_research_eligible = false`
- `original_feature_manifest_eligibility_gate_status = "pending"`
- `original_feature_manifest_sha256 = "624e8c5e…"` (verbatim)
- `original_feature_manifest_must_remain_byte_identical = true`
- `manifest_mutation_permitted = false`
- `feature_parquet_sha256`, `feature_config_hash`, `feature_row_count`, `schema_columns`, `feature_quality_columns`, `lineage_identity_metadata_columns`
- `phase_4bh_validation` (135 / 135 PASS)
- `phase_4bi_a_structural_qa` (67 / 67 + 18 / 18 PASS; same-T tie-break PASS; validate 135 / 135 PASS)
- `phase_4bi_b_feature_family_gate` (report id + SHA verbatim; 70 / 70 PASS)
- `phase_4bi_c_policy_decision` (memo path, merge-closeout path, merge commit SHA, selected outcome, decision text, `machine_readable_marker_required = true`)
- `upstream_artefact_shas` (normalized parquet, derived manifest, raw manifest, raw zip, Phase 4bb-D gate report, Phase 4bf gate report, Phase 4bg-B successor-state — all verbatim)
- `governance_labels` (labels / targets / ml / strategy / backtest / acquisition / paper_shadow_live / deployment / exchange_write — all forbidden / unauthorized)
- `boundary_confirmations` (17 keys all `true`: no_feature_manifest_mutation; no_prior_manifest_mutation; no_feature_parquet_mutation; no_gate_report_mutation; no_labels; no_targets; no_signals; no_ml_training; no_strategy; no_backtest; no_acquisition; no_network; no_credentials; no_mcp_or_graphify; no_m0_amendment; no_retained_verdict_revision; no_successor_authorization)
- `created_at_unix_ms = 1778445390206`
- `created_at_utc = "2026-05-10T20:36:30.206830Z"`
- `code_commit_sha = "b3bb6dbe7dceb097af0346cf0e7318ff48669b28"`

The serialization is deterministic: `json.dumps(payload, sort_keys=True, indent=2) + "\n"`.

---

## 10. Hash / sidecar verification

- The JSON was serialized to bytes once; the SHA256 of those bytes was computed.
- The bytes were written atomically via `tmp + os.replace`.
- The on-disk file SHA256 was recomputed and matched the expected SHA exactly: `8176aa3fea1b78a0776fe13cd28053843b0ea67eb3fc3a894848e6bf41ce808a`.
- The sidecar was written as `<sha>  <filename>\n` (160 bytes including the trailing newline) and verified by parsing its first whitespace-separated token, which matches the recomputed JSON SHA.
- No other `data/microstructure/` artefact was created.

---

## 11. Feature manifest preservation

The feature manifest at `data/microstructure/manifests/microstructure_features_aggtrades_v001__v001.json` was **not** modified. SHA256 `624e8c5eac9276fa179df33594255636f9a620937dd2fa9e0a56fdd3997fe718` is byte-for-byte identical pre- and post-Phase-4bi-D. The on-disk fields:

- `research_eligible = false` (unchanged)
- `eligibility_gate_status = pending` (unchanged)
- `governance_labels.labels = forbidden` (unchanged)
- `governance_labels.ml = forbidden` (unchanged)
- `governance_labels.strategy = forbidden` (unchanged)
- `governance_labels.backtest = forbidden` (unchanged)
- `governance_labels.acquisition = unauthorized` (unchanged)
- `governance_labels.feature_computation = allowed_by_phase_4bh` (unchanged)
- `governance_labels.stop_trigger_domain = trade_price_backtest_candidate` (unchanged)
- `governance_labels.phase_id = 4bh` (unchanged)

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant remains preserved end-to-end and was never invoked by this phase.

The Phase 4bg-B successor-state JSON (derived family) was likewise not touched.

The Phase 4bi-B feature-family gate report and its sidecar were not touched.

---

## 12. Machine-readable state interpretation

After Phase 4bi-D, the on-disk machine-readable state is:

| Object | Field | Value |
| ------ | ----- | ----- |
| Feature manifest | `research_eligible` | `false` (unchanged) |
| Feature manifest | `eligibility_gate_status` | `pending` (unchanged) |
| Feature manifest | `governance_labels.labels` | `forbidden` (unchanged) |
| Feature manifest | `governance_labels.ml` | `forbidden` (unchanged) |
| Feature manifest | `governance_labels.strategy` | `forbidden` (unchanged) |
| Feature manifest | `governance_labels.backtest` | `forbidden` (unchanged) |
| Feature manifest | `governance_labels.acquisition` | `unauthorized` (unchanged) |
| Phase 4bi-B gate report | `research_eligible_after` | `false` (unchanged) |
| Phase 4bi-B gate report | `feature_manifest_research_eligible_after` | `false` (unchanged) |
| Phase 4bi-B gate report | `feature_manifest_eligibility_gate_status_after` | `pending` (unchanged) |
| Phase 4bi-B gate report | `stage_5_authorized` | `false` (unchanged) |
| Phase 4bi-B gate report | `stage_5_research_or_ml_use` | `false` (unchanged) |
| Phase 4bi-B gate report | `no_successor_authorization` | `true` (unchanged) |
| **Phase 4bi-D successor-state JSON (NEW)** | `successor_research_ml_admissible` | `true` |
| **Phase 4bi-D successor-state JSON (NEW)** | `successor_research_eligible` | `true` |
| **Phase 4bi-D successor-state JSON (NEW)** | `successor_eligibility_gate_status` | `pass` |
| **Phase 4bi-D successor-state JSON (NEW)** | `manifest_mutation_permitted` | `false` |
| **Phase 4bi-D successor-state JSON (NEW)** | `original_feature_manifest_research_eligible` | `false` |
| **Phase 4bi-D successor-state JSON (NEW)** | `original_feature_manifest_eligibility_gate_status` | `pending` |
| **Phase 4bi-D successor-state JSON (NEW)** | `original_feature_manifest_must_remain_byte_identical` | `true` |
| **Phase 4bi-D successor-state JSON (NEW)** | every `governance_labels.*` | forbidden / unauthorized |
| **Phase 4bi-D successor-state JSON (NEW)** | every `boundary_confirmations.*` | `true` |

Critical interpretation:

- The Stage-5 admissibility marker exists **only** at the new sibling successor-state JSON (file path documented above).
- Any tool that wishes to interpret the feature family as Stage-5-admissible must read the successor-state JSON, never the feature manifest, and never assume that `research_eligible=true` should be flipped on the manifest.
- Stage-5 admissibility is **not** a strategy hypothesis, **not** a predictive claim, **not** an edge claim, **not** a backtest permission, and **not** an M0 bypass.

---

## 13. Boundary confirmations

- no source code modified
- no tests modified
- no scripts modified
- no configs / README / pyproject / `.gitignore` / MCP files modified
- no data acquisition
- no public endpoint calls
- no Binance API calls
- no WebSocket
- no credential / `.env` / `.mcp.json` / MCP / Graphify
- no normalizer rerun
- no raw eligibility-gate rerun
- no derived-family eligibility-gate rerun
- no feature kernel rerun
- no feature-family eligibility-gate rerun
- no replacement feature parquet
- no replacement feature manifest
- no replacement gate report
- no replacement upstream artefact
- no labels / targets / signals / ML / strategy / backtest artefacts
- no PnL / MFE / MAE / R-multiple / equity / position / alpha / edge / prediction / model-score / decision-score / entry-exit / strategy output
- no tracked `data/microstructure/` output
- raw-family `research_eligible` remains `false`
- raw-family `eligibility_gate_status` remains `pending`
- original derived manifest `research_eligible` remains `false`
- original derived manifest `eligibility_gate_status` remains `pending`
- feature manifest `research_eligible = false` (unchanged)
- feature manifest `eligibility_gate_status = pending` (unchanged)
- Phase 4bi-B gate report's `stage_5_authorized = false` and `no_successor_authorization = true` invariants preserved
- Phase 4aw `flip_research_eligible(...)` always-raises invariant preserved (never invoked)
- no retained verdict revised
- no project lock loosened
- no M0 amendment
- no successor authorized

---

## 14. What this phase proves

- a machine-readable Stage-5 admissibility marker now exists for `microstructure_features_aggtrades_v001`;
- the marker exists only as a sibling gitignored successor-state JSON, never on the feature manifest itself;
- the original feature manifest is byte-identical pre/post Phase 4bi-D;
- the entire upstream evidence chain (10 artefacts) is byte-identical pre/post Phase 4bi-D;
- the Phase 4bg-B precedent (sibling-only, manifest-immutable) is correctly reproduced for the feature family;
- the M0 admissibility gate, post-null cooldown rule, refined no-rescue rule, and feature-family boundary all remain binding.

---

## 15. What this phase does not prove

- the feature family is **not** proven to have predictive validity;
- the feature family is **not** proven to produce a tradable signal;
- the feature family's evidence chain is **not** generalised to additional symbols or additional UTC dates;
- no label has been designed;
- no target has been defined;
- no train / validation / test split has been designed;
- no strategy hypothesis has been admitted under M0;
- no backtest has been run;
- no edge claim is made;
- no successor authorization is granted.

Stage-5 admissibility is a governance state, not an empirical claim about edge.

---

## 16. Preserved boundaries

- **Retained verdict ledger** (preserved verbatim): H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per Phase 3t; V2 HARD REJECT — terminal for V2 first-spec; G1 HARD REJECT — terminal for G1 first-spec; C1 HARD REJECT — terminal for C1 first-spec.
- **Project locks** (preserved verbatim): §11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 = 0.25% / 2× / one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q; Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template; Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D, 4bb-E, 4bc, 4bd-A, 4bd, 4be, 4bf-A, 4bf, 4bg-A, 4bg-B, 4bh-A, 4bh-B, 4bh, 4bi-A, 4bi-B, 4bi-C preserved verbatim.
- **No-rescue boundary**: Stage-5 admissibility is upstream of M0. M0 still applies to any future hypothesis, label, target, strategy, or backtest. Phase 4bi-D does not authorise rescue of any cooled-down family.
- **Feature-manifest immutability**: SHA `624e8c5e…` unchanged.
- **Feature-parquet immutability**: SHA `618d9b86…` unchanged.
- **Phase 4bi-B gate report immutability**: SHA `aa5d29c2…` unchanged.
- **Phase 4bg-B successor-state immutability**: SHA `8bcc7d01…` unchanged.
- **Cross-artefact immutability**: nine pre-existing upstream artefacts byte-for-byte unchanged; one new sibling successor-state artefact created plus paired sidecar.

---

## 17. Recommended future options

- **Primary**: remain paused.
- **Conditional next** (NOT authorised by Phase 4bi-D): future docs-only **Phase 4bj-A** — Label Boundary / Target Definition Memo. This is the next admissibility layer upstream of any ML-use implementation, and it is allowed in principle now that a machine-readable Stage-5 admissibility marker exists. Authorization for Phase 4bj-A is a separate operator decision.
- **Conditional cleanup** (NOT authorised by Phase 4bi-D): future code + docs **Phase 4bb-F** — Gate Report Output Path Hygiene (only before any future repeated raw or feature-family gate execution).
- **Conditional raw-policy marker** (NOT authorised by Phase 4bi-D): future **Phase 4bb-G** — Raw Manifest Successor-State Recording.

**FORBIDDEN** options:

- verdict revision;
- lock revision;
- parameter optimization;
- strategy resurrection (R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid);
- M0 amendment derived from Phase 4bi-D reasoning;
- reopening the 5m research thread;
- flipping `research_eligible` to `true` on any actual manifest from this phase alone;
- transitioning `eligibility_gate_status` on any actual manifest from this phase alone;
- creating labels / targets / signals / ML / strategy / backtests from this phase alone;
- paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

Phase 4 (canonical) remains unauthorized. Phase 4bj-A / Phase 4bj / Phase 4bb-F / Phase 4bb-G / Phase 5 / any successor phase remains unauthorized.

---

## 18. Closeout / lock preservation

Phase 4bi-D is docs + local gitignored successor-state artefact recording. No source code, tests, scripts, configs, README, pyproject, `.gitignore`, MCP files, raw artefacts, derived artefacts, feature artefacts, manifests, sidecars, gate reports, or prior successor-state artefacts have been or will be modified by this phase. The single new successor-state JSON and its paired sidecar exist only under the gitignored `data/microstructure/successor-state/` namespace and are NOT committed to git.

Phase 4bi-D preserves verbatim:

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
- every prior phase's recorded outcomes.

**Recommended state: remain paused.**

**No successor phase is authorized by Phase 4bi-D.**
