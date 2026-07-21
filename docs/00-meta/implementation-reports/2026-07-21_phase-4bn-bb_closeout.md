# Phase 4bn-BB — Closeout

## 1. Phase identity

Phase 4bn-BB — Corrected CF-1 Realized-Volatility Substrate-Test Execution. A code + tests + local
gitignored artefacts + committed evidence-report phase executing exactly one new evidence-bearing
corrected CF-1 run under the merged Phase 4bn-BA contract.

`Phase 4bn-BB is a new corrected experiment under the merged Phase 4bn-BA contract, not a rerun or continuation of Phase 4bn-AZ.`

## 2. Branch and base

- **Branch:** `phase-4bn-bb/corrected-cf1-realized-volatility-substrate-test-execution`.
- **Base `main` == `origin/main`:** `e26193e8f61cae797e4cbfab932025b709b74566` (Phase 4bn-BA
  merge-closeout SHA-finalization tip), unchanged throughout.
- Required lineage confirmed: BA merge `7096ce853dd85dfe6bd95ae88942548bc76400dd`; BA merge-closeout
  branch `ba6ddf12dfa97a2f4ef04abf2bd35127c7f04274`; BA contract tip
  `adc06e68cf532e00b0477d0cefca9d97d2287449`; AY contract tip
  `0fb560656aa9b50cf110602e15be8222b7343623`; AZ implementation
  `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1`; AZ merge
  `8e82e185a0def318acd2ec42fcb73337edc67b51`.

## 3. Commits

| Role | SHA |
|---|---|
| BB implementation commit | `0f5942b31e6dfa5ca537ec2c8b962a0ce57c8917` |
| BB result (execution + verdict + artefact/leakage) commit | `6ba76b56a514cb0abaeac0480a59a688a7cdebeb` |
| BB closeout / final phase SHA | this commit (`docs(phase-4bn-bb): add closeout`) |

Final-phase-SHA convention: this closeout commit's own SHA is the canonical Phase 4bn-BB branch tip;
it is recorded in the final operator report and Git log after commit. No merge is performed or
authorized.

## 4. Files added

**Source (3):**

- `src/prometheus/research/microstructure/cf1_corrected_contract_v002.py`
- `src/prometheus/research/microstructure/cf1_corrected_evaluation_v002.py`
- `src/prometheus/research/microstructure/cf1_corrected_artifacts_v002.py`

**Script (1):**

- `scripts/phase4bn_bb_cf1_corrected_realized_volatility_execution.py`

**Tests (5):**

- `tests/research/microstructure/test_cf1_corrected_contract_v002.py`
- `tests/research/microstructure/test_cf1_corrected_evaluation_v002.py`
- `tests/research/microstructure/test_cf1_corrected_artifacts_v002.py`
- `tests/research/microstructure/test_cf1_corrected_no_network_v002.py`
- `tests/research/microstructure/test_phase4bn_bb_cf1_corrected_execution.py`

**Reports (3):**

- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-execution-and-verdict.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_cf1-corrected-artefact-leakage-and-split-validation.md`
- `docs/00-meta/implementation-reports/2026-07-21_phase-4bn-bb_closeout.md` (this file)

No additional helper file was created. **No Phase 4bn-AY, Phase 4bn-AZ, or Phase 4bn-BA document was
modified**; the historical AZ orchestration/evaluation/artifact modules and
`cf1_realized_volatility_v001` were not modified. No data path or local artefact was staged or
committed.

## 5. Test / lint / type results

- BB unit tests (all five files): **PASS** (contract, evaluation, artifacts, no-network, runner).
- Full `tests/research/microstructure` directory: **PASS**.
- `ruff check` over the nine new/affected files: **All checks passed**.
- `mypy --strict` over the three corrected source modules: **Success: no issues found in 3 source
  files**.
- Full suite `uv run pytest -q` before data access: two failures, both in
  `tests/simulation/test_backtest_real_2026_03.py::{test_real_2026_03_btcusdt, test_real_2026_03_ethusdt}`
  — `KeyError: 'trade_count'` in `src/prometheus/research/data/storage.py:232` while reading **kline**
  Parquet. These are **pre-existing** and **unrelated to Phase 4bn-BB**: the failing tests import
  `prometheus.research.backtest` / `research.data.storage` / klines and reference no CF-1,
  microstructure, aggTrades, or BB code; the BB additions are purely additive new files that cannot
  affect those modules. No BB-related failure exists.

(Note: `uv run pytest` invoked the pytest console-script trampoline, which errored in this
environment with "uv trampoline failed to canonicalize script path"; the identical suite was run via
`uv run python -m pytest`, which is equivalent and avoids the stale trampoline exe.)

## 6. Execution accounting

- `--preflight` invocations: **1** (standalone final preflight) → `PREFLIGHT_PASS`. The `--run`
  command additionally reran the full preflight internally.
- `--run` invocations: **exactly 1**.
- Access-start artefact written: **yes**, at `2026-07-21T17:36:13.417563Z`, immediately before the
  first market-data byte.
- Market-data access began: **yes**. **The single Phase 4bn-BB evidence-bearing run is consumed.**

## 7. Exact outcome and result state

- Scientific outcome: **`CF1_VALID_PASS`**.
- P1 (`Δ_equal = 0.011938843831425896 > 0`): true. P2 (positive block count 7/7 ≥ 6): true. P3
  (`LB_95 = 0.006273843055395148 > 0`): true. Validity: true.
- Long result state:

```
CF1_CORRECTED_VALID_PASS__DEVELOPMENT_LEVEL_INCREMENTAL_VOLATILITY_MAGNITUDE_INFORMATION_SUPPORTED__DOCS_ONLY_FILTER_ASSESSMENT_ONLY__NO_DIRECTION_OR_PNL_AUTHORIZED__RESERVES_UNTOUCHED
```

## 8. Artefact root and integrity

- BB output root: `data/research/cf1_corrected_realized_volatility_substrate_test_v002/`, **local and
  gitignored**. Eight artefact families + paired `.sha256` sidecars (16 files); all sidecar digests
  recomputed and validated (8/8). No data or artefact committed.
- The target layer carries exactly two feature columns; the prohibited `rolling_quantity_mean_60s`
  column appears in no schema, payload, or manifest.

## 9. Phase 4bn-AZ status

`Phase 4bn-AZ remains CF1_INVALID_RUN and its evidence-bearing run remains consumed.` No Phase 4bn-AZ
local artefact was opened or reused; the AZ v001 output root was never read
(`az_output_root_read = false`). The committed AZ reports were consulted as historical documentation
only.

## 10. No-rerun after access

The single Phase 4bn-BB evidence-bearing run is consumed. **No rerun of `--run` is authorized.** No
second seed, second feature set, second bootstrap, or second evidence-bearing invocation is
authorized.

## 11. Scientific consequence

A valid pass supports **development-level incremental one-hour realized-volatility magnitude
information only** — docs-only filter assessment. It establishes no direction, no signal, no
profitability, no ability to clear the locked 8 bps/side · 16 bps round trip, no tradability, and no
M0 clearance. Recommended next action: a **separate docs-only filter-admissibility and consequence
assessment**. No strategy, signal, or PnL phase is automatically authorized.

`No direction, signal, strategy, PnL, backtest, paper, shadow, live, or exchange-write authorization follows from Phase 4bn-BB.`

## 12. Preserved governance locks

Preserved exactly and unchanged: `STOP_LONGHORIZON_ML_ARC`;
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE = INADMISSIBLE_OR_UNAVAILABLE`;
`test_rows_loaded = 0`; `research_eligible = false`; `eligibility_gate_status = pending`; all
authorization flags false; the Phase 4aw always-raising `flip_research_eligible(...)` flip (never
invoked); Phase 4bn-AE §19; the Phase 4ak twelve-clause M0 gate with its cooldown and
cooled-down-family rules; 8 bps/side and 16 bps round trip; every prior verdict; every dataset
identity/hash; all split/holdout/sidecar/storage policies; and the evidence-ledger and
spending-authority rules. No stopped arc is softened, merged, reinterpreted, reopened, or rescued.

## 13. Working tree, merge, and successor non-authorization

- Working tree clean except the transient `.claude/scheduled_tasks.lock`; no local artefact tracked;
  no data committed; `main == origin/main == e26193e8f61cae797e4cbfab932025b709b74566`.
- **No merge is performed or authorized. No merge-closeout is created.**
- **No successor phase is authorized and no successor prompt is drafted.** Any downstream action —
  including a docs-only filter-admissibility assessment — requires separate operator authorization
  and a new Claude Code prompt.

## 14. Recommended next operator action

Review the three Phase 4bn-BB reports and the local (gitignored) artefacts. Then decide separately
whether to (a) authorize a merge phase for Phase 4bn-BB, and/or (b) authorize a separate docs-only
CF-1 filter-admissibility and consequence assessment. Default recommendation: **remain paused**.

`Remaining paused is a valid operator choice.`
