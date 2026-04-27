# Slippage Wording Consistency Cleanup Report

**Date:** 2026-04-27 UTC.
**Branch:** `docs/slippage-wording-consistency`.
**Scope:** Docs-only correction of stale textual descriptions of slippage tiers in older Phase 2 reports so they match the canonical project config (`src/prometheus/research/backtest/config.py` `DEFAULT_SLIPPAGE_BPS`).

**Canonical values (unchanged):**

```python
DEFAULT_SLIPPAGE_BPS: dict[SlippageBucket, float] = {
    SlippageBucket.LOW: 1.0,        # 0.01% per side
    SlippageBucket.MEDIUM: 3.0,     # 0.03% per side  (committed default)
    SlippageBucket.HIGH: 8.0,       # 0.08% per side
}
```

This cleanup was identified by Phase 2y §2.6 / §4.4 as out-of-Phase-2y-scope and explicitly recommended for a future docs-only consistency-cleanup phase. This file IS that phase.

---

## 1. Files inspected

### 1.1 Files explicitly listed in the operator brief

- `docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md`
- `docs/00-meta/implementation-reports/2026-04-27_phase-2x_family-review-memo.md`

### 1.2 Files surfaced by repository-wide grep on stale phrases

Grep patterns searched across `docs/00-meta/implementation-reports/`:

- `LOW = 0`
- `MEDIUM = 5`
- `HIGH = 15`
- `3× baseline` / `3x baseline`
- `3× MED` / `3x MED`
- `MEDIUM (5 bps`
- `5 bps`
- `15 bps`

Files that matched (after triage):

