import requests
import ipdb
import settings
from core.exceptions import APICallError

class TechnicalIndicators:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.api_key = settings.APIKEY

    def _build_url(self, path):
        return f"{self.base_url}?{path}&apikey={self.api_key}"

    def _make_request(self, url):
        resp = requests.get(url)

        if resp.status_code == 200:
            return resp.json()

        raise APICallError(
            f"Não foi possivel consumir o serviço: STATUS_CODE"
            f"={resp.status_code}"
        )

    def sma(self, function, symbol, interval, time_period, series_type,  **kwargs):
        path = f"function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def ema(self, function, symbol, interval, time_period, series_type, **kwargs):
        path = f"function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp


# tech = TechnicalIndicators()
#
# d1 = tech.sma('SMA', 'IBM', 'weekly', '10', 'open')
# print('sma', d1['Technical Analysis: SMA'])
#
# d2 = tech.ema('EMA', 'IBM', 'weekly', '10', 'open')
# print('ema', d2['Technical Analysis: EMA'])