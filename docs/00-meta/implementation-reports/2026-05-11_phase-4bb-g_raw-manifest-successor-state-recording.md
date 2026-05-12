# Phase 4bb-G — Raw Manifest Successor-State Recording

## §1. Phase identity

- **Phase identifier:** Phase 4bb-G
- **Phase name:** Raw Manifest Successor-State Recording
- **Phase type:** Docs + local gitignored successor-state artefact
  recording phase. Mirrors the Phase 4bg-B (derived family), Phase
  4bi-D (feature family), and Phase 4bj-G (label family) precedents,
  transposed to the raw family `microstructure_raw_aggtrades_v001`.
- **Authorization basis:** Operator authorization specific to Phase
  4bb-G. The Phase 4bb-E successor-state policy memo §6 lists this
  raw-family successor-state recording as the conditional
  implementation of Option B and notes that the prior Phase 4bb-E /
  4bb-F memos did not authorize it.

## §2. Pre-state

- **Main HEAD at start of phase:**
  `07d6ea7c612abbdde370b131af541a9a4c37b969`
  — the Phase 4bb-F-implementation SHA-chain-fixup commit on top of
  merge-closeout `b1c49a12fd931a64e9c7d46821739432acd94479`. Per the
  Phase 4bb-F-implementation merge-closeout §2 SHA-chain-fixup
  recording convention, the merge-closeout commit `b1c49a1` is the
  canonical project-complete anchor; `07d6ea7` is the one-commit fixup
  that records the merge-closeout SHA into §2 of the merge-closeout.
- **`origin/main` at start of phase:** `07d6ea7c612abbdde370b131af541a9a4c37b969`.
- **Branch created:** `phase-4bb-g/raw-manifest-successor-state-recording`
  from `main` at `07d6ea7`.
- **Working tree pre-phase:** clean apart from the always-untracked
  `.claude/scheduled_tasks.lock` and the gitignored `data/research/`.

## §3. Goal

Record exactly one sibling raw-family successor-state JSON artefact for
`microstructure_raw_aggtrades_v001` to complete raw-family governance
symmetry with the derived (Phase 4bg-B), feature (Phase 4bi-D), and
label (Phase 4bj-G) successor-state artefacts.

The raw manifest's `research_eligible = false` and
`eligibility_gate_status = "pending"` must remain permanent on the
original manifest. The admissibility marker must live only in the
sibling successor-state JSON.

## §4. Local artefacts produced

Two files under the gitignored `data/microstructure/successor-state/`
namespace (`.gitignore:85: data/microstructure/`):

1. **Successor-state JSON**
   - Path: `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`
   - Size: 12,726 bytes
   - SHA256: `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452`
   - Encoding: UTF-8; deterministic JSON (`sort_keys=True`, `indent=2`); no
     trailing newline.

2. **Paired SHA256 sidecar**
   - Path: `data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`
   - Size: 158 bytes
   - SHA256: `8ed0fbc0c31bc7f228ccfb35b92968f99dbbef06ef6b0d07621b14baeb41ef46`
   - Body (exact): `ab6a82e7d2e7aebd2e88986975390e7f2364dd32364b8ea9f0f169ee403ab452  microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json\n`
     (two spaces between hash and basename; trailing newline).

Both files are gitignored, **not staged**, and **not committed**. They
are reproducible from the source artefact SHAs and the Phase 4bb-F-
implementation `canonical_paths` helpers.

## §5. Naming convention

The filename uses the canonical Phase 4bb-F successor-state convention:

```text
<dataset_family>__<dataset_version>__<stage_marker>__phase-<phase_id>.json
```

- `dataset_family` = `microstructure_raw_aggtrades_v001`
- `dataset_version` = `v001`
- `stage_marker` = `stage2_raw_admissible`
- `phase_id` = `4bb-g`

