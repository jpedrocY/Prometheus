# Phase 4bb-E — Gate-Report Interpretation / Successor-State Policy Memo

**Phase identity:** Phase 4bb-E — Gate-Report Interpretation / Successor-State Policy Memo.
**Type:** docs-only governance / successor-state policy memo.
**Date:** 2026-05-07.
**Branch:** `phase-4bb-e/gate-report-successor-state-policy`.
**Status:** drafted; pending operator review.

---

## 1. Phase header

Phase 4bb-E is a docs-only governance memo. Its purpose is to interpret the Phase 4bb-D PASS gate report and to define whether and how raw aggTrades dataset family manifests may ever transition `eligibility_gate_status` from `pending` to `pass`, while preserving `research_eligible = false` for raw families and preserving the original Phase 4az manifest as immutable.

Phase 4bb-E is **text only**. It does not modify source code, tests, scripts, configs, the existing Phase 4bb-D gate report, the Phase 4az manifest / raw zip / sidecar / acquisition log, or anything under `data/microstructure/`. It does not authorize any successor phase.

---

## 2. Current state

| Item | Value |
| ---- | ----- |
| `main` HEAD | `ba7d7d6ded4e1d3f8b1a177dcf9fc1acdccfc68a` |
| `origin/main` HEAD | `ba7d7d6ded4e1d3f8b1a177dcf9fc1acdccfc68a` |
| Local / origin sync | in sync |
| Phase 4bb-D merge commit (ancestor verified) | `a6ec0d1f759e7ee618d63c748e2e716fbd3021ef` |
| Phase 4bb-D merge-closeout file | `docs/00-meta/implementation-reports/2026-05-07_phase-4bb-d_merge-closeout.md` (present on `main`) |
| `data/microstructure/` gitignored | yes (`.gitignore:85`) |
| Phase 4az manifest | `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (`research_eligible=false`, `eligibility_gate_status=pending`, mtime unchanged since Phase 4az `2026-05-07 21:55`) |
| Phase 4bb-D local gate report | present on this workspace at `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` (17,053 bytes); paired sidecar 140 bytes; report SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` matches sidecar bit-for-bit |

---

## 3. Inputs reviewed

- Phase 4az acquisition + manifest (BTCUSDT 2025-01-15; 1,681,098 events; raw zip SHA `f560c2e5...`).
- Phase 4ba staged eligibility-gate model + 45-check definition + 5-stage ladder.
- Phase 4bb-A structural QA (21 / 21 PASS).
- Phase 4bb-B execution plan.
- Phase 4bb-C primitive (`eligibility_io.py`, `eligibility_gate.py`, `eligibility_checks.py`, `eligibility_report.py`).
- Phase 4bb-D execution result (`overall_status=pass`; 45 / 45 PASS; 0 invalid windows; 13 / 13 boundary confirmations true; `research_eligible_after=False`; `no_successor_authorization=True`; manifest / raw / sidecar / acquisition-log SHA pre / post identical).
- Phase 4bb-D tracked memo, closeout, and merge-closeout files.
- Project locks: §11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6/§7/§8, Phase 4j §11, Phase 4ak M0 + post-null cooldown, Phase 4al refined no-rescue rule + §13 + §14.

No live endpoints, credentials, `.env`, `.mcp.json`, MCP, Graphify, or external services were consulted.

---

## 4. Scope

- Interpret the Phase 4bb-D PASS gate report at the report level vs the manifest level.
- Define raw-family `research_eligible` permanence policy.
- Define original-manifest immutability policy.
- Enumerate successor-manifest / successor-state options and recommend a conservative posture.
- Distinguish Phase 4ba Stage-2 (gate-passed) from Stage-3 (normalized derived family).
- Define the impact of the PASS report on the sequencing of any future normalization-design work.
- Define how the local gitignored gate report should be referenced in tracked docs without ever committing it.
- Document the doubled `gate-reports/gate-reports/` path issue as known behavior and recommend a separately authorized cleanup phase before any future production-style gate execution.
- Recommend a conditional bounded successor sequence and explicitly NOT authorize any successor.

---

## 5. Non-scope

Phase 4bb-E did not:

- modify source code;
- modify tests;
- modify scripts;
- modify configs;
- rerun the gate;
- generate a new gate report;
- delete, move, rename, modify, or commit the existing local gitignored gate report;
- modify `data/microstructure/`;
- modify the Phase 4az manifest;
- create a successor manifest;
- create a successor-state registry;
- flip `research_eligible`;
- transition `eligibility_gate_status` out of `pending`;
- normalize the dataset;
- create JSONL, Parquet, DuckDB, feature tables, labels, or derived datasets;
- acquire data;
- call public endpoints;
- call Binance APIs;
- open WebSockets;
- use private endpoints;
- request or use credentials;
- create `.env`;
- create `.mcp.json`;
- enable MCP or Graphify;
- compute features;
- compute returns, alpha, edge, opportunity rate, taker imbalance, sweep detection, aggressive-flow score, spread, depth, liquidity, slippage, order-flow, or execution-quality proxies;
- train ML;
- create a strategy;
- run backtests;
- revise retained verdicts;
- change project locks;
- amend M0;
- authorize Phase 4bb-F, Phase 4bb-G, Phase 4bc, Phase 5, Phase 4 canonical, paper / shadow, live-readiness, deployment, exchange-write, production keys, authenticated APIs, private endpoints, user stream, or live WebSocket implementation.

---

## 6. Phase 4bb-D gate-report summary

| Field | Value |
| ----- | ----- |
| `report_id` | `microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` |
| `report_path` (gitignored, NOT committed) | `data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json` |
| Report SHA256 (recomputed; matches paired sidecar) | `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` |
| `overall_status` | `pass` |
| Total checks | `45` |
| PASS / FAIL / NOT_APPLICABLE / ERROR | `45 / 0 / 0 / 0` |
| `len(invalid_window_candidates)` | `0` |
| `research_eligible_after` | `False` |
| `eligibility_gate_status_after` (recommendation only) | `pass` |
| `no_successor_authorization` | `True` |
| Boundary confirmations | 13 / 13 `true` |
| Manifest / raw zip / sidecar / acquisition-log immutability | SHA pre-run vs post-run identical for all four artefacts |
| Manifest mtime | unchanged across the run |
| Actual on-disk manifest after run | `research_eligible=false`, `eligibility_gate_status=pending` |

The report is preserved in the tracked Phase 4bb-D memo, closeout, and merge-closeout files (committed) plus the local gitignored JSON + sidecar (not committed).

---

## 7. Interpretation of PASS at the report level

PASS means: the offline gate observed the Phase 4az archive against all 45 Phase 4ba §10 checks and recorded zero failures, zero error checks, zero not-applicable checks, and zero invalid-window candidates; pre-run vs post-run hashes for the manifest, raw zip, sidecar, and acquisition log were bit-for-bit identical; the gate did not contact any Binance endpoint, open any WebSocket, read any credential, write outside the gate-reports namespace, mutate any artefact, or perform any feature / ML / strategy / backtest work; and the orchestrator's invariant `research_eligible_after = False` was honored.

PASS at the report level does **not** mean:

- the dataset is research-eligible;
- the dataset has been promoted to Stage 2 (gate-passed) on its own manifest;
- the manifest's `eligibility_gate_status` has been transitioned from `pending` to `pass`;
- normalization is authorized;
- feature computation is authorized;
- ML training is authorized;
- strategy implementation is authorized;
- backtest execution is authorized;
- additional acquisition is justified;
- paper / shadow, live-readiness, deployment, or exchange-write are authorized.

PASS at the report level is **structural eligibility-time evidence only**. It says the artefact has cleared the structural eligibility-time floor at the moment of the run, under the locked-commit version of the gate code (`code_commit_sha = aa612ba2778c97a5150b80064244b90d024bfa54`) and the locked Phase 4ba 45-check set. Anything beyond that requires a separately authorized successor phase that **explicitly cites this report as evidence**.

---

## 8. Raw-family eligibility-state policy

Three policy layers are distinguished:

1. **Report level (gate evidence).** Whether a gate report exists with `overall_status=pass`. PASS at this level can be re-checked any time by re-invoking the deterministic Phase 4bb-C primitive (subject to Phase 4bb-F output-path hygiene below). It does not modify any manifest.
2. **Manifest level (on-disk manifest fields).** Whether the actual manifest's `eligibility_gate_status` field reads `pending` / `pass` / `fail` and whether `research_eligible` reads `false` / `true`. Mutating these fields requires a separately authorized phase. This is the permanent project record.
3. **Research-eligibility level (downstream usability).** Whether downstream research code may treat the dataset as `research_eligible`. Per Phase 4ba's staged ladder, `research_eligible = true` is reserved for Stage 3 normalized derived families only and **never** appears on a raw family.

Binding raw-family policy:

- **Raw-family `research_eligible` MUST remain `false` permanently.** No future phase, no operator approval, and no gate result PASS may flip a raw family's `research_eligible` to `true`. This is consistent with the Phase 4ba staged ladder, the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant, and the Phase 4bb-C orchestrator invariant `research_eligible_after = False`.
- **Raw-family `eligibility_gate_status` MAY in principle transition from `pending` to `pass` (or to `fail`), but only via a separately authorized successor-state phase.** Phase 4bb-D used `write_successor_manifest=False` and did not attempt this transition. Phase 4bb-E does not authorize this transition either.
- A `pass` at the manifest level is purely descriptive of structural eligibility; it does not unlock normalization, features, ML, strategy, backtest, paper / shadow, or live-readiness.

---

## 9. Original-manifest immutability policy

The original Phase 4az manifest at `data/microstructure/manifests/microstructure_raw_aggtrades_v001__v001.json` (SHA256 `a371edd492fe12523af2fe9759391350ac415bfeabf34e4fdc6c33da8e16a201`; mtime `2026-05-07 21:55:40 +0100`; 1491 bytes) **must remain immutable**.

Binding rules:

- The original v001 manifest's bytes must not be modified by any future phase.
- The original v001 manifest's mtime must not be modified by any future phase.
- Any future Stage-2 transition must NOT overwrite the original v001 manifest.
- Any future successor-state recording mechanism must be byte-additive: it must record the new state in a separate file or registry; it must reference the original v001 manifest by SHA and path; it must be re-derivable from the gate report; and it must include the gate report's `report_id` and `code_commit_sha`.

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` method always raises and was never bypassed by Phase 4bb-D or by any prior phase. That invariant should not be relaxed.

---

## 10. Successor-manifest / successor-state options

Four successor-state mechanisms are evaluated. Each is described qualitatively with its tradeoffs.

### Option A — Keep original raw manifest pending forever; treat PASS report as external gate evidence only

The original v001 manifest is never modified and remains `pending`. The Phase 4bb-D PASS report (gitignored locally; recorded in the tracked Phase 4bb-D Markdown trio) is the only project record that the artefact has cleared the gate. Any future docs-only or docs-and-code phase that wants to act on the gate result reads it from the tracked Markdown plus the local gate report and proceeds without touching the manifest.

- **Pros.** Maximally conservative. Zero new state to maintain. Zero new failure modes. Zero new ways to accidentally flip `research_eligible`. The tracked Markdown is the project record; local report is reproducible from the Phase 4bb-C primitive.
- **Cons.** Future phases that want a programmatic / machine-readable Stage-2 signal must read tracked Markdown rather than a manifest field. Slightly less convenient for any future automation.
- **Reversibility.** Trivially reversible because nothing was changed.

### Option B — Future successor-state manifest may record `eligibility_gate_status=pass`

A future separately authorized phase creates a new sibling manifest (e.g. `microstructure_raw_aggtrades_v001__v001__gate_state.json`) that records `eligibility_gate_status=pass`, references the original v001 manifest by SHA and path, references the Phase 4bb-D `report_id`, references the gate `code_commit_sha`, and **never** flips `research_eligible` to `true`. The original v001 manifest remains byte-identical.

- **Pros.** Provides a machine-readable Stage-2 marker without overwriting the original manifest. Supports future automation that wants to dispatch on `eligibility_gate_status` without parsing tracked Markdown. Preserves the Phase 4ba staged-ladder semantics.
- **Cons.** Adds a second source of truth. Requires a clear naming convention. Requires a clear rule about what happens if the gate is re-run (e.g. a new gate report is generated): is the successor-state manifest replaced, versioned, or appended? Requires a clear rule about what happens if a future gate run returns FAIL.
- **Reversibility.** Reversible by deleting the successor-state manifest, which re-establishes Option A semantics (the original manifest is untouched).

### Option C — Use a separate tracked or gitignored gate-state registry

Instead of a sibling manifest, use a single project-wide registry (e.g. `data/microstructure/manifests/gate_state.jsonl`, gitignored) where each line records `(dataset_family, version, manifest_sha, gate_status, gate_report_id, gate_report_sha, code_commit_sha, decided_at_utc_ms)`. Any read of "what is the current gate status of family X version Y?" consults the registry's most-recent matching line.

- **Pros.** One file to maintain across all future families and versions. Append-only structure makes history explicit. Easier to query programmatically. Generalizes naturally to multiple datasets.
- **Cons.** Heavier governance design upfront. Requires a clear schema, a clear concurrency / append-safety design, a clear policy for handling FAIL → PASS or PASS → FAIL transitions, and a clear rule about whether the registry is gitignored (operator-machine-only) or tracked (project-wide). Tracked would require committing structured state derived from the gate, which is a different governance posture than the current "gate reports stay gitignored" rule.
- **Reversibility.** Reversible by deleting the registry; the original manifest remains untouched.

### Option D — Fix the gate report output-root path behavior before any future gate execution

The Phase 4bb-D gate report was written under `data/microstructure/gate-reports/gate-reports/...`, with the doubled `gate-reports/` segment. This is observed Phase 4bb-C orchestrator behavior (the writer composes `output_root / "gate-reports" / filename` while Phase 4bb-D supplied `output_root = data/microstructure/gate-reports`). Option D is a separately authorized small phase (proposed name: Phase 4bb-F — Gate Report Output Path Hygiene) that decides between three sub-options:

- **D.1.** Treat the doubled path as harmless (entirely under the gitignored `data/microstructure/` namespace), document it as known behavior, and never re-run the gate. Acceptable because Phase 4bb-D used `write_report=True` exactly once and the operator may decide to keep that one report as the canonical record.
- **D.2.** Fix Phase 4bb-C orchestrator code so that future gate runs write to a single non-doubled path (e.g. `data/microstructure/gate-reports/<report_filename>`). Requires a small code change to one file under `src/prometheus/research/microstructure/` plus targeted tests; preserves backward compatibility because the existing Phase 4bb-D report remains intact at its existing path.
- **D.3.** Change the Phase 4bb-C `AggTradesEligibilityGateInput` calling convention so that callers pass `output_root` as the parent of the desired gate-reports directory (e.g. `output_root = data/microstructure`) and the orchestrator appends `gate-reports/`. Requires either an API tweak with a deprecation note or an explicit calling-convention contract; cleaner long-term but more invasive.

Option D is **independent** of Options A / B / C — any of those can be paired with any sub-option of D. Phase 4bb-E does not authorize Option D itself; it only documents the known issue and recommends that Option D be addressed before any future production-style gate execution.

---

## 11. Recommended successor-state policy

The recommended posture for the immediate term is the conservative pairing of **Option A (default current)** with **deferred Option B (formal successor-state manifest, only if separately authorized)** and **deferred Option D.2 (gate-report output-path hygiene, only if separately authorized)**.

Specifically:

- **Default current state (no further action required):** Option A. The original Phase 4az manifest remains immutable and `pending`. The Phase 4bb-D PASS report exists locally under the gitignored `data/microstructure/gate-reports/` namespace and is referenced verbatim in the tracked Phase 4bb-D memo, closeout, and merge-closeout. The tracked Markdown is the project record.
- **Conditional next, only if the operator wants a machine-readable Stage-2 marker:** Option B, implemented in a separately authorized future phase (proposed name: Phase 4bb-G — Raw Manifest Successor-State Recording). That phase must (i) preserve the original v001 manifest byte-identically; (ii) write a sibling successor-state manifest that references the original by SHA and path, references `report_id`, and references `code_commit_sha`; (iii) preserve `research_eligible = false`; (iv) be docs-and-local-gitignored-output or docs-and-code with strict path discipline; (v) leave the gate-reports namespace gitignored; (vi) not authorize normalization, features, ML, strategy, backtest, or live work.
- **Cleanup, only if the operator intends to re-run the gate later:** Option D.2 (or D.3), in a separately authorized future phase (proposed name: Phase 4bb-F — Gate Report Output Path Hygiene). Without this cleanup, future gate runs will continue to write to `data/microstructure/gate-reports/gate-reports/...`. That is harmless on its own (still under the gitignored namespace) but is undesirable as a project-record artefact. If the operator does not intend to re-run the gate, Option D.2 / D.3 can be deferred indefinitely.
- **Option C (gate-state registry) is NOT recommended now.** It requires heavier governance design upfront, and it generalizes only after the project has multiple raw datasets with reportable gate state. With one dataset, Option B is simpler.

The recommended successor-state policy is **conservative-by-default**: do nothing until the operator wants either a machine-readable Stage-2 marker (Option B) or a re-run-friendly gate-report output path (Option D). Either or both options remain unauthorized at this time.

---

## 12. Stage-2 versus Stage-3 distinction

Per Phase 4ba's staged ladder, the five stages are: 0 acquired → 1 inspected → 2 gate-passed → 3 normalized → 4 feature-cleared. Phase 4bb-E reaffirms:

- The Phase 4az artefact is currently at **Stage 0 (acquired)** by manifest field semantics (`eligibility_gate_status = pending`).
- The Phase 4bb-D PASS gate report demonstrates that the artefact has cleared the structural eligibility-time floor that defines **Stage 2 (gate-passed)** at the report level. Whether this becomes Stage 2 at the manifest level depends on whether the operator authorizes a successor-state phase (Option B / Phase 4bb-G).
- **Stage 3 (normalized)** is the first stage at which `research_eligible = true` is permitted, and it applies only to a **derived normalized family**, not to a raw family. The original raw family `microstructure_raw_aggtrades_v001` is forever excluded from `research_eligible = true` regardless of which successor-state policy is adopted.
- **Stage 4 (feature-cleared)** is the first stage at which feature computation is authorized. It depends on a Stage-3 normalized derived family being research-eligible plus a separately authorized feature-design phase.

Phase 4bb-E does not advance the Phase 4az artefact past Stage 0 at the manifest level. It records that the artefact has cleared the Stage-2 structural floor at the report level only.

---

## 13. Impact on normalization-design sequencing

Two distinct activities are separated:

- **Normalization design (docs-only).** Defining what a normalized derived family for aggTrades would look like — schema, partitioning, semantics, derived columns, normalization-time data-quality rules, governance for the new family's manifest, eligibility-gate equivalence. This is docs work; it touches no runtime code, no data, and no manifest. Normalization design **may proceed before** any Stage-2 transition at the manifest level, provided the design memo references the Phase 4bb-D PASS gate report as the structural basis. Phase 4bc — AggTrades Normalization Design Memo (docs-only) is the recommended placeholder name for that phase if the operator chooses to pursue it. Phase 4bc is **not authorized** by Phase 4bb-E.
- **Normalization implementation (code + derived data).** Building the normalizer, writing JSONL / Parquet / DuckDB derived datasets, building the derived family's manifest. This is code-and-data work; it produces a Stage-3 candidate. Normalization implementation **must require** either a referenced PASS gate report (Option A continues) or a formal Stage-2 transition (Option B applied). Either way, normalization implementation is **not authorized** by Phase 4bb-E and must be a separately authorized successor phase.

The recommended sequence (none of these are authorized by Phase 4bb-E):

```text
Option A (current) → optional Phase 4bb-F output-path hygiene
                  → optional Phase 4bb-G Stage-2 successor-state recording
                  → optional Phase 4bc normalization-design memo
                  → optional Phase 4bc-execution normalization implementation
