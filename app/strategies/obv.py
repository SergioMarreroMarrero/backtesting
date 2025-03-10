import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame, ma_period: int):
    df["obv"] = (np.sign(df["close"].diff()) * df["volume"]) \
                .fillna(0) \
                .cumsum()
    df['obv_ma'] = round(df["obv"].rolling(window=ma_period).mean(), 2)  # rolling pide la funcion de agregacion a aplicar
    df['signal'] = np.where(df['obv'] > df['obv_ma'], 1, -1)  # si obv esta por encima de la media movil long si no short
    df['pnl'] = df["close"].pct_change() * df['signal'].shift(1)
    # drawdown
    df["cum_pnl"] = df["pnl"].cumsum()
    df["max_cum_pnl"] = df["cum_pnl"].cummax()
    df["drawdown"] = df["max_cum_pnl"] - df["cum_pnl"]
    return df["pnl"].sum(), df["drawdown"].max()


