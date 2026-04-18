# First-Run Setup Checklist

## Purpose

This document defines the practical first-run setup checklist for the v1 Prometheus trading system.

Its purpose is to guide the operator from a fresh or near-fresh repository checkout toward a safe, staged operating environment without accidentally enabling real-capital trading before the correct phase gate.

This checklist is intentionally practical. It connects the architecture, security, operations, data, dashboard, alerting, and phase-gate documents into a step-by-step operator path.

Prometheus v1 is a safety-first, operator-supervised Binance USDⓈ-M futures trading system. It is not a lights-out autonomous AI trader.

---

## Scope

This checklist applies to Prometheus v1 under the following assumptions:

- venue: Binance USDⓈ-M futures,
- initial live symbol: BTCUSDT perpetual,
- ETHUSDT is research/comparison only,
- v1 live scope is one symbol, one position, and one active protective stop,
- runtime account mode is one-way mode,
- margin mode is isolated margin,
- strategy is rules-based breakout continuation,
- signal timeframe is 15m,
- higher-timeframe bias is 1h,
- entries use completed-bar confirmation followed by market entry,
- protective stop is exchange-side `STOP_MARKET`,
- restart always begins in `SAFE_MODE`,
- exchange state is authoritative,
- unknown execution outcomes fail closed,
- live operation is staged and supervised,
- initial tiny-live risk is 0.25% of sizing equity,
- initial effective leverage cap is 2x,
- internal notional cap is mandatory before live.

This checklist covers:

- repository setup,
- local development readiness,
- Python/tooling setup,
- configuration skeleton,
- historical data preparation,
- runtime database/log setup,
- dry-run setup,
- dashboard setup,
- Telegram/n8n alert-route setup,
- dedicated NUC / mini PC preparation,
- host-hardening checks,
- backup/restore checks,
- paper/shadow readiness,
- production Binance key timing,
- tiny-live readiness,
- emergency access readiness,
- and first-run evidence capture.

This checklist does **not** define final implementation commands before the implementation exists.

Where exact commands are not yet known, this document uses implementation placeholders such as:

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

Claude Code or the human implementer must replace those placeholders once the actual code, package manager, CLI, services, migrations, and dashboard entrypoints exist.

---

## Current Operator Starting Point

As of this checklist version, the operator already has:

```text
Repository cloned locally at: C:\Prometheus
Repository tracked with: GitHub Desktop
Repository open in: AntiGravity IDE
Claude Code extension: installed and logged in
Claude Code account tier: Max plan
```

The initial local workflow should therefore begin from:

```powershell
cd C:\Prometheus
```

This checklist assumes the operator will work with ChatGPT guidance during setup by sharing screenshots, photos, terminal output, IDE state, dashboard state, logs, and error messages when needed.

The operator-guided workflow is part of setup discipline. When setup output is unclear, the correct response is to inspect evidence and resolve it before proceeding, not to guess.

---

## Non-Negotiable Safety Rules

## Rule 1 — Do not create production trade-capable Binance API keys yet

Do **not** create production trade-capable Binance API keys during:

- repository setup,
- local development,
- dependency installation,
- historical data setup,
- validation/research,
- early dry-run runtime,
- dashboard development,
- or initial Claude Code implementation.

Production trade-capable Binance keys belong near the approved transition toward tiny live, after the correct phase gate, host-hardening, secrets management, IP restrictions, permission scoping, alerting, backup/restore, and operator readiness checks are complete.

## Rule 2 — Credentials alone never permit trading

The presence of credentials must not enable live order placement by itself.

Live exchange-write capability must also require explicit environment/config permission and phase-gate approval.

A safe configuration must support this state:

```text
credentials_present = true
exchange_write_enabled = false
live_order_submission = blocked
```

## Rule 3 — Dry-run and paper/shadow come before tiny live

Prometheus must proceed through staged validation:

```text
local development
→ validation / research
→ dry-run runtime
→ paper / shadow
→ tiny live
→ scaled live
```

Tiny live is not allowed just because code exists.

## Rule 4 — Every live-capable restart begins in SAFE_MODE

No runtime may start directly into normal live trading mode.

On startup or restart, Prometheus must:

1. enter `SAFE_MODE`,
2. load local persisted state as provisional,
3. initialize observability,
4. verify configuration and secrets,
5. establish required streams/connectivity,
6. reconcile exchange state where applicable,
7. verify position/protection state where applicable,
8. expose status to the operator,
9. and only then allow normal operation if all gates pass.

## Rule 5 — Unknown state fails closed

If the system cannot prove that account, order, position, stop, stream, or reconciliation state is safe, it must block new entries.

The safe default is:

```text
entries_blocked = true
reconciliation_required = true
operator_review_required = true where needed
```

## Rule 6 — No manual bypasses

The dashboard, CLI, scripts, or IDE must not allow bypassing:

- kill switch,
- reconciliation,
- incidents,
- exposure limits,
- stop-protection requirements,
- phase gates,
- or operator approval requirements.

## Rule 7 — No discretionary trading terminal in v1

The dashboard may be polished, information-rich, and Binance-like where useful.

It must remain a supervision and control surface, not a discretionary manual trading terminal.

Forbidden in v1:

- arbitrary manual buy/sell,
- click-to-trade,
- manual pyramiding,
- manual reversal,
- manual stop widening,
- casual risk/leverage sliders,
- bypassing reconciliation,
- bypassing kill switch,
- bypassing incidents or approvals.

---

## Setup Philosophy

## 1. Build from safe foundations

The implementation and setup order should be:

```text
data and storage
→ strategy/backtest validation
→ risk/state/persistence
→ observability/dashboard
→ dry-run execution simulation
→ paper/shadow
→ tiny live
```

Execution capable of changing real exchange state comes late.

## 2. Each stage must end with evidence

Do not move forward because the system “looks okay.”

Each setup stage should produce saved evidence such as:

- test output,
- lint/type-check output,
- data integrity output,
- migration output,
- dry-run logs,
- dashboard screenshots without secrets,
- alert test confirmation,
- backup/restore proof,
- reconciliation output,
- phase-gate approval notes.

## 3. Exact commands are implementation-owned

This document defines what must be done.

The final codebase must define how it is done through:

- README commands,
- CLI commands,
- scripts,
- Makefile tasks,
- package-manager commands,
- service files,
- dashboard run commands,
- migration commands,
- test commands,
- and deployment commands.

