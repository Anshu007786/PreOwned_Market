from django.urls import path, include
from MarketApp.views import GetProducts

urlpatterns = [
    path('<slug>/', GetProducts, name="products"),
]
