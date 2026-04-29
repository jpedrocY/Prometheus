# Phase 3j — Merge Report

**Authority:** Phase 2f Gate 1 plan §§ 8–11; Phase 2i §1.7.3 project-level locks; Phase 2p §C.1; Phase 2y closeout (§11.6 = 8 bps HIGH preserved); Phase 3d-B2 precedent (F1 HARD REJECT); **Phase 3g D1-A spec memo + methodology audit (binding spec)**; **Phase 3h D1-A execution-planning memo (binding execution plan, with timing-clarification amendments)**; **Phase 3i-B1 engine wiring (binding implementation surface)**.

**Date:** 2026-04-29 UTC. **Merged into main.**

---

## 1. Phase 3j branch tip SHA before merge

```text
ee6856262fc9376cdae9301f99c5b56e1f60e75a
```

(Branch: `phase-3j/d1a-execution-diagnostics`; HEAD prior to merge after the report-cleanup commit.)

## 2. Merge commit hash

```text
5c8537bde462d328985b5c917729c663deaabc04
```

(Subject: `Merge Phase 3j (D1-A first execution + diagnostics + first-execution-gate eval) into main`. Created via `git merge --no-ff phase-3j/d1a-execution-diagnostics`.)

## 3. Merge-report commit hash

```text
5d18408daaed08ab30be47236f06c9d38c468f99
```

(Subject: `docs(phase-3j): merge report`. The merge-report file itself; this section was filled in by the immediate follow-up commit `<see §6 latest commits>` so the report records its own provenance.)

## 4. Main / origin sync confirmation

After `git push origin main`:

```text
local  main:        5c8537bde462d328985b5c917729c663deaabc04
remote origin/main: 5c8537bde462d328985b5c917729c663deaabc04
```

Local `main` and `origin/main` are synced.

## 5. Git status

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

(Working tree clean immediately prior to this merge-report commit; the report file itself is the next add+commit step which will update sections 3 + 6 to reference the merge-report commit hash.)

## 6. Latest 5 commits

```text
5c8537b Merge Phase 3j (D1-A first execution + diagnostics + first-execution-gate eval) into main
ee68562 phase-3j: report cleanup -- catastrophic-floor wording, M2 magnitude, long/short split, P.14 full table
c540dc4 phase-3j: D1-A first execution + diagnostics + first-execution-gate eval
564dfdb docs(phase-3i-B1): merge report
9a9764c Merge Phase 3i-B1 (D1-A engine wiring + lifecycle counters + runner scaffold) into main
```

## 7. Files included in the merge

Phase 3j branch contributed exactly **4 files** (1 modified, 3 new) — zero `data/` artifacts:

```text
M  scripts/phase3j_D1A_execution.py
A  scripts/_phase3j_D1A_analysis.py
A  docs/00-meta/implementation-reports/2026-04-29_phase-3j_D1A_execution-diagnostics.md
A  docs/00-meta/implementation-reports/2026-04-29_phase-3j_closeout-report.md
```

Diff stat (branch → main pre-merge):

```text
4 files changed, 1750 insertions(+), 90 deletions(-)
```

## 8. Phase 3j was the first real D1-A candidate-execution phase

**Confirmed.** Phase 3i-A (implementation controls) and Phase 3i-B1 (engine wiring + runner scaffold) consumed the Phase 3g binding spec without running any real-data D1-A backtest; the Phase 3i-B1 runner scaffold was double-gated (`--phase-3j-authorized` flag required AND the run-loop body raised "not yet implemented"). Phase 3j is the FIRST phase to:

- implement the runner-loop body (`scripts/phase3j_D1A_execution.py`),
- execute D1-A on real BTCUSDT / ETHUSDT v002 datasets,
- evaluate the Phase 3h §11 first-execution gate,
- compute the Phase 3h §12 M1 / M2 / M3 mechanism checks on real data,
- gather the Phase 3h §13 mandatory diagnostics,
- validate the Phase 3h §14 P.14 hard-block invariants surface.

## 9. D1-A R-window mandatory inventory was executed

