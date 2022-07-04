import datetime
from typing import Literal

from django.conf import settings


currencies_available = Literal[settings.CURRENCIES_AVAILABLE]


def get_exchange_rate_data(
        source_currency: currencies_available,
        exchanged_currency: currencies_available,
        valuation_date: datetime.date,
        provider):

    return provider.get_exchange_rate_data(source_currency, exchanged_currency, valuation_date)
