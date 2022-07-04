from rest_framework import routers

from currencies import views

router = routers.DefaultRouter()

router.register(r'currency-exchange-rates', views.CurrencyExchangeRateViewSet)
urlpatterns = []
urlpatterns += router.urls
