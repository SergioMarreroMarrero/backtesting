import datetime
from exchanges.binance import BinanceClient
from exchanges.mexc import MexcClient
from data_collector import collect_all
import backtester
from app.utils import TF_EQUIV

if __name__ == '__main__':
    mode = input("Choose the yaml mode (data / yaml / optimize): ").lower()
    if mode == '':
        mode = 'yaml'
    while True:
        exchange = input("Choose an exchange: ").lower()
        if exchange == '':
            exchange = 'binance'
        if exchange in ["ftx", "binance"]:
            break

    if exchange == "binance":
        client = BinanceClient(True)
    elif exchange == "ftx":
        client = MexcClient(True)

    while True:
        symbol = input("Choose a symbol: ").upper()
        if symbol == '':
            symbol = 'BTCUSDT'
        if symbol in client.symbols:
            break

    if mode == "data":
        collect_all(client, exchange, symbol)
    elif mode == "yaml":

        # Strategy

        available_strategies = ["obv"]

        while True:
            strategy = input(f"fChoose a strategy ({', '.join(available_strategies)})").lower()
            if strategy == '':
                strategy = 'obv'

            if strategy in available_strategies:
                break

        # Timeframe

        while True:
            tf = input(f"Choose a timeframe: ({', '.join(TF_EQUIV.keys())}): ").lower()
            if tf == '':
                tf = '15m'
            if tf in TF_EQUIV.keys():
                break

        # From

        while True:
            from_time = input("Backtest from (yyyy-mm-dd) or Press Enter)")
            if from_time == "":
                from_time = 0
                break

            try:
                from_time = int(datetime.datetime.strptime(from_time, '%Y-%m-%d').timestamp() * 1000)
            except ValueError:
                continue

        # To

        while True:
            to_time = input("Backtest to (yyyy-mm-dd) or Press Enter)")
            if to_time == "":
                to_time = int(datetime.datetime.now().timestamp() * 1000)
                break

            try:
                to_time = int(datetime.datetime.strptime(to_time, '%Y-%m-%d').timestamp() * 1000)
            except ValueError:
                continue

        backtester.run(exchange, symbol, strategy, tf, from_time, to_time)