The stage marker `stage2_raw_admissible` reflects the Phase 4ba
five-stage eligibility ladder position for the raw family: Stage-2
(gate-passed) at the report level only, with raw-family
`research_eligible` permanently `false` (the raw family cannot reach
Stage-3 by design — Stage-3 applies only to derived families). The
marker differs from the derived (`stage3_research_eligible`) and
feature / label (`stage5_research_ml_admissible`) markers because raw
admissibility is structural-integrity admissibility only.

## §6. Mechanism

The Phase 4bb-F-implementation `canonical_paths` helpers were used to
compose the canonical successor-state filename, derive the canonical
path under `data/microstructure/successor-state/`, and write the
paired SHA256 sidecar in the canonical two-space + trailing-newline
format:

- `compose_canonical_successor_state_filename(...)` produced the
  filename `microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g`.
- `derive_canonical_successor_state_path(...)` produced the full path
  under the gitignored successor-state namespace.
- `write_paired_sha256_sidecar(...)` wrote the sidecar atomically with
  refuse-overwrite discipline.

The JSON was serialised via `json.dumps(payload, indent=2, sort_keys=True)`
to keep the payload byte-deterministic and reviewable.

A one-off helper script `_phase4bb_g_writer.py` was used to drive the
write, ran exactly once successfully, and was deleted immediately
after. It was never staged, never tracked, and not committed.

## §7. Successor-state payload — semantic summary

The 12,726-byte JSON records:

- **Identity:** `schema_version=v001`, `phase=Phase 4bb-G`,
  `phase_id=4bb-G`, `artefact_type=raw_family_successor_state`,
  `successor_state_family=microstructure_raw_aggtrades_v001`,
  `successor_state_version=v001`,
  `successor_state_type=raw_family_successor_state_record`.
- **Source raw artefacts** (exact paths and SHAs):
  - raw manifest `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json`
    (SHA `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`)
  - raw zip `data/microstructure/raw/microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.zip`
    (SHA `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`)
  - raw zip sidecar (SHA `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d`)
  - acquisition log (SHA `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c`)
  - **Raw manifest has no separate `.sha256` sidecar on disk**, so the
    `source_raw_manifest_sidecar_sha256` field is `null` in the payload.
- **Phase 4bb-D gate report references** (verified from the on-disk
  payload):
  - path `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`
  - SHA `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`
  - sidecar SHA `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8`
  - `overall_status = pass`
  - 45 / 45 PASS / 0 FAIL / 0 ERROR / 0 NOT_APPLICABLE
  - `research_eligible_after = false`
  - `eligibility_gate_status_after = pass` (report-level only)
  - `no_successor_authorization = true`
  - `code_commit_sha = aa612ba2778c97a5150b80064244b90d024bfa54`
  - `created_at_utc_ms = 1778351069361`
  - `phase_4bb_d_gate_report_path_is_doubled_gate_reports = true`
    (documented Phase 4bb-C orchestrator behaviour; Phase 4bb-F locked
    the canonical policy prospectively only and explicitly does NOT
    migrate this artefact).
- **Phase 4bb-E policy decision:** raw-family `research_eligible=false`
  permanent on the original manifest; admissibility marker required to
  live only in a sibling successor-state artefact.
- **Phase 4bb-F / Phase 4bb-F-implementation references:** canonical
  successor-state root recorded; helpers used named explicitly.
- **Successor admissibility semantics:**
  - `successor_admissibility_status = admissible_in_principle_policy_level_only`
  - `successor_admissibility_kind = raw_family_structural_integrity_admissibility_only`
  - `successor_raw_use_admissible = true`
  - `successor_research_use_admissible = "conditional_future_only"`
  - `successor_ml_use_admissible = false`
  - `successor_stage = raw_family_successor_state_recorded`
  - `manifest_research_eligible_after = false`
  - `manifest_eligibility_gate_status_after = "pending"`
  - `manifest_mutation_permitted = false`
  - `original_raw_manifest_must_remain_byte_identical = true`
  - `original_raw_zip_must_remain_byte_identical = true`
  - `original_gate_report_must_remain_byte_identical = true`
