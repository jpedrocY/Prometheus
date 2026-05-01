# Phase 4j Closeout

## Summary

Phase 4j (V2 Metrics Data Governance Memo) is **complete on the
Phase 4j branch and not merged to main**. Phase 4j decided how the
Phase 4i metrics partial-pass evidence is governed before any V2
backtest can be considered, mirroring the Phase 3r §8 mark-price
gap governance pattern.

Phase 4j is **docs-only**. No source code, tests, scripts, data,
manifests, specs, thresholds, parameters, project locks, or prior
verdicts were modified. No data was acquired. No backtests were
run. No Phase 4i acquisition script was modified or executed. No
Phase 4i manifest was modified. No Phase 4f / 4g / 4h / 4i text
was modified.

V2 remains **pre-research only**: not implemented, not backtested,
not validated, not live-ready, **not a rescue** of R3 / R2 / F1 /
D1-A.

Phase 4j recommendation: **adopt Phase 4j §11 as binding governance;
remain paused** (Option A) primary; **adopt Phase 4j §11 + authorize
a docs-only V2 backtest-plan phase as future Phase 4k** (Option B)
conditional secondary. **No** immediate V2 backtest; **no** V2
implementation; **no** patching / forward-fill / interpolation; **no**
mark-price acquisition; **no** aggTrades acquisition; **no** paper /
shadow / live / exchange-write.

## Files changed

