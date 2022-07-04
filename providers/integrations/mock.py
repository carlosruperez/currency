import datetime
import random
from decimal import Decimal

from django.conf import settings
from providers.integrations.base import BaseProvider
from providers.utils import currencies_available


class MockProvider(BaseProvider):

    def _api_request(self, url):
        pass

    def get_exchange_rate_data(
            self,
            source_currency: currencies_available,
            exchanged_currency: currencies_available,
            valuation_date: datetime.date) -> dict:

        rates = {}

        for currency in settings.CURRENCIES_AVAILABLE:
            rates.update({
                currency: Decimal(random.randrange(5, 20))/10
            })

        return rates
