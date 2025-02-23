import backtester
from config import config
from app.data_collector import collect_all


if __name__ == '__main__':

    params = config.get_validated_config("sup_res")

    if params.program_execution.mode == "data":

        collect_all(params.program_execution.exchange_client(), params.program_execution.exchange, params.program_execution.symbol)

    elif params.program_execution.mode == "backtest":

        backtester.run(exchange=params.program_execution.exchange,
                       symbol=params.program_execution.symbol,
                       strategy=params.backtest.strategy,
                       tf=params.backtest.timeframe,
                       from_time=params.backtest.from_time_to_timestamp_milliseconds(),
                       to_time=params.backtest.to_time_to_timestamp_milliseconds())
