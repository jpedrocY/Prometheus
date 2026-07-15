# Phase 4bn-AW — Return-to-Strategy-Research Candidate-Family Screening

## 1. Phase identity

Phase 4bn-AW — Return-to-Strategy-Research Candidate-Family Screening and Bounded
Independent-Review Preparation.

## 2. Branch

`phase-4bn-aw/return-to-strategy-research-candidate-family-screening`.

## 3. Base SHA

`d90505a2e82c3f018cf68eeff8e7c5c1e92ee1d2` (`HEAD == main == origin/main` at branch
time; tip after the Phase 4bn-AV merge-closeout SHA-finalization commit). Verified in
sync before branching; the only untracked item was the transient
`.claude/scheduled_tasks.lock`, which was not staged, modified, deleted, cleaned, or
committed.

## 4. Phase type

Docs-only **screening and independent-review-preparation** phase. It inspects committed
documentation, committed source, committed tests, and Git history read-only; reasons over
the committed negative-result lineage and the committed data-capability record; and
creates exactly three new documentation files. It is **not** a preregistration, an
experiment design, a reserve-spend proposal, a data-acquisition proposal, a model-selection
phase, a backtest, a diagnostic, a strategy implementation, or a continuation of either
stopped arc. It authorizes nothing beyond the creation of documentation.

## 5. Risk tier

Tier 1 / Full Phase per `docs/00-meta/process/phase-risk-tiering-standard.md` — it touches
scientific direction and the return-to-strategy-research question, so it is treated at the
highest ceremony tier even though it mutates no eligibility, manifest, verdict, reserve, or
lock and produces a **provisional, non-authorizing** shortlist only.

## 6. Exact authorization boundary

Authorized: read committed docs / source / tests / Git metadata; author exactly three new
files (this screening memo, a bounded Fable independent-review brief, and a closeout);
commit and push the dedicated phase branch. **Not** authorized: to spend, read, load,
inspect, enumerate for content, sample, or score any evidence reserve; to open the v002
terminal window or v002 sealed test; to open anything under `data/microstructure/` or
`data/research/`; to acquire or read any market data; to run pytest / Ruff / mypy / any
project script / builder / diagnostic / model / label / feature pipeline / backtest /
replay / runtime process; to use the network, web search, any API, credentials, WebSocket,
MCP, Graphify, or `.mcp.json`; to run Fable or any external reviewer; to modify any
existing file; to create a process standard, preregistration, reserve-spend proposal, or
successor execution prompt; or to authorize any successor phase. This phase used committed
repository evidence only.

## 7. Documents, source, tests, and Git history inspected

Committed, read-only (README and `current-project-state.md` treated as potentially stale
navigational documents; recent implementation reports and merge-closeouts outrank stale
summaries):

