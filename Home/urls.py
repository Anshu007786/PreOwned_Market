from django.urls import path, include
from Home.views import Index

urlpatterns = [
    path('', Index, name="index")
]
