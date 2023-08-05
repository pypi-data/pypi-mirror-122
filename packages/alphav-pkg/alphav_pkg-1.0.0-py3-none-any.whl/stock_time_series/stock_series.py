import requests

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

    def daily_series(self, function, symbol, **kwargs):

        path = f"function={function}&symbol={symbol}"
        options = [f"{item[0]}={item[1]}" for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path) # gera url

        resp = self._make_request(url) # faz requisição e retorna response.json()

    def daily_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

    def weekly_series(self, *args, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

    def weekly_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

    def monthly_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

    def monthly_adjusted_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)

    def quote_series(self, function, symbol, **kwargs):

        path = f'function={function}&symbol={symbol}'
        options = [f'{item[0]}={item[1]}' for item in kwargs.items()]
        path = f"{path}&{'&'.join(options)}" if options else path

        url = self._build_url(path)

        resp = self._make_request(url)
