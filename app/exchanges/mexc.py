import requests
import logging
from typing import Dict, List, Optional

logger = logging.getLogger()


class MexcClient:
    """
    Para spot:
    https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#exchange-information
    Para futuros:
    https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Exchange-Information
    """
    def __init__(self, futures=False):

        self.futures = futures
        if self.futures:
            self._base_url = "https://fapi.binance.com"
        else:
            self._base_url = "https://api.binance.com"
        self.symbols = self._get_symbols()

    def _make_request(self, endpoint: str, query_parameters: Dict):
        try:
            response = requests.get(self._base_url + endpoint, params=query_parameters)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    "Error while making request to %s: %s (status code = %s)",
                    endpoint, response.json(), response.status_code
                )
                return None
        except Exception as e:
            logger.error("Connection error while making request to %s: %s", endpoint, e)

    def _get_symbols(self) -> List[str]:

        params = dict()
        endpoint = "/fapi/v1/exchangeInfo" if self.futures else "/api/v3/exchangeInfo"
        data = self._make_request(endpoint, params)
        symbols = [x["symbol"] for x in data["symbols"]]
        return symbols

    def get_historical_data(self,
                       symbol: str,
                       start_time: Optional[int] = None,
                       end_time: Optional[int] = None) -> List | None:

        params = dict()
        params["symbol"] = symbol
        params["interval"] = "1m"
        params["limit"] = 1500

        if start_time is not None:
            params["startTime"] = start_time

        if end_time is not None:
            params["endTime"] = end_time

        endpoint = "/fapi/v1/klines" if self.futures else "/api/v3/klines"
        raw_candles = self._make_request(endpoint, params)

        candles = []
        if raw_candles is not None:
            for c in raw_candles:
                # 0: open time, 1: open price, 2: high price, 3: low price, 4: close price, 5: volume
                # convert into tuple to load easier into HDF5
                candles.append((float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])))
            return candles
        else:
            return None