```

Phase 4bc may also be issued before Phase 4bb-G if the operator prefers to keep manifest state untouched and rely on the tracked PASS gate report citation. The above sequence is one acceptable ordering, not the only one.

---

## 14. Handling of local gitignored gate reports in tracked docs

The Phase 4bb-D gate report and paired sidecar exist locally on the operator machine under the gitignored `data/microstructure/gate-reports/` namespace. They are **not** committed to the repository, and they should remain so. To reference them in tracked Markdown without committing them, the project record uses the following convention:

- Tracked memos record the **gate report SHA256** verbatim (`96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423` for Phase 4bb-D). This is a pinning hash; if the operator ever re-derives the report, the SHA can be re-checked.
- Tracked memos record the **gate report path relative to the repo root** (`data/microstructure/gate-reports/gate-reports/microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c.json`). This is reproducible by re-invoking the Phase 4bb-C primitive at the same code commit.
- Tracked memos record the **gate report sidecar path** (`...json.sha256`).
- Tracked memos record the **`code_commit_sha`** that was supplied to the gate (`aa612ba2778c97a5150b80064244b90d024bfa54` for Phase 4bb-D), so the report can be regenerated deterministically.
- Tracked memos record the **`report_id`** (`microstructure_raw_aggtrades_v001__v001__1778351069361__aa612ba2778c` for Phase 4bb-D), which encodes the dataset family, version, generation timestamp (`1778351069361` ms), and a short prefix of the `code_commit_sha`.
- Tracked memos record the **`overall_status`**, the per-status counts, the `len(invalid_window_candidates)`, the boundary-confirmation count, and any other relevant report fields verbatim.

The local gate report itself is not necessary to read the tracked Markdown record. If the local report is ever lost (workspace reset, machine swap, etc.), the operator can re-derive it deterministically by checking out `code_commit_sha` (now an ancestor of `main`), invoking `run_eligibility_gate` with the same `AggTradesEligibilityGateInput` against the same Phase 4az artefacts, and verifying that the resulting report's SHA matches the recorded `96f09159...`. (Subject to Phase 4bb-F output-path hygiene if the operator wants the re-derived report to live at a non-doubled path.)

This convention should be applied to all future gate reports under `data/microstructure/gate-reports/`: **never commit the report itself; always commit the SHA + path + commit + report-id + status + counts in tracked Markdown.**

---

## 15. Known path issue: doubled `gate-reports/gate-reports/`

Observed Phase 4bb-C orchestrator behavior: when Phase 4bb-D supplied `AggTradesEligibilityGateInput.output_root = Path("data/microstructure/gate-reports")` and `write_report=True`, the orchestrator wrote the report to `data/microstructure/gate-reports/gate-reports/<report_filename>`. The doubled `gate-reports/` segment indicates that the writer composes `output_root / "gate-reports" / <report_filename>` rather than `output_root / <report_filename>`.

Assessment:

- **Correctness:** the report and sidecar are physically present at the doubled path; the SHA matches the sidecar bit-for-bit; the file is well-formed JSON and contains all expected fields. The report is valid evidence.
- **Boundary safety:** the doubled path is **fully under** `data/microstructure/`. `git check-ignore -v data/microstructure/gate-reports/` returns `.gitignore:85:data/microstructure/	data/microstructure/gate-reports/`, confirming gitignore. No tracked file is affected.
- **Project-record cleanliness:** the doubled path is undesirable as a long-term artefact convention. It is harmless once but ugly if the gate is invoked repeatedly (each invocation will write under `data/microstructure/gate-reports/gate-reports/...`).
- **Risk:** none for the existing Phase 4bb-D report. Low for any future single re-run. Low-to-medium for any future repeated production-style runs that build a longer gate-report archive.

Phase 4bb-E recommendation: **document the doubled path as known Phase 4bb-C behavior** (this section is the official record); **do NOT modify the existing Phase 4bb-D report** (path, contents, or sidecar); and **defer the fix** to a separately authorized cleanup phase named Phase 4bb-F — Gate Report Output Path Hygiene. Phase 4bb-F is **not authorized** by Phase 4bb-E. If Phase 4bb-F is ever authorized, it should choose between Option D.2 (orchestrator emits to a single non-doubled path) and Option D.3 (calling-convention change so the caller passes `output_root = data/microstructure` and the orchestrator appends `gate-reports/`); document the chosen convention; preserve the Phase 4bb-D report at its existing path for record continuity; and add a regression test that the new convention is honored.

The doubled path **does not invalidate** the Phase 4bb-D PASS gate result. The interpretation in §7 stands.

---

## 16. Fail-closed rules

The following fail-closed rules apply to any future successor-state phase (Option B / Phase 4bb-G), gate-report cleanup phase (Option D / Phase 4bb-F), or normalization-design phase (Phase 4bc):

- **Original Phase 4az manifest must not be modified.** Any phase that mutates the original v001 manifest fails closed.
- **`research_eligible` for raw families must remain `false`.** Any phase that flips `research_eligible` to `true` on a raw family fails closed.
- **Existing Phase 4bb-D gate report must not be deleted, moved, renamed, or modified.** Any phase that mutates the existing report fails closed.
- **No commit under `data/microstructure/`.** The gitignored namespace stays gitignored. Any phase that commits a file under `data/microstructure/` fails closed.
- **No silent transition `pending → pass` on a manifest field.** Any phase that mutates `eligibility_gate_status` without explicit operator authorization, without reference to a specific gate report, without the report's `code_commit_sha`, and without preserving the original manifest fails closed.
- **No bypass of `MicrostructureManifest.flip_research_eligible(...)`'s always-raises guard.** That invariant is preserved.
- **No network I/O, credentials, MCP, Graphify, or `.mcp.json`.** Any phase that introduces those fails closed.
- **No data acquisition, no normalization, no feature computation, no ML, no strategy, no backtest, no paper / shadow, no live-readiness, no exchange-write, no production keys.** None of these are authorized by Phase 4bb-E or by any of the proposed successor phases at the policy level.

---

## 17. What this phase proves

- The Phase 4bb-D PASS gate report is structural eligibility-time evidence at the report level, valid under the locked Phase 4bb-C primitive at `code_commit_sha = aa612ba2778c97a5150b80064244b90d024bfa54` and the locked Phase 4ba 45-check set.
- The original Phase 4az manifest's immutability has been preserved through Phase 4bb-D and through Phase 4bb-E.
- Raw-family `research_eligible = false` is binding policy; PASS at the gate level does not flip it.
- A staged successor-state policy is feasible: Option A (default current; do nothing) is conservative-and-correct; Option B (sibling successor-state manifest) is feasible if a machine-readable Stage-2 marker is wanted; Option D (gate-report output-path hygiene) is feasible if the operator wants future gate runs to use a non-doubled path.
- The doubled `gate-reports/gate-reports/` path is a known and documented Phase 4bb-C behavior; it does not invalidate the Phase 4bb-D report.
- Normalization design (docs-only) may proceed before Stage-2 transition, provided the design memo references the Phase 4bb-D PASS report.
- Normalization implementation (code + derived data) requires either a referenced PASS gate report (Option A continued) or a formal Stage-2 transition (Option B applied), and is not authorized.

---

## 18. What this phase does not prove

- That `research_eligible = true` is now allowed on the Phase 4az raw family. It is not.
- That `eligibility_gate_status = pass` should be recorded on the actual Phase 4az manifest. It should not be, by Phase 4bb-E recommendation; only a separately authorized Phase 4bb-G could record that on a sibling successor-state manifest.
- That normalization, feature computation, ML training, strategy implementation, backtests, paper / shadow, or live-readiness are now authorized. None of those are authorized.
- That the Phase 4bb-C primitive's doubled-path behavior should be patched right now. It is documented; the fix is deferred to a separately authorized cleanup phase.
- That a gate-state registry (Option C) is the right governance design. It is not recommended now.
- That any retained verdict (R3 baseline-of-record; R1a / R1b-narrow retained; R2 FAILED §11.6; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL; V2 / G1 / C1 HARD REJECT terminal; 5m thread CLOSED; H0 framework anchor) should be revised. None should be revised.
- That any project lock (§11.6, §1.7.3, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, Phase 4j §11, Phase 4ak M0 + post-null cooldown) should be relaxed. None should be relaxed.

---

## 19. Preserved boundaries

| Boundary | Preserved? |
| -------- | :--------: |
| No source code change | yes |
| No test change | yes |
| No script change | yes |
| No config change | yes |
| No `.gitignore` change | yes |
| No M0 governance change | yes |
| No data acquisition | yes |
| No public-endpoint calls | yes |
| No Binance API calls | yes |
| No WebSocket | yes |
| No credential / `.env` / `.mcp.json` / MCP / Graphify | yes |
| No data normalization | yes |
| No feature computation | yes |
| No ML / strategy / backtest | yes |
| No mutation of `data/microstructure/` | yes |
| Original Phase 4az manifest unchanged | yes |
| Phase 4bb-D gate report unchanged | yes |
| `research_eligible` for raw family stays `false` | yes |
| `eligibility_gate_status` stays `pending` | yes |
| No retained verdict revised | yes |
| No project lock loosened | yes |
| No successor authorized | yes |

---

## 20. Recommended future options

- **Primary — remain paused.** No successor phase is authorized by Phase 4bb-E.
- **Conditional next, only if the operator wants to begin moving toward normalization:** future docs-only **Phase 4bc — AggTrades Normalization Design Memo**. May proceed before any Stage-2 manifest transition. Must reference Phase 4bb-D PASS report. Must NOT authorize normalization implementation. NOT authorized by Phase 4bb-E.
- **Conditional cleanup, only before any future repeated gate execution:** future code-and-docs **Phase 4bb-F — Gate Report Output Path Hygiene**. Fixes the doubled `gate-reports/gate-reports/` path behavior in Phase 4bb-C orchestrator code via Option D.2 or D.3. Preserves the existing Phase 4bb-D report at its existing path. Adds a regression test. NOT authorized by Phase 4bb-E.
- **Conditional policy implementation, only if the operator wants a machine-readable Stage-2 marker:** future docs-and-local-gitignored-output (or docs-and-code) **Phase 4bb-G — Raw Manifest Successor-State Recording**. Implements Option B: a sibling successor-state manifest that records `eligibility_gate_status=pass` while preserving the original v001 manifest byte-identically and preserving `research_eligible=false`. NOT authorized by Phase 4bb-E.
- **Not recommended.** Acquiring more aggTrades data; flipping `research_eligible`; computing features; training ML; creating a strategy; running backtests; reopening the 5m research thread; rescuing R2 / F1 / D1-A / V2 / G1 / C1 / V1-arc; touching MCP / Graphify / `.mcp.json` / credentials.
- **Forbidden.** Verdict revision; lock revision; parameter optimization derived from Phase 4bb-D evidence; M0 amendment derived from Phase 4bb-D evidence; paper / shadow / live-readiness / deployment / production-key creation / authenticated APIs / private endpoints / public-endpoint calls in code / user stream / live WebSocket / exchange-write.

---

## 21. Closeout / lock preservation

Phase 4bb-E preserves every retained verdict and project lock verbatim:

- H0 FRAMEWORK ANCHOR;
- R3 BASELINE-OF-RECORD;
- R1a / R1b-narrow RETAINED — NON-LEADING;
- R2 FAILED — §11.6;
- F1 HARD REJECT;
- D1-A MECHANISM PASS / FRAMEWORK FAIL;
- 5m thread OPERATIONALLY CLOSED per Phase 3t;
- V2 HARD REJECT — terminal for V2 first-spec;
- G1 HARD REJECT — terminal for G1 first-spec;
- C1 HARD REJECT — terminal for C1 first-spec;
- §11.6 = 8 bps per side; round-trip = 16 bps;
- §1.7.3 0.25% / 2× / one-position / mark-price stops;
- Phase 3p §4.7 strict integrity gate;
- Phase 3r §8; Phase 3v §8; Phase 3w §6 / §7 / §8;
- Phase 4j §11;
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template;
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy;
- Phase 4am, 4an, 4ao, 4ap, 4aq, 4ar, 4as, 4at, 4au, 4av, 4aw, 4ax, 4ay, 4az, 4ba, 4bb-A, 4bb-B, 4bb-C, 4bb-D results — all preserved verbatim.

The Phase 4az dataset's eligibility flags are unchanged: `research_eligible` remains `false`, `eligibility_gate_status` remains `pending`. Phase 4bb-D gate report and paired sidecar remain untouched at their existing local gitignored path with SHA256 `96f09159df7c89906637ada0f0f9e68e4b8850d8c5f2a38960aaa70f6afe6423`.

**Phase 4 (canonical) remains unauthorized. Phase 4bb-F / Phase 4bb-G / Phase 4bc / Phase 5 / any successor phase remains unauthorized. Paper / shadow, live-readiness, deployment, production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, credentials, and additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition all remain unauthorized.**

**Recommended state: remain paused. No next phase authorized.**
