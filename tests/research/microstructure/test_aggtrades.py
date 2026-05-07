"""Tests for the aggTrades-only collector skeleton (Phase 4ax)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path

import pytest

from prometheus.research.microstructure.aggtrades import (
    AggTradeMode,
    AggTradePlan,
    AggTradePlanError,
    AggTradesError,
    AggTradeValidationError,
    TakerSide,
    assert_aggtrades_endpoint_allowed,
    build_aggtrades_plan,
    validate_aggtrade_payload,
    write_validated_aggtrades_to_path,
)
from prometheus.research.microstructure.allowlist import EndpointNotAllowedError
from prometheus.research.microstructure.raw_writer import RawWriterPathError

# --------------------------------------------------------------------------- #
# Payload fixtures
# --------------------------------------------------------------------------- #


def _rest_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "a": 12345,
        "p": "27000.50",
        "q": "0.001",
        "f": 1000,
        "l": 1002,
        "T": 1_700_000_000_000,
        "m": False,
    }
    base.update(overrides)
    return base


def _stream_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "e": "aggTrade",
        "E": 1_700_000_000_010,
        "s": "BTCUSDT",
        "a": 12345,
        "p": "27000.50",
        "q": "0.001",
        "f": 1000,
        "l": 1002,
        "T": 1_700_000_000_000,
        "m": True,
    }
    base.update(overrides)
    return base


# --------------------------------------------------------------------------- #
# Payload validation
# --------------------------------------------------------------------------- #


def test_valid_rest_payload_validates() -> None:
    p = validate_aggtrade_payload(_rest_payload())
    assert p.aggregate_trade_id == 12345
    assert p.price == Decimal("27000.50")
    assert p.quantity == Decimal("0.001")
    assert p.first_trade_id == 1000
    assert p.last_trade_id == 1002
    assert p.trade_time_ms == 1_700_000_000_000
    assert p.buyer_is_maker is False
    assert p.taker_side is TakerSide.BUY
    assert p.event_time_ms is None


def test_valid_stream_payload_validates_with_event_time() -> None:
    p = validate_aggtrade_payload(_stream_payload())
    assert p.event_time_ms == 1_700_000_000_010
    assert p.buyer_is_maker is True
    assert p.taker_side is TakerSide.SELL
    # Stream-only fields end up in extra_fields.
    assert "e" in p.extra_fields
    assert p.extra_fields["s"] == "BTCUSDT"


def test_missing_required_field_fails() -> None:
    payload = _rest_payload()
    del payload["p"]
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(payload)


def test_invalid_price_fails() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(p="-1.0"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(p="0"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(p="not-a-number"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(p=""))


def test_invalid_quantity_fails() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(q="0"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(q="-0.001"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(q="bad"))


def test_invalid_trade_id_ordering_fails() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(f=2000, l=1000))


def test_invalid_trade_time_fails() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(T=0))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(T=-1))


def test_invalid_buyer_is_maker_type_fails() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(m="true"))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_rest_payload(m=1))


def test_invalid_event_time_fails_when_present() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_stream_payload(E=0))
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload(_stream_payload(E=-5))


def test_extra_fields_preserved() -> None:
    p = validate_aggtrade_payload(_rest_payload(extra_marker="phase-4ax"))
    assert p.extra_fields["extra_marker"] == "phase-4ax"


def test_payload_must_be_mapping() -> None:
    with pytest.raises(AggTradeValidationError):
        validate_aggtrade_payload("not-a-mapping")  # type: ignore[arg-type]


def test_int_shaped_string_fields_accepted() -> None:
    p = validate_aggtrade_payload(
        _rest_payload(a="42", f="100", l="200", T="1700000000000")
    )
    assert p.aggregate_trade_id == 42
    assert p.first_trade_id == 100
    assert p.last_trade_id == 200
    assert p.trade_time_ms == 1_700_000_000_000


# --------------------------------------------------------------------------- #
# Taker side derivation
# --------------------------------------------------------------------------- #


def test_taker_side_buy_when_buyer_is_not_maker() -> None:
    p = validate_aggtrade_payload(_rest_payload(m=False))
    assert p.taker_side is TakerSide.BUY


def test_taker_side_sell_when_buyer_is_maker() -> None:
    p = validate_aggtrade_payload(_rest_payload(m=True))
    assert p.taker_side is TakerSide.SELL


# --------------------------------------------------------------------------- #
# Endpoint allowlist enforcement
# --------------------------------------------------------------------------- #


def test_allowlist_accepts_rest_aggtrades() -> None:
    assert_aggtrades_endpoint_allowed("https://fapi.binance.com/fapi/v1/aggTrades")


def test_allowlist_accepts_ws_aggtrade() -> None:
    assert_aggtrades_endpoint_allowed("wss://fstream.binance.com/ws/btcusdt@aggTrade")


def test_allowlist_accepts_logical_label() -> None:
    assert_aggtrades_endpoint_allowed("aggtrade_ws")


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://fapi.binance.com/fapi/v1/order",
        "https://fapi.binance.com/fapi/v1/openOrders",
        "https://fapi.binance.com/fapi/v1/forceOrders",
        "https://fapi.binance.com/fapi/v2/account",
        "https://fapi.binance.com/fapi/v2/positionRisk",
        "https://fapi.binance.com/fapi/v1/leverage",
        "https://fapi.binance.com/fapi/v1/marginType",
        "https://fapi.binance.com/fapi/v1/listenKey",
        "wss://fstream.binance.com/ws/userDataStream",
        "api_key=ABC",
        "X-MBX-APIKEY: header",
        "/path/to/.mcp.json",
    ],
)
def test_allowlist_denylist_dominance(endpoint: str) -> None:
    with pytest.raises(EndpointNotAllowedError):
        assert_aggtrades_endpoint_allowed(endpoint)


def test_allowlist_rejects_non_aggtrades_public_endpoint() -> None:
    # bookTicker is public-only and on the Phase 4aw allowlist, but it
    # is not aggTrades-shaped, so the aggTrades-specific guard rejects it.
    with pytest.raises(EndpointNotAllowedError):
        assert_aggtrades_endpoint_allowed(
            "wss://fstream.binance.com/ws/btcusdt@bookTicker"
        )


# --------------------------------------------------------------------------- #
# Dry-run plan
# --------------------------------------------------------------------------- #


def test_dry_run_archive_plan_does_not_create_directories(tmp_path: Path) -> None:
    nonexistent_root = tmp_path / "should-not-exist"
    plan = build_aggtrades_plan(
        symbol="BTCUSDT",
        mode=AggTradeMode.ARCHIVE,
        start_time_ms=1_700_000_000_000,
        end_time_ms=1_700_000_001_000,
        output_root=str(nonexistent_root),
    )
    assert isinstance(plan, AggTradePlan)
    assert plan.symbol == "BTCUSDT"
    assert plan.mode is AggTradeMode.ARCHIVE
    assert plan.capture_mode_label == "historical_archive"
    assert plan.dataset_family == "microstructure_raw_aggtrades_v001"
    # Directory must NOT have been created.
    assert not nonexistent_root.exists()


def test_dry_run_rest_plan_does_not_call_endpoints() -> None:
    plan = build_aggtrades_plan(symbol="ETHUSDT", mode="rest")
    assert plan.mode is AggTradeMode.REST
    assert plan.endpoint_reference == "/fapi/v1/aggTrades"
    assert plan.capture_mode_label == "rest_polling"


def test_dry_run_ws_plan_does_not_open_websockets() -> None:
    plan = build_aggtrades_plan(symbol="BTCUSDT", mode=AggTradeMode.WS)
    assert plan.mode is AggTradeMode.WS
    assert plan.endpoint_reference == "@aggTrade"
    assert plan.capture_mode_label == "ws_live_capture_required"


def test_dry_run_plan_rejects_invalid_mode() -> None:
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(symbol="BTCUSDT", mode="not-a-mode")


def test_dry_run_plan_rejects_invalid_time_range() -> None:
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(
            symbol="BTCUSDT",
            mode=AggTradeMode.ARCHIVE,
            start_time_ms=1_000,
            end_time_ms=500,
        )
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(
            symbol="BTCUSDT",
            mode=AggTradeMode.ARCHIVE,
            start_time_ms=-1,
        )
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(
            symbol="BTCUSDT",
            mode=AggTradeMode.ARCHIVE,
            end_time_ms=-1,
        )


def test_dry_run_plan_rejects_unknown_symbol_without_explicit_extras() -> None:
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(symbol="SOLUSDT", mode=AggTradeMode.REST)


def test_dry_run_plan_admits_explicit_extra_symbol() -> None:
    plan = build_aggtrades_plan(
        symbol="SOLUSDT",
        mode=AggTradeMode.REST,
        explicit_extra_symbols={"SOLUSDT": "phase-4ac-core-symbol"},
    )
    assert plan.symbol == "SOLUSDT"


def test_dry_run_plan_rejects_lowercase_symbol() -> None:
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(symbol="btcusdt", mode=AggTradeMode.REST)


def test_dry_run_plan_rejects_non_aggtrades_dataset_family() -> None:
    with pytest.raises(AggTradePlanError):
        build_aggtrades_plan(
            symbol="BTCUSDT",
            mode=AggTradeMode.REST,
            dataset_family="microstructure_raw_bookticker_v001",
        )


# --------------------------------------------------------------------------- #
# Temp-path writer composition
# --------------------------------------------------------------------------- #


def _expected_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_temp_path_writer_writes_jsonl_and_summary(tmp_path: Path) -> None:
    target = tmp_path / "aggtrades.jsonl"
    payloads = [
        _rest_payload(a=1, T=1_700_000_000_001, m=False),
        _rest_payload(a=2, T=1_700_000_000_002, m=True),
        _rest_payload(a=3, T=1_700_000_000_003, m=False),
    ]
    result = write_validated_aggtrades_to_path(payloads, target)
    assert target.exists()
    sha_path = target.with_suffix(target.suffix + ".sha256")
    assert sha_path.exists()
    assert result.record_count == 3
    assert result.start_time_ms == 1_700_000_000_001
    assert result.end_time_ms == 1_700_000_000_003
    assert result.taker_side_buy_count == 2
    assert result.taker_side_sell_count == 1
    assert result.sha256 == _expected_sha(target)
    # Validate JSONL structure.
    lines = target.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in lines]
    assert len(parsed) == 3
    assert parsed[0]["taker_side"] == "BUY"
    assert parsed[1]["taker_side"] == "SELL"
    assert parsed[0]["event_time_ms_source"] == "trade_time"


def test_temp_path_writer_preserves_stream_event_time(tmp_path: Path) -> None:
    target = tmp_path / "stream.jsonl"
    payloads = [_stream_payload(a=1, E=1_700_000_001_000, T=1_700_000_000_500, m=True)]
    result = write_validated_aggtrades_to_path(payloads, target)
    parsed = json.loads(target.read_text(encoding="utf-8").splitlines()[0])
    assert parsed["event_time_ms"] == 1_700_000_001_000
    assert parsed["event_time_ms_source"] == "stream"
    assert parsed["taker_side"] == "SELL"
    assert result.taker_side_sell_count == 1


def test_temp_path_writer_rejects_project_data_microstructure(tmp_path: Path) -> None:
    forbidden = tmp_path / "data" / "microstructure" / "raw" / "aggtrades.jsonl"
    with pytest.raises(RawWriterPathError):
        write_validated_aggtrades_to_path([_rest_payload()], forbidden)


def test_temp_path_writer_rejects_invalid_payload_before_finalization(
    tmp_path: Path,
) -> None:
    target = tmp_path / "aggtrades.jsonl"
    payloads: list[Mapping[str, object]] = [
        _rest_payload(a=1, T=1_700_000_000_001),
        _rest_payload(a=2, p="-1.0"),  # invalid: negative price
    ]
    with pytest.raises(AggTradeValidationError):
        write_validated_aggtrades_to_path(payloads, target)
    # Final file must NOT exist (close() never ran).
    assert not target.exists()
    # No SHA file either.
    assert not target.with_suffix(target.suffix + ".sha256").exists()


def test_temp_path_writer_rejects_non_sequence_payloads(tmp_path: Path) -> None:
    target = tmp_path / "aggtrades.jsonl"
    with pytest.raises(AggTradesError):
        write_validated_aggtrades_to_path("not-a-sequence", target)  # type: ignore[arg-type]


def test_temp_path_writer_does_not_create_manifest(tmp_path: Path) -> None:
    target = tmp_path / "aggtrades.jsonl"
    write_validated_aggtrades_to_path([_rest_payload()], target)
    # No manifest path should appear adjacent to the data file.
    for entry in tmp_path.iterdir():
        assert "manifest" not in entry.name.lower()


def test_no_data_microstructure_directory_created(tmp_path: Path) -> None:
    """Negative regression: no test in this module ever causes
    the project ``data/microstructure/`` tree to be created."""
    project_root = Path(__file__).resolve().parents[3]
    assert not (project_root / "data" / "microstructure").exists()
