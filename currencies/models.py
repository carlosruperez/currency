import datetime
from decimal import Decimal
from django.db import models

from currencies.managers import CurrencyExchangeRateManager
from currencies.utils import get_inversed_rate_value
from providers.models import Provider
from providers.utils import get_exchange_rate_data

from_date = datetime.date
to_date = datetime.date


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.code


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency, related_name='exchanges', on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)
    objects = CurrencyExchangeRateManager()

    class Meta:
        unique_together = ['valuation_date', 'source_currency', 'exchanged_currency']
        ordering = ['-valuation_date']

    def __str__(self):
        return f'#{self.id} {self.valuation_date} - {self.source_currency}/{self.exchanged_currency}'

    @staticmethod
    def get_conversion_through(source_currency, exchanged_currency, through_currency, valuation_date):
        exchange_rate_through_currency = CurrencyExchangeRate.objects.get(
            source_currency=source_currency,
            exchanged_currency=through_currency,
            valuation_date=valuation_date
        )

        exchange_rate = CurrencyExchangeRate.objects.get(
            source_currency=through_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date
        )

        return exchange_rate_through_currency.rate_value * exchange_rate.rate_value

    @staticmethod
    def load_exchange_rates_data(from_date: datetime.date, to_date: datetime.date):
        providers = Provider.objects.active()

        days = (to_date - from_date).days

        source_currency = Currency.objects.get(code='EUR')
        currency_codes = ['EUR', 'CHF', 'USD', 'GBP']
        currencies = Currency.objects.filter(code__in=currency_codes).exclude(code=source_currency.code)

        for day in range(days + 1):

            valuation_date = from_date + datetime.timedelta(days=day)

            for provider in providers:
                provider_adapter = provider.get_adapter()

                data = get_exchange_rate_data(
                    source_currency=source_currency.code,
                    exchanged_currency=list(set(currency_codes) - set(source_currency.code)),
                    valuation_date=valuation_date,
                    provider=provider_adapter
                )

                if data:

                    for exchanged_currency in currencies:
                        rate_value = data[exchanged_currency.code]

                        CurrencyExchangeRate.objects.update_or_create(
                            source_currency=source_currency,
                            exchanged_currency=exchanged_currency,
                            valuation_date=valuation_date,
                            defaults={
                                'rate_value': rate_value
                            }
                        )

                        CurrencyExchangeRate.objects.update_or_create(
                            source_currency=exchanged_currency,
                            exchanged_currency=source_currency,
                            valuation_date=valuation_date,
                            defaults={
                                'rate_value': get_inversed_rate_value(rate_value)
                            }
                        )
                    break

            for currency in currencies:
                for exchanged_currency in currencies:
                    if currency == exchanged_currency:
                        continue

                    rate_value = CurrencyExchangeRate.get_conversion_through(
                        source_currency=currency,
                        exchanged_currency=exchanged_currency,
                        through_currency=source_currency,
                        valuation_date=valuation_date
                    )

                    if rate_value:
                        CurrencyExchangeRate.objects.update_or_create(
                            source_currency=currency,
                            exchanged_currency=exchanged_currency,
                            valuation_date=valuation_date,
                            defaults={
                                'rate_value': rate_value
                            }
                        )

    def convert_rate_value(self, amount: float):
        return self.rate_value * Decimal(amount)
