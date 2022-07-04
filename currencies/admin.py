from django.contrib import admin
from import_export.admin import ImportMixin

from currencies.models import Currency, CurrencyExchangeRate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name']
    list_display = ['id', 'code', 'name', 'symbol']


@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(ImportMixin, admin.ModelAdmin):
    list_filter = ['valuation_date', 'source_currency', 'exchanged_currency']
    list_display = ['id', 'source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
