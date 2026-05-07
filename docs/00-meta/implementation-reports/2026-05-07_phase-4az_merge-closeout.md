# Phase 4az — Merge Closeout

**Phase identity:** Phase 4az — Public AggTrades Archive Acquisition (BTCUSDT, 2025-01-15 UTC).
**Type:** code-and-docs public-archive acquisition phase.
**Date:** 2026-05-07.
**Action:** merge into `main`.

---

## 1. Merge purpose

To merge the Phase 4az public aggTrades archive acquisition phase from the Phase 4az feature branch into `main`. Phase 4az is the project's first authorized real-data microstructure acquisition phase. It acquired exactly one Binance USDⓈ-M Futures aggTrades daily archive for `BTCUSDT` on `2025-01-15` UTC from the public `data.binance.vision` archive under the strict integrity gate predeclared in Phase 4ay §10.

The merge does **not** acquire additional data, contact any Binance API endpoint, open any WebSocket, normalise the dataset, compute features, create a strategy candidate, train an ML model, flip `research_eligible` to `True`, or authorize any successor phase. The acquired dataset's manifest has `research_eligible=false` and `eligibility_gate_status=pending`; the dataset is **infrastructure evidence only**.

---

## 2. Branches

| Item | Value |
| ---- | ----- |
| Target branch | `main` |
| Source branch | `phase-4az/public-aggtrades-archive-acquisition` |

---

## 3. SHAs

| Item | SHA |
| ---- | --- |
| `main` before merge | `caaad39e40604571758bc58eaac374344c7852e8` |
| Phase 4az acquisition commit | `b97a8c63c6e389637fd4d7f0b6acab13ab46b6ee` |
| Phase 4az closeout commit | `4f81d1bdc64b5b692f53d5ea21ee5f9237265dcf` |
| Phase 4az wording correction commit | `e88ce9ebcbbe2ebbacd67ae051d9054d69645c0a` |
| Source branch HEAD | `e88ce9ebcbbe2ebbacd67ae051d9054d69645c0a` |
| Source / origin in sync at start | yes |
| Merge method | `git merge --no-ff --no-commit` |

The merge commit SHA appears in the operator report after `git commit` and `git push`.

---

## 4. Files brought forward by the merge

6 file changes, 2,430 insertions, 5 deletions.

**Added (4 new tracked files):**

```
scripts/phase4az_acquire_btcusdt_aggtrades_archive.py
tests/research/microstructure/test_phase4az_archive_acquisition.py
docs/00-meta/implementation-reports/2026-05-07_phase-4az_public-aggtrades-archive-acquisition.md
docs/00-meta/implementation-reports/2026-05-07_phase-4az_closeout.md
```

**Modified (2 narrow updates):**

```
tests/research/microstructure/test_aggtrades.py    (one obsolete Phase 4ax regression check repurposed)
docs/00-meta/current-project-state.md              (Phase 4az narrative paragraph + new "Current phase:" block; prior Phase 4ay block preserved as historical context)
```

`.gitignore` is unchanged. No file under `src/prometheus/` modified. No existing script modified. No existing dataset manifest under `data/manifests/` modified. No `pyproject.toml`, `README.md`.

**Local data outputs (NOT committed):** the four files under `data/microstructure/` (raw `.zip`, paired `.sha256`, manifest, acquisition log) live under the gitignored `data/microstructure/` tree and are not part of this commit.

---

## 5. Pre-merge wording correction

A single narrow wording correction was applied on the Phase 4az branch before merge.

**File:** `docs/00-meta/implementation-reports/2026-05-07_phase-4az_public-aggtrades-archive-acquisition.md` (executive summary, §1).

**Old wording:**

> "No code under src/prometheus/ was modified beyond the new acquisition script"

**New wording:**

> "No code under src/prometheus/ was modified. Phase 4az added one new standalone acquisition script under scripts/."

