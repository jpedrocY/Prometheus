# Phase 4f Closeout

## Summary

Phase 4f — **External Strategy Research Landscape and V2 Hypothesis Candidate Memo** (docs-only) — is committed on branch `phase-4f/external-strategy-research-landscape-v2-candidates` and pushed to `origin/phase-4f/external-strategy-research-landscape-v2-candidates`. The memo surveys high-quality academic and practitioner evidence on systematic trading strategies, evaluates institutional-trading transferability to a single-symbol, fake-adapter-only, supervised v1 project, and predeclares one bounded V2 candidate hypothesis family — *V2 — Participation-Confirmed Trend Continuation* — together with a bounded predeclared feature list (≤8 entry features, ≤3 exit/regime features), a bounded predeclared timeframe matrix (15m/30m/1h signal; 1h/4h bias; 5m diagnostic-only), predeclared exclusion rules, and predeclared validation requirements.

**Phase 4f does NOT backtest. Phase 4f does NOT implement. Phase 4f does NOT download data. Phase 4f does NOT create a strategy variant. Phase 4f does NOT revise any previous verdict. Phase 4f does NOT claim profitability. Phase 4f does NOT authorize paper/shadow/live/exchange-write.**

**Recommendation:** Option B (docs-only V2 strategy-spec memo for Participation-Confirmed Trend Continuation) primary; Option C (docs-only V2 data-requirements and feasibility memo) conditional secondary; Option A (remain paused) procedurally acceptable but understates operator-stated motivation; Options D / E (data acquisition or backtest before predeclaration) NOT recommended; Option F (paper/shadow / live-readiness / exchange-write) FORBIDDEN.

**Verification:**

- `git status`: clean.
- `python --version`: Python 3.12.4.
- `ruff check .`: **All checks passed!**
- `pytest`: **785 passed in 15.54s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

**No retained-evidence verdict revised.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. **No policy locks changed.** Phase 4a public API and runtime behavior preserved. Phase 4e reconciliation-model design preserved.

**No code, tests, scripts, data, manifests modified by Phase 4f.** No diagnostics rerun. No Q1–Q7 rerun. No backtests. No data acquisition / patching / regeneration / modification. **`scripts/phase3q_5m_acquisition.py` not run.** **`scripts/phase3s_5m_diagnostics.py` not run.** No paper/shadow / live-readiness / deployment / production-key / exchange-write / MCP / Graphify / `.mcp.json` / credentials work. No private endpoints / user stream / WebSocket / public endpoints consulted in code. No secrets requested or stored. **Recommended state remains paused.** **No successor phase has been authorized.**

## Files changed

