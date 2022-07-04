import datetime

from django.core.management.base import BaseCommand

from currencies.models import CurrencyExchangeRate


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--from_date', type=str)
        parser.add_argument('--to_date', type=str)

    def handle(self, *args, **options):

        if from_date := options.get('from_date'):
            from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        else:
            from_date = datetime.date.today()

        if to_date := options.get('to_date'):
            to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        else:
            to_date = datetime.date.today()
        CurrencyExchangeRate.load_exchange_rates_data(from_date=from_date, to_date=to_date)