**Confirmed.** All 4 mandatory cells per Phase 3h §10 inventory:

| Cell | BTC trades | BTC expR / PF | ETH trades | ETH expR / PF |
|------|----------:|-------------:|----------:|-------------:|
| **R MED MARK** | 198 | −0.3217 / 0.6467 | 179 | −0.1449 / 0.8297 |
| R LOW MARK | 198 | −0.2423 / 0.7248 | 180 | −0.1168 / 0.8609 |
| **R HIGH MARK** | 197 | −0.4755 / 0.5145 | 178 | −0.2543 / 0.7217 |
| R MED TRADE_PRICE | 198 | −0.3703 / 0.6014 | 180 | −0.2222 / 0.7478 |

Run directories (under git-ignored `data/derived/backtests/`):

- `phase-3j-d1a-window=r-slip=medium/2026-04-29T03-22-26Z`
- `phase-3j-d1a-window=r-slip=low/2026-04-29T03-23-02Z`
- `phase-3j-d1a-window=r-slip=high/2026-04-29T03-23-34Z`
- `phase-3j-d1a-window=r-slip=medium-stop=trade_price/2026-04-29T03-24-06Z`

## 10. D1-A V MED MARK was NOT executed

**Confirmed.** The Phase 3h §10.5 + Phase 3j brief require V-window cell execution to be conditional on R-window verdict = PROMOTE. The R-window verdict is **MECHANISM PASS / FRAMEWORK FAIL — other** — not PROMOTE. No V-window run directory was created (`data/derived/backtests/phase-3j-d1a-window=v-*` does not exist).

## 11. No forbidden runs were executed

**Confirmed.** Phase 3j executed only the 4 mandatory D1-A R-window cells listed above plus the 5 control reproductions (H0 R/V × MED MARK; R3 R/V × MED MARK; F1 R × MED MARK; each producing BTC + ETH outputs = 10 symbol-level cells). No D1-A-prime, D1-B, V1/D1 hybrid, F1/D1 hybrid, alternative-axes, alternative-window, alternative-symbol, or sweep cell was executed. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP run was executed.

## 12. Phase 3j verdict

**Confirmed: MECHANISM PASS / FRAMEWORK FAIL — other** per Phase 3h §11.2 mapping. Driven by:

- Condition (i) `BTC MED expR > 0` — **FAIL** (BTC R MED MARK expR = −0.3217).
- Condition (ii) `M1 BTC h=32 PASS` — **PASS** (mean +0.1748R; fraction-non-negative 0.5101).
- Condition (iii) `ETH MED non-catastrophic` — **PASS** (expR −0.1449; PF 0.8297).
- Condition (iv) `BTC HIGH cost-resilience` — **FAIL** (BTC HIGH expR = −0.4755 < 0).
- Condition (v) `MED absolute floors` — **PASS** (both symbols).
- Catastrophic-floor predicate — **No violation** on any of 4 cells.

Verdict mapping:

```text
catastrophic_floor:  False  →  not HARD REJECT
condition (ii) M1:   PASS   →  not MECHANISM FAIL
condition (i):       FAIL          →  not PROMOTE
condition (iv):      FAIL          →  cost-resilience also blocks
                                  →  MECHANISM PASS / FRAMEWORK FAIL — other
```

## 13. No catastrophic-floor violation

**Confirmed.** A cell is non-catastrophic iff `expR > −0.50 AND PF > 0.30` (both conditions); equivalently the catastrophic-floor predicate triggers iff `expR ≤ −0.50 OR PF ≤ 0.30`. All 4 BTC/ETH × MED/HIGH MARK cells satisfy the non-catastrophic conjunction:

| Cell | expR | PF | expR > −0.50? | PF > 0.30? | Non-catastrophic |
|------|-----:|---:|--------------:|-----------:|-----------------:|
| BTC R MED MARK | −0.3217 | 0.6467 | Yes | Yes | **Yes** |
| ETH R MED MARK | −0.1449 | 0.8297 | Yes | Yes | **Yes** |
| BTC R HIGH MARK | −0.4755 | 0.5145 | Yes | Yes | **Yes** |
| ETH R HIGH MARK | −0.2543 | 0.7217 | Yes | Yes | **Yes** |