The Phase 4j branch introduces two new docs-only files relative to
`main`:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4j_v2-metrics-data-governance.md`
  (Phase 4j governance memo; 26 sections; 1397 lines)
- `docs/00-meta/implementation-reports/2026-04-30_phase-4j_closeout.md`
  (this file)

`docs/00-meta/current-project-state.md` is **NOT modified** on the
Phase 4j branch (per the Phase 4j brief). It would be updated only
during the merge housekeeping commit, after a separate operator
authorization.

No source code, tests, scripts, existing data, existing manifests,
specs, thresholds, parameters, project locks, or prior verdicts were
modified by Phase 4j. No new manifest was created. No corrected
manifest was created. No `__v002` metrics manifest was created. No
v003 dataset family was created. No data was acquired. No data was
downloaded. No data was patched, forward-filled, interpolated, or
silently omitted.

## Governance conclusion

Phase 4j adopts the **Phase 4j §11 metrics OI-subset
partial-eligibility rule** — a 12-clause binding governance rule
immutable from operator approval forward — as the recommended
disposition for the Phase 4i metrics partial-pass evidence.

The rule preserves all integrity discipline:

- Metrics manifests remain GLOBALLY `research_eligible: false`. No
  manifest modification. No corrected manifest. No `__v002` metrics.
  No v003.
- Feature-level partial-eligibility is permitted for the OI subset
  only (`create_time`, `symbol`, `sum_open_interest`,
  `sum_open_interest_value`).
- The four optional ratio columns
  (`count/sum_toptrader_long_short_ratio`, `count_long_short_ratio`,
  `sum_taker_long_short_vol_ratio`) remain `feature_eligible: false`
  for V2's first backtest.
- Any 30m V2 signal bar whose six aligned 5-minute metrics records
  are not all present AND non-NaN in OI columns is EXCLUDED from V2
  candidate setup generation.
- No forward-fill, no interpolation, no imputation, no replacement,
  no synthetic OI data.
- Exclusions must be counted and reported per §11.6.
- A sensitivity analysis comparing main-cell vs.
  exclude-entire-affected-days variant is required per §11.7.
- The rule never revises retained verdicts, never licenses backtest
  authorization, and is immutable from operator approval forward.

The Phase 4j §11 rule mirrors the Phase 3r §8 pattern transposed
from per-trade exclusion (Q6 mark-price) to per-bar exclusion (V2
candidate setup metrics OI). The pattern is proven — Phase 3r §8
has been the standing governance for mark-price gaps since the
Phase 3r merge.

## Metrics evidence recap

Per Phase 4i:

- **Four kline datasets are research_eligible:**
  - `binance_usdm_btcusdt_30m__v001` (74 448 bars; 0 gaps).
  - `binance_usdm_ethusdt_30m__v001` (74 448 bars; 0 gaps).
  - `binance_usdm_btcusdt_4h__v001` (9 306 bars; 0 gaps).
  - `binance_usdm_ethusdt_4h__v001` (9 306 bars; 0 gaps).
- **BTCUSDT metrics is NOT research_eligible:**
  - 446 555 / 446 688 records (133 short).
  - 5 699 missing 5-minute observations.
  - 91 840 rows with at least one NaN in optional ratio columns.
  - 0 missing daily archives.
  - **Required `sum_open_interest` and `sum_open_interest_value`
    fully populated** (zero NaN).
- **ETHUSDT metrics is NOT research_eligible:**
  - 446 555 / 446 688 records (133 short).
  - 3 631 missing 5-minute observations.
  - 91 841 rows with at least one NaN in optional ratio columns.
  - 0 missing daily archives.
  - **Required `sum_open_interest` and `sum_open_interest_value`
    fully populated** (zero NaN).
- NaN values are concentrated in optional ratio columns, especially
  early-2022 (~97% NaN in 2022-01 ratio columns; ~0% NaN by 2026-03).
- Phase 4i did NOT relax strict gates and stopped for operator review.

## Chosen governance rule

**Phase 4j §11 metrics OI-subset partial-eligibility rule.**

Twelve binding clauses (full normative form in Phase 4j §11.1):

1. **§11.1** — Metrics manifests remain globally
   `research_eligible: false`. No manifest modification.
2. **§11.2** — Feature-level partial-eligibility for the OI subset
   only.
3. **§11.3** — Optional ratio columns remain `feature_eligible: false`.
4. **§11.4** — Per-bar exclusion test: 30m signal bar OI-feature-eligible
   only if all six aligned 5-minute records are present AND non-NaN
   in OI columns.
5. **§11.5** — No forward-fill, interpolation, imputation,
   replacement, synthetic OI data.
6. **§11.6** — Exclusions must be counted and reported in any future
   V2 backtest output.
7. **§11.7** — Sensitivity analysis required (main-cell vs.
   exclude-entire-affected-days).
8. **§11.8** — No automatic prior-verdict revision.
9. **§11.9** — No strategy rescue, parameter change, or live-readiness
   implication.
10. **§11.10** — No silent rule revision (rule is immutable absent
    a separately authorized amendment).
11. **§11.11** — Exclusion test must be predeclared in any future
    V2 backtest brief.
12. **§11.12** — Optional ratio activation requires separate
    operator authorization.

Predeclared OI delta computation rule (Phase 4j §17): last completed
5-minute OI of current 30m window vs. last completed 5-minute OI
of previous 30m window (point-in-time clear; no future records; no
partial windows; no mean-over-window aggregation).

## Backtest preconditions

A future V2 backtest remains BLOCKED until ALL of the following are
satisfied (per Phase 4j §20):

1. Phase 4j is merged to `main`.
2. `docs/00-meta/current-project-state.md` records the governance
   rule.
3. A separate V2 backtest-plan phase is authorized.
4. V2 backtest code explicitly implements the Phase 4j per-bar
   exclusion rule.
5. V2 backtest report separately reports:
   - the number of 30m bars excluded by metrics OI gaps;
   - the number of V2 candidate setups excluded;
   - the number of V2 trades excluded;
   - whether exclusions cluster by date / regime;
   - sensitivity to excluding all dates with metrics invalid windows;
   - explicit confirmation that NO optional ratio column was used.

**Phase 4j does NOT authorize any of these.** The V2 backtest-plan
phase is conditional secondary.

## Candidate next-slice decision

Phase 4j §25 presents the operator decision menu:

- **Option A — Adopt Phase 4j §11 as binding governance; remain
  paused.** **PRIMARY RECOMMENDATION.** The operator approves Phase
  4j §11 as the formally binding governance rule. Phase 4j is merged
  when convenient. Strategy execution remains paused.
- **Option B — Adopt Phase 4j §11 + authorize a docs-only V2
  backtest-plan phase (future Phase 4k).** **CONDITIONAL SECONDARY.**
  The operator approves §11 AND authorizes a follow-on docs-only
  memo that operationalizes the per-bar exclusion algorithm,
  predeclares the backtest implementation plan, predeclares evidence
  thresholds, and predeclares variant comparison rules. The plan
  phase would itself be docs-only.
- **Option C — Reject Phase 4j §11 and keep V2 backtesting blocked
  indefinitely.** Procedurally safe but stalls V2 even though
  V2-required `sum_open_interest` is fully populated. **NOT
  RECOMMENDED.**
- **Option D — Reject Phase 4j §11 and remove the OI feature from
  V2.** Modifies Phase 4g §28; forbidden by Phase 4j brief
  ("Do not remove the OI feature from V2 in Phase 4j"). **NOT
  RECOMMENDED.**
- **Option E — Authorize a metrics data-patching governance memo
  permitting forward-fill / interpolation.** **REJECTED.** Forbidden
  by Phase 3r §8 / Phase 3p §4.7 / Phase 4h §17–§19 / Phase 4i §17.
- **Option F — Immediate V2 backtest.** **REJECTED.** Phase 4i and
  Phase 4j both block this until a separately authorized
  backtest-plan phase is in place.
- **Option G — Paper / shadow / live-readiness / exchange-write.**
  **FORBIDDEN.** Per `docs/12-roadmap/phase-gates.md`, none of
  these gates is met.

## Commands run

The following commands were run during Phase 4j per the Phase 4j
brief:

| # | Command | Purpose |
|---|---|---|
| 1 | `git status` | Verify clean tree pre-branch |
| 2 | `git checkout -b phase-4j/v2-metrics-data-governance` | Create Phase 4j branch |
| 3 | `git rev-parse main`, `git rev-parse origin/main` | Verify main == origin/main at 17ebb75 |
| 4 | `.venv/Scripts/python --version` | Confirm Python toolchain |
| 5 | `.venv/Scripts/python -m ruff check .` | Verify whole-repo Ruff clean |
| 6 | `.venv/Scripts/python -m pytest` | Verify whole-repo pytest clean |
| 7 | `.venv/Scripts/python -m mypy` | Verify mypy strict clean |
| 8 | `git add ... && git commit -m ...` | Commit Phase 4j memo |
| 9 | `git push -u origin phase-4j/...` | Push Phase 4j branch |

The following commands were **NOT** run (per Phase 4j brief
prohibitions):

- No `scripts/phase3q_5m_acquisition.py` execution.
- No `scripts/phase3s_5m_diagnostics.py` execution.
- No `scripts/phase4i_v2_acquisition.py` execution.
- No backtest execution.
- No diagnostics execution.
- No data acquisition.
- No data download.
- No new public Binance endpoint consulted.

## Verification results

| Check | Result |
|---|---|
| `.venv/Scripts/python --version` | `Python 3.12.4` |
| `.venv/Scripts/python -m ruff check .` | `All checks passed!` |
| `.venv/Scripts/python -m pytest` | `785 passed in 12.53s` |
| `.venv/Scripts/python -m mypy` | `Success: no issues found in 82 source files` |

Whole-repo quality gates remain **fully clean**: zero ruff errors;
785 / 785 tests passing; zero mypy strict issues across 82 source
files. No regressions relative to the post-Phase-4i-merge baseline.

## Commit

| Role | SHA | Message |
|---|---|---|
| Phase 4j memo | `6fa92766da5b47ef1d5ebf2b7f7c8334e15b317e` | phase-4j: V2 metrics data governance memo (docs-only) |
| Phase 4j closeout | `<recorded in chat closeout block after this file is committed>` | docs(phase-4j): closeout report (Markdown artefact) |

## Final git status

After the closeout commit and push:

```text
On branch phase-4j/v2-metrics-data-governance
Your branch is up to date with 'origin/phase-4j/v2-metrics-data-governance'.

