import pytest

from app.utils import convert_candlestick_timeframe_to_pandas_rule_options

# Prueba para valores correctos


@pytest.mark.parametrize("input_timeframe", "expected",[
    ("15m", "15Min"),
    ("2h", "2h"),
    ("3d", "3D"),
    ("1w", "1W"),
    ("6M", "6M")
])
def test_valid_timeframes(input_timeframe, expected):
    assert convert_candlestick_timeframe_to_pandas_rule_options(input_timeframe) == expected


@pytest.mark.parametrize('invalid_timeframe', [123, 32, (), {}])
def test_invalid_timeframes(invalid_timeframe):
    with pytest.raises(TypeError):
        convert_candlestick_timeframe_to_pandas_rule_options(invalid_timeframe)