import datetime
import backtester

from pydantic import BaseModel, Field
from datetime import datetime
from config import config



if __name__ == '__main__':

    params = config.get_validated_config("1")

    # if params["mode"] == "data":
    #
    #     collect_all(client, exchange, symbol)
    #
    # elif params["mode"] == "backtest":

    #
    backtester.run(exchange=params.program_execution.exchange,
                   symbol=params.program_execution.symbol,
                   strategy=params.backtest.strategy,
                   tf=params.backtest.timeframe,
                   from_time=params.backtest.from_time_to_timestamp_milliseconds(),
                   to_time=params.backtest.to_time_to_timestamp_milliseconds())
    # if config.PROGRAM_EXECUTION['exchange'] == "binance":
    #     client = BinanceClient(True)
    # elif config.PROGRAM_EXECUTION['exchange'] == "mexc":
    #     client = MexcClient(True)
    #
    #
    # assert config.PROGRAM_EXECUTION['symbol'] in client.symbols, "..."
    #
    #
    #
    # if mode == "data":
    #     collect_all(client, exchange, symbol)
    # elif mode == "yaml":
    #
    #     # Strategy
    #
    #     available_strategies = ["obv"]
    #
    #     while True:
    #         strategy = input(f"fChoose a strategy ({', '.join(available_strategies)})").lower()
    #         if strategy == '':
    #             strategy = 'obv'
    #
    #         if strategy in available_strategies:
    #             break
    #
    #     # Timeframe
    #
    #     while True:
    #         tf = input(f"Choose a timeframe: ({', '.join(TF_EQUIV.keys())}): ").lower()
    #         if tf == '':
    #             tf = '15m'
    #         if tf in TF_EQUIV.keys():
    #             break
    #
    #     # From
    #
    #     while True:
    #         from_time = input("Backtest from (yyyy-mm-dd) or Press Enter)")
    #         if from_time == "":
    #             from_time = 0
    #             break
    #
    #         try:
    #             from_time = int(datetime.datetime.strptime(from_time, '%Y-%m-%d').timestamp() * 1000)
    #         except ValueError:
    #             continue
    #
    #     # To
    #
    #     while True:
    #         to_time = input("Backtest to (yyyy-mm-dd) or Press Enter)")
    #         if to_time == "":
    #             to_time = int(datetime.datetime.now().timestamp() * 1000)
    #             break
    #
    #         try:
    #             to_time = int(datetime.datetime.strptime(to_time, '%Y-%m-%d').timestamp() * 1000)
    #         except ValueError:
    #             continue


