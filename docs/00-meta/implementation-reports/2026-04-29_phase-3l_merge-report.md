# Phase 3l — Merge Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11; Phase 2i §1.7.3 project-level locks; Phase 2p §C.1 (R3 baseline-of-record); **Phase 2y slippage / cost-policy review (§11.6 = 8 bps HIGH preserved verbatim; framework-discipline anchor)**; Phase 3d-B2 F1 HARD REJECT; Phase 3j D1-A MECHANISM PASS / FRAMEWORK FAIL — other; Phase 3k post-D1-A research consolidation memo (remain-paused primary recommendation; external-cost-evidence review as conditional secondary alternative).

**Date:** 2026-04-29 UTC. **Merged into main.**

---

## 1. Phase 3l branch tip SHA before merge

```text
75ed18d0735a2b8e024627e6c526d11613508772
```

(Branch: `phase-3l/external-cost-evidence-review`; HEAD prior to merge after the closeout SHA fill-in + minimal current-project-state update cleanup commit.)

## 2. Merge commit hash

```text
dde1a495247583a1854ffc9ae114b2a424f17292
```

(Subject: `Merge Phase 3l (docs-only external execution-cost evidence review) into main`. Created via `git merge --no-ff phase-3l/external-cost-evidence-review`.)

## 3. Merge-report commit hash

```text
788833969ede8cabc11810fe7cdc11ec48194b3e  docs(phase-3l): merge report
                                          (initial commit of this merge-report file)
<filled by self-reference cleanup commit>  docs(phase-3l): record merge-report
                                           commit hash in section 3
                                           (clerical fill-in only)
```