| File | Match category | Action |
|------|----------------|--------|
| `2026-04-26_phase-2l_R3_variant-comparison.md` | line 331 (header text); line 342 (prose) | **CORRECTED** |
| `2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md` | line 350 (header text); line 361 (prose) | **CORRECTED** |
| `2026-04-27_phase-2s_R1b-narrow_variant-comparison.md` | line 386 (prose) | **CORRECTED** |
| `2026-04-27_phase-2x_family-review-memo.md` | line 151 (table header); line 153 (prose in R3 row) | **CORRECTED** |
| `2026-04-27_phase-2v_R2_gate-1-execution-plan.md` | line 63 (matched on `3× MED` inside an existing self-correction note quoting prior-draft wording) | **NOT TOUCHED** — already correct; the matched phrase is inside an explanatory parenthetical that documents a prior-draft correction (canonical 1/3/8 bps already stated). |
| `2026-04-27_phase-2y_slippage-cost-policy-review.md` | lines 87, 91, 177 (memo deliberately quotes the stale wording as historical evidence in §2.6) | **NOT TOUCHED** — operator brief constraint #4: "Do not alter Phase 2y's conclusion." Phase 2y §2.6's quote is the historical record of what was stale at the time the memo was written. |
| `2026-04-27_phase-2y_closeout-report.md` | line 61 (closeout report quotes Phase 2y memo's flagged inconsistency) | **NOT TOUCHED** — same reasoning. |
| `2026-04-20_phase-2e-baseline-summary.md` | lines 17, 186 ("3 bps slippage MEDIUM, 5 bps taker fee") | **NOT TOUCHED** — already correct (3 bps is the canonical MED value; 5 bps is the canonical taker fee). |
| `2026-04-24_phase-2g_wave1_variant-comparison.md` | line 7 ("taker = 5 bps, slippage = MEDIUM (3 bps)") | **NOT TOUCHED** — already correct. |
| `2026-04-27_phase-2s_R1b-narrow_variant-comparison.md` line 55 ("taker fee rate 0.0005 (5 bps)") | line 55 only matched "5 bps" for taker fee | **NOT TOUCHED** — already correct (5 bps taker fee is the canonical value). |
| `2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md` line 52 (same — taker fee) | matched "5 bps" for taker | **NOT TOUCHED** — already correct. |
| `2026-04-26_phase-2l_R3_variant-comparison.md` line 47 (same — taker fee) | matched "5 bps" for taker | **NOT TOUCHED** — already correct. |
| `2026-04-27_phase-2v_R2_gate-1-execution-plan.md` line 70 (same — taker fee) | matched "5 bps" for taker | **NOT TOUCHED** — already correct. |

## 2. Files changed

| File | Diff |
|------|------|
| [docs/00-meta/implementation-reports/2026-04-26_phase-2l_R3_variant-comparison.md](2026-04-26_phase-2l_R3_variant-comparison.md) | 4 lines changed (line 331 header text; line 342 prose) |
| [docs/00-meta/implementation-reports/2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md](2026-04-27_phase-2m_R1a_on_R3_variant-comparison.md) | 4 lines changed (line 350 header text; line 361 prose) |
| [docs/00-meta/implementation-reports/2026-04-27_phase-2s_R1b-narrow_variant-comparison.md](2026-04-27_phase-2s_R1b-narrow_variant-comparison.md) | 2 lines changed (line 386 prose) |
| [docs/00-meta/implementation-reports/2026-04-27_phase-2x_family-review-memo.md](2026-04-27_phase-2x_family-review-memo.md) | 6 lines changed (line 151 table header alignment row; line 153 R3 row prose) |

**Diff stat:** 4 files changed, 8 insertions(+), 8 deletions(−). Net character change is small; the corrections are targeted phrase-level updates.

## 3. Exact stale phrases corrected

### 3.1 Phase 2l §8 header (line 331)

**Before:**

```text
GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. LOW = 0 bps; MEDIUM = 5 bps (baseline); HIGH = 15 bps (3x baseline).
```

**After:**

```text
GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. Per the canonical project config (`src/prometheus/research/backtest/config.py` `DEFAULT_SLIPPAGE_BPS`): LOW = 1.0 bps per side; MEDIUM = 3.0 bps per side (committed default); HIGH = 8.0 bps per side. The numerical run results in this section were computed using these canonical values. (The Phase 2l text originally described LOW = 0 / MEDIUM = 5 / HIGH = 15 bps; that was inline-description drift. Cleaned per the 2026-04-27 docs-only slippage-wording consistency cleanup; numerical results unchanged.)
```

### 3.2 Phase 2l §8 prose (line 342)

**Before:**

```text
Cost sensitivity is monotone and proportional. Even at HIGH (3x baseline) R3 does not cross the §10.4 hard-reject thresholds...
```

**After:**

```text
Cost sensitivity is monotone and proportional. Even at HIGH (8 bps per side; ~2.67× the committed MEDIUM) R3 does not cross the §10.4 hard-reject thresholds...
```

### 3.3 Phase 2m §10 header (line 350)

**Before:**

```text
GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. LOW = 0 bps; MEDIUM = 5 bps (baseline); HIGH = 15 bps (3× baseline). R1a+R3 on R-window:
```

**After:**

```text
GAP-20260424-032 carry-forward + Phase 2f §11.6 cost-sensitivity gate. Per the canonical project config (`src/prometheus/research/backtest/config.py` `DEFAULT_SLIPPAGE_BPS`): LOW = 1.0 bps per side; MEDIUM = 3.0 bps per side (committed default); HIGH = 8.0 bps per side. The numerical run results in this section were computed using these canonical values. (The Phase 2m text originally described LOW = 0 / MEDIUM = 5 / HIGH = 15 bps; that was inline-description drift carried forward from Phase 2l. Cleaned per the 2026-04-27 docs-only slippage-wording consistency cleanup; numerical results unchanged.) R1a+R3 on R-window:
```

### 3.4 Phase 2m §10 prose (line 361)

**Before:**

```text
Cost sensitivity is monotone and proportional. At HIGH (3× baseline) BTC expR drops to −0.544...
```

**After:**

```text
Cost sensitivity is monotone and proportional. At HIGH (8 bps per side; ~2.67× the committed MEDIUM) BTC expR drops to −0.544...
```

### 3.5 Phase 2s §10 prose (line 386)

**Before:**

```text
Cost sensitivity is monotone and proportional. At HIGH (3× baseline): BTC expR −0.389, ETH expR −0.371...
```

**After:**

```text
Cost sensitivity is monotone and proportional. At HIGH (8 bps per side; ~2.67× the committed MEDIUM): BTC expR −0.389, ETH expR −0.371...
```

### 3.6 Phase 2x §4.5 table header (line 151)

**Before:**

```text
| Candidate | LOW (0 bps) | MEDIUM (5 bps, committed) | HIGH (8 bps) | Cost-sensitivity profile |
```

**After:**

```text
| Candidate | LOW (1 bps per side) | MEDIUM (3 bps per side, committed) | HIGH (8 bps per side) | Cost-sensitivity profile |
```

The HIGH column was already correct at 8 bps. LOW and MEDIUM column labels updated.

### 3.7 Phase 2x §4.5 R3-row prose (line 153)

**Before:**

```text
Cost-robust. Even at HIGH (3× MED), R3 is still better than H0 at MED.
```

**After:**

```text
Cost-robust. Even at HIGH (~2.67× MED), R3 is still better than H0 at MED.
```

The other rows in the Phase 2x §4.5 table (R1a + R3, R1b-narrow, R2 + R3) did not contain the "3× MED" / "3× baseline" phrasing and were not edited.

## 4. Confirmation: no metrics, verdicts, thresholds, strategy parameters, code, or data changed

This cleanup is **strictly textual**. The following are explicitly preserved:

### 4.1 No metric / numerical-result changes

- All slippage sensitivity tables (Phase 2l §8, Phase 2m §10, Phase 2s §10, Phase 2x §4.5) contain unchanged trade counts, expR values, PF values, netPct values, maxDD values, and (for Phase 2x §4.5) the R3 / R1a+R3 / R1b-narrow / R2+R3 cost-sensitivity profile classifications. The numerical run results were always computed using the canonical config.py 1 / 3 / 8 bps tier values; only the inline textual descriptions of those tiers had drifted.

- All headline R-window and V-window comparison tables across Phase 2l / 2m / 2s / 2x — unchanged.

- All §10.3 / §10.4 / §11.3 / §11.4 / §11.6 verdict tables — unchanged.

### 4.2 No verdict changes

- Phase 2l R3: PROMOTE (§10.3.a + §10.3.c on both symbols) — unchanged.
- Phase 2m R1a+R3: PROMOTE (mixed-PROMOTE per Phase 2p §D framing) — unchanged.
- Phase 2s R1b-narrow: PROMOTE / PASS-with-caveats — unchanged.
- Phase 2w R2+R3: FAILED — §11.6 cost-sensitivity blocks — unchanged.
- Phase 2x §5 family-ceiling assessment ("V1 breakout family has likely reached its useful ceiling under the current framework") — unchanged.
- Phase 2y recommendation (§11.6 = 8 bps stays UNCHANGED) — unchanged.

### 4.3 No threshold changes

- §10.3 / §10.4 / §11.3 / §11.4 / §11.6 thresholds preserved per Phase 2f §11.3.5 (no post-hoc loosening).
- §11.6 HIGH = 8 bps per side preserved per Phase 2y primary recommendation.

### 4.4 No strategy-parameter changes

- R3 sub-parameters (`exit_kind=FIXED_R_TIME_STOP`, `exit_r_target=2.0`, `exit_time_stop_bars=8`) preserved.
- R1a sub-parameters (X = 25 percentile threshold, N = 200 trailing-bar lookback) preserved.
- R1b-narrow sub-parameter (S = 0.0020 magnitude threshold) preserved.
- R2 sub-parameters (8-bar validity window, setup_high/setup_low pullback level, close-not-violating-stop confirmation, next-bar-open after-confirmation fill model) preserved.
- H0 baseline parameters preserved.

### 4.5 No project-level lock changes

- §1.7.3 BTCUSDT-primary, ETHUSDT research/comparison only, one-symbol-only, one-position max, 0.25% risk per trade, 2× leverage cap, mark-price stops, v002 datasets — all preserved.

### 4.6 No code changes

- `src/`, `tests/`, `scripts/` untouched. Zero source files modified.
- `src/prometheus/research/backtest/config.py` `DEFAULT_SLIPPAGE_BPS` is the canonical source of truth and was NOT modified — this cleanup aligned old documentation TEXT to that canonical source, never the other direction.

### 4.7 No data changes

- `data/` untouched. No `data/` commits.
- v002 datasets untouched.

### 4.8 No reinterpretation of prior phase outcomes

- Phase 2y memo (which is the document that originally diagnosed this inconsistency) is **NOT modified** by this cleanup. Phase 2y §2.6's verbatim quote of the stale wording is preserved as the historical record of what was inconsistent at the time Phase 2y was written.
- Phase 2y §4.3 "(at 3× baseline as the Phase 2s text describes — though the canonical config.py 8 bps HIGH is closer to 2.7× the canonical 3 bps MED)" — preserved as Phase 2y's own self-aware diagnosis.

### 4.9 No reinterpretation of mechanism / cost-sensitivity readings

- The mechanism readings (M1 + M3 PASS for R2 on BTC; M2 FAIL on both) preserved.
- The cost-sensitivity profile classifications (R3 cost-robust; R1a+R3 cost-monotone; R1b-narrow cost-monotone; R2+R3 cost-fragile) preserved.
- The §11.6 gate definition unchanged.

## 5. Git status and commit hash

Pre-commit `git diff --stat` (after edits, before staging):

```text
4 files changed, 8 insertions(+), 8 deletions(-)
```

The commit and branch state are reported in the closing section of this file after the commit completes.

---

## 6. Closing summary

This cleanup brings four older Phase 2 reports' inline slippage-tier descriptions into agreement with the canonical project config. Six small textual edits across four files; ~16 lines of textual change; zero metric / verdict / threshold / parameter / code / data change. The Phase 2y memo's diagnosis of the inconsistency is preserved verbatim as the historical record of what was wrong before this cleanup happened.

**Phase 2y's conclusion is unchanged.** §11.6 = 8 bps HIGH stays. R2 stays FAILED. R3 remains baseline-of-record. H0 remains framework anchor. R1a / R1b-narrow / R2 remain retained as research evidence. No paper/shadow / Phase 4 / live-readiness / deployment authorized. All framework thresholds and §1.7.3 project-level locks preserved.

This cleanup is committed on `docs/slippage-wording-consistency` per operator brief; **not merged to main**; not pushed to origin (push not part of this task).
