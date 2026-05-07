# Phase 4az — Closeout

**Phase identity:** Phase 4az — Public AggTrades Archive Acquisition (BTCUSDT, 2025-01-15 UTC).
**Type:** code-and-docs public-archive acquisition phase.
**Date:** 2026-05-07.
**Status:** drafted on branch `phase-4az/public-aggtrades-archive-acquisition`; pending operator review and merge approval.

---

## 1. Purpose

Phase 4az is the project's first authorized real-data microstructure acquisition phase. It acquired exactly one Binance USDⓈ-M Futures aggTrades daily archive for `BTCUSDT` on `2025-01-15` UTC from the public `data.binance.vision` archive under the strict integrity gate predeclared in Phase 4ay §10. The raw `.zip`, paired `.sha256`, manifest with `research_eligible=false`, and acquisition log were written under the gitignored `data/microstructure/` tree.

---

## 2. Branch and base

| Item | Value |
| ---- | ----- |
| Branch | `phase-4az/public-aggtrades-archive-acquisition` |
| Base SHA (`main`) | `caaad39e40604571758bc58eaac374344c7852e8` |
| Base parent commit | `docs(phase-4ay): merge aggtrades archive acquisition authorization` |

---

## 3. Acquisition commit SHA

```
b97a8c63c6e389637fd4d7f0b6acab13ab46b6ee   data(phase-4az): acquire btcusdt aggtrades archive sample
```

(The closeout commit SHA appears in the operator report after this file is committed.)

---

## 4. Acquisition status

**`SUCCESSFUL_ACQUISITION`.**

Live invocation: `python scripts/phase4az_acquire_btcusdt_aggtrades_archive.py --output-root data/microstructure` returned exit 0 and printed the success block. All 19 Phase 4ay §10 integrity-gate checks passed (18 PASS + 1 `NOT_APPLICABLE` for `invalid_windows` because no integrity events occurred during the run).

---

## 5. Local data outputs

Generated under the gitignored `data/microstructure/` tree:

```
data/microstructure/
├── raw/
│   └── microstructure_raw_aggtrades_v001/BTCUSDT/2025/01/
│       ├── BTCUSDT-aggTrades-2025-01-15.zip            (~21 MiB)
│       └── BTCUSDT-aggTrades-2025-01-15.zip.sha256     (66 bytes)
└── manifests/
    ├── microstructure_raw_aggtrades_v001__v001.json    (1.5 KiB)
    └── microstructure_raw_aggtrades_v001__v001_acquisition_log.json (914 bytes)
```

Archive SHA256: `f560c2e529e980c1660b612c79408f3dfd27aa48136fa10965db15f3e2852b3e`.
Event count: `1,681,098`.
First trade time (ms): `1736899205109` (2025-01-15 00:00:05.109 UTC).
Last trade time (ms): `1736985599991` (2025-01-15 23:59:59.991 UTC).

The staging tree (`data/microstructure/staging/...`) was cleaned on success.

The manifest's `research_eligible` is `false` and `eligibility_gate_status` is `pending`.

`git status` does not list any of these files. `git check-ignore -v` confirms the `data/microstructure/` rule (line 85 of `.gitignore`) applies.

---

## 6. Files added / modified

### Added (3 new tracked files + 1 closeout below)

```
scripts/phase4az_acquire_btcusdt_aggtrades_archive.py
tests/research/microstructure/test_phase4az_archive_acquisition.py
docs/00-meta/implementation-reports/2026-05-07_phase-4az_public-aggtrades-archive-acquisition.md
```

### Modified

```
tests/research/microstructure/test_aggtrades.py    (one obsolete regression check repurposed)
docs/00-meta/current-project-state.md              (Phase 4az narrative paragraph + new "Current phase:" block)
```

### Files NOT modified

- No file under `src/prometheus/`.
- No existing test under `tests/research/microstructure/` other than the narrowly-updated regression check in `test_aggtrades.py`.
- No existing test under `tests/unit/`, `tests/integration/`, `tests/simulation/`, or `tests/fixtures/`.
- No existing script under `scripts/` (Phase 3q / 3s / 4i / 4l / 4r / 4x / 4aq scripts all unchanged).
- No existing dataset manifest under `data/manifests/`.
- No existing trade log under `data/derived/backtests/`.
- No existing strategy spec, validation checklist, runtime doc, or governance memo.
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Local data outputs (NOT committed)

