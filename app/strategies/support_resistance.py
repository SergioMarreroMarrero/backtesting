import pandas as pd
import numpy as np


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)


def backtest(df: pd.DataFrame,
             min_points: int,
             min_diff_points: int,
             rounding_nb: float,
             take_profit: float,
             stop_loss: float):
    """
    Esta función redondea valores al múltiplo más cercano de un tamaño de tick específico.

    En trading, los precios de los activos solo pueden moverse en incrementos mínimos llamados "ticks".
    Para garantizar que los precios calculados sean válidos y ejecutables en el mercado, es necesario ajustarlos al múltiplo más cercano del tamaño de tick.

    Diferencia con el redondeo estándar:
    - round(10.07) → 10 (redondeo convencional, pierde precisión en trading)
    - round(10.07 / tick_size) * tick_size → 10.05 (redondeo al múltiplo más cercano de tick_size = 0.05)

    Esto es esencial para evitar errores en órdenes y garantizar que los niveles de precios en estrategias algorítmicas
    sean compatibles con el mercado.

    :param df:
    :param min_points: puntos minimos para considerarlo un suporte/resistencia
    :param min_diff_points: minimo puntos de separacion
    :param rounding_nb:
    :param take_profit:
    :param stop_loss:
    :return:
    """

    df["rounded_high"] = round(df["high"] / rounding_nb) * rounding_nb
    df["rounded_low"] = round(df["low"] / rounding_nb) * rounding_nb
    return df["pnl"].sum()

    # return df


