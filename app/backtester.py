from database import Hdf5Client
from app.utils import resample_timeframe
from strategies import obv, ichimoku, support_resistance
from config.logger import logger
from config.config import strat_params


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):

    params = strat_params[strategy]

    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = obv.backtest(data, ma_period=params.ma_period)
        print(pnl)

    elif strategy == 'ichimoku':

        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = ichimoku.backtest(data, tenkan_period=params.tenkan_period, kijun_period=params.kijun_period)
        print(pnl)

    elif strategy == 'sup_res':

        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = support_resistance.backtest(data,
                                          min_points=params.min_points,
                                          min_diff_points=params.min_diff_points,
                                          rounding_nb=params.rounding_nb,
                                          take_profit=params.take_profit,
                                          stop_loss=params.stop_loss)
        print(pnl)