Where the implementation has not yet created exact commands, this checklist leaves placeholders.

## 4. The operator remains in control

Human/operator promotion decisions are required for:

- moving from dry-run to paper/shadow,
- moving from paper/shadow to tiny live,
- creating production trade-capable keys,
- enabling exchange-write capability,
- clearing kill switches,
- resolving severe incidents,
- increasing live risk,
- increasing leverage cap,
- scaling live operation.

---

# Part 1 — Repository and Local Development Setup

## Goal

Confirm that the local repository is available, tracked, editable, and ready for implementation work.

## Current expected state

```text
Local path: C:\Prometheus
GitHub Desktop: tracking repository
AntiGravity IDE: repository open
Claude Code extension: installed and logged in
```

## Checklist

- [ ] Open GitHub Desktop.
- [ ] Confirm the repository is visible and tracking the correct GitHub remote.
- [ ] Confirm the current branch is the intended working branch.
- [ ] Confirm there are no unexpected uncommitted changes before new documentation edits.
- [ ] Open AntiGravity IDE.
- [ ] Confirm the folder open in the IDE is:

```text
C:\Prometheus
```

- [ ] Confirm Claude Code extension is available inside the IDE.
- [ ] Confirm Claude Code is logged in to the expected account.
- [ ] Confirm the local terminal can open at:

```powershell
C:\Prometheus
```

- [ ] Confirm the repository contains the expected top-level documentation structure:

```text
docs/
```

- [ ] Confirm the following docs exist before coding handoff:

```text
docs/00-meta/current-project-state.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/09-operations/first-run-setup-checklist.md
docs/00-meta/ai-coding-handoff.md
```

## Evidence to save

- [ ] GitHub Desktop screenshot showing the correct repository.
- [ ] IDE screenshot showing `C:\Prometheus` open.
- [ ] Terminal output showing the repository path.
- [ ] Git status output with no unexpected changes after committing documentation updates.

## Do not proceed if

- repository path is wrong,
- GitHub Desktop is tracking the wrong repo,
- IDE is open to the wrong folder,
- Claude Code is not logged in,
- unexpected changes exist and have not been reviewed,
- or the documentation handoff files are missing.

---

# Part 2 — Python / Dependency / Tooling Setup

## Goal

Prepare the local development environment once implementation defines the toolchain.

## Required decisions to be filled by implementation

The AI coding handoff or first implementation phase must define:

- supported Python version,
- dependency manager,
- environment creation command,
- dependency install command,
- test command,
- lint command,
- formatting command,
- type-check command,
- local run command,
- dashboard run command,
- migration command.

## Checklist

- [ ] Confirm supported Python version.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Create local virtual environment or equivalent isolated environment.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Activate local environment.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Install project dependencies.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run dependency lock/check command if used.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run unit tests.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run lint checks.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run formatting check.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run type checks.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm test/lint/type-check failures are resolved or logged as implementation blockers.

## Required safety expectations

- [ ] No test requires production Binance credentials.
- [ ] No unit test requires live network access unless explicitly marked as an integration test.
- [ ] Fake exchange adapter tests exist before live exchange adapter tests are used.
- [ ] Exchange-write tests are impossible without explicit live-capability configuration.
- [ ] Secret values are not printed during test failures.

## Evidence to save

- [ ] Python version output.
- [ ] Dependency installation output.
- [ ] Test output.
- [ ] Lint output.
- [ ] Type-check output.
- [ ] List of failing checks, if any, with issue/spec-gap references.

## Do not proceed if

- the Python version is unsupported,
- dependency installation fails,
- core tests fail without explanation,
- tooling commands are unclear,
- or any test tries to use production exchange-write credentials.

---

# Part 3 — Configuration Skeleton

## Goal

Create safe configuration files for local development and later staged environments without enabling live trading accidentally.

## Required configuration environments

The implementation should support separate configurations for:

```text
LOCAL_DEVELOPMENT
VALIDATION_RESEARCH
DRY_RUN_RUNTIME
PAPER_SHADOW
TINY_LIVE
SCALED_LIVE
```

## Checklist

- [ ] Identify the configuration file format selected by implementation.

```text
FORMAT TO BE FILLED BY IMPLEMENTATION
```

- [ ] Create local development config from example/template.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm local development config uses fake adapter or no exchange-write capability.
- [ ] Confirm validation/research config does not contain production trade-capable credentials.
- [ ] Confirm dry-run config has:

```text
exchange_write_enabled = false
real_capital_enabled = false
adapter = fake or dry_run
```

- [ ] Confirm paper/shadow config has no real-capital write capability unless a later approved mode requires carefully scoped read-only access.
- [ ] Confirm tiny-live config template exists but is not activated before phase-gate approval.
- [ ] Confirm all config files avoid secrets in git.
- [ ] Confirm `.gitignore` or equivalent excludes local secret/config files.
- [ ] Confirm example config contains safe defaults.

## Required default safety values

The safest default config must include:

```text
runtime_mode_on_start = SAFE_MODE
entries_blocked_default = true
exchange_write_enabled = false
real_capital_enabled = false
live_symbol = BTCUSDT only when live stage is approved
paper_symbols = BTCUSDT, optionally ETHUSDT for comparison only
initial_live_risk_fraction = 0.0025
max_effective_leverage = 2.0
internal_notional_cap = required before live
```

## Secrets boundary

- [ ] No Binance API secret is stored in git.
- [ ] No Telegram bot token is stored in git.
- [ ] No n8n webhook secret is stored in git.
- [ ] No dashboard admin secret is stored in git.
- [ ] No `.env` file containing real secrets is committed.
- [ ] Secret templates contain placeholder values only.

## Evidence to save

- [ ] Redacted config screenshot or output.
- [ ] `.gitignore` confirmation.
- [ ] Config validation output.
- [ ] Screenshot or log showing exchange-write disabled in local/dry-run config.

## Do not proceed if

- any real secret is committed,
- config defaults allow live writes,
- local development config can place real orders,
- stage boundaries are unclear,
- or risk/leverage defaults are missing.

---

# Part 4 — Historical Data and Research Storage Setup

## Goal

Prepare historical research storage for BTCUSDT and ETHUSDT validation without mixing it with live runtime persistence.

## Required storage separation

Historical research storage and live runtime database storage must remain separate.

Conceptual layout:

```text
data/historical/
data/research/
data/derived/
reports/backtests/
reports/validation/
runtime/             # live runtime state, not historical archive
```