nothing to commit, working tree clean
```

## Final git log --oneline -5

(Captured after the closeout commit; recorded verbatim in the chat
closeout block.)

## Final rev-parse

(Captured after the closeout commit; recorded verbatim in the chat
closeout block: `git rev-parse HEAD` and
`git rev-parse origin/phase-4j/v2-metrics-data-governance`.)

## Branch / main status

- Phase 4j branch: `phase-4j/v2-metrics-data-governance` exists
  locally and on `origin`.
- Phase 4j branch is **NOT merged to main**.
- `main` and `origin/main` remain at
  `17ebb755ce32ccc5d605329d9972df2e4ce2f140` (Phase 4i housekeeping).
- A separate operator authorization is required before any merge.

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4k / successor phase started.** No
  subsequent phase has been authorized, scoped, briefed, branched,
  or commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 validation.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **No `scripts/phase3q_5m_acquisition.py` execution.**
- **No `scripts/phase3s_5m_diagnostics.py` execution.**
- **No `scripts/phase4i_v2_acquisition.py` execution.**
- **No data acquisition / patching / regeneration / modification.**
- **No data download.**
- **No `data/manifests/*.manifest.json` modification.** All Phase
  4i manifests preserved verbatim. All v002 / v001-of-5m manifests
  preserved verbatim.
- **No corrected manifest created.**
- **No `__v002` metrics manifest created.**
- **No v003 created.**
- **No mark-price 30m / 4h acquisition.**
- **No `aggTrades` acquisition.**
- **No spot data acquisition.**
- **No cross-venue data acquisition.**
- **No funding-rate re-acquisition.**
- **No silent OI patching.**
- **No forward-fill.**
- **No interpolation.**
- **No imputation.**
- **No silent omission.**
- **No optional ratio-column activation.**
- **No OI feature removal from V2.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 /
  D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3r §8 mark-price gap governance modification.**
- **No Phase 3v `stop_trigger_domain` governance modification.**
- **No Phase 3w `break_even_rule` / `ema_slope_method` /
  `stagnation_window_role` governance modification.**
- **No Phase 4f text modification.**
- **No Phase 4g V2 strategy-spec modification.**
- **No Phase 4h text modification.**
- **No Phase 4i text modification.**
- **No Phase 4i acquisition script modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No existing `scripts/**` modification.**
- **No `prometheus.research.data.*` extension.**
- **No `Interval` enum extension.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `.env` file creation.**
- **No credential storage / request / use.**
- **No authenticated REST / private endpoint / public endpoint /
  user-stream / WebSocket calls.**
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling.**
- **No deployment artefact created.**
- **No paper / shadow runtime created.**
- **No live-readiness implication.**
- **No order placement / cancellation.**
- **No real exchange adapter implementation.**
- **No exchange-write capability.**
- **No reconciliation implementation.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the
  Phase 4j branch.**
- **No `.claude/rules/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused** for any successor phase. Phase
  4j deliverables exist as branch-only artefacts pending operator
  review.
- **Phase 4j output:** docs-only governance memo + this closeout
  artefact on the Phase 4j branch.
- **Repository quality gate state:** **fully clean.** Whole-repo
  `ruff check .` passes; pytest 785 passed; mypy strict 0 issues
  across 82 source files (verified during Phase 4j).
- **5m research thread state:** Operationally complete and closed
  (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase
  4 (canonical) remains not authorized. Phase 4a–4i all merged.
  Phase 4j V2 metrics governance memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 +
  enforced in code by Phase 4a (preserved through Phase 4j).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced
  in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced
  in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 +
  enforced in code by Phase 4a (preserved).
- **Mark-price gap governance:** Phase 3r §8 (preserved).
- **V2 metrics governance:** Phase 4j §11 (this branch; recommended
  for adoption as binding governance).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet
  enforced in code.
- **V2 strategy-research direction:** Predeclared by Phase 4f as
  *Participation-Confirmed Trend Continuation*; operationalized by
  Phase 4g (strategy spec) and Phase 4h (data requirements).
  Phase 4i acquired 6 dataset families; 4 of 6 research-eligible;
  2 of 6 (metrics) NOT research-eligible. Phase 4j defines the
  binding governance for partial-eligibility OI-subset use of the
  metrics datasets. V2 is **NOT implemented; NOT backtested; NOT
  validated; NOT live-ready; NOT a rescue.**
- **OPEN ambiguity-log items after Phase 4j:** zero relevant to
  runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0
  framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained
  research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks;
  F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other;
  §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price
  stops; v002 verdict provenance; Phase 3q mark-price 5m manifests
  `research_eligible: false`; Phase 4i metrics manifests
  `research_eligible: false`. All preserved.
- **Branch state:** `phase-4j/v2-metrics-data-governance` exists
  locally and on `origin`. NOT merged to main.

## Next authorization status

**No next phase has been authorized.** Phase 4j's primary
recommendation is **Option A** (adopt Phase 4j §11 as binding
governance; remain paused), with **Option B** (adopt §11 + authorize
a docs-only V2 backtest-plan phase as future Phase 4k) as
**conditional secondary**.

Selection of any subsequent phase requires explicit operator
authorization for that specific phase. No such authorization has
been issued.

The 5m research thread remains operationally complete and closed
(per Phase 3t). The implementation-readiness boundary remains
reviewed (per Phase 3u). All four Phase 3u §8.5 pre-coding
governance blockers remain RESOLVED at the governance level (per
Phase 3v + Phase 3w). The Phase 4a safe-slice scope is implemented
(per Phase 4a). The Phase 4b / 4c quality-gate restorations are
complete. The Phase 4d post-4a/4b/4c review is complete. The Phase
4e reconciliation-model design memo is complete. The Phase 4f V2
hypothesis predeclaration is complete. The Phase 4g V2 strategy spec
is complete. The Phase 4h V2 data-requirements / feasibility memo
is complete. The Phase 4i V2 public data acquisition + integrity
validation is complete with partial-pass verdict. The Phase 4j V2
metrics data governance memo is complete on this branch (this
phase) and recommends adoption of the §11 metrics OI-subset
partial-eligibility rule as the binding governance for any future
V2 backtest. **Recommended state remains paused.**