This is materially milder than Phase 3d-B2 F1 (which tripped 5 catastrophic-floor violations and produced a HARD REJECT verdict).

## 14. M1 PASS, M2 FAIL, M3 PASS-isolated

**Confirmed.**

- **M1 (post-entry counter-displacement at h=32 R, BTC drives §11.1 (ii)):** mean +0.1748R, fraction-non-negative 0.5101 — both above the §11.1 (ii) thresholds of mean ≥ +0.10R AND fraction ≥ 0.50. **PASS**.
- **M2 (funding-cost benefit, mean funding_pnl / realized_risk_usdt):** BTC +0.00234R (~21× below the +0.05R PASS threshold); ETH +0.00452R (~11× below). **FAIL on both symbols**.
- **M3 (TARGET-exit subset, mean R + aggregate R per symbol):** BTC n=52, mean +2.143R, aggregate +111.46R; ETH n=49, mean +2.447R, aggregate +119.89R. Both above thresholds (mean ≥ +0.30R AND aggregate > 0). **PASS-isolated** — descriptive only per Phase 3h §12.3 framing; cannot rescue framework-fail outcome.

## 15. D1-A retained as research evidence only and non-leading

**Confirmed.** Per Phase 3h §11 / §15 framework:

- D1-A is **retained as research evidence**, analogous to R1a / R1b-narrow / R2 / F1.
- D1-A is **non-leading**. R3 remains the V1 baseline-of-record (Phase 2p §C.1). H0 remains the framework anchor (Phase 2i §1.7.3).
- D1-A's locked spec values (Phase 3g binding) are preserved verbatim in `FundingAwareConfig` and consumed unmodified by the engine; no axis was modified by Phase 3j.

## 16. Phase 3j is terminal for D1-A under the current locked spec

**Confirmed.** Under the current locked Phase 3g D1-A spec axes (|Z_F| ≥ 2.0 over trailing 90 days / 270 events; current event excluded from rolling mean/std; 1.0 × ATR(20) stop; +2.0R TARGET; 32-bar TIME_STOP; per-funding-event cooldown; band [0.60, 1.80] × ATR(20); contrarian direction; no regime filter), Phase 3j's MECHANISM PASS / FRAMEWORK FAIL — other verdict is the binding decision. No further D1-A backtest cells are authorized; no V-window / alternative-cost / alternative-axes runs are authorized.

## 17. No D1-A-prime, D1-B, V1/D1 hybrid, or F1/D1 hybrid is authorized

**Confirmed.** Per Phase 3h §15 governance:

- **No D1-A-prime** (modified Z threshold / lookback / stop / target / time-stop / cooldown / direction / regime filter) authorized.
- **No D1-B** (alternative funding-aware family) authorized.
- **No V1/D1 hybrid** (D1-A entries combined with V1 trend filter, V1 sizing, V1 regime gating) authorized.
- **No F1/D1 hybrid** (D1-A entries combined with F1 mean-reversion overextension primitives) authorized.

Any successor variant requires a separately authorized phase per Phase 3h §15 + the AI coding handoff phase-gate governance.

## 18. No `data/` artifacts were committed

**Confirmed.** Phase 3j branch contains exactly 4 non-`data/` files (3 new + 1 modified). All Phase 3j candidate runs + control reproductions wrote outputs under git-ignored `data/derived/backtests/` directories, which `git status` reports as clean (covered by the existing `.gitignore` for `data/derived/`). No `data/` entry appears in `git log -1 --stat` for any Phase 3j commit (`c540dc4`, `ee68562`, `5c8537b`).

## 19. No thresholds, strategy parameters, project locks, or live-readiness work changed

**Confirmed.**

