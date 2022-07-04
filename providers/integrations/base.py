import datetime

from abc import ABC, abstractmethod
from providers.utils import currencies_available


class BaseProvider(ABC):

    @abstractmethod
    def _api_request(self, url):
        pass

    @abstractmethod
    def get_exchange_rate_data(
            self,
            source_currency: currencies_available,
            exchanged_currency: currencies_available,
            valuation_date: datetime.date) -> dict:
        pass
