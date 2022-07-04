from django.contrib import admin

from providers.models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['is_active']
    list_display = ['id', 'name', 'priority', 'is_active']
