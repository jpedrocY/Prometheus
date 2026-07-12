"""Phase 4bn-AR — Fixed Long-Horizon Baseline Run + Preregistered Verdict (CLI).

Thin orchestrator around
``prometheus.research.microstructure.longhorizon_fixed_baseline_run_v001``. It runs
the three frozen baseline families (majority / persistence /
L2-multinomial-logistic) **once each**, per authorized horizon (5m primary; 30m/1h
secondary diagnostics), over the verified Phase 4bn-AQ long-horizon dataset
specification, and records exactly one Phase 4bn-AP §25 verdict
(``CONTINUE_ONE_BOUNDED_FOLLOWUP`` / ``INVESTIGATE_AMBIGUOUS`` /
``STOP_LONGHORIZON_ML_ARC``) under the frozen Phase 4bn-AE §16 thresholds. Compact
JSON artefacts + Phase 4bb-F ``.sha256`` sidecars are written to the single
authorized local/gitignored namespace
``data/research/microstructure/ml_baselines/longhorizon_pre_v001_fixed_run/``.

Strict scope — this script does NOT and MUST NOT: run a fourth model / tree /
neural / ensemble; search models / features / hyperparameters / thresholds / seeds
/ epochs; perform cross-validation / calibration training / probability
recalibration / confidence-threshold selection; write row-level predictions; run
strategy / signals / PnL / backtests; mutate the AH / AJ / AN / AQ namespaces or
any frozen v002 family / manifest / gate / sidecar / split file; read the v002
terminal window, any sealed-test date, or any test row; rerun the AQ / AN / AH
builders; acquire data or call endpoints; commit any data / model artefact; flip
eligibility; or authorize any successor phase. All source bindings are verified
before any data read; any pre-run / alignment / numerical / output-guard breach
fails closed.

Usage:
    python scripts/phase4bn_ar_run_fixed_longhorizon_baselines.py --dry-run
    python scripts/phase4bn_ar_run_fixed_longhorizon_baselines.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPTS_DIR.parent
_SRC_DIR = _REPO_ROOT / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from prometheus.research.microstructure import (  # noqa: E402
    longhorizon_fixed_baseline_run_v001 as run_mod,
)

PHASE_ID = "4bn-AR"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Phase 4bn-AR fixed long-horizon baseline run (single run)"
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "verify the 7 AQ artefacts + 14 sidecars, source bindings, 550 "
            "per-parquet sidecars, dataset-contract-hash, and the budget preflight, "
            "but train nothing, read no rows, and write nothing"
        ),
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="suppress per-partition progress output",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.dry_run:
        summary = run_mod.verify_preflight(progress=not args.quiet)
    else:
        summary = run_mod.run(progress=not args.quiet)
    print(f"[{PHASE_ID}] DONE")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