(The §3 self-reference is filled in by an immediate follow-up clerical commit so the report records its own provenance. The cleanup commit's SHA is recorded in §6 latest commits below once it exists.)

## 4. Main / origin sync confirmation

After the final clerical cleanup commit and `git push origin main`:

```text
local  main:        <see latest commit in §6 below — the §3 self-reference cleanup commit>
remote origin/main: <same SHA>
```

Local `main` and `origin/main` are synced after every push step (initial merge `dde1a49`; merge-report commit `7888339`; this clerical §3 cleanup commit).

## 5. Git status

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

(Working tree clean after the §3 self-reference cleanup commit and push.)

## 6. Latest 5 commits

```text
<latest>  docs(phase-3l): record merge-report commit hash in section 3
7888339   docs(phase-3l): merge report
dde1a49   Merge Phase 3l (docs-only external execution-cost evidence review) into main
75ed18d   phase-3l: closeout SHA fill-in + minimal current-project-state update
f342dfb   phase-3l: docs-only external execution-cost evidence review
```

## 7. Files included in the merge

Phase 3l branch contributed exactly **3 files** (1 modified + 2 new) — zero source code; zero tests; zero scripts; zero `data/` artifacts:

```text
M  docs/00-meta/current-project-state.md
A  docs/00-meta/implementation-reports/2026-04-29_phase-3l_external-cost-evidence-review.md
A  docs/00-meta/implementation-reports/2026-04-29_phase-3l_closeout-report.md
```

Diff stat (branch → main pre-merge):

```text
3 files changed, 763 insertions(+), 1 deletion(-)
```

## 8. Phase 3l was docs-only

**Confirmed.** Phase 3l changed only Markdown documentation under `docs/00-meta/`:

- `docs/00-meta/current-project-state.md` (modified) — narrow Phase 3l record.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3l_external-cost-evidence-review.md` (new) — the Phase 3l cost-evidence review memo.
- `docs/00-meta/implementation-reports/2026-04-29_phase-3l_closeout-report.md` (new) — the Phase 3l closeout report.

Phase 3l did NOT: write source code; write tests; write scripts; run backtests; rerun R2 / F1 / D1-A / H0 / R3 / any controls; create variants; tune parameters; change thresholds (including §11.6); change strategy parameters; change project-level locks; revise prior verdicts; rescue R2 / F1 / D1-A; authorize D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid / ML feasibility / new strategy discovery / regime-first / 5m timeframe feasibility / formal cost-model revision; start paper/shadow planning; start Phase 4; start live-readiness or deployment work; enable MCP / Graphify / `.mcp.json`; request or use credentials; call authenticated/private Binance APIs; create or use production Binance keys; touch exchange-write paths; commit `data/` artifacts; or start any phase after Phase 3l.

## 9. current-project-state.md was updated narrowly

**Confirmed.** The update to `docs/00-meta/current-project-state.md` is intentionally narrow: a single-paragraph addition to the "Current Phase" subsection plus one line in the inline status box. The added paragraph records:

- Phase 3l completed docs-only external execution-cost evidence review (operator selected the Phase 3k secondary acceptable alternative).
- Primary assessment: **B — current cost model appears conservative but defensible.**
- §11.6 policy recommendation: **§11.6 remains unchanged pending stronger evidence.**
- No prior verdict revised; no backtests run; no threshold / strategy-parameter / project-lock changes.
- R2 / F1 / D1-A / R3 / H0 / R1a / R1b-narrow verdict statuses preserved verbatim.
- No formal cost-model revision, regime-first, 5m timeframe feasibility, ML feasibility, new strategy-family discovery, D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, exchange-write, or `data/` work started by Phase 3l.
- Recommended state remains **paused**.

The "Most recent merge" block, "Strategy Research Arc Outcomes" section, "Locked V1 Decisions", "Locked Architecture Direction", "Implementation Readiness Status", and all other canonical-state sections are **UNCHANGED**. The diff is 4 lines net (+1 paragraph + 1-line inline status box update; -1 line replaced inline status box).

## 10. Phase 3l primary assessment is B — current cost model appears conservative but defensible

**Confirmed.** Per the Phase 3l consolidation memo §11.1:

> **Primary assessment: B — Current cost model appears conservative but defensible.**
>
> Rationale: the committed `taker_fee_rate = 0.0005` matches the publicly-known VIP 0 USDⓈ-M Futures standard taker rate (0.05%) exactly; the model does NOT assume the operator pays in BNB (which would give ~10% off → effective ~0.045%); the model does NOT assume VIP-tier discounts. Slippage tiers 1/3/8 bps per side are plausible at order-of-magnitude level for BTCUSDT/ETHUSDT perpetual at Prometheus research notionals. MARK_PRICE stop-trigger matches Binance's public stop-order machinery and v1 protective-stop spec live-runtime intent. Funding modeling empirically validated by D1-A's M2 measurement (per-trade accrual on the order of 0.001–0.005 R, consistent with the 8-hour settlement cycle × locked sizing × realized funding-rate magnitudes). Tick / step / min-notional constraints are not material at locked research sizing.

A "B-shape" sub-finding is recorded in the Phase 3l memo: the slippage-tier calibration specifically rests on qualitative consensus rather than direct measurement; a future operator-authorized phase could pursue rigorous tick-level measurement (this is documented as evidence requirements, not as an authorized successor phase).

## 11. §11.6 remains unchanged pending stronger evidence

**Confirmed.** Per the Phase 3l consolidation memo §12.1:

> **Phase 3l recommends: KEEP §11.6 UNCHANGED PENDING STRONGER EVIDENCE.**
>
> No internal evidence supports revision (Phase 2y already established this); no external evidence obtained within Phase 3l directly contradicts the current §11.6 = 8 bps HIGH per side calibration; no external evidence directly supports relaxing or tightening §11.6. The §11.3.5 framework-discipline anchor (no post-hoc loosening) is preserved. The "pending stronger evidence" framing leaves the door open for a future operator-authorized cost-model revision phase if and when the operator independently judges that rigorous tick-level Binance-specific evidence-gathering is warranted. Phase 3l does NOT pre-authorize such a phase.

`DEFAULT_SLIPPAGE_BPS` map (LOW=1.0 / MED=3.0 / HIGH=8.0 per side) UNCHANGED. `taker_fee_rate=0.0005` UNCHANGED.

## 12. No prior verdict was changed

**Confirmed.** All prior framework verdicts are preserved verbatim:

- **R3 V1 breakout baseline-of-record** per Phase 2p §C.1 — UNCHANGED.
- **H0 V1 breakout framework anchor** per Phase 2i §1.7.3 — UNCHANGED.
- **R1a retained research evidence** per Phase 2p §D — UNCHANGED.
- **R1b-narrow retained research evidence** per Phase 2s §13 — UNCHANGED.
- **R2 FAILED — §11.6 cost-sensitivity blocks** per Phase 2w §16.1 — UNCHANGED.
- **F1 HARD REJECT** per Phase 3c §7.3 catastrophic-floor predicate — UNCHANGED.
- **D1-A MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2 — UNCHANGED.
- **Phase 3d-B2 terminal for F1** — UNCHANGED.
- **Phase 3j terminal for D1-A under current locked spec** — UNCHANGED.

Phase 3l explicitly affirms (per Phase 3l memo §13) that no candidate is re-classified, no backtest is rerun, and no candidate is rescued.

## 13. No backtests were run

**Confirmed.** No backtest engine invocation occurred during Phase 3l. No candidate cells were re-executed. No control reproduction was performed. No new run directories under `data/derived/backtests/` were created. The only data flow during Phase 3l was reading existing internal documentation (`docs/`) and `src/prometheus/research/backtest/config.py` for cost-model citation, plus public-Binance-page web fetches via the read-only WebFetch / WebSearch tools (no authenticated calls; no `data/` commits).

## 14. No formal cost-model revision, regime-first, 5m, ML, new strategy-family, D1-A-prime, D1-B, hybrid, implementation, backtesting, paper/shadow, Phase 4, live-readiness, deployment, MCP, Graphify, `.mcp.json`, credentials, exchange-write, threshold, strategy-parameter, project-lock, or `data/` work changed

**Confirmed.** Full preserved-scope table:

| Category | Status |
|----------|--------|
| Source code (`src/`) | UNCHANGED |
| Tests (`tests/`) | UNCHANGED |
| Scripts (`scripts/`) | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| §11.6 = 8 bps HIGH per side | UNCHANGED (Phase 3l recommends "Keep unchanged pending stronger evidence") |
| `DEFAULT_SLIPPAGE_BPS` map (LOW=1.0 / MED=3.0 / HIGH=8.0 per side) | UNCHANGED |
| `taker_fee_rate=0.0005` | UNCHANGED |
| §1.7.3 project-level locks | UNCHANGED |
| H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A spec axes | UNCHANGED |
| R3 baseline-of-record / H0 framework anchor | PRESERVED |
| R2 FAILED / F1 HARD REJECT / D1-A MECHANISM PASS / FRAMEWORK FAIL — other | PRESERVED |
| R1a / R1b-narrow / R2 / F1 / D1-A retained-research-evidence status | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Authenticated / private Binance API calls | NONE |
| Production Binance keys | NONE |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| `docs/05-backtesting-validation/cost-modeling.md` | UNCHANGED |
| `docs/05-backtesting-validation/backtesting-principles.md` | UNCHANGED |
| `src/prometheus/research/backtest/config.py` | UNCHANGED |
| **Formal cost-model revision memo** | **NOT AUTHORIZED, NOT PROPOSED** |
| **Regime-first research framework memo** | **NOT AUTHORIZED, NOT PROPOSED** |
| **5m timeframe feasibility memo** | **NOT AUTHORIZED, NOT PROPOSED** |
| **ML feasibility memo** | **NOT AUTHORIZED, NOT PROPOSED** |
| **New strategy-family discovery memo** | **NOT AUTHORIZED, NOT PROPOSED** |
| **D1-A-prime / D1-B / V1/D1 hybrid / F1/D1 hybrid spec** | **NOT AUTHORIZED, NOT PROPOSED** |

## 15. No next phase was started

**Confirmed.** No Phase 3m, no Phase 4, no formal cost-model revision phase, no regime-first phase, no 5m timeframe feasibility phase, no ML feasibility phase, no new strategy-family discovery phase, no D1-A-prime / D1-B / hybrid spec phase, no paper/shadow planning, no live-readiness, no deployment, no production-key, no exchange-write work was started. The project remains at the post-Phase-3l boundary; the operator decides whether and when any subsequent phase is authorized.

---

**End of Phase 3l merge report.** Phase 3l is the docs-only external execution-cost evidence review (operator selected the Phase 3k secondary acceptable alternative). Primary assessment: **B — current cost model appears conservative but defensible.** §11.6 policy recommendation: **§11.6 remains unchanged pending stronger evidence.** No prior verdict revised; no backtest rerun; no thresholds / strategy parameters / project locks / paper-shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credentials / authenticated-Binance-API / exchange-write change. R2 remains FAILED — §11.6 cost-sensitivity blocks; F1 remains HARD REJECT; D1-A remains MECHANISM PASS / FRAMEWORK FAIL — other; R3 remains V1 breakout baseline-of-record; H0 remains framework anchor. No next phase started. Merge into main (`dde1a49`) pushed to `origin/main`.
