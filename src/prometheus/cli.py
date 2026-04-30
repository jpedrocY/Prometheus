"""Phase 4a read-only CLI entrypoint.

Usage::

    python -m prometheus.cli inspect-runtime --db PATH

Prints the current runtime control state from a SQLite database file.
The CLI is intentionally minimal: only a read-only ``inspect-runtime``
subcommand exists. Phase 4a does NOT implement any subcommand that
would mutate live exchange state, place orders, cancel orders, or
modify a kill switch from the CLI; control mutations belong to the
operator workflow proper, which is out of scope for Phase 4a.
"""

from __future__ import annotations

import argparse
import sys

from prometheus.core.time import utc_now_ms
from prometheus.operator.state_view import format_state_view
from prometheus.persistence.runtime_store import RuntimeStore
from prometheus.state.control import fresh_control_state


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prometheus",
        description=(
            "Phase 4a local read-only CLI. Local-only / fake-exchange / "
            "dry-run / exchange-write-free."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser(
        "inspect-runtime",
        help="Print the current runtime control state from a local SQLite DB",
    )
    inspect.add_argument(
        "--db",
        required=True,
        help="Path to the runtime SQLite database file",
    )
    inspect.add_argument(
        "--allow-empty",
        action="store_true",
        help=(
            "If set and the DB contains no persisted runtime control row, "
            "print a fresh SAFE_MODE view rather than exiting non-zero."
        ),
    )
    return parser


def _cmd_inspect_runtime(args: argparse.Namespace) -> int:
    store = RuntimeStore(args.db)
    store.initialize()
    persisted = store.load_persisted()
    if persisted is None:
        if not args.allow_empty:
            sys.stderr.write(
                "no persisted runtime control row found; pass --allow-empty "
                "to print a fresh SAFE_MODE view\n"
            )
            return 2
        control = fresh_control_state(utc_now_ms())
    else:
        # Per Phase 3x §9.2, the runtime never auto-resumes from a persisted
        # RUNNING mode. The CLI is informational, however, and prints the
        # raw persisted record for the operator's inspection. The operator
        # can see whether a stale RUNNING row exists; the runtime layer is
        # responsible for resetting it on the next live process start.
        control = persisted
    sys.stdout.write(format_state_view(control=control))
    sys.stdout.write("\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "inspect-runtime":
        return _cmd_inspect_runtime(args)
    parser.print_help()
    return 2


if __name__ == "__main__":  # pragma: no cover - exercised via tests
    sys.exit(main())
