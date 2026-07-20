# Phase 4bn-AZ — Closeout

## 1. Phase name

Phase 4bn-AZ — CF-1 Realized-Volatility Substrate-Test Execution. The first and only authorized
execution of the CF-1 development experiment frozen and merged by Phase 4bn-AY. Code + tests +
bounded local data-reading + local gitignored artefacts + committed reports. Tier 1 / Full Phase.

## 2. Branch and base

- **Branch:** `phase-4bn-az/cf1-realized-volatility-substrate-test-execution`
- **Base `main` (== `origin/main`, verified before branching and unchanged at completion):**
  `e65feb849c8020b5e157d1c472b1a075244c7d9d`
- **Phase 4bn-AY merge commit:** `cd5a3b7128bb7bc8d887fb4c7ea1c1538e5b1305`
- **Phase 4bn-AY final scientific-contract tip:** `0fb560656aa9b50cf110602e15be8222b7343623`

The only untracked item at branch time was the transient `.claude/scheduled_tasks.lock`, which was
never staged, modified, deleted, cleaned, or committed.

## 3. Commit history and SHA self-reference convention

| # | SHA | Message | Role |
|---|---|---|---|
| 1 | `05fa63a8bf8c9b1fe386cc4ab67805046ae418b1` | `feat(phase-4bn-az): implement CF-1 substrate execution` | **Implementation commit** — created, pushed, and verified equal to origin **before** any market data was opened. This is the frozen evidence-bearing code SHA stamped into every artefact. |
| 2 | `00dfefdd82e8a31f86ff7ca6393ed76350d906d6` | `research(phase-4bn-az): record CF-1 execution verdict` | **Result commit** — the execution-and-verdict report and the artefact/leakage/split validation report. |
| 3 | *this commit* | `docs(phase-4bn-az): add closeout` | **Closeout commit.** A commit cannot embed its own SHA; per the established convention its exact SHA is recorded in the final operator report and in the Git log after commit. |

## 4. Exact files changed

Relative to base `main`, the AZ tracked diff is **eleven added files, no modifications, no
deletions, no renames**:

**Source (3)**
1. `src/prometheus/research/microstructure/cf1_realized_volatility_v001.py`
2. `src/prometheus/research/microstructure/cf1_evaluation_v001.py`
3. `src/prometheus/research/microstructure/cf1_artifacts_v001.py`

**Script (1)**
4. `scripts/phase4bn_az_cf1_realized_volatility_execution.py`

**Tests (4)**
5. `tests/research/microstructure/test_cf1_realized_volatility_v001.py`
6. `tests/research/microstructure/test_cf1_evaluation_v001.py`
7. `tests/research/microstructure/test_cf1_artifacts_v001.py`
8. `tests/research/microstructure/test_cf1_no_network_v001.py`

**Documents (3)**
9. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_cf1-execution-and-verdict.md`
10. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_cf1-artefact-leakage-and-split-validation.md`
11. `docs/00-meta/implementation-reports/2026-07-17_phase-4bn-az_closeout.md` (this file)

No `__init__.py` export change was required. No AY file, split policy, feature schema, manifest,
eligibility code, project lock, `pyproject.toml`, `uv.lock`, README, `current-project-state.md`, or
existing report was modified. No merge-closeout was created.

## 5. Exact local outputs (gitignored, not committed)

Root: `data/research/cf1_realized_volatility_substrate_test_v001/` — confirmed gitignored
(`.gitignore:88:data/research/`). Six artefacts, each with a valid paired `.sha256` sidecar
(`ALL_SIDECARS_VALID: True`):

| Relative path | SHA256 |
|---|---|
| `proofs/cf1_timestamp_boundary_proof_v001__v001__1784558563200__05fa63a8bf8c.json` | `ecdf0fcbad2e192968c0bb9960c8c9117813fd217e94c4a938f201e8aff77248` |
| `runs/cf1_execution_access_start_v001__v001__1784558563266__05fa63a8bf8c.json` | `66c807976dc43e1d74e697336b91a15a39f54814485197103c4a9878d43c2ed2` |
| `targets/cf1_realized_variance_target_layer_v001__v001__1784558563266__05fa63a8bf8c.parquet` | `9a7f1a922a02391ac997244e196e12446f56db6deb696ba66d5b8dffcc245010` |
| `proofs/cf1_leakage_split_coverage_proof_v001__v001__1784559571783__05fa63a8bf8c.json` | `c398d9ac6e1a4dabb86861d4f6d2a9c2c83f651a0d6cd56f090452646b0fba1e` |
| `manifests/cf1_model_run_manifest_v001__v001__1784558563266__05fa63a8bf8c.json` | `794480596f9623117f576d205f6fc5926769bf33e61f4494ffc023ad7027ebd9` |
| `manifests/cf1_execution_artifact_inventory_v001__v001__1784559572363__05fa63a8bf8c.json` | `fefc5b51e45b203283ff24f32f793fee6a23580adc142fa52514c626872bc1df` |

