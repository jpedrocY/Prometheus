# Phase 4bm-B — Merge Closeout

## 1. Phase identity

- **Phase:** Phase 4bm-B — Multi-Day Normalization Implementation
- **Type:** docs-and-code Tier 1 implementation phase (per Phase 4bl-F risk-tiering standard)
- **Action:** merge into `main`
- **Merge purpose:** bring the Phase 4bm-B multi-day normalization orchestrator, its offline test suite, the implementation report, the closeout, and the narrow `current-project-state.md` Phase 4bm-B update into `main` so that Phase 4bm-B transitions from branch-complete to project-complete. The orchestrator's exactly-once real run already produced the 90 per-day Parquet files + 90 paired sidecars + 1 multi-day index manifest + 1 manifest sidecar under the gitignored `data/microstructure/` namespace; none of those local artefacts are committed by this merge. The Phase 4bm-A locked design is now realised as tracked code, tests, and reports on `main`.
- **Target branch:** `main`
- **Source branch:** `phase-4bm-b/multi-day-normalization-implementation`

## 2. SHAs

- **`main` SHA before merge:** `56f96a4c613a3d8c8794905be4c1847fcdac5e58` (Phase 4bm-A-P1 merge-closeout)
- **Phase 4bm-B branch commit SHAs:**
  - feat commit: `80f596daed0fc867f2b0c1d7fc282d8d052f76ae` — `feat(phase-4bm-b): multi-day normalization orchestrator + tests`
  - docs commit: `83d4e2bc0bfb3884574af656d3a62be7e637b5ad` — `docs(phase-4bm-b): implementation report, closeout, current-project-state update`
  - **Branch tip merged:** `83d4e2bc0bfb3884574af656d3a62be7e637b5ad` (the docs commit; the feat commit `80f596d` is the parent of the branch tip and is included in the merge)
