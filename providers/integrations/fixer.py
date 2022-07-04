import datetime
import requests

from django.conf import settings

from providers.integrations.base import BaseProvider
from providers.utils import currencies_available


class FixerProvider(BaseProvider):

    def _api_request(self, url):
        headers = {'apikey': settings.FIXER_API_KEY}
        response = requests.request("GET", url, headers=headers, data={})
        return response

    def get_exchange_rate_data(
            self,
            source_currency: currencies_available,
            exchanged_currency: currencies_available,
            valuation_date: datetime.date) -> dict:

        currencies_available = ','.join(exchanged_currency)
        url = f'https://api.apilayer.com/fixer/{valuation_date}?symbols={currencies_available}&base={source_currency}'
        response = self._api_request(url)

        results = response.json()
        results = {**results['rates']} if results.get('success') else None

        return results