The final layout must be defined by implementation and documented.

## Required historical data for v1

At minimum, research/validation requires:

- BTCUSDT standard futures klines,
- ETHUSDT standard futures klines,
- derived or direct 1h bars,
- mark-price data where required for validation context,
- funding-rate history,
- exchange metadata snapshots,
- leverage bracket snapshots,
- commission assumptions.

## Checklist

- [ ] Confirm historical data directory layout.

```text
LAYOUT TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm research storage uses Parquet/DuckDB or the selected implementation equivalent.
- [ ] Confirm BTCUSDT 15m historical data download command exists.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm ETHUSDT 15m historical data download command exists.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm 1h bars are fetched or derived using point-in-time-valid logic.
- [ ] Confirm mark-price data fetch command exists where required.
- [ ] Confirm funding-rate fetch command exists where required.
- [ ] Confirm exchange metadata snapshot command exists.
- [ ] Confirm leverage bracket snapshot command exists.
- [ ] Confirm dataset manifest creation command exists.
- [ ] Confirm normalized dataset versions are immutable after validation use.
- [ ] Confirm invalid/missing data windows are logged explicitly.

## Data integrity checks

- [ ] No missing bars silently forward-filled.
- [ ] No malformed bars accepted silently.
- [ ] Timestamps are UTC Unix milliseconds.
- [ ] Bar identity uses `symbol`, `interval`, and `open_time`.
- [ ] 1h higher-timeframe alignment is point-in-time valid.
- [ ] Partial candles are not used as completed historical bars.

## Evidence to save

- [ ] Data download logs.
- [ ] Dataset manifest.
- [ ] Data completeness report.
- [ ] Invalid-window report if applicable.
- [ ] BTCUSDT dataset summary.
- [ ] ETHUSDT dataset summary.
- [ ] Metadata snapshot reference.
- [ ] Funding-rate coverage summary.

## Do not proceed if

- data source is unclear,
- BTCUSDT data is incomplete without logged invalid windows,
- ETHUSDT comparison data is incomplete without logged invalid windows,
- timestamps are not canonical UTC milliseconds,
- 1h bias alignment is not tested,
- or historical storage is mixed with runtime DB state.

---

# Part 5 — Runtime Database, Logs, and Local State

## Goal

Prepare local runtime persistence for restart safety, event/audit history, reconciliation continuity, incident tracking, and operator action tracking.

## Runtime persistence principles

The runtime database is part of the safety system.

It must preserve enough local continuity to support safe restart and reconciliation, but it does not become exchange truth.

Exchange state remains authoritative for:

- live position existence,
- live position side/size,
- open normal orders,
- open algo/protective orders,
- protective stop existence,
- filled order status.

## Recommended v1 runtime DB posture

The current design recommends SQLite with WAL mode for v1 unless implementation updates the decision.

Required SQLite behavior if used:

```text
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = configured_nonzero_value;
```

The selected synchronous setting must be documented before tiny live.

## Checklist

- [ ] Confirm runtime DB engine selected.

```text
ENGINE TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm runtime DB file path.

```text
PATH TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm logs directory path.

```text
PATH TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm structured events directory/path if separate.

```text
PATH TO BE FILLED BY IMPLEMENTATION
```

- [ ] Initialize runtime database.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Run migrations.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm runtime control state table/entity exists.
- [ ] Confirm active trade continuity table/entity exists.
- [ ] Confirm protection continuity table/entity exists.
- [ ] Confirm reconciliation table/entity exists.
- [ ] Confirm incident table/entity exists.
- [ ] Confirm operator action audit table/entity exists.
- [ ] Confirm runtime events table/entity exists.
- [ ] Confirm exchange events table/entity exists.
- [ ] Confirm daily loss/drawdown state tables/entities exist when implemented.
- [ ] Confirm secrets are not stored in runtime tables.
- [ ] Confirm raw exchange payloads, if stored, are redacted.

## Required startup behavior

- [ ] Fresh runtime DB starts in `SAFE_MODE`.
- [ ] Fresh runtime DB has `entries_blocked = true` until gates pass.
- [ ] Existing runtime DB preserves kill switch state across restart.
- [ ] Existing runtime DB preserves operator pause state across restart.
- [ ] Existing runtime DB preserves incident state across restart.
- [ ] Existing runtime DB preserves unknown outcome state across restart.
- [ ] Existing runtime DB requires reconciliation after confidence loss.

## Evidence to save

- [ ] Migration output.
- [ ] DB integrity check output.
- [ ] Redacted table/entity listing.
- [ ] Startup state output showing `SAFE_MODE`.
- [ ] Test output for persisted kill switch / pause / incident state.

## Do not proceed if

- runtime DB cannot initialize,
- migrations fail,
- startup does not enter `SAFE_MODE`,
- kill switch can auto-clear,
- unknown execution state can be forgotten,
- or secrets appear in DB/log output.

---

# Part 6 — Dry-Run Runtime Setup

## Goal

Run Prometheus in live-like orchestration mode without real exchange order placement.

Dry-run is not historical backtesting. It is a runtime rehearsal.

## Required dry-run behavior

Dry-run should exercise:

- runtime startup,
- safe-mode-first behavior,
- market-data flow or simulated completed bars,
- strategy evaluation,
- risk checks,
- fake execution adapter,
- fake fills,
- fake protective stops,
- state transitions,
- runtime DB persistence,
- dashboard state,
- alert routing,
- restart/reconciliation behavior,
- incident handling simulations,
- kill-switch behavior.

## Checklist

- [ ] Confirm dry-run config exists.
- [ ] Confirm dry-run config has:

```text
exchange_write_enabled = false
real_capital_enabled = false
adapter = fake or dry_run
```

- [ ] Start dry-run runtime.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm runtime starts in `SAFE_MODE`.
- [ ] Confirm operator/dashboard can see `SAFE_MODE`.
- [ ] Confirm entries are initially blocked.
- [ ] Confirm fake adapter is active.
- [ ] Confirm no production Binance order endpoint can be reached from dry-run mode.
- [ ] Feed or receive completed BTCUSDT 15m bars.
- [ ] Confirm partial candles do not trigger strategy decisions.
- [ ] Confirm completed bars can trigger strategy evaluation.
- [ ] Confirm fake strategy signal path can produce a candidate entry.
- [ ] Confirm risk layer can approve or reject candidate.
- [ ] Confirm fake entry order lifecycle is simulated.
- [ ] Confirm fake fill lifecycle is simulated.
- [ ] Confirm fake protective stop lifecycle is simulated.
- [ ] Confirm a filled fake position is not considered protected until fake protection is confirmed.
- [ ] Confirm missing fake protective stop creates emergency/blocked behavior.
- [ ] Confirm unknown fake execution outcome blocks entries.
- [ ] Confirm dry-run restart returns to `SAFE_MODE`.
- [ ] Confirm dry-run reconciliation must pass before normal continuation.

