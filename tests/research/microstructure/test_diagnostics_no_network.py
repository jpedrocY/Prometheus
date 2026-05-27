"""Phase 4bm-W static no-network / no-credential / no-MCP scan.

Scans the three new Phase 4bm-W diagnostics source modules + the Phase 4bm-W
runner script for forbidden imports, credential-shaped tokens, and MCP /
Graphify references in code (excluding docstrings / comments). Confirms the
descriptive diagnostics surface is inert with respect to network, credentials,
and execution side-channels.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = REPO_ROOT / "src" / "prometheus" / "research" / "microstructure"
SCRIPTS_ROOT = REPO_ROOT / "scripts"

PHASE_4BM_W_MODULES: tuple[str, ...] = (
    "diagnostics_split_policy_v002.py",
    "descriptive_diagnostics_v002.py",
    "diagnostics_report_v002.py",
)

PHASE_4BM_W_SCRIPTS: tuple[str, ...] = (
    "phase4bm_w_run_descriptive_diagnostics.py",
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
    ("os.environ-secret", r"\bos\.environ\b"),
    ("getenv", r"\bgetenv\s*\("),
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


def _phase_4bm_w_files() -> list[Path]:
    files = [PACKAGE_ROOT / name for name in PHASE_4BM_W_MODULES]
    files += [SCRIPTS_ROOT / name for name in PHASE_4BM_W_SCRIPTS]
    return files


@pytest.mark.parametrize("module_path", _phase_4bm_w_files(), ids=lambda p: p.name)
def test_phase_4bm_w_module_has_no_forbidden_imports(module_path: Path) -> None:
    text = module_path.read_text(encoding="utf-8")
    stripped = _strip_docstrings_and_comments(text)
    for label, pattern in FORBIDDEN_IMPORT_PATTERNS:
        if re.search(pattern, stripped, flags=re.MULTILINE):
            pytest.fail(
                f"{module_path.name} contains forbidden import / reference matching "
                f"{label!r} ({pattern}) in code (not in docstrings)"
            )


_DENY_TOKENS: tuple[str, ...] = (
    "api_key", "secret", "signature", "listenKey", "userDataStream",
    "/fapi/v1/order", "/fapi/v2/account", "/fapi/v2/positionRisk",
    "/fapi/v1/leverage", "/fapi/v1/marginType", "/fapi/v1/forceOrders",
    "Graphify", "MCP", ".mcp.json",
)

_DOT_ENV_RE = re.compile(r"\.env(?![A-Za-z0-9_])")


def test_phase_4bm_w_modules_have_no_credential_tokens_in_code() -> None:
    for module_path in _phase_4bm_w_files():
        text = module_path.read_text(encoding="utf-8")
        code = _strip_docstrings_and_comments(text)
        for token in _DENY_TOKENS:
            assert token not in code, (
                f"{module_path.name} code (excluding docstrings/comments) must not "
                f"contain forbidden token {token!r}"
            )
        assert not _DOT_ENV_RE.search(code), (
            f"{module_path.name} code (excluding docstrings/comments) must not "
            f"reference any '.env' file (word-boundary match)"
        )


def test_phase_4bm_w_module_files_exist() -> None:
    for module_path in _phase_4bm_w_files():
        assert module_path.exists(), f"missing module: {module_path}"
