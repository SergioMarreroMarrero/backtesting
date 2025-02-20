from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from datetime import datetime
from app.utils import safe_load_yaml
from app.config import paths
from app.exchanges.binance import BinanceClient
from app.exchanges.mexc import MexcClient


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