from django.urls import path

from . import views

urlpatterns = [
    path('getWeather/', views.GetWeather.as_view(), name='getWeather'),
]