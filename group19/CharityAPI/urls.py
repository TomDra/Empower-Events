from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.CharityLogin.as_view(), name='loginCharity'),
    path('logout/', views.CharityLogout.as_view(), name='logoutCharity'),
]
