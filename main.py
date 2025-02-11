from logger_config import logger
from exchanges.binance import BinanceClient
from exchanges.mexc import MexcClient
from data_collector import collect_all


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