- **Non-authorizations:** all 21 `*_authorized` boolean fields are
  `false`. `successor_authorizes_next_phase = false`. `recommended_state
  = "remain_paused"`.
- **Boundary confirmations:** 41 boolean keys, all `true`.
- **Retained verdict ledger:** 11 verdicts preserved verbatim
  (H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow
  RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A
  MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED;
  V2 HARD REJECT terminal; G1 HARD REJECT terminal; C1 HARD REJECT
  terminal).
- **Preserved project locks:** 17 locks recorded (§11.6, round-trip,
  §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8,
  Phase 4j §11, Phase 4k, Phase 4p, Phase 4q, Phase 4v, Phase 4w,
  Phase 4ak M0 twelve-clause gate + post-null cooldown + cooled-down
  families list + memo template, Phase 4al refined no-rescue rule +
  §13 boundary + §14 hierarchy, Phase 4aw `flip_research_eligible(...)`
  always-raises invariant, Phase 4bb-F canonical path policy).
- **No-rescue statement** verbatim records that Phase 4bb-G does NOT
  reopen R2 / F1 / D1-A / V2 / G1 / C1 / the 5m thread, does NOT
  authorize any strategy hypothesis, ML phase, label-evaluation phase,
  Phase 4 canonical, Phase 5, paper / shadow, live-readiness,
  exchange-write, deployment, or production-key creation.
- **Lifecycle anchor:** `base_main_commit_sha = "07d6ea7c612abbdde370b131af541a9a4c37b969"`
  with `base_main_lifecycle_anchor` explanatory note pointing to
  merge-closeout `b1c49a1` as the canonical Phase 4bb-F-implementation
  project-complete anchor.
- `created_at_unix_ms` and `created_at_utc` recorded at write time.

## §8. Upstream immutability evidence

Every upstream artefact SHA256 was recomputed before and after the
write. All six were byte-for-byte identical:

| Artefact | SHA256 |
|---|---|
| raw manifest | `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201` |
| raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| raw zip sidecar | `b80c27682689a97db5811f43c0e35036f884256b1cfce32d166f974aa605b42d` |
| acquisition log | `f88b28b48ceb9d0aefff3f8e7738254e2e5c57982bd8f84c1ffeeba90dec8a1c` |
| Phase 4bb-D gate report | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| Phase 4bb-D gate report sidecar | `93e68eb60d7b611f5220a7d354d97eb94b101420b1fc76373158844b6b649dc8` |

`mtime_ns` was also unchanged for the three primary upstream artefacts:

- raw manifest: `1778187340311355300` (pre == post)
- raw zip: `1778187330570003400` (pre == post)
- Phase 4bb-D gate report: `1778351069364441100` (pre == post)

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
always-raises invariant was preserved — never invoked.

## §9. Validation

- `git status --short`: only the always-untracked `.claude/scheduled_tasks.lock`
  and the gitignored `data/research/`. **No `data/microstructure/`
  artefact is staged or committed.**
- `git diff --check`: clean.
- `git check-ignore -v data/microstructure/successor-state/`:
  `.gitignore:85:data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json`:
  `.gitignore:85:data/microstructure/`.
- `git check-ignore -v data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v001__stage2_raw_admissible__phase-4bb-g.json.sha256`:
  `.gitignore:85:data/microstructure/`.
- ruff / mypy / pytest: **not rerun** because Phase 4bb-G changes no
  source code and no tests. The Phase 4bb-F-implementation merge
  validation remains the latest authoritative whole-repo validation
  (`ruff PASS`, `mypy strict 120 source files PASS`, `pytest tests/research/microstructure/`
  915 passed + 1 pre-existing labelled placeholder skip, whole-repo
  pytest 1698 passed + 1 skipped + 2 pre-existing simulation failures).

## §10. Boundary confirmations

Phase 4bb-G did NOT:

