"""Phase 4bj-E label-gate static no-network / no-credential scan.

This test complements the existing parametrised
``test_import_boundaries.py`` scan (which globs every ``*.py`` under
``src/prometheus/research/microstructure/``) by explicitly listing the
four new Phase 4bj-E modules and asserting that they do not import any
networking, credential, MCP, or Graphify symbols, and that they do not
contain credential-shaped tokens or private-endpoint paths in their
source bodies.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "src"
    / "prometheus"
    / "research"
    / "microstructure"
)

PHASE_4BJ_E_MODULES: tuple[str, ...] = (
    "label_gate_io.py",
    "label_gate_checks.py",
    "label_gate_report.py",
    "label_gate.py",
)

FORBIDDEN_IMPORT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("prometheus.runtime", r"^\s*(?:from|import)\s+prometheus\.runtime\b"),
    ("prometheus.execution", r"^\s*(?:from|import)\s+prometheus\.execution\b"),
    ("prometheus.persistence", r"^\s*(?:from|import)\s+prometheus\.persistence\b"),
    ("requests", r"^\s*(?:from|import)\s+requests\b"),
    ("httpx", r"^\s*(?:from|import)\s+httpx\b"),
    ("aiohttp", r"^\s*(?:from|import)\s+aiohttp\b"),
    ("websockets", r"^\s*(?:from|import)\s+websockets\b"),
    ("binance", r"^\s*(?:from|import)\s+binance\b"),
    ("dotenv", r"^\s*(?:from|import)\s+dotenv\b"),
    ("python-dotenv", r"^\s*(?:from|import)\s+python_dotenv\b"),
    ("urllib.request", r"^\s*(?:from|import)\s+urllib\.request\b"),
    ("urllib3", r"^\s*(?:from|import)\s+urllib3\b"),
    ("socket", r"^\s*(?:from|import)\s+socket\b"),
    ("os.environ-read", r"\bos\.environ\b"),
    ("getenv", r"\bgetenv\s*\("),
)

FORBIDDEN_CONTENT_TOKENS: tuple[str, ...] = (
    "api_key",
    "secret",
    "signature",
    "listenKey",
    "userDataStream",
    "/fapi/v1/order",
    "/fapi/v2/account",
    "/fapi/v2/positionRisk",
    "/fapi/v1/leverage",
    "/fapi/v1/marginType",
    "/fapi/v1/forceOrders",
    ".env",
    "Graphify",
    "MCP",
    ".mcp.json",
)


_TRIPLE_DQ = re.compile(r'""".*?"""', flags=re.DOTALL)
_TRIPLE_SQ = re.compile(r"'''.*?'''", flags=re.DOTALL)


def _strip_docstrings_and_comments(text: str) -> str:
    text = _TRIPLE_DQ.sub("", text)
    text = _TRIPLE_SQ.sub("", text)
    out: list[str] = []
    for line in text.splitlines():
        idx = line.find("#")
        if idx >= 0:
            out.append(line[:idx])
        else:
            out.append(line)
    return "\n".join(out)


@pytest.mark.parametrize("module_name", PHASE_4BJ_E_MODULES)
def test_phase_4bj_e_module_has_no_forbidden_imports(module_name: str) -> None:
    module_path = PACKAGE_ROOT / module_name
    assert module_path.exists(), f"missing module: {module_path}"
    text = module_path.read_text(encoding="utf-8")
    stripped = _strip_docstrings_and_comments(text)
    for label, pattern in FORBIDDEN_IMPORT_PATTERNS:
        if re.search(pattern, stripped, flags=re.MULTILINE):
            pytest.fail(
                f"{module_name} contains forbidden import / reference "
                f"matching {label!r} ({pattern}) in code (not docstrings)"
            )


@pytest.mark.parametrize("module_name", PHASE_4BJ_E_MODULES)
def test_phase_4bj_e_module_has_no_forbidden_content_tokens(
    module_name: str,
) -> None:
    module_path = PACKAGE_ROOT / module_name
    text = module_path.read_text(encoding="utf-8")
    code = _strip_docstrings_and_comments(text)
    for token in FORBIDDEN_CONTENT_TOKENS:
        assert token not in code, (
            f"{module_name} code (excluding docstrings/comments) must not "
            f"contain token {token!r}"
        )


def test_existing_import_boundaries_scan_will_pick_up_new_modules() -> None:
    """Sentinel: the existing ``test_import_boundaries.py`` scan
    parametrises over every ``*.py`` under ``PACKAGE_ROOT``, which means
    the four new Phase 4bj-E modules are also scanned by the existing
    suite. This sentinel test asserts that the four files exist so a
    silent miss surfaces here too.
    """
    for module_name in PHASE_4BJ_E_MODULES:
        p = PACKAGE_ROOT / module_name
        assert p.is_file(), f"missing: {p}"
