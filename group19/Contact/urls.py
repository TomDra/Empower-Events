from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_contact_form, name='submit_contact_form'),
]
