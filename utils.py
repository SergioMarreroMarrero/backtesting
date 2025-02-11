import datetime
import pandas as pd

TF_EQUIV = {
    "1m": "1Min",
    "5m": "5Min",
    "15m": "15Min",
    "30m": "30Min",
    "1h": "1h",
    "4h": "4h",
    "12h": "12h",
    "1d": "D",

}

def ms_to_dt(ms: int)-> datetime.datetime:
    """
    Convertimos timestamp en milisegundos (milisegundos medidos desde 1 enero 1970) a formato datetime
    :param ms:
    :return:
    """
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.UTC)

def resample_timeframe(data: pd.DataFrame, tf: str) -> pd.DataFrame:
    return data.resample(TF_EQUIV[tf]).agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
    )
