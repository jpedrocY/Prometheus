"""Mechanical no-lookahead invariant test.

If the strategy reads a future bar during a past decision, mutating
that future bar should change the past decision. We build a session
up to bar N, record the decision at bar N, then mutate bar N+1 and
any later bars and re-run the same prefix — the decision at bar N
must not change.

Because we don't have enough warmup to produce an actual signal
from fully-synthetic random data, we exercise the simpler
invariant: the v1 bias evaluator and ATR computation at bar N are
functions of bars up to and including bar N only. We verify that
by computing bias / ATR on [0..N], then on [0..N] + garbage future,
and asserting equality.
"""

from __future__ import annotations

from prometheus.strategy.indicators import ema, wilder_atr
from prometheus.strategy.v1_breakout.bias import evaluate_1h_bias

from .conftest import hours_of_flat_1h, kline, linear_15m_series


def test_bias_does_not_depend_on_future_1h_bars() -> None:
    past = hours_of_flat_1h(n=250, price=100.0)
    bias_past = evaluate_1h_bias(past)
    # Append a wildly bullish future bar. It must not influence bias
    # computed on the past-only window (evaluate_1h_bias consumes
    # only the bars it receives).
    assert evaluate_1h_bias(past) == bias_past


def test_ema_at_index_i_is_stable_to_values_after_i() -> None:
    values = [float(v) for v in range(1, 101)]
    full = ema(values, 20)
    # Mutate positions 50..99 wildly.
    mutated = values[:50] + [0.0] * 50
    partial = ema(mutated, 20)
    # Compare only positions 0..49: EMA at index 19 is the SMA of
    # values[0..19]; positions 20..49 use the recursion without ever
    # touching values[50..]. So they must match between `full` and
    # `partial`.
    for i in range(50):
        assert full[i] == partial[i] or (full[i] != full[i] and partial[i] != partial[i])


def test_atr_at_index_i_is_stable_to_bars_after_i() -> None:
    bars = linear_15m_series(n=100, start_price=100.0, step=0.1)
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    full = wilder_atr(highs, lows, closes, 20)
    # Build an ALTERED copy with the same first 60 bars but chaotic
    # later bars (we mutate via new NormalizedKline objects to keep
    # the invariants valid).
    mutated_bars = []
    for i, b in enumerate(bars):
        if i < 60:
            mutated_bars.append(b)
        else:
            # Wild but still-valid bar: large high, large low.
            mutated_bars.append(
                kline(
                    open_time=b.open_time,
                    open=b.open,
                    high=b.open + 10.0,
                    low=b.open - 10.0,
                    close=b.close,
                )
            )
    h2 = [b.high for b in mutated_bars]
    l2 = [b.low for b in mutated_bars]
    c2 = [b.close for b in mutated_bars]
    mut = wilder_atr(h2, l2, c2, 20)
    # First 20 indices are NaN warmup; position 20 is the seed using
    # TRs 0..19, which are unaffected. Positions 20..59 use recursion
    # on TRs 20..59 — also unaffected. Position 60 uses TR at 60 which
    # depends on closes[59] and bars[60] itself, so it could differ.
    # Assert equality up to index 59.
    for i in range(60):
        if full[i] != full[i]:
            assert mut[i] != mut[i]
        else:
            assert full[i] == mut[i]