**Rationale:** the new acquisition script `scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` is under `scripts/`, not under `src/prometheus/`. The original wording could be misread as implying the script is part of the `src/prometheus/` tree. The corrected wording is unambiguous: nothing under `src/prometheus/` was touched, and the new script lives under `scripts/`.

The correction was made in commit `e88ce9ebcbbe2ebbacd67ae051d9054d69645c0a` (`docs(phase-4az): clarify acquisition script location`). It changed exactly one line (1 insertion, 1 deletion). It did **not** modify the acquisition result, row counts, checksum, timestamps, validation results, data paths, recommendations, governance statements, retained verdicts, project locks, or successor authorization status.

---

## 6. Phase 4az was code-and-docs public-archive acquisition

**Confirmed.** Phase 4az is a code-and-docs public-archive acquisition phase. Its scope was strictly limited to:

- one new acquisition script under `scripts/`;
- one new test file under `tests/research/microstructure/`;
- one narrowly-modified existing test file (`test_aggtrades.py`: the obsolete Phase 4ax regression check repurposed);
- two new docs files (memo + closeout) plus this merge-closeout;
- one narrow `current-project-state.md` update;
- local data outputs created under the gitignored `data/microstructure/` tree (raw `.zip`, paired `.sha256`, manifest, acquisition log).

Verified by automated import-boundary, content-scan, and acquisition-time URL allowlist enforcement that the new script and its tests contain no live Binance API endpoint references, no credential paths, and no MCP / Graphify / `.mcp.json` / user stream / listenKey / order / account / position / leverage / margin / `forceOrders` REST references.

---

## 7. Acquisition status

**`SUCCESSFUL_ACQUISITION`.** All 19 Phase 4ay §10 integrity-gate checks passed (18 PASS + 1 NOT_APPLICABLE for `invalid_windows` because no integrity events occurred during the run).

---

## 8. Acquisition target

| Item | Value |
| ---- | ----- |
| Symbol | `BTCUSDT` |
| Date | `2025-01-15` (UTC) |
| Market | Binance USDⓈ-M Futures |
| Source | public `data.binance.vision` archive only |
| Mode | `historical_archive` (one daily aggTrades archive only) |
| Dataset family | `microstructure_raw_aggtrades_v001` |
| Dataset version | `v001` |
| Schema version | `v001` |

The script downloaded exactly two files from `data.binance.vision`: the `.CHECKSUM` companion first, then (only after the checksum was parsed and validated) the daily archive ZIP. No other URL was contacted.

---

## 9. Local data outputs

Generated under the gitignored `data/microstructure/` tree:

```
data/microstructure/
├── raw/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/
│       ├── BTCUSDT-aggTrades-2025-01-15.zip            (~21 MiB)
│       └── BTCUSDT-aggTrades-2025-01-15.zip.sha256
└── manifests/
    ├── microstructure_raw_aggtrades_v001__v001.json
    └── microstructure_raw_aggtrades_v001__v001_acquisition_log.json
```

| Item | Value |
| ---- | ----- |
| Archive SHA256 | `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e` |
| Event count | `1,681,098` |
| First trade time (ms) | `1736899205109` (2025-01-15 00:00:05.109 UTC) |
| Last trade time (ms) | `1736985599991` (2025-01-15 23:59:59.991 UTC) |
| UTC-day coverage | every observed `T` falls in `[2025-01-15 00:00:00.000 UTC, 2025-01-16 00:00:00.000 UTC)` |
| Manifest `research_eligible` | **`false`** |
| Manifest `eligibility_gate_status` | **`pending`** |
| Local dataset size | ~21 MiB |
| Staging cleanup | artefacts cleaned on success |

**All four output files are gitignored and uncommitted.** `git status` does not list them. `git check-ignore -v` confirms the `data/microstructure/` rule (line 85 of `.gitignore` added by Phase 4aw) applies. `git status --ignored` shows them under "Ignored files".

---

## 10. Boundary confirmations

The Phase 4az merge confirms verbatim:

- **No normalised dataset created.** The archive `.zip` is preserved verbatim. No JSONL or Parquet was produced.
- **No features computed.** No metric, transform, taker-imbalance, sweep detection, or aggressive-flow score was computed.
- **No strategy or ML created.** No strategy candidate; no entry / exit design; no ML model.
- **No Binance API endpoint contacted.** No `fapi.binance.com`. No `/fapi/v1/aggTrades`. No `/fapi/v1/order`. No `/fapi/v2/account`. No `/fapi/v2/positionRisk`. No `/fapi/v1/leverage`. No `/fapi/v1/marginType`. No `/fapi/v1/forceOrders`. No `/fapi/v1/listenKey`.
- **No WebSocket opened.** No subscription, no stream.
- **No credentials / private endpoint / user stream / listenKey used.** No API key, no `.env` reads, no signed request, no `X-MBX-APIKEY` header, no listenKey lifecycle, no MCP, no Graphify, no `.mcp.json`.

The script's URL allowlist enforces every one of these denials in code, and the test suite verifies the allowlist with parametrised denylist references.

---

## 11. Validation summary

Validation was performed on the Phase 4az branch immediately before merge.

| Item | Result |
| ---- | ------ |
| Targeted microstructure pytest | **196 passed** (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35) |
| Phase 4az tests (`test_phase4az_archive_acquisition.py`) | **35 passed** |
| Whole-repo ruff | passed |
| Whole-repo mypy strict | passed (89 source files) |
| Whole-repo pytest | 944 + 35 new = 979 passed, **2 failed** (verified pre-existing on `main` before Phase 4az; see below); **zero new regressions** from Phase 4az |
| Targeted mypy on the new script | `Success: no issues found in 1 source file` |
| `python -m compileall` on script and tests | both pass |
| `git diff --check` | clean |
| Live acquisition | `SUCCESSFUL_ACQUISITION` (1,681,098 events) |
| `data/microstructure/` directory check | exists locally, **gitignored**; `git status` does not list it |

**Whole-repo pytest has 2 failures, both reproduced on main before Phase 4az and unrelated to the public-archive acquisition; Phase 4az introduced zero new regressions.**

The two failures are in `tests/simulation/test_backtest_real_2026_03.py`:

- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt`
- `tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_ethusdt`

Both fail with `KeyError: 'trade_count'` raised in the unrelated `src/prometheus/research/data/storage.py:232`. The failures were verified as pre-existing on `main` before Phase 4az. The Phase 4az acquisition script does not touch `src/prometheus/research/data/storage.py`, the simulation tests, or any related path.

---

## 12. Implementation / governance review

### What changed?

- One new acquisition script (`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`) — stdlib only plus three names imported from `prometheus.research.microstructure.aggtrades` (Phase 4ax validator).
- One new test file (`tests/research/microstructure/test_phase4az_archive_acquisition.py`, 35 offline tests using pytest `tmp_path` only).
- One narrowly-modified test (`tests/research/microstructure/test_aggtrades.py`: the obsolete `test_no_data_microstructure_directory_created` regression check was repurposed to verify that Phase 4ax test code itself writes solely under `tmp_path`).
- Two new docs files (Phase 4az memo + closeout) plus this merge-closeout.
- One narrow `current-project-state.md` update.
- One narrow wording correction in §1 of the Phase 4az memo (commit `e88ce9e`).
- Local data outputs created under the gitignored `data/microstructure/` tree. None committed.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text (`docs/00-meta/m0-mechanism-admissibility-gate.md` unchanged).
- No Phase 4ak / 4al / 4j / 3p §4.7 / 3r / 3v / 3w governance.
- No file under `src/prometheus/`.
- No existing dataset manifest under `data/manifests/`.
- No data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/`.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing script under `scripts/` (Phase 3q / 3s / 4i / 4l / 4r / 4x / 4aq scripts all unchanged).
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Were any locks, verdicts, or safety boundaries affected?

No. Phase 4az is data acquisition, not strategy or methodology. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4az paragraph addition and the Phase 4ax obsolete-regression-check repurpose described above.