- **Merge commit SHA:** `57a2219dcf5662fb1c5684275a53f90d0dc39347` — `docs(phase-4bm-b): merge multi-day normalization implementation`
- **Final `main` / `origin/main` SHA after this merge-closeout commit + push:** recorded in §15 below after the merge-closeout commit is pushed (this merge-closeout's own commit advances `main` one further commit; the SHA is captured at the very end of the push step in this same closeout under §15).

**Branch-tip note on the SHA-chain.** The authorization prompt stated the expected branch-tip SHA was `80f596d` (the feat commit) but also explicitly anticipated that a follow-up docs commit might shift the tip and instructed merge review to verify the actual tip. The actual tip `83d4e2b` is the valid Phase 4bm-B docs commit (implementation report + closeout + `current-project-state.md` update) per the standard SHA-chain pattern documented across prior phase closeouts. Both commits were merged together by the `--no-ff` merge.

## 3. Merge method

- `git merge --no-ff phase-4bm-b/multi-day-normalization-implementation -m "docs(phase-4bm-b): merge multi-day normalization implementation"`
- Strategy: `ort` (the default).
- Force: none. Skip-hooks: none. Skip-signing: none.
- Pushed to `origin/main` with no force, no skip-hooks, no skip-signing (recorded in §15 after merge-closeout commit).

## 4. Files brought forward by the merge

**Tracked files added (4):**

- `scripts/phase4bm_b_normalize_multiday_aggtrades.py` (~1,613 lines; standalone offline multi-day normalization orchestrator; pure pyarrow + numpy + stdlib; no `prometheus.runtime/execution/persistence` imports; no network I/O; no credentials; no `.env`; no `.mcp.json`; no MCP; no Graphify)
- `tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` (~866 lines; 33 offline tests; all PASS)
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_multi-day-normalization-implementation.md` (Phase 4bm-B implementation report, 19 sections)
- `docs/00-meta/implementation-reports/2026-05-15_phase-4bm-b_closeout.md` (Phase 4bm-B closeout, 16 sections)

**Tracked files modified narrowly (1):**

- `docs/00-meta/current-project-state.md` (Phase 4bm-B narrative paragraph + new "Current phase:" block; prior Phase 4bm-A-P1 "Current phase:" block preserved as historical context)

**No `data/microstructure/` file was modified by this merge.**

No prior `src/prometheus/` source module modified. No prior test modified. No prior `scripts/` script modified. No prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition. `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, and MCP files unchanged.

## 5. Diff summary

```text
 docs/00-meta/current-project-state.md              |  371 +++++
 .../2026-05-15_phase-4bm-b_closeout.md             |  196 +++
 ...4bm-b_multi-day-normalization-implementation.md |  453 ++++++
 scripts/phase4bm_b_normalize_multiday_aggtrades.py | 1613 ++++++++++++++++++++
 .../test_phase4bm_b_multiday_normalization.py      |  866 +++++++++++
 5 files changed, 3499 insertions(+)
```

The diff matches the expected Phase 4bm-B change set from the authorization prompt verbatim: exactly five tracked files (one modified, four added) and 3,499 insertions across the tracked surface.

## 6. Verdict

**CODE LANDED — multi-day normalization Tier 1 implementation merged into `main`.**

Phase 4bm-B operationalised the Phase 4bm-A locked Multi-Day Normalization Design Memo by implementing an offline orchestrator that normalises the v002 multi-day BTCUSDT aggTrades raw archive (90 contiguous UTC dates 2024-12-01..2025-02-28; 155,153,449 events; 1,943,823,208 source bytes) acquired by Phase 4bl-C and admitted by the Phase 4bl-D-R PASS gate (33/33 PASS) and the Phase 4bl-E Stage-2 raw successor-state, into a new normalized derived dataset family with identity `dataset_family = microstructure_normalized_aggtrades_v001` (reused; schema byte-identical to Phase 4bd), `dataset_version = v002` (new; bounded source-dataset discriminator), and `schema_version = v001` (unchanged). The orchestrator's exactly-once real run produced 90 per-day Parquet files + 90 paired canonical Phase 4bb-F sidecars + 1 multi-day index manifest + 1 manifest sidecar — all under the gitignored `data/microstructure/` namespace; none committed. The 65-criterion strict-fail-closed validation contract reports PASS across all six groups (10 precondition + 21 per-day × 90 collapsed + 8 aggregate + 12 immutability + 6 governance + 8 quality-gate). All 188 immutability witnesses verified byte-identical pre/post. The new v002 derived manifest is locked at Stage-0 with `research_eligible=false` and `eligibility_gate_status="pending"`; the Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked).

## 7. Local gitignored outputs (referenced; not committed)

The Phase 4bm-B orchestrator's exactly-once real run produced these local artefacts under the gitignored `data/microstructure/` namespace. **None were committed by this merge.**

| Path | Size (bytes) | SHA256 | Status |
| ---- | ------------ | ------ | ------ |
| `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` | 104,094 | `01c5fa538aaa732249483dfac5302945b67461b151cae573cf1cd200e1a2554a` | not committed |
| `data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json.sha256` | 118 | `d96f31ae1256f86d2e4590d0808d1853268474e84797ab509d0a59a676eb5888` | not committed |
| 90 per-day Parquet files at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/{2024/12,2025/01,2025/02}/BTCUSDT-aggTrades-<YYYY-MM-DD>.parquet` | per-file sizes recorded in manifest `per_file_inventory[i].parquet_size_bytes` | per-file SHA256 recorded in manifest `per_file_inventory[i].parquet_sha256` | not committed |
| 90 paired canonical Phase 4bb-F sidecars (one `.parquet.sha256` per parquet; body `<sha>  <basename>\n` with two ASCII spaces and trailing LF) | per-file sizes recorded in manifest `per_file_inventory[i].sidecar_size_bytes` | per-file SHA256 recorded in manifest `per_file_inventory[i].sidecar_sha256` | not committed |

**Manifest + sidecar SHA256 independently recomputed at merge-verification time** via PowerShell `Get-FileHash` and matched the recorded values bit-for-bit. Per-day output presence spot-checked: `data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/BTCUSDT/2024/12/` contains 62 entries (31 parquets + 31 sidecars); `BTCUSDT/2025/01/` contains 62 entries; `BTCUSDT/2025/02/` contains 56 entries (28 parquets + 28 sidecars). Total = 180 files = exactly 90 parquets + 90 sidecars.

**`git check-ignore -v` confirmations:**

```text
.gitignore:85:data/microstructure/    data/microstructure/
.gitignore:85:data/microstructure/    data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/
.gitignore:85:data/microstructure/    data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json
```

The 24-minute orchestrator was not rerun for this merge phase. Merge verification relied on the Phase 4bm-B implementation report, closeout, and direct read-only spot-checks of the on-disk manifest, sidecar, and per-day output counts.

## 8. Validation results

Validation reruns performed at merge-verification time on the Phase 4bm-B branch tip immediately before merging into `main`:

- `uv run ruff check scripts/phase4bm_b_normalize_multiday_aggtrades.py tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` → `All checks passed!`
- `uv run mypy scripts/phase4bm_b_normalize_multiday_aggtrades.py` → `Success: no issues found in 1 source file`
- `uv run pytest tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` → `33 passed in 0.29s`
- `uv run pytest tests/research/microstructure/` → `1156 passed, 1 skipped in 11.11s` (the 1 skip is the pre-existing labelled placeholder in `test_label_gate_report.py`)
- `git diff --check` → clean (no whitespace errors)

Whole-repo validation also rerun at merge-verification time:

- `uv run ruff check .` (whole repo) → `All checks passed!`
- `uv run mypy src/prometheus` (whole repo, strict) → `Success: no issues found in 120 source files`
- `uv run pytest` (whole repo) → `1939 passed, 2 failed, 1 skipped in 16.70s`. The 2 failures are the pre-existing simulation failures `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, both `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232`. **Unchanged from prior phases; not introduced by this merge.** The Phase 4bm-B targeted and microstructure pytest scopes are clean.

Gitignore coverage confirmations at merge-verification time:

- `git check-ignore -v data/microstructure/` → `.gitignore:85:data/microstructure/`
- `git check-ignore -v data/microstructure/normalized/microstructure_normalized_aggtrades_v001__v002/` → covered by `.gitignore:85`
- `git check-ignore -v data/microstructure/manifests/microstructure_normalized_aggtrades_v001__v002.json` → covered by `.gitignore:85`

## 9. Upstream immutability evidence

The Phase 4bm-B implementation report records that the orchestrator captured pre-run SHA256 for **188 immutability witnesses** before any output write and re-captured post-run SHA256 after all outputs were committed, with all 188 verified byte-identical pre/post. The witness set is:

- 4 governance artefacts: v002 raw manifest (`016967865c970012a8dc762af3117fd871e86ecdd51749b84bb8a39d51d87485`), v002 acquisition log (`52f6d7fb3cb0f136ee9c050bed64524b87383aa737af374d2a0f925e90c6b314`), Phase 4bl-D-R PASS gate report (`f9493fd10d1cf58fde253dac68c3beecb6906f8c293798df29d4cad79b6f1c46`), Phase 4bl-E successor-state (`a0576ca656bd99388099c25b3a7a390c177b7c5e9ed86eaafe87501a3d1f751d`);
- 4 governance sidecars (paired `.sha256` for each above);
- 90 v002 raw zips;
- 90 v002 raw zip sidecars.

The Phase 4bd v001 single-day parquet at `data/microstructure/normalized/microstructure_normalized_aggtrades_v001/BTCUSDT/2025/01/BTCUSDT-aggTrades-2025-01-15.parquet` was re-verified post-run with SHA256 `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` (matches recorded Phase 4bd value).

Drift on any witness fails the run closed (criteria 40-51 of the 65-criterion contract). No drift occurred.

## 10. Manifest state preservation

| Manifest | `research_eligible` | `eligibility_gate_status` | `chronological_split_policy` | Notes |
| -------- | ------------------- | ------------------------- | ---------------------------- | ----- |
| v002 raw manifest (`microstructure_raw_aggtrades_v001__v002.json`) | `false` | `"pending"` | n/a | unchanged from Phase 4bl-C |
| Phase 4bd v001 derived manifest (`microstructure_normalized_aggtrades_v001__v001.json`) | `false` | `"pending"` | n/a | unchanged from Phase 4bd |
| Phase 4bh feature manifest (`microstructure_features_aggtrades_v001__v001.json`) | `false` | `"pending"` | n/a | unchanged |
| Phase 4bj-C label manifest (`microstructure_labels_aggtrades_v001__v001.json`) | `false` | `"pending"` | `"not_yet_defined"` | unchanged |
| **NEW** Phase 4bm-B v002 derived manifest (`microstructure_normalized_aggtrades_v001__v002.json`) | `false` | `"pending"` | n/a | locked at Stage-0 by Phase 4bm-B |

The Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant is preserved end-to-end (never invoked). The new multi-day index manifest is a sibling shape (mirroring the Phase 4bl-C raw v002 manifest layout) and does NOT use the single-file `MicrostructureManifest` data class; its locked `research_eligible=false` and `eligibility_gate_status="pending"` are top-level fields of that sibling shape.

## 11. Boundary confirmations

All true at the close of the Phase 4bm-B merge:

- no `data/microstructure/` file modified by this merge;
- no `data/microstructure/` file committed by this merge;
- no source code modified outside `scripts/phase4bm_b_normalize_multiday_aggtrades.py` (new) and the narrow `current-project-state.md` paragraph addition;
- no test modified outside `tests/research/microstructure/test_phase4bm_b_multiday_normalization.py` (new);
- no script modified outside `scripts/phase4bm_b_normalize_multiday_aggtrades.py` (new);
- no `pyproject.toml`, `README.md`, `.gitignore`, `.gitattributes`, or MCP file modified;
- no prior governance memo modified beyond the narrow `current-project-state.md` paragraph addition;
- no `research_eligible` flipped on any actual manifest;
- no `eligibility_gate_status` transitioned on any actual manifest;
- no `chronological_split_policy` changed on any actual manifest;
- no manifest state mutation of any kind;
- no Phase 4bd v001 derived parquet / manifest / sidecar mutation;
- no Phase 4bh feature parquet / manifest mutation;
- no Phase 4bj-C label parquet / manifest mutation;
- no Phase 4bb-D / Phase 4bf / Phase 4bi-B / Phase 4bj-E gate report mutation;
- no Phase 4bg-B / Phase 4bi-D / Phase 4bj-G / Phase 4bb-G / Phase 4bl-E successor-state mutation;
- no Phase 4bl-D / 4bl-D-S1 / 4bl-D-S2 / 4bl-D-R artefact mutation;
- no data acquired;
- no public endpoint called;
- no Binance API called;
- no WebSocket opened;
- no credential / `.env` / `.mcp.json` / MCP / Graphify used;
- no normalizer rerun (the 24-minute orchestrator was not invoked during this merge phase);
- no raw / derived / feature / label eligibility gate rerun;
- no kernel rerun;
- no feature computed;
- no label computed;
- no signal computed;
- no ML model trained;
- no strategy created;
- no backtest run;
- no force push;
- no skip-hooks;
- no skip-signing;
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant preserved (never invoked);
- Phase 4bb-F canonical path policy preserved verbatim;
- Phase 4bl-F four-tier risk model preserved verbatim;
- Phase 4bl-F nine reusable non-authorization blocks preserved verbatim;
- Phase 4bl-F R-SIDECAR-CRLF standing rule preserved verbatim (cited; not invoked — Phase 4bm-B writes use canonical LF natively);
- no retained verdict revised;
- no project lock loosened;
- no M0 amendment;
- no successor authorized;
- **path-layout clarification recorded:** v002 implemented under `microstructure_normalized_aggtrades_v001__v002/` (see §16).

## 12. Retained verdict ledger

All preserved verbatim:

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

## 13. Preserved project locks

All preserved verbatim:

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
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy
- Phase 4aw `MicrostructureManifest.flip_research_eligible(...)` always-raises invariant
- Phase 4bb-F canonical path policy
- Phase 4bb-G raw `__v001` successor-state precedent
- Phase 4bg-B / Phase 4bi-D / Phase 4bj-G / Phase 4bl-E successor-state precedents
- Phase 4bl-F four-tier risk model + nine reusable non-authorization blocks + R-SIDECAR-CRLF standing rule
- Phase 4am .. Phase 4bm-A-P1 results — all preserved verbatim

## 14. No-rescue constraints

The Phase 4bm-B merge does not, and cannot, be construed as authorising:

- ML model training, model selection, feature ranking, meta-labeling, strategy hypothesis generation, or any conversion of normalized data / labels into signals;
- strategy signal construction, strategy logic, position state, entry / exit rules, or backtest design;
- paper / shadow / live-readiness / deployment / exchange-write work;
- Phase 4 canonical or Phase 5 authorisation;
- 30s / 5m / 30m / 1h / 4h / longer-horizon label generation;
- barrier / target-before-stop / MFE / MAE / R-multiple / PnL labels;
- mark-price / spot / cross-venue / order-book / additional aggTrades acquisition beyond the 90 locked BTCUSDT UTC dates;
- old-strategy alt-symbol rerun or cooled-down-family reopening;
- 5m research-thread reopening (Phase 3t closure preserved);
- transitioning any manifest's `research_eligible`, `eligibility_gate_status`, or `chronological_split_policy` from the Phase 4bm-B Stage-0 artefact evidence alone;
- R3-prime / R1a-prime / R1b-narrow-prime / R2-prime / H0-prime / F1-prime / D1-A-prime / D1-B / V2-prime / V2-narrow / V2-relaxed / V2 hybrid / G1-prime / G1-narrow / G1-extension / G1 hybrid / C1-prime / C1-narrow / C1-extension / C1 hybrid / V1-D1 / F1-D1 / any cross-strategy hybrid;
- M0 amendment derived from Phase 4bm-B reasoning;
- production keys, authenticated APIs, private endpoints, public-endpoint calls in code, user stream, live WebSocket implementation, MCP, Graphify, `.mcp.json`, or credentials.

## 15. Successor authorization

**None.**

Phase 4bm-B is now project-complete. The following candidate successors are explicitly **not** authorized by this merge:

- Phase 4bm-C — Multi-Day Normalized Structural QA Memo (the natural conditional successor by Phase 4be precedent; would mirror Phase 4be analysis-and-docs against the v002 derived family; **not** authorized here)
- Phase 4bm-D — Multi-Day Derived-Family Eligibility Gate (Phase 4bf precedent; would mirror Phase 4bf for the v002 family; **not** authorized here)
- Phase 4bm-E — Multi-Day Derived-Family Research-Eligibility Decision Memo (Phase 4bg-A precedent; **not** authorized here)
- Phase 4bm-F — Multi-Day Derived-Family Successor-State Recording (Phase 4bg-B precedent; **not** authorized here)
- Phase 4bm-* — any other multi-day successor; **not** authorized here
- Phase 4bn-* — any feature arc on multi-day data; **not** authorized here
- Phase 4bo-* — any label arc on multi-day data; **not** authorized here
- Phase 4bp-* — any diagnostic arc on multi-day data; **not** authorized here
- Phase 4bq-* — any chronological split arc on multi-day data; **not** authorized here
- Phase 5 — **not** authorized
- Phase 4 canonical — **not** authorized
- additional aggTrades / 5m / 1m / tick / mark-price 30m / 4h / order-book / spot / cross-venue / funding / OI data acquisition — **not** authorized
- ML implementation — **not** authorized
- strategy implementation — **not** authorized
- backtest implementation — **not** authorized
- paper / shadow — **not** authorized
- live-readiness — **not** authorized
- deployment — **not** authorized
- exchange-write — **not** authorized
- production keys — **not** authorized
- authenticated APIs — **not** authorized
- private endpoints — **not** authorized
- public-endpoint calls in code — **not** authorized
- user stream — **not** authorized
- MCP / Graphify / `.mcp.json` / credentials — **not** authorized

**Final `main` / `origin/main` SHA after this merge-closeout commit + push:** recorded immediately after this file is committed and pushed (see operator report). The merge commit is `57a2219dcf5662fb1c5684275a53f90d0dc39347`; the merge-closeout commit is the commit that adds this file to `main`. The final SHA is the merge-closeout commit SHA.

## 16. Recommended state

**Remain paused.**

Phase 4bm-B is project-complete: the multi-day normalization Tier 1 implementation is now on `main`. The v002 derived family is at Stage-0 (artefacts present locally; manifest pending). No successor is authorized by this merge.

**Path-layout clarification recorded.** The Phase 4bm-A design memo §7 specified that the v002 derived family writes its parquets under the family-name directory `microstructure_normalized_aggtrades_v001/` while simultaneously requiring coexistence with the Phase 4bd `__v001` single-day parquet at the 2025-01-15 date. Those two literal requirements are inconsistent at the filesystem layer (two parquets cannot share an absolute path). The Phase 4bm-B implementation resolved this by version-suffixing the v002 family directory to `microstructure_normalized_aggtrades_v001__v002/`, preserving the Phase 4bd `__v001` single-day parquet byte-identically (SHA `2b3d69787d93137ea2dcefcd79ab84cacbe80fe55527ce9c83ea01778808f6fa` verified post-run; matches recorded Phase 4bd value), avoiding overwrite/collision risk, and keeping the dataset identity intact (`dataset_family = microstructure_normalized_aggtrades_v001`; `dataset_version = v002`; `schema_version = v001`). The clarification is recorded in §8 of the Phase 4bm-B implementation report. This is an implementation-level path-layout decision, not a schema or governance change.

**Conditional next, NOT authorized:** Phase 4bm-C — Multi-Day Normalized Structural QA Memo (analysis-and-docs Tier 1 phase mirroring the Phase 4be precedent against the v002 derived family) is the cleanest non-paused option. It would read-only inspect the 90 v002 parquets, the multi-day index manifest, and the sidecars; report descriptive structural QA against the locked schema; preserve every retained verdict, project lock, and the Phase 4aw `flip_research_eligible(...)` always-raises invariant; and not transition the new v002 manifest's `research_eligible` or `eligibility_gate_status`. Phase 4bm-C is **not** authorised by this merge.

The M0 mechanism-admissibility gate and post-null cooldown rule remain binding prospective governance for any future research lane.

No data was acquired, no endpoint was contacted, no credential was used, no manifest was mutated, no kernel was rerun, no gate was rerun, no successor-state was recorded, no `research_eligible` was flipped, no retained verdict was revised, and no project lock was loosened by this merge.
