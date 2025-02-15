from database import Hdf5Client
from app.utils import resample_timeframe
import strategies.obv


def run(exchange: str, symbol: str, strategy: str, tf: str, from_time: int, to_time: int):
    
    if strategy == "obv":
        h5_db = Hdf5Client(exchange)
        data = h5_db.get_data(symbol, from_time, to_time)
        data = resample_timeframe(data, tf)
        pnl = strategies.obv.backtest(data, 9)
        print(pnl)