### Mergeability

The phase introduces only code that is verifiably bounded (one acquisition script with explicit URL allowlist; tests use `tmp_path` only and `do_network=False`), is fully covered by 35 offline tests plus a real-network success run, passes whole-repo ruff and mypy strict, and introduces zero new test regressions. The acquired data is gitignored and not committed. The merge is a clean automatic merge (no conflicts) with `--no-ff` to preserve the Phase 4az commit history.

---

## 13. Research interpretation review

### What did this phase prove?

That the project can safely acquire one predeclared BTCUSDT public aggTrades daily archive (1,681,098 rows; ~21 MiB; SHA256 verified) from the public `data.binance.vision` archive without contacting any Binance API endpoint, opening any WebSocket, using any credential, modifying any verdict / lock / governance, normalizing into a separate dataset, computing any feature, or authorising any successor phase. The Phase 4aw scaffold + Phase 4ax aggTrades skeleton + Phase 4ay authorization framework compose end-to-end on real data. All 19 Phase 4ay §10 integrity-gate checks passed (18 PASS + 1 NOT_APPLICABLE).

### What did this phase NOT prove?

Anything about edge, opportunity rate, predictive content, microstructure feature viability, or strategy potential of the acquired data. The acquired dataset is one symbol's aggregate trades for a single UTC day; no statistical claim is made or licensed. No historical strategy verdict changed. No project lock changed. No cooled-down family is reopened.

### What does this mean for strategy research?

Plumbing only. The project now has its first real microstructure raw dataset. The dataset is `research_eligible=false` and `eligibility_gate_status=pending`; it is **infrastructure evidence only**. No strategy candidate is created. No cooled-down family is reopened. M0 admissibility and post-null cooldown remain binding for any future hypothesis.

### What does this mean for governance?

Nothing changes. M0 (Phase 4ak), the Phase 4al refined no-rescue rule, the Phase 4j §11 OI subset governance, the Phase 3p §4.7 strict integrity gate, the Phase 3r §8 mark-price gap governance, the Phase 3v §8 stop-trigger-domain governance, the Phase 3w §6 / §7 / §8 break-even / EMA slope / stagnation governance, and §11.6 / §1.7.3 project-level locks all remain verbatim. Phase 4az is the first concrete demonstration that the Phase 4ay authorization framework — and the §10 integrity gate, §11 staging plan, §12 manifest contract, and §13 fail-closed rules — works end-to-end on real data.

### Clean next step

After the merge, **remain paused** is the primary recommendation. If the operator separately wishes to advance, two natural separately-authorized next steps exist: (a) docs-only Phase 4ba eligibility-gate review memo, or (b) docs-only Phase 4ba data-quality interpretation memo (descriptive statistics only). None of these is authorized by this merge.

---

## 14. Retained verdict ledger (preserved verbatim)

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL — other.
- **5m thread** — OPERATIONALLY CLOSED per Phase 3t.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.

No verdict is revised by this merge.

---

## 15. Preserved project locks

- M0 governance remains binding prospectively only.
- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade; 2× leverage cap; one position max; mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent recorded by Phase 4ay and applied by Phase 4az).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8 (break-even / EMA slope / stagnation governance).
- Phase 4j §11 (OI subset governance).
- Phase 4ak M0 twelve-clause gate + post-null cooldown rule + cooled-down families list + memo template.
- Phase 4al refined no-rescue rule + §13 boundary + §14 hierarchy.
- Phase 4am §11.A audit findings.
- Phase 4an inventory result.
- Phase 4ao harmonization result.
- Phase 4ap forensic plan.
- Phase 4aq computation result preserved as descriptive evidence only.
- Phase 4ar interpretation result preserved as descriptive interpretation only.
- Phase 4as mechanism-map result preserved as docs-only reset evidence only.
- Phase 4at availability / capture-feasibility result preserved as docs-only feasibility evidence only.
- Phase 4au capture-design result preserved as docs-only design evidence only.
- Phase 4av implementation-plan result preserved as docs-only planning evidence only.
- Phase 4aw scaffold result preserved as scaffold-only infrastructure evidence only.
- Phase 4ax aggTrades skeleton result preserved as collector-skeleton infrastructure evidence only.
- Phase 4ay authorization-boundary result preserved as docs-only acquisition-boundary evidence only.
- Phase 4az acquisition result preserved as public-archive infrastructure evidence only.