The `cf1_paired_model_predictions_v001` family was deliberately not written: no block produced a
fitted augmented model, so zero paired forecasts exist. No local artefact was staged or committed.

## 6. Exact verdict

```
CF1_INVALID_RUN
```

The single evidence-bearing run fail-closed at the frozen augmented-model numerical guard in **all
seven evaluation blocks**: augmented design-matrix condition numbers 1.019e+16 – 1.087e+16 against
the frozen threshold `> 1e10 ⇒ CF1_INVALID_RUN`. The baseline HAR design was well conditioned
throughout (3.418e+02 – 6.172e+02, full rank 4).

**Root cause (verified to machine precision).** The Phase 4bn-AY contract froze three features —
`rolling_aggtrade_count_60s`, `rolling_quantity_sum_60s`, `rolling_quantity_mean_60s` — together
with a natural-log transform. Because mean trade size is by definition sum ÷ count,
`ln(mean) ≡ ln(sum) − ln(count)` identically, so the three log-features span two dimensions and the
7-column augmented design is structurally rank 6. Measured on the frozen target layer across all
5,516 valid origins: `max |ln(x3) − (ln(x2) − ln(x1))| = 3.33e-14`. The defect is in the
**preregistered design**, not in the data, the substrate, the implementation, the timestamp
semantics, the split, or the leakage controls.

Everything upstream succeeded: 244 partitions opened and integrity-verified, 340,447,363 rows read
per family, 5,516 valid paired origins, every block above its minimum (valid eval origins B1 720,
B2 744, B3 720, B4 744, B5 744, B6 719, B7 550; training origins 551 – 4,966), the synthetic
timestamp-boundary proof PASSED before any data read, and the leakage/split/coverage proof PASSED
before any metric.

**No QLIKE, `d_{i,t}`, `D_i`, `Δ_equal`, `ρ`, MSE, MZ R², or bootstrap was computed.** P4 is false
on its own terms; P1/P2/P3 are recorded `false` only as uninitialised placeholders and are **not**
negative scientific findings.

## 7. Exact result state

```
CF1_INVALID_RUN__NO_SCIENTIFIC_CLAIM__NO_RERUN_AUTHORIZED__SEPARATE_CORRECTIVE_PHASE_REQUIRED__RESERVES_UNTOUCHED
```

## 8. No scientific claim

An invalid run is **not** interpretable scientifically — neither a pass nor a fail — and must never
be converted into one. Phase 4bn-AZ makes **no** claim about the CF-1 hypothesis. `H0` was neither
rejected nor supported. The result does **not** show that the aggTrades microstructure features are
uninformative about future realized-volatility magnitude; it shows only that, as frozen, they are
mutually redundant and cannot be jointly estimated. The Phase 4bn-AY §32 fail consequence
(materially narrowing the magnitude lane) explicitly does **not** apply, because there was no valid
fail. The magnitude lane is **not** narrowed by this phase.

## 9. No rerun

The one authorized evidence-bearing run has been consumed. **No rerun is authorized** — not with
corrected code, not with a modified feature set, not with a relaxed numerical guard, not with a
different seed. The code was frozen at `05fa63a8bf8c…` at the moment the access-start record was
written, and was not modified thereafter. No patch-and-rerun occurred, no constant was changed, no
output was altered, no adverse block or date was excluded, and no second scientific implementation
was run to confirm the answer. Only artefact hashes were recomputed, plus one permitted lightweight
arithmetic validation of the already-frozen target layer using identical formulas and no new market
data.

## 10. No reserve

