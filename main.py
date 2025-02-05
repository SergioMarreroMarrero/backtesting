from logger_config import logger
from exchanges.binance import BinanceClient
from exchanges.mexc import MexcClient
from data_collector import collect_all
# import logging


# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
#
# formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)
# stream_handler.setLevel(logging.INFO)
#
# file_handler = logging.FileHandler("info.log")
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)
#
# logger.addHandler(stream_handler)
# logger.addHandler(file_handler)
# logger.debug('This a info log')

if __name__ == '__main__':
    # mode = input("Choose the program mode (data / backtest / optimize)").lower()
    mode = "data"
    futures = True
    exchange = 'binance'


    # while True:
    #     exchange = input("Choose an exchange: ").lower()
    #     if exchange not in ("mexc", "binance"):
    #         break

    if exchange == 'mexc':
        client = MexcClient(futures=futures)
    if exchange == 'binance':
        client = BinanceClient(futures=futures)

    data = collect_all(client=client, exchange=exchange, symbol='BTCUSDT')

    '''    
    data[0] 1738700460000
    data[1] 1738700520000
    data[-1] 1738790400000
    '''
