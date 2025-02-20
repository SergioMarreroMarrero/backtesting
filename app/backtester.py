from database import Hdf5Client
from app.utils import resample_timeframe
from strategies import obv, ichimoku, support_resistance
from config.logger import logger


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):
    
    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = obv.backtest(data, 9)
        print(pnl)

    elif strategy == 'ichimoku':

        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = ichimoku.backtest(data, tenkan_period=9, kijun_period=26)
        print(pnl)

    elif strategy == 'sup_res':

        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = support_resistance.backtest(data)
        print(pnl)
