from django.urls import path
from .views import TradesAPIView

urlpatterns = [
    path('trades/', TradesAPIView.as_view(), name='api_trade'),
    path('trades/<int:id>', TradesAPIView.as_view(), name='api_trade_indexed')
]