The four files under `data/microstructure/` (raw `.zip`, paired `.sha256`, manifest, acquisition log) are present locally and gitignored. They are not staged and not committed.

---

## 7. Code-and-docs / data-boundary confirmation

Phase 4az is a code-and-docs acquisition phase. It contains:

- **Code:** one new acquisition script under `scripts/`, one new test file under `tests/research/microstructure/`, and one narrowly-modified existing test file.
- **Docs:** Phase 4az memo, this closeout, and a narrow `current-project-state.md` update.
- **Local data:** four files under the gitignored `data/microstructure/` tree (raw `.zip`, paired `.sha256`, manifest, acquisition log). Not committed.

The `data/microstructure/` boundary is preserved:

- `.gitignore:85` line `data/microstructure/` is unchanged.
- All produced files live under that gitignored root.
- `git status` confirms zero `data/microstructure/` entries appear in tracked or untracked file lists.
- `git check-ignore -v` confirms the rule applies.

---

## 8. Validation commands

Run on the Phase 4az branch with `data/microstructure/` containing the live-acquired dataset:

```
python -m compileall scripts/phase4az_acquire_btcusdt_aggtrades_archive.py
python -m compileall tests/research/microstructure
.venv/Scripts/ruff check scripts/phase4az_acquire_btcusdt_aggtrades_archive.py tests/research/microstructure
.venv/Scripts/ruff check .
.venv/Scripts/pytest tests/research/microstructure
.venv/Scripts/pytest tests/research/microstructure/test_phase4az_archive_acquisition.py
.venv/Scripts/pytest
.venv/Scripts/mypy scripts/phase4az_acquire_btcusdt_aggtrades_archive.py
.venv/Scripts/mypy
python scripts/phase4az_acquire_btcusdt_aggtrades_archive.py --output-root data/microstructure
git diff --check
git status
git status --ignored
git log --oneline -8
```

---

## 9. Test results

| Command | Result |
| ------- | ------ |
| `compileall scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` | pass |
| `compileall tests/research/microstructure` | pass |
| `ruff check scripts/...phase4az_... tests/research/microstructure` | `All checks passed!` |
| `ruff check .` (whole repo) | `All checks passed!` |
| `pytest tests/research/microstructure` | **196 passed** (Phase 4aw 114 + Phase 4ax 47 + Phase 4az 35) |
| `pytest tests/research/microstructure/test_phase4az_archive_acquisition.py` | **35 passed** |
| `pytest` (whole repo) | **979 passed, 2 failed**; both 2 failures verified pre-existing on `main` (`tests/simulation/test_backtest_real_2026_03.py::test_real_2026_03_btcusdt` and `::test_real_2026_03_ethusdt`, `KeyError: 'trade_count'` in unrelated `src/prometheus/research/data/storage.py:232`); **zero new regressions** |
| `mypy scripts/phase4az_acquire_btcusdt_aggtrades_archive.py` | `Success: no issues found in 1 source file` |
| `mypy` (whole repo) | `Success: no issues found in 89 source files` |
| Live acquisition | `SUCCESSFUL_ACQUISITION` (1,681,098 events) |
| `git diff --check` | clean |
| `data/microstructure/` directory | exists locally, **gitignored** |
| `git status` for `data/microstructure/...` | no entries |

---

## 10. Implementation / governance review

### What changed?

- One new acquisition script (`scripts/phase4az_acquire_btcusdt_aggtrades_archive.py`) — stdlib + Phase 4ax/4aw scaffold imports only; URL allowlist for `data.binance.vision`; 19-check Phase 4ay §10 strict integrity gate; CLI with `--dry-run`, `--fail-if-existing/--no-fail-if-existing`, `--output-root`; standalone `acquire(...)` orchestrator with `do_network=False` test hook.
- One new test file (`tests/research/microstructure/test_phase4az_archive_acquisition.py`, 35 offline tests).
- One narrowly-modified test (`tests/research/microstructure/test_aggtrades.py`: the obsolete `test_no_data_microstructure_directory_created` regression check was repurposed to verify only that Phase 4ax test code itself writes solely under `tmp_path`).
- Two new docs files (memo + this closeout).
- One narrow `current-project-state.md` update.
- Local data outputs created under the gitignored `data/microstructure/` tree (raw `.zip`, paired `.sha256`, manifest, acquisition log). None committed.

### What did not change?

- No retained verdict.
- No project lock.
- No M0 governance text.
- No Phase 4ak / 4al / 4j / 3p §4.7 / 3r / 3v / 3w governance.
- No file under `src/prometheus/`.
- No existing dataset manifest under `data/manifests/`.
- No existing data file under `data/raw/`, `data/normalized/`, `data/derived/`, or `data/research/`.
- No strategy spec, backtest plan, validation checklist, runtime doc, or live-readiness doc.
- No existing script under `scripts/` (Phase 3q / 3s / 4i / 4l / 4r / 4x / 4aq scripts all unchanged).
- No `pyproject.toml`, `README.md`, or `.gitignore`.

### Were any locks, verdicts, or safety boundaries affected?

No. Phase 4az is data acquisition, not strategy or methodology. All locks (§11.6 = 8 bps slippage per side; §1.7.3 = 0.25% risk / 2× leverage / one position max / mark-price stops) and all verdicts (H0 framework anchor; R3 baseline-of-record; R1a / R1b-narrow retained — non-leading; R2 failed — §11.6; F1 hard reject; D1-A mechanism pass / framework fail; 5m thread closed; V2 / G1 / C1 hard reject — terminal) remain verbatim.

### Were any historical scripts, existing data, manifests, or strategy specs modified?

No. None of the existing scripts under `scripts/` was modified. None of the existing dataset manifests, trade logs, strategy specs, validation checklists, or governance memos was modified beyond the narrow `current-project-state.md` Phase 4az paragraph addition and the Phase 4ax obsolete-regression-check repurpose described above.

### Mergeability

Mergeable as code-and-docs acquisition. The new script is fully covered by 35 offline tests; whole-repo ruff and mypy strict are clean; whole-repo pytest has zero new regressions. The acquired data is gitignored and not committed. No verdict, lock, or governance was modified.

---

## 11. Research interpretation review

### 1. What did this phase prove?

That the project can safely acquire one predeclared BTCUSDT public aggTrades daily archive from `data.binance.vision`, verify checksum bit-for-bit, validate every one of 1,681,098 rows against the Phase 4ax aggTrades validator, enforce the Phase 4ay §10 strict integrity gate end-to-end, and store the raw archive plus a manifest with `research_eligible=false` and `eligibility_gate_status=pending` under the gitignored `data/microstructure/` tree — without contacting any Binance API endpoint, opening any WebSocket, using any credential, modifying any verdict / lock / governance, normalizing into a separate dataset, computing any feature, or authorising any successor phase. The Phase 4aw scaffold + Phase 4ax aggTrades skeleton + Phase 4ay authorization framework compose cleanly with a working public-archive acquisition.

### 2. What did this phase not prove?

Anything about edge, opportunity rate, predictive content, microstructure feature viability, or strategy potential of the acquired data. The acquired dataset is one symbol's aggregate trades for a single UTC day; no statistical claim is made or licensed. No historical strategy verdict changed. No project lock changed. No cooled-down family is reopened.

### 3. Which original questions did it answer?

- "Can the project safely acquire one predeclared BTCUSDT public aggTrades daily archive, verify checksum, validate row integrity, store the raw archive under gitignored `data/microstructure/`, write a manifest with `research_eligible=false`, and fail closed on any uncertainty?" → **Yes** (verified in production by `SUCCESSFUL_ACQUISITION`; verified in the offline test suite by 35 passing tests).
- "Does the Phase 4ax aggTrades validator handle real Binance public-archive rows without modification?" → **Yes** (1,681,098 rows validated cleanly).
- "Does the Phase 4ay strict integrity gate work in practice?" → **Yes** (18 PASS + 1 NOT_APPLICABLE).

### 4. Which original questions remain open?

- Whether the Binance public archive is uniformly checksum-companion-equipped across other (symbol, date) combinations remains an acquisition-time consideration; Phase 4az verified availability for BTCUSDT 2025-01-15 only.
- Whether any aggTrades-derived feature would carry edge under §11.6 cost realism is not addressed.
- Whether the eligibility-gate primitive should ever be implemented is deferred to a separately authorized future phase.
- Whether to acquire ETHUSDT, additional days, monthly archives, or other data families is deferred — Phase 4az is one acquisition only.

### 5. What does it mean for strategy research?

Plumbing only. The project now has its first real microstructure raw dataset. The dataset is `research_eligible=false`; it is **infrastructure evidence only**. No strategy candidate is created. No cooled-down family is reopened. M0 admissibility and post-null cooldown remain binding for any future hypothesis.