## Dry-run failure simulations

Run simulations for:

- [ ] market-data stale while flat,
- [ ] market-data stale while positioned,
- [ ] user-stream stale while flat,
- [ ] user-stream stale while positioned,
- [ ] entry submission timeout/unknown,
- [ ] entry rejected,
- [ ] partial fill ambiguity,
- [ ] stop submission rejected,
- [ ] stop confirmation timeout,
- [ ] stop cancel unknown,
- [ ] multiple protective stops detected,
- [ ] orphaned protective stop while flat,
- [ ] manual/non-bot exposure detected,
- [ ] kill switch activated,
- [ ] restart during in-flight order,
- [ ] restart during active fake position,
- [ ] restart during unknown outcome,
- [ ] emergency flatten simulation.

## Evidence to save

- [ ] Dry-run startup log.
- [ ] Runtime mode output showing `SAFE_MODE` on startup.
- [ ] Fake adapter confirmation.
- [ ] Dry-run trade lifecycle log.
- [ ] Dry-run protective stop lifecycle log.
- [ ] Failure simulation output.
- [ ] Restart/reconciliation output.
- [ ] Dry-run dashboard screenshot without secrets.

## Do not proceed if

- dry-run can place real orders,
- runtime starts directly into healthy/running mode,
- fake filled position is considered protected before stop confirmation,
- unknown outcomes do not block entries,
- restart does not begin in `SAFE_MODE`,
- or failure simulations do not produce safe/blocked behavior.

---

# Part 7 — Dashboard / Local Operator Display Setup

## Goal

Prepare the operator dashboard as a supervision, control, and visibility surface.

The dashboard should be polished and information-rich where useful, but it must not become a discretionary manual trading terminal.

## Required dashboard role

The dashboard should show:

- runtime mode,
- entries allowed/blocked state,
- active pause/kill switch state,
- operator review requirements,
- current symbol and stage,
- open position state,
- open normal orders,
- open algo/protective orders,
- protective stop state,
- unknown execution outcomes,
- stream health,
- reconciliation state,
- incidents,
- alerts,
- daily loss state,
- drawdown state,
- risk state,
- host/NUC health,
- release/config state,
- Telegram/n8n route state,
- recent critical events.

A future TradingView-like candle/setup/trade visualization is allowed for rule verification, but it must remain read-only.

## Checklist

- [ ] Confirm dashboard implementation entrypoint.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Start dashboard locally.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm dashboard can connect to local/dry-run runtime.
- [ ] Confirm dashboard shows runtime mode.
- [ ] Confirm dashboard shows entries blocked/allowed.
- [ ] Confirm dashboard shows fake position state in dry-run.
- [ ] Confirm dashboard shows fake protective stop state in dry-run.
- [ ] Confirm dashboard shows open normal orders.
- [ ] Confirm dashboard shows open algo/protective orders.
- [ ] Confirm dashboard shows market-data stream health.
- [ ] Confirm dashboard shows user-stream/private-state health.
- [ ] Confirm dashboard shows reconciliation state.
- [ ] Confirm dashboard shows incidents and severity.
- [ ] Confirm dashboard shows kill switch state.
- [ ] Confirm dashboard shows alert-route status.
- [ ] Confirm dashboard does not expose secrets.
- [ ] Confirm dashboard does not allow arbitrary manual buy/sell.
- [ ] Confirm dashboard does not allow stop widening.
- [ ] Confirm dashboard does not allow bypassing incidents/reconciliation/kill switch.

## Local display expectations

On the eventual dedicated NUC / mini PC:

- [ ] dashboard is visible whenever the attached desk monitor is on during operation,
- [ ] dashboard can be started after reboot,
- [ ] dashboard makes blocked/safe/emergency states obvious,
- [ ] dashboard does not require exposing secrets on screen,
- [ ] dashboard remains readable from the normal operator viewing distance,
- [ ] emergency actions require deliberate confirmation where allowed.

## Evidence to save

- [ ] Dashboard startup output.
- [ ] Dashboard screenshot in `SAFE_MODE` without secrets.
- [ ] Dashboard screenshot during dry-run fake position without secrets.
- [ ] Dashboard screenshot showing an incident/blocked state without secrets.
- [ ] Confirmation that forbidden manual trading controls are absent.

## Do not proceed if

- dashboard cannot show runtime safety state,
- dashboard hides protective stop state,
- dashboard cannot show incidents,
- dashboard exposes secrets,
- dashboard allows arbitrary manual trading,
- or dashboard can bypass safety gates.

---

# Part 8 — Telegram / n8n Alert Route Setup

## Goal

Configure alert routing so the operator receives critical Prometheus state changes outside the dashboard.

Telegram and/or n8n may be used for alert routing.

They should not initially approve high-risk actions.

## Alerting principles

- Alerts are for visibility, urgency, and review.
- The dashboard remains the primary supervision surface.
- High-risk approvals should not initially be performed through Telegram/n8n.
- Alert secrets must not be committed to git.
- Alerts must not include API secrets, private keys, or unredacted credential material.

## Required alert categories

At minimum, alert routing should support:

- runtime started,
- runtime entered `SAFE_MODE`,
- entries blocked,
- kill switch activated,
- incident opened,
- severity escalated,
- unknown execution outcome,
- position exists without confirmed protection,
- protective stop missing/uncertain,
- user stream stale while exposed,
- reconciliation required,
- emergency flatten branch entered,
- alert route degraded/unavailable,
- backup/restore failure,
- paper/shadow session summary,
- tiny-live session summary when approved.

## Checklist

- [ ] Decide initial alert route:

```text
Telegram only / n8n only / Telegram via n8n / other
```

