from typing import Union
import time
from exchanges.binance import BinanceClient
from exchanges.mexc import MexcClient
from logger_config import logger
from utils import ms_to_dt


def collect_all(client: Union[BinanceClient, MexcClient], exchange: str, symbol: str):

    oldest_ts, most_recent_ts = None, None
    # Initial Request
    '''
    timestamp_ms = int(time.time() * 1000)  # Milisegundos
    timestamp_ns = int(time.time() * 1e9)   # Nanosegundos
    time.time() * 1000  # 1707145667123  (en milisegundos)
    (time.time() * 1000) - 60000  # 1707145607123 (hace 1 minuto)
    ¿Por qué le quitamos el último minuto? Porque la vela actual no ha terminado, con lo cual queremos estar seguros
    que no estamos cogiendo la vela actual, ya que aun no ha cerrado.
    '''
    if oldest_ts is None:
        data = client.get_historical(symbol, end_time=int(time.time() * 1000 - 60000))
        if len(data) == 0:
            # podria pasar que no haya datos de ese simbolo en concreto
            logger.warning("%s %s: no initial data found", exchange, symbol)
        else:
            oldest_ts = data[0][0]
            most_recent_ts = data[-1][0]
            logger.info("%s %s: Collected %s initial data from %s to %s", exchange, symbol,
                        len(data), ms_to_dt(oldest_ts), ms_to_dt(most_recent_ts))
        return data

        # Insert into database



    # Most recent data

    # Older data
