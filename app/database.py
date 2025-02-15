import h5py
from typing import List, Tuple, Union
import numpy as np
from app.config.logger import logger
from app.config.paths import ProjectFiles
import pandas as pd
import time


class Hdf5Client:
    def __init__(self, exchange: str):
        self.hf = h5py.File(name=ProjectFiles.h5(exchange), mode="a")
        self.hf.flush()  # persist in disk even if we dont close the file

    def create_dataset(self, symbol: str):
        if symbol not in self.hf.keys():  # nos aseguramos que el datataset no exista
            self.hf.create_dataset(symbol, (0, 6), maxshape=(None, 6), dtype="float64")
            self.hf.flush()

    def write_data(self, symbol: str, data: List[Tuple]):
        data_array = np.array(data)
        """
        # shape es (0, 6) asi que estamos cogiendo el 0
        array([[0, 1, 2, 3, 4],
               [0, 1, 2, 3, 4]])
        La shape de este array (2, 5) -> 2 listas de 5 elementos cada una
        No entiendo muy bien pero el objetiivo es aumentar o informar de las filas (rows) del dataset
        para tocar las filas: axis = 0
        y basicamente le decimos que: a las que ya tiene: 0, le añada 1500 mas. (o las que sean)
        Me imagino que a medida que en la siguiente iteracion serán a las 1500 peus otras 1500
        y por eso ahcemos hf.symbol[0].shape[0] + data_array.shape[0]
        """

        # Para evitar que introducimos tipestamp que ya esta en la base de datos
        # [min_ts, max_ts] si el timestamp esta dentro de este rango lo sacamos
        min_ts, max_ts = self.get_first_last_timestamp(symbol)

        # Esto lo metemos para forzar que se cumplan las condiciones de abajo
        if min_ts is None:
            min_ts = float("inf")
            max_ts = 0

        filtered_data = []
        for d in data:
            if d[0] < min_ts:
                filtered_data.append(d)
            if d[0] > max_ts:
                filtered_data.append(d)

        if len(filtered_data) == 0:
            logger.info("%s: No data to insert", symbol)
            return None, None

        # De alguna manera estamos creando el espacio que vamos a usar de forma manual
        self.hf[symbol].resize(self.hf[symbol].shape[0] + data_array.shape[0], axis=0)
        # pillamos esas 1500 nuevas filas que hemos creado
        self.hf[symbol][-data_array.shape[0]:] = data_array
        self.hf.flush()

    def get_data(self, symbol: str, from_time: int, to_time: int) -> Union[None, pd.DataFrame]:

        start_query = time.time()
        existing_data = self.hf[symbol][:]
        if len(existing_data) == 0:
            return None

        data = sorted(existing_data, key=lambda x: x[0])
        data = np.array(data)
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df = df[(df["timestamp"] >= from_time & (df["timestamp"] <= to_time))]

        df["timestamp"] = pd.to_datetime(df["timestamp"].values.astype(np.int64), unit="ms")
        df.set_index("timestamp", drop=True, inplace=True)

        query_time = round(time.time()-start_query, 2)

        logger.info("Retrieved %s %s data from database in %s seconds", len(df.index), symbol, query_time)

        return df




    def get_first_last_timestamp(self, symbol: str) -> Union[Tuple[None, None], Tuple[float, float]]:

        existing_data = self.hf[symbol][:]
        if len(existing_data) == 0:
            return None, None

        first_ts = min(existing_data, key=lambda x: x[0])[0]
        last_ts = max(existing_data, key=lambda x: x[0])[0]

        return first_ts, last_ts




