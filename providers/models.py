from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from importlib import import_module

from providers.managers import ProviderManager


class Provider(models.Model):

    PROVIDERS = (
        (settings.FIXER_PROVIDER, 'Fixer.io'),
        (settings.MOCK_PROVIDER, 'Mock'),
    )
    name = models.CharField(choices=PROVIDERS, max_length=32, unique=True)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    objects = ProviderManager()

    class Meta:
        ordering = ['priority', 'name']

    def __str__(self):
        return self.name

    def get_adapter(self):
        adapter_path = dict(settings.PROVIDER_ADAPTERS).get(self.name)

        try:
            mod_name, class_name = adapter_path.rsplit('.', 1)
            mod = import_module(mod_name)
        except ImportError as e:
            raise ImproperlyConfigured(f'Error importing provider adapter backend module {mod_name}: "{e}"')
        try:
            adapter_class = getattr(mod, class_name)
        except AttributeError as e:
            raise ImproperlyConfigured(f'Module "{mod_name}" does not define a "{class_name}" class: "{e}"')
        return adapter_class()
