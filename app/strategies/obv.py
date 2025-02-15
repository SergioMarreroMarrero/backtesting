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

    '''
    tiempo 1 | signal: long
    tiempo 2 | pnl: % close tiempo 1 / tiempo 2 teniendo en cuenta que en tiempo 1 entramos en long
    Con lo cual: para calcular el obv en tiempo 2 tenemos que hacerlo segun la seña del tiempo 1. Por eso usamos shift(1)
    '''
    df['pnl'] = df["close"].pct_change() * df['signal'].shift(1)

    return df["pnl"].sum()


