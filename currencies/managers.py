from django.db import models


class CurrencyExchangeRateQuerySet(models.QuerySet):

    def get_time_weighted_return(self, **kwargs):
        queryset = self.order_by('valuation_date')
        twr = 0

        for i, currency_exchange_rate in enumerate(queryset):
            rate_value = currency_exchange_rate.rate_value

            if i == 0:
                previous_rate_value = rate_value
                continue

            twr = (rate_value - previous_rate_value) / previous_rate_value

            previous_rate_value = rate_value

        return twr


class CurrencyExchangeRateManager(models.Manager):

    def get_queryset(self):
        return CurrencyExchangeRateQuerySet(self.model, using=self._db)

    def get_time_weighted_return(self, **kwargs):
        return self.get_queryset().get_time_weighted_return(**kwargs)
