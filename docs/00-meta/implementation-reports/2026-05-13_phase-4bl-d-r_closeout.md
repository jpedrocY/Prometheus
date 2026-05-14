# Phase 4bl-D-R — Closeout

## 1. Phase identity

- **Phase:** Phase 4bl-D-R — Multi-Day Raw Manifest Eligibility Gate
  Rerun
- **Branch:** `phase-4bl-d-r/multi-day-raw-manifest-eligibility-gate-rerun`
- **Base commit (`main` / `origin/main` at branch creation):**
  `69e45280f080e320171f1d851933fdb13213aaea`
  (Phase 4bl-D-S2 merge-closeout commit; project-complete on `main`).
- **Implementation report:**
  `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-r_multi-day-raw-manifest-eligibility-gate-rerun.md`

## 2. Result

**`RAW_MULTIDAY_GATE_PASS`** — 33 / 33 PASS / 0 FAIL / 0 ERROR / 0 NA.

The four Phase 4bl-D failing checks (`raw_zip_sidecar_integrity`,
`per_file_row_count_consistency`,
`per_file_time_bounds_consistency`,
`total_row_count_consistency`) all PASS in Phase 4bl-D-R with the
Phase 4bl-D-S2-canonicalised 2025-01-15 sidecar in place. The
remaining 29 Phase 4bl-D PASS checks remain PASS.

The full per-row Phase 4ax `validate_aggtrade_payload` validation
recomputed:

- `recomputed_total_row_count = 155,153,449` (matches manifest)
- `recomputed_total_size_bytes = 1,943,823,208` (matches manifest)

Wall-clock: `893.984` seconds (~14.9 minutes) — consistent with the
Phase 4bl-D first run (`880.188` seconds).

## 3. Tracked files added (4)

- `scripts/phase4bl_d_r_rerun_raw_gate.py` (thin wrapper around the
  Phase 4bl-D gate script; Python standard library + Phase 4bl-D gate
  module loaded by file path; no network imports; no credential
  reads; no `.env`; no `.mcp.json`; no MCP / Graphify; no exchange
  adapters; no `prometheus.runtime` / `prometheus.execution` /
  `prometheus.persistence` imports; ruff clean; `py_compile` clean).
- `tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py` (23
  offline tests; pytest `tmp_path` only; static forbidden-import scan;
  static forbidden-runtime-token scan; deterministic-serialisation
  test; augmentation-purity test).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-r_multi-day-raw-manifest-eligibility-gate-rerun.md`
  (this implementation report; 17 sections).
- `docs/00-meta/implementation-reports/2026-05-13_phase-4bl-d-r_closeout.md`
  (this closeout).

## 4. Tracked files modified narrowly (1)

- `docs/00-meta/current-project-state.md` (new Phase 4bl-D-R
  narrative paragraph + new "Current phase:" block; prior
  Phase 4bl-D-S2 "Current phase:" block preserved as historical
  context).

## 5. Local gitignored artefacts (NOT committed)

- `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json`
  (Phase 4bl-D-R gate-rerun report; 171,342 bytes; SHA256
  `f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`).
- `data/microstructure/gate-reports/raw/microstructure_raw_aggtrades_v001__v002__phase-4bl-d-r__1778717359124__69e45280f080.json.sha256`
  (paired sidecar; 155 bytes; canonical Phase 4bb-F body
  `<sha256>  <basename>\n`; sidecar self-SHA256
  `84f37b7b424d67dfa0dae06bb51279354b5b37998beb4f9b1cf6b6f617dd8c02`).

Both files are gitignored under `.gitignore:85: data/microstructure/`
(verified via `git check-ignore -v`).

## 6. Upstream artefact pre/post immutability (six artefacts)

All byte-identical pre and post the Phase 4bl-D-R rerun:

| Artefact | SHA256 |
| --- | --- |
| target sidecar (canonicalised) | `c40e6be60753a912063d9a5f5c1617ba31ec987c09121c50adab3ba0226018fc` |
| target raw zip | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| v002 raw manifest | `016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485` |
| v002 acquisition log | `52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314` |
| Phase 4bl-D gate report | `d97948ed4d2a7e49de7ba82813b9b4befaec03acfe067320afa7c77d1f6629e7` |
| Phase 4bl-D-S2 canonicalisation report | `8c6457b65a4a3413c7836aea391d6b2cbd82c5cbd6252c6239f7e948e20809d3` |

## 7. Manifest state preserved

- v002 raw manifest `research_eligible` remains `false`.
- v002 raw manifest `eligibility_gate_status` remains `"pending"`.
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)`
  always-raises invariant preserved (never invoked).

## 8. Validation

