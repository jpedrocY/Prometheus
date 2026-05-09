"""Phase 4bb-C boundary tests: gate is offline-only.

The gate must:
- not import any networking library (no ``requests`` / ``httpx`` /
  ``aiohttp`` / ``websockets`` / ``binance`` / ``dotenv`` / ``urllib3``);
- not open any socket;
- not read ``.env`` or ``.mcp.json``;
- run cleanly when ``socket.socket`` is monkey-patched to raise.
"""

from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
from _eligibility_fixtures import build_happy_fixture  # noqa: E402

from prometheus.research.microstructure import (  # noqa: E402
    AggTradesEligibilityGateInput,
    GateIOError,
    run_eligibility_gate,
)
from prometheus.research.microstructure.eligibility_io import (  # noqa: E402
    assert_no_dangerous_imports_loaded,
)

_FORBIDDEN_MODULE_NAMES = (
    "requests",
    "httpx",
    "aiohttp",
    "websockets",
    "binance",
    "dotenv",
    "python_dotenv",
    "urllib3",
)


def test_assert_no_dangerous_imports_loaded_returns_when_forbidden_absent(
    monkeypatch,
) -> None:
    """The runtime guard succeeds when no forbidden module is in sys.modules.

    Other test suites in the same pytest session can legitimately import
    networking libraries (e.g. ``httpx``) for unrelated reasons. The
    runtime guard is therefore not invoked by the orchestrator; the
    static import-boundary scan is the binding contract for the gate's
    own modules. This test sanity-checks the guard in a clean state.
    """
    forbidden_now_loaded = [
        n
        for n in (
            "requests",
            "httpx",
            "aiohttp",
            "websockets",
            "binance",
            "dotenv",
            "python_dotenv",
        )
        if n in sys.modules
    ]
    for name in forbidden_now_loaded:
        monkeypatch.delitem(sys.modules, name, raising=False)
    assert_no_dangerous_imports_loaded()


def test_gate_modules_do_not_import_forbidden_modules_statically() -> None:
    """Static scan: none of the four new modules should reference networking libs."""
    forbidden_substrings = (
        "import requests",
        "import httpx",
        "import aiohttp",
        "import websockets",
        "import urllib.request",
        "import urllib3",
        "import socket",
        "from binance",
        "from dotenv",
        "import dotenv",
        "import python_dotenv",
        "os.environ",
        "os.getenv",
        "load_dotenv",
        ".env",
        ".mcp.json",
    )
    pkg_dir = (
        Path(__file__).resolve().parents[3]
        / "src"
        / "prometheus"
        / "research"
        / "microstructure"
    )
    targets = [
        pkg_dir / "eligibility_gate.py",
        pkg_dir / "eligibility_checks.py",
        pkg_dir / "eligibility_report.py",
        pkg_dir / "eligibility_io.py",
    ]
    for path in targets:
        assert path.exists(), f"missing module: {path}"
        text = path.read_text(encoding="utf-8")
        # Strip docstrings via a simple heuristic: split by '"""' and discard
        # alternating sections. This is good enough for the import-boundary
        # scan and avoids false positives in module docstrings.
        sanitized = _strip_python_docstrings(text)
        for needle in forbidden_substrings:
            assert needle not in sanitized, (
                f"forbidden token {needle!r} reachable in {path.name}"
            )


def _strip_python_docstrings(text: str) -> str:
    parts = text.split('"""')
    keep = []
    for i, p in enumerate(parts):
        if i % 2 == 0:
            keep.append(p)
    return "".join(keep)


def test_gate_runs_with_socket_socket_patched_to_raise(monkeypatch, tmp_path: Path) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)

    def _explode(*_a, **_kw):
        raise OSError("socket use forbidden in offline gate")

    monkeypatch.setattr(socket, "socket", _explode)

    res = run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    # The gate completed without ever touching socket.socket.
    assert len(res.checks) == 45


def test_assert_no_dangerous_imports_loaded_raises_when_forbidden_present() -> None:
    """If ``requests`` is artificially placed in ``sys.modules``, the guard fails."""
    sentinel = object()
    sys.modules["requests"] = sentinel  # type: ignore[assignment]
    try:
        with pytest.raises(GateIOError):
            assert_no_dangerous_imports_loaded()
    finally:
        del sys.modules["requests"]


def test_no_env_variable_read_during_gate(monkeypatch, tmp_path: Path) -> None:
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    fb = build_happy_fixture(tmp_path, code_commit_sha=sha)

    import os

    accessed: list[str] = []
    real_getitem = os.environ.__class__.__getitem__

    def _record_get(self, key):
        accessed.append(str(key))
        return real_getitem(self, key)

    monkeypatch.setattr(os.environ.__class__, "__getitem__", _record_get)

    run_eligibility_gate(
        AggTradesEligibilityGateInput(
            manifest_path=fb.manifest_path,
            output_root=fb.output_root,
            code_commit_sha=sha,
            write_report=False,
        )
    )
    # The gate itself must not read environment variables. (subprocess.run
    # may consult environ internally in the standard library, but the gate's
    # own code path does not look up named env vars.)
    forbidden_names = {"BINANCE_API_KEY", "BINANCE_API_SECRET", "MCP_TOKEN"}
    leaked = forbidden_names.intersection(accessed)
    assert not leaked


def test_no_mcp_or_graphify_or_dotenv_imported_after_gate() -> None:
    # The gate run can be invoked elsewhere; we just confirm post-import
    # state has none of the canonical forbidden modules present.
    for name in ("mcp", "Graphify", "dotenv", "python_dotenv"):
        assert name not in sys.modules