- [ ] Create non-production alert test route.
- [ ] Store alert secrets outside git.
- [ ] Configure local/dry-run alert settings.
- [ ] Send basic test alert.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm operator receives test alert.
- [ ] Confirm alert message identifies environment/stage.
- [ ] Confirm alert message does not include secrets.
- [ ] Confirm dry-run incident produces alert.
- [ ] Confirm kill switch activation produces alert.
- [ ] Confirm reconciliation-required state produces alert.
- [ ] Confirm alert-route failure is visible on dashboard.
- [ ] Confirm Telegram/n8n cannot approve high-risk actions in v1 initial setup.

## Evidence to save

- [ ] Screenshot of test alert without secrets.
- [ ] Screenshot/log showing alert-route healthy state.
- [ ] Screenshot/log of dry-run incident alert.
- [ ] Screenshot/log of kill switch alert.
- [ ] Redacted alert configuration confirmation.

## Do not proceed if

- alerts are not received,
- alert secrets are stored in git,
- alerts include secrets,
- alert route status is not visible,
- or Telegram/n8n can approve high-risk actions before explicit future approval.

---

# Part 9 — Dedicated NUC / Mini PC Preparation

## Goal

Prepare the default live-capable host: a dedicated local NUC / mini PC used only for Prometheus, with an attached desk monitor showing the dashboard during operation.

## Stage timing

The NUC does not need to be fully live-hardened before local development works.

Recommended timing:

```text
local development setup first
→ dry-run runtime works locally
→ dashboard/alerts work locally
→ prepare NUC for paper/shadow
→ harden NUC before tiny live
```

## Default host requirements

The NUC / mini PC should be:

- dedicated to Prometheus,
- physically controlled by the operator,
- not used as a general-purpose personal computer,
- connected to stable power,
- connected to stable internet,
- time-synchronized,
- backed up,
- able to run the dashboard on attached monitor,
- able to run runtime service/process reliably,
- able to preserve runtime DB/logs across restart,
- able to support emergency operator access.

## Checklist

- [ ] Select NUC / mini PC hardware.
- [ ] Install supported operating system.
- [ ] Create dedicated Prometheus user/account.
- [ ] Disable casual/general-purpose use.
- [ ] Connect attached desk monitor.
- [ ] Confirm monitor can display dashboard clearly.
- [ ] Configure stable network connection.
- [ ] Configure time synchronization.
- [ ] Configure automatic security updates or an approved update policy.
- [ ] Configure firewall baseline.
- [ ] Configure local access policy.
- [ ] Configure SSH only if needed and hardened.
- [ ] Configure repository checkout on NUC.
- [ ] Configure runtime environment on NUC.
- [ ] Configure runtime DB/log directories with correct permissions.
- [ ] Configure backup target.
- [ ] Configure alert route on NUC.
- [ ] Configure dashboard startup behavior.
- [ ] Configure runtime service/process manager when implementation provides service files.

## Evidence to save

- [ ] Host model/spec summary.
- [ ] OS/version output.
- [ ] Time sync status.
- [ ] Firewall status.
- [ ] Runtime user confirmation.
- [ ] Dashboard visible on attached monitor.
- [ ] Service/process startup output.
- [ ] Backup path confirmation.
- [ ] Alert test from NUC.

## Do not proceed if

- NUC is used for unrelated risky activity,
- physical access is uncontrolled,
- time sync is broken,
- internet is unstable,
- dashboard cannot run on monitor,
- backups are not configured,
- secrets are unprotected,
- or runtime DB/log directories are not protected.

---

# Part 10 — Security and Host-Hardening Prechecks

## Goal

Verify that the live-capable host and secrets boundary are safe enough before paper/shadow and especially before tiny live.

## Security checklist

- [ ] Host is dedicated to Prometheus.
- [ ] Host is physically controlled.
- [ ] Host has a dedicated runtime user.
- [ ] Host is updated according to approved policy.
- [ ] Firewall baseline is configured.
- [ ] Remote access is disabled or hardened.
- [ ] SSH keys, if used, are protected.
- [ ] Local login is protected.
- [ ] Disk permissions protect runtime files.
- [ ] Secrets files are readable only by required user/process.
- [ ] Runtime DB is protected from casual access.
- [ ] Logs are protected from casual access.
- [ ] Backups are protected.
- [ ] Dashboard access is controlled.
- [ ] API keys are not stored in docs, git, prompts, screenshots, or logs.
- [ ] Telegram/n8n secrets are not stored in git.
- [ ] `.env` or equivalent secrets file is excluded from git.
- [ ] Redaction behavior is tested.
- [ ] Dependency update process is defined.
- [ ] Emergency key-revocation process is understood.

## Binance account/key prechecks without creating production keys

Before production key creation is allowed, confirm:

- [ ] Binance account security posture is reviewed.
- [ ] Futures account mode requirements are understood.
- [ ] One-way mode requirement is understood.
- [ ] Isolated margin requirement is understood.
- [ ] IP restriction plan is understood.
- [ ] API permission scoping plan is understood.
- [ ] Key storage location is planned.
- [ ] Key revocation procedure is understood.
- [ ] Production key creation is blocked until phase-gate approval.

## Evidence to save

- [ ] Redacted host-hardening checklist output.
- [ ] Redacted file-permission output.
- [ ] Redacted secrets-location confirmation.
- [ ] Redacted dashboard access confirmation.
- [ ] Redacted backup-location confirmation.
- [ ] Written note confirming production keys have not been created yet.

## Do not proceed if

- host is not dedicated for live-capable operation,
- secrets may leak into git/logs/screenshots,
- dashboard access is uncontrolled,
- backups are unprotected,
- key revocation procedure is unclear,
- or production keys were created before approval.

---

# Part 11 — Backup and Restore Verification

## Goal

Prove that runtime state, logs, configs, and operational evidence can survive failure and be restored safely.

Backup is not complete until restore is tested.

## Required backup targets

Backups should cover:

- runtime database,
- runtime logs,
- structured event logs,
- operator action audit logs,
- incident records,
- reconciliation records,
- config files without secrets where appropriate,
- secret files through a secure secrets-backup method if approved,
- release/config references,
- validation reports,
- phase-gate evidence.

## Checklist

- [ ] Define backup source paths.
- [ ] Define backup destination.
- [ ] Define backup frequency.
- [ ] Define retention policy.
- [ ] Define restore location.
- [ ] Confirm backups do not leak secrets to unsafe storage.
- [ ] Run backup command.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Verify backup artifact exists.
- [ ] Run restore test into safe test location.

```text
COMMAND TO BE FILLED BY IMPLEMENTATION
```

