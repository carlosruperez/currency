from rest_framework import serializers

from currencies.models import Currency, CurrencyExchangeRate


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['code', 'name', 'symbol']


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = CurrencySerializer()
    exchanged_currency = CurrencySerializer()

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value', ]


class CurrencyExchangeRateConvertSerializer(serializers.ModelSerializer):
    source_currency = CurrencySerializer()
    exchanged_currency = CurrencySerializer()
    convert_rate_value = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value', 'convert_rate_value']

    def get_convert_rate_value(self, obj):
        return obj.convert_rate_value()
