from django.urls import path

from . import views

urlpatterns = [
    path('api/auth/login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]
