from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.CharityLogin.as_view(), name='login'),
]
