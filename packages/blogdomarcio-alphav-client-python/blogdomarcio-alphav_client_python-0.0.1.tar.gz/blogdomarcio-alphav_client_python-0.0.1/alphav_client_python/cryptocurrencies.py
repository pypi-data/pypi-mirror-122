import requests
import ipdb
import settings
from core.exceptions import APICallError


class CryptoCurrencies:
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

    def currency_exchange_rate(self, function, from_currency, to_currency, **kwargs):
        path = f"function={function}&from_currency={from_currency}&to_currency={to_currency}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

        return resp


# crypto = CryptoCurrencies()
# #
# d1 = crypto.currency_exchange_rate('CURRENCY_EXCHANGE_RATE', 'BTC', 'CNY',)
# print('Realtime Currency Exchange Rate', d1['Realtime Currency Exchange Rate'])