No new lock is introduced. No existing lock is loosened.

---

## 16. No-rescue constraints (preserved)

- No R3-prime / R3 next-spec / R3 rescue / baseline-of-record revision.
- No R1a-prime / R1a promotion to leading.
- No R1b-narrow-prime / R1b-narrow promotion to leading.
- No R2-prime / R2 rescue / R2 cheaper-cost rerun.
- No H0-prime / framework-anchor revision.
- No F1-prime / F1 rescue / F1 profitable-subset rescue.
- No D1-A-prime / D1-A extra-filter / D1-B / V1-D1 hybrid / F1-D1 hybrid.
- No V2-prime / V2-narrow / V2-relaxed / V2 hybrid.
- No G1-prime / G1-narrow / G1-extension / G1 hybrid / G1 classifier relaxation.
- No C1-prime / C1-narrow / C1-extension / C1 hybrid.
- No cross-strategy hybrid of any kind.
- No 5m thread reopening.
- No 5m strategy / hybrid / retained-evidence successor.
- No conversion of Phase 4aq forensic numbers, Phase 4l V2 forensic numbers, Phase 4r G1 active-fraction numbers, Phase 4x C1 forensic numbers, or Phase 4az aggTrades counts into parameter-selection inputs.
- No M0 amendment derived from Phase 4az reasoning.
- No flipping of `research_eligible` to `True` for the Phase 4az dataset without a separately authorized eligibility-gate phase.

---

## 17. Successor authorisation

**No successor phase is authorized by this merge.**

In particular, the merge does NOT authorize:

- Phase 4ba,
- Phase 5,
- Phase 4 canonical,
- additional data acquisition,
- ETHUSDT acquisition,
- alt-symbol acquisition,
- multi-day acquisition,
- monthly archive acquisition,
- Binance API endpoint calls,
- REST polling,
- WebSocket connections,
- live REST implementation,
- live WebSocket implementation,
- order-book reconstruction,
- replay implementation,
- eligibility-gate execution,
- flipping `research_eligible` to `True`,
- normalization into Parquet / JSONL,
- feature computation,
- ML model creation,
- strategy candidate creation,
- entry / exit design,
- old-strategy alt-symbol reruns,
- R3 / R2 / V1-arc rescue,
- 5m research thread reopening,
- 5m / 1m / tick / mark-price 30m / 4h / order-book data acquisition,
- paper / shadow,
- live-readiness,
- deployment,
- exchange-write,
- production keys,
- authenticated APIs,
- private endpoints,
- user stream,
- MCP, Graphify, `.mcp.json`,
- credentials.

Any successor phase requires a separate operator authorization brief. Phase 4ba (whether docs-only eligibility-gate review or docs-only data-quality interpretation) is documented as a possible future path but is **not** activated by this merge.

---

## 18. Recommended state

**Recommended state remains paused.** The Phase 4az acquired dataset is now available locally as gitignored infrastructure evidence; the script and tests are now available on `main` for any future separately-authorized phase to consult. No further work should occur until the operator separately authorizes a future phase.

---

## 19. Final note

This merge-closeout is preserved alongside the Phase 4az memo and the Phase 4az closeout under `docs/00-meta/implementation-reports/`. The merge is intentionally `--no-ff` so the Phase 4az commit history (acquisition + closeout + wording correction) is preserved and the boundary between Phase 4ay (authorization-boundary memo) and Phase 4az (real-data acquisition) remains visible in `git log`.

**Phase 4az is now merged into `main`. No next phase is authorized.**