| Category | Status |
|----------|--------|
| Phase 2f thresholds (§10.3 / §10.4 / §11.3 / §11.4) | UNCHANGED |
| §11.6 = 8 bps HIGH per side (Phase 2y closeout) | UNCHANGED |
| §1.7.3 project-level locks | UNCHANGED |
| H0 / R3 / R1a / R1b-narrow / R2 / F1 spec axes | UNCHANGED |
| **D1-A locked spec values** (Phase 3g binding) | **PRESERVED VERBATIM** |
| R3 baseline-of-record / H0 framework anchor | PRESERVED |
| F1 framework verdict (HARD REJECT, Phase 3d-B2 terminal) | PRESERVED |
| Paper/shadow planning | NOT AUTHORIZED, NOT PROPOSED |
| Phase 4 (runtime / state / persistence) work | NOT AUTHORIZED, NOT PROPOSED |
| Live-readiness / deployment / production-key / exchange-write work | NOT AUTHORIZED, NOT PROPOSED |
| MCP servers / Graphify / `.mcp.json` | NOT ACTIVATED, NOT TOUCHED |
| Credentials / `.env` / API keys | NOT REQUESTED, NOT CREATED, NOT TOUCHED |
| Existing strategy / validation / cost / data / phase-gate / ai-coding-handoff specs | UNCHANGED |
| `docs/12-roadmap/technical-debt-register.md` | UNCHANGED |
| `docs/00-meta/implementation-ambiguity-log.md` | UNCHANGED |
| `docs/00-meta/current-project-state.md` | UNCHANGED (will be updated post-Phase-3k by an authorized post-Phase-3j consolidation memo, when authorized) |
| `docs/00-meta/ai-coding-handoff.md` | UNCHANGED |
| `data/` directory | UNCHANGED, NO COMMITS |

## 20. No next phase was started

**Confirmed.** Phase 3k is **NOT started**. No paper/shadow / Phase 4 / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials / threshold / strategy-parameter / project-lock / spec-axis change occurred. The recommended next step per Phase 3h §15 framework is **operator-driven post-Phase-3j consolidation** (a docs-only memo analogous to Phase 3e's post-F1 consolidation, summarizing the V1 + F1 + D1-A research arc, recording the framework-fail outcomes, and deferring the next-phase decision to the operator). Phase 3j does NOT author this memo — it is reserved for an authorized Phase 3k or equivalent.

---

## Quality-gate confirmations

All 4 gates were green at the Phase 3j branch tip prior to merge:

| Gate | Result |
|------|--------|
| `uv run pytest` | **668 passed** in 12.10s |
| `uv run ruff check .` | **All checks passed!** |
| `uv run ruff format --check .` | **157 files already formatted** |
| `uv run mypy src` | **Success: no issues found in 61 source files** |

Full control set (5 named controls / 10 symbol-level cells) reproduced bit-for-bit:

| Control | Symbols | Reproduces |
|---------|---------|-----------|
| H0 R MED MARK | BTC + ETH | **identical** (n=33 each) |
| H0 V MED MARK | BTC + ETH | **identical** (n=8 / 14) |
| R3 R MED MARK | BTC + ETH | **identical** (n=33 each) |
| R3 V MED MARK | BTC + ETH | **identical** (n=8 / 14) |
| F1 R MED MARK | BTC + ETH | **identical** (n=4720 / 4826) |

(Bit-for-bit on summary metrics + trade-log content; the only differences are in random `trade_id` UUID suffix and NaN-equality semantics, both expected and not economic-content differences.)

---

**End of Phase 3j merge report.** Phase 3j was the first real D1-A candidate-execution phase. R-window mandatory inventory (4 cells) executed; V MED MARK NOT executed (verdict not PROMOTE); no forbidden runs. Verdict: MECHANISM PASS / FRAMEWORK FAIL — other. M1 PASS, M2 FAIL, M3 PASS-isolated. No catastrophic-floor violation. D1-A retained as research evidence only; non-leading; Phase 3j terminal for D1-A under current locked spec; no D1-A-prime / D1-B / V1/D1 / F1/D1 hybrid authorized. No `data/` artifacts committed. No thresholds / strategy parameters / project locks / paper/shadow / Phase 4 / live-readiness / deployment / MCP / Graphify / `.mcp.json` / credentials / exchange-write change. No next phase started. Merge into main (`5c8537b`) pushed to `origin/main`.