- [ ] Confirm restored runtime starts in `SAFE_MODE`.
- [ ] Confirm restored runtime does not assume exchange truth.
- [ ] Confirm restored runtime requires reconciliation before normal operation.
- [ ] Confirm kill switch state survives backup/restore.
- [ ] Confirm incident state survives backup/restore.
- [ ] Confirm unknown outcome state survives backup/restore.

## Evidence to save

- [ ] Backup command output.
- [ ] Backup artifact metadata.
- [ ] Restore test output.
- [ ] Restored runtime `SAFE_MODE` output.
- [ ] Notes on what was and was not backed up.

## Do not proceed if

- backups are untested,
- restore procedure is unclear,
- restored runtime starts as healthy without reconciliation,
- secrets are backed up unsafely,
- or incident/kill-switch/unknown-outcome state is lost.

---

# Part 12 — Paper / Shadow Readiness

## Goal

Prepare for live-like operation without real capital exposure.

Paper/shadow should prove operational behavior, not profitability alone.

## Paper/shadow expectations

Paper/shadow should validate:

- live market-data intake,
- completed-bar strategy timing,
- 1h bias alignment,
- runtime state transitions,
- fake or paper execution lifecycle,
- protective stop lifecycle simulation or paper equivalent,
- dashboard visibility,
- alert routing,
- restart/reconciliation,
- incident handling,
- operator workflow,
- daily/weekly review process.

## Checklist

- [ ] Phase gate allows paper/shadow preparation.
- [ ] Dry-run acceptance evidence is saved.
- [ ] Dashboard is working.
- [ ] Alert route is working.
- [ ] Runtime DB/log persistence is working.
- [ ] Backup/restore test has passed.
- [ ] Dedicated NUC is prepared or paper/shadow host is approved.
- [ ] Paper/shadow config exists.
- [ ] Paper/shadow config cannot place real capital orders unless explicitly approved by a future paper environment design.
- [ ] Runtime starts in `SAFE_MODE`.
- [ ] Operator can observe dashboard during operation.
- [ ] Completed bars drive strategy evaluation.
- [ ] Partial bars are clearly excluded from strategy decisions.
- [ ] Paper/shadow trade decisions are logged.
- [ ] Paper/shadow risk decisions are logged.
- [ ] Paper/shadow protection state is represented.
- [ ] Paper/shadow incidents are represented.
- [ ] Paper/shadow summaries can be exported.

## Minimum paper/shadow run evidence

Before tiny-live consideration, gather:

- [ ] run duration summary,
- [ ] number of completed 15m bars processed,
- [ ] number of signals,
- [ ] number of simulated/paper entries,
- [ ] number of simulated/paper exits,
- [ ] number of stop/protection lifecycle events,
- [ ] strategy no-trade reasons,
- [ ] risk rejection reasons,
- [ ] stream gaps,
- [ ] reconciliation events,
- [ ] incidents,
- [ ] alerts sent,
- [ ] dashboard uptime/visibility notes,
- [ ] restart tests,
- [ ] operator review notes.

## Do not proceed if

- dry-run evidence is missing,
- dashboard/alerts are not reliable,
- runtime cannot restart safely,
- completed-bar timing is not proven,
- paper/shadow state is not persisted,
- incidents are not visible,
- or operator review is skipped.

---

# Part 13 — Production Binance Key Timing

## Goal

Define when production Binance API keys may be created.

## Hard rule

Production trade-capable Binance keys must **not** be created until the correct phase gate approves preparation for tiny live.

Key creation is not a local setup step.

Key creation is a live-capability step.

## Required conditions before production trade-capable key creation

Before production trade-capable keys may be created, all of the following should be true:

- [ ] Phase gate approves tiny-live preparation.
- [ ] Paper/shadow evidence has been reviewed.
- [ ] Dedicated NUC / mini PC is prepared.
- [ ] Host-hardening checks pass.
- [ ] Secrets-management procedure is ready.
- [ ] Permission-scoping plan is ready.
- [ ] IP restriction plan is ready.
- [ ] Backup/restore has been tested.
- [ ] Dashboard is working on the NUC monitor.
- [ ] Telegram/n8n alert route is tested.
- [ ] Emergency access is tested.
- [ ] Kill switch behavior is tested.
- [ ] Restart/reconciliation behavior is tested.
- [ ] Internal notional cap is configured.
- [ ] Initial risk is configured at 0.25% of sizing equity.
- [ ] Effective leverage cap is configured at 2x.
- [ ] One-way mode requirement is verified.
- [ ] Isolated margin requirement is verified.
- [ ] Operator explicitly approves key creation.

## Key creation safety requirements

When approved later, production keys should be created with:

- [ ] minimum required permissions,
- [ ] no withdrawal permission,
- [ ] IP restrictions where supported and approved,
- [ ] clear labeling,
- [ ] documented creation date,
- [ ] documented permission set,
- [ ] documented revocation procedure,
- [ ] secure local storage,
- [ ] no entry into git/docs/prompts/screenshots/logs.

## Evidence to save later

- [ ] Phase-gate approval note.
- [ ] Redacted permission screenshot.
- [ ] Redacted IP restriction screenshot.
- [ ] Redacted key label screenshot.
- [ ] Secure storage confirmation without revealing secret.
- [ ] Revocation procedure note.

## Do not proceed if

- phase gate has not approved,
- host is not hardened,
- IP restriction plan is missing,
- permission scope is unclear,
- secrets storage is unclear,
- dashboard/alerts are not working,
- backup/restore is untested,
- or operator approval is not recorded.

---

# Part 14 — Tiny-Live Readiness

## Goal

Confirm all requirements before first real-capital operation at tiny-live risk.

Tiny live is first real-capital validation. It is not scaled production.

## Tiny-live locked starting policy

Initial tiny-live defaults:

```text
symbol = BTCUSDT
risk_fraction = 0.0025
max_effective_leverage = 2.0
max_positions = 1
max_active_protective_stops = 1
position_mode = one-way
margin_mode = isolated
exchange_write_enabled = explicitly approved only
internal_notional_cap = mandatory
restart_mode = SAFE_MODE
```

## Tiny-live readiness checklist

