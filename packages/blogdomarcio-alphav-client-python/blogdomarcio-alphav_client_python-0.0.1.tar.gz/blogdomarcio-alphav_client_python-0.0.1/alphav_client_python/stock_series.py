import requests
import ipdb
import settings
from core.exceptions import APICallError


class StockTimeSeries:

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

    def intraday_series(self, function, symbol, interval, **kwargs):

        path = f"function={function}&symbol={symbol}&interval={interval}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp


    def daily_series(self, function, symbol, **kwargs):

        path = f"function={function}&symbol={symbol}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path) # gera url

        resp = self._make_request(url) # faz requisição e retorna response.json()

        return resp

    def daily_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def weekly_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def weekly_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def monthly_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def monthly_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

    def quote_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'

        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp

#
# a = StockTimeSeries()
#
# d1 = a.intraday_series('TIME_SERIES_WEEKLY', 'IBM', '60min', slice='year1month1')
# print('intraday_series', d1)
#
#
# d2 = a.daily_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_series', d2)
#
# d3 = a.daily_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_adjusted_series', d3)
#
# d4 = a.weekly_series('TIME_SERIES_WEEKLY', 'IBM')
# print('weekly_series', d4)
#
#
# d5 = a.weekly_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_series', d5)
#
# d6 = a.monthly_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_adjusted_series', d6)
#
# d7 = a.weekly_adjusted_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_series', d7)
#
# d8 = a.monthly_series('TIME_SERIES_WEEKLY', 'IBM',)
# print('daily_adjusted_series', d8)
#


