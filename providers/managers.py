from django.db import models


class ProviderQuerySet(models.QuerySet):
    def active(self, **kwargs):
        return self.filter(is_active=True).order_by('priority')


class ProviderManager(models.Manager):

    def get_queryset(self):
        return ProviderQuerySet(self.model, using=self._db)

    def active(self, **kwargs):
        return self.get_queryset().active(**kwargs)