- modify the raw manifest, raw zip, raw zip sidecar, acquisition log,
  derived manifest, normalized parquet, feature parquet, feature
  manifest, label parquet, or label manifest;
- modify the Phase 4bb-D gate report or its sidecar;
- modify the Phase 4bg-B / Phase 4bi-D / Phase 4bj-G successor-state
  artefacts or their sidecars;
- migrate the Phase 4bb-D doubled-path gate report to canonical
  placement (Phase 4bb-F §6 preserves it at its recorded path);
- create a new gate report or rerun any gate (raw / derived / feature
  / label);
- commit anything under `data/microstructure/`;
- modify any source code, test, script, configuration, `pyproject.toml`,
  `README.md`, `.gitignore`, MCP file, runtime configuration, or prior
  governance memo (beyond the narrow `current-project-state.md`
  paragraph addition);
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- change `chronological_split_policy` on any actual manifest;
- compute features, labels, signals, ML, strategy, backtest, PnL, MFE,
  MAE, R-multiple, equity, position, alpha, edge, prediction,
  model-score, decision-score, entry-exit, or strategy output;
- acquire data;
- call any Binance, public, or private endpoint;
- open any WebSocket;
- use any credential;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- revise any retained verdict;
- change any project lock;
- amend M0 governance;
- merge into `main`;
- authorize Phase 4bb-H, Phase 5, Phase 4 canonical, paper / shadow,
  live-readiness, deployment, exchange-write, production-key creation,
  authenticated APIs, private endpoints, user stream, or live
  WebSocket implementation.

## §11. Retained verdict ledger preserved verbatim

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow RETAINED —
NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A MECHANISM PASS /
FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED; V2 HARD REJECT
terminal; G1 HARD REJECT terminal; C1 HARD REJECT terminal.

## §12. Preserved project locks

§11.6 = 8 bps per side; round-trip = 16 bps; §1.7.3 0.25% / 2× /
one-position / mark-price stops; Phase 3p §4.7; Phase 3r §8; Phase 3v
§8; Phase 3w §6 / §7 / §8; Phase 4j §11; Phase 4k; Phase 4p; Phase 4q;
Phase 4v; Phase 4w; Phase 4ak M0 twelve-clause gate + post-null
cooldown + cooled-down families list + memo template; Phase 4al
refined no-rescue rule + §13 boundary + §14 hierarchy; Phase 4aw
`MicrostructureManifest.flip_research_eligible(...)` always-raises
invariant; Phase 4bb-F canonical path policy (prospective only;
preserves Phase 4bb-D doubled-path artefact).

## §13. No-rescue statement

Phase 4bb-G is a raw-family successor-state policy marker only. It
does NOT reopen any cooled-down family (R2 / F1 / D1-A / V2 / G1 / C1
/ the 5m thread), does NOT authorize any strategy hypothesis, ML or
label-evaluation phase, Phase 4 canonical, Phase 5, paper / shadow,
live-readiness, exchange-write, deployment, or production-key creation,
and does NOT license any rescue interpretation of the cumulative
six-candidate rejection topology. The Phase 4ak M0 twelve-clause gate,
post-null cooldown rule, cooled-down families list, and Phase 4al
refined no-rescue rule remain binding.

## §14. Recommended state

**Remain paused.** No successor phase is authorized by Phase 4bb-G.

## §15. Successor authorization

**None.**

Candidate successor phases not authorized by Phase 4bb-G include:

- Phase 4bb-H (or any further raw-family follow-up);
- Phase 5;
- Phase 4 canonical;
- any ML / strategy / signal / backtest / label-evaluation phase;
- any acquisition / paper / shadow / live-readiness / deployment /
  exchange-write phase;
- any migration of the Phase 4bb-D doubled-path artefact to canonical
  placement (explicitly NOT recommended per Phase 4bb-F §6).

Phase 4bb-G is **branch-complete only** by this work. Per the Phase
4bk-A workflow standard, it is NOT project-complete until a separately
authorized merge phase records its merge-closeout on `main`.