`No evidence reserve was spent by Phase 4bn-AZ.` `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED` and
`V002_SEALED_TEST = UNTOUCHED_RESERVED` are preserved exactly and were never opened.
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED` is preserved and was never opened. The
`UNUSED_NON_RESERVE_BUFFER` (2024-11-01..2024-11-15), 2024-11-16, and 2024-10-01 were never opened.
Verified: `v002_terminal_window_read = false`, `sealed_test_split_touched = false`,
`test_rows_loaded = 0`, `consumed_holdout_opened = false`, `november_buffer_opened = false`.

## 11. No PnL / no trading

`No signal generation, strategy, PnL analysis, backtest, replay, paper, shadow, live, or
exchange-write execution was performed or is authorized by Phase 4bn-AZ.` No directional or
tradable object was produced. No plot, notebook, or exploratory output exists. `network_used =
false`; `data_acquisition_used = false`; all eight non-authorization flags are `false`.

## 12. Preserved locks

Unchanged and preserved exactly: `STOP_LONGHORIZON_ML_ARC` and
`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct; not merged, softened, reinterpreted, rescued,
reopened, or continued); `REJECTED_AS_RESCUE_SHAPED_PROXY_MECHANISM_MISMATCH`;
`PRE_V002_INTERNAL_HOLDOUT = CONSUMED`; `V002_TERMINAL_WINDOW = UNTOUCHED_RESERVED`;
`V002_SEALED_TEST = UNTOUCHED_RESERVED`; `HIST_TOB_BOOKTICKER_SOURCE =
INADMISSIBLE_OR_UNAVAILABLE`; `test_rows_loaded = 0`; `research_eligible = false`;
`eligibility_gate_status = pending`; all published authorization flags false; Phase 4aw
`flip_research_eligible(...)` always-raising and never invoked; Phase 4bn-AE §19; the Phase 4ak
twelve-clause M0 gate with §6 cooldown and §7 cooled-down families; M0 cooldown and
cooled-down-family rules; the locked 8 bps/side · 16 bps round trip; every prior verdict and
retained-evidence classification; every dataset identity and hash; all split, holdout, sidecar, and
storage policies (Phase 4bn-Y / L / AA / 4bb-F); the Phase 4bn-AV evidence ledger, spending-authority
standard, and late-inadmissibility protocol. `docs/00-meta/current-project-state.md` and the README
are left unchanged by this phase.

The operator's acceptance of the CF-1 M0.3 mapping remains scoped to the frozen development-level
comparison only; it cleared no directional strategy through M0 and authorized no reserve spend.

## 13. Merge non-authorization

**No merge is performed or authorized by this phase.** No merge-closeout is created. Merging Phase
4bn-AZ into `main` requires a **separate operator prompt and decision**. `main` and `origin/main`
remain exactly `e65feb849c8020b5e157d1c472b1a075244c7d9d`; no `main` push and no SHA-finalization
commit were performed. No successor phase is authorized by this closeout.

## 14. Recommended next operator action

Based strictly on the `CF1_INVALID_RUN` verdict:

1. **Return this closeout and the two AZ reports to ChatGPT for compliance review**, and decide
   separately whether to merge the AZ branch. Merging is a recording decision (it preserves the
   execution evidence and the discovered contract defect in `main`); it is not a scientific
   endorsement, since an invalid run carries no claim.
2. **Do not authorize any CF-1 re-execution.** Re-running the experiment as frozen is guaranteed to
   reproduce `CF1_INVALID_RUN` on any data, because the collinearity is an algebraic identity of the
   feature contract.
3. If the operator wishes to pursue the CF-1 question at all, the only admissible next step is a
   **separate, docs-only contract-correction phase** that re-preregisters the feature contract —
   because the defect lives in the merged Phase 4bn-AY scientific contract, correcting it is a
   preregistration change and must not be done inside an execution phase. Such a phase would need a
   new mechanism justification, an explicit anti-duplication audit, and its own operator
   authorization. **This closeout neither authorizes nor designs that phase, and does not
   pre-approve any particular remedy** (for example dropping the redundant third feature, or
   replacing it with a genuinely independent sign-invariant column).
4. **Remaining paused is a fully valid operator choice.** Nothing in this phase creates pressure to
   continue: no lane was narrowed, no reserve was spent, and no arc was reopened.

Recommended state: **paused**, pending operator review and a separate merge decision.