- [ ] Phase gate approves tiny live.
- [ ] AI coding handoff has been followed.
- [ ] Implementation ambiguity/spec-gap log has no unresolved live blockers.
- [ ] Dry-run evidence has passed review.
- [ ] Paper/shadow evidence has passed review.
- [ ] Validation checklist has passed required gates.
- [ ] Dedicated NUC is ready.
- [ ] Host-hardening passes.
- [ ] Dashboard is visible on attached monitor.
- [ ] Alert route is tested from the NUC.
- [ ] Runtime DB/log paths are protected.
- [ ] Backup/restore is tested.
- [ ] Production Binance key has approved permissions.
- [ ] Production Binance key has no withdrawal permission.
- [ ] Production Binance key is IP-restricted where approved.
- [ ] Secrets are stored securely.
- [ ] Runtime starts in `SAFE_MODE`.
- [ ] Startup reconciliation passes.
- [ ] User stream is healthy.
- [ ] Market-data stream is healthy.
- [ ] Exchange account mode is one-way.
- [ ] BTCUSDT margin mode is isolated.
- [ ] No manual/non-bot exposure exists.
- [ ] No stale open orders exist.
- [ ] No unexpected protective orders exist.
- [ ] Internal notional cap is configured.
- [ ] Initial live risk is 0.25%.
- [ ] Effective leverage cap is 2x.
- [ ] Kill switch is tested and visible.
- [ ] Emergency flatten path is tested in dry-run/paper equivalent.
- [ ] Stop placement behavior has been verified in approved non-real or tiny-live preparation environment.
- [ ] Operator is available and watching during first live run.

## First tiny-live session constraints

- [ ] Operator is present.
- [ ] Dashboard is visible.
- [ ] Alerts are active.
- [ ] No unrelated work is being performed on the NUC.
- [ ] No manual discretionary trades are placed in the same futures account.
- [ ] Do not change risk during the session.
- [ ] Do not change leverage cap during the session.
- [ ] Do not add ETHUSDT live trading.
- [ ] Do not add additional symbols.
- [ ] Do not run multiple strategies.
- [ ] Do not run multiple bots on the account.

## Tiny-live first-session evidence

Save:

- [ ] startup log,
- [ ] reconciliation result,
- [ ] dashboard screenshot before enabling entries,
- [ ] alert-route status,
- [ ] config version,
- [ ] risk config,
- [ ] notional cap,
- [ ] stream health,
- [ ] first signal/no-signal logs,
- [ ] first trade lifecycle if one occurs,
- [ ] protective stop confirmation if a trade occurs,
- [ ] incident logs if any,
- [ ] end-of-session summary,
- [ ] operator notes.

## Do not proceed if

- any tiny-live readiness item is missing,
- operator cannot supervise,
- dashboard is not visible,
- alerts are not working,
- account mode/margin mode is wrong,
- unknown exposure exists,
- kill switch is active and unresolved,
- reconciliation is incomplete,
- production key permissions are unclear,
- or internal notional cap is missing.

---

# Part 15 — Emergency Access and Recovery Readiness

## Goal

Ensure the operator can respond to urgent conditions before any live-capable operation.

## Emergency conditions to prepare for

- position exists without confirmed protective stop,
- protective stop rejected,
- protective stop status unknown,
- entry submission outcome unknown,
- stop replacement ambiguity,
- user stream stale while exposed,
- REST reconciliation unavailable while exposed,
- local/exchange position mismatch,
- multiple stops detected,
- orphaned stop detected,
- manual/non-bot exposure detected,
- suspected credential compromise,
- host compromise,
- dashboard unavailable,
- alert route unavailable,
- power/internet outage,
- NUC crash/reboot,
- runtime DB unavailable,
- backup restore needed.

## Checklist

- [ ] Operator knows how to view Binance account state directly.
- [ ] Operator knows how to check open BTCUSDT position directly.
- [ ] Operator knows how to check open normal orders directly.
- [ ] Operator knows how to check open algo/protective orders directly.
- [ ] Operator knows how to revoke API key.
- [ ] Operator knows how to activate Prometheus kill switch.
- [ ] Operator knows how to stop the runtime process/service.
- [ ] Operator knows how to restart the runtime into `SAFE_MODE`.
- [ ] Operator knows where runtime DB is stored.
- [ ] Operator knows where logs are stored.
- [ ] Operator knows where backups are stored.
- [ ] Operator knows how to capture dashboard/log evidence without revealing secrets.
- [ ] Operator knows how to contact alert route if needed.
- [ ] Operator understands that emergency flattening is a safety action, not discretionary trading.

## Emergency action boundaries

While kill switch or emergency state is active, allowed actions may include:

- exchange state reads,
- reconciliation,
- stop restoration if deterministic and safe,
- risk-reducing stop repair,
- stale order cancellation,
- emergency flattening through approved path,
- logging,
- operator review,
- key revocation if security concern exists.

Forbidden actions include:

- new strategy entries,
- adding to exposure,
- reversing exposure,
- discretionary stop widening,
- bypassing reconciliation,
- clearing kill switch without review,
- ignoring unknown execution outcome.

## Evidence to save

- [ ] Emergency access notes.
- [ ] Runtime stop/start test output.
- [ ] Kill-switch activation/clearance test in non-live mode.
- [ ] Redacted Binance account-state navigation notes.
- [ ] Key-revocation procedure notes.
- [ ] Backup restore drill output.

## Do not proceed if

- operator cannot access account state,
- operator cannot activate kill switch,
- operator cannot stop/restart runtime,
- key revocation is unclear,
- logs/DB/backups cannot be found,
- or emergency procedures are untested.

---

# Part 16 — First-Run Acceptance Checklist

## Goal

Define the minimum acceptance criteria for the first full setup run.

This does not approve tiny live by itself.

It proves the setup path is coherent.

## Acceptance checklist

- [ ] Repository is correctly cloned at `C:\Prometheus`.
- [ ] GitHub Desktop tracks the correct repo.
- [ ] AntiGravity IDE opens the correct repo folder.
- [ ] Claude Code extension is logged in and ready.
- [ ] Documentation handoff files exist.
- [ ] Python/tooling environment is installed.
- [ ] Dependencies install successfully.
- [ ] Unit tests pass or failures are documented as blockers.
- [ ] Lint/type checks pass or failures are documented as blockers.
- [ ] Local safe config exists.
- [ ] Local config disables exchange-write capability.
- [ ] Runtime DB initializes.
- [ ] Runtime starts in `SAFE_MODE`.
- [ ] Runtime persists safety/control state.
- [ ] Dry-run runtime works with fake adapter.
- [ ] Dry-run unknown execution outcome blocks entries.
- [ ] Dry-run missing protective stop creates emergency/blocked behavior.
- [ ] Dashboard starts locally.
- [ ] Dashboard shows runtime mode and blocked state.
- [ ] Dashboard shows position/protection state in dry-run.
- [ ] Dashboard does not expose secrets.
- [ ] Dashboard does not allow arbitrary manual trading.
- [ ] Alert test succeeds.
- [ ] Backup test succeeds.
- [ ] Restore test succeeds into `SAFE_MODE`.
- [ ] No production trade-capable Binance keys have been created before approval.
- [ ] All unresolved setup issues are logged.