### 6. What does it mean for governance?

Nothing changes. M0 (Phase 4ak), Phase 4al refined no-rescue rule, Phase 4j §11, Phase 3p §4.7, Phase 3r §8, Phase 3v §8, Phase 3w §6 / §7 / §8, and §11.6 / §1.7.3 remain verbatim. Phase 4az is the first concrete demonstration that the Phase 4ay authorization framework works end-to-end on real data.

### 7. Clean next step

After operator review and merge of Phase 4az, **remain paused** is the primary recommendation. Two natural separately-authorized next steps exist if the operator wishes to advance: (a) a docs-only Phase 4ba eligibility-gate review memo, or (b) a docs-only Phase 4ba data-quality interpretation memo (descriptive statistics only, no edge / feature evidence). Phase 4az **does not authorize** either.

### 8. What should we not do yet?

- Do not flip `research_eligible` to `True`.
- Do not normalise the dataset into Parquet / JSONL.
- Do not compute features.
- Do not create a strategy candidate.
- Do not run any backtest against the dataset.
- Do not acquire ETHUSDT, additional days, monthly archives, or any other data family.
- Do not contact any Binance API endpoint.
- Do not open any WebSocket.
- Do not approach paper / shadow, live-readiness, deployment, exchange-write, or production keys.
- Do not authorize a successor phase.

---

## 12. Preserved verdicts and locks

Phase 4az preserves verbatim:

- **H0** — FRAMEWORK ANCHOR.
- **R3** — BASELINE-OF-RECORD.
- **R1a** — RETAINED — NON-LEADING.
- **R1b-narrow** — RETAINED — NON-LEADING.
- **R2** — FAILED — §11.6.
- **F1** — HARD REJECT.
- **D1-A** — MECHANISM PASS / FRAMEWORK FAIL.
- **5m thread** — OPERATIONALLY CLOSED.
- **V2** — HARD REJECT — terminal for V2 first-spec.
- **G1** — HARD REJECT — terminal for G1 first-spec.
- **C1** — HARD REJECT — terminal for C1 first-spec.
- §11.6 = 8 bps slippage per side; round-trip = 16 bps.
- §1.7.3 = 0.25% risk per trade, 2× leverage cap, one position max, mark-price stops where applicable.
- Phase 3p §4.7 (kline strict integrity gate; aggTrades equivalent applied verbatim by Phase 4az).
- Phase 3r §8 (mark-price gap governance).
- Phase 3v §8 (stop-trigger-domain governance).
- Phase 3w §6 / §7 / §8.
- Phase 4j §11 (OI subset governance).
- Phase 4ak (M0 twelve-clause gate, post-null cooldown rule, cooled-down families list, memo template).
- Phase 4al (refined no-rescue rule + §13 boundary + §14 hierarchy).
- Phase 4am, Phase 4an, Phase 4ao, Phase 4ap, Phase 4aq, Phase 4ar, Phase 4as, Phase 4at, Phase 4au, Phase 4av, Phase 4aw, Phase 4ax, Phase 4ay results.

No new lock is introduced. No existing lock is loosened.

---

## 13. Recommendation

- **Primary:** remain paused. After operator review, merge Phase 4az into `main`, then stop.
- **Conditional secondary (NOT authorized by Phase 4az):** future docs-only Phase 4ba eligibility-gate review memo, separately authorized.
- **Conditional tertiary (NOT authorized by Phase 4az):** future docs-only Phase 4ba data-quality interpretation memo, separately authorized.
- **Not recommended:** acquiring more data, normalizing the dataset, computing features, implementing the eligibility-gate primitive without a docs-only review first.
- **Forbidden:** verdict revision, lock revision, parameter optimization, strategy resurrection, M0 amendment derived from Phase 4az reasoning, reopening the 5m research thread, flipping `research_eligible` to `True` without a separately authorized eligibility-gate phase, paper / shadow / live-readiness / deployment / exchange-write / production-key creation / authenticated APIs / private endpoints / user stream / live WebSocket implementation / MCP / Graphify / `.mcp.json` / credentials.

---

## 14. Final status

Phase 4az is **drafted** as a code-and-docs public-archive acquisition phase on branch `phase-4az/public-aggtrades-archive-acquisition`. It is ready for operator review and (if approved) merge into `main`.

After merge, the recommended state remains **paused**.

**No successor phase is authorized.**
