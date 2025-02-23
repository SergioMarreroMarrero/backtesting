import datetime
import pandas as pd
import yaml
import re


def convert_candlestick_timeframe_to_pandas_rule_options(tf: str):
    """Convierte un timeframe al formato de pandas dinámicamente con regex."""
    match = re.fullmatch(r"(\d+)([mhdw])", tf)  # Extrae el número y la unidad
    if not match:
        raise ValueError(f"Invalid timeframe format: {tf}")

    value, unit = match.groups()

    # Mapear unidades al formato de pandas
    unit_map = {"m": "Min", "h": "h", "d": "D", 'w': 'W'}

    return f"{value}{unit_map[unit]}"


def ms_to_dt(ms: int) -> datetime.datetime:
    """
    Convertimos timestamp en milisegundos (milisegundos medidos desde 1 enero 1970) a formato datetime
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.UTC)


def resample_timeframe(data: pd.DataFrame, tf: str) -> pd.DataFrame:
    return data.resample(convert_candlestick_timeframe_to_pandas_rule_options(tf)).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )


def safe_load_yaml(file_path) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def round_to_nearest_tick_size_multiple(n: float, tick_size: float) -> float:
    """
    Esta función redondea valores al múltiplo más cercano de un tamaño de tick específico.
    La clave para entender esta funcion está en entender que al dividir por el tick_size estamos expresandolo en términos
    de tick_sizes, es decir, transformamos el espacio.
    Es decir:
    Si solo tenemos barras de 2 metros, una barra de 125:
    125 / 2 = 62.5 -> lo pasamos al espacio de barras
    round(62.5) = 62 barras -> quitamos las que sobran
    62 * 2 = 124 metros -> devolvemos al espacio origian

    En trading, los precios de los activos solo pueden moverse en incrementos mínimos llamados "ticks".
    Para garantizar que los precios calculados sean válidos y ejecutables en el mercado, es necesario ajustarlos al múltiplo más cercano del tamaño de tick.

    Diferencia con el redondeo estándar:
    - round(10.07) → 10 (redondeo convencional, pierde precisión en trading)
    - round(10.07 / tick_size) * tick_size → 10.05 (redondeo al múltiplo más cercano de tick_size = 0.05)

    Esto es esencial para evitar errores en órdenes y garantizar que los niveles de precios en estrategias algorítmicas
    sean compatibles con el mercado.
    :param n: numero a redondear
    :param tick_size: tamaño del tick
    :return: redondeo al multiplo mas cercano
    """
    return round(n / tick_size) * tick_size