The Phase 4f report commit (`4f5d12b97e0127daaef6bea7e96db322fb98d053`) consists of 1 new file:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4f_external-strategy-research-landscape-v2-candidates.md` — Phase 4f research memo (680 lines; 34 sections).

The Phase 4f closeout commit adds 1 new file:

- `docs/00-meta/implementation-reports/2026-04-30_phase-4f_closeout.md` — this closeout artefact.

**NOT modified:**

- All `src/prometheus/**` — Phase 4a / 4c runtime code preserved verbatim.
- All `tests/**`.
- All `scripts/**` — Phase 4b cleanup deliverables preserved verbatim.
- All `data/**` and `data/manifests/**`.
- All `docs/**` other than the two new Phase 4f artefacts.
- All `.claude/rules/**`.
- `pyproject.toml`.
- `.gitignore`.
- `.mcp.json`.
- `uv.lock`.
- `docs/00-meta/current-project-state.md` (preferred update only after merge per the Phase 4f brief).
- All Phase 3o / 3p / 3q / 3r / 3s / 3t / 3u / 3v / 3w / 3x / 4a / 4b / 4c / 4d / 4e reports / closeouts / merge-closeouts.

## Research conclusion

Phase 4f's research memo writes the following conclusions into the project record:

- **Time-series momentum / trend-following is the strongest and most-replicated systematic-trading evidence base** ([Moskowitz, Ooi, Pedersen 2012](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2089463); [Hurst, Ooi, Pedersen 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2993026); [Brock, Lakonishok, LeBaron 1992](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1992.tb04681.x); [Liu, Tsyvinski 2018/2021 NBER WP 24877](https://www.nber.org/papers/w24877)). The signal mechanic is reproducible on a single asset; the institutional diversification advantage is forfeit for v1.
- **Volume / order-flow imbalance has documented predictive content** ([Easley, O'Hara, Yang, Zhang 2024](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4814346)) — strongest as *confirmation* on price-based signals, weaker as standalone signal.
- **Crypto derivatives-flow indicators are best used as regime / cost / context lenses, not standalone entry signals** (BIS WP 1087; OI / funding-rate / long-short-ratio research). Funding-rate percentile and OI-delta have informative content; long/short ratio is weak-medium; liquidation cascades are a regime, not an exploitable mispricing.
- **Bitcoin intraday seasonality is real and exploitable as a cost-aware timing feature** (Hattori 2024 — UK tea time peak; Eross/Urquhart/Wolfe 2019 — time-of-day periodicities). Phase 4f treats UTC hour bucketing as a *cost-aware* feature rather than a primary signal.
- **5m timeframe is excluded as a primary signal timeframe** per Phase 3o §6 / Phase 3p §8 / Phase 3t closure. 5m is acceptable only as a timing diagnostic.
- **Backtest overfitting is the dominant risk for any V2 candidate** (Bailey, Borwein, López de Prado, Zhu 2014). Mitigations: predeclaration of bounded feature list and threshold grids; combinatorially symmetric cross-validation (CSCV); deflated Sharpe; chronological holdout; multi-symbol cross-check.
- **Institutional infrastructure-dependent strategies are NOT transferable** — HFT market making, latency-dependent strategies, ML-first black-box forecasting, multi-venue arbitrage, cross-sectional / multi-asset diversification, and authenticated-data-feed strategies are all out of scope.
- **No prior verdict revised.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim. V2 is a new ex-ante hypothesis, NOT a rescue.

## V2 candidate hypothesis family

Phase 4f predeclares one bounded V2 candidate hypothesis family:

**Name:** V2 — Participation-Confirmed Trend Continuation.

**Status:** pre-research hypothesis only; not implemented, not backtested, not validated, not live-ready, not a rescue of any failed strategy.

**Core premise:** Trade trend-continuation / breakout events on BTCUSDT perpetual *only when four conditions align simultaneously*:

1. **Price structure** signals trend-continuation (Donchian breakout from recent compression with confirming HTF trend bias).
2. **Volatility regime** is in a *post-compression / expansion-friendly* state (ATR percentile within a predeclared band).
3. **Participation / volume** confirms the breakout (relative volume / volume z-score / taker-imbalance above predeclared thresholds at the breakout bar).
4. **Derivatives-flow context** is non-pathological (funding-rate percentile inside a predeclared "neither extreme-overheated nor extreme-fearful" band; OI-delta consistent with new positioning rather than late-cycle blow-off).

**Risk and exit framing:** structural stop + ATR buffer (mark-price-runtime domain per Phase 3v §8.4); locked v1 sizing constants (0.25% risk, 2× leverage cap, internal notional cap); Fixed-R + unconditional time-stop (R3 baseline-of-record exit family preserved as canonical baseline); long and short symmetric; predeclared post-trade cooldown.

**What V2 is NOT:** NOT a 5m strategy; NOT a contrarian / mean-reversion overlay; NOT a hybrid of any retained-evidence strategy; NOT a parameter-optimized version of R3 / R2 / F1 / D1-A; NOT an ML-first model; NOT a market-making / HFT / latency-dependent design; NOT a basis / carry / spot-perpetual-arbitrage strategy; NOT a paper/shadow / live-readiness evidence claim.

**Predeclared feature candidates (§23):** Price/trend (1h or 4h return state; Donchian trend state; EMA slope or separation; HH/HL structure); Breakout/compression (Donchian width %ile; ATR %ile; breakout close location; range-expansion ratio); Volume/participation (relative volume; volume z-score; volume %ile by UTC hour; breakout-bar volume expansion); Derivatives flow (OI delta; taker buy/sell imbalance; funding-rate %ile; long/short ratio; mark-vs-trade divergence); Timing (UTC hour bucket; high-volume session bucket; funding-window proximity); Risk quality (stop distance / ATR; expected fee burden; slippage sensitivity). **Bound:** maximum of 8 active entry features, 3 active exit/regime features, predeclared before any backtest.

**Predeclared timeframe candidates (§24):** Signal 15m/30m/1h; Bias 1h/4h; Session bucket 30m/1h; Daily optional broad context; **5m diagnostic-only, NOT primary signal.**

**Predeclared exclusion rules (§25):** No 5m-only scalping; no private/authenticated data; no HFT/market making; no post-hoc rescue; no thresholds chosen after looking at outcomes; no more than the bounded feature set; no unbounded parameter search; no strategy promotion without chronological validation and cost sensitivity; no live or paper implications.

**Predeclared validation requirements (§26):** Predeclaration evidence; no look-ahead; chronological holdout; §11.6 cost-sensitivity gate at HIGH (8 bps per side) on both BTCUSDT and ETHUSDT; catastrophic-floor predicate; multi-symbol confirmation; multi-window OOS testing; deflated Sharpe per Bailey & López de Prado; M1 / M2 / M3 mechanism check; explicit `stop_trigger_domain` labeling per Phase 3v §8; explicit `break_even_rule` / `ema_slope_method` / `stagnation_window_role` declarations per Phase 3w §6/§7/§8.

## Candidate next-slice decision

Phase 4f ranks six candidate next moves and records the following decision:

- **Option A — Remain paused.** Procedurally acceptable but understates the operator-stated motivation. NOT recommended as the primary move.
- **Option B — Docs-only V2 strategy-spec memo for "Participation-Confirmed Trend Continuation".** **Primary recommendation.** A Phase-4g-style docs-only memo that operationalizes the §22 hypothesis: chooses one signal timeframe; chooses one bias timeframe; selects ≤8 active entry features and ≤3 active exit/regime features; specifies predeclared threshold grids; specifies the M1 / M2 / M3 mechanism-check decomposition; specifies validation requirements; explicitly declares all four governance labels per Phase 3v + Phase 3w. The strategy spec would NOT authorize backtest or implementation; that is a separate operator decision.
- **Option C — Docs-only V2 data-requirements and feasibility memo.** **Conditional secondary.** Operationalizes §21: enumerates exact bulk-archive datasets needed (`metrics` history; `aggTrades` history; etc.); specifies SHA256-verified acquisition plan analogous to Phase 3q; specifies dataset-versioning convention (e.g., `binance_usdm_btcusdt_metrics__v001`); specifies integrity-check rules; predeclares `research_eligible` semantics. The data-requirements memo would NOT authorize acquisition; that is a separate operator decision.
- **Option D — Acquire data immediately.** NOT recommended. Forbidden until a docs-only data-requirements memo predeclares what is needed and why.
- **Option E — Run exploratory backtests immediately.** REJECTED. Backtesting before predeclaration is the data-snooping pattern Bailey et al. 2014 document as the leading cause of out-of-sample failure.
- **Option F — Paper / shadow / live-readiness / exchange-write.** FORBIDDEN.

The natural ordering depends on operator preference: Option B → C means "design first, then check feasibility"; Option C → B means "verify data availability first, then design against what exists." Either order is acceptable.

## Commands run

All commands run from `c:\Prometheus` against the project's `.venv` (Python 3.12.4):

```text
git status
git rev-parse HEAD
git rev-parse origin/main
git checkout -b phase-4f/external-strategy-research-landscape-v2-candidates
.venv/Scripts/python --version
.venv/Scripts/python -m ruff check .
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m pytest
.venv/Scripts/python -m mypy
git add docs/00-meta/implementation-reports/2026-04-30_phase-4f_external-strategy-research-landscape-v2-candidates.md
git commit -m "phase-4f: external strategy research landscape and V2 hypothesis candidate memo (docs-only)"
git push -u origin phase-4f/external-strategy-research-landscape-v2-candidates
```

External web research used the WebSearch tool only; no WebFetch was invoked. Web research was conducted against public web pages (academic paper search results, exchange documentation summary results, BIS / NBER / SSRN / arXiv search results). No data was acquired / downloaded. No script was run. No diagnostics. No backtests. No network I/O via project code.

## Verification results

- `git status`: clean (before commit / after commit).
- `python --version`: Python 3.12.4.
- `ruff check .`: **All checks passed!** Whole-repo Ruff quality gate is fully clean.
- `pytest`: **785 passed in 15.54s.** No regressions.
- `mypy` strict: **Success: no issues found in 82 source files.**

## Commit

| Commit | Subject |
|---|---|
| `4f5d12b97e0127daaef6bea7e96db322fb98d053` | `phase-4f: external strategy research landscape and V2 hypothesis candidate memo (docs-only)` — Phase 4f research memo (680 lines). |
| _(this commit)_ | `docs(phase-4f): closeout report (Markdown artefact)` — Phase 4f closeout. |

Both commits are on branch `phase-4f/external-strategy-research-landscape-v2-candidates`. Branch pushed to `origin/phase-4f/external-strategy-research-landscape-v2-candidates`. Per prior phase pattern, this closeout file's own SHA cannot be embedded in itself; the inherent self-reference limit is acknowledged. The closeout commit's SHA is reported in the chat closeout block accompanying this commit.

## Final git status

```text
clean
```

Working tree empty after both commits on the Phase 4f branch.

## Final git log --oneline -5

Snapshot at the closeout commit (the topmost SHA is reported in the chat closeout):

```text
<recorded after this closeout commit itself is committed>  docs(phase-4f): closeout report (Markdown artefact)
4f5d12b  phase-4f: external strategy research landscape and V2 hypothesis candidate memo (docs-only)
da0f7c4  docs(phase-4e): merge closeout + current-project-state sync
eeaf72d  Merge Phase 4e (reconciliation-model design memo, docs-only) into main
d5a3616  docs(phase-4e): closeout report (Markdown artefact)
```

## Final rev-parse

- **`git rev-parse HEAD`** (on `phase-4f/external-strategy-research-landscape-v2-candidates`): the closeout commit's SHA, reported in the chat closeout block accompanying this commit.
- **`git rev-parse phase-4f/external-strategy-research-landscape-v2-candidates`**: same as `HEAD`.
- **`git rev-parse origin/phase-4f/external-strategy-research-landscape-v2-candidates`**: same as `HEAD` (after push).
- **`git rev-parse main`**: `da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c` (unchanged from pre-Phase-4f).
- **`git rev-parse origin/main`**: `da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c` (unchanged).
- **`git rev-parse phase-4e/reconciliation-model-design-memo`**: `d5a3616979bcb1b7ca71298da2af4207bebfff15` (preserved).
- **`git rev-parse phase-4d/runtime-foundation-review-and-next-slice-decision`**: `f7eb19b0ae72657364fa340a7fef3148e1a4d405` (preserved).
- **`git rev-parse phase-4c/state-package-ruff-residual-cleanup`**: `52e6127ecb0dbb999cf2307b5d2a173c897bae24` (preserved).
- **`git rev-parse phase-4b/repository-quality-gate-restoration`**: `1c6d36bfbb0bd869325b4cd773a1d25584bdbcce` (preserved).
- **`git rev-parse phase-4a/local-safe-runtime-foundation`**: `9c10dbd4e80e7daa60ffd77c1830d51d4776b345` (preserved).

## Branch / main status

- **`phase-4f/external-strategy-research-landscape-v2-candidates`** — pushed to `origin/phase-4f/external-strategy-research-landscape-v2-candidates`. Two commits on the branch: the Phase 4f research memo (`4f5d12b9`) and this closeout (SHA reported in chat). Branch NOT merged to `main`.
- **`main`** — unchanged at `da0f7c428ec8da0a4fb9eaf4e7bb96e726f52d9c`. Local `main` = `origin/main` = `da0f7c42`.
- **No merge to main.** Per the Phase 4f brief: *"Do not merge to main unless explicitly instructed."*

## Forbidden-work confirmation

- **No Phase 4 canonical / Phase 4g / successor phase started.** No subsequent phase has been authorized, scoped, briefed, branched, or commenced.
- **No V2 implementation.**
- **No V2 backtest.**
- **No V2 strategy-spec memo (this memo is a hypothesis-candidate memo, not a strategy spec).**
- **No data acquired.** No `data/` artefact modified. No public Binance endpoint consulted in code.
- **No implementation code written.** Phase 4f is text-only.
- **No real exchange adapter implemented.**
- **No exchange-write capability.**
- **No order placement / cancellation.**
- **No Binance credentials used.** No request, no storage, no `.env` modification.
- **No authenticated REST / private endpoint / public endpoint / user-stream / WebSocket calls.** Phase 4f performs no network I/O via project code; web research used WebSearch tool only.
- **No production alerting / Telegram / n8n production routes.**
- **No MCP enabling / Graphify enabling / `.mcp.json` modification.**
- **No `.env` file creation.**
- **No credential handling modification.**
- **No deployment artefact created.**
- **No paper/shadow runtime created.**
- **No live-readiness implication.**
- **No V1 / R3 / R2 / F1 / D1-A / other strategy implementation.**
- **No strategy rescue proposal.** V2 is a NEW ex-ante hypothesis, NOT a re-parameterized successor.
- **No 5m strategy / hybrid / retained-evidence successor / new variant created.**
- **No diagnostics run.** No Phase 3o / 3p Q1–Q7 question rerun.
- **No backtests run.**
- **`scripts/phase3q_5m_acquisition.py` not run.**
- **`scripts/phase3s_5m_diagnostics.py` not run.**
- **No data acquisition / download / patch / regeneration / modification.** No `data/` artefact modified.
- **No data manifest modification.** All `data/manifests/*.manifest.json` preserved verbatim.
- **No v002 dataset / manifest modification.**
- **No Phase 3q v001-of-5m manifest modification.**
- **No v003 created.**
- **No verdict revision.** R3 / H0 / R1a / R1b-narrow / R2 / F1 / D1-A all preserved verbatim.
- **No threshold / parameter / project-lock modifications.**
- **No Phase 3v stop-trigger-domain governance modification.**
- **No Phase 3w break-even / EMA slope / stagnation governance modification.**
- **No `docs/03-strategy-research/v1-breakout-strategy-spec.md` substantive change.**
- **No `docs/03-strategy-research/v1-breakout-backtest-plan.md` substantive change.**
- **No `docs/05-backtesting-validation/v1-breakout-validation-checklist.md` substantive change.**
- **No `docs/07-risk/stop-loss-policy.md` substantive change.**
- **No `docs/06-execution-exchange/binance-usdm-order-model.md` substantive change.**
- **No `docs/12-roadmap/phase-gates.md` substantive change.**
- **No `docs/12-roadmap/technical-debt-register.md` substantive change.**
- **No `docs/00-meta/ai-coding-handoff.md` substantive change.**
- **No `docs/09-operations/first-run-setup-checklist.md` substantive change.**
- **No `docs/00-meta/implementation-ambiguity-log.md` modification.**
- **No `docs/00-meta/current-project-state.md` modification on the Phase 4f branch.**
- **No `.claude/rules/**` modification.**
- **No `pyproject.toml` modification.**
- **No `.gitignore` modification.**
- **No `.mcp.json` modification.**
- **No `uv.lock` modification.**
- **No `src/prometheus/**` modification.**
- **No `tests/**` modification.**
- **No `scripts/**` modification.**
- **No merge to main.**
- **No successor phase started.**

## Remaining boundary

- **Recommended state:** **paused.**
- **Phase 4f output:** docs-only research memo + closeout artefact on the Phase 4f branch.
- **Repository quality gate state:** **fully clean.** Whole-repo `ruff check .` passes; pytest 785 passed; mypy strict 0 issues across 82 source files.
- **5m research thread state:** Operationally complete and closed (Phase 3t).
- **Implementation-readiness boundary:** Reviewed (Phase 3u). Phase 4 (canonical) remains not authorized. Phase 4a executed and merged. Phase 4b/4c quality cleanups merged. Phase 4d review merged. Phase 4e reconciliation-model design merged. Phase 4f research memo on this branch.
- **Stop-trigger domain governance:** RESOLVED by Phase 3v §8 + enforced in code by Phase 4a (preserved by 4b / 4c / 4d / 4e / 4f).
- **Break-even rule governance:** RESOLVED by Phase 3w §6 + enforced in code by Phase 4a (preserved).
- **EMA slope method governance:** RESOLVED by Phase 3w §7 + enforced in code by Phase 4a (preserved).
- **Stagnation window role governance:** RESOLVED by Phase 3w §8 + enforced in code by Phase 4a (preserved).
- **Reconciliation governance:** Defined by Phase 4e but NOT yet enforced in code; awaits separately authorized future implementation phase.
- **V2 strategy-research direction:** Predeclared by Phase 4f (this branch) as **"Participation-Confirmed Trend Continuation"**; bounded feature list, bounded timeframe matrix, predeclared exclusion rules, predeclared validation requirements. NOT implemented; NOT backtested; NOT validated.
- **OPEN ambiguity-log items after Phase 4f:** zero relevant to runtime / strategy implementation.
- **Project locks preserved verbatim.** R3 baseline-of-record; H0 framework anchor; R1a / R1b-narrow / R2 / F1 / D1-A retained research evidence only; R2 FAILED — §11.6 cost-sensitivity blocks; F1 HARD REJECT; D1-A MECHANISM PASS / FRAMEWORK FAIL — other; §11.6 = 8 bps HIGH per side; §1.7.3 project-level locks; mark-price stops; v002 verdict provenance; Phase 3q mark-price 5m manifests `research_eligible: false`. All preserved.
- **Branch state:**
  - `phase-4f/external-strategy-research-landscape-v2-candidates` pushed to `origin/phase-4f/external-strategy-research-landscape-v2-candidates`. Two commits on the branch (memo + closeout). NOT merged to main.
  - All prior phase branches preserved at their respective tips.

## Next authorization status

**No next phase has been authorized.** Phase 4f's recommendation is **Option B (docs-only V2 strategy-spec memo for Participation-Confirmed Trend Continuation) as primary**, with **Option C (docs-only V2 data-requirements and feasibility memo) as conditional secondary**. Option A (remain paused) is procedurally acceptable but understates operator-stated motivation. Options D / E (immediate data acquisition or backtest) are NOT recommended. Option F (paper/shadow / live-readiness / exchange-write) is forbidden / not recommended.

Selection of any subsequent phase requires explicit operator authorization for that specific phase. No such authorization has been issued.
