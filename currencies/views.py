import json

from django.shortcuts import render
from django.views import View
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from currencies.models import Currency, CurrencyExchangeRate
from currencies.serializers import CurrencyExchangeRateSerializer


class CurrencyExchangeRateFilter(filters.FilterSet):
    source_currency = filters.CharFilter(field_name='source_currency', lookup_expr='code__exact')
    exchanged_currency = filters.CharFilter(field_name='exchanged_currency', lookup_expr='code__exact')
    date_from = filters.DateTimeFilter(field_name='valuation_date', lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name='valuation_date', lookup_expr='lte')

    class Meta:
        model = CurrencyExchangeRate
        fields = ['source_currency', 'date_from', 'date_to',]


class CurrencyExchangeRateViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
    permission_classes = [AllowAny]
    filter_class = CurrencyExchangeRateFilter
    filter_backends = [filters.DjangoFilterBackend]

    @action(methods=['GET'], detail=False, url_path='convert-rate-value')
    def convert_rate_value(self, request, *args, **kwargs):
        """
        Parameters: source_currency, amount, exchanged_currency.
        Expected response: an object containing at least the rate value between source and exchanges currencies.
        """

        if 'source_currency' not in self.request.query_params or \
                'exchanged_currency' not in self.request.query_params or \
                'amount' not in self.request.query_params:
            return Response({'msg': 'Missing required params'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        instance = queryset.order_by('-valuation_date').first()

        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response_data = {
            'converted_rate_value': instance.convert_rate_value(request.query_params.get('amount', 0))
        }

        return Response(response_data)

    @action(methods=['GET'], detail=False, url_path='time-weighted-rate')
    def get_twr(self, request, *args, **kwargs):
        """
        Parameters: source_currency, amount, exchanged_currency, start_date
        Expected response: an object containing at least the rate value between source and exchanges currencies.
        """
        if 'source_currency' not in self.request.query_params or \
                'exchanged_currency' not in self.request.query_params or \
                'amount' not in self.request.query_params or \
                'date_from' not in self.request.query_params:
            return Response({'msg': 'Missing required params'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())

        response_data = {
            'twr': queryset.get_time_weighted_return()
        }

        return Response(response_data)


class ExchangeRateEvolutionAdmin(View):
    template = 'admin_exchange_rate_evolution.html'

    def get(self, request):
        context = {
            'currencies': Currency.objects.all(),
            'days': ['2022-07-3', '2022-07-2', '2022-07-1', '2022-06-30', '2022-06-29', '2022-06-28', ]
        }
        return render(request, self.template, context=context)

    def post(self, request):
        base_currency_exchange_rates = CurrencyExchangeRate.objects.filter(
            valuation_date__gte=request.POST['date_from'],
            valuation_date__lte=request.POST['date_to'],
        )

        days = []
        datasets = []
        for i in range(1, 6):
            source_currency = request.POST[f'source_currency_{i}']
            exchanged_currency = request.POST[f'exchanged_currency_{i}']
            currency_exchange_rates = base_currency_exchange_rates.filter(
                source_currency__code=source_currency,
                exchanged_currency__code=exchanged_currency
            ).order_by('valuation_date')

            if i == 1:
                days = [rate.valuation_date.strftime('%Y-%m-%d') for rate in currency_exchange_rates]

            if currency_exchange_rates:

                datasets.append({
                    'data': [float(rate.rate_value) for rate in currency_exchange_rates],  # TODO improve
                    'label': f'{source_currency}-{exchanged_currency}'
                })

        context = {
            'currencies': Currency.objects.all(),
            'days': days,
            'datasets': datasets
        }

        return render(request, self.template, context=context)
