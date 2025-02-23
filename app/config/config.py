from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from datetime import datetime
from app.utils import safe_load_yaml
from app.config import paths
from app.exchanges.binance import BinanceClient
from app.exchanges.mexc import MexcClient


# Strategies
STRATEGIES = [
    'obv',
    "ichimoku",
    "sup_res"
]


class ProgramExecutionConfig(BaseModel):
    mode: str = Field(..., pattern="^(data|backtest|optimize)", description="Execution mode")
    exchange: str = Field(..., pattern="^(binance|mexc)", description="Exchange name")
    symbol: str = Field(..., description="Trading pair symbol")

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        """Uppercase symbol assertion"""
        if v != v.upper():
            raise ValueError(f"Symbol '{v}' must be in uppercase (e.g. 'BTCUSDT'")
        return v

    def exchange_client(self) -> Union[BinanceClient, MexcClient]:
        if self.exchange == "binance":
            return BinanceClient(True)
        elif self.exchange == "mexc":
            return MexcClient(True)


class BacktestConfig(BaseModel):
    strategy: str = Field("obv", description="Strategy to use")
    timeframe: str = Field(..., description="Candlestick timeframe")
    from_time: Optional[datetime] = Field(None, description="Start time in format YYYY-MM-DD HH:MM:SS")
    to_time: Optional[datetime] = Field(None, description="End time in format YYYY-MM-DD HH:MM:SS")

    @field_validator("strategy")
    @classmethod
    def validate_strategy(cls, v: str) -> str:
        if v not in STRATEGIES:
            ValueError(f"Strategy '{v}' must belong to available strategies list: {"\n".join(strategy for strategy in STRATEGIES)}")
        return v


    @field_validator("from_time", "to_time", mode="before")
    @classmethod
    def validate_from_time(cls, v: Union[str, datetime]) -> Optional[datetime]:
        return None if v == "" else v

    def from_time_to_timestamp_milliseconds(self) -> int:
        return int(self.from_time.timestamp() * 1000) if isinstance(self.from_time, datetime) else 0

    def to_time_to_timestamp_milliseconds(self) -> int:
        return int(self.to_time.timestamp() * 1000) if isinstance(self.to_time, datetime) else int(datetime.now().timestamp() * 1000)


class ConfigSchema(BaseModel):
    program_execution: ProgramExecutionConfig
    backtest: Optional[BacktestConfig] = None


def get_validated_config(fil_name):
    raw_config = safe_load_yaml(paths.ProjectFiles.config_yaml(file_name=fil_name))
    return ConfigSchema(**raw_config)


# STRAT_PARAMS = {
#     "obv": {
#         "ma_period": {"name": "MA Period", "type": int},
#     },
#     "ichimoku": {
#         "kijun": {"name": "Kijun Period", "type": int},
#         "tenkan": {"name": "Tenkan Period", "type": int},
#     },
#     "sup_res": {
#         "min_points": {"name": "Min. Points", "type": int},
#         "min_diff_points": {"name": "Min. Difference between Points", "type": int},
#         "rounding_nb": {"name": "Rounding Number", "type": float},
#         "take_profit": {"name": "Take Profit %", "type": float},
#         "stop_loss": {"name": "Stop Loss %", "type": float},
#     },
# }

# Strategies
class OBV(BaseModel):
    ma_period: int = Field(9, description="MA Period")

class Ichimoku(BaseModel):
    kijun: int = Field(9, description="Kijun Period")
    tenkan: int = Field(26, description="Tenkan Period")

class SupportResistence(BaseModel):
    min_points: int = Field(3, description="Min. Points")
    min_diff_points: int = Field(7, description="Min. Difference between Points")
    rounding_nb: float = Field(400, description="Rounding Number")
    take_profit: float = Field(3, description="Take Profit %")
    stop_loss: float = Field(3, description="Stop Loss %")


class StratParams(BaseModel):
    obv: OBV
    ichimoku: Ichimoku
    sup_res: SupportResistence

    def __getitem__(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"Strategy {key} not found")


strat_params = {
    "obv": {"ma_period": 9},
    "ichimoku": {
        "kijun": 9,
        "tenkan": 26
    },
    "sup_res": {
        "min_points": 3,
        "min_diff_points": 7,
        "rounding_nb": 400,
        "take_profit": 3,
        "stop_loss": 3
    }
}

strat_params = StratParams(**strat_params)