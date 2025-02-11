from typing import Union
import time
from exchanges.binance import BinanceClient
from exchanges.mexc import MexcClient
from logger_config import logger
from utils import ms_to_dt, resample_timeframe
from database import Hdf5Client


def collect_all(client: Union[BinanceClient, MexcClient], exchange: str, symbol: str):
    """
    Realmente lo que tenemos es lo siguiente
    suponemos que los datos son estos numeros:
    collector = []
    list_to_collect = 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16

    En la primera tanta cojo los 5 primeros.
    Mas tarde, si quiero recorrer la lista hacia alante o detrás es lo que marca la diferencia
    del metodo a seguir


    ----------------------------------------


    :param client:
    :param exchange:
    :param symbol:
    :return:
    """
    h5_db = Hdf5Client(exchange=exchange)
    h5_db.create_dataset(symbol=symbol)
    data = h5_db.get_data(symbol, from_time=0, to_time=int(time.time()*1000))

    oldest_ts, most_recent_ts = h5_db.get_first_last_timestamp(symbol=symbol)

    # Initial Request
    if oldest_ts is None:
        # print(int(time.time()*1000))
        # print(ms_to_dt(int(time.time()*1000)))

        data = client.get_historical_data(symbol, end_time=int(time.time() * 1_000) - 60_000)
        # print(ms_to_dt(int(data[-1][0])))
        if len(data) == 0:
            # podria pasar que no haya datos de ese simbolo en concreto
            logger.warning("%s %s: no initial data found", exchange, symbol)
            return
        else:
            h5_db.write_data(symbol=symbol, data=data)
            logger.info("%s %s: Collected %s initial data from %s to %s", exchange, symbol,
                        len(data), ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))



        oldest_ts = data[0][0]
        most_recent_ts = data[-1][0]
        # Insert into database
    # Most recent data
    # sumamos 1 minuto (60000 ms) para no tener la misma vela con la que empezamos en start_time
    data_to_insert = []
    while True:
        data = client.get_historical_data(symbol, start_time=int(most_recent_ts + 60_000))

        # print(ms_to_dt(int(most_recent_ts)))
        # print(ms_to_dt(int(data[-1][0])))

        if data is None:
            time.sleep(4)  # If overwhelming the API wait 4 seconds and repeat
            continue

        if len(data) < 2:  # la ultima llamada trae menos de 2 tuplas (no ponemos cero porque hacia la derecha no es estatico)
            logger.info("%s %s: Stopped recent data collection because no data was found after %s", exchange, symbol, ms_to_dt(data[-1][0]))
            break

        data = data[:-1]  # no queremos la ultima vela, porque aun no ha cerrado y lo mas probable es que cambie

        data_to_insert = data_to_insert + data
        if len(data_to_insert) > 10_000:  ## lo hacemos para no abusar del metodo write_data
            h5_db.write_data(symbol=symbol, data=data)
            data_to_insert.clear()
            # logger.info("%s %s: Collected %s recent data from %s to %s", exchange, symbol,
            #             len(data_to_insert), ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        if data[-1][0] > most_recent_ts:
            # Update most_rescent_ts
            most_recent_ts = data[-1][0]

        logger.info("%s %s: Collected %s recent data from %s to %s", exchange, symbol,
                    len(data), ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)
    h5_db.write_data(symbol=symbol, data=data)
    data_to_insert.clear()

    # Older data
    if data[0][0] < oldest_ts:
        oldest_ts = data[0][0]
    while True:
        data = client.get_historical_data(symbol, end_time=int(oldest_ts - 60000))

        if data is None:
            time.sleep(4)  # If overwhelming the API wait 4 seconds and repeat
            continue

        if len(data) == 0:
            logger.info("%s %s: Stopped older data collection because no data was found before %s", exchange, symbol, data[0][0])
            break
        data_to_insert = data_to_insert + data
        if len(data_to_insert) > 10_000:
            h5_db.write_data(symbol=symbol, data=data)
            data_to_insert.clear()

        if data[0][0] < oldest_ts:
            oldest_ts = data[0][0]

        logger.info("%s %s: Collected %s older data from %s to %s", exchange, symbol,
                    len(data), ms_to_dt(data[0][0]), ms_to_dt(data[-1][0]))

        time.sleep(1.1)

    h5_db.write_data(symbol=symbol, data=data)
    data_to_insert.clear()