| Check | Result |
| --- | --- |
| `python -m py_compile` (wrapper + tests) | OK |
| Scoped `uv run ruff check` (wrapper + tests) | All checks passed |
| `uv run pytest tests/research/microstructure/test_phase4bl_d_r_gate_rerun.py` | 23 passed |
| One-shot gate rerun via `uv run python -X utf8 scripts/phase4bl_d_r_rerun_raw_gate.py` | `RAW_MULTIDAY_GATE_PASS` |
| Augmented report sidecar token matches recomputed JSON SHA | YES |
| `git diff --check` (pre-commit) | clean |
| `git status --short` | only tracked Phase 4bl-D-R additions + pre-existing untracked entries |

Whole-repo `ruff` / `mypy` / `pytest` were NOT rerun by Phase 4bl-D-R
because no prior source module was modified. The wrapper is a new
file; the gate script itself is unchanged.

## 9. No-rescue / non-authorisation invariants preserved

Phase 4bl-D-R does NOT:

- modify the Phase 4bl-D gate script;
- weaken any of the 33 Phase 4bl-D checks;
- relax the sidecar parser to accept CRLF;
- amend the Phase 4bb-F canonical path policy;
- amend the Phase 4ak M0 twelve-clause gate, post-null cooldown rule,
  cooled-down families list, or memo template;
- amend the Phase 4al refined no-rescue rule, §13 boundary, or §14
  hierarchy;
- amend the Phase 4aw `flip_research_eligible(...)` always-raises
  invariant;
- modify any prior `data/microstructure/` artefact;
- flip `research_eligible` on any actual manifest;
- transition `eligibility_gate_status` on any actual manifest;
- change `chronological_split_policy` on any actual manifest;
- revise any retained verdict;
- change any project lock;
- acquire data;
- download anything;
- call any Binance / public / private endpoint;
- open any WebSocket;
- use any credential;
- read or create `.env`;
- create or read `.mcp.json`;
- enable MCP or Graphify;
- run normalization, derivation, features, labels, diagnostics, ML,
  strategy, signals, or backtests;
- compute PnL / MFE / MAE / R-multiple / equity / position / alpha /
  edge / prediction / model-score / decision-score / entry-exit /
  strategy output;
- create a successor-state artefact;
- authorise Phase 4bl-D-R merge phase, Phase 4bl-E, Phase 4bm-*,
  Phase 4bn-*, Phase 4bo-*, Phase 4bp-*, Phase 4bq-*, Phase 5,
  Phase 4 canonical, paper / shadow, live-readiness, deployment,
  exchange-write, production-key creation, authenticated APIs,
  private endpoints, user stream, or live WebSocket implementation.

## 10. Retained verdicts preserved (verbatim)

H0 FRAMEWORK ANCHOR; R3 BASELINE-OF-RECORD; R1a / R1b-narrow
RETAINED — NON-LEADING; R2 FAILED — §11.6; F1 HARD REJECT; D1-A
MECHANISM PASS / FRAMEWORK FAIL; 5m thread OPERATIONALLY CLOSED per
Phase 3t; V2 / G1 / C1 HARD REJECT — terminal.

## 11. Recommended state

**Remain paused.** Phase 4bl-D-R is branch-complete only by this
work. Per the Phase 4bk-A workflow standard, Phase 4bl-D-R is NOT
project-complete until a separately authorised merge phase records
its merge-closeout on `main`.

## 12. Conditional next, NOT authorised

After a separately authorised Phase 4bl-D-R merge phase, the natural
conditional successor (per the Phase 4bb-G precedent for the
Phase 4az `__v001` raw family) is **Phase 4bl-E — Multi-Day Raw
Manifest Successor-State Recording**, which would record a sibling
successor-state JSON artefact at
`data/microstructure/successor-state/microstructure_raw_aggtrades_v001__v002__stage2_raw_admissible__phase-4bl-e.json`
citing the Phase 4bl-D-R PASS report and preserving the v002 raw
manifest byte-identically. Phase 4bl-D-R does not authorise
Phase 4bl-E.

## 13. No next phase authorised

Phase 4 canonical remains unauthorised. Phase 4bl-D-R merge phase /
Phase 4bl-E / Phase 4bm-* / Phase 4bn-* / Phase 4bo-* / Phase 4bp-*
/ Phase 4bq-* / Phase 5 / any successor phase remains unauthorised.
Paper / shadow, live-readiness, deployment, production keys,
authenticated APIs, private endpoints, public-endpoint calls in
code, user stream, WebSocket implementation, MCP, Graphify,
`.mcp.json`, credentials, exchange-write, and any additional
acquisition beyond the 90 locked BTCUSDT UTC dates remain
unauthorised.