## Setup accepted when

All required items above are either:

```text
PASS
```

or explicitly recorded as:

```text
BLOCKER — must resolve before next phase
```

No safety-critical item may be silently skipped.

---

# Part 17 — Evidence to Save Before Promotion

## Goal

Define the evidence bundle that should be saved before moving to the next stage.

## Local development evidence

Save:

- [ ] repository status,
- [ ] Python version,
- [ ] dependency install output,
- [ ] test output,
- [ ] lint/type-check output,
- [ ] config validation output,
- [ ] known blockers.

## Data/research evidence

Save:

- [ ] dataset manifest,
- [ ] data completeness report,
- [ ] BTCUSDT summary,
- [ ] ETHUSDT summary,
- [ ] invalid-window report,
- [ ] exchange metadata snapshot,
- [ ] funding-rate coverage summary.

## Runtime/dry-run evidence

Save:

- [ ] runtime startup log,
- [ ] `SAFE_MODE` confirmation,
- [ ] fake adapter confirmation,
- [ ] dry-run lifecycle log,
- [ ] failure simulation results,
- [ ] restart/reconciliation output,
- [ ] runtime DB integrity output.

## Dashboard/alert evidence

Save:

- [ ] dashboard `SAFE_MODE` screenshot,
- [ ] dashboard dry-run position/protection screenshot,
- [ ] dashboard incident screenshot,
- [ ] alert test screenshot,
- [ ] alert route health output.

## Host/security evidence

Save:

- [ ] NUC host summary,
- [ ] OS/version output,
- [ ] time sync output,
- [ ] firewall output,
- [ ] file permission confirmation,
- [ ] backup/restore output,
- [ ] redacted secrets-location confirmation,
- [ ] note confirming production keys have not been created before approval.

## Paper/shadow evidence

Save:

- [ ] run duration,
- [ ] completed bars processed,
- [ ] signals/no-signals,
- [ ] simulated entries/exits,
- [ ] risk decisions,
- [ ] protection lifecycle events,
- [ ] incidents,
- [ ] alerts,
- [ ] dashboard uptime notes,
- [ ] restart/reconciliation tests,
- [ ] operator review notes.

## Tiny-live evidence later

Save only after approved tiny-live operation:

- [ ] phase-gate approval,
- [ ] startup reconciliation,
- [ ] dashboard before enabling entries,
- [ ] config/risk/notional-cap snapshot without secrets,
- [ ] first live trade lifecycle if any,
- [ ] protective stop confirmation if trade occurs,
- [ ] incident logs if any,
- [ ] end-of-session review.

---

# Part 18 — Working With ChatGPT During Setup

## Goal

Define the assisted setup workflow for the operator.

The operator may use ChatGPT to inspect setup evidence and guide installation step by step.

## Recommended workflow

At each setup step, the operator may provide:

- screenshots,
- terminal output,
- GitHub Desktop state,
- IDE state,
- logs,
- dashboard screenshots,
- photos of the NUC/monitor setup,
- redacted config snippets,
- redacted alert screenshots,
- error messages,
- test output,
- phase-gate evidence.

## Redaction rules before sharing

Before sharing screenshots or logs, remove or hide:

- Binance API keys,
- API secrets,
- request signatures,
- Telegram bot tokens,
- n8n webhook secrets,
- dashboard passwords,
- SSH private keys,
- recovery codes,
- seed phrases,
- private account identifiers where unnecessary,
- any live credential material.

## Chat-assisted setup rules

- [ ] Share one problem or checkpoint at a time when possible.
- [ ] Include the stage/environment being tested.
- [ ] Include exact command output when safe.
- [ ] Include screenshots when UI state matters.
- [ ] Redact secrets before sharing.
- [ ] Do not proceed past unclear safety output.
- [ ] Record unresolved issues in the ambiguity/spec-gap or technical-debt log.

## Do not proceed if

- output is unclear and safety-relevant,
- secrets appear in logs or screenshots,
- the runtime appears to enable live writes unexpectedly,
- or an installation step contradicts phase-gate policy.

---

# Related Documents

This checklist should be read with:

```text
docs/00-meta/current-project-state.md
docs/00-meta/ai-coding-handoff.md
docs/12-roadmap/phase-gates.md
docs/12-roadmap/technical-debt-register.md
docs/08-architecture/deployment-model.md
docs/08-architecture/implementation-blueprint.md
docs/08-architecture/state-model.md
docs/08-architecture/runtime-persistence-spec.md
docs/08-architecture/database-design.md
docs/08-architecture/event-flows.md
docs/04-data/data-requirements.md
docs/04-data/historical-data-spec.md
docs/04-data/live-data-spec.md
docs/04-data/timestamp-policy.md
docs/05-backtesting-validation/v1-breakout-validation-checklist.md
docs/06-execution-exchange/exchange-adapter-design.md
docs/06-execution-exchange/user-stream-reconciliation.md
docs/06-execution-exchange/failure-recovery.md
docs/07-risk/position-sizing-framework.md
docs/07-risk/exposure-limits.md
docs/07-risk/stop-loss-policy.md
docs/07-risk/kill-switches.md
docs/09-operations/restart-procedure.md
docs/09-operations/incident-response.md
docs/09-operations/operator-workflow.md
docs/09-operations/release-process.md
docs/09-operations/rollback-procedure.md
docs/10-security/api-key-policy.md
docs/10-security/secrets-management.md
docs/10-security/permission-scoping.md
docs/10-security/host-hardening.md
docs/10-security/disaster-recovery.md
docs/11-interface/operator-dashboard-requirements.md
docs/11-interface/dashboard-metrics.md
docs/11-interface/alerting-ui.md
```

---

# Final Note

This checklist does not approve live trading.

It prepares the operator and implementation environment for staged setup.

Live exchange-write capability requires phase-gate evidence, clean safety state, approved host/security posture, successful dry-run and paper/shadow operation, and explicit operator approval.