- **Stopped-arc lineage:** `2026-07-08_phase-4bn-ak_ml-arc-decision-memo.md`;
  `2026-07-12_phase-4bn-as_longhorizon-ml-ambiguity-decision-memo.md`
  (`STOP_LONGHORIZON_ML_ARC`); `2026-07-14_phase-4bn-at_top-of-book-mechanism-admissibility-bounce-preregistration.md`
  (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`); the Phase 4bn-AJ / AP / AQ / AR results as
  restated through AK/AS/AT.
- **Direction / governance:** `2026-07-14_phase-4bn-au_post-at-project-direction-progress-successor-selection.md`
  and its Fable independent-review assessment; `2026-07-14_phase-4bn-av_evidence-budget-ledger-...-consequence-protocol.md`
  and its closeout (the evidence ledger and spending-authority standard).
- **Data / admissibility capability:** `2026-06-05_phase-4bn-ab_source-admissibility-memo.md`;
  `2026-05-07_phase-4at_binance-microstructure-data-availability-capture-feasibility.md`
  (the data-family availability matrix and historical-vs-live classification); the Phase
  4bn-Y chronological-split / holdout policy and Phase 4bn-L storage/budget references as
  restated through AB/AV.
- **Governance gate:** `docs/00-meta/m0-mechanism-admissibility-gate.md` (twelve-clause M0;
  post-null cooldown §6; cooled-down families §7); process standards under
  `docs/00-meta/process/`.
- **Committed source (read for capability confirmation only; none modified):**
  `src/prometheus/research/microstructure/manifest.py` (Phase 4aw `flip_research_eligible`
  always-raises; `research_eligible = False`); `pre_v002_ml_dataset_contract.py` (locked
  8/16 bps; frozen success thresholds); `pre_v002_split_policy.py`; `canonical_paths.py`.
- **Git history / metadata:** `git log`/`status`/`rev-parse`/`ls-files`/`check-ignore` for
  base-state verification and to confirm `data/` remains gitignored (0 tracked).

## 8. Confirmation no data or reserve was opened

Confirmed. No feature/label/raw Parquet row, no v002 terminal window, no v002 sealed test,
no local generated research/model/backtest/diagnostic artefact, and no file under
`data/microstructure/` or `data/research/` was opened, read, listed for content, hashed,
sampled, or scored. `test_rows_loaded = 0` posture preserved. Only `git` bookkeeping,
committed-document reads, and repository text search touched anything under `data/` paths,
and those inspect Git state only, not file contents. No network, API, credential, or
external reviewer was used.

## 9. Summary of stopped arcs and negative-result lineage

The committed lineage is a long, disciplined sequence of negatives on an aggTrades-only
substrate plus a data-inadmissibility stop:

- **Price-only single-symbol directional continuation (DEPLETED, M0 §7.A).** R2
  (cost-fragility), F1 (catastrophic-floor), V2 (design-stage), G1 (regime-gate × setup
  sparseness), C1 (fires-and-loses), plus Phase 4af's bar-level directional-persistence
  null across 80 (symbol, interval, N) cells.
- **Cross-sectional trend / relative-strength symbol-selection (COOLED_DOWN, §7.B).**
  Phase 4ai's composite ranking + rank-quality filter returned `NOT_SUPPORTED` (frac_selected
  > median ≈ 0.49; median spread ≤ 0; IC median 0.0 in every primary cell).
- **Derivatives-context directional lane (CONDITIONAL_ONLY, §7.C).** D1-A reached MECHANISM
  PASS / FRAMEWORK FAIL; derivatives-context is admissible only as a **context lens**, never
  a directional trigger.
- **Long-horizon aggTrades ML arc (`STOP_LONGHORIZON_ML_ARC`, Phase 4bn-AS).** The clean 15s
  directional-information result (L2 +5.03 pp over majority, block agreement 1.000, no holdout
  reversal) was **economically thin** (only 2.47% of 15s moves clear 16 bps) and **inverted**
  at the materiality-motivated longer horizons (5m accuracy vs majority −0.222 pp; 30m −1.348;
  1h −2.868; 5m calibration unusable; mixed blocks). Stopped as an evidence-and-methodology
  stop; the pre-v002 internal holdout is now **consumed**.
- **Top-of-book mechanism arc (`STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`, Phase 4bn-AT).**
  The model-free question of whether the 15s result was genuine midpoint movement or bid–ask
  bounce could not be answered: the retrospective futures bookTicker source is Tier-1
  undocumented, carries an unremediated out-of-order defect (issue #305), reportedly ceased
  in 2024, and its 2024-10…11 coverage is unconfirmed; prospective capture is regime-non-
  comparable and cannot be aligned to the 2024 trades. A source-admissibility / measurability
  stop.

**Load-bearing reading.** Only a *narrow implementation* is ruled out in some cases (a
specific 15s strict-sign classifier), but the broader picture is decisive on two points: the
aggTrades-only substrate has shown no *economically material, robust, directional* edge at
admissible cost, and the quote-based measurement lane is data-inadmissible retrospectively.
Both stopped arcs are preserved exactly and are **not** merged, softened, reinterpreted, or
reopened.

## 10. Summary of consumed and reserved evidence (Phase 4bn-AV ledger)

- `PRE_V002_INTERNAL_HOLDOUT` — 2024-11-17 .. 2024-11-30 (14 dates) — **CONSUMED**; scored
  under Phase 4bn-AR; not reusable as independent confirmation; descriptive-with-provenance
  only.
- `V002_TERMINAL_WINDOW` — 2024-12-01 .. 2025-02-28 (90 dates; 155,153,449 rows by committed
  reference) — **UNTOUCHED_RESERVED**.
- `V002_SEALED_TEST` — 2025-02-14 .. 2025-02-28 (15 dates; `test_rows_loaded = 0`) —
  **UNTOUCHED_RESERVED**, highest protection.
- `HIST_TOB_BOOKTICKER_SOURCE` — **INADMISSIBLE_OR_UNAVAILABLE** for the 2024 mechanism
  question; not a spendable reserve; prospective collection cannot retroactively answer the
  historical question.

Every candidate below is screened on the hard constraint that **initial development must
spend no reserve** — it must run on already-used development data (pre-v002 train/validation,
already built) and/or already-acquired non-reserve data, holding the terminal and sealed
reserves untouched for a later, separately-authorized confirmation stage only.

## 11. Summary of admissible and inadmissible data-source families (committed records)

From the Phase 4at availability matrix and the Phase 4bn-AB source-admissibility record (no
data opened to establish this):

**Admissible without new acquisition (already on disk or archive-precedented, non-reserve):**

- **BTCUSDT USDⓈ-M aggTrades, pre-v002** (2024-03-01…2024-11-30; 275 dates; ~400M rows) —
  fully normalized/feature/label built; train 214d + validation 45d usable as development;
  holdout 14d CONSUMED (descriptive only). This is the project's actual substrate.
- **Klines (OHLCV), multi-symbol, multi-interval** — already on disk for BTCUSDT, ETHUSDT and
  the Phase 4ac core set (ADA, SOL, XRP) at multiple intervals (Phase 2 v002 + Phase 4i
  `__v001`); archive-available (`data.binance.vision`).
- **Funding-rate history** — already on disk (`funding__v001`) for BTCUSDT, ETHUSDT, and the
  Phase 4ac core set; admissible only as a **context lens** (D1-A precedent).
- **Mark-price / premium-index / index-price klines** — archive-available; governed partial
  (Phase 3r §8 invalid-window rules).

**Inadmissible or blocking (no acquisition authorized; several cannot answer a historical
question at all):**

- **bookTicker / partial-depth / diff-depth / order-book reconstruction / forceOrder
  liquidations** — WS-live-capture only, **no historical archive**; retrospectively
  INADMISSIBLE; prospective capture regime-non-comparable.
- **OI historical statistics, top/global long-short ratios, taker buy/sell ratio** — REST
  30-day retention only; historically BLOCKED for a 2024 window without forward capture.
- **Multi-symbol aggTrades other than BTCUSDT** — archive-available but **not acquired**;
  needs a separately-authorized acquisition phase (blocking now).

## 12. Candidate-generation method

Generation followed the negative-result and data-capability audit (not a predetermined
favourite, no target count). The method: enumerate mechanism families from (a) the committed
Phase 4as M-1…M-14 microstructure/derivatives map, (b) classical, externally-documented
market stylized facts, and (c) cross-asset structure; then filter by two gates applied
before any preference — **(i) admissible development without acquisition or reserve spend**,
and **(ii) genuine structural distance from both stopped arcs and every cooled-down/rejected
family**. Families sharing one mechanism and differing only by implementation were combined.
Novelty was assessed against the actual committed lineage, not by renaming. Fewer candidates
(including zero) was an accepted outcome; the audit yielded exactly three survivors, so no
padding was required.

## 13. Candidate overlap / rescue audit

Each survivor was checked for reduction to stopped/exhausted work:

- **CF-1** (realized-volatility magnitude forecasting) is not the stopped ML arc: the target
  is return **magnitude / variance**, not direction/sign; the mechanism is volatility
  clustering, not directional information; it does not reuse the consumed holdout as
  confirmation and does not re-fit `forward_direction_<H>`.
- **CF-2** (cross-symbol temporal lead–lag) is not the cooled-down cross-sectional lane (§7.B):
  that lane **ranks** symbols cross-sectionally at one time; CF-2 is a **temporal-causal**
  relationship (lagged BTC → alt), a different mechanism and object.
- **CF-3** (derivatives-context + settlement/session-timing volatility-regime conditioning) is
  not D1-A (§7.C): it uses funding/positioning and a deterministic calendar as a
  **non-directional context/regime** signal, never a directional trigger.

None reduces to R2/F1/V2/G1/C1, the price-only continuation lane, the ToB quote lane, or a
relabeled stopped hypothesis.

## 14. Full candidate list (generated)

1. Forward-direction classifier on aggTrades at a new horizon/threshold/model.
2. Top-of-book bounce decomposition / any quote-referenced label.
3. Order-book imbalance / depth / sweep / replenishment (M-2/3/4/7/8).
4. Liquidation-cascade proxy (M-9).
5. Cross-sectional relative-strength symbol ranking.
6. Funding-aware directional contrarian.
7. Price-only single-symbol directional continuation (any interval).
8. **CF-1 — Microstructure realized-volatility (magnitude) forecasting from aggTrades.**
9. **CF-2 — Cross-symbol return lead–lag / information transmission (temporal).**
10. **CF-3 — Derivatives-context + settlement/session-timing volatility-regime conditioning.**
11. Trade-burst / activity (liquidity-demand) prediction (M-6).
12. Jump / discontinuity prediction from order flow.
13. Intraday variance-ratio / microstructure-noise diagnostic on aggTrades.
14. Prospective new-data-collection-first (capture depth/bookTicker, then define a hypothesis).

## 15. Rejected and blocked candidates with reasons

| # | Candidate | Disposition | Binding reason (hard-rejection rule) |
|---|---|---|---|
| 1 | Forward-direction classifier, new horizon/threshold/model | **REJECT** | Rescue/duplicate of `STOP_LONGHORIZON_ML_ARC` and the 15s arc (rules 1, 3); result-informed after consumed evidence (rule 13). |
| 2 | Top-of-book bounce / quote label | **REJECT** | Duplicate of `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE`; data inadmissible (rules 2, 6). |
| 3 | Order-book imbalance / depth / sweep | **REJECT** | Data WS-only, unacquired, no history → inadmissible (rule 6); M0 §7.D. |
| 4 | Liquidation-cascade proxy | **REJECT** | Proxy-only, no history, WS-only; completeness-invalid (rule 6). |
| 5 | Cross-sectional relative-strength ranking | **REJECT** | Cooled-down §7.B after `NOT_SUPPORTED`; post-null tweak (rule 3; M0 §6). |
| 6 | Funding-aware directional contrarian | **REJECT** | D1-A rescue; context-lens-only precedent (rules 3, 18; M0 §7.C). |
| 7 | Price-only single-symbol continuation | **REJECT** | Depleted §7.A; unlimited nearby variants (rules 1, 10). |
| 11 | Trade-burst / activity prediction | **REJECT / MERGE** | Same magnitude-family as CF-1; low standalone decision consequence (rule 17); combined into CF-1. |
| 12 | Jump / discontinuity prediction | **REJECT** | Rare events untradable at 16 bps; unbounded multiple testing (rules 10, 11). |
| 13 | Variance-ratio / microstructure-noise diagnostic | **REJECT** | A measurement/diagnostic, not a strategy family; rescue-adjacent to the stopped ToB bounce question (rules 17, 3). |
| 14 | Prospective-capture-first | **REJECT** | Data-acquisition-before-hypothesis (rule 12); prospective cannot answer a historical question; acquisition unauthorized. |

Rejected candidates are not promoted into the Fable shortlist.

## 16. Screening matrix (surviving candidates)

Scale: `STRONG` / `MODERATE` / `WEAK` / `FAIL`; reasoned ordinal comparison, not a weighted
numeric optimizer.

| Criterion | CF-1 RV-forecasting | CF-2 Lead–lag | CF-3 Context/timing regime |
|---|---|---|---|
| 1 Genuine novelty (distance from stopped/rejected) | STRONG (magnitude target, new mechanism) | MODERATE (temporal ≠ cross-sectional; adjacency risk) | MODERATE (context-lens reframing; not D1-A) |
| 2 Mechanism strength | STRONG (volatility clustering — robust stylized fact) | STRONG (price-discovery diffusion latency) | MODERATE (positioning/settlement/session effects) |
| 3 Prediction precision | STRONG (beat HAR-RV / RV-persistence, predeclarable) | MODERATE (IC vs contemporaneous baseline; pair/lag choices) | MODERATE (regime split predeclarable; effect size uncertain) |
| 4 Boundary-condition clarity | STRONG (regime/jump caveats explicit) | MODERATE (liquidity-tiered; decays with efficiency) | MODERATE (event-window bounded) |
| 5 Data admissibility | STRONG (BTCUSDT aggTrades on disk) | **FAIL/WEAK** (tradeable form needs unacquired multi-symbol aggTrades; klines too coarse) | MODERATE (funding on disk; OI blocked; calendar free) |
| 6 Development-evidence sufficiency (no reserve) | STRONG (pre-v002 train/validation) | WEAK (blocked at tradeable granularity) | STRONG (funding + calendar + klines/aggTrades) |
| 7 Evidence-budget compatibility (protects reserves) | STRONG | STRONG (if unblocked) | STRONG |
| 8 Falsifiability | STRONG (no skill over HAR-RV ⇒ stop) | MODERATE (IC ≤ baseline ⇒ stop; multiple-testing pressure) | MODERATE (no regime differential ⇒ stop) |
| 9 Negative-result value | STRONG (closes magnitude-predictability of substrate) | MODERATE | MODERATE |
| 10 Multiple-testing risk | MODERATE (few baselines; horizon set predeclarable) | **WEAK** (pairs × lags × horizons) | MODERATE (calendar fixed ex-ante; funding buckets bounded) |
| 11 Rescue risk | LOW/MODERATE (microstructure-adjacent; must clear M0.5/§7.D) | MODERATE (cross-sectional adjacency) | MODERATE (D1-A adjacency) |
| 12 M0 compatibility | MODERATE (non-directional; M0.3 via baseline-differential; M0.8 PASS) | MODERATE (M0.8 BLOCKING now) | MODERATE (M0.8 partial; context-lens compliant) |
| 13 Decision consequence | MODERATE (indirect: vol-targeting/regime gating, not a directional edge) | STRONG-if-unblocked (directional, tradeable) | WEAK/MODERATE (context layer; no standalone edge) |
| 14 Implementation burden | LOW (data built; labels derivable descriptively) | HIGH (acquisition + alignment) if unblocked | LOW/MODERATE |
| 15 Durable project value | STRONG (first admissible test of a robust stylized fact on the substrate) | MODERATE | MODERATE |

## 17. Provisional ranking

1. **CF-1 — Microstructure realized-volatility (magnitude) forecasting** (provisional
   first-ranked).
2. **CF-2 — Cross-symbol return lead–lag / information transmission** (shortlisted; **BLOCKED**
   on data admissibility, therefore cannot rank first).
3. **CF-3 — Derivatives-context + settlement/session-timing volatility-regime conditioning**
   (shortlisted; developable now but weakest decision consequence and target-overlap with
   CF-1).

The CF-2↔CF-3 ordering is the closest call: CF-2 has the strongest mechanism and the only
genuinely directional decision consequence but is blocked pending acquisition; CF-3 is fully
developable now but its consequence is indirect. CF-2 is placed second for mechanism and
decision consequence while explicitly barred from first by its blocked status; this is
provisional and is a primary question for independent review.

## 18. Shortlist (≤ 3 candidates)

CF-1, CF-2, CF-3 — exactly the three survivors. Each passes every hard-rejection rule, is
structurally distinct from both stopped arcs, has a clear mechanism and falsification path,
requires **no reserve spend for initial development**, and could plausibly become a bounded
preregistration later (CF-2 only after a separately-authorized acquisition phase clears its
data block).

## 19. Provisional first-ranked candidate

**CF-1 — Microstructure realized-volatility forecasting.** It is the only survivor that is
fully developable now on already-built, non-reserve data; rests on the most robust,
externally-documented mechanism (volatility clustering / long-memory in realized variance);
admits the cleanest predeclared kill (no incremental skill over a HAR-RV / RV-persistence
baseline on validation blocks); carries the highest negative-result value (a null closes the
question of whether the admissible substrate holds *any* exploitable predictable structure
beyond the already-tested directional target); and preserves both scarce reserves for a later
confirmation stage. Its binding weakness — indirect decision consequence — is stated plainly
in §26 and §29 and is not minimized.

## 20. Mechanism and prediction of each shortlisted candidate

- **CF-1.** *Mechanism:* realized variance exhibits clustering and long memory (ARCH/HAR
  stylized fact); aggTrades order-flow intensity and trade-size dispersion plausibly carry
  incremental information about near-future realized variance beyond past RV. *Prediction:*
  aggTrades-derived intensity/dispersion features improve out-of-sample RV forecasts over a
  HAR-RV(-persistence) baseline, measured by a predeclared loss (e.g. QLIKE) on UTC
  date/month blocks.
- **CF-2.** *Mechanism:* price discovery concentrates in the most liquid instrument (BTC);
  information diffuses to less-liquid correlated assets with a measurable latency (Granger-
  causal lead–lag). *Prediction:* lagged BTC returns predict same-sign short-horizon alt
  returns with cross-symbol IC above a contemporaneous-only baseline, strongest for the
  least-liquid admissible symbols.
- **CF-3.** *Mechanism:* crowded positioning (funding extremes) and deterministic settlement/
  session timing (funding settlement at fixed UTC hours; session opens) precede predictable
  shifts in the **volatility/liquidity regime** (not direction). *Prediction:* realized
  volatility / activity is systematically elevated (or suppressed) in predeclared funding-
  extreme and calendar windows versus matched control windows.

## 21. Boundary conditions

- **CF-1:** incremental skill concentrated in normal (diffusive) regimes; expected to weaken
  at news-driven jumps and structural breaks; the substrate's regime-narrow late-2024
  development window limits regime generality.
- **CF-2:** strongest for less-liquid alts and high-information periods; absent among
  equally-liquid pairs; decays as the relationship is arbitraged; likely already arbitraged
  at the only admissible (coarse kline) granularity.
- **CF-3:** effects expected around fixed settlement/session boundaries and funding extremes;
  expected to weaken away from those windows and in calm-funding regimes.

## 22. Required data family (per shortlisted candidate)

- **CF-1:** BTCUSDT USDⓈ-M aggTrades, pre-v002 — **admissible, on disk, non-reserve**. RV
  labels derivable descriptively from the same rows. No new source.
- **CF-2:** multi-symbol return series at a tradeable granularity. Admissible form = multi-
  symbol **klines** (on disk) but likely too coarse; tradeable form = multi-symbol
  **aggTrades**, which are **not acquired** → **BLOCKING** without a separately-authorized
  acquisition phase.
- **CF-3:** funding-rate history (on disk, **context-lens only**) + a deterministic UTC
  calendar (no data) + optional aggTrades/klines for the RV/activity target. OI-history
  component is **BLOCKED** (30-day retention). Admissible for the funding+calendar form.

## 23. Development-evidence path (no reserve)

All three develop **without** the terminal window or sealed test. CF-1 and CF-3 use pre-v002
train/validation (already used development data) plus non-reserve on-disk data; the consumed
holdout may be used **descriptively only**. CF-2's admissible-granularity form uses on-disk
multi-symbol klines; its tradeable form cannot be developed without acquisition. Genuine
independent confirmation for any survivor would be reserved for a later, separately-
authorized stage against the untouched terminal reserve — never during discovery, screening,
feature development, debugging, or model selection.

## 24. Falsification path

- **CF-1:** no incremental out-of-sample skill over the HAR-RV / RV-persistence baseline
  (predeclared loss, block-consistent) ⇒ stop the family.
- **CF-2:** cross-symbol IC ≤ the contemporaneous-only baseline, or no consistent lead
  direction across admissible symbols/blocks ⇒ stop.
- **CF-3:** no predeclared volatility/activity differential between the funding-extreme /
  calendar windows and matched controls, block-consistent ⇒ stop.

## 25. Negative-result value

- **CF-1:** HIGH — a null shows the admissible substrate lacks even magnitude-predictability
  beyond price-based baselines, materially narrowing the search and reinforcing the stop
  posture at near-zero reserve cost.
- **CF-2:** MODERATE — a null closes the lead–lag lane at the tested granularity but leaves
  finer-granularity variants open (hence the acquisition question).
- **CF-3:** MODERATE — a null closes the positioning/timing regime-conditioning lane for the
  admissible signals.

## 26. Evidence-budget implications

None of the three spends any reserve during development; all three protect
`V002_TERMINAL_WINDOW` and `V002_SEALED_TEST` for a later confirmation stage that would
itself require the full Phase 4bn-AV pre-spend sequence (docs-only proposal → repository-
grounded compliance review → bounded independent critical review → explicit operator approval
→ separate execution prompt → ledger preflight → post-spend update). This screening authorizes
**no** such spend. The reserve-preservation property is a shared strength and is why a thin
admissible shortlist is preferable to any candidate that would require early reserve access.

## 27. Multiple-testing and post-hoc risk

- **CF-1:** MODERATE — few baselines and a predeclarable horizon/feature set bound the search;
  the risk is feature-menu expansion, controllable by preregistration.
- **CF-2:** WEAK (high risk) — pairs × lags × horizons is a large garden of forking paths; a
  bounded preregistration would have to fix the symbol set, lag set, and horizon before any
  analysis.
- **CF-3:** MODERATE — the calendar is fixed ex-ante (low researcher freedom), but funding-
  bucket and window definitions must be predeclared.

Across all three, the consumed-holdout and anti-rescue constraints (Phase 4bn-AS §21/§24; M0.10;
Phase 4bn-AV §16) forbid result-informed reuse; no candidate may change its question after
reference to consumed results.

## 28. M0 compatibility

- **CF-1:** non-directional, so it escapes the depleted directional lanes; M0.3 is satisfied
  via the "equivalent baseline differential for non-strategy mechanism claims" route (predicted
  skill over HAR-RV, not a Δ_R). M0.8 data feasibility **PASS** (aggTrades on disk). M0.5 cost-
  realism does not bind per-prediction for a non-trading forecast, but any eventual trading
  overlay must independently clear 8/16 bps — flagged, not assumed. M0.4/M0.10 clear by
  non-directional structural distinctness; §7.D microstructure-lane caution addressed because
  the data is already acquired and the target is magnitude, not short-horizon direction.
- **CF-2:** M0.8 **BLOCKING** now (multi-symbol aggTrades unacquired); M0.4/M0.10 require
  explicit distance from the cooled-down cross-sectional lane (temporal-causal ≠ cross-
  sectional ranking); M0.6/M0.7 opportunity- and edge-rate floors must be predeclared before
  any acquisition.
- **CF-3:** M0.8 partial (funding PASS, OI BLOCKED); M0.9/§7.C compliance requires it remain a
  **context/regime lens**, never a directional trigger (D1-A boundary).

No candidate is authorized to clear M0; M0 clearance is a separate future docs-only step per
candidate.

## 29. Strongest counterargument

The strongest case against reopening strategy research now: the repeated negatives indicate
the admissible aggTrades-only substrate most plausibly lacks an *exploitable, economically
material, robust directional* structure — the 15s directional information was thin and possibly
bounce-contaminated, the long-horizon extension inverted, the cross-sectional lane cooled down,
and the quote-based measurement lane is data-inadmissible. Against that backdrop, candidate
generation risks post-hoc invention, and the survivors are vulnerable to the "novelty by target-
swap, not by a new tradeable edge" critique: CF-1 and CF-3 are **non-directional**, so even a
clean success would not by itself produce a directional edge or clear the locked 16 bps frame,
and the one genuinely directional survivor (CF-2) is **blocked** on data. A dormant-runtime
safety slice (the Phase 4bn-AU Candidate A restart-re-hydration fix) or simply remaining paused
may be more concrete and more falsifiable than another substrate research arc.

**Does the shortlist overcome it? Partially, and honestly not fully.** CF-1 does carry genuine,
independent value: it tests a *different and more robust* stylized fact (volatility clustering)
on already-built data at near-zero reserve cost, and a null would materially narrow the search
while a positive would be the first admissible predictive result on a non-directional target —
a real decision either way. But the deeper objection stands: none of the survivors is a
demonstrated tradeable directional edge, and CF-1/CF-3 successes would not, alone, clear the
directional-cost frame the project ultimately needs. The objection is therefore **not defeated**;
it is the reason this phase produces a *provisional* shortlist for independent review rather
than declaring a winner, and it is why "remain paused / do the concrete runtime-safety slice"
remains a live competing option the operator should weigh.

## 30. Evidence or argument that would change the ranking

- If independent review judges that a **non-directional forecast has no meaningful decision
  consequence** under the project's directional/cost frame, CF-1's indirect-consequence weakness
  could demote the entire shortlist below "remain paused."
- If a **bounded, low-multiple-testing lead–lag preregistration on admissible klines** is shown
  to be both mechanism-faithful and falsifiable at that granularity, CF-2 could rise (its data
  block partly lifts).
- If a closer reading shows CF-3's admissible (funding+calendar) form collapses to a known
  D1-A-adjacent or already-tested effect, CF-3 should be demoted or rejected.
- If CF-1's HAR-RV baseline is judged trivially beatable (so a "win" is uninformative) or
  trivially unbeatable (so the null is preordained), its falsifiability weakens and it should
  drop.

## 31. Exact scope of the later Fable review

The bounded Fable review brief (companion file
`2026-07-15_phase-4bn-aw_bounded-fable-independent-review-brief.md`) is a single first-round
decision task on the **shortlist only**, treating the brief as the entire evidence set. It asks
Fable to: rank the three shortlisted candidates; recommend one or recommend none; give the
strongest objection to its own recommendation; give one clean kill criterion for the recommended
candidate; state the evidence/reasoning that would most change its ranking; and name at most one
genuinely-distinct omitted family. It does **not** ask Fable to inspect any repository, design
the next Claude Code phase, produce implementation steps, or perform web research. It begins with
the literal no-inspection instruction and is bounded to ~900 words in / ~1,200 words out.

## 32. Confirmation Fable has not yet reviewed the shortlist

`Fable has not reviewed the shortlist during Phase 4bn-AW.` The brief is created for later use
by the operator in a fresh Fable chat; no external reviewer, network, or tool was used in this
phase.

## 33. Confirmation no hypothesis is authorized for execution

`The Phase 4bn-AW shortlist is provisional and non-authorizing.` No candidate is selected for
execution. No preregistration, experiment design, reserve-spend proposal, data-acquisition
proposal, model selection, or backtest is created or authorized.

## 34. Recommended next operator action

Return the three Phase 4bn-AW files and the operator report to ChatGPT for compliance review and
plain-language interpretation, and make a separate merge decision. After approval, paste **only**
the bounded review brief into a completely fresh Fable chat. Do not authorize any candidate, any
preregistration, any acquisition, or any reserve spend; the project remains paused with respect to
execution. Any candidate selected after independent review requires a separate preregistration
phase, explicit operator authorization, and a new Claude Code prompt.

## 35. Exact final result state

`RETURN_TO_STRATEGY_RESEARCH_CANDIDATE_FAMILIES_SCREENED__PROVISIONAL_SHORTLIST_RECORDED__BOUNDED_FABLE_INDEPENDENT_REVIEW_BRIEF_CREATED__NO_HYPOTHESIS_EXECUTION_AUTHORIZED__NO_EVIDENCE_RESERVE_SPEND_AUTHORIZED`

`No hypothesis, strategy, model, diagnostic, backtest, data acquisition, data reading, paper, shadow, live, or exchange-write execution is authorized by Phase 4bn-AW.`

`No evidence reserve is authorized for spending by Phase 4bn-AW.`

`The Phase 4bn-AW shortlist is provisional and non-authorizing.`

`Fable has not reviewed the shortlist during Phase 4bn-AW.`

`Any candidate selected after independent review requires a separate preregistration phase, explicit operator authorization, and a new Claude Code prompt.`

`Phase 4bn-AX or any other successor requires separate operator authorization.`

## 36. Preserved project locks

Unchanged: `STOP_LONGHORIZON_ML_ARC` and `STOP_TOB_MECHANISM_ARC_DATA_INADMISSIBLE` (distinct,
not merged, softened, reinterpreted, rescued, or reopened); Phase 4aw `flip_research_eligible(...)`
always-raising, never invoked; `research_eligible = False`; `eligibility_gate_status = PENDING`;
all published authorization flags `false`; the Phase 4bn-AE §19 M0 boundary (absolute); the locked
8 bps/side · 16 bps round-trip cost; the Phase 4ak twelve-clause M0 gate and §6 cooldown / §7
cooled-down families; the Phase 4bn-AV evidence ledger, spending-authority standard, and late-
inadmissibility protocol; Phase 4bb-F sidecar policy; Phase 4bn-L storage/budget policy; split and
holdout policies; dataset identities and hashes; sidecar and storage policies; every prior strategy
verdict (H0 / R3 / R1a / R1b-narrow / R2 / F1 / D1-A / V2 / G1 / C1 and the 5m thread); every
retained-evidence classification; and every completed implementation report.
