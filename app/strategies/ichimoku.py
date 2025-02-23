import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, tenkan_period: int, kijun_period: int):

    # Tenkan Sen: Short-term signal line
    df["rolling_min_tenkan"] = df["low"].rolling(window=tenkan_period).min()
    df["rolling_max_tenkan"] = df["high"].rolling(window=tenkan_period).max()
    df["tenkan_sen"] = (df["rolling_max_tenkan"] + df["rolling_min_tenkan"]) / 2
    df.drop(["rolling_max_tenkan", "rolling_min_tenkan"], axis=1, inplace=True)

    # Kijun Sen: Long-term signal line

    df["rolling_min_kijun"] = df["low"].rolling(window=kijun_period).min()
    df["rolling_max_kijun"] = df["high"].rolling(window=kijun_period).max()
    df["kijun_sen"] = (df["rolling_min_kijun"] + df["rolling_max_kijun"]) / 2
    df.drop(["rolling_min_kijun", "rolling_max_kijun"], axis=1, inplace=True)

    # Senkou span A
    df["senkou_span_a"] = (df["tenkan_sen"] + df["kijun_sen"]) / 2

    # Senkou span B
    df["rolling_min_senkou"] = df["low"].rolling(window=kijun_period * 2).min()
    df["rolling_max_senkou"] = df["high"].rolling(window=kijun_period * 2).max()
    df["senkou_span_b"] = ((df["rolling_max_senkou"] + df["rolling_min_senkou"]) / 2).shift(kijun_period)
    df.drop(["rolling_min_senkou", "rolling_max_senkou"], axis=1, inplace=True)

    # Chikou Span:: Confirmation line
    df["chikou_span"] = df["close"].shift(kijun_period)

    df.dropna(inplace=True)

    # Signal
    df["tenkan_minus_kijun"] = df["tenkan_sen"] - df["kijun_sen"]
    df["prev_tenkan_minus_kijun"] = df["tenkan_minus_kijun"].shift(1)

    # Esto es cuando se da el cruce
    long_signal = (
        (df["tenkan_minus_kijun"] > 0) & (df["prev_tenkan_minus_kijun"] > 0) & # bullish moving agerages crossover
        (df["close"] > df["senkou_span_a"]) & # close price over senkou_span_a
        (df["close"] > df["senkou_span_b"]) & # close price over senkou_span_b
        (df["close"] > df["chikou_span"])     # close price over chikou_span
    )

    short_signal = (
        (df["tenkan_minus_kijun"] < 0) & (df["prev_tenkan_minus_kijun"] < 0) & # bearish moving agerages crossover
        (df["close"] < df["senkou_span_a"]) & # close price below senkou_span_a
        (df["close"] < df["senkou_span_b"]) & # close price below senkou_span_b
        (df["close"] < df["chikou_span"])     # close price below chikou_span
    )

    # si hay señal alcista: 1
    # si hay señal bajista: -1
    # si no hay ninguna señal: 0
    df["signal"] = np.where(long_signal, 1, np.where(short_signal, 1, 0))

    df = df[df["signal"] != 0].copy()
    df["pnl"] = df["close"].pct_change() * df["signal"].shift(1)

    # drawdown
    df["cum_pnl"] = df["pnl"].cumsum()
    df["max_cum_pnl"] = df["cum_pnl"].cummax()
    df["drawdown"] = df["max_cum_pnl"] - df["cum_pnl"]

    return df["pnl"].sum(), df["drawdown"].max()

    # return